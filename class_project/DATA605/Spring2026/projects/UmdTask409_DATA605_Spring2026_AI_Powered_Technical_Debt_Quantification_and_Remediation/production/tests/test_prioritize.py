"""Tests for production.stages.prioritize."""

import sys
import unittest
from pathlib import Path

# Make production package importable.
sys.path.insert(0, "/data")

from production.stages.prioritize import (
    prioritize_issues,
    compute_pareto_front,
    SEVERITY_WEIGHT_BY_PRIORITY,
    EFFORT_MINUTES_BY_PRIORITY,
    RULESET_WEIGHT,
    DEFAULT_RULESET_WEIGHT,
)


def make_issue(rule, ruleset, priority, fault_prob, issue_id="x"):
    return {
        "issue_id": issue_id,
        "rule": rule,
        "ruleset": ruleset,
        "priority": priority,
        "fault_probability": fault_prob,
        "file_path": "/tmp/Foo.java",
        "file_relative": "Foo.java",
        "begin_line": 1,
    }


class TestPrioritizeIssuesEmpty(unittest.TestCase):
    def test_empty_list_returns_empty(self):
        result = prioritize_issues([])
        self.assertEqual(result, [])


class TestPrioritizeIssuesScoring(unittest.TestCase):
    def test_score_uses_severity_weight(self):
        # Two issues, identical except priority.
        issues = [
            make_issue("R1", "Best Practices", 1, 0.5, "high"),
            make_issue("R1", "Best Practices", 5, 0.5, "low"),
        ]
        prioritize_issues(issues)
        high = next(i for i in issues if i["issue_id"] == "high")
        low = next(i for i in issues if i["issue_id"] == "low")
        # priority 1 has 16x the severity weight of priority 5.
        self.assertGreater(high["impact"], low["impact"] * 10)

    def test_score_uses_ruleset_weight(self):
        issues = [
            make_issue("R1", "Performance", 3, 0.5, "perf"),
            make_issue("R1", "Best Practices", 3, 0.5, "best"),
        ]
        prioritize_issues(issues)
        perf = next(i for i in issues if i["issue_id"] == "perf")
        best = next(i for i in issues if i["issue_id"] == "best")
        self.assertGreater(perf["impact"], best["impact"])

    def test_score_uses_effort_in_denominator(self):
        # Two issues, identical impact but different priority -> different effort.
        # priority 5 -> 2 min; priority 3 -> 10 min. Lower effort -> higher score.
        # But priority 5 also has lower severity. Let me construct a case where
        # the effort effect is the dominant variable.
        issues = [
            make_issue("R", "Best Practices", 4, 1.0, "low_eff"),  # eff=5
            make_issue("R", "Best Practices", 1, 0.0625, "high_eff"),  # eff=20
        ]
        # impact_low = 1.0 * 0.125 = 0.125; score = 0.125/5 = 0.025
        # impact_high = 0.0625 * 1.0 = 0.0625; score = 0.0625/20 = 0.003125
        # low_eff should rank higher.
        prioritize_issues(issues)
        low = next(i for i in issues if i["issue_id"] == "low_eff")
        high = next(i for i in issues if i["issue_id"] == "high_eff")
        self.assertLess(low["priority_rank"], high["priority_rank"])

    def test_priority_rank_starts_at_1(self):
        issues = [
            make_issue("R1", "Best Practices", 3, 0.5, "a"),
            make_issue("R2", "Best Practices", 3, 0.3, "b"),
            make_issue("R3", "Best Practices", 3, 0.7, "c"),
        ]
        prioritize_issues(issues)
        self.assertEqual(issues[0]["priority_rank"], 1)
        self.assertEqual(issues[-1]["priority_rank"], 3)

    def test_returned_list_is_sorted_by_score_desc(self):
        issues = [
            make_issue("R1", "Best Practices", 3, 0.1, "low"),
            make_issue("R2", "Best Practices", 3, 0.9, "high"),
            make_issue("R3", "Best Practices", 3, 0.5, "mid"),
        ]
        prioritize_issues(issues)
        self.assertEqual(issues[0]["issue_id"], "high")
        self.assertEqual(issues[-1]["issue_id"], "low")

    def test_missing_fault_probability_treated_as_zero(self):
        issues = [
            make_issue("R1", "Best Practices", 3, None, "missing"),
            make_issue("R2", "Best Practices", 3, 0.5, "present"),
        ]
        prioritize_issues(issues)
        missing = next(i for i in issues if i["issue_id"] == "missing")
        self.assertEqual(missing["impact"], 0.0)

    def test_unknown_priority_uses_default(self):
        issues = [make_issue("R1", "Best Practices", 99, 0.5, "x")]
        prioritize_issues(issues)
        # Should not crash. Default sev weight is 0.25, default effort is 10.
        self.assertAlmostEqual(issues[0]["impact"], 0.5 * 0.25 * 1.0)
        self.assertEqual(issues[0]["effort_minutes"], 10)

    def test_unknown_ruleset_uses_default(self):
        issues = [make_issue("R1", "BogusRuleset", 3, 0.5, "x")]
        prioritize_issues(issues)
        self.assertEqual(issues[0]["ruleset_weight"], DEFAULT_RULESET_WEIGHT)

class TestTopNIssues(unittest.TestCase):
    def _ranked(self, items):
        # Quick helper: assign rank in order.
        for rank, item in enumerate(items, start=1):
            item["priority_rank"] = rank
        return items

    def test_returns_top_n(self):
        from production.stages.prioritize import top_n_issues
        issues = self._ranked([
            {"file_path": "/a", "score": 1.0, "id": "x"},
            {"file_path": "/b", "score": 0.5, "id": "y"},
            {"file_path": "/c", "score": 0.1, "id": "z"},
        ])
        result = top_n_issues(issues, n=2)
        self.assertEqual([i["id"] for i in result], ["x", "y"])

    def test_max_per_file_caps_repeats(self):
        from production.stages.prioritize import top_n_issues
        issues = self._ranked([
            {"file_path": "/a", "score": 1.0, "id": "1"},
            {"file_path": "/a", "score": 0.9, "id": "2"},
            {"file_path": "/a", "score": 0.8, "id": "3"},
            {"file_path": "/b", "score": 0.5, "id": "4"},
        ])
        result = top_n_issues(issues, n=10, max_per_file=2)
        # Should keep first 2 from /a, then /b.
        self.assertEqual([i["id"] for i in result], ["1", "2", "4"])

    def test_max_per_file_one_picks_one_per_file(self):
        from production.stages.prioritize import top_n_issues
        issues = self._ranked([
            {"file_path": "/a", "score": 1.0, "id": "1"},
            {"file_path": "/a", "score": 0.9, "id": "2"},
            {"file_path": "/b", "score": 0.5, "id": "3"},
        ])
        result = top_n_issues(issues, n=10, max_per_file=1)
        self.assertEqual([i["id"] for i in result], ["1", "3"])

    def test_empty_input(self):
        from production.stages.prioritize import top_n_issues
        self.assertEqual(top_n_issues([], n=5), [])

class TestComputePareto(unittest.TestCase):
    def test_empty_input(self):
        self.assertEqual(compute_pareto_front([]), [])

    def test_dominated_issue_excluded(self):
        # B dominates A: same effort, higher impact.
        issues = [
            {"impact": 0.1, "effort_minutes": 10, "id": "A"},
            {"impact": 0.5, "effort_minutes": 10, "id": "B"},
        ]
        front = compute_pareto_front(issues)
        ids = [i["id"] for i in front]
        self.assertIn("B", ids)
        self.assertNotIn("A", ids)

    def test_lower_effort_lower_impact_kept_if_not_dominated(self):
        # A has low impact but lowest effort; B has high impact, higher effort.
        # Both should be on the front.
        issues = [
            {"impact": 0.1, "effort_minutes": 2, "id": "A"},
            {"impact": 0.5, "effort_minutes": 10, "id": "B"},
        ]
        front = compute_pareto_front(issues)
        ids = [i["id"] for i in front]
        self.assertIn("A", ids)
        self.assertIn("B", ids)

    def test_front_sorted_by_effort_ascending(self):
        issues = [
            {"impact": 0.5, "effort_minutes": 10, "id": "med"},
            {"impact": 0.2, "effort_minutes": 2, "id": "cheap"},
            {"impact": 0.9, "effort_minutes": 50, "id": "expensive"},
        ]
        front = compute_pareto_front(issues)
        efforts = [i["effort_minutes"] for i in front]
        self.assertEqual(efforts, sorted(efforts))


class TestIntegrationFullPipeline(unittest.TestCase):
    """Stage 1 -> Stage 2 -> Stage 4 -> Stage 5 on commons-lang3."""

    COMMONS_LANG = (
        "/data/production/spikes/q1_agent_on_real_code/commons-lang"
    )
    MODEL_PATH = "/data/production/data/fault_predictor.pkl"

    def test_full_pipeline(self):
        if not Path(self.COMMONS_LANG).exists():
            self.skipTest("commons-lang3 not available")
        if not Path(self.MODEL_PATH).exists():
            self.skipTest("Trained model not available")

        from production.stages.ingest import ingest_repository
        from production.stages.analyze import analyze_repository
        from production.stages.predict import predict_fault_probability

        result = ingest_repository(self.COMMONS_LANG)
        issues = analyze_repository(result["java_source_root"])
        predict_fault_probability(
            issues, result["repo_root"], result["java_source_root"]
        )
        prioritize_issues(issues)
        front = compute_pareto_front(issues)

        # Sanity checks.
        for issue in issues:
            self.assertIn("priority_rank", issue)
            self.assertIn("score", issue)
            self.assertIn("impact", issue)
            self.assertIn("effort_minutes", issue)

        ranks = [i["priority_rank"] for i in issues]
        self.assertEqual(ranks, sorted(ranks))
        self.assertEqual(ranks[0], 1)
        self.assertEqual(ranks[-1], len(issues))

        # Pareto front should be non-empty and a subset.
        self.assertGreater(len(front), 0)
        self.assertLessEqual(len(front), len(issues))
        front_ids = {id(i) for i in front}
        all_ids = {id(i) for i in issues}
        self.assertTrue(front_ids.issubset(all_ids))


if __name__ == "__main__":
    unittest.main()