#set document(
  title: "Search Algorithms",
  author: "AI Education",
)

#set page(
  margin: (left: 1.5in, right: 1.2in, top: 1in, bottom: 1in),
  footer: context [
    #set text(size: 10pt, fill: gray)
    #h(1fr)
    #counter(page).display("– 1 –")
  ],
)

#set text(font: "Times New Roman", size: 9pt, lang: "en")
#set heading(numbering: "1.1.1")

// Color definitions
#let aima-purple = rgb("#9B8BB0")
#let aima-maroon = rgb("#933333")
#let aima-blue = rgb("#0077BE")
#let aima-gray = rgb("#E8E8E8")

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

// Main document
#chapter("3", "Solving Problems by Searching")

// Chapter introduction box (AIMA style)
#block(
  fill: aima-gray,
  inset: 12pt,
  radius: 0pt,
  width: 100%,
)[
  #set text(size: 10pt, style: "italic", fill: black)
  In which we examine the task of solving problems by searching through possible solutions. We cover uninformed and informed search strategies, emphasizing practical techniques for finding optimal paths in complex problem spaces.
]

#v(0.8em)

== Problem-Solving Agents

#glossary("Problem formulation")

An agent that solves a problem through a sequence of actions must first formulate
a goal based on its performance measure, and then use this to formulate a problem.
A problem consists of:

1. *Initial state*: starting configuration
2. *Actions*: possible transitions
3. *Goal test*: determines if goal reached
4. *Path cost*: sum of step costs

=== Example: Vacuum World

#glossary("State space")

Consider a simple vacuum cleaner agent. The state space is finite and discrete.
The agent perceives which square it is in and whether there is dirt present. It
can move left, right, or suck.

#figure(
  rect(width: 3cm, height: 1.5cm, stroke: 1pt)[
    #grid(
      columns: (1fr, 1fr),
      rows: (1fr,),
      rect(width: 100%, height: 100%, stroke: 0.5pt)[A],
      rect(width: 100%, height: 100%, stroke: 0.5pt)[B],
    )
  ],
  caption: [The vacuum world. Each square can contain dirt (D) or not.],
)

== Uninformed Search Strategies

#glossary("Breadth-first search")

*Breadth-first search* (BFS) expands the shallowest nodes first. It is complete
and optimal for uniform costs, but requires exponential space.

#algorithm("BREADTH-FIRST-SEARCH", [
  *function* BFS(problem) *returns* solution or failure \
  #h(1em) frontier ← a FIFO queue with problem.INITIAL-STATE \
  #h(1em) explored ← an empty set \
  #h(1em) *loop* *do* \
  #h(2em) *if* EMPTY?(frontier) *then return* failure \
  #h(2em) node ← POP(frontier) \
  #h(2em) *if* problem.GOAL-TEST(node.STATE) *then return* node \
  #h(2em) explored ← explored ∪ \{node.STATE\} \
  #h(2em) *for each* action *in* problem.ACTIONS(node.STATE) *do* \
  #h(3em) child ← CHILD-NODE(problem, node, action) \
  #h(3em) *if* child.STATE ∉ explored and child.STATE ∉ frontier *then* \
  #h(4em) frontier ← INSERT(child, frontier)
])

=== Complexity Analysis

Breadth-first search has:
- *Time complexity*: $O(b^d)$ where $b$ is branching factor and $d$ is depth
- *Space complexity*: $O(b^d)$ for storing nodes in frontier
- *Optimality*: Yes, for unit costs

The main limitation is memory usage—with $b = 10$ and $d = 5$, we need
111,111 nodes in memory.

== Informed Search Strategies

#glossary("Heuristic function")

*Greedy best-first search* uses a heuristic function $h(n)$ to estimate the cost
of the cheapest path from node $n$ to the goal. It always expands the node with
the smallest $h(n)$ value.

#algorithm("GREEDY-BEST-FIRST-SEARCH", [
  *function* GREEDY(problem, h) *returns* solution or failure \
  #h(1em) frontier ← a priority queue ordered by $h(n)$ \
  #h(1em) *loop* *do* \
  #h(2em) *if* EMPTY?(frontier) *then return* failure \
  #h(2em) node ← POP(frontier) \
  #h(2em) *if* problem.GOAL-TEST(node.STATE) *then return* node \
  #h(2em) *for each* child *of* node *do* \
  #h(3em) frontier ← INSERT(child, frontier)
])

Key properties:
- _Not_ optimal (finds suboptimal solutions)
- Often faster than uninformed search
- Depends critically on heuristic quality

#pagebreak()

== Summary

Informed search strategies exploit domain knowledge through heuristic functions.
The $A^*$ algorithm combines actual cost $g(n)$ with estimated remaining cost
$h(n)$ to find optimal solutions efficiently:

$$f(n) = g(n) + h(n)$$

This is optimal and complete when the heuristic is admissible ($h(n) <= h^*(n)$ for all $n$).
