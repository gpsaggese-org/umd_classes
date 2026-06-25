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

## Research Topics

- VC dimension of time-indexed hypothesis classes
- Time-dependent Rademacher complexity
- Stability under evolving distributions
- Meta-learning for non-stationary tasks

## References

- Derived from *Research_plan/paper.tex* (Section: Time as a Feature of
  Machine Learning)