# Summary

## Title
- From Data to Decisions: Building Decision Systems with Probabilistic Causal
  Reasoning

- Reasoning under Uncertainty: Causal Machine Learning for Decision Making

## Target audience
- Senior ML engineers and data scientists with a statistics and probabilistic ML
  background who build production decision systems
- Working knowledge of causal basics (DAGs, SCMs, do-calculus) assumed

## Short TOC
- The sequence of the parts in the books are:
  - Motivation
    - 01. Why Decisions, Not Predictions
    - 02. The Cost of Ignoring Causality
    - 03. The Cost of Ignoring Uncertainty
  - Advanced Modeling Theory & Tools
    - 04. Knowledge Representation
    - 05. Probalistic ML
    - 06. Causal ML
  - Data
    - 07. Building Causal Knowledge
    - 08. Causal data pipelines
      - Selection Bias
        - How data collection processes bias what you observe
        - Missing data mechanisms (MCAR, MAR, MNAR)
        - Biases introduced by how samples were selected
      - Distribution Shift
        - Training vs. production data distribution mismatch
        - Covariate shift, label shift, and concept drift
        - Detecting and mitigating distribution changes
  - Decision-Making Theory & Tools
    - 09. Decision Theory Foundations
    - 10. Taxonomy of Decision-Making Problems and Algorithms
    - 11. Simple Decisions
    - 12. Complex Decisions
    - 13. Agentic Causal Reasoning
  - Implementation, Deployment, & Governance
    - 14. Building Stakeholder Alignment
    - 15. Deployment, Monitoring, and Adaptation
    - 16. Trust, Explainability, Fairness, and Governance

# Detailed TOC

# Part I: Why Businesses Need Decisions, not Predictions (Motivation)

## 1: Why Decisions, Not Predictions

### Topics
- Course Roadmap: the decision pipeline ($data \to model \to policy \to action
  \to feedback$) and five-part structure
- Why Traditional ML Falls Short: four critical gaps (causality, uncertainty,
  business objective, dynamics)
- From Data Science to Decision Science: predictive vs. decision-making paradigms
- Causal vs Predictive Questions: predictive form vs. causal form of business
  questions
- The Analytics Maturity Ladder: from descriptive (level 0) through predictive
  (level 1), causal (level 2), to decision (level 3)

## 2: The Cost of Ignoring Causality

### Topics
- When Correlation Misleads
  - Correlation encodes confounding as causation: $\Pr(Y | X) \neq \Pr(Y |
    do(X))$
  - Missing interventions and counterfactuals: observational models cannot answer
    "what if?" questions
  - Selection bias and the missing counterfactual: incomplete populations in
    historical data
- Structural Failure Modes
  - Interference and spillovers across units: SUTVA violations in marketplaces
    and networks
  - Simpson's Paradox: when aggregates reverse while subgroups show consistent
    effects
  - Collider bias: conditioning creates illusions (Berkson's paradox)
  - Discarding domain knowledge and mechanism: pattern-driven models inherit
    training data artifacts

## 3: The Cost of Ignoring Uncertainty

### Topics
- Point Estimates in a Small-Data World
  - Point estimates without error bars: single numbers hide decision-relevant
    variance
  - Epistemic vs aleatoric uncertainty conflated: inability to detect
    out-of-distribution inputs
  - No abstention: systems that never say "I don't know" are overconfident
    off-distribution
  - Overfitting and statistical significance traps: peeking, multiple
    comparisons, burned test sets

# Part II: Data

## 4: Building Causal Knowledge

### Topics
- Eliciting causal knowledge from domain experts: structured methods, expert
  judgment, and iterative refinement
- Building causal DAGs: variable selection, causal assumptions, and graph
  construction from domain knowledge
- Variable types and relationships: confounders, mediators, colliders,
  moderators, and their roles in causal inference
- Temporal structure in causal systems: causal order, feedback delays, causal
  acyclicity, and dynamic relationships
- Measurement and operationalization: defining variables, measurement validity,
  proxy variables for latent constructs
- Documenting causal assumptions: transparency, validation, and stakeholder
  alignment on causal structures

## 5: Causal Data Pipelines

### Topics
- Data collection and its biases: how collection processes introduce selection
  bias and confounding
- Selection bias and incomplete populations: missing data mechanisms (MCAR, MAR,
  MNAR) and their impact on causal inference
- Distribution shift and covariate mismatch: training vs. production misalignment,
  concept drift, and environment shifts
- Measurement error and proxy validity: assessing proxy variable quality,
  attenuation in causal effects, and measurement error correction
- Pre-flight checks: validating data quality, assessing confounder balance,
  checking assumptions before causal modeling
- Data quality for causal inference: handling missingness, outliers, and data
  anomalies in causal analysis

# Part III: Advanced Modeling Theory & Tools

## 6: Knowledge Representation

### Topics
- Causal DAGs vs. Bayesian networks: how causality orients edges and encodes
  independence
- Structural equations and mechanisms: modeling causal relationships, functional
  forms, and how variables depend on parents
- Causal assumptions and identifiability: what assumptions enable causal
  inference (consistency, SUTVA, no unmeasured confounding)
- D-separation and graphical criteria: reading independence from DAG structure,
  backdoor/frontdoor criteria for adjustment
- Structural causal models (SCMs): formal representation of causal mechanisms
  and counterfactual reasoning
- Causal invariance and modularity: which causal relationships persist across
  environments and why

## 7: Probabilistic ML

### Topics
- Bayesian inference fundamentals: posterior updating, conjugate priors, and
  probabilistic decision-making
- Uncertainty quantification: epistemic vs. aleatoric uncertainty, confidence
  intervals, and posterior predictive distributions
- Generative models and latent variables: topic models, mixture models, and
  disentangled representations
- Approximate inference: variational inference, Markov Chain Monte Carlo (MCMC),
  expectation-propagation
- Graphical models: factor graphs, belief propagation, and message-passing
  algorithms
- Modern probabilistic programming: probabilistic languages and tools for
  building uncertainty-aware systems

## 8: Causal ML

### Topics
- Causal discovery from data: when and how to learn causal structure from
  observational data
- Discovery algorithms: constraint-based (PC/FCI), score-based (GES), functional
  (LiNGAM, ANM)
- Identifiability and Markov equivalence: what can and cannot be learned from
  observational data
- Latent confounders and hidden variables: proxy variables, negative controls,
  sensitivity analysis, and incomplete adjustment
- Causal representation learning: disentangling mechanisms for domain transfer
  and generalization across environments
- Robustness and sensitivity: E-values, bounding unmeasured confounding, and
  partial identification

# Part IV: Decision-Making Theory & Tools

## 10: Decision Theory Foundations

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

## 11: Taxonomy of Decision-Making

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

## 12: Simple Decisions

### Topics
- Heterogeneous treatment effects and CATE: learning who benefits from treatment
- Doubly robust estimation and double/debiased ML: reducing sensitivity to
  nuisance parameters
- Meta-learners for heterogeneity: T-, S-, X-, R-learners and when to use each
- Distributional and quantile effects: going beyond average treatment effects
- Off-policy learning and policy optimization: evaluating and improving policies
  from data
- Safe policy improvement: deployable decisions with finite-sample guarantees

## 13: Complex Decisions

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
- Markov decision processes and multi-step planning: states, actions, transitions,
  and solving with value/policy iteration
- Causal world models as environment dynamics: planning, counterfactual rollouts,
  and policy search

## 14: Agentic Causal Reasoning

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
- Performativity and adaptive systems: decisions that change the world, feedback
  loops, and learning from outcomes
- Online causal discovery: learning and revising causal models from deployment
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
