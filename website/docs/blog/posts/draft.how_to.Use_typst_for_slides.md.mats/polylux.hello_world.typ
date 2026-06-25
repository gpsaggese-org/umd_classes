// Polylux-style slides (simulated with raw Typst)
// This demonstrates the Polylux approach: minimal, flexible layouts with manual customization

#set page(paper: "presentation-16-9", margin: 1.5cm)
#set text(font: "DejaVu Sans", size: 20pt)

// Minimal slide macro (Polylux philosophy: flexible, not opinionated)
#let slide(body) = {
  body
  pagebreak()
}

#let title-slide(title, subtitle: none, author: none) = {
  slide[
    #align(center + horizon)[
      #text(size: 48pt, weight: "bold")[#title]
      #if subtitle != none {
        [#v(0.5em)]
        [#text(size: 28pt, fill: gray)[#subtitle]]
      }
      #if author != none {
        [#v(2em)]
        [#text(size: 20pt)[#author]]
      }
    ]
  ]
}

// Alternative slide with heading
#let slide-with-title(title, body) = {
  slide[
    #text(size: 36pt, weight: "bold")[#title]
    #line(length: 100%, stroke: 1.5pt)
    #v(0.5em)
    #body
  ]
}

// Content starts here

#title-slide("Polylux Presentation", subtitle: "A Typst Framework with Flexible Layouts", author: "Your Name")

#slide-with-title("What is Polylux?")[
  - Lightweight, minimal presentation framework
  - Emphasizes *flexibility* over predefined themes
  - Clean, readable syntax
  - Good for code-heavy presentations
  - DIY component approach

  #v(1em)

  *Key principle:* You build what you need, nothing more.
]

#slide-with-title("Example: Simple Lists")[
  Benefits of Polylux:
  + Minimal dependencies
  + Learn Typst syntax naturally
  + Full control over styling
  + Great for academic presentations
  + Easy to customize further

  #v(1em)

  Code blocks integrate seamlessly:
  ```python
  def polylux_demo():
      return "minimalist slides"
  ```
]

#slide[
  #grid(
    columns: (1fr, 1fr),
    gutter: 1em,
    [
      === Left Section

      #box(
        width: 100%,
        fill: rgb("#f0f0f0"),
        inset: 10pt,
        radius: 5pt,
      )[
        *Highlighted Point*

        This is a colored box, manually styled with Typst's built-in layout functions.
      ]
    ],
    [
      === Right Section

      Comparison table:

      #table(
        columns: 2,
        inset: 8pt,
        [*Static*], [*Dynamic*],
        [Themes], [Customization],
        [Fixed], [Flexible],
      )
    ]
  )
]

#slide-with-title("The Polylux Advantage")[
  #box(
    width: 100%,
    fill: rgb("#e8f4ff"),
    inset: 12pt,
    radius: 4pt,
  )[
    *Why choose Polylux?*
    - No heavy theming overhead
    - Direct control via Typst
    - Perfect for custom designs
    - Minimal learning curve if you know Typst
  ]

  #v(1em)

  When you need:
  - Unique slide layouts
  - Code-first presentations
  - Lightweight PDF output
  - Control over every pixel
]

#slide[
  #align(center + horizon)[
    #text(size: 44pt, weight: "bold")[Questions?]
    #v(1em)
    #text(size: 20pt, fill: gray)[Thank you for watching]
  ]
]
