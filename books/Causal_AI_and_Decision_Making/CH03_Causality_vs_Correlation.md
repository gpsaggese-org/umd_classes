# Causality Vs. Correlation
Every data scientist has heard the phrase: "correlation does not imply
causation." Yet, despite this widespread awareness, the distinction is
surprisingly easy to violate in practice. This chapter builds the conceptual and
mathematical foundation for understanding why correlation falls short, what
causation really means, and how to reason rigorously about cause-and-effect
relationships using the language of causal graphs.

We begin with spurious correlations and the famous Simpson's paradox — cases
where the data actively misleads you. We then introduce the key structural
elements of causal reasoning: confounders, colliders, and the do-calculus. By
the end of the chapter, you will have the vocabulary and the tools to ask — and
answer — causal questions with the same rigor you bring to predictive modeling.

## Spurious Correlations and Simpson's Paradox

### The Danger of Pattern-Matching
- Modern machine learning is exceptionally good at finding patterns in data —
  but patterns are not causes
- A model trained on correlational data will faithfully reproduce whatever
  regularities exist in the training set, including ones that are completely
  accidental
- The internet has made the problem vivid: Tyler Vigen's "Spurious Correlations"
  website documents dozens of near-perfect statistical associations between
  completely unrelated variables:
  - Per capita cheese consumption and deaths by bedsheet tangling ($r = 0.947$)
  - Nicolas Cage films released per year and pool drownings ($r = 0.666$)
- These are absurd, but the same trap appears in serious scientific and business
  contexts all the time

### What Makes a Correlation Spurious
- A **spurious correlation** is a statistical association between two variables
  that is not caused by any direct or indirect causal link between them
- The association usually arises from one of three sources:
  - **Common cause (confounding)**: a third variable causes both, making them
    move together (e.g., temperature drives both ice cream sales and drowning
    rates)
  - **Selection bias**: the sample was filtered in a way that creates artificial
    dependence
  - **Chance**: with enough variables tested, random high correlations are
    inevitable (multiple comparisons problem)
- A correlation-based model cannot distinguish these cases from genuine
  causation — and neither can the data alone without additional structural
  assumptions

### Simpson's Paradox
- **Simpson's paradox** is one of the most striking illustrations of how
  aggregated statistics can reverse when you condition on a relevant subgroup
- The classic form: a treatment appears beneficial in aggregate but harmful in
  every subgroup — or vice versa
- **Classic example: UC Berkeley admissions (1973)**
  - Aggregate data showed men were admitted at higher rates than women,
    suggesting gender discrimination
  - When broken down by department, women were admitted at equal or higher rates
    in most departments
  - The paradox arose because women disproportionately applied to more
    competitive departments
  - The aggregate "correlation" between gender and admission was entirely an
    artifact of the confounding variable: department selectivity
- **Medical example: kidney stone treatment**
  - Treatment A appears more effective than Treatment B in aggregate
  - But Treatment B is better in both small-stone and large-stone subgroups
  - The paradox: Treatment A was preferentially given to smaller
    (easier-to-treat) stones, inflating its apparent effectiveness
- **Why this matters**
  - Simpson's paradox is not a statistical curiosity — it reveals that summary
    statistics are always conditional on an implicit choice of what to aggregate
    over
  - The "right" disaggregation is not a statistical question; it requires causal
    knowledge about which variables are confounders
  - Resolving Simpson's paradox requires asking: which subgroup analysis
    reflects the true causal mechanism?

### The Resolution: Causal Models
- Pure statistics cannot resolve Simpson's paradox on its own
- The correct analysis depends on understanding the causal structure:
  - If the grouping variable (e.g., department) is a confounder, you should
    stratify by it
  - If it is a mediator (part of the causal pathway), you should not
- This is why Judea Pearl argues that statistics alone is insufficient — you
  need a causal model to decide which associations to trust

**Resources**

- Judea Pearl and Dana Mackenzie, _The Book of Why: The New Science of Cause and
  Effect_ (2018), Chapter 6
- C.R. Blyth, "On Simpson's Paradox and the Sure-Thing Principle," _Journal of
  the American Statistical Association_ (1972)
- Tyler Vigen, _Spurious Correlations_ (2015)
- Bernhard Scholkopf et al., "Toward Causal Representation Learning," _PNAS_
  (2021)

## Confounding Variables and Colliders
Understanding what can distort a causal analysis is just as important as knowing
how to estimate a causal effect. Two structural patterns in causal graphs are
responsible for most of the common errors in causal inference: **confounders**
and **colliders**.

### Confounders: the Most Common Threat
- A **confounding variable** (confounder) is a variable that causally influences
  both the treatment (cause) and the outcome (effect)
- Because a confounder affects both sides, it creates a spurious statistical
  association between treatment and outcome that is not causal
- **Formal structure in a DAG**:
  - $C \rightarrow X$ (confounder affects treatment)
  - $C \rightarrow Y$ (confounder affects outcome)
  - $X \rightarrow Y$ (actual causal relationship of interest)
- The problem: if you observe $X$ and $Y$ moving together, you cannot tell how
  much is due to the real causal path $X \rightarrow Y$ versus the backdoor path
  $X \leftarrow C \rightarrow Y$

- **Canonical example: ice cream and drowning**
  - Ice cream sales and drowning rates are positively correlated
  - No causal relationship between them
  - The confounder is temperature: hot weather causes both more ice cream
    consumption and more swimming activity (and thus more drownings)
  - Controlling for temperature (e.g., by looking at the relationship within
    temperature bands) makes the spurious association disappear

- **Business example: consulting and business performance**
  - There is a correlation between hiring top-tier consulting firms and having
    strong business performance
  - But the causal arrow may run the other way: successful businesses with large
    budgets can afford top consulting firms
  - The confounder is underlying business health, which influences both
    decisions

- **How to handle confounders**
  - The gold standard is randomized controlled experimentation: random
    assignment of treatment breaks the link $C \rightarrow X$ by design
  - In observational settings, methods include:
    - Regression adjustment (include the confounder as a covariate)
    - Propensity score matching (balance the groups on observed confounders)
    - Instrumental variable methods (find a variable that affects treatment but
      not outcome directly)
    - Difference-in-differences (use time variation to remove stable
      confounders)
  - All observational methods require the assumption that the relevant
    confounders are observed — if important ones are hidden, bias remains

### Mediators Vs. Confounders
- A **mediator** lies on the causal pathway from treatment to outcome:
  $X \rightarrow M \rightarrow Y$
- Confounders and mediators have opposite implications for analysis:
  - You should control for confounders to remove spurious associations
  - You should generally _not_ control for mediators if you want the total
    causal effect of $X$ on $Y$ — doing so blocks the very pathway you care
    about
- **Example: training and productivity**
  - A training program $X$ may improve productivity $Y$ by first increasing job
    satisfaction $M$: $X \rightarrow M \rightarrow Y$
  - If you control for job satisfaction in a regression, you remove the
    mechanism through which training works, underestimating the total effect
  - The distinction between direct and indirect effects requires mediation
    analysis

### Colliders: the Less Obvious Trap
- A **collider** is a variable that is caused by two or more other variables:
  $B \rightarrow A \leftarrow C$
- Unlike confounders, a collider naturally blocks information flow between its
  causes — $B$ and $C$ are independent given nothing
- The trap: **conditioning on a collider** opens a spurious association between
  its causes that did not exist before
  - This is known as **collider bias** or Berkson's paradox
  - It arises whenever you filter a sample by a variable that is affected by
    both treatment and outcome (or by two other variables you care about)

- **Example: exercise, diet, and body weight**
  - Both exercise $E$ and diet $D$ independently affect body weight $W$:
    $E \rightarrow W \leftarrow D$
  - In the general population, $E$ and $D$ are independent — knowing someone
    exercises tells you nothing about their diet
  - But if you condition on body weight (e.g., study only people with a specific
    BMI range), you introduce a spurious negative correlation: among people with
    the same weight, those who exercise more tend to have worse diets, and vice
    versa
  - This is a statistical artifact created by the conditioning, not a real
    causal relationship

- **Real-world collider traps**
  - **Hospitalization bias**: patients admitted to a hospital have either
    disease A or disease B. If you study the correlation between A and B in
    hospitalized patients only, you induce spurious negative correlation — this
    is a classic collider bias
  - **Publication bias**: papers are published (selected) if they are either
    high-quality or surprising. Among published papers, quality and
    surprise-value appear negatively correlated — another collider artifact
  - **Selection in tech hiring**: candidates are hired if they have either
    strong coding skills or strong communication skills. Among hired employees,
    the two skills will appear negatively correlated even if they are positively
    correlated in the general population

### The Path Taxonomy
- Understanding causal graphs requires categorizing the types of paths:
  - **Fork** ($D \leftarrow X \rightarrow C$): a common cause creates spurious
    association; conditioning on the fork blocks the path
  - **Chain** ($X \rightarrow M \rightarrow Y$): a mediating path; conditioning
    on $M$ blocks the causal flow
  - **Inverted fork / collider** ($X \rightarrow A \leftarrow C$): independent
    by default; conditioning on $A$ opens a spurious path

- This taxonomy is the basis for **d-separation**, the formal criterion for
  reading conditional independencies from a DAG (covered in the next section)

**Resources**

- Judea Pearl, _Causality: Models, Reasoning, and Inference_, 2nd ed. (2009),
  Chapter 2
- Miguel Hernan and James Robins, _Causal Inference: What If_ (2020) — freely
  available at hsph.harvard.edu/miguel-hernan/causal-inference-book
- Elias Bareinboim and Judea Pearl, "Causal Inference and the Data-Fusion
  Problem," _PNAS_ (2016)
- Sander Greenland, "Quantifying Biases in Causal Models," _Epidemiology_ (2003)

## Causal Questions Vs. Predictive Questions
A central theme in causal AI is the distinction between two fundamentally
different types of questions that look superficially similar but require
completely different tools to answer.

### The Core Distinction
- A **predictive question** asks: _"Given what I observe, what should I
  expect?"_
  - It is answered by conditional probability: $\Pr(Y | X = x)$
  - It requires observational data and a good statistical model
  - E.g., "Given that a patient has these symptoms, what is the probability of
    disease?"

- A **causal question** asks: _"If I intervene and set $X = x$, what will happen
  to $Y$?"_
  - It requires a causal model and the do-operator: $\Pr(Y | \text{do}(X = x))$
  - It cannot be answered from observational data alone without additional
    structural assumptions
  - E.g., "If I prescribe this drug, what will happen to the patient's
    outcomes?"

- These questions have different answers whenever confounders are present:
  $\Pr(Y | X = x) \neq \Pr(Y | \text{do}(X = x))$

### Pearl's Ladder of Causation
- Judea Pearl organizes causal reasoning into three levels, each requiring
  progressively richer reasoning:

- **Rung 1: Association** — $\Pr(Y | X)$
  - Activity: passive observation
  - Question: "What is? How are things related?"
  - Example: "What does a fever tell us about the likelihood of flu?"
  - This is the domain of all traditional statistics and machine learning
  - Requires only data

- **Rung 2: Intervention** — $\Pr(Y | \text{do}(X), Z)$
  - Activity: active manipulation
  - Question: "What if? What happens if we do something?"
  - Example: "If we ban smoking in restaurants, will lung cancer rates drop?"
  - Example: "What happens to sales if we cut prices by 10%?"
  - Requires a causal model — not just data
  - This is the domain of randomized experiments and do-calculus

- **Rung 3: Counterfactuals** — $\Pr(Y_X | x', y')$
  - Activity: imagination and retrograde reasoning
  - Question: "Why? What would have happened under different circumstances?"
  - Example: "Would this patient have recovered if we had given them the
    treatment?"
  - Example: "Was my marketing campaign the reason sales increased, or would
    they have increased anyway?"
  - Requires a fully specified structural causal model
  - This is the domain of policy evaluation, legal reasoning, and fairness
    analysis

### Why ML Cannot Answer Causal Questions Alone
- Standard machine learning operates entirely at Rung 1 — it learns patterns
  from observational data
- This makes it highly effective for prediction tasks where the test
  distribution matches the training distribution
- But it fails for causal questions because:
  - **Interventions change the distribution**: when you intervene on $X$, you
    break the statistical relationships that held during data collection
  - **Correlation exploits confounding**: ML models may use a confounder as a
    shortcut feature; when you intervene, the confounder no longer predicts the
    outcome in the same way
  - **Models are not stable under policy changes**: this is the **Lucas
    critique** — empirical relationships break down when the policy changes,
    because the underlying structural relationships are different from the
    observed correlations

- **Business example: pricing**
  - An ML model trained on historical pricing data learns that high prices
    correlate with high sales (perhaps because premium pricing was used during
    peak demand periods)
  - If you act on this model by raising prices, the intervention changes the
    data-generating process — the ML model is not predicting what will happen
    under the intervention, only what has been observed

### Framing the Right Question
- In practice, most high-value business questions are causal:
  - "What is the impact of this marketing campaign?" (Rung 2)
  - "What would revenue have been if we had not run the promotion?" (Rung 3)
  - "Which customers would churn if we remove this feature?" (Rung 3)
  - "What happens to bank margins if we increase credit lines?" (Rung 2)
- Answering them requires explicitly choosing the right level of the ladder and
  the right modeling tools

**Resources**

- Judea Pearl, "The Seven Tools of Causal Inference with Reflections on
  Education," _Communications of the ACM_ (2019)
- Robert Lucas, "Econometric Policy Evaluation: A Critique," in _The Phillips
  Curve and Labor Markets_ (1976) — the original statement of the Lucas critique
- Elias Bareinboim, "Causal Reinforcement Learning," tutorial at NeurIPS (2020)
- Bernhard Scholkopf, "Causality for Machine Learning," in _Probabilistic and
  Causal Inference: The Works of Judea Pearl_ (2022)

## DAGs and D-Separation: the Language of Causal Reasoning
To reason systematically about causality, we need a formal language that can
represent causal structure, make assumptions explicit, and allow us to derive
what can and cannot be estimated from data. **Directed Acyclic Graphs** (DAGs)
and the concept of **d-separation** provide exactly this.

### What Is a Causal DAG?
- A **Directed Acyclic Graph** (DAG) is a graph where:
  - **Nodes** represent variables (observed or unobserved)
  - **Directed edges** ($X \rightarrow Y$) represent direct causal
    relationships: $X$ is a direct cause of $Y$
  - **Acyclic**: no variable can be its own cause (no feedback loops)

- The direction of an arrow matters deeply:
  - $Fire \rightarrow Smoke$ says fire causes smoke
  - $Smoke \rightarrow Fire$ says smoke causes fire
  - These are statistically equivalent Bayesian networks but causally opposite
  - Only the causal DAG supports reasoning about interventions

- A causal DAG encodes structural assumptions, not just statistical ones:
  - The absence of an edge $X \rightarrow Y$ is a strong assumption: $X$ has no
    direct causal effect on $Y$ (though it may have an indirect effect)
  - These assumptions come from domain knowledge, not from data

### Structural Causal Models
- A **Structural Causal Model** (SCM) makes a causal DAG quantitative
- Each variable $X_i$ is defined by a structural equation:
  $$
  X_i = f_i\bigl(\text{Parents}(X_i),\, \varepsilon_i\bigr)
  $$
  where $\varepsilon_i$ is an exogenous noise term capturing unmodeled variation
- Structural equations are assignments (like code), not symmetric equations:
  - $Smoke := f(Fire, \varepsilon_{Smoke})$ means fire determines smoke
  - You cannot invert this to say $Fire := f(Smoke, \varepsilon_{Fire})$

- **Example: Sprinkler system**
  - $Cloudy \rightarrow Sprinkler$, $Cloudy \rightarrow Rain$,
    $Sprinkler \rightarrow WetGrass$, $Rain \rightarrow WetGrass$,
    $WetGrass \rightarrow GreenerGrass$
  - Structural equations:
    - $C := f_C(\varepsilon_C)$ (cloudy weather has no parents in the model)
    - $R := f_R(C, \varepsilon_R)$
    - $S := f_S(C, \varepsilon_S)$
    - $W := f_W(R, S, \varepsilon_W)$
    - $G := f_G(W, \varepsilon_G)$
  - The joint distribution factorizes as:
    $$
    \Pr(C, R, S, W, G) = \Pr(C)\,\Pr(R|C)\,\Pr(S|C)\,\Pr(W|R,S)\,\Pr(G|W)
    $$

### D-Separation: Reading Independence From a DAG
- **D-separation** (directional separation) is the formal criterion for
  determining whether two variables are conditionally independent given a set of
  observed variables, purely from the graph structure
- "D-separated" means "blocked" — all paths between two variables are blocked
  given the conditioning set $Z$
- A path is **blocked** by a conditioning set $Z$ if:
  - It contains a **chain** $X \rightarrow M \rightarrow Y$ or a **fork**
    $X \leftarrow M \rightarrow Y$, and $M \in Z$ (conditioning on the middle
    node blocks the path)
  - It contains a **collider** $X \rightarrow A \leftarrow Y$ (or has $A$ as an
    ancestor of $Z$), and $A \notin Z$ — an unconditioned collider naturally
    blocks the path
- Conditioning on a collider _opens_ a path that was otherwise blocked

- **Reading the rules**:
  - **Fork blocked**: $A \leftarrow B \rightarrow C$ — $A$ and $C$ become
    independent once you condition on $B$
  - **Chain blocked**: $A \rightarrow B \rightarrow C$ — $A$ and $C$ become
    independent once you condition on $B$ (the mediator)
  - **Collider opened**: $A \rightarrow B \leftarrow C$ — $A$ and $C$ are
    independent by default, but conditioning on $B$ induces dependence

- **The key theorem**: if $X$ and $Y$ are d-separated by $Z$ in the DAG, then
  $X \perp\!\!\!\perp Y \mid Z$ in every distribution compatible with the DAG
  (the **Markov condition**)

### Observed, Unobserved, Endogenous, and Exogenous Variables
- **Observed variables**: directly measured in the data (e.g., income,
  education, blood pressure)
- **Unobserved (latent) variables**: exist in the causal system but are not
  captured in the data (e.g., motivation, genetic predisposition)
  - Ignoring unobserved confounders leads to biased causal estimates
  - Represented in DAGs as dashed nodes or as bidirected edges between affected
    variables
- **Endogenous variables**: determined by other variables within the model (have
  parents in the DAG)
- **Exogenous variables**: determined outside the model — they have no parents,
  representing background conditions or external interventions

### The Do-Operator and Graph Surgery
- Pearl's **do-operator** $\text{do}(X = x)$ formalizes what an intervention
  means in a causal model
- An intervention on $X$ corresponds to **graph surgery**: remove all incoming
  edges to $X$ and set $X = x$
  - This severs the relationship between $X$ and its natural causes
    (confounders)
  - It models the difference between "we observe $X = x$" and "we set $X = x$"
- **Adjustment formula**: under certain conditions (no unobserved confounders,
  no selection bias), the interventional distribution can be estimated from
  observational data by conditioning on all confounders:
  $$
  \Pr(Y | \text{do}(X = x)) = \sum_z \Pr(Y | X = x, Z = z)\,\Pr(Z = z)
  $$
  - This is the **backdoor adjustment formula** — it adjusts for all variables
    that block the backdoor paths (paths from $X$ to $Y$ going through
    confounders)

### Building a Causal DAG in Practice
- Constructing a causal DAG is an iterative, domain-driven process:
  - Start with the treatment and outcome of interest
  - Add variables that causally affect either the treatment or the outcome
  - Distinguish confounders (affect both) from mediators (lie on the path) from
    colliders (affected by both)
  - Mark which variables are observed vs. unobserved
  - Validate the implied conditional independencies against the data
- The DAG is a communication tool as much as a technical one — it makes
  assumptions explicit and forces alignment between domain experts and analysts

**Resources**

- Judea Pearl, _Causality: Models, Reasoning, and Inference_, 2nd ed. (2009)
- Jonas Peters, Dominik Janzing, and Bernhard Scholkopf, _Elements of Causal
  Inference_ (2017) — open access at mitpress.mit.edu
- Miguel Hernan, "A Second Chance to Get Causal Inference Right: A
  Classification of Data Science Tasks," _Chance_ (2019)
- Ilya Shpitser and Judea Pearl, "Identification of Joint Interventional
  Distributions in Recursive Semi-Markovian Causal Models," AAAI (2006)

## TUTORIAL: DoWhy (illustrating the Difference Between Correlation and Causal Effect)

## TUTORIAL: CausalImpact (detecting Causal Impact of Interventions Vs. Spurious Trends)