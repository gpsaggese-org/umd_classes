#!/usr/bin/env python

"""
Generate lecture slides PDF.

This script generates a PDF from lecture source files using notes_to_pdf.py.

Usage:
> gen_slides.py data605 01.1
> gen_slides.py msml610 02.3
> gen_slides.py msml610/lectures_source/Lesson10.2-Causal_Discovery.txt

Import as:

import class_scripts.gen_slides as clgeslio
"""

import argparse
import logging
import re
from pathlib import Path

import class_scripts.common_utils as clcomuut
import helpers.hdbg as hdbg
import helpers.hparser as hparser
import helpers.hsystem as hsystem

_LOG = logging.getLogger(__name__)

# #############################################################################


def _extract_lesson_from_file(file_path_str: str) -> tuple[str, str]:
    """
    Extract lesson number and directory from a file path.

    Parses filenames like "Lesson10.2-Causal_Discovery.txt" to extract "10.2".
    Also extracts the course directory (data605 or msml610) from the path.

    :param file_path_str: file path like "msml610/lectures_source/Lesson10.2-Name.txt"
    :return: tuple of (dir, lesson) e.g., ("msml610", "10.2")
    """
    # TODO(ai_gp): use os functions and not Path.
    file_path = Path(file_path_str)
    filename = file_path.name
    # Extract lesson number from filename (e.g., "Lesson10.2-...")
    match = re.match(r"Lesson(\d+(?:\.\d+)?)", filename)
    hdbg.dassert(
        match,
        f"Could not extract lesson number from filename: {filename}",
    )
    # TODO(ai_gp): Use dbg.dassert_is_not(
    assert match is not None
    lesson = match.group(1)
    # Extract directory (should be first part of the path)
    dir_name = file_path.parts[0]
    hdbg.dassert_in(
        dir_name,
        clcomuut.VALID_DIRS,
        f"Directory specified from %s is invalid", file_path_str
    )
    _LOG.debug(
        "Extracted lesson='%s', dir='%s' from path='%s'",
        lesson,
        dir_name,
        file_path_str,
    )
    return dir_name, lesson


def _parse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "dir",
        type=str,
        help="Course directory (e.g., data605, msml610) or file path (e.g.,"
            " msml610/lectures_source/Lesson10.2-Name.txt)",
    )
    parser.add_argument(
        "lesson",
        type=str,
        nargs="?",
        default=None,
        help="Lesson number (e.g., 01.1, 02.3). Optional if dir is a file path.",
    )
    parser.add_argument(
        "extra_opts",
        nargs="*",
        help="Additional options to pass to notes_to_pdf.py",
    )
    hparser.add_verbosity_arg(parser)
    return parser


def _main(parser: argparse.ArgumentParser) -> None:
    args = parser.parse_args()
    hdbg.init_logger(verbosity=args.log_level, use_exec_path=True)
    # Handle two cases:
    # - file path or
    # - dir + lesson, e.g., `msml610/lectures_source/Lesson10.2-Name.txt)"
    if args.lesson is None:
        # First argument is a file path.
        dir_arg, lesson_arg = _extract_lesson_from_file(args.dir)
    else:
        # Dir and lesson are separate arguments.
        dir_arg = args.dir
        lesson_arg = args.lesson
    # Validate arguments.
    clcomuut.validate_dir_lesson_args(dir_arg, lesson_arg)
    # Get source and destination names.
    src_name = clcomuut.get_source_name(dir_arg, lesson_arg)
    dst_name = clcomuut.get_output_name(src_name, ".pdf")
    # Build paths.
    input_file = f"{dir_arg}/lectures_source/{src_name}"
    output_file = f"{dir_arg}/lectures/{dst_name}"
    # Ensure output directory exists.
    clcomuut.ensure_dir_exists(f"{dir_arg}/lectures")
    # Build the command with debug options.
    opts_debug = "--skip_action cleanup_before --skip_action cleanup_after"
    cmd_parts = [
        "notes_to_pdf.py",
        f"--input {input_file}",
        f"--output {output_file}",
        "--type slides",
        "--toc_type navigation",
        "--debug_on_error",
        opts_debug,
    ]
    # Add extra options if provided.
    if args.extra_opts:
        cmd_parts.extend(args.extra_opts)
    cmd = " ".join(cmd_parts)
    _LOG.info("Running command: %s", cmd)
    # Execute the command.
    hsystem.system(cmd)


if __name__ == "__main__":
    _main(_parse())
