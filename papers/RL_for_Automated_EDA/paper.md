---
title: "Reinforcement Learning with Verifiable Rewards for Automated Exploratory Data Analysis"
author:
  - name: Dev Delvitron1019 + Giacinto Paolo (GP) Saggese
    department: "Department of Computer Science"
    organization: "University of Maryland, College Park"
    location: "College Park, MD, USA"
    email: "`gsaggese@umd.edu`{=typst}"
abstract: |
  Exploratory data analysis (EDA) is the process by which a data scientist forms
  and tests hypotheses about the process that generated an unfamiliar dataset.
  Existing automation for this process, so-called AutoEDA tools, relies on
  hand-crafted heuristics for what to try next and cannot be trained end to end,
  while causal structure-learning algorithms recover a graph but are not
  formulated as a sequential decision problem and cannot incorporate an
  open-ended toolbox. Reinforcement learning with verifiable rewards (RLVR) has
  proven effective for training sequential-decision policies in math and code,
  domains where a proposed answer can be checked exactly, but EDA on real data
  has no such ground truth against which to check a proposed data-generating
  process.

  This paper proposes closing that gap by training the EDA loop entirely on
  synthetic environments: a random graphical model $G^*$ is sampled from an
  existing generator, a dataset is drawn from it and split into training and
  test partitions, and an agent equipped with a toolbox of statistical
  operations chooses a sequence of tool calls over the training data and emits
  a discovered graph $\hat{G}$. Because $G^*$ is known at training time, the
  agent can be scored exactly by combining structural agreement between
  $\hat{G}$ and $G^*$ with the discovered graph's out-of-sample predictive
  performance, yielding a verifiable reward suitable for policy-gradient
  training.

  We formalize this training environment, specify a candidate reward and
  toolbox, and work through two illustrative examples, one in which the
  policy must recover a linear-Gaussian structure and one in which it must
  avoid a spurious edge induced by an unmeasured confounder.

  // TODO(*): Add info about the results

keywords:
  - reinforcement learning
  - exploratory data analysis
  - causal discovery
  - verifiable rewards
  - policy gradients
  - synthetic data
bibliography: references.bib
---

# Introduction

Exploratory data analysis is typically the first step a data scientist takes
when confronted with an unfamiliar dataset: forming hypotheses about which
variables relate to which, testing those hypotheses with statistical tools,
and revising them until a model of the data-generating process emerges. This
process is difficult to automate for two related reasons:

- **Open-ended.** There is no fixed sequence of steps that is correct for
  every dataset, so an automated agent must decide adaptively, given what it
  has learned so far, which tool to try next.
- **No ground truth.** On a real dataset, the true data-generating process is
  unknown, so there is no ground truth against which an automated agent's
  output can be checked, either at deployment time or, more importantly for
  training, during learning.

Prior work on automating this process falls into three categories:

- **AutoEDA and AutoML tooling** applies fixed heuristics or search
  procedures, such as ranking candidate visualizations by an
  information-theoretic utility score or enumerating summary statistics and
  plots in a pre-defined order, to surface patterns a human analyst can then
  interpret
  [@vartak2015seedb; @wongsuphasawat2017voyager; @milo2020autoeda; @he2021automl].
  These systems do not learn an adaptive policy: their decision rule is
  engineered once and does not improve from experience across datasets.
- **Causal and probabilistic structure learning** recovers a graph over
  variables from data using constraint-based tests [@spirtes2000causation],
  greedy score-based search [@chickering2002ges], or continuous optimization
  over a differentiable acyclicity constraint [@zheng2018notears]. These
  algorithms produce a structural output that can be compared against ground
  truth, but they are not formulated as sequential decision problems over an
  extensible toolbox and are not trained to improve at choosing among
  competing statistical tests.
- **Reinforcement learning with verifiable rewards (RLVR)** is a recent
  training paradigm in which a policy is optimized against an automatically
  checkable reward rather than a learned or human-provided one
  [@lambert2024tulu3]. RLVR has proven effective for training large language
  models to reason through multi-step math and code problems, where a
  proposed final answer or a generated program can be checked exactly against
  a known solution or test suite [@deepseekai2025r1]. This recipe
  presupposes a ground-truth checker, which is precisely what is missing for
  EDA on real data: a dataset collected in the wild carries no verified
  data-generating process to check a discovered graph against.

This paper proposes closing that gap between the second and third categories
by supplying the missing ground truth synthetically. Rather than training on
real datasets, the agent trains on datasets generated from randomly sampled
graphical models, whose generating graph $G^*$ is known exactly because it was
sampled by the training procedure itself. This converts causal structure
discovery from an unverifiable problem into a verifiable one, allowing the
sequential, adaptive, tool-using policy that RLVR training produces in math
and code to be trained for the EDA loop as well.

The framework rests on the following simplifying assumptions.

- **Synthetic ground truth suffices for reward computation.** The random
  graphs and datasets generated during training are assumed to be
  representative enough of real data-generating processes that a policy
  optimized against them acquires skills that transfer, a question we return
  to in Section VI.
- **A fixed, enumerable toolbox.** The agent chooses among a finite set of
  statistical operations (e.g., regression, correlation and independence
  tests) rather than writing arbitrary code, which keeps the action space
  tractable for policy-gradient training.
- **A single discovered graph as the terminal output.** The agent's episode
  ends when it emits one candidate graph $\hat{G}$, rather than an open-ended
  analysis report, so that a single scalar reward can be computed at episode
  end.

This paper makes the following contributions.

- We formalize a synthetic training environment for the EDA loop in which the
  reward is verifiable by construction (Section III).
- We specify a reward that combines structural agreement with $G^*$ and
  out-of-sample predictive performance, and a candidate toolbox and training
  procedure based on policy-gradient methods (Section IV).
- We work through two illustrative examples, a linear-Gaussian recovery task
  and a confounded-feature task, and describe a shortcut-policy failure mode
  worth evaluating explicitly (Section V).
- We discuss the open reward-design and sim-to-real transfer questions this
  framework raises, and state plainly that it has not yet been implemented or
  evaluated (Section VI).

The remainder of the paper is organized as follows. Section II surveys related
work in more detail. Section III formalizes the training environment and the
two sub-problems it must solve. Section IV describes the reward, toolbox, and
policy-training procedure. Section V works through the illustrative examples.
Section VI discusses limitations and the sim-to-real question. Section VII
concludes and outlines an implementation plan.

# Related Work

**AutoEDA and visualization recommendation.** _SeeDB_ scores candidate
visualizations by how much they deviate from a reference distribution, and
_Voyager 2_ blends specification-driven and recommendation-driven visual
analysis to surface relationships a human analyst reviews interactively
[@vartak2015seedb; @wongsuphasawat2017voyager]. Milo and Somech survey a wider
family of AutoEDA systems that apply machine learning to individual sub-tasks
such as visualization ranking and outlier flagging [@milo2020autoeda]. Across
this line of work, the analysis policy, what to compute or plot next given
what has been seen so far, is fixed by design rather than learned, so these
systems cannot improve their strategy from experience and do not target a
single unifying model of the data-generating process the way structure
learning does.

**Causal and probabilistic structure learning.** Constraint-based algorithms
such as PC recover a graph by testing conditional independence relations
[@spirtes2000causation]; score-based algorithms such as Greedy Equivalence
Search optimize a model-fit score over the space of graphs
[@chickering2002ges]; and continuous-optimization methods such as NOTEARS
recast acyclic structure learning as a smooth constrained optimization problem
solvable with gradient-based methods [@zheng2018notears]. Structural Hamming
distance between a discovered and a ground-truth graph is the standard metric
for evaluating these algorithms on synthetic benchmarks
[@tsamardinos2006shd]. These algorithms are the natural source of both tools
and evaluation metrics for the toolbox and reward proposed here, but each
algorithm is itself a fixed procedure: none of them is formulated as a policy
that chooses, case by case, which test or estimator to apply next, nor trained
end to end to make that choice better over time.

**Reinforcement learning with verifiable rewards.** Policy-gradient methods
optimize a parametrized policy directly against expected reward
[@williams1992reinforce; @sutton1999policygradient], with Proximal Policy
Optimization (PPO) as a widely used stabilized variant
[@schulman2017ppo]. RLVR applies this machinery with a reward computed by an
automatic checker rather than a learned reward model, and has been used to
train large language models on math and code tasks with checkable final
answers [@lambert2024tulu3; @deepseekai2025r1]. This line of work supplies the
training algorithm this paper proposes to reuse, but it has, to our knowledge,
only been applied to domains, math and code, where the checkable ground truth
is a static, pre-existing part of the task. This paper instead constructs the
ground truth synthetically, as part of the environment, so the same training
recipe can be applied to the EDA loop, where no pre-existing ground-truth
checker exists on real data.

# Problem Formulation

## Notation and Setup

Let $G^*$ denote a directed graph over a set of $n$ variables, sampled from a
random graph generator, together with the parametrization (e.g., linear
coefficients and noise variances) needed to turn $G^*$ into a data-generating
process. Let $D \sim G^*$ denote a dataset of $N$ i.i.d. rows drawn from that
process, split into a training partition $D_{train}$ and a held-out partition
$D_{test}$. Let $T = \{t_1, \dots, t_k\}$ denote a fixed toolbox of statistical
operations available to the agent (Table I), each of which, given a subset of
variables and $D_{train}$, returns a numeric or categorical result. Let
$\pi_\theta$ denote the agent's policy, parametrized by $\theta$, which
selects a sequence of tool calls $(t_{i_1}, a_1), (t_{i_2}, a_2), \dots$ over
$D_{train}$, where $a_j$ denotes the arguments (e.g., variable subset) to the
$j$-th call, and terminates by emitting a discovered graph $\hat{G}$ over the
same $n$ variables.

## Simplifying Assumptions

- **Known variable set.** The number and identity of the $n$ variables is
  assumed known to the agent; only the edges among them are unknown.
- **No intervention.** The agent may only observe $D_{train}$ through the
  toolbox $T$ and cannot perform interventions, so the environment models
  observational rather than experimental EDA.
- **Episodic termination.** The agent's tool-call sequence is assumed to
  terminate in a bounded number of steps, either by an explicit "emit graph"
  action or a step budget, so that training episodes are finite.

## Problem 1: Environment Construction

Given a random graph generator $\mathcal{G}$ (e.g., a `pgmpy` random Bayesian
network sampler or `sklearn`'s `make_regression`/`make_classification` with
latent structure) and a sample size $N$, construct a distribution over
training episodes $(G^*, D_{train}, D_{test})$ such that $G^*$ is retained by
the environment (never exposed to the policy) and $D_{train}$, $D_{test}$ are
the only quantities the policy observes.

## Problem 2: Verifiable Reward Design

Given the ground-truth $G^*$, the discovered graph $\hat{G}$, and $D_{test}$,
define a scalar reward
$$
r = \text{score}(\hat{G}, G^*, D_{test})
$$
that (a) is computable without human judgment, so that it can be used for
policy-gradient training at scale, and (b) rewards both structural correctness
and predictive usefulness, so that a policy cannot obtain high reward by
matching $G^*$'s topology while ignoring whether the recovered relationships
actually hold predictive power on unseen data, or vice versa.

# RLVR Framework for EDA

## Toolbox Design

Table I lists a candidate toolbox $T$. Each tool takes a subset of variables
and $D_{train}$ as input and returns a result the policy observes as part of
its next state, so that later tool calls can be conditioned on earlier
results, mirroring how a human analyst chooses the next test based on what
the previous one showed.

: Candidate toolbox $T$ available to the policy $\pi_\theta$.

| Tool | Input | Output |
| :--- | :--- | :--- |
| $y$-$x$ regression | target var., predictor subset | coefficients, $R^2$ |
| Pairwise correlation | two variables | correlation coefficient |
| Conditional independence test | two vars., conditioning set | test statistic, $p$-value |
| Mutual information | two variables | MI estimate |
| Hypothesis test (e.g., $t$-test) | one or two variables | test statistic, $p$-value |
| Emit graph (terminal action) | — | discovered graph $\hat{G}$ |

## Reward Design

We propose combining a structural term with a predictive term:
$$
\begin{aligned}
\text{score}(\hat{G}, G^*, D_{test}) = &-\lambda \cdot \text{SHD}(\hat{G}, G^*) \\
  &+ (1-\lambda) \cdot \text{Pred}(\hat{G}, D_{test})
\end{aligned}
$$
where $\text{SHD}$ is the structural Hamming distance between the discovered
and ground-truth graphs, the standard metric for comparing graphs recovered
by structure-learning algorithms against a known reference
[@tsamardinos2006shd], and $\text{Pred}(\hat{G}, D_{test})$ measures how well
the conditional relationships implied by $\hat{G}$ predict held-out variables
in $D_{test}$, for example an out-of-sample $R^2$ or log-likelihood averaged
over the graph's implied conditional distributions. The weight
$\lambda \in [0, 1]$ trades off exact structural recovery against predictive
usefulness; Section V.3 illustrates why relying on either term alone is
insufficient.

## Policy Training

The policy $\pi_\theta$ is trained with policy-gradient methods. The basic
REINFORCE estimator [@williams1992reinforce] provides an unbiased but
high-variance gradient estimate of expected reward with respect to $\theta$;
Proximal Policy Optimization (PPO) [@schulman2017ppo] is a practical,
variance-reduced alternative already used for RLVR training of tool-using
policies in math and code [@lambert2024tulu3; @deepseekai2025r1], and is the
candidate algorithm for training $\pi_\theta$ here, following the treatment in
[@lambert2024rlhfbook]. Because each episode's reward is computed exactly from
the sampled $G^*$, no reward model or human feedback is required at any point
in training, which is the property that makes the reward verifiable in the
RLVR sense.

## Curriculum Learning

Because the environment samples $G^*$ synthetically, the difficulty of
training episodes can be controlled directly, by the number of variables $n$,
the edge density of $G^*$, and the noise level of the data-generating
process. We propose increasing these three parameters over the course of
training, so that the policy first masters small, low-noise graphs before
being exposed to the larger, denser, noisier graphs it must handle for the
sim-to-real evaluation discussed in Section VI.

# Illustrative Worked Example

This section works through two of the training scenarios the environment of
Section III is intended to produce, and a failure mode the reward of Section
IV.2 is intended to guard against. These examples are hand-traced
illustrations of the intended agent behavior, not the output of a trained
policy; no computational implementation has been built to generate them.

**Linear-Gaussian recovery.** Consider $G^*$ sampled as a three-node chain
$X_1 \to X_2 \to Y$ with linear-Gaussian conditional distributions, generated
by a `pgmpy` random Bayesian network sampler. A policy pursuing high reward
would call the $y$-$x$ regression tool with $Y$ as target and $X_2$ as
predictor, observe a large, statistically significant coefficient, then
regress $X_2$ on $X_1$ and observe the same, and finally check that $Y$
regressed on $X_1$ alone yields a weaker fit than $Y$ regressed on $X_2$
alone, consistent with $X_1$'s effect on $Y$ being mediated by $X_2$. Emitting
$\hat{G} = G^*$ from this sequence of results yields $\text{SHD} = 0$ and a
predictive term close to its maximum, since the discovered graph is the true
generating process.

**Confounded features.** Consider instead $G^*$ with an unmeasured confounder
$U \to X_1$, $U \to X_2$, and no direct edge between $X_1$ and $X_2$,
generated with `sklearn`'s `make_regression` with latent structure. A naive
policy that only checks pairwise correlation would observe a large
correlation between $X_1$ and $X_2$, induced entirely by their shared
dependence on $U$, and could emit a spurious $X_1$-$X_2$ edge. A policy that
instead uses the conditional independence test, conditioning on other
observed variables correlated with $U$, or that recognizes the pairwise
correlation is not corroborated by a corresponding regression coefficient
once other variables are controlled for, avoids adding the false edge.
Figure 1 contrasts the two outcomes: panel (a) shows the correct discovered
graph, which omits the spurious edge, and panel (b) shows the naive policy's
erroneous graph, which adds it. Because $\text{SHD}$ penalizes the extra edge
in panel (b) directly, this failure is visible to the reward even though $U$
itself is never observed by the policy.

![Ground-truth structure with a latent confounder $U$ (dashed), compared
against a policy's correctly discovered graph (a), which omits a direct edge
between $X_1$ and $X_2$, and a naive policy's erroneous graph (b), which adds
a spurious edge because it relies on pairwise correlation
alone.](figures/confounder_example.png)

**Overfitting to tool-call patterns.** A distinct failure mode, not tied to
either example above, is a policy that learns a fixed sequence of tool calls,
for instance always running pairwise correlation on every variable pair
followed by a fixed-order regression, regardless of what the data show. Such
a policy can score well on training graphs whose topology matches the
patterns it has memorized, while failing to generalize to test graphs with a
different topology, such as graphs with a different number of confounders or
a different chain length. We regard this as analogous to reward hacking in
other RLVR domains, where a policy exploits regularities in the reward rather
than solving the underlying task, and consider it a failure mode that must be
evaluated explicitly, by holding out graph topologies from training, rather
than assumed away.

Figure 2 summarizes the overall training loop these examples instantiate: a
graph generator produces $G^*$ and a train/test split, the policy interacts
with $D_{train}$ through the toolbox until it emits $\hat{G}$, and the
verifiable reward compares $\hat{G}$ against the retained $G^*$ and against
$D_{test}$ to produce the policy-gradient signal.

![The proposed RLVR training loop: a random graph generator produces the
ground-truth graph $G^*$ and a train/test split; the policy queries the
toolbox over $D_{train}$ and emits a discovered graph $\hat{G}$; the
verifiable reward compares $\hat{G}$ against the retained $G^*$ and against
$D_{test}$ to produce a policy-gradient
update.](figures/training_loop_schematic.png)

# Discussion and Limitations

**No implementation or empirical evaluation.** This paper proposes a
framework and works through hand-traced illustrative examples; no synthetic
environment, toolbox, or policy has been implemented, and no reward or
training curve reported here is measured. All quantitative claims in Section
V are illustrative of intended behavior, not observed results.

**Reward design under synthetic-only ground truth.** The reward of Section
IV.2 is only computable when $G^*$ is known, which holds during training but
never at deployment on a real dataset. It remains an open question, listed as
Question 1 in the originating research note, whether a policy trained
against this reward internalizes a decision procedure that a human can trust
in the absence of the same verifiable signal at deployment time, or whether
additional deployment-time proxies (e.g., held-out predictive performance
without a known $G^*$) are required.

**Sim-to-real transfer is unvalidated.** The framework assumes that skills
learned on randomly generated graphs transfer to real datasets with mixed
variable types, missing data, and non-stationary distributions, none of which
is modeled by the graph generators proposed in Section III. This is the
central risk of the approach: if synthetic graphs are not representative of
real data-generating processes along these dimensions, the trained policy may
overfit to properties of the generator (e.g., pgmpy's default parametrization
of conditional distributions) rather than acquiring a generally useful EDA
strategy. A curriculum over graph size, density, and noise (Section IV.4) is
proposed as a partial mitigation but has not been evaluated.

**Toolbox coverage bounds the discoverable structure.** The agent can only
discover relationships expressible through the fixed toolbox $T$ of Table I;
nonlinear, non-Gaussian, or higher-order relationships not captured by the
listed tools cannot be recovered regardless of policy quality, so the
reported reward would need to be interpreted relative to this toolbox rather
than as a general measure of EDA competence.

# Conclusion and Future Work

This paper proposed training an automated exploratory-data-analysis agent
with reinforcement learning by supplying the verifiable ground truth that
this reward paradigm requires synthetically, through randomly generated
graphical models whose generating graph is known exactly at training time.
We formalized the resulting training environment, a candidate toolbox and
reward that combines structural agreement with out-of-sample predictive
performance, and a policy-gradient training procedure, and worked through two
illustrative examples together with a shortcut-policy failure mode that a
sound evaluation protocol must guard against. No computational implementation
or empirical evaluation has been carried out; the contribution of this paper
is the framework and the questions it makes precise, not a validated result.

Future work follows the implementation plan below.

1. Build the synthetic environment: wire up a random graph generator
   (`pgmpy` or `sklearn`) to produce $(G^*, D_{train}, D_{test})$ episodes
   [@ankan2015pgmpy; @pedregosa2011sklearn].
2. Implement the toolbox of Table I and a scripted baseline agent, together
   with the scoring pipeline of Section IV.2, to obtain a working, if
   unlearned, point of comparison.
3. Train $\pi_\theta$ with policy-gradient methods over the verifiable reward
   and compare it against the scripted baseline on held-out synthetic graphs.
4. Introduce the curriculum of Section IV.4 and evaluate sim-to-real transfer
   on real datasets whose ground-truth graph is unknown, reporting the
   observed gap and failure modes rather than assuming transfer succeeds.
