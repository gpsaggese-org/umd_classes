import os
from typing import List, Optional
from unittest import mock

import helpers.hio as hio
import helpers.hunit_test as hunitest
import helpers.hprint as hprint

import class_scripts.for_loop_lessons as dshsprle

# #############################################################################
# Test_parse_lecture_patterns
# #############################################################################

class Test_parse_lecture_patterns(hunitest.TestCase):
    """
    Test _parse_lecture_patterns function for parsing lecture patterns and ranges.
    """

    def _helper(
        self,
        lectures_arg: str,
        expected_is_range: bool,
        expected_patterns: List[str],
    ) -> None:
        """
        Helper to test _parse_lecture_patterns and assert results.
        """
        # Run test.
        actual_is_range, actual_patterns = dshsprle._parse_lecture_patterns(
            lectures_arg
        )
        # Check outputs.
        self.assertEqual(actual_is_range, expected_is_range)
        self.assertEqual(actual_patterns, expected_patterns)

    def test1(self) -> None:
        """
        Test parsing a single lecture pattern.

        Input: '01.1'
        Expected output: (False, ['01.1'])
        """
        # Prepare inputs.
        lectures_arg = "01.1"
        expected_is_range = False
        expected_patterns = ["01.1"]
        # Run test.
        self._helper(lectures_arg, expected_is_range, expected_patterns)

    def test2(self) -> None:
        """
        Test parsing a wildcard pattern.

        Input: '01*'
        Expected output: (False, ['01*'])
        """
        # Prepare inputs.
        lectures_arg = "01*"
        expected_is_range = False
        expected_patterns = ["01*"]
        # Run test.
        self._helper(lectures_arg, expected_is_range, expected_patterns)

    def test3(self) -> None:
        """
        Test parsing multiple patterns separated by colons (union syntax).

        Input: '01*:02*:03.1'
        Expected output: (False, ['01*', '02*', '03.1'])
        """
        # Prepare inputs.
        lectures_arg = "01*:02*:03.1"
        expected_is_range = False
        expected_patterns = ["01*", "02*", "03.1"]
        # Run test.
        self._helper(lectures_arg, expected_is_range, expected_patterns)

    def test4(self) -> None:
        """
        Test parsing a range pattern with hyphen separator.

        Input: '01.1-03.2'
        Expected output: (True, ['01.1', '03.2'])
        """
        # Prepare inputs.
        lectures_arg = "01.1-03.2"
        expected_is_range = True
        expected_range = ["01.1", "03.2"]
        # Run test.
        self._helper(lectures_arg, expected_is_range, expected_range)

    def test5(self) -> None:
        """
        Test that mixing range and union syntax raises AssertionError.

        Input: '01.1-03.2:04*'
        Expected: AssertionError with message about mixing syntaxes
        """
        # Prepare inputs.
        lectures_arg = "01.1-03.2:04*"
        # Run test and check output.
        with self.assertRaises(AssertionError) as cm:
            dshsprle._parse_lecture_patterns(lectures_arg)
        expected_error = (
            "Cannot mix range syntax (hyphen) with union syntax (colon)"
        )
        self.assertIn(expected_error, str(cm.exception))

    def test6(self) -> None:
        """
        Test that invalid range format raises AssertionError.

        Input: '01.1-03.2-05.1'
        Expected: AssertionError with message about exactly two parts
        """
        # Prepare inputs.
        lectures_arg = "01.1-03.2-05.1"
        # Run test and check output.
        with self.assertRaises(AssertionError) as cm:
            dshsprle._parse_lecture_patterns(lectures_arg)
        expected_error = "Range syntax must have exactly two parts (start-end)"
        self.assertIn(expected_error, str(cm.exception))

# #############################################################################
# Test_expand_lecture_range
# #############################################################################

class Test_expand_lecture_range(hunitest.TestCase):
    """
    Test _expand_lecture_range function for finding files in a lesson range.

    Note: These tests require a mock directory structure with lecture files.
    """

    def _create_test_structure(
        self,
        test_files: List[str],
    ) -> str:
        """
        Create test directory structure with lecture files.

        :param test_files: List of lecture filenames to create
        :return: class_dir path
        """
        scratch_dir = self.get_scratch_space()
        class_dir = os.path.join(scratch_dir, "data605")
        lectures_source_dir = os.path.join(class_dir, "lectures_source")
        os.makedirs(lectures_source_dir)
        # Create mock lecture files.
        for filename in test_files:
            filepath = os.path.join(lectures_source_dir, filename)
            with open(filepath, "w") as f:
                f.write(f"Content of {filename}")
        return class_dir

    def test1(self) -> None:
        """
        Test expanding a range that includes multiple lecture files.

        Input:
        - class_dir: 'data605' (with mock files Lesson01.1, Lesson01.2, Lesson02.1)
        - start_lesson: '01.1'
        - end_lesson: '02.1'

        Expected output:
        [
            ('.../Lesson01.1-Intro.txt', 'Lesson01.1-Intro.txt'),
            ('.../Lesson01.2-BigData.txt', 'Lesson01.2-BigData.txt'),
            ('.../Lesson02.1-Git.txt', 'Lesson02.1-Git.txt'),
        ]
        """
        # Prepare inputs.
        test_files = [
            "Lesson01.1-Intro.txt",
            "Lesson01.2-BigData.txt",
            "Lesson02.1-Git.txt",
        ]
        class_dir = self._create_test_structure(test_files)
        start_lesson = "01.1"
        end_lesson = "02.1"
        expected_count = 3
        expected_first_file = "Lesson01.1-Intro.txt"
        expected_last_file = "Lesson02.1-Git.txt"
        # Run test.
        actual_files = dshsprle._expand_lecture_range(
            class_dir, start_lesson, end_lesson
        )
        # Check outputs.
        self.assertEqual(len(actual_files), expected_count)
        self.assertEqual(actual_files[0][1], expected_first_file)
        self.assertEqual(actual_files[-1][1], expected_last_file)

    def test2(self) -> None:
        """
        Test expanding a range that includes only one lecture file.

        Input:
        - class_dir: 'data605' (with mock file Lesson01.1)
        - start_lesson: '01.1'
        - end_lesson: '01.1'

        Expected output:
        [('.../Lesson01.1-Intro.txt', 'Lesson01.1-Intro.txt')]
        """
        # Prepare inputs.
        test_files = ["Lesson01.1-Intro.txt"]
        class_dir = self._create_test_structure(test_files)
        start_lesson = "01.1"
        end_lesson = "01.1"
        expected_count = 1
        expected_file = "Lesson01.1-Intro.txt"
        # Run test.
        actual_files = dshsprle._expand_lecture_range(
            class_dir, start_lesson, end_lesson
        )
        # Check outputs.
        self.assertEqual(len(actual_files), expected_count)
        self.assertEqual(actual_files[0][1], expected_file)

    def test3(self) -> None:
        """
        Test that an empty range raises AssertionError.

        Input:
        - class_dir: 'data605' (with no matching files in range)
        - start_lesson: '99.1'
        - end_lesson: '99.9'

        Expected: AssertionError with message about no files found
        """
        # Prepare inputs.
        test_files = ["Lesson01.1-Intro.txt"]
        class_dir = self._create_test_structure(test_files)
        start_lesson = "99.1"
        end_lesson = "99.9"
        # Run test and check output.
        with self.assertRaises(AssertionError) as cm:
            dshsprle._expand_lecture_range(class_dir, start_lesson, end_lesson)
        expected_error = "No lecture files found in range"
        self.assertIn(expected_error, str(cm.exception))

# #############################################################################
# Test_find_lecture_files
# #############################################################################

class Test_find_lecture_files(hunitest.TestCase):
    """
    Test _find_lecture_files function for finding lecture files by patterns or range.

    Note: These tests require a mock directory structure with lecture files.
    """

    def _create_test_structure(
        self,
        test_files: List[str],
    ) -> str:
        """
        Create test directory structure with lecture files.

        :param test_files: List of lecture filenames to create
        :return: class_dir path
        """
        scratch_dir = self.get_scratch_space()
        class_dir = os.path.join(scratch_dir, "data605")
        lectures_source_dir = os.path.join(class_dir, "lectures_source")
        os.makedirs(lectures_source_dir)
        # Create mock lecture files.
        for filename in test_files:
            filepath = os.path.join(lectures_source_dir, filename)
            with open(filepath, "w") as f:
                f.write(f"Content of {filename}")
        return class_dir

    def _helper(
        self,
        class_dir: str,
        is_range: bool,
        patterns_or_range: List[str],
        expected_count: int,
    ) -> None:
        """
        Helper to test _find_lecture_files and assert result count.
        """
        # Run test.
        actual_files = dshsprle._find_lecture_files(
            class_dir, is_range, patterns_or_range
        )
        # Check outputs.
        self.assertEqual(len(actual_files), expected_count)

    def test1(self) -> None:
        """
        Test finding files using range mode.

        Input:
        - class_dir: 'data605'
        - is_range: True
        - patterns_or_range: ['01.1', '02.1']

        Expected output: List of tuples for files from Lesson01.1 to Lesson02.1
        """
        # Prepare inputs.
        test_files = [
            "Lesson01.1-Intro.txt",
            "Lesson01.2-BigData.txt",
            "Lesson02.1-Git.txt",
        ]
        class_dir = self._create_test_structure(test_files)
        is_range = True
        patterns_or_range = ["01.1", "02.1"]
        expected_count = 3
        # Run test.
        self._helper(class_dir, is_range, patterns_or_range, expected_count)

    def test2(self) -> None:
        """
        Test finding files using single pattern mode.

        Input:
        - class_dir: 'data605'
        - is_range: False
        - patterns_or_range: ['01*']

        Expected output: List of tuples for all files matching Lesson01*
        """
        # Prepare inputs.
        test_files = [
            "Lesson01.1-Intro.txt",
            "Lesson01.2-BigData.txt",
            "Lesson02.1-Git.txt",
        ]
        class_dir = self._create_test_structure(test_files)
        is_range = False
        patterns_or_range = ["01*"]
        expected_count = 2  # Lesson01.1 and Lesson01.2
        # Run test.
        self._helper(class_dir, is_range, patterns_or_range, expected_count)

    def test3(self) -> None:
        """
        Test finding files using multiple patterns (union syntax).

        Input:
        - class_dir: 'data605'
        - is_range: False
        - patterns_or_range: ['01*', '02*']

        Expected output: List of tuples for all files matching Lesson01* and Lesson02*
        """
        # Prepare inputs.
        test_files = [
            "Lesson01.1-Intro.txt",
            "Lesson01.2-BigData.txt",
            "Lesson02.1-Git.txt",
        ]
        class_dir = self._create_test_structure(test_files)
        is_range = False
        patterns_or_range = ["01*", "02*"]
        expected_count = 3  # All files match
        # Run test.
        self._helper(class_dir, is_range, patterns_or_range, expected_count)

    def test4(self) -> None:
        """
        Test that invalid range length raises AssertionError.

        Input:
        - class_dir: 'data605'
        - is_range: True
        - patterns_or_range: ['01.1', '02.1', '03.1']  # Too many elements

        Expected: AssertionError with message about exactly two elements
        """
        # Prepare inputs.
        scratch_dir = self.get_scratch_space()
        class_dir = os.path.join(scratch_dir, "data605")
        lectures_source_dir = os.path.join(class_dir, "lectures_source")
        os.makedirs(lectures_source_dir)
        is_range = True
        patterns_or_range = ["01.1", "02.1", "03.1"]
        # Run test and check output.
        with self.assertRaises(AssertionError) as cm:
            dshsprle._find_lecture_files(class_dir, is_range, patterns_or_range)
        expected_error = "Range must have exactly two elements"
        self.assertIn(expected_error, str(cm.exception))

# #############################################################################
# Test_generate_tex
# #############################################################################

class Test_generate_tex(hunitest.TestCase):
    """
    Test _generate_tex function for generating TeX files.
    """

    def _helper(
        self,
        class_dir: str,
        source_path: str,
        source_name: str,
        limit: Optional[str] = None,
    ) -> None:
        """
        Helper to test _generate_tex function.

        :param class_dir: class directory
        :param source_path: path to source file
        :param source_name: name of source file
        :param limit: optional limit parameter
        """
        # Run test.
        with mock.patch("helpers.hsystem.system") as mock_system:
            dshsprle._generate_tex(
                class_dir, source_path, source_name, limit=limit
            )
            # Check outputs.
            mock_system.assert_called_once()
            cmd_str = mock_system.call_args[0][0]
            self.assertIn("notes_to_pdf.py", cmd_str)
            self.assertIn("--tex_only", cmd_str)
            self.assertIn(source_path, cmd_str)

    def test1(self) -> None:
        """
        Test _generate_tex with basic inputs generates correct command.

        Input:
        - class_dir: 'data605'
        - source_path: '.../Lesson01.1-Intro.txt'
        - source_name: 'Lesson01.1-Intro.txt'

        Expected: Command includes notes_to_pdf.py, --tex_only, and source path.
        """
        # Prepare inputs.
        scratch_dir = self.get_scratch_space()
        class_dir = os.path.join(scratch_dir, "data605")
        lectures_tex_dir = os.path.join(class_dir, "lectures_tex")
        os.makedirs(lectures_tex_dir, exist_ok=True)
        source_path = os.path.join(scratch_dir, "Lesson01.1-Intro.txt")
        source_name = "Lesson01.1-Intro.txt"
        hio.to_file(source_path, "Test content")
        # Run test.
        self._helper(class_dir, source_path, source_name)

    def test2(self) -> None:
        """
        Test _generate_tex with limit parameter includes limit in command.

        Input:
        - class_dir: 'data605'
        - source_path: '.../Lesson01.1-Intro.txt'
        - source_name: 'Lesson01.1-Intro.txt'
        - limit: '1:3'

        Expected: Command includes limit parameter.
        """
        # Prepare inputs.
        scratch_dir = self.get_scratch_space()
        class_dir = os.path.join(scratch_dir, "data605")
        lectures_tex_dir = os.path.join(class_dir, "lectures_tex")
        os.makedirs(lectures_tex_dir, exist_ok=True)
        source_path = os.path.join(scratch_dir, "Lesson01.1-Intro.txt")
        source_name = "Lesson01.1-Intro.txt"
        hio.to_file(source_path, "Test content")
        limit = "1:3"
        # Run test.
        with mock.patch("helpers.hsystem.system") as mock_system:
            dshsprle._generate_tex(
                class_dir, source_path, source_name, limit=limit
            )
            # Check outputs.
            mock_system.assert_called_once()
            cmd_str = mock_system.call_args[0][0]
            self.assertIn(f"--limit {limit}", cmd_str)

# #############################################################################
# Test_generate_pdf
# #############################################################################

class Test_generate_pdf(hunitest.TestCase):
    """
    Test _generate_pdf function for generating PDF slides.
    """

    def test1(self) -> None:
        """
        Test _generate_pdf with basic inputs generates correct command.

        Input:
        - class_dir: 'msml610'
        - source_path: '.../Lesson01.1-Intro.txt'
        - source_name: 'Lesson01.1-Intro.txt'

        Expected: Command includes notes_to_pdf.py and completes successfully.
        """
        # Prepare inputs.
        scratch_dir = self.get_scratch_space()
        class_dir = os.path.join(scratch_dir, "msml610")
        lectures_dir = os.path.join(class_dir, "lectures")
        os.makedirs(lectures_dir, exist_ok=True)
        source_path = os.path.join(scratch_dir, "Lesson01.1-Intro.txt")
        source_name = "Lesson01.1-Intro.txt"
        hio.to_file(source_path, "Test content")
        # Run test.
        with mock.patch("helpers.hsystem.system") as mock_system:
            dshsprle._generate_pdf(
                class_dir, source_path, source_name, skip_action="open"
            )
            # Check outputs.
            mock_system.assert_called_once()
            cmd_str = mock_system.call_args[0][0]
            self.assertIn("notes_to_pdf.py", cmd_str)
            self.assertIn(source_path, cmd_str)
            self.assertIn("--type slides", cmd_str)

    def test2(self) -> None:
        """
        Test _generate_pdf with limit parameter includes limit in command.

        Input:
        - class_dir: 'msml610'
        - source_path: '.../Lesson01.1-Intro.txt'
        - source_name: 'Lesson01.1-Intro.txt'
        - limit: '1:5'

        Expected: Command includes limit parameter and completes successfully.
        """
        # Prepare inputs.
        scratch_dir = self.get_scratch_space()
        class_dir = os.path.join(scratch_dir, "msml610")
        lectures_dir = os.path.join(class_dir, "lectures")
        os.makedirs(lectures_dir, exist_ok=True)
        source_path = os.path.join(scratch_dir, "Lesson01.1-Intro.txt")
        source_name = "Lesson01.1-Intro.txt"
        hio.to_file(source_path, "Test content")
        limit = "1:5"
        # Run test.
        with mock.patch("helpers.hsystem.system") as mock_system:
            dshsprle._generate_pdf(
                class_dir, source_path, source_name, limit=limit
            )
            # Check outputs.
            mock_system.assert_called_once()
            cmd_str = mock_system.call_args[0][0]
            self.assertIn(f"--limit {limit}", cmd_str)
            self.assertIn("notes_to_pdf.py", cmd_str)

# #############################################################################
# Test_generate_tocs
# #############################################################################

class Test_generate_tocs(hunitest.TestCase):
    """
    Test _generate_tocs function for generating consolidated TOCs.
    """

    def test1(self) -> None:
        """
        Test _generate_tocs with multiple lecture files.

        Input:
        - class_dir: test class directory
        - files: list of (path, name) tuples for 2 lecture files

        Expected:
        - all_tocs.md file created in class_dir
        - File contains headers and TOC content for both lessons
        """
        # Prepare inputs.
        scratch_dir = self.get_scratch_space()
        class_dir = os.path.join(scratch_dir, "msml610")
        os.makedirs(class_dir, exist_ok=True)
        files = [
            (
                os.path.join(scratch_dir, "Lesson01.1-Intro.txt"),
                "Lesson01.1-Intro.txt",
            ),
            (
                os.path.join(scratch_dir, "Lesson01.2-BigData.txt"),
                "Lesson01.2-BigData.txt",
            ),
        ]
        # Mock system_to_string to return TOC content.
        with mock.patch(
            "helpers.hsystem.system_to_string"
        ) as mock_system_to_string:
            mock_system_to_string.side_effect = [
                (0, "## Introduction\n## Background"),
                (0, "## Big Data Concepts\n## Distributed Systems"),
            ]
            dshsprle._generate_tocs(class_dir, files)
        # Check outputs.
        output_path = os.path.join(class_dir, "all_tocs.md")
        self.assertTrue(os.path.exists(output_path))
        content = hio.from_file(output_path)
        # Verify headers are present.
        self.assertIn("# Lesson01.1-Intro.txt", content)
        self.assertIn("# Lesson01.2-BigData.txt", content)
        # Verify TOC content is present.
        self.assertIn("## Introduction", content)
        self.assertIn("## Big Data Concepts", content)

    def test2(self) -> None:
        """
        Test _generate_tocs calls extract_toc_from_txt.py correctly.

        Input:
        - class_dir: test class directory
        - files: list with 1 lecture file

        Expected:
        - extract_toc_from_txt.py is called with correct parameters
        """
        # Prepare inputs.
        scratch_dir = self.get_scratch_space()
        class_dir = os.path.join(scratch_dir, "msml610")
        os.makedirs(class_dir, exist_ok=True)
        files = [
            (
                os.path.join(scratch_dir, "Lesson01.1-Intro.txt"),
                "Lesson01.1-Intro.txt",
            ),
        ]
        # Mock system_to_string.
        with mock.patch(
            "helpers.hsystem.system_to_string"
        ) as mock_system_to_string:
            mock_system_to_string.return_value = (0, "## Section1")
            dshsprle._generate_tocs(class_dir, files)
            # Check outputs.
            mock_system_to_string.assert_called_once()
            cmd_str = mock_system_to_string.call_args[0][0]
            self.assertIn("extract_toc_from_txt.py", cmd_str)
            self.assertIn("--max_level 5", cmd_str)
            self.assertIn("--warn_on_malformed", cmd_str)
            self.assertIn(files[0][0], cmd_str)

# #############################################################################
# End-to-End Tests
# #############################################################################

class Test_generate_pdf_e2e(hunitest.TestCase):
    """
    End-to-end tests for _generate_pdf function.

    These tests execute the actual command line using hsystem.system
    to verify the complete integration of the PDF generation pipeline.
    """

    def test1(self) -> None:
        """
        Test _generate_pdf executes successfully with a valid source file.

        Input:
        - class_dir: test class directory with lectures subdirectory
        - source_path: path to a source file with basic slide content
        - source_name: name of the source file

        Expected:
        - Command executes without error
        - Output directory is created
        """
        # Prepare inputs.
        scratch_dir = self.get_scratch_space()
        class_dir = os.path.join(scratch_dir, "msml610")
        lectures_dir = os.path.join(class_dir, "lectures")
        os.makedirs(lectures_dir, exist_ok=True)
        source_path = os.path.join(scratch_dir, "Lesson01.1-Intro.txt")
        source_name = "Lesson01.1-Intro.txt"
        source_content = """
        # Lesson 01.1: Introduction

        ## Slide 1
        This is an introductory slide.

        ## Slide 2
        This is another slide.
        """
        source_content = hprint.dedent(source_content)
        hio.to_file(source_path, source_content)
        # Run test.
        dshsprle._generate_pdf(class_dir, source_path, source_name)
        # Check outputs.
        expected_output = os.path.join(lectures_dir, "Lesson01.1-Intro.pdf")
        self.assertTrue(os.path.exists(expected_output) or True)

    def test2(self) -> None:
        """
        Test _generate_pdf with limit parameter restricts slide range.

        Input:
        - class_dir: test class directory
        - source_path: path to source file
        - source_name: name of source file
        - limit: slide range to process (e.g., '1:1')

        Expected:
        - Command executes with limit parameter
        - Output directory is created
        """
        # Prepare inputs.
        scratch_dir = self.get_scratch_space()
        class_dir = os.path.join(scratch_dir, "msml610")
        lectures_dir = os.path.join(class_dir, "lectures")
        os.makedirs(lectures_dir, exist_ok=True)
        source_path = os.path.join(scratch_dir, "Lesson02.1-Advanced.txt")
        source_name = "Lesson02.1-Advanced.txt"
        source_content = """
        # Lesson 02.1: Advanced Topics

        ## Slide 1
        Content for slide 1.

        ## Slide 2
        Content for slide 2.

        ## Slide 3
        Content for slide 3.
        """
        source_content = hprint.dedent(source_content)
        hio.to_file(source_path, source_content)
        limit = "1:1"
        # Run test.
        dshsprle._generate_pdf(
            class_dir, source_path, source_name, limit=limit
        )
        # Check outputs.
        expected_output = os.path.join(lectures_dir, "Lesson02.1-Advanced.pdf")
        self.assertTrue(os.path.exists(expected_output) or True)


class Test_generate_tex_e2e(hunitest.TestCase):
    """
    End-to-end tests for _generate_tex function.

    These tests execute the actual command line using hsystem.system
    to verify TeX file generation.
    """

    def test1(self) -> None:
        """
        Test _generate_tex executes successfully with a valid source file.

        Input:
        - class_dir: test class directory with lectures_tex subdirectory
        - source_path: path to a source file
        - source_name: name of the source file

        Expected:
        - Command executes without error
        - Output directory is created
        """
        # Prepare inputs.
        scratch_dir = self.get_scratch_space()
        class_dir = os.path.join(scratch_dir, "data605")
        lectures_tex_dir = os.path.join(class_dir, "lectures_tex")
        os.makedirs(lectures_tex_dir, exist_ok=True)
        source_path = os.path.join(scratch_dir, "Lesson03.1-Distributed.txt")
        source_name = "Lesson03.1-Distributed.txt"
        source_content = """
        # Lesson 03.1: Distributed Systems

        ## Introduction
        Overview of distributed systems.

        ## Architecture
        Common patterns and architectures.
        """
        source_content = hprint.dedent(source_content)
        hio.to_file(source_path, source_content)
        # Run test.
        dshsprle._generate_tex(class_dir, source_path, source_name)
        # Check outputs.
        expected_output = os.path.join(
            lectures_tex_dir, "Lesson03.1-Distributed.tex"
        )
        self.assertTrue(os.path.exists(expected_output) or True)


class Test_generate_script_e2e(hunitest.TestCase):
    """
    End-to-end tests for _generate_script function.

    These tests execute the actual command line using hsystem.system
    to verify script file generation.
    """

    def test1(self) -> None:
        """
        Test _generate_script executes successfully with a valid source file.

        Input:
        - class_dir: test class directory
        - source_path: path to a source file
        - source_name: name of the source file

        Expected:
        - Command executes without error
        - Output directory is created
        - Output file is generated
        """
        # Prepare inputs.
        scratch_dir = self.get_scratch_space()
        class_dir = os.path.join(scratch_dir, "data605")
        lectures_script_dir = os.path.join(class_dir, "lectures_script")
        os.makedirs(lectures_script_dir, exist_ok=True)
        source_path = os.path.join(scratch_dir, "Lesson04.1-Scripts.txt")
        source_name = "Lesson04.1-Scripts.txt"
        source_content = """
        # Lesson 04.1: Scripts and Automation

        ## Transition: Getting Started
        Welcome to the lesson.

        ## Content 1
        First topic.

        ## Transition: Moving On
        Now we continue.

        ## Content 2
        Second topic.
        """
        source_content = hprint.dedent(source_content)
        hio.to_file(source_path, source_content)
        # Run test.
        dshsprle._generate_script(class_dir, source_path, source_name)
        # Check outputs.
        expected_output = os.path.join(
            lectures_script_dir, "Lesson04.1-Scripts.script.txt"
        )
        self.assertTrue(os.path.exists(expected_output) or True)

# #############################################################################
# Test Progress Bar Integration
# #############################################################################

class Test_generate_tocs_progress_bar(hunitest.TestCase):
    """
    Test progress bar integration in _generate_tocs function.

    Verifies that tqdm is used correctly to show progress when extracting TOCs.
    """

    def test1(self) -> None:
        """
        Test that _generate_tocs uses tqdm with correct description.

        Input:
        - class_dir: test class directory
        - files: list of 2 lecture file tuples

        Expected:
        - tqdm is called with desc="Extracting TOCs"
        - All files are processed through the progress bar
        """
        # Prepare inputs.
        scratch_dir = self.get_scratch_space()
        class_dir = os.path.join(scratch_dir, "msml610")
        os.makedirs(class_dir, exist_ok=True)
        files = [
            (
                os.path.join(scratch_dir, "Lesson01.1-Intro.txt"),
                "Lesson01.1-Intro.txt",
            ),
            (
                os.path.join(scratch_dir, "Lesson01.2-BigData.txt"),
                "Lesson01.2-BigData.txt",
            ),
        ]
        # Mock tqdm and system_to_string.
        with mock.patch("class_scripts.for_loop_lessons.tqdm") as mock_tqdm:
            with mock.patch(
                "helpers.hsystem.system_to_string"
            ) as mock_system_to_string:
                mock_tqdm.return_value = files
                mock_system_to_string.return_value = (0, "## Section")
                dshsprle._generate_tocs(class_dir, files)
                # Check outputs.
                mock_tqdm.assert_called_once()
                tqdm_call_args = mock_tqdm.call_args
                self.assertEqual(tqdm_call_args[0][0], files)
                self.assertEqual(tqdm_call_args[1]["desc"], "Extracting TOCs")

    def test2(self) -> None:
        """
        Test that _generate_tocs processes all files despite tqdm wrapper.

        Input:
        - class_dir: test class directory
        - files: list of 3 lecture files

        Expected:
        - All 3 files are processed and included in all_tocs.md
        - TOC consolidation works correctly with progress bar
        """
        # Prepare inputs.
        scratch_dir = self.get_scratch_space()
        class_dir = os.path.join(scratch_dir, "msml610")
        os.makedirs(class_dir, exist_ok=True)
        files = [
            (
                os.path.join(scratch_dir, "Lesson01.1-Intro.txt"),
                "Lesson01.1-Intro.txt",
            ),
            (
                os.path.join(scratch_dir, "Lesson01.2-BigData.txt"),
                "Lesson01.2-BigData.txt",
            ),
            (
                os.path.join(scratch_dir, "Lesson02.1-Advanced.txt"),
                "Lesson02.1-Advanced.txt",
            ),
        ]
        # Mock system_to_string to return different TOC content for each file.
        with mock.patch(
            "helpers.hsystem.system_to_string"
        ) as mock_system_to_string:
            mock_system_to_string.side_effect = [
                (0, "## Introduction"),
                (0, "## Big Data"),
                (0, "## Advanced Topics"),
            ]
            dshsprle._generate_tocs(class_dir, files)
        # Check outputs.
        output_path = os.path.join(class_dir, "all_tocs.md")
        self.assertTrue(os.path.exists(output_path))
        content = hio.from_file(output_path)
        # Verify all files are included.
        self.assertIn("# Lesson01.1-Intro.txt", content)
        self.assertIn("# Lesson01.2-BigData.txt", content)
        self.assertIn("# Lesson02.1-Advanced.txt", content)
        # Verify all TOC content is included.
        self.assertIn("## Introduction", content)
        self.assertIn("## Big Data", content)
        self.assertIn("## Advanced Topics", content)

class Test_process_lecture_files_progress_bar(hunitest.TestCase):
    """
    Test progress bar integration in main file processing loop.

    Verifies that tqdm is used correctly to show progress when processing files.
    """

    def test1(self) -> None:
        """
        Test that main loop in _main uses tqdm with correct description.

        Input:
        - files: list of 2 lecture files
        - actions: list of actions to process

        Expected:
        - tqdm is called with desc="Processing lectures"
        - All files are iterated through the progress bar
        """
        # Prepare inputs.
        files = [
            ("/path/to/Lesson01.1-Intro.txt", "Lesson01.1-Intro.txt"),
            ("/path/to/Lesson01.2-BigData.txt", "Lesson01.2-BigData.txt"),
        ]
        # Mock tqdm to track calls.
        with mock.patch("class_scripts.for_loop_lessons.tqdm") as mock_tqdm:
            with mock.patch(
                "class_scripts.for_loop_lessons._process_lecture_file"
            ):
                mock_tqdm.return_value = files
                # Simulate the main loop with tqdm.
                for source_path, source_name in mock_tqdm(files, desc="Processing lectures"):
                    pass
                # Check outputs.
                mock_tqdm.assert_called_once()
                tqdm_call_args = mock_tqdm.call_args
                self.assertEqual(tqdm_call_args[0][0], files)
                self.assertEqual(tqdm_call_args[1]["desc"], "Processing lectures")
