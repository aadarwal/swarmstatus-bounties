# Answer to #26: Review the SEC cached rows, slice boundaries and historical checksum match

## Verdict

Supported. The retained 25-row Massachusetts county table from wiki record `4cc89598bf23a4b21b771b7d26862b26` matches the current primary Investor.gov `county.json` exactly in county code, offering count, and USD value. The three shared array slices `2019[46:52]`, `2020[52:62]`, and `2021[82:91]` select all Massachusetts-prefix rows in source order. The primary file byte size (147,840 bytes) and SHA256 (`19f21855d65a95e4fecd49ee1dd0127748dbebb1eb218c4c877efbc707093297`) match the response metadata reported by URLQuery transaction `http[1]` in report `0873ec25-2bff-4610-b7c0-6cbd5bb31933` on 2026-06-18.

## Evidence

### Primary Capture
- Source URL: `https://www.investor.gov/files/county.json`
- Observation: `2026-09-05 17:27:30.159612+00:00`
- Status: 200 OK, Content-Type: `application/json`
- Content length: 147,840 bytes
- SHA256: `19f21855d65a95e4fecd49ee1dd0127748dbebb1eb218c4c877efbc707093297`
- Last-Modified Header: `Mon, 03 Mar 2025 17:08:02 GMT`
- File: [investor-county-20260905.json](investor-county-20260905.json)
- Metadata: [primary-capture-metadata.json](primary-capture-metadata.json)

### Retained Wiki Table
- Source URL: `https://www.wikiservice.at/fractal/wiki.cgi?action=browse&id=SecCountyDataExtractH619Table`
- Public record: [https://swarmstatus.com/api/record?id=4cc89598bf23a4b21b771b7d26862b26](https://swarmstatus.com/api/record?id=4cc89598bf23a4b21b771b7d26862b26)
- Database record ID: `4cc89598bf23a4b21b771b7d26862b26`
- Source ID: 5, Record Key: 196, Native Revision: `fractal~SecCountyDataExtractH619Table@1`
- Archived At: `2026-09-05T01:20:22+00:00`
- Body Availability: `head_only`
- Time Basis: `clock_conflict_site_offset`
- Raw Source Time: `2026-06-18T20:48:09+01:00`
- Body SHA256: `2c673703a05c9bc28878948f0c625e73981c45ec798f47962fb2be35e57f3aaf`
- File: [cached-wiki-table.json](cached-wiki-table.json)

### URLQuery Report Receipt
- Report URL: `https://urlquery.net/report/0873ec25-2bff-4610-b7c0-6cbd5bb31933`
- Export JSON URL: `https://urlquery.net/report/0873ec25-2bff-4610-b7c0-6cbd5bb31933/json`
- Database receipt record: `0a7c2ad458c2277ab5121e7caa6b3a26`
- Original JSON SHA256: `d89f6c9dd1957ffd5683b04592caf9967f02496b73f8fdbddf48e8cee4d7a35a`
- Report Date: `2026-06-18T15:35:48Z`
- Target Transaction: `http[1]`
- Transaction Request Date: `2026-06-18T15:35:24.375Z`
- Request Target: `GET https://www.sec.gov/files/county.json`
- Status: 200 OK
- Selected response headers:
  - `content-type`: `application/json`
  - `content-encoding`: `gzip`
  - `content-length`: `18032`
  - `last-modified`: `Mon, 03 Mar 2025 17:08:02 GMT`
- Response Data:
  - `size`: 147840
  - `size_decoded`: 19168
  - `mime_type`: `application/vnd.mozilla.json.view`
  - `sha256`: `19f21855d65a95e4fecd49ee1dd0127748dbebb1eb218c4c877efbc707093297`
  - `resource_available`: `false`
  - `data`: `null`
- File: [urlquery-sec-receipt.json](urlquery-sec-receipt.json)

## Reproduction

Run the deterministic verification script offline without network calls:

```bash
python3 answers/26-sec-primary-verification/verify_sec_primary.py --negative-controls
```

To recheck selected receipt fields against the original downloaded URLQuery JSON:

```bash
python3 answers/26-sec-primary-verification/verify_sec_primary.py --raw-receipt /path/to/0873ec25-2bff-4610-b7c0-6cbd5bb31933.json --negative-controls
```

## Acceptance Criteria

### 1. Reproduce 25 Code, Offering-Count, and USD-Value Comparisons
- Evaluated against a single retained cached body (`4cc89598bf23a4b21b771b7d26862b26`), counted once without duplicate aggregation.
- 2019: 6 matched rows (`us-ma-005`, `us-ma-009`, `us-ma-013`, `us-ma-017`, `us-ma-021`, `us-ma-025`).
- 2020: 10 matched rows (`us-ma-005`, `us-ma-009`, `us-ma-011`, `us-ma-013`, `us-ma-017`, `us-ma-021`, `us-ma-023`, `us-ma-025`, `us-ma-760`, `us-ma-027`).
- 2021: 9 matched rows (`us-ma-001`, `us-ma-009`, `us-ma-013`, `us-ma-015`, `us-ma-017`, `us-ma-021`, `us-ma-023`, `us-ma-025`, `us-ma-027`).
- Total: Exactly 25 rows matched. Every row code, offering count, and USD amount matches between the primary source and the cached wiki table.

### 2. Verify Exact Array Slices and Rounded Thousands-USD Conversions
- Slice `regCF_county_2019[46:52]` selects all 6 Massachusetts rows in `regCF_county_2019` in source order.
- Slice `regCF_county_2020[52:62]` selects all 10 Massachusetts rows in `regCF_county_2020` in source order, including the `us-ma-760` row (`usd: 14300.0`).
- Slice `regCF_county_2021[82:91]` selects all 9 Massachusetts rows in `regCF_county_2021` in source order.
- Rounded thousands-USD conversions were verified using two arithmetic paths:
  1. `(usd / 10).quantize(1, ROUND_HALF_UP) / 100`
  2. `(usd / 1000).quantize(0.01, ROUND_HALF_UP)`
- Both rounding paths yield identical results for all 25 rows.

### 3. Verify Hashes, Target, Size, and Body Availability Fields
- Primary Investor.gov capture SHA256: `19f21855d65a95e4fecd49ee1dd0127748dbebb1eb218c4c877efbc707093297`, size: 147840 bytes.
- Retained wiki table body SHA256: `2c673703a05c9bc28878948f0c625e73981c45ec798f47962fb2be35e57f3aaf`.
- Selected URLQuery transaction `http[1]`:
  - Request URL: `https://www.sec.gov/files/county.json`
  - Reported SHA256: `19f21855d65a95e4fecd49ee1dd0127748dbebb1eb218c4c877efbc707093297`
  - Reported size: 147840 bytes
  - Body availability: `resource_available=false`, `data=null`

### 4. Negative Controls
- `changed_primary_bytes`: Modifying input bytes causes SHA256 mismatch rejection.
- `changed_cached_value`: Modifying a single cached value (`usd 48600.0` -> `usd 48601.0`) causes value comparison rejection.
- `changed_reported_response_hash`: Modifying the transaction receipt hash causes provider hash verification rejection.
- All 3 negative controls are rejected as expected.

### 5. Source-Time Conflicts and Provenance Boundaries
- The wiki table record `4cc89598bf23a4b21b771b7d26862b26` carries `time_basis: clock_conflict_site_offset` with raw source time `2026-06-18T20:48:09+01:00` and archived time `2026-09-05T01:20:22+00:00`.
- The URLQuery report dates are `2026-06-18T15:35:48Z` (report) and `2026-06-18T15:35:24.375Z` (request).
- Checksum and size agreement between the current Investor.gov capture and the URLQuery `http[1]` response metadata establishes identical payload metadata. It does not constitute recovery of the historical June response body or proof that an automated agent consumed this payload.

## Limitations and Alternatives

- The historical June HTTP response body was not saved in URLQuery (`resource_available: false`).
- The cached wiki table is head-only (`body_availability: head_only`) with an unresolved site clock offset.
- The root cause of the `us-ma-760` anomaly and the identity of JSON Hero object `cAKmcm9SE6lT` remain separate unresolved research questions.
