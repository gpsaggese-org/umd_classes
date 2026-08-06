# Tool-Agnostic and Few-Shot Tool Learning for Agents

## Status
**Status:** draft  
**Complete Specs:** 22%  
**Assignee:** —

# Core Idea [REQUIRED]
Agents trained on a specific set of tools (web navigation + APIs + code sandbox)
struggle to generalize to new tools. KIMI K2 and DeepSeek-V3 both required
training on diverse tool types to learn generalizable patterns (Lesson 16.11),
yet even with such diversity, deployment on novel tools requires fine-tuning
Each tool has idiosyncratic conventions: web buttons are clicked with
coordinates, APIs accept structured JSON, CLIs take string arguments. Errors
manifest differently too (network timeout vs. parse error vs. permission
denied)

**Central hypothesis**: Agents can learn tool-agnostic action representations
and meta-patterns that transfer to new tools with minimal examples. Instead of
representing actions as tool-specific tokens, represent them abstractly as
`(function_name, typed_arguments)`. Train the agent to learn patterns like "call
function, check result, retry if error" that work across domains. Given a new
tool's documentation and 1–2 examples, the agent can adapt in-context without
weight updates

This is a meta-learning problem: learn the learning algorithm for tools, not
individual tools

## Formalization [OPTIONAL]
Let $T = \{t_1, t_2, \ldots, t_k\}$ be a set of tools (web, API, code, CLI)
Each tool $t$ has:

- **Interface**: $I_t = \{f_1, f_2, \ldots, f_m\}$ (set of callable functions)
- **Schema**: for each $f$, types and constraints on inputs/outputs
- **Error modes**: exceptions and failure patterns specific to $t$

**Tool-agnostic representation**:

$$
a_t = (\text{func_id}, \text{args}; \text{type_signature})
$$

where `func_id` is abstract (can be bound to any tool's function), `args` are
typed, and `type_signature` is explicit

**Meta-learning objective**:

$$
\theta^* = \arg\min_{\theta} \sum_{t \in T_{\text{train}}} \mathcal{L}_{\text{RL}}(\tau_t; \theta)
$$

where $\tau_t$ are trajectories using tool $t$. The trained $\theta$ should:

1. Generalize to new tools $t \notin T_{\text{train}}$ with few-shot adaptation
2. Learn that "call function → check result → adapt" is universal

**Few-shot adaptation**: given new tool $t_{\text{new}}$ with documentation
$D_{\text{new}}$ and 1–2 examples $(x, \tau_{\text{demo}})$:

$$
\theta_{\text{new}} = \text{MAML-style update}(\theta; D_{\text{new}}, \tau_{\text{demo}})
$$

or in-context:

$$
a_{\text{new}} = \pi_{\theta}(o_t \mid D_{\text{new}}, \tau_{\text{demo}})
$$

## Key Examples [REQUIRED]
- **Web to API transition**: Agent trained on Selenium-based web browsing
  (click, type, read HTML) must adapt to REST APIs (GET, POST, parse JSON)
  Tool-agnostic representation treats both as: `call(func, args) → result`
  Error patterns ("not found" vs. "auth failed") are learned as meta-patterns,
  not tool-specific

- **Code sandbox to REPL**: Agent trained to generate Python code in a sandbox
  (run, see error, fix) must adapt to an interactive REPL where state persists
  Underlying pattern is the same: `execute(code) → output`. The difference
  (persisted state) is captured by the tool's schema, not the action
  representation

- **New API endpoint discovery**: Developer publishes a new API endpoint. Agent
  is shown 2 example API calls and their responses. It immediately learns to use
  this endpoint without retraining, because it generalizes the pattern
  "construct request → parse response" across all APIs it has seen before

- **Edge case (failure mode)**: Some tools are fundamentally different (e.g., a
  formal theorem prover has different success criteria than a web scraper)
  Meta-learning may not transfer across such dissimilar domains. Mitigation:
  cluster tools by similarity; meta-learn within clusters

## Questions [OPTIONAL]
1. **Universal action representation**: Is there a single action representation
   that works for all tools, or do we need domain-specific embeddings? Can we
   learn this representation from data?

2. **Few-shot sample complexity**: How many examples are needed for good
   in-context adaptation? Is 1 enough? Does it depend on tool similarity to
   training tools?

3. **Error recovery generalization**: An agent learns to recover from specific
   error types (timeout, permission denied). Does it generalize to new error
   types it hasn't seen? How do we measure generalization?

4. **Compositionality across tools**: If agent learns to chain web + code tools,
   can it chain code + API tools without retraining?

## Research Topics [OPTIONAL]
- **Tool representations**: Design and evaluate candidate action representations
  (abstract, typed, explicit-error-handling). Which generalizes best?
- **Meta-learning algorithms**: Compare in-context learning (prompt examples)
  vs. MAML-style gradient updates vs. adapter layers for tool adaptation
- **Tool similarity metrics**: Define a metric to measure which tools are
  similar enough to share meta-patterns. Use this to guide curriculum learning
- **Evaluation benchmark**: Create a benchmark with 50+ tools (web, APIs, CLIs,
  code, databases). Train on subset; evaluate zero-shot and few-shot on held-out
  tools

## References [OPTIONAL]
- Yao, S., Yu, D., Zhao, J., et al. (2022). "ReAct: Synergizing Reasoning and
  Acting in Language Models." arXiv:2210.03629. [Agents with tools; grounding
  necessary]
- OpenAI. (2024). "KIMI K2: Open Agentic Intelligence." Unpublished. [Lesson
  16.11 case study; multi-tool training needed]
- Xu, C., Liu, K., Cao, Y., et al. (2024). "DeepSeek-V3 Technical Report."
  Unpublished. [Lesson 16.11 case study; tool specialization via routing]

## Derived From
- **Lesson 16.11: Lessons from Training Agentic Models**: domain generalization
  is hard; agents trained on one tool struggle on others
- **Lesson 16.1: What Is an Agentic AI**: tools are the agent's hands;
  constrained action space
- **Lesson 16.5: Reasoning, Memory, and Planning**: generic patterns for
  planning (search, evaluate) apply across domains
