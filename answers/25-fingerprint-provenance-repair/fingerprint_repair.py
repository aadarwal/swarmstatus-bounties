#!/usr/bin/env python3
"""Verify source-qualified fingerprint links and repair a NEW database copy.

No network requests. Original observations, records, declarations and IDs are
preserved; the only existing column changed is fingerprint_observations.record_id.
"""
import argparse
from collections import Counter, defaultdict
import csv
import hashlib
import json
from pathlib import Path
import sqlite3
from urllib.parse import quote, unquote

VERSION = "source-qualified-fingerprint-v1"
REPOSITORIES = {"WikiAgentSwarmInvestigation": "JoshuaDavid/WikiAgentSwarmInvestigation",
                "collusion-wiki-link-shorteners": "brausepulver/collusion-wiki-link-shorteners"}


class VerificationError(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise VerificationError(message)


def digest(path):
    hasher = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            hasher.update(block)
    return hasher.hexdigest()


def text_hash(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest() if text else ""


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def source_locator(path, commit, line):
    parts = Path(path).parts
    try:
        index = parts.index("repos")
        repo = REPOSITORIES[parts[index + 1]]
        relative = "/".join(parts[index + 2:])
        return f"https://github.com/{repo}/blob/{commit}/{quote(relative, safe='/')}#L{line}"
    except (ValueError, KeyError, IndexError):
        return ""


def resolve_observations(db, workspace):
    """Return an exhaustive verified plan; any ambiguity/content mismatch fails closed.

    Matching uses source path + checksum + stable alias/revision ID. Neither CSV
    line numbers nor body hashes alone identify a record. Original raw files are
    checked independently of the DB, including full unnormalized destinations.
    """
    workspace = Path(workspace).resolve()
    observations = [dict(row) for row in db.execute("SELECT * FROM fingerprint_observations ORDER BY id")]
    groups = defaultdict(list)
    for observation in observations:
        meta = json.loads(observation["metadata_json"])
        require(meta.get("local_source") == observation["source_path"], "Observation source path disagrees with declaration")
        require(meta.get("source_kind") in {"shortener_creation", "wiki_revision"}, "Unsupported source kind")
        require(meta.get("fingerprint") == observation["fingerprint"], "Fingerprint declaration disagrees")
        require(meta.get("line") == observation["source_line"], "Source line declaration disagrees")
        require(bool(meta.get("record_key")), "Missing stable source identity")
        observation["meta"] = meta
        groups[(observation["source_path"], meta["source_kind"])].append(observation)
    results = []
    for (relative, kind), hits in sorted(groups.items()):
        path = (workspace / relative).resolve()
        require(path.is_relative_to(workspace), "Source escapes acquisition workspace")
        source_hash = digest(path)
        sources = [dict(row) for row in db.execute("SELECT * FROM sources WHERE path=? AND sha256=?", (relative, source_hash))]
        require(len(sources) == 1, f"Source absent, ambiguous, or checksum changed: {relative}")
        source = sources[0]
        wanted = {hit["meta"]["record_key"] for hit in hits}
        raw_by_id = defaultdict(list)
        if kind == "shortener_creation":
            with path.open(encoding="utf-8", newline="") as stream:
                reader = csv.DictReader(stream)
                require({"alias", "url", "timestamp"}.issubset(reader.fieldnames or []), "CSV columns missing")
                for ordinal, raw in enumerate(reader, 1):
                    # csv.reader.line_num reports physical lines, unlike enumerate.
                    end = reader.line_num
                    start = end - sum(str(value).count("\n") for value in raw.values() if value is not None)
                    if raw.get("alias") in wanted:
                        raw_by_id[raw["alias"]].append(dict(raw=raw, ordinal=ordinal, physical_start=start, physical_end=end))
        else:
            with path.open(encoding="utf-8") as stream:
                for line, value in enumerate(stream, 1):
                    if not value.strip():
                        continue
                    raw = json.loads(value)
                    if raw.get("rev_id") in wanted:
                        raw_by_id[raw["rev_id"]].append(dict(raw=raw, ordinal=line, physical_start=line, physical_end=line))
        candidates = defaultdict(list)
        field = "alias" if kind == "shortener_creation" else "rev_id"
        expected_type = "shortener_link" if kind == "shortener_creation" else "wiki_revision"
        query = """SELECT r.id,r.object_id,r.record_key,r.source_url,r.body_hash,r.time_raw,r.time_basis,
                   o.platform,o.object_key,json_extract(r.metadata_json,?) stable_id
                   FROM records r JOIN objects o ON o.id=r.object_id WHERE r.source_id=? AND r.record_type=?"""
        for row in db.execute(query, ("$." + field, source["id"], expected_type)):
            if row["stable_id"] in wanted:
                candidates[row["stable_id"]].append(dict(row))
        for hit in hits:
            meta = hit["meta"]
            stable_id = meta["record_key"]
            require(len(raw_by_id[stable_id]) == 1, f"Original source identity missing or ambiguous: {stable_id}")
            require(len(candidates[stable_id]) == 1, f"Retained source identity missing or ambiguous: {stable_id}")
            raw_info = raw_by_id[stable_id][0]
            raw = raw_info["raw"]
            resolved = candidates[stable_id][0]
            record = dict(db.execute("SELECT * FROM records WHERE id=?", (resolved["id"],)).fetchone())
            record_meta = json.loads(record["metadata_json"])
            require(record["record_key"] == str(raw_info["ordinal"]), f"Retained row provenance mismatch: {stable_id}")
            require(record["body_hash"] == text_hash(record["body"] or ""), f"Retained body checksum mismatch: {stable_id}")
            hash_basis = "declared hash equals retained UTF-8 text hash"
            if kind == "shortener_creation":
                platform, alias = meta.get("object_key", "").split("/", 1)
                require(alias == stable_id and resolved["platform"] == "shortener:" + platform
                        and resolved["object_key"] == alias, f"Object identity mismatch: {stable_id}")
                require(meta.get("destination") == raw["url"] == record["body"] == record_meta.get("url"),
                        f"Exact raw destination mismatch: {stable_id}")
                require(record_meta.get("alias") == alias, f"Alias declaration mismatch: {stable_id}")
                require(meta.get("reported_time") == raw["timestamp"] == record["time_raw"], f"Source time mismatch: {stable_id}")
                destinations = {row[0] for row in db.execute("""SELECT u.raw_url FROM record_urls ru JOIN urls u ON u.id=ru.url_id
                                                           WHERE ru.record_id=? AND ru.role='destination'""", (resolved["id"],))}
                require(raw["url"].strip() in destinations, f"Destination provenance link absent: {stable_id}")
            else:
                require(raw.get("page_id") == meta.get("object_key") == resolved["object_key"], f"Wiki page mismatch: {stable_id}")
                require(raw.get("body", "") == record["body"], f"Original JSONL body mismatch: {stable_id}")
                require(raw.get("body_sha256") == meta.get("body_hash") == record_meta.get("body_sha256"),
                        f"Source-declared body hash mismatch: {stable_id}")
                require(raw.get("time") == meta.get("reported_time") == record["time_raw"], f"Wiki source time mismatch: {stable_id}")
                if meta.get("body_hash") != record["body_hash"]:
                    try:
                        recovered = record["body"].encode("latin1")
                        recovered.decode("utf8")
                    except (UnicodeEncodeError, UnicodeDecodeError):
                        recovered = b""
                    hash_basis = ("source hash equals Latin-1 encoded exported text / recovered UTF-8 bytes"
                                  if recovered and hashlib.sha256(recovered).hexdigest() == meta.get("body_hash")
                                  else "unexplained source-declared versus retained-text hash discrepancy")
            prior = db.execute("""SELECT r.id,r.body,r.body_hash,r.source_url,o.object_key,r.time_raw,r.time_basis
                                  FROM records r JOIN objects o ON o.id=r.object_id WHERE r.id=?""", (hit["record_id"],)).fetchone()
            prior = dict(prior) if prior else {}
            results.append(dict(observation_id=hit["id"], fingerprint=hit["fingerprint"], source_kind=kind,
                                original_record_id=hit["record_id"], resolved_record_id=resolved["id"],
                                changed=hit["record_id"] != resolved["id"], intended_identity=stable_id,
                                intended_object_key=meta["object_key"], original_object_key=prior.get("object_key"),
                                original_source_url=prior.get("source_url"), resolved_source_url=record["source_url"],
                                original_body_hash=prior.get("body_hash"), resolved_body_hash=record["body_hash"],
                                declared_body_hash=meta.get("body_hash"), hash_basis=hash_basis,
                                original_destination=prior.get("body") if kind == "shortener_creation" else None,
                                exact_destination=meta.get("destination"), source_path=relative, source_sha256=source_hash,
                                commit_sha=source["commit_sha"], source_locator=source_locator(relative, source["commit_sha"], raw_info["physical_start"]),
                                declared_source_line=hit["source_line"], source_data_row=raw_info["ordinal"],
                                physical_start_line=raw_info["physical_start"], physical_end_line=raw_info["physical_end"],
                                original_time_raw=prior.get("time_raw"), original_time_basis=prior.get("time_basis"),
                                time_raw=record["time_raw"], time_basis=record["time_basis"],
                                original_csv_row_sha256=(hashlib.sha256(canonical(raw).encode()).hexdigest() if kind == "shortener_creation" else None),
                                observation_metadata_sha256=hashlib.sha256(hit["metadata_json"].encode()).hexdigest()))
    return sorted(results, key=lambda item: item["observation_id"])


def table_digest(db, table, omit=()):
    info = list(db.execute('PRAGMA table_info("' + table + '")'))
    columns = [row[1] for row in info if row[1] not in omit]
    primary = [row[1] for row in sorted(info, key=lambda item: item[5]) if row[5]]
    ordering = ','.join('"' + column + '"' for column in primary) if primary else 'rowid'
    require(all(column.replace("_", "").isalnum() for column in columns), "Unexpected SQL identifier")
    hasher = hashlib.sha256()
    count = 0
    for row in db.execute('SELECT ' + ','.join('"' + col + '"' for col in columns) + ' FROM "' + table + '" ORDER BY ' + ordering):
        value = canonical([{"hex": item.hex()} if isinstance(item, bytes) else item for item in row]).encode()
        hasher.update(len(value).to_bytes(8, "big")); hasher.update(value); count += 1
    return dict(rows=count, sha256=hasher.hexdigest(), columns=columns)


def derived(db):
    counts = [dict(row) for row in db.execute("""SELECT f.fingerprint,count(*) observations,
          count(DISTINCT r.id) retained_records,count(DISTINCT r.object_id) objects,
          count(DISTINCT r.body_hash) distinct_retained_bodies,count(DISTINCT o.platform) platforms
          FROM fingerprint_observations f JOIN records r ON r.id=f.record_id JOIN objects o ON o.id=r.object_id
          GROUP BY f.fingerprint ORDER BY f.fingerprint""")]
    memberships = [dict(row) for row in db.execute("""SELECT f.fingerprint,r.object_id,o.platform,o.object_key,
          f.id observation_id,r.id record_id,r.source_url,r.body_hash,r.time_raw,r.time_basis
          FROM fingerprint_observations f JOIN records r ON r.id=f.record_id JOIN objects o ON o.id=r.object_id
          ORDER BY f.fingerprint,r.object_id,f.id""")]
    return dict(family_counts=counts, memberships=memberships)


def write_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n")


def write_jsonl(path, values):
    path.write_text("".join(canonical(value) + "\n" for value in values))


def repair_copy(source, out, workspace, report):
    source, out, workspace, report = map(lambda value: Path(value).resolve(), (source, out, workspace, report))
    require(source != out, "Refusing to modify the input database")
    require(not out.exists(), "Output must be a NEW file; refusing overwrite")
    protected = [workspace / "outputs/database/research.sqlite3", workspace / "outputs/swarm-evidence/data/local/research.sqlite3"]
    require(out not in protected, "Refusing a live database output path")
    source_sha = digest(source)
    original = sqlite3.connect(source.as_uri() + "?mode=ro", uri=True)
    original.row_factory = sqlite3.Row
    original.execute("PRAGMA query_only=ON")
    plan = resolve_observations(original, workspace)
    before = derived(original)
    # No table except the pointer column is allowed to change. Source declarations
    # are separately hashed even though they live beside the repaired pointer.
    protected_tables = [row[0] for row in original.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
                        if row[0] not in {"fingerprint_observations", "fingerprint_mapping_repairs"}]
    before_hashes = {table: table_digest(original, table) for table in protected_tables}
    immutable_observations = table_digest(original, "fingerprint_observations", ("record_id",))
    out.parent.mkdir(parents=True, exist_ok=True)
    repaired = sqlite3.connect(out)
    repaired.row_factory = sqlite3.Row
    try:
        original.backup(repaired)
        repaired.execute("PRAGMA foreign_keys=ON")
        repaired.execute("""CREATE TABLE IF NOT EXISTS fingerprint_mapping_repairs(
            observation_id INTEGER PRIMARY KEY,original_record_id TEXT,resolved_record_id TEXT,
            repair_version TEXT,evidence_json TEXT)""")
        for item in plan:
            if not item["changed"]:
                continue
            repaired.execute("INSERT INTO fingerprint_mapping_repairs VALUES(?,?,?,?,?)",
                             (item["observation_id"], item["original_record_id"], item["resolved_record_id"], VERSION, canonical(item)))
            changed = repaired.execute("UPDATE fingerprint_observations SET record_id=? WHERE id=? AND record_id IS ?",
                                       (item["resolved_record_id"], item["observation_id"], item["original_record_id"]))
            require(changed.rowcount == 1, "Observation changed since planning")
        repaired.commit()
        verification = resolve_observations(repaired, workspace)
        require(not any(row["changed"] for row in verification), "Some mappings are still unresolved")
        after_hashes = {table: table_digest(repaired, table) for table in protected_tables}
        require(before_hashes == after_hashes, "An unrelated table changed")
        require(immutable_observations == table_digest(repaired, "fingerprint_observations", ("record_id",)), "Original observation fields changed")
        require(repaired.execute("PRAGMA integrity_check").fetchone()[0] == "ok", "Integrity check failed")
        require(not repaired.execute("PRAGMA foreign_key_check").fetchall(), "Foreign-key check failed")
        after = derived(repaired)
    except Exception:
        repaired.close(); original.close(); out.unlink(missing_ok=True)
        raise
    repaired.close(); original.close()
    require(digest(source) == source_sha, "Original database changed during repair")
    changes = [row for row in plan if row["changed"]]
    old_memberships = {(row["fingerprint"], row["object_id"]) for row in before["memberships"]}
    new_memberships = {(row["fingerprint"], row["object_id"]) for row in after["memberships"]}
    membership_diff = [dict(fingerprint=fingerprint, object_id=oid, change=direction)
                       for direction, group in (("removed", old_memberships-new_memberships), ("added", new_memberships-old_memberships))
                       for fingerprint, oid in sorted(group)]
    summary = dict(repair_version=VERSION, source_database_sha256=source_sha, repaired_database_sha256=digest(out),
                   verified_observations=len(plan), corrected_observations=len(changes),
                   unchanged_observations=len(plan)-len(changes), changed_by_kind=dict(Counter(row["source_kind"] for row in changes)),
                   changed_by_fingerprint=dict(Counter(row["fingerprint"] for row in changes)),
                   changed_destination=sum(row["original_destination"] != row["exact_destination"] for row in changes),
                   identical_destination_wrong_alias=sum(row["original_destination"] == row["exact_destination"] for row in changes),
                   declared_hash_exceptions=sum(bool(row["declared_body_hash"]) and row["declared_body_hash"] != row["resolved_body_hash"] for row in plan),
                   unrelated_tables_identical=True, original_observation_fields_identical=True,
                   original_database_identical=True, integrity_check="ok", foreign_key_violations=0,
                   membership_pairs_removed=len(old_memberships-new_memberships), membership_pairs_added=len(new_memberships-old_memberships),
                   before_counts=before["family_counts"], after_counts=after["family_counts"])
    report.mkdir(parents=True, exist_ok=True)
    write_json(report / "summary.json", summary)
    write_jsonl(report / "all_observation_checks.jsonl", plan)
    write_jsonl(report / "corrected_links.jsonl", changes)
    write_jsonl(report / "declared_hash_exceptions.jsonl", [row for row in plan if row["declared_body_hash"] and row["declared_body_hash"] != row["resolved_body_hash"]])
    write_json(report / "unchanged_table_hashes.json", before_hashes)
    write_json(report / "immutable_observation_hash.json", immutable_observations)
    write_jsonl(report / "membership_provenance.before.jsonl", before["memberships"])
    write_jsonl(report / "membership_provenance.after.jsonl", after["memberships"])
    write_jsonl(report / "changed_object_memberships.jsonl", membership_diff)
    return summary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--workspace", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(repair_copy(args.source, args.out, args.workspace, args.report), indent=2))


if __name__ == "__main__":
    main()
