#!/usr/bin/env python3
"""Offline verification for the GDDY->TWLO same-date retrieval pair question.

No network access is required: every check runs against the retained target
strings and timestamps recorded in ./evidence. Run from the repository root:

    python3 answers/34-gddy-twlo-same-date-pair/verify.py
"""

import json
import os
import re
import sys
from datetime import datetime, timezone
from urllib.parse import unquote

HERE = os.path.dirname(os.path.abspath(__file__))
EVIDENCE = os.path.join(HERE, "evidence")


def load(name):
    with open(os.path.join(EVIDENCE, name), "r", encoding="utf-8") as handle:
        return json.load(handle)


def utc_day(epoch_seconds):
    return datetime.fromtimestamp(int(epoch_seconds), tz=timezone.utc).strftime("%Y%m%d")


def main():
    observations = load("observations.json")["observations"]
    pair = load("pair.json")
    staging = load("staging-artifact.json")
    classification = load("classification.json")

    by_id = {item["record_id"]: item for item in observations}
    checks = []

    def check(check_id, ok, detail):
        checks.append({"id": check_id, "ok": bool(ok), "detail": detail})

    check(
        "C1",
        len(observations) == 3 and len(by_id) == 3,
        "three retained records with distinct record ids",
    )

    gddy = by_id.get(pair["first_record_id"])
    twlo = by_id.get(pair["second_record_id"])
    markdown = by_id.get(staging["record_id"])

    check(
        "C2",
        bool(gddy)
        and bool(twlo)
        and pair["ordered_pair"] == ["GDDY", "TWLO"]
        and pair["from"] == pair["to"] == pair["date"] == "20191115",
        "ordered pair GDDY then TWLO carries from=to=20191115",
    )

    check(
        "C3",
        bool(gddy)
        and gddy["surface"] == "yahoo_japan_direct"
        and "finance.yahoo.co.jp" in gddy["target"]
        and "from=20191115" in gddy["target"]
        and "to=20191115" in gddy["target"],
        "GDDY leg is a direct Yahoo Japan route with from=to=20191115",
    )

    window = re.search(r"period1=(\d+)&period2=(\d+)", twlo["target"]) if twlo else None
    check(
        "C4",
        bool(window)
        and utc_day(window.group(1)) == "20191115"
        and int(pair["epoch"]["period1"]) == int(window.group(1))
        and int(pair["epoch"]["period2"]) == int(window.group(2))
        and int(window.group(2)) > int(window.group(1)),
        "TWLO leg encodes the same date as a period1/period2 epoch window starting 2019-11-15",
    )

    encoded = markdown["target"] if markdown else ""
    decoded = unquote(encoded.split("url=", 1)[1]) if "url=" in encoded else ""
    check(
        "C5",
        bool(markdown)
        and encoded.startswith("https://markdown.new/")
        and decoded == staging["decoded_prefix"]
        and bool(gddy)
        and gddy["target"].startswith(staging["decoded_prefix"])
        and "20191115" not in encoded,
        "additional staging artifact is a markdown.new wrapper holding a truncated copy of the GDDY route",
    )

    check(
        "C6",
        bool(twlo)
        and twlo["surface"] == "pure_md_epoch_window"
        and twlo["target"].startswith("https://pure.md/")
        and "GDDY" not in twlo["target"],
        "TWLO leg is an independent observation: different surface, no GDDY substring",
    )

    check(
        "C7",
        classification["copied_source_blocks"] == [staging["record_id"]]
        and pair["first_record_id"] in classification["independent_observations"]
        and pair["second_record_id"] in classification["independent_observations"],
        "classification separates the copied markdown.new block from the independent observations",
    )

    check(
        "C8",
        bool(gddy)
        and bool(twlo)
        and gddy["time_raw"] != twlo["time_raw"]
        and gddy["time_basis"] == "raw_unzoned"
        and twlo["time_basis"] == "raw_unzoned",
        "the two independent observations carry distinct raw timestamps",
    )

    result = {
        "issue": "gddy-twlo-same-date-pair",
        "status": "pass" if all(item["ok"] for item in checks) else "fail",
        "ordered_pair": pair["ordered_pair"],
        "date": pair["date"],
        "staging_artifact": staging["record_id"],
        "classification": {
            "copied_source_blocks": classification["copied_source_blocks"],
            "independent_observations": classification["independent_observations"],
        },
        "checks": checks,
    }

    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    sys.exit(main())
