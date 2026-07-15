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

## All Lesson Materials
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

- <Invariant>: for each chapter
  - Find the relevant material from the materials in `## All Lesson Materials`
    above to cover the corresponding `### Topics`
  - Use the template below

### Topics
- Topic 1
  - Subtopic 1.1
  - Subtopic 1.2
- Topic 2
  ...

### Lesson Materials
- `pointer to a lecture`
  - [<Amount of the lecture material covering this chapter>]: <topics>
- `book_springer/lectures_source/Lesson01.02_Integrating_Causality_And_Probability_in_ML.txt`
  - [100%]: Integration of causality and uncertainty into ML systems, moving beyond correlation
- Not covered
  - [<Amount of topics not covered by any lesson>]: <topics>

# Detailed TOC

# Part I: Why Businesses Need Decisions, not Predictions (Motivation)

## 00: Introduction

### Topics
- The Decision Pipeline Framework
  - From raw data to prediction to causal effect estimation to utility-maximizing policy
  - Feedback loops and learning from outcomes
  - Why each stage matters and what breaks when stages are skipped
- Why Traditional ML Falls Short for Decision-Making
  - Predictive accuracy ≠ decision quality: optimizing the wrong metric
  - Four critical gaps: causality, uncertainty, business objectives, dynamics
  - Real-world costs of ignoring each gap
- Causal Reasoning as the Bridge
  - Moving beyond correlation to counterfactual reasoning
  - What "causal" means in practice and why it matters
  - Why domain experts and formal models are both necessary
- Uncertainty as Signal, Not Noise
  - Decision-relevant variance: what point estimates hide
  - Confidence vs. credibility: when estimates are trustworthy
  - Overconfidence: systems that never say "I don't know"
- How This Book Is Organized
  - Five-part structure: motivation, theory, data, algorithms, deployment/governance
  - Intended audience and prerequisites
  - How chapters build on each other and fit into the decision pipeline

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
- Course Roadmap
  - The decision pipeline: data → model → policy → action → feedback loops
  - Five-part book structure (motivation, theory, data, algorithms, deployment)
- Why Traditional ML Falls Short
  - Four critical gaps: causality, uncertainty, business objectives, dynamics
  - Real-world costs of ignoring each gap
- From Data Science to Decision Science
  - Predictive paradigm: optimize accuracy on held-out test data
  - Decision paradigm: optimize business value of actions taken
- Causal vs Predictive Questions
  - Predictive form: "What will happen if we observe X?"
  - Causal form: "What will happen if we intervene and set X?"
- The Analytics Maturity Ladder
  - Level 0 (Descriptive): "What happened in the past?"
  - Level 1 (Predictive): "What will likely happen?"
  - Level 2 (Causal): "What will happen if we intervene?"
  - Level 3 (Decision): "What should we do?"

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

## 02: The Cost of Ignoring Causality, Uncertainty and Dynamics

### Topics
- When Correlation Misleads
  - Confounding: $\Pr(Y | X) \neq \Pr(Y | do(X))$ when unobserved variables affect both X and Y
  - Missing counterfactuals: observational models cannot answer "what if we intervene?" questions
  - Selection bias: incomplete historical populations hide causal mechanisms
- Structural Failure Modes
  - Interference and spillovers: SUTVA violations when units interact (marketplaces, networks)
  - Simpson's Paradox: aggregates reverse while subgroups show consistent effects
  - Collider bias: conditioning on outcomes creates spurious correlations (Berkson's paradox)
  - Mechanistic blindness: pattern-driven models inherit artifacts from training data
- Point Estimates in a Small-Data World
  - Single numbers hide decision-relevant variance; error bars are essential
  - Epistemic vs. aleatoric uncertainty: conflating known unknowns with unknown unknowns
  - Overconfidence off-distribution: systems that never say "I don't know" fail on novel inputs
  - Statistical traps: p-hacking, multiple comparisons, test set reuse, peeking at data

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
  - Symbolic logic: propositional and first-order logic for structured reasoning
  - Ontologies and semantic networks: organizing domain knowledge
  - Logic-based agents: inference engines and rule-based systems
- Graphical Models for Uncertainty
  - Bayesian networks: encoding conditional independence and probabilistic structure
  - D-separation and Markov blankets: reading independence from graphs
  - Inference algorithms: belief propagation and variable elimination
- Causal Graphical Models
  - Structural causal models (SCMs): formal representation of mechanisms
  - DAGs: encoding causal order, observed vs. unobserved variables
  - Identifying confounders, mediators, colliders from graph structure
- Integrating Logic and Causality
  - Combining symbolic reasoning with probabilistic inference
  - From correlation to causal reasoning: what graphs add beyond data

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
  - Bayesian framework: updating beliefs from prior and data
  - Frequentist vs. Bayesian views: philosophical differences and practical implications
  - Prior specification and elicitation: encoding domain knowledge
- Inference in Probabilistic Models
  - Exact algorithms: belief propagation, variable elimination for graphical models
  - Approximate inference: sampling, variational inference, MCMC for complex models
  - Probabilistic programming: languages and tools (PyMC, Pyro, Stan)
- Bayesian Generative Models
  - Linear regression: uncertainty quantification via posterior distributions
  - Logistic regression and classification: Bayesian approach
  - Hierarchical models: multi-level structure and pooling information across groups
  - Regularization via priors: soft constraints on parameters
- Uncertainty in Predictions
  - Posterior predictive distributions: averaging over model uncertainty
  - Epistemic vs. aleatoric uncertainty: model uncertainty vs. irreducible noise
  - Posterior predictive checks: validating model fit against data
- Bayesian Decision-Making
  - Expected utility: maximizing decision value under posterior uncertainty
  - Loss functions and utility encoding: connecting preferences to parameters
  - Sequential decision-making: updating beliefs and acting
- Model Comparison and Selection
  - Information criteria (AIC, BIC, WAIC): balancing fit and complexity
  - Cross-validation and out-of-sample error: evaluating generalization
  - Bayes factors and hypothesis testing: comparing model hypotheses
  - Model ensembles: combining multiple models for robustness

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
  - Structural causal models (SCMs): formal specification of mechanisms
  - DAGs: encoding causal order, variable dependencies, latent confounders
  - Identifying confounders, mediators, colliders from graph structure
- Do-Calculus and Interventional Reasoning
  - The do-operator: distinguishing intervention from observation
  - Transforming observational queries into interventional quantities
  - Three rules of do-calculus: identifying when interventions are identifiable
- Identification Criteria
  - Back-door criterion: adjusting for confounders to identify effects
  - Front-door criterion: handling unobserved confounding via mediators
  - D-separation: reading conditional independence from causal graphs
- Advanced Identification Methods
  - Instrumental variables: leveraging exogenous variation to break confounding
  - Sensitivity analysis: quantifying robustness to unmeasured confounding
  - Identifying limits: when causal effects are unidentifiable from data
- Causal Discovery from Observational Data
  - Learning causal DAGs from observational data without experiments
  - Constraint-based methods: using conditional independence tests
  - Score-based methods: searching over graph structures
  - Markov equivalence: understanding discovery limits from observational data

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
- Eliciting Causal Knowledge from Experts
  - Structured elicitation methods and expert judgment techniques
  - Iterative refinement: cycling between experts and data
  - Handling disagreement and uncertainty among stakeholders
- Building Causal DAGs
  - Variable selection: identifying relevant nodes and boundaries
  - Encoding causal assumptions: direction, mechanisms, feedback
  - Graph construction: translating domain knowledge into formal structure
- Variable Types and Relationships
  - Confounders: common causes that bias estimation
  - Mediators: mechanisms through which effects operate
  - Colliders: outcomes of multiple causes; conditioning dangers
  - Moderators: variables that change effect size across subgroups
- Temporal Structure
  - Causal order: establishing precedence and acyclicity
  - Feedback delays: when current outcomes influence future causes
  - Dynamic systems: modeling evolution over time
- Measurement and Operationalization
  - Defining variables: translating concepts to measurable quantities
  - Proxy variables: when direct measurement impossible
  - Validity assessment: does the proxy capture the construct?
- Documenting Assumptions
  - Transparency: making causal structures explicit and testable
  - Validation: checking assumptions against domain knowledge and data
  - Stakeholder alignment: ensuring shared understanding of causal structure

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
- Data Collection and Its Biases
  - Collection design: how sampling and measurement choices shape data
  - Selection mechanisms: who and what is captured vs. missed
  - Confounder introduction: biases built into acquisition process
- Selection Bias and Incomplete Populations
  - Missing data mechanisms: MCAR (random), MAR (depends on observed), MNAR (depends on unobserved)
  - Subgroup representation: historical data misses critical populations
  - Impact on causal inference: incomplete data breaks identifiability assumptions
- Distribution Shift and Covariate Mismatch
  - Training vs. production: when learned causal effects fail in new environments
  - Concept drift: non-stationary relationships over time
  - Detecting shift: monitoring data distributions for changes
- Measurement Error and Proxy Validity
  - Proxy variable quality: does the proxy capture the true construct?
  - Attenuation: measurement error weakens causal effect estimates
  - Correction methods: debiasing estimates under known measurement error
- Pre-Flight Checks
  - Data quality validation: assessing completeness, accuracy, consistency
  - Confounder balance: checking covariate distributions match assumptions
  - Assumption diagnostics: verifying causal identification conditions hold
- Data Quality for Causal Inference
  - Handling missingness: understanding patterns and implications
  - Outlier detection: distinguishing errors from true anomalies
  - Robust inference: methods that work under imperfect data

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
- Von Neumann-Morgenstern Axioms
  - Rational choice axioms: completeness, transitivity, continuity, independence
  - Utility existence theorem: rational preferences representable as utility function
  - Implications: why expected utility is the right framework
- Utility Functions in Practice
  - Eliciting preferences: methods for extracting stakeholder objectives
  - Encoding business value: linking decisions to monetary or non-monetary outcomes
  - Designing utility: avoiding common pitfalls in preference specification
- Subjective Expected Utility
  - Belief + Preference: combining uncertainty (beliefs) with values (preferences)
  - Bayesian updating: revising beliefs from new information
  - Decision rules: how to choose actions under posterior uncertainty
- Multi-Criteria Trade-Offs
  - Value functions: combining multiple objectives into single metric
  - Pareto optimality: solutions that dominate no alternatives
  - Weight elicitation: balancing competing criteria
- Influence Diagrams and Decision Networks
  - Graphical representation: nodes for decisions, uncertainties, values
  - Backward induction: solving networks to extract optimal policies
  - Value of information: computing worth of additional observations
- Risk Preferences and Utility Curvature
  - Risk aversion: decreasing marginal utility of wealth
  - Risk neutrality: linear utility function
  - Risk seeking: increasing marginal utility (rare, context-dependent)

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
- From Causal Effects to Expected Value
  - Causal effect estimates: treatment effects on outcomes
  - Utility encoding: translating effects into decision value
  - Decision rule: maximizing expected utility over actions
- Bayesian Decision-Making
  - Posterior-based choices: using full posterior distribution, not point estimates
  - Belief updating: iterative learning from data
  - Sequential decisions: adapting choices as information arrives
- Value of Information
  - EVPI (perfect information): upper bound on experimentation value
  - EVSI (sample information): value of specific experiments
  - When to experiment: comparing cost of experiment vs. value of learning
- Bayesian Optimization and Acquisition Functions
  - Efficient exploration: guided search over high-dimensional decision spaces
  - Acquisition functions: balancing exploitation (use what works) and exploration
  - Active learning: selecting experiments intelligently
- Exploration vs. Exploitation
  - Thompson sampling: drawing from posterior beliefs and acting
  - Upper confidence bound (UCB): balancing uncertainty and performance
  - Contextual bandits: making decisions conditional on context
- Counterfactual Decision Analysis
  - Alternative scenarios: "What if we had chosen differently?"
  - Causal reasoning about decisions: understanding decision consequences
  - Regret analysis: evaluating decision quality retrospectively
- Robustness Under Misspecification
  - Decisions under model uncertainty: when causal assumptions may be wrong
  - Minimax and distributional robustness: hedging against unknown unknowns
  - Sensitivity analysis: how much do conclusions change with assumptions?

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
- **Bayesian Inference for Decisions**: Reasoning about uncertainty over model parameters and predictions using Bayesian networks, variational inference, and MCMC; encoding prior knowledge and updating beliefs from data to support decision-making under partial information
- **Sequential Inference with Hidden State**: Tracking unobserved system state over time using HMMs, Kalman filters, and particle filters; partially observable decision problems (POMDPs) where decisions must be made without full observability
- **Bandit Algorithms**: Sequential decision-making with online exploration-exploitation tradeoff; algorithms (ε-greedy, UCB, Thompson sampling, contextual variants) that learn which actions are best while maintaining uncertainty over alternatives
- **Planning and Search**: Deterministic and stochastic planning methods (MCTS, minimax, A* search, MPC) for finding near-optimal action sequences when the decision horizon is finite and environment dynamics are known
- **Value-Based Reinforcement Learning**: Learning optimal policies from trial-and-error experience using value functions (Q-learning, SARSA, value/policy iteration, DQN); applicable when rewards are delayed and environment structure is learned from interaction

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
- **Policy-Based and Gradient Methods**: Directly parameterizing and optimizing decision policies using gradient ascent (REINFORCE, PPO, TRPO, natural policy gradient); applicable to high-dimensional or continuous action spaces where value-based methods struggle
- **Actor-Critic Architectures**: Combining value estimation (critic) with policy optimization (actor) for stable, efficient learning; practical algorithms (A2C, A3C, DDPG, TD3, SAC) that balance bias-variance and sample efficiency in continuous control
- **Planning with Learned Models**: Integrating learning (model identification) and planning (lookahead) in the same agent; algorithms like Dyna-Q that use imagined rollouts to accelerate policy improvement
- **Deep Reinforcement Learning and Search**: Scaling decision-making to high-dimensional state spaces via neural networks combined with search (AlphaGo, AlphaZero, MuZero); learning world models that enable long-horizon reasoning
- **Hierarchical and Modular Decision-Making**: Decomposing complex decisions into subtasks or options; hierarchical abstractions that make long-horizon planning tractable and enable knowledge reuse across related problems
- **Offline and Batch Learning**: Learning policies from logged data without interaction; addressing distribution mismatch between behavior policy and learned policy; algorithms (batch Q-learning, offline RL, behavior cloning, CQL) for decision-making from observational data
- **Multi-Agent and Game-Theoretic Algorithms**: Reasoning about decisions when multiple agents interact; Nash equilibrium solvers (CFR), coordination methods (QMIX, CommNet), and policy distribution learning (MAPPO, MAAC, MADDPG) for competitive and cooperative settings

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
- Causal Reasoning in LLMs
  - Pattern-based limits: why foundation models struggle with counterfactuals
  - Knowledge vs. reasoning: language models know facts but may not reason causally
  - In-context learning: eliciting causal reasoning via prompting
- Chain-of-Thought and Tree-of-Thought Prompting
  - Structured reasoning: breaking problems into steps
  - Causal decomposition: reasoning about mechanisms explicitly
  - Verification: checking causal chains for consistency
- SCM-Augmented Agents
  - Embedding causal world models: agents that understand mechanisms
  - Model-based reasoning: planning using causal models of environment
  - Integration with learning: updating SCMs from experience
- Tool-Use and Causal Simulation
  - External tools: calculators, simulators, retrieval systems
  - Causal simulation: planning by running forward models
  - Grounding reasoning: connecting abstract reasoning to executable actions
- Integrating Causality with Probabilistic Inference
  - Hybrid reasoning: combining symbolic causal models with learned probabilities
  - Joint planning: reasoning about both what will happen and what we should do
  - Uncertainty quantification: maintaining belief distributions over causal structures
- Trustworthy Agentic AI
  - Transparency: explaining agent decisions causally
  - Robustness: decisions that work under causal assumption violations
  - Fairness: ensuring decisions treat groups equitably
- Performativity and Adaptive Systems
  - Decisions that change the world: acknowledging feedback from actions
  - Adaptive learning: updating models based on outcome observations
  - Avoiding traps: recognizing when interventions alter underlying distributions
- Online Causal Discovery
  - Learning from deployment: discovering causal structures from live data
  - Iterative refinement: updating DAGs as new evidence arrives
  - Stability guarantees: maintaining safe assumptions during learning

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
- Eliciting Causal Knowledge from Experts
  - Structured methods: interviews, surveys, consensus-building
  - Handling disagreement: when experts disagree on causal structure
  - Iterative refinement: cycling between expert input and data validation
- Stakeholder Feedback During Development
  - Intermediate results: sharing findings and getting expert critique
  - Sensitivity analyses: showing impact of assumption changes
  - Refinement loop: updating DAGs based on feedback
- Communicating Causal Assumptions
  - Audience targeting: tailoring message for experts vs. operations vs. leadership
  - Precision without jargon: explaining technical concepts accessibly
  - Honest uncertainty: being clear about what is known vs. assumed
- Causal DAG Visualization and Debate
  - Graphical representation: making causal structures visible and debatable
  - Disagreement resolution: protocols for handling conflicting opinions
  - Documentation: recording assumptions and decisions
- Sensitivity Analysis as Communication Tool
  - Robustness demonstration: showing decisions work across assumptions
  - Threshold identification: finding breaking points in assumptions
  - Stakeholder confidence: building trust through thorough analysis
- Intervention Design Communication
  - Lever identification: which variables can we actually control?
  - Justification: why these interventions are causal levers
  - Trade-offs: costs, side effects, feasibility of different options
- Risk Tolerance and Cost Asymmetry
  - False positives vs. false negatives: aligning on acceptable error rates
  - Business impact: tying decision errors to business consequences
  - Stakeholder agreement: consensus on acceptable risk levels
- Stakeholder Buy-In Before Deployment
  - Model adequacy review: does the model capture the business problem?
  - Assumption sign-off: stakeholders endorse causal structure
  - Go/no-go decision: readiness for production deployment

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
- From Notebook to Production
  - Infrastructure: moving models from experimentation to operational systems
  - Data pipelines: integrating real-time data streams
  - Latency and throughput: meeting production performance requirements
- Cost-Aware Deployment Strategies
  - Phased rollout: gradual expansion to manage risk
  - Shadow mode: running model in parallel without affecting decisions
  - Canary analysis: testing on small user subsets before full deployment
  - Cost asymmetry: tailoring rollout to false positive vs. false negative costs
- Monitoring Causal Assumptions
  - Directly testable: effect stability, proxy validity, heterogeneity patterns
  - Indirectly testable: sensitivity bounds, negative controls, balancing checks
  - Domain-assessed: causal structure validity (periodic expert review)
  - Dashboards: alerting on threshold violations and assumption breakdown
- A/B Testing vs. Observational Methods
  - When to experiment: high-uncertainty decisions warrant experiment cost
  - When to trust causal models: observational methods faster but riskier
  - Hybrid approaches: combining both for robustness
- Continuous Experimentation
  - Sequential testing: running experiments iteratively as data arrives
  - Exploration vs. exploitation: balancing learning and decision value
  - Policy improvement: incremental updates based on experimental evidence
- Heterogeneous Deployment
  - Effect heterogeneity: recognizing treatment effects vary across subgroups
  - Stratified rollout: different policies for different segments
  - Monitoring divergence: detecting when effect heterogeneity changes
- Versioning and Rollback
  - Error budgets: acceptable decision error thresholds
  - Model versioning: tracking causal assumptions and model changes
  - Rollback procedures: reverting to previous models when failures detected
- Feedback Loops and Adaptation
  - Learning from deployed decisions: updating models from real outcomes
  - Concept drift: adapting to changes in causal relationships
  - Iterative refinement: continuous improvement over time
- Technical Debt and Maintenance
  - System reliability: monitoring and fixing technical issues
  - Documentation: keeping causal assumptions and decisions documented
  - Legacy management: managing old systems and transitions

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
- Building Trust
  - Transparency: making decisions and assumptions visible
  - Stakeholder alignment: shared understanding of decision rationale
  - Justified confidence: earned trust through evidence and validation
- Causal vs. Statistical Explainability
  - Causal explainability: "Why did we intervene?" via mechanisms and counterfactuals
  - Statistical explainability: "What features correlated?" via SHAP, LIME, importance
  - Risks of confusion: confounders ranked high by SHAP but not actionable levers
  - Danger zone: conflating correlation importance with causal relevance
- Operationalizing Causal Explanations
  - Serve-time explanations: generating reasons for individual decisions
  - Mechanism-based: explaining via causal paths, not feature ranks
  - Stakeholder communication: tailoring explanations to audience
- Identifying Failure Modes
  - Runtime detection: when decisions fail in production
  - Root causes: model misspecification, distribution shift, assumption breakdown
  - Diagnosis vs. prevention: post-facto diagnosis vs. proactive monitoring
  - Emergency response: rapid detection and rollback
- Fairness Under Deployment
  - Disparate impact: preventing systematic harm to groups
  - Fairness monitoring: tracking outcomes across subgroups
  - Heterogeneous effects: recognizing treatment effects vary, planning accordingly
  - Fairness-robustness tradeoff: balancing group fairness and model accuracy
- Override Procedures and Human-in-the-Loop
  - Escalation mechanisms: when and how to flag decisions for human review
  - Decision disputes: protocols for challenging system recommendations
  - Trust calibration: knowing when to rely on vs. override the system
- Failure Detection and Response
  - Monitoring systems: dashboards and alerts for anomalies
  - Root cause analysis: diagnosing why failures occurred
  - Remediation: fixing root causes, not just symptoms
- Decision Governance and Audit Trails
  - Documentation: who approved decisions, what assumptions were made
  - Audit trails: logging decisions and outcomes for accountability
  - Change history: tracking model versions and deployment decisions
  - Impact assessment: understanding consequences of decisions
- Regulatory and Compliance Alignment
  - Regulatory landscape: GDPR, EU AI Act, fairness standards, compliance frameworks
  - Documentation requirements: causal assumptions, deployment decisions, override logs
  - Audit preparation: demonstrating compliance and responsible use
  - Lawyer coordination: knowing when to involve legal/compliance teams
- Guardrails and Safety Constraints
  - Harmful behavior prevention: blocking dangerous decisions
  - Assumption safeguards: enforcing causal structure constraints
  - Edge case management: handling distribution tails and anomalies
  - Graceful degradation: safe fallbacks when systems fail

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
