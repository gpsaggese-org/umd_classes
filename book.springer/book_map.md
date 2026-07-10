**Title**:
- From Data to Decisions: Building Decision Systems with Probabilistic Causal
  Reasoning

- Reasoning under Uncertainty: Causal Machine Learning for Decision Making

**Target audience:**
- Senior ML engineers and data scientists with a statistics and probabilistic ML
  background who build production decision systems
- Working knowledge of causal basics (DAGs, SCMs, do-calculus) assumed

# Part I: Why Businesses Need Decisions, not Predictions (Motivation)

## 1: From Prediction Pipelines to Decision Pipelines

### Topics
- Prediction vs. decision: fundamentally different mathematical problems
  (traditional ML relies on correlation)
- Correlation-based ML encodes confounding as causation: Pr(Y | X) ≠ Pr(Y |
  do(X)), so acting on correlations backfires
- No interventions or counterfactuals, and the ladder of causation: observation,
  intervention, and counterfactual reasoning
- Simpson's paradox and policy reversals: why predictive accuracy fails in
  decisions
- Predictions are not recommendations: black-box scores give no actionable lever
  or "why"
- The decision pipeline: from causal models to utility-maximizing actions
- Causal models as the foundation for decision-making
- Why organizations fail: the cost of ignoring causality in data-driven systems

### TODO
- [ ] Add the topics from actual slides
- [ ] Split Chap 1 in more chapters with also "solutions" and "examples"
- [ ] Add
  - /Users/saggese/src/csfy1/blog/docs/posts/Cracking_the_Long_Tail_of_Data_Science_Problems.md
  - /Users/saggese/src/csfy1/blog/docs/posts/Data_Is_Dumb_And_Thats_Why_Causality_Matters.md
- [ ] Replace some of the introduction with a Chapter on "Data"?

### Lessons
- `msml610/lectures_source/Lesson08.1-Causal_AI_intro.txt`
  - [FULL] — Ladder of Causation; Data Science → Decision Science; Causal vs
    Predictive Questions; Roadmap Prediction→Decision; Data Analytics
    Sophistication (maturity model); Why AI Projects Fail
- `msml610/lectures_source/Lesson11.1-Decision_Making_with_Causal_Models.txt`
  - [PART] — From Predictions to Decisions; Prediction vs Decision Side-by-Side;
    Simpson's Paradox (+Causal Resolution); Policy Reversal
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
- [B039] Hurwitz & Thompson, "Causal Artificial Intelligence", 2024

### Related papers
- [P005] Pearl, "Simpson's Paradox, Confounding, and Collapsibility", 1999
  https://bayes.cs.ucla.edu/BOOK-2K
- [P007] Zhang et al., "A Survey on Causal Inference", 2020
  https://arxiv.org/pdf/2002.05209.pdf
- [P009] Pearl, "The Seven Pillars of Causal Reasoning with Reflections on
  Machine Learning", 2021
  https://cacm.acm.org/research/seven-pillars-of-causal-reasoning-with-reflections-on-machine-learning/

## 2: Why Good Data Leads to Bad Decisions

### Topics
- Statistical significance traps and overfitting: peeking, multiple comparisons,
  novelty effects, and burning the test set
- Heterogeneous treatment effects: when average effects mask sub-group reversals
- Confounding in causal ML: biases when causal assumptions are unmet
- Selection bias and the missing-counterfactual problem: data reflects only
  decisions actually made (e.g., approved loans)
- Feedback loops: how predictions change the world and break model assumptions
- Strategic and adversarial response: deployed models get gamed (credit gaming,
  SEO), violating passive-agent assumptions
- Distribution shift and causal assumptions under intervention
- Decision readiness under uncertainty: knowing when causal claims are safe to
  act on, especially in small-data regimes

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
- [B003] Huyen, "Designing Machine Learning Systems", 2022

### Related papers
- [P001] Ribeiro et al., "Why Should I Trust You? Explaining the Predictions of
  Any Classifier", 2016 https://arxiv.org/pdf/1602.04938.pdf
- [P002] Lundberg & Lee, "A Unified Approach to Interpreting Model Predictions",
  2017 https://arxiv.org/pdf/1705.07874.pdf
- [P003] Taori et al., "Data Feedback Loops: Model-driven Amplification of
  Dataset Biases", 2020 https://proceedings.mlr.press/v202/taori23a/taori23a.pdf

## 3: Problem Framing and Intervention Design

### Topics
- From KPI selection to causal objectives and utilities: avoiding Goodhart's law
  when a proxy becomes the target
- Cost-asymmetry in decisions: why symmetric losses (log-loss, MSE) misprice
  asymmetric business errors
- Building causal DAGs: variable identification, temporal structure, and domain
  knowledge
- Intervention design: choosing levers, targets, scales, and timing
- Causal variable types: confounders, mediators, colliders, and their adjustment
  rules
- Identifiability and causal assumptions: backdoor, frontdoor, and IV conditions
- End-to-end decision framing vs. splitting into individually-solved sub-problems
- Data collection strategy aligned with causal identification requirements

### Lessons
- `msml610/lectures_source/Lesson08.1-Causal_AI_intro.txt`
  - [PART] — Causal AI Workflow Steps 1–7 (Intended Outcomes → Interventions →
    Factors → Build DAG → Data Acquisition → Model Modification → Deployment);
    Marketing Example: Price Intervention
- `msml610/lectures_source/Lesson08.5-Experimentation.txt`
  - [PART] — Decision Framework: Experiment or Observe?; Feasibility Constraints
- No slide for "Causal Project Checklist"

### Tutorials

### Related packages

### Related books
- [B040] Brynjolfsson & McAfee, "Machine, Platform, Crowd", 2021
- [B041] Angrist & Pischke, "Probability, Statistics, and Causal Inference", 2020

### Related papers
- [P004] Imbens & Wooldridge, "Recent Developments in the Econometrics of Program
  Evaluation", 2018 https://www.nber.org/papers/w24318
- [P006] Kaddour et al., "Challenges and Opportunities with Causal Discovery
  Algorithms", 2023 https://www.nature.com/articles/s41598-020-59669-x

# Part II: Advanced Tools & Theory (Foundations)

## 4: Knowledge Representation

### Topics
- Causal DAGs vs. Bayesian networks: how causality orients edges
- Structural equations and mechanisms: modeling how variables depend on parents
- Variable types and adjustment rules: confounders, mediators, colliders,
  moderators
- Temporal structure: causal order, feedback delays, and acyclicity
- Building DAGs from domain knowledge and expert judgment
- Measurement validity and causal assumptions in data collection

### TODO
- [ ] Use and improve the lesson03 content
- [ ] Symbolic logic + embeddings

### Lessons
- `msml610/lectures_source/Lesson08.2-Causal_Networks.txt`
  - [PART] — Building a Causal DAG; variable types
    (mediator/moderator/confounder/collider); temporal structure
- `msml610/lectures_source/Lesson12.2-Causal_Discovery.txt`
  - [PART] — Using Domain Knowledge as Constraints; Combining Discovery with
    Expert Judgment
- `msml610/lectures_source/Lesson03-Knowledge_representation.txt`
  - [WEAK] — symbolic KR (ontologies, FOL, knowledge graphs); thin overlap — book
    Ch4 = decision scoping, not symbolic logic

### Tutorials

### Related packages

### Related books
- [B047] Jensen & Nielsen, "Bayesian Networks and Decision Graphs", 2007
- [B054] Spirtes et al., "Causation, Prediction, and Search", 2000
- [B055] Heckerman et al., "Learning Bayesian Networks", 1995

### Related papers
- [P064] Lauritzen, "Graphical Models", 1996
- [P065] Richardson, "Markov Properties for Acyclic Directed Mixed Graphs", 2003
  https://arxiv.org/abs/1209.1514

## 5: Advanced Probabilistic ML

### Topics
- Short summary from Lesson6*

### Lessons
- `msml610/lectures_source/Lesson11.2-Probabilistic_deep_learning.txt`
  - [FULL] — VAEs; Normalizing Flows; Bayesian NNs; VI/SVI; MCMC; Calibration;
    Conformal Prediction; Neural Processes; Deep Latent Variable Models
- `msml610/lectures_source/Lesson07.1-Intro_to_Probabilistic_Programming.txt`
  - [PART] — PPLs, Bayesian models (Pyro/PyMC/Stan)
- `msml610/lectures_source/Lesson96.Refresher_stochastic_processes.txt`
  - [WEAK] — Gaussian Processes (one slide)
- Gap: amortized VI; neural posterior estimation / simulation-based inference

### Tutorials

### Related packages

### Related books
- [B048] Bishop, "Pattern Recognition and Machine Learning", 2006
- [B004] Koller et al., "Probabilistic Graphical Models", 2009
- [B043] Pearl, "Probabilistic Reasoning in Intelligent Systems: Networks of
  Plausible Inference", 1988
- [B056] Blei et al., "Variational Inference: A Review for Statisticians", 2017
- [B057] Rezende & Mohamed, "Variational Inference with Normalizing Flows", 2015

### Related papers
- [P066] Kingma & Welling, "Auto-Encoding Variational Bayes", 2014
  https://arxiv.org/abs/1312.6114
- [P067] Rezende et al., "Stochastic Backpropagation and Approximate Inference in Deep Generative Models", 2014
  https://arxiv.org/abs/1401.4082
- [P068] Hoffman et al., "Stochastic Variational Inference", 2013
  https://arxiv.org/abs/1206.7051
- [P069] Lakshminarayanan et al., "Simple and Scalable Predictive Uncertainty Estimation using Deep Ensembles", 2017
  https://arxiv.org/abs/1706.04599
- [P070] Grangier et al., "Exploring the Space of Neural Processes with Variational Inference", 2019
  https://arxiv.org/abs/1905.12141

## 6: Advanced Causal Modeling

### Topics
- Causal discovery from data: identifiability, Markov equivalence, and
  assumptions
- Discovery algorithms: constraint-based (PC/FCI), score-based (GES), functional
  (LiNGAM, ANM)
- Faithfulness and causal sufficiency: when discovery succeeds and fails
- Latent confounders: proxy variables, negative controls, and adjustment
  strategies
- Causal representation learning: disentangling mechanisms for domain transfer
- Sensitivity analysis and robustness: E-values, bounds, and partial
  identification

### Lessons
- `msml610/lectures_source/Lesson12.2-Causal_Discovery.txt`
  - [FULL] — algorithm families (constraint/PC-FCI, score/GES,
    functional/LiNGAM-ANM); Markov equivalence; identifiability; faithfulness;
    refutation
- `msml610/lectures_source/Lesson08.3-Do_Calculus.txt`
  - [PART] — do-calculus rules; back/front-door adjustment
- `msml610/lectures_source/Lesson08.2-Causal_Networks.txt`
  - [PART] — SCM; causal DAGs (basics)
- `msml610/lectures_source/Lesson11.2-Probabilistic_deep_learning.txt`
  - [PART] — Causal Deep Learning (representation learning)
- Gap: latent confounders/proxy/negative controls; E-values/sharp-bounds
  sensitivity

### Tutorials

### Related packages

### Related books
- [B049] Imbens, Angrist & Rubin, "Causal Inference for the Social, Biological, and Biomedical Sciences", 2015
- [B050] Hernán & Robins, "Causal Inference: What If", 2020
- [B053] Molak, "Causal Inference and Discovery in Python", 2023
- [B007] Pearl, "Causality", 2009
- [B008] Peters et al., "Elements of Causal Inference", 2017
- [B027] Spirtes et al., "Causation, Prediction, and Search", 2000
- [B042] Pearl et al., "Causal Inference in Statistics: A Primer", 2016
  https://ftp.cs.ucla.edu/pub/stat_ser/r481.pdf

### Related papers
- [P008] Peters et al., "Causality: Models, Learning, and Inference", 2023
  https://arxiv.org/pdf/2012.13993.pdf
- [P011] Peters et al., "Elements of Causal Inference: Foundations and Learning
  Algorithms", 2020
  https://mitpress.mit.edu/9780262037310/elements-of-causal-inference/

# Part III: Single-Step Decisions

## 7: Decision Theory Foundations

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

### Lessons
- `msml610/lectures_source/Lesson11.1-Decision_Making_with_Causal_Models.txt`
  - [FULL] — Utility Functions; Expected Utility Principle
    (+insurance/two-treatment examples); Decision Networks (=influence diagrams);
    Solving a Decision Network; Risk Preferences; Aleatoric vs Epistemic
    Uncertainty
- `msml610/lectures_source/Lesson12.1-Reinforcement_learning.txt`
  - [PART] — MEU; Dynamic Decision Networks

### Tutorials

### Related packages

### Related books
- [B047] Jensen & Nielsen, "Bayesian Networks and Decision Graphs", 2007
- [B028] Kochenderfer, "Decision Making Under Uncertainty", 2015
- [B029] Russell et al., "Artificial Intelligence: A Modern Approach", 2020

### Related papers
- [P071] von Neumann & Morgenstern, "Theory of Games and Economic Behavior", 1944
- [P072] Savage, "The Foundations of Statistics", 1954
- [P073] Raiffa, "Decision Analysis: Introductory Lectures on Choices under Uncertainty", 1968
- [P074] Keeney & Raiffa, "Decisions with Multiple Objectives: Preferences and Value Trade-offs", 1976

## 8: Decision-Making with Causal Models

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

### Lessons
- `msml610/lectures_source/Lesson11.1-Decision_Making_with_Causal_Models.txt`
  - [FULL] — Bayesian Decision-Making; Value of Information (EVPI/EVSI); Bayesian
    Optimization for Experimentation; Acquisition Functions; Causal Bayesian
    Optimization; Exploration vs Exploitation; Causal Multi-Armed Bandits;
    Counterfactual decisions
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
- [B058] Bishop & Nasrabadi, "Pattern Recognition and Machine Learning", 2006

### Related papers
- [P075] Gittins, "Bandit Processes and Dynamic Allocation Indices", 1979
- [P076] Thompson, "On the Likelihood that One Unknown Probability Exceeds Another in View of the Evidence of Two Samples", 1933
- [P077] Auer, "Using Confidence Bounds for Exploration-Exploitation Trade-offs", 2002
- [P078] Mockus et al., "Bayesian Approach to Global Optimization and Application to Multiphase and Multicriteria Design", 1978

## 9: Policy Learning & Distributional Causal Effects

### Topics
- Heterogeneous treatment effects and CATE: learning who benefits from treatment
- Doubly robust estimation and double/debiased ML: reducing sensitivity to
  nuisance parameters
- Meta-learners for heterogeneity: T-, S-, X-, R-learners and when to use each
- Distributional and quantile effects: going beyond average treatment effects
- Off-policy learning and policy optimization: evaluating and improving policies
  from data
- Safe policy improvement: deployable decisions with finite-sample guarantees

### Lessons
- `msml610/lectures_source/Lesson08.4.txt`
  - [FULL] — Metalearners T/S/X/R-Learner; R-learner (Double/Debiased ML);
    Double-ML for CATE; Effect heterogeneity; CATE evaluation; Cumulative
    Gain/AUC
- `msml610/lectures_source/Lesson08.5-Experimentation.txt`
  - [PART] — Policy Evaluation and Off-Policy Learning
- `msml610/lectures_source/Lesson12.1-Reinforcement_learning.txt`
  - [WEAK] — off-policy / deconfounding
- Gap: quantile/distributional treatment effects; safe policy improvement

### Tutorials

### Related packages

### Related books
- [B046] Durai Rajamanickam, "Causal Inference for Machine Learning Engineers", 2024
- [B014] Angrist et al., "Mostly Harmless Econometrics", 2008
- [B059] Athey & Wager, "Policy Learning with Observational Data", 2019

### Related papers
- [P079] Athey & Wager, "Efficient Policy Learning", 2021
  https://arxiv.org/abs/2011.02038
- [P080] Kennedy, "Optimal Uniform Convergence Rates and Adaptive Estimation of Nonparametric Quantile Effects", 2020
  https://arxiv.org/abs/2010.05893
- [P081] Chernozhukov et al., "Double Machine Learning for Treatment and Causal Parameters", 2018
  https://arxiv.org/abs/1701.08687
- [P082] Kunzel et al., "Metalearners for Estimating Heterogeneous Treatment Effects Using Machine Learning", 2019
  https://arxiv.org/abs/1706.03762

## 10: Partial Identification & Robust Inference

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
- [B051] Cunningham, "Causal Inference: The Mixtape", 2021
- [B060] Manski, "Identification for Prediction and Decision", 2007
- [B061] Rotnitzky et al., "Semiparametric Regression for the Social, Behavioral, and Biomedical Sciences", 2011

### Related papers
- [P083] Manski, "Partial Identification of Probability Distributions", 2003
  https://doi.org/10.1007/978-1-4419-1254-1_1
- [P084] Rosenbaum & Rubin, "Assessing Sensitivity to an Unobserved Binary Covariate in an Observational Study with Binary Outcome", 1983
  https://doi.org/10.1080/01621459.1983.10478144
- [P085] VanderWeele & Ding, "Sensitivity Analysis in Observational Research: Introducing the E-Value", 2017
  https://doi.org/10.7326/M16-2607
- [P086] Chernozhukov et al., "Bounds on Treatment Effects in the Presence of Unobserved Confounding", 2013
  https://arxiv.org/abs/1311.2884

## 11: Agentic Causal Reasoning

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

### Lessons
- `msml610/lectures_source/Lesson15.1-Causal_Reasoning_Agents.txt`
  - [FULL] — LLM causal limits; pattern vs causal reasoning; CoT causal
    prompting; integrating causal+probabilistic; causal agent architectures;
    causal MDPs; Trustworthy AI (transparency/robustness/fairness/safety);
    guardrails
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
- [B036] Christian, "The Alignment Problem", 2020
- [B037] Russell, "Human Compatible", 2019
- [B038] Schölkopf et al., "Causal Artificial Intelligence", 2021

### Related papers
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
- Markov decision processes: states, actions, transitions, and solving with
  value/policy iteration
- Utilities over time: discount factors, finite vs. infinite horizons, and
  optimality criteria
- Causal world models: structural causal models as environment dynamics for
  planning
- Model-based reinforcement learning: learning dynamics, counterfactual rollouts,
  and policy search
- Off-policy evaluation with causal guarantees: doubly robust, IPW, and DR
  estimators
- Invariant causal mechanisms and environment generalization: learning robust
  policies across shifts
- Partially observable MDPs: state inference and planning under hidden variables

### Lessons
- `msml610/lectures_source/Lesson12.1-Reinforcement_learning.txt`
  - [FULL] — MDPs/POMDPs; utilities/discount; value & policy iteration;
    model-based/free RL; Causal RL; SCMs for MDPs; Counterfactual credit
    assignment; Deconfounding off-policy; Causal Generalization
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
- [B044] Puterman, "Markov Decision Processes: Discrete Stochastic Dynamic Programming", 1994
- [B062] Barto & Sutton, "Reinforcement Learning: An Introduction", 2018

### Related papers
- [P087] Hafner et al., "Dream to Control: Learning Behaviors by Latent Imagination", 2020
  https://arxiv.org/abs/1912.01603
- [P088] Chua et al., "Deep Reinforcement Learning in a Handful of Trials using Probabilistic Dynamics Models", 2018
  https://arxiv.org/abs/1805.12114
- [P089] Janner et al., "When to Trust Your Model: Model-Based Policy Optimization", 2019
  https://arxiv.org/abs/1907.04629
- [P090] Dai et al., "Causal Policy Gradient for Lifelong Reinforcement Learning", 2022
  https://arxiv.org/abs/2206.14925
- [P091] Precup et al., "Off-Policy Temporal-Difference Learning with Function Approximation", 2001
  https://arxiv.org/abs/cs/0106227

## 13: Forecasting Under Causal Intervention

### Topics
- Why temporal patterns fail under intervention: distribution shift and causal
  assumptions
- Granger causality and causal constraints on time-series models
- Difference-in-differences and synthetic control: comparing counterfactual
  scenarios
- Structural time series with causal priors: Bayesian modeling of interventions
- Online learning under nonstationarity: adapting to feedback and regime shifts
- Forecasting with SCMs: causal models as alternatives to black-box time-series

### Lessons
- `msml610/lectures_source/Lesson10.2-Causal_Inference_for_Time_Series.txt`
  - [FULL] — forecasting breaks under intervention; Granger; ITS; DiD; Synthetic
    Control; Structural VARs; when temporal structure misleads
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
- [B063] Brodsky & Darkhovsky, "Nonparametric Methods in Change Point Problems", 1993

### Related papers
- [P092] Abadie & Gardeazabal, "The Economic Costs of Conflict: A Case Study of the Basque Country", 2003
  https://doi.org/10.1257/000282803321455188
- [P093] Angrist & Pischke, "Mostly Harmless Econometrics: An Empiricist's Companion", 2008
  https://www.mostlyharmlesseconometrics.com
- [P094] Brodsky & Darkhovsky, "Non-parametric Statistical Diagnosis: Problems and Methods", 1993
- [P095] Imbens & Wooldridge, "Recent Developments in the Econometrics of Program Evaluation", 2009
  https://doi.org/10.1016/j.jeconom.2008.12.010

## 14: Feedback Loops & Adaptive Causal Systems

### Topics
- Performativity and Goodhart's law: decisions that change the world and break
  past patterns
- Causal graphs that change over time: nonstationarity and structural adaptation
- Online causal discovery: learning and revising the causal model from feedback
- Contextual and causal bandits: exploration with side information under feedback
- Dynamic treatment regimes: adaptive decisions that respond to evolving
  patient/environment state
- Learning from adaptive experiments: methods for sequential decision-making with
  feedback

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
- [B064] Goodhart, "Monetary Theory and Practice", 1975
- [B065] Campbell & Shiller, "Valuation Ratios and the Long-Run Stock Market Outlook", 1998
- [B066] Acemoglu & Robinson, "Why Nations Fail: The Origins of Power, Prosperity, and Poverty", 2012

### Related papers
- [P096] Goodhart, "Problems of Monetary Management: The U.K. Experience", 1984
  https://doi.org/10.1016/S0261-5606(84)80005-8
- [P097] Strathern, "Improving Ratings: Audit in the British University System", 1997
  https://doi.org/10.1080/03075079712331380714
- [P098] Taori et al., "Data Feedback Loops: Model-driven Amplification of Dataset Biases", 2023
  https://arxiv.org/abs/2209.03942
- [P099] Liu et al., "Performative Prediction", 2021
  https://arxiv.org/abs/2007.02153

# Part V: Implementation (Deployment, Monitoring, Communication)

## 15: Building Stakeholder Alignment

### Topics
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

### TODO

### Lessons
- `msml610/lectures_source/Lesson11.1-Decision_Making_with_Causal_Models.txt`
  - [PART] — Communicating Uncertainty to Stakeholders (+Worked Example);
    Multi-Criteria Trade-offs; Visualizing Risk Aversion
- `msml610/lectures_source/Lesson08.1-Causal_AI_intro.txt`
  - [PART] — Roles in Hybrid Teams; Executing a Hybrid Team Project; Causal AI
    Workflow (domain knowledge elicitation)
- `msml610/lectures_source/Lesson08.3-Do_Calculus.txt`
  - [PART] — Visual DAG explanation, confounding intuition
- `msml610/lectures_source/Lesson12.2-Causal_Discovery.txt`
  - [PART] — Using Domain Knowledge as Constraints; Combining Discovery with Expert Judgment

### Tutorials

### Related packages

### Related books
- [B067] Tufte, "The Visual Display of Quantitative Information", 2001
- [B068] Cairo, "The Functional Art: An Introduction to Information Graphics and Visualization", 2012
- [B069] Spiegelhalter et al., "Sex by Numbers: What Statistics Can and Cannot Tell Us About Sexuality", 2016
- [B070] Few, "Now You See It: Simple Visualization Techniques for Quantitative Analysis", 2009
- [B040] Brynjolfsson & McAfee, "Machine, Platform, Crowd", 2021

### Related papers
- [P100] Kahneman & Tversky, "Prospect Theory: An Analysis of Decision under Risk", 1979
  https://doi.org/10.2307/1914185
- [P101] Tversky & Kahneman, "Judgment under Uncertainty: Heuristics and Biases", 1974
  https://doi.org/10.1126/science.185.4157.1124
- [P102] Slovic, "Perception of Risk", 2000
  https://doi.org/10.1126/science.280.5364.1030
- [P103] Spiegelhalter, "Trust, but Verify: The Role of Uncertainty in Data Visualization", 2019
- [P006] Kaddour et al., "Challenges and Opportunities with Causal Discovery Algorithms", 2023
  https://www.nature.com/articles/s41598-020-59669-x

## 16: Deployment, Monitoring, and Adaptation

### Topics
- From notebook to production: operationalizing causal decision systems
- Cost-aware deployment strategies: phased rollout, shadow mode, and canary
  analysis tailored to decision cost asymmetry
- Operationalizing causal assumption monitoring: testable vs. untestable
  assumptions, failure detection
  - **Directly testable assumptions**: temporal stability of effects, proxy
    variable validity, treatment effect heterogeneity stability
  - **Indirectly testable assumptions**: robustness bounds via sensitivity
    analysis, negative controls, instrumental variable diagnostics
  - **Domain-assessed assumptions**: causal graph structure, sufficiency of
    confounding set (requires expert re-assessment)
  - Concrete monitoring dashboards: metrics that flag assumption breakdown
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

### TODO

### Lessons
- `msml610/lectures_source/Lesson08.5-Experimentation.txt`
  - [FULL] — A/B testing; continuous experimentation; when to experiment vs
    observe; Feasibility Constraints; sequential decision-making
- `msml610/lectures_source/Lesson08.1-Causal_AI_intro.txt`
  - [PART] — Step 7: Preparing for Deployment in Business; Feedback Loops;
    Distribution Shift
- `msml610/lectures_source/Lesson08.4.txt`
  - [PART] — Effect heterogeneity and subgroup analysis
- `msml610/lectures_source/Lesson09.3-Multi_Armed_Bandits.txt`
  - [PART] — Exploration vs Exploitation; Sequential Decision-Making

### Tutorials

### Related packages
- CausalImpact (5,600): Causal inference for intervention analysis
- CausalML (4,800): Uplift modeling and causal inference
- EconML (4,600): ML-based causal effect estimation
- Azua (1,400): Causal decision-making framework
- Evidently (2,500): ML monitoring and data drift detection
- WhyLabs (—): ML observability and monitoring
- Feature Store (e.g., Tecton, Feast): managing features for causal models in production

### Related books
- [B034] Iansiti et al., "Competing in the Age of AI", 2020
- [B035] Kleppmann, "Designing Data-Intensive Applications", 2017
- [B052] Géron, "Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow", 2022
- [B071] Reinsel et al., "The Digitization of the World: From Edge to Core", 2018
- [B003] Huyen, "Designing Machine Learning Systems", 2022

### Related papers
- [P104] Amershi et al., "Software Engineering for Machine Learning: A Case Study", 2019
  https://arxiv.org/abs/1909.09090
- [P105] Sculley et al., "Technical Debt in Machine Learning Systems", 2015
  https://doi.org/10.5555/2969442.2969519
- [P106] Polyzotis et al., "Data Validation for Machine Learning", 2019
  https://arxiv.org/abs/1901.09162
- [P107] Breck et al., "The ML Test Score: A Rubric for ML Production Readiness and Technical Debt Reduction", 2017
  https://arxiv.org/abs/1702.06783
- [P003] Taori et al., "Data Feedback Loops: Model-driven Amplification of Dataset Biases", 2020
  https://proceedings.mlr.press/v202/taori23a/taori23a.pdf
- [P098] Taori et al., "Data Feedback Loops: Model-driven Amplification of Dataset Biases", 2023
  https://arxiv.org/abs/2209.03942
- [P099] Liu et al., "Performative Prediction", 2021
  https://arxiv.org/abs/2007.02153
- [P079] Athey & Wager, "Efficient Policy Learning", 2021
  https://arxiv.org/abs/2011.02038

## 17: Trust, Explainability, Fairness, and Governance

### Topics
- Building trust: transparency, stakeholder alignment, and justified confidence
  in causal decisions
- Causal vs. statistical explainability: distinguishing mechanisms (do-calculus,
  SCM) from attribution (SHAP, LIME, permutation importance)
  - Causal explainability answers: "Why did we intervene?" (via causal mechanisms
    and counterfactuals)
  - Statistical explainability answers: "What features correlated with this
    decision?" (can be misleading if features are confounders, not levers)
  - Operational risk: high statistical importance + low causal relevance, or vice
    versa
- Operationalizing causal explainability in production: decision explanations at
  serve-time, contrast with feature importance
- Identifying failure modes: when decisions fail and why (model misspecification,
  distribution shift, assumption breakdown, feedback loops)
- Fairness under deployment: preventing disparate impact, fairness monitoring
  across subgroups, heterogeneous decision effects
- Override procedures and human-in-the-loop: escalation mechanisms, decision
  disputes, and when to trust vs. challenge the system
- Failure mode detection and response: monitoring, alerting, root cause analysis,
  and remediation
- Decision governance and audit trails: who approved what, when assumptions
  broke, what was the impact, and institutional accountability
- Regulatory alignment: GDPR right-to-explanation, fairness certifications, ML
  Act compliance, and documentation requirements
- Guardrails and safety constraints: preventing harmful behaviors, maintaining
  causal assumptions, and safeguarding against edge cases

### TODO

### Lessons
- `msml610/lectures_source/Lesson13.1-Explainability.txt`
  - [FULL] — SHAP; LIME; permutation importance; counterfactual explanations; Causal AI and Explainability; Quality/Faithfulness/Stability of Explanations
- `msml610/lectures_source/Lesson15.1-Causal_Reasoning_Agents.txt`
  - [FULL] — Trustworthy AI Through Causality; Transparency/Robustness/Fairness/Safety; guardrails; human oversight; causal guardrails
- `msml610/lectures_source/Lesson08.1-Causal_AI_intro.txt`
  - [PART] — Importance of Explainability; Approaches to Explainability; Why Organizations Fail
- `msml610/lectures_source/Lesson08.4.txt`
  - [PART] — Effect heterogeneity and fairness implications

### Tutorials

### Related packages
- InterpretML (—): Model agnostic interpretation
- Alibi Explain (—): Model explanation algorithms

### Related books
- [B019] Molnar, "Interpretable Machine Learning", 2022
- [B045] Barocas et al., "Fairness and Machine Learning", 2019
  https://fairmlbook.org
- [B072] Metcalf & Moss, "Owning Ethics: Corporate Logics, Silicon Valley, and the Social Implications of Ethical AI", 2019
- [B073] Eubanks, "Automating Inequality: How High-Tech Tools Profile, Police, and Punish the Poor", 2018
- [B036] Christian, "The Alignment Problem", 2020

### Related papers
- [P010] Joshi et al., "Towards Realistic Counterfactual Explanations with Contrastive Pertinent Features", 2019
  https://arxiv.org/pdf/1906.04957.pdf
- [P108] Corbett-Davies et al., "Algorithmic Decision Making and the Cost of Fairness", 2017
  https://arxiv.org/abs/1701.08230
- [P109] Mitchell et al., "Model Cards for Model Reporting", 2019
  https://arxiv.org/abs/1810.03993
- [P110] Buolamwini & Busch, "The Gender Shades: Intersectional Accuracy Disparities in Commercial Gender Classification", 2018
  https://arxiv.org/abs/1801.09453
- [P111] Selbst & Barocas, "The Intuitive Appeal of Explainable Machines", 2018
  https://arxiv.org/abs/1805.06959
- [P047] Lipton, "The Mythos of Model Interpretability", 2018
  https://arxiv.org/abs/1606.03490
- [P048] Sundararajan et al., "The many Shapley values for model explanation", 2020
  https://arxiv.org/abs/1908.08474
- [P049] Miller, "Explanation in artificial intelligence: Insights from the social sciences", 2019
  https://arxiv.org/abs/1706.07269
- [P054] Kusner et al., "Counterfactual Fairness", 2017
  https://arxiv.org/abs/1705.10264
- [P055] Zhang et al., "Mitigating Unwanted Biases with Adversarial Learning", 2018
  https://arxiv.org/abs/1801.07593
- [P056] Nabi et al., "Fair inference through semiparametric-efficient estimation over constraint-specific paths", 2018
  https://arxiv.org/abs/1806.09055
- [P057] Hardt et al., "Equality of Opportunity in Supervised Learning", 2016
  https://arxiv.org/abs/1610.02413
- [P058] Amodei et al., "Concrete Problems in AI Safety", 2016
  https://arxiv.org/abs/1606.06565

# Appendix
