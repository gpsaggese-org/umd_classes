# From Prediction to Decision: Causal AI for Machine Learning Practitioners

## Part I — Understanding Causality

### 1: From Prediction Pipelines to Decision Pipelines
[msml610/lectures_source/Lesson08.1-Causal_AI_intro.txt](https://github.com/gpsaggese/gpsaggese.github.io/tree/master/msml610/lectures/Lesson08.1-Causal_AI_intro.pdf)

- Introduction and Motivation
  - Background
  - What ML Systems Can and Cannot Tell You
- Why Causal AI Matters
  - Problems with Traditional AI
  - Optimization vs. Inference vs. Decision Theory
  - The Cost of Ignoring Causality
- Causal AI Fundamentals
  - The Ladder of Causation
  - Correlation vs. Causation Models
  - Data Science vs. Decision Science
- Causal AI in Business
  - Business Context and Motivation
  - The Causal AI Workflow
  - Explainability and Interpretability
- Tools and Tutorials
  - TUTORIAL: Introduction to causal modeling frameworks

### 2: Bayesian Networks
msml610/lectures_source/Lesson06.1-Bayesian_Networks.txt
msml610/lectures_source/Lesson06.2-Using_Bayesian_Networks.txt

- Logic-Based AI Under Uncertainty
  - Problem
  - Solution
  - Causal and Exhaustive Augmentation
- Probabilistic Reasoning
  - Full Joint Probability Distribution
  - Conditional Independence
  - Bayesian Networks
- Semantics and Construction of Bayesian Networks
  - Semantics of Bayesian Networks
  - Constructing a Bayesian Network
- Applications and Inference
  - Basic inference procedures
  - Exact vs. approximate inference
- Tools and Tutorials
  - TUTORIAL: Implementing Bayesian Networks in PyMC

### 3: Causal DAGs and Structural Models
[msml610/lectures_source/Lesson08.3-Do_Calculus.txt](https://github.com/gpsaggese/gpsaggese.github.io/tree/master/msml610/lectures/Lesson08.3-Do_Calculus.pdf)

- From Bayesian to Causal Networks
  - (Non-Causal) Bayesian Networks
  - Causal (Bayesian) Networks
  - Causal DAG
  - Examples: Tornado Warning, Ladder of Causation
- Structural Causal Models
  - Definition and Notation
  - Structural Causal Model: Sprinkler Example
  - From Graphs to Equations
- Variables and Relationships in Causal Models
  - Observed vs. Unobserved Variables
  - Endogenous vs. Exogenous Variables
  - Building a Causal DAG: Heart Attack Example
  - Weights and Relationships
- Special Variable Types
  - Mediator, Moderator, and Confounder Variables
  - Collider and Collider Bias
  - Chain Structures and Path Types
- Tools and Tutorials
  - TUTORIAL: Building causal DAGs with domain experts
  - TUTORIAL: Visualizing and validating causal structures

### 4: From Causal Models to Code
msml610/lectures_source/Lesson07.1-Intro_to_Probabilistic_Programming.txt
msml610/lectures_source/Lesson07.2-Posterior_Based_Decisions.txt
msml610/lectures_source/Lesson07.3-Hierarchical_Models.txt
msml610/lectures_source/Lesson07.4-Generalized_Linear_Models.txt
msml610/lectures_source/Lesson07.5-Bayesian_Model_Comparison.txt

- From Theory to Implementation
  - Exact Inference in Bayesian Networks
  - Approximate Inference in Bayesian Networks
- Probabilistic Models in Practice
  - Generalized Linear Models
  - Hierarchical Models
- Decision Making with Posteriors
  - Posterior-Based Decisions
  - Bayesian Model Comparison
- Tools and Tutorials
  - TUTORIAL: PyMC (inference, diagnostics, and posterior workflows)

## Part II — Estimating Causal Effects

### 5: Interventions, Experiments, and Adjustments
// Ref: TBD

- From Observation to Intervention
  - Interventions in Causal Networks
  - Counterfactuals: What if we intervene?
  - Why experiments are the gold standard
- Randomized Controlled Trials
  - What is a Randomized Controlled Trial?
  - Randomized Controlled Trial: Example
  - When RCTs are not feasible
- Observational Adjustment and Identification Methods
  - Back-Door Paths and Confounding
  - Back-Door Adjustment: The Framework
  - Back-Door Criterion and Common Mistakes
  - Front-Door Adjustment: Cereal and Ads Example
- Do-Calculus: A Complete Framework
  - Do-Calculus Fundamentals
  - The Rules of Do-Calculus
  - Back/Front-door Adjustments and Do-calculus
  - When Do-Calculus Tells You Estimation Is Impossible
- Tools and Tutorials
  - TUTORIAL: DoWhy (do-calculus and adjustment methods)

### 6: Causal Identification and Estimation
[msml610/lectures_source/Lesson08.3-Do_Calculus.txt](https://github.com/gpsaggese/gpsaggese.github.io/tree/master/msml610/lectures/Lesson08.3-Do_Calculus.pdf)
msml610/lectures_source/Lesson08.4.txt

- The Identification Problem
  - When can we estimate causal effects from observational data?
  - Identifiable vs. unidentifiable causal effects
  - Foundational Assumptions: causal sufficiency, positivity, consistency, SUTVA
- Classical Identification Strategies
  - Instrumental variables and natural experiments
  - Regression discontinuity design (RDD)
  - Difference-in-differences (DiD)
  - Selection Bias and Confounding: why observational data is biased
- Estimation Methods and Robustness
  - Matching and propensity score methods
  - Regression adjustment and doubly robust estimation
  - Causal forests and meta-learners (S/T/X/R-learners)
  - Unmeasured confounding: Rosenbaum bounds and E-values
  - Refutation methods: placebo tests, data subset, causal model validation
- Heterogeneous Treatment Effects and Sensitivity
  - Average treatment effect (ATE) vs. conditional ATE (CATE)
  - Uplift modeling and targeting strategies
  - Validation and Robustness Checks
- Case Study: Healthcare Treatment Effect Estimation
  - Workflow: DAG → method selection → robustness checks
  - When estimates differ across methods and why
- Tools and Tutorials
  - TUTORIAL: EconML (policy learning and heterogeneous effects)
  - TUTORIAL: CausalML (propensity scores and meta-learners)
  - TUTORIAL: DoWhy (end-to-end causal analysis)

### 7: Explainability and Causal Attribution
[msml610/lectures_source/Lesson11-Probabilistic_deep_learning.txt](https://github.com/gpsaggese/gpsaggese.github.io/tree/master/msml610/lectures/Lesson11-Probabilistic_deep_learning.pdf)

- The Core Problem: Explanation vs. Causality
  - Why practitioners reach for explainability first
  - The promise and pitfalls of post-hoc interpretation
  - When explainability is sufficient and when you need causality
- Explanation Methods (Overview)
  - Model-specific interpretability: linear models, trees, GAMs
  - Model-agnostic methods: PDP, ALE, ICE, feature importance
  - SHAP: Shapley values and correct interpretation
  - LIME: local linear approximations and their limits
- The Critical Gap: Correlation vs. Causation
  - Feature importance is not causality
  - Correlation masquerades as contribution
  - Why post-hoc explanations can mislead decision-makers
  - Common mistakes: confusing prediction vs. intervention
- Causal Attribution Methods
  - Counterfactual explanations: "what if" reasoning
  - Causal SHAP: extending Shapley values with causal structure
  - Contrasting causal effects with feature importance
  - Actionable recourse: guiding changes that actually matter
- Decision Support and Real-World Application
  - Using explainability to identify potential causal relationships
  - From "what does the model rely on?" to "what should we intervene on?"
  - Case study: credit decision (why explaining rejection isn't the same as fixing bias)
- Tools and Tutorials
  - TUTORIAL: SHAP and LIME (interpretation frameworks)
  - TUTORIAL: DiCE and DoWhy (causal attribution)

### 8: Causal Inference for Time Series
[msml610/lectures_source/Lesson10-Timeseries_forecasting.txt](https://github.com/gpsaggese/gpsaggese.github.io/tree/master/msml610/lectures/Lesson10-Timeseries_forecasting.pdf)

- Time Series vs. Cross-Sectional Causality
  - Temporal causal structures
  - Challenges specific to time series
  - When temporal structure helps and when it misleads
- Granger Causality
  - Definition and intuition
  - Assumptions and limitations
  - Practical examples
- Interrupted Time Series (ITS)
  - Design and estimation
  - ITS and regression discontinuity
  - Applications in causal inference
- Difference-in-Differences (DiD)
  - Parallel trends assumption
  - Estimation and robustness
  - Extensions: multiple time periods
- Synthetic Control Methods
  - Constructing a counterfactual from donor series
  - Weighted combinations and optimal weights
  - When synthetic control succeeds and fails
- Tools and Tutorials
  - TUTORIAL: CausalImpact (Bayesian interrupted time series)
  - TUTORIAL: CausalPy (DiD and synthetic control)

### 9: A/B Testing and Experimentation
[msml610/lectures_source/Lesson09.3-Multi_Armed_Bandits.txt](https://github.com/gpsaggese/gpsaggese.github.io/tree/master/msml610/lectures/Lesson09.3-Multi_Armed_Bandits.pdf)

- Randomization as Causal Identification
  - Why randomization breaks confounding
  - Causal graphs of randomized experiments
- A/B Testing in Practice
  - Classic A/B test design and power analysis
  - Switchback experiments and temporal structures
  - Multi-armed bandits: balancing exploration vs. exploitation
  - The limits of standard A/B testing
- When to Experiment vs. Observe
  - Feasibility constraints: cost, time, ethics
  - When observational methods are necessary
  - Hybrid approaches: experiments + causal methods
- Tools and Tutorials
  - TUTORIAL: CausalML (A/B test analysis)
  - TUTORIAL: CausalPy (Bayesian experiment design)

### 10: Causal Discovery
- The Discovery Problem: When and Why It Works
  - Inferring causal structure from observational data
  - Identifiability and causal sufficiency: what assumptions are required?
  - Practical limitations of automated discovery
- When to Use Discovery vs. Domain Knowledge
  - Discovery as hypothesis generation, not conclusion
  - Using partial domain information to constrain the search
  - Combining automated discovery with expert judgment
- Discovery Algorithm Families
  - Constraint-based methods: PC algorithm, FCI
  - Score-based methods: GES, NOTEARS
  - Non-Gaussian methods: LiNGAM (exploiting non-Gaussianity)
- Challenges and Validation
  - Why Standard ML Fails at Causal Discovery
  - Multiple models produce identical predictions
  - Distinguishing different causal structures requires assumptions
  - Domain expert review and refutation testing
  - When discovery should change (and not change) your DAG
- Tools and Tutorials
  - TUTORIAL: causal-learn (constraint and score-based discovery)
  - TUTORIAL: LiNGAM (non-Gaussian causal discovery)

## Part III — Making Decisions with Causality

### 11: Decision-Making with Causal Models
[msml610/lectures_source/Lesson09.3-Multi_Armed_Bandits.txt](https://github.com/gpsaggese/gpsaggese.github.io/tree/master/msml610/lectures/Lesson09.3-Multi_Armed_Bandits.pdf)

- Why Prediction Is Not Enough
  - Prediction pipelines vs. decision pipelines
  - When prediction fails: Simpson's paradox, confounding, and policy reversal
  - Causal models as the foundation for decisions
- Foundations of Decision Theory
  - Utility functions and expected utility
  - Causal interventions and their expected outcomes
  - Risk preferences and multi-criteria trade-offs
- Decision Support with Causal Models
  - Influence diagrams: adding decisions and utility nodes to causal DAGs
  - Bayesian decision-making: posteriors to optimal actions
  - Prior elicitation: specifying beliefs about causal effects
- Sequential Decision-Making and Active Learning
  - Value of information: when to gather more data before deciding
  - Exploration vs. exploitation with causal learning
  - Thompson sampling and Bayesian optimization for experimentation
- Uncertainty in Causal Decisions
  - Aleatoric uncertainty: irreducible randomness
  - Epistemic uncertainty: model misspecification
  - Communicating uncertainty to stakeholders
- Tools and Tutorials
  - TUTORIAL: PyMC (causal inference and posterior-based decisions)
  - TUTORIAL: BoTorch (Bayesian optimization for sequential decisions)

### 12: Causal Reinforcement Learning

- Why Standard RL Fails
  - MDPs assume no confounding and stable environments
  - When RL produces brittle, non-generalizable policies
  - Distribution shift and out-of-distribution failures
  - How causal structure improves robustness and transfer
- Causal Dynamics Models
  - Learning causal transition models instead of black-box predictors
  - Model-based RL: building environment models that generalize
  - Integrating domain knowledge about causal structure
- Offline RL and Causal Corrections
  - Learning from logged data without experiments
  - Addressing confounding in offline settings
  - Off-policy evaluation with causal adjustments
- Policy Learning with Causal Effects
  - Learning policies from causal effect estimates
  - Heterogeneous treatment effects in policy optimization
  - Counterfactual policy evaluation before deployment
- Tools and Tutorials
  - TUTORIAL: gymnasium (RL environments)
  - TUTORIAL: d3rlpy (offline RL with causal considerations)

### 13: Forecasting Under Causal Intervention

- Why Standard Forecasting Breaks
  - Standard methods assume stationarity
  - Structural breaks and regime changes under intervention
  - When past patterns don't predict future outcomes
- Causal Constraints on Forecasts
  - Using causal models to validate forecasts
  - Forecasting demand under new pricing policies
  - Causal models as constraints on valid predictions
- Bayesian Forecasting with Causal Models
  - Generating forecasts from posterior causal models
  - Propagating causal uncertainty into prediction intervals
  - Posterior predictive checks: validating model assumptions
- Forecasting Spillover Effects
  - Joint distributions of multiple outcomes under intervention
  - Indirect consequences and second-order effects
  - Validating multivariate causal forecasts
- Tools and Tutorials
  - TUTORIAL: PyMC (posterior predictive validation)
  - TUTORIAL: Prophet (structural time series with interventions)

### 14: Causal Decision Making in Practice
[msml610/lectures_source/Lesson08.5-Causal_AI_In_Business.txt](https://github.com/gpsaggese/gpsaggese.github.io/tree/master/msml610/lectures/Lesson08.5-Causal_AI_In_Business.pdf)

- From Learning to Deployment
  - Bridging causal inference and business decisions
  - When prediction fails: Simpson's paradox and policy reversal
  - Causal models as decision support tools
- Policy Learning and Optimization
  - Learning optimal policies from causal effects
  - Heterogeneous effects: matching interventions to individuals
  - Uplift and targeting strategies
  - Adapting policies to different populations
- Real-World Applications
  - Marketing: targeting customers with causal uplift models
  - Healthcare: treatment guidelines from observational data
  - Operations: resource allocation with causal constraints
  - Pricing: demand models informed by causal dynamics
  - HR: hiring and retention driven by causal insights
- Validation and Continuous Learning
  - A/B testing policy recommendations
  - Off-policy evaluation before full deployment
  - Monitoring assumptions and adapting when they break
  - Iterative improvement of decision systems
- Tools and Tutorials
  - TUTORIAL: DoWhy (policy evaluation and decision support)
  - TUTORIAL: EconML (policy optimization and uplift)

### 15: Causal Reasoning in AI Systems

- LLMs and Causal Reasoning
  - Where LLMs excel: pattern matching at scale
  - Where they fail: explicit causal reasoning and counterfactuals
  - Limitations of pattern-based reasoning for intervention
  - Robustness: when causal misunderstanding leads to bad decisions
- Enhancing LLM Reasoning
  - Chain-of-thought prompting for structured causal reasoning
  - Connecting LLMs to causal and probabilistic frameworks
  - Tool use: integrating causal inference tools into agent workflows
- Causal Agent Architectures
  - Agents with explicit causal models in their reasoning
  - Integrating causal inference into planning and action selection
  - Planning under causal uncertainty: generating robust policies
- Trustworthy AI Through Causality
  - Transparency: making reasoning explicit and interpretable
  - Robustness: using causal structure to find brittle decisions
  - Fairness: causal approaches to bias and discrimination
  - Safety: causal constraints on harmful outcomes
- Tools and Tutorials
  - TUTORIAL: LangChain + DoWhy (causal reasoning in agents)
  - TUTORIAL: ReAct (reasoning and acting with causal structure)
  - TUTORIAL: LlamaIndex (knowledge-grounded reasoning)
