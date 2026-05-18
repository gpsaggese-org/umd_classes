"""
Unit tests for round-trip parsing of markdown lesson files.

Tests that lesson files can be read, parsed, reassembled, and match the original.
"""

import glob
import logging
import os
from typing import Any, Dict, List

import helpers.hio as hio
import helpers.hunit_test as hunitest
from helpers.hmarkdown_lesson_iterator import (
    read_lesson_file,
    reassemble_from_items,
)

_LOG = logging.getLogger(__name__)


class TestLessonRoundTrip(hunitest.TestCase):
    """
    Test round-trip parsing of markdown lesson files.

    Verifies that lesson files can be read, parsed into structured items,
    reassembled back to markdown, and match the original content exactly.
    """

    def test_lesson_files_round_trip(self) -> None:
        """
        Test round-trip parsing of all Lesson*.txt files in msml610/lectures_source/.

        Reads each lesson file, parses it, reassembles it, and verifies the
        reassembled content matches the original byte-for-byte.
        """
        # Find all lesson files.
        lesson_dir = "msml610/lectures_source"
        if not os.path.exists(lesson_dir):
            self.skipTest(f"Lesson directory '{lesson_dir}' not found")
        lesson_pattern = os.path.join(lesson_dir, "Lesson*.txt")
        lesson_files = sorted(glob.glob(lesson_pattern))
        # TODO(ai_gp): Turn this into a dassert
        if not lesson_files:
            self.skipTest(f"No lesson files found matching '{lesson_pattern}'")
        # Test each lesson file.
        for lesson_file in lesson_files:
            # TODO(ai_gp): Factor out in a helper.
            with self.subTest(lesson_file=lesson_file):
                # Read original content.
                # TODO(ai_gp): Use hio.from_file
                with open(lesson_file, "r") as f:
                    original_content = f.read()
                # Parse the lesson file.
                items = list(read_lesson_file(lesson_file))
                # Reassemble from parsed items.
                reassembled_content = reassemble_from_items(
                    items, original_content=original_content
                )
                # Verify round-trip: reassembled must match original.
                self.assertEqual(
                    reassembled_content,
                    original_content,
                    f"Round-trip failed for {lesson_file}: reassembled content "
                    "does not match original",
                )
