#!/usr/bin/env python

"""
Generate lecture slides PDF.

This script generates a PDF from lecture source files using notes_to_pdf.py.

# Usage Example

- Generate the slides PDF for msml610 lesson 08.1:
> gen_slides.py msml610/08.1

- Generate the slides PDF for data605 lesson 01.1:
> gen_slides.py data605/01.1

- Generate the slides PDF for msml610 lesson 08.1, skipping the
  cleanup_before action:
> gen_slides.py msml610/08.1 --skip_action cleanup_before

- Generate the slides PDF by specifying the lecture source file path
  directly:
> gen_slides.py msml610/lectures_source/Lesson10.2-Causal_Discovery.txt
"""

import argparse
import logging
import os
import re
import shlex
from typing import Tuple

import class_scripts.common_utils as csccouti
import helpers.hdbg as hdbg
import helpers.hparser as hparser
import helpers.hprint as hprint
import helpers.hsystem as hsystem

_LOG = logging.getLogger(__name__)

# #############################################################################


def _extract_lesson_from_file(file_path_str: str) -> Tuple[str, str]:
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
    hdbg.dassert_dir_exists(
        dir_name,
    )
    _LOG.debug(
        "Extracted lesson='%s', dir='%s' from path='%s'",
        lesson,
        dir_name,
        file_path_str,
    )
    return dir_name, lesson


def _parse_first_arg(arg: str) -> Tuple[str, str]:
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
    hdbg.dassert_dir_exists(dir_input)
    return dir_input, lesson


def _parse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=hparser.CustomHelpFormatter,
    )
    parser.add_argument(
        "input",
        type=str,
        help="Lecture specification: 'data605/08.1', 'msml610/08.1', "
        "or file path 'msml610/lectures_source/Lesson10.2-Name.txt'",
    )
    parser.add_argument(
        "--daemon",
        action="store_true",
        help="Watch input file for changes and regenerate PDF on change",
    )
    parser.add_argument(
        "--slides_engine",
        action="store",
        default=None,
        choices=["beamer", "typst"],
        help="Engine used to render slides: 'beamer' (default) or 'typst'",
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
    # Filter --daemon from extra_opts if REMAINDER swallowed it.
    if args.extra_opts:
        filtered = []
        for opt in args.extra_opts:
            if opt == "--daemon":
                args.daemon = True
            else:
                filtered.append(opt)
        args.extra_opts = filtered
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
    # Build the command with debug options.
    cmd_parts = [
        "notes_to_pdf.py",
        f"--input={input_file}",
        f"--output={output_file}",
        "--type=slides",
        "--toc_type=navigation",
        "--debug_on_error",
        "--skip_action=cleanup_before",
        "--skip_action=cleanup_after",
    ]
    # Add slides engine if specified.
    if args.slides_engine:
        cmd_parts.append(f"--slides_engine={args.slides_engine}")
    # Add extra options if provided.
    if args.extra_opts:
        cmd_parts.extend(args.extra_opts)
    if not args.daemon:
        # `notes_to_pdf.py`'s default actions don't include "open_pdf", so
        # add it explicitly to open the PDF after a one-shot generation.
        cmd_parts.append("--action=open_pdf")
    # Prepare command by quoting all arguments to preserve special characters.
    quoted_parts = [shlex.quote(part) for part in cmd_parts]
    cmd = " ".join(quoted_parts)
    if args.daemon:
        # `notes_to_pdf.py`'s default actions don't include "open_pdf", so
        # build once upfront and open the PDF; then hand off to its own
        # `--daemon` watch loop, which regenerates on change without
        # reopening the viewer (it skips "open_pdf" on watch runs since the
        # viewer auto-reloads).
        initial_cmd = cmd + " --action=open_pdf"
        _LOG.info("%s", hprint.color_highlight(f"> {initial_cmd}", "green"))
        hsystem.system(initial_cmd, suppress_output=False)
        cmd += " --daemon"
    # Execute the command.
    _LOG.info("%s", hprint.color_highlight(f"> {cmd}", "green"))
    hsystem.system(cmd, suppress_output=False)


if __name__ == "__main__":
    _main(_parse())
