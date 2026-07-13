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

## 5: Advanced Probabilistic ML

### Topics
- Short summary from Lesson6*

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

# Appendix
