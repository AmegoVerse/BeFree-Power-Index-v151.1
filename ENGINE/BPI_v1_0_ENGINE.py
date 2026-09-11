"""
BeFree Power Index v151.1 - BPI v1.0 Calculation Engine
Engine Version: BPI_v1.0_ENGINE
Target: Standalone deterministic BPI v1.0 calculation with 100% strict compliance, 
including strict-integer and exact-field validation.
"""

import pandas as pd
import numpy as np
import sys

ENGINE_VERSION = "BPI_v1.0_ENGINE"

class BPIEngineError(Exception):
    """Custom exception raised for dataset or calculation validation failures."""
    pass

def validate_dataset(df: pd.DataFrame) -> None:
    if df is None or df.empty:
        raise BPIEngineError("Validation Error: Dataset is empty.")

    mandatory_fields = [
        "team_name", "matches_played", "wins", "draws", "losses", 
        "goals_for", "goals_against", "points", "recent_form_score"
    ]
    
    current_columns = list(df.columns)
    if set(current_columns) != set(mandatory_fields):
        extra = set(current_columns) - set(mandatory_fields)
        missing = set(mandatory_fields) - set(current_columns)
        raise BPIEngineError(f"Validation Error: Dataset columns do not match exact contract. Missing: {missing}, Extra: {extra}")

    if df.isnull().any().any():
        raise BPIEngineError("Validation Error: Dataset contains NaN or Null values.")

    for val in df["team_name"]:
        if not isinstance(val, str) or isinstance(val, bool):
            raise BPIEngineError("Validation Error: 'team_name' must contain strictly string values.")
    
    if (df["team_name"].str.strip() == "").any():
        raise BPIEngineError("Validation Error: 'team_name' cannot be empty or whitespace-only.")

    if df["team_name"].duplicated().any():
        raise BPIEngineError("Validation Error: Duplicate team names detected in dataset.")

    integer_fields = ["matches_played", "wins", "draws", "losses", "goals_for", "goals_against", "points"]
    
    for col in integer_fields:
        col_series = df[col]
        if np.issubdtype(col_series.dtype, np.floating):
            raise BPIEngineError(f"Validation Error: Field '{col}' contains floating-point values. Strict integers required.")
        
        if not np.issubdtype(col_series.dtype, np.integer):
            for item in col_series:
                if not isinstance(item, (int, np.integer)) or isinstance(item, bool):
                    raise BPIEngineError(f"Validation Error: Field '{col}' must contain strict integer values.")

        if (col_series < 0).any():
            raise BPIEngineError(f"Validation Error: Field '{col}' contains negative values.")
        if np.isinf(col_series).any():
            raise BPIEngineError(f"Validation Error: Field '{col}' contains Infinity values.")

    form_col = "recent_form_score"
    form_series = df[form_col]
    if not np.issubdtype(form_series.dtype, np.number):
        raise BPIEngineError(f"Validation Error: Field '{form_col}' must be numeric.")
    if (form_series < 0).any():
        raise BPIEngineError(f"Validation Error: Field '{form_col}' contains negative values.")
    if np.isinf(form_series).any():
        raise BPIEngineError(f"Validation Error: Field '{form_col}' contains Infinity values.")

    if (df["matches_played"] == 0).any():
        raise BPIEngineError("Validation Error: 'matches_played' cannot be zero.")

    match_sum = df["wins"] + df["draws"] + df["losses"]
    if not (match_sum == df["matches_played"]).all():
        raise BPIEngineError("Calculation Validation Error: (wins + draws + losses) != matches_played for one or more teams.")

    calculated_points = (df["wins"] * 3) + (df["draws"] * 1)
    if not (calculated_points == df["points"]).all():
        raise BPIEngineError("Calculation Validation Error: ((wins * 3) + (draws * 1)) != points for one or more teams.")


def calculate_bpi(input_data) -> pd.DataFrame:
    df = pd.DataFrame(input_data).copy()
    validate_dataset(df)

    df["ppg"] = df["points"] / df["matches_played"]
    df["gd"] = df["goals_for"] - df["goals_against"]
    df["gd_match"] = df["gd"] / df["matches_played"]
    df["win_rate"] = (df["wins"] / df["matches_played"]) * 100.0
    df["gf_match"] = df["goals_for"] / df["matches_played"]
    df["ga_match"] = df["goals_against"] / df["matches_played"]

    def normalize_metric(series, higher_is_better=True, is_defensive=False):
        x_min, x_max = series.min(), series.max()
        if x_max == x_min:
            return pd.Series(50.0, index=series.index)
        if is_defensive:
            return ((x_max - series) / (x_max - x_min)) * 100.0
        elif higher_is_better:
            return ((series - x_min) / (x_max - x_min)) * 100.0
        else:
            return ((x_max - series) / (x_max - x_min)) * 100.0

    df["s_ppg"] = normalize_metric(df["ppg"])
    df["s_gd"] = normalize_metric(df["gd_match"])
    df["s_wr"] = normalize_metric(df["win_rate"])
    df["s_rf"] = normalize_metric(df["recent_form_score"])
    df["s_gf"] = normalize_metric(df["gf_match"])
    df["s_def"] = normalize_metric(df["ga_match"], is_defensive=True)

    df["unrounded_bpi"] = (
        (0.30 * df["s_ppg"]) +
        (0.20 * df["s_gd"]) +
        (0.20 * df["s_wr"]) +
        (0.15 * df["s_rf"]) +
        (0.10 * df["s_gf"]) +
        (0.05 * df["s_def"])
    )

    df = df.sort_values(by=["unrounded_bpi", "team_name"], ascending=[False, True]).reset_index(drop=True)
    df["bpi_rank"] = df.index + 1
    N = len(df)

    power_gaps = []
    for r in range(N):
        if r < N - 1:
            gap = df.loc[r, "unrounded_bpi"] - df.loc[r + 1, "unrounded_bpi"]
        else:
            gap = 0.0000
        power_gaps.append(gap)
    df["unrounded_power_gap"] = power_gaps

    df["bpi_score"] = df["unrounded_bpi"].round(4)
    df["power_gap"] = df["unrounded_power_gap"].round(4)

    return df[["bpi_rank", "team_name", "bpi_score", "power_gap"]].copy()


def test_bpi_golden_001() -> bool:
    golden_dataset = [
        {"team_name": "Alpha FC",   "matches_played": 10, "wins": 8, "draws": 1, "losses": 1, "goals_for": 24, "goals_against": 8,  "points": 25, "recent_form_score": 80},
        {"team_name": "Bravo FC",   "matches_played": 10, "wins": 6, "draws": 2, "losses": 2, "goals_for": 20, "goals_against": 10, "points": 20, "recent_form_score": 67},
        {"team_name": "Charlie FC", "matches_played": 10, "wins": 5, "draws": 2, "losses": 3, "goals_for": 17, "goals_against": 13, "points": 17, "recent_form_score": 53},
        {"team_name": "Delta FC",   "matches_played": 10, "wins": 3, "draws": 3, "losses": 4, "goals_for": 13, "goals_against": 17, "points": 12, "recent_form_score": 40},
        {"team_name": "Echo FC",    "matches_played": 10, "wins": 1, "draws": 2, "losses": 7, "goals_for": 8,  "goals_against": 24, "points": 5,  "recent_form_score": 27},
    ]

    expected_results = {
        "Alpha FC":   {"bpi_rank": 1, "bpi_score": 100.0000, "power_gap": 23.0411},
        "Bravo FC":   {"bpi_rank": 2, "bpi_score": 76.9589,  "power_gap": 18.7780},
        "Charlie FC": {"bpi_rank": 3, "bpi_score": 58.1809,  "power_gap": 26.2276},
        "Delta FC":   {"bpi_rank": 4, "bpi_score": 31.9533,  "power_gap": 31.9533},
        "Echo FC":    {"bpi_rank": 5, "bpi_score": 0.0000,   "power_gap": 0.0000},
    }

    try:
        result_df = calculate_bpi(golden_dataset)
        for _, row in result_df.iterrows():
            team = row["team_name"]
            assert team in expected_results
            exp = expected_results[team]
            assert row["bpi_rank"] == exp["bpi_rank"]
            assert row["bpi_score"] == exp["bpi_score"]
            assert row["power_gap"] == exp["power_gap"]
        return True
    except Exception:
        return False


def run_regression_suite() -> bool:
    success_count = 0
    total_tests = 20

    def run_test(test_id, test_name, test_func):
        nonlocal success_count
        try:
            test_func()
            print(f"[{test_id}] {test_name}: PASS")
            success_count += 1
        except Exception as e:
            print(f"[{test_id}] {test_name}: FAIL ({e})")

    base_valid_data = [
        {"team_name": "Alpha FC",   "matches_played": 10, "wins": 8, "draws": 1, "losses": 1, "goals_for": 24, "goals_against": 8,  "points": 25, "recent_form_score": 80},
        {"team_name": "Bravo FC",   "matches_played": 10, "wins": 6, "draws": 2, "losses": 2, "goals_for": 20, "goals_against": 10, "points": 20, "recent_form_score": 67},
        {"team_name": "Charlie FC", "matches_played": 10, "wins": 5, "draws": 2, "losses": 3, "goals_for": 17, "goals_against": 13, "points": 17, "recent_form_score": 53},
        {"team_name": "Delta FC",   "matches_played": 10, "wins": 3, "draws": 3, "losses": 4, "goals_for": 13, "goals_against": 17, "points": 12, "recent_form_score": 40},
        {"team_name": "Echo FC",    "matches_played": 10, "wins": 1, "draws": 2, "losses": 7, "goals_for": 8,  "goals_against": 24, "points": 5,  "recent_form_score": 27},
    ]

    def assert_raises_bpi_error(test_func):
        try:
            test_func()
            raise AssertionError("Expected BPIEngineError was not raised.")
        except BPIEngineError:
            pass

    run_test("TC-01", "Golden Test #001 Integration", lambda: assert_true(test_bpi_golden_001()))
    run_test("TC-02", "Empty Dataset Rejection", lambda: assert_raises_bpi_error(lambda: calculate_bpi([])))
    run_test("TC-03", "Missing Mandatory Field Rejection", lambda: assert_raises_bpi_error(lambda: calculate_bpi([{k: v for k, v in base_valid_data[0].items() if k != "points"}])))
    run_test("TC-04", "Extra Field Rejection", lambda: assert_raises_bpi_error(lambda: calculate_bpi([{**base_valid_data[0], "extra": 1}])))
    run_test("TC-05", "Duplicate Team Name Rejection", lambda: assert_raises_bpi_error(lambda: calculate_bpi([base_valid_data[0], base_valid_data[0]])))
    run_test("TC-06", "Empty/Whitespace Team Name Rejection", lambda: assert_raises_bpi_error(lambda: calculate_bpi([{**base_valid_data[0], "team_name": "   "}])))
    run_test("TC-07", "Non-String Team Name Rejection", lambda: assert_raises_bpi_error(lambda: calculate_bpi([{**base_valid_data[0], "team_name": 12345}])))
    run_test("TC-08", "NaN Value Rejection", lambda: assert_raises_bpi_error(lambda: calculate_bpi([{**base_valid_data[0], "points": float('nan')}])))
    run_test("TC-09", "Null Value Rejection", lambda: assert_raises_bpi_error(lambda: calculate_bpi([{**base_valid_data[0], "wins": None}])))
    run_test("TC-10", "Infinity Value Rejection", lambda: assert_raises_bpi_error(lambda: calculate_bpi([{**base_valid_data[0], "goals_for": float('inf')}])))
    run_test("TC-11", "Negative Integer Rejection", lambda: assert_raises_bpi_error(lambda: calculate_bpi([{**base_valid_data[0], "goals_against": -2}])))
    run_test("TC-12", "Floating-Point Integer (10.0) Rejection", lambda: assert_raises_bpi_error(lambda: calculate_bpi([{**base_valid_data[0], "matches_played": 10.0}])))
    run_test("TC-13", "Decimal Integer (10.5) Rejection", lambda: assert_raises_bpi_error(lambda: calculate_bpi([{**base_valid_data[0], "points": 10.5}])))
    run_test("TC-14", "W+D+L Mismatch Rejection", lambda: assert_raises_bpi_error(lambda: calculate_bpi([{**base_valid_data[0], "wins": 7}])))
    run_test("TC-15", "Points Mismatch Rejection", lambda: assert_raises_bpi_error(lambda: calculate_bpi([{**base_valid_data[0], "points": 20}])))
    run_test("TC-16", "Zero Matches Played Rejection", lambda: assert_raises_bpi_error(lambda: calculate_bpi([{**base_valid_data[0], "matches_played": 0}])))

    def test_zero_range():
        identical_data = [
            {"team_name": "Team A", "matches_played": 5, "wins": 2, "draws": 1, "losses": 2, "goals_for": 5, "goals_against": 5, "points": 7, "recent_form_score": 50},
            {"team_name": "Team B", "matches_played": 5, "wins": 2, "draws": 1, "losses": 2, "goals_for": 5, "goals_against": 5, "points": 7, "recent_form_score": 50},
        ]
        res = calculate_bpi(identical_data)
        assert len(res) == 2
        assert res.loc[0, "bpi_score"] == 50.0000
    run_test("TC-17", "Zero-Range Normalization Handling", test_zero_range)

    def test_tie_breaking():
        tie_data = [
            {"team_name": "Zebra FC", "matches_played": 10, "wins": 5, "draws": 2, "losses": 3, "goals_for": 15, "goals_against": 15, "points": 17, "recent_form_score": 50},
            {"team_name": "Alpha FC", "matches_played": 10, "wins": 5, "draws": 2, "losses": 3, "goals_for": 15, "goals_against": 15, "points": 17, "recent_form_score": 50},
        ]
        res = calculate_bpi(tie_data)
        assert res.loc[0, "team_name"] == "Alpha FC"
    run_test("TC-18", "Deterministic Tie-Breaking", test_tie_breaking)

    def test_reproducibility():
        res1 = calculate_bpi(base_valid_data)
        res2 = calculate_bpi(base_valid_data)
        pd.testing.assert_frame_equal(res1, res2)
    run_test("TC-19", "Repeated Identical Execution", test_reproducibility)

    def test_golden_regression():
        res = calculate_bpi(base_valid_data)
        assert res.loc[0, "power_gap"] == 23.0411
        assert res.loc[4, "power_gap"] == 0.0000
    run_test("TC-20", "Golden Regression Structural Check", test_golden_regression)

    if success_count == total_tests:
        print(f"REGRESSION TEST SUITE COMPLETED: {success_count}/{total_tests} PASSED.")
        print("[SUCCESS] BPI v1.0 REGRESSION SUITE PASSED.")
        return True
    else:
        print(f"REGRESSION TEST SUITE COMPLETED: {success_count}/{total_tests} PASSED.")
        print("[FAILURE] BPI v1.0 REGRESSION SUITE FAILED.")
        return False

def assert_true(condition):
    assert condition, "Condition evaluated to False."

if __name__ == "__main__":
    if not run_regression_suite():
        sys.exit(1)
