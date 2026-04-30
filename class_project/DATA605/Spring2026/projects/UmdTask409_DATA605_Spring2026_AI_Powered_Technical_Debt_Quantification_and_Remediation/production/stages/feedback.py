"""
Stage 8: Feedback logging for the Option B pipeline.

Each pipeline stage that produces a meaningful event (prediction,
prioritization, refactoring, validation) writes a row to a SQLite
database. Over many runs this builds up a dataset of (predicted,
actual) pairs that future work can use to recalibrate the fault
predictor or evaluate refactoring quality.

Stage 8 only records. It does not retrain models or alter pipeline
behavior. Closing the loop autonomously is future work.

Schema:
    feedback_id     INTEGER PRIMARY KEY AUTOINCREMENT
    timestamp       TEXT (ISO 8601)
    issue_id        TEXT (deterministic hash from Stage 2)
    event_type      TEXT (predicted, prioritized, refactored, validated)
    repo_name       TEXT (optional)
    file_path       TEXT (optional)
    rule            TEXT (optional)
    payload         TEXT (JSON blob, event-specific fields)

Usage:
    from production.stages.feedback import log_event, get_events_for_issue
    log_event(
        event_type="predicted",
        issue=stage_4_issue,
        repo_name="commons-lang",
        payload={"fault_probability": 0.55, "host_commit": "abc123"},
    )
    history = get_events_for_issue(issue["issue_id"])
"""

import json
import logging
import os
import sqlite3
from datetime import datetime, timezone
from typing import Optional

logger = logging.getLogger(__name__)


DEFAULT_DB_PATH = "/data/production/data/feedback.sqlite"

VALID_EVENT_TYPES = {
    "predicted",
    "prioritized",
    "refactored",
    "validated",
}

_SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS feedback (
    feedback_id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    issue_id TEXT NOT NULL,
    event_type TEXT NOT NULL,
    repo_name TEXT,
    file_path TEXT,
    rule TEXT,
    payload TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_issue_id ON feedback(issue_id);
CREATE INDEX IF NOT EXISTS idx_event_type ON feedback(event_type);
CREATE INDEX IF NOT EXISTS idx_timestamp ON feedback(timestamp);
"""


def initialize_database(db_path: str = DEFAULT_DB_PATH) -> None:
    """Create the feedback table and indices. Idempotent.

    Called automatically by log_event the first time it runs against
    a given database path. Safe to call manually too.
    """
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    with sqlite3.connect(db_path) as conn:
        conn.executescript(_SCHEMA_SQL)
        conn.commit()
    logger.debug("Initialized feedback database at %s", db_path)


def log_event(
    event_type: str,
    issue: dict,
    repo_name: Optional[str] = None,
    payload: Optional[dict] = None,
    db_path: str = DEFAULT_DB_PATH,
) -> int:
    """Record one event for an issue.

    Args:
        event_type: one of VALID_EVENT_TYPES.
        issue: issue dict from any pipeline stage. Must have 'issue_id'.
        repo_name: short name of the repo the issue is from.
        payload: dict of event-specific fields. JSON-serialized into
            the database. None becomes an empty dict.
        db_path: SQLite database file path.

    Returns:
        feedback_id of the inserted row.

    Raises:
        ValueError: if event_type is not recognized or issue has no
            issue_id.
    """
    if event_type not in VALID_EVENT_TYPES:
        raise ValueError(
            f"Unknown event_type: {event_type!r}. "
            f"Valid: {sorted(VALID_EVENT_TYPES)}"
        )
    issue_id = issue.get("issue_id")
    if not issue_id:
        raise ValueError(
            "Issue dict must have 'issue_id' field for feedback logging."
        )

    initialize_database(db_path)

    timestamp = datetime.now(timezone.utc).isoformat()
    payload_json = json.dumps(payload or {})

    with sqlite3.connect(db_path) as conn:
        cursor = conn.execute(
            """
            INSERT INTO feedback
                (timestamp, issue_id, event_type, repo_name,
                 file_path, rule, payload)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                timestamp,
                issue_id,
                event_type,
                repo_name,
                issue.get("file_path"),
                issue.get("rule"),
                payload_json,
            ),
        )
        conn.commit()
        feedback_id = cursor.lastrowid

    logger.debug(
        "Logged %s event for issue %s as feedback_id %d",
        event_type, issue_id, feedback_id,
    )
    return feedback_id


def get_events_for_issue(
    issue_id: str,
    db_path: str = DEFAULT_DB_PATH,
) -> list:
    """Return all events for one issue, ordered by timestamp ascending.

    Each event is a dict with the row's columns plus the parsed payload.
    Returns an empty list if the issue has no events or the database
    does not exist.
    """
    if not os.path.exists(db_path):
        return []

    with sqlite3.connect(db_path) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            """
            SELECT * FROM feedback
            WHERE issue_id = ?
            ORDER BY timestamp ASC
            """,
            (issue_id,),
        ).fetchall()

    return [_row_to_dict(row) for row in rows]


def get_recent_events(
    event_type: Optional[str] = None,
    limit: int = 100,
    db_path: str = DEFAULT_DB_PATH,
) -> list:
    """Return the most recent events, optionally filtered by event_type.

    Args:
        event_type: if set, only events of this type are returned.
        limit: maximum number of rows to return.
        db_path: SQLite database file path.

    Returns:
        List of event dicts, most recent first.
    """
    if not os.path.exists(db_path):
        return []

    with sqlite3.connect(db_path) as conn:
        conn.row_factory = sqlite3.Row
        if event_type is not None:
            if event_type not in VALID_EVENT_TYPES:
                raise ValueError(
                    f"Unknown event_type: {event_type!r}"
                )
            rows = conn.execute(
                """
                SELECT * FROM feedback
                WHERE event_type = ?
                ORDER BY timestamp DESC
                LIMIT ?
                """,
                (event_type, limit),
            ).fetchall()
        else:
            rows = conn.execute(
                """
                SELECT * FROM feedback
                ORDER BY timestamp DESC
                LIMIT ?
                """,
                (limit,),
            ).fetchall()

    return [_row_to_dict(row) for row in rows]


def get_event_counts(db_path: str = DEFAULT_DB_PATH) -> dict:
    """Return the count of events grouped by event_type.

    Useful for dashboards and quick sanity checks.
    """
    if not os.path.exists(db_path):
        return {}
    with sqlite3.connect(db_path) as conn:
        rows = conn.execute(
            """
            SELECT event_type, COUNT(*) as n
            FROM feedback
            GROUP BY event_type
            """
        ).fetchall()
    return {event_type: count for event_type, count in rows}


def _row_to_dict(row: sqlite3.Row) -> dict:
    """Convert a SQLite row to a dict with parsed payload."""
    d = dict(row)
    try:
        d["payload"] = json.loads(d["payload"])
    except (json.JSONDecodeError, TypeError):
        d["payload"] = {}
    return d

def get_summary_metrics(db_path: str = DEFAULT_DB_PATH) -> dict:
    """Return overall pipeline health metrics from the feedback DB.

    Returns a dict with:
        total_events: total rows in the feedback table
        events_by_type: count per event_type
        unique_issues: number of distinct issue_ids
        unique_repos: number of distinct repo_names
        first_event: earliest timestamp seen
        last_event: latest timestamp seen
    """
    if not os.path.exists(db_path):
        return {
            "total_events": 0,
            "events_by_type": {},
            "unique_issues": 0,
            "unique_repos": 0,
            "first_event": None,
            "last_event": None,
        }

    with sqlite3.connect(db_path) as conn:
        total = conn.execute(
            "SELECT COUNT(*) FROM feedback"
        ).fetchone()[0]

        events_by_type = dict(
            conn.execute(
                "SELECT event_type, COUNT(*) FROM feedback "
                "GROUP BY event_type"
            ).fetchall()
        )

        unique_issues = conn.execute(
            "SELECT COUNT(DISTINCT issue_id) FROM feedback"
        ).fetchone()[0]

        unique_repos = conn.execute(
            "SELECT COUNT(DISTINCT repo_name) FROM feedback "
            "WHERE repo_name IS NOT NULL"
        ).fetchone()[0]

        first_event, last_event = conn.execute(
            "SELECT MIN(timestamp), MAX(timestamp) FROM feedback"
        ).fetchone()

    return {
        "total_events": total,
        "events_by_type": events_by_type,
        "unique_issues": unique_issues,
        "unique_repos": unique_repos,
        "first_event": first_event,
        "last_event": last_event,
    }


def get_success_rate_by_rule(
    event_type: str,
    db_path: str = DEFAULT_DB_PATH,
) -> dict:
    """Compute per-rule success rates for a given event type.

    For event_type='refactored', success means best_strategy is not None.
    For event_type='validated', success means succeeded is True.

    Returns:
        dict mapping rule -> {"total": int, "succeeded": int,
                              "rate": float}
    """
    if event_type not in {"refactored", "validated"}:
        raise ValueError(
            f"Success rate is only defined for 'refactored' or "
            f"'validated' events, got {event_type!r}"
        )
    if not os.path.exists(db_path):
        return {}

    with sqlite3.connect(db_path) as conn:
        rows = conn.execute(
            """
            SELECT rule, payload
            FROM feedback
            WHERE event_type = ? AND rule IS NOT NULL
            """,
            (event_type,),
        ).fetchall()

    by_rule: dict = {}
    for rule, payload_text in rows:
        try:
            payload = json.loads(payload_text)
        except (json.JSONDecodeError, TypeError):
            continue

        if event_type == "refactored":
            succeeded = payload.get("best_strategy") is not None
        else:
            succeeded = bool(payload.get("succeeded"))

        bucket = by_rule.setdefault(
            rule, {"total": 0, "succeeded": 0, "rate": 0.0}
        )
        bucket["total"] += 1
        if succeeded:
            bucket["succeeded"] += 1

    for bucket in by_rule.values():
        if bucket["total"] > 0:
            bucket["rate"] = bucket["succeeded"] / bucket["total"]

    return by_rule


def get_per_repo_summary(db_path: str = DEFAULT_DB_PATH) -> dict:
    """Per-repo summary of event activity.

    Returns:
        dict mapping repo_name -> {"events_by_type": {...},
                                   "unique_issues": int,
                                   "first_event": str,
                                   "last_event": str}
    """
    if not os.path.exists(db_path):
        return {}

    with sqlite3.connect(db_path) as conn:
        repo_rows = conn.execute(
            "SELECT DISTINCT repo_name FROM feedback "
            "WHERE repo_name IS NOT NULL"
        ).fetchall()

        result: dict = {}
        for (repo,) in repo_rows:
            events_by_type = dict(
                conn.execute(
                    "SELECT event_type, COUNT(*) FROM feedback "
                    "WHERE repo_name = ? GROUP BY event_type",
                    (repo,),
                ).fetchall()
            )
            unique_issues = conn.execute(
                "SELECT COUNT(DISTINCT issue_id) FROM feedback "
                "WHERE repo_name = ?",
                (repo,),
            ).fetchone()[0]
            first_event, last_event = conn.execute(
                "SELECT MIN(timestamp), MAX(timestamp) FROM feedback "
                "WHERE repo_name = ?",
                (repo,),
            ).fetchone()
            result[repo] = {
                "events_by_type": events_by_type,
                "unique_issues": unique_issues,
                "first_event": first_event,
                "last_event": last_event,
            }

    return result