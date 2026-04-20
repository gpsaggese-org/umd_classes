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


# =============================================================================
# SECTION 5: PRIORITIZATION
# =============================================================================
#
# Given the open issues in a target project and a trained fault predictor,
# score each issue by its host commit's fault probability, combine with
# SonarQube's remediation effort estimate, and rank by impact/effort.
# Also compute the Pareto front for multi-objective reporting.


def build_open_issues_for_prioritization(
    conn: sqlite3.Connection,
    project_id: str,
) -> pd.DataFrame:
    """
    Load open issues from the target project joined to their host commit's
    code metrics and churn features. One row per open issue.

    Only issues with STATUS = 'OPEN' are returned, since closed issues
    don't need prioritization.

    Returns
    -------
    pd.DataFrame
        Columns: ISSUE_KEY, PROJECT_ID, COMMIT_HASH, TYPE, SEVERITY, EFFORT,
        DEBT, RULE, COMPONENT, START_LINE, plus all metric and churn
        features from Section 4b.
    """
    metric_cols_sql = ", ".join(
        [f"sm.{c} AS {c}" for c in DEBT_CLASSIFIER_METRIC_COLUMNS]
    )

    query = f"""
    SELECT
        si.ISSUE_KEY AS ISSUE_KEY,
        si.PROJECT_ID AS PROJECT_ID,
        sa.REVISION AS COMMIT_HASH,
        si.TYPE AS TYPE,
        si.SEVERITY AS SEVERITY,
        si.EFFORT AS EFFORT,
        si.DEBT AS DEBT,
        si.RULE AS RULE,
        si.COMPONENT AS COMPONENT,
        si.START_LINE AS START_LINE,
        si.MESSAGE AS MESSAGE,
        {metric_cols_sql},
        COALESCE(churn.files_changed, 0) AS files_changed,
        COALESCE(churn.lines_added, 0) AS lines_added,
        COALESCE(churn.lines_removed, 0) AS lines_removed
    FROM SONAR_ISSUES si
    JOIN SONAR_ANALYSIS sa
        ON si.CREATION_ANALYSIS_KEY = sa.ANALYSIS_KEY
       AND si.PROJECT_ID = sa.PROJECT_ID
    JOIN SONAR_MEASURES sm
        ON si.CREATION_ANALYSIS_KEY = sm.ANALYSIS_KEY
       AND si.PROJECT_ID = sm.PROJECT_ID
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
       AND si.PROJECT_ID = churn.PROJECT_ID
    WHERE si.PROJECT_ID = ?
      AND si.STATUS = 'OPEN'
      AND si.TYPE IN ('BUG', 'CODE_SMELL', 'VULNERABILITY')
    """
    df = pd.read_sql(query, conn, params=(project_id,))

    # Derived churn features to match Section 4b's feature set.
    df["churn_total"] = df["lines_added"] + df["lines_removed"]
    df["churn_ratio"] = df["lines_added"] / (df["churn_total"] + 1)

    # Force numeric types on metric columns.
    non_numeric = {
        "ISSUE_KEY", "PROJECT_ID", "COMMIT_HASH", "TYPE",
        "SEVERITY", "RULE", "COMPONENT", "MESSAGE",
    }
    for c in df.columns:
        if c not in non_numeric:
            df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0)

    logger.info(
        "Loaded %d open issues for prioritization from %s",
        len(df),
        project_id,
    )

    return df


def prioritize_issues(
    open_issues: pd.DataFrame,
    fault_model,
    fault_feature_names: list[str],
    min_effort_minutes: float = 1.0,
) -> pd.DataFrame:
    """
    Score and rank open issues by impact-over-effort ratio.

    Impact is the fault probability of the issue's host commit (from the
    trained predictor). Effort is SonarQube's remediation estimate, with
    a floor to prevent zero-effort issues from exploding the ratio.

    Returns
    -------
    pd.DataFrame
        Input frame with added columns: impact, effort_minutes,
        impact_over_effort, priority_rank.
        Sorted by priority_rank ascending (rank 1 = top priority).
    """
    missing = [c for c in fault_feature_names if c not in open_issues.columns]
    if missing:
        raise ValueError(
            f"open_issues missing features the model needs: {missing}"
        )

    probs = fault_model.predict_proba(open_issues[fault_feature_names])[:, 1]

    result = open_issues.copy()

    # Weight the host-commit fault probability by both the issue's severity
    # and its type. Severity uses an exponential scale (BLOCKER counts much
    # more than INFO, not just linearly). Type weights recognize that bugs
    # and vulnerabilities are functional/security concerns while code smells
    # are maintainability concerns.
    severity_weight_map = {
        "BLOCKER": 16.0,
        "CRITICAL": 8.0,
        "MAJOR": 4.0,
        "MINOR": 2.0,
        "INFO": 1.0,
    }
    type_weight_map = {
        "BUG": 1.5,
        "VULNERABILITY": 1.5,
        "CODE_SMELL": 1.0,
    }
    severity_weight = (
        result["SEVERITY"].map(severity_weight_map).fillna(1.0) / 16.0
    )
    type_weight = result["TYPE"].map(type_weight_map).fillna(1.0)

    result["impact"] = probs * severity_weight * type_weight
    result["effort_minutes"] = result["EFFORT"].clip(lower=min_effort_minutes)
    result["impact_over_effort"] = (
        result["impact"] / result["effort_minutes"]
    )
    # Short hash for readability in printouts; full hash stays in COMMIT_HASH.
    result["COMMIT_SHORT"] = result["COMMIT_HASH"].str[:8]

    result = result.sort_values(
        "impact_over_effort", ascending=False
    ).reset_index(drop=True)
    result["priority_rank"] = result["impact_over_effort"].rank(
        method="min", ascending=False
    ).astype(int)

    logger.info(
        "Ranked %d issues. Top issue: impact=%.3f effort=%.1f min ratio=%.4f",
        len(result),
        result.iloc[0]["impact"],
        result.iloc[0]["effort_minutes"],
        result.iloc[0]["impact_over_effort"],
    )

    return result


def compute_pareto_front(
    ranked_issues: pd.DataFrame,
    impact_col: str = "impact",
    effort_col: str = "effort_minutes",
) -> pd.DataFrame:
    """
    Compute the Pareto front on (high impact, low effort).

    An issue is on the Pareto front if no other issue has both higher
    impact AND lower-or-equal effort (or higher-or-equal impact AND
    strictly lower effort).

    Returns
    -------
    pd.DataFrame
        Subset of ranked_issues that lies on the Pareto front, sorted
        by effort ascending so the trade-off curve reads left-to-right.
    """
    if ranked_issues.empty:
        return ranked_issues.copy()

    # Sort by effort ascending, then impact descending. Walk through and
    # keep only issues whose impact exceeds the running maximum.
    sorted_df = ranked_issues.sort_values(
        by=[effort_col, impact_col],
        ascending=[True, False],
    ).reset_index(drop=True)

    pareto_rows = []
    max_impact_seen = -float("inf")
    for _, row in sorted_df.iterrows():
        if row[impact_col] > max_impact_seen:
            pareto_rows.append(row)
            max_impact_seen = row[impact_col]

    pareto_df = pd.DataFrame(pareto_rows).reset_index(drop=True)

    logger.info(
        "Pareto front: %d of %d issues are non-dominated",
        len(pareto_df),
        len(ranked_issues),
    )

    return pareto_df


# =============================================================================
# SECTION 7: BENCHMARK RESULTS LOADING
# =============================================================================
#
# Loads the JSON outputs from the Nexus sweep (5 models x 3 strategies x
# 1000 CodeXGLUE pairs) and organizes them into a leaderboard dataframe.
# Used by the Example notebook to present the model comparison that
# justifies the agent's model choice.

BENCHMARK_STRATEGIES = ["zero_shot", "few_shot_static", "few_shot_retrieval"]


def load_benchmark_results(results_dir: str) -> pd.DataFrame:
    """
    Load all 1000-pair benchmark JSONs from a directory and return them
    as a dataframe with one row per (model, strategy) configuration.

    Filename convention: ``<org>__<model>__<strategy>__1000pairs.json``

    Returns
    -------
    pd.DataFrame
        Columns: model, model_short, strategy, bleu, exact_match_rate,
        java_valid_rate, sec_per_pair, n_pairs, n_successful_runs.
    """
    import json

    path = Path(results_dir)
    if not path.exists():
        raise FileNotFoundError(f"Benchmark results directory not found: {path}")

    rows = []
    for fp in sorted(path.glob("*1000pairs*.json")):
        with open(fp) as f:
            data = json.load(f)
        cfg = data["config"]
        agg = data["aggregate"]
        rows.append({
            "model": cfg["model"],
            "model_short": cfg["model"].split("/")[-1],
            "strategy": cfg["strategy"],
            "bleu": agg["mean_bleu"],
            "exact_match_rate": agg["exact_match_rate"],
            "java_valid_rate": agg["java_valid_rate"],
            "sec_per_pair": agg["mean_elapsed_per_pair_s"],
            "n_pairs": agg["n_pairs"],
            "n_successful_runs": agg["n_successful_runs"],
        })

    if not rows:
        raise ValueError(f"No 1000-pair JSON files found in {path}")

    df = pd.DataFrame(rows)
    logger.info(
        "Loaded %d benchmark configurations from %s",
        len(df),
        results_dir,
    )
    return df


def build_leaderboard_table(benchmark_df: pd.DataFrame) -> pd.DataFrame:
    """
    Reshape the flat benchmark dataframe into a model-by-strategy grid
    of BLEU scores, with columns for each strategy and a rank column.

    Returns
    -------
    pd.DataFrame
        One row per model. Columns: zero_shot, few_shot_static,
        few_shot_retrieval (each containing BLEU), best_strategy,
        best_bleu, rank_by_best.
    """
    pivot = benchmark_df.pivot_table(
        index="model_short",
        columns="strategy",
        values="bleu",
    )

    # Reorder columns to the canonical strategy order.
    pivot = pivot[BENCHMARK_STRATEGIES]

    pivot["best_strategy"] = pivot[BENCHMARK_STRATEGIES].idxmax(axis=1)
    pivot["best_bleu"] = pivot[BENCHMARK_STRATEGIES].max(axis=1)
    pivot["rank_by_best"] = (
        pivot["best_bleu"].rank(ascending=False, method="min").astype(int)
    )

    pivot = pivot.sort_values("best_bleu", ascending=False)

    logger.info(
        "Leaderboard top config: %s with BLEU %.2f",
        pivot.index[0] + " + " + pivot.iloc[0]["best_strategy"],
        pivot.iloc[0]["best_bleu"],
    )

    return pivot


def summarize_benchmark_insights(benchmark_df: pd.DataFrame) -> dict:
    """
    Compute the headline findings from the benchmark.

    Returns
    -------
    dict
        Keys:
        - overall_winner: (model_short, strategy, bleu)
        - retrieval_beats_static: bool, True if retrieval > static for all models
        - static_beats_zeroshot: bool, True if static > zero-shot for all models
        - best_cpu_capable: (model_short, strategy, bleu) for the 0.5B model
        - worst_config: (model_short, strategy, bleu)
        - validity_outlier: model whose java_valid_rate is noticeably lower
    """
    df = benchmark_df.copy()

    # Overall winner by BLEU.
    best_row = df.loc[df["bleu"].idxmax()]
    overall_winner = (
        best_row["model_short"],
        best_row["strategy"],
        float(best_row["bleu"]),
    )

    # Retrieval vs static vs zero-shot, per model.
    retrieval_beats_static = True
    static_beats_zeroshot = True
    for model, group in df.groupby("model_short"):
        by_strat = group.set_index("strategy")["bleu"].to_dict()
        z = by_strat.get("zero_shot", float("nan"))
        s = by_strat.get("few_shot_static", float("nan"))
        r = by_strat.get("few_shot_retrieval", float("nan"))
        if not (r > s):
            retrieval_beats_static = False
        if not (s > z):
            static_beats_zeroshot = False

    # Best CPU-capable config (0.5B model).
    cpu_rows = df[df["model_short"].str.contains("0.5B", case=False)]
    if len(cpu_rows) > 0:
        cpu_best = cpu_rows.loc[cpu_rows["bleu"].idxmax()]
        best_cpu_capable = (
            cpu_best["model_short"],
            cpu_best["strategy"],
            float(cpu_best["bleu"]),
        )
    else:
        best_cpu_capable = None

    # Worst config.
    worst_row = df.loc[df["bleu"].idxmin()]
    worst_config = (
        worst_row["model_short"],
        worst_row["strategy"],
        float(worst_row["bleu"]),
    )

    # Validity outlier: any model whose mean validity is more than
    # 10 points below the others.
    validity_by_model = df.groupby("model_short")["java_valid_rate"].mean()
    median_validity = validity_by_model.median()
    validity_outlier = None
    for model, val in validity_by_model.items():
        if val < median_validity - 0.10:
            validity_outlier = (model, float(val))
            break

    insights = {
        "overall_winner": overall_winner,
        "retrieval_beats_static": retrieval_beats_static,
        "static_beats_zeroshot": static_beats_zeroshot,
        "best_cpu_capable": best_cpu_capable,
        "worst_config": worst_config,
        "validity_outlier": validity_outlier,
    }

    logger.info(
        "Benchmark insights: winner=%s, retrieval_dominates=%s, "
        "static_dominates=%s, cpu_best=%s",
        overall_winner,
        retrieval_beats_static,
        static_beats_zeroshot,
        best_cpu_capable,
    )

    return insights


# =============================================================================
# SECTION 4c: TECHNICAL DEBT FORECASTING (Time Series)
# =============================================================================
#
# Predicts the evolution of accumulated technical debt using ARIMA(0,1,1),
# following Tsoukalas et al. (2020) "Technical debt forecasting: An empirical
# study on open-source repositories" (Journal of Systems and Software).
#
# Target: cumulative remediation effort over time (SonarQube SQALE analog).
# Cumulative curves are smoother than raw weekly counts and are what the
# TD forecasting literature consistently uses.


def build_debt_timeseries(
    conn: sqlite3.Connection,
    project_id: str,
    frequency: str = "W",
) -> pd.DataFrame:
    """
    Build a cumulative-effort time series for one project.

    Parameters
    ----------
    conn : sqlite3.Connection
    project_id : str
    frequency : str
        "W" for weekly (default, matches Tsoukalas et al.) or "M" for monthly.

    Returns
    -------
    pd.DataFrame
        Columns: period_start (datetime), period_effort, cumulative_effort,
        n_issues, n_active_commits.
        Indexed by period_start.
    """
    if frequency not in ("W", "M"):
        raise ValueError(f"frequency must be 'W' or 'M', got {frequency!r}")

    # Pull raw per-issue data with creation date.
    q = """
    SELECT
        sa.DATE AS creation_date,
        CAST(si.EFFORT AS REAL) AS effort,
        sa.REVISION AS commit_hash
    FROM SONAR_ISSUES si
    JOIN SONAR_ANALYSIS sa
        ON si.CREATION_ANALYSIS_KEY = sa.ANALYSIS_KEY
       AND si.PROJECT_ID = sa.PROJECT_ID
    WHERE si.PROJECT_ID = ?
      AND si.EFFORT IS NOT NULL
    """
    raw = pd.read_sql(q, conn, params=(project_id,))
    if raw.empty:
        raise ValueError(f"No issues with effort data for {project_id}")

    raw["creation_date"] = pd.to_datetime(
        raw["creation_date"], errors="coerce"
    )
    raw = raw.dropna(subset=["creation_date"])
    raw["effort"] = raw["effort"].fillna(0)

    # Resample to the chosen frequency.
    raw = raw.set_index("creation_date").sort_index()
    period_effort = raw["effort"].resample(frequency).sum()
    n_issues = raw["effort"].resample(frequency).count()
    n_active_commits = (
        raw["commit_hash"].resample(frequency).nunique()
    )

    # Fill any completely missing periods with zero so the series is regular.
    full_index = pd.date_range(
        start=period_effort.index.min(),
        end=period_effort.index.max(),
        freq=frequency,
    )
    period_effort = period_effort.reindex(full_index, fill_value=0)
    n_issues = n_issues.reindex(full_index, fill_value=0)
    n_active_commits = n_active_commits.reindex(full_index, fill_value=0)

    df = pd.DataFrame({
        "period_effort": period_effort,
        "cumulative_effort": period_effort.cumsum(),
        "n_issues": n_issues.astype(int),
        "n_active_commits": n_active_commits.astype(int),
    })
    df.index.name = "period_start"

    logger.info(
        "Built %s time series for %s: %d periods, cumulative effort %.0f min",
        "weekly" if frequency == "W" else "monthly",
        project_id,
        len(df),
        df["cumulative_effort"].iloc[-1],
    )

    return df


def forecast_debt_arima(
    timeseries: pd.DataFrame,
    target_col: str = "cumulative_effort",
    train_fraction: float = 0.8,
    order: tuple = (0, 1, 1),
    auto_search: bool = False,
) -> dict:
    """
    Forecast technical debt evolution using ARIMA.

    Splits the series temporally (first ``train_fraction`` for training,
    remainder for evaluation), fits an ARIMA model on the train portion,
    forecasts the test portion, reports accuracy.

    Parameters
    ----------
    timeseries : pd.DataFrame
        Output of ``build_debt_timeseries``. Must have ``target_col``.
    target_col : str
        Which column to forecast. Defaults to ``cumulative_effort``.
    train_fraction : float
        Fraction of series used for training. Default 0.8.
    order : tuple
        ARIMA (p, d, q). Default (0, 1, 1) per Tsoukalas et al.
    auto_search : bool
        If True, use pmdarima.auto_arima to search for best parameters.
        Slower but often finds better fits. Default False.

    Returns
    -------
    dict
        Keys: train, test, predictions (pd.Series indexed by date),
        model, order_used, metrics (mape, rmse, mae), train_fraction.
    """
    import numpy as np
    from sklearn.metrics import mean_absolute_error, mean_squared_error

    if target_col not in timeseries.columns:
        raise ValueError(
            f"target_col {target_col!r} not in timeseries columns"
        )
    if len(timeseries) < 20:
        raise ValueError(
            f"Need at least 20 periods for reliable forecasting, "
            f"got {len(timeseries)}"
        )

    y = timeseries[target_col].astype(float)
    split_idx = int(len(y) * train_fraction)
    y_train = y.iloc[:split_idx]
    y_test = y.iloc[split_idx:]

    if auto_search:
        import pmdarima as pm
        model = pm.auto_arima(
            y_train,
            seasonal=False,
            suppress_warnings=True,
            error_action="ignore",
        )
        order_used = model.order
        forecast = model.predict(n_periods=len(y_test))
        predictions = pd.Series(forecast, index=y_test.index)
    else:
        from statsmodels.tsa.arima.model import ARIMA
        model = ARIMA(y_train, order=order).fit()
        order_used = order
        forecast = model.forecast(steps=len(y_test))
        predictions = pd.Series(forecast.values, index=y_test.index)

    # Metrics.
    mae = float(mean_absolute_error(y_test, predictions))
    rmse = float(np.sqrt(mean_squared_error(y_test, predictions)))
    # MAPE guards against zeros in the denominator.
    nonzero_mask = y_test != 0
    if nonzero_mask.any():
        mape = float(
            np.mean(
                np.abs(
                    (y_test[nonzero_mask] - predictions[nonzero_mask])
                    / y_test[nonzero_mask]
                )
            )
            * 100
        )
    else:
        mape = float("nan")

    logger.info(
        "Forecasted %s: train=%d test=%d periods. Order %s. "
        "MAPE=%.2f%% RMSE=%.1f MAE=%.1f",
        target_col,
        len(y_train),
        len(y_test),
        order_used,
        mape,
        rmse,
        mae,
    )

    return {
        "train": y_train,
        "test": y_test,
        "predictions": predictions,
        "model": model,
        "order_used": order_used,
        "metrics": {"mape": mape, "rmse": rmse, "mae": mae},
        "train_fraction": train_fraction,
    }



# =============================================================================
# SECTION 6: JAVA REFACTORING AGENT
# =============================================================================
#
# A model-agnostic refactoring agent for Java code. Takes a method as input,
# generates a refactored version using a local LLM, validates the output,
# and returns a confidence-scored result.
#
# Design based on benchmark results: Qwen-Coder-0.5B + few-shot retrieval is
# the recommended default (BLEU 67.78 on CodeXGLUE small test split), chosen
# for CPU-capable inference time (~100 sec/call on MacBook Air).
#
# The agent is language-agnostic in structure but uses Java-specific tools
# (javalang for parsing, CodeXGLUE as the retrieval corpus).


AGENT_DEFAULT_MODEL = "Qwen/Qwen2.5-Coder-0.5B-Instruct"
AGENT_DEFAULT_MAX_NEW_TOKENS = 512
AGENT_DEFAULT_SEED = 42
AGENT_DEFAULT_N_RETRIEVAL_EXAMPLES = 3
AGENT_CONFIDENCE_HIGH_BLEU_THRESHOLD = 50.0


def validate_java_syntax(code: str) -> dict:
    """
    Check whether a string parses as valid Java.

    CodeXGLUE methods are wrapped in a synthetic class for parsing since
    isolated methods are not valid top-level Java syntax.

    Returns
    -------
    dict with keys ``is_valid`` (bool) and ``error`` (str or None).
    """
    import javalang

    wrapped = f"class _AgentWrapper {{ {code} }}"
    try:
        javalang.parse.parse(wrapped)
        return {"is_valid": True, "error": None}
    except Exception as e:
        return {"is_valid": False, "error": str(e)[:200]}


def compute_bleu_against_reference(candidate: str, reference: str) -> float:
    """
    Compute sentence-level BLEU of the candidate against one reference.

    Uses sacrebleu, matching CodeXGLUE's evaluation convention. Returns a
    score in [0, 100].
    """
    import sacrebleu

    if not candidate or not reference:
        return 0.0
    try:
        bleu = sacrebleu.sentence_bleu(candidate, [reference])
        return float(bleu.score)
    except Exception:
        return 0.0


def is_exact_match(candidate: str, reference: str) -> bool:
    """
    Whitespace-normalized exact match between candidate and reference.

    This is the convention used by CodeXGLUE and the benchmark scripts.
    """
    if not candidate or not reference:
        return False
    # Collapse all whitespace runs to a single space before comparing.
    norm_c = " ".join(candidate.split())
    norm_r = " ".join(reference.split())
    return norm_c == norm_r


def compute_confidence_score(
    is_valid: bool,
    exact_match: bool,
    bleu_score: float,
    bleu_threshold: float = AGENT_CONFIDENCE_HIGH_BLEU_THRESHOLD,
) -> dict:
    """
    Derive a confidence score and label from validation results.

    Confidence tiers:
      - HIGH: valid Java AND (exact match OR BLEU >= threshold)
      - MEDIUM: valid Java AND BLEU in [threshold/2, threshold)
      - LOW: valid Java AND BLEU < threshold/2
      - FAILED: invalid Java

    Returns
    -------
    dict with ``level`` (str) and ``score`` (float in [0, 1]).
    """
    if not is_valid:
        return {"level": "FAILED", "score": 0.0}

    if exact_match or bleu_score >= bleu_threshold:
        return {"level": "HIGH", "score": 0.9 + 0.1 * min(bleu_score / 100, 1)}
    if bleu_score >= bleu_threshold / 2:
        return {"level": "MEDIUM", "score": 0.5 + 0.3 * (bleu_score - bleu_threshold / 2) / (bleu_threshold / 2)}
    return {"level": "LOW", "score": 0.2 + 0.3 * (bleu_score / (bleu_threshold / 2))}


# -----------------------------------------------------------------------------
# CodeXGLUE retrieval index: build, cache, query
# -----------------------------------------------------------------------------

AGENT_RETRIEVAL_CACHE_DIRNAME = "retrieval_cache"
AGENT_RETRIEVAL_SUBSET = "small"  # matches the benchmark run


def _retrieval_cache_paths(cache_dir: str) -> dict:
    """Return the paths where the retrieval index is cached on disk."""
    p = Path(cache_dir)
    return {
        "root": p,
        "vectorizer": p / "tfidf_vectorizer.pkl",
        "train_data": p / "train_data.pkl",
    }


def build_retrieval_index(
    cache_dir: str = AGENT_RETRIEVAL_CACHE_DIRNAME,
    subset: str = AGENT_RETRIEVAL_SUBSET,
    force_rebuild: bool = False,
) -> dict:
    """
    Build a TF-IDF retrieval index over the CodeXGLUE code_refinement
    training split, or load a previously cached one.

    On first run, downloads the training split (~50K Java method pairs
    for ``subset='small'``), fits a TF-IDF vectorizer on the buggy halves,
    and caches both the vectorizer and the training pairs to disk.

    Parameters
    ----------
    cache_dir : str
        Directory to hold cached pickles. Created if missing.
    subset : str
        "small" (methods up to 50 tokens) or "medium" (up to 100).
        Match the subset used at inference time.
    force_rebuild : bool
        If True, ignore any cached files and rebuild from scratch.

    Returns
    -------
    dict with keys:
        - vectorizer: fitted TfidfVectorizer
        - train_pairs: list of {"buggy": str, "fixed": str, "vec": sparse row}
    """
    import pickle
    from sklearn.feature_extraction.text import TfidfVectorizer

    paths = _retrieval_cache_paths(cache_dir)
    paths["root"].mkdir(parents=True, exist_ok=True)

    if (
        not force_rebuild
        and paths["vectorizer"].exists()
        and paths["train_data"].exists()
    ):
        logger.info("Loading cached retrieval index from %s", paths["root"])
        with open(paths["vectorizer"], "rb") as f:
            vectorizer = pickle.load(f)
        with open(paths["train_data"], "rb") as f:
            train_pairs = pickle.load(f)
        logger.info(
            "Retrieval index loaded: %d training pairs, %d features",
            len(train_pairs),
            len(vectorizer.get_feature_names_out()),
        )
        from scipy import sparse
        train_matrix = sparse.vstack([p["vec"] for p in train_pairs])
        return {
            "vectorizer": vectorizer,
            "train_pairs": train_pairs,
            "train_matrix": train_matrix,
        }

    logger.info(
        "Building retrieval index from CodeXGLUE (subset=%s). "
        "This runs once and caches to disk.",
        subset,
    )
    from datasets import load_dataset

    ds = load_dataset(
        "google/code_x_glue_cc_code_refinement", subset, split="train"
    )
    buggy_texts = [row["buggy"] for row in ds]
    fixed_texts = [row["fixed"] for row in ds]
    logger.info("Loaded %d CodeXGLUE training pairs", len(buggy_texts))

    vectorizer = TfidfVectorizer(
        analyzer="char",
        ngram_range=(3, 5),
        max_features=20000,
        min_df=2,
    )
    matrix = vectorizer.fit_transform(buggy_texts)
    logger.info(
        "Fitted TF-IDF: %d documents x %d features",
        matrix.shape[0],
        matrix.shape[1],
    )

    # Store each row's sparse vector alongside the pair so retrieval at
    # query time is a single vectorize + cosine op.
    train_pairs = [
        {"buggy": buggy_texts[i], "fixed": fixed_texts[i], "vec": matrix[i]}
        for i in range(len(buggy_texts))
    ]

    with open(paths["vectorizer"], "wb") as f:
        pickle.dump(vectorizer, f)
    with open(paths["train_data"], "wb") as f:
        pickle.dump(train_pairs, f)
    logger.info("Cached retrieval index to %s", paths["root"])

    from scipy import sparse
    train_matrix = sparse.vstack([p["vec"] for p in train_pairs])

    return {
        "vectorizer": vectorizer,
        "train_pairs": train_pairs,
        "train_matrix": train_matrix,
    }


def retrieve_similar_examples(
    query_code: str,
    index: dict,
    k: int = AGENT_DEFAULT_N_RETRIEVAL_EXAMPLES,
) -> list[dict]:
    """
    Return the top-k training pairs most similar to the query by
    TF-IDF cosine similarity.

    Parameters
    ----------
    query_code : str
        Java method the agent is being asked to refactor.
    index : dict
        Output of ``build_retrieval_index``.
    k : int
        Number of examples to return.

    Returns
    -------
    list of {"buggy": str, "fixed": str, "similarity": float}
        Sorted by similarity descending.
    """
    from sklearn.metrics.pairwise import cosine_similarity
    import numpy as np
    from scipy import sparse

    vectorizer = index["vectorizer"]
    train_pairs = index["train_pairs"]
    train_matrix = index["train_matrix"]


    query_vec = vectorizer.transform([query_code])

    # Stack all training vectors vertically (one-time cost per query).
    # For very large indices we'd do this once outside the function, but
    # for 50K pairs it's fine.
    sims = cosine_similarity(query_vec, train_matrix)[0]

    top_idx = np.argsort(sims)[::-1][:k]

    return [
        {
            "buggy": train_pairs[i]["buggy"],
            "fixed": train_pairs[i]["fixed"],
            "similarity": float(sims[i]),
        }
        for i in top_idx
    ]


# -----------------------------------------------------------------------------
# The refactoring agent
# -----------------------------------------------------------------------------

AGENT_SYSTEM_PROMPT = (
    "You are a Java code refactoring assistant. "
    "Given a buggy Java method, produce the fixed version. "
    "Output only the corrected Java method, no explanations, "
    "no markdown fences, no surrounding commentary."
)


def _build_few_shot_messages(
    buggy_code: str,
    retrieved_examples: list[dict],
) -> list[dict]:
    """
    Build the chat-format message list for a few-shot-retrieval prompt.

    Matches the benchmark's prompt structure so agent results are
    comparable to the Section 7 leaderboard.
    """
    messages = [{"role": "system", "content": AGENT_SYSTEM_PROMPT}]

    for ex in retrieved_examples:
        messages.append({
            "role": "user",
            "content": f"Fix this Java method:\n\n{ex['buggy']}",
        })
        messages.append({
            "role": "assistant",
            "content": ex["fixed"],
        })

    messages.append({
        "role": "user",
        "content": f"Fix this Java method:\n\n{buggy_code}",
    })

    return messages


def _extract_java_from_response(response: str) -> str:
    """
    Strip markdown fences and extraneous prose from the model's output.

    Models sometimes wrap code in ```java ... ``` blocks or add commentary
    even when instructed not to. Pull out the longest code-like segment.
    """
    text = response.strip()

    # Markdown java fence.
    if "```java" in text:
        after = text.split("```java", 1)[1]
        if "```" in after:
            return after.split("```", 1)[0].strip()
        return after.strip()

    # Plain markdown fence.
    if "```" in text:
        parts = text.split("```")
        if len(parts) >= 3:
            return parts[1].strip()
        return parts[1].strip() if len(parts) == 2 else text

    return text


def refactor_java_method(
    buggy_code: str,
    model,
    tokenizer,
    retrieval_index: Optional[dict] = None,
    reference_code: Optional[str] = None,
    n_retrieval_examples: int = AGENT_DEFAULT_N_RETRIEVAL_EXAMPLES,
    max_new_tokens: int = AGENT_DEFAULT_MAX_NEW_TOKENS,
    seed: int = AGENT_DEFAULT_SEED,
) -> dict:
    """
    Run one refactoring pass: generate a fixed version of the buggy
    Java method, validate it, and return a confidence-scored result.

    Parameters
    ----------
    buggy_code : str
        The Java method to refactor. Can be a CodeXGLUE-normalized method
        (with VAR_1, METHOD_1 tokens) or any Java method.
    model, tokenizer : transformers model + tokenizer pair
        The LLM used for generation. Any HuggingFace causal-LM model works.
    retrieval_index : dict, optional
        Output of ``build_retrieval_index``. If provided, the agent uses
        few-shot retrieval. If None, the agent runs zero-shot.
    reference_code : str, optional
        Ground-truth fix, used for BLEU and exact-match metrics. If None,
        metrics against a reference are skipped and confidence is based on
        validity alone.
    n_retrieval_examples : int
        Number of similar examples to retrieve. Ignored if
        retrieval_index is None.
    max_new_tokens : int
        Generation cap. 512 matches the benchmark.
    seed : int
        Fixed for deterministic output (do_sample=False + torch seed).

    Returns
    -------
    dict with keys:
        buggy, generated_raw, generated_clean, reference,
        is_valid, exact_match, bleu,
        confidence (dict: level + score),
        elapsed_s, strategy_used, retrieved_examples (if any).
    """
    import time
    import torch

    t_start = time.time()

    # Select strategy and build prompt.
    if retrieval_index is not None:
        retrieved = retrieve_similar_examples(
            buggy_code, retrieval_index, k=n_retrieval_examples
        )
        messages = _build_few_shot_messages(buggy_code, retrieved)
        strategy_used = "few_shot_retrieval"
    else:
        retrieved = []
        messages = [
            {"role": "system", "content": AGENT_SYSTEM_PROMPT},
            {"role": "user", "content": f"Fix this Java method:\n\n{buggy_code}"},
        ]
        strategy_used = "zero_shot"

    # Apply chat template and tokenize.
    prompt_text = tokenizer.apply_chat_template(
        messages, tokenize=False, add_generation_prompt=True
    )
    inputs = tokenizer([prompt_text], return_tensors="pt").to(model.device)

    torch.manual_seed(seed)
    with torch.no_grad():
        output_ids = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            do_sample=False,
            pad_token_id=tokenizer.eos_token_id,
        )

    generated_ids = output_ids[0][len(inputs.input_ids[0]):]
    generated_raw = tokenizer.decode(generated_ids, skip_special_tokens=True)
    generated_clean = _extract_java_from_response(generated_raw)

    # Validate and score.
    syntax = validate_java_syntax(generated_clean)
    is_valid = syntax["is_valid"]

    if reference_code:
        exact_match = is_exact_match(generated_clean, reference_code)
        bleu = compute_bleu_against_reference(generated_clean, reference_code)
    else:
        exact_match = False
        bleu = 0.0

    confidence = compute_confidence_score(
        is_valid=is_valid,
        exact_match=exact_match,
        bleu_score=bleu,
    )

    elapsed = time.time() - t_start

    logger.info(
        "Refactored via %s: valid=%s exact=%s BLEU=%.1f confidence=%s (%.1fs)",
        strategy_used,
        is_valid,
        exact_match,
        bleu,
        confidence["level"],
        elapsed,
    )

    elapsed = time.time() - t_start

    # Free memory between calls. In tight-memory environments (CPU-only
    # Docker on a laptop), PyTorch holds on to activation and cache memory
    # by default. Clearing them after generation lets subsequent calls
    # reuse the space instead of accumulating.
    import gc
    del inputs, output_ids, generated_ids
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()

    return {
        "buggy": buggy_code,
        "generated_raw": generated_raw,
        "generated_clean": generated_clean,
        "reference": reference_code,
        "is_valid": is_valid,
        "exact_match": exact_match,
        "bleu": bleu,
        "confidence": confidence,
        "elapsed_s": elapsed,
        "strategy_used": strategy_used,
        "retrieved_examples": retrieved,
        "syntax_error": syntax["error"],
    }