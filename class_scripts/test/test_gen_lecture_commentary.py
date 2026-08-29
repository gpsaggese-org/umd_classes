# TODO(ai_gp): Add logging import and _LOG definition to follow the template structure (testing.rules.md:## Unit Test Code Structure)
"""
Unit tests for gen_lecture_commentary.py.

Import as:

import class_scripts.test.test_gen_lecture_commentary as csttgelcom
"""

from unittest import mock

import helpers.hunit_test as hunitest

import class_scripts.gen_lecture_commentary as clgelcom


# #############################################################################
# Test_get_image_extension
# #############################################################################


class Test_get_image_extension(hunitest.TestCase):
    # TODO(ai_gp): Add module path to docstring (e.g., `class_scripts.gen_lecture_commentary.get_image_extension()`) (testing.rules.md:## Test Class Documentation)
    """
    Test `get_image_extension()` function.
    """

    def test1(self) -> None:
        """
        Test happy path: "png" image type maps to the "png" extension.
        """
        # Prepare inputs.
        image_type = "png"
        # Prepare outputs.
        expected = "png"
        # Run test.
        actual = clgelcom.get_image_extension(image_type)
        # Check outputs.
        # TODO(ai_gp): Use self.assert_equal() for string comparisons instead of self.assertEqual() (testing.rules.md:## Assertion Patterns)
        self.assertEqual(actual, expected)

    # TODO(ai_gp): Create helper method for test1 and test2 since they test the same function with different inputs (testing.rules.md:## Use Helper Methods When You Have Repetitive Tests)
    def test2(self) -> None:
        """
        Test happy path: "jpg" image type maps to the "jpg" extension.
        """
        # Prepare inputs.
        image_type = "jpg"
        # Prepare outputs.
        expected = "jpg"
        # Run test.
        actual = clgelcom.get_image_extension(image_type)
        # Check outputs.
        # TODO(ai_gp): Use self.assert_equal() for string comparisons instead of self.assertEqual() (testing.rules.md:## Assertion Patterns)
        self.assertEqual(actual, expected)

    # TODO(ai_gp): Remove test for error condition (invalid input and assertion); follow guidance to not test heavily error conditions (testing.rules.md:## What not to Test)
    def test3(self) -> None:
        """
        Test edge case: an unsupported image type raises AssertionError.
        """
        # Prepare inputs.
        image_type = "bmp"
        # Prepare outputs.
        expected = "Invalid image type specified"
        # Run test.
        with self.assertRaises(AssertionError) as cm:
            clgelcom.get_image_extension(image_type)
        # Check outputs.
        # TODO(ai_gp): Compare whole exception message output instead of piecewise with assertIn(); use self.assert_equal() (testing.rules.md:## Compare Whole Output with `assert_equal`, Not Piecewise)
        self.assertIn(expected, str(cm.exception))


# #############################################################################
# Test__generate_slide_commentary
# #############################################################################

# TODO(ai_gp): Avoid testing private functions (_generate_slide_commentary); test the public interface instead (testing.rules.md:## Test From the Outside-In)

class Test__generate_slide_commentary(hunitest.TestCase):
    # TODO(ai_gp): Add module path to docstring (e.g., `class_scripts.gen_lecture_commentary._generate_slide_commentary()`) (testing.rules.md:## Test Class Documentation)
    """
    Test `_generate_slide_commentary()` function.
    """

    def test1(self) -> None:
        """
        Test happy path: the slide content (with no images) is sent to
        `common_utils.call_llm()` and its response is returned unchanged.
        """
        # Prepare inputs.
        # TODO(ai_gp): Use triple-quote assignment with hprint.dedent instead of escaped \n for multi-line strings (testing.rules.md:### Use Triple-Quote Assignment with `hprint.dedent` for Multi-line Strings)
        slide_content = "* Slide 1\nSome text without images."
        system_prompt = "You are a helpful assistant."
        model = "gpt-4"
        llm_backend = "hllm"
        # Prepare outputs.
        expected = "Commentary about slide 1."
        # Run test.
        with mock.patch(
            "class_scripts.common_utils.call_llm", return_value=expected
        ) as mock_call_llm:
            actual = clgelcom._generate_slide_commentary(
                slide_content, system_prompt, model, llm_backend
            )
        # Check outputs.
        # TODO(ai_gp): Use self.assert_equal() for string comparisons instead of self.assertEqual() (testing.rules.md:## Assertion Patterns)
        self.assertEqual(actual, expected)
        mock_call_llm.assert_called_once_with(
            slide_content,
            system_prompt,
            model,
            llm_backend,
            images_as_base64=(),
        )

    # TODO(ai_gp): Remove test for error condition (invalid input and assertion); follow guidance to not test heavily error conditions (testing.rules.md:## What not to Test)
    def test2(self) -> None:
        """
        Test edge case: an unsupported `llm_backend` raises AssertionError.
        """
        # Prepare inputs.
        # TODO(ai_gp): Use triple-quote assignment with hprint.dedent instead of escaped \n for multi-line strings (testing.rules.md:### Use Triple-Quote Assignment with `hprint.dedent` for Multi-line Strings)
        slide_content = "* Slide 1\nSome text."
        system_prompt = "You are a helpful assistant."
        model = ""
        llm_backend = "invalid_backend"
        # Prepare outputs.
        expected = "'invalid_backend'"
        # Run test.
        with self.assertRaises(AssertionError) as cm:
            clgelcom._generate_slide_commentary(
                slide_content, system_prompt, model, llm_backend
            )
        # Check outputs.
        # TODO(ai_gp): Compare whole exception message output instead of piecewise with assertIn(); use self.assert_equal() (testing.rules.md:## Compare Whole Output with `assert_equal`, Not Piecewise)
        self.assertIn(expected, str(cm.exception))
