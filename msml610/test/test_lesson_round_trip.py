"""
Unit tests for round-trip parsing of markdown lesson files.

Tests that lesson files can be read, parsed, reassembled, and match the original.
"""

import glob
import os

import helpers.hdbg as hdbg
import helpers.hio as hio
import helpers.hunit_test as hunitest

# TODO(ai_gp): Use import helpers.hmarkdown_lesson_iterator as XYZ
from helpers.hmarkdown_lesson_iterator import (
    read_lesson_file,
    reassemble_from_items,
)

import logging
_LOG = logging.getLogger(__name__)


class TestLessonRoundTrip(hunitest.TestCase):
    """
    Test round-trip parsing of markdown lesson files.

    Verifies that lesson files can be read, parsed into structured items,
    reassembled back to markdown, and match the original content exactly.
    """

    def helper_test_round_trip(self, lesson_file: str) -> None:
        """
        Test helper for lesson round-trip parsing.

        :param lesson_file: Path to the lesson file to test
        """
        _LOG.info("Processing %s", lesson_file)
        # Read original content.
        original_content = hio.from_file(lesson_file)
        # Remove trailing empty lines before round-trip test.
        original_content = original_content.rstrip() + "\n"
        # Parse the lesson file.
        items = list(read_lesson_file(lesson_file))
        # Reassemble from parsed items.
        reassembled_content = reassemble_from_items(items)
        # Remove trailing empty lines from reassembled content.
        reassembled_content = reassembled_content.rstrip() + "\n"
        # Verify round-trip: reassembled must match original.
        self.assert_equal(
            original_content,
            reassembled_content,
        )

    def test_lesson_files_round_trip(self) -> None:
        """
        Test round-trip parsing of all Lesson*.txt files in msml610/lectures_source/.

        Reads each lesson file, parses it, reassembles it, and verifies the
        reassembled content matches the original byte-for-byte.
        """
        # Find all lesson files.
        lesson_dir = "msml610/lectures_source"
        lesson_pattern = os.path.join(lesson_dir, "Lesson*.txt")
        lesson_files = sorted(glob.glob(lesson_pattern))
        hdbg.dassert_ne(
            len(lesson_files),
            0,
            "Lesson files must be found matching pattern: '%s'",
            lesson_pattern,
        )
        # Test each lesson file.
        for lesson_file in lesson_files:
            self.helper_test_round_trip(lesson_file)
