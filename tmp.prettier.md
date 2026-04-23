# Chapter 5. Propensity Score

## Overview

- Propensity score weighting is an alternative to linear regression for adjusting confounding bias
- Uses a model of the treatment assignment mechanism to reweight data
- Combines with orthogonalization principles to achieve double robustness
- Particularly suited for binary or discrete treatments
- Extension available for continuous treatments via generalized propensity score (GPS)

## The Impact of Management Training

### Context and Problem
- Tech companies often transition talented individual contributors to management roles
- Many new managers lack management skills despite technical expertise
- A multinational company invested in manager training to ease the transition
- Goal: measure training effectiveness using employee engagement scores

### Data Structure
- Treatment: `intervention` (whether manager received training)
- Outcome: `engagement_score` (average standardized employee engagement)
- Confounders: `tenure`, `n_of_reports`, `gender`, `role`, `department_size`, `department_score`, `last_engagement_score`
- Challenge: noncompliance (some assigned managers didn't attend, others attended without assignment)

### Noncompliance
- When individuals don't receive intended treatment, called noncompliance
- Transforms randomized study into observational one requiring bias adjustment
- More details in Chapter 11 on instrumental variables

## Adjusting with Regression (Baseline)

- Naive comparison (no adjustment): ATE = 0.4346 (biased, overstates effect)
- Regression with confounders: ATE = 0.2677 (adjusted estimate shows positive bias existed)
- Indicates managers with more engaged teams were more likely to participate
- Propensity weighting compared against this regression baseline

## Propensity Score

### Core Concept
- **Propensity score**: Conditional probability of receiving treatment given covariates
- Formula: $e(x) = P(T \mid X)$ 
- Acts as dimensionality reduction: instead of conditioning on high-dimensional $X$, condition on single propensity score
- Blocks backdoor paths through confounders
- Balancing property: $\left( Y_{1},Y_{0} \right) \perp T \mid P(x)$

### Intuition
- If two managers have same propensity score but different treatment status, difference is due to chance
- Treatment becomes "as good as random" after controlling for propensity score
- Causal graph shows X → e(x) → T structure

## Propensity Score Estimation

### Logistic Regression Approach
- Use logistic regression to estimate $e(x)$ from covariates
- Binary treatment makes logistic regression natural choice
- Replace true (unknown) propensity score with estimated version
- Apply in observational data where assignment mechanism unknown

### Machine Learning Alternative
- Can use ML models to estimate propensity score
- Requires careful attention to:
  - Calibrated probability predictions
  - Out-of-fold predictions to avoid overfitting bias
- Use sklearn's calibration module and cross-validation

## Propensity Score and Orthogonalization

- Freilich-Wooldridge-Newey (FWL) theorem: linear regression models $E[T \mid X]$ in debiasing step
- Propensity score estimation via logistic regression achieves similar orthogonalization
- Can use estimated propensity score $\hat{e}(X)$ in regression: engagement_score ~ intervention + propensity_score
- Result ($\hat{ATE} = 0.263$) remarkably similar to regression with all covariates
- Both approaches orthogonalize treatment but use different models for $T$

## Propensity Score Matching

### Method
- Matches treated and control units based on propensity score similarity
- Essentially 1-Nearest Neighbors (KNN with K=1) on propensity score
- Fit KNN on treated units to impute $Y_1$ for controls
- Fit KNN on control units to impute $Y_0$ for treated
- Matched value is outcome of nearest unit

### Matching Estimator Formula
$$
\hat{ATE} = \frac{1}{N}\sum\left\{ \left( {Y_{i} - Y_{jm}(i)} \right)T_{i} + \left( {Y_{jm}(i) - Y_{i}} \right)\left( 1 - T_{i} \right) \right\}
$$

- Drawbacks (author's view):
  - Biased estimator with bias increasing in dimensionality
  - Difficult to derive variance
  - KNN inefficient in high dimensions (though less issue when using propensity score alone)
  - Not recommended compared to inverse propensity weighting

### Bias Correction for Matching
- Can add bias correction using outcome models $\hat{\mu}_0(X)$ and $\hat{\mu}_1(X)$
- Requires fitting conditional expectation functions on matched data

## Inverse Propensity Weighting (IPW)

### Core Principle
- Reweight data by inverse probability of observed treatment
- Create pseudo-population where treatment appears randomly assigned
- For treated: upweight those unlikely to be treated (low $e(x)$)
- For control: upweight those likely to be treated (high $e(x)$)

### Mathematical Formulation
$$
E[Y_t] = E\left[\frac{1(T = t)Y}{P(T = t \mid X)}\right]
$$

$$
ATE = E\left[\frac{1(T = 1)Y}{P(T = 1 \mid X)}\right] - E\left[\frac{1(T = 0)Y}{P(T = 0 \mid X)}\right]
$$

### Simplified Formula
$$
ATE = E\left[Y\frac{T - e(x)}{e(x)(1 - e(x))}\right]
$$

### Intuition for Weighting
- Treated individuals with low propensity look like untreated → high weight to estimate $Y_1 \mid T=0$
- Control individuals with high propensity look like treated → high weight to estimate $Y_0 \mid T=1$
- Balances treatment groups to appear randomly assigned

### IPW Implementation
- Estimate propensity score via logistic regression
- Calculate weights: $w_t = 1/\hat{e}(X)$ for treated, $w_{nt} = 1/(1-\hat{e}(X))$ for control
- Compute weighted means and take difference
- Result in management training data: $\hat{ATE} = 0.266$ (similar to regression)

### Comparison with Regression
- Regression: $\tau_{ols} = E[Y(T - E[T \mid X])] / E[Var(T \mid X)]$
- IPW: $\tau_{ipw} = E[Y(T - E[T \mid X]) / Var(T \mid X)]$
- Key difference: regression weights by treatment variance, IPW doesn't
- Both essentially orthogonalize treatment but with different weighting schemes

## Variance of IPW

### Bootstrap Confidence Intervals
- Standard error for IPW not straightforward like linear regression
- Use bootstrap method: resample with replacement multiple times
- Fit IPW estimator on each sample
- Calculate 2.5th and 97.5th percentiles for 95% CI

### Implementation Pattern
- Wrap IPW estimation in reusable function
- Use sklearn's LogisticRegression (faster than statsmodels)
- Use patsy's dmatrix for R-style formulas
- Apply bootstrap with parallel processing (joblib)

### Variance Drivers
- High variance when few units in critical regions:
  - Few control units with high propensity score
  - Few treated units with low propensity score
- Large weights create variance (few units drive estimate)
- Balancing large weights is key challenge

## Stabilized Propensity Weights

### Motivation
- Raw inverse propensity weights can be very large
- Treatment with low probability creates extreme weights
- Computational stability issue

### Stabilization Formula
$$
w = \frac{P(T = t)}{P(T = t \mid X)}
$$

- Balances small denominator with also small numerator
- Produces more stable weights without changing balancing properties
- Sum of weights in each group matches original group sizes

### Properties
- Reconstructs marginal $P(T = t)$ instead of unconditional $P(T = t) = 1$
- Effective sample size of pseudo-population matches original treated/control group sizes
- Yields identical ATE estimate to unstabilized weights
- Much better computational properties

## Pseudo-Populations

### Concept
- IPW creates artificial population where treatment appears random
- In pseudo-population with IPW weights, $P(T \mid X) = P(T)$

### Understanding Bias Removal
- Original data: treatment distribution differs by $X$ (confounding)
- After IPW reweighting:
  - Low-propensity treated units upweighted
  - High-propensity control units upweighted
  - Two treatment distributions now overlap
  - Treatment becomes independent of $X$ in weighted sample

### Visual Understanding
- Plot propensity score distributions by treatment status
- Before weighting: distributions shifted (confounding)
- After weighting: distributions overlap (treatment appears random)
- Overlapping distributions essential for IPW validity

## Selection Bias

### Beyond Confounding
- IPW originally developed (Horvitz-Thompson 1952) for selection bias
- Can adjust for nonresponse in surveys
- Can handle both confounding and selection together

### Application Example
- Survey respondents may differ from nonrespondents
- Estimate probability of responding $P(R = 1 \mid X)$
- Reweight respondents by $1/\hat{P}(R = 1)$ to account for who didn't respond
- Creates pseudo-population representing full population

### Combined Adjustment
- When facing both confounding and selection bias:
$$
W = \frac{\hat{P}(T = t)}{\hat{P}(R = 1 \mid X)\hat{P}(T = t \mid X)}
$$

## Bias-Variance Trade-Off

### Core Tension
- Better treatment prediction → lower bias but higher variance
- Precise propensity model concentrates treatment in narrow regions
- Few treated units with low propensity score = high variance
- Perfect treatment model = no units for counterfactual estimation

### Under Randomization
- If treatment truly random: $P(T \mid X) = P(T)$
- Propensity score has zero predictive power
- Best-case scenario: no predictive power but low variance

### Precision vs Accuracy
- Very precise $e(x)$ model:
  - High $e(x)$ for all treated (correctly predicts treatment)
  - Low $e(x)$ for all control
  - No treated units with low $e(x)$ to estimate $Y_1 \mid T = 0$
- Overfitting propensity score increases variance substantially

### Noise-Inducing Controls
- Same logic from Chapter 4: variables predicting $T$ but not causing $Y$ only add variance
- Must balance modeling bias sources vs. inducing high variance

### Trimming Strategy
- Trim propensity scores to avoid extreme weights (e.g., keep between 1% and 99%)
- Alternatively, clip weights to maximum value (e.g., max weight = 100)
- Creates biased estimator but may reduce mean squared error
- Trade-off: slight bias for substantial variance reduction

## Positivity Assumption

### Definition
- Positivity: every unit has positive probability of receiving each treatment level
- Formally: $0 < P(T = t \mid X) < 1$ for all $t$ and $X$
- Essential for IPW validity

### Problem When Violated
- Some subgroups have almost no treated (or control) units
- Cannot estimate counterfactual outcomes in those regions
- IPW has no data to reconstruct pseudo-population

### IPW Sensitivity
- IPW fails when positivity violated: cannot reweight units that don't exist
- Propensity score distribution easy to visualize
- Can directly check if treatment groups overlap

### Comparison with Regression
- Regression can extrapolate beyond region with data
- Assumes linear (or specified) functional form for $E[Y \mid T, X]$
- Can recover ATE even with positivity violation if model specification correct
- IPW makes no functional form assumptions → fails without positivity

### Positivity-Bias Trade-Off
- More covariates in propensity model → stronger unconfoundedness but weaker positivity
- Fewer covariates → better positivity but potential confounding bias
- Balance is contextual and requires judgment

## Design-Based vs Model-Based Identification

### Two Paradigms

**Design-Based (IPW)**
- Makes assumptions about treatment assignment mechanism
- Models $P(T \mid X)$
- Reweights data to create pseudo-population
- Nonparametric: makes no assumptions on outcome function

**Model-Based (Regression)**
- Makes assumptions about conditional outcome function
- Models $E[Y \mid T, X]$
- Imputes missing potential outcomes
- Parametric: assumes functional form

### When to Choose Each
- Good understanding of treatment assignment? → Use design-based IPW
- Better understanding of outcome process? → Use model-based regression
- Design-based fails without positivity, model-based needs correct specification
- Personal judgment call based on data context

### Regression as Hybrid
- Can view regression as both design-based and model-based
- From orthogonalization perspective: design-based
- From outcome model perspective: model-based
- Combines advantages of both when correctly specified

## Doubly Robust Estimation

### Core Idea
- Combines propensity score weighting (design-based) with outcome modeling (model-based)
- Only requires ONE of the two models to be correctly specified
- Gets "two shots" at being correct

### Mathematical Formulation
$$
\hat{\mu}_t^{DR}(\hat{m}, \hat{e}) = \frac{1}{N}\sum\hat{m}(X) + \frac{1}{N}\sum\left[\frac{T}{\hat{e}(x)}(Y - \hat{m}(X))\right]
$$

Where:
- $\hat{m}(X)$: outcome model (e.g., linear regression)
- $\hat{e}(X)$: propensity score model

### Robustness Properties

**If propensity model wrong but outcome model correct:**
- Second term converges to zero (since $E[Y - \hat{m}(X)] = 0$)
- Left with first term: correct outcome model
- Estimates average outcome directly

**If outcome model wrong but propensity model correct:**
- Rewrite as: $\hat{\mu}_t^{DR} = \frac{1}{N}\sum\frac{TY}{\hat{e}(X)} + \frac{1}{N}\sum\frac{T - \hat{e}(X)}{\hat{e}(X)}\hat{m}(X)$
- Second term converges to zero (since $T - \hat{e}(X) \approx 0$ when propensity model correct)
- Left with first term: IPW estimator
- Estimates via reweighting correctly

### DR for Treatment Effect
$$
ATE = \hat{\mu}_1^{DR}(\hat{m}, \hat{e}) - \hat{\mu}_0^{DR}(\hat{m}, \hat{e})
$$

### Implementation
- Fit propensity score model: logistic regression
- Fit two outcome models: one for treated, one for control
- Each outcome model predicts on full dataset
- Combine both to form DR estimator for each potential outcome
- Take difference for ATE

### Advantages
- More precise than pure IPW when both models somewhat correct
- Guards against misspecification in either component
- Maintains consistency as long as one model is right

## Treatment Is Easy to Model (DR Example 1)

### Scenario
- Treatment assignment easy to predict (follows logistic form)
- Outcome relationship complex and nonlinear
- True ATE = 2.006

### Why Regression Fails
- Simple linear regression: ATE = 1.787 (underestimates)
- Cannot capture cubic relationship in outcome
- Misses treatment effect heterogeneity

### Why Regression Can Work
- With correct functional form (including cubic term): ATE = 1.997
- But in practice, don't know true functional form
- Would need exploratory analysis or prior knowledge

### IPW Performance
- Propensity score: ATE = 2.002 (accurate)
- 95% CI: [1.808, 2.226]
- Works well because treatment model correct
- No assumptions on outcome functional form

### DR Performance
- DR ATE = 2.002 (accurate)
- 95% CI: [1.871, 2.145]
- Narrower confidence interval than pure IPW
- More efficient when propensity model correct despite wrong outcome model

### Key Insight
- When $P(T \mid X)$ easy to model but $E[Y_t \mid X]$ complex
- DR leverages correct propensity model and improves variance
- Avoids burden of correctly specifying outcome nonlinearity

## Outcome Is Easy to Model (DR Example 2)

### Scenario
- Outcome relationship simple and linear
- Treatment assignment complex and nonlinear (cubic form)
- True ATE = -1.0

### Why IPW Fails
- Logistic propensity model cannot capture cubic relationship
- Estimates ATE = -1.104 (biased)
- 95% CI: [-1.143, -1.066]
- Misses true value due to propensity model misspecification

### Why Regression Works
- Linear regression: ATE = -1.001 (accurate)
- Simple outcome model correct
- No need to model complex treatment assignment

### DR Performance
- DR ATE = -1.003 (accurate)
- 95% CI: [-1.042, -0.964]
- Recovers truth despite wrong propensity model
- Outcome model "rescues" the estimate

### Key Insight
- When $E[Y_t \mid X]$ easy to model but $P(T \mid X)$ complex
- DR leverages correct outcome model to get right answer
- Propensity model errors don't matter when outcome model correct

### Practical Takeaway
- Don't need to get both models perfect
- Having one correct is sufficient
- DR provides insurance policy against model misspecification
- Flexible approach when uncertain about data generation process

### Variations of DR
- Fit outcome model with propensity score weights
- Add propensity score as covariate to regression
- Linear regression is technically DR (models $e(x) = \beta X$)
- Many DR variants exist (see Robins et al. for comprehensive treatment)

## Generalized Propensity Score for Continuous Treatment

### Challenge with Continuous Treatment
- Continuous variables have zero probability: $P(T = t) = 0$
- Cannot estimate $P(T = t \mid X)$ for continuous $T$
- Infinitely many potential outcomes $Y_t$
- No parametric response function assumption

### Approach: Work with Density
- Use conditional density $f(T \mid X)$ instead of probability
- Assume treatment follows normal distribution: $T \sim N(\mu_i, \sigma^2)$
- Estimate parameters: mean via OLS, variance from residuals

### Generalized Propensity Score (GPS)
- GPS evaluates conditional density at observed treatment value
- Formula for normal: $f(t_i) = \frac{\exp(-(1/2)((t_i - \mu_i)/\sigma)^2)}{\sigma\sqrt{2\pi}}$
- Use scipy.stats.norm for implementation
- Produces vector of density values, one per observation

### Beyond Normal Distribution
- Can use generalized linear models for other distributions
- Poisson for count treatment: use GLM with Poisson family
- Negative binomial, gamma, etc. as needed
- Extract predicted mean and use scipy distributions

### IPW with GPS
- Create weights: $w = 1/GPS$
- Use weighted least squares to estimate treatment effect
- Upweights unlikely treatments (far from predicted mean)
- Downweights likely treatments (close to prediction)

### Problem with Unstabilized GPS Weights
- Can become extremely large (weights > 1000 in example)
- Creates high variance in estimates
- Few high-weight units drive the estimate
- Difficult to interpret

### Stabilized GPS Weights
- Stabilize by marginal density $f(t)$: $w = f(t) / f(t \mid x)$
- Estimate $f(t)$ from treatment mean and variance
- Results in effective sample size ≈ original sample size
- Much smaller weights with better numerical stability
- Lower variance while maintaining consistency

### Properties of Stabilized GPS
- Weights sum to approximately original sample size
- More interpretable: upweight units with unlikely treatment combinations with $x$ values
- Reduces variance substantially compared to unstabilized
- Gets closer to true ATE with tighter confidence intervals
- Example: unstabilized CI [-0.811, -0.526], stabilized CI [-0.858, -0.710]

### Alternative Approaches
- Include GPS as covariate in regression (Hirano-Imbens)
- Segment data by predicted treatment, fit local regressions (Imai-van Dyk)
- Use causal-curve Python package for scikit-learn style API
- More options available as continuous treatment literature advances

### When to Use GPS vs Regression
- Author's preference: regression with functional form assumptions
- GPS useful when treatment functional form unknown
- Continuous treatment has few data points around specific treatment values
- Pooling information across neighboring treatments preferable

## Key Ideas and Summary

### Comparison of Core Methods
- **Regression**: Models $E[Y \mid T, X]$, orthogonalizes treatment, uses OLS
- **IPW**: Models $P(T \mid X)$, reweights by inverse propensity, creates pseudo-population
- **DR**: Combines both, only needs one to be correct

### Reweighting Formula
$$
w = \frac{P(T)}{P(T \mid X)}
$$

This makes treatment appear drawn from distribution not depending on $X$

### Visual Intuition (Figure 5-1)
- Original data: biased relationship due to confounding through $X$
- Orthogonalization: residualize treatment, removes $X$ correlation
- IPW: reweight data, treatment distributions overlap
- Both recover positive causal effect though using different mechanisms

### When to Use Each Method
- **Discrete treatment, clear assignment process**: IPW
- **Continuous treatment**: Regression with functional form
- **Uncertain about specification**: Doubly robust (IPW + regression)
- **Discrete treatment + outcome unknown**: DR recommended

### Practical Recommendations
- IPW works well with discrete treatments
- Pair with outcome modeling for doubly robust approach
- For continuous treatment: prefer regression (better than GPS)
- Use stabilized weights to reduce variance
- Check positivity assumption via propensity score visualization
- Use bootstrap for confidence intervals
