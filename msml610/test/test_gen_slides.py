"""
Test gen_slides.py script for msml610 course.

Import as:

import msml610.test.test_gen_slides as mttestgs
"""

import logging

import pytest

import class_scripts.gen_slides_test_utils as csgsteut

_LOG = logging.getLogger(__name__)


# #############################################################################
# Test_Msml610_Run_gen_slides_py_Sample
# #############################################################################


class Test_Msml610_Run_gen_slides_py_Sample(csgsteut.Run_gen_slides_py_TestCase):
    """
    Test gen_slides.py script for msml610 sample lessons.
    """

    @pytest.mark.slow
    def test1(self) -> None:
        """
        Generate slides for msml610 lesson 01.1.
        """
        # Prepare inputs.
        course_dir = "msml610"
        lesson = "01.1"
        # Run test.
        self._run_gen_slides(course_dir, lesson)

    @pytest.mark.slow
    def test2(self) -> None:
        """
        Generate slides for msml610 lesson 08.1.
        """
        # Prepare inputs.
        course_dir = "msml610"
        lesson = "08.1"
        # Run test.
        self._run_gen_slides(course_dir, lesson)


# #############################################################################
# Test_Msml610_LessonDiscovery
# #############################################################################


class Test_Msml610_LessonDiscovery(csgsteut.LessonDiscovery_TestCase):
    """
    Test discovery of msml610 lessons.
    """

    def test1(self) -> None:
        """
        Check discovery of expected lesson file.
        """
        # Prepare inputs.
        course_dir = "msml610"
        expected_filename = "Lesson01.1-AI_and_Machine_Learning.txt"
        # Run test.
        self._check_lesson_discovery(course_dir, expected_filename)

    def test2(self) -> None:
        """
        Check lesson count for msml610 course.
        """
        # Prepare inputs.
        course_dir = "msml610"
        # Run test.
        self._check_lesson_count(course_dir)

    def test3(self) -> None:
        """
        Check lesson file format for msml610 course.
        """
        # Prepare inputs.
        course_dir = "msml610"
        # Run test.
        self._check_lesson_format(course_dir)

    def test4(self) -> None:
        """
        Check get_lesson_files() utility function.
        """
        # Prepare inputs.
        course_dir = "msml610"
        # Run test.
        lesson_files = csgsteut.get_lesson_files(course_dir)
        self.assertGreater(len(lesson_files), 0)
        _LOG.info("Found %d lesson files in %s", len(lesson_files), course_dir)

    def test5(self) -> None:
        """
        Check get_lesson_numbers() utility function.
        """
        # Prepare inputs.
        course_dir = "msml610"
        # Run test.
        lesson_numbers = csgsteut.get_lesson_numbers(course_dir)
        self.assertGreater(len(lesson_numbers), 0)
        _LOG.info(
            "Found %d lesson numbers in %s", len(lesson_numbers), course_dir
        )


# #############################################################################
# Test_Msml610_AllLessonsCollection
# #############################################################################


class Test_Msml610_AllLessonsCollection(csgsteut.LessonDiscovery_TestCase):
    """
    Test collection of all lessons across courses.
    """

    def test1(self) -> None:
        """
        Check collect_all_lessons() utility function.
        """
        # Run test.
        all_lessons = csgsteut.collect_all_lessons()
        self.assertGreater(len(all_lessons), 0)
        self.assertIn("msml610", all_lessons)
        msml610_lessons = all_lessons["msml610"]
        self.assertGreater(len(msml610_lessons), 0)
        _LOG.info(
            "Collected %d courses with %d msml610 lessons",
            len(all_lessons),
            len(msml610_lessons),
        )


# #############################################################################
# Test_Msml610_Integration
# #############################################################################


class Test_Msml610_Integration(
    csgsteut.Run_gen_slides_py_TestCase,
    csgsteut.Run_notes_to_pdf_py_TestCase,
):
    """
    Integration tests for msml610 slide generation and preprocessing.
    """

    @pytest.mark.superslow
    def test1(self) -> None:
        """
        Render all msml610 lessons to PDF.
        """
        # Prepare inputs.
        course_dir = "msml610"
        # Run test.
        self._render_all_lessons_to_pdf(course_dir)

    @pytest.mark.superslow
    def test2(self) -> None:
        """
        Test markdown preprocessing for msml610 lessons.
        """
        # Prepare inputs.
        course_dir = "msml610"
        # Run test.
        self._run_notes_to_pdf_md_py(course_dir)

    @pytest.mark.superslow
    def test3(self) -> None:
        """
        Test LaTeX preprocessing for msml610 lessons.
        """
        # Prepare inputs.
        course_dir = "msml610"
        # Run test.
        self._run_notes_to_pdf_tex_py(course_dir)
