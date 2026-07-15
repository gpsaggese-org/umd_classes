# Summary

## Title
- From Data to Decisions: Building Decision Systems with Probabilistic Causal
  Reasoning

- Reasoning under Uncertainty: Causal Machine Learning for Decision Making

## Target audience
- Senior ML engineers and data scientists with a statistics and probabilistic ML
  background who build production decision systems
- Working knowledge of causal basics (DAGs, SCMs, do-calculus) assumed

## Short TOC
- The sequence of the parts in the books are:
  - Motivation
    - 01. Why Decisions, Not Predictions
    - 02. The Cost of Ignoring Causality
    - 03. The Cost of Ignoring Uncertainty
  - Advanced Modeling Theory & Tools
    - 04. Knowledge Representation
    - 05. Probalistic ML
    - 06. Causal ML
  - Data
    - 07. Building Causal Knowledge
    - 08. Causal data pipelines
  - Decision-Making Theory & Tools
    - 09. Decision Theory Foundations
    - 10. Taxonomy of Decision-Making Problems and Algorithms
    - 11. Simple Decisions
    - 12. Complex Decisions
    - 13. Agentic Causal Reasoning
  - Implementation, Deployment, & Governance
    - 14. Building Stakeholder Alignment
    - 15. Deployment, Monitoring, and Adaptation
    - 16. Trust, Explainability, Fairness, and Governance

## Lesson Materials
// From ./generate_all_tocs.sh
- `msml610/all_tocs.md`
- `msml610/lectures_source/*.txt`

- `book.Agentic_AI/all_tocs.md`
- `book.Agentic_AI/lectures_source/*.txt`

- `book_springer/all_tocs.md`
- `book_springer/lectures_source/*.txt`

- `data605/all_tocs.md`
- `data605/lectures_source/*.txt`

# Detailed TOC

# Part I: Why Businesses Need Decisions, not Predictions (Motivation)

## 00: Introduction

### Topics
- Path of the book
- Description of the goals
- Description of the chapters

### Lesson Materials
- [100%]: `msml610/lectures_source/Lesson08.1-Causal_AI_intro.txt`
  - Motivation for causal AI, business context, workflow overview, role of decision systems
- [90%]: `msml610/lectures_source/Lesson00-Class.txt`
  - Course structure, books and resources, grading, class map and organization
- [80%]: `book_springer/lectures_source/Lesson01.01_From_Data_Science_To_Decision_Science.txt`
  - Decision science framework, decision pipeline overview, transition from data science
- [50%]: Not covered - Detailed chapter-by-chapter preview, book-specific narrative

## 01: Why Decisions, Not Predictions

### Topics
- Course Roadmap: the decision pipeline ($data \to model \to policy \to action
  \to feedback$) and five-part structure
- Why Traditional ML Falls Short: four critical gaps (causality, uncertainty,
  business objective, dynamics)
- From Data Science to Decision Science: predictive vs. decision-making paradigms
- Causal vs Predictive Questions: predictive form vs. causal form of business
  questions
- The Analytics Maturity Ladder: from descriptive (level 0) through predictive
  (level 1), causal (level 2), to decision (level 3)

### Lesson Materials
- [100%]: `book_springer/lectures_source/Lesson01.01_From_Data_Science_To_Decision_Science.txt`
  - Decision pipeline framework, data science vs decision science paradigm shift, prediction vs action framing
- [100%]: `book_springer/lectures_source/Lesson01.02_Integrating_Causality_And_Probability_in_ML.txt`
  - Integration of causality and uncertainty into ML systems, moving beyond correlation
- [100%]: `book_springer/lectures_source/Lesson01.03_Integrating_Business_Objective_And_Real_World_Dynamics.txt`
  - Business objective encoding, real-world dynamics, feedback loops, performativity
- [85%]: `msml610/lectures_source/Lesson08.1-Causal_AI_intro.txt`
  - Ladder of Causation; Data Science → Decision Science; Causal vs Predictive Questions; Analytics Sophistication; Why AI Projects Fail
- [40%]: `msml610/lectures_source/Lesson11.1-Decision_Making_with_Causal_Models.txt`
  - Predictions vs Decisions Side-by-Side; Simpson's Paradox; Causal Resolution; Policy Reversal
- [5%]: `msml610/lectures_source/Lesson08.2-Causal_Networks.txt`
  - Example of ladder of causation (Tornado Warning)

## 02: The Cost of Ignoring Causality

### Topics
- When Correlation Misleads
  - Correlation encodes confounding as causation: $\Pr(Y | X) \neq \Pr(Y |
    do(X))$
  - Missing interventions and counterfactuals: observational models cannot answer
    "what if?" questions
  - Selection bias and the missing counterfactual: incomplete populations in
    historical data
- Structural Failure Modes
  - Interference and spillovers across units: SUTVA violations in marketplaces
    and networks
  - Simpson's Paradox: when aggregates reverse while subgroups show consistent
    effects
  - Collider bias: conditioning creates illusions (Berkson's paradox)
  - Discarding domain knowledge and mechanism: pattern-driven models inherit
    training data artifacts

### Lesson Materials
- [100%]: `msml610/lectures_source/Lesson08.1-Causal_AI_intro.txt`
  - Correlation is not causation, problems with traditional AI, cost of ignoring causality, causal vs predictive questions
- [95%]: `msml610/lectures_source/Lesson08.2-Causal_Networks.txt`
  - Causal DAGs, structural causal models, confounding bias, collider bias, mediators and moderators, types of paths
- [90%]: `msml610/lectures_source/Lesson08.4.txt`
  - Simpson's Paradox, confounding bias, selection bias, SUTVA violations, interference, causal inference basics
- [85%]: `msml610/lectures_source/Lesson08.5-Experimentation.txt`
  - Why randomization breaks confounding, causal identification through design, network effects and interference
- [70%]: `msml610/lectures_source/Lesson12.2-Causal_Discovery.txt`
  - Markov equivalence, identifiability, faithfulness, challenges in causal discovery from observational data
- [30%]: Not covered - Advanced sensitivity analysis, bounding methods for unmeasured confounding

## 03: The Cost of Ignoring Uncertainty

### Topics
- Point Estimates in a Small-Data World
  - Point estimates without error bars: single numbers hide decision-relevant
    variance
  - Epistemic vs aleatoric uncertainty conflated: inability to detect
    out-of-distribution inputs
  - No abstention: systems that never say "I don't know" are overconfident
    off-distribution
  - Overfitting and statistical significance traps: peeking, multiple
    comparisons, burned test sets

### Lesson Materials
- [100%]: `msml610/lectures_source/Lesson07.2-Posterior_Based_Decisions.txt`
  - Aleatoric vs epistemic uncertainty, representing uncertainty in decisions, communicating uncertainty to stakeholders
- [95%]: `msml610/lectures_source/Lesson07.1-Intro_to_Probabilistic_Programming.txt`
  - Bayesian approach to uncertainty, confidence vs credible intervals, posterior predictive distributions, uncertainty quantification
- [90%]: `msml610/lectures_source/Lesson05.2-Overfitting.txt`
  - Overfitting and underfitting, bias-variance decomposition, high-variance regime, learning curves, statistical significance traps
- [85%]: `msml610/lectures_source/Lesson05.1-Learning_Theory.txt`
  - Generalization bounds, Hoeffding inequality, VC dimension, when learning is possible
- [80%]: `msml610/lectures_source/Lesson05.3-Learn_Validation.txt`
  - Train-test split, cross-validation, bootstrap methods, confidence intervals, out-of-sample error estimation
- [75%]: `msml610/lectures_source/Lesson91.Refresher_probability.txt`
  - Probability fundamentals, confidence intervals, hypothesis testing, multiple comparison issues
- [60%]: `msml610/lectures_source/Lesson02.5-ML_Techniques_Model_Evaluation.txt`
  - Model selection, performance metrics, precision-recall trade-offs, evaluation methodology
- [40%]: Not covered - Calibration in neural networks, conformal prediction methods

# Part II: Advanced Modeling Theory & Tools

## 04: Knowledge Representation

### Topics
- Knowledge Representation
  - Basics of Knowledge Representation
  - Examples of Logic
  - Logical Agents
  - Ontologies
  - Reasoning in Ontologies
- Propositional logic
  - Syntax
  - Semantics
- First-order Logic
  - Syntax
  - Semantics
- Non-classical Logics
  - Intro and Examples
  - Description Logics
  - Semantic Web
- Bayesian networks
- Causal networks

### Lesson Materials
- [85%]: `msml610/lectures_source/Lesson03-Knowledge_representation.txt`
  - Knowledge representation fundamentals, logic, symbolic representation, ontologies, first-order logic
- [100%]: `msml610/lectures_source/Lesson08.2-Causal_Networks.txt`
  - Causal DAGs, structural causal models, causal edges and stability, mechanisms, observed vs unobserved variables
- [95%]: `msml610/lectures_source/Lesson08.3-Do_Calculus.txt`
  - Do-calculus, interventions, counterfactuals, back-door and front-door adjustments, do-operator, graphical criteria
- [90%]: `msml610/lectures_source/Lesson06.1-Bayesian_Networks.txt`
  - Bayesian networks as graphical models, conditional independence, d-separation, Markov blanket
- [75%]: `msml610/lectures_source/Lesson08.4.txt`
  - Causal models, potential outcomes, consistency, identification, d-separation, graphical models, confounding
- [70%]: `msml610/lectures_source/Lesson06.2-Using_Bayesian_Networks.txt`
  - Constructing Bayesian networks, causal vs diagnostic models, ordering of nodes, assumptions
- [60%]: Not covered - Advanced identifiability theory, instrumental variable theory, generalization across environments

## 05: Probabilistic ML

### Topics
- Logic-Based AI Under Uncertainty
  - Problem
  - Solution
- Probabilistic Reasoning
  - Conditional Independence
  - Bayesian Networks
- Semantics of Bayesian Networks
- Constructing a Bayesian Network
- Exact Inference in Bayesian Networks
- Approximate Inference in Bayesian Networks
- Concepts
- Coin Example
  - Analytical Approach
  - Frequentist vs Bayesian
  - Probabilistic Programming
- Posterior-Based Decisions
  - Chemical Shift: Example
  - Posterior Predictive Checks
    - Robust Inference
  - Groups Comparison
- Hierarchical Models
- Generalized Linear Models
  - Simple Linear Model
  - Logistic Regression
  - Multiple Linear Regression
- Bayesian Model Comparison
    - Posterior Predictive Checks
  - The Balance Between Simplicity and Accuracy
  - Measures of Predictive Accuracy
    - Information Criteria
    - Cross-Validation
  - Bayesian Model Selection and Ensemble
  - Bayesian Hypothesis Testing
    - Bayes Factors and Information Criteria
  - Regularizing Priors

### Lesson Materials
- `msml610/lectures_source/Lesson06.1-Bayesian_Networks.txt`
  - Graphical models for uncertainty, probabilistic reasoning, conditional independence, Bayesian network structure
- `msml610/lectures_source/Lesson06.2-Using_Bayesian_Networks.txt`
  - Constructing Bayesian networks, inference algorithms, message-passing, belief propagation
- `msml610/lectures_source/Lesson07.1-Intro_to_Probabilistic_Programming.txt`
  - Bayesian inference fundamentals, EDA vs inference, modern probabilistic tools (PyMC, Pyro), MCMC introduction
- `msml610/lectures_source/Lesson07.2-Posterior_Based_Decisions.txt`
  - Posterior-based choices, Bayesian decision-making, utility under uncertainty, loss functions
- `msml610/lectures_source/Lesson07.3-Hierarchical_Models.txt`
  - Hierarchical Bayesian models, structured latent variables, multi-level probabilistic modeling
- `msml610/lectures_source/Lesson07.4-Generalized_Linear_Models.txt`
  - Probabilistic GLMs, generative models, hierarchical probabilistic structures, Bayesian regression
- `msml610/lectures_source/Lesson07.5-Bayesian_Model_Comparison.txt`
  - Bayesian model selection, posterior predictive checks, model comparison criteria (AIC, BIC, WAIC)

## 06: Causal ML

### Topics

### Lesson Materials
- `msml610/lectures_source/Lesson08.2-Causal_Networks.txt`
  - Causal DAGs, structural causal models, mechanisms, identifying causal structures
- `msml610/lectures_source/Lesson08.3-Do_Calculus.txt`
  - Do-calculus, interventional identification, front-door and back-door criteria
- `msml610/lectures_source/Lesson08.4.txt`
  - Identification, d-separation, graphical criteria, confounding bias, instrumental variables
- `msml610/lectures_source/Lesson12.2-Causal_Discovery.txt`
  - Causal discovery from observational data, identifiability, Markov equivalence, algorithm families (constraint, score, functional), validation

# Part III: Data

## 07: Building Causal Knowledge

### Topics
- Eliciting causal knowledge from domain experts: structured methods, expert
  judgment, and iterative refinement
- Building causal DAGs: variable selection, causal assumptions, and graph
  construction from domain knowledge
- Variable types and relationships: confounders, mediators, colliders,
  moderators, and their roles in causal inference
- Temporal structure in causal systems: causal order, feedback delays, causal
  acyclicity, and dynamic relationships
- Measurement and operationalization: defining variables, measurement validity,
  proxy variables for latent constructs
- Documenting causal assumptions: transparency, validation, and stakeholder
  alignment on causal structures

### Lesson Materials
- [90%]: `msml610/lectures_source/Lesson08.1-Causal_AI_intro.txt`
  - Causal AI workflow, building causal DAGs, eliciting from domain experts, step-by-step process
- [95%]: `msml610/lectures_source/Lesson08.2-Causal_Networks.txt`
  - Building causal DAGs, variable types (mediators, confounders, colliders, moderators), observed vs unobserved variables
- [70%]: `msml610/lectures_source/Lesson08.3-Do_Calculus.txt`
  - Structural causal models, mechanisms, functional forms, causal order
- [75%]: `msml610/lectures_source/Lesson08.4.txt`
  - Confounding, mediation, moderators, causal assumptions, temporal structure
- [60%]: `msml610/lectures_source/Lesson09.1-Reasoning_over_time.txt`
  - Temporal causal structures, Markov property, feedback delays, dynamic systems
- [85%]: `msml610/lectures_source/Lesson12.2-Causal_Discovery.txt`
  - Using domain knowledge as constraints, combining discovery with expert judgment, validation
- [50%]: Not covered - Formal elicitation methods, measurement error correction, proxy variable selection strategies

## 08: Causal Data Pipelines

### Topics
- Data collection and its biases: how collection processes introduce selection
  bias and confounding
- Selection bias and incomplete populations: missing data mechanisms (MCAR, MAR,
  MNAR) and their impact on causal inference
- Distribution shift and covariate mismatch: training vs. production misalignment,
  concept drift, and environment shifts
- Measurement error and proxy validity: assessing proxy variable quality,
  attenuation in causal effects, and measurement error correction
- Pre-flight checks: validating data quality, assessing confounder balance,
  checking assumptions before causal modeling
- Data quality for causal inference: handling missingness, outliers, and data
  anomalies in causal analysis
- Selection Bias
  - How data collection processes bias what you observe
  - Missing data mechanisms (MCAR, MAR, MNAR)
  - Biases introduced by how samples were selected
- Distribution Shift
  - Training vs. production data distribution mismatch
  - Covariate shift, label shift, and concept drift
  - Detecting and mitigating distribution changes

### Lesson Materials
- [95%]: `msml610/lectures_source/Lesson08.1-Causal_AI_intro.txt`
  - Data acquisition and integration in causal workflows, data quality for causal inference
- [90%]: `msml610/lectures_source/Lesson08.4.txt`
  - Selection bias, confounding from data collection, SUTVA violations, interference, missing data mechanisms
- [85%]: `data605/lectures_source/Lesson02.3-Data_Pipelines.txt`
  - Data pipeline architectures, data quality checks, data transformation
- [80%]: `data605/lectures_source/Lesson07.2-Data_Wrangling.txt`
  - Data cleaning, handling missing data, outlier detection, data preprocessing
- [75%]: `msml610/lectures_source/Lesson10.2-Causal_Inference_for_Time_Series.txt`
  - Distribution shift, non-stationarity, temporal structure, confounding over time
- [70%]: `msml610/lectures_source/Lesson08.3-Do_Calculus.txt`
  - Causal identification under confounding, backdoor and frontdoor criteria
- [65%]: `msml610/lectures_source/Lesson02.3-ML_Techniques_Input_Processing.txt`
  - Data processing, handling outliers, missing data, normalization, feature engineering
- [60%]: Not covered - Advanced measurement error correction, missing data mechanisms (MAR/MNAR specifics), covariate shift adaptation strategies

# Part IV: Decision-Making Theory & Tools

## 09: Decision Theory Foundations

### Topics
- Von Neumann-Morgenstern theorem: axioms of rational choice and utility
  existence
- Utility functions in practice: eliciting preferences and encoding business
  objectives
- Subjective expected utility: belief updating and decision-making under
  uncertainty
- Multi-criteria trade-offs: value functions, weights, and Pareto optimality
- Influence diagrams and solving decision networks: backward induction and policy
  extraction
- Risk preferences and utility curvature: risk-aversion, neutrality, and seeking

### Lesson Materials
- [95%]: `msml610/lectures_source/Lesson11.1-Decision_Making_with_Causal_Models.txt`
  - Utility functions, expected utility principle, causal interventions, decision networks, Bayesian decision-making
- [90%]: `msml610/lectures_source/Lesson07.2-Posterior_Based_Decisions.txt`
  - Utility functions, expected utility, risk preferences, multi-criteria trade-offs, prior elicitation
- [85%]: `msml610/lectures_source/Lesson12.1-Reinforcement_learning.txt`
  - Utility of states, Bellman equations, expected utility of policies, value iteration
- [80%]: `msml610/lectures_source/Lesson09.3-Multi_Armed_Bandits.txt`
  - Sequential decision-making, exploration-exploitation, value of information, Bayesian optimization
- [75%]: `msml610/lectures_source/Lesson07.1-Intro_to_Probabilistic_Programming.txt`
  - Bayesian models for decision-making, posterior-based choices, uncertainty in utility
- [60%]: Not covered - Formal axiomatic foundations of utility theory, advanced risk-preference elicitation, cooperative game theory

## 10: Taxonomy of Decision-Making Problems and Algorithms

### Topics
- From causal effects to expected value: plugging treatment effects into utility
  functions
- Bayesian decision-making: posterior-based choices and belief updating from data
- Value of information: EVPI, EVSI, and when to experiment vs. observe
- Bayesian optimization and acquisition functions: efficient search over decision
  spaces
- Exploration vs. exploitation: Thompson sampling, UCB, and contextual bandits
- Counterfactual decision analysis: reasoning about alternative choices
- Robustness under model misspecification: decisions that work across causal
  assumptions

### Lesson Materials
- [95%]: `msml610/lectures_source/Lesson11.1-Decision_Making_with_Causal_Models.txt`
  - Causal effects to expected value, Bayesian decision-making, value of information, exploration vs exploitation, robustness
- [90%]: `msml610/lectures_source/Lesson09.3-Multi_Armed_Bandits.txt`
  - Thompson sampling, UCB, epsilon-greedy, contextual bandits, regret bounds, exploration-exploitation tradeoff
- [85%]: `msml610/lectures_source/Lesson12.1-Reinforcement_learning.txt`
  - MDPs, value iteration, policy iteration, optimal decision-making under uncertainty
- [80%]: `msml610/lectures_source/Lesson08.5-Experimentation.txt`
  - A/B testing, experimentation design, value of information, when to experiment vs observe, hybrid approaches
- [75%]: `msml610/lectures_source/Lesson07.2-Posterior_Based_Decisions.txt`
  - Posterior-based choices, decision networks, value of information, Bayesian optimization
- [60%]: `msml610/lectures_source/Lesson07.1-Intro_to_Probabilistic_Programming.txt`
  - Bayesian approaches to sequential decision-making, posterior updating
- [50%]: Not covered - Distributional robustness, minmax optimization, advanced acquisition functions

## 11: Simple Decisions

### Topics
- Heterogeneous treatment effects and CATE: learning who benefits from treatment
- Doubly robust estimation and double/debiased ML: reducing sensitivity to
  nuisance parameters
- Meta-learners for heterogeneity: T-, S-, X-, R-learners and when to use each
- Distributional and quantile effects: going beyond average treatment effects
- Off-policy learning and policy optimization: evaluating and improving policies
  from data
- Safe policy improvement: deployable decisions with finite-sample guarantees

### Lesson Materials
- [95%]: `msml610/lectures_source/Lesson08.4.txt`
  - Heterogeneous treatment effects, CATE, individual treatment effects, causal forests, meta-learners (T, X, S, R learners)
- [90%]: `msml610/lectures_source/Lesson08.5-Experimentation.txt`
  - Heterogeneous treatment effects, treatment effect variation across subgroups, policy evaluation
- [85%]: `msml610/lectures_source/Lesson11.1-Decision_Making_with_Causal_Models.txt`
  - Off-policy learning, policy optimization, evaluating decisions from data
- [80%]: `msml610/lectures_source/Lesson12.1-Reinforcement_learning.txt`
  - Off-policy RL, policy iteration, off-line learning, safe policy improvement
- [70%]: `msml610/lectures_source/Lesson07.2-Posterior_Based_Decisions.txt`
  - Distributional effects, uncertainty in treatment effects, posterior predictive distributions
- [60%]: Not covered - Doubly robust estimation details, R-learner specifics, safe policy improvement bounds

## 12: Complex Decisions

### Topics
- Partial identification: when point estimates are impossible, bound what you can
- Manski bounds and instrumental variable bounds: leveraging assumptions
  strategically
- Sensitivity analysis: Rosenbaum bounds and E-values for robustness to
  unmeasured confounding
- Positivity violations: trimming, extrapolation, and inverse-probability
  weighting trade-offs
- Distributional robustness and minimax inference: decisions robust to model
  misspecification
- Causal generalization and domain adaptation: transferring lessons across
  environments
- Markov decision processes and multi-step planning: states, actions, transitions,
  and solving with value/policy iteration
- Causal world models as environment dynamics: planning, counterfactual rollouts,
  and policy search

### Lesson Materials
- [95%]: `msml610/lectures_source/Lesson12.1-Reinforcement_learning.txt`
  - MDPs, multi-step planning, value iteration, policy iteration, dynamic decision networks, world models
- [90%]: `msml610/lectures_source/Lesson08.4.txt`
  - Positivity, IPW, sensitivity analysis, feature selection dilemma, propensity score methods
- [85%]: `msml610/lectures_source/Lesson10.2-Causal_Inference_for_Time_Series.txt`
  - Multi-step causal inference, feedback loops, dynamic systems, temporal planning
- [80%]: `msml610/lectures_source/Lesson11.1-Decision_Making_with_Causal_Models.txt`
  - Robustness under uncertainty, causal generalization, model misspecification, sequential planning
- [75%]: `msml610/lectures_source/Lesson09.1-Reasoning_over_time.txt`
  - Temporal reasoning, Markov processes, state transitions, temporal structure
- [60%]: `msml610/lectures_source/Lesson07.2-Posterior_Based_Decisions.txt`
  - Uncertainty in sequential decisions, value of information
- [50%]: Not covered - Partial identification bounds, Manski bounds specifics, E-values and sensitivity analysis

## 13: Agentic Causal Reasoning

### Topics
- Causal reasoning in LLMs: pattern-based limits and why foundation models
  struggle with counterfactuals
- Chain-of-thought and tree-of-thought prompting: structured reasoning for causal
  inference
- SCM-augmented agents: embedding causal world models in agent architectures
- Tool-use and causal simulation: planning with learned or specified dynamics
- Integrating causality with probabilistic inference: hybrid reasoning systems
- Trustworthy AI through causality: transparency, robustness, fairness, and
  safety
- Causal guardrails and safety constraints: preventing harmful behaviors in
  autonomous agents
- Performativity and adaptive systems: decisions that change the world, feedback
  loops, and learning from outcomes
- Online causal discovery: learning and revising causal models from deployment
  feedback

### Lesson Materials
- [95%]: `book.Agentic_AI/lectures_source/Lesson01.07-Tool_use_and_retrieval.txt`
  - Agent tool-use architecture, causal simulation, planning with external tools, grounded reasoning
- [95%]: `book.Agentic_AI/lectures_source/Lesson01.04-LLM_Reasoning.txt`
  - Chain-of-thought variants, tree-of-thought, structured decomposition, verifiable reasoning chains
- [90%]: `book.Agentic_AI/lectures_source/Lesson01.05-Reasoning_Memory_and_Planning.txt`
  - Planning ahead, world models, model-based planning, simulation-based decision-making, causal rollouts
- [90%]: `book.Agentic_AI/lectures_source/Lesson01.01-What_Is_An_Agentic_AI.txt`
  - Agent architecture foundations, perception-decision-action loops, goal-directed systems
- [85%]: `book.Agentic_AI/lectures_source/Lesson01.08-Learning_to_reason.txt`
  - Training reasoning capabilities, process reward models, causal reasoning in learned models
- [80%]: `book.Agentic_AI/lectures_source/Lesson01.09_Post_training_and_verifiable_agents.txt`
  - Safety constraints, verification of agent behavior, guardrails for preventing harmful actions
- [75%]: `book.Agentic_AI/lectures_source/Lesson01.11_Lessons_from_training_agentic_models.txt`
  - Practical insights on agentic model training, learned behavior patterns, feedback loop insights
- [70%]: `book.Agentic_AI/lectures_source/Lesson01.10_Open_training_recipes_for_reasoning.txt`
  - Training approaches for reasoning, curriculum learning for causal reasoning
- [70%]: `book.Agentic_AI/lectures_source/Lesson01.06-Inference_time_techniques.txt`
  - Search algorithms for planning, inference-time reasoning, exploring multiple causal paths
- [50%]: `book.Agentic_AI/lectures_source/Lesson01.02-LLM_Building_Blocks.txt`
  - Foundation model capabilities and limitations relevant to causal reasoning
- [40%]: `book.Agentic_AI/lectures_source/Lesson01.03-History_of_LLM_Agents.txt`
  - Historical evolution of agent concepts, context for understanding modern agentic systems
- [20%]: Not covered - Specific online causal discovery algorithms, detailed performativity mathematics

# Part V: Implementation, Deployment, Governance

## 14: Building Stakeholder Alignment

### Topics
- Eliciting causal knowledge from domain experts during DAG construction: structured
  elicitation methods, disagreement resolution, and iterative refinement of causal
  structures before model building
- Stakeholder feedback loops during model development: reviewing intermediate
  results, sensitivity analyses, and refining assumptions based on expert critique
- Communicating causal assumptions to different audiences: domain experts,
  operations teams, business leadership
- Causal DAG visualization and debate: handling disagreement on causal structures
  and variable selection
- Sensitivity analysis as a communication tool: demonstrating robustness to
  assumption violations
- Intervention design communication: selecting and justifying decision levers
  with stakeholders
- Risk tolerance and decision cost asymmetry: aligning stakeholders on cost of
  false positives vs false negatives
- Stakeholder buy-in before deployment: achieving consensus on causal model
  adequacy and assumptions

### Lesson Materials
- [90%]: `msml610/lectures_source/Lesson08.1-Causal_AI_intro.txt`
  - Causal workflow with stakeholders, eliciting causal knowledge, hybrid teams, stakeholder alignment
- [85%]: `msml610/lectures_source/Lesson12.2-Causal_Discovery.txt`
  - Using domain knowledge as constraints, combining discovery with expert judgment, validation
- [80%]: `msml610/lectures_source/Lesson11.1-Decision_Making_with_Causal_Models.txt`
  - Communicating uncertainty to stakeholders, decision support, stakeholder alignment
- [75%]: `msml610/lectures_source/Lesson08.2-Causal_Networks.txt`
  - Building causal DAGs with domain experts, causal assumptions, documenting assumptions
- [70%]: `msml610/lectures_source/Lesson07.2-Posterior_Based_Decisions.txt`
  - Communicating uncertainty, prior elicitation, stakeholder preferences in utilities
- [60%]: `msml610/lectures_source/Lesson08.4.txt`
  - Confounding, cost asymmetry, false positives vs negatives, robustness
- [50%]: Not covered - Formal stakeholder elicitation methods, disagreement resolution protocols

## 15: Deployment, Monitoring, and Adaptation

### Topics
- From notebook to production: operationalizing causal decision systems
- Cost-aware deployment strategies: phased rollout, shadow mode, and canary
  analysis tailored to decision cost asymmetry
- Operationalizing causal assumption monitoring: testable vs. untestable
  assumptions, failure detection, and implementation strategies
  - **Directly testable assumptions**: temporal stability of effects, proxy
    variable validity, treatment effect heterogeneity stability; monitoring via
    time-series trend detection, proxy correlation drift, stratified effect
    estimates in real-time dashboards
  - **Indirectly testable assumptions**: robustness bounds via sensitivity
    analysis, negative controls, instrumental variable diagnostics; pre-compute
    E-value bounds and flag when observational data approaches these thresholds
  - **Domain-assessed assumptions**: causal graph structure, sufficiency of
    confounding set (requires periodic expert re-assessment; schedule quarterly
    or post-deployment reviews)
  - Concrete monitoring dashboards: metrics that flag assumption breakdown
    (e.g., alert when treatment effect heterogeneity variance exceeds baseline,
    when proxy validity correlation drops below threshold, when negative control
    estimates diverge from zero)
- A/B testing vs. causal inference in production: when to run experiments vs rely
  on observational causal models
- Continuous experimentation and policy improvement: sequential testing,
  exploration vs exploitation, incremental policy updates
- Heterogeneous deployment: adapting rollout to treatment effect variation across
  subgroups
- Model versioning, error budgets, and rollback: decision error thresholds and
  when/how to revert
- Feedback loops in production: learning from deployed decisions to update causal
  models iteratively
- Technical debt and decision system maintenance: keeping systems reliable over
  time

### Lesson Materials
- [95%]: `msml610/lectures_source/Lesson08.5-Experimentation.txt`
  - A/B testing vs observational methods, continuous experimentation, sequential testing, policy improvement
- [90%]: `msml610/lectures_source/Lesson11.1-Decision_Making_with_Causal_Models.txt`
  - Monitoring uncertainty, robustness under misspecification, feedback loops, learning from deployed decisions
- [85%]: `msml610/lectures_source/Lesson12.1-Reinforcement_learning.txt`
  - Online learning, feedback loops, policy iteration, adaptive systems, model-based updates
- [80%]: `msml610/lectures_source/Lesson10.2-Causal_Inference_for_Time_Series.txt`
  - Monitoring temporal stability, distribution shift detection, feedback loops over time
- [75%]: `msml610/lectures_source/Lesson08.4.txt`
  - Effect heterogeneity monitoring, heterogeneous deployment, stratified rollout
- [70%]: `msml610/lectures_source/Lesson09.1-Reasoning_over_time.txt`
  - Monitoring assumptions over time, temporal monitoring, updating beliefs from deployment
- [60%]: `data605/lectures_source/Lesson02.3-Data_Pipelines.txt`
  - Production data pipelines, monitoring, alerting, technical infrastructure
- [50%]: Not covered - Advanced monitoring dashboard design, comprehensive error budgeting, detailed rollback procedures

## 16: Trust, Explainability, Fairness, and Governance

### Topics
- Building trust: transparency, stakeholder alignment, and justified confidence
  in causal decisions
- Causal vs. statistical explainability: distinguishing mechanisms (do-calculus,
  SCM) from attribution (SHAP, LIME, permutation importance)
  - Causal explainability tools and answers: "Why did we intervene?" via causal
    mechanisms (backdoor/frontdoor adjustment paths), mediation analysis (direct
    vs. indirect effects), counterfactual reasoning (what if we had intervened
    differently?), and SCM-based decision explanations
  - Statistical explainability tools and answers: "What features correlated with
    this decision?" (SHAP, LIME, permutation importance); risk: features may be
    confounders or colliders, not causal levers; can mislead stakeholders about
    what they can actually change
  - Operational risk: high statistical importance + low causal relevance (e.g.,
    a confounding variable ranked high by SHAP but not actionable), or vice versa
- Operationalizing causal explainability in production: decision explanations at
  serve-time, contrast with feature importance
- Identifying failure modes in production: when decisions fail and why at runtime
  (model misspecification becoming evident, distribution shift, causal assumption
  breakdown, unexpected feedback loops); differs from Ch16 assumption monitoring
  in scope (early detection vs. post-facto diagnosis) and remediation (emergency
  rollback vs. controlled re-calibration)
- Fairness under deployment: preventing disparate impact, fairness monitoring
  across subgroups, heterogeneous decision effects
- Override procedures and human-in-the-loop: escalation mechanisms, decision
  disputes, and when to trust vs. challenge the system
- Failure mode detection and response: monitoring, alerting, root cause analysis,
  and remediation
- Decision governance and audit trails: who approved what, when assumptions
  broke, what was the impact, and institutional accountability
- Regulatory and compliance alignment: overview of regulatory landscape (GDPR,
  EU AI Act, fairness certifications) and engineer accountability; focus on
  documentation requirements (causal assumptions, deployment decisions, override
  logs), audit trails for decisions, and when to involve compliance/legal teams
  rather than deep regulatory expertise
- Guardrails and safety constraints: preventing harmful behaviors, maintaining
  causal assumptions, and safeguarding against edge cases

### Lesson Materials
- [95%]: `msml610/lectures_source/Lesson13.1-Explainability.txt`
  - Causal vs statistical explainability, SHAP, LIME, counterfactual explanations, distinguishing causal from correlational
- [90%]: `msml610/lectures_source/Lesson08.2-Causal_Networks.txt`
  - Causal mechanisms, mediation analysis, direct vs indirect effects, counterfactual reasoning
- [85%]: `book.Agentic_AI/lectures_source/Lesson01.09_Post_training_and_verifiable_agents.txt`
  - Safety constraints, verification, guardrails, preventing harmful behaviors, trustworthy AI
- [80%]: `msml610/lectures_source/Lesson08.1-Causal_AI_intro.txt`
  - Interpretability, explainability, causal AI for trustworthy systems, transparency
- [75%]: `msml610/lectures_source/Lesson11.1-Decision_Making_with_Causal_Models.txt`
  - Uncertainty communication, stakeholder trust, decision transparency
- [70%]: `msml610/lectures_source/Lesson08.4.txt`
  - Fairness, disparate impact, effect heterogeneity across subgroups, bias
- [60%]: `book.Agentic_AI/lectures_source/Lesson01.01-What_Is_An_Agentic_AI.txt`
  - Human-in-the-loop, decision oversight, agent transparency, safety
- [50%]: Not covered - Regulatory compliance details (GDPR/EU AI Act specifics), formal governance frameworks, audit trail design

# Appendix
