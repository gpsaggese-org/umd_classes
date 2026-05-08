"""
Test gen_slides.py script for data605 course.

Import as:

import data605.test.test_gen_slides as d6ttestgs
"""

import pytest

import class_scripts.gen_slides_test_utils as csgsteut


# #############################################################################
# Test_gen_slides_sample
# #############################################################################


class Test_gen_slides_sample(csgsteut.GenSlidesSample_TestCase):
    """
    Test gen_slides.py script for data605 sample lessons.
    """

    @pytest.mark.slow
    def test1(self) -> None:
        # Prepare test inputs.
        course_dir = "data605"
        lesson = "01.1"
        # Run test.
        self._run_gen_slides(course_dir, lesson)

    @pytest.mark.slow
    def test2(self) -> None:
        # Prepare test inputs.
        course_dir = "data605"
        lesson = "08.2"
        # Run test.
        self._run_gen_slides(course_dir, lesson)


# #############################################################################
# Test_data605_lesson_discovery
# #############################################################################


class Test_data605_lesson_discovery(csgsteut.LessonDiscovery_TestCase):
    """
    Test discovery of data605 lessons.
    """

    def test1(self) -> None:
        # Prepare test inputs.
        course_dir = "data605"
        expected_filename = "Lesson01.1-Intro.txt"
        # Run test.
        self._check_lesson_discovery(course_dir, expected_filename)

    def test2(self) -> None:
        # Prepare test inputs.
        course_dir = "data605"
        # Run test.
        self._check_lesson_count(course_dir)

    def test3(self) -> None:
        # Prepare test inputs.
        course_dir = "data605"
        # Run test.
        self._check_lesson_format(course_dir)


# #############################################################################
# Test_data605_gen_slides_integration
# #############################################################################


class Test_data605_gen_slides_integration(
    csgsteut.GenSlidesIntegration_TestCase
):
    """
    Integration tests for data605 slide generation.
    """

    @pytest.mark.superslow
    def test1(self) -> None:
        # Prepare test inputs.
        course_dir = "data605"
        # Run test.
        self._render_all_lessons_to_pdf(course_dir)

    @pytest.mark.superslow
    def test2(self) -> None:
        # Prepare test inputs.
        course_dir = "data605"
        # Run test.
        self._test_md_preprocessing(course_dir)

    @pytest.mark.superslow
    def test3(self) -> None:
        # Prepare test inputs.
        course_dir = "data605"
        # Run test.
        self._test_tex_preprocessing(course_dir)
