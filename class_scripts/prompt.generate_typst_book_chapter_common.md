# Typst Book Chapter: Shared Rules

Typst-specific rules shared by both `typst_aima` generation paths:
- `prompt.generate_typst_book_chapter.md` (whole-document generation)
- `prompt.generate_typst_book_chapter_slide.md` (per-slide body generation)

`gen_book_chapter.py` concatenates this file with whichever of the two above
applies, after `prompt.generate_book_chapter_common.md`. Keep this file free
of anything specific to only one path: document boilerplate, headings, and
figure embedding belong in `prompt.generate_typst_book_chapter.md`;
placeholder tokens and the input/output framing of a single slide fragment
belong in `prompt.generate_typst_book_chapter_slide.md`

## Highlighting and Emphasis

- `#strong[...]` is reserved for the term or claim being formally defined or
  named for the first time, normally in a sentence shaped like "#strong[Term]
  is/refers to/means ..." or the direct answer to a "what is X?" question. Use
  it sparingly: a handful of times per slide at most, and never for a list
  item's lead phrase
- Everything else the source marks for emphasis becomes `#emph[...]` instead:
  a `**bold**` list-item lead phrase, a term already defined earlier and
  mentioned again, or a word/phrase emphasized for rhetorical weight rather
  than being defined. Decide `#strong` vs `#emph` by the role the phrase
  plays in the sentence, not by mechanically mapping `**text**` → `#strong[text]`
  — the source's markdown bold does not settle it
- `_text_` (markdown italic) → `#emph[text]`
- Never leave `**`, `_`, or a bare `*` used as markdown emphasis in the output —
  those characters have no special meaning in Typst body markup and will render as
  literal asterisks/underscores
- A plain quoted phrase (`"..."`) stays a plain quoted string: do not prefix it with
  `#`. `#"text"` is a Typst string _expression_, not a quoted phrase, and drops the
  visible quote marks

- Input: `- **Omniscience vs. no-regrets**: the best decision is based on the
  information available at the time of acting.`
- Bad output (a list-item lead phrase is emphasis, not a definition):
  `- #strong[Omniscience vs. no-regrets]: the best decision is based on the
  information available at the time of acting.`
- Good output:
  `- #emph[Omniscience vs. no-regrets]: the best decision is based on the
  information available at the time of acting.`

## Semantic Tags in Typst

`@Definition@`, `@Example@`, `@Pros@`, `@Cons@`, `@Problem@`, `@Solution@`,
`@Question@`, `@Answer@`, `@Remark@`, `@Key idea@`, ... mark the _rhetorical role_ of
the bullet that follows; `@word` is also Typst label-reference syntax, so leaving it
verbatim is a compile error, not just a style issue. See "Dissolving Semantic Tags"
in `prompt.generate_book_chapter_common.md` for the rules: this is what applying
them looks like in Typst
Never emit the tag word itself as a `#strong[...]` label (`#strong[Definition]`,
`#strong[Pros]`, `#strong[Cons]`, `#strong[Problem]`, `#strong[Question]`, ...). Use
`#strong[...]` only for the actual term or claim being introduced

- Input:

  ```text
  - @Definition@: An **agent** is something that perceives and acts to
    reach a goal
  ```
- Bad output (relabels the tag, keeps the outline structure):
  ```text
  - #strong[Definition]: An #strong[agent] is something that perceives and
    acts to reach a goal.
  ```
- Good output (a plain sentence; only the term is bold):
  ```text
  An #strong[agent] is something that perceives and acts to reach a goal.
  ```

- Input:
  ```text
  - @Pros@
    - Express precise theory of the human mind as a computer program

  - @Cons@
    - Unknown workings of the human mind
    - Anthropocentric definition
  ```
- Bad output (two tag-labeled lists):
  ```text
  - #strong[Pros]:
    - Express precise theory of the human mind as a computer program.
  - #strong[Cons]:
    - Unknown workings of the human mind.
    - Anthropocentric definition.
  ```
- Good output (one passage weighing both sides):
  ```text
  Expressing this as a computer program forces a precise theory of the
  human mind instead of a vague verbal one. The cost is that the mind's
  own workings are still largely unknown, and the definition of "thinking
  like a human" is inescapably anthropocentric.
  ```

- Input:
  ```text
  - @Question@: What is artificial intelligence?
    - First, understand what **human intelligence** is
  ```
- Good output (the question stays a question; the tag disappears):
  ```text
  What is artificial intelligence? Answering that starts with
  understanding what #strong[human intelligence] is.
  ```

- Input:

  ```text
  - @Limitations@
    - **Omniscience vs no-regrets**
      - Best is based on available information, not perfect knowledge
  ```
  Good output (a genuinely enumerable set stays a list, without the tag label;
  the item's lead phrase is emphasis, not a definition, so it is `#emph`, not
  `#strong` — see "Highlighting and Emphasis" above):

  ```text
  - #emph[Omniscience vs no-regrets]: the best decision is based on
    available information, not perfect knowledge.
  ```

## Formulas

- Inline: `` `formula` `` for text-like expressions (e.g.,
  `` `f(n) = g(n) + h(n)` ``), or `$formula$` for inline math
- Display math: `$ formula $` on its own line/paragraph
- Prefer native Typst math syntax over raw LaTeX inside `$...$` (e.g.,
  `subset.eq`, `|X|` instead of `\subseteq`, `\abs{X}`)
