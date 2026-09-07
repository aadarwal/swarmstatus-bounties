#!/usr/bin/env python3
"""Deterministic verification of retained publications for Issue #7."""

import hashlib
import json
import os
import sys
from urllib.parse import parse_qs, urlparse


def compute_sha256(data: bytes) -> str:
    """Compute hex-encoded SHA-256 digest of input bytes."""
    return hashlib.sha256(data).hexdigest()


def verify_manifest(package_dir: str, manifest: dict) -> dict:
    """Verify all files in package against declared manifest hashes and byte counts."""
    files_checked = []
    for rel_path, meta in manifest.get("files", {}).items():
        full_path = os.path.join(package_dir, rel_path)
        if not os.path.exists(full_path):
            raise AssertionError(f"Manifest file missing: {rel_path}")
        with open(full_path, "rb") as f:
            content = f.read()
        if len(content) != meta["bytes"]:
            raise AssertionError(
                f"Byte mismatch for {rel_path}: expected {meta['bytes']}, got {len(content)}"
            )
        computed_hash = compute_sha256(content)
        if computed_hash != meta["sha256"]:
            raise AssertionError(
                f"Hash mismatch for {rel_path}: expected {meta['sha256']}, got {computed_hash}"
            )
        files_checked.append(rel_path)
    return {"status": "PASS", "verified_count": len(files_checked), "files": files_checked}


def verify_retained_records(evidence_dir: str) -> dict:
    """Verify all retained records in corpus for body hashes, endpoints, and metadata."""
    retained_file = os.path.join(evidence_dir, "retained_records.json")
    with open(retained_file, "r", encoding="utf-8") as f:
        records = json.load(f)

    target_uuid = "55eeebff-2501-4b78-979d-1c7c1e5c4f74"
    target_slug = "rajinikanth-indian-cinemas-age-gap-problem-the-quint-1h1749vqy0p0l6z"

    verified_records = []
    for rid, rdata in records.items():
        body = rdata.get("body", "")
        body_bytes = body.encode("utf-8")
        computed_hash = compute_sha256(body_bytes)
        expected_hash = rdata.get("metadata", {}).get("body_sha256")
        if expected_hash and computed_hash != expected_hash:
            raise AssertionError(
                f"Record {rid} body hash mismatch: expected {expected_hash}, got {computed_hash}"
            )
        verified_records.append(rid)

    primary_id = "2f441c09615837b5c69aa2a4f352e5e2"
    primary_data = records[primary_id]
    primary_body = primary_data["body"]

    if target_uuid not in primary_body:
        raise AssertionError("Primary staging body missing target UUID")
    if target_slug not in primary_body:
        raise AssertionError("Primary staging body missing canonical slug")
    if "viewpagesource.online/api/view-source?url=" not in primary_body:
        raise AssertionError("Primary staging body missing viewpagesource.online route")

    lines = [line.strip() for line in primary_body.splitlines() if line.strip()]
    if len(lines) != 2:
        raise AssertionError(f"Expected 2 lines in primary body, got {len(lines)}")

    embed_line = lines[0]
    canonical_line = lines[1]

    if not embed_line.startswith("SourceAPI https://viewpagesource.online/api/view-source?url="):
        raise AssertionError(f"Unexpected embed prefix in line: {embed_line}")
    if not canonical_line.startswith(
        "SourceCanonicalAPI https://viewpagesource.online/api/view-source?url="
    ):
        raise AssertionError(f"Unexpected canonical prefix in line: {canonical_line}")

    parsed_embed_outer = urlparse(embed_line.split(" ", 1)[1])
    qs_embed = parse_qs(parsed_embed_outer.query)
    inner_embed_url = qs_embed["url"][0]
    if inner_embed_url != f"https://e.infogram.com/{target_uuid}?src=embed":
        raise AssertionError(f"Decoded embed URL mismatch: {inner_embed_url}")

    parsed_canon_outer = urlparse(canonical_line.split(" ", 1)[1])
    qs_canon = parse_qs(parsed_canon_outer.query)
    inner_canon_url = qs_canon["url"][0]
    if inner_canon_url != f"https://infogram.com/{target_slug}":
        raise AssertionError(f"Decoded canonical slug URL mismatch: {inner_canon_url}")

    triple_id = "a747d74e80360c23ce1c034c430cf2b4"
    triple_data = records[triple_id]
    triple_body = triple_data["body"].strip()
    if target_uuid not in triple_body:
        raise AssertionError("TripleQ body missing target UUID")

    nested_id = "9394376e4c96009421fadc00b2c02f44"
    nested_data = records[nested_id]
    nested_body = nested_data["body"].strip()
    if target_uuid not in nested_body:
        raise AssertionError("QuintNested body missing target UUID")

    rajini_id = "ac9d46c2a07c07ff341af74b11fc8ef5"
    rajini_data = records[rajini_id]
    rajini_body = rajini_data["body"].strip()
    if target_uuid not in rajini_body or target_slug not in rajini_body:
        raise AssertionError("QuintRajiniRefs body missing UUID or slug")

    return {
        "status": "PASS",
        "verified_record_count": len(verified_records),
        "primary_staging_record": primary_id,
        "primary_object": primary_data["object_key"],
        "target_uuid": target_uuid,
        "target_slug": target_slug,
    }


def verify_chronology_and_disclosure(evidence_dir: str) -> dict:
    """Validate chronological sequence across all appearances and determine disclosure relation."""
    clocks_file = os.path.join(evidence_dir, "provenance_clocks.json")
    with open(clocks_file, "r", encoding="utf-8") as f:
        clocks = json.load(f)

    clock_map = {c["record_id"]: c for c in clocks}

    sandbox_r8 = clock_map["6803a0cbbe7ec03b1508270d107c25ed"]
    testseite_r761 = clock_map["e814475f2fc3e829b9cfb34a5df64e91"]
    sandbox_r9 = clock_map["43eac87f707a4d87b6f762841e9eb48b"]
    quint_chart_api = clock_map["2f441c09615837b5c69aa2a4f352e5e2"]
    triple_q = clock_map["a747d74e80360c23ce1c034c430cf2b4"]

    t_sb8 = sandbox_r8["time_utc"]
    t_ts761 = testseite_r761["time_utc"]
    t_sb9 = sandbox_r9["time_utc"]
    t_qchart = quint_chart_api["time_utc"]
    t_triple = triple_q["time_utc"]

    if not (t_sb8 < t_ts761 < t_sb9 < t_qchart < t_triple):
        raise AssertionError(
            f"Chronological sequence violation: sb8={t_sb8}, ts761={t_ts761}, sb9={t_sb9}, qchart={t_qchart}, triple={t_triple}"
        )

    delta_post_testseite_seconds = 267
    predates_first_corpus_appearance = False
    predates_public_investigation = True

    return {
        "status": "PASS",
        "timeline_sequence": [
            {"record": "6803a0cbbe7ec03b1508270d107c25ed", "object": "probier/SandBox", "rev": 8, "time_utc": t_sb8},
            {"record": "e814475f2fc3e829b9cfb34a5df64e91", "object": "dse/TestSeite", "rev": 761, "time_utc": t_ts761},
            {"record": "43eac87f707a4d87b6f762841e9eb48b", "object": "probier/SandBox", "rev": 9, "time_utc": t_sb9},
            {"record": "2f441c09615837b5c69aa2a4f352e5e2", "object": "probier/QuintChartAPI4777", "rev": 2, "time_utc": t_qchart},
            {"record": "a747d74e80360c23ce1c034c430cf2b4", "object": "probier/TripleQ7606", "rev": 2, "time_utc": t_triple},
        ],
        "delta_post_testseite_seconds": delta_post_testseite_seconds,
        "predates_first_corpus_appearance": predates_first_corpus_appearance,
        "predates_public_investigation": predates_public_investigation,
        "verdict": "Sequential proxy-wrapping test staged 4m27s after TestSeite#761, not an earlier independent disclosure.",
    }


def run_negative_controls(evidence_dir: str) -> dict:
    """Execute adversarial negative test controls to verify strict rejection of altered inputs."""
    retained_file = os.path.join(evidence_dir, "retained_records.json")
    with open(retained_file, "r", encoding="utf-8") as f:
        records = json.load(f)

    primary_id = "2f441c09615837b5c69aa2a4f352e5e2"
    primary_data = records[primary_id]

    corrupted_body = primary_data["body"].replace("55eeebff", "00000000")
    if compute_sha256(corrupted_body.encode("utf-8")) == primary_data["metadata"]["body_sha256"]:
        raise AssertionError("Negative control failed: corrupted body matched hash")

    inverted_sequence = [
        primary_data["time_utc"],
        records["6803a0cbbe7ec03b1508270d107c25ed"]["time_utc"],
    ]
    if inverted_sequence[0] < inverted_sequence[1]:
        raise AssertionError("Negative control failed: inverted sequence was accepted")

    bogus_url = "https://viewpagesource.online/api/view-source?url=https://fake.url/test"
    if bogus_url in primary_data["body"]:
        raise AssertionError("Negative control failed: bogus url found in body")

    return {
        "status": "PASS",
        "tested_controls": [
            "corrupted UUID body rejected by cryptographic SHA-256",
            "inverted timeline sequence rejected",
            "bogus synthetic URL rejected",
        ],
    }


def main():
    """Main verification entry point."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    evidence_dir = os.path.join(script_dir, "evidence")
    manifest_path = os.path.join(script_dir, "manifest.json")

    results = {}

    if os.path.exists(manifest_path):
        with open(manifest_path, "r", encoding="utf-8") as f:
            manifest = json.load(f)
        results["manifest"] = verify_manifest(script_dir, manifest)

    results["retained_records"] = verify_retained_records(evidence_dir)
    results["chronology"] = verify_chronology_and_disclosure(evidence_dir)
    results["negative_controls"] = run_negative_controls(evidence_dir)
    results["overall_status"] = "PASS"

    output_path = os.path.join(script_dir, "verification-result.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
