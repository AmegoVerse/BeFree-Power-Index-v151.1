BeFree Power Index v151.1

BPI v1.0 — Power Ranking Engine

Engine Status: Locked
Engine Type: Power Ranking Engine
Project: BeFree Power Index v151.1
Owner: AmegoVerse

---

1. Purpose

BPI v1.0 is the foundational Power Ranking Engine of the BeFree Power Index system.

Its primary purpose is:

«Measure the overall power of football teams based on validated league performance data.»

BPI v1.0 is designed to provide a stable and reproducible baseline for the BeFree Power Index system.

BPI v1.0 does not attempt to predict the outcome of an individual match.

Match-specific prediction belongs to the BPI v2.0 Match Engine.

---

2. Core Formula

For each team i:

[
BPI_i =
0.30S_{PPG,i}
+0.20S_{GD,i}
+0.20S_{WR,i}
+0.15S_{RF,i}
+0.10S_{GF,i}
+0.05S_{DEF,i}
]

Where:

- S_{PPG} = normalized Points Per Game score
- S_{GD} = normalized Goal Difference per Match score
- S_{WR} = normalized Win Rate score
- S_{RF} = normalized Recent Form score
- S_{GF} = normalized Goals For per Match score
- S_{DEF} = normalized Defensive score

Total weight:

[
0.30+0.20+0.20+0.15+0.10+0.05=1.00
]

Therefore:

Total Weight = 100%

---

3. Component Weights

Component| Symbol| Weight
Points Per Game| PPG| 30%
Goal Difference per Match| GD| 20%
Win Rate| WR| 20%
Recent Form| RF| 15%
Goals For per Match| GF| 10%
Defensive Score| DEF| 5%
Total| | 100%

---

4. Required Input Data

BPI v1.0 requires the following team-level data:

Input| Description
Team| Team name
Played (P)| Number of matches played
Wins (W)| Number of wins
Draws (D)| Number of draws
Losses (L)| Number of losses
Goals For (GF)| Goals scored
Goals Against (GA)| Goals conceded
Points (Pts)| League points
Recent Form| Approved recent-form value

All teams used in the same ranking calculation must come from the same approved data snapshot.

---

5. Data Validation

Before calculation:

Matches

[
W+D+L=P
]

must be true.

Points

For a standard three-point league system:

[
Pts=(3\times W)+D
]

must be consistent with the supplied points.

Goals

[
GF \geq 0
]

[
GA \geq 0
]

Matches

[
P>0
]

Division by zero is not permitted.

Invalid records must be rejected or corrected before official calculation.

---

6. Derived Metrics

BPI v1.0 derives the following metrics from the input data.

6.1 Points Per Game

[
PPG_i=\frac{Pts_i}{P_i}
]

PPG measures the average league points obtained per match.

---

6.2 Goal Difference per Match

First calculate total goal difference:

[
GD_i=GF_i-GA_i
]

Then:

[
GD/Match_i=\frac{GF_i-GA_i}{P_i}
]

---

6.3 Win Rate

[
WinRate_i=
\frac{W_i}{P_i}\times100
]

Win Rate represents the percentage of matches won.

---

6.4 Goals For per Match

[
GF/Match_i=
\frac{GF_i}{P_i}
]

This measures attacking output per match.

---

6.5 Goals Against per Match

[
GA/Match_i=
\frac{GA_i}{P_i}
]

This value is used to calculate the defensive component.

---

7. Normalization

BPI v1.0 converts each component into a common 0–100 scale.

Normalization is performed using the minimum and maximum values from the same approved league snapshot.

---

7.1 Higher-Is-Better Components

For PPG, GD/Match, Win Rate, Recent Form, and GF/Match:

[
S_x(i)=
\frac{x_i-x_{min}}
{x_{max}-x_{min}}
\times100
]

Where:

- x_i = team's value
- x_{min} = minimum value among teams
- x_{max} = maximum value among teams

Therefore:

Highest value = 100
Lowest value  = 0

---

8. Defensive Score

Goals Against per Match is a lower-is-better metric.

Therefore the normalization direction is reversed.

[
S_{DEF}(i)=
\frac{x_{max}-GA/Match_i}
{x_{max}-x_{min}}
\times100
]

Where:

- x_{max} = highest GA/Match among teams
- x_{min} = lowest GA/Match among teams

Therefore:

Best defensive record = 100
Worst defensive record = 0

---

9. Zero-Range Rule

If:

[
x_{max}=x_{min}
]

the standard normalization formula would produce division by zero.

In this situation, all teams have the same value for that component.

The component score must therefore be assigned:

[
S_x=50
]

for every team.

This prevents division-by-zero and represents a neutral score when no team has an advantage in that component.

---

10. Recent Form

Recent Form is an official BPI v1.0 component with a weight of 15%.

The Recent Form input must be converted into a numeric value before normalization.

The approved Recent Form methodology must remain consistent within a calculation snapshot.

The exact source and encoding of Recent Form must be defined in:

"DATA/BPI_DATA_SPEC.md"

Recent Form must not be manually altered to improve a team's BPI score.

---

11. Final BPI Score

After normalization, calculate:

[
BPI_i =
0.30S_{PPG,i}
+0.20S_{GD,i}
+0.20S_{WR,i}
+0.15S_{RF,i}
+0.10S_{GF,i}
+0.05S_{DEF,i}
]

The theoretical output range is:

[
0\leq BPI_i\leq100
]

A higher BPI Score represents greater measured team power within the evaluated league snapshot.

---

12. Power Ranking

Teams are ranked according to BPI Score in descending order.

Highest BPI Score
       ↓
      Rank 1
       ↓
      Rank 2
       ↓
      Rank 3
       ↓
      ...

If two teams have exactly the same BPI Score, the tie-handling rule must be defined by the testing/data specification before implementation.

The calculation engine must not invent a tie-break rule silently.

---

13. Power Gap

For two teams A and B:

[
PowerGap_{A,B}=BPI_A-BPI_B
]

Interpretation:

Positive → A has higher BPI
Negative → B has higher BPI
Zero     → Equal BPI

Absolute Power Gap:

[
|PowerGap|=
|BPI_A-BPI_B|
]

Power Gap is a derived analytical output and does not modify BPI Score.

---

14. BPI Change

BPI Change compares two validated BPI snapshots.

[
BPIChange_t=
BPI_t-BPI_{t-1}
]

Interpretation:

Positive → BPI increased
Negative → BPI decreased
Zero     → BPI unchanged

BPI Change must only compare compatible snapshots.

The underlying methodology and normalization rules must remain consistent when interpreting historical changes.

---

15. Calculation Sequence

The official calculation sequence is:

1. Load approved data snapshot
        ↓
2. Validate input data
        ↓
3. Calculate derived metrics
        ↓
4. Determine min/max values
        ↓
5. Normalize components
        ↓
6. Calculate weighted BPI Score
        ↓
7. Rank teams
        ↓
8. Calculate Power Gap
        ↓
9. Compare historical snapshot for BPI Change
        ↓
10. Store official result

---

16. Deterministic Requirement

BPI v1.0 must be deterministic.

Given:

- identical validated input,
- identical snapshot,
- identical normalization rules,
- identical BPI v1.0 specification,

the result must be identical.

Same Input
+
Same Formula
+
Same Version
=
Same BPI Result

---

17. Rounding Rules

Internal calculations should retain sufficient precision to avoid cumulative rounding errors.

Rounding should be applied only at the defined output stage.

The exact display precision must be defined before implementation of the production calculation engine.

The calculation engine must not round intermediate values unless explicitly specified.

---

18. Formula Lock

The following elements are locked for BPI v1.0:

- Component selection
- Component weights
- Core formula
- Derived metric definitions
- Normalization direction
- Defensive normalization
- Zero-range handling
- Deterministic calculation principle

Any fundamental modification requires a new BPI engine version.

No silent formula changes are permitted.

---

19. Golden Test Requirement

BPI v1.0 must have an official Golden Test Case.

The Golden Test Case must contain:

- Fixed input dataset
- Derived metrics
- Min/max values
- Normalized component scores
- Weighted component contributions
- Final BPI Score
- Ranking
- Power Gap
- Expected outputs

Future implementations must reproduce the official expected results.

The first official reference will be:

Golden Test Case #001

---

20. Relationship to BPI v2.0

BPI v1.0 is the foundational Power Ranking Engine.

BPI v2.0 may use BPI v1.0 outputs as baseline information.

BPI v2.0 must not modify the historical BPI v1.0 calculation.

BPI v1.0
   │
   │ baseline
   ↓
BPI v2.0 Match Engine

---

21. Official Status

BPI v1.0 — Power Ranking Engine

Status:

«LOCKED FOUNDATION»

This specification is the official technical definition of BPI v1.0 within BeFree Power Index v151.1.

---

End of BPI v1.0 Specification
