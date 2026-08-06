# Time as a Feature in Learning Theory

**Status:** draft | **Specs:** 10% | **Assignee:** —

## Core Idea

Modern learning theory largely treats time as an external index over data. Yet
in real systems, time is not merely a coordinate—it is generative, causal, and
structural. Markets evolve, machines degrade, energy systems adapt, and agents
respond to predictions.

The core question: *Is time truly special, or have we artificially separated it
from the feature space due to historical modeling choices?* Can we unify time
and features into a single formal structure, removing the boundary between
static learning and dynamical systems?

## Formalization

Define a time-indexed hypothesis class:

\[
\mathcal{H}_{t} = \{h_{t}(x) : t \in \mathbb{T}\}
\]

Assume bounded drift between consecutive hypotheses:

\[
\|h_{t+1} - h_{t}\| \le \epsilon
\]

Classical PAC bound:

\[
n \gtrsim \frac{VC(\mathcal{H}) + \log(1/\delta)}{\epsilon^{2}}
\]

Time-aware extension:

\[
n \gtrsim \frac{VC(\mathcal{H}) + D_{T} + \log(1/\delta)}{\epsilon^{2}}
\]

where \(D_{T}\) measures cumulative drift:

\[
D_{T} = \sum_{t=1}^{T-1} \|h_{t+1} - h_{t}\|
\]

### Temporal VC Dimension (Complexity View)

- Merged from `draft.Temporal_VC_Dimension.md`. Complementary to the drift-bound
  view above: instead of bounding sample complexity via cumulative drift
  \(D_{T}\), bound it via the complexity of the *union* of hypothesis classes
  visited over time:

\[
VC_{T} = VC\left( \bigcup_{t=1}^{T} \mathcal{H}_{t} \right)
\]

- If \(h_{t}\) can drift arbitrarily, \(VC_{T}\) can grow unboundedly with
  \(T\), potentially making long-term learning impossible — the complexity
  analogue of the drift bound blowing up as \(D_{T} \to \infty\)

## Key Examples

- **Stock market prediction**: \(h_{t}(x)\) predicts returns from features
  where the relationship changes due to market regimes (bull/bear markets,
  crisis periods)
- **Adaptive recommendation systems**: User preferences drift over time,
  requiring hypothesis updates as tastes evolve
- **Climate modeling**: Physical relationships shift due to anthropogenic
  forcing, violating stationarity assumptions
- **Medical diagnosis**: Disease patterns and diagnostic criteria evolve with
  new treatments and emerging pathogens
- **NLP**: Language models trained on pre-2020 data fail to understand
  pandemic-related terminology or evolving slang
- **Fraud detection**: Fraudsters continuously adapt strategies to evade
  detection, creating adversarial drift where \(P(y|x,t)\) is actively
  manipulated
- **Energy demand forecasting**: The relationship between temperature and
  electricity usage changes as solar panel adoption and electric vehicles
  increase

### Complexity Examples (Temporal VC Dimension)

- **Linear classifiers with drift**: For \(h_{t}(x) = \text{sign}(w_{t}^{\top}
  x)\) where \(w_{t}\) drifts smoothly, at any fixed \(t\),
  \(VC(\mathcal{H}) = d+1\). But over \(T\) timesteps with unbounded drift,
  \(VC_{T}\) can grow without bound as the union captures increasingly complex
  decision boundaries
- **Neural networks with time-varying weights**: If weights can change
  arbitrarily, \(VC_{T}\) may equal the VC dimension of the universal function
  approximator class, even if each \(h_{t}\) individually has bounded
  complexity
- **Seasonal models**: A retailer uses \(h_{\text{holiday}}\) during December
  and \(h_{\text{regular}}\) otherwise. Then \(VC_{T}\) is at least
  \(\max(VC(h_{\text{holiday}}), VC(h_{\text{regular}}))\) but could be larger
  if the union creates new decision boundaries

## Provocative Questions

1. Can a model that constantly adapts to time still learn anything
   generalizable? If \(h_{t}\) changes at every timestep, is this learning or
   mere tracking?
2. Is forgetting necessary for generalization in non-stationary environments?
   Classical theory rewards more data, but in drifting environments, old data
   may hurt performance.
3. Does the notion of "ground truth" even make sense in time-varying systems?
   If \(y = f_{t}(x)\) where \(f_{t}\) itself evolves, what are we actually
   trying to learn—the current \(f_{t}\) or the meta-function that generates
   the sequence \(\{f_{t}\}\)?
4. Can we have PAC-style guarantees without stationarity? Or does
   non-stationarity fundamentally break the connection between empirical and
   true risk?
5. Should we penalize model complexity or model *stability*? A complex but
   stable model might generalize better over time than a simple but volatile
   one.
6. Is the distinction between "learning from data" and "tracking a signal"
   just a matter of timescale? At what rate of change does learning become
   impossible?
7. _(from Temporal VC Dimension)_ Is complexity additive over time, or does
   the union bound \(VC_{T}\) capture interaction effects that a simple sum
   would miss?
8. _(from Temporal VC Dimension)_ If \(VC_{T} \to \infty\) as \(T \to \infty\),
   does that mean all long-term predictions are impossible, or just that the
   *union* bound is too loose to be useful?
9. _(from Temporal VC Dimension)_ Can two models have identical
   \(VC(\mathcal{H})\) but vastly different \(VC_{T}\) due to different drift
   patterns — i.e., does drift *pattern* (not just magnitude) matter?

## Research Topics

- VC dimension of time-indexed hypothesis classes, in particular the growth
  rate of \(VC_{T}\) as a function of drift smoothness, and when it grows
  sublinearly (learnable) vs. linearly (unlearnable)
- PAC-style bounds parameterized by \(VC_{T}\) vs. by cumulative drift
  \(D_{T}\) — are these two views of the same bound, or genuinely different?
- Time-dependent Rademacher complexity
- Stability under evolving distributions
- Meta-learning for non-stationary tasks

## References

- Derived from *Research_plan/paper.tex* (Section: Time as a Feature of
  Machine Learning; Section: Quasi-Stationary Learning / Temporal VC
  Dimension)