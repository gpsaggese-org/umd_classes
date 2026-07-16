# Robust Reasoning Under Distribution Shift

## Status
**Status:** draft  
**Complete Specs:** 20%  
**Assignee:** —

# Core Idea [REQUIRED]
Current LLMs exhibit brittle reasoning that fails under superficial
perturbations logically equivalent to the original task. On R-GSM (reordered
grade-school math problems), accuracy drops >30% despite the math being
identical, only with premises in a different order (Lesson 16.4). This
brittleness indicates that models perform pattern-matching on surface structure,
not robust logical reasoning. Agents in deployment face distribution shift
constantly: new websites with different layouts, codebases with different
conventions, API responses with rephrased field names. A reasoning system that
cannot generalize to equivalent problem formulations is fundamentally
unreliable

**Hypothesis**: We can train reasoning models to be invariant to distribution
shifts by explicitly teaching invariance during training. Rather than hoping
scaling and in-context learning will solve this, we can use adversarial
perturbation and invariance-aware verification to enforce robustness to
irrelevant variations

## Formalization [OPTIONAL]
Let $\mathcal{T}$ be a task and $\mathcal{P}(x)$ be a set of perturbations of
input $x$ (e.g., premise reordering, synonym replacement, numeric value
changes). A model $\pi$ is **logically robust** if:

$$
\Pr[\pi(x') = \text{correct} \mid x' \in \mathcal{P}(x), \pi(x) = \text{correct}] \approx 1
$$

Currently, LLMs violate this. Standard supervised fine-tuning minimizes:

$$
\mathcal{L}_{\text{SFT}} = -\log \pi(y \mid x)
$$

**Proposed loss with invariance**: augment with adversarial perturbations and
consistency regularization:

$$
\mathcal{L}_{\text{robust}} = -\log \pi(y \mid x) + \lambda \sum_{x' \in \mathcal{P}(x)} \text{KL}(\pi(y \mid x) \| \pi(y \mid x'))
$$

This penalizes the model if its confidence in the correct answer drops when the
input is perturbed. Alternatively, during RL training with verification, reward
only trajectories that generalize to perturbations:

$$
r_{\text{robust}}(\tau) = \begin{cases}
1 & \text{if task succeeds on } x \text{ and all } x' \in \mathcal{P}(x) \\
0 & \text{otherwise}
\end{cases}
$$

## Key Examples [REQUIRED]
- **R-GSM brittleness**: "If John has 5 apples and Mary has 3, how many do they
  have together?" vs. "Mary has 3 apples. How many do they have together? John
  has 5." Both are identical math, yet LLMs solve the second less reliably
  Training with premise-reordered examples teaches invariance

- **Code refactoring**: An agent trained to fix bugs in a specific codebase
  style (Pythonic, with type hints) fails when given the same logical bug in a
  different style (untyped, more imperative). Adversarial perturbation includes
  renaming variables, restructuring conditionals, changing loop styles

- **Web automation across domains**: An agent trained to log into Gmail fails on
  Outlook, even though both are email login flows. Invariance to UI layout,
  button naming, and field order is critical. Training on diverse logins teaches
  domain-agnostic patterns

- **Edge case**: some perturbations are not semantically equivalent (e.g.,
  "multiply by 2" vs. "divide by 0.5" are mathematically equivalent but not
  perceptually). The perturbation set $\mathcal{P}$ must be carefully scoped to
  irrelevant changes only

## Questions [OPTIONAL]
1. **Scope of perturbations**: How do we define the set $\mathcal{P}(x)$ of
   valid perturbations for a task? For math, premise order is clearly
   irrelevant; for code, variable names are, but loop structure may matter. How
   do we automatically infer this?

2. **Computational cost**: Enforcing invariance to all perturbations is
   expensive. Can we sample a small subset of $\mathcal{P}$ during training and
   still achieve robustness? What sampling strategy is optimal?

3. **Generalization bounds**: If a model is invariant to a known set of
   perturbations, does it generalize to unknown perturbations in the same class?
   Can we use this to prove robustness?

4. **Trade-off with performance**: Does forcing invariance hurt performance on
   in-distribution tasks? Is there a Pareto frontier between robustness and
   accuracy?

## Research Topics [OPTIONAL]
- **Perturbation generation**: Automatically synthesize valid perturbations for
  a task class (math, code, dialogue). Use templates or rule-based
  transformations
- **Robustness metrics**: Develop benchmarks like R-GSM for other domains
  (R-HumanEval for code, R-WebArena for web agents). Measure both individual and
  compositional robustness
- **Meta-learning for perturbations**: Train a model to learn which
  perturbations are task-irrelevant, rather than hand-specifying them
- **Certified robustness**: Use formal verification techniques (e.g., abstract
  interpretation) to prove a model is robust to a class of perturbations

## References [OPTIONAL]
- Chen, L., Zaharia, M., & Zou, J. (2024). "Premise Order Matters in Reasoning
  with Large Language Models." arXiv:2402.08939. [Lesson 16.4 source]
- Wei, J., Wang, X., & Schuurmans, D. (2022). "Chain-of-Thought Prompting
  Elicits Reasoning in Large Language Models." arXiv:2201.11903. [Implicit
  reasoning brittleness]
- Yao, S., Yu, D., Zhao, J., et al. (2022). "ReAct: Synergizing Reasoning and
  Acting in Language Models." arXiv:2210.03629. [Agents need grounding to avoid
  hallucination]

## Derived From
- **Lesson 16.4: LLM Reasoning**: brittleness of reasoning to premise order,
  autoregressive bias
- **Lesson 16.1: What Is an Agentic AI**: agents deployed in varied
  environments face distribution shift
- **Lesson 16.11: Lessons from Training Agentic Models**: domain generalization
  is hard; agents trained on one tool struggle on another
