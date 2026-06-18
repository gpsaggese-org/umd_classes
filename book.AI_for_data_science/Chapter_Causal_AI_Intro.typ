== Background

Big data and traditional AI have dominated the landscape for the past decade.
Organizations have focused on collecting and organizing massive data volumes,
then running analytics—dashboards, models, and reports—to extract insights.
This #strong[data-driven] approach has produced valuable results, but it operates
within important limits.

Data analytics exist on a spectrum of sophistication. #strong[Descriptive
statistics] answer "What happened?" by showing metrics like mean, median, and
standard deviation. #strong[Predictive models] address "What will happen?" by
forecasting based on patterns. #strong[Prescriptive programs] tackle "What should we
do?" by recommending actions. The most sophisticated approach combines
#strong[simulation and optimization] to find "What's the best we can do?" under
different conditions.

However, there is a critical gap between the sophistication of these methods
and what they actually reveal about the world. Traditional AI systems excel at
finding patterns but fail to explain mechanisms or test interventions. This
limitation becomes clear when examining what models can and cannot tell us.

#figure(
  image("../msml610/lectures_source/figures/L08.1.Analytical_sophistication.png", width: 90%),
  caption: [Analytical sophistication: progression from descriptive to prescriptive to optimal decision-making]
)

== What ML Systems Can and Cannot Tell You

Machine learning creates an illusion of understanding. A model with 95%
accuracy at predicting customer churn might win validation metrics while being
utterly useless for business decisions. The core problem: #strong[prediction accuracy
does not imply causal knowledge].

Consider the difference between prediction and explanation. Prediction models
find patterns in historical data and extrapolate to new cases. They cannot
explain why those patterns exist or what happens when you intervene. A sales
forecast that accurately projects next quarter's revenue cannot tell you what
happens if you lower prices by 10%. This gap between prediction and
intervention is the domain of causation.

#strong[Association] occurs when variables co-occur or are statistically dependent.
The classic example: people who buy diapers also buy beer. Association reveals
correlation but not direction or mechanism. #strong[Correlation] is a specific type
of association—a linear relationship between variables. Ice cream sales and
drowning deaths correlate strongly, but both are seasonal phenomena, not
causally related.

#strong[Causation] means changing one variable directly affects another. Asbestos
causes cancer. Unlike correlation, causation requires either experimentation or
a causal model to establish. The illusion lies here: high correlation feels
like understanding, but real understanding means knowing what happens when you
intervene.

ML systems can identify #strong[pattern recognition], finding correlations and
similar items through clustering or classification. They can deliver
#strong[predictive accuracy] when training and future data match, though this only
works if conditions remain stable. They can measure #strong[feature importance],
identifying variables with strongest statistical associations. Yet they cannot
distinguish correlation from causation.

ML systems cannot answer causal questions. They cannot infer #strong[causation from
observational data alone] without additional assumptions. Strong correlations
arise from confounding, reverse causation, or coincidence. They cannot predict
#strong[effects of interventions]—"If we change X, what happens to Y?"—without
causal assumptions. They cannot generate #strong[counterfactuals]—"What would have
happened with a different decision?" They cannot ensure #strong[fairness] beyond
statistical bias; a model can be statistically unbiased while using proxy
variables that encode protected attributes.

Finally, ML systems optimize for #strong[accuracy, not business outcomes]. A 90%
accurate fraud detector that blocks half of legitimate transactions produces
worse business results than an 85% accurate one. Accuracy is a means, not an
end.

== Why Causal AI Matters

Organizations face concrete problems that correlation-based AI cannot solve.
The first is fundamental: #strong[correlation is not causation].

Humans intuitively understand this distinction but regularly confuse
association with causation in decisions. If you eat food and develop a
stomachache, you infer the food caused the problem. If a stock rises after you
buy it, you might believe you timed the market. Yet sometimes causality runs
both directions: does top consulting improve businesses, or do successful
businesses hire top consultants?

The hotel industry illustrates the danger. Prices are low when hotels are empty
and high when demand surges and hotels fill. A naive model trained on this data
would suggest raising prices to sell more rooms—backwards logic that would
destroy revenue. In online marketplaces, the same pattern appears with pricing
decisions. The causal question—"What is the impact of lowering prices on units
sold?"—depends on business type, timing, customer segments, and competitor
behavior. Correlation cannot answer this.

The second problem is #strong[decision making]. Businesses need decisions, not just
predictions. Policy questions demand causal reasoning: "Low-sugar or low-fat
diet: which works?" "If we increase credit lines, how does bank margin change?"
"Should we build a library or give tablets to boost test scores?"

The third problem is #strong[ML explainability]. Regulators increasingly require
defense of AI decisions in hiring, lending, and policy. Many ML systems are
black boxes, particularly neural networks. Humans cannot understand how inputs
produce outputs or explain decisions to shareholders. Features like age, race,
and sex introduce obvious bias. Solutions like fines, customer backlash, and
activist pressure follow. Explainable AI that helps users understand, trust,
and explain results is essential.

The fourth problem: #strong[how ML systems make decisions today]. Typical workflows
collect data, train models, and deploy systems that predict X then take action
Y. The critical limitation is optimization for prediction accuracy, not
decision quality or business outcomes. A fraud detector with 95% accuracy that
blocks 50% legitimate transactions fails fundamentally.

The fifth problem involves #strong[feedback loops]. Prediction systems change the
world, creating cycles that amplify bias. Recommendation systems recommending
sensational content lead users to click more, which produces more sensational
training data, which recommends even more sensational content—driving
radicalization and echo chambers. In criminal justice, minorities policed more
get arrested more, producing biased arrest data, which trains models that
judges use for bail and sentencing, making the system increasingly biased.
College admissions models trained on historically racist and sexist decisions
encode and perpetuate those biases.

The sixth problem is #strong[distribution shift]. The world constantly changes.
#strong[Concept drift] occurs when the relationship between inputs and outcomes
shifts over time—customer preferences change, making 2020 models less accurate
by 2023. #strong[Covariate shift] happens when input distribution changes but
relationships stay—more young customers join, harming models trained on older
cohorts. #strong[Label shift] occurs when outcome distribution changes—fraud tactics
evolve, reducing effectiveness of models trained on old fraud patterns.

Causal models address these failures by encoding mechanisms, not just patterns.
Mechanisms stay stable across distribution shifts; understanding why enables
prediction in new contexts.

== Optimization vs. Inference vs. Decision Theory

Machine learning conflates three distinct paradigms. #strong[Optimization] finds the
best action given a known objective, assuming world behavior is established.
Tools include gradient descent, linear programming, evolutionary algorithms.
The goal: minimize cost, maximize throughput, tune parameters.

#strong[Statistical inference] estimates parameters from data given a model
structure. It learns from observations—estimating treatment effects, computing
confidence intervals. Tools include regression, Bayesian estimation, hypothesis
testing.

#strong[Decision theory] chooses actions under uncertainty, requiring reasoning
about interventions and outcomes. When should you launch a product with
uncertain demand? What experiment will most reduce uncertainty? Tools include
utility functions, expected value of information, causal models.

ML focuses on inference and optimization but real problems need #strong[decision
theory]. Organizations must act under uncertainty with causal knowledge. The
three paradigms differ in their core questions: Optimization asks "What
maximizes this objective?" Inference asks "What is this parameter?" Decision
theory asks "What should we do?"

Causal AI bridges inference and decision theory. Inference reveals what the
world looks like. Causal models show what happens when you act. Decision theory
selects which action to choose.

== The Cost of Ignoring Causality

Organizations waste resources and make wrong decisions by ignoring causality.
#strong[Simpson's Paradox] shows how aggregate data trends reverse in subgroups.
Berkeley admissions appeared biased overall but unbiased within departments—the
causal fix was conditioning on the right variables using directed acyclic
graphs. #strong[Confounding bias] occurs when a hidden variable drives both
treatment and outcome; ice cream sales and drowning deaths both rise in summer.
Control for confounders to fix this. #strong[Collider bias] appears when
conditioning on a common effect creates false associations; in hospitalized
patients, unrelated diseases appear correlated because both cause
hospitalization. Never condition on colliders.

#strong[Feedback loop amplification] makes biased predictions reinforce bias in
future data. More police in minority neighborhoods produce more arrests,
training models that deem neighborhoods more dangerous, sending more police.
Model feedback explicitly to address this.

#strong[Intervention backfire] occurs when acting on correlation leads to wrong
actions. Hospitals with more staff have higher mortality rates—confounded by
severity. A naive intervention reducing staff would be catastrophic.
Distinguish correlation from causal effect before acting.

Causal AI solves these problems. It #strong[understands the why], determining
cause-and-effect between variables: "Did marketing increase sales?" It
#strong[identifies interventions], finding variables and actions that change
outcomes: "Which lifestyle changes reduce blood pressure?" It #strong[predicts
counterfactuals], hypothesizing outcomes under different circumstances: "Would
a student get different grades at a different school?" It #strong[avoids bias] by
accounting for confounding variables. It #strong[improves decisions] by revealing
relationships that enable better choices.

The contrast with traditional AI is stark. Current AI uses correlation to
analyze data, identify patterns, make predictions, with quality depending on
data quality—biased data produces poor models. Causal AI infers causation from
association, understands when causation and association differ, and understands
cause-and-effect to intervene for desired effects.

Judea Pearl captured this shift: "The next revolution of data science is the
science of interpreting reality, not of summarizing data."

== The Ladder of Causation

Pearl provided a three-level framework for understanding causality. The
#strong[ladder of causation] progresses from seeing to doing to imagining.

#strong[Rung 1: Association] asks "How would seeing X change your belief in Y?" The
math is $Pr(Y|X)$. The activity is passive observation to determine if
variables relate. Traditional AI and ML operate here. Examples: trees have
green leaves in spring; what does a symptom tell you about disease; what does a
survey reveal about elections?

#strong[Rung 2: Intervention] asks "What happens to Y if you do X?" The math is
`Pr(Y | do(X), Z)`. The activity requires understanding action X's impact on Y
under conditions Z using a causal model, not just observations. Examples:
spring makes leaves turn green; did headache disappear from pain reliever or
food; if I take aspirin, will my headache cure; if we ban sodas, what happens?

#strong[Rung 3: Counterfactuals] asks "Was X that caused Y?" The symbol is $Pr(Y_X |
x', y')$. The activity requires imagining what would happen if facts were
different—the highest form of reasoning, requiring causal understanding.
Examples: what if a child received an adult drug dose; what would a jury
conclude; why did a marketing campaign fail?

Most organizations operate on rung 1, making predictions from patterns. Causal
AI enables movement to rungs 2 and 3, where real decisions happen.

== Correlation vs. Causation Models

#strong[Correlation] describes how variables relate. #strong[Causality] describes whether
one variable causes another. Both approaches accept inputs, transform them,
compute predictions. But they differ in philosophy and process.

#strong[Correlation-based AI] uses a "data first" approach: more data is better. The
process follows: acquire data, integrate and clean it, perform exploratory
analysis, engineer features, build and test models, deploy in production.
Common failures include organizational misalignment, opaque models lacking
explainability, spurious correlations, and never articulating business goals.

#strong[Causation-based AI] uses a "model first" approach: understand the business
question before collecting data. The process asks: What is the intended
outcome? What intervention is proposed? What confounding and effecting factors
exist? Create a model diagram. Then acquire data. The approach prioritizes
understanding before action.

== From Data Science to Decision Science

Data science and decision science are #strong[two different paradigms] serving
different purposes. Data science predicts outcomes using statistical models and
ML. Decision science chooses best actions using causal models and decision
theory. Data science outputs scores, forecasts, clusters. Decision science
outputs recommended actions with expected outcomes.

Data science measures success by accuracy, AUC, RMSE. Decision science measures
by business outcome, ROI, impact. Data science requires historical
observations. Decision science requires observations plus causal structure.

#strong[Key insight]: organizations have data science teams doing prediction while
business stakeholders need decision science. The gap between "what will happen"
and "what should we do" is causal reasoning. Machine learning excels at
prediction but fails at "what-if" questions involving interventions.

#strong[Predictive questions] ask "What will happen?" Using standard ML on
observational data alone, they suit monitoring and alerting. Examples: which
patients will be readmitted, which customers will churn, what will sales be,
which students will fail, which transactions are fraudulent.

#strong[Causal questions] ask "What to do?" or "Why?" Using causal models or
experiments, they answer "what if" and suit decisions and policy design.
Examples: which intervention reduces readmission, what action prevents churn,
how would a 10% price cut affect sales, does tutoring improve scores, what
policy reduces fraud?

Organizations progress through levels of sophistication. #strong[Level 0:
Descriptive] answers "What happened?" with dashboards, reports, statistics.
#strong[Level 1: Predictive] answers "What will happen?" with ML and forecasting,
assuming a stable world. #strong[Level 2: Causal] answers "Why?" and "What if we
intervene?" using DAGs and do-calculus to understand mechanisms. #strong[Level 3:
Decision] answers "What should we do?" combining causal models, decision
theory, and business goals. Most organizations stall at level 1; causal AI
enables jumps to levels 2 and 3.

== Digital Transformation and AI Projects

#strong[Digital transformation] uses digital technologies—AI, cloud, IoT,
automation—to reduce costs and improve revenues. It requires integrating
technology, fostering cultural change toward innovation and data-driven
thinking, adopting customer-centric approaches, automating processes, and
making data-driven decisions.

Yet AI projects fail regularly, often because they approach problems only from
an ML perspective. Data scientists focus on model accuracy and technical
metrics, working isolated from domain experts and business users. This
isolation produces irrelevant solutions. #strong[Misalignment with business goals]
causes models to solve wrong problems or answer irrelevant questions.
#strong[Black-box models] fail because they are difficult to interpret or explain to
stakeholders, reducing trust and adoption. #strong[Data issues] undermine
performance. #strong[Deployment challenges] prevent integration into production.
#strong[Lack of feedback loops] leaves performance unmonitored post-deployment.

Successful AI projects follow a different path. #strong[Create a hybrid team]
representing all business aspects using a collaborative framework and common
language like DAGs. #strong[Meet regularly] to ensure continuity. #strong[Find an
executive sponsor] who understands goals and potential. #strong[Run an initial
pilot] with a small team on a bounded problem, demonstrating merit before
scaling.

== The Causal AI Workflow

Using causal AI in business involves a structured workflow that moves from business goals through causal models to actionable results. The process forms a cycle: business goals define use cases, which drive causal model design, which requires data sources, which feed into knowledge models, which enable algorithmic solutions, which suggest interventions, which produce results, which inform future business goals.

#figure(
  image("../msml610/lectures_source/figures/causal_ai_workflow.svg", width: 100%),
  caption: [The Causal AI workflow: a circular process from business goals through causal models to actionable results]
) <fig:causal_workflow>

#strong[Step 1: Intended Outcomes] aligns project with business goals. Most AI projects fail from
misalignment. Ask: What process are you analyzing? What happens with different
courses of action? What data can be combined? What interventions are possible?
What confounders exist but can't be measured?

#strong[Step 2: Proposed Interventions] identifies levers to achieve outcomes. In
customer marketing, possible interventions include introducing new products,
bundling products, adjusting advertisement focus, adding product variations,
discontinuing products, or divesting product lines.

#strong[Step 3: Identifying Factors] maps confounders that obscure relationships,
direct effects through intervention, indirect effects from environment or
byproducts, and total causal effects from all modifying factors.

#strong[Step 4: Build Causal DAG] creates visual models simplifying systems while
preserving key relationships. Causal models aid communication between
stakeholders, reduce cognitive overload, guide data collection by identifying
impactful variables, and support hypothesis testing. Balance simplicity—too
little loses insight; too much loses clarity.

For example, in a pricing optimization problem, the DAG must capture how price affects customer behavior, product amount sold, and revenue. It must also account for confounders: competitive offers, product supply, and store distance all influence how much customers buy. Understanding these relationships prevents incorrect interventions like raising prices to increase sales.

#figure(
  image("../msml610/lectures_source/figures/pricing_dag.svg", width: 80%),
  caption: [Example: Causal DAG for pricing decisions. Price has multiple paths to revenue, with confounders creating indirect effects.]
) <fig:pricing_dag>

#strong[Step 5: Data Acquisition] gathers data for causal modeling, treating and
transforming it to match refined models. Clean, normalize, and align data with
model assumptions. Encode categorical variables, handle missing data, normalize
values, control for bias.

#strong[Step 6: Model Refinement] refines DAGs post-design to reduce bias and
improve reliability, clarifying variables as confounders, mediators, or
outcomes. Avoid controlling for mediators or colliders. Control for direct and
indirect confounders. Test against technical and business objectives.

#strong[Step 7: Deployment] transitions from experimentation to decision-making.
Validate against real-world outcomes. Develop user-friendly interfaces.
Automate data pipelines. Establish monitoring metrics. Document clearly. Train
stakeholders. Deliver measurable business value.

#strong[Hybrid teams] include business strategists aligning modeling with goals,
subject-matter experts providing domain knowledge, data experts sourcing and
cleaning data, data scientists constructing causal models, software developers
building tools and pipelines, IT professionals ensuring infrastructure, and
project managers coordinating collaboration.

== Explainability and the Future

Modern AI systems require explanation. Users must understand how ML models make
decisions, whether they can be trusted, whether they are biased. AI systems
foster trust, transparency, and confidence through explanation.

#strong[LIME] (Local Interpretable Model-agnostic Explanations) focuses on single
predictions, approximating models locally with interpretable models. #strong[PDP]
(Partial Dependence Plots) shows marginal feature effects by varying one
feature while holding others constant. #strong[ICE] (Individual Conditional
Expectation) shows feature-prediction relationships for individual instances.
#strong[SHAP] (SHapley Additive exPlanations) quantifies feature contributions to
specific predictions.

Causal AI enhances interpretability. DAGs present variables, relationships, and
strengths visually. Counterfactuals predict action outcomes. Removing
confounders prevents skewed estimates. Output is understandable to experts and
non-experts. Hybrid teams enhance context and reduce blind spots.

#strong[The future of causal AI] moves from academia to commercial use, departing
from purely data-driven systems toward reflecting human thinking and
decision-making. Causal AI will converge with traditional AI, deep learning,
and generative techniques to create more trustworthy, interpretable, and
effective systems.
