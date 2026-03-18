"""
Configuration for pytest in msml610/test directory.
"""

import sys

# Add helpers_root to Python path for imports.
import os

test_dir = os.path.dirname(__file__)
msml610_dir = os.path.dirname(test_dir)
project_root = os.path.dirname(msml610_dir)
helpers_root = os.path.join(project_root, "helpers_root")

if helpers_root not in sys.path:
    sys.path.insert(0, helpers_root)

if project_root not in sys.path:
    sys.path.insert(0, project_root)
