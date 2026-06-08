# Notebook Outline: Refuting Causal Estimates

## Learning Objectives

By the end of this notebook, students will be able to:

- Understand the falsification-based philosophy for validating causal analysis
- Distinguish between estimation methods that pass and fail refutation tests
- Apply negative control refutation methods (placebo, dummy outcome, random confounder, subsample)
- Interpret refutation test results and identify problematic estimators
- Conduct sensitivity analysis to assess robustness to unobserved confounding
- Compare competing causal estimation methods using refutation results
- Decide when and how to apply each refutation technique to real problems

## Cell 1: Why We Cannot Prove Causality (Markdown + Visualization)

**Purpose**: Build intuition about the fundamental limitations of causal inference from observational data

**Content Description**:

- Core principle: observational data alone cannot prove causal relationships are correct
  - Statistical correlations can arise from causation, reverse causation, or confounding
  - Many causal graphs produce the same statistical patterns (observational equivalence)
  - No amount of data can rule out hidden confounders
- Karl Popper's falsification philosophy: we cannot prove a causal claim true, but we can try to refute it
- Intuitive examples showing why failed assumptions matter
  - Example 1: Drug efficacy study with hidden health awareness confounder
  - Example 2: Marketing impact analysis confounded by seasonal trends
- Visual comparison: methods that pass multiple robustness tests vs. those that fail

**Expected Output**:

- Clear explanation of the asymmetry: failure proves problems, success doesn't prove correctness
- Visual examples showing equivalent causal structures producing different refutation test results
- Intuition that confidence comes from surviving many challenges, not from proving correctness

## Cell 2: Introduction to Refutation Methods (Markdown + Table)

**Purpose**: Survey the landscape of refutation approaches and when to use each

**Content Description**:

- Two main categories of refutations
  - Negative control refutations: test necessary conditions that good estimators must satisfy
  - Sensitivity analysis: test robustness when key assumptions are relaxed
- Overview of four negative control refutation methods
  - **Placebo treatment refuter**: assigns fake treatment to test for spurious effects
  - **Dummy outcome refuter**: uses artificial outcome variable to detect systematic bias
  - **Random common cause refuter**: introduces random confounders to test if estimator ignores them
  - **Data subsample refuter**: checks consistency across different samples and time periods
- Overview of sensitivity analysis approaches
  - Simulation-based: directly perturb the data to simulate unobserved confounding
  - Partial R² based: uses observed variance to bound the strength of hidden confounders
  - Reisz estimator based: bounds treatment effect under violations of no unmeasured confounding
- Comparison table: method name, what it tests, interpretation, when to use
- Key principle: if an estimator fails any test (p-value < 0.05), it indicates methodological problems

**Expected Output**:

- Clear table summarizing all refutation methods
- Visual flowchart showing decision points for choosing refutation approaches
- Understanding that multiple tests provide convergent validation

## Cell 3: Simple Synthetic Data with Known Truth (Code + Visualization)

**Purpose**: Establish a baseline where we know the true causal effect to validate refutation methods

**Content Description**:

- Generate synthetic data from a simple causal model with known ground truth
  - Three variables: $X$ (treatment), $Y$ (outcome), $Z$ (confounder)
  - True causal effect: treatment increases outcome by fixed amount (e.g., ATE = 2.0)
  - Data generation includes hidden confounder or selection bias
- Visualize the data-generating process
  - DAG showing true causal structure
  - Scatter plot of $X$ vs. $Y$ colored by $Z$
  - Distribution of treated vs. untreated populations
- Store ground truth effect size for later comparison

**Key Variables**:

- Sample size (e.g., 500 samples)
- True average treatment effect (e.g., ATE = 2.0)
- Strength of confounder effect
- Random seed for reproducibility

**Expected Output**:

- Synthetic dataset with labeled treatment, outcome, and covariates
- Visualization of the causal structure and data patterns
- Printed statement of ground truth effect size

## Cell 4: Naive Estimation Reveals the Problem (Code)

**Purpose**: Demonstrate that naive methods can give very wrong answers

**Content Description**:

- Estimate causal effect using naive methods (simple difference in means, linear regression without adjusting for confounders)
- Compare naive estimates to the ground truth
- Show that the naive estimate is biased (differs from true ATE)
- Discuss why this happens: omitted variable bias, confounding
- Visualize the bias: true effect vs. estimated effect with confidence interval

**Key Variables**:

- Estimation method (e.g., simple mean difference, OLS regression)
- Confidence level for intervals (e.g., 95%)

**Expected Output**:

- Point estimate of causal effect from naive method
- Confidence interval showing the range
- Comparison with ground truth, highlighting the bias
- Print message: "Naive estimator is off by X units"

## Cell 5: Placebo Treatment Refutation (Code + Interactive)

**Purpose**: Learn how placebo treatment tests detect spurious effects and methodological problems

**Content Description**:

- Concept: if we assign a fake treatment that cannot possibly have a causal effect, a good estimator should find zero effect
- Apply placebo treatment refutation to the naive estimator from Cell 4
  - Create random placebo treatment (no causal effect on outcome)
  - Apply same estimation method to estimate placebo treatment effect
  - Run refutation multiple times with different random treatments
  - Collect distribution of placebo effect estimates
- Visualize results: histogram of placebo effects
  - Good estimator: placebo effects concentrated around zero
  - Bad estimator: placebo effects systematically non-zero
- Compare naive estimator's placebo effects to true treatment effect
- Interactive widget: adjust key parameters (sample size, noise level) and see how placebo distribution changes

**Key Variables**:

- Number of placebo treatments to generate (e.g., 50)
- Random seed for reproducibility

**Expected Output**:

- Distribution of placebo treatment effects (histogram or violin plot)
- Summary statistics (mean, std dev of placebo effects)
- Comparison: is the true effect within the placebo distribution? (indicates spurious estimation)
- p-value showing probability that observed effect could have arisen by chance

## Cell 6: Dummy Outcome Refutation (Code)

**Purpose**: Learn how dummy outcome tests reveal systematic bias in estimation methods

**Content Description**:

- Concept: create artificial outcome variable with no causal relationship to treatment, estimator should find zero effect
- Apply dummy outcome refutation to naive estimator
  - Generate multiple artificial outcomes (e.g., random noise, shuffled real outcome)
  - Estimate treatment effect on each dummy outcome
  - Collect distribution of dummy outcome effects
- Visualize results: histogram of dummy outcome effects
  - Interpretation: if estimator finds non-zero effects on outcomes that shouldn't be affected, it indicates bias
- Compare with true treatment effect
- Discuss what dummy outcome refutation tests: whether the estimator is finding signals in noise

**Key Variables**:

- Number of dummy outcomes to generate (e.g., 100)
- Type of dummy outcome (random, shuffled, permuted)

**Expected Output**:

- Distribution of effects on dummy outcomes
- Summary showing mean dummy effect and confidence interval
- Comparison with true effect: how does true effect compare to dummy effects?
- Visual marker: if true effect is extreme in dummy distribution, that's good

## Cell 7: Random Common Cause Refutation (Code)

**Purpose**: Test whether estimator incorrectly adjusts for confounders that have no causal effect

**Content Description**:

- Concept: introduce random variables as fake confounders, a good estimator should not change estimates when we wrongly adjust for them
- Apply random confounder refutation to naive estimator
  - Generate random variables with no causal relationship to treatment or outcome
  - Re-estimate treatment effect while wrongly adjusting for each random confounder
  - Collect distribution of estimated effects with different fake confounders
- Visualize results: how much does estimated effect change when we adjust for random variables?
  - Good estimator: estimated effect stays stable (doesn't change much)
  - Bad estimator: estimated effect varies widely depending on which random variables are included
- Interpretation: sensitivity to confounder choice reveals lack of robustness

**Key Variables**:

- Number of random confounders to introduce (e.g., 10)
- Method for adjusting for confounders (e.g., linear regression with additional covariates)

**Expected Output**:

- Distribution of estimated effects as random confounders are added
- Visualization: scatter plot or violin plot showing estimate variability
- Summary: standard deviation of estimates across different confounder sets
- Interpretation: how much does the estimate fluctuate?

## Cell 8: Data Subsample Refutation (Code)

**Purpose**: Test consistency and stability of estimates across different data subsets

**Content Description**:

- Concept: if causal relationship is real and estimation is robust, effect estimate should be consistent across random subsamples
- Apply subsample refutation to naive estimator
  - Repeatedly sample random subsets of the data (e.g., 80% samples)
  - Estimate treatment effect on each subset
  - Collect distribution of subsample estimates
- Visualize results: histogram or time series of subsample estimates
  - Good estimator: subsample estimates concentrated around a point, low variance
  - Bad estimator: subsample estimates highly variable, unstable
- Compare variance across subsamples to variance expected from random sampling alone

**Key Variables**:

- Subsample size (e.g., 80% of original data)
- Number of subsamples (e.g., 50)
- Random seed

**Expected Output**:

- Distribution of treatment effect estimates across subsamples
- Visualization showing mean and confidence interval of subsample estimates
- Summary statistics: mean effect and standard error
- Stability assessment: how consistent are the estimates?

## Cell 9: Sensitivity Analysis to Unobserved Confounding (Code + Interactive)

**Purpose**: Understand how robust causal estimates are when key assumptions are violated

**Content Description**:

- Core concept: we cannot observe hidden confounders, but we can test robustness by assuming they exist and checking if conclusions hold
- Generate data with varying degrees of hidden confounding
  - Create scenarios where a hidden confounder has increasing strength
  - Re-estimate treatment effect under each scenario
- Three approaches to sensitivity analysis
  - Simulation-based: directly add noise/confounding and re-estimate
  - Partial R² based: use observed variance patterns to bound hidden confounder strength
  - Reisz estimator based: derive bounds on treatment effect assuming unobserved confounding
- Interactive widget: adjust strength of hidden confounder, see how estimate changes
  - Slider for confounder strength relative to observed confounding
  - Real-time visualization of sensitivity range

**Key Variables**:

- Strength of simulated hidden confounder (as multiple of observed confounder strength)
- Assumed correlation structure between hidden confounder and treatment/outcome
- Bootstrap samples for uncertainty quantification

**Expected Output**:

- Sensitivity plot showing treatment effect estimate as hidden confounding increases
- Visualization: effect estimate with confidence band showing plausible range
- Interpretation: at what level of hidden confounding would conclusions reverse?
- Interactive feedback: "effect remains significant if hidden confounder explains < X% of residual variance"

## Cell 10: Comparing Multiple Estimators via Refutations (Code + Visualization)

**Purpose**: Use refutation tests to rank competing causal estimation methods

**Content Description**:

- Apply all refutation methods to multiple estimators (e.g., naive regression, propensity score matching, doubly robust)
- For each estimator, collect results from cells 5-9
  - Placebo test p-value
  - Dummy outcome test p-value
  - Subsample variability (standard error)
  - Sensitivity bounds
- Create comparison scorecard: which estimators pass most tests?
- Visualization: heatmap showing pass/fail for each estimator and test
- Calculation: count tests passed (failures: p < 0.05)
- Discussion: which estimator is most trustworthy based on refutation battery?

**Key Variables**:

- List of estimators to compare (e.g., 3-5 methods)
- Significance level (alpha = 0.05)
- Refutation test choices

**Expected Output**:

- Comparison table: estimator × refutation test
- Visual heatmap showing pass/fail status
- Summary scorecard: number of tests passed per estimator
- Recommendation: which estimator would you trust most and why?

## Cell 11: Real Data Example: Refuting a Job Training Study (Code + Interactive)

**Purpose**: Apply complete refutation workflow to realistic problem with stakes

**Content Description**:

- Realistic scenario: evaluate impact of job training program on earnings
- Dataset: individuals with varying training participation and post-training earnings
- Setup similar to classic econometric studies with potential selection bias
- Apply one correct estimator (e.g., doubly robust) and one incorrect estimator (e.g., naive OLS)
- Run full refutation battery on both
  - Placebo: what happens when we estimate effect of non-existent past training?
  - Dummy outcome: does estimator find effects on unrelated outcomes?
  - Subsamples: is effect stable across years or demographic groups?
  - Sensitivity: how much hidden confounding would reverse the conclusion?
- Visualize results: side-by-side comparison showing correct estimator passes all tests, naive fails

**Key Variables**:

- Real or realistic synthetic dataset
- Treatment: training participation (binary)
- Outcome: post-training earnings
- Confounders: age, education, prior income

**Expected Output**:

- Estimated training effect from both estimators
- Refutation results showing which estimator is credible
- Narrative conclusion: "Based on refutation tests, we have more confidence in Method X because..."
- Discussion of remaining limitations and unmeasured confounding risks

## Cell 12: Synthesis and Decision Framework (Markdown + Interactive)

**Purpose**: Develop practical judgment about when to trust causal estimates

**Content Description**:

- Decision framework: how to decide whether a causal analysis is trustworthy
  - Checklist of refutation tests to run
  - Interpretation guide: when are results concerning vs. reassuring?
  - When to dig deeper vs. when conclusions are robust enough
- Common patterns in refutation results and what they mean
  - All tests pass: high confidence in causal estimate
  - Placebo test fails: suggests spurious estimation
  - Sensitivity widens with small confounding: estimate is fragile
  - Subsample inconsistency: suggests unmeasured confounding or treatment heterogeneity
- Practical guidance
  - Which refutation tests to prioritize for different problem types
  - How to communicate results to stakeholders who want certainty
  - When to combine multiple estimators using refutation-based weighting
- Interactive summary: reflect on each tutorial dataset and describe what refutation results would convince you to trust the causal claim

**Expected Output**:

- Practical decision checklist for practitioners
- Reference table: problem type → recommended refutation tests
- Clear communication template for presenting refutation results
- Summary of key takeaway: causal inference is about finding robust signals that survive systematic challenges, not about statistical proof

