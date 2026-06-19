// AIMA-style formatting template
// Reusable style configuration for textbook chapters
// Import this file in your document with: #include "aima_style.typ"

// Color definitions (AIMA palette)
#let aima-purple = rgb("#8B7BA8")
#let aima-maroon = rgb("#8B3A62")
#let aima-blue = rgb("#0066CC")
#let aima-gray = rgb("#F0F0F0")

// Page and text configuration
#set page(
  margin: (left: 1.2in, right: 1.2in, top: 0.85in, bottom: 0.85in),
  header: context {
    let page-num = counter(page).get().first()
    if page-num > 2 [
      #set text(size: 8.5pt, fill: black)
      #if page-num == 3 {
        [Chapter 1 Introduction]
      } else {
        [Section 1.1 What Is AI?]
      }
      #h(1fr)
      #page-num
    ]
  },
)

#set text(font: "Times New Roman", size: 9.5pt, lang: "en")
#set par(justify: true, leading: 0.6em)
#set heading(numbering: "1.1.1")

// Chapter heading style (AIMA style)
#let chapter(num, title) = {
  pagebreak()

  // Reset heading counter to chapter number
  counter(heading).update((int(num),))

  // Purple header bar with "CHAPTER" label and number
  block(
    fill: aima-purple,
    width: 100%,
    inset: (x: 12pt, y: 10pt),
  )[
    #set text(size: 13pt, weight: "bold", fill: white)
    CHAPTER
    #h(1fr)
    #set text(size: 32pt, weight: "bold")
    #num
  ]

  v(0.5em)

  // Title in burgundy/maroon
  set text(size: 26pt, weight: "bold", fill: aima-maroon)
  [#title]

  v(0.8em)
}

// Configure heading styles
#show heading: it => {
  if it.level == 2 {
    counter(heading).step(level: it.level)
    let nums = counter(heading).get()
    let num-text = if nums.len() > 1 {
      str(nums.at(0)) + "." + str(nums.at(1)) + " "
    } else {
      ""
    }
    block(spacing: 0.5em)[
      #v(0.8em)
      #set text(size: 11pt, weight: "bold", fill: aima-maroon)
      #num-text
      #it.body
      #line(length: 100%, stroke: 1.2pt + aima-maroon)
      #v(0.4em)
    ]
  } else if it.level == 3 {
    counter(heading).step(level: it.level)
    let nums = counter(heading).get()
    let num-text = if nums.len() > 2 {
      str(nums.at(0)) + "." + str(nums.at(1)) + "." + str(nums.at(2)) + " "
    } else {
      ""
    }
    block(spacing: 0.6em)[
      #v(0.6em)
      #set text(size: 10pt, weight: "bold", fill: aima-maroon)
      #num-text
      #it.body
      #v(0.3em)
    ]
  } else {
    it
  }
}

// Margin glossary term
#let glossary(term) = {
  place(
    right,
    dx: 0.3in,
    dy: 0em,
  )[
    #set text(size: 8.5pt, fill: aima-blue, weight: "regular")
    #term
  ]
}

// Algorithm box (AIMA style)
#let algorithm(name, content) = {
  block(
    fill: rgb("#F5F5F5"),
    inset: 10pt,
    radius: 0pt,
    breakable: false,
    stroke: 0.5pt + rgb("#E0E0E0"),
  )[
    #set text(weight: "bold", size: 8pt, font: "Courier New")
    Figure. #name
    #v(0.2em)
    #set text(weight: "regular", size: 7.8pt, font: "Courier New", fill: black)
    #content
  ]
}

// Chapter introduction box (AIMA style)
#let chapter-intro(content) = {
  block(
    fill: aima-gray,
    inset: 11pt,
    radius: 0pt,
    width: 100%,
    stroke: 0.5pt + rgb("#CCCCCC"),
  )[
    #set text(size: 9.5pt, style: "italic", fill: black)
    #content
  ]
}
