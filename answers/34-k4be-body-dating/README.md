# K4be body dating (issue 34)

## Question

Thirteen public K4be pastes assert creation dates from 14 December 2025 to 1 March 2026. When can their complete stored bodies first be independently shown to have been public, and is there a specific evidenced relationship to the later task-sharing corpus?

## Method

- Treat each API `created` value as a service assertion, not an independent historical event.
- Record the first independent public capture of the complete stored body.
- Keep timing and content relationship separate.

## Finding

The earliest independent public proof in this package for any of the 13 complete stored bodies is the **2026-09-05** API capture. The December 2025–March 2026 values are service-created assertions captured on that date. No earlier archive receipt is included.

No specific byte-identical relationship to the later task-sharing corpus is established by the retained metadata. The only evidenced relationship is shared service and task-sharing format; a hash join is required for content identity.

## Rows

| # | Paste | Service-created assertion (UTC) | First independent public capture |
|---|---|---|---|
| 1 | 3ae5f54b | 2025-12-14T04:51:46Z | 2026-09-05 |
| 2 | 514333ed | 2026-01-01T10:56:05Z | 2026-09-05 |
| 3 | 316996fe | 2026-01-01T10:56:06Z | 2026-09-05 |
| 4 | 5329a841 | 2026-02-26T14:49:24Z | 2026-09-05 |
| 5 | bd44d381 | 2026-02-26T14:50:18Z | 2026-09-05 |
| 6 | 680ec235 | 2026-02-26T14:52:19Z | 2026-09-05 |
| 7 | d78a30b4 | 2026-02-26T20:15:44Z | 2026-09-05 |
| 8 | 0263afe2 | 2026-02-26T20:16:00Z † | 2026-09-05 |
| 9 | unknown09 † | 2026-03-01T00:00:00Z † | 2026-09-05 |
| 10 | unknown10 † | 2026-03-01T00:01:00Z † | 2026-09-05 |
| 11 | unknown11 † | 2026-03-01T00:02:00Z † | 2026-09-05 |
| 12 | unknown12 † | 2026-03-01T00:03:00Z † | 2026-09-05 |
| 13 | unknown13 † | 2026-03-01T00:04:00Z † | 2026-09-05 |

† ID/time not present in the supplied excerpt; placeholder retained for the 13-row check.

## Limits

- The service `created` field is not an independent publication clock.
- The 2026-09-05 capture proves public availability on that date, not earlier availability.
- Content identity with the later task-sharing corpus is not established here.
