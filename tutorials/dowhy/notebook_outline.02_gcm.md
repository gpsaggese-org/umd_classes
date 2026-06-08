# Notebook Outline: Graphical Causal Models (GCMs) and Structural Causal Models

## Learning Objectives

By the end of this notebook, students will be able to:

- Understand the components of a graphical causal model (DAG and causal mechanisms)
- Distinguish between probabilistic and structural causal models
- Build and specify causal models using domain knowledge
- Fit a structural causal model (SCM) to real data
- Generate synthetic samples from a fitted causal model
- Evaluate the quality of a fitted model
- Customize causal mechanism assignments for specific problem domains
- Estimate confidence intervals for causal quantities
- Apply GCMs to root cause analysis and counterfactual reasoning

## Cell 1: What are Graphical Causal Models? (Markdown + Visualization)

**Purpose**: Build intuition about GCMs and their components

**Content Description**:

- Visual explanation: A GCM has two parts
  - A directed acyclic graph (DAG) showing causal structure
  - A causal mechanism for each node describing how it depends on parents
- Intuitive example: Health outcome model with age, diet, exercise, genetics
  - Show the DAG structure
  - Explain mechanisms in plain language (e.g., "health depends on diet and exercise")
- Contrast with statistical models: SCM captures causality, not just correlation
- Distinguish between probabilistic causal models (PCM) and structural causal models (SCM)
  - PCMs encode joint distributions
  - SCMs enable counterfactual reasoning via causal mechanisms

**Expected Output**:

- Clear DAG visualization with labeled nodes and edges
- Side-by-side comparison of correlation vs. causation thinking
- Intuitive explanation of why mechanisms matter beyond just the graph structure

## Cell 2: Building a Simple GCM by Hand (Code + Visualization)

**Purpose**: Learn the basic workflow of constructing a causal model

**Content Description**:

- Create a simple SCM with 3-4 variables using domain knowledge
- Define the causal graph explicitly (e.g., weather → activity, temperature → ice cream sales)
- Specify causal mechanisms manually using simple functions
  - Linear mechanisms: `child = a * parent1 + b * parent2 + noise`
  - Demonstrate how to write mechanisms as Python functions
- Visualize the resulting DAG
- Generate samples from the model

**Key Variables**:

- Simple dataset with 3-4 variables
- Manually defined mechanism functions
- DAG structure as adjacency matrix or networkx graph

**Expected Output**:

- A clean visualization of the DAG
- Sample data generated from the mechanisms
- Print statements showing sample relationships (e.g., "When temperature increases, ice cream sales increase")

## Cell 3: Automatic Mechanism Assignment (Code)

**Purpose**: Understand how to let DoWhy automatically assign mechanisms

**Content Description**:

- Load a real dataset (e.g., Sachs et al. protein signaling data or synthetic UCI dataset)
- Create a causal graph based on domain knowledge or prior discovery
- Use DoWhy's automatic mechanism assignment
  - Explore different mechanism types available: linear, polynomial, neural network, etc.
  - Show how DoWhy infers reasonable mechanisms from data
- Visualize the assigned mechanisms and their assumed functional forms
- Discuss the trade-offs: automatic assignment is fast but may not capture domain knowledge

**Key Variables**:

- Real dataset with known or assumed causal structure
- Causal graph specification (from domain knowledge or discovery)
- Mechanism type selection

**Expected Output**:

- Visualization showing assigned mechanisms for each node
- Summary of mechanism types and their mathematical forms
- Comparison with hand-specified mechanisms from Cell 2

## Cell 4: Fitting an SCM to Data (Code)

**Purpose**: Learn how to estimate model parameters from observed data

**Content Description**:

- Take the SCM from Cell 3 with automatically assigned mechanisms
- Fit the model to the data using DoWhy's `fit()` method
- Explain the fitting process: estimate parameters of each mechanism independently (sequential fitting)
- Show convergence and fitting quality diagnostics
- Visualize parameter estimates and uncertainty

**Key Variables**:

- Dataset with continuous variables
- SCM with assigned mechanisms
- Fitting method (default sequential fitting)

**Expected Output**:

- Fitted model parameters
- Diagnostic plots showing fit quality for each mechanism
- Summary statistics of parameter estimates

## Cell 5: Generating Samples from a Fitted Model (Code + Visualization)

**Purpose**: Understand how to use a fitted model for synthetic data generation

**Content Description**:

- Generate synthetic samples from the fitted SCM
- Interactive widget: adjust sample size and noise levels, regenerate samples
- Compare synthetic samples with original data
  - Overlaid distributions
  - Summary statistics comparison
  - Scatter plots of relationships between variables
- Build intuition about what the model learned from the data

**Key Variables**:

- Sample size (e.g., 100, 500, 1000 samples)
- Optional noise perturbation
- Number of generated samples

**Expected Output**:

- Synthetic dataset with same dimensionality as original
- Visual comparison: original vs. generated data distributions
- Summary statistics showing alignment between original and synthetic

## Cell 6: Evaluating Model Quality (Code + Visualization)

**Purpose**: Learn systematic ways to assess whether a fitted model captures the data well

**Content Description**:

- Multiple evaluation metrics for fitted GCMs
  - Residual analysis: check if residuals are independent and zero-mean
  - Goodness of fit: compare predicted vs. actual values
  - Marginal distribution matching: how well does the model match empirical distributions
- Run model evaluation using DoWhy's evaluation toolkit
- Interactive widget: select evaluation metric and variable to inspect
- Highlight problematic mechanisms or variables that don't fit well

**Key Variables**:

- Fitted SCM
- Evaluation metric selection
- Variable selection for detailed inspection

**Expected Output**:

- Evaluation report with scores for each mechanism
- Diagnostic plots (residuals, Q-Q plots, prediction errors)
- Summary identifying which variables fit well and which are problematic

## Cell 7: Confidence Intervals for Causal Estimates (Code)

**Purpose**: Understand uncertainty in causal quantities from a fitted model

**Content Description**:

- Explain why confidence intervals matter: parameter estimates have uncertainty
- Use bootstrap or analytical methods to estimate confidence intervals
- Demonstrate on a concrete causal quantity (e.g., average treatment effect)
- Visualize confidence intervals and interpret their meaning
- Interactive widget: select causal quantity and sample size, compute confidence intervals

**Key Variables**:

- Fitted SCM
- Treatment variable and outcome of interest
- Intervention specification (e.g., fix variable to a value)
- Number of bootstrap samples or analytic method

**Expected Output**:

- Confidence intervals for point estimates
- Visualization: point estimates with error bars
- Interpretation statement (e.g., "With 95% confidence, the effect is between X and Y")

## Cell 8: Customizing Causal Mechanism Assignment (Code)

**Purpose**: Learn how to incorporate domain knowledge into mechanism specification

**Content Description**:

- Show scenarios where automatic mechanism assignment is insufficient
  - Domain expert knows mechanisms are nonlinear
  - Prior knowledge suggests specific functional forms
  - Physics or subject matter theory constrains the relationship
- Demonstrate custom mechanism assignment
  - Define custom mechanism functions (e.g., exponential, sigmoidal)
  - Mix automatic and custom mechanisms in same model
  - Validate that custom mechanisms make sense for the domain
- Compare models with automatic vs. custom mechanisms

**Key Variables**:

- Domain knowledge about specific mechanisms
- Custom mechanism functions as Python callables
- Dataset for fitting

**Expected Output**:

- Fitted model with custom mechanisms
- Comparison plots showing how custom mechanisms differ from automatic ones
- Evaluation metrics comparing model quality

## Cell 9: Root Cause Analysis Example (Code + Interactive)

**Purpose**: Apply GCMs to a realistic problem: microservice troubleshooting

**Content Description**:

- Realistic scenario: API latency increases, need to identify root cause
- Dataset: latency measurements + system metrics (CPU, memory, network, database queries)
- Build a GCM from domain knowledge about system behavior
- Fit the model to normal operations data
- Detect anomaly by generating samples under different intervention scenarios
- Interactive widget: set suspected root causes, see predicted latency impact
- Identify which intervention would most reduce latency

**Key Variables**:

- System metrics dataset
- Causal model specification from infrastructure knowledge
- Intervention scenarios (e.g., increase resources, optimize queries)

**Expected Output**:

- Fitted causal model of system behavior
- Counterfactual predictions showing impact of each intervention
- Recommendation of which variable to intervene on for maximum benefit

## Cell 10: Medical Counterfactual Example (Code + Interactive)

**Purpose**: Apply GCMs to healthcare: personalized causal reasoning

**Content Description**:

- Realistic scenario: patient with specific risk factors, need to predict treatment effect
- Dataset: medical records with patient characteristics, treatments, outcomes
- Build GCM encoding causal relationships in healthcare (confounding, treatment effects)
- Fit model to historical data
- Use model to answer counterfactual questions
  - "What would this patient's outcome be under treatment A vs. treatment B?"
  - "Which patient characteristics most influence treatment effectiveness?"
- Interactive widget: adjust patient characteristics, see updated counterfactual predictions

**Key Variables**:

- Patient demographic and clinical variables
- Treatment variable
- Outcome of interest
- Patient profile specification

**Expected Output**:

- Fitted healthcare causal model
- Counterfactual predictions for personalized treatment
- Sensitivity analysis: which variables most influence the outcome

## Cell 11: Model Limitations and When GCMs Fail (Markdown + Code)

**Purpose**: Understand assumptions and failure modes

**Content Description**:

- Key assumptions underlying GCMs
  - Causal Markov condition: variables conditionally independent given parents
  - Causal sufficiency: no hidden confounders
  - Acyclicity: no feedback loops in the DAG
  - Mechanism autonomy: mechanisms don't change when other nodes intervene
- Demonstrate consequences when assumptions are violated
  - Example 1: unmeasured confounder (violates sufficiency)
  - Example 2: feedback loop (violates acyclicity)
  - Example 3: nonlinear mechanism fit with linear model
- Discuss practical implications and mitigation strategies

**Expected Output**:

- Clear explanation of assumptions with visual examples
- Demonstrations of what happens when assumptions fail
- Guidance on when to use GCMs vs. other methods

## Cell 12: Putting It All Together (Code + Interactive Project)

**Purpose**: Integrate all concepts in a comprehensive applied example

**Content Description**:

- Open-ended project: student chooses a domain (e.g., e-commerce conversion, supply chain, environmental monitoring)
- Workflow summary:
  1. Define causal graph from domain knowledge or discovery
  2. Specify or customize mechanisms
  3. Fit the model to available data
  4. Evaluate model quality and identify weak points
  5. Generate counterfactual predictions for decision-making
- Interactive dashboard: adjust model components and see downstream effects
- Reflection prompts: What would you improve? What assumptions are you uncertain about?

**Key Variables**:

- Choice of application domain
- Domain-specific data and causal knowledge
- Intervention scenarios of interest

**Expected Output**:

- Fully specified and fitted SCM for chosen domain
- Model evaluation report
- Counterfactual analysis addressing a decision question
- Reflection on model assumptions and limitations
