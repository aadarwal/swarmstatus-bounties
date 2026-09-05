# Bounty #15 — exact older PBS workbook is readable; partial result

The first-party Tableau view for **PBS-dashboard-AgeGroup-Monthly-date-20241128/PBSdashboard** opened on 5 September 2026, and its ordinary Image download produced a readable PNG. This advances the exact-workbook evidence. **It does not recover historical filtered values or resolve #15; keep the issue open.**

[Exact older-workbook view used](https://viz.aihw.gov.au/t/Public/views/PBS-dashboard-AgeGroup-Monthly-date-20241128/PBSdashboard?:showVizHome=no&State/Territory=Victoria&LGA=Wodonga&ATC%20Level%201=Dermatologicals). The navigation used the view rather than the previously submitted `.csv` resource. The literal `20241128` in the name is a workbook identifier, not proof of publication on that date or a November-only data period. A currently served workbook with that name need not preserve its historical content.

## What the captured artifacts show

| Observation | Current evidence |
| --- | --- |
| URL contains Victoria, Wodonga, Dermatologicals under legacy field names | Initial and final view URLs retained verbatim in `evidence/observations.json`; the accessibility snapshot includes the exact workbook title and URL. |
| Initial visible controls | Australia; All LGAs; All years; Monthly data; ATC1 “(All PBS prescriptions)”. These do not visibly reflect the three requested legacy filters. |
| Actual publisher PNG | Australia; All LGAs; All years; Monthly data; ATC1 “None”; ATC2 “Agents acting on the renin-angiotensin system”. Both chart panels display suppression text and no values. |
| Manual location selection | Through visible controls, Victoria then Wodonga were selected. The LGA control changed its label to “Select a Victoria LGA:”. The expanded menu also contained Ballarat. |
| Manual medicine selection | The ATC1 menu displayed “No Items.” Dermatologicals could not be selected or exported in this observed state. |

The difference between the initial UI's “(All PBS prescriptions)” label and the export's “None” is retained rather than reconciled by assumption. We do not know whether all legacy query values were ignored internally, acted as different filters, or contributed to the empty/suppressed state. Visible suppression does not prove that underlying government data are globally absent.

The unmodified [publisher PNG](evidence/pbs-default-export.png) is 800 × 1830 pixels, 98,272 bytes, SHA-256 `df10488dd47b56217f41afdab375dcda011bf24f3ecf018312e301c62078a680`. Its acquisition clock is the browser download file modification time, `2026-09-05T19:08:33.355180+00:00`. It was requested before the manual location changes and visibly retains Australia/All. Its HTTP response status and download endpoint were not captured, so neither is invented here.

The two viewport screenshots are JPEG/JFIF files (`initial-query.jpg` and `manual-victoria-wodonga-empty-medicine.jpg`), each 1200 × 909 pixels. Their bytes are unchanged from the browser captures. The publisher export is a separate true PNG. The viewport screenshots and their accessibility text were captured at `2026-09-05T19:07:50.752Z` (initial state) and `2026-09-05T19:09:50.497Z` (manual Victoria/Wodonga state with empty medicine menu). The intermediate LGA-menu snapshot has a bounded acquisition interval between those clocks; no exact timestamp is asserted for it.

## Reproduce the retained checks

```sh
python3 verify.py --negative-controls
```

Python 3.9+ and the standard library are sufficient. The script reads only this package, makes no network requests and writes no files. It checks all nine retained evidence files, the PNG dimensions/hash, exact workbook/sheet/query identifiers, selected values in accessibility text, Ballarat/Wodonga menu entries and the explicit partial-result flags. Negative controls reject altered bytes, a wrong workbook version, wrong LGA, a false filter-success assertion and a false historical-period assertion. Pixel interpretation is an observer's transcription, not automatic OCR; inspect the images directly.

To repeat the current UI observation, open the linked first-party view, inspect its visible control values before touching them, then use Download → Image. To inspect the location choices, select Victoria through the visible state control and open the resulting Victoria LGA selector. A fresh run may differ. Do not treat query-string presence or HTTP success as proof of honored filters. No proxy or recorded POST payload was replayed in this pass.

## Scope against #15

The exact named workbook now has a retained current publisher image and source-qualified UI captures. The legacy request strings are preserved, and the mismatch with actual visible selections is documented. However, no independent historical publication linking all constraints was recovered, no Dermatologicals data export or historical response bytes were obtained, and no underlying data period was established. “All years” is a selected control, not a verified coverage range.

The observed labels are current UI labels, not verified URL parameter keys. Their relationship to `PBS-dashboard-AgeGroup-Monthly-date-20250430` and `PBSdashboardallATC1-ATC2medicines-Agegroup` remains untested. This package does not establish equivalent field names, constraints or values across those versions. It neither validates PR #36's alleged successful response nor supplies its missing evidence.

The bounded pass comprised one exact view navigation, one Image export, ordinary controls on that same view and one official-domain search with no results. Empty search results do not establish global source absence. The initial automatic browser security check resolved without intervention. The export arrived after an initial download-directory check; its retained bytes establish the eventual successful image result. No database, site or GitHub content was changed.

## Attribution

**Source: Australian Institute of Health and Welfare.** The downloaded publisher PNG is unmodified. Viewport screenshots and control-value transcriptions are based on Australian Institute of Health and Welfare material. The [AIHW copyright policy](https://www.aihw.gov.au/copyright), previously reviewed on 5 September 2026, releases downloadable material under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) subject to stated logo, trademark, third-party and separate-notice exceptions. No such separate notice is visible on the retained publisher PNG. Source and license attribution must not imply endorsement. This notice does not grant a blanket license to Tableau's software or interface.
