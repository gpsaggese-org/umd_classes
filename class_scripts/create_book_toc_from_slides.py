#!/usr/bin/env python3
r"""
Generate comprehensive table of contents for book from lecture slides.

Reads the book_map.md file which contains chapters and their associated lesson
files, then extracts the table of contents from each lesson file and combines
them into a single output markdown file.

Usage:
> create_book_toc_from_slides.py --output book_toc.md --max_level 2

> create_book_toc_from_slides.py --output book_toc.md --max_level 5
"""

import argparse
import logging
import re
import subprocess
from typing import List, Tuple

from tqdm import tqdm

import helpers.hdbg as hdbg
import helpers.hgit as hgit
import helpers.hparser as hparser
import helpers.hselect_input_output as hseinout

_LOG = logging.getLogger(__name__)


def _extract_chapters_and_lessons(
    book_map_file: str,
) -> List[Tuple[str, str, List[str]]]:
    """
    Extract chapters and their associated lesson files from book_map.md.

    :param book_map_file: Path to the book_map.md file
    :return: List of (chapter_title, chapter_header, lesson_files) tuples
        where each tuple contains the chapter title, markdown header line,
        and list of associated lesson file paths
    """
    hdbg.dassert_file_exists(book_map_file)
    # Read book_map.md file.
    with open(book_map_file, "r") as f:
        lines = f.readlines()
    # Parse chapters and lessons.
    chapters = []
    current_chapter_title = ""
    current_chapter_header = ""
    current_lessons = []
    in_lessons_section = False
    for line in lines:
        line = line.rstrip()
        # Check for chapter header (## N: Title).
        match = re.match(r"^## (\d+): (.+)$", line)
        if match:
            # Save previous chapter.
            if current_chapter_title:
                chapters.append(
                    (current_chapter_title, current_chapter_header, current_lessons)
                )
            current_chapter_title = match.group(2)
            current_chapter_header = line
            current_lessons = []
            in_lessons_section = False
            continue
        # Check for **Lessons** section.
        if line.startswith("**Lessons**"):
            in_lessons_section = True
            continue
        # Check for next section (e.g., **Tutorials**).
        if line.startswith("**") and line != "**Lessons**":
            in_lessons_section = False
            continue
        # Extract lesson files.
        if in_lessons_section and line.strip().startswith("- "):
            lesson_file = line.strip()[2:].strip()
            current_lessons.append(lesson_file)
    # Save last chapter.
    if current_chapter_title:
        chapters.append(
            (current_chapter_title, current_chapter_header, current_lessons)
        )
    return chapters


def _extract_toc_from_lesson(lesson_file: str, *, max_level: int) -> str:
    """
    Extract table of contents from a single lesson file.

    Calls extract_toc_from_txt.py to extract headers up to max_level from
    the lesson file and returns the markdown-formatted output.

    :param lesson_file: Path to the lesson file
    :param max_level: Maximum header level to extract
    :return: Extracted table of contents as markdown string
    """
    hdbg.dassert_file_exists(lesson_file)
    # Call extract_toc_from_txt.py to extract TOC.
    extract_toc_script = hgit.find_file_in_git_tree("extract_toc_from_txt.py")
    cmd_parts = [
        extract_toc_script,
        f"--input={lesson_file}",
        "--output=-",
        f"--max_level={max_level}",
        "--warn_on_malformed",
        "--count_slides",
    ]
    cmd = " ".join(cmd_parts)
    result = subprocess.run(
        cmd,
        shell=True,
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout


def _create_book_toc(
    book_map_file: str,
    output_file: str,
    *,
    max_level: int,
    max_number: int = 0,
) -> None:
    """
    Create combined table of contents for all chapters and lessons.

    Reads book_map.md, extracts chapters and lessons, then extracts the
    table of contents from each lesson file and combines them into a single
    output file with proper markdown structure.

    :param book_map_file: Path to the book_map.md file
    :param output_file: Path to the output file
    :param max_level: Maximum header level to extract
    :param max_number: Maximum number of chapters (h2 headers) to include
        - Default: 0 (include all chapters)
    """
    # Validate input file exists.
    hdbg.dassert_file_exists(book_map_file)
    # Extract chapters and lessons.
    chapters = _extract_chapters_and_lessons(book_map_file)
    _LOG.info("Found '%d' chapters", len(chapters))
    # Validate all lesson files exist before processing.
    for _, _, lessons in chapters:
        for lesson_file in lessons:
            hdbg.dassert_file_exists(lesson_file)
    # Limit chapters if max_number is specified.
    if max_number > 0:
        chapters = chapters[:max_number]
        _LOG.warning("Limited to '%d' chapters", len(chapters))
    # Build output content.
    output_lines = []
    output_lines.append("# Book Table of Contents")
    output_lines.append("")
    # Create flattened list with chapter info for progress tracking.
    lessons_with_chapters = [
        (chapter_idx, chapter_header, lesson_file)
        for chapter_idx, (_, chapter_header, lessons) in enumerate(chapters)
        for lesson_file in lessons
    ]
    # Process lessons with progress bar.
    current_chapter_idx = -1
    for chapter_idx, chapter_header, lesson_file in tqdm(
        lessons_with_chapters, desc="Processing lectures"
    ):
        # Add chapter header when moving to a new chapter.
        if chapter_idx != current_chapter_idx:
            output_lines.append(chapter_header)
            output_lines.append("")
            current_chapter_idx = chapter_idx
        _LOG.info("Extracting TOC from '%s'", lesson_file)
        output_lines.append(f"### {lesson_file}")
        output_lines.append("")
        # Extract TOC from lesson.
        toc_content = _extract_toc_from_lesson(lesson_file, max_level=max_level)
        hdbg.dassert_ne(toc_content, "")
        output_lines.append(toc_content)
    # Write output file.
    output_content = "\n".join(output_lines)
    hseinout.to_file(output_content, output_file)
    _LOG.info("Wrote output to '%s'", output_file)


def _parse() -> argparse.ArgumentParser:
    """
    Create and return the argument parser.

    :return: Configured argument parser
    """
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--input",
        type=str,
        default="book.From_Data_To_Decisions/book_map.md",
        help="Path to the book_map.md file",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="book_toc.md",
        help="Path to the output file",
    )
    parser.add_argument(
        "--max_level",
        type=int,
        default=5,
        help="Maximum header level to extract",
    )
    parser.add_argument(
        "--max_number",
        type=int,
        default=0,
        help="Maximum number of chapters (h2 headers) to include (0 = all)",
    )
    hparser.add_verbosity_arg(parser)
    return parser


def _main(parser: argparse.ArgumentParser) -> None:
    """
    Main entry point.

    :param parser: Argument parser
    """
    args = parser.parse_args()
    hdbg.init_logger(verbosity=args.log_level, use_exec_path=True)
    _create_book_toc(
        book_map_file=args.input,
        output_file=args.output,
        max_level=args.max_level,
        max_number=args.max_number,
    )


if __name__ == "__main__":
    parser = _parse()
    _main(parser)
