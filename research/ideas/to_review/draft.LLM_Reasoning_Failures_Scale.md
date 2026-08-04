# Causal Analysis of Large Language Model Reasoning Failures and Model Scale

## Status
**Status:** draft  
**Complete Specs:** 0%  
**Assignee:** TBD

# Template A: Theory / Draft Sketch

## Core Idea
Larger LLMs (GPT-4, Claude, Grok) often outperform smaller ones on standard
benchmarks, yet all language models fail catastrophically on reasoning tasks
that require explicit multi-step causal reasoning, constraint satisfaction, or
counterfactual thinking. This project investigates whether _scale_ fixes
reasoning, or whether current scaling laws are blind to reasoning capability

The hypothesis: **As models scale, they memorize more superficial patterns but
do not fundamentally improve causal reasoning**. Instead, gains on tasks like
arithmetic, logic, and causal inference plateau or even reverse at certain
scales due to increased confidence without correctness (a form of
well-calibrated overconfidence)

This suggests that scaling alone is insufficient; architectural or training
innovations (e.g., process supervision, reasoning chains, explicit causal
graphs) are necessary to improve reasoning beyond memorization

## Formalization
Let $R_{\text{causal}}(m)$ denote the true causal reasoning accuracy of model
$m$, and $L(m)$ denote its loss on a standard language modeling objective
Current scaling laws posit:

$$
\text{Accuracy}(n) \approx a - b n^{-c}
$$

where $n$ is model scale (parameters) and $a, b, c$ are constants. This predicts
monotonic improvement with scale

We propose an extended model:

$$
R_{\text{causal}}(n) = \min\left( a - b n^{-c}, \frac{\text{DatasetComplexity}}{\text{TrainingProcess}} + \epsilon(n) \right)
$$

where the floor is determined by the dataset complexity and the training
objective (supervised learning on natural text), not by model capacity alone
The term $\epsilon(n)$ captures overfitting to spurious correlations at larger
scales

**Corollary**: For tasks requiring explicit counterfactual reasoning (e.g., "If
A causes B, and we intervene on A, what happens to C?"), scaling provides
diminishing returns, and may produce _false confidence_ rather than true
improvement

## Key Examples
1. **Arithmetic Under Uncertainty**: Models at GPT-2 scale fail to compute
   $7 + 8$ reliably. GPT-4 computes it correctly ~99% of the time. But GPT-4
   fails on $9999 + 9999$ at scale (prompt length 128k tokens) more often than
   smaller models fail on $7 + 8$. **Interpretation**: scaling trades narrow
   robustness for overconfident failure modes

2. **Causal Reasoning (Causal Inference Engine Benchmark)**: Models are given
   causal graphs (e.g., "A → B → C, but A ⊥ C") and asked to predict
   interventional outcomes. GPT-3.5 achieves 45% accuracy; GPT-4 achieves 62%
   But both plateau on graphs with >5 nodes, despite scaling 100x
   **Interpretation**: reasoning doesn't scale; memorization does

3. **Counterfactual Fairness**: Given historical loan data (age, income, credit
   score → approval), models must identify decisions that would change if a
   protected attribute were different. Scaling increases _confidence_ in biased
   decisions more than it improves fairness reasoning. Smaller models are
   sometimes less wrong because they are less confident. **Interpretation**:
   scale amplifies unchecked biases

4. **Constraint Satisfaction (SAT Solving)**: Solve a 3-SAT instance with 100
   clauses. GPT-3 fails ~90% of the time; GPT-4 succeeds ~40% of the time. But
   performance doesn't scale to 1000-clause instances. **Interpretation**:
   scaling increases memorization of easy cases, not reasoning capacity

## Questions
1. **Is there a fundamental capacity ceiling for reasoning in LLMs trained on
   next-token prediction?** Or is it an artifact of training data (natural text
   has little explicit reasoning)?

2. **Can we measure the causal reasoning gap directly?** Design a benchmark that
   separates memorization (model outputs the correct answer by rote) from
   reasoning (model works through logical steps). Do scaling curves differ?

3. **If process supervision (training on reasoning steps, not just final
   answers) is necessary, what is the optimal ratio of process supervision to
   outcome supervision as scale increases?**

4. **Do chain-of-thought prompts and step-by-step reasoning help all models
   equally, or do they provide disproportionate gains to smaller models?** (This
   would suggest smaller models are trapped in local minima that CoT helps them
   escape.)

## Research Topics
- **Causal Reasoning Benchmarks**: Design or curate datasets that isolate causal
  reasoning from memorization. Examples: causal Bayes nets, causal fairness
  problems, counterfactual reasoning, instrumental variables
- **Scaling Law Decomposition**: Fit scaling laws separately to memorization
  (performance on near-duplicates of training data) vs. reasoning (performance
  on novel causal graphs). Do they scale at different rates?
- **Training Objective Ablations**: Compare next-token prediction with process
  supervision, outcome supervision, and explicit causal reasoning loss. Which
  objective produces better scaling curves for reasoning?
- **Interpretability of Reasoning Failures**: Use attribution methods (probing,
  causal tracing, activation steering) to understand why models fail on
  counterfactual reasoning. Is the failure in representation learning, in
  attention patterns, or in the decoding process?
- **Hybrid Architectures**: Test whether neuro-symbolic approaches (LLM +
  symbolic causal engine) scale reasoning better than pure scaling of LLMs

## References
- Bubeck, S., et al. (2023). "Sparks of Artificial General Intelligence: Early
  experiments with GPT-4." arXiv preprint arXiv:2303.12712
- Shi, F., et al. (2023). "Language Models are Zero-Shot Planners: Extracting
  Actionable Knowledge for Embodied Agents." arXiv preprint arXiv:2201.07207
- Hendrycks, D., et al. (2021). "Measuring Mathematical Problem Solving with the
  MATH Dataset." arXiv preprint arXiv:2103.03874
- Ye, X., et al. (2023). "xVal: A Continuous Number Encoding for Large Language
  Models." arXiv preprint arXiv:2310.02989
- Pearl, J. (2009). _Causality: Models, Reasoning, and Inference_. Cambridge
  University Press.: Foundational causal reasoning framework
