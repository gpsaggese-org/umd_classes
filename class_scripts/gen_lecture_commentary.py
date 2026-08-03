#!/usr/bin/env python

"""
Generate a PDF to comment the slides from lecture source

The output looks like
https://github.com/gpsaggese/gpsaggese.github.io/blob/master/data605/lectures_commentary

This script performs multiple steps:
1. Generate PDF using notes_to_pdf.py
2. Generate book chapter using generate_book_chapter.py
3. Convert to PDF using pandoc
4. Open the PDF in Skim

Usage:
> gen_lecture_commentary.py data605 01.1
> gen_lecture_commentary.py msml610 02.3

Import as:

import class_scripts.gen_lecture_commentary as clgelcom
"""

import argparse
import logging
from pathlib import Path

import class_scripts.common_utils as clcomuut
import helpers.hdbg as hdbg
import helpers.hparser as hparser
import helpers.hsystem as hsystem

_LOG = logging.getLogger(__name__)

# #############################################################################


def _parse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "dir",
        type=str,
        help="Course directory (e.g., data605, msml610)",
    )
    parser.add_argument(
        "lesson",
        type=str,
        help="Lesson number (e.g., 01.1, 02.3)",
    )
    hparser.add_verbosity_arg(parser)
    return parser


def _main(parser: argparse.ArgumentParser) -> None:
    args = parser.parse_args()
    hdbg.init_logger(verbosity=args.log_level, use_exec_path=True)
    # Validate arguments.
    clcomuut.validate_dir_lesson_args(args.dir, args.lesson)
    # Get source name.
    src_name = clcomuut.get_source_name(args.dir, args.lesson)
    input_file = f"{args.dir}/lectures_source/{src_name}"
    # Step 1: Generate the PDF.
    _LOG.info("Step 1: Generating PDF from lecture source")
    dst_name = clcomuut.get_output_name(src_name, ".pdf")
    tmp_pdf = f"tmp.{dst_name}"
    cmd = (
        "notes_to_pdf.py "
        f"--input {input_file} "
        f"--output {tmp_pdf} "
        "--type slides --toc_type remove_headers"
    )
    hsystem.system(cmd, print_command=True)
    # Step 2: Generate book chapter.
    _LOG.info("Step 2: Generating book chapter")
    out_dir = f"{args.dir}/lecture_commentary"
    clcomuut.ensure_dir_exists(out_dir)
    cmd = (
        "generate_book_chapter.py "
        f"--input_file {input_file} "
        f"--input_pdf_file {tmp_pdf} "
        f"--output_dir {out_dir}"
    )
    hsystem.system(cmd, print_command=True)
    # Step 3: Convert to PDF using pandoc.
    _LOG.info("Step 3: Converting to PDF using pandoc")
    basename = Path(src_name).stem
    book_chapter_md = f"{out_dir}/{basename}.book_chapter.md"
    pdf_file_name = f"{out_dir}/{basename}.book_chapter.pdf"
    cmd = (
        f"pandoc {book_chapter_md} -o {pdf_file_name} "
        f"--pdf-engine=xelatex "
        f"-V geometry:margin=1in "
        f"-V fontsize=11pt "
        f"--highlight-style=tango "
        f"--include-in-header={Path(__file__).parent}/header-style.tex"
    )
    hsystem.system(cmd, print_command=True)
    # Step 4: Open the PDF in Skim.
    _LOG.info("Step 4: Opening PDF in Skim")
    cmd = f"open -a /Applications/Skim.app {pdf_file_name}"
    hsystem.system(cmd, print_command=True)
    _LOG.info("Book chapter generated: %s", pdf_file_name)


if __name__ == "__main__":
    _main(_parse())
