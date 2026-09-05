# Evidence update for bounty #12 — keep open

The actual publisher PNG has been recovered and matched to the historical response. The official Tableau interface, with `Cohort=Permanent residential aged care` and `Condition=Mood disorders`, exported an 800×550 PNG of 71,515 bytes. Its SHA-256 is `a634c746bc2c2e78a360034a359dd1c7f07ec08490b4b173bd0a86f44366e316`, exactly matching transaction 9 of [receipt 66e46234-179e-4214-ada1-fc3ed344d1ae](https://urlquery.net/report/66e46234-179e-4214-ada1-fc3ed344d1ae). That transaction occurred at `2026-06-18T04:11:21.214Z`; the report date is `2026-06-18T04:11:43Z`. The current download was acquired on 5 September 2026. Thirteen historical transactions in the frozen receipt collection report this same image hash.

The recovered image visibly confirms the workbook/sheet and both filters. It also resolves a semantic ambiguity: **the selected mode is “Proportion of people,” with a percentage axis**. The alternative “Age-and-sex-specific crude rate (per 1,000)” control is unselected. The filename `F05-Age-specificcruderates` alone does not establish which measure was displayed. This is an age distribution among people with mood disorders, not the alternative crude-rate view.

The [official report](https://www.aihw.gov.au/reports/aged-care/mental-health-in-aged-care/contents/mental-health-conditions-in-aged-care-service-user) links this workbook as Figure 5. Its [data page](https://www.aihw.gov.au/reports/aged-care/mental-health-in-aged-care/data) also yielded the [supplementary XLSX](https://www.aihw.gov.au/getmedia/8bf253f8-1d4e-4024-a755-69f5cfe7fca8/AIHW-AGE-115-Mental-health-in-aged-care-Supplementary-results-tables.xlsx), 168,285 bytes, SHA-256 `dd19e2e5db79b7719af1d9121fb5baa4cec441fbfa3e539ab4dc24cac03bf718`. It contains Contents and Tables S1–S5; it does not contain Figure 5's age-by-sex series. Table S2 gives the all-years residential mood-disorder count 131,648 and proportion 44.4%, a different denominator/quantity. Do not substitute those values for Figure 5.

Acceptance review:

- Retained, hashed publisher artifact with source URL and acquisition date: met. The workbook identifier's date and report release date are not historical task-publication timestamps.
- Full workbook/sheet and both cohort/condition filters preserved and compared: met.
- Request, response metadata, readable image and displayed measure separated: met. Image match does not establish that a task actor read an answer.
- Independence explained: met as a classification. This is a current publisher recovery matching previously recorded bytes, not a newly found task-origin publication.
- **Underlying question—independent task, paste, wiki body or publication containing the full constraints: unresolved.** The two retained b7ps3 referrer records still contain only unfiltered resource links and have no publication timestamp.

Suggested status: retain #12 as open, update its known evidence and replace the remaining gap with the missing independent task-origin/staging publication. No actor or model attribution follows from this recovery.

For reuse, the [AIHW copyright policy](https://www.aihw.gov.au/copyright) releases downloadable material under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), subject to stated exceptions for logos, third-party material, trademarks and separate notices. The retained PNG has none of those exceptions visibly marked. Attribute the unmodified image exactly: **Source: Australian Institute of Health and Welfare.** Include the source/chart and license links and do not imply AIHW endorsement. The image is unmodified.

## Packaged reproduction

Run `python3 verify.py --negative-controls` from the package. The verifier checks the image signature, dimensions, exact SHA-256, the selected receipt transaction and all 13 matching historical image transactions. It also re-parses the full workbook/sheet/filter URLs and checks the retained transcription is explicitly a proportion mode, not the alternative crude rate. The image itself remains the primary evidence for visual labels: the script does not perform OCR or independently verify the observer's transcription. Open `evidence/aihw-figure5-proportion.png` to inspect it. A second researcher independently inspected these controls and axis during review.

The supplemental workbook is included as an unmodified, separately hashed artifact for anyone checking why Table S2 must not replace Figure 5. The automated verifier checks its integrity; it does not extract or claim to verify its cells. The historical ledger records successful response hashes without provider-retained bodies; this current image matches those hashes. Current acquisition time, historical HTTP transaction time, provider report date, study period and unzoned/referrer metadata remain different clocks.

`evidence/aihw-referrer-urls.json` retains the exact two public unfiltered links and their record IDs. Neither has a publication timestamp, nor does either encode the required cohort/condition. Their presence does not close the independent full-constraint task-origin gap. Leave #12 open.

Source: Australian Institute of Health and Welfare. Image and workbook are unmodified. See [reuse details](REUSE.md).
