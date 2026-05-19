"""
Tests for for_loop_slides.py.

Import as:

import class_scripts.test.test_for_loop_slides as cstfls
"""

import os
from typing import List

import helpers.hio as hio
import helpers.hmarkdown_slide_iterator as hmsiterite
import helpers.hprint as hprint
import helpers.hunit_test as hunitest

import class_scripts.for_loop_slides as csfls


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
        result = csfls._read_prompt_file(rule_file)
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
        result = csfls._read_prompt_file(rule_file)
        # Check outputs.
        self.assertEqual(result, rule_content)


class Test_extract_slides(hunitest.TestCase):
    """
    Tests for the _extract_slides function.
    """

    def test1(self) -> None:
        """
        Test extracting slides from mixed content (slides and headers).
        """
        # Prepare inputs.
        slide1: hmsiterite.SlideItem = {
            "type": "slide",
            "content": ["* First Slide", "- Bullet point 1"],
            "line_number": 1,
        }
        slide2: hmsiterite.SlideItem = {
            "type": "slide",
            "content": ["* Second Slide", "- Bullet point 2"],
            "line_number": 5,
        }
        header: hmsiterite.SlideItem = {
            "type": "header",
            "content": ["# Section Header"],
            "line_number": 10,
        }
        items: List[hmsiterite.SlideItem] = [slide1, header, slide2]
        # Prepare outputs.
        expected_slide_items = [slide1, slide2]
        expected_slide_texts = [
            "* First Slide\n- Bullet point 1",
            "* Second Slide\n- Bullet point 2",
        ]
        # Run test.
        slide_items, slide_texts = csfls._extract_slides(items)
        # Check outputs.
        self.assertEqual(len(slide_items), len(expected_slide_items))
        self.assertEqual(len(slide_texts), len(expected_slide_texts))
        self.assertEqual(slide_texts, expected_slide_texts)

    def test2(self) -> None:
        """
        Test extracting slides when only slides exist.
        """
        # Prepare inputs.
        slide1: hmsiterite.SlideItem = {
            "type": "slide",
            "content": ["* Only Slide"],
            "line_number": 1,
        }
        items: List[hmsiterite.SlideItem] = [slide1]
        # Prepare outputs.
        expected_slide_count = 1
        expected_text = "* Only Slide"
        # Run test.
        slide_items, slide_texts = csfls._extract_slides(items)
        # Check outputs.
        self.assertEqual(len(slide_items), expected_slide_count)
        self.assertEqual(slide_texts[0], expected_text)

    def test3(self) -> None:
        """
        Test extracting slides from empty items list.
        """
        # Prepare inputs.
        items: List[hmsiterite.SlideItem] = []
        # Run test.
        slide_items, slide_texts = csfls._extract_slides(items)
        # Check outputs.
        self.assertEqual(len(slide_items), 0)
        self.assertEqual(len(slide_texts), 0)


class Test_reconstruct_file(hunitest.TestCase):
    """
    Tests for the _reconstruct_file function.
    """

    def test1(self) -> None:
        """
        Test reconstructing file with transformed slides.
        """
        # Prepare inputs.
        original_slide: hmsiterite.SlideItem = {
            "type": "slide",
            "content": ["* Original Slide", "- Old content"],
            "line_number": 1,
        }
        header: hmsiterite.SlideItem = {
            "type": "header",
            "content": ["# Header"],
            "line_number": 5,
        }
        items: List[hmsiterite.SlideItem] = [original_slide, header]
        transformed_slides = ["* Transformed Slide\n- New content"]
        # Prepare outputs.
        expected_output = (
            "* Transformed Slide\n- New content\n# Header"
        )
        # Run test.
        result = csfls._reconstruct_file(items, transformed_slides)
        # Check outputs.
        self.assertEqual(result, expected_output)

    def test2(self) -> None:
        """
        Test reconstructing file with multiple transformed slides.
        """
        # Prepare inputs.
        slide1: hmsiterite.SlideItem = {
            "type": "slide",
            "content": ["* Slide 1"],
            "line_number": 1,
        }
        slide2: hmsiterite.SlideItem = {
            "type": "slide",
            "content": ["* Slide 2"],
            "line_number": 3,
        }
        items: List[hmsiterite.SlideItem] = [slide1, slide2]
        transformed_slides = ["* New Slide 1", "* New Slide 2"]
        # Prepare outputs.
        expected_output = "* New Slide 1\n* New Slide 2"
        # Run test.
        result = csfls._reconstruct_file(items, transformed_slides)
        # Check outputs.
        self.assertEqual(result, expected_output)

    def test3(self) -> None:
        """
        Test reconstructing file preserves non-slide content.
        """
        # Prepare inputs.
        header1: hmsiterite.SlideItem = {
            "type": "header",
            "content": ["# First Header"],
            "line_number": 1,
        }
        slide: hmsiterite.SlideItem = {
            "type": "slide",
            "content": ["* Slide"],
            "line_number": 3,
        }
        comment: hmsiterite.SlideItem = {
            "type": "comment",
            "content": ["// This is a comment"],
            "line_number": 5,
        }
        items: List[hmsiterite.SlideItem] = [header1, slide, comment]
        transformed_slides = ["* Transformed"]
        # Prepare outputs.
        expected_output = "# First Header\n* Transformed\n// This is a comment"
        # Run test.
        result = csfls._reconstruct_file(items, transformed_slides)
        # Check outputs.
        self.assertEqual(result, expected_output)
