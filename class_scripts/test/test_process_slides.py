"""
Unit tests for process_slides.py.

Import as:

import class_scripts.test.test_process_slides as csttprsl
"""

import os
import pprint
from unittest import mock

import helpers.hio as hio
import helpers.hunit_test as hunitest
import helpers.hunit_test_utils as hunteuti

import class_scripts.process_slides as csprsl


# #############################################################################
# Test__extract_slides_from_markdown
# #############################################################################


class Test__extract_slides_from_markdown(hunitest.TestCase):
    """
    Test `_extract_slides_from_markdown()` function.
    """

    def test1(self) -> None:
        """
        Test edge case: text with no `* ` headers yields no slides.
        """
        # Prepare inputs.
        txt = "Just some text.\nAnother line."
        # Run test.
        actual = csprsl._extract_slides_from_markdown(txt)
        # Check outputs.
        expected: list = []
        self.assertEqual(actual, expected)

    def test2(self) -> None:
        """
        Test happy path: a single header captures all following lines.
        """
        # Prepare inputs.
        txt = "* Slide 1\nContent line 1\nContent line 2"
        # Run test.
        actual = csprsl._extract_slides_from_markdown(txt)
        # Check outputs.
        expected = [
            ("Slide 1", "* Slide 1\nContent line 1\nContent line 2")
        ]
        self.assertEqual(actual, expected)

    def test3(self) -> None:
        """
        Test happy path: multiple headers split content at each header.
        """
        # Prepare inputs.
        txt = "* Slide 1\nContent 1\n* Slide 2\nContent 2"
        # Run test.
        actual = csprsl._extract_slides_from_markdown(txt)
        # Check outputs.
        expected = [
            ("Slide 1", "* Slide 1\nContent 1"),
            ("Slide 2", "* Slide 2\nContent 2"),
        ]
        self.assertEqual(actual, expected)

    def test4(self) -> None:
        """
        Test edge case: the last slide's content runs to EOF.
        """
        # Prepare inputs.
        txt = "* Slide 1\nContent 1\n* Slide 2\nContent 2\nMore content"
        # Run test.
        actual = csprsl._extract_slides_from_markdown(txt)
        # Check outputs.
        expected = [
            ("Slide 1", "* Slide 1\nContent 1"),
            ("Slide 2", "* Slide 2\nContent 2\nMore content"),
        ]
        self.assertEqual(actual, expected)


# #############################################################################
# Test__get_system_prompt_from_tag
# #############################################################################


class Test__get_system_prompt_from_tag(hunitest.TestCase):
    """
    Test `_get_system_prompt_from_tag()` function.

    Note: `_get_system_prompt_from_tag()` calls `eval(f"{prompt_tag}()")`,
    but the prompt functions (e.g., `text_check_fix()`) are only reachable
    through `dev_scripts_helpers.llms.llm_prompts` (imported as `dshlllpr`)
    and are never bound as bare names in `process_slides.py`'s namespace.
    This makes every valid tag raise `NameError` in the current code; these
    tests document that behavior as-is.
    """

    def test1(self) -> None:
        """
        Test that a real tag (`text_check_fix`) raises `NameError`.
        """
        # Run test.
        with self.assertRaises(NameError) as cm:
            csprsl._get_system_prompt_from_tag("text_check_fix")
        # Check outputs.
        self.assertIn("text_check_fix", str(cm.exception))

    def test2(self) -> None:
        """
        Test that a real tag (`slide_improve`) raises `NameError`.
        """
        # Run test.
        with self.assertRaises(NameError) as cm:
            csprsl._get_system_prompt_from_tag("slide_improve")
        # Check outputs.
        self.assertIn("slide_improve", str(cm.exception))

    def test3(self) -> None:
        """
        Test that a real tag (`slide_reduce`) raises `NameError`.
        """
        # Run test.
        with self.assertRaises(NameError) as cm:
            csprsl._get_system_prompt_from_tag("slide_reduce")
        # Check outputs.
        self.assertIn("slide_reduce", str(cm.exception))

    def test4(self) -> None:
        """
        Test edge case: an unknown tag raises `AssertionError` before the
        `eval()` call is reached.
        """
        # Prepare inputs.
        prompt_tag = "not_a_real_tag"
        # Run test.
        with self.assertRaises(AssertionError) as cm:
            csprsl._get_system_prompt_from_tag(prompt_tag)
        # Check outputs.
        self.assertIn(prompt_tag, str(cm.exception))


# #############################################################################
# Test__process_slide_with_llm_transform
# #############################################################################


class Test__process_slide_with_llm_transform(hunitest.TestCase):
    """
    Test `_process_slide_with_llm_transform()` function.
    """

    def test1(self) -> None:
        """
        Test happy path: builds the `llm_transform.py` command and reads
        back the (pre-seeded) output file.
        """
        # Prepare inputs.
        slide_content = "* Slide 1\nContent"
        action = "text_check_fix"
        tmp_in_path = "tmp.process_slide_with_llm_transform.input.txt"
        tmp_out_path = "tmp.process_slide_with_llm_transform.output.txt"
        expected_output = "Processed content"
        hio.to_file(tmp_out_path, expected_output)
        llm_transform_script = "/repo/dev_scripts_helpers/llms/llm_transform.py"
        # Run test.
        with mock.patch(
            "helpers.hgit.find_file_in_git_tree",
            return_value=llm_transform_script,
        ):
            with hunteuti.capture_system_calls() as invocations:
                actual = csprsl._process_slide_with_llm_transform(
                    slide_content, action
                )
        # Check outputs.
        self.assertEqual(actual, expected_output)
        self.assertEqual(hio.from_file(tmp_in_path), slide_content)
        actual_str = pprint.pformat(invocations)
        expected_cmd = (
            f"{llm_transform_script} -i {tmp_in_path} -o {tmp_out_path} "
            f"-p {action}"
        )
        expected_str = pprint.pformat(
            [
                {
                    "function": "hsystem.system",
                    "args": (expected_cmd,),
                    "kwargs": {"suppress_output": False},
                }
            ]
        )
        self.assert_equal(actual_str, expected_str)


# #############################################################################
# Test__process_single_slide
# #############################################################################


class Test__process_single_slide(hunitest.TestCase):
    """
    Test `_process_single_slide()` function.

    Uses `use_llm_transform=True` to route through
    `_process_slide_with_llm_transform()` and avoid the `NameError` bug in
    `_get_system_prompt_from_tag()` (see `Test__get_system_prompt_from_tag`).
    """

    def _helper(self, processed_output: str, expected: str) -> None:
        """
        Test helper: pre-seed the `llm_transform` output file, run
        `_process_single_slide()`, and check the formatted result.

        :param processed_output: content to pre-seed as the `llm_transform`
            output
        :param expected: expected formatted result entry
        """
        # Prepare inputs.
        tmp_out_path = "tmp.process_slide_with_llm_transform.output.txt"
        hio.to_file(tmp_out_path, processed_output)
        # Run test.
        with mock.patch(
            "helpers.hgit.find_file_in_git_tree",
            return_value="/repo/dev_scripts_helpers/llms/llm_transform.py",
        ):
            with hunteuti.capture_system_calls():
                actual = csprsl._process_single_slide(
                    "Slide 1",
                    "* Slide 1\nContent",
                    "text_check_fix",
                    True,
                    False,
                )
        # Check outputs.
        self.assertEqual(actual, expected)

    def test1(self) -> None:
        """
        Test happy path: result already starts with `"* {slide_title}"`.
        """
        # Prepare inputs/outputs.
        processed_output = "* Slide 1\n\nAlready prefixed content"
        expected = processed_output
        # Run test.
        self._helper(processed_output, expected)

    def test2(self) -> None:
        """
        Test edge case: result missing the `"* {slide_title}"` prefix gets
        one prepended.
        """
        # Prepare inputs/outputs.
        processed_output = "Content without prefix"
        expected = "* Slide 1\n\nContent without prefix"
        # Run test.
        self._helper(processed_output, expected)


# #############################################################################
# Test__process_slides
# #############################################################################


class Test__process_slides(hunitest.TestCase):
    """
    Test `_process_slides()` function.
    """

    def test1(self) -> None:
        """
        Test happy path: processes every slide.
        """
        # Prepare inputs.
        slides = [
            ("Slide 1", "* Slide 1\nContent 1"),
            ("Slide 2", "* Slide 2\nContent 2"),
            ("Slide 3", "* Slide 3\nContent 3"),
        ]
        tmp_out_path = "tmp.process_slide_with_llm_transform.output.txt"
        hio.to_file(tmp_out_path, "Processed")
        # Run test.
        with mock.patch(
            "helpers.hgit.find_file_in_git_tree",
            return_value="/repo/dev_scripts_helpers/llms/llm_transform.py",
        ):
            with hunteuti.capture_system_calls():
                actual = csprsl._process_slides(
                    slides, "text_check_fix", use_llm_transform=True
                )
        # Check outputs.
        expected = [
            "* Slide 1\n\nProcessed",
            "* Slide 2\n\nProcessed",
            "* Slide 3\n\nProcessed",
        ]
        self.assertEqual(actual, expected)

    def test2(self) -> None:
        """
        Test `limit_range` restricts which slides are processed.
        """
        # Prepare inputs.
        slides = [
            ("Slide 1", "* Slide 1\nContent 1"),
            ("Slide 2", "* Slide 2\nContent 2"),
            ("Slide 3", "* Slide 3\nContent 3"),
        ]
        tmp_out_path = "tmp.process_slide_with_llm_transform.output.txt"
        hio.to_file(tmp_out_path, "Processed")
        # Run test.
        with mock.patch(
            "helpers.hgit.find_file_in_git_tree",
            return_value="/repo/dev_scripts_helpers/llms/llm_transform.py",
        ):
            with hunteuti.capture_system_calls():
                actual = csprsl._process_slides(
                    slides,
                    "text_check_fix",
                    limit_range=(0, 1),
                    use_llm_transform=True,
                )
        # Check outputs.
        expected = [
            "* Slide 1\n\nProcessed",
            "* Slide 2\n\nProcessed",
        ]
        self.assertEqual(actual, expected)


# #############################################################################
# Test_parse
# #############################################################################


class Test_parse(hunitest.TestCase):
    """
    Test `_parse()` function.
    """

    def _assert_parse_args(self, arg_list: list, expected_values: dict) -> None:
        """
        Test helper for `_parse()`.

        :param arg_list: list of arguments to parse
        :param expected_values: dict of expected argument values
        """
        parser = csprsl._parse()
        args = parser.parse_args(arg_list)
        for key, value in expected_values.items():
            self.assertEqual(getattr(args, key), value)

    def test1(self) -> None:
        """
        Test happy path: required arguments parse correctly.
        """
        # Prepare inputs.
        arg_list = [
            "--in_file",
            "in.md",
            "--action",
            "text_check_fix",
            "--out_file",
            "out.md",
        ]
        # Prepare outputs.
        expected_values = {
            "in_file": "in.md",
            "action": "text_check_fix",
            "out_file": "out.md",
            "use_llm_transform": False,
            "no_abort_on_error": False,
        }
        # Run test.
        self._assert_parse_args(arg_list, expected_values)

    def test2(self) -> None:
        """
        Test that flag options and `--limit` parse correctly.
        """
        # Prepare inputs.
        arg_list = [
            "--in_file",
            "in.md",
            "--action",
            "slide_improve",
            "--out_file",
            "out.md",
            "--use_llm_transform",
            "--no_abort_on_error",
            "--limit",
            "1:2",
        ]
        # Prepare outputs.
        expected_values = {
            "use_llm_transform": True,
            "no_abort_on_error": True,
            "limit": "1:2",
        }
        # Run test.
        self._assert_parse_args(arg_list, expected_values)


# #############################################################################
# Test_main
# #############################################################################


class Test_main(hunitest.TestCase):
    """
    Test `_main()` function.
    """

    def test1(self) -> None:
        """
        Test happy path: reads slides from `in_file`, processes them, and
        writes formatted results to `out_file`.
        """
        # Prepare inputs.
        scratch_dir = self.get_scratch_space()
        in_file = os.path.join(scratch_dir, "in.md")
        out_file = os.path.join(scratch_dir, "out.md")
        hio.to_file(in_file, "* Slide A\nLine A1\n* Slide B\nLine B1")
        tmp_out_path = "tmp.process_slide_with_llm_transform.output.txt"
        hio.to_file(tmp_out_path, "Processed")
        arg_list = [
            "process_slides.py",
            "--in_file",
            in_file,
            "--action",
            "text_check_fix",
            "--out_file",
            out_file,
            "--use_llm_transform",
        ]
        # Run test.
        with mock.patch(
            "helpers.hgit.find_file_in_git_tree",
            return_value="/repo/dev_scripts_helpers/llms/llm_transform.py",
        ):
            with hunteuti.capture_system_calls():
                with mock.patch("sys.argv", arg_list):
                    csprsl._main(csprsl._parse())
        # Check outputs.
        actual = hio.from_file(out_file)
        expected = "* Slide A\n\nProcessed\n\n* Slide B\n\nProcessed"
        self.assertEqual(actual, expected)
