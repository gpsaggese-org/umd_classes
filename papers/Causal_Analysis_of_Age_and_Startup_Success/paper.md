---
title: "A Causal Analysis of Founder Age and Startup Success"
author:
  - name: Giacinto Paolo (GP) Saggese
    department: "Department of Computer Science"
    organization: "University of Maryland, College Park"
    location: "College Park, MD, USA"
    email: "`gsaggese@umd.edu`{=typst}"
abstract: |
  Popular narratives celebrate the young startup founder, yet large-scale
  administrative and meta-analytic studies find that successful founders are
  typically middle-aged and that prior industry experience, which accumulates
  with age, is itself a strong predictor of success. This creates a specific
  identification problem that existing empirical work does not fully resolve:
  age is entangled with a set of pre-founding confounders (industry, team
  size, market timing) that must be adjusted for, and with at least one
  post-founding mediator, prior industry experience, that must not be, if the
  goal is to estimate the total causal effect of age rather than a
  mediation-adjusted residual.
  <!-- -->
  This paper proposes a causal-inference framework for the founder-age
  question that makes this distinction explicit. We construct a causal
  directed acyclic graph (DAG) separating confounders from the mediator,
  formalize the total effect and the controlled direct effect as distinct
  estimands under the backdoor criterion, and develop a propensity-score
  matching (PSM) estimation procedure for the total effect, cross-checked
  against inverse-probability weighting and stratification, together with a
  Rosenbaum-bounds sensitivity-analysis protocol for the framework's central
  identification threat: unmeasured founder ability. We extend the framework
  to nonlinear, quadratic-in-age effects and to treatment-effect heterogeneity
  across industries via causal forests.
  <!-- -->
  We illustrate the estimation mechanism with a small, hand-computed synthetic
  example in which propensity-score matching shrinks a naive age-success gap
  of 26.7 percentage points to a matched estimate of 20 percentage points,
  consistent with the literature's conclusion that part, but not all, of the
  observed association reflects confounding. No real-data computational
  implementation or empirical evaluation has been carried out; this paper is a
  methodology and identification framework grounded in and synthesizing
  existing large-scale findings, not a new empirical result.
keywords:
  - causal inference
  - founder age
  - startup success
  - propensity score matching
  - confounding
  - mediation analysis
  - entrepreneurship
bibliography: references.bib
---

# Introduction

Media coverage of entrepreneurship disproportionately features founders in
their twenties, and venture-funding culture has at times treated youth as a
proxy for disruptive potential. Large-scale evidence points the other way.
An analysis of 2.7 million U.S. firm founders finds an average founder age of
41.9 years, an average age of 45 among the top 0.1% of fastest-growing firms,
and a 50-year-old founder roughly 1.8 times more likely than a 30-year-old
founder to build a top-growth firm [@azoulay2018age]. A meta-analysis of 102
independent samples finds a weak positive, and possibly U-shaped, relationship
between founder age and success, with the sign and magnitude depending on
which success metric is used [@zhao2021age].

Both findings raise the same unresolved question: is age itself a cause of
startup success, or does it merely index other resources, chiefly prior
industry experience, that accumulate over a founder's career? The distinction
matters for policy (should age-based signals in hiring or funding decisions
be discounted) and for measurement (whether to condition on experience when
estimating an age effect), and the two studies above answer it differently in
practice. Azoulay et al. treat prior industry experience as a control
variable and report that age remains predictive after adding it
[@azoulay2018age]. Zhao et al. treat the overall age-success correlation as
likely proxying for age-correlated resources without further decomposition
[@zhao2021age]. Neither paper poses the question in the language of a causal
graph, so it is not stated explicitly that adding "prior industry
experience" as a control changes which causal quantity is being estimated
rather than simply refining the same estimate.

This paper argues that founder age plays two distinct causal roles relative to
startup success, and that conflating them is a specific, nameable
identification error. A set of pre-founding characteristics, industry, team
size, market timing, geography, education, are common causes of both age at
founding and success; these are confounders and must be adjusted for to
identify the causal effect of age. Prior industry experience, by contrast, is
plausibly caused by age (older founders have had more career time in which to
accumulate it) and itself causes success; it is a mediator, not a confounder,
and adjusting for it answers a different question, the effect of age net of
its experience channel, rather than the total effect of age.

The framework rests on the following simplifying assumptions, developed
formally in Section III.

- **Binarized treatment.** Founder age is discretized into an "older" versus
  "younger" cohort at a threshold for propensity-score matching, trading
  continuous dose-response information for matching tractability; a
  continuous extension is developed separately in Section V.
- **Conditional ignorability.** Treatment assignment (the age cohort) is taken
  to be as-good-as-random once the observed confounders are held fixed; this
  assumption is not directly testable and is the target of the
  sensitivity analysis in Section IV.
- **A correctly specified causal graph.** The classification of each variable
  as a confounder, a mediator, or unobserved is assumed rather than
  data-derived, consistent with standard practice in applied causal
  inference but itself a source of possible error, discussed in Section VII.

The main contributions of this paper are:

- A causal DAG that separates pre-founding confounders from the mediator
  "prior industry experience" and an unmeasured confounder "founder ability,"
  and a formalization of the resulting total-effect and controlled-direct-
  effect estimands under Pearl's backdoor criterion [@pearl2009causality]
  (Section III).
- A propensity-score-matching estimation procedure for the total effect of
  founder age on startup success, cross-checked against inverse-probability
  weighting and stratification, together with a Rosenbaum-bounds
  sensitivity-analysis protocol targeting the framework's central
  identification threat, unmeasured founder ability (Section IV).
- An extension of the framework to a nonlinear, quadratic-in-age effect and to
  treatment-effect heterogeneity across industries via causal forests
  (Section V).
- A hand-computed illustrative example on a small synthetic founder dataset
  showing the mechanism by which naive comparisons overstate the age effect
  relative to the propensity-score-adjusted estimate (Section VI).

The paper is organized as follows. Section II reviews related empirical and
methodological work. Section III formalizes the causal model. Section IV
develops the estimation and sensitivity-analysis framework. Section V extends
the framework to nonlinear and heterogeneous effects. Section VI works a
small illustrative example by hand. Section VII discusses limitations, and
Section VIII concludes.

# Related Work

**Large-scale administrative evidence.** The most comprehensive study of
founder age and growth outcomes uses U.S. Census administrative data covering
2.7 million firm founders between 2007 and 2014, and finds that founder age
is positively associated with the probability of building a high-growth firm
and with the probability of a successful exit, an association that survives
the inclusion of prior industry experience as a regression control
[@azoulay2018age]. This is associational evidence conditioned on observables
through linear regression; it does not formalize a causal graph, so it does
not distinguish, at the level of the identification strategy, between
"controlling for a confounder" and "controlling for a mediator" when
industry experience is added to the model. Section III formalizes exactly
this distinction for the same substantive question.

**Meta-analytic synthesis.** A meta-analysis of 102 independent samples finds
an overall weak positive, and possibly U-shaped, relationship between founder
age and entrepreneurial success, with the direction and magnitude of the
effect varying by which success metric, firm growth, financial performance,
firm size, subjective success, or survival, is used [@zhao2021age]. Because
meta-analysis aggregates published correlational estimates obtained under
heterogeneous designs and covariate sets, it characterizes the empirical
landscape without itself supplying a single causal identification strategy.
This paper is complementary: it proposes one specific identification strategy
that could, in principle, be applied uniformly across the outcome measures
that the meta-analysis shows behave differently.

**Causal-graph and propensity-score methodology.** The propensity score, the
probability of treatment given observed covariates, was shown to be a
sufficient statistic for confounder adjustment under conditional
ignorability, enabling matching or stratification on a single scalar instead
of the full covariate vector [@rosenbaum1983propensity]. The backdoor
criterion formalizes which covariate sets validly identify a causal effect
from observational data, and explicitly excludes descendants of the
treatment, including mediators, from a valid adjustment set
[@pearl2009causality]; the companion methodology for isolating the portion of
an effect that operates through a specific mediator is developed in the
causal-mediation literature [@vanderweele2015explanation]. This methodology
is general and predates the founder-age question; this paper's contribution
is connecting it specifically to founder age and prior industry experience,
where the confounder/mediator distinction has direct empirical consequences
for how the existing literature's control variables should be interpreted.

# Problem Formulation

## Notation and Setup

We adopt the Neyman-Rubin potential-outcomes framework. For founder $i =
1, \dots, n$, let $\mathrm{Age}_i \in \mathbb{R}_{+}$ denote age at founding,
and let $T_i = \mathbb{1}[\mathrm{Age}_i \ge a^\star]$ denote a binarized
treatment indicator for an "older founder" cohort at threshold $a^\star$.
Let $Y_i(1)$ and $Y_i(0)$ denote the potential success outcomes under the
older and younger cohort respectively, with the observed outcome $Y_i = T_i
Y_i(1) + (1 - T_i) Y_i(0)$. Table I summarizes the notation.

: Notation used throughout Sections III-VI.

| Symbol | Meaning |
| :--- | :--- |
| $T_i \in \{0,1\}$ | Treatment: older ($\mathrm{Age}_i \ge a^\star$) vs. younger founder |
| $X_i \in \mathbb{R}^k$ | Confounders: industry, team size, founding year, geography, education, funding stage |
| $M_i$ | Mediator: prior industry experience at founding |
| $U_i$ | Unmeasured confounder: founder ability/motivation |
| $Y_i(t)$ | Potential success outcome under treatment $t \in \{0,1\}$ |
| $e(x) = P(T_i{=}1 \mid X_i{=}x)$ | Propensity score |
| $\tau_{\mathrm{ATT}}$ | Average treatment effect on the treated |

## Simplifying Assumptions

- **SUTVA.** A founder's potential outcomes do not depend on other founders'
  treatment status, and there is a single well-defined version of "older
  founder" for a given threshold $a^\star$; interaction effects between
  co-founders of different ages within the same team are not modeled.
- **Binarized treatment.** Discretizing $\mathrm{Age}_i$ at $a^\star$
  simplifies estimation to standard binary-treatment matching machinery at
  the cost of the continuous dose-response information used in Section V.
- **Conditional ignorability.** $(Y_i(0), Y_i(1)) \perp T_i \mid X_i$, i.e.,
  conditional on the observed confounders $X_i$, treatment assignment is as
  good as random. This assumption fails if $U_i$ (unmeasured founder ability)
  affects both the age at which a founder starts a company and the
  probability of success; Section IV-D develops a sensitivity analysis for
  exactly this failure mode.
- **Positivity.** $0 < e(x) < 1$ for every $x$ in the support of $X$, so that
  comparable treated and control founders exist at every covariate value used
  for matching.
- **Correct confounder/mediator classification.** $X_i$ is assumed to consist
  only of causes that precede treatment, and $M_i$ is assumed to be caused by
  $T_i$ rather than a further confounder of $T_i$ and $Y_i$; Section VII
  discusses the consequences of misclassifying this graph.

## Problem 1: Confounder-Mediator Identification

Figure 1 shows the causal DAG assumed throughout the paper.

![Causal DAG relating confounders $X$, treatment $T$ (founder age), mediator
$M$ (prior industry experience), outcome $Y$ (startup success), and the
unmeasured confounder $U$ (founder ability). The red edge $T \to Y$ is the
total causal effect of interest.](figures/causal_dag.png)

By the backdoor criterion, a covariate set $Z$ identifies the total causal
effect of $T$ on $Y$ if $Z$ blocks every path from $T$ to $Y$ that begins with
an arrow into $T$, and $Z$ contains no descendant of $T$
[@pearl2009causality]. Here $X$ satisfies both conditions: it blocks the
backdoor path $T \leftarrow X \to Y$, and it precedes $T$. The mediator $M$
does not: it is a descendant of $T$, so including it in the adjustment set
blocks part of the very causal pathway $T \to M \to Y$ that the total effect
is meant to capture. This gives two distinct, both well-defined, estimands:

$$
\tau_{\mathrm{total}} = \mathbb{E}[Y(1) - Y(0)] ,
$$

$$
\tau_{\mathrm{direct}}(m) = \mathbb{E}[Y(1, m) - Y(0, m)] ,
$$

where $\tau_{\mathrm{total}}$ is identified by adjusting for $X$ alone (the
target of Section IV), and $\tau_{\mathrm{direct}}(m)$, the controlled direct
effect holding prior industry experience fixed at level $m$, requires
adjusting for $X$ and $M$ jointly and additionally assumes no unmeasured
confounding of the $M$-$Y$ relationship [@vanderweele2015explanation]. When a
regression specification "controls for prior industry experience" without
this distinction, as is common in the applied literature (Section II), it
silently estimates $\tau_{\mathrm{direct}}$ rather than $\tau_{\mathrm{total}}$,
which is a different, and generally smaller in magnitude, quantity whenever
$M$ carries part of age's causal effect. This paper's estimation framework
(Section IV) targets $\tau_{\mathrm{total}}$, and Section V-A separately
estimates $\tau_{\mathrm{direct}}$ for comparison.

## Problem 2: Average Treatment Effect Estimation

Given observational data $\{(T_i, X_i, Y_i)\}_{i=1}^n$ drawn i.i.d. from the
population of interest, and under the assumptions of Section III-B, the
estimation problem is to compute a sample estimate $\hat\tau_{\mathrm{ATT}}$
of the average treatment effect on the treated,

$$
\tau_{\mathrm{ATT}} = \mathbb{E}[\, Y(1) - Y(0) \mid T = 1 \,],
$$

together with a diagnostic of how sensitive $\hat\tau_{\mathrm{ATT}}$ is to a
violation of conditional ignorability through the unmeasured confounder $U$.
Section IV develops both.

# Causal Estimation Framework

## Propensity Score Estimation

We estimate $e(x) = P(T=1 \mid X=x)$ by fitting a model, e.g., logistic
regression or gradient-boosted trees, of $T_i$ on $X_i$ using only the
confounder set identified in Section III-C, excluding both the mediator $M_i$
and the outcome $Y_i$. Rosenbaum and Rubin's central result justifies
reducing the matching problem to this scalar: if $(Y(0), Y(1)) \perp T \mid
X$, then also $(Y(0), Y(1)) \perp T \mid e(X)$, so balancing the scalar
propensity score is sufficient to balance the full covariate vector in
expectation [@rosenbaum1983propensity].

## Matching and the ATT Estimator

For each treated founder $i$, we find the nearest untreated founder in
propensity-score space,

$$
j(i) = \arg\min_{j : T_j = 0} \; \lvert \hat e(X_i) - \hat e(X_j) \rvert ,
$$

optionally discarding matches with $\lvert \hat e(X_i) - \hat e(X_j(i))
\rvert$ above a caliper $\delta$, and estimate

$$
\hat\tau_{\mathrm{ATT}} = \frac{1}{n_1} \sum_{i : T_i = 1}
\big[\, Y_i - Y_{j(i)} \,\big] ,
$$

where $n_1$ is the number of treated founders retained after caliper
trimming. Founders without a comparable match, i.e., outside the region of
common support, are excluded rather than compared, which is what prevents the
estimator from extrapolating the effect to covariate combinations that do not
occur in both groups.

## Alternative Estimators for Robustness

Because $\hat\tau_{\mathrm{ATT}}$ depends on the specific matching algorithm
and caliper, we cross-check it against two standard alternatives that use the
same estimated propensity score differently. Inverse-probability weighting
(IPW) reweights every observation rather than discarding unmatched units,

$$
\hat\tau_{\mathrm{IPW}} = \frac{1}{n} \sum_{i=1}^n
\left[ \frac{T_i Y_i}{\hat e(X_i)} - \frac{(1-T_i) Y_i}{1 - \hat e(X_i)}
\right] ,
$$

and stratification partitions founders into $K$ propensity-score bins and
aggregates within-bin treated-minus-control differences, weighted by bin
size, in the spirit of Mantel-Haenszel adjustment. Agreement across the three
estimators is evidence against the result being an artifact of one
particular adjustment mechanism [@imbens2004nonparametric]; disagreement
signals that overlap is poor enough for the estimators' different
extrapolation behavior to matter, which is itself diagnostic information
about the data.

## Sensitivity Analysis for Unmeasured Confounding

Conditional ignorability (Section III-B) cannot be tested directly because
$U_i$, founder ability, is unobserved. Rosenbaum's sensitivity-analysis
framework asks instead how large a violation would have to be to overturn the
conclusion [@rosenbaum2002observational]. For each matched pair, suppose the
unmeasured confounder can change the odds of treatment by at most a factor
$\Gamma \ge 1$ between the two matched founders. The framework gives bounds
on the matched-pair test statistic as a function of $\Gamma$, and the
smallest $\Gamma^\star$ at which the bound on the p-value crosses a
significance threshold (e.g., $0.05$) is reported as a summary sensitivity
statistic: the larger $\Gamma^\star$, the more implausibly large an
unmeasured confounder would have to be to explain away $\hat\tau_{\mathrm{ATT}}$
as bias rather than a genuine effect of age.

## Computational Considerations

Fitting $\hat e(x)$ by logistic regression is $O(nk)$ per iteration in the
number of founders $n$ and confounders $k$. Nearest-neighbor matching without
replacement is $O(n_1 n_0)$ in the worst case for $n_1$ treated and $n_0$
control founders, or $O(n \log n)$ with a sorted-array search over $\hat
e(X)$, which is the practical choice at the scale of large founder
databases such as Crunchbase and Y Combinator. The
Rosenbaum-bounds sensitivity analysis is computed per matched pair and adds
negligible cost relative to fitting $\hat e(x)$.

# Nonlinear and Heterogeneous Age Effects

## Quadratic Age Effect and the Controlled Direct Effect

The binarized treatment of Sections III-IV discards information about the
shape of the age-success relationship, in particular the possible U-shaped
pattern reported by Zhao et al. [@zhao2021age]. As a continuous-treatment
complement, we consider the regression-adjustment specification

$$
Y_i = \beta_0 + \beta_1 \mathrm{Age}_i + \beta_2 \mathrm{Age}_i^2 + \gamma^\top
X_i + \varepsilon_i ,
$$

whose peak (or trough) occurs at $\mathrm{Age}^\star = -\beta_1 / (2
\beta_2)$. Fitting this specification with $X_i$ only recovers an estimate
analogous to $\tau_{\mathrm{total}}$; adding $M_i$ (prior industry experience)
as a further regressor recovers an estimate analogous to
$\tau_{\mathrm{direct}}$ from Section III-C. Comparing the two fits operates
as the paper's central diagnostic: a $\beta_1$ that shrinks substantially
once $M_i$ is added indicates that age's total effect operates largely
through the experience channel, while a $\beta_1$ that is stable indicates an
independent, "life stage" component of the age effect not mediated by
measured prior experience.

## Heterogeneity via Causal Forests

The confounders in Table I plausibly interact with treatment: it is a
plausible, untested hypothesis that the age effect differs by industry, with
faster-moving sectors such as SaaS placing less weight on accumulated domain
expertise than slower, capital- or regulation-intensive sectors such as
biotech or hardware. Rather than pre-specifying such interaction terms by
hand, a causal forest estimates a conditional average treatment effect
function directly,

$$
\hat\tau(x) = \widehat{\mathbb{E}}[\, Y(1) - Y(0) \mid X = x \,] ,
$$

as an ensemble of trees trained to split on covariates that maximize
heterogeneity in the estimated treatment effect rather than in the outcome
directly [@wager2018causalforests]. Applied to $X_i$ restricted to industry
and founding-year indicators, $\hat\tau(x)$ would let the age effect vary
freely across industries, complementing the finding that the age-success
relationship's sign and magnitude already vary by which success metric is
used [@zhao2021age], by testing whether it also varies by sector.

# Illustrative Worked Example

To make the estimator of Section IV concrete, this section works a small,
hand-computed example on a synthetic dataset of ten founders. It is intended
purely to illustrate the matching mechanism, not as an empirical finding
about real founders; a full computational implementation over real Crunchbase
and Y Combinator data is future work (Section VIII).

## Setup

Table II lists five treated founders (age at or above the threshold
$a^\star$) and six control founders (below the threshold), each with an
illustrative propensity score $\hat e(X_i)$, computed from a single binary
confounder, prior industry experience, standing in for the fuller confounder
set $X$ of Table I, and an illustrative binary success outcome $Y_i$.

: Toy example: ten treated and control founders with illustrative propensity
scores and outcomes. Matches are nearest-neighbor pairs within a caliper of
0.10; $C_6$ falls outside common support and is discarded.

| Founder | Group | $\hat e(X)$ | Match | $Y$ |
| :--- | :--- | ---: | :--- | ---: |
| $T_1$ | Treated | 0.82 | $C_1$ | 1 |
| $T_2$ | Treated | 0.71 | $C_2$ | 1 |
| $T_3$ | Treated | 0.55 | $C_3$ | 0 |
| $T_4$ | Treated | 0.65 | $C_4$ | 1 |
| $T_5$ | Treated | 0.40 | $C_5$ | 0 |
| $C_1$ | Control | 0.79 | $T_1$ | 1 |
| $C_2$ | Control | 0.68 | $T_2$ | 0 |
| $C_3$ | Control | 0.52 | $T_3$ | 0 |
| $C_4$ | Control | 0.62 | $T_4$ | 1 |
| $C_5$ | Control | 0.35 | $T_5$ | 0 |
| $C_6$ | Control | 0.15 | none | 0 |

## Matching and the ATT

Nearest-neighbor matching pairs each treated founder with the control founder
of closest propensity score: $T_1$-$C_1$, $T_2$-$C_2$, $T_4$-$C_4$,
$T_3$-$C_3$, and $T_5$-$C_5$, each within the 0.10 caliper. $C_6$, at $\hat
e = 0.15$, is not the nearest match for any treated founder and is discarded
as outside common support, i.e., there is no comparably "old-looking" treated
founder to compare it against. The treated group's mean outcome is
$3/5 = 0.60$; the matched-control group's mean outcome is $2/5 = 0.40$,
giving

$$
\hat\tau_{\mathrm{ATT}} = 0.60 - 0.40 = 0.20 .
$$

By contrast, the naive, unadjusted comparison of all five treated founders
against all six control founders (including $C_6$) gives a control mean of
$2/6 = 0.333$ and a naive difference of $0.60 - 0.333 = 0.267$. Figure 2
plots both estimates. The gap between them, 26.7 versus 20 percentage points,
illustrates the mechanism by which failing to restrict the comparison to
propensity-matched founders inflates the apparent age effect: $C_6$ pulls the
naive control mean down not because it is a valid counterfactual for any
treated founder, but because it is systematically less experienced than every
treated founder in the sample.

![Toy-example naive versus propensity-score-matched (ATT) estimate of the
age effect on the ten-founder illustrative dataset of Table
II.](figures/toy_example_att.png)

## What the Toy Example Does and Does Not Show

This example is illustrative of the estimation mechanism only. With five
matched pairs, a Rosenbaum-bounds sensitivity analysis (Section IV-D) would
not have meaningful power, so we do not compute one here; a real analysis
would require sample sizes closer to those available in large founder
databases such as Crunchbase and Y Combinator. The specific shrinkage
from 26.7 to 20 percentage points is a property of the illustrative numbers
chosen for Table II, not an empirical estimate of the true founder-age
effect, and should not be read as a validated finding.

# Discussion and Limitations

**Unmeasured founder ability.** The framework's central identification threat
is the unmeasured confounder $U$ in Figure 1: founders with greater
underlying ability, risk tolerance, or access to informal capital may both
choose to found companies at systematically different ages and be more
likely to succeed regardless of age. Conditional ignorability given $X$ rules
this out by assumption; Section IV-D's sensitivity analysis quantifies, but
does not eliminate, this risk. Whether such confounding would inflate or
deflate the age effect is not determined by the framework itself and depends
on the (currently unknown) correlation structure between $U$, age at
founding, and success in real data.

**Confounder-mediator misspecification.** The framework's identification
result in Section III-C depends on the DAG in Figure 1 being correctly
specified. If prior industry experience in fact also has a direct
confounding path into age at founding, for example, because founders who
happen to accumulate relevant experience earlier also found earlier for
reasons connected to that same underlying trait, then $M$ is not a pure
mediator and the total-effect estimand of Section III-C would need to be
revised; distinguishing these cases from observational data alone is
difficult and is not attempted here.

**Selection and survivorship bias.** Crunchbase- and Y-Combinator-style
datasets systematically under-represent startups that never raised
disclosed funding or that failed quietly without a recorded outcome, which
biases both the founder-age distribution and the observed success rate in
ways that are not corrected by the propensity-score adjustment in Section IV,
since that adjustment only balances observed confounders within the sample
actually collected.

**Estimand sensitivity to the success metric.** The meta-analytic evidence
finds different signs of the age-success relationship depending on whether
success is measured by growth, financial performance, firm size, subjective
success, or survival [@zhao2021age]. The framework in Sections III-IV applies
unchanged to any binary or continuous $Y_i$, but $\hat\tau_{\mathrm{ATT}}$
estimated on one outcome measure should not be interpreted as generalizing to
another without re-estimation.

**Discretizing a continuous treatment.** Binarizing age at a threshold
$a^\star$ (Sections III-IV) discards the dose-response information that
motivates the quadratic specification of Section V-A, and the choice of
$a^\star$ itself is not derived from the data in this framework; a
data-driven threshold selection, or a fully continuous-treatment estimator,
is left to future work.

# Conclusion and Future Work

This paper proposed a causal-inference framework for the founder-age
question that makes explicit a distinction the existing literature applies
inconsistently: prior industry experience is a mediator of age's effect on
startup success, not a confounder, and adjusting for it estimates a
controlled direct effect rather than the total causal effect of age. We
formalized both estimands under the backdoor criterion, developed a
propensity-score-matching estimator for the total effect with
inverse-probability-weighting and stratification cross-checks and a
Rosenbaum-bounds sensitivity analysis for unmeasured founder ability, and
extended the framework to nonlinear and heterogeneous age effects.

No computational implementation or empirical evaluation on real data has
been carried out; the illustrative example in Section VI is a small,
hand-computed synthetic case that demonstrates the estimation mechanism, not
a validated empirical finding. The most immediate next steps are:

1. Collect and integrate founder age, industry, team size, funding, and
   outcome data from Crunchbase and Y Combinator, and macroeconomic
   confounders from Census and BLS sources, as outlined in the underlying
   research idea's dataset plan.
2. Implement the propensity-score estimation, matching, IPW, and
   stratification pipeline computationally, e.g., using DoWhy
   [@sharma2020dowhy], following the general treatment-effect estimation
   practice surveyed in Cunningham [@cunningham2021mixtape], and verify
   positivity and covariate balance on the real covariate distribution
   rather than the illustrative Table II.
3. Compute a real Rosenbaum-bounds sensitivity analysis (Section IV-D) at the
   sample sizes available in the collected data, rather than the
   underpowered five-pair illustration of Section VI.
4. Investigate instrumental-variable designs [@angrist1996identification],
   using macroeconomic shocks (e.g., recessions or technology booms) at the
   time of founding as a candidate instrument for age cohort, to partially
   address the unmeasured-ability threat identified in Section VII, while
   explicitly testing the exclusion restriction this requires.
5. Estimate the causal-forest heterogeneity model of Section V-B on real
   industry and founding-year data to test whether the age effect differs
   across sectors as the literature suggests.
6. Extend the outcome model from a binary success indicator to a
   time-to-exit survival specification, to test whether age affects not only
   whether a startup succeeds but how quickly.
