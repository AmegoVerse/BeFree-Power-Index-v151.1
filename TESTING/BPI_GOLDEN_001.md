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
- Min-max normalization
- Defensive score calculation
- Weighted BPI calculation
- Power Ranking
- Power Gap

---

# 2. TEST DATASET

The dataset contains five synthetic teams:

| Team | P | W | D | L | GF | GA | Points | Recent Form |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Alpha FC | 10 | 8 | 1 | 1 | 24 | 8 | 25 | 80 |
| Bravo FC | 10 | 6 | 2 | 2 | 20 | 10 | 20 | 67 |
| Charlie FC | 10 | 5 | 2 | 3 | 17 | 13 | 17 | 53 |
| Delta FC | 10 | 3 | 3 | 4 | 13 | 17 | 12 | 40 |
| Echo FC | 10 | 1 | 2 | 7 | 8 | 24 | 5 | 27 |

---

# 3. GOLDEN EXPECTED OUTPUT

The implementation must produce exactly:

| Rank | Team | BPI Score | Power Gap |
|---:|---|---:|---:|
| 1 | Alpha FC | 100.0000 | 23.0411 |
| 2 | Bravo FC | 76.9589 | 18.7780 |
| 3 | Charlie FC | 58.1809 | 26.2276 |
| 4 | Delta FC | 31.9533 | 31.9533 |
| 5 | Echo FC | 0.0000 | 0.0000 |
