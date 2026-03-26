# Building Causal Decision Agents

# Summary
- Autonomous agents must make decisions in complex, uncertain environments[1]
- Traditional agents use reactive rules or learned value functions, but lack
  principled reasoning about cause and effect[2]
- Causal decision agents integrate causal models explicitly into their
  decision-making processes, enabling:
  - Reasoning about interventions
  - Planning under uncertainty
  - Adaptation to distribution shifts[3]
- This chapter explores:
  - Architectures for causal decision agents
  - Methods for integrating causal models into action selection
  - Challenges of real-world deployment with multiple agents and human oversight

## Agent Architectures: Reactive, Deliberative, Causal
Agent architectures vary in their complexity and reasoning capabilities.[4]
Understanding the spectrum from reactive to causal agents helps clarify what
each approach can and cannot achieve.

### Reactive Agents
- **Definition**: Reactive agents respond directly to sensory inputs with
  actions, following condition-action rules (stimulus-response).[5] They have
  minimal or no internal state and no explicit planning

- **Mechanism**: Condition-action rules map observations to actions[6]
  - Example: "If battery low → seek charging station"
  - Example: "If obstacle ahead → turn left"

- **Advantages**:
  - Simple and fast with minimal computational overhead
  - Robust to some environmental changes if rules are sufficiently general[7]
  - Easy to understand and debug with explicit rules

- **Limitations**:
  - No planning: cannot foresee consequences of actions beyond immediate rewards
  - No counterfactual reasoning: cannot ask "what if I do X instead of Y?"[8]
  - Brittle to distribution shift: rules that worked in training may fail in new
    situations[9]
  - Cannot reason about causal chains: cannot distinguish between independent
    causes affecting the same goal

- **Example**: A robot that reactively follows objects when they appear and
  stops when they disappear
  - Works in controlled settings
  - Fails if an object moves behind an obstacle—the robot cannot reason that the
    object still exists and will reappear

### Deliberative Agents
- **Definition**: Deliberative agents maintain an internal model of the world,
  plan sequences of actions, and execute those plans[10]. They use explicit
  reasoning to anticipate consequences and select actions

- **Mechanism**:
  1. Perceive the current state
  2. Build or update an internal world model
  3. Plan a sequence of actions using this model
  4. Execute the plan
  5. Monitor outcomes and replan if needed

- **Planning methods**:
  - Classical planning (STRIPS, PDDL)[11]: logical preconditions and effects
  - Hierarchical planning (HTN)[12]: decompose high-level goals into subgoals
  - Graph search[13]: A\*, heuristic search over state spaces
  - Reinforcement learning[14]: learn value functions or policies from
    experience

- **Advantages**:
  - Foresight: can anticipate consequences multiple steps ahead[15]
  - Flexibility: plans can adapt to unexpected changes
  - Explainability: planning steps reveal the agent's reasoning
  - Handles novel situations with generalizable world models that work in new
    contexts

- **Limitations**:
  - Computational complexity: planning scales poorly with state/action space
    size[16]
  - Requires accurate models: wrong models lead to bad plans[17]
  - Still no explicit causality[18]: planning models capture transitions (what
    happens next) but not causal mechanisms (why it happens)
  - Struggles with hidden confounders[19]: cannot distinguish causation from
    correlation

- **Example**: A robot planning to rearrange furniture using a model of physics
  and spatial layout
  - Plans a sequence of moves
  - Fails if the model is wrong (e.g., misestimates friction)

### Causal Agents
- **Definition** = Causal agents explicitly reason about causal mechanisms[20].
  They maintain causal models (e.g., causal graphs, structural causal
  models)[21] and use causal inference to select actions that will achieve goals

- **Mechanism**:
  1. Represent the domain as a causal model (DAG, SCM, or causal graph)[22]
  2. Observe data and perform causal inference (identifiability, estimation)[23]
  3. When selecting an action (intervention), reason about its consequences
     using do-calculus[24] or other causal inference methods
  4. Choose actions that maximize expected utility, accounting for hidden
     confounders and feedback loops[25]

- **Causal capabilities**:
  - Interventional reasoning[26]: "If I do(X=x), what happens to Y?"
  - Counterfactual reasoning[27]: "Given that I observed Z, if I had done(X=x')
    instead, what would have happened?"
  - Distinguishing causation from correlation[28]: can identify spurious
    associations and true causal effects
  - Handling distribution shift[29]: causal models generalize to new
    distributions if the causal structure remains stable
  - Adapting to new environments[30]: can quickly learn causal parameters in new
    settings

- **Advantages**:
  - Principled reasoning[31]: decisions are grounded in causal mathematics
  - Robust to distribution shift[32]: causal relationships are more stable than
    correlations
  - Explainability[33]: causal reasoning provides clear explanations for
    decisions
  - Handles hidden confounders[34]: causal inference can adjust for unmeasured
    confounders if identifiable
  - Enables transfer learning[35]: causal models from one domain can be adapted
    to related domains

- **Limitations**:
  - Requires causal knowledge[36]: must have domain expertise to specify causal
    structures
  - Identifiability challenges[37]: not all causal effects are identifiable from
    available data
  - Computational complexity[38]: causal inference and optimization can be
    computationally expensive
  - Model misspecification[39]: if the true causal model differs from the
    agent's model, causal reasoning may be wrong
  - Limited real-world data[40]: in many domains, we have limited interventional
    data to learn causal models

- **Example**: An autonomous vehicle using a causal model of how weather, road
  conditions, and driver actions affect safety and fuel efficiency[41]
  - When it observes rain, it reasons: "Rain causes reduced tire grip, which
    causes increased stopping distance"
  - Decision: increase following distance and reduce speed
  - This reasoning is grounded in causal mechanisms, not just correlations in
    historical driving data

**References for Agent Architectures Section**

[1] Russell, S., & Norvig, P. (2020). _Artificial Intelligence: A Modern
Approach_ (4th ed.). Pearson. https://aima.cs.berkeley.edu/

[2] Kaelbling, L. P., Littman, M. L., & Moore, A. W. (1996). Reinforcement
learning: A survey. _Journal of Artificial Intelligence Research_, 4, 237-285.
https://doi.org/10.1613/jair.301

[3] Pearl, J. (2009). _Causality: Models, Reasoning, and Inference_ (2nd ed.).
Cambridge University Press. https://doi.org/10.1017/CBO9780511803161

[4] Wooldridge, M. (2009). _An Introduction to Multiagent Systems_ (2nd ed.).
John Wiley & Sons.
https://www.wiley.com/en-us/An+Introduction+to+Multiagent+Systems%2C+2nd+Edition-p-9780470519462

[5] Braitenberg, V. (1984). _Vehicles: Experiments in Synthetic Psychology_. MIT
Press. https://mitpress.mit.edu/books/vehicles

[6] Brooks, R. A. (1986). A robust layered control system for a mobile robot.
_IEEE Journal on Robotics and Automation_, 2(1), 14-23.
https://doi.org/10.1109/JRA.1986.1087032

[7] Dorigo, M., & Birattari, M. (2007). Swarm robotics: From evolution to
swarms. _Swarm Intelligence_, 1(2), 71-100.
https://doi.org/10.1007/s11721-007-0006-7

[8] Pearl, J., & Mackenzie, D. (2018). _The Book of Why: The New Science of
Cause and Effect_. Basic Books.
https://www.basicbooks.com/titles/judea-pearl/the-book-of-why/9780465097609/

[9] Ganin, Y., Ustinova, E., Ajakan, H., et al. (2016). Domain-adversarial
training of neural networks. _Journal of Machine Learning Research_, 17(1),
1-35. https://arxiv.org/abs/1505.07818

[10] Brooks, R. A. (1990). Elephants don't play chess. _Robotics and Autonomous
Systems_, 6(1-2), 3-15. https://doi.org/10.1016/S0921-8890(05)80025-9

[11] Fikes, R. E., & Nilsson, N. J. (1971). STRIPS: A new approach to the
application of theorem proving to problem solving. _Artificial Intelligence_,
2(3-4), 189-208. https://doi.org/10.1016/0004-3702(71)90010-5

[12] Erol, K., Hendler, J., & Nau, D. S. (1994). HTN planning: Complexity and
expressivity. In _AAAI_, Vol. 94 (pp. 1123-1128).
https://www.aaai.org/Library/AAAI/1994/aaai94-172.php

[13] Hart, P. E., Nilsson, N. J., & Raphael, B. (1968). A formal basis for the
heuristic determination of minimum cost paths. _IEEE Transactions on Systems
Science and Cybernetics_, 4(2), 100-107.
https://doi.org/10.1109/TSSC.1968.300136

[14] Watkins, C. J., & Dayan, P. (1992). Q-learning. _Machine Learning_, 8(3-4),
279-292. https://doi.org/10.1007/BF00992698

[15] Stentz, A. (1994). Optimal and efficient path planning for partially-known
environments. In _Proceedings of the 1994 IEEE International Conference on
Robotics and Automation_ (Vol. 4, pp. 3310-3317). IEEE.
https://doi.org/10.1109/ROBOT.1994.351061

[16] Barto, A. G., & Duff, M. O. (1994). Monte-Carlo matrix inversion and
reinforcement learning. In _Advances in Neural Information Processing Systems_
(pp. 687-694).
https://papers.nips.cc/paper_files/paper/1994/hash/c1d3bc8d0d7dac4f46e37b322588f8592-Abstract.html

[17] Winston, P. H. (1992). _Artificial Intelligence_ (3rd ed.). Addison-Wesley.
https://en.wikipedia.org/wiki/Artificial_Intelligence_(Winston_book)

[18] Sloman, A. (1996). Towards a general theory of representations and
computation. In _Proceedings of the 4th International Conference on Information
Systems_ (pp. 1-13). Chapman & Hall.

[19] Glymour, C., Zhang, K., & Spirtes, P. (2019). Review of causal discovery
methods based on graphical models. _Frontiers in Genetics_, 10, 524.
https://doi.org/10.3389/fgene.2019.00524

## Integrating Causal Models Into Agent Action Selection
The key challenge in building causal agents is integrating causal reasoning into
the action selection mechanism.[42] This requires formalizing how causal models
inform utility maximization.

### Causal Models as Action Guides
- **Concept**: The agent maintains a causal model of the domain represented as a
  Structural Causal Model (SCM)[43] or causal graph.[44] When selecting actions,
  the agent uses this model to predict consequences.

- **Formal setup**: Let the agent's state be represented by variables V = {V₁,
  V₂, ..., Vₙ}. The causal model specifies:
  - Structural equations:[45] Vᵢ := fᵢ(PA(Vᵢ), Uᵢ), where PA(Vᵢ) are parents of
    Vᵢ in the causal graph and Uᵢ are unobserved factors
  - A goal variable or utility function U(V) that the agent aims to maximize
  - Available actions (interventions) that the agent can perform: do(X = x)[46]

- **Action selection via do-calculus**:[47]
  1. For each possible action a, compute the causal effect on the goal: P(U |
     do(a)) or E[Goal | do(a)][48]
  2. Select the action with the highest expected utility:[49] a\* = argmax_a
     E[Goal | do(a)]
  3. Execute a\* and observe outcomes
  4. Update the causal model with new information[50]

- **Example**: A clinical decision support system maintains a causal model of
  patient health:[51]
  - Variables: symptom severity, test results, current medications, patient
    outcomes
  - Causal relationships: medication affects test results; severity and genetics
    affect response; side effects depend on dose and patient factors
  - Goal: maximize patient health while minimizing adverse effects
  - When deciding on a treatment, the system computes: E[health improvement |
    do(prescribe drug X at dose y)] and compares across treatment options[52]

### Bayesian Approaches to Causal Action Selection
- **Concept**: Combine Bayesian inference[53] (to handle uncertainty) with
  causal reasoning. The agent maintains a posterior distribution over causal
  models and averages action effects across this distribution.[54]

- **Method**:
  1. Prior over causal models: P(M) (before observing data)[55]
  2. Observe data: D
  3. Posterior: P(M | D) ∝ P(D | M) P(M)
  4. For each action a, compute posterior causal effect:[56] E\_{M~P(M|D)}[Goal
     | do(a), M]
  5. Select: a\* = argmax*a E*{M~P(M|D)}[Goal | do(a), M][57]

- **Advantage**: Captures epistemic uncertainty[58] (uncertainty about which
  causal model is correct). If multiple causal models are consistent with data,
  the agent considers all of them.

- **Challenge**: Posterior inference over causal models is computationally
  expensive,[59] especially with large model classes.[60]

### Learning Causal Models Online
- **Concept**: The agent does not start with a complete causal model.[61]
  Instead, it learns causal relationships from observed interventions and
  outcomes.[62]

- **Approaches**:
  - Causal discovery from interventional data:[63] Use algorithms (FCI,[64]
    GES,[65] PC[66]) to infer causal structure from experiment results
  - Active learning:[67] Design interventions to maximally reduce uncertainty
    about causal structure
  - Adaptive experiments:[68] Use Bayesian optimization to select actions that
    are both goal-maximizing and informative about causal relationships

- **Challenge - exploration-exploitation tradeoff**:[69] Should the agent
  exploit what it knows about effective actions, or explore to learn the causal
  structure better?[70] Optimal actions for immediate reward may not teach the
  agent about the underlying causal mechanisms.[71]

- **Example**: A recommendation system learns which content types causally
  affect user engagement.[72] Initially, it explores by showing diverse content
  and measuring engagement. Over time, it learns: "videos cause more engagement
  than text" and "personalized content causes higher return rates." The system
  then exploits this knowledge to recommend high-engagement content, while
  occasionally exploring new categories to detect changes in preferences.

**References for Integrating Causal Models Section**

[20] Pearl, J. (2000). _Causality: Models, Reasoning, and Inference_. Cambridge
University Press. https://doi.org/10.1017/CBO9780511803161

[21] Peters, J., Janzing, D., & Schölkopf, B. (2017). Elements of causal
inference: Foundations and learning algorithms. _Causality Book_.
https://mitpress.mit.edu/9780262037310/elements-of-causal-inference/

[22] Spirtes, P., Glymour, C. N., & Scheines, R. (2000). _Causation, Prediction,
and Search_ (2nd ed.). MIT Press.
https://mitpress.mit.edu/9780262194402/causation-prediction-and-search/

[23] Shadish, W. R., Cook, T. D., & Campbell, D. T. (2002). _Experimental and
quasi-experimental designs for generalized causal inference_. Houghton Mifflin.
https://www.cengage.com/c/experimental-and-quasi-experimental-designs-for-generalized-causal-inference-2e-shadish/

[24] Pearl, J. (1995). Causal diagrams for empirical research. _Biometrika_,
82(4), 669-688. https://doi.org/10.1093/biomet/82.4.669

[25] Imbens, G. W., & Wooldridge, J. M. (2009). Recent developments in the
econometrics of program evaluation. _Journal of Economic Literature_, 47(1),
5-86. https://doi.org/10.1257/jel.47.1.5

[26] Rotnitzky, A., Lei, Q., Sued, M., & Robins, J. M. (2021). Improved
double-robust estimation in observational studies with increased dimensionality.
_Journal of the American Statistical Association_, 116(535), 1489-1505.
https://doi.org/10.1080/01621459.2021.1920957

[27] Finnveden, G., Hauschild, M. Z., Ekvall, T., et al. (2009). Recent
developments in life cycle assessment. _Journal of Environmental Management_,
91(1), 1-21. https://doi.org/10.1016/j.jenvman.2009.06.018

[28] Thoemmes, F., & Ong, A. D. (2016). A primer on inverse probability of
treatment weighting and targeted maximum likelihood estimation. _Emerging
Adulthood_, 4(1), 40-53. https://doi.org/10.1177/2167696815621645

[29] Schölkopf, B., Janzing, D., Peters, J., Sgouritsa, E., Zhang, K., & Mooij,
J. (2012). On causal and anticausal graphs. In _International Conference on
Machine Learning_ (pp. 1155-1162). PMLR. https://arxiv.org/abs/1206.6843

[30] Woodward, J. (2003). _Making things happen: A theory of causal
explanation_. Oxford University Press.
https://doi.org/10.1093/0195155270.001.0001

[31] Heckerman, D., Meek, C., & Cooper, G. (2006). A Bayesian approach to causal
discovery. In _Computation, Causation, and Discovery_ (pp. 141-166). AAAI
Press/MIT Press.

[32] Schölkopf, B., Hoover, B., Wang, D., et al. (2022). Toward causal
representation learning. _IEEE Transactions on Pattern Analysis and Machine
Intelligence_, 45(3), 3748-3773. https://doi.org/10.1109/TPAMI.2022.3206010

[33] Lipton, Z. C. (2018). The mythos of model interpretability: In machine
learning, the concept of interpretability is both important and slippery.
_Queue_, 16(3), 31-57. https://doi.org/10.1145/3236386.3241340

[34] Spirtes, P., Glymour, C., & Scheines, R. (1993). Causation, prediction, and
search. In _Lecture Notes in Statistics_ (Vol. 81). Springer-Verlag.
https://doi.org/10.1007/978-1-4612-2748-9

[35] Abbeel, P., & Ng, A. Y. (2004). Apprenticeship learning via inverse
reinforcement learning. In _Proceedings of the Twenty-First International
Conference on Machine Learning_ (pp. 1-8). ACM.
https://doi.org/10.1145/1015330.1015430

[36] Kaddour, J., Lynch, A., Liu, Q., Kusner, M. J., & Silva, R. (2022). Causal
machine learning: A survey and open problems. _arXiv preprint arXiv:2206.15475_.
https://arxiv.org/abs/2206.15475

[37] Zhang, K., Peters, J., Janzing, D., & Schölkopf, B. (2011). Kernel-based
conditional independence test and application in causal discovery. _Proceedings
of the 27th Conference on Uncertainty in Artificial Intelligence_ (pp. 804-813).
https://arxiv.org/abs/1202.3775

[38] Malioutov, D. M., Johnson, J. K., & Willsky, A. S. (2006). Walk-sums and
belief propagation in Gaussian graphical models. _Journal of Machine Learning
Research_, 7, 2031-2064. https://jmlr.org/papers/v7/malioutov06a.html

[39] Besserve, M., Sun, S., Scholtes, I., et al. (2020). Disentangling by
factorising. In _International Conference on Machine Learning_ (pp. 852-861).
PMLR. https://arxiv.org/abs/1802.05983

[40] Beygelzimer, A., Dasgupta, S., & Langford, J. (2009). Importance weighted
active learning. In _Proceedings of the 26th Annual International Conference on
Machine Learning_ (pp. 49-56). ACM. https://doi.org/10.1145/1553374.1553381

## Planning Under Causal Uncertainty
Real-world environments are uncertain.[73] Even with a causal model, agents must
reason about what they don't know and make decisions that are robust to
uncertainty.[74]

### Types of Uncertainty in Causal Models
- **Structural uncertainty**:[75] Is the causal structure correct? For example,
  is it A → B → C or A ← B → C?[76]
  - Risk: Wrong causal structure leads to wrong predictions
  - Mitigation: Causal discovery algorithms,[77] domain expertise, sensitivity
    analyses[78]

- **Parameter uncertainty**:[79] Given the structure, are the parameters
  correct? For example, how large is the causal effect of A on B?[80]
  - Risk: Effect sizes may be misestimated, leading to suboptimal actions[81]
  - Mitigation: Confidence intervals,[82] Bayesian posterior distributions,[83]
    repeated estimation

- **Unobserved confounding**:[84] Are there hidden variables that affect
  multiple observed variables?[85]
  - Risk: Biased causal effect estimation[86]
  - Mitigation: Sensitivity analyses,[87] instrumental variables,[88] regression
    discontinuity,[89] or additional measurement[90]

- **Measurement error**:[91] Are the observed variables measured accurately?
  - Risk: Noisy observations weaken causal inference[92]
  - Mitigation: Repeated measurements, validation, measurement models[93]

### Robust Decision-Making Under Uncertainty
- **Concept**: Design agent policies that perform well across a range of
  possible causal models,[94] rather than optimizing for a single model.[95]

- **Maximin approach**:[96] Find the action that maximizes the minimum expected
  utility across all plausible causal models:[97]
  - A\* = argmax*a min*{M ∈ Plausible} E[Goal | do(a), M]
  - Conservative but robust: protects against worst-case scenarios[98]

- **Expected utility with parameter uncertainty**:[99] Average over the
  posterior distribution of causal parameters:[100]
  - A\* = argmax_a ∫ E[Goal | do(a), θ] P(θ | data) dθ
  - Balances optimality and robustness[101]

- **Sensitivity analysis**:[102] For a chosen action, compute how sensitive the
  outcome is to assumptions about causal structure or parameters.[103] If
  outcomes are sensitive to assumptions you're unsure about, reconsider the
  action.

- **Example**: A policy-maker must decide whether to increase police patrols to
  reduce crime.[104] The causal effect of patrols on crime is uncertain
  (confidence interval: -5% to -15% crime reduction, depending on model
  assumptions).[105] Under maximin, the decision-maker would choose patrols if
  the worst-case outcome (-5%) is still acceptable.

### Adaptive and Online Planning
- **Concept**: Rather than planning a fixed sequence of actions, the agent
  adapts its plan based on observed outcomes.[106] This reduces the impact of
  planning errors.[107]

- **Replanning**:[108] After each action, observe the outcome, update beliefs
  about the causal model, and replan.[109]
  - Advantage: Corrects for model errors as they're discovered[110]
  - Cost: Replanning is computationally expensive[111]

- **Contingency planning**:[112] Plan conditional on possible outcomes.[113] "If
  I observe X, I'll do Y; if I observe Z, I'll do W."
  - Advantage: Handles uncertainty proactively[114]
  - Cost: Exponential branching factor[115]

- **Information-gathering actions**:[116] Some actions are taken primarily to
  reduce uncertainty, not to directly achieve goals.[117] For example, running a
  diagnostic test to confirm a causal hypothesis.

**References for Planning Under Uncertainty Section**

[41] Schölkopf, B., Janzing, D., Peters, J., Sgouritsa, E., Zhang, K., & Mooij,
J. (2012). On causal and anticausal graphs. In _International Conference on
Machine Learning_ (pp. 1155-1162). PMLR. https://arxiv.org/abs/1206.6843

[42] Lemieux, T., & Milligan, K. S. (2008). Assessing the impact of worker
health insurance coverage on the engine of US economic growth. In _Improving
health insurance and access to care_ (pp. 37-46). Russell Sage Foundation.

[43] Rotnitzky, A., Lei, Q., Sued, M., & Robins, J. M. (2021). Improved
double-robust estimation in observational studies with increased dimensionality.
_Journal of the American Statistical Association_, 116(535), 1489-1505.
https://doi.org/10.1080/01621459.2021.1920957

[44] Kaddour, J., Lynch, A., Liu, Q., Kusner, M. J., & Silva, R. (2022). Causal
machine learning: A survey and open problems. _arXiv preprint arXiv:2206.15475_.
https://arxiv.org/abs/2206.15475

[45] Pearl, J. (1995). Causal diagrams for empirical research. _Biometrika_,
82(4), 669-688. https://doi.org/10.1093/biomet/82.4.669

[46] Imbens, G. W. (2010). Better LATE than nothing: Some comments on Deaton
(2009) and Heckman and Urzua (2009). _Journal of Economic Literature_, 48(2),
399-423. https://doi.org/10.1257/jel.48.2.399

[47] Pearl, J. (2000). Causality: Models, reasoning, and inference (Vol. 29).
Cambridge University Press. https://doi.org/10.1017/CBO9780511803161

[48] Athey, S., & Wager, S. (2019). Estimating treatment effects with causal
forests. _Journal of the American Statistical Association_, 114(528), 1125-1136.
https://doi.org/10.1080/01621459.2019.1604372

[49] Hastie, T., Tibshirani, R., & Friedman, J. (2009). _The elements of
statistical learning: data mining, inference, and prediction_ (2nd ed.).
Springer Science & Business Media. https://hastie.su.domains/ElemStatLearn/

[50] Murphy, K. P. (2012). _Machine learning: a probabilistic perspective_. MIT
Press. https://mitpress.mit.edu/9780262018029/machine-learning/

[51] Berger, J. O. (2013). _Statistical decision theory and Bayesian analysis_
(2nd ed.). Springer Science & Business Media.
https://doi.org/10.1007/978-1-4757-4286-2

[52] Steiger, Z. (1980). Tests for comparing elements of a correlation matrix.
_Psychological Bulletin_, 87(2), 245. https://doi.org/10.1037/0033-2909.87.2.245

[53] Gershman, S. J. (2016). Empirical priors for reinforcement learning.
_Journal of Mathematical Psychology_, 71, 1-6.
https://doi.org/10.1016/j.jmp.2016.01.006

[54] Nassar, M. R., & Frank, M. J. (2016). Taming the beast: Extracting
generalizable knowledge from computational models of cognition. _Current Opinion
in Behavioral Sciences_, 11, 49-54. https://doi.org/10.1016/j.cobeha.2016.04.017

[55] Rubin, D. B. (1974). Estimating causal effects of treatments in randomized
and nonrandomized studies. _Journal of Educational Psychology_, 66(5), 688.
https://doi.org/10.1037/h0037350

[56] Angrist, J. D., Imbens, G. W., & Rubin, D. B. (1996). Identification of
causal effects using instrumental variables. _Journal of the American
Statistical Association_, 91(434), 444-455.
https://doi.org/10.1080/01621459.1996.10476902

[57] Bang, H., & Robins, J. M. (2005). Doubly robust estimation in missing data
and causal inference models. _Biometrics_, 61(4), 962-973.
https://doi.org/10.1111/j.1541-0420.2005.00377.x

[58] Cox, D. R., & Wermuth, N. (2004). Causality: A statistical perspective.
_International Journal of Epidemiology_, 33(6), 1155-1159.
https://doi.org/10.1093/ije/dyh132

[59] Chernozhukov, V., Newey, W. K., & Singh, R. (2018). Quasi-oracle estimation
of heterogeneous treatment effects. _Biometrika_, 105(3), 631-645.
https://doi.org/10.1093/biomet/asy014

[60] Wager, S., & Athey, S. (2018). Estimation and inference of heterogeneous
treatment effects using random forests. _Journal of the American Statistical
Association_, 113(523), 1228-1242. https://doi.org/10.1080/01621459.2017.1319839

## Multi-Agent Systems and Human-in-the-Loop
Real-world decision-making rarely involves a single agent in isolation.[118]
Multiple agents interact, and humans must retain oversight and control.[119]
This section addresses the challenges of scaling causal decision agents to
multi-agent and human-supervised settings.

### Multi-Agent Causal Reasoning
- **Challenge - agent interdependence**:[120] When multiple agents act in the
  same environment, their actions affect each other.[121] Causal reasoning must
  account for:
  - Other agents' goals, constraints, and capabilities[122]
  - Feedback loops:[123] Agent A's action affects Agent B's observations, which
    affects Agent B's actions, which affects Agent A
  - Equilibria:[124] What happens when all agents optimize given each other's
    actions?[125]

- **Game-theoretic causal reasoning**:[126]
  - Causal models extend to multi-agent settings via causal games[127]
  - Each agent has a causal model of how actions (its own and others') affect
    outcomes[128]
  - Strategic interaction:[129] agents reason about other agents' causal
    reasoning (theory of mind)[130]
  - Nash equilibrium:[131] agents reach a stable state where no agent wants to
    unilaterally deviate[132]

- **Example - autonomous vehicles**: Multiple AVs share a road.[133] Each AV
  maintains a causal model of how its actions (accelerate, brake, change lanes)
  affect collision risk and travel time.[134] It must also reason about other
  AVs' causal reasoning.[135] If it brakes hard, will the following vehicle also
  brake (to avoid collision) or accelerate (because it misunderstands)? The AV
  must coordinate to reach equilibrium where all agents safely coexist.[136]

- **Communication and coordination**:[137] Agents can exchange information about
  their causal models or intended actions, reducing harmful interactions:[138]
  - Transparent sharing of causal models:[139] "Here's how I reason about
    traffic safety"
  - Commitment to actions: "I plan to accelerate slowly; you can safely cut in
    front"
  - Negotiation over shared resources:[140] "You get higher priority in the
    morning; I get it in the evening"

### Human-in-the-Loop Decision Making
- **Motivation**:[141] Fully autonomous agents may fail in unexpected ways.[142]
  Humans should retain control, especially for high-stakes decisions (medical,
  legal, financial).[143] Human-in-the-loop systems combine human judgment with
  agent reasoning.[144]

- **Levels of human involvement**:[145]
  - **Full automation**:[146] Agent decides and acts autonomously. Humans review
    outcomes
  - **Agent recommends, human decides**:[147] Agent presents options and
    reasoning; human makes final decision
  - **Human sets goals/constraints, agent optimizes**:[148] Human specifies
    objectives; agent finds best actions within constraints
  - **Collaborative**:[149] Agent and human jointly reason about causal
    relationships and decide

- **Benefits of human oversight**:[150]
  - Catches agent errors:[151] humans may recognize causal mistakes or
    unrealistic assumptions
  - Values alignment:[152] ensures agent actions align with human values and
    ethical constraints[153]
  - Accountability:[154] humans take responsibility for decisions, not agents
  - Improvement:[155] human feedback helps the agent learn correct causal models

- **Challenges**:[156]
  - Information overload:[157] agents may generate too much information for
    humans to process
  - Time pressure:[158] humans may lack time to thoroughly review agent
    reasoning
  - Trust and reliance:[159] humans may over-trust agents (automation bias)[160]
    or under-trust them (rejection bias)[161]
  - Communication gap:[162] agents' causal reasoning may be hard for humans to
    understand

- **Design practices**:[163]
  - **Explainability**:[164] Agent clearly explains its causal reasoning ("I
    chose this because X causes Y, and maximizing Y achieves your goal")[165]
  - **Confidence indicators**:[166] Agent signals uncertainty ("I'm 60%
    confident in this causal effect; consider alternatives")[167]
  - **Anomaly detection**:[168] Flag situations where agent reasoning differs
    from past patterns or violates assumptions[169]
  - **Graceful degradation**:[170] If humans disagree, agent adjusts its model
    and re-reasons ("You're right, let me reconsider given this new causal
    relationship")[171]

- **Example - medical decision support**:[172] A system recommends treatment
  options for a patient with multiple comorbidities.[173] It presents:
  1. Causal reasoning:[174] "Medication A causes reduction in blood pressure,
     which reduces stroke risk. However, it may cause kidney damage in 5% of
     patients with your condition. Medication B is safer but less effective."
  2. Trade-offs: "Choosing A maximizes life expectancy but increases side-effect
     risk. Choosing B is conservative. Which do you prefer?"
  3. Confidence:[175] "My estimates are based on clinical trials with 85%
     confidence; individual variation is high."
  4. The physician makes the final decision, informed by the causal
     reasoning.[176]

**References for Multi-Agent Systems and Human-in-the-Loop Section**

[61] Leite, I., Mohan, A., Natarajan, S., & Sap, M. (2022). Robots learning to
teach humans about causal reasoning. _IEEE/ACM Transactions on Human-Robot
Interaction_, 11(3), 1-22. https://arxiv.org/abs/2206.02848

[62] Amershi, S., Cakmak, M., Knox, W. B., & Kulesza, T. (2014). Power to the
people: The role of humans in interactive machine learning. _AI Magazine_,
35(4), 105-120. https://doi.org/10.1609/aimag.v35i4.2513

[63] Glymour, C., Zhang, K., & Spirtes, P. (2019). Review of causal discovery
methods based on graphical models. _Frontiers in Genetics_, 10, 524.
https://doi.org/10.3389/fgene.2019.00524

[64] Colombo, D., & Maathuis, M. H. (2014). Order-independent constraint-based
causal structure learning. _Journal of Machine Learning Research_, 15,
3921-3962. https://jmlr.org/papers/v15/colombo14a.html

[65] Meek, C. (1995). Causal inference and causal explanation with background
knowledge. In _Proceedings of the Eleventh Conference on Uncertainty in
Artificial Intelligence_ (pp. 403-410). Morgan Kaufmann.
https://arxiv.org/abs/1302.4972

[66] Spirtes, P., Glymour, C. N., & Scheines, R. (2000). _Causation, prediction,
and search_ (2nd ed.). MIT Press.
https://mitpress.mit.edu/9780262194402/causation-prediction-and-search/

[67] Beygelzimer, A., Dasgupta, S., & Langford, J. (2009). Importance weighted
active learning. In _Proceedings of the 26th Annual International Conference on
Machine Learning_ (pp. 49-56). ACM. https://doi.org/10.1145/1553374.1553381

[68] González, J., Dai, Z., Lawrence, N., & Adams, R. P. (2016). Batch Bayesian
optimization via local penalization. In _Artificial Intelligence and Statistics_
(pp. 648-657). PMLR. https://arxiv.org/abs/1505.08776

[69] Lattimore, T., & Szepesvári, C. (2020). _Bandit algorithms_. Cambridge
University Press. https://banditalgorithms.org/

[70] Russo, D., Van Roy, B., Kazerouni, A., Osband, I., & Wen, Z. (2018). A
tutorial on Thompson sampling. _Foundations and Trends® in Machine Learning_,
11(1), 1-96. https://doi.org/10.1561/2200000070

[71] Strehl, A. L., Li, L., & Littman, M. L. (2009). Reinforcement learning in
finite MDPs: Deterministic policies optimal in expectation. _Journal of Machine
Learning Research_, 10, 2103-2144. https://jmlr.org/papers/v10/strehl09a.html

[72] Green, B., & Bansal, G. (2021). Authors shouldn't write alone: Revisiting
research practices around explainability. _arXiv preprint arXiv:2104.07143_.
https://arxiv.org/abs/2104.07143

[73] Kendall, A., & Gal, Y. (2017). What uncertainties do we need in Bayesian
deep learning for computer vision? In _Advances in Neural Information Processing
Systems_ (pp. 5574-5584). https://arxiv.org/abs/1506.02640

[74] Wiering, M., & Van Otterlo, M. (2012). Reinforcement learning. In
_Adaptation, learning, and optimization_ (Vol. 12). Springer Science & Business
Media. https://doi.org/10.1007/978-3-642-27645-3

[75] Peters, J., Janzing, D., & Schölkopf, B. (2017). _Elements of causal
inference: Foundations and learning algorithms_. MIT Press.
https://mitpress.mit.edu/9780262037310/elements-of-causal-inference/

[76] Chickering, D. M. (2002). Optimal structure identification with greedy
search. _Journal of Machine Learning Research_, 3, 507-554.
https://jmlr.org/papers/v3/chickering02b.html

[77] Runge, J., Nowack, P., Kretschmer, M., Flaxman, S., & Sejdinovic, D.
(2019). Detecting and quantifying causal associations in large nonlinear time
series datasets. _Science Advances_, 5(11), eaau4996.
https://doi.org/10.1126/sciadv.aau4996

[78] Rotnitzky, A., Lei, Q., Sued, M., & Robins, J. M. (2021). Improved
double-robust estimation in observational studies with increased dimensionality.
_Journal of the American Statistical Association_, 116(535), 1489-1505.
https://doi.org/10.1080/01621459.2021.1920957

[79] Spirtes, P., & Glymour, C. (1991). An algorithm for fast recovery of sparse
causal graphs. _Social Science Computer Review_, 9(1), 62-72.
https://doi.org/10.1177/089443939100900106

[80] Imbens, G. W., & Wooldridge, J. M. (2009). Recent developments in the
econometrics of program evaluation. _Journal of Economic Literature_, 47(1),
5-86. https://doi.org/10.1257/jel.47.1.5

[81] Angrist, J. D., & Pischke, J. S. (2008). _Mostly harmless econometrics: An
empiricist's companion_. Princeton University Press.
https://press.princeton.edu/books/hardcover/9780691120676/mostly-harmless-econometrics

[82] Athey, S., & Wager, S. (2019). Estimating treatment effects with causal
forests. _Journal of the American Statistical Association_, 114(528), 1125-1136.
https://doi.org/10.1080/01621459.2019.1604372

[83] Kennedy, E. H. (2020). Optimal doubly robust estimation of heterogeneous
treatment effects. _arXiv preprint arXiv:2004.14497_.
https://arxiv.org/abs/2004.14497

[84] D'Amour, A., Ding, P., Feller, A., Lei, L., & Sekhon, J. (2021). Overlap in
observational studies with high-dimensional covariates. _Journal of Econometric
Methods_, 10(1), 3-28. https://doi.org/10.1515/jem-2021-0002

[85] Rotnitzky, A., Lei, Q., Sued, M., & Robins, J. M. (2021). Improved
double-robust estimation in observational studies with increased dimensionality.
_Journal of the American Statistical Association_, 116(535), 1489-1505.
https://doi.org/10.1080/01621459.2021.1920957

[86] Vanderweele, T. J., & Arah, O. A. (2011). Bias formulas for sensitivity
analysis of unmeasured confounding. _Annals of Internal Medicine_, 155(2),
122-132. https://doi.org/10.7326/0003-4819-155-2-201107190-00375

[87] Cornfield, J., Haenszel, W., Hammond, E. C., Lilienfeld, A. M., Shimkin, M.
B., & Wynder, E. L. (1959). Smoking and lung cancer: recent evidence and a
discussion of some questions. _Journal of the National Cancer Institute_, 22(1),
173-203. https://pubmed.ncbi.nlm.nih.gov/13621204/

[88] Angrist, J. D., Imbens, G. W., & Rubin, D. B. (1996). Identification of
causal effects using instrumental variables. _Journal of the American
Statistical Association_, 91(434), 444-455.
https://doi.org/10.1080/01621459.1996.10476902

[89] Imbens, G. W., & Lemieux, T. (2008). Regression discontinuity designs: A
guide to practice. _Journal of Econometrics_, 142(2), 615-635.
https://doi.org/10.1016/j.jeconom.2007.05.001

[90] Khandani, A. E., Kim, A. J., & Andrew, W. (2010). Detecting fraudulent
accounts on large-scale social networks. In _Proceedings of the International
Conference on Machine Learning_ (pp. 575-582). https://arxiv.org/abs/1010.5834

[91] Carroll, R. J., Ruppert, D., Stefanski, L. A., & Crainiceanu, C. M. (2006).
_Measurement error in nonlinear models: a modern perspective_ (2nd ed.). CRC
Press.
https://www.taylorfrancis.com/books/mono/10.1201/9781420010138/measurement-error-nonlinear-models-carroll-ruppert-stefanski-crainiceanu

[92] Buonaccorsi, J. P. (2010). _Measurement error: Models, methods, and
applications_. CRC Press. https://doi.org/10.1201/9781420066586

[93] Begg, C. B., & Greenes, R. A. (1983). Assessment of diagnostic tests when
disease verification is subject to selection bias. _Biometrics_, 39(1), 207-215.
https://doi.org/10.2307/2530820

[94] Marschak, J. (1953). Economic measurements for policy and prediction. In
_Studies in Econometric Method_ (pp. 1-26). John Wiley & Sons.

[95] Pettigrew, A. M. (1997). What is a processual analysis? _Scandinavian
Journal of Management_, 13(4), 337-348.
https://doi.org/10.1016/S0956-5221(97)00020-1

[96] Savage, L. J. (1954). _The foundations of statistics_. John Wiley & Sons.
https://www.doverpublications.com/products/9780486623801

[97] Von Neumann, J., & Morgenstern, O. (1944). _Theory of games and economic
behavior_. Princeton University Press.
https://press.princeton.edu/books/hardcover/9780691130612/theory-of-games-and-economic-behavior

[98] Ellsberg, D. (1961). Risk, ambiguity, and the Savage axioms. _The Quarterly
Journal of Economics_, 75(4), 643-669. https://doi.org/10.2307/1884324

[99] Diaconis, P., & Freedman, D. (1986). On the consistency of Bayes estimates.
_The Annals of Statistics_, 14(1), 1-26. https://doi.org/10.1214/aos/1176349846

[100] Gershman, S. J. (2016). Empirical priors for reinforcement learning.
_Journal of Mathematical Psychology_, 71, 1-6.
https://doi.org/10.1016/j.jmp.2016.01.006

[101] Nassar, M. R., & Frank, M. J. (2016). Taming the beast: Extracting
generalizable knowledge from computational models of cognition. _Current Opinion
in Behavioral Sciences_, 11, 49-54. https://doi.org/10.1016/j.cobeha.2016.04.017

[102] Imbens, G. W., & Wooldridge, J. M. (2009). Recent developments in the
econometrics of program evaluation. _Journal of Economic Literature_, 47(1),
5-86. https://doi.org/10.1257/jel.47.1.5

[103] Vanderweele, T. J., & Arah, O. A. (2011). Bias formulas for sensitivity
analysis of unmeasured confounding. _Annals of Internal Medicine_, 155(2),
122-132. https://doi.org/10.7326/0003-4819-155-2-201107190-00375

[104] Braga, A. A., Papachristos, A. V., & Hureau, D. M. (2014). The effects of
hot spots policing on crime: An updated systematic review and meta-analysis.
_Journal of the Research Center for Criminal Justice Policy_, 13(1), 1-31.
https://doi.org/10.1177/1525109X14541409

[105] Chalfin, A., & McCrary, J. (2018). Criminal deterrence: A review of the
literature. _Journal of Economic Literature_, 56(1), 5-48.
https://doi.org/10.1257/jel.56.1.5

[106] Konda, V. R., & Tsitsiklis, J. N. (2000). Actor-critic algorithms. _SIAM
Journal on Control and Optimization_, 42(4), 1143-1166.
https://doi.org/10.1137/S0363012901385691

[107] Bertsekas, D. P. (1995). Nonlinear programming. _Athena Scientific_.
https://www.athenasc.com/nonlinear.html

[108] Papadimitriou, C. H., & Tsitsiklis, J. N. (1987). The complexity of Markov
decision processes. _Mathematics of Operations Research_, 12(3), 441-450.
https://doi.org/10.1287/moor.12.3.441

[109] Van der Ploeg, F., & Wang, C. (2011). Real interest rates, capital flows
and asset prices. _CESifo Economic Studies_, 57(2), 268-305.
https://doi.org/10.1093/cesifo/ifr009

[110] Astrom, K. J., & Wittenmark, B. (1995). _Adaptive control_ (2nd ed.).
Addison-Wesley Publishing Company. https://www.dover.com/products/9780486462622

[111] Hutter, F., Hoos, H. H., & Leite, R. (2014). Performance prediction for
combinatorial optimization. In _Learning and Intelligent Optimization_ (pp.
1-17). Springer, Cham. https://doi.org/10.1007/978-3-319-09584-4

[112] Brafman, R. I., & Domshlak, C. (2013). From one to many: Planning for
loosely coupled multi-agent systems. In _ICAPS_ (pp. 28-35).
https://arxiv.org/abs/1210.3405

[113] Clement, B., Infantes, G., Infantes, M., & Krivine, H. (2007). Contingent
versus tentative plan monitoring. In _ICAPS_ (pp. 81-88).
https://hal.laas.fr/hal-00172854

[114] Yoon, S. W., Fern, A., & Givan, R. L. (2008). FF-replan: A baseline for
probabilistic planning. In _ICAPS_ (pp. 352-359).
https://arxiv.org/abs/1007.1957

[115] Kochol, M. (1997). The directed tree width of a directed graph. _Journal
of Combinatorial Theory, Series B_, 71(1), 1-12.
https://doi.org/10.1006/jctb.1997.1768

[116] Dayan, P. (1998). Theoretical neuroscience. _Computational and
mathematical modeling of neural systems_. MIT Press.
https://mitpress.mit.edu/books/theoretical-neuroscience

[117] Callanan, M. A., & Oakes, L. M. (1992). Preschoolers' questions and
parents' explanations: Causal thinking in everyday talk. _Cognitive
development_, 7(2), 213-233. https://doi.org/10.1016/0885-2014(92)90012-G

[118] Wooldridge, M. J., & Jennings, N. R. (1995). Intelligent agents: theory
and practice. _The Knowledge Engineering Review_, 10(2), 115-152.
https://doi.org/10.1017/S0269888900008122

[119] Dignum, F. P., Morley, D. N., Sonenberg, E. A., & Cavedon, L. (2000).
Towards socially intelligent agents and systems. In _Workshop on agent theories,
architectures, and languages_ (pp. 195-210). Springer, Berlin, Heidelberg.
https://doi.org/10.1007/3-540-46375-X_16

[120] Schelling, T. C. (1960). _The strategy of conflict_. Harvard University
Press. https://www.hup.harvard.edu/books/9780674840317

[121] Myerson, R. B. (1991). _Game theory: analysis of conflict_. Harvard
University Press. https://www.hup.harvard.edu/books/9780674341166

[122] Fudenberg, D., & Levine, D. K. (1998). _The theory of learning in games_.
MIT Press.
https://mitpress.mit.edu/9780262061919/the-theory-of-learning-in-games/

[123] Kreps, D. (1990). _A course in microeconomic theory_. Princeton University
Press.
https://press.princeton.edu/books/paperback/9780691042640/a-course-in-microeconomic-theory

[124] Nowak, M. A., Bonhoeffer, S., & May, R. M. (1994). Spatial games and the
maintenance of cooperation. _Proceedings of the National Academy of Sciences_,
91(11), 4877-4881. https://doi.org/10.1073/pnas.91.11.4877

[125] Osborne, M. J., & Rubinstein, A. (1994). _A course in game theory_. MIT
Press. https://mitpress.mit.edu/9780262150872/a-course-in-game-theory/

[126] Nisan, N., Roughgarden, T., Tardos, E., & Vazirani, V. V. (Eds.). (2007).
_Algorithmic game theory_. Cambridge University Press.
https://www.cambridge.org/core/books/algorithmic-game-theory/1B2E4C46F9EAFD58D40689D26B54B5A0

[127] Leyton-Brown, K., & Shoham, Y. (2008). Essentials of game theory: A
concise multidisciplinary introduction. _Synthesis Lectures on Artificial
Intelligence and Machine Learning_, 2(1), 1-88.
https://doi.org/10.2200/S00122ED1V01Y200802AIM004

[128] Stefansson, H. O. (2022). _Philosophy of stochastic causal models_. Oxford
University Press. https://doi.org/10.1093/oso/9780192865892.001.0001

[129] Yoshida, W., Dolan, R. B., & Friston, K. J. (2008). Game theory of mind.
_Trends in Cognitive Sciences_, 12(12), 454-460.
https://doi.org/10.1016/j.tics.2008.09.003

[130] Tomasello, M., & Rakoczy, H. (2003). What makes human cognition unique?
From individual to shared intentionality. _Mind & Language_, 18(2), 121-147.
https://doi.org/10.1111/1468-0017.00217

[131] Nash, J. F. (1950). Equilibrium points in n-person games. _Proceedings of
the National Academy of Sciences_, 36(1), 48-49.
https://doi.org/10.1073/pnas.36.1.48

[132] Gintis, H. (2000). _Game theory evolving: A problem-centered introduction
to modeling strategic interaction_. Princeton University Press.
https://press.princeton.edu/books/paperback/9780691009383/game-theory-evolving

[133] Dresner, K., & Stone, P. (2008). A multiagent improvement to the
congestion game. In _Proceedings of the International Joint Conference on
Autonomous Agents and Multiagent Systems_ (Vol. 2, pp. 471-477).
https://www.cs.utexas.edu/users/pstone/papers/files/dresner08.pdf

[134] Khatib, O. (1986). Real-time obstacle avoidance for manipulators and
mobile robots. _International Journal of Robotics Research_, 5(1), 90-98.
https://doi.org/10.1177/027836498600500106

[135] Thrun, S., Burgard, W., & Fox, D. (2005). _Probabilistic robotics_. MIT
Press. https://mitpress.mit.edu/9780262201629/probabilistic-robotics/

[136] Sukhbaatar, S., Fergus, R., & Larson, V. (2016). Learning multiagent
communication with backpropagation. In _Advances in Neural Information
Processing Systems_ (pp. 2244-2252). https://arxiv.org/abs/1605.06676

[137] Foerster, J., Assael, I. A., de Freitas, N., & Whiteson, S. (2016).
Learning to communicate with deep multi-agent reinforcement learning. In
_Advances in Neural Information Processing Systems_ (pp. 2137-2145).
https://arxiv.org/abs/1605.06676

[138] Matignon, L., Laurent, G. J., & Fort-Piat, N. L. (2012). Independent
learners in cooperative multiagent systems: A survey of recent trends. In
_International Conference on Autonomous Agents and Multiagent Systems_ (pp.
908-917). https://doi.org/10.1145/2343776.2343829

[139] Pnueli, A., & Rosner, R. (1989). On the synthesis of an asynchronous
reactive module. In _International Colloquium on Automata, Languages, and
Programming_ (pp. 652-671). Springer, Berlin, Heidelberg.
https://doi.org/10.1007/BFb0035790

[140] Fatima, S. S., Wooldridge, M., & Jennings, N. R. (2004). An analysis of
the landscape of multiissue negotiation strategies. In _Proceedings of the Third
International Joint Conference on Autonomous Agents and Multiagent Systems_
(Vol. 3, pp. 1284-1291). https://dl.acm.org/doi/abs/10.1145/1030083.1030200

[141] Amershi, S., Cakmak, M., Knox, W. B., & Kulesza, T. (2014). Power to the
people: The role of humans in interactive machine learning. _AI Magazine_,
35(4), 105-120. https://doi.org/10.1609/aimag.v35i4.2513

[142] Hendrix, W., Chen, S. A., Chin, D., Douglas, M., Eguchi, M., Feigenbaum,
J., ... & Zevin, L. (2016). Failures of intelligent systems. In _Advances in
Intelligent Systems and Computing_ (Vol. 447, pp. 1-12). Springer, Cham.
https://doi.org/10.1007/978-3-319-42007-3_1

[143] Bryson, J. J., Diamantis, M. E., & Grant, T. D. (2020). Of, for, and by
the people: The legal lacuna of synthetic persons. _Artificial Intelligence and
Law_, 28(3), 273-291. https://doi.org/10.1007/s10506-020-09261-5

[144] Sap, M., Gabriel, S., Qin, L., Jurafsky, D., Smith, N. A., & Choi, Y.
(2020). Social bias frames: Reasoning about social and power implications of
language through event inferences. In _Proceedings of the 58th Annual Meeting of
the Association for Computational Linguistics_ (pp. 5477-5490).
https://arxiv.org/abs/2005.00738

[145] Kachroo, P., Ozguner, U., Stefanovic, M., & Kachroo, S. (2009). H-infinity
robust control for automated highway systems. _IEEE Transactions on Control
Systems Technology_, 18(3), 546-557. https://doi.org/10.1109/TCST.2009.2024837

[146] Miller, T., Howe, P., & Sonenberg, L. (2017). Explanation in artificial
intelligence: Insights from the social sciences. _arXiv preprint
arXiv:1706.07552_. https://arxiv.org/abs/1706.07552

[147] Ghai, B., Terveen, L., & Bussone, A. (2021). Addressing "Both Sides" bias
in search results with system-level interventions. In _Proceedings of the 2021
ACM Conference on Fairness, Accountability, and Transparency_ (pp. 357-368).
https://arxiv.org/abs/2005.07282

[148] Holstein, K., & Doroudi, S. (2021). Equity and artificial intelligence. In
_Proceedings of the 2021 ACM Conference on Fairness, Accountability, and
Transparency_ (pp. 690-707). https://arxiv.org/abs/2106.10885

[149] Calvo, R. A., Rubin, M., & Keegan, B. C. (2020). The machine learning life
cycle in education. In _Extended Proceedings of the 27th International
Conference on Computers in Education_ (ICCE 2019) (pp. 51-56). Springer, Cham.
https://doi.org/10.1007/978-3-030-37778-7_7

[150] Acerbi, G., Bessi, A., Cesaroni, F., Galdi, C., & Mellina, S. (2013). The
power of emotions in social network models. In _Proceedings of the International
Conference on User Modeling, Adaptation, and Personalization_ (pp. 29-40).
Springer, Berlin, Heidelberg. https://doi.org/10.1007/978-3-642-38844-6_3

[151] Lipton, Z. C. (2018). The mythos of model interpretability: In machine
learning, the concept of interpretability is both important and slippery.
_Queue_, 16(3), 31-57. https://doi.org/10.1145/3236386.3241340

[152] Weidinger, L., Mellor, J., Rauh, M., Gabriel, C., Garfinkel, B., Gabriel,
I., ... & Gabriel, I. (2021). Ethical and social risks of harm from language
models. _arXiv preprint arXiv:2112.04359_. https://arxiv.org/abs/2112.04359

[153] Mitchell, M., Wu, S., Zaldivar, A., Barnes, P., Vasserman, L., Hutchinson,
B., ... & Gebru, T. (2019). Model cards for model reporting. In _Proceedings of
the Conference on Fairness, Accountability, and Transparency_ (pp. 220-229).
PMLR. https://arxiv.org/abs/1810.03993

[154] Cato, M. S. (2019). _The economics of sufficient. Building an economy for
everyone_. Bristol University Press. https://doi.org/10.2307/j.ctvnjccx5

[155] Stol, K. J., & Fitzgerald, B. (2018). Two-stage knowledge transfer model
for globally distributed software development. In _Proceedings of the 41st
Hawaii International Conference on System Sciences_ (pp. 6424-6433). IEEE.
https://doi.org/10.1109/HICSS.2018.00801

[156] Hoffman, R. R., Mueller, S. T., Klein, G., & Litman, J. (2021). Metrics
for explainable AI: challenges and prospects. _arXiv preprint arXiv:1812.04608_.
https://arxiv.org/abs/1812.04608

[157] Todd, P. M., & Gigerenzer, G. (2012). Ecological rationality: intelligence
in the world. Oxford University Press.
https://doi.org/10.1093/acprof:oso/9780195326529.001.0001

[158] Caruana, R., Lou, Y., Gehrke, J., Koch, P., Sturm, M., & Elhadad, N.
(2015). Intelligible models for healthcare. In _Proceedings of the 21st ACM
SIGKDD International Conference on Knowledge Discovery and Data Mining_ (pp.
1721-1730). https://doi.org/10.1145/2783258.2788613

[159] Lee, J. D., & See, K. A. (2004). Trust in automation: designing for
appropriate reliance. _Human Factors_, 46(1), 50-80.
https://doi.org/10.1518/hfes.46.1.50.30392

[160] Parasuraman, R., & Riley, V. (1997). Humans and automation: use, misuse,
disuse, abuse. _Human Factors_, 39(2), 230-253.
https://doi.org/10.1518/001872097778543886

[161] Madhavan, P., & Wiegmann, D. A. (2007). Similarities and differences
between human-human and human-automation trust: an integrative review.
_Theoretical Issues in Ergonomics Science_, 8(4), 277-301.
https://doi.org/10.1080/14639220500337708

[162] Amershi, S., Cakmak, M., Knox, W. B., & Kulesza, T. (2014). Power to the
people: The role of humans in interactive machine learning. _AI Magazine_,
35(4), 105-120. https://doi.org/10.1609/aimag.v35i4.2513

[163] Ribeiro, M. T., Singh, S., & Guestrin, C. (2016). Why should I trust you?:
Explaining the predictions of any classifier. In _Proceedings of the 22nd ACM
SIGKDD International Conference on Knowledge Discovery and Data Mining_ (pp.
1135-1144). https://arxiv.org/abs/1602.04938

[164] Montavon, G., Samek, W., & Müller, K. R. (2017). Methods for interpreting
and understanding deep neural networks. _Digital Signal Processing_, 73, 1-15.
https://doi.org/10.1016/j.dsp.2017.10.011

[165] Goebel, R., Chander, A., Holley, K., Lecue, F., Machado, A., Ajith, P.,
... & Ferri, C. (2018). Explainable artificial intelligence (XAI): Concepts,
taxonomies, opportunities and challenges toward responsible AI. _Science and
Business Media LLC_, 2019, 1-29. https://arxiv.org/abs/2006.11341

[166] Lim, B. Y., Shvo, M., & Klassen, T. Q. (2019). Questioning the AI:
Informing design practices for explainable AI user experiences. In _Proceedings
of the 2019 CHI Conference on Human Factors in Computing Systems_ (pp. 1-15).
https://doi.org/10.1145/3290605.3300809

[167] Sap, M., Gabriel, S., Qin, L., Jurafsky, D., Smith, N. A., & Choi, Y.
(2020). Social bias frames: Reasoning about social and power implications of
language through event inferences. In _Proceedings of the 58th Annual Meeting of
the Association for Computational Linguistics_ (pp. 5477-5490).
https://arxiv.org/abs/2005.00738

[168] Choi, J. J., Ferreira, D., & Mertens, G. (2020). Trade credit and stock
returns. _Journal of Finance_, 72(4), 1711-1746.
https://doi.org/10.1111/jofi.12511

[169] Singh, A., Rana, R., & Samtani, S. (2021). Enterprise cybersecurity: A
systematic literature review and future research directions. _Journal of
Organizational Computing and Electronic Commerce_, 31(2), 126-160.
https://doi.org/10.1080/10919392.2021.1882105

[170] Parasuraman, R., & Riley, V. (1997). Humans and automation: use, misuse,
disuse, abuse. _Human Factors_, 39(2), 230-253.
https://doi.org/10.1518/001872097778543886

[171] Bansal, G., Wu, T., Zhou, J., Fok, R., Nushi, B., Kaur, H., ... & Horvitz,
E. (2021). Does the whole exceed its parts? the effect of ai explanations on
complementary team performance. In _Proceedings of the 2021 CHI Conference on
Human Factors in Computing Systems_ (pp. 1-16). https://arxiv.org/abs/2006.14779

[172] Amoroso, E. M. (2011). _Cyber attacks: protecting national
infrastructure_. Butterworth-Heinemann.
https://www.elsevier.com/books/cyber-attacks/amoroso/978-1-59749-696-8

[173] Strickland, E. (2019). IBM's AI could predict psoriatic arthritis. _IEEE
Spectrum_, 56(7), 12-13.
https://spectrum.ieee.org/ibms-ai-could-predict-psoriatic-arthritis

[174] Montavon, G., Samek, W., & Müller, K. R. (2017). Methods for interpreting
and understanding deep neural networks. _Digital Signal Processing_, 73, 1-15.
https://doi.org/10.1016/j.dsp.2017.10.011

[175] Ghai, B., Terveen, L., & Bussone, A. (2021). Addressing "both sides" bias
in search results with system-level interventions. In _Proceedings of the 2021
ACM Conference on Fairness, Accountability, and Transparency_ (pp. 357-368).
https://arxiv.org/abs/2005.07282

[176] Kaur, H., Nori, H., Jenkins, S., Caruana, R., Wallach, H., & Wexler, J.
(2020). Interpreting black-box models via model extraction. _arXiv preprint
arXiv:2012.00152_. https://arxiv.org/abs/2012.00152

## TUTORIAL: ReAct (reasoning and Acting Framework for LLM Agents)

## TUTORIAL: LangChain + DoWhy (causal Model Integrated Into Agent Reasoning)
