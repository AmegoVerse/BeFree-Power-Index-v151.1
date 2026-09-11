# BeFree Power Index v151.1
# BPI ENGINE SPECIFICATION

**Project:** BeFree Power Index v151.1
**Engine:** BPI v1.0
**Target Implementation:** Python 3.x
**Target File:** `ENGINE/BPI_v1_0_ENGINE.py`
**Status:** APPROVED & LOCKED

---

## 1. PURPOSE
The Engine Specification defines the contract for the computational implementation of BPI v1.0. The code must be a faithful translation of this contract. The engine is not allowed to modify formulas, impute missing data, or perform silent corrections.

---

## 2. ENGINE IDENTITY
The calculation engine must carry an internal identifier constant:
`ENGINE_VERSION = "BPI_v1.0_ENGINE"`
This engine must strictly implement BPI v1.0 components. It must NOT include any logic, weighting, or architecture intended for BPI v2.0 (Match Engine).

---

## 3. INPUT DATA CONTRACT
The engine must accept a tabular data structure (e.g., list of dictionaries or pandas DataFrame) representing the league table.

### 3.1 Mandatory Fields
Every team record must contain exactly these fields:
*   `team_name` (String)
*   `matches_played` (Integer)
*   `wins` (Integer)
*   `draws` (Integer)
*   `losses` (Integer)
*   `goals_for` (Integer)
*   `goals_against` (Integer)
*   `points` (Integer)
*   `recent_form_score` (Numeric Scalar - Form encoding is PENDING FORM ENCODING LOCK, but the engine accepts the pre-calculated numeric value)

---

## 4. VALIDATION & PROTECTION

### 4.1 Dataset-Level Validation (Hard Fail conditions)
The engine must reject the entire dataset and raise an Exception if ANY of these conditions are met. (No silent skipping or deletion of rows is allowed).
*   Dataset is empty.
*   Any mandatory field is missing.
*   `team_name` is empty or duplicated.
*   Any numeric field contains NaN, Null, or Infinity.
*   `matches_played`, `wins`, `draws`, `losses`, `goals_for`, `goals_against`, `points` contain non-integer or negative values.
*   `matches_played` is 0 (ZeroDivision protection).

### 4.2 Calculation-Level Validation (Hard Fail conditions)
*   `wins + draws + losses != matches_played`
*   `(wins * 3) + (draws * 1) != points`

---

## 5. MATHEMATICAL CALCULATION RULES

### 5.1 Precision and Rounding Flow
To prevent calculation drift, the engine must follow this exact order of operations:
1.  **Raw Calculation:** Calculate derived metrics and normalized scores using standard double-precision floating point. Do NOT round intermediate results.
2.  **BPI Calculation:** Calculate the `unrounded_BPI_score` (weighted sum).
3.  **Ranking:** Sort based on the `unrounded_BPI_score`.
4.  **Power Gap:** Calculate Power Gap using the `unrounded_BPI_score`.
5.  **Final Rounding:** Round the final `bpi_score` and `power_gap` to exactly 4 decimal places ONLY before the final output.

### 5.2 Zero Range Normalization
If the maximum and minimum values for any metric across the dataset are identical (`x_max == x_min`), the normalized score for that specific metric for all teams must be exactly `50.0000`.

---

## 6. DETERMINISTIC RANKING & TIE-BREAKING
The ranking output must be 100% deterministic.
1.  **Primary Sort:** Sort teams descending by `unrounded_BPI_score`.
2.  **Tie-Breaker:** If two or more teams have identical `unrounded_BPI_score`, sort them ascending alphabetically by `team_name`.
3.  **Rank Assignment:** Ranks (`bpi_rank`) are assigned sequentially from 1 to N without skipping or sharing ranks.

---

## 7. POWER GAP DEFINITION
Power Gap measures the absolute distance in BPI to the team immediately below in the ranking:
*   For any team at rank $r$ where $r < N$: 
    $$\text{PowerGap}_r = \text{unrounded\_BPI}_r - \text{unrounded\_BPI}_{r+1}$$
*   For the team at the lowest rank ($r = N$): 
    $$\text{PowerGap}_N = 0.0000$$

---

## 8. OUTPUT CONTRACT
The engine must output a clean, ranked data structure containing:
*   `bpi_rank` (Integer)
*   `team_name` (String)
*   `bpi_score` (Float, exactly 4 decimal places)
*   `power_gap` (Float, exactly 4 decimal places)
*   *(Optional)* Audit output data containing unrounded metrics for traceability.

---

## 9. GOLDEN TEST INTEGRATION
The engine file must include a callable function (`test_bpi_golden_001()`) that validates the engine's output against the `BPI-GOLDEN-001` snapshot data. The engine is only considered verified if this test returns `PASS`.
