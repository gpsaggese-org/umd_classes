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
# To handle better progress bars with pytest buffering output. 
from tqdm.auto import tqdm

import class_scripts.common_utils as csccouti
import helpers.hdbg as hdbg
import helpers.hio as hio
import helpers.hprint as hprint
import helpers.hsystem as hsystem
import helpers.hunit_test as hunitest

_LOG = logging.getLogger(__name__)


# #############################################################################
# Utils
# #############################################################################


def _get_lesson_numbers(course_dir: str) -> List[str]:
    """
    Get all lesson numbers in a course.

    :param course_dir: Course directory (data605 or msml610)
    :return: Sorted list of lesson numbers like
        ```
        ["01.1", "01.2", "02", "03", "04.1"]
        ```
    """
    _LOG.debug(hprint.to_str("course_dir"))
    lectures_source_dir = os.path.join(course_dir, "lectures_source")
    hdbg.dassert_dir_exists(lectures_source_dir)
    lessons = []
    for file in os.listdir(lectures_source_dir):
        # Match lesson numbers from filenames like "Lesson01.1-BigData.txt"
        # -> "01.1".
        match = re.match(r"Lesson(\d+(?:\.\d+)?)", file)
        if match:
            lesson_num = match.group(1)
            lessons.append(lesson_num)
    # De-dup since e.g. both "Lesson01.1-*.txt" and "Lesson01.1-*.pdf" match.
    lessons = sorted(set(lessons))
    _LOG.debug("return=%s", lessons)
    return lessons


def collect_all_lessons() -> Dict[str, List[str]]:
    """
    Collect all lessons organized by course.

    :return: Dict with course dirs as keys and lesson lists as values, e.g.,
        ```
        {"data605": ["01.1", "01.2", "02"], "msml610": ["01", "02.1"]}
        ```
    """
    all_lessons = {}
    for course_dir in csccouti.VALID_DIRS:
        all_lessons[course_dir] = _get_lesson_numbers(course_dir)
    _LOG.debug("return=%s", all_lessons)
    return all_lessons


# #############################################################################
# LessonDiscovery_TestCase
# #############################################################################


class LessonDiscovery_TestCase(hunitest.TestCase):
    """
    Base class for testing lesson discovery in a course.

    This test case ensures that:
    - All lesson files in a course are properly discovered by filename pattern
    - The expected first lesson file is present among discovered files
    - The course contains at least a minimum number of lessons

    Subclasses must set COURSE_DIR and FIRST_LESSON_FILENAME.
    """

    # Subclasses must override these.
    COURSE_DIR: str = ""
    FIRST_LESSON_FILENAME: str = ""

    @staticmethod
    def get_lesson_files(course_dir: str) -> List[str]:
        """
        Discover all lesson files in a course directory.

        :param course_dir: Course directory (data605 or msml610)
        :return: Sorted list of lesson file paths, e.g.,
            ```
            ["data605/lectures_source/Lesson01.1-BigData.txt",
            "data605/lectures_source/Lesson01.2-History.txt"]
            ```
        """
        _LOG.debug(hprint.to_str("course_dir"))
        lectures_source_dir = os.path.join(course_dir, "lectures_source")
        hdbg.dassert_dir_exists(lectures_source_dir)
        lesson_files = []
        for file in os.listdir(lectures_source_dir):
            # Match files like "Lesson01.1-BigData.txt" or
            # "Lesson02-Introduction.txt".
            if re.match(r"^Lesson\d+", file):
                file_path = os.path.join(lectures_source_dir, file)
                lesson_files.append(file_path)
        lesson_files = sorted(lesson_files)
        _LOG.debug("return=%s", lesson_files)
        return lesson_files

    def test_check_lesson_discovery(self) -> None:
        """
        Check that the first lesson file is discovered in the course.
        """
        _LOG.debug(hprint.to_str("self.COURSE_DIR self.FIRST_LESSON_FILENAME"))
        hdbg.dassert_ne(self.COURSE_DIR, "")
        hdbg.dassert_ne(self.FIRST_LESSON_FILENAME, "")
        lesson_files = self.get_lesson_files(self.COURSE_DIR)
        self.assertGreater(len(lesson_files), 0)
        # Compare only basenames since discovered paths are full file paths.
        basenames = [os.path.basename(f) for f in lesson_files]
        self.assertIn(self.FIRST_LESSON_FILENAME, basenames)

    def test_check_lesson_count(self) -> None:
        """
        Check that the course has at least the minimum expected number of
        lessons.
        """
        _LOG.debug(hprint.to_str("self.COURSE_DIR"))
        hdbg.dassert_ne(self.COURSE_DIR, "")
        min_expected_lessons = 35
        lessons = _get_lesson_numbers(self.COURSE_DIR)
        self.assertGreaterEqual(
            len(lessons),
            min_expected_lessons,
            f"{self.COURSE_DIR} should have at least {min_expected_lessons} "
            f"lessons, found {len(lessons)}",
        )
        _LOG.info("%s has %d lessons", self.COURSE_DIR, len(lessons))

    def test_check_lesson_format(self) -> None:
        """
        Check that all lesson numbers match the expected format.
        """
        _LOG.debug(hprint.to_str("self.COURSE_DIR"))
        hdbg.dassert_ne(self.COURSE_DIR, "")
        valid_lesson_pattern = r"^\d+(\.\d+)?$"
        lessons = _get_lesson_numbers(self.COURSE_DIR)
        for lesson in lessons:
            self.assertRegex(
                lesson,
                valid_lesson_pattern,
                f"Invalid lesson format '{lesson}' in {self.COURSE_DIR}",
            )

    def test_get_lesson_files(self) -> None:
        """
        Check that lesson files are found for the course.
        """
        _LOG.debug(hprint.to_str("self.COURSE_DIR"))
        hdbg.dassert_ne(self.COURSE_DIR, "")
        files = self.get_lesson_files(self.COURSE_DIR)
        self.assertGreater(len(files), 0)
        _LOG.debug("Found %d lesson files", len(files))

    def test_get_lesson_numbers(self) -> None:
        """
        Check that lesson numbers are found for the course.
        """
        _LOG.debug(hprint.to_str("self.COURSE_DIR"))
        hdbg.dassert_ne(self.COURSE_DIR, "")
        numbers = _get_lesson_numbers(self.COURSE_DIR)
        self.assertGreater(len(numbers), 0)
        _LOG.debug("Found %d lesson numbers", len(numbers))

    def test_collect_all_lessons(self) -> None:
        """
        Check that the course is present in the collected lessons.
        """
        _LOG.debug(hprint.to_str("self.COURSE_DIR"))
        hdbg.dassert_ne(self.COURSE_DIR, "")
        all_lessons = collect_all_lessons()
        self.assertIn(self.COURSE_DIR, all_lessons)


# #############################################################################
# Run_preprocess_notes_py_TestCase
# #############################################################################


class Run_preprocess_notes_py_TestCase(hunitest.TestCase):
    """
    Base class for integration tests for `preprocess_notes.py` script.

    This test case verifies that:
    - The script correctly preprocesses lesson files for different courses and
      output types (PDF, HTML, slides)
    - Table of contents options are properly handled during preprocessing
    - Preprocessed output is generated for each specified lesson and written to
      the expected output location
    """

    COURSE_DIR: str = ""

    def _run_preprocess_notes_py(
        self,
        course_dir: str,
        lessons: List[str],
        output_type: str,
        *,
        toc_type: str = "none",
    ) -> None:
        """
        Test preprocessing output for a set of lessons.

        :param course_dir: Course directory (e.g., "data605")
        :param output_dir: Output directory for test results
        :param lessons: List of lesson numbers to test
        :param output_type: Either "pdf", "html", or "slides"
        :param toc_type: Type of table of contents ("none", "pandoc_native",
            "navigation", "remove_headers")
        """
        _LOG.debug(
            hprint.to_str("course_dir output_dir lessons output_type toc_type")
        )
        scratch_dir = self.get_scratch_space()
        for lesson in tqdm(lessons, desc=f"Preprocessing {output_type.upper()}", file=sys.stderr, disable=False):
            # Get source file.
            src_name = csccouti.get_source_name(course_dir, lesson)
            input_file = os.path.join(course_dir, "lectures_source", src_name)
            # Use lesson-specific output directory to avoid file conflicts.
            lesson_dir = os.path.join(scratch_dir, f"lesson_{lesson}")
            hio.create_dir(lesson_dir, incremental=True)
            # Prepare output file path.
            output_file = os.path.join(lesson_dir, "preprocessed.md")
            # Prepare command arguments.
            input_arg = shlex.quote(input_file)
            output_arg = shlex.quote(output_file)
            # Build and execute command, e.g.,
            # ```
            # > preprocess_notes.py \
            #     --input='/path/to/lesson.txt' \
            #     --output='/out/notes.md' \
            #     --type=pdf \
            #     --toc_type=none
            # ```
            cmd = (
                f"preprocess_notes.py "
                f"--input={input_arg} "
                f"--output={output_arg} "
                f"--type={output_type} "
                f"--toc_type={toc_type}"
            )
            _LOG.debug("Running command: %s", cmd)
            hsystem.system(cmd)
            #sys.stdout.flush()
            # Extract and check output after preprocessing.
            hdbg.dassert_file_exists(output_file)
            content = hio.from_file(output_file)
            self.check_string(content, fuzzy_match=True, tag=lesson)
            #sys.stdout.flush()
            _LOG.debug(
                "Verified %s preprocessing for lesson %s",
                output_type.upper(),
                lesson,
            )

    @pytest.mark.superslow
    def test_preprocess_notes_pdf(self) -> None:
        """
        Test preprocessing notes to PDF format.
        """
        _LOG.debug(hprint.to_str("self.COURSE_DIR"))
        hdbg.dassert_ne(self.COURSE_DIR, "")
        lessons = _get_lesson_numbers(self.COURSE_DIR)
        # Test PDF output type.
        output_type = "pdf"
        self._run_preprocess_notes_py(
            self.COURSE_DIR, lessons, output_type
        )

    @pytest.mark.superslow
    def test_preprocess_notes_html(self) -> None:
        """
        Test preprocessing notes to HTML format.
        """
        _LOG.debug(hprint.to_str("self.COURSE_DIR"))
        hdbg.dassert_ne(self.COURSE_DIR, "")
        lessons = _get_lesson_numbers(self.COURSE_DIR)
        # Test HTML output type.
        output_type = "html"
        self._run_preprocess_notes_py(
            self.COURSE_DIR, lessons, output_type
        )

    @pytest.mark.superslow
    def test_preprocess_notes_slides(self) -> None:
        """
        Test preprocessing notes to slides format.
        """
        _LOG.debug(hprint.to_str("self.COURSE_DIR"))
        hdbg.dassert_ne(self.COURSE_DIR, "")
        lessons = _get_lesson_numbers(self.COURSE_DIR)
        # Test slides output type.
        output_type = "slides"
        self._run_preprocess_notes_py(
            self.COURSE_DIR, lessons, output_type
        )


# #############################################################################
# Run_notes_to_pdf_py_TestCase
# #############################################################################


@pytest.mark.superslow
class Run_notes_to_pdf_py_TestCase(hunitest.TestCase):
    """
    Base class for integration tests for slide generation using `notes_to_pdf.py`.

    # - Tests that Markdown and LaTeX files (PDF or TEX) can be generated from
    #   lesson source notes for a given course
    # - Checks output correctness for multiple lessons
    # - Ensures that preprocessing and file conversion steps are properly
    #   functioning
    # - Verifies both "md" (Markdown→PDF) and "tex" (LaTeX) output types
    # - Runs the conversion script on all selected lessons and asserts that
    #   outputs are produced without error
    """

    COURSE_DIR: str = ""

    def _run_notes_to_pdf_py(
        self,
        course_dir: str,
        output_dir: str,
        lessons: List[str],
        output_type: str,
        skip_actions: Optional[List[str]] = None,
    ) -> None:
        """
        Test notes_to_pdf.py output (MD or TeX) for a set of lessons.

        :param course_dir: Course directory (e.g., "data605")
        :param output_dir: Output directory for test results
        :param lessons: List of lesson numbers to test
        :param output_type: Either "md" for markdown or "tex" for LaTeX output
        :param skip_actions: Additional actions to skip (in addition to
            cleanup_after and open)
        """
        _LOG.debug(
            hprint.to_str(
                "course_dir output_dir lessons output_type skip_actions"
            )
        )
        if skip_actions is None:
            skip_actions = []
        for lesson in tqdm(
            lessons, desc=f"Testing {output_type.upper()} output"
        ):
            # Get source file.
            src_name = csccouti.get_source_name(course_dir, lesson)
            input_file = os.path.join(course_dir, "lectures_source", src_name)
            # Use lesson-specific output directory to avoid file conflicts.
            lesson_dir = os.path.join(output_dir, f"lesson_{lesson}")
            hio.create_dir(lesson_dir, incremental=True)
            #
            # TODO(ai_gp): Use _extract_slide_metadata() to decide if the slides
            # for a lesson are typ or latex
            #
            # TODO(ai_gp): Add an explanation of what output_file and temp_file
            # mean.
            # `output_file` is the final rendered artifact (PDF/TeX/Typst);
            # `temp_file` is the intermediate file whose content is checked
            # against the expected test output via `check_string()`.
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
            elif output_type == "typ":
                output_file = os.path.join(lesson_dir, "output.typ")
                # TODO(ai_gp): No intermediate file name is set for "typ" yet,
                # so `temp_file` resolves to `lesson_dir` itself.
                temp_file = os.path.join(
                    lesson_dir, ""
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
            self.check_string(content, fuzzy_match=True, tag=lesson)
            sys.stdout.flush()
            _LOG.info(
                "Verified %s output for lesson %s", output_type.upper(), lesson
            )

    @pytest.mark.superslow
    def test_notes_to_pdf_md(self) -> None:
        """
        Test converting notes to PDF (markdown intermediate).
        """
        _LOG.debug(hprint.to_str("self.COURSE_DIR"))
        hdbg.dassert_ne(self.COURSE_DIR, "")
        output_dir = self.get_output_dir()
        lessons = _get_lesson_numbers(self.COURSE_DIR)
        skip_actions = ["run_pandoc"]
        self._run_notes_to_pdf_py(
            self.COURSE_DIR, output_dir, lessons, "md", skip_actions
        )

    @pytest.mark.superslow
    def test_notes_to_pdf_tex(self) -> None:
        """
        Test converting notes to PDF (TeX intermediate).
        """
        _LOG.debug(hprint.to_str("self.COURSE_DIR"))
        hdbg.dassert_ne(self.COURSE_DIR, "")
        output_dir = self.get_output_dir()
        lessons = _get_lesson_numbers(self.COURSE_DIR)
        self._run_notes_to_pdf_py(
            self.COURSE_DIR, output_dir, lessons, "tex"
        )

    @pytest.mark.superslow
    def test_notes_to_pdf_typ(self) -> None:
        """
        Test converting notes to PDF (Typst intermediate).
        """
        _LOG.debug(hprint.to_str("self.COURSE_DIR"))
        hdbg.dassert_ne(self.COURSE_DIR, "")
        output_dir = self.get_output_dir()
        lessons = _get_lesson_numbers(self.COURSE_DIR)
        self._run_notes_to_pdf_py(
            self.COURSE_DIR, output_dir, lessons, "typ"
        )
   

# #############################################################################
# Run_gen_slides_py_TestCase
# #############################################################################


class Run_gen_slides_py_TestCase(hunitest.TestCase):
    """
    Base class for testing `gen_slides.py` script with course-specific lessons.

    Tests performed:
    - Verify that `gen_slides.py` can generate TeX output for the first lesson.
    - Verify that `gen_slides.py` can generate TeX output for the second lesson.
    - Render and check that TeX output is generated for all lessons in the course.
    """

    COURSE_DIR: str = ""
    FIRST_LESSON: str = ""
    SECOND_LESSON: str = ""

    @staticmethod
    def _run_gen_slides(course_dir: str, lesson: str) -> None:
        """
        Run gen_slides for a lesson, generating only TeX output.
        """
        _LOG.debug(hprint.to_str("course_dir lesson"))
        cmd = (
            f"gen_slides.py {course_dir}/{lesson} --skip_action open --tex_only"
        )
        hsystem.system(cmd)

    @pytest.mark.slow
    def test_gen_slides_first_lesson(self) -> None:
        """
        Test generating slides for the first lesson.
        """
        _LOG.debug(hprint.to_str("self.COURSE_DIR self.FIRST_LESSON"))
        hdbg.dassert_ne(self.COURSE_DIR, "")
        self._run_gen_slides(self.COURSE_DIR, self.FIRST_LESSON)

    @pytest.mark.slow
    def test_gen_slides_second_lesson(self) -> None:
        """
        Test generating slides for the second lesson.
        """
        _LOG.debug(hprint.to_str("self.COURSE_DIR self.SECOND_LESSON"))
        hdbg.dassert_ne(self.COURSE_DIR, "")
        hdbg.dassert_ne(self.SECOND_LESSON, "")
        self._run_gen_slides(self.COURSE_DIR, self.SECOND_LESSON)

    @pytest.mark.superslow
    def test_render_all_lessons(self) -> None:
        """
        Test generating slides for all the lessons.
        """
        _LOG.debug(hprint.to_str("self.COURSE_DIR"))
        hdbg.dassert_ne(self.COURSE_DIR, "")
        lessons = _get_lesson_numbers(self.COURSE_DIR)
        for lesson in tqdm(lessons, desc="Rendering lessons to TeX"):
            cmd = f"gen_slides.py {self.COURSE_DIR}/{lesson} --skip_action open --tex_only"
            hsystem.system(cmd)
            _LOG.info(
                "Successfully rendered %s lesson %s as TeX",
                self.COURSE_DIR,
                lesson,
            )
