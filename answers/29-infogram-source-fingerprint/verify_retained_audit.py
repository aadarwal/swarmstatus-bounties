#!/usr/bin/env python3
"""Offline verification of retained corpus audit and source-discriminating fingerprint for Issue #29."""
import argparse
import copy
import json
from pathlib import Path

UUID = "55eeebff-2501-4b78-979d-1c7c1e5c4f74"
EXPECTED_RECORD_COUNT = 10
EXPECTED_OBJECT_COUNT = 6
EXPECTED_SIBLING_COUNT = 3

def verify_audit_data(audit_data, chart_data):
    assert audit_data["target_uuid"] == UUID == chart_data["source_uuid"]
    assert audit_data["corpus_scope"]["matching_records_count"] == EXPECTED_RECORD_COUNT
    assert audit_data["corpus_scope"]["unique_objects_count"] == EXPECTED_OBJECT_COUNT
    assert len(audit_data["retained_records"]) == EXPECTED_RECORD_COUNT

    unique_objects = set()
    for rec in audit_data["retained_records"]:
        assert len(rec["id"]) == 32
        assert len(rec["body_hash"]) == 64
        assert rec["contains_table_data"] is False
        assert rec["contains_answer_passage"] is False
        unique_objects.add(rec["object_key"])

    assert len(unique_objects) == EXPECTED_OBJECT_COUNT

    # Sibling UUID negative controls
    siblings = audit_data["sibling_uuids_negative_control"]
    assert len(siblings) == EXPECTED_SIBLING_COUNT
    for sib in siblings:
        assert sib["retained_records_count"] == 0
        assert sib["uuid"] != UUID

    # Source fingerprint check (41 vs 42)
    chart_rows = chart_data["rows"]
    row_2_0 = next(r for r in chart_rows if r[0] == "2.0")
    rajini_age = int(row_2_0[1])
    amy_age = int(row_2_0[2].split()[0])
    derived_difference = rajini_age - amy_age

    comp = audit_data["source_fingerprint_comparison"]
    assert comp["chart_cell_rajini_age"] == rajini_age == 67
    assert comp["chart_derived_age_difference"] == derived_difference == 41
    assert comp["article_prose_wording"] == "about 42 years"
    assert comp["supported_representation"] == "none_retained"

    # Acceptance criteria coverage
    criteria = audit_data["acceptance_criteria_assessment"]
    assert len(criteria) == 4
    assert all(c["met"] is True for c in criteria)

    return {
        "verified_retained_records": len(audit_data["retained_records"]),
        "verified_unique_objects": len(unique_objects),
        "verified_sibling_negative_controls": len(siblings),
        "derived_chart_difference": derived_difference,
        "article_prose_difference_claim": comp["article_prose_wording"],
        "supported_retained_representation": comp["supported_representation"],
        "contradictory_result_documented": True,
        "acceptance_criteria_verified": 4
    }

def run_negative_controls(audit_data, chart_data):
    # Control 1: Mutate record body hash
    mutated = copy.deepcopy(audit_data)
    mutated["retained_records"][0]["body_hash"] = "0" * 64
    # should still pass length check, but test if we modify contains_answer_passage
    mutated["retained_records"][0]["contains_answer_passage"] = True
    try:
        verify_audit_data(mutated, chart_data)
    except AssertionError:
        pass
    else:
        raise AssertionError("Negative control failed: fake answer passage accepted")

    # Control 2: Mutate sibling count
    mutated2 = copy.deepcopy(audit_data)
    mutated2["sibling_uuids_negative_control"][0]["retained_records_count"] = 1
    try:
        verify_audit_data(mutated2, chart_data)
    except AssertionError:
        pass
    else:
        raise AssertionError("Negative control failed: non-zero sibling match accepted")

    # Control 3: Mutate derived age gap
    mutated3 = copy.deepcopy(audit_data)
    mutated3["source_fingerprint_comparison"]["chart_derived_age_difference"] = 42
    try:
        verify_audit_data(mutated3, chart_data)
    except AssertionError:
        pass
    else:
        raise AssertionError("Negative control failed: altered age difference accepted")

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--negative-controls", action="store_true", help="Run synthetic negative controls")
    args = parser.parse_args()

    base_dir = Path(__file__).parent
    audit_file = base_dir / "retained-corpus-audit.json"
    chart_file = base_dir / "chart-table.json"

    audit_data = json.loads(audit_file.read_text())
    chart_data = json.loads(chart_file.read_text())

    result = verify_audit_data(audit_data, chart_data)

    if args.negative_controls:
        run_negative_controls(audit_data, chart_data)
        result["negative_controls_passed"] = True

    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
