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

- In many real-world problems, we do not just want to estimate a parameter or
  learn a distribution. We want to **make a decision** and we need to quantify
  how good or bad each possible decision is

- **Utility theory** provides a formal framework for this
  - A **utility function** $U(\theta, a)$ assigns a numerical value to the
    outcome of taking action $a$ when the true state of the world is $\theta$
  - A rational agent should choose the action that maximizes **expected
    utility**, averaging over uncertainty about $\theta$

- Equivalently, we often work with **loss functions** (the negative of utility)
  - A **loss function** $L(\theta, \hat{\theta})$ quantifies "how bad is an
    estimation mistake?"
  - Larger loss indicates worse estimation
  - Loss measures the difference between the true value $\theta$ and the
    estimated value $\hat{\theta}$

- Common loss functions and their corresponding optimal point estimates:

  | **Loss** | **Expression** | **Optimal Point Estimate** |
  | :------- | :------- | :------- |
  | Quadratic (squared) loss | $(\theta - \hat{\theta})^2$ | Mean of the posterior |
  | Absolute loss | $\lvert\theta - \hat{\theta}\rvert$ | Median of the posterior |
  | 0-1 loss | $I(\theta \ne \hat{\theta})$ | Mode of the posterior |

- The **expected loss** (or Bayes risk) for a decision $\hat{\theta}$ is
  $$
  \mathbb{E}[L(\theta, \hat{\theta})] = \int L(\theta, \hat{\theta}) \, p(\theta | \text{data}) \, d\theta
  $$
  - The optimal decision minimizes this expected loss over the posterior
    distribution
  - This is the **Bayes optimal decision**: it is the best you can do given the
    available information

- **Why loss functions matter in practice**
  - Decision costs are often **asymmetric**: the cost of a bad decision may far
    exceed the benefit of a good one
  - For example, in medical diagnosis the cost of a false negative (missing a
    disease) is typically much greater than a false positive (unnecessary
    follow-up test)
  - Loss functions let us encode these asymmetries explicitly and make
    principled trade-offs

**References**
- James O. Berger, _Statistical Decision Theory and Bayesian Analysis_ (1985)
- Christian P. Robert, _The Bayesian Choice_ (2007)
- Andrew Gelman et al., _Bayesian Data Analysis_, 3rd Edition (2013), Chapter 5

## Risk Preferences and Risk-aware Decisions

- Different decision-makers have different **risk preferences**, and utility
  theory formalizes this via the shape of the utility function

- A decision-maker is:
  - **Risk-neutral** if they care only about expected value (linear utility)
  - **Risk-averse** if they prefer a certain outcome over a gamble with the same
    expected value (concave utility, e.g., $U(x) = \log(x)$)
  - **Risk-seeking** if they prefer the gamble over the certain outcome (convex
    utility)

- The **expected utility framework** (von Neumann-Morgenstern) states that
  rational preferences over uncertain outcomes can be represented by maximizing
  the expected value of a utility function
  - This is the foundation of modern decision theory

- In practice, risk preferences affect how we make decisions under uncertainty
  - A risk-averse investor may prefer a portfolio with lower expected return but
    also lower variance
  - A risk-neutral clinical trial designer treats all patients equally; a
    risk-averse one might favor treatments with more evidence

- **Bayesian decision theory** naturally handles risk preferences by
  integrating the utility function over the posterior distribution
  $$
  a^* = \arg\max_a \int U(\theta, a) \, p(\theta | \text{data}) \, d\theta
  $$
  - The posterior captures epistemic uncertainty about $\theta$
  - The utility function encodes the decision-maker's preferences and risk
    attitudes

- **Minimax decisions** represent an alternative, worst-case approach
  - Choose the action that minimizes the maximum possible loss:
    $a^* = \arg\min_a \max_\theta L(\theta, a)$
  - This is extremely conservative and does not require a prior distribution
  - Useful when the stakes are high and uncertainty is hard to quantify

**References**
- John von Neumann and Oskar Morgenstern, _Theory of Games and Economic Behavior_ (1944)
- Leonard J. Savage, _The Foundations of Statistics_ (1954)
- Daniel Kahneman and Amos Tversky, "Prospect Theory: An Analysis of Decision under Risk" (1979)

## Multi-criteria Decisions and Trade-offs

- Real-world decisions often involve **multiple competing objectives**
  - For example, a machine learning model deployment must balance accuracy,
    latency, fairness, and cost
  - A clinical trial must balance efficacy, safety, and patient burden

- **Multi-criteria decision making** (MCDM) provides frameworks for navigating
  these trade-offs
  - **Pareto optimality**: A solution is Pareto optimal if no objective can be
    improved without worsening another
  - The set of all Pareto optimal solutions forms the **Pareto frontier**
  - Decision-makers must choose a point on this frontier based on their
    preferences

- Common approaches:
  - **Weighted sum**: Combine objectives into a single scalar using weights
    $\sum_i w_i f_i(a)$, then optimize
    - Simple but requires choosing weights upfront
  - **Lexicographic ordering**: Rank objectives by priority; optimize the most
    important first, break ties with the next, etc.
  - **Constraint-based**: Optimize one objective subject to constraints on
    others (e.g., maximize accuracy subject to fairness $\geq$ threshold)

- **Bayesian approaches to multi-objective optimization**
  - Extend the utility function to multiple attributes:
    $U(\theta, a) = \sum_i w_i U_i(\theta, a)$
  - Use multi-objective Bayesian optimization (e.g., expected hypervolume
    improvement) to explore the Pareto frontier efficiently

- The key insight is that **there is no single "best" solution** when
  objectives conflict
  - The choice depends on the decision-maker's values and context
  - Making trade-offs explicit is better than hiding them in an opaque model

**References**
- Ralph L. Keeney and Howard Raiffa, _Decisions with Multiple Objectives_ (1993)
- Kaisa Miettinen, _Nonlinear Multiobjective Optimization_ (1998)
- Samuel Daulton et al., "Differentiable Expected Hypervolume Improvement for Parallel Multi-Objective Bayesian Optimization" (NeurIPS 2020)

## Statistical Decision Theory and Bayes Optimal Decisions

- **Statistical decision theory** unifies estimation, testing, and prediction
  under a single framework
  - A **decision rule** $\delta(x)$ maps observed data $x$ to an action $a$
  - The **risk** of a decision rule is its expected loss:
    $R(\theta, \delta) = \mathbb{E}_{X|\theta}[L(\theta, \delta(X))]$
  - A **Bayes optimal decision rule** minimizes the expected risk averaged over
    the prior:
    $\delta^* = \arg\min_\delta \int R(\theta, \delta) \, p(\theta) \, d\theta$

- The **Bayes estimator** under squared loss is the posterior mean
  - Under absolute loss, it is the posterior median
  - Under 0-1 loss, it is the posterior mode (MAP estimate)
  - These results follow directly from minimizing the expected posterior loss

- **Admissibility**: A decision rule is admissible if no other rule has
  uniformly smaller risk
  - Every Bayes rule (with a proper prior) is admissible
  - This is one of the strongest arguments for the Bayesian approach

- **Connection to frequentist methods**
  - Maximum likelihood estimation (MLE) corresponds to using a flat prior and
    taking the mode of the posterior
  - MLE is a point estimate, not a distribution of plausible values
  - Regularized estimators (ridge, lasso) correspond to specific prior
    distributions:
    - Ridge regression uses a normal prior on coefficients (pushing toward zero)
    - Lasso regression uses a Laplace prior (inducing sparsity)

- **Practical workflow for Bayesian decisions**
  1. Define the loss function based on the problem context
  2. Specify the probabilistic model (prior + likelihood)
  3. Compute the posterior distribution (analytically or numerically)
  4. Find the action that minimizes expected posterior loss

**References**
- James O. Berger, _Statistical Decision Theory and Bayesian Analysis_ (1985)
- Abraham Wald, _Statistical Decision Functions_ (1950)
- Andrew Gelman et al., _Bayesian Data Analysis_, 3rd Edition (2013), Chapters 2 and 5

## Bayesian Inference and Posterior-based Decisions

- **Bayes' theorem** is the engine of Bayesian inference
  $$
  p(\theta | X) = \frac{p(X | \theta) \cdot p(\theta)}{p(X)}
  $$
  where:
  - $p(\theta | X)$ is the **posterior**: probability of parameters $\theta$
    after seeing data $X$
  - $p(X | \theta)$ is the **likelihood**: plausibility of data $X$ given
    parameters $\theta$
  - $p(\theta)$ is the **prior**: knowledge about $\theta$ before any data
  - $p(X)$ is the **evidence** (marginal likelihood): probability of observing
    data $X$, averaging over all possible parameter values

- The posterior distribution is the complete answer to a Bayesian inference
  problem
  - It encodes all uncertainty about $\theta$ given the data
  - Every summary (mean, median, mode, credible intervals) is derived from it

- **Choosing priors**
  - **Weakly-informative priors**: provide minimal information, e.g.,
    $\beta \sim \text{Normal}(0, 10)$
  - **Regularizing priors**: encode known constraints, e.g.,
    $\sigma \sim \text{HalfCauchy}(0, 5)$ for a positive parameter
  - **Informative priors**: incorporate strong prior knowledge from experts or
    previous studies, e.g., $p \sim \text{Beta}(2, 38)$ when about 5% of cases
    are positive
  - **Prior elicitation**: compute the least informative distribution satisfying
    given constraints (maximum entropy approach)

- **Posterior-based decisions**
  - Sometimes describing the posterior is not enough: we need to **make
    decisions based on inference**
  - For example, after estimating the bias $\theta$ of a coin:
    - $\mathbb{E}[\hat{\theta}] = 0.324$ suggests bias
    - But the highest posterior interval (HPI) $[0.03, 0.65]$ contains 0.5, so
      we cannot rule out a fair coin
    - For sharper decisions: collect more data or use a more informative prior

- **Key Bayesian decision tools**
  - **Savage-Dickey density ratio**: Tests a point null hypothesis by comparing
    prior and posterior densities at the null value
    $BF_{01} = p(\theta_0 | H_1) / p(\theta_0 | \mathcal{D}, H_1)$
  - **ROPE (Region of Practical Equivalence)**: Define an interval where values
    are practically equivalent to the null
    - Compare ROPE with the HPI: if HPI is within ROPE, no effect; if HPI is
      outside ROPE, effect is present; if they overlap, inconclusive
  - **Loss-based decisions**: Pick $\hat{\theta}$ minimizing expected loss
    under the posterior (as described in earlier sections)

- **Posterior predictive checks (PPC)**
  - Generate predictions from the posterior and compare to observed data
  - If the model cannot reproduce the observed data, it is inadequate
  $$
  p(\tilde{y} | y) = \int p(\tilde{y} | \theta) \, p(\theta | y) \, d\theta
  $$
  - PPC is the primary tool for model validation in Bayesian workflows

- **Bayesian workflow**
  1. Design a probabilistic model (prior + likelihood)
  2. Condition on data to obtain the posterior
  3. Validate with posterior predictive checks
  4. Make decisions using the posterior and a loss function
  - Steps may involve backtracking: correct coding errors, improve the model,
    or gather more data

**References**
- Osvaldo Martin, _Bayesian Analysis with Python_, 2nd Edition (2018)
- Andrew Gelman et al., _Bayesian Data Analysis_, 3rd Edition (2013)
- John K. Kruschke, _Doing Bayesian Data Analysis_, 2nd Edition (2015)
- Stuart Russell and Peter Norvig, _Artificial Intelligence: A Modern Approach_, 4th Edition (2020), Chapter 15

## Thompson Sampling and Bayesian Optimization

- **Thompson Sampling** is a Bayesian algorithm for sequential decision-making
  under uncertainty, originally proposed by William R. Thompson in 1933

- **The multi-armed bandit problem**
  - Imagine facing $K$ slot machines ("arms"), each with an unknown probability
    of winning
  - At each time step, choose one arm, observe a random reward, and learn
  - **Goal**: Maximize total reward over $T$ rounds
  - **Central challenge**: Balance **exploration** (trying uncertain arms to
    learn their rewards) with **exploitation** (playing the arm believed to be
    best)

- **Thompson Sampling algorithm** (for Bernoulli bandits with Beta priors)
  1. Initialize: For each arm $i$, set $\alpha_i = 1, \beta_i = 1$ (uniform
     prior)
  2. At each round $t$:
     - Sample $\tilde{\mu}_i \sim \text{Beta}(\alpha_i, \beta_i)$ for each arm
     - Pull arm $A_t = \arg\max_i \tilde{\mu}_i$
     - Observe reward $R_t$
     - Update: if $R_t = 1$, increment $\alpha_{A_t}$; else increment
       $\beta_{A_t}$

- **Why Thompson Sampling works**
  - It implements "probability matching": it pulls arm $i$ with probability
    approximately equal to $\Pr(i \text{ is optimal} | \text{data})$
  - If an arm is uncertain, its posterior sample might be high, driving
    exploration
  - As more data is collected, posteriors sharpen and the algorithm
    concentrates on the best arm

- **Theoretical guarantees**
  - Achieves $O(\log T)$ cumulative regret, matching the Lai-Robbins lower
    bound (order-optimal)
  - Often outperforms UCB (Upper Confidence Bound) in practice with better
    constants

- **Comparison with other bandit algorithms**
  - **Epsilon-greedy**: Explore randomly with probability $\epsilon$; simple
    but achieves only $O(T)$ or $O(T^{2/3})$ regret
  - **UCB (Upper Confidence Bound)**: Pull the arm with the highest upper
    confidence bound $\hat{\mu}_i + \sqrt{2 \log t / N_i(t)}$; achieves
    $O(\log T)$ regret but explores uniformly in its uncertainty
  - **Thompson Sampling**: Directs exploration toward promising arms via
    posterior sampling; empirically often faster to converge

- **Bayesian Optimization** extends these ideas to continuous, expensive-to-evaluate functions
  - **Problem**: Optimize $f(x)$ where each evaluation is costly (e.g.,
    hyperparameter tuning, drug design, engineering design)
  - **Approach**:
    1. Place a **Gaussian process (GP)** prior over $f$
    2. After each evaluation, update the GP posterior
    3. Use an **acquisition function** to decide where to evaluate next
  - Common acquisition functions:
    - **Expected Improvement (EI)**: Expected amount of improvement over the
      current best
    - **Upper Confidence Bound (GP-UCB)**: $\mu(x) + \kappa \sigma(x)$,
      trading off predicted mean and uncertainty
    - **Knowledge Gradient**: Value of information from the next evaluation

- Bayesian optimization is the continuous analog of Thompson Sampling: both
  use Bayesian posteriors to balance exploration and exploitation in sequential
  decisions

**References**
- William R. Thompson, "On the Likelihood that One Unknown Probability Exceeds Another in View of the Evidence of Two Samples" (1933)
- Shipra Agrawal and Navin Goyal, "Analysis of Thompson Sampling for the Multi-Armed Bandit Problem" (COLT 2012)
- Peter Auer, Nicolo Cesa-Bianchi, Paul Fischer, "Finite-time Analysis of the Multiarmed Bandit Problem" (2002)
- Tze Leung Lai and Herbert Robbins, "Asymptotically Efficient Adaptive Allocation Rules" (1985)
- Bobak Shahriari et al., "Taking the Human Out of the Loop: A Review of Bayesian Optimization" (2016)
- Carl Edward Rasmussen and Christopher K. I. Williams, _Gaussian Processes for Machine Learning_ (2006)

## Bayesian Hypothesis Testing for Practitioners

- Bayesian hypothesis testing provides an alternative to frequentist null
  hypothesis significance testing (NHST) that many practitioners find more
  intuitive and informative

- **Bayes factors**
  - The Bayes factor compares two competing models (hypotheses) by computing
    the ratio of their marginal likelihoods:
    $$
    BF_{01} = \frac{p(y | M_0)}{p(y | M_1)}
    $$
  - $BF_{01} > 1$ means the data supports $M_0$ over $M_1$
  - Interpretation scale (Jeffreys):

    | **Bayes Factor** | **Interpretation** |
    | :------- | :------- |
    | 1-3 | Anecdotal evidence |
    | 3-10 | Moderate evidence |
    | 10-30 | Strong evidence |
    | 30-100 | Very strong evidence |
    | >100 | Extreme evidence |

  - Bayes factors have a built-in Occam's Razor: models with more parameters
    spread their prior more thinly, so they are naturally penalized unless the
    extra complexity is justified by the data

- **Savage-Dickey density ratio**
  - A simplified method for computing Bayes factors when testing a point null
    hypothesis (e.g., $H_0: \theta = 0.5$)
  - Compares prior and posterior densities at the null value:
    if the posterior is much lower than the prior at $\theta_0$, the data
    provides strong evidence against $H_0$
  - Limitation: it is a point statistic and does not consider the entire
    posterior

- **Region of Practical Equivalence (ROPE)**
  - Instead of testing whether $\theta$ equals an exact value, define a region
    where values are practically equivalent
  - Example: for a coin bias, ROPE might be $\theta \in [0.45, 0.55]$ (close
    enough to fair)
  - Decision rule:
    - HPI entirely within ROPE: accept $H_0$ (no meaningful effect)
    - HPI entirely outside ROPE: reject $H_0$ (meaningful effect)
    - HPI overlaps ROPE: inconclusive, collect more data
  - The ROPE should be chosen **before** the analysis based on domain knowledge

- **Posterior predictive model comparison**
  - Compare models using posterior predictive checks (PPC): generate data from
    each model's posterior and compare to observed data
  - Use information criteria as quantitative summaries:
    - **WAIC** (Widely Applicable Information Criterion): Bayesian version of
      AIC using the full posterior
    - **LOO-CV** (Leave-One-Out Cross-Validation via PSIS): Estimates
      out-of-sample predictive accuracy from a single model fit
  - **Model averaging**: When multiple models explain the data, combine them
    using weights proportional to their predictive accuracy

- **Bayesian vs. frequentist p-values**
  - Frequentist p-value: probability of data as or more extreme, assuming the
    null is true. Does not incorporate parameter uncertainty
  - Bayesian p-value: probability that simulated data from the model is as or
    more extreme than observed data. Incorporates uncertainty through the
    posterior
  - A Bayesian p-value near 0.5 indicates good model fit; near 0 or 1
    indicates poor fit

**References**
- Harold Jeffreys, _Theory of Probability_ (1961)
- John K. Kruschke, "Bayesian Estimation Supersedes the t Test" (2013)
- Aki Vehtari, Andrew Gelman, and Jonah Gabry, "Practical Bayesian Model Evaluation Using Leave-One-Out Cross-Validation and WAIC" (2017)
- Osvaldo Martin, _Bayesian Analysis with Python_, 2nd Edition (2018), Chapter 5

## Aleatoric Vs. Epistemic Uncertainty

- Uncertainty is not monolithic. There are two fundamentally different kinds,
  and distinguishing them has important consequences for decision-making

- **Aleatoric uncertainty** (irreducible uncertainty)
  - Arises from inherent randomness in the system
  - Cannot be reduced by collecting more data
  - Examples:
    - The outcome of a fair coin toss
    - Measurement noise from a sensor
    - Quantum-level randomness
  - In a probabilistic model, captured by the **likelihood**
    $p(\tilde{y} | \theta)$

- **Epistemic uncertainty** (reducible uncertainty)
  - Arises from lack of knowledge about the system
  - Can be reduced by collecting more data or improving the model
  - Examples:
    - Uncertainty about a model's parameters when training data is limited
    - Uncertainty about which model is correct
    - Uncertainty in the value of a physical constant measured with finite
      precision
  - In a probabilistic model, captured by the **posterior** $p(\theta | y)$

- **Why the distinction matters for decisions**
  - If uncertainty is mostly **epistemic**, the right action is to gather more
    data before committing to a decision
  - If uncertainty is mostly **aleatoric**, no amount of data will eliminate it,
    and the decision must account for irreducible variability
  - A well-calibrated decision-maker allocates resources (data collection,
    experimentation) toward reducing epistemic uncertainty where it matters most

- **Posterior predictive distribution combines both sources**
  $$
  p(\tilde{y} | y) = \int p(\tilde{y} | \theta) \, p(\theta | y) \, d\theta
  $$
  - $p(\tilde{y} | \theta)$: aleatoric uncertainty (sampling variability)
  - $p(\theta | y)$: epistemic uncertainty (parameter uncertainty)
  - The total predictive uncertainty is always at least as large as the
    aleatoric uncertainty alone

- **In the Bayesian framework**, data has three sources of uncertainty:
  - **Ontological**: The system is intrinsically stochastic
  - **Technical**: Measurement precision is limited or noisy
  - **Epistemic**: Conceptual limitations in understanding

**References**
- Armen Der Kiureghian and Ove Ditlevsen, "Aleatory or Epistemic? Does It Matter?" (2009)
- Yarin Gal, "Uncertainty in Deep Learning" (PhD Thesis, 2016)
- Andrew Gelman et al., _Bayesian Data Analysis_, 3rd Edition (2013), Chapter 1

## Confidence Intervals and Prediction Intervals

- Quantifying uncertainty in estimates and predictions is critical for
  decision-making, but different types of intervals answer different questions

- **Frequentist confidence intervals**
  - A 95% confidence interval does **not** mean "there is a 95% probability
    the true value is in this interval"
  - Correct interpretation: "If we repeated the experiment many times, 95% of
    the constructed intervals would contain the true value"
  - Once computed, the interval either contains the true value or it does not;
    the 95% refers to the long-run procedure, not this particular interval

- **Bayesian credible intervals**
  - A 95% Bayesian credible interval means: "Given the observed data and our
    prior, there is a 95% probability that the true parameter lies within this
    interval"
  - This is the interpretation most people intuitively expect
  - **Highest Posterior Density (HPD)** interval: the shortest interval
    containing a specified probability mass (e.g., 94% in ArviZ by default)

- **Confidence intervals vs. credible intervals: an analogy**
  - **Confidence interval (frequentist)**: Imagine fishing in a lake. You throw
    a net. A 95% CI means "if I threw this net 100 times, about 95 nets would
    catch the fish." Once thrown, it either caught the fish or not
  - **Credible interval (Bayesian)**: Imagine a map showing where fish
    probably are, based on past observations. A 95% credible interval means
    "given my map, there's a 95% chance the fish is in this part of the lake"

- **Prediction intervals**
  - A prediction interval covers a future **observation**, not a parameter
  - It is always wider than a confidence or credible interval because it
    accounts for both parameter uncertainty and sampling variability
  - In Bayesian terms, the prediction interval comes from the **posterior
    predictive distribution** $p(\tilde{y} | y)$

- **Practical guidance**
  - Use **confidence/credible intervals** when you want to quantify
    uncertainty about a parameter (e.g., the mean treatment effect)
  - Use **prediction intervals** when you want to quantify uncertainty about
    a future observation (e.g., the next patient's outcome)
  - In Bayesian workflows, both come naturally from the posterior and posterior
    predictive distributions

**References**
- Larry Wasserman, _All of Statistics_ (2004), Chapter 6
- John K. Kruschke, _Doing Bayesian Data Analysis_, 2nd Edition (2015), Chapter 12
- Andrew Gelman et al., _Bayesian Data Analysis_, 3rd Edition (2013), Chapter 2

## TUTORIAL: PyMC (Bayesian Inference, Uncertainty Quantification, and Posterior-based Decisions)

## TUTORIAL: BoTorch (Bayesian Optimization for Sequential Decision Making)
