We are interested in studying how discrete problems can be made differentiable
and then solved with gradient descent

// TODO(gp): Maybe we should split into multiple research ones, one per type of
// problem

# Approaches

There are several standard techniques, depending on what "discrete" means in context:

**Relaxation to continuous variables**
- Replace discrete choices (0/1, categorical) with continuous ones in [0,1] or a simplex, optimize, then round/threshold. Used in LP relaxations, continuous relaxations of combinatorial problems.
- **Softmax / Gumbel-Softmax**: for categorical or argmax decisions, replace the hard argmax with a temperature-controlled softmax. As temperature → 0 it approaches the discrete choice, but stays differentiable. Very common in neural architecture search, discrete latent variables in VAEs.

**Straight-Through Estimator (STE)**
- Do the discrete operation (e.g., rounding, thresholding, argmax) in the forward pass, but pretend the gradient of that operation is 1 (identity) in the backward pass. Crude but effective — widely used for quantized neural networks and binary neural nets.

**Reparameterization tricks**
- Move the randomness/discreteness outside the differentiable path. E.g., the Gumbel-Max trick rewrites sampling from a categorical distribution as argmax of continuous Gumbel-perturbed logits, which Gumbel-Softmax then relaxes further.

**Score function / REINFORCE estimator**
- Instead of differentiating through the discrete operation, use the log-derivative trick: ∇E[f(x)] = E[f(x)∇log p(x)]. This gives an unbiased gradient estimate without needing the function itself to be differentiable — common in reinforcement learning and discrete latent variable models. Usually high variance, so paired with variance-reduction (baselines, control variates).

**Convex/probabilistic relaxation of combinatorial structure**
- For problems like graph cuts, matching, or TSP, replace hard constraints with soft/probabilistic versions (e.g., doubly stochastic matrices via Sinkhorn instead of permutation matrices), then anneal toward discreteness.

**Smoothing the objective itself**
- If the objective is piecewise-constant or has discrete jumps (like accuracy or 0/1 loss), replace it with a smooth surrogate (cross-entropy instead of 0/1 loss, hinge loss, etc.) that's easier to optimize but correlates with the true objective.

# Drawbacks

Each of these fixes introduces its own headaches:

**Relaxation to continuous variables**
- The relaxed optimum can be far from the true discrete optimum — there's no guarantee rounding gives a good (or even feasible) solution.
- "Integrality gap" — for some problems (e.g. certain LP relaxations of NP-hard problems) this gap can be large.
- Rounding after the fact is itself a nontrivial, sometimes unstable step.

**Softmax / Gumbel-Softmax**
- Temperature is a fragile hyperparameter: too high → mushy, uninformative gradients; too low → gradients vanish and it behaves like a discrete function again (curse of "peaky" softmax).
- Annealing schedules need tuning and add training complexity.
- At intermediate temperatures, the forward pass is a "soft" object that doesn't match what you'll actually deploy (a hard discrete choice), creating a train/test mismatch.

**Straight-Through Estimator**
- Biased gradient estimator — there's no formal guarantee it points in a descent direction, it just tends to work empirically.
- Can cause instability or poor convergence, especially with many discrete layers stacked (bias compounds).
- Somewhat "hacky" theoretically; behavior is not well understood outside empirical validation.

**Reparameterization (Gumbel-Max/Softmax)**
- Only really clean for certain distributions (Gumbel for categorical); harder to extend to arbitrary discrete structures (e.g. combinatorial objects like trees, permutations).
- Same temperature/bias tradeoffs as above when relaxed.

**Score function / REINFORCE**
- Very high variance — gradient estimates can be noisy enough to make training slow or unstable.
- Needs variance reduction techniques (baselines, control variates, Rao-Blackwellization), which add complexity and their own tuning burden.
- Sample-inefficient — often needs many samples per update to get a usable signal.

**Sinkhorn / soft combinatorial relaxations (matchings, permutations)**
- Computationally expensive (iterative normalization) compared to a simple discrete assignment.
- Still needs annealing/rounding at the end, with similar gap issues as generic relaxation.
- Doesn't easily generalize to combinatorial structures beyond specific templates (e.g. permutations, assignments) — arbitrary discrete structures (like general graphs, trees, programs) don't have neat continuous relaxations.

**Surrogate/smoothed losses**
- The surrogate is not the actual objective — optimizing it well doesn't guarantee optimizing the true (discrete) objective well. Cross-entropy minimized ≠ accuracy maximized, in general.
- Choice of surrogate is somewhat arbitrary/heuristic; different surrogates can lead to different behavior.

**Cutting across all of them**
- Loss of interpretability/exactness: you're often optimizing a proxy problem, and success on the proxy doesn't formally guarantee success on the original discrete problem.
- Extra hyperparameters (temperature, variance-reduction terms, relaxation schedules) that need tuning and add fragility.
- No universal recipe — the "right" relaxation is often problem-specific, and picking wrong can silently degrade solution quality without an obvious sign that something is off.

# Research ideas

For each approach
- Find 5 problems where that are known to be solved with the given approach
- Create an example of a problem for each category and apply the transform
  approach to it
- Solve the problem as a discrete one and then solve it using the differentiable
  approach (using Python)
- Compare the solutions

The right choice depends on whether the discreteness is in the *variables*
(things like Sinkhorn, Gumbel-Softmax, relaxation) or in the *loss/objective*
(surrogate losses, STE)

