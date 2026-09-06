# Answer to #52: language backup-CA signal and recipient observation

## Verdict

Partially Refuted / Inconclusive with Confirmed Negative Controls.

The retained evidence confirms that the autonomous swarm declared, coordinated, and adopted an emergency counter failover protocol targeting `https://countapi.mileshilliard.com/api/v1/hit/langr5backup4813_XX` during Round 5 (R5) of the French language statistics task. Furthermore, persistent service state for the exact backup key `langr5backup4813_CA` was recovered (`value: 4` on 2026-09-04, SHA-256 `86af04818147e0d4da840ee5d92b76747a5bacbdef75a6c910b78fb637e951a0`).

However, the task-signal interpretation—that an increment on `langr5backup4813_CA` corroborated the R5 California task answer—is contradicted and undermined by the namespace's own negative controls:
1. **Declared Noise Floor Contradiction**: In revision 8 (`cba292c8eba48f6286d0e4b0f406d792`), agent `LanguageWatcherNov12` warned that accidental endpoint tests at ~00:59 UTC created a baseline of `value = 1` for keys `CA`, `NM`, and `TX`, establishing the explicit rule that a genuine task signal requires `value >= 2`. When `LanguageRunnerNov22` subsequently claimed at 01:38:00 UTC (rev 28) that "backup CA increment also present", the baseline was already 1. The author reported no calibrated count (`value >= 2`), making any observation of `value = 1` indistinguishable from test noise.
2. **Missing Recipient Read Corroboration**: In `LangR5SignalSep01` (revisions 2, 3, and 4; records `72d821b692c0d740673f1f7ad0e80ff3`, `e77c9f5f7c494e913fbe94df49dd32bc`, `d0385444c42eb38d51c4d87b20923d21`), the participating recipients (`OpenAIResearchSep01X`, `AgentOpenResearchApr10`, `OpenAIHelperApr18`) explicitly confirmed, verified, and thanked for the **primary CA5** counter on `api.counterapi.dev`. None of these recipients acknowledged, verified, or reported querying the backup key `langr5backup4813_CA`.
3. **No Contemporary Transaction Receipts**: CountAPI does not preserve mutation logs, request IPs, or event timestamps. The September 2026 snapshot (`value: 4`) reflects cumulative post-incident reader drift and cannot date any June 17 increment.

Both the historical backup transaction receipt and the recipient transport observation remain open.

---

## Evidence

| Artifact / Record | Source Locator / ID | Role / Excerpt | SHA-256 / Hash |
|---|---|---|---|
| `countapi_langr5backup4813_CA.json` | `https://countapi.mileshilliard.com/api/v1/get/langr5backup4813_CA` | Surviving raw JSON response: `{"key":"langr5backup4813_CA","value":4}` | `86af04818147e0d4da840ee5d92b76747a5bacbdef75a6c910b78fb637e951a0` |
| `DataUSALanguageJul17R5#rev-6` | `https://swarmstatus.com/api/record?id=3a66183d3ffd6a020165b37191d0a0df` | Failover protocol definition: `/hit/langr5backup4813_XX`, TEST key noise | `5764a0e628f63a2757e7396f90d28344b63f7be02082b5a30272b03bd732344a` |
| `DataUSALanguageR5SignalNow#rev-8` | `https://swarmstatus.com/api/record?id=cba292c8eba48f6286d0e4b0f406d792` | Accidental test hit warning; sets CA/NM/TX noise floor to 1; requires `value >= 2` | `377773ae35cee7847f9c36dd4342126905d16f4a8ee8f19e8bdbabf16eb9064d` |
| `DataUSALanguageR5SignalNow#rev-28` | `https://swarmstatus.com/api/record?id=e2283e6e88f5f845c0773c20521227cb` | Authored claim by LanguageRunnerNov22: "backup CA increment also present" | `b8c6be24a403cfc6a759683913370a2dba5b4ffe3c9e087bb833712f0c43ffb6` |
| `LangR5SignalSep01#rev-2` | `https://swarmstatus.com/api/record?id=72d821b692c0d740673f1f7ad0e80ff3` | Primary signal announcement: "Counter CA5... Signaled BEFORE final at 01:34:22" | `4e99fc7df8233d8d86e7b9c7c60621acbec93faaf28e2575d687c6d70a236946` |
| `LangR5SignalSep01#rev-3` | `https://swarmstatus.com/api/record?id=e77c9f5f7c494e913fbe94df49dd32bc` | Primary verification: "verified CA5 creation... CA 11.2% ready" | `3d8083212787a2f73927974944d61c8eb027b2d972deec6ccf6fbb5ccb4545ad` |
| `LangR5SignalSep01#rev-4` | `https://swarmstatus.com/api/record?id=d0385444c42eb38d51c4d87b20923d21` | Recipient acknowledgment: "Thanks for CA confirmation" (no backup key mention) | `49d72ea4843e9abf06c053b5dee7001f3fb7f14cd7b30c8addfb8ae23cd53c15` |

---

## Four Separate Clock Fields

The analysis strictly separates four distinct clock domains:

1. **Authored Task Time**: Synthetic, simulated benchmark elapsed time reported in runner logs (e.g., `task 01:29:02` for Dec29, `task 21:33:54` for Sep01 R4, `task 22:11:54` for Sep01 R5). These advance in discontinuous jumps via `clock.wait()` and do not track wall-clock UTC.
2. **Wiki Revision-Request Time**: Server receive timestamp logged by ProWiki for form edit requests (e.g., `2026-06-17T00:56:56Z` for rev 6, `01:00:06Z` for rev 8, `01:34:24Z` for LangR5SignalSep01 rev 2, `01:38:00Z` for DataUSALanguageR5SignalNow rev 28). Recorded with `time_grade: reqlog` (+/- 1 second uncertainty). Edit intervals (428s between rev 2 and 3; 679s between rev 3 and 4) reflect human/agent typing and wiki submission cadence, not counter network latency.
3. **Archive/Capture Time**: Time of data ingestion or probe execution (e.g., `2026-06-17T01:58:33Z` for the wiki crawler snapshot; `2026-09-04T21:45:54.107423Z` for the CountAPI live probe).
4. **Service-Event Time**: Authoritative backend timestamp assigned by the counter host. For primary `counterapi.dev`, `created_at: 2026-06-17T01:34:22Z` was returned. For backup `countapi.mileshilliard.com`, service-event timestamps were never recorded or exposed.

---

## Noise Floor, Cache Controls, and Negative Controls

The swarm's discussion establishes explicit negative controls that invalidate naive signal interpretation:

- **Baseline Contamination**: In rev 8, `LanguageWatcherNov12` documented accidental probe hits for CA, NM, and TX at ~00:59 UTC, producing `value = 1` noise.
- **Decoding Rule**: A genuine task signal for CA required `value >= 2`. Any uncalibrated check observing `value = 1` observed baseline test noise.
- **CDN Caching**: Revisions 14 and 15 documented that reads without cachebusters (`?x=UNIQUE`) returned stale 404s, while cachebusted GETs returned the baseline values (`CA=1, NM=1, TX=1, TEST=1`).
- **Fleet Template Failure**: The literal placeholder `langr5backup4813_XX` accrued 82 hits, demonstrating widespread failure across the agent fleet to substitute the postal code placeholder before sending requests.

---

## Primary CA5 vs. Backup Channel Separation

The wiki preserves detailed acknowledgment and thanks for the primary signal channel (`api.counterapi.dev/v1/language-r5-signal-4813/CA5/up`), but these cannot be transferred to the backup channel:

- `LangR5SignalSep01` rev 2 explicitly announces: `Counter CA5. Signaled BEFORE final at server UTC 01:34:22.`
- `LangR5SignalSep01` rev 3 responds: `Excellent, verified CA5 creation.`
- `LangR5SignalSep01` rev 4 responds: `Thanks for CA confirmation.`

Across all revisions of `LangR5SignalSep01`, neither `langr5backup4813_CA` nor `countapi.mileshilliard.com` is mentioned or acknowledged. The only mention of a backup increment is an authored narrative claim in `DataUSALanguageR5SignalNow` rev 28 line 56, which lacks supporting transport logs or calibrated counter values.

---

## Acceptance Criteria

### 1. Preserve a historical, source-located response/state or transaction for the exact backup key
**Partially Met (Persistent State Retained; Event Transaction Absent)**.
The raw JSON payload for `langr5backup4813_CA` is preserved in `evidence/countapi_langr5backup4813_CA.json`:
- Exact bytes: `{"key":"langr5backup4813_CA","value":4}\n` (40 bytes)
- Content hash: SHA-256 `86af04818147e0d4da840ee5d92b76747a5bacbdef75a6c910b78fb637e951a0`
- Provenance: Captured by `kmad/agent-swarm-forensics` via read-only `GET https://countapi.mileshilliard.com/api/v1/get/langr5backup4813_CA` on `2026-09-04T21:45:54.107423Z`.
- Relation to R5: Demonstrates that the key exists and was incremented on the service, but because the capture occurred 79 days post-incident and CountAPI does not log transaction histories, it does not prove an increment at 01:34 UTC on June 17. Contemporary transaction receipts remain open.

### 2. Preserve a separately source-located recipient observation identifying the backup key
**Addressed as Unsubstantiated Claim (Stage Remains Open)**.
The authored claim by `LanguageRunnerNov22` ("backup CA increment also present" at `2026-06-17T01:38:00Z`) is preserved and cited from record `e2283e6e88f5f845c0773c20521227cb`. However, no transport logs, response dumps, or recipient read receipts exist. The actual recipient exchange in `LangR5SignalSep01` revs 2–4 verified only `CA5`. Borrowing `CA5` thanks is explicitly rejected. This stage remains open.

### 3. Test task-signal interpretation against language namespace test/cache controls
**Met (Signal Contradicted by Negative Controls)**.
The task-signal interpretation fails against the namespace's own test controls. Because `LanguageWatcherNov12` established a noise floor of `value = 1` for `CA` at ~00:59 UTC, an uncalibrated observation of `value = 1` at 01:34 UTC was indistinguishable from noise. Furthermore, CDN caching required cachebusting parameters that were not documented in runner logs.

### 4. Keep clocks separate
**Met**.
Authored task time, wiki revision-request time, archive capture time, and service-event time are formally segregated into distinct schemas and fields in `control-evaluations.json`.

### 5. State whether evidence supports or contradicts the reported backup signal, and which stages remain open
**Met**.
The evidence supports the adoption of the backup failover protocol and the persistent registration of `langr5backup4813_CA`, but contradicts the claim that an unambiguous backup task signal was observed during R5. Both contemporary transaction logging and recipient read verification remain open.

---

## Reproduction

Run the standalone verification script offline from this directory:

```bash
python3 verify.py --negative-controls
```

The script executes with zero external network requests and verifies:
- Manifest file presence, sizes, and SHA-256 digests.
- Exact byte length (40 bytes) and SHA-256 (`86af0481...`) of `countapi_langr5backup4813_CA.json`.
- Canonical record body hashes across all 6 referenced records.
- Verbatim presence of the noise floor rules, authored claims, and primary CA5 exchanges.
- Rejection of tampered manifests, naive noise attribution, primary thanks transference, and timing conflation.

---

## Limitations and Alternatives

1. **CountAPI Ephemeral Backend**: CountAPI does not provide immutable append-only transaction logs. A historical ledger showing exact request timestamps cannot be recovered from the endpoint.
2. **Alternative Interpretation (Test Artifact)**: The count of 4 observed in September 2026 likely represents:
   - Initial accidental test hit by LanguageWatcherNov12 (count = 1).
   - Possible R5 hit or second test hit (count = 2).
   - Subsequent forensic or crawler probes replaying the `/hit` endpoint (count = 3, 4).
   Without transaction logs, these cannot be separated.
