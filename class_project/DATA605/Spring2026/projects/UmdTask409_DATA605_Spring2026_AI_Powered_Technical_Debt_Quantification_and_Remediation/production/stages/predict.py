"""
Stage 4: Predict fault probability for each issue.

For each issue from Stage 3, identify the commit that last touched its
file, build the 24-feature vector by combining repo-wide metrics (at HEAD)
with per-commit churn, and run the trained fault predictor to get a
probability that the host commit was fault-inducing.

Each issue gains two fields: fault_probability and host_commit. Issues
whose file has never been committed (or whose repo is not a git repo)
receive fault_probability=None.

Calibration caveat: the model was trained on SonarQube-derived metrics.
We feed it metrics reconstructed from javalang and git. The relative
ranking of probabilities is informative; absolute values may be skewed.
Documented in LIMITATIONS_AND_FUTURE_IMPROVEMENTS.md.

Usage:
    from production.stages.predict import predict_fault_probability
    issues = predict_fault_probability(
        issues=stage_3_issues,
        repo_root=ingest_result["repo_root"],
        java_source_root=ingest_result["java_source_root"],
    )
"""

import logging
import os
import pickle
from typing import Optional

import pandas as pd

from production.lib.metrics import (
    compute_repo_metrics,
    compute_commit_churn,
    find_last_touch_commit,
)

logger = logging.getLogger(__name__)


DEFAULT_MODEL_PATH = "/data/production/data/fault_predictor.pkl"


def predict_fault_probability(
    issues: list,
    repo_root: str,
    java_source_root: str,
    model_path: str = DEFAULT_MODEL_PATH,
) -> list:
    """Augment each issue with fault_probability and host_commit fields.

    Args:
        issues: list of issue dicts from Stage 3 (with file_path).
        repo_root: absolute path to the git repository root.
        java_source_root: absolute path to the Java source root.
        model_path: path to the pickled model artifact.

    Returns:
        The same issue list with each issue augmented in place.

    Raises:
        FileNotFoundError: if model_path or required paths don't exist.
    """
    if not os.path.exists(model_path):
        raise FileNotFoundError(
            f"Trained model not found at {model_path}. "
            "Run production/scripts/train_fault_predictor.py first."
        )
    if not os.path.isdir(repo_root):
        raise FileNotFoundError(f"repo_root not found: {repo_root}")
    if not os.path.isdir(java_source_root):
        raise FileNotFoundError(
            f"java_source_root not found: {java_source_root}"
        )

    if not issues:
        logger.info("No issues to predict on; returning empty list.")
        return issues

    logger.info("Loading model artifact from %s", model_path)
    artifact = _load_model_artifact(model_path)
    model = artifact["model"]
    feature_names = artifact["feature_names"]

    # Step 1: compute repo metrics once. Shared across all issues.
    logger.info("Computing repo metrics at HEAD")
    repo_metrics = compute_repo_metrics(java_source_root)

    # Step 2: find last-touch commit per unique file.
    unique_files = {issue["file_path"] for issue in issues}
    logger.info("Finding last-touch commit for %d unique files",
                len(unique_files))
    file_to_commit = {}
    for file_path in unique_files:
        try:
            sha = find_last_touch_commit(repo_root, file_path)
        except RuntimeError as e:
            logger.warning("git log failed for %s: %s", file_path, e)
            sha = None
        file_to_commit[file_path] = sha

    # Step 3: compute churn per unique commit.
    unique_commits = {sha for sha in file_to_commit.values() if sha}
    logger.info("Computing churn for %d unique commits", len(unique_commits))
    commit_to_churn = {}
    for sha in unique_commits:
        try:
            commit_to_churn[sha] = compute_commit_churn(repo_root, sha)
        except RuntimeError as e:
            logger.warning("Churn computation failed for %s: %s", sha, e)
            commit_to_churn[sha] = None

    # Step 4: build feature vectors per unique commit and predict in batch.
    feature_rows = []
    commit_order = []
    for sha in unique_commits:
        churn = commit_to_churn.get(sha)
        if churn is None:
            continue
        row = _build_feature_row(repo_metrics, churn, feature_names)
        feature_rows.append(row)
        commit_order.append(sha)

    commit_to_probability = {}
    if feature_rows:
        df = pd.DataFrame(feature_rows, columns=feature_names)
        # XGBClassifier.predict_proba returns probabilities for both
        # classes; we want the probability of class 1 (fault-inducing).
        probs = model.predict_proba(df)[:, 1]
        for sha, prob in zip(commit_order, probs):
            commit_to_probability[sha] = float(prob)
        logger.info("Predicted on %d commits; mean probability %.3f",
                    len(commit_order), probs.mean())
    else:
        logger.warning("No commits had usable churn; all probabilities None.")

    # Step 5: attach probability and host_commit to each issue.
    for issue in issues:
        sha = file_to_commit.get(issue["file_path"])
        issue["host_commit"] = sha
        issue["fault_probability"] = commit_to_probability.get(sha)

    return issues


def _load_model_artifact(model_path: str) -> dict:
    """Load the pickled model artifact and validate its shape."""
    with open(model_path, "rb") as f:
        artifact = pickle.load(f)
    required_keys = {"model", "feature_names"}
    missing = required_keys - set(artifact.keys())
    if missing:
        raise RuntimeError(
            f"Model artifact at {model_path} missing keys: {missing}"
        )
    return artifact


def _build_feature_row(metrics: dict, churn: dict,
                       feature_names: list) -> list:
    """Build one feature row in the order specified by feature_names."""
    combined = {**metrics, **churn}
    row = []
    for name in feature_names:
        if name not in combined:
            raise KeyError(
                f"Feature '{name}' missing from computed metrics/churn. "
                f"Available: {sorted(combined.keys())}"
            )
        row.append(combined[name])
    return row