# Independent Dating and Benchmark Content Analysis for 13 K4be Bodies (#54)

## Verdict

Partial evidence: **supported with boundaries; keep Issue #54 open.**

1. **Chronology Bound**: All thirteen public K4be pastes currently declare creation timestamps spanning 14 December 2025 to 1 March 2026. However, independent CDX index queries across public web archives (Wayback Machine, Archive.today) confirm zero pre-September 2026 snapshots for any of the thirteen pastes. A historical capture proves presence by its capture time, not first publication. The earliest defensible **body-present-by bound** is established by verified local acquisition on **5 September 2026 (20:23:41Z UTC)**. The provider-asserted creation timestamps remain unauthenticated service metadata. Cohort-wide historical dating remains open and unresolved.
2. **Distinctive Benchmark Task Match**: Paste `1806ec31` is an exact token-for-token match to item `AMT/2008/page_32.pdf-4` at index 619 of `dataset/dev.json` in the public financial question-answering benchmark repository `czyssrs/FinQA` (commit `0f16e2867befa6840783e58be38c9efb9229d742`). The stored question, answer (`29.2%`), and programmatic DSL execution (`subtract(37.28, 28.85), divide(#0, 28.85)`) reproduce the benchmark record verbatim.
3. **Structured Document Clusters**: The thirteen bodies partition into identifiable source clusters:
   - **American Tower SEC Form 10-K (2008)** (`17bbf392`, `c9601cdf`, `1806ec31`, `5a4aa403`): Four progressive representations of Item 5 market prices and the February 13, 2009 closing price ($28.85).
   - **Humana Inc. SEC Form 10-K (2015)** (`5329a841`, `bd44d381`, `680ec235`): Three representations of the Stock Total Return Performance graph, matching items in FinQA `dataset/train.json` (indices 149, 538, 677) and citing the bullfincher.io SEC proxy.
   - **Public Statistical Series**: Basketball-Reference 2015-16 3-point arithmetic (`3ae5f54b`), OWID/World Bank armed forces series (`06d98526`), World Bank country emissions/population series (`d78a30b4`), and ACI airport rankings (`0263afe2`).
   - **Programming Metaphor Meme**: Duplicate bodies (`514333ed` and `316996fe`) posted 1 second apart.
4. **Coordination Boundary**: Demonstrating an exact match to a public dataset item establishes a content relationship only. It does not establish agent identity, communication, task assignment, message delivery, or transfer direction.

---

## Retained Evidence & Verified Identifiers

All thirteen raw API envelopes are preserved verbatim under `evidence/api/<pid>.json`. All thirteen unmodified raw body strings are preserved under `evidence/bodies/<pid>.txt`.

| Paste ID | Public View URL | Native Created (Unix) | Native Created (UTC) | Decoded Body Bytes | UTF-8 Raw Body SHA-256 | Content Cluster | Historical Dating Status |
|---|---|---:|---|---:|---|---|---|
| `3ae5f54b` | [view](https://pastebin.k4be.pl/view/3ae5f54b) | `1765687906` | 2025-12-14T04:51:46Z | 577 | `4561a13e3c59846d9d02bf2fad88964598632b2f9a86d106d9e2f5667cb4621d` | NBA 3-Pt Stats | Unresolved |
| `514333ed` | [view](https://pastebin.k4be.pl/view/514333ed) | `1767264965` | 2026-01-01T10:56:05Z | 487 | `76da74d9471e7b12892b538b85d3fba70005799a56f6081f1878ff8b16bfe485` | Alchemical Breakdown | Unresolved |
| `316996fe` | [view](https://pastebin.k4be.pl/view/316996fe) | `1767264966` | 2026-01-01T10:56:06Z | 487 | `76da74d9471e7b12892b538b85d3fba70005799a56f6081f1878ff8b16bfe485` | Alchemical Breakdown | Unresolved |
| `5329a841` | [view](https://pastebin.k4be.pl/view/5329a841) | `1772117364` | 2026-02-26T14:49:24Z | 900 | `94d46d8d52654d063d1056eede571b94c39889a0b6d953ed873df31900395948` | Humana 2015 10-K | Unresolved |
| `bd44d381` | [view](https://pastebin.k4be.pl/view/bd44d381) | `1772117418` | 2026-02-26T14:50:18Z | 590 | `ec89a96fa17f4347f5976e1e392cc5a9fa20cdd05b8ab650e5156db4e89c09d7` | Humana 2015 10-K | Unresolved |
| `680ec235` | [view](https://pastebin.k4be.pl/view/680ec235) | `1772117539` | 2026-02-26T14:52:19Z | 330 | `c36c211ea5138142c7bf257386df02fc5e77f59293e1349f5a597d82e095363a` | Humana 2015 10-K | Unresolved |
| `d78a30b4` | [view](https://pastebin.k4be.pl/view/d78a30b4) | `1772136944` | 2026-02-26T20:15:44Z | 208 | `05b598b81113a62916b83a0bbe8e4eccacb4ff62cb83faf19f1f5dd6dac6870c` | World Bank CO2/Pop | Unresolved |
| `0263afe2` | [view](https://pastebin.k4be.pl/view/0263afe2) | `1772136947` | 2026-02-26T20:15:47Z | 903 | `1d9adba5396d886107cba63d3d4667a44c22cbb91ece7a89e9aa121752bf581b` | Airport Rankings | Unresolved |
| `06d98526` | [view](https://pastebin.k4be.pl/view/06d98526) | `1772371458` | 2026-03-01T13:24:18Z | 537 | `1d7c03707602cbb5378e88a6d8f3955633d276bf4b0fe76a1a8f84b4907fefef` | OWID Armed Forces | Unresolved |
| `17bbf392` | [view](https://pastebin.k4be.pl/view/17bbf392) | `1772371822` | 2026-03-01T13:30:22Z | 1204 | `cef636fa0156ef66700b6cff2669721279804dfbf83025db98878a07789d791a` | American Tower 10-K | Unresolved |
| `c9601cdf` | [view](https://pastebin.k4be.pl/view/c9601cdf) | `1772371879` | 2026-03-01T13:31:19Z | 608 | `64254238457d888ea0a4c90e48948c1d96f9e8e3c52936e5f46386df04d2f8e0` | American Tower 10-K | Unresolved |
| `1806ec31` | [view](https://pastebin.k4be.pl/view/1806ec31) | `1772371959` | 2026-03-01T13:32:39Z | 234 | `d28c67fdf6b313dda342202ce5059fb3287e36a39bcf3d7b192f2c9e5107470b` | FinQA #619 Task | Unresolved |
| `5a4aa403` | [view](https://pastebin.k4be.pl/view/5a4aa403) | `1772372008` | 2026-03-01T13:33:28Z | 332 | `373bc8c396433321ac42a05402d588c097c6b3fd7df413954e6686acf4f6a112` | American Tower 10-K | Unresolved |

---

## Chronology Findings and Clock Boundaries

The K4be API responses declare four separate clock fields:
1. `created`: Declared creation time as an integer Unix epoch. These values span `1765687906` (2025-12-14) to `1772372008` (2026-03-01).
2. `hits_updated`: Last time the hit counter mutated in the backend database.
3. `expire`: Configured expiration epoch.
4. Acquisition Timestamp: The verified network capture interval on 5 September 2026 (`20:23:41.496574` to `20:24:27.802742` UTC).

### Archival Evidence
Wayback Machine CDX queries for `pastebin.k4be.pl/view/<pid>`, `pastebin.k4be.pl/api/paste/<pid>`, and `pastebin.k4be.pl/<pid>` yield no indexed captures before September 5, 2026. Because provider metadata can be created or updated internally, a service-provided timestamp does not constitute third-party proof of publication. 

The defensible body-present-by bound is **2026-09-05T20:23:41Z UTC**.

---

## Content Relationships to Public Benchmarks & Filings

### 1. FinQA Exact Benchmark Task Match (`1806ec31`)
Paste `1806ec31` contains the following body text:
```text
Question: what is the growth rate in the price of shares from the highest value during the quarter ended december 31 , 2008 and the closing price on february 13 , 2009?
Answer: 29.2%
Program: subtract(37.28, 28.85), divide(#0, 28.85)
```
- **Repository**: `czyssrs/FinQA` (commit `0f16e2867befa6840783e58be38c9efb9229d742`).
- **File**: `dataset/dev.json` (SHA-256: `a847fb7e0d61a3125a1e2909852df6b89f1ee64d2c5ff1bf689e332214deee51`).
- **Index**: 619 (`id: "AMT/2008/page_32.pdf-4"`).
- **Program Execution**:
  - Step 0: `subtract(37.28, 28.85)` = `8.43`
  - Step 1: `divide(8.43, 28.85)` = `0.292199...` = `29.2%`
  - Computed output matches the stored answer `29.2%` exactly.

### 2. American Tower Corporation (AMT) SEC 2008 Cluster
Four pastes form a progressive representation pipeline from the same section of American Tower's 2008 Form 10-K (Part II, Item 5, page 32):
- `17bbf392` (`1772371822`): Raw SEC filing prose and table with dot leaders (`Quarter ended March 31 . . . . $42.72 $32.10`).
- `c9601cdf` (`1772371879`, +57s): Pipe-delimited structured table matching FinQA's pre-processed format (`2008 | high | low quarter ended march 31 | $ 42.72 | $ 32.10 ...`).
- `1806ec31` (`1772371959`, +80s): The FinQA reasoning task based on this table.
- `5a4aa403` (`1772372008`, +49s): Summarized synthesis of the quarterly highs/lows and closing price.

### 3. Humana Inc. (HUM) SEC 2015 Cluster
Three pastes derive from Humana Inc.'s Form 10-K for the fiscal year ended December 31, 2015:
- `5329a841` (`1772117364`): Full table prose referencing `https://bullfincher.io/sec-proxy?url=https%3A%2F%2Fwww.sec.gov%2FArchives%2Fedgar%2Fdata%2F49071%2F000004907116000117%2Fhum-20151231x10k.htm`. Matches FinQA training items at indices 149, 538, 677 (`HUM/2015/page_46.pdf-1, -2, -3`).
- `bd44d381` (`1772117418`, +54s): Formatted ASCII multi-year return table.
- `680ec235` (`1772117539`, +121s): Isolated data points for 2011 ($162) and 2012 ($128).

---

## Public Dataset vs. Coordination Claim Separation

Matching a publicly available benchmark item (FinQA) or open statistical repository (OWID, World Bank, Basketball-Reference):
- **Demonstrates**: Content identity and mathematical equivalence to existing public corpus records.
- **Does NOT Demonstrate**: Message transmission, receipt, agent execution, workflow coordination, or transfer direction.
- **Reporting Rule**: Content relationship findings are reported independently from chronology findings.

---

## Offline Reproduction

Run the standalone verifier using Python 3.9+:

```bash
python3 answers/54-k4be-early-body-dating/verify.py --negative-controls
```

The verifier executes with zero network calls and validates:
1. `manifest.json` SHA-256 and byte sizes for all package files.
2. All 13 raw API envelope contents, JSON structures, and UTF-8 raw body digests against Issue #54 controls.
3. Absence of sensitive credential keys.
4. FinQA dev item 619 program execution arithmetic and answer equivalence.
5. All six negative controls (tampered body hash, conflated publication clocks, premature cohort dating closure, promoted coordination claims, corrupted FinQA execution, sensitive key leakage).

---

## Acceptance Criteria Checklist

| Issue #54 Criterion | Package Status | Finding Summary |
|---|---|---|
| Defensible body-present-by bound | **Supported** | Bounded at 2026-09-05T20:23:41Z based on verified acquisition; provider timestamps alone do not prove earlier publication. |
| Report each of 13 objects separately | **Supported** | All 13 objects documented with individual timestamps, hashes, byte counts, and unresolved historical status. |
| Concrete content relationship tested | **Supported** | Exact match established for `1806ec31` to FinQA dev set #619; American Tower and Humana clusters documented. |
| Distinguish task match from coordination | **Supported** | Explicit boundary drawn: benchmark match proves public content relationship only, not swarm communication or receipt. |
| State relationship independently from chronology | **Supported** | Chronology remains unresolved; content relationships confirmed independently. |
