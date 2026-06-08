# Approximate Inference in Bayesian Networks

- This notebook teaches how to estimate posteriors $P(X \mid \mathbf{e})$ by
  sampling, when exact inference is too expensive or impossible
- Concepts are built on the canonical AIMA sprinkler network with variables
  $Cloudy \to Sprinkler$, $Cloudy \to Rain$, $Sprinkler \to WetGrass$,
  $Rain \to WetGrass$, and the running query $P(Rain \mid Sprinkler{=}T)$
- The pedagogical arc is:
  - Turn uniform randomness into samples (inverse transform) -> sample a whole
    network (prior sampling) -> watch estimates converge ($1/\sqrt{N}$) ->
    condition on evidence by rejection -> rescue rare evidence with importance
    weights -> walk the state space with MCMC (mixing, Gibbs,
    Metropolis-Hastings)
- Focus is on hands-on discovery: students turn knobs, watch sample clouds
  form, and see why each method fixes the weakness of the one before it
- This notebook is the approximate counterpart to
  `notebook_outline.exact_inference.md`: the exact posteriors computed there
  with `pgmpy` are reused throughout as the ground-truth reference that every
  estimate is compared against

# Part 1: From Randomness to Samples

## Cell 1.1: Turning Uniform Randomness into Any Distribution

- **Purpose**: Establish the atom of every method in this notebook, namely that
  a single stream of uniform random numbers $r \in [0,1]$ can be reshaped into
  samples from any distribution via the inverse CDF
- **Display**:
  - A 1x4 panel layout:
    - Panel 1: the target distribution, switchable between a discrete bar chart
      (e.g., a biased die) and a continuous density (e.g., exponential with rate
      $\lambda$)
    - Panel 2: the CDF $F(x) = \Pr(X \le x)$ as a staircase (discrete) or smooth
      curve (continuous), with a horizontal line at a sampled $r$ and a dropped
      vertical line showing the returned $x = F^{-1}(r)$
    - Panel 3: a histogram of $N$ generated samples (solid, dark) overlaid on
      the target density (light, dotted), showing the match improve as $N$ grows
    - Panel 4: comments panel
  - The inverse-transform construction is animated: each new $r$ on the y-axis
    maps through the CDF to an $x$ on the x-axis that lands in the histogram
- **Interactive widget**:
  - Dropdown for distribution type: "biased die (discrete)" vs "exponential
    (continuous)"
  - Slider for $\lambda$ (rate of the exponential), linear scale
  - Log-scale slider for $N$ (number of samples drawn)
  - Slider for `seed` (placed last)
  - Description: "Pick a target, then watch a uniform $r$ get mapped through the
    CDF into a sample. Increase $N$ to see the histogram fill in the target."
- **Key insights**:
  - Any sampler in this notebook ultimately consumes uniform random numbers;
    the CDF is the universal adapter
  - For discrete targets you find the smallest outcome where $F(x) > r$; for
    continuous targets you invert, e.g.,
    $x = -\frac{1}{\lambda}\ln(1-r)$ for the exponential
  - When $F^{-1}$ has no closed form you fall back to numerical inversion, but
    the idea is unchanged
- **Comment box**: "One trick underlies everything: stretch a flat $[0,1]$
  number through the CDF and it comes out distributed like the target. Sampling
  a network is just doing this many times in the right order."
- **Implementation**: `numpy` uniform draws, closed-form inverse CDF for the
  exponential, cumulative-probability table lookup for the discrete case,
  `seaborn` histograms, `matplotlib` for the CDF staircase,
  `htutori.build_widget_control` and `htutori.build_log_widget_control` for the
  sliders, `htutori.add_fitted_text_box()` for panel 4

## Cell 1.2: Prior Sampling from the Sprinkler Network

- **Purpose**: Scale the single-variable trick up to a whole Bayesian network by
  sampling variables in topological order, generating full events with no
  evidence
- **Display**:
  - A 1x4 panel layout:
    - Panel 1: the sprinkler DAG drawn with `plot_causal_dag()`, nodes lighting
      up one at a time in topological order ($Cloudy$, then $Sprinkler$ and
      $Rain$, then $WetGrass$) as the current sample is built
    - Panel 2: the CPT of the variable currently being sampled, with the row
      selected by the already-sampled parents highlighted
    - Panel 3: a running tally of generated full events
      $(C, S, R, W)$ as a `pandas` table plus a bar chart of the estimated joint
      frequencies vs the `pgmpy` exact joint (light, dotted)
    - Panel 4: comments panel
  - Each completed sample appends one row; the bar chart redraws as counts
    accumulate
- **Interactive widget**:
  - Log-scale slider for $N$ (number of full events to generate)
  - Dropdown to highlight one variable whose marginal $\Pr(\cdot)$ estimate is
    tracked against its exact value
  - Slider for `seed` (placed last)
  - Description: "Generate $N$ complete worlds from the network. Watch each
    variable get sampled only after its parents, and the estimated frequencies
    approach the true joint."
- **Key insights**:
  - Topological order guarantees every parent has a value before its child is
    sampled, so each draw uses a fully specified CPT row
  - Prior sampling realizes the network's factorization
    $f_{PS}(x_1,\dots,x_n) = \prod_i \Pr(x_i \mid parents(X_i))$
  - With no evidence, the relative frequency of any event approximates its joint
    probability $\Pr(x_1,\dots,x_n)$
- **Comment box**: "Prior sampling = inverse-transform sampling, once per node,
  parents first. The fraction of samples equal to an event is an estimate of
  that event's joint probability."
- **Implementation**: `pgmpy.sampling.BayesianModelSampling.forward_sample` (or a
  hand-rolled topological sampler for transparency), `networkx.topological_sort`,
  `plot_causal_dag()` from `helpers_root/helpers/hgraphviz.py`, `pandas`,
  `seaborn`, `htutori` widget helpers

## Cell 1.3: Consistency and the $1/\sqrt{N}$ Convergence Rate

- **Purpose**: Make convergence tangible, showing that prior-sampling estimates
  are consistent and that error shrinks like $1/\sqrt{N}$, which sets
  expectations for every sampler that follows
- **Display**:
  - A 1x4 panel layout:
    - Panel 1: a single estimate's trajectory, the running estimate
      $\hat{P} = N_{PS}/N$ for a chosen event plotted against $N$, converging to
      the exact `pgmpy` value drawn as a flat dotted reference line
    - Panel 2: several independent chains of estimates (different seeds) as a
      fan, narrowing as $N$ grows to show variance shrinking
    - Panel 3: absolute error $|\hat{P} - P|$ vs $N$ on log-log axes, with a
      reference slope of $-1/2$ overlaid to confirm the $1/\sqrt{N}$ rate
    - Panel 4: comments panel
  - Empirical curves are solid and dark; the exact value and the theoretical
    slope are light and dotted
- **Interactive widget**:
  - Log-scale slider for the maximum $N$
  - Slider for the number of independent repetitions shown in the fan, linear
    scale
  - Dropdown to choose which event/marginal is being estimated
  - Slider for `seed` (placed last)
  - Description: "Watch one estimate settle toward the truth, then watch many of
    them. Error drops, but only as $1/\sqrt{N}$: ten times the accuracy costs a
    hundred times the samples."
- **Key insights**:
  - Estimates are consistent:
    $\lim_{N\to\infty} N_{PS}(x)/N = \Pr(x)$
  - The error decreases as $1/\sqrt{N}$, so accuracy is expensive: a slope of
    $-1/2$ on log-log axes is the signature of Monte Carlo
  - More samples always help, but with diminishing returns; this motivates
    smarter samplers rather than just more samples
- **Comment box**: "Sampling is consistent but slow to sharpen. The $1/\sqrt{N}$
  law is unavoidable for plain Monte Carlo, which is why the rest of the
  notebook focuses on using each sample better."
- **Implementation**: repeated calls to the Cell 1.2 sampler with different
  seeds, `pgmpy` exact value as reference, `seaborn` line plots, `numpy` for
  log-log error fitting, `htutori` widget helpers and
  `htutori.add_fitted_text_box()`

# Part 2: Conditioning on Evidence

## Cell 2.1: Rejection Sampling

- **Purpose**: Introduce the simplest way to condition on evidence, namely
  generate prior samples and throw away those that disagree with the evidence,
  and expose its central weakness
- **Display**:
  - A 1x4 panel layout:
    - Panel 1: a stream of generated samples drawn as dots colored by whether
      they match the evidence $Sprinkler{=}T$ (kept) or not (rejected and faded)
    - Panel 2: a funnel/counter showing total generated, number rejected, and
      number retained, restating the worked example
      ($73$ rejected, $27$ kept, of which $8$ have $Rain$)
    - Panel 3: bar chart of the estimated posterior
      $P(Rain \mid Sprinkler{=}T) \approx 8/27$ against the `pgmpy` exact
      posterior (light, dotted)
    - Panel 4: comments panel
  - Kept samples are solid and dark; rejected samples are light and translucent
- **Interactive widget**:
  - Log-scale slider for $N$ (total prior samples generated)
  - Dropdown for the query variable $X$
  - Checkboxes plus True/False dropdowns to set the evidence $\mathbf{e}$
  - Slider for `seed` (placed last)
  - Description: "Add evidence and watch how many samples survive. Rare evidence
    means most of the work is thrown away."
- **Key insights**:
  - Rejection sampling is consistent: kept samples are exactly distributed as
    $P(X \mid \mathbf{e})$
  - The retained fraction equals $\Pr(\mathbf{e})$, so rare evidence wastes most
    samples
  - The effective sample size, not $N$, controls accuracy
- **Comment box**: "Correct but wasteful. Rejection sampling keeps only the
  samples that already agree with the evidence, so the rarer the evidence, the
  more samples you burn to learn anything."
- **Implementation**:
  `pgmpy.sampling.BayesianModelSampling.rejection_sample`, the Cell 1.2 prior
  sampler with a filtering step for the teaching view, `seaborn` for the dot
  cloud and bars, `pgmpy` exact reference, `htutori` widget helpers

## Cell 2.2: Importance Sampling and Likelihood Weighting

- **Purpose**: Fix rejection sampling's waste by keeping every sample and
  correcting the bias with importance weights, so no sample is discarded
- **Display**:
  - A 1x4 panel layout:
    - Panel 1: samples drawn from the easier proposal $Q(X)$ (evidence clamped),
      each dot sized by its importance weight $w = \Pr(X)/Q(X)$
    - Panel 2: the weight distribution as a histogram, flagging weight collapse
      when a few samples dominate
    - Panel 3: bar chart of the weighted estimate
      $E[f(X)] \approx \frac{1}{N}\sum_i w_i f(X_i)$ for
      $P(Rain \mid Sprinkler{=}T)$ against the `pgmpy` exact posterior (light,
      dotted), with rejection sampling's estimate shown for comparison
    - Panel 4: comments panel
  - Larger weights are darker/larger dots; the exact reference is light and
    dotted
- **Interactive widget**:
  - Log-scale slider for $N$ (number of weighted samples)
  - Dropdown for the query variable $X$
  - Checkboxes plus True/False dropdowns to set the evidence $\mathbf{e}$
  - Slider for `seed` (placed last)
  - Description: "Every sample is kept and reweighted. Compare the effective
    sample size to rejection sampling at the same $N$, especially when the
    evidence is rare."
- **Key insights**:
  - Drawing from an easier distribution $Q$ and weighting by $w=\Pr(X)/Q(X)$
    keeps all samples while staying unbiased
  - Likelihood weighting (clamp evidence, weight by the evidence CPTs) is the
    Bayesian-network instance of this idea
  - When weights are very uneven a few samples dominate (weight collapse),
    shrinking the effective sample size despite a large $N$
- **Comment box**: "Reweight instead of reject. Importance sampling spends every
  sample, focusing effort where the evidence lives, but only helps if the
  weights stay reasonably balanced."
- **Implementation**:
  `pgmpy.sampling.BayesianModelSampling.likelihood_weighted_sample`, explicit
  weight computation for the teaching view, `seaborn` histograms and bars,
  `pgmpy` exact reference, `htutori` widget helpers and
  `htutori.add_fitted_text_box()`

# Part 3: Markov Chain Monte Carlo

## Cell 3.1: Markov Chains and the Stationary Distribution

- **Purpose**: Introduce the core MCMC idea, that a random walk over states can
  be designed so its long-run distribution equals the posterior, instead of
  drawing each sample independently
- **Display**:
  - A 1x4 panel layout:
    - Panel 1: a small state-transition diagram (a handful of network
      configurations as nodes, transition probabilities as labeled edges) drawn
      with `networkx`, with the current state highlighted as the walk steps
    - Panel 2: the distribution over states $\pi_t(\mathbf{x})$ as a bar chart
      that updates each step, visibly settling toward a fixed shape
    - Panel 3: total-variation distance between $\pi_t$ and the stationary
      distribution vs step $t$, decaying toward zero
    - Panel 4: comments panel
  - The stationary target is drawn as light dotted bars behind the evolving
    solid bars in panel 2
- **Interactive widget**:
  - Slider for the number of steps $t$, linear scale
  - Dropdown for the initial state (to show the limit is independent of where
    the walk starts)
  - Slider for `seed` (placed last)
  - Description: "Step the chain and watch the distribution over states converge
    to a fixed shape, no matter where it started."
- **Key insights**:
  - A Markov chain is a memoryless walk: the next state depends only on the
    current one via $\Pr(\mathbf{x}\to\mathbf{x}')$
  - Under ergodicity (every state reachable) and aperiodicity (no trapping
    cycles), $\pi_t$ converges to a unique stationary distribution
  - MCMC is the art of building a chain whose stationary distribution is exactly
    the posterior $P(\text{non-evidence} \mid \mathbf{e})$
- **Comment box**: "The magic link: design the walk so that hanging around in
  proportion to the posterior is its natural equilibrium. Then just walk and
  count where you land."
- **Implementation**: `networkx` for the transition diagram, `numpy` matrix
  powers for $\pi_t$, `seaborn` bar charts, `matplotlib` for the convergence
  curve, `htutori` widget helpers

## Cell 3.2: Mixing and Burn-in

- **Purpose**: Show that a correct stationary distribution is not enough,
  because how fast the chain explores (mixing) determines whether finite-sample
  estimates are trustworthy
- **Display**:
  - A 1x4 panel layout:
    - Panel 1: trace plot of the sampled value over iterations for a bimodal
      target, contrasting a well-mixed chain (jumps between modes) and a
      poorly-mixed one (stuck in one mode)
    - Panel 2: the running histogram of collected samples vs the true bimodal
      posterior (light, dotted), showing the stuck chain misses a mode
    - Panel 3: autocorrelation vs lag, high and slowly decaying for poor mixing,
      quickly vanishing for good mixing, with a shaded burn-in region marked on
      the trace
    - Panel 4: comments panel
- **Interactive widget**:
  - Slider for proposal/step size controlling mixing quality, linear scale
  - Slider for burn-in length (number of initial samples discarded), linear
    scale
  - Log-scale slider for total iterations
  - Slider for `seed` (placed last)
  - Description: "Tune the step size to move between poor and good mixing, and
    set the burn-in to discard the chain's wandering start."
- **Key insights**:
  - Good mixing means moving between high-probability regions often with low
    correlation between successive samples; poor mixing gets stuck in one mode
  - Early samples reflect the arbitrary starting point and are discarded as
    burn-in before estimates are formed
  - Poor mixing produces biased, high-variance estimates even though the
    stationary distribution is correct in principle
- **Comment box**: "Right target, wrong speed. A chain can be provably correct in
  the limit yet useless in practice if it explores slowly. Watch the trace and
  the autocorrelation, not just the final histogram."
- **Implementation**: a small Metropolis sampler on a bimodal distribution for
  the trace, `seaborn` for histograms, `statsmodels`/`numpy` autocorrelation,
  `matplotlib` shaded burn-in region, `htutori` widget helpers and
  `htutori.add_fitted_text_box()`

## Cell 3.3: Gibbs Sampling and the Markov Blanket

- **Purpose**: Specialize MCMC to Bayesian networks with Gibbs sampling, which
  resamples one variable at a time from its Markov blanket, the simplest MCMC to
  implement on any network
- **Display**:
  - A 1x4 panel layout:
    - Panel 1: the sprinkler DAG with evidence nodes ($Sprinkler{=}T$,
      $WetGrass{=}T$) clamped/shaded, the variable currently being resampled
      highlighted, and its Markov blanket (parents, children, co-parents)
      outlined
    - Panel 2: the full-conditional $P(X_i \mid \text{MB}(X_i))$ being sampled
      from at this step, shown as a small bar chart
    - Panel 3: running estimate of $P(Rain \mid Sprinkler{=}T)$ (and
      $P(Cloudy \mid \dots)$) as bars vs the `pgmpy` exact posterior (light,
      dotted), updating as the sweep proceeds
    - Panel 4: comments panel
  - Evidence nodes are visually frozen; non-evidence nodes update in sequence
- **Interactive widget**:
  - Log-scale slider for the number of Gibbs sweeps
  - Slider for burn-in, linear scale
  - Dropdown for the sweep order over non-evidence variables
  - Checkboxes plus True/False dropdowns to set the evidence
  - Slider for `seed` (placed last)
  - Description: "Hold the evidence fixed and resample each hidden variable from
    its Markov blanket. Watch the estimate approach the exact posterior."
- **Key insights**:
  - Gibbs sampling only ever needs the local conditional
    $P(X_i \mid \text{MB}(X_i))$, where the Markov blanket is parents, children,
    and children's other parents
  - Evidence variables stay clamped, so every sample is automatically consistent
    with the evidence (no rejection, unlike Cell 2.1)
  - It is simple and scales to large graphs via local updates, but mixes slowly
    when variables are strongly correlated
- **Comment box**: "Gibbs sampling is MCMC made local: never touch the whole
  network at once, just resample one variable from its Markov blanket. Easy to
  code, but watch out for slow mixing under strong correlations."
- **Implementation**: `pgmpy.sampling.GibbsSampling`, the network's Markov
  blanket via `pgmpy` model queries, `plot_causal_dag()` with blanket
  highlighting, `seaborn` bars, `pgmpy` exact reference, `htutori` widget
  helpers and `htutori.add_fitted_text_box()`

## Cell 3.4: Metropolis-Hastings and Accept/Reject Moves

- **Purpose**: Generalize beyond Gibbs to Metropolis-Hastings, where an
  arbitrary proposal is corrected by an acceptance probability, unifying the
  ideas of proposing, accepting, and exploring
- **Display**:
  - A 1x4 panel layout:
    - Panel 1: the current state and a proposed state $\mathbf{x}'$ side by side,
      annotated with the acceptance probability
      $A(\mathbf{x},\mathbf{x}') = \min\!\big(1, \frac{\pi(\mathbf{x}')q(\mathbf{x}\mid\mathbf{x}')}{\pi(\mathbf{x})q(\mathbf{x}'\mid\mathbf{x})}\big)$
      and a coin-flip outcome (accept moves, reject stays)
    - Panel 2: the trace of accepted states and a running acceptance-rate
      readout, illustrating the exploration/exploitation balance
    - Panel 3: running estimate of $P(Rain \mid Sprinkler{=}T)$ as bars vs the
      `pgmpy` exact posterior (light, dotted)
    - Panel 4: comments panel
- **Interactive widget**:
  - Slider for the proposal mix (e.g., probability of a Gibbs-style local move
    vs a broader jump), linear scale
  - Log-scale slider for the number of iterations
  - Slider for burn-in, linear scale
  - Slider for `seed` (placed last)
  - Description: "Propose a move, then accept or reject it by the Hastings ratio.
    Tune the proposal and watch the acceptance rate and convergence trade off."
- **Key insights**:
  - Metropolis-Hastings accepts uphill moves and sometimes accepts downhill ones,
    which is what lets the chain escape local modes
  - The acceptance ratio $A(\mathbf{x},\mathbf{x}')$ guarantees the posterior is
    the stationary distribution for any valid proposal $q$
  - Gibbs sampling is a special case where every proposal is accepted; a good
    proposal balances acceptance rate against step size
- **Comment box**: "Propose anything, then correct with the Hastings ratio.
  Flexibility is the prize and the cost: any proposal is valid, but a bad one
  mixes slowly. Gibbs is just the case where you always accept."
- **Implementation**: a hand-rolled Metropolis-Hastings sampler over the network
  states for transparency, `seaborn` trace and bars, `pgmpy` exact reference,
  `htutori` widget helpers and `htutori.add_fitted_text_box()`
