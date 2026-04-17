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