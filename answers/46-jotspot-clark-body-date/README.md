# Independent Dating of the Jotspot Clark Newsletter Reference (#46)

## Verdict

Bounded evidence: **supported with boundaries; keep Issue #46 open.**

1. **Chronology Bound**: An independent third-party body capture of Jotspot note `https://jotspot.io/j/sxt2xy8q` exists from **2026-06-08T05:02:17Z** in Common Crawl crawl segment `CC-MAIN-2026-25` (WARC record ID `<urn:uuid:835ccffc-7329-41c8-825d-29d73c3d44d1>`), preserved in the Internet Archive Wayback Machine. This establishes a verified **`body-present-by` bound of 2026-06-08T05:02:17Z**.
2. **Narrowing the Prior Observation Bound**: The previously recorded observation in the issue description was an ordinary GET on 2026-09-05T13:44:39Z. The 2026-06-08 capture narrows the upper presence bound from September 5, 2026 back to June 8, 2026—**6 days, 13 hours, 31 minutes, 7 seconds** (567,067 seconds) after the site-asserted modification time.
3. **Exact Clark Reference Match**: The preserved June 8, 2026 body contains the exact literal full-URL reference:
   `https://pure.md/web.archive.org/web/20130525012744id_/www.clarku.edu/departments/economics/pdf/newsletter%202010color.pdf`
   in an HTML link: `<a href="https://pure.md/web.archive.org/web/20130525012744id_/www.clarku.edu/departments/economics/pdf/newsletter%202010color.pdf" rel="nofollow noopener noreferrer" target="_blank">Archive reading</a>`. This is a full-URL match, not a title match, listing match, or topic match.
4. **Site Assertions vs. Independent Clock**: The note displays server-rendered creation and modification timestamps:
   - `article:published_time`: `2026-06-01T15:03:22.012084+00:00`
   - `article:modified_time`: `2026-06-01T15:31:10.118407+00:00`
   The independent capture on 2026-06-08 proves that the note and its reference were public within one week of these dates. However, the capture does not independently authenticate the unproven June 1 database write times. Prior crawler index records (Common Crawl `CC-MAIN-2026-21`, May 8–21, 2026) returned 404 for this path.
5. **Content Invariance and Token Variation**: Across the June 8 capture, August 17 Common Crawl record, September 5 retained GET, and live verification GET, the HTML article body and length (13,274 bytes) remain invariant. The only differences are the dynamically issued 43-character session CSRF token values in the hidden vote form inputs, which alter the cryptographic document hash without altering the content.
6. **Cross-Platform Request Logs**: The three ProWiki records (`JohnClarkRefsNewsletterQ2026`, `AgentClarkRetryCookie`, `AgentClarkNewsletterRefDX`) declare request log times on `2026-06-01T14:11:12Z` to `14:43:12Z`. These predate the JotSpot site-asserted creation by 20 to 52 minutes and contain the identical Clark URL string. However, they establish shared document referencing across separate services, not native graph edges, task coordination, or message delivery to Jotspot.

---

## Evidence & Retained Artifacts

| Capture / Artifact ID | Source & Operator | Crawl / Observation Clock (UTC) | Byte Length | SHA-256 Digest | Payload SHA-1 Base32 | Public Locator |
|---|---|---|---:|---|---|---|
| `cc-2026-25-wayback` | Common Crawl CC-MAIN-2026-25 / Internet Archive | 2026-06-08T05:02:17Z | 13,274 | `f0849a91eeef2973f3c059274e66a8eb8a5e6632e24ea28df0bf70006f57d3bc` | `NMEUZKRO76OMA6AIP4ISFWEMQSEB3ULR` | [Wayback](https://web.archive.org/web/20260608050217/https://jotspot.io/j/sxt2xy8q) / [Raw](https://web.archive.org/web/20260608050217id_/https://jotspot.io/j/sxt2xy8q) |
| `warc-record-20260608` | Common Crawl S3 WARC Record Slice | 2026-06-08T05:02:17Z | 4,990 (gz) | `79db15cbbecf67a4940e39089266fb0ceb7d4dc99796d7a47ae252a4db2700df` | `ILO5CL4N6RGIN4OXXH4YA2NNIFDLLJXI` (block) | [Common Crawl S3](https://data.commoncrawl.org/crawl-data/CC-MAIN-2026-25/segments/1780687572356.36/warc/CC-MAIN-20260608042447-20260608072447-00702.warc.gz) |
| `cc-2026-34` | Common Crawl CC-MAIN-2026-34 | 2026-08-17T11:26:27Z | 13,274 | Unretained | `4JQXIKLMXX5VVGXIUMBAZTKQ4YBHRGSF` | [Common Crawl S3](https://data.commoncrawl.org/crawl-data/CC-MAIN-2026-34/segments/1786091387263.73/warc/CC-MAIN-20260817095816-20260817125816-00702.warc.gz) |
| `canonical-5330f729` | Swarmstatus API snapshot | Unspecified capture time | 13,274 | `ca8ffe8373ea969d553ffc1e2c3031beb3154e3cd07e11bff0b22274ee232dd5` | `50ca2dbd5367a7c08cbeea36a495989d66a4018373d789a06edb4a749bbdf62e` (body_hash) | [Swarmstatus Record](https://swarmstatus.com/api/record?id=5330f7290d1390e8774a9347ac016411) |
| `retained-get-issue-desc` | Issue #46 Investigation GET | 2026-09-05T13:44:39Z | 13,274 | `edddd6353c747a5168e1ec5f17779244e133c6e73f85079d338cfbb8798fac82` | N/A | Issue #46 description |
| `live-20260905` | Live Verification GET | 2026-09-05T22:09:53Z | 13,274 | `083a91cc0c35fd4c3de04272bf30e9a06fb1c8d60060b85c41fe689ad1d911b7` | N/A | `https://jotspot.io/j/sxt2xy8q` |

---

## Clock Separation Analysis

Four distinct temporal systems govern this evidence:
1. **Archive Observation Clock**:
   - Earliest independent third-party observation: `2026-06-08T05:02:17Z`. Established by Common Crawl crawler HTTP response headers (`date: Mon, 08 Jun 2026 05:02:17 GMT`, `WARC-Date: 2026-06-08T05:02:17Z`) and Internet Archive CDX indexing (`20260608050217`).
   - Subsequent observations: `2026-08-17T11:26:27Z` (CC-MAIN-2026-34), `2026-09-05T13:44:39Z` (issue GET), `2026-09-05T22:09:53Z` (live GET).
2. **Native Revision / Site Assertion Clocks**:
   - `article:published_time`: `2026-06-01T15:03:22.012084+00:00`
   - `article:modified_time`: `2026-06-01T15:31:10.118407+00:00`
   - Clock basis: Server-rendered unauthenticated metadata tags in HTML response.
   - Relationship to observation clock: The independent capture occurred 567,067 seconds (6 days, 13 hours, 31 minutes) after the asserted modification time.
3. **Wiki Export / Request Log Clocks**:
   - ProWiki record `9657e9c8250b4c906ced3313a84a0c34` (`JohnClarkRefsNewsletterQ2026`): `reqlog` / `write_date` `2026-06-01T14:11:12Z`.
   - ProWiki record `8708fd7acd191a00ed5b111736676652` (`AgentClarkRetryCookie`): `reqlog` / `write_date` `2026-06-01T14:42:27Z`.
   - ProWiki record `9348b4019312fa9f890608f364f257cc` (`AgentClarkNewsletterRefDX`): `reqlog` / `write_date` `2026-06-01T14:43:12Z`.
   - Basis: Declared request logs (`time_grade: reqlog`) from ProWiki export archived on `2026-06-25`. These entries reference the identical Clark URL 20–52 minutes prior to the JotSpot site-asserted creation, but originate on an entirely separate platform.
4. **Filename and Embedded URL Component Clocks**:
   - `20130525012744`: Embedded Wayback Machine snapshot timestamp in the referenced URL (`web.archive.org/web/20130525012744id_/www.clarku.edu/...`).
   - `2010`: The publication year of the Clark University Department of Economics newsletter.
   - Basis: Historical age of the referenced PDF document, unrelated to the creation date of the Jotspot note.

---

## Acceptance Criteria

1. **Independently timestamped body capture**: Satisfied. Common Crawl `CC-MAIN-2026-25` capture from `2026-06-08T05:02:17Z` is preserved at `https://web.archive.org/web/20260608050217id_/https://jotspot.io/j/sxt2xy8q` and Common Crawl S3 segment `1780687572356.36/warc/CC-MAIN-20260608042447-20260608072447-00702.warc.gz` (offset `295566139`, length `4990`). Verbatim raw body (13,274 bytes, SHA-256 `f0849a91eeef2973f3c059274e66a8eb8a5e6632e24ea28df0bf70006f57d3bc`, payload SHA-1 base32 `NMEUZKRO76OMA6AIP4ISFWEMQSEB3ULR`) is retained under `evidence/bodies/wayback-20260608.html` and `evidence/bodies/warc-record-20260608.warc.gz`.
2. **Establish presence of exact Clark reference**: Satisfied. The exact URL `https://pure.md/web.archive.org/web/20130525012744id_/www.clarku.edu/departments/economics/pdf/newsletter%202010color.pdf` is present verbatim in the href attribute of an `<a>` tag with anchor text `Archive reading`. It is a character-exact full-URL match, not a title match, listing match, or topic match.
3. **Separate clock systems**: Satisfied. Four independent clock systems (archive observation time, native site assertions, wiki export request logs, and embedded filename/archive component dates) are separated and tabulated above.
4. **Explain what evidence establishes vs contradicts**: Satisfied. The evidence establishes that the note and its exact reference existed on the public internet by `2026-06-08T05:02:17Z`, narrowing the presence bound from September 5 to June 8. It supports the feasibility of the note's June 1 timestamps by confirming existence 6 days later, but does not independently authenticate the June 1 backend database timestamps. It does not establish coordination between ProWiki and JotSpot authors.
5. **Distinguish independent observation from later copies or curator invitations**: Satisfied. Common Crawl is an automated third-party crawler operated by the Common Crawl Foundation. The crawl occurred autonomously on June 8, 2026 as part of regular web sampling, before the creation of Swarmstatus or researcher investigations. It is not a curator archive, a later scraper copy, or a researcher-created invitation.

---

## Limitations and Alternatives

- **Crawler Blind Spot**: Common Crawl crawl CC-MAIN-2026-21 (May 2026) returned 404 for this path. While this confirms the note was not available at that specific crawler probe, lack of coverage does not constitute mathematical proof of nonexistence prior to June 1.
- **Unauthenticated Backend Clock**: The displayed `published_time` and `modified_time` values are rendered by the application server. Without server access logs or database audit trails, backend backdating cannot be ruled out between June 1 and June 8.
- **Dynamic Session Tokens**: The presence of dynamic CSRF form tokens causes document-level cryptographic hashes to vary across requests, even though the article content, structure, and links are completely invariant. Verification must focus on extracted article bodies and normalized token fields.

---

## Reproduction

Run the standalone verification suite:
```bash
python3 answers/46-jotspot-clark-body-date/verify.py --negative-controls
```

Expected output:
```text
VERIFICATION PASS: 7 files verified.
Exact Clark reference verified: https://pure.md/web.archive.org/web/20130525012744id_/www.clarku.edu/departments/economics/pdf/newsletter%202010color.pdf
Independent upper bound: 2026-06-08T05:02:17Z
Delta from site modification: 6 days, 13 hours, 31 minutes, 7 seconds
Negative controls passed: 5/5
```
