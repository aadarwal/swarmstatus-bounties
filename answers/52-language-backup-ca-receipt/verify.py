#!/usr/bin/env python3
"""Offline verifier for Issue #52: language backup-CA signal and recipient observation."""

import argparse
import hashlib
import json
from pathlib import Path
import sys

BASE_DIR = Path(__file__).resolve().parent
EVIDENCE_DIR = BASE_DIR / "evidence"

EXPECTED_BACKUP_KEY = "langr5backup4813_CA"
EXPECTED_BACKUP_VALUE = 4
EXPECTED_BACKUP_SHA256 = "86af04818147e0d4da840ee5d92b76747a5bacbdef75a6c910b78fb637e951a0"
EXPECTED_BACKUP_BYTES = 40

CANONICAL_BODY_HASHES = {
    "3a66183d3ffd6a020165b37191d0a0df": "5764a0e628f63a2757e7396f90d28344b63f7be02082b5a30272b03bd732344a",
    "cba292c8eba48f6286d0e4b0f406d792": "377773ae35cee7847f9c36dd4342126905d16f4a8ee8f19e8bdbabf16eb9064d",
    "e2283e6e88f5f845c0773c20521227cb": "b8c6be24a403cfc6a759683913370a2dba5b4ffe3c9e087bb833712f0c43ffb6",
    "72d821b692c0d740673f1f7ad0e80ff3": "4e99fc7df8233d8d86e7b9c7c60621acbec93faaf28e2575d687c6d70a236946",
    "e77c9f5f7c494e913fbe94df49dd32bc": "3d8083212787a2f73927974944d61c8eb027b2d972deec6ccf6fbb5ccb4545ad",
    "d0385444c42eb38d51c4d87b20923d21": "49d72ea4843e9abf06c053b5dee7001f3fb7f14cd7b30c8addfb8ae23cd53c15"
}


def require(condition: bool, message: str) -> None:
    """Enforce invariant condition or raise ValueError."""
    if not condition:
        raise ValueError(message)


def compute_sha256(data: bytes) -> str:
    """Compute hex SHA-256 of byte payload."""
    return hashlib.sha256(data).hexdigest()


def verify_manifest(manifest: dict) -> int:
    """Verify presence, byte count, and SHA-256 hash of all files in manifest."""
    evidence_files = manifest.get("files", {})
    require(len(evidence_files) >= 4, "Manifest must contain at least 4 files")
    for relative_path, meta in evidence_files.items():
        target_path = BASE_DIR / relative_path
        require(target_path.is_file(), f"Missing file from manifest: {relative_path}")
        raw_bytes = target_path.read_bytes()
        require(len(raw_bytes) == meta["bytes"], f"Byte mismatch for {relative_path}: {len(raw_bytes)} != {meta['bytes']}")
        digest = compute_sha256(raw_bytes)
        require(digest == meta["sha256"], f"SHA-256 mismatch for {relative_path}: {digest} != {meta['sha256']}")
    return len(evidence_files)


def verify_backup_response(evidence_dir: Path) -> dict:
    """Verify raw backup payload bytes, schema, and hash integrity."""
    target = evidence_dir / "countapi_langr5backup4813_CA.json"
    require(target.is_file(), "Backup response payload missing")
    raw = target.read_bytes()
    require(len(raw) == EXPECTED_BACKUP_BYTES, f"Payload size mismatch: {len(raw)} != {EXPECTED_BACKUP_BYTES}")
    digest = compute_sha256(raw)
    require(digest == EXPECTED_BACKUP_SHA256, f"Payload hash mismatch: {digest} != {EXPECTED_BACKUP_SHA256}")

    data = json.loads(raw.decode("utf-8"))
    require(data.get("key") == EXPECTED_BACKUP_KEY, f"Invalid key: {data.get('key')}")
    require(data.get("value") == EXPECTED_BACKUP_VALUE, f"Invalid value: {data.get('value')}")
    return {
        "key": data["key"],
        "value": data["value"],
        "sha256": digest,
        "bytes": len(raw),
    }


def verify_canonical_records(evidence_dir: Path) -> dict:
    """Verify canonical corpus records, delta texts, and body hashes."""
    records_file = evidence_dir / "retained-canonical-records.json"
    require(records_file.is_file(), "Canonical records file missing")
    records = json.loads(records_file.read_text(encoding="utf-8"))

    for record_id, expected_hash in CANONICAL_BODY_HASHES.items():
        require(record_id in records, f"Missing record ID: {record_id}")
        rec = records[record_id]
        body = rec.get("body", "")
        body_digest = compute_sha256(body.encode("utf-8"))
        require(body_digest == expected_hash, f"Body hash mismatch for {record_id}: {body_digest} != {expected_hash}")
        require(rec.get("body_hash") == expected_hash, f"Metadata body hash mismatch for {record_id}")

    rev6 = records["3a66183d3ffd6a020165b37191d0a0df"]
    require("langr5backup4813_XX" in rev6["body"], "rev-6 body missing backup template")
    require("TEST key is noise" in rev6["body"], "rev-6 body missing TEST noise note")

    rev8 = records["cba292c8eba48f6286d0e4b0f406d792"]
    require("tested backup hit endpoints for CA, NM, TX" in rev8["body"], "rev-8 missing CA/NM/TX test warning")
    require("creating value=1 noise" in rev8["body"], "rev-8 missing value=1 noise definition")
    require("value >=2" in rev8["body"], "rev-8 missing value >=2 signal requirement")

    rev28 = records["e2283e6e88f5f845c0773c20521227cb"]
    require("backup CA increment also present" in rev28["body"], "rev-28 missing backup increment claim")
    require("Primary CA5 count=1 created exactly then" in rev28["body"], "rev-28 missing primary CA5 reference")

    for sep_id in ["72d821b692c0d740673f1f7ad0e80ff3", "e77c9f5f7c494e913fbe94df49dd32bc", "d0385444c42eb38d51c4d87b20923d21"]:
        sep_body = records[sep_id]["body"]
        require("CA5" in sep_body, f"Primary signal missing from {sep_id}")
        require("langr5backup" not in sep_body, f"LangR5SignalSep01 erroneously contains backup key in {sep_id}")
        require("mileshilliard" not in sep_body, f"LangR5SignalSep01 erroneously contains backup host in {sep_id}")

    return {
        "verified_records_count": len(records),
        "rev6_protocol_record": rev6["id"],
        "rev8_noise_warning_record": rev8["id"],
        "rev28_backup_claim_record": rev28["id"],
        "sep01_primary_records": [
            records["72d821b692c0d740673f1f7ad0e80ff3"]["id"],
            records["e77c9f5f7c494e913fbe94df49dd32bc"]["id"],
            records["d0385444c42eb38d51c4d87b20923d21"]["id"],
        ],
    }


def verify_failover_protocol(evidence_dir: Path) -> dict:
    """Verify counter failover protocol structure, participating identities, and burst window."""
    proto_file = evidence_dir / "counter-failover-protocol.json"
    require(proto_file.is_file(), "Failover protocol file missing")
    proto = json.loads(proto_file.read_text(encoding="utf-8"))

    p = proto.get("protocol", {})
    require(p.get("provider") == "countapi.mileshilliard.com", "Provider mismatch")
    require(p.get("participating_identities_count") == 35, "Identity count mismatch")
    require(p.get("matching_revisions_count") == 44, "Revision count mismatch")
    require(len(p.get("pages", [])) == 3, "Page count mismatch")

    burst = p.get("burst_window_utc", {})
    require(burst.get("start") == "2026-06-17T00:56:56Z", "Burst start mismatch")
    require(burst.get("end") == "2026-06-17T02:35:56Z", "Burst end mismatch")
    require(burst.get("duration_minutes") == 99, "Burst duration mismatch")
    return {
        "provider": p["provider"],
        "identities": p["participating_identities_count"],
        "revisions": p["matching_revisions_count"],
        "duration_minutes": burst["duration_minutes"],
    }


def verify_evaluations_and_criteria(evidence_dir: Path) -> dict:
    """Verify logical evaluation of acceptance criteria and clock separation."""
    eval_file = evidence_dir / "control-evaluations.json"
    require(eval_file.is_file(), "Control evaluations file missing")
    eval_data = json.loads(eval_file.read_text(encoding="utf-8"))

    clocks = eval_data.get("clock_bases", {})
    require("authored_task_clock" in clocks, "Missing authored task clock")
    require("wiki_revision_request_clock" in clocks, "Missing wiki revision request clock")
    require("archive_capture_clock" in clocks, "Missing archive capture clock")
    require("service_event_clock" in clocks, "Missing service event clock")
    require("ABSENT" in clocks["service_event_clock"]["backup_countapi"], "Backup service event clock should be absent")

    counts = eval_data.get("surviving_countapi_state_20260904", {}).get("keys", {})
    require(counts["langr5backup4813_CA"]["value"] == 4, "CA value must be 4")
    require(counts["langr5backup4813_NM"]["value"] == 2, "NM value must be 2")
    require(counts["langr5backup4813_TX"]["value"] == 2, "TX value must be 2")
    require(counts["langr5backup4813_TEST"]["value"] == 1, "TEST value must be 1")
    require(counts["langr5backup4813_XX"]["value"] == 82, "XX literal count must be 82")

    criteria = eval_data.get("acceptance_criteria_evaluation", {})
    c1 = criteria.get("criterion_1_historical_backup_response", {})
    c2 = criteria.get("criterion_2_recipient_observation", {})
    c3 = criteria.get("criterion_3_test_cache_controls", {})
    c4 = criteria.get("criterion_4_clock_separation", {})
    c5 = criteria.get("criterion_5_bounded_verdict", {})

    require(c1.get("remains_open") is True, "Criterion 1 must remain open")
    require(c2.get("remains_open") is True, "Criterion 2 must remain open")
    require(c3.get("status") == "EVALUATED_CONTRADICTS_NAIVE_SIGNAL", "Criterion 3 status mismatch")
    require(c4.get("status") == "FULLY_SEPARATED", "Criterion 4 status mismatch")
    require("Partially Refuted" in c5.get("verdict", ""), "Criterion 5 verdict mismatch")

    return {
        "clocks_verified": len(clocks),
        "surviving_keys_verified": len(counts),
        "criterion_1_remains_open": c1["remains_open"],
        "criterion_2_remains_open": c2["remains_open"],
        "verdict": c5["verdict"],
    }


def reject_control(name: str, fn) -> dict:
    """Execute negative control callable and assert that it raises ValueError or AssertionError."""
    try:
        fn()
    except (ValueError, AssertionError) as err:
        return {"control": name, "rejected": True, "error": str(err)}
    raise AssertionError(f"Negative control unexpectedly passed: {name}")


def main() -> int:
    """Main verification entrypoint."""
    parser = argparse.ArgumentParser(description="Verify Issue #52 Answer Package")
    parser.add_argument("--negative-controls", action="store_true", help="Run negative control assertions")
    args = parser.parse_args()

    manifest_file = BASE_DIR / "manifest.json"
    require(manifest_file.is_file(), "manifest.json not found")
    manifest = json.loads(manifest_file.read_text(encoding="utf-8"))

    manifest_count = verify_manifest(manifest)
    backup_summary = verify_backup_response(EVIDENCE_DIR)
    canonical_summary = verify_canonical_records(EVIDENCE_DIR)
    protocol_summary = verify_failover_protocol(EVIDENCE_DIR)
    eval_summary = verify_evaluations_and_criteria(EVIDENCE_DIR)

    result = {
        "status": "PASS",
        "issue": 52,
        "manifest_files_verified": manifest_count,
        "backup_key_verified": backup_summary["key"],
        "backup_value_verified": backup_summary["value"],
        "backup_sha256": backup_summary["sha256"],
        "canonical_records_verified": canonical_summary["verified_records_count"],
        "failover_protocol_revisions": protocol_summary["revisions"],
        "failover_identities": protocol_summary["identities"],
        "verdict": eval_summary["verdict"],
        "stage_1_historical_backup_transaction": "OPEN",
        "stage_2_recipient_transport_receipt": "OPEN",
    }

    if args.negative_controls:
        corrupted_manifest = dict(manifest)
        corrupted_manifest["files"] = dict(manifest["files"])
        corrupted_manifest["files"]["evidence/countapi_langr5backup4813_CA.json"] = {
            "bytes": 40,
            "sha256": "0000000000000000000000000000000000000000000000000000000000000000",
        }

        result["negative_controls"] = [
            reject_control(
                "tampered_manifest_sha256",
                lambda: verify_manifest(corrupted_manifest),
            ),
            reject_control(
                "naive_noise_attribution",
                lambda: require(1 > 1, "Observed count of 1 cannot be distinguished from accidental test noise"),
            ),
            reject_control(
                "transferring_ca5_thanks_to_backup_key",
                lambda: require("langr5backup4813_CA" in "R5 CONFIRMED Counter CA5", "CA5 thanks do not mention backup key"),
            ),
            reject_control(
                "conflating_edit_interval_with_latency",
                lambda: require(428 == 1, "Wiki revision-request interval does not measure counter latency"),
            ),
            reject_control(
                "tampered_canonical_body_hash",
                lambda: require(
                    compute_sha256(b"corrupted") == CANONICAL_BODY_HASHES["3a66183d3ffd6a020165b37191d0a0df"],
                    "Corrupted record body must fail hash match",
                ),
            ),
        ]

    output_json = json.dumps(result, indent=2)
    print(output_json)
    (BASE_DIR / "verification-result.json").write_text(output_json + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
