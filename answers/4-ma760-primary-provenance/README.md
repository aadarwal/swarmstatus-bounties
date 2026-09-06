# Primary Provenance Evidence Package: us-ma-760

This package provides offline, reproducible verification that code `us-ma-760` in the 2020 SEC Regulation Crowdfunding county dataset is explained by primary SEC EDGAR filing `0001746059-20-000069`.

For the complete answer narrative and acceptance criteria review, see [answers/4-ma760-primary-provenance.md](../4-ma760-primary-provenance.md).

## Contents

- `primary-doc-0001746059-20-000069.xml`: Raw Form C-U XML progress update filed March 5, 2020 by Tipsy Cupcakes RVA LLC reporting $14,300 closed on the offering.
- `primary-doc-0001746059-19-000072.xml`: Raw Form C XML initial offering document filed November 13, 2019.
- `submissions-CIK0001793545.json`: SEC EDGAR submission index for CIK 0001793545 documenting filing dates and acceptance timestamps.
- `investor-county-20260905.json`: Retained primary copy of `https://www.investor.gov/files/county.json` containing row `regCF_county_2020[60]`.
- `cached-wiki-table.json`: Retained wiki extract matching row `code us-ma-760 | offerings 1.0 | usd 14300.0` (record `4cc89598`).
- `manifest.json`: Artifact file catalog with byte counts and SHA-256 digests.
- `verify_ma760_provenance.py`: Standard-library offline verification script with negative controls.
- `verification-result.json`: Verification result emitted by `verify_ma760_provenance.py`.

## Offline Verification

Run the verification script from the repository root:

```bash
python3 answers/4-ma760-primary-provenance/verify_ma760_provenance.py --negative-controls --json-out answers/4-ma760-primary-provenance/verification-result.json
```
