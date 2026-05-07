"""
Test gen_slides.py script for data605 course.

Import as:

import data605.test.test_gen_slides as d6ttestgs
"""

import logging
import os
import shlex
from typing import List

import pytest
from tqdm import tqdm

import class_scripts.common_utils as csccouti
import class_scripts.gen_slides_test_utils as csgentuit
import helpers.hdbg as hdbg
import helpers.hio as hio
import helpers.hsystem as hsystem
import helpers.hunit_test as hunitest

_LOG = logging.getLogger(__name__)


# #############################################################################
# Test_gen_slides_sample
# #############################################################################


class Test_gen_slides_sample(hunitest.TestCase):
    """
    Test gen_slides.py script for data605 sample lessons.
    """

    @pytest.mark.slow
    def test1(self) -> None:
        """
        Test running gen_slides.py for data605 lesson 01.1.
        """
        # Prepare inputs.
        course_dir = "data605"
        lesson = "01.1"
        cmd = f"gen_slides.py {course_dir}/{lesson} --skip_action open"
        # Run test.
        hsystem.system(cmd)
        # Check outputs - if no exception, test passed.

    @pytest.mark.slow
    def test2(self) -> None:
        """
        Test running gen_slides.py for data605 lesson 08.2.
        """
        # Prepare inputs.
        course_dir = "data605"
        lesson = "08.2"
        cmd = f"gen_slides.py {course_dir}/{lesson} --skip_action open"
        # Run test.
        hsystem.system(cmd)
        # Check outputs - if no exception, test passed.


# #############################################################################
# Test_data605_lesson_discovery
# #############################################################################


class Test_data605_lesson_discovery(hunitest.TestCase):
    """
    Test discovery of data605 lessons.
    """

    def test1(self) -> None:
        """
        Test that data605 lessons can be discovered.
        """
        # Prepare inputs.
        course_dir = "data605"
        # Run test.
        lesson_files = csgentuit.get_lesson_files(course_dir)
        # Check outputs.
        self.assertGreater(len(lesson_files), 0)
        basenames = [os.path.basename(f) for f in lesson_files]
        self.assertIn("Lesson01.1-Intro.txt", basenames)

    def test2(self) -> None:
        """
        Test that data605 has expected number of lessons.
        """
        # Prepare inputs.
        course_dir = "data605"
        min_expected_lessons = 35
        # Run test.
        lessons = csgentuit.get_lesson_numbers(course_dir)
        # Check outputs.
        self.assertGreaterEqual(
            len(lessons),
            min_expected_lessons,
            f"data605 should have at least {min_expected_lessons} "
            f"lessons, found {len(lessons)}"
        )
        _LOG.info("data605 has %d lessons", len(lessons))

    def test3(self) -> None:
        """
        Test that data605 lesson numbers are well-formed.
        """
        # Prepare inputs.
        course_dir = "data605"
        valid_lesson_pattern = r"^\d+(\.\d+)?$"
        # Run test.
        lessons = csgentuit.get_lesson_numbers(course_dir)
        # Check outputs.
        for lesson in lessons:
            self.assertRegex(
                lesson,
                valid_lesson_pattern,
                f"Invalid lesson format '{lesson}' in {course_dir}"
            )


# #############################################################################
# Helper functions
# #############################################################################


def _test_lessons_preprocessing(
    test_case: hunitest.TestCase,
    course_dir: str,
    output_dir: str,
    lessons: List[str],
    output_type: str,
) -> None:
    """
    Test preprocessing output (MD or TeX) for a set of lessons.

    :param test_case: TestCase instance for assertions
    :param course_dir: Course directory (e.g., "data605")
    :param output_dir: Output directory for test results
    :param lessons: List of lesson numbers to test
    :param output_type: Either "md" for markdown or "tex" for LaTeX output
    """
    for lesson in tqdm(lessons, desc=f"Testing {output_type.upper()} output"):
        # Get source file.
        src_name = csccouti.get_source_name(course_dir, lesson)
        input_file = os.path.join(course_dir, "lectures_source", src_name)
        # Use lesson-specific output directory to avoid file conflicts.
        lesson_dir = os.path.join(output_dir, f"lesson_{lesson}")
        hio.create_dir(lesson_dir, incremental=True)

        if output_type == "md":
            output_file = os.path.join(lesson_dir, "output.pdf")
            temp_file = os.path.join(
                lesson_dir, "tmp.notes_to_pdf.preprocess_notes.txt"
            )
        elif output_type == "tex":
            output_file = os.path.join(lesson_dir, "output.tex")
            temp_file = os.path.join(lesson_dir, "tmp.notes_to_pdf.render_image2.tex")
        else:
            raise ValueError(f"Unknown output_type: {output_type}")

        cmd_parts = [
            "notes_to_pdf.py",
            "--input", input_file,
            "--output", output_file,
            "--type", "slides",
            "--toc_type", "navigation",
            "--skip_action", "cleanup_after",
            "--skip_action", "open",
        ]
        cmd = " ".join(shlex.quote(part) for part in cmd_parts)
        hsystem.system(cmd)
        # Extract and check output after preprocessing.
        hdbg.dassert_file_exists(temp_file)
        content = hio.from_file(temp_file)
        test_case.check_string(content, fuzzy_match=True)
        _LOG.info("Verified %s output for lesson %s", output_type.upper(), lesson)


# #############################################################################
# Test_data605_gen_slides_integration
# #############################################################################


class Test_data605_gen_slides_integration(hunitest.TestCase):
    """
    Integration tests for data605 slide generation.
    """

    @pytest.mark.superslow
    def test1(self) -> None:
        """
        Test that all data605 lessons can be rendered as PDF.
        """
        # Prepare inputs.
        course_dir = "data605"
        # Run test.
        lessons = csgentuit.get_lesson_numbers(course_dir)
        # Check outputs.
        for lesson in lessons:
            cmd = (
                f"gen_slides.py {course_dir}/{lesson} "
                "--skip_action open"
            )
            hsystem.system(cmd)
            _LOG.info("Successfully rendered %s lesson %s as PDF",
                     course_dir, lesson)

    @pytest.mark.superslow
    def test2(self) -> None:
        """
        Test MD output after preprocessing stage for all data605 lessons.
        """
        # Prepare inputs.
        course_dir = "data605"
        output_dir = self.get_output_dir()
        lessons = csgentuit.get_lesson_numbers(course_dir)
        # Run test.
        _test_lessons_preprocessing(self, course_dir, output_dir, lessons, "md")

    @pytest.mark.superslow
    def test3(self) -> None:
        """
        Test TeX output before rendering stage for all data605 lessons.
        """
        # Prepare inputs.
        course_dir = "data605"
        output_dir = self.get_output_dir()
        lessons = csgentuit.get_lesson_numbers(course_dir)
        # Run test.
        _test_lessons_preprocessing(self, course_dir, output_dir, lessons, "tex")
