"""
Unit tests for gen_slides.py script.

Import as:

import class_scripts.test.test_gen_slides as cstestgs
"""

import argparse
import logging

import helpers.hunit_test as hunitest

import class_scripts.gen_slides as clgeslio

_LOG = logging.getLogger(__name__)


class Test_extract_lesson_from_file(hunitest.TestCase):
    """
    Test _extract_lesson_from_file() function.
    """

    def _assert_extract_lesson(
        self, file_path: str, expected_dir: str, expected_lesson: str
    ) -> None:
        """
        Test helper for _extract_lesson_from_file.

        :param file_path: File path to test
        :param expected_dir: Expected directory from extraction
        :param expected_lesson: Expected lesson number from extraction
        """
        # Run test.
        actual_dir, actual_lesson = clgeslio._extract_lesson_from_file(file_path)
        # Check outputs.
        self.assertEqual(actual_dir, expected_dir)
        self.assertEqual(actual_lesson, expected_lesson)

    def _assert_extract_lesson_raises(
        self, file_path: str, expected_error_msg: str
    ) -> None:
        """
        Test helper for _extract_lesson_from_file error cases.

        :param file_path: File path to test
        :param expected_error_msg: Expected substring in error message
        """
        # Run test and check output.
        with self.assertRaises(AssertionError) as cm:
            clgeslio._extract_lesson_from_file(file_path)
        self.assertIn(expected_error_msg, str(cm.exception))

    def test1(self) -> None:
        """
        Test extraction from valid file path with single digit lesson.
        """
        # Prepare inputs.
        file_path = "msml610/lectures_source/Lesson10-Introduction.md"
        # Prepare outputs.
        expected_dir = "msml610"
        expected_lesson = "10"
        # Run test.
        self._assert_extract_lesson(file_path, expected_dir, expected_lesson)

    def test2(self) -> None:
        """
        Test extraction from valid file path with dotted lesson number.
        """
        # Prepare inputs.
        file_path = "data605/lectures_source/Lesson02.3-MapReduce.txt"
        # Prepare outputs.
        expected_dir = "data605"
        expected_lesson = "02.3"
        # Run test.
        self._assert_extract_lesson(file_path, expected_dir, expected_lesson)

    def test3(self) -> None:
        """
        Test extraction with lesson number containing multiple dots.
        """
        # Prepare inputs.
        file_path = "msml610/lectures_source/Lesson10.2.1-Complex.md"
        # Prepare outputs.
        expected_dir = "msml610"
        expected_lesson = "10.2"
        # Run test.
        self._assert_extract_lesson(file_path, expected_dir, expected_lesson)

    def test4(self) -> None:
        """
        Test that invalid filename without Lesson prefix raises AssertionError.
        """
        # Prepare inputs.
        file_path = "msml610/lectures_source/InvalidName.md"
        # Prepare outputs.
        expected_error_msg = "Could not extract lesson number"
        # Run test.
        self._assert_extract_lesson_raises(file_path, expected_error_msg)

    def test5(self) -> None:
        """
        Test that invalid directory in path raises AssertionError.
        """
        # Prepare inputs.
        file_path = "invalid_dir/lectures_source/Lesson01-Name.md"
        # Prepare outputs.
        expected_error_msg = "invalid"
        # Run test.
        self._assert_extract_lesson_raises(file_path, expected_error_msg)


class Test_parse(hunitest.TestCase):
    """
    Test _parse() function.
    """

    def _assert_parse_args(self, arg_list: list, expected_values: dict) -> None:
        """
        Test helper for _parse.

        :param arg_list: List of arguments to parse
        :param expected_values: Dictionary of expected argument values
        """
        # Run test.
        parser = clgeslio._parse()
        args = parser.parse_args(arg_list)
        # Check outputs.
        for key, value in expected_values.items():
            self.assertEqual(getattr(args, key), value)

    def test1(self) -> None:
        """
        Test parser accepts directory and lesson arguments.
        """
        # Prepare inputs.
        arg_list = ["data605", "01.1"]
        # Prepare outputs.
        expected_values = {"dir": "data605", "lesson": "01.1"}
        # Run test.
        parser = clgeslio._parse()
        self.assertIsInstance(parser, argparse.ArgumentParser)
        self._assert_parse_args(arg_list, expected_values)

    def test2(self) -> None:
        """
        Test parser accepts file path without lesson argument.
        """
        # Prepare inputs.
        arg_list = ["msml610/lectures_source/Lesson10-Name.txt"]
        # Prepare outputs.
        expected_values = {
            "dir": "msml610/lectures_source/Lesson10-Name.txt",
            "lesson": None,
        }
        # Run test.
        self._assert_parse_args(arg_list, expected_values)

    def test3(self) -> None:
        """
        Test parser accepts extra positional arguments.
        """
        # Prepare inputs.
        arg_list = ["data605", "02.1", "extra_arg1", "extra_arg2"]
        # Prepare outputs.
        expected_values = {
            "dir": "data605",
            "lesson": "02.1",
            "extra_opts": ["extra_arg1", "extra_arg2"],
        }
        # Run test.
        self._assert_parse_args(arg_list, expected_values)

    def test4(self) -> None:
        """
        Test parser has expected description and help.
        """
        # Run test.
        parser = clgeslio._parse()
        # Check outputs.
        self.assertIsNotNone(parser.description)
        self.assertIn("Generate lecture slides", parser.description)
