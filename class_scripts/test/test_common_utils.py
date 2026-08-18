"""
Unit tests for common_utils.py.

Import as:

import class_scripts.test.test_common_utils as csttcout
"""

# TODO(gp): Make sure this file follows our unit test conventions

import os
from unittest import mock

import helpers.hio as hio
import helpers.hunit_test as hunitest

import class_scripts.common_utils as csccouti


# #############################################################################
# Test_validate_dir_lesson_args
# #############################################################################


class Test_validate_dir_lesson_args(hunitest.TestCase):
    """
    Test `validate_dir_lesson_args()` function.
    """

    def test1(self) -> None:
        """
        Test happy path: non-empty dir and lesson pass validation.
        """
        # Prepare inputs.
        dir_arg = "msml610"
        lesson_arg = "01.1"
        # Prepare outputs.
        expected = None
        # Run test.
        actual = csccouti.validate_dir_lesson_args(dir_arg, lesson_arg)
        # Check outputs.
        self.assertEqual(actual, expected)

    def test2(self) -> None:
        """
        Test edge case: empty `dir_arg` raises AssertionError.
        """
        # Prepare inputs.
        dir_arg = ""
        lesson_arg = "01.1"
        # Prepare outputs.
        expected = "DIR argument cannot be empty"
        # Run test.
        with self.assertRaises(AssertionError) as cm:
            csccouti.validate_dir_lesson_args(dir_arg, lesson_arg)
        # Check outputs.
        self.assertIn(expected, str(cm.exception))

    def test3(self) -> None:
        """
        Test edge case: empty `lesson_arg` raises AssertionError.
        """
        # Prepare inputs.
        dir_arg = "msml610"
        lesson_arg = ""
        # Prepare outputs.
        expected = "LESSON argument cannot be empty"
        # Run test.
        with self.assertRaises(AssertionError) as cm:
            csccouti.validate_dir_lesson_args(dir_arg, lesson_arg)
        # Check outputs.
        self.assertIn(expected, str(cm.exception))


# #############################################################################
# Test_find_lecture_file
# #############################################################################


class Test_find_lecture_file(hunitest.TestCase):
    """
    Test `find_lecture_file()` function.
    """

    def _create_lecture_source_dir(self, filenames: list) -> str:
        """
        Create a `lectures_source/` scratch dir with the given filenames.

        :param filenames: file names to create under `lectures_source/`
        :return: path to the parent (course) directory
        """
        scratch_dir = self.get_scratch_space()
        source_dir = os.path.join(scratch_dir, "lectures_source")
        os.makedirs(source_dir, exist_ok=True)
        for filename in filenames:
            hio.to_file(os.path.join(source_dir, filename), "content")
        return scratch_dir

    def test1(self) -> None:
        """
        Test happy path: exactly one matching file is found.
        """
        # Prepare inputs.
        filenames = ["Lesson01-Introduction.smd"]
        dir_path = self._create_lecture_source_dir(filenames)
        # Prepare outputs.
        expected = os.path.join(
            dir_path, "lectures_source", "Lesson01-Introduction.smd"
        )
        # Run test.
        actual = csccouti.find_lecture_file(dir_path, "01")
        # Check outputs.
        self.assert_equal(str(actual), expected)

    def test2(self) -> None:
        """
        Test edge case: no matching file raises AssertionError.
        """
        # Prepare inputs.
        filenames = ["Lesson02-Other.smd"]
        dir_path = self._create_lecture_source_dir(filenames)
        # Prepare outputs.
        expected = "Expected exactly one file"
        # Run test.
        with self.assertRaises(AssertionError) as cm:
            csccouti.find_lecture_file(dir_path, "01")
        # Check outputs.
        self.assertIn(expected, str(cm.exception))

    def test3(self) -> None:
        """
        Test edge case: two matching files raises AssertionError.
        """
        # Prepare inputs.
        filenames = ["Lesson01-First.smd", "Lesson01-Second.smd"]
        dir_path = self._create_lecture_source_dir(filenames)
        # Prepare outputs.
        expected = "Expected exactly one file"
        # Run test.
        with self.assertRaises(AssertionError) as cm:
            csccouti.find_lecture_file(dir_path, "01")
        # Check outputs.
        self.assertIn(expected, str(cm.exception))


# #############################################################################
# Test_get_source_name
# #############################################################################


class Test_get_source_name(hunitest.TestCase):
    """
    Test `get_source_name()` function.
    """

    def test1(self) -> None:
        """
        Test happy path: returns the file name without the directory path.
        """
        # Prepare inputs.
        scratch_dir = self.get_scratch_space()
        source_dir = os.path.join(scratch_dir, "lectures_source")
        os.makedirs(source_dir, exist_ok=True)
        hio.to_file(
            os.path.join(source_dir, "Lesson01-Introduction.smd"), "content"
        )
        # Prepare outputs.
        expected = "Lesson01-Introduction.smd"
        # Run test.
        actual = csccouti.get_source_name(scratch_dir, "01")
        # Check outputs.
        self.assert_equal(actual, expected)


# #############################################################################
# Test_get_output_name
# #############################################################################


class Test_get_output_name(hunitest.TestCase):
    """
    Test `get_output_name()` function.
    """

    def _helper(self, source_name: str, extension: str, expected: str) -> None:
        """
        Test helper for `get_output_name()`.

        :param source_name: source file name
        :param extension: new extension
        :param expected: expected output file name
        """
        # Run test.
        actual = csccouti.get_output_name(source_name, extension)
        # Check outputs.
        self.assert_equal(actual, expected)

    def test1(self) -> None:
        """
        Test happy path: replace extension on a simple file name.
        """
        # Prepare inputs.
        source_name = "Lesson01-Introduction.md"
        extension = ".pdf"
        # Prepare outputs.
        expected = "Lesson01-Introduction.pdf"
        # Run test.
        self._helper(source_name, extension, expected)

    def test2(self) -> None:
        """
        Test edge case: source name without an extension.
        """
        # Prepare inputs.
        source_name = "Lesson01-Introduction"
        extension = ".pdf"
        # Prepare outputs.
        expected = "Lesson01-Introduction.pdf"
        # Run test.
        self._helper(source_name, extension, expected)

    def test3(self) -> None:
        """
        Test edge case: source name with multiple dots keeps all but the
        last extension.
        """
        # Prepare inputs.
        source_name = "Lesson02.3-MapReduce.txt"
        extension = ".md"
        # Prepare outputs.
        expected = "Lesson02.3-MapReduce.md"
        # Run test.
        self._helper(source_name, extension, expected)


# #############################################################################
# Test_ensure_dir_exists
# #############################################################################


class Test_ensure_dir_exists(hunitest.TestCase):
    """
    Test `ensure_dir_exists()` function.
    """

    def test1(self) -> None:
        """
        Test happy path: creates a new directory that doesn't exist yet.
        """
        # Prepare inputs.
        scratch_dir = self.get_scratch_space()
        dir_path = os.path.join(scratch_dir, "new_dir")
        # Prepare outputs.
        expected = True
        # Run test.
        csccouti.ensure_dir_exists(dir_path)
        # Check outputs.
        actual = os.path.isdir(dir_path)
        self.assertEqual(actual, expected)

    def test2(self) -> None:
        """
        Test idempotency: calling twice keeps existing content in place.
        """
        # Prepare inputs.
        scratch_dir = self.get_scratch_space()
        dir_path = os.path.join(scratch_dir, "existing_dir")
        csccouti.ensure_dir_exists(dir_path)
        file_path = os.path.join(dir_path, "file.txt")
        hio.to_file(file_path, "content")
        # Prepare outputs.
        expected = (True, True)
        # Run test.
        csccouti.ensure_dir_exists(dir_path)
        # Check outputs.
        actual = (os.path.isdir(dir_path), os.path.exists(file_path))
        self.assertEqual(actual, expected)

    def test3(self) -> None:
        """
        Test `from_scratch=True` wipes prior directory content.
        """
        # Prepare inputs.
        scratch_dir = self.get_scratch_space()
        dir_path = os.path.join(scratch_dir, "from_scratch_dir")
        csccouti.ensure_dir_exists(dir_path)
        file_path = os.path.join(dir_path, "file.txt")
        hio.to_file(file_path, "content")
        # Prepare outputs.
        expected = (True, False)
        # Run test.
        csccouti.ensure_dir_exists(dir_path, from_scratch=True)
        # Check outputs.
        actual = (os.path.isdir(dir_path), os.path.exists(file_path))
        self.assertEqual(actual, expected)


# #############################################################################
# Test_count_pdf_pages
# #############################################################################


class Test_count_pdf_pages(hunitest.TestCase):
    """
    Test `count_pdf_pages()` function.
    """

    def test1(self) -> None:
        """
        Test happy path: parses page count from well-formed `mdls` output.
        """
        # Prepare inputs.
        scratch_dir = self.get_scratch_space()
        pdf_path = os.path.join(scratch_dir, "Lesson01.pdf")
        hio.to_file(pdf_path, "")
        mdls_output = (0, "kMDItemNumberOfPages = 42")
        # Prepare outputs.
        expected = 42
        # Run test.
        with mock.patch(
            "helpers.hsystem.system_to_string", return_value=mdls_output
        ):
            actual = csccouti.count_pdf_pages(pdf_path)
        # Check outputs.
        self.assertEqual(actual, expected)

    def test2(self) -> None:
        """
        Test edge case: malformed `mdls` output raises AssertionError.
        """
        # Prepare inputs.
        scratch_dir = self.get_scratch_space()
        pdf_path = os.path.join(scratch_dir, "Lesson01.pdf")
        hio.to_file(pdf_path, "")
        mdls_output = (0, "kMDItemNumberOfPages")
        # Prepare outputs.
        expected = "Unexpected mdls output format"
        # Run test.
        with mock.patch(
            "helpers.hsystem.system_to_string", return_value=mdls_output
        ):
            with self.assertRaises(AssertionError) as cm:
                csccouti.count_pdf_pages(pdf_path)
        # Check outputs.
        self.assertIn(expected, str(cm.exception))


# #############################################################################
# Test_get_pdf_page_counts
# #############################################################################


class Test_get_pdf_page_counts(hunitest.TestCase):
    """
    Test `get_pdf_page_counts()` function.
    """

    def test1(self) -> None:
        """
        Test happy path: returns a page count per matching PDF file.
        """
        # Prepare inputs.
        scratch_dir = self.get_scratch_space()
        hio.to_file(os.path.join(scratch_dir, "Lesson01.pdf"), "")
        hio.to_file(os.path.join(scratch_dir, "Lesson02.pdf"), "")
        page_counts = [10, 20]
        # Prepare outputs.
        expected = {"Lesson01.pdf": 10, "Lesson02.pdf": 20}
        # Run test.
        with mock.patch(
            "class_scripts.common_utils.count_pdf_pages",
            side_effect=page_counts,
        ):
            actual = csccouti.get_pdf_page_counts(scratch_dir)
        # Check outputs.
        self.assert_equal(str(actual), str(expected))

    def test2(self) -> None:
        """
        Test edge case: no matching PDF files returns an empty dict.
        """
        # Prepare inputs.
        scratch_dir = self.get_scratch_space()
        # Prepare outputs.
        expected: dict = {}
        # Run test.
        actual = csccouti.get_pdf_page_counts(scratch_dir)
        # Check outputs.
        self.assert_equal(str(actual), str(expected))
