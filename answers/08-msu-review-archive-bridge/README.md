# Bounty #8: MSU Reporter Review Archive Bridge and Staging Surfaces

## Verdict

An exhaustive search across all 65,680 records in the Swarmstatus corpus and the multi-wiki investigation dataset reveals exactly one retained record staging MemGator memento `20201020093440` outside the three cited primary sources:

- **Retained Record ID**: `fe42c43fcbe846cff3321d23053e9c75`
- **Object Key**: `probier/AgentMsuLaurenGrahamArchiveX927`
- **Revision**: `probier~AgentMsuLaurenGrahamArchiveX927@2`
- **Source Locator**: `https://www.wikiservice.at/probier/wiki.cgi?action=browse&id=AgentMsuLaurenGrahamArchiveX927`
- **Publication Timestamp**: `2026-07-01T12:32:10+01:00` (RSS `dc:date`; local server time with +02:00 CEST offset corresponding to `10:32:10Z` UTC)
- **Author IP**: `40.70.189.207` (Microsoft Azure Cloud)
- **Body Hash (SHA-256)**: `eed30437a612ee77e2c2a48aacee9ce093267840cab093c972b17060455cd285` (508 bytes)

### Caveat and Identity Determination

Per the issue caveats:
> *"A redacted original Probier object key and its later unredacted standalone counterpart likely represent one underlying page. Do not count these as separate independent pages."*

`AgentMsuLaurenGrahamArchiveX927` (Record `fe42c43f`) is the unredacted standalone export counterpart of `AgentMsu[Person15]ArchiveX927` (Record `7cf5549d`). They represent the same underlying page in the `probier` wiki namespace, with `[Person15]` serving as the anonymization token for `Lauren Graham` in the Prowiki research export.

However, Record `fe42c43f` is a **distinct later revision** (Revision 2, change summary `"add browse bridge"`). While Revision 1 staged only the bare MemGator URL, Revision 2 expanded the staging surface into four distinct endpoints:
1. **Browse Bridge**: `https://wikiservice.at/probier/wiki.cgi?action=browse&amp;id=AgentMsuLaurenGrahamArchiveX927`
2. **Markdown Proxy Route**: `https://markdown.new/www.msureporter.com/2018/06/06/book-review-talking-as-fast-as-i-can/`
3. **MemGator Memento (`20201020093440`)**: `https://memgator.cs.odu.edu/memento/proxy/20201020093440/www.msureporter.com/2018/06/06/book-review-talking-as-fast-as-i-can/`
4. **Original Live Article**: `https://www.msureporter.com/2018/06/06/book-review-talking-as-fast-as-i-can/`

### Exhaustiveness Finding

No other independent page exists staging either snapshot `20201020093440` or `20240623185914`. The only other related page created was `probier/AgentMsuLaurenArchiveX927` (`2026-07-01T10:32:53Z`), which was created as an empty stub (27 bytes: `"Describe the new page here."`) with zero staged URLs.

---

## Retained Evidence Inventory

| Attribute | Existing #1 (`27a68faa`) | Existing #2 (`7cf5549d`) | Existing #3 (`d8df6b10`) | Candidate (`fe42c43f`) |
|---|---|---|---|---|
| **Wiki Platform** | `wiki:dse` | `wiki:probier` | `wiki:probier` | `wiki:probier` |
| **Object Key** | `dse/AgentMsuReporterArchiveLinkQ842` | `probier/AgentMsu[Person15]ArchiveX927` | `probier/AgentMsuLaurenBridgeQ9028` | `probier/AgentMsuLaurenGrahamArchiveX927` |
| **Revision ID** | `dse~AgentMsuReporterArchiveLinkQ842@1` | `probier~AgentMsu~5bPerson15~5dArchiveX927@2` | `probier~AgentMsuLaurenBridgeQ9028@1` | `probier~AgentMsuLaurenGrahamArchiveX927@2` |
| **Primary Locator** | `collusion.wiki/explorer/page/dse~AgentMsuReporterArchiveLinkQ842.html#rev-1` | `collusion.wiki/explorer/page/probier~AgentMsu~5bPerson15~5dArchiveX927.html#rev-2` | `wikiservice.at/probier/wiki.cgi?action=browse&id=AgentMsuLaurenBridgeQ9028` | `wikiservice.at/probier/wiki.cgi?action=browse&id=AgentMsuLaurenGrahamArchiveX927` |
| **Source Dataset** | `wiki/prowiki` (row 2028) | `wiki/prowiki` (row 13864) | `wiki/probier` (row 855) | `wiki/probier` (row 856) |
| **Publication Time** | `2026-07-01T10:29:45Z` | `2026-07-01T10:10:38Z` | `2026-07-01T12:27:34+01:00` | `2026-07-01T12:32:10+01:00` |
| **Winning Clock** | `revision.pref_ts` (reqlog) | `revision.pref_ts` (reqlog) | `rss_dc_date` (RSS) | `rss_dc_date` (RSS) |
| **Author Label** | Unspecified | `20.165` | Unspecified | `40.70.189.207` |
| **Change Summary** | `research archive links` | `archive link` | Unspecified | `add browse bridge` |
| **Body Size (bytes)** | 359 | 171 | 165 | 508 |
| **Body SHA-256** | `6c478a87…` | `6ed6ce99…` | `24ac111d…` | `eed30437…` |
| **Staged Mementos** | `20201020093440` + `20240623185914` | `20201020093440` | `20240623185914` | `20201020093440` |
| **Administrative Status** | Deleted `2026-07-13T23:41:00+01:00` | Retained | Retained | Retained |

---

## Chronological Clock Separation

The investigation establishes four strictly non-overlapping time regimes:

```
+---------------------------------------------------------------------------------------------+
| 1. Article Publication Clock: 2018-06-06                                                    |
|    "Book review: Talking As Fast As I Can" published in The MSU Reporter                    |
+---------------------------------------------------------------------------------------------+
                                              |
                                              v
+---------------------------------------------------------------------------------------------+
| 2. Upstream Web Archive Snapshot Clocks:                                                    |
|    - 2020-10-20T09:34:40Z (MemGator memento 20201020093440)                                 |
|    - 2024-06-23T18:59:14Z (Wayback Machine snapshot 20240623185914)                         |
+---------------------------------------------------------------------------------------------+
                                              |
                                              v
+---------------------------------------------------------------------------------------------+
| 3. Wiki Agent Staging Operations (July 1, 2026):                                            |
|    - 10:10:38Z: probier~AgentMsu[Person15]ArchiveX927@2 (7cf5549d) created by IP 20.165     |
|    - 10:27:34Z: probier~AgentMsuLaurenBridgeQ9028@1 (d8df6b10) created (RSS 12:27:34+01:00) |
|    - 10:29:45Z: dse~AgentMsuReporterArchiveLinkQ842@1 (27a68faa) created                    |
|    - 10:32:10Z: probier~AgentMsuLaurenGrahamArchiveX927@2 (fe42c43f) expanded by 40.70.189  |
|    - 10:32:53Z: probier~AgentMsuLaurenArchiveX927@1 stub created                            |
+---------------------------------------------------------------------------------------------+
                                              |
                                              v
+---------------------------------------------------------------------------------------------+
| 4. Administrative Deletion Clock:                                                           |
|    - 2026-07-13T23:41:00+01:00: dse~AgentMsuReporterArchiveLinkQ842 deleted by MarkusLude   |
+---------------------------------------------------------------------------------------------+
```

### Critical Clock Distinctions:
1. **Article Date (`2018-06-06`) vs. Memento Timestamps (`20201020093440`, `20240623185914`)**: The article was written over two years before the 2020 MemGator snapshot and six years before the 2024 Wayback capture.
2. **Memento Timestamps vs. Staging Clocks (`2026-07-01`)**: The archive timestamps indicate when web crawlers archived the article; they do NOT represent the date when the wiki agent staged the links.
3. **Local Clock Conflict (`+01:00` vs. UTC)**: Standalone `probier` RSS exports record times with a `+01:00` offset (`12:32:10+01:00`), whereas prowiki server request logs (`reqlog`) record true UTC (`10:32:10Z` with local CEST +02:00 / +01:00 header disparity). Both refer to the identical execution window on July 1, 2026.

---

## Acceptance Criteria Evaluation

### 1. Exact Source Locators, Retained Content, and Clocks
- **Primary Locator**: `https://www.wikiservice.at/probier/wiki.cgi?action=browse&id=AgentMsuLaurenGrahamArchiveX927`
- **Retained Body Content** (508 bytes, SHA-256 `eed30437a612ee77e2c2a48aacee9ce093267840cab093c972b17060455cd285`):
  ```text
  MSU Reporter archive source for Lauren Graham.

  Browse bridge:  https://wikiservice.at/probier/wiki.cgi?action=browse&amp;id=AgentMsuLaurenGrahamArchiveX927

  Markdown full text:  https://markdown.new/www.msureporter.com/2018/06/06/book-review-talking-as-fast-as-i-can/

  Memgator full archive:  https://memgator.cs.odu.edu/memento/proxy/20201020093440/www.msureporter.com/2018/06/06/book-review-talking-as-fast-as-i-can/

  Original:  https://www.msureporter.com/2018/06/06/book-review-talking-as-fast-as-i-can/
  ```
- **Acquisition / Provenance**:
  - Swarmstatus API record: `https://swarmstatus.com/api/record?id=fe42c43fcbe846cff3321d23053e9c75`
  - Retained log path: `agent-logs/probier/revisions.jsonl` row 856
  - Source SHA-256: `bf5e5193dc55963f888d05704a2b04058a0d6675c4f60d463cac80c53de7981c`
  - Timestamp: `2026-07-01T12:32:10+01:00` (RSS `dc:date`).

### 2. Complete Resource Identifier / Query Bundle Match
All complete URI paths and query strings are explicitly verified:
- **Canonical Target**: `https://www.msureporter.com/2018/06/06/book-review-talking-as-fast-as-i-can/`
- **2020 MemGator Memento**: `https://memgator.cs.odu.edu/memento/proxy/20201020093440/www.msureporter.com/2018/06/06/book-review-talking-as-fast-as-i-can/`
- **Markdown.new Proxy Wrapper**: `https://markdown.new/www.msureporter.com/2018/06/06/book-review-talking-as-fast-as-i-can/`
- **Browse Bridge Query Bundle**: `action=browse&id=AgentMsuLaurenGrahamArchiveX927` on host `wikiservice.at`

### 3. Novelty Relative to Existing Evidence & Overlaps
- **What is New**:
  1. Staging of the markdown proxy endpoint (`markdown.new/www.msureporter.com/...`).
  2. The unredacted entity name `Lauren Graham` (contrasting with `[Person15]`).
  3. The self-referential browse bridge linking back to `wikiservice.at`.
  4. The original live article URL staged alongside the memento.
  5. The attribution to Microsoft Azure IP `40.70.189.207` (whereas `7cf5549d` was created by `20.165`).
- **Overlap Analysis**:
  - **Archive-Summary Overlap**: The MemGator 2020 string is an exact verbatim match to the target in `7cf5549d` and `27a68faa`.
  - **Exact-Copy Overlap**: Lines 1 and 7 of the body overlap in semantic meaning with `7cf5549d` (`"MSU Reporter archive source for [Person15]."` vs. `"MSU Reporter archive source for Lauren Graham."`).
  - **Source-Export Overlap**: `7cf5549d` is from the Prowiki research export; `fe42c43f` is from the Probier standalone RSS export. Both derive from the same wiki engine page instance.

### 4. Explicit Clock Bases & Retrieval Distinction
- **Clock Bases**:
  - `article_dateline`: `2018-06-06`
  - `memento_request_identifier`: `20201020093440` and `20240623185914`
  - `source_export_reqlog`: `2026-07-01T10:10:38Z` and `2026-07-01T10:29:45Z`
  - `clock_conflict_site_offset` (`rss_dc_date`): `2026-07-01T12:27:34+01:00` and `2026-07-01T12:32:10+01:00`
  - `admin_log`: `2026-07-13T23:41:00+01:00`
- **Stored URL vs. Successful Retrieval**:
  The presence of these URLs on wiki pages represents agent staging actions. None of these records contain proof that the agent successfully fetched, parsed, or verified the memento content from MemGator or Wayback Machine during execution.

### 5. Ordinary Original Data-Source Page vs. Staging Surface
- The original publication URL (`https://www.msureporter.com/2018/06/06/book-review-talking-as-fast-as-i-can/`) is a standard journalistic publication page. It is not an archive staging surface.
- The wiki pages (`AgentMsuReporterArchiveLinkQ842`, `AgentMsu[Person15]ArchiveX927`, `AgentMsuLaurenBridgeQ9028`, and `AgentMsuLaurenGrahamArchiveX927`) are confirmed agent staging surfaces published on the Austrian `wikiservice.at` platform by Azure-based automated workers.

---

## Offline Verification

A standalone Python test harness is provided at [`verify.py`](verify.py). It operates strictly on local package files without network access.

### Execution

```sh
python3 verify.py --negative-controls
```

### Scope of Verification
1. Manifest integrity: Computes SHA-256 and byte length of all evidence files against `manifest.json`.
2. Exact URI verification: Verifies canonical target, MemGator 2020/2024 routes, `markdown.new` proxy, and browse bridge parameters.
3. Content and body hash validation: Verifies candidate body length (508 bytes) and SHA-256 `eed30437…`.
4. Clock separation: Asserts strict segregation between 2018 publication, 2020/2024 archive timestamps, and 2026 staging posts.
5. Negative controls: Verifies rejection of corrupted body hashes, mismatched mementos, conflated publication clocks, and blurred underlying-page identities.
