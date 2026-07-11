"""
Unit tests for count_words.py.

Import as:

import class_scripts.test.test_count_words as csttcwds
"""

# TODO(gp): Make sure this file follows our unit test conventions

import os
from pathlib import Path
from unittest import mock

import helpers.hio as hio
import helpers.hunit_test as hunitest

import class_scripts.count_words as clcowoor


# #############################################################################
# Test_parse
# #############################################################################


class Test_parse(hunitest.TestCase):
    """
    Test `_parse()` function.
    """

    def test1(self) -> None:
        """
        Test parser accepts the positional `dir` argument.
        """
        # Prepare inputs.
        arg_list = ["msml610"]
        # Prepare outputs.
        expected = "msml610"
        # Run test.
        parser = clcowoor._parse()
        args = parser.parse_args(arg_list)
        # Check outputs.
        self.assert_equal(args.dir, expected)


# #############################################################################
# Test__count_words_in_file
# #############################################################################


class Test__count_words_in_file(hunitest.TestCase):
    """
    Test `_count_words_in_file()` function.
    """

    def test1(self) -> None:
        """
        Test happy path: counts words separated by whitespace.
        """
        # Prepare inputs.
        scratch_dir = self.get_scratch_space()
        file_path = os.path.join(scratch_dir, "script.txt")
        hio.to_file(file_path, "one two three four")
        # Prepare outputs.
        expected = 4
        # Run test.
        actual = clcowoor._count_words_in_file(Path(file_path))
        # Check outputs.
        self.assertEqual(actual, expected)

    def test2(self) -> None:
        """
        Test edge case: empty file has zero words.
        """
        # Prepare inputs.
        scratch_dir = self.get_scratch_space()
        file_path = os.path.join(scratch_dir, "empty.txt")
        hio.to_file(file_path, "")
        # Prepare outputs.
        expected = 0
        # Run test.
        actual = clcowoor._count_words_in_file(Path(file_path))
        # Check outputs.
        self.assertEqual(actual, expected)


# #############################################################################
# Test_main
# #############################################################################


class Test_main(hunitest.TestCase):
    """
    Test `_main()` function.
    """

    def test1(self) -> None:
        """
        Test happy path: logs word counts for each file in the
        `lectures_video_script/` directory, sorted by filename.
        """
        # Prepare inputs.
        scratch_dir = self.get_scratch_space()
        script_dir = os.path.join(scratch_dir, "lectures_video_script")
        os.makedirs(script_dir, exist_ok=True)
        hio.to_file(os.path.join(script_dir, "a.txt"), "one two three")
        hio.to_file(os.path.join(script_dir, "b.txt"), "four five")
        arg_list = [scratch_dir]
        # Prepare outputs.
        expected_log = "a.txt\t3\nb.txt\t2"
        # Run test.
        with self.assertLogs("class_scripts.count_words", level="INFO") as cm:
            with mock.patch("sys.argv", ["count_words.py"] + arg_list):
                clcowoor._main(clcowoor._parse())
        # Check outputs.
        # Log records are prefixed with the level and logger name, so only
        # the last two records (one per file) are checked.
        actual_log = "\n".join(
            record.split(":", 2)[-1] for record in cm.output[-2:]
        )
        self.assert_equal(actual_log, expected_log)

    def test2(self) -> None:
        """
        Test edge case: missing `lectures_video_script/` directory raises
        AssertionError.
        """
        # Prepare inputs.
        scratch_dir = self.get_scratch_space()
        arg_list = [scratch_dir]
        # Prepare outputs.
        expected = "Directory does not exist"
        # Run test.
        with mock.patch("sys.argv", ["count_words.py"] + arg_list):
            with self.assertRaises(AssertionError) as cm:
                clcowoor._main(clcowoor._parse())
        # Check outputs.
        self.assertIn(expected, str(cm.exception))
