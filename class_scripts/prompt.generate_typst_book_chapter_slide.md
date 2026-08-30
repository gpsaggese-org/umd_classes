# Typst Book Chapter — Per-Slide Body Conversion

Mode-specific instructions for `--mode typst_aima`'s per-slide generation
path. See `prompt.generate_book_chapter_common.md` for the shared style
guide (audience, tone, content rules).

Unlike `prompt.generate_typst_book_chapter.md` (used for the older
whole-document generation path), this prompt is used to convert **one
slide's body text at a time** (or one column panel of a slide, if the
slide uses a two-column layout). Everything structural — chapter/section
headings, the `::: columns` layout, figures, diagrams, and tables — is
handled by Python before and after this call. Your job is narrow: turn the
given fragment of `.smd` markdown into valid Typst body markup, expanding
it into clear prose per the shared style guide.

## What you will NEVER see in the input, and must NEVER produce

- No document boilerplate (`#import`, `#show`, `#chapter(...)`)
- No headings (`#`, `##`, `###`, `*`)
- No `::: columns` / `:::: {.column width=X%}` pandoc div markers
- No raw code fences (` ```graphviz `, ` ```mermaid `, ` ```tikz `,
  ` ```{=typst} `) — these are already extracted out of your input

## Placeholder tokens — copy verbatim, do not touch

A token that looks like `@@FIGURE_1@@`, `@@FIGURE_2@@`, etc. stands in for
a figure, diagram, or table that has already been converted to Typst by
Python. Copy each such token to the output **exactly as written**, on its
own line, with no surrounding markup, no `#figure(...)`, no brackets — do
not explain, describe, or wrap it. Never invent a token that was not in
the input.

- Input:
  ```text
  - @Definition@: The term "Artificial Intelligence" was coined in 1956

  @@FIGURE_1@@
  ```
  Output:
  ```text
  - #strong[Definition]: The term "Artificial Intelligence" was coined in
    1956.

  @@FIGURE_1@@
  ```

## Citations — copy verbatim

A `#cite("key")` call is already valid Typst; copy it through unchanged,
at the same position in the sentence. Never wrap it, quote it, or alter
the key.

## Semantic Tags

Do not leave the semantic tags (e.g., `@Definition@`, `@Example@`) in the
text — `@word` is Typst label-reference syntax, so leaving it verbatim is
a compile error, not just a style issue. Convert `@Tag@` into
`#strong[Tag]` and weave it into the sentence.

- Input:
  ```text
  - @Definition@: An **agent** is something that perceives and acts to
    reach a goal
  ```
  Output:
  ```text
  - #strong[Definition]: An #strong[agent] is something that perceives and
    acts to reach a goal.
  ```

- Input:
  ```text
  - @Limitations@
    - **Omniscience vs no-regrets**
      - Best is based on available information, not perfect knowledge
  ```
  Output:
  ```text
  - #strong[Limitations]:
    - #strong[Omniscience vs no-regrets]: the best decision is based on
      available information, not perfect knowledge.
  ```

## Highlighting and Emphasis

- `**text**` (markdown bold) → `#strong[text]`
- `_text_` (markdown italic) → `#emph[text]`
- Never leave `**`, `_`, or a bare `*` used as markdown emphasis in the
  output — those characters have no special meaning in Typst body markup
  and will render as literal asterisks/underscores
- A plain quoted phrase (`"..."`) stays a plain quoted string — do not
  prefix it with `#`. `#"text"` is a Typst string *expression*, not a
  quoted phrase, and drops the visible quote marks

## Lists

- Bullet lists (`- item`) and numbered lists (`1. item`) use the same
  syntax in Typst as in Markdown — copy the list structure and nesting as
  is, just convert the text of each item per the rules above

## Formulas

- Inline: `` `formula` `` for text-like expressions, or `$formula$` for
  inline math
- Display math: `$ formula $` on its own line/paragraph
- Prefer native Typst math syntax over raw LaTeX commands inside `$...$`
  (e.g., `subset.eq`, `|X|` instead of `\subseteq`, `\abs{X}`)

## Be Direct

- **Bad**: `- The slide suggests that _acting rationally_ encompasses more
  than just _thinking rationally_.`
- **Good**: `- Acting rationally encompasses more than just thinking
  rationally.`

## Other Rules

- Do not repeat a bullet verbatim; expand and explain it
- Close every `#strong[`, `#emph[`, `[...]`, `(...)` you open
- Output only the converted body — no commentary, no code fence wrapping
  the whole response
