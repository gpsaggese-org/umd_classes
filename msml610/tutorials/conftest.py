"""
Configuration for pytest in msml610/tutorials directory.
"""

import logging
import os
import sys
from typing import Any

# Add helpers_root to Python path for imports.
test_dir = os.path.dirname(__file__)
msml610_dir = os.path.dirname(test_dir)
project_root = os.path.dirname(msml610_dir)
helpers_root = os.path.join(project_root, "helpers_root")

if helpers_root not in sys.path:
    sys.path.insert(0, helpers_root)

if project_root not in sys.path:
    sys.path.insert(0, project_root)

import helpers.hdbg as dbg
import helpers.hunit_test as hut

# Define fixture at module level to ensure it's always registered.
import pytest


@pytest.fixture(autouse=True)
def populate_globals(capsys: Any) -> None:
    """
    Populate global capsys for pytest output capture.
    """
    hut._GLOBAL_CAPSYS = capsys


# Hack to workaround pytest not happy with multiple redundant conftest.py
# (bug #34).
if not hasattr(hut, "_CONFTEST_ALREADY_PARSED"):
    # pylint: disable=protected-access
    hut._CONFTEST_ALREADY_PARSED = True

    # Store whether we are running unit test through pytest.
    # pylint: disable=line-too-long
    # From https://docs.pytest.org/en/latest/example/simple.html#detect-if-running-from-within-a-pytest-run
    def pytest_configure(config: Any) -> None:
        _ = config
        # pylint: disable=protected-access
        hut._CONFTEST_IN_PYTEST = True

    def pytest_unconfigure(config: Any) -> None:
        _ = config
        # pylint: disable=protected-access
        hut._CONFTEST_IN_PYTEST = False

    # Add custom options.
    def pytest_addoption(parser: Any) -> None:
        parser.addoption(
            "--update_outcomes",
            action="store_true",
            default=False,
            help="Update golden outcomes of test",
        )
        parser.addoption(
            "--incremental",
            action="store_true",
            default=False,
            help="Reuse and not clean up test artifacts",
        )
        parser.addoption(
            "--dbg_verbosity",
            dest="log_level",
            choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
            help="Set the logging level",
        )
        parser.addoption(
            "--dbg",
            action="store_true",
            help="Set the logging level to TRACE",
        )

    def pytest_collection_modifyitems(config: Any, items: Any) -> None:
        _ = items
        import helpers.henv as henv

        _WARNING = "\033[33mWARNING\033[0m"
        try:
            print(henv.get_system_signature()[0])
        except Exception:
            print(f"\n{_WARNING}: Can't print system_signature")
        if config.getoption("--update_outcomes"):
            print(f"\n{_WARNING}: Updating test outcomes")
            hut.set_update_tests(True)
        if config.getoption("--incremental"):
            print(f"\n{_WARNING}: Using incremental test mode")
            hut.set_incremental_tests(True)
        # Set the verbosity level.
        level = logging.INFO
        if config.getoption("--dbg_verbosity", None) or config.getoption(
            "--dbg", None
        ):
            if config.getoption("--dbg_verbosity", None):
                level = config.getoption("--dbg_verbosity")
            elif config.getoption("--dbg", None):
                # Use 5 as fallback TRACE level.
                level = getattr(logging, "TRACE", 5)
            else:
                raise ValueError("Can't get here")
            print(f"\n{_WARNING}: Setting verbosity level to {level}")
            # When we specify the debug verbosity we monkey patch the command
            # line to add the '-s' option to pytest to not suppress the output.
            # NOTE: monkey patching sys.argv is often fragile.
            import sys

            sys.argv.append("-s")
            sys.argv.append("-o log_cli=true")
        # TODO(gp): redirect also the stderr to file.
        dbg.init_logger(level, in_pytest=True, log_filename="tmp.pytest.log")
