#!/usr/bin/env python

"""
Generate a PDF with the lecture commentaries from slides lecture source.

This script performs multiple steps:
1. Generate PDF using notes_to_pdf.py
2. Generate book chapter using generate_book_chapter.py
3. Convert to PDF using pandoc
4. Open the PDF in Skim

Usage:
> gen_lecture_commentary.py data605 01.1
> gen_lecture_commentary.py msml610 02.3

The output looks like:
https://github.com/gpsaggese/gpsaggese.github.io/blob/master/data605/lectures_commentary
or 

```
> ls -1 data605/lectures_commentary/Lesson01.1-Intro.*
data605/lectures_commentary/Lesson01.1-Intro.book_chapter.pdf
data605/lectures_commentary/Lesson01.1-Intro.book_chapter.txt

data605/lectures_commentary/Lesson01.1-Intro.png:
slides001.png
slides002.png
...
```

Import as:

import class_scripts.gen_lecture_commentary as clgelcom
"""

import argparse
import logging
import os

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
    parser.add_argument(
        "--dry_run",
        action="store_true",
        help="Only print the commands that would be executed without running them",
    )
    parser.add_argument(
        "--no_incremental",
        action="store_true",
        help=(
            "Force regeneration of intermediate files even if they already "
            "exist (by default, steps are skipped if their output already "
            "exists)"
        ),
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
    # Precompute the paths of all intermediate/output files, so that we can
    # skip steps whose output already exists (unless --no_incremental).
    dst_name = clcomuut.get_output_name(src_name, ".pdf")
    tmp_pdf = f"tmp.{dst_name}"
    out_dir = f"{args.dir}/lecture_commentary"
    basename = os.path.splitext(src_name)[0]
    book_chapter_md = f"{out_dir}/{basename}.book_chapter.md"
    pdf_file_name = f"{out_dir}/{basename}.book_chapter.pdf"
    do_incremental = not args.no_incremental
    # Step 1: Generate the PDF.
    if do_incremental and os.path.exists(tmp_pdf):
        _LOG.warning("Step 1: Skipping, '%s' already exists", tmp_pdf)
    else:
        _LOG.info("Step 1: Generating PDF from lecture source")
        cmd = (
            "notes_to_pdf.py "
            f"--input {input_file} "
            f"--output {tmp_pdf} "
            "--type slides --toc_type remove_headers"
        )
        hsystem.system(cmd, print_command=True, dry_run=args.dry_run)
    # Step 2: Generate book chapter.
    clcomuut.ensure_dir_exists(out_dir)
    if do_incremental and os.path.exists(book_chapter_md):
        _LOG.warning("Step 2: Skipping, '%s' already exists", book_chapter_md)
    else:
        _LOG.info("Step 2: Generating book chapter")
        cmd = (
            "generate_book_chapter.py "
            f"--input_file {input_file} "
            f"--input_pdf_file {tmp_pdf} "
            f"--output_dir {out_dir} "
            f"--output_file {book_chapter_md}"
        )
        hsystem.system(cmd, print_command=True, dry_run=args.dry_run)
    # Step 3: Convert to PDF using pandoc.
    if do_incremental and os.path.exists(pdf_file_name):
        _LOG.warning("Step 3: Skipping, '%s' already exists", pdf_file_name)
    else:
        _LOG.info("Step 3: Converting to PDF using pandoc")
        header_dir = os.path.dirname(os.path.abspath(__file__))
        cmd = (
            f"pandoc {book_chapter_md} -o {pdf_file_name} "
            f"--pdf-engine=xelatex "
            f"-V geometry:margin=1in "
            f"-V fontsize=11pt "
            f"--highlight-style=tango "
            f"--include-in-header={header_dir}/header-style.tex"
        )
        hsystem.system(cmd, print_command=True, dry_run=args.dry_run)
    # Step 4: Open the PDF in Skim.
    _LOG.info("Step 4: Opening PDF in Skim")
    cmd = f"open -a /Applications/Skim.app {pdf_file_name}"
    hsystem.system(cmd, print_command=True, dry_run=args.dry_run)
    _LOG.info("Book chapter generated: %s", pdf_file_name)


if __name__ == "__main__":
    _main(_parse())
