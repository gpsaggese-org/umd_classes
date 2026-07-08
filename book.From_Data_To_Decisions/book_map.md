**Title**:
- From Data to Decisions: Building Decision Systems with Probabilistic Causal
  Reasoning

**Target audience:**
- Senior ML engineers and data scientists with a statistics and probabilistic ML
  background who build production decision systems
- Working knowledge of causal basics (DAGs, SCMs, do-calculus) assumed

**Decision Pipeline**

# Part I: Why Businesses Need Decisions, not Predictions (Motivation)

## 1: From Prediction Pipelines to Decision Pipelines

### Topics
- Why organizations fail with good data
- Prediction vs. decision: Simpson's paradox and policy reversals
- The decision pipeline
  - Data → Probabilistic Causal Model → Effect Estimation → Policy → Action → Feedback → Learning Loop
- Ladder of causation as decision tool
- Causal maturity model: from descriptive to autonomous decisions

### Lessons
- `msml610/lectures_source/Lesson08.1-Causal_AI_intro.txt`
  - [FULL] — Ladder of Causation; Data Science → Decision Science; Causal vs Predictive Questions; Roadmap Prediction→Decision; Data Analytics Sophistication (maturity model); Why AI Projects Fail
- `msml610/lectures_source/Lesson11.1-Decision_Making_with_Causal_Models.txt`
  - [PART] — From Predictions to Decisions; Prediction vs Decision Side-by-Side; Simpson's Paradox (+Causal Resolution); Policy Reversal
- `msml610/lectures_source/Lesson08.2-Causal_Networks.txt`
  - [PART] — Example of ladder of causation (Tornado Warning)

### Tutorials

### Related packages
- DoWhy (6,600): Causal inference using graphical models
- PyWhy (2,400): Python ecosystem for causal inference
- Azua (1,400): Causal decision-making framework

### Related books
- [B001] Agrawal et al., "Prediction Machines", 2018
- [B002] Pearl et al., "The Book of Why", 2018
- [B003] Huyen, "Designing Machine Learning Systems", 2022
- [B039] Hurwitz & Thompson, "Causal Artificial Intelligence", 2024
- [B040] Brynjolfsson & McAfee, "Machine, Platform, Crowd", 2021
- [B041] Angrist & Pischke, "Probability, Statistics, and Causal Inference", 2020

### Related Papers
- [P001] Ribeiro et al., "Why Should I Trust You? Explaining the Predictions of
  Any Classifier", 2016 https://arxiv.org/pdf/1602.04938.pdf
- [P002] Lundberg & Lee, "A Unified Approach to Interpreting Model Predictions",
  2017 https://arxiv.org/pdf/1705.07874.pdf
- [P003] Taori et al., "Data Feedback Loops: Model-driven Amplification of
  Dataset Biases", 2020 https://proceedings.mlr.press/v202/taori23a/taori23a.pdf
- [P004] Imbens & Wooldridge, "Recent Developments in the Econometrics of Program
  Evaluation", 2018 https://www.nber.org/papers/w24318
- [P005] Pearl, "Simpson's Paradox, Confounding, and Collapsibility", 1999
  https://bayes.cs.ucla.edu/BOOK-2K
- [P006] Kaddour et al., "Challenges and Opportunities with Causal Discovery
  Algorithms", 2023 https://www.nature.com/articles/s41598-020-59669-x
- [P007] Zhang et al., "A Survey on Causal Inference", 2020
  https://arxiv.org/pdf/2002.05209.pdf
- [P008] Peters et al., "Causality: Models, Learning, and Inference", 2023
  https://arxiv.org/pdf/2012.13993.pdf
- [P009] Pearl, "The Seven Pillars of Causal Reasoning with Reflections on
  Machine Learning", 2021
  https://cacm.acm.org/research/seven-pillars-of-causal-reasoning-with-reflections-on-machine-learning/
- [P010] Joshi et al., "Towards Realistic Counterfactual Explanations with
  Contrastive Pertinent Features", 2019 https://arxiv.org/pdf/1906.04957.pdf
- [P011] Peters et al., "Elements of Causal Inference: Foundations and Learning
  Algorithms", 2020
  https://mitpress.mit.edu/9780262037310/elements-of-causal-inference/

## 2: Why Good Data Leads to Bad Decisions

### Topics
- Statistical significance trap in business
- A/B tests and heterogeneous treatment effects
- Causal ML failure modes in production
- When correct estimates lead to bad policies
- Decision Readiness Scorecard

### Lessons
- `msml610/lectures_source/Lesson08.4.txt`
  - [PART] — Effect heterogeneity; CATE; Why Prediction Is Not the Answer
- `msml610/lectures_source/Lesson08.1-Causal_AI_intro.txt`
  - [PART] — Problem 2 Decision Making; Problem 5 Feedback Loops; Problem 6 Distribution Shift; Cost of Ignoring Causality
- `msml610/lectures_source/Lesson08.5-Experimentation.txt`
  - [PART] — Peeking/Multiple Comparisons; SRM; Novelty/Primacy (significance traps)
- `msml610/lectures_source/Lesson91.Refresher_probability.txt`
  - [WEAK] — p-hacking; multiple hypothesis testing; FDR
- No slide for "Decision Readiness Scorecard"

### Tutorials

### Related packages

### Related books

## 3: Problem Framing and Intervention Design

### Topics
- From KPI selection to decision objectives
- Intervention design: lever, target, timing
- Data collection strategy for identifiability
- Decision artifacts and templates
- Causal Project Checklist

### Lessons
- `msml610/lectures_source/Lesson08.1-Causal_AI_intro.txt`
  - [PART] — Causal AI Workflow Steps 1–7 (Intended Outcomes → Interventions → Factors → Build DAG → Data Acquisition → Model Modification → Deployment); Marketing Example: Price Intervention
- `msml610/lectures_source/Lesson08.5-Experimentation.txt`
  - [PART] — Decision Framework: Experiment or Observe?; Feasibility Constraints
- No slide for "Causal Project Checklist"

### Tutorials

### Related packages

### Related books

# Part II: Advanced Tools & Theory (Foundations)

## 4: Knowledge Representation

### Topics
- Problem scope and system boundaries
- Domain knowledge and constraints
- Data availability and measurement
- Variables, relationships, and temporal structure
- Stakeholders and decision levers

### Lessons
- `msml610/lectures_source/Lesson08.2-Causal_Networks.txt`
  - [PART] — Building a Causal DAG; variable types (mediator/moderator/confounder/collider); temporal structure
- `msml610/lectures_source/Lesson12.2-Causal_Discovery.txt`
  - [PART] — Using Domain Knowledge as Constraints; Combining Discovery with Expert Judgment
- `msml610/lectures_source/Lesson03-Knowledge_representation.txt`
  - [WEAK] — symbolic KR (ontologies, FOL, knowledge graphs); thin overlap — book Ch4 = decision scoping, not symbolic logic

### Tutorials

### Related packages

### Related books

## 5: Advanced Probabilistic ML

### Topics
- Gaussian processes: kernels, inference, and uncertainty
- Variational inference and amortized VI in deep models
- Normalizing flows and expressive density estimation
- Probabilistic programs: Pyro, NumPyro, Stan
- Neural posterior estimation and simulation-based inference
- Calibration and conformal prediction at scale

### Lessons
- `msml610/lectures_source/Lesson11.2-Probabilistic_deep_learning.txt`
  - [FULL] — VAEs; Normalizing Flows; Bayesian NNs; VI/SVI; MCMC; Calibration; Conformal Prediction; Neural Processes; Deep Latent Variable Models
- `msml610/lectures_source/Lesson07.1-Intro_to_Probabilistic_Programming.txt`
  - [PART] — PPLs, Bayesian models (Pyro/PyMC/Stan)
- `msml610/lectures_source/Lesson96.Refresher_stochastic_processes.txt`
  - [WEAK] — Gaussian Processes (one slide)
- Gap: amortized VI; neural posterior estimation / simulation-based inference

### Tutorials

### Related packages

### Related books

## 6: Advanced Causal Modeling

### Topics
- Causal basics assumed (DAGs, SCMs, do-calculus — see Durai 2025)
- Latent confounders: proxy variables and negative controls
- Causal representation learning and disentanglement
- Causal discovery: constraint-based (PC/FCI), score-based (GES), FCMs (LiNGAM, ANM)
- Nonparametric identification and generalized do-calculus
- Sensitivity analysis: E-values, amplification, sharp bounds

### Lessons
- `msml610/lectures_source/Lesson12.2-Causal_Discovery.txt`
  - [FULL] — algorithm families (constraint/PC-FCI, score/GES, functional/LiNGAM-ANM); Markov equivalence; identifiability; faithfulness; refutation
- `msml610/lectures_source/Lesson08.3-Do_Calculus.txt`
  - [PART] — do-calculus rules; back/front-door adjustment
- `msml610/lectures_source/Lesson08.2-Causal_Networks.txt`
  - [PART] — SCM; causal DAGs (basics)
- `msml610/lectures_source/Lesson11.2-Probabilistic_deep_learning.txt`
  - [PART] — Causal Deep Learning (representation learning)
- Gap: latent confounders/proxy/negative controls; E-values/sharp-bounds sensitivity

### Tutorials

### Related packages

### Related books

# Part III: Single-Step Decisions

## 7: Decision Theory Foundations

### Topics
- Expected utility maximization
- Utility functions in business
- From treatment effects to expected value
- Influence diagrams and policy solving
- Risk and uncertainty quantification

### Lessons
- `msml610/lectures_source/Lesson11.1-Decision_Making_with_Causal_Models.txt`
  - [FULL] — Utility Functions; Expected Utility Principle (+insurance/two-treatment examples); Decision Networks (=influence diagrams); Solving a Decision Network; Risk Preferences; Aleatoric vs Epistemic Uncertainty
- `msml610/lectures_source/Lesson12.1-Reinforcement_learning.txt`
  - [PART] — MEU; Dynamic Decision Networks

### Tutorials

### Related packages

### Related books

## 8: Decision-Making with Causal Models

### Topics
- Translating causal effects into decisions
- Bayesian decision-making and belief updating
- Value of information and experimental design
- Bayesian optimization for experimentation
- Exploration vs. exploitation trade-offs
- Decision robustness under model misspecification
- Counterfactual decision analysis

### Lessons
- `msml610/lectures_source/Lesson11.1-Decision_Making_with_Causal_Models.txt`
  - [FULL] — Bayesian Decision-Making; Value of Information (EVPI/EVSI); Bayesian Optimization for Experimentation; Acquisition Functions; Causal Bayesian Optimization; Exploration vs Exploitation; Causal Multi-Armed Bandits; Counterfactual decisions
- `msml610/lectures_source/Lesson09.3-Multi_Armed_Bandits.txt`
  - [PART] — Thompson Sampling; Bayesian Bandits; UCB
- `msml610/lectures_source/Lesson07.2-Posterior_Based_Decisions.txt`
  - [PART] — posterior-based decisions; loss functions

### Tutorials

### Related packages
- DoWhy (6,600): Causal inference using graphical models
- EconML (4,600): ML-based causal effect estimation
- BoTorch (3,300): Bayesian optimization in PyTorch
- Azua (1,400): Causal decision-making framework

### Related books
- [B028] Kochenderfer, "Decision Making Under Uncertainty", 2015
- [B029] Russell et al., "Artificial Intelligence: A Modern Approach", 2020
- [B002] Pearl et al., "The Book of Why", 2018

## 9: Policy Learning & Distributional Causal Effects

### Topics
- Beyond ATE: quantile and distributional treatment effects
- Doubly robust and debiased/double-ML estimation
- Meta-learners: T-, S-, X-, R-learner comparison
- Off-policy optimization and safe policy improvement
- Multi-task and transfer learning for policy adaptation

### Lessons
- `msml610/lectures_source/Lesson08.4.txt`
  - [FULL] — Metalearners T/S/X/R-Learner; R-learner (Double/Debiased ML); Double-ML for CATE; Effect heterogeneity; CATE evaluation; Cumulative Gain/AUC
- `msml610/lectures_source/Lesson08.5-Experimentation.txt`
  - [PART] — Policy Evaluation and Off-Policy Learning
- `msml610/lectures_source/Lesson12.1-Reinforcement_learning.txt`
  - [WEAK] — off-policy / deconfounding
- Gap: quantile/distributional treatment effects; safe policy improvement

### Tutorials

### Related packages

### Related books

## 10: Partial Identification & Robust Inference

### Topics
- Partial identification: Manski bounds, IV bounds, sharp bounds
- Sensitivity analysis: Rosenbaum bounds, E-values, amplification factors
- Relaxing positivity: trimming, extrapolation, and weighting
- Distributional robustness and minimax causal inference
- Domain adaptation under covariate and concept shift

### Lessons
- `msml610/lectures_source/Lesson08.4.txt`
  - [PART] — Positivity; IPW Sensitivity; Positivity-Bias Trade-Off; Non-compliance and instruments
- `msml610/lectures_source/Lesson10.2-Causal_Inference_for_Time_Series.txt`
  - [PART] — Instrumental Variables (IV)
- `msml610/lectures_source/Lesson12.1-Reinforcement_learning.txt`
  - [WEAK] — Causal Generalization Across Environments
- Gap: Manski/Rosenbaum bounds; E-values; minimax/distributional robustness

### Tutorials

### Related packages

### Related books

## 11: Agentic Causal Reasoning

### Topics
- Causal reasoning limits in LLMs and foundation models
- Pattern-based reasoning vs. causal reasoning
- Chain-of-thought prompting for causal reasoning
- Integrating causal and probabilistic frameworks
- SCM-augmented agents: structured causal knowledge in the loop
- Tool-use and causal simulation for multi-step planning
- Multi-agent interference: spillover, coordination, and equilibrium
- Trustworthy AI through causality:
  - Transparency and interpretability
  - Robustness through causal constraints
  - Fairness through causal reasoning
  - Safety through causal reasoning
- Causal guardrails and safety constraints for autonomous agents

### Lessons
- `msml610/lectures_source/Lesson15.1-Causal_Reasoning_Agents.txt`
  - [FULL] — LLM causal limits; pattern vs causal reasoning; CoT causal prompting; integrating causal+probabilistic; causal agent architectures; causal MDPs; Trustworthy AI (transparency/robustness/fairness/safety); guardrails
- `msml610/lectures_source/Lesson16.4-LLM_Reasoning.txt`
  - [PART] — Chain-of-Thought and variants
- `msml610/lectures_source/Lesson16.1-What_Is_An_Agentic_AI.txt`
  - [PART] — agents, tools, perceive-plan-act loop
- `msml610/lectures_source/Lesson16.5-Reasoning_Memory_and_Planning.txt`
  - [PART] — world models for planning
- `msml610/lectures_source/Lesson16.7-Tool_use_and_retrieval.txt`
  - [PART] — tool use, retrieval/grounding

### Tutorials

### Related packages
- DoWhy (6,600): Causal inference using graphical models
- PyWhy (2,400): Python ecosystem for causal inference
- Causica (2,000): Microsoft tool combining causal discovery and inference with
  deep learning
- ALICE (1,000): ML and econometrics integration

### Related books
- [B002] Pearl et al., "The Book of Why", 2018
- [B004] Koller et al., "Probabilistic Graphical Models", 2009
- [B007] Pearl, "Causality", 2009
- [B008] Peters et al., "Elements of Causal Inference", 2017
- [B014] Angrist et al., "Mostly Harmless Econometrics", 2008
- [B019] Molnar, "Interpretable Machine Learning", 2022
- [B027] Spirtes et al., "Causation, Prediction, and Search", 2000
- [B036] Christian, "The Alignment Problem", 2020
- [B037] Russell, "Human Compatible", 2019
- [B038] Schölkopf et al., "Causal Artificial Intelligence", 2021
- [B042] Pearl et al., "Causal Inference in Statistics: A Primer", 2016
  https://ftp.cs.ucla.edu/pub/stat_ser/r481.pdf
- [B043] Pearl, "Probabilistic Reasoning in Intelligent Systems: Networks of
  Plausible Inference", 1988
- [B044] Puterman, "Markov Decision Processes: Discrete Stochastic Dynamic
  Programming", 1994
- [B045] Barocas et al., "Fairness and Machine Learning", 2019
  https://fairmlbook.org

### Related Papers
- [P029] Brown et al., "Language Models are Few-Shot Learners", 2020
  https://arxiv.org/abs/2005.14165
- [P030] Kaplan et al., "Scaling Laws for Neural Language Models", 2020
  https://arxiv.org/abs/2001.08361
- [P031] Hoffmann et al., "Training Compute-Optimal Large Language Models", 2022
  https://arxiv.org/abs/2203.15556
- [P032] Kojima et al., "Large Language Models are Zero-Shot Reasoners", 2022
  https://arxiv.org/abs/2205.11916
- [P033] Wei et al., "Chain-of-Thought Prompting Elicits Reasoning in Large
  Language Models", 2022 https://arxiv.org/abs/2201.11903
- [P034] Yao et al., "Tree of Thoughts: Deliberate Problem Solving with Large
  Language Models", 2023 https://arxiv.org/abs/2305.10601
- [P035] Wei et al., "Emergent Abilities of Large Language Models", 2022
  https://arxiv.org/abs/2206.07682
- [P036] Bottou et al., "Counterfactual reasoning and learning systems: The
  example of computational advertising", 2013 https://arxiv.org/abs/1209.0467
- [P037] Rotnitzky et al., "Semiparametric regression adjustment to estimate
  policy effects", 2005 https://doi.org/10.1198/016214504000001646
- [P038] Richards et al., "A deep learning framework for neuroscience", 2019
  https://doi.org/10.1038/s41593-019-0520-2
- [P039] Peters et al., "Causal inference using invariant prediction:
  identification and outlook", 2015 https://arxiv.org/abs/1501.01332
- [P040] Precup et al., "Reinforcement learning with unsupervised auxiliary
  tasks", 2017 https://arxiv.org/abs/1611.05397
- [P041] Schaal et al., "Computational approaches to motor learning by
  imitation", 2003 https://doi.org/10.1098/rstb.2003.1257
- [P042] Hafner et al., "Mastering Atari, Go, Chess and Shogi by Planning with a
  Learned World Model", 2023 https://arxiv.org/abs/2104.06294
- [P043] Dasgupta et al., "Causal reasoning from meta-reinforcement learning",
  2019 https://arxiv.org/abs/1901.08162
- [P044] Ivgi et al., "Causal Effect Inference with Deep Latent-Variable Models",
  2022
- [P045] Buesing et al., "Learning and Policy Search in Stochastic Dynamical
  Systems with Bayesian Neural Networks", 2018 https://arxiv.org/abs/1805.12114
- [P046] Bareinboim et al., "Causal inference and the data-fusion problem", 2016
  https://arxiv.org/abs/1412.3608
- [P047] Lipton, "The Mythos of Model Interpretability", 2018
  https://arxiv.org/abs/1606.03490
- [P048] Sundararajan et al., "The many Shapley values for model explanation",
  2020 https://arxiv.org/abs/1908.08474
- [P049] Miller, "Explanation in artificial intelligence: Insights from the
  social sciences", 2019 https://arxiv.org/abs/1706.07269
- [P050] Goodfellow et al., "Explaining and Harnessing Adversarial Examples",
  2014 https://arxiv.org/abs/1412.6572
- [P051] Papernot et al., "Practical Black-Box Attacks against Machine Learning",
  2016 https://arxiv.org/abs/1602.02697
- [P052] Schott et al., "Towards the first adversarially robust neural network
  model on MNIST", 2019 https://arxiv.org/abs/1805.09190
- [P053] Scholkopf et al., "Toward Causal Representation Learning", 2021
  https://arxiv.org/abs/2102.11107
- [P054] Kusner et al., "Counterfactual Fairness", 2017
  https://arxiv.org/abs/1705.10264
- [P055] Zhang et al., "Mitigating Unwanted Biases with Adversarial Learning",
  2018 https://arxiv.org/abs/1801.07593
- [P056] Nabi et al., "Fair inference through semiparametric-efficient estimation
  over constraint-specific paths", 2018 https://arxiv.org/abs/1806.09055
- [P057] Hardt et al., "Equality of Opportunity in Supervised Learning", 2016
  https://arxiv.org/abs/1610.02413
- [P058] Amodei et al., "Concrete Problems in AI Safety", 2016
  https://arxiv.org/abs/1606.06565
- [P059] Soares et al., "Agent Foundations for Artificial General Intelligence",
  2017 https://intelligence.org/files/Foundations.pdf
- [P060] Everitt et al., "Sequential Extensions of Causal Models", 2018
  https://arxiv.org/abs/1807.10470
- [P061] Hendrycks, "Natural and Artificial Intelligence", 2023
  https://arxiv.org/abs/2307.04187
- [P062] Brendel et al., "Decision-based adversarial attacks: reliable attacks
  against machine learning models", 2018 https://arxiv.org/abs/1712.04248
- [P063] Rubin, "Estimating causal effects of treatments in randomized and
  nonrandomized studies", 1974 https://doi.org/10.1037/h0037350

# Part IV: Multi-Step & Dynamic Decisions

## 12: Causal World Models & Reinforcement Learning

### Topics
- Sequential decision problems: MDPs and POMDPs
- Utilities over time and discount factors
- Solving MDPs: value iteration and policy iteration
- Causal world models: learning and planning with SCMs
- Model-based causal RL: counterfactual rollouts and policy search
- Off-policy evaluation with causal guarantees (DM, IPW, DR estimators)
- Invariant causal mechanisms and distribution-shift robustness
- Multi-agent causal RL: interference, Nash equilibria, and spillover

### Lessons
- `msml610/lectures_source/Lesson12.1-Reinforcement_learning.txt`
  - [FULL] — MDPs/POMDPs; utilities/discount; value & policy iteration; model-based/free RL; Causal RL; SCMs for MDPs; Counterfactual credit assignment; Deconfounding off-policy; Causal Generalization
- `msml610/lectures_source/Lesson16.5-Reasoning_Memory_and_Planning.txt`
  - [PART] — World Models (WebDreamer)
- `msml610/lectures_source/Lesson09.5-Kalman_Filter.txt`
  - [PART] — POMDP-adjacent state estimation

### Tutorials

### Related packages
- contextualbandits (1,700): Python implementations of contextual bandit
  algorithms
- MABWiser (280): Multi-armed bandit library with sklearn-style API
- PyXAB (200): Research-focused library for X-armed bandits and online
  optimization

### Related books
- [B030] Sutton et al., "Reinforcement Learning: An Introduction", 2018
- [B031] Szepesvári, "Algorithms for Reinforcement Learning", 2010
- [B032] Ness et al., "Causal AI", 2023

## 13: Forecasting Under Causal Intervention

### Topics
- Why standard forecasting breaks under intervention
- Causal constraints on time-series models
- Bayesian structural time series with causal priors
- Counterfactual forecasting and synthetic control
- Adaptive forecasting under feedback and regime shifts

### Lessons
- `msml610/lectures_source/Lesson10.2-Causal_Inference_for_Time_Series.txt`
  - [FULL] — forecasting breaks under intervention; Granger; ITS; DiD; Synthetic Control; Structural VARs; when temporal structure misleads
- `msml610/lectures_source/Lesson10.1-Timeseries_forecasting.txt`
  - [PART] — Bayesian Time Series Models; Markov-Switching (regime shifts); State Space Models
- `msml610/lectures_source/Lesson08.4.txt`
  - [PART] — Synthetic control; Difference-in-differences

### Tutorials

### Related packages
- TiMINo (3,600): Time-series causal discovery under independent noise
  assumptions
- orbit (2,000): Bayesian time series models
- HMMlearn (1,600): Hidden Markov Models with sklearn API
- BETS (350): Time-series causal network inference using elastic net regression

### Related books
- [B023] Hyndman et al., "Forecasting: Principles and Practice", 2021
- [B033] Hanke et al., "Business Forecasting", 2009
- [B022] Hamilton, "Time Series Analysis", 1994

## 14: Feedback Loops & Adaptive Causal Systems

### Topics
- Decisions change the system: performativity and Goodhart's law
- Time-varying and non-stationary causal graphs
- Online causal discovery and structure adaptation
- Bandit algorithms with causal side information
- Causal inference under feedback: dynamic treatment regimes

### Lessons
- `msml610/lectures_source/Lesson08.1-Causal_AI_intro.txt`
  - [PART] — Feedback Loops (Problem 5); Distribution Shift
- `msml610/lectures_source/Lesson09.3-Multi_Armed_Bandits.txt`
  - [PART] — Non-Stationary Bandits; Contextual Bandits
- `msml610/lectures_source/Lesson11.1-Decision_Making_with_Causal_Models.txt`
  - [PART] — Causal Multi-Armed Bandits
- `msml610/lectures_source/Lesson12.2-Causal_Discovery.txt`
  - [WEAK] — When Discovery Should Change Your DAG (online adaptation)
- Gap: performativity/Goodhart; dynamic treatment regimes

### Tutorials

### Related packages

### Related books

# Part V: Implementation (Deployment, Monitoring, Communication)

## 15: Communicating Decisions to Executives

### Topics
- From causal estimates to recommendations
- Visualizing uncertainty and trade-offs
- Communicating risk and assumptions
- Narrative structure for decisions
- Executive decision brief template

### Lessons
- `msml610/lectures_source/Lesson11.1-Decision_Making_with_Causal_Models.txt`
  - [PART] — Communicating Uncertainty to Stakeholders (+Worked Example); Multi-Criteria Trade-offs; Visualizing Risk Aversion
- `msml610/lectures_source/Lesson08.1-Causal_AI_intro.txt`
  - [WEAK] — Roles in Hybrid Teams; Executing a Hybrid Team Project
- No slide for "Executive decision brief template"

### Tutorials

### Related packages

### Related books

## 16: Deployment and the Decision Lifecycle

### Topics
- Bridging development and production
- Deployment strategies and rollout
- Monitoring causal assumptions in production
- A/B testing and continuous experimentation
- Shadow deployment and canary analysis

### Lessons
- `msml610/lectures_source/Lesson08.5-Experimentation.txt`
  - [PART] — A/B testing; continuous experimentation; when to experiment vs observe
- `msml610/lectures_source/Lesson08.1-Causal_AI_intro.txt`
  - [WEAK] — Step 7: Preparing for Deployment in Business
- Gap: rollout/shadow/canary; monitoring causal assumptions

### Tutorials

### Related packages
- CausalImpact (5,600): Causal inference for intervention analysis
- CausalML (4,800): Uplift modeling and causal inference
- EconML (4,600): ML-based causal effect estimation
- Azua (1,400): Causal decision-making framework
- ALICE (1,000): ML and econometrics integration

### Related books
- [B034] Iansiti et al., "Competing in the Age of AI", 2020
- [B001] Agrawal et al., "Prediction Machines", 2018
- [B035] Kleppmann, "Designing Data-Intensive Applications", 2017

## 17: Trust, Explainability, and Failure Modes

### Topics
- Building trust in decision systems
- Model auditing and causal explainability
- Failure modes and ethical pitfalls
- Guardrails and human-in-the-loop
- Governance and accountability

### Lessons
- `msml610/lectures_source/Lesson13.1-Explainability.txt`
  - [FULL] — SHAP; LIME; permutation importance; counterfactual explanations; Causal AI and Explainability; Quality/Faithfulness/Stability of Explanations
- `msml610/lectures_source/Lesson15.1-Causal_Reasoning_Agents.txt`
  - [PART] — Trustworthy AI Through Causality; guardrails; human oversight
- `msml610/lectures_source/Lesson08.1-Causal_AI_intro.txt`
  - [PART] — Importance of Explainability; Approaches to Explainability

### Tutorials

### Related packages

### Related books

# Appendix

## Advanced Topics for Time Series Predictions

- Self-Supervised and Representation Learning for Time Series
  - Contrastive learning (e.g., TS-TCC, SimCLR adaptations)
  - Predictive coding models (e.g., CPC)
  - Applications: few-shot forecasting, anomaly detection

- Hierarchical Bayesian Forecasting
  - Multi-level time series models
  - Shrinkage across groups
  - Handling partial pooling across different but related series

- Reinforcement Learning for Time Series Decision Making
  - Forecasting coupled with decision making
  - Inventory control, dynamic pricing
  - Predict-then-Optimize pipelines

- Transformers and Attention Mechanisms for Time Series
  - Temporal Fusion Transformer (TFT)
  - Informer, Autoformer, FEDformer
  - Handling long-term dependencies better than RNNs

- Energy-Based Models and Diffusion Models for Forecasting
  - Energy-based forecasting models
  - Diffusion probabilistic models adapted for sequences

- Time Series Generative Models
  - GANs for time series (e.g., TimeGAN)
  - Variational Autoencoders (VAEs) for synthetic data generation
  - Applications: simulation, data augmentation

- Long-Horizon Forecasting Challenges
  - Distribution shift over long horizons
  - Degradation of model accuracy
  - Specialized architectures: recurrent decoders, multi-resolution forecasting

- Uncertainty Quantification and Calibration
  - Prediction intervals
  - Coverage probability and reliability diagrams
  - Post-hoc calibration (e.g., temperature scaling)
