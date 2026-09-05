#!/usr/bin/env python3
"""Verify the public repair ledger directly against the frozen public CSV.

No database or network access is needed. URL strings are never fetched.
"""
import argparse
from collections import Counter
import csv
import hashlib
import json
from pathlib import Path
from urllib.parse import unquote


def row_id(source_path, source_hash, ordinal):
    return hashlib.sha256((source_path + "\0" + source_hash + "\0" + str(ordinal)).encode()).hexdigest()[:32]


def matches(fingerprint, raw):
    text = raw
    for _ in range(4):
        decoded = unquote(text)
        if decoded == text:
            break
        text = decoded
    if fingerprint == "task_worldpoverty_2018_2020_rural_215_fivecountries":
        return all(token in text for token in ["worldPovertyRegion","2018","2020","2.15","AFG","GHA","NGA","IND","MEX","ruralValue","headcount"])
    if fingerprint == "task_ipeds_cs_county_2013_cip1107":
        return all(token in text for token in ["ipeds_completions","County","2013","1107","Completions"])
    if fingerprint == "object_india_malaria_chart_d88e6864":
        return "d88e6864f43c426dbcd1ee675a8944a7" in text
    if fingerprint == "task_sec_regcf_2019_massachusetts":
        return "regCF_county_2019" in text and any(token in text for token in ["us-ma",'"ma"',"Massachusetts"])
    raise ValueError("Unknown fingerprint predicate")


def verify(csv_path, ledger_path):
    checksum = hashlib.sha256(Path(csv_path).read_bytes()).hexdigest()
    ledger = [json.loads(line) for line in Path(ledger_path).read_text().splitlines() if line]
    assert len({item["observation_id"] for item in ledger}) == len(ledger), "Duplicate observation ID"
    assert {item["source_sha256"] for item in ledger} == {checksum}, "CSV checksum does not match the frozen source"
    rows = []
    with Path(csv_path).open(encoding="utf8", newline="") as stream:
        reader = csv.DictReader(stream)
        for ordinal, row in enumerate(reader, 1):
            rows.append((ordinal, reader.line_num, row))
    by_alias = {}
    for ordinal, end_line, row in rows:
        assert row["alias"] not in by_alias, "Ambiguous alias in CSV"
        by_alias[row["alias"]] = (ordinal, end_line, row)
    source_paths = {item["source_path"] for item in ledger}
    assert len(source_paths) == 1, "Pass one source CSV ledger at a time"
    source_path = next(iter(source_paths))
    by_record_id = {row_id(source_path, checksum, ordinal): (ordinal, end_line, row)
                    for ordinal, end_line, row in rows}
    assert len(by_record_id) == len(rows), "Source record ID collision"
    changed_target = 0
    wrong_target_still_matches_rule = 0
    for item in ledger:
        ordinal, end_line, row = by_alias[item["intended_identity"]]
        assert row["url"] == item["exact_destination"], "Corrected full raw URL differs"
        assert row["timestamp"] == item["time_raw"], "Corrected source clock differs"
        assert ordinal == item["source_data_row"] and end_line == item["physical_end_line"], "CSV provenance differs"
        assert row_id(item["source_path"], checksum, ordinal) == item["resolved_record_id"], "Corrected source-qualified record ID differs"
        assert item["original_record_id"] in by_record_id, "Original record ID does not resolve"
        old_ordinal, _, old = by_record_id[item["original_record_id"]]
        assert old["alias"] == item["original_object_key"] and old["url"] == item["original_destination"], "Before-state evidence differs"
        assert old["alias"] != row["alias"], "This is not an alias repair"
        assert matches(item["fingerprint"], row["url"]), "Corrected destination does not meet the frozen task rule"
        assert old_ordinal == ordinal + 1, "The observed defect is not the documented next-row attachment"
        changed_target += old["url"] != row["url"]
        wrong_target_still_matches_rule += matches(item["fingerprint"],old["url"])
    by_alias_ledger = {row["intended_identity"]:row for row in ledger}
    for alias, bad_alias, bad_target in [("agx544064","atestxyz555","https://example.org/xyz123zzz"),
                                        ("tynwd","wr-n2","https://example.org/testtest")]:
        row = by_alias_ledger[alias]
        assert row["original_object_key"] == bad_alias and row["original_destination"] == bad_target
        assert not matches(row["fingerprint"],bad_target), "Negative control unexpectedly matches the task"
        assert row["exact_destination"] != bad_target
    return dict(passed=True, csv_sha256=checksum, csv_data_rows=len(rows), verified_repairs=len(ledger),
                by_fingerprint=dict(Counter(item["fingerprint"] for item in ledger)),
                changed_destinations=changed_target, identical_destination_wrong_alias=len(ledger)-changed_target,
                incorrectly_attached_destinations_that_still_match_task_rule=wrong_target_still_matches_rule,
                source_qualified_ids_verified=True, full_raw_urls_verified=True, counterexamples_removed=True,
                interpretation="Matching task text alone cannot establish alias provenance or independent activity")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--csv",type=Path,required=True)
    parser.add_argument("--ledger",type=Path,default=Path(__file__).with_name("corrected_links.jsonl"))
    parser.add_argument("--out",type=Path)
    args = parser.parse_args()
    result = verify(args.csv,args.ledger)
    text = json.dumps(result,indent=2)+"\n"
    if args.out:
        args.out.write_text(text)
    print(text,end="")
