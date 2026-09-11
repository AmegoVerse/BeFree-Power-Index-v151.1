
BeFree Power Index v151.1

BPI Master Specification

Document Status: Official
Project: BeFree Power Index v151.1
Owner: AmegoVerse
System Type: Proprietary Football Analytics System
Specification Status: Foundation Specification

---

1. Purpose

This document defines the master architecture, principles, versioning rules, and governance of the BeFree Power Index system.

It serves as the highest-level technical specification for the BPI project.

All BPI engines, data specifications, testing procedures, evaluation systems, and future implementations must remain consistent with this specification.

---

2. Project Identity

The official project identity is:

BeFree Power Index v151.1

Project version and analytical engine versions are separate.

BeFree Power Index v151.1
│
├── BPI v1.0
│   └── Power Ranking Engine
│
└── BPI v2.0
    └── Match Engine

Version Convention

v151.1
│
├── 151 = project identity
└── .1 = build number

A new project build does not automatically mean that the BPI calculation formula has changed.

---

3. System Objectives

The BeFree Power Index system is designed to:

1. Measure football team strength.
2. Produce reproducible analytical results.
3. Provide a stable power-ranking baseline.
4. Evaluate match-specific strength.
5. Track changes in team power over time.
6. Measure prediction performance against historical outcomes.
7. Maintain historical records.
8. Support future standalone implementation.

---

4. Core Architecture

The BPI system follows this architecture:

DATA SOURCE
     ↓
DATA LAYER
     ↓
VALIDATION
     ↓
BPI CALCULATION ENGINE
     ↓
BPI OUTPUT
     ↓
EVALUATION ENGINE
     ↓
HISTORICAL RECORD

The future Match Engine extends the architecture:

                    BPI SYSTEM
                        │
              ┌─────────┴─────────┐
              ↓                   ↓
      POWER RANKING ENGINE    MATCH ENGINE
           BPI v1.0              BPI v2.0
              │                   │
              └─────────┬─────────┘
                        ↓
                 EVALUATION

---

5. BPI v1.0 — Power Ranking Engine

BPI v1.0 is the foundational engine.

Its primary purpose is:

«Measure the overall power of football teams.»

BPI v1.0 is based on league performance data and produces a normalized power score.

The core formula is locked.

Official Weighting

Component| Weight
Points Per Game| 30%
Goal Difference per Match| 20%
Win Rate| 20%
Recent Form| 15%
Goals For per Match| 10%
Defensive Score| 5%
Total| 100%

The detailed mathematical specification is maintained in:

"CORE/BPI_v1.0.md"

---

6. BPI v1.0 Formula Lock

The BPI v1.0 core formula is considered LOCKED.

The official formula is:

BPI =
0.30 × S_PPG
+ 0.20 × S_GD
+ 0.20 × S_WR
+ 0.15 × S_RF
+ 0.10 × S_GF
+ 0.05 × S_DEF

Where:

S_PPG = normalized Points Per Game
S_GD  = normalized Goal Difference per Match
S_WR  = normalized Win Rate
S_RF  = normalized Recent Form
S_GF  = normalized Goals For per Match
S_DEF = normalized Defensive Score

A fundamental change to these weights, components, or calculation methodology requires a new BPI engine version.

The formula must never be silently modified.

---

7. BPI v1.0 Outputs

The Power Ranking Engine produces:

Primary Outputs

- BPI Score
- Power Ranking

Analytical Outputs

- Power Gap
- BPI Change

Power Ranking

Teams are ranked in descending order of BPI Score.

Rank 1 = highest BPI Score
Rank 2 = second highest BPI Score
...

---

8. Power Gap

Power Gap measures the difference in BPI Score between two teams.

PowerGap(A,B) = BPI(A) - BPI(B)

Absolute Power Gap:

|PowerGap| = |BPI(A) - BPI(B)|

Power Gap does not modify the BPI Score.

It is an analytical output derived from the official BPI scores.

---

9. BPI Change

BPI Change measures movement in team power between two validated snapshots.

BPIChange(t) = BPI(t) - BPI(t-1)

Interpretation:

Positive  = power increased
Negative  = power decreased
Zero      = unchanged

BPI Change is an output and does not modify the core BPI formula.

---

10. Evaluation Layer

Evaluation is an independent layer of the BPI system.

Its purpose is to determine how accurately the system performs against historical outcomes.

Potential metrics include:

- Accuracy
- Precision
- Recall
- F1 Score
- Error Rate
- Prediction Error
- Confidence
- Calibration
- Historical Error Analysis
- Power Gap Error
- Log Loss
- Brier Score
- Confidence Accuracy
- Upset Error
- Home/Away Error
- Favorite Error

Evaluation results must not silently alter BPI v1.0.

Any validated improvement requiring a fundamental formula modification must result in a new engine version.

---

11. BPI v2.0 — Match Engine

BPI v2.0 is the planned Match Engine.

Its primary purpose is:

«Evaluate relative team strength for a specific football match.»

BPI v2.0 uses BPI v1.0 as its foundational baseline.

Planned components include:

- Recent Form
- Home/Away Form
- Opponent Strength Adjustment
- Starting XI Strength
- Injury Impact
- Suspension Impact
- Bench Strength
- Momentum
- Goal Timing Profile / Matchup

Potential outputs:

- Match Strength
- Match Gap
- Win Probability
- Draw Probability
- Loss Probability
- Confidence
- Scenario Analysis

The complete BPI v2.0 specification is maintained separately in:

"CORE/BPI_v2.0.md"

---

12. Data Governance

All official BPI calculations must use validated data.

Data must be:

- Accurate
- Complete
- Consistent
- Timestamped
- Traceable
- Versioned

All teams in a ranking calculation must use the same approved data snapshot.

Mixed snapshots must not be used for official rankings.

---

13. Reproducibility

BPI is designed to be deterministic.

The following condition must hold:

Same validated input
+
Same BPI engine version
+
Same calculation rules
=
Same output

If two valid implementations produce different results from identical inputs, the implementation must be investigated.

---

14. Golden Test Principle

The BPI system must maintain official test cases.

A Golden Test Case contains:

- Fixed input data
- Exact calculation procedure
- Expected intermediate values
- Expected BPI Score
- Expected ranking
- Expected Power Gap
- Expected BPI Change where applicable

Future implementations must reproduce the expected results.

The first official reference will be:

Golden Test Case #001

---

15. Version Control Rules

Project Version

Example:

v151.1
v151.2
v151.3

These represent project builds.

Engine Version

Example:

BPI v1.0
BPI v2.0

These represent analytical engine versions.

Fundamental Formula Change

A fundamental change to an engine requires a new engine version.

Example:

BPI v1.0
    ↓
fundamental formula change
    ↓
BPI v1.1 or later

The exact versioning decision must be documented before implementation.

---

16. Change Governance

Changes to the BPI system must be:

1. Documented.
2. Identified by version.
3. Tested.
4. Compared against the previous version.
5. Recorded in "DOCUMENTATION/CHANGELOG.md".

No fundamental change should be introduced silently.

---

17. Proprietary Status

The BeFree Power Index system is proprietary.

This includes:

- Methodology
- Formula
- Specifications
- Architecture
- Calculation logic
- Testing methodology
- Evaluation methodology
- Source code
- Historical records
- Documentation
- Future implementations

The repository may be publicly visible during development.

Public visibility does not grant open-source rights or permission to reproduce, modify, distribute, or commercialize the system.

No open-source license is granted.

---

18. Source of Truth

This repository is the official source of truth for:

BeFree Power Index v151.1

The approved specifications contained within this repository take precedence over informal descriptions, experimental implementations, or external copies.

---

19. Development Principle

The development of BPI follows a conservative principle:

«Protect the validated foundation before adding complexity.»

BPI v1.0 remains the stable Power Ranking foundation.

New functionality must be added through clearly defined layers or new engine versions rather than by silently modifying the foundation.

---

20. Current Status

Project                  : BeFree Power Index v151.1
BPI v1.0                 : Formula Locked
BPI v2.0                 : Architecture Defined
Data Layer               : Development
Calculation Engine       : Not Implemented
Golden Test Case #001    : Pending
Evaluation Engine        : Pending
Historical Database      : Pending

---

End of Master Specification
