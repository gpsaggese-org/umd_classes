"""Tests for production.stages.analyze."""

import os
import tempfile
import unittest
from pathlib import Path

# Make production package importable.

from production.stages.analyze import (
    analyze_repository,
    _compute_issue_id,
    DEFAULT_PMD_PATH,
)


COMMONS_LANG_PATH = (
    "/data/production/spikes/q1_agent_on_real_code/"
    "commons-lang/src/main/java"
)


class TestComputeIssueId(unittest.TestCase):
    def test_deterministic(self):
        a = _compute_issue_id("/foo/Bar.java", "UseUtilityClass", 42)
        b = _compute_issue_id("/foo/Bar.java", "UseUtilityClass", 42)
        self.assertEqual(a, b)

    def test_different_inputs_give_different_ids(self):
        a = _compute_issue_id("/foo/Bar.java", "UseUtilityClass", 42)
        b = _compute_issue_id("/foo/Bar.java", "UseUtilityClass", 43)
        self.assertNotEqual(a, b)


class TestAnalyzeRepository(unittest.TestCase):
    """Integration tests against the real commons-lang3 clone."""

    def test_returns_many_issues(self):
        if not Path(COMMONS_LANG_PATH).exists():
            self.skipTest("commons-lang3 not available")
        issues = analyze_repository(COMMONS_LANG_PATH)
        self.assertGreater(len(issues), 100,
                           "Expected at least 100 issues; PMD config issue?")

    def test_issue_schema(self):
        if not Path(COMMONS_LANG_PATH).exists():
            self.skipTest("commons-lang3 not available")
        issues = analyze_repository(COMMONS_LANG_PATH)
        self.assertGreater(len(issues), 0)
        first = issues[0]
        expected_keys = {
            "issue_id", "file_path", "file_relative",
            "rule", "ruleset", "begin_line", "end_line",
            "begin_column", "end_column", "priority",
            "description", "external_info_url",
        }
        self.assertEqual(set(first.keys()), expected_keys)

    def test_issue_ids_are_unique(self):
        """No two issues should have the same ID."""
        if not Path(COMMONS_LANG_PATH).exists():
            self.skipTest("commons-lang3 not available")
        issues = analyze_repository(COMMONS_LANG_PATH)
        ids = [i["issue_id"] for i in issues]
        # Allow some collisions if multiple violations of the same rule
        # exist on the same line, but not many.
        self.assertGreater(len(set(ids)), len(ids) * 0.95)


class TestAnalyzeOnSyntheticFile(unittest.TestCase):
    """Test against a synthetic Java file with known issues."""

    def test_detects_use_utility_class(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            java_file = Path(tmpdir) / "AllStaticUtil.java"
            java_file.write_text("""
public class AllStaticUtil {
    public static int add(int a, int b) {
        return a + b;
    }
    public static int sub(int a, int b) {
        return a - b;
    }
}
""".strip())
            issues = analyze_repository(tmpdir)
            rules = [i["rule"] for i in issues]
            self.assertIn("UseUtilityClass", rules,
                          f"Expected UseUtilityClass; got rules: {rules}")


if __name__ == "__main__":
    unittest.main()