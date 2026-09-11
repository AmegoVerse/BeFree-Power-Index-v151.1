BeFree Power Index v151.1

BPI v2.0 — Match Engine

Engine Status: Architecture Defined
Engine Type: Match Engine
Project: BeFree Power Index v151.1
Baseline Engine: BPI v1.0
Owner: AmegoVerse

---

1. Purpose

BPI v2.0 is the Match Engine of the BeFree Power Index system.

Its primary purpose is:

«Evaluate the relative strength and expected performance of two teams in a specific football match.»

BPI v2.0 extends the foundational strength measurement provided by BPI v1.0 with match-specific information.

BPI v2.0 is therefore different from the BPI v1.0 Power Ranking Engine.

---

2. Relationship with BPI v1.0

BPI v1.0 measures:

«Overall team power.»

BPI v2.0 evaluates:

«Match-specific team strength.»

The architecture is:

BPI v1.0
Power Ranking
     │
     │ baseline
     ↓
BPI v2.0
Match Engine

BPI v2.0 must not silently modify the historical BPI v1.0 score.

The BPI v1.0 score remains an independent baseline measurement.

---

3. Match Engine Concept

A football match is influenced by factors that may not be fully represented by a season-level power ranking.

BPI v2.0 therefore considers additional contextual factors.

The planned model is:

BPI v1.0 Baseline
        ↓
Recent Form
        ↓
Home/Away Context
        ↓
Opponent Strength
        ↓
Starting XI
        ↓
Injuries
        ↓
Suspensions
        ↓
Bench Strength
        ↓
Momentum
        ↓
Goal Timing Profile
        ↓
Match-Specific Strength
        ↓
Probability Output

---

4. Match Factors

4.1 Recent Form

Recent Form measures the team's latest competitive performance.

It provides a short-term performance signal that complements the longer-term BPI v1.0 baseline.

Recent Form must be based on validated historical matches.

It must not be manually manipulated to produce a desired prediction.

---

5. Home/Away Form

Home and away performance may differ significantly.

BPI v2.0 therefore considers:

- Home team performance at home.
- Away team performance away from home.

The model must distinguish between:

Home Performance
vs.
Away Performance

Home/Away information is contextual and does not modify the historical BPI v1.0 score.

---

6. Opponent Strength Adjustment

Recent results against weak and strong opponents should not necessarily carry the same analytical meaning.

BPI v2.0 therefore includes an Opponent Strength Adjustment.

Concept:

Performance
      +
Opponent Strength
      ↓
Adjusted Performance

The adjustment should use BPI-based strength information where appropriate.

The final mathematical weighting must be determined through historical testing.

---

7. Starting XI Strength

The expected Starting XI can materially affect match strength.

BPI v2.0 may evaluate:

- Expected starters
- Individual player strength
- Positional importance
- Availability
- Recent player performance

Starting XI strength must be calculated using a defined and reproducible methodology.

---

8. Injury Impact

Unavailable players may reduce team strength.

BPI v2.0 therefore includes Injury Impact.

Potential considerations:

- Player importance
- Position
- Expected starting status
- Replacement quality
- Number of unavailable players

The impact must not be determined solely by player reputation.

A reproducible scoring method must be established before production implementation.

---

9. Suspension Impact

Suspended players may reduce available team strength.

The model should evaluate:

- Suspended player importance
- Position
- Expected starting status
- Replacement quality

Suspension impact is separate from injury impact.

---

10. Bench Strength

Substitution quality can affect match outcomes, particularly during the second half.

BPI v2.0 therefore includes Bench Strength.

Potential inputs:

- Available substitutes
- Player strength
- Positional coverage
- Attacking options
- Defensive options

Bench Strength should be calculated independently from Starting XI Strength.

---

11. Momentum

Momentum represents short-term performance direction.

Potential indicators may include:

- Recent results
- Recent goal difference
- Recent scoring trend
- Recent defensive trend
- Consecutive positive or negative results

Momentum must not duplicate Recent Form without a measurable analytical purpose.

Historical testing must determine whether Momentum provides independent predictive value.

---

12. Goal Timing Profile

BPI v2.0 includes Goal Timing Profile / Matchup.

This evaluates when teams tend to score and concede.

Potential intervals:

0–15
16–30
31–45+
46–60
61–75
76–90+

Potential analysis:

- Scoring timing
- Conceding timing
- First-half strength
- Second-half strength
- Late-game strength

Goal Timing Profile may become particularly important when comparing two teams with different scoring patterns.

---

13. Match Strength

BPI v2.0 produces a match-specific strength assessment.

Conceptually:

Team A
BPI Baseline
   +
Match Factors
   ↓
Match Strength A

Team B
BPI Baseline
   +
Match Factors
   ↓
Match Strength B

The difference between the two values produces a Match Gap.

---

14. Match Gap

For teams A and B:

[
MatchGap = MatchStrength_A - MatchStrength_B
]

Interpretation:

Positive → advantage Team A
Negative → advantage Team B
Zero     → equal match strength

Absolute Match Gap:

[
|MatchGap|=
|MatchStrength_A-MatchStrength_B|
]

Match Gap is an analytical output.

---

15. Probability Output

BPI v2.0 is intended to produce:

- Win Probability
- Draw Probability
- Loss Probability

For a two-team match:

[
P(HomeWin)+P(Draw)+P(AwayWin)=100%
]

Probabilities must be generated using a defined and validated probability model.

The probability model must not be arbitrarily assigned.

---

16. Confidence

BPI v2.0 may provide a confidence measurement.

Confidence should represent the reliability of the prediction rather than simply the probability of the favored outcome.

Potential confidence factors include:

- Match Gap
- Data completeness
- Model agreement
- Historical calibration
- Uncertainty
- Injury/lineup uncertainty

Confidence must be calibrated against historical results before being considered an official production metric.

---

17. Scenario Analysis

BPI v2.0 may support scenario analysis.

Examples:

Scenario A
Expected Starting XI

Scenario B
Key Player Unavailable

Scenario C
Multiple Injuries

Scenario D
Different Starting XI

Scenario analysis must not alter the official historical BPI v1.0 score.

---

18. Evaluation

BPI v2.0 must be evaluated against historical match outcomes.

Primary evaluation metrics may include:

- Accuracy
- Precision
- Recall
- F1 Score
- Error Rate
- Prediction Error
- Calibration
- Confidence Accuracy

Advanced metrics may include:

- Log Loss
- Brier Score
- Power Gap Error
- Match Gap Error
- Upset Error
- Home/Away Error
- Favorite Error

---

19. Complexity Control

BPI v2.0 must follow a controlled-complexity principle.

A factor should only remain in the production model if historical testing demonstrates measurable value.

The factor should demonstrate one or more of:

- Improved accuracy
- Reduced error
- Improved calibration
- Improved probability reliability
- Improved prediction stability

A factor that does not provide measurable improvement may be removed or revised.

---

20. Separation from BPI v1.0

BPI v2.0 must not overwrite BPI v1.0.

The system must preserve:

BPI v1.0
     │
     ├── Historical Power Score
     │
     └── Stable Ranking Baseline

BPI v2.0
     │
     ├── Match Context
     ├── Match Strength
     ├── Probability
     └── Confidence

This separation allows the performance of the Match Engine to be evaluated independently.

---

21. Future Mathematical Specification

At this stage, BPI v2.0 defines the architecture and required components.

The final mathematical weights must not be invented before sufficient historical testing is available.

The development sequence is:

Architecture
     ↓
Data Collection
     ↓
Feature Definition
     ↓
Historical Testing
     ↓
Weight Optimization
     ↓
Validation
     ↓
Production Formula

Therefore, this document does not yet lock final BPI v2.0 weights.

---

22. Deterministic Requirement

Once the BPI v2.0 production formula is finalized, the Match Engine must become deterministic.

The same:

- Input data
- Engine version
- Formula
- Configuration

must produce the same result.

---

23. Golden Test Requirement

BPI v2.0 will require dedicated Match Engine Golden Test Cases.

These tests must include:

- Match input
- Team baseline BPI
- Match factors
- Intermediate calculations
- Match Strength
- Match Gap
- Probability
- Confidence
- Expected output

BPI v2.0 Golden Tests must remain separate from BPI v1.0 Golden Tests.

---

24. Development Status

BPI v2.0 Architecture       : Defined
BPI v1.0 Baseline            : Locked
Match Factors                : Defined
Final Mathematical Formula   : Pending Testing
Probability Model            : Pending Testing
Confidence Model             : Pending Testing
Golden Test                  : Pending
Production Engine            : Not Implemented

---

25. Official Status

BPI v2.0 — Match Engine

Current status:

«ARCHITECTURE DEFINED — FORMULA NOT YET LOCKED»

BPI v2.0 must be developed without compromising the locked BPI v1.0 foundation.

---

End of BPI v2.0 Specification
