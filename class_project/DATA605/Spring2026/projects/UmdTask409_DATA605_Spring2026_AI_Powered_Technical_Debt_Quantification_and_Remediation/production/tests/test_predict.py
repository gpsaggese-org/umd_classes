"""Tests for production.stages.predict."""

import os
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

# Make production package importable.

from production.stages.predict import (
    predict_fault_probability,
    _build_feature_row,
    DEFAULT_MODEL_PATH,
)


COMMONS_LANG_REPO = (
    "/data/production/spikes/q1_agent_on_real_code/commons-lang"
)
COMMONS_LANG_SRC = (
    "/data/production/spikes/q1_agent_on_real_code/"
    "commons-lang/src/main/java"
)


class TestBuildFeatureRow(unittest.TestCase):
    def test_correct_order(self):
        metrics = {"COMPLEXITY": 100, "NCLOC": 5000}
        churn = {"files_changed": 3, "lines_added": 50}
        feature_names = ["COMPLEXITY", "files_changed", "NCLOC", "lines_added"]
        row = _build_feature_row(metrics, churn, feature_names)
        self.assertEqual(row, [100, 3, 5000, 50])

    def test_missing_feature_raises(self):
        metrics = {"COMPLEXITY": 100}
        churn = {"files_changed": 3}
        feature_names = ["COMPLEXITY", "MISSING_FEATURE"]
        with self.assertRaises(KeyError):
            _build_feature_row(metrics, churn, feature_names)


class TestPredictFaultProbabilityIntegration(unittest.TestCase):
    """End-to-end test: Stage 1 -> 2 -> 4, against commons-lang3."""

    def test_full_pipeline(self):
        if not Path(DEFAULT_MODEL_PATH).exists():
            self.skipTest(
                "Trained model not available; run "
                "production/scripts/train_fault_predictor.py first."
            )
        if not Path(COMMONS_LANG_REPO).exists():
            self.skipTest("commons-lang3 not available")

        from production.stages.ingest import ingest_repository
        from production.stages.analyze import analyze_repository

        result = ingest_repository(COMMONS_LANG_REPO)
        issues = analyze_repository(result["java_source_root"])
        # Limit to keep the test fast: take a sample.
        issues = issues[:50]

        augmented = predict_fault_probability(
            issues=issues,
            repo_root=result["repo_root"],
            java_source_root=result["java_source_root"],
        )

        self.assertEqual(len(augmented), 50)
        for issue in augmented:
            self.assertIn("fault_probability", issue)
            self.assertIn("host_commit", issue)
            if issue["fault_probability"] is not None:
                self.assertGreaterEqual(issue["fault_probability"], 0.0)
                self.assertLessEqual(issue["fault_probability"], 1.0)
            if issue["host_commit"] is not None:
                self.assertEqual(len(issue["host_commit"]), 40)

    def test_at_least_some_predictions_succeeded(self):
        if not Path(DEFAULT_MODEL_PATH).exists():
            self.skipTest("Trained model not available")
        if not Path(COMMONS_LANG_REPO).exists():
            self.skipTest("commons-lang3 not available")

        from production.stages.ingest import ingest_repository
        from production.stages.analyze import analyze_repository

        result = ingest_repository(COMMONS_LANG_REPO)
        issues = analyze_repository(result["java_source_root"])[:30]

        augmented = predict_fault_probability(
            issues=issues,
            repo_root=result["repo_root"],
            java_source_root=result["java_source_root"],
        )

        with_prob = [i for i in augmented if i["fault_probability"] is not None]
        self.assertGreater(
            len(with_prob), 0,
            "Expected at least some issues to receive a probability"
        )


class TestPredictMissingModel(unittest.TestCase):
    def test_raises_when_model_missing(self):
        with self.assertRaises(FileNotFoundError):
            predict_fault_probability(
                issues=[{"file_path": "/tmp/Foo.java"}],
                repo_root="/tmp",
                java_source_root="/tmp",
                model_path="/nonexistent/model.pkl",
            )


class TestPredictEmptyInput(unittest.TestCase):
    def test_empty_issues_returns_empty(self):
        if not Path(DEFAULT_MODEL_PATH).exists():
            self.skipTest("Trained model not available")
        if not Path(COMMONS_LANG_REPO).exists():
            self.skipTest("commons-lang3 not available")
        result = predict_fault_probability(
            issues=[],
            repo_root=COMMONS_LANG_REPO,
            java_source_root=COMMONS_LANG_SRC,
        )
        self.assertEqual(result, [])


if __name__ == "__main__":
    unittest.main()