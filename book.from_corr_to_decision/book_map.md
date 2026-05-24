## Part I: Understanding Causality

### 1: From Prediction Pipelines to Decision Pipelines
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

### 2: Bayesian Networks
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

### 3: Causal DAGs and Structural Models
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

### 4: From Causal Models to Code

**Lessons**
- msml610/lectures_source/Lesson07.1-Intro_to_Probabilistic_Programming.txt
- msml610/lectures_source/Lesson07.2-Posterior_Based_Decisions.txt
- msml610/lectures_source/Lesson07.3-Hierarchical_Models.txt
- msml610/lectures_source/Lesson07.4-Generalized_Linear_Models.txt
- msml610/lectures_source/Lesson07.5-Bayesian_Model_Comparison.txt

**Tutorials**
- msml610/tutorials/L07_prob_programming/L07_01_bayesian_coin.ipynb
- msml610/tutorials/L07_prob_programming/L07_02_probabilistic_programming.ipynb
- msml610/tutorials/L07_prob_programming/L07_02_robust_modeling.ipynb
- msml610/tutorials/L07_prob_programming/L07_03_hierarchical_models.ipynb
- msml610/tutorials/L07_prob_programming/L07_04_generalized_linear_models.ipynb
- msml610/tutorials/L07_prob_programming/L07_05_evaluating_models.ipynb

**Related packages**
- pyro (8,200): Probabilistic programming on PyTorch
- PyMC3 (7,900): Bayesian statistical modeling framework
- TensorFlow Probability (3,800): Probabilistic reasoning library
- Numpyro (3,200): Probabilistic programming with NumPy/JAX
- PyStan (2,400): Python interface to Stan
- CmdStanPy (1,300): Python interface to CmdStan

**Related books**
- [B010] Imbens et al., "Causal Inference for Statistics, Social, and Biomedical Sciences", 2015
- [B011] Sutton, "Python Causal Analysis", 2024
- [B012] Burkov, "Machine Learning Engineering", 2020

## Part II: Estimating Causal Effects

### 5: Interventions, Experiments, and Adjustments
**Lessons**
- msml610/lectures_source/Lesson08.3-Do_Calculus.txt

**Tutorials**

**Related packages**
- DoWhy (6,600): Causal inference using graphical models
- CausalImpact (5,600): Causal inference for intervention analysis
- CausalML (4,800): Uplift modeling and causal inference
- EconML (4,600): ML-based causal effect estimation

**Related books**
- [B013] Rosenbaum, "Observation and Experiment", 2017
- [B014] Angrist et al., "Mostly Harmless Econometrics", 2008
- [B015] Gerber et al., "Field Experiments", 2012

### 6: Causal Identification and Estimation

**Lessons**
- msml610/lectures_source/Lesson08.4.txt

**Tutorials**
- msml610/tutorials/L08_causal_inference/L08_04_01_causal_inference.ipynb
- msml610/tutorials/L08_causal_inference/L08_04_02_causal_inference.ipynb
- msml610/tutorials/L08_causal_inference/L08_04_05_propensity_score.ipynb
- msml610/tutorials/L08_causal_inference/L08_04_07_metalearners.ipynb
- msml610/tutorials/L08_causal_inference/L08_04_08_difference_in_difference.ipynb

**Related packages**
- DoWhy (6,600): Causal inference using graphical models
- CausalML (4,800): Uplift modeling and causal inference
- EconML (4,600): ML-based causal effect estimation
- causal-learn (3,200): Causal discovery and inference toolkit
- CausalPy (1,200): Causal effect estimation and visualization
- CausalInference (1,100): Statistical causal inference methods

**Related books**
- [B016] Angrist et al., "Mastering 'Metrics", 2014
- [B017] Wooldridge, "Econometric Analysis of Cross Section and Panel Data", 2010
- [B018] Huntington-Klein, "The Effect", 2021

### 7: Explainability and Causal Attribution
**Lessons**
- ?

**Tutorials**

**Related packages**
- DoWhy (6,600): Causal inference using graphical models
- CausalNex (3,000): Causal reasoning with Bayesian Networks
- CausalGraphicalModels (1,500): Toolkit for causal graphs in Python

**Related books**
- [B019] Molnar, "Interpretable Machine Learning", 2022
- [B020] Kearns et al., "The Ethical Algorithm", 2019
- [B021] Kohavi et al., "Trustworthy Online Controlled Experiments", 2020

### 8: Causal Inference for Time Series
**Lessons**
- msml610/lectures_source/Lesson10-Timeseries_forecasting.txt
- msml610/lectures_source/Lesson10.1-Causal_Inference_for_Time_Series.txt

**Tutorials**
- msml610/tutorials/L09_kalman_filter

**Related packages**
- TiMINo (3,600): Time-series causal discovery under independent noise assumptions
- orbit (2,000): Bayesian time series models
- HMMlearn (1,600): Hidden Markov Models with sklearn API
- BETS (350): Time-series causal network inference using elastic net regression

**Related books**
- [B022] Hamilton, "Time Series Analysis", 1994
- [B023] Hyndman et al., "Forecasting: Principles and Practice", 2021
- [B024] Molak, "Causal Inference and Discovery in Python", 2023

### 9: A/B Testing and Experimentation

**Lessons**
- msml610/lectures_source/Lesson09.3-Multi_Armed_Bandits.txt

**Tutorials**
- msml610/tutorials/L09_multi_armed_bandits

**Related packages**
- Vowpal Wabbit (8,600): High-performance online learning with contextual bandit support
- contextualbandits (1,700): Python implementations of contextual bandit algorithms
- MABWiser (280): Contextual and non-contextual multi-armed bandit library
- PyXAB (200): Research-focused library for X-armed bandits

**Related books**
- [B021] Kohavi et al., "Trustworthy Online Controlled Experiments", 2020
- [B025] Siroker et al., "A/B Testing", 2013
- [B026] Thomke, "Experimentation Works", 2020

### 10: Causal Discovery
**Lessons**
- msml610/lectures_source/Lesson10.2-Causal_Discovery.txt

**Tutorials**
- pywhy
- causal-learn
- CDT
- LiNGAM

**Related packages**
- causal-learn (3,200): Causal discovery and inference toolkit
- Causal Discovery Toolbox (3,100): Framework for discovering causal structure from observational data
- gCastle (2,400): Toolkit for causal structure learning and trustworthy AI
- bnlearn (1,900): Causal discovery with Bayesian networks
- LiNGAM (1,400): Discovery of linear non-Gaussian causal models
- Tetrad (1,100): Suite for causal model discovery and analysis

**Related books**
- [B008] Peters et al., "Elements of Causal Inference", 2017
- [B004] Koller et al., "Probabilistic Graphical Models", 2009
- [B027] Spirtes et al., "Causation, Prediction, and Search", 2000

## Part III: Making Decisions with Causality

### 11: Decision-Making with Causal Models
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

### 12: Causal Reinforcement Learning
**Lessons**
- msml610/lectures_source/Lesson12-Reinforcement_learning.txt

**Tutorials**

**Related packages**
- contextualbandits (1,700): Python implementations of contextual bandit algorithms
- MABWiser (280): Multi-armed bandit library with sklearn-style API
- PyXAB (200): Research-focused library for X-armed bandits and online optimization

**Related books**
- [B030] Sutton et al., "Reinforcement Learning: An Introduction", 2018
- [B031] Szepesvári, "Algorithms for Reinforcement Learning", 2010
- [B032] Ness et al., "Causal AI", 2023

### 13: Forecasting Under Causal Intervention
**Lessons**

**Tutorials**

**Related packages**
- TiMINo (3,600): Time-series causal discovery under independent noise assumptions
- orbit (2,000): Bayesian time series models
- HMMlearn (1,600): Hidden Markov Models with sklearn API
- BETS (350): Time-series causal network inference using elastic net regression

**Related books**
- [B023] Hyndman et al., "Forecasting: Principles and Practice", 2021
- [B033] Hanke et al., "Business Forecasting", 2009
- [B022] Hamilton, "Time Series Analysis", 1994

### 14: Causal Decision Making in Practice
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

### 15: Causal Reasoning in AI Systems
**Lessons**
- msml610/lectures_source/Lesson15.1-Causal_Reasoning_Agents

**Tutorials**

**Related packages**
- DoWhy (6,600): Causal inference using graphical models
- PyWhy (2,400): Python ecosystem for causal inference
- Causica (2,000): Microsoft tool combining causal discovery and inference with deep learning
- ALICE (1,000): ML and econometrics integration

**Related books**
- [B036] Christian, "The Alignment Problem", 2020
- [B037] Russell, "Human Compatible", 2019
- [B038] Schölkopf et al., "Causal Artificial Intelligence", 2021
