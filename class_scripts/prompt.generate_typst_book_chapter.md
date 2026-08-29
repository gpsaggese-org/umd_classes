# Typst Book Chapter

Mode-specific instructions for `--mode typst_aima`. See
`prompt.generate_book_chapter_common.md` for the shared style guide
(audience, tone, content rules, constraints): this file covers only the
Typst syntax and structure.

Copied and adapted from
`/Users/saggese/src/notes1/book_proposals/prompt.create_typst_book_chap_from_lesson_slides.md`.

## Output Format

- Generate Typst with a complete document structure, starting with the
  document template below (do not omit the `#import`/`#show` boilerplate)

## Document Template

```typst
// Import AIMA style formatting and macros.
#import "aima_style.typ": aima-style, chapter, algorithm, glossary

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

## Highlighting and Emphasis

- Use `#strong[text]` for concepts, definitions, algorithm names, and key
  terms
- Use `*text*` for italics sparingly (emphasis only, not decoration)

## Algorithms and Pseudocode

- Use `#algorithm("NAME", [...])` for all structured algorithms, pseudocode,
  or procedural content
  - Format with `#h(1em)` for indentation levels
  - Use `*keyword*` for language keywords (function, if, loop, return, etc.)
  - Use symbolic notation ($sigma$, $in.not$, etc.) where appropriate

## Formulas

- Inline: `` `formula` `` for text-like expressions (e.g.,
  `` `f(n) = g(n) + h(n)` ``), or `$formula$` for inline math
- Display math: `$ formula $` on its own line/paragraph
- Prefer native Typst math syntax over raw LaTeX inside `$...$` (e.g.,
  `subset.eq`, `|X|` instead of `\subseteq`, `\abs{X}`)

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
  placement: "auto",
) <fig:chart>
```

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

## Typst Syntax Requirements

- Follow Typst (not markdown) syntax: `#strong[text]` not `**text**`,
  `*text*` for italic, `== Heading` / `=== Subheading` (auto-numbered)
- Do NOT mix markdown and Typst syntax (no `**`, `__`, `~~`)
- Always close `#strong[`, `[...]`, `(...)` with matching brackets
