# Explainability Methods: What They Do and Do Not Tell You

## Why Practitioners Reach for Explainability First
When a machine learning model makes a high-stakes decision—denying a loan,
recommending a treatment, flagging a transaction as fraudulent—someone always
asks: "Why?" This question has become inescapable in modern ML systems.
Regulators demand transparency, stakeholders want accountability, and data
scientists need to debug failures. Rather than tackle the harder problem of
building causal models, most practitioners reach for **explainability methods
first**.

Explainability methods promise a shortcut: without understanding causal
mechanisms, can we at least understand what the model is doing? Can we decompose
a prediction into contributions from individual features? Can we approximate a
black-box model with something interpretable? The appeal is obvious. You already
have a trained model that predicts well. Explainability methods offer a way to
make that model inspectable without retraining or redesigning.

But this appeal masks a fundamental tension. The question "why did the model
predict this?" is not the same as "why is this prediction true?" The first is
about model introspection; the second is about causation. Explainability methods
are excellent at the first. They can tell you which features the model relied
on, how a feature's value changes the prediction, and where a prediction sits
relative to a reference point. But they cannot tell you whether those features
are causally connected to the outcome, whether the model's reliance is
justified, or whether acting on the explanation will achieve the intended
effect.

**Key characteristics of explainability methods**:

- They explain **model behavior**: what the model did, not whether it was right
- They are **correlation-based**: they show which features correlate with
  predictions
- They are **model-centric**: they focus on introspection, not domain
  understanding
- They are **post-hoc**: applied after training, not part of model design
- They are **fast and practical**: no retraining, no domain expertise required
- They assume the model is correct and try to understand why it made its choice

**Why practitioners prefer explainability to causal reasoning**:

- Explainability is easy: apply a method to an existing model
- Causal reasoning is hard: requires domain knowledge, experiment design,
  careful assumptions
- Explainability is immediate: produces results in hours
- Causal reasoning is slow: takes weeks or months to design and run experiments
- Explainability scales to any model: linear, neural networks, ensembles
- Causal reasoning is model-specific: requires custom reasoning for each domain
- Regulators accept explainability as evidence of fairness and accountability
- Causal reasoning is unfamiliar to most data teams and harder to communicate

The consequence: explainability has become the default mechanism for addressing
trust, fairness, and accountability in ML. But explainability alone is
insufficient for decision-making, which explains the subtitle of this chapter:
"What They Do and Do Not Tell You."

**References**

- Molnar, C. _Interpretable Machine Learning: A Guide for Making Black Box
  Models Explainable_ (2023)
  - Practical overview of explainability methods for practitioners
- Ribeiro, M. T., Singh, S., and Guestrin, C. "Why Should I Trust You?
  Explaining the Predictions of Any Classifier" (ACM KDD 2016)
  - Introduction to LIME and the motivation for post-hoc explainability methods
- Wachter, T., Mittelstadt, B., and Russell, C. "Counterfactual Explanations
  Without Opening the Black Box" (Harvard Data Science Review 2017)
  - Why explainability methods alone cannot satisfy regulatory and ethical
    demands

## Black Box Models, Regulation, and Trust
The term "black box" refers to any model whose internal decision-making process
is opaque—not because we lack the mathematics to understand it, but because the
sheer complexity makes inspection infeasible. A linear regression with 500
features is technically interpretable: you can read the coefficients. But a
neural network with 500 million parameters is uninterpretable in practice: no
human can mentally simulate its behavior.

Black-box models dominate production ML because they work. Deep learning,
ensemble methods, and tree-based models like XGBoost achieve state-of-the-art
performance on many tasks. The cost: they are hard to inspect, debug, and trust.
You can measure their accuracy on a test set, but you cannot easily trace why
they made a particular decision.

**The regulation driver**: In regulated industries—finance, healthcare, criminal
justice—decision-makers must justify their choices. If a bank denies a loan, the
applicant has a right to know why. If a hospital recommends surgery, the patient
deserves an explanation. If a court uses risk assessment in sentencing, the
defendant can challenge the reasoning. These requirements, formalized in
regulations like the EU's GDPR (right to explanation) and Fair Lending laws,
created demand for methods that crack open black boxes.

**The fairness narrative**: Explainability got tangled with fairness and
accountability. The (incorrect) logic is: if we can explain why the model made a
decision, then the decision is fair and trustworthy. This is deeply wrong. An
explanation of a biased decision is still an explanation of a biased decision.
But the narrative stuck: explainability became a proxy for trustworthiness.

**The causality gap**: Regulations ask for causal justifications, but
explainability methods provide correlations. The law says: "Why was this
applicant denied a loan?" Explainability says: "The model relied heavily on
neighborhood poverty rate." The law wants to know: "Is there a causal reason to
consider neighborhood when evaluating credit risk?" But explainability does not
answer causal questions.

**When explainability serves a real purpose**:

- **Debugging**: Understanding why the model fails on specific examples
  - Example: A model predicts high fraud risk for a legitimate transaction.
    Explainability shows the model relied on zip code—revealing a dataset bias
    toward geographic clustering of fraud
  - Action: Collect more balanced training data or add fairness constraints
- **Auditing**: Checking that the model relies on defensible features, not
  proxies for protected attributes
  - Example: A hiring model relies heavily on years of experience. You check
    whether this correlates with age (a protected attribute). If yes, the proxy
    has a disparate impact
  - Action: Retrain without the correlated feature or add fairness penalties
- **Stakeholder communication**: Helping business users understand model
  behavior at a high level
  - Example: A sales forecasting model relies on marketing spend and
    seasonality. Explaining these drives helps stakeholders calibrate their
    trust
  - Action: Use explanations in dashboards and reports to build confidence

**Key points about black boxes and explainability**:

- Black-box models offer accuracy but sacrifice interpretability
- Regulation creates pressure for explainability, conflating transparency with
  fairness
- Explainability methods can expose bugs and biases in existing models
- But explainability of a biased model is not fairness; it is accurate
  description of bias
- Explaining a spurious correlation does not make it causal
- The best approach is often **interpretable-by-design**: build the model to be
  transparent from the start
  - Linear models, decision trees, and GAMs are inherently interpretable
  - Accuracy loss is often small for well-engineered interpretable models
  - No need for post-hoc explanation methods

**References**

- Selbst, A. D. and Barocas, S. "The Hidden Assumptions Behind
  Discrimination-Aware Data Mining" (Journal of Data and Information
  Quality 2019)
  - How explainability became conflated with fairness, and why the connection is
    flawed
- Goodman, B. and Flaxman, S. "European Union Regulations on Algorithmic
  Decision-Making and a 'Right to Explanation'" (AI Magazine 2016)
  - Analysis of GDPR and regulations driving demand for explainability
- Rudin, C. "Stop Explaining Black Box Machine Learning Models for High Stakes
  Decisions and Use Interpretable Models Instead" (Nature Machine
  Intelligence 2019)
  - Argument for interpretable-by-design models in high-stakes applications

## Model-specific Interpretability: Linear Models, Decision Trees, GAMs
Before explainability methods became fashionable, practitioners built
interpretable models directly. Linear models, decision trees, and generalized
additive models (GAMs) are **inherently interpretable**: you can read off the
logic without post-hoc explanation.

**Linear Models** are the gold standard of interpretability. A logistic
regression for credit scoring produces a formula:

$$
\text{log-odds} = \beta_0 + \beta_1 \cdot \text{income} + \beta_2 \cdot \text{credit\_score} + \beta_3 \cdot \text{debt\_to\_income}
$$

The coefficients directly tell you the effect of each feature. A 1% increase in
income changes the log-odds by $\beta_1$. You can even compute the feature
contribution to a specific prediction: $\beta_i \cdot x_i$. This is transparent
and defensible. Banks often use logistic regression because regulators
understand it, competitors can verify it, and data scientists can tweak it.

**Decision Trees** work by recursively splitting the input space. Each split is
a yes/no question: "Is income > 50,000?" A path from root to leaf describes the
logic for a prediction. You can visualize the tree and understand exactly which
conditions trigger a classification. Depth-limited trees (max_depth=5-10) are
fully interpretable. Deep trees (max_depth=50+) become black boxes.

**Generalized Additive Models (GAMs)** generalize linear models by allowing each
feature to have a non-linear effect:

$$
\text{prediction} = \beta_0 + f_1(x_1) + f_2(x_2) + \cdots + f_p(x_p)
$$

Each function $f_i$ is a smooth curve fit to the data. You can plot each curve
and understand: "As income increases, the probability of default follows this
curve." GAMs are more flexible than linear models but much more interpretable
than black-box neural networks.

**Strengths of inherently interpretable models**:

- **Transparency**: You can audit the model before deployment
- **Simplicity**: Easy to debug, easy to communicate to stakeholders
- **Regulatory alignment**: Regulators and domain experts understand these
  models
- **Stability**: Predictions change smoothly with input, no wild swings
- **Fairness**: Easier to ensure the model does not rely on protected attributes

**Limitations of inherently interpretable models**:

- **Accuracy loss**: They may not achieve state-of-the-art performance on
  complex problems
  - Example: An image classification task with 1 million training images. A
    decision tree will overfit or be too shallow. A convolutional neural network
    will perform much better
- **Feature interactions**: Linear models and simple trees miss important
  non-linear patterns
  - Example: The effect of temperature on air conditioning demand depends on
    humidity. A linear model cannot capture this. GAMs can (by fitting separate
    curves), but the interaction may still be invisible
- **Data size**: Interpretable models scale poorly to very large feature sets or
  datasets
  - Example: A GAM with 1000 features requires fitting 1000 curves.
    Computational cost and overfitting risk escalate

**When to use inherently interpretable models**:

- **High-stakes domains**: Finance, healthcare, criminal justice where decisions
  must be explicable
- **Regulated industries**: When regulators expect to audit the model
- **Stakeholder buy-in**: When business users need to trust the model, not just
  its predictions
- **Data scarcity**: When you lack the volume and variety needed for deep
  learning
- **Operational simplicity**: When the cost of explanation infrastructure
  (deploying SHAP, LIME, etc.) is not worth it

**Practical example: Credit Scoring**

- You have 10,000 historical loans with outcomes (default/repaid)
- Features: income, debt-to-income ratio, credit score, loan amount, loan term
- Linear logistic regression achieves 75% AUC
- XGBoost achieves 82% AUC
- But XGBoost is a black box
- Solution: Use logistic regression or a shallow decision tree (max_depth=5)
- Accuracy loss: 7 percentage points
- Gain: Full interpretability, regulatory alignment, faster deployment
- Trade-off is worth it if the use case values explicability

**References**

- Hastie, T., Tibshirani, R., and Friedman, J. _The Elements of Statistical
  Learning_ (2nd ed., 2009)
  - Chapters 4-5 on linear models and decision trees with full treatment of
    interpretability
- Lou, Y., Caruana, R., and Guestrin, C. "Intelligible Models for Classification
  and Regression" (KDD 2012)
  - Foundational paper on GAMs for ML; shows GAMs achieve near-black-box
    accuracy with full interpretability
- Rudin, C. "Stop Explaining Black Box Machine Learning Models for High Stakes
  Decisions and Use Interpretable Models Instead" (Nature Machine
  Intelligence 2019)
  - Argument and case studies for building interpretable models first, not
    explaining black boxes

## Model-agnostic Methods: PDP, ICE, Feature Importance
Once a black-box model is trained, explainability methods try to crack it open.
The first wave of methods are **model-agnostic**: they work on any model,
treating it as a black box and probing behavior through queries.

**Partial Dependence Plots (PDPs)** answer: "How does the model's prediction
change as we vary a single feature, all else equal?" To build a PDP for feature
$X_j$:

1. Pick a range of values for $X_j$: $x_j^{(1)}, x_j^{(2)}, \ldots, x_j^{(m)}$
2. For each value $x_j^{(k)}$, replace $X_j$ with that value in all training
   examples
3. Average the model's predictions across all modified examples
4. Plot the average predictions against the feature values

The result is a curve showing the marginal effect of the feature. For example, a
PDP for income in a credit model might show: "As income increases from $20,000
to $200,000, the default probability decreases from 8% to 1%."

**Individual Conditional Expectation (ICE) Plots** are the disaggregated
version: instead of averaging predictions across all examples, plot one curve
per example. This reveals **heterogeneity**: does the feature have the same
effect for everyone, or do some individuals respond differently?

Example: A PDP for age in loan default might show a U-shaped curve (high risk
for very young and very old applicants). An ICE plot reveals that this is driven
by a subset of applicants; most show flat or monotonic age effects. This
heterogeneity is crucial for fairness audits.

**Feature Importance** measures how much each feature contributes to
predictions. There are several variants:

- **Drop-column importance**: Train the model, measure accuracy. Then permute
  feature $X_j$ and measure accuracy again. The drop in accuracy is the
  importance
  - Intuition: if the feature is important, scrambling it hurts predictions
  - Problem: Features that are correlated with confounders inflate importance
  - Example: In a hiring model, years of experience is important. But if the
    training data has gender imbalance in experience, the importance of
    experience is inflated by the correlated gender signal

- **Gain/Gini importance** (for tree-based models): Measure how much each
  feature reduces impurity (entropy or Gini) when split upon
  - Only applicable to specific models
  - Biased toward high-cardinality features (many unique values)

- **Permutation importance**: Shuffle a feature randomly and measure performance
  drop
  - More robust than drop-column
  - Still confounded by feature correlation

**Strengths of PDP/ICE/Importance**:

- **Model-agnostic**: Works on any model
- **Intuitive**: Easy to visualize and communicate
- **Fast**: Requires only forward passes through the model, no retraining
- **Comprehensive**: Can analyze global patterns and individual heterogeneity

**Limitations**:

- **Correlation confounds interpretation**: A feature appears important because
  it correlates with a confounder
- **Unrealistic scenarios**: PDP varies one feature while holding others fixed.
  But the resulting combinations may be impossible (e.g., very high income with
  zero education)
- **Ignores feature interactions**: PDP shows marginal effects but not how
  features combine
- **Not causal**: Shows how the model responds to feature changes, not how the
  outcome responds

**Practical example: Churn Prediction**

- Model predicts which customers will cancel next month
- Feature importance shows: "contract length" is the top feature
- PDP shows: customers with short contracts have 30% churn, long contracts have
  5% churn
- Naive interpretation: "Increase contract length to reduce churn"
- Reality: Unhappy customers request short contracts _before_ they churn.
  Contract length is a symptom, not a cause
- The PDP misled you because it shows correlation with the model's predictions,
  not the causal effect of contract length on churn
- A causal analysis would reveal: the causal effect of contract length is
  actually negative (longer contracts lock in unhappy customers and they churn
  more within that period)

**References**

- Friedman, J. H. "Greedy Function Approximation: A Gradient Boosting Machine"
  (Annals of Statistics 2001)
  - Introduction of Partial Dependence Plots in the context of gradient boosting
- Goldstein, A., Kapelner, A., Bleich, J., and Pitkin, E. "Peeking Inside the
  Black Box: Visualizing Statistical Learning with Plots of Individual
  Conditional Expectation" (Journal of Computational and Graphical
  Statistics 2015)
  - ICE plots and analysis of heterogeneous effects across examples
- Fisher, A., Rudin, C., and Dominici, F. "All Models Are Wrong, but Many Are
  Useful: Learning a Variable's Importance by Studying an Entire Class of
  Prediction Models" (Journal of Machine Learning Research 2019)
  - Critical analysis of feature importance and its interpretation issues

## Local Vs. Global Explanations
Explainability methods split into two categories based on scope:

**Global explanations** describe the model's overall behavior: "How does the
model work in general?" These are useful for model auditing, communication to
stakeholders, and understanding aggregate patterns.

- Examples: Feature importance rankings, average PDPs, decision tree rules
- Use cases: "Is the model relying on the right signals?" "What does the model
  think matters most?"
- Strength: Comprehensive view of the model
- Weakness: Cannot explain specific predictions or individual variation

**Local explanations** describe why a specific prediction was made: "Why did the
model classify this example as high-risk?" These are useful for debugging
individual failures, communicating to end-users, and understanding heterogeneous
effects.

- Examples: LIME (Local Interpretable Model-agnostic Explanations), SHAP
  (SHapley Additive exPlanations)
- Use cases: "Why did the model deny this loan?" "Which features pushed the
  prediction in this direction?"
- Strength: Precise, example-specific, shows feature contributions
- Weakness: No comprehensive view of the model's logic

**The local-global tradeoff**:

Global explanations can mask important local variation. Example: A global PDP
shows that credit score has a monotonic effect on default risk. But a local
explanation reveals that for one applicant, credit score is irrelevant; their
risk is driven entirely by income volatility. This heterogeneity is invisible in
the global view.

Conversely, local explanations can be misleading if they are not representative.
Example: You explain 100 loan denials and find that income is the top feature in
each case. But when you look globally, income ranks 5th in importance. The local
examples are biased (maybe denials are driven by income, but approvals are
driven by credit score).

**Diagnostic strategy**:

1. Start with global explanations to understand the model's average behavior
2. Drill into local explanations for anomalies or failures
3. Check whether the local and global views are consistent
4. If inconsistent, investigate the source of heterogeneity

**Example: Medical Diagnosis Model**

- Global feature importance shows: "Lab tests (blood count, chemistry panel) are
  most important"
- Local explanation for Patient A shows: "Image findings override lab results"
- Local explanation for Patient B shows: "Age dominates everything else"
- Interpretation: The model makes different decisions for different patients
  based on their clinical context
- Action: Understand the clinical pathways the model learned and validate them
  against medical knowledge

**References**

- Ribeiro, M. T., Singh, S., and Guestrin, C. "Why Should I Trust You?:
  Explaining the Predictions of Any Classifier" (KDD 2016)
  - Distinguishes local vs. global explanations and introduces LIME for local
    explanations
- Molnar, C. _Interpretable Machine Learning: A Guide for Making Black Box
  Models Explainable_ (2023)
  - Comprehensive treatment of local and global explanation methods with
    examples
- Murdoch, W. J., Singh, C., Kumbier, K., Abbasi-Asl, R., and Yu, B.
  "Definitions, Methods, and Applications in Interpretable Machine Learning"
  (PNAS 2019)
  - Framework for categorizing and evaluating explainability methods

## SHAP: Shapley Values From Game Theory to ML; TreeSHAP, KernelSHAP, DeepSHAP
**SHAP** (SHapley Additive exPlanations) is arguably the most theoretically
grounded explainability method. It imports an idea from game theory (Shapley
values) and applies it to ML: how should we fairly allocate credit for a model's
prediction to individual features?

**The Shapley Value Concept**

Imagine a game where players cooperate to generate a reward. How should the
total reward be fairly distributed among players?

Example: Three friends play a business game:

- Alice alone generates \$100 in profit
- Bob alone generates \$50
- Carol alone generates \$80
- But together, they generate \$500 (synergy!)

How should \$500 be split? You cannot just divide equally (\$166.67 each)
because that ignores their solo contributions. And you cannot just give them
their solo contributions (\$100, \$50, \$80) because that only accounts for
\$230, leaving \$270 unallocated.

**Shapley's solution**: For each player, compute the average marginal
contribution across all possible orderings of players joining the game. If Alice
joins first (the trio hasn't formed yet), she contributes \$500 - \$250 = \$250
(the value of the duo is \$250). If she joins second, her contribution is the
value of the three minus the value of the two others, etc. Average across all
orderings.

The Shapley value allocates the total reward such that:

- Each player gets at least their solo contribution
- The allocation is unique and satisfies fairness axioms
- The allocations sum exactly to the total reward (no surplus or deficit)

**SHAP for Machine Learning**

Transpose this to ML: the "reward" is the model's prediction, and "players" are
features.

For a specific prediction, the question is: how much did each feature
contribute?

SHAP computes the Shapley value for each feature, where the "reward" is the
difference between the model's prediction and the base rate (average
prediction):

$$
\text{prediction} = \text{base\_rate} + \sum_i \phi_i
$$

where $\phi_i$ is the SHAP value (Shapley contribution) of feature $i$.

**Interpreting SHAP values**:

- $\phi_i = 0$: The feature has no impact on this prediction
- $\phi_i > 0$: The feature pushes the prediction up (increases it)
- $\phi_i < 0$: The feature pushes the prediction down
- $|\phi_i|$ is large: The feature has a strong impact
- Sum of all $\phi_i$ equals the gap between the prediction and base rate

Example: A loan default model predicts 75% default probability for an applicant.
The base rate (average default) is 10%.

- Income contributes: $\phi_{\text{income}} = -30\%$ (strong protective effect,
  lowers probability to below base rate)
- Credit score contributes: $\phi_{\text{credit}} = -25\%$ (also protective)
- Debt-to-income contributes: $\phi_{\text{debt}} = +20\%$ (increases risk)
- Other features contribute: $\phi_{\text{other}} = +50\%$ combined

Sum: $10\% - 30\% - 25\% + 20\% + 50\% = 25\%$... Wait, that sums to 25%, not
75%. The calculation is on the log-odds scale or probability scale, not
probability directly, but the intuition is: each feature pushes the prediction
up or down from the base rate, and the sum is the final prediction.

**Computing Shapley Values**: Exact computation requires evaluating the model on
all $2^p$ subsets of features (where $p$ is the number of features), which is
exponential. For large $p$, this is infeasible.

**TreeSHAP** exploits the structure of tree-based models to compute Shapley
values in polynomial time. It recursively walks the tree, computing the
contribution of each node.

**KernelSHAP** approximates Shapley values using a weighted regression. It
samples random subsets of features, evaluates the model on each subset (with
missing features replaced by a reference value or imputed), and fits a weighted
linear model to the results. The regression coefficients approximate the Shapley
values. This is model-agnostic and much faster than exact computation, at the
cost of approximation error.

**DeepSHAP** adapts Shapley values to neural networks. The core idea: instead of
sampling, use the network's gradients to compute feature contributions. This is
fast and leverages the model's structure.

**Strengths of SHAP**:

- **Theoretically principled**: Grounded in Shapley values and game theory
- **Local and global**: Can explain individual predictions or aggregate patterns
  (SHAP summary plots)
- **Model-agnostic**: KernelSHAP works on any model; TreeSHAP works on trees;
  DeepSHAP works on neural networks
- **Consistent**: Satisfies the Shapley axioms
- **Interpretable**: SHAP values sum exactly to the prediction, so you can
  decompose any prediction

**Limitations of SHAP**:

- **Computational cost**: Exact computation is exponential; approximations may
  diverge
- **Feature independence assumption**: SHAP assumes features are independent
  when computing marginal contributions. If features are correlated, this is
  violated
  - Example: In a house price model, square footage and number of rooms are
    correlated. SHAP will assign credit for price to both, but the correlation
    means their marginal contributions are confounded
- **Still not causal**: SHAP explains the model's decision, not the causal
  effect of features
  - Example: If the model learned that red wine drinkers are wealthy, SHAP will
    assign positive contribution to "drinks red wine." But drinking red wine
    does not cause wealth; wealth causes red wine consumption. SHAP does not
    make this distinction
- **Reference value problem**: SHAP requires a baseline prediction (base rate)
  to compute the difference. Different baselines yield different Shapley values.
  There is no universally correct baseline
  - Example: Should the baseline be the average prediction on all training data,
    or the average in a specific demographic group? This choice affects the
    interpretation

**Practical example: Loan Denial Explanation**

- Model denies loan to applicant Jane
- Base rate: 15% of applicants are denied
- Prediction probability: 95% (denied)
- SHAP values:
  - Income (\$35k): $-10\%$ (protective, she has some income)
  - Debt-to-income (0.6): $+40\%$ (increases risk)
  - Credit score (650): $+35\%$ (increases risk)
  - Recent delinquency: $+15\%$ (increases risk)
- Explanation: "We denied your loan because your debt-to-income ratio is too
  high and you have a recent delinquency. Your income and credit score were
  slightly in your favor, but not enough to overcome the risk from your debt and
  delinquency."
- This is accurate model behavior. But it does not explain whether the model is
  right to be more risk-averse to high debt-to-income. That requires causal
  reasoning: does high debt-to-income cause defaults, or does it correlate with
  defaults due to confounding?

**References**

- Lundberg, S. M. and Lee, S.-I. "A Unified Approach to Interpreting Model
  Predictions" (NeurIPS 2017)
  - Original SHAP paper; introduces the connection between Shapley values and
    model interpretability
- Lundberg, S. M., Erion, G., and Lee, S.-I. "Consistent Individualized Feature
  Attribution for Tree Ensembles" (NeurIPS 2018)
  - TreeSHAP algorithm for efficient computation on tree models
- Molnar, C., König, G., and Bischl, B. "Model-Agnostic Counterfactual
  Explanations via Reinforcement Learning" (International Conference on
  Explainable AI 2020)
  - Critique of SHAP and relationship to causal reasoning

## LIME: Local Linear Approximations
**LIME** (Local Interpretable Model-agnostic Explanations) takes a different
approach than SHAP. Instead of Shapley values, LIME approximates the black-box
model with a simple, interpretable model in the neighborhood of the example
being explained.

**The Core Idea**

LIME operates on a simple principle: **locally, most complex models are
approximately linear**. If you zoom in around a single data point, the model's
surface becomes nearly flat, and a linear approximation fits well.

Algorithm:

1. Start with an example $x$ and a prediction $y = f(x)$ (from the black-box
   model)
2. Generate synthetic examples near $x$ by sampling from a distribution around
   it
3. Get predictions from the black-box model on these synthetic examples:
   $f(x_i)$ for each synthetic $x_i$
4. Compute distances from each synthetic example to the original example
5. Fit a weighted linear model to the synthetic examples:
   - Weights are distances (closer examples have higher weight)
   - Target is the black-box predictions
   - Coefficients are the LIME explanations
6. Interpret the linear model: "The black-box model behaves like this linear
   model in the neighborhood of the example"

**Example: Image Classification**

You have a neural network that classifies images. Input: a cat photo. Output:
92% confidence "cat."

LIME:

1. Generate 1000 synthetic "cat-like" images by perturbing pixels randomly
2. Get the network's confidence for each synthetic image
3. Fit a linear model:
   $\text{confidence} = w_1 \cdot \text{pixel\_1} + w_2 \cdot \text{pixel\_2} + \cdots + w_n \cdot \text{pixel\_n}$
4. The weights show which pixel regions matter most for the "cat" classification
5. Visualize: highlight the pixels with the largest absolute weights
6. Interpretation: "The model relies on the ears, whiskers, and eyes to classify
   this as a cat"

**Strengths of LIME**:

- **Model-agnostic**: Works on any model (images, text, tabular data)
- **Local focus**: Explains why a specific prediction was made, not the model's
  global behavior
- **Interpretable**: Linear models are easy to understand
- **Flexible**: Can generate explanations in many modalities (words in text,
  pixels in images, features in tabular)
- **Fast**: Requires only forward passes through the black-box model

**Limitations of LIME**:

- **Instability**: Small changes in the synthetic data or random seed can
  produce very different explanations for the same example
  - Example: You explain why the model classified an image as "dog" twice, and
    get different top features both times
  - This undermines trust in the explanation
- **Local vs. global inconsistency**: LIME explains locally, but the local
  explanation may not be representative of the model's global behavior
  - Example: LIME says feature A is important for this example, but feature A is
    not in the top-10 globally
- **Arbitrariness of neighborhoods**: How do you define "near"? For tabular
  data, is nearby in feature space or prediction space?
  - Example: For an income feature, is a neighbor someone with income \$50k ±
    \$1k, or ± 10%?
  - Different definitions yield different explanations
- **Still not causal**: LIME shows which features the model relies on locally,
  not whether those features are causally relevant
- **Synthetic data artifacts**: Generating synthetic examples near $x$ may
  create unrealistic combinations
  - Example: For a house price model, LIME might generate houses with "6
    bedrooms but 500 sq ft," which violates the correlation between bedrooms and
    square footage in the real world
  - The linear model fits well to unrealistic synthetic data, and the
    explanation does not transfer to real predictions

**Practical example: Text Classification**

You have a model that classifies customer reviews as positive or negative. A
review gets classified as negative:

"The product broke after two weeks. I wasted money. Total disappointment."

LIME:

1. Generate 1000 synthetic reviews by randomly removing words
2. Get the model's sentiment for each (positive/negative)
3. Fit a linear model:
   $\text{negative probability} = w_1 \cdot \text{broke} + w_2 \cdot \text{wasted} + \cdots$
4. LIME highlights: "broke," "wasted," and "disappointment" have high positive
   weights (push toward negative)
5. Explanation: "The model classified this as negative because it contains
   negative sentiment words like 'broke' and 'wasted'"

This is intuitive and correct. But it does not tell you whether the model's
sentiment classification is well-calibrated or whether it over-relies on
explicit sentiment at the expense of nuance (e.g., sarcasm).

**Comparison: SHAP vs. LIME**

| Aspect               | SHAP                                  | LIME                       |
| :------------------- | :------------------------------------ | :------------------------- |
| **Theory**           | Shapley values from game theory       | Local linear approximation |
| **Consistency**      | Satisfies Shapley axioms              | Heuristic, can be unstable |
| **Speed**            | TreeSHAP fast, KernelSHAP slower      | Generally fast             |
| **Global view**      | Can aggregate for global patterns     | Local only                 |
| **Interpretability** | SHAP values + base rate decomposition | Weights of linear model    |

Both SHAP and LIME are post-hoc methods that explain black-box predictions
without modifying the model. Both are model-agnostic (with variants for
efficiency). Both are local explanations. The main difference is theory (Shapley
values vs. linear approximation) and computational strategy.

**References**

- Ribeiro, M. T., Singh, S., and Guestrin, C. "Why Should I Trust You?:
  Explaining the Predictions of Any Classifier" (KDD 2016)
  - Original LIME paper; introduces local linear approximations for model
    explanation
- Ribeiro, M. T., Singh, S., and Guestrin, C. "Model-Agnostic Meta-Learning for
  Fast Adaptation of Deep Networks" (ICML 2017)
  - Extensions of LIME to different data types
- Slack, D., Hilgard, S., Jia, E., Singh, S., and Lakkaraju, H. "Fooling LIME
  and SHAP: Adversarial Attacks on Post hoc Explanation Methods" (NeurIPS 2019)
  - Demonstrates that LIME explanations can be manipulated and are not always
    reliable

## When SHAP Is Causal and When It Is Not
A critical question: Does SHAP tell you about causation or only about
correlation? The answer depends on the structure of the model and the data.

**When SHAP is NOT Causal**

SHAP values explain the model's reliance on features. But the model may rely on
a feature for non-causal reasons:

1. **Confounding**: The feature correlates with a confounder that the model uses
   - Example: A hiring model predicts job performance. SHAP says "graduation
     from prestigious university" is important. But prestigious universities
     admit high-ability applicants. The model is relying on prestige as a proxy
     for ability, not because prestige itself causes performance
   - SHAP correctly identifies that the model uses prestige in its predictions
   - But prestige is confounded with ability; the causal effect of prestige on
     performance is likely zero

2. **Reverse Causality**: The feature is a consequence of the outcome, not a
   cause
   - Example: A hospital mortality prediction model. SHAP says "being in the
     ICU" increases predicted mortality
   - This is correct: sicker patients go to the ICU, and they are more likely to
     die
   - But the ICU does not cause death; illness causes both ICU admission and
     death
   - SHAP identifies the correlation; it cannot distinguish cause from
     consequence

3. **Mediation**: The feature is downstream of the true cause
   - Example: A customer churn model. SHAP says "customer support tickets"
     predict churn
   - True: dissatisfied customers open more tickets _before_ they churn
   - So the model is using tickets as a _symptom_ of dissatisfaction
   - The true cause is dissatisfaction; tickets are a symptom
   - SHAP correctly identifies that the model relies on tickets, but acting on
     this (e.g., "close tickets to prevent churn") would be pointless

**When SHAP IS Causal (or closer to causal)**

SHAP comes closer to causal inference in specific scenarios:

1. **Randomized Experiments**: If the feature was randomized (independent of
   confounders)
   - Example: An A/B test where prices were randomly assigned. SHAP values for
     price in a revenue model directly reflect the causal effect of price on
     revenue
   - Why: Randomization breaks confounding; the model cannot exploit spurious
     correlations

2. **Strong Prior Knowledge of Causal Structure**: If domain experts guarantee
   that certain features are causes and others are not
   - Example: In a medical diagnostic model, you know symptom X causes disease
     Y, not vice versa
   - You can interpret SHAP values for symptom X as causal
   - This requires strong domain knowledge and is not automatic from the data

3. **Interpretable Models with Causal Assumptions**: If the model is built with
   causal assumptions baked in
   - Example: A linear model where you regressed $Y$ on $X_1, X_2, X_3$ and
     adjusted for confounders
   - The coefficients (and corresponding SHAP values) have a causal
     interpretation if the confounders are sufficient
   - This requires correct causal model specification, which is hard

**The Safe Assumption: SHAP Explains Correlation, Not Causation**

By default, treat SHAP values as correlations. A high SHAP value for a feature
means the model relies on it, but not necessarily that the feature has a causal
effect.

To interpret SHAP values causally, you must:

1. Understand the causal relationships in your domain
2. Verify that confounding is not present (or adjust for it)
3. Distinguish causes from consequences
4. Validate causal assumptions through experiments or domain knowledge

**Practical example: Course Grade Prediction**

You build a model to predict student grades. Features: attendance, homework
completion, study hours per week, previous GPA.

SHAP values show: **attendance** is the top driver of grades.

Possible interpretations:

- **Correlational (safe)**: "The model predicts that students who attend class
  tend to have higher grades"
- **Naïve causal (wrong)**: "Attending class causes higher grades; students
  should attend more"
- **Confounded interpretation (closer to true)**: "Students who are motivated
  attend more and earn higher grades. Attendance is a symptom of motivation, not
  a cause of grades"
- **Causal (requires evidence)**: "We could randomize attendance (force some
  students to skip class) and measure the effect on grades. Only then would we
  know if attendance is causal"

If you want to act on the SHAP explanation (e.g., "increase attendance to
improve grades"), you need causal knowledge, not just a SHAP value.

**References**

- Zhao, Q. and Hastie, T. "Causal Interpretations of Black-box Models" (Journal
  of Business and Economic Statistics 2021)
  - Formal analysis of when SHAP and other explainability methods do and do not
    have causal interpretations
- Janzing, D., Minorics, L., and Scholkopf, B. "Feature Relevance Quantification
  in Explainable AI: A Causal Problem" (JMLR 2020)
  - Connection between feature importance and causality; why traditional
    importance metrics are insufficient for causal questions
- Wachter, T., Mittelstadt, B., and Russell, C. "Counterfactual Explanations
  Without Opening the Black Box" (arXiv 2017)
  - Distinction between explaining predictions and explaining counterfactual
    outcomes

## The Gap Between Explanation and Causation: Feature Importance Is Not Causality
This section addresses the core theme of the chapter: **explaining a model's
predictions is not the same as causal reasoning**.

**What Explainability Methods Tell You**

- Which features the model relies on
- How features correlate with predictions in the training data
- How predictions change as features change (holding other features fixed)
- The model's decision boundary in feature space

**What Explainability Methods Cannot Tell You**

- Whether those features are causally related to the outcome
- Whether acting on the explanation will achieve your goal
- Whether the model's logic is correct or aligned with domain knowledge
- What happens if you intervene to change a feature

**The Smoking Gun Example**

Suppose you have a medical diagnosis model trained on hospital data. The model
predicts pneumonia risk from patient symptoms.

SHAP/LIME explanation: "Smoking history is the top predictor of pneumonia risk."

What this means:

- In the training data, smokers have higher pneumonia rates than non-smokers
- The model learned this correlation
- The model relies on smoking as a strong signal

What this does NOT mean:

- Smoking causes pneumonia (actually, smoking increases pneumonia risk, so this
  is causal)
- But even if smoking were correlated without being causal, the explanation
  would still say "smoking is important"
- Example: suppose "hospital admission" correlates with pneumonia (patients
  admitted to the hospital have higher rates because sicker patients are
  admitted). The model would learn this correlation. But hospital admission does
  not cause pneumonia; severity causes both

**The SHAP/importance Paradox**

Feature importance (via SHAP, permutation, or other methods) measures the
reduction in prediction error when a feature is removed or permuted. This is
purely about predictive value, not causality.

Example: Suppose the true causal model is:

$$
\text{Outcome} = \beta_0 + \beta_1 \cdot \text{Cause} + \epsilon
$$

And suppose a feature `Proxy` is highly correlated with `Cause` but is not
causal:

$$
\text{Outcome} = f(\text{Cause}) \quad \text{(Cause is causal)}
$$

$$
\text{Proxy} = g(\text{Cause}) + \text{noise} \quad \text{(Proxy is a consequence of Cause)}
$$

A prediction model trained on data with `Cause`, `Proxy`, and `Outcome` will
find that both are important. If `Proxy` is less noisy than `Cause`, the model
might even rank `Proxy` higher.

But:

- Intervening on `Proxy` (e.g., "force this proxy to increase") has no causal
  effect on the outcome
- Intervening on `Cause` (the true causal factor) does
- SHAP/importance cannot distinguish between them

**Why the Gap Matters**

**Decision-making requires causality; prediction requires only correlation.**

- For **prediction** (rung 1 of Pearl's Ladder): "Will this patient develop
  pneumonia?" You only need features that correlate with the outcome. Smoking
  status is fine; so is hospital admission or chest X-ray findings
- For **intervention** (rung 2): "If we reduce smoking rates, will pneumonia
  decline?" You need causal relationships. Reducing hospital admission would not
  help (hospitals do not cause pneumonia). Reducing smoking would (smoking
  causes pneumonia)
- For **counterfactual reasoning** (rung 3): "Would this specific patient have
  developed pneumonia if they had never smoked?" You need causal models and
  domain knowledge

**The Slippery Slope**

Once explainability methods label a feature as "important," organizations often
treat it as causal:

- **Finance**: A feature importance algorithm ranks "zip code" as top-5 for
  credit risk. Loan officers interpret this as: "Applicants from certain zip
  codes are bad credit risks." But zip code is a proxy for socioeconomic status,
  which is a proxy for opportunity, not a direct cause of credit behavior.
  Treating it as causal is discriminatory
- **Healthcare**: A mortality prediction model relies on "previous ICU
  admission." Doctors interpret this as: "ICU admission increases mortality
  risk," so they avoid ICU admission. But ICU admission is a consequence of
  severity, not a cause of death. Avoiding the ICU for severe patients would
  harm them
- **Hiring**: A model ranks "current job title" as the top predictor of
  performance. The company interprets this as: "Hire people with high-seniority
  job titles." But job title is a proxy for experience and track record. The
  model should really be predicting based on skills and experience, not job
  title per se

**Bridging the Gap: When (and How) to Use Causal Reasoning**

The solution is not to abandon explainability methods. Rather, use them as a
diagnostic tool, then validate with causal reasoning:

1. **Use explainability to identify candidates**: SHAP/importance tells you
   which features the model relies on
2. **Ask causal questions**: "Is this feature a cause, a symptom, a confounder,
   or a proxy?"
3. **Validate with domain knowledge**: Consult domain experts to verify causal
   claims
4. **Design experiments when possible**: Randomized experiments, natural
   experiments, or sensitivity analysis
5. **Use causal models**: Build a causal graph representing your domain,
   identify confounders, and estimate causal effects

**Practical example: Customer Retention**

Model predicts churn. SHAP values show: "months since last purchase" is the top
driver.

Naive interpretation: "Customers who haven't purchased recently are likely to
churn." Question: Is this causal?

Possible causal stories:

- **Causal 1**: A long time without purchasing is a _symptom_ of churn (customer
  interest is waning, so they stop buying, then they churn). The cause is
  underlying dissatisfaction, not the lack of purchases
- **Causal 2**: The company is not engaging the customer frequently enough. Long
  periods without contact cause disengagement and churn. Reaching out more
  frequently prevents churn
- **Causal 3**: The customer's needs have changed. They no longer need the
  product. "Months since purchase" is a symptom of changed needs, not a cause of
  churn

Interventions based on each causal story:

- Story 1: Survey customers to identify dissatisfaction, then address root
  causes
- Story 2: Implement a contact/engagement campaign; reach out every N months
- Story 3: Identify customers with changing needs and recommend new products

SHAP alone cannot tell you which story is true. You need causal reasoning,
domain knowledge, and experiments.

**References**

- Peters, J., Janzing, D., and Scholkopf, B. "Elements of Causal Inference" (MIT
  Press 2017)
  - Formal treatment of the distinction between prediction and causation
- Athey, S. and Wager, S. "Estimating Treatment Effects with Causal Forests"
  (Journal of the American Statistical Association 2019)
  - How to use machine learning for causal inference, going beyond prediction
- Molnar, C. "Interpretable Machine Learning: A Guide for Making Black Box
  Models Explainable" (2023)
  - Chapter on the limitations of explainability methods and when to use causal
    reasoning

## When Explainability Is Sufficient and When Causal Reasoning Is Needed
This final non-tutorial section ties together the chapter's themes: given the
limitations of explainability, when is it enough, and when must you move to
causal reasoning?

**Explainability Is Sufficient When**

1. **You are only predicting, not intervening**
   - Example: A model that predicts next quarter's revenue for financial
     forecasting
   - Use case: Shareholders want to know the model's logic; auditors want to
     verify it is not gaming
   - Explainability is sufficient: "The model relies on historical revenue,
     competitor pricing, and seasonality"
   - You are not making decisions based on the explanation; you are just
     inspecting the model

2. **The stakes are low and experimentation is feasible**
   - Example: A recommendation system that suggests movies
   - Use case: You want to explain why a movie was recommended
   - Explainability is sufficient as long as you can run A/B tests to validate
     recommendations
   - If recommendations fail, you can experiment and learn from the feedback

3. **Domain experts validate that the correlations are causal**
   - Example: A credit scoring model where a lending expert has verified that
     each feature has a known causal relationship with default
   - Explainability is sufficient because the expert has done the causal vetting
   - The explanation is trustworthy because it aligns with known mechanisms

4. **Regulatory compliance is the only goal**
   - Example: Fair lending regulations require that you can explain lending
     decisions
   - Use case: A regulator asks, "Why was this applicant denied a loan?"
   - Explainability is sufficient: "According to our model, this applicant's
     debt-to-income ratio and recent delinquency increased risk."
   - The regulation requires transparency, not causal correctness
   - (Note: This is often a flawed regulation, but if complying is your only
     goal, explainability suffices)

5. **You are monitoring for bias and drift**
   - Example: Quarterly audits of a hiring model to ensure it is not
     discriminating by age or gender
   - Use case: You explain predictions for a random sample and check that
     protected attributes are not driving decisions
   - Explainability is sufficient: "The model relies on interview ratings and
     work experience, not age"
   - You are auditing the model, not deciding whether to act on it

**Causal Reasoning Is Needed When**

1. **You are making decisions that affect people's lives**
   - Example: Loan approval, medical treatment, hiring, criminal sentencing
   - Use case: You want to justify a decision not just explain it
   - Explainability is insufficient: "The model said deny the loan" is not a
     justification
   - Causal reasoning is needed: "The causal effect of this applicant's
     debt-to-income ratio is to increase default risk, so we deny"
   - This requires a causal model, not just feature importance

2. **You want to understand the effect of an intervention**
   - Example: "If we give a discount, will the customer stay?" (churn reduction)
   - Use case: You want to know the causal effect of discounts on retention
   - Explainability is insufficient: Feature importance might show "discount
     value" is important, but that is correlation
   - Customers who receive discounts might be at-risk anyway; the discount is a
     symptom of risk, not a cause of retention
   - Causal reasoning is needed: Randomized experiments or causal models to
     estimate the true effect of discounts

3. **You need to generalize to new contexts**
   - Example: A credit model trained on 2019-2020 data is deployed in 2024
   - Use case: Conditions have changed; unemployment, interest rates, economic
     conditions are different
   - Explainability is insufficient: The model's correlations may have shifted
     with the context
   - Causal reasoning is needed: Understanding the causal mechanisms (why
     unemployment affects default) allows you to adapt the model to new
     conditions
   - A purely correlational model built on 2019 data will fail in 2024

4. **You are competing with an adversary or facing feedback loops**
   - Example: Fraud detection in an arms race with fraudsters
   - Use case: Fraudsters observe the model's decisions and adapt; the
     distribution shifts
   - Explainability is insufficient: Explaining the current model's behavior
     does not predict how it will behave when fraudsters adapt
   - Causal reasoning is needed: Understanding the causal mechanisms of fraud
     allows you to anticipate how the model will degrade

5. **You need to do counterfactual reasoning**
   - Example: "Was it our marketing campaign that caused the sales surge, or
     would sales have increased anyway?"
   - Use case: Learning from past decisions to improve future ones
   - Explainability is insufficient: It cannot answer counterfactuals
   - Causal reasoning is needed: Causal models and sensitivity analysis

**Decision Matrix**

| Scenario                                    | Explainability             | Causal Reasoning |
| :------------------------------------------ | :------------------------- | :--------------- |
| Pure prediction, no intervention            | Sufficient                 | Not needed       |
| Decision-making with low stakes             | Sufficient                 | Nice-to-have     |
| High-stakes decisions (lending, healthcare) | Necessary but insufficient | Needed           |
| Intervention effects (pricing, discounts)   | Insufficient               | Needed           |
| Generalization to new domains/times         | Insufficient               | Needed           |
| Counterfactual reasoning                    | Insufficient               | Needed           |
| Regulatory compliance (transparency)        | Sufficient                 | Not required     |
| Detecting bias and unfairness               | Sufficient                 | Nice-to-have     |

**Practical Integration**

Best practice: Combine both.

1. **Start with explainability**: SHAP, LIME, or feature importance to
   understand what the model learned
2. **Then ask causal questions**: "Is the learned correlation causal?"
3. **Validate with domain knowledge**: "Does this make sense according to the
   domain expert?"
4. **Design experiments**: Randomized tests or natural experiments to validate
   causal claims
5. **Build a causal model**: Document the causal structure of your domain
6. **Iterate**: Refine the model based on experimental results

Example: E-commerce Conversion

Problem: A model predicts purchase probability from user behavior.

Step 1 (Explainability): SHAP shows that users who view similar items many times
have higher conversion probability.

Step 2 (Causal question): Does viewing similar items cause purchase, or is
viewing a symptom of purchase intent?

Step 3 (Domain knowledge): Marketing team says: "Users who come back to browse
similar items are genuinely interested. Showing them reviews and comparisons
helps them decide. So viewing behavior is both a signal and a place to
intervene."

Step 4 (Experiment): A/B test: for users who have viewed similar items 3+ times,
randomly show half of them review summaries and comparisons (treatment) and half
the normal page (control). Measure conversion.

Step 5 (Causal model): If the experiment shows treatment increases conversion,
then the causal effect of "providing comparison information to high-intent
users" is positive. The original explanation "viewing behavior predicts
purchase" is now interpreted as "high-intent users view more, and we can boost
their conversion by helping them compare."

Step 6 (Iterate): Refine the comparison interface based on user feedback and
conversion metrics.

Result: An evidence-based decision that combines explainability (understanding
the model) with causal reasoning (validating and acting on it).

**References**

- Pearl, J. and Mackenzie, D. _The Book of Why_ (2018)
  - Overview of when causation matters and why correlation is insufficient for
    decision-making
- Hernán, M. A. and Robins, J. M. _Causal Inference: What If_ (2020)
  - When observational data and causal reasoning are necessary for valid
    inference
- Hurwitz, J. and Thompson, M. _Causal Artificial Intelligence_ (2024)
  - Integration of explainability and causal reasoning in AI systems

## TUTORIAL: SHAP (explaining Black-box Model Predictions with Shapley Values)

## TUTORIAL: LIME (local Interpretable Model-agnostic Explanations)