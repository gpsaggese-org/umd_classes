"""
Test gen_slides.py script for data605 course.

Import as:

import data605.test.test_gen_slides as d6ttestgs
"""

import pytest

import class_scripts.gen_slides_test_utils as csgsteut


# #############################################################################
# Test_data605_lesson_discovery
# #############################################################################


class Test_data605_lesson_discovery(csgsteut.LessonDiscovery_TestCase):
    """
    Test discovery of data605 lessons.
    """

    def test1(self) -> None:
        """
        Check discovery of expected lesson file.
        """
        # Prepare test inputs.
        course_dir = "data605"
        expected_filename = "Lesson01.1-Intro.txt"
        # Run test.
        self._check_lesson_discovery(course_dir, expected_filename)

    def test2(self) -> None:
        """
        Check lesson count for data605 course.
        """
        # Prepare test inputs.
        course_dir = "data605"
        # Run test.
        self._check_lesson_count(course_dir)

    def test3(self) -> None:
        """
        Check lesson file format for data605 course.
        """
        # Prepare test inputs.
        course_dir = "data605"
        # Run test.
        self._check_lesson_format(course_dir)


# #############################################################################
# Test_data605_preprocess_notes_py_integration
# #############################################################################


class Test_data605_preprocess_notes_py_integration(
    csgsteut.GenSlidesIntegration_TestCase
):
    """
    Integration tests for data605 preprocessing (preprocess_notes action).
    """

    @pytest.mark.superslow
    def test1(self) -> None:
        """
        Test markdown preprocessing for data605 lessons (skip run_pandoc).
        """
        # Prepare test inputs.
        course_dir = "data605"
        # Run test.
        self._test_md_preprocessing(course_dir)

    @pytest.mark.superslow
    def test2(self) -> None:
        """
        Test LaTeX preprocessing for data605 lessons.
        """
        # Prepare test inputs.
        course_dir = "data605"
        # Run test.
        self._test_tex_preprocessing(course_dir)


# #############################################################################
# Test_data605_gen_slides_py_sample
# #############################################################################


class Test_data605_gen_slides_py_sample(csgsteut.GenSlidesSample_TestCase):
    """
    Test gen_slides.py script for data605 sample lessons.
    """

    @pytest.mark.slow
    def test1(self) -> None:
        """
        Generate slides for data605 lesson 01.1.
        """
        # Prepare test inputs.
        course_dir = "data605"
        lesson = "01.1"
        # Run test.
        self._run_gen_slides(course_dir, lesson)

    @pytest.mark.slow
    def test2(self) -> None:
        """
        Generate slides for data605 lesson 08.2.
        """
        # Prepare test inputs.
        course_dir = "data605"
        lesson = "08.2"
        # Run test.
        self._run_gen_slides(course_dir, lesson)


# #############################################################################
# Test_data605_gen_slides_py
# #############################################################################


class Test_data605_gen_slides_py(
    csgsteut.GenSlidesIntegration_TestCase
):
    """
    Integration tests for data605 slide generation (PDF rendering).
    """

    @pytest.mark.superslow
    def test1(self) -> None:
        """
        Render all data605 lessons to PDF.
        """
        # Prepare test inputs.
        course_dir = "data605"
        # Run test.
        self._render_all_lessons_to_pdf(course_dir)