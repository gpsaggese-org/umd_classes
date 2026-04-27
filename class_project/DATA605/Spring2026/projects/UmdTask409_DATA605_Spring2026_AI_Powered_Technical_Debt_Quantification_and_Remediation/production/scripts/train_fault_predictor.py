"""
One-off training script for the Stage 4 fault predictor.

This script trains the XGBoost fault-inducing commit classifier the
same way the MVP example notebook does (Section 4b), and pickles the
trained model plus its feature names to disk. Stage 4 (predict.py)
loads the pickle on every pipeline run.

This script needs to run only once. Re-run it if:
    - The dataset (td_V2.db) is updated.
    - The MVP changes its training procedure.
    - The model artifact is missing or corrupted.

Run from inside the Docker container:
    cd /data && python production/scripts/train_fault_predictor.py

Output:
    /data/production/data/fault_predictor.pkl
"""

import logging
import os
import pickle
import sys
import time
from pathlib import Path

# Make ai_technical_debt_utils importable.
sys.path.insert(0, "/data")

import ai_technical_debt_utils as utils

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
logger = logging.getLogger("train_fault_predictor")


# Inputs.
DB_PATH = "/data/data/td_V2.db"
TARGET_PROJECT = utils.DEFAULT_TARGET_PROJECT
ISSUES_CAP = utils.DEFAULT_ISSUES_PER_PROJECT_CAP

# Output.
OUTPUT_PATH = "/data/production/data/fault_predictor.pkl"


def main():
    if not os.path.exists(DB_PATH):
        raise FileNotFoundError(
            f"Dataset not found at {DB_PATH}. Cannot train."
        )

    logger.info("Connecting to dataset at %s", DB_PATH)
    conn = utils.connect_to_database(DB_PATH)

    logger.info("Building training/target split (target held out: %s)",
                TARGET_PROJECT)
    all_projects = utils.get_projects(conn)["PROJECT_ID"].tolist()
    training_projects = [p for p in all_projects if p != TARGET_PROJECT]
    logger.info("Training projects: %d (target held out)",
                len(training_projects))

    logger.info(
        "Building fault-prediction training matrix "
        "(this takes about a minute)..."
    )
    t0 = time.time()
    training_data = utils.build_multi_project_fault_prediction_data(
        conn=conn,
        project_ids=training_projects,
        commits_per_project_cap=ISSUES_CAP,
    )
    logger.info(
        "Training matrix built in %.1fs: shape %s",
        time.time() - t0,
        training_data.shape,
    )

    fault_rate = training_data["IS_FAULT_INDUCING"].mean()
    logger.info(
        "Class balance: %.1f%% fault-inducing of %d commits",
        100 * fault_rate,
        len(training_data),
    )

    logger.info("Training XGBoost classifier (this takes about a minute)...")
    t0 = time.time()
    result = utils.train_fault_inducing_predictor(
        training_data=training_data,
        random_state=42,
    )
    logger.info("Training complete in %.1fs", time.time() - t0)

    metrics = result.get("metrics", {})
    if metrics:
        logger.info("Test-set metrics:")
        for k, v in metrics.items():
            if isinstance(v, float):
                logger.info("  %s: %.4f", k, v)
            else:
                logger.info("  %s: %s", k, v)

    # Persist the artifact: the model itself plus the feature names so
    # Stage 4 knows what column order to feed it. We do not save X_test/
    # y_test from training; the pickle stays small (a few MB).
    artifact = {
        "model": result["model"],
        "feature_names": result["feature_names"],
        "normalization_stats": result.get("normalization_stats"),
        "training_metrics": metrics,
        "training_projects": training_projects,
        "target_project": TARGET_PROJECT,
        "trained_at": time.time(),
    }

    output_dir = os.path.dirname(OUTPUT_PATH)
    os.makedirs(output_dir, exist_ok=True)

    with open(OUTPUT_PATH, "wb") as f:
        pickle.dump(artifact, f)

    size_mb = os.path.getsize(OUTPUT_PATH) / 1024 / 1024
    logger.info("Saved model artifact to %s (%.2f MB)",
                OUTPUT_PATH, size_mb)
    logger.info("Feature names (%d): %s",
                len(artifact["feature_names"]),
                ", ".join(artifact["feature_names"]))


if __name__ == "__main__":
    main()