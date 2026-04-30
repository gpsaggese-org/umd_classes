"""Tests for production.stages.feedback."""

import os
import tempfile
import unittest
from pathlib import Path

# Make production package importable.

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

class TestSummaryMetrics(unittest.TestCase):
    def test_empty_db(self):
        from production.stages.feedback import get_summary_metrics
        with tempfile.TemporaryDirectory() as tmpdir:
            db = os.path.join(tmpdir, "empty.sqlite")
            metrics = get_summary_metrics(db)
            self.assertEqual(metrics["total_events"], 0)
            self.assertEqual(metrics["events_by_type"], {})
            self.assertEqual(metrics["unique_issues"], 0)

    def test_populated_db(self):
        from production.stages.feedback import (
            log_event, get_summary_metrics,
        )
        with tempfile.TemporaryDirectory() as tmpdir:
            db = os.path.join(tmpdir, "feedback.sqlite")
            log_event("predicted",
                      make_issue("a"), repo_name="r1",
                      payload={}, db_path=db)
            log_event("predicted",
                      make_issue("b"), repo_name="r1",
                      payload={}, db_path=db)
            log_event("refactored",
                      make_issue("a"), repo_name="r1",
                      payload={}, db_path=db)
            log_event("predicted",
                      make_issue("c"), repo_name="r2",
                      payload={}, db_path=db)

            metrics = get_summary_metrics(db)
            self.assertEqual(metrics["total_events"], 4)
            self.assertEqual(metrics["events_by_type"]["predicted"], 3)
            self.assertEqual(metrics["events_by_type"]["refactored"], 1)
            self.assertEqual(metrics["unique_issues"], 3)
            self.assertEqual(metrics["unique_repos"], 2)


class TestSuccessRateByRule(unittest.TestCase):
    def test_refactored_event_type(self):
        from production.stages.feedback import (
            log_event, get_success_rate_by_rule,
        )
        with tempfile.TemporaryDirectory() as tmpdir:
            db = os.path.join(tmpdir, "feedback.sqlite")
            log_event("refactored",
                      make_issue("a", rule="RuleX"),
                      payload={"best_strategy": "zero_shot"},
                      db_path=db)
            log_event("refactored",
                      make_issue("b", rule="RuleX"),
                      payload={"best_strategy": None},
                      db_path=db)
            log_event("refactored",
                      make_issue("c", rule="RuleY"),
                      payload={"best_strategy": "zero_shot"},
                      db_path=db)

            rates = get_success_rate_by_rule("refactored", db)
            self.assertEqual(rates["RuleX"]["total"], 2)
            self.assertEqual(rates["RuleX"]["succeeded"], 1)
            self.assertAlmostEqual(rates["RuleX"]["rate"], 0.5)
            self.assertEqual(rates["RuleY"]["total"], 1)
            self.assertEqual(rates["RuleY"]["succeeded"], 1)
            self.assertAlmostEqual(rates["RuleY"]["rate"], 1.0)

    def test_validated_event_type(self):
        from production.stages.feedback import (
            log_event, get_success_rate_by_rule,
        )
        with tempfile.TemporaryDirectory() as tmpdir:
            db = os.path.join(tmpdir, "feedback.sqlite")
            log_event("validated",
                      make_issue("a", rule="RuleX"),
                      payload={"succeeded": True},
                      db_path=db)
            log_event("validated",
                      make_issue("b", rule="RuleX"),
                      payload={"succeeded": False},
                      db_path=db)

            rates = get_success_rate_by_rule("validated", db)
            self.assertEqual(rates["RuleX"]["total"], 2)
            self.assertEqual(rates["RuleX"]["succeeded"], 1)
            self.assertAlmostEqual(rates["RuleX"]["rate"], 0.5)

    def test_invalid_event_type_raises(self):
        from production.stages.feedback import get_success_rate_by_rule
        with self.assertRaises(ValueError):
            get_success_rate_by_rule("predicted")

    def test_empty_db(self):
        from production.stages.feedback import get_success_rate_by_rule
        with tempfile.TemporaryDirectory() as tmpdir:
            db = os.path.join(tmpdir, "empty.sqlite")
            self.assertEqual(get_success_rate_by_rule("refactored", db), {})


class TestPerRepoSummary(unittest.TestCase):
    def test_per_repo_grouping(self):
        from production.stages.feedback import (
            log_event, get_per_repo_summary,
        )
        with tempfile.TemporaryDirectory() as tmpdir:
            db = os.path.join(tmpdir, "feedback.sqlite")
            log_event("predicted",
                      make_issue("a"), repo_name="r1",
                      db_path=db)
            log_event("refactored",
                      make_issue("a"), repo_name="r1",
                      db_path=db)
            log_event("predicted",
                      make_issue("b"), repo_name="r2",
                      db_path=db)

            summary = get_per_repo_summary(db)
            self.assertIn("r1", summary)
            self.assertIn("r2", summary)
            self.assertEqual(summary["r1"]["events_by_type"]["predicted"], 1)
            self.assertEqual(summary["r1"]["events_by_type"]["refactored"], 1)
            self.assertEqual(summary["r1"]["unique_issues"], 1)
            self.assertEqual(summary["r2"]["events_by_type"]["predicted"], 1)
            self.assertEqual(summary["r2"]["unique_issues"], 1)

    def test_empty_db(self):
        from production.stages.feedback import get_per_repo_summary
        with tempfile.TemporaryDirectory() as tmpdir:
            db = os.path.join(tmpdir, "empty.sqlite")
            self.assertEqual(get_per_repo_summary(db), {})


if __name__ == "__main__":
    unittest.main()