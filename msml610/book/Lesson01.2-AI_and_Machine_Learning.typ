// git_hash=99ad2d9ee-wy8 timestamp=20260830_150733
// Import AIMA style formatting and macros.
#import "/helpers_root/dev_scripts_helpers/typst/aima_style.typ": (
  aima-style, algorithm, chapter, glossary, styled-table,
)
// Import the custom citation/bibliography system.
#import "/helpers_root/dev_scripts_helpers/typst/umd_references.typ": (
  cite, references,
)

// Document metadata
#set document(
  title: "L01.2: AI and Machine Learning",
  author: "MSML610: Advanced Machine Learning",
)

// Apply the AIMA document template (page/text/heading set + show rules).
#show: aima-style

#chapter(01, "L01.2: AI and Machine Learning")

// From: msml610/lectures_source/Lesson01.2-AI_and_Machine_Learning.smd:10 '# AI and Machine Learning'
// Slide: AI and Machine Learning
#strong[AI and Machine Learning]

// From: msml610/lectures_source/Lesson01.2-AI_and_Machine_Learning.smd:12 '## What Is AI?'
// Slide: What Is AI?
== What Is AI?

// From: msml610/lectures_source/Lesson01.2-AI_and_Machine_Learning.smd:14 '* ML, AI, and Intelligence'
// Slide: ML, AI, and Intelligence
#strong[ML, AI, and Intelligence]

- #strong[Definition]: #strong[Machine Learning] is a subset of Artificial
  Intelligence (AI). Although the term is widely used, it is often confused with
  neighboring fields such as #emph[deep learning], #emph[large-language models],
  and #emph[predictive analytics]. Each of these is related but distinct: deep
  learning is a particular family of machine-learning methods built on
  multi-layer neural networks; large-language models are a specific application
  of deep learning to natural language; and predictive analytics is a broader
  practice that may or may not involve machine learning at all. Keeping these
  distinctions clear from the outset prevents a great deal of conceptual muddle
  later on.

- #strong[Question]: What is artificial intelligence? Before answering that, it
  helps to step back and ask what #strong[human intelligence] is, since AI has
  always been defined, at least implicitly, by comparison with the human case.

- #strong[Question]: What is human intelligence? We call ourselves #emph["homo
    sapiens"] — "wise man" — precisely because intelligence is the trait we
  believe sets us apart from other animals. For thousands of years,
  philosophers, scientists, and theologians have tried to understand how we
  think, and it remains one of the #emph[biggest mysteries] in all of science.
  The human brain is a small lump of biological matter, roughly 1.4 kilograms,
  yet it has managed to grasp some of nature's deepest secrets:
  - The theory of relativity, which describes the fabric of spacetime.
  - Quantum mechanics, which governs the behavior of matter at the smallest
    scales.
  - Black holes, objects so extreme that they warp the very definitions of space
    and time.

  The puzzle is striking: how can the brain understand, predict, and manipulate
  a world that is far more complex than the brain itself? This question is not
  merely philosophical — it is directly relevant to AI research, because any
  attempt to build an intelligent machine must reckon with what intelligence
  actually requires.

// From: msml610/lectures_source/Lesson01.2-AI_and_Machine_Learning.smd:33 '* Artificial Intelligence'
// Slide: Artificial Intelligence
#strong[Artificial Intelligence]

#grid(
  columns: (80%, 20%),
  gutter: 1em,
  [
    - #strong[Definition]: The term #emph["Artificial Intelligence"] was coined
      in 1956, when a small group of researchers gathered at Dartmouth College
      to propose that "every aspect of learning or any other feature of
      intelligence can in principle be so precisely described that a machine can
      be made to simulate it" #cite("mccarthy1955dartmouth"). That ambitious
      proposal launched an entire field of study and engineering that continues
      to expand today.

    - #strong[Goal]: Artificial intelligence pursues two complementary
      objectives. The first is to #strong[understand human intelligence] — to
      build computational models that shed light on how perception, reasoning,
      language, and learning actually work in biological minds. The second is to
      #strong[create intelligent entities] that can perform tasks autonomously,
      whether or not they replicate the mechanisms found in humans. Richard
      Feynman captured the deep link between these two aims with his famous
      remark, #emph["What I cannot create, I do not understand"] (Feynman,
      1988): constructing a working system is often the most rigorous test of
      whether we truly grasp the underlying principles.

    - #strong[Characteristics]: Several features set AI apart from most other
      engineering disciplines:
      - #strong[Breadth of applicability]: AI is not confined to a single
        domain. It applies, at least in principle, to #emph[any] human activity
        and task — from medical diagnosis and legal reasoning to artistic
        creation and scientific discovery.
      - #strong[Historical significance]: Many researchers argue that the
        long-term impact of AI exceeds any past historical event, because it is
        the first technology that augments not just physical labor but cognitive
        work itself.
      - #strong[Economic scale]: The field already generates hundreds of
        billions of dollars annually in market revenue, and projections estimate
        trillions in global economic impact by 2030 #cite(
          "bughin2018aifrontier",
        ). These figures span hardware, software, services, and the productivity
        gains AI enables across other industries.
      - #strong[Open problems]: Unlike disciplines with settled core theories —
        arithmetic, for instance, or Newtonian mechanics within its domain of
        validity — AI still has many #emph[unresolved] fundamental questions.
        There is no single, universally accepted formal framework that explains
        intelligence, and active debate continues over the right
        representations, learning algorithms, and evaluation criteria. This
        makes the field simultaneously exciting and humbling: progress is rapid,
        yet the frontier of what we do not yet understand remains vast.
  ],
  [
    #figure(
      image("../lectures_source/figures/L01.2.Richard_Feynman.jpg", width: 80%),
      caption: [Richard Feynman (1965)],
      kind: "figure",
      supplement: [Fig.],
      placement: auto,
    ) <fig:richardfeynman>
  ],
)

// From: msml610/lectures_source/Lesson01.2-AI_and_Machine_Learning.smd:64 '* AI Formal Definition'
// Slide: AI Formal Definition
#strong[AI Formal Definition]

#grid(
  columns: (65%, 30%),
  gutter: 1em,
  [
    - #strong[Definition]: AI is characterized along #strong[two key axes]
      #cite("russell2020aima"). The first axis distinguishes between
      #strong[thinking] (internal reasoning processes) and #strong[acting]
      (external behavior and decision-making). The second axis contrasts
      #strong[human-like] performance — mimicking how people actually think or
      behave — with #strong[rational] performance, which measures success
      against an ideal standard of correctness.

    - #strong[Four resulting definitions]: These two axes combine to produce
      four distinct ways of defining AI, each casting the field in a different
      light. AI can be viewed as a machine that can:
      1. #strong[Think humanly] — model and replicate the cognitive processes
        humans use when reasoning, problem-solving, or making decisions.
      2. #strong[Think rationally] — apply formal logical rules to derive
        correct conclusions from given premises, following the tradition of the
        "laws of thought."
      3. #strong[Act humanly] — behave in a way that is indistinguishable from
        human behavior, as captured by benchmarks like the Turing Test.
      4. #strong[Act rationally] — select actions that maximize expected success
        given available information and goals, regardless of whether the
        underlying process resembles human cognition.

    - #strong[Question]: Which of these four definitions best captures what AI
      should ultimately aim for? Thinking humanly is limited by incomplete
      knowledge of actual human cognition. Thinking rationally runs into
      computational intractability for all but the simplest problems. Acting
      humanly sets human behavior as the gold standard, yet humans are not
      always optimal decision-makers. That leaves acting rationally as the most
      robust and general target.

    - #strong[Key idea]: Building machines that #strong[act rationally] is the
      ultimate goal of AI. A rational agent perceives its environment and
      selects actions that are expected to achieve the best outcome — or, under
      uncertainty, the best #emph[expected] outcome. This framing is powerful
      because it does not require the agent to think the way humans do, nor does
      it demand perfect logical omniscience. It only requires that the agent
      makes the best possible use of the information available to it.
      Rationality as a design target also provides a clear, measurable standard:
      we can evaluate an agent by the quality of its decisions relative to what
      could reasonably be known at the time, rather than by whether its internal
      workings mirror human psychology.
  ],
  [
    #styled-table(
      headers: ("", "Human", "Rational"),
      rows: (
        ("Thinking", "Think humanly", "Think rationally"),
        ("Acting", "Act humanly", "Act rationally"),
      ),
      bold-first-col: true,
    )
  ],
)

// From: msml610/lectures_source/Lesson01.2-AI_and_Machine_Learning.smd:101 '* 1. AI as Thinking Humanly'
// Slide: 1. AI as Thinking Humanly
#strong[1. AI as Thinking Humanly]

- #strong[Problem]: To build machines that think like humans, we must first
  #strong[determine how humans think]. This is the central challenge of the
  cognitive-modeling approach to AI: before we can replicate human-level
  reasoning in software, we need a scientific account of the internal mechanisms
  that produce it. Researchers in this tradition draw on experimental
  psychology, neuroscience, and introspection to propose computational models of
  cognition, then compare the program's input–output behavior (and, ideally, its
  intermediate steps) against data from human subjects.

- #strong[Pros]:
  - A validated cognitive model lets us express a #strong[precise theory of the
      human mind as a computer program]. Instead of vague verbal descriptions of
    how people solve problems, we get executable specifications that can be
    tested, debugged, and refined. Allen Newell and Herbert Simon's _General
    Problem Solver_ (GPS) was an early landmark: it did not merely try to solve
    problems correctly but aimed to match the order and timing of steps that
    human participants exhibited in protocol-analysis experiments. When the
    program's trace diverges from a human trace, the discrepancy points to a gap
    in the theory — turning AI development into a form of cognitive science.

- #strong[Cons]:
  - The #strong[unknown workings of the human mind] present a fundamental
    obstacle. Despite decades of research, we lack a complete, agreed-upon
    theory of how neurons give rise to reasoning, creativity, or common sense.
    Cognitive models therefore rest on incomplete evidence — behavioral data,
    reaction times, neuroimaging — and the mapping from brain to algorithm
    remains underdetermined. A program can mimic human outputs without sharing
    any of the underlying mechanisms, making it hard to know whether the model
    is genuinely explanatory or merely curve-fitting.
  - The approach also imposes an #strong[anthropocentric definition] of
    intelligence. By measuring success against human cognition, we implicitly
    assume that the way people think is the standard to emulate. This can be
    unnecessarily limiting: for many tasks — chess endgames, protein-structure
    prediction, large-scale optimization — methods that bear little resemblance
    to human thought processes vastly outperform human experts. Tying AI to
    human cognition risks overlooking superior strategies simply because they do
    not mirror what a person would do.

// From: msml610/lectures_source/Lesson01.2-AI_and_Machine_Learning.smd:113 '* 2. AI as Thinking Rationally'
// Slide: 2. AI as Thinking Rationally
#strong[2. AI as Thinking Rationally]

#grid(
  columns: (65%, 30%),
  gutter: 1em,
  [
    - #strong[Question]: What are the rules of correct thinking? Given correct
      premises, a system of correct thinking must yield correct conclusions.

    - #strong[Techniques]: #strong[Logic] studies the "laws of thought" by
      formalizing statements about objects and the relations that hold among
      them. Through precise symbolic notation, logic provides the foundation for
      determining whether an argument is valid — that is, whether its
      conclusions follow necessarily from its premises.

    - #strong[Techniques]: #strong[Automatic theorem proving] builds on this
      logical foundation. Theorem-proving programs accept problems expressed in
      logical notation and search for proofs or refutations. A key limitation,
      however, is that first-order validity is only #emph[semi-decidable]: a
      prover will eventually find a proof if one exists, but it may run
      indefinitely when no solution exists, with no guarantee of termination in
      the negative case.
  ],
  [
    // rendered_images:begin
    //     ```graphviz
    //     digraph laws_of_thought {
    //         bgcolor="transparent";
    //         pad="0.15";
    //         splines=spline;
    //         nodesep=0.4;
    //         ranksep=0.5;
    //         rankdir=TB;
    //
    //         node [shape=box,
    //               style="rounded,filled",
    //               penwidth=1.8,
    //               fontname="Helvetica",
    //               fontsize=12,
    //               margin="0.22,0.14",
    //               height=0.50];
    //
    //         edge [color="#A3B1C0",
    //               penwidth=1.3,
    //               arrowhead=vee,
    //               arrowsize=0.75,
    //               fontname="Helvetica",
    //               fontsize=10,
    //               fontcolor="#7B8794"];
    //
    //         premises [label="Correct\npremises", fillcolor="#A9DDB0", color="#4F9A5C", fontcolor="#1F4E2E"];
    //         logic [label="Logic", fillcolor="#FFC98A", color="#D98E2B", fontcolor="#6B4517"];
    //         conclusion [label="Correct\nconclusions", fillcolor="#9CC4F2", color="#3C6FB0", fontcolor="#1F4E79"];
    //
    //         premises -> logic -> conclusion;
    //     }
    //     ```
    // rendered_images:end
    // render_images:begin
    #figure(
      image(
        "Lesson01.2-AI_and_Machine_Learning.typ.figs/Lesson01.2-AI_and_Machine_Learning.1.png",
      ),
    )
    // render_images:end
  ],
)

// From: msml610/lectures_source/Lesson01.2-AI_and_Machine_Learning.smd:168 '* Thinking Rationally: Challenges'
// Slide: Thinking Rationally: Challenges
#strong[Thinking Rationally: Challenges]

- #strong[Challenges]:

  + #strong[Formalizing informal knowledge is difficult.] Everyday concepts that
    humans grasp effortlessly can become enormously complex when expressed in
    formal logic. Consider a seemingly simple action like a handshake: #emph[two
      people extend their hands toward each other, grip, shake, and release.]
    Translating this into logical notation requires spelling out every entity
    and relation explicitly:

    $
      exists x, y, h_x, h_y quad & "Person"(x) and "Person"(y) and x eq.not y and "Hand"(x, h_x) and "Hand"(y, h_y) \
      and & "MoveToward"(h_x, h_y) and "Contact"(h_x, h_y) \
      and & "Shake"(h_x, h_y) and "Release"(h_x, h_y)
    $

    Even this formalization glosses over subtleties — timing, social context,
    force — that a human understands without effort. The gap between intuitive
    understanding and formal specification remains one of the deepest obstacles
    in knowledge representation.

  + #strong[Probabilistic nature of knowledge.] Much of what we know about the
    world is uncertain rather than categorical. In medicine, for instance,
    #emph[fever, cough, and fatigue could indicate flu, COVID-19, or another
      illness entirely.] A purely logical system that demands definitive truth
    values struggles with this kind of ambiguity. Handling uncertainty well
    requires probabilistic reasoning frameworks — Bayesian networks,
    probabilistic graphical models — that can weigh evidence and assign degrees
    of belief rather than binary truth.

  + #strong[Scalability challenges.] Even when a problem can be formally
    specified and its uncertainty properly modeled, the sheer size of realistic
    domains often makes exact solutions computationally intractable. Search
    spaces grow exponentially, inference in richly connected probabilistic
    models is NP-hard in general, and planning over long horizons compounds the
    difficulty further. In practice, large problems demand heuristics,
    approximations, and domain-specific shortcuts to arrive at practical
    solutions within acceptable time and resource budgets.

  + #strong[Intelligence requires more than rational thinking.] An agent that
    reasons flawlessly in its head but never acts accomplishes nothing. Real
    intelligence demands interaction with the world — perceiving the
    environment, executing actions, and adapting to feedback. This is the
    problem of the #strong[embodiment of AI]: cognition does not exist in a
    vacuum but is deeply coupled with a physical or virtual body that senses and
    manipulates its surroundings. Designing agents that close this
    perception–action loop effectively remains a central challenge in AI
    research.

// From: msml610/lectures_source/Lesson01.2-AI_and_Machine_Learning.smd:193 '* 3. AI as Acting Humanly'
// Slide: 3. AI as Acting Humanly
#strong[3. AI as Acting Humanly]

#grid(
  columns: (75%, 25%),
  gutter: 1em,
  [
    - #strong[Components]: Passing the #strong[(embodied) Turing test] requires
      a broad suite of capabilities, each corresponding to a major subfield of
      AI:

      + #strong[Natural language processing] to communicate successfully in a
        human language — understanding questions, generating coherent replies,
        and maintaining context across a conversation.
      + #strong[Knowledge representation] to store what the agent knows or
        learns about the world in a structured form that supports later
        retrieval and inference.
      + #strong[Automated reasoning] to draw conclusions from stored knowledge,
        answer novel questions, and chain together facts to solve problems.
      + #strong[Machine learning] to detect patterns in data, adapt to new
        situations, and extrapolate beyond what has been explicitly programmed.
      + #strong[Computer vision and speech recognition] to perceive the
        environment — recognizing objects, reading text, and understanding
        spoken language as a human would.
      + #strong[Robotics] to manipulate physical objects and navigate the real
        world, closing the loop between perception and action.

    Together, these six competencies define what it means for an agent to be
    indistinguishable from a human not only in conversation but also in physical
    interaction — hence the qualifier #emph[embodied].
  ],
  [
    #figure(
      image("../lectures_source/figures/L01.1.Ex_machina.jpg", width: 80%),
      caption: [Ex machina],
      kind: "figure",
      supplement: [Fig.],
      placement: auto,
    ) <fig:exmachina>
  ],
)

// From: msml610/lectures_source/Lesson01.2-AI_and_Machine_Learning.smd:223 '* Turing Test: Pros and Cons'
// Slide: Turing Test: Pros and Cons
#strong[Turing Test: Pros and Cons]

#grid(
  columns: (50%, 50%),
  gutter: 1em,
  [
    - #strong[Pros]: Rational-agent design offers an #emph[operational]
      definition of intelligence — one grounded in measurable behavior rather
      than introspection. Instead of asking unanswerable questions such as "What
      is consciousness?" or "Can a machine truly think?", we ask whether the
      agent consistently selects actions that maximize its expected performance
      given the information available. This sidesteps centuries of philosophical
      vagueness and gives engineers a concrete objective to optimize against.
  ],
  [
    - #strong[Cons]:
      - Intelligence is defined by #strong[anthropomorphic] criteria — that is,
        strictly in human terms. This is a significant limitation because
        multiple forms of non-human intelligence exist (consider, for example,
        the navigational abilities of migratory birds or the collective
        problem-solving of ant colonies), none of which would register on a test
        designed to mimic human conversation.
      - Passing the test ultimately means #strong[fooling humans] into believing
        the machine is human, which conflates the ability to deceive with
        genuine understanding or competence.
  ],
)

// From: msml610/lectures_source/Lesson01.2-AI_and_Machine_Learning.smd:248 '* 4. AI as Acting Rationally'
// Slide: 4. AI as Acting Rationally
#strong[4. AI as Acting Rationally]

- #strong[Definition]: A #strong[rational agent] is an agent that does the
  "right thing" given what it knows. More precisely, a rational agent selects
  actions that are expected to maximize its performance measure, based on the
  evidence provided by its percept sequence and whatever built-in knowledge it
  possesses. Rationality, then, is not about omniscience or infallibility — it
  is about making the best possible decision with the information currently
  available.

- #strong[Characteristics]: Agents that #strong[act rationally] should exhibit
  several key properties:
  1. #strong[Operate autonomously] — rely on their own percepts and learned
    knowledge rather than depending entirely on a human designer's prior
    specification of every possible situation.
  2. #strong[Perceive their environment] — gather information through sensors so
    that decisions are grounded in the actual state of the world rather than
    assumptions alone.
  3. #strong[Persist over time] — maintain continuity of operation, accumulating
    experience and updating internal state rather than treating every moment as
    an isolated event.
  4. #strong[Adapt to change] — adjust behavior when the environment shifts in
    unexpected ways, rather than rigidly following a fixed policy that may have
    become outdated.
  5. #strong[Create and pursue goals] — formulate objectives (or accept
    externally specified ones) and select actions directed toward achieving
    them, closing the loop between perception and purposeful action.

These five characteristics collectively distinguish a rational agent from a
simple reactive program. A thermostat, for instance, perceives temperature and
acts by toggling a heater, but it neither adapts to novel situations nor pursues
richer goals. A self-driving car, by contrast, must do all five: it senses
traffic, persists across an entire trip, adapts to construction detours, and
continually plans a route toward its destination — all without a human
micromanaging every steering correction. The richer the environment, the more
these characteristics matter, because a brittle, non-adaptive system will
inevitably encounter situations its designer never anticipated.

// From: msml610/lectures_source/Lesson01.2-AI_and_Machine_Learning.smd:260 '* Acting Rationally as Ultimate Goal of AI'
// Slide: Acting Rationally as Ultimate Goal of AI
#strong[Acting Rationally as Ultimate Goal of AI]

#grid(
  columns: (65%, 30%),
  gutter: 1em,
  [
    - #strong[Question]: Which definition of AI best captures what we should
      build? The debate typically centers on two axes: acting versus thinking,
      and rational versus human-like.

    - #strong[Acting is more fundamental than Thinking]: acting rationally is a
      broader objective than thinking rationally. A system that acts rationally
      must still reason, but it must also handle perception, uncertainty, and
      real-time constraints that pure reasoning ignores. Correct inference is
      one tool an agent can use, but it is not the only one, and in many
      practical situations an agent must act even when provably correct
      inference is infeasible.

    - #strong[Rational is more objective than Human]: rationality can be
      mathematically defined — for example, through expected-utility
      maximization — giving us a clear, measurable standard for evaluating
      system behavior. Human behavior, by contrast, is shaped by millions of
      years of evolutionary pressure and is riddled with cognitive biases,
      heuristics, and inconsistencies. Modeling AI on human cognition therefore
      imports those limitations rather than transcending them.

    - #strong[Key idea]: AI should focus on #strong[agents acting rationally].
      This stance combines the best of both axes: it privileges action over mere
      thought, and it anchors evaluation in a formal, objective criterion rather
      than in the idiosyncrasies of human psychology.
  ],
  [
    #styled-table(
      headers: ("", "Human", "Rational"),
      rows: (
        ("Thinking", "Think humanly", "Think rationally"),
        ("Acting", "Act humanly", "*Act rationally*"),
      ),
      bold-first-col: true,
    )
  ],
)

// From: msml610/lectures_source/Lesson01.2-AI_and_Machine_Learning.smd:295 '* Rationality Is Not Absolute'
// Slide: Rationality Is Not Absolute
#strong[Rationality Is Not Absolute]

- #strong[Problem]: AI aims to build agents that #strong[do the right thing] —
  but defining what counts as the "right thing" is far from straightforward. The
  answer depends on the information available to the agent at the time it acts,
  the costs and benefits of alternative actions, and sometimes on deeper ethical
  considerations that resist easy formalization.

- #strong[Example — getting struck by a branch]: Suppose you leave the house and
  a falling branch strikes you. Did you act rationally? Almost certainly yes.
  You had no reason to anticipate the branch, and the cost of checking every
  tree before stepping outside would be absurdly high relative to the tiny
  probability of the event. Rationality does not demand omniscience; it demands
  making the best decision given the information at hand.

- #strong[Example — crossing the street without looking]: Now suppose you cross
  the street without checking for oncoming traffic and a car knocks you over.
  Did you act rationally? Almost certainly not. Glancing left and right takes a
  fraction of a second — an extremely low-cost action — yet it dramatically
  reduces the chance of a catastrophic outcome. A rational agent weighs the cost
  of gathering information against the expected harm of acting without it, and
  here the balance clearly favors looking first.

- #strong[Challenges — moral dilemmas in self-driving cars]: These questions
  become even harder when ethical trade-offs are involved. Consider the classic
  trolley-style scenario for autonomous vehicles: should a self-driving car
  swerve and hit a pedestrian to avoid a frontal crash that would kill two
  occupants? There is no universally accepted answer. Different ethical
  frameworks — utilitarian calculus, deontological rules, virtue ethics — yield
  conflicting prescriptions. Encoding any single framework into an agent's
  decision policy means implicitly choosing whose values the system embodies,
  which raises profound questions about accountability, fairness, and public
  trust. Designing agents that "do the right thing" therefore requires grappling
  not only with uncertainty and information costs but also with the limits of
  formal rationality in morally charged situations.

// From: msml610/lectures_source/Lesson01.2-AI_and_Machine_Learning.smd:313 '* Problems of a Rational Agent'
// Slide: Problems of a Rational Agent
#strong[Problems of a Rational Agent]

- #strong[Challenges — Probabilistic environment]: A rational agent operates in
  a world riddled with uncertainty. In a fully deterministic setup the agent
  simply aims for the best possible outcome, but once the environment becomes
  probabilistic the goal shifts to achieving the #strong[best expected outcome].
  Expected here carries its statistical meaning: the agent must weigh each
  possible result by its probability and choose the action whose weighted
  average payoff is highest.

- #strong[Problem — What does "best" mean?] The classical answer is that "best"
  is determined by an #strong[objective function] — a single scalar quantity the
  agent tries to maximise or minimise. Depending on the field this function goes
  by different names: a cost function in optimisation, a sum of rewards in
  reinforcement learning, a loss function in supervised learning, or a utility
  function in decision theory. All of these are mathematically equivalent up to
  sign conventions: maximising utility is the same as minimising negative
  utility. Yet in practice, defining "best" is rarely so tidy. Real objectives
  are multi-dimensional, partially conflicting, and sometimes impossible to
  specify precisely — a challenge that will recur throughout the course.

- #strong[Limitations]:
  - #strong[Omniscience vs no-regrets]: the best decision is based on available
    information, not perfect knowledge. An agent that acts optimally given what
    it currently knows may still suffer a bad outcome; the standard of
    rationality is #emph[no regrets] — would you make the same choice again with
    the same information?
  - Sometimes #strong[no provably correct action] exists, yet the agent must
    still act. Deferring action indefinitely is itself an action with
    consequences.
  - Even #strong[with perfect information] rationality may not be feasible
    because of:
    - #strong[Data-acquisition cost]: gathering all relevant data may be
      prohibitively expensive or harmful — ordering every conceivable medical
      test for a patient is neither economical nor ethical.
    - #strong[Computational demands]: exhaustively searching a decision tree
      whose branches outnumber the atoms in the observable universe
      ($approx 10^(80)$) is physically impossible regardless of hardware.
    - #strong[Real-time demands]: in high-frequency trading a decision may need
      to be made within one microsecond, far less time than any exact
      optimisation algorithm could require.

- #strong[Solution — "Satisficing"]: When optimality is out of reach, the
  pragmatic alternative is #strong[satisficing] — selecting an action that is
  #emph[good enough] rather than perfect #cite("simon1956satisficing"). A
  satisficing agent sets an aspiration level and accepts the first option that
  meets it, thereby acting appropriately given the constraints of time,
  computation, and information it faces. This concept, introduced by Herbert
  Simon, remains one of the most influential ideas in bounded rationality and
  underpins much of modern AI system design.

// From: msml610/lectures_source/Lesson01.2-AI_and_Machine_Learning.smd:340 '## What Is Machine Learning?'
// Slide: What Is Machine Learning?
== What Is Machine Learning?

// From: msml610/lectures_source/Lesson01.2-AI_and_Machine_Learning.smd:342 '* Machine Learning: Definitions'
// Slide: Machine Learning: Definitions
#strong[Machine Learning: Definitions]

#grid(
  columns: (75%, 20%),
  gutter: 1em,
  [
    - #strong[Question]: How should we #strong[define machine learning]?

    - #strong[Definition]: Arthur Samuel offered one of the earliest and most
      intuitive characterizations: #emph["Machine learning is the field of study
        that gives computers the ability to learn without being explicitly
        programmed"] (Samuel, 1959) #cite("samuel1959checkers"). In other words,
      machine learning builds machines that do #emph[useful things] without a
      developer having to hand-code every rule. Samuel's own checkers-playing
      program illustrated the idea nicely: the computer learned by playing
      thousands of games against itself and memorizing which board positions
      tended to lead to wins, gradually improving without any new instructions
      from its programmer.

      Tom Mitchell later sharpened the concept into a more formal definition:
      #emph["A computer program is said to learn from experience $E$ with
        respect to some task $T$ and some performance measure $P$, if $P(T)$
        improves with experience $E$"] (Mitchell, 1997) #cite(
        "mitchell1997machinelearning",
      ). This formulation is useful because it makes the three ingredients of
      any learning problem explicit — the task we care about, the experience
      (data) the system trains on, and the metric we use to judge whether it is
      actually getting better.

    - #strong[Applications]: Common machine learning examples that put these
      ideas into practice include:
      - #strong[Computer vision] — recognizing objects, faces, or scenes in
        images and video.
      - #strong[Speech recognition] — converting spoken language into text, as
        in virtual assistants and transcription services.
      - #strong[Natural language processing] — enabling machines to understand,
        generate, and translate human language.
  ],
  [
    #figure(
      image("../lectures_source/figures/L01.2.Tom_Mitchell.jpg", width: 80%),
      caption: [Tom Mitchell (2025)],
      kind: "figure",
      supplement: [Fig.],
      placement: auto,
    ) <fig:tommitchell>
  ],
)

// From: msml610/lectures_source/Lesson01.2-AI_and_Machine_Learning.smd:374 '* The 3 Machine Learning Assumptions'
// Slide: The 3 Machine Learning Assumptions
#strong[The 3 Machine Learning Assumptions]

- #strong[Fact]: Machine learning solves a practical problem that unfolds across
  several phases: gathering a dataset, #emph[building a statistical model from
    the dataset algorithmically], evaluating the model, and finally deploying
  and monitoring the model in production. Each phase carries its own challenges,
  but the algorithmic construction of the model is where the core intellectual
  contribution of ML lies.

- #strong[Problem] (Abu-Mostafa, 2012) #cite("abumostafa2012learning"): Most of
  these phases are "engineering" — collecting data, cleaning it, deploying
  infrastructure, monitoring drift. Building the model, however, is the
  "research" part: it is where theory meets practice. Abu-Mostafa identifies
  #strong[three core assumptions] that underpin any machine learning endeavor:
  1. A #emph[pattern exists] in the data — there is some regularity to be
    discovered.
  2. The pattern cannot be #emph[precisely defined mathematically] — if we could
    write down a closed-form solution, we would not need learning.
  3. #emph[Data is available] — we have observations from which the algorithm
    can extract the pattern.

- #strong[Question]: Which of these three assumptions is truly
  #strong[essential]?
  1. If no pattern exists, does it make sense to run a learning algorithm? Not
    really — but in practice we rarely know for certain whether a pattern exists
    until we try, so this assumption is more of a prerequisite hope than a hard
    gate.
  2. Is it a problem if mathematics can devise the pattern but we still use
    machine learning? Not at all — ML can still be useful even when an
    analytical solution exists, for instance when the closed-form solution is
    computationally expensive or when an approximate learned model generalizes
    better under noise.
  3. Can progress happen without data? This is the hard constraint.

- #strong[Remark]: #emph[Without data, no progress is possible.] Data
  availability is the assumption that is truly essential. The first two
  assumptions are desirable and shape how useful the learned model will be, but
  the third is non-negotiable: a learning algorithm with no observations has
  nothing to learn from. This is why so much of modern ML research — from data
  augmentation to synthetic data generation to active learning — revolves around
  obtaining, enriching, or efficiently using data.

// From: msml610/lectures_source/Lesson01.2-AI_and_Machine_Learning.smd:399 '* AI vs ML vs Deep Learning'
// Slide: AI vs ML vs Deep Learning
#strong[AI vs ML vs Deep Learning]

#grid(
  columns: (65%, 30%),
  gutter: 1em,
  [
    - #strong[Definition]:
      - #strong[AI (Artificial Intelligence)]: machines programmed to reason,
        learn, and act in a rational way. The term covers any system that
        exhibits behaviour we would consider "intelligent," whether or not the
        system learns from data.
      - #strong[ML (Machine Learning)]: machines capable of performing tasks
        without being explicitly programmed for each case. Instead of following
        hand-written rules, an ML system extracts patterns from data and
        generalises to new inputs.
      - AI models that are not ML are entirely possible. A handcrafted
        rule-based system such as IBM Deep Blue, which played championship-level
        chess using search trees and expert-tuned evaluation functions,
        qualifies as AI yet involves no learning from data whatsoever.

    - #strong[Definition]:
      - #strong[DL (Deep Learning)]: a subfield of ML that uses a particular
        family of models — neural networks with many layers — to learn
        hierarchical representations of data. Depth allows these networks to
        compose simple features into increasingly abstract concepts.
      - #strong[LLM (Large Language Models)]: neural networks trained on massive
        #emph[text] datasets to predict text, often further tuned with
        reinforcement learning from human feedback (RLHF) #cite(
          "ouyang2022instructgpt",
        ). LLMs are a specific application of deep learning focused on natural
        language.
      - DL models that are not LLMs are common. For example, a convolutional
        neural network designed for image classification or a recurrent network
        built for speech recognition is a deep learning system but not an LLM,
        because it operates on visual or auditory data rather than text.
  ],
  [
    // rendered_images:begin
    //     ```tikz
    //     % Define colors.
    //       \definecolor{AIcolor}{RGB}{244,166,166}    % Red/Pink
    //       \definecolor{MLcolor}{RGB}{178,226,178}    % Green
    //       \definecolor{DLcolor}{RGB}{160,214,209}    % Teal
    //       \definecolor{LLMcolor}{RGB}{198,166,244}   % Purple
    //
    //       % Draw AI circle
    //       \fill[AIcolor] (0,0) circle (3);
    //       \draw (0,0) circle (3);
    //       \node[above] at (0,2) {\textbf{AI}};
    //
    //       % Draw ML circle inside AI
    //       \fill[MLcolor] (0.5,-0.5) circle (2);
    //       \draw (0.5,-0.5) circle (2);
    //       \node[above] at (0.5,0.5) {\textbf{ML}};
    //
    //       % Draw DL circle inside ML
    //       \fill[DLcolor] (1,-1) circle (1);
    //       \draw (1,-1) circle (1);
    //       \node[above] at (1,-0.6) {\textbf{DL}};
    //
    //       % Draw LLM circle inside DL
    //       \fill[LLMcolor] (1.2,-1.2) circle (0.6);
    //       \draw (1.2,-1.2) circle (0.6);
    //       \node[above] at (1.2,-1.4) {\textbf{LLMs}};
    //     ```
    // rendered_images:end
    // render_images:begin
    #figure(
      image(
        "Lesson01.2-AI_and_Machine_Learning.typ.figs/Lesson01.2-AI_and_Machine_Learning.2.png",
      ),
    )
    // render_images:end
  ],
)

// From: msml610/lectures_source/Lesson01.2-AI_and_Machine_Learning.smd:457 '* Limits of AI Compared to Human Intelligence (1/2)'
// Slide: Limits of AI Compared to Human Intelligence (1/2)
#strong[Limits of AI Compared to Human Intelligence (1/2)]

- #strong[Problem]: AI and ML differ fundamentally from human intelligence.
  Machines do not learn the way humans do — large language models, for instance,
  process language through statistical patterns over massive corpora rather than
  through grounded experience. Whether the brain uses anything resembling
  gradient descent remains an open question in computational neuroscience; the
  evidence is far from conclusive. Reinforcement learning, on the other hand,
  has a somewhat stronger biological analogue: dopaminergic reward signals in
  the brain bear a resemblance to temporal-difference learning, so the brain
  probably does employ a form of reinforcement learning, albeit one that differs
  substantially from the algorithms used in practice.

- #strong[Limitations]:
  - #strong[Fragility to input variations]: ML models can fail catastrophically
    when faced with slight distortions of their inputs. Adversarial attacks
    demonstrate this vividly — altering a single pixel in an image can cause a
    classifier to switch its prediction entirely #cite("su2019onepixel").
    Similarly, a reinforcement learning agent trained to play a video game may
    collapse if the screen is rotated by a few degrees, even though a human
    player would adapt effortlessly. This brittleness reveals that current
    models often latch onto superficial statistical regularities rather than
    learning robust, generalizable representations.
  - #strong[Lack of transfer learning]: Human learners routinely carry knowledge
    from one domain to another — understanding physics helps when learning
    engineering, and literacy in one language accelerates acquisition of a
    second. ML systems, by contrast, typically cannot apply what they have
    learned in one task to a different task without substantial retraining or
    fine-tuning. Despite progress in foundation models and multi-task learning,
    genuine flexible transfer remains elusive.
  - #strong[Massive data and compute requirements]: Modern ML demands enormous
    datasets and computational resources. Consider driving: a teenager can learn
    to operate a car competently in a matter of hours behind the wheel, drawing
    on years of accumulated perceptual and motor experience. Self-driving
    systems, however, require billions of compute hours, petabytes of sensor
    data, and extensive simulation environments before they reach comparable
    competence — and even then they struggle with rare edge cases that a human
    handles intuitively.
  - #strong[Poor common sense and reasoning]: Perhaps the most persistent gap is
    the absence of common-sense knowledge. Humans bring a lifetime of intuitive
    physics, social understanding, and causal reasoning to every task. ML models
    lack this built-in world knowledge, which is why they can produce confident
    but nonsensical answers — correctly identifying objects in an image yet
    failing to reason about what would happen if one of those objects were
    removed or moved.

// From: msml610/lectures_source/Lesson01.2-AI_and_Machine_Learning.smd:480 '* Limits of AI Compared to Human Intelligence (2/2)'
// Slide: Limits of AI Compared to Human Intelligence (2/2)
#strong[Limits of AI Compared to Human Intelligence (2/2)]

- #strong[Limitations]:
  - #strong[Opaque decision-making]: many ML models offer little transparency
    into how they arrive at their decisions. This opacity limits trust,
    interpretability, and accountability, especially in critical applications
    such as healthcare, criminal justice, and autonomous driving where
    stakeholders need to understand #emph[why] a particular decision was made.
  - #strong[Dependence on narrow objectives]: ML systems excel at optimizing
    well-defined, narrow tasks but struggle when goals are ambiguous or
    multifaceted. For example, a recommendation algorithm that maximizes user
    engagement may end up promoting sensationalist or harmful content, because
    engagement is only a proxy for the broader goal of user well-being.
  - #strong[Susceptibility to bias and data quality]: models inherit and can
    amplify biases present in their training data. If historical data reflects
    discriminatory patterns, the learned model will reproduce — and often
    reinforce — those same patterns in its predictions.
  - #strong[Lack of embodiment and physical interaction]: human cognition is
    deeply grounded in physical and sensory experience. Current ML systems
    operate on abstract numerical representations and lack the embodied
    understanding that comes from interacting with the physical world, limiting
    their ability to generalize the way humans do.

// From: msml610/lectures_source/Lesson01.2-AI_and_Machine_Learning.smd:494 '* Key Takeaways'
// Slide: Key Takeaways
#strong[Key Takeaways]

- #strong[Key idea]: AI should focus on #strong[agents acting rationally], not
  on mimicking human thought or behavior. Rather than asking whether a machine
  can replicate the way people think or behave, the more productive question is
  whether it can select actions that maximize progress toward its goals given
  the information available.

- #strong[Definition]:
  - #strong[AI] (Artificial Intelligence): machines programmed to reason, learn,
    and act rationally.
  - #strong[ML] (Machine Learning): a subset of AI in which systems learn to
    perform tasks from data without being explicitly programmed for each case.
  - #strong[DL] (Deep Learning): a subset of ML that uses multi-layer neural
    networks to learn hierarchical representations of data.
  - #strong[LLM] (Large Language Model): a subset of DL trained on massive text
    datasets to predict the next token in a sequence, often further refined with
    Reinforcement Learning from Human Feedback (RLHF) to align outputs with
    human preferences.

  Each layer in this hierarchy builds on the one below it: deep learning is a
  particular technique within machine learning, which is itself one approach to
  building artificially intelligent systems. Understanding where a given method
  sits in this stack helps clarify both its capabilities and its limitations.

- #strong[Remark]: Current ML and DL systems, despite their impressive
  performance on benchmarks and specific tasks, still fall short of human
  intelligence in several important respects. They tend to be #strong[fragile],
  failing unpredictably when inputs shift even slightly from the training
  distribution. They struggle with #strong[transfer learning], meaning that
  knowledge gained on one task does not easily carry over to related problems
  the way it does for humans. They are #strong[data-inefficient], often
  requiring millions of examples to learn patterns a person can grasp from a
  handful. Finally, they lack #strong[common-sense reasoning]—the broad,
  implicit understanding of how the physical and social world works that humans
  acquire effortlessly through everyday experience. These gaps are a central
  motivation for ongoing research in AI.

// From: msml610/lectures_source/Lesson01.2-AI_and_Machine_Learning.smd:510 '* References'
// Slide: References
#strong[References]

#set text(size: 0.75em)
#references("/msml610/lectures_source/refs.bib")
