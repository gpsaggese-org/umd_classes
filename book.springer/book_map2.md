# Content

**Title**:
- From Data to Decisions: Building Decision Systems with Probabilistic Causal
  Reasoning

- Reasoning under Uncertainty: Causal Machine Learning for Decision Making

**Target audience:**
- Senior ML engineers and data scientists with a statistics and probabilistic ML
  background who build production decision systems
- Working knowledge of causal basics (DAGs, SCMs, do-calculus) assumed

## From Predictions to Decisions

- The book is organized 
  - data → causal model → effect estimation → policy → action → feedback

- The book walks this end-to-end across five parts:

- Part I: Why Businesses Need Decisions, not Predictions
  - The limitations and costs of current machine learning

- Part II: Advanced Tools & Theory: the advanced probabilistic and causal
  foundations required to model real systems, including Gaussian processes,
  variational inference, normalizing flows, and modern causal discovery

- Part III: Single-Step Decisions: single-step decisions, covering decision
  theory, policy learning, partial identification, and agentic causal reasoning

- Part IV: Multi-Step & Dynamic Decisions: multi-step and dynamic decisions,
  covering causal world models, causal reinforcement learning, forecasting under
  intervention, and feedback loops

- Part V: Implementation: the implementation concerns of deploying, monitoring,
  communicating, and governing decision systems in production

// TODO(ai_gp): Add a hint of a solution using causal and probabilistic
// machine learning
// From Data Science vs. Decision Science

* Limitations of Traditional ML in Business

1. Ignoring causality
   - Modeling correlation, not mechanisms

2. Ignoring uncertainty
   - No uncertainty quantification (especially on "small data" problem)

3. Ignoring the business objective
   - A prediction is not a decision

4. Ignoring dynamics
   - The world isn't static or passive, but it reacts

* The Cost of Ignoring Causality

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

- **Interference / spillovers (SUTVA violation)**
  - One unit's action changes another's outcome — marketplaces, pricing
    equilibria, social networks
  - Pervasive in business, yet standard ML assumes units are independent

- **Selection bias baked into the training data**
  - Historical data only reflects decisions actually made — loan data shows
    outcomes for approved applicants, never rejected ones
  - A missing-counterfactual problem present _before_ modeling starts, distinct
    from confounding

- **Simpson's paradox as a concrete failure mode**
  - Aggregate trends can reverse when split by subgroup (or vice versa)
  - A model can look correct overall yet be wrong — or harmful — for every
    segment

- **Collider bias / Berkson's paradox**
  - Conditioning on a common effect induces a spurious association
  - Another concrete failure mode alongside Simpson's paradox

- **Ignoring domain knowledge / mechanism**
  - Pure ML discards known structure (physics, economics, the causal graph)
  - No principled way to inject constraints or priors

* The Cost of Ignoring Uncertainty

- **Lack of assessing uncertainty**
  - Most problems are "small data" problems

- **Epistemic vs. aleatoric uncertainty conflated**
  - No "known-unknowns": the model cannot flag what it has not seen
  - Confidently wrong off-distribution — exactly where decisions bite

- **No abstention or deferral**
  - Cannot say _"I don't know"_ and route the case to a human

- **Overfitting**
  - Statistical significance traps: peeking, multiple comparisons, and novelty effects
  - Not only in one single run, but from burning the "test set"
  - Lack of assumptions doesn't limit the fit (prior)

* The Cost of Ignoring the Business Objective

- **Optimizes the wrong objective**
  - Models chase a proxy metric (clicks, accuracy) instead of the actual
    business goal (revenue, retention, wellbeing)
  - _Goodhart's Law_: once a proxy becomes a target, it stops measuring what you
    care about

- **No native cost-asymmetry handling**
  - Standard losses (log-loss, MSE) treat errors symmetrically
  - Business errors are not: a fraud false negative costs differently than a
    false positive; requires cost matrices bolted on after the fact

- **Multi-objective decisions under constraints**
  - Real decisions trade off competing goals under budget, capacity, and legal
    limits
  - A single scalar loss cannot express constrained, multi-stakeholder trade-offs

- **Black-box outputs aren't actionable or auditable**
  - A prediction is not a recommendation — it says no _why_, no lever to pull
  - Credit, hiring, healthcare increasingly require explanations, not just scores

- **Lack of end-to-end learning**
  - Problems are split into smaller problems and solved individually
  - Learning end-to-end has shown to

* The Cost of Ignoring Dynamics and Feedback

- **Assumes a static world**
  - Any decision changes the world, breaking the training distribution
  - Concept, covariate, and label shift degrade accuracy over time

- **Ignores feedback loops**
  - Predictions act on the world and reshape future data
  - Leads to bias amplification (echo chambers, over-policing)

- **Performativity**
  - The prediction changes the very quantity it predicts
  - A sharper, named form of feedback loops

- **No exploration (observational-only)**
  - The model never experiments; it is trapped in the support of the logged
    policy
  - Cannot learn the effect of never-taken actions (an overlap / positivity
    violation)

- **Delayed and long-horizon effects**
  - Optimizes an immediate proxy, ignoring downstream outcomes
  - No credit assignment over time (short-termism, surrogate outcomes)

- **Strategic / adversarial response unmodeled**
  - Once deployed, people optimize against the model (credit gaming, SEO, resume
    keyword-stuffing)
  - Traditional ML assumes passive agents; in business, they are not

## 1: Ignoring Causality and Uncertainty

### The Problem
- **Prediction vs. decision are different mathematical problems**:
  - Traditional ML learns $\Pr(Y | X)$ to answer _"what will happen?"_
  - It is optimized for predictive accuracy, not for _"what should we do?"_ and
    decision quality
- **Correlation encodes confounding as causation**:
  - A hidden common cause makes $X$ and $Y$ correlate spuriously
  - $\Pr(Y | X) \neq \Pr(Y | do(X))$, so acting on correlations backfires
- **No interventions or counterfactuals**: correlation models cannot answer
  - _"if we change $X$, what happens to $Y$?"_
  - _"what would have happened otherwise?"_
- **Selection bias and the missing-counterfactual problem**:
  - Data reflects only decisions actually made — approved loans, never rejected
    ones
  - A problem present _before_ modeling starts, distinct from confounding
- **Simpson's paradox and policy reversals**:
  - Aggregate trends reverse by subgroup
  - A model correct overall can be wrong — or harmful — for every segment
- **Heterogeneous treatment effects**: average effects mask sub-group reversals
- **Interference / spillovers (SUTVA violation)**:
  - One unit's action changes another's outcome — marketplaces, pricing
    equilibria, social networks
  - Standard ML assumes independent units; business rarely obliges
- **Collider bias / Berkson's paradox**: conditioning on a common effect induces
  a spurious association — a concrete failure mode alongside Simpson's
- **Ignoring domain knowledge / mechanism**: pure ML discards known structure,
  with no principled way to inject constraints or priors

### Toward a Solution (Causal Modeling)
- **The ladder of causation**: observation, intervention, and counterfactual
  reasoning as distinct rungs
- **Building causal DAGs**: variable identification, temporal structure, and
  domain knowledge
- **Causal variable types**: confounders, mediators, colliders, and their
  adjustment rules
- **Identifiability and causal assumptions**: backdoor, frontdoor, and
  instrumental-variable conditions
- **Intervention design**: choosing levers, targets, scales, and timing
- **Data collection strategy** aligned with causal identification requirements
- **Assumptions are not free**: causal estimates are biased when identification
  assumptions (ignorability, positivity) are unmet
- **Causal models as the foundation** for utility-maximizing decisions

### The Problem
- **No uncertainty quantification**: most problems are "small data" problems, yet
  models emit point estimates as if they were certain
- **Overfitting and statistical significance traps**:
  - Peeking, multiple comparisons, and novelty effects
  - Not only in a single run, but from burning the test set
  - Without assumptions (priors), nothing limits the fit
- **Epistemic vs. aleatoric uncertainty conflated**: no "known-unknowns", so the
  model is confidently wrong off-distribution — exactly where decisions bite
- **No abstention or deferral**: cannot say _"I don't know"_ and route the case
  to a human

### Toward a Solution (Probabilistic ML)
- **Posteriors over effects, not point estimates**: priors encode assumptions and
  regularize the "small data" regime
- **Probabilistic toolkit** (developed in Part II): Gaussian processes,
  variational inference, and normalizing flows
- **Decision readiness under uncertainty**: knowing when causal claims are safe to
  act on

## 3: Ignoring the Business Objective and Real-World Dynamics

### The Problem
- **Optimizes the wrong objective**:
  - Models chase a proxy (clicks, accuracy) instead of the business goal
    (revenue, retention, wellbeing)
  - _Goodhart's law_: once a proxy becomes the target, it stops measuring what
    you care about
- **No native cost-asymmetry handling**:
  - Symmetric losses (log-loss, MSE) misprice asymmetric business errors
  - A fraud false negative costs differently than a false positive
- **Predictions are not recommendations**:
  - Black-box scores give no actionable lever and no _"why"_
  - Credit, hiring, and healthcare increasingly require explanations, not just
    scores
- **No end-to-end learning**: splitting a problem into individually-solved
  sub-problems loses the joint objective
- **Multi-objective decisions under constraints**: real decisions trade off
  competing goals under budget, capacity, and legal limits — not one scalar loss

### Toward a Solution (Decision Theory)
- **From KPIs to causal objectives and utilities**: optimize the decision, not a
  proxy metric
- **Cost matrices and asymmetric loss**: price business errors explicitly instead
  of bolting fixes on after the fact
- **The decision pipeline**: data → causal model → effect estimation → policy →
  action → feedback
- **End-to-end, decision-focused learning**: optimize the whole pipeline for
  decision quality

### The Problem
- **Assumes a static world**:
  - Any decision changes the world and breaks the training distribution
  - Concept, covariate, and label shift degrade accuracy over time
- **Feedback loops**: predictions act on the world and reshape future data,
  amplifying bias (echo chambers, over-policing)
- **Strategic and adversarial response**:
  - Deployed models get gamed (credit gaming, SEO, resume keyword-stuffing)
  - This violates the passive-agent assumption
- **Performativity**: the prediction changes the very quantity it predicts — a
  sharper, named form of feedback loops
- **No exploration (observational-only)**:
  - The model never experiments; it is trapped in the support of the logged
    policy
  - Cannot learn the effect of never-taken actions (an overlap / positivity
    violation)
- **Delayed and long-horizon effects**: optimizes an immediate proxy, ignoring
  downstream outcomes and credit assignment over time (short-termism, surrogate
  outcomes)

### Toward a Solution (Dynamic Causal ML)
- **Model the world's response** (developed in Part IV): causal world models,
  causal reinforcement learning, and forecasting under intervention
- **Feedback-aware design**: anticipate distribution shift and bias amplification
  before deployment
