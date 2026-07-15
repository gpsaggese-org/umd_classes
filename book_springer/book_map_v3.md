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

## Chapter Template

### Topics
- Topic 1
  - Subtopic 1.1
  - Subtopic 1.2
- Topic 2
  ...

### Lesson Materials
- `pointer to a lecture`
  - [Amount of lecture used in this chapter]: <topics>
- `book_springer/lectures_source/Lesson01.02_Integrating_Causality_And_Probability_in_ML.txt`
  - [100%]: Integration of causality and uncertainty into ML systems, moving beyond correlation
- Not covered
  - [<Amount of topics not covered by any lesson>]: <topics>

# Detailed TOC

# Part I: Why Businesses Need Decisions, not Predictions (Motivation)

## 00: Introduction

### Topics
- Path of the book
- Description of the goals
- Description of the chapters

### Lesson Materials
- `msml610/lectures_source/Lesson08.1-Causal_AI_intro.txt`
  - [100%] Motivation for causal AI, business context, workflow overview, role of decision systems
- `msml610/lectures_source/Lesson00-Class.txt`
  - [90%] Course structure, books and resources, grading, class map and organization
- `book_springer/lectures_source/Lesson01.01_From_Data_Science_To_Decision_Science.txt`
  - [80%] Decision science framework, decision pipeline overview, transition from data science
- Not covered
  - [50%] Detailed chapter-by-chapter preview, book-specific narrative

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
- `book_springer/lectures_source/Lesson01.01_From_Data_Science_To_Decision_Science.txt`
  - [100%] Decision pipeline framework, data science vs decision science paradigm shift, prediction vs action framing
- `book_springer/lectures_source/Lesson01.02_Integrating_Causality_And_Probability_in_ML.txt`
  - [100%] Integration of causality and uncertainty into ML systems, moving beyond correlation
- `book_springer/lectures_source/Lesson01.03_Integrating_Business_Objective_And_Real_World_Dynamics.txt`
  - [100%] Business objective encoding, real-world dynamics, feedback loops, performativity
- `msml610/lectures_source/Lesson08.1-Causal_AI_intro.txt`
  - [85%] Ladder of Causation; Data Science → Decision Science; Causal vs Predictive Questions; Analytics Sophistication; Why AI Projects Fail
- `msml610/lectures_source/Lesson11.1-Decision_Making_with_Causal_Models.txt`
  - [40%] Predictions vs Decisions Side-by-Side; Simpson's Paradox; Causal Resolution; Policy Reversal
- `msml610/lectures_source/Lesson08.2-Causal_Networks.txt`
  - [5%] Example of ladder of causation (Tornado Warning)

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
- `msml610/lectures_source/Lesson08.1-Causal_AI_intro.txt`
  - [100%] Correlation is not causation, problems with traditional AI, cost of ignoring causality, causal vs predictive questions
- `msml610/lectures_source/Lesson08.2-Causal_Networks.txt`
  - [95%] Causal DAGs, structural causal models, confounding bias, collider bias, mediators and moderators, types of paths
- `msml610/lectures_source/Lesson08.4.txt`
  - [90%] Simpson's Paradox, confounding bias, selection bias, SUTVA violations, interference, causal inference basics
- `msml610/lectures_source/Lesson08.5-Experimentation.txt`
  - [85%] Why randomization breaks confounding, causal identification through design, network effects and interference
- `msml610/lectures_source/Lesson12.2-Causal_Discovery.txt`
  - [70%] Markov equivalence, identifiability, faithfulness, challenges in causal discovery from observational data
- Not covered
  - [30%] Advanced sensitivity analysis, bounding methods for unmeasured confounding

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
- `msml610/lectures_source/Lesson07.2-Posterior_Based_Decisions.txt`
  - [100%] Aleatoric vs epistemic uncertainty, representing uncertainty in decisions, communicating uncertainty to stakeholders
- `msml610/lectures_source/Lesson07.1-Intro_to_Probabilistic_Programming.txt`
  - [95%] Bayesian approach to uncertainty, confidence vs credible intervals, posterior predictive distributions, uncertainty quantification
- `msml610/lectures_source/Lesson05.2-Overfitting.txt`
  - [90%] Overfitting and underfitting, bias-variance decomposition, high-variance regime, learning curves, statistical significance traps
- `msml610/lectures_source/Lesson05.1-Learning_Theory.txt`
  - [85%] Generalization bounds, Hoeffding inequality, VC dimension, when learning is possible
- `msml610/lectures_source/Lesson05.3-Learn_Validation.txt`
  - [80%] Train-test split, cross-validation, bootstrap methods, confidence intervals, out-of-sample error estimation
- `msml610/lectures_source/Lesson91.Refresher_probability.txt`
  - [75%] Probability fundamentals, confidence intervals, hypothesis testing, multiple comparison issues
- `msml610/lectures_source/Lesson02.5-ML_Techniques_Model_Evaluation.txt`
  - [60%] Model selection, performance metrics, precision-recall trade-offs, evaluation methodology
- Not covered
  - [40%] Calibration in neural networks, conformal prediction methods

# Part II: Advanced Modeling Theory & Tools

## 04: Knowledge Representation

### Topics
- Formal Knowledge Representation
  - Symbolic logic and reasoning systems
  - Propositional and first-order logic
  - Ontologies and semantic web
  - Logic-based agents and inference
- Graphical Models for Uncertainty
  - Bayesian networks: structure, conditional independence, d-separation
  - Markov blankets and efficient inference
  - Constructing and interpreting probabilistic models
- Causal Graphical Models
  - Structural causal models (SCMs) and directed acyclic graphs (DAGs)
  - Causal mechanisms and variable relationships
  - Observed vs. unobserved confounders
- Integrating Logic and Causality
  - Moving from correlation to causal reasoning
  - Combining symbolic representation with probabilistic inference

### Lesson Materials
- `msml610/lectures_source/Lesson03-Knowledge_representation.txt`
  - [85%] Knowledge representation fundamentals, logic, symbolic representation, ontologies, first-order logic
- `msml610/lectures_source/Lesson06.1-Bayesian_Networks.txt`
  - [95%] Bayesian networks as graphical models, conditional independence, d-separation, Markov blanket
- `msml610/lectures_source/Lesson08.2-Causal_Networks.txt`
  - [90%] Causal DAGs, structural causal models, causal edges and stability, mechanisms, observed vs unobserved variables
- `msml610/lectures_source/Lesson06.2-Using_Bayesian_Networks.txt`
  - [80%] Constructing Bayesian networks, causal vs diagnostic models, ordering of nodes, assumptions
- `msml610/lectures_source/Lesson08.4.txt`
  - [70%] Causal models, graphical models, d-separation, identification concepts
- `msml610/lectures_source/Lesson08.3-Do_Calculus.txt`
  - [50%] Do-calculus, interventions, graphical criteria for identification
- Not covered
  - [20%] Advanced identifiability theory, instrumental variable theory, generalization across environments

## 05: Probabilistic ML

### Topics
- Foundations of Bayesian Inference
  - Frequentist vs. Bayesian frameworks
  - Bayesian networks as joint probability distributions
  - Conditional independence and d-separation
  - Prior specification and elicitation
- Inference in Probabilistic Models
  - Exact inference algorithms (belief propagation, variable elimination)
  - Approximate inference (sampling, variational inference, MCMC)
  - Probabilistic programming languages and tools
- Bayesian Generative Models
  - Linear regression with uncertainty quantification
  - Logistic regression and classification
  - Hierarchical models and multi-level structures
  - Regularization via priors
- Uncertainty in Predictions
  - Posterior predictive distributions
  - Epistemic vs. aleatoric uncertainty
  - Posterior predictive checks for model validation
- Bayesian Decision-Making
  - Expected utility under posterior uncertainty
  - Utility functions and loss encoding
  - Decision-making with incomplete information
- Model Comparison and Selection
  - Information criteria (AIC, BIC, WAIC)
  - Cross-validation and out-of-sample prediction
  - Bayes factors and Bayesian hypothesis testing
  - Model ensembles and averaging

### Lesson Materials
- `msml610/lectures_source/Lesson07.1-Intro_to_Probabilistic_Programming.txt`
  - [100%] Bayesian inference fundamentals, EDA vs inference, modern probabilistic tools (PyMC, Pyro), MCMC introduction
- `msml610/lectures_source/Lesson07.2-Posterior_Based_Decisions.txt`
  - [95%] Posterior-based choices, Bayesian decision-making, utility under uncertainty, loss functions
- `msml610/lectures_source/Lesson06.1-Bayesian_Networks.txt`
  - [95%] Graphical models for uncertainty, probabilistic reasoning, conditional independence, Bayesian network structure
- `msml610/lectures_source/Lesson07.5-Bayesian_Model_Comparison.txt`
  - [95%] Bayesian model selection, posterior predictive checks, model comparison criteria (AIC, BIC, WAIC)
- `msml610/lectures_source/Lesson07.4-Generalized_Linear_Models.txt`
  - [90%] Probabilistic GLMs, generative models, hierarchical probabilistic structures, Bayesian regression
- `msml610/lectures_source/Lesson06.2-Using_Bayesian_Networks.txt`
  - [90%] Constructing Bayesian networks, inference algorithms, message-passing, belief propagation
- `msml610/lectures_source/Lesson07.3-Hierarchical_Models.txt`
  - [85%] Hierarchical Bayesian models, structured latent variables, multi-level probabilistic modeling
- Not covered
  - [10%] Advanced variational inference, neural probabilistic models, scalable inference for large datasets

## 06: Causal ML

### Topics
- Causal Graphical Models
  - Structural causal models (SCMs) and causal mechanisms
  - Causal DAGs: identifying causal structures and variable relationships
  - Observed vs. unobserved confounders and hidden variables
- Do-Calculus and Interventional Reasoning
  - The do-operator and interventional distributions
  - Transforming observational queries into interventional quantities
  - Three rules of do-calculus for causal identification
- Identification Criteria
  - Graphical criteria for causal effect identification
  - Back-door criterion: adjusting for confounders
  - Front-door criterion: handling unobserved confounding
  - D-separation and conditional independence in causal graphs
- Advanced Identification Methods
  - Instrumental variables: leveraging natural experiments and exogenous variation
  - Confounding bias quantification and adjustment strategies
  - When identification is possible vs. impossible
- Causal Discovery from Observational Data
  - Learning causal structures from data without experiments
  - Constraint-based, score-based, and functional causal models
  - Markov equivalence and identifiability from observational data
  - Validation and robustness of discovered causal structures

### Lesson Materials
- `msml610/lectures_source/Lesson08.2-Causal_Networks.txt`
  - [100%] Causal DAGs, structural causal models, mechanisms, identifying causal structures
- `msml610/lectures_source/Lesson08.3-Do_Calculus.txt`
  - [100%] Do-calculus, interventional identification, front-door and back-door criteria
- `msml610/lectures_source/Lesson08.4.txt`
  - [95%] Identification, d-separation, graphical criteria, confounding bias, instrumental variables
- `msml610/lectures_source/Lesson12.2-Causal_Discovery.txt`
  - [90%] Causal discovery from observational data, identifiability, Markov equivalence, algorithm families (constraint, score, functional), validation
- Not covered
  - [10%] Online causal discovery, real-time causal inference in streaming data, advanced bounds and sensitivity analysis

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
- `msml610/lectures_source/Lesson08.1-Causal_AI_intro.txt`
  - [90%] Causal AI workflow, building causal DAGs, eliciting from domain experts, step-by-step process
- `msml610/lectures_source/Lesson08.2-Causal_Networks.txt`
  - [95%] Building causal DAGs, variable types (mediators, confounders, colliders, moderators), observed vs unobserved variables
- `msml610/lectures_source/Lesson08.3-Do_Calculus.txt`
  - [70%] Structural causal models, mechanisms, functional forms, causal order
- `msml610/lectures_source/Lesson08.4.txt`
  - [75%] Confounding, mediation, moderators, causal assumptions, temporal structure
- `msml610/lectures_source/Lesson09.1-Reasoning_over_time.txt`
  - [60%] Temporal causal structures, Markov property, feedback delays, dynamic systems
- `msml610/lectures_source/Lesson12.2-Causal_Discovery.txt`
  - [85%] Using domain knowledge as constraints, combining discovery with expert judgment, validation
- Not covered
  - [50%] Formal elicitation methods, measurement error correction, proxy variable selection strategies

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
- `msml610/lectures_source/Lesson08.1-Causal_AI_intro.txt`
  - [95%] Data acquisition and integration in causal workflows, data quality for causal inference
- `msml610/lectures_source/Lesson08.4.txt`
  - [90%] Selection bias, confounding from data collection, SUTVA violations, interference, missing data mechanisms
- `data605/lectures_source/Lesson02.3-Data_Pipelines.txt`
  - [85%] Data pipeline architectures, data quality checks, data transformation
- `data605/lectures_source/Lesson07.2-Data_Wrangling.txt`
  - [80%] Data cleaning, handling missing data, outlier detection, data preprocessing
- `msml610/lectures_source/Lesson10.2-Causal_Inference_for_Time_Series.txt`
  - [75%] Distribution shift, non-stationarity, temporal structure, confounding over time
- `msml610/lectures_source/Lesson08.3-Do_Calculus.txt`
  - [70%] Causal identification under confounding, backdoor and frontdoor criteria
- `msml610/lectures_source/Lesson02.3-ML_Techniques_Input_Processing.txt`
  - [65%] Data processing, handling outliers, missing data, normalization, feature engineering
- Not covered
  - [60%] Advanced measurement error correction, missing data mechanisms (MAR/MNAR specifics), covariate shift adaptation strategies

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
- `msml610/lectures_source/Lesson11.1-Decision_Making_with_Causal_Models.txt`
  - [95%] Utility functions, expected utility principle, causal interventions, decision networks, Bayesian decision-making
- `msml610/lectures_source/Lesson07.2-Posterior_Based_Decisions.txt`
  - [90%] Utility functions, expected utility, risk preferences, multi-criteria trade-offs, prior elicitation
- `msml610/lectures_source/Lesson12.1-Reinforcement_learning.txt`
  - [85%] Utility of states, Bellman equations, expected utility of policies, value iteration
- `msml610/lectures_source/Lesson09.3-Multi_Armed_Bandits.txt`
  - [80%] Sequential decision-making, exploration-exploitation, value of information, Bayesian optimization
- `msml610/lectures_source/Lesson07.1-Intro_to_Probabilistic_Programming.txt`
  - [75%] Bayesian models for decision-making, posterior-based choices, uncertainty in utility
- Not covered
  - [60%] Formal axiomatic foundations of utility theory, advanced risk-preference elicitation, cooperative game theory

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
- `msml610/lectures_source/Lesson11.1-Decision_Making_with_Causal_Models.txt`
  - [95%] Causal effects to expected value, Bayesian decision-making, value of information, exploration vs exploitation, robustness
- `msml610/lectures_source/Lesson09.3-Multi_Armed_Bandits.txt`
  - [90%] Thompson sampling, UCB, epsilon-greedy, contextual bandits, regret bounds, exploration-exploitation tradeoff
- `msml610/lectures_source/Lesson12.1-Reinforcement_learning.txt`
  - [85%] MDPs, value iteration, policy iteration, optimal decision-making under uncertainty
- `msml610/lectures_source/Lesson08.5-Experimentation.txt`
  - [80%] A/B testing, experimentation design, value of information, when to experiment vs observe, hybrid approaches
- `msml610/lectures_source/Lesson07.2-Posterior_Based_Decisions.txt`
  - [75%] Posterior-based choices, decision networks, value of information, Bayesian optimization
- `msml610/lectures_source/Lesson07.1-Intro_to_Probabilistic_Programming.txt`
  - [60%] Bayesian approaches to sequential decision-making, posterior updating
- Not covered
  - [50%] Distributional robustness, minmax optimization, advanced acquisition functions

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

### Foundational Algorithms for Decision-Making
- Bayesian Inference: Bayesian Networks, Variational Inference, Bayesian Neural Networks, MCMC
- Hidden State & Sequential Inference: HMM, Kalman Filter, Particle Filtering, POMDP, POMCP
- Bandit Algorithms: ε-Greedy, UCB, Thompson Sampling, Contextual Bandits
- Planning & Search: MCTS, Minimax/Alpha-Beta, A* Search, MPC, iLQR, RRT
- Core Value-Based RL: Q-Learning, SARSA, Value/Policy Iteration, DQN

### Lesson Materials
- `msml610/lectures_source/Lesson08.4.txt`
  - [95%] Heterogeneous treatment effects, CATE, individual treatment effects, causal forests, meta-learners (T, X, S, R learners)
- `msml610/lectures_source/Lesson08.5-Experimentation.txt`
  - [90%] Heterogeneous treatment effects, treatment effect variation across subgroups, policy evaluation
- `msml610/lectures_source/Lesson11.1-Decision_Making_with_Causal_Models.txt`
  - [85%] Off-policy learning, policy optimization, evaluating decisions from data
- `msml610/lectures_source/Lesson12.1-Reinforcement_learning.txt`
  - [80%] Off-policy RL, policy iteration, off-line learning, safe policy improvement
- `msml610/lectures_source/Lesson07.2-Posterior_Based_Decisions.txt`
  - [70%] Distributional effects, uncertainty in treatment effects, posterior predictive distributions
- Not covered
  - [60%] Doubly robust estimation details, R-learner specifics, safe policy improvement bounds

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

### Advanced Algorithms for Complex Multi-Step Decisions
- Policy-Based Algorithms: REINFORCE, PPO, TRPO, Natural Policy Gradient, Evolutionary Strategies
- Actor-Critic Methods: Actor-Critic Framework, A2C, A3C, DDPG, TD3, SAC
- Integrated Learning & Planning: Dyna-Q
- Deep RL & Foundational Models: AlphaGo, AlphaZero, MuZero, Hindsight Experience Replay
- Hierarchical & Modular Approaches: Hierarchical RL, Options Framework
- Offline/Batch Learning: Batch Q-Learning/Offline RL, Behavior Cloning, CQL
- Game Theory & Multi-Agent Algorithms: CFR, Nash Equilibrium Solvers, QMIX, MAPPO, MAAC, MADDPG, CommNet

### Lesson Materials
- `msml610/lectures_source/Lesson12.1-Reinforcement_learning.txt`
  - [95%] MDPs, multi-step planning, value iteration, policy iteration, dynamic decision networks, world models
- `msml610/lectures_source/Lesson08.4.txt`
  - [90%] Positivity, IPW, sensitivity analysis, feature selection dilemma, propensity score methods
- `msml610/lectures_source/Lesson10.2-Causal_Inference_for_Time_Series.txt`
  - [85%] Multi-step causal inference, feedback loops, dynamic systems, temporal planning
- `msml610/lectures_source/Lesson11.1-Decision_Making_with_Causal_Models.txt`
  - [80%] Robustness under uncertainty, causal generalization, model misspecification, sequential planning
- `msml610/lectures_source/Lesson09.1-Reasoning_over_time.txt`
  - [75%] Temporal reasoning, Markov processes, state transitions, temporal structure
- `msml610/lectures_source/Lesson07.2-Posterior_Based_Decisions.txt`
  - [60%] Uncertainty in sequential decisions, value of information
- Not covered
  - [50%] Partial identification bounds, Manski bounds specifics, E-values and sensitivity analysis

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
- `book.Agentic_AI/lectures_source/Lesson01.07-Tool_use_and_retrieval.txt`
  - [95%] Agent tool-use architecture, causal simulation, planning with external tools, grounded reasoning
- `book.Agentic_AI/lectures_source/Lesson01.04-LLM_Reasoning.txt`
  - [95%] Chain-of-thought variants, tree-of-thought, structured decomposition, verifiable reasoning chains
- `book.Agentic_AI/lectures_source/Lesson01.05-Reasoning_Memory_and_Planning.txt`
  - [90%] Planning ahead, world models, model-based planning, simulation-based decision-making, causal rollouts
- `book.Agentic_AI/lectures_source/Lesson01.01-What_Is_An_Agentic_AI.txt`
  - [90%] Agent architecture foundations, perception-decision-action loops, goal-directed systems
- `book.Agentic_AI/lectures_source/Lesson01.08-Learning_to_reason.txt`
  - [85%] Training reasoning capabilities, process reward models, causal reasoning in learned models
- `book.Agentic_AI/lectures_source/Lesson01.09_Post_training_and_verifiable_agents.txt`
  - [80%] Safety constraints, verification of agent behavior, guardrails for preventing harmful actions
- `book.Agentic_AI/lectures_source/Lesson01.11_Lessons_from_training_agentic_models.txt`
  - [75%] Practical insights on agentic model training, learned behavior patterns, feedback loop insights
- `book.Agentic_AI/lectures_source/Lesson01.10_Open_training_recipes_for_reasoning.txt`
  - [70%] Training approaches for reasoning, curriculum learning for causal reasoning
- `book.Agentic_AI/lectures_source/Lesson01.06-Inference_time_techniques.txt`
  - [70%] Search algorithms for planning, inference-time reasoning, exploring multiple causal paths
- `book.Agentic_AI/lectures_source/Lesson01.02-LLM_Building_Blocks.txt`
  - [50%] Foundation model capabilities and limitations relevant to causal reasoning
- `book.Agentic_AI/lectures_source/Lesson01.03-History_of_LLM_Agents.txt`
  - [40%] Historical evolution of agent concepts, context for understanding modern agentic systems
- Not covered
  - [20%] Specific online causal discovery algorithms, detailed performativity mathematics

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
- `msml610/lectures_source/Lesson08.1-Causal_AI_intro.txt`
  - [90%] Causal workflow with stakeholders, eliciting causal knowledge, hybrid teams, stakeholder alignment
- `msml610/lectures_source/Lesson12.2-Causal_Discovery.txt`
  - [85%] Using domain knowledge as constraints, combining discovery with expert judgment, validation
- `msml610/lectures_source/Lesson11.1-Decision_Making_with_Causal_Models.txt`
  - [80%] Communicating uncertainty to stakeholders, decision support, stakeholder alignment
- `msml610/lectures_source/Lesson08.2-Causal_Networks.txt`
  - [75%] Building causal DAGs with domain experts, causal assumptions, documenting assumptions
- `msml610/lectures_source/Lesson07.2-Posterior_Based_Decisions.txt`
  - [70%] Communicating uncertainty, prior elicitation, stakeholder preferences in utilities
- `msml610/lectures_source/Lesson08.4.txt`
  - [60%] Confounding, cost asymmetry, false positives vs negatives, robustness
- Not covered
  - [50%] Formal stakeholder elicitation methods, disagreement resolution protocols

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
- `msml610/lectures_source/Lesson08.5-Experimentation.txt`
  - [95%] A/B testing vs observational methods, continuous experimentation, sequential testing, policy improvement
- `msml610/lectures_source/Lesson11.1-Decision_Making_with_Causal_Models.txt`
  - [90%] Monitoring uncertainty, robustness under misspecification, feedback loops, learning from deployed decisions
- `msml610/lectures_source/Lesson12.1-Reinforcement_learning.txt`
  - [85%] Online learning, feedback loops, policy iteration, adaptive systems, model-based updates
- `msml610/lectures_source/Lesson10.2-Causal_Inference_for_Time_Series.txt`
  - [80%] Monitoring temporal stability, distribution shift detection, feedback loops over time
- `msml610/lectures_source/Lesson08.4.txt`
  - [75%] Effect heterogeneity monitoring, heterogeneous deployment, stratified rollout
- `msml610/lectures_source/Lesson09.1-Reasoning_over_time.txt`
  - [70%] Monitoring assumptions over time, temporal monitoring, updating beliefs from deployment
- `data605/lectures_source/Lesson02.3-Data_Pipelines.txt`
  - [60%] Production data pipelines, monitoring, alerting, technical infrastructure
- Not covered
  - [50%] Advanced monitoring dashboard design, comprehensive error budgeting, detailed rollback procedures

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
- `msml610/lectures_source/Lesson13.1-Explainability.txt`
  - [95%] Causal vs statistical explainability, SHAP, LIME, counterfactual explanations, distinguishing causal from correlational
- `msml610/lectures_source/Lesson08.2-Causal_Networks.txt`
  - [90%] Causal mechanisms, mediation analysis, direct vs indirect effects, counterfactual reasoning
- `book.Agentic_AI/lectures_source/Lesson01.09_Post_training_and_verifiable_agents.txt`
  - [85%] Safety constraints, verification, guardrails, preventing harmful behaviors, trustworthy AI
- `msml610/lectures_source/Lesson08.1-Causal_AI_intro.txt`
  - [80%] Interpretability, explainability, causal AI for trustworthy systems, transparency
- `msml610/lectures_source/Lesson11.1-Decision_Making_with_Causal_Models.txt`
  - [75%] Uncertainty communication, stakeholder trust, decision transparency
- `msml610/lectures_source/Lesson08.4.txt`
  - [70%] Fairness, disparate impact, effect heterogeneity across subgroups, bias
- `book.Agentic_AI/lectures_source/Lesson01.01-What_Is_An_Agentic_AI.txt`
  - [60%] Human-in-the-loop, decision oversight, agent transparency, safety
- Not covered
  - [50%] Regulatory compliance details (GDPR/EU AI Act specifics), formal governance frameworks, audit trail design

# Appendix
