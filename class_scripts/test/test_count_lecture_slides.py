"""
Unit tests for count_lecture_slides.

Import as:

import class_scripts.test.test_count_lecture_slides as cstestcls
"""

import os
from typing import List

import helpers.hio as hio
import helpers.hunit_test as hunitest

import class_scripts.count_lecture_slides as clcoulsl


# #############################################################################
# Test__count_slides
# #############################################################################


class Test__count_slides(hunitest.TestCase):
    """
    Test `_count_slides()`.
    """

    def test1(self) -> None:
        """
        Test counting slides with multiple slide markers.

        Input: content with 3 lines starting with "* "
        Expected: 3
        """
        # Prepare inputs.
        content = "# Header\n* Slide 1\nSome text\n* Slide 2\n* Slide 3\nMore text"
        expected = 3
        # Run test.
        actual = clcoulsl._count_slides(content)
        # Check outputs.
        self.assertEqual(actual, expected)

    def test2(self) -> None:
        """
        Test counting slides with no slide markers.

        Input: content with no lines starting with "* "
        Expected: 0
        """
        # Prepare inputs.
        content = "# Header\nSome text\nMore text\n*No space after asterisk"
        expected = 0
        # Run test.
        actual = clcoulsl._count_slides(content)
        # Check outputs.
        self.assertEqual(actual, expected)

    def test3(self) -> None:
        """
        Test counting slides with asterisk not at start of line.

        Input: content with "* " not at start of line
        Expected: 0
        """
        # Prepare inputs.
        content = "This is text with * in the middle\nNot * at start"
        expected = 0
        # Run test.
        actual = clcoulsl._count_slides(content)
        # Check outputs.
        self.assertEqual(actual, expected)


# #############################################################################
# Test__count_headers
# #############################################################################


class Test__count_headers(hunitest.TestCase):
    """
    Test `_count_headers()`.
    """

    def test1(self) -> None:
        """
        Test counting headers at all three levels.

        Input: content with 1 H1, 2 H2, 1 H3
        Expected: (1, 2, 1)
        """
        # Prepare inputs.
        content = "# Main Title\nSome text\n## Section 1\nText\n## Section 2\nText\n### Subsection\n"
        expected = (1, 2, 1)
        # Run test.
        actual = clcoulsl._count_headers(content)
        # Check outputs.
        self.assertEqual(actual, expected)

    def test2(self) -> None:
        """
        Test counting headers with no headers.

        Input: content with no header markers at start of line
        Expected: (0, 0, 0)
        """
        # Prepare inputs.
        content = "This is just text\nNo headers here\nText with # in middle"
        expected = (0, 0, 0)
        # Run test.
        actual = clcoulsl._count_headers(content)
        # Check outputs.
        self.assertEqual(actual, expected)

    def test3(self) -> None:
        """
        Test counting headers distinguishing between levels.

        Input: content with mixed header syntax
        Expected: correct count at each level (0, 1, 0)
        """
        # Prepare inputs.
        content = "## Level 2\nNot a header: ## in text\n####Too many hashes"
        expected = (0, 1, 0)
        # Run test.
        actual = clcoulsl._count_headers(content)
        # Check outputs.
        self.assertEqual(actual, expected)


# #############################################################################
# Test__count_text_stats
# #############################################################################


class Test__count_text_stats(hunitest.TestCase):
    """
    Test `_count_text_stats()`.
    """

    def test1(self) -> None:
        """
        Test counting lines, words, and characters.

        Input: 3-line content
        Expected: (3, 7, 36)
        """
        # Prepare inputs.
        content = "Hello world\nLine two here\nFinal line"
        expected = (3, 7, 36)
        # Run test.
        actual = clcoulsl._count_text_stats(content)
        # Check outputs.
        self.assertEqual(actual, expected)

    def test2(self) -> None:
        """
        Test counting stats for empty content.

        Input: empty string
        Expected: (1, 0, 0)
        """
        # Prepare inputs.
        content = ""
        expected = (1, 0, 0)
        # Run test.
        actual = clcoulsl._count_text_stats(content)
        # Check outputs.
        self.assertEqual(actual, expected)

    def test3(self) -> None:
        """
        Test counting stats with single word.

        Input: single word
        Expected: (1, 1, word_length)
        """
        # Prepare inputs.
        content = "word"
        expected = (1, 1, 4)
        # Run test.
        actual = clcoulsl._count_text_stats(content)
        # Check outputs.
        self.assertEqual(actual, expected)


# #############################################################################
# Test__collect_stats
# #############################################################################


class Test__collect_stats(hunitest.TestCase):
    """
    Test `_collect_stats()`.
    """

    def test1(self) -> None:
        """
        Test collecting stats from multiple files.

        Creates two fake lecture files and verifies stats collection.
        """
        # Prepare inputs.
        scratch = self.get_scratch_space()
        course_dir = os.path.join(scratch, "testcourse")
        lectures_source = os.path.join(course_dir, "lectures_source")
        os.makedirs(lectures_source, exist_ok=True)
        lesson1_content = "# Intro\n* Slide 1\n* Slide 2\n## Section\nText here"
        lesson2_content = "# Chapter\n* Slide A\n## Part 1\n### Sub\nMore text"
        hio.to_file(
            os.path.join(lectures_source, "Lesson01-Intro.txt"), lesson1_content
        )
        hio.to_file(
            os.path.join(lectures_source, "Lesson02-Chapter.txt"),
            lesson2_content,
        )
        # Run test.
        rows = clcoulsl._collect_stats(course_dir)
        # Check outputs.
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0]["File"], "Lesson01-Intro.txt")
        self.assertEqual(rows[0]["Slides"], 2)
        self.assertEqual(rows[0]["H1"], 1)
        self.assertEqual(rows[0]["H2"], 1)
        self.assertEqual(rows[1]["File"], "Lesson02-Chapter.txt")
        self.assertEqual(rows[1]["Slides"], 1)
        self.assertEqual(rows[1]["H1"], 1)
        self.assertEqual(rows[1]["H2"], 1)
        self.assertEqual(rows[1]["H3"], 1)


# #############################################################################
# Test__format_table
# #############################################################################


class Test__format_table(hunitest.TestCase):
    """
    Test `_format_table()`.
    """

    def _make_test_rows(self) -> List[dict]:
        """Helper to create test rows."""
        return [
            {
                "File": "Lesson01.txt",
                "Slides": 5,
                "H1": 1,
                "H2": 2,
                "H3": 1,
                "Lines": 50,
                "Words": 300,
                "Chars": 2000,
            },
        ]

    def test1(self) -> None:
        """
        Test markdown format output.

        Input: single row
        Expected: markdown table with GitHub format
        """
        # Prepare inputs.
        rows = self._make_test_rows()
        # Run test.
        actual = clcoulsl._format_table(rows, format_type="markdown")
        # Check outputs.
        self.assertIn("|", actual)
        self.assertIn("File", actual)
        self.assertIn("Lesson01.txt", actual)

    def test2(self) -> None:
        """
        Test TSV format output.

        Input: single row
        Expected: tab-separated values
        """
        # Prepare inputs.
        rows = self._make_test_rows()
        # Run test.
        actual = clcoulsl._format_table(rows, format_type="tsv")
        # Check outputs.
        lines = actual.strip().split("\n")
        self.assertEqual(len(lines), 2)
        self.assertIn("File", lines[0])
        self.assertIn("Lesson01.txt", lines[1])

    def test3(self) -> None:
        """
        Test CSV format output.

        Input: single row
        Expected: comma-separated values
        """
        # Prepare inputs.
        rows = self._make_test_rows()
        # Run test.
        actual = clcoulsl._format_table(rows, format_type="csv")
        # Check outputs.
        lines = actual.strip().split("\n")
        self.assertEqual(len(lines), 2)
        self.assertIn("File", lines[0])
        self.assertIn("Lesson01.txt", lines[1])
