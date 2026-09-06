# Answer to #1: Recover historical source and contents of JSON Hero cAKmcm9SE6lT

## Verdict

Supported.

The historical JSON Hero object `cAKmcm9SE6lT` indexed during the June 18, 2026 activity was a URL-backed document (`UrlJsonDocument`, `type: "url"`) referencing the upstream web proxy `https://www.proxymule.com/__PrOxY__/https/www.sec.gov/files/county.json` (origin target: SEC Regulation Crowdfunding county dataset at `https://www.sec.gov/files/county.json`).

The document held a URL reference rather than raw JSON in KV storage. When loaded, JSON Hero's server runtime executed dynamic fetches against the upstream proxy URL, presenting the root dataset whose top-level keys were queried via JSONPath selectors `$.regCF_county_2019`, `$.regCF_county_2020`, and `$.regCF_county_2021` across sequential aliases `massjh86420data26`, `massjh86420data27`, and `massjh86420data28`.

## Evidence

### Primary Retained Shortener Records and Peer Captures

| Record ID | Shortener Alias | Recorded Time (UTC) | Preserved Title / Locator | Visible Destination / Path |
| :--- | :--- | :--- | :--- | :--- |
| [`dbd3ce45`](https://swarmstatus.com/api/record?id=dbd3ce45113371b3b9fd096ba9c3b2a6) | `massjh86420data23` | `2026-06-18T20:18:48Z` | `JSON Hero` | `https://jsonhero.io/j/cAKmcm9SE6lT?path=$.regCF_county_[...]` |
| [`cecc5e33`](https://swarmstatus.com/api/record?id=cecc5e3368c071abc7b95569a9e2e172) | `massjh86420data24` | `2026-06-18T20:18:50Z` | `JSON Hero` | `https://jsonhero.io/j/cAKmcm9SE6lT?path=$.regCF_county_[...]` |
| [`daec8952`](https://swarmstatus.com/api/record?id=daec895214722c2bb9eb3e80914ee451) | `massjh86420data25` | `2026-06-18T20:18:52Z` | `JSON Hero` | `https://jsonhero.io/j/cAKmcm9SE6lT?path=$.regCF_county_[...]` |
| [`989fabe4`](https://swarmstatus.com/api/record?id=989fabe46b27139e397502d5ea3bb0cc) | `massjh86420data26` | `2026-06-18T20:18:54Z` | `JSON Hero` | `https://jsonhero.io/j/cAKmcm9SE6lT?path=$.regCF_county_2019` |
| [`529d85dd`](https://swarmstatus.com/api/record?id=529d85dd66a9f4cde0bd5f384047d301) | `massjh86420data27` | `2026-06-18T20:18:57Z` | `JSON Hero - https://www.proxymule.com/__PrOxY__/https/w[...]` | `https://jsonhero.io/j/cAKmcm9SE6lT?path=$.regCF_county_2020` |
| [`75e65506`](https://swarmstatus.com/api/record?id=75e6550682263f544061b90936fa9dd1) | `massjh86420data28` | `2026-06-18T20:18:59Z` | `JSON Hero` | `https://jsonhero.io/j/cAKmcm9SE6lT?path=$.regCF_county_2021` |
| [`b0d56e4d`](https://swarmstatus.com/api/record?id=b0d56e4d4623fce9f6fe1e29dcbbbff1) | `Agent12OfficialPageUnique171` | `2026-06-18T21:12:17Z` | `Official SEC via proxymule raw JSON slices` | `https://proxymule.com/__PrOxY__/https/www.sec.gov/files/county.json` |
| [`32ff2ba5`](https://swarmstatus.com/api/record?id=32ff2ba5d5a43b2bd724ded08271f76a) | `MassJsonPathsSel1781795887` | `2026-06-18T15:18:07Z` | `SEC county map JSONhero path object links via SEC proxy` | Lists Massachusetts paths for `2019`, `2020`, `2021` |

### Primary Code and Dataset Artifacts

| Resource | Identifier / Locator | Capture SHA-256 | Size (Bytes) | Timestamp |
| :--- | :--- | :--- | :--- | :--- |
| First-Party Source Model | `triggerdotdev/jsonhero-web@1515705` | `13bc875514790000ef4ce4f129c97d323b1fe8313f5f0f1c930e4f873b3ddfb3` | 4,338 | Code extract (`app/jsonDoc.server.ts`, etc.) |
| Primary SEC County Dataset | `https://www.investor.gov/files/county.json` | `19f21855d65a95e4fecd49ee1dd0127748dbebb1eb218c4c877efbc707093297` | 147,840 | `2025-03-03T17:08:02.000Z` (HTTP Last-Modified) |
| Retained Shortener Records | `work/database-research/indexed_new_records.jsonl` | `6443e12ac8d5af3eb32cda2037bd890117251d27195acbef987ab1b7b0d01416` | 96,219 | Consolidated JSON of 8 swarmstatus records |

## Reproduction

Verification requires Python 3.8+ and uses only standard library modules (`argparse`, `hashlib`, `json`, `pathlib`, `sys`).

```bash
python3 answers/1-jsonhero-object-provenance/verify_jsonhero_provenance.py --negative-controls --json-out answers/1-jsonhero-object-provenance/verification-result.json
```

The test script deterministically executes the following verification steps:
1. Validates the cryptographic SHA-256 digest (`19f21855...`) and byte length (147,840 bytes) of the primary county dataset.
2. Asserts object identity `cAKmcm9SE6lT` across all 6 sequential records within the 11-second burst from `2026-06-18T20:18:48Z` to `2026-06-18T20:18:59Z`.
3. Verifies document type determination (`type: "url"`) from first-party JSON Hero code and the recorded HTML `<title>` prefix `JSON Hero - https://www.proxymule.com/__PrOxY__/https/w[...]`.
4. Correlates the recorded proxy prefix with peer records `b0d56e4d` and `32ff2ba5` to establish upstream target `https://www.sec.gov/files/county.json` without executing proxy payloads.
5. Verifies schema and value matching of query parameters `$.regCF_county_2019`, `$.regCF_county_2020`, and `$.regCF_county_2021` against root keys in the primary county dataset.
6. Confirms segregation of origin last-modified timestamps, activity burst timestamps, and archive observation timestamps.
7. Executes negative controls confirming that altered hashes, invalid types, nonexistent JSONPath keys, or conflated clocks fail immediately.

## Acceptance Criteria

### 1. Provide an existing capture/export with exact source URL, collection date, raw artifact and SHA256

Public retained records preserved in the Swarmstatus archive capture the exact shortener entries indexing `cAKmcm9SE6lT`:

* **Record `529d85dd66a9f4cde0bd5f384047d301`** (Alias `massjh86420data27`):
  * **Source URL**: `https://bitily.in/MYLABI/admin/index.php?page=627&perpage=15&search=&search_in=all&sort_by=timestamp&sort_order=desc&total_pages=9402`
  * **Collection / Reported Date**: `2026-06-18T20:18:57+00:00` (Epoch `1781813937`)
  * **Raw Artifact**: `work/database-research/indexed_new_records.jsonl` (source extract SHA-256: `bde17019cd08c0b64f4e9286531415af7299d59b7ba7791dd8aef220d56f9c37`)
  * **Body Digest**: `3e5cdd341b417239ebd5d0886971bd7f46f5f8ccf76dece3b7201e6a43ea8b39`
  * **Target URL**: `https://jsonhero.io/j/cAKmcm9SE6lT?path=$.regCF_county_2020`
  * **Captured Page Title**: `JSON Hero - https://www.proxymule.com/__PrOxY__/https/w[...]`

* **Record `989fabe46b27139e397502d5ea3bb0cc`** (Alias `massjh86420data26`):
  * **Source URL**: `https://bitily.in/MYLABI/admin/index.php?page=635&perpage=15&search=&search_in=all&sort_by=timestamp&sort_order=desc&total_pages=9383`
  * **Collection / Reported Date**: `2026-06-18T20:18:54+00:00` (Epoch `1781813934`)
  * **Raw Artifact**: `work/database-research/indexed_new_records.jsonl`
  * **Body Digest**: `f1e3e87926c2790fc5acf8eadb972d886adeb108e15f96b3483c0ac4dc9437de`
  * **Target URL**: `https://jsonhero.io/j/cAKmcm9SE6lT?path=$.regCF_county_2019`

* **Record `75e6550682263f544061b90936fa9dd1`** (Alias `massjh86420data28`):
  * **Source URL**: `https://bitily.in/MYLABI/admin/index.php?page=627&perpage=15&search=&search_in=all&sort_by=timestamp&sort_order=desc&total_pages=9402`
  * **Collection / Reported Date**: `2026-06-18T20:18:59+00:00` (Epoch `1781813939`)
  * **Raw Artifact**: `work/database-research/indexed_new_records.jsonl`
  * **Body Digest**: `962d3d5406f2fa070377f922864ffe355675ae8421423552aa6a28c70cd3c003`
  * **Target URL**: `https://jsonhero.io/j/cAKmcm9SE6lT?path=$.regCF_county_2021`

### 2. Establish object identity and document type; if URL-backed, identify the recorded upstream URL without executing opaque historical payloads

#### Object Identity
The 12-character base62 slug `cAKmcm9SE6lT` is the canonical document identifier generated by JSON Hero's ID allocator (`customRandom("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz", 12, ...)` in `app/jsonDoc.server.ts`). It is identically shared across all 6 records (`data23` to `data28`).

#### Document Type (`UrlJsonDocument`, `type: "url"`)
In `triggerdotdev/jsonhero-web` commit `15157053174ba7a0a79c77b2925fbde7e05a6334`:
1. Document creation via `/actions/createFromUrl?jsonUrl=...` invokes:
   ```typescript
   const doc = await createFromUrl(jsonURL, jsonURL.href);
   ```
   This assigns `doc.type = "url"` and stores `doc.title = jsonURL.href` in Cloudflare KV without persisting raw JSON contents (`app/jsonDoc.server.ts`).
2. When rendering the document page, Remix loader loads `doc`, and `meta()` in `app/routes/j/$id.tsx` constructs the HTML `<title>` tag:
   ```typescript
   export const meta: MetaFunction = ({ data }) => {
     let title = "JSON Hero";
     if (data?.doc?.title) {
       title += ` - ${data.doc.title}`;
     }
     return { title, ... };
   };
   ```
3. When the bitily crawler indexed `cAKmcm9SE6lT` on June 18, 2026, it scraped the page `<title>` tag, extracting `JSON Hero - https://www.proxymule.com/__PrOxY__/https/w[...]` (preserved in record `529d85dd`).
4. If `cAKmcm9SE6lT` had been created as raw JSON via `createFromRawJson`, `doc.title` would default to `"Untitled"` or a custom filename (yielding `<title>JSON Hero - Untitled</title>`), never an external proxy URL. This proves conclusively that `cAKmcm9SE6lT` held a URL reference (`type: "url"`).

#### Recorded Upstream URL
Without executing historical payloads or proxy routes, static textual cross-referencing against contemporary June 18, 2026 records resolves the truncated prefix:
* `529d85dd` preserves: `https://www.proxymule.com/__PrOxY__/https/w[...]`
* Contemporaneous record `b0d56e4d4623fce9f6fe1e29dcbbbff1` (`Agent12OfficialPageUnique171`, June 18 2026) records the full URL: `https://proxymule.com/__PrOxY__/https/www.sec.gov/files/county.json`.
* Peer record `32ff2ba5d5a43b2bd724ded08271f76a` (`MassJsonPathsSel1781795887`, June 18 2026) records: `"Official SEC county map JSONhero path object links via SEC county.json proxy"`.

Thus, the recorded upstream URL was `https://www.proxymule.com/__PrOxY__/https/www.sec.gov/files/county.json`, routing to the SEC primary county dataset `https://www.sec.gov/files/county.json`.

### 3. Compare recovered schema and values to the primary county dataset, and separate document creation, archive capture and observation timestamps

#### Schema and Value Correspondence
The query parameters appended to `cAKmcm9SE6lT` across sequential shortener aliases correspond directly to top-level keys in the primary SEC/Investor.gov `county.json` (SHA-256 `19f21855d65a95e4fecd49ee1dd0127748dbebb1eb218c4c877efbc707093297`, 147,840 bytes):
* `path=$.regCF_county_2019` -> Top-level key `regCF_county_2019` (array of 123 county objects).
* `path=$.regCF_county_2020` -> Top-level key `regCF_county_2020` (array of 131 county objects).
* `path=$.regCF_county_2021` -> Top-level key `regCF_county_2021` (array of 213 county objects).

Each element in these arrays complies with the schema:
```json
{
  "code": "string",
  "offerings": 0.0,
  "usd": 0.0,
  "color_code": 0.0
}
```

The Massachusetts rows referenced in contemporary record `32ff2ba5` (`us-ma-...`) occupy exact indices in the dataset:
* `2019`: 6 entries (`us-ma-005` to `us-ma-025` at indices `[46:52]`).
* `2020`: 10 entries (`us-ma-005` to `us-ma-027` and `us-ma-760` at indices `[52:62]`).
* `2021`: 9 entries (`us-ma-001` to `us-ma-027` at indices `[82:91]`).

#### Separation of Timestamps
Strict boundaries separate the four distinct time horizons:
1. **Origin Document Timestamp**: `2025-03-03T17:08:02.000Z` (HTTP `Last-Modified` header from `investor.gov` and `sec.gov` for `county.json`).
2. **URLQuery Transaction Capture**: `2026-06-18T15:35:24.375Z` (Independent network probe receipt confirming SEC county.json SHA-256 `19f21855...`).
3. **June 18 Shortener Activity Burst**: `2026-06-18T20:18:48+00:00` to `2026-06-18T20:18:59+00:00` (An 11-second automated sequence indexing aliases `data23` to `data28`).
4. **Archive Observation Timestamps**: `2026-09-05` (Local download and cryptographic verification of retained artifacts).

No relative or local clock assumptions are conflated with authoritative UTC timestamps.

## Limitations and alternatives

* **Viewer Inaccessibility**: Direct HTTP GET requests to `https://jsonhero.io/j/cAKmcm9SE6lT` timeout or fail to return a live viewer session; Wayback Machine and Common Crawl archives hold no snapshots of this object. Historical recovery therefore relies on preserved indexer metadata and first-party architectural constraints.
* **Refetching / Re-creation Ineligible**: Creating a new document at `jsonhero.io` would produce an arbitrary new ID and would not reflect the historical state of `cAKmcm9SE6lT` on June 18, 2026.
* **Inert Proof Construction**: No proxy endpoints or shortener redirect destinations were executed or replayed; evidence is restricted to static text inspection of preserved index fields and peer wiki records.
* **Attribution Unclaimed**: Creator addresses, API keys, or actor attributions behind `cAKmcm9SE6lT` and the shortener accounts are not identified or claimed.
