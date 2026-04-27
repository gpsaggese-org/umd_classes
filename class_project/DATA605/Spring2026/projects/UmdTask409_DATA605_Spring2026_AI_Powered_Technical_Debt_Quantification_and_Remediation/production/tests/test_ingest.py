"""Tests for production.stages.ingest."""

import os
import sys
import tempfile
import unittest
from pathlib import Path

# Make production package importable.
sys.path.insert(0, "/data")

from production.stages.ingest import (
    ingest_repository,
    _is_url,
    _extract_repo_name,
    _find_java_source_root,
)

COMMONS_LANG_PATH = (
    "/data/production/spikes/q1_agent_on_real_code/commons-lang"
)


class TestIsUrl(unittest.TestCase):
    def test_https_url(self):
        self.assertTrue(_is_url("https://github.com/apache/commons-lang.git"))

    def test_http_url(self):
        self.assertTrue(_is_url("http://github.com/apache/commons-lang.git"))

    def test_git_at_url(self):
        self.assertTrue(_is_url("git@github.com:apache/commons-lang.git"))

    def test_ssh_url(self):
        self.assertTrue(
            _is_url("ssh://git@github.com/apache/commons-lang.git")
        )

    def test_absolute_path_is_not_url(self):
        self.assertFalse(
            _is_url("/data/production/spikes/q1_agent_on_real_code/commons-lang")
        )

    def test_relative_path_is_not_url(self):
        self.assertFalse(_is_url("relative/path/to/repo"))

    def test_plain_name_is_not_url(self):
        self.assertFalse(_is_url("commons-lang"))


class TestExtractRepoName(unittest.TestCase):
    def test_https_with_git_suffix(self):
        name = _extract_repo_name(
            "https://github.com/apache/commons-lang.git"
        )
        self.assertEqual(name, "commons-lang")

    def test_https_without_git_suffix(self):
        name = _extract_repo_name(
            "https://github.com/apache/commons-lang"
        )
        self.assertEqual(name, "commons-lang")

    def test_git_at_url(self):
        name = _extract_repo_name(
            "git@github.com:apache/commons-lang.git"
        )
        self.assertEqual(name, "commons-lang")

    def test_local_path(self):
        name = _extract_repo_name(
            "/data/production/spikes/q1_agent_on_real_code/commons-lang"
        )
        self.assertEqual(name, "commons-lang")

    def test_local_path_trailing_slash(self):
        name = _extract_repo_name(
            "/data/production/spikes/q1_agent_on_real_code/commons-lang/"
        )
        self.assertEqual(name, "commons-lang")


class TestFindJavaSourceRoot(unittest.TestCase):
    def test_standard_maven_layout(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            java_dir = Path(tmpdir) / "src" / "main" / "java"
            java_dir.mkdir(parents=True)
            (java_dir / "Foo.java").write_text("public class Foo {}")
            result = _find_java_source_root(tmpdir)
            self.assertEqual(result, str(java_dir.resolve()))

    def test_nested_module_layout(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            java_dir = (
                Path(tmpdir) / "module-core" / "src" / "main" / "java"
            )
            java_dir.mkdir(parents=True)
            (java_dir / "Bar.java").write_text("public class Bar {}")
            result = _find_java_source_root(tmpdir)
            self.assertEqual(result, str(java_dir.resolve()))

    def test_raises_when_no_java_source_root(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            with self.assertRaises(RuntimeError) as ctx:
                _find_java_source_root(tmpdir)
            self.assertIn("No Java source root found", str(ctx.exception))


class TestIngestLocalPath(unittest.TestCase):
    def test_ingest_commons_lang(self):
        if not Path(COMMONS_LANG_PATH).exists():
            self.skipTest(
                "commons-lang clone not available at " + COMMONS_LANG_PATH
            )
        result = ingest_repository(COMMONS_LANG_PATH)
        self.assertFalse(result["was_cloned"])
        self.assertEqual(
            result["repo_root"], os.path.realpath(COMMONS_LANG_PATH)
        )
        self.assertTrue(
            result["java_source_root"].endswith("src/main/java"),
            f"Expected java_source_root to end in src/main/java, "
            f"got: {result['java_source_root']}",
        )
        self.assertEqual(result["repo_name"], "commons-lang")
        self.assertEqual(result["source_input"], COMMONS_LANG_PATH)

    def test_ingest_local_result_keys(self):
        if not Path(COMMONS_LANG_PATH).exists():
            self.skipTest(
                "commons-lang clone not available at " + COMMONS_LANG_PATH
            )
        result = ingest_repository(COMMONS_LANG_PATH)
        expected_keys = {
            "repo_root",
            "java_source_root",
            "source_input",
            "was_cloned",
            "repo_name",
        }
        self.assertEqual(set(result.keys()), expected_keys)


class TestIngestExplicitJavaSourceSubpath(unittest.TestCase):
    def test_explicit_subpath(self):
        if not Path(COMMONS_LANG_PATH).exists():
            self.skipTest(
                "commons-lang clone not available at " + COMMONS_LANG_PATH
            )
        result = ingest_repository(
            COMMONS_LANG_PATH,
            java_source_subpath="src/main/java",
        )
        expected = os.path.realpath(
            os.path.join(COMMONS_LANG_PATH, "src", "main", "java")
        )

        self.assertEqual(result["java_source_root"], expected)
        self.assertFalse(result["was_cloned"])


class TestIngestNonexistentLocalPath(unittest.TestCase):
    def test_nonexistent_path_raises_file_not_found(self):
        fake_path = "/this/path/does/not/exist/at/all"
        with self.assertRaises(FileNotFoundError) as ctx:
            ingest_repository(fake_path)
        self.assertIn("does not exist", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
