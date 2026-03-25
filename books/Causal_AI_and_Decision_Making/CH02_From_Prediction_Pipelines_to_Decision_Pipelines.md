# From Prediction Pipelines to Decision Pipelines
// Lesson02.2-ML_Paradigms.txt

## How Production ML Systems Make Decisions Today
- Most modern machine learning systems are organized as **prediction pipelines**
  - Break a complex problem into sub-problems
  - Solve each sub-problem independently with a specialized model
  - Chain solutions together to produce a final output
  - E.g., an OCR pipeline: text detection -> character segmentation -> character
    classification -> spelling correction

- The key insight driving pipeline design is **decomposition**:

  $$
  p_{\text{system}} = \sum_i p_i \cdot \alpha_i
  $$

  where $p_i$ is the performance of each stage and $\alpha_i$ is its relative
  importance to the overall system

- In practice, production ML systems follow a structured flow:
  - **Question**: Precisely define the prediction target
    - Bad: "How can we improve sales?"
    - Good: "What factors most significantly impact sales of product X in region
      Y during season Z?"
  - **Input data**: Collect labeled examples specific to the prediction goal
    - Training distribution should match the deployment distribution
  - **Features**: Engineer high-level representations from raw inputs
    - Good features compress information, retain relevance, and encode domain
      knowledge
  - **Algorithm**: Choose a model that balances accuracy, interpretability,
    speed, and scalability
  - **Evaluation**: Measure performance on held-out data using task-appropriate
    metrics

- The hierarchy matters:
  - Question $>$ Data $>$ Features $>$ Algorithm
  - Practitioners commonly over-invest in model selection while under-investing
    in problem formulation and data quality

- **Production decisions are implicit, not explicit**
  - A fraud detection model outputs a probability score
  - A business rule (threshold, policy) converts the score into an action
  - This separation is often unexamined and poorly audited
  - The pipeline predicts; the decision layer acts - but the decision layer is
    rarely modeled as rigorously as the prediction layer

### How Production ML Systems Make Decisions Today
- Burkov, A. _The Hundred-Page Machine Learning Book_ (2019)
  - Accessible overview of supervised, unsupervised, and reinforcement learning
    paradigms with emphasis on practical pipeline organization
- Russell, S. and Norvig, P. _Artificial Intelligence: A Modern Approach_ (4th
  ed., 2020)
  - Chapter 18-19 on learning agents and building ML pipelines
- Hastie, T., Tibshirani, R., and Friedman, J. _The Elements of Statistical
  Learning_ (2nd ed., 2009)
  - Chapter 7 on model assessment and selection, foundational for understanding
    pipeline evaluation

## Feedback Loops and Distribution Shift
- Production ML systems do not operate in a static world
  - The data-generating process changes over time
  - The model itself changes the world it is trying to predict

- **Distribution shift** occurs when the deployment distribution diverges from
  the training distribution
  - **Covariate shift**: inputs $X$ change but $P(Y|X)$ stays the same
    - E.g., a churn model trained on 2019 customer behavior fails after a
      product redesign changes user engagement patterns
  - **Label shift**: the class distribution $P(Y)$ changes
    - E.g., fraud rates spike after a new attack vector emerges
  - **Concept drift**: the underlying relationship $P(Y|X)$ changes
    - E.g., a credit scoring model built before a recession becomes unreliable
      as economic conditions redefine creditworthiness

- **Feedback loops** arise when model outputs influence future inputs
  - **Performative feedback**: the model's recommendations change behavior,
    which changes the distribution the model was trained on
    - E.g., a recommendation system that promotes content generates new
      engagement data biased toward its own prior choices
  - **Positive feedback loops** amplify existing patterns and can entrench bias
    - E.g., a hiring model trained on historical hires perpetuates historical
      biases if hiring decisions feed back into training data
  - **Negative feedback loops** can destabilize predictions
    - E.g., an ad bidding model that raises prices causes competitors to adjust,
      changing the equilibrium the model assumed

- The pipeline metaphor breaks down in dynamic environments
  - Static pipelines assume the world is fixed
  - Real systems are **closed-loop**: the pipeline output affects the input
    distribution
  - Ignoring this leads to silent model degradation, often undetected until
    downstream harm occurs

- Mitigating distribution shift requires:
  - Monitoring input and output distributions continuously
  - Designing retraining schedules that account for concept drift
  - Building causal models that separate stable relationships from unstable
    correlations

### Feedback Loops and Distribution Shift
- Quionero-Candela, J. et al. _Dataset Shift in Machine Learning_ (2009)
  - Comprehensive treatment of covariate shift, label shift, and concept drift
- Sculley, D. et al. "Hidden Technical Debt in Machine Learning Systems"
  (NeurIPS 2015)
  - Production ML failures including feedback loop and distribution shift
    failure modes
- Lazer, D. et al. "The Parable of Google Flu: Traps in Big Data Analysis"
  _Science_ (2014)
  - Case study of distribution shift and spurious correlation at scale

## Optimization Vs. Inference Vs. Decision Theory
- Production ML conflates three conceptually distinct tasks:
  1. **Inference**: estimating a quantity from data
     - E.g., "What is the probability this customer churns?"
  2. **Optimization**: finding the best action according to a fixed objective
     - E.g., "Which pricing strategy maximizes expected revenue this quarter?"
  3. **Decision-making**: choosing actions under uncertainty while accounting
     for consequences, preferences, and constraints
     - E.g., "Given uncertainty about customer sensitivity, what pricing
       strategy should we adopt to balance revenue and retention risk?"

- **Inference** is what ML models do best
  - Supervised learning estimates $P(Y|X)$ from data
  - The model does not take actions; it produces probability estimates
  - Inference does not require specifying what to do with the estimate

- **Optimization** applies a fixed objective to the inference output
  - E.g., pick the action $a$ that maximizes expected reward $\mathbb{E}[R|a]$
  - Requires a well-defined, single objective
  - Brittle when objectives are multi-dimensional or contested
  - Does not account for long-term consequences or unintended side effects

- **Decision theory** provides a principled framework for action under
  uncertainty
  - Explicitly models:
    - States of the world
    - Possible actions
    - Outcomes (payoffs) as a function of actions and states
    - Probability distributions over states
  - Maximizes **expected utility**: $\mathbb{E}[U(outcome)|action]$
  - Handles multi-objective tradeoffs through utility functions or Pareto
    analysis

- Most production systems are implicitly optimization systems with inference
  sub-components
  - They lack explicit models of outcomes, utilities, or downstream effects
  - Decision theory reveals what is missing: a causal model connecting actions
    to outcomes

- Reinforcement learning sits at the intersection of all three
  - Learn policy $\pi(s) \to a$ that maximizes cumulative reward
  - Requires an explicit reward signal - which is itself a design choice
  - E.g., AlphaGo (game playing), data center cooling, treatment planning in
    healthcare

## The Cost of Ignoring Causality: Concrete Failure Modes
- **Spurious correlation** - The model learns associations that do not hold
  under intervention
  - E.g., Google Flu Trends predicted flu prevalence from search queries but
    failed catastrophically in 2012-2013 because the query-flu correlation broke
    when search behavior changed independently of flu rates
  - The model had no causal model of why certain queries correlated with flu; it
    exploited a fragile association

- **Feedback-driven bias** - The model's predictions become self-fulfilling
  - E.g., a recidivism prediction model trained on arrest data learns patterns
    from policing decisions, not from underlying risk
  - Arresting more people in certain neighborhoods generates more training
    labels in those neighborhoods, reinforcing biased patterns

- **Policy failure from observational estimates** - A model trained on
  observational data gives the wrong answer to an intervention question
  - E.g., a model trained on historical ad exposure data shows that users who
    see more ads have higher purchase rates
  - Naively increasing ad exposure fails because the historical correlation
    reflects selection: high-intent users both see more ads and buy more, not
    because ads cause purchases
  - The intervention ("show more ads") changes the data-generating process; the
    observational model provides no valid guidance

- **Feature instability under distribution shift** - Features correlated with
  the target in training become uninformative or adversarial at deployment
  - E.g., in the Netflix Prize, ensemble models achieved state-of-the-art
    accuracy but were too slow and complex to deploy at scale
  - The pipeline optimized a proxy metric (prediction accuracy) rather than the
    actual deployment objective (scalable, robust recommendation)

- **Ceiling analysis blindness** - Without causal modeling, pipeline
  improvements may target the wrong stage
  - Ceiling analysis (mocking pipeline stages with oracles) identifies which
    stages bound performance
  - But ceiling analysis on a correlated pipeline can mislead: fixing one stage
    may not help if the bottleneck is a confounded input
  - E.g., improving character recognition accuracy in OCR may be irrelevant if
    text detection is confounded by image quality artifacts

- **Silent model failure** - Causally uninformed models fail silently
  - Accuracy metrics on held-out data look fine
  - Downstream business outcomes degrade
  - The gap between predictive accuracy and decision quality is the cost of
    ignoring causality

### Optimization Vs. Inference Vs. Decision Theory
- Berger, J. O. _Statistical Decision Theory and Bayesian Analysis_ (2nd
  ed., 1985)
  - Foundational treatment of decision theory, expected utility, and Bayesian
    decision-making
- Sutton, R. S. and Barto, A. G. _Reinforcement Learning: An Introduction_ (2nd
  ed., 2018)
  - Definitive text on RL as a framework for sequential decision-making under
    uncertainty
- Manski, C. F. _Identification Problems in the Social Sciences_ (1995)
  - The gap between what inference can establish and what decisions require

## Data Science Vs. Decision Science
- **Data Science** focuses on extracting patterns from data
  - Core questions: "What happened?", "What is likely to happen?"
  - Tools: statistics, ML, visualization, data engineering
  - Output: predictions, summaries, scores, dashboards
  - Implicitly assumes the world is fixed and the analyst is a passive observer

- **Decision Science** focuses on choosing actions that produce desired outcomes
  - Core questions: "What should we do?", "What would happen if we did X?"
  - Tools: causal inference, decision theory, optimization, experiment design
  - Output: actionable recommendations, policies, intervention strategies
  - Explicitly models the analyst as an agent intervening in the world

- The distinction maps directly onto Pearl's Ladder of Causation:

  | Level              | Question                     | Examples                                                 |
  | :----------------- | :--------------------------- | :------------------------------------------------------- |
  | **Association**    | What correlates with Y?      | "Users who buy X also buy Y"                             |
  | **Intervention**   | What happens if we do X?     | "What if we lower the price?"                            |
  | **Counterfactual** | What would have happened if? | "Would this customer have churned without the discount?" |
  - Data Science mostly operates at Level 1 (association)
  - Decision Science requires Level 2 (intervention) and Level 3
    (counterfactual)

- In practice, the gap between Data Science and Decision Science is the gap
  between **prediction accuracy** and **decision quality**
  - A model can be highly accurate at predicting churn yet provide no useful
    guidance on which intervention will reduce churn
  - A model can correctly identify that ice cream sales correlate with drowning
    rates without providing any insight into how to reduce drowning

- **Decision pipelines** extend prediction pipelines by adding:
  - An explicit action space: "What can we do?"
  - A causal model: "How do actions cause outcomes?"
  - A utility function: "What outcomes do we value and how much?"
  - An uncertainty model: "How confident are we in our causal estimates?"

- Building decision pipelines requires the discipline of **causal thinking**:
  - Distinguish observational from interventional quantities
  - Identify confounders that bias action-outcome estimates
  - Design experiments when observational data is insufficient
  - Use counterfactual reasoning to evaluate policies retrospectively

### Data Science Vs. Decision Science
- Pearl, J. _Causality: Models, Reasoning, and Inference_ (2nd ed., 2009)
  - Formal treatment of Pearl's Ladder of Causation and the distinction between
    associational and interventional reasoning
- Hernán, M. A. and Robins, J. M. _Causal Inference: What If_ (2020)
  - Rigorous treatment of the gap between observational data and causal
    decision-making in epidemiology and beyond
- Spirtes, P., Glymour, C., and Scheines, R. _Causation, Prediction, and Search_
  (2nd ed., 2000)
  - Foundational text on causal discovery and the role of causal structure in
    building decision-relevant models

## TUTORIAL: Pgmpy (Bayesian Decision Networks and Decision Pipeline Modeling)
