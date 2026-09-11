# BeFree Power Index v151.1
# BPI GOLDEN TEST CASE 001

**Test ID:** BPI-GOLDEN-001  
**Project:** BeFree Power Index v151.1  
**Engine:** BPI v1.0  
**Engine Name:** Power Ranking Engine  
**Data Specification:** v1.0  
**Test Type:** Golden Test  
**Status:** OFFICIAL REFERENCE TEST  

---

# 1. PURPOSE

BPI-GOLDEN-001 is the first official deterministic reference test for BPI v1.0.

The purpose of this test is to verify that an implementation of BPI v1.0 correctly performs:

- Data validation
- Derived metric calculation
- Recent Form processing
- Min-max normalization
- Defensive score calculation
- Weighted BPI calculation
- Power Ranking
- Power Gap

This test uses a controlled synthetic dataset.

The dataset is intentionally independent from live competition data so that the expected result remains stable.

---

# 2. TEST PRINCIPLE

The following principle applies:

Same Data

+

Same Data Specification

+

Same BPI Engine Version

+

Same Formula

=

Same BPI Result

Any implementation that produces a different result must be investigated.

---

# 3. DATA SNAPSHOT

Snapshot ID:

BPI-GOLDEN-001-SNAPSHOT

Competition:

Synthetic Test Competition

Season:

Golden Test Season

Snapshot Date:

2026-09-11

Snapshot Time:

12:00:00 UTC

Data Source:

BPI Controlled Synthetic Dataset

Data Specification Version:

1.0

BPI Engine Version:

v1.0

Data Quality Status:

VALID

---

# 4. TEST DATASET

The dataset contains five synthetic teams.

| Team | P | W | D | L | GF | GA | Points | Recent Form |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Alpha FC | 10 | 8 | 1 | 1 | 24 | 8 | 25 | 80 |
| Bravo FC | 10 | 6 | 2 | 2 | 20 | 10 | 20 | 67 |
| Charlie FC | 10 | 5 | 2 | 3 | 17 | 13 | 17 | 53 |
| Delta FC | 10 | 3 | 3 | 4 | 13 | 17 | 12 | 40 |
| Echo FC | 10 | 1 | 2 | 7 | 8 | 24 | 5 | 27 |

Validation:

Alpha FC:

8 + 1 + 1 = 10

Bravo FC:

6 + 2 + 2 = 10

Charlie FC:

5 + 2 + 3 = 10

Delta FC:

3 + 3 + 4 = 10

Echo FC:

1 + 2 + 7 = 10

Points validation:

Alpha FC:

3(8) + 1 = 25

Bravo FC:

3(6) + 2 = 20

Charlie FC:

3(5) + 2 = 17

Delta FC:

3(3) + 3 = 12

Echo FC:

3(1) + 2 = 5

All validation rules pass.

---

# 5. RECENT FORM TEST CONDITION

For this Golden Test, Recent Form values are supplied directly as controlled input values.

The values are:

Alpha FC = 80

Bravo FC = 67

Charlie FC = 53

Delta FC = 40

Echo FC = 27

These values are used only to test the BPI calculation pipeline.

IMPORTANT:

The final official Recent Form encoding remains:

PENDING FORM ENCODING LOCK

Therefore, this Golden Test does not lock the underlying production encoding method.

---

# 6. DERIVED METRICS

## Alpha FC

PPG:

25 / 10 = 2.5000

GD:

24 - 8 = 16

GD/Match:

16 / 10 = 1.6000

Win Rate:

8 / 10 × 100 = 80.0000

GF/Match:

24 / 10 = 2.4000

GA/Match:

8 / 10 = 0.8000

---

## Bravo FC

PPG:

20 / 10 = 2.0000

GD:

20 - 10 = 10

GD/Match:

10 / 10 = 1.0000

Win Rate:

6 / 10 × 100 = 60.0000

GF/Match:

20 / 10 = 2.0000

GA/Match:

10 / 10 = 1.0000

---

## Charlie FC

PPG:

17 / 10 = 1.7000

GD:

17 - 13 = 4

GD/Match:

4 / 10 = 0.4000

Win Rate:

5 / 10 × 100 = 50.0000

GF/Match:

17 / 10 = 1.7000

GA/Match:

13 / 10 = 1.3000

---

## Delta FC

PPG:

12 / 10 = 1.2000

GD:

13 - 17 = -4

GD/Match:

-4 / 10 = -0.4000

Win Rate:

3 / 10 × 100 = 30.0000

GF/Match:

13 / 10 = 1.3000

GA/Match:

17 / 10 = 1.7000

---

## Echo FC

PPG:

5 / 10 = 0.5000

GD:

8 - 24 = -16

GD/Match:

-16 / 10 = -1.6000

Win Rate:

1 / 10 × 100 = 10.0000

GF/Match:

8 / 10 = 0.8000

GA/Match:

24 / 10 = 2.4000

---

# 7. NORMALIZATION RANGES

## PPG

Minimum:

0.5000

Maximum:

2.5000

Range:

2.0000

---

## GD/Match

Minimum:

-1.6000

Maximum:

1.6000

Range:

3.2000

---

## Win Rate

Minimum:

10.0000

Maximum:

80.0000

Range:

70.0000

---

## Recent Form

Minimum:

27

Maximum:

80

Range:

53

---

## GF/Match

Minimum:

0.8000

Maximum:

2.4000

Range:

1.6000

---

## GA/Match

Minimum:

0.8000

Maximum:

2.4000

Range:

1.6000

---

# 8. NORMALIZED SCORES

Formula for higher-is-better components:

Score = ((x - xmin) / (xmax - xmin)) × 100

---

## Alpha FC

PPG Score:

100.0000

GD Score:

100.0000

Win Rate Score:

100.0000

Recent Form Score:

100.0000

GF Score:

100.0000

Defensive Score:

100.0000

---

## Bravo FC

PPG Score:

75.0000

GD Score:

81.2500

Win Rate Score:

71.4286

Recent Form Score:

75.4717

GF Score:

75.0000

Defensive Score:

87.5000

---

## Charlie FC

PPG Score:

60.0000

GD Score:

62.5000

Win Rate Score:

57.1429

Recent Form Score:

49.0566

GF Score:

56.2500

Defensive Score:

68.7500

---

## Delta FC

PPG Score:

35.0000

GD Score:

37.5000

Win Rate Score:

28.5714

Recent Form Score:

24.5283

GF Score:

31.2500

Defensive Score:

43.7500

---

## Echo FC

PPG Score:

0.0000

GD Score:

0.0000

Win Rate Score:

0.0000

Recent Form Score:

0.0000

GF Score:

0.0000

Defensive Score:

0.0000

---

# 9. DEFENSIVE SCORE VERIFICATION

Formula:

DefensiveScore = ((GAmax - GAi) / (GAmax - GAmin)) × 100

GAmax:

2.4000

GAmin:

0.8000

---

Alpha FC:

((2.4 - 0.8) / 1.6) × 100

= 100.0000

---

Bravo FC:

((2.4 - 1.0) / 1.6) × 100

= 87.5000

---

Charlie FC:

((2.4 - 1.3) / 1.6) × 100

= 68.7500

---

Delta FC:

((2.4 - 1.7) / 1.6) × 100

= 43.7500

---

Echo FC:

((2.4 - 2.4) / 1.6) × 100

= 0.0000

---

# 10. BPI v1.0 FORMULA

BPI =

0.30 × S_PPG

+

0.20 × S_GD

+

0.20 × S_WR

+

0.15 × S_RF

+

0.10 × S_GF

+

0.05 × S_DEF

---

# 11. BPI CALCULATION

## Alpha FC

BPI =

(0.30 × 100.0000)

+

(0.20 × 100.0000)

+

(0.20 × 100.0000)

+

(0.15 × 100.0000)

+

(0.10 × 100.0000)

+

(0.05 × 100.0000)

BPI:

100.0000

---

## Bravo FC

BPI =

(0.30 × 75.0000)

+

(0.20 × 81.2500)

+

(0.20 × 71.4286)

+

(0.15 × 75.4717)

+

(0.10 × 75.0000)

+

(0.05 × 87.5000)

BPI:

76.9589

---

## Charlie FC

BPI =

(0.30 × 60.0000)

+

(0.20 × 62.5000)

+

(0.20 × 57.1429)

+

(0.15 × 49.0566)

+

(0.10 × 56.2500)

+

(0.05 × 68.7500)

BPI:

58.1809

---

## Delta FC

BPI =

(0.30 × 35.0000)

+

(0.20 × 37.5000)

+

(0.20 × 28.5714)

+

(0.15 × 24.5283)

+

(0.10 × 31.2500)

+

(0.05 × 43.7500)

BPI:

31.9533

---

## Echo FC

BPI:

0.0000

---

# 12. EXPECTED POWER RANKING

| Rank | Team | Expected BPI |
|---:|---|---:|
| 1 | Alpha FC | 100.0000 |
| 2 | Bravo FC | 76.9589 |
| 3 | Charlie FC | 58.1809 |
| 4 | Delta FC | 31.9533 |
| 5 | Echo FC | 0.0000 |

The implementation must produce this ranking.

---

# 13. EXPECTED POWER GAP

Power Gap formula:

PowerGap(A,B) = BPI(A) - BPI(B)

---

## Alpha FC vs Bravo FC

100.0000 - 76.9589

Expected Power Gap:

23.0411

---

## Bravo FC vs Charlie FC

76.9589 - 58.1809

Expected Power Gap:

18.7780

---

## Charlie FC vs Delta FC

58.1809 - 31.9533

Expected Power Gap:

26.2276

---

## Delta FC vs Echo FC

31.9533 - 0.0000

Expected Power Gap:

31.9533

---

# 14. GOLDEN EXPECTED OUTPUT

The implementation must produce approximately:

| Rank | Team | BPI Score |
|---:|---|---:|
| 1 | Alpha FC | 100.0000 |
| 2 | Bravo FC | 76.9589 |
| 3 | Charlie FC | 58.1809 |
| 4 | Delta FC | 31.9533 |
| 5 | Echo FC | 0.0000 |

The exact internal calculation must retain sufficient precision.

Displayed rounding may be applied only at the output stage according to the approved display specification.

---

# 15. GOLDEN TEST ACCEPTANCE CRITERIA

The test passes only if:

1. All input data passes validation.
2. All derived metrics match the reference values.
