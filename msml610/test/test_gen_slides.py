"""
Test gen_slides.py script for msml610 course.

Import as:

import msml610.test.test_gen_slides as m6ttestgs
"""

import pytest

import class_scripts.gen_slides_test_utils as csgentuit


# #############################################################################
# Test_gen_slides_sample
# #############################################################################


class Test_gen_slides_sample(csgentuit.GenSlidesSample_TestCase):
    """
    Test gen_slides.py script for msml610 sample lessons.
    """

    @pytest.mark.slow
    def test1(self) -> None:
        self._run_gen_slides("msml610", "01.1")

    @pytest.mark.slow
    def test2(self) -> None:
        self._run_gen_slides("msml610", "08.1")


# #############################################################################
# Test_msml610_lesson_discovery
# #############################################################################


class Test_msml610_lesson_discovery(csgentuit.LessonDiscovery_TestCase):
    """
    Test discovery of msml610 lessons.
    """

    def test1(self) -> None:
        self._check_lesson_discovery("msml610", "Lesson01.1-AI_and_Machine_Learning.txt")

    def test2(self) -> None:
        self._check_lesson_count("msml610")

    def test3(self) -> None:
        self._check_lesson_format("msml610")


# #############################################################################
# Test_msml610_gen_slides_integration
# #############################################################################


class Test_msml610_gen_slides_integration(csgentuit.GenSlidesIntegration_TestCase):
    """
    Integration tests for msml610 slide generation.
    """

    @pytest.mark.superslow
    def test1(self) -> None:
        self._render_all_lessons_to_pdf("msml610")

    @pytest.mark.superslow
    def test2(self) -> None:
        self._test_md_preprocessing("msml610")

    @pytest.mark.superslow
    def test3(self) -> None:
        self._test_tex_preprocessing("msml610")

