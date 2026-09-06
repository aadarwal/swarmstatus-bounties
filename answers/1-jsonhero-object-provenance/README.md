# Evidence Artifacts: JSON Hero Object cAKmcm9SE6lT Provenance

This directory contains the preserved evidence artifacts, code models, and offline verification suite resolving **Issue #1: Recover historical source and contents of JSON Hero cAKmcm9SE6lT**.

## File Inventory

| File | Bytes | SHA-256 | Description |
| :--- | :--- | :--- | :--- |
| `investor-county-20260905.json` | 147,840 | `19f21855d65a95e4fecd49ee1dd0127748dbebb1eb218c4c877efbc707093297` | Primary SEC/Investor.gov Regulation Crowdfunding county dataset containing root keys `regCF_county_2019`, `regCF_county_2020`, `regCF_county_2021`. |
| `retained-records.json` | 96,219 | `6443e12ac8d5af3eb32cda2037bd890117251d27195acbef987ab1b7b0d01416` | Retained records from Swarmstatus indexing `cAKmcm9SE6lT` across shortener burst sequence `massjh86420data23`–`data28` and corroborating peer proxy records. |
| `jsonhero-code-extract.ts` | 4,338 | `13bc875514790000ef4ce4f129c97d323b1fe8313f5f0f1c930e4f873b3ddfb3` | Implementation extracts from `triggerdotdev/jsonhero-web` commit `15157053174ba7a0a79c77b2925fbde7e05a6334` defining `UrlJsonDocument` vs `RawJsonDocument` and title generation. |
| `verify_jsonhero_provenance.py` | 12,351 | `5ee408dd3082a9c9e550209fa2292196bed0c784afcd1e73612dab6adfab28cb` | Self-contained Python verification script with negative controls. |
| `verification-result.json` | 2,784 | `2b51725a55863df740e413bdf239767be62f6fff580323a186e0800aab4edad4` | Machine-readable verification output log. |
| `manifest.json` | - | - | Cryptographic manifest of files in this directory. |

## Reproduction

Run the standalone verification suite:

```bash
python3 answers/1-jsonhero-object-provenance/verify_jsonhero_provenance.py --negative-controls --json-out answers/1-jsonhero-object-provenance/verification-result.json
```
