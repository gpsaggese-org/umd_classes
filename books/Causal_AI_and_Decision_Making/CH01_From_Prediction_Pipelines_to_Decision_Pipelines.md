// Refs
//
// msml610/lectures_source/Lesson08.1-Causal_AI_intro.txt
// msml610/lectures/Lesson08.1-Causal_AI_intro.pdf
//
// msml610/lectures_source/Lesson02.2-ML_Paradigms.txt
// msml610/lectures/Lesson02.2-ML_Paradigms.pdf

# From Prediction Pipelines to Decision Pipelines

## What ML Systems Can and Cannot Tell You
// msml610/lectures_source/Lesson08.1-Causal_AI_intro.txt:45  "Why Causal AI?"
// msml610/lectures_source/Lesson08.1-Causal_AI_intro.txt:91  "Problem 1: Association vs Correlation"

- Traditional machine learning excels at **finding patterns** in historical data
  - Models learn statistical associations: "when X occurs, Y tends to follow"
  - This works well for prediction tasks where the future resembles the past
  - Examples: spam detection, image classification, demand forecasting

- But ML systems struggle with **why** questions and intervention scenarios
  - A model trained on observational data cannot answer: "What if we did X?"
  - Correlation-based models work by spotting regularities, not causal
    mechanisms
  - They generalize only to distributions similar to their training data

- The fundamental limitation: **data alone cannot tell you about causation**
  - Two variables may move together due to:
    - Direct causation (X causes Y)
    - Reverse causation (Y causes X)
    - A hidden confounder (Z causes both X and Y)
    - Pure coincidence
  - Without domain knowledge and causal reasoning, no amount of data can
    distinguish these cases

- ML models are "data first" systems
  - They accumulate data, clean it, engineer features, and fit patterns
  - The process treats all correlations equally
  - Bias in the data propagates directly into the model

- **Explainability is incomplete without causal insight**
  - A model can explain _what_ it predicts without understanding _why_
  - Feature importance tells you which variables the model relied on, not
    whether those relationships are causal
  - Regulators want organizations to justify decisions, not just produce model
    outputs

## Correlation, Association, and the Illusion of Understanding
// msml610/lectures_source/Lesson08.1-Causal_AI_intro.txt:103  "Correlation is Not Causation!"
// msml610/lectures_source/Lesson08.1-Causal_AI_intro.txt:123  "Correlation is Not Causation: Examples"

- **Association** is a statistical property: two variables move together
  - Association is powerful for prediction but dangerous for decision-making

- **Humans are primed to mistake association for causation**
  - Example: You eat a particular food and get a stomachache several times
    - You infer: "This food is bad for me"
    - Reality: Maybe the food is fine, but you eat it when stressed, and stress
      causes the ache
  - Example: You buy a stock right before its price skyrockets
    - You infer: "I can time the market"
    - Reality: You got lucky, and overconfidence leads to riskier bets that
      eventually fail

- **Causation** is a mechanism: changing one variable directly influences
  another
  - You cannot conclude causation from correlation alone
  - You must understand the mechanism by which one variable influences another

- **Three reasons variables may correlate without causal connection**:
  - **Reverse causality**: Y causes X (not X causes Y)
    - Example: Does depression cause poor sleep, or does insomnia cause
      depression?
    - A correlational study cannot distinguish these
  - **Confounding**: A hidden third variable Z causes both X and Y
    - Example: Hotels charge high prices _and_ have high occupancy during
      tourist season
      - Naive analysis: raising prices increases occupancy
      - Reality: demand (Z) causes both high prices and high occupancy
  - **Coincidence**: The correlation is spurious
    - Example: Nicolas Cage movies released per year correlates with swimming
      pool drownings
    - No mechanism connects them; the correlation is noise in large datasets

- **Data does not understand causes and effects**
  - Only humans can identify variables and relationships based on domain
    knowledge
  - Without causal reasoning, intelligent decision-making is impossible

- **The cost of ignoring causation**:
  - Decisions based on spurious correlations fail when conditions change
  - Interventions based on correlation often backfire
  - Example: Google Flu Trends predicted flu prevalence from search query
    patterns
    - The model was accurate on historical data
    - But when search behavior changed (media hype, algorithm changes), the
      model collapsed
    - The query-flu correlation was fragile; no causal understanding existed

## Three Kinds of Questions: Association, Intervention, Counterfactual (Pearl's Ladder)
// msml610/lectures_source/Lesson08.1-Causal_AI_intro.txt:228  "The Ladder of Causation"

- Judea Pearl's **Ladder of Causation** distinguishes three types of questions
  - Each rung requires stronger reasoning than the one below
  - Most current AI operates only at the bottom rung

### Rung 1: Association (Observing)
// msml610/lectures_source/Lesson08.1-Causal_AI_intro.txt:245  "Rung 1: Association"

- **Question**: "How would seeing X change our belief in Y?"
- **Mathematical notation**: $\Pr(Y|X)$ (the conditional probability of Y given
  X)
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
  - A model can be arbitrarily accurate at prediction yet provide no guidance
    for action

### Rung 2: Intervention (Doing)
// msml610/lectures_source/Lesson08.1-Causal_AI_intro.txt:261  "Rung 2: Intervention"

- **Question**: "What happens to Y if you do X?" or "What if we intervened on
  X?"
- **Mathematical notation**: $\Pr(Y | do(X), Z)$ (the probability of Y if we
  intervene to set X, under conditions Z)
- **Activity**: Understanding the causal impact of an action on an outcome

- Interventions require a **causal model**: an explicit representation of
  mechanisms
  - You must understand not just that X and Y correlate, but _why_
  - You must know which confounders exist and account for them
  - You must distinguish correlation from causation

- **Examples of intervention questions**:
  - "If we lower prices by 10%, how many additional units will sell?"
  - "If we increase the credit line for a customer, what happens to default
    risk?"
  - "If we switch from a low-sugar diet to a low-fat diet, will health improve?"
  - "If we ban sodas in schools, will childhood obesity decline?"

- **Why observational data alone is insufficient**:
  - A model trained on historical prices and sales sees: lower prices correlate
    with higher volume
  - This reflects confounding: promotions lower prices and attract
    price-sensitive customers, both increasing volume
  - If you try to boost profit by raising prices (inverting the correlation),
    you fail because the causal direction runs the other way

### Rung 3: Counterfactuals (Imagining)
// msml610/lectures_source/Lesson08.1-Causal_AI_intro.txt:278  "Rung 3: Counterfactuals"

- **Question**: "Was X the reason Y occurred?" or "What would have happened if
  we had done differently?"
- **Mathematical notation**: $\Pr(Y_{X=x'} | X=x, Y=y')$ (the probability Y
  would have been different under a counterfactual scenario)
- **Activity**: Reasoning about alternative scenarios and causal attributions

- Counterfactual reasoning is the highest form of causal reasoning
  - You must understand not just mechanisms, but how they apply to specific
    individuals
  - It lets you answer "why?" about past events

- **Examples of counterfactual questions**:
  - "Was it the marketing campaign that caused the sales increase, or would
    sales have increased anyway?"
  - "Why did this particular customer churn? Would they have stayed if we had
    offered a discount?"
  - "Was it the drug that cured the patient, or would they have recovered on
    their own?"
  - "If this student had attended a different school, would their grades be
    different?"

- **Why counterfactuals matter for learning and improvement**:
  - You observe an outcome and want to explain it
  - Attribution matters: "did my action cause this, or would it have happened
    anyway?"
  - Without counterfactuals, you cannot learn from experience

## A Roadmap: From Prediction to Causal Reasoning to Decision Intelligence
// msml610/lectures_source/Lesson08.1-Causal_AI_intro.txt:72  "Data Analytics Sophistication"
// msml610/lectures_source/Lesson08.1-Causal_AI_intro.txt:299  "Correlation vs Causation Model"

- The evolution of data and AI reflects increasing sophistication in answering
  business questions

- **Level 1: Descriptive Analytics** - "What happened?"
  - Tools: Summary statistics, historical reports, dashboards
  - Activity: Collect data, compute means, medians, aggregations
  - Value: Understanding past performance
  - Example: "Our revenue was $10M last quarter, down 5% from last year"

- **Level 2: Predictive Analytics** - "What will happen?"
  - Tools: Machine learning, statistical models, forecasting
  - Activity: Learn patterns from historical data and extrapolate
  - Value: Anticipating future outcomes under current conditions
  - Example: "We forecast 15% customer churn this quarter based on engagement
    patterns"

- **Level 3: Prescriptive Analytics** - "What should we do?"
  - Tools: Optimization, decision analysis, causal inference
  - Activity: Identify interventions that produce desired outcomes
  - Value: Actionable recommendations that improve outcomes
  - Example: "Offering a 10% discount to at-risk customers reduces churn by 20%"

- **Level 4: Decision Intelligence** - "What's the best we can do?"
  - Tools: Causal AI, reinforcement learning, simulation
  - Activity: Continuously learn and optimize decisions under uncertainty
  - Value: Sustained improvement through adaptive decision-making
  - Example: "Our AI recommends personalized offers for each customer that
    maximize lifetime value while accounting for inventory and competitive
    dynamics"

- **Why causal AI is the bridge between prediction and decision intelligence**:

- Traditional ML is a **"data-first" approach**
  - Accumulate data and let patterns speak for themselves
  - Strengths: Works well with abundant data, scales easily
  - Weaknesses: Spurious correlations, poor generalization to new conditions, no
    explainability

- Causal AI is a **"model-first" approach**
  - Start with the business question and domain knowledge
  - Build a causal model that represents mechanisms
  - Use data to estimate causal parameters, not just correlations
  - Strengths: Generalizes to interventions, interpretable, robust to
    distribution shift
  - Weaknesses: Requires domain expertise, more complex, less data-hungry

// msml610/lectures_source/Lesson08.1-Causal_AI_intro.txt:329  "Causation-based Model Process"
- **Causal AI process**:

  1. What is the intended outcome we want to achieve?
  2. What interventions are possible (which variables can we change)?
  3. What are the confounding factors (hidden causes that affect both outcomes
     and our choices)?
  4. What are the mediating factors (how do interventions affect outcomes)?
  5. Create a causal model (diagram or graph) representing mechanisms
  6. Collect data and estimate causal effects
  7. Design experiments or observational studies to validate causal assumptions
  8. Use causal estimates to inform decisions

- **ML is powerful but narrowly scoped**:
  - ML excels at prediction when training and deployment distributions are
    similar
  - ML fails at decision-making when you must reason about interventions not in
    the training data

- **The future of intelligent systems**:
  - Integrate predictive power of ML with causal reasoning
  - Use ML for estimation (learning from data)
  - Use causal graphs for reasoning (understanding mechanisms)
  - Use decision theory to choose actions (optimizing under uncertainty)

## How Production ML Systems Make Decisions Today
// msml610/lectures_source/Lesson02.2-ML_Paradigms.txt:230  "Machine Learning Flow (1/2)"

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

// msml610/lectures_source/Lesson02.2-ML_Paradigms.txt:244  "Machine Learning Flow (2/2)"

- The hierarchy matters:
  - Question $>$ Data $>$ Features $>$ Algorithm
  - Teams usually over-invest in model selection while under-investing in
    problem formulation and data quality

- **Production decisions are implicit, not explicit**
  - A fraud detection model outputs a probability score
  - A business rule (threshold, policy) converts the score into an action
  - This separation is often unexamined and poorly audited
  - The pipeline predicts; the decision layer acts, but the decision layer is
    rarely modeled as rigorously as the prediction layer

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
  - Ignore this and the model degrades silently, often undetected until harm
    shows up downstream

- Mitigating distribution shift requires:
  - Monitoring input and output distributions continuously
  - Designing retraining schedules that account for concept drift
  - Building causal models that separate stable relationships from unstable
    correlations

## Optimization Vs. Inference Vs. Decision Theory
// msml610/lectures_source/Lesson08.1-Causal_AI_intro.txt:220  "Machine Learning and Decision Making"

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
// msml610/lectures_source/Lesson08.1-Causal_AI_intro.txt:145  "Problem 2: Decision Making"
// msml610/lectures_source/Lesson08.1-Causal_AI_intro.txt:158  "Problem 3: ML Explainability"

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
    reflects selection: high-intent users see more ads and buy more, not because
    ads cause purchases
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
  - But on a correlated pipeline, ceiling analysis misleads: fixing one stage
    may not help if the bottleneck is a confounded input
  - E.g., improving character recognition accuracy in OCR doesn't matter if text
    detection is confounded by image quality artifacts

- **Silent model failure** - Causally uninformed models fail silently
  - Accuracy metrics on held-out data look fine
  - Downstream business outcomes degrade
  - The gap between accuracy and decision quality is the cost of ignoring
    causality

## Data Science Vs. Decision Science
// msml610/lectures_source/Lesson08.1-Causal_AI_intro.txt:299  "Correlation vs Causation Model"
// msml610/lectures_source/Lesson02.2-ML_Paradigms.txt:278  "Question"

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

## References

- Angrist, J. D. and Pischke, J.-S. _Mostly Harmless Econometrics_ (2009)
- Berger, J. O. _Statistical Decision Theory and Bayesian Analysis_ (2nd ed., 1985)
- Burkov, A. _The Hundred-Page Machine Learning Book_ (2019)
- Hastie, T., Tibshirani, R., and Friedman, J. _The Elements of Statistical
  Learning_ (2nd ed., 2009)
- Hernán, M. A. and Robins, J. M. _Causal Inference: What If_ (2020)
- Hurwitz, J. and Thompson, M. _Causal Artificial Intelligence_ (2024)
- Lazer, D. et al. "The Parable of Google Flu: Traps in Big Data Analysis"
  _Science_ (2014)
- Manski, C. F. _Identification Problems in the Social Sciences_ (1995)
- Pearl, J. and Mackenzie, D. _The Book of Why_ (2018)
- Pearl, J. _Causality: Models, Reasoning, and Inference_ (2nd ed., 2009)
- Quionero-Candela, J. et al. _Dataset Shift in Machine Learning_ (2009)
- Russell, S. and Norvig, P. _Artificial Intelligence: A Modern Approach_ (4th
  ed., 2020)
- Scholkopf, B. et al. "Toward Causal Representation Learning" _Journal of
  Machine Learning Research_ (2021)
- Sculley, D. et al. "Hidden Technical Debt in Machine Learning Systems"
  (NeurIPS 2015)
- Spirtes, P., Glymour, C., and Scheines, R. _Causation, Prediction, and Search_
  (2nd ed., 2000)
- Sutton, R. S. and Barto, A. G. _Reinforcement Learning: An Introduction_ (2nd
  ed., 2018)
