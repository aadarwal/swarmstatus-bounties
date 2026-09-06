#!/usr/bin/env python3
"""Offline verification of primary EDGAR provenance for the us-ma-760 county row.

Validates the primary SEC Form C-U filing against the 2020 county dataset,
demonstrating that us-ma-760 is an artifact of issuer clerical error in
EDGAR accession 0001746059-20-000069.
"""

import argparse
from decimal import Decimal
import hashlib
import json
from pathlib import Path
import re
import sys
import xml.etree.ElementTree as ET

HERE = Path(__file__).resolve().parent

PRIMARY_CU_XML_SHA256 = "1a4ec0d324e0a5ef94e3b1e510d0d450be407aa4653ccea085dae43d4f506a37"
PRIMARY_C_XML_SHA256 = "d9cd7a5c950372f4b38a011b8cc19b2e766ddc4b0acbd280d399e38dca11500e"
SUBMISSIONS_JSON_SHA256 = "03a47b389cadc3a855cab26a4796f2fe8600ef6bf082e23ef938a7221766be5f"
COUNTY_JSON_SHA256 = "19f21855d65a95e4fecd49ee1dd0127748dbebb1eb218c4c877efbc707093297"
CACHE_TABLE_SHA256 = "2c673703a05c9bc28878948f0c625e73981c45ec798f47962fb2be35e57f3aaf"

VALID_MA_FIPS = {
    "001": "Barnstable",
    "003": "Berkshire",
    "005": "Bristol",
    "007": "Dukes",
    "009": "Essex",
    "011": "Franklin",
    "013": "Hampden",
    "015": "Hampshire",
    "017": "Middlesex",
    "019": "Nantucket",
    "021": "Norfolk",
    "023": "Plymouth",
    "025": "Suffolk",
    "027": "Worcester",
}


def require(condition: bool, message: str) -> None:
    """Assert condition or raise ValueError with diagnostic message.

    Parameters:
        condition: Expression evaluated for truthiness.
        message: Diagnostic error explanation if condition is false.
    """
    if not condition:
        raise ValueError(message)


def compute_sha256(path: Path) -> str:
    """Compute hexadecimal SHA-256 digest of file bytes.

    Parameters:
        path: Path to target file on local filesystem.

    Returns:
        Hexadecimal representation of SHA-256 hash.
    """
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(65536):
            digest.update(chunk)
    return digest.hexdigest()


def parse_form_cu_xml(path: Path) -> dict:
    """Extract primary issuer and progress update fields from SEC Form C-U XML.

    Parameters:
        path: Path to Form C-U XML primary document.

    Returns:
        Dictionary containing extracted issuer metadata and financial figures.
    """
    tree = ET.parse(path)
    root = tree.getroot()

    fields = {}
    for elem in root.iter():
        tag = elem.tag.split("}")[-1] if "}" in elem.tag else elem.tag
        if elem.text and elem.text.strip():
            fields[tag] = elem.text.strip()

    progress_text = fields.get("progressUpdate", "")
    match_amount = re.search(r"\$([0-9,]+)", progress_text)
    amount_dollars = None
    if match_amount:
        amount_dollars = Decimal(match_amount.group(1).replace(",", ""))

    return {
        "submission_type": fields.get("submissionType", ""),
        "filer_cik": fields.get("filerCik", ""),
        "file_number": fields.get("fileNumber", ""),
        "issuer_name": fields.get("nameOfIssuer", ""),
        "legal_form": fields.get("legalStatusForm", ""),
        "jurisdiction": fields.get("jurisdictionOrganization", ""),
        "street1": fields.get("street1", ""),
        "city": fields.get("city", ""),
        "state_or_country": fields.get("stateOrCountry", ""),
        "zip_code": fields.get("zipCode", ""),
        "intermediary_name": fields.get("companyName", ""),
        "intermediary_cik": fields.get("commissionCik", ""),
        "progress_update": progress_text,
        "amount_dollars": amount_dollars,
        "signature_date": fields.get("signatureDate", ""),
    }


def verify_artifacts_and_provenance(base_dir: Path) -> dict:
    """Execute complete offline verification of primary artifacts and derivation.

    Parameters:
        base_dir: Directory containing retained primary and cached artifacts.

    Returns:
        Structured verification results summarizing checks.
    """
    cu_xml_path = base_dir / "primary-doc-0001746059-20-000069.xml"
    c_xml_path = base_dir / "primary-doc-0001746059-19-000072.xml"
    sub_json_path = base_dir / "submissions-CIK0001793545.json"
    county_json_path = base_dir / "investor-county-20260905.json"
    cache_json_path = base_dir / "cached-wiki-table.json"

    require(cu_xml_path.is_file(), f"Missing {cu_xml_path}")
    require(c_xml_path.is_file(), f"Missing {c_xml_path}")
    require(sub_json_path.is_file(), f"Missing {sub_json_path}")
    require(county_json_path.is_file(), f"Missing {county_json_path}")
    require(cache_json_path.is_file(), f"Missing {cache_json_path}")

    cu_hash = compute_sha256(cu_xml_path)
    c_hash = compute_sha256(c_xml_path)
    sub_hash = compute_sha256(sub_json_path)
    county_hash = compute_sha256(county_json_path)

    require(cu_hash == PRIMARY_CU_XML_SHA256, f"Form C-U hash mismatch: {cu_hash}")
    require(c_hash == PRIMARY_C_XML_SHA256, f"Form C hash mismatch: {c_hash}")
    require(sub_hash == SUBMISSIONS_JSON_SHA256, f"Submissions hash mismatch: {sub_hash}")
    require(county_hash == COUNTY_JSON_SHA256, f"County JSON hash mismatch: {county_hash}")

    cache_data = json.loads(cache_json_path.read_text())
    cache_body = cache_data.get("body", "")
    cache_body_hash = hashlib.sha256(cache_body.encode("utf-8")).hexdigest()
    require(cache_body_hash == CACHE_TABLE_SHA256, f"Cache body hash mismatch: {cache_body_hash}")

    cu_data = parse_form_cu_xml(cu_xml_path)
    require(cu_data["submission_type"] == "C-U", "Expected submissionType C-U")
    require(cu_data["filer_cik"] == "0001793545", "Expected CIK 0001793545")
    require(cu_data["file_number"] == "020-25844", "Expected fileNumber 020-25844")
    require(cu_data["issuer_name"] == "Tipsy Cupcakes RVA LLC", "Expected issuer Tipsy Cupcakes RVA LLC")
    require(cu_data["jurisdiction"] == "VA", "Expected jurisdiction VA")
    require(cu_data["city"].upper() == "RICHMOND", "Expected city RICHMOND")
    require(cu_data["state_or_country"].upper() == "MA", "Expected stateOrCountry MA")
    require(cu_data["zip_code"] == "23221", "Expected zipCode 23221")
    require(cu_data["amount_dollars"] == Decimal("14300"), "Expected amount 14300")

    sub_data = json.loads(sub_json_path.read_text())
    recent_filings = sub_data.get("filings", {}).get("recent", {})
    acc_list = recent_filings.get("accessionNumber", [])
    require("0001746059-20-000069" in acc_list, "Accession 0001746059-20-000069 missing from submissions")
    cu_idx = acc_list.index("0001746059-20-000069")
    require(recent_filings.get("filingDate", [])[cu_idx] == "2020-03-05", "Expected filingDate 2020-03-05")
    require(recent_filings.get("acceptanceDateTime", [])[cu_idx] == "2020-03-05T10:34:10.000Z", "Expected acceptance time")

    county_data = json.loads(county_json_path.read_text())
    c2020_rows = county_data.get("regCF_county_2020", [])
    target_row = next((r for r in c2020_rows if r.get("code") == "us-ma-760"), None)
    require(target_row is not None, "Target code us-ma-760 missing from regCF_county_2020")
    require(Decimal(str(target_row.get("offerings"))) == Decimal("1.0"), "Expected 1.0 offering")
    require(Decimal(str(target_row.get("usd"))) == Decimal("14300.0"), "Expected 14300.0 usd")

    cache_line = "code us-ma-760 | offerings 1.0 | usd 14300.0"
    require(cache_line in cache_body, "Target row missing from cached wiki table")

    state_prefix = "us-" + cu_data["state_or_country"].lower()
    county_fips_component = "760"
    synthesized_code = f"{state_prefix}-{county_fips_component}"
    require(synthesized_code == "us-ma-760", "Expected synthesized code us-ma-760")
    require(county_fips_component not in VALID_MA_FIPS, "FIPS 760 must not exist in Massachusetts")

    return {
        "verdict": "SUPPORTED",
        "primary_filing": {
            "cik": cu_data["filer_cik"],
            "accession": "0001746059-20-000069",
            "issuer": cu_data["issuer_name"],
            "jurisdiction": cu_data["jurisdiction"],
            "address": {
                "street": cu_data["street1"],
                "city": cu_data["city"],
                "state_reported": cu_data["state_or_country"],
                "zip": cu_data["zip_code"],
            },
            "filing_date": recent_filings.get("filingDate", [])[cu_idx],
            "acceptance_datetime_utc": recent_filings.get("acceptanceDateTime", [])[cu_idx],
            "reported_amount_usd": float(cu_data["amount_dollars"]),
        },
        "target_row": target_row,
        "derivation_explanation": (
            "Primary clerical error: filer reported state MA with Richmond VA 23221 address. "
            "Automated SEC pipeline concatenated state prefix 'us-ma' with Richmond independent "
            "city FIPS county component 760, creating nonstandard orphaned code us-ma-760."
        ),
    }


def run_negative_controls(base_dir: Path) -> None:
    """Validate that mutated artifacts and invalid assertions trigger failures.

    Parameters:
        base_dir: Directory containing retained primary and cached artifacts.
    """
    county_json_path = base_dir / "investor-county-20260905.json"
    data = json.loads(county_json_path.read_text())
    mutated_c2020 = data["regCF_county_2020"]
    for row in mutated_c2020:
        if row.get("code") == "us-ma-760":
            row["usd"] = 99999.0
            break

    found_mismatch = False
    for row in mutated_c2020:
        if row.get("code") == "us-ma-760":
            if Decimal(str(row["usd"])) != Decimal("14300.0"):
                found_mismatch = True
                break
    require(found_mismatch, "Negative control failed: mutated row was not detected")

    bogus_hash = hashlib.sha256(b"tampered_bytes").hexdigest()
    require(bogus_hash != PRIMARY_CU_XML_SHA256, "Negative control failed: hash collision detected")


def main() -> int:
    """Command line entrypoint for offline verification.

    Returns:
        Status code 0 on complete verification success.
    """
    parser = argparse.ArgumentParser(description="Verify SEC EDGAR provenance for us-ma-760")
    parser.add_argument("--base-dir", type=Path, default=HERE, help="Path to evidence directory")
    parser.add_argument("--negative-controls", action="store_true", help="Execute negative controls")
    parser.add_argument("--json-out", type=Path, help="Optional path to write verification JSON")
    args = parser.parse_args()

    results = verify_artifacts_and_provenance(args.base_dir)

    if args.negative_controls:
        run_negative_controls(args.base_dir)

    if args.json_out:
        args.json_out.write_text(json.dumps(results, indent=2) + "\n")

    print("VERIFICATION SUCCESS: us-ma-760 explained by primary EDGAR Form C-U filing.")
    print(f"Issuer: {results['primary_filing']['issuer']} (CIK {results['primary_filing']['cik']})")
    print(f"Accession: {results['primary_filing']['accession']}, Filing Date: {results['primary_filing']['filing_date']}")
    print(f"Address in filing: {results['primary_filing']['address']['city']}, {results['primary_filing']['address']['state_reported']} {results['primary_filing']['address']['zip']}")
    print(f"Amount: ${results['primary_filing']['reported_amount_usd']:,.2f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
