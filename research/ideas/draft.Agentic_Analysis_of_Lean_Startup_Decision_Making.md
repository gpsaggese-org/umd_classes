# Batch vs. Iterative Decision-Making in Startups: Agent-Based Simulation

## Status

- **Status**: draft
- **Complete Specs**: 40%
- **Assignee**: TBD

## Core Idea

- Classic "waterfall vs. agile" recast as startup strategy: collect-then-decide
  vs. plan-execute-learn-repeat
- Maps onto existing formal frameworks from decision theory, optimal stopping,
  and reinforcement learning, enabling direct simulation and comparison
- Key tension: upfront research reduces decision variance (Bayesian updating) but
  suffers staleness penalty if markets are non-stationary, while iteration keeps
  beliefs synced to moving targets but incurs switching costs and thrashing risk

## Formalization

### Batch Startup Model

- Agent spends `T_info` rounds gathering signals about world state `θ`
  (market demand, product-market fit, unit economics) with no market feedback
  loop or revenue
- After `T_info` rounds, commits to decision `d*` maximizing expected value given
  posterior belief: `P(θ | s_1, ..., s_T)`
- This is an **optimal stopping problem**: founder chooses `T_info` balancing
  value of information (marginal variance reduction) vs. cost of delay (burn
  rate, competitor entry, market drift)
- Decision quality is increasing and concave in `T_info` (diminishing returns):
  posterior variance shrinks as `1/T_info` (classic Bayesian updating)
- **Staleness risk**: if `θ_t` drifts over time (`θ_t = θ_{t-1} + η_t`,
  `η_t ~ N(0, σ_θ²)`), long collection phase optimizes for outdated state

### Iterative Startup Model

- **Sequential decision process** (multi-armed bandit or online RL): at each
  round `t`, take action `a_t` (ship feature, run experiment, test price),
  observe reward `r_t = f(a_t, θ_t) + ε_t`, update belief before next round
- Trades one-shot commitment for **sequence of reversible bets**, each generating
  real signal (revealed preference > surveys/forecasts, less noisy)
- **Thompson sampling / bandit logic**: exploit best-so-far while exploring
  enough to avoid premature convergence to locally-optimal-but-globally-wrong
  strategy
- Continuous feedback allows tracking **non-stationary θ_t**: smaller staleness
  penalty since beliefs refresh against current world
- **Switching cost** `c` (rebuild, re-onboard, context-switch, morale): too-
  frequent iteration prevents signal from materializing ("thrashing" regime,
  analogous to committee groupthink)

## Key Examples

- **Example 1 (Stable Market)**: established SaaS market with clear buyer
  personas and documented demand patterns
  - Batch approach: 3-month market research validates product direction, launch
    with high confidence
  - Iterative approach: rapid prototyping and user testing uncovers the same
    insights faster but incurs more pivot costs
  - Batch wins (information high-quality, market stable, switching costs harmful)

- **Example 2 (Volatile Market)**: emerging vertical AI applications where
  product-market fit is undefined
  - Batch approach: 6-month research still fails to predict demand; by launch,
    market has evolved past assumptions
  - Iterative approach: weekly customer interviews and feature experiments reveal
    real signals; pivots compound learning efficiently
  - Iteration wins (market moving faster than research, revealed preference > surveys)

- **Example 3 (Thrashing Failure)**: startup with high switching cost and noisy
  signals
  - Too-frequent pivots prevent any strategy from generating meaningful revenue
  - Moving monthly burns morale and reduces speed-to-signal
  - Both strategies fail, but batch suffers less (at least commits once)

## Questions

1. What is the phase transition between "batch works" and "iteration works"?
   Does it depend on drift rate, noise level, runway, or some combination?

2. Can we identify optimal switching thresholds that minimize thrashing while
   preserving adaptability? (e.g., "pivot if confidence drops below 30%")

3. Does the batch vs. iteration choice interact with team size, capital access,
   or founder risk tolerance in systematic ways?

4. If proved: does this framework predict which founders/VCs will favor different
   strategies, and can it explain observed failures (e.g., "pivot fatigue")?

## Research Topics

- **Optimal stopping theory**: reformulate `T_info` choice as optimal stopping with
  drift and regime-switching
- **Bandit literature**: Thompson sampling, regret bounds, and false-discovery
  rates under non-stationary arms
- **Empirical startup data**: correlate decision cadence (batch vs. iterative
  style) with time-to-product, runway survival, and post-launch success rates
- **Startup narratives**: qualitative study of decision-making stories from Y
  Combinator, TechCrunch, founder interviews (confirm theoretical predictions)

## Next Steps

- [ ] Look for related research (optimal stopping with drift, non-stationary
  bandits, startup case studies)
- [ ] Finalize the implementation plan and create detailed model pseudocode
- [ ] GP to review and approve the plan
- [ ] Hack a quick end-to-end prototype (1–2 days): Python simulation with
  batch and iterative agents, simple market drift, measure quality vs. runway
  consumed
- [ ] Break problem into phases (baseline model, drift + switching costs,
  empirical validation)
- [ ] Execute one step at a time

## Implementation Plan

- **Phase 1: Baseline Simulation**
  - Environment: true state `θ_t` on 1D or 2D landscape, optionally drifting
  - Batch agent: spends `T_info` steps observing `s_i = θ_t + ε_i`, then commits
    to one decision for remaining `T_total − T_info` steps
  - Iterative agent: at each step, takes action `a_t`, observes reward
    `r_t = f(a_t, θ_t) + ε_t`, updates via gradient descent or Thompson sampling
  - Metrics: final decision quality, time-to-viable-product, cumulative cash
    burn, runway survival probability, robustness to drift

- **Phase 2: Parameter Sweeps and Analysis**
  - Sweep `T_info` (batch research duration), drift rate `σ_θ`, switching cost
    `c`, noise level `σ_ε`, runway/burn rate
  - Plot decision quality vs. runway, identify crossover points
  - Summary metric: **decision quality per unit runway consumed** (unified
    comparison)

- **Phase 3: Qualitative Validation**
  - Collect startup case studies (Y Combinator, TechCrunch) annotated with
    decision cadence (batch vs. iterative)
  - Compare observed patterns (e.g., "thrashing failure") to simulation
    predictions

## References

- Wald, A., & Wolfowitz, J. (1948). _Optimum character of the sequential
  probability ratio test_. The Annals of Mathematical Statistics
- Thompson, W. R. (1933). _On the likelihood that one unknown probability
  exceeds another in the light of the evidence of two samples_
- Bergemann, D., & Välimäki, J. (2006). _Bandit problems_. Handbook of game
  theory
- Koopmans, T. C. (1960). _Activity analysis of production and allocation_
- Case studies: Y Combinator founders on decision-making (Paul Graham essays),
  TechCrunch startup postmortems
