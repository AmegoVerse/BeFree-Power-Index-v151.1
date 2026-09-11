# BeFree Power Index v151.1
# BPI TEST CASES

**Document:** BPI_TEST_CASES.md  
**Project:** BeFree Power Index v151.1  
**Testing Layer:** BPI Testing Specification  
**Status:** Official Testing Specification  
**BPI v1.0 Formula:** LOCKED  
**BPI v2.0 Formula:** NOT YET LOCKED  

---

# 1. PURPOSE

This document defines the official testing standards for the BeFree Power Index system.

The purpose of BPI testing is to ensure that:

- Data is processed correctly
- Validation rules are enforced
- Derived metrics are calculated correctly
- Normalization is correct
- BPI scores are calculated correctly
- Rankings are deterministic
- Power Gap is calculated correctly
- BPI Change is calculated correctly
- Invalid data is rejected
- Historical results remain reproducible
- Future engine changes do not silently break previous behavior

Testing is part of the official BPI development process.

---

# 2. TESTING PRINCIPLES

All BPI tests must follow these principles:

1. Deterministic
2. Reproducible
3. Traceable
4. Independent
5. Version-aware
6. Data-driven
7. Formula-driven
8. Regression-safe

A test must have clearly defined:

- Input
- Expected behavior
- Expected output
- Test condition
- Test status

---

# 3. TESTING SCOPE

Testing covers the following BPI system layers:

DATA

↓

VALIDATION

↓

DERIVED METRICS

↓

NORMALIZATION

↓

BPI CALCULATION

↓

RANKING

↓

POWER GAP

↓

BPI CHANGE

↓

HISTORICAL RECORD

Testing may also cover system integrity and reproducibility.

---

# 4. TEST CASE IDENTIFICATION

Every official test case must have a unique ID.

Format:

BPI-TC-XXX

Example:

BPI-TC-001

BPI-TC-002

BPI-TC-003

Test IDs must not be reused for different test definitions.

---

# 5. TEST CASE STRUCTURE

Each test case should contain:

Test ID

Test Name

Purpose

Input Data

Preconditions

Test Procedure

Expected Result

Actual Result

Status

Notes

Example structure:

Test ID:
BPI-TC-001

Test Name:
Valid Basic Dataset

Purpose:
Verify that a valid dataset passes validation.

Input:
Valid team statistics using one approved snapshot.

Expected Result:
Validation status = VALID

Actual Result:
To be recorded during testing.

Status:
PENDING

---

# 6. TEST CATEGORIES

Official BPI testing categories include:

## Category A — Data Validation

Tests whether input data follows the official data specification.

## Category B — Derived Metrics

Tests calculations such as:

- PPG
- GD
- GD/Match
- Win Rate
- GF/Match
- GA/Match
- Defensive Score

## Category C — Normalization

Tests normalized component scores.

## Category D — BPI Calculation

Tests the official BPI v1.0 formula.

## Category E — Ranking

Tests sorting and ranking behavior.

## Category F — Power Gap

Tests the difference between team BPI scores.

## Category G — BPI Change

Tests changes between snapshots.

## Category H — Invalid Data

Tests rejection of invalid or incomplete data.

## Category I — Reproducibility

Tests whether identical input produces identical output.

## Category J — Regression

Tests whether future implementation changes alter previously validated behavior.

## Category K — Golden Test

Tests the official reference calculation used as the primary BPI v1.0 benchmark.

---

# 7. DATA VALIDATION TESTS

## BPI-TC-001 — Valid Dataset

Purpose:

Verify that a complete and internally consistent dataset is accepted.

Conditions:

- Team is present
- Played > 0
- Wins >= 0
- Draws >= 0
- Losses >= 0
- GF >= 0
- GA >= 0
- W + D + L = P
- Points are valid
- No duplicate team
- Same approved snapshot

Expected Result:

DATA QUALITY STATUS = VALID

Status:

PENDING

---

## BPI-TC-002 — Missing Required Field

Purpose:

Verify that missing required data is rejected.

Test:

Remove one mandatory input field.

Expected Result:

DATA QUALITY STATUS = INVALID

Official BPI calculation must not proceed.

Status:

PENDING

---

## BPI-TC-003 — Invalid Played Value

Purpose:

Verify that Played = 0 or a negative value is rejected for official BPI calculation.

Expected Result:

INVALID

Status:

PENDING

---

## BPI-TC-004 — Invalid Win/Draw/Loss Relationship

Purpose:

Verify:

W + D + L = P

Test:

Provide a dataset where the relationship is false.

Expected Result:

INVALID

Status:

PENDING

---

## BPI-TC-005 — Negative Goals

Purpose:

Verify that negative GF or GA values are rejected.

Expected Result:

INVALID

Status:

PENDING

---

## BPI-TC-006 — Invalid Points

Purpose:

Verify that Points is consistent with the official competition scoring system.

For a standard three-point league:

Points = 3W + D

Expected Result:

If inconsistent:

INVALID

Status:

PENDING

---

## BPI-TC-007 — Duplicate Team

Purpose:

Verify that the same team cannot appear twice within the same snapshot.

Expected Result:

INVALID

Status:

PENDING

---

## BPI-TC-008 — Mixed Snapshot

Purpose:

Verify that teams from different snapshots cannot be silently combined.

Expected Result:

INVALID

Status:

PENDING

---

# 8. DERIVED METRIC TESTS

## BPI-TC-009 — Points Per Game

Formula:

PPG = Points / Played

Expected Result:

Calculated value must match the reference calculation.

Status:

PENDING

---

## BPI-TC-010 — Goal Difference

Formula:

GD = GF - GA

Expected Result:

Calculated value must match the reference calculation.

Status:

PENDING

---

## BPI-TC-011 — Goal Difference Per Match

Formula:

GD/Match = GD / Played

Expected Result:

Calculated value must match the reference calculation.

Status:

PENDING

---

## BPI-TC-012 — Win Rate

Formula:

WinRate = (Wins / Played) × 100

Expected Result:

Calculated value must match the reference calculation.

Status:

PENDING

---

## BPI-TC-013 — Goals For Per Match

Formula:

GF/Match = GF / Played

Expected Result:

Calculated value must match the reference calculation.

Status:

PENDING

---

## BPI-TC-014 — Goals Against Per Match

Formula:

GA/Match = GA / Played

Expected Result:

Calculated value must match the reference calculation.

Status:

PENDING

---

## BPI-TC-015 — Defensive Score

Formula:

DefensiveScore = ((GAmax - GAi) / (GAmax - GAmin)) × 100

Expected Result:

Lower GA/Match produces a higher Defensive Score.

Status:

PENDING

---

## BPI-TC-016 — Defensive Score Zero Range

Condition:

GAmax = GAmin

Expected Result:

Defensive Score = 50 for all teams.

Status:

PENDING

---

# 9. RECENT FORM TESTS

Recent Form is a 15% component of BPI v1.0.

The final encoding method is currently:

PENDING FORM ENCODING LOCK

Therefore, no test may permanently lock a specific Recent Form encoding until the method is officially approved.

A proposed five-match method may be tested separately as an experimental test.

Proposed method:

Win = 3

Draw = 1

Loss = 0

RecentForm = PointsLast5 / 15 × 100

Experimental results must not be treated as official BPI v1.0 behavior until the encoding is locked.

---

# 10. NORMALIZATION TESTS

BPI v1.0 uses min-max normalization.

For higher-is-better metrics:

Score = ((x - xmin) / (xmax - xmin)) × 100

Tests must verify:

- Minimum value produces 0
- Maximum value produces 100
- Intermediate values are proportional
- Ranking direction is correct

---

## BPI-TC-017 — Higher-Is-Better Normalization

Expected behavior:

Highest input receives 100.

Lowest input receives 0.

Status:

PENDING

---

## BPI-TC-018 — Lower-Is-Better Defensive Normalization

Expected behavior:

Lowest GA/Match receives the highest Defensive Score.

Highest GA/Match receives the lowest Defensive Score.

Status:

PENDING

---

## BPI-TC-019 — Zero Range Normalization

Condition:

xmax = xmin

Expected Result:

All teams receive 50.

Status:

PENDING

---

# 11. BPI v1.0 CALCULATION TESTS

Official BPI v1.0 formula:

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

The component weights must total:

100%

or:

1.00

Expected Result:

The implementation must reproduce the approved formula exactly.

---

## BPI-TC-020 — Weight Sum

Verify:

0.30 + 0.20 + 0.20 + 0.15 + 0.10 + 0.05 = 1.00

Expected Result:

PASS

Status:

PENDING

---

## BPI-TC-021 — BPI Component Calculation

Purpose:

Verify that each normalized component is multiplied by the correct weight.

Expected Result:

Each component contributes according to the official BPI v1.0 formula.

Status:

PENDING

---

## BPI-TC-022 — Complete BPI Calculation

Purpose:

Verify complete BPI v1.0 calculation from validated input data.

Expected Result:

Calculated BPI matches the approved reference result.

Status:

PENDING

---

# 12. RANKING TESTS

BPI Ranking is based on descending BPI Score.

Highest BPI:

Rank 1

Second highest:

Rank 2

And so on.

---

## BPI-TC-023 — Ranking Order

Purpose:

Verify that teams are sorted from highest BPI to lowest BPI.

Expected Result:

Descending BPI order.

Status:

PENDING

---

## BPI-TC-024 — Ranking Stability

Purpose:

Verify that identical inputs always produce identical rankings.

Expected Result:

Same ranking every time.

Status:

PENDING

---

# 13. POWER GAP TESTS

Power Gap:

PowerGap(A,B) = BPI(A) - BPI(B)

Absolute Power Gap:

|PowerGap| = |BPI(A) - BPI(B)|

---

## BPI-TC-025 — Positive Power Gap

Condition:

BPI(A) > BPI(B)

Expected Result:

PowerGap(A,B) > 0

Status:

PENDING

---

## BPI-TC-026 — Negative Power Gap

Condition:

BPI(A) < BPI(B)

Expected Result:

PowerGap(A,B) < 0

Status:

PENDING

---

## BPI-TC-027 — Equal Power

Condition:

BPI(A) = BPI(B)

Expected Result:

PowerGap = 0

Status:

PENDING

---

# 14. BPI CHANGE TESTS

BPI Change:

BPIChange(t) = BPI(t) - BPI(t-1)

---

## BPI-TC-028 — Positive BPI Change

Condition:

Current BPI > Previous BPI

Expected Result:

Positive BPI Change.

Status:

PENDING

---

## BPI-TC-029 — Negative BPI Change

Condition:

Current BPI < Previous BPI

Expected Result:

Negative BPI Change.

Status:

PENDING

---

## BPI-TC-030 — Zero BPI Change

Condition:

Current BPI = Previous BPI

Expected Result:

BPI Change = 0

Status:

PENDING

---

# 15. REPRODUCIBILITY TESTS

Reproducibility is a mandatory BPI requirement.

The following must remain identical:

Same Data

+

Same Data Specification

+

Same BPI Engine Version

+

Same Formula

=

Same BPI Result

---

## BPI-TC-031 — Identical Input Reproduction

Run the same dataset multiple times.

Expected Result:

Identical BPI scores and ranking.

Status:

PENDING

---

## BPI-TC-032 — Version Reproduction

Run the same dataset using the same engine version.

Expected Result:

Identical result.

Status:

PENDING

---

# 16. INVALID DATA TESTS

Invalid datasets must not generate an official BPI result.

Invalid conditions include:

- Missing required field
- Invalid Played
- Invalid W/D/L relationship
- Negative goals
- Invalid Points
- Duplicate team
- Mixed snapshot
- Invalid data structure
- Division-by-zero condition

Expected behavior:

Reject the dataset or mark it INVALID.

The system must not silently produce an official BPI result from invalid data.

---

# 17. ROUNDING TESTS

The BPI engine must retain sufficient internal precision.

Intermediate values must not be unnecessarily rounded.

Rounding should occur at the output stage according to the approved display specification.

Tests must verify that premature rounding does not materially alter the final result.

---

## BPI-TC-033 — Intermediate Precision

Purpose:

Verify that intermediate calculations retain sufficient precision.

Expected Result:

Final BPI result matches the reference calculation within the approved output precision.

Status:

PENDING

---

# 18. HISTORICAL DATA TESTS

Historical records must preserve the calculation context.

Each historical record should identify:

- Snapshot
- Data Specification Version
- Engine Version
- Formula
- Team
- Input Data
- Derived Data
- BPI Score
- Ranking

---

## BPI-TC-034 — Historical Record Integrity

Purpose:

Verify that historical BPI results retain sufficient information for reproduction.

Expected Result:

Historical result can be traced back to its source data and calculation version.

Status:

PENDING

---

# 19. DATA IMMUTABILITY TESTS

Historical results must not be silently overwritten.

---

## BPI-TC-035 — Historical Record Protection

Purpose:

Verify that a corrected dataset creates a new documented snapshot instead of silently modifying an old result.

Expected Result:

Original historical record remains traceable.

Status:

PENDING

---

# 20. REGRESSION TESTS

Regression testing ensures that future changes do not unintentionally alter previously validated behavior.

Every validated test case may become part of the regression test suite.

When the engine is updated:

1. Run existing regression tests.
2. Compare results.
3. Identify differences.
4. Determine whether differences are intentional.
5. Document approved changes.
6. Update the relevant version when required.

A failed regression test must not be ignored.

---

## BPI-TC-036 — Regression Integrity

Purpose:

Verify that an engine update does not change previously validated BPI v1.0 behavior without documented justification.

Expected Result:

PASS if unchanged.

If changed:

Difference must be explained and documented.

Status:

PENDING

---

# 21. GOLDEN TEST CASE

The Golden Test Case is the primary reference test for BPI v1.0.

The Golden Test must contain:

- Official input dataset
- Data Snapshot
- Data Specification Version
- BPI Engine Version
- Raw data
- Derived metrics
- Normalized scores
- Recent Form value
- BPI component calculations
- Final BPI Score
- Ranking
- Power Gap where applicable
- Expected output

The Golden Test must be deterministic.

The Golden Test must not depend on live data.

The Golden Test must remain unchanged unless:

- The specification changes
- The engine version changes
- A documented test correction is approved

---

# 22. GOLDEN TEST IDENTIFICATION

The first official Golden Test will be:

BPI-GOLDEN-001

Status:

NOT YET CREATED

The Golden Test will be created after the Testing Specification is approved.

---

# 23. TEST RESULT STATUS

Allowed test statuses:

PASS

The implementation matches the expected result.

FAIL

The implementation does not match the expected result.

PENDING

The test has not yet been executed.

BLOCKED

The test cannot be executed because a required dependency is unavailable.

NOT APPLICABLE

The test does not apply to the current engine or dataset.

---

# 24. TEST RESULT RECORDING

Each completed test should record:

- Test ID
- Execution Date
- Engine Version
- Data Specification Version
- Input Reference
- Expected Result
- Actual Result
- Status
- Notes

Example:

Test ID:
BPI-TC-001

Execution Date:
YYYY-MM-DD

Engine Version:
v1.0

Expected:
VALID

Actual:
VALID

Status:
PASS

Notes:
Dataset passed all mandatory validation rules.

---

# 25. TEST ENVIRONMENT

Testing should identify the environment used.

Recommended information:

- BPI Engine Version
- Data Specification Version
- Operating Environment
- Implementation Version
- Test Dataset Version
- Execution Timestamp

The purpose is to improve reproducibility.

---

# 26. TEST INDEPENDENCE

Testing must not be designed to force a preferred team ranking.

Test datasets should be constructed to verify mathematical behavior.

The test outcome must be determined by the specification and input data.

Testing must not be changed merely because an expected result is undesirable.

---

# 27. BPI v1.0 TESTING RULE

BPI v1.0 is the baseline Power Ranking Engine.

Testing must preserve the locked BPI v1.0 formula.

No test may introduce:

- New weights
- New formula components
- Match-specific adjustments
- Squad adjustments
- Injury adjustments
- Home/Away adjustments

into BPI v1.0 unless the official engine specification is changed through the project's version governance.

---

# 28. BPI v2.0 TESTING

BPI v2.0 will require a separate testing layer when its formula is finalized.

Potential test categories include:

- Match Strength
- Match Gap
- Win Probability
- Draw Probability
- Loss Probability
- Confidence
- Recent Form
- Home/Away Form
- Opponent Strength
- Starting XI
- Injury Impact
- Suspension Impact
- Bench Strength
- Momentum
- Goal Timing Profile

BPI v2.0 tests must not overwrite BPI v1.0 tests.

---

# 29. TESTING WORKFLOW

Official testing workflow:

TEST DATA

↓

VALIDATE DATA

↓

CALCULATE DERIVED METRICS

↓

NORMALIZE COMPONENTS

↓

CALCULATE BPI

↓

VERIFY RANKING

↓

VERIFY POWER GAP

↓

VERIFY BPI CHANGE

↓

COMPARE WITH EXPECTED RESULT

↓

RECORD TEST RESULT

↓

ADD VALIDATED TEST TO REGRESSION SUITE

---

# 30. CURRENT TESTING STATUS

BPI v1.0 Formula:

LOCKED

Data Specification:

DEFINED

Testing Specification:

DEFINED

Calculation Engine:

NOT YET IMPLEMENTED

Automated Testing:

NOT YET IMPLEMENTED

Golden Test:

NOT YET CREATED

Regression Suite:

NOT YET CREATED

Evaluation Engine:

NOT YET IMPLEMENTED

BPI v2.0 Testing:

PENDING FINAL ENGINE FORMULA

---

# 31. OFFICIAL TESTING PRINCIPLE

The BPI testing system exists to ensure that the BeFree Power Index is:

- Correct
- Deterministic
- Reproducible
- Traceable
- Testable
- Stable
- Version-controlled
- Resistant to formula drift

No production BPI engine should be considered complete until it passes the required validation and Golden Test requirements.

---

# END OF BPI TEST CASES
