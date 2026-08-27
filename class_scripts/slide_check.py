#!/usr/bin/env python

"""
Check and fix text in lecture slides.

This script checks and fixes text in lecture slides using process_slides.py
with the text_check_fix action.

# Usage Example

- Check and fix text in DATA605 lesson 01.1 slides:
> slide_check.py data605/01.1

- Check and fix text in MSML610 lesson 02.3 slides:
> slide_check.py msml610/02.3

Import as:

import class_scripts.slide_check as clslchec
"""

import argparse
import logging

import class_scripts.common_utils as csccouti
import helpers.hdbg as hdbg
import helpers.hparser as hparser
import helpers.hprint as hprint
import helpers.hsystem as hsystem

_LOG = logging.getLogger(__name__)

# #############################################################################


def _parse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=hparser.CustomHelpFormatter,
    )
    parser.add_argument(
        "input",
        type=str,
        help="Lecture specification: 'data605/08.1', 'msml610/08.1', "
        "or file path 'msml610/lectures_source/Lesson10.2-Name.smd'",
    )
    parser.add_argument(
        "--dry_run",
        action="store_true",
        help="Print the command that would be executed without running it",
    )
    parser.add_argument(
        "extra_opts",
        nargs="*",
        help="Additional options to pass to process_slides.py",
    )
    hparser.add_verbosity_arg(parser)
    return parser


def _main(parser: argparse.ArgumentParser) -> None:
    args = parser.parse_args()
    hdbg.init_logger(verbosity=args.log_level, use_exec_path=True)
    # Parse and validate arguments.
    dir_arg, lesson_arg = csccouti.parse_lesson_spec(args.input)
    csccouti.validate_dir_lesson_args(dir_arg, lesson_arg)
    # Find the lecture file.
    lecture_file = csccouti.find_lecture_file(dir_arg, lesson_arg)
    src_name = str(lecture_file)
    dst_name = src_name
    # Build the command.
    cmd_parts = [
        "process_slides.py",
        f"--in_file {src_name}",
        "--action text_check_fix",
        f"--out_file {dst_name}",
        "--use_llm_transform",
    ]
    if args.dry_run:
        cmd_parts.append("--dry_run")
    # Add extra options if provided.
    if args.extra_opts:
        cmd_parts.extend(args.extra_opts)
    cmd = " ".join(cmd_parts)
    _LOG.info("%s", hprint.color_highlight(f"> {cmd}", "green"))
    # Execute the command.
    hsystem.system(cmd)


if __name__ == "__main__":
    _main(_parse())
