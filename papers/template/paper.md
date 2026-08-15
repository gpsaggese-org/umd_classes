<!--
Markdown-based academic paper template, built with pandoc + Typst using the
official IEEE "charged-ieee" template. Modeled on
`papers/Optimal_strategy_for_racket_sports/paper.md`.

Usage:
  > cd papers/<your_paper_dir>
  > make            # build paper.pdf
  > make figures    # regenerate figures/*.png from figures/make_figures.py
  > make clean      # remove build artifacts

Files:
  paper.md            - this file (pandoc/Typst source)
  Makefile            - build recipe
  references.bib      - BibTeX bibliography
  ieee-template.typ   - pandoc Typst template (IEEE charged-ieee)
  figures/            - figure-generation script and outputs

Replace every `<...>` placeholder and the guidance bullets under each
heading with real content, then delete the guidance bullets. Sections in
< > are illustrative structure, not mandatory: add, remove, or rename
sections to fit the paper, but keep Introduction, Related Work,
Discussion/Limitations, and Conclusion.
-->
---
title: "<Paper Title: State the Problem and the Approach>"
author:
  - name: <Author Name(s), comma-separated>
    department: "<Department>"
    organization: "<Organization>"
    location: "<City, State/Country>"
    email: "`<email1@domain.edu, email2@domain.edu>`{=typst}"
abstract: |
  <Paragraph 1: what problem this paper addresses, and why existing
  approaches fall short (2-3 sentences).>
  <!-- -->
  <Paragraph 2: what this paper proposes and how it works, at a high
  level (2-4 sentences).>
  <!-- -->
  <Paragraph 3 (optional): a concrete result, illustration, or scope
  statement, plus limitations acknowledged up front.>
keywords:
  - <keyword 1>
  - <keyword 2>
  - <keyword 3>
bibliography: references.bib
---

# Introduction

- State the decision/problem being studied and why it is hard: uncertainty,
  time constraints, an adversary, scale, etc.
- Survey prior work in 2-3 categories, each with a concrete limitation
  (cite with `[@key]`).
- State this paper's approach as filling the gap between those categories.
- List the simplifying assumptions the framework rests on, as a bullet list
  (one bold lead-in per assumption).
- List the paper's main contributions as a bullet list; tie each
  contribution to the section that develops it, e.g. "(Section III)".
- Close with a one-sentence-per-section roadmap of the rest of the paper.

# Related Work

- One paragraph per line of related work, each starting with a bold
  lead-in phrase, e.g. **<Topic Name>.**, summarizing what prior work does
  and citing it.
- End each paragraph by contrasting that line of work with this paper's
  contribution: what question it answers that prior work does not.

# Problem Formulation

## <Notation and Setup>

- Define the state variables, geometry, or notation used throughout the
  paper.
- Include a parameter table if the problem has domain-specific constants
  (dimensions, rates, bounds), with citations for each value.

## Simplifying Assumptions

- Bullet list, bold lead-in per assumption, e.g. **<Assumption name>.**
  One sentence stating the simplification and, where possible, a citation
  or estimate of the error it introduces.

## Problem 1: <Name>

- Formal statement of the first sub-problem, with equations as needed.

## Problem 2: <Name>

- Formal statement of the second sub-problem, with equations as needed.
  Add a `## Problem 3: <Name>` section for additional sub-problems.

# <Core Methodology Section Name>

- One `##` subsection per methodological component (e.g. discretization,
  estimation procedure, algorithm). Include equations, and a computational
  complexity discussion if relevant to the paper's claims.

# <Extension Section Name> (optional)

- A theoretical extension that builds on the core methodology (e.g. a
  game-theoretic, statistical, or robustness layer). Omit this section if
  the paper has no such extension.

# Illustrative Worked Example

- A small, hand-computed or toy example that makes the method of the
  previous section(s) concrete. State plainly whether this is a full
  computational evaluation or a simplified illustration.
- Reference a figure, e.g.:

  ![<Figure caption describing what it shows.>](figures/example_figure.png)

- Reference a table if useful, e.g.:

  : <Table caption.>

  | <Column 1> | <Column 2> | <Column 3> |
  | :--- | ---: | ---: |
  | <value> | <value> | <value> |

# Discussion and Limitations

- One paragraph per limitation, bold lead-in per limitation, e.g.
  **<Limitation name>.** State what is not modeled or not validated, and
  the likely direction/magnitude of the resulting bias if known.

# Conclusion and Future Work

- Summarize the paper's contributions in 2-3 sentences.
- State plainly what has and has not been validated (e.g. "no
  computational implementation / empirical evaluation has been carried
  out" if that is the case).
- Numbered list of concrete next steps for future work.
