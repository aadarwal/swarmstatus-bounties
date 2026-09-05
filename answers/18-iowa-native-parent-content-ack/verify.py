#!/usr/bin/env python3
"""Package-only verifier. No network, database, imports of source code or output writes."""
import argparse
import copy
import csv
from datetime import datetime, timezone
import hashlib
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
EXPECTED = {
    "7a45b400": ("dac704aaa0f079ccf471e57ae8d9a633a1fdd0238b580149c8b43be13e3bf6fa", 1274),
    "e53f96e2": ("b07bcc35a0d9be178f437420ceaa5f67939e59126c66f795ac0b1f2f68b7983b", 607),
    "d509c771": ("c199b0df812b465a7498f86714a12d74a8401cfbe1b4a11d4a3bf5759c47cfea", 930),
    "8246f250": ("8701d2f2638a7c2d23f6e85e16b7dce39c000c05ec632b51f425fd0a5ca6b71f", 1033),
}

def require(condition, message):
    if not condition:
        raise ValueError(message)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def load(name):
    return json.loads((ROOT / name).read_text(encoding="utf-8"))

def local(name):
    path = (ROOT / name).resolve()
    require(path.is_relative_to(ROOT), "Non-package path")
    require(path.is_file(), "Missing file: " + name)
    return path

def utc(epoch):
    return datetime.fromtimestamp(int(epoch), timezone.utc).isoformat().replace("+00:00", "Z")

def validate_native(api, claim):
    child, parent = api["7a45b400"], api["e53f96e2"]
    require(child["inreply"]["url"] == parent["url"], "Wrong native parent")
    require(parent["raw"] == "hello-from-our-agent", "Changed greeting control")
    require("PLEASE post exact Q5 wording before answering" in child["raw"], "Child request missing")
    require(claim["semantic_class"] == "structural_only", "Parent relation promoted to an answer")
    require(claim["request_answer_edge"] is False, "Unsupported request-answer edge")
    require(claim["created_delta_seconds"] == int(child["created"]) - int(parent["created"]) == 4323, "Parent clock arithmetic")

def validate_ack(api, claim):
    report, ack = api["d509c771"], api["8246f250"]
    text = html.unescape(ack["raw"])
    require("Thanks @" + report["name"] + "!" in text, "Literal addressee mismatch")
    require("85 and older" in text and "85 and older" in html.unescape(report["raw"]), "Q5 text mismatch")
    require("inreply" not in report and "inreply" not in ack, "Unexpected native reply field")
    require(report["url"] not in text and report["pid"] not in text, "Exact report object actually cited")
    require(claim["exact_report_url_present"] is False, "Claimed exact URL without evidence")
    require(claim["provider_stored_relation"] is False, "Text ACK promoted to native relation")
    require(claim["independent_receipt_verified"] is False, "Unsupported delivery receipt")
    require(claim["unique_report_object_resolved"] is False, "Label match promoted to unique object")
    require(claim["created_delta_seconds"] == int(ack["created"]) - int(report["created"]) == 57, "ACK clock arithmetic")

def validate_body(api, observation):
    value = api[observation["paste_id"]]["raw"]
    decoded = html.unescape(value).encode("utf-8")
    require(sha(value.encode("utf-8")) == observation["parsed_raw_utf8_sha256"], "Parsed raw hash")
    require(sha(decoded) == observation["decoded_body_sha256"], "Decoded hash confused with capture")
    require(sha(decoded) == observation["canonical_body_sha256"], "Declared canonical body mismatch")
    require(local(observation["decoded_body_file"]).read_bytes() == decoded, "Derived body bytes")
    require(len(decoded) == observation["decoded_body_bytes"], "Derived body length")
    require(observation["canonical_body_preexisting"] is True, "Preexisting body misclassified")
    return decoded

def verify(negative_controls=False):
    manifest = load("manifest.json")
    require(manifest["schema_version"] == 1, "Manifest version")
    for filename, expected in manifest["files"].items():
        data = local(filename).read_bytes()
        require(len(data) == expected["bytes"] and sha(data) == expected["sha256"], "File integrity: " + filename)
    observations = load("evidence/observations.json")
    require(len(observations) == 4, "Object count")
    byid = {x["paste_id"]: x for x in observations}
    require(set(byid) == set(EXPECTED), "Object set")
    api = {}
    for pid, (expected_hash, expected_length) in EXPECTED.items():
        row = byid[pid]
        raw = local(row["envelope_file"]).read_bytes()
        require(sha(raw) == expected_hash == row["envelope_sha256"], "Original envelope hash")
        require(len(raw) == expected_length == row["envelope_bytes"], "Original envelope length")
        api[pid] = json.loads(raw)
        require(api[pid]["pid"] == pid and api[pid]["url"] == row["view_url"], "Exact object locator")
        require(row["api_url"] == "https://paste.linuxiarz.pl/api/paste/" + pid, "Exact acquired API locator")
        require(api[pid]["private"] == "0", "Private field control")
        sensitive = {"password", "token", "api_key", "apikey", "authorization", "cookie", "ip", "ip_address", "email"}
        require(not sensitive.intersection(api[pid]), "Sensitive envelope field")
        validate_body(api, row)
        require(row["native_created_raw"] == api[pid]["created"], "Native clock field")
        require(row["native_created_utc"] == utc(api[pid]["created"]), "Native clock interpretation")
        require(row["http_status"] == 200, "Capture status")
        start = datetime.fromisoformat(row["capture_started_utc"].replace("Z", "+00:00"))
        finish = datetime.fromisoformat(row["capture_finished_utc"].replace("Z", "+00:00"))
        require(start.tzinfo is not None and finish >= start, "Capture clock ordering")
        require(start.date().isoformat() >= "2026-09-04", "Capture mistaken for June event")
    provenance = load("evidence/provenance.json")
    require(len(provenance) == 4, "Receipt-summary count")
    for p in provenance:
        row = byid[p["paste_id"]]
        for field in ("envelope_file", "capture_started_utc", "capture_finished_utc", "http_status", "envelope_sha256", "envelope_bytes"):
            require(p[field] == row[field], "Receipt-derived field mismatch: " + field)
        require(p["original_receipt_redistributed"] is False, "Receipt summary mislabeled")
        require(len(p["original_receipt_sha256"]) == 64, "Receipt hash anchor")
    with local("body-clock-provenance.csv").open(newline="", encoding="utf-8") as handle:
        csv_rows = list(csv.DictReader(handle))
    require(len(csv_rows) == 4, "CSV row count")
    for row in csv_rows:
        for k, value in row.items():
            require(value == str(byid[row["paste_id"]][k]), "CSV/JSON table disagreement: " + k)
    claims = load("evidence/claims.json")
    require(claims["issue"] == 18 and claims["status"] == "partial" and claims["closes_issue"] is False, "Partial issue scope")
    validate_native(api, claims["native_relation"])
    validate_ack(api, claims["acknowledgment"])
    require(claims["canonical_scope"]["preexisting_body_records"] == 4 and claims["canonical_scope"]["new_historical_events"] == 0, "Preexisting observation scope")
    require(claims["six_reviewed_writer_graphs"]["changes"] == 0 and claims["six_reviewed_writer_graphs"]["request_answer_edge_added"] is False, "Graph mutation claim")
    event = load("updates-event-draft.json")
    require(event["issues"] == [18] and event["publication_time"] is None, "Fabricated publication or wrong issue")
    require(event["status"] == "draft_pending_acceptance", "Draft event status")
    controls = []
    if negative_controls:
        def rejected(label, function):
            try:
                function()
            except ValueError:
                controls.append(label)
            else:
                raise ValueError("Negative control accepted: " + label)
        changed = copy.deepcopy(api)
        changed["7a45b400"]["inreply"]["url"] = api["d509c771"]["url"]
        rejected("wrong_observed_object_as_parent", lambda: validate_native(changed, claims["native_relation"]))
        bad = copy.deepcopy(claims["native_relation"])
        bad["semantic_class"] = "request_answer"
        rejected("greeting_parent_promoted_to_Q5_answer", lambda: validate_native(api, bad))
        bad_row = copy.deepcopy(byid["8246f250"])
        bad_row["decoded_body_sha256"] = bad_row["envelope_sha256"]
        rejected("envelope_hash_substituted_for_decoded_body", lambda: validate_body(api, bad_row))
        bad_ack = copy.deepcopy(claims["acknowledgment"])
        bad_ack["unique_report_object_resolved"] = True
        rejected("matching_label_promoted_to_exact_object_receipt", lambda: validate_ack(api, bad_ack))
        bad_ack2 = copy.deepcopy(claims["acknowledgment"])
        bad_ack2["independent_receipt_verified"] = True
        rejected("content_ACK_promoted_to_independent_delivery", lambda: validate_ack(api, bad_ack2))
        bad_clock = copy.deepcopy(claims["native_relation"])
        bad_clock["created_delta_seconds"] = 7323
        rejected("incorrect_parent_clock_difference", lambda: validate_native(api, bad_clock))
    return {
        "status": "PASS", "refs": [18], "scope": "partial",
        "original_envelopes_verified": 4, "original_envelope_bytes": 3844,
        "decoded_body_files_verified": 4, "declared_canonical_body_hash_matches": 4,
        "native_parent_relation": "7a45b400 -> e53f96e2", "native_parent_semantics": "structural_only",
        "parent_created_delta_seconds": 4323, "report_to_ACK_created_delta_seconds": 57,
        "exact_report_object_receipt": False, "writer_graph_edges_added": 0,
        "negative_controls_rejected": controls,
        "limitations": [
            "Canonical database and original HTTP receipts are not included; canonical ID/hash anchors and receipt-extracted capture clocks cannot be independently reauthenticated by this standalone verifier.",
            "It verifies included original API-envelope bytes, deterministic body derivations and native metadata arithmetic, not historical publication, actor identity, successful execution or message delivery."
        ]
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--negative-controls", action="store_true")
    args = parser.parse_args()
    print(json.dumps(verify(args.negative_controls), indent=2))
