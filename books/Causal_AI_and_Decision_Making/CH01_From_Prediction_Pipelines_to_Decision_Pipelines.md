// Lesson08.1-Causal_AI_intro.txt

## What ML systems can and cannot tell you

- Traditional machine learning excels at **finding patterns** in historical data
  - Models learn statistical associations: "when X occurs, Y tends to follow"
  - This works well for prediction tasks where the future resembles the past
  - Examples: spam detection, image classification, demand forecasting

- But ML systems struggle with **why** questions and intervention scenarios
  - A model trained on observational data cannot answer: "What if we did X?"
  - Correlation-based models work by spotting regularities, not causal mechanisms
  - They generalize only to distributions similar to their training data

- The fundamental limitation: **data alone cannot tell you about causation**
  - Two variables may move together due to:
    - Direct causation (X causes Y)
    - Reverse causation (Y causes X)
    - A hidden confounder (Z causes both X and Y)
    - Pure coincidence
  - Without domain knowledge and causal reasoning, no amount of data can distinguish these cases

- ML models are "data first" systems
  - They accumulate data, clean it, engineer features, and fit patterns
  - The process treats all correlations equally
  - Bias in the data propagates directly into the model

- **Explainability without causality is theater**
  - A model can explain *what* it predicts without understanding *why*
  - Feature importance tells you which variables the model relied on, not whether those relationships are causal
  - Regulators want organizations to justify decisions, not just explain model outputs

**References**

- Pearl, J. and Mackenzie, D. _The Book of Why_ (2018)
  - Exposition of why machine learning's pattern-matching cannot substitute for causal reasoning
- Hurwitz, J. and Thompson, M. _Causal Artificial Intelligence_ (2024)
  - Discussion of limitations of correlation-based AI for decision-making
- Scholkopf, B. et al. "Toward Causal Representation Learning" _Journal of Machine Learning Research_ (2021)
  - Formal treatment of why current ML architectures are insufficient for causal inference

## Correlation, association, and the illusion of understanding

- **Association** is a statistical property: two variables move together
  - Humans naturally observe that X and Y co-occur and infer a relationship
  - Association is powerful for prediction but dangerous for decision-making

- **Humans are primed to mistake association for causation**
  - Example: You eat a particular food and get a stomachache several times
    - You infer: "This food is bad for me"
    - Reality: Maybe the food is fine, but you eat it when stressed, and stress causes the ache
  - Example: You buy a stock right before its price skyrockets
    - You infer: "I can time the market"
    - Reality: You got lucky, and overconfidence leads to riskier bets that eventually fail

- **Causation** is a mechanism: changing one variable directly influences another
  - You cannot conclude causation from correlation alone
  - You must understand the mechanism by which one variable influences another

- **Three reasons variables may correlate without causal connection**:
  - **Reverse causality**: Y causes X (not X causes Y)
    - Example: Does depression cause poor sleep, or does insomnia cause depression?
    - A correlational study cannot distinguish these
  - **Confounding**: A hidden third variable Z causes both X and Y
    - Example: Hotels charge high prices *and* have high occupancy during tourist season
      - Naive analysis: raising prices increases occupancy
      - Reality: demand (Z) causes both high prices and high occupancy
  - **Coincidence**: The correlation is spurious
    - Example: Nicolas Cage movies released per year correlates with swimming pool drownings
    - No mechanism connects them; the correlation is noise in large datasets

- **Data does not understand causes and effects**
  - Only humans can identify variables and relationships based on domain knowledge
  - Without causal reasoning, intelligent decision-making is impossible

- **The cost of ignoring causation**:
  - Decisions based on spurious correlations fail when conditions change
  - Interventions based on correlation often backfire
  - Example: Google Flu Trends predicted flu prevalence from search query patterns
    - The model was accurate on historical data
    - But when search behavior changed (media hype, algorithm changes), the model collapsed
    - The query-flu correlation was fragile; no causal understanding existed

**References**

- Pearl, J. _Causality: Models, Reasoning, and Inference_ (2nd ed., 2009)
  - Formal definitions of association, causation, and confounding
- Angrist, J. D. and Pischke, J.-S. _Mostly Harmless Econometrics_ (2009)
  - Practical treatment of confounding and how to identify causal relationships from data
- Lazar, D. et al. "The Parable of Google Flu: Traps in Big Data Analysis" _Science_ (2014)
  - Case study of spurious correlation and distribution shift at scale

## Three kinds of questions: association, intervention, counterfactual (Pearl's ladder)

- Judea Pearl's **Ladder of Causation** distinguishes three types of questions
  - Each rung requires stronger reasoning than the one below
  - Most current AI operates only at the bottom rung

### Rung 1: Association (Observing)

- **Question**: "How would seeing X change our belief in Y?"
- **Mathematical notation**: $\Pr(Y|X)$ (the conditional probability of Y given X)
- **Activity**: Passive observation to determine whether X and Y are related

- This is what traditional AI and machine learning do best
  - The model observes correlations in data
  - It estimates conditional probabilities from labeled examples
  - Bayesian approaches formalize this as probability updates

- **Examples of association questions**:
  - "What symptom tells you about a disease?"
  - "What does a survey tell you about election results?"
  - "What customer features predict churn?"

- **Limitations**:
  - Association answers "what is?" not "what if?"
  - A model can be arbitrarily accurate at prediction yet provide no guidance for action

### Rung 2: Intervention (Doing)

- **Question**: "What happens to Y if you do X?" or "What if we intervened on X?"
- **Mathematical notation**: $\Pr(Y | do(X), Z)$ (the probability of Y if we intervene to set X, under conditions Z)
- **Activity**: Understanding the causal impact of an action on an outcome

- Interventions require a **causal model**: an explicit representation of mechanisms
  - You must understand not just that X and Y correlate, but *why*
  - You must know which confounders exist and account for them
  - You must distinguish correlation from causation

- **Examples of intervention questions**:
  - "If we lower prices by 10%, how many additional units will sell?"
  - "If we increase the credit line for a customer, what happens to default risk?"
  - "If we switch from a low-sugar diet to a low-fat diet, will health improve?"
  - "If we ban sodas in schools, will childhood obesity decline?"

- **Why observational data alone is insufficient**:
  - A model trained on historical prices and sales sees: lower prices correlate with higher volume
  - This reflects confounding: promotions lower prices and attract price-sensitive customers, both increasing volume
  - If you try to boost profit by raising prices (inverting the correlation), you fail because the causal direction runs the other way

### Rung 3: Counterfactuals (Imagining)

- **Question**: "Was X the reason Y occurred?" or "What would have happened if we had done differently?"
- **Mathematical notation**: $\Pr(Y_{X=x'} | X=x, Y=y')$ (the probability Y would have been different under a counterfactual scenario)
- **Activity**: Reasoning about alternative scenarios and causal attributions

- Counterfactual reasoning is the highest form of causal reasoning
  - You must understand not just mechanisms, but how they apply to specific individuals
  - It lets you answer "why?" about past events

- **Examples of counterfactual questions**:
  - "Was it the marketing campaign that caused the sales increase, or would sales have increased anyway?"
  - "Why did this particular customer churn? Would they have stayed if we had offered a discount?"
  - "Was it the drug that cured the patient, or would they have recovered on their own?"
  - "If this student had attended a different school, would their grades be different?"

- **Why counterfactuals matter for learning and improvement**:
  - You observe an outcome and want to explain it
  - Attribution matters: "did my action cause this, or would it have happened anyway?"
  - Without counterfactuals, you cannot learn from experience

**References**

- Pearl, J. _The Book of Why_ (2018)
  - Accessible exposition of the Ladder of Causation with examples
- Pearl, J. _Causality: Models, Reasoning, and Inference_ (2nd ed., 2009)
  - Formal mathematical treatment of association, intervention, and counterfactuals
- Hernán, M. A. and Robins, J. M. _Causal Inference: What If_ (2020)
  - Rigorous treatment of intervention and counterfactual reasoning in epidemiology and beyond

## A roadmap: from prediction to causal reasoning to decision intelligence

- The evolution of data and AI reflects increasing sophistication in answering business questions

- **Level 1: Descriptive Analytics** - "What happened?"
  - Tools: Summary statistics, historical reports, dashboards
  - Activity: Collect data, compute means, medians, aggregations
  - Value: Understanding past performance
  - Example: "Our revenue was $10M last quarter, down 5% from last year"

- **Level 2: Predictive Analytics** - "What will happen?"
  - Tools: Machine learning, statistical models, forecasting
  - Activity: Learn patterns from historical data and extrapolate
  - Value: Anticipating future outcomes under current conditions
  - Example: "We forecast 15% customer churn this quarter based on engagement patterns"

- **Level 3: Prescriptive Analytics** - "What should we do?"
  - Tools: Optimization, decision analysis, causal inference
  - Activity: Identify interventions that produce desired outcomes
  - Value: Actionable recommendations that improve outcomes
  - Example: "Offering a 10% discount to at-risk customers reduces churn by 20%"

- **Level 4: Decision Intelligence** - "What's the best we can do?"
  - Tools: Causal AI, reinforcement learning, simulation
  - Activity: Continuously learn and optimize decisions under uncertainty
  - Value: Sustained improvement through adaptive decision-making
  - Example: "Our AI recommends personalized offers for each customer that maximize lifetime value while accounting for inventory and competitive dynamics"

- **Why causal AI is the bridge between prediction and decision intelligence**:

- Traditional ML is a **"data-first" approach**
  - Accumulate data and let patterns speak for themselves
  - Strengths: Works well with abundant data, scales easily
  - Weaknesses: Spurious correlations, poor generalization to new conditions, no explainability

- Causal AI is a **"model-first" approach**
  - Start with the business question and domain knowledge
  - Build a causal model that represents mechanisms
  - Use data to estimate causal parameters, not just correlations
  - Strengths: Generalizes to interventions, interpretable, robust to distribution shift
  - Weaknesses: Requires domain expertise, more complex, less data-hungry

- **Causal AI process**:
  1. What is the intended outcome we want to achieve?
  2. What interventions are possible (which variables can we change)?
  3. What are the confounding factors (hidden causes that affect both outcomes and our choices)?
  4. What are the mediating factors (how do interventions affect outcomes)?
  5. Create a causal model (diagram or graph) representing mechanisms
  6. Collect data and estimate causal effects
  7. Design experiments or observational studies to validate causal assumptions
  8. Use causal estimates to inform decisions

- **ML is powerful but narrowly scoped**:
  - ML excels at prediction when training and deployment distributions are similar
  - ML fails at decision-making when you must reason about interventions not in the training data

- **The future of intelligent systems**:
  - Integrate predictive power of ML with causal reasoning
  - Use ML for estimation (learning from data)
  - Use causal graphs for reasoning (understanding mechanisms)
  - Use decision theory to choose actions (optimizing under uncertainty)

**References**

- Hurwitz, J. and Thompson, M. _Causal Artificial Intelligence_ (2024)
  - Overview of the evolution from analytics to causal AI
- Russell, S. and Norvig, P. _Artificial Intelligence: A Modern Approach_ (4th ed., 2020)
  - Chapter on learning agents and the limitations of purely associational systems
- Pearl, J. _The Book of Why_ (2018)
  - Why the next revolution in AI must be causal
- Pearl, J. and Mackenzie, D. _The Book of Why_ (2018)
  - The "three-table" representation of cause, effect, and confounding

## TUTORIAL: DoWhy (end-to-end causal reasoning from observational data)
# From Prediction Pipelines to Decision Pipelines
// Lesson02.2-ML_Paradigms.txt

## How Production ML Systems Make Decisions Today
- Most production ML systems are **prediction pipelines**
  - Break a complex problem into sub-problems
  - Solve each sub-problem independently with a specialized model
  - Chain solutions together to produce a final output
  - E.g., an OCR pipeline: text detection → character segmentation → character
    classification → spelling correction

- The key idea behind pipeline design is **decomposition**:

  $$
  p_{\text{system}} = \sum_i p_i \cdot \alpha_i
  $$

  where $p_i$ is the performance of each stage and $\alpha_i$ is its relative
  importance to the overall system

- Production ML systems follow a structured flow:
  - **Question**: Define the prediction target precisely
    - Bad: "How can we improve sales?"
    - Good: "What factors most significantly impact sales of product X in region
      Y during season Z?"
  - **Input data**: Collect labeled examples specific to the prediction goal
    - Training distribution should match the deployment distribution
  - **Features**: Engineer high-level representations from raw inputs
    - Good features compress information, preserve relevance, and encode domain
      knowledge
  - **Algorithm**: Choose a model that balances accuracy, interpretability,
    speed, and scalability
  - **Evaluation**: Measure performance on held-out data using task-appropriate
    metrics

- The hierarchy matters:
  - Question $>$ Data $>$ Features $>$ Algorithm
  - Teams usually over-invest in model selection while under-investing
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
  - Ignore this and the model degrades silently, often undetected until
    harm shows up downstream

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
  - The model produces probability estimates; it takes no actions
  - You don't need to specify what to do with the estimate

- **Optimization** applies a fixed objective to the inference output
  - E.g., pick the action $a$ that maximizes expected reward $\mathbb{E}[R|a]$
  - Requires a well-defined, single objective
  - Brittle when objectives are multi-dimensional or contested
  - Ignores long-term consequences and unintended side effects

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
    failed in 2012-2013 because the query-flu correlation broke when search
    behavior changed independently of flu rates
  - The model exploited a fragile association without understanding why certain
    queries correlated with flu

- **Feedback-driven bias** - The model's predictions become self-fulfilling
  - E.g., a recidivism prediction model trained on arrest data learns from
    policing decisions, not from underlying risk
  - When you arrest more people in certain neighborhoods, you generate more
    training labels in those neighborhoods, reinforcing bias

- **Policy failure from observational estimates** - A model trained on
  observational data gives the wrong answer to an intervention question
  - E.g., a model trained on historical ad exposure data shows that users who
    see more ads have higher purchase rates
  - If you increase ad exposure, it fails because the historical correlation
    reflects selection: high-intent users see more ads and buy more, not
    because ads cause purchases
  - The intervention ("show more ads") changes the data-generating process; the
    observational model can't guide you

- **Feature instability under distribution shift** - Features correlated with
  the target in training become uninformative or adversarial at deployment
  - E.g., in the Netflix Prize, ensemble models achieved state-of-the-art
    accuracy but were too slow to deploy at scale
  - The pipeline optimized prediction accuracy instead of the actual objective:
    scalable, robust recommendation

- **Ceiling analysis blindness** - Without causal modeling, pipeline
  improvements target the wrong stage
  - Ceiling analysis (mocking pipeline stages with oracles) identifies which
    stages bound performance
  - But on a correlated pipeline, ceiling analysis misleads: fixing one stage may
    not help if the bottleneck is a confounded input
  - E.g., improving character recognition accuracy in OCR doesn't matter if text
    detection is confounded by image quality artifacts

- **Silent model failure** - Causally uninformed models fail silently
  - Accuracy metrics on held-out data look fine
  - Downstream business outcomes degrade
  - The gap between accuracy and decision quality is the cost of ignoring causality

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

- The gap between Data Science and Decision Science is the gap between
  **prediction accuracy** and **decision quality**
  - A model can be highly accurate at predicting churn yet offer no guidance on
    which intervention will reduce churn
  - A model can correctly identify that ice cream sales correlate with drowning
    rates without telling you how to reduce drowning

- **Decision pipelines** extend prediction pipelines by adding:
  - An explicit action space: "What can we do?"
  - A causal model: "How do actions cause outcomes?"
  - A utility function: "What outcomes do we value and how much?"
  - An uncertainty model: "How confident are we in our causal estimates?"

- Building decision pipelines requires **causal thinking**:
  - Distinguish observational from interventional quantities
  - Identify confounders that bias action-outcome estimates
  - Design experiments when observational data is insufficient
  - Use counterfactual reasoning to evaluate policies after the fact

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
