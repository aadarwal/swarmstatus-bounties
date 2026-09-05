# Charleston lcdl129141: primary manifest recovery for #17

The exact [institutional manifest](https://rspace.library.cofc.edu/iiif/lcdl129141JPEG1jpg/manifest) identifies **View in Magnolia Cemetery**. A direct acquisition on September 5, 2026 returned 5,484 bytes with SHA-256 `7c981bfa48feb24abdf81e56e17c5f70a2b39aeb11e8664f0b67abaeee26a96c`, matching the response hash and size reported by both retained historical exact-manifest receipts.

This primary recovery was made by the maintainer reviewer while checking PR #35. It was **not present in that submission** at head `b912815e7eb19d271129d7845be7f2d086f5642a`; that submission had a placeholder host and an unrelated revision-export hash. Credit the recovery separately from its author.

## Exact document identity

| Field | lcdl129141JPEG1jpg | Nearby control lcdl129143JPEG1jpg |
|---|---|---|
| Manifest label | View in Magnolia Cemetery | View on South Battery |
| Description | Footbridges at Magnolia Cemetery viewed from across a pond | View west on South Battery from East Battery, with Louis Desaussure House in foreground |
| Contributing institution | Historic Charleston Foundation | Historic Charleston Foundation |
| Catalog Date field | 1893 | 1893 |
| Image service identifier | `https://iiif.library.cofc.edu/iiif/2/205927` | `https://iiif.library.cofc.edu/iiif/2/205929` |
| Current manifest size | 5,484 bytes | 5,257 bytes |
| Current SHA-256 | `7c981bfa48feb24abdf81e56e17c5f70a2b39aeb11e8664f0b67abaeee26a96c` | `13be97ce9731be5687862ec9e89916fe0bcda59a89df6bbd14724d3a7509dae9` |

Both complete JSON bodies are included. The exact manifest has one canvas, 2000×1581, and identifies its media using the source labels `Books` and `StillImage`. The nearby [129143 manifest](https://rspace.library.cofc.edu/iiif/lcdl129143JPEG1jpg/manifest) has a distinct canonical manifest ID, caption and image service. A common numeric prefix, institution or catalog year does not make the objects identical. Images were not retrieved; readable first-party manifest metadata is sufficient for the identity claim.

The catalog Date `1893` describes the cataloged material. It is not the manifest's publication date, the task date, or this acquisition's timestamp. `evidence/identity.json` preserves the exact source fields separately from the capture clocks. The source manifests declare `Public domain.`; this package attributes the factual metadata to the institutional manifests and does not assert a blanket license for either website.

## Historical correspondence and clocks

| Report | Provider report date | Recorded exact GET date | Reported response |
|---|---|---|---|
| [37c153c8](https://urlquery.net/report/37c153c8-a72a-42f2-b183-d36052a0234d) | 2026-05-28 10:53:10Z | 2026-05-28 10:52:49.389Z | 200, 5,484 bytes, SHA-256 `7c981bfa…` |
| [d7cba212](https://urlquery.net/report/d7cba212-4cc3-4c58-85c1-4a1846969d03) | 2026-05-28 10:53:13Z | 2026-05-28T10:52:52.178Z | 200, 5,484 bytes, same SHA-256 |

Both exact report entries name the full URL with host `rspace.library.cofc.edu`. Historical raw HTTP metadata declares `application/ld+json`; the provider's browser-response data describes `application/vnd.mozilla.json.view`. The hash comparison is to that provider-reported response representation. The cached reports have inline response body data **null**. Accordingly, this package establishes a current literal body that matches both historical reported response hashes; it does not pretend that the historical reports themselves exposed readable inline JSON.

The provider JSON files were downloaded earlier on September 5 and retained with independent full-file hashes and acquisition clocks. `evidence/historical-receipts.json` includes the minimal relevant fields and those provenance hashes, omitting IPs, browser headers and unrelated report metadata. Fresh attempts to fetch the report JSON during review returned 404; the historical comparison therefore uses the earlier retained downloads. These fresh failures say nothing about what a historical request returned.

The exact manifest was acquired at `2026-09-05T19:02:22.062267+00:00`; the nearby and wildcard controls at `2026-09-05T19:03:28.728314+00:00` and `2026-09-05T19:03:28.728676+00:00`. These times are acquisition clocks, separate from all catalog, request and report dates.

## Wildcard control

The literal [wildcard route](https://rspace.library.cofc.edu/iiif/%2A129141%2A/manifest) returned HTTP 200, `text/html; charset=UTF-8`, and an empty response in this acquisition. Its empty bytes are included. The [historical wildcard receipt](https://urlquery.net/report/8c45dd93-439f-4e73-9e2a-d5f3b8d2e99c) likewise reports 200 HTML and zero response bytes, with no inline body.

There is no readable canonical object or fallback page in either body-backed current observation or the historical metadata. This evidence does not justify expanding the wildcard to the exact object. Whether the historical server internally treated the route as a fallback or another empty outcome remains undecidable from the available evidence; the issue explicitly permits that outcome to be documented.

## Verification

With Python 3.9 or later, run:

```sh
python3 verify.py --negative-controls
```

The verifier reads only local files, checks every evidence-file hash, parses both manifests, validates exact canonical IDs and image services, compares the two historical reported hashes, and rejects six altered-body, altered-ID, altered-hash and wildcard controls. It never fetches embedded image/context/URL locators or executes code from a source.

To additionally validate the minimal receipt extraction against the retained original compressed JSON reports:

```sh
python3 verify.py --receipt-dir /path/to/retained/report-cache --negative-controls
```

The directory must contain the three `<report_id>.json.gz` files named in the evidence. They are read as inert bytes and their full hashes must match. Without this option the standalone verifier checks the retained receipt declarations; it cannot independently reconstruct omitted provider JSON or prove its acquisition metadata. Both verification modes were run against the local original sources during preparation.

## Acceptance criteria

All six #17 requirements are addressed by this maintainer-supplied package: literal body-backed primary manifests with full locators/dates/hashes; exact complete IDs; separated target/request/response/body/answer scopes; distinct 129141 and 129143 identity evidence; readable canonical manifest metadata; and an explicit, bounded wildcard non-match/undecidable explanation. No actor attribution, conversation link, task execution or new staging-source claim follows from this recovery.
