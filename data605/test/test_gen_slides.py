"""
Test gen_slides.py script for data605 course.

Import as:

import data605.test.test_gen_slides as d6ttestgs
"""

import logging
import os
import shlex

import pytest

import class_scripts.common_utils as csccouti
import class_scripts.gen_slides_test_utils as csgentuit
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
# Test_data605_gen_slides_integration
# #############################################################################


# TODO(ai_gp): Have a fast test checking only a couple of lessons and
# a super slow test checking all of them.
# Factor out the code so that code across classes in these files and
# across data605/test/test_gen_slides.py and msml610/test/test_gen_slides.py
# don't repeat code.
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
        Test MD output after preprocessing stage for data605 sample lessons.
        """
        # Prepare inputs.
        course_dir = "data605"
        output_dir = self.get_output_dir()
        # TODO(ai_gp): Check all of them and do a git add for all the relevant files.
        sample_lessons = ["01.1", "08.2"]
        # Run test.
        # TODO(ai_gp): Add a tqdm progress bar
        for lesson in sample_lessons:
            # Get source file.
            src_name = csccouti.get_source_name(course_dir, lesson)
            input_file = os.path.join(course_dir, "lectures_source", src_name)
            # Use lesson-specific output directory to avoid file conflicts.
            lesson_dir = os.path.join(output_dir, f"lesson_{lesson}")
            hio.create_dir(lesson_dir, incremental=True)
            cmd_parts = [
                "notes_to_pdf.py",
                "--input", input_file,
                "--output", os.path.join(lesson_dir, "output.pdf"),
                "--type", "slides",
                "--toc_type", "navigation",
                "--skip_action", "cleanup_after",
                "--skip_action", "open",
            ]
            cmd = " ".join(shlex.quote(part) for part in cmd_parts)
            hsystem.system(cmd)
            # Extract and check MD output after preprocessing.
            md_file = os.path.join(lesson_dir, "tmp.notes_to_pdf.preprocess_notes.txt")
            # TODO(ai_gp): This needs to be a dassert_file_exists.
            if os.path.exists(md_file):
                md_content = hio.from_file(md_file)
                actual = md_content
                self.check_string(actual, fuzzy_match=True)
                _LOG.info("Verified MD output for lesson %s", lesson)

    @pytest.mark.superslow
    def test3(self) -> None:
        """
        Test TeX output before rendering stage for data605 sample lessons.
        """
        # Prepare inputs.
        course_dir = "data605"
        output_dir = self.get_output_dir()
        # TODO(ai_gp): Check all of them and do a git add for all the relevant files.
        sample_lessons = ["01.1", "08.2"]
        # Run test.
        # TODO(ai_gp): Add a tqdm progress bar
        for lesson in sample_lessons:
            # Get source file.
            src_name = csccouti.get_source_name(course_dir, lesson)
            input_file = os.path.join(course_dir, "lectures_source", src_name)
            # Use lesson-specific output directory to avoid file conflicts.
            lesson_dir = os.path.join(output_dir, f"lesson_{lesson}")
            hio.create_dir(lesson_dir, incremental=True)
            cmd_parts = [
                "notes_to_pdf.py",
                "--input", input_file,
                "--output", os.path.join(lesson_dir, "output.tex"),
                "--type", "slides",
                "--toc_type", "navigation",
                "--skip_action", "cleanup_after",
                "--skip_action", "open",
            ]
            cmd = " ".join(shlex.quote(part) for part in cmd_parts)
            hsystem.system(cmd)
            # Extract and check TeX output before rendering.
            tex_file = os.path.join(lesson_dir, "tmp.notes_to_pdf.render_image2.tex")
            # TODO(ai_gp): This needs to be a dassert_file_exists.
            if os.path.exists(tex_file):
                tex_content = hio.from_file(tex_file)
                actual = tex_content
                self.check_string(actual, fuzzy_match=True)
                _LOG.info("Verified TeX output for lesson %s", lesson)
