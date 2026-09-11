#!/usr/bin/env python3
"""
BPI Evaluation Test Runner (TESTING/BPI_EVAL_TESTS.py)
Version: v1.0 (Strict Contract-Verified Final Reference Harness)
Parent Specification: BPI Evaluation Test Specification v1.0 (Locked)
Parent Baseline: BPI v1.0 (Immutable)

Description:
Deterministic test suite and reference test harness for the BPI Evaluation Layer.
Enforces 1:1 contract coverage with SPEC-EVAL-TEST-v1.0, featuring robust 
path-normalized ISO-01 (Resource Protection Policy Guard), rigorous ISO-02 
(True Boundary Deep State Isolation & Pristine Sentinel Feedback Channel),
and verified mathematical expectations (60.00% Win Rate, 80.00% Non-Loss Rate).
Exits with code 0 ONLY if all mandatory tests pass successfully.
"""

import sys
import os
import copy
import unittest
from decimal import Decimal, ROUND_HALF_UP

# =====================================================================
# ARCHITECTURAL BOUNDARY & GUARD IMPLEMENTATIONS
# =====================================================================

class ProtectedResourceGuard:
    """
    Enforces ISO-01 Resource Protection Policy Guard Contract.
    Uses strict path normalization and root-boundary matching to prevent 
    false positives (e.g., blocking 'MY_CORE/' while correctly blocking 'CORE/').
    """
    def __init__(self, protected_base_paths=("CORE", "ENGINE")):
        self.protected_paths = [os.path.normpath(p) for p in protected_base_paths]

    def enforce_write_policy(self, target_path, data):
        norm_target = os.path.normpath(target_path)
        for base in self.protected_paths:
            if norm_target == base or norm_target.startswith(base + os.sep):
                raise PermissionError(
                    f"Security Policy Violation: Evaluation layer attempted unauthorized write to protected resource '{target_path}'."
                )
        return True


class BPIEvaluationEngine:
    """
    Evaluation Engine implementing strict read-only audit rules, data contract validation,
    and anti-leakage guards compliant with BPI Evaluation Specification v1.0.
    Accepts an optional baseline_state to enforce true state-boundary inspection.
    """
    def __init__(self, dataset, baseline_state=None):
        self.dataset = dataset
        self.baseline_state = baseline_state  # Read-only boundary reference to BPI v1.0 baseline

    def validate_record(self, record, seen_match_ids=None):
        # 1. Mandatory Data Contract Fields Check (EC-03)
        mandatory_fields = [
            "match_id", "team_home", "team_away", 
            "bpi_home_pre", "bpi_away_pre", "power_gap", 
            "actual_goals_home", "actual_goals_away", "actual_result"
        ]
        for field in mandatory_fields:
            if field not in record or record[field] is None:
                raise ValueError(f"Missing mandatory field contract violation: {field}")
        
        # 2. Duplicate Match ID Check (EC-04)
        if seen_match_ids is not None:
            if record["match_id"] in seen_match_ids:
                raise ValueError(f"Duplicate match_id detected violating append-only integrity: {record['match_id']}")
            seen_match_ids.add(record["match_id"])

        # 3. Data Leakage Check (DL-02 - Controlled Test Metadata Flag)
        if record.get("snapshot_type") == "post_match":
            raise SecurityError("Data Leakage Detected: Post-match BPI snapshot is strictly prohibited.")
        
        # 4. Value Range Validations
        if record["bpi_home_pre"] < 0 or record["bpi_away_pre"] < 0:
            raise ValueError("BPI pre-match values cannot be negative.")
            
        return True

    def evaluate(self):
        if self.baseline_state is not None:
            _ = self.baseline_state.get("bpi_version")

        total_fixtures = len(self.dataset)
        
        # EC-02: Single Fixture Dataset support check
        if total_fixtures == 0:
            raise ValueError("Dataset cannot be empty.")

        eligible_higher_rank = 0
        higher_rank_wins = 0
        higher_rank_non_losses = 0
        equal_bpi_count = 0
        
        seen_match_ids = set()
        
        gap_buckets = {
            "0-<10": {"count": 0, "wins": 0},
            "10-<20": {"count": 0, "wins": 0},
            "20-<30": {"count": 0, "wins": 0},
            ">=30": {"count": 0, "wins": 0}
        }

        for record in self.dataset:
            self.validate_record(record, seen_match_ids)
            
            bpi_h = record["bpi_home_pre"]
            bpi_a = record["bpi_away_pre"]
            gap = record["power_gap"]
            res = record["actual_result"]
            
            if 0 <= gap < 10:
                bucket = "0-<10"
            elif 10 <= gap < 20:
                bucket = "10-<20"
            elif 20 <= gap < 30:
                bucket = "20-<30"
            else:
                bucket = ">=30"
                
            gap_buckets[bucket]["count"] += 1

            # Handle Equal BPI (Gap == 0) -> EC-01
            if bpi_h == bpi_a:
                equal_bpi_count += 1
                continue

            # Determine higher-ranked team & match outcome
            if bpi_h > bpi_a:
                eligible_higher_rank += 1
                if res == "H":
                    higher_rank_wins += 1
                    higher_rank_non_losses += 1
                    gap_buckets[bucket]["wins"] += 1
                elif res == "D":
                    higher_rank_non_losses += 1
            else:
                eligible_higher_rank += 1
                if res == "A":
                    higher_rank_wins += 1
                    higher_rank_non_losses += 1
                    gap_buckets[bucket]["wins"] += 1
                elif res == "D":
                    higher_rank_non_losses += 1

        win_rate = (Decimal(higher_rank_wins) / Decimal(eligible_higher_rank) * Decimal(100)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP) if eligible_higher_rank > 0 else Decimal('0.00')
        non_loss_rate = (Decimal(higher_rank_non_losses) / Decimal(eligible_higher_rank) * Decimal(100)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP) if eligible_higher_rank > 0 else Decimal('0.00')

        return {
            "total_fixtures": total_fixtures,
            "equal_bpi_fixtures": equal_bpi_count,
            "eligible_higher_rank_fixtures": eligible_higher_rank,
            "higher_rank_wins": higher_rank_wins,
            "higher_rank_non_losses": higher_rank_non_losses,
            "higher_rank_win_rate": float(win_rate),
            "higher_rank_non_loss_rate": float(non_loss_rate),
            "gap_buckets": gap_buckets,
            "upset_rate": "PENDING",
            "ranking_stability": "PENDING"
        }


class SecurityError(Exception):
    """Raised when security boundaries or isolation rules are breached."""
    pass


# =====================================================================
# UNIT TEST SUITE (Strict Contract Coverage)
# =====================================================================

class TestBPIEvaluationLayer(unittest.TestCase):
    
    def setUp(self):
        # Controlled Synthetic Historical Dataset mandated by BPI Test Spec v1.0
        self.synthetic_dataset = [
            {
                "match_id": "FX-003", "team_home": "Tim E", "team_away": "Tim F",
                "bpi_home_pre": 70.00, "bpi_away_pre": 65.00, "power_gap": 5.00,
                "actual_goals_home": 0, "actual_goals_away": 2, "actual_result": "A"
            },
            {
                "match_id": "FX-004", "team_home": "Tim G", "team_away": "Tim H",
                "bpi_home_pre": 60.00, "bpi_away_pre": 60.00, "power_gap": 0.00,
                "actual_goals_home": 1, "actual_goals_away": 0, "actual_result": "H"
            },
            {
                "match_id": "FX-005", "team_home": "Tim I", "team_away": "Tim J",
                "bpi_home_pre": 55.00, "bpi_away_pre": 70.00, "power_gap": 15.00,
                "actual_goals_home": 0, "actual_goals_away": 3, "actual_result": "A"
            },
            {
                "match_id": "FX-001", "team_home": "Tim A", "team_away": "Tim B",
                "bpi_home_pre": 80.00, "bpi_away_pre": 60.00, "power_gap": 20.00,
                "actual_goals_home": 2, "actual_goals_away": 0, "actual_result": "H"
            },
            {
                "match_id": "FX-002", "team_home": "Tim C", "team_away": "Tim D",
                "bpi_home_pre": 75.00, "bpi_away_pre": 50.00, "power_gap": 25.00,
                "actual_goals_home": 1, "actual_goals_away": 1, "actual_result": "D"
            },
            {
                "match_id": "FX-006", "team_home": "Tim K", "team_away": "Tim L",
                "bpi_home_pre": 85.00, "bpi_away_pre": 45.00, "power_gap": 40.00,
                "actual_goals_home": 4, "actual_goals_away": 1, "actual_result": "H"
            }
        ]

    def test_metric_higher_rank_win_rate(self):
        """Validates Higher-Rank Win Rate = 60.00% (3/5)."""
        engine = BPIEvaluationEngine(self.synthetic_dataset)
        results = engine.evaluate()
        self.assertEqual(results["eligible_higher_rank_fixtures"], 5)
        self.assertEqual(results["higher_rank_wins"], 3)
        self.assertEqual(results["higher_rank_win_rate"], 60.00)
        print(" -> [PASS] Metric Test: Higher-Rank Win Rate = 60.00% (3/5)")

    def test_metric_higher_rank_non_loss_rate(self):
        """Validates Higher-Rank Non-Loss Rate = 80.00% (4/5)."""
        engine = BPIEvaluationEngine(self.synthetic_dataset)
        results = engine.evaluate()
        self.assertEqual(results["higher_rank_non_losses"], 4)
        self.assertEqual(results["higher_rank_non_loss_rate"], 80.00)
        print(" -> [PASS] Metric Test: Higher-Rank Non-Loss Rate = 80.00% (4/5)")

    def test_edge_case_ec01_equal_bpi(self):
        """EC-01: Validates equal BPI (Gap = 0) handling and exclusion from higher-rank metrics."""
        engine = BPIEvaluationEngine(self.synthetic_dataset)
        results = engine.evaluate()
        self.assertEqual(results["equal_bpi_fixtures"], 1)
        print(" -> [PASS] Edge Case EC-01: Equal BPI correctly handled.")

    def test_edge_case_ec02_single_fixture(self):
        """EC-02: Validates metric calculation behavior on a single fixture dataset (N=1)."""
        single_dataset = [self.synthetic_dataset[3]]
        engine = BPIEvaluationEngine(single_dataset)
        results = engine.evaluate()
        self.assertEqual(results["total_fixtures"], 1)
        self.assertEqual(results["higher_rank_win_rate"], 100.00)
        print(" -> [PASS] Edge Case EC-02: Single fixture dataset processed successfully.")

    def test_edge_case_ec03_missing_pre_match_bpi(self):
        """EC-03: Validates rejection of records with missing/null pre-match BPI fields."""
        invalid_dataset = self.synthetic_dataset.copy()
        invalid_dataset[0] = invalid_dataset[0].copy()
        invalid_dataset[0]["bpi_home_pre"] = None
        
        engine = BPIEvaluationEngine(invalid_dataset)
        with self.assertRaises(ValueError):
            engine.evaluate()
        print(" -> [PASS] Edge Case EC-03: Missing pre-match BPI successfully rejected.")

    def test_edge_case_ec04_duplicate_match_id(self):
        """EC-04: Validates detection and rejection of duplicate match IDs."""
        invalid_dataset = self.synthetic_dataset.copy()
        invalid_dataset[1] = invalid_dataset[0].copy()
        
        engine = BPIEvaluationEngine(invalid_dataset)
        with self.assertRaises(ValueError):
            engine.evaluate()
        print(" -> [PASS] Edge Case EC-04: Duplicate match_id successfully rejected.")

    def test_data_leakage_rejection(self):
        """DL-02: Validates strict rejection of post-match BPI snapshots."""
        leaky_dataset = self.synthetic_dataset.copy()
        leaky_dataset[0] = leaky_dataset[0].copy()
        leaky_dataset[0]["snapshot_type"] = "post_match"
        
        engine = BPIEvaluationEngine(leaky_dataset)
        with self.assertRaises(SecurityError):
            engine.evaluate()
        print(" -> [PASS] Data Leakage Test: Post-match snapshot rejected.")

    def test_iso01_resource_protection_policy_guard(self):
        """
        ISO-01: Rigorously tests the Resource Protection Policy Guard.
        Verifies normalized path boundary enforcement blocking CORE/ and ENGINE/ 
        while safely allowing unprotected paths (and preventing false positives on similar substrings).
        """
        guard = ProtectedResourceGuard(protected_base_paths=("CORE", "ENGINE"))
        
        with self.assertRaises(PermissionError):
            guard.enforce_write_policy("CORE/BPI_MASTER_SPEC.md", "payload")
            
        with self.assertRaises(PermissionError):
            guard.enforce_write_policy("ENGINE/BPI_v1_0_ENGINE.py", "payload")
            
        success = guard.enforce_write_policy("MY_CORE/file.txt", "payload")
        self.assertTrue(success)
        
        success = guard.enforce_write_policy("EVALUATION/REPORT.txt", "payload")
        self.assertTrue(success)
        
        print(" -> [PASS] Isolation Test ISO-01: Normalized resource protection policy guard verified.")

    def test_iso02_zerofeedback_deep_state_isolation(self):
        """
        ISO-02: Proves Zero Feedback Loop via True Boundary Deep State Isolation.
        Passes a deep-copied evaluation input snapshot (bound to BPI v1.0 baseline state 
        featuring a complex PRISTINE sentinel) into the Evaluation Engine boundary. 
        Asserts strict pre-state == post-state identity and verifies zero baseline mutation or leakage.
        """
        bpi_baseline_runtime_input = {
            "bpi_version": "v1.0",
            "active_snapshots_count": len(self.synthetic_dataset),
            "evaluation_feedback": {
                "status": "SENTINEL_PRISTINE",
                "value": None
            }
        }
        
        state_snapshot_before = copy.deepcopy(bpi_baseline_runtime_input)
        evaluation_input_snapshot = copy.deepcopy(bpi_baseline_runtime_input)
        
        engine = BPIEvaluationEngine(self.synthetic_dataset, baseline_state=evaluation_input_snapshot)
        eval_output = engine.evaluate()
        
        state_snapshot_after = copy.deepcopy(bpi_baseline_runtime_input)
        
        self.assertEqual(state_snapshot_before, state_snapshot_after)
        self.assertEqual(evaluation_input_snapshot, state_snapshot_before)
        self.assertEqual(
            bpi_baseline_runtime_input["evaluation_feedback"],
            {"status": "SENTINEL_PRISTINE", "value": None}
        )
        self.assertEqual(
            evaluation_input_snapshot["evaluation_feedback"],
            {"status": "SENTINEL_PRISTINE", "value": None}
        )
        self.assertNotIn("higher_rank_win_rate", bpi_baseline_runtime_input)
        self.assertNotIn("higher_rank_win_rate", evaluation_input_snapshot)
        
        print(" -> [PASS] Isolation Test ISO-02: True boundary deep state isolation & sentinel feedback channel verified.")

    def test_reproducibility_multi_run(self):
        """REP-01: Validates absolute determinism across 3 consecutive execution runs."""
        runs = []
        for _ in range(3):
            engine = BPIEvaluationEngine(self.synthetic_dataset)
            runs.append(engine.evaluate())
            
        self.assertEqual(runs[0], runs[1])
        self.assertEqual(runs[1], runs[2])
        print(" -> [PASS] Reproducibility Test REP-01: Run #1 == Run #2 == Run #3 verified.")

    def test_pending_metrics_status(self):
        """Validates that Upset Rate and Ranking Stability are explicitly marked as PENDING."""
        engine = BPIEvaluationEngine(self.synthetic_dataset)
        results = engine.evaluate()
        self.assertEqual(results["upset_rate"], "PENDING")
        self.assertEqual(results["ranking_stability"], "PENDING")
        print(" -> [PASS] Pending Status Test: Upset Rate and Ranking Stability marked PENDING.")


if __name__ == "__main__":
    print("==================================================")
    print(" BPI Evaluation Test Suite Runner v1.0 (Final)    ")
    print(" Parent Spec: SPEC-EVAL-TEST-v1.0 (Locked)         ")
    print(" Reference Harness Mode                           ")
    print("==================================================")
    
    suite = unittest.TestLoader().loadTestsFromTestCase(TestBPIEvaluationLayer)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print("==================================================")
    if result.wasSuccessful():
        print(" STATUS: ALL SPECIFICATION CONTRACTS VERIFIED   ")
        print(" EXIT CODE: 0                                     ")
        print("==================================================")
        sys.exit(0)
    else:
        print(" STATUS: TEST SUITE FAILED                        ")
        print(" EXIT CODE: 1                                     ")
        print("==================================================")
        sys.exit(1)
