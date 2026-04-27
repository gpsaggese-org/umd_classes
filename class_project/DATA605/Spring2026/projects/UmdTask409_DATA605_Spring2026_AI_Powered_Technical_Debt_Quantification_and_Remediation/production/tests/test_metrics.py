"""Tests for production.lib.metrics."""

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

# Make production package importable.
sys.path.insert(0, "/data")

from production.lib.metrics import (
    compute_repo_metrics,
    compute_commit_churn,
    find_last_touch_commit,
    METRIC_COLUMNS,
    CHURN_COLUMNS,
    _cyclomatic_complexity,
    _count_lines,
    _comment_density,
    _safe_div,
)


COMMONS_LANG_REPO = (
    "/data/production/spikes/q1_agent_on_real_code/commons-lang"
)
COMMONS_LANG_SRC = (
    "/data/production/spikes/q1_agent_on_real_code/"
    "commons-lang/src/main/java"
)


class TestCountLines(unittest.TestCase):
    def test_simple_code(self):
        text = "int a = 1;\nint b = 2;\n"
        total, comment, ncloc = _count_lines(text)
        self.assertEqual(ncloc, 2)
        self.assertEqual(comment, 0)

    def test_line_comment(self):
        text = "// hello\nint a = 1;\n"
        total, comment, ncloc = _count_lines(text)
        self.assertEqual(comment, 1)
        self.assertEqual(ncloc, 1)

    def test_block_comment(self):
        text = "/* hello\n   world */\nint a = 1;\n"
        total, comment, ncloc = _count_lines(text)
        self.assertEqual(comment, 2)
        self.assertEqual(ncloc, 1)

    def test_blank_lines_ignored(self):
        text = "\n\nint a = 1;\n\n"
        total, comment, ncloc = _count_lines(text)
        self.assertEqual(ncloc, 1)
        self.assertEqual(comment, 0)


class TestSafeDiv(unittest.TestCase):
    def test_normal(self):
        self.assertAlmostEqual(_safe_div(10, 2), 5.0)

    def test_zero_denominator(self):
        self.assertEqual(_safe_div(10, 0), 0.0)


class TestCommentDensity(unittest.TestCase):
    def test_normal(self):
        # 30 comment, 70 code -> 30%
        self.assertAlmostEqual(_comment_density(30, 70), 30.0)

    def test_zero_total(self):
        self.assertEqual(_comment_density(0, 0), 0.0)


class TestCyclomaticComplexity(unittest.TestCase):
    def _parse_method(self, source):
        import javalang
        wrapped = f"public class Wrapper {{ {source} }}"
        tree = javalang.parse.parse(wrapped)
        for _, m in tree.filter(javalang.tree.MethodDeclaration):
            return m
        raise AssertionError("no method found")

    def test_no_branches_is_one(self):
        method = self._parse_method(
            "public int foo() { return 1; }"
        )
        self.assertEqual(_cyclomatic_complexity(method), 1)

    def test_single_if_is_two(self):
        method = self._parse_method(
            "public int foo(int x) { if (x > 0) return 1; return 0; }"
        )
        self.assertEqual(_cyclomatic_complexity(method), 2)

    def test_if_else_chain(self):
        method = self._parse_method(
            "public int foo(int x) {"
            "  if (x > 0) return 1;"
            "  else if (x < 0) return -1;"
            "  return 0;"
            "}"
        )
        # Two ifs => base 1 + 2 = 3.
        self.assertEqual(_cyclomatic_complexity(method), 3)

    def test_logical_and(self):
        method = self._parse_method(
            "public boolean foo(int x, int y) { return x > 0 && y > 0; }"
        )
        # Base 1 + 1 (&&) = 2.
        self.assertEqual(_cyclomatic_complexity(method), 2)

    def test_for_loop(self):
        method = self._parse_method(
            "public int foo(int n) {"
            "  int s = 0;"
            "  for (int i = 0; i < n; i++) s += i;"
            "  return s;"
            "}"
        )
        # Base 1 + 1 (for) = 2. The condition i < n is a comparison, not &&/||,
        # so it does not add.
        self.assertEqual(_cyclomatic_complexity(method), 2)


class TestComputeRepoMetrics(unittest.TestCase):
    def test_synthetic_repo(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            (Path(tmpdir) / "Foo.java").write_text(
                "public class Foo {\n"
                "    public int add(int a, int b) {\n"
                "        return a + b;\n"
                "    }\n"
                "}\n"
            )
            metrics = compute_repo_metrics(tmpdir)
            self.assertEqual(set(metrics.keys()), set(METRIC_COLUMNS))
            self.assertEqual(metrics["FILES"], 1)
            self.assertEqual(metrics["CLASSES"], 1)
            self.assertEqual(metrics["FUNCTIONS"], 1)
            self.assertGreaterEqual(metrics["NCLOC"], 3)
            self.assertEqual(metrics["DUPLICATED_LINES"], 0)

    def test_commons_lang(self):
        if not Path(COMMONS_LANG_SRC).exists():
            self.skipTest("commons-lang not available")
        metrics = compute_repo_metrics(COMMONS_LANG_SRC)
        # Plausibility ranges; commons-lang is sizable.
        self.assertGreater(metrics["FILES"], 100)
        self.assertGreater(metrics["FUNCTIONS"], 1000)
        self.assertGreater(metrics["NCLOC"], 10000)
        self.assertGreater(metrics["COMPLEXITY"], 1000)
        self.assertEqual(set(metrics.keys()), set(METRIC_COLUMNS))


class TestComputeCommitChurn(unittest.TestCase):
    def test_commons_lang_head(self):
        if not Path(COMMONS_LANG_REPO).exists():
            self.skipTest("commons-lang not available")
        result = subprocess.run(
            ["git", "-C", COMMONS_LANG_REPO, "rev-parse", "HEAD"],
            capture_output=True, text=True,
        )
        head = result.stdout.strip()
        churn = compute_commit_churn(COMMONS_LANG_REPO, head)
        self.assertEqual(set(churn.keys()), set(CHURN_COLUMNS))
        self.assertGreaterEqual(churn["files_changed"], 0)
        self.assertEqual(
            churn["churn_total"],
            churn["lines_added"] + churn["lines_removed"],
        )

    def test_invalid_commit_raises(self):
        if not Path(COMMONS_LANG_REPO).exists():
            self.skipTest("commons-lang not available")
        with self.assertRaises(RuntimeError):
            compute_commit_churn(COMMONS_LANG_REPO, "deadbeef0000notreal")


class TestFindLastTouchCommit(unittest.TestCase):
    def test_finds_commit_for_known_file(self):
        if not Path(COMMONS_LANG_REPO).exists():
            self.skipTest("commons-lang not available")
        sha = find_last_touch_commit(
            COMMONS_LANG_REPO,
            "src/main/java/org/apache/commons/lang3/StringUtils.java",
        )
        self.assertIsNotNone(sha)
        self.assertEqual(len(sha), 40)  # full SHA

    def test_absolute_path_works(self):
        if not Path(COMMONS_LANG_REPO).exists():
            self.skipTest("commons-lang not available")
        abs_path = os.path.join(
            COMMONS_LANG_REPO,
            "src/main/java/org/apache/commons/lang3/StringUtils.java",
        )
        sha = find_last_touch_commit(COMMONS_LANG_REPO, abs_path)
        self.assertIsNotNone(sha)


if __name__ == "__main__":
    unittest.main()