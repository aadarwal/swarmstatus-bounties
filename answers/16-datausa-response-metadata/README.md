# DataUSA #16: partial response-metadata supplement

## Verdict

Supported, narrowly: each of four retained report JSONs explicitly records
`x-tesseract-queryrows: 60`, `x-tesseract-totalrows: 60`, and
`x-tesseract-columns: CIP6 ID,CIP6,Year,Completions,Top Completions`.
The HTTP-event dates add a chronology layer to the issue's correctly labeled
report dates. These fields were additional to the issue snapshot reviewed at 20:16 UTC and
prior findings. Main1 has since appended a
[Research update to issue #16](https://github.com/aadarwal/swarmstatus-bounties/issues/16)
at `2026-09-05T20:25:53Z` stating these findings. This package complements that
clarification with portable selected evidence and checks; it adds no new source
acquisition or duplicate issue edit.

No completion values, readable historical response body, or top-five/top-three
row reconciliation are established. Reported row counts do not establish an
actual 60-row table, twelve-year span, ranking rule, or treatment of ties.
Issue [#16](https://github.com/aadarwal/swarmstatus-bounties/issues/16) remains open.

## Evidence and exact query identity

[selected-evidence.json](selected-evidence.json) contains four selected excerpts.
Each identifies the original report URL, full uncompressed report JSON hash and
byte count, canonical acquisition-record ID, exact JSON pointers and raw-string
line positions. The complete report envelopes are excluded.

Each submitted URL, observed URL and request line has this exact parameter order:

```text
https://api.datausa.io/tesseract/data.jsonrecords?cube=ipeds_completions&drilldowns=Year,CIP6&measures=Completions&include=University:<ID>;Gender:<ID>&top=5.Year.Completions.desc
```

The four pairs are 153658/1, 153658/2, 215062/2 and 215062/1. The excerpts preserve
their complete literal URLs as inert evidence. These requests have no additional
or duplicate query keys, standalone `Year`, or `locale`. Do not execute the URLs.

| University / Gender | Original report JSON | Full uncompressed JSON SHA256 | Bytes |
|---|---|---|---:|
| 153658 / 1 | [b658f273](https://urlquery.net/report/b658f273-fd60-4191-b496-d244d47d5531/json) | `4aad92b58f03715d433029ee2b1ccbb441eb0f114d3710490887c2d7ba3351f2` | 7800 |
| 153658 / 2 | [dd6c4784](https://urlquery.net/report/dd6c4784-2a86-49d8-8418-431ed781f0b7/json) | `9255cbc45222f46a0e62b21cd7eb7cbd233511220cf8563b4682ac6bded2d94c` | 7800 |
| 215062 / 2 | [65144082](https://urlquery.net/report/65144082-bcc5-4e7d-96b9-556f35d63872/json) | `82e62ae8f9d4e34004c981b8b00f8ccf8ecbd8d184ac1d10023df2ad753ea666` | 7560 |
| 215062 / 1 | [fabdcd45](https://urlquery.net/report/fabdcd45-6f13-49c8-8823-8650a9905622/json) | `0908f5dda535a478261609e93f51bda46676927dfdfc94f2ad3da49c08349337` | 7800 |

The three count/schema values are lines 9, 10 and 8 of
`/http/0/response/raw`, counting the status line as line 1. The separate structured
`/http/0/response/headers` value is null. Each report has one HTTP event, independently
checked against the complete held original. The canonical acquisition-record IDs
refer to curated ledger records; their note-body hashes are not the report hashes.

## Four separate clock fields

All May dates below are 2026-05-28; the event and report fields retain their literal
`Z` timestamps in the evidence JSON. Response `Date` strings are retained verbatim
and have only second precision.

| University / Gender | HTTP event `/http/0/date` | Report `/date` | Response `Date` header | Report minus event |
|---|---|---|---|---:|
| 153658 / 1 | 00:35:26.339Z | 00:35:47Z | Thu, 28 May 2026 00:35:26 GMT | 20.661 s |
| 153658 / 2 | 00:35:30.424Z | 00:35:51Z | Thu, 28 May 2026 00:35:30 GMT | 20.576 s |
| 215062 / 2 | 00:35:40.750Z | 00:36:02Z | Thu, 28 May 2026 00:35:41 GMT | 21.250 s |
| 215062 / 1 | 00:35:44.570Z | 00:36:05Z | Thu, 28 May 2026 00:35:44 GMT | 20.430 s |

The fourth clock comes from a separate local acquisition manifest:

| University / Gender | Recorded acquisition-workflow start (UTC) | `fetch_manifest.json` pointer |
|---|---|---|
| 153658 / 1 | 2026-09-05T17:29:44.659553+00:00 | `/results/1144/attempted_at_utc` |
| 153658 / 2 | 2026-09-05T17:30:09.653089+00:00 | `/results/1266/attempted_at_utc` |
| 215062 / 2 | 2026-09-05T17:30:02.567143+00:00 | `/results/1232/attempted_at_utc` |
| 215062 / 1 | 2026-09-05T17:30:58.919280+00:00 | `/results/1494/attempted_at_utc` |

Manifest SHA256: `c93d0cafc03e6fd804fc41813696202742e3cb9f2094108de531968422d979fa`.
`attempted_at_utc` was assigned at acquisition-workflow start, before cache checking
or request waiting. It is not exact HTTP-send time, acquisition completion, source
publication, or incident time. No source-publication time or clock accuracy is
established. The differences above do not measure actor latency, delivery, or use.

## Missing bodies and reproduced baseline

All four `/http/0/response/data/data` fields are null, `size_decoded` is zero, and
the response-data SHA256 is the empty-content digest. This supplies no readable
response bytes; it does not show that the origin response itself was empty.

The issue already identifies the four university/gender combinations, response
metadata and missing bodies. It also distinguishes the receipt's top-five query
from later links with `Year=2016,2017,2018` and `top=3.Year.Completions.desc`.
Those distinctions are baseline, not new discoveries here. Later wiki links and
their behavior are not reverified by this package. The issue describes `locale=en`
on retained top-five wiki links; locale is a presentation difference, explicitly
separate from analytical parameters. The four report queries here omit it.

## Reproduction and review boundaries

Run from this directory using Python 3.9 or later:

```sh
python3 -I -B verify.py
```

The verifier uses only these package files and the Python standard library. It
checks file hashes and sizes against [manifest.json](manifest.json), exact source
mappings, pointers, literal query order, header lines and separate clock fields.
Its negative controls reject changed count/schema headers, swapped source hashes,
conflated clocks, changed acquisition-clock meaning and an added year filter.
The manifest covers every payload file except itself. The PR commit pins the
manifest and verifier. Changing all pins can create another internally consistent
package; these checks are not an external authenticity proof.

The portable check does **not** decompress the full originals, recompute their
hashes, prove excerpt completeness, or independently validate historical counts.
It also cannot establish there were no additional HTTP events in the omitted
envelopes. Those comparisons were performed separately against all four held
originals by an independent reviewer; see [review-provenance.json](review-provenance.json).
The full originals total 30,960 uncompressed bytes. The selected-evidence file's
own digest in the manifest is different from each original report digest above.
No source refresh or target/proxy replay is needed or authorized by this package.

## Acceptance criteria and remaining work

| Issue criterion | Status of this partial |
|---|---|
| Stable artifact, dates and content hash | Supplied for selected report metadata, with separate full-source hashes; no numeric body supplied. |
| Complete resource identifier and filters | Preserved for four exact top-five receipt queries; top-three behavior remains unresolved. |
| Submitted URL, observed request, metadata, body and answer distinguished | Preserved; metadata is the supported result, and neither readable body nor numeric answer is claimed. |
| Preserve university, gender, years, limits, drilldowns and measures | All receipt parameters retained; no year filter in these receipts. Later 2016/2017/2018 top-three queries remain distinct baseline. |
| Readable saved response and row comparison | **Unresolved** for all four combinations. |
| Language locale explicitly distinguished | Locale absent in these receipts; the issue's wiki `locale=en` distinction is presentation context, not analytical equivalence by omission. |

Resolution still requires retained numeric CIP6/Year/Completions rows tied to all
four university/gender queries and a row-wise comparison to the later top-three
variants. Neither standalone `Year` enforcement nor changes in filters, data
versions, rank behavior or year coverage can be inferred from these headers.
Matching identifiers, status codes, labels or clocks do not authenticate an actor
or prove receipt/use. Refs #16; no resolution or acceptance is asserted.
