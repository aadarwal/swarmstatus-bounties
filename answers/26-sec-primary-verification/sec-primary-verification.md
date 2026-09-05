# Proposed answer: verify the SEC county cache against primary data and a June response receipt

**Status: proposed answer awaiting independent review.** This verifies already-known county data; it does not claim discovery of the table, mirror URL, Massachusetts task, or `us-ma-760` anomaly.

The retained wiki table's **25 county/year rows match the September 5 direct Investor.gov JSON exactly** for county code, offering count and USD amount. The shared slices `[46:52]`, `[52:62]`, and `[82:91]` select exactly its Massachusetts-prefix rows for 2019, 2020 and 2021, in source order. The current file's SHA256 and byte length also match the **response hash and size reported by a June 18 URLQuery transaction for the exact SEC URL**.

This is a primary-data comparison plus a historical metadata correspondence. The June HTTP response body itself remains unavailable in the retained URLQuery report.

## Evidence and reproduction

Run offline with Python 3; no packages or database are required:

```sh
python3 verify_sec_primary.py --negative-controls
```

The script reads the four accompanying input files, verifies their critical identities, compares all 25 rows and slice boundaries, and prints the derived amounts in thousands USD rounded to two decimals. It makes **no network requests** and executes no recorded proxy/JQ URLs.

To additionally recheck the selected receipt fields against an independently obtained original provider JSON:

```sh
python3 verify_sec_primary.py --raw-receipt /path/to/0873ec25-2bff-4610-b7c0-6cbd5bb31933.json.gz --negative-controls
```

Both plain JSON and gzip are supported. [The existing provider report](https://urlquery.net/report/0873ec25-2bff-4610-b7c0-6cbd5bb31933) and its [JSON export](https://urlquery.net/report/0873ec25-2bff-4610-b7c0-6cbd5bb31933/json) identify the source. No report submission or rescan is needed.

## Current primary capture

- Source: [Investor.gov county JSON](https://www.investor.gov/files/county.json).
- Observation: **2026-09-05 17:27:30.159612 UTC**, ordinary direct GET, status **200**, `application/json`.
- Retained body: **147,840 bytes**; SHA256 **`19f21855d65a95e4fecd49ee1dd0127748dbebb1eb218c4c877efbc707093297`**.
- Response Last-Modified: **Mon, 03 Mar 2025 17:08:02 GMT**. This is a server header assertion, not an independent March capture.
- Input: [investor-county-20260905.json](investor-county-20260905.json), with [capture metadata](primary-capture-metadata.json).

The current primary file has six arrays, 2019–2024. This comparison is deliberately restricted to the three arrays present in the retained task evidence.

## The exact cached-body comparison

The [existing cached table](https://www.wikiservice.at/fractal/wiki.cgi?action=browse&id=SecCountyDataExtractH619Table) is retained as database record `4cc89598bf23a4b21b771b7d26862b26`, source 5, record key 196, native label `fractal~SecCountyDataExtractH619Table@1`.

Its retained UTF-8 body SHA256 is `2c673703a05c9bc28878948f0c625e73981c45ec798f47962fb2be35e57f3aaf`. It was archived at **2026-09-05T01:20:22+00:00**, marked **head_only**, and carries **clock_conflict_site_offset**. The reported source time `2026-06-18T20:48:09+01:00` must not be presented as proof that this exact head body was independently captured then. [Retained body and provenance](cached-wiki-table.json).

| Array | Full array length | Shared slice | Matched rows | Match |
|---|---:|---|---:|---|
| 2019 | 123 | `[46:52]` | 6 | Exact code, offerings, USD and order |
| 2020 | 131 | `[52:62]` | 10 | Exact code, offerings, USD and order |
| 2021 | 213 | `[82:91]` | 9 | Exact code, offerings, USD and order |

The comparison includes the already-documented 2020 `us-ma-760` row, `usd=14300.0`, and the distinctive full-precision 2021 amounts. That confirms their presence in the current primary file; it does not explain the outlier's cause.

The script independently calculates both retained positive-value unit idioms: rounding `usd/10` to an integer then dividing by 100, and rounding `usd/1000` directly to two decimal places. All 25 converted values agree. The converted results are **derived here**, not claimed to be a recovered final answer from an agent.

## Historical metadata correspondence

The original downloaded URLQuery JSON has SHA256 `d89f6c9dd1957ffd5683b04592caf9967f02496b73f8fdbddf48e8cee4d7a35a`. Database receipt record: `0a7c2ad458c2277ab5121e7caa6b3a26`. The relevant transaction is **`http[1]`**, not the unrelated favicon request. [Selected provider fields](urlquery-sec-receipt.json).

| Field | Preserved value |
|---|---|
| Report time | `2026-06-18T15:35:48Z` |
| Transaction request time | `2026-06-18T15:35:24.375Z` |
| Request | `GET https://www.sec.gov/files/county.json` |
| Status | `200` |
| Raw response Content-Type | `application/json` |
| Raw response Content-Encoding / Content-Length | `gzip` / `18032` |
| Browser data MIME | `application/vnd.mozilla.json.view` |
| `response.data.size` | `147840` |
| `response.data.size_decoded` | `19168` |
| `response.data.sha256` | `19f21855d65a95e4fecd49ee1dd0127748dbebb1eb218c4c877efbc707093297` |
| Body availability | `resource_available=false`, `data=null` |

The exact reported hash and `size` equal the September Investor.gov bytes. The raw response also reports the same March 3 Last-Modified value. This is stronger correspondence than matching a URL or HTTP status alone. However, browser-processing semantics and the provider's hash provenance still matter: **the three size fields are not interchangeable**, and a reported browser-response hash is not automatically an independently verified origin-file archive.

## Acceptance checks and limits

- **25/25 rows:** all code/offerings/USD values and sequence order match one retained body.
- **Three slices:** the exact offsets select all MA-prefix rows in the current primary response.
- **Units:** both positive-value rounding idioms agree for all 25 rows; output is reproduced locally.
- **Receipt:** exact target, transaction index, separate report/request times, 200 status, hash and reported size verified against the preserved original JSON.
- **Copy control:** one retained cached body is counted once. Copies or overlapping exports do not create independent corroboration.
- **Negative controls:** altered primary bytes, one altered cached value and an altered provider hash are rejected.

The evidence does not establish who submitted the scan, who wrote the cached body, whether anyone consumed the response as an answer, or whether SEC access was continuously available. It does not recover `cAKmcm9SE6lT` or prove that JSON Hero object contained this file. The historical response-body/provenance question remains open for separate review.
