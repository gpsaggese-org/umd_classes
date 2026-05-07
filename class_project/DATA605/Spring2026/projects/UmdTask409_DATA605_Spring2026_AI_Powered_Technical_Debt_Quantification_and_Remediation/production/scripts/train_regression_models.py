"""
Train three regression models on the Lenarduzzi V2 Technical Debt Dataset.

Models:
1. Defect density per file (n bug-inducing commits per Java file)
2. Issue resolution time (TIME_SPENT in hours per Jira issue)
3. Team velocity (commits per developer per month per project)

Holdout: commons-io (matches the existing fault predictor's protocol).

Outputs three pickles in production/data/:
  - defect_density_regressor.pkl
  - resolution_time_regressor.pkl
  - velocity_regressor.pkl

Each pickle contains: model, feature_names, holdout_metrics, training_metadata.

Run from project root:
    python production/scripts/train_regression_models.py
"""

import logging
import pickle
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
import xgboost as xgb
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
log = logging.getLogger("train_regression_models")

# ------- Configuration -------
PROJECT_ROOT = Path(__file__).resolve().parents[2]
DB_PATH = PROJECT_ROOT / "production" / "data" / "td_V2.db"
OUT_DIR = PROJECT_ROOT / "production" / "data"
HOLDOUT_PROJECT = "org.apache:commons-io"

XGB_PARAMS = {
    "max_depth": 6,
    "learning_rate": 0.1,
    "n_estimators": 300,
    "objective": "reg:squarederror",
    "random_state": 42,
    "n_jobs": 4,
}


# =====================================================================
# Model A: Defect density per file
# =====================================================================
def build_defect_density_dataset(conn: sqlite3.Connection) -> pd.DataFrame:
    """Aggregate per-file features and bug counts across all projects."""
    log.info("Model A: building defect density dataset")
    log.info("Model A: querying file-level churn from GIT_COMMITS_CHANGES")
    churn_q = """
    SELECT
      gcc.PROJECT_ID,
      gcc.FILE,
      COUNT(DISTINCT gcc.COMMIT_HASH)        AS n_commits,
      COUNT(DISTINCT gcc.COMMITTER_ID)       AS n_authors,
      COALESCE(SUM(CAST(gcc.LINES_ADDED   AS INTEGER)), 0) AS lines_added,
      COALESCE(SUM(CAST(gcc.LINES_REMOVED AS INTEGER)), 0) AS lines_removed,
      MIN(gcc.DATE) AS first_touch,
      MAX(gcc.DATE) AS last_touch
    FROM GIT_COMMITS_CHANGES gcc
    WHERE gcc.FILE LIKE '%.java'
    GROUP BY gcc.PROJECT_ID, gcc.FILE
    """
    churn = pd.read_sql(churn_q, conn)
    log.info(f"Model A: {len(churn):,} (project, file) rows from churn")

    log.info("Model A: querying bug counts via SZZ join")
    bugs_q = """
    SELECT
      gcc.PROJECT_ID,
      gcc.FILE,
      COUNT(DISTINCT s.FAULT_INDUCING_COMMIT_HASH) AS n_bug_commits
    FROM SZZ_FAULT_INDUCING_COMMITS s
    JOIN GIT_COMMITS_CHANGES gcc
      ON s.FAULT_INDUCING_COMMIT_HASH = gcc.COMMIT_HASH
     AND s.PROJECT_ID = gcc.PROJECT_ID
    WHERE gcc.FILE LIKE '%.java'
    GROUP BY gcc.PROJECT_ID, gcc.FILE
    """
    bugs = pd.read_sql(bugs_q, conn)
    log.info(f"Model A: {len(bugs):,} files have at least one bug-inducing commit")

    df = churn.merge(bugs, on=["PROJECT_ID", "FILE"], how="left")
    df["n_bug_commits"] = df["n_bug_commits"].fillna(0).astype(int)

    # Feature: file age in days
    df["first_touch_dt"] = pd.to_datetime(df["first_touch"], errors="coerce", utc=True)
    df["last_touch_dt"] = pd.to_datetime(df["last_touch"], errors="coerce", utc=True)
    df["file_age_days"] = (
        (df["last_touch_dt"] - df["first_touch_dt"]).dt.total_seconds() / 86400.0
    ).fillna(0)

    # Feature: is the file in a test directory?
    df["is_test_file"] = df["FILE"].str.contains("/test/", case=False, regex=False).astype(int)

    # Feature: lines per commit (intensity proxy)
    df["lines_per_commit"] = (df["lines_added"] + df["lines_removed"]) / df["n_commits"].clip(lower=1)

    # Feature: net lines (additions minus removals)
    df["net_lines"] = df["lines_added"] - df["lines_removed"]

    log.info(
        f"Model A: dataset shape={df.shape}, "
        f"target mean={df['n_bug_commits'].mean():.2f}, "
        f"target max={df['n_bug_commits'].max()}"
    )
    return df


def train_defect_density_model(df: pd.DataFrame) -> dict:
    """Train Model A and save artifact. Returns metrics dict."""
    log.info("Model A: training")

    feature_cols = [
        "n_commits",
        "n_authors",
        "lines_added",
        "lines_removed",
        "lines_per_commit",
        "net_lines",
        "file_age_days",
        "is_test_file",
    ]

    train_mask = df["PROJECT_ID"] != HOLDOUT_PROJECT
    test_mask = df["PROJECT_ID"] == HOLDOUT_PROJECT
    log.info(f"Model A: train rows={train_mask.sum():,}, test rows={test_mask.sum():,}")

    X_train = df.loc[train_mask, feature_cols].values
    X_test = df.loc[test_mask, feature_cols].values
    # Log-transform target to handle skew
    y_train = np.log1p(df.loc[train_mask, "n_bug_commits"].values)
    y_test_orig = df.loc[test_mask, "n_bug_commits"].values
    y_test = np.log1p(y_test_orig)

    model = xgb.XGBRegressor(**XGB_PARAMS)
    model.fit(X_train, y_train)

    pred_log = model.predict(X_test)
    pred_orig = np.expm1(pred_log).clip(min=0)

    metrics = {
        "r2_log": float(r2_score(y_test, pred_log)),
        "mae_log": float(mean_absolute_error(y_test, pred_log)),
        "rmse_log": float(np.sqrt(mean_squared_error(y_test, pred_log))),
        "mae_bugs": float(mean_absolute_error(y_test_orig, pred_orig)),
        "rmse_bugs": float(np.sqrt(mean_squared_error(y_test_orig, pred_orig))),
        "test_n": int(test_mask.sum()),
        "train_n": int(train_mask.sum()),
    }
    log.info(f"Model A holdout metrics: {metrics}")

    artifact = {
        "model": model,
        "feature_names": feature_cols,
        "holdout_metrics": metrics,
        "target_transform": "log1p",
        "training_metadata": {
            "trained_at": datetime.now(timezone.utc).isoformat(),
            "holdout_project": HOLDOUT_PROJECT,
            "n_train_files": int(train_mask.sum()),
            "n_test_files": int(test_mask.sum()),
            "xgb_params": XGB_PARAMS,
        },
    }
    out = OUT_DIR / "defect_density_regressor.pkl"
    with open(out, "wb") as fh:
        pickle.dump(artifact, fh)
    log.info(f"Model A: saved to {out}")
    return metrics


# =====================================================================
# Model B: Issue resolution time
# =====================================================================
def build_resolution_time_dataset(conn: sqlite3.Connection) -> pd.DataFrame:
    """Build per-issue features for issues that have TIME_SPENT populated."""
    log.info("Model B: building resolution time dataset")
    q = """
    SELECT
      PROJECT_ID,
      KEY,
      TYPE,
      PRIORITY,
      STATUS,
      CAST(VOTES AS INTEGER)        AS votes,
      CAST(WATCH_COUNT AS INTEGER)  AS watch_count,
      LENGTH(DESCRIPTION)           AS description_length,
      LENGTH(SUMMARY)               AS summary_length,
      CAST(TIME_SPENT AS REAL)      AS time_spent_seconds,
      CREATION_DATE
    FROM JIRA_ISSUES
    WHERE TIME_SPENT != ''
      AND TIME_SPENT IS NOT NULL
      AND CAST(TIME_SPENT AS REAL) > 0
    """
    df = pd.read_sql(q, conn)
    log.info(f"Model B: {len(df):,} issues with TIME_SPENT populated")

    # Convert to hours
    df["time_spent_hours"] = df["time_spent_seconds"] / 3600.0

    # Filter outliers: drop top 1% (>40 hours is suspicious)
    cap = df["time_spent_hours"].quantile(0.99)
    log.info(f"Model B: 99th percentile of time_spent_hours = {cap:.2f}")
    df = df[df["time_spent_hours"] <= cap].copy()
    log.info(f"Model B: after 99th-percentile cap: {len(df):,} rows")

    df["description_length"] = df["description_length"].fillna(0)
    df["summary_length"] = df["summary_length"].fillna(0)
    df["votes"] = df["votes"].fillna(0)
    df["watch_count"] = df["watch_count"].fillna(0)

    # Categorical features as one-hot
    df = pd.concat(
        [
            df,
            pd.get_dummies(df["TYPE"], prefix="type"),
            pd.get_dummies(df["PRIORITY"], prefix="priority"),
        ],
        axis=1,
    )

    log.info(
        f"Model B: dataset shape={df.shape}, "
        f"target mean (hours)={df['time_spent_hours'].mean():.2f}, "
        f"target median (hours)={df['time_spent_hours'].median():.2f}"
    )
    return df


def train_resolution_time_model(df: pd.DataFrame) -> dict:
    """Train Model B and save artifact. Returns metrics dict."""
    log.info("Model B: training")

    type_cols = [c for c in df.columns if c.startswith("type_")]
    priority_cols = [c for c in df.columns if c.startswith("priority_")]
    feature_cols = [
        "votes",
        "watch_count",
        "description_length",
        "summary_length",
    ] + type_cols + priority_cols

    train_mask = df["PROJECT_ID"] != HOLDOUT_PROJECT
    test_mask = df["PROJECT_ID"] == HOLDOUT_PROJECT
    log.info(f"Model B: train rows={train_mask.sum():,}, test rows={test_mask.sum():,}")

    if test_mask.sum() < 5:
        log.warning(
            f"Model B: holdout project '{HOLDOUT_PROJECT}' has only "
            f"{test_mask.sum()} issues with TIME_SPENT. Falling back to "
            "20% random holdout for evaluation."
        )
        rng = np.random.default_rng(42)
        all_idx = np.arange(len(df))
        rng.shuffle(all_idx)
        cutoff = int(len(df) * 0.8)
        train_idx = all_idx[:cutoff]
        test_idx = all_idx[cutoff:]
        train_mask = pd.Series(False, index=df.index)
        test_mask = pd.Series(False, index=df.index)
        train_mask.iloc[train_idx] = True
        test_mask.iloc[test_idx] = True
        log.info(
            f"Model B: random split train={train_mask.sum()}, test={test_mask.sum()}"
        )

    X_train = df.loc[train_mask, feature_cols].astype(float).values
    X_test = df.loc[test_mask, feature_cols].astype(float).values
    y_train = np.log1p(df.loc[train_mask, "time_spent_hours"].values)
    y_test_orig = df.loc[test_mask, "time_spent_hours"].values
    y_test = np.log1p(y_test_orig)

    model = xgb.XGBRegressor(**XGB_PARAMS)
    model.fit(X_train, y_train)

    pred_log = model.predict(X_test)
    pred_orig = np.expm1(pred_log).clip(min=0)

    metrics = {
        "r2_log": float(r2_score(y_test, pred_log)),
        "mae_log": float(mean_absolute_error(y_test, pred_log)),
        "rmse_log": float(np.sqrt(mean_squared_error(y_test, pred_log))),
        "mae_hours": float(mean_absolute_error(y_test_orig, pred_orig)),
        "rmse_hours": float(np.sqrt(mean_squared_error(y_test_orig, pred_orig))),
        "test_n": int(test_mask.sum()),
        "train_n": int(train_mask.sum()),
    }
    log.info(f"Model B holdout metrics: {metrics}")

    artifact = {
        "model": model,
        "feature_names": feature_cols,
        "holdout_metrics": metrics,
        "target_transform": "log1p",
        "training_metadata": {
            "trained_at": datetime.now(timezone.utc).isoformat(),
            "holdout_project": HOLDOUT_PROJECT,
            "n_train_issues": int(train_mask.sum()),
            "n_test_issues": int(test_mask.sum()),
            "xgb_params": XGB_PARAMS,
            "type_categories": type_cols,
            "priority_categories": priority_cols,
        },
    }
    out = OUT_DIR / "resolution_time_regressor.pkl"
    with open(out, "wb") as fh:
        pickle.dump(artifact, fh)
    log.info(f"Model B: saved to {out}")
    return metrics


# =====================================================================
# Model C: Team velocity
# =====================================================================
def build_velocity_dataset(conn: sqlite3.Connection) -> pd.DataFrame:
    """Build (project, month) rows with velocity target and debt features."""
    log.info("Model C: building velocity dataset")
    log.info("Model C: aggregating commits per project-month")
    commit_q = """
    SELECT
      PROJECT_ID,
      strftime('%Y-%m', AUTHOR_DATE) AS month,
      COUNT(*)                       AS n_commits,
      COUNT(DISTINCT AUTHOR)         AS n_authors
    FROM GIT_COMMITS
    WHERE IN_MAIN_BRANCH = 'True'
      AND MERGE = 'False'
      AND AUTHOR_DATE IS NOT NULL
      AND AUTHOR_DATE != ''
    GROUP BY PROJECT_ID, month
    """
    commits = pd.read_sql(commit_q, conn)
    commits = commits[commits["month"].notna() & (commits["month"] != "")].copy()
    log.info(f"Model C: {len(commits):,} project-month rows from commits")

    # Velocity target: commits per developer per month
    commits["velocity"] = commits["n_commits"] / commits["n_authors"].clip(lower=1)

    log.info("Model C: aggregating bug counts per project-month")
    bugs_q = """
    SELECT
      gc.PROJECT_ID,
      strftime('%Y-%m', gc.AUTHOR_DATE) AS month,
      COUNT(DISTINCT s.FAULT_INDUCING_COMMIT_HASH) AS n_bug_commits
    FROM SZZ_FAULT_INDUCING_COMMITS s
    JOIN GIT_COMMITS gc
      ON s.FAULT_INDUCING_COMMIT_HASH = gc.COMMIT_HASH
     AND s.PROJECT_ID = gc.PROJECT_ID
    WHERE gc.IN_MAIN_BRANCH = 'True'
      AND gc.AUTHOR_DATE IS NOT NULL
    GROUP BY gc.PROJECT_ID, month
    """
    bugs = pd.read_sql(bugs_q, conn)
    log.info(f"Model C: {len(bugs):,} project-month rows have bugs")

    log.info("Model C: aggregating sonar issue counts per project-month")
    sonar_q = """
    SELECT
      sa.PROJECT_ID,
      strftime('%Y-%m', sa.DATE) AS month,
      AVG(CAST(sm.NCLOC AS INTEGER))           AS avg_ncloc,
      AVG(CAST(sm.COMPLEXITY AS REAL))         AS avg_complexity,
      AVG(CAST(sm.CODE_SMELLS AS REAL))        AS avg_code_smells,
      AVG(CAST(sm.SQALE_INDEX AS REAL))        AS avg_sqale_index
    FROM SONAR_ANALYSIS sa
    JOIN SONAR_MEASURES sm
      ON sm.ANALYSIS_KEY = sa.ANALYSIS_KEY
    WHERE sa.DATE IS NOT NULL
    GROUP BY sa.PROJECT_ID, month
    """
    try:
        sonar = pd.read_sql(sonar_q, conn)
        log.info(f"Model C: {len(sonar):,} project-month rows from SonarQube")
    except Exception as e:
        log.warning(f"Model C: SonarQube join failed ({e}); proceeding without")
        sonar = pd.DataFrame(columns=[
            "PROJECT_ID", "month", "avg_ncloc", "avg_complexity",
            "avg_code_smells", "avg_sqale_index",
        ])

    # Merge everything
    df = commits.merge(bugs, on=["PROJECT_ID", "month"], how="left")
    df["n_bug_commits"] = df["n_bug_commits"].fillna(0).astype(int)
    df = df.merge(sonar, on=["PROJECT_ID", "month"], how="left")
    for c in ["avg_ncloc", "avg_complexity", "avg_code_smells", "avg_sqale_index"]:
        if c not in df.columns:
            df[c] = np.nan
        df[c] = df[c].fillna(df[c].median() if df[c].notna().any() else 0)

    # Project age in months at this point
    df["month_dt"] = pd.to_datetime(df["month"] + "-01", errors="coerce", utc=True)
    df = df[df["month_dt"].notna()].copy()
    df["project_first_month"] = df.groupby("PROJECT_ID")["month_dt"].transform("min")
    df["project_age_months"] = (
        (df["month_dt"] - df["project_first_month"]).dt.days / 30.0
    ).round().astype(int)

    log.info(
        f"Model C: dataset shape={df.shape}, "
        f"target mean velocity={df['velocity'].mean():.2f}, "
        f"target median velocity={df['velocity'].median():.2f}"
    )
    return df


def train_velocity_model(df: pd.DataFrame) -> dict:
    """Train Model C and save artifact. Returns metrics dict."""
    log.info("Model C: training")

    feature_cols = [
        "n_authors",
        "n_bug_commits",
        "avg_ncloc",
        "avg_complexity",
        "avg_code_smells",
        "avg_sqale_index",
        "project_age_months",
    ]

    train_mask = df["PROJECT_ID"] != HOLDOUT_PROJECT
    test_mask = df["PROJECT_ID"] == HOLDOUT_PROJECT
    log.info(f"Model C: train rows={train_mask.sum():,}, test rows={test_mask.sum():,}")

    if test_mask.sum() < 5:
        log.warning(
            f"Model C: holdout project '{HOLDOUT_PROJECT}' has only "
            f"{test_mask.sum()} project-months. Falling back to 20% random holdout."
        )
        rng = np.random.default_rng(42)
        all_idx = np.arange(len(df))
        rng.shuffle(all_idx)
        cutoff = int(len(df) * 0.8)
        train_idx = all_idx[:cutoff]
        test_idx = all_idx[cutoff:]
        train_mask = pd.Series(False, index=df.index)
        test_mask = pd.Series(False, index=df.index)
        train_mask.iloc[train_idx] = True
        test_mask.iloc[test_idx] = True

    X_train = df.loc[train_mask, feature_cols].astype(float).values
    X_test = df.loc[test_mask, feature_cols].astype(float).values
    y_train = np.log1p(df.loc[train_mask, "velocity"].values)
    y_test_orig = df.loc[test_mask, "velocity"].values
    y_test = np.log1p(y_test_orig)

    model = xgb.XGBRegressor(**XGB_PARAMS)
    model.fit(X_train, y_train)

    pred_log = model.predict(X_test)
    pred_orig = np.expm1(pred_log).clip(min=0)

    metrics = {
        "r2_log": float(r2_score(y_test, pred_log)),
        "mae_log": float(mean_absolute_error(y_test, pred_log)),
        "rmse_log": float(np.sqrt(mean_squared_error(y_test, pred_log))),
        "mae_velocity": float(mean_absolute_error(y_test_orig, pred_orig)),
        "rmse_velocity": float(np.sqrt(mean_squared_error(y_test_orig, pred_orig))),
        "test_n": int(test_mask.sum()),
        "train_n": int(train_mask.sum()),
    }
    log.info(f"Model C holdout metrics: {metrics}")

    artifact = {
        "model": model,
        "feature_names": feature_cols,
        "holdout_metrics": metrics,
        "target_transform": "log1p",
        "training_metadata": {
            "trained_at": datetime.now(timezone.utc).isoformat(),
            "holdout_project": HOLDOUT_PROJECT,
            "n_train_months": int(train_mask.sum()),
            "n_test_months": int(test_mask.sum()),
            "xgb_params": XGB_PARAMS,
        },
    }
    out = OUT_DIR / "velocity_regressor.pkl"
    with open(out, "wb") as fh:
        pickle.dump(artifact, fh)
    log.info(f"Model C: saved to {out}")
    return metrics


# =====================================================================
# Main
# =====================================================================
def main() -> None:
    if not DB_PATH.exists():
        raise FileNotFoundError(
            f"TD dataset not found at {DB_PATH}. "
            f"Run the API notebook's Section 8 to download it first."
        )
    log.info(f"Connecting to {DB_PATH}")
    conn = sqlite3.connect(DB_PATH)

    log.info("=" * 70)
    log.info("MODEL A: Defect density per file")
    log.info("=" * 70)
    df_a = build_defect_density_dataset(conn)
    metrics_a = train_defect_density_model(df_a)

    log.info("=" * 70)
    log.info("MODEL B: Issue resolution time")
    log.info("=" * 70)
    df_b = build_resolution_time_dataset(conn)
    metrics_b = train_resolution_time_model(df_b)

    log.info("=" * 70)
    log.info("MODEL C: Team velocity")
    log.info("=" * 70)
    df_c = build_velocity_dataset(conn)
    metrics_c = train_velocity_model(df_c)

    conn.close()

    log.info("=" * 70)
    log.info("TRAINING COMPLETE")
    log.info("=" * 70)
    log.info(f"Defect density: R² log={metrics_a['r2_log']:.3f}, MAE bugs={metrics_a['mae_bugs']:.2f}")
    log.info(f"Resolution time: R² log={metrics_b['r2_log']:.3f}, MAE hours={metrics_b['mae_hours']:.2f}")
    log.info(f"Velocity:        R² log={metrics_c['r2_log']:.3f}, MAE velocity={metrics_c['mae_velocity']:.2f}")
    log.info(f"Three pickles saved to {OUT_DIR}")


if __name__ == "__main__":
    main()