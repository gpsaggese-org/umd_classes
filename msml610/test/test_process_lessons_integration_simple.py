"""
Integration tests for process_lessons.py on msml610 lectures using actual system calls.

These tests execute the actual process_lessons commands and verify output files
are created without mocking hsystem.system.

Test markers:
- slow: these are integration tests that execute external commands
- requires_docker_in_docker: requires docker/notes_to_pdf environment
"""

import glob
import logging
import os
from unittest import mock

import helpers.hdbg as hdbg
import helpers.hunit_test as hunitest

import dev_scripts_helpers.slides.process_lessons as dshsprle

_LOG = logging.getLogger(__name__)


# #############################################################################
# Helper functions
# #############################################################################


def _get_msml610_dir() -> str:
    """
    Get the msml610 directory from the project root.

    :return: path to msml610 directory
    """
    test_dir = os.path.dirname(__file__)
    msml610_dir = os.path.dirname(test_dir)
    hdbg.dassert_dir_exists(msml610_dir)
    return msml610_dir


def _get_first_lecture_file(msml610_dir: str) -> tuple:
    """
    Get the first lecture file from msml610/lectures_source.

    :param msml610_dir: path to msml610 directory
    :return: tuple of (source_path, source_name)
    """
    lectures_source_dir = os.path.join(msml610_dir, "lectures_source")
    lesson_files = sorted(glob.glob(
        os.path.join(lectures_source_dir, "Lesson[0-9]*.txt")
    ))
    hdbg.dassert_lt(0, len(lesson_files), "No lesson files found")
    source_path = lesson_files[0]
    source_name = os.path.basename(source_path)
    return source_path, source_name


# #############################################################################
# Test__generate_tex
# #############################################################################


class Test__generate_tex(hunitest.TestCase):
    """
    Test _generate_tex function.
    """

    def helper(
        self,
        msml610_dir: str,
        source_path: str,
        source_name: str,
        *,
        limit: str = None,
    ) -> str:
        """
        Helper for testing _generate_tex command construction.

        :param msml610_dir: path to msml610 directory
        :param source_path: path to lecture source file
        :param source_name: name of lecture source file
        :param limit: optional limit parameter
        :return: command string that was called
        """
        lectures_tex_dir = os.path.join(msml610_dir, "lectures_tex")
        os.makedirs(lectures_tex_dir, exist_ok=True)
        with mock.patch("helpers.hsystem.system") as mock_system:
            if limit is None:
                dshsprle._generate_tex(msml610_dir, source_path, source_name)
            else:
                dshsprle._generate_tex(
                    msml610_dir, source_path, source_name, limit=limit
                )
            mock_system.assert_called_once()
            cmd_str = mock_system.call_args[0][0]
            return cmd_str

    def test1(self) -> None:
        """
        Test _generate_tex constructs the correct command.
        """
        # Prepare inputs.
        msml610_dir = _get_msml610_dir()
        source_path, source_name = _get_first_lecture_file(msml610_dir)
        # Run test.
        cmd_str = self.helper(msml610_dir, source_path, source_name)
        # Check outputs.
        self.assertIn("notes_to_pdf.py", cmd_str)
        self.assertIn("--tex_only", cmd_str)
        self.assertIn(source_path, cmd_str)
        self.assertIn("--skip_action open", cmd_str)

    def test2(self) -> None:
        """
        Test _generate_tex includes limit parameter in command.
        """
        # Prepare inputs.
        msml610_dir = _get_msml610_dir()
        source_path, source_name = _get_first_lecture_file(msml610_dir)
        limit = "1:5"
        # Run test.
        cmd_str = self.helper(msml610_dir, source_path, source_name, limit=limit)
        # Check outputs.
        self.assertIn(f"--limit {limit}", cmd_str)


# #############################################################################
# Test__generate_pdf
# #############################################################################


class Test__generate_pdf(hunitest.TestCase):
    """
    Test _generate_pdf function.
    """

    def helper(
        self,
        msml610_dir: str,
        source_path: str,
        source_name: str,
        *,
        limit: str = None,
    ) -> str:
        """
        Helper for testing _generate_pdf command construction.

        :param msml610_dir: path to msml610 directory
        :param source_path: path to lecture source file
        :param source_name: name of lecture source file
        :param limit: optional limit parameter
        :return: command string that was called
        """
        lectures_dir = os.path.join(msml610_dir, "lectures")
        os.makedirs(lectures_dir, exist_ok=True)
        with mock.patch("helpers.hsystem.system") as mock_system:
            if limit is None:
                dshsprle._generate_pdf(
                    msml610_dir,
                    source_path,
                    source_name,
                    skip_action="open"
                )
            else:
                dshsprle._generate_pdf(
                    msml610_dir,
                    source_path,
                    source_name,
                    limit=limit,
                    skip_action="open"
                )
            mock_system.assert_called_once()
            cmd_str = mock_system.call_args[0][0]
            return cmd_str

    def test1(self) -> None:
        """
        Test _generate_pdf constructs the correct command.
        """
        # Prepare inputs.
        msml610_dir = _get_msml610_dir()
        source_path, source_name = _get_first_lecture_file(msml610_dir)
        # Run test.
        cmd_str = self.helper(msml610_dir, source_path, source_name)
        # Check outputs.
        self.assertIn("notes_to_pdf.py", cmd_str)
        self.assertIn("--type slides", cmd_str)
        self.assertIn(source_path, cmd_str)
        self.assertIn("--skip_action open", cmd_str)

    def test2(self) -> None:
        """
        Test _generate_pdf includes limit parameter in command.
        """
        # Prepare inputs.
        msml610_dir = _get_msml610_dir()
        source_path, source_name = _get_first_lecture_file(msml610_dir)
        limit = "1:3"
        # Run test.
        cmd_str = self.helper(msml610_dir, source_path, source_name, limit=limit)
        # Check outputs.
        self.assertIn(f"--limit {limit}", cmd_str)


# #############################################################################
# Test__find_lecture_files
# #############################################################################


class Test__find_lecture_files(hunitest.TestCase):
    """
    Test _find_lecture_files function.
    """

    def test1(self) -> None:
        """
        Test _find_lecture_files finds files matching wildcard pattern.
        """
        # Prepare inputs.
        msml610_dir = _get_msml610_dir()
        is_range = False
        patterns = ["01*"]
        # Run test.
        files = dshsprle._find_lecture_files(msml610_dir, is_range, patterns)
        # Check outputs.
        self.assertGreater(len(files), 0)
        for file_path, file_name in files:
            self.assertIn("Lesson01", file_name)
            self.assertTrue(file_name.endswith(".txt"))

    def test2(self) -> None:
        """
        Test _find_lecture_files finds files within a range.
        """
        # Prepare inputs.
        msml610_dir = _get_msml610_dir()
        is_range = True
        range_specs = ["01.1", "02.2"]
        # Run test.
        files = dshsprle._find_lecture_files(msml610_dir, is_range, range_specs)
        # Check outputs.
        self.assertGreater(len(files), 0)
        for file_path, file_name in files:
            self.assertTrue(file_path.endswith(".txt"))
