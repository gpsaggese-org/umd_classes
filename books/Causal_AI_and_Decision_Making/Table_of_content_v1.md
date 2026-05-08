# From Prediction to Decision: Causal AI for Machine Learning Practitioners

## Part I — Foundations of Causal Inference

### 1: From Prediction Pipelines to Decision Pipelines
[msml610/lectures_source/Lesson08.1-Causal_AI_intro.txt](https://github.com/gpsaggese/gpsaggese.github.io/tree/master/msml610/lectures/Lesson08.1-Causal_AI_intro.pdf)

- What ML systems can and cannot tell you
- Correlation, association, and the illusion of understanding
- Three kinds of questions: association, intervention, counterfactual (Pearl's
  ladder)
- A roadmap: from prediction to causal reasoning to decision intelligence
- TUTORIAL: DoWhy (end-to-end causal reasoning from observational data)

[msml610/lectures_source/Lesson02.2-ML_Paradigms.txt](https://github.com/gpsaggese/gpsaggese.github.io/tree/master/msml610/lectures/Lesson02.2-ML_Paradigms.pdf)

- How production ML systems make decisions today
- Feedback loops and distribution shift
- Optimization vs. inference vs. decision theory
- The cost of ignoring causality: concrete failure modes
- Data Science vs. Decision Science
- TUTORIAL: pgmpy (Bayesian decision networks and decision pipeline modeling)

### 2: Causality Vs. Correlation
[msml610/lectures_source/Lesson08.1-Causal_AI_intro.txt](https://github.com/gpsaggese/gpsaggese.github.io/tree/master/msml610/lectures/Lesson08.1-Causal_AI_intro.pdf)
[msml610/lectures_source/Lesson08.2-Causal_Networks.txt](https://github.com/gpsaggese/gpsaggese.github.io/tree/master/msml610/lectures/Lesson08.2-Causal_Networks.pdf)

- Spurious correlations and Simpson's paradox
- Confounding variables and colliders
- Causal questions vs. predictive questions
- DAGs and d-separation: the language of causal reasoning
- TUTORIAL: DoWhy (illustrating the difference between correlation and causal
  effect)
- TUTORIAL: CausalImpact (detecting causal impact of interventions vs. spurious
  trends)

### 3: Structural Causal Models
[msml610/lectures_source/Lesson08.2-Causal_Networks.txt](https://github.com/gpsaggese/gpsaggese.github.io/tree/master/msml610/lectures/Lesson08.2-Causal_Networks.pdf)
[msml610/lectures_source/Lesson08.3-Do_Calculus.txt](https://github.com/gpsaggese/gpsaggese.github.io/tree/master/msml610/lectures/Lesson08.3-Do_Calculus.pdf)

- Causal graphs (DAGs) as a reasoning formalism
- Structural equations and functional causal models
- Interventions and the do-operator
- The do-calculus: rules for interventional reasoning
- D-separation and conditional independence
- Potential outcomes framework (Rubin causal model) and its equivalence to SCMs
- TUTORIAL: pgmpy (building and querying Bayesian networks and DAGs)
- TUTORIAL: Dagitty (DAG creation and causal effect identification)

### 4: Counterfactual Reasoning
[msml610/lectures_source/Lesson08.1-Causal_AI_intro.txt](https://github.com/gpsaggese/gpsaggese.github.io/tree/master/msml610/lectures/Lesson08.1-Causal_AI_intro.pdf)
[msml610/lectures_source/Lesson08.3-Do_Calculus.txt](https://github.com/gpsaggese/gpsaggese.github.io/tree/master/msml610/lectures/Lesson08.3-Do_Calculus.pdf)

- What is a counterfactual
- Counterfactuals vs. interventions: the three rungs of the ladder of causation
- Computing counterfactuals from structural causal models
- Counterfactual explanations for ML predictions and algorithmic recourse
- Applications: what would have happened without the treatment?
- TUTORIAL: DoWhy (counterfactual queries in structural causal models)
- TUTORIAL: DiCE (diverse counterfactual explanations for ML models)

### 5: Causal Identification
[msml610/lectures_source/Lesson08.3-Do_Calculus.txt](https://github.com/gpsaggese/gpsaggese.github.io/tree/master/msml610/lectures/Lesson08.3-Do_Calculus.pdf)

- The identification problem: when can we estimate causal effects from data?
- Backdoor and frontdoor criteria
- Instrumental variables and natural experiments
- Regression discontinuity and difference-in-differences
- Selection bias
- TUTORIAL: DoWhy (applying backdoor/frontdoor/IV criteria for causal
  identification)

### 6: Estimating Causal Effects
// Not covered

- Average treatment effect (ATE) and conditional ATE (CATE)
- Matching methods and propensity scores
- Regression adjustment and doubly robust methods
- Uplift modeling and heterogeneous treatment effects
- Application: healthcare observational studies and treatment effect estimation
- TUTORIAL: EconML (double ML, causal forests, and meta-learners for ATE/CATE
  estimation)
- TUTORIAL: CausalML (propensity scoring, matching, and uplift estimation)

### 7: Sensitivity Analysis and Causal Model Validation
// Not covered

- Why causal estimates can be fragile
- Unmeasured confounding and its consequences
- Rosenbaum bounds and E-values
- Refutation methods: random common cause, data subset, placebo treatment
- How to know if your causal model is wrong
- TUTORIAL: DoWhy (built-in refutation tests and sensitivity analysis)

### 8: A/B Testing, Experimentation, and Causal Inference in Practice
[msml610/lectures_source/Lesson09.3-Multi_Armed_Bandits.txt](https://github.com/gpsaggese/gpsaggese.github.io/tree/master/msml610/lectures/Lesson09.3-Multi_Armed_Bandits.pdf)

- Randomization and its relationship to causal identification
- A/B testing, switchback experiments, and their limits
- When to use observational methods vs. experiments
- Uplift modeling and targeted interventions
- Policy evaluation
- Application: marketing uplift, targeted customer interventions, and campaign
  analysis
- TUTORIAL: CausalML (uplift modeling and A/B test analysis)
- TUTORIAL: CausalPy (causal effect estimation with Bayesian models)

## Part II — Causal Methods in Practice

### 9: Causal Inference for Time Series
[msml610/lectures_source/Lesson10-Timeseries_forecasting.txt](https://github.com/gpsaggese/gpsaggese.github.io/tree/master/msml610/lectures/Lesson10-Timeseries_forecasting.pdf)

- Time series vs. cross-sectional causal inference
- Granger causality: definition, assumptions, and limitations
- Interrupted time series (ITS) and regression discontinuity
- Difference-in-differences (DiD) and parallel trends assumption
- Synthetic control: constructing a counterfactual from donor series
- When temporal structure helps and when it misleads
- TUTORIAL: CausalImpact (Bayesian interrupted time series for causal inference)
- TUTORIAL: CausalPy (DiD and synthetic control with Bayesian models)

### 10: Causal Discovery: Learning Structure From Data
// Not covered

- Constraint-based methods: PC algorithm and FCI
- Score-based methods: GES, NOTEARS
- LiNGAM and non-Gaussian methods
- Granger causality and state space representations
- Practical limitations and when discovery fails
- TUTORIAL: causal-learn (PC algorithm, GES, and constraint-based discovery)
- TUTORIAL: LiNGAM (linear non-Gaussian causal model discovery)

### 11: Static Decision-Making
[msml610/lectures_source/Lesson07.1-Intro_to_Probabilistic_Programming.txt](https://github.com/gpsaggese/gpsaggese.github.io/tree/master/msml610/lectures/Lesson07.1-Intro_to_Probabilistic_Programming.pdf)
[msml610/lectures_source/Lesson07.2-Posterior_Based_Decisions.txt](https://github.com/gpsaggese/gpsaggese.github.io/tree/master/msml610/lectures/Lesson07.2-Posterior_Based_Decisions.pdf)

- Utility theory and expected utility
- Risk preferences and risk-aware decisions
- Multi-criteria decisions and trade-offs
- Statistical decision theory and Bayes optimal decisions
- Bayesian inference and posterior-based decisions
- Uncertainty quantification for decision-making
- Confidence intervals and prediction intervals
- TUTORIAL: PyMC (Bayesian inference, uncertainty quantification, and
  posterior-based decisions)

### 12: Sequential Decision-Making
[msml610/lectures_source/Lesson12-Reinforcement_learning.txt](https://github.com/gpsaggese/gpsaggese.github.io/tree/master/msml610/lectures/Lesson12-Reinforcement_learning.pdf)
[msml610/lectures_source/Lesson08.5-Causal_AI_In_Business.txt](https://github.com/gpsaggese/gpsaggese.github.io/tree/master/msml610/lectures/Lesson08.5-Causal_AI_In_Business.pdf)

- Markov decision processes and optimal policies
- Exploration vs. exploitation trade-off
- Model-based vs. model-free reinforcement learning
- Offline reinforcement learning and batch policy evaluation
- Causal reinforcement learning: integrating causal models into sequential decisions
- Heterogeneous treatment effects and personalization
- Policy interventions and treatment policies
- TUTORIAL: gymnasium (standard RL environments for MDP experimentation)
- TUTORIAL: Stable Baselines3 (reliable RL algorithm implementations)
- TUTORIAL: d3rlpy (offline reinforcement learning algorithms)
- TUTORIAL: EconML (causal RL and treatment policy optimization)

### 13: Decisions Under Uncertainty
[msml610/lectures_source/Lesson10-Timeseries_forecasting.txt](https://github.com/gpsaggese/gpsaggese.github.io/tree/master/msml610/lectures/Lesson10-Timeseries_forecasting.pdf)

- Aleatoric vs. epistemic uncertainty
- Probabilistic forecasting and predictive distributions
- Bayesian prediction and calibration
- Conformal prediction and distribution-free methods
- Quantile regression and interval forecasts
- Sensitivity analysis and robustness
- Worst-case analysis and robust optimization
- TUTORIAL: PyMC (posterior predictive checks and uncertainty quantification)
- TUTORIAL: Hugging Face Transformers (uncertainty in pretrained models)

### 14: From Insights to Outcomes
[msml610/lectures_source/Lesson08.5-Causal_AI_In_Business.txt](https://github.com/gpsaggese/gpsaggese.github.io/tree/master/msml610/lectures/Lesson08.5-Causal_AI_In_Business.pdf)
[msml610/lectures_source/Lesson09.3-Multi_Armed_Bandits.txt](https://github.com/gpsaggese/gpsaggese.github.io/tree/master/msml610/lectures/Lesson09.3-Multi_Armed_Bandits.pdf)

- A/B testing and experimental design
- Causal decision-making in practice
- Business applications and uplift modeling
- Policy evaluation and continuous learning
- Communicating causal insights to stakeholders
- Causal fairness and algorithmic accountability
- Path-specific effects and direct vs. indirect discrimination
- Counterfactual fairness and interventional fairness
- Applications: credit scoring, hiring, criminal justice, marketing
- TUTORIAL: CausalML (uplift modeling and A/B test analysis)
- TUTORIAL: DoWhy (counterfactual reasoning and policy evaluation)
- TUTORIAL: EconML (treatment policy optimization and business analytics)

## Part III — Advanced Topics and Extensions

**Note**: The core decision-making curriculum is covered in Chapters 11–14. The following chapters provide advanced extensions and specialized applications.

### 15: Explainability and Interpretability
[msml610/lectures_source/Lesson11-Probabilistic_deep_learning.txt](https://github.com/gpsaggese/gpsaggese.github.io/tree/master/msml610/lectures/Lesson11-Probabilistic_deep_learning.pdf)

- Why practitioners reach for explainability first
- Black box models, regulation, and trust
- Model-specific interpretability: linear models, decision trees, GAMs
- Model-agnostic methods: PDP, ICE, feature importance
- SHAP: Shapley values and when they are causal
- LIME: local linear approximations
- The gap between explanation and causation
- When explainability is sufficient and when causal reasoning is needed
- Causal SHAP and causal attribution methods
- Counterfactual explanations and algorithmic recourse
- TUTORIAL: SHAP (explaining black-box model predictions with Shapley values)
- TUTORIAL: LIME (local interpretable model-agnostic explanations)
- TUTORIAL: DiCE (diverse counterfactual explanations and algorithmic recourse)

### 16: Advanced Causal Methods
// Not covered

- Why standard ML fails at causal questions
- Double machine learning
- Meta-learners: S-learner, T-learner, X-learner, R-learner
- Causal forests and nonparametric methods
- Heterogeneous treatment effects estimation
- Sensitivity analysis and causal model validation
- Unmeasured confounding and robustness
- TUTORIAL: EconML (double ML, causal forests, S/T/X-learners, HTE estimation)
- TUTORIAL: CausalML (meta-learners and heterogeneous treatment effect estimation)
- TUTORIAL: DoWhy (refutation tests and sensitivity analysis)

### 17: LLMs and Causal Reasoning
// Not covered

- What LLMs get right and wrong about causality
- Chain-of-thought, tree-of-thought, and self-consistency for causal tasks
- Reflection and self-correction: Reflexion and iterative refinement
- Connecting LLM reasoning to causal and probabilistic reasoning
- Agent architectures: reactive, deliberative, causal
- Integrating causal models into agent action selection
- Planning under causal uncertainty
- Multi-agent systems and human-in-the-loop
- TUTORIAL: ReAct (reasoning and acting framework for LLM agents)
- TUTORIAL: LangChain (CoT and tool-augmented reasoning pipelines)
- TUTORIAL: LangChain + DoWhy (causal model integrated into agent reasoning)
- TUTORIAL: LlamaIndex (knowledge-grounded reasoning over structured data)
