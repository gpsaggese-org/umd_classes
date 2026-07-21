# Summary

## Title
- From Data to Decisions: Building Decision Systems with Probabilistic Causal
  Reasoning

- Reasoning under Uncertainty: Causal Machine Learning for Decision Making

## Target Audience
- Senior ML engineers and data scientists with a statistics and probabilistic ML
  background who build production decision systems
- Working knowledge of causal basics (DAGs, SCMs, do-calculus) assumed

## Approach of the book
- Focus on:
  - The minimal mathematics to understand the problem and the solutions
  - Intuition
  - Toy examples
  - How to make the theory operational
    - Referring to packages in the Python ecosystem
  - Jupyter notebooks to back up the intuition with toy and more complex examples

- Provide resources to go one level deep
  - My classes
  - References to books and papers

## Short TOC
- The sequence of the parts in the books are:
  - Motivation
    - 01, Introduction
    - 02, Why Decisions, Not Predictions
    - 03, the Cost of Ignoring Causality, Uncertainty and Dynamics
  - Advanced Modeling Theory & Tools
    - 04, Knowledge Representation
    - 05, Probabilistic ML
    - 06, Causal ML
  - Data
    - 07, Building Causal Knowledge
    - 08, Causal data pipelines
  - Decision-Making Theory & Tools
    - 09, Decision Theory Foundations
    - 10, Taxonomy of Decision-Making Problems and Algorithms
    - 11, Simple Decisions
    - 12, Complex Decisions
    - 13, Agentic Causal Reasoning
  - Implementation, Deployment, & Governance
    - 14, Building Stakeholder Alignment
    - 15, Deployment, Monitoring, and Adaptation
    - 16, Trust, Explainability, Fairness, and Governance

## All Lesson Materials
// From ./generate_all_tocs.sh

- `data605/all_tocs.md`
- `data605/lectures_source/*.txt`

- `msml610/all_tocs.md`
- `msml610/lectures_source/*.txt`

- `book.Agentic_AI/all_tocs.md`
- `book.Agentic_AI/lectures_source/*.txt`

- `book_springer/all_tocs.md`
- `book_springer/lectures_source/*.txt`

## Chapter Templates and Invariants

### Goals
- 3 short bullet points of less of 100 characters each explaining what are the
  goals of the chapter

### Topics
- The `### Topics` section for each chapter should be in nested bullet points
  - Level 1 bullets: the title of the subchapter
  - Level 2 bullets: a short list of topics
- It should follow the template
  ```
  ### Topics
  - Topic 1
    - Subtopic 1.1
    - Subtopic 1.2
  - Topic 2
    ...
  ```
- The `### Topics` should be less than 20-25 lines and 175-200 words

### Slides
- This points to the slides in `book_springer/lectures_source` containing the
  book chapter
- Each slide deck should be about 30-35 slides

### Lesson Materials
- For each chapter
  - Read the table of content for the slides in `### Topics` and the content in
    `### Lesson Materials`
  - Update the `### Lesson Materials` to cover the `### Topics` using the
    materials listed above in `## All Lesson Materials`
  - Reference the actual lecture files to verify coverage percentages
  - The output must follow the template below
  ```
  ### Lesson Materials
  - `pointer to a lecture`
    - [<Amount of the lecture material covering this chapter>]: <topics>
  - `book_springer/lectures_source/Lesson01.02_Integrating_Causality_And_Probability_in_ML.txt`
    - [100%]: Integration of causality and uncertainty into ML systems, moving beyond correlation
  - Not covered
    - [<Amount of topics not covered by any lesson>]: <topics>
  ```

### Notes

# Roadmap

// https://docs.google.com/spreadsheets/d/1dU3crReWWLcSG8jI4jTvA4430-yMkqvdOEXEIbmktPQ/edit?gid=831837256#gid=831837256

| Chap                                                    | Slides                                                                     | TOC complete | Mat complete | Criticize | Slides finalized | Tutorial complete | Book complete |
| ------------------------------------------------------- | -------------------------------------------------------------------------- | ------------ | ------------ | --------- | ---------------- | ----------------- | ------------- |
|                                                         |                                                                            |              |              |           |                  |                   |               |
| Motivation                                              |                                                                            |              |              |           |                  |                   |               |
| 01. Why Decisions, Not Predictions                      | Lesson01.01_From_Data_Science_To_Decision_Science.txt                      | 50%          |              |           |                  |                   |               |
| 02. The Cost of Ignoring Causality                      | Lesson01.02_Integrating_Causality_And_Probability_in_ML.txt                |              |              |           |                  |                   |               |
| Advanced Modeling Theory & Tools                        |                                                                            |              |              |           |                  |                   |               |
| 04. Knowledge Representation                            | msml610/lectures_source/Lesson03.1-Knowledge_representation.txt            | 70%          | 80%          | 50%       |                  |                   |               |
|                                                         | msml610/lectures_source/Lesson03.2-Propositional_and_first_order_logic.txt | 80%          | 80%          | -         |                  |                   |               |
|                                                         | msml610/lectures_source/Lesson03.3-Non_classical_logics.txt                | 80%          | 80%          | -         |                  |                   |               |
| 05. Probalistic ML                                      |                                                                            |              |              |           |                  |                   |               |
|                                                         | msml610/lectures_source/Lesson06.1-Bayesian_Networks.txt                   |              |              |           |                  |                   |               |
|                                                         | msml610/lectures_source/Lesson06.2-Using_Bayesian_Networks.txt             |              |              |           |                  |                   |               |
| 06. Causal ML                                           |                                                                            |              |              |           |                  |                   |               |
| Data                                                    |                                                                            |              |              |           |                  |                   |               |
| 07. Building Causal Knowledge                           |                                                                            |              |              |           |                  |                   |               |
| 08. Causal data pipelines                               |                                                                            |              |              |           |                  |                   |               |
| Decision-Making Theory & Tools                          |                                                                            |              |              |           |                  |                   |               |
| 09. Decision Theory Foundations                         |                                                                            |              |              |           |                  |                   |               |
| 10. Taxonomy of Decision-Making Problems and Algorithms | Lesson10.01_Taxonomy_of_Decision_Problems.txt                              |              |              |           |                  |                   |               |
| 11. Simple Decisions                                    | Lesson11.01_Simple_Decisions.txt                                           |              |              |           |                  |                   |               |
| 12. Complex Decisions                                   | Lesson12.01_Complex_Decisions.txt                                          |              |              |           |                  |                   |               |
| 13. Agentic Causal Reasoning                            |                                                                            |              |              |           |                  |                   |               |
| Implementation, Deployment, & Governance                |                                                                            |              |              |           |                  |                   |               |
| 14. Building Stakeholder Alignment                      |                                                                            |              |              |           |                  |                   |               |
| 15. Deployment, Monitoring, and Adaptation              | Lesson15.01_Deployment_Monitoring_And_Adaptation.txt                       |              |              |           |                  |                   |               |
| 16. Trust, Explainability, Fairness, and Governance     |                                                                            |              |              |           |                  |                   |               |

# Detailed TOC

# Part I: Why Businesses Need Decisions, Not Predictions

## 01: Introduction

### Goals
- Frame the core premise: ML systems must optimize for decision value, not
  prediction accuracy
- Introduce the Decision Pipeline Framework (data → prediction → causal effect →
  policy)
- Explain why causal and probabilistic reasoning for business decision-making

### Topics
- The Philosophy and Motivation
  - Why prediction accuracy alone fails to drive business value
  - Decision-centric framing: from data science to decision science
  - Role of causal reasoning and probabilistic models in decision systems
- The Decision Pipeline Framework
  - From raw data to prediction to causal effect estimation to utility-maximizing
    policy
  - Feedback loops and learning from outcomes
  - Why each stage matters and what breaks when stages are skipped
- How This Book Is Organized
  - Five-part structure: motivation, theory, data, algorithms,
    deployment/governance
  - Intended audience and prerequisites
  - How chapters build on each other and fit into the decision pipeline

### Slides
- N/A

### Lesson Materials
- `msml610/lectures_source/Lesson00-Class.txt`
- `msml610/lectures_source/Lesson08.1-Causal_AI_intro.txt`
- `msml610/lectures_source/Lesson11.1-Decision_Making_with_Causal_Models.txt`

## 02: Why Decisions, Not Predictions

### Goals
- Show the gap: High prediction accuracy ≠ good business value (ROI)
- Distinguish prediction from decision
- Expose four critical failure modes: ignoring causality, uncertainty
  quantification, business objectives, and dynamics

### Topics
- Why Decisions, Not Predictions
- The Cost of Ignoring Causality
  - When Correlation Misleads
  - Structural Failure Modes
- The Cost of Ignoring Uncertainty
- The Cost of Ignoring the Business Objective
  - Proxies, Costs, and Trade-offs
  - From Scores to Actionable Decisions
- The Cost of Ignoring Dynamics and Feedback
  - A World That Reacts
  - Missing Exploration and Long Horizons
- Why This Matters
  - Roadmap

### Slides
- `book_springer/lectures_source/Lesson02.01_From_Data_Science_To_Decision_Science.txt`

### Lesson Materials
- `msml610/lectures_source/Lesson08.1-Causal_AI_intro.txt`
- `msml610/lectures_source/Lesson08.2-Causal_Networks.txt`
- `msml610/lectures_source/Lesson11.1-Decision_Making_with_Causal_Models.txt`

## 03: Handling Causality, Uncertainty, Business Objectives, and Dynamics

### Goals
- Combine causality and probability to find true effects
- Quantify uncertainty from evidence to decision bounds
- Encode business goals as utility-based decision functions

### Topics
- Causal Models and Effect Identification
  - Moving beyond correlation: confounding, mediators, and spurious paths in
    observational data
  - Structural causal models (SCMs) and DAGs: formalizing mechanisms
  - Identification criteria: back-door, front-door, do-calculus
- Probabilistic Uncertainty Quantification
  - Bayesian inference: priors, posteriors, posterior predictive distributions
  - Epistemic uncertainty over model; aleatoric irreducible noise
  - Decision-relevant bounds: confidence intervals, credible intervals,
    thresholds
- Business Objectives and Decision Rules
  - Utility functions: preferences, risk attitudes, multi-criteria trade-offs
  - Cost asymmetries: false-positive and false-negative costs
  - From predictions to actions: translating scores into decisions
- Dynamics, Feedback, and Performativity
  - Temporal causality: feedback loops linking past decisions to future causes
  - Performativity: how decisions change the systems they operate on
  - Sequential reasoning: multi-period consequences and adaptation
// TODO(ai_gp): Check this

### Slides 
- `book_springer/lectures_source/Lesson01.02_Integrating_Causality_And_Probability_in_ML.txt`
- `book_springer/lectures_source/Lesson01.03_Integrating_Business_Objective_And_Real_World_Dynamics.txt`

### Lesson Materials

# Part II: Advanced Modeling Theory & Tools

## 04: Knowledge Representation

### Goals
- Understand representation as a foundation for reasoning
- Master formal knowledge representation schemes
- Integrate symbolic and probabilistic reasoning

### Topics
- Representation as a Foundation for Decisions
  - Why representation choice shapes what questions a model can answer
  - Symbolic, sub-symbolic, procedural, declarative, and natural-language
    representations: trade-offs in expressiveness and tractability
- Formal Knowledge Representation
  - Propositional and first-order logic, entailment, and inference: symbolic
    reasoning foundations
  - Non-monotonic reasoning, default logic, and open- vs. closed-world
    assumptions
  - Rule-based and knowledge-based agents; grounding symbols in the world
  - Ontologies, description logics, RDF/SPARQL, semantic networks, and
    knowledge graphs: organizing domain knowledge into reusable structures
- Graphical Models for Uncertainty
  - Why logic fails under uncertainty
  - Bayesian networks: definition and structure
- Causal Graphical Models
  - Causal networks (causal DAGs) and the ladder of causation: association,
    intervention, and counterfactual
  - Structural causal models (SCMs): definition
- Integrating Logic and Causality
  - Markov logic networks: combining symbolic reasoning with probabilistic
    inference
  - From correlation to causal reasoning: what graphs add beyond raw data
  - Choosing a representation: when logic, probability, or causal graphs fit
    best

### Slides
- `book_springer/lectures_source/Lesson04.01_Knowledge_Representation.txt`

### Lesson Materials
- `msml610/lectures_source/Lesson03.1-Knowledge_representation.txt`
- `msml610/lectures_source/Lesson03.2-Propositional_and_first_order_logic.txt`
- `msml610/lectures_source/Lesson03.3-Non_classical_logics.txt`
- `msml610/lectures_source/Lesson06.1-Bayesian_Networks.txt`
- `msml610/lectures_source/Lesson08.2-Causal_Networks.txt`
- `msml610/lectures_source/Lesson09.2-Hidden_Markov_Models.txt`

## 05: Probabilistic ML

### Goals
- Master Bayesian updating: priors, posteriors, and approximate inference methods
- Build Bayesian generative models: networks, regression, and hierarchical models
- Turn posterior uncertainty into decisions, comparisons, and model choices

### Topics
- Bayesian Inference Foundations
  - Bayesian updating: turning priors into posteriors as evidence arrives,
    versus the frequentist view
  - Approximate inference: sampling, variational methods, and MCMC for
    posteriors with no closed form
- Bayesian Generative Models
  - Bayesian networks: structure, semantics, and exact vs. approximate
    inference
  - Regression and hierarchical models: posterior-based uncertainty over
    parameters, pooled across groups
- Uncertainty in Predictions
  - Posterior predictive distributions and checks: averaging over model
    uncertainty, validating fit
  - Epistemic vs. aleatoric uncertainty; robust inference and effect-size
    comparison across groups
- Bayesian Decision-Making
  - Expected utility and loss functions: turning posterior uncertainty into
    a decision
  - Savage-Dickey ratios, credible intervals, and prior choice for
    communicating results
- Model Comparison and Selection
  - Balancing fit and complexity: Occam's razor, overfitting, and the
    bias-variance trade-off
  - Information criteria, cross-validation, ensembles, and Bayes factors for
    choosing among models

### Slides
- `book_springer/lectures_source/Lesson05.01_Probabilistic_ML.txt`

### Lesson Materials
- `msml610/lectures_source/Lesson06.1-Bayesian_Networks.txt`
- `msml610/lectures_source/Lesson06.2-Using_Bayesian_Networks.txt`
- `msml610/lectures_source/Lesson07.1-Intro_to_Probabilistic_Programming.txt`
- `msml610/lectures_source/Lesson07.2-Posterior_Based_Decisions.txt`
- `msml610/lectures_source/Lesson07.3-Hierarchical_Models.txt`
- `msml610/lectures_source/Lesson07.4-Generalized_Linear_Models.txt`
- `msml610/lectures_source/Lesson07.5-Bayesian_Model_Comparison.txt`

## 06: Causal ML

### Goals
- Represent causal assumptions with DAGs and structural causal models
- Use do-calculus to identify interventional effects from observational data
- Apply back-door, front-door, and IV methods; know when identification fails

### Topics
- Causal Graphical Models
  - Structural causal models and DAGs: formal specification of generative
    mechanisms and causal order
  - Confounders, mediators, and colliders; the ladder of causation from
    association to counterfactuals
- Do-Calculus and Interventional Reasoning
  - The do-operator: distinguishing intervention from passive observation, and
    the three rules of do-calculus
  - From interventions to potential outcomes: individual, average, and
    conditional treatment effects
- Identification Criteria
  - Back-door and front-door criteria for identifying effects under
    confounding and mediation
  - D-separation and graph structure; confounding bias and propensity-score
    adjustment in practice
- Advanced Identification Methods
  - Instrumental variables and natural experiments for breaking confounding
    via exogenous variation
  - Sensitivity analysis for unmeasured confounding, and the limits of
    identifiability from observational data

### Slides
- `book_springer/lectures_source/Lesson06.01_Causal_ML.txt`

### Lesson Materials
- `msml610/lectures_source/Lesson08.2-Causal_Networks.txt`
- `msml610/lectures_source/Lesson08.3-Do_Calculus.txt`
- `msml610/lectures_source/Lesson08.4.txt`
- `msml610/lectures_source/Lesson10.2-Causal_Inference_for_Time_Series.txt`
- `msml610/lectures_source/Lesson12.2-Causal_Discovery.txt`

# Part III: Data

## 07: Building Probabilistic and Causal Knowledge

### Goals
- Elicit causal structure from experts and encode it as a validated DAG
- Distinguish confounders, mediators, moderators, and colliders in a graph
- Learn causal structure from data and reason about time-dependent causality

### Topics
- Eliciting Causal Knowledge from Experts
  - Structured, step-by-step elicitation of outcomes, interventions, and
    drivers from stakeholders
  - Handling disagreement in hybrid teams; eliciting and validating priors
- Building Causal DAGs
  - From a business question to a graph: choosing variables and encoding
    assumed mechanisms
  - Specifying edges and validating the resulting DAG against a worked example
- Variable Types and Relationships
  - Observed vs. unobserved and endogenous vs. exogenous variables
  - Confounders, moderators, colliders, and fork structures; how each role
    biases or clarifies effect estimation
- Causal Discovery from Data
  - Formal discovery problem; observational vs. interventional data
  - Constraint-based and score-based algorithm families
  - Combining automated discovery with domain knowledge, and validating the
    resulting DAG
- Temporal Structure in Causal Models
  - Why time series causality differs from the cross-sectional case
  - Feedback loops, simultaneity, and non-stationarity
  - When temporal structure helps identification, and when it misleads it

### Slides
- `book_springer/lectures_source/Lesson07.01_Building_Probabilistic_And_Causal_Knowledge.txt`

### Lesson Materials
- `msml610/lectures_source/Lesson08.1-Causal_AI_intro.txt`
- `msml610/lectures_source/Lesson08.2-Causal_Networks.txt`
- `msml610/lectures_source/Lesson08.4.txt`
- `msml610/lectures_source/Lesson10.2-Causal_Inference_for_Time_Series.txt`
- `msml610/lectures_source/Lesson12.2-Causal_Discovery.txt`
- `msml610/lectures_source/Lesson11.1-Decision_Making_with_Causal_Models.txt`

## 08: Causal Data Pipelines

### Goals
- Trace how data collection and selection choices bias causal estimates
- Detect distribution shift and proxy decay before they corrupt decisions
- Run pre-flight checks so causal assumptions hold before modeling begins

### Topics
- Data Collection and Its Biases
  - Collection design: how sampling and measurement choices shape the data
  - Selection mechanisms: who and what gets captured versus missed
  - Confounder introduction: biases built into the acquisition process itself
- Selection Bias and Incomplete Populations
  - Missing data mechanisms: MCAR, MAR, and MNAR patterns
  - Subgroup representation: historical data often misses critical populations
  - Impact on causal inference: incomplete data breaks identifiability
    assumptions
- Distribution Shift and Covariate Mismatch
  - Training vs. production: causal effects fail to hold in new environments
  - Concept drift: non-stationary relationships that change over time
  - Detecting shift: monitoring input distributions for meaningful changes
- Measurement Error and Proxy Validity
  - Proxy quality: does the proxy actually capture the true construct?
  - Attenuation: measurement error systematically weakens causal effect
    estimates
  - Correction methods: debiasing estimates under known measurement error
- Pre-Flight Data Quality Checks
  - Confounder balance: checking covariate distributions match assumptions
  - Missingness and outlier detection before modeling begins
  - Robust inference: methods that tolerate imperfect, noisy data

### Slides
- `book_springer/lectures_source/Lesson08.01_Causal_Data_Pipelines.txt`

### Lesson Materials
- `msml610/lectures_source/Lesson08.1-Causal_AI_intro.txt`
- `msml610/lectures_source/Lesson08.4.txt`
- `data605/lectures_source/Lesson02.3-Data_Pipelines.txt`
- `data605/lectures_source/Lesson07.2-Data_Wrangling.txt`
- `msml610/lectures_source/Lesson10.2-Causal_Inference_for_Time_Series.txt`
- `msml610/lectures_source/Lesson08.3-Do_Calculus.txt`
- `msml610/lectures_source/Lesson02.3-ML_Techniques_Input_Processing.txt`
- `msml610/lectures_source/Lesson02.6-ML_Techniques_How_To_Do_Research.txt`
- `book_springer/lectures_source/Lesson15.01_Deployment_Monitoring_And_Adaptation.txt`

# Part IV: Decision-Making Theory & Tools

## 09: Decision Theory Foundations

### Topics
- Von Neumann-Morgenstern Axioms
  - Rational choice axioms: completeness, transitivity, continuity, and
    independence
  - Utility existence theorem: rational preferences representable as a utility
    function
  - Why expected utility is the mathematically correct decision framework
- Utility Functions in Practice
  - Eliciting preferences: methods for extracting stakeholder objectives
  - Multi-criteria trade-offs: combining value functions toward Pareto
    optimality
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
  - [95%]: Utility functions, expected utility principle, risk preferences and
    visualizing risk aversion, multi-criteria trade-offs, decision networks,
    Bayesian decision rules, prior elicitation
- `msml610/lectures_source/Lesson12.1-Reinforcement_learning.txt`
  - [75%]: Maximum Expected Utility principle, utility of states/policies,
    Bellman equation: expected-utility framework applied to sequential
    decisions
- `msml610/lectures_source/Lesson07.1-Intro_to_Probabilistic_Programming.txt`
  - [65%]: Bayes' theorem, priors, Bayesian vs. frequentist updating —
    foundation for subjective expected utility
- `msml610/lectures_source/Lesson07.2-Posterior_Based_Decisions.txt`
  - [55%]: Posterior-based decision rules via loss functions, ROPE,
    Savage-Dickey ratio: decision rules under posterior uncertainty; not
    risk/utility content
- `msml610/lectures_source/Lesson09.3-Multi_Armed_Bandits.txt`
  - [50%]: Sequential decision-making, Bayesian bandits, value-of-information
    framing: peripheral to axiomatic utility core
- Not covered
  - [55%]: Formal VNM axioms (completeness, transitivity, continuity,
    independence) and the utility-existence theorem, stakeholder
    preference-elicitation methodology beyond priors

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
  - [95%]: Causal effects to expected value, EVPI/EVSI, Bayesian optimization,
    causal multi-armed bandits, exploration vs. exploitation
- `msml610/lectures_source/Lesson09.3-Multi_Armed_Bandits.txt`
  - [90%]: Thompson sampling, UCB, epsilon-greedy, contextual bandits, regret
    bounds
- `msml610/lectures_source/Lesson12.1-Reinforcement_learning.txt`
  - [80%]: MDPs, value/policy iteration, off-line vs. on-line MDP solving
- `msml610/lectures_source/Lesson08.5-Experimentation.txt`
  - [75%]: A/B testing design, decision framework for experiment vs. observe,
    hybrid experimental-causal approaches
- `msml610/lectures_source/Lesson07.2-Posterior_Based_Decisions.txt`
  - [65%]: Posterior-based decision rules via loss functions and ROPE: using
    full posterior distribution, not point estimates
- `msml610/lectures_source/Lesson07.1-Intro_to_Probabilistic_Programming.txt`
  - [45%]: Bayesian updating fundamentals, priors: foundational only
- Not covered
  - [50%]: Minimax/distributional robustness against model misspecification,
    formal sensitivity analysis, advanced acquisition-function design

## 11: Simple Decisions

### Topics
- Bayesian Inference for Decisions
  - Reasoning over model uncertainty: Bayesian networks, variational inference,
    MCMC
  - Encoding prior knowledge: updating beliefs as evidence arrives
  - Deciding under partial information: posterior uncertainty plus decision
    rules
- Sequential Inference with Hidden State
  - Tracking unobserved state: HMMs, Kalman filters, particle filters
  - Partially observable decision problems (POMDPs): acting without full
    observability
  - Belief states: a sufficient statistic for decisions over hidden state
- Bandit Algorithms
  - Exploration-exploitation tradeoff: learning about actions vs. exploiting
    known-good ones
  - Algorithm family: epsilon-greedy, UCB, Thompson sampling, contextual bandits
  - Regret: minimizing cumulative loss while learning
- Planning and Search
  - Deterministic planning: A\* search and model predictive control (MPC)
  - Stochastic and adversarial planning: Monte Carlo tree search (MCTS), minimax
  - Finite-horizon assumption: near-optimal sequences under known, bounded
    dynamics
- Value-Based Reinforcement Learning
  - Value functions: Q-learning, SARSA, value and policy iteration
  - Deep value-based methods: DQN and function approximation for large states
  - Delayed rewards: learning environment structure from sparse feedback

### Lesson Materials
- `msml610/lectures_source/Lesson12.1-Reinforcement_learning.txt`
  - [95%]: MDPs, POMDPs, belief-state transitions, value/Q-learning,
    temporal-difference learning, policy search
- `msml610/lectures_source/Lesson09.3-Multi_Armed_Bandits.txt`
  - [95%]: Epsilon-greedy, UCB, Thompson sampling, contextual bandits, regret
    analysis
- `msml610/lectures_source/Lesson09.1-Reasoning_over_time.txt`
  - [85%]: Sequential inference over hidden state: filtering, prediction,
    smoothing, Viterbi/most-likely-explanation
- `msml610/lectures_source/Lesson07.1-Intro_to_Probabilistic_Programming.txt`
  - [70%]: Bayesian inference, belief updating, posterior-based reasoning
- `msml610/lectures_source/Lesson07.2-Posterior_Based_Decisions.txt`
  - [55%]: Loss-function-based decision rules under posterior uncertainty
- Not covered
  - [35%]: Deterministic/stochastic/adversarial planning and search (A\*, MPC,
    MCTS, minimax): no lecture in any of the four courses covers classical
    search/planning; deep Q-network specifics

## 12: Complex Decisions

### Topics
- Policy-Based and Actor-Critic Methods
  - Direct policy parameterization via gradient ascent: REINFORCE, PPO, TRPO
  - Actor-critic stability: combining value and policy in A2C, A3C, DDPG, TD3,
    SAC
  - High-dimensional and continuous action spaces where value-based methods
    struggle
- Planning with Learned Models and Deep Search
  - Model-based planning: Dyna-Q style imagined rollouts accelerate learning
  - Neural networks combined with tree search: AlphaGo, AlphaZero, MuZero
  - World models: learned dynamics enabling long-horizon reasoning
- Hierarchical and Modular Decision-Making
  - Decomposing complex decisions into subtasks, options, and temporal
    abstraction
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
  - [95%]: Model-based vs. model-free RL, policy search, causal RL, structural
    causal models for MDPs, counterfactual credit assignment, deconfounding
    offline/off-policy data
- `class_cs_refreshers/lectures_source/Lesson95.Refresher_game_theory.txt`
  - [50%]: Nash equilibrium, zero-sum games and the minimax theorem, cooperative
    game theory, mechanism design, multi-agent RL (conceptual foundations, not
    QMIX/MAPPO/CFR specifics)
- `msml610/lectures_source/Lesson11.1-Decision_Making_with_Causal_Models.txt`
  - [55%]: Robustness under misspecification (aleatoric/epistemic uncertainty),
    exploration vs. exploitation in a causal-decision frame
- `msml610/lectures_source/Lesson08.5-Experimentation.txt`
  - [55%]: Policy evaluation and off-policy learning: logged-data learning
    without live interaction
- `msml610/lectures_source/Lesson10.2-Causal_Inference_for_Time_Series.txt`
  - [35%]: Temporal causal structure, feedback loops/simultaneity, VARs —
    causal-inference methodology, not policy-learning algorithms
- `msml610/lectures_source/Lesson09.1-Reasoning_over_time.txt`
  - [35%]: Markov process/state-transition fundamentals: loosely supports
    temporal abstraction, no hierarchical-RL content
- Not covered
  - [50%]: Policy-gradient/actor-critic algorithm details (REINFORCE, PPO, TRPO,
    A2C/A3C, DDPG/TD3/SAC), AlphaGo/AlphaZero/MuZero-style neural+tree search,
    hierarchical RL/options, offline RL algorithm specifics (CQL), deep MARL
    algorithms (QMIX, MAPPO, MADDPG, CFR)

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
  - Hybrid reasoning: combining symbolic causal models with learned
    probabilities
  - Uncertainty quantification maintained over causal structure itself
  - Online discovery: learning causal DAGs from live deployment data

### Lesson Materials
- `msml610/lectures_source/Lesson15.1-Causal_Reasoning_Agents.txt`
  - [98%]: LLM causal-reasoning strengths/limits, chain-of-thought
    causal-prompting frameworks, integrating causal DAGs with LLM workflows,
    causal agent architectures, causal MDPs and planning under causal
    uncertainty, transparency/fairness/robustness/safety through causal
    constraints
- `book.Agentic_AI/lectures_source/Lesson01.05-Reasoning_Memory_and_Planning.txt`
  - [60%]: World models for planning: LLM-as-world-model, WebDreamer "simulate
    before you act" (forward-model causal simulation)
- `book.Agentic_AI/lectures_source/Lesson01.04-LLM_Reasoning.txt`
  - [55%]: Chain-of-thought/tree-of-thought variants, self-consistency: general
    reasoning scaffolding, not causal-specific decomposition
- `book.Agentic_AI/lectures_source/Lesson01.07-Tool_use_and_retrieval.txt`
  - [45%]: Tool-use/retrieval architecture, grounding on enterprise knowledge —
    the tool-use half of the topic, no causal-simulation content
- `book.Agentic_AI/lectures_source/Lesson01.01-What_Is_An_Agentic_AI.txt`
  - [30%]: Generic perceive-plan-act agent architecture and tool/environment
    taxonomy: background context only
- `book.Agentic_AI/lectures_source/Lesson01.09_Post_training_and_verifiable_agents.txt`
  - [25%]: Verification, reward hacking: tangential to trustworthy-agent topic,
    not causal/fairness/performativity specific
- `book.Agentic_AI/lectures_source/Lesson01.03-History_of_LLM_Agents.txt`
  - [20%]: ReAct and agent history: background context
- Not covered
  - [30%]: Online causal-discovery algorithms learning DAGs from live deployment
    data, formal performativity mathematics, hybrid symbolic-probabilistic
    uncertainty quantified over causal structure itself

# Part V: Implementation, Deployment, Governance

## 14: Building Stakeholder Alignment

### Topics
- Eliciting and Refining Causal Knowledge
  - Structured methods: interviews, surveys, and consensus-building workshops
  - Handling disagreement: reconciling conflicting views among domain experts
  - Iterative refinement: cycling between expert input and data validation
- Communicating Causal Assumptions
  - Audience targeting: tailoring the message for experts, operations,
    leadership
  - Precision without jargon: explaining technical concepts accessibly
  - DAG visualization: making causal structures visible and open to debate
- Sensitivity Analysis as Communication Tool
  - Robustness demonstration: showing decisions hold across plausible
    assumptions
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
  - [90%]: Causal AI workflow with hybrid teams, "Roles in Hybrid Teams," Step 4
    (Build Causal DAG), stakeholder alignment in business deployment
- `msml610/lectures_source/Lesson12.2-Causal_Discovery.txt`
  - [85%]: Using domain knowledge as constraints, combining discovery with
    expert judgment, validating a discovered DAG
- `msml610/lectures_source/Lesson11.1-Decision_Making_with_Causal_Models.txt`
  - [88%]: Communicating uncertainty to stakeholders; prior elicitation methods
    and pitfalls (structured elicitation of causal/prior knowledge)
- `msml610/lectures_source/Lesson08.2-Causal_Networks.txt`
  - [75%]: Building a causal DAG, mediator/moderator/confounder types,
    documenting causal assumptions for review
- `msml610/lectures_source/Lesson07.2-Posterior_Based_Decisions.txt`
  - [60%]: Loss-function elicitation, Region of Practical Equivalence: framing
    acceptable error/cost trade-offs for stakeholder sign-off
- `msml610/lectures_source/Lesson08.4.txt`
  - [45%]: Causal DAG structures (chains, forks, colliders, d-separation),
    confounding bias, backdoor adjustment: supports DAG
    visualization/communication only
- Not covered
  - [45%]: Formal structured elicitation methods (interviews, surveys, consensus
    workshops), disagreement-resolution protocols among experts, formal go/no-go
    sign-off procedures

## 15: Deployment, Monitoring, and Adaptation

### Topics
- From Notebook to Production
  - Infrastructure: moving models from experimentation to operational systems
  - Data pipelines: integrating real-time data streams into serving
  - Latency and throughput requirements for production performance
- Cost-Aware Rollout and Experimentation
  - Phased rollout, shadow mode, and canary analysis to manage risk
  - A/B testing vs. observational methods, combined in hybrid approaches
  - Continuous experimentation: sequential testing and incremental policy
    improvement
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
- `book_springer/lectures_source/Lesson15.01_Deployment_Monitoring_And_Adaptation.txt`
  - [98%]: Notebook-to-production gap, serving patterns, phased rollout
    (shadow/canary/ramp), guardrail metrics, assumption-monitoring taxonomy
    (directly/indirectly testable/domain-assessed), sensitivity analysis and
    E-values, negative controls, versioning, error budgets, rollback, feedback
    loops, performativity, technical debt
- `msml610/lectures_source/Lesson08.5-Experimentation.txt`
  - [85%]: A/B test design, power analysis, SRM, novelty/primacy effects,
    multi-armed bandits, experiment-vs-observe decision framework, off-policy
    evaluation
- `msml610/lectures_source/Lesson12.1-Reinforcement_learning.txt`
  - [75%]: Policy iteration, model-based/model-free RL, active/passive RL,
    off-policy deconfounding, causal generalization across environments
- `msml610/lectures_source/Lesson10.2-Causal_Inference_for_Time_Series.txt`
  - [65%]: Non-stationarity/trend detection, feedback loops and simultaneity,
    time-varying unobserved confounders
- `msml610/lectures_source/Lesson08.4.txt`
  - [65%]: CATE, effect heterogeneity, cumulative-gain curves: basis for
    heterogeneous deployment and stratified rollout targeting
- `data605/lectures_source/Lesson02.3-Data_Pipelines.txt`
  - [55%]: ETL/ELT paradigms, workflow orchestration, data ingestion —
    production pipeline infrastructure
- Not covered
  - [20%]: Vendor-specific monitoring/dashboard tooling, organization-specific
    runbook templates

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
  - [95%]: Causal vs statistical explainability, SHAP, LIME, counterfactual
    explanations, faithfulness/stability of explanations
- `msml610/lectures_source/Lesson15.1-Causal_Reasoning_Agents.txt`
  - [90%]: Counterfactual fairness, path-specific effects, causal definitions of
    fairness/discrimination, causal constraints for fair models,
    safety-through-causal-constraints (guardrails, harmful-outcome prevention),
    transparency for trustworthy autonomy, human-in-the-loop override, causal
    monitoring/adaptation
- `msml610/lectures_source/Lesson08.2-Causal_Networks.txt`
  - [85%]: Causal mechanisms, mediation analysis, direct vs indirect effects —
    foundation for path-specific fairness reasoning
- `msml610/lectures_source/Lesson08.1-Causal_AI_intro.txt`
  - [70%]: Interpretability/explainability techniques, causal AI for trustworthy
    and transparent systems
- `book.Agentic_AI/lectures_source/Lesson01.01-What_Is_An_Agentic_AI.txt`
  - [55%]: Human-in-the-loop vs full autonomy trade-offs, audit and
    accountability, error-catching before real-world consequences
- `msml610/lectures_source/Lesson08.4.txt`
  - [35%]: Effect heterogeneity (CATE) across subgroups: relevant to detecting
    disparate treatment effects, though it defines no fairness metrics
- Not covered
  - [55%]: Regulatory compliance specifics (GDPR, EU AI Act provisions), formal
    audit-trail/documentation standards, legal coordination processes

# Appendix
