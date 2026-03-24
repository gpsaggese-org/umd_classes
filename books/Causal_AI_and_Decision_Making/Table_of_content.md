# Beyond Prediction: Causal AI, Explainability, and Decision Intelligence for Machine Learning Practitioners

## Table of Contents

## Part I — From Prediction to Decision Intelligence
1. **Introduction: The Limits of Prediction**
   - Prediction vs. reasoning vs. decision-making: a three-way distinction
   - Why correlation is not enough
   - From ML models to reasoning systems to decision systems
   - Overview of causal AI, automatic reasoning, and explainability
   - TUTORIAL: DoWhy (end-to-end causal reasoning from observational data)

2. **Data Science vs. Decision Science**
   - Predictive modeling pipelines
   - Decision pipelines
   - Optimization vs. inference
   - Feedback loops in ML systems
   - TUTORIAL: pgmpy (Bayesian decision networks and decision pipeline modeling)

3. **Uncertainty in Machine Learning**
   - Aleatoric vs. epistemic uncertainty
   - Confidence intervals and prediction intervals
   - Bayesian thinking for ML practitioners
   - Risk-aware decision-making
   - TUTORIAL: PyMC (Bayesian statistical modeling and uncertainty quantification)

4. **The Causal AI Practitioner's Toolkit**
   - The library landscape: causal inference, explainability, decision optimization
   - Mapping tools to questions: identification vs. estimation vs. discovery
   - End-to-end causal AI workflow overview
   - When correlation-based tools fail and causal tools are needed
   - TUTORIAL: DoWhy + EconML (integrated causal AI workflow from data to decision)

## Part II — Foundations of Causal Inference
5. **Causality vs. Correlation**
   - Spurious correlations
   - Simpson's paradox
   - Confounding variables
   - Causal questions vs. predictive questions
   - TUTORIAL: DoWhy (illustrating the difference between correlation and causal effect)
   - TUTORIAL: CausalImpact (detecting causal impact of interventions vs. spurious trends)

6. **Structural Causal Models**
   - Causal graphs (DAGs) as a reasoning formalism
   - Structural equations
   - Interventions and the do-operator
   - The do-calculus: rules for interventional reasoning
   - d-separation and conditional independence
   - Automated reasoning over causal graphs: identification algorithms
   - TUTORIAL: pgmpy (building and querying Bayesian networks and DAGs)
   - TUTORIAL: CausalGraphicalModels (defining and visualizing structural causal models)
   - TUTORIAL: Dagitty (DAG creation and causal effect identification)

7. **Counterfactual Reasoning**
   - What is a counterfactual
   - Counterfactuals vs. interventions: the three rungs of the ladder of causation
   - Potential outcomes framework (Rubin causal model)
   - Computing counterfactuals from structural causal models
   - Counterfactual explanations for ML predictions and algorithmic recourse
   - Applications: what would have happened without the treatment?
   - TUTORIAL: DoWhy (counterfactual queries in structural causal models)
   - TUTORIAL: DiCE (diverse counterfactual explanations for ML models)

8. **Causal Identification**
   - Backdoor criterion
   - Frontdoor criterion
   - Instrumental variables
   - Selection bias
   - TUTORIAL: DoWhy (applying backdoor/frontdoor criteria for causal identification)
   - TUTORIAL: IBM Causal Inference 360 (identification strategies and sensitivity analysis)

9. **Estimating Causal Effects**
   - Average treatment effect (ATE)
   - Matching methods
   - Propensity scores
   - Regression adjustment
   - Doubly robust methods
   - Application: healthcare observational studies and treatment effect estimation
   - TUTORIAL: EconML (double ML, causal forests, and meta-learners for ATE estimation)
   - TUTORIAL: CausalML (propensity scoring, matching, and uplift estimation)
   - TUTORIAL: CausalInference (regression adjustment and doubly robust methods)
   - TUTORIAL: IBM Causal Inference 360 (causal inference toolkit for health outcomes)

10. **Sensitivity Analysis and Robustness**
    - Why causal estimates can be fragile
    - Unmeasured confounding and its consequences
    - Rosenbaum bounds
    - E-values for unmeasured confounding
    - Placebo tests and falsification
    - Refutation methods: random common cause, data subset, placebo treatment
    - TUTORIAL: DoWhy (built-in refutation tests and sensitivity analysis)
    - TUTORIAL: IBM Causal Inference 360 (sensitivity analysis for observational studies)

11. **Causal Inference in Practice**
    - A/B testing and experimentation
    - Uplift modeling
    - Policy evaluation
    - Observational vs experimental data
    - Application: marketing uplift, targeted customer interventions, and campaign analysis
    - TUTORIAL: CausalML (uplift modeling and A/B test analysis)
    - TUTORIAL: CausalPy (causal effect estimation with Bayesian models)
    - TUTORIAL: CausalImpact (policy evaluation using interrupted time-series analysis)
    - TUTORIAL: EconML (heterogeneous treatment effects for targeted marketing)

12. **Causal Inference for Time Series**
    - Time series vs. cross-sectional causal inference
    - Granger causality: definition, assumptions, and limitations
    - Interrupted time series (ITS) and regression discontinuity
    - Difference-in-differences (DiD) and parallel trends assumption
    - Synthetic control: constructing a counterfactual from donor series
    - When temporal structure helps and when it misleads
    - TUTORIAL: CausalImpact (Bayesian interrupted time series for causal inference)
    - TUTORIAL: statsmodels (Granger causality tests and VAR models)
    - TUTORIAL: CausalPy (DiD and synthetic control with Bayesian models)

## Part III — Causal AI
13. **What is Causal AI**
    - Predictive AI vs Causal AI
    - Decision intelligence systems
    - Causal reasoning systems
    - TUTORIAL: DoWhy (causal reasoning pipeline vs. predictive pipeline)
    - TUTORIAL: EconML (causal AI for business decision systems)

14. **Causal Discovery**
    - Constraint-based methods
    - Score-based methods
    - Granger causality and state space representations
    - Practical limitations
    - TUTORIAL: causal-learn (PC algorithm, GES, and constraint-based discovery)
    - TUTORIAL: LiNGAM (linear non-Gaussian causal model discovery)
    - TUTORIAL: bnlearn (Bayesian network structure learning)
    - TUTORIAL: gCastle (Huawei toolkit for causal structure learning)
    - TUTORIAL: Tetrad (suite for causal model discovery and analysis)
    - TUTORIAL: Causal Discovery Toolbox (framework for causal structure discovery)

15. **Causal Machine Learning**
    - Double machine learning
    - Causal forests
    - Meta-learners (S-learner, T-learner, X-learner)
    - Heterogeneous treatment effects
    - TUTORIAL: EconML (double ML, causal forests, S/T/X-learners, HTE estimation)
    - TUTORIAL: CausalML (meta-learners and heterogeneous treatment effect estimation)

16. **Causal Representation Learning**
    - Learning causal structure
    - Invariant risk minimization
    - Domain adaptation and causality
    - Distribution shifts
    - TUTORIAL: Causica (combining causal discovery and inference with deep learning)
    - TUTORIAL: CausalNex (causal representation with Bayesian Networks)

17. **Neuro-Symbolic Causal Reasoning**
    - Symbolic reasoning: logic, rules, and knowledge bases
    - Neural reasoning: learning from data
    - Combining neural and symbolic: neuro-symbolic AI
    - Causal structure as symbolic knowledge + neural estimation
    - Knowledge graphs and causal ontologies
    - Probabilistic logic and soft constraints
    - TUTORIAL: DeepProbLog (probabilistic logic programming with neural predicates)
    - TUTORIAL: PyReason (neuro-symbolic reasoning with temporal logic)
    - TUTORIAL: CausalNex (knowledge graph reasoning with Bayesian Networks)

18. **From Prediction Systems to Decision Systems**
    - Recommendation systems
    - Pricing systems
    - Marketing interventions
    - Healthcare decision systems
    - Application: causal recommendation systems beyond collaborative filtering
    - Application: causal pricing and revenue optimization
    - TUTORIAL: CausalML (causal intervention modeling for business systems)
    - TUTORIAL: EconML (policy-based decision and pricing optimization)
    - TUTORIAL: DoWhy (causal recommendation systems and end-to-end decision pipelines)
    - TUTORIAL: optuna (pricing strategy optimization with Bayesian search)

## Part IV — Machine Learning Explainability
19. **Explainability vs Causality**
    - Feature importance is not causality
    - When explanations are misleading
    - Causal feature importance
    - Interventions vs attribution
    - Why explainability methods must be interpreted through a causal lens
    - TUTORIAL: DoWhy (contrasting causal effect with feature importance)
    - TUTORIAL: EconML (causal feature importance vs. predictive importance)
    - TUTORIAL: SHAP (showing limitations when correlations mislead attribution)

20. **Why Explainability Matters**
    - Black box models
    - Regulation and trust
    - Debugging ML models
    - Explainability vs interpretability
    - Application: fraud detection, risk scoring, and fairness-aware models
    - TUTORIAL: SHAP (explaining black-box model predictions with Shapley values)
    - TUTORIAL: AI Fairness 360 (bias detection and regulation-driven fairness auditing)
    - TUTORIAL: Fairlearn (fairness-aware risk models)
    - TUTORIAL: pysyft (privacy-preserving ML for sensitive risk data)

21. **Model-Specific Interpretability**
    - Linear models
    - Decision trees
    - Rule-based models
    - Generalized additive models (GAMs)
    - TUTORIAL: What-If Tool (interactive model interpretability and comparison)
    - TUTORIAL: SHAP (feature attribution for linear models and tree-based models)

22. **Model-Agnostic Explainability**
    - Feature importance
    - Partial dependence plots
    - ICE plots
    - Global vs local explanations
    - TUTORIAL: SHAP (global and local model-agnostic explanations)
    - TUTORIAL: LIME (local interpretable model-agnostic explanations)

23. **SHAP, LIME, and Modern Explanation Methods**
    - Shapley values
    - LIME explanations
    - Counterfactual explanations
    - Limitations of explainability methods
    - TUTORIAL: SHAP (Shapley values for model explanation)
    - TUTORIAL: LIME (local surrogate model explanations)
    - TUTORIAL: Fairlearn (fairness metrics and counterfactual fairness)

24. **Causal Fairness**
    - Limitations of statistical fairness (demographic parity, equalized odds)
    - Causal definitions of fairness
    - Path-specific effects and direct vs. indirect discrimination
    - Counterfactual fairness
    - Interventional fairness
    - Applications: credit scoring, hiring, criminal justice
    - TUTORIAL: AI Fairness 360 (causal fairness metrics and auditing)
    - TUTORIAL: Fairlearn (fairness-aware model training with causal constraints)
    - TUTORIAL: DoWhy (counterfactual fairness analysis)

## Part V — Decision-Making Under Uncertainty
25. **Decision Theory for Data Scientists**
    - Utility theory
    - Loss functions vs utility
    - Expected value and expected utility
    - Risk preferences
    - TUTORIAL: optuna (hyperparameter optimization as a decision problem)
    - TUTORIAL: Ax (adaptive experimentation and expected utility maximization)

26. **Bayesian Decision Making**
    - Bayesian inference
    - Posterior distributions
    - Thompson sampling
    - Bayesian optimization
    - TUTORIAL: PyMC (Bayesian inference and posterior-based decisions)
    - TUTORIAL: Numpyro (probabilistic programming for Bayesian decision making)
    - TUTORIAL: BoTorch (Bayesian optimization for sequential decision making)
    - TUTORIAL: pyro (probabilistic programming with PyTorch)

27. **Time Series Forecasting and Uncertainty**
    - Time series decomposition: trend, seasonality, residuals
    - Classical models: ARIMA, SARIMA, exponential smoothing
    - Machine learning models: XGBoost, LightGBM on time features
    - Deep learning models: N-BEATS, TFT, PatchTST
    - Probabilistic forecasting and prediction intervals
    - Conformal prediction for time series
    - Evaluating forecasts: MASE, CRPS, calibration
    - Application: supply chain demand forecasting and forecast-driven decisions
    - Demand forecasting pipelines: from data to decisions
    - Hierarchical forecasting across SKUs, regions, and time horizons
    - Reconciliation methods: bottom-up, top-down, optimal reconciliation
    - Anomaly detection in supply chain signals
    - Connecting forecasts to inventory, staffing, and procurement decisions
    - Newsvendor model and service-level optimization
    - Causal factors in demand: promotions, price, weather, events
    - Measuring forecast value in downstream decisions
    - TUTORIAL: Darts (unified forecasting with classical, ML, and deep learning models)
    - TUTORIAL: sktime (time series ML framework for forecasting and classification)
    - TUTORIAL: NeuralForecast (deep learning models for probabilistic time series)
    - TUTORIAL: GluonTS (probabilistic demand forecasting)
    - TUTORIAL: orbit (Bayesian time series models for supply chain planning)
    - TUTORIAL: CausalImpact (measuring the causal effect of promotions on demand)

28. **Sequential State Estimation and Filtering**
    - Hidden state and the state space model
    - Discrete Bayes filter (the foundation of all filtering)
    - Hidden Markov Models and the forward algorithm
    - Kalman filter: linear-Gaussian exact Bayesian inference
    - Discretizing continuous systems (matrix exponential, Van Loan method)
    - Extended and Unscented Kalman filters for nonlinear systems
    - Particle filters for non-Gaussian and nonlinear systems
    - Applications: tracking, sensor fusion, demand estimation
    - TUTORIAL: pykalman (linear Kalman filter and Kalman smoother)
    - TUTORIAL: HMMlearn (discrete filtering with Gaussian and multinomial HMMs)

29. **Reinforcement Learning and Sequential Decisions**
    - Markov decision processes
    - Partially observable MDPs (POMDPs) and belief states
    - Exploration vs exploitation
    - Policy learning
    - Offline reinforcement learning
    - TUTORIAL: gymnasium (standard RL environments for MDP experimentation)
    - TUTORIAL: Stable Baselines3 (reliable RL algorithm implementations)
    - TUTORIAL: ray[rllib] (scalable reinforcement learning)
    - TUTORIAL: d3rlpy (offline reinforcement learning algorithms)

30. **Causal Decision Making**
    - Policy interventions
    - Counterfactual reasoning
    - Decision optimization with causal models
    - Uplift and treatment policies
    - TUTORIAL: DoWhy (counterfactual reasoning and policy evaluation)
    - TUTORIAL: EconML (treatment policy optimization and uplift)
    - TUTORIAL: CausalML (causal policy learning and uplift modeling)

## Part VI — AI Coding, Agents, and Automation
31. **AI-Assisted Programming**
    - Code generation with LLMs
    - Prompt engineering for coding
    - Code review and debugging with AI
    - Testing with AI
    - TUTORIAL: llm (minimal library for working with LLMs for coding tasks)
    - TUTORIAL: HuggingFace (transformer models for code generation and review)

32. **LLM Reasoning Techniques**
    - Why LLMs struggle with reasoning and how to fix it
    - Chain-of-thought (CoT): step-by-step reasoning prompting
    - Tree-of-thought (ToT): branching and backtracking over reasoning paths
    - Self-consistency: sampling multiple reasoning chains and voting
    - Reflection and self-correction: Reflexion and iterative refinement
    - Tool-augmented reasoning: calculators, code, search, knowledge bases
    - Connecting LLM reasoning to causal and probabilistic reasoning
    - TUTORIAL: LangChain (CoT and tool-augmented reasoning pipelines)
    - TUTORIAL: Reflexion (self-reflective LLM reasoning with iterative improvement)
    - TUTORIAL: LlamaIndex (knowledge-grounded reasoning over structured data)

33. **Building Data Science Agents**
    - Agent architectures
    - Tool use and function calling
    - Autonomous data analysis agents
    - Multi-agent systems
    - TUTORIAL: LlamaIndex (LLM-powered data retrieval and analysis agents)
    - TUTORIAL: Langchain and Neo4j (LLM agent with graph-based knowledge)
    - TUTORIAL: ReAct (reasoning and acting framework for LLM agents)
    - TUTORIAL: Griptape (framework for building AI-powered applications)
    - TUTORIAL: AutoGPT (autonomous GPT-based agent for task planning)

34. **Automating Machine Learning Workflows**
    - AutoML
    - Feature engineering agents
    - Experimentation agents
    - Monitoring agents
    - TUTORIAL: FLAML (fast and lightweight AutoML)
    - TUTORIAL: AutoGluon (AutoML for tabular, text, and image data)
    - TUTORIAL: TPOT (AutoML using genetic programming)
    - TUTORIAL: optuna (automated hyperparameter optimization)
    - TUTORIAL: Featuretools (automated feature engineering)

35. **Decision-Making Agents**
    - Planning agents
    - Simulation environments
    - Decision optimization agents
    - Human-in-the-loop systems
    - TUTORIAL: ReAct (planning agents with reasoning and acting)
    - TUTORIAL: Reflexion (self-reflective agent framework for improved reasoning)
    - TUTORIAL: Griptape (decision optimization agent pipelines)
    - TUTORIAL: gymnasium (simulation environments for agent decision making)

36. **Causal AI Agents**
    - Agents that reason with causal models
    - Counterfactual reasoning agents
    - Experiment design agents
    - Policy optimization agents
    - TUTORIAL: DoWhy (building agents that reason with causal graphs)
    - TUTORIAL: Causica (deep learning agents with causal discovery and inference)
    - TUTORIAL: EconML (policy optimization agents with causal models)
    - TUTORIAL: Reflexion (counterfactual reasoning via self-reflection in agents)

37. **Automated Scientific Reasoning**
    - Hypothesis generation and testing with AI
    - Experiment design agents: active learning and causal exploration
    - LLM-guided causal discovery: from text to causal graphs
    - Automated statistical reasoning: from data to conclusions
    - Human-AI collaboration in scientific discovery
    - Open problems: grounding, verification, and trust
    - TUTORIAL: DoWhy (LLM-assisted causal graph construction and querying)
    - TUTORIAL: causal-learn (automated causal structure search as reasoning)
    - TUTORIAL: Reflexion (iterative hypothesis refinement via self-reflection)

## Conclusion
38. **Toward Causal Intelligence: Synthesis and the Road Ahead**
    - Prediction, causation, and decision-making as a unified framework
    - The causal AI stack: from raw data to decisions
    - Connecting the threads: SCMs, explainability, and decision optimization
    - Open problems: causal discovery at scale, causal LLMs, real-time causal systems
    - Practical starting points for ML practitioners
    - The shift from correlational to causal AI in industry

## Appendix
- Mathematical foundations of causal inference
- Bayesian statistics refresher
- Optimization methods
- Reinforcement learning math
- Time series math: stationarity, spectral analysis, state space representations
- Python libraries for causal ML and explainability
- Further reading and research papers
