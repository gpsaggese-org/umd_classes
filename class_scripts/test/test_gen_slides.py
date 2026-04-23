"""
Unit tests for gen_slides.py script.

Import as:

import class_scripts.test.test_gen_slides as cstestgs
"""

import argparse
import logging
from unittest import mock

import helpers.hunit_test as hunitest

import class_scripts.gen_slides as clgeslio

_LOG = logging.getLogger(__name__)


class Test_extract_lesson_from_file(hunitest.TestCase):
    """
    Test _extract_lesson_from_file() function.
    """

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
        actual_dir, actual_lesson = clgeslio._extract_lesson_from_file(file_path)
        # Check outputs.
        self.assertEqual(actual_dir, expected_dir)
        self.assertEqual(actual_lesson, expected_lesson)

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
        actual_dir, actual_lesson = clgeslio._extract_lesson_from_file(file_path)
        # Check outputs.
        self.assertEqual(actual_dir, expected_dir)
        self.assertEqual(actual_lesson, expected_lesson)

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
        actual_dir, actual_lesson = clgeslio._extract_lesson_from_file(file_path)
        # Check outputs.
        self.assertEqual(actual_dir, expected_dir)
        self.assertEqual(actual_lesson, expected_lesson)

    def test4(self) -> None:
        """
        Test that invalid filename without Lesson prefix raises AssertionError.
        """
        # Prepare inputs.
        invalid_file = "msml610/lectures_source/InvalidName.md"
        # Run test and check output.
        with self.assertRaises(AssertionError) as cm:
            clgeslio._extract_lesson_from_file(invalid_file)
        actual = str(cm.exception)
        self.assertIn("Could not extract lesson number", actual)

    def test5(self) -> None:
        """
        Test that invalid directory in path raises AssertionError.
        """
        # Prepare inputs.
        invalid_file = "invalid_dir/lectures_source/Lesson01-Name.md"
        # Run test and check output.
        with self.assertRaises(AssertionError) as cm:
            clgeslio._extract_lesson_from_file(invalid_file)
        actual = str(cm.exception)
        self.assertIn("invalid", actual)


class Test_parse(hunitest.TestCase):
    """
    Test _parse() function.
    """

    def test1(self) -> None:
        """
        Test parser accepts directory and lesson arguments.
        """
        # Run test.
        parser = clgeslio._parse()
        # Check outputs.
        self.assertIsInstance(parser, argparse.ArgumentParser)
        args = parser.parse_args(["data605", "01.1"])
        self.assertEqual(args.dir, "data605")
        self.assertEqual(args.lesson, "01.1")

    def test2(self) -> None:
        """
        Test parser accepts file path without lesson argument.
        """
        # Run test.
        parser = clgeslio._parse()
        # Check outputs.
        args = parser.parse_args(["msml610/lectures_source/Lesson10-Name.txt"])
        self.assertEqual(args.dir, "msml610/lectures_source/Lesson10-Name.txt")
        self.assertIsNone(args.lesson)

    def test3(self) -> None:
        """
        Test parser accepts extra positional arguments.
        """
        # Run test.
        parser = clgeslio._parse()
        # Check outputs.
        args = parser.parse_args(["data605", "02.1", "extra_arg1", "extra_arg2"])
        self.assertEqual(args.dir, "data605")
        self.assertEqual(args.lesson, "02.1")
        self.assertEqual(args.extra_opts, ["extra_arg1", "extra_arg2"])

    def test4(self) -> None:
        """
        Test parser has expected description and help.
        """
        # Run test.
        parser = clgeslio._parse()
        # Check outputs.
        description = parser.description
        self.assertIsNotNone(description)
        self.assertIn("Generate lecture slides", description)
