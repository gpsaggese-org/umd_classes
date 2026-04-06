# The Limits of Prediction

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
