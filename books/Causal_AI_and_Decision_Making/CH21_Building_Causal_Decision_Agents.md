# Building Causal Decision Agents

Autonomous agents must make decisions in complex, uncertain environments.[1] Traditional agents use reactive rules or learned value functions, but they often lack principled reasoning about cause and effect.[2] Causal decision agents integrate causal models explicitly into their decision-making processes, enabling them to reason about interventions, plan under uncertainty, and adapt to distribution shifts.[3] This chapter explores architectures for causal decision agents, methods for integrating causal models into action selection, and the challenges of real-world deployment with multiple agents and human oversight.

## Agent Architectures: Reactive, Deliberative, Causal

Agent architectures vary in their complexity and reasoning capabilities.[4] Understanding the spectrum from reactive to causal agents helps clarify what each approach can and cannot achieve.

### Reactive Agents

- **Definition**: Reactive agents respond directly to sensory inputs with actions, following condition-action rules (stimulus-response).[5] They have minimal or no internal state and no explicit planning.

- **Mechanism**: Condition-action rules map observations to actions.[6] For example: "If battery low → seek charging station" or "If obstacle ahead → turn left."

- **Advantages**:
  - Simple and fast: minimal computational overhead
  - Robust to some environmental changes: if rules are sufficiently general[7]
  - Easy to understand and debug: rules are explicit

- **Limitations**:
  - No planning: cannot foresee consequences of actions beyond immediate rewards
  - No counterfactual reasoning: cannot ask "what if I do X instead of Y?"[8]
  - Brittle to distribution shift: rules that worked in training may fail in new situations[9]
  - Cannot reason about causal chains: if multiple conditions affect the same goal, reactive agents cannot distinguish between independent causes

- **Example**: A robot that reactively follows objects when they appear and stops when they disappear. This works in controlled settings but fails if an object moves behind an obstacle—the robot cannot reason that the object still exists and will reappear.

### Deliberative Agents
- **Definition**: Deliberative agents maintain an internal model of the world,
  plan sequences of actions, and execute those plans. They use explicit
  reasoning to anticipate consequences and select actions.

- **Mechanism**:
  1. Perceive the current state
  2. Build or update an internal world model
  3. Plan a sequence of actions using this model
  4. Execute the plan
  5. Monitor outcomes and replan if needed

- **Planning methods**:
  - Classical planning (STRIPS, PDDL): logical preconditions and effects
  - Hierarchical planning (HTN): decompose high-level goals into subgoals
  - Graph search: A\*, heuristic search over state spaces
  - Reinforcement learning: learn value functions or policies from experience

- **Advantages**:
  - Foresight: can anticipate consequences multiple steps ahead
  - Flexibility: plans can adapt to unexpected changes
  - Explainability: planning steps reveal the agent's reasoning
  - Handles novel situations: generalizable world models can work in new
    contexts

- **Limitations**:
  - Computational complexity: planning scales poorly with state/action space
    size
  - Requires accurate models: planning relies on correct world model; wrong
    models lead to bad plans
  - Still no explicit causality: planning models capture transitions (what
    happens next) but not causal mechanisms (why it happens)
  - Struggles with hidden confounders: standard planning assumes full
    observability or uses probability, but cannot distinguish causation from
    correlation

- **Example**: A robot planning to rearrange furniture. It uses a model of
  physics and spatial layout to plan a sequence of moves. However, if the model
  is wrong (e.g., misestimates friction), the plan may fail.

### Causal Agents
- **Definition**: Causal agents explicitly reason about causal mechanisms. They
  maintain causal models (e.g., causal graphs, structural causal models) and use
  causal inference to select actions that will achieve goals.

- **Mechanism**:
  1. Represent the domain as a causal model (DAG, SCM, or causal graph)
  2. Observe data and perform causal inference (identifiability, estimation)
  3. When selecting an action (intervention), reason about its consequences
     using do-calculus or other causal inference methods
  4. Choose actions that maximize expected utility, accounting for hidden
     confounders and feedback loops

- **Causal capabilities**:
  - Interventional reasoning: "If I do(X=x), what happens to Y?"
  - Counterfactual reasoning: "Given that I observed Z, if I had done(X=x')
    instead, what would have happened?"
  - Distinguishing causation from correlation: can identify spurious
    associations and true causal effects
  - Handling distribution shift: causal models generalize to new distributions
    if the causal structure remains stable
  - Adapting to new environments: can quickly learn causal parameters in new
    settings

- **Advantages**:
  - Principled reasoning: decisions are grounded in causal mathematics
  - Robust to distribution shift: causal relationships are more stable than
    correlations
  - Explainability: causal reasoning provides clear explanations for decisions
    ("I chose this action because it has the largest causal effect on my goal")
  - Handles hidden confounders: causal inference can adjust for unmeasured
    confounders if identifiable
  - Enables transfer learning: causal models from one domain can be adapted to
    related domains

- **Limitations**:
  - Requires causal knowledge: must have domain expertise to specify causal
    structures
  - Identifiability challenges: not all causal effects are identifiable from
    available data
  - Computational complexity: causal inference and optimization can be
    computationally expensive
  - Model misspecification: if the true causal model differs from the agent's
    model, causal reasoning may be wrong
  - Limited real-world data: in many domains, we have limited interventional
    data to learn causal models

- **Example**: An autonomous vehicle makes decisions using a causal model of how
  weather, road conditions, and driver actions affect safety and fuel
  efficiency. When it observes rain, it reasons: "Rain causes reduced tire grip,
  which causes increased stopping distance. Therefore, I should increase
  following distance and reduce speed." This reasoning is grounded in causal
  mechanisms, not just correlations in historical driving data.

**References**

- Russel, S., & Norvig, P. (2020). _Artificial Intelligence: A Modern Approach_
  (4th ed.). Pearson.
- Wooldridge, M. (2009). _An Introduction to Multiagent Systems_ (2nd ed.). John
  Wiley & Sons.
- Pearl, J. (2009). _Causality: Models, Reasoning, and Inference_ (2nd ed.).
  Cambridge University Press.

## Integrating Causal Models Into Agent Action Selection
The key challenge in building causal agents is integrating causal reasoning into
the action selection mechanism. This requires formalizing how causal models
inform utility maximization.

### Causal Models as Action Guides
- **Concept**: The agent maintains a causal model of the domain represented as a
  Structural Causal Model (SCM) or causal graph. When selecting actions, the
  agent uses this model to predict consequences.

- **Formal setup**: Let the agent's state be represented by variables V = {V₁,
  V₂, ..., Vₙ}. The causal model specifies:
  - Structural equations: Vᵢ := fᵢ(PA(Vᵢ), Uᵢ), where PA(Vᵢ) are parents of Vᵢ
    in the causal graph and Uᵢ are unobserved factors
  - A goal variable or utility function U(V) that the agent aims to maximize
  - Available actions (interventions) that the agent can perform: do(X = x)

- **Action selection via do-calculus**:
  1. For each possible action a, compute the causal effect on the goal: P(U |
     do(a)) or E[Goal | do(a)]
  2. Select the action with the highest expected utility: a\* = argmax_a E[Goal
     | do(a)]
  3. Execute a\* and observe outcomes
  4. Update the causal model with new information

- **Example**: A clinical decision support system maintains a causal model of
  patient health:
  - Variables: symptom severity, test results, current medications, patient
    outcomes
  - Causal relationships: medication affects test results; severity and genetics
    affect response; side effects depend on dose and patient factors
  - Goal: maximize patient health while minimizing adverse effects
  - When deciding on a treatment, the system computes: E[health improvement |
    do(prescribe drug X at dose y)] and compares across treatment options

### Bayesian Approaches to Causal Action Selection
- **Concept**: Combine Bayesian inference (to handle uncertainty) with causal
  reasoning. The agent maintains a posterior distribution over causal models and
  averages action effects across this distribution.

- **Method**:
  1. Prior over causal models: P(M) (before observing data)
  2. Observe data: D
  3. Posterior: P(M | D) ∝ P(D | M) P(M)
  4. For each action a, compute posterior causal effect: E\_{M~P(M|D)}[Goal |
     do(a), M]
  5. Select: a\* = argmax*a E*{M~P(M|D)}[Goal | do(a), M]

- **Advantage**: Captures epistemic uncertainty (uncertainty about which causal
  model is correct). If multiple causal models are consistent with data, the
  agent considers all of them.

- **Challenge**: Posterior inference over causal models is computationally
  expensive, especially with large model classes.

### Learning Causal Models Online
- **Concept**: The agent does not start with a complete causal model. Instead,
  it learns causal relationships from observed interventions and outcomes.

- **Approaches**:
  - Causal discovery from interventional data: Use algorithms (FCI, GES, PC) to
    infer causal structure from experiment results
  - Active learning: Design interventions to maximally reduce uncertainty about
    causal structure
  - Adaptive experiments: Use Bayesian optimization to select actions that are
    both goal-maximizing and informative about causal relationships

- **Challenge - exploration-exploitation tradeoff**: Should the agent exploit
  what it knows about effective actions, or explore to learn the causal
  structure better? Optimal actions for immediate reward may not teach the agent
  about the underlying causal mechanisms.

- **Example**: A recommendation system learns which content types causally
  affect user engagement. Initially, it explores by showing diverse content and
  measuring engagement. Over time, it learns: "videos cause more engagement than
  text" and "personalized content causes higher return rates." The system then
  exploits this knowledge to recommend high-engagement content, while
  occasionally exploring new categories to detect changes in preferences.

**References**

- Imbens, G. W., & Wooldridge, J. M. (2009). Recent developments in the
  econometrics of program evaluation. _Journal of economic literature_, 47(1),
  5-86.
- Abbeel, P., & Ng, A. Y. (2004). Apprenticeship learning via inverse
  reinforcement learning. In _Proceedings of the Twenty-First International
  Conference on Machine Learning_ (p. 1).
- Beygelzimer, A., Dasgupta, S., & Langford, J. (2009). Importance weighted
  active learning. In _Proceedings of the 26th annual international conference
  on machine learning_ (pp. 49-56).

## Planning Under Causal Uncertainty
Real-world environments are uncertain. Even with a causal model, agents must
reason about what they don't know and make decisions that are robust to
uncertainty.

### Types of Uncertainty in Causal Models
- **Structural uncertainty**: Is the causal structure correct? For example, is
  it A → B → C or A ← B → C?
  - Risk: Wrong causal structure leads to wrong predictions
  - Mitigation: Causal discovery algorithms, domain expertise, sensitivity
    analyses

- **Parameter uncertainty**: Given the structure, are the parameters correct?
  For example, how large is the causal effect of A on B?
  - Risk: Effect sizes may be misestimated, leading to suboptimal actions
  - Mitigation: Confidence intervals, Bayesian posterior distributions, repeated
    estimation

- **Unobserved confounding**: Are there hidden variables that affect multiple
  observed variables?
  - Risk: Biased causal effect estimation
  - Mitigation: Sensitivity analyses, instrumental variables, regression
    discontinuity, or additional measurement

- **Measurement error**: Are the observed variables measured accurately?
  - Risk: Noisy observations weaken causal inference
  - Mitigation: Repeated measurements, validation, measurement models

### Robust Decision-Making Under Uncertainty
- **Concept**: Design agent policies that perform well across a range of
  possible causal models, rather than optimizing for a single model.

- **Maximin approach**: Find the action that maximizes the minimum expected
  utility across all plausible causal models:
  - A\* = argmax*a min*{M ∈ Plausible} E[Goal | do(a), M]
  - Conservative but robust: protects against worst-case scenarios

- **Expected utility with parameter uncertainty**: Average over the posterior
  distribution of causal parameters:
  - A\* = argmax_a ∫ E[Goal | do(a), θ] P(θ | data) dθ
  - Balances optimality and robustness

- **Sensitivity analysis**: For a chosen action, compute how sensitive the
  outcome is to assumptions about causal structure or parameters. If outcomes
  are sensitive to assumptions you're unsure about, reconsider the action.

- **Example**: A policy-maker must decide whether to increase police patrols to
  reduce crime. The causal effect of patrols on crime is uncertain (confidence
  interval: -5% to -15% crime reduction, depending on model assumptions). Under
  maximin, the decision-maker would choose patrols if the worst-case outcome
  (-5%) is still acceptable.

### Adaptive and Online Planning
- **Concept**: Rather than planning a fixed sequence of actions, the agent
  adapts its plan based on observed outcomes. This reduces the impact of
  planning errors.

- **Replanning**: After each action, observe the outcome, update beliefs about
  the causal model, and replan.
  - Advantage: Corrects for model errors as they're discovered
  - Cost: Replanning is computationally expensive

- **Contingency planning**: Plan conditional on possible outcomes. "If I observe
  X, I'll do Y; if I observe Z, I'll do W."
  - Advantage: Handles uncertainty proactively
  - Cost: Exponential branching factor

- **Information-gathering actions**: Some actions are taken primarily to reduce
  uncertainty, not to directly achieve goals. For example, running a diagnostic
  test to confirm a causal hypothesis.

**References**

- Lemieux, T., & Milligan, K. S. (2008). Assessing the impact of worker health
  insurance coverage on the engine of US economic growth. In _Improving health
  insurance and access to care_ (pp. 37-46). New York: Russell Sage Foundation.
- Rotnitzky, A., Lei, Q., Sued, M., & Robins, J. M. (2021). Improved
  double-robust estimation in observational studies with increased
  dimensionality. _arXiv preprint arXiv:2107.02304_.

## Multi-Agent Systems and Human-in-the-Loop
Real-world decision-making rarely involves a single agent in isolation. Multiple
agents interact, and humans must retain oversight and control. This section
addresses the challenges of scaling causal decision agents to multi-agent and
human-supervised settings.

### Multi-Agent Causal Reasoning
- **Challenge - agent interdependence**: When multiple agents act in the same
  environment, their actions affect each other. Causal reasoning must account
  for:
  - Other agents' goals, constraints, and capabilities
  - Feedback loops: Agent A's action affects Agent B's observations, which
    affects Agent B's actions, which affects Agent A
  - Equilibria: What happens when all agents optimize given each other's
    actions?

- **Game-theoretic causal reasoning**:
  - Causal models extend to multi-agent settings via causal games
  - Each agent has a causal model of how actions (its own and others') affect
    outcomes
  - Strategic interaction: agents reason about other agents' causal reasoning
    (theory of mind)
  - Nash equilibrium: agents reach a stable state where no agent wants to
    unilaterally deviate

- **Example - autonomous vehicles**: Multiple AVs share a road. Each AV
  maintains a causal model of how its actions (accelerate, brake, change lanes)
  affect collision risk and travel time. It must also reason about other AVs'
  causal reasoning. If it brakes hard, will the following vehicle also brake (to
  avoid collision) or accelerate (because it misunderstands)? The AV must
  coordinate to reach equilibrium where all agents safely coexist.

- **Communication and coordination**: Agents can exchange information about
  their causal models or intended actions, reducing harmful interactions:
  - Transparent sharing of causal models: "Here's how I reason about traffic
    safety"
  - Commitment to actions: "I plan to accelerate slowly; you can safely cut in
    front"
  - Negotiation over shared resources: "You get higher priority in the morning;
    I get it in the evening"

### Human-in-the-Loop Decision Making
- **Motivation**: Fully autonomous agents may fail in unexpected ways. Humans
  should retain control, especially for high-stakes decisions (medical, legal,
  financial). Human-in-the-loop systems combine human judgment with agent
  reasoning.

- **Levels of human involvement**:
  - **Full automation**: Agent decides and acts autonomously. Humans review
    outcomes
  - **Agent recommends, human decides**: Agent presents options and reasoning;
    human makes final decision
  - **Human sets goals/constraints, agent optimizes**: Human specifies
    objectives; agent finds best actions within constraints
  - **Collaborative**: Agent and human jointly reason about causal relationships
    and decide

- **Benefits of human oversight**:
  - Catches agent errors: humans may recognize causal mistakes or unrealistic
    assumptions
  - Values alignment: ensures agent actions align with human values and ethical
    constraints
  - Accountability: humans take responsibility for decisions, not agents
  - Improvement: human feedback helps the agent learn correct causal models

- **Challenges**:
  - Information overload: agents may generate too much information for humans to
    process
  - Time pressure: humans may lack time to thoroughly review agent reasoning
  - Trust and reliance: humans may over-trust agents (automation bias) or
    under-trust them (rejection bias)
  - Communication gap: agents' causal reasoning may be hard for humans to
    understand

- **Design practices**:
  - **Explainability**: Agent clearly explains its causal reasoning ("I chose
    this because X causes Y, and maximizing Y achieves your goal")
  - **Confidence indicators**: Agent signals uncertainty ("I'm 60% confident in
    this causal effect; consider alternatives")
  - **Anomaly detection**: Flag situations where agent reasoning differs from
    past patterns or violates assumptions
  - **Graceful degradation**: If humans disagree, agent adjusts its model and
    re-reasons ("You're right, let me reconsider given this new causal
    relationship")

- **Example - medical decision support**: A system recommends treatment options
  for a patient with multiple comorbidities. It presents:
  1. Causal reasoning: "Medication A causes reduction in blood pressure, which
     reduces stroke risk. However, it may cause kidney damage in 5% of patients
     with your condition. Medication B is safer but less effective."
  2. Trade-offs: "Choosing A maximizes life expectancy but increases side-effect
     risk. Choosing B is conservative. Which do you prefer?"
  3. Confidence: "My estimates are based on clinical trials with 85% confidence;
     individual variation is high."
  4. The physician makes the final decision, informed by the causal reasoning.

**References**

- Leite, I., Mohan, A., Natarajan, S., & Sap, M. (2022). Robots learning to
  teach humans about causal reasoning. _arXiv preprint arXiv:2206.02848_.
- Amershi, S., Cakmak, M., Knox, W. B., & Kulesza, T. (2014). Power to the
  people: The role of humans in interactive machine learning. _AI Magazine_,
  35(4), 105-120.
- Green, B., & Bansal, G. (2021). Authors shouldn't write alone: Revisiting
  research practices around explainability. _arXiv preprint arXiv:2104.07143_.

## TUTORIAL: ReAct (reasoning and Acting Framework for LLM Agents)

## TUTORIAL: LangChain + DoWhy (causal Model Integrated Into Agent Reasoning)