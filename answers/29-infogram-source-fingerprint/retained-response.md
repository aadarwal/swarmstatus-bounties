# Retained response: chart table vs article prose

## Answer

No independently retained task response or answer passage in this repository currently reproduces the exact Infogram table. The retained artifacts are source-side captures, not a task response. A response that does distinguish the chart from prose must use both fingerprints below.

## Discriminating fingerprints

1. The `2.0` row has exact chart cells `67` for Rajinikanth's age and `26` for the age of the female lead, giving a derived difference of `67 - 26 = 41`. The publisher article prose says about `42`. A response using `41`, or the exact cells `67` and `26`, is chart-derived; one using about `42` is prose-derived.
2. The table has an ordered 11-film sequence: Baba; Chandramukhi; Sivaji: The Boss; Enthiran/Robot; Lingaa; Kabali; Kaala; 2.0; Petta; Darbar; Annaatthe. A response preserving this order and the exact numeric cells is table-derived.

## Retained evidence

- `answers/29-infogram-source-fingerprint/chart-table.json` contains the exact table and the `2.0` cells.
- `answers/29-infogram-source-fingerprint/publisher-chart-locators.json` contains the UUID locator.
- `answers/29-infogram-source-fingerprint/capture-metadata.json` records the direct capture.
- The issue's retained record `2f441c09` is a source revision; its body does not include a returned table or final answer.

## Scope

This is a repository-local finding. It does not claim that no external retained response exists; it records that none is present in the checked-in answer artifacts and supplies the readable response and fingerprints needed to classify one.
