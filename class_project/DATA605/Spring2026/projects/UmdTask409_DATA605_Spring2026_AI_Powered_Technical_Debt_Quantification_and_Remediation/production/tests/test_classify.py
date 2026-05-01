"""Tests for production.stages.classify."""

import unittest
from pathlib import Path

from production.stages.classify import (
    aggregate_to_readme_view,
    summarize_view,
    classify_issue,
    PMD_RULESET_TO_README,
    README_BUCKETS,
    RULE_TO_README,
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


class TestClassifyIssue(unittest.TestCase):
    """Test the per-issue classification function directly."""

    def test_per_rule_mapping_takes_precedence(self):
        # ReplaceHashtableWithHashMap is in the CSV as outdated_patterns.
        # Its ruleset is Best Practices, which maps to code_smells via
        # the fallback. Per-rule should win.
        issue = make_issue("ReplaceHashtableWithHashMap", "Best Practices")
        self.assertEqual(classify_issue(issue), "outdated_patterns")

    def test_ruleset_fallback_when_rule_unmapped(self):
        # An obscure rule not in the CSV should fall back to ruleset.
        issue = make_issue("SomeRuleNotInCSV", "Performance")
        self.assertEqual(classify_issue(issue), "performance_issues")

    def test_unknown_ruleset_returns_none(self):
        issue = make_issue("UnknownRule", "BogusRuleset")
        self.assertIsNone(classify_issue(issue))

    def test_missing_fields_returns_none(self):
        self.assertIsNone(classify_issue({}))


class TestAggregateToReadmeView(unittest.TestCase):
    def test_empty_input_produces_empty_buckets(self):
        view = aggregate_to_readme_view([])
        self.assertEqual(view["total"], 0)
        for bucket in README_BUCKETS:
            self.assertEqual(view["buckets"][bucket], [])
        self.assertEqual(view["unmapped"], [])

    def test_design_issue_routes_to_architectural_violations(self):
        # UseUtilityClass is in the CSV as architectural_violations.
        issues = [make_issue("UseUtilityClass", "Design")]
        view = aggregate_to_readme_view(issues)
        self.assertEqual(len(view["buckets"]["architectural_violations"]), 1)

    def test_performance_ruleset_fallback(self):
        # A rule not in the CSV with Performance ruleset should fall
        # back to performance_issues via ruleset-level mapping.
        issues = [make_issue("FakePerformanceRuleNotInCSV", "Performance")]
        view = aggregate_to_readme_view(issues)
        self.assertEqual(len(view["buckets"]["performance_issues"]), 1)

    def test_multithreading_issue_routes_to_concurrency_issues(self):
        # An obscure multithreading rule not in CSV: ruleset fallback.
        issues = [make_issue("SomeUncommonThreadRule", "Multithreading")]
        view = aggregate_to_readme_view(issues)
        self.assertEqual(len(view["buckets"]["concurrency_issues"]), 1)

    def test_best_practices_routes_to_code_smells_via_fallback(self):
        # An obscure best-practices rule not in CSV.
        issues = [make_issue("SomeObscureBestPractice", "Best Practices")]
        view = aggregate_to_readme_view(issues)
        self.assertEqual(len(view["buckets"]["code_smells"]), 1)

    def test_outdated_patterns_bucket_populated_by_csv(self):
        # ReplaceHashtableWithHashMap is in the CSV as outdated_patterns.
        # This is the key behavior change from the old ruleset-only
        # version, which left outdated_patterns empty by design.
        issues = [
            make_issue("ReplaceHashtableWithHashMap", "Best Practices"),
            make_issue("ReplaceVectorWithArrayList", "Best Practices"),
        ]
        view = aggregate_to_readme_view(issues)
        self.assertEqual(len(view["buckets"]["outdated_patterns"]), 2)

    def test_unknown_ruleset_goes_to_unmapped(self):
        issues = [make_issue("UnknownRule", "BogusRuleset")]
        view = aggregate_to_readme_view(issues)
        self.assertEqual(len(view["unmapped"]), 1)
        for bucket in README_BUCKETS:
            self.assertEqual(view["buckets"][bucket], [])

    def test_missing_ruleset_field_goes_to_unmapped(self):
        issues = [{"issue_id": "x", "rule": "Foo"}]
        view = aggregate_to_readme_view(issues)
        self.assertEqual(len(view["unmapped"]), 1)

    def test_total_matches_input_length(self):
        issues = [
            make_issue("UseUtilityClass", "Design", "a"),
            make_issue("ReplaceVectorWithArrayList", "Best Practices", "b"),
            make_issue("Foo", "BogusRuleset", "c"),
        ]
        view = aggregate_to_readme_view(issues)
        self.assertEqual(view["total"], 3)


class TestRuleMappingLoaded(unittest.TestCase):
    """The CSV should be loaded at module import."""

    def test_csv_loaded_with_expected_size(self):
        # The CSV has 292 mapped rules (293 lines including header).
        # Allow some tolerance in case the CSV is updated.
        self.assertGreater(len(RULE_TO_README), 250)

    def test_csv_contains_outdated_patterns_examples(self):
        # Sanity-check that some rules map to outdated_patterns.
        outdated_rules = [
            r for r, c in RULE_TO_README.items()
            if c == "outdated_patterns"
        ]
        self.assertGreater(len(outdated_rules), 10)


class TestSummarizeView(unittest.TestCase):
    def test_summarize_with_issues(self):
        issues = [
            make_issue("UseUtilityClass", "Design"),
            make_issue("ReplaceVectorWithArrayList", "Best Practices"),
        ]
        view = aggregate_to_readme_view(issues)
        summary = summarize_view(view)
        self.assertIn("Total issues: 2", summary)
        self.assertIn("architectural_violations: 1", summary)
        self.assertIn("outdated_patterns: 1", summary)

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
        # Check non-empty buckets we expect on commons-lang3.
        self.assertGreater(len(view["buckets"]["code_smells"]), 0)
        self.assertGreater(len(view["buckets"]["architectural_violations"]), 0)
        self.assertGreater(len(view["buckets"]["performance_issues"]), 0)


if __name__ == "__main__":
    unittest.main()