"""
Tests for for_loop_slides.py.

Import as:

import class_scripts.test.test_for_loop_slides as cstfls
"""

import logging
import os
from typing import List

import helpers.hio as hio
import helpers.hmarkdown_slide_iterator as hmaslite
import helpers.hprint as hprint
import helpers.hunit_test as hunitest

import class_scripts.for_loop_slides as csfolosl

_LOG = logging.getLogger(__name__)


# #############################################################################
# Test_read_prompt_file
# #############################################################################


class Test_read_prompt_file(hunitest.TestCase):
    """
    Tests for the _read_prompt_file function.
    """

    def test1(self) -> None:
        """
        Test reading a rule file with simple content.
        """
        # Prepare inputs.
        rule_content = hprint.dedent(
            """
            ## Use Bold for Slide Sections

            - Every first level bullet point should start with a bold label
            """
        )
        rule_file = os.path.join(self.get_scratch_space(), "test_rule.md")
        hio.to_file(rule_file, rule_content)
        # Run test.
        result = csfolosl._read_prompt_file(rule_file)
        # Check outputs.
        self.assertEqual(result, rule_content)

    def test2(self) -> None:
        """
        Test reading a rule file with empty content.
        """
        # Prepare inputs.
        rule_content = ""
        rule_file = os.path.join(self.get_scratch_space(), "empty_rule.md")
        hio.to_file(rule_file, rule_content)
        # Run test.
        result = csfolosl._read_prompt_file(rule_file)
        # Check outputs.
        self.assertEqual(result, rule_content)


# #############################################################################
# Test_extract_slides
# #############################################################################


class Test_extract_slides(hunitest.TestCase):
    """
    Tests for the _extract_slides function.
    """

    def helper(
        self,
        items: List[hmaslite.SlideItem],
        expected_slide_count: int,
        expected_slide_texts: List[str],
    ) -> None:
        """
        Test helper for `_extract_slides()`.

        :param items: Input list of slide items
        :param expected_slide_count: Expected number of extracted slides
        :param expected_slide_texts: Expected extracted slide texts
        """
        # Run test.
        slide_items, slide_texts = csfolosl._extract_slides(items)
        # Check outputs.
        self.assertEqual(len(slide_items), expected_slide_count)
        self.assertEqual(len(slide_texts), expected_slide_count)
        self.assertEqual(slide_texts, expected_slide_texts)

    def test1(self) -> None:
        """
        Test extracting slides from mixed content (slides and headers).
        """
        # Prepare inputs.
        slide1: hmaslite.SlideItem = {
            "type": "slide",
            "content": ["* First Slide", "- Bullet point 1"],
            "line_number": 1,
        }
        slide2: hmaslite.SlideItem = {
            "type": "slide",
            "content": ["* Second Slide", "- Bullet point 2"],
            "line_number": 5,
        }
        header: hmaslite.SlideItem = {
            "type": "header",
            "content": ["# Section Header"],
            "line_number": 10,
        }
        items: List[hmaslite.SlideItem] = [slide1, header, slide2]
        # Prepare outputs.
        expected_slide_texts = [
            "* First Slide\n- Bullet point 1",
            "* Second Slide\n- Bullet point 2",
        ]
        # Run test.
        self.helper(items, 2, expected_slide_texts)

    def test2(self) -> None:
        """
        Test extracting slides when only slides exist.
        """
        # Prepare inputs.
        slide1: hmaslite.SlideItem = {
            "type": "slide",
            "content": ["* Only Slide"],
            "line_number": 1,
        }
        items: List[hmaslite.SlideItem] = [slide1]
        # Prepare outputs.
        expected_slide_texts = ["* Only Slide"]
        # Run test.
        self.helper(items, 1, expected_slide_texts)

    def test3(self) -> None:
        """
        Test extracting slides from empty items list.
        """
        # Prepare inputs.
        items: List[hmaslite.SlideItem] = []
        # Prepare outputs.
        expected_slide_texts: List[str] = []
        # Run test.
        self.helper(items, 0, expected_slide_texts)


# #############################################################################
# Test_reconstruct_file
# #############################################################################


class Test_reconstruct_file(hunitest.TestCase):
    """
    Tests for the _reconstruct_file function.
    """

    def helper(
        self,
        items: List[hmaslite.SlideItem],
        transformed_slides: List[str],
        expected_output: str,
    ) -> None:
        """
        Test helper for `_reconstruct_file()`.

        :param items: Input list of slide items
        :param transformed_slides: Transformed slide content
        :param expected_output: Expected reconstructed file content
        """
        # Run test.
        result = csfolosl._reconstruct_file(items, transformed_slides)
        # Check outputs.
        self.assertEqual(result, expected_output)

    def test1(self) -> None:
        """
        Test reconstructing file with transformed slides.
        """
        # Prepare inputs.
        original_slide: hmaslite.SlideItem = {
            "type": "slide",
            "content": ["* Original Slide", "- Old content"],
            "line_number": 1,
        }
        header: hmaslite.SlideItem = {
            "type": "header",
            "content": ["# Header"],
            "line_number": 5,
        }
        items: List[hmaslite.SlideItem] = [original_slide, header]
        transformed_slides = ["* Transformed Slide\n- New content"]
        # Prepare outputs.
        expected_output = "* Transformed Slide\n- New content\n# Header"
        # Run test.
        self.helper(items, transformed_slides, expected_output)

    def test2(self) -> None:
        """
        Test reconstructing file with multiple transformed slides.
        """
        # Prepare inputs.
        slide1: hmaslite.SlideItem = {
            "type": "slide",
            "content": ["* Slide 1"],
            "line_number": 1,
        }
        slide2: hmaslite.SlideItem = {
            "type": "slide",
            "content": ["* Slide 2"],
            "line_number": 3,
        }
        items: List[hmaslite.SlideItem] = [slide1, slide2]
        transformed_slides = ["* New Slide 1", "* New Slide 2"]
        # Prepare outputs.
        expected_output = "* New Slide 1\n* New Slide 2"
        # Run test.
        self.helper(items, transformed_slides, expected_output)

    def test3(self) -> None:
        """
        Test reconstructing file preserves non-slide content.
        """
        # Prepare inputs.
        header1: hmaslite.SlideItem = {
            "type": "header",
            "content": ["# First Header"],
            "line_number": 1,
        }
        slide: hmaslite.SlideItem = {
            "type": "slide",
            "content": ["* Slide"],
            "line_number": 3,
        }
        comment: hmaslite.SlideItem = {
            "type": "comment",
            "content": ["// This is a comment"],
            "line_number": 5,
        }
        items: List[hmaslite.SlideItem] = [header1, slide, comment]
        transformed_slides = ["* Transformed"]
        # Prepare outputs.
        expected_output = "# First Header\n* Transformed\n// This is a comment"
        # Run test.
        self.helper(items, transformed_slides, expected_output)
