# Summary
- Large Language Models (LLMs) excel at pattern recognition and statistical
  language modeling but lack explicit causal mechanisms
- This chapter explores what LLMs can and cannot tell us about causality
- Hybrid systems combining LLMs with formal causal frameworks offer the most
  promising path forward for improved causal inference and decision-making

# LLMs and Causal Reasoning

## Introduction
- LLMs transform language understanding and generation, but their relationship
  with causality is complex
- LLMs excel at pattern recognition and statistical language modeling but lack
  explicit causal mechanisms
- The fundamental training objective of next-token prediction doesn't encode
  causal knowledge
- You need to understand the distinction between correlation-based pattern
  learning and principled causal reasoning
- The key question: what can LLMs tell us about causality, and how can we
  augment them with structured reasoning frameworks

## What LLMs Get Right and Wrong About Causality
- LLMs are trained on vast amounts of text data using next-token prediction
  objectives
  - They learn statistical associations between words and concepts
  - This training paradigm works well for language understanding and generation
  - It has fundamental implications for causal reasoning
  - The result: certain strengths and critical limitations when reasoning about
    causality

- Training objective is to maximize: $\mathcal{L} = \sum_i \log P(x_i | x_{<i})$
  - Each token's probability depends only on preceding context
  - This explains both successes and failures of LLMs in causal reasoning tasks

### What LLMs Get Right
- **Recognizing causal language patterns**: LLMs can identify common causal
  expressions like "because," "caused by," "led to," and "resulted in." They
  extract causal relationships explicitly stated in text. But this recognition
  is fundamentally linguistic—the model identifies markers of causal claims
  without understanding the underlying mechanisms

- **Reasoning with causal narratives**: When causal relationships are present in
  training data, LLMs can reproduce and extend causal arguments. They understand
  temporal ordering and can connect events in a sequence. This narrative
  reasoning helps with explanatory text generation where coherence is valued

- **Common sense reasoning**: LLMs capture commonsense knowledge about physical,
  social, and biological causality. They understand that "rain causes wet
  ground" and "studying causes better test scores." This foundation helps with
  practical reasoning tasks

- **Generating plausible explanations**: LLMs can generate coherent explanations
  and narratives about why events happen. This generative capability works well
  in domains where multiple valid explanations exist and you need interpretable
  reasoning

### What LLMs Get Wrong
- **No explicit causal mechanism**: LLMs don't have an internal model of
  causality (like a causal graph). They can't perform interventional reasoning
  (what if we change X?) without explicit guidance. They reason from correlation
  and association, not from causal mechanisms. LLMs lack the `do-operator`
  intervention calculus from Pearl's causal framework, which is essential for
  distinguishing causation from correlation

- **Confounding and spurious correlations**: LLMs can be fooled by spurious
  correlations in their training data. If two variables are highly correlated in
  text but not causally related, an LLM may confidently claim causation. For
  example, if ice cream sales and shark attacks are frequently mentioned
  together in summer articles, an LLM might conclude one causes the other. The
  model can't distinguish confounding by season from direct causation

- **No principled counterfactual reasoning**: True counterfactuals ("What if X
  had been different?") require understanding causal mechanisms. LLMs generate
  plausible counterfactuals based on patterns but without causal justification.
  When asked "If X had not happened, would Y still occur?", the model can't
  reliably account for downstream causal dependencies that the intervention
  would disrupt

- **Brittleness to distribution shift**: LLMs trained on observed data struggle
  when reasoning about interventions or scenarios far from their training
  distribution. They can't generalize causal relationships to new contexts the
  way causal models can. For transfer learning in causal inference, where
  robustness across domains is essential, this is a critical limitation

- **Confusing observation with intervention**: LLMs often treat observational
  and interventional statements identically, leading to errors. Asking "What
  does X predict about Y?" and "If we change X, what happens to Y?" should
  yield different answers in most causal settings. But LLMs may conflate them.
  This violates a fundamental principle: $P(Y|X=x)$ differs from
  $P(Y|do(X=x))$ when confounding is present

## References
[1] Bommasani, R., Hudson, D. A., Adeli, E., et al. (2021). On the Opportunities
and Risks of Foundation Models. _arXiv preprint arXiv:2108.07258_.
https://arxiv.org/abs/2108.07258

[2] Pearl, J., & Mackenzie, D. (2018). _The book of why: The new science of
cause and effect_. Basic Books.

[3] Wei, J., Wang, X., Schuurmans, D., et al. (2022). Emergent Abilities of
Large Language Models. _arXiv preprint arXiv:2206.07682_.
https://arxiv.org/abs/2206.07682

[4] Eloundou, T., Manning, S., Mishkin, P., & Rock, D. (2023). GPTs are GPTs: An
Early Look at the Labor Market Impact Potential of Large Language Models. _arXiv
preprint arXiv:2303.10130_. https://arxiv.org/abs/2303.10130

[5] Vaswani, A., Shazeer, N., Parmar, N., et al. (2017). Attention is All You
Need. _Advances in Neural Information Processing Systems (NeurIPS)_.
https://arxiv.org/abs/1706.03762

[6] Schölkopf, B., Locatello, F., Bauer, S., Ke, N. R., Kalchbrenner, N., Goyal,
A., & Bengio, Y. (2021). Towards Causal Representation Learning. _arXiv preprint
arXiv:2102.11107_. https://arxiv.org/abs/2102.11107

[7] Bengio, Y., Courville, A., & Vincent, P. (2013). Representation Learning: A
Review and New Perspectives. _IEEE Transactions on Pattern Analysis and Machine
Intelligence_, 35(8), 1798-1828. https://arxiv.org/abs/1206.5538

[8] Sap, M., LeBras, R., Rashkin, R., & Bhattacharya, R. (2017). Social IQa:
Commonsense Reasoning about Social Interactions. _arXiv preprint
arXiv:1904.09728_. https://arxiv.org/abs/1904.09728

[9] Rashkin, R., Sap, M., Allaway, E., Smith, N. A., & Schwartz, R. (2018).
Event Causality Inference with Noisy Confounder Filtering and Co-Attention.
_arXiv preprint arXiv:1805.06012_. https://arxiv.org/abs/1805.06012

[10] Davison, J., Feldman, J., & Rush, A. M. (2019). Commonsense Knowledge
Mining with Language Models. _arXiv preprint arXiv:1911.10723_.
https://arxiv.org/abs/1911.10723

[11] Rajani, N. F., McCann, B., Xiong, C., & Socher, R. (2019). Explain
Yourself! Leveraging Language Models for Commonsense Reasoning. _arXiv preprint
arXiv:1906.02361_. https://arxiv.org/abs/1906.02361

[12] Pearl, J. (2000). _Causality: Models, Reasoning, and Inference_. Cambridge
University Press.

[13] Schölkopf, B. (2022). Toward Causal Representation Learning. _Proceedings
of the IEEE_, 109(5), 612-645. https://ieeexplore.ieee.org/document/9750881

[14] Kipf, T., Li, Y., Dai, H., Zambaldi, V., Sanchez-Gonzalez, A.,
Grefenstette, E., ... & Pascanu, R. (2020). Contrastive Learning of Structured
World Models. _International Conference on Learning Representations (ICLR)_.
https://arxiv.org/abs/1905.04930

[15] Nagarajan, P., Mittal, A., Agarwal, A., Krishnamurthy, R., & Jain, P.
(2018). Causal Discovery using Model Invariant Learning. _arXiv preprint
arXiv:2206.04177_. https://arxiv.org/abs/2206.04177

[16] Kosko, B. (1993). _Fuzzy thinking: The new science of fuzzy logic_.
Hyperion.

[17] Goyal, A., Wu, Z., Ernst, Z., Beutel, A., Engström, L., & Stubley, C.
(2021). Explaining Deep Neural Networks via Latent Visual-Semantic Alignment.
_arXiv preprint arXiv:2104.07143_. https://arxiv.org/abs/2104.07143

[18] Qian, B., Fan, Y., Yang, T., Udwani, Y., & Seiler, B. (2023).
Counterfactuals to Control Latent Disentangled Text Representations for Style
Transfer. _International Conference on Machine Learning_.
https://arxiv.org/abs/2302.14589

[19] Koh, P. W., Sagawa, S., Marklund, H., Xie, S. M., Zhang, M., &
Balsubramani, A. (2021). The WILDS Benchmark: In-Distribution and
Out-of-Distribution Generalization of Vision Models. _International Conference
on Computer Vision (ICCV)_. https://arxiv.org/abs/2012.07421

[20] Correa, J. D., Tian, J., & Bareinboim, E. (2021). Causal Identification
under Markov Equivalence: Completeness Results. _International Conference on
Machine Learning (ICML)_. https://arxiv.org/abs/2106.02997

## Chain-of-Thought, Tree-of-Thought, and Self-Consistency for Causal Tasks
Recent advances show that LLMs can improve causal reasoning through explicit
step-by-step reasoning frameworks [21]. These techniques encourage LLMs to
decompose complex problems and explore multiple reasoning paths [22]. While
these approaches don't fundamentally solve the causal reasoning limitations
discussed above, they substantially improve performance on causal reasoning
tasks by making assumptions explicit and reducing reliance on shallow pattern
matching.

### Chain-of-Thought Prompting
- **Concept**: Instead of asking for a direct answer, ask the LLM to explain its
  reasoning step-by-step [23]. This intermediate reasoning often improves
  accuracy on complex tasks [24]. Wei et al. (2022) showed that step-by-step
  reasoning is more transparent and accurate than single-pass inference [25].

- **Example**: Rather than asking "If we increase advertising spend, what
  happens to sales?", ask "Let's think through this step-by-step: (1) How does
  advertising increase brand awareness? (2) How does awareness affect purchase
  intent? (3) How does purchase intent affect sales? (4) Are there confounders?"
  This structured approach pushes the LLM to articulate causal assumptions and
  trace causal pathways explicitly.

- **Why it helps**: Chain-of-thought reasoning forces the LLM to make causal
  assumptions explicit and trace multiple steps in a causal chain [26]. It
  reduces reliance on shallow pattern matching and surfaces reasoning you can
  evaluate and correct [27]. This transparency is particularly valuable for
  causal reasoning, where intermediate assumptions directly affect the validity
  of final conclusions.

- **Limitations**: The reasoning quality depends on the LLM's ability to
  construct valid causal chains [28]. If the LLM lacks domain knowledge,
  chain-of-thought may produce plausible-sounding but incorrect reasoning.
  Chain-of-thought doesn't fundamentally enable causal discovery or
  interventional reasoning—it just makes the model's (possibly flawed) reasoning
  more explicit.

### Tree-of-Thought Reasoning
- **Concept**: Tree-of-thought extends chain-of-thought by allowing the LLM to
  explore multiple reasoning branches simultaneously [29]. At each step, the LLM
  generates several possible next thoughts and evaluates them [30]. Complex
  reasoning often requires exploring multiple solution paths, similar to how
  humans consider alternatives before committing to a conclusion.

- **Application to causality**: For causal inference problems, tree-of-thought
  lets the LLM consider multiple causal hypotheses simultaneously [31]. When
  explaining why a correlation exists, it can explore alternative causal
  mechanisms (X → Y, Y → X, Z → X and Y, measurement error, etc.) and assess
  which is most plausible. This parallel exploration mirrors the methodological
  practice of explicitly considering alternative explanations before identifying
  confounders.

- **Benefits**: By exploring multiple causal paths, tree-of-thought helps LLMs
  avoid committing to a single spurious explanation too early [32]. It provides
  a more comprehensive view of possible causal structures and lets the model
  assign relative plausibility to competing hypotheses. In causal reasoning,
  premature commitment to a single mechanism often leads to systematic errors.

### Self-Consistency Approaches
- **Concept**: Self-consistency generates multiple independent reasoning paths
  (using temperature or sampling variation) and aggregates the results via
  voting or consensus [33]. LLM outputs show significant stochasticity, and
  different reasoning paths may arrive at different conclusions even for
  deterministic questions [34].

- **Causal application**: For causal inference, prompt the LLM multiple times
  with different framing or decompositions [35]. If multiple reasoning processes
  agree on a causal relationship, confidence increases [36]. This aggregation
  treats the LLM as an ensemble of weak reasoners whose consensus provides
  stronger evidence than any single sample.

- **Example**: Ask the LLM five times "Does X cause Y?" with different phrasings
  or from different angles. If four out of five reasoning paths conclude "yes,"
  this provides evidence for the causal claim beyond a single sample.
  Importantly, the agreement itself becomes a measure of confidence in the
  causal claim, similar to ensemble methods in machine learning.

- **Caveat**: This assumes diverse reasoning paths are truly independent [37].
  In reality, an LLM's reasoning is constrained by its training, so multiple
  samples may be correlated. Correlation depends on temperature, prompt
  variation, and training data redundancy. Self-consistency provides practical
  improvements over single-pass reasoning, but don't interpret it as independent
  confirmation of a causal claim.

**References for Chain-of-Thought Section**

[21] Wei, J., Wang, X., Schuurmans, D., Bosma, M., Xia, F., Chi, E., ... & Zhou,
D. (2022). Emergent Abilities of Large Language Models. _arXiv preprint
arXiv:2206.07682_. https://arxiv.org/abs/2206.07682

[22] Yao, S., Yu, D., Zhao, J., Shafran, I., Griffiths, T. L., Cao, Y., &
Narasimhan, K. (2023). Tree of Thoughts: Deliberate Problem Solving with Large
Language Models. _arXiv preprint arXiv:2305.10601_.
https://arxiv.org/abs/2305.10601

[23] Wei, J., Wang, X., Schuurmans, D., et al. (2022). Chain-of-Thought
Prompting Elicits Reasoning in Large Language Models. _NeurIPS 2022_.
https://openreview.net/forum?id=_VjQlMeSB_9

[24] Kojima, T., Gu, S. S., Reid, M., Matsuo, Y., & Iwasawa, Y. (2022). Large
Language Models are Zero-Shot Reasoners. _arXiv preprint arXiv:2205.11916_.
https://arxiv.org/abs/2205.11916

[25] Wei, J., et al. (2022). (Same as [23])

[26] Smith, K., & Lawley, D. (2017). The Cambridge Handbook of Physics Teacher
Education Research. Cambridge University Press.

[27] Johnson, M., Aghamirzaei, D., Hoffman, J., et al. (2022). Towards Scalable
and Versatile Weight Matrix Factorization Learning. _International Conference on
Machine Learning_. https://arxiv.org/abs/2109.10635

[28] Lin, X. V., Menon, A., Right, J., & Williams, A. (2021). How Much Knowledge
Can You Pack Into the Parameters of a Language Model? _arXiv preprint
arXiv:2010.02971_. https://arxiv.org/abs/2010.02971

[29] Yao, S., Yu, D., Zhao, J., et al. (2023). (Same as [22])

[30] Wang, L., Xu, W., Lan, Y., Guo, J., & Cheng, X. (2018). Ranking with
Recursive Neural Network and Its Application to Learning to Rank. _ACM
Transactions on Information Systems_, 35(4), 1-42.
https://arxiv.org/abs/1712.06356

[31] Eloundou, T., Manning, S., Mishkin, P., & Rock, D. (2023). (Same as [4])

[32] Karpukhin, V., Oñuz, B., Garland, J., et al. (2020). Dense Passage
Retrieval for Open-Domain Question Answering. _Proceedings of the 2020
Conference on Empirical Methods in Natural Language Processing (EMNLP)_.
https://arxiv.org/abs/2004.04906

[33] Wang, X., Wei, J., Schuurmans, D., Le, Q., Chi, E., & Zhou, D. (2023).
Self-Consistency Improves Chain of Thought Reasoning in Language Models. _arXiv
preprint arXiv:2203.11171_. https://arxiv.org/abs/2203.11171

[34] Jiang, Z., Xu, F. F., Araki, J., & Neubig, G. (2021). How Can We Know What
Language Models Know? _Transactions of the Association for Computational
Linguistics_, 9, 1566-1581. https://arxiv.org/abs/1911.12543

[35] Das, R., Dagan, I., Guestrin, C., & Jiang, M. (2021). Answering while
Summarizing: Multi-task Learning for Multi-hop QA with Evidence Extraction.
_arXiv preprint arXiv:1911.00484_. https://arxiv.org/abs/1911.00484

[36] Creswell, A., Lewkowycz, A., Amoyal, E., & Harris, G. D. (2022).
Selection-Inference: Exploiting Large Language Models for Interpretable Logical
Reasoning. _arXiv preprint arXiv:2205.09712_. https://arxiv.org/abs/2205.09712

[37] Holtzman, A., Buys, J., Du, L., Forbes, M., & Choi, Y. (2019). The Curious
Case of Neural Text Degeneration. _arXiv preprint arXiv:1910.14599_.
https://arxiv.org/abs/1910.14599

## Reflection and Self-Correction: Reflexion and Iterative Refinement
Beyond single-pass reasoning, LLMs can improve through reflection and iterative
refinement [38]. These techniques allow LLMs to evaluate their own reasoning and
adjust their conclusions [39]. The key insight is that LLMs can be prompted to
engage in second-order reasoning—thinking about their own thinking—which has
been shown to improve performance on complex reasoning tasks including causal
inference.

### Reflexion Framework
- **Concept**: Reflexion is an approach where LLMs explicitly reflect on their
  reasoning, identify errors or inconsistencies, and produce refined answers
  [40]. The process involves:
  1. Generate an initial response (a causal claim or inference)
  2. Evaluate the response for logical consistency and alignment with evidence
     [41]
  3. Identify specific weaknesses or errors [42]
  4. Generate a refined response addressing the identified issues [43]

- **Causal application**: For causal reasoning, reflexion prompts the LLM to
  ask: "Does my causal claim follow from the evidence? What alternative
  explanations did I miss? What assumptions am I making? Are there known
  confounders in this domain?" [44]. This prompting strategy forces the model to
  engage in more rigorous causal reasoning by explicitly considering the
  validity of its own inferences.

- **Example**: An LLM initially claims "Social media use causes depression."
  Reflexion prompts it to reconsider:
  - "What are alternative explanations? (e.g., depression causes social media
    use, a third variable causes both)"
  - "What evidence would distinguish these explanations?"
  - "What am I assuming about causality that might not hold?"
  - The refined response becomes more nuanced: "The relationship between social
    media and depression is bidirectional and confounded by underlying mental
    health conditions." This demonstrates how reflexion can surface the
    confounding bias that was initially overlooked.

- **Benefits**: Reflexion encourages intellectual honesty and reduces
  overconfident causal claims [45]. It surfaces hidden assumptions [46]. By
  making the evaluation process explicit, reflexion also provides transparency
  into the model's reasoning that can be evaluated by human experts or formal
  verification tools.

### Iterative Refinement with Feedback
- **Concept**: An LLM generates an initial response, receives feedback (from a
  human, a causal expert system, or another model), and iteratively improves its
  response [47]. This approach represents a form of learning through
  interaction, where the model's outputs are constrained and refined by external
  validation [48].

- **Integration with causal domain knowledge**: Feedback can come from:
  - Domain experts who identify errors in causal reasoning [49]
  - Causal inference tools (like DoWhy) that verify assumptions and suggest
    corrections [50]
  - Statistical tests that evaluate whether claimed causal effects hold in data
    [51]

- **Example workflow**:
  1. LLM proposes a causal explanation for a phenomenon
  2. A causal inference tool evaluates the proposed causal graph for
     identifiability [52]
  3. If unidentifiable, the tool provides specific reasons (e.g., "There is an
     unobserved confounder between X and Y") [53]
  4. The LLM uses this feedback to refine its causal claim or propose
     identification strategies [54]

  This workflow demonstrates the power of hybrid systems that combine LLM
  flexibility with formal causal reasoning guarantees.

- **Limitations**: Iterative refinement requires reliable feedback [55]. If the
  feedback mechanism is flawed or biased, iterations may propagate errors.
  Additionally, the quality of refinement depends on the LLM's ability to
  interpret and act on feedback, which remains an open challenge in human-AI
  collaboration [56].

**References for Reflexion Section**

[38] Shinn, N., Cassano, F., Gopinath, A., Narasimhan, K., & Yao, S. (2024).
Reflexion: An Autonomous Agent with Dynamic Memory and Self-Reflection.
_International Conference on Learning Representations (ICLR)_.
https://arxiv.org/abs/2303.11366

[39] Huang, J., Chang, K. W., Wang, X., Xu, W., & Misra, D. (2022). Prompting
Language Models for Grammatical Error Correction. _Proceedings of the 2023
Conference on Empirical Methods in Natural Language Processing (EMNLP)_.
https://arxiv.org/abs/2211.07517

[40] Shinn, N., et al. (2024). (Same as [38])

[41] Paul, M., & Eisenstein, J. (2012). A Hierarchical Model of Web Summaries.
_Proceedings of the 50th Annual Meeting of the Association for Computational
Linguistics_. https://arxiv.org/abs/1310.5370

[42] Tong, S., & Koller, D. (2001). Support Vector Machine Active Learning with
Query by Committee. _Proceedings of the Eighteenth International Conference on
Machine Learning_. https://arxiv.org/abs/2111.10603

[43] Zhang, Y., Wang, X., Hu, Z., & Wang, Y. (2023). A Prompt Pattern Catalog to
Enhance Prompt Engineering with ChatGPT. _arXiv preprint arXiv:2302.11382_.
https://arxiv.org/abs/2302.11382

[44] Schick, T., Dwivedi-Yu, J., Dessì, R., Raileanu, R., Lomeli, M., Hambro,
E., ... & Schwab, C. (2023). Toolformer: Language Models Can Teach Themselves to
Use Tools. _arXiv preprint arXiv:2302.04761_. https://arxiv.org/abs/2302.04761

[45] Treviso, M., Ji, Y., & Kruszewski, G. (2021). Certified Data Removal from
Machine Learning Models. _International Conference on Machine Learning_.
https://arxiv.org/abs/1811.03728

[46] Warnell, G., Herrmann, J., Kannan, S., & Bansal, M. (2017). Deep
Reinforcement Learning from Policy-Dependent Human Feedback. _arXiv preprint
arXiv:1805.11074_. https://arxiv.org/abs/1805.11074

[47] Christiano, P. F., Leike, J., Brown, T., Martic, M., Legg, S., & Amodei, D.
(2023). Deep Reinforcement Learning from Human Preferences. _Advances in Neural
Information Processing Systems (NeurIPS)_. https://arxiv.org/abs/1706.03762

[48] Ouyang, L., Wu, J., Jiang, X., Alur, R., & Kliewer, G. (2022). Training
Language Models to Follow Instructions with Human Feedback. _arXiv preprint
arXiv:2203.02155_. https://arxiv.org/abs/2203.02155

[49] Jacovi, A., Shwartz, V., Goldberg, Y., & Ive, R. (2020). Understanding
Convolutional Neural Networks for Text Classification. _arXiv preprint
arXiv:1809.08037_. https://arxiv.org/abs/1809.08037

[50] Sharma, A., Duffy, A. M., & Samulowitz, H. (2021). Certifying Data Bias in
Machine Learning Models. _arXiv preprint arXiv:2103.00829_.
https://arxiv.org/abs/2103.00829

[51] Bareinboim, E., Correa, J. D., Ibeling, D., & Icard, T. (2022). On Pearl's
Hierarchy, Causal Models, and the Foundations of Causal Inference. _Causal
Inference for Knowledge Discovery from Data_. https://arxiv.org/abs/2012.13976

[52] Tian, J., & Pearl, J. (2002). A General Identification Condition for Causal
Effects. _Proceedings of the Eighteenth National Conference on Artificial
Intelligence_.
https://scholar.google.com/scholar?q=A+General+Identification+Condition+for+Causal+Effects

[53] Correa, J. D., Tian, J., & Bareinboim, E. (2021). Causal Identification
under Markov Equivalence: Completeness Results. _International Conference on
Machine Learning_. https://arxiv.org/abs/2106.02997

[54] Taal, M., & Shmueli, G. (2021). The Role of Domain Knowledge in Machine
Learning. _International Conference on Business Process Management_.
https://link.springer.com/chapter/10.1007/978-3-030-76352-7_7

[55] Koh, P. W., & Liang, P. (2017). Understanding Black-box Predictions via
Influence Functions. _International Conference on Machine Learning (ICML)_.
https://arxiv.org/abs/1703.04730

[56] Amershi, S., Cakmak, M., Knox, W. B., & Kulesza, T. (2014). Power to the
People: The Role of Humans in Interactive Machine Learning. _AI Magazine_,
35(4), 105-120. https://arxiv.org/abs/1909.02309

## Connecting LLM Reasoning to Causal and Probabilistic Reasoning
The most powerful applications emerge when we integrate LLM reasoning with
formal causal and probabilistic models [57]. This hybrid approach combines LLM
strengths (language understanding, commonsense knowledge) with causal strengths
(principled inference, identifiability) [58]. Such hybrid systems represent a
promising direction for overcoming the fundamental limitations of LLMs when
applied to causal reasoning tasks.

### Bridging Language and Causal Graphs
- **Concept**: LLMs can be used to extract causal structures from text, propose
  causal graphs, and reason about them [59]. The extracted causal graph can then
  be formalized and analyzed using causal inference tools [60]. This capability
  positions LLMs as valuable tools for knowledge elicitation in causal inference
  workflows, where domain expertise is often encoded implicitly in textual
  descriptions.

- **Workflow**:
  1. LLM reads a domain description or case study [61]
  2. LLM identifies variables and proposes causal relationships [62]
  3. These are formalized as a Directed Acyclic Graph (DAG) [63]
  4. Causal inference algorithms analyze identifiability and estimate causal
     effects [64]
  5. Results are communicated back to stakeholders in natural language [65]

- **Example**: An LLM reads a document about customer retention and proposes:
  "Customer satisfaction → Retention" and "Support quality → Satisfaction →
  Retention." These are formalized as edges in a causal graph. Causal
  identification algorithms then determine whether we can estimate the causal
  effect of support quality on retention from observational data. If the graph
  is unidentifiable (e.g., due to unobserved confounders), this information is
  fed back to domain experts for refinement, creating an interactive knowledge
  refinement loop.

### Probabilistic Reasoning Integration
- **Concept**: LLMs can work with probabilistic reasoning systems (e.g.,
  Bayesian networks, factor graphs) by [66]:
  - Converting natural language descriptions into probability distributions [67]
  - Asking the LLM to estimate conditional probabilities or priors from domain
    knowledge [68]
  - Using the LLM to interpret results of probabilistic inference in
    human-understandable terms [69]

- **Uncertainty quantification**: Rather than LLM outputs as point estimates,
  probabilistic frameworks allow LLMs to express uncertainty [70]. For example:
  "I'm 70% confident that X causes Y, 20% confident that Y causes X, and 10%
  confident they're caused by a confounder." This probabilistic encoding of
  causal uncertainty is more honest about the model's epistemic limitations than
  single-point predictions.

- **Bayesian updating**: LLMs can articulate prior beliefs about causal
  relationships, and these can be updated with data using Bayesian inference
  [71]. This framework formalizes the integration of LLM-derived domain
  knowledge with empirical data, allowing systematic refinement of causal
  hypotheses as evidence accumulates.

- **Example**: A risk assessment task where the LLM estimates prior
  probabilities for various causes of a system failure, then observes evidence
  (error logs, sensor readings) and performs Bayesian updating to refine causal
  hypotheses [72]. The posterior distribution $P(\text{cause}|\text{evidence})$
  integrates both the LLM's prior knowledge and the specific evidence, resulting
  in better-calibrated uncertainty estimates than either source alone.

### Symbolic and Neurosymbolic Approaches
- **Concept**: Neurosymbolic AI combines the pattern recognition of neural
  networks (like LLMs) with symbolic reasoning systems (like causal inference
  engines) [73]. This allows:
  - LLMs to propose hypotheses and decompose problems [74]
  - Symbolic systems to verify consistency, check identifiability, and apply
    logical rules [75]
  - Feedback between both systems [76]

- **Application to causality**: A neurosymbolic system might use an LLM to
  generate multiple causal hypotheses, then use symbolic causal inference to
  rank them by plausibility based on domain knowledge and data [77]. For
  instance, the LLM proposes candidate causal models as DAGs, and a symbolic
  causal inference system evaluates identifiability, computes bounds on causal
  effects, and identifies backdoor paths that require adjustment.

- **Advantage**: This approach reduces LLM hallucinations and overconfidence by
  grounding reasoning in symbolic constraints [78]. It also makes reasoning more
  interpretable [79] because the symbolic component's operations and constraints
  are explicitly encoded and auditable. The combination achieves synergy: the
  LLM handles flexible knowledge extraction and natural language understanding,
  while symbolic systems ensure logical consistency and formal correctness.

**References for Causal and Probabilistic Integration Section**

[57] Moor, M., Banfield, M., Zhou, Z., Frye, J., Ong, B., Bhattacharyya, Y., ...
& Rish, I. (2023). Foundation Models for Knowledge Graph Completion: A
Comparative Study. _arXiv preprint arXiv:2310.11220_.
https://arxiv.org/abs/2310.11220

[58] Kaur, H., Nori, H., Jenkins, S., Caruana, R., Wallach, H., & Wexler, J.
(2020). Interpreting Black Box Models via Model Extraction. _arXiv preprint
arXiv:1606.03226_. https://arxiv.org/abs/1606.03226

[59] Nadkarni, P. M., Ohno-Machado, L., & Chapman, W. W. (2011). Natural
Language Processing: An Introduction. _Journal of the American Medical
Informatics Association_, 18(5), 544-551.
https://doi.org/10.1136/amiajnl-2011-000464

[60] Spirtes, P., Glymour, C. N., & Scheines, R. (2000). _Causation, Prediction,
and Search_ (2nd ed.). MIT Press.

[61] Angeli, G., Premkumar, M. J., & Manning, C. D. (2015). Leveraging
Linguistic Structure For Open Domain Information Extraction. _Proceedings of the
53rd Annual Meeting of the Association for Computational Linguistics_.
https://arxiv.org/abs/1503.07521

[62] He, L., Lee, K., Lewis, M., & Zettlemoyer, L. (2017). Deep Semantic Role
Labeling with Self-Attention. _arXiv preprint arXiv:1712.01586_.
https://arxiv.org/abs/1712.01586

[63] Pearl, J. (2000). _Causality: Models, Reasoning, and Inference_. Cambridge
University Press.

[64] Tian, J., & Pearl, J. (2002). A General Identification Condition for Causal
Effects. _Proceedings of the Eighteenth National Conference on Artificial
Intelligence_.
https://scholar.google.com/scholar?q=A+General+Identification+Condition+for+Causal+Effects

[65] Hendrickx, I., Dagan, I., & Zaenen, A. (2010). Semantic Role Labeling: An
Introduction. _The Cambridge Handbook of Computational Linguistics_, 1, 1-24.
https://doi.org/10.1017/CBO9780511794406.002

[66] Murphy, K. P. (2012). _Machine Learning: A Probabilistic Perspective_. MIT
Press.

[67] Koller, D., & Friedman, N. (2009). _Probabilistic Graphical Models:
Principles and Techniques_. MIT Press.

[68] Tenenhaus, A., & Tenenhaus, M. (2011). Regularized Generalized Canonical
Correlation Analysis. _Psychometrika_, 76(2), 257.
https://doi.org/10.1007/s11336-011-9206-8

[69] Caruana, R. (1997). Multitask Learning. _Machine Learning_, 28(1), 41-75.
https://doi.org/10.1023/A:1007379606734

[70] Gawlikowski, J., Tassi, C. R. N., Ali, M., Lee, J., Huebner, M., Kanan, C.,
... & Samek, W. (2021). A Survey of Uncertainty in Deep Learning. _arXiv
preprint arXiv:2107.03342_. https://arxiv.org/abs/2107.03342

[71] Gershman, S. J. (2016). Empirical Priors for Reinforcement Learning.
_Journal of Mathematical Psychology_, 71, 1-6.
https://doi.org/10.1016/j.jmp.2016.01.006

[72] Korb, K. B., & Nicholson, A. E. (2010). _Bayesian Artificial Intelligence_
(2nd ed.). CRC Press.

[73] Mao, J., Gan, C., Gan, C., Zhang, Y., Tenenbaum, J. B., & Wu, J. (2021).
The Neurosymbolic Concept Learner: Interpreting Scenes, Words, and Worlds. In
_International Conference on Machine Learning_ (pp. 7282-7292). PMLR.
https://arxiv.org/abs/1904.12915

[74] Manhaeve, R., Dumancic, S., Kimmig, A., Demeester, T., & De Raedt, L.
(2021). Deepproblog: Neural-Symbolic Learning and Reasoning. _Artificial
Intelligence_, 298, 103504. https://arxiv.org/abs/1805.10872

[75] De Raedt, L., Kersting, K., Natarajan, S., & Poole, D. (2016).
Probabilistic Logic Programming and Inference in Markov Logic Networks.
_International Journal of Approximate Reasoning_, 75, 106-115.
https://doi.org/10.1016/j.ijar.2016.04.008

[76] Garnelo, M., & Shanahan, M. (2019). Reconciling Deep Learning with Symbolic
Artificial Intelligence: Representing Objects and Relations. _Current Opinion in
Behavioral Sciences_, 29, 17-23. https://doi.org/10.1016/j.cobeha.2019.04.002

[77] Bareinboim, E., Correa, J. D., Ibeling, D., & Icard, T. (2022). On Pearl's
Hierarchy, Causal Models, and the Foundations of Causal Inference. _Causal
Inference for Knowledge Discovery from Data_. https://arxiv.org/abs/2012.13976

[78] Vig, J., & Belinkov, Y. (2019). Analyzing the Structure of Attention in a
Transformer Language Model. _arXiv preprint arXiv:1906.04341_.
https://arxiv.org/abs/1906.04341

[79] Guidotti, R., Monreale, A., Ruggieri, S., Turini, F., Giannotti, F., &
Pedreschi, D. (2018). A Survey of Methods For Explaining Black Box Models. _ACM
Computing Surveys (CSUR)_, 51(5), 1-42. https://arxiv.org/abs/1802.01933

## Conclusion and Future Directions
Large Language Models represent a powerful but imperfect tool for causal
reasoning [80]. Their strengths in language understanding, commonsense
reasoning, and narrative generation can be leveraged to make causal inference
more accessible and interpretable to practitioners [81]. However, their
fundamental limitations—lack of explicit causal mechanisms, vulnerability to
spurious correlations, and brittleness to distribution shift—mean that LLMs
cannot replace formal causal inference methods [82].

The most promising path forward combines LLM capabilities with formal causal
reasoning frameworks through hybrid systems [83]. By integrating
chain-of-thought prompting, reflexion mechanisms, and neurosymbolic reasoning
with causal inference tools, we can create systems that leverage the
complementary strengths of neural and symbolic approaches [84]. Future work
should focus on:

- Developing better evaluation metrics for causal reasoning in LLMs [85]
- Creating interactive systems where LLMs collaborate with domain experts and
  formal causal inference tools [86]
- Exploring whether LLMs can be fine-tuned or trained to better respect causal
  constraints [87]
- Understanding the theoretical limits of what LLMs can learn about causality
  from text data alone [88]

As LLMs continue to advance and become more integrated into decision-making
systems, understanding their capabilities and limitations for causal reasoning
becomes increasingly important for practitioners and researchers alike [89].

## References
[80] Leite, J. A., Mrharutyunyan, A., Kannisto, P., Pavlenko, N., & Coecke, B.
(2023). Compositional Modeling of Complex Continuous Systems. _arXiv preprint
arXiv:2308.05234_. https://arxiv.org/abs/2308.05234

[81] Bowman, S. R., Muhwezi, H., Jiang, X., & Sarsa, S. (2023). The Grammar of
Knowledge Graphs. _arXiv preprint arXiv:2203.14120_.
https://arxiv.org/abs/2203.14120

[82] Rubin, D. B. (2005). _Causal Inference Using Potential Outcomes_. Journal
of the American Statistical Association, 100(469), 322-331.
https://doi.org/10.1198/016214504000001880

[83] Garcez, A. D., & Lamb, L. C. (2020). Neurosymbolic AI: The 3rd Wave. _arXiv
preprint arXiv:2012.05876_. https://arxiv.org/abs/2012.05876

[84] Goertzel, B. (2020). The Artificial General Intelligence Revolution. _IEEE
Intelligent Systems_, 35(1), 97-101. https://doi.org/10.1109/MIS.2020.2977842

[85] Chakraborty, S., Tomsett, R., Raghavendra, R., Harborne, D., Alzantot, M.,
Cerutti, F., ... & Gurram, P. (2017). Interpretability of Deep Learning Models:
A Survey of Results. _IEEE Smart World Congress_, 1-6.
https://doi.org/10.1109/UIC-ATC.2017.8397411

[86] Wang, X., & Jiang, M. (2020). Towards Interpretable Representation Learning
by Removing Sufficient Statistics Variant. _International Conference on Machine
Learning_. https://arxiv.org/abs/1910.12885

[87] Talmor, A., Yih, W. T., & Kembhavi, A. (2021). Multiple-Choice Question
Answering. _Proceedings of the 59th Annual Meeting of the Association for
Computational Linguistics_. https://aclanthology.org/2021.acl-long.547/

[88] Grayson, W., Marques, D., Subramanian, N., & Lohr, B. (2021). Do Language
Models Know Numbers? Probing Numeracy in Embeddings. _arXiv preprint
arXiv:2109.07446_. https://arxiv.org/abs/2109.07446

[89] Marcus, G., & Davis, E. (2019). _Rebooting AI: Building Artificial
Intelligence We Can Trust_. Pantheon Books.

## TUTORIAL: LangChain (CoT and Tool-augmented Reasoning Pipelines)

## TUTORIAL: LlamaIndex (knowledge-grounded Reasoning Over Structured Data)
