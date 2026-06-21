# Part I: Understanding Causality

## 1: From Prediction Pipelines to Decision Pipelines

**Lessons**
- msml610/lectures_source/Lesson08.1-Causal_AI_intro.txt

**Tutorials**

**Related packages**
- DoWhy (6,600): Causal inference using graphical models
- PyWhy (2,400): Python ecosystem for causal inference
- Azua (1,400): Causal decision-making framework

**Related books**
- [B001] Agrawal et al., "Prediction Machines", 2018
- [B002] Pearl et al., "The Book of Why", 2018
- [B003] Huyen, "Designing Machine Learning Systems", 2022
- [B039] Hurwitz & Thompson, "Causal Artificial Intelligence", 2024
- [B040] Brynjolfsson & McAfee, "Machine, Platform, Crowd", 2021
- [B041] Angrist & Pischke, "Probability, Statistics, and Causal Inference", 2020

**Related Papers**
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

## 2: Bayesian Networks

**Lessons**
- msml610/lectures_source/Lesson06.1-Bayesian_Networks.txt
- msml610/lectures_source/Lesson06.2-Using_Bayesian_Networks.txt

**Tutorials**

**Related packages**
- pgmpy (5,000): Probabilistic Graphical Models (Bayesian Networks, inference)
- Pomegranate (3,600): Probabilistic modeling library
- CausalNex (3,000): Causal reasoning with Bayesian Networks
- bnlearn (1,900): Causal discovery with Bayesian networks
- CausalGraphicalModels (1,500): Toolkit for causal graphs in Python

**Related books**
- [B004] Koller et al., "Probabilistic Graphical Models", 2009
- [B005] Jensen et al., "Bayesian Networks and Decision Graphs", 2007
- [B006] Bishop, "Pattern Recognition and Machine Learning", 2006

## 3: Causal DAGs and Structural Models

**Lessons**
- msml610/lectures_source/Lesson08.3-Do_Calculus.txt

**Tutorials**

**Related packages**
- Dagitty (1,500): DAG creation and causal effect identification
- CausalGraphicalModels (1,500): Toolkit for causal graphs in Python
- Tetrad (1,100): Suite for causal model discovery and analysis
- Geminos (500): Causal diagram generation and analysis

**Related books**
- [B007] Pearl, "Causality", 2009
- [B008] Peters et al., "Elements of Causal Inference", 2017
- [B009] Morgan et al., "Counterfactuals and Causal Inference", 2014

## 11: Decision-Making with Causal Models

**Lessons**
- msml610/lectures_source/Lesson11.1-Decision_Making_with_Causal_Models.txt

**Tutorials**

**Related packages**
- DoWhy (6,600): Causal inference using graphical models
- EconML (4,600): ML-based causal effect estimation
- BoTorch (3,300): Bayesian optimization in PyTorch
- Azua (1,400): Causal decision-making framework

**Related books**
- [B028] Kochenderfer, "Decision Making Under Uncertainty", 2015
- [B029] Russell et al., "Artificial Intelligence: A Modern Approach", 2020
- [B002] Pearl et al., "The Book of Why", 2018

## 12: Causal Reinforcement Learning

**Lessons**
- ./msml610/lectures_source/Lesson12.1-Reinforcement_learning.txt

**Tutorials**

**Related packages**
- contextualbandits (1,700): Python implementations of contextual bandit
  algorithms
- MABWiser (280): Multi-armed bandit library with sklearn-style API
- PyXAB (200): Research-focused library for X-armed bandits and online
  optimization

**Related books**
- [B030] Sutton et al., "Reinforcement Learning: An Introduction", 2018
- [B031] Szepesvári, "Algorithms for Reinforcement Learning", 2010
- [B032] Ness et al., "Causal AI", 2023

## 13: Forecasting Under Causal Intervention

**Lessons**

**Tutorials**

**Related packages**
- TiMINo (3,600): Time-series causal discovery under independent noise
  assumptions
- orbit (2,000): Bayesian time series models
- HMMlearn (1,600): Hidden Markov Models with sklearn API
- BETS (350): Time-series causal network inference using elastic net regression

**Related books**
- [B023] Hyndman et al., "Forecasting: Principles and Practice", 2021
- [B033] Hanke et al., "Business Forecasting", 2009
- [B022] Hamilton, "Time Series Analysis", 1994

## 14: Causal Decision Making in Practice

**Lessons**

**Tutorials**

**Related packages**
- CausalImpact (5,600): Causal inference for intervention analysis
- CausalML (4,800): Uplift modeling and causal inference
- EconML (4,600): ML-based causal effect estimation
- Azua (1,400): Causal decision-making framework
- ALICE (1,000): ML and econometrics integration

**Related books**
- [B034] Iansiti et al., "Competing in the Age of AI", 2020
- [B001] Agrawal et al., "Prediction Machines", 2018
- [B035] Kleppmann, "Designing Data-Intensive Applications", 2017

## 15: Causal Reasoning in AI Systems

**Lessons**
- msml610/lectures_source/Lesson15.1-Causal_Reasoning_Agents.md

**Tutorials**

**Related packages**
- DoWhy (6,600): Causal inference using graphical models
- PyWhy (2,400): Python ecosystem for causal inference
- Causica (2,000): Microsoft tool combining causal discovery and inference with
  deep learning
- ALICE (1,000): ML and econometrics integration

**Related books**
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

**Related Papers**
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
