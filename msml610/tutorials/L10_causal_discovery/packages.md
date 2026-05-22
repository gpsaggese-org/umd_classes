# Functionality Clusters

| Cluster | Function | Packages Ordered by Stars |
|---|---|---|
| **1. Causal Discovery / Structure Learning** | Learn causal graphs and discover causal structure from observational or temporal data | causal-learn (3,200), Causal Discovery Toolbox (3,100), gCastle (2,400), Causica (2,000), bnlearn (1,900), LiNGAM (1,400), Tetrad (1,100), ALICE (1,000), BETS (350) |
| **2. Causal Inference / Treatment Effect Estimation** | Estimate causal effects, interventions, counterfactuals, and uplift | DoWhy (6,600), CausalImpact (5,600), CausalML (4,800), EconML (4,600), PyWhy (2,400), IBM Causal Inference 360 (1,700), Azua (1,400), CausalPy (1,200), CausalInference (1,100) |
| **3. Causal Graphs / DAG Modeling / Identification** | Build, manipulate, visualize, and analyze DAGs and causal graphs | CausalGraphicalModels (1,500), Dagitty (1,500), Geminos (500) |
| **4. Bayesian Networks & Probabilistic Graphical Models** | Bayesian networks, graphical model inference, probabilistic reasoning | pgmpy (5,000), Pomegranate (3,600), CausalNex (3,000) |
| **5. Probabilistic Programming / Bayesian Statistical Modeling** | General-purpose Bayesian inference and probabilistic programming frameworks | pyro (8,200), PyMC3 (7,900), TensorFlow Probability (3,800), Numpyro (3,200), PyStan (2,400), CmdStanPy (1,300) |
| **6. Bandits / Online Learning / Reinforcement Learning** | Contextual bandits, multi-armed bandits, online learning, reinforcement learning | Vowpal Wabbit (8,600), contextualbandits (1,700), MABWiser (280), PyXAB (200) |
| **7. Bayesian Optimization / Sequential Optimization** | Bayesian optimization and sequential black-box optimization | BoTorch (3,300), scikit-optimize (2,800) |
| **8. Time-Series / Temporal Probabilistic Modeling** | Time-series forecasting, temporal latent-state models, hidden Markov models | TiMINo (3,600), orbit (2,000), HMMlearn (1,600) |

# Packages

## causal-learn
- Description: Causal Discovery in Python. Learning causality from data
- GitHub URL: https://github.com/py-why/causal-learn
- Stars (as of May 2026): 1.6k

### Features
- Implements constraint-based causal discovery algorithms such as PC and FCI
- Supports score-based methods including GES for structure learning
- Includes time-series causal discovery capabilities
- Provides conditional independence tests for continuous and discrete data
- Integrates graph visualization and causal graph manipulation utilities

### Alternatives
- Causal Discovery Toolbox: https://github.com/FenTechSolutions/CausalDiscoveryToolbox
- gCastle: https://github.com/huawei-noah/trustworthyAI
- Tetrad: https://github.com/cmu-phil/tetrad
- LiNGAM: https://github.com/cdt15/lingam
- bnlearn: https://github.com/erdogant/bnlearn

## dowhy
- Description: DoWhy is a Python library for causal inference that supports
  explicit modeling and testing of causal assumptions
- GitHub URL: https://github.com/py-why/dowhy
- Stars (as of May 2026): 8.1k

### Features
- Models causal assumptions explicitly using causal graphs
- Estimates treatment effects with multiple inference backends
- Performs robustness checks and refutation tests on causal estimates
- Integrates with EconML and other machine learning libraries
- Supports mediation analysis and counterfactual reasoning workflows

### Alternatives
- CausalML: https://github.com/uber/causalml
- IBM Causal Inference 360: https://github.com/IBM/causallib
- CausalInference: https://github.com/laurencium/CausalInference
- CausalPy: https://github.com/pymc-labs/CausalPy
- CausalImpact: https://github.com/google/CausalImpact

## pywhy-graphs
- Description: [Experimental] Causal graphs that are networkx-compliant for the
  py-why ecosystem
- GitHub URL: https://github.com/py-why/pywhy-graphs
- Stars (as of May 2026): 65

### Features
- Provides graph data structures specialized for causal analysis
- Extends NetworkX compatibility for mixed-edge causal graphs
- Supports directed, bidirected, and partially directed graph types
- Enables graph transformations used in causal identification algorithms
- Integrates with other PyWhy ecosystem libraries

### Alternatives
- CausalGraphicalModels: https://github.com/ijmbarr/causalgraphicalmodels
- Dagitty: https://github.com/jtextor/dagitty
- pgmpy: https://github.com/pgmpy/pgmpy
- CausalNex: https://github.com/quantumblacklabs/causalnex

## dodiscover
- Description: [Experimental] Global causal discovery algorithms
- GitHub URL: https://github.com/py-why/dodiscover
- Stars (as of May 2026): 112

### Features
- Implements scalable causal discovery pipelines
- Supports both observational and interventional data settings
- Provides modular APIs for plugging in custom discovery algorithms
- Includes utilities for graph orientation and edge pruning
- Integrates with pywhy-graphs and causal-learn

### Alternatives
- Causal Discovery Toolbox —
  https://github.com/FenTechSolutions/CausalDiscoveryToolbox
- gCastle: https://github.com/huawei-noah/trustworthyAI
- causal-learn: https://github.com/py-why/causal-learn
- Tetrad: https://github.com/cmu-phil/tetrad
- TiMINo: https://github.com/jakobrunge/tigramite

## EconML
- Description: ALICE (Automated Learning and Intelligence for Causation and
  Economics) is a Microsoft Research project aimed at applying AI concepts to
  economics and causal inference
- GitHub URL: https://github.com/py-why/EconML
- Stars (as of May 2026): 4.6k

### Features
- Estimates heterogeneous treatment effects using machine learning
- Implements Double Machine Learning (DML) estimators
- Supports causal forests and meta-learners for uplift modeling
- Integrates with scikit-learn pipelines and estimators
- Provides inference tools for confidence intervals and uncertainty estimation

### Alternatives
- CausalML: https://github.com/uber/causalml
- DoWhy: https://github.com/py-why/dowhy
- IBM Causal Inference 360: https://github.com/IBM/causallib
- Causica: https://github.com/microsoft/causica
- Azua: https://github.com/causalens/azua

## graphs
- Description: [Not used] Now, an open PR for mixed-edge graph support is open in
  networkx
- GitHub URL: https://github.com/py-why/graphs
- Stars (as of May 2026): 2

### Features
- Explores experimental mixed-edge graph representations
- Provides prototype graph APIs for causal modeling
- Tests interoperability with NetworkX graph structures
- Serves as a sandbox for graph-related experimentation

### Alternatives
- pywhy-graphs: https://github.com/py-why/pywhy-graphs
- CausalGraphicalModels: https://github.com/ijmbarr/causalgraphicalmodels
- pgmpy: https://github.com/pgmpy/pgmpy

## pywhyllm
- Description: Experimental library integrating LLM capabilities to support
  causal analyses
- GitHub URL: https://github.com/py-why/pywhyllm
- Stars (as of May 2026): 304

### Features
- Uses large language models to assist causal reasoning workflows
- Generates natural-language explanations for causal analyses
- Helps automate causal graph construction from text
- Supports interactive causal analysis assistants
- Integrates LLM-driven summarization and interpretation tools

### Alternatives
- Geminos: https://github.com/causeinfer/geminos
- Azua: https://github.com/causalens/azua
- Causica: https://github.com/microsoft/causica

## pywhy-stats
- Description: Python package for (conditional) independence testing and
  statistical functions related to causality
- GitHub URL: https://github.com/py-why/pywhy-stats
- Stars (as of May 2026): 32

### Features
- Implements conditional independence tests for causal discovery
- Supports statistical testing for continuous and categorical variables
- Provides reusable statistical utilities for causal pipelines
- Includes permutation-based and kernel-based testing methods
- Integrates with causal-learn and other PyWhy tools

### Alternatives
- bnlearn: https://github.com/erdogant/bnlearn
- pgmpy: https://github.com/pgmpy/pgmpy
- Pomegranate: https://github.com/jmschrei/pomegranate
- TensorFlow Probability: https://github.com/tensorflow/probability

## causaltune
- Description: AutoML for causal inference
- GitHub URL: https://github.com/py-why/causaltune
- Stars (as of May 2026): 241

### Features
- Automates model selection for causal inference tasks
- Tunes hyperparameters for treatment effect estimation models
- Benchmarks multiple causal estimators automatically
- Supports uplift modeling and heterogeneous treatment effect analysis
- Integrates with popular machine learning frameworks and estimators

### Alternatives
- CausalML: https://github.com/uber/causalml
- EconML: https://github.com/microsoft/EconML
- scikit-optimize: https://github.com/scikit-optimize/scikit-optimize
- BoTorch: https://github.com/pytorch/botorch
