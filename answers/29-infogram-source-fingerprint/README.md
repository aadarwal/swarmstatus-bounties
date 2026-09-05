# Recovered Rajinikanth chart: a source-specific numeric fingerprint

The current canonical Infogram page and exact embedded UUID yield equal literal `window.infographicData` JSON objects. No page JavaScript was executed. The embedded table has 11 film rows; the publisher article directly embeds that UUID alongside three sibling chart UUIDs.

The table lists Rajinikanth as 67 and Amy Jackson as 26 for *2.0*, giving a derived difference of 41. The accompanying publisher article says the gap was about 42. These are distinct published representations. This report does not adjudicate actual ages or establish which representation any agent retrieved.

Sources: [canonical chart](https://infogram.com/rajinikanth-indian-cinemas-age-gap-problem-the-quint-1h1749vqy0p0l6z), [embedded chart](https://e.infogram.com/55eeebff-2501-4b78-979d-1c7c1e5c4f74?src=embed), [publisher article](https://www.thequint.com/entertainment/salman-khan-to-akshay-kumar-only-bollywood-heroes-are-forever-young).

`chart-table.json` preserves the factual table, exact cell strings, UUID and source-declared creation/update times. Capture timestamps and full-response hashes are separate in `capture-metadata.json`. Source-declared 2022 timestamps do not independently date the table's historical contents.

The exact UUID appears in 10 retained source rows. They provide retrieval links, including carried-forward copies, rather than a recovered chart response or answer. Example revision-qualified sources: [DSE TestSeite revision761](https://collusion.wiki/explorer/page/dse~TestSeite.html#rev-761), [Probier SandBox revision8](https://collusion.wiki/explorer/page/probier~SandBox.html#rev-8), and [QuintChartAPI4777 revision 2](https://collusion.wiki/explorer/page/probier~QuintChartAPI4777.html#rev-2).

All three sibling UUIDs are absent from literal body search of the 199,197 retained rows. That is a bounded negative control, not global absence or evidence of new task activity. The original publisher article is source context, not an independent agent staging surface; bounty #7 remains unresolved.

The primary table provides a better search fingerprint than the generic title: ordered film rows, exact cell spelling, secondary-lead columns and the 41-year computed difference. Future matches require source context and dating; repeated data alone does not identify an actor.


## Reproduce from primary captures

This package contains the factual chart table and capture metadata. Full publisher article HTML is not redistributed. Save each of the three primary responses linked above as `canonical.html`, `embed.html` and `publisher.html`, then run:

```sh
python3 verify_chart.py --canonical canonical.html --embed embed.html --publisher publisher.html
```

The verifier extracts literal JSON without executing page scripts and checks UUID identity, the complete ordered table, equality of canonical/embed data, publisher embedding, source-declared dates (not historical proof), and altered-UUID/cell/date negative controls. The verifier compares input hashes with `capture-metadata.json`; add `--require-capture-hashes` to require exact September 5 bytes: a later changed response is a new capture and cannot reproduce the historical acquisition hash. `verification.json` records the independently repeated checks on the September 5 captures.

This partial answer advances [#7](https://github.com/aadarwal/swarmstatus-bounties/issues/7) and the more specific [#29](https://github.com/aadarwal/swarmstatus-bounties/issues/29). Both remain open pending the requested independent staging or retained answer evidence.
