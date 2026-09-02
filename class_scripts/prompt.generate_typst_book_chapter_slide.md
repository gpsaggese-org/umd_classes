# Typst Book Chapter: Per-Slide Body Conversion

Mode-specific instructions for `--mode typst_aima`'s per-slide generation path. See
`prompt.generate_book_chapter_common.md` for the shared style guide (audience, tone,
content rules) and `prompt.generate_typst_book_chapter_common.md` for Typst rules
shared with the whole-document path (emphasis, semantic tags, formulas)
Unlike `prompt.generate_typst_book_chapter.md` (used for the older whole-document
generation path), this prompt is used to convert **one slide's entire body text at a
time**, in a single call, regardless of whether the source slide used a `:::
columns` two-column layout. That layout is a page-layout choice made in the `.smd`
source, not semantic content, so it is stripped out before you ever see the slide
(see "What You Will NEVER See in the Input" below) and is never reconstructed in the
output: you always write the slide as one flowing passage. Everything else
structural: chapter/section headings, figures, diagrams, and tables: is handled by
Python before and after this call. Your job is narrow: turn the given fragment of
`.smd` markdown into valid Typst body markup, expanding it into clear prose per the
shared style guide

## What You Will NEVER See in the Input, and Must NEVER Produce

- No document boilerplate (`#import`, `#show`, `#chapter(...)`)
- No headings (`#`, `##`, `###`, `*`)
- No `::: columns` / `:::: {.column width=X%}` pandoc div markers
- No raw code fences (` ```graphviz `, ` ```mermaid `, ` ```tikz `, ` ```{=typst} `)
  — these are already extracted out of your input

## Placeholder Tokens: Copy Verbatim, but Write Around Them

A token that looks like `@@FIGURE_1@@`, `@@FIGURE_2@@`, etc. stands in for a figure,
diagram, or table that has already been converted to Typst by Python. Copy each such
token to the output **exactly as written**, on its own line, with no surrounding
markup, no `#figure(...)`, no brackets. Never invent a token that was not in the
input, and never put the token itself inside a sentence

After the slide fragment, you are also given a `Figure manifest:` block listing each
token's Typst label and a one-line description of what it shows — never copy that
block into your output. For every token in the manifest, add one sentence to the
prose you are already writing (near the token, in the same fragment) that:

- refers to it by its label, written as plain text (`@fig:richardfeynman`,
  `@tab:foundations`, ...): this is a real Typst content reference and will render
  as an auto-numbered "Figure 1"/"Table 1"; do not alter, quote, or remove the `@`
- explains, in that same sentence, what it shows and how it connects to the
  surrounding discussion

If the fragment is nothing but a visual, with no other prose of its own (e.g., the
whole slide is one image), still write that one sentence — do not leave the token
standing with no prose around it at all

- Input:
  ```text
  - @Definition@: The term "Artificial Intelligence" was coined in 1956

  @@FIGURE_1@@
  ```

  Figure manifest:
  ```text
  @@FIGURE_1@@ -> label: fig:richardfeynman, shows: "Richard Feynman, 1965"
  ```
- Output:
  ```text
  The term "Artificial Intelligence" was coined in 1956. As @fig:richardfeynman
  shows, Richard Feynman's 1965 remark that "what I cannot create, I do not
  understand" captures the same spirit: building an intelligent system is itself a
  path to understanding intelligence.

  @@FIGURE_1@@
  ```

## Citations: Copy Verbatim

A `#cite("key")` call is already valid Typst; copy it through unchanged, at the same
position in the sentence. Never wrap it, quote it, or alter the key

## Semantic Tags: Dissolve, Don't Relabel

See "Semantic Tags in Typst" in `prompt.generate_typst_book_chapter_common.md`
for the rules and worked examples (how `@Definition@`, `@Pros@`/`@Cons@`,
`@Question@`, etc. dissolve into prose, and the `#strong` vs `#emph`
decision).

A `@Pros@`/`@Cons@` (or `@Problem@`/`@Solution@`) pair always reaches you together
in the same call, even if the source put them in separate `::: columns` panels (that
layout is stripped before you see it): merge them into one passage per the rule
above, never two labeled halves.

## Highlighting and Emphasis

See "Highlighting and Emphasis" in
`prompt.generate_typst_book_chapter_common.md`.

## Lists

- Not every `-` bullet in the input should become a Typst list item. A lone tagged
  bullet (`@Definition@`, `@Example@`, `@Remark@`, ...) that holds one short point
  becomes a plain sentence in the paragraph instead: see "Semantic Tags: Dissolve,
  Don't Relabel" above
- Keep a real Typst list only for content meant to be scanned as parallel items: an
  enumerated set of steps, assumptions, properties, or named alternatives. For a list
  you do keep, bullet lists (`- item`) and numbered lists (`1. item`) use the same
  syntax in Typst as in Markdown: copy the list structure and nesting as is, just
  convert the text of each item per the rules above

## Be Direct

- **Bad**:
  `- The slide suggests that _acting rationally_ encompasses more than just _thinking rationally_.`
- **Good**: `- Acting rationally encompasses more than just thinking rationally.`

## Other Rules

- Do not repeat a bullet verbatim; expand and explain it
- Close every `#strong[`, `#emph[`, `[...]`, `(...)` you open
- Output only the converted body: no commentary, no code fence wrapping the whole
  response
