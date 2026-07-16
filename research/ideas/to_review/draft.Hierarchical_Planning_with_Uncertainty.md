# Hierarchical Planning with Uncertainty Quantification

## Status
**Status:** draft  
**Complete Specs:** 25%  
**Assignee:** —

# Core Idea [REQUIRED]
Current agentic systems (ReAct) operate reactively: perceive current state,
choose one action, execute it, repeat. This myopic strategy accumulates errors
over long horizons. With per-step success probability $p = 0.95$, a 10-step task
has only $(0.95)^{10} \approx 0.60$ success rate (Lesson 16.1). World models
exist (WebDreamer, Lesson 16.5) but only simulate 1–2 steps ahead in a latent
space that may diverge from reality

**Central insight**: Agents need to reason hierarchically before committing
First, decompose the goal into subgoals and order them (high-level planning)
Then, estimate uncertainty in action outcomes and identify "critical" vs. "safe"
decisions. Finally, execute low-level actions with adaptive replanning when
observations contradict predictions

This mirrors human decision-making: "to book a flight, I need to (1) search
airlines, (2) compare options, (3) choose one, (4) enter payment." Each step has
risks; we plan to mitigate them before acting

## Formalization [OPTIONAL]
Let $g$ be a goal. A **hierarchical planner** decomposes
$g \to [g_1, g_2, \ldots, g_k]$ (subgoals in order)

For each subgoal $g_i$, estimate **uncertainty**:
$U_i = \Pr[\text{fail at } g_i \mid \text{succeed at } g_{i-1}]$

Define **criticality**: $C_i = U_i \cdot \text{cost\_if\_fail}(g_i)$. High
criticality means errors are expensive and likely

**Planning strategy**:

- For low-criticality goals: act reactively (one action, observe, adapt)
- For high-criticality goals: search over candidate actions using a learned
  world model; pick the action with lowest predicted failure probability

Formal objective:

$$
\pi^* = \arg\max_{\pi} \Pr[\text{succeed at } g] = \prod_{i=1}^{k} (1 - U_i)
$$

Approximate using a world model $M(s, a) \to s'$:

$$
U_i \approx 1 - \max_{a \in A_i} \Pr[s' \text{ is in target region} \mid M(s, a)]
$$

## Key Examples [REQUIRED]
- **Flight booking**: Goal is "book a flight to NYC on June 1, under $300."
  Decompose into: (1) search for flights (low criticality, search is robust),
  (2) filter by date/price (low criticality), (3) enter payment details (high
  criticality: typos are costly). For step 3, use uncertainty-aware search: try
  multiple formulations of payment entry, pick the one the world model predicts
  will succeed

- **Multi-hop question answering**: Goal is "find author of novel that inspired
  film that won Best Picture in 2020." Decompose: (1) identify film, (2) find
  novel, (3) find author. Step 1 is high-risk (wrong film ruins everything). Use
  world model to simulate multiple film searches, pick the one with highest
  confidence. Steps 2–3 are lower risk given step 1

- **Code debugging**: Agent is asked to fix a failing test. Decompose: (1)
  understand the test (what should happen), (2) find the bug (where is the
  failure), (3) write the fix. Step 2 is high-criticality: finding the wrong
  location wastes time. For step 2, sample multiple hypotheses about where the
  bug is, simulate the fix for each, and choose the hypothesis the world model
  predicts will resolve the test most confidently

- **Edge case (failure mode)**: hierarchical planning assumes subgoals are
  independent. If subgoals interact (e.g., fixing a bug in module A breaks a
  previously passing test in module B), the hierarchy collapses and the plan
  must be replanned. Agents need to detect such interactions and backtrack

## Questions [OPTIONAL]
1. **Automatic subgoal decomposition**: How does an agent automatically
   decompose a goal into subgoals without task-specific knowledge? Can this be
   learned from demonstrations, or must it be provided?

2. **Uncertainty estimation**: What is a good estimator of $U_i$? Option 1:
   learned value function. Option 2: uncertainty in world model predictions
   Option 3: empirical success rate from past rollouts. Which generalizes best?

3. **Replanning criterion**: When should an agent abandon a plan and replan? If
   the observed state diverges from the world model's prediction, how much
   divergence triggers replanning?

4. **Scalability to long horizons**: Can hierarchical planning scale to 100-step
   tasks? Do we need multiple levels of hierarchy (high-level goals → subgoals →
   micro-actions)?

## Research Topics [OPTIONAL]
- **Learning hierarchies**: Train a model to decompose goals using
  self-supervised learning from successful trajectories (extract the subgoals
  humans would use)
- **World models for hierarchies**: Build world models that operate at different
  levels of abstraction. A high-level world model predicts "will this search
  find a relevant result?" A low-level one predicts "will this keystroke be
  correctly interpreted?"
- **Uncertainty propagation**: Formalize how uncertainty at one level compounds
  across levels. Derive bounds on end-to-end success probability given per-step
  uncertainties
- **Adaptive compute allocation**: Spend more model inference on
  high-criticality steps (more extensive search); rush through low-criticality
  steps

## References [OPTIONAL]
- Yao, S., Yu, D., Zhao, J., et al. (2022). "ReAct: Synergizing Reasoning and
  Acting in Language Models." arXiv:2210.03629. [Current reactive approach]
- Gu, W., Zaharia, M., Ermon, S., & Liang, P. (2024). "WebDreamer: Is Your LLM
  Secretly a World Model of the Internet?" arXiv:2411.06559. [World models for
  web agents]
- Li, Z., Chen, W., Gao, S., et al. (2024). "Chain-of-Thought Empowers
  Transformers to Solve Inherently Serial Problems." arXiv:2402.12875. [Serial
  reasoning as computation]

## Derived From
- **Lesson 16.1: What Is an Agentic AI**: compounding errors over long horizons
- **Lesson 16.5: Reasoning, Memory, and Planning**: world models, model-based
  planning
- **Lesson 16.3: History of LLM Agents**: reactive (ReAct) limitations, need
  for better planning
