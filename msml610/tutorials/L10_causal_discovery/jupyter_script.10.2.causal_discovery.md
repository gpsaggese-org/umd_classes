# Jupyter Notebook Outline: Causal Discovery

## Overview
This notebook teaches causal discovery through interactive visualizations and
incremental examples, building intuition about how algorithms infer causal
structure from observational data

## Cell 1: The Core Problem: Correlation vs. Causation

- **Purpose**: Understand why causal direction matters for decision-making and see the fundamental gap between correlation and causation.
- **Display**:
  - Two scatter plots side-by-side showing identical correlation patterns
  - Both show X and Y with perfect correlation (r = 0.95)
  - Left plot labeled: "Chain: X -> Y" with annotation "(if we intervene on X, Y changes)"
  - Right plot labeled: "Reverse: Z -> Y -> X" with annotation "(intervening on X has no effect)"
  - Summary box showing decision scenarios: "Which variable should you intervene on to change the outcome?"
- **Interactive widget**:
  - Toggle: observational vs. interventional mode
    - Observational: both DAGs produce identical scatter plot
    - Interventional: shows divergent outcomes after intervention
  - Slider for correlation strength (r = 0.3 to r = 0.99)
  - "Intervene on X" button to show counterfactual outcome
- **Key insights**:
  - Prediction and causation require fundamentally different reasoning
  - Correlation alone cannot determine causal direction
  - Same correlation pattern can hide opposite causal implications
- **Comment box**: "This is the core problem: no amount of observational data alone distinguishes these structures. We need additional assumptions or interventions."
- **Implementation**: Matplotlib for scatter plots, numpy for correlated data generation, ipywidgets for toggles and sliders

## Cell 2: Markov Equivalence: Three Indistinguishable Structures

- **Purpose**: Show that different DAGs encode identical conditional independencies and introduce the CPDAG as the best we can do with observational data.
- **Display**:
  - Three DAGs side-by-side: Chain (X -> Y -> Z), Reverse (Z -> Y -> X), Common Cause (X <- Y -> Z)
  - Below each DAG: list of implied conditional independencies
    - All three imply: X indep Z | Y
    - Distributions are mathematically identical
  - CPDAG visualization showing the equivalence class
    - Skeleton with undirected edges (X - Y - Z)
    - Marks indicating which edge directions are ambiguous
- **Interactive widget**:
  - Slider: sample size (N = 50 to N = 5000)
  - Histogram panel showing correlation between X and Z (identical across all three)
  - Histogram panel showing conditional correlation X vs Z given Y (near-zero for all)
  - Toggle: "Show which CI tests were performed" to reveal the critical tests
- **Key insights**:
  - Observational data recover only conditional independence structure
  - Edge directions in chains are fundamentally ambiguous
  - CPDAG is the most informative output possible from observational data
- **Comment box**: "This is why observational discovery outputs equivalence classes. Without interventions or functional assumptions, multiple DAGs are equally valid."
- **Implementation**: Networkx for DAG structures, matplotlib for visualization, numpy for statistical testing, pandas for CI test results

## Cell 3: Why Direction Matters: Causal Effects via Intervention

- **Purpose**: Show concretely why edge direction determines causal effect and build intuition for why structure recovery is crucial for policy.
- **Display**:
  - Three side-by-side panels showing counterfactual outcomes for each structure
  - Scenario: intervene on X (set high vs. low) and observe effect on Z
    - Chain (X -> Y -> Z): large effect on Z
    - Reverse (Z -> Y -> X): no effect on Z
    - Common Cause (Y confounds both): no direct effect on Z
  - Table: effect size, confidence interval, direction for each structure
  - Visualization of how effect propagates (or not) through the DAG using color flow
- **Interactive widget**:
  - Slider: intervention strength (magnitude of change to X, range 0-3)
  - Slider: sample size for effect estimation (N = 100 to N = 5000)
  - Toggle: "Show confounding" to highlight when hidden confounders explain the observation
  - "Intervene" button to trigger simulation
- **Key insights**:
  - Same observational correlation, wildly different causal effects
  - Edge direction determines whether an intervention is effective
  - Policy decisions depend critically on DAG structure
- **Comment box**: "This illustrates why we cannot simply read causation from correlation. Choosing the wrong DAG leads to ineffective interventions."
- **Implementation**: Matplotlib for counterfactual visualization, numpy for causal simulation, scipy for confidence intervals

## Cell 4: The PC Algorithm: Learning From Conditional Independence Tests

- **Purpose**: Understand constraint-based discovery and see step-by-step how PC uses CI tests to prune edges and build the CPDAG.
- **Display**:
  - Animated visualization of PC algorithm on 4-5 variable DAG
  - Start with fully connected graph
  - Step-by-step progression:
    1. Show first CI test (e.g., X1 indep X2?)
    2. If true, remove edge and highlight separating set
    3. Continue through all pairs with conditioning sets
    4. Show intermediate graph after each decision
    5. Orient v-structures (colliders)
    6. Apply orientation rules to finalize CPDAG
  - Right panel: current step number, CI test being performed, p-value, separating set
- **Interactive widget**:
  - Slider: CI test threshold (alpha = 0.001 to 0.2)
    - Lower threshold: stricter tests, keep more edges
    - Higher threshold: liberal tests, remove more edges
  - Dropdown: CI test type (Partial correlation, Gaussian G-squared, Conditional mutual information)
  - Play/Pause buttons for step-by-step exploration
  - Speed slider for animation
- **Key insights**:
  - PC recovers skeleton via CI tests, then orients v-structures
  - Stronger distributional assumptions enable more powerful tests
  - CI test errors propagate directly to DAG structure errors
- **Comment box**: "PC is sound in the large-sample limit, but CI tests are underpowered in finite samples. Small samples or weak dependencies cause edge recovery errors."
- **Implementation**: Causallearn PC implementation or from-scratch numpy/scipy CI tests, networkx for graph operations, matplotlib for animation

## Cell 5: Score-Based Search: GES (Greedy Equivalence Search)

- **Purpose**: Introduce score-based discovery where algorithms optimize fit to data instead of testing independencies.
- **Display**:
  - Left panel: animated DAG evolving during search
    - Starts empty (no edges)
    - Shows which edge is being added/removed at each step
    - Color-codes edges by score contribution (bright = high improvement)
    - Current BIC score displayed below graph
  - Right panel: line plot of BIC score vs. iteration
    - Annotations for forward/backward phase transitions
    - Shows local maxima and convergence plateau
  - Bottom: table of top 5 candidate edges at current iteration
- **Interactive widget**:
  - Slider: sample size (N = 50 to N = 10000)
    - BIC penalty proportional to log(N) for model complexity
    - Larger N allows more edges
  - Slider: regularization strength (encourages sparsity)
  - Dropdown: score function (BIC, BDeu)
  - Play/Pause buttons and speed slider for animation
- **Key insights**:
  - GES searches DAG space using greedy forward-backward heuristics
  - BIC balances likelihood fit with model complexity
  - Forward phase adds edges, backward removes low-value edges
- **Comment box**: "GES is guaranteed to recover the equivalence class in the limit, but greedy search can get stuck in local optima. Multiple random initializations improve robustness."
- **Implementation**: Causallearn GES or pgmpy for score-based search, matplotlib for score trajectory visualization, pandas for edge ranking

## Cell 6: Non-Gaussian Methods: LiNGAM for Full Identifiability

- **Purpose**: Show how non-Gaussianity breaks directional symmetry and enables full DAG recovery instead of just equivalence classes.
- **Display**:
  - Top row: three scatter plots showing data clouds for the same three structures from Cell 2
    - Gaussian case: all three shapes identical (same covariance ellipsoid)
    - Non-Gaussian case: shapes show asymmetry revealing direction
  - Middle row: LiNGAM adjacency matrices
    - Matrix B where Xi = sum(bij * Xj) + ei
    - B is acyclic (uniquely oriented DAG)
    - Compare to PC output (many undirected edges) and GES (similar to PC)
  - Bottom row: histograms of noise distributions
    - Show non-Gaussianity metrics (heavy tails, skewness)
    - Highlight that ICA recovers independent non-Gaussian components
- **Interactive widget**:
  - Slider: skewness of noise distribution (0 = Gaussian to 5 = heavy-tailed)
    - Gaussian: chains indistinguishable
    - Skewed: asymmetry reveals direction
  - Slider: signal-to-noise ratio (Low = noise dominates, High = clear signal)
  - Toggle: show recovered B matrix vs. show as DAG
  - Jarque-Bera test result displayed
- **Key insights**:
  - Gaussian linear models are symmetric: X->Y and Y->X produce same distribution
  - Non-Gaussianity breaks symmetry: LiNGAM exploits asymmetry to orient edges
  - LiNGAM provides full DAG identification under linear non-Gaussian assumptions
- **Comment box**: "If data are non-Gaussian, LiNGAM can recover the full directed DAG. Test for non-Gaussianity first using Jarque-Bera or skewness tests."
- **Implementation**: Causallearn LiNGAM or lingam library, scipy.stats for distribution tests, matplotlib for data clouds and B matrix heatmap

## Cell 7: Comparing Algorithms: Which One to Use?

- **Purpose**: Show outputs from PC, GES, and LiNGAM on the same data and build intuition for algorithm selection.
- **Display**:
  - Three DAG outputs side-by-side
    - PC output: CPDAG with mixed directed/undirected edges
    - GES output: Full DAG with directed edges
    - LiNGAM output: Full DAG with edge weight labels
  - Below each: summary statistics
    - Edge count, ambiguity count, computation time
    - Edge weights or confidence scores
  - Consensus heatmap: which edges recovered by each algorithm (venn diagram style)
- **Interactive widget**:
  - Dropdown: dataset type (Linear Gaussian, Linear Non-Gaussian, Nonlinear)
  - Slider: sample size (N = 100 to N = 5000)
  - Toggle: show edge weights/confidence scores
  - "Run all algorithms" button
- **Key insights**:
  - PC: constraint-based, good for small samples, returns equivalence class
  - GES: score-based, more directed edges, assumes no hidden confounders
  - LiNGAM: functional approach, requires non-Gaussianity, full DAG recovery
  - Consensus edges (found by multiple algorithms) are most trustworthy
- **Comment box**: "Start with PC for exploratory analysis. Use GES if you want directed edges. Use LiNGAM only if non-Gaussianity is confirmed. Trust edges found by multiple algorithms."
- **Implementation**: Causallearn for PC/GES/LiNGAM, matplotlib for side-by-side visualization, pandas for consensus statistics

## Cell 8: Validating Discovered DAGs with Refutation Tests

- **Purpose**: Show how to validate that a discovered DAG's implications hold in the data.
- **Display**:
  - Left panel: discovered CPDAG from PC or GES
  - Right panel: validation dashboard with three sections
    - CI test validation: bar chart of p-values for all implied independencies (green = pass, red = fail)
    - Placebo test: discovery output when applied to shuffled data (should find nothing)
    - Sensitivity analysis: line plot showing conclusion robustness vs. hidden confounder strength
  - Bottom: overall validation score (% of implied independencies confirmed)
- **Interactive widget**:
  - Slider: CI test threshold (alpha = 0.01 to 0.2) for validation
  - Slider: hidden confounder strength (0 = none to 1 = strong)
  - "Run placebo test" button
  - Toggle: show failed tests vs. show all tests
  - "Run validation" button
- **Key insights**:
  - Validation checks whether discovered DAG implications hold in data
  - Low validation score suggests violated assumptions (hidden confounders, non-stationarity)
  - Placebo tests detect spurious structure discovery in noise
  - Sensitivity analysis quantifies robustness to unobserved confounders
- **Comment box**: "A discovered DAG is a hypothesis. Validation checks consistency with data. Consistency is not proof of causality, but inconsistency is refutation."
- **Implementation**: DoWhy for refutation tests, scipy.stats for CI tests, matplotlib for validation dashboard

## Cell 9: Domain Knowledge Integration: Constraints and Prior DAGs

- **Purpose**: Show how expert knowledge (forbidden/required edges, temporal order) drastically improves discovery accuracy.
- **Display**:
  - Top left: fully automatic discovery result (no constraints)
  - Top right: expert-specified constraints listed
    - Forbidden edges (e.g., "outcome cannot cause treatment")
    - Required edges (e.g., "treatment causes outcome")
    - Temporal tiers showing variable layers
  - Bottom left: discovery with constraints applied
    - Reduced edge candidate space
    - Fewer ambiguities in final DAG
  - Bottom right: impact summary
    - Bar chart showing search space reduction
    - Table showing which constraints affected final DAG
- **Interactive widget**:
  - Checkboxes: toggle each constraint to see its impact
  - Text input: add custom constraint (e.g., "Forbid X -> Y")
  - Slider: strength of prior (how much to trust expert knowledge)
  - "Re-run discovery" button
- **Key insights**:
  - Partial domain knowledge drastically reduces search space and improves accuracy
  - Constraints must be correct: wrong priors inject errors
  - Temporal ordering is the strongest constraint
  - Expert and automated discovery are complementary
- **Comment box**: "Combine automatic discovery with domain expertise. Expert knowledge guides the search, and data refutes false structures."
- **Implementation**: Causallearn with domain knowledge objects, networkx for constraint enforcement, matplotlib for impact visualization

## Cell 10: End-to-End Workflow: From Data to Validated DAG

- **Purpose**: Integrate all techniques into a complete discovery pipeline showing the practical workflow from raw data to validated causal structure.
- **Display**:
  - Multi-panel workflow visualization with six stages:
    1. Data preparation: variable histograms, non-Gaussianity test results, temporal order
    2. Discovery step: run selected algorithms with results displayed
    3. Consensus step: Venn diagram of edges found by each algorithm
    4. Refinement step: expert review with constraint options
    5. Validation step: refutation tests with pass/fail results
    6. Final DAG: refined and validated causal structure
  - Progress bar showing current workflow stage
  - Summary statistics at each stage
- **Interactive widget**:
  - Dropdown: select dataset (Synthetic: Linear Gaussian, Linear Non-Gaussian, Nonlinear; Real: economic, health data)
  - Checkboxes: select algorithms to run (PC, GES, LiNGAM)
  - "Add constraint" button for step-by-step expert input
  - "Validate" button to run full validation pipeline
  - Speed slider for animation
  - "Export results" button
- **Key insights**:
  - Discovery is a pipeline, not a single algorithm call
  - Multiple algorithms provide robustness via consensus
  - Expert review and constraints improve accuracy without losing data-driven insights
  - Validation ensures the discovered structure is plausible
- **Comment box**: "This workflow balances automated discovery with expert judgment. Discovery is most powerful when combined with domain knowledge, validated carefully, and interpreted as a hypothesis for investigation."
- **Implementation**: Integration of causallearn (PC/GES/LiNGAM), DoWhy for refutation, matplotlib/plotly for multi-stage visualization, pandas for workflow statistics
