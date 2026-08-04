#!/usr/bin/env python

"""
Generate an HTML page with links to lesson materials for a class or book.

For each lesson source file found in `{DIR}/lectures_source/`, builds an HTML
page linking to that lesson's generated artifacts:
- Slides PDF: `{DIR}/lectures_pdf/{LESSON}.pdf`
- Lecture commentary: `{DIR}/lectures_commentary/{LESSON}.book_chapter.html`
  and `{DIR}/lectures_commentary/{LESSON}.book_chapter.pdf`
- Lesson recap: `{DIR}/lectures_recap/{LESSON}.recap.md`

Each existing artifact is linked to its GitHub URL (via `to_github.py`) so the
page works when shared outside of a local checkout. Pass `--use_master` to
link to the `master` branch instead of the current branch.

By default the script stops with an error as soon as an expected artifact is
missing. Pass `--do_not_fail_on_warnings` to instead log a warning, list the
lesson without the missing link, and keep going.

Usage:
> publish_class_links.py --dir data605 --out_file data605/class_links.html
> publish_class_links.py --dir msml610 --out_file /tmp/links.html --do_not_fail_on_warnings --use_master

Import as:

import class_scripts.publish_class_links as cspucli
"""

import argparse
import glob
import logging
import os
from typing import List, NamedTuple

import dev_scripts_helpers.github.to_github as dshgtogi
import helpers.hdbg as hdbg
import helpers.hio as hio
import helpers.hparser as hparser
import helpers.hprint as hprint

_LOG = logging.getLogger(__name__)

# #############################################################################
# Constants
# #############################################################################

_LECTURES_SOURCE_SUBDIR = "lectures_source"
_LECTURES_PDF_SUBDIR = "lectures_pdf"
_LECTURES_COMMENTARY_SUBDIR = "lectures_commentary"
_LECTURES_RECAP_SUBDIR = "lectures_recap"

_LABEL_SLIDES_PDF = "Slides (PDF)"
_LABEL_COMMENTARY_HTML = "Commentary (HTML)"
_LABEL_COMMENTARY_PDF = "Commentary (PDF)"
_LABEL_RECAP = "Recap"

# GitHub serves `.html` files as raw source rather than rendering them, so
# route commentary links through htmlpreview.github.io to render in-browser.
_HTMLPREVIEW_PREFIX = "https://htmlpreview.github.io/?"

# Stylesheet embedded (not linked) into the generated page so it stays
# self-contained and portable regardless of where it is opened from.
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_CSS_FILE_PATH = os.path.join(_SCRIPT_DIR, "link-page-style.css")


# #############################################################################
# LessonArtifact
# #############################################################################


class LessonArtifact(NamedTuple):
    """
    Store one expected lesson artifact and whether it exists on disk.
    """

    label: str
    file_path: str
    exists: bool


class LessonPage(NamedTuple):
    """
    Store a lesson name and its list of `LessonArtifact` in display order.
    """

    lesson_name: str
    artifacts: List[LessonArtifact]


# #############################################################################
# Helper functions
# #############################################################################


def _find_lesson_names(dir_: str) -> List[str]:
    """
    Find the sorted lesson names from the lecture source files.

    :param dir_: course/book directory (e.g., `data605`)
    :return: sorted lesson names
        - Example: `['Lesson01.1-Intro', 'Lesson01.2-Big_Data']`
    """
    lectures_source_dir = os.path.join(dir_, _LECTURES_SOURCE_SUBDIR)
    hdbg.dassert_dir_exists(lectures_source_dir)
    pattern = os.path.join(lectures_source_dir, "Lesson*.txt")
    source_files = sorted(glob.glob(pattern))
    hdbg.dassert_lt(
        0,
        len(source_files),
        "No lecture source files found matching '%s'",
        pattern,
    )
    lesson_names = [
        os.path.splitext(os.path.basename(f))[0] for f in source_files
    ]
    _LOG.debug(hprint.to_str("lesson_names"))
    return lesson_names


def _get_lesson_artifacts(
    dir_: str, lesson_name: str, *, do_not_fail_on_warnings: bool
) -> List[LessonArtifact]:
    """
    Build and check the expected artifact paths for a lesson.

    :param dir_: course/book directory
    :param lesson_name: lesson name (e.g., `Lesson01.1-Intro`)
    :param do_not_fail_on_warnings: if `True`, log missing artifacts as
        warnings and keep going; if `False`, stop on the first missing
        artifact
    :return: one `LessonArtifact` per expected artifact, in display order
        (slides PDF, commentary HTML, commentary PDF, recap)
    """
    artifact_specs = [
        (
            _LABEL_SLIDES_PDF,
            os.path.join(dir_, _LECTURES_PDF_SUBDIR, f"{lesson_name}.pdf"),
        ),
        (
            _LABEL_COMMENTARY_HTML,
            os.path.join(
                dir_,
                _LECTURES_COMMENTARY_SUBDIR,
                f"{lesson_name}.book_chapter.html",
            ),
        ),
        (
            _LABEL_COMMENTARY_PDF,
            os.path.join(
                dir_,
                _LECTURES_COMMENTARY_SUBDIR,
                f"{lesson_name}.book_chapter.pdf",
            ),
        ),
        (
            _LABEL_RECAP,
            os.path.join(
                dir_, _LECTURES_RECAP_SUBDIR, f"{lesson_name}.recap.md"
            ),
        ),
    ]
    artifacts = []
    for label, file_path in artifact_specs:
        exists = os.path.isfile(file_path)
        if not exists:
            # Report the missing artifact: stop unless the caller asked to
            # only warn and keep going.
            hdbg.dassert_file_exists(
                file_path,
                "Missing '%s' for lesson '%s'",
                label,
                lesson_name,
                only_warning=do_not_fail_on_warnings,
            )
        artifacts.append(LessonArtifact(label, file_path, exists))
    return artifacts


# #############################################################################
# HTML generation
# #############################################################################


def _generate_html_page(
    dir_: str, lessons: List[LessonPage], *, use_master: bool
) -> str:
    """
    Generate the HTML page content listing artifact links for each lesson.

    Each existing artifact is linked to its GitHub URL (via
    `to_github.py`'s `_get_github_url()`) so that the page works when
    shared outside of a local checkout. The stylesheet from
    `link-page-style.css` is embedded (not linked) for the same reason.

    :param dir_: course/book directory, used for the page title
    :param lessons: one `LessonPage` per lesson, in display order
    :param use_master: if `True`, link to the `master` branch instead of
        the current branch
    :return: HTML page content
    """
    course_name = os.path.basename(dir_.rstrip("/"))
    css_content = hio.from_file(_CSS_FILE_PATH)
    # Build one table row per lesson.
    rows = []
    for lesson in lessons:
        cells = [f"    <td>{lesson.lesson_name}</td>"]
        for artifact in lesson.artifacts:
            if artifact.exists:
                href = dshgtogi._get_github_url(
                    file_path=artifact.file_path, use_master=use_master
                )
                if artifact.label == _LABEL_COMMENTARY_HTML:
                    # GitHub serves `.html` files as raw source rather than
                    # rendering them: preview via htmlpreview.github.io.
                    href = f"{_HTMLPREVIEW_PREFIX}{href}"
                cell = f'    <td><a href="{href}">{artifact.label}</a></td>'
            else:
                cell = f'    <td class="missing">{artifact.label}</td>'
            cells.append(cell)
        cells_str = "\n".join(cells)
        rows.append(f"  <tr>\n{cells_str}\n  </tr>")
    rows_str = "\n".join(rows)
    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
    <meta charset="utf-8">
    <title>{course_name} - Class Links</title>
    <style>
    {css_content}
    </style>
    </head>
    <body>
    <h1>{course_name} - Class Links</h1>
    <table>
    <tr>
      <th>Lesson</th>
      <th>Slides</th>
      <th>Commentary (HTML)</th>
      <th>Commentary (PDF)</th>
      <th>Recap</th>
    </tr>
    {rows_str}
    </table>
    </body>
    </html>
    """
    html = hprint.dedent(html)
    return html


# #############################################################################
# Script
# #############################################################################


def _parse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--dir",
        type=str,
        required=True,
        help="Course/book directory to scan for lessons (e.g., data605)",
    )
    parser.add_argument(
        "--out_file",
        type=str,
        required=True,
        help="Path to the output HTML file",
    )
    parser.add_argument(
        "--do_not_fail_on_warnings",
        action="store_true",
        help=(
            "Log missing lesson artifacts as warnings and keep going "
            "instead of stopping at the first missing file"
        ),
    )
    parser.add_argument(
        "--use_master",
        action="store_true",
        help=(
            "Link to the 'master' branch instead of the current branch "
            "when building the GitHub URLs for lesson artifacts"
        ),
    )
    hparser.add_verbosity_arg(parser)
    return parser


def _main(parser: argparse.ArgumentParser) -> None:
    args = parser.parse_args()
    hdbg.init_logger(verbosity=args.log_level, use_exec_path=True)
    dir_ = args.dir
    out_file = args.out_file
    do_not_fail_on_warnings = args.do_not_fail_on_warnings
    # Find the lessons to publish.
    lesson_names = _find_lesson_names(dir_)
    _LOG.info("Found %d lessons in '%s'", len(lesson_names), dir_)
    # Check each lesson's artifacts and collect the results.
    lessons = []
    for lesson_name in lesson_names:
        artifacts = _get_lesson_artifacts(
            dir_, lesson_name, do_not_fail_on_warnings=do_not_fail_on_warnings
        )
        lessons.append(LessonPage(lesson_name, artifacts))
    # Generate and write the HTML page.
    html = _generate_html_page(dir_, lessons, use_master=args.use_master)
    hio.to_file(out_file, html)
    _LOG.info("Wrote HTML page to '%s'", out_file)


if __name__ == "__main__":
    _main(_parse())
