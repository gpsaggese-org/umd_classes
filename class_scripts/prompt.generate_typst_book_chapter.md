# Typst Book Chapter

Mode-specific instructions for `--mode typst_aima`'s whole-document
generation path. See `prompt.generate_book_chapter_common.md` for the shared
style guide (audience, tone, content rules, constraints) and
`prompt.generate_typst_book_chapter_common.md` for Typst rules shared with
the per-slide path (emphasis, semantic tags, formulas): this file covers only
document structure and syntax specific to generating the whole document in
one call.

Copied and adapted from
`/Users/saggese/src/notes1/book_proposals/prompt.create_typst_book_chap_from_lesson_slides.md`.

## Output Format

- Generate Typst with a complete document structure, starting with the
  document template below (do not omit the `#import`/`#show` boilerplate)

## Document Template

```typst
// Import AIMA style formatting and macros.
#import "aima_style.typ": aima-style, chapter, algorithm, glossary, wrap-content
// Import the custom citation/bibliography system.
#import "/helpers_root/dev_scripts_helpers/typst/umd_references.typ": cite, references

// Document metadata
#set document(
  title: "[Chapter Title]",
  author: "[Course Title]",
)

// Apply the AIMA document template (page/text/heading set + show rules).
#show: aima-style

#chapter([CHAPTER_NUMBER], "[Chapter Title]")
```

- The chapter number and title, the course title, and the exact relative
  path for the `#import` line are given in the user message; use them
  verbatim

## Structural Hierarchy → Typst

- H1 (`#`) → `#chapter([num], "Title")` (only once, at the top; do not
  repeat for further H1s in the same file, use `== Title` instead if a
  second top-level topic appears)
- H2 (`##`) → `== Title`
- H3+ (`###`+) → `=== Title`
- Slide-level heading (`*`) → a paragraph starting with `#strong[Heading]`
  followed by its body text

## Source Attribution

- Comment marker: `//`
- Before each section of content taken from a slide, add a comment to help
  track source and maintain alignment with slides:
  ```typst
  // Slide: [slide title or description]
  ```
- Also add the shared source-attribution comment right above it:
  ```typst
  // From: msml610/lectures_source/Lesson10.2-Causal_Inference_for_Time_Series.smd:12 '## Some Heading'
  // Slide: Some Heading
  ```

## Algorithms and Pseudocode

- Use `#algorithm("NAME", [...])` for all structured algorithms, pseudocode,
  or procedural content
  - Format with `#h(1em)` for indentation levels
  - Use `*keyword*` for language keywords (function, if, loop, return, etc.)
  - Use symbolic notation ($sigma$, $in.not$, etc.) where appropriate

## Use Lists

```typst
#list(
  [Use *item1* when:
    #list([...])],
  [Use *item2* when:
    #list([...])],
)
```

## Figures

```typst
#figure(
  image("chart.png", width: 80%),
  caption: [Custom labeled figure.],
  kind: "figure",
  supplement: [Fig.],
  placement: auto,
) <fig:chart>
```

- `placement` takes a bare keyword (`auto`, `none`, `top`, `bottom`), not a
  string — `placement: "auto"` is a type error

- Every figure needs a label (`<fig:<description>>`), a one-line caption,
  and a reference in the text (`@fig:diagram`) that integrates it into the
  prose
- Image paths are relative to the source file location (use `../` as
  needed)
- If the source markdown documents the figure with a commented block (e.g.,
  a `graphviz`/`mermaid` code fence under a `rendered_image:begin` /
  `rendered_image:end` marker), keep that comment block above the `#figure`
  call and update its `label`/`caption` fields to match, so the two stay in
  sync:
  ```
  // rendered_image:begin
  // ```graphviz
  //    ... image code ...
  // ```
  // label=fig:my_label
  // caption=This is a caption
  // rendered_image:end
  ```

## Text-Wrapped Figures

- For a figure that should sit beside its own explanatory paragraph
  (magazine-style, text flowing around the image) instead of a full-width
  figure floating separately from the text, use `#wrap-content(...)` (from
  `aima_style.typ`, re-exporting the `wrap-it` package) instead of a bare
  `#figure(...)` call
- Signature: `#wrap-content([figure-block], align: right, column-gutter:
  1em, columns: (1fr, <width>))[body text]`
  - First positional argument: a content block containing the `#figure(...)`
    call (with its own `caption`, `kind`, `supplement`, and label as usual)
  - `align: right` places the figure on the right (the standard choice in
    this book; do not switch sides without a reason)
  - `columns: (1fr, <width>)` sets the text-column / figure-column widths;
    pick `<width>` (e.g. `20%`, `30%`, `40%`) to roughly match the figure's
    aspect ratio so it doesn't dominate or shrink to nothing
  - Trailing bracket content: the paragraph(s) that wrap around the figure;
    reference the figure from inside this text with `@fig:<label>`
  ```typst
  #wrap-content(
    [
      #figure(
        image("path/to/img.jpg", width: 100%),
        caption: [Caption text],
        kind: "figure",
        supplement: [Fig.],
      ) <fig:mylabel>
    ],
    align: right,
    column-gutter: 1em,
    columns: (1fr, 20%),
  )[
    Paragraph text that wraps around the figure, referencing it as
    @fig:mylabel.
  ]
  ```
- Use `#wrap-content` for one figure paired with the paragraph(s) discussing
  it (the common case for portraits, small diagrams, single illustrative
  images); keep a bare `#figure(...)` (no wrapping) for figures that need
  the full text width (tables via `styled-table`, multi-panel grids, wide
  diagrams) or that aren't tied to one specific paragraph
- `#wrap-content` still requires everything a normal figure needs: a label
  (`<fig:...>`), a one-line caption, and an in-text reference (`@fig:...`)
  inside the wrapped body

## Bibliography

- Never use Typst's native `#bibliography(...)`/`[@key]` citation syntax --
  it cannot render a custom link label (only the raw URL/DOI text itself
  can be hyperlinked). Use the shared `umd_references.typ` module instead,
  which renders inline citations as superscript bracketed numbers (`[10]`)
  and reference-list entries as `Author et al., "Title", Venue, Year. link`
  (see `.claude/references.rules.md`)
  (already imported by the document template above)
- Cite inline with `#cite("<bib-key>")` (not `[@<bib-key>]`):
  ```typst
  The Turing test #cite("turing1950computing") remains influential.
  ```
- End the `References` section with:
  ```typst
  #references("/msml610/lectures_source/refs.bib")
  ```

## Typst Syntax Requirements

- Follow Typst (not markdown) syntax: `#strong[text]` not `**text**`,
  `#emph[text]` not `*text*`/`_text_`, `== Heading` / `=== Subheading`
  (auto-numbered)
- Do NOT mix markdown and Typst syntax (no `**`, `__`, `~~`, `*text*`)
- Never rewrite the content inside a raw code fence (` ```mermaid `,
  ` ```graphviz `, ` ```tikz `, etc.) — copy it verbatim, character for
  character; those blocks are not Typst and must not contain `#strong[`,
  `#emph[`, or other Typst markup
- If the source slide markdown wraps native Typst calls in a pandoc raw
  block (` ```{=typst} ... ``` `) or an inline raw span (`` `code`{=typst} ``,
  used for a Typst call like `#cite(...)` sitting mid-sentence), do NOT
  copy that fence/span into the `.typ` output — the output document is
  already native Typst, so this pandoc-only wrapping is not executed
  there, it is shown as inert literal text. Strip the fence markers or
  the backticks + `{=typst}` and emit the enclosed Typst code directly
- Never leave semantic tags such as `@Definition@`, `@Question@`,
  `@Example@` verbatim in a `.typ` file — `@word` is Typst
  label-reference syntax there, so it is a compile error, not just a style
  issue; dissolve each into prose per "Semantic Tags in Typst" in
  `prompt.generate_typst_book_chapter_common.md`
- Always close `#strong[`, `[...]`, `(...)` with matching brackets
