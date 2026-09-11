# Changelog - BeFree Power Index (BPI)

All notable changes to the BeFree Power Index project will be documented in this file.

---

## [v151.1] - 2026-09-11 (Milestone: BPI v1.0 Engine Verified & Locked)

### Added
- **Engine Implementation:** Introduced `ENGINE/BPI_v1_0_ENGINE.py` implementing the deterministic BPI v1.0 calculation pipeline.
- **Engine Specification:** Formalized and locked `ENGINE/BPI_ENGINE_SPEC.md` establishing strict data contracts, validation rules, and rounding logic.
- **Regression Test Suite:** Added a comprehensive 20-point regression test suite (TC-01 through TC-20) covering positive integration tests and strict negative validation cases with automated CI exit codes.
- **Golden Test Reference:** Formalized `TESTING/BPI_GOLDEN_001.md` as the official mathematical reference point.

### Verified & Locked
- **BPI v1.0 Calculation Engine:** Officially declared **VERIFIED & LOCKED** after achieving 20/20 PASS results (exit code 0) on runtime regression execution.
- **Golden Test Case #001:** Validated calculation consistency against the synthetic reference dataset without deviation.

### Core Guarantees Maintained
- **Formula Integrity:** BPI v1.0 formula components and component weights remain strictly locked (PPG 30%, GD/Match 20%, Win Rate 20%, Recent Form 15%, GF/Match 10%, Defensive Score 5%).
- **Determinism:** Enforced strict floating-point handling, sequential ranking, alphabetical tie-breaking, and exact 4-decimal-place rounding.
- **Defensive Validation:** Enforced hard-fail constraints on schema mismatches, non-integer inputs (including rejecting float integers like `10.0`), null/NaN/Infinity values, and mathematical inconsistencies (such as `W+D+L != P`).
