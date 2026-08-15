"""
Unit tests for the txtai embeddings helpers.

Covers ``get_data_dir`` env-var override and on-demand directory creation.
The expensive paths (model load, index build) are not exercised here because
they require sentence-transformers and an actual index on disk.
"""

import os
import tempfile
import unittest
from pathlib import Path

from app.pipeline.embeddings import get_data_dir


# #############################################################################
# Test_get_data_dir
# #############################################################################


class Test_get_data_dir(unittest.TestCase):
    """
    Test that ``get_data_dir`` honors ``TXTAI_DATA_DIR`` and creates the path.
    """

    def test1(self) -> None:
        """
        Env override returns the requested directory and creates it.
        """
        # Prepare inputs.
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "txtai_test_data"
            old = os.environ.get("TXTAI_DATA_DIR")
            os.environ["TXTAI_DATA_DIR"] = str(target)
            try:
                # Run test.
                out = get_data_dir()
                # Check outputs.
                self.assertEqual(out, target)
                self.assertTrue(out.exists())
                self.assertTrue(out.is_dir())
            finally:
                if old is None:
                    os.environ.pop("TXTAI_DATA_DIR", None)
                else:
                    os.environ["TXTAI_DATA_DIR"] = old


if __name__ == "__main__":
    unittest.main()
