---
name: bayesian_networks_pgmpy
description: Interactive Jupyter notebook outline for teaching Bayesian Networks with pgmpy
metadata:
  type: notebook_outline
  lesson: MSML610 Lesson 06.1
  libraries: pgmpy, matplotlib, ipywidgets
  domain: probabilistic_reasoning
---

# Bayesian Networks: Learning Through pgmpy

Interactive notebook outline teaching Bayesian Networks through hands-on exploration and visualization.

## Cell 3: Conditional Independence Intuition

- **Purpose**: Build intuition for conditional independence before formalizing it mathematically
- **Display**:
  - Two network structures side by side:
    - Left: Rain and Sprinkler as independent nodes
    - Right: Rain and Sprinkler both caused by Weather
  - Color intensity shows strength of dependence between variables
  - Heatmap showing correlation between Rain and Sprinkler under different observations
- **Interactive widget**:
  - Dropdown for "what do we observe?": nothing, Weather, WetGrass, or Weather+WetGrass
  - Heatmap updates to show new conditional correlation
  - Text displays: "Are Rain and Sprinkler independent given this observation? [Yes/No]"
- **Key insights**:
  - Variables can be dependent or independent depending on what we observe
  - Conditioning on Weather makes Rain and Sprinkler independent (confounder explanation)
  - Conditioning on WetGrass makes Rain and Sprinkler dependent (explaining away)
- **Comment box**:
  - Callout: "Observing the common cause (Weather) blocks correlation"
  - Callout: "Observing the effect (WetGrass) creates correlation between causes"
  - Key term: "Fork path (confounder) creates dependence, condition blocks it"
- **Implementation**: seaborn/matplotlib heatmap, ipywidgets Dropdown, numpy for correlation computation

## Cell 4: Building the Garden World Bayesian Network

- **Purpose**: Construct an actual Bayesian Network with pgmpy and specify conditional probability tables
- **Display**:
  - Network diagram showing: Weather -> Rain, Weather -> Sprinkler, Rain -> WetGrass, Sprinkler -> WetGrass
  - Color-coded nodes: parents in blue, effects in green
  - Display structure (nodes and edges) in text form
  - Show CPT values in formatted tables
- **Interactive widget**: None (demonstration code)
- **Key insights**:
  - Bayesian Networks encode conditional independence assumptions visually
  - Each node needs a CPT specifying P(node | parents)
  - Network structure is separate from numerical parameters
- **Comment box**:
  - "This network encodes: Weather is root cause, affects both Rain and Sprinkler independently"
  - "WetGrass depends only on Rain and Sprinkler, not on Weather directly"
- **Implementation**: pgmpy.models.BayesianNetwork, pgmpy.factors.discrete.TabularCPD

## Cell 5: Conditional Probability Tables Made Concrete

- **Purpose**: Understand how CPTs quantify relationships by showing them visually and interactively
- **Display**:
  - Multiple CPT visualizations side by side:
    - Weather (root node): simple bar chart, probabilities sum to 1
    - Rain given Weather: grouped bar chart showing P(Rain | Weather=sunny/cloudy/rainy)
    - WetGrass given Rain and Sprinkler: heatmap showing all 4 combinations
  - Rows sum to 1 are highlighted in green
- **Interactive widget**:
  - Slider for P(Rain | Weather=sunny): 0.0-1.0
  - Slider for P(Rain | Weather=rainy): 0.0-1.0
  - Other sliders for different CPT entries
  - Network diagram updates to reflect new probabilities
  - Display shows joint probability of sample scenarios (e.g., P(sunny, no rain, wet grass))
- **Key insights**:
  - CPT rows always sum to 1 (fundamental constraint)
  - Each row represents a different conditioning case
  - Probabilities reflect domain knowledge or data
  - Different CPT values produce different behavior
- **Comment box**:
  - "Each row answers: 'Given this parent state, what are the probabilities for this node?'"
  - Observation: "Changing a CPT value changes what the network believes"
- **Implementation**: matplotlib bar charts and heatmaps, ipywidgets FloatSlider, pandas for CPT display

## Cell 6: Inference 1: Joint Probability Queries

- **Purpose**: Show how Bayesian Networks compute joint probabilities and answer basic queries
- **Display**:
  - Network diagram highlighted with current query
  - Table showing joint probability P(W=w, R=r, S=s, G=g) for all 16 combinations
  - Bar chart of top 5 most likely joint configurations
  - Sorted in descending probability order
- **Interactive widget**:
  - Radio buttons for "select scenario": user picks values for all nodes
  - Displays computed P(selected scenario)
  - Highlights row in table with green background
  - Shows how this probability was computed from CPTs (show factorization)
- **Key insights**:
  - Joint probabilities are computed by multiplying CPT entries along the network
  - Most configurations have very low probability
  - Network structure enables efficient computation
- **Comment box**:
  - "P(W, R, S, G) = P(W) * P(R|W) * P(S|W) * P(G|R,S)"
  - Text: "The network factorizes the joint distribution"
- **Implementation**: pgmpy.inference.VariableElimination, pandas DataFrame

## Cell 7: Inference 2: Marginal Queries

- **Purpose**: Learn how to ask "what's the probability of just one variable?" without specifying others
- **Display**:
  - Side-by-side comparison:
    - Left: joint probabilities (16 rows)
    - Right: marginal distributions (one row per variable)
  - Animation or highlighting showing which joint rows sum to compute each marginal
  - Bar chart for each variable showing P(variable)
- **Interactive widget**:
  - Dropdown to select "which variable?": Weather, Rain, Sprinkler, WetGrass
  - Bar chart updates to show marginal distribution
  - Tooltip shows: "Computed by summing over all other variables"
  - Text displays factorization: "P(WetGrass) = sum over W,R,S of P(W,R,S,G)"
- **Key insights**:
  - Marginal probability is the answer without specifying other variables
  - Joint and marginal probabilities are related by summation
  - Most real queries are marginal (we don't know everything)
- **Comment box**:
  - "Marginalization: sum over unknowns to get the probability you care about"
  - Observation: "What's the probability it will rain? Answer: marginal P(Rain)"
- **Implementation**: pgmpy inference, numpy sum operations, matplotlib bar charts

## Cell 8: Inference 3: Conditional Probabilities (Basic)

- **Purpose**: Learn to query conditional probabilities P(X | Y=y) without evidence
- **Display**:
  - Three-panel comparison:
    - Panel 1: P(Rain) unconditional (prior)
    - Panel 2: P(Rain | Weather=sunny)
    - Panel 3: P(Rain | Weather=rainy)
  - Color bars show how belief changes with observation
  - Text overlay: "Prior: 0.27 -> Given sunny: 0.05 -> Given rainy: 0.90"
- **Interactive widget**:
  - Dropdown for "what do we observe?": Weather, Rain, Sprinkler, WetGrass
  - Dropdown for "observed value": (options depend on selected variable)
  - Third dropdown for "query variable": any variable not in observation
  - Bar chart updates showing conditional probability
  - Display: P(query | observation) = X%
- **Key insights**:
  - Observations change our belief about unobserved variables
  - Conditional probability is different from prior (unless independent)
  - Bayes' rule relates P(X|Y) to P(Y|X) and priors
- **Comment box**:
  - "Our belief about rain changes based on what weather we observe"
  - Highlight: "This is inference: using observations to update beliefs"
- **Implementation**: pgmpy.inference.VariableElimination with evidence parameter

## Cell 9: Inference 4: Reasoning with Multiple Observations

- **Purpose**: Show how multiple pieces of evidence combine to constrain beliefs
- **Display**:
  - Network diagram with highlighted evidence nodes (colored differently)
  - Three stages of belief update shown visually:
    - Stage 1: Prior P(Rain) = 0.27
    - Stage 2: After observing WetGrass: P(Rain | WetGrass=True) = 0.71
    - Stage 3: After observing Sprinkler=Off: P(Rain | WetGrass=True, Sprinkler=Off) = 0.94
  - Bar charts showing belief evolution
- **Interactive widget**:
  - Checkboxes for "evidence": Weather, Rain, Sprinkler, WetGrass
  - For each checked evidence, dropdown to select value
  - Query dropdown to select variable to reason about
  - Display shows P(query | all evidence)
  - "Evidence summary": lists all observations
  - "Belief change": shows numerical difference from prior
- **Key insights**:
  - Multiple observations can dramatically change beliefs
  - Evidence propagates through the network in both directions
  - Some evidence is more informative than others
  - Non-intuitive effects: observing one effect can make causes correlated (explaining away)
- **Comment box**:
  - "Wet grass is evidence for rain OR sprinkler"
  - Observation: "But knowing sprinkler is off increases rain probability significantly"
  - Term: "This is explaining away: one cause explains the effect, reducing belief in others"
- **Implementation**: pgmpy inference with multiple evidence values

## Cell 10: Explaining Away Phenomenon

- **Purpose**: Visualize and understand the counterintuitive "explaining away" effect
- **Display**:
  - Network diagram highlighting Rain and Sprinkler as causes, WetGrass as effect
  - Three-stage animation:
    - Stage 1: P(Rain | WetGrass) as bar chart
    - Stage 2: Add Sprinkler=True as evidence
    - Stage 3: P(Rain | WetGrass, Sprinkler=True) - notice it DECREASES
  - Heatmap showing P(Rain, Sprinkler | WetGrass) for all combinations
  - Color intensity shows high/low probability regions
- **Interactive widget**:
  - Slider for "probability of sprinkler being on": 0.0-1.0 (controls P(S|W))
  - Observe how this affects the "explaining away" magnitude
  - Slider for "P(Rain | W=rainy)": changes how likely rain is given weather
  - Display shows: "If rain is already very likely, sprinkler observation has less impact"
- **Key insights**:
  - Observing one cause of an effect reduces belief in alternative causes
  - This is conditional dependence between causes
  - Counterintuitive because Rain and Sprinkler are unconditionally independent
  - Explains why domain knowledge about causal structures matters
- **Comment box**:
  - "Rain and Sprinkler are independent normally, but dependent given WetGrass"
  - Insight: "Observing an effect 'explains away' other causes"
  - Technical term: "This occurs at collider nodes (nodes with multiple parents)"
- **Implementation**: pgmpy inference, matplotlib heatmaps, ipywidgets sliders

## Cell 11: The Burglar Alarm Network

- **Purpose**: Learn to build and reason with a more complex real-world Bayesian Network
- **Display**:
  - Network diagram: Burglary, Earthquake -> Alarm -> JohnCalls, MaryCalls
  - Each node labeled with its prior or CPT (concise notation)
  - Visual shows conditional independencies:
    - Burglary and Earthquake are independent (no edge between them)
    - JohnCalls depends only on Alarm (not directly on Burglary/Earthquake)
- **Interactive widget**: None (demonstration)
- **Key insights**:
  - Real networks can have multiple independent causes
  - Children of a node are conditionally independent given the node
  - Network structure encodes meaningful domain assumptions
- **Comment box**:
  - "John and Mary only know about the alarm, not about burglaries or earthquakes"
  - Design principle: "Children of a node depend on that node, not its parents"
- **Implementation**: pgmpy.models.BayesianNetwork construction

## Cell 12: Burglar Alarm Inference Scenario 1

- **Purpose**: Work through a realistic inference scenario: "I heard alarm, but John didn't call. What happened?"
- **Display**:
  - Four sequential stages:
    - Stage 1: "Heard the alarm" - network update showing P(B|A), P(E|A)
    - Stage 2: "John didn't call" - further update showing P(A|¬J)
    - Stage 3: Combined evidence - display P(B|A,¬J) and P(E|A,¬J)
    - Stage 4: Interpretation - show most likely scenario
  - Bar charts at each stage showing belief evolution
  - Narrative text: "Alarm is less likely, so both burglary and earthquake are less likely"
- **Interactive widget**: None (demonstration)
- **Key insights**:
  - Negative evidence (alarm didn't result in John's call) is informative
  - Can reason backwards: observations about effects constrain beliefs about causes
  - Multiple pieces of evidence combine multiplicatively (in a sense)
- **Comment box**:
  - "If the alarm actually rang, John would almost certainly call"
  - Reasoning: "John didn't call, so either alarm didn't ring or John didn't hear it"
  - Conclusion: "Burglary probability drops because alarm likelihood drops"
- **Implementation**: pgmpy inference with multiple evidence pieces

## Cell 13: Burglar Alarm Inference Scenario 2 (Interactive)

- **Purpose**: Explore the alarm network interactively, answering user-posed queries
- **Display**:
  - Network diagram on left (always visible, highlighting current evidence nodes)
  - Query panel on right with controls and results
  - Network displays current marginal probabilities for all nodes
  - Result shows P(query | evidence) as both percentage and bar chart
  - Narrative text explains the result in plain English
- **Interactive widget**:
  - Radio buttons for evidence: "I observe..." with options (Burglary, Earthquake, Alarm, JohnCalls, MaryCalls)
  - For each, dropdown to set value (True/False)
  - Button to "add more evidence" or "clear evidence"
  - Query dropdown: "What's the probability of..." (any unobserved variable)
  - "Explanation" button generates plain-English summary
- **Key insights**:
  - Different evidence leads to different conclusions
  - Can discover that some evidence is redundant given other evidence
  - Can find surprising conditional independencies
- **Comment box**:
  - Displays automatically based on query result
  - Examples: "Both calls make alarm more likely" or "Earthquake doesn't help predict calls"
- **Implementation**: pgmpy inference, ipywidgets interactive controls

## Cell 14: Building Networks from Domain Knowledge

- **Purpose**: Teach the methodology for constructing Bayesian Networks from scratch
- **Display**:
  - Three stages shown as diagrams:
    - Stage 1: "List variables" - nodes without edges
    - Stage 2: "Identify dependencies" - edges added based on causal reasoning
    - Stage 3: "Verify structure" - highlight conditional independencies encoded
  - Checklist of design principles displayed as text
- **Interactive widget**:
  - Text input: "suggest variables for this domain" (e.g., "diagnosing car problems")
  - Dropdown to select from common example domains
  - Visualization updates to show a network for that domain
  - User can toggle edges on/off and see what conditional independencies change
- **Key insights**:
  - Network topology should reflect domain causal structure
  - Must choose between "is this a direct dependency?" or "indirect through another variable?"
  - More connections mean more CPT parameters to estimate
  - Domain expertise determines network structure
- **Comment box**:
  - Design principles listed: "(1) Parents influence children directly, (2) No cycles, (3) Model only relevant variables, (4) Keep CPTs manageable"
  - Observation: "Too many edges = too many parameters; too few = poor predictions"
- **Implementation**: matplotlib for network visualization, ipywidgets for domain selection

## Cell 15: When Does a Network Fail?

- **Purpose**: Understand limitations of Bayesian Networks through failure cases
- **Display**:
  - Three failure scenarios shown visually:
    - Scenario 1: Missing confounder (hidden common cause)
    - Scenario 2: Cycles in the network (acyclicity violated)
    - Scenario 3: Incorrect conditional independence assumptions
  - For each, show what wrong predictions result
  - Contrast with correct network
- **Interactive widget**:
  - Dropdown to select "failure scenario"
  - Input field: user can adjust CPT values and see predictions change
  - Button to "reveal the mistake"
  - Visualization highlights the problem area
- **Key insights**:
  - Bayesian Networks assume acyclic structure
  - Missing variables can create spurious correlations
  - Incorrect structure leads to wrong inference
  - Domain knowledge is crucial for network validity
- **Comment box**:
  - "Always check: Are there unmeasured common causes?"
  - Warning: "Correlations in data don't prove causal direction"
  - Reminder: "Network edges represent domain assumptions, verify them"
- **Implementation**: matplotlib visualization, annotation of error regions
