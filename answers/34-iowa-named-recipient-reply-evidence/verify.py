#!/usr/bin/env python3
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def load(name):
    with (ROOT / name).open(encoding="utf-8") as fh:
        return json.load(fh)


def main():
    claims = load("evidence/claims.json")
    sources = load("evidence/sources.json")
    result = load("verification-result.json")

    assert claims["status"] == "partial"
    assert claims["closes_issue"] is False
    assert claims["join_matrix"]["provider_stored_parent_reply"] is False
    assert claims["join_matrix"]["explicit_source_link_to_exact_request"] is False
    assert claims["join_matrix"]["independent_read_acknowledgement"] is False
    assert claims["join_matrix"]["named_recipient"] is True
    assert claims["join_matrix"]["cache_citation"] is True
    assert claims["join_matrix"]["q5_wording_claim"] is True

    assert sources["cache"]["id"] == "eb7e28bd"
    assert sources["cache"]["exact_request_object_retained"] is False

    expected = {
        "IowaReply0227": (
            "https://paste.linuxiarz.pl/view/11d30c3f",
            "570051f593cd4ebd1e572cd77e44fb46634bccd48d19ceb5722050cf276230cb",
            "25194b724b3fc7ea94dc26bbf0fb0bba",
        ),
        "IowaCacheReply": (
            "https://paste.linuxiarz.pl/view/1ad7edc4",
            "33c42767e95a708a78c3c02380d8e1142fdc86d236d824292e91d9d78ab8d81b",
            "bffc285e8e4b206ae385c314525320c9",
        ),
        "ThanksPostQ5": (
            "https://paste.linuxiarz.pl/view/28c3155e",
            "06215ba7ebf9a6ef4020a38e0d41288dd8acba35e9a4f8c0d7ad8950cf65a50d",
            "073",
        ),
    }
    by_id = {item["id"]: item for item in sources["sources"]}
    assert set(by_id) == set(expected)
    for source_id, (url, digest, record) in expected.items():
        item = by_id[source_id]
        assert item["url"] == url
        assert item["sha256"] == digest
        assert re.fullmatch(r"[0-9a-f]{64}", item["sha256"])
        assert item["retained_record"] == record
        assert item["time_raw"] == "2 Months ago."
        assert item["time_basis"] == "relative_age"

    assert claims["replies"][0]["record"] == "25194b724b3fc7ea94dc26bbf0fb0bba"
    assert claims["replies"][1]["record"] == "bffc285e8e4b206ae385c314525320c9"
    assert claims["acknowledgement_candidate"]["record_prefix"] == "073"
    assert claims["acknowledgement_candidate"]["proof_of_read"] is False
    assert result["result"] == "PASS"
    print("PASS: Iowa named-recipient reply evidence is internally consistent")
    return 0


if __name__ == "__main__":
    sys.exit(main())
