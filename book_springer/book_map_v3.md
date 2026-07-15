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

- <Invariant>: each `### Topics` for each chapter should be in 
  nested bullet points
  - Level 1 bullets: the title of the subchapter
  - Level 2 bullets: a short list of topics
- The `### Topics` should be less than 20 lines and 175 words

### Topics
- Topic 1
  - Subtopic 1.1
  - Subtopic 1.2
- Topic 2
  ...

- <Invariant>: for each chapter
  - Find the relevant material from the materials listed abo]e in `## All Lesson
    Materials` to cover the corresponding `### Topics`
  - Use the template below

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
  - From raw data to prediction to causal effect estimation to utility-maximizing
    policy
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
  - Five-part structure: motivation, theory, data, algorithms,
    deployment/governance
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
  - Running example: one decision revisited across the book
- Why Traditional ML Falls Short
  - Four critical gaps: causality, uncertainty, business objectives, dynamics
  - Real-world costs of ignoring each gap
  - Case vignette: a high-accuracy churn model with negative-ROI offers
- From Data Science to Decision Science
  - Predictive paradigm: optimize accuracy on held-out test data
  - Decision paradigm: optimize business value of actions taken
  - Organizational shift: incentives move from accuracy to decision value
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
  - Confounding: unobserved variables bias both X and Y
  - Missing counterfactuals: no way to answer "what if we intervene?"
  - Selection bias: incomplete populations hide causal mechanisms
  - Reverse causality: correlation can't distinguish X to Y from Y to X
- Structural Failure Modes
  - Interference and spillovers: SUTVA violations in networks
  - Simpson's Paradox: aggregates reverse subgroup trends
  - Collider bias: conditioning on outcomes creates spurious links
  - Mechanistic blindness: models inherit training-data artifacts
- Point Estimates in a Small-Data World
  - Single numbers hide decision-relevant variance
  - Epistemic vs. aleatoric uncertainty: known vs. unknown unknowns
  - Overconfidence off-distribution: never saying "I don't know"
  - Statistical traps: p-hacking, multiple comparisons, peeking at data
  - Silent failure cost: confident decisions on wide error bars
- The Cost of Ignoring Dynamics
  - Static models assumed frozen while conditions drift
  - Feedback loops and performativity reshape training distributions
  - Myopic optimization ignores long-horizon consequences

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
  - Ontologies and semantic networks: organizing domain knowledge into reusable structures
  - Logic-based agents: inference engines and rule-based reasoning systems
- Graphical Models for Uncertainty
  - Bayesian networks: encoding conditional independence and probabilistic structure
  - D-separation and Markov blankets: reading independence directly from graph topology
  - Inference algorithms: belief propagation and variable elimination for exact answers
- Causal Graphical Models
  - Structural causal models (SCMs): formal representation of generative mechanisms
  - DAGs: encoding causal order, observed vs. unobserved variables, edge direction
  - Identifying confounders, mediators, and colliders directly from graph structure
- Integrating Logic and Causality
  - Combining symbolic reasoning with probabilistic inference for hybrid systems
  - From correlation to causal reasoning: what graphs add beyond raw data
  - Choosing a representation: when logic, probability, or causal graphs fit best
- Representation as a Foundation for Decisions
  - Why representation choice shapes what questions a model can answer
  - Connecting knowledge representation to the causal ML techniques in later chapters

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
- Bayesian Inference Foundations
  - Bayesian framework: updating beliefs from priors as new data arrives
  - Frequentist vs. Bayesian views: philosophical differences with practical modeling implications
  - Approximate inference: sampling, variational inference, and MCMC for intractable posteriors
- Bayesian Generative Models
  - Linear and logistic regression: posterior-based uncertainty over parameters
  - Hierarchical models: multi-level structure pooling information across groups
  - Regularization via priors: soft constraints that shrink unstable estimates
- Uncertainty in Predictions
  - Posterior predictive distributions: averaging predictions over model uncertainty
  - Epistemic vs. aleatoric uncertainty: model uncertainty vs. irreducible noise
  - Posterior predictive checks: validating model fit against observed data
- Bayesian Decision-Making
  - Expected utility: maximizing decision value under posterior uncertainty
  - Loss functions: connecting stakeholder preferences to model parameters
  - Sequential decision-making: updating beliefs and acting as evidence arrives
- Model Comparison and Selection
  - Information criteria (AIC, BIC, WAIC): balancing model fit and complexity
  - Cross-validation: evaluating out-of-sample generalization performance
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
  - Structural causal models (SCMs): formal specification of generative mechanisms
  - DAGs: encoding causal order, variable dependencies, and latent confounders
  - Identifying confounders, mediators, and colliders from graph structure
- Do-Calculus and Interventional Reasoning
  - The do-operator: distinguishing intervention from passive observation
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
  - Learning causal DAGs without running experiments
  - Constraint-based and score-based search methods over graph space
  - Markov equivalence: understanding the limits of discovery from data alone

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
  - Structured elicitation methods, refined iteratively against incoming data
  - Handling disagreement among stakeholders about the causal structure
  - Documenting and validating assumptions before they enter the model
- Building Causal DAGs
  - Variable selection: identifying relevant nodes and system boundaries
  - Encoding causal assumptions: direction, mechanisms, and feedback paths
  - Translating domain knowledge into a formal graphical structure
- Variable Types and Relationships
  - Confounders: common causes that bias effect estimation
  - Mediators and moderators: mechanisms and shifts in effect size
  - Colliders: variables where conditioning creates spurious associations
- Temporal Structure
  - Causal order: establishing precedence and acyclicity among variables
  - Feedback delays: current outcomes influencing future causes over time
  - Dynamic systems: modeling how causal relationships evolve
- Measurement and Operationalization
  - Defining variables: translating abstract concepts into measurable quantities
  - Proxy variables: substitutes used when direct measurement is impossible
  - Validity assessment: checking whether the proxy captures the construct

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
  - Collection design: how sampling and measurement choices shape the data
  - Selection mechanisms: who and what gets captured versus missed
  - Confounder introduction: biases built into the acquisition process itself
- Selection Bias and Incomplete Populations
  - Missing data mechanisms: MCAR, MAR, and MNAR patterns
  - Subgroup representation: historical data often misses critical populations
  - Impact on causal inference: incomplete data breaks identifiability assumptions
- Distribution Shift and Covariate Mismatch
  - Training vs. production: causal effects fail to hold in new environments
  - Concept drift: non-stationary relationships that change over time
  - Detecting shift: monitoring input distributions for meaningful changes
- Measurement Error and Proxy Validity
  - Proxy quality: does the proxy actually capture the true construct?
  - Attenuation: measurement error systematically weakens causal effect estimates
  - Correction methods: debiasing estimates under known measurement error
- Pre-Flight Data Quality Checks
  - Confounder balance: checking covariate distributions match assumptions
  - Missingness and outlier detection before modeling begins
  - Robust inference: methods that tolerate imperfect, noisy data

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
  - Rational choice axioms: completeness, transitivity, continuity, and independence
  - Utility existence theorem: rational preferences representable as a utility function
  - Why expected utility is the mathematically correct decision framework
- Utility Functions in Practice
  - Eliciting preferences: methods for extracting stakeholder objectives
  - Multi-criteria trade-offs: combining value functions toward Pareto optimality
  - Designing utility functions while avoiding common specification pitfalls
- Subjective Expected Utility
  - Belief plus preference: combining uncertainty with stakeholder values
  - Bayesian updating: revising beliefs as new information arrives
  - Decision rules: how to choose actions under posterior uncertainty
- Influence Diagrams and Decision Networks
  - Graphical representation: nodes for decisions, uncertainties, and values
  - Backward induction: solving decision networks for optimal policies
  - Value of information: computing the worth of additional observations
- Risk Preferences and Utility Curvature
  - Risk aversion: decreasing marginal utility of wealth
  - Risk neutrality: a linear utility function over outcomes
  - Risk seeking: increasing marginal utility, rare and context-dependent

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
  - Treatment effect estimates translated directly into decision value
  - Utility encoding: mapping causal effects onto a decision-relevant scale
  - Decision rule: choosing the action that maximizes expected utility
- Bayesian Decision-Making and Value of Information
  - Posterior-based choices: using the full distribution, not point estimates
  - EVPI/EVSI: value of perfect information versus sample information
  - Sequential decisions: adapting choices as new information arrives
- Exploration vs. Exploitation
  - Thompson sampling and UCB: balancing uncertainty against performance
  - Contextual bandits: making decisions conditional on observed context
  - Bayesian optimization: acquisition functions guiding efficient search
- Counterfactual Decision Analysis
  - Alternative scenarios: "What if we had chosen differently?"
  - Causal reasoning about the consequences of past decisions
  - Regret analysis: evaluating decision quality after the fact
- Robustness Under Misspecification
  - Decisions made under uncertainty about model correctness
  - Minimax and distributional robustness against unknown unknowns
  - Sensitivity analysis: how much conclusions change with assumptions

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
- Bayesian Inference for Decisions
  - Reasoning over model uncertainty: Bayesian networks, variational inference, MCMC
  - Encoding prior knowledge: updating beliefs as evidence arrives
  - Deciding under partial information: posterior uncertainty plus decision rules
- Sequential Inference with Hidden State
  - Tracking unobserved state: HMMs, Kalman filters, particle filters
  - Partially observable decision problems (POMDPs): acting without full observability
  - Belief states: a sufficient statistic for decisions over hidden state
- Bandit Algorithms
  - Exploration-exploitation tradeoff: learning about actions vs. exploiting known-good ones
  - Algorithm family: epsilon-greedy, UCB, Thompson sampling, contextual bandits
  - Regret: minimizing cumulative loss while learning
- Planning and Search
  - Deterministic planning: A* search and model predictive control (MPC)
  - Stochastic and adversarial planning: Monte Carlo tree search (MCTS), minimax
  - Finite-horizon assumption: near-optimal sequences under known, bounded dynamics
- Value-Based Reinforcement Learning
  - Value functions: Q-learning, SARSA, value and policy iteration
  - Deep value-based methods: DQN and function approximation for large states
  - Delayed rewards: learning environment structure from sparse feedback

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
- Policy-Based and Actor-Critic Methods
  - Direct policy parameterization via gradient ascent: REINFORCE, PPO, TRPO
  - Actor-critic stability: combining value and policy in A2C, A3C, DDPG, TD3, SAC
  - High-dimensional and continuous action spaces where value-based methods struggle
- Planning with Learned Models and Deep Search
  - Model-based planning: Dyna-Q style imagined rollouts accelerate learning
  - Neural networks combined with tree search: AlphaGo, AlphaZero, MuZero
  - World models: learned dynamics enabling long-horizon reasoning
- Hierarchical and Modular Decision-Making
  - Decomposing complex decisions into subtasks, options, and temporal abstraction
  - Hierarchical abstractions that reduce the effective planning horizon
  - Knowledge reuse: transferring learned subpolicies across related problems
- Offline and Batch Learning
  - Learning from logged data with no live environment interaction
  - Distribution mismatch: divergence between behavior and learned policies
  - Algorithm family: batch Q-learning, offline RL, and CQL
- Multi-Agent and Game-Theoretic Algorithms
  - Reasoning about decisions when other agents are also acting
  - Equilibrium and coordination: Nash equilibrium solvers (CFR), QMIX, CommNet
  - Competitive and cooperative learning: MAPPO, MAAC, MADDPG

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
  - Knowledge vs. reasoning: knowing facts does not mean reasoning causally
  - In-context learning: eliciting causal reasoning through careful prompting
- Structured Prompting and SCM-Augmented Agents
  - Chain-of-thought and tree-of-thought: causal decomposition and verification
  - Embedding causal world models directly into agent architectures
  - Model-based reasoning: planning using explicit causal models
- Tool-Use and Causal Simulation
  - External tools: calculators, simulators, and retrieval systems
  - Causal simulation: planning by running forward models
  - Grounding reasoning: connecting abstract plans to executable actions
- Trustworthy and Adaptive Agentic AI
  - Transparency and fairness in agent decision-making
  - Performativity: decisions that change the world they act on
  - Adaptive learning: updating models based on observed outcomes
- Probabilistic Integration and Online Discovery
  - Hybrid reasoning: combining symbolic causal models with learned probabilities
  - Uncertainty quantification maintained over causal structure itself
  - Online discovery: learning causal DAGs from live deployment data

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
- Eliciting and Refining Causal Knowledge
  - Structured methods: interviews, surveys, and consensus-building workshops
  - Handling disagreement: reconciling conflicting views among domain experts
  - Iterative refinement: cycling between expert input and data validation
- Communicating Causal Assumptions
  - Audience targeting: tailoring the message for experts, operations, leadership
  - Precision without jargon: explaining technical concepts accessibly
  - DAG visualization: making causal structures visible and open to debate
- Sensitivity Analysis as Communication Tool
  - Robustness demonstration: showing decisions hold across plausible assumptions
  - Threshold identification: finding the breaking points in assumptions
  - Building stakeholder confidence through transparent, thorough analysis
- Intervention Design and Risk Alignment
  - Lever identification: determining which variables can actually be controlled
  - Trade-offs: weighing costs, side effects, and feasibility of options
  - Cost asymmetry: aligning stakeholders on acceptable error rates
- Stakeholder Buy-In Before Deployment
  - Model adequacy review: does the model capture the business problem?
  - Assumption sign-off: stakeholders formally endorse the causal structure
  - Go/no-go decision: assessing readiness for production deployment

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
  - Data pipelines: integrating real-time data streams into serving
  - Latency and throughput requirements for production performance
- Cost-Aware Rollout and Experimentation
  - Phased rollout, shadow mode, and canary analysis to manage risk
  - A/B testing vs. observational methods, combined in hybrid approaches
  - Continuous experimentation: sequential testing and incremental policy improvement
- Monitoring Causal Assumptions
  - Directly testable signals: effect stability and proxy validity
  - Indirectly testable signals: sensitivity bounds and negative controls
  - Dashboards: alerting when assumptions begin to break down
- Heterogeneous Deployment, Versioning, and Rollback
  - Stratified rollout across segments with different treatment effects
  - Error budgets and model versioning to track changes over time
  - Rollback procedures triggered when failures are detected
- Feedback, Adaptation, and Technical Debt
  - Learning from deployed decisions and adapting to concept drift
  - Iterative refinement of models and assumptions over time
  - System reliability, documentation, and management of legacy components

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
- Building Trust and Explainability
  - Transparency and justified confidence earned through evidence
  - Causal vs. statistical explainability: mechanisms versus SHAP and LIME
  - Serve-time explanations: mechanism-based and tailored to the audience
- Identifying and Responding to Failures
  - Runtime detection: root causes in misspecification and distribution drift
  - Diagnosis versus proactive monitoring of production behavior
  - Emergency response: rapid detection followed by rollback
- Fairness Under Deployment
  - Disparate impact and fairness monitoring across subgroups
  - Heterogeneous effects: balancing the fairness-robustness tradeoff
  - Planning ahead for effect variation across different groups
- Human Oversight and Governance
  - Escalation and override: human-in-the-loop review protocols
  - Trust calibration: knowing when to rely on versus override the system
  - Audit trails: documentation, versioning, and impact assessment
- Regulatory Compliance and Guardrails
  - GDPR, the EU AI Act, and other fairness standards
  - Documentation and audit preparation, with legal coordination as needed
  - Guardrails: safety constraints and graceful degradation under failure

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
