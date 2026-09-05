#!/usr/bin/env python3
"""Offline regression tests; fixtures never touch either acquisition database."""
import csv
import json
from pathlib import Path
import sqlite3
import tempfile
import unittest
from unittest import mock
import fingerprint_repair as repair

SCHEMA = """
CREATE TABLE sources(id INTEGER PRIMARY KEY,path TEXT,sha256 TEXT,commit_sha TEXT);
CREATE TABLE objects(id INTEGER PRIMARY KEY,platform TEXT,object_key TEXT);
CREATE TABLE records(id TEXT PRIMARY KEY,source_id INTEGER,object_id INTEGER,record_key TEXT,record_type TEXT,
 source_url TEXT,body TEXT,body_hash TEXT,time_raw TEXT,time_basis TEXT,metadata_json TEXT);
CREATE TABLE urls(id INTEGER PRIMARY KEY,raw_url TEXT);
CREATE TABLE record_urls(record_id TEXT,url_id INTEGER,role TEXT);
CREATE TABLE fingerprint_observations(id INTEGER PRIMARY KEY,fingerprint TEXT,record_id TEXT REFERENCES records,
 source_path TEXT,source_line INTEGER,metadata_json TEXT);
CREATE TABLE candidate_links(id INTEGER PRIMARY KEY,reason_json TEXT);
INSERT INTO candidate_links VALUES(1,'{"source":"unchanged original candidate"}');
"""
CSV_PATH = "work/repos/collusion-wiki-link-shorteners/raw_artifacts/shorteners/vanderbi.lt/links.csv"


class RepairTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.path = self.root / "original.sqlite3"
        self.db = sqlite3.connect(self.path)
        self.db.row_factory = sqlite3.Row
        self.db.executescript(SCHEMA)
        self.addCleanup(self.db.close)
        self.rows = [dict(alias="intended", url="https://example.test/data?a=1&b=2", timestamp="2026-06-21 01:00:00", title="Original"),
                     dict(alias="next-alias", url="https://example.test/unrelated", timestamp="2026-06-21 01:01:00", title="Next")]
        self.add_csv(CSV_PATH, self.rows, 1)
        self.add_hit(1, "r1-2", CSV_PATH, "shortener_creation", "intended", "vanderbi.lt/intended", 2,
                     destination=self.rows[0]["url"], reported_time=self.rows[0]["timestamp"])

    def add_csv(self, relative, rows, sid):
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", newline="") as stream:
            writer = csv.DictWriter(stream, fieldnames=["alias", "url", "timestamp", "title"])
            writer.writeheader(); writer.writerows(rows)
        self.db.execute("INSERT INTO sources VALUES(?,?,?,?)", (sid, relative, repair.digest(path), "0"*40))
        for i, row in enumerate(rows, 1):
            rid, oid, uid = f"r{sid}-{i}", sid*100+i, sid*100+i
            self.db.execute("INSERT INTO objects VALUES(?,?,?)", (oid,"shortener:vanderbi.lt",row["alias"]))
            self.db.execute("INSERT INTO records VALUES(?,?,?,?,?,?,?,?,?,?,?)", (rid,sid,oid,str(i),"shortener_link",
                "https://vanderbi.lt/"+row["alias"]+"+",row["url"],repair.text_hash(row["url"]),row["timestamp"],"raw_unzoned",json.dumps(row)))
            self.db.execute("INSERT INTO urls VALUES(?,?)", (uid,row["url"]))
            self.db.execute("INSERT INTO record_urls VALUES(?,?,?)", (rid,uid,"destination"))
        self.db.commit()

    def add_hit(self, fid, rid, relative, kind, identity, obj, line, **extra):
        meta = dict(fingerprint="fixture_task", local_source=relative, source_kind=kind,
                    record_key=identity, object_key=obj, line=line, **extra)
        self.db.execute("INSERT INTO fingerprint_observations VALUES(?,?,?,?,?,?)", (fid,"fixture_task",rid,relative,line,json.dumps(meta)))
        self.db.commit()

    def plan(self):
        return repair.resolve_observations(self.db, self.root)

    def test_wrong_next_alias_resolves_by_exact_source_identity(self):
        plan = self.plan()
        self.assertEqual(plan[0]["resolved_record_id"], "r1-1")
        self.assertTrue(plan[0]["changed"])
        self.assertNotEqual(plan[0]["original_destination"], plan[0]["exact_destination"])

    def test_duplicate_destination_does_not_make_wrong_alias_correct(self):
        body = self.rows[0]["url"]
        self.db.execute("UPDATE records SET body=?,body_hash=? WHERE id='r1-2'", (body,repair.text_hash(body)))
        result = self.plan()[0]
        self.assertTrue(result["changed"])
        self.assertEqual(result["original_destination"], result["exact_destination"])

    def test_same_alias_in_another_source_is_not_joined(self):
        tail = CSV_PATH.replace("vanderbi.lt/", "vanderbi.lt_tail/")
        self.add_csv(tail, [dict(self.rows[0], url="https://different.test/")], 2)
        self.assertEqual(self.plan()[0]["resolved_record_id"], "r1-1")

    def test_line_numbers_do_not_select_identity(self):
        meta = json.loads(self.db.execute("SELECT metadata_json FROM fingerprint_observations").fetchone()[0])
        meta["line"] = 1000
        self.db.execute("UPDATE fingerprint_observations SET source_line=1000,metadata_json=?", (json.dumps(meta),))
        result = self.plan()[0]
        self.assertEqual(result["resolved_record_id"], "r1-1")
        self.assertEqual(result["physical_start_line"], 2)
        self.assertEqual(result["declared_source_line"], 1000)

    def test_multiline_csv_preserves_physical_range_without_using_it_as_key(self):
        path = self.root / CSV_PATH
        self.rows[0]["title"] = "First line\nSecond line"
        with path.open("w", newline="") as stream:
            writer = csv.DictWriter(stream, fieldnames=self.rows[0].keys());writer.writeheader();writer.writerows(self.rows)
        self.db.execute("UPDATE sources SET sha256=? WHERE id=1", (repair.digest(path),))
        result = self.plan()[0]
        self.assertEqual((result["source_data_row"], result["physical_start_line"], result["physical_end_line"]), (1,2,3))

    def test_ambiguous_retained_identity_fails_closed(self):
        self.db.execute("INSERT INTO records SELECT 'duplicate',source_id,object_id,record_key,record_type,source_url,body,body_hash,time_raw,time_basis,metadata_json FROM records WHERE id='r1-1'")
        with self.assertRaisesRegex(repair.VerificationError, "ambiguous"):
            self.plan()

    def test_source_checksum_change_is_rejected(self):
        with (self.root / CSV_PATH).open("a") as stream:
            stream.write("\n")
        with self.assertRaisesRegex(repair.VerificationError, "checksum changed"):
            self.plan()

    def test_raw_destination_mismatch_is_rejected_even_with_same_alias(self):
        self.db.execute("UPDATE records SET body=?,body_hash=? WHERE id='r1-1'", ("https://example.test/data?b=2&a=1",repair.text_hash("https://example.test/data?b=2&a=1")))
        with self.assertRaisesRegex(repair.VerificationError, "Exact raw destination mismatch"):
            self.plan()

    def test_missing_intended_record_does_not_fall_back_to_equal_body(self):
        self.db.execute("DELETE FROM records WHERE id='r1-1'")
        self.db.execute("UPDATE records SET body=?,body_hash=? WHERE id='r1-2'", (self.rows[0]["url"],repair.text_hash(self.rows[0]["url"])))
        with self.assertRaisesRegex(repair.VerificationError, "identity missing"):
            self.plan()

    def test_wiki_jsonl_does_not_receive_csv_header_adjustment(self):
        relative = "work/repos/WikiAgentSwarmInvestigation/agent-logs/probier/revisions.jsonl"
        body = "Original wiki body"
        raw = dict(rev_id="probier~Page@1",page_id="probier/Page",body=body,body_sha256=repair.text_hash(body),time="2026-06-21T01:00:00Z")
        path = self.root / relative;path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(raw)+"\n")
        self.db.execute("INSERT INTO sources VALUES(?,?,?,?)", (3,relative,repair.digest(path),"1"*40))
        self.db.execute("INSERT INTO objects VALUES(301,'wiki:probier','probier/Page')")
        self.db.execute("INSERT INTO records VALUES(?,?,?,?,?,?,?,?,?,?,?)", ("wiki-first",3,301,"1","wiki_revision","https://collusion.wiki/explorer/page/probier~Page.html#rev-1",body,repair.text_hash(body),raw["time"],"site_declared_offset",json.dumps(raw)))
        self.add_hit(2,"wiki-first",relative,"wiki_revision",raw["rev_id"],raw["page_id"],1,body_hash=raw["body_sha256"],reported_time=raw["time"])
        wiki = self.plan()[1]
        self.assertFalse(wiki["changed"])
        self.assertEqual(wiki["source_data_row"],1)

    def test_copy_repair_preserves_originals_all_other_tables_and_is_idempotent(self):
        self.db.commit()
        before = repair.digest(self.path)
        out = self.root / "repaired.sqlite3"
        summary = repair.repair_copy(self.path,out,self.root,self.root/"report")
        self.assertEqual(summary["corrected_observations"],1)
        self.assertEqual(repair.digest(self.path),before)
        with sqlite3.connect(out) as updated:
            updated.row_factory=sqlite3.Row
            self.assertFalse(any(item["changed"] for item in repair.resolve_observations(updated,self.root)))
            self.assertEqual(updated.execute("SELECT original_record_id FROM fingerprint_mapping_repairs").fetchone()[0],"r1-2")
            self.assertEqual(repair.table_digest(updated,"candidate_links"),repair.table_digest(self.db,"candidate_links"))
            self.assertEqual(repair.table_digest(updated,"records"),repair.table_digest(self.db,"records"))
        second = repair.repair_copy(out,self.root/"second.sqlite3",self.root,self.root/"second-report")
        self.assertEqual(second["corrected_observations"],0)

    def test_no_overwrite_or_live_path_is_allowed(self):
        with self.assertRaises(repair.VerificationError):
            repair.repair_copy(self.path,self.path,self.root,self.root/"report")
        with self.assertRaises(repair.VerificationError):
            repair.repair_copy(self.path,self.root/"outputs/database/research.sqlite3",self.root,self.root/"report")

    def test_failed_validation_removes_partial_copy(self):
        self.db.commit()
        plan = self.plan()
        out = self.root/"failed.sqlite3"
        with mock.patch.object(repair,"resolve_observations",side_effect=[plan,repair.VerificationError("injected verification failure")]):
            with self.assertRaisesRegex(repair.VerificationError,"injected"):
                repair.repair_copy(self.path,out,self.root,self.root/"report")
        self.assertFalse(out.exists())


if __name__ == "__main__":
    unittest.main(verbosity=2)
