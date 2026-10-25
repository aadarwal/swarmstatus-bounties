#!/usr/bin/env python3
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent

EXPECTED = [
    ("3ae5f54b", "2025-12-14T04:51:46Z"),
    ("514333ed", "2026-01-01T10:56:05Z"),
    ("316996fe", "2026-01-01T10:56:06Z"),
    ("5329a841", "2026-02-26T14:49:24Z"),
    ("bd44d381", "2026-02-26T14:50:18Z"),
    ("680ec235", "2026-02-26T14:52:19Z"),
    ("d78a30b4", "2026-02-26T20:15:44Z"),
    ("0263afe2", "2026-02-26T20:16:00Z"),
    ("unknown09", "2026-03-01T00:00:00Z"),
    ("unknown10", "2026-03-01T00:01:00Z"),
    ("unknown11", "2026-03-01T00:02:00Z"),
    ("unknown12", "2026-03-01T00:03:00Z"),
    ("unknown13", "2026-03-01T00:04:00Z"),
]


def parse(value):
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def main():
    data = json.loads((ROOT / "evidence" / "pastes.json").read_text())
    pastes = data["pastes"]

    assert len(pastes) == 13, "expected 13 rows"
    assert len({row["id"] for row in pastes}) == 13, "duplicate paste id"

    observed = [(row["id"], row["created_assertion"]) for row in pastes]
    assert observed == EXPECTED, "row ids or assertion times changed"

    for row in pastes:
        assert row["first_independent_public_capture"] == "2026-09-05"
        parse(row["created_assertion"])

    dates = [parse(row["created_assertion"]) for row in pastes]
    assert min(dates).isoformat().startswith("2025-12-14")
    assert max(dates).isoformat().startswith("2026-03-01")

    print("OK: 13 K4be rows; assertions span 2025-12-14..2026-03-01; first independent capture 2026-09-05")


if __name__ == "__main__":
    main()
