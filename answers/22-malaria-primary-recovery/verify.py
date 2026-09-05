"""Offline verification of the partial malaria source recovery. No network calls."""
import argparse
import base64
import gzip
import hashlib
import json
import pathlib
import re

CHART_ID = "d88e6864f43c426dbcd1ee675a8944a7"
ARTICLE_URL = "https://www.dataforindia.com/malaria-in-india/"
EXPECTED_YEARS = ["2005", "2008", "2012", "2015", "2016", "2017", "2018", "2019", "2020", "2021", "2022"]
EXPECTED_CODES = ["dfi_6_deaths", "dfi_8_de04", "dfi_15_de514", "dfi_10_de1529", "dfi_12_de3044", "dfi_14_de4554", "dfi_16_de5569", "dfi_17_deat70"]


def require(value, message):
    if not value:
        raise ValueError(message)


def digest1(value):
    return base64.b32encode(hashlib.sha1(value).digest()).decode().rstrip("=")


def header(block, key):
    match = re.search(rb"(?im)^" + key.encode() + rb":\s*([^\r\n]+)", block)
    require(match is not None, "Missing header " + key)
    return match[1].decode()


def verify_archive(compressed, provenance, chart_id=CHART_ID):
    require(hashlib.sha256(compressed).hexdigest() == provenance["compressed_sha256"], "Compressed WARC SHA256 mismatch")
    raw = gzip.decompress(compressed)
    require(hashlib.sha256(raw).hexdigest() == provenance["warc_sha256"], "Decompressed WARC SHA256 mismatch")
    warc_headers, remainder = raw.split(b"\r\n\r\n", 1)
    block = remainder[:int(header(warc_headers, "Content-Length"))]
    http_headers, payload = block.split(b"\r\n\r\n", 1)
    require(header(warc_headers, "WARC-Target-URI") == ARTICLE_URL, "WARC target mismatch")
    require(header(warc_headers, "WARC-Date") == "2026-06-13T11:59:01Z", "Archive capture date mismatch")
    require(http_headers.startswith(b"HTTP/1.1 200"), "Archived HTTP status is not 200")
    require(len(payload) == int(header(http_headers, "Content-Length")), "HTTP payload length mismatch")
    require(digest1(payload) == header(warc_headers, "WARC-Payload-Digest").removeprefix("sha1:") == provenance["index_record"]["digest"], "Payload SHA1/index digest mismatch")
    require(digest1(block) == header(warc_headers, "WARC-Block-Digest").removeprefix("sha1:"), "WARC block SHA1 mismatch")
    require(hashlib.sha256(payload).hexdigest() == provenance["html_sha256"], "Payload SHA256 mismatch")
    pattern = rb'<iframe\b[^>]*src="https://charts\.dataforindia\.com/charts/' + chart_id.encode() + rb'"[^>]*></iframe>'
    frames = re.findall(pattern, payload)
    require(len(frames) == 1, "Expected exact chart iframe ID once in historical article")
    return payload, frames[0]


def verify_semantics(config, data, chart_id=CHART_ID):
    require(config["code"] == chart_id, "Configuration chart identifier mismatch")
    require(config["chart"]["yAxis"]["unit"] == "%", "Chart unit must be percentage")
    require(config["query"]["args"]["filter"]["expression"] == '`dfi_4_location`=="India" and `dfi_5_caofde`=="Malaria"', "Geography/cause filter mismatch")
    require(config["query"]["args"]["target"] == "projects/dfi_11_srs/datasets/dfi_1_caofde/tables/dfi_6_caofdev5", "Dataset/table target mismatch")
    require(data["data"]["dfi_2_year"] == EXPECTED_YEARS and data["num_rows"] == 11, "Year list or row count mismatch")
    require(config["chart"]["indicators"] == EXPECTED_CODES, "Age series order mismatch")
    require(config["chart"]["yAxis"]["selected"] == ["dfi_6_deaths", "dfi_15_de514"], "Default series selection mismatch")
    require(set(data["data"]) == {"dfi_2_year", *EXPECTED_CODES}, "Unexpected data fields")
    require(all(len(data["data"][code]) == 11 for code in EXPECTED_CODES), "Unaligned age series")
    require(all(type(v) in (int, float) and 0 <= v <= 100 for code in EXPECTED_CODES for v in data["data"][code]), "Invalid percentage values")
    require(data["labels"]["dfi_6_deaths"] == "Sum Deaths", "Generic data label changed")
    require(config["chart"]["yAxis"]["info"]["dfi_15_de514"]["label"] == "5-14 years", "Age label mismatch")
    return {"years": EXPECTED_YEARS, "age_series": len(EXPECTED_CODES), "numeric_cells": 88, "unit": "%", "geography": "India", "cause": "Malaria", "generic_data_label": data["labels"]["dfi_6_deaths"], "historical_numeric_values_proven": False}


def rejected(name, operation):
    try:
        operation()
    except (ValueError, AssertionError) as error:
        return {"name": name, "rejected": True, "reason": str(error)}
    raise ValueError("Negative control was incorrectly accepted: " + name)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--negative-controls", action="store_true")
    args = parser.parse_args()
    root = pathlib.Path(__file__).resolve().parent
    manifest = json.loads((root / "manifest.json").read_text())
    for name, expected in manifest.items():
        content = (root / name).read_bytes()
        require(len(content) == expected["bytes"], "File size mismatch: " + name)
        require(hashlib.sha256(content).hexdigest() == expected["sha256"], "File hash mismatch: " + name)
    evidence = root / "evidence"
    compressed = (evidence / "article-20260613.warc.gz").read_bytes()
    provenance = json.loads((evidence / "warc-provenance.json").read_text())
    _, frame = verify_archive(compressed, provenance)
    require((evidence / "literal-iframe-extract.html").read_bytes() == frame + b"\n", "Literal iframe extract mismatch")
    config = json.loads((evidence / "config-20260905.json").read_text())
    data = json.loads((evidence / "data-20260905.json").read_text())
    semantics = verify_semantics(config, data)
    captures = json.loads((evidence / "primary-captures.json").read_text())
    for capture in captures:
        leaf = "data.json" if capture["id"] == "malaria-data" else "config.json"
        require(capture["url"] == "https://assets.dataforindia.com/charts/" + CHART_ID + "/" + leaf, "Primary source URL mismatch")
        require(hashlib.sha256((root / capture["path"]).read_bytes()).hexdigest() == capture["sha256"], "Primary capture hash mismatch")
        require(capture["status"] == 200, "Primary capture unsuccessful")
    aliases = json.loads((evidence / "retained-aliases.json").read_text())
    require(len(aliases) == 4 and len({row["record_id"] for row in aliases}) == 4, "Alias source record count mismatch")
    require(all(CHART_ID in row["raw_targets"][0] and row["time_basis"] == "raw_unzoned" for row in aliases), "Alias object/clock basis mismatch")
    report = {"status": "PASS", "manifest_files_verified": len(manifest), "archive_date": "2026-06-13T11:59:01Z", "historical_publisher_citation_verified": True, "current_semantics": semantics, "historical_data_or_config_recovered": False, "new_task_staging_verified": False, "issue": 22, "submission": "Advances #22; does not close it"}
    if args.negative_controls:
        wrong_id = CHART_ID[:-1] + "8"
        corrupted = bytes([compressed[0] ^ 1]) + compressed[1:]
        wrong_unit = json.loads(json.dumps(config))
        wrong_unit["chart"]["yAxis"]["unit"] = "deaths"
        report["negative_controls"] = [rejected("altered archive chart ID", lambda: verify_archive(compressed, provenance, wrong_id)), rejected("altered config chart ID", lambda: verify_semantics(config, data, wrong_id)), rejected("altered compressed WARC byte/hash", lambda: verify_archive(corrupted, provenance)), rejected("treat generic Sum Deaths as count unit", lambda: verify_semantics(wrong_unit, data))]
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
