// git_hash=854d98e0, timestamp=2026-07-09T23:22:08Z

// Import AIMA style formatting and macros.
#import "../../helpers_root/dev_scripts_helpers/typst/aima_style.typ": (
  aima-style, algorithm, chapter, glossary,
)

// Document metadata
#set document(
  title: "From Data Science to Decision Science",
  author: "MSML610: Advanced Machine Learning",
)

// Apply the AIMA document template (page/text/heading set + show rules).
#show: aima-style

#chapter(1, "Why Decisions, Not Predictions")

// Slide: Course Roadmap

== Course Roadmap

The path from raw data to actionable decisions requires moving beyond
traditional machine learning, which optimizes for prediction accuracy alone.
This course and book walk a single integrated pipeline end-to-end, from data to
action:

$$data -> model -> policy -> action -> feedback$$

Each stage transforms the output of the previous one, creating a tightly coupled
system where every component must work in concert. The model sits at the center
of this pipeline, but it is both #strong[causal and probabilistic]. A causal
model can answer not just _"what will happen?"_ but more importantly _"what
should we do?"_—the difference between prediction and prescription. A
probabilistic model quantifies uncertainty, allowing decision-makers to weigh
risks and allocate resources intelligently.

The pipeline loops back on itself. Actions change the world, producing new data
that feeds back into model training and policy revision. Ignoring this feedback
creates systematic failures that accumulate over time. A static, one-pass
approach to decision-making cannot survive in dynamic environments where the
system's own actions reshape the landscape.

The book is organized in five interconnected parts, each building on prior
concepts:

- #strong[Part I]: Why businesses need decisions, not predictions. This part
  catalogs the gaps between predictive pipelines and decision pipelines.
- #strong[Part II]: Probabilistic and causal foundations, including Gaussian
  processes, variational inference, normalizing flows, and causal discovery.
- #strong[Part III]: Single-step decisions, including decision theory, policy
  learning, and partial identification under uncertainty.
- #strong[Part IV]: Multi-step and dynamic decisions, including causal world
  models, causal reinforcement learning, and feedback loops.
- #strong[Part V]: Deploying, monitoring, and governing decision systems in
  production at scale.

This lesson opens Part I by cataloging what traditional machine learning leaves
out—the structural gaps between prediction and action. Understanding these gaps
is the first step toward building systems that actually work in the real world.

=== Why Traditional ML Falls Short

// Slide: Why Traditional ML Falls Short

Traditional machine learning optimizes for #strong[prediction accuracy on a
  fixed distribution], a goal that ignores four critical gaps a real decision
requires. Each gap is not a minor limitation but a systematic source of failure
in production systems.

First, #strong[causality]: Standard ML models learn correlations and patterns
from historical data. They become experts at recognizing what went with what in
the past. But correlation does not guide action. When you intervene—when you
change the world by making a decision—the correlations that the model learned
can disappear or even reverse. The model has learned _"what is,"_ not _"what
changes when I act."_ This is not a flaw in the model's accuracy; it is a flaw
in the objective itself.

Second, #strong[uncertainty]: Most business problems are small-data problems.
The training dataset is modest, the signal is noisy, and the future may differ
from the past. Yet standard ML pipelines emit a single number—a point
estimate—as if it were certain. No error bars, no posterior distribution, no
sense of how wrong the estimate could be. A decision-maker operating under
uncertainty needs to know not just the forecast but the range of plausible
outcomes.

Third, #strong[the business objective]: A prediction is not a decision. Knowing
that a customer has a 70% churn probability does not tell a business what action
to take, how much it will cost, or whether it is worth taking. ML models
optimize proxy metrics—accuracy, AUC, RMSE—that correlate with business value
but are not the same as business value. This misalignment turns technically
accurate models into operationally useless ones.

Fourth, #strong[dynamics]: The world is not static. Any decision changes the
world, breaking the distribution the model was trained on. Customers respond to
offers. Competitors react to pricing changes. Fraudsters adapt to detection
systems. A model trained on yesterday's data assumes tomorrow's world looks the
same. It does not.

Each of these gaps turns a technically accurate model into a poor
decision-maker. The rest of this lesson works through the cost of each gap in
turn, building the case for a more comprehensive approach.

== From Data Science to Decision Science

// Slide: From Data Science to Decision Science

Data science and decision science are cousins but optimize for different
objectives, ask different questions, and require different tools. This
distinction shapes every choice downstream: what data to collect, what model to
build, what metric to track, and ultimately whether the system adds value to the
organization.

Data science starts with a question like _"what will happen?"_ and uses
historical data to build a model that predicts future outcomes as accurately as
possible. The goal is to minimize prediction error on some test set, a clean
mathematical objective. Decision science starts with a different question:
_"what should we do?"_ and uses causal reasoning to determine which actions lead
to which outcomes and how trade-offs between competing goals can be resolved.

The table below contrasts the two approaches:

#table(
  columns: 3,
  [#strong[Dimension]], [#strong[Data Science]], [#strong[Decision Science]],
  [Goal], [Predict outcomes accurately], [Choose best actions],
  [Question], [What will happen?], [What should we do?],
  [Method], [Statistical models, ML], [Causal models, decision theory],
  [Output], [Score, forecast], [Action + expected outcome],
  [Metric], [Accuracy, AUC, RMSE], [Business outcome, ROI],
  [Data], [Observations only], [Observations + causal structure],
)

#strong[Key idea]: Teams that ship predictions while the business needs
decisions leave both the causal reasoning and the value on the table. A
high-accuracy model answering the wrong question is a failed project, no matter
what the metrics dashboard says. The shift from data science to decision science
is not a technical upgrade; it is a reframing of what success looks like.

=== Causal vs Predictive Questions

// Slide: Causal vs Predictive Questions

Every practical business question has two forms: a predictive form and a causal
form. Learning to distinguish between them is the first step toward building
decision systems that work.

A predictive question describes what will happen based on historical patterns.
_"Which customers will churn?"_ is predictive. It asks what the data suggests
about future churn risk. The answer comes from fitting a model to observational
data. A causal question asks what will happen if we intervene. _"What action
prevents churn?"_ is causal. It asks not just who is at risk, but what we can do
about it and how effective that action will be.

The distinction matters because the same outcome can have very different causes.
A customer might churn because they are dissatisfied _or_ because they are a
seasonal user who naturally stops purchasing in the off-season. A predictive
model sees both cases and learns they correlate with churn. But an intervention
that addresses dissatisfaction will not affect the seasonal customer, while
misjudging the cause leads to wasted retention spend.

Here are four examples showing how every business question has both forms:

#table(
  columns: 2,
  [#strong[Predictive Question]], [#strong[Causal Question]],
  [Which customers will churn?], [What action prevents churn?],
  [What will sales be next quarter?], [How would a 10% price cut affect sales?],
  [Which students will fail the exam?], [Does tutoring improve exam scores?],
  [Which transactions are fraudulent?], [What policy change reduces fraud?],
)

Predictive questions need only observational data and support monitoring,
alerting, and triggering workflows. _"Alert me when churn probability exceeds
threshold."_ Causal questions need causal models or experiments, and support
decisions and policy design. _"Test whether a discount offer reduces this
customer's churn."_

#strong[Key idea]: A causal model lets you reason about interventions,
trade-offs, and counterfactuals. A predictive model does not. Choosing the right
question is as important as choosing the right model.

=== The Analytics Maturity Ladder

// Slide: The Analytics Maturity Ladder

Organizations do not jump from no analytics to perfect decisions. They climb a
ladder of increasing sophistication, each level building on the prior one but
unlocking fundamentally new capabilities.

Level 0, #strong[descriptive], answers _"what happened?"_ using dashboards,
reports, and summaries of past events. A business might ask _"how many customers
did we acquire last month?"_ or _"what was our revenue by region?"_ Descriptive
analytics is essential but passive. It describes the landscape without guiding
action.

Level 1, #strong[predictive], answers _"what will happen?"_ using machine
learning and forecasting. A business predicts churn, demand, fraud, or other
future events. Most organizations stop here. Predictive analytics is powerful
and popular, but it does not say what to do. A churn model does not prescribe an
intervention.

Level 2, #strong[causal], answers _"why? What if we act?"_ using directed
acyclic graphs (DAGs) and causal do-calculus. A business moves from observing
correlations to reasoning about mechanisms. _"If we cut price, how will demand
respond?"_ Causal reasoning requires either domain knowledge encoded in a causal
graph or experimental data from interventions. Most organizations have not
reached this level.

Level 3, #strong[decision], answers _"what should we do?"_ by integrating causal
models with decision theory and utility functions. A business reasons about
actions in the context of competing objectives, constraints, and uncertainty.
Decision-making systems at this level optimize for business outcomes, not proxy
metrics.

Here is the maturity ladder:

#table(
  columns: 3,
  [#strong[Level]], [#strong[Question]], [#strong[Tools]],
  [0. Descriptive], [What happened?], [Dashboards, reports],
  [1. Predictive], [What will happen?], [ML, forecasting],
  [2. Causal], [Why? What if we act?], [DAGs, do-calculus],
  [3. Decision], [What should we do?], [Causal models + utility],
)

Most organizations are stuck at Level 1. They build accurate predictive models,
deploy them, and then apply rule-based heuristics to turn predictions into
actions. This hybrid approach leaves value on the table. #strong[Key idea]:
Climbing to Levels 2 and 3 is the jump this book makes, from prediction
pipelines to decision pipelines. The climb is achievable but requires new tools,
new thinking, and a shift in what success means.

== The Cost of Ignoring Causality

Causal reasoning separates meaningful patterns from spurious correlations. A
causal model encodes the mechanisms by which the world works, allowing
generalizations to new contexts. Without it, models trained on historical data
inherit its confounding and biases, and they cannot reliably generalize to new
interventions.

=== When Correlation Misleads

// Slide: Correlation Encodes Confounding as Causation

A purely predictive model learns $\Pr(Y | X)$ from historical data and absorbs
every association in the data, whether spurious or causal. It becomes an expert
pattern-matcher. It answers _"what will happen?"_ based on what has historically
co-occurred, but it makes no claim about causation. It does not distinguish
between correlation and causation, and it assumes the world stays fixed even
though actions informed by the prediction change it.

The danger lies in a simple confusion: correlation in observational data
reflects not just causal relationships but also confounders, selection effects,
and the way data was collected. When you intervene, the correlations can
disappear or reverse.

The classic example illustrates the stakes sharply. Ice cream sales and drowning
deaths are highly correlated—both peak in summer. A predictive model would learn
_"more ice cream predicts more drownings"_ and, if asked to predict drownings
given ice cream sales, would be accurate on historical data. But a decision
built on this would be _"ban ice cream to cut drownings,"_ which is disastrous.
The true causal mechanism is different: hot weather drives both ice cream sales
and beach visits, where drowning accidents happen. Ice cream is a symptom, not a
cause.

The problem lies in the mismatch between observational and interventional
quantities:

$$\Pr(Y | X) ≠ \Pr(Y | "do"(X))$$

The observational distribution $\Pr(Y | X)$ describes correlation in data
already collected under whatever policy generated that data. The interventional
distribution $\Pr(Y | "do"(X))$ describes what happens when you *set* $X$ to a
specific value through deliberate action, breaking the correlations that held in
the observational data. Acting on $\Pr(Y | X)$ when you need $\Pr(Y | "do"(X))$
is what makes correlation-based decisions backfire so reliably.

A causal model encodes the true mechanisms: weather causes both ice cream sales
and drowning risk. It can then reason: if we artificially increase ice cream
sales without changing the weather, drownings will not increase. Correlation
alone cannot make this inference. #strong[Key idea]: A causal model estimates
the interventional distribution; a predictive model does not. This gap is not
academic—it is the difference between decisions that work and decisions that
fail in the field.

// Slide: Missing Interventions and Counterfactuals

=== Missing Interventions and Counterfactuals

A correlation model answers _"what is?"_, never _"what if?"_ or _"why?"_ Two
entire classes of business questions stay permanently out of reach without
causal reasoning.

The first class is #strong[intervention questions]: _"If we cut price 10%, how
do units sold and revenue change?"_ A predictive model trained on historical
data has seen many price points and learned how sales correlate with each. But
historical data reflects the pricing decisions the business actually made, not a
counterfactual pricing experiment. The model cannot reliably extrapolate beyond
the range of prices it has seen, and even within that range, correlation is not
causation. Price might correlate with sales because low prices drive volume or
because the business lowered prices during seasonal downturns. A causal model
teases apart mechanism from confounding and can predict the effect of a new
price.

The second class is #strong[counterfactual questions]: _"Would this customer
have churned had we offered a discount?"_ Counterfactuals ask about outcomes in
worlds that never happened. The historical data contains no information about
what would have occurred if we had taken a different action. No amount of
additional observational data resolves this. Only a causal model that explains
the mechanism by which discounts affect churn can answer the counterfactual.

Consider a concrete example: a tutoring program correlates with higher exam
scores. Does tutoring cause the improvement, or do strong students self-select
into tutoring? A predictive model sees the correlation and cannot distinguish.
No amount of additional observational data—more schools, more years, more
students—resolves this without causal reasoning. A causal model would need to
encode either a random experiment (tutoring assigned at random) or strong
assumptions about the selection mechanism. An intervention question asks:
_"Would a randomly selected student's exam score improve if we enrolled them in
tutoring?"_ The answer requires causal inference, not just pattern matching.

#strong[Key idea]: Answering intervention and counterfactual questions requires
a causal model, not a more accurate predictor. These questions are not
theoretical—they are the core of business decision-making. If a model cannot
answer them, it cannot guide action.

// Slide: Selection Bias and the Missing Counterfactual

=== Selection Bias and the Missing Counterfactual

Historical data records only the decisions actually made, never the alternative.
This creates a structural problem called #strong[selection bias]—the observed
outcomes depend on which units received which treatment, and the units are not a
random sample from the population.

A bank's loan data shows outcomes for approved applicants—repayment rates,
default dates, profitability. It does not show outcomes for rejected applicants.
What would have happened if the bank had approved someone it rejected? The data
contains no answer. A credit model trained only on approved loans learns what
predicts repayment among people the bank already trusted. It becomes an expert
at distinguishing good borrowers from bad ones _within the approved population_.
But it cannot say who among the rejected applicants would have repaid. The
rejected population is structurally different from the approved population; the
model has never seen them.

This is a #strong[missing-counterfactual problem], distinct from confounding and
present _before_ modeling starts. A model can be highly accurate on the
population it observed and still be blind to the population the business needed
to reason about.

The problem is structural, not statistical. Collecting more historical loan data
does not help. More data on approved loans tells the model more about approved
borrowers but does nothing to illuminate the rejected population. The only ways
to resolve selection bias are: (1) conduct experiments on the rejected
population, randomly approving some and denying others to observe outcomes, or
(2) use strong causal assumptions to infer missing counterfactuals.

This matters for fairness and profit. If the bank's approval model was trained
on biased historical data—say, it approved men more often than equally qualified
women—the model will inherit and amplify this bias. Approving a woman with the
same qualifications as an approved man is treated as off-distribution.

#strong[Key idea]: A model trained on selected data inherits the selection bias
in that data. Missing-counterfactual problems cannot be fixed by collecting more
of the same data. They require either intervention or causal reasoning to
overcome.

=== Interference and Spillovers Across Units

// Slide: Interference and Spillovers Across Units

Standard machine learning assumes each unit's outcome depends only on its own
treatment and features. This is called the #strong[no-interference or SUTVA
  assumption]. Marketplaces, pricing equilibria, social networks, and
competitive environments routinely violate this assumption, sometimes
catastrophically.

When one unit's action changes another unit's outcome, the usual statistical
estimates of treatment effects become biased. This is called
#strong[interference or spillover].

Consider a concrete example: a company tests a discount on a product by showing
it to group A and showing the full price to group B. The discount increases
purchases in group A, so the experiment seems successful. But if group A and
group B share the same limited inventory or the same social network, the story
is more complex. Group A might be cannibalizing purchases that would have gone
to group B—not converting new customers but converting customers from one group
to another. Or group A's heavy promotion might saturate the market, depressing
group B's demand not because of the price difference but because of depletion.
Group B is no longer a clean counterfactual for group A.

Marketplaces exhibit pervasive interference. Uber's surge pricing in one area
redistributes demand across the city. Amazon's recommendation system affects not
just the recommended customer but also the visibility of competing products and
sellers. A treatment on one node in a social network spreads to neighbors,
affecting their behavior.

When interference exists, the standard randomized experiment—randomize
treatment, compare groups—produces biased estimates of the causal effect. The
effect that one unit perceives depends on what is happening to neighboring
units. The economy is not linear; individual treatments do not add up.

#strong[Key idea]: Interference violates the no-interference (SUTVA) assumption
that underlies most causal inference methods. Ignoring it turns a valid
treatment estimate into a biased one. Systems exhibiting interference require
specialized methods that model spillovers explicitly.

// Slide: Simpson's Paradox: When Aggregates Lie

=== Simpson's Paradox: When Aggregates Lie

#strong[Simpson's Paradox] describes a striking phenomenon: a trend within every
subgroup reverses once the subgroups are pooled. It is not a quirk or
statistical artifact—it is a signal that the aggregate hides important causal
structure.

Consider a drug's recovery rate by gender. The drug is tested on male and female
patients, and recovery is recorded:

#table(
  columns: 3,
  [#strong[Group]], [#strong[Recovery w/ drug]], [#strong[Recovery w/o drug]],
  [Male], [81 / 87 = 93%], [234 / 270 = 87%],
  [Female], [192 / 263 = 73%], [55 / 80 = 69%],
  [Combined], [273 / 350 = 78%], [289 / 350 = 83%],
)

The drug helps *each* subgroup. Men recover better with the drug: 93% versus
87%. Women recover better with the drug: 73% versus 69%. Yet when the groups are
pooled, the drug appears to hurt: 78% with drug versus 83% without drug. How is
this possible?

The answer lies in confounding at the aggregate level. Gender correlates with
both treatment choice and baseline recovery. Perhaps women with severe illness
were more likely to receive the drug (gender affects treatment assignment), and
women had lower baseline recovery rates regardless (gender affects outcome).
When you pool across genders without controlling for the confounding, the
aggregate trend reverses.

Simpson's Paradox is not a paradox about mathematics—it is a warning about
causality. An aggregate comparison can hide the true causal effect when the
comparison confounds two different groups. The individual-level effects are
positive (the drug works for everyone), but the aggregate effect is negative
because of who received treatment.

The lesson is sharp and practical: a model can look correct in aggregate and be
wrong, or harmful, for every segment it is applied to. If a recommendation
system is trained and evaluated on aggregate metrics, it might perform well on
average while failing systematically for subgroups. Aggregation can hide the
causal structure.

#strong[Key idea]: Causal reasoning must respect subgroup structure and
heterogeneous treatment effects. Ignoring it can reverse the true effect or mask
systematic harm to minorities.

// Slide: Collider Bias: Conditioning Creates Illusions

=== Collider Bias: Conditioning Creates Illusions

A #strong[collider] is a variable influenced by two or more independent causes.
Conditioning on a collider—that is, filtering or restricting analysis to units
with a particular value of that collider—opens a spurious association between
its causes. This is called #strong[Berkson's paradox] and is one of the most
counterintuitive causal phenomena.

Suppose within a company, two independent skills—statistics skill and flattery
ability—both influence who gets promoted. They are independent: the correlation
between statistics skill and flattery across all employees is zero. But now
consider only the promoted employees. Among the promoted, a surprising negative
correlation emerges: employees who are bad at statistics must be good at
flattery to have been promoted; employees who are good at statistics could have
been promoted on merit alone, so they need not be good at flattery. Conditioning
on the collider (promotion) creates an association between the causes
(statistics and flattery).

This is not merely a statistical quirk. Real systems exhibit collider bias. In
hiring, consider that both qualification and demographic fit (correctly or
incorrectly) influence hiring decisions. If you only analyze hired employees,
you create a negative correlation between qualification and other attributes. In
healthcare, consider that both disease severity and availability of a treatment
influence who receives the treatment. If you condition on having received the
treatment, you create correlations that do not exist in the broader population.

The insight is troubling: conditioning on the wrong variable—not just omitting
the right one, but actively conditioning on the wrong one—is enough to
manufacture a correlation with no causal meaning. A model can learn spurious
associations simply by conditioning on colliders in the causal graph,
accidentally discovering patterns that point in the wrong direction or have no
causal meaning at all.

#strong[Key idea]: Collider bias is a selection problem created by conditioning
on a common consequence. A model that unknowingly conditions on colliders will
learn spurious associations. Avoiding collider bias requires understanding the
causal graph, not just the data.

// Slide: Discarding Domain Knowledge and Mechanism

=== Discarding Domain Knowledge and Mechanism

A purely correlation-based pipeline discards known structure—physics, economics,
biology, the causal graph, domain expertise—in favor of whatever pattern the
data happens to contain. There is no principled way to inject constraints,
priors, or known mechanisms. The model chases correlations that may or may not
reflect causation.

The wolf-vs-husky classifier illustrates the risk. A model trained to
distinguish wolves from huskies achieves high accuracy on a test set. But
investigation reveals it is keying on #strong[snow in the background], not the
animal's features. Snow presence correlates strongly with wolves in the training
data— wolves were photographed in snowy regions, huskies mostly in backyards.
The model learned this statistical signal and became expert at exploiting it. It
is accurate for the completely wrong reason and breaks immediately in a
different visual context.

More broadly, a model that ignores mechanism inherits every artifact of how the
training data was collected. If training data is biased, unrepresentative, or
collected under a specific regime, the model will incorporate that bias. It has
no way to distinguish between causal mechanisms and statistical coincidences.

Consider a loan model trained on historical approval data. It might learn that
applicants who have a gym membership are more likely to repay loans. This could
reflect a real behavioral difference—gym members demonstrate discipline,
consistency, and self-investment. Or it could be spurious—gym membership is a
proxy for geographic location, social class, or demographic factors correlated
with approval rates in the training data. The model cannot distinguish. A causal
understanding of what drives repayment would allow injecting the constraint:
_"Gym membership should not directly influence approval."_

A model that encodes causal mechanism—the true drivers of outcomes and how they
interact—degrades more gracefully than one that chases surface correlations.
When the distribution shifts, mechanisms remain more stable than correlations. A
correlation learned from one time period or geography breaks when conditions
change; a mechanism is more likely to travel.

#strong[Key idea]: A model that ignores causal mechanism is brittle to
distribution shift. Encoding domain knowledge and causal structure makes models
more robust, more interpretable, and more trustworthy for decision-making.

== The Cost of Ignoring Uncertainty

Most business problems are "small data" problems—the training dataset is modest,
the signal-to-noise ratio is low, the future may differ from the past. Standard
ML pipelines emit a single number as if it were certain, with no error bars, no
posterior, and no sense of how wrong the estimate could be. Uncertainty
quantification is not a luxury for theoreticians; it is essential information
for decision-making.

=== Point Estimates Without Error Bars

// Slide: Point Estimates Without Error Bars

A demand forecast of "1,200 units next month" hides critical information. If the
true range is 1,100–1,300 units, the forecast is precise and useful: the
business can plan with confidence. If the true range is 400–3,000 units, the
forecast is useless for operations; the business must plan for either shortages
or overstock. The two ranges call for entirely different inventory decisions,
warehousing strategies, and procurement agreements with suppliers. The point
estimate alone does not convey this.

Most business problems are small-data problems. The training dataset is modest
relative to the complexity of the world—maybe hundreds or thousands of examples
for a high-stakes decision. The signal-to-noise ratio is low. Random variation,
unmeasured confounders, and model misspecification all introduce uncertainty.
Yet standard ML pipelines emit a single number as the prediction, no error bars,
no quantile estimates, no sense of the forecast's reliability. This is like
driving in fog while the dashboard shows only the car's current speed, with no
gauge for visibility or road conditions ahead.

Why do ML pipelines do this? Prediction is often framed as a point estimation
problem: given features $X$, output a single value $\hat{Y}$. The loss function
trains the model to minimize error in that point estimate (mean squared error,
cross-entropy). The model learns a function that outputs a single number. It
does not naturally output uncertainty.

But uncertainty is essential information for a decision-maker. Suppose a demand
forecasting model predicts 1,200 units with an 80% credible interval of [1,100,
1,300]. Now the business knows: there is an 80% chance demand falls in this
narrow range. Inventory planning becomes precise. Now suppose the interval is
[400, 3,000]. Demand could vary wildly. The business might plan for the worst
case (3,000 units) and accept potential overstock, or plan for a middle ground
and accept potential shortage risk. Either way, the decision is explicit and
informed by the uncertainty.

A decision-maker operating under uncertainty needs the spread of an estimate at
least as much as its center. Without it, they are flying blind, relying on
assumptions about uncertainty that may or may not be correct.

#strong[Key idea]: Uncertainty quantification is not a luxury. It is essential
information for decision-making under resource constraints.

// Slide: Epistemic vs Aleatoric Uncertainty Conflated

=== Epistemic vs Aleatoric Uncertainty Conflated

Standard models collapse two different kinds of uncertainty into a single
prediction. The two kinds are fundamentally different and imply different
strategies for reducing error.

#strong[Aleatoric uncertainty] is irreducible randomness in the outcome itself.
Even with perfect knowledge and perfect models, outcomes vary. A coin flip has
aleatoric uncertainty—the outcome is random and cannot be perfectly predicted.
Demand for an established product might be fundamentally stochastic due to
weather, competitor actions, and customer sentiment shifts; no amount of data or
modeling will collapse this randomness to zero. More data does not reduce
aleatoric uncertainty.

#strong[Epistemic uncertainty] comes from not having seen enough data or from
using the wrong model. A new product's demand is epistemically uncertain because
the business has never seen demand for this product at this price point. A
credit model's prediction on a novel application type is epistemically uncertain
because the model has never seen this demographic before. Epistemic uncertainty
shrinks with more data or a better model.

Separating them is crucial. If a fraud model's low predicted risk for a novel
transaction pattern reflects aleatoric risk—the transaction genuinely is low
risk—the model can approve with confidence. But if it reflects epistemic
uncertainty—the model has simply never seen this pattern before—the model should
flag it for review. Treating both as the same number catastrophically misleads
the decision of when to collect more data, when to defer to a human, or when to
change the model.

Consider a medical diagnosis system. A patient presents with symptoms that have
never appeared in the training data. The model predicts a low risk of a rare
disease. Is this aleatoric (the patient genuinely is low risk) or epistemic (the
model has no basis for prediction)? The patient's doctor should know which. If
epistemic, the doctor should seek additional expert input. If aleatoric, the
doctor can trust the model.

Standard models—neural networks, tree ensembles, linear regressions—do not
distinguish. A Bayesian model that specifies a prior and posterior can. A
ensemble model that quantifies disagreement among ensemble members can. A model
that learns a confidence score can. But a standard point estimator cannot.

#strong[Key idea]: Only epistemic uncertainty shrinks with more data. Treating
both as one number misleads the decision of when to collect more data, when to
defer to a human, or when to invest in a better model. Separating them is
essential for robust decision-making.

// Slide: No Abstention: Systems That Never Say "I Don't Know"

=== No Abstention: Systems That Never Say "I Don't Know"

A standard classifier or regressor always returns an answer. Hand it any input,
even one far outside its training distribution, and it will output a prediction
and often a confidence score. There is no abstention or deferral mechanism.
There is no way to say _"I don't know"_ or _"this is not my problem."_

A loan-approval model forced to score an applicant profile unlike anything in
its training data still returns a confident approval or denial. It has no way to
say: _"I have never seen an applicant like this. I cannot confidently assess
their creditworthiness. This decision should go to a human underwriter."_ The
model must choose.

This is a failure mode. The cases the model cannot handle reliably are often the
most interesting or important ones. A new immigrant with no US credit history
has no precedent in the training data. A startup founder with unconventional
income has no precedent. These are exactly the cases where human judgment is
most valuable, yet the model gives no signal of its uncertainty.

The technical fix is to add an abstention or deferral mechanism: let the model
output "uncertain" for some fraction of inputs, routing those to a human. But
this creates a new problem: under what threshold does the model defer? How do
you trade off between having the model decide more often (covering more cases,
potentially erring more) versus deferring more often (losing scale, requiring
human review on many cases)?

The deeper issue is that a decision system must know its limits. A model that
cannot abstain cannot be trusted with high-stakes decisions. It will be
confidently wrong exactly where it should be most cautious—off-distribution,
novel, high-stakes.

#strong[Key idea]: A decision system that cannot say _"I don't know"_ cannot be
trusted with the cases that matter most. Building in uncertainty quantification
and abstention mechanisms is essential for robust systems.

// Slide: Overfitting and the Statistical Significance Traps

=== Overfitting and the Statistical Significance Traps

Overfitting is not a single mistake in a single model run. It accumulates from
every repeated look at the same data. Without strong priors or constraints to
bound overfitting, the model will fit noise.

Statistical significance traps compound the problem. They are the mechanisms by
which researchers (intentionally or not) find spurious patterns in data.

#strong[Peeking] refers to checking a test repeatedly and stopping the moment
$p < 0.05$. Nominally, a $p$-value of 0.05 means a 5% false-positive rate: if
the null hypothesis is true and you run the test once, there is a 5% chance of
rejecting it by chance. But if you peek repeatedly—run the test, look at the
result, run it again if not significant—the false-positive rate balloons. Peek
100 times and expect roughly 5 false positives. A researcher who peeks at her
test results daily for a month and stops the moment she sees significance is
almost guaranteed a false positive.

#strong[Multiple comparisons] occur when testing many metrics at once. Suppose
you test 100 different metrics for a treatment effect, each at 5% significance.
By chance alone, about 5 of them will appear significant even if the treatment
has no effect. A company that measures hundreds of metrics—engagement,
retention, churn, upsell, fraud, latency, etc.—and reports the metrics that show
significance will find spurious wins. This is not fraud; it is how randomness
works. But it is a systematic bias toward false positives.

#strong[Burning the test set] occurs when reusing the same held-out data across
many rounds of tuning. The test set was meant to be a fresh evaluation set,
never seen during training. But if you use it to decide between model versions,
choose hyperparameters, or select features, it becomes training data in
disguise. The test set's error is no longer a reliable estimate of future error.
You have fit noise in the test set.

Each of these practices is individually understandable but collectively
catastrophic. A researcher who peeks, tests many metrics, and burns the test set
will find spurious patterns reliably. The solution is discipline: prespecify
what you will test and how, commit to it, then run the analysis.

#strong[Key idea]: Overfitting accumulates from repeated looks at data. Testing
multiple hypotheses, peeking at results, and reusing test sets all inflate the
false-positive rate. Statistical rigor—preregistration, correction for multiple
tests, honest error reporting—is not optional for decision-making systems.

== The Cost of Ignoring the Business Objective

A model can be accurate and still wrong if it optimizes the wrong objective. The
objective a model is trained on becomes the objective the business gets, whether
or not that was the intent. This misalignment between technical objective and
business objective is one of the most common sources of failure in production
systems.

=== Optimizing the Wrong Objective

// Slide: Optimizing the Wrong Objective

Models chase proxy metrics—accuracy, AUC, RMSE, clicks, engagement, retention—
instead of the business goal those metrics stand in for: revenue, customer
lifetime value, wellbeing, or market share. When a proxy becomes a target, it
stops measuring what you care about. This principle is called #strong[Goodhart's
  Law]: _Once a proxy becomes a target, it stops measuring what you care about._

A concrete example: a social media recommender is optimized purely for
click-through rate. Clicks are an easy metric to measure and optimize. The model
learns to recommend sensational, outrage-inducing content because such content
drives clicks. Clicks grow. The company celebrates. Engagement metrics climb.
But long-term user retention falls. Users become fatigued by outrage, platform
trust erodes, and the business loses value over time. The model achieved the
objective it was trained on—clicks—at the expense of the objective that matters
for business—long-term value.

A different example: a spam filter is trained to minimize false positives (not
blocking legitimate emails) because false positives are visible to users and
generate complaints. The model learns a conservative policy, rarely blocking
emails. Legitimate email flows are excellent. But spam flows are also excellent,
filling user inboxes. Spam complaints exceed false positive complaints. The
model optimized the wrong metric.

Another example: a loan approval model is trained to maximize accuracy on
approval decisions. It learns to approve applicants with high credit scores and
employment stability, deny others. Loan performance is strong—approvals default
less often. But the bank is implicitly learning to approve primarily wealthy
applicants and deny minorities and low-income applicants, inheriting and
amplifying historical bias. Accuracy on the approval population is high, but
fairness across populations is not measured.

The core issue is that business value is complex and multifaceted. It involves
trade-offs, constraints, and stakeholder considerations that do not compress
into a single number. An ML model trained on a scalar loss function will
optimize that loss ruthlessly, exploiting any misalignment between the loss and
true business value.

#strong[Key idea]: The objective a model is trained on becomes the objective the
business gets. Misalignment between technical objective and business objective
turns a technically excellent model into a business failure. Choosing the right
objective is as important as choosing the right algorithm.

// Slide: Symmetric Losses for Asymmetric Errors

=== Symmetric Losses for Asymmetric Errors

Standard losses—log-loss, mean squared error, misclassification rate—treat every
error the same size. A fraud model's log-loss does not distinguish between false
positives (blocking a legitimate transaction) and false negatives (missing
fraud). Both are errors; the loss function penalizes them equally. But business
errors are not symmetric. They cost differently.

A fraud false negative costs money directly—the business loses the transaction
amount. A fraud false positive costs customer frustration, abandoned cart,
customer support load, and churn risk. The two are not the same. In some cases,
false positives might be more costly than false negatives (if the fraud rate is
low and customers are sensitive to false blocks). In other cases, false
negatives are costlier (if fraud is prevalent and customer loss is small). The
business must choose based on its risk tolerance.

A fraud model trained on symmetric cross-entropy loss will find a decision
threshold that balances false positives and false negatives at a 50-50 point,
roughly. But the optimal decision threshold might be very different. If blocking
a legitimate transaction costs 10x the fraud loss, the optimal threshold should
be conservative—block only when very confident of fraud.

Consider a concrete example: a fraud model with 95% accuracy blocks half of
legitimate transactions. Sounds good on paper: 95% accuracy. But operationally,
this is disastrous. Customers cannot use their cards. Customer support is
overwhelmed. Churn spikes. The business suffers despite the model's high
accuracy, because accuracy does not capture the asymmetric cost of errors.

Cost asymmetry must be built into the loss function during training, not bolted
on after deployment. A proper approach is to define a custom loss function that
penalizes false positives and false negatives differently, weighting them by
their business costs.

#strong[Key idea]: Cost asymmetry must be built into the objective during
training. Using a symmetric loss and trying to apply cost-weighted decisions
afterward leads to suboptimal trade-offs and misaligned incentives.

// Slide: Multi-Objective Decisions Under Constraints

=== Multi-Objective Decisions Under Constraints

Real decisions trade off competing goals under budget, capacity, and legal
constraints. A single scalar loss cannot express this complexity. Collapsing a
multiobjective decision into one loss function hides the trade-off instead of
making it explicit.

Consider a hospital choosing a cancer therapy. Five-year survival is one
objective. Quality of life during treatment is another. Cost is a third. The
therapy that maximizes five-year survival might be intense, expensive, and
destroy quality of life. The therapy that maximizes quality of life might be
palliative, lengthen life less. The therapy that minimizes cost might be
inferior on both medical dimensions. There is no single "best" therapy
independent of how those three objectives are weighed against each other.
Moreover, different patients have different preferences; what is best for a
30-year-old might not be best for an 80-year-old.

Another example: a hiring system could optimize for diversity (hire equally from
all demographic groups), merit (hire the highest-scored candidates), and gender
balance. These objectives can conflict. A pure merit optimization might result
in all-male hires. A pure diversity optimization might result in lower-quality
hires. The organization must decide explicitly: how much merit am I willing to
trade for diversity? The trade-off should be explicit, not hidden.

A third example: a content recommendation system balances engagement (recommend
content that keeps users on the platform), fairness to creators (recommend from
diverse creators, not just popular ones), and user satisfaction (recommend
content users actually like). These objectives can conflict. Maximizing
engagement leads to concentrating attention on a few popular creators.
Maximizing fairness leads to recommending from lesser-known creators at the
expense of user satisfaction. The system must navigate trade-offs.

Single-objective optimization obscures these trade-offs. A model trained to
maximize a single weighted average of multiple objectives appears to make
trade-offs implicitly, but the weights are often not transparent or even known
to the decision-maker. Multi-objective approaches make trade-offs explicit,
presenting decision-makers with Pareto frontiers: the set of non-dominated
solutions where improving one objective requires worsening another.

#strong[Key idea]: Multiobjective decisions require explicit trade-off surfaces,
not a single scalar target. Making trade-offs explicit is more honest and often
leads to better outcomes than hiding them in a loss function.

=== Black-Box Scores Are Not Recommendations

// Slide: Black-Box Scores Are Not Recommendations

A black-box score ranks units but names no lever and gives no *why*. A churn
score might rank customers from most likely to churn to least likely to churn.
But it does not say which action prevents churn, how much retention budget to
spend, or whether the action is worth taking. It is not a recommendation; it is
a ranking.

A bare prediction is not actionable. _"This customer has churn score 0.8"_
provides no guidance. _"Offering a discount lowers this customer's churn
probability by 12 points"_ is actionable. It names the lever (discount), the
effect size (12 points), and the unit it acts on (this customer).

Credit, hiring, and healthcare increasingly require explanations, not just
scores, to justify decisions to regulators and stakeholders. Regulators ask:
_"Why did you deny this loan?"_ If the answer is _"the model said so,"_ that is
inadequate. The lender must explain the mechanisms: income, debt-to-income
ratio, payment history, and how each influenced the decision.

A bare prediction does not provide this. A proper decision system must return:
(1) an action (approve, deny, offer discount), (2) the expected outcome of that
action (probability of repayment, change in churn risk), and (3) an explanation
(why this action).

This has technical implications. A black-box deep learning model can be accurate
but opaque. A logistic regression or decision tree can be less accurate but
transparent. For high-stakes decisions, transparency often matters more than
marginal accuracy gains. A 95% accurate opaque model that cannot explain itself
is less useful than an 92% accurate transparent model that can.

Moreover, a recommendation system must learn end-to-end from decision to
outcome. If the system recommends an action but does not observe the outcome of
that action, it cannot learn whether its recommendation was correct. A churn
model that recommends discounts must eventually observe whether the customer
churned after the discount was offered. Only then can the system learn and
improve.

#strong[Key idea]: A bare prediction is not a recommendation. A proper decision
system must return an action, an expected outcome, and an explanation. Black-box
models, however accurate, are insufficient for high-stakes decision-making.

// Slide: The Cost of Solving Sub-Problems Separately

=== The Cost of Solving Sub-Problems Separately

A decision pipeline is often split into smaller, individually optimized pieces.
First, a model predicts an outcome. Second, a separate rule or policy transforms
that prediction into an action. Learning end-to-end—optimizing the entire
pipeline from input to business outcome—outperforms stitching together
separately-optimized parts. This is called #strong[decision-focused learning].

Consider an inventory system. Approach 1: Train a demand forecasting model to
minimize RMSE, then apply a fixed reorder rule to the forecast. Forecast 1,200
units, order 1,200 units. Approach 2: Train a system end-to-end to minimize
inventory cost (holding cost + shortage cost). The end-to-end system learns how
forecast uncertainty translates to inventory decisions. It might order 1,300
units despite forecasting 1,200, because the added holding cost is less than the
risk of stockout.

The end-to-end system outperforms the separate pieces because it avoids
information loss. When you separate prediction from decision, you lose
information about how decisions respond to uncertainty. The predictor does not
know what the decision-maker will do with the forecast. The decision-maker does
not tune the forecast to their specific needs.

Another example: loan underwriting. Approach 1: Train a credit risk model to
predict default probability, then apply a threshold rule (approve if risk <
threshold). Approach 2: Train a system end-to-end to maximize expected profit,
accounting for approval rate, interest rates, default risk, and operational
cost. The end-to-end system learns how to trade off default risk against volume
and profitability. It might approve marginal applicants with higher default risk
but better interest rate economics.

The principle generalizes: end-to-end optimization beats modular optimization
when the modules interact. The decision-making system should be trained to
optimize what matters—business outcomes—not a proxy like prediction accuracy.

#strong[Key idea]: Optimizing each piece in isolation does not add up to
optimizing the decision. End-to-end learning from input to outcome outperforms
splitting the problem into separately-optimized stages.

== The Cost of Ignoring Dynamics and Feedback

A decision changes the world. Once a model is deployed and begins informing
actions, it is no longer operating in a static environment. The distribution
evolves in response to the actions informed by the model. Feedback loops,
concept drift, and strategic adaptation can all turn a model that worked in
training into one that fails in production.

=== The Static-World Assumption Breaks

// Slide: The Static-World Assumption Breaks

Any decision changes the world, breaking the distribution the model was trained
on. Three ways the world moves out from under a static model are: concept shift,
covariate shift, and label shift.

#strong[Concept shift] occurs when the link $\Pr(Y | X)$ between inputs and
outcomes changes. A fraud detection model trained on 2019 fraud patterns relied
on certain transaction features. Fraudsters adapted their techniques; the
relationship between those features and fraud changed. The same feature values
now mean something different. Concept shift is the most dangerous because models
have no natural way to detect it from data alone.

#strong[Covariate shift] occurs when the input distribution $\Pr(X)$ changes
while the relationship $\Pr(Y | X)$ stays the same. The model learned how
features predict outcomes correctly, but the features themselves are now
different. A housing price model trained on pre-pandemic data saw certain
distribution of features. Post-pandemic, the feature distribution shifted—more
remote work means different neighborhood preferences. The relationship between
features and prices held, but the features themselves changed.

#strong[Label shift] occurs when the outcome distribution $\Pr(Y)$ changes while
the relationship $\Pr(Y | X)$ stays the same. A fraud model trained on last
year's fraud rate operated in an environment where 0.5% of transactions were
fraudulent. This year, fraud prevalence rose to 1%. The features still predict
fraud, but the base rate changed. The model, which assumed the historical
prevalence, now over-predicts fraud.

A fraud model trained on last year's tactics degrades as attackers adopt new
tactics, a label or concept shift the model has no way to detect on its own. The
model continues outputting predictions, but they grow stale.

A model that encodes mechanism, not just pattern, degrades more gracefully.
Consider a causal model of fraud: certain behaviors (rapid login from new
location, unusual purchase amount) increase fraud risk through understood
mechanisms. When fraudsters adapt, some mechanisms break (they avoid certain
behaviors), but the core causal structure—that certain actions increase risk—may
remain stable. A model that learned only surface correlations breaks
immediately.

#strong[Key idea]: A model that encodes causal mechanism is more robust to
distribution shift than one that chases correlations. Mechanisms are more stable
across distribution shift than surface correlations are.

// Slide: Feedback Loops and Bias Amplification

=== Feedback Loops and Bias Amplification

Predictions act on the world and reshape the future data the model is retrained
on. A small initial bias becomes a growing one, purely from the model training
on the outcomes of its own decisions. This is a #strong[feedback loop].

A concrete example: a recommender system optimized for click-through rate. The
model recommends sensational content because it drives clicks. Users see and
click on sensational content. Future training data contains even more clicks on
sensational content, reflecting the model's prior recommendations. The next
version of the model trains on this biased data and recommends more sensational
content still. The feedback loop amplifies the initial bias.

Another example: policing resource allocation. A model is trained to predict
crime hot spots based on historical arrest data. The model flags a particular
neighborhood as high-risk, justifying increased police presence. Increased
police presence leads to more arrests in that neighborhood (not necessarily more
crime, just more detection). Future training data shows higher arrest counts in
that neighborhood. The next model updates and flags the neighborhood as even
higher-risk. The feedback loop amplifies the initial bias, turning what might
have been a small disparity into entrenched inequality.

A third example: hiring. A company uses a model to screen resumes for senior
technical positions. The model trained on historical hiring data learns that
resumes from certain universities, companies, and backgrounds are more likely to
be hired. The model screens candidates, passing more from those backgrounds. The
company hires from those backgrounds at higher rates. Future training data
reflects this hiring pattern. The next model trains on biased data and amplifies
the bias.

The pernicious aspect of feedback loops is they are self-reinforcing. A decision
that is already wrong gets reinforced by data created by that decision. Breaking
a feedback loop requires intervention: randomization, A/B testing, or deliberate
exposure to diverse populations—anything that breaks the feedback from prior
decisions back to training data.

#strong[Key idea]: A feedback loop turns a small initial bias into a growing
one, purely from training on the outcomes of prior decisions. Feedback loops are
self-reinforcing and difficult to detect. Breaking them requires deliberate
intervention and monitoring.

// Slide: Performativity: When the Prediction Changes the Outcome

=== Performativity: When the Prediction Changes the Outcome

#strong[Performativity] is a prediction that changes the very quantity it
predicts—a sharper, more formal case of a feedback loop. Once a prediction is
performative, $\Pr(Y | "do"(X))$ (what actually happens when you intervene with
the prediction) is no longer a fixed target to fit. It becomes a function of
which model gets deployed.

A concrete example: a credit-risk score is published. Borrowers see their
scores. Borrowers with low scores realize they are seen as risky, so they change
behavior—they might avoid taking on new debt, defer large purchases, or clean up
credit. Borrowers with high scores might assume they are trusted, so they relax
caution. The published score moves borrower behavior, which moves the true
default rate the score was trying to predict. The score is performative.

Another example: a published search-ranking algorithm invites keyword-stuffing
as website owners game the system to improve ranking. The ranking changes the
distribution of websites in search results, which changes what searchers see and
click on, which changes the true relationship between ranking and user value.
The ranking algorithm itself changes what it is supposed to measure.

Once a prediction is performative, the problem is no longer a static prediction
task. The model's training data reflect outcomes under the previous model's
policy. Deploy a new model, and the data-generating process changes. The new
model must account for adaptation.

#strong[Key idea]: In performative settings, a model's accuracy on historical
data tells nothing about its effect once deployed. The model itself changes the
system it is predicting. This requires dynamic approaches that anticipate
adaptation.

=== No Exploration: Trapped in the Logged Policy

// Slide: No Exploration: Trapped in the Logged Policy

An observational-only model never experiments. It stays trapped inside the
support of whatever policy logged the training data. It cannot learn the effect
of an action nobody has ever taken—an overlap or positivity violation.

A pricing model trained on historical prices that never dropped below \$20
cannot say what happens at \$15, no matter how much historical data it has. The
model has no basis for extrapolation. Price elasticity might be different at
\$15; the customer population might change; competitor responses might differ.
The model does not know.

More broadly, some business questions cannot be answered by more historical
data. They require deliberate intervention. _"What happens if we implement
dynamic pricing?"_ cannot be answered by analyzing historical static pricing
data. _"What is the effect of free shipping on conversion?"_ cannot be answered
unless the company has historically offered free shipping to some customers.
These questions require experimentation.

A model that learns only from observational data is fundamentally limited. It
can extrapolate within the support of the data but not beyond it. For novel
decisions, novel product launches, or novel markets, observational data provides
no guidance.

#strong[Key idea]: Some business questions cannot be answered by more historical
data, only by deliberate intervention. Observational-only models are trapped in
the support of the logged data. Strategic innovations require experiments.

// Slide: Delayed and Long-Horizon Effects

=== Delayed and Long-Horizon Effects

A model optimized for an immediate proxy ignores downstream outcomes and has no
mechanism to assign credit over time. Short-term proxies and long-term business
outcomes can point in opposite directions. Only one of them is what the business
actually cares about.

A support team optimized for fast ticket closure learns to close tickets
quickly, whether or not the underlying issue is resolved. A customer's problem
is "solved" in the system—ticket closed—even if the customer still cannot use
the product. The true cost—repeat contacts, frustration, churn—shows up months
later, in a different metric (customer lifetime value, churn rate). The support
model optimized the wrong thing.

A learning system used in hiring might be optimized to minimize time-to-hire.
The system learns to quickly screen out candidates and move the best candidates
to offer. Hiring is fast. But months later, hired candidates underperform or
leave quickly. The hiring model optimized speed, not quality. The long-term
outcome (retention, performance) contradicted the short-term optimization
target.

A content recommender optimized for watch-time per session learns to recommend
content that keeps users engaged in the moment. Over weeks, users become
fatigued, platform trust erodes, and monthly active users decline. The
recommendation model optimized a metric that contradicted the true business
objective over a longer horizon.

The core issue is that business outcomes are complex and delayed. Revenue does
not arrive immediately; it is the cumulative result of retention, repeat
purchase, and referrals over months and years. A model optimized for a
short-term metric cannot capture this. It becomes a measure of short-term
behavior, not long-term value.

The technical solution is to optimize for long-term outcomes directly or to add
explicit decay factors that penalize short-term gains that harm long-term value.
A causal model can reason about how short-term actions affect long-term
outcomes.

#strong[Key idea]: Short-term proxies and long-term outcomes often contradict.
Optimizing a short-term proxy often harms the long-term outcome. Models must be
evaluated on outcomes that matter over the decision-maker's true time horizon.

// Slide: Strategic and Adversarial Response

=== Strategic and Adversarial Response

Once a model is deployed, the people it scores learn to optimize against it.
Standard ML assumes passive agents; in business, agents are not passive. They
respond strategically to the system's incentives.

Publishing the features of a credit-scoring model invites credit gaming.
Borrowers learn the features the model uses and optimize against them: they
might open new credit accounts to improve utilization ratios, time large
purchases to avoid showing recent debt, or other gaming tactics. The model's
predictions degrade not because the model itself changed but because the
population it scores changed.

Publishing a search-ranking algorithm invites keyword-stuffing. Website owners
reverse-engineer the ranking algorithm and optimize their pages for it—bulking
up keywords, gaming link profiles, crafting meta-descriptions that exploit the
algorithm's patterns. Search results are gamed; user value declines. The ranking
algorithm's usefulness erodes.

In loan underwriting, if the model is known to weight certain factors heavily,
borrowers optimize those factors before applying. If the model weights income
heavily, a borderline borrower might time their application to when their income
is highest (and possibly unsustainably high). The model's predictions become
less reliable.

The key insight is that a model trained on how agents behaved before deployment
becomes wrong the moment agents learn how it scores them and adapt. The game has
changed. The model must anticipate adaptation or expect to fail.

This is not a bug in the model; it is a feature of strategic environments.
Real-world systems with high stakes attract strategic response. The alternative
to strategic adaptation is to change what is optimizable or to accept that the
system will be gamed.

#strong[Key idea]: In strategic settings, deployed models change the behavior
they were trained to predict. This requires either building adaptive systems
that anticipate gaming, changing what is optimizable, or accepting performance
degradation over time.

== Why This Matters

=== Why AI Projects Fail

// Slide: Why AI Projects Fail

Most AI project failures are not modeling failures. They are framing failures.
The model is accurate, but it is answering the wrong question, optimizing the
wrong objective, or operating in the wrong context.

#strong[Misalignment] is common. The model optimizes a proxy metric, not the
business goal it stands in for. Recommendation systems optimized for engagement
destroy trust. Hiring models optimized for pattern-matching inherit historical
bias. Credit models optimized for default prediction approve the wrong
populations. The model is accurate relative to its objective, but the objective
is wrong.

#strong[Black boxes] prevent adoption. Outputs cannot be explained, so they are
not trusted by stakeholders or regulators. A fraud model might be 95% accurate,
but if it cannot explain why a transaction was blocked, customers and regulators
demand accountability. The model, however accurate, is not deployable.

#strong[No lever] means a score is delivered where an action was needed. A
customer churn score tells who is at risk but not what to do about it. A staff
attrition prediction tells which employees might leave but not how to retain
them. A bare prediction does not guide action.

#strong[No feedback] means performance is never monitored after deployment.
Models degrade over time due to concept drift, adversarial adaptation, and
feedback loops. But if the business does not measure model performance in
production, degradation is invisible. The model continues outputting
predictions, but they grow stale.

An accurate model that answers the wrong question is a failed project, however
good its metrics look on a dashboard. The technical definition of success—high
cross-validation accuracy—is not the same as business success—achieving the
goal.

#strong[Key idea]: Framing—choosing the right problem to solve—often matters
more than execution. An accurate answer to the wrong question is a failed
project.

=== Four Costs, One Root Cause

// Slide: Four Costs, One Root Cause

The four costs surveyed in this lesson—ignoring causality, uncertainty, the
business objective, and dynamics—look unrelated but share a single root cause.

Each one arises from optimizing #strong[prediction accuracy on a fixed
  distribution] instead of #strong[decision quality on a distribution the
  decision itself changes].

A causal model can reason about interventions. An uncertain model can quantify
confidence. A well-aligned objective guides decisions toward what matters. A
dynamic model anticipates feedback and adaptation. Each addresses one of the
four costs.

But they address a single underlying problem: the gap between prediction and
decision. A prediction is a guess about a fixed world. A decision is an action
in a world that responds to that action. Standard ML is built for prediction.
This book is built for decision.

Fixing all four costs at once is not four separate projects. It is one shift in
what the pipeline is built to optimize: from prediction to decision, from static
to dynamic, from correlation to causation, from point estimates to uncertainty
quantification.

#strong[Key idea]: Every later technique in this book plugs into one loop
through data, model, policy, action, and feedback.

=== Roadmap: Where the Book Goes From Here

// Slide: Roadmap: Where the Book Goes From Here

This lesson catalogued what a purely predictive pipeline misses. The rest of the
book builds the pipeline that does not miss it.

#strong[Part II] supplies the probabilistic and causal foundations. Gaussian
processes allow flexible modeling with uncertainty quantification. Variational
inference scales Bayesian computation. Normalizing flows model complex
distributions. Causal discovery learns causal structure from data.

#strong[Part III] turns those tools into single-step decisions. Decision theory
formalizes the choice between actions under uncertainty. Policy learning
optimizes decisions given a causal model. Partial identification handles cases
where data alone cannot determine all quantities of interest.

#strong[Part IV] extends to multi-step and dynamic decisions. Causal world
models predict how the world evolves. Causal reinforcement learning optimizes
sequences of decisions over time. Feedback loops are explicitly modeled and
managed.

#strong[Part V] covers deploying, monitoring, and governing the resulting
decision systems in production. A model that works in training must be monitored
for drift and failure. Decisions must be explainable to stakeholders. Feedback
loops must be managed to prevent harm.

Every later technique plugs into one loop: data informs the model, the model
informs policy, policy guides action, and action produces feedback. Data informs
the model. The model informs policy. Policy guides action. Action produces
feedback. The loop closes.

#strong[Key idea]: Decision-making under uncertainty and causality is learnable.
This book shows how. The path from data to decisions is systematic, teachable,
and applied throughout industry and science.
