#!/usr/bin/env python3
"""Offline verifier for Bounty #8: MSU review archive bridge and staging surfaces."""

import argparse
import copy
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CANDIDATE_BODY_HASH = "eed30437a612ee77e2c2a48aacee9ce093267840cab093c972b17060455cd285"
CANDIDATE_BODY_LEN = 508

CANONICAL_ARTICLE = "https://www.msureporter.com/2018/06/06/book-review-talking-as-fast-as-i-can/"
MEMGATOR_2020 = "https://memgator.cs.odu.edu/memento/proxy/20201020093440/www.msureporter.com/2018/06/06/book-review-talking-as-fast-as-i-can/"
MEMGATOR_2024 = "https://memgator.cs.odu.edu/memento/proxy/20240623185914/www.msureporter.com/2018/06/06/book-review-talking-as-fast-as-i-can/"
MARKDOWN_PROXY = "https://markdown.new/www.msureporter.com/2018/06/06/book-review-talking-as-fast-as-i-can/"
BROWSE_BRIDGE = "https://wikiservice.at/probier/wiki.cgi?action=browse&id=AgentMsuLaurenGrahamArchiveX927"


def require(ok, msg):
    if not ok:
        raise ValueError(msg)


def sha256_bytes(b):
    return hashlib.sha256(b).hexdigest()


def check_file(raw, spec):
    require(len(raw) == spec["bytes"], f"Byte count mismatch: expected {spec['bytes']}, got {len(raw)}")
    require(sha256_bytes(raw) == spec["sha256"], f"SHA256 mismatch: expected {spec['sha256']}, got {sha256_bytes(raw)}")


def check_candidate_body(raw_bytes):
    require(len(raw_bytes) == CANDIDATE_BODY_LEN, f"Candidate body length mismatch: {len(raw_bytes)}")
    require(sha256_bytes(raw_bytes) == CANDIDATE_BODY_HASH, "Candidate body hash mismatch")
    text = raw_bytes.decode("utf-8")
    require(CANONICAL_ARTICLE in text, "Canonical article URL missing from candidate body")
    require(MEMGATOR_2020 in text, "MemGator 2020 URL missing from candidate body")
    require(MARKDOWN_PROXY in text, "Markdown proxy URL missing from candidate body")
    require(BROWSE_BRIDGE.replace("&", "&amp;") in text, "Browse bridge URL missing from candidate body")
    require("Lauren Graham" in text, "Unredacted author name missing from candidate body")
    return text


def check_clock_separation(timeline):
    entities = timeline.get("entities", {})
    orig = entities.get("original_publication", {})
    require(orig.get("publication_date") == "2018-06-06", "Original publication date must be 2018-06-06")
    require(orig.get("clock_basis") == "article_dateline", "Original publication clock basis mismatch")

    snapshots = entities.get("archive_snapshots", {})
    s2020 = snapshots.get("memento_20201020093440", {})
    require(s2020.get("timestamp_raw") == "20201020093440", "Memento 2020 raw timestamp mismatch")
    require(s2020.get("timestamp_iso") == "2020-10-20T09:34:40Z", "Memento 2020 ISO timestamp mismatch")

    s2024 = snapshots.get("memento_20240623185914", {})
    require(s2024.get("timestamp_raw") == "20240623185914", "Memento 2024 raw timestamp mismatch")
    require(s2024.get("timestamp_iso") == "2024-06-23T18:59:14Z", "Memento 2024 ISO timestamp mismatch")

    stagings = entities.get("staging_publications", [])
    require(len(stagings) == 5, f"Expected 5 staging entries, got {len(stagings)}")
    for st in stagings:
        t = st.get("time_raw")
        require(t.startswith("2026-07-01"), f"Staging timestamp {t} must be 2026-07-01")
        require(st.get("time_basis") in ["source_export_reqlog", "clock_conflict_site_offset"], "Invalid staging clock basis")

    admin = entities.get("administrative_event", {})
    require(admin.get("action") == "deletion", "Administrative action must be deletion")
    require(admin.get("timestamp") == "2026-07-13T23:41:00+01:00", "Administrative deletion timestamp mismatch")


def check_locators_and_routes(routes_data):
    target = routes_data.get("target_article", {})
    require(target.get("url") == CANONICAL_ARTICLE, "Canonical article URL mismatch")
    require(target.get("publication_date") == "2018-06-06", "Canonical article publication date mismatch")

    routes = routes_data.get("archive_routes", [])
    route_ids = [r.get("route_id") for r in routes]
    require("memgator_2020" in route_ids, "memgator_2020 route missing")
    require("memgator_2024" in route_ids, "memgator_2024 route missing")
    require("allorigins_wayback_2024" in route_ids, "allorigins_wayback_2024 route missing")
    require("markdown_new_proxy" in route_ids, "markdown_new_proxy route missing")
    require("probier_browse_bridge" in route_ids, "probier_browse_bridge route missing")

    bridge = next(r for r in routes if r.get("route_id") == "probier_browse_bridge")
    require(bridge.get("parameters", {}).get("action") == "browse", "Browse bridge action parameter mismatch")
    require(bridge.get("parameters", {}).get("id") == "AgentMsuLaurenGrahamArchiveX927", "Browse bridge id mismatch")


def check_caveat_compliance(timeline):
    stagings = timeline.get("entities", {}).get("staging_publications", [])
    cand = next(s for s in stagings if s.get("record_id") == "fe42c43fcbe846cff3321d23053e9c75")
    base = next(s for s in stagings if s.get("record_id") == "7cf5549dddec014835e4ad964ebd0b28")

    require(cand.get("underlying_page_relationship") == "unredacted_standalone_counterpart_revision", "Candidate must be classified as counterpart revision")
    require(cand.get("counterpart_record_id") == base.get("record_id"), "Candidate must reference base record ID")
    require(base.get("anonymized") is True and base.get("anonymization_token") == "[Person15]", "Base record must be anonymized with [Person15]")
    require(cand.get("anonymized") is False and cand.get("unredacted_name") == "Lauren Graham", "Candidate must expose unredacted Lauren Graham")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--negative-controls", action="store_true", help="Run negative controls")
    args = parser.parse_args()

    manifest_path = ROOT / "manifest.json"
    require(manifest_path.exists(), "manifest.json not found")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    files = {}
    for rel_path, spec in manifest.get("files", {}).items():
        p = (ROOT / rel_path).resolve()
        require(p.is_relative_to(ROOT), f"File escaped package root: {rel_path}")
        require(p.exists(), f"File does not exist: {rel_path}")
        raw = p.read_bytes()
        check_file(raw, spec)
        files[rel_path] = raw

    body_bytes = files["evidence/candidate-body.txt"]
    check_candidate_body(body_bytes)

    timeline = json.loads(files["evidence/timeline-clocks.json"].decode("utf-8"))
    check_clock_separation(timeline)

    routes = json.loads(files["evidence/locators-and-routes.json"].decode("utf-8"))
    check_locators_and_routes(routes)

    check_caveat_compliance(timeline)

    cand_rec = json.loads(files["evidence/candidate-record-fe42c43f.json"].decode("utf-8"))
    require(cand_rec.get("id") == "fe42c43fcbe846cff3321d23053e9c75", "Candidate record ID mismatch")
    require(cand_rec.get("metadata", {}).get("body_sha256") == CANDIDATE_BODY_HASH, "Candidate record body SHA256 mismatch")
    require(cand_rec.get("metadata", {}).get("body_len") == CANDIDATE_BODY_LEN, "Candidate record body length mismatch")

    result = {
        "status": "PASS",
        "evidence_files_verified": len(files),
        "candidate_record_id": "fe42c43fcbe846cff3321d23053e9c75",
        "candidate_body_bytes": len(body_bytes),
        "candidate_body_sha256": sha256_bytes(body_bytes),
        "clock_separation_verified": True,
        "complete_query_bundle_verified": True,
        "caveat_underlying_page_verified": True,
        "negative_controls_passed": 0
    }

    if args.negative_controls:
        rejected = []

        def reject(name, fn):
            try:
                fn()
            except (ValueError, KeyError, TypeError):
                rejected.append(name)
            else:
                raise ValueError(f"Control unexpectedly accepted: {name}")

        reject("tampered candidate body bytes", lambda: check_candidate_body(b"Tampered " + body_bytes[9:]))
        reject("wrong candidate body hash", lambda: check_file(body_bytes, {"bytes": len(body_bytes), "sha256": "0" * 64}))

        t_bad = copy.deepcopy(timeline)
        t_bad["entities"]["original_publication"]["publication_date"] = "2026-07-01"
        reject("conflated publication date with staging date", lambda: check_clock_separation(t_bad))

        t_bad2 = copy.deepcopy(timeline)
        t_bad2["entities"]["archive_snapshots"]["memento_20201020093440"]["timestamp_raw"] = "20260701101038"
        reject("conflated memento snapshot with staging timestamp", lambda: check_clock_separation(t_bad2))

        t_bad3 = copy.deepcopy(timeline)
        t_bad3["entities"]["staging_publications"][3]["underlying_page_relationship"] = "independent_distinct_page"
        reject("violating caveat by counting unredacted counterpart as independent distinct page", lambda: check_caveat_compliance(t_bad3))

        r_bad = copy.deepcopy(routes)
        r_bad["archive_routes"][4]["parameters"]["action"] = "edit"
        reject("tampered browse bridge query action", lambda: check_locators_and_routes(r_bad))

        result["negative_controls_passed"] = len(rejected)
        result["negative_controls_rejected"] = rejected

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
