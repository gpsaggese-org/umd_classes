# Beyond Prediction: Causal AI, Explainability, and Decision Intelligence for Machine Learning Practitioners

## Table of Contents

## Part I — From Prediction to Decision Intelligence
1. **Introduction: The Limits of Prediction**
   - Prediction vs. decision-making
   - Why correlation is not enough
   - From ML models to decision systems
   - Overview of causal AI and explainability
   - TUTORIAL: DoWhy (end-to-end causal reasoning from observational data)

2. **Data Science vs. Decision Science**
   - Predictive modeling pipelines
   - Decision pipelines
   - Optimization vs. inference
   - Feedback loops in ML systems
   - TUTORIAL: YData-profiling (data understanding and profiling for decision workflows)

3. **Uncertainty in Machine Learning**
   - Aleatoric vs. epistemic uncertainty
   - Confidence intervals and prediction intervals
   - Bayesian thinking for ML practitioners
   - Risk-aware decision-making
   - TUTORIAL: PyMC3 (Bayesian statistical modeling and uncertainty quantification)
   - TUTORIAL: TensorFlow Probability (probabilistic reasoning and uncertainty estimation)

## Part II — Foundations of Causal Inference
4. **Causality vs. Correlation**
   - Spurious correlations
   - Simpson's paradox
   - Confounding variables
   - Causal questions vs. predictive questions
   - TUTORIAL: DoWhy (illustrating the difference between correlation and causal effect)
   - TUTORIAL: CausalImpact (detecting causal impact of interventions vs. spurious trends)

5. **Structural Causal Models**
   - Causal graphs (DAGs)
   - Structural equations
   - Interventions and counterfactuals
   - The do-operator
   - TUTORIAL: pgmpy (building and querying Bayesian networks and DAGs)
   - TUTORIAL: CausalGraphicalModels (defining and visualizing structural causal models)
   - TUTORIAL: Dagitty (DAG creation and causal effect identification)

6. **Causal Identification**
   - Backdoor criterion
   - Frontdoor criterion
   - Instrumental variables
   - Selection bias
   - TUTORIAL: DoWhy (applying backdoor/frontdoor criteria for causal identification)
   - TUTORIAL: IBM Causal Inference 360 (identification strategies and sensitivity analysis)

7. **Estimating Causal Effects**
   - Average treatment effect (ATE)
   - Matching methods
   - Propensity scores
   - Regression adjustment
   - Doubly robust methods
   - TUTORIAL: EconML (double ML, causal forests, and meta-learners for ATE estimation)
   - TUTORIAL: CausalML (propensity scoring, matching, and uplift estimation)
   - TUTORIAL: CausalInference (regression adjustment and doubly robust methods)

8. **Causal Inference in Practice**
   - A/B testing and experimentation
   - Uplift modeling
   - Policy evaluation
   - Observational vs experimental data
   - TUTORIAL: CausalML (uplift modeling and A/B test analysis)
   - TUTORIAL: CausalPy (causal effect estimation with Bayesian models)
   - TUTORIAL: CausalImpact (policy evaluation using interrupted time-series analysis)

## Part III — Machine Learning Explainability
9. **Why Explainability Matters**
   - Black box models
   - Regulation and trust
   - Debugging ML models
   - Explainability vs interpretability
   - TUTORIAL: SHAP (explaining black-box model predictions with Shapley values)
   - TUTORIAL: AI Fairness 360 (bias detection and regulation-driven fairness auditing)

10. **Model-Specific Interpretability**
    - Linear models
    - Decision trees
    - Rule-based models
    - Generalized additive models (GAMs)
    - TUTORIAL: What-If Tool (interactive model interpretability and comparison)
    - TUTORIAL: SHAP (feature attribution for linear models and tree-based models)

11. **Model-Agnostic Explainability**
    - Feature importance
    - Partial dependence plots
    - ICE plots
    - Global vs local explanations
    - TUTORIAL: SHAP (global and local model-agnostic explanations)
    - TUTORIAL: LIME (local interpretable model-agnostic explanations)

12. **SHAP, LIME, and Modern Explanation Methods**
    - Shapley values
    - LIME explanations
    - Counterfactual explanations
    - Limitations of explainability methods
    - TUTORIAL: SHAP (Shapley values for model explanation)
    - TUTORIAL: LIME (local surrogate model explanations)
    - TUTORIAL: Fairlearn (fairness metrics and counterfactual fairness)

13. **Explainability vs Causality**
    - Feature importance is not causality
    - When explanations are misleading
    - Causal feature importance
    - Interventions vs attribution
    - TUTORIAL: DoWhy (contrasting causal effect with feature importance)
    - TUTORIAL: EconML (causal feature importance vs. predictive importance)
    - TUTORIAL: SHAP (showing limitations when correlations mislead attribution)

## Part IV — Decision-Making Under Uncertainty
14. **Decision Theory for Data Scientists**
    - Utility theory
    - Loss functions vs utility
    - Expected value and expected utility
    - Risk preferences
    - TUTORIAL: optuna (hyperparameter optimization as a decision problem)
    - TUTORIAL: Ax (adaptive experimentation and expected utility maximization)

15. **Bayesian Decision Making**
    - Bayesian inference
    - Posterior distributions
    - Thompson sampling
    - Bayesian optimization
    - TUTORIAL: PyMC3 (Bayesian inference and posterior-based decisions)
    - TUTORIAL: Numpyro (probabilistic programming for Bayesian decision making)
    - TUTORIAL: BoTorch (Bayesian optimization for sequential decision making)
    - TUTORIAL: pyro (probabilistic programming with PyTorch)

16. **Reinforcement Learning and Sequential Decisions**
    - Markov decision processes
    - Exploration vs exploitation
    - Policy learning
    - Offline reinforcement learning
    - TUTORIAL: gymnasium (standard RL environments for MDP experimentation)
    - TUTORIAL: Stable Baselines3 (reliable RL algorithm implementations)
    - TUTORIAL: ray[rllib] (scalable reinforcement learning)
    - TUTORIAL: d3rlpy (offline reinforcement learning algorithms)

17. **Causal Decision Making**
    - Policy interventions
    - Counterfactual reasoning
    - Decision optimization with causal models
    - Uplift and treatment policies
    - TUTORIAL: DoWhy (counterfactual reasoning and policy evaluation)
    - TUTORIAL: EconML (treatment policy optimization and uplift)
    - TUTORIAL: CausalML (causal policy learning and uplift modeling)

## Part V — Causal AI: Going Beyond Correlation
18. **What is Causal AI**
    - Predictive AI vs Causal AI
    - Decision intelligence systems
    - Causal reasoning systems
    - TUTORIAL: DoWhy (causal reasoning pipeline vs. predictive pipeline)
    - TUTORIAL: EconML (causal AI for business decision systems)

19. **Causal Machine Learning**
    - Double machine learning
    - Causal forests
    - Meta-learners (S-learner, T-learner, X-learner)
    - Heterogeneous treatment effects
    - TUTORIAL: EconML (double ML, causal forests, S/T/X-learners, HTE estimation)
    - TUTORIAL: CausalML (meta-learners and heterogeneous treatment effect estimation)

20. **Causal Representation Learning**
    - Learning causal structure
    - Invariant risk minimization
    - Domain adaptation and causality
    - Distribution shifts
    - TUTORIAL: Causica (combining causal discovery and inference with deep learning)
    - TUTORIAL: CausalNex (causal representation with Bayesian Networks)

21. **Causal Discovery**
    - Constraint-based methods
    - Score-based methods
    - Granger causality
    - Practical limitations
    - TUTORIAL: causal-learn (PC algorithm, GES, and constraint-based discovery)
    - TUTORIAL: LiNGAM (linear non-Gaussian causal model discovery)
    - TUTORIAL: bnlearn (Bayesian network structure learning)
    - TUTORIAL: gCastle (Huawei toolkit for causal structure learning)
    - TUTORIAL: Tetrad (suite for causal model discovery and analysis)
    - TUTORIAL: Causal Discovery Toolbox (framework for causal structure discovery)

22. **From Prediction Systems to Decision Systems**
    - Recommendation systems
    - Pricing systems
    - Marketing interventions
    - Healthcare decision systems
    - TUTORIAL: CausalML (causal intervention modeling for business systems)
    - TUTORIAL: EconML (policy-based decision optimization)
    - TUTORIAL: DoWhy (end-to-end decision systems with causal models)

## Part VI — AI Coding, Agents, and Automation
23. **AI-Assisted Programming**
    - Code generation with LLMs
    - Prompt engineering for coding
    - Code review and debugging with AI
    - Testing with AI
    - TUTORIAL: llm (minimal library for working with LLMs for coding tasks)
    - TUTORIAL: HuggingFace (transformer models for code generation and review)

24. **Building Data Science Agents**
    - Agent architectures
    - Tool use and function calling
    - Autonomous data analysis agents
    - Multi-agent systems
    - TUTORIAL: LlamaIndex (LLM-powered data retrieval and analysis agents)
    - TUTORIAL: Langchain and Neo4j (LLM agent with graph-based knowledge)
    - TUTORIAL: ReAct (reasoning and acting framework for LLM agents)
    - TUTORIAL: Griptape (framework for building AI-powered applications)
    - TUTORIAL: AutoGPT (autonomous GPT-based agent for task planning)

25. **Automating Machine Learning Workflows**
    - AutoML
    - Feature engineering agents
    - Experimentation agents
    - Monitoring agents
    - TUTORIAL: FLAML (fast and lightweight AutoML)
    - TUTORIAL: AutoGluon (AutoML for tabular, text, and image data)
    - TUTORIAL: TPOT (AutoML using genetic programming)
    - TUTORIAL: optuna (automated hyperparameter optimization)
    - TUTORIAL: Featuretools (automated feature engineering)

26. **Decision-Making Agents**
    - Planning agents
    - Simulation environments
    - Decision optimization agents
    - Human-in-the-loop systems
    - TUTORIAL: ReAct (planning agents with reasoning and acting)
    - TUTORIAL: Reflexion (self-reflective agent framework for improved reasoning)
    - TUTORIAL: Griptape (decision optimization agent pipelines)
    - TUTORIAL: gymnasium (simulation environments for agent decision making)

27. **Causal AI Agents**
    - Agents that reason with causal models
    - Counterfactual reasoning agents
    - Experiment design agents
    - Policy optimization agents
    - TUTORIAL: DoWhy (building agents that reason with causal graphs)
    - TUTORIAL: Causica (deep learning agents with causal discovery and inference)
    - TUTORIAL: EconML (policy optimization agents with causal models)
    - TUTORIAL: Reflexion (counterfactual reasoning via self-reflection in agents)

## Part VII — Real-World Systems and Case Studies
28. **Marketing and Uplift Modeling**
    - TUTORIAL: CausalML (uplift modeling and marketing intervention analysis)
    - TUTORIAL: EconML (heterogeneous treatment effects for targeted marketing)

29. **Recommendation Systems and Interventions**
    - TUTORIAL: DoWhy (causal recommendation systems beyond collaborative filtering)
    - TUTORIAL: EconML (intervention-based recommendation optimization)

30. **Pricing and Revenue Optimization**
    - TUTORIAL: EconML (causal pricing and revenue optimization)
    - TUTORIAL: optuna (pricing strategy optimization with Bayesian search)

31. **Healthcare and Treatment Effects**
    - TUTORIAL: DoWhy (observational study analysis for treatment effects)
    - TUTORIAL: EconML (heterogeneous treatment effects in clinical data)
    - TUTORIAL: CausalML (propensity scoring and matching for healthcare studies)
    - TUTORIAL: IBM Causal Inference 360 (causal inference toolkit for health outcomes)

32. **Supply Chain and Forecast + Decision Systems**
    - TUTORIAL: Darts (time series forecasting for supply chain)
    - TUTORIAL: sktime (time series ML framework for demand forecasting)
    - TUTORIAL: orbit (Bayesian time series models for supply chain planning)
    - TUTORIAL: GluonTS (probabilistic time-series modeling for forecasting)

33. **Risk, Fraud, and Decision Intelligence**
    - TUTORIAL: SHAP (model explanation for fraud detection models)
    - TUTORIAL: AI Fairness 360 (bias detection in risk scoring systems)
    - TUTORIAL: Fairlearn (fairness-aware risk models)
    - TUTORIAL: pysyft (privacy-preserving ML for sensitive risk data)

## Part VIII — the Future of Data Science and AI
34. **From Data Scientist to Decision Scientist**
35. **The Rise of Causal AI**
36. **Autonomous Decision Systems**
37. **AI Agents that Run Companies**
38. **Open Problems in Causal AI and Decision Intelligence**

## Appendix
- Mathematical foundations of causal inference
- Bayesian statistics refresher
- Optimization methods
- Reinforcement learning math
- Python libraries for causal ML and explainability
- Further reading and research papers
