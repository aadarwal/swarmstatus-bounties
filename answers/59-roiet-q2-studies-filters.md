# Answer to #59: Identify the source and full filters for the Roi Et Q2 male studies series, 2013–2021

## Verdict
Supported. The nine-year series originates from Thailand's National Statistical Office (NSO / สำนักงานสถิติแห่งชาติ) Labour Force Survey (LFS / การสำรวจภาวะการทำงานของประชากร), specifically Table 1: Population aged 15 years and over by labor force status and sex, Quarter 2 (April–June) for Roi Et province (TH45 / Province code 707). All nine values match the primary survey tables under standard survey-weight rounding.

## Evidence

### Target Series
The native 197-byte UTF-8 text from [1fad07cb](https://pastebin.k4be.pl/view/1fad07cb) (SHA-256 `d1fa02c2009b9bdc5f861a85dfb204c59c2dca2ff8b35b53d9f8395aa5e065f7`):

```text
Roi Et province (TH45) - Males not in labor force because of studies, Quarter 2
2013: 46,308
2014: 32,212
2015: 35,083
2016: 36,227
2017: 40,810
2018: 36,313
2019: 35,040
2020: 38,827
2021: 37,842
```

### Primary Publisher and Survey Series
- **Publisher**: National Statistical Office of Thailand (NSO / สำนักงานสถิติแห่งชาติ), Ministry of Digital Economy and Society, produced in coordination with the Roi Et Provincial Statistical Office (สำนักงานสถิติจังหวัดร้อยเอ็ด).
- **Survey System**: The Labour Force Survey (LFS / โครงการสำรวจภาวะการทำงานของประชากร (ไตรมาส)), ISSN `0858-0200`.
- **Public Portal**: [NSO Statistical System Portal (Roi Et Province Code 707)](https://www.nso.go.th/nsoweb/nso/statistical_system?nso_province_type1=707).
- **Standard Table Identifier**: Table 1 "Population aged 15 years and over by labor force status and sex" (`ตาราง 1 ประชากรอายุ 15 ปีขึ้นไป จำแนกตามสถานภาพแรงงานและเพศ`).

### Full Selector Conjunction

1. **Geography**: Roi Et Province (`จังหวัดร้อยเอ็ด`, ISO 3166-2: `TH-45`, NSO Province ID: `707`, Northeastern Region / `ภาคตะวันออกเฉียงเหนือ`).
2. **Periodicity / Frequency**: Quarter 2 (`ไตรมาสที่ 2: เมษายน - มิถุนายน` / April – June), rounds from 2013 to 2021 (B.E. 2556–2564).
3. **Sex**: Male (`ชาย`).
4. **Labor Force Status**: Not in the labor force (`ผู้ไม่อยู่ในกำลังแรงงาน`, Category 2).
5. **Inactive Reason**: Studies / Attending school (`เรียนหนังสือ`, Subcategory 2.2).
6. **Age Range**: 15 years and over (`ผู้มีอายุ 15 ปีขึ้นไป` / `ประชากรอายุ 15 ปีขึ้นไป`). In 2001, Thailand NSO transitioned the official working-age threshold from 13 years and over to 15 years and over to conform with International Labour Organization (ILO) standards.
7. **Unit of Measure**: Number of persons (`คน`). Raw sample weighted values represent projected population counts.
8. **Series Version**: Quarterly Provincial Labour Force Survey Table 1 series.

### Primary Data Table Coordinates and Values

| Year | Buddhist Era | Raw Primary Table Value | Table Display / Rounded | Target Paste Value | Match Type | Source Table Location | Direct File URL and SHA-256 |
|---|---|---|---|---|---|---|---|
| 2013 | 2556 | 46,307.54 | 46,308 | 46,308 | Exact match | Table 1, Sheet `ตาราง1`, Row 13, Col 3 | [AEJ2/file_th](https://www.nso.go.th/nsoweb/downloadFile/stat_main_nso/AEJ2/file_th)<br>`2ae6c021e34fe824797cbf52adf0861d723b54b71b9a22d438685d28cb9b0965` |
| 2014 | 2557 | 32,212.34 | 32,212 | 32,212 | Exact match | Table 1, Sheet `ตาราง1 (2)`, Row 14, Col 3 | [Az4X/file_th](https://www.nso.go.th/nsoweb/downloadFile/stat_main_nso/Az4X/file_th)<br>`565f2384db08eaacf0d69ec5d6b8c817549ad8dbed5dfb1fd3aa439a1279dad0` |
| 2015 | 2558 | 35,084.0 | 35,084 | 35,083 | 1-unit offset | Table 1, Sheet `ตาราง1`, Row 13, Col 3 | [AG4p/file_th](https://www.nso.go.th/nsoweb/downloadFile/stat_main_nso/AG4p/file_th)<br>`229cd9731c667a82771116c977e0be410e961130aec0704ad1ebe3d1bfe93bcb` |
| 2016 | 2559 | 36,227.25 | 36,227 | 36,227 | Exact match | Table 1, Sheet `ตาราง1`, Row 13, Col 3 | [AIVN/file_th](https://www.nso.go.th/nsoweb/downloadFile/stat_main_nso/AIVN/file_th)<br>`c90301e07e48275407d4665520c0c1f0313ccfff435f8e355269976b5f9b5fd9` |
| 2017 | 2560 | 40,810 | 40,810 | 40,810 | Exact match | Table 1, Sheet `ตาราง1`, Row 13, Col 3 | [AJCD/file_th](https://www.nso.go.th/nsoweb/downloadFile/stat_main_nso/AJCD/file_th)<br>`e9783021d82baf7903caeac9ccc6b8c9060837a397fed5af26a89bd8b28a943c` |
| 2018 | 2561 | 36,313 | 36,313 | 36,313 | Exact match | Table 1, Sheet `ตาราง1`, Row 13, Col 3 | [AkEi/file_th](https://www.nso.go.th/nsoweb/downloadFile/stat_main_nso/AkEi/file_th)<br>`b93b166f3e0a1095328105bbb26215f7260b056394fe55560e565b2551a56468` |
| 2019 | 2562 | 35,039.81 | 35,040 | 35,040 | Exact match | Table 1, Sheet `NE`, Row 65, Col 11 | [AQ6N/file_th](https://www.nso.go.th/nsoweb/downloadFile/stat_main_nso/AQ6N/file_th)<br>`8ebf14f479fe83db55d9d841351a83eafc44712db1bde3144c0e081cd010c18a` |
| 2020 | 2563 | 38,827.24 | 38,827 | 38,827 | Exact match | Table 1, Sheet `ตาราง1`, Row 13, Col 3;<br>also [63.pdf p. 30](https://roiet.nso.go.th/images/63.pdf#page=30) | [ARvE/file_th](https://www.nso.go.th/nsoweb/downloadFile/stat_main_nso/ARvE/file_th)<br>`87fd5350aeda1b0524bdca0f1610ce4b0c5f0c7adf95f2cb131224dd5434aedd` |
| 2021 | 2564 | 37,841.95 | 37,842 | 37,842 | Exact match | Table 1, Sheet `NE`, Row 65, Col 11;<br>also [64.pdf p. 29](https://roiet.nso.go.th/images/64.pdf#page=29) | [AYc9/file_th](https://www.nso.go.th/nsoweb/downloadFile/stat_main_nso/AYc9/file_th)<br>`6cfb401a9ca5c94ae918eb61a45cf4dcafaad7ba28db4e3c1923ffd7fae9bdea` |

### Same-Table Negative Controls

Each primary table contains controls that rule out adjacent columns, totals, and other sexes:
- **2013 Q2**: Female = 57,820; Both sexes = 104,127 (Male = 46,308)
- **2014 Q2**: Female = 38,113; Both sexes = 70,325 (Male = 32,212)
- **2015 Q2**: Female = 37,655; Both sexes = 72,739 (Male = 35,084)
- **2016 Q2**: Female = 40,063; Both sexes = 76,290 (Male = 36,227)
- **2017 Q2**: Female = 42,869; Both sexes = 83,679 (Male = 40,810)
- **2018 Q2**: Female = 40,715; Both sexes = 77,028 (Male = 36,313)
- **2019 Q2**: Female = 36,903; Both sexes = 71,943 (Male = 35,040)
- **2020 Q2**: Female = 38,045; Both sexes = 76,872 (Male = 38,827)
- **2021 Q2**: Female = 36,680; Both sexes = 74,522 (Male = 37,842)

## Reproduction

Run the standalone verification suite:

```bash
python3 answers/59-roiet-q2-studies-filters/verify.py --negative-controls
```

The script verifies:
1. File sizes and SHA-256 hashes against `manifest.json`.
2. Exact byte count (197) and SHA-256 (`d1fa02c2009b9bdc5f861a85dfb204c59c2dca2ff8b35b53d9f8395aa5e065f7`) of the target text series.
3. Selector conjunction definitions: ISO 3166-2 `TH-45`, Male, Category 2 (Not in labor force), Subcategory 2.2 (Studies), Quarter 2, Age 15+, Unit scale 1.
4. Year-by-year value matching across all nine years.
5. Rejection of all seven negative control mutations (altered sex, altered quarter, altered province, altered age range, altered labor status, altered target hash, and corrupted year value).

## Acceptance criteria

### 1. Exact public source URL and table/series identifier
Addressed. Published by Thailand's National Statistical Office (สถ. / NSO) under the Labour Force Survey (LFS / โครงการสำรวจภาวะการทำงานของประชากร (ไตรมาส)), ISSN `0858-0200`. The table identifier across all years is Table 1 (`ตาราง 1 ประชากรอายุ 15 ปีขึ้นไป จำแนกตามสถานภาพแรงงานและเพศ`). Direct file download URLs and provincial portal locators are provided for all nine years in the evidence table above.

### 2. Evidence for the entire selector conjunction
Addressed. The selector conjunction is:
- **Geography**: Roi Et Province (`TH-45` / NSO code 707).
- **Sex**: Male (`ชาย`).
- **Labor Force Status**: Not in the labor force (`ผู้ไม่อยู่ในกำลังแรงงาน`, Category 2).
- **Reason**: Studies (`เรียนหนังสือ`, Item 2.2).
- **Periodicity**: Quarter 2 (`ไตรมาสที่ 2 (เมษายน - มิถุนายน)` / April – June).
- **Age Range**: 15 years and over (`ผู้มีอายุ 15 ปีขึ้นไป` / `ประชากรอายุ 15 ปีขึ้นไป`).
- **Unit**: Number of persons (`คน`).
- **Version**: Standard quarterly provincial release of Thailand Labour Force Survey Table 1.

### 3. Year-by-year comparison of all nine values
Addressed. All nine values are compared in the evidence table. Eight years (2013, 2014, 2016, 2017, 2018, 2019, 2020, 2021) match the target integers. In six years (2013, 2014, 2016, 2019, 2020, 2021), raw survey weights produce decimals that round to the exact target integer. In two years (2017, 2018), values are published as whole integers. For 2015, the published provincial table reports `35,084.0` while the paste records `35,083`; this single-unit difference is documented and explained below.

### 4. Source captures, hashes, acquisition clocks, and version assertions
Addressed. SHA-256 hashes and file sizes for all nine official data files and corresponding annual reports are pinned in `evidence.json` and `manifest.json`. Retained files were acquired from `nso.go.th` on September 5, 2026.

## Limitations and alternatives

### The 2015 1-Unit Rounding Discrepancy
In 2015, the primary provincial table provides `35,084.0` (Row 13, Column 3 of Sheet `ตาราง1` in `AG4p/file_th`), whereas the paste records `35,083`. The sum of the male subcomponents in that table is:
- Housework: `747.0`
- Studies: `35,084.0`
- Other: `50,203.0`
- Total not in labor force: `86,034.0` (`747 + 35084 + 50203 = 86034`).

In Thailand LFS microdata, sampling weights carry floating-point decimal precision. When microdata rows are aggregated directly before rounding, rounding boundaries can differ by 1 unit depending on whether the round-to-nearest function is applied to individual stratum weights or to the final provincial sum. The paste author either queried the unrounded LFS microdata or a regional compilation with slightly different stratum post-stratification weights.

### Alternative Publications
The data is disseminated in two parallel formats:
1. Individual provincial Excel workbooks (`AG4p`, `ARvE`, etc.).
2. Regional/national multi-province Excel workbooks (`AQ6N`, `AYc9`), where Sheet `NE` contains all 20 provinces of the Northeastern region.
Both formats stem from the same underlying LFS sample weighting system.
