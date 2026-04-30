"""Tests for production.stages.refactor."""

import os
import tempfile
import unittest
from pathlib import Path

# Make production package importable.

from production.stages.refactor import (
    _select_top_issues,
    _extract_method_source,
    _find_method_end,
    _slice_lines,
    _check_signature_preserved,
    _extract_signature,
    _extract_java_from_response,
    _strip_leading_imports,
    _produce_diff,
    _pick_best,
)


# ---------------------------------------------------------------------------
# Tests that don't need the agent.
# ---------------------------------------------------------------------------


class TestSelectTopIssues(unittest.TestCase):
    def test_basic_top_n(self):
        issues = [
            {"file_path": "/a", "id": 1},
            {"file_path": "/b", "id": 2},
            {"file_path": "/c", "id": 3},
        ]
        result = _select_top_issues(issues, n=2, max_per_file=None)
        self.assertEqual([i["id"] for i in result], [1, 2])

    def test_max_per_file_caps(self):
        issues = [
            {"file_path": "/a", "id": 1},
            {"file_path": "/a", "id": 2},
            {"file_path": "/b", "id": 3},
        ]
        result = _select_top_issues(issues, n=10, max_per_file=1)
        self.assertEqual([i["id"] for i in result], [1, 3])


class TestSliceLines(unittest.TestCase):
    def test_basic(self):
        text = "a\nb\nc\nd\ne"
        self.assertEqual(_slice_lines(text, 2, 4), "b\nc\nd")


class TestFindMethodEnd(unittest.TestCase):
    def test_simple_method(self):
        text = (
            "class Foo {\n"
            "    public int bar() {\n"
            "        return 1;\n"
            "    }\n"
            "}\n"
        )
        # Method starts at line 2.
        self.assertEqual(_find_method_end(text, 2), 4)

    def test_nested_braces(self):
        text = (
            "class Foo {\n"
            "    public int bar() {\n"
            "        if (true) {\n"
            "            return 1;\n"
            "        }\n"
            "        return 0;\n"
            "    }\n"
            "}\n"
        )
        self.assertEqual(_find_method_end(text, 2), 7)

    def test_braces_inside_strings_ignored(self):
        text = (
            "public void foo() {\n"
            '    String s = "{not a real brace}";\n'
            "    return;\n"
            "}\n"
        )
        self.assertEqual(_find_method_end(text, 1), 4)

    def test_braces_inside_comments_ignored(self):
        text = (
            "public void foo() {\n"
            "    // { also not real\n"
            "    /* { still not */\n"
            "    return;\n"
            "}\n"
        )
        self.assertEqual(_find_method_end(text, 1), 5)


class TestExtractMethodSource(unittest.TestCase):
    def test_finds_method_containing_line(self):
        text = (
            "public class Foo {\n"
            "    public int bar() {\n"      # line 2
            "        return 1;\n"            # line 3
            "    }\n"                        # line 4
            "    public int baz() {\n"       # line 5
            "        return 2;\n"            # line 6
            "    }\n"                        # line 7
            "}\n"
        )
        result = _extract_method_source(text, 6)
        self.assertIsNotNone(result)
        self.assertEqual(result["method_name"], "baz")
        self.assertEqual(result["start_line"], 5)
        self.assertEqual(result["end_line"], 7)
        self.assertIn("return 2", result["source"])

    def test_returns_none_for_unparseable(self):
        text = "this is not valid java"
        self.assertIsNone(_extract_method_source(text, 1))


class TestSignaturePreservation(unittest.TestCase):
    def test_signature_preserved(self):
        original = (
            "public int add(int a, int b) {\n"
            "    return a + b;\n"
            "}"
        )
        refactored = (
            "public int add(int a, int b) {\n"
            "    return Math.addExact(a, b);\n"
            "}"
        )
        self.assertTrue(_check_signature_preserved(original, refactored))

    def test_signature_changed_param_names_dont_matter(self):
        original = (
            "public int add(int a, int b) { return a + b; }"
        )
        refactored = (
            "public int add(int x, int y) { return x + y; }"
        )
        # Param names differ, but types are the same.
        self.assertTrue(_check_signature_preserved(original, refactored))

    def test_signature_changed_param_count(self):
        original = (
            "public int add(int a, int b) { return a + b; }"
        )
        refactored = (
            "public int add(int a, int b, int c) { return a + b + c; }"
        )
        self.assertFalse(_check_signature_preserved(original, refactored))

    def test_signature_changed_method_name(self):
        original = "public int add(int a, int b) { return a + b; }"
        refactored = "public int sum(int a, int b) { return a + b; }"
        self.assertFalse(_check_signature_preserved(original, refactored))


class TestExtractJavaFromResponse(unittest.TestCase):
    def test_no_fences(self):
        text = "public int foo() { return 1; }"
        self.assertEqual(_extract_java_from_response(text), text)

    def test_java_fence(self):
        text = "```java\npublic int foo() { return 1; }\n```"
        self.assertEqual(
            _extract_java_from_response(text),
            "public int foo() { return 1; }",
        )

    def test_lone_closing_fence(self):
        # The Q1 spike bug: fence at end with no opening fence.
        text = "public int foo() { return 1; }\n```"
        self.assertEqual(
            _extract_java_from_response(text),
            "public int foo() { return 1; }",
        )

    def test_strips_leading_imports(self):
        text = (
            "import java.util.List;\n"
            "import java.util.Map;\n"
            "\n"
            "public int foo() { return 1; }"
        )
        self.assertEqual(
            _extract_java_from_response(text),
            "public int foo() { return 1; }",
        )


class TestProduceDiff(unittest.TestCase):
    def test_diff_shows_change(self):
        original = "int x = 1;\nreturn x;\n"
        refactored = "int x = 2;\nreturn x;\n"
        diff = _produce_diff(original, refactored, "Foo.java")
        self.assertIn("-int x = 1;", diff)
        self.assertIn("+int x = 2;", diff)


class TestPickBest(unittest.TestCase):
    def _strategy(self, name, level, score, signature_preserved=True):
        return {
            "strategy_name": name,
            "confidence": {"level": level, "score": score},
            "signature_preserved": signature_preserved,
        }

    def test_picks_highest_score(self):
        results = [
            self._strategy("zero_shot", "MEDIUM", 0.5),
            self._strategy("few_shot_retrieval", "HIGH", 0.9),
        ]
        best = _pick_best(results)
        self.assertEqual(best["strategy_name"], "few_shot_retrieval")

    def test_skips_failed(self):
        results = [
            self._strategy("zero_shot", "FAILED", 0.0),
            self._strategy("few_shot_retrieval", "MEDIUM", 0.5),
        ]
        best = _pick_best(results)
        self.assertEqual(best["strategy_name"], "few_shot_retrieval")

    def test_all_failed_returns_none(self):
        results = [
            self._strategy("zero_shot", "FAILED", 0.0),
            self._strategy("few_shot_retrieval", "FAILED", 0.0),
        ]
        self.assertIsNone(_pick_best(results))

    def test_skips_signature_changes(self):
        results = [
            self._strategy("zero_shot", "HIGH", 0.9, signature_preserved=False),
            self._strategy("few_shot_retrieval", "MEDIUM", 0.5,
                           signature_preserved=True),
        ]
        best = _pick_best(results)
        self.assertEqual(best["strategy_name"], "few_shot_retrieval")

    def test_all_changed_signature_returns_none(self):
        results = [
            self._strategy("zero_shot", "HIGH", 0.9, signature_preserved=False),
            self._strategy("few_shot_retrieval", "MEDIUM", 0.5,
                           signature_preserved=False),
        ]
        self.assertIsNone(_pick_best(results))


# ---------------------------------------------------------------------------
# Integration test that runs the full Stage 6 pipeline.
# Marked slow; uses small N to keep total runtime around 30-60 seconds.
# ---------------------------------------------------------------------------


COMMONS_LANG_REPO = (
    "/data/production/spikes/q1_agent_on_real_code/commons-lang"
)
MODEL_PATH = "/data/production/data/fault_predictor.pkl"


class TestRefactorIntegration(unittest.TestCase):
    """End-to-end: Stage 1 -> 2 -> 4 -> 5 -> 6 on commons-lang3."""

    def test_full_pipeline_one_issue(self):
        if not Path(COMMONS_LANG_REPO).exists():
            self.skipTest("commons-lang3 not available")
        if not Path(MODEL_PATH).exists():
            self.skipTest("fault predictor model not available")

        from production.stages.ingest import ingest_repository
        from production.stages.analyze import analyze_repository
        from production.stages.predict import predict_fault_probability
        from production.stages.prioritize import prioritize_issues
        from production.stages.refactor import refactor_top_issues

        result = ingest_repository(COMMONS_LANG_REPO)
        issues = analyze_repository(result["java_source_root"])
        predict_fault_probability(
            issues, result["repo_root"], result["java_source_root"]
        )
        prioritize_issues(issues)

        # Just one issue, both strategies, to keep the test in a few minutes.
        records = refactor_top_issues(
            ranked_issues=issues,
            repo_root=result["repo_root"],
            n=1,
            max_per_file=1,
            strategies=("zero_shot", "few_shot_retrieval"),
            log_to_feedback=False,
            repo_name="commons-lang",
        )

        self.assertEqual(len(records), 1)
        record = records[0]
        # Either we extracted a method and ran strategies, or we have an
        # error explaining why we couldn't.
        self.assertIn("error", record)
        if record["error"] is None:
            self.assertEqual(len(record["strategies"]), 2)
            for s in record["strategies"]:
                self.assertIn("strategy_name", s)
                self.assertIn("confidence", s)
                self.assertIn("diff", s)

class TestSaveAndLoadRecords(unittest.TestCase):
    def _sample_records(self):
        return [
            {
                "issue": {
                    "rule": "TestRule",
                    "file_path": "/x/Foo.java",
                    "begin_line": 1,
                    "fault_probability": 0.5,
                    "_extraction": "should be stripped",
                },
                "method_source": "void foo() {}",
                "method_start_line": 1,
                "method_end_line": 1,
                "method_name": "foo",
                "strategies": [
                    {
                        "strategy_name": "zero_shot",
                        "generated_raw": "void foo() {}",
                        "generated_clean": "void foo() {}",
                        "is_valid_java": True,
                        "syntax_error": None,
                        "signature_preserved": True,
                        "bleu_vs_input": 100.0,
                        "exact_match_vs_input": True,
                        "confidence": {"level": "HIGH", "score": 0.9},
                        "diff": "",
                        "elapsed_s": 1.5,
                        "retrieved_count": 0,
                        "retrieved_similarities": [],
                    }
                ],
                "best_strategy": "zero_shot",
                "error": None,
            }
        ]

    def test_save_and_load_round_trip(self):
        from production.stages.refactor import (
            save_refactor_records, load_refactor_records,
        )
        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "records.json")
            records = self._sample_records()
            save_refactor_records(
                records,
                output_path=path,
                model_name="test/model",
                repo_name="test-repo",
                strategies=("zero_shot",),
            )
            self.assertTrue(os.path.exists(path))
            loaded = load_refactor_records(path)
            self.assertEqual(len(loaded["records"]), 1)
            self.assertEqual(loaded["model_name"], "test/model")
            self.assertEqual(loaded["repo_name"], "test-repo")

    def test_extraction_field_stripped_on_save(self):
        from production.stages.refactor import (
            save_refactor_records, load_refactor_records,
        )
        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "records.json")
            records = self._sample_records()
            self.assertIn("_extraction", records[0]["issue"])
            save_refactor_records(
                records, output_path=path,
                model_name="test/model",
            )
            loaded = load_refactor_records(path)
            self.assertNotIn("_extraction", loaded["records"][0]["issue"])

    def test_load_missing_file_raises(self):
        from production.stages.refactor import load_refactor_records
        with self.assertRaises(FileNotFoundError):
            load_refactor_records("/nonexistent/path.json")

    def test_load_invalid_json_raises(self):
        from production.stages.refactor import load_refactor_records
        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "bad.json")
            with open(path, "w") as f:
                f.write('"just a string"')
            with self.assertRaises(ValueError):
                load_refactor_records(path)

class TestSaveAndLoadIssues(unittest.TestCase):
    def _sample_issues(self):
        return [
            {
                "issue_id": "abc",
                "rule": "TestRule",
                "ruleset": "Best Practices",
                "priority": 3,
                "file_path": "/origin/path/Foo.java",
                "file_relative": "Foo.java",
                "begin_line": 42,
                "fault_probability": 0.5,
                "host_commit": "deadbeef",
                "score": 0.02,
                "priority_rank": 1,
                "_extraction": "should be stripped",
            }
        ]

    def test_save_and_load_round_trip(self):
        from production.stages.refactor import (
            save_ranked_issues, load_ranked_issues,
        )
        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "issues.json")
            save_ranked_issues(
                self._sample_issues(),
                output_path=path,
                repo_root="/some/repo",
                java_source_root="/some/repo/src/main/java",
                repo_name="test-repo",
            )
            envelope = load_ranked_issues(path)
            self.assertEqual(len(envelope["issues"]), 1)
            self.assertEqual(envelope["repo_name"], "test-repo")
            self.assertEqual(
                envelope["repo_root_on_origin"], "/some/repo"
            )
            self.assertEqual(
                envelope["java_source_root_on_origin"],
                "/some/repo/src/main/java",
            )

    def test_extraction_field_stripped(self):
        from production.stages.refactor import (
            save_ranked_issues, load_ranked_issues,
        )
        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "issues.json")
            save_ranked_issues(
                self._sample_issues(),
                output_path=path,
                repo_root="/some/repo",
                java_source_root="/some/repo/src",
            )
            envelope = load_ranked_issues(path)
            self.assertNotIn("_extraction", envelope["issues"][0])

    def test_derived_fields_preserved(self):
        from production.stages.refactor import (
            save_ranked_issues, load_ranked_issues,
        )
        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "issues.json")
            save_ranked_issues(
                self._sample_issues(),
                output_path=path,
                repo_root="/some/repo",
                java_source_root="/some/repo/src",
            )
            envelope = load_ranked_issues(path)
            issue = envelope["issues"][0]
            self.assertEqual(issue["fault_probability"], 0.5)
            self.assertEqual(issue["score"], 0.02)
            self.assertEqual(issue["priority_rank"], 1)
            self.assertEqual(issue["host_commit"], "deadbeef")

    def test_load_missing_file_raises(self):
        from production.stages.refactor import load_ranked_issues
        with self.assertRaises(FileNotFoundError):
            load_ranked_issues("/nonexistent/issues.json")
            
if __name__ == "__main__":
    unittest.main()