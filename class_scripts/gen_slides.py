#!/usr/bin/env python

"""
Generate lecture slides PDF.

This script generates a PDF from lecture source files using notes_to_pdf.py.

Usage:
> gen_slides.py msml610/08.1
> gen_slides.py data605/01.1
> gen_slides.py msml610/08.1 --skip_action cleanup_before
> gen_slides.py msml610/lectures_source/Lesson10.2-Causal_Discovery.txt
"""

import argparse
import logging
import os
import re
import shlex

import class_scripts.common_utils as csccouti
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

    :param file_path_str: File path like "msml610/lectures_source/Lesson10.2-Name.txt"
    :return: Tuple of (dir, lesson) e.g., ("msml610", "10.2")
    """
    filename = os.path.basename(file_path_str)
    match = re.match(r"Lesson(\d+(?:\.\d+)?)", filename)
    hdbg.dassert_is_not(
        match,
        None,
        "Could not extract lesson number from filename: %s",
        filename,
    )
    lesson = match.group(1)  # type: ignore[union-attr]
    dir_name = file_path_str.split(os.sep)[0]
    hdbg.dassert_in(
        dir_name,
        csccouti.VALID_DIRS,
        "Directory extracted from %s is invalid",
        file_path_str,
    )
    _LOG.debug(
        "Extracted lesson='%s', dir='%s' from path='%s'",
        lesson,
        dir_name,
        file_path_str,
    )
    return dir_name, lesson


def _parse_first_arg(arg: str) -> tuple[str, str]:
    """
    Parse the first argument to extract directory and lesson.

    Handles:
    - "data605/08.1" or "msml610/08.1" -> ("data605", "08.1")
    - "data605/lectures_source/Lesson10.2-Name.txt" -> extracted via file parsing

    :param arg: first argument from command line
    :return: tuple of (directory, lesson)
    """
    if "lectures_source" in arg or arg.endswith(".txt"):
        return _extract_lesson_from_file(arg)
    hdbg.dassert(
        "/" in arg,
        f"Invalid input '{arg}'. Use 'data605/08.1' or "
        "'data605/lectures_source/Lesson08.1-Name.txt'",
    )
    parts = arg.split("/")
    hdbg.dassert_eq(
        len(parts),
        2,
        f"Expected dir/lesson format, got '{arg}'. Use 'data605/08.1'",
    )
    dir_input, lesson = parts
    hdbg.dassert_in(
        dir_input,
        csccouti.VALID_DIRS,
        f"Invalid directory '{dir_input}'. Must be one of: {csccouti.VALID_DIRS}",
    )
    return dir_input, lesson


def _parse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "input",
        type=str,
        help="Lecture specification: 'data605/08.1', 'msml610/08.1', "
        "or file path 'msml610/lectures_source/Lesson10.2-Name.txt'",
    )
    parser.add_argument(
        "extra_opts",
        nargs=argparse.REMAINDER,
        help="Additional options to pass to notes_to_pdf.py",
    )
    hparser.add_verbosity_arg(parser)
    return parser


def _main(parser: argparse.ArgumentParser) -> None:
    args = parser.parse_args()
    hdbg.init_logger(verbosity=args.log_level, use_exec_path=True)
    dir_arg, lesson_arg = _parse_first_arg(args.input)
    csccouti.validate_dir_lesson_args(dir_arg, lesson_arg)
    # Get source and destination names.
    src_name = csccouti.get_source_name(dir_arg, lesson_arg)
    dst_name = csccouti.get_output_name(src_name, ".pdf")
    # Build paths.
    input_file = f"{dir_arg}/lectures_source/{src_name}"
    output_file = f"{dir_arg}/lectures/{dst_name}"
    # Ensure output directory exists.
    csccouti.ensure_dir_exists(f"{dir_arg}/lectures")
    # Prepare command arguments.
    script_name = "notes_to_pdf.py"
    input_flag = "--input"
    output_flag = "--output"
    type_flag = "--type"
    output_type = "slides"
    toc_type_flag = "--toc_type"
    toc_type = "navigation"
    debug_flag = "--debug_on_error"
    skip_action_flag = "--skip_action"
    cleanup_before = "cleanup_before"
    cleanup_after = "cleanup_after"
    # Build the command with debug options.
    cmd_parts = [
        script_name,
        input_flag,
        input_file,
        output_flag,
        output_file,
        type_flag,
        output_type,
        toc_type_flag,
        toc_type,
        debug_flag,
        skip_action_flag,
        cleanup_before,
        skip_action_flag,
        cleanup_after,
    ]
    # Add extra options if provided.
    if args.extra_opts:
        cmd_parts.extend(args.extra_opts)
    # Prepare command by quoting all arguments to preserve special characters.
    quoted_parts = [shlex.quote(part) for part in cmd_parts]
    cmd = " ".join(quoted_parts)
    _LOG.info("Running command: %s", cmd)
    # Execute the command.
    hsystem.system(cmd)


if __name__ == "__main__":
    _main(_parse())
