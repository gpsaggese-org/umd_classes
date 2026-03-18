"""
Conftest for class_project tests.

Skips tests when required dependencies are not available.
"""

import pytest

# TODO(ai_gp): This should just skip in general.
pytest.importorskip("tutorial_class_project_instructions")
