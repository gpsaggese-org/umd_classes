"""Tests for production.stages.validate."""

import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, "/data")

from production.stages.validate import (
    _splice_method,
    _detect_build_system,
    _tail,
    _summarize_error,
    _find_strategy,
    validate_refactor_records,
)


class TestSpliceMethod(unittest.TestCase):
    def test_basic_splice(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "Foo.java")
            with open(path, "w") as f:
                f.write("a\nb\nc\nd\ne\n")
            _splice_method(path, 2, 4, "X\nY")
            with open(path) as f:
                self.assertEqual(f.read(), "a\nX\nY\ne\n")

    def test_replacement_adds_newline(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "Foo.java")
            with open(path, "w") as f:
                f.write("a\nb\nc\n")
            _splice_method(path, 2, 2, "X")  # no trailing newline
            with open(path) as f:
                self.assertEqual(f.read(), "a\nX\nc\n")

    def test_invalid_range_raises(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "Foo.java")
            with open(path, "w") as f:
                f.write("a\nb\n")
            with self.assertRaises(ValueError):
                _splice_method(path, 0, 1, "X")
            with self.assertRaises(ValueError):
                _splice_method(path, 2, 1, "X")
            with self.assertRaises(ValueError):
                _splice_method(path, 1, 99, "X")


class TestDetectBuildSystem(unittest.TestCase):
    def test_detects_maven(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            Path(tmpdir, "pom.xml").write_text("<project/>")
            self.assertEqual(_detect_build_system(tmpdir), "maven")

    def test_detects_gradle_wrapper(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            Path(tmpdir, "build.gradle").write_text("// gradle")
            wrapper = Path(tmpdir, "gradlew")
            wrapper.write_text("#!/bin/sh\n")
            os.chmod(wrapper, 0o755)
            self.assertEqual(_detect_build_system(tmpdir), "gradle_wrapper")

    def test_detects_gradle_system(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            Path(tmpdir, "build.gradle.kts").write_text("// gradle")
            self.assertEqual(_detect_build_system(tmpdir), "gradle_system")

    def test_detects_none(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            Path(tmpdir, "Foo.java").write_text("class Foo {}")
            self.assertEqual(_detect_build_system(tmpdir), "none")


class TestTail(unittest.TestCase):
    def test_short_text_unchanged(self):
        self.assertEqual(_tail("hello", 100), "hello")

    def test_long_text_truncated(self):
        text = "x" * 5000
        result = _tail(text, 100)
        self.assertIn("[truncated]", result)
        self.assertLessEqual(len(result), 200)


class TestSummarizeError(unittest.TestCase):
    def test_finds_error_line(self):
        text = "compiling foo\nERROR: cannot find symbol\nmore output"
        self.assertIn("cannot find symbol", _summarize_error(text))

    def test_falls_back_to_first_line(self):
        text = "build failed for unknown reasons"
        self.assertEqual(_summarize_error(text),
                         "build failed for unknown reasons")

    def test_empty_input(self):
        self.assertEqual(_summarize_error(""), "build failed (no error output)")


class TestFindStrategy(unittest.TestCase):
    def test_finds_named_strategy(self):
        record = {
            "strategies": [
                {"strategy_name": "zero_shot", "x": 1},
                {"strategy_name": "few_shot_retrieval", "x": 2},
            ]
        }
        s = _find_strategy(record, "few_shot_retrieval")
        self.assertEqual(s["x"], 2)

    def test_returns_none_when_missing(self):
        record = {"strategies": [{"strategy_name": "zero_shot"}]}
        self.assertIsNone(_find_strategy(record, "nope"))


class TestValidateRefactorRecordsEdgeCases(unittest.TestCase):
    def test_empty_records(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            self.assertEqual(
                validate_refactor_records([], tmpdir, tmpdir, log_to_feedback=False),
                [],
            )

    def test_record_with_no_best_strategy(self):
        record = {
            "issue": {"issue_id": "x", "file_relative": "Foo.java"},
            "best_strategy": None,
            "strategies": [],
        }
        with tempfile.TemporaryDirectory() as tmpdir:
            results = validate_refactor_records(
                [record], tmpdir, tmpdir, log_to_feedback=False,
            )
            self.assertEqual(len(results), 1)
            self.assertTrue(results[0]["skipped"])
            self.assertIn("no best strategy", results[0]["skip_reason"])


COMMONS_LANG = "/data/production/spikes/q1_agent_on_real_code/commons-lang"


class TestValidateIntegration(unittest.TestCase):
    """Stage 1 -> 2 -> 4 -> 5 -> 6 -> 7 on commons-lang3."""

    def test_full_pipeline_compile_only(self):
        if not Path(COMMONS_LANG).exists():
            self.skipTest("commons-lang3 not available")
        if not Path("/data/production/data/fault_predictor.pkl").exists():
            self.skipTest("fault predictor model not available")

        from production.stages.ingest import ingest_repository
        from production.stages.analyze import analyze_repository
        from production.stages.predict import predict_fault_probability
        from production.stages.prioritize import prioritize_issues
        from production.stages.refactor import refactor_top_issues

        result = ingest_repository(COMMONS_LANG)
        issues = analyze_repository(result["java_source_root"])
        predict_fault_probability(
            issues, result["repo_root"], result["java_source_root"]
        )
        prioritize_issues(issues)

        records = refactor_top_issues(
            ranked_issues=issues,
            repo_root=result["repo_root"],
            n=1,
            max_per_file=1,
            strategies=("zero_shot",),
            log_to_feedback=False,
            repo_name="commons-lang",
        )

        validations = validate_refactor_records(
            records=records,
            repo_root=result["repo_root"],
            java_source_root=result["java_source_root"],
            repo_name="commons-lang",
            run_tests=False,
            timeout_seconds=300,
            log_to_feedback=False,
        )

        self.assertEqual(len(validations), 1)
        v = validations[0]
        # Maven build system should be detected.
        if not v.get("skipped"):
            self.assertEqual(v["build_system"], "maven")
            self.assertIsNotNone(v["target"])
            # Either succeeded or has an error summary (not crashed).
            if not v["succeeded"]:
                self.assertIsNotNone(v["error_summary"])


if __name__ == "__main__":
    unittest.main()