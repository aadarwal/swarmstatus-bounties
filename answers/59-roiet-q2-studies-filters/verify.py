#!/usr/bin/env python3
"""Offline verification script for Swarmstatus Issue #59.

Validates primary evidence, selector conjunction, and year-by-year values
for Roi Et province (TH45) males not in labor force because of studies, Quarter 2 (2013-2021).
"""
import argparse
import copy
import hashlib
import json
from pathlib import Path
import sys

BASE = Path(__file__).resolve().parent
TARGET_SERIES_SHA256 = "d1fa02c2009b9bdc5f861a85dfb204c59c2dca2ff8b35b53d9f8395aa5e065f7"
TARGET_SERIES_BYTES = 197

EXPECTED_YEARS = [2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021]
EXPECTED_PASTE_VALUES = {
    2013: 46308,
    2014: 32212,
    2015: 35083,
    2016: 36227,
    2017: 40810,
    2018: 36313,
    2019: 35040,
    2020: 38827,
    2021: 37842,
}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def read_json(name):
    path = BASE / name
    require(path.exists(), f"Missing required file: {name}")
    return json.loads(path.read_text(encoding="utf-8"))


def validate_manifest(manifest):
    require(manifest.get("schema_version") == 1, "Invalid manifest schema version")
    require(manifest.get("issue") == 59, "Manifest does not match issue #59")
    files = manifest.get("files", {})
    require("evidence.json" in files, "evidence.json missing from manifest")
    require("README.md" in files, "README.md missing from manifest")
    require("verify.py" in files, "verify.py missing from manifest")

    for fname, pin in files.items():
        if fname == "manifest.json":
            continue
        fpath = BASE / fname
        require(fpath.exists(), f"File {fname} declared in manifest does not exist")
        data = fpath.read_bytes()
        actual_size = len(data)
        actual_hash = hashlib.sha256(data).hexdigest()
        require(
            actual_size == pin["bytes"],
            f"Size mismatch for {fname}: expected {pin['bytes']}, got {actual_size}",
        )
        require(
            actual_hash == pin["sha256"],
            f"Hash mismatch for {fname}: expected {pin['sha256']}, got {actual_hash}",
        )


def validate_evidence(doc):
    require(doc.get("schema_version") == 1, "Invalid schema version")
    require(doc.get("issue") == 59, "Document does not match issue #59")

    target = doc.get("target_series", {})
    target_str = target.get("string", "")
    target_bytes = target_str.encode("utf-8")
    computed_hash = hashlib.sha256(target_bytes).hexdigest()

    require(
        len(target_bytes) == TARGET_SERIES_BYTES,
        f"Target series byte length mismatch: expected {TARGET_SERIES_BYTES}, got {len(target_bytes)}",
    )
    require(
        computed_hash == TARGET_SERIES_SHA256,
        f"Target series SHA256 mismatch: expected {TARGET_SERIES_SHA256}, got {computed_hash}",
    )
    require(
        target.get("sha256") == TARGET_SERIES_SHA256,
        "Metadata target sha256 mismatch",
    )

    conj = doc.get("selector_conjunction", {})
    require(conj.get("geography", {}).get("iso_3166_2") == "TH-45", "Wrong geography ISO code")
    require(conj.get("geography", {}).get("nso_province_id") == 707, "Wrong NSO province ID")
    require(conj.get("sex", {}).get("name_en") == "Male", "Wrong sex selector (must be Male)")
    require(
        conj.get("labor_force_status", {}).get("category_code") == "2",
        "Wrong labor force status (must be Category 2: Not in labor force)",
    )
    require(
        conj.get("reason", {}).get("subcategory_code") == "2.2",
        "Wrong inactive reason (must be Subcategory 2.2: Studies / Attending school)",
    )
    require(
        conj.get("periodicity", {}).get("quarter_code") == 2,
        "Wrong quarter (must be Quarter 2: April - June)",
    )
    require(
        "15" in conj.get("age_range", {}).get("description", ""),
        "Wrong age range (must specify population aged 15 years and over)",
    )
    require(
        conj.get("unit", {}).get("scale") == 1,
        "Wrong unit scale (must be unscaled persons count)",
    )

    records = doc.get("records", [])
    require(len(records) == 9, f"Expected 9 year records, found {len(records)}")

    years_found = [r["year"] for r in records]
    require(years_found == EXPECTED_YEARS, f"Years order mismatch: {years_found}")

    for r in records:
        y = r["year"]
        expected_paste = EXPECTED_PASTE_VALUES[y]
        require(
            r["target_paste_value"] == expected_paste,
            f"Year {y} paste value mismatch: expected {expected_paste}, got {r['target_paste_value']}",
        )

        table_raw = r["table_value_raw"]
        table_rounded = round(table_raw)
        if y == 2015:
            # 2015 published table has 35084.0, while paste has 35083 (1-unit sample weighting offset)
            require(
                table_rounded in (35083, 35084),
                f"Year 2015 value unexpected: table_rounded={table_rounded}",
            )
            require(
                r["match_status"] == "1_unit_rounding_offset",
                "Year 2015 must document 1_unit_rounding_offset",
            )
        else:
            require(
                table_rounded == expected_paste,
                f"Year {y} table rounded value mismatch: table={table_rounded}, expected={expected_paste}",
            )
            require(
                r["match_status"] == "exact_match",
                f"Year {y} must have exact_match status",
            )

        controls = r.get("same_table_controls", {})
        require("female_rounded" in controls, f"Year {y} missing female negative control")
        require("total_rounded" in controls, f"Year {y} missing total negative control")
        require(
            controls["female_rounded"] != expected_paste,
            f"Year {y} female control coincidentally equals male value",
        )
        require(
            controls["total_rounded"] != expected_paste,
            f"Year {y} total control coincidentally equals male value",
        )


def run_negative_controls(doc):
    def mutate_sex(d):
        d["selector_conjunction"]["sex"]["name_en"] = "Female"
        for r in d["records"]:
            r["table_value_raw"] = r["same_table_controls"]["female_raw"]

    def mutate_quarter(d):
        d["selector_conjunction"]["periodicity"]["quarter_code"] = 1

    def mutate_geography(d):
        d["selector_conjunction"]["geography"]["iso_3166_2"] = "TH-40"
        d["selector_conjunction"]["geography"]["nso_province_id"] = 705

    def mutate_age_range(d):
        d["selector_conjunction"]["age_range"]["description"] = "13 years and over"

    def mutate_labor_status(d):
        d["selector_conjunction"]["labor_force_status"]["category_code"] = "1"

    def mutate_target_hash(d):
        d["target_series"]["string"] = d["target_series"]["string"] + "\n"

    def mutate_year_value(d):
        d["records"][0]["table_value_raw"] = 99999.0

    cases = [
        ("mutate_sex_to_female", mutate_sex),
        ("mutate_quarter_to_q1", mutate_quarter),
        ("mutate_geography_to_khon_kaen", mutate_geography),
        ("mutate_age_range_to_13_plus", mutate_age_range),
        ("mutate_labor_status_to_employed", mutate_labor_status),
        ("mutate_target_hash", mutate_target_hash),
        ("mutate_year_value", mutate_year_value),
    ]

    rejected = []
    for name, mutate in cases:
        altered = copy.deepcopy(doc)
        mutate(altered)
        try:
            validate_evidence(altered)
        except ValueError:
            rejected.append(name)
        else:
            raise ValueError(f"Negative control accepted unexpectedly: {name}")

    return rejected


def main():
    parser = argparse.ArgumentParser(description="Verify Roi Et Q2 male studies evidence.")
    parser.add_argument(
        "--negative-controls",
        action="store_true",
        help="Run semantic negative control mutation suite.",
    )
    args = parser.parse_args()

    manifest = read_json("manifest.json")
    validate_manifest(manifest)

    evidence = read_json("evidence.json")
    validate_evidence(evidence)

    rejected_controls = []
    if args.negative_controls:
        rejected_controls = run_negative_controls(evidence)

    summary = {
        "status": "PASS",
        "issue": 59,
        "target_series_sha256": TARGET_SERIES_SHA256,
        "target_series_bytes": TARGET_SERIES_BYTES,
        "all_9_years_verified": True,
        "negative_controls_evaluated": len(rejected_controls),
        "negative_controls_rejected": rejected_controls,
    }
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"FAIL: {e}", file=sys.stderr)
        sys.exit(1)
