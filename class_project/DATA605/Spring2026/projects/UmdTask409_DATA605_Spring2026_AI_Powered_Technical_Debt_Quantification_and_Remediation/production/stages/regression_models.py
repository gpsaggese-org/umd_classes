"""
Regression models for technical debt impact.

Three models trained on the Lenarduzzi V2 Technical Debt Dataset:
    Model A: defect density per file (n bug-inducing commits)
    Model B: issue resolution time (hours)
    Model C: team velocity (commits per developer per month)

All three predict on the log-scale during training and we expm1 to get
back to the original units. All three hold out commons-io for evaluation.

This module provides:
    - load_*_model() to load a trained pickle
    - predict_*() for inference
    - Helper functions to compute features from a fresh git repo
      (where applicable: Models A and C only; Model B requires Jira data
      that we do not have for an arbitrary repo).

Models train via production/scripts/train_regression_models.py.
"""

import logging
import pickle
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

import numpy as np
import pandas as pd

log = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "production" / "data"


# =====================================================================
# Loaders
# =====================================================================
def _load_pickle(name: str) -> dict:
    path = DATA_DIR / name
    if not path.exists():
        raise FileNotFoundError(
            f"{name} not found at {path}. "
            f"Run production/scripts/train_regression_models.py first."
        )
    log.info(f"Loading {name} from {path}")
    with open(path, "rb") as fh:
        return pickle.load(fh)


def load_defect_density_model() -> dict:
    return _load_pickle("defect_density_regressor.pkl")


def load_resolution_time_model() -> dict:
    return _load_pickle("resolution_time_regressor.pkl")


def load_velocity_model() -> dict:
    return _load_pickle("velocity_regressor.pkl")


# =====================================================================
# Model A: Defect density predictions
# =====================================================================
def predict_defect_density(artifact: dict, features_df: pd.DataFrame) -> np.ndarray:
    """Predict bug counts per file. features_df must have the model's
    feature columns. Returns predictions in the original (bugs) scale."""
    model = artifact["model"]
    feature_names = artifact["feature_names"]
    missing = [c for c in feature_names if c not in features_df.columns]
    if missing:
        raise ValueError(f"Missing feature columns: {missing}")
    X = features_df[feature_names].astype(float).values
    log_pred = model.predict(X)
    return np.expm1(log_pred).clip(min=0)


def compute_file_features_from_repo(
    repo_path: str,
    java_only: bool = True,
) -> pd.DataFrame:
    """Compute Model A's features for every file in a fresh git repo.
    Uses git log for churn data."""
    log.info(f"Computing per-file churn features from {repo_path}")
    try:
        from pydriller import Repository
    except ImportError as e:
        raise ImportError("pydriller is required: pip install pydriller") from e

    rows = []
    file_data: dict = {}

    for commit in Repository(repo_path).traverse_commits():
        for m in commit.modified_files:
            path = m.new_path or m.old_path
            if path is None:
                continue
            if java_only and not path.endswith(".java"):
                continue
            d = file_data.setdefault(
                path,
                {
                    "FILE": path,
                    "n_commits": 0,
                    "authors": set(),
                    "lines_added": 0,
                    "lines_removed": 0,
                    "first_touch": commit.author_date,
                    "last_touch": commit.author_date,
                },
            )
            d["n_commits"] += 1
            d["authors"].add(commit.author.name)
            d["lines_added"] += m.added_lines or 0
            d["lines_removed"] += m.deleted_lines or 0
            if commit.author_date < d["first_touch"]:
                d["first_touch"] = commit.author_date
            if commit.author_date > d["last_touch"]:
                d["last_touch"] = commit.author_date

    for path, d in file_data.items():
        rows.append(
            {
                "FILE": path,
                "n_commits": d["n_commits"],
                "n_authors": len(d["authors"]),
                "lines_added": d["lines_added"],
                "lines_removed": d["lines_removed"],
                "lines_per_commit": (d["lines_added"] + d["lines_removed"])
                / max(d["n_commits"], 1),
                "net_lines": d["lines_added"] - d["lines_removed"],
                "file_age_days": (d["last_touch"] - d["first_touch"]).total_seconds()
                / 86400.0,
                "is_test_file": int("/test/" in path.lower()),
            }
        )
    df = pd.DataFrame(rows)
    log.info(f"Computed features for {len(df)} files")
    return df


# =====================================================================
# Model B: Issue resolution time
# =====================================================================
def predict_resolution_time(artifact: dict, features_df: pd.DataFrame) -> np.ndarray:
    """Predict hours-to-resolve for issues. features_df must have all
    one-hot type/priority columns the model was trained on."""
    model = artifact["model"]
    feature_names = artifact["feature_names"]
    # Add missing columns as zero (means that category wasn't present)
    for c in feature_names:
        if c not in features_df.columns:
            features_df[c] = 0
    X = features_df[feature_names].astype(float).values
    log_pred = model.predict(X)
    return np.expm1(log_pred).clip(min=0)


def build_issue_features_for_inference(
    issues_df: pd.DataFrame,
    artifact: dict,
) -> pd.DataFrame:
    """Take a raw issues df with TYPE, PRIORITY, votes, watch_count,
    description_length, summary_length and produce the one-hot dataframe
    Model B expects."""
    df = issues_df.copy()
    df["votes"] = df.get("votes", 0).fillna(0) if "votes" in df.columns else 0
    df["watch_count"] = (
        df.get("watch_count", 0).fillna(0) if "watch_count" in df.columns else 0
    )
    df["description_length"] = (
        df.get("description_length", 0).fillna(0)
        if "description_length" in df.columns else 0
    )
    df["summary_length"] = (
        df.get("summary_length", 0).fillna(0)
        if "summary_length" in df.columns else 0
    )

    type_cats = artifact["training_metadata"]["type_categories"]
    priority_cats = artifact["training_metadata"]["priority_categories"]

    # Add one-hot columns
    if "TYPE" in df.columns:
        for cat in type_cats:
            label = cat[len("type_"):]
            df[cat] = (df["TYPE"] == label).astype(int)
    else:
        for cat in type_cats:
            df[cat] = 0
    if "PRIORITY" in df.columns:
        for cat in priority_cats:
            label = cat[len("priority_"):]
            df[cat] = (df["PRIORITY"] == label).astype(int)
    else:
        for cat in priority_cats:
            df[cat] = 0
    return df


# =====================================================================
# Model C: Velocity predictions
# =====================================================================
def predict_velocity(artifact: dict, features_df: pd.DataFrame) -> np.ndarray:
    """Predict commits-per-developer-per-month. features_df must have
    the model's feature columns."""
    model = artifact["model"]
    feature_names = artifact["feature_names"]
    missing = [c for c in feature_names if c not in features_df.columns]
    if missing:
        raise ValueError(f"Missing feature columns: {missing}")
    X = features_df[feature_names].astype(float).values
    log_pred = model.predict(X)
    return np.expm1(log_pred).clip(min=0)


def compute_project_month_features_from_repo(repo_path: str) -> pd.DataFrame:
    """Compute Model C's features for the given repo, month by month.
    Note: SonarQube features (avg_ncloc, avg_complexity, avg_code_smells,
    avg_sqale_index) are not available from a fresh repo without analysis,
    so this fills them with the training-set medians as a placeholder."""
    log.info(f"Computing project-month features from {repo_path}")
    try:
        from pydriller import Repository
    except ImportError as e:
        raise ImportError("pydriller is required") from e

    monthly = {}
    project_first = None

    for commit in Repository(repo_path).traverse_commits():
        if commit.merge:
            continue
        ts = commit.author_date
        month_key = ts.strftime("%Y-%m")
        if project_first is None or ts < project_first:
            project_first = ts
        d = monthly.setdefault(
            month_key,
            {"month": month_key, "n_commits": 0, "authors": set(), "n_bug_commits": 0},
        )
        d["n_commits"] += 1
        d["authors"].add(commit.author.name)

    rows = []
    # Placeholder values for SonarQube-derived features
    placeholder_ncloc = 5000.0
    placeholder_complexity = 100.0
    placeholder_code_smells = 50.0
    placeholder_sqale_index = 1000.0

    for month_key, d in sorted(monthly.items()):
        month_dt = datetime.strptime(month_key + "-01", "%Y-%m-%d").replace(
            tzinfo=timezone.utc
        )
        if project_first is not None:
            age_months = int((month_dt - project_first.astimezone(timezone.utc)).days / 30)
        else:
            age_months = 0
        rows.append(
            {
                "month": month_key,
                "n_commits": d["n_commits"],
                "n_authors": len(d["authors"]),
                "n_bug_commits": d["n_bug_commits"],
                "avg_ncloc": placeholder_ncloc,
                "avg_complexity": placeholder_complexity,
                "avg_code_smells": placeholder_code_smells,
                "avg_sqale_index": placeholder_sqale_index,
                "project_age_months": age_months,
                "actual_velocity": d["n_commits"] / max(len(d["authors"]), 1),
            }
        )
    df = pd.DataFrame(rows)
    log.info(f"Computed features for {len(df)} months")
    return df