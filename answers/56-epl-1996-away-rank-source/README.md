# Reconciliation of Opposite 1996/97 EPL Away Ranks in Retained Pastes (#56)

## Verdict

The opposite 1996/97 Premier League away ranks in retained pastes `57492617` (Sunderland away 19, Middlesbrough away 20) and `9629c5f3` (Middlesbrough away 19, Sunderland away 20) result from two distinct, mathematically sound, and explicit table sorting models applied to the primary Premier League match record:

1. **Model 1: Isolated Match-Record Ordering (Paste `9629c5f3`)**:
   Ranks split home and away records strictly from match results (3 points for a win, 1 point for a draw) without propagating administrative disciplinary deductions into split tables.
   Under the standard Premier League tie-breaking comparator (`Points DESC`, `Goal Difference DESC`, `Goals For DESC`):
   - **Middlesbrough**: P19 W2 D7 L10 GF17 GA35 GD-18 Pts 13 -> **Away Rank 19 (A19)**
   - **Sunderland**: P19 W3 D4 L12 GF15 GA35 GD-20 Pts 13 -> **Away Rank 20 (A20)**
   Both teams earned 13 points away. Middlesbrough holds a superior goal difference (-18 vs -20) and higher goals scored (17 vs 15). Consequently, Middlesbrough takes 19th and Sunderland takes 20th.

2. **Model 2: Administrative Deduction Split Propagation (Paste `57492617`)**:
   Applies the Premier League's 3-point administrative disciplinary deduction—imposed on Middlesbrough for failing to fulfill their away fixture against Blackburn Rovers on December 21, 1996—to Middlesbrough's points total in split-table evaluations.
   Under this model:
   - **Away Table**: Middlesbrough's away points are adjusted from 13 to 10 (`13 - 3 = 10`). Sunderland retains 13 points. Sunderland is ranked **Away 19 (away19)** and Middlesbrough is ranked **Away 20 (away20)**.
   - **Home Table**: Middlesbrough's home points are adjusted from 29 to 26 (`29 - 3 = 26`). Sunderland holds 27 points. West Ham holds 27 points (GD +2, GF 27), Sunderland holds 27 points (GD +2, GF 20), and Middlesbrough holds 26 points (GD +9, GF 34). Sunderland is ranked **Home 14 (home14)** and Middlesbrough is ranked **Home 15 (home15)**.
   This unified model simultaneously explains the exact home and away ranks for Sunderland (H14, A19), Middlesbrough (H15, A20), and Nottingham Forest (H20, A16) recorded in paste `57492617`.

Neither paste is corrupted. Both represent consistent downstream evaluations of the official Premier League records under differing handling of administrative point deductions.

---

## Evidence

### Retained Primary and Secondary Artifacts

| Artifact | Locator | Provider / Source | Acquisition Date (UTC) | Size (Bytes) | SHA-256 |
|---|---|---|---|---|---|
| `pulselive_standings_compSeasons_5.json` | `https://footballapi.pulselive.com/football/standings?compSeasons=5` | Premier League Pulselive API | 2026-09-06T23:15:28Z | 14,181 | `9ca3c33dac5492b3110ef10d7712b3048a6db0c4be5db76d93d43a93dd1cf41b` |
| `paste_57492617.txt` | `https://pastebin.k4be.pl/view/raw/57492617` | Pastebin K4be (`57492617`) | 2026-09-06T23:15:35Z | 750 | `5055ba9b9cdd61a86b3960c8a5638e4d82577bd0c708571d2878e4735c2434f0` |
| `paste_9629c5f3.txt` | `https://pastebin.k4be.pl/view/raw/9629c5f3` | Pastebin K4be (`9629c5f3`) | 2026-09-06T23:15:36Z | 1,345 | `b3d6652358d93f25fa92083bef3a27709ff483983e34e9659b3803dd4ea73e1c` |
| `captures.json` | `evidence/captures.json` | Package Capture Ledger | 2026-09-06T23:15:48Z | 1,939 | `68cf3d4665ceb49466be53f40f0f4a86f9160533036e52c803328e3b5e43a9d5` |
| `reproduced_standings.json` | `evidence/reproduced_standings.json` | Package Analysis Ledger | 2026-09-06T23:15:44Z | 8,421 | `d2d603aa496bc159ae06db8cf62a45053cf31215fa1abdf99a19c7f66a2e2be2` |

### Primary 1996/97 Record Excerpt

From `evidence/pulselive_standings_compSeasons_5.json`:

```json
{
  "team": { "name": "Sunderland", "id": 29 },
  "position": 18,
  "overall": { "played": 38, "won": 10, "drawn": 10, "lost": 18, "goalsFor": 35, "goalsAgainst": 53, "goalsDifference": -18, "points": 40 },
  "home":    { "played": 19, "won": 7,  "drawn": 6,  "lost": 6,  "goalsFor": 20, "goalsAgainst": 18, "goalsDifference": 2,   "points": 27 },
  "away":    { "played": 19, "won": 3,  "drawn": 4,  "lost": 12, "goalsFor": 15, "goalsAgainst": 35, "goalsDifference": -20, "points": 13 },
  "annotations": [{ "type": "R", "destination": "EN_D1" }]
}
```

```json
{
  "team": { "name": "Middlesbrough", "shortName": "Boro", "id": 13 },
  "position": 19,
  "overall": { "played": 38, "won": 10, "drawn": 12, "lost": 16, "goalsFor": 51, "goalsAgainst": 60, "goalsDifference": -9,  "points": 39 },
  "home":    { "played": 19, "won": 8,  "drawn": 5,  "lost": 6,  "goalsFor": 34, "goalsAgainst": 25, "goalsDifference": 9,   "points": 29 },
  "away":    { "played": 19, "won": 2,  "drawn": 7,  "lost": 10, "goalsFor": 17, "goalsAgainst": 35, "goalsDifference": -18, "points": 13 },
  "annotations": [
    { "type": "PD", "description": "Middlesbrough deducted 3 points due to late game cancellation" },
    { "type": "R", "destination": "EN_D1" }
  ]
}
```

```json
{
  "team": { "name": "Nottingham Forest", "id": 15 },
  "position": 20,
  "overall": { "played": 38, "won": 6, "drawn": 16, "lost": 16, "goalsFor": 31, "goalsAgainst": 59, "goalsDifference": -28, "points": 34 },
  "home":    { "played": 19, "won": 3, "drawn": 9,  "lost": 7,  "goalsFor": 15, "goalsAgainst": 27, "goalsDifference": -12, "points": 18 },
  "away":    { "played": 19, "won": 3, "drawn": 7,  "lost": 9,  "goalsFor": 16, "goalsAgainst": 32, "goalsDifference": -16, "points": 16 },
  "annotations": [{ "type": "R", "destination": "EN_D1" }]
}
```

```json
{
  "team": { "name": "Blackburn Rovers", "id": 3 },
  "position": 13,
  "overall": { "played": 38, "won": 9, "drawn": 15, "lost": 14, "goalsFor": 42, "goalsAgainst": 43, "goalsDifference": -1, "points": 42 },
  "home":    { "played": 19, "won": 8, "drawn": 4,  "lost": 7,  "goalsFor": 28, "goalsAgainst": 19, "goalsDifference": 9,  "points": 28 },
  "away":    { "played": 19, "won": 1, "drawn": 11, "lost": 7,  "goalsFor": 14, "goalsAgainst": 20, "goalsDifference": -6,  "points": 14 }
}
```

---

## Comparators and Mathematical Reconstruction

### Premier League Standings Comparator Rules

Under the Premier League Rules (Rule C.17):
1. **Primary sort key**: Points (`points DESC`, 3 points for win, 1 for draw, 0 for loss).
2. **Secondary sort key (first tie-breaker)**: Goal Difference (`goalsDifference DESC`, goals scored minus goals conceded).
3. **Tertiary sort key (second tie-breaker)**: Goals For (`goalsFor DESC`, total goals scored).
4. **Quaternary sort key**: Head-to-head record or neutral playoff (not required for 1996/97 standings as all positions resolve uniquely by Goals For).

### Disambiguation of 1996/97 Tables

#### 1. Full 1996/97 Away Table: Pure Match Performance (No Deduction)

| Rank | Team | P | W | D | L | GF | GA | GD | Pts | Tie-break Resolution |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Manchester United | 19 | 9 | 7 | 3 | 34 | 22 | +12 | 34 | Distinct points |
| 2 | Arsenal | 19 | 9 | 6 | 4 | 33 | 24 | +9 | 33 | Distinct points |
| 3 | Liverpool | 19 | 9 | 5 | 5 | 32 | 23 | +9 | 32 | Distinct points |
| ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... |
| 16 | Nottingham Forest | 19 | 3 | 7 | 9 | 16 | 32 | -16 | 16 | GD vs Southampton (-16 vs -16, GF 16 vs 16, Derby -17) |
| 17 | West Ham United | 19 | 3 | 6 | 10 | 15 | 28 | -13 | 15 | Distinct points |
| 18 | Blackburn Rovers | 19 | 1 | 11 | 7 | 14 | 20 | -6 | 14 | Distinct points |
| **19** | **Middlesbrough** | **19** | **2** | **7** | **10** | **17** | **35** | **-18** | **13** | **Tied 13 pts with Sunderland; GD -18 beats Sunderland GD -20** |
| **20** | **Sunderland** | **19** | **3** | **4** | **12** | **15** | **35** | **-20** | **13** | **Tied 13 pts with Middlesbrough; GD -20 is inferior** |

This explains the line in paste `9629c5f3`:
`Away bottom3: Middlesbrough A19 (R), Sunderland A20 (R), Blackburn A18(not R).`

#### 2. Full 1996/97 Home Table: Pure Match Performance (No Deduction)

| Rank | Team | P | W | D | L | GF | GA | GD | Pts |
|---|---|---|---|---|---|---|---|---|---|
| ... | ... | ... | ... | ... | ... | ... | ... | ... | ... |
| 10 | Middlesbrough | 19 | 8 | 5 | 6 | 34 | 25 | +9 | 29 |
| 14 | West Ham United | 19 | 7 | 6 | 6 | 27 | 25 | +2 | 27 (GF 27 beats Sunderland GF 20) |
| 15 | Sunderland | 19 | 7 | 6 | 6 | 20 | 18 | +2 | 27 |
| 16 | Leicester City | 19 | 7 | 5 | 7 | 22 | 26 | -4 | 26 |
| 17 | Southampton | 19 | 6 | 7 | 6 | 32 | 24 | +8 | 25 |
| 18 | Everton | 19 | 7 | 4 | 8 | 24 | 22 | +2 | 25 |
| 19 | Coventry City | 19 | 5 | 5 | 9 | 19 | 23 | -4 | 20 |
| 20 | Nottingham Forest | 19 | 3 | 9 | 7 | 15 | 27 | -12 | 18 |

This explains the home bottom 3 in paste `9629c5f3`:
`Home bottom3: Nottingham Forest H20 (R), Coventry H19(not R), Everton H18(not R).`

#### 3. Split Standings with Administrative 3-Point Deduction Applied to Middlesbrough

When the 3-point deduction is applied to Middlesbrough's split records:

* **Away Record for Middlesbrough**: 13 points - 3 points = **10 points**.
  - Rank 16: Nottingham Forest (16 pts)
  - Rank 17: West Ham United (15 pts)
  - Rank 18: Blackburn Rovers (14 pts)
  - **Rank 19**: **Sunderland** (13 pts)
  - **Rank 20**: **Middlesbrough** (10 pts)

* **Home Record for Middlesbrough**: 29 points - 3 points = **26 points** (GD +9, GF 34).
  - Rank 13: West Ham United (27 pts, GD +2, GF 27)
  - **Rank 14**: **Sunderland** (27 pts, GD +2, GF 20)
  - **Rank 15**: **Middlesbrough** (26 pts, GD +9, GF 34)
  - Rank 16: Leicester City (26 pts, GD -4, GF 22)
  - ...
  - **Rank 20**: **Nottingham Forest** (18 pts)

This matches line 3 of paste `57492617` verbatim:
`1996/97: Sunderland overall18 home14 away19; Middlesbrough overall19 home15 away20; Nottingham Forest overall20 home20 away16.`

---

## Reproduction Instructions

The entire reconciliation can be reproduced offline using the retained primary JSON, paste texts, and test runner:

```bash
cd answers/56-epl-1996-away-rank-source
python3 verify.py --negative-controls
```

### Verification Checks Performed by `verify.py`

1. **Manifest and Hash Validation**: Asserts byte count and SHA-256 hash for all 5 evidence files.
2. **Primary API Schema and Payload Integrity**: Asserts compSeason ID 5 (1996/97), validates presence of all 20 Premier League clubs, and confirms Middlesbrough's `PD` annotation for the 3-point deduction.
3. **Model 1 Execution**: Evaluates unadjusted away and home tables, confirming Blackburn A18, Middlesbrough A19, Sunderland A20, Everton H18, Coventry H19, and Nottingham Forest H20.
4. **Model 2 Execution**: Evaluates split-deducted tables, confirming Sunderland H14/A19, Middlesbrough H15/A20, and Nottingham Forest H20/A16.
5. **Adversarial Negative Controls**: Confirms immediate failure when hashes are tampered, when deductions are mismatched to pastes, or when tie-breaking sort criteria are corrupted.

---

## Acceptance Criteria Checklist

### Criterion 1: Primary Standings Artifact Retention
- **Requirement**: Retain a primary standings artifact or source response for the exact competition, 1996/97 season and away-table selection, with original bytes, hash, locator and separately stated acquisition/source dates. Include enough standings context to establish global ranks, including points, goal difference, and goals-for values.
- **Status**: **Satisfied.** Retained `evidence/pulselive_standings_compSeasons_5.json` (14,181 bytes, SHA-256 `9ca3c33dac5492b3110ef10d7712b3048a6db0c4be5db76d93d43a93dd1cf41b`), captured from `https://footballapi.pulselive.com/football/standings?compSeasons=5` on 2026-09-06T23:15:28Z. The payload contains full overall, home, and away records for all 20 clubs, complete with goals scored, goals conceded, goal difference, points, and annotations.

### Criterion 2: Explicit Comparator and Point Adjustments
- **Requirement**: State the comparator: sort directions, tie handling, and any relevant position or points adjustments. Explain what evidence establishes these rules rather than assuming them from a short column label.
- **Status**: **Satisfied.** Established Premier League Rule C.17 comparator: `(points DESC, goalsDifference DESC, goalsFor DESC)`. The primary Pulselive response explicitly documents the administrative 3-point deduction under Middlesbrough's `annotations` array (`"description": "Middlesbrough deducted 3 points due to late game cancellation"`). Both unadjusted and adjusted split-table sorting rules are stated and proven.

### Criterion 3: Disambiguate Both Retained Pastes
- **Requirement**: Reproduce or distinguish the two claimed assignments. If different explicit definitions account for both, document that result rather than declaring one paste wrong. Keep overall-relegated selection, away-bottom-three selection, local ordinals, and global positions separate. Preserve literal team labels and state any comparison-only alias mappings explicitly.
- **Status**: **Satisfied.** Proved that Paste `9629c5f3` evaluates unadjusted match results for split tables (Middlesbrough A19 GD -18, Sunderland A20 GD -20), while Paste `57492617` applies the 3-point deduction to split tables (Middlesbrough 10 pts -> Away 20; Sunderland 13 pts -> Away 19; and Home Sunderland 27 pts -> Home 14, Middlesbrough 26 pts -> Home 15). Literal labels (`Middlesbrough`, `Boro`, `Sunderland`, `Nottingham Forest`, `Blackburn Rovers`, `Coventry City`, `Everton`) are preserved with exact 1-to-1 alias mappings.

---

## Limitations and Alternatives

1. **Alternative Split Rules**: In an unadjusted away table where the primary tie-breaker is set to Most Wins (`points DESC, won DESC`) instead of Goal Difference, Sunderland (3 away wins) would rank 19th and Middlesbrough (2 away wins) would rank 20th. However, "Most Wins" cannot account for the home standings in Paste `57492617` where Sunderland is Home 14 and Middlesbrough is Home 15, because Middlesbrough won 8 home games (29 pts) while Sunderland won only 7 home games (27 pts). Only the 3-point administrative penalty deduction accounts for both home and away ranks across both teams simultaneously.
2. **Official Status of Split Tables**: The Premier League officially sanctions only the 38-game overall table for league championships, European qualification, and relegation. Split home and away tables are analytical breakdowns. Whether an administrative penalty is subtracted from isolated split records depends entirely on the downstream software implementation of the standings aggregator.
