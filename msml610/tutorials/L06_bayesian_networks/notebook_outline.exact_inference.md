---
name: exact_inference
description: Interactive Jupyter notebook outline for teaching exact inference in Bayesian networks (enumeration and variable elimination)
metadata:
  type: notebook_outline
  lesson: MSML610 Lesson 06.2
  libraries: pgmpy, pandas, seaborn, matplotlib, ipywidgets, networkx
  domain: probabilistic_reasoning
---

# Exact Inference in Bayesian Networks

- This notebook teaches how to compute exact posteriors $P(X \mid \mathbf{e})$ in
  a discrete Bayesian network
- Concepts are built on the canonical AIMA burglary-alarm network and the query
  $P(Burglary \mid JohnCalls, MaryCalls)$
- The pedagogical arc is:
  - Inference by enumeration (brute force) -> variable elimination (caching)
    -> irrelevant-variable pruning -> complexity and limits
- Focus is on hands-on discovery: students manipulate evidence, watch sums
  unfold, and see why caching turns an exponential computation into a tractable
  one

# Part 1: Setting Up the Inference Problem

## Cell 1.1: The Burglary Alarm Network and Its CPTs

- **Purpose**: Re-anchor students in the network we will reason about, so that
  every later inference step refers to a concrete, visible structure and set of
  numbers
- **Display**:
  - Causal DAG drawn with `plot_causal_dag()`: $Burglary \to Alarm$,
    $Earthquake \to Alarm$, $Alarm \to JohnCalls$, $Alarm \to MaryCalls$
  - Root causes (Burglary, Earthquake) in blue, Alarm in orange, calls
    (JohnCalls, MaryCalls) in purple
  - Beside the graph, the five conditional probability tables shown as formatted
    `pandas` DataFrames:
    - $P(B)=0.001$, $P(E)=0.002$
    - $P(A \mid B, E)$ with the four parent combinations
    - $P(J \mid A)$ and $P(M \mid A)$
- **Interactive widget**: None (reference cell that sets up the running example)
- **Key insights**:
  - The joint over five variables factorizes into five small CPTs:
    $P(B,E,A,J,M) = P(B)\,P(E)\,P(A \mid B,E)\,P(J \mid A)\,P(M \mid A)$
  - Calls depend on the world only through $Alarm$: they are conditionally
    independent of $Burglary$ and $Earthquake$ given $Alarm$
  - Storing 5 small CPTs (10 independent numbers) is far cheaper than the full
    joint ($2^5 - 1 = 31$ numbers)
- **Comment box**: "Inference never touches the full joint directly. It works
  with the factored form: a product of the small CPTs attached to each node."
- **Implementation**: `pgmpy.models.DiscreteBayesianNetwork`,
  `pgmpy.factors.discrete.TabularCPD`, `plot_causal_dag()` from
  `helpers_root/helpers/hgraphviz.py`, `pandas` for CPT display

## Cell 1.2: Query, Evidence, and Hidden Variables

- **Purpose**: Introduce the three roles every variable plays in an inference
  query, since the entire algorithm is organized around this partition
- **Display**:
  - Same DAG, but nodes are color-recolored by their role for the current query:
    - Query variable $X$: bold outline (e.g., Burglary)
    - Evidence variables $\mathbf{E}=\mathbf{e}$: filled/shaded (e.g.,
      JohnCalls=True, MaryCalls=True)
    - Hidden variables $\mathbf{Y}$: greyed out (e.g., Earthquake, Alarm)
  - A text strip restates the query in math:
    $P(Burglary \mid JohnCalls{=}T, MaryCalls{=}T)$
- **Interactive widget**:
  - Dropdown for query variable $X$: pick any single node
  - Checkboxes for which remaining nodes are observed (evidence), each with a
    True/False dropdown for its observed value
  - Remaining unselected nodes are automatically labeled hidden
  - Description: "Choose what you are asking about and what you have observed.
    Everything else is hidden and must be summed out."
- **Key insights**:
  - Every node is exactly one of: query, evidence, or hidden
  - The posterior we want is $P(X \mid \mathbf{e})$; hidden variables are not in
    the answer but cannot simply be dropped
  - Changing the evidence changes which variables are hidden, and therefore how
    much summing is needed
- **Comment box**: "Goal: $P(X \mid \mathbf{e})$. Hidden variables $\mathbf{Y}$
  are nuisances we must marginalize (sum) away to get an answer about $X$
  alone."
- **Implementation**: `ipywidgets.Dropdown`, `ipywidgets.Checkbox`,
  `plot_causal_dag()` with per-query node coloring

# Part 2: Inference by Enumeration

## Cell 2.1: From Conditional to Joint via Normalization

- **Purpose**: Derive, step by step, why a conditional query reduces to summing
  entries of the joint and then normalizing, building the formula students will
  compute in the next cell
- **Display**:
  - Three stacked equation panels that reveal one line at a time:
    1. $P(X \mid \mathbf{e}) = \alpha\, P(X, \mathbf{e})$
    2. $P(X, \mathbf{e}) = \sum_{\mathbf{y}} P(X, \mathbf{e}, \mathbf{y})$
    3. For the example:
       $P(b \mid j,m) = \alpha \sum_e \sum_a P(b)P(e)P(a \mid b,e)P(j \mid a)P(m \mid a)$
  - A bar showing the unnormalized vector $\langle P(b,j,m), P(\lnot b,j,m)\rangle$
    next to the normalized posterior, with the normalization constant $\alpha$
    labeled as $1/(\text{their sum})$
- **Interactive widget**:
  - Toggle "show normalization": switches the displayed bars between unnormalized
    joint values and the normalized posterior that sums to 1
- **Key insights**:
  - The normalization constant $\alpha$ removes the need to ever compute
    $P(\mathbf{e})$ directly
  - A conditional query is just a slice of the joint (fix evidence) plus a sum
    over hidden variables plus a rescale
  - The joint slice is evaluated as a product of CPT lookups, never as one giant
    table
- **Comment box**: "Two moves turn a query into arithmetic: (1) replace the
  conditional by a joint and a constant $\alpha$, (2) sum the joint over hidden
  variables. $\alpha$ is fixed at the end so the answer sums to 1."
- **Implementation**: `matplotlib` text/equation panels, `pandas` for the
  value vectors, `ipywidgets.ToggleButton`

## Cell 2.2: Computing the Posterior by Enumeration

- **Purpose**: Let students compute the exact posterior themselves by summing
  CPT products over hidden variables, and confirm it against `pgmpy`
- **Display**:
  - A 1x4 panel layout:
    - Panel 1: table of every hidden-variable assignment
      $(Earthquake, Alarm)$ and the product
      $P(b)P(e)P(a \mid b,e)P(j \mid a)P(m \mid a)$ for the query value $b$
    - Panel 2: same table for $\lnot b$
    - Panel 3: bar chart of the resulting posterior
      $P(Burglary \mid j,m) \approx \langle 0.284, 0.716 \rangle$, with the
      `pgmpy` reference overlaid as light dotted bars
    - Panel 4: comments panel
  - Empirical/computed bars are solid and dark; the `pgmpy` reference is light
    and dotted
- **Interactive widget**:
  - Dropdown for query variable $X$
  - Checkboxes plus True/False dropdowns to set the evidence
  - The summation tables and posterior bar chart recompute live
  - Description: "Add or remove evidence and watch the rows that get summed and
    the posterior change."
- **Key insights**:
  - The exact posterior $P(b \mid j,m) \approx 0.28$ matches the famous AIMA
    result, computed purely from CPT products
  - The number of rows summed is $2^{(\text{number of hidden variables})}$: it
    grows fast as more variables stay hidden
  - Hand computation and the `pgmpy` engine agree, validating the procedure
- **Comment box**: "Enumeration is correct and simple: list every hidden-world
  combination, multiply the CPTs, sum, normalize. Its weakness is the row count,
  which doubles with each extra hidden variable."
- **Implementation**: `pgmpy.inference.VariableElimination` for the reference,
  explicit nested-sum computation for the teaching table, `pandas`, `seaborn`
  bar charts, `htutori.add_fitted_text_box()` for panel 4

## Cell 2.3: Visualizing the Enumeration Tree

- **Purpose**: Expose the structure of the enumeration computation as a tree, so
  students can literally see the repeated subexpressions that motivate variable
  elimination
- **Display**:
  - An evaluation tree for $\sum_e \sum_a P(b)P(e)P(a \mid b,e)P(j \mid a)P(m \mid a)$
  - Branches alternate over the values of hidden variables ($e$, then $a$),
    leaves show the CPT products being multiplied
  - Repeated subtrees (e.g., the $P(j \mid a)P(m \mid a)$ factors that recur
    under every value of $e$) are highlighted in the same color
- **Interactive widget**:
  - Dropdown for the elimination/summation order (e.g., $e$ first vs $a$ first)
  - The tree redraws and a counter reports the number of multiplications and
    additions performed
  - Toggle "highlight repeated work": shades identical subtrees
- **Key insights**:
  - Enumeration recomputes the same factor products in many branches: this is
    wasted work
  - The order in which variables are summed changes the shape of the tree and
    the operation count
  - The repeated subtrees are exactly what the next algorithm will compute once
    and cache
- **Comment box**: "Look at the repeated branches: the same products are
  evaluated again and again. Caching them is the single idea behind variable
  elimination."
- **Implementation**: `networkx` tree layout with `matplotlib`, color-coded
  repeated nodes, `ipywidgets.Dropdown` for ordering

# Part 3: Variable Elimination

## Cell 3.1: Factors as the Unit of Computation

- **Purpose**: Introduce the factor as the data structure manipulated by
  variable elimination, bridging from CPTs to intermediate results
- **Display**:
  - Each CPT shown as a labeled factor, e.g., $f_A(A,B,E)$, $f_J(J,A)$,
    $f_M(M,A)$, drawn as small tables with their scope (variable set) annotated
  - Two factor operations illustrated visually:
    - Pointwise product: two small tables combine into one over the union of
      their scopes
    - Summing out a variable: a table loses one column and its rows collapse
- **Interactive widget**:
  - Dropdown to pick a variable to sum out of a selected factor
  - The before/after tables update, and the change in table size (number of
    rows) is reported
- **Key insights**:
  - A factor is just a table over a subset of variables; CPTs and intermediate
    results are both factors
  - Two operations suffice for inference: pointwise product and summing out
  - Summing out a variable shrinks the table along that dimension
- **Comment box**: "Everything in variable elimination is a factor. Multiply
  factors that share variables, then sum out the variable you want to remove."
- **Implementation**: `pandas` for factor tables, `seaborn` heatmaps for factor
  visualization, `ipywidgets.Dropdown`

## Cell 3.2: Variable Elimination Step by Step

- **Purpose**: Walk through variable elimination on the alarm query, showing how
  caching intermediate factors avoids the repeated work seen in the enumeration
  tree
- **Display**:
  - A 1x4 panel layout:
    - Panel 1: the current list of active factors (scopes only), updated after
      each elimination step
    - Panel 2: the factor being created at this step (product then sum-out),
      shown as a table
    - Panel 3: bar chart of the running posterior and a side-by-side
      operation-count comparison "enumeration vs variable elimination"
    - Panel 4: comments panel
  - A step counter and "next step" control advance the elimination one variable
    at a time
- **Interactive widget**:
  - Dropdown for elimination order
  - Slider/stepper for "elimination step" (0 to number of hidden variables)
  - Dropdown for query variable and evidence checkboxes (consistent with earlier
    cells)
  - As steps advance, the factor list shrinks and the operation counts update
- **Key insights**:
  - Variable elimination computes each shared factor once and reuses it,
    matching the highlighted repeats from Cell 2.3
  - It returns the identical posterior as enumeration but with far fewer
    operations
  - A good elimination order keeps the intermediate factors small; a bad order
    can create large ones
- **Comment box**: "Same answer, less work. Variable elimination is enumeration
  with the repeated subexpressions cached as intermediate factors. Order
  matters: it controls how big those factors get."
- **Implementation**: `pgmpy.inference.VariableElimination` with explicit
  elimination order, a lightweight hand-rolled factor stepper for the teaching
  view, `pandas`, `seaborn`, `htutori.add_fitted_text_box()`

## Cell 3.3: Pruning Irrelevant Variables

- **Purpose**: Show that variables that are not ancestors of the query or
  evidence contribute nothing and can be removed before any computation
- **Display**:
  - The DAG with the query and evidence fixed
  - Nodes are shaded by relevance: ancestors of query-or-evidence are kept,
    everything else is faded and marked "irrelevant"
  - Beside it, the posterior computed on the full network vs the posterior on the
    pruned network, shown as identical bars
- **Interactive widget**:
  - Dropdown for query variable and evidence checkboxes
  - Toggle "prune irrelevant variables": switches between full and pruned
    network, with the operation count updating
  - For an extended network (add a leaf such as a non-evidence
    $Neighbor$ child of Alarm), students see that the leaf drops out when it is
    neither query nor evidence
- **Key insights**:
  - Any variable that is not an ancestor of the query or the evidence sums to 1
    and leaves the answer unchanged
  - Pruning is free correctness-preserving speedup done before the main
    algorithm runs
  - This is why an effect node we did not observe and are not asking about can be
    ignored
- **Comment box**: "If a variable is neither asked about, observed, nor an
  ancestor of something that is, it cannot affect the answer. Delete it first."
- **Implementation**: `networkx` ancestor computation, `plot_causal_dag()` with
  relevance shading, `pgmpy` inference on full vs reduced model

# Part 4: Complexity and Limits

## Cell 4.1: Complexity: Polytrees vs General Graphs

- **Purpose**: Make concrete the claim that exact inference is cheap on
  tree-shaped networks but blows up in general, so students know when exact
  methods are viable
- **Display**:
  - A 1x4 panel layout:
    - Panel 1: a polytree (chain/tree) network of adjustable size
    - Panel 2: a densely connected network of the same node count
    - Panel 3: line chart of operation count vs number of nodes $n$, one curve
      roughly linear ($O(n)$, polytree) and one roughly exponential ($O(2^n)$,
      dense), with a log-scaled y-axis
    - Panel 4: comments panel
  - The polytree curve and the exponential curve are visually distinct (solid vs
    a steeper solid line), annotated with their big-O labels
- **Interactive widget**:
  - Slider for number of nodes $n$
  - Dropdown for structure: "polytree" vs "fully connected"
  - Dropdown for elimination order quality: "good" vs "bad" (shows order changes
    the constant and even the growth on dense graphs)
  - The operation-count curves and the highlighted operating point update live
- **Key insights**:
  - On polytrees (singly connected networks) exact inference is $O(n)$
  - On general (multiply connected) networks cost can grow as $O(2^n)$: exact
    inference is NP-hard in the worst case
  - Elimination order strongly affects cost; finding the optimal order is itself
    hard
- **Comment box**: "Exact inference is fast when the network is tree-like and the
  intermediate factors stay small. Dense connectivity makes those factors
  explode, and cost grows exponentially."
- **Implementation**: `networkx` for structure generation, `seaborn` line plots
  with log y-axis, `ipywidgets` sliders and dropdowns,
  `htutori.add_fitted_text_box()`

## Cell 4.2: When Exact Inference Breaks Down

- **Purpose**: Summarize the boundaries of exact inference and motivate the
  approximate (sampling) methods covered next in the lecture
- **Display**:
  - A compact table contrasting three regimes:
    - Small discrete polytree: exact inference fast and recommended
    - Large densely connected discrete network: exact inference intractable, use
      approximate
    - Continuous variables: enumeration sums do not apply, need other methods
  - A small continuous-variable network sketch with a reminder that the
    summation $\sum_{\mathbf{y}}$ becomes an integral with no closed form
- **Interactive widget**:
  - Dropdown for "scenario": selects one of the three regimes and updates a
    recommendation banner ("exact" vs "approximate")
  - Toggle "discrete vs continuous" on a node to show the sum turning into an
    intractable integral
- **Key insights**:
  - Exact inference fails for large dense networks (exponential cost) and for
    continuous variables (sums become hard integrals)
  - These failures are exactly the motivation for Monte Carlo and MCMC sampling
  - Exact methods remain the gold-standard reference for validating approximate
    ones on small networks
- **Comment box**: "Exact inference is the right tool for small discrete,
  tree-like networks. When the graph is large and dense, or variables are
  continuous, switch to the approximate sampling methods covered next."
- **Implementation**: `pandas` comparison table, `plot_causal_dag()` sketch,
  `ipywidgets.Dropdown` and `ipywidgets.ToggleButton`
