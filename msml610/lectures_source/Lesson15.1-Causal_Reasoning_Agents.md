::: columns
:::: {.column width=15%}
![](msml610/lectures_source/figures/UMD_Logo.png)
::::
:::: {.column width=75%}

\vspace{0.4cm}
\begingroup \large
MSML610: Advanced Machine Learning
\endgroup
::::
:::

\vspace{1cm}

\begingroup \Large
**$$\text{\blue{Lesson 15.1: Causal Reasoning Agents}}$$**
\endgroup
\vspace{1cm}

::: columns
:::: {.column width=65%}
**Instructor**: Dr. GP Saggese, [gsaggese@umd.edu](gsaggese@umd.edu)

**References**:

- Pearl, J.: _"The Book of Why"_ (2018)

- Pearl, J. & Mackenzie, D.: _"The Seven Pillars of Causal Reasoning"_ (2018)

- Bottou, L. et al.: _"From Machine Learning to Machine Reasoning"_ (2013)

::::
:::: {.column width=40%}

![](msml610/lectures_source/figures/book_covers/Book_cover_Book_of_why.jpg){ height=25% }

::::
:::

# ##############################################################################
# LLMs and Causal Reasoning
# ##############################################################################

// Books:
// - Pearl, J. (2009). "Causality: Models, Reasoning, and Inference" (2nd ed.)
//   https://bayes.cs.ucla.edu/BOOK-2K
// - Pearl, J., Glymour, M., & Jewell, N. P. (2016). "Causal Inference in Statistics: A Primer"
//   https://ftp.cs.ucla.edu/pub/stat_ser/r481.pdf

// Papers:
// - Spirtes, P., Glymour, C., & Scheines, R. (2000). "Causation, Prediction, and Search" (2nd ed.)
//   https://doi.org/10.7551/mitpress/1754.001.0001
// - Rubin, D. B. (1974). "Estimating causal effects of treatments in randomized and nonrandomized studies"
//   Journal of Educational Psychology, 66(5), 688-701
//   https://doi.org/10.1037/h0037350

## ##############################################################################
## LLMs: Strengths and Limitations
## ##############################################################################

// Papers:
// - Brown, T. B., Mann, B., Ryder, N., Subbiah, M., Kaplan, J., Dhariwal, P., ... & Amodei, D. (2020). 
//   "Language Models are Few-Shot Learners"
//   https://arxiv.org/abs/2005.14165
// - Hoffmann, J., Borgeaud, S., Mensch, A., Perez, E., Ramesh, A., Huang, Y., ... & Sifre, L. (2022).
//   "Training Compute-Optimal Large Language Models"
//   https://arxiv.org/abs/2203.15556
// - Kaplan, J., McCandlish, S., Henighan, T., Brown, T. B., Chess, B., Child, R., ... & Amodei, D. (2020).
//   "Scaling Laws for Neural Language Models"
//   https://arxiv.org/abs/2001.08361

* LLMs: Where They Excel

- Large Language Models excel at **pattern matching at scale**
  - Trained on massive text corpora to capture statistical regularities
  - Exceptional for prediction: $\Pr(\text{next token} | \text{history})$
  - Strong performance on language understanding, summarization, generation
  - World knowledge encoded through pretraining

- **Example**: Predicting the next word in _"The capital of France is ___"_ → easy

- Strengths:
  - Massive scale enables capturing complex statistical patterns
  - Transfer learning from pretraining to diverse downstream tasks
  - Few-shot learning through in-context examples

* LLMs: Critical Limitations

- LLMs fundamentally struggle with **explicit causal reasoning**
  - Pattern matching cannot distinguish correlation from causation
  - No built-in mechanism to reason about counterfactuals (what-if scenarios)
  - Cannot reliably predict interventions vs. observational data
  - Confounding variables not explicitly handled

- **Example**: Given _"Ice cream sales and drowning deaths both spike in summer"_, 
  an LLM may infer a causal link rather than recognizing temperature as a confounder

- Critical gaps:
  - **Intervention reasoning**: _"What if we increase X? How does Y change?"_
  - **Counterfactual reasoning**: _"What would have happened if the past were different?"_
  - **Causal discovery**: Learning causal structure from data
  - **Robustness to distribution shift**: Generalizing under causal changes

## ##############################################################################
## Pattern-Based Reasoning vs. Causal Reasoning
## ##############################################################################

// Papers:
// - Peters, J., Janzing, D., & Schölkopf, B. (2017). "Elements of Causal Inference: Foundations and Learning Algorithms"
//   https://mitpress.mit.edu/books/elements-causal-inference
// - Rotnitzky, A., & Robins, J. M. (2005). "Semiparametric regression adjustment to estimate policy effects"
//   Journal of the American Statistical Association, 100(469), 319-331
//   https://doi.org/10.1198/016214504000001646
// - Angrist, J. D., & Pischke, J. S. (2008). "Mostly Harmless Econometrics: An Empiricist's Companion"
//   https://economics.mit.edu/files/11869
// - Bottou, L., Peters, J., Quiñonero-Candela, J., Charles, X., Chickering, M., Garcez, A. D. D., ... & Zhang, K. (2013).
//   "Counterfactual reasoning and learning systems: The example of computational advertising"
//   Journal of Machine Learning Research, 14(11), 3207-3260
//   https://arxiv.org/abs/1209.0467

* Pattern Recognition and Its Limits

- **Pattern-based reasoning**: Learn $f: X \to Y$ from observed associations
  - Extract statistical regularities: what features predict outcomes
  - No understanding of _why_ these associations exist
  - Works perfectly in stationary environments

- **Causal reasoning**: Learn mechanisms—the underlying data-generating process
  - Understand _why_ X causes Y through explicit models
  - Transfer knowledge to new interventions and environments
  - Explain and debug failures

::: columns
:::: {.column width=50%}
**Pattern Matching**

- Pros
  - Scales with data quantity
  - Captures complex associations
  - Practical for stable settings

- Cons
  - Breaks under distribution shift
  - Cannot reason about interventions
  - Vulnerable to confounding
  - Opaque causal mechanisms
::::
:::: {.column width=50%}
**Causal Reasoning**

- Pros
  - Robust to distribution shift
  - Generalizes to new interventions
  - Interpretable mechanisms
  - Handles confounding

- Cons
  - Requires causal model specification
  - Sample complexity for learning
  - Stronger assumptions
::::
:::

* Robustness: When Pattern Matching Fails

- **Distribution shift**: When test data differs from training data
  - Spurious correlations learned during training don't hold in deployment
  - LLMs confidently make wrong predictions due to pattern reliance

- **Example**: Medical diagnosis
  - Training data: Hospital A diagnoses condition X using test Y
  - Hospital A had a faulty calibration: test Y strongly predicts diagnosis but not disease
  - Pattern-based model learns: high Y $\to$ condition X
  - New hospital with correct calibration: model fails spectacularly

- **Intervention robustness**: Actions that change the world
  - Feedback loops: recommending product A increases demand, changing patterns
  - Reward hacking: optimizing a proxy metric instead of true objective
  - Policy change: changing business rules invalidates historical patterns

- **Example**: Content recommendation
  - Pattern: users who engage with trending topics get recommended more trending
  - Intervention: change algorithm to reduce trending bias
  - Unintended consequence: recommendation patterns shift, breaking past associations

# ##############################################################################
# Enhancing LLM Reasoning with Causality
# ##############################################################################

// Papers:
// - Wei, J., Wang, X., Schuurmans, D., Bosma, M., Ichien, B., Xia, F., ... & Zhou, D. (2022).
//   "Emergent Abilities of Large Language Models"
//   https://arxiv.org/abs/2206.07682

## ##############################################################################
## Chain-of-Thought Prompting for Causal Reasoning
## ##############################################################################

// Papers:
// - Wei, J., Wang, X., Schuurmans, D., Bosma, M., Ichien, B., Xia, F., ... & Zhou, D. (2022).
//   "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models"
//   https://arxiv.org/abs/2201.11903
// - Kojima, T., Gu, S. S., Reid, M., Matsuo, Y., & Iwasawa, Y. (2022).
//   "Large Language Models are Zero-Shot Reasoners"
//   https://arxiv.org/abs/2205.11916
// - Yao, S., Yu, D., Zhao, J., Shafran, I., Griffiths, T. L., Cao, Y., & Narasimhan, K. (2023).
//   "Tree of Thoughts: Deliberate Problem Solving with Large Language Models"
//   https://arxiv.org/abs/2305.10601

* Chain-of-Thought Prompting: Structured Reasoning

- **Chain-of-thought (CoT)** encourages the model to break down complex reasoning
  - Instead of: _"Q: Does X cause Y?"_ → Direct answer
  - CoT: _"Let me think step by step..."_ → Intermediate reasoning steps

- How it helps with causal reasoning:
  - Forces explicit consideration of mechanisms
  - Enables backtracking and correction of errors
  - Makes assumptions and reasoning transparent
  - Allows verification of causal logic

- **Example**: CoT for causal inference
  ```
  Q: "If we increase advertising budget, will sales increase?"
  
  CoT: "Let me think about this:
  1. Advertising increases brand awareness (mechanism)
  2. Brand awareness increases purchase intent (mechanism)
  3. Purchase intent leads to sales (mechanism)
  4. But we should also check for confounders...
     (Are we only increasing budget in growing markets?)
  5. And feedback loops: Does higher sales justify more spending?"
  ```

- Limitations of plain CoT:
  - Still pattern-based, not mechanistic
  - Can rationalize incorrect causal claims
  - Doesn't ground reasoning in data or formal causal models

* Causal Prompting Frameworks

- **Structured causal prompts** guide explicit causal reasoning
  - What are the variables involved?
  - What are the causal relationships? (DAG or causal graph)
  - What are the confounders?
  - What are the identifying assumptions?

- **Example**: Structured causal prompt template
  ```
  Problem: [description]
  
  Variables:
  - Treatment: [what are we intervening on?]
  - Outcome: [what do we care about?]
  - Confounders: [what common causes exist?]
  
  Causal structure: [draw or describe relationships]
  
  Identification strategy: [how do we isolate the causal effect?]
    - Assumption 1: [e.g., no unmeasured confounding]
    - Assumption 2: [e.g., positivity/overlap]
    - Assumption 3: [e.g., no feedback loops]
  
  Conclusion: [the causal effect is...]
  ```

## ##############################################################################
## Integrating Causal and Probabilistic Frameworks
## ##############################################################################

// Books:
// - Pearl, J. (1988). "Probabilistic Reasoning in Intelligent Systems: Networks of Plausible Inference"
//   https://doi.org/10.1016/B978-0-08-051489-5.50008-4
// - Koller, D., & Friedman, N. (2009). "Probabilistic Graphical Models: Principles and Techniques"
//   https://mitpress.mit.edu/books/probabilistic-graphical-models

// Papers:
// - Janzing, D., & Schölkopf, B. (2010). "Causal inference using invariant prediction: identification and outlook"
//   Journal of The Royal Statistical Society Series B, 77(5), 1015-1048
//   https://arxiv.org/abs/1304.4877
// - Nowak-Brzezińska, A., & Xięski, T. (2020). "Causal Bayesian Networks"
//   In: Yin, H., et al. IDEAL 2017. IDEAL 2017. Lecture Notes in Computer Science, vol 10585.
// - Richards, B. A., Lillicrap, T. P., Beaudoin, P., Bengio, Y., Bogacz, R., Christensen, A., ... & Zambaldi, V. (2019).
//   "A deep learning framework for neuroscience"
//   Nature Neuroscience, 22(11), 1761-1770
//   https://doi.org/10.1038/s41593-019-0520-2

* Connecting LLMs to Formal Causal Models

- **Gap between LLMs and causal inference**:
  - LLMs: black-box functions trained on text
  - Causal inference: formal models with explicit assumptions and identifiability

- **Integration strategy**: Use LLM for reasoning, ground in causal frameworks
  - LLM as semantic engine: interpret domain knowledge, generate hypotheses
  - Causal model as reasoning engine: formal inference, constraint checking
  - Probabilistic framework as uncertainty quantifier: propagate uncertainty

- **Example**: Causal reasoning for policy evaluation
  - LLM input: _"We're considering a new hiring policy. What are potential causal effects?"_
  - LLM output: Proposes causal graph with treatment (policy), outcome (hiring equity)
  - Causal inference: Estimates causal effects using observed data under identifying assumptions
  - Uncertainty quantification: Confidence intervals accounting for assumptions

* Bayesian Networks and Causal DAGs

- **Causal DAG** (Directed Acyclic Graph): represents causal relationships
  - Nodes: variables (treatments, outcomes, confounders, mediators)
  - Directed edges: causal influences
  - Absence of edge: no direct causal effect

- **Example**: Educational intervention causal DAG
  ```graphviz
  digraph CausalDAG {
      splines=true;
      nodesep=1.0;
      ranksep=0.75;
      rankdir=LR;

      node [shape=box, style="rounded,filled", fontname="Helvetica", fontsize=11, penwidth=1.4];

      SES [label="Socioeconomic\nStatus", fillcolor="#FFD1A6"];
      SchoolQuality [label="School\nQuality", fillcolor="#FFD1A6"];
      Tutorial [label="Tutorial\nProgram", fillcolor="#F4A6A6"];
      StudentMotiv [label="Student\nMotivation", fillcolor="#B2E2B2"];
      TestScore [label="Test\nScore", fillcolor="#A6C8F4"];

      SES -> SchoolQuality;
      SES -> StudentMotiv;
      SchoolQuality -> Tutorial [label="  Selection"];
      StudentMotiv -> Tutorial;
      Tutorial -> TestScore;
      StudentMotiv -> TestScore;
      SchoolQuality -> TestScore;

      { rank=same; SES; SchoolQuality; }
  }
  ```

- Key concepts:
  - **Confounder**: variable with arrows to both treatment and outcome
  - **Mediator**: variable on causal path from treatment to outcome
  - **Collider**: variable with incoming arrows from multiple causes

* Tool Use: Integrating Causal Inference into LLM Workflows

- **Tool use paradigm**: LLM as reasoner, external tools as executors
  - LLM decides what reasoning to perform
  - Tools execute causal inference, simulation, or statistical analysis
  - Results feed back into LLM for further reasoning

- **Available tools for causal reasoning**:
  - Causal discovery tools: learn causal structure from data
  - Causal effect estimation: ATE (Average Treatment Effect), heterogeneous effects
  - Counterfactual simulation: what-if predictions under assumed causal model
  - Sensitivity analysis: robustness to assumption violations

- **Example**: LLM-guided causal analysis workflow
  ```
  1. LLM reads domain knowledge and data description
  2. LLM proposes causal DAG
  3. LLM selects identification strategy (e.g., matching, instrumental variables)
  4. Tool executes: estimates causal effect from data
  5. Tool output: point estimate, confidence interval, sensitivity checks
  6. LLM interprets: what does this estimate tell us about the intervention?
  7. LLM explains: what are the key assumptions and their plausibility?
  ```

- Benefits:
  - Explicit reasoning is interpretable and verifiable
  - Formal guarantees and assumptions are transparent
  - Tool outputs ground LLM claims in data
  - Failures are diagnostic rather than opaque

# ##############################################################################
# Causal Agent Architectures
# ##############################################################################

// Papers:
// - Schaal, S., Ijspeert, A., & Billard, A. (2003). "Computational approaches to motor learning by imitation"
//   Philosophical Transactions of the Royal Society B: Biological Sciences, 358(1431), 537-547
//   https://doi.org/10.1098/rstb.2003.1257
// - Precup, D., Teh, Y. W., & Welling, M. (2017). "Reinforcement learning with unsupervised auxiliary tasks"
//   In: International Conference on Learning Representations (ICLR)
//   https://arxiv.org/abs/1611.05397

## ##############################################################################
## Agents with Explicit Causal Models
## ##############################################################################

// Papers:
// - Pearl, J. (2019). "The Book of Why: The New Science of Cause and Effect"
// - Dasgupta, I., Wang, S. A., Chiappa, S., Ortega, J., Raposo, D., Hughes, E., ... & Leibo, J. Z. (2019).
//   "Causal reasoning from meta-reinforcement learning"
//   In: International Conference on Learning Representations (ICLR)
//   https://arxiv.org/abs/1901.08162
// - Mnih, V., Kavukcuoglu, K., & Silver, D. (2013). "Learning play representations from match graphs"
//   In: International Conference on Machine Learning (ICML)
// - Hafner, D., Dreyer, T., & Ba, J. (2023). "Mastering Atari, Go, Chess and Shogi by Planning with a Learned World Model"
//   https://arxiv.org/abs/2104.06294

* Causal Reasoning Agents: Design

- **Goal**: Build agents that can reason causally about the world and act robustly
  - Maintain an explicit causal model of the environment
  - Use causal inference to evaluate proposed actions
  - Update causal beliefs as new evidence arrives
  - Adapt behavior when causal assumptions are violated

- **Agent components**:
  - **Causal model**: formal representation of how actions affect outcomes
  - **Observational data**: what the agent observes in the environment
  - **Inference engine**: computes causal effects and counterfactuals
  - **Planning module**: selects actions to achieve goals
  - **Learning module**: updates causal model from experience

* Causal Agent Architecture (1/2)

```graphviz
digraph CausalAgent {
    splines=true;
    nodesep=1.0;
    ranksep=0.75;

    node [shape=box, style="rounded,filled", fontname="Helvetica", fontsize=11, penwidth=1.4];

    WorldModel [label="Causal Model\n(DAG + SCM)", fillcolor="#A6C8F4"];
    Observations [label="Observations\nfrom Env", fillcolor="#FFD1A6"];
    Inference [label="Causal\nInference", fillcolor="#A0D6D1"];
    Planning [label="Planning &\nDecision Making", fillcolor="#F4A6A6"];
    Action [label="Action\nExecution", fillcolor="#B2E2B2"];

    { rank=same; WorldModel; Observations; }
    { rank=same; Inference; Planning; }

    Observations -> Inference;
    WorldModel -> Inference;
    Inference -> Planning;
    Planning -> Action;
    Action -> Observations [label="  Environment\nFeedback"];
    Observations -> WorldModel [label="  Learning"];
}
```

* Causal Agent Architecture (2/2)

- **Causal model** represents assumptions about mechanisms
  - Structural Causal Model (SCM): $Y := f_Y(PA_Y, U_Y)$ for each variable
  - Parameters: effect sizes, functional forms
  - Uncertainty: distributions over possible models or parameters

- **Inference module** answers causal queries
  - $\Pr(Y | do(X = x))$ : effect of intervention X on Y
  - $Y_{x'} = f_Y(x', U_Y)$ : counterfactual outcomes
  - Effect heterogeneity: how effects differ across populations

- **Planning module** optimizes over actions
  - Evaluate action $a$ by computing: $\EE[U | do(a)]$ where U is utility
  - Consider robustness: What if my causal model is wrong?
  - Explore vs. exploit: Balance testing assumptions vs. maximizing reward

- **Learning module** updates the model
  - Fit parameters to observed data
  - Test causal assumptions (Markov, faithfulness)
  - Detect model misspecification

## ##############################################################################
## Integrating Causal Inference into Planning
## ##############################################################################

// Papers:
// - Puterman, M. L. (1994). "Markov Decision Processes: Discrete Stochastic Dynamic Programming"
//   https://doi.org/10.1002/9780470316887
// - Bareinboim, E., & Pearl, J. (2016). "Causal inference and the data-fusion problem"
//   Proceedings of the National Academy of Sciences, 113(27), 7345-7352
//   https://arxiv.org/abs/1412.3608
// - Buesing, L., Weber, T., Racanière, S., Eslami, S. M. A., Pfaff, T., Czarnecki, J. M., & Pascanu, R. (2018).
//   "Learning and Policy Search in Stochastic Dynamical Systems with Bayesian Neural Networks"
//   In: International Conference on Learning Representations (ICLR)
//   https://arxiv.org/abs/1805.12114
// - Ivgi, S., Berant, J., & Globerson, A. (2022). "Causal Effect Inference with Deep Latent-Variable Models"
//   In: Neural Information Processing Systems (NeurIPS)
//   https://arxiv.org/abs/2205.06934

* Planning Under Causal Uncertainty

- **Core challenge**: Agent's causal model may be wrong
  - True world has causal structure agent doesn't know
  - Agent must choose actions using possibly incorrect model
  - Need policies that work well even under model misspecification

- **Robust planning approaches**:
  - **Conservatism**: prefer actions with robust effects across models
  - **Exploration**: test uncertain causal assumptions through action
  - **Adaptation**: update causal model as new evidence arrives
  - **Sensitivity analysis**: quantify robustness to assumption violations

* Markov Decision Processes (MDPs) with Causal Structure

- **Standard MDP**: $M = \langle \mathcal{S}, \mathcal{A}, P, R \rangle$
  - State space, action space, transition dynamics, reward function
  - Dynamics may embed causal structure implicitly

- **Causal MDP**: explicitly model causal mechanisms
  - Variables $X = (X_1, \ldots, X_n)$ that evolve over time
  - Actions intervene on specific variables
  - Rewards depend on achievable states
  - Transition: $X_t' := f(X_t, A_t, \varepsilon_t)$ (causal functions)

- **Example**: Medical treatment sequential decision
  - Variables: $(Patient\_Severity, Treatment, Patient\_Outcome)$
  - Action: choose treatment type
  - Outcome: health improvement (depends on severity + treatment)
  - Causal structure: Treatment has different effects for different severity levels

* Value Functions and Causal Effects

- **Standard RL**: value function $V(s) = \EE[\sum_t \gamma^t r_t | s_0 = s]$

- **Causal RL**: value function accounts for causal effects
  - $V(s) = \EE[R | do(A = a^*), S = s]$ where $a^*$ is optimal action
  - Policies must account for how actions change world state
  - Offline learning: learn from historical data with unknown confounding

- **Q-function with causal effects**:
  $$Q(s, a) = \Pr(\text{Reward} | do(A = a), S = s)$$

  - Standard RL assumes: $\Pr(\text{next state} | a, s) = P(s' | a, s)$ (known transition)
  - Causal RL must infer: Does $a$ actually cause $s'$, or is $s$ a confounder?

* Policy Robustness: Worst-Case Planning

- **Robust planning**: find policy that performs well under model uncertainty
  - Let $\Theta$ be set of possible causal models
  - Robust value: $V_{\text{robust}}(s) = \max_a \min_{\theta \in \Theta} Q_\theta(s, a)$
  - Guarantees: policy works even if true model is worst-case

- **Uncertainty sets**:
  - Parameter uncertainty: effect sizes could be different
  - Structural uncertainty: causal graph might be different
  - Identification uncertainty: causal effects may be unidentified

- **Example**: Drug dosage decision under causal uncertainty
  - Low dose vs. high dose: which is safer?
  - Risk: high dose might have nonlinear side effects we haven't modeled
  - Robust policy: start with conservative low dose, observe response, adapt

# ##############################################################################
# Trustworthy AI Through Causality
# ##############################################################################

// Papers:
// - Molnar, C. (2019). "Interpretable Machine Learning: A Guide for Making Black Box Models Explainable"
//   https://christophm.github.io/interpretable-ml-book/
// - Lipton, Z. C. (2018). "The Mythos of Model Interpretability"
//   Communications of the ACM, 61(10), 35-43
//   https://arxiv.org/abs/1606.03490

## ##############################################################################
## Transparency and Interpretability
## ##############################################################################

// Papers:
// - Ribeiro, M. T., Singh, S., & Guestrin, C. (2016). "Why Should I Trust You?: Explaining the Predictions of Any Classifier"
//   In: ACM SIGKDD Conference on Knowledge Discovery and Data Mining (KDD)
//   https://arxiv.org/abs/1602.04938
// - Sundararajan, M., & Najmi, A. (2020). "The many Shapley values for model explanation"
//   In: International Conference on Machine Learning (ICML)
//   https://arxiv.org/abs/1908.08474
// - Miller, T. (2019). "Explanation in artificial intelligence: Insights from the social sciences"
//   Journal of Artificial Intelligence Research, 67, 181-200
//   https://arxiv.org/abs/1706.07269
// - Caswell, I., & Liang, B. (2020). "Recent Advances and Clinical Applications of Deep Learning in Medical Image Analysis"
//   IEEE Reviews in Biomedical Engineering, 14, 194-217

* Making Reasoning Explicit and Interpretable

- **Opacity problem**: Black-box AI systems are hard to trust and debug
  - Neural networks: uninterpretable high-dimensional feature spaces
  - LLMs: billions of parameters, unclear what's being reasoned
  - Consequences: hard to catch failures before deployment

- **Causal transparency**: explicit mechanisms make reasoning visible
  - Causal graph: clear representation of assumed relationships
  - Causal effects: quantify impact of each decision
  - Counterfactuals: explain decisions by contrasting what-ifs

- **Example**: Loan approval decision
  - Black-box: Model says _"Loan denied"_ (opaque)
  - Causal: Model says _"Loan denied because credit score drops effect on default rate by 15%, controlling for income and employment"_ (transparent)

* Causal Explanations for Decisions

- **Contrastive explanations**: Why A rather than B?
  - Not just why A happened, but what would need to change for B instead

- **Recourse**: How can someone affected by decision change the outcome?
  - Requires causal model: what actions lead to decision reversal?
  - Fairness concern: recourse may be impossible if requirements are correlated with protected attributes

- **Example**: Hiring decision
  - Denial reason (non-causal): _"You have fewer years of experience"_
  - Causal recourse: _"Adding 2 years of experience would likely change decision, but experience is correlated with age, raising fairness concerns"_

- **Feature importance from causality**:
  - Not correlation (feature co-varies with outcome) $\to$ confounding
  - True causal importance: direct effect on outcome under intervention

## ##############################################################################
## Robustness Through Causal Constraints
## ##############################################################################

// Papers:
// - Goodfellow, I. J., Shlens, J., & Szegedy, C. (2014). "Explaining and Harnessing Adversarial Examples"
//   https://arxiv.org/abs/1412.6572
// - Papernot, N., McDaniel, P., Goodfellow, I., Jha, S., Celik, Z. B., & Swami, A. (2016).
//   "Practical Black-Box Attacks against Machine Learning"
//   In: ACM Asia Conference on Computer and Communications Security (ASIACCS)
//   https://arxiv.org/abs/1602.02697
// - Schott, L., Rauber, J., Bethge, M., & Brendel, W. (2019). "Towards the first adversarially robust neural network model on MNIST"
//   In: International Conference on Learning Representations (ICLR)
//   https://arxiv.org/abs/1805.09190
// - Scholkopf, B., Janzing, D., Peters, J., Sgarbossa, E., Zech, K., & Muandet, K. (2021).
//   "Toward Causal Representation Learning"
//   Proceedings of the IEEE, 109(5), 612-633
//   https://arxiv.org/abs/2102.11107

* Finding Brittle Decisions Through Causal Analysis

- **Brittleness**: decisions that break under small perturbations
  - Spurious correlations learned by pattern-based models
  - Vulnerable to adversarial examples or distribution shift
  - Often due to unrecognized confounding in training data

- **Causal analysis uncovers brittleness**:
  - Compare learned patterns to causal ground truth
  - Identify decisions driven by spurious correlations
  - Test robustness under causal interventions

- **Example**: Recidivism prediction (criminal justice)
  - Pattern learned: arrest history strongly predicts re-offense
  - Causal truth: arrest history may be proxy for policing patterns, not criminality
  - Brittleness: model fails if policing patterns change (different neighborhood, different police policy)

* Causal Constraints on Model Predictions

- **Constraint approach**: restrict model to predictions consistent with causal knowledge
  - Hard constraints: must enforce causal assumptions (e.g., no effect if no mechanism)
  - Soft constraints: penalize predictions violating causal knowledge
  - Helps prevent spurious patterns from being learned

- **Monotonicity constraints**: if treatment increases, outcome can't decrease
  - E.g., more education should not decrease earnings
  - Helps prevent absurd predictions

- **Structural constraints**: encode causal DAG
  - Variable A cannot affect B if no directed path A $\to$ B
  - Reduces model flexibility but increases robustness

* Adversarial Robustness with Causal Models

- **Adversarial examples**: small input perturbations that fool models
  - Pattern-based models: vulnerable because they rely on associations
  - Causal models: more robust because mechanisms are explicit

- **Causal adversarial robustness**:
  - Only perturbations along causal edges can meaningfully affect outcome
  - Confounded perturbations (correlating with true causes) are benign
  - Helps distinguish real threats from spurious ones

## ##############################################################################
## Fairness Through Causal Reasoning
## ##############################################################################

// Papers:
// - Kusner, M. J., Loftus, J., Russell, C., & Silva, R. (2017). "Counterfactual Fairness"
//   In: Advances in Neural Information Processing Systems (NeurIPS)
//   https://arxiv.org/abs/1705.10264
// - Hardt, M., Price, E., & Srebro, N. (2016). "Equality of Opportunity in Supervised Learning"
//   In: Advances in Neural Information Processing Systems (NeurIPS)
//   https://arxiv.org/abs/1610.02413
// - Nabi, R., & Shpitser, I. (2018). "Fair inference through semiparametric-efficient estimation over constraint-specific paths"
//   In: Advances in Neural Information Processing Systems (NeurIPS)
//   https://arxiv.org/abs/1806.09055
// - Zhang, B. H., Lemoine, B., & Mitchell, M. (2018). "Mitigating Unwanted Biases with Adversarial Learning"
//   In: AIES '18: Conference on AI Ethics and Society
//   https://arxiv.org/abs/1801.07593
// - Barocas, S., Hardt, M., & Narayanan, A. (2019). "Fairness and Machine Learning"
//   https://fairmlbook.org

* Causal Approaches to Bias and Discrimination

- **Fairness challenge**: what does it mean to treat people fairly?
  - Statistical parity: outcomes equally distributed across groups
  - Causal fairness: no discrimination through causal mechanisms

- **Three sources of group differences**:
  1. **Direct discrimination**: causal effect of protected attribute (illegal)
  2. **Indirect discrimination**: protected attribute causes unprotected predictor which causes outcome
  3. **Structural discrimination**: system perpetuates historical inequities

- **Example**: Hiring fairness
  - Protected: gender
  - Potential discriminator: field of study (may be correlated with gender)
  - Question: can we use field of study if it correlates with gender?
  - Causal answer: depends on whether field of study is a barrier to entry or just different productivity

* Causal Definitions of Fairness

- **Counterfactual fairness** (Kusner et al.):
  - Decisions would be same if protected attribute were different
  - Requires model of how protected attribute influences other variables
  - Strong requirement: may be too restrictive in practice

- **Path-specific effects** (decompositional approach):
  - Decompose total effect into direct (discriminatory) and indirect
  - Allow indirect effects if not caused by discrimination
  - More nuanced: separates correlation from causation

- **Example**: Gender wage gap
  - Total gap: women earn 20% less
  - Causal decomposition:
    - Direct effect: 5% unexplained by occupation/experience (discrimination)
    - Indirect effect: 15% via occupational segregation (structural inequity)

* Causal Constraints for Fair Models

- **Fairness through constraints**:
  - Control for mediators: adjust for variables on causal path
  - Balance confounders: ensure treatment and control groups similar on confounders
  - Remove selection bias: correct for how samples were selected

- **Example**: College admissions fairness
  - Constraint: admission decision should not depend on applicant's gender
  - But gender may have influenced GPA (indirect path)
  - Solution: directly adjust for GPA (mediator) if you believe it's fair predictor
  - Or: use causal effect of gender on success (counterfactual score) instead of observed score

## ##############################################################################
## Safety Through Causal Reasoning
## ##############################################################################

// Papers:
// - Amodei, D., Olah, C., Steinhardt, J., Christiano, P., Schulman, J., & Mané, D. (2016).
//   "Concrete Problems in AI Safety"
//   https://arxiv.org/abs/1606.06565
// - Soares, N., & Fallenstein, B. (2017). "Agent Foundations for Artificial General Intelligence"
//   In: The Technological Singularity
//   https://intelligence.org/files/Foundations.pdf
// - Everitt, T., Leike, J., & Hutter, M. (2018). "Sequential Extensions of Causal Models"
//   In: International Conference on Machine Learning (ICML)
//   https://arxiv.org/abs/1807.10470
// - Taylor, J., Levin, E., & Krebs, G. B. (2016). "The AI Alignment Problem"
//   In: The Technological Singularity
// - Hendrycks, D. (2023). "Natural and Artificial Intelligence"
//   Accessed at: https://arxiv.org/abs/2307.04187

* Causal Constraints on Harmful Outcomes

- **Safety challenge**: prevent AI systems from causing harm
  - Specification problem: hard to enumerate all bad outcomes
  - Unintended consequences: system optimizes for stated goal but harms something else
  - Feedback loops: system's actions change the world in unexpected ways

- **Causal approach**: model how system's actions affect harms
  - Identify causal paths to bad outcomes
  - Prohibit or mitigate interventions on these paths
  - Monitor for emergence of new causal pathways

- **Example**: Content recommendation safety
  - Harm: radicalization through information bubbles
  - Causal path: algorithm optimizes for engagement $\to$ recommends extreme content $\to$ radicalizes users
  - Safeguard: constraint that algorithm cannot increase polarization score

* Transparency for Trustworthy Autonomy

- **Autonomous systems and trust**:
  - Humans must understand and trust system decisions
  - Black-box autonomy is high-risk (medical decisions, criminal justice, military)
  - Causal reasoning provides transparency

- **Causal explanations for actions**:
  - Why did agent take action A?
  - What causal model led to this decision?
  - What would have to change for different action?
  - What assumptions could be wrong?

- **Human-in-the-loop with causality**:
  - Agent proposes action with causal justification
  - Human reviews: are assumptions correct? Are harms mitigated?
  - Human can override: here's a causal reason why that's wrong
  - Iterative refinement of agent's causal model

* Causal Monitoring and Adaptation

- **Deployment robustness**: system must work even when deployed
  - Distribution shift: world changes from training environment
  - Causal monitoring: detect when causal assumptions are violated
  - Adapt: update model or trigger human oversight

- **Causal anomaly detection**:
  - Expected relationship: $Y = f(X) + \varepsilon$
  - Observe: $Y$ deviates from expectation
  - Diagnosis: Is it random noise, confounding, or violation of causal mechanism?
  - Response: retrain, debug, or alert human

- **Example**: Medical treatment effectiveness monitoring
  - Deployed model: drug X increases recovery by 30%
  - Observation: new patient cohort shows only 10% improvement
  - Diagnosis: new cohort is older, has comorbidities
  - Causal monitoring: heterogeneous effect analysis reveals drug less effective for elderly
  - Adaptation: patient stratification in treatment recommendations

# ##############################################################################
# Summary and Key Takeaways
# ##############################################################################

// Books:
// - Pearl, J., & Mackenzie, D. (2018). "The Book of Why: The New Science of Cause and Effect"
//   Basic Books. ISBN: 978-0465097609
// - Peters, J., Janzing, D., & Schölkopf, B. (2017). "Elements of Causal Inference: Foundations and Learning Algorithms" (2nd ed.)
//   MIT Press. https://mitpress.mit.edu/books/elements-causal-inference

// Papers:
// - Schölkopf, B., Locatello, F., Bauer, S., Ke, N. R., Kalchbrenner, N., Goyal, A., & Bengio, Y. (2021).
//   "Toward Causal Representation Learning"
//   Proceedings of the IEEE, 109(5), 612-633
//   https://arxiv.org/abs/2102.11107
// - Brendel, W., Rauber, J., & Bethge, M. (2018). "Decision-based adversarial attacks: reliable attacks against machine learning models"
//   In: International Conference on Learning Representations (ICLR)
//   https://arxiv.org/abs/1712.04248

* Causal Reasoning for Trustworthy AI

- **Core insight**: LLMs excel at pattern matching but fail at causal reasoning
  - Pattern-based decisions break under distribution shift and interventions
  - Causal models provide robustness through explicit mechanisms

- **Integration strategy**: combine LLM strengths with causal frameworks
  - LLM reasoning + causal tools + explicit models = trustworthy AI
  - Tool use enables grounding claims in data and formal inference

- **Causal agent architectures**:
  - Explicit causal models in reasoning and planning
  - Planning under uncertainty with robustness
  - Adaptive learning from experience

- **Four pillars of trustworthy AI through causality**:
  1. **Transparency**: explicit mechanisms are interpretable
  2. **Robustness**: causal constraints prevent brittle decisions
  3. **Fairness**: causal decomposition separates discrimination from structure
  4. **Safety**: causal monitoring and constraints prevent harms

* The Path Forward

- Building trustworthy autonomous agents requires:
  - Making causal assumptions explicit
  - Testing these assumptions with data
  - Integrating formal inference into decision-making
  - Monitoring deployed systems for causal violations

- Open challenges:
  - Learning causal models from limited data
  - Reasoning under causal uncertainty
  - Balancing transparency with complexity
  - Scaling causal inference to high-dimensional problems

- Key message: _"AI systems that reason causally are fundamentally more trustworthy, transparent, and robust than pure pattern-matching approaches."_
