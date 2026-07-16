# Hybrid Memory: Scalable Retrieval with In-Weight Reasoning

## Status
**Status:** draft  
**Complete Specs:** 20%  
**Assignee:** —

# Core Idea [REQUIRED]
Million-token context windows enable agents to stuff large documents into
prompts, and the needle-in-a-haystack benchmark shows 99%+ recall for single
facts at 1M tokens (Lesson 16.7). But the test is misleading: on realistic tasks
with 100 embedded facts, recall drops to ~60%. Meanwhile, retrieval systems (RAG
with vector search) are practical but fail on multi-hop queries where relevant
passages never co-occur (Lesson 16.5). HippoRAG solves multi-hop via knowledge
graphs, but updating a graph is expensive (requires reindexing). Parametric
memory (grokking, Lesson 16.5) can encode reasoning over facts into weights,
achieving near-perfect accuracy on in-distribution queries, but updating
requires retraining

**Central insight**: Agents need a _hybrid_ memory system that combines three
modes:

1. **Core parametric memory**: frequently-needed patterns and reasoning (stored
   in weights via grokking or standard training)
2. **Dynamic retrieval index**: recent/specialized facts retrievable on-demand
3. **Adaptive router**: decides when to reason from weights vs. when to retrieve

This mirrors human cognition: we know common facts (world capitals, arithmetic)
from memory; we look up specialized facts in books; we know how to find
information (what search terms work)

## Formalization [OPTIONAL]
Let $K = \{k_1, k_2, \ldots, k_N\}$ be a knowledge base of facts. Partition
into:

- **Core**: $K_c$ (frequently accessed, $|K_c| \ll |K|$)
- **Peripheral**: $K_p = K \setminus K_c$ (rare, specialized)

**Memory system**:

$$
\text{answer} = \pi(\text{query}; \pi_{\text{core}}, \pi_{\text{retrieval}}, R)
$$

where:

- $\pi_{\text{core}}$ answers from weights (parametric memory of $K_c$)
- $\pi_{\text{retrieval}}$ retrieves from index, answers from $K_p$
- $R$ is a learned **router** that decides which mode to use

**Router**:

$$
R(\text{query}) \to (\text{mode} \in \{\text{core}, \text{retrieve}, \text{both}\})
$$

**Training objective** (jointly optimize all three):

$$
\mathcal{L} = \sum_{q, a^*} \ell(\text{answer}(q), a^*) + \lambda_c \cdot \text{cost}_{\text{core}} + \lambda_r \cdot \text{cost}_{\text{retrieve}}
$$

where cost terms penalize retrieval latency and parametric memory staleness

**Multi-hop reasoning**:

Extend retrieval to iterative:

$$
\text{passage}_1 = \text{retrieve}(q)
$$

$$
\text{passage}_2 = \text{retrieve}(q + \text{passage}_1)
$$

$$
\text{answer} = \pi(\text{query}, \text{passage}_1, \text{passage}_2)
$$

or use graph-structured retrieval (HippoRAG, Lesson 16.5)

## Key Examples [REQUIRED]
- **Enterprise knowledge base**: Company has 10M documents. Agent needs to
  answer customer support questions. Core memory: common policies (returns,
  shipping, warranty) stored in weights via SFT. Peripheral: individual customer
  records, contract details, specific product specs. Router decides: "returns
  policy?" → answer from core. "Customer 12345's order status?" → retrieve from
  index. "Did our recent product launch comply with regulations?" → both
  (retrieve launch docs, reason using core knowledge of regulations)

- **Scientific literature synthesis**: Researcher has 50K papers on machine
  learning. Agent writes survey on "robustness in neural networks." Core memory:
  foundational concepts (gradient descent, adversarial examples, certified
  defenses) learned from standard training. Peripheral: recent papers with novel
  techniques. Router: general concepts from core, specific findings and
  citations from retrieval. Multi-hop: "Which robustness method uses ideas from
  X?" routes through HippoRAG-style graph

- **Persistent agent across sessions**: Agent operates over days, accumulating
  experience. Each session adds new facts (user preferences, API changes, task
  outcomes). New facts initially in retrieval index (hot facts). After repeated
  access, facts migrate to parametric memory (periodic fine-tuning on frequent
  facts). Old facts archived (moved to cold storage or dropped). This is like
  human memory: recently learned facts are in working memory, then consolidate
  to long-term

- **Edge case (failure mode)**: Router is wrong. Agent asks question that looks
  like "core" but is actually "peripheral" (e.g., "capital of X" where X is a
  new micro-nation). Router sends to core, gets hallucination. Mitigation: learn
  router confidence; route to retrieval when confidence is low

## Questions [OPTIONAL]
1. **Partitioning strategy**: How do we decide which facts belong in core vs
   peripheral? Options: frequency (frequent → core), recency (recent →
   peripheral), importance (critical → core). Which minimizes cost + accuracy?

2. **Router training**: Is a separate router model needed, or can we train
   end-to-end with a soft router (learned gating)? How much does routing
   performance affect overall accuracy?

3. **Staleness of parametric memory**: Facts in weights are fixed until
   retraining. How stale can they be before performance degrades? How often
   should we retrain core memory?

4. **Multi-hop beyond two hops**: HippoRAG handles multi-hop via graph. Can we
   compose parametric + retrieval multi-hop? E.g., fact 1 from weights, fact 2
   from retrieval, reason over both

## Research Topics [OPTIONAL]
- **Core/peripheral partitioning**: Devise automatic algorithms (e.g., access
  frequency, inverse document frequency, gradient-based importance). Compare
  strategies on benchmarks
- **Joint training**: Optimize parametric + retrieval + router end-to-end
  Design loss functions that balance accuracy, latency, and staleness
- **Adaptive router design**: Compare fixed rules (frequency threshold) vs
  learned routers (small MLP). Measure routing accuracy on oracle ground truth
  (we know which facts are in core)
- **Evaluation benchmark**: Create benchmark with 1M facts, realistic access
  patterns. Measure latency, accuracy, staleness. Compare to pure stuffing and
  pure retrieval baselines

## References [OPTIONAL]
- Gutiérrez, R., Dehaene, S., & Leblois, A. (2024). "HippoRAG: Neurobiologically
  Inspired Long-Term Memory for Large Language Models." arXiv:2405.14831
  [Multi-hop retrieval via knowledge graphs]
- Wang, Y., Zhang, Y., Hong, S., et al. (2024). "Grokked Transformers are
  Implicit Reasoners." arXiv:2405.15071. [Parametric memory via training]
- Kamradt, T. (2023). "The Needle in a Haystack Test: Evaluating Performance of
  RAG Systems." Toward Data Science. [Long-context recall limitations]

## Derived From
- **Lesson 16.7: Tool Use and Retrieval**: RAG, vector search,
  needle-in-haystack tradeoffs
- **Lesson 16.5: Reasoning, Memory, and Planning**: HippoRAG for multi-hop,
  grokking for parametric memory
- **Lesson 16.2: LLM Building Blocks**: context window limits drive memory
  choices
