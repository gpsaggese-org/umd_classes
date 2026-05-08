import pytest

import class_scripts.gen_slides_test_utils as csgsteut


# #############################################################################
# Test_gen_slides_sample
# #############################################################################


class Test_gen_slides_sample(csgsteut.GenSlidesSample_TestCase):
    """
    Test gen_slides.py script for msml610 sample lessons.
    """

    @pytest.mark.slow
    def test1(self) -> None:
        # Prepare test inputs.
        course_dir = "msml610"
        lesson = "01.1"
        # Run test.
        self._run_gen_slides(course_dir, lesson)

    @pytest.mark.slow
    def test2(self) -> None:
        # Prepare test inputs.
        course_dir = "msml610"
        lesson = "08.1"
        # Run test.
        self._run_gen_slides(course_dir, lesson)


# #############################################################################
# Test_msml610_lesson_discovery
# #############################################################################


class Test_msml610_lesson_discovery(csgsteut.LessonDiscovery_TestCase):
    """
    Test discovery of msml610 lessons.
    """

    def test1(self) -> None:
        # Prepare test inputs.
        course_dir = "msml610"
        expected_filename = "Lesson01.1-AI_and_Machine_Learning.txt"
        # Run test.
        self._check_lesson_discovery(course_dir, expected_filename)

    def test2(self) -> None:
        # Prepare test inputs.
        course_dir = "msml610"
        # Run test.
        self._check_lesson_count(course_dir)

    def test3(self) -> None:
        # Prepare test inputs.
        course_dir = "msml610"
        # Run test.
        self._check_lesson_format(course_dir)


# #############################################################################
# Test_msml610_gen_slides_integration
# #############################################################################


class Test_msml610_gen_slides_integration(
    csgsteut.GenSlidesIntegration_TestCase
):
    """
    Integration tests for msml610 slide generation.
    """

    @pytest.mark.superslow
    def test1(self) -> None:
        # Prepare test inputs.
        course_dir = "msml610"
        # Run test.
        self._render_all_lessons_to_pdf(course_dir)

    @pytest.mark.superslow
    def test2(self) -> None:
        # Prepare test inputs.
        course_dir = "msml610"
        # Run test.
        self._test_md_preprocessing(course_dir)

    @pytest.mark.superslow
    def test3(self) -> None:
        # Prepare test inputs.
        course_dir = "msml610"
        # Run test.
        self._test_tex_preprocessing(course_dir)
