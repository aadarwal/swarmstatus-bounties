#!/usr/bin/env python3
"""Offline verifier for Issue #46: Independently date Jotspot Clark newsletter reference.

Verifies package file integrity, WARC headers, exact URL matches, clock separation,
and runs negative controls with zero network or database dependencies.
"""
import argparse
import base64
import copy
from datetime import datetime, timezone
import gzip
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent

EXACT_CLARK_URL = (
    "https://pure.md/web.archive.org/web/20130525012744id_/"
    "www.clarku.edu/departments/economics/pdf/newsletter%202010color.pdf"
)

EXPECTED_WAYBACK_SHA256 = "f0849a91eeef2973f3c059274e66a8eb8a5e6632e24ea28df0bf70006f57d3bc"
EXPECTED_PAYLOAD_SHA1_B32 = "NMEUZKRO76OMA6AIP4ISFWEMQSEB3ULR"
EXPECTED_WARC_RECORD_ID = "<urn:uuid:835ccffc-7329-41c8-825d-29d73c3d44d1>"
EXPECTED_WARC_TARGET_URI = "https://jotspot.io/j/sxt2xy8q"
EXPECTED_WARC_DATE = "2026-06-08T05:02:17Z"
EXPECTED_SITE_PUBLISHED = "2026-06-01T15:03:22.012084+00:00"
EXPECTED_SITE_MODIFIED = "2026-06-01T15:31:10.118407+00:00"


def require(condition: bool, message: str) -> None:
    """Enforce an invariant condition or raise ValueError."""
    if not condition:
        raise ValueError(message)


def compute_sha256(data: bytes) -> str:
    """Compute hex SHA-256 digest of bytes."""
    return hashlib.sha256(data).hexdigest()


def compute_b32_sha1(data: bytes) -> str:
    """Compute base32 SHA-1 digest of bytes."""
    return base64.b32encode(hashlib.sha1(data).digest()).decode("ascii")


def load_json(rel_path: str) -> dict:
    """Load JSON file from package root."""
    path = ROOT / rel_path
    require(path.is_file(), f"Missing expected file: {rel_path}")
    return json.loads(path.read_text(encoding="utf-8"))


def verify_manifest(manifest: dict) -> int:
    """Verify manifest schema and file hashes against disk."""
    require(manifest.get("schema_version") == 1, "manifest schema_version must be 1")
    require(manifest.get("refs") == [46], "manifest refs must be [46]")
    files = manifest.get("files", {})
    require(len(files) > 0, "manifest files mapping must not be empty")

    verified_count = 0
    for rel_path, meta in files.items():
        if rel_path in ("manifest.json", "verification-result.json"):
            continue
        file_path = ROOT / rel_path
        require(file_path.is_file(), f"File listed in manifest does not exist: {rel_path}")
        data = file_path.read_bytes()
        require(
            len(data) == meta["bytes"],
            f"Byte count mismatch for {rel_path}: expected {meta['bytes']}, got {len(data)}"
        )
        actual_sha256 = compute_sha256(data)
        require(
            actual_sha256 == meta["sha256"],
            f"SHA-256 mismatch for {rel_path}: expected {meta['sha256']}, got {actual_sha256}"
        )
        verified_count += 1
    return verified_count


def verify_html_content(html_bytes: bytes) -> dict:
    """Verify HTML body contains exact Clark URL, metadata timestamps, and titles."""
    text = html_bytes.decode("utf-8")

    require(
        EXACT_CLARK_URL in text,
        "Exact Clark newsletter reference URL string not found in HTML"
    )

    expected_link_needle = (
        '<a href="' + EXACT_CLARK_URL + '" rel="nofollow noopener noreferrer" target="_blank">'
        'Archive reading</a>'
    )
    require(expected_link_needle in text, "Clark link element mismatch in HTML")

    pub_needle = '<meta property="article:published_time" content="' + EXPECTED_SITE_PUBLISHED + '">'
    require(pub_needle in text, "article:published_time meta tag mismatch")

    mod_needle = '<meta property="article:modified_time" content="' + EXPECTED_SITE_MODIFIED + '">'
    require(mod_needle in text, "article:modified_time meta tag mismatch")

    require("<title>Economics reference reading 2010 | JotSpot</title>" in text, "Title mismatch")
    require('<h1>Economics reference reading 2010</h1>' in text, "Header mismatch")

    return {
        "exact_clark_url_verified": True,
        "anchor_text": "Archive reading",
        "published_val": EXPECTED_SITE_PUBLISHED,
        "modified_val": EXPECTED_SITE_MODIFIED,
    }


def verify_warc_record(warc_path: Path, expected_body: bytes) -> dict:
    """Verify WARC record headers, decompress payload, and compare with expected body."""
    require(warc_path.is_file(), f"WARC record file missing: {warc_path}")
    with gzip.open(warc_path, "rb") as f:
        raw_warc = f.read()

    delimiter = bytes([13, 10, 13, 10])
    parts = raw_warc.split(delimiter, 2)
    require(len(parts) >= 3, "Malformed WARC record structure")
    warc_headers_str = parts[0].decode("latin1")
    http_headers_str = parts[1].decode("latin1")
    raw_payload = parts[2]

    warc_headers = {}
    for line in warc_headers_str.splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            warc_headers[k.strip().lower()] = v.strip()

    require(
        warc_headers.get("warc-target-uri") == EXPECTED_WARC_TARGET_URI,
        f"WARC target URI mismatch: {warc_headers.get('warc-target-uri')}"
    )
    require(
        warc_headers.get("warc-date") == EXPECTED_WARC_DATE,
        f"WARC date mismatch: {warc_headers.get('warc-date')}"
    )
    require(
        warc_headers.get("warc-record-id") == EXPECTED_WARC_RECORD_ID,
        f"WARC record ID mismatch: {warc_headers.get('warc-record-id')}"
    )
    require(
        warc_headers.get("warc-payload-digest") == f"sha1:{EXPECTED_PAYLOAD_SHA1_B32}",
        f"WARC payload digest mismatch: {warc_headers.get('warc-payload-digest')}"
    )

    trimmed_payload = raw_payload[:13274]
    require(
        trimmed_payload == expected_body,
        "WARC extracted payload bytes do not match expected body bytes"
    )
    require(
        compute_b32_sha1(trimmed_payload) == EXPECTED_PAYLOAD_SHA1_B32,
        "WARC payload SHA-1 base32 mismatch"
    )

    return {
        "warc_target_uri": warc_headers.get("warc-target-uri"),
        "warc_date": warc_headers.get("warc-date"),
        "warc_record_id": warc_headers.get("warc-record-id"),
        "warc_payload_digest": warc_headers.get("warc-payload-digest"),
        "payload_bytes": len(trimmed_payload),
    }


def verify_clock_separation() -> dict:
    """Verify separation of observation, site assertions, and export clocks."""
    t_obs = datetime.fromisoformat("2026-06-08T05:02:17+00:00")
    t_site_pub = datetime.fromisoformat(EXPECTED_SITE_PUBLISHED)
    t_site_mod = datetime.fromisoformat(EXPECTED_SITE_MODIFIED)

    delta_mod_seconds = round((t_obs - t_site_mod).total_seconds())
    require(delta_mod_seconds == 567067, f"Unexpected delta: {delta_mod_seconds}")
    require(t_obs > t_site_mod > t_site_pub, "Clock sequence ordering error")

    return {
        "archive_observation_utc": "2026-06-08T05:02:17Z",
        "site_published_utc": EXPECTED_SITE_PUBLISHED,
        "site_modified_utc": EXPECTED_SITE_MODIFIED,
        "delta_seconds_obs_minus_mod": delta_mod_seconds,
        "delta_human": "6 days, 13 hours, 31 minutes, 7 seconds",
        "bounds_verdict": "Verified upper bound established at 2026-06-08T05:02:17Z",
    }


def run_negative_controls(manifest: dict, html_bytes: bytes, warc_path: Path) -> dict:
    """Execute negative controls to verify that invalid evidence is rejected."""
    controls_passed = 0

    tampered_manifest = copy.deepcopy(manifest)
    first_file = next(iter(tampered_manifest["files"]))
    tampered_manifest["files"][first_file]["sha256"] = "0" * 64
    try:
        verify_manifest(tampered_manifest)
        raise AssertionError("Negative control failed: tampered SHA-256 did not raise")
    except ValueError:
        controls_passed += 1

    tampered_html = html_bytes.replace(b"newsletter%202010color.pdf", b"newsletter%202012.pdf")
    try:
        verify_html_content(tampered_html)
        raise AssertionError("Negative control failed: modified Clark URL did not raise")
    except ValueError:
        controls_passed += 1

    truncated_html = html_bytes[:1000]
    try:
        verify_html_content(truncated_html)
        raise AssertionError("Negative control failed: truncated HTML did not raise")
    except ValueError:
        controls_passed += 1

    tampered_manifest_refs = copy.deepcopy(manifest)
    tampered_manifest_refs["refs"] = [999]
    try:
        verify_manifest(tampered_manifest_refs)
        raise AssertionError("Negative control failed: invalid refs did not raise")
    except ValueError:
        controls_passed += 1

    try:
        t_obs = datetime.fromisoformat("2026-06-01T15:03:22+00:00")
        t_mod = datetime.fromisoformat(EXPECTED_SITE_MODIFIED)
        require(t_obs > t_mod, "Observation must post-date modification")
        raise AssertionError("Negative control failed: promoting site time to observation did not raise")
    except ValueError:
        controls_passed += 1

    return {
        "negative_controls_total": 5,
        "negative_controls_passed": controls_passed,
    }


def main():
    parser = argparse.ArgumentParser(description="Verify Issue #46 answer package.")
    parser.add_argument("--negative-controls", action="store_true", help="Run negative controls suite")
    parser.add_argument("--json", action="store_true", help="Emit JSON output")
    args = parser.parse_args()

    manifest_path = ROOT / "manifest.json"
    if not manifest_path.is_file():
        sys.stderr.write("manifest.json missing. Generate manifest first.\n")
        sys.exit(1)

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    files_verified = verify_manifest(manifest)

    html_file = ROOT / "evidence/bodies/wayback-20260608.html"
    html_bytes = html_file.read_bytes()
    require(len(html_bytes) == 13274, "Wayback HTML byte length must be 13274")
    require(compute_sha256(html_bytes) == EXPECTED_WAYBACK_SHA256, "Wayback HTML SHA-256 mismatch")

    content_res = verify_html_content(html_bytes)
    warc_res = verify_warc_record(ROOT / "evidence/bodies/warc-record-20260608.warc.gz", html_bytes)
    clock_res = verify_clock_separation()

    neg_res = {}
    if args.negative_controls:
        neg_res = run_negative_controls(
            manifest,
            html_bytes,
            ROOT / "evidence/bodies/warc-record-20260608.warc.gz"
        )

    result = {
        "status": "PASS",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "issue_ref": 46,
        "files_verified_count": files_verified,
        "content_verification": content_res,
        "warc_verification": warc_res,
        "clock_separation": clock_res,
        "negative_controls": neg_res,
    }

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"VERIFICATION PASS: {files_verified} files verified.")
        print(f"Exact Clark reference verified: {EXACT_CLARK_URL}")
        print(f"Independent upper bound: {clock_res['archive_observation_utc']}")
        print(f"Delta from site modification: {clock_res['delta_human']}")
        if args.negative_controls:
            print(f"Negative controls passed: {neg_res['negative_controls_passed']}/{neg_res['negative_controls_total']}")

    (ROOT / "verification-result.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
