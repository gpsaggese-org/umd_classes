# Book Map

data → causal model → effect estimation → policy → action → feedback

The book walks this end-to-end across five parts:

Part I: Why Businesses Need Decisions, not Predictions: why organizations fail with good data and need decisions, not predictions
Part II: Advanced Tools & Theory: the advanced probabilistic and causal foundations required to model real systems, including Gaussian processes, variational inference, normalizing flows, and modern causal discovery
Part III: Single-Step Decisions: single-step decisions, covering decision theory, policy learning, partial identification, and agentic causal reasoning
Part IV: Multi-Step & Dynamic Decisions: multi-step and dynamic decisions, covering causal world models, causal reinforcement learning, forecasting under intervention, and feedback loops
Part V: Implementation: the implementation concerns of deploying, monitoring, communicating, and governing decision systems in production

// TODO(ai_gp): Add a hint of a solution using causal and probabilistic
// machine learning
// From Data Science vs. Decision Science

* Limitations of Traditional Machine Learning in Business Setups

- **Traditional ML relies on correlation**: it learns $\Pr(Y | X)$ from
  historical data
  - Answers _"what will happen?"_, not _"what should we do?"_
  - Optimized for predictive accuracy, not decision quality

- **Confounding is encoded as causation**
  - A hidden common cause makes $X$ and $Y$ correlate spuriously
  - $\Pr(Y | X) \neq \Pr(Y | do(X))$; acting on correlations backfires

- **No interventions or counterfactuals**
  - Cannot answer _"if we change $X$, what happens to $Y$?"_
  - Cannot reason about _"what would have happened otherwise?"_

- **Assumes a static world**
  - Any decision changes the world, breaking the training distribution
  - Concept, covariate, and label shift degrade accuracy over time

- **Ignores feedback loops**
  - Predictions act on the world and reshape future data
  - Leads to bias amplification (echo chambers, over-policing)

- **Lack of assessing uncertainty**
  - Most problems are "small data" problems

* Limitations of Traditional Machine Learning in Business Setups (cont.)

- **Optimizes the wrong objective**
  - Models chase a proxy metric (clicks, accuracy) instead of the actual
    business goal (revenue, retention, wellbeing)
  - _Goodhart's Law_: once a proxy becomes a target, it stops measuring what you
    care about

- **Selection bias baked into the training data**
  - Historical data only reflects decisions actually made — loan data shows
    outcomes for approved applicants, never rejected ones
  - A missing-counterfactual problem present _before_ modeling starts, distinct
    from confounding

- **Simpson's paradox as a concrete failure mode**
  - Aggregate trends can reverse when split by subgroup (or vice versa)
  - A model can look correct overall yet be wrong — or harmful — for every
    segment

- **No native cost-asymmetry handling**
  - Standard losses (log-loss, MSE) treat errors symmetrically
  - Business errors are not: a fraud false negative costs differently than a
    false positive; requires cost matrices bolted on after the fact

- **Strategic / adversarial response unmodeled**
  - Once deployed, people optimize against the model (credit gaming, SEO, resume
    keyword-stuffing)
  - Traditional ML assumes passive agents; in business, they are not

- **Black-box outputs aren't actionable or auditable**
  - A prediction is not a recommendation — it says no _why_, no lever to pull
  - Credit, hiring, healthcare increasingly require explanations, not just scores

- **Lack of end-to-end learning**
  - Problems are split into smaller problems and solved individually
  - Learning end-to-end has shown to 

- **Overfitting**
  - Statistical significance traps: peeking, multiple comparisons, and novelty effects
  - Not only in one single run, but from buring the "test set"
  - Lack of assumptions doesn't limit the fit (prior)

# Chapters

## 1: From Prediction Pipelines to Decision Pipelines

### Topics
- Prediction vs. decision: fundamentally different mathematical problems (traditional ML relies on correlation)
- Correlation-based ML encodes confounding as causation: Pr(Y | X) ≠ Pr(Y | do(X)), so acting on correlations backfires
- No interventions or counterfactuals, and the ladder of causation: observation, intervention, and counterfactual reasoning
- Simpson's paradox and policy reversals: why predictive accuracy fails in decisions
- Predictions are not recommendations: black-box scores give no actionable lever or "why"
- The decision pipeline: from causal models to utility-maximizing actions
- Causal models as the foundation for decision-making
- Why organizations fail: the cost of ignoring causality in data-driven systems

## 2: Why Good Data Leads to Bad Decisions

### Topics
- Statistical significance traps and overfitting: peeking, multiple comparisons, novelty effects, and burning the test set
- Heterogeneous treatment effects: when average effects mask sub-group reversals
- Confounding in causal ML: biases when causal assumptions are unmet
- Selection bias and the missing-counterfactual problem: data reflects only decisions actually made (e.g., approved loans)
- Feedback loops: how predictions change the world and break model assumptions
- Strategic and adversarial response: deployed models get gamed (credit gaming, SEO), violating passive-agent assumptions
- Distribution shift and causal assumptions under intervention
- Decision readiness under uncertainty: knowing when causal claims are safe to act on, especially in small-data regimes

## 3: ?

### Topics
- From KPI selection to causal objectives and utilities: avoiding Goodhart's law when a proxy becomes the target
- Cost-asymmetry in decisions: why symmetric losses (log-loss, MSE) misprice asymmetric business errors
- Building causal DAGs: variable identification, temporal structure, and domain knowledge
- Intervention design: choosing levers, targets, scales, and timing
- Causal variable types: confounders, mediators, colliders, and their adjustment rules
- Identifiability and causal assumptions: backdoor, frontdoor, and IV conditions
- End-to-end decision framing vs. splitting into individually-solved sub-problems
- Data collection strategy aligned with causal identification requirements

