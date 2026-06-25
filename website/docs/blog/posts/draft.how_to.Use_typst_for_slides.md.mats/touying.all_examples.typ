// Touying-Style Example Slides
// Demonstrates all slide styles from slides.rules.md

#set page(paper: "presentation-16-9", margin: 1.5cm)
#set text(size: 22pt)

#let slide-title(t) = {
  text(size: 28pt, weight: "bold", fill: rgb("#003366"))[#t]
  line(length: 100%, stroke: 2pt + rgb("#0066cc"))
  v(0.5em)
}

#let slide-end = pagebreak()

#let title-slide(t, s) = {
  align(center + horizon)[
    text(size: 48pt, weight: "bold", fill: rgb("#003366"))[#t]
    v(0.5em)
    text(size: 28pt, fill: rgb("#666666"))[#s]
  ]
  pagebreak()
}

// ============================================================================
// TITLE SLIDE
// ============================================================================

#title-slide("Lecture Slides: Complete Examples", "Touying Style with All Slide Patterns")

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
    *Diagram:*

    A simple network:
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
)

#slide-end

// ============================================================================
// 3. DEFINITION SLIDE
// ============================================================================

#slide-title("3. Definition: Machine Learning")

*Definition*: Machine learning is building machines to do useful things without being explicitly programmed.
- Learns from experience
- Improves with data
- Performs tasks without hardcoded rules

*Formally*: A computer program is said to learn from experience $E$ with respect to some task $T$ and some performance measure $P$, if $P(T)$ improves with experience $E$ (Mitchell, 1998)

*Example*: Computer vision system that learns to recognize cats from labeled image datasets without being programmed with cat detection rules.

#slide-end

// ============================================================================
// 4. ALGORITHM SLIDE
// ============================================================================

#slide-title("4. Algorithm: Forward Pass")

*Input*: Network weights $W$, input data $x$, biases $b$

*Output*: Predicted output $hat(y)$

*Steps*:
1. Initialize activation: $a^((0)) = x$
2. For each layer $l = 1, \ldots, L$:
   - Compute: $z^((l)) = W^((l)) a^((l-1)) + b^((l))$
   - Apply activation: $a^((l)) = sigma(z^((l)))$
3. Output: $hat(y) = a^((L))$

*Complexity*:
- Time: $O(n \cdot m)$ where $n$ = input size, $m$ = hidden units
- Space: $O(m)$ for intermediate activations

#slide-end

// ============================================================================
// 5. PROS/CONS SLIDE
// ============================================================================

#slide-title("5. Pros and Cons: Deep Learning")

*Pros*
- Feature Learning: Automatically discovers useful representations
- Scalability: Performs well with large datasets
- Flexibility: Adaptable to many problem domains

*Cons*
- Computational Cost: Requires significant GPU resources
- Interpretability: Difficult to understand internal decisions
- Data Requirements: Typically needs large labeled datasets

#slide-end

// ============================================================================
// 6. QUESTION SLIDE
// ============================================================================

#slide-title("6. Question: Which Approach?")

*Question*: How do we handle uncertainty when making decisions?

Consider these options:
- *Option A*: Use deterministic rules and hope they always work
- *Option B*: Model uncertainty as probability distributions
- *Option C*: Make decisions based on majority votes from experts

*Answer*: Option B because:
- Probability provides a principled framework
- Accounts for partial observability and non-determinism
- Integrates with decision theory for optimal choices

*Key Takeaway*: Probabilistic reasoning is fundamental to robust AI.

#slide-end

// ============================================================================
// 7. THEOREM / PROOF SLIDE
// ============================================================================

#slide-title("7. Theorem: Bayes' Rule")

*Theorem*: Bayes' rule provides a way to compute conditional probability in reverse.

$$P(H | E) = frac(P(E | H) P(H), P(E))$$

*Proof*
1. *Joint Probability Chain Rule*
   $$P(H, E) = P(H) P(E | H)$$

2. *Alternative Factorization*
   $$P(H, E) = P(E) P(H | E)$$

3. *Equate and Solve for Posterior*
   $$P(H) P(E | H) = P(E) P(H | E)$$
   $$P(H | E) = frac(P(E | H) P(H), P(E))$$

This enables computing beliefs _given_ observations.

#slide-end

// ============================================================================
// 8. WORKED COMPUTATION SLIDE
// ============================================================================

#slide-title("8. Worked Computation: Joint Probability")

*Problem*: Compute $P(R, S, W)$ given the network:
- Rain causes WetGrass
- Sprinkler causes WetGrass

*Solution*: Express as factored product:

$$P(R, S, W) = P(R) times P(S) times P(W | R, S)$$

By conditional independence: $R perp S$
- $P(R) = 0.2$
- $P(S) = 0.1$
- $P(W | R, S) = 0.99$

Final: $P(R, S, W) = 0.2 times 0.1 times 0.99 = 0.0198$

#slide-end

// ============================================================================
// 9. ANNOTATED-DIAGRAM SLIDE
// ============================================================================

#slide-title("9. Markov Blanket Example: Medical Diagnosis")

Consider diagnosing a patient's disease based on symptoms and test results.

*Diagram Roles*:

*Target Node* (Disease): The variable we want to infer

*Parent Nodes* (observable causes):
- Genetic — hereditary risk factors
- Lifestyle — diet, exercise, stress

*Children Nodes* (observable effects):
- Symptom — patient-reported signs
- TestResult — lab or imaging results

*Co-parents (Spouses)*:
- Age — confounding factor affecting both causes and effects

*Key Insight*: Knowing only the parents, children, and co-parents is sufficient to infer the target; other variables become conditionally independent.

#slide-end

// ============================================================================
// 10. NODE-COLORING LEGEND SLIDE
// ============================================================================

#slide-title("10. Graph Structure: Variable Categories")

*Legend*:
- *Blue nodes*: Observable inputs (weather, actions)
- *Red nodes*: Hidden / latent variables (unobserved states)
- *Green nodes*: Target / output variables (predictions)

Network structure:
```
┌──────────┐
│ Weather  │  (blue: observable)
└────┬─────┘
     │
     ▼
┌──────────────┐
│ Sprinkler    │  (red: hidden decision)
└────┬─────────┘
     │
     ▼
┌──────────────┐
│ WetGrass     │  (green: target)
└──────────────┘
```

Color coding makes roles immediately clear.

#slide-end

// ============================================================================
// 11. MULTI-SLIDE CONTINUATION (Part 1/2)
// ============================================================================

#slide-title("11. Conditional Independence (1/2)")

*Definition*: Random variables X and Y are conditionally independent given Z (written $X perp Y | Z$) if:

$$P(X | Y, Z) = P(X | Z)$$

*In English*: Knowing Y gives no additional information about X once we know Z.

*Intuition*: Z "explains away" the dependence between X and Y.

Example: In the sprinkler network:
- Rain and Sprinkler are _independent_ (neither causes the other)
- Given WetGrass = true, they become _dependent_: observing rain makes sprinkler less likely

#slide-end

// ============================================================================
// 12. MULTI-SLIDE CONTINUATION (Part 2/2)
// ============================================================================

#slide-title("11. Conditional Independence (2/2)")

*Why it matters*: Conditional independence structure determines how information flows in graphical models.

*In Bayesian networks*:
- $X perp Y | "Parents"(X)$ always holds
- Enables factorization: $P(X | Y, Z) = P(X | Z)$ when Z is sufficient

*Applications*:
- Simplifies inference: fewer variables to consider
- Enables parallelization: independent subgraphs compute separately
- Improves learning: reduces parameters needed to fit the model

*Key Takeaway*: Graph structure encodes independence assumptions; exploit them for efficiency.

#slide-end

// ============================================================================
// CLOSING SLIDE
// ============================================================================

#slide-title("Summary")

You've seen all major slide patterns:
1. Symmetric and asymmetric side-by-side layouts
2. Definition slides with formal and informal description
3. Algorithm specifications with complexity analysis
4. Pros/cons tradeoff evaluation
5. Question-driven engagement
6. Formal proofs with step-by-step derivation
7. Worked computations with numeric examples
8. Annotated diagrams with role colors
9. Legend-based variable categorization
10. Multi-slide continuations

All follow pedagogical best practices: intuition before formalism, concrete examples, progressive complexity, and clear visual hierarchy.
