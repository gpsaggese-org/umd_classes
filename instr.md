Execute skill /notebook.outline.create ./msml610/lectures_source/Lesson10.2-Causal_Discovery.txt

// Packages:
// - gCastle (causal-learn)
//   - Implements constraint-based (PC, FCI), score-based (GES), and functional
//     (LiNGAM) algorithms
//   - Supports both observational and interventional data discovery
//   - Includes evaluation metrics and algorithm comparisons
// - CausalNex
//   - Build and visualize causal graphs programmatically
//   - Define domain constraints (forbidden/required edges, temporal ordering)
//   - Structural causal model inference and visualization
// - DoWhy
//   - Causal inference and effect estimation from discovered graphs
//   - Refutation testing (placebo, random treatment, confounder sensitivity)
//   - Validation and assumption checking for discovered structures

// Tutorial outline:
// - Load real-world observational data (e.g., UCI datasets)
// - Run multiple discovery algorithms (PC, GES, LiNGAM) and compare outputs
// - Encode domain knowledge as constraints and measure impact on discovery
// - Validate discovered DAGs using conditional independence tests
// - Perform refutation tests to check robustness
// - Analyze Markov equivalence classes and ambiguous edge directions
// - Visualize discovered graphs and confidence scores for edges

// Tutorial:
// - Load a real dataset (e.g., stock returns, health metrics)
// - Test conditional independence using `gCastle.pc()` and `CausalNex` graph
//   operations
// - Compare PC output across different CI test statistics (correlation, partial
//   correlation, G²)
// - Visualize the discovered CPDAG and highlight ambiguous edges
// - Save outputs as images showing skeleton vs. directed edges

// Tutorial:
// - Use `CausalNex` to define domain knowledge as a constraint graph
// - Encode temporal ordering: create layers and forbid backward edges
// - Mark forbidden edges (e.g., "outcome cannot cause treatment") and required edges
// - Run discovery algorithm (PC, GES) with and without constraints
// - Quantify impact: compare edge count, equivalence class size, computation time
// - Visualize constraint graphs and discovered CPDAGs side-by-side

// Tutorial:
// - Implement PC algorithm step-by-step using `gCastle.pc()`
// - Load dataset and specify CI test (e.g., partial correlation for continuous data)
// - Compare runtime and edge recovery with different CI test thresholds
// - Inspect the separating sets returned by PC to understand orientation rules
// - Validate output by checking implied conditional independencies hold in data

// Tutorial:
// - Use `gCastle.ges()` to run score-based search with BIC scoring
// - Compare GES results directly with PC/FCI outputs on same dataset
// - Analyze which edges are consistently discovered across algorithms (robust edges)
// - Implement GES with alternative scoring functions (BDeu) and compare stability
// - Visualize the forward and backward search phases to understand the optimization process

// Tutorial:
// - Test data for non-Gaussianity using statistical tests (Jarque-Bera, skewness)
// - Use `gCastle.lingam()` to recover the full directed DAG
// - Compare LiNGAM-recovered DAG with PC and GES outputs
// - Visualize the adjacency matrix $B$ showing edge coefficients and directions
// - Assess recovery performance on synthetic data with known ground truth

// Tutorial:
// - Use `CausalNex` to extract all conditional independence statements from
//   discovered DAG
// - Implement a refutation pipeline: for each CI statement, run statistical test
//   on data
// - Count violations; compute p-values for each implied independence
// - Run placebo tests using `DoWhy`: replace target variable with random noise
// - Check robustness via sensitivity analysis: add unobserved confounder,
//   recompute effects
// - Report validation summary: percentage of implied independencies confirmed

// Tutorial:
// - Start with an expert-specified DAG as baseline (prior knowledge)
// - Run discovery algorithms to generate candidate structures
// - For each new discovered edge: check algorithm agreement (multi-algorithm voting)
// - Validate using refutation tests and domain plausibility
// - Incrementally update the DAG as evidence accumulates
// - Document the reasoning for each edge addition/removal in a decision log


// Complete workflow integrating all techniques:

// **Data Preparation & Exploration**
// - Load observational dataset; inspect missingness, distributions
// - Test for non-Gaussianity (statistical tests)
// - Identify temporal ordering and natural variable tiers

// **Domain Knowledge Integration**
// - Create expert-specified prior knowledge graph using `CausalNex`
// - Define forbidden edges (causality reversals), required edges (known mechanisms)
// - Encode temporal constraints (past → future)

// **Algorithm Comparison**
// - Run PC (constraint-based) with multiple CI tests
// - Run GES (score-based) with BIC and alternative scores
// - Run LiNGAM (functional) if non-Gaussianity confirmed
// - Compare CPDAGs: skeleton overlap, ambiguous edge directions

// **Robustness & Validation**
// - Extract consensus edges found by multiple algorithms
// - Enumerate conditional independencies from discovered DAG
// - Run refutation tests: placebo, random treatment, confounder sensitivity
// - Report validation score (% of implied independencies confirmed)

// **Expert Review & Iteration**
// - Present discovered structure to domain expert
// - Refute edges contradicting known mechanisms
// - Suggest next interventional experiment using active learning criteria

// **Visualization & Documentation**
// - Create comparison plots: PC vs. GES vs. LiNGAM outputs
// - Highlight consensus edges (thick) vs. algorithm-specific edges (thin)
// - Document assumptions, limitations, and sensitivity to parameter choices

- If the task is not perfectly clear, you MUST not perform it, but ask for
  clarifications
  - When the task is complex, create a plan.md with 5 bullet points explaining
    what the plan is

- When writing code you must always follow the instructions in
  `@.claude/skills/coding.rules.md`

- Generate unit tests for the new code following the instructions in
  `@.claude/skills/testing.rules.md`
