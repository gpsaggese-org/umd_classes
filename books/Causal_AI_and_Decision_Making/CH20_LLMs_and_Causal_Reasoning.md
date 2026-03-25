# LLMs and Causal Reasoning
Large Language Models (LLMs) have transformed how we approach language
understanding and generation, but their relationship with causal reasoning is
complex. LLMs excel at pattern recognition and language modeling but lack
explicit causal mechanisms. This chapter explores what LLMs can and cannot tell
us about causality, and how we can augment them with structured reasoning
frameworks to improve causal inference and decision-making tasks.

## What LLMs Get Right and Wrong About Causality
LLMs are trained on vast amounts of text data using next-token prediction
objectives, which means they learn statistical associations between words and
concepts. This gives them certain strengths and critical limitations when
reasoning about causality.

### What LLMs Get Right
- **Recognizing causal language patterns**: LLMs can identify common causal
  expressions like "because," "caused by," "led to," and "resulted in." They can
  extract causal relationships that are explicitly stated in text.

- **Reasoning with causal narratives**: When causal relationships are present in
  training data, LLMs can reproduce and extend causal arguments. They understand
  temporal ordering and can connect events in a sequence.

- **Common sense reasoning**: LLMs capture commonsense knowledge about physical,
  social, and biological causality. For example, they understand that "rain
  causes wet ground" and "studying causes better test scores."

- **Generating plausible explanations**: LLMs can generate coherent explanations
  and narratives about why events happen, drawing on patterns in their training
  data.

### What LLMs Get Wrong
- **No explicit causal mechanism**: LLMs do not have an internal model of
  causality (like a causal graph). They cannot perform interventional reasoning
  (what if we change X?) without explicit guidance. They reason from correlation
  and association, not from causal mechanisms.

- **Confounding and spurious correlations**: LLMs can be misled by spurious
  correlations in their training data. If two variables are highly correlated in
  text but not causally related, an LLM may confidently claim causation. For
  example, if ice cream sales and shark attacks are frequently mentioned
  together in summer articles, an LLM might conclude one causes the other.

- **No principled counterfactual reasoning**: Generating true counterfactuals
  ("What if X had been different?") requires understanding causal mechanisms.
  LLMs generate plausible counterfactuals based on patterns but without causal
  justification. They may produce grammatically correct but causally
  inconsistent counterfactuals.

- **Brittleness to distribution shift**: LLMs trained on observed data struggle
  when asked to reason about interventions or scenarios far from their training
  distribution. They cannot generalize causal relationships to new contexts in
  the principled way causal models can.

- **Confusing observation with intervention**: LLMs often treat observational
  statements and interventional statements identically, leading to errors.
  Asking "What does X predict about Y?" and "If we change X, what happens to Y?"
  should yield different answers in most causal settings, but LLMs may conflate
  them.

**References**

- Kosko, B. (1993). _Fuzzy thinking: The new science of fuzzy logic_. Hyperion.
- Pearl, J., & Mackenzie, D. (2018). _The book of why: The new science of cause
  and effect_. Basic Books.
- Schölkopf, B. (2022). Toward causal representation learning. _Proceedings of
  the IEEE_, 109(5), 612-645.

## Chain-of-Thought, Tree-of-Thought, and Self-Consistency for Causal Tasks
Recent advances in prompting and reasoning have shown that LLMs can improve
their causal reasoning through explicit step-by-step reasoning frameworks. These
techniques encourage LLMs to decompose complex problems and explore multiple
reasoning paths.

### Chain-of-Thought Prompting
- **Concept**: Instead of asking an LLM to directly answer a question, you ask
  it to explain its reasoning step-by-step. This intermediate reasoning often
  improves accuracy on complex tasks.

- **Example**: Rather than asking "If we increase advertising spend, what
  happens to sales?", ask "Let's think through this step-by-step: (1) How does
  advertising increase brand awareness? (2) How does awareness affect purchase
  intent? (3) How does purchase intent affect sales? (4) Are there confounders?"
  This structured approach pushes the LLM to articulate causal assumptions.

- **Why it helps**: Chain-of-thought reasoning forces the LLM to make causal
  assumptions explicit and consider multiple steps in a causal chain. It reduces
  reliance on shallow pattern matching.

- **Limitations**: The reasoning quality depends on the LLM's ability to
  construct valid causal chains. If the LLM lacks knowledge about a domain,
  chain-of-thought may produce plausible-sounding but incorrect reasoning.

### Tree-of-Thought Reasoning
- **Concept**: Tree-of-thought extends chain-of-thought by allowing the LLM to
  explore multiple reasoning branches simultaneously. At each step, the LLM
  generates several possible next thoughts and evaluates them.

- **Application to causality**: For causal inference problems, tree-of-thought
  allows the LLM to consider multiple causal hypotheses simultaneously. For
  example, when explaining why a correlation exists, the LLM can explore
  alternative causal mechanisms (X → Y, Y → X, Z → X and Y, measurement error,
  etc.) and reason about which is most plausible.

- **Benefits**: By exploring multiple causal paths, tree-of-thought can help
  LLMs avoid committing to a single spurious explanation too early. It provides
  a more comprehensive view of possible causal structures.

### Self-Consistency Approaches
- **Concept**: Self-consistency generates multiple independent reasoning paths
  (using temperature or sampling variation) and then aggregates the results via
  voting or consensus.

- **Causal application**: For causal inference, you can prompt the LLM multiple
  times with different framing or decompositions. If multiple independent
  reasoning processes agree on a causal relationship, confidence in that
  reasoning increases.

- **Example**: Ask the LLM five times "Does X cause Y?" with different phrasings
  or from different angles. If four out of five reasoning paths conclude "yes,"
  this provides evidence for the causal claim beyond a single sample.

- **Caveat**: This assumes that diverse reasoning paths are truly independent.
  In reality, an LLM's reasoning is constrained by its training, so multiple
  samples may be correlated.

**References**

- Wei, J., Wang, X., Schuurmans, D., Bosma, M., Xia, F., Chi, E., ... & Zhou, D.
  (2022). Emergent abilities of large language models. arXiv preprint
  arXiv:2206.07682.
- Yao, S., Yu, D., Zhao, J., Shafran, I., Griffiths, T. L., Cao, Y., &
  Narasimhan, K. (2023). Tree of Thoughts: Deliberate Problem Solving with Large
  Language Models. arXiv preprint arXiv:2305.10601.
- Wang, X., Wei, J., Schuurmans, D., Le, Q., Chi, E., & Zhou, D. (2023).
  Self-consistency improves chain of thought reasoning in language models.
  _arXiv preprint arXiv:2203.11171_.

## Reflection and Self-Correction: Reflexion and Iterative Refinement
Beyond single-pass reasoning, LLMs can improve through reflection and iterative
refinement. These techniques allow LLMs to evaluate their own reasoning and
adjust their conclusions.

### Reflexion Framework
- **Concept**: Reflexion is an approach where LLMs explicitly reflect on their
  reasoning, identify errors or inconsistencies, and produce refined answers.
  The process involves:
  1. Generate an initial response (a causal claim or inference)
  2. Evaluate the response for logical consistency and alignment with evidence
  3. Identify specific weaknesses or errors
  4. Generate a refined response addressing the identified issues

- **Causal application**: For causal reasoning, reflexion prompts the LLM to
  ask: "Does my causal claim follow from the evidence? What alternative
  explanations did I miss? What assumptions am I making? Are there known
  confounders in this domain?"

- **Example**: An LLM initially claims "Social media use causes depression."
  Reflexion prompts it to reconsider:
  - "What are alternative explanations? (e.g., depression causes social media
    use, a third variable causes both)"
  - "What evidence would distinguish these explanations?"
  - "What am I assuming about causality that might not hold?"
  - The refined response becomes more nuanced: "The relationship between social
    media and depression is bidirectional and confounded by underlying mental
    health conditions."

- **Benefits**: Reflexion encourages intellectual honesty and reduces
  overconfident causal claims. It surfaces hidden assumptions.

### Iterative Refinement with Feedback
- **Concept**: An LLM generates an initial response, receives feedback (from a
  human, a causal expert system, or another model), and iteratively improves its
  response.

- **Integration with causal domain knowledge**: Feedback can come from:
  - Domain experts who identify errors in causal reasoning
  - Causal inference tools (like DoWhy) that verify assumptions and suggest
    corrections
  - Statistical tests that evaluate whether claimed causal effects hold in data

- **Example workflow**:
  1. LLM proposes a causal explanation for a phenomenon
  2. A causal inference tool evaluates the proposed causal graph for
     identifiability
  3. If unidentifiable, the tool provides specific reasons (e.g., "There is an
     unobserved confounder between X and Y")
  4. The LLM uses this feedback to refine its causal claim or propose
     identification strategies

- **Limitations**: Iterative refinement requires reliable feedback. If the
  feedback mechanism is flawed or biased, iterations may propagate errors.

**References**

- Shinn, N., Cassano, F., Gopinath, A., Narasimhan, K., & Yao, S. (2024).
  Reflexion: an autonomous agent with dynamic memory and self-reflection. _arXiv
  preprint arXiv:2303.11366_.
- Warnell, G., Herrmann, J., Kannan, S., & Bansal, M. (2017). Deep reinforcement
  learning from policy-dependent human feedback. arXiv preprint
  arXiv:1805.11074.

## Connecting LLM Reasoning to Causal and Probabilistic Reasoning
The most powerful applications emerge when we integrate LLM reasoning with
formal causal and probabilistic models. This hybrid approach combines LLM
strengths (language understanding, commonsense knowledge) with causal strengths
(principled inference, identifiability).

### Bridging Language and Causal Graphs
- **Concept**: LLMs can be used to extract causal structures from text, propose
  causal graphs, and reason about them. The extracted causal graph can then be
  formalized and analyzed using causal inference tools.

- **Workflow**:
  1. LLM reads a domain description or case study
  2. LLM identifies variables and proposes causal relationships
  3. These are formalized as a Directed Acyclic Graph (DAG)
  4. Causal inference algorithms analyze identifiability and estimate causal
     effects
  5. Results are communicated back to stakeholders in natural language

- **Example**: An LLM reads a document about customer retention and proposes:
  "Customer satisfaction → Retention" and "Support quality → Satisfaction →
  Retention." These are formalized as edges in a causal graph. Causal
  identification algorithms then determine whether we can estimate the causal
  effect of support quality on retention from observational data.

### Probabilistic Reasoning Integration
- **Concept**: LLMs can work with probabilistic reasoning systems (e.g.,
  Bayesian networks, factor graphs) by:
  - Converting natural language descriptions into probability distributions
  - Asking the LLM to estimate conditional probabilities or priors from domain
    knowledge
  - Using the LLM to interpret results of probabilistic inference in
    human-understandable terms

- **Uncertainty quantification**: Rather than LLM outputs as point estimates,
  probabilistic frameworks allow LLMs to express uncertainty. For example: "I'm
  70% confident that X causes Y, 20% confident that Y causes X, and 10%
  confident they're caused by a confounder."

- **Bayesian updating**: LLMs can articulate prior beliefs about causal
  relationships, and these can be updated with data using Bayesian inference.

- **Example**: A risk assessment task where the LLM estimates prior
  probabilities for various causes of a system failure, then observes evidence
  (error logs, sensor readings) and performs Bayesian updating to refine causal
  hypotheses.

### Symbolic and Neurosymbolic Approaches
- **Concept**: Neurosymbolic AI combines the pattern recognition of neural
  networks (like LLMs) with symbolic reasoning systems (like causal inference
  engines). This allows:
  - LLMs to propose hypotheses and decompose problems
  - Symbolic systems to verify consistency, check identifiability, and apply
    logical rules
  - Feedback between both systems

- **Application to causality**: A neurosymbolic system might use an LLM to
  generate multiple causal hypotheses, then use symbolic causal inference to
  rank them by plausibility based on domain knowledge and data.

- **Advantage**: This approach reduces LLM hallucinations and overconfidence by
  grounding reasoning in symbolic constraints. It also makes reasoning more
  interpretable.

**References**

- Moor, M., Banfield, M., Zhou, Z., Frye, J., Ong, B., Bhattacharyya, Y., ... &
  Rish, I. (2023). Foundation models for knowledge graph completion: A
  comparative study. arXiv preprint arXiv:2310.11220.
- Kaur, H., Nori, H., Jenkins, S., Caruana, R., Wallach, H., & Wexler, J.
  (2020). Interpreting Black Box Models via Model Extraction. arXiv preprint
  arXiv:1606.03226.
- Mao, J., Gan, C., Gan, C., Zhang, Y., Tenenbaum, J. B., & Wu, J. (2021). The
  neurosymbolic concept learner: Interpreting scenes, words, and worlds. In
  _International Conference on Machine Learning_ (pp. 7282-7292). PMLR.

## TUTORIAL: LangChain (CoT and Tool-augmented Reasoning Pipelines)

## TUTORIAL: LlamaIndex (knowledge-grounded Reasoning Over Structured Data)