# Jupyter Notebook Outline: Causal Discovery

## Overview
This notebook teaches causal discovery through interactive visualizations and
incremental examples, building intuition about how algorithms infer causal
structure from observational data

## Cell 1: the Core Problem
**Purpose**

- Understand why causal direction matters for decision-making
- See the gap between correlation (what ML optimizes) and causation (what we
  need for intervention)
- Build motivation for learning causal discovery

**Display**

- Two scatter plots side-by-side showing identical correlation patterns
- Both show $X$ and $Y$ perfectly correlated: $r = 0.95$
- Left plot labeled: "Chain: $X \to Y$ (if we change $X$, $Y$ changes)"
- Right plot labeled: "Reverse: $Y \to X$ (changing $X$ has no effect)"
- Summary box with decision scenarios
  - Scenario 1: "You can only intervene on one variable. Which would help?"
  - Scenario 2: "Both models fit the data equally well. How do you choose?"

**Interactive widgets**

- Toggle between observational and interventional outcomes
  - When "observational": both DAGs produce identical correlation
  - When "interventional": left plot shows change in $Y$ when $X$ intervenes;
    right plot shows no change
- Slider: correlation strength ($r = 0.3$ to $r = 0.99$)
- Seed: randomization for data generation

**Key insights**

- Prediction and causation require different thinking
- Correlation alone cannot determine direction
- Need either domain knowledge, interventions, or structural assumptions

**Comment box**

- Highlight the essential problem: "No amount of observational data alone
  distinguishes these structures"

## Cell 2: Markov Equivalence---Three Indistinguishable Structures
**Purpose**

- Show the fundamental limit: different DAGs encode identical conditional
  independencies
- Build intuition for why the best observational algorithms return equivalence
  classes, not unique DAGs
- Introduce the CPDAG (Completed Partially Directed Acyclic Graph) as the
  solution

**Display**

- Three DAGs in a row
  - **Chain 1**: $X \to Y \to Z$
  - **Chain 2**: $Z \to Y \to X$
  - **Common cause**: $X \leftarrow Y \rightarrow Z$
- Below each: list implied conditional independencies
  - All three imply: $X \perp Z \mid Y$ (and only that)
  - Distributions are mathematically identical
- Third visualization: CPDAG representing the equivalence class
  - Shows the skeleton: $X - Y - Z$ (undirected edges)
  - Marks which edges can be oriented consistently

**Interactive widgets**

- Generate samples from each structure and show they are statistically
  indistinguishable
  - Slider: sample size ($N = 50$ to $N = 5000$)
  - Histogram of $X$ vs. $Z$ correlation (identical across all three)
  - Histogram of $X$ vs. $Z$ given $Y$ (near-zero for all three)
- Toggle: "Show conditional independencies tested" to reveal which CI tests
  matter

**Key insights**

- Observational data can only recover conditional independence structure
- Edge directions in chains are fundamentally ambiguous
- CPDAG: the honest answer about what can be learned from observational data

**Comment box**

- "This is why observational discovery outputs equivalence classes. Without
  interventions or functional assumptions, multiple DAGs are equally valid."

## Cell 3: When Direction Matters: Causal Effects Via Intervention
**Purpose**

- Show concretely why edge direction determines causal effect
- Build intuition for interventional thinking (do-operator)
- Motivate why identifiability of structure is crucial for policy

**Display**

- Side-by-side counterfactual outcomes for each of the three structures from
  Cell 2
- Scenario: intervene on $X$ (set it to high vs. low) and observe effect on $Z$
  - **Chain 1** ($X \to Y \to Z$): large effect on $Z$
  - **Chain 2** ($Z \to Y \to X$): no effect on $Z$
  - **Common cause** ($Y$ confounds both): no direct effect on $Z$
- Table: Effect size and confidence interval for each structure
- Visualization of how effect propagates (or not) through the DAG

**Interactive widgets**

- Slider: intervention strength (how much to change $X$)
- Slider: sample size for estimating the effect
- Toggle: "Show confounding" to highlight when a hidden confounder explains the
  observation
- Seed: for reproducibility

**Key insights**

- Same observational correlation, wildly different causal effects
- Direction determines whether an intervention is effective
- This is why we cannot simply read causation from correlation

**Comment box**

- "Policy decisions depend critically on DAG structure. Choosing the wrong DAG
  leads to ineffective interventions."

## Cell 4: the PC Algorithm: Learning From Conditional Independence Tests
**Purpose**

- Understand constraint-based discovery: using CI tests to prune edges
- Build intuition for how the PC algorithm works step-by-step
- See the trade-off between power and sample complexity

**Display**

- Animated visualization of the PC algorithm on a 4-5 variable DAG
- Start with fully connected graph
- Step-by-step:
  1. Show first CI test (e.g., $X_1 \perp X_2$?)
  2. If true, remove edge; highlight the "separating set"
  3. Continue through all pairs and conditioning sets
  4. Show the intermediate graph after each decision
  5. Final step: orient v-structures (colliders)
  6. Apply orientation rules to finalize CPDAG
- Panel on right shows:
  - Current step number and CI test being performed
  - P-value from the CI test
  - Separating set (if edge was removed)
  - Visualization of which edges remain

**Interactive widgets**

- Slider: CI test threshold (alpha = 0.001 to 0.2)
  - Lower threshold: stricter CI tests, keep more edges
  - Higher threshold: liberal CI tests, remove more edges
- Dropdown: CI test type
  - Partial correlation (linear)
  - Gaussian $G^2$-test (non-linear Gaussian)
  - Conditional mutual information (non-parametric)
- Play/pause buttons for step-by-step exploration
- Seed: for randomization of test data

**Key insights**

- PC recovers skeleton via CI tests, then orients edges
- Stronger assumptions (e.g., Gaussianity) enable more powerful tests
- False positives/negatives in CI tests propagate to errors in DAG structure

**Comment box**

- "PC is sound in the large-sample limit, but CI tests are underpowered in
  finite samples. Small sample size or weak dependencies can cause edge recovery
  errors."

## Cell 5: Score-Based Search: GES (Greedy Equivalence Search)
**Purpose**

- Introduce score-based discovery: search DAG space to optimize fit
- Show forward and backward search phases of GES
- Build intuition for greedy search in huge DAG space

**Display**

- Left panel: animated DAG evolving during search
  - Starts empty (no edges)
  - Shows which edge is being added/removed at each step
  - Color-codes edges by their contribution to score improvement
  - Displays current score (BIC) below the graph
- Right panel:
  - Line plot of BIC score vs. iteration
  - Annotations showing when forward phase ends and backward phase begins
  - Shows local maxima and the final plateau
- Bottom: table of top-5 candidate edges at each phase

**Interactive widgets**

- Slider: sample size ($N = 50$ to $N = 10000$)
  - BIC score incorporates penalty $\propto \log N$ for complexity
  - Larger $N$ allows more edges
- Slider: prior edge penalty (regularization) to encourage sparsity
- Dropdown: score function
  - BIC (Bayesian Information Criterion)
  - BDeu (Bayesian Dirichlet equivalent uniform)
- Speed slider: animation speed for algorithm steps
- Seed: for data generation

**Key insights**

- Score-based search explores DAG space (combinatorially large) using greedy
  heuristics
- BIC balances likelihood fit with model complexity: more edges must improve fit
  more than their added complexity costs
- Forward-backward search: forward phase finds good edges; backward removes
  edges that add little

**Comment box**

- "GES is guaranteed to recover the true equivalence class in the limit, but
  greedy search can get stuck in local optima. Start from multiple random
  initializations for robustness."

## Cell 6: Non-Gaussian Methods: LiNGAM for Full Identifiability
**Purpose**

- Show how non-Gaussianity breaks symmetry and enables full DAG recovery
- Understand that functional assumptions (beyond CI and scores) can identify
  direction
- Compare LiNGAM output to PC and GES

**Display**

- Top row: three panels showing data clouds for the same three indistinguishable
  structures from Cell 2
  - If data are Gaussian: shapes are identical (same covariance ellipsoid)
  - If data are non-Gaussian: shapes show asymmetry that reveals direction
- Middle row: LiNGAM adjacency matrices
  - Matrix $B$ where $B_{ij}$ is the coefficient $X_i = b_{ij} X_j + e_i$
  - Show that $B$ is acyclic (uniquely oriented)
  - Compare to PC output (many ambiguous edges) and GES output (similar to PC)
- Bottom row: Histogram of noise distributions
  - Show non-Gaussianity (e.g., heavy tails, skewness)
  - Highlight that ICA can recover these independent non-Gaussian components

**Interactive widgets**

- Slider: skewness of noise distribution (0 = Gaussian to 5 = heavy-tailed)
  - Gaussian case: chains indistinguishable
  - Skewed case: asymmetry reveals direction
- Slider: signal-to-noise ratio (SNR)
  - Low SNR: noise dominates, harder to detect asymmetry
  - High SNR: clear non-Gaussianity signal
- Toggle: "Show recovered $B$ matrix" vs. "Show as DAG"
- Seed: for data generation

**Key insights**

- Gaussian linear models are symmetric: swapping cause and effect preserves
  distribution
- Non-Gaussianity breaks the symmetry: LiNGAM exploits this to orient edges
- LiNGAM requires strong assumptions (linear, independent non-Gaussian noise)
  but provides full identifiability

**Comment box**

- "If your data are non-Gaussian, LiNGAM can recover the full directed DAG. Test
  for non-Gaussianity first (Jarque-Bera, skewness tests)."

## Cell 7: Comparing Algorithms: Which One to Use?
**Purpose**

- Show outputs from PC, GES, and LiNGAM on the same data
- Build intuition for when each algorithm excels
- Understand trade-offs between assumptions, scalability, and informativeness

**Display**

- Three DAG outputs side-by-side
  - **PC output**: CPDAG with undirected and directed edges
  - **GES output**: Full DAG with directed edges
  - **LiNGAM output**: Full DAG with edge weights
- Below each: summary statistics
  - Number of edges
  - Number of undirected vs. directed edges (for PC)
  - Edge confidence (for LiNGAM, show coefficients)
- Consensus matrix: heatmap showing which edges are recovered by each algorithm

**Interactive widgets**

- Dropdown: select dataset type
  - Linear Gaussian data (PC and GES agree; LiNGAM fails)
  - Linear non-Gaussian data (LiNGAM succeeds)
  - Nonlinear data (none fully recover, GES often best)
- Slider: sample size ($N = 100$ to $N = 5000$)
- Toggle: "Show edge weights" to see LiNGAM coefficients
- Seed: for data generation

**Key insights**

- PC: constraint-based, good for small samples, returns equivalence class (many
  ambiguous edges)
- GES: score-based, more interpretable output, but assumes no hidden confounders
- LiNGAM: functional, requires non-Gaussianity, gives full DAG, but limited to
  linear models
- Consensus: edges found by multiple algorithms are more trustworthy

**Comment box**

- "Start with PC for exploratory analysis. Use GES if you want directed edges
  Use LiNGAM only if non-Gaussianity is confirmed. Trust edges found by multiple
  algorithms."

## Cell 8: Validating Discovered DAGs with Refutation Tests
**Purpose**

- Show how to validate a discovered DAG against data
- Build intuition for when to trust discovery output
- Demonstrate placebo tests and sensitivity checks

**Display**

- Left panel: discovered CPDAG from PC or GES
- Right panel: validation results displayed as a dashboard
  - **CI test validation**: for each implied independence, show p-value
    - Bar chart: p-values for all implied CIs
    - Green if p > alpha (independence confirmed)
    - Red if p < alpha (independence violated)
  - **Placebo test**: shuffle the target variable and re-run discovery
    - Show that discovery still finds edges (should not!)
    - Highlight this as evidence of overfitting
  - **Sensitivity analysis**: add a simulated hidden confounder and measure
    effect on conclusions
    - Line plot: conclusion robustness vs. confounder strength
- Bottom: overall validation score (% of implied independencies confirmed)

**Interactive widgets**

- Slider: CI test threshold (alpha = 0.01 to 0.2) for validation
- Slider: strength of simulated hidden confounder (0 to 1)
- Toggle: "Run placebo test" to execute a null-hypothesis check
- Toggle: "Show failed tests" vs. "Show all tests"
- Seed: for validation data (separate from discovery data)

**Key insights**

- Validation checks whether the discovered DAG's implications hold in data
- Low validation score suggests violated assumptions (hidden confounders,
  non-stationarity)
- Placebo tests catch overfitting: if discovery finds structure in pure noise,
  something is wrong
- Sensitivity analysis quantifies robustness to unobserved confounders

**Comment box**

- "A discovered DAG is a hypothesis. Validation tells you if the hypothesis is
  consistent with data. Consistency is not proof, but inconsistency is
  refutation."

## Cell 9: Domain Knowledge Integration: Constraints and Prior DAGs
**Purpose**

- Show how expert knowledge can guide discovery
- Demonstrate the impact of forbidding/requiring edges
- Build intuition for combining data-driven discovery with domain expertise

**Display**

- Top left: fully automatic discovery result (no constraints)
- Top right: expert-specified constraints
  - List of forbidden edges (e.g., "outcome cannot cause treatment")
  - List of required edges (e.g., "treatment causes outcome")
  - Temporal tiers (variables ordered in time layers)
- Bottom left: discovery with constraints applied
  - Shows reduced edge candidate space
  - Faster algorithm (fewer edges to consider)
  - Fewer ambiguities in final DAG
- Bottom right: impact summary
  - Bar chart showing reduction in search space
  - Table of which constraints affected the final DAG

**Interactive widgets**

- Checkboxes: toggle each constraint on/off to see its impact
  - Watch the search space shrink when constraints added
  - See final DAG change as constraints change
- Add custom constraint: "Forbid edge $X \to Y$" with text input
  - Immediately re-run discovery and show updated result
- Slider: strength of prior (how much to trust expert knowledge)
- Seed: for data generation

**Key insights**

- Partial domain knowledge drastically reduces search space and improves
  accuracy
- Constraints must be correct: wrong priors inject errors
- Temporal ordering is the strongest constraint (past cannot depend on future)
- Active learning: after discovery, expert can suggest next experiment to reduce
  ambiguity

**Comment box**

- "Combine automatic discovery with domain expertise. Expert knowledge should
  guide the search, but data should refute false structures."

## Cell 10: End-to-End Workflow: From Data to Validated DAG
**Purpose**

- Integrate all previous concepts into a complete discovery pipeline
- Show real-world workflow: preparation, discovery, refinement, validation
- Build confidence that discovery can guide practical causal reasoning

**Display**

- Multi-panel workflow visualization:
  1. **Data preparation**: histogram of variables, test for non-Gaussianity,
     identify temporal order
  2. **Discovery step**: run PC, GES, and LiNGAM (toggle which algorithms to
     use)
  3. **Consensus step**: Venn diagram of edges found by each algorithm
  4. **Refinement step**: expert review, add constraints, re-run discovery
  5. **Validation step**: refutation tests, validation score, sensitivity
     analysis
  6. **Final DAG**: refined and validated causal structure
- Progress bar: shows which stage of workflow is active

**Interactive widgets**

- Dropdown: select a dataset (synthetic or real-world example)
  - Synthetic: linear Gaussian, linear non-Gaussian, nonlinear
  - Real: economic data (inflation, unemployment, interest rates), health data
- Checkboxes: select algorithms to run (PC, GES, LiNGAM)
- "Add constraint" button: step-by-step add expert knowledge
- "Validate" button: run full validation pipeline
- Speed slider: animation speed for the workflow
- Seed: for reproducibility

**Key insights**

- Discovery is a pipeline, not a single algorithm call
- Multiple algorithms provide robustness: edges found by all are most
  trustworthy
- Expert review and constraints improve accuracy without losing data-driven
  insights
- Validation ensures the discovered structure is plausible and consistent with
  data

**Comment box**

- "This workflow balances automated discovery with expert judgment. Discovery is
  most powerful when combined with domain knowledge, validated with care, and
  interpreted as a hypothesis for further investigation."

## Summary of Key Takeaways
- **Identifiability is limited**: observational data can only recover
  equivalence classes unless you have interventions or functional assumptions
- **Three algorithm families**:
  - Constraint-based (PC): uses conditional independence tests
  - Score-based (GES): searches DAG space to optimize fit
  - Functional (LiNGAM): exploits non-Gaussianity for full recovery
- **Discovery generates hypotheses**: treat output as plausible candidates, not
  ground truth
- **Validation is essential**: check that discovered DAG's implications hold in
  data
- **Combine with expertise**: domain knowledge guides discovery and refutes
  implausible structures
- **No algorithm solves causality alone**: humans and data together recover
  causal understanding
