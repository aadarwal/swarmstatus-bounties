# Bounty #9: NAEP alias/query surface bounding and registration provenance

## Verdict

1. **Third Surface Recurrence**: Refuted. Exhaustive auditing across all 20+ shortener services in the primary artifact corpus, the Swarmstatus multi-platform feature index, and the complete wiki database (`collusion-wiki.db`) bounds the exact alias `nrcnaepres9983` and query pair to strictly two surfaces: `shortener:rmn.re` and `shortener:vanderbi.lt`. No third independently sourced registration, archived message, or wiki page exists.
2. **Registration Provenance**: The two entries are **separate, parallel autonomous registrations**, not copied or imported database records. Both shorteners received independent HTTP creation requests from distinct Microsoft Azure IP addresses within six seconds of each other.

---

## Evidence and Forensic Analysis

### 1. Target Query Bundle
Both entries target the identical, high-entropy 8-parameter NAEP query:
`https://www.nationsreportcard.gov/Dataservice/GetAdhocData.aspx?type=data&subject=science&grade=12&subscale=SRPUV&variable=HAOHTAIC&jurisdiction=NP&stattype=MN:MN&Year=2019`

The parameters define:
- `Year`: 2019
- `grade`: 12
- `jurisdiction`: NP (National Public)
- `stattype`: MN:MN (Mean and standard error)
- `subject`: science
- `subscale`: SRPUV (Science overall scale)
- `type`: data
- `variable`: HAOHTAIC (Student report on how often they do science activities)

### 2. Forensic Comparison: RMN vs. Vanderbilt

| Attribute | Vanderbilt (`vanderbi.lt`) | RMN (`rmn.re`) | Provenance Implication |
| :--- | :--- | :--- | :--- |
| **Record ID** | `bca374c2713e81cc5ac4bfc9dc62c511` | `450789df13b6c28f392700ad20a91558` | Two separate platform records in Swarmstatus index |
| **Alias (Keyword)** | `nrcnaepres9983` | `nrcnaepres9983` | Identical high-entropy task alias |
| **Raw Stored Clock** | `2026-06-12 17:09:31` | `2026-06-12 22:09:25` (DB) / `2026-06-13 02:09` (UI) | Both services use unzoned server clocks |
| **Clock Timezone Basis** | US/Central (CDT, UTC-5) | UTC (UTC+0) | Vanderbilt server in Nashville, TN (UTC-5) |
| **Normalized UTC Time** | `2026-06-12 22:09:31 UTC` | `2026-06-12 22:09:25 UTC` | **Delta: 6 seconds** (simultaneous dual-registration) |
| **Creator IP** | `135.119.61.210` | `64.236.176.163` | **Distinct IPs refutes database copy/import** |
| **Creator ASN** | AS8075 (Microsoft Corporation) | AS8075 (Microsoft Corporation) | Azure cloud infrastructure origin |
| **Lifetime Clicks** | 1 click | 33 clicks (31 at baseline, 33 at capture) | Distinct reachability/downstream interaction |
| **Referrer Breakdown** | 0 referrers logged | 4 self-referrers (`rmn.re`), 29 direct | Traffic directed exclusively to RMN |
| **Preceding Probe** | `crqeg` (2026-06-12 21:26:34 UTC) | `jw`, `jx`, `ourt665714` (2026-06-12 21:15–21:24 UTC) | Coordinated reconnaissance window |

### 3. Disproof of Copied / Imported Records

The hypothesis of a database replica, SQL table import, or scraper mirror is disproven by three empirical invariants:
1. **Divergent Originating IPs:** In YOURLS architectures, the `yourls_url` SQL table stores the client IP in the `ip` column. An import or mirror preserves identical client IPs. Vanderbilt records `135.119.61.210`, whereas RMN records `64.236.176.163`. Both shorteners received independent external HTTP POST requests.
2. **Sub-Ten-Second True Concurrency:** The positive control alias `zzx9` (`https://example.org/agtest`) was registered on Vanderbilt at `2026-06-18 11:38:08` (CDT) and on RMN at `2026-06-18 16:38:07` (UTC), confirming a 4-hour, 59-minute, 59-second server clock delta. Applying this calibrated 5-hour offset to `nrcnaepres9983` establishes that RMN registered at `22:09:25 UTC` and Vanderbilt registered at `22:09:31 UTC` — an interval of exactly 6 seconds. This represents concurrent multi-target registration by an automated agent dispatching across multiple shortener endpoints.
3. **Telemetry Asymmetry:** Vanderbilt logged 1 lifetime click with zero referrers, while RMN logged 33 clicks with 4 internal preview referrers. Downstream traffic was routed to RMN rather than Vanderbilt.

### 4. Corpus Search and Surface Bounding

To test for recurrence on a third surface, we audited four distinct layers of evidence:
1. **Swarmstatus Multi-Platform Registry:** Queried across 50+ platforms for `HAOHTAIC` and `nrcnaepres9983`. Exactly two records exist: `450789df` and `bca374c2`. Platform count equals 2, object count equals 2.
2. **Raw Shortener Archive Corpus:** Audited all shorteners archived in `collusion-wiki-link-shorteners` (`da.gd`, `uoft.me`, `u.ethz.ch`, `goto.unm.edu`, `yourls.pl`, `yourls.space`, `zapro.si`, `klickhier.at`, `bitily.in`, `kodak.love`, `linkrutgon.net`, etc.). Zero additional matches for `nrcnaepres9983` or `HAOHTAIC` exist. The query bundle is absent from all other shorteners.
3. **Wiki Database (`collusion-wiki.db`):** Subagent reports 8 and 9 confirm that NAEP is one of 89 out-of-wiki evaluation task families. It appears 0 times in `collusion-wiki.db`. The agent created short links on external services but never posted the links or results to the wiki.
4. **Third-Party Referrer Analysis:** The only other occurrence of NAEP in any artifact is a distinct query (`variable=B034602`, not `HAOHTAIC`) appearing as an HTTP referrer string in `goto.unm.edu/plus/discvr.html`. This does not match the required high-entropy query bundle and represents a distinct test probe.

---

## Offline Deterministic Verification

The package contains an offline verifier requiring Python 3.9+ and standard library only:

```sh
python3 verify.py
```

To output machine-parseable JSON:

```sh
python3 verify.py --json
```

The script verifies:
1. Cryptographic hashes and integrity of all seven retained evidence artifacts.
2. Exact parameter matching for all 8 query bundle keys and values.
3. Distinct creator IP attribution to Microsoft Corporation ASN 8075.
4. Server clock calibration and 6-second concurrency window.
5. Strict bounding to N=2 surfaces across the entire indexed corpus.
6. Five negative controls rejecting alternate query variables, generic homepages, identical-IP copy assumptions, unzoned clock misinterpretations, and unverified third-surface claims.

---

## Acceptance Criteria Checklist

- [x] **Exact source locators, retained content, and acquisition timestamps:** Full record snapshots (`450789df13b6c28f392700ad20a91558.json`, `bca374c2713e81cc5ac4bfc9dc62c511.json`, `rmn_raw_link.json`, `vanderbilt_raw_link.json`) are preserved in `evidence/`.
- [x] **Match the complete resource identifier/query bundle:** All 8 query parameters (`Year=2019`, `grade=12`, `jurisdiction=NP`, `stattype=MN:MN`, `subject=science`, `subscale=SRPUV`, `type=data`, `variable=HAOHTAIC`) verified against both destinations.
- [x] **State what is new and check overlaps:** Clarified that the observed 5-hour / 9-hour raw time gap is a server timezone offset (CDT vs UTC), demonstrating near-simultaneous execution (Δ = 6s) rather than publication latency. Exhaustively proved absence across all other shorteners and the wiki DB.
- [x] **Explicit clock bases and URL storage vs. delivery:** Clarified that both server clocks are unzoned (`vanderbi.lt` running US/Central UTC-5, `rmn.re` running UTC). Explicitly noted that registering a redirect URL does not constitute proof of successful target response retrieval or downstream message delivery.
- [x] **Original data-source page context:** Addressed the NAEP official data service context; demonstrated that external data sources alone do not constitute staging surfaces without active registration.

---

## Limitations and Provenance Anchors

1. **Absence of Stored Target Payload:** Neither shortener stored the HTTP response body returned by `nationsreportcard.gov`. The records prove alias registration and redirect targeting, not successful data receipt or response persistence.
2. **Single Resource Fingerprint:** Because both shorteners target the identical destination URL, they represent one resource fingerprint evaluated across two endpoints, rather than two independent information sources.
3. **Actor Attribution:** While both registrations originated from Microsoft Corporation ASN 8075 IP blocks within 6 seconds, the specific human, model, or task-orchestration identity cannot be inferred solely from IP infrastructure telemetry.
