"""
Shared utilities for slide generation testing.

Import as:

import class_scripts.gen_slides_test_utils as csgsteut
"""

import logging
import os
import re
import shlex
import sys
from typing import Dict, List, Optional

import pytest
from tqdm import tqdm

import class_scripts.common_utils as csccouti
import helpers.hdbg as hdbg
import helpers.hio as hio
import helpers.hsystem as hsystem
import helpers.hunit_test as hunitest

_LOG = logging.getLogger(__name__)


# #############################################################################
# Lesson Discovery Utilities
# #############################################################################


def get_lesson_files(course_dir: str) -> List[str]:
    """
    Discover all lesson files in a course directory.

    :param course_dir: Course directory (data605 or msml610)
    :return: Sorted list of lesson file paths
    """
    lectures_source_dir = os.path.join(course_dir, "lectures_source")
    hdbg.dassert_dir_exists(lectures_source_dir)
    lesson_files = []
    for file in os.listdir(lectures_source_dir):
        if re.match(r"^Lesson\d+", file):
            file_path = os.path.join(lectures_source_dir, file)
            lesson_files.append(file_path)
    return sorted(lesson_files)


def get_lesson_numbers(course_dir: str) -> List[str]:
    """
    Get all lesson numbers in a course.

    :param course_dir: Course directory (data605 or msml610)
    :return: Sorted list of lesson numbers like ["01.1", "01.2", ...]
    """
    lectures_source_dir = os.path.join(course_dir, "lectures_source")
    hdbg.dassert_dir_exists(lectures_source_dir)
    lessons = []
    for file in os.listdir(lectures_source_dir):
        match = re.match(r"Lesson(\d+(?:\.\d+)?)", file)
        if match:
            lesson_num = match.group(1)
            lessons.append(lesson_num)
    return sorted(set(lessons))


# #############################################################################
# Lesson Collection Utilities
# #############################################################################


def collect_all_lessons() -> Dict[str, List[str]]:
    """
    Collect all lessons organized by course.

    :return: Dict with course dirs as keys and lesson lists as values
    """
    all_lessons = {}
    for course_dir in csccouti.VALID_DIRS:
        all_lessons[course_dir] = get_lesson_numbers(course_dir)
    return all_lessons


# #############################################################################
# LessonDiscovery_TestCase
# #############################################################################


class LessonDiscovery_TestCase(hunitest.TestCase):
    """
    Base class for testing lesson discovery in a course.
    """

    # Subclasses must override these.
    COURSE_DIR: str = ""
    FIRST_LESSON_FILENAME: str = ""

    def test_check_lesson_discovery(self) -> None:
        hdbg.dassert_ne(self.COURSE_DIR, "")
        hdbg.dassert_ne(self.FIRST_LESSON_FILENAME, "")
        self._check_lesson_discovery(self.COURSE_DIR, self.FIRST_LESSON_FILENAME)

    def test_check_lesson_count(self) -> None:
        hdbg.dassert_ne(self.COURSE_DIR, "")
        self._check_lesson_count(self.COURSE_DIR)

    def test_check_lesson_format(self) -> None:
        hdbg.dassert_ne(self.COURSE_DIR, "")
        self._check_lesson_format(self.COURSE_DIR)

    def test_get_lesson_files(self) -> None:
        hdbg.dassert_ne(self.COURSE_DIR, "")
        files = get_lesson_files(self.COURSE_DIR)
        self.assertGreater(len(files), 0)
        _LOG.debug("Found %d lesson files", len(files))

    def test_get_lesson_numbers(self) -> None:
        hdbg.dassert_ne(self.COURSE_DIR, "")
        numbers = get_lesson_numbers(self.COURSE_DIR)
        self.assertGreater(len(numbers), 0)
        _LOG.debug("Found %d lesson numbers", len(numbers))

    def test_collect_all_lessons(self) -> None:
        hdbg.dassert_ne(self.COURSE_DIR, "")
        all_lessons = collect_all_lessons()
        self.assertIn(self.COURSE_DIR, all_lessons)

    def _check_lesson_discovery(
        self, course_dir: str, expected_first_lesson_filename: str
    ) -> None:
        """Check that lessons can be discovered."""
        lesson_files = get_lesson_files(course_dir)
        self.assertGreater(len(lesson_files), 0)
        basenames = [os.path.basename(f) for f in lesson_files]
        self.assertIn(expected_first_lesson_filename, basenames)

    def _check_lesson_count(self, course_dir: str) -> None:
        """Check that course has expected number of lessons."""
        min_expected_lessons = 35
        lessons = get_lesson_numbers(course_dir)
        self.assertGreaterEqual(
            len(lessons),
            min_expected_lessons,
            f"{course_dir} should have at least {min_expected_lessons} "
            f"lessons, found {len(lessons)}",
        )
        _LOG.info("%s has %d lessons", course_dir, len(lessons))

    def _check_lesson_format(self, course_dir: str) -> None:
        """Check that lesson numbers are well-formed."""
        valid_lesson_pattern = r"^\d+(\.\d+)?$"
        lessons = get_lesson_numbers(course_dir)
        for lesson in lessons:
            self.assertRegex(
                lesson,
                valid_lesson_pattern,
                f"Invalid lesson format '{lesson}' in {course_dir}",
            )


# #############################################################################
# Run_preprocess_notes_py_TestCase
# #############################################################################


class Run_preprocess_notes_py_TestCase(hunitest.TestCase):
    """
    Base class for integration tests for preprocess_notes.py script.
    """

    COURSE_DIR: str = ""

    @pytest.mark.slow
    def test_preprocess_notes_pdf(self) -> None:
        hdbg.dassert_ne(self.COURSE_DIR, "")
        self._run_preprocess_notes_pdf(self.COURSE_DIR)

    @pytest.mark.slow
    def test_preprocess_notes_html(self) -> None:
        hdbg.dassert_ne(self.COURSE_DIR, "")
        self._run_preprocess_notes_html(self.COURSE_DIR)

    @pytest.mark.slow
    def test_preprocess_notes_slides(self) -> None:
        hdbg.dassert_ne(self.COURSE_DIR, "")
        self._run_preprocess_notes_slides(self.COURSE_DIR)

    @staticmethod
    def _run_preprocess_notes_py(
        test_case: hunitest.TestCase,
        course_dir: str,
        output_dir: str,
        lessons: List[str],
        output_type: str,
        toc_type: str = "none",
    ) -> None:
        """
        Test preprocessing output for a set of lessons.

        :param test_case: TestCase instance for assertions
        :param course_dir: Course directory (e.g., "data605")
        :param output_dir: Output directory for test results
        :param lessons: List of lesson numbers to test
        :param output_type: Either "pdf", "html", or "slides"
        :param toc_type: Type of table of contents ("none", "pandoc_native",
            "navigation", "remove_headers")
        """
        for lesson in tqdm(lessons, desc=f"Preprocessing {output_type.upper()}"):
            # Get source file.
            src_name = csccouti.get_source_name(course_dir, lesson)
            input_file = os.path.join(course_dir, "lectures_source", src_name)
            # Use lesson-specific output directory to avoid file conflicts.
            lesson_dir = os.path.join(output_dir, f"lesson_{lesson}")
            hio.create_dir(lesson_dir, incremental=True)
            # Prepare output file path.
            output_file = os.path.join(lesson_dir, "preprocessed.md")
            # Prepare command arguments.
            input_arg = shlex.quote(input_file)
            output_arg = shlex.quote(output_file)
            # Build and execute command.
            cmd = (
                f"preprocess_notes.py "
                f"--input={input_arg} "
                f"--output={output_arg} "
                f"--type={output_type} "
                f"--toc_type={toc_type}"
            )
            _LOG.info("Running command: %s", cmd)
            hsystem.system(cmd)
            sys.stdout.flush()
            # Extract and check output after preprocessing.
            hdbg.dassert_file_exists(output_file)
            content = hio.from_file(output_file)
            test_case.check_string(content, fuzzy_match=True)
            sys.stdout.flush()
            _LOG.info(
                "Verified %s preprocessing for lesson %s", output_type.upper(),
                lesson
            )

    def _run_preprocess_notes_pdf(self, course_dir: str) -> None:
        """
        Test PDF preprocessing for all lessons.

        Verifies that the preprocessing output is correct for all lessons
        in a course when targeting PDF output.

        :param course_dir: Course directory (e.g., "data605" or "msml610")
        """
        output_dir = self.get_output_dir()
        lessons = get_lesson_numbers(course_dir)
        self._run_preprocess_notes_py(
            self, course_dir, output_dir, lessons, "pdf"
        )

    def _run_preprocess_notes_html(self, course_dir: str) -> None:
        """
        Test HTML preprocessing for all lessons.

        Verifies that the preprocessing output is correct for all lessons
        in a course when targeting HTML output.

        :param course_dir: Course directory (e.g., "data605" or "msml610")
        """
        output_dir = self.get_output_dir()
        lessons = get_lesson_numbers(course_dir)
        self._run_preprocess_notes_py(
            self, course_dir, output_dir, lessons, "html"
        )

    def _run_preprocess_notes_slides(self, course_dir: str) -> None:
        """
        Test slides preprocessing for all lessons.

        Verifies that the preprocessing output is correct for all lessons
        in a course when targeting slides output.

        :param course_dir: Course directory (e.g., "data605" or "msml610")
        """
        output_dir = self.get_output_dir()
        lessons = get_lesson_numbers(course_dir)
        self._run_preprocess_notes_py(
            self, course_dir, output_dir, lessons, "slides"
        )

# #############################################################################
# Run_notes_to_pdf_py_TestCase
# #############################################################################


class Run_notes_to_pdf_py_TestCase(hunitest.TestCase):
    """
    Base class for integration tests for slide generation.
    """

    COURSE_DIR: str = ""

    @pytest.mark.superslow
    def test_notes_to_pdf_md(self) -> None:
        hdbg.dassert_ne(self.COURSE_DIR, "")
        self._run_notes_to_pdf_md_py(self.COURSE_DIR)

    @pytest.mark.superslow
    def test_notes_to_pdf_tex(self) -> None:
        hdbg.dassert_ne(self.COURSE_DIR, "")
        self._run_notes_to_pdf_tex_py(self.COURSE_DIR)

    @staticmethod
    def _run_notes_to_pdf_py(
        test_case: hunitest.TestCase,
        course_dir: str,
        output_dir: str,
        lessons: List[str],
        output_type: str,
        skip_actions: Optional[List[str]] = None,
    ) -> None:
        """
        Test preprocessing output (MD or TeX) for a set of lessons.

        :param test_case: TestCase instance for assertions
        :param course_dir: Course directory (e.g., "data605")
        :param output_dir: Output directory for test results
        :param lessons: List of lesson numbers to test
        :param output_type: Either "md" for markdown or "tex" for LaTeX output
        :param skip_actions: Additional actions to skip (in addition to cleanup_after and open)
        """
        if skip_actions is None:
            skip_actions = []
        for lesson in tqdm(lessons, desc=f"Testing {output_type.upper()} output"):
            # Get source file.
            src_name = csccouti.get_source_name(course_dir, lesson)
            input_file = os.path.join(course_dir, "lectures_source", src_name)
            # Use lesson-specific output directory to avoid file conflicts.
            lesson_dir = os.path.join(output_dir, f"lesson_{lesson}")
            hio.create_dir(lesson_dir, incremental=True)
            #
            if output_type == "md":
                output_file = os.path.join(lesson_dir, "output.pdf")
                temp_file = os.path.join(
                    lesson_dir, "tmp.notes_to_pdf.preprocess_notes.txt"
                )
            elif output_type == "tex":
                output_file = os.path.join(lesson_dir, "output.tex")
                temp_file = os.path.join(
                    lesson_dir, "tmp.notes_to_pdf.render_image2.tex"
                )
            else:
                raise ValueError(f"Unknown output_type: {output_type}")
            # Prepare command arguments.
            input_arg = shlex.quote(input_file)
            output_arg = shlex.quote(output_file)
            output_type_arg = "slides"
            toc_type_arg = "navigation"
            cleanup_action = "cleanup_after"
            open_action = "open"
            # Build skip_action arguments.
            all_skip_actions = [cleanup_action, open_action] + skip_actions
            skip_action_args = " ".join(
                f"--skip_action={action}" for action in all_skip_actions
            )
            # Build tex_only argument for tex tests.
            tex_only_arg = "--tex_only" if output_type == "tex" else ""
            # Build and execute command.
            cmd = (
                f"notes_to_pdf.py "
                f"--input={input_arg} "
                f"--output={output_arg} "
                f"--type={output_type_arg} "
                f"--toc_type={toc_type_arg} "
                f"{skip_action_args} "
                f"{tex_only_arg}"
            )
            _LOG.info(f"Running command: {cmd}")
            hsystem.system(cmd)
            sys.stdout.flush()
            # Extract and check output after preprocessing.
            hdbg.dassert_file_exists(temp_file)
            content = hio.from_file(temp_file)
            test_case.check_string(content, fuzzy_match=True, tag=lesson)
            sys.stdout.flush()
            _LOG.info(
                "Verified %s output for lesson %s", output_type.upper(), lesson
            )

    def _run_notes_to_pdf_md_py(self, course_dir: str) -> None:
        """
        Test Markdown output after preprocessing stage for all lessons.

        Verifies that the Markdown preprocessing output is correct for all
        lessons in a course. Results are saved to the output directory and
        compared using fuzzy matching.

        :param course_dir: Course directory (e.g., "data605" or "msml610")
        :param skip_actions: Additional actions to skip during preprocessing
        """
        output_dir = self.get_output_dir()
        lessons = get_lesson_numbers(course_dir)
        skip_actions = ["run_pandoc"]
        self._run_notes_to_pdf_py(
            self, course_dir, output_dir, lessons, "md", skip_actions
        )

    def _run_notes_to_pdf_tex_py(self, course_dir: str) -> None:
        """
        Test TeX output before rendering stage for all lessons.

        Verifies that the LaTeX preprocessing output is correct for all lessons
        in a course. Results are saved to the output directory and compared using
        fuzzy matching.

        :param course_dir: Course directory (e.g., "data605" or "msml610")
        """
        output_dir = self.get_output_dir()
        lessons = get_lesson_numbers(course_dir)
        self._run_notes_to_pdf_py(self, course_dir, output_dir, lessons, "tex")


# #############################################################################
# Run_gen_slides_py_TestCase
# #############################################################################


class Run_gen_slides_py_TestCase(hunitest.TestCase):
    """
    Base class for testing gen_slides.py script with course-specific lessons.
    """

    COURSE_DIR: str = ""
    FIRST_LESSON: str = ""
    SECOND_LESSON: str = ""

    @pytest.mark.slow
    def test_gen_slides_first_lesson(self) -> None:
        hdbg.dassert_ne(self.COURSE_DIR, "")
        self._run_gen_slides(self.COURSE_DIR, self.FIRST_LESSON)

    @pytest.mark.slow
    def test_gen_slides_second_lesson(self) -> None:
        hdbg.dassert_ne(self.COURSE_DIR, "")
        hdbg.dassert_ne(self.SECOND_LESSON, "")
        self._run_gen_slides(self.COURSE_DIR, self.SECOND_LESSON)

    @pytest.mark.superslow
    def test_render_all_lessons(self) -> None:
        hdbg.dassert_ne(self.COURSE_DIR, "")
        self._render_all_lessons_to_pdf(self.COURSE_DIR)

    @staticmethod
    def _run_gen_slides_py(course_dir: str) -> None:
        """
        Test that all lessons in a course can be rendered as PDF.

        :param course_dir: Course directory (e.g., "data605" or "msml610")
        """
        lessons = get_lesson_numbers(course_dir)
        for lesson in tqdm(lessons, desc="Rendering lessons to PDF"):
            cmd = f"gen_slides.py {course_dir}/{lesson} --skip_action open"
            hsystem.system(cmd)
            _LOG.info(
                "Successfully rendered %s lesson %s as PDF", course_dir, lesson
            )

    def _run_gen_slides(self, course_dir: str, lesson: str) -> None:
        """
        Run gen_slides for a lesson.
        """
        cmd = f"gen_slides.py {course_dir}/{lesson} --skip_action open"
        hsystem.system(cmd)

    def _render_all_lessons_to_pdf(self, course_dir: str) -> None:
        """
        Render all lessons in a course to PDF.

        Discovers all lesson numbers in the course directory and renders each
        one as a PDF using `gen_slides.py`. Progress is displayed via a progress
        bar. The rendered PDF is opened by default.

        :param course_dir: Course directory (e.g., "data605" or "msml610")
        """
        self._run_gen_slides_py(course_dir)
