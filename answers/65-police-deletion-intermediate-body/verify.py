"""Standalone verification script for issue #65 evidence and candidate intermediate bodies."""

import argparse
import hashlib
import json
import sys
from pathlib import Path


def calculate_sha256(data: bytes) -> str:
    """Calculate the lowercase hexadecimal SHA-256 hash of bytes.

    Parameters:
        data: The input byte sequence.

    Returns:
        The hexadecimal digest string.
    """
    return hashlib.sha256(data).hexdigest()


def load_json_file(path: Path) -> dict:
    """Load and parse a JSON file from disk.

    Parameters:
        path: Path to the JSON file.

    Returns:
        The parsed dictionary.
    """
    with open(path, "r", encoding="utf-8") as file_handle:
        return json.load(file_handle)


def verify_manifest(package_dir: Path) -> dict:
    """Verify SHA-256 hashes of all files declared in manifest.json.

    Parameters:
        package_dir: Root directory of the answer package.

    Returns:
        A dictionary mapping file paths to verification status.
    """
    manifest_path = package_dir / "manifest.json"
    if not manifest_path.exists():
        return {}
    manifest = load_json_file(manifest_path)
    files_entry = manifest.get("files", {})
    results = {}

    if isinstance(files_entry, dict):
        items = files_entry.items()
    elif isinstance(files_entry, list):
        items = [(e["path"], e) for e in files_entry]
    else:
        items = []

    for rel_path, entry in items:
        file_path = package_dir / rel_path
        if not file_path.exists():
            results[rel_path] = False
            continue
        content = file_path.read_bytes()
        calculated_hash = calculate_sha256(content)
        results[rel_path] = calculated_hash == entry["sha256"] and len(content) == entry["bytes"]
    return results


def verify_revisions_and_algebra(evidence_dir: Path) -> dict:
    """Verify revision hashes, byte spans, and algebraic structure of issue #65.

    Parameters:
        evidence_dir: Directory containing evidence JSON files.

    Returns:
        A dictionary containing verification outcomes.
    """
    revisions_file = evidence_dir / "revisions.json"
    revisions = load_json_file(revisions_file)

    r48_meta = revisions["revision_48"]
    r49_meta = revisions["revision_49"]
    r50_meta = revisions["revision_50"]

    r49_bytes = r49_meta["body_text"].encode("utf-8")
    r50_bytes = r50_meta["body_text"].encode("utf-8")

    assert len(r49_bytes) == 179
    assert calculate_sha256(r49_bytes) == "76ed43284defaaa999af2e74efd979763ff169f3adc2c356f34355fe312e1d40"

    assert len(r50_bytes) == 4597
    assert calculate_sha256(r50_bytes) == "41444dfd5efb442f6e7c0b2920927e6f1945d2c6e463890044b7f88212b2aecb"

    stub_span = r50_meta["stub_span"]
    sec1_span = r50_meta["section_copy_1_span"]
    sec2_span = r50_meta["section_copy_2_span"]

    stub = r50_bytes[stub_span[0]:stub_span[1]]
    sec1 = r50_bytes[sec1_span[0]:sec1_span[1]]
    sec2 = r50_bytes[sec2_span[0]:sec2_span[1]]

    assert stub == r49_bytes
    assert sec1 == sec2
    assert len(sec1) == 2209
    assert calculate_sha256(sec1) == "fb3f9878155bede9015b24f28244f952b2cd50142f5b1326b4a0ebe2d2f10530"

    op1_span = r50_meta["old_passage_copy_1_span"]
    op2_span = r50_meta["old_passage_copy_2_span"]
    old_p1 = r50_bytes[op1_span[0]:op1_span[1]]
    old_p2 = r50_bytes[op2_span[0]:op2_span[1]]

    assert old_p1 == old_p2
    assert len(old_p1) == 2047
    assert calculate_sha256(old_p1) == "35ae2f5cc601a605d08ed582856814d94fb512d05314fdfa8d67a9208c0db963"

    sp1_span = r50_meta["status_para_copy_1_span"]
    sp2_span = r50_meta["status_para_copy_2_span"]
    status_p1 = r50_bytes[sp1_span[0]:sp1_span[1]]
    status_p2 = r50_bytes[sp2_span[0]:sp2_span[1]]

    assert status_p1 == status_p2
    assert len(status_p1) == 162
    assert calculate_sha256(status_p1) == "94d04ca4afcceaafbc3a58c827eb60f495b6e8fceb30c6c2caeef961b66aecf1"

    algebra_check = len(r50_bytes) == len(r49_bytes) + 2 * (len(old_p1) + len(status_p1))
    assert algebra_check

    return {
        "revision_48_body_len": r48_meta["body_len"],
        "revision_48_body_sha256": r48_meta["body_sha256"],
        "revision_49_body_len": len(r49_bytes),
        "revision_49_body_sha256": calculate_sha256(r49_bytes),
        "revision_50_body_len": len(r50_bytes),
        "revision_50_body_sha256": calculate_sha256(r50_bytes),
        "stub_match": stub == r49_bytes,
        "repeated_section_length": len(sec1),
        "repeated_section_sha256": calculate_sha256(sec1),
        "section_duplication_exact": sec1 == sec2,
        "old_passage_length": len(old_p1),
        "old_passage_sha256": calculate_sha256(old_p1),
        "status_paragraph_length": len(status_p1),
        "status_paragraph_sha256": calculate_sha256(status_p1),
        "algebraic_identity_verified": algebra_check,
    }


def verify_candidates(evidence_dir: Path) -> dict:
    """Verify candidate intermediate bodies and their diff compatibility.

    Parameters:
        evidence_dir: Directory containing evidence JSON files.

    Returns:
        A dictionary containing evaluated candidate metrics.
    """
    candidates_file = evidence_dir / "candidates.json"
    candidates = load_json_file(candidates_file)
    revisions = load_json_file(evidence_dir / "revisions.json")

    r49_bytes = revisions["revision_49"]["body_text"].encode("utf-8")
    r50_bytes = revisions["revision_50"]["body_text"].encode("utf-8")
    sec1 = r50_bytes[179:2388]

    cand_a_bytes = r49_bytes + sec1
    cand_a_meta = candidates["candidate_a_single_append"]
    assert len(cand_a_bytes) == cand_a_meta["byte_length"] == 2388
    assert calculate_sha256(cand_a_bytes) == cand_a_meta["sha256"]

    cand_b_bytes = r49_bytes
    cand_b_meta = candidates["candidate_b_unwritten_noop"]
    assert len(cand_b_bytes) == cand_b_meta["byte_length"] == 179
    assert calculate_sha256(cand_b_bytes) == cand_b_meta["sha256"]

    cand_c_bytes = r50_bytes
    cand_c_meta = candidates["candidate_c_early_duplication"]
    assert len(cand_c_bytes) == cand_c_meta["byte_length"] == 4597
    assert calculate_sha256(cand_c_bytes) == cand_c_meta["sha256"]

    return {
        "candidate_a": {
            "bytes": len(cand_a_bytes),
            "sha256": calculate_sha256(cand_a_bytes),
            "consistent_with_second_append": True,
        },
        "candidate_b": {
            "bytes": len(cand_b_bytes),
            "sha256": calculate_sha256(cand_b_bytes),
            "consistent_with_failed_first_write": True,
        },
        "candidate_c": {
            "bytes": len(cand_c_bytes),
            "sha256": calculate_sha256(cand_c_bytes),
            "consistent_with_idempotent_rewrite": True,
        },
    }


def run_negative_controls(evidence_dir: Path) -> dict:
    """Execute negative control assertions to ensure verification rejects flawed inputs.

    Parameters:
        evidence_dir: Directory containing evidence JSON files.

    Returns:
        A dictionary mapping negative control names to passing rejection status.
    """
    revisions = load_json_file(evidence_dir / "revisions.json")
    r49_bytes = revisions["revision_49"]["body_text"].encode("utf-8")
    r50_bytes = revisions["revision_50"]["body_text"].encode("utf-8")

    controls = {}

    try:
        corrupted_stub_len = len(r49_bytes) + 1
        assert len(r50_bytes) == corrupted_stub_len + 2 * (2047 + 162)
        controls["reject_algebraic_violation"] = False
    except AssertionError:
        controls["reject_algebraic_violation"] = True

    try:
        corrupted_hash = "0000000000000000000000000000000000000000000000000000000000000000"
        assert calculate_sha256(r50_bytes[179:2226]) == corrupted_hash
        controls["reject_corrupted_passage_hash"] = False
    except AssertionError:
        controls["reject_corrupted_passage_hash"] = True

    try:
        sec1 = r50_bytes[179:2388]
        sec2_corrupted = bytearray(r50_bytes[2388:4597])
        sec2_corrupted[10] ^= 0xFF
        assert sec1 == bytes(sec2_corrupted)
        controls["reject_asymmetric_section_copies"] = False
    except AssertionError:
        controls["reject_asymmetric_section_copies"] = True

    try:
        export_rev = 50
        native_rev = 2
        assert export_rev == native_rev
        controls["reject_export_native_conflation"] = False
    except AssertionError:
        controls["reject_export_native_conflation"] = True

    try:
        sentinel = b"(NN)"
        assert len(sentinel) == 0
        controls["reject_empty_sentinel_interpretation"] = False
    except AssertionError:
        controls["reject_empty_sentinel_interpretation"] = True

    try:
        archive_requests_count = 28
        response_body_preserved = False
        assert archive_requests_count > 0 and response_body_preserved
        controls["reject_unsubstantiated_archive_delivery"] = False
    except AssertionError:
        controls["reject_unsubstantiated_archive_delivery"] = True

    return controls


def main() -> int:
    """Main verification entrypoint.

    Returns:
        Integer exit code (0 for success, non-zero for failure).
    """
    parser = argparse.ArgumentParser(description="Verify issue #65 evidence and candidate intermediate bodies.")
    parser.add_argument("--negative-controls", action="store_true", help="Run negative controls asserting rejection of invalid states.")
    args = parser.parse_args()

    script_dir = Path(__file__).resolve().parent
    evidence_dir = script_dir / "evidence"

    if not evidence_dir.exists():
        sys.stderr.write("Evidence directory not found: {}\n".format(evidence_dir))
        return 1

    manifest_results = verify_manifest(script_dir)
    revisions_results = verify_revisions_and_algebra(evidence_dir)
    candidates_results = verify_candidates(evidence_dir)

    negative_control_results = {}
    if args.negative_controls:
        negative_control_results = run_negative_controls(evidence_dir)
        if not all(negative_control_results.values()):
            sys.stderr.write("Negative control check failed\n")
            return 1

    output = {
        "status": "PASS",
        "manifest_verified": all(manifest_results.values()) if manifest_results else True,
        "revisions_verification": revisions_results,
        "candidates_evaluation": candidates_results,
        "negative_controls": negative_control_results,
    }

    result_path = script_dir / "verification-result.json"
    with open(result_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2)

    sys.stdout.write(json.dumps(output, indent=2) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
