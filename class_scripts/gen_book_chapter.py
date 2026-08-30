#!/usr/bin/env python

r"""
Generate a book chapter from lecture slides using an LLM.

Converts a lecture source file in `.smd` format into a book chapter, in one
of three formats selected via `--mode`:
- `springer_latex`: a Springer LaTeX chapter (`.tex`)
- `typst_aima`: a Typst/AIMA-style chapter (`.typ`)
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
> gen_book_chapter.py --mode typst_aima msml610/10.2 --open_pdf

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
from typing import Dict, List, Optional, Tuple

import class_scripts.common_utils as csccouti
import dev_scripts_helpers.documentation.preprocess_notes as dshdprno
import dev_scripts_helpers.dockerize.lib_typst as dshdlity
import helpers.hdbg as hdbg
import helpers.hgit as hgit
import helpers.hio as hio
import helpers.hmarkdown_slide_iterator as hmaslite
import helpers.hparser as hparser
import helpers.hprint as hprint
import helpers.hsystem as hsystem

_LOG = logging.getLogger(__name__)

# #############################################################################
# Modes
# #############################################################################

# Map `--mode` to the output file extension.
_MODE_TO_EXTENSION = {
    "springer_latex": "tex",
    "typst_aima": "typ",
    "md": "md",
}

# Backends supported by `_call_llm()`.
# - "hllm": `helpers.hllm.get_completion()`
# - "hllm_cli": `helpers.hllm_cli.apply_llm()`, text-only
_LLM_BACKENDS = csccouti.LLM_BACKENDS


# #############################################################################
# Prompt building
# #############################################################################

# Map `--mode` to the mode-specific prompt file, sitting next to this script.
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_COMMON_PROMPT_FILE = os.path.join(
    _SCRIPT_DIR, "prompt.generate_book_chapter_common.md"
)
_MODE_TO_PROMPT_FILE = {
    "springer_latex": os.path.join(
        _SCRIPT_DIR, "prompt.generate_latex_book_chapter.md"
    ),
    "typst_aima": os.path.join(
        _SCRIPT_DIR, "prompt.generate_typst_book_chapter.md"
    ),
    "md": os.path.join(_SCRIPT_DIR, "prompt.generate_md_book_chapter.md"),
}

# Per-slide prompt file used only by the `typst_aima` per-slide generation
# path (see "Per-slide Typst generation" below): narrower than
# `prompt.generate_typst_book_chapter.md` since headings, columns, and
# figures are handled deterministically in Python and never reach the LLM.
_TYPST_SLIDE_PROMPT_FILE = os.path.join(
    _SCRIPT_DIR, "prompt.generate_typst_book_chapter_slide.md"
)


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


def _get_system_prompt_slide() -> str:
    """
    Build the system prompt used by the `typst_aima` per-slide generation
    path (see "Per-slide Typst generation" below).

    :return: combined system prompt
    """
    common_prompt = hio.from_file(_COMMON_PROMPT_FILE)
    slide_prompt = hio.from_file(_TYPST_SLIDE_PROMPT_FILE)
    system_prompt = f"{common_prompt}\n\n{slide_prompt}"
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
    if mode == "typst_aima":
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


def _call_llm(
    user_prompt: str, system_prompt: str, model: str, llm_backend: str
) -> str:
    """
    Generate the book chapter text using an LLM.

    :param user_prompt: user message (source content plus context)
    :param system_prompt: system prompt (style guide)
    :param model: LLM model to use, or "" to use the backend's default
    :param llm_backend: which LLM backend to use, one of `_LLM_BACKENDS`
    :return: generated chapter text
    """
    hdbg.dassert_in(llm_backend, _LLM_BACKENDS)
    return csccouti.call_llm_cached(user_prompt, system_prompt, model, llm_backend)


# #############################################################################
# Post-processing
# #############################################################################


# TODO(ai_gp): Convert it into a verbose one with explanation.
# TODO(ai_gp): Move inside the function
# Matches an entire response wrapped in a single fenced code block, e.g. the
# LLM answering with "```latex\n...\n```" despite being asked not to.
# The `\n?` before the closing fence makes the content group optional, so an
# empty fence (e.g., "```\n```", with no content line at all) also matches.
_CODE_FENCE_RE = re.compile(r"^```[a-zA-Z0-9_+-]*\n(.*?)\n?```\s*$", re.DOTALL)


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
        prefix = csccouti.get_comment_prefix(_MODE_TO_EXTENSION[mode])
        result = f"{prefix} {tag}\n{text}"
    return result


# #############################################################################
# Per-slide Typst generation
# #############################################################################

# Only `typst_aima` uses this path (see the `--mode` choice in `_parse()`).
# It follows the same approach as `gen_lecture_commentary.py`: structure
# (headings, `::: columns` layout, figures/diagrams/tables) is emitted
# deterministically by Python, and the LLM is called once per slide (or
# once per column panel, for a two-column slide), only to convert that
# slide's *prose* into Typst body markup. This keeps each LLM call small
# and focused, instead of asking one call to transform an entire
# multi-hundred-line lecture (and every construct in it) at once, which is
# what left artifacts like stray `::: columns` markers and `@Tag@` labels
# in the whole-document path (`_generate_book_chapter()` below, still used
# by `springer_latex` and `md`).

# Matches a `::: columns` / `:::: {.column width=X%}` ... `::::` / `:::`
# pandoc fenced-div layout (see "Use Lists"/columns in the `.smd` source
# convention). Column width is captured so `_wrap_columns()` can rebuild a
# Typst `#grid(columns: (...))` with the same proportions.
_COLUMNS_OPEN_RE = re.compile(r"^:::\s*columns\s*$")
_COLUMN_PANEL_OPEN_RE = re.compile(r"^::::\s*\{\.column\s+width=(\d+)%\}\s*$")
_COLUMN_PANEL_CLOSE_RE = re.compile(r"^::::\s*$")
_COLUMNS_CLOSE_RE = re.compile(r"^:::\s*$")

# A raw diagram-source code fence: rendered by `render_images.py` into a
# PNG (see `render_typst.sh`), never by the LLM.
_DIAGRAM_FENCE_RE = re.compile(
    r"```(graphviz|mermaid|tikz)\n(.*?)\n```", re.DOTALL
)
# A pandoc `{=typst}` raw block (e.g. a `#styled-table(...)`/`#references(...)`
# call already written in native Typst in the `.smd` source): valid only
# when spliced in unwrapped, since a Typst document (unlike a Pandoc
# markdown-to-Typst conversion) never executes a `{=typst}` fence.
_TYPST_RAW_FENCE_RE = re.compile(r"```\{=typst\}\n(.*?)\n```", re.DOTALL)
# A bare Markdown image, optionally followed (after a blank line) by an
# italicized caption line, e.g. `\footnotesize _Caption text_` or
# `_Caption text_`.
_IMAGE_RE = re.compile(
    r"!\[(?P<alt>[^\]]*)\]\((?P<path>[^)]+)\)(?P<attrs>\{[^}]*\})?"
    r"(?:\n\n?(?:\\footnotesize\s+)?_(?P<caption>[^_]+)_)?"
)
# Strips a leading course/lesson prefix off a figure basename, e.g.
# "L01.2.Richard_Feynman" -> "Richard_Feynman".
_FIGURE_PREFIX_RE = re.compile(r"^L\d+(?:\.\d+)*\.")
# A Pandoc inline raw-Typst span, e.g. `` `#cite("key")`{=typst} `` ->
# `#cite("key")`. This is Pandoc's markdown convention for embedding a
# literal Typst call inline in prose (so slides, which go through Pandoc,
# render it); a native `.typ` file has no such convention and would
# otherwise show the backticks and `{=typst}` suffix as literal text.
_INLINE_TYPST_RAW_RE = re.compile(r"`([^`]+)`\{=typst\}")


def _split_column_panels(body: str) -> List[Tuple[Optional[str], str]]:
    """
    Split a slide body into its column panels.

    :param body: raw slide body text (everything after the `* Title`
        line), possibly wrapped in a `::: columns` div
    :return: list of (width_percent, panel_content) tuples; `width_percent`
        is `None` and there is a single element if `body` has no `:::
        columns` wrapper
    """
    lines = body.splitlines()
    if not any(_COLUMNS_OPEN_RE.match(l.strip()) for l in lines):
        return [(None, body)]
    panels: List[Tuple[str, str]] = []
    in_columns = False
    cur_width: Optional[str] = None
    cur_lines: List[str] = []
    for line in lines:
        stripped = line.strip()
        if not in_columns:
            if _COLUMNS_OPEN_RE.match(stripped):
                in_columns = True
            continue
        panel_open = _COLUMN_PANEL_OPEN_RE.match(stripped)
        if panel_open:
            if cur_width is not None:
                panels.append((cur_width, "\n".join(cur_lines).strip("\n")))
            cur_width = panel_open.group(1)
            cur_lines = []
            continue
        if _COLUMN_PANEL_CLOSE_RE.match(stripped):
            if cur_width is not None:
                panels.append((cur_width, "\n".join(cur_lines).strip("\n")))
                cur_width = None
                cur_lines = []
            continue
        if _COLUMNS_CLOSE_RE.match(stripped):
            in_columns = False
            continue
        cur_lines.append(line)
    hdbg.dassert_lt(0, len(panels), "No column panels found in: %s", body)
    return panels  # type: ignore[return-value]


def _slugify_figure_name(path: str) -> str:
    """
    Turn an image path into a Typst label slug, e.g.
    ".../L01.2.Richard_Feynman.jpg" -> "richardfeynman".

    :param path: image path from the `.smd` source
    :return: lowercase alphanumeric label slug
    """
    base = os.path.splitext(os.path.basename(path))[0]
    base = _FIGURE_PREFIX_RE.sub("", base)
    slug = re.sub(r"[^a-zA-Z0-9]", "", base).lower()
    return slug


def _humanize_figure_name(path: str) -> str:
    """
    Derive a fallback caption from an image's filename, e.g.
    ".../L01.2.Richard_Feynman.jpg" -> "Richard Feynman".

    :param path: image path from the `.smd` source
    :return: human-readable caption derived from the filename
    """
    base = os.path.splitext(os.path.basename(path))[0]
    base = _FIGURE_PREFIX_RE.sub("", base)
    return base.replace("_", " ")


def _render_image_placeholder(match: "re.Match[str]", output_dir: str) -> str:
    """
    Deterministically render a Markdown image match (see `_IMAGE_RE`) as a
    Typst `#figure(...)` call.

    :param match: `_IMAGE_RE` match
    :param output_dir: directory the chapter file is written to (image
        paths are resolved relative to it)
    :return: Typst `#figure(...)` snippet
    """
    path = match.group("path")
    caption = match.group("caption")
    if not caption:
        caption = _humanize_figure_name(path)
    else:
        caption = caption.strip()
    label = _slugify_figure_name(path)
    rel_path = os.path.relpath(path, start=output_dir)
    lines = [
        "#figure(",
        f'  image("{rel_path}", width: 80%),',
        f"  caption: [{caption}],",
        '  kind: "figure",',
        "  supplement: [Fig.],",
        "  placement: auto,",
        f") <fig:{label}>",
    ]
    return "\n".join(lines)


def _render_diagram_placeholder(lang: str, code: str) -> str:
    """
    Pass a diagram-source fence (see `_DIAGRAM_FENCE_RE`) through
    unchanged, as a bare (uncommented) fence.

    `render_images.py` (run as a separate step by `render_typst.sh`,
    *after* this script) is the one that comments the code out, renders
    it, assigns it its sequential figure number, and inserts the
    `#figure(image(...))` call — it expects to find the fence exactly as
    written in the `.smd` source, not pre-commented or pre-numbered: doing
    either here would just make `render_images.py` comment it out a second
    time and never render it.

    :param lang: fence language (`graphviz`, `mermaid`, or `tikz`)
    :param code: diagram source code
    :return: the unchanged fence
    """
    return f"```{lang}\n{code.strip(chr(10))}\n```"


def _process_panel_body(
    body: str,
    *,
    output_dir: str,
    system_prompt: str,
    model: str,
    llm_backend: str,
) -> str:
    """
    Convert one column panel's raw `.smd` body into Typst.

    Figures, diagrams, and `{=typst}` raw blocks are pulled out into
    `@@FIGURE_N@@` placeholder tokens and rendered deterministically (see
    `prompt.generate_typst_book_chapter_slide.md` for the placeholder
    contract); only the remaining prose, if any, is sent to the LLM. A
    panel that is nothing but a figure/table skips the LLM call entirely.

    :param body: raw panel body text
    :param output_dir: directory the chapter file is written to
    :param system_prompt: system prompt for the LLM (slide-body prompt)
    :param model: LLM model to use, or "" to use the backend's default
    :param llm_backend: which LLM backend to use, one of `_LLM_BACKENDS`
    :return: Typst snippet for this panel
    """
    placeholders: Dict[str, str] = {}
    token_idx = [0]

    def _next_token() -> str:
        token_idx[0] += 1
        return f"@@FIGURE_{token_idx[0]}@@"

    def _repl_diagram(m: "re.Match[str]") -> str:
        token = _next_token()
        placeholders[token] = _render_diagram_placeholder(m.group(1), m.group(2))
        return token

    def _repl_typst_raw(m: "re.Match[str]") -> str:
        token = _next_token()
        placeholders[token] = m.group(1).strip("\n")
        return token

    def _repl_image(m: "re.Match[str]") -> str:
        token = _next_token()
        placeholders[token] = _render_image_placeholder(m, output_dir)
        return token

    body = _DIAGRAM_FENCE_RE.sub(_repl_diagram, body)
    body = _TYPST_RAW_FENCE_RE.sub(_repl_typst_raw, body)
    body = _IMAGE_RE.sub(_repl_image, body)
    remaining = body
    for token in placeholders:
        remaining = remaining.replace(token, "")
    if remaining.strip():
        raw_text = csccouti.call_llm_cached(
            body, system_prompt, model, llm_backend
        )
        text = _strip_code_fence(raw_text)
    else:
        # The panel is nothing but a figure/table: no prose to convert, so
        # skip the LLM call entirely.
        text = body
    for token, replacement in placeholders.items():
        text = text.replace(token, replacement)
    return text


def _wrap_columns(panel_texts: List[str], widths: List[str]) -> str:
    """
    Wrap converted column panels in a Typst `#grid(...)` with the same
    proportions as the source `::: columns` div.

    :param panel_texts: converted Typst snippet for each panel, in order
    :param widths: width percentage for each panel (e.g., "65"), in order
    :return: a `#grid(...)` snippet, or `panel_texts[0]` unchanged if there
        is only one panel
    """
    if len(panel_texts) == 1:
        return panel_texts[0]
    hdbg.dassert_eq(len(panel_texts), len(widths))
    col_defs = ", ".join(f"{w}%" for w in widths)
    lines = ["#grid(", f"  columns: ({col_defs}),", "  gutter: 1em,"]
    for text in panel_texts:
        indented = "\n".join(f"  {l}" if l else "" for l in text.splitlines())
        lines.append(f"  [\n{indented}\n  ],")
    lines.append(")")
    return "\n".join(lines)


def _generate_typst_slide(
    slide_lines: List[str],
    *,
    output_dir: str,
    system_prompt: str,
    model: str,
    llm_backend: str,
    source_file: str,
    line_number: int,
) -> str:
    """
    Convert one `* Slide Title` block (with its body, and optional
    `::: columns` layout) into Typst.

    :param slide_lines: lines of the slide, starting with `* Title`
    :param output_dir: directory the chapter file is written to
    :param system_prompt: system prompt for the LLM (slide-body prompt)
    :param model: LLM model to use, or "" to use the backend's default
    :param llm_backend: which LLM backend to use, one of `_LLM_BACKENDS`
    :param source_file: path to the `.smd` source, for the `// From:`
        provenance comment
    :param line_number: 1-based line number of the `* Title` line
    :return: Typst snippet for this slide
    """
    title = slide_lines[0][1:].strip()
    body = "\n".join(slide_lines[1:])
    panels = _split_column_panels(body)
    panel_texts = []
    widths: List[str] = []
    for width, content in panels:
        panel_texts.append(
            _process_panel_body(
                content,
                output_dir=output_dir,
                system_prompt=system_prompt,
                model=model,
                llm_backend=llm_backend,
            )
        )
        if width is not None:
            widths.append(width)
    body_out = _wrap_columns(panel_texts, widths) if widths else panel_texts[0]
    parts = [
        f"// From: {source_file}:{line_number} '{slide_lines[0]}'",
        f"// Slide: {title}",
        f"#strong[{title}]",
        "",
        body_out,
    ]
    return "\n".join(parts)


def _generate_typst_header(level: int, title: str, source_file: str, line_number: int) -> str:
    """
    Convert one `#`/`##`/`###`-prefixed heading line into Typst.

    A level-1 heading becomes a bold paragraph, not a `==` section: the
    chapter-level `#chapter(...)` call (using the lesson's metadata title,
    which is normally the same topic worded differently) has already been
    emitted once, at the top of the document, so a level-1 heading in the
    body is redundant with it rather than introducing a new chapter.

    :param level: heading level (1 for `#`, 2 for `##`, etc.)
    :param title: heading text, without the leading `#`s
    :param source_file: path to the `.smd` source, for the `// From:`
        provenance comment
    :param line_number: 1-based line number of the heading line
    :return: Typst snippet for this heading
    """
    marker = "#" * level
    heading = f"#strong[{title}]" if level == 1 else f"{'=' * level} {title}"
    parts = [
        f"// From: {source_file}:{line_number} '{marker} {title}'",
        f"// Slide: {title}",
        heading,
    ]
    return "\n".join(parts)


def _build_typst_document_header(
    course_title: str, chapter_title: str, chapter_num: str
) -> str:
    """
    Build the fixed Typst document boilerplate: imports, metadata, and the
    single `#chapter(...)` call.

    :param course_title: course title (e.g., "MSML610: Advanced Machine
        Learning")
    :param chapter_title: chapter title (e.g., "L01.2: AI and Machine
        Learning")
    :param chapter_num: chapter number (e.g., "1")
    :return: Typst document header
    """
    lines = [
        "// Import AIMA style formatting and macros.",
        '#import "../../helpers_root/dev_scripts_helpers/typst/'
        'aima_style.typ": (',
        "  aima-style, algorithm, chapter, glossary, styled-table,",
        ")",
        "// Import the custom citation/bibliography system.",
        '#import "/helpers_root/dev_scripts_helpers/typst/'
        'umd_references.typ": cite, references',
        "",
        "// Document metadata",
        "#set document(",
        f'  title: "{chapter_title}",',
        f'  author: "{course_title}",',
        ")",
        "",
        "// Apply the AIMA document template (page/text/heading set + show rules).",
        "#show: aima-style",
        "",
        f'#chapter({chapter_num}, "{chapter_title}")',
    ]
    return "\n".join(lines)


def _generate_typst_chapter_per_slide(
    input_file: str,
    output_file: str,
    model: str,
    llm_backend: str,
    lesson: str,
    course_title: str,
    chapter_title: str,
) -> None:
    """
    Generate a `typst_aima` book chapter one slide (or column panel) at a
    time and write it to disk (see "Per-slide Typst generation" above).

    :param input_file: path to the input markdown slides file
    :param output_file: path to write the generated `.typ` chapter to
    :param model: LLM model to use, or "" to use the backend's default
    :param llm_backend: which LLM backend to use, one of `_LLM_BACKENDS`
    :param lesson: lesson number (e.g., "10.2"), used to derive the Typst
        chapter number
    :param course_title: course title, used in the document metadata
    :param chapter_title: chapter title, used in `#chapter(...)` and the
        document metadata
    """
    hdbg.dassert_file_exists(input_file)
    content = _INLINE_TYPST_RAW_RE.sub(r"\1", hio.from_file(input_file))
    lines = content.splitlines()
    items = list(hmaslite.iterate_slide_lines(lines))
    system_prompt = _get_system_prompt_slide()
    output_dir = os.path.dirname(output_file) or "."
    chapter_num = lesson.split(".")[0]
    parts = [
        _build_typst_document_header(course_title, chapter_title, chapter_num)
    ]
    for item in items:
        if item["type"] == "header":
            first_line = item["content"][0]
            level = len(first_line) - len(first_line.lstrip("#"))
            title = first_line.lstrip("#").strip()
            parts.append(
                _generate_typst_header(
                    level, title, input_file, item["line_number"]
                )
            )
        elif item["type"] == "slide":
            parts.append(
                _generate_typst_slide(
                    item["content"],
                    output_dir=output_dir,
                    system_prompt=system_prompt,
                    model=model,
                    llm_backend=llm_backend,
                    source_file=input_file,
                    line_number=item["line_number"],
                )
            )
        # "comment"/"preamble" items are metadata/frontmatter, already
        # captured by `_extract_course_and_title()`, and not part of the
        # chapter body.
    text = "\n\n".join(parts)
    text = _insert_provenance_tag(text, "typst_aima")
    hio.to_file(output_file, text)
    _LOG.info("Wrote book chapter to: %s", output_file)


# #############################################################################
# Book chapter generation
# #############################################################################


def _generate_book_chapter(
    input_file: str,
    output_file: str,
    mode: str,
    model: str,
    llm_backend: str,
    lesson: str,
) -> None:
    """
    Generate a book chapter from lecture slides and write it to disk.

    :param input_file: path to the input markdown slides file
    :param output_file: path to write the generated chapter to
    :param mode: generation mode, one of `_MODE_TO_EXTENSION`
    :param model: LLM model to use, or "" to use the backend's default
    :param llm_backend: which LLM backend to use, one of `_LLM_BACKENDS`
    :param lesson: lesson number (e.g., "10.2"), used to derive the Typst
        chapter number
    """
    hdbg.dassert_file_exists(input_file)
    hdbg.dassert_in(mode, _MODE_TO_EXTENSION)
    content = hio.from_file(input_file)
    course_title, chapter_title = _extract_course_and_title(input_file, content)
    if mode == "typst_aima":
        # Per-slide generation path (see "Per-slide Typst generation"
        # above): structure is deterministic, the LLM only converts prose.
        _generate_typst_chapter_per_slide(
            input_file,
            output_file,
            model,
            llm_backend,
            lesson,
            course_title,
            chapter_title,
        )
        return
    system_prompt = _get_system_prompt(mode)
    user_prompt = _build_user_prompt(
        input_file, content, mode, course_title, chapter_title, lesson
    )
    raw_text = _call_llm(user_prompt, system_prompt, model, llm_backend)
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


def _lint_with_lint_text(output_file: str, *, dry_run: bool) -> None:
    """
    Lint a Markdown or LaTeX file in place with `lint_text.py`.

    :param output_file: path to the file to lint (its type is inferred
        from its extension)
    :param dry_run: print the command without executing it
    """
    cmd = f"lint_text.py -i {output_file} -o {output_file}"
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
    if mode == "typst_aima":
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
            "PDF preview is not supported for --mode springer_latex. You "
            "need to compile the book (chapter file: '%s')",
            output_file,
        )
        return
    # TODO(gp): This should be a function checking on mac
    cmd = f"open -a /Applications/Skim.app {pdf_file}"
    hsystem.system(cmd, print_command=True, dry_run=dry_run)


# #############################################################################
# CLI
# #############################################################################


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
        "SNmono LaTeX chapter, 'typst_aima' for a Typst/AIMA-style chapter, "
        "'md' for a plain Markdown chapter",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="",
        help="Path to the output book chapter file (default: derived from "
        "the input and --mode, as '<dir>/book/<basename>.<ext>')",
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
        "--model",
        type=str,
        default="",
        help="LLM model to use (e.g., 'gpt-4o', 'claude-opus-4'); empty "
        "string (default) uses the --llm_backend's default model",
    )
    parser.add_argument(
        "--open_pdf",
        action="store_true",
        help="Compile the generated chapter to PDF and open it in Skim "
        "(supported for --mode typst_aima and --mode md only)",
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
    extension = _MODE_TO_EXTENSION[args.mode]
    if args.output:
        # Use the user-provided output path, derived `out_dir`/`basename`.
        output_file = args.output
        out_dir = os.path.dirname(output_file) or "."
        basename = os.path.splitext(os.path.basename(output_file))[0]
    else:
        out_dir = f"{dir_arg}/book"
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
        _LOG.info(
            "\n%s",
            hprint.frame(f"Step 2: Generating '{args.mode}' book chapter"),
        )
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
                args.model,
                args.llm_backend,
                lesson_arg,
            )
    # Step 3: Track the generated file in git.
    _LOG.info("\n%s", hprint.frame("Step 3: Adding book chapter to git"))
    csccouti.git_add_with_retry(output_file, dry_run=args.dry_run)
    # Step 4: Lint the generated file (mode-specific).
    _LOG.info("\n%s", hprint.frame(f"Step 4: Linting '{args.mode}' file"))
    if args.mode == "typst_aima":
        # TODO(gp): Move this inside lint_text.py to support also typst.
        _lint_typst_file(output_file, dry_run=args.dry_run)
    else:
        _lint_with_lint_text(output_file, dry_run=args.dry_run)
    # Step 5: Compile to PDF and open in Skim.
    if args.open_pdf:
        _LOG.info(
            "\n%s",
            hprint.frame("Step 5: Compiling to PDF and opening in Skim"),
        )
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
