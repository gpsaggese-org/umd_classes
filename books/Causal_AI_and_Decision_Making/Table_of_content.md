# Beyond Prediction: Causal AI, Explainability, and Decision Intelligence for Machine Learning Practitioners

## Part I — The Practitioner's Case for Causal AI

### 1: The Limits of Prediction
[Slides: Lesson08.1-Causal_AI_intro](https://github.com/gpsaggese/gpsaggese.github.io/tree/master/msml610/lectures/Lesson08.1-Causal_AI_intro.pdf)

- What ML systems can and cannot tell you
- Correlation, association, and the illusion of understanding
- Three kinds of questions: association, intervention, counterfactual (Pearl's ladder)
- A roadmap: from prediction to causal reasoning to decision intelligence
- TUTORIAL: DoWhy (end-to-end causal reasoning from observational data)

### 2: From Prediction Pipelines to Decision Pipelines
[Slides: Lesson02.2-ML_Paradigms](https://github.com/gpsaggese/gpsaggese.github.io/tree/master/msml610/lectures/Lesson02.2-ML_Paradigms.pdf)

- How production ML systems make decisions today
- Feedback loops and distribution shift
- Optimization vs. inference vs. decision theory
- The cost of ignoring causality: concrete failure modes
- Data Science vs. Decision Science
- TUTORIAL: pgmpy (Bayesian decision networks and decision pipeline modeling)

## Part II — Foundations of Causal Inference

### 3: Causality vs. Correlation
[Slides: Lesson08.1-Causal_AI_intro](https://github.com/gpsaggese/gpsaggese.github.io/tree/master/msml610/lectures/Lesson08.1-Causal_AI_intro.pdf) | [Lesson08.2-Causal_Networks](https://github.com/gpsaggese/gpsaggese.github.io/tree/master/msml610/lectures/Lesson08.2-Causal_Networks.pdf)

- Spurious correlations and Simpson's paradox
- Confounding variables and colliders
- Causal questions vs. predictive questions
- DAGs and d-separation: the language of causal reasoning
- TUTORIAL: DoWhy (illustrating the difference between correlation and causal effect)
- TUTORIAL: CausalImpact (detecting causal impact of interventions vs. spurious trends)

### 4: Structural Causal Models
[Slides: Lesson08.2-Causal_Networks](https://github.com/gpsaggese/gpsaggese.github.io/tree/master/msml610/lectures/Lesson08.2-Causal_Networks.pdf) | [Lesson08.3-Do_Calculus](https://github.com/gpsaggese/gpsaggese.github.io/tree/master/msml610/lectures/Lesson08.3-Do_Calculus.pdf)

- Causal graphs (DAGs) as a reasoning formalism
- Structural equations and functional causal models
- Interventions and the do-operator
- The do-calculus: rules for interventional reasoning
- d-separation and conditional independence
- Potential outcomes framework (Rubin causal model) and its equivalence to SCMs
- TUTORIAL: pgmpy (building and querying Bayesian networks and DAGs)
- TUTORIAL: Dagitty (DAG creation and causal effect identification)

### 5: Counterfactual Reasoning
[Slides: Lesson08.1-Causal_AI_intro](https://github.com/gpsaggese/gpsaggese.github.io/tree/master/msml610/lectures/Lesson08.1-Causal_AI_intro.pdf) | [Lesson08.3-Do_Calculus](https://github.com/gpsaggese/gpsaggese.github.io/tree/master/msml610/lectures/Lesson08.3-Do_Calculus.pdf)

- What is a counterfactual
- Counterfactuals vs. interventions: the three rungs of the ladder of causation
- Computing counterfactuals from structural causal models
- Counterfactual explanations for ML predictions and algorithmic recourse
- Applications: what would have happened without the treatment?
- TUTORIAL: DoWhy (counterfactual queries in structural causal models)
- TUTORIAL: DiCE (diverse counterfactual explanations for ML models)

### 6: Causal Identification
[Slides: Lesson08.3-Do_Calculus](https://github.com/gpsaggese/gpsaggese.github.io/tree/master/msml610/lectures/Lesson08.3-Do_Calculus.pdf)

- The identification problem: when can we estimate causal effects from data?
- Backdoor and frontdoor criteria
- Instrumental variables and natural experiments
- Regression discontinuity and difference-in-differences
- Selection bias
- TUTORIAL: DoWhy (applying backdoor/frontdoor/IV criteria for causal identification)
- TUTORIAL: IBM Causal Inference 360 (identification strategies and sensitivity analysis)

### 7: Estimating Causal Effects
// Not covered
- Average treatment effect (ATE) and conditional ATE (CATE)
- Matching methods and propensity scores
- Regression adjustment and doubly robust methods
- Uplift modeling and heterogeneous treatment effects
- Application: healthcare observational studies and treatment effect estimation
- TUTORIAL: EconML (double ML, causal forests, and meta-learners for ATE/CATE estimation)
- TUTORIAL: CausalML (propensity scoring, matching, and uplift estimation)

### 8: Sensitivity Analysis and Causal Model Validation
// Not covered
- Why causal estimates can be fragile
- Unmeasured confounding and its consequences
- Rosenbaum bounds and E-values
- Refutation methods: random common cause, data subset, placebo treatment
- How to know if your causal model is wrong
- TUTORIAL: DoWhy (built-in refutation tests and sensitivity analysis)
- TUTORIAL: IBM Causal Inference 360 (sensitivity analysis for observational studies)

### 9: A/B Testing, Experimentation, and Causal Inference in Practice
[Slides: Lesson09.3-Multi_Armed_Bandits](https://github.com/gpsaggese/gpsaggese.github.io/tree/master/msml610/lectures/Lesson09.3-Multi_Armed_Bandits.pdf)

- Randomization and its relationship to causal identification
- A/B testing, switchback experiments, and their limits
- When to use observational methods vs. experiments
- Uplift modeling and targeted interventions
- Policy evaluation
- Application: marketing uplift, targeted customer interventions, and campaign analysis
- TUTORIAL: CausalML (uplift modeling and A/B test analysis)
- TUTORIAL: CausalPy (causal effect estimation with Bayesian models)

## Part III — Causal Methods in Practice

### 10: Causal Inference for Time Series
[Slides: Lesson10-Timeseries_forecasting](https://github.com/gpsaggese/gpsaggese.github.io/tree/master/msml610/lectures/Lesson10-Timeseries_forecasting.pdf)

- Time series vs. cross-sectional causal inference
- Granger causality: definition, assumptions, and limitations
- Interrupted time series (ITS) and regression discontinuity
- Difference-in-differences (DiD) and parallel trends assumption
- Synthetic control: constructing a counterfactual from donor series
- When temporal structure helps and when it misleads
- TUTORIAL: CausalImpact (Bayesian interrupted time series for causal inference)
- TUTORIAL: CausalPy (DiD and synthetic control with Bayesian models)

### 11: Causal Discovery: Learning Structure from Data
// Not covered
- Constraint-based methods: PC algorithm and FCI
- Score-based methods: GES, NOTEARS
- LiNGAM and non-Gaussian methods
- Granger causality and state space representations
- Practical limitations and when discovery fails
- TUTORIAL: causal-learn (PC algorithm, GES, and constraint-based discovery)
- TUTORIAL: LiNGAM (linear non-Gaussian causal model discovery)

### 12: Causal Machine Learning
// Not covered
- Why standard ML fails at causal questions
- Double machine learning
- Meta-learners: S-learner, T-learner, X-learner, R-learner
- Causal forests and nonparametric methods
- Heterogeneous treatment effects in practice
- TUTORIAL: EconML (double ML, causal forests, S/T/X-learners, HTE estimation)
- TUTORIAL: CausalML (meta-learners and heterogeneous treatment effect estimation)

### 13: Causal Fairness and Algorithmic Accountability
// Not covered
- Limitations of statistical fairness (demographic parity, equalized odds)
- Causal definitions of fairness
- Path-specific effects and direct vs. indirect discrimination
- Counterfactual fairness and interventional fairness
- Applications: credit scoring, hiring, criminal justice
- TUTORIAL: AI Fairness 360 (causal fairness metrics and auditing)
- TUTORIAL: DoWhy (counterfactual fairness analysis)

## Part IV — Explainability

### 14: Explainability Methods: What They Do and Do Not Tell You
[Slides: Lesson11-Probabilistic_deep_learning](https://github.com/gpsaggese/gpsaggese.github.io/tree/master/msml610/lectures/Lesson11-Probabilistic_deep_learning.pdf)

- Why practitioners reach for explainability first
- Black box models, regulation, and trust
- Model-specific interpretability: linear models, decision trees, GAMs
- Model-agnostic methods: PDP, ICE, feature importance
- Local vs. global explanations
- SHAP: Shapley values from game theory to ML; TreeSHAP, KernelSHAP, DeepSHAP
- LIME: local linear approximations
- When SHAP is causal and when it is not
- The gap between explanation and causation: feature importance is not causality
- When explainability is sufficient and when causal reasoning is needed
- TUTORIAL: SHAP (explaining black-box model predictions with Shapley values)
- TUTORIAL: LIME (local interpretable model-agnostic explanations)

### 15: Causal Explainability and Algorithmic Recourse
[Slides: Lesson08.1-Causal_AI_intro](https://github.com/gpsaggese/gpsaggese.github.io/tree/master/msml610/lectures/Lesson08.1-Causal_AI_intro.pdf) | [Lesson11-Probabilistic_deep_learning](https://github.com/gpsaggese/gpsaggese.github.io/tree/master/msml610/lectures/Lesson11-Probabilistic_deep_learning.pdf)

- Causal SHAP and causal attribution methods
- Counterfactual explanations and actionable recourse
- Why explainability methods must be interpreted through a causal lens
- Contrasting causal effects with feature importance
- TUTORIAL: DiCE (diverse counterfactual explanations and algorithmic recourse)
- TUTORIAL: DoWhy (contrasting causal effect with feature importance)

## Part V — Decision-Making Under Uncertainty

### 16: Decision Theory and Bayesian Decision Making
[Slides: Lesson07.1-Intro_to_Probabilistic_Programming](https://github.com/gpsaggese/gpsaggese.github.io/tree/master/msml610/lectures/Lesson07.1-Intro_to_Probabilistic_Programming.pdf) | [Lesson07.2-Posterior_Based_Decisions](https://github.com/gpsaggese/gpsaggese.github.io/tree/master/msml610/lectures/Lesson07.2-Posterior_Based_Decisions.pdf) | [Lesson07.5-Bayesian_Model_Comparison](https://github.com/gpsaggese/gpsaggese.github.io/tree/master/msml610/lectures/Lesson07.5-Bayesian_Model_Comparison.pdf) | [Lesson09.3-Multi_Armed_Bandits](https://github.com/gpsaggese/gpsaggese.github.io/tree/master/msml610/lectures/Lesson09.3-Multi_Armed_Bandits.pdf)

- Utility theory, loss functions, and expected utility
- Risk preferences and risk-aware decisions
- Multi-criteria decisions and trade-offs
- Statistical decision theory and Bayes optimal decisions
- Bayesian inference and posterior-based decisions
- Thompson sampling and Bayesian optimization
- Bayesian hypothesis testing for practitioners
- Aleatoric vs. epistemic uncertainty
- Confidence intervals and prediction intervals
- TUTORIAL: PyMC (Bayesian inference, uncertainty quantification, and posterior-based decisions)
- TUTORIAL: BoTorch (Bayesian optimization for sequential decision making)

### 17: Probabilistic Forecasting and Uncertainty Quantification
[Slides: Lesson10-Timeseries_forecasting](https://github.com/gpsaggese/gpsaggese.github.io/tree/master/msml610/lectures/Lesson10-Timeseries_forecasting.pdf)

- Time series decomposition: trend, seasonality, residuals
- Classical models: ARIMA, SARIMA, exponential smoothing
- Machine learning models: XGBoost, LightGBM on time features
- Deep learning models: N-BEATS, TFT, PatchTST
- Probabilistic forecasting, prediction intervals, and calibration
- Conformal prediction for time series
- Evaluating forecasts: MASE, CRPS, calibration
- Application: supply chain demand forecasting and forecast-driven decisions
- TUTORIAL: Darts (unified forecasting with classical, ML, and deep learning models)
- TUTORIAL: NeuralForecast (deep learning models for probabilistic time series)

### 18: Reinforcement Learning and Sequential Decisions
[Slides: Lesson12-Reinforcement_learning](https://github.com/gpsaggese/gpsaggese.github.io/tree/master/msml610/lectures/Lesson12-Reinforcement_learning.pdf)

- Markov decision processes
- Partially observable MDPs (POMDPs) and belief states
- Exploration vs. exploitation
- Model-based vs. model-free RL
- Offline reinforcement learning and batch policy evaluation
- TUTORIAL: gymnasium (standard RL environments for MDP experimentation)
- TUTORIAL: Stable Baselines3 (reliable RL algorithm implementations)
- TUTORIAL: d3rlpy (offline reinforcement learning algorithms)

### 19: Causal Decision Making
[Slides: Lesson08.5-Causal_AI_In_Business](https://github.com/gpsaggese/gpsaggese.github.io/tree/master/msml610/lectures/Lesson08.5-Causal_AI_In_Business.pdf)

- Why causal models are required for interventional decisions
- Decision diagrams and influence diagrams
- Policy interventions, uplift, and treatment policies
- Causal RL: integrating causal models into sequential decision making
- TUTORIAL: DoWhy (counterfactual reasoning and policy evaluation)
- TUTORIAL: EconML (treatment policy optimization and uplift)

## Part VI — Causal AI Agents

### 20: LLMs and Causal Reasoning
// Not covered
- What LLMs get right and wrong about causality
- Chain-of-thought, tree-of-thought, and self-consistency for causal tasks
- Reflection and self-correction: Reflexion and iterative refinement
- Connecting LLM reasoning to causal and probabilistic reasoning
- TUTORIAL: LangChain (CoT and tool-augmented reasoning pipelines)
- TUTORIAL: LlamaIndex (knowledge-grounded reasoning over structured data)

### 21: Building Causal Decision Agents
// Not covered
- Agent architectures: reactive, deliberative, causal
- Integrating causal models into agent action selection
- Planning under causal uncertainty
- Multi-agent systems and human-in-the-loop
- TUTORIAL: ReAct (reasoning and acting framework for LLM agents)
- TUTORIAL: LangChain + DoWhy (causal model integrated into agent reasoning)

## Conclusion

### 22: Toward Causal Intelligence: Synthesis and the Road Ahead
// Not covered
- Revisiting the prediction-reasoning-decision arc
- The causal AI stack: from raw data to decisions
- Open problems: causal discovery at scale, causal LLMs, real-time causal systems
- The limits of causal AI: when causal methods fail or are inapplicable
- Practical starting points for ML practitioners
- The shift from correlational to causal AI in industry

## Appendix (online)

- A: Mathematical foundations of causal inference
  [Slides: Lesson08.1-Causal_AI_intro](https://github.com/gpsaggese/gpsaggese.github.io/tree/master/msml610/lectures/Lesson08.1-Causal_AI_intro.pdf) | [Lesson08.2-Causal_Networks](https://github.com/gpsaggese/gpsaggese.github.io/tree/master/msml610/lectures/Lesson08.2-Causal_Networks.pdf) | [Lesson08.3-Do_Calculus](https://github.com/gpsaggese/gpsaggese.github.io/tree/master/msml610/lectures/Lesson08.3-Do_Calculus.pdf)

- B: DAG notation, d-separation rules, and identification algorithms
  [Slides: Lesson08.2-Causal_Networks](https://github.com/gpsaggese/gpsaggese.github.io/tree/master/msml610/lectures/Lesson08.2-Causal_Networks.pdf) | [Lesson08.3-Do_Calculus](https://github.com/gpsaggese/gpsaggese.github.io/tree/master/msml610/lectures/Lesson08.3-Do_Calculus.pdf)

- C: Potential outcomes framework reference
  [Slides: Lesson08.2-Causal_Networks](https://github.com/gpsaggese/gpsaggese.github.io/tree/master/msml610/lectures/Lesson08.2-Causal_Networks.pdf) | [Lesson08.3-Do_Calculus](https://github.com/gpsaggese/gpsaggese.github.io/tree/master/msml610/lectures/Lesson08.3-Do_Calculus.pdf)

- D: Bayesian statistics refresher
  [Slides: Lesson07.1-Intro_to_Probabilistic_Programming](https://github.com/gpsaggese/gpsaggese.github.io/tree/master/msml610/lectures/Lesson07.1-Intro_to_Probabilistic_Programming.pdf) | [Lesson07.2-Posterior_Based_Decisions](https://github.com/gpsaggese/gpsaggese.github.io/tree/master/msml610/lectures/Lesson07.2-Posterior_Based_Decisions.pdf) | [Lesson07.3-Hierarchical_Models](https://github.com/gpsaggese/gpsaggese.github.io/tree/master/msml610/lectures/Lesson07.3-Hierarchical_Models.pdf) | [Lesson07.4-Generalized_Linear_Models](https://github.com/gpsaggese/gpsaggese.github.io/tree/master/msml610/lectures/Lesson07.4-Generalized_Linear_Models.pdf) | [Lesson07.5-Bayesian_Model_Comparison](https://github.com/gpsaggese/gpsaggese.github.io/tree/master/msml610/lectures/Lesson07.5-Bayesian_Model_Comparison.pdf)

- E: Optimization methods
  [Slides: Lesson97.Refresher_numerical_optimization](https://github.com/gpsaggese/gpsaggese.github.io/tree/master/msml610/lectures/Lesson97.Refresher_numerical_optimization.pdf)

- F: Reinforcement learning math
  [Slides: Lesson12-Reinforcement_learning](https://github.com/gpsaggese/gpsaggese.github.io/tree/master/msml610/lectures/Lesson12-Reinforcement_learning.pdf)

- G: Time series math: stationarity, spectral analysis, state space representations
  [Slides: Lesson10-Timeseries_forecasting](https://github.com/gpsaggese/gpsaggese.github.io/tree/master/msml610/lectures/Lesson10-Timeseries_forecasting.pdf) | [Lesson96.Refresher_stochastic_processes](https://github.com/gpsaggese/gpsaggese.github.io/tree/master/msml610/lectures/Lesson96.Refresher_stochastic_processes.pdf)
// Not covered
- H: Python ecosystem guide (tools, libraries, comparison table)
// Not covered
- I: Further reading and research papers
