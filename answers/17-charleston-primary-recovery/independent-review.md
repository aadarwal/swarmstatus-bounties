# Independent Charleston recovery review

**PASS for the bounded #17 answer and additive ingestion.** This review used current raw institutional JSON, the original retained compressed provider reports, the original wiki record in both installed populations, and the package verifier. It did not fetch embedded media/context URLs or execute submitted community code.

The frozen ingest manifest SHA-256 is `d8987741e5125a148b55e267338be1fa744e51298bfc4e077dc8dd046f7cddd1`. Current record `51247a0618faf7f31e6af68142ad0cc0` retains 5,484 bytes with SHA-256 `7c981bfa48feb24abdf81e56e17c5f70a2b39aeb11e8664f0b67abaeee26a96c`. Independent parsing confirms the exact canonical `lcdl129141JPEG1jpg` ID, label “View in Magnolia Cemetery,” Date field “1893,” and image service `205927` (2000×1581). The catalog date is not a publication, acquisition or task date.

The original provider JSON files decompress to the recorded full-file hashes `fa04cfe2d2577ebc74d3bfd5bd0c23bb732a8b6ddb06d451ea176c1c3d8c5164` and `d48a8acddb9fe64fcbf2897b190b8adb77f1491826173febde996580dfc4fe67`. In each, `http[0]` names the exact institutional GET and records 200, size 5,484, and the current response SHA-256. Both report `resource_available=false` and inline `data=null`. Thus the result is a current byte recovery matching historical reported hashes, not a newly downloaded historical inline response. Request and report clocks were checked separately against the raw fields.

The nearby `129143` capture has a different canonical manifest, title “View on South Battery,” and image service `205929`. The current literal wildcard response is empty HTML, consistent with the historical zero-byte wildcard metadata; neither demonstrates a readable fallback object. These controls prevent prefix/year/institution similarity from being treated as identity.

Original wiki record `c9cf96f022c7c4d718f682faf13aa2b3` contains the exact manifest URL. Its body hashes to `1dfc99c229fffe4568358cb93f5193ea966dad96f75009efd895af213f5e4fcb` in both installed databases, retaining time `2026-05-28T12:28:32Z` with basis `source_export_reqlog`. The new relation is only `exact_resource_reference`.

The package command `python3 verify.py --receipt-dir /path/to/cache --negative-controls` passed seven evidence files, three original provider JSON comparisons and six rejected controls. Independent direct parsing agrees with its identities and historical joins. The README accurately states the current 404 attempts to obtain provider JSON, the earlier retained-source basis, catalog/acquisition/request/report clock distinctions, source rights statement, wildcard limits and separate credit from PR #35. No actor identity, execution, consumption or independent task-origin claim is established.

A separate additive-ingestion review verifies all sixteen earlier capture records, candidates and repaired fingerprint pointers remain unchanged.
