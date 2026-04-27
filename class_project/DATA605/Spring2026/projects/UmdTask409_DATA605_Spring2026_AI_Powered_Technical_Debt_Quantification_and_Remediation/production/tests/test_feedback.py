"""Tests for production.stages.feedback."""

import os
import sys
import tempfile
import unittest
from pathlib import Path

# Make production package importable.
sys.path.insert(0, "/data")

from production.stages.feedback import (
    initialize_database,
    log_event,
    get_events_for_issue,
    get_recent_events,
    get_event_counts,
    VALID_EVENT_TYPES,
)


def make_issue(issue_id="x123", rule="UseUtilityClass",
               file_path="/tmp/Foo.java"):
    return {
        "issue_id": issue_id,
        "rule": rule,
        "ruleset": "Design",
        "file_path": file_path,
        "begin_line": 42,
    }


class TestInitializeDatabase(unittest.TestCase):
    def test_creates_database_file(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = os.path.join(tmpdir, "test.sqlite")
            initialize_database(db_path)
            self.assertTrue(os.path.exists(db_path))

    def test_idempotent(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = os.path.join(tmpdir, "test.sqlite")
            initialize_database(db_path)
            initialize_database(db_path)  # second call should not fail
            self.assertTrue(os.path.exists(db_path))


class TestLogEvent(unittest.TestCase):
    def test_log_event_returns_feedback_id(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = os.path.join(tmpdir, "test.sqlite")
            issue = make_issue()
            fid = log_event(
                event_type="predicted",
                issue=issue,
                repo_name="commons-lang",
                payload={"fault_probability": 0.5},
                db_path=db_path,
            )
            self.assertIsInstance(fid, int)
            self.assertGreater(fid, 0)

    def test_log_event_persists(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = os.path.join(tmpdir, "test.sqlite")
            issue = make_issue("abc", "MethodNamingConventions")
            log_event("predicted", issue, db_path=db_path,
                      payload={"fault_probability": 0.7})
            events = get_events_for_issue("abc", db_path=db_path)
            self.assertEqual(len(events), 1)
            self.assertEqual(events[0]["event_type"], "predicted")
            self.assertEqual(events[0]["payload"]["fault_probability"], 0.7)
            self.assertEqual(events[0]["rule"], "MethodNamingConventions")

    def test_log_event_invalid_event_type_raises(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = os.path.join(tmpdir, "test.sqlite")
            with self.assertRaises(ValueError):
                log_event(
                    "bogus_type",
                    issue=make_issue(),
                    db_path=db_path,
                )

    def test_log_event_missing_issue_id_raises(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = os.path.join(tmpdir, "test.sqlite")
            with self.assertRaises(ValueError):
                log_event(
                    "predicted",
                    issue={"rule": "Foo"},  # no issue_id
                    db_path=db_path,
                )

    def test_log_event_default_payload(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = os.path.join(tmpdir, "test.sqlite")
            log_event("predicted", make_issue("z"), db_path=db_path)
            events = get_events_for_issue("z", db_path=db_path)
            self.assertEqual(events[0]["payload"], {})


class TestQueryFunctions(unittest.TestCase):
    def test_get_events_for_issue_ordered(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = os.path.join(tmpdir, "test.sqlite")
            issue = make_issue("ord")
            log_event("predicted", issue, db_path=db_path)
            log_event("prioritized", issue, db_path=db_path)
            log_event("validated", issue, db_path=db_path)
            events = get_events_for_issue("ord", db_path=db_path)
            self.assertEqual(len(events), 3)
            types = [e["event_type"] for e in events]
            self.assertEqual(types, ["predicted", "prioritized", "validated"])

    def test_get_events_for_nonexistent_issue(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = os.path.join(tmpdir, "test.sqlite")
            log_event("predicted", make_issue("x"), db_path=db_path)
            events = get_events_for_issue("nonexistent", db_path=db_path)
            self.assertEqual(events, [])

    def test_get_recent_events_no_db(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = os.path.join(tmpdir, "nonexistent.sqlite")
            self.assertEqual(get_recent_events(db_path=db_path), [])

    def test_get_recent_events_filtered(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = os.path.join(tmpdir, "test.sqlite")
            log_event("predicted", make_issue("a"), db_path=db_path)
            log_event("prioritized", make_issue("a"), db_path=db_path)
            log_event("predicted", make_issue("b"), db_path=db_path)
            predicted = get_recent_events(
                event_type="predicted", db_path=db_path
            )
            self.assertEqual(len(predicted), 2)
            for e in predicted:
                self.assertEqual(e["event_type"], "predicted")

    def test_get_recent_events_limit(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = os.path.join(tmpdir, "test.sqlite")
            for i in range(10):
                log_event(
                    "predicted",
                    make_issue(f"id_{i}"),
                    db_path=db_path,
                )
            events = get_recent_events(limit=3, db_path=db_path)
            self.assertEqual(len(events), 3)

    def test_get_event_counts(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = os.path.join(tmpdir, "test.sqlite")
            log_event("predicted", make_issue("a"), db_path=db_path)
            log_event("predicted", make_issue("b"), db_path=db_path)
            log_event("validated", make_issue("a"), db_path=db_path)
            counts = get_event_counts(db_path=db_path)
            self.assertEqual(counts.get("predicted"), 2)
            self.assertEqual(counts.get("validated"), 1)
            self.assertNotIn("refactored", counts)


class TestPayloadJSON(unittest.TestCase):
    def test_complex_payload_round_trip(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = os.path.join(tmpdir, "test.sqlite")
            payload = {
                "fault_probability": 0.55,
                "host_commit": "abc123",
                "nested": {"a": 1, "b": [1, 2, 3]},
            }
            log_event(
                "predicted",
                make_issue("p"),
                payload=payload,
                db_path=db_path,
            )
            events = get_events_for_issue("p", db_path=db_path)
            self.assertEqual(events[0]["payload"], payload)


if __name__ == "__main__":
    unittest.main()