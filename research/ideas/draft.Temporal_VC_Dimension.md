# Temporal VC Dimension

**Status:** draft | **Specs:** 10% | **Assignee:** —

## Core Idea

When the data-generating process evolves over time, the classical VC dimension—
which assumes a fixed hypothesis class—is insufficient. We need a *temporal VC
dimension* that captures the complexity of a sequence of hypothesis classes,
especially when drift allows the hypothesis to change over time.

## Formalization

Define the temporal VC dimension as the VC dimension of the union over time:

\[
VC_{T} = VC\left( \bigcup_{t=1}^{T} \mathcal{H}_{t} \right)
\]

If \(h_{t}\) can drift arbitrarily, \(VC_{T}\) can grow unboundedly with \(T\),
potentially making long-term learning impossible.

## Key Examples

- **Linear classifiers with drift**: For \(h_{t}(x) = \text{sign}(w_{t}^{\top}
  x)\) where \(w_{t}\) drifts smoothly, at any fixed \(t\),
  \(VC(\mathcal{H}) = d+1\). But over \(T\) timesteps with unbounded drift,
  \(VC_{T}\) can grow without bound as the union captures increasingly complex
  decision boundaries.
- **Neural networks with time-varying weights**: If weights can change
  arbitrarily, \(VC_{T}\) may equal the VC dimension of the universal function
  approximator class, even if each \(h_{t}\) individually has bounded
  complexity.
- **Seasonal models**: A retailer uses \(h_{\text{holiday}}\) during December
  and \(h_{\text{regular}}\) otherwise. Then \(VC_{T}\) is at least
  \(\max(VC(h_{\text{holiday}}), VC(h_{\text{regular}}))\) but could be larger
  if the union creates new decision boundaries.

## Questions

1. Is complexity additive over time?
2. If \(VC_{T} \to \infty\) as \(T \to \infty\), does this mean all long-term
   predictions are impossible?
3. Can two models have identical \(VC(\mathcal{H})\) but vastly different
   \(VC_{T}\) due to different drift patterns?
4. Does smooth drift (small \(\|h_{t+1} - h_{t}\|\)) lead to sublinear growth
   in \(VC_{T}\), or is any non-zero drift enough to cause unbounded
   complexity?
5. If we observe concept drift but don't model it, does the effective
   \(VC_{T}\) perceived by a stationary learner explode?

## Research Topics

- Characterize the growth rate of \(VC_{T}\) as a function of drift
  smoothness
- Develop PAC-style bounds parameterized by \(VC_{T}\) rather than
  \(VC(\mathcal{H})\)
- Understand when \(VC_{T}\) grows sublinearly (learnable) vs. linearly
  (unlearnable)

## References

- Derived from *Research_plan/paper.tex* (Section: Quasi-Stationary Learning /
  Temporal VC Dimension)