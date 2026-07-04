"""
Unit tests for get_lecture_file.py.

Import as:

import class_scripts.test.test_get_lecture_file as csttglfi
"""

import os
from unittest import mock

import helpers.hio as hio
import helpers.hunit_test as hunitest

import class_scripts.get_lecture_file as clgelifi


# #############################################################################
# Test_parse
# #############################################################################


class Test_parse(hunitest.TestCase):
    """
    Test `_parse()` function.
    """

    def test1(self) -> None:
        """
        Test parser accepts the positional `dir` and `lesson` arguments.
        """
        # Prepare inputs.
        arg_list = ["msml610", "01.1"]
        # Run test.
        parser = clgelifi._parse()
        args = parser.parse_args(arg_list)
        # Check outputs.
        self.assertEqual(args.dir, "msml610")
        self.assertEqual(args.lesson, "01.1")


# #############################################################################
# Test_main
# #############################################################################


class Test_main(hunitest.TestCase):
    """
    Test `_main()` function.
    """

    def test1(self) -> None:
        """
        Test happy path: finds and logs the path of the matching lecture
        file.
        """
        # Prepare inputs.
        scratch_dir = self.get_scratch_space()
        source_dir = os.path.join(scratch_dir, "lectures_source")
        os.makedirs(source_dir, exist_ok=True)
        hio.to_file(
            os.path.join(source_dir, "Lesson01-Introduction.txt"), "content"
        )
        arg_list = [scratch_dir, "01"]
        # Run test.
        with self.assertLogs(
            "class_scripts.get_lecture_file", level="INFO"
        ) as cm:
            with mock.patch("sys.argv", ["get_lecture_file.py"] + arg_list):
                clgelifi._main(clgelifi._parse())
        # Check outputs.
        expected_path = os.path.join(
            source_dir, "Lesson01-Introduction.txt"
        )
        actual_log = "\n".join(cm.output)
        self.assertIn(expected_path, actual_log)
