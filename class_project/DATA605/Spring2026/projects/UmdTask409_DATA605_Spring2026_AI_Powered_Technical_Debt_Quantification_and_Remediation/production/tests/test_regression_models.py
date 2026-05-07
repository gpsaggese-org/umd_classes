"""Tests for production.stages.regression_models."""

import os
import pickle
import unittest
from pathlib import Path

import numpy as np
import pandas as pd

from production.stages import regression_models as rm

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "production" / "data"
COMMONS_LANG_PATH = (
    PROJECT_ROOT / "production" / "spikes" / "q1_agent_on_real_code" / "commons-lang"
)


class TestArtifactLoading(unittest.TestCase):
    """The three artifacts must load and have expected structure."""

    def _check_artifact(self, artifact: dict, expected_keys: list):
        self.assertIn("model", artifact)
        self.assertIn("feature_names", artifact)
        self.assertIn("holdout_metrics", artifact)
        self.assertIn("target_transform", artifact)
        self.assertEqual(artifact["target_transform"], "log1p")
        for k in expected_keys:
            self.assertIn(k, artifact["holdout_metrics"])

    def test_defect_density_artifact(self):
        path = DATA_DIR / "defect_density_regressor.pkl"
        if not path.exists():
            self.skipTest("Run train_regression_models.py first")
        artifact = rm.load_defect_density_model()
        self._check_artifact(
            artifact,
            ["r2_log", "mae_log", "rmse_log", "mae_bugs", "rmse_bugs"],
        )

    def test_resolution_time_artifact(self):
        path = DATA_DIR / "resolution_time_regressor.pkl"
        if not path.exists():
            self.skipTest("Run train_regression_models.py first")
        artifact = rm.load_resolution_time_model()
        self._check_artifact(
            artifact,
            ["r2_log", "mae_log", "rmse_log", "mae_hours", "rmse_hours"],
        )

    def test_velocity_artifact(self):
        path = DATA_DIR / "velocity_regressor.pkl"
        if not path.exists():
            self.skipTest("Run train_regression_models.py first")
        artifact = rm.load_velocity_model()
        self._check_artifact(
            artifact,
            ["r2_log", "mae_log", "rmse_log", "mae_velocity", "rmse_velocity"],
        )


class TestPredictionShapes(unittest.TestCase):
    """Predictions should produce non-negative values of the right shape."""

    def test_defect_density_prediction(self):
        path = DATA_DIR / "defect_density_regressor.pkl"
        if not path.exists():
            self.skipTest("Run train_regression_models.py first")
        artifact = rm.load_defect_density_model()
        df = pd.DataFrame(
            {
                "n_commits": [10, 50, 200],
                "n_authors": [3, 8, 20],
                "lines_added": [500, 5000, 25000],
                "lines_removed": [100, 1000, 10000],
                "lines_per_commit": [60.0, 120.0, 175.0],
                "net_lines": [400, 4000, 15000],
                "file_age_days": [365.0, 1825.0, 3650.0],
                "is_test_file": [0, 0, 1],
            }
        )
        preds = rm.predict_defect_density(artifact, df)
        self.assertEqual(len(preds), 3)
        self.assertTrue((preds >= 0).all())

    def test_velocity_prediction(self):
        path = DATA_DIR / "velocity_regressor.pkl"
        if not path.exists():
            self.skipTest("Run train_regression_models.py first")
        artifact = rm.load_velocity_model()
        df = pd.DataFrame(
            {
                "n_authors": [5, 15],
                "n_bug_commits": [2, 10],
                "avg_ncloc": [5000.0, 50000.0],
                "avg_complexity": [100.0, 1000.0],
                "avg_code_smells": [50.0, 500.0],
                "avg_sqale_index": [1000.0, 10000.0],
                "project_age_months": [12, 60],
            }
        )
        preds = rm.predict_velocity(artifact, df)
        self.assertEqual(len(preds), 2)
        self.assertTrue((preds >= 0).all())

    def test_resolution_time_prediction_with_inference_helper(self):
        path = DATA_DIR / "resolution_time_regressor.pkl"
        if not path.exists():
            self.skipTest("Run train_regression_models.py first")
        artifact = rm.load_resolution_time_model()
        raw = pd.DataFrame(
            {
                "TYPE": ["Bug", "Improvement"],
                "PRIORITY": ["Major", "Minor"],
                "votes": [3, 1],
                "watch_count": [5, 2],
                "description_length": [500, 200],
                "summary_length": [50, 30],
            }
        )
        feat_df = rm.build_issue_features_for_inference(raw, artifact)
        preds = rm.predict_resolution_time(artifact, feat_df)
        self.assertEqual(len(preds), 2)
        self.assertTrue((preds >= 0).all())


class TestRepoFeatureExtraction(unittest.TestCase):
    """compute_*_from_repo functions should produce the right columns."""

    def test_file_features_from_repo(self):
        if not COMMONS_LANG_PATH.exists():
            self.skipTest("commons-lang not present locally")
        df = rm.compute_file_features_from_repo(str(COMMONS_LANG_PATH))
        expected = {
            "FILE", "n_commits", "n_authors", "lines_added", "lines_removed",
            "lines_per_commit", "net_lines", "file_age_days", "is_test_file",
        }
        self.assertTrue(expected.issubset(set(df.columns)))
        self.assertGreater(len(df), 100)

    def test_project_month_features_from_repo(self):
        if not COMMONS_LANG_PATH.exists():
            self.skipTest("commons-lang not present locally")
        df = rm.compute_project_month_features_from_repo(str(COMMONS_LANG_PATH))
        expected = {
            "month", "n_commits", "n_authors", "n_bug_commits",
            "avg_ncloc", "avg_complexity", "avg_code_smells",
            "avg_sqale_index", "project_age_months", "actual_velocity",
        }
        self.assertTrue(expected.issubset(set(df.columns)))
        self.assertGreater(len(df), 10)


class TestEndToEndDefectDensity(unittest.TestCase):
    """Full end-to-end: load model, compute features from commons-lang3,
    predict, ensure top predictions look reasonable."""

    def test_e2e_commons_lang(self):
        if not COMMONS_LANG_PATH.exists():
            self.skipTest("commons-lang not present locally")
        path = DATA_DIR / "defect_density_regressor.pkl"
        if not path.exists():
            self.skipTest("Run train_regression_models.py first")
        artifact = rm.load_defect_density_model()
        features = rm.compute_file_features_from_repo(str(COMMONS_LANG_PATH))
        preds = rm.predict_defect_density(artifact, features)
        self.assertEqual(len(preds), len(features))
        # Top predicted file should have many commits and authors
        features["pred_bugs"] = preds
        top = features.nlargest(5, "pred_bugs")
        self.assertGreater(top["n_commits"].mean(), 5)


if __name__ == "__main__":
    unittest.main()