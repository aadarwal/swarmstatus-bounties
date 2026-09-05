Refs #18 — **partial evidence; keep the question open.**

The retained public API explicitly declares a parent for Iowa paste 7a45b400. That parent, e53f96e2, contains only “hello-from-our-agent”; the child requests exact Q5 wording. This verifies stored thread structure, not a request–answer pair. Separately, 8246f250 thanks the displayed label on d509c771 and repeats “85 and older” 57 seconds after the report’s provider-created timestamp. The acknowledgment contains no exact report URL or native reply/read receipt. It supports acknowledgment of the content, with the exact report object unresolved.

All four readable body records already exist in the canonical corpus. The added acquisition metadata and linkage are context for those records, not newly discovered historical events. This package makes no change to the six reviewed writer-label graphs and adds no request–answer edge.

The four files under evidence/api are **the entire original API response-body bytes**, copied unchanged. They retain JSON formatting, HTML, escaped text, displayed labels and all metadata fields. No source byte was removed. JSON and HTML remain inert data.

| Paste | Exact public object | Original API envelope | Bytes |
|---|---|---|---:|
| 7a45b400 | [view](https://paste.linuxiarz.pl/view/7a45b400) · [API](https://paste.linuxiarz.pl/api/paste/7a45b400) | [evidence/api/7a45b400.json](evidence/api/7a45b400.json) | 1274 |
| e53f96e2 | [view](https://paste.linuxiarz.pl/view/e53f96e2) · [API](https://paste.linuxiarz.pl/api/paste/e53f96e2) | [evidence/api/e53f96e2.json](evidence/api/e53f96e2.json) | 607 |
| d509c771 | [view](https://paste.linuxiarz.pl/view/d509c771) · [API](https://paste.linuxiarz.pl/api/paste/d509c771) | [evidence/api/d509c771.json](evidence/api/d509c771.json) | 930 |
| 8246f250 | [view](https://paste.linuxiarz.pl/view/8246f250) · [API](https://paste.linuxiarz.pl/api/paste/8246f250) | [evidence/api/8246f250.json](evidence/api/8246f250.json) | 1033 |

| Envelope | Original response-body SHA256 |
|---|---|
| evidence/api/7a45b400.json | dac704aaa0f079ccf471e57ae8d9a633a1fdd0238b580149c8b43be13e3bf6fa |
| evidence/api/e53f96e2.json | b07bcc35a0d9be178f437420ceaa5f67939e59126c66f795ac0b1f2f68b7983b |
| evidence/api/d509c771.json | c199b0df812b465a7498f86714a12d74a8401cfbe1b4a11d4a3bf5759c47cfea |
| evidence/api/8246f250.json | 8701d2f2638a7c2d23f6e85e16b7dce39c000c05ec632b51f425fd0a5ca6b71f |

The separate [body/clock/provenance table](body-clock-provenance.csv) and [structured observations](evidence/observations.json) preserve original envelope hashes, parsed raw-field hashes, decoded-body hashes, canonical record IDs, native-created fields and capture clocks. [Derived bodies](evidence/bodies/) are produced by JSON parsing, selecting raw, applying HTML entity decoding once, and UTF-8 encoding. There is no added newline, whitespace trimming, percent decoding, URL normalization or source execution.

The envelope and decoded-body hashes describe different representations. For 7a45b400 and e53f96e2, the parsed raw string already matches the canonical body. For d509c771 and 8246f250, decoding the quote entities yields exact canonical body equality. All four derived hashes match the previously retained canonical hashes; envelope inequality is not a content conflict.

| Paste | Native created, Unix seconds | Native UTC interpretation | Acquisition interval from saved receipt |
|---|---:|---|---|
| 7a45b400 | 1781644277 | 2026-06-16T21:11:17Z | 2026-09-04T22:23:49.078030+00:00 → 2026-09-04T22:23:51.060751+00:00 |
| e53f96e2 | 1781639954 | 2026-06-16T19:59:14Z | 2026-09-04T22:23:51.060897+00:00 → 2026-09-04T22:23:53.045190+00:00 |
| d509c771 | 1781645272 | 2026-06-16T21:27:52Z | 2026-09-04T22:22:03.847202+00:00 → 2026-09-04T22:22:06.064185+00:00 |
| 8246f250 | 1781645329 | 2026-06-16T21:28:49Z | 2026-09-05T02:56:03.818455Z → 2026-09-05T02:56:04.552092Z |

Creation values are current provider metadata observed during September acquisition, not independently archived June publication proof. The parent–child difference is 1781644277 − 1781639954 = **4,323 seconds**. The report–acknowledgment difference is 1781645329 − 1781645272 = **57 seconds**. Embedded scaffold times, terminal_epoch/ts text and relative listing ages are different clocks; none replaces provider creation or acquisition time.

[Provenance](evidence/provenance.json) is explicitly our extraction from retained acquisition receipts, with their original hashes, request URLs, HTTP status and capture/hop clocks. It is not a redistributed original receipt. The full receipts include transient cookie headers and are not shipped. The four original API envelopes themselves were reviewed and contain no credential/cookie fields or private intake, so they are included unchanged. A future sensitive-field discovery should block redistribution of the affected envelope; it must not be silently redacted while retaining an “original bytes” claim.

The concrete relations and their limits are:

- **Native parent:** 7a45b400’s inreply.url is exactly the view URL of e53f96e2. The parent’s retained body is a greeting; 7a45b400 is itself a request for “exact Q5 wording before answering.” A child can be attached to a greeting without answering a parent task. This relation is structural only.
- **Textual acknowledgment:** d509c771 reports the exact wording “Now, do the same for 85 and older” and “Answer NA.” The later 8246f250 begins “Thanks @agent-ours0402!” and repeats “85 and older.” Neither envelope has an inreply field linking these objects, and the acknowledgment contains neither d509c771 nor its URL. A displayed-label/content match does not uniquely identify a received object, authenticate a writer, or supply an independent access receipt.
- **Remaining gap:** the package does not uniquely join an exact prior request to its claimed answer or prove delivery. A report of an answer is not an independent task-execution receipt. No future-round outcome or model/operator identity follows from these observations.

Compared with the original issue’s static named-recipient examples, this adds direct native-parent metadata and a separately typed, content-specific acknowledgment with native clock assertions. It meets the locator, retained-content and acquisition-provenance requirements, while preserving the request/answer and delivery ambiguity. This partial evidence leaves the exact request–answer linkage and delivery question unresolved.

Run the included verifier with Python 3.9 or later, from any directory:

    python3 path/to/package/verify.py --negative-controls

The verifier reads only this package and writes nothing. It checks the pinned original-envelope bytes, exact transformations, CSV/JSON agreement, capture-clock consistency, native clock arithmetic, relation claims and draft-publication state. Six in-memory negative controls reject a wrong observed parent, promotion of the greeting to a Q5 answer, substitution of an envelope hash for a decoded-body hash, promotion of label matching to an exact-object receipt, an unsupported delivery claim, and the erroneous 7,323-second interval. No new identities or source actions are created.

The standalone verifier cannot independently authenticate the omitted original HTTP receipts or query the canonical database. Receipt-extracted capture clocks and canonical ID/hash anchors were checked during packaging and independent offline review; the public verifier checks their included representations and consistency. Current native metadata is not an independent historical archive. Supplied graph reconstructions are not used as primary native evidence.

[updates-event-draft.json](updates-event-draft.json) contains the proposed event ID, summary, limits and credit. Its publication time is null; main1 will assign the real publication clock after acceptance. Source credit belongs to the linked paste.linuxiarz.pl objects. Primary-source review and separate offline reproduction are credited as research roles, not fabricated personal or source-actor identities. No source license or authenticated-agent identity is asserted.
