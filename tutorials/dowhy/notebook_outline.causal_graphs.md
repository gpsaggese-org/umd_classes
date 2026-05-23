# Notebook Outline: Causal Graphs and Causal Discovery

## Learning Objectives
By the end of this notebook, students will be able to:
- Specify causal graphs using domain knowledge
- Understand different approaches to learning causal structure from data
- Compare causal discovery algorithms (CDT, dodiscover, causal-learn)
- Validate and refute causal hypotheses using statistical tests
- Apply causal graph methods to practical data problems

---

## Cell 1: Introduction to Causal Graphs (Markdown + Visualization)

**Purpose**: Build intuition about what causal graphs are and why they matter

**Content Description**:
- Visual explanation: Simple DAG (Directed Acyclic Graph) examples
- Distinction between correlation and causation
- Three motivating examples from different domains (health, economics, social)
- Interactive diagram showing how adding/removing edges changes the causal structure

**Expected Output**: 
- Clear diagrams showing causal relationships
- Audience understanding of why causal thinking differs from statistical thinking

---

## Cell 2: Domain Knowledge and Expert Causal Graphs (Code + Visualization)

**Purpose**: Learn how to encode domain knowledge into formal causal graphs

**Content Description**:
- Load a realistic dataset (e.g., synthetic healthcare or economic data)
- Build a causal graph by hand using domain expertise
- Show how to represent the graph using networkx or pygraphviz
- Visualize the resulting DAG with clear node labels and edge directions

**Key Variables**:
- Dataset with 5-10 variables for manageable complexity
- Node names, edge directions based on domain knowledge

**Expected Output**:
- A clean visualization of a hand-specified causal graph
- Print the graph structure (adjacency representation)

---

## Cell 3: Limitations of Domain Knowledge Alone (Interactive)

**Purpose**: Motivate the need for data-driven causal discovery

**Content Description**:
- Show 2-3 real datasets where domain knowledge alone is insufficient
- Highlight ambiguous relationships that data might help resolve
- Interactive widget: toggle different graph configurations and see how they fit the data differently
- Build intuition that data can help validate or refute causal assumptions

**Key Variables**:
- Multiple candidate graph structures
- Dataset with correlation patterns

**Expected Output**:
- Visualization showing which graphs are consistent with the data
- Clear demonstration that statistical patterns alone don't determine causality

---

## Cell 4: Causal Discovery Algorithms Overview (Markdown + Comparison Table)

**Purpose**: Introduce the major causal discovery approaches and their trade-offs

**Content Description**:
- Brief overview of three main algorithms: CDT (Causal Discovery Toolbox), dodiscover, causal-learn
- Table comparing: assumptions, computational complexity, assumptions, output type
- Visual diagram showing the general workflow: Data -> Algorithm -> Causal Graph
- Highlight key differences in assumptions (Markov, causal sufficiency, acyclicity, etc.)

**Expected Output**:
- Comparison table with algorithm properties
- Clear visual workflow diagram

---

## Cell 5: Causal Discovery with CDT (Code)

**Purpose**: Hands-on experience with the CDT library

**Content Description**:
- Load a synthetic dataset with known causal structure (but students don't know it yet)
- Apply CDT causal discovery algorithm
- Visualize the discovered graph
- Compare discovered graph to the true causal structure (show accuracy metrics: precision, recall)

**Key Variables**:
- CDT algorithm parameters (e.g., method selection)
- Dataset with 5-8 variables and 500+ samples

**Expected Output**:
- Discovered causal graph visualization
- Comparison metrics showing how well CDT recovered the true structure

---

## Cell 6: Causal Discovery with dodiscover (Code)

**Purpose**: Hands-on experience with dodiscover algorithm

**Content Description**:
- Apply dodiscover on the same dataset as Cell 5
- Visualize the discovered graph
- Compare with CDT results: which edges did each algorithm agree on? Disagree on?
- Interactive visualization: toggle between CDT and dodiscover results

**Key Variables**:
- dodiscover algorithm parameters
- Same dataset as Cell 5

**Expected Output**:
- Discovered graph visualization
- Side-by-side comparison with CDT results
- Summary of agreement/disagreement between methods

---

## Cell 7: Causal Discovery with causal-learn (Code)

**Purpose**: Hands-on experience with causal-learn library

**Content Description**:
- Apply causal-learn on the same dataset
- Show multiple algorithms available in causal-learn (e.g., PC, FCI, GES)
- Visualize results from 2-3 different causal-learn algorithms
- Interactive widget: select algorithm and visualize the resulting causal graph

**Key Variables**:
- causal-learn algorithm selection
- Parameter tuning (independence test type, significance level)

**Expected Output**:
- Graphs from multiple causal-learn algorithms
- Interactive interface to explore different methods

---

## Cell 8: Comparing Causal Discovery Methods (Visualization + Analysis)

**Purpose**: Synthesize understanding of different algorithms

**Content Description**:
- Summary comparison: which edges appear in all methods? Some methods? Only one method?
- Consensus graph showing high-confidence edges
- Discussion of stability and robustness across algorithms
- Visualization: show edges colored by "confidence" (number of algorithms that found them)

**Key Variables**:
- Results from all three algorithms (CDT, dodiscover, causal-learn)

**Expected Output**:
- Consensus/confidence-weighted graph visualization
- Table showing agreement across algorithms

---

## Cell 9: Independence Tests for Causal Validation (Code + Interactive)

**Purpose**: Learn how to statistically test causal relationships

**Content Description**:
- Explain the concept of conditional independence
- Show different independence test types (Pearson, Spearman, Kernel CMI, etc.)
- For the discovered causal graph, perform independence tests implied by the graph
- Interactive widget: select two variables and a conditioning set, visualize the test result

**Key Variables**:
- Variable pairs for testing
- Independence test type
- Significance level (alpha)

**Expected Output**:
- Test statistics and p-values
- Visualization of independent/dependent variable pairs

---

## Cell 10: Refuting Causal Graphs with Graph Refutations (Code)

**Purpose**: Learn systematic ways to test whether a causal graph is plausible

**Content Description**:
- Introduce graph refutation methods (independence tests at scale)
- For the discovered causal graph, run a full refutation analysis
- Show which edges have strong support and which are questionable
- Visualization: mark problematic edges that violate independence assumptions

**Key Variables**:
- Causal graph (from discovery)
- Refutation test type
- Confidence threshold

**Expected Output**:
- Refutation report showing problematic edges
- Annotated graph highlighting uncertain or unsupported relationships

---

## Cell 11: Sensitivity Analysis on Graph Discovery (Interactive)

**Purpose**: Understand robustness of discovered causal structures

**Content Description**:
- Re-run causal discovery with different parameters or subsets of data
- Interactive widget: adjust key parameters (sample size, noise level, algorithm hyperparameters)
- See how the discovered graph changes with different settings
- Build intuition about which edges are stable and which are fragile

**Key Variables**:
- Parameter ranges (sample size, noise, independence test threshold, etc.)

**Expected Output**:
- Multiple discovered graphs under different conditions
- Summary showing which edges are consistent across variations
