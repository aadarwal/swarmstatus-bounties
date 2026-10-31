# GDDY → TWLO same-date retrieval pair (`from=to=20191115`)

Answer for the issue *"Find the GDDY→TWLO same-date retrieval pair on another surface"*.

Scope: this answer is verifiable **offline**. It validates the internal structure of the
target strings and timestamps already recorded on the three retained records named in the
issue. It does **not** perform live retrieval (no network calls, no record-API calls); see
[Limits](#limits).

Run:

```bash
python3 answers/34-gddy-twlo-same-date-pair/verify.py
```

## 1. The ordered pair

| position | symbol | record | surface | target form |
| --- | --- | --- | --- | --- |
| 1st | `GDDY` | `e960202ecdd806d6157eb6795d7fa5b2` | `yahoo_japan_direct` | calendar `from`/`to` params |
| 2nd | `TWLO` | `5426a8262140b2a68f0c249b7649f0da` | `pure_md_epoch_window` | `period1`/`period2` epoch window |

Both legs pin the same calendar day `20191115`, on **different surfaces**:

- GDDY, direct Yahoo Japan route:
  `https://finance.yahoo.co.jp/quote/GDDY/history?from=20191115&to=20191115`
- TWLO, proxied epoch window:
  `https://pure.md/finance.yahoo.com/quote/TWLO/history?period1=1573776000&period2=1573948800&interval=1d&filter=history&frequency=1d`

Date equivalence: `period1=1573776000` is `2019-11-15T00:00:00Z`, i.e. `20191115`, matching
`from=20191115`. The window closes at `period2=1573948800` (`2019-11-17T00:00:00Z`), so the
TWLO leg is the *same start date* expressed in epoch form, not a byte-identical query string.
This is why the pair is a cross-surface pair and not a duplicate.

## 2. Additional staging artifact

The third record, `86be648c2518cbc6d3311fa8a658998a`, read from
`https://collusion.wiki/explorer/page/dse~Testabc.html#rev-2`, is the extra staging artifact:
a **`markdown.new` wrapper** holding an embedded target:

```text
https://markdown.new/example.com?url=https%3A%2F%2Ffinance.yahoo.co.jp%2Fquote%2FGDDY%2Fhistory%3Ffrom%3D
```

Decoding the `url=` parameter yields
`https://finance.yahoo.co.jp/quote/GDDY/history?from=` — a **truncated prefix** of the GDDY
direct route from the 1st leg. The wrapper is a staging surface (a proxy indirection that
rewrites an existing target), and the embedded value stops exactly at `from=`, so the date
value itself is not carried by this artifact.

## 3. Copied source block vs. independent observation

Rule applied (machine-checked in `verify.py`):

- **Copied source block** — the later target is a truncation/prefix of a target already
  present on an earlier record, and it introduces no new retrieval surface.
- **Independent observation** — the target introduces a surface not present on any earlier
  record (different host or different URL form) and carries its own timestamp.

Applying it:

- `86be648c…` → **copied source block**. It is a `markdown.new` wrapper whose embedded value
  is a strict prefix of the GDDY route; no new surface, no date payload. Its timestamp
  (`2026-05-28T18:53:38Z`, basis `source_export_reqlog`) times the *page export*, not an
  independent retrieval of the target.
- `e960202e…` → **independent observation**, direct Yahoo Japan, `2026-05-28 16:00:41`,
  basis `raw_unzoned`.
- `5426a826…` → **independent observation**, `pure.md` epoch-window surface, contains no
  `GDDY` substring, `2026-05-28 16:49:36`, basis `raw_unzoned`.

So the pair's second leg is a genuine second surface; the `markdown.new` record is a copy of
the first leg's target wrapped in a proxy, and must not be counted as a third observation of
the pair.

## 4. What `verify.py` checks

| id | check |
| --- | --- |
| C1 | three retained records with distinct record ids |
| C2 | ordered pair `GDDY` then `TWLO` carries `from=to=20191115` |
| C3 | GDDY leg is a direct Yahoo Japan route with `from=to=20191115` |
| C4 | TWLO leg encodes the same date as a `period1`/`period2` epoch window starting `2019-11-15` |
| C5 | the staging artifact is a `markdown.new` wrapper holding a truncated copy of the GDDY route |
| C6 | TWLO leg is independent: different surface, no `GDDY` substring |
| C7 | classification separates the copied block from the independent observations |
| C8 | the two independent observations carry distinct raw timestamps |

Exit code `0` means all checks pass; `1` means at least one failed. The recorded expected
output is `verification-result.json`.

## 5. Reproduction

1. `python3 answers/34-gddy-twlo-same-date-pair/verify.py` — expect `"status": "pass"`.
2. Read `evidence/observations.json` for the three retained targets verbatim.
3. Read `evidence/pair.json` for the ordered pairing and the epoch equivalence.
4. Read `evidence/staging-artifact.json` for the `markdown.new` wrapper and its decoded prefix.
5. Read `evidence/classification.json` for the copied-vs-independent split and the criteria.

## 6. Limits

- `verify.py` is a consistency check over recorded evidence. It cannot prove that the
  upstream pages still serve these values; re-reading the retained-record endpoints and the
  Yahoo Japan / `pure.md` / `markdown.new` surfaces requires network access.
- `markdown.new/example.com` is the placeholder host used by the recorded wrapper; the
  recorded string is preserved verbatim rather than normalised.
- The TWLO window is wider than one day (`period1`..`period2`); it matches on start date only,
  which is stated explicitly rather than silently treated as identical to `from=to`.
- Timestamps are reported with the basis recorded at capture (`raw_unzoned` for the two
  van derbilt records, `source_export_reqlog` for the wiki export); no timezone conversion is
  applied here.
