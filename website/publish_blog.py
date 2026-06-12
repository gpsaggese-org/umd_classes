#!/usr/bin/env python

"""
Toggle a blog post between draft and published states.

The script
- renames the file (adding/removing `draft.` prefix)
- flips the `draft:` flag in the YAML frontmatter.

# Usage

## Publish a draft
> ./publish_blog.py --file draft.how_to.Use_OpenRouter.md

## Unpublish (revert to draft)
> ./publish_blog.py --file how_to.Use_OpenRouter.md --undo
"""

import argparse
import logging
import os
import re

import helpers.hdbg as hdbg
import helpers.hio as hio
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
        "--file",
        action="store",
        required=True,
        help="Path to the blog post markdown file",
    )
    parser.add_argument(
        "--undo",
        action="store_true",
        help="Reverse the transformation: published -> draft",
    )
    hparser.add_verbosity_arg(parser)
    return parser


def _publish(file_path: str) -> None:
    """
    Publish a draft blog post.

    Renames the file by removing the `draft.` prefix and sets
    `draft: true` to `draft: false` in the YAML frontmatter.

    :param file_path: Path to the draft blog post (e.g., `draft.my_post.md`)
    """
    _LOG.info("Publishing '%s'", file_path)
    basename = os.path.basename(file_path)
    # Validate that the file starts with `draft.` prefix.
    hdbg.dassert(
        basename.startswith("draft."),
        "File name must start with 'draft.' for publishing: '%s'",
        file_path,
    )
    # Read the file content using helpers.
    content = hio.from_file(file_path)
    # Swap 'draft: true' to 'draft: false' in the YAML frontmatter.
    content = re.sub(
        r"^draft:\s*true",
        "draft: false",
        content,
        count=1,
        flags=re.MULTILINE,
    )
    # Add or update the date to today in the YAML frontmatter.
    today = "2026-06-12"
    if re.search(r"^date:\s*\S+", content, re.MULTILINE):
        # Update existing date line.
        content = re.sub(
            r"^date:\s*\S+", "date: " + today, content, count=1, flags=re.MULTILINE
        )
    else:
        # Insert date line after the `draft:` line.
        content = re.sub(
            r"^(draft:\s*(?:true|false))\n",
            r"\1\n" + "date: " + today + "\n",
            content,
            count=1,
            flags=re.MULTILINE,
        )
    # Strip the `draft.` prefix to get the new file name.
    new_basename = basename[len("draft."):]
    new_path = os.path.join(os.path.dirname(file_path), new_basename)
    # Write the modified content and remove the old file.
    hio.to_file(new_path, content)
    os.remove(file_path)
    _LOG.info("Published -> '%s'", new_path)


def _unpublish(file_path: str) -> None:
    """
    Unpublish a blog post (revert to draft).

    Renames the file by prepending the `draft.` prefix and sets
    `draft: false` to `draft: true` in the YAML frontmatter.

    :param file_path: Path to the published blog post (e.g., `my_post.md`)
    """
    _LOG.info("Unpublishing '%s'", file_path)
    basename = os.path.basename(file_path)
    # Validate that the file does NOT start with `draft.` prefix.
    hdbg.dassert(
        not basename.startswith("draft."),
        "File name must not start with 'draft.' for unpublishing: '%s'",
        file_path,
    )
    # Read the file content using helpers.
    content = hio.from_file(file_path)
    # Swap 'draft: false' to 'draft: true' in the YAML frontmatter.
    content = re.sub(
        r"^draft:\s*false",
        "draft: true",
        content,
        count=1,
        flags=re.MULTILINE,
    )
    # Prepend the `draft.` prefix to get the new file name.
    new_basename = "draft." + basename
    new_path = os.path.join(os.path.dirname(file_path), new_basename)
    # Write the modified content and remove the old file.
    hio.to_file(new_path, content)
    os.remove(file_path)
    _LOG.info("Unpublished -> '%s'", new_path)


def _main(parser: argparse.ArgumentParser) -> None:
    args = parser.parse_args()
    hdbg.init_logger(verbosity=args.log_level, use_exec_path=True)
    file_path = args.file
    # Validate that the file exists.
    hdbg.dassert_file_exists(file_path, "File not found: '%s'", file_path)
    if args.undo:
        _unpublish(file_path)
    else:
        _publish(file_path)


if __name__ == "__main__":
    _main(_parse())