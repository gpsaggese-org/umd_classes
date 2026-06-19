// AIMA-style formatting template
// Reusable style configuration for textbook chapters
// Import this file in your document with: #include "aima_style.typ"

// Color definitions (AIMA palette)
#let aima-purple = rgb("#9B8BB0")
#let aima-maroon = rgb("#933333")
#let aima-blue = rgb("#0077BE")
#let aima-gray = rgb("#E8E8E8")

// Page and text configuration
#set page(
  margin: (left: 1.5in, right: 1.2in, top: 1in, bottom: 1in),
  footer: context [
    #set text(size: 10pt, fill: gray)
    #h(1fr)
    #counter(page).display("– 1 –")
  ],
)

#set text(font: "Times New Roman", size: 9pt, lang: "en")
#set par(justify: true)
#set heading(numbering: "1.1.1")

// Chapter heading style (AIMA style)
#let chapter(num, title) = {
  pagebreak()

  // Reset heading counter to chapter number
  counter(heading).update((int(num),))

  // Purple header bar with "CHAPTER" label
  block(
    fill: aima-purple,
    width: 100%,
    inset: (x: 12pt, y: 8pt),
  )[
    #set text(size: 14pt, weight: "bold", fill: white)
    CHAPTER
  ]

  v(-0.8em)

  // Chapter number in large purple text, positioned on the right
  box(width: 100%, height: auto)[
    #set text(size: 48pt, weight: "bold", fill: aima-purple)
    #h(1fr)
    #num
  ]

  v(0.3em)

  // Title in burgundy/maroon
  set text(size: 24pt, weight: "bold", fill: aima-maroon)
  [#title]

  v(0.5em)
}

// Configure heading styles
#show heading: it => {
  if it.level == 2 {
    block(spacing: 0.5em)[
      #v(1.2em)
      #set text(size: 11pt, weight: "bold", fill: aima-maroon)
      #if it.numbering != none {
        counter(heading).display(it.numbering)
        h(0.5em)
      }
      #it.body
      #v(-0.5em)
      #line(length: 100%, stroke: 1pt + aima-maroon)
    ]
  } else if it.level == 3 {
    block(spacing: 0.8em)[
      #set text(size: 10pt, weight: "bold", fill: aima-maroon)
      #if it.numbering != none {
        counter(heading).display(it.numbering)
        h(0.5em)
      }
      #it.body
    ]
  } else {
    it
  }
}

// Margin glossary term
#let glossary(term) = {
  place(
    left,
    dx: -1.4in,
    dy: 0em,
  )[
    #set text(size: 9pt, fill: aima-blue, weight: "regular")
    #term
  ]
}

// Algorithm box (AIMA style)
#let algorithm(name, content) = {
  set text(size: 8pt, font: "Courier New")
  block(
    fill: rgb("#f5f5f5"),
    inset: 12pt,
    radius: 4pt,
    breakable: false,
  )[
    #set text(weight: "bold", size: 8.5pt)
    Figure. #name
    #set text(weight: "regular", size: 8pt)
    #v(0.3em)
    #content
  ]
}

// Chapter introduction box (AIMA style)
#let chapter-intro(content) = {
  block(
    fill: aima-gray,
    inset: 12pt,
    radius: 0pt,
    width: 100%,
  )[
    #set text(size: 10pt, style: "italic", fill: black)
    #content
  ]
}
