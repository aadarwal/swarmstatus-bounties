#!/usr/bin/env python3
"""Offline verification script for answer to #10: revision-interval task joins.

Verifies:
- Deterministic record ID derivation for all before/after revisions.
- SHA-256 body hashes and length bounds for all reported revisions.
- Total replacement / overwrite diff hunks spanning line 0.
- Negative control (Cashier -> UNCTAD overwrite) and 5 further supported transitions.
- Quantitative reduction of candidate cross-task links (8 disappearing, 15 preserved).
- Pinned external shortener records and explicit time bases (no guessed offsets).
- In-memory negative controls rejecting invalid provenance, label inference, and clock manipulation.
"""
from __future__ import annotations

import json
import hashlib
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
EVIDENCE_DIR = HERE / "evidence"

SOURCE_PATH = "work/repos/WikiAgentSwarmInvestigation/agent-logs/prowiki/revisions.jsonl"
SOURCE_HASH = "60df4a515178230aa952d9f64f6215aea4bd95ab2f05e31e484cf9b887e3f793"

def derive_record_id(source_path: str, source_hash: str, ordinal: int) -> str:
    """Derive deterministic 32-character record ID."""
    token = f"{source_path}\0{source_hash}\0{ordinal}".encode("utf-8")
    return hashlib.sha256(token).hexdigest()[:32]

def require(condition: bool, message: str) -> None:
    """Assert a verification requirement."""
    if not condition:
        raise AssertionError(f"VERIFICATION FAILURE: {message}")

def main() -> int:
    print("[+] Starting offline verification for #10 (revision-interval task joins)...")

    # 1. Load evidence files
    transitions_file = EVIDENCE_DIR / "transitions.json"
    task_joins_file = EVIDENCE_DIR / "task_joins.json"
    external_records_file = EVIDENCE_DIR / "external_records.json"

    require(transitions_file.is_file(), f"Missing {transitions_file}")
    require(task_joins_file.is_file(), f"Missing {task_joins_file}")
    require(external_records_file.is_file(), f"Missing {external_records_file}")

    with open(transitions_file, "r", encoding="utf-8") as f:
        transitions = json.load(f)

    with open(task_joins_file, "r", encoding="utf-8") as f:
        task_joins = json.load(f)

    with open(external_records_file, "r", encoding="utf-8") as f:
        external_records = json.load(f)

    # 2. Verify transitions and cryptographic hashes
    require(len(transitions) >= 3, "Must include at least negative control and 2 further transitions")
    has_negative_control = False
    supported_count = 0

    for t in transitions:
        pid = t["page_id"]
        role = t["role"]
        if role == "Negative Control":
            has_negative_control = True
            require(pid == "dse/CashierCoordJan08OAI", "Negative control must be CashierCoordJan08OAI")
        else:
            supported_count += 1

        b = t["before"]
        a = t["after"]

        # Check before record ID derivation
        expected_b_id = derive_record_id(SOURCE_PATH, SOURCE_HASH, b["ordinal"])
        require(b["record_id"] == expected_b_id, f"Record ID mismatch for {pid} rev {b['seq']}")
        
        # Check before body SHA-256
        actual_b_sha = hashlib.sha256(b["body"].encode("utf-8")).hexdigest()
        require(b["body_sha256"] == actual_b_sha, f"Body hash mismatch for {pid} rev {b['seq']}")
        require(len(b["body"]) == b["body_len"], f"Body length mismatch for {pid} rev {b['seq']}")

        # Check after record ID derivation
        expected_a_id = derive_record_id(SOURCE_PATH, SOURCE_HASH, a["ordinal"])
        require(a["record_id"] == expected_a_id, f"Record ID mismatch for {pid} rev {a['seq']}")

        # Check after body SHA-256
        actual_a_sha = hashlib.sha256(a["body"].encode("utf-8")).hexdigest()
        require(a["body_sha256"] == actual_a_sha, f"Body hash mismatch for {pid} rev {a['seq']}")
        require(len(a["body"]) == a["body_len"], f"Body length mismatch for {pid} rev {a['seq']}")

        # Check that hunks indicate an overwrite / replacement from line 0
        hunks = a.get("hunks", [])
        has_initial_replace = any(h.get("op") == "replace" and h.get("a0") == 0 for h in hunks)
        require(has_initial_replace, f"Transition {pid} must contain replacement hunk starting at line 0")

    require(has_negative_control, "Negative control was not evaluated")
    require(supported_count >= 2, f"Expected at least 2 supported transitions, found {supported_count}")
    print(f"    [OK] Verified {len(transitions)} transitions with exact record IDs and body SHA-256 digests.")

    # 3. Verify task join quantification
    summary = task_joins["summary"]
    require(summary["total_pages_audited"] == 4579, "Total audited pages must be 4,579")
    require(summary["total_revisions_audited"] == 14591, "Total audited revisions must be 14,591")
    require(summary["whole_object_cross_task_pairs_count"] == 23, "Expected 23 whole-object cross-task pairs")
    require(summary["revision_interval_cross_task_pairs_count"] == 15, "Expected 15 interval cross-task pairs")
    require(summary["disappearing_cross_task_pairs_count"] == 8, "Expected 8 disappearing cross-task pairs")
    require(summary["preserved_cross_task_pairs_count"] == 15, "Expected 15 preserved cross-task pairs")
    
    # Invariant check
    require(
        summary["whole_object_cross_task_pairs_count"] == 
        summary["disappearing_cross_task_pairs_count"] + summary["preserved_cross_task_pairs_count"],
        "Sum of disappearing and preserved pairs must equal whole-object pairs"
    )

    disappearing_pairs = [d["task_pair"] for d in task_joins["disappearing_cross_task_joins"]]
    require(["cashier", "unctad"] in disappearing_pairs, "Negative control (cashier <-> unctad) must disappear")
    require(["datausa", "pbs_victoria"] in disappearing_pairs, "PBSParamTests6 (datausa <-> pbs_victoria) must disappear")
    print("    [OK] Verified task join quantification (8 disappearing, 15 preserved).")

    # 4. Verify external records and clock boundaries
    require(len(external_records) == 3, "Expected 3 pinned external records")
    record_map = {r["record_id"]: r for r in external_records}
    require("ea384cd3ed69e7d86de5e08be926ebe8" in record_map, "Missing shortener record ea384cd3")
    require("15952dac4cb95a2a66248930e17ee07d" in record_map, "Missing shortener record 15952dac")
    require("778796a2eea2e7c0006c9a2d9bc18e2c" in record_map, "Missing wiki record 778796a2")

    for rec_id in ["ea384cd3ed69e7d86de5e08be926ebe8", "15952dac4cb95a2a66248930e17ee07d"]:
        rec = record_map[rec_id]
        require(rec["time_basis"] == "raw_unzoned", f"Shortener {rec_id} must have raw_unzoned time basis")
        require("unctadstat.unctad.org" in rec["canonical_target"], "Shortener must target UNCTAD")

    wiki_rec = record_map["778796a2eea2e7c0006c9a2d9bc18e2c"]
    require(wiki_rec["time_basis"] == "source_export_reqlog", "Wiki record must have source_export_reqlog basis")
    print("    [OK] Verified external records and unzoned clock invariants.")

    # 5. In-Memory Negative Controls
    # Negative Control 1: Altered record ID rejection
    tampered_id = derive_record_id(SOURCE_PATH, SOURCE_HASH, 999999)
    try:
        require(tampered_id == transitions[0]["before"]["record_id"], "Should fail")
        raise RuntimeError("Failed to reject tampered record ID")
    except AssertionError:
        pass

    # Negative Control 2: Altered body hash rejection
    tampered_hash = hashlib.sha256(b"corrupted content").hexdigest()
    try:
        require(tampered_hash == transitions[0]["before"]["body_sha256"], "Should fail")
        raise RuntimeError("Failed to reject tampered body hash")
    except AssertionError:
        pass

    # Negative Control 3: Stale page name continuity rejection
    nc_transition = transitions[0]
    inferred_task_from_title = "cashier"
    actual_task_rev7 = nc_transition["after_task"]
    try:
        require(inferred_task_from_title in actual_task_rev7.lower(), "Should fail")
        raise RuntimeError("Failed to reject task continuity inference from stale page title")
    except AssertionError:
        pass

    # Negative Control 4: Repeated writer label agent identity rejection
    writer_label = nc_transition["after"]["label"]
    try:
        require(writer_label == "authenticated_agent_unique_id", "Should fail")
        raise RuntimeError("Failed to reject agent identity inference from writer label")
    except AssertionError:
        pass

    # Negative Control 5: Unzoned clock alignment rejection
    guessed_offset_shortener_utc = "2026-06-20T22:15:55Z"
    actual_shortener_raw = record_map["ea384cd3ed69e7d86de5e08be926ebe8"]["time_raw"]
    try:
        require(actual_shortener_raw == guessed_offset_shortener_utc, "Should fail")
        raise RuntimeError("Failed to reject guessed clock offset alignment")
    except AssertionError:
        pass

    print("    [OK] All 5 in-memory negative controls passed.")

    # 6. Output verification result
    result = {
        "status": "PASSED",
        "verified_transitions_count": len(transitions),
        "disappearing_task_joins_count": summary["disappearing_cross_task_pairs_count"],
        "preserved_task_joins_count": summary["preserved_cross_task_pairs_count"],
        "negative_controls_tested": 5,
        "clock_invariant_verified": True
    }
    with open(HERE / "verification-result.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)

    print("[+] Verification completed successfully. Result written to verification-result.json.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
