---
title: "Produce professional images"
authors:
  - gpsaggese
date: 2026-06-22
description:
categories:
  - "Developer Tools"
draft: true
---

TL;DR: [Summary needed]

<!-- more -->

SVG vs Tikz

Both can produce professional vector output, but they're suited to different workflows. Here's how they compare:

# SVG
Strengths:

Native to web/browsers — direct embedding, no conversion
Excellent tooling: Inkscape, Illustrator, Figma all edit it visually and natively
Great for illustrations, icons, logos, complex paths, gradients, freeform art
Easy to manipulate programmatically (JS/CSS) for interactivity or animation
Universally supported by design and publishing pipelines

Weaknesses:

Not great for precise mathematical/technical diagrams (plots, geometric constructions) unless paired with a library
Typography integration with LaTeX documents is clunky (font/baseline mismatches)

# TikZ (LaTeX)
Strengths:

Best-in-class for technical/scientific diagrams: plots, graphs, geometric figures, circuit diagrams, trees, automata
Perfect typographic consistency with LaTeX documents — same fonts, same math rendering, no mismatch
Precise coordinate-based, programmatic control (great for reproducibility, parametrized figures)
Compiles to vector PDF — ideal for academic papers, theses, textbooks
Huge ecosystem of libraries (pgfplots, tikz-cd, forest, circuitikz, etc.)

Weaknesses:

Steep learning curve, verbose syntax
No visual/WYSIWYG editing — pure code, slower iteration
Not native to the web; needs PDF→SVG/PNG conversion for online use
Overkill or awkward for purely artistic/illustrative work

# To convert 

inkscape input.svg --export-type=pdf --export-filename=output.pdf

Just use SVG directly — Typst has native SVG support via #image():

#image("diagram.svg")
#image("figure.pdf")

#

.claude/skills/svg.rules.md
