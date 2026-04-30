"""Tests for production.scripts.run_pipeline."""

import sys
import unittest
from pathlib import Path

# Make production package importable.
sys.path.insert(0, "/data")


class TestRunPipelineImports(unittest.TestCase):
    def test_module_imports(self):
        """Verify the runner module can be imported without error."""
        from production.scripts import run_pipeline
        self.assertTrue(hasattr(run_pipeline, "main"))

    def test_help_runs_without_crash(self):
        """Verify --help works (validates arg parser is well-formed)."""
        import subprocess
        result = subprocess.run(
            ["python", "/data/production/scripts/run_pipeline.py", "--help"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        self.assertEqual(result.returncode, 0)
        self.assertIn("repo", result.stdout)
        self.assertIn("top", result.stdout)


if __name__ == "__main__":
    unittest.main()