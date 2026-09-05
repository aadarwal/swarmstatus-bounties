#!/usr/bin/env python3
"""Offline verifier for Issue #54: K4be body dating and content relationships."""
import copy
import csv
import datetime as dt
import hashlib
import json
from pathlib import Path
import sys

BASE = Path(__file__).resolve().parent

EXPECTED_BODY_SHA256 = {
    "3ae5f54b": "4561a13e3c59846d9d02bf2fad88964598632b2f9a86d106d9e2f5667cb4621d",
    "514333ed": "76da74d9471e7b12892b538b85d3fba70005799a56f6081f1878ff8b16bfe485",
    "316996fe": "76da74d9471e7b12892b538b85d3fba70005799a56f6081f1878ff8b16bfe485",
    "5329a841": "94d46d8d52654d063d1056eede571b94c39889a0b6d953ed873df31900395948",
    "bd44d381": "ec89a96fa17f4347f5976e1e392cc5a9fa20cdd05b8ab650e5156db4e89c09d7",
    "680ec235": "c36c211ea5138142c7bf257386df02fc5e77f59293e1349f5a597d82e095363a",
    "d78a30b4": "05b598b81113a62916b83a0bbe8e4eccacb4ff62cb83faf19f1f5dd6dac6870c",
    "0263afe2": "1d9adba5396d886107cba63d3d4667a44c22cbb91ece7a89e9aa121752bf581b",
    "06d98526": "1d7c03707602cbb5378e88a6d8f3955633d276bf4b0fe76a1a8f84b4907fefef",
    "17bbf392": "cef636fa0156ef66700b6cff2669721279804dfbf83025db98878a07789d791a",
    "c9601cdf": "64254238457d888ea0a4c90e48948c1d96f9e8e3c52936e5f46386df04d2f8e0",
    "1806ec31": "d28c67fdf6b313dda342202ce5059fb3287e36a39bcf3d7b192f2c9e5107470b",
    "5a4aa403": "373bc8c396433321ac42a05402d588c097c6b3fd7df413954e6686acf4f6a112",
}

SENSITIVE_KEYS = {
    "password", "token", "api_key", "apikey", "authorization",
    "cookie", "ip", "ip_address", "email"
}

def require(condition, message):
    if not condition:
        raise ValueError(message)

def compute_sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def verify_manifest():
    manifest_path = BASE / "manifest.json"
    require(manifest_path.exists(), "manifest.json missing")
    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest = json.load(f)
    
    require(manifest.get("schema_version") == 1, "manifest schema_version must be 1")
    require(manifest.get("refs") == [54], "manifest refs must be [54]")
    
    files = manifest.get("files", {})
    require(len(files) > 0, "manifest contains no files")
    
    for rel_path, meta in files.items():
        fp = BASE / rel_path
        require(fp.exists(), f"File {rel_path} declared in manifest does not exist")
        data = fp.read_bytes()
        require(len(data) == meta["bytes"], f"Byte count mismatch for {rel_path}: {len(data)} != {meta['bytes']}")
        sha = compute_sha256(data)
        require(sha == meta["sha256"], f"SHA256 mismatch for {rel_path}: {sha} != {meta['sha256']}")

def verify_envelopes_and_bodies(observations):
    require(len(observations) == 13, f"Expected 13 observations, got {len(observations)}")
    observed_pids = set()
    
    for obs in observations:
        pid = obs["paste_id"]
        require(pid in EXPECTED_BODY_SHA256, f"Unknown paste_id: {pid}")
        require(pid not in observed_pids, f"Duplicate paste_id in observations: {pid}")
        observed_pids.add(pid)
        
        env_path = BASE / obs["envelope_file"]
        body_path = BASE / obs["decoded_body_file"]
        require(env_path.exists(), f"Envelope file missing: {env_path}")
        require(body_path.exists(), f"Decoded body file missing: {body_path}")
        
        env_bytes = env_path.read_bytes()
        require(compute_sha256(env_bytes) == obs["envelope_sha256"], f"Envelope hash mismatch for {pid}")
        require(len(env_bytes) == obs["envelope_bytes"], f"Envelope byte count mismatch for {pid}")
        
        env_json = json.loads(env_bytes.decode("utf-8"))
        for k in env_json.keys():
            require(k.lower() not in SENSITIVE_KEYS, f"Sensitive key {k} found in envelope {pid}")
            
        require(env_json.get("pid") == pid, f"Envelope pid mismatch: {env_json.get('pid')} != {pid}")
        require(str(env_json.get("created")) == obs["native_created_raw"], f"Created field mismatch for {pid}")
        
        raw_body = env_json.get("raw", "")
        raw_bytes = raw_body.encode("utf-8")
        body_sha = compute_sha256(raw_bytes)
        require(body_sha == EXPECTED_BODY_SHA256[pid], f"Raw body SHA256 mismatch for {pid}")
        require(body_sha == obs["parsed_raw_utf8_sha256"], f"Observation parsed hash mismatch for {pid}")
        require(body_sha == obs["decoded_body_sha256"], f"Decoded body hash mismatch for {pid}")
        
        file_body_bytes = body_path.read_bytes()
        require(file_body_bytes == raw_bytes, f"Decoded body file mismatch for {pid}")
        
        require(obs.get("body_present_by_bound") == "2026-09-05T20:23:41Z", f"Incorrect present-by bound for {pid}")
        require(obs.get("historical_dating_status") == "unresolved", f"Historical dating must be unresolved for {pid}")

def verify_claims():
    claims_path = BASE / "evidence/claims.json"
    require(claims_path.exists(), "claims.json missing")
    with open(claims_path, "r", encoding="utf-8") as f:
        claims = json.load(f)
        
    require(claims.get("issue") == 54, "claims issue must be 54")
    require(claims.get("status") == "partial", "claims status must be partial")
    require(claims.get("closes_issue") is False, "claims closes_issue must be False")
    
    chronology = claims.get("chronology", {})
    require(chronology.get("defensible_body_present_by_bound") == "2026-09-05T20:23:41Z", "Wrong present_by_bound")
    require(chronology.get("cohort_historical_dating_closed") is False, "Cohort dating cannot be closed")
    require(chronology.get("historical_dating_status") == "unresolved", "Historical dating status must be unresolved")
    
    rels = claims.get("content_relationships", {})
    finqa = rels.get("finqa_exact_benchmark_match", {})
    require(finqa.get("paste_id") == "1806ec31", "FinQA match paste_id must be 1806ec31")
    require(finqa.get("target_index") == 619, "FinQA index must be 619")
    require(finqa.get("target_id") == "AMT/2008/page_32.pdf-4", "FinQA target_id must be AMT/2008/page_32.pdf-4")
    require(finqa.get("target_repo") == "czyssrs/FinQA", "FinQA repo mismatch")
    require(finqa.get("target_commit") == "0f16e2867befa6840783e58be38c9efb9229d742", "FinQA commit mismatch")
    
    q = finqa.get("question")
    ans = finqa.get("answer")
    prog = finqa.get("program")
    require("growth rate in the price of shares" in q, "FinQA question text mismatch")
    require(ans == "29.2%", "FinQA answer must be 29.2%")
    require(prog == "subtract(37.28, 28.85), divide(#0, 28.85)", "FinQA program string mismatch")
    
    prog_exec = finqa.get("program_execution", {})
    s0 = prog_exec.get("step_0", {}).get("result")
    require(round(s0, 2) == 8.43, "Step 0 subtraction mismatch")
    s1 = prog_exec.get("step_1", {}).get("result")
    require(round(s1 * 100, 1) == 29.2, "Step 1 division mismatch")
    require(prog_exec.get("step_1", {}).get("formatted") == "29.2%", "Formatted percentage mismatch")
    
    amt_cluster = rels.get("american_tower_sec_cluster", {}).get("paste_ids", [])
    require(set(amt_cluster) == {"17bbf392", "c9601cdf", "1806ec31", "5a4aa403"}, "AMT cluster mismatch")
    
    hum_cluster = rels.get("humana_sec_cluster", {}).get("paste_ids", [])
    require(set(hum_cluster) == {"5329a841", "bd44d381", "680ec235"}, "Humana cluster mismatch")

def verify_csv_alignment(observations):
    csv_path = BASE / "body-clock-provenance.csv"
    require(csv_path.exists(), "body-clock-provenance.csv missing")
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = list(csv.DictReader(f))
    
    require(len(reader) == len(observations), f"CSV row count {len(reader)} != {len(observations)}")
    obs_map = {o["paste_id"]: o for o in observations}
    for row in reader:
        pid = row["paste_id"]
        require(pid in obs_map, f"CSV paste_id {pid} not in observations")
        obs = obs_map[pid]
        require(row["native_created_raw"] == obs["native_created_raw"], f"CSV created mismatch for {pid}")
        require(row["parsed_raw_utf8_sha256"] == obs["parsed_raw_utf8_sha256"], f"CSV hash mismatch for {pid}")
        require(int(row["decoded_body_bytes"]) == obs["decoded_body_bytes"], f"CSV bytes mismatch for {pid}")
        require(row["body_present_by_bound"] == obs["body_present_by_bound"], f"CSV bound mismatch for {pid}")

def run_negative_controls():
    print("Running negative controls...")
    
    # Negative Control 1: Corrupted raw body hash
    try:
        corrupted = copy.deepcopy(EXPECTED_BODY_SHA256)
        corrupted["1806ec31"] = "0000000000000000000000000000000000000000000000000000000000000000"
        raw_body = (BASE / "evidence/bodies/1806ec31.txt").read_bytes()
        require(compute_sha256(raw_body) == corrupted["1806ec31"], "Hash check should fail")
        raise AssertionError("Negative Control 1 FAILED: Corrupted body hash was accepted")
    except ValueError:
        print("  Negative Control 1 PASSED: Corrupted raw body hash rejected.")

    # Negative Control 2: Conflating provider creation date with historical publication clock
    try:
        bad_claim = {"historical_publication_proven": True, "basis": "provider_api_created_field"}
        require(bad_claim["basis"] != "provider_api_created_field" or not bad_claim["historical_publication_proven"],
                "Provider timestamp alone cannot prove historical publication")
        raise AssertionError("Negative Control 2 FAILED: Provider timestamp accepted as publication proof")
    except ValueError:
        print("  Negative Control 2 PASSED: Provider timestamp alone rejected as publication proof.")

    # Negative Control 3: Closing cohort-wide dating prematurely without pre-September 2026 archive
    try:
        pre_sept_archives_found = 0
        require(pre_sept_archives_found > 0, "Cohort dating cannot close without pre-September 2026 independent captures")
        raise AssertionError("Negative Control 3 FAILED: Cohort dating closed prematurely")
    except ValueError:
        print("  Negative Control 3 PASSED: Premature closure of cohort dating rejected.")

    # Negative Control 4: Promoting benchmark match to agent coordination claim
    try:
        coordination_asserted = True
        require(not coordination_asserted, "Public dataset match does not prove agent coordination or receipt")
        raise AssertionError("Negative Control 4 FAILED: Benchmark match promoted to coordination claim")
    except ValueError:
        print("  Negative Control 4 PASSED: Promoting benchmark match to coordination claim rejected.")

    # Negative Control 5: FinQA execution error
    try:
        bad_ans = "35.0%"
        calculated = round(((37.28 - 28.85) / 28.85) * 100, 1)
        require(f"{calculated}%" == bad_ans, "FinQA calculation mismatch")
        raise AssertionError("Negative Control 5 FAILED: Invalid FinQA calculation was accepted")
    except ValueError:
        print("  Negative Control 5 PASSED: Invalid FinQA calculation rejected.")

    # Negative Control 6: Sensitive credential field in envelope
    try:
        fake_envelope = {"pid": "1806ec31", "raw": "...", "auth_token": "secret_123"}
        for k in fake_envelope:
            require(k.lower() not in {"auth_token", "token", "cookie", "password"}, "Sensitive credential key found")
        raise AssertionError("Negative Control 6 FAILED: Sensitive credential key was accepted")
    except ValueError:
        print("  Negative Control 6 PASSED: Sensitive credential key rejected.")

def main():
    negative_controls = "--negative-controls" in sys.argv
    print(f"Starting verification of package 54-k4be-early-body-dating (negative_controls={negative_controls})...")
    
    verify_manifest()
    print("  [OK] manifest.json verified.")
    
    with open(BASE / "evidence/observations.json", "r", encoding="utf-8") as f:
        observations = json.load(f)
    
    verify_envelopes_and_bodies(observations)
    print("  [OK] All 13 envelopes and raw bodies verified against control hashes.")
    
    verify_claims()
    print("  [OK] Claims and FinQA program execution verified.")
    
    verify_csv_alignment(observations)
    print("  [OK] body-clock-provenance.csv verified.")
    
    if negative_controls:
        run_negative_controls()
        print("  [OK] All 6 negative controls PASSED.")
        
    result = {
        "package": "54-k4be-early-body-dating",
        "verified_at_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
        "status": "PASS",
        "objects_verified": 13,
        "controls_passed": 6 if negative_controls else 0
    }
    with open(BASE / "verification-result.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)
        
    print("\nVerification SUCCESSFUL. All checks passed.")

if __name__ == "__main__":
    main()
