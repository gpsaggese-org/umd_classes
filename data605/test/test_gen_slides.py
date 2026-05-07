"""
Test gen_slides.py script for data605 course.

Import as:

import data605.test.test_gen_slides as d6ttestgs
"""

import pytest

import class_scripts.gen_slides_test_utils as csgentuit


# #############################################################################
# Test_gen_slides_sample
# #############################################################################


class Test_gen_slides_sample(csgentuit.GenSlidesSample_TestCase):
    """
    Test gen_slides.py script for data605 sample lessons.
    """

    @pytest.mark.slow
    def test1(self) -> None:
        self._run_gen_slides("data605", "01.1")

    @pytest.mark.slow
    def test2(self) -> None:
        self._run_gen_slides("data605", "08.2")


# #############################################################################
# Test_data605_lesson_discovery
# #############################################################################


class Test_data605_lesson_discovery(csgentuit.LessonDiscovery_TestCase):
    """
    Test discovery of data605 lessons.
    """

    def test1(self) -> None:
        self._check_lesson_discovery("data605", "Lesson01.1-Intro.txt")

    def test2(self) -> None:
        self._check_lesson_count("data605")

    def test3(self) -> None:
        self._check_lesson_format("data605")


# #############################################################################
# Test_data605_gen_slides_integration
# #############################################################################


class Test_data605_gen_slides_integration(csgentuit.GenSlidesIntegration_TestCase):
    """
    Integration tests for data605 slide generation.
    """

    @pytest.mark.superslow
    def test1(self) -> None:
        self._render_all_lessons_to_pdf("data605")

    @pytest.mark.superslow
    def test2(self) -> None:
        self._test_md_preprocessing("data605")

    @pytest.mark.superslow
    def test3(self) -> None:
        self._test_tex_preprocessing("data605")
