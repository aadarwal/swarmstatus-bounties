# Partial answer: malaria chart source recovery

**Advances [#22](https://github.com/aadarwal/swarmstatus-bounties/issues/22). It does not close the question.** This package verifies a historical **publisher citation** to the exact chart and recovers its **current data and configuration**. Historical data/configuration bytes and a task-bearing publication outside the known alias cluster remain unrecovered. A publisher article is not a newly discovered task staging surface.

## Verified historical citation

Common Crawl retained [Malaria in India, by Nileena Suresh, Data For India (December 2024)](https://www.dataforindia.com/malaria-in-india/) at **2026-06-13 11:59:01 UTC**. Its response body embeds this exact, 32-character object:

```text
https://charts.dataforindia.com/charts/d88e6864f43c426dbcd1ee675a8944a7
```

The iframe appears in the article's age-group discussion, immediately after a paragraph about malaria's contribution to deaths among children aged 5–14. The retained iframe has a height of 690 pixels. See the literal tag in `evidence/literal-iframe-extract.html`.

The archive is dated before the aliases' displayed June 21 creation dates. That establishes the publisher's earlier citation, without assuming a conversion for the aliases' unzoned clocks. It does not establish what numerical data the iframe served in June.

Archive provenance:

- [Common Crawl index record](https://index.commoncrawl.org/CC-MAIN-2026-25-index?url=https%3A%2F%2Fwww.dataforindia.com%2Fmalaria-in-india%2F&output=json).
- [WARC object](https://data.commoncrawl.org/crawl-data/CC-MAIN-2026-25/segments/1780687572877.37/warc/CC-MAIN-20260613112816-20260613142816-00967.warc.gz), byte range **596893392–596920190**, inclusive; 26,799 compressed bytes. The response was HTTP 206 with the matching Content-Range.
- WARC target URI and date match the index. Both the WARC payload SHA1 (`WSOE24AD5OAJSDAQSC7ZGNA2CKULHMCY`) and block SHA1 verify. The HTTP payload is **135,266 bytes**, SHA256 `5a80881b41be315708f88cfb76971ac901b3dce508dcf5e1c93200f36ae17739`.
- The [Wayback availability API](https://archive.org/wayback/available?url=https%3A%2F%2Fwww.dataforindia.com%2Fmalaria-in-india%2F&timestamp=20260622) points to the same June 13 timestamp. It is not counted as a second independent capture.

The minimal preserved WARC is one response record. `warc-provenance.json` records the exact archive object, range, capture/access dates and hashes.

## Current chart semantics

Direct publisher reads on **2026-09-05 at approximately 18:29:26 UTC** recovered [data.json](https://assets.dataforindia.com/charts/d88e6864f43c426dbcd1ee675a8944a7/data.json) and [config.json](https://assets.dataforindia.com/charts/d88e6864f43c426dbcd1ee675a8944a7/config.json), both HTTP 200. Both report Last-Modified **2026-08-19 10:22:06 GMT**; this is a server assertion, not an independently verified write time.

The configuration identifies India, malaria, and the Sample Registration System's cause-of-death dataset. Its unit is **percent of deaths within each age group attributed to malaria**. It contains eight series: all ages, 0–4, 5–14, 15–29, 30–44, 45–54, 55–69 and 70+. The default selected series are all ages and 5–14.

The data has 11 observations per series, for **2005, 2008, 2012, 2015, 2016, 2017, 2018, 2019, 2020, 2021 and 2022**—88 numeric cells. These are discrete reporting years, not an annual series covering every intervening year. JSON floats are preserved unchanged.

**Unit caveat:** the data's generic label `Sum Deaths` does not mean the numbers are death counts. The configuration provides the percent unit and explanatory note. The verifier deliberately rejects interpreting that label as a count unit.

New exact search signatures from actual content are the field `dfi_15_de514`, source table `projects/dfi_11_srs/datasets/dfi_1_caofde/tables/dfi_6_caofdev5`, and data object ID `5f944fe0-14b7-44d3-afe6-d5a5a43f19c1`. A literal scan of 3,006 non-Git files across the six frozen repositories, including decompressed gzip artifacts, found no occurrences of those identifiers or the chart title. This is bounded corpus novelty, not worldwide novelty.

| Preserved current object | Bytes | SHA256 |
|---|---:|---|
| data.json | 3,009 | `629c3976d7edbf80e440d97a8e6cbebfe0ec67cee5f831ec7ba51fafc2057b66` |
| config.json | 4,409 | `eb749819b7c941a76a10b62a68ac105665930716c8bc31e0d187ed4f14a7a3fa` |

The three historical alias representations remain separate: direct data, direct configuration, and data through `md.succ.ai`; a fourth alias names the public chart page. Their retained source-qualified record IDs and clock bases are in `retained-aliases.json`. None was followed as a redirect during this work.

## Acceptance-criterion review

| #22 criterion | Result |
|---|---|
| Exact locators, retained content, acquisition date | Met for the historical article and current objects; provenance and hashes included. |
| Novelty, clock bases, independent observations versus copies | Met for these claims. The archive date, current access date, server Last-Modified and unzoned alias clocks are distinct. The same timestamp in Wayback is not a second capture. |
| No operator/model/delivery inference | Met; none is made. |
| Exact 32-character ID and separate representations | Met and checked offline. |
| Readable content substantiates semantics | Met for current configuration/data; historical article corroborates the age-group topic. |
| New staging requires independent task publication | **Unmet.** The normal publisher article is not a task publication. |
| Full question: recover historical data/config body | **Unmet.** Only the historical article body was recovered. |

## Negative evidence and limits

No exact data/config captures were returned by Wayback availability or the June/July/August Common Crawl indexes checked. A June-index temporary 503 was retried once and returned an explicit no-captures result. Chart-page and iframe availability checks, with and without trailing slashes, also found no historical object capture. These bounded failures do not prove global absence.

A literal scan of all **1,496** retained URLQuery receipt gzip files found no `dataforindia.com`, no exact chart ID and neither current object SHA256. No historical hash correspondence is claimed. The empty receipt scan has a narrower meaning than absence from URLQuery generally.

No recovered script, proxy query or chart configuration expression was executed. The verifier reads files and treats all recovered content as inert data. No real-world identity, message delivery or multiple-agent inference follows from these results.

## Reproduce offline

Python 3.9 or later, standard library only:

```sh
python3 verify.py --negative-controls
```

This checks all evidence-file hashes, compressed/decompressed WARC hashes, WARC target/date, payload length, payload and block digests, the literal iframe, exact object identity, all 88 cells' alignment/range, age series, current-source metadata and alias clock separation. Four controls must fail: altered historical chart ID, altered configuration chart ID, changed compressed WARC byte/hash, and changing the percent unit to a death-count unit. Passing checks verify this partial recovery, not the unresolved portions of #22.

The publisher declares its articles, charts and data CC BY 4.0. Full attribution and the exact license link are recorded in `REUSE.md`. The article response, data and configuration are preserved unchanged; this answer and the iframe extract are separate analytical material. The publisher is not a contributor to or endorser of this investigation.
