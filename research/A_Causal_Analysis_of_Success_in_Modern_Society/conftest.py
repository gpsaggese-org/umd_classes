"""
Configure pytensor to use Python backend to avoid C compilation issues on macOS.
"""

import platform

# Disable C compilation to avoid linker errors on macOS with ld64.
if platform.system() == "Darwin":
    try:
        import pytensor

        pytensor.config.cxx = ""
    except ImportError:
        pass
