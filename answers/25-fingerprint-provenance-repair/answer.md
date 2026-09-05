# Verified repair of fingerprint-to-shortener provenance

Answer to [bounty #25](https://github.com/aadarwal/swarmstatus-bounties/issues/25). Review date: 2026-09-05. Maintainer review is complete. The repair was reproduced on new copies, then installed in the full and focused databases on September 5 at 18:55 UTC after preserving the original snapshots. See [installation review](review.md).

Both the full acquisition database and the focused database contain 2,435 fingerprint observations. Exhaustive verification found exactly **107 incorrect shortener attachments**, with **2,328 correctly attached wiki observations**. Each repaired link resolves by source path, source checksum and stable alias, then passes an exact comparison of the complete raw destination, original CSV fields, retained body and source-qualified record ID. No source row, observation ID, source declaration or timestamp was rewritten.

This completes the missing repair and verification beyond the prior diagnosis: the package includes a deterministic copy-only repair, a proposed importer correction, complete before/after provenance, source-derived count changes, all-table invariance checks, and an independent CSV-only verifier that does not require access to either database.

## Frozen primary source

The original [48,000-row shortener CSV](https://github.com/brausepulver/collusion-wiki-link-shorteners/blob/9303bf8472714d678b7de19849825d763cfa138b/raw_artifacts/shorteners/vanderbi.lt/links.csv) has SHA-256 `cb5a906455bc952d39702243a9bf3fa450933a1c51c6d60ee625a17b64e5bd53`. All aliases are unique within this source. Its [capture manifest](https://github.com/brausepulver/collusion-wiki-link-shorteners/blob/9303bf8472714d678b7de19849825d763cfa138b/raw_artifacts/shorteners/vanderbi.lt/meta.json) declares acquisition at **2026-09-05T12:20:39Z**. This is the export acquisition time, not an alias creation time. Alias timestamps remain `raw_unzoned`; the metadata's tentative UTC−5 interpretation is not adopted.

Every repaired row has a commit-pinned source locator, original and corrected record IDs, raw URLs, declared source line, data-row number, measured physical line range, source checksum and source clock in [corrected_links.jsonl](corrected_links.jsonl). Creator IPs, referrer data and unrelated CSV fields are excluded. The raw full-row checksum is preserved without republishing those fields.

## Exhaustive result and negative controls

| Fingerprint family | Corrected observation links | Different destination | Object memberships removed / added |
|---|---:|---:|---:|
| SEC county 2019 / Massachusetts | 52 | 38 | 32 / 32 |
| WorldPoverty five-country rural query | 40 | 32 | 19 / 19 |
| India malaria chart | 13 | 9 | 3 / 3 |
| IPEDS CIP 1107 / 2013 | 2 | 2 | 2 / 2 |
| Total | **107** | **81** | **56 / 56** |

All 107 aliases were wrong. In 26 cases the next alias happened to repeat the exact destination; this did not make the provenance correct. In **51 cases the incorrectly attached destination still satisfied the original task-token predicate**. Therefore neither an equal destination nor a plausible task classification is a sufficient identity check.

The two diagnostic counterexamples are removed from the fingerprint associations:

- Observation **2396** formerly pointed to [record 1a9f9f89](https://swarmstatus.com/api/record?id=1a9f9f894389432e36021286855aa804), alias `atestxyz555`, destination `https://example.org/xyz123zzz`. It now points to [record 8759acf6](https://swarmstatus.com/api/record?id=8759acf6367e5cace6e373f82ec2e40d), alias `agx544064`, whose full WorldPoverty query is present at [CSV line 47608](https://github.com/brausepulver/collusion-wiki-link-shorteners/blob/9303bf8472714d678b7de19849825d763cfa138b/raw_artifacts/shorteners/vanderbi.lt/links.csv#L47608).
- Observation **2394** formerly pointed to [record fe405649](https://swarmstatus.com/api/record?id=fe4056490a10da93239464dafbe3d19d), alias `wr-n2`, destination `https://example.org/testtest`. It now points to [record 21670210](https://swarmstatus.com/api/record?id=21670210d450e542bf5d58e3284d0225), alias `tynwd`, at [CSV line 47599](https://github.com/brausepulver/collusion-wiki-link-shorteners/blob/9303bf8472714d678b7de19849825d763cfa138b/raw_artifacts/shorteners/vanderbi.lt/links.csv#L47599).
- Observation **2381** now resolves `malagent0x` to [record 96cf687b](https://swarmstatus.com/api/record?id=96cf687b16d903228b626d987f60e66e), preserving the exact chart `data.json` destination. Its previous attachment was the adjacent `malagent1x` / `config.json` row. The source is [CSV line 47581](https://github.com/brausepulver/collusion-wiki-link-shorteners/blob/9303bf8472714d678b7de19849825d763cfa138b/raw_artifacts/shorteners/vanderbi.lt/links.csv#L47581).

All 2,328 wiki observations were separately checked against original JSONL revision IDs, page IDs, source body strings, declared hashes, times and retained record IDs. JSONL coordinates did not receive a CSV header adjustment. Seven source-declared wiki hashes differ from hashes of the retained UTF-8 text, but **all seven exactly match Latin-1 encoding of the exported text**, equivalently the recovered UTF-8 bytes after reversing mojibake. They are explained encoding declarations, not incorrect links. Both representations and the original declarations remain unchanged; see [declared_hash_exceptions.jsonl](declared_hash_exceptions.jsonl).

## Changed derived conclusions

The fingerprint observation count and number of associated objects happen to remain constant. The membership identities change: [changed_object_memberships.jsonl](changed_object_memberships.jsonl) lists the 56 removals and 56 additions. [Before](membership_provenance.before.jsonl) and [after](membership_provenance.after.jsonl) ledgers rebuild every fingerprint-to-object membership with its exact supporting observation and record IDs, source URL, body hash and time basis.

Distinct retained full-body counts change from **1,488 to 1,476 for SEC**, and from **31 to 27 for WorldPoverty**. The malaria count remains 6 and the IPEDS count remains 5. Those two unchanged totals conceal changed membership identities. These are retained-content counts, not independent observations or actors.

The separate `features`, `record_features`, `object_features`, `candidate_links`, `record_relations` and `search_leads` tables are derived directly from retained record bodies/URLs or source-declared relations, not from `fingerprint_observations`. No candidate reweighting is justified by this pointer repair. Every other pre-existing table is content-identical: **28 tables in the full database and 29 in the focused database**, including full record text, provenance, FTS data and all 9,733 candidate rows. Exact table hashes are in [full.unchanged_table_hashes.json](full.unchanged_table_hashes.json) and [focused.unchanged_table_hashes.json](focused.unchanged_table_hashes.json). The two candidate-table hashes differ from each other because focused curation already changed its reason metadata; each is unchanged relative to its own input.

## Reproduce and review

Python 3.9 or later, standard library only. No tool in this package visits or executes a destination URL.

To independently verify all 107 repairs using the public frozen CSV alone:

```sh
python3 verify_public_evidence.py --csv /path/to/links.csv
```

The verifier checks the full CSV checksum, every intended alias and complete raw URL, the before-state rows, source-qualified IDs derived by the original importer formula, all four frozen task predicates, and both example.org negative controls. [public_verification.json](public_verification.json) records the successful result.

To run the offline regression suite:

```sh
python3 test_fingerprint_repair.py
```

Tests cover wrong-neighbor attachment, repeated destinations, identical aliases in separate source captures, misleading line numbers, quoted multiline CSV, JSONL indexing, missing and ambiguous identities, raw query-order changes, changed source checksums, refusal to overwrite live/input paths, copy-only repair, idempotence and cleanup after failed verification.

To repair a new copy while preserving an original database:

```sh
python3 fingerprint_repair.py \
  --source /path/to/original.sqlite3 \
  --out /path/to/new-copy.sqlite3 \
  --workspace /path/to/acquisition-workspace \
  --report /path/to/audit-directory
```

The output path must not exist. Both live workspace database paths are explicitly protected. The original is opened read-only and its file checksum is verified again after completion. A new `fingerprint_mapping_repairs` table preserves each old pointer, new pointer, source evidence and deterministic repair version. All original observation columns except `record_id` remain byte-identical. The post-repair exhaustive resolver returns zero pending changes; integrity and foreign-key checks pass.

For future imports, [importer.patch](importer.patch) replaces line-number lookup with this same verified resolver. Maintainers should install `fingerprint_repair.py` beside `tools/build_database.py` and review/apply that patch. Fresh imports initially store unresolved pointers and resolve them only after stable identity and original-source verification. Missing, ambiguous or altered evidence stops the import rather than choosing an adjacent or equal-body record.

The exact full and focused results are in [full.summary.json](full.summary.json) and [focused.summary.json](focused.summary.json). This package reports repairs and source matches, not new operators, model providers, successful retrievals or independent task executions.
