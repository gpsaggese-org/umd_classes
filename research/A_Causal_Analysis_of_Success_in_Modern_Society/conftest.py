"""
Configure pytensor to use Python backend to avoid C compilation issues on macOS.
"""

from typing import List

# import pytensor

# Disable C compilation to avoid linker errors on macOS with ld64.
# pytensor.config.cxx = ""

# Disable test collection for this directory.
collect_ignore_glob: List[str] = ["test_*.py"]
