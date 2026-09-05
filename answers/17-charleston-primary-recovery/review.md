# Public evidence review — 5 September 2026

**Pass for publication as the maintainer-supplied answer to #17.** Reviewed all seven evidence files, the README, source identities, clocks, and verification scope.

- No unrelated report metadata, IP addresses, browser headers, credentials, wallet data, or actual local filesystem paths are included. Paths within the evidence are package-relative; the README's external-cache path is a generic example.
- Both literal institutional manifests match the packaged hashes. The exact 5,484-byte `lcdl129141JPEG1jpg` body identifies *View in Magnolia Cemetery*, image service `205927`. The nearby `lcdl129143JPEG1jpg` body identifies *View on South Battery*, image service `205929`.
- The current exact body matches two historical provider-reported response hashes and sizes. Historical inline response bodies remain absent. Catalog Date `1893`, recorded requests, provider report dates, and current acquisition clocks are kept separate. The public date-basis description says “provider report date,” without assuming report-processing semantics.
- The current wildcard response is empty and cannot supply a readable object identity. Historical fallback behavior remains undecidable. No actor, task-execution, copying-direction, or staging-source inference is made.
- The README correctly credits the new recovery separately from PR #35's submitted head and explains the limitations of omitted original provider reports.

Final standalone verification: **PASS**, seven evidence files, two historical reported-hash matches, distinct nearby control, empty wildcard control, and all six negative controls rejected.

Final verification against the three retained original compressed provider JSON files: **PASS**. Original hashes and the minimal extracted report/request/response fields match. The originals were read as inert local bytes; no payload or embedded resource was executed or fetched during verification.
