# Bounty #14: readable TB responses and verified interpretation

The readable TB responses are recovered. Both exact requests return the same 2,789-byte JSON body, whose SHA-256 is `465bf8370140b491c6648b5917e976e21b4f285bed6ea2b7a9025634fad0ba0e`. This matches the hashes recorded in the [2000 receipt](https://urlquery.net/report/080803aa-5bc2-4147-9e8c-3ba881d40757) and [2010 receipt](https://urlquery.net/report/b9cdcab5-0c79-4654-acb9-bbd5a320057d). The fresh captures were acquired on 5 September 2026; the historical HTTP transaction times are 29 May 2026 at 22:49:31.816Z and 22:36:06.094Z, respectively. Those transaction times differ from the report dates.

The [exact 2000 endpoint](https://vizhub.healthdata.org/lbd/api/v1/themes/tb/schemas/annual_mort/info/aggregate/components/1?location_id=66&measure=mort&sex=1&age=10&stat=mean&year_mort=2000) and corresponding [2010 endpoint](https://vizhub.healthdata.org/lbd/api/v1/themes/tb/schemas/annual_mort/info/aggregate/components/1?location_id=66&measure=mort&sex=1&age=10&stat=mean&year_mort=2010) return 54 rows: 18 years, each with upper, mean and lower statistics. Component 1 is the line-chart series. Its configuration expands the year domain and statistic; the year/statistic query fields do not restrict this response to a single row. Select both fields from the returned body before reporting a value.

| Year | Lower | Mean | Upper |
| --- | ---: | ---: | ---: |
| 2000 | 9.22879 | 11.438 | 13.6907 |
| 2010 | 5.72293 | 7.32944 | 9.12279 |

These are Ecuador male tuberculosis mortality rates, age 25–29, per 100,000. The [official configuration](https://vizhub.healthdata.org/lbd/api/v1/themes/tb/config) supplies the sex/age labels, mortality units, statistic definitions and component schema. Its 3,630-byte body also matches 174 historical response hashes. The [current location hierarchy](https://vizhub.healthdata.org/lbd/api/v1/themes/tb/location-hierarchy) maps location 66 to Ecuador. The hierarchy's current hash differs from historical metadata and is used only as current semantic context.

The retained wiki already points to component 0 as a backup. Current component 0 requests for the same complete parameters return three statistics for the selected year, confirming all six values above against component 1. The files and URLs are preserved in the capture ledger; no historical match is claimed for these component 0 captures.

The [cited wiki revision](https://collusion.wiki/explorer/page/dse~AgentTBValuesXYZ19087.html#rev-1), record `20305c8f41f63092aba719f60c9e5314`, labels the sex=1 and sex=2 links “Male Ecuador” and “Female Ecuador.” Those labels agree with the official metadata. It contains no literal numeric rate claim, so this answer does not invent one to validate. [AgentTBEcuadorDataOfficialRefs revision 1](https://collusion.wiki/explorer/page/dse~AgentTBEcuadorDataOfficialRefs.html#rev-1), record `d0c99878be32fc1895ac496fd7c98272`, explicitly describes Ecuador mortality rates for age 25–29 by sex; that description also agrees. Neither comparison establishes that anyone read or used the response.

The [malformed receipt](https://urlquery.net/report/1f80ebe0-2cc2-40de-82a1-c415c5e4a217) has one `location_id` value containing literal ampersands after query parsing. It returned 400 HTML, 138 bytes. It must remain separate from the valid six-parameter request. No malformed request or recorded posting payload was replayed.

All six acceptance criteria are met for response recovery, filter/schema interpretation and body-backed wiki comparison. No actor, model or task-origin inference is supported. Suggested status: maintainer review for resolution of #14.

## Offline verification

From this extracted package, run:

```sh
python3 verify.py --negative-controls
```

Python 3.9 or later is sufficient. The verifier locates evidence relative to itself, reads only this package, makes no network requests and writes no files. It checks 16 file hashes, the exact six query parameters, the malformed one-parameter request, complete year/statistic coverage, component 0 agreement, official metadata, retained wiki excerpts and all 203 distinct ledger joins. Eight in-memory negative controls reject altered bytes, wrong sex/year/condition, a wrong schema, an out-of-range year, wrong units and improper query decoding.

The 203 ledger rows comprise 16 TB series transactions, 174 configuration transactions and 13 AIHW image transactions. These are response observations, not counts of tasks or people. Two TB request URLs share one response body; their identical bytes must not be double-counted as two artifacts. Some additional historical series joins are proxy-wrapper requests, so the exact direct six-parameter assertion applies to the two selected receipts rather than automatically to every hash join.

## Acceptance evidence and limits

| Criterion | Retained support |
| --- | --- |
| Stable artifact, source/acquisition dates and hash | `evidence/acquisitions.json`, `manifest.json`, exact primary links above, unchanged TB JSON captures |
| Full identifiers and filters | `evidence/primary-receipts.json`; the two successful requests and malformed request remain distinct |
| Request, metadata, body and verified answer separated | Provider did not retain the successful bodies. Current publisher bytes match its historical SHA-256 and byte counts. This is a current recovery of matching bytes, not a newly downloaded historical body. |
| Query parsing before comparison | The verifier splits query parameters before percent-decoding their values. The malformed request remains one value and a 400 response. |
| Exact quantity and schema | `tb-config.json`, `tb-series.json`, selected-year component 0 captures and current Ecuador location excerpt |
| Body-backed wiki comparison | `wiki-claim-excerpts.json` retains literal labels/links, a short description, exact source/revision IDs and original body hashes. The claim has no literal numeric answer to compare. |

The original full-corpus verification checked original wiki body hashes and the literal labels against both read-only research databases, and scanned 1,496 cached receipt records. That run is described in `evidence/full-corpus-verification.json`. This small public package verifies the exported ledger and excerpts; it does not independently establish the completeness of that absent collection, reconstruct omitted full wiki bodies, or reconstruct the omitted 3.3 MB location hierarchy from three fields. Original full-body hashes are provenance anchors, not hashes of the retained excerpts. The current hierarchy mapping is context only; its body hash does not match historical hierarchy metadata.

All original response bytes and acquisition metadata are frozen as observed on 5 September 2026. A fresh network request may now differ. To independently re-acquire, make a GET to each URL in `evidence/acquisitions.json` whose method is GET, retain the raw bytes before JSON formatting, and record the acquisition clock/status separately. Compare the captured SHA-256 against the manifest and public URLQuery report JSON fields. For location 66, read `/children/7` from the hierarchy captured at the stated date; indices can change in a later response. Do not replay recorded POST requests or the malformed request. The AIHW image used Tableau's ordinary Download → Image interface, with no export endpoint/status captured; its acquisition limitations are explicit in that ledger.

See [AIHW-12.md](AIHW-12.md) for the partial aged-care result and [REUSE.md](REUSE.md) for source-specific reuse terms. No task-origin, actor or model identity is established.
