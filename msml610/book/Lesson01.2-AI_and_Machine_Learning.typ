// git_hash=502eb3ce4-l0s timestamp=20260830_103822
// Import AIMA style formatting and macros.
#import "../../helpers_root/dev_scripts_helpers/typst/aima_style.typ": (
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

- #strong[Definition]: #strong[Machine Learning] is a subset of
  #strong[Artificial Intelligence (AI)]. It is important to note that machine
  learning is often confused with other related fields such as #emph[deep
    learning], #emph[large-language models], and #emph[predictive analytics].
  Each of these fields has its own focus and methodology, but they all fall
  under the broader umbrella of artificial intelligence.

- #strong[Question]: What is artificial intelligence? To grasp the concept of
  artificial intelligence, we must first understand what #strong[human
    intelligence] entails. Human intelligence comprises our cognitive abilities,
  allowing us to learn, reason, solve problems, and adapt to new situations.

- #strong[Question]: What is human intelligence? The term #emph["homo sapiens"]
  signifies that intelligence is a defining trait that sets us apart from other
  animals. For thousands of years, humanity has sought to understand the
  intricacies of our thought processes. This quest to comprehend our
  intelligence unveils one of the #emph[biggest mysteries]: despite the small
  size of our brains, we have developed the capacity to grasp nature's most
  profound secrets. Remarkable concepts such as the theory of relativity,
  quantum mechanics, and black holes were constructed by our minds. This raises
  an intriguing question: how can the brain comprehend, predict, and manipulate
  a world that is far more complex than itself?

// From: msml610/lectures_source/Lesson01.2-AI_and_Machine_Learning.smd:33 '* Artificial Intelligence'
// Slide: Artificial Intelligence
#strong[Artificial Intelligence]

#grid(
  columns: (80%, 20%),
  gutter: 1em,
  [
    - #strong[Definition]: The term "Artificial Intelligence" was coined in 1956
      #cite("mccarthy1955dartmouth").

    - #strong[Goal]:
      - The primary goals of Artificial Intelligence (AI) are to understand
        human intelligence and to create intelligent entities.
      - As physicist Richard Feynman articulated in 1988, “What I cannot create,
        I do not understand.” This principle underscores the notion that deep
        understanding is intertwined with the ability to replicate cognitive
        processes.

    - #strong[Characteristics]:
      - AI can be applied to any human activity and task, which highlights its
        versatility and broad relevance.
      - The impact of AI is projected to exceed that of any past historical
        event, signifying a transformative potential across various domains of
        society.
      - Presently, AI generates hundreds of billions of dollars annually in
        market revenue, with projections estimating that it could contribute
        trillions to the global economy by 2030 #cite("bughin2018aifrontier").
        This financial aspect emphasizes the growing importance of AI in
        economic development and innovation.
      - Despite its rapid advancements, AI still faces many unresolved problems,
        contrasting with other disciplines that have established core theories,
        such as arithmetic or Newtonian mechanics. This ongoing challenge
        reflects the dynamic and evolving nature of AI research and its
        application.
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
      #cite("russell2020aima"):
      - #strong[Thinking vs. Acting]
      - #strong[Human vs. Rational (ideal performance)]

    - #strong[Four resulting definitions]: AI as a machine that can:
      1. Think humanly
      2. Think rationally
      3. Act humanly
      4. Act rationally

    - #strong[Question]: Which definition best captures what AI should aim for?

    - #strong[Key idea]: Building machines that #strong[act rationally] is the
      ultimate goal of AI.
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
  #strong[determine how humans think]. Understanding human cognition is a complex
  challenge due to the intricacies of human thought processes and mental
  representations.

- #strong[Pros]:
  - By expressing a precise theory of the human mind as a computer program, we
    can develop models that not only simulate human-like thinking but also
    potentially outperform human decision-making in specific domains.

- #strong[Cons]:
  - The unknown workings of the human mind present a significant limitation, as
    we may lack the comprehensive understanding necessary to accurately
    replicate thought processes in machines.
  - There is also an anthropocentric definition to consider, which centers our
    understanding of intelligence around human experiences and may not encompass
    other forms of intelligence that could exist.

// From: msml610/lectures_source/Lesson01.2-AI_and_Machine_Learning.smd:113 '* 2. AI as Thinking Rationally'
// Slide: 2. AI as Thinking Rationally
#strong[2. AI as Thinking Rationally]

#grid(
  columns: (65%, 30%),
  gutter: 1em,
  [
    - #strong[Question]: What are the rules of #strong[correct thinking]?
      - Given correct premises, one can yield correct conclusions. This
        principle underscores the importance of beginning with accurate and
        reliable information when engaging in reasoning processes. If the
        premises are valid, the conclusions derived from them will also hold
        true, thereby establishing a foundation for sound logical inference.

    - #strong[Techniques]: #strong[Logic] studies the "laws of thought".
      - Logic serves as a formal system that allows us to analyze and validate
        arguments. It aims to formalize statements concerning objects and their
        relationships. By doing so, logic provides tools and frameworks to
        ensure conclusions follow logically from premises, enabling clearer
        reasoning and communication of complex ideas.

    - #strong[Techniques]: #strong[Automatic theorem proving]
      - This involves using computer programs to solve problems expressed in
        logical notation. Automatic theorem provers are designed to establish
        the validity of given logical statements. However, it is critical to
        note that these programs can run indefinitely if no solutions exist for
        a particular problem. This is due to the nature of first-order validity
        being only semi-decidable, which means that there is no guaranteed
        method or algorithm that can determine the truth of every statement in
        all possible cases.
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
  image("Lesson01.2-AI_and_Machine_Learning.typ.figs/Lesson01.2-AI_and_Machine_Learning.1.png"),
)
// render_images:end
  ],
)

// From: msml610/lectures_source/Lesson01.2-AI_and_Machine_Learning.smd:168 '* Thinking Rationally: Challenges'
// Slide: Thinking Rationally: Challenges
#strong[Thinking Rationally: Challenges]

- #strong[Challenges]:
  1. #strong[Formalizing informal knowledge is difficult]:
    - For instance, consider the description: "A handshake occurs when two
      people extend, grip, shake hands, then release." This seemingly simple
      action encompasses a variety of interactions and processes that can be
      challenging to define rigorously in a formal system. In formal notation,
      one might express this as:
      $$
      \begin{aligned} & \exists \; x, y, h_x, h_y \\ & \quad Person(x) \land
      Person(y) \land x \neq y \land {} \\ & Hand(x, h_x) \land Hand(y, h_y)
      \land {} \\ & \quad MoveToward(h_x, h_y) \land Contact(h_x, h_y) \land {}
      \\ & \quad Shake(h_x, h_y) \land {} \\ & \quad Release(h_x, h_y) \\
      \end{aligned}
      $$
      This captures the essential elements of a handshake in a formal logical
      expression, highlighting the complexities involved in translating informal
      knowledge into formal representations.
  2. #strong[Probabilistic nature of knowledge]:
    - An example from medicine illustrates this concept: "Fever, cough, and
      fatigue could indicate flu, COVID-19, or another illness." Here, the
      classification of symptoms demonstrates that knowledge in this domain is
      inherently probabilistic, where multiple conclusions might arise from the
      same evidence, necessitating careful consideration of context and
      uncertainty in diagnosis.
  3. #strong[Scalability challenges]:
    - When dealing with large problems, there is often a necessity to employ
      heuristics to develop practical solutions. Heuristics can simplify complex
      problem-solving processes, enabling systems to respond effectively even in
      scenarios where exhaustive computational resources may be impractical.
  4. #strong[Intelligence requires more than rational thinking]:
    - An intelligent agent must engage with its environment to exhibit true
      intelligence. This aspect brings to light the challenge of the "embodiment
      of AI," requiring systems not only to reason logically but also to
      interact and learn from the world in meaningful ways.

// From: msml610/lectures_source/Lesson01.2-AI_and_Machine_Learning.smd:193 '* 3. AI as Acting Humanly'
// Slide: 3. AI as Acting Humanly
#strong[3. AI as Acting Humanly]

#grid(
  columns: (75%, 25%),
  gutter: 1em,
  [
    - #strong[Components]:
      - Passing the #strong[(embodied) Turing test] requires:
        1. Natural language processing to communicate effectively with humans.
        2. Knowledge representation to store and organize information in a
          usable format.
        3. Automated reasoning to utilize stored knowledge for answering
          questions and making inferences.
        4. Machine learning to identify and detect patterns within data.
        5. Computer vision and speech recognition to accurately perceive and
          understand spoken language.
        6. Robotics to manipulate physical objects and navigate environments.
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
    - #strong[Pros]:
      - An operational definition of intelligence provides a clear and
        measurable framework for evaluating intelligent behavior in both humans
        and machines.
      - This definition sidesteps philosophical vagueness by focusing on
        observable actions rather than abstract concepts, such as consciousness
        or the capability of a machine to think.
  ],
  [
    - #strong[Cons]:
      - Intelligence is often defined by #emph[anthropomorphic] criteria, which
        means it is evaluated based on human-like characteristics. However, it
        is important to recognize that multiple forms of non-human intelligence
        exist, each with its own attributes and capabilities.
      - Achieving a passing score in intelligence assessments often involves
        #strong[fooling humans] into believing that the entity being evaluated
        is human. This highlights the complexities involved in defining and
        assessing intelligence, as human-like behavior does not encompass the
        full spectrum of intelligent actions that may be exhibited by non-human
        entities.
  ],
)

// From: msml610/lectures_source/Lesson01.2-AI_and_Machine_Learning.smd:248 '* 4. AI as Acting Rationally'
// Slide: 4. AI as Acting Rationally
#strong[4. AI as Acting Rationally]

- #strong[Definition]: #strong[Rational agents] are agents that do the
  #emph["right thing"] given what they know.

- #strong[Characteristics]: Agents that #strong[act rationally] should
  1. Operate autonomously.
  2. Perceive their environment.
  3. Persist over time.
  4. Adapt to change.
  5. Create and pursue goals.

// From: msml610/lectures_source/Lesson01.2-AI_and_Machine_Learning.smd:260 '* Acting Rationally as Ultimate Goal of AI'
// Slide: Acting Rationally as Ultimate Goal of AI
#strong[Acting Rationally as Ultimate Goal of AI]

#grid(
  columns: (65%, 30%),
  gutter: 1em,
  [
    - #strong[Question]: Which definition of AI best captures what we should
      build?
      - #strong[Acting vs. Thinking]
      - #strong[Rational vs. Human]

    - #strong[Acting is more fundamental than Thinking]: Acting rationally
      encompasses a broader range of actions than merely thinking rationally.
      While thinking involves the cognitive processes and reasoning capabilities
      of an agent, acting pertains to the execution of those thoughts in the
      real world. Therefore, a more comprehensive understanding of artificial
      intelligence includes the ability to act effectively and appropriately in
      various situations, not just to think or process information.

    - #strong[Rational is more objective than Human]: Rationality can be
      mathematically defined and assessed through formal models, making it a
      more objective standard than human behavior. While human actions are
      influenced by a host of factors, including emotions, social contexts, and
      evolutionary pressures, rational actions are based on principles and
      logical structures that can be evaluated quantitatively. This distinction
      is crucial in designing AI systems that aim to replicate decision-making
      in a consistent and predictable manner, transcending the complexities of
      human behavior.

    - #strong[Key idea]: AI should focus on #strong[agents acting rationally].
      This means that when developing artificial intelligence systems, priority
      should be given to their ability to make decisions and perform tasks based
      on a framework of rationality, thereby ensuring optimal performance in
      various contexts.
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

- #strong[Problem]: AI aims to build agents that #strong[do the right thing],
  but what is the #emph[right thing]?

- #strong[Example]: Consider the scenario where you leave the house and a branch
  unexpectedly strikes you.
  - _"Did you act rationally?"_
  - The answer is probably yes, as you could not have anticipated this event.

- #strong[Example]: In another situation, you might cross the street without
  checking for oncoming traffic, resulting in being struck by a car.
  - _"Did you act rationally?"_
  - Here, the answer depends on the circumstances; it is probably not rational
    since checking for traffic is a low-cost precaution that could prevent harm.

- #strong[Challenges]: This raises important moral issues, particularly in the
  case of self-driving cars.
  - _"Should a car swerve and hit a pedestrian to avoid a frontal crash that
    would kill two people?"_
  - Such dilemmas highlight the complexities involved in designing AI systems
    that make ethical decisions in life-threatening situations.

// From: msml610/lectures_source/Lesson01.2-AI_and_Machine_Learning.smd:313 '* Problems of a Rational Agent'
// Slide: Problems of a Rational Agent
#strong[Problems of a Rational Agent]

- #strong[Challenges]: In a **probabilistic environment**, a rational agent’s
  goal shifts from merely achieving the best outcome in deterministic setups to
  striving for the best expected outcome under conditions of uncertainty. This
  dual focus is essential as real-world scenarios often involve inherent
  unpredictability, requiring agents to consider probabilities and potential
  variations in outcomes.

- #strong[Problem]: The definition of **"best"** is crucial in decision-making
  frameworks. Traditionally, "best" is determined by an objective function,
  which quantifies the desirability of outcomes in a way that can guide choices.
  This could manifest in various forms, such as a cost function that assesses
  the financial implications of different decisions, a sum of rewards that
  reflects the cumulative benefits of choices, a loss function that quantifies
  the penalties for errors, or utility functions that measure satisfaction or
  preference. However, the determination of what constitutes the best outcome is
  often more complex than these classical models suggest.

- #strong[Limitations]: A critical limitation arises in the dichotomy between
  **omniscience and no-regrets**. The notion of the "best" outcome relies
  heavily on the information available to the agent; it does not necessitate
  perfect knowledge about the environment. In many scenarios, particularly in
  dynamic fields like medicine, there may not exist a **provably correct
  action**, necessitating the agent to make decisions based on partial
  information. Moreover, even when an agent theoretically possesses perfect
  information, achieving rationality can still be implausible due to several
  constraints:
  - The **cost of acquiring comprehensive data** can be prohibitive. For
    instance, in medical settings, gathering exhaustive details for accurate
    diagnosis can be financially and logistically unfeasible.
  - The **computational demands** of analyzing vast datasets or traversing
    complex decision trees can exceed practical limits, especially considering
    scenarios with branching paths that may surpass the number of atoms in the
    observable universe, estimated to be around $\sim 10^{80}$.
  - **Real-time demands** further complicate rational decision-making, as in
    high-frequency trading (HFT), where decisions must be made in fractions of a
    microsecond to capitalize on fleeting opportunities.

- #strong[Solution]: A pragmatic approach to these challenges is embodied in the
  concept of **"satisficing,"** where the focus shifts towards achieving
  outcomes that are _good enough_ rather than striving for perfection. This
  strategy involves making decisions that are feasible and appropriate given the
  constraints faced, allowing rational agents to function effectively in complex
  and uncertain environments #cite("simon1956satisficing").

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
    - #strong[Question]: How should we define machine learning?

    - #strong[Definition]:
      - "Machine learning is the field of study that gives computers the ability
        to learn without being explicitly programmed" (Samuel, 1959) #cite(
          "samuel1959checkers",
        ). This highlights the fundamental concept of machine learning: the
        capacity for machines to improve their performance on tasks by learning
        from data rather than relying on predetermined instructions.

      - In practice, machine learning consists of creating systems that perform
        useful tasks autonomously. For instance, a computer can learn to master
        the game of checkers by playing against itself, analyzing the outcomes
        of various moves, and memorizing positions that lead to victories. This
        capability exemplifies the potential of machine learning to develop
        strategies and make decisions based on experience.

      - More formally, we can define machine learning through a precise
        framework: "A computer program is said to learn from experience $E$ with
        respect to some task $T$ and some performance measure $P$, if $P(T)$
        improves with experience $E$" (Mitchell, 1997) #cite(
          "mitchell1997machinelearning",
        ). This definition emphasizes the relationship between the data
        encountered, the task being performed, and the associated performance
        metric that determines success.

    - #strong[Applications]: Common ML examples include:
      - Computer vision
      - Speech recognition
      - Natural language processing

    These applications illustrate the versatility and widespread impact of
    machine learning technologies across various domains, showcasing their
    ability to interpret visual information, understand spoken language, and
    process written text.
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

- #strong[Fact]: Machine learning (ML) addresses a practical problem by
  following a series of phases:
  - Gathering a dataset is the first crucial step, as it forms the foundation
    for any ML task.
  - Building a statistical model from the dataset algorithmically involves
    applying various algorithms to learn patterns from the collected data, which
    encapsulates the essence of machine learning.
  - Once the model is developed, evaluating the model is necessary to assess its
    performance and reliability in making predictions based on unseen data.
  - Lastly, deploying and monitoring the model in a real-world application
    ensures that it functions effectively and can be updated or retrained as new
    data becomes available.

- #strong[Problem] (Abu-Mostafa, 2012) #cite("abumostafa2012learning"):
  - While many of the aforementioned phases are primarily "engineering" tasks,
    the phase of building the model stands out as the "research" component. This
    is where theoretical innovation and exploration take place.
  - The **three core assumptions** of machine learning are critical for the
    success of ML implementations:
    1. A _pattern exists_ in the data, which the model will learn to recognize
      and utilize.
    2. The pattern cannot be _precisely defined mathematically_, indicating that
      the complexity of real-world data often precludes a simple mathematical
      description.
    3. _Data is available_ to train the model, as without data, there would be
      nothing for the model to learn from.

- #strong[Question]: Which assumption is **essential**?
  1. If no pattern exists, does it make sense to run learning? This question
    challenges the foundation of the ML process; without a pattern to find,
    running a learning algorithm would yield no meaningful results.
  2. Is it a problem if mathematics can devise the pattern but we still use
    machine learning? This highlights the difference between theoretical
    mathematical solutions and practical ML applications, and whether relying on
    ML is justified even when a mathematical description exists.
  3. Can progress happen without data? This question emphasizes the pivotal role
    of data in any machine learning endeavor.

- #strong[Remark]: _Without data, no progress is possible_: The availability of
  data is the truly essential assumption for machine learning, as it enables the
  model to learn, adapt, and ultimately provide valuable predictions and
  insights.

// From: msml610/lectures_source/Lesson01.2-AI_and_Machine_Learning.smd:399 '* AI vs ML vs Deep Learning'
// Slide: AI vs ML vs Deep Learning
#strong[AI vs ML vs Deep Learning]

#grid(
  columns: (65%, 30%),
  gutter: 1em,
  [
    - #strong[Definition]:
      - #strong[AI (Artificial Intelligence)]: Machines programmed to reason,
        learn, and act in a rational way.
      - #strong[ML (Machine Learning)]: Machines capable of performing tasks
        without being explicitly programmed.
      - #emph[AI models that are not ML] are possible:
        - For example, handcrafted rule-based systems, such as IBM Deep Blue
          playing chess, do not learn from data but are still considered AI
          systems.

    - #strong[Definition]:
      - #strong[DL (Deep Learning)]: A form of ML that utilizes a particular
        type of model, specifically neural networks with many layers.
      - #strong[LLM (Large Language Models)]: Neural networks trained on massive
        text datasets to predict text, often further refined through
        reinforcement learning from human feedback (RLHF) #cite(
          "ouyang2022instructgpt",
        ).
      - #emph[DL models that are not LLMs] are possible:
        - For instance, a convolutional neural network designed for vision or
          speech is a deep learning system but does not qualify as an LLM.
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
  image("Lesson01.2-AI_and_Machine_Learning.typ.figs/Lesson01.2-AI_and_Machine_Learning.2.png"),
)
// render_images:end
  ],
)

// From: msml610/lectures_source/Lesson01.2-AI_and_Machine_Learning.smd:457 '* Limits of AI Compared to Human Intelligence (1/2)'
// Slide: Limits of AI Compared to Human Intelligence (1/2)
#strong[Limits of AI Compared to Human Intelligence (1/2)]

- #strong[Problem]: AI and ML differ from human intelligence.
  - Machines learn in fundamentally different ways compared to humans. For
    instance, large language models (LLMs) follow specific algorithms to process
    and generate language, which may not reflect the nuanced, adaptive nature of
    human learning. This difference brings about distinct limitations inherent
    in machine learning systems.
  - The question of whether the human brain employs gradient descent, a common
    optimization technique used in training machine learning models, remains
    unclear. This reflects a broader uncertainty in the parallels drawn between
    human cognitive processes and computational methods.
  - Similarly, there is speculation about whether human learning can be likened
    to reinforcement learning, which is a paradigm where agents learn by
    interacting with their environment and receiving feedback. While some
    aspects of human learning exhibit these characteristics, it is complicated
    and not entirely accurate to equate the two.

- #strong[Limitations]:
  - #strong[Fragility to input variations]: Machine learning models are
    particularly sensitive to variations in input. They may fail dramatically
    when presented with even slight distortions in data. For example,
    adversarial attacks can lead to misclassification of images by merely
    altering a single pixel in the input data, as demonstrated in studies on
    vulnerability to such attacks #cite("su2019onepixel"). In a practical
    scenario, a machine learning model trained to recognize objects within a
    video game might become ineffective if the display is rotated slightly,
    whereas humans can adjust and perform consistently well regardless of such
    variations.
  - #strong[Lack of transfer learning]: One of the significant limitations of
    current machine learning systems is their inability to apply knowledge
    learned in one domain to another without extensive retraining. Unlike
    humans, who can leverage learned skills across various contexts, ML models
    typically require fresh datasets to retrain for new tasks.
  - #strong[Massive data and compute requirements]: Machine learning
    necessitates vast amounts of data and considerable computational resources.
    For instance, while a teenager may learn to drive a car in just a few hours,
    self-driving vehicles require billions of hours of computational processing
    and extensive datasets to train effectively, highlighting the disparity in
    learning efficiency between humans and machines.
  - #strong[Poor common sense and reasoning]: Despite advancements in ML, these
    systems still exhibit a lack of built-in world knowledge and intuitive
    logic. This deficiency limits their ability to reason or infer conclusions
    in the same way humans might, highlighting a fundamental gap between human
    cognition and machine processing.

// From: msml610/lectures_source/Lesson01.2-AI_and_Machine_Learning.smd:480 '* Limits of AI Compared to Human Intelligence (2/2)'
// Slide: Limits of AI Compared to Human Intelligence (2/2)
#strong[Limits of AI Compared to Human Intelligence (2/2)]

- #strong[Limitations]:
  - #strong[Opaque decision-making]: Many machine learning (ML) models offer
    little transparency into their decision-making processes. This lack of
    transparency can significantly limit trust, interpretability, and
    accountability, especially in critical applications such as healthcare,
    finance, and autonomous systems.

  - #strong[Dependence on narrow objectives]: While ML systems excel at
    optimizing specific, narrow tasks, they often struggle with ambiguous or
    broader goals. For example, an algorithm designed to maximize user
    engagement might inadvertently promote harmful content, showcasing the
    pitfalls of focusing strictly on quantitative metrics at the expense of
    qualitative considerations.

  - #strong[Susceptibility to bias and data quality]: Models are highly
    susceptible to the biases present in their training data. They can inherit
    and even amplify these biases, leading to skewed outcomes that reflect and
    perpetuate existing social inequalities or stereotypes.

  - #strong[Lack of embodiment and physical interaction]: Human cognition and
    decision-making are deeply grounded in physical and sensory experiences. ML
    systems, which typically lack such embodiment, may struggle to replicate the
    nuanced understanding of context that arises from human interactions with
    the physical world.

// From: msml610/lectures_source/Lesson01.2-AI_and_Machine_Learning.smd:494 '* Key Takeaways'
// Slide: Key Takeaways
#strong[Key Takeaways]

- #strong[Key idea]: AI should focus on #strong[agents acting rationally],
  rather than on mimicking human thought or behavior. This principle underscores
  the significance of developing AI systems that operate based on rational
  decision-making processes, which can be distinct from how humans think or
  behave.

- #strong[Definition]:
  - #strong[AI]: Machines programmed to reason, learn, and act rationally. This
    encapsulates the core essence of artificial intelligence, emphasizing the
    capability of machines to not only perform tasks but to engage in reasoning
    and learning processes that enable them to make informed decisions.
  - #strong[ML]: A subset of AI that performs tasks without being explicitly
    programmed. This highlights the automatic nature of machine learning, where
    algorithms improve their performance through experience rather than through
    direct human intervention.
  - #strong[DL]: A subset of ML that uses multi-layer neural networks. Deep
    learning leverages complex architectures of interconnected nodes (neurons)
    to capture and represent intricate patterns in data, thereby facilitating
    advanced learning capabilities.
  - #strong[LLM]: A subset of DL trained on massive text datasets to predict
    text, often further tuned with #strong[RLHF] (Reinforcement Learning from
    Human Feedback). This specifies that large language models use extensive
    textual data to enhance their prediction skills, which are typically refined
    by incorporating human feedback for improved relevance and coherence.

- #strong[Remark]: Current ML/DL systems, despite their power, still fall short
  of human intelligence in areas such as fragility, transfer learning, data
  efficiency, and common-sense reasoning. This observation points to critical
  limitations in existing machine learning and deep learning approaches, where
  the resilience and adaptability of human cognition often exceed what current
  AI technologies can accomplish.

// From: msml610/lectures_source/Lesson01.2-AI_and_Machine_Learning.smd:510 '* References'
// Slide: References
#strong[References]

#set text(size: 0.75em)
#references("/msml610/lectures_source/refs.bib")
