# BeFree Power Index v151.1
# BPI DATA SPECIFICATION

**Document:** BPI_DATA_SPEC.md  
**Project:** BeFree Power Index v151.1  
**Data Layer:** BPI Data Specification  
**Status:** Official Data Specification  
**BPI v1.0 Formula:** LOCKED  
**BPI v2.0 Formula:** NOT YET LOCKED  

---

# 1. PURPOSE

BPI DATA SPECIFICATION defines the official data standards used by the BeFree Power Index system.

The specification establishes:

- Required data inputs
- Data definitions
- Data validation
- Data consistency
- Data timestamping
- Data versioning
- Data traceability
- Data reproducibility
- Historical data recording
- Data quality control
- Data separation between BPI engine versions

The purpose is to ensure that every BPI result can be:

- Reproduced
- Tested
- Audited
- Compared
- Evaluated
- Traced to its original data source

---

# 2. DATA PRINCIPLES

All BPI data must follow these principles:

1. Accurate
2. Complete
3. Consistent
4. Traceable
5. Timestamped
6. Versioned
7. Reproducible

Data must represent the actual approved source data.

Data must not be manipulated to produce a preferred BPI result.

Data must not be changed because of:

- Team popularity
- Personal preference
- Expected prediction
- Market opinion
- Social media sentiment
- Desired ranking

---

# 3. DATA SNAPSHOT

Every BPI calculation must be associated with a Data Snapshot.

Minimum Snapshot information:

- Snapshot ID
- Snapshot Date
- Snapshot Time
- Competition
- Season
- Data Source
- Extraction Timestamp
- Data Specification Version
- BPI Engine Version
- Data Quality Status

Example:

Snapshot ID:
EPL-2026-09-11-001

Competition:
English Premier League

Season:
2026/27

Snapshot Time:
2026-09-11 12:00:00 UTC

Data Specification:
1.0

BPI Engine:
v1.0

Quality Status:
VALID

---

# 4. DATA CONSISTENCY

All teams included in one BPI calculation must use the same approved Data Snapshot.

The system must not mix:

- Different dates
- Different league tables
- Different seasons
- Different data sources
- Different calculation snapshots

within the same BPI calculation.

Example:

If Team A uses data from 11 September 2026, all other teams in the same calculation must also use the approved 11 September 2026 snapshot.

---

# 5. BPI v1.0 REQUIRED DATA

BPI v1.0 requires the following raw data:

1. Team
2. Played
3. Wins
4. Draws
5. Losses
6. Goals For
7. Goals Against
8. Points
9. Recent Form

These data fields form the official input layer for BPI v1.0.

---

# 6. BPI v1.0 RAW DATA DEFINITIONS

## 6.1 Team

Definition:

Official team name used by the approved competition data source.

Constraint:

- Must not be empty
- Must be unique within a snapshot

---

## 6.2 Played

Definition:

Number of matches played by the team.

Constraint:

- Must be greater than 0 for official BPI calculation
- Must be an integer

---

## 6.3 Wins

Definition:

Number of matches won.

Constraint:

- Must be non-negative
- Must be an integer

---

## 6.4 Draws

Definition:

Number of matches drawn.

Constraint:

- Must be non-negative
- Must be an integer

---

## 6.5 Losses

Definition:

Number of matches lost.

Constraint:

- Must be non-negative
- Must be an integer

---

## 6.6 Played Consistency

The following relationship must always be satisfied:

W + D + L = P

Where:

W = Wins  
D = Draws  
L = Losses  
P = Played

If this condition is violated, the dataset is INVALID.

---

## 6.7 Goals For

Definition:

Total goals scored by the team.

Constraint:

- Must be non-negative
- Must be an integer

---

## 6.8 Goals Against

Definition:

Total goals conceded by the team.

Constraint:

- Must be non-negative
- Must be an integer

---

## 6.9 Points

For a standard three-point league system:

Points = (3 × Wins) + Draws

The recorded Points value must be consistent with Wins and Draws.

If the competition uses a different official points system, the system must explicitly identify the competition-specific rule before calculation.

---

## 6.10 Recent Form

Recent Form represents the team's recent performance.

Recent Form contributes 15% to the BPI v1.0 formula.

The exact encoding method is currently:

PENDING FORM ENCODING LOCK

Therefore, no implementation may treat a proposed Recent Form encoding as permanently official until it has been explicitly locked.

---

# 7. RECENT FORM

Recent Form is an official BPI v1.0 component with a weight of 15%.

However, the final data encoding method has not yet been permanently locked.

Status:

PENDING FORM ENCODING LOCK

The final encoding must be:

- Clearly defined
- Testable
- Reproducible
- Historically applicable
- Consistent across teams
- Documented before production implementation

---

# 8. PROPOSED RECENT FORM ENCODING

The following method is a proposed candidate only.

It is NOT currently the final official encoding.

For the last five matches:

Win = 3 points  
Draw = 1 point  
Loss = 0 points

Maximum possible points:

15

Proposed formula:

RecentForm = (PointsLast5 / 15) × 100

Example:

Results:

W - W - D - L - W

Points:

3 + 3 + 1 + 0 + 3 = 10

Proposed Recent Form:

(10 / 15) × 100 = 66.67

IMPORTANT:

This method remains PROPOSED until the Recent Form encoding is explicitly locked.

---

# 9. DERIVED DATA

The following metrics are derived from raw data.

## 9.1 Points Per Game

PPG = Points / Played

---

## 9.2 Goal Difference

GD = Goals For - Goals Against

---

## 9.3 Goal Difference Per Match

GD/Match = GD / Played

---

## 9.4 Win Rate

WinRate = (Wins / Played) × 100

---

## 9.5 Goals For Per Match

GF/Match = Goals For / Played

---

## 9.6 Goals Against Per Match

GA/Match = Goals Against / Played

---

## 9.7 Defensive Score

Lower Goals Against Per Match is better.

Formula:

DefensiveScore = ((GAmax - GAi) / (GAmax - GAmin)) × 100

Where:

GAmax = highest GA/Match in the dataset

GAmin = lowest GA/Match in the dataset

GAi = team's GA/Match

If:

GAmax = GAmin

then:

DefensiveScore = 50

for all teams.

---

# 10. INPUT → DERIVED → SCORE FLOW

The official data processing flow is:

RAW DATA

↓

DATA VALIDATION

↓

DERIVED METRICS

↓

NORMALIZATION

↓

BPI v1.0 CALCULATION

↓

BPI SCORE

↓

POWER RANKING

↓

HISTORICAL RECORD

The system must not bypass the validation layer.

---

# 11. DATA VALIDATION

Before BPI calculation, the system must validate:

1. Played > 0
2. Wins >= 0
3. Draws >= 0
4. Losses >= 0
5. Goals For >= 0
6. Goals Against >= 0
7. Wins + Draws + Losses = Played
8. Points >= 0
9. Points are consistent with the official competition points system
10. Team name is not empty
11. Team name is unique within the snapshot
12. All teams use the same approved snapshot
13. Required data fields are present
14. No division by zero is possible

If a required validation fails, the dataset must not be used for an official BPI result.

---

# 12. MISSING DATA

Required data must not be silently estimated.

If a required field is missing:

DATA QUALITY STATUS = INVALID

The system must not automatically:

- Guess the value
- Copy another team's value
- Use an outdated value without documentation
- Replace the value with zero
- Use an AI-generated estimate

Any approved exception must be explicitly documented.

---

# 13. DUPLICATE DATA

A team must appear only once within the same Data Snapshot.

Duplicate team records are invalid unless they represent explicitly different entities according to the competition's official data structure.

If duplicate records exist:

DATA QUALITY STATUS = INVALID

The dataset must be corrected before official BPI calculation.

---

# 14. DATA SOURCE

Every official dataset must identify its source.

Minimum source information:

- Source Name
- Source Reference
- Extraction Date
- Extraction Time
- Extraction Timestamp
- Relevant Competition
- Relevant Season

The source must be traceable.

---

# 15. DATA TIMESTAMP

All official data extraction timestamps should use:

YYYY-MM-DD HH:MM:SS UTC

Example:

2026-09-11 12:00:00 UTC

The timestamp identifies the exact point at which the approved dataset was collected.

---

# 16. DATA VERSIONING

Current Data Specification Version:

DATA_SPEC_VERSION = 1.0

A material structural change to the data specification requires a new specification version.

Examples of material changes:

- New mandatory data field
- Removal of a mandatory data field
- Change to field meaning
- Change to validation rules
- Change to data architecture

Minor documentation corrections that do not change data behavior may be recorded without changing the specification version, subject to project governance.

---

# 17. BPI ENGINE VERSION

Every official BPI result must store the BPI Engine Version used to produce it.

Example:

BPI_ENGINE_VERSION = v1.0

The system must preserve the relationship between:

- Data Snapshot
- Data Specification Version
- BPI Engine Version
- Formula Version

Same approved data + same specification + same engine version + same formula must produce the same BPI result.

---

# 18. HISTORICAL DATA RECORD

Every official historical BPI record should preserve:

- Snapshot ID
- Snapshot Date
- Competition
- Season
- Team
- Played
- Wins
- Draws
- Losses
- Goals For
- Goals Against
- Points
- Recent Form
- Derived Metrics
- Normalized Scores
- BPI Score
- Power Ranking
- BPI Engine Version
- Data Specification Version
- Data Source

Historical records must be sufficient to reproduce the calculation.

---

# 19. DATA IMMUTABILITY

Historical BPI records should not be silently overwritten.

If an error is discovered:

1. Preserve the original record.
2. Identify the error.
3. Create a corrected Data Snapshot.
4. Record the correction.
5. Preserve an audit trail.
6. Recalculate only under the appropriate version and snapshot.

This prevents historical results from being silently rewritten.

---

# 20. BPI v2.0 DATA

BPI v2.0 is designed as a Match Engine.

Potential match-level data includes:

- Match ID
- Match Date
- Competition
- Season
- Home Team
- Away Team
- Venue
- Recent Performance
- Home Form
- Away Form
- Opponent Strength
- Starting XI Strength
- Injury Status
- Suspension Status
- Bench Strength
- Momentum
- Goal Timing Profile
- Matchup Information

BPI v2.0 data requirements may expand during development.

The final mathematical model is NOT YET LOCKED.

---

# 21. DATA SEPARATION

BPI v1.0 and BPI v2.0 have different purposes.

BPI v1.0:

League / competition power ranking.

BPI v2.0:

Specific match evaluation.

Match-specific information must not silently enter BPI v1.0.

BPI v1.0 historical results must remain reproducible independently of BPI v2.0.

---

# 22. DATA QUALITY STATUS

Each dataset must have a quality status.

Allowed statuses:

VALID

The dataset passed all required validation rules.

WARNING

The dataset contains a documented issue that does not necessarily invalidate the intended calculation.

INVALID

The dataset fails one or more mandatory validation requirements.

Official BPI production results should normally be generated only from VALID data.

---

# 23. DATA AUDIT

The complete data audit chain should be traceable through:

SOURCE

↓

SNAPSHOT

↓

RAW DATA

↓

VALIDATION

↓

DERIVED METRICS

↓

NORMALIZATION

↓

BPI CALCULATION

↓

BPI SCORE

↓

POWER RANKING

↓

HISTORICAL RECORD

An auditor should be able to trace a BPI result back to its source data.

---

# 24. REPRODUCIBILITY

Official reproducibility principle:

Same Data + Same Specification + Same Engine Version + Same Formula = Same BPI Result

This principle is mandatory for the BPI system.

A different result must be explainable by a documented difference in:

- Data
- Specification
- Engine Version
- Formula
- Calculation procedure

---

# 25. DATA SECURITY AND INTEGRITY

BPI data must not be manipulated to produce a preferred result.

The system must remain independent from:

- Team preference
- Fan preference
- Social media popularity
- Betting preference
- Personal opinion
- Commercial interest
- Expected outcome

The data layer exists to provide objective inputs to the BPI engine.

---

# 26. GOLDEN TEST REQUIREMENT

Before production implementation, the BPI system must have at least one Golden Test Case.

The Golden Test Case must contain:

- Complete input data
- Valid data structure
- Defined Data Snapshot
- Defined Data Specification Version
- Defined BPI Engine Version
- Expected derived metrics
- Expected normalized scores
- Expected BPI scores
- Expected ranking
- Expected Power Gap where applicable

The Golden Test must be:

- Deterministic
- Repeatable
- Documented
- Reproducible

If the specification and engine remain unchanged, the expected result must remain unchanged.

---

# 27. CHANGE GOVERNANCE

Changes to the data layer must be classified.

## Minor Change

Examples:

- Typographical correction
- Documentation clarification
- Non-functional formatting correction

Minor changes may not require a new engine version if calculation behavior remains unchanged.

## Material Change

Examples:

- New mandatory data field
- Changed data definition
- Changed validation rule
- Changed calculation input
- Changed formula-related data behavior

Material changes must be:

1. Documented
2. Tested
3. Evaluated
4. Recorded in CHANGELOG.md
5. Assigned the appropriate version

No material change may be silently introduced.

---

# 28. SOURCE OF TRUTH

The BPI project documentation hierarchy is:

BPI_MASTER_SPEC.md

↓

BPI_v1.0.md / BPI_v2.0.md

↓

BPI_DATA_SPEC.md

↓

TEST CASES

↓

IMPLEMENTATION

The implementation must follow the approved specifications.

If implementation conflicts with the specification, the specification must be reviewed before changing the formula or behavior.

---

# 29. CURRENT STATUS

Current BPI Data Layer status:

BPI v1.0 Formula:
LOCKED

BPI v1.0 Data Structure:
DEFINED

BPI v1.0 Required Data:
DEFINED

Data Validation:
DEFINED

Data Snapshot:
DEFINED

Historical Data Structure:
DEFINED

Data Audit:
DEFINED

Data Reproducibility:
DEFINED

Recent Form Encoding:
PENDING FORM ENCODING LOCK

BPI v2.0 Data Architecture:
DEFINED

BPI v2.0 Final Formula:
NOT YET LOCKED

Calculation Engine:
NOT YET IMPLEMENTED

Golden Test:
NOT YET IMPLEMENTED

Evaluation Engine:
NOT YET IMPLEMENTED

---

# 30. OFFICIAL PRINCIPLE

The BeFree Power Index data layer must ensure that every BPI result is:

- Traceable
- Testable
- Repeatable
- Comparable
- Auditable
- Evaluatable
- Reproducible
- Developable without breaking historical versions

The BPI system is proprietary.

All methodology, specifications, formulas, data structures, testing procedures, source code, evaluation methods, historical records, and documentation are proprietary to the BeFree Power Index project.

No open-source license is granted unless explicitly authorized by the project owner.

---

# END OF BPI DATA SPECIFICATION
