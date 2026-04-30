"""Tests for production.stages.classify."""

import unittest
from pathlib import Path

# Make production package importable.

from production.stages.classify import (
    aggregate_to_readme_view,
    summarize_view,
    PMD_RULESET_TO_README,
    README_BUCKETS,
)


def make_issue(rule, ruleset, issue_id="test_id"):
    """Build a minimal issue dict for testing."""
    return {
        "issue_id": issue_id,
        "rule": rule,
        "ruleset": ruleset,
        "file_path": "/tmp/Foo.java",
        "begin_line": 1,
    }


class TestAggregateToReadmeView(unittest.TestCase):
    def test_empty_input_produces_empty_buckets(self):
        view = aggregate_to_readme_view([])
        self.assertEqual(view["total"], 0)
        for bucket in README_BUCKETS:
            self.assertEqual(view["buckets"][bucket], [])
        self.assertEqual(view["unmapped"], [])

    def test_design_issue_routes_to_architectural_violations(self):
        issues = [make_issue("UseUtilityClass", "Design")]
        view = aggregate_to_readme_view(issues)
        self.assertEqual(len(view["buckets"]["architectural_violations"]), 1)
        self.assertEqual(len(view["buckets"]["code_smells"]), 0)

    def test_performance_issue_routes_to_performance_issues(self):
        issues = [make_issue("UseLocaleWithCaseConversions", "Performance")]
        view = aggregate_to_readme_view(issues)
        self.assertEqual(len(view["buckets"]["performance_issues"]), 1)

    def test_multithreading_issue_routes_to_concurrency_issues(self):
        issues = [make_issue("DoNotUseThreads", "Multithreading")]
        view = aggregate_to_readme_view(issues)
        self.assertEqual(len(view["buckets"]["concurrency_issues"]), 1)

    def test_best_practices_routes_to_code_smells(self):
        issues = [make_issue("UnusedImports", "Best Practices")]
        view = aggregate_to_readme_view(issues)
        self.assertEqual(len(view["buckets"]["code_smells"]), 1)

    def test_outdated_patterns_bucket_is_always_empty(self):
        # No PMD ruleset maps to outdated_patterns. The bucket should
        # always exist (so writeups can report on it) but stay empty.
        issues = [
            make_issue("UseUtilityClass", "Design"),
            make_issue("UnusedImports", "Best Practices"),
            make_issue("UseLocaleWithCaseConversions", "Performance"),
        ]
        view = aggregate_to_readme_view(issues)
        self.assertEqual(view["buckets"]["outdated_patterns"], [])

    def test_unknown_ruleset_goes_to_unmapped(self):
        issues = [make_issue("SomeRule", "BogusRuleset")]
        view = aggregate_to_readme_view(issues)
        self.assertEqual(len(view["unmapped"]), 1)
        for bucket in README_BUCKETS:
            self.assertEqual(view["buckets"][bucket], [])

    def test_missing_ruleset_field_goes_to_unmapped(self):
        issues = [{"issue_id": "x", "rule": "Foo"}]  # no ruleset field
        view = aggregate_to_readme_view(issues)
        self.assertEqual(len(view["unmapped"]), 1)

    def test_total_matches_input_length(self):
        issues = [
            make_issue("UseUtilityClass", "Design", "a"),
            make_issue("UnusedImports", "Best Practices", "b"),
            make_issue("Foo", "BogusRuleset", "c"),
        ]
        view = aggregate_to_readme_view(issues)
        self.assertEqual(view["total"], 3)


class TestSummarizeView(unittest.TestCase):
    def test_summarize_with_issues(self):
        issues = [
            make_issue("UseUtilityClass", "Design"),
            make_issue("UnusedImports", "Best Practices"),
        ]
        view = aggregate_to_readme_view(issues)
        summary = summarize_view(view)
        self.assertIn("Total issues: 2", summary)
        self.assertIn("architectural_violations: 1", summary)
        self.assertIn("code_smells: 1", summary)

    def test_summarize_with_unmapped(self):
        issues = [make_issue("Foo", "BogusRuleset")]
        view = aggregate_to_readme_view(issues)
        summary = summarize_view(view)
        self.assertIn("unmapped", summary)


class TestIntegrationWithCommonsLang(unittest.TestCase):
    """Stage 1 + Stage 2 + Stage 3 end-to-end on commons-lang3."""

    COMMONS_LANG_PATH = (
        "/data/production/spikes/q1_agent_on_real_code/commons-lang"
    )

    def test_full_pipeline(self):
        if not Path(self.COMMONS_LANG_PATH).exists():
            self.skipTest("commons-lang3 not available")

        from production.stages.ingest import ingest_repository
        from production.stages.analyze import analyze_repository

        result = ingest_repository(self.COMMONS_LANG_PATH)
        issues = analyze_repository(result["java_source_root"])
        view = aggregate_to_readme_view(issues)

        # Sanity checks.
        self.assertGreater(view["total"], 100)
        self.assertEqual(view["unmapped"], [])
        # We expect at least some hits in each non-empty bucket on
        # commons-lang3 (except outdated_patterns, which is always empty).
        self.assertGreater(len(view["buckets"]["code_smells"]), 0)
        self.assertGreater(len(view["buckets"]["architectural_violations"]), 0)
        self.assertGreater(len(view["buckets"]["performance_issues"]), 0)
        self.assertEqual(view["buckets"]["outdated_patterns"], [])


if __name__ == "__main__":
    unittest.main()