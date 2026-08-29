#!/usr/bin/env python

r"""
Generate a book chapter from lecture slides using an LLM.

Converts a lecture source file in `.smd` format into a book chapter, in one
of three formats selected via `--mode`:
- `springer_latex`: a Springer LaTeX chapter (`.tex`)
# TODO(ai_gp): -> typst_aima
- `typst`: a Typst/AIMA-style chapter (`.typ`)
- `md`: a plain Markdown chapter (`.md`)

The style guide for all three modes is split across:
- `prompt.generate_book_chapter_common.md`: shared style guide (audience,
  tone, content rules, constraints) common to all modes
- `prompt.generate_latex_book_chapter.md`, `prompt.generate_typst_book_chapter.md`,
  `prompt.generate_md_book_chapter.md`: mode-specific syntax and structure

The output is written next to the input's course directory, in a sibling
`book/` directory (e.g., `msml610/lectures_source/Lesson10.2-Name.smd` ->
`msml610/book/Lesson10.2-Name.<ext>`), with the same base name as the input
and the extension for the selected `--mode`.

This script performs the following steps:
1. Generate the book chapter text via LLM
2. Add the generated file to Git
3. Lint the generated file
4. Compile to PDF
5. Open the PDF

# Usage Example

- Generate a Springer LaTeX chapter for MSML610 lesson 08.1:
> gen_book_chapter.py --mode springer_latex msml610/08.1

- Generate a Typst chapter for MSML610 lesson 10.2 and preview the PDF:
> gen_book_chapter.py --mode typst msml610/10.2 --open_pdf

- Generate a Markdown chapter for DATA605 lesson 01.1:
> gen_book_chapter.py --mode md data605/01.1

Import as:

import class_scripts.gen_book_chapter as clgeboch
"""

import argparse
import logging
import os
import re
import shutil
from typing import Tuple

import class_scripts.common_utils as csccouti
import dev_scripts_helpers.documentation.preprocess_notes as dshdprno
import dev_scripts_helpers.dockerize.lib_typst as dshdlity
import helpers.hcache_simple as hcacsimp
import helpers.hdbg as hdbg
import helpers.hgit as hgit
import helpers.hio as hio
import helpers.hparser as hparser
import helpers.hsystem as hsystem

_LOG = logging.getLogger(__name__)

# #############################################################################
# Modes
# #############################################################################

# Map `--mode` to the output file extension.
_MODE_TO_EXTENSION = {
    "springer_latex": "tex",
    "typst": "typ",
    "md": "md",
}

# TODO(ai_gp): Move close to the use.
# Map `--mode` to the mode-specific prompt file, sitting next to this script.
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_COMMON_PROMPT_FILE = os.path.join(
    _SCRIPT_DIR, "prompt.generate_book_chapter_common.md"
)
_MODE_TO_PROMPT_FILE = {
    "springer_latex": os.path.join(
        _SCRIPT_DIR, "prompt.generate_latex_book_chapter.md"
    ),
    "typst": os.path.join(
        _SCRIPT_DIR, "prompt.generate_typst_book_chapter.md"
    ),
    "md": os.path.join(_SCRIPT_DIR, "prompt.generate_md_book_chapter.md"),
}

# Map `--mode` to the comment marker used for the provenance tag (`md` uses
# an HTML comment, handled separately since it needs a closing marker too).
# TODO(ai_gp): Is there any general function for this? If not let's factor out
# from multiple places.
_MODE_TO_COMMENT_PREFIX = {
    "springer_latex": "%",
    "typst": "//",
}

# Backends supported by `_call_llm()`.
# - "hllm": `helpers.hllm.get_completion()`
# - "hllm_cli": `helpers.hllm_cli.apply_llm()`, text-only
_LLM_BACKENDS = ("hllm", "hllm_cli")


# #############################################################################
# Prompt building
# #############################################################################


def _get_system_prompt(mode: str) -> str:
    """
    Build the system prompt for `mode` by concatenating the shared style
    guide with the mode-specific instructions.

    :param mode: generation mode, one of `_MODE_TO_EXTENSION`
    :return: combined system prompt
    """
    hdbg.dassert_in(mode, _MODE_TO_PROMPT_FILE)
    common_prompt = hio.from_file(_COMMON_PROMPT_FILE)
    mode_prompt = hio.from_file(_MODE_TO_PROMPT_FILE[mode])
    system_prompt = f"{common_prompt}\n\n{mode_prompt}"
    return system_prompt


def _add_line_numbers(content: str) -> str:
    """
    Prefix each line of `content` with its 1-based line number.

    Used so the LLM can populate accurate `From: <file>:<line num> ...`
    source-attribution comments (see "Source Input Format" in
    `prompt.generate_book_chapter_common.md`).

    :param content: text to number
    :return: `content` with a `"<line num> | "` prefix on every line
    """
    lines = content.splitlines()
    numbered_lines = [
        f"{i:>5} | {line}" for i, line in enumerate(lines, start=1)
    ]
    numbered_content = "\n".join(numbered_lines)
    return numbered_content


def _extract_course_and_title(input_file: str, content: str) -> Tuple[str, str]:
    """
    Extract the course title and chapter title from the lecture source.

    :param input_file: path to the input markdown slides file
    :param content: content of `input_file`
    :return: tuple of (course_title, chapter_title); `course_title` is ""
        if not found, `chapter_title` falls back to the input's base name
    """
    lines = content.split("\n")
    metadata, _ = dshdprno.extract_slide_metadata(lines)
    course_title = metadata.get("course_title", "")
    chapter_title = csccouti.extract_title_from_markdown(input_file)
    if not chapter_title:
        chapter_title = os.path.splitext(os.path.basename(input_file))[0]
    return course_title, chapter_title


def _build_user_prompt(
    input_file: str,
    content: str,
    mode: str,
    course_title: str,
    chapter_title: str,
    lesson: str,
) -> str:
    """
    Build the user prompt: a header with the context the LLM needs (source
    file path, titles, mode-specific metadata), followed by the numbered
    source content.

    :param input_file: path to the input markdown slides file
    :param content: content of `input_file`
    :param mode: generation mode, one of `_MODE_TO_EXTENSION`
    :param course_title: course title (e.g., "MSML610: Advanced Machine
        arning"), empty if not found in the source
    :param chapter_title: chapter title to use verbatim in the output
    :param lesson: lesson number (e.g., "10.2"), used to derive the Typst
        chapter number
    :return: user prompt to send to the LLM
    """
    header_lines = [
        f"Source file: {input_file}",
        f"Chapter title: {chapter_title}",
        f"Course title: {course_title}",
    ]
    if mode == "typst":
        # The chapter number is the integer part of the lesson number
        # (e.g., "10.2" -> "10").
        chapter_num = lesson.split(".")[0]
        header_lines.append(f"Chapter number: {chapter_num}")
        # `<dir>/book/` is always 2 directories below the repo root, so the
        # relative import path is always the same regardless of `<dir>`.
        header_lines.append(
            "Typst import line: "
            '#import "../../helpers_root/dev_scripts_helpers/typst/'
            'aima_style.typ": aima-style, algorithm, chapter, glossary'
        )
    header = "\n".join(header_lines)
    numbered_content = _add_line_numbers(content)
    user_prompt = f"{header}\n\n---\n\n{numbered_content}"
    return user_prompt


# #############################################################################
# LLM call
# #############################################################################


# TODO(ai_gp): Factor it out and use it everywhere is needed.
@hcacsimp.simple_cache(cache_type="json")
def _call_llm(user_prompt: str, system_prompt: str, llm_backend: str) -> str:
    """
    Generate the book chapter text using an LLM.

    :param user_prompt: user message (source content plus context)
    :param system_prompt: system prompt (style guide)
    :param llm_backend: which LLM backend to use, one of `_LLM_BACKENDS`
    :return: generated chapter text
    """
    hdbg.dassert_in(llm_backend, _LLM_BACKENDS)
    if llm_backend == "hllm":
        import helpers.hllm as hllm

        response = hllm.get_completion(
            user_prompt=user_prompt,
            system_prompt=system_prompt,
            model="",
            cache_mode="NORMAL",
            temperature=0.1,
        )
    else:
        import helpers.hllm_cli as hllmcli

        response, _ = hllmcli.apply_llm(
            user_prompt,
            system_prompt=system_prompt,
            model="",
            backend="library",
        )
    return str(response)


# #############################################################################
# Post-processing
# #############################################################################


# Matches an entire response wrapped in a single fenced code block, e.g. the
# LLM answering with "```latex\n...\n```" despite being asked not to.
_CODE_FENCE_RE = re.compile(r"^```[a-zA-Z0-9_+-]*\n(.*)\n```\s*$", re.DOTALL)


def _strip_code_fence(text: str) -> str:
    """
    Strip a single Markdown code fence wrapping the entire `text`, if any.

    :param text: raw LLM output
    :return: `text` without an enclosing code fence
    """
    text = text.strip()
    match = _CODE_FENCE_RE.match(text)
    if match:
        text = match.group(1)
    return text


def _insert_provenance_tag(text: str, mode: str) -> str:
    """
    Insert a comment with the git hash and timestamp of generation, so that
    one can tell from which commit and when the file was generated.

    :param text: generated chapter text
    :param mode: generation mode, one of `_MODE_TO_EXTENSION`
    :return: `text` with the provenance tag inserted
    """
    tag = hgit.get_generation_tag()
    if mode == "md":
        # Insert after the YAML front matter, if any, since `---` must
        # stay the first line of the file for pandoc to recognize it.
        comment = f"<!-- {tag} -->"
        yaml_end = text.find("\n---\n") if text.startswith("---\n") else -1
        if yaml_end == -1:
            result = f"{comment}\n\n{text}"
        else:
            split_at = yaml_end + len("\n---\n")
            result = f"{text[:split_at]}{comment}\n\n{text[split_at:]}"
    else:
        prefix = _MODE_TO_COMMENT_PREFIX[mode]
        result = f"{prefix} {tag}\n{text}"
    return result


# #############################################################################
# Book chapter generation
# #############################################################################


def _generate_book_chapter(
    input_file: str,
    output_file: str,
    mode: str,
    llm_backend: str,
    lesson: str,
) -> None:
    """
    Generate a book chapter from lecture slides and write it to disk.

    :param input_file: path to the input markdown slides file
    :param output_file: path to write the generated chapter to
    :param mode: generation mode, one of `_MODE_TO_EXTENSION`
    :param llm_backend: which LLM backend to use, one of `_LLM_BACKENDS`
    :param lesson: lesson number (e.g., "10.2"), used to derive the Typst
        chapter number
    """
    hdbg.dassert_file_exists(input_file)
    hdbg.dassert_in(mode, _MODE_TO_EXTENSION)
    content = hio.from_file(input_file)
    course_title, chapter_title = _extract_course_and_title(input_file, content)
    system_prompt = _get_system_prompt(mode)
    user_prompt = _build_user_prompt(
        input_file, content, mode, course_title, chapter_title, lesson
    )
    raw_text = _call_llm(user_prompt, system_prompt, llm_backend)
    text = _strip_code_fence(raw_text)
    text = _insert_provenance_tag(text, mode)
    hio.to_file(output_file, text)
    _LOG.info("Wrote book chapter to: %s", output_file)


def _lint_typst_file(typst_file: str, *, dry_run: bool) -> None:
    """
    Lint a Typst file in place with `typstyle`, if it is on the PATH.

    :param typst_file: path to the `.typ` file to lint
    :param dry_run: print the command without executing it
    """
    if shutil.which("typstyle") is None:
        _LOG.warning(
            "'typstyle' not found on PATH, skipping lint of '%s'", typst_file
        )
        return
    cmd = f"typstyle --inplace --wrap-text -l 80 {typst_file}"
    hsystem.system(cmd, print_command=True, dry_run=dry_run)


def _compile_and_open_pdf(
    output_file: str,
    out_dir: str,
    basename: str,
    mode: str,
    script_dir: str,
    *,
    dry_run: bool,
) -> None:
    """
    Compile the generated book chapter to PDF and open it in Skim, if possible.

    :param output_file: path to the generated chapter file
    :param out_dir: directory holding the generated chapter (and where the
        PDF is written)
    :param basename: chapter file base name, without extension
    :param mode: generation mode, one of `_MODE_TO_EXTENSION`
    :param script_dir: directory of this script (for pandoc header files)
    :param dry_run: print the commands without executing them
    """
    pdf_file = os.path.join(out_dir, f"{basename}.pdf")
    if mode == "typst":
        if dry_run:
            _LOG.warning(
                "As per user request, not compiling '%s' to PDF", output_file
            )
        else:
            repo_root = hgit.find_git_root()
            dshdlity.run_dockerized_typst(
                output_file, pdf_file, [], typst_root_dir=repo_root
            )
    elif mode == "md":
        csccouti.convert_markdown_to_pdf(
            output_file, pdf_file, script_dir, dry_run=dry_run
        )
    else:
        _LOG.warning(
            "PDF preview is not supported for --mode springer_latex. You need to compile the book",
            out_dir,
            out_dir,
            output_file,
        )
        return
    # TODO(gp): This should be a function checking on mac
    cmd = f"open -a /Applications/Skim.app {pdf_file}"
    hsystem.system(cmd, print_command=True, dry_run=dry_run)


# #############################################################################
# CLI
# #############################################################################

# TODO(ai_gp): typst -> typst_aima
# TODO(ai_gp): Add output

def _parse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=hparser.CustomHelpFormatter,
    )
    # TODO(gp2): This should be factor out (maybe also dry run and no_incremental)?
    parser.add_argument(
        "input",
        type=str,
        help="Lecture specification: 'data605/08.1', 'msml610/08.1', "
        "or file path 'msml610/lectures_source/Lesson10.2-Name.smd'",
    )
    parser.add_argument(
        "--mode",
        type=str,
        choices=list(_MODE_TO_EXTENSION.keys()),
        required=True,
        help="Output format to generate: 'springer_latex' for a Springer "
        "SNmono LaTeX chapter, 'typst' for a Typst/AIMA-style chapter, "
        "'md' for a plain Markdown chapter",
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
    parser.add_argument(
        "--llm_backend",
        type=str,
        choices=_LLM_BACKENDS,
        default="hllm",
        help=(
            "LLM backend to use for book chapter generation: 'hllm' "
            "(default) uses `helpers.hllm`, 'hllm_cli' uses "
            "`helpers.hllm_cli` (text-only)"
        ),
    )
    parser.add_argument(
        "--open_pdf",
        action="store_true",
        help="Compile the generated chapter to PDF and open it in Skim "
        "(supported for --mode typst and --mode md only)",
    )
    hparser.add_verbosity_arg(parser)
    return parser


def _main(parser: argparse.ArgumentParser) -> None:
    args = parser.parse_args()
    hdbg.init_logger(verbosity=args.log_level, use_exec_path=True)
    # Parse and validate arguments.
    dir_arg, lesson_arg = csccouti.parse_lesson_spec(args.input)
    csccouti.validate_dir_lesson_args(dir_arg, lesson_arg)
    # Get source name and compute the output path.
    src_name = csccouti.get_source_name(dir_arg, lesson_arg)
    input_file = f"{dir_arg}/lectures_source/{src_name}"
    out_dir = f"{dir_arg}/book"
    extension = _MODE_TO_EXTENSION[args.mode]
    basename = os.path.splitext(src_name)[0]
    output_file = f"{out_dir}/{basename}.{extension}"
    do_incremental = not args.no_incremental
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Step 1: Create the output directory.
    csccouti.ensure_dir_exists(out_dir)
    # Step 2: Generate the book chapter.
    if do_incremental and os.path.exists(output_file):
        _LOG.warning("Step 2: Skipping, '%s' already exists", output_file)
    else:
        _LOG.info("Step 2: Generating '%s' book chapter", args.mode)
        if args.dry_run:
            _LOG.warning(
                "As per user request, not generating book chapter for '%s'",
                input_file,
            )
        else:
            _generate_book_chapter(
                input_file,
                output_file,
                args.mode,
                args.llm_backend,
                lesson_arg,
            )
    # Step 3: Track the generated file in git.
    _LOG.info("Step 3: Adding book chapter to git")
    csccouti.git_add_with_retry(output_file, dry_run=args.dry_run)
    # Step 4: Lint the generated file (mode-specific).
    # TODO(ai_gp): Generalize for markdown and latex use lint_text.py
    if args.mode == "typst":
        _LOG.info("Step 4: Linting Typst file")
        _lint_typst_file(output_file, dry_run=args.dry_run)
    # Step 5: Compile to PDF and open in Skim.
    if args.open_pdf:
        # TODO(ai_gp): use hprint.frame for all this one.
        _LOG.info("Step 5: Compiling to PDF and opening in Skim")
        _compile_and_open_pdf(
            output_file,
            out_dir,
            basename,
            args.mode,
            script_dir,
            dry_run=args.dry_run,
        )
    _LOG.info("Book chapter generated: %s", output_file)


if __name__ == "__main__":
    _main(_parse())
