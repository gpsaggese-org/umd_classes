"""
Unit tests for count_lecture_pages.py.

Import as:

import class_scripts.test.test_count_lecture_pages as csttclpa
"""

# TODO(gp): Make sure this file follows our unit test conventions

import os
from unittest import mock

import helpers.hunit_test as hunitest

import class_scripts.count_lecture_pages as clcolepa


# #############################################################################
# Test_parse
# #############################################################################


class Test_parse(hunitest.TestCase):
    """
    Test `_parse()` function.
    """

    def test1(self) -> None:
        """
        Test parser accepts the positional `dir` argument.
        """
        # Prepare inputs.
        arg_list = ["msml610"]
        # Prepare outputs.
        expected = "msml610"
        # Run test.
        parser = clcolepa._parse()
        args = parser.parse_args(arg_list)
        # Check outputs.
        self.assert_equal(args.dir, expected)


# #############################################################################
# Test_main
# #############################################################################


class Test_main(hunitest.TestCase):
    """
    Test `_main()` function.
    """

    def test1(self) -> None:
        """
        Test happy path: `get_pdf_page_counts()` is called with the
        `{dir}/lectures` directory and results are logged.
        """
        # Prepare inputs.
        scratch_dir = self.get_scratch_space()
        os.makedirs(os.path.join(scratch_dir, "lectures"), exist_ok=True)
        arg_list = [scratch_dir]
        page_counts = {"Lesson01.pdf": 10, "Lesson02.pdf": 20}
        # Prepare outputs.
        expected_dir = f"{scratch_dir}/lectures"
        expected_log = "Lesson01.pdf\t10\nLesson02.pdf\t20"
        # Run test.
        with mock.patch(
            "class_scripts.common_utils.get_pdf_page_counts",
            return_value=page_counts,
        ) as mock_get_counts:
            with self.assertLogs(
                "class_scripts.count_lecture_pages", level="INFO"
            ) as cm:
                with mock.patch(
                    "sys.argv", ["count_lecture_pages.py"] + arg_list
                ):
                    clcolepa._main(clcolepa._parse())
        # Check outputs.
        mock_get_counts.assert_called_once_with(
            expected_dir, pattern="Lesson*.pdf"
        )
        # Log records are prefixed with the level and logger name, so only
        # the last two records (one per page count) are checked.
        actual_log = "\n".join(
            record.split(":", 2)[-1] for record in cm.output[-2:]
        )
        self.assert_equal(actual_log, expected_log)
