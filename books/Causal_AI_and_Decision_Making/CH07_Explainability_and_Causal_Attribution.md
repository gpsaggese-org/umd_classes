# Sensitivity Analysis and Causal Model Validation
// Not covered

## Why Causal Estimates Can Be Fragile

- Causal inference from observational data depends on **untestable assumptions**
  - Unlike prediction, where we can evaluate performance on held-out data,
    causal estimates rely on structural assumptions about the data-generating
    process that we cannot directly verify
  - The entire identification strategy rests on assumptions like unconfoundedness,
    positivity, and correct model specification

- Key sources of fragility in causal estimates:
  - **Unobserved confounders**: variables that affect both treatment and outcome
    but are not measured in the data
  - **Model misspecification**: choosing the wrong functional form for the
    outcome model or propensity score
  - **Positivity violations**: regions of the covariate space where treatment
    assignment is deterministic (probability 0 or 1), making counterfactual
    estimation impossible
  - **Measurement error**: treatment or outcome variables measured with noise,
    biasing estimates toward or away from zero

- The fundamental problem: **we can never observe both potential outcomes** for
  the same unit
  - In a randomized experiment, randomization ensures balance on average across
    all confounders (observed and unobserved)
  - In observational studies, we must explicitly account for every relevant
    confounder — and we can never be sure we have done so

- This is why sensitivity analysis is essential: it asks _"How much would an
  unobserved confounder need to influence treatment and outcome to explain
  away our estimated effect?"_

- A useful analogy: causal estimates are like a **bridge supported by
  assumptions**
  - Sensitivity analysis is the **stress test** — it tells you how much load
    the bridge can bear before collapsing
  - A robust causal estimate survives plausible violations of assumptions; a
    fragile one does not

## Unmeasured Confounding and Its Consequences

- **Unmeasured confounding** (also called omitted variable bias) occurs when a
  variable $U$ exists such that:
  - $U$ influences the treatment $T$
  - $U$ influences the outcome $Y$
  - $U$ is not included in the adjustment set

- Graphically, this creates a **backdoor path** from $T$ to $Y$ through $U$
  that cannot be blocked:

  ```graphviz
  digraph unmeasured_confounding {
    rankdir=TB;
    node [shape=ellipse, fontname="Helvetica"];
    edge [fontname="Helvetica"];

    U [label="U (unmeasured)", style=dashed];
    T [label="T (treatment)"];
    Y [label="Y (outcome)"];
    X [label="X (observed\ncovariates)"];

    U -> T;
    U -> Y;
    X -> T;
    X -> Y;
    T -> Y [label="causal effect?"];
  }
  ```

- Consequences of unmeasured confounding:
  - **Biased treatment effect estimates**: the estimated effect includes both
    the true causal effect and the spurious association through $U$
  - **Direction of bias is unknown**: depending on the signs of the
    relationships, bias can inflate or deflate the estimated effect
  - **Confidence intervals are misleading**: standard errors and p-values
    assume no unmeasured confounding, so statistical significance does not
    imply causal validity

- Classic example: estimating the effect of **education on earnings**
  - Ability is a likely unmeasured confounder: high-ability individuals both
    pursue more education and earn more
  - Naive regression of earnings on education overestimates the causal effect
    because part of the association is driven by ability
  - This motivated the use of instrumental variables (e.g., proximity to
    college) and natural experiments in labor economics

- The **omitted variable bias formula** for linear models:
  $$\text{Bias} = \gamma \cdot \delta$$
  where $\gamma$ is the effect of the unmeasured confounder $U$ on the outcome
  $Y$, and $\delta$ is the relationship between $U$ and the treatment $T$
  conditional on observed covariates
  - Both $\gamma$ and $\delta$ must be nonzero for bias to exist
  - The formula shows that bias depends on the **product** of two relationships:
    how strongly $U$ predicts treatment and how strongly $U$ predicts outcome

- Key insight: **there is no statistical test** that can detect unmeasured
  confounding from observed data alone
  - This is a fundamental limitation, not a technical one
  - The best we can do is quantify **how sensitive** our conclusions are to
    hypothetical unobserved confounders of various strengths

## Rosenbaum Bounds and E-values

- **Rosenbaum bounds** provide a framework for sensitivity analysis in
  matched observational studies
  - Developed by Paul Rosenbaum in the 1980s-2000s as part of his work on
    observational studies

- The core idea: introduce a parameter $\Gamma$ (capital gamma) that quantifies
  the degree of departure from random treatment assignment
  - $\Gamma = 1$: treatment assignment is as-if random (no unmeasured
    confounding)
  - $\Gamma = 2$: two matched individuals with identical observed covariates
    could differ in their odds of treatment by a factor of 2 due to an
    unmeasured confounder
  - $\Gamma = 3$: odds could differ by a factor of 3, and so on

- Formally, for two matched individuals $i$ and $j$ with the same observed
  covariates:
  $$\frac{1}{\Gamma} \leq \frac{P(T_i = 1) / P(T_i = 0)}{P(T_j = 1) / P(T_j = 0)} \leq \Gamma$$
  - This bounds the ratio of odds of treatment between matched individuals

- How to use Rosenbaum bounds in practice:
  1. Conduct a matched study and compute the treatment effect estimate and
     p-value under the assumption $\Gamma = 1$ (no hidden bias)
  2. Gradually increase $\Gamma$ and recompute the p-value bounds
  3. Find the **critical value** $\Gamma^*$ at which the conclusion changes
     (e.g., the p-value exceeds 0.05)
  4. Report: _"The conclusion is robust to unmeasured confounders that change
     the odds of treatment by up to a factor of $\Gamma^*$"_

- Example interpretation:
  - If $\Gamma^* = 1.2$, the result is fragile — a weak unmeasured confounder
    could explain it away
  - If $\Gamma^* = 6$, the result is robust — an unmeasured confounder would
    need to increase the odds of treatment sixfold to nullify the effect

- **E-values** (introduced by VanderWeele and Ding, 2017) offer a more
  intuitive and general sensitivity measure:
  - The **E-value** is the minimum strength of association (on the risk ratio
    scale) that an unmeasured confounder would need to have with **both**
    treatment and outcome to fully explain away the observed effect
  - For an observed risk ratio $RR$:
    $$E\text{-value} = RR + \sqrt{RR \times (RR - 1)}$$
  - The E-value for the confidence interval bound is also reported: this tells
    you how strong confounding would need to be to shift the confidence
    interval to include the null

- Advantages of E-values over Rosenbaum bounds:
  - **Applicable beyond matched designs**: works with any study design that
    produces a risk ratio, odds ratio, or hazard ratio
  - **Intuitive interpretation**: a single number that summarizes robustness
  - **Easy to compute**: available through online calculators and R/Python
    packages

- Example: a study finds that a drug reduces mortality with $RR = 0.5$
  (halves the risk)
  - $E\text{-value} = 2 + \sqrt{2 \times 1} = 2 + 1.41 \approx 3.4$
  - An unmeasured confounder would need a risk ratio of at least 3.4 with both
    treatment and outcome to explain away the observed effect
  - Is that plausible? Domain knowledge is needed to judge

## Refutation Methods: Random Common Cause, Data Subset, Placebo Treatment

- **Refutation tests** take a different approach to sensitivity analysis: instead
  of parameterizing the strength of an unmeasured confounder, they **perturb**
  the data or model and check whether the estimate changes in expected ways

- The logic follows **Karl Popper's falsificationism**: we cannot prove a causal
  model is correct, but we can try to **refute** it
  - If a model survives multiple refutation attempts, we gain confidence
    (though not certainty) in its validity

- Three key refutation methods:

- **Random common cause test**:
  - Add a randomly generated variable as an additional confounder to the model
  - Re-estimate the causal effect including this random variable
  - **Expected result**: the estimate should **not change** significantly,
    because a random variable cannot be a real confounder
  - **If the estimate changes**: this suggests the model is sensitive to the
    inclusion of additional covariates, raising concerns about unmeasured
    confounding
  - This test checks the **stability** of the estimate to covariate adjustment

- **Data subset test** (bootstrap refutation):
  - Re-estimate the causal effect on random subsets of the data
  - **Expected result**: the estimate should remain **stable** across subsets
  - **If the estimate varies widely**: this suggests the estimate depends on
    specific data points and may not be robust
  - This is related to the idea of **influence functions** in robust statistics
    — how much does the estimate change when observations are removed?

- **Placebo treatment test** (permutation test):
  - Replace the real treatment variable with a randomly permuted version
    (breaking the true treatment-outcome relationship)
  - Re-estimate the causal effect with the placebo treatment
  - **Expected result**: the estimated effect should be **close to zero**,
    because the shuffled treatment has no causal relationship with the outcome
  - **If the estimate is significantly nonzero**: this suggests the method is
    picking up spurious associations, possibly due to model misspecification

- Additional refutation approaches:
  - **Placebo outcome**: replace the outcome with a variable known to be
    unrelated to the treatment — the estimated effect should be zero
  - **Negative control exposure**: use a treatment known to have no effect on
    the outcome — the method should return a null result
  - **Positive control**: use a treatment-outcome pair where the causal effect
    is well established — the method should recover the known effect

- How to interpret refutation results:
  - Refutation tests are **necessary but not sufficient**: passing them does not
    prove the causal model is correct
  - Failing a refutation test is a **strong signal** that something is wrong
  - Think of refutation tests as a **diagnostic panel**: each test probes a
    different vulnerability, and together they provide a more complete picture

## How to Know If Your Causal Model Is Wrong

- There is no single test that definitively validates or invalidates a causal
  model, but several strategies can help detect problems

- **Testable implications of causal graphs**:
  - A causal DAG implies certain **conditional independence** relationships among
    observed variables (via d-separation)
  - These can be tested empirically: if the data violate an implied conditional
    independence, the DAG is wrong
  - Example: if your DAG says $X \perp Y \mid Z$, but a partial correlation
    test rejects this independence, then the graph is misspecified
  - Tools: the `daggity` R package and DoWhy can enumerate testable implications

- **Overidentification tests**:
  - If a causal effect can be estimated via multiple identification strategies
    (e.g., backdoor adjustment and instrumental variables), compare the
    estimates
  - Large discrepancies suggest at least one set of assumptions is violated
  - This is analogous to the **Hausman test** in econometrics

- **Falsification outcomes**:
  - Identify outcomes that the treatment should **not** affect based on domain
    knowledge
  - Estimate the treatment effect on these outcomes
  - A nonzero effect suggests confounding or model misspecification
  - Example: if studying the effect of a job training program on wages, check
    whether the program also "affects" pre-treatment outcomes (it should not)

- **Pre-treatment covariate balance** (for propensity score methods):
  - After matching or weighting, check that treated and control groups are
    balanced on observed covariates
  - Standardized mean differences (SMD) should be small (typically < 0.1)
  - Poor balance indicates that the propensity model is inadequate

- **Cross-validation of causal estimates**:
  - Split data into training and validation sets
  - Estimate the causal model on training data and check stability on
    validation data
  - Large discrepancies indicate overfitting or instability

- A practical checklist for causal model validation:
  1. State all assumptions explicitly (draw the DAG)
  2. Test conditional independencies implied by the DAG
  3. Run refutation tests (random common cause, placebo, data subset)
  4. Compute sensitivity measures (E-values or Rosenbaum bounds)
  5. Compare estimates across multiple identification strategies if available
  6. Check falsification outcomes
  7. Assess covariate balance (for matching/weighting methods)
  8. Report robustness alongside point estimates

- Key mindset: treat causal modeling like **debugging software**
  - Assume your model is wrong until evidence accumulates otherwise
  - Each test is a unit test for a different assumption
  - A model that passes many tests is more trustworthy, but never proven correct

## TUTORIAL: DoWhy (built-in Refutation Tests and Sensitivity Analysis)

## TUTORIAL: IBM Causal Inference 360 (sensitivity Analysis for Observational Studies)

**References**

- Paul Rosenbaum, _Observational Studies_ (2nd ed., 2002) — comprehensive
  treatment of sensitivity analysis for matched studies, including Rosenbaum
  bounds
- Paul Rosenbaum, _Design of Observational Studies_ (2010) — practical guidance
  on designing observational studies that are robust to unmeasured confounding
- Tyler VanderWeele and Peng Ding, "Sensitivity Analysis in Observational
  Research: Introducing the E-Value" (2017) — introduces the E-value as a
  measure of robustness to unmeasured confounding
- Amit Sharma and Emre Kiciman, "DoWhy: An End-to-End Library for Causal
  Inference" (2020) — describes DoWhy's refutation framework for causal model
  validation
- Judea Pearl, _Causality: Models, Reasoning, and Inference_ (2nd ed., 2009)
  — foundational text on causal graphical models and testable implications
- Miguel Hernan and James Robins, _Causal Inference: What If_ (2020) — covers
  identification assumptions, sensitivity analysis, and practical causal
  inference methods
- Carlos Cinelli and Chad Hazlett, "Making Sense of Sensitivity: Extending
  Omitted Variable Bias" (2020) — modern sensitivity analysis framework
  extending the omitted variable bias formula
- Guido Imbens, "Sensitivity to Exogeneity Assumptions in Program Evaluation"
  (2003) — sensitivity analysis methods for treatment effect estimation
- Louisa Smith and Tyler VanderWeele, "The E-value" (2019) — accessible tutorial
  on E-value computation and interpretation
- IBM Research, "Causal Inference 360: A Python Package for Causal Inference"
  (2021) — toolkit including sensitivity analysis methods for observational
  studies