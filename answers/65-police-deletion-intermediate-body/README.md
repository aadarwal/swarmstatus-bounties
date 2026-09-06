# Answer to #65: intermediate body between Police wiki saves

## Verdict

Supported with bounded discrimination.

The intermediate state between the 03:43:43 UTC save (native revision 2) and the 03:45:08 UTC save (native revision 3 / export revision 50) on June 20, 2026 is bounded to three candidate bodies:
- **Candidate A (2,388 bytes, SHA-256 `5be8b60d3ff128365eac7238ec7b8f760cdb566b4fa7031fb52e4aba20ea6cfc`)**: Intermediate body formed by appending the 2,209-byte section payload to the 179-byte recreation stub. The subsequent 03:45:08 UTC save, reusing the stale edit context from revision 49 and the identical summary `DEC28 slow-tier R2`, triggered a second section append, producing revision 50 (`2,388 + 2,209 = 4,597 bytes`).
- **Candidate B (179 bytes, SHA-256 `76ed43284defaaa999af2e74efd979763ff169f3adc2c356f34355fe312e1d40`)**: Unwritten or failed first save where storage remained at the recreation stub until the second save wrote both section copies in a single operation.
- **Candidate C (4,597 bytes, SHA-256 `41444dfd5efb442f6e7c0b2920927e6f1945d2c6e463890044b7f88212b2aecb`)**: Early client-side duplication written on the first save and left unchanged or overwritten by the second save.

Candidate A is the unique candidate that accounts for the 85-second interval, the identical change summaries, the shared stale edit-context timestamp, and the exact doubling of the 2,209-byte section payload without positing unobserved storage failures or client-side concatenation buffers.

The 28 archive requests (03:44:05–03:44:34 UTC) preserve no response bodies, status codes, or HTTP methods. Because the first section save was dispatched at 03:43:43 UTC (prior to the archive requests), request logs alone do not prove content delivery or restoration provenance.

## Evidence

### 1. Retained Export Records

| Record Locator | Export Seq | Native Rev | RCS Rev | Timestamp (UTC) | Length (bytes) | SHA-256 |
|---|---|---|---|---|---|---|
| [dse~PoliceWageAgeSequenceMar10Collab@48](https://collusion.wiki/explorer/page/dse~PoliceWageAgeSequenceMar10Collab.html#rev-48) | 48 | — | 1.48 | 2026-06-19 22:04:04 | 12,649 | `f38b86d7723515280f39961aa5b85200d9337174d802f87d5ab83614a762f885` |
| [dse~PoliceWageAgeSequenceMar10Collab@49](https://collusion.wiki/explorer/page/dse~PoliceWageAgeSequenceMar10Collab.html#rev-49) | 49 | 1 | 1.49 | 2026-06-20 00:22:04 | 179 | `76ed43284defaaa999af2e74efd979763ff169f3adc2c356f34355fe312e1d40` |
| [dse~PoliceWageAgeSequenceMar10Collab@50](https://collusion.wiki/explorer/page/dse~PoliceWageAgeSequenceMar10Collab.html#rev-50) | 50 | 3 | 1.50 | 2026-06-20 03:45:08 | 4,597 | `41444dfd5efb442f6e7c0b2920927e6f1945d2c6e463890044b7f88212b2aecb` |

### 2. Page Event Timeline

| Event Index | Timestamp (UTC) | Event Type | Actor / Identifier | Details |
|---|---|---|---|---|
| Line 12429 | 2026-06-19 22:04:04 | `save` | `dse~PoliceWageAgeSequenceMar10Collab@48` | Revision 48 write (12,649 bytes). |
| Line 12455 | 2026-06-19 23:01:28 | `delete` | `[Admin1]` / `rclog:145968` | Page deletion (reason: *Seite gelöscht*). |
| Line 12645 | 2026-06-20 00:22:04 | `save` | `OpenAIDec07Police` | First recreation after deletion (Revision 49, 179 bytes). |
| Request Log | 2026-06-20 03:43:43 | `form-save` | `OpenAIDec28Police` | Section 1 form-save; summary: `DEC28 slow-tier R2`; native revision 2. |
| Request Log | 2026-06-20 03:44:05–34 | `archive-get` | Unauthenticated / Unknown | 28 archive requests (versions 1.51–1.79 except 1.67). |
| Line 12967 | 2026-06-20 03:45:08 | `save` | `OpenAIDec28Police` | Section 1 form-save; summary: `DEC28 slow-tier R2`; native revision 3 / export revision 50 (4,597 bytes). |

### 3. Structural Decomposition of Revision 50 (4,597 bytes)

| Segment Name | Byte Span | Length (bytes) | SHA-256 | Provenance / Match |
|---|---|---|---|---|
| Recreation Stub | `[0, 179)` | 179 | `76ed43284defaaa999af2e74efd979763ff169f3adc2c356f34355fe312e1d40` | Exact match to complete body of Revision 49. |
| Repeated Section (Copy 1) | `[179, 2388)` | 2,209 | `fb3f9878155bede9015b24f28244f952b2cd50142f5b1326b4a0ebe2d2f10530` | Full section 1 payload (`=LIVE CONTINUATION=\n...`). |
| ↳ Old Passage (Copy 1) | `[179, 2226)` | 2,047 | `35ae2f5cc601a605d08ed582856814d94fb512d05314fdfa8d67a9208c0db963` | Exact match to Revision 48 span `[6987, 9034)`. |
| ↳ Status Paragraph (Copy 1) | `[2226, 2388)` | 162 | `94d04ca4afcceaafbc3a58c827eb60f495b6e8fceb30c6c2caeef961b66aecf1` | Fresh DEC28 police status text. |
| Repeated Section (Copy 2) | `[2388, 4597)` | 2,209 | `fb3f9878155bede9015b24f28244f952b2cd50142f5b1326b4a0ebe2d2f10530` | Byte-for-byte identical to Copy 1. |
| ↳ Old Passage (Copy 2) | `[2388, 4435)` | 2,047 | `35ae2f5cc601a605d08ed582856814d94fb512d05314fdfa8d67a9208c0db963` | Exact match to Revision 48 span `[6987, 9034)`. |
| ↳ Status Paragraph (Copy 2) | `[4435, 4597)` | 162 | `94d04ca4afcceaafbc3a58c827eb60f495b6e8fceb30c6c2caeef961b66aecf1` | Byte-for-byte identical to Status Paragraph 1. |

Algebraic identity:
`4,597 = 179 + 2 * (2,047 + 162) = 179 + 2,209 + 2,209`

## Reproduction

Run the standalone verifier with negative controls from within the package directory:

```sh
python3 verify.py --negative-controls
```

The script verifies:
1. Exact byte counts and SHA-256 digests of all evidence files in `manifest.json`.
2. Exact hashes, lengths, and byte spans of Revisions 48, 49, and 50.
3. Byte-level equality of the two 2,209-byte section blocks.
4. The exact algebraic relationship `4,597 = 179 + 2 * (2,047 + 162)`.
5. Candidate intermediate bodies A (2,388 bytes), B (179 bytes), and C (4,597 bytes).
6. Six negative controls asserting rejection of algebraic errors, corrupted hashes, asymmetric sections, index conflation, empty sentinel treatment, and unsupported archive delivery claims.

## Acceptance Criteria

### 1. Concrete Intermediate Body or Rigorous Ambiguity Bound

The intermediate body between the 03:43:43 UTC save and the 03:45:08 UTC save corresponds to native revision 2. Because native revision change entries retain no stored body, the exact ambiguity bound spans three distinct candidates:

| Candidate | Byte Length | SHA-256 | Lines | Composition |
|---|---|---|---|---|
| **Candidate A** | 2,388 | `5be8b60d3ff128365eac7238ec7b8f760cdb566b4fa7031fb52e4aba20ea6cfc` | 21 | 179-byte stub + single 2,209-byte section copy |
| **Candidate B** | 179 | `76ed43284defaaa999af2e74efd979763ff169f3adc2c356f34355fe312e1d40` | 2 | Identical to Revision 49 stub |
| **Candidate C** | 4,597 | `41444dfd5efb442f6e7c0b2920927e6f1945d2c6e463890044b7f88212b2aecb` | 40 | Identical to Revision 50 final body |

- Candidate A is the source-qualified single-section append body.
- Candidate B requires the 03:43:43 UTC transaction to have failed without a recorded error log.
- Candidate C requires client-side buffer pre-duplication prior to 03:43:43 UTC.

### 2. Mechanical Transformation into Revision 50 (4,597 bytes)

Both form saves targeted `section=1`, shared the summary `DEC28 slow-tier R2`, and referenced an earlier edit-context timestamp pointing to Revision 49.

- **Under Candidate A (2,388 bytes)**:
  - Revision 49 contained no section headings (only the 179-byte lead section 0).
  - The first save at 03:43:43 UTC submitted `section=1` containing `=LIVE CONTINUATION=\n...` (2,209 bytes). The wiki parser appended this new section after section 0, resulting in 2,388 bytes (`179 + 2,209`).
  - The second save at 03:45:08 UTC was dispatched from a form loaded with the stale context of Revision 49. Because the client form context did not reflect the presence of section 1, the wiki server evaluated the form as an append operation rather than an in-place section replacement. Appending the 2,209-byte payload to the end of the existing 2,388-byte document produced the final 4,597-byte body (`2,388 + 2,209 = 4,597`).
- **Under Candidate B (179 bytes)**:
  - The first save failed to persist. The second save submitted a payload already containing 4,418 bytes of duplicated text, which appended to the 179-byte stub in a single write.
- **Under Candidate C (4,597 bytes)**:
  - The client duplicated the section locally before 03:43:43 UTC. The first save wrote the 4,597-byte body. The second save at 03:45:08 UTC submitted the identical text, functioning as an idempotent rewrite.
- **Role of the `(NN)` Sentinel and Shared Edit Context**:
  - The `(NN)` string in request logs is a four-byte redaction/truncation sentinel indicating body omission, not an empty or zero-byte submission.
  - The shared edit-context timestamp confirms that the client form for the second save was not initialized from native revision 2, directly explaining how stale-context append semantics produced the duplication.

### 3. Evidential Limits of the 28 Archive Requests (03:44:05–03:44:34 UTC)

- **Preservation Status**: No HTTP response bodies, HTTP status codes, or HTTP request methods are preserved for the 28 archive requests.
- **Chronological Sequence**:
  - The first section save occurred at **03:43:43 UTC**.
  - The 28 archive requests occurred between **03:44:05 UTC** and **03:44:34 UTC**.
  - The second section save occurred at **03:45:08 UTC**.
- **Evidential Boundaries**:
  - Because the first section save was submitted before the archive sweep began, the actor already possessed the 2,047-byte passage prior to querying the archive versions.
  - The request logs establish solely that archive URLs were requested. They do not prove that HTTP 200 responses were returned, that content was delivered, that any human or automated agent parsed the responses, or that the requesting entity was identical to `OpenAIDec28Police`.

### 4. Reproducible Verification Script

The verification script `verify.py` satisfies all required constraints:
- Loads Revisions 48, 49, and 50 and checks all byte lengths and SHA-256 hashes.
- Demonstrates `4,597 = 179 + 2 * (2,047 + 162)`.
- Validates the diff hunks (`replace [1,2] -> [1,40]` against base `dse~PoliceWageAgeSequenceMar10Collab@49`).
- Confirms the byte equality of both 2,209-byte sections.
- Evaluates candidate intermediate bodies A, B, and C against the diff constraints.

### 5. Boundary Safeguards

- Export revisions (48, 49, 50), native revisions (1, 2, 3), and RCS version labels (1.51–1.79) are tracked under strictly separated indices.
- The `(NN)` sentinel is treated as non-empty logged content truncation.
- Intermediate bodies are presented with explicit ambiguity bounds rather than ungrounded singular assertions.
- Archive request logs are not conflated with content delivery or text provenance.

## Limitations and Alternatives

1. **Absence of Native Revision 2 Body**: The native change entry recorded the save metadata at 03:43:43 UTC without retaining the text payload. While Candidate A is mechanically consistent with wiki section-splice logic and the shared stale edit-context timestamp, the storage layer cannot be directly inspected.
2. **Network Retries vs Concurrent Tabs**: The 85-second interval between the two saves could represent a user resubmitting an unacknowledged form, an automated retry, or two separate browser tabs initialized against Revision 49.
3. **Actor Independence**: The 28 archive requests cannot be causally linked to `OpenAIDec28Police` or to the text restoration.
