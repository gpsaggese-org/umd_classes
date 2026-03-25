# Structural Causal Models

## Causal Graphs (DAGs) as a Reasoning Formalism
A Directed Acyclic Graph (DAG) is the lingua franca of modern causal inference.
Before we can estimate causal effects or reason about interventions, we need a
language for expressing _who causes whom_. DAGs provide exactly that — a visual
and mathematical representation of causal assumptions that makes them explicit,
testable, and communicable.

- **What is a DAG?**
  - **Directed**: every edge has an arrow indicating the direction of causation
    ($X \to Y$ means "$X$ causes $Y$")
  - **Acyclic**: no variable can be both a cause and a downstream effect of
    itself — causality respects temporal order
  - Nodes represent random variables; edges represent direct causal
    relationships

- **Bayesian networks vs. causal networks**
  - An ordinary Bayesian network represents a joint probability distribution
    using conditional independence structure
  - The same joint distribution can often be represented by multiple graphs with
    different edge directions
  - E.g., both $Fire \to Smoke$ and $Smoke \to Fire$ can encode the same
    statistical relationship
  - A **causal** network uses only edges that reflect true cause-and-effect
    relationships grounded in domain knowledge and the laws of nature
  - The direction of edges now has a physical meaning: $Fire \to Smoke$ is
    correct; $Smoke \to Fire$ is not
  - The asymmetry matters for interventions: extinguishing fire stops smoke;
    removing smoke does not extinguish fire

- **Structural equations as assignments**
  - Causal relationships are better understood as _assignments_ than as
    _equations_
  - In programming terms: `Smoke := f(Fire)` captures that smoke is determined
    by fire, not the other way around
  - Formally: $X_j \to X_i$ means
    $X_i := f_i(\text{Parents}(X_i), \varepsilon_i)$
  - This asymmetric notation is the foundation of Structural Causal Models

- **Benefits of causal DAGs**
  - Make causal assumptions explicit and auditable
  - Support reasoning about interventions ($do$-operator) and counterfactuals
  - Enable explainable AI by tracing causal paths
  - Provide stability: causal relationships hold across contexts and populations
    (unlike correlations, which are dataset-specific)
  - Enable causal identification: can we recover a causal effect from
    observational data?

- **Limitations of causal DAGs**
  - Require domain knowledge to specify correctly — the graph is an
    _assumption_, not a fact derived from data
  - Assume all relevant variables are included (no hidden unobserved
    confounders, unless explicitly modeled)
  - Acyclicity rules out feedback loops and simultaneous causation (though
    extensions exist)

- **A worked example: Tornado Warning**
  - Variables: $T$ (tornado forms), $W$ (warning issued), $A$ (radio
    broadcasts), $B$ (TV broadcasts), $R$ (residents warned)
  - Graph: $T \to W \to A \to R$, $W \to B \to R$
  - This encodes that residents are warned only through official channels, which
    are activated only by the Weather Service
  - **Level 1 (Association)**: "If residents are warned, was a warning issued?"
    - Yes — reading the graph upward ($R \Rightarrow W$)
    - "If radio $A$ broadcast, did TV $B$ also broadcast?"
    - Yes — both are caused by $W$ (common cause / confounder)
  - **Level 2 (Intervention)**: "If you _make_ radio broadcast ($do(A=1)$), will
    residents be warned?"
    - Yes, but the edge $W \to A$ is now severed
    - $B$ did _not_ broadcast, because forcing $A$ does not inform $W$
    - This is the key insight: "seeing $A$" and "doing $A$" yield different
      conclusions
  - **Level 3 (Counterfactual)**: "Knowing that residents were warned, would
    they still be warned if radio $A$ had not broadcast?"
    - Yes — TV $B$ still broadcasts via $W$, and residents are warned through
      $B$ alone

- **Key rule of thumb**
  - If you cannot encode your causal assumptions as a DAG before looking at
    data, you are not ready to make causal claims from that data

### References
- Judea Pearl, _Causality_ (Cambridge University Press, 2009), Chapter 1
- Daphne Koller and Nir Friedman, _Probabilistic Graphical Models_ (MIT
  Press, 2009)
- Jonas Peters, Dominik Janzing, and Bernhard Scholkopf, _Elements of Causal
  Inference_ (MIT Press, 2017), Chapter 6
- Russell and Norvig, _Artificial Intelligence: A Modern Approach_, 4th ed.,
  Chapter 13

## Structural Equations and Functional Causal Models
A causal DAG draws the skeleton of causal assumptions. Structural Causal Models
(SCMs) — also called Functional Causal Models — give that skeleton quantitative
flesh by specifying the precise mechanism by which each variable is determined.

- **Definition of an SCM**
  - An SCM consists of:
    - A set of _endogenous_ variables $X_1, \ldots, X_n$ (determined within the
      model)
    - A set of _exogenous_ variables $\varepsilon_1, \ldots, \varepsilon_n$
      (background noise, independent of each other and of other causes)
    - A structural equation for each endogenous variable:
      $$
      X_i := f_i(\text{Parents}(X_i), \varepsilon_i)
      $$
  - The exogenous variables $\varepsilon_i$ represent everything that influences
    $X_i$ that is not explicitly modeled

- **Endogenous vs. exogenous variables**
  - _Endogenous_: values determined by other variables in the model (e.g.,
    education level, income)
  - _Exogenous_: values determined outside the model — they are the "root
    causes" that drive the system (e.g., economic policy, random shocks)
  - Exogenous variables have no parents in the DAG

- **Observed vs. unobserved variables**
  - _Observed_ (measured, visible): variables directly available in the dataset
    (e.g., education, income, economic policy)
  - _Unobserved_ (latent, hidden): variables that exist but are not measured
    (e.g., motivation, natural talent)
  - Ignoring unobserved variables leads to incorrect causal conclusions
  - Classic example: $IceCreamSales \leftarrow Temperature \to DrowningRates$ —
    omitting $Temperature$ makes ice cream sales appear to cause drowning

- **The Sprinkler SCM: a worked example**
  - Variables: $C$ (Cloudy), $R$ (Rain), $S$ (Sprinkler), $W$ (Wet Grass), $G$
    (Greener Grass)
  - Structural equations:
    $$
    \begin{aligned}
    C &:= f_C(\varepsilon_C) \\
    R &:= f_R(C, \varepsilon_R) \\
    S &:= f_S(C, \varepsilon_S) \\
    W &:= f_W(R, S, \varepsilon_W) \\
    G &:= f_G(W, \varepsilon_G)
    \end{aligned}
    $$
  - $\varepsilon_W$ might represent morning dew — a source of wet grass beyond
    sprinkler and rain
  - The joint distribution factorizes as:
    $$
    \Pr(C, R, S, W, G) = \Pr(C)\Pr(R|C)\Pr(S|C)\Pr(W|R,S)\Pr(G|W)
    $$

- **Why SCMs go beyond Bayesian networks**
  - A Bayesian network encodes the joint distribution and supports inference
    (e.g., $\Pr(C | W=\text{true})$)
  - An SCM additionally supports _intervention_ ($do$-operator) and
    _counterfactual_ reasoning
  - The structural equations encode the _mechanism_, not just the _distribution_
  - Mechanisms are stable across interventions; distributions are not

- **Practical implications**
  - SCMs have been used in econometrics (structural equation models) and
    genetics (path analysis) long before formal causal theory
  - In ML pipelines, replacing statistical models with SCMs forces teams to
    articulate _why_ variables are related — often a valuable discipline in
    itself

### References
- Judea Pearl, _Causality_ (Cambridge University Press, 2009), Chapter 7
- Jonas Peters et al., _Elements of Causal Inference_ (MIT Press, 2017),
  Chapters 2–3
- Bernhard Scholkopf et al., "Toward Causal Representation Learning," _PNAS_
  (2021)
- Wright, S., "Correlation and Causation," _Journal of Agricultural Research_
  (1921) — the origin of path analysis / structural equations

## Interventions and the Do-Operator
The $do$-operator is the mathematical device that separates causal reasoning
from associational reasoning. It formalizes what it means to _intervene_ on a
system, distinguishing it from merely _observing_ the system.

- **The distinction between seeing and doing**
  - _Observing_ $X = x$: we learn that $X$ happened to take value $x$; this
    provides information about other variables via the joint distribution
  - _Intervening_ $do(X = x)$: we externally force $X$ to take value $x$,
    overriding its natural causal mechanism
  - These are fundamentally different:
    $$
    \Pr(Y \mid X = x) \ne \Pr(Y \mid do(X = x))
    $$
  - The left side is conditioned on observing $X = x$; the right side describes
    the world after forcing $X = x$

- **The mutilated graph**
  - The $do$-operator is represented graphically by _removing all incoming
    arrows to $X$_ (the "mutilated" graph)
  - When we set $do(S = \text{true})$ for the Sprinkler:
    - The edge $Cloudy \to Sprinkler$ is severed
    - Sprinkler is now fixed regardless of cloudiness
    - Only descendants of Sprinkler ($WetGrass$) change; $Cloudy$ and $Rain$ are
      unaffected
  - Formally, the mutilated joint distribution is:
    $$
    P_{X_j = x_j^k}(x_1, \ldots, x_n) =
    \begin{cases}
    \prod_{i \ne j} \Pr(x_i \mid \text{Parents}(X_i)) & \text{if } X_j = x_j^k \\
    0 & \text{otherwise}
    \end{cases}
    $$

- **Computing interventional distributions**
  - The _adjustment formula_ for estimating the causal effect of $X_j$ on $X_i$:
    $$
    \Pr(X_i = x_i \mid do(X_j = x_j^k)) =
    \sum_{\text{Parents}(X_j)} \Pr(x_i \mid x_j^k, \text{Parents}(X_j))
    \Pr(\text{Parents}(X_j))
    $$
  - This formula marginalizes over the distribution of the parents of $X_j$,
    effectively averaging over all contexts

- **Why the distinction matters in business**
  - "Hotels with high prices have high occupancy" — an observation
  - "If we raise prices, occupancy will increase" — an intervention (likely
    wrong)
  - The $do$-operator prevents us from confusing statistical regularities with
    levers we can pull

- **Randomized Controlled Trials (RCTs) as physical $do$-operators**
  - An RCT physically implements $do(X = x)$ by randomly assigning units to
    treatment, breaking all incoming edges to $X$ in the natural world
  - This is why RCTs are the gold standard: they make
    $\Pr(Y \mid X) = \Pr(Y \mid do(X))$ by design
  - Limitations of RCTs:
    - May be unethical (e.g., assigning a known harmful treatment)
    - Expensive or impractical at scale
    - Non-compliance and attrition can undermine randomization
    - Results may not generalize (external validity)
  - The $do$-calculus provides an alternative path: recovering
    $\Pr(Y \mid do(X))$ from observational data under certain conditions

### References
- Judea Pearl, _Causality_ (Cambridge University Press, 2009), Chapter 3
- Judea Pearl and Dana Mackenzie, _The Book of Why_ (Basic Books, 2018),
  Chapters 4–5
- Miguel Hernan and James Robins, _Causal Inference: What If_ (CRC Press, 2020),
  Chapter 2

## The Do-Calculus: Rules for Interventional Reasoning
The $do$-calculus is a complete formal system developed by Judea Pearl for
transforming expressions involving the $do$-operator into expressions computable
from observational data. It consists of three rules that, applied in sequence,
can eliminate $do()$ from any identifiable causal query.

- **The core problem**
  - We want: $\Pr(Y \mid do(X = x))$ — a causal quantity
  - We have: $\Pr(Y \mid X = x)$ — an observational quantity
  - In general, these differ due to confounding
  - The $do$-calculus provides algebraic rules to bridge the gap, given a causal
    graph

- **The three rules of do-calculus**

  Let $G$ be the causal DAG, $G_{\overline{X}}$ the graph with incoming edges to
  $X$ removed, and $G_{\underline{Z}}$ the graph with outgoing edges from $Z$
  removed.
  - **Rule 1 — Insertion/Deletion of Observations**
    - If $Y \perp\!\!\!\perp Z \mid X, W$ in $G_{\overline{X}}$, then:
      $$
      \Pr(Y \mid do(X), Z, W) = \Pr(Y \mid do(X), W)
      $$
    - Intuition: if $Z$ is irrelevant to $Y$ given $X$ and $W$ (after removing
      arrows into $X$), we can ignore $Z$
  - **Rule 2 — Action/Observation Exchange**
    - If $Y \perp\!\!\!\perp Z \mid X, W$ in $G_{\overline{X}, \underline{Z}}$,
      then:
      $$
      \Pr(Y \mid do(X), do(Z), W) = \Pr(Y \mid do(X), Z, W)
      $$
    - Intuition: if $Z$ has no back-door path to $Y$ (after removing incoming
      arrows to $X$ and outgoing from $Z$), intervention on $Z$ equals
      observation of $Z$
  - **Rule 3 — Insertion/Deletion of Actions**
    - If $Y \perp\!\!\!\perp Z \mid X, W$ in
      $G_{\overline{X}, \overline{Z(W)}}$, then:
      $$
      \Pr(Y \mid do(X), do(Z), W) = \Pr(Y \mid do(X), W)
      $$
    - Intuition: if $Z$ has no causal effect on $Y$ in a modified graph, the
      intervention $do(Z)$ can be dropped

- **Back-door adjustment as a special case**
  - A set $Z$ satisfies the _back-door criterion_ relative to $X \to Y$ if:
    - No variable in $Z$ is a descendant of $X$
    - $Z$ blocks every path from $X$ to $Y$ that has an arrow entering $X$
  - When satisfied:
    $$
    \Pr(Y \mid do(X)) = \sum_z \Pr(Y \mid X, Z = z)\Pr(Z = z)
    $$
  - This formula allows computing causal effects from observational data by
    adjusting for the confounders in $Z$

- **Chains, forks, and colliders — the three path motifs**
  - **Chain** $X \to M \to Y$
    - $M$ is a _mediator_; it transmits the causal effect of $X$ to $Y$
    - Conditioning on $M$ blocks the causal path — do _not_ control for
      mediators when estimating the total effect of $X$ on $Y$
  - **Fork** $X \leftarrow Z \to Y$ (confounder)
    - $Z$ is a _common cause_ that creates a spurious association between $X$
      and $Y$
    - Conditioning on $Z$ removes confounding and isolates the causal effect —
      _do_ control for confounders
  - **Collider** $X \to M \leftarrow Y$
    - $M$ is a _collider_; $X$ and $Y$ are independent in the marginal
      distribution
    - Conditioning on $M$ _opens_ a spurious path between $X$ and $Y$ — do _not_
      control for colliders
    - This is one of the most common mistakes in applied statistics

- **Common mistakes in practice**
  - Conditioning on a descendant of $X$ (biases the estimate)
  - Conditioning on a collider (introduces spurious association)
  - Controlling for every available covariate ("throw in the kitchen sink") —
    likely opens collider paths
  - Forgetting to block all back-door paths (leaves confounding in)
  - Using variables on the causal path as controls (blocks the mediator)

- **Front-door adjustment: when back-door fails**
  - When an unobserved confounder $U$ exists (no set of observables blocks all
    back-door paths), the front-door criterion may apply
  - Requires a mediator $M$ such that:
    1. All paths from $X$ to $Y$ go through $M$
    2. No unobserved confounder affects $X$ and $M$
    3. All back-door paths from $M$ to $Y$ are blocked by $X$
  - Front-door formula:
    $$
    \Pr(Y \mid do(X)) = \sum_m \Pr(M = m \mid X)
    \sum_{x'} \Pr(Y \mid M = m, X = x') \Pr(X = x')
    $$
  - Example: ads ($X$) → kids' nagging ($M$, the mediator) → cereal purchase
    ($Y$), with hidden confounder "parents who care about breakfast" ($U$)

- **Completeness of do-calculus**
  - Pearl's do-calculus is _complete_: if a causal effect is identifiable from a
    given graph and observational data, do-calculus can derive the formula
  - If do-calculus cannot reduce a $do$-expression to observational quantities,
    the effect is not identifiable without additional assumptions or experiments

### References
- Judea Pearl, "Causal Diagrams for Empirical Research," _Biometrika_ (1995)
- Judea Pearl, _Causality_ (Cambridge University Press, 2009), Chapters 3–4
- Ilya Shpitser and Judea Pearl, "Identification of Joint Interventional
  Distributions in Recursive Semi-Markovian Causal Models," _AAAI_ (2006)
- Brady Neal, "Introduction to Causal Inference," lecture notes (2020) — Chapter
  4 (free online)

## d-Separation and Conditional Independence
d-Separation is the graphical criterion that tells us which variables are
conditionally independent given a set of conditioning variables. It is the
bridge between the causal graph (a qualitative structure) and the probability
distribution (a quantitative object).

- **Motivation**
  - Given a causal DAG, we want to know: does conditioning on a set $Z$ make $X$
    and $Y$ independent?
  - D-Separation answers this question by inspecting paths in the graph

- **Paths and blocking**
  - A _path_ between $X$ and $Y$ is any sequence of edges (ignoring direction)
    connecting them in the graph
  - A path is _blocked_ (d-separated) by a set $Z$ if it contains:
    - A **chain** $A \to B \to C$ where $B \in Z$ (conditioning blocks the
      information flow)
    - A **fork** $A \leftarrow B \to C$ where $B \in Z$ (conditioning removes
      common cause)
    - A **collider** $A \to B \leftarrow C$ where $B \notin Z$ and no descendant
      of $B$ is in $Z$ (colliders are _naturally_ blocked, but conditioning
      _opens_ them)

- **d-Separation defined**
  - $X$ and $Y$ are _d-separated_ by $Z$ (written $X \perp\!\!\!\perp Y \mid Z$
    in $G$) if every path between $X$ and $Y$ is blocked by $Z$
  - When d-separated, $X$ and $Y$ are conditionally independent given $Z$ in
    every distribution compatible with the graph:
    $$
    X \perp\!\!\!\perp_G Y \mid Z \implies X \perp\!\!\!\perp_P Y \mid Z
    $$

- **Why colliders require special care**
  - In an unmanipulated system, a collider $A \to B \leftarrow C$ naturally
    blocks the path — $A$ and $C$ are independent given no conditioning
  - Conditioning on $B$ (or any descendant of $B$) _opens_ the path, creating a
    spurious association between $A$ and $C$
  - This phenomenon is known as _Berkson's paradox_ or _collider bias_
  - Example: conditioning on "hospital admission" opens a spurious negative
    correlation between disease severity and a second independent cause of
    admission, making the two causes appear to be negatively associated

- **d-Separation and the Markov condition**
  - A distribution $P$ is _Markov compatible_ with a DAG $G$ if every
    d-separation in $G$ implies conditional independence in $P$
  - The Markov factorization:
    $$
    \Pr(X_1, \ldots, X_n) = \prod_{i=1}^n \Pr(X_i \mid \text{Parents}(X_i))
    $$
  - This factorization is the basis for efficient inference in Bayesian networks

- **Using d-Separation in practice**
  - To test whether controlling for $Z$ is sufficient to identify the causal
    effect of $X$ on $Y$: check whether $Z$ d-separates all non-causal paths
    from $X$ to $Y$ without d-separating the causal path
  - To detect collider bias: verify that you are not conditioning on common
    effects of $X$ and $Y$ or their descendants

### References
- Judea Pearl, _Causality_ (Cambridge University Press, 2009), Chapter 1.2
- Geiger, D., Verma, T., and Pearl, J., "d-Separation: From Theorems to
  Algorithms," _Uncertainty in Artificial Intelligence_ (1990)
- Cinelli, C., Forney, A., and Pearl, J., "A Crash Course in Good and Bad
  Controls," _Sociological Methods and Research_ (2022)

## Potential Outcomes Framework (Rubin Causal Model) and Its Equivalence to SCMs
The potential outcomes framework, also known as the Rubin Causal Model (RCM), is
the dominant paradigm for causal inference in statistics, economics, and
epidemiology. While superficially different from Pearl's graphical approach, the
two frameworks are mathematically equivalent for many classes of problems.

- **Core concepts of the potential outcomes framework**
  - For each unit $i$ and binary treatment $X \in \{0, 1\}$:
    - $Y_i(1)$: the outcome unit $i$ _would have_ if treated
    - $Y_i(0)$: the outcome unit $i$ _would have_ if not treated
    - These are called _potential outcomes_ or _counterfactual outcomes_
  - The _individual treatment effect_: $\tau_i = Y_i(1) - Y_i(0)$
  - The _fundamental problem of causal inference_: we can only observe one of
    $Y_i(1)$ or $Y_i(0)$ for any given unit — the other is counterfactual

- **Key estimands**
  - **Average Treatment Effect (ATE)**:
    $$
    \text{ATE} = \mathbb{E}[Y(1) - Y(0)]
    $$
  - **Average Treatment Effect on the Treated (ATT)**:
    $$
    \text{ATT} = \mathbb{E}[Y(1) - Y(0) \mid X = 1]
    $$
  - **Average Treatment Effect on the Controls (ATC)**:
    $$
    \text{ATC} = \mathbb{E}[Y(1) - Y(0) \mid X = 0]
    $$

- **Identification assumptions in the RCM**
  - **SUTVA** (Stable Unit Treatment Value Assumption):
    - No interference between units (one unit's treatment does not affect
      another's outcome)
    - No hidden treatment versions
  - **Ignorability** (unconfoundedness, no unmeasured confounders):
    $$
    (Y(0), Y(1)) \perp\!\!\!\perp X \mid Z
    $$
    - After conditioning on $Z$, treatment assignment is as good as random
  - **Overlap** (positivity):
    $$
    0 < \Pr(X = 1 \mid Z = z) < 1 \text{ for all } z
    $$
    - Every unit has a non-zero probability of receiving either treatment

- **Equivalence to the SCM / graphical framework**
  - In Pearl's framework: $\Pr(Y \mid do(X = x))$ — the interventional
    distribution
  - In the RCM: $\mathbb{E}[Y(x)]$ — the expected potential outcome under
    treatment $x$
  - These are mathematically equivalent:
    $$
    \mathbb{E}[Y(x)] = \mathbb{E}[Y \mid do(X = x)]
    $$
  - Ignorability in the RCM corresponds to the back-door criterion in DAGs
  - SCMs additionally support counterfactual reasoning at the individual level
    (which the RCM does as well via the notation $Y_i(x)$)

- **Practical differences between the frameworks**

  | Aspect    | Potential Outcomes (RCM)                             | Graphical (SCM / DAG)                                           |
  | :-------- | :--------------------------------------------------- | :-------------------------------------------------------------- |
  | Strengths | Tight statistical theory, rich estimation literature | Transparent assumptions, supports non-parametric identification |
  | Weakness  | Assumptions often implicit                           | Requires specifying full causal graph                           |
  | Common in | Statistics, economics, epidemiology                  | CS, AI, causal ML                                               |
  | Key tool  | Propensity scores, matching                          | do-calculus, d-separation                                       |

- **When to use which**
  - Use the RCM when the primary goal is estimation and you have a well-defined
    treatment and outcome (common in A/B testing, policy evaluation)
  - Use the graphical SCM when you need to reason about multiple interventions,
    mediation, selection bias, or when assumptions need to be made explicit

### References
- Donald Rubin, "Estimating Causal Effects of Treatments in Randomized and
  Nonrandomized Studies," _Journal of Educational Psychology_ (1974)
- Paul Rosenbaum and Donald Rubin, "The Central Role of the Propensity Score in
  Observational Studies," _Biometrika_ (1983)
- Judea Pearl, "Potential Outcomes, Counterfactuals and Graphical Models,"
  _Statistical Science_ (2009)
- Guido Imbens and Donald Rubin, _Causal Inference for Statistics, Social, and
  Biomedical Sciences_ (Cambridge University Press, 2015)
- Guido Imbens, "Potential Outcome and Directed Acyclic Graph Approaches to
  Causality: Relevance for Empirical Practice in Economics," _Journal of
  Economic Literature_ (2020)

## Tutorial: Pgmpy (Building and Querying Bayesian Networks and DAGs)
