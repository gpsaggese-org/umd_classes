# From Prediction to Decision: Causal AI for Machine Learning Practitioners

## Part I — Foundations of Causal Inference

### 1: From Prediction Pipelines to Decision Pipelines
[msml610/lectures_source/Lesson08.1-Causal_AI_intro.txt](https://github.com/gpsaggese/gpsaggese.github.io/tree/master/msml610/lectures/Lesson08.1-Causal_AI_intro.pdf)

- Introduction and Motivation
  - Background
  - What ML Systems Can and Cannot Tell You
- Why Causal AI Matters
  - Problems with Traditional AI
  - Optimization vs. Inference vs. Decision Theory
  - The Cost of Ignoring Causality
  - Data Science vs. Decision Science
- Causal AI Fundamentals
  - The Ladder of Causation
  - Correlation vs Causation Models
- Causal AI in Business
  - Business Context and Motivation
  - The Causal AI Workflow
  - Explainability and Interpretability

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
- Semantics of Bayesian Networks
- Constructing a Bayesian Network

### 3: Probabilistic Programming
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

### 4: Causal DAGs and Structural Models
[msml610/lectures_source/Lesson08.3-Do_Calculus.txt](https://github.com/gpsaggese/gpsaggese.github.io/tree/master/msml610/lectures/Lesson08.3-Do_Calculus.pdf)

- From Bayesian to Causal Networks
  - (Non-Causal) Bayesian Networks
  - Causal (Bayesian) Networks
  - Causal DAG
  - Example of ladder of causation
  - Example: Tornado Warning
- Structural Causal Models
  - Definition and Notation
  - Structural Causal Model: Sprinkler Example
  - From Graphs to Equations
- Variables in Causal Models
  - Observed Vs. Unobserved Variables
  - Endogenous Vs. Exogenous Variables
  - Building a Causal DAG
  - Heart Attack: Example
  - Weights and Relationships
- Special Variable Types
  - Mediator Variable
  - Moderator Variable
  - Confounder Variable
  - Collider
  - Collider Bias
- Causal Paths and Structures
  - Types of Paths in Causal AI
  - Fork Structure
  - Inverted Fork

## Part II — Causal Methods in Practice

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
- Observational Adjustment Methods
  - Back-Door Paths and Confounding
  - Back-Door Adjustment: The Framework
  - Back-Door Criterion: Overview
  - Chains, Forks, and Colliders
  - Common Mistakes in Back-Door Adjustment
  - When Back-Door Adjustment Fails
- Front-Door Adjustment
  - Front-Door Adjustment in Causal Inference
  - Example: Cereal and Ads
- Do-Calculus: A Complete Framework
  - Do-Calculus Fundamentals
  - The Rules of Do-Calculus
  - Back/Front-door Adjustments and Do-calculus
  - When Do-Calculus Tells You Estimation Is Impossible

### 6: Causal Identification and Estimation
[msml610/lectures_source/Lesson08.3-Do_Calculus.txt](https://github.com/gpsaggese/gpsaggese.github.io/tree/master/msml610/lectures/Lesson08.3-Do_Calculus.pdf)

- The Identification Problem
  - When can we estimate causal effects from data?
  - Identifiable vs. Unidentifiable Causal Effects
- Classical Identification Strategies
  - Instrumental variables and natural experiments
  - Regression discontinuity design
  - Difference-in-differences approach
- Selection Bias and Its Consequences
  - Selection bias mechanisms
  - Why standard estimates fail under selection

- Average treatment effect (ATE) and conditional ATE (CATE)
- Matching methods and propensity scores
- Regression adjustment and doubly robust methods
- Uplift modeling and heterogeneous treatment effects
- Application: healthcare observational studies and treatment effect estimation
- TUTORIAL: EconML (double ML, causal forests, and meta-learners for ATE/CATE estimation)
- TUTORIAL: CausalML (propensity scoring, matching, and uplift estimation)
- Why causal estimates can be fragile
- Unmeasured confounding and its consequences
- Rosenbaum bounds and E-values
- Refutation methods: random common cause, data subset, placebo treatment
- How to know if your causal model is wrong
- TUTORIAL: DoWhy (built-in refutation tests and sensitivity analysis)

### 7: Causal Discovery and Machine Learning
// Ref: TBD

- Constraint-based methods: PC algorithm and FCI
- Score-based methods: GES, NOTEARS
- LiNGAM and non-Gaussian methods
- Granger causality and state space representations
- Practical limitations and when discovery fails
- TUTORIAL: causal-learn (PC algorithm, GES, and constraint-based discovery)
- TUTORIAL: LiNGAM (linear non-Gaussian causal model discovery)
- Why standard ML fails at causal questions
- Double machine learning: combining ML with causal inference
- Meta-learners: S-learner, T-learner, X-learner, R-learner
- Causal forests and nonparametric methods
- Heterogeneous treatment effects in practice
- TUTORIAL: EconML (double ML, causal forests, S/T/X-learners, HTE estimation)
- TUTORIAL: CausalML (meta-learners and heterogeneous treatment effect estimation)

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
  - TUTORIAL: CausalImpact (Bayesian interrupted time series for causal inference)
  - TUTORIAL: CausalPy (DiD and synthetic control with Bayesian models)


### 9: Explainability Methods: What They Do and Do Not Tell You
[msml610/lectures_source/Lesson11-Probabilistic_deep_learning.txt](https://github.com/gpsaggese/gpsaggese.github.io/tree/master/msml610/lectures/Lesson11-Probabilistic_deep_learning.pdf)

- Why Practitioners Reach for Explainability First
  - Black box models, regulation, and trust
  - The promise and pitfalls of interpretation
- Model-Specific Interpretability
  - Linear models: coefficients as explanations
  - Decision trees and rule-based models
  - Generalized additive models (GAMs)
- Model-Agnostic Explanation Methods
  - Partial dependence plots (PDP) and accumulated local effects (ALE)
  - Individual conditional expectation (ICE)
  - Feature importance: Gini, permutation, and others
  - Local vs. global explanations
- SHAP: Shapley Values in Machine Learning
  - Shapley values: from game theory to ML
  - TreeSHAP, KernelSHAP, DeepSHAP implementations
  - Interpreting SHAP values correctly
  - When SHAP is causal and when it is not
  - TUTORIAL: SHAP (explaining black-box model predictions with Shapley values)
- LIME: Local Linear Approximations
  - How LIME works
  - When to trust local explanations
  - TUTORIAL: LIME (local interpretable model-agnostic explanations)
- The Gap Between Explanation and Causation
  - Feature importance is not causality
  - Why post-hoc explanations can mislead
  - When explainability is sufficient and when causal reasoning is needed
- Causal SHAP and causal attribution methods
- Counterfactual explanations and actionable recourse
- Why explainability methods must be interpreted through a causal lens
- Contrasting causal effects with feature importance
- TUTORIAL: DiCE (diverse counterfactual explanations and algorithmic recourse)
- TUTORIAL: DoWhy (contrasting causal effect with feature importance)

### 10: A/B Testing and Experimentation
[msml610/lectures_source/Lesson09.3-Multi_Armed_Bandits.txt](https://github.com/gpsaggese/gpsaggese.github.io/tree/master/msml610/lectures/Lesson09.3-Multi_Armed_Bandits.pdf)

- Randomization as Causal Identification
  - Why randomization breaks confounding
  - Randomization and its relationship to causal identification
  - Causal graphs of randomized experiments
- A/B Testing in Practice
  - Classic A/B test design and power analysis
  - Switchback experiments and temporal structures
  - Multi-armed bandits and exploration vs. exploitation
  - The limits of standard A/B testing
- Observational vs. Experimental Methods
  - When experiments are feasible
  - When to use observational causal methods
  - Hybrid approaches
- Heterogeneous Treatment Effects and Uplift
  - Uplift modeling: finding who benefits most
  - Conditional average treatment effects (CATE)
  - Targeted interventions: matching effects to populations
  - Applications: marketing uplift, customer interventions, campaign analysis
- Policy Evaluation
  - Off-policy evaluation from experiments
  - Offline policy learning
- Tools and Tutorials
  - TUTORIAL: CausalML (uplift modeling and A/B test analysis)
  - TUTORIAL: CausalPy (causal effect estimation with Bayesian models)

## Part III — Decision-Making Under Uncertainty

### 11: Decision Theory and Bayesian Decision Making
[msml610/lectures_source/Lesson09.3-Multi_Armed_Bandits.txt](https://github.com/gpsaggese/gpsaggese.github.io/tree/master/msml610/lectures/Lesson09.3-Multi_Armed_Bandits.pdf)

- Foundations of Decision Theory
  - Utility theory and loss functions
  - Expected utility maximization
  - Risk preferences and risk-aware decisions
  - Multi-criteria decisions and trade-offs
- Bayesian Approach to Decision Making
  - Statistical decision theory
  - Bayes optimal decisions
  - Bayesian inference and posterior-based decisions
  - Prior elicitation and specification
- Sequential Decision Making Under Uncertainty
  - Thompson sampling: intuition and implementation
  - Bayesian optimization for expensive functions
  - Multi-armed bandits and adaptive allocation
- Uncertainty Quantification for ML Practitioners
  - Aleatoric vs. epistemic uncertainty
  - Confidence intervals vs. prediction intervals
  - Calibration and coverage
  - Communicating uncertainty to stakeholders
- Bayesian Hypothesis Testing
  - Bayesian testing vs. frequentist testing
  - Bayes factors and evidence
  - Sequential testing and adaptive designs
- Tools and Tutorials
  - TUTORIAL: PyMC (Bayesian inference, uncertainty quantification, and posterior-based decisions)
  - TUTORIAL: BoTorch (Bayesian optimization for sequential decision making)

### 12: Reinforcement Learning and Sequential Decisions
[msml610/lectures_source/Lesson12-Reinforcement_learning.txt](https://github.com/gpsaggese/gpsaggese.github.io/tree/master/msml610/lectures/Lesson12-Reinforcement_learning.pdf)

- Markov Decision Processes (MDPs)
  - States, actions, and rewards
  - Transition models and value functions
  - Optimal policies and Bellman equations
- Solving MDPs
  - Value iteration
  - Policy iteration
  - Dynamic programming approaches
- Dealing with Partial Observability
  - Partially observable MDPs (POMDPs)
  - Belief states and information states
  - Approximate solutions for POMDPs
- Learning from Experience
  - Model-based RL: learning the dynamics
  - Model-free RL: learning values directly
  - Q-learning, SARSA, and temporal difference learning
  - Exploration vs. exploitation trade-offs
- Offline and Batch Settings
  - Offline reinforcement learning
  - Batch policy evaluation
  - When to learn and when to evaluate
- Tools and Tutorials
  - TUTORIAL: gymnasium (standard RL environments for MDP experimentation)
  - TUTORIAL: Stable Baselines3 (reliable RL algorithm implementations)
  - TUTORIAL: d3rlpy (offline reinforcement learning algorithms)

### 13: Probabilistic Forecasting and Uncertainty Quantification
// Ref: TBD

- Predictive distributions and Bayesian prediction
- Conformal prediction and distribution-free methods
- Quantile regression and interval forecasts
- Uncertainty calibration and coverage
- TUTORIAL: PyMC (posterior predictive checks and uncertainty quantification)
- TUTORIAL: Hugging Face Transformers (uncertainty in pretrained models)

- Aleatoric vs. epistemic uncertainty (see Chapter 11)
- Bayesian approaches to uncertainty (Chapter 11, 12)
- Calibration and coverage in decision contexts (Chapter 11)

### 14: Causal Decision Making in Practice
[msml610/lectures_source/Lesson08.5-Causal_AI_In_Business.txt](https://github.com/gpsaggese/gpsaggese.github.io/tree/master/msml610/lectures/Lesson08.5-Causal_AI_In_Business.pdf)

- Why Causal Models Are Required for Interventions
  - Causal vs. predictive thinking in decision making
  - When prediction fails: Simpson's paradox and policy reversal
  - Causal models as decision support tools
- Decision Diagrams and Influence Diagrams
  - Graphical representations of decision problems
  - Adding decision nodes to causal DAGs
  - Value of information and optimal decisions
- Policy Interventions and Optimization
  - Policy interventions: atomic and compound actions
  - Treatment policies and heterogeneous effects
  - Policy learning from data
  - Uplift and targeting strategies
- Causal Reinforcement Learning
  - Integrating causal models with RL
  - When RL is insufficient and causality helps
  - Model-based causal RL
- Real-World Applications
  - Marketing and customer interventions
  - Recommendation systems with causal constraints
  - Healthcare policy evaluation
- Tools and Tutorials
  - TUTORIAL: DoWhy (counterfactual reasoning and policy evaluation)
  - TUTORIAL: EconML (treatment policy optimization and uplift)

### 15: Causal Reasoning in AI Systems
// Ref: TBD

- What LLMs get right and wrong about causality
- Chain-of-thought, tree-of-thought, and self-consistency for causal tasks
- Reflection and self-correction: Reflexion and iterative refinement
- Connecting LLM reasoning to causal and probabilistic reasoning
- Agent architectures: reactive, deliberative, and causal
- Integrating causal models into agent action selection
- Planning under causal uncertainty
- Multi-agent systems and human-in-the-loop
- TUTORIAL: ReAct (reasoning and acting framework for LLM agents)
- TUTORIAL: LangChain (CoT and tool-augmented reasoning pipelines)
- TUTORIAL: LangChain + DoWhy (causal model integrated into agent reasoning)
- TUTORIAL: LlamaIndex (knowledge-grounded reasoning over structured data)
