# Decision Theory and Bayesian Decision Making

// msml610/lectures_source/Lesson07.1-Intro_to_Probabilistic_Programming.txt
// https://github.com/gpsaggese/gpsaggese.github.io/tree/master/msml610/lectures/Lesson07.1-Intro_to_Probabilistic_Programming.pdf
// msml610/lectures_source/Lesson07.2-Posterior_Based_Decisions.txt
// https://github.com/gpsaggese/gpsaggese.github.io/tree/master/msml610/lectures/Lesson07.2-Posterior_Based_Decisions.pdf
// msml610/lectures_source/Lesson07.5-Bayesian_Model_Comparison.txt
// https://github.com/gpsaggese/gpsaggese.github.io/tree/master/msml610/lectures/Lesson07.5-Bayesian_Model_Comparison.pdf
// msml610/lectures_source/Lesson09.3-Multi_Armed_Bandits.txt
// https://github.com/gpsaggese/gpsaggese.github.io/tree/master/msml610/lectures/Lesson09.3-Multi_Armed_Bandits.pdf

## Utility Theory, Loss Functions, and Expected Utility

### Motivating Problem-Dependent Decision Making

In many practical problems, simply describing a posterior distribution is insufficient. We need to make decisions based on inference. The challenge becomes especially acute when the costs or benefits of different decisions are asymmetric.

For example, consider a medical diagnosis where:

- The cost of a false negative (missing a serious disease) is extremely high
- The cost of a false positive (unnecessary treatment) is relatively low

In such asymmetric scenarios, a standard point estimate of the posterior (like the mean) may not be the best basis for decision-making. We need a framework that explicitly accounts for the consequences of different choices.

### Loss Functions and Expected Utility

A **loss function** (also called a cost function) quantifies "how bad is an estimation mistake?" It measures the discrepancy between:

- The true value θ (unknown)
- Our estimated value θ̂

Larger loss indicates worse estimation. The inverse perspective—focusing on gain rather than cost—is known as a **utility function**.

The key insight is that different loss functions lead to different optimal point estimates from the same posterior:

- **Quadratic loss**: $L(θ, θ̂) = (θ - θ̂)^2$
  - Minimized by the **mean** of the posterior
  - Emphasizes large errors (squaring them)
  - Appropriate when errors in both directions are equally bad

- **Absolute loss**: $L(θ, θ̂) = |θ - θ̂|$
  - Minimized by the **median** of the posterior
  - More robust to outliers than quadratic loss
  - Appropriate for symmetric but moderate penalties

- **0-1 loss**: $L(θ, θ̂) = I(θ ≠ θ̂)$
  - Minimized by the **mode** of the posterior
  - Binary classification: correct or incorrect
  - Appropriate when only exact match matters

### Bayesian Decision Rule

The algorithm for making optimal decisions using a loss function:

1. **Estimate the posterior distribution**: Combine prior belief with observed data
2. **Minimize expected loss**: Find θ̂ that minimizes the expected loss over the posterior
   $$\hat{\theta}^* = \argmin_{\hat{\theta}} \mathbb{E}_{\theta | \text{data}}[L(\theta, \hat{\theta})]$$
3. **Make the decision**: Use θ̂* as your point estimate

This framework generalizes naturally to more complex decision problems beyond point estimation, including classification and action selection.

### References

- Berger, J. O. (1985). Statistical Decision Theory and Bayesian Analysis (2nd ed.). Springer.
- Robert, C. P. (2007). The Bayesian Choice: From Decision-Theoretic Foundations to Computational Implementation (2nd ed.). Springer.
- DeGroot, M. H. (1970). Optimal Statistical Decisions. McGraw-Hill.

## Risk Preferences and Risk-aware Decisions

### The Role of Risk in Decision Making

Real-world decisions often involve risk and uncertainty. Decision-makers exhibit different preferences toward risk, which should be reflected in their loss functions and expected utility calculations.

### Characterizing Risk Preferences

Decision-makers can be categorized based on their attitude toward risk:

- **Risk-averse**: Prefers certainty over gambling with the same expected value
  - Example: Willing to accept lower expected return for less variance
  - Utility function is concave
  - Common in safety-critical applications (medical treatments, engineering)

- **Risk-neutral**: Indifferent between gambles with the same expected value
  - Focuses on maximizing expected value only
  - Utility function is linear
  - Standard assumption in many economic models

- **Risk-seeking**: Prefers gambles to certain outcomes with the same expected value
  - Willing to take high-variance options for higher potential upside
  - Utility function is convex
  - Less common in practice; sometimes appears in startup ventures

### Incorporating Risk into Loss Functions

Risk preferences can be embedded in loss functions through:

- **Weighted loss functions**: Assign higher penalties to errors in certain directions
  - Asymmetric cost structure: False negatives cost more than false positives

- **Variance-aware objectives**: Explicitly penalize posterior uncertainty
  - Quadratic loss plus regularization term for variance
  - Encourages exploration in sequential decision problems

- **Quantile-based decisions**: Select decisions that achieve specific risk guarantees
  - 95th percentile confidence intervals ensure robustness
  - Useful for worst-case scenario planning

### References

- von Neumann, J., & Morgenstern, O. (1944). Theory of Games and Economic Behavior. Princeton University Press.
- Savage, L. J. (1954). The Foundations of Statistics. Wiley.
- Pratt, J. W. (1964). Risk Aversion in the Small and in the Large. Econometrica, 32(1), 122-136.

## Multi-criteria Decisions and Trade-offs

### The Pareto Frontier Perspective

Many real-world decisions involve multiple competing objectives with no clear "best" solution. A decision is **Pareto optimal** if you cannot improve one criterion without worsening another.

### Common Multi-criteria Scenarios

- **Accuracy vs. Interpretability**: Machine learning models with higher accuracy often lack transparency
  - Healthcare: Accurate deep learning models vs. interpretable decision trees

- **Cost vs. Quality**: Production decisions trading off manufacturing cost against product quality

- **Exploration vs. Exploitation**: Sequential decision-making balancing learning new information against using known good decisions

### Decision-Making Approaches

- **Weighted aggregation**: Combine multiple objectives with weights reflecting priorities
  $$U(a) = w_1 \cdot U_1(a) + w_2 \cdot U_2(a) + \ldots$$

- **Constraint-based optimization**: Optimize one objective subject to minimum thresholds on others
  - Maximize accuracy subject to: interpretability score ≥ 0.8

- **Bayesian multi-objective optimization**: Use Gaussian processes to model tradeoffs and find promising regions of the Pareto frontier

### References

- Keeney, R. L., & Raiffa, H. (1993). Decisions with Multiple Objectives: Preferences and Value Tradeoffs. Cambridge University Press.
- Marler, R. T., & Arora, J. S. (2004). Survey of Multi-Objective Optimization Methods for Engineering. Structural and Multidisciplinary Optimization, 26(6), 369-395.
- Palar, P. S., & Shimoyama, K. (2019). Bayesian Optimization with a Probabilistic Pareto Selection. Journal of Global Optimization, 73(3), 619-649.

## Statistical Decision Theory and Bayes Optimal Decisions

### The Decision-Theoretic Framework

Statistical decision theory formalizes the relationship between:

- **Nature** (the true state of the world)
- **Agent** (the decision maker)
- **Action space** (possible decisions)
- **Loss function** (consequences of decisions)

### Bayes Optimal Decision Rule

Given a posterior distribution p(θ | data), the **Bayes optimal decision** minimizes expected loss:

$$a^* = \argmin_{a \in \mathcal{A}} \mathbb{E}_{\theta | \text{data}}[L(θ, a)]$$

This decision rule is **admissible**: No other decision rule dominates it for all possible parameter values.

### Key Principle: Posterior-Based Decisions

The posterior distribution contains all relevant information from the data about the unknown parameters. The Bayes optimal decision depends only on:

1. The posterior distribution p(θ | data)
2. The loss function L(θ, a)

NOT on:
- The specific data values (only through their influence on the posterior)
- The prior distribution (only through its influence on the posterior)
- The likelihood function (only through its influence on the posterior)

### Connection to Frequentist Concepts

- **Admissibility**: Bayes rules are admissible (unless the prior places zero probability on true parameter values)
- **Minimax decisions**: Choosing a prior that yields the worst-case loss
- **Complete class theorem**: Every admissible decision rule is a Bayes rule for some prior

### References

- Lehmann, E. L., & Casella, G. (1998). Theory of Point Estimation (2nd ed.). Springer.
- Ferguson, T. S. (1967). Mathematical Statistics: A Decision-Theoretic Approach. Academic Press.
- Ghosh, J. K., Delampady, M., & Samanta, T. (2006). An Introduction to Bayesian Analysis. Springer.

## Bayesian Inference and Posterior-based Decisions

### From Inference to Decision

Sometimes describing the posterior distribution is not enough—we need to translate inference into actionable decisions. The challenge lies in making "sharp decisions" when the posterior remains uncertain about the true parameter value.

### Case Study: Coin Fairness Example

Consider testing whether a coin is fair (θ = 0.5):

- Posterior mean: μ̂ = 0.324 suggests bias
- But highest posterior interval (HPI) = [0.03, 0.65] includes 0.5
- Cannot rule out unbiased since the true value lies within our credible interval

Strategies to sharpen decisions:

1. **Collect more data** to reduce posterior spread
2. **Define more informative priors** based on domain knowledge
3. **Use principled hypothesis testing** methods (Bayesian model comparison)

### Point Estimate Selection by Loss Function

Different loss functions yield different optimal decisions from the same posterior:

| Loss Type | Formula | Optimal Estimate | Use Case |
|-----------|---------|------------------|----------|
| Quadratic | (θ - θ̂)² | Posterior mean | Continuous estimation |
| Absolute | \|θ - θ̂\| | Posterior median | Robust estimation |
| 0-1 | I(θ ≠ θ̂) | Posterior mode | Classification |

### Savage-Dickey Density Ratio for Hypothesis Testing

The **Savage-Dickey ratio** tests point null hypotheses in Bayesian inference by comparing prior and posterior densities at a specific point:

$$BF_{01} = \frac{p(θ_0 | H_1)}{p(θ_0 | \text{data}, H_1)}$$

where:
- p(θ₀ | H₁) = prior density under alternative hypothesis
- p(θ₀ | data, H₁) = posterior density under alternative hypothesis

**Interpretation**: Shows how data changes belief about θ₀

If posterior density at θ₀ is much smaller than prior density, strong evidence against the null hypothesis H₀.

**Bayes Factor Scale**:

| BF Range | Interpretation |
|----------|----------------|
| 1-3 | Not enough evidence |
| 3-10 | Substantial evidence |
| 10-100 | Strong evidence |
| > 100 | Decisive evidence |

**Limitation**: Point statistic that doesn't consider the entire posterior distribution

### Region of Practical Equivalence (ROPE)

Instead of point hypotheses, **ROPE** defines an interval where parameter values are "practically equivalent":

- **Example**: For coin fairness, ROPE = [0.45, 0.55] (close enough to 0.5)
- Can't reject H₀: "coin is fair" if ROPE is too wide

**Decision rule using ROPE and HPI** (Highest Posterior Interval):

- HPI within ROPE → No effect, reject H₁ (no significant difference)
- HPI outside ROPE → Effect present, reject H₀ (significant difference exists)
- HPI overlaps ROPE → Inconclusive (need more data)

**Critical principle**: Decide ROPE before analysis based on domain knowledge. Choosing it after seeing results introduces selection bias (analogous to p-hacking).

### Chemical Shift Example: Robust Inference

**Context**: Nuclear magnetic resonance (NMR) measures chemical shift to reveal molecular structure. Observed data appears roughly Gaussian with a few outliers.

**Initial approach**: Assume Gaussian likelihood with weakly informative priors:
- μ ∼ U(40, 70)
- σ ∼ HalfNormal(0, 10)

**Problem identified**: Posterior predictive check shows the model poorly reproduces data:
- Posterior mean shifted toward outliers
- Posterior std dev increased
- Model cannot generate realistic data

**Solution**: Use Student's t-distribution (heavy tails) instead of Normal:
- Degrees of freedom ν ∼ Exp(λ) (unknown, estimated from data)
- Student's t has tail behavior: ν = 1 (Cauchy, extreme tails) to ν → ∞ (Gaussian)

**Result with Student's t**:
- Estimation more robust to outliers
- Posterior mean closer to true central tendency
- Posterior std dev smaller
- Posterior predictive checks show better fit

### References

- Gelman, A., Carlin, J. B., Stern, H. S., Dunson, D. B., Vehtari, A., & Rubin, D. B. (2013). Bayesian Data Analysis (3rd ed.). Chapman & Hall/CRC.
- Kruschke, J. K. (2014). Doing Bayesian Data Analysis: A Tutorial with R, JAGS, and Stan (2nd ed.). Academic Press.
- Martin, O. A., Kumar, R., & Lao, J. (2018). Bayesian Modeling and Computation in Python. ArXiv preprint.

## Thompson Sampling and Bayesian Optimization

### Multi-Armed Bandits: The Core Problem

**Setting**: Imagine facing K slot machines (arms) with unknown reward distributions. At each time step you must:

1. Choose which arm to play
2. Receive a random reward from that arm
3. Decide whether to try other arms or exploit the best known option

**Central Challenge**: Balance exploration (learning which arms are best) vs. exploitation (playing the best arm found so far).

### The Exploration-Exploitation Tradeoff

This tradeoff is unavoidable:

- **Pure exploitation**: Never try uncertain arms → Risk getting stuck with suboptimal choice forever
- **Pure exploration**: Always try random arms → High information but low rewards
- **Optimal policy**: Explore enough to find good arms, exploit enough to gain high rewards

### Thompson Sampling Algorithm

**Thompson Sampling** (posterior sampling) is an elegant Bayesian approach:

**Algorithm**:
1. Maintain posterior distribution for each arm's reward mean μᵢ
2. At each time step t:
   - Sample θ̃ᵢ ∼ p(μᵢ | data) for each arm i
   - Pull arm A_t = argmax_i θ̃ᵢ (choose best sample)
   - Observe reward R_t
   - Update posterior for arm A_t using Bayes' rule

**Intuition**: "Probability matching"
- If arm i is likely optimal, its sample will often be highest
- If arm i is uncertain, randomness ensures it still gets tried
- As arms are explored, uncertainty decreases, exploration naturally reduces

### Concrete Example: Bernoulli Bandits

**Setup**: K arms, each returns 1 (success) with probability μᵢ, else 0

**Bayesian framework**:
- Prior: μᵢ ∼ Beta(1, 1) (uniform) for each arm
- Likelihood: R ∼ Bernoulli(μᵢ)
- Posterior: p(μᵢ | successes=s, failures=f) = Beta(1+s, 1+f)

**Algorithm**:
1. Initialize: αᵢ = 1, βᵢ = 1 for each arm
2. At time t:
   - Sample θ̃ᵢ ∼ Beta(αᵢ, βᵢ) for each arm
   - Pull A_t = argmax_i θ̃ᵢ
   - If R_t = 1: αₐₜ += 1; else: βₐₜ += 1

**Performance**:
- Achieves O(log T) cumulative regret (near-optimal)
- Often outperforms UCB in practice (better constants)
- Naturally incorporates prior knowledge

### Bayesian Optimization

**Motivation**: Optimize an expensive black-box function where:
- Evaluations are costly (experiments, simulations)
- Gradient information unavailable
- Need efficient search strategy

**Bayesian optimization approach**:
1. Maintain a surrogate model (usually Gaussian Process) of function landscape
2. Use acquisition function to decide next evaluation point
   - Balance exploration (uncertain regions) vs. exploitation (high mean)
3. Update surrogate model with new observation
4. Repeat until budget exhausted

**Key insight**: Use posterior uncertainty to guide exploration toward promising regions

### References

- Agrawal, S., & Goyal, N. (2012). Thompson Sampling for 1-Dimensional Exponential Family Bandits. In Advances in Neural Information Processing Systems (pp. 1775-1783).
- Golovin, D., Solnik, B., Moitra, S., Kochanski, G., Karro, J., & Sculley, D. (2017). Google Vizier: A Service for Black-Box Optimization. In Proceedings of the 23rd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining (pp. 1487-1495).
- Brochu, E., Cora, V. M., & de Freitas, N. (2010). A Tutorial on Bayesian Optimization of Expensive Cost Functions, with Application to Active User Modeling and Hierarchical Reinforcement Learning. arXiv preprint arXiv:1012.2599.

## Bayesian Hypothesis Testing for Practitioners

### Moving Beyond Null Hypothesis Significance Testing

Traditional frequentist hypothesis testing focuses on p-values: the probability of observing data as or more extreme than observed, assuming the null hypothesis is true. Bayesian approaches offer direct answers to practitioners' actual questions.

### Bayesian vs. Frequentist P-Values

**Frequentist p-value**: P(observed data as or more extreme | H₀ is true)
- Focuses on long-run properties
- Cannot directly state probability that hypothesis is true given data

**Bayesian approach**: p(H₁ | data) and p(H₀ | data)
- Direct probability of hypotheses given observed data
- Incorporates prior beliefs
- Naturally handles multiple comparisons

### Bayes Factors and Model Comparison

The **Bayes factor** compares two hypotheses:

$$BF_{10} = \frac{p(\text{data} | H_1)}{p(\text{data} | H_0)}$$

This ratio tells us how much more likely the data is under H₁ than H₀.

**Advantages of Bayes factors**:
- Can provide evidence for null hypothesis (traditional tests cannot)
- No need for p-value adjustments in multiple comparisons
- Interpretation is straightforward probability ratio

### Posterior Predictive Checks

Rather than checking if a model is "true" (it never is), evaluate if it can reproduce observed data:

**PPC workflow**:
1. Fit probabilistic model to observed data y
2. Generate predictions ỹ from posterior distribution
3. Compare summary statistics T of predictions vs. data
4. Compute Bayesian p-value: Pr(T(ỹ) ≥ T(y) | y)

**Interpretation**:
- Value close to 0.5: Model fits well
- Value close to 0 or 1: Model has problems
- Identifies specific aspects where model fails

### Bayesian P-Value

Given posterior distribution p(θ | y), generate predictions ỹ and compare:

1. Choose summary statistic T (mean, median, std dev, etc.)
2. Compute T for observed data: T_obs
3. For each posterior sample, compute T for simulated data: T_sim
4. Bayesian p-value = fraction where T_sim ≥ T_obs

**Key benefit**: Incorporates parameter uncertainty in the check (unlike frequentist approach using point estimates)

### References

- Kass, R. E., & Raftery, A. E. (1995). Bayes Factors. Journal of the American Statistical Association, 90(430), 773-795.
- Guo, Y., & Sarkar, S. K. (2016). Controlling the False Discovery Rate by Fraction of False Positives. Journal of the Royal Statistical Society: Series B (Statistical Methodology), 79(5), 1333-1358.
- Gelman, A., Meng, X. L., & Stern, H. (1996). Posterior Predictive Assessment of Model Fitness via Realized Discrepancies. Statistica Sinica, 6(4), 733-760.

## Aleatoric Vs. Epistemic Uncertainty

### Two Types of Uncertainty

Real-world predictions contain two fundamentally different sources of uncertainty:

**Aleatoric Uncertainty** (data uncertainty):
- Arises from inherent randomness in the process
- Irreducible: cannot decrease with more data
- Example: Coin flip outcome (even if we know μ = 0.5 perfectly)
- Also called: irreducible error, noise, stochasticity

**Epistemic Uncertainty** (model uncertainty):
- Arises from lack of knowledge about the process
- Reducible: decreases as we collect more data
- Example: Not knowing whether a coin has μ = 0.4 or μ = 0.6
- Also called: reducible error, uncertainty, ignorance

### Bayesian Perspective on Both Types

The posterior predictive distribution naturally combines both:

$$p(\tilde{y} | y) = \int p(\tilde{y} | θ) p(θ | y) dθ$$

where:
- **p(θ | y)**: Posterior distribution—captures epistemic uncertainty about parameters
- **p(ỹ | θ)**: Likelihood—captures aleatoric uncertainty for given θ

Total predictive uncertainty = parameter uncertainty + observation noise

### Practical Implications

- **For model improvement**: Focus on epistemic uncertainty (more data, better model)
- **For risk assessment**: Must account for both types
- **For decision-making**: High epistemic uncertainty → need more data before deciding

### Quantifying Both Types

- **Posterior mean**: E[ỹ | y] captures central prediction
- **Posterior variance**: Var[ỹ | y] = E[Var[ỹ | θ]] + Var[E[ỹ | θ]]
  - First term: aleatoric uncertainty (irreducible)
  - Second term: epistemic uncertainty (reducible)

### References

- Kendall, A., & Gal, Y. (2017). What Uncertainties Do We Need in Bayesian Deep Learning for Computer Vision?. In Advances in neural information processing systems (pp. 5574-5584).
- Hora, S. C. (1996). Aleatory and Epistemic Uncertainty in Probabilistic Risk Assessment. In Probabilistic Safety Assessment and Management (pp. 1071-1076).
- Spiegelhalter, D. J., & Ruttenberg, A. M. (1994). Regression Methods for Estimating Interactions between Treatment and Covariates. Statistics in Medicine, 13(15), 1517-1528.

## Confidence Intervals and Prediction Intervals

### From Posterior to Intervals

A full posterior distribution is ideal, but practitioners often need a simple interval summarizing uncertainty. Different intervals answer different questions.

### Highest Posterior Interval (HPI)

The **Highest Posterior Interval** (also called Highest Density Interval or HDI):

- Defines interval containing α% of posterior probability
- Selects the narrowest such interval
- Interpretation: The α% most credible parameter values

**Construction**:
1. Sort posterior samples by density
2. Include samples with highest density until α% accumulated
3. Resulting interval is the shortest credible interval

**Key properties**:
- Directly answers: "What is the most likely range for θ?"
- Interpretation is straightforward (not backwards like frequentist CI)
- Depends on prior through posterior

### Credible Intervals vs. Confidence Intervals

**Bayesian Credible Interval**:
- P(θ ∈ [L, U] | data) = 0.95 (θ is in interval with 95% probability)
- Direct probability statement
- Depends on both prior and data

**Frequentist Confidence Interval**:
- P(procedure includes true θ) = 0.95 (across repeated sampling)
- Probability statement about procedure, not parameter
- θ is fixed (though unknown), interval is random
- Does not depend on prior (doesn't use one)

### Prediction Intervals

Prediction intervals address a different question: "Where will future observations fall?"

**Posterior Predictive Interval**:
- P(ỹ ∈ [L, U] | observed data) = 0.95
- Averages over both parameter uncertainty and observation noise
- Always wider than credible interval for parameters
- Captures aleatoric uncertainty that parameters alone cannot eliminate

### Calibration

An α% credible interval is **calibrated** if, across many problems with similar structure:
- Approximately α% of intervals contain the true parameter

Well-specified Bayesian models with proper priors are typically calibrated. This is not guaranteed for frequentist methods without careful analysis.

### References

- Gelman, A., Carlin, J. B., Stern, H. S., Dunson, D. B., Vehtari, A., & Rubin, D. B. (2013). Bayesian Data Analysis (3rd ed.). Chapman & Hall/CRC.
- Newcombe, R. G. (2000). Two-Sided Confidence Intervals for the Single Proportion: Comparison of Seven Methods by Robert G. Newcombe. Statistics in Medicine, 17(8), 857-872.
- Carpenter, B., Gelman, A., Hoffman, M. D., Lee, D., Goodrich, B., Betancourt, M., ... & Riddell, A. (2017). Stan: A Probabilistic Programming Language. Journal of Statistical Software, 76(1).

## TUTORIAL: PyMC (Bayesian Inference, Uncertainty Quantification, and Posterior-based Decisions)

## TUTORIAL: BoTorch (Bayesian Optimization for Sequential Decision Making)
