"""
Unit tests for slide_check.py.

Import as:

import class_scripts.test.test_slide_check as csttslch
"""

# TODO(gp): Make sure this file follows our unit test conventions

import os
import pprint
from unittest import mock

import helpers.hio as hio
import helpers.hunit_test as hunitest
import helpers.hunit_test_utils as hunteuti

import class_scripts.slide_check as cscslche


def _create_lecture_source(self) -> str:
    """
    Create a scratch `lectures_source/LessonXX-Foo.smd` fixture.

    :return: path to the scratch (course) directory
    """
    scratch_dir = self.get_scratch_space()
    source_dir = os.path.join(scratch_dir, "lectures_source")
    os.makedirs(source_dir, exist_ok=True)
    hio.to_file(os.path.join(source_dir, "Lesson01.1-Intro.smd"), "content")
    return scratch_dir


# #############################################################################
# Test_parse
# #############################################################################


class Test_parse(hunitest.TestCase):
    """
    Test `_parse()` function.
    """

    def test1(self) -> None:
        """
        Test parser accepts `input`, with no extra options.
        """
        # Prepare inputs.
        arg_list = ["msml610/01.1"]
        # Prepare outputs.
        expected_input = "msml610/01.1"
        expected_extra_opts: list = []
        # Run test.
        parser = cscslche._parse()
        args = parser.parse_args(arg_list)
        # Check outputs.
        self.assert_equal(args.input, expected_input)
        self.assert_equal(str(args.extra_opts), str(expected_extra_opts))

    def test2(self) -> None:
        """
        Test parser accepts extra positional options.
        """
        # Prepare inputs.
        arg_list = ["msml610/01.1", "extra_arg1", "extra_arg2"]
        # Prepare outputs.
        expected_extra_opts = ["extra_arg1", "extra_arg2"]
        # Run test.
        parser = cscslche._parse()
        args = parser.parse_args(arg_list)
        # Check outputs.
        self.assert_equal(str(args.extra_opts), str(expected_extra_opts))


# #############################################################################
# Test_main
# #############################################################################


class Test_main(hunitest.TestCase):
    """
    Test `_main()` function.
    """

    def test1(self) -> None:
        """
        Test happy path: builds and runs the expected `process_slides.py`
        command for the found lecture file.
        """
        # Prepare inputs.
        scratch_dir = _create_lecture_source(self)
        lecture_file = os.path.join(
            scratch_dir, "lectures_source", "Lesson01.1-Intro.smd"
        )
        arg_list = [lecture_file]
        # Prepare outputs.
        expected_cmd = (
            f"process_slides.py --in_file {lecture_file} "
            "--action text_check_fix "
            f"--out_file {lecture_file} --use_llm_transform"
        )
        expected_str = pprint.pformat(
            [
                {
                    "function": "hsystem.system",
                    "args": (expected_cmd,),
                    "kwargs": {},
                }
            ]
        )
        # Run test.
        with hunteuti.capture_sys_calls() as sys_calls:
            with mock.patch("sys.argv", ["slide_check.py"] + arg_list):
                cscslche._main(cscslche._parse())
        # Check outputs.
        actual_str = pprint.pformat(sys_calls)
        self.assert_equal(actual_str, expected_str)

    def test2(self) -> None:
        """
        Test `extra_opts` are appended to the built command.
        """
        # Prepare inputs.
        scratch_dir = _create_lecture_source(self)
        lecture_file = os.path.join(
            scratch_dir, "lectures_source", "Lesson01.1-Intro.smd"
        )
        arg_list = [lecture_file, "extra_arg1", "extra_arg2"]
        # Prepare outputs.
        expected_cmd = (
            f"process_slides.py --in_file {lecture_file} "
            "--action text_check_fix "
            f"--out_file {lecture_file} --use_llm_transform "
            "extra_arg1 extra_arg2"
        )
        expected_str = pprint.pformat(
            [
                {
                    "function": "hsystem.system",
                    "args": (expected_cmd,),
                    "kwargs": {},
                }
            ]
        )
        # Run test.
        with hunteuti.capture_sys_calls() as sys_calls:
            with mock.patch("sys.argv", ["slide_check.py"] + arg_list):
                cscslche._main(cscslche._parse())
        # Check outputs.
        actual_str = pprint.pformat(sys_calls)
        self.assert_equal(actual_str, expected_str)
