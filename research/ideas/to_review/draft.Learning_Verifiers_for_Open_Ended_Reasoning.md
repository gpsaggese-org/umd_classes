# Learning Verifiers for Open-Ended Reasoning

## Status
**Status:** draft  
**Complete Specs:** 20%  
**Assignee:** —

# Core Idea [REQUIRED]
Verification is powerful for agent training when ground truth is available:
SWE-bench uses test suites to verify code fixes (Lesson 16.9), BrowseComp uses
task completion checks to verify web agents. With verification, agents can be
trained via RL on real outcomes, not preferences. However, many real agent tasks
have no mechanical oracle: open-ended planning, creative problem-solving, causal
reasoning, narrative generation. For these, practitioners fall back on
preference-based training (DPO, Lesson 16.8), which is noisier and susceptible
to hallucination and reward hacking (Lesson 16.9, Lesson 16.11)

**Central hypothesis**: We can learn task-agnostic verifiers that assess
trajectory quality without hand-crafted ground truth. A verifier trained on
historical feedback (past outcomes labeled by humans or downstream metrics) can
learn to rank agent trajectories by quality. This "learned verification" bridges
the gap between checkable tasks and open-ended reasoning

Key insight: A verifier does not need to solve the task; it only needs to
reliably distinguish good trajectories from bad. This is strictly easier than
task completion

## Formalization [OPTIONAL]
Let $\tau = (o_0, a_0, o_1, a_1, \ldots, a_{n-1}, o_n)$ be a trajectory
(observation-action pairs)

**Ground truth verifier** (when available):

$$
V_{\text{oracle}}(\tau) = \begin{cases} 1 & \text{if task objective satisfied} \\ 0 & \text{otherwise} \end{cases}
$$

**Learned verifier**:

$$
V_{\theta}(\tau) = P_{\theta}(\text{trajectory quality} \mid \tau)
$$

where $\theta$ are learned parameters

Training signal: historical data $\{(\tau_i, y_i)\}_{i=1}^{N}$ where
$y_i \in \{0, 1\}$ comes from upstream metric or human evaluation

**Verifier loss** (supervised classification):

$$
\mathcal{L}_{\text{verifier}} = -\sum_{i} y_i \log V_{\theta}(\tau_i) + (1 - y_i) \log(1 - V_{\theta}(\tau_i))
$$

Then use $V_{\theta}$ as reward in RL or as ranking in preference-based
training:

**DPO with learned verifier**: Given two trajectories $\tau_w, \tau_l$ for the
same task, if $V_{\theta}(\tau_w) > V_{\theta}(\tau_l)$, treat $\tau_w$ as
preferred and apply DPO loss

## Key Examples [REQUIRED]
- **Scientific writing**: Agent is asked to write a survey of recent papers on
  topic $X$. No mechanical ground truth. But historical data shows: surveys with
  high citation count, coherent narrative, and accurate summaries are good;
  surveys with hallucinated citations or contradictions are bad. Train verifier
  on (survey, quality_label) pairs. Use learned verifier to rank sampled
  surveys, then apply DPO

- **Multi-agent debate**: Two agents propose solutions to a problem; a verifier
  ranks them. Verifier is initially untrained; it learns from human feedback on
  past debates. Becomes increasingly accurate over time

- **Code generation for scientific computing**: Agent writes code to implement a
  numerical algorithm. Ground truth is hard: the code may run but be
  inefficient, or converge slowly. Verifier learns from historical performance
  metrics (runtime, accuracy, memory). Ranks trajectories by these metrics,
  enabling RL training without explicitly coding the reward

- **Edge case (failure mode)**: Verifier is biased by training distribution. If
  historical data overweights short trajectories, learned verifier may prefer
  brevity over correctness. Mitigation: detect and correct bias through
  out-of-distribution evaluation

## Questions [OPTIONAL]
1. **Verifier capacity and coverage**: How complex must the verifier be? Can a
   small model learn to rank complex reasoning, or does it need similar capacity
   to the generator?

2. **Feedback efficiency**: How much labeled historical data is needed to train
   a reliable verifier? Is 1K examples enough? 10K?

3. **Adversarial robustness**: Can an agent game the learned verifier (Lesson
   16.9's reward hacking)? How do we build verifiers that are hard to exploit?

4. **Domain transfer**: If trained on code verification, can the same verifier
   architecture work for planning or writing tasks?

## Research Topics [OPTIONAL]
- **Verifier architectures**: Should verifiers attend to full trajectories, or
  can they use summary statistics (final state, trajectory length, cost)? Can we
  build hierarchical verifiers (one for each task type)?
- **Multi-signal fusion**: Combine multiple imperfect signals (human preference,
  downstream metric, execution speed, user satisfaction) into a single verifier
  Weight them adaptively
- **Calibrated confidence**: Verifiers should not just rank, but assign
  confidence. A high-confidence ranking should be more reliable. How do we
  ensure calibration?
- **Active learning for verifiers**: Which trajectories should we label to most
  improve the verifier? Use uncertainty sampling or query-by-committee

## References [OPTIONAL]
- Dhuliawala, S., Pasunuru, R., Welbl, J., et al. (2023). "Chain-of-Verification
  Reduces Hallucination in Large Language Models." arXiv:2309.11495
  [Verification for hallucination reduction; learned decomposition]
- Huang, W., Abbeel, P., Pathak, D., & Xie, A. (2023). "Large Language Models
  Cannot Self-Correct Reasoning Yet." arXiv:2310.01798. [Self-correction without
  ground truth fails]
- Snell, C., Lee, J., Xu, K., & Kumar, A. (2024). "Scaling LLM Test-Time Compute
  Optimally Can Be More Effective than Scaling Model Parameters."
  arXiv:2408.03314. [Verification signals guide compute allocation]

## Derived From
- **Lesson 16.9: Post-Training and Verifiable Agents**: verification gap,
  reward hacking, verifiable tasks narrow
- **Lesson 16.8: Learning to Reason**: preference-based training brittleness
  without external signal
- **Lesson 16.6: Inference-Time Techniques**: OPRO shows optimization via real
  feedback; Self-Debug shows execution feedback drives refinement
