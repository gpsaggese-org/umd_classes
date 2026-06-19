// Polylux-Style Example Slides
// Demonstrates all slide styles from slides.rules.md
// Philosophy: minimal framework, flexible layouts, DIY components

#set page(paper: "presentation-16-9", margin: 1.2cm)
#set text(size: 20pt)

// ============================================================================
// MINIMAL SLIDE MACROS (Polylux philosophy)
// ============================================================================

#let slide-title(t) = {
  text(size: 32pt, weight: "bold", fill: rgb("#003366"))[#t]
  line(length: 100%, stroke: 1.5pt + rgb("#0066cc"))
  v(0.5em)
}

#let slide-end = pagebreak()

#let title-slide(t, s, a) = {
  align(center + horizon)[
    text(size: 44pt, weight: "bold", fill: rgb("#003366"))[#t]
    v(0.8em)
    text(size: 26pt, fill: rgb("#555555"))[#s]
    v(2em)
    text(size: 18pt, fill: gray)[#a]
  ]
  pagebreak()
}

#let colored-box(label, color, content) = {
  box(
    width: 100%,
    fill: color,
    inset: 12pt,
    radius: 4pt,
  )[
    *#label*
    #content
  ]
}

// ============================================================================
// TITLE SLIDE
// ============================================================================

#title-slide(
  "Lecture Slides: Complete Examples",
  "Polylux Style with All Slide Patterns",
  "Demonstrating Minimal, Flexible Layouts"
)

// ============================================================================
// 1. SIDE-BY-SIDE CONTENT: SYMMETRIC
// ============================================================================

#slide-title("1. Side-by-Side: Symmetric Layout")

#grid(
  columns: (1fr, 1fr),
  gutter: 1.5em,
  [
    *Left Heading*
    - Point 1: Symmetric layout with equal columns
    - Point 2: Both sides have equal weight
    - Point 3: Good for comparisons
  ],
  [
    *Right Heading*
    - Point 1: Same formatting on both sides
    - Point 2: Balanced visual appearance
    - Point 3: Audience reads left then right
  ]
)

#slide-end

// ============================================================================
// 2. SIDE-BY-SIDE CONTENT: ASYMMETRIC
// ============================================================================

#slide-title("2. Side-by-Side: Asymmetric Layout")

#grid(
  columns: (1.8fr, 1fr),
  gutter: 1.5em,
  [
    - Main content with extensive text explanation
    - Multiple bullet points detailing the concept
    - Detailed explanation of how the system works
    - This side carries the narrative weight
    - Additional context and setup for the diagram
  ],
  [
    #align(center)[
      *Diagram*

      Simple network:
      ```
      ┌─────┐
      │  X  │
      └──┬──┘
         │
         ▼
      ┌─────┐
      │  Y  │
      └─────┘
      ```
    ]
  ]
)

#slide-end

// ============================================================================
// 3. DEFINITION SLIDE
// ============================================================================

#slide-title("3. Definition: Machine Learning")

#colored-box("Definition", rgb("#e3f2fd"))[
  Machine learning is building machines to do useful things without being explicitly programmed.
  - Learns from experience
  - Improves with data
  - Performs tasks without hardcoded rules
]

#v(0.8em)

*Formally*: A computer program is said to learn from experience $E$ with respect to some task $T$ and some performance measure $P$, if $P(T)$ improves with experience $E$ (Mitchell, 1998)

#v(0.8em)

*Example*: Computer vision system that learns to recognize cats from labeled image datasets without being programmed with cat detection rules.

#slide-end

// ============================================================================
// 4. ALGORITHM SLIDE
// ============================================================================

#slide-title("4. Algorithm: Forward Pass")

#colored-box("Input", rgb("#fff3e0"))[
  Network weights $W$, input data $x$, biases $b$
]

#v(0.6em)

#colored-box("Output", rgb("#f3e5f5"))[
  Predicted output $hat(y)$
]

#v(0.6em)

*Steps*:
1. Initialize activation: $a^((0)) = x$
2. For each layer $l = 1, \ldots, L$:
   - Compute: $z^((l)) = W^((l)) a^((l-1)) + b^((l))$
   - Apply activation: $a^((l)) = sigma(z^((l)))$
3. Output: $hat(y) = a^((L))$

#v(0.6em)

#table(
  columns: (1fr, 1.5fr),
  inset: 8pt,
  align: (left, left),
  [*Metric*], [*Complexity*],
  [Time], [$O(n \cdot m)$],
  [Space], [$O(m)$],
)

#slide-end

// ============================================================================
// 5. PROS/CONS SLIDE
// ============================================================================

#slide-title("5. Pros and Cons: Deep Learning")

#grid(
  columns: (1fr, 1fr),
  gutter: 1.5em,
  [
    #colored-box("Pros", rgb("#e8f5e9"))[
      - Feature Learning: Auto-discover representations
      - Scalability: Works well with large datasets
      - Flexibility: Adaptable to many domains
    ]
  ],
  [
    #colored-box("Cons", rgb("#ffebee"))[
      - Computational Cost: Needs GPU resources
      - Interpretability: Hard to understand decisions
      - Data Requirements: Needs large labeled sets
    ]
  ]
)

#slide-end

// ============================================================================
// 6. QUESTION SLIDE
// ============================================================================

#slide-title("6. Question: Which Approach?")

*Question*: How do we handle uncertainty when making decisions?

#v(0.8em)

#table(
  columns: (auto, 1fr),
  inset: 10pt,
  align: (left, left),
  [*Option A*], [Use deterministic rules and hope they always work],
  [*Option B*], [Model uncertainty as probability distributions],
  [*Option C*], [Make decisions based on majority votes from experts],
)

#v(0.8em)

#colored-box("Answer", rgb("#e1f5fe"))[
  Option B because:
  - Probability provides a principled framework
  - Accounts for partial observability and non-determinism
  - Integrates with decision theory for optimal choices
]

#v(0.6em)

*Key Takeaway*: Probabilistic reasoning is fundamental to robust AI.

#slide-end

// ============================================================================
// 7. THEOREM / PROOF SLIDE
// ============================================================================

#slide-title("7. Theorem: Bayes' Rule")

#colored-box("Theorem", rgb("#f3e5f5"))[
  Bayes' rule provides a way to compute conditional probability in reverse.

  $$P(H | E) = frac(P(E | H) P(H), P(E))$$
]

#v(0.8em)

*Proof Steps*:

1. *Joint Probability Chain Rule*
   $$P(H, E) = P(H) P(E | H)$$

2. *Alternative Factorization*
   $$P(H, E) = P(E) P(H | E)$$

3. *Equate and Solve for Posterior*
   $$P(H) P(E | H) = P(E) P(H | E)$$
   $$therefore quad P(H | E) = frac(P(E | H) P(H), P(E))$$

This enables computing beliefs _given_ observations.

#slide-end

// ============================================================================
// 8. WORKED COMPUTATION SLIDE
// ============================================================================

#slide-title("8. Worked Computation: Joint Probability")

#grid(
  columns: (1.6fr, 1fr),
  gutter: 1.2em,
  [
    *Problem*: Compute $P(R, S, W)$

    Given network:
    - Rain causes WetGrass
    - Sprinkler causes WetGrass
    - $R perp S$ (independent)

    #v(0.8em)

    *Solution*: Express as factored product
    $$P(R, S, W) = P(R) times P(S) times P(W | R, S)$$

    Substitute values:
    $$= 0.2 times 0.1 times 0.99 = 0.0198$$
  ],
  [
    #align(center)[
      *Network*

      ```
      ┌──────────┐
      │  Rain    │
      └──────┬───┘
             │
      ┌──────┴──────────┐
      │                 │
      ▼                 ▼
      ┌──────────┐  ┌──────────┐
      │Sprinkler │  │WetGrass  │
      └──────────┘  └──────────┘
      ```
    ]
  ]
)

#slide-end

// ============================================================================
// 9. ANNOTATED-DIAGRAM SLIDE
// ============================================================================

#slide-title("9. Markov Blanket: Medical Diagnosis")

Consider diagnosing a patient's disease based on symptoms and test results.

#v(0.8em)

#table(
  columns: (auto, 1fr),
  inset: 10pt,
  align: (left, left),
  [*Role*], [*Variables*],
  [*Target Node*], [Disease — what we infer],
  [*Parents*], [Genetic, Lifestyle — causes],
  [*Children*], [Symptom, TestResult — effects],
  [*Co-parents*], [Age — confounding factor],
)

#v(0.8em)

#colored-box("Key Insight", rgb("#e0f2f1"))[
  Knowing only the parents, children, and co-parents is sufficient to infer the target. Other variables become conditionally independent.
]

#slide-end

// ============================================================================
// 10. NODE-COLORING LEGEND SLIDE
// ============================================================================

#slide-title("10. Graph Structure: Variable Categories")

*Legend*:

#table(
  columns: (auto, 1fr),
  inset: 10pt,
  align: (left, left),
  [*Blue nodes*], [Observable inputs (weather, actions)],
  [*Red nodes*], [Hidden / latent variables (unobserved)],
  [*Green nodes*], [Target / output variables (predictions)],
)

#v(1em)

Network structure:
```
┌──────────────┐
│ Weather      │ ◄── blue: observable
└────┬─────────┘
     │
     ▼
┌──────────────┐
│ Sprinkler    │ ◄── red: hidden decision
└────┬─────────┘
     │
     ▼
┌──────────────┐
│ WetGrass     │ ◄── green: target
└──────────────┘
```

Color coding makes roles immediately clear.

#slide-end

// ============================================================================
// 11. MULTI-SLIDE CONTINUATION (1/2)
// ============================================================================

#slide-title("11. Conditional Independence (1/2)")

#colored-box("Definition", rgb("#fce4ec"))[
  Random variables X and Y are conditionally independent given Z (written $X perp Y | Z$) if:
  $$P(X | Y, Z) = P(X | Z)$$
]

#v(0.8em)

*In English*: Knowing Y gives no additional information about X once we know Z.

#v(0.6em)

*Intuition*: Z "explains away" the dependence between X and Y.

#v(0.6em)

*Example*: In the sprinkler network:
- Rain and Sprinkler are _independent_ (neither causes the other)
- Given WetGrass = true, they become _dependent_: observing rain makes sprinkler less likely

#slide-end

// ============================================================================
// 12. MULTI-SLIDE CONTINUATION (2/2)
// ============================================================================

#slide-title("11. Conditional Independence (2/2)")

*Why it matters*: Conditional independence structure determines how information flows in graphical models.

#v(0.8em)

#table(
  columns: (1.2fr, 1.8fr),
  inset: 10pt,
  align: (left, left),
  [*In Bayesian Networks*], [*Effect*],
  [$X perp Y | "Parents"(X)$], [Always holds; enables factorization],
  [Graph structure], [Encodes independence assumptions],
)

#v(0.8em)

*Applications*:
- Simplifies inference: fewer variables to consider
- Enables parallelization: independent subgraphs compute separately
- Improves learning: reduces parameters needed to fit the model

#v(0.8em)

#colored-box("Key Takeaway", rgb("#e0f2f1"))[
  Graph structure encodes independence assumptions; exploit them for efficiency.
]

#slide-end

// ============================================================================
// CLOSING SLIDE
// ============================================================================

#slide-title("Summary")

You've seen all major slide patterns:

#table(
  columns: (auto, 1fr),
  inset: 8pt,
  align: (left, left),
  [1.], [Symmetric and asymmetric side-by-side layouts],
  [2.], [Definition slides with formal and informal description],
  [3.], [Algorithm specifications with complexity analysis],
  [4.], [Pros/cons tradeoff evaluation],
  [5.], [Question-driven engagement],
  [6.], [Formal proofs with step-by-step derivation],
  [7.], [Worked computations with numeric examples],
  [8.], [Annotated diagrams with role annotations],
  [9.], [Legend-based variable categorization],
  [10.], [Multi-slide continuations],
)

#v(0.8em)

All follow pedagogical best practices: intuition before formalism, concrete examples, progressive complexity, and clear visual hierarchy.
