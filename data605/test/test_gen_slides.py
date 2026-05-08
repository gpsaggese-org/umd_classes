"""
Test gen_slides.py script for data605 course.

Import as:

import data605.test.test_gen_slides as d6ttestgs
"""

import logging

import pytest

import class_scripts.gen_slides_test_utils as csgsteut

_LOG = logging.getLogger(__name__)


# #############################################################################
# Test_Data605_LessonDiscovery
# #############################################################################


class Test_Data605_LessonDiscovery(csgsteut.LessonDiscovery_TestCase):
    """
    Test discovery of data605 lessons.
    """

    def test1(self) -> None:
        """
        Check discovery of expected lesson file.
        """
        # Prepare inputs.
        course_dir = "data605"
        expected_filename = "Lesson01.1-Intro.txt"
        # Run test.
        self._check_lesson_discovery(course_dir, expected_filename)

    def test2(self) -> None:
        """
        Check lesson count for data605 course.
        """
        # Prepare inputs.
        course_dir = "data605"
        # Run test.
        self._check_lesson_count(course_dir)

    def test3(self) -> None:
        """
        Check lesson file format for data605 course.
        """
        # Prepare inputs.
        course_dir = "data605"
        # Run test.
        self._check_lesson_format(course_dir)

    def test4(self) -> None:
        """
        Check get_lesson_files() utility function.
        """
        # Prepare inputs.
        course_dir = "data605"
        # Run test.
        lesson_files = csgsteut.get_lesson_files(course_dir)
        self.assertGreater(len(lesson_files), 0)
        _LOG.info("Found %d lesson files in %s", len(lesson_files), course_dir)

    def test5(self) -> None:
        """
        Check get_lesson_numbers() utility function.
        """
        # Prepare inputs.
        course_dir = "data605"
        # Run test.
        lesson_numbers = csgsteut.get_lesson_numbers(course_dir)
        self.assertGreater(len(lesson_numbers), 0)
        _LOG.info(
            "Found %d lesson numbers in %s", len(lesson_numbers), course_dir
        )

    def test6(self) -> None:
        """
        Check collect_all_lessons() utility function.
        """
        # Run test.
        all_lessons = csgsteut.collect_all_lessons()
        self.assertGreater(len(all_lessons), 0)
        self.assertIn("data605", all_lessons)
        data605_lessons = all_lessons["data605"]
        self.assertGreater(len(data605_lessons), 0)
        _LOG.info(
            "Collected %d courses with %d data605 lessons",
            len(all_lessons),
            len(data605_lessons),
        )


# #############################################################################
# Test_Data605_Run_notes_to_pdf_py
# #############################################################################


class Test_Data605_Run_notes_to_pdf_py(
    csgsteut.Run_notes_to_pdf_py_TestCase
):
    """
    Integration tests for data605 preprocessing (preprocess_notes action).
    """

    @pytest.mark.superslow
    def test1(self) -> None:
        """
        Test markdown preprocessing for data605 lessons (skip run_pandoc).
        """
        # Prepare inputs.
        course_dir = "data605"
        # Run test.
        self._run_notes_to_pdf_md_py(course_dir)

    @pytest.mark.superslow
    def test2(self) -> None:
        """
        Test LaTeX preprocessing for data605 lessons.
        """
        # Prepare inputs.
        course_dir = "data605"
        # Run test.
        self._run_notes_to_pdf_tex_py(course_dir)


# #############################################################################
# Test_Data605_Run_gen_slides_py
# #############################################################################


class Test_Data605_Run_gen_slides_py(csgsteut.Run_gen_slides_py_TestCase):
    """
    Integration tests for data605 slide generation (PDF rendering).
    """

    @pytest.mark.slow
    def test1(self) -> None:
        """
        Generate slides for data605 lesson 01.1.
        """
        # Prepare inputs.
        course_dir = "data605"
        lesson = "01.1"
        # Run test.
        self._run_gen_slides(course_dir, lesson)

    @pytest.mark.slow
    def test2(self) -> None:
        """
        Generate slides for data605 lesson 08.2.
        """
        # Prepare inputs.
        course_dir = "data605"
        lesson = "08.2"
        # Run test.
        self._run_gen_slides(course_dir, lesson)

    @pytest.mark.superslow
    def test3(self) -> None:
        """
        Render all data605 lessons to PDF.
        """
        # Prepare inputs.
        course_dir = "data605"
        # Run test.
        self._render_all_lessons_to_pdf(course_dir)
