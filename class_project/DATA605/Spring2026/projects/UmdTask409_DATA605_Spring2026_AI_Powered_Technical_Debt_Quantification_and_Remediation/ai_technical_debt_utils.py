"""
AI-Powered Technical Debt Quantification and Remediation
=========================================================
Utility functions for the DATA605 Spring 2026 project.

This module provides all reusable logic for loading, processing, and
analyzing technical debt data from the Technical Debt Dataset (Lenarduzzi
et al., 2019). It supports the full pipeline: data ingestion, feature
engineering, debt classification, impact prediction, prioritization,
and LLM-based remediation.

References:
    - Lenarduzzi, Saarimaki, Taibi (2019). "The Technical Debt Dataset."
      PROMISE'19. https://github.com/clowee/The-Technical-Debt-Dataset
    - Tornhill, Borg, Hagatulah, Soderberg (2025). "ACE: Automated
      Technical Debt Remediation with Validated LLM Refactorings." FSE 2025.
"""

import logging
import sqlite3
from pathlib import Path
from typing import Optional

import numpy as np
import pandas as pd

# =============================================================================
# Logging
# =============================================================================
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# =============================================================================
# SECTION 1: DATABASE CONNECTION
# =============================================================================

def connect_to_database(db_path: str) -> sqlite3.Connection:
    """
    Open a connection to the Technical Debt Dataset SQLite database.

    Parameters
    ----------
    db_path : str
        Path to the .db file (e.g., "path/to/td_V2.db").

    Returns
    -------
    sqlite3.Connection
        A connection object that can be passed to all query functions.

    Raises
    ------
    FileNotFoundError
        If the database file does not exist at the given path.

    Example
    -------
    >>> conn = connect_to_database("/path/to/td_V2.db")
    >>> projects = get_projects(conn)
    >>> conn.close()
    """
    path = Path(db_path)
    if not path.exists():
        raise FileNotFoundError(
            f"Database not found at {db_path}. "
            "Download it from: "
            "https://github.com/clowee/The-Technical-Debt-Dataset/releases"
        )
    logger.info("Connecting to database: %s", db_path)
    conn = sqlite3.connect(db_path)
    return conn


# =============================================================================
# SECTION 2: DATA LOADING FUNCTIONS
# =============================================================================

def get_projects(conn: sqlite3.Connection) -> pd.DataFrame:
    """
    Get the list of all projects in the dataset.

    Parameters
    ----------
    conn : sqlite3.Connection
        Database connection from connect_to_database().

    Returns
    -------
    pd.DataFrame
        Columns: PROJECT_KEY, GIT_LINK, JIRA_LINK, SONAR_PROJECT_KEY,
        PROJECT_ID.
    """
    query = "SELECT * FROM PROJECTS"
    df = pd.read_sql_query(query, conn)
    logger.info("Loaded %d projects", len(df))
    return df


def get_sonar_measures(
    conn: sqlite3.Connection,
    project_id: Optional[str] = None,
) -> pd.DataFrame:
    """
    Get SonarQube code metrics (complexity, coverage, duplication, etc.).

    Each row is one analysis snapshot for one commit. The ANALYSIS_KEY
    links to the SONAR_ANALYSIS table, which maps to Git commit hashes.

    Parameters
    ----------
    conn : sqlite3.Connection
        Database connection.
    project_id : str, optional
        Filter by project. If None, returns data for all projects.

    Returns
    -------
    pd.DataFrame
        Code metrics per analysis snapshot. Key columns include:
        COMPLEXITY, COGNITIVE_COMPLEXITY, COVERAGE, NCLOC,
        DUPLICATED_LINES_DENSITY, and many others.
    """
    query = "SELECT * FROM SONAR_MEASURES"
    if project_id:
        query += f" WHERE PROJECT_ID = '{project_id}'"
    df = pd.read_sql_query(query, conn)
    logger.info(
        "Loaded %d SONAR_MEASURES rows%s",
        len(df),
        f" for project {project_id}" if project_id else "",
    )
    return df


def get_sonar_issues(
    conn: sqlite3.Connection,
    project_id: Optional[str] = None,
) -> pd.DataFrame:
    """
    Get all SonarQube issues (bugs, code smells, vulnerabilities).

    Each row is one detected issue with its type, severity, rule,
    component (file), line numbers, creation date, and remediation effort.

    Parameters
    ----------
    conn : sqlite3.Connection
        Database connection.
    project_id : str, optional
        Filter by project. If None, returns data for all projects.

    Returns
    -------
    pd.DataFrame
        Issue records. Key columns: TYPE (BUG/CODE_SMELL/VULNERABILITY),
        SEVERITY (BLOCKER/CRITICAL/MAJOR/MINOR/INFO), EFFORT, DEBT.
    """
    query = "SELECT * FROM SONAR_ISSUES"
    if project_id:
        query += f" WHERE PROJECT_ID = '{project_id}'"
    df = pd.read_sql_query(query, conn)
    logger.info(
        "Loaded %d SONAR_ISSUES rows%s",
        len(df),
        f" for project {project_id}" if project_id else "",
    )
    return df


def get_fault_inducing_commits(
    conn: sqlite3.Connection,
    project_id: Optional[str] = None,
) -> pd.DataFrame:
    """
    Get the SZZ fault-inducing commit data.

    Each row links a Jira fault to the commit that introduced it
    and the commit that fixed it. This is the ground truth for
    the impact prediction model.

    Parameters
    ----------
    conn : sqlite3.Connection
        Database connection.
    project_id : str, optional
        Filter by project. If None, returns data for all projects.

    Returns
    -------
    pd.DataFrame
        Columns: PROJECT_ID, FAULT_FIXING_COMMIT_HASH,
        FAULT_INDUCING_COMMIT_HASH.
    """
    query = "SELECT * FROM SZZ_FAULT_INDUCING_COMMITS"
    if project_id:
        query += f" WHERE PROJECT_ID = '{project_id}'"
    df = pd.read_sql_query(query, conn)
    logger.info(
        "Loaded %d fault-inducing commit records%s",
        len(df),
        f" for project {project_id}" if project_id else "",
    )
    return df


def get_refactorings(
    conn: sqlite3.Connection,
    project_id: Optional[str] = None,
) -> pd.DataFrame:
    """
    Get refactoring operations detected by Refactoring Miner.

    Each row is one refactoring with its type (e.g., Extract Method,
    Rename Class) and detailed description of what was changed.

    Parameters
    ----------
    conn : sqlite3.Connection
        Database connection.
    project_id : str, optional
        Filter by project. If None, returns data for all projects.

    Returns
    -------
    pd.DataFrame
        Columns: COMMIT_HASH, PROJECT_ID, REFACTORING_TYPE,
        REFACTORING_DETAIL.
    """
    query = "SELECT * FROM REFACTORING_MINER"
    if project_id:
        query += f" WHERE PROJECT_ID = '{project_id}'"
    df = pd.read_sql_query(query, conn)
    logger.info(
        "Loaded %d refactoring records%s",
        len(df),
        f" for project {project_id}" if project_id else "",
    )
    return df


def get_git_commits(
    conn: sqlite3.Connection,
    project_id: Optional[str] = None,
) -> pd.DataFrame:
    """
    Get Git commit metadata (messages, authors, dates).

    Parameters
    ----------
    conn : sqlite3.Connection
        Database connection.
    project_id : str, optional
        Filter by project. If None, returns data for all projects.

    Returns
    -------
    pd.DataFrame
        Columns include: COMMIT_HASH, COMMIT_MESSAGE, AUTHOR,
        AUTHOR_DATE, COMMITTER_DATE, and others.
    """
    query = "SELECT * FROM GIT_COMMITS"
    if project_id:
        query += f" WHERE PROJECT_ID = '{project_id}'"
    df = pd.read_sql_query(query, conn)
    logger.info(
        "Loaded %d commit records%s",
        len(df),
        f" for project {project_id}" if project_id else "",
    )
    return df


def get_sonar_analysis(
    conn: sqlite3.Connection,
    project_id: Optional[str] = None,
) -> pd.DataFrame:
    """
    Get the SonarQube analysis-to-commit mapping (V2 specific).

    This table bridges SONAR_MEASURES/SONAR_ISSUES (which use
    ANALYSIS_KEY) to GIT_COMMITS (which use COMMIT_HASH). The
    REVISION column in this table is the Git commit hash.

    Parameters
    ----------
    conn : sqlite3.Connection
        Database connection.
    project_id : str, optional
        Filter by project. If None, returns data for all projects.

    Returns
    -------
    pd.DataFrame
        Columns: PROJECT_ID, ANALYSIS_KEY, DATE, REVISION.
    """
    query = "SELECT * FROM SONAR_ANALYSIS"
    if project_id:
        query += f" WHERE PROJECT_ID = '{project_id}'"
    df = pd.read_sql_query(query, conn)
    logger.info(
        "Loaded %d analysis records%s",
        len(df),
        f" for project {project_id}" if project_id else "",
    )
    return df


def get_jira_issues(
    conn: sqlite3.Connection,
    project_id: Optional[str] = None,
) -> pd.DataFrame:
    """
    Get Jira issue tracker data (bug reports, feature requests).

    Parameters
    ----------
    conn : sqlite3.Connection
        Database connection.
    project_id : str, optional
        Filter by project. If None, returns data for all projects.

    Returns
    -------
    pd.DataFrame
        Columns include: KEY, PROJECT_ID, PRIORITY, TYPE, STATUS,
        RESOLUTION, REPORTER, CREATOR_NAME, ASSIGNEE, and others.
    """
    query = "SELECT * FROM JIRA_ISSUES"
    if project_id:
        query += f" WHERE PROJECT_ID = '{project_id}'"
    df = pd.read_sql_query(query, conn)
    logger.info(
        "Loaded %d Jira issues%s",
        len(df),
        f" for project {project_id}" if project_id else "",
    )
    return df


def get_dataset_summary(conn: sqlite3.Connection) -> pd.DataFrame:
    """
    Get a quick summary of all table row counts in the dataset.

    Useful for the introduction section of notebooks to describe
    the dataset at a glance.

    Returns
    -------
    pd.DataFrame
        Two columns: TABLE_NAME and ROW_COUNT.
    """
    tables = [
        "GIT_COMMITS",
        "GIT_COMMITS_CHANGES",
        "SONAR_MEASURES",
        "SONAR_ISSUES",
        "SONAR_ANALYSIS",
        "SONAR_RULES",
        "REFACTORING_MINER",
        "JIRA_ISSUES",
        "SZZ_FAULT_INDUCING_COMMITS",
        "PROJECTS",
    ]
    rows = []
    for table in tables:
        count = pd.read_sql_query(
            f"SELECT COUNT(*) as cnt FROM {table}", conn
        ).iloc[0]["cnt"]
        rows.append({"TABLE_NAME": table, "ROW_COUNT": count})
    summary = pd.DataFrame(rows)
    logger.info("Dataset summary:\n%s", summary.to_string(index=False))
    return summary


# =============================================================================
# SECTION 3: FEATURE ENGINEERING
# =============================================================================

def build_commit_features(
    conn: sqlite3.Connection,
    project_id: str,
) -> pd.DataFrame:
    """
    Build a per-commit feature matrix by joining SONAR_MEASURES with
    SONAR_ANALYSIS to get the commit hash, then labeling each commit
    as fault-inducing or not using SZZ_FAULT_INDUCING_COMMITS.

    This is the core training data for the impact prediction model.

    Parameters
    ----------
    conn : sqlite3.Connection
        Database connection.
    project_id : str
        The project to build features for.

    Returns
    -------
    pd.DataFrame
        One row per analyzed commit with columns:
        - All SONAR_MEASURES metrics (COMPLEXITY, COVERAGE, etc.)
        - COMMIT_HASH (from SONAR_ANALYSIS.REVISION)
        - IS_FAULT_INDUCING (1 if the commit introduced a bug, 0 otherwise)
    """
    # Step 1: Get measures and link to commit hashes via SONAR_ANALYSIS.
    query_measures = """
        SELECT
            sm.*,
            sa.REVISION as COMMIT_HASH,
            sa.DATE as ANALYSIS_DATE
        FROM SONAR_MEASURES sm
        JOIN SONAR_ANALYSIS sa
            ON sm.ANALYSIS_KEY = sa.ANALYSIS_KEY
            AND sm.PROJECT_ID = sa.PROJECT_ID
        WHERE sm.PROJECT_ID = ?
    """
    measures = pd.read_sql_query(query_measures, conn, params=[project_id])
    logger.info(
        "Project %s: %d commits with metrics", project_id, len(measures)
    )
    if measures.empty:
        logger.warning("No measures found for project %s", project_id)
        return measures

    # Step 2: Get the set of fault-inducing commit hashes for this project.
    fault_commits = get_fault_inducing_commits(conn, project_id)
    fault_hashes = set(fault_commits["FAULT_INDUCING_COMMIT_HASH"].unique())
    logger.info(
        "Project %s: %d unique fault-inducing commits",
        project_id,
        len(fault_hashes),
    )

    # Step 3: Label each commit.
    measures["IS_FAULT_INDUCING"] = measures["COMMIT_HASH"].isin(
        fault_hashes
    ).astype(int)
    fault_count = measures["IS_FAULT_INDUCING"].sum()
    logger.info(
        "Project %s: %d / %d commits are fault-inducing (%.1f%%)",
        project_id,
        fault_count,
        len(measures),
        100 * fault_count / len(measures) if len(measures) > 0 else 0,
    )
    return measures


def build_issue_counts_per_commit(
    conn: sqlite3.Connection,
    project_id: str,
) -> pd.DataFrame:
    """
    Count the number of SonarQube issues by type and severity for each
    analyzed commit. This produces features like "how many BUGs were
    present at this commit" or "how many CRITICAL issues existed."

    Parameters
    ----------
    conn : sqlite3.Connection
        Database connection.
    project_id : str
        The project to aggregate for.

    Returns
    -------
    pd.DataFrame
        One row per commit with columns for each issue type count
        and severity count, plus total issue count.
    """
    query = """
        SELECT
            sa.REVISION as COMMIT_HASH,
            si.TYPE,
            si.SEVERITY,
            COUNT(*) as ISSUE_COUNT
        FROM SONAR_ISSUES si
        JOIN SONAR_ANALYSIS sa
            ON si.CREATION_ANALYSIS_KEY = sa.ANALYSIS_KEY
            AND si.PROJECT_ID = sa.PROJECT_ID
        WHERE si.PROJECT_ID = ?
        GROUP BY sa.REVISION, si.TYPE, si.SEVERITY
    """
    raw = pd.read_sql_query(query, conn, params=[project_id])
    if raw.empty:
        logger.warning("No issues found for project %s", project_id)
        return pd.DataFrame()

    # Pivot by TYPE.
    type_counts = (
        raw.groupby(["COMMIT_HASH", "TYPE"])["ISSUE_COUNT"]
        .sum()
        .unstack(fill_value=0)
        .add_prefix("COUNT_")
    )
    # Pivot by SEVERITY.
    severity_counts = (
        raw.groupby(["COMMIT_HASH", "SEVERITY"])["ISSUE_COUNT"]
        .sum()
        .unstack(fill_value=0)
        .add_prefix("COUNT_SEV_")
    )
    # Total issues per commit.
    total = raw.groupby("COMMIT_HASH")["ISSUE_COUNT"].sum()
    total.name = "TOTAL_ISSUES"

    # Combine all.
    result = pd.concat([type_counts, severity_counts, total], axis=1)
    result = result.reset_index()
    logger.info(
        "Project %s: issue counts for %d commits", project_id, len(result)
    )
    return result


def build_full_feature_matrix(
    conn: sqlite3.Connection,
    project_id: str,
) -> pd.DataFrame:
    """
    Build the complete feature matrix for one project by combining:
    1. SONAR_MEASURES metrics (complexity, coverage, duplication)
    2. Issue counts by type and severity
    3. Fault-inducing label from SZZ

    This is the main function called by the Example notebook to
    prepare training data for the ML models.

    Parameters
    ----------
    conn : sqlite3.Connection
        Database connection.
    project_id : str
        The project to build features for.

    Returns
    -------
    pd.DataFrame
        One row per commit with all features and the target label.
    """
    # Get commit-level metrics with fault label.
    commit_features = build_commit_features(conn, project_id)
    if commit_features.empty:
        return commit_features

    # Get issue counts per commit.
    issue_counts = build_issue_counts_per_commit(conn, project_id)

    if issue_counts.empty:
        # No issue data, return just the metrics.
        return commit_features

    # Merge on COMMIT_HASH.
    merged = commit_features.merge(
        issue_counts,
        on="COMMIT_HASH",
        how="left",
    )
    # Fill NaN issue counts with 0 (commits with no issues).
    issue_cols = [c for c in merged.columns if c.startswith("COUNT_")]
    if "TOTAL_ISSUES" in merged.columns:
        issue_cols.append("TOTAL_ISSUES")
    merged[issue_cols] = merged[issue_cols].fillna(0)

    logger.info(
        "Project %s: full feature matrix has %d rows and %d columns",
        project_id,
        len(merged),
        len(merged.columns),
    )
    return merged


def build_multi_project_features(
    conn: sqlite3.Connection,
    project_ids: list,
) -> pd.DataFrame:
    """
    Build feature matrices for multiple projects and combine them.

    Parameters
    ----------
    conn : sqlite3.Connection
        Database connection.
    project_ids : list of str
        List of PROJECT_ID values to include.

    Returns
    -------
    pd.DataFrame
        Combined feature matrix with a PROJECT_ID column to identify
        which project each row belongs to.
    """
    frames = []
    for pid in project_ids:
        logger.info("Building features for project: %s", pid)
        df = build_full_feature_matrix(conn, pid)
        if not df.empty:
            frames.append(df)
    if not frames:
        logger.warning("No data found for any of the specified projects")
        return pd.DataFrame()
    combined = pd.concat(frames, ignore_index=True)
    logger.info(
        "Combined feature matrix: %d rows across %d projects",
        len(combined),
        len(frames),
    )
    return combined


# =============================================================================
# SECTION 4: MULTI-PROJECT ML MODELING
# =============================================================================
#
# Trains machine learning models across all 31 projects in the Technical Debt
# Dataset. The target project (commons-io) is held out from training so the
# models are evaluated on unseen project data, matching the "integrated
# pipeline on one project" structure of the Example notebook.

# Code metrics we use as features for classification.
# These come from SONAR_MEASURES and describe the commit where each issue was
# detected. We deliberately exclude distribution columns (which are verbose
# text blobs) and columns dominated by zeros across the dataset.
DEBT_CLASSIFIER_METRIC_COLUMNS = [
    "COMPLEXITY",
    "FILE_COMPLEXITY",
    "CLASS_COMPLEXITY",
    "FUNCTION_COMPLEXITY",
    "COMPLEXITY_IN_CLASSES",
    "COMPLEXITY_IN_FUNCTIONS",
    "COGNITIVE_COMPLEXITY",
    "NCLOC",
    "LINES",
    "STATEMENTS",
    "FUNCTIONS",
    "CLASSES",
    "FILES",
    "COMMENT_LINES",
    "COMMENT_LINES_DENSITY",
    "DUPLICATED_LINES",
    "DUPLICATED_LINES_DENSITY",
    "DUPLICATED_BLOCKS",
    "DUPLICATED_FILES",
]

# Issue-level features we use alongside the commit metrics.
# SEVERITY and EFFORT carry information about how SonarQube triaged the issue.
DEBT_CLASSIFIER_ISSUE_COLUMNS = [
    "SEVERITY",
    "EFFORT",
    "DEBT",
]

# Map textual severity to a numeric scale for the model.
SEVERITY_TO_NUMERIC = {
    "BLOCKER": 5,
    "CRITICAL": 4,
    "MAJOR": 3,
    "MINOR": 2,
    "INFO": 1,
}

# Default project to hold out during training. The pipeline demo in the
# Example notebook classifies, predicts, prioritizes, and refactors issues
# from this project using models trained on the other 30.
DEFAULT_TARGET_PROJECT = "org.apache:commons-io"

# Cap per project when sampling. Prevents the largest projects (Hive alone
# has 509K issues) from dominating the training signal.
DEFAULT_ISSUES_PER_PROJECT_CAP = 10000


# -----------------------------------------------------------------------------
# Data builder for multi-project debt-type classification
# -----------------------------------------------------------------------------

def build_multi_project_issue_classification_data(
    conn: sqlite3.Connection,
    project_ids: list[str],
    issues_per_project_cap: int = DEFAULT_ISSUES_PER_PROJECT_CAP,
    random_state: int = 42,
) -> pd.DataFrame:
    """
    Build the training matrix for debt-type classification across projects.

    For each project in ``project_ids``, joins SONAR_ISSUES with SONAR_MEASURES
    through CREATION_ANALYSIS_KEY, samples up to ``issues_per_project_cap``
    issues (stratified by TYPE to preserve minority classes), and concatenates
    into one dataframe.

    Parameters
    ----------
    conn : sqlite3.Connection
        Open connection to the Technical Debt Dataset V2 database.
    project_ids : list[str]
        List of PROJECT_ID values to include (e.g. ``["org.apache:hive", ...]``).
    issues_per_project_cap : int
        Maximum number of issues to sample per project. Prevents large projects
        from dominating the training signal.
    random_state : int
        Seed for reproducible sampling.

    Returns
    -------
    pd.DataFrame
        One row per issue with code metrics, issue metadata, and the TYPE
        target. Includes a ``PROJECT_ID`` column for auditing.
    """
    metric_cols_sql = ", ".join(
        [f"sm.{c} AS {c}" for c in DEBT_CLASSIFIER_METRIC_COLUMNS]
    )
    issue_cols_sql = ", ".join(
        [f"si.{c} AS {c}" for c in DEBT_CLASSIFIER_ISSUE_COLUMNS]
    )

    per_project_frames = []
    for project_id in project_ids:
        query = f"""
        SELECT
            si.PROJECT_ID AS PROJECT_ID,
            si.TYPE AS TYPE,
            {issue_cols_sql},
            {metric_cols_sql}
        FROM SONAR_ISSUES si
        JOIN SONAR_MEASURES sm
            ON si.CREATION_ANALYSIS_KEY = sm.ANALYSIS_KEY
           AND si.PROJECT_ID = sm.PROJECT_ID
        WHERE si.PROJECT_ID = ?
          AND si.TYPE IN ('BUG', 'CODE_SMELL', 'VULNERABILITY')
          AND si.TYPE IS NOT NULL
        """
        project_df = pd.read_sql(query, conn, params=(project_id,))

        if project_df.empty:
            logger.warning(
                "No joined rows for project %s, skipping", project_id
            )
            continue

        # Sample down to the cap, stratified by TYPE so minority classes
        # are preserved proportionally. If a project has fewer rows than
        # the cap, we keep all of them.
        if len(project_df) > issues_per_project_cap:
            total_rows = len(project_df)
            sampled_parts = []
            for type_value, group in project_df.groupby("TYPE"):
                target_n = max(
                    1,
                    int(issues_per_project_cap * len(group) / total_rows),
                )
                n_to_sample = min(len(group), target_n)
                sampled_parts.append(
                    group.sample(n=n_to_sample, random_state=random_state)
                )
            project_df = pd.concat(sampled_parts, ignore_index=True)

        per_project_frames.append(project_df)
        logger.info(
            "Project %s: %d issues sampled",
            project_id,
            len(project_df),
        )

    if not per_project_frames:
        raise ValueError(
            "No data assembled. Check that the project IDs exist and that "
            "SONAR_ISSUES has matching SONAR_MEASURES rows."
        )

    combined = pd.concat(per_project_frames, ignore_index=True)
    # Drop any rows where TYPE is null or didn't match our filter.
    # Belt-and-suspenders with the SQL WHERE clause.
    combined = combined[
        combined["TYPE"].isin(["BUG", "CODE_SMELL", "VULNERABILITY"])
    ].reset_index(drop=True)


    # Convert severity strings to numeric.
    combined["SEVERITY_NUM"] = (
        combined["SEVERITY"].map(SEVERITY_TO_NUMERIC).fillna(0)
    )
    combined = combined.drop(columns=["SEVERITY"])

    # Force numeric dtype on everything that should be numeric.
    # Empty strings in some TEXT-stored columns become NaN, then 0.
    numeric_cols = [
        c for c in combined.columns
        if c not in ("PROJECT_ID", "TYPE")
    ]
    for c in numeric_cols:
        combined[c] = pd.to_numeric(combined[c], errors="coerce").fillna(0)

    logger.info(
        "Assembled classification dataset: %d rows across %d projects",
        len(combined),
        combined["PROJECT_ID"].nunique(),
    )
    logger.info(
        "TYPE distribution: %s",
        combined["TYPE"].value_counts().to_dict(),
    )

    return combined


# -----------------------------------------------------------------------------
# Trainer for debt-type classification
# -----------------------------------------------------------------------------

def train_debt_type_classifier(
    training_data: pd.DataFrame,
    test_size: float = 0.2,
    random_state: int = 42,
) -> dict:
    """
    Train an XGBoost classifier to predict debt TYPE from code metrics
    and issue metadata.

    Parameters
    ----------
    training_data : pd.DataFrame
        Output of ``build_multi_project_issue_classification_data``.
    test_size : float
        Fraction of the data used for held-out evaluation.
    random_state : int
        Seed for reproducible splits and training.

    Returns
    -------
    dict
        Keys: ``model``, ``label_encoder``, ``feature_names``,
        ``metrics`` (F1 and precision per class, plus macro averages),
        ``classification_report`` (string), ``X_test``, ``y_test``.
    """
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import LabelEncoder
    from sklearn.metrics import (
        classification_report,
        f1_score,
        precision_score,
    )
    from xgboost import XGBClassifier

    # Drop non-feature columns.
    feature_names = [
        c for c in training_data.columns
        if c not in ("PROJECT_ID", "TYPE")
    ]
    X = training_data[feature_names]
    y = training_data["TYPE"]

    # Encode TYPE to integers for XGBoost.
    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y)

    # Stratified split to keep class proportions in both halves.
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y_encoded,
        test_size=test_size,
        random_state=random_state,
        stratify=y_encoded,
    )

    model = XGBClassifier(
        n_estimators=100,
        max_depth=5,
        learning_rate=0.1,
        random_state=random_state,
        eval_metric="mlogloss",
        tree_method="hist",
    )
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    class_names = [str(c) for c in label_encoder.classes_]

    report_str = classification_report(
        y_test,
        y_pred,
        target_names=class_names,
        zero_division=0,
    )

    f1_per_class = f1_score(
        y_test, y_pred, average=None, zero_division=0
    )
    precision_per_class = precision_score(
        y_test, y_pred, average=None, zero_division=0
    )

    metrics = {
        "f1_per_class": dict(zip(class_names, f1_per_class.tolist())),
        "precision_per_class": dict(
            zip(class_names, precision_per_class.tolist())
        ),
        "f1_macro": float(f1_score(y_test, y_pred, average="macro")),
        "precision_macro": float(
            precision_score(
                y_test, y_pred, average="macro", zero_division=0
            )
        ),
    }

    logger.info("Trained debt-type classifier")
    logger.info("Classes: %s", class_names)
    logger.info("F1 (macro): %.3f", metrics["f1_macro"])
    logger.info("Precision (macro): %.3f", metrics["precision_macro"])

    return {
        "model": model,
        "label_encoder": label_encoder,
        "feature_names": feature_names,
        "metrics": metrics,
        "classification_report": report_str,
        "X_test": X_test,
        "y_test": y_test,
    }


# -----------------------------------------------------------------------------
# Data builder for multi-project fault-inducing commit prediction
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# Churn-based features and project-normalized fault prediction
# -----------------------------------------------------------------------------
# Research (Mockus & Votta 2000, Nagappan & Ball 2005) consistently shows
# that code-change metrics (churn) outperform snapshot metrics for fault
# prediction. We join GIT_COMMITS_CHANGES aggregates to each commit.
#
# Per-project standardization removes scale differences between projects,
# which helps the model generalize to held-out projects (Zimmermann et al.
# 2009 cross-project prediction challenge).

FAULT_PREDICTOR_CHURN_COLUMNS = [
    "files_changed",
    "lines_added",
    "lines_removed",
    "churn_total",
    "churn_ratio",
]


def build_multi_project_fault_prediction_data(
    conn: sqlite3.Connection,
    project_ids: list[str],
    commits_per_project_cap: int = DEFAULT_ISSUES_PER_PROJECT_CAP,
    random_state: int = 42,
) -> pd.DataFrame:
    """
    Build the training matrix for fault-inducing commit prediction.

    For each project, joins commit-level code metrics (SONAR_MEASURES)
    with churn aggregates (GIT_COMMITS_CHANGES) and labels each commit
    as fault-inducing if its hash appears in SZZ_FAULT_INDUCING_COMMITS.

    Returns
    -------
    pd.DataFrame
        One row per commit with snapshot metrics, churn features,
        PROJECT_ID, COMMIT_HASH, and the IS_FAULT_INDUCING target.
    """
    metric_cols_sql = ", ".join(
        [f"sm.{c} AS {c}" for c in DEBT_CLASSIFIER_METRIC_COLUMNS]
    )

    per_project_frames = []
    for project_id in project_ids:
        query = f"""
        SELECT DISTINCT
            sm.PROJECT_ID AS PROJECT_ID,
            sa.REVISION AS COMMIT_HASH,
            {metric_cols_sql},
            COALESCE(churn.files_changed, 0) AS files_changed,
            COALESCE(churn.lines_added, 0) AS lines_added,
            COALESCE(churn.lines_removed, 0) AS lines_removed,
            CASE
                WHEN szz.FAULT_INDUCING_COMMIT_HASH IS NOT NULL THEN 1
                ELSE 0
            END AS IS_FAULT_INDUCING
        FROM SONAR_MEASURES sm
        JOIN SONAR_ANALYSIS sa
            ON sm.ANALYSIS_KEY = sa.ANALYSIS_KEY
           AND sm.PROJECT_ID = sa.PROJECT_ID
        LEFT JOIN (
            SELECT
                PROJECT_ID,
                COMMIT_HASH,
                COUNT(*) AS files_changed,
                SUM(CAST(LINES_ADDED AS INTEGER)) AS lines_added,
                SUM(CAST(LINES_REMOVED AS INTEGER)) AS lines_removed
            FROM GIT_COMMITS_CHANGES
            GROUP BY PROJECT_ID, COMMIT_HASH
        ) churn
            ON sa.REVISION = churn.COMMIT_HASH
           AND sm.PROJECT_ID = churn.PROJECT_ID
        LEFT JOIN (
            SELECT DISTINCT PROJECT_ID, FAULT_INDUCING_COMMIT_HASH
            FROM SZZ_FAULT_INDUCING_COMMITS
        ) szz
            ON sa.REVISION = szz.FAULT_INDUCING_COMMIT_HASH
           AND sm.PROJECT_ID = szz.PROJECT_ID
        WHERE sm.PROJECT_ID = ?
        """
        
        project_df = pd.read_sql(query, conn, params=(project_id,))

        if project_df.empty:
            logger.warning(
                "No commits with metrics for project %s, skipping", project_id
            )
            continue

        # Derived churn features.
        project_df["churn_total"] = (
            project_df["lines_added"] + project_df["lines_removed"]
        )
        project_df["churn_ratio"] = project_df["lines_added"] / (
            project_df["churn_total"] + 1
        )

        # Sample down to cap, stratified by the target.
        if len(project_df) > commits_per_project_cap:
            total_rows = len(project_df)
            sampled_parts = []
            for fault_value, group in project_df.groupby("IS_FAULT_INDUCING"):
                target_n = max(
                    1,
                    int(commits_per_project_cap * len(group) / total_rows),
                )
                n_to_sample = min(len(group), target_n)
                sampled_parts.append(
                    group.sample(n=n_to_sample, random_state=random_state)
                )
            project_df = pd.concat(sampled_parts, ignore_index=True)

        fault_rate = project_df["IS_FAULT_INDUCING"].mean()
        per_project_frames.append(project_df)
        logger.info(
            "Project %s: %d commits sampled, %.1f%% fault-inducing",
            project_id,
            len(project_df),
            100 * fault_rate,
        )

    if not per_project_frames:
        raise ValueError(
            "No data assembled. Check project IDs and database joins."
        )

    combined = pd.concat(per_project_frames, ignore_index=True)

    non_numeric = {"PROJECT_ID", "COMMIT_HASH", "IS_FAULT_INDUCING"}
    for c in combined.columns:
        if c not in non_numeric:
            combined[c] = pd.to_numeric(combined[c], errors="coerce").fillna(0)

    logger.info(
        "Assembled fault-prediction dataset: %d commits across %d projects",
        len(combined),
        combined["PROJECT_ID"].nunique(),
    )
    logger.info(
        "Overall fault-inducing rate: %.1f%%",
        100 * combined["IS_FAULT_INDUCING"].mean(),
    )

    return combined


def _compute_project_normalization_stats(
    training_data: pd.DataFrame,
    feature_names: list[str],
) -> pd.DataFrame:
    """Per-project mean and std for each feature. Used by normalize_features."""
    stats = (
        training_data.groupby("PROJECT_ID")[feature_names]
        .agg(["mean", "std"])
    )
    return stats


def _normalize_features(
    data: pd.DataFrame,
    feature_names: list[str],
    stats: pd.DataFrame,
    fallback_to_global: bool = True,
) -> pd.DataFrame:
    """
    Subtract per-project mean and divide by per-project std.

    If a row's project is not in stats (e.g. a held-out project at inference
    time), fall back to global mean/std computed from the stats table itself.
    """
    # stats has a MultiIndex on columns: (feature_name, 'mean'|'std').
    # Extract the mean and std dataframes separately for simpler indexing.
    means_df = stats.xs("mean", level=1, axis=1)
    stds_df = stats.xs("std", level=1, axis=1).replace(0, 1)

    global_mean = means_df.mean()
    global_std = stds_df.mean().replace(0, 1)

    normalized_frames = []
    for project_id, group in data.groupby("PROJECT_ID"):
        if project_id in means_df.index:
            proj_mean = means_df.loc[project_id]
            proj_std = stds_df.loc[project_id]
        elif fallback_to_global:
            proj_mean = global_mean
            proj_std = global_std
        else:
            raise ValueError(
                f"Project {project_id} not in stats and fallback disabled"
            )

        normalized = group[feature_names].copy()
        for col in feature_names:
            normalized[col] = (normalized[col] - proj_mean[col]) / proj_std[col]

        keep_cols = [c for c in group.columns if c not in feature_names]
        normalized = pd.concat(
            [group[keep_cols].reset_index(drop=True),
             normalized.reset_index(drop=True)],
            axis=1,
        )
        normalized_frames.append(normalized)

    return pd.concat(normalized_frames, ignore_index=True)

def train_fault_inducing_predictor(
    training_data: pd.DataFrame,
    test_size: float = 0.2,
    random_state: int = 42,
    use_project_normalization: bool = False,
) -> dict:
    """
    Train an XGBoost binary classifier to predict fault-inducing commits.

    Parameters
    ----------
    use_project_normalization : bool
        If True, standardize features within each project before training.
        Helps with cross-project generalization. Default True.

    Returns
    -------
    dict
        Keys: model, feature_names, normalization_stats (or None),
        metrics, classification_report, X_test, y_test.
    """
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import (
        classification_report,
        f1_score,
        precision_score,
        recall_score,
        roc_auc_score,
        accuracy_score,
    )
    from xgboost import XGBClassifier

    feature_names = (
        DEBT_CLASSIFIER_METRIC_COLUMNS + FAULT_PREDICTOR_CHURN_COLUMNS
    )

    missing = [c for c in feature_names if c not in training_data.columns]
    if missing:
        raise ValueError(f"training_data missing columns: {missing}")

    normalization_stats = None
    if use_project_normalization:
        normalization_stats = _compute_project_normalization_stats(
            training_data, feature_names
        )
        training_data = _normalize_features(
            training_data, feature_names, normalization_stats
        )

    X = training_data[feature_names]
    y = training_data["IS_FAULT_INDUCING"].astype(int)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=test_size,
        random_state=random_state,
        stratify=y,
    )

    n_pos = int((y_train == 1).sum())
    n_neg = int((y_train == 0).sum())
    scale = max(1.0, n_neg / max(n_pos, 1))

    model = XGBClassifier(
        n_estimators=100,
        max_depth=5,
        learning_rate=0.1,
        random_state=random_state,
        eval_metric="logloss",
        scale_pos_weight=scale,
        tree_method="hist",
    )
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1]

    report_str = classification_report(
        y_test, y_pred,
        target_names=["Safe", "Fault-Inducing"],
        zero_division=0,
    )
    metrics = {
        "f1_positive": float(f1_score(y_test, y_pred, zero_division=0)),
        "precision_positive": float(
            precision_score(y_test, y_pred, zero_division=0)
        ),
        "recall_positive": float(
            recall_score(y_test, y_pred, zero_division=0)
        ),
        "auc": float(roc_auc_score(y_test, y_prob)),
        "accuracy": float(accuracy_score(y_test, y_pred)),
    }

    logger.info("Trained fault-inducing commit predictor")
    logger.info(
        "F1: %.3f | Precision: %.3f | Recall: %.3f | AUC: %.3f | Normalized: %s",
        metrics["f1_positive"],
        metrics["precision_positive"],
        metrics["recall_positive"],
        metrics["auc"],
        use_project_normalization,
    )

    return {
        "model": model,
        "feature_names": feature_names,
        "normalization_stats": normalization_stats,
        "metrics": metrics,
        "classification_report": report_str,
        "X_test": X_test,
        "y_test": y_test,
    }


def score_commits_for_fault_risk(
    model,
    feature_matrix: pd.DataFrame,
    feature_names: list[str],
    threshold: float = 0.5,
    normalization_stats: Optional[pd.DataFrame] = None,
) -> pd.DataFrame:
    """
    Score commits using a trained fault-inducing predictor.

    If ``normalization_stats`` is provided (from the training output),
    features will be standardized per project before scoring. This must
    match how the model was trained.
    """
    missing = [c for c in feature_names if c not in feature_matrix.columns]
    if missing:
        raise ValueError(
            f"feature_matrix is missing expected columns: {missing}"
        )

    data_to_score = feature_matrix
    if normalization_stats is not None:
        data_to_score = _normalize_features(
            feature_matrix, feature_names, normalization_stats
        )

    X = data_to_score[feature_names]
    probs = model.predict_proba(X)[:, 1]

    result = feature_matrix.copy()
    result["fault_probability"] = probs
    result["predicted_fault"] = (probs >= threshold).astype(int)

    logger.info(
        "Scored %d commits at threshold %.2f: %d flagged (%.1f%%)",
        len(result),
        threshold,
        int(result["predicted_fault"].sum()),
        100 * result["predicted_fault"].mean(),
    )

    return result