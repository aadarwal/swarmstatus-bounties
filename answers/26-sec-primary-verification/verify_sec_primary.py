#!/usr/bin/env python3
"""Offline, standard-library verification of the proposed SEC evidence claim.

No network calls, shell commands, historical query execution, or database writes.
The default inputs travel with this script. Optional --raw-receipt verifies the
selected metadata against the original downloaded URLQuery JSON or JSON.gz.
"""
import argparse
import copy
from decimal import Decimal, ROUND_HALF_UP
import gzip
import hashlib
import json
from pathlib import Path
import re
import sys

HERE = Path(__file__).resolve().parent
PRIMARY_SHA256 = "19f21855d65a95e4fecd49ee1dd0127748dbebb1eb218c4c877efbc707093297"
CACHE_SHA256 = "2c673703a05c9bc28878948f0c625e73981c45ec798f47962fb2be35e57f3aaf"
PROVIDER_JSON_SHA256 = "d89f6c9dd1957ffd5683b04592caf9967f02496b73f8fdbddf48e8cee4d7a35a"
REPORT_ID = "0873ec25-2bff-4610-b7c0-6cbd5bb31933"
WINDOWS = {2019: (46, 52), 2020: (52, 62), 2021: (82, 91)}


def require(condition: bool, message: str) -> None:
    """Enforce an invariant condition or raise a ValueError with the given message."""
    if not condition:
        raise ValueError(message)


def load_json(path: Path) -> dict:
    """Load JSON file from path parsing floating-point numbers into Decimal."""
    return json.loads(path.read_text(), parse_float=Decimal)


def cache_rows(body: str, year: int) -> list:
    """Extract and parse structured county rows for a given year from the wiki body.

    Args:
        body: Plain text body of the retained wiki page.
        year: Target year (2019, 2020, 2021).

    Returns:
        List of dicts containing code, offerings, and usd values.
    """
    marker = "{regCF county " + str(year) + "}"
    require(body.count(marker) == 1, f"Expected one cached {year} section")
    section = body.split(marker, 1)[1].split("{regCF county ", 1)[0]
    matches = re.findall(r"code (us-ma-\d+) \| offerings ([\d.]+) \| usd ([\d.]+)", section)
    return [{"code": code, "offerings": Decimal(offerings), "usd": Decimal(usd)}
            for code, offerings, usd in matches]


def select_transaction(raw: dict) -> dict:
    """Extract relevant transaction fields from the full URLQuery JSON export.

    Args:
        raw: Full dictionary loaded from the raw URLQuery report.

    Returns:
        Normalized dictionary containing sanitized request, header, and response fields.
    """
    transaction = raw["http"][1]
    headers = {}
    wanted = {"content-type", "content-length", "content-encoding", "last-modified", "date"}
    for line in transaction["response"]["raw"].splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            if key.lower() in wanted:
                headers[key.lower()] = value.strip()
    return {
        "request_url": transaction["url"]["schema"] + "://" + transaction["url"]["addr"],
        "request_method": transaction["request"]["method"],
        "request_date": transaction["date"],
        "request_timestamp": transaction["timestamp"],
        "is_navigation_request": transaction["is_navigation_request"],
        "resource_type": transaction["resource_type"],
        "response_status_code": transaction["response"]["status_code"],
        "selected_response_headers": headers,
        "response_data": {key: transaction["response"]["data"][key]
                          for key in ("size", "size_decoded", "mime_type", "magic", "sha256", "resource_available", "data")},
    }


def verify(primary_bytes: bytes, cached: dict, receipt: dict, capture: dict, raw_receipt_path: Path = None) -> dict:
    """Perform deterministic verification of primary bytes, cached rows, and receipt metadata.

    Args:
        primary_bytes: Raw bytes of the primary SEC Investor.gov JSON file.
        cached: Dictionary of retained wiki table record.
        receipt: Selected metadata from URLQuery transaction.
        capture: Capture metadata for primary source.
        raw_receipt_path: Optional path to raw URLQuery JSON report.

    Returns:
        Summary dictionary containing verification results and comparison metrics.
    """
    digest = hashlib.sha256(primary_bytes).hexdigest()
    require(digest == PRIMARY_SHA256, "Primary capture SHA256 differs")
    require(digest == capture["sha256"], "Capture metadata hash differs")
    require(len(primary_bytes) == capture["bytes"] == 147840, "Primary capture byte length differs")
    require(capture["source_url"] == "https://www.investor.gov/files/county.json", "Unexpected primary source")
    require(capture["capture_at_utc"] == "2026-09-05T17:27:30.159612+00:00", "Unexpected capture observation time")
    require(hashlib.sha256(cached["body"].encode()).hexdigest() == cached["body_hash"] == CACHE_SHA256,
            "Retained wiki body hash differs")
    require(cached["id"] == "4cc89598bf23a4b21b771b7d26862b26", "Unexpected source-qualified cache record")
    require(cached["body_availability"] == "head_only", "Cache availability qualification changed")
    require(cached["time_basis"] == "clock_conflict_site_offset", "Cache clock qualification changed")
    source = json.loads(primary_bytes, parse_float=Decimal)
    year_keys = sorted(key for key in source if re.fullmatch(r"regCF_county_\d{4}", key))
    require(year_keys == ["regCF_county_" + str(y) for y in range(2019, 2025)], "Source year-array set differs")
    comparisons = []
    for year, (start, end) in WINDOWS.items():
        array = source["regCF_county_" + str(year)]
        selected = array[start:end]
        ma_prefix = [row for row in array if row["code"].startswith("us-ma-")]
        require(selected == ma_prefix, f"{year} slice does not exactly equal MA-prefix rows in source order")
        retained = cache_rows(cached["body"], year)
        expected = [{key: row[key] for key in ("code", "offerings", "usd")} for row in selected]
        require(len(retained) == len(expected) == end - start, f"{year} retained row count differs")
        require(retained == expected, f"{year} cached code/offerings/usd rows differ")
        require(len({row["code"] for row in retained}) == len(retained), f"Duplicate county rows in {year}")
        converted = []
        for row in expected:
            require(row["usd"] >= 0, "This rounded-unit check is scoped to nonnegative observed values")
            via_ten = (row["usd"] / Decimal(10)).quantize(Decimal(1), rounding=ROUND_HALF_UP) / Decimal(100)
            via_thousand = (row["usd"] / Decimal(1000)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
            require(via_ten == via_thousand, f"Rounded unit conversion differs for {year}/{row['code']}")
            converted.append({"code": row["code"], "thousands_usd": format(via_thousand, ".2f")})
        comparisons.append({"year": year, "source_array_length": len(array), "slice": [start, end],
                            "matched_rows": len(retained), "all_ma_prefix_rows_in_source_order": True,
                            "exact_cached_values_match": True, "derived_rounded_thousands_usd": converted})
    require(sum(item["matched_rows"] for item in comparisons) == 25, "Expected exactly 25 matched rows")
    outlier = [row for row in source["regCF_county_2020"] if row["code"] == "us-ma-760"]
    require(len(outlier) == 1 and outlier[0]["usd"] == Decimal(14300), "Known 2020 outlier differs")

    require(receipt["report_id"] == REPORT_ID and receipt["transaction_index"] == 1, "Unexpected URLQuery transaction")
    require(receipt["report_date"] == "2026-06-18T15:35:48Z", "Unexpected report timestamp")
    transaction = receipt["transaction"]
    require(transaction["request_url"] == "https://www.sec.gov/files/county.json", "Receipt request target differs")
    require(transaction["request_method"] == "GET" and transaction["is_navigation_request"] is True,
            "Receipt is not the recorded GET navigation")
    require(transaction["request_date"] == "2026-06-18T15:35:24.375Z", "Unexpected transaction timestamp")
    require(transaction["response_status_code"] == "200", "Receipt does not report HTTP 200")
    response_data = transaction["response_data"]
    require(response_data["sha256"] == digest, "Provider-reported response hash does not match primary bytes")
    require(response_data["size"] == len(primary_bytes), "Provider-reported size does not match primary length")
    require(response_data["size_decoded"] == 19168, "Provider size_decoded field differs")
    require(response_data["mime_type"] == "application/vnd.mozilla.json.view", "Browser MIME field differs")
    require(response_data["resource_available"] is False and response_data["data"] is None,
            "Historical body-availability qualification changed")
    headers = transaction["selected_response_headers"]
    require(headers["content-type"] == "application/json", "Recorded origin Content-Type differs")
    require(headers["content-encoding"] == "gzip" and headers["content-length"] == "18032",
            "Recorded compressed-transfer header fields differ")
    require(headers["last-modified"] == capture["last_modified_header"], "Reported Last-Modified values differ")
    raw_verified = False
    if raw_receipt_path:
        raw = raw_receipt_path.read_bytes()
        if raw.startswith(b"\x1f\x8b"):
            raw = gzip.decompress(raw)
        require(hashlib.sha256(raw).hexdigest() == receipt["original_provider_json_sha256"] == PROVIDER_JSON_SHA256,
                "Original provider JSON hash differs")
        parsed = json.loads(raw)
        require(parsed["report_id"] == REPORT_ID and parsed["date"] == receipt["report_date"], "Raw report identity differs")
        require(select_transaction(parsed) == transaction, "Selected receipt fields do not match original provider JSON")
        raw_verified = True
    return {
        "result": "PASS", "network_requests": 0, "primary_sha256": digest, "primary_bytes": len(primary_bytes),
        "cached_rows_matched": 25, "independent_cached_bodies_compared": 1,
        "cache_record_id": cached["id"], "source_year_arrays": year_keys, "comparisons": comparisons,
        "provider_reported_hash_and_size_match": True, "raw_provider_json_checked": raw_verified,
        "report_date": receipt["report_date"], "transaction_request_date": transaction["request_date"],
        "historical_response_body_recovered": False,
        "limits": ["Provider hash/size metadata correspondence, not a freshly recovered June response body.",
                   "Browser MIME, size_decoded and compressed Content-Length remain separate fields.",
                   "One retained head-only wiki body; copies are not independent sources.",
                   "No claim of actor identity, answer consumption, uninterrupted availability, or novel county values."]}


def main() -> int:
    """CLI entrypoint for running SEC verification suite."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--primary", type=Path, default=HERE / "investor-county-20260905.json")
    parser.add_argument("--cached", type=Path, default=HERE / "cached-wiki-table.json")
    parser.add_argument("--receipt", type=Path, default=HERE / "urlquery-sec-receipt.json")
    parser.add_argument("--capture-metadata", type=Path, default=HERE / "primary-capture-metadata.json")
    parser.add_argument("--raw-receipt", type=Path, help="Optional original provider JSON or JSON.gz; read locally only")
    parser.add_argument("--negative-controls", action="store_true", help="Confirm in-memory altered inputs are rejected")
    args = parser.parse_args()
    primary = args.primary.read_bytes()
    cached, receipt, capture = load_json(args.cached), load_json(args.receipt), load_json(args.capture_metadata)
    try:
        result = verify(primary, cached, receipt, capture, args.raw_receipt)
        if args.negative_controls:
            wrong_value = copy.deepcopy(cached)
            wrong_value["body"] = wrong_value["body"].replace("usd 48600.0", "usd 48601.0", 1)
            wrong_receipt = copy.deepcopy(receipt)
            wrong_receipt["transaction"]["response_data"]["sha256"] = "0" * 64
            rejected = []
            for name, p, c, r in (("changed_primary_bytes", primary + b"\n", cached, receipt),
                                  ("changed_cached_value", primary, wrong_value, receipt),
                                  ("changed_reported_response_hash", primary, cached, wrong_receipt)):
                try:
                    verify(p, c, r, capture)
                except ValueError:
                    rejected.append(name)
                else:
                    raise ValueError("Negative control unexpectedly passed: " + name)
            result["negative_controls_rejected"] = rejected
        print(json.dumps(result, indent=2))
    except (ValueError, KeyError, TypeError) as error:
        print(json.dumps({"result": "FAIL", "error": str(error)}), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
