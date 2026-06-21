// class_scripts/create_book_toc_from_slides.py --input book.Causal_Probabilistic_ML/book_map.md --max_level 2 --in_place
//
// Current TOC: book.Causal_Probabilistic_ML/book_toc.md
// Official TOC: ~/src/notes1/book.manning.Causal_Probabilistic_Machine_Learning/manning.proposal_v3.toc.md

# Part I: Understanding Causality

## 1: The Need for Probabilistic and Causal Machine Learning

### Lessons
- `msml610/lectures_source/Lesson08.1-Causal_AI_intro.txt`

### Target TOC
- The Problem: When Prediction Fails
- What ML Systems Can and Cannot Tell You
- The Ladder of Causation
- Data Science vs. Decision Science
- Tools and Tutorials — Introduction to causal DAGs using real-world examples
- Summary

### TODOs
- [ ] Add content to probabilistic intro

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

## 2: Bayesian Networks and Probabilistic Reasoning

### Lessons
- `msml610/lectures_source/Lesson06.1-Bayesian_Networks.txt`
- `msml610/lectures_source/Lesson06.2-Using_Bayesian_Networks.txt`

### Target TOC
- Probability and Conditional Independence
- Bayesian Networks
- Constructing a Bayesian Network
- Exact and Approximate Inference
- Tools and Tutorials — Implementing Bayesian Networks in PyMC
- Summary

### Tutorials

### Related packages
- pgmpy (5,000): Probabilistic Graphical Models (Bayesian Networks, inference)
- Pomegranate (3,600): Probabilistic modeling library
- CausalNex (3,000): Causal reasoning with Bayesian Networks
- bnlearn (1,900): Causal discovery with Bayesian networks
- CausalGraphicalModels (1,500): Toolkit for causal graphs in Python

### Related books
- [B004] Koller et al., "Probabilistic Graphical Models", 2009
- [B005] Jensen et al., "Bayesian Networks and Decision Graphs", 2007
- [B006] Bishop, "Pattern Recognition and Machine Learning", 2006

## 3: Causal DAGs and Structural Models

### Lessons
- `msml610/lectures_source/Lesson08.3-Do_Calculus.txt`

### Target TOC
- Causal vs. Observational Graphs
- Structural Causal Models
- Special Variable Types (mediators, moderators, confounders, colliders)
- Building Causal DAGs from Domain Knowledge
- Tools and Tutorials — Building and visualizing causal DAGs
- Summary

### Tutorials

### Related packages
- Dagitty (1,500): DAG creation and causal effect identification
- CausalGraphicalModels (1,500): Toolkit for causal graphs in Python
- Tetrad (1,100): Suite for causal model discovery and analysis
- Geminos (500): Causal diagram generation and analysis

### Related books
- [B007] Pearl, "Causality", 2009
- [B008] Peters et al., "Elements of Causal Inference", 2017
- [B009] Morgan et al., "Counterfactuals and Causal Inference", 2014

## 4: From Causal Models to Code

### Lessons
- `msml610/lectures_source/Lesson07.1-Intro_to_Probabilistic_Programming.txt`
- `msml610/lectures_source/Lesson07.2-Posterior_Based_Decisions.txt`
- `msml610/lectures_source/Lesson07.3-Hierarchical_Models.txt`
- `msml610/lectures_source/Lesson07.4-Generalized_Linear_Models.txt`
- `msml610/lectures_source/Lesson07.5-Bayesian_Model_Comparison.txt`


### Target TOC
- Bayesian Inference in Practice
- Generalized Linear Models
- Hierarchical Models
- Posterior-Based Decisions
- Tools and Tutorials — Posterior workflows in PyMC
- Summary

### Tutorials
- msml610/tutorials/L07_prob_programming/L07_01_bayesian_coin.ipynb
- msml610/tutorials/L07_prob_programming/L07_02_probabilistic_programming.ipynb
- msml610/tutorials/L07_prob_programming/L07_02_robust_modeling.ipynb
- msml610/tutorials/L07_prob_programming/L07_03_hierarchical_models.ipynb
- msml610/tutorials/L07_prob_programming/L07_04_generalized_linear_models.ipynb
- msml610/tutorials/L07_prob_programming/L07_05_evaluating_models.ipynb

### Related packages
- pyro (8,200): Probabilistic programming on PyTorch
- PyMC3 (7,900): Bayesian statistical modeling framework
- TensorFlow Probability (3,800): Probabilistic reasoning library
- Numpyro (3,200): Probabilistic programming with NumPy/JAX
- PyStan (2,400): Python interface to Stan
- CmdStanPy (1,300): Python interface to CmdStan

### Related books
- [B010] Imbens et al., "Causal Inference for Statistics, Social, and Biomedical
  Sciences", 2015
- [B011] Sutton, "Python Causal Analysis", 2024
- [B012] Burkov, "Machine Learning Engineering", 2020

# Part II: Estimating Causal Effects

## 5: Interventions, Experiments, and Adjustments

### Lessons
- `msml610/lectures_source/Lesson08.3-Do_Calculus.txt`


### Target TOC
- Interventions and Counterfactuals
- Randomized Controlled Trials
- Observational Adjustment
- Do-Calculus
- Tools and Tutorials — Using DoWhy for causal inference
- Summary

### Tutorials

### Related packages
- DoWhy (6,600): Causal inference using graphical models
- CausalImpact (5,600): Causal inference for intervention analysis
- CausalML (4,800): Uplift modeling and causal inference
- EconML (4,600): ML-based causal effect estimation

### Related books
- [B013] Rosenbaum, "Observation and Experiment", 2017
- [B014] Angrist et al., "Mostly Harmless Econometrics", 2008
- [B015] Gerber et al., "Field Experiments", 2012

## 6: Causal Identification and Estimation

### Lessons
- `msml610/lectures_source/Lesson08.4.txt`


### Target TOC
- The Identification Problem
- Classical Strategies (instrumental variables, RDD, DiD)
- Matching and Propensity Scores
- Modern Causal Forests
- Sensitivity to Unmeasured Confounding
- Case Study: Healthcare Treatment Effects
- Tools and Tutorials — EconML and CausalML
- Summary

### Tutorials
- msml610/tutorials/L08_causal_inference/L08_04_01_causal_inference.ipynb
- msml610/tutorials/L08_causal_inference/L08_04_02_causal_inference.ipynb
- msml610/tutorials/L08_causal_inference/L08_04_05_propensity_score.ipynb
- msml610/tutorials/L08_causal_inference/L08_04_07_metalearners.ipynb
- msml610/tutorials/L08_causal_inference/L08_04_08_difference_in_difference.ipynb

### Related packages
- DoWhy (6,600): Causal inference using graphical models
- CausalML (4,800): Uplift modeling and causal inference
- EconML (4,600): ML-based causal effect estimation
- causal-learn (3,200): Causal discovery and inference toolkit
- CausalPy (1,200): Causal effect estimation and visualization
- CausalInference (1,100): Statistical causal inference methods

### Related books
- [B016] Angrist et al., "Mastering 'Metrics", 2014
- [B017] Wooldridge, "Econometric Analysis of Cross Section and Panel Data", 2010
- [B018] Huntington-Klein, "The Effect", 2021

## 7: Explainability and Causal Attribution

### Lessons

### Target TOC
- Explanation vs. Causality
- Explanation Methods (SHAP, LIME)
- The Critical Gap: Feature Importance Is Not Causality
- Causal Attribution
- Decision Support
- Tools and Tutorials — SHAP, LIME, DiCE, and DoWhy
- Summary

### Tutorials

### Related packages
- DoWhy (6,600): Causal inference using graphical models
- CausalNex (3,000): Causal reasoning with Bayesian Networks
- CausalGraphicalModels (1,500): Toolkit for causal graphs in Python

### Related books
- [B019] Molnar, "Interpretable Machine Learning", 2022
- [B020] Kearns et al., "The Ethical Algorithm", 2019
- [B021] Kohavi et al., "Trustworthy Online Controlled Experiments", 2020

## 8: Causal Inference for Time Series

### Lessons
- `msml610/lectures_source/Lesson10-Timeseries_forecasting.txt`
- `msml610/lectures_source/Lesson10.1-Causal_Inference_for_Time_Series.txt`

### Target TOC
- Time Series vs. Cross-Sectional Causality
- Granger Causality
- Interrupted Time Series
- Difference-in-Differences
- Synthetic Control Methods
- Tools and Tutorials — CausalImpact and CausalPy
- Summary

### Tutorials
- `msml610/tutorials/L09_kalman_filter`

### Related packages
- TiMINo (3,600): Time-series causal discovery under independent noise
  assumptions
- orbit (2,000): Bayesian time series models
- HMMlearn (1,600): Hidden Markov Models with sklearn API
- BETS (350): Time-series causal network inference using elastic net regression

### Related books
- [B022] Hamilton, "Time Series Analysis", 1994
- [B023] Hyndman et al., "Forecasting: Principles and Practice", 2021
- [B024] Molak, "Causal Inference and Discovery in Python", 2023

## 9: A/B Testing and Experimentation

### Lessons
- `msml610/lectures_source/Lesson09.3-Multi_Armed_Bandits.txt`

### Target TOC
- Randomization as Causal Identification
- A/B Test Design
- Beyond Standard A/B Tests (switchbacks, multi-armed bandits)
- Sequential Decision-Making
- Tools and Tutorials — CausalML and CausalPy
- Summary

### Tutorials
- `msml610/tutorials/L09_multi_armed_bandits`

### Related packages
- Vowpal Wabbit (8,600): High-performance online learning with contextual bandit
  support
- contextualbandits (1,700): Python implementations of contextual bandit
  algorithms
- MABWiser (280): Contextual and non-contextual multi-armed bandit library
- PyXAB (200): Research-focused library for X-armed bandits

### Related books
- [B021] Kohavi et al., "Trustworthy Online Controlled Experiments", 2020
- [B025] Siroker et al., "A/B Testing", 2013
- [B026] Thomke, "Experimentation Works", 2020

## 10: Causal Discovery

### Lessons
- `msml610/lectures_source/Lesson10.2-Causal_Discovery.txt`

### Target TOC
- When Discovery Works and When It Doesn't
- Discovery vs. Domain Knowledge
- Discovery Algorithms (PC, FCI, GES, NOTEARS, LiNGAM)
- Validation and Refutation
- Tools and Tutorials — causal-learn and LiNGAM
- Summary

### Tutorials
- From
  - IN PROGRESS: tutorials/dowhy
  - causal-learn
  - CDT
  - LiNGAM

### Related packages
- causal-learn (3,200): Causal discovery and inference toolkit
- Causal Discovery Toolbox (3,100): Framework for discovering causal structure
  from observational data
- gCastle (2,400): Toolkit for causal structure learning and trustworthy AI
- bnlearn (1,900): Causal discovery with Bayesian networks
- LiNGAM (1,400): Discovery of linear non-Gaussian causal models
- Tetrad (1,100): Suite for causal model discovery and analysis

### Related books
- [B007] Pearl, "Causality", 2009
- [B008] Peters et al., "Elements of Causal Inference", 2017
- [B004] Koller et al., "Probabilistic Graphical Models", 2009
- [B027] Spirtes et al., "Causation, Prediction, and Search", 2000

### Related Papers
- [P012] Zanga et al., "A Survey on Causal Discovery: Theory and Practice", 2023
  https://arxiv.org/pdf/2305.10032
- [P013] Glymour et al., "Review of Causal Discovery Methods Based on Graphical
  Models", 2020 https://par.nsf.gov/servlets/purl/10125762
- [P014] Guo et al., "A survey on causal inference", 2015
  https://qiniu.pattern.swarma.org/attachment/A%20Survey%20on%20Causal%20Inference.pdf
- [P015] Meek, "Causal inference and causal explanation with background
  knowledge", 2006 https://arxiv.org/pdf/1302.4972
- [P016] Maathuis et al., "Estimating high-dimensional intervention effects from
  observational data", 2012
- [P017] Kalisch et al., "Causal inference using invariant prediction", 2010
- [P018] Zhang et al., "On the identifiability of the post-nonlinear causal
  model", 2009 https://arxiv.org/pdf/1205.2599
- [P019] Loh et al., "Causal discovery with identifiable nonlinear models", 2018
- [P020] Uhler et al., "Geometries of faithfulness in graphical models", 2017
  https://arxiv.org/abs/1608.00191
- [P021] Gamella et al., "Active learning of linear causal models", 2021
  https://arxiv.org/abs/2006.05690
- [P022] Wang et al., "RL-based structural equation modeling", 2019
- [P023] Mani et al., "Learning the structure of causal models with experimental
  and observational data", 2013
- [P024] Solus et al., "Causal discovery with unknown interventions", 2019
- [P025] Squires et al., "Active structure learning of causal DAGs", 2018
  https://arxiv.org/abs/2011.00641
- [P026] Sachs et al., "Causal protein-signaling networks derived from
  multiparameter single-cell data", 2015
- [P027] Castelo et al., "Structural, syntactic, and statistical issues in
  learning Bayesian networks from data", 2008
- [P028] Zheng et al., "DAGs with NO TEARS: Continuous Optimization for Structure
  Learning", 2018
  https://papers.nips.cc/paper/8157-dags-with-no-tears-continuous-optimization-for-structure-learning.pdf
