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
- [ ] Add the topics from actual slides

### TODO
- [ ] Split Chap 1 in more chapters with also "solutions" and "examples"
- [ ] Add
  - /Users/saggese/src/csfy1/blog/docs/posts/Cracking_the_Long_Tail_of_Data_Science_Problems.md
  - /Users/saggese/src/csfy1/blog/docs/posts/Data_Is_Dumb_And_Thats_Why_Causality_Matters.md
- [ ] Replace some of the introduction with a Chapter on "Data"?

### Lessons
- `book.springer/lectures_source/Lesson01.01_From_Data_Science_To_Decision_Science.txt`
- `book.springer/lectures_source/Lesson01.02_Integrating_Causality_And_Probability_in_ML.txt`
- `book.springer/lectures_source/Lesson01.03_Integrating_Business_Objective_And_Real_World_Dynamics.txt`
- `msml610/lectures_source/Lesson08.1-Causal_AI_intro.txt`
  - [85%] — Ladder of Causation; Data Science → Decision Science; Causal vs
    Predictive Questions; Roadmap Prediction→Decision; Data Analytics
    Sophistication (maturity model); Why AI Projects Fail
- `msml610/lectures_source/Lesson11.1-Decision_Making_with_Causal_Models.txt`
  - [40%] — From Predictions to Decisions; Prediction vs Decision Side-by-Side;
    Simpson's Paradox (+Causal Resolution); Policy Reversal
- `msml610/lectures_source/Lesson08.2-Causal_Networks.txt`
  - [5%] — Example of ladder of causation (Tornado Warning)

### Tutorials

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
  - [50%] — Effect heterogeneity; CATE; Why Prediction Is Not the Answer
- `msml610/lectures_source/Lesson08.1-Causal_AI_intro.txt`
  - [45%] — Problem 2 Decision Making; Problem 5 Feedback Loops; Problem 6 Distribution Shift; Cost of Ignoring Causality
- `msml610/lectures_source/Lesson08.5-Experimentation.txt`
  - [40%] — Peeking/Multiple Comparisons; SRM; Novelty/Primacy (significance traps)
- `msml610/lectures_source/Lesson91.Refresher_probability.txt`
  - [15%] — p-hacking; multiple hypothesis testing; FDR
- Gap: Selection bias detail; missing-counterfactual problem; strategic/adversarial gaming; decision-readiness scorecard

### Tutorials

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
  - [60%] — Causal AI Workflow Steps 1–7 (Intended Outcomes → Interventions →
    Factors → Build DAG → Data Acquisition → Model Modification → Deployment);
    Marketing Example: Price Intervention
- `msml610/lectures_source/Lesson08.5-Experimentation.txt`
  - [30%] — Decision Framework: Experiment or Observe?; Feasibility Constraints
- Gap: Identifiability formal conditions (backdoor/frontdoor/IV); cost-asymmetry pricing; data collection strategy alignment
- Missing: Causal Project Checklist

### Tutorials

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
  - [70%] — Building a Causal DAG; variable types
    (mediator/moderator/confounder/collider); temporal structure
- `msml610/lectures_source/Lesson12.2-Causal_Discovery.txt`
  - [40%] — Using Domain Knowledge as Constraints; Combining Discovery with
    Expert Judgment
- `msml610/lectures_source/Lesson03-Knowledge_representation.txt`
  - [5%] — symbolic KR (ontologies, FOL, knowledge graphs); thin overlap — book
    Ch4 = decision scoping, not symbolic logic
- Gap: Structural equations/mechanisms; DAGs vs Bayesian networks distinction; measurement validity; SCM formalism

### Tutorials

## 5: Advanced Probabilistic ML

### Topics
- Short summary from Lesson6*

### Lessons
- `msml610/lectures_source/Lesson11.2-Probabilistic_deep_learning.txt`
  - [95%] — VAEs; Normalizing Flows; Bayesian NNs; VI/SVI; MCMC; Calibration;
    Conformal Prediction; Neural Processes; Deep Latent Variable Models
- `msml610/lectures_source/Lesson07.1-Intro_to_Probabilistic_Programming.txt`
  - [35%] — PPLs, Bayesian models (Pyro/PyMC/Stan)
- `msml610/lectures_source/Lesson96.Refresher_stochastic_processes.txt`
  - [10%] — Gaussian Processes (one slide)
- Gap: amortized VI; neural posterior estimation / simulation-based inference

### Tutorials

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
  - [75%] — algorithm families (constraint/PC-FCI, score/GES,
    functional/LiNGAM-ANM); Markov equivalence; identifiability; faithfulness;
    refutation
- `msml610/lectures_source/Lesson08.3-Do_Calculus.txt`
  - [25%] — do-calculus rules; back/front-door adjustment
- `msml610/lectures_source/Lesson08.2-Causal_Networks.txt`
  - [15%] — SCM; causal DAGs (basics)
- `msml610/lectures_source/Lesson11.2-Probabilistic_deep_learning.txt`
  - [20%] — Causal Deep Learning (representation learning)
- Gap: latent confounders/proxy/negative controls; E-values/sharp-bounds
  sensitivity analysis depth

### Tutorials

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
  - [90%] — Utility Functions; Expected Utility Principle
    (+insurance/two-treatment examples); Decision Networks (=influence diagrams);
    Solving a Decision Network; Risk Preferences; Aleatoric vs Epistemic
    Uncertainty
- `msml610/lectures_source/Lesson12.1-Reinforcement_learning.txt`
  - [25%] — MEU; Dynamic Decision Networks
- Gap: von Neumann-Morgenstern axioms explicit formulation; multi-criteria/Pareto optimality; deep elicitation methods

### Tutorials

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
  - [95%] — Bayesian Decision-Making; Value of Information (EVPI/EVSI); Bayesian
    Optimization for Experimentation; Acquisition Functions; Causal Bayesian
    Optimization; Exploration vs Exploitation; Causal Multi-Armed Bandits;
    Counterfactual decisions
- `msml610/lectures_source/Lesson09.3-Multi_Armed_Bandits.txt`
  - [40%] — Thompson Sampling; Bayesian Bandits; UCB
- `msml610/lectures_source/Lesson07.2-Posterior_Based_Decisions.txt`
  - [30%] — posterior-based decisions; loss functions
- Gap: Robustness under model misspecification; explicit causal-effect-to-utility pathway

### Tutorials

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
  - [85%] — Metalearners T/S/X/R-Learner; R-learner (Double/Debiased ML);
    Double-ML for CATE; Effect heterogeneity; CATE evaluation; Cumulative
    Gain/AUC
- `msml610/lectures_source/Lesson08.5-Experimentation.txt`
  - [40%] — Policy Evaluation and Off-Policy Learning
- `msml610/lectures_source/Lesson12.1-Reinforcement_learning.txt`
  - [20%] — off-policy / deconfounding
- Gap: distributional/quantile effects; safe policy improvement with finite-sample guarantees; deep off-policy optimization

### Tutorials

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
  - [50%] — Positivity; IPW Sensitivity; Positivity-Bias Trade-Off; Non-compliance and instruments
- `msml610/lectures_source/Lesson10.2-Causal_Inference_for_Time_Series.txt`
  - [30%] — Instrumental Variables (IV)
- `msml610/lectures_source/Lesson12.1-Reinforcement_learning.txt`
  - [15%] — Causal Generalization Across Environments
- Gap: Manski bounds; Rosenbaum bounds; E-values; distributional robustness/minimax; domain adaptation depth; partial identification theory

### Tutorials

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
  - [90%] — LLM causal limits; pattern vs causal reasoning; CoT causal
    prompting; integrating causal+probabilistic; causal agent architectures;
    causal MDPs; Trustworthy AI (transparency/robustness/fairness/safety);
    guardrails
- `msml610/lectures_source/Lesson16.4-LLM_Reasoning.txt`
  - [30%] — Chain-of-Thought and variants
- `msml610/lectures_source/Lesson16.1-What_Is_An_Agentic_AI.txt`
  - [25%] — agents, tools, perceive-plan-act loop
- `msml610/lectures_source/Lesson16.5-Reasoning_Memory_and_Planning.txt`
  - [35%] — world models for planning
- `msml610/lectures_source/Lesson16.7-Tool_use_and_retrieval.txt`
  - [30%] — tool use, retrieval/grounding
- Gap: Deep integration of SCMs in agent loops; causal simulation for planning; tool-use calibration under causality; stronger guardrail frameworks

### Tutorials

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
  - [90%] — MDPs/POMDPs; utilities/discount; value & policy iteration;
    model-based/free RL; Causal RL; SCMs for MDPs; Counterfactual credit
    assignment; Deconfounding off-policy; Causal Generalization
- `msml610/lectures_source/Lesson16.5-Reasoning_Memory_and_Planning.txt`
  - [30%] — World Models (WebDreamer)
- `msml610/lectures_source/Lesson09.5-Kalman_Filter.txt`
  - [20%] — POMDP-adjacent state estimation
- Gap: Detailed POMDP algorithms; counterfactual rollout mechanics; off-policy evaluation proofs; environment generalization mechanisms

### Tutorials

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
  - [85%] — forecasting breaks under intervention; Granger; ITS; DiD; Synthetic
    Control; Structural VARs; when temporal structure misleads
- `msml610/lectures_source/Lesson10.1-Timeseries_forecasting.txt`
  - [35%] — Bayesian Time Series Models; Markov-Switching (regime shifts); State Space Models
- `msml610/lectures_source/Lesson08.4.txt`
  - [20%] — Synthetic control; Difference-in-differences
- Gap: Structural time series with causal priors detail; online learning/adaptation algorithms; nonstationarity handling depth

### Tutorials

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
  - [45%] — Feedback Loops (Problem 5); Distribution Shift
- `msml610/lectures_source/Lesson09.3-Multi_Armed_Bandits.txt`
  - [55%] — Non-Stationary Bandits; Contextual Bandits
- `msml610/lectures_source/Lesson11.1-Decision_Making_with_Causal_Models.txt`
  - [30%] — Causal Multi-Armed Bandits
- `msml610/lectures_source/Lesson12.2-Causal_Discovery.txt`
  - [10%] — When Discovery Should Change Your DAG (online adaptation)
- Gap: Performativity/Goodhart's law formalization; online causal discovery algorithms; dynamic treatment regimes (DTRs); adaptive experiments (SMART trials); structural adaptation mechanisms

### Tutorials

# Part V: Implementation, Deployment, Governance

## 15: Building Stakeholder Alignment

### Topics
- Eliciting causal knowledge from domain experts during DAG construction: structured
  elicitation methods, disagreement resolution, and iterative refinement of causal
  structures before model building
- Stakeholder feedback loops during model development: reviewing intermediate
  results, sensitivity analyses, and refining assumptions based on expert critique
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
  - [40%] — Communicating Uncertainty to Stakeholders (+Worked Example);
    Multi-Criteria Trade-offs; Visualizing Risk Aversion
- `msml610/lectures_source/Lesson08.1-Causal_AI_intro.txt`
  - [45%] — Roles in Hybrid Teams; Executing a Hybrid Team Project; Causal AI
    Workflow (domain knowledge elicitation)
- `msml610/lectures_source/Lesson08.3-Do_Calculus.txt`
  - [25%] — Visual DAG explanation, confounding intuition
- `msml610/lectures_source/Lesson12.2-Causal_Discovery.txt`
  - [25%] — Using Domain Knowledge as Constraints; Combining Discovery with Expert Judgment
- Gap: Structured elicitation methods (Delphi, SGE); disagreement resolution; sensitivity analysis pedagogy; risk tolerance elicitation; buy-in protocols; intervention justification frameworks
- Missing: Communication toolkit for different stakeholder personas

### Tutorials

## 16: Deployment, Monitoring, and Adaptation

### Topics
- From notebook to production: operationalizing causal decision systems
- Cost-aware deployment strategies: phased rollout, shadow mode, and canary
  analysis tailored to decision cost asymmetry
- Operationalizing causal assumption monitoring: testable vs. untestable
  assumptions, failure detection, and implementation strategies
  - **Directly testable assumptions**: temporal stability of effects, proxy
    variable validity, treatment effect heterogeneity stability; monitoring via
    time-series trend detection, proxy correlation drift, stratified effect
    estimates in real-time dashboards
  - **Indirectly testable assumptions**: robustness bounds via sensitivity
    analysis, negative controls, instrumental variable diagnostics; pre-compute
    E-value bounds and flag when observational data approaches these thresholds
  - **Domain-assessed assumptions**: causal graph structure, sufficiency of
    confounding set (requires periodic expert re-assessment; schedule quarterly
    or post-deployment reviews)
  - Concrete monitoring dashboards: metrics that flag assumption breakdown
    (e.g., alert when treatment effect heterogeneity variance exceeds baseline,
    when proxy validity correlation drops below threshold, when negative control
    estimates diverge from zero)
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
  - [75%] — A/B testing; continuous experimentation; when to experiment vs
    observe; Feasibility Constraints; sequential decision-making
- `msml610/lectures_source/Lesson08.1-Causal_AI_intro.txt`
  - [35%] — Step 7: Preparing for Deployment in Business; Feedback Loops;
    Distribution Shift
- `msml610/lectures_source/Lesson08.4.txt`
  - [25%] — Effect heterogeneity and subgroup analysis
- `msml610/lectures_source/Lesson09.3-Multi_Armed_Bandits.txt`
  - [30%] — Exploration vs Exploitation; Sequential Decision-Making
- Gap: Assumption monitoring operationalization (dashboards, metrics); cost-aware rollout strategy depth; model versioning/error budgets; technical debt frameworks; production monitoring architecture; failure detection systems
- Missing: Concrete monitoring dashboard specs; rollback decision protocols

### Tutorials

## 17: Trust, Explainability, Fairness, and Governance

### Topics
- Building trust: transparency, stakeholder alignment, and justified confidence
  in causal decisions
- Causal vs. statistical explainability: distinguishing mechanisms (do-calculus,
  SCM) from attribution (SHAP, LIME, permutation importance)
  - Causal explainability tools and answers: "Why did we intervene?" via causal
    mechanisms (backdoor/frontdoor adjustment paths), mediation analysis (direct
    vs. indirect effects), counterfactual reasoning (what if we had intervened
    differently?), and SCM-based decision explanations
  - Statistical explainability tools and answers: "What features correlated with
    this decision?" (SHAP, LIME, permutation importance); risk: features may be
    confounders or colliders, not causal levers; can mislead stakeholders about
    what they can actually change
  - Operational risk: high statistical importance + low causal relevance (e.g.,
    a confounding variable ranked high by SHAP but not actionable), or vice versa
- Operationalizing causal explainability in production: decision explanations at
  serve-time, contrast with feature importance
- Identifying failure modes in production: when decisions fail and why at runtime
  (model misspecification becoming evident, distribution shift, causal assumption
  breakdown, unexpected feedback loops); differs from Ch16 assumption monitoring
  in scope (early detection vs. post-facto diagnosis) and remediation (emergency
  rollback vs. controlled re-calibration)
- Fairness under deployment: preventing disparate impact, fairness monitoring
  across subgroups, heterogeneous decision effects
- Override procedures and human-in-the-loop: escalation mechanisms, decision
  disputes, and when to trust vs. challenge the system
- Failure mode detection and response: monitoring, alerting, root cause analysis,
  and remediation
- Decision governance and audit trails: who approved what, when assumptions
  broke, what was the impact, and institutional accountability
- Regulatory and compliance alignment: overview of regulatory landscape (GDPR,
  EU AI Act, fairness certifications) and engineer accountability; focus on
  documentation requirements (causal assumptions, deployment decisions, override
  logs), audit trails for decisions, and when to involve compliance/legal teams
  rather than deep regulatory expertise
- Guardrails and safety constraints: preventing harmful behaviors, maintaining
  causal assumptions, and safeguarding against edge cases

### TODO

### Lessons
- `msml610/lectures_source/Lesson13.1-Explainability.txt`
  - [80%] — SHAP; LIME; permutation importance; counterfactual explanations; Causal AI and Explainability; Quality/Faithfulness/Stability of Explanations
- `msml610/lectures_source/Lesson15.1-Causal_Reasoning_Agents.txt`
  - [75%] — Trustworthy AI Through Causality; Transparency/Robustness/Fairness/Safety; guardrails; human oversight; causal guardrails
- `msml610/lectures_source/Lesson08.1-Causal_AI_intro.txt`
  - [25%] — Importance of Explainability; Approaches to Explainability; Why Organizations Fail
- `msml610/lectures_source/Lesson08.4.txt`
  - [20%] — Effect heterogeneity and fairness implications
- Gap: Operational causal explainability (serve-time implementations); deep fairness monitoring systems; regulatory compliance architecture; governance frameworks; override protocols; root-cause analysis for failures; audit trail design
- Missing: Governance/compliance depth; regulatory landscape specifics; failure-response playbooks

### Tutorials

# Appendix
