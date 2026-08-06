// Touying-style slides (simulated with raw Typst)
// This demonstrates the Touying approach: structured slide macros with built-in styling

#set page(paper: "presentation-16-9", margin: 2cm)
#set text(font: "DejaVu Sans", size: 24pt)

// Slide macro inspired by Touying's approach
#let slide(title: none, body) = {
  if title != none {
    text(size: 32pt, weight: "bold", fill: rgb("#003366"))[#title]
    line(length: 100%, stroke: 2pt + rgb("#0066cc"))
    v(0.5em)
  }
  body
  pagebreak()
}

#let title-slide(title, subtitle) = {
  align(center + horizon)[
    text(size: 48pt, weight: "bold", fill: rgb("#003366"))[#title]
    v(0.5em)
    text(size: 28pt, fill: rgb("#666666"))[#subtitle]
  ]
  pagebreak()
}

// Content starts here

#title-slide("Touying Presentation", "A Typst Slide Framework")

#slide(title: "Key Features")[
  - Built-in themes and styling
  - Automatic slide layouts
  - Easy customization with macros
  - Support for animations (in real Touying)
  - Multiple themes: default, simple, aqua

  #v(1em)
  *Example syntax:*
  ```typst
  #slide(title: [My Slide])[
    Your content here
  ]
  ```
]

#slide(title: "Two-Column Layout")[
  #grid(
    columns: (1fr, 1fr),
    gutter: 1.5em,
    [
      *Left Column*

      - Point 1
      - Point 2
      - Point 3

      Declarative syntax makes structure clear.
    ],
    [
      *Right Column*

      Code example:
      ```rust
      fn main() {
        println!("Hello");
      }
      ```

      Output:
      ```
      Hello
      ```
    ]
  )
]

#slide(title: "Tables in Touying")[
  #table(
    columns: (1fr, 1fr, 1fr),
    inset: 10pt,
    align: (col, row) =>
      if row == 0 { center } else { left },
    [*Feature*], [*Touying*], [*Polylux*],
    [Themes], [Many], [Minimal],
    [Complexity], [Medium], [Low],
    [Built-in Effects], [Yes], [Basic],
  )
]

#slide(title: "Focus/Emphasis")[
  #align(center + horizon)[
    #text(size: 44pt, weight: "bold", fill: rgb("#0066cc"))[
      Thank You!
    ]

    #v(1em)
    #text(size: 28pt, fill: gray)[Questions?]
  ]
]
