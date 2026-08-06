# VC Dimension of Causal / Bayesian Networks

**Status:** draft | **Specs:** 10% | **Assignee:** —

## Core Idea

Causal structure provides inductive bias that can dramatically reduce sample
complexity. The VC dimension of a causal or Bayesian network depends not only
on the number of parameters but on the structural properties of the DAG:
number of nodes, maximum indegree, and the parametric family of conditional
distributions.

Understanding this complexity is essential for characterizing the sample
complexity of causal discovery and the generalization properties of
causally-structured models.

## Formalization

The VC dimension of a causal/Bayesian network depends on:
- **Number of nodes**: More nodes → larger hypothesis space
- **Maximum indegree**: Higher indegree → more complex conditional
  distributions
- **Parametric family of conditionals**: E.g., linear Gaussian vs. non-linear
  vs. non-parametric

## Key Examples

- A 10-node causal DAG with max indegree 3 and linear Gaussian conditionals
  has far lower VC dimension than a fully-connected 10-node network. This
  suggests causal structure provides inductive bias that improves
  generalization—but only if the assumed structure is correct.

## Provocative Questions

1. Does learning the wrong causal structure hurt generalization more than
   ignoring causality entirely and using pure correlation?
2. Can we define a "causal VC dimension" that captures not just the
   complexity of the model but the complexity of interventions it can
   represent?
3. If two causal graphs are Markov equivalent (indistinguishable from
   observational data), do they have the same VC dimension?
4. Is there a fundamental trade-off between causal interpretability and
   predictive accuracy?

## Research Topics

- Structural VC dimension of DAGs
- Sample complexity of causal discovery
- MDL penalties for structure learning
- Causal VC dimension for interventional distributions
- Bounds on generalization error for causal vs. purely correlational models

## References

- Derived from *Research_plan/paper.tex* (Section: Quasi-Stationary Learning /
  VC Dimension of Causal / Bayesian Networks)