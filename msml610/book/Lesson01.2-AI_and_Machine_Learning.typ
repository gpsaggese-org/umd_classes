// git_hash=d5a505bbb-mu1 timestamp=20260829_233752
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

- #strong[Definition]: #strong[Machine Learning] is a subset of Artificial
  Intelligence (AI). It is often confused with #emph[deep learning],
  #emph[large-language models], #emph[predictive analytics], and other related
  fields.

- #strong[Question]: What is artificial intelligence? To answer this, we must
  first understand what #strong[human intelligence] is.

- #strong[Question]: What is human intelligence? We call ourselves #emph["homo
    sapiens"] because intelligence sets us apart from animals. For thousands of
  years, humans have tried to understand how we think. This remains one of the
  #emph[biggest mysteries]: the brain, though small in size, can grasp nature's
  secrets, such as the theory of relativity, quantum mechanics, and black holes.
  How can the brain understand, predict, and manipulate a world more complex
  than itself?

// From: msml610/lectures_source/Lesson01.2-AI_and_Machine_Learning.smd:33 '* Artificial Intelligence'
// Slide: Artificial Intelligence
#strong[Artificial Intelligence]

#grid(
  columns: (80%, 20%),
  gutter: 1em,
  [
    - #strong[Definition]: The term #emph["Artificial Intelligence"] was coined
      in 1956 #cite("mccarthy1955dartmouth").

    - #strong[Goal]:
      - Understand human intelligence.
      - Create intelligent entities. As Feynman famously stated, #emph["What I
          cannot create, I do not understand"] (1988).

    - #strong[Characteristics]:
      - Artificial Intelligence applies to any human activity and task.
      - Its impact exceeds any past historical event.
      - It generates hundreds of billions of dollars annually in market revenue,
        with trillions in global economic impact projected by 2030 #cite(
          "bughin2018aifrontier",
        ).
      - Unlike disciplines with settled core theories, such as arithmetic or
        Newtonian mechanics within its domain, AI has many unresolved problems.
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
      - Thinking vs. Acting
      - Human vs. Rational (ideal performance)

    - #strong[Four resulting definitions]: AI can be defined as a machine that
      can:
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

- #strong[Problem]: To build machines that think like humans, it is essential to
  first #strong[determine how humans think]. This involves understanding the
  cognitive processes and mechanisms that underlie human thought and translating
  them into computational models.

- #strong[Pros]:
  - This approach allows us to express a precise theory of the human mind as a
    computer program. By modeling human cognition computationally, we can gain
    insights into the processes that drive human thought and behavior.

- #strong[Cons]:
  - One major challenge is the unknown workings of the human mind. Despite
    advances in cognitive science and neuroscience, many aspects of human
    cognition remain mysterious and difficult to replicate in machines.
  - Additionally, this approach relies on an anthropocentric definition of
    intelligence, which may limit our understanding of non-human forms of
    intelligence and the potential for machines to develop unique cognitive
    abilities.

// From: msml610/lectures_source/Lesson01.2-AI_and_Machine_Learning.smd:113 '* 2. AI as Thinking Rationally'
// Slide: 2. AI as Thinking Rationally
#strong[2. AI as Thinking Rationally]

#grid(
  columns: (65%, 30%),
  gutter: 1em,
  [
    - #strong[Question]: What are the rules of #strong[correct thinking]?
      - When provided with correct premises, the process should lead to correct
        conclusions.

    - #strong[Techniques]: #strong[Logic] is the study of the "laws of thought."
      - It involves formalizing statements about objects and their
        relationships.

    - #strong[Techniques]: #strong[Automatic theorem proving]
      - These are programs designed to solve problems expressed in logical
        notation.
      - They may run indefinitely if no solution exists, as first-order validity
        is only semi-decidable.
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
  1. #strong[Formalizing informal knowledge is difficult]: Consider the example
    of a handshake. It can be described informally as "a handshake occurs when
    two people extend, grip, shake hands, then release." However, formalizing
    this interaction requires a complex logical representation:
    $$
    \begin{aligned} & \exists \; x, y, h_x, h_y \\ & \quad Person(x) \land
    Person(y) \land x \neq y \land {} Hand(x, h_x) \land Hand(y, h_y) \land {}
    \\ & \quad MoveToward(h_x, h_y) \land Contact(h_x, h_y) \land {} Shake(h_x,
    h_y) \land {} \\ &\quad Release(h_x, h_y) \\ \end{aligned}
    $$
  2. #strong[Probabilistic nature of knowledge]: In fields like medicine,
    symptoms such as fever, cough, and fatigue could indicate flu, COVID-19, or
    another illness. This uncertainty highlights the probabilistic nature of
    knowledge.
  3. #strong[Scalability challenges]: Addressing large problems often requires
    heuristics to find practical solutions, as exhaustive methods may be
    computationally infeasible.
  4. #strong[Intelligence requires more than rational thinking]: An intelligent
    agent must interact with the world, which introduces the problem of the
    "embodiment of AI." This means that intelligence encompasses more than just
    rational thought; it involves engaging with the environment.

// From: msml610/lectures_source/Lesson01.2-AI_and_Machine_Learning.smd:193 '* 3. AI as Acting Humanly'
// Slide: 3. AI as Acting Humanly
#strong[3. AI as Acting Humanly]

#grid(
  columns: (75%, 25%),
  gutter: 1em,
  [
    - #strong[Components]: Passing the #strong[(embodied) Turing test] requires
      several key components:
      1. #strong[Natural language processing] to enable effective communication.
      2. #strong[Knowledge representation] to store and organize information
        efficiently.
      3. #strong[Automated reasoning] to utilize stored knowledge and provide
        answers to questions.
      4. #strong[Machine learning] to identify and learn from patterns in data.
      5. #strong[Computer vision and speech recognition] to perceive and
        comprehend visual and auditory information.
      6. #strong[Robotics] to physically interact with and manipulate objects in
        the environment.
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
      - Provides an operational definition of intelligence, which is practical
        and actionable.
      - Sidesteps philosophical vagueness by avoiding questions such as "What is
        consciousness?" or "Can a machine think?" This allows for a more focused
        and empirical approach to understanding intelligence.
  ],
  [
    - #strong[Cons]:
      - Intelligence is often defined by #strong[anthropomorphic] criteria,
        meaning it is evaluated in human terms. This perspective overlooks the
        existence of multiple forms of non-human intelligence, which may not
        align with human characteristics or behaviors.
      - Passing a test of intelligence often involves #strong[fooling humans]
        into believing that an entity is human. This criterion emphasizes the
        ability to mimic human-like responses rather than demonstrating genuine
        understanding or intelligence.
  ],
)

// From: msml610/lectures_source/Lesson01.2-AI_and_Machine_Learning.smd:248 '* 4. AI as Acting Rationally'
// Slide: 4. AI as Acting Rationally
#strong[4. AI as Acting Rationally]

- #strong[Definition]: #strong[Rational agents] are agents that do the
  #emph["right thing"] given what they know.

- #strong[Characteristics]: Agents that #strong[act rationally] should:
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
      - Acting vs. Thinking
      - Rational vs. Human

    - #strong[Acting is more fundamental than Thinking]: Acting rationally is
      broader than thinking rationally.

    - #strong[Rational is more objective than Human]:
      - Rationality can be mathematically defined.
      - Human behavior is shaped by evolutionary conditions.

    - #strong[Key idea]: AI should focus on #strong[agents acting rationally].
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
  but what exactly is the #emph[right thing]?

- #strong[Example]: Imagine you leave the house and a branch strikes you. The
  question arises, #emph["Did you act rationally?"] The answer is probably yes,
  as the event was unforeseen and unavoidable.

- #strong[Example]: Consider crossing the street without checking for oncoming
  traffic, resulting in being hit by a car. Here, the question is again,
  #emph["Did you act rationally?"] The answer is less clear and likely no, since
  taking a moment to check for traffic was a low-cost action that could have
  prevented harm.

- #strong[Challenges]: There are moral issues associated with self-driving cars.
  For instance, #emph["Should a car swerve and hit a pedestrian to avoid a
    frontal crash that would kill two people?"] This scenario raises complex
  ethical questions about decision-making in AI systems.

// From: msml610/lectures_source/Lesson01.2-AI_and_Machine_Learning.smd:313 '* Problems of a Rational Agent'
// Slide: Problems of a Rational Agent
#strong[Problems of a Rational Agent]

- #strong[Challenges]: #strong[Probabilistic environment]
  - A rational agent aims for:
    - The best outcome in a deterministic setup.
    - The best expected outcome under uncertainty.

- #strong[Problem]: What does #strong["best"] mean?
  - The classical answer is that #emph["best"] is determined by the
    #emph[objective function], such as a cost function, sum of rewards, loss
    function, or utility.
  - However, the situation is often more complex.

- #strong[Limitations]:
  - #strong[Omniscience vs no-regrets]: The best decision is based on available
    information, not perfect knowledge.
  - Sometimes, there is #strong[no provably correct action] available, yet an
    action must still be taken.
  - Even #strong[with perfect information], rationality may not be feasible due
    to:
    - The cost of acquiring all data, as seen in fields like medicine.
    - Computational demands, such as traversing a search tree with more branches
      than atoms in the observable universe, approximately $10^{80}$.
    - Real-time demands, for example, making a decision within 1 microsecond in
      high-frequency trading (HFT).

- #strong[Solution]: #strong["Satisficing"]: Achieve a #emph[good enough]
  outcome instead of a #emph[perfect] one #cite("simon1956satisficing").
  - This involves acting appropriately given the constraints.

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

    - #strong[Definition]:
      - #emph["Machine learning is the field of study that gives computers the
          ability to learn without being explicitly programmed"] (Samuel, 1959)
        #cite("samuel1959checkers").
      - Machine learning involves building machines that can perform
        #emph[useful things] without being #emph[explicitly programmed]. For
        example, a computer can learn to play checkers by playing against itself
        and memorizing winning positions.
      - More formally, #emph["A computer program is said to learn from
          experience $E$ with respect to some task $T$ and some performance
          measure $P$, if $P(T)$ improves with experience $E$"] (Mitchell, 1997)
        #cite("mitchell1997machinelearning").

    - #strong[Applications]: Common examples of machine learning include:
      - Computer vision
      - Speech recognition
      - Natural language processing
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

- #strong[Fact]: Machine learning addresses a practical problem through a series
  of steps:
  - Gathering a dataset.
  - #emph[Building a statistical model from the dataset algorithmically].
  - Evaluating the model.
  - Deploying and monitoring the model.

- #strong[Problem] (Abu-Mostafa, 2012) #cite("abumostafa2012learning"):
  - While most phases of machine learning are considered "engineering",
    #emph[building the model] is regarded as the "research" component.
  - The #strong[three core assumptions] of machine learning are:
    1. A #emph[pattern exists].
    2. The pattern cannot be #emph[precisely defined mathematically].
    3. #emph[Data is available].

- #strong[Question]: Which assumption is #strong[essential]?
  1. If no pattern exists, does it make sense to run learning?
  2. Is it a problem if math can devise the pattern but we still use machine
    learning?
  3. Can progress happen without data?

- #strong[Remark]: #emph[Without data, no progress is possible]: data
  availability is the assumption that is truly essential.

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
      - #emph[AI models that are not ML] is possible. For example, handcrafted
        rule-based systems, such as IBM Deep Blue playing chess, do not learn
        from data but are still considered AI systems.

    - #strong[Definition]:
      - #strong[DL (Deep Learning)]: A subset of ML that uses a particular type
        of models, specifically neural networks with many layers.
      - #strong[LLM (Large Language Models)]: Neural networks trained on massive
        #emph[text] datasets to predict text, often further tuned with
        reinforcement learning from human feedback (RLHF) #cite(
          "ouyang2022instructgpt",
        ).
      - #emph[DL models that are not LLMs] are possible. For instance, a
        convolutional neural network for vision or speech is a deep learning
        system but not an LLM.
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

- #strong[Problem]: #strong[AI and ML differ from human intelligence]
  - Machines do not learn in the same way humans do. For example, large language
    models (LLMs) have distinct limitations compared to human learning
    processes.
  - It is unclear whether the human brain employs gradient descent as a learning
    mechanism.
  - The brain might use reinforcement learning, but this is likely only true in
    a certain sense.

- #strong[Limitations]:
  - #strong[Fragility to input variations]: Machine learning models often fail
    when faced with slight input distortions. For instance, adversarial attacks
    can cause misclassification by altering just one pixel #cite(
      "su2019onepixel",
    ). A model trained on a video game may fail if the screen rotates slightly,
    whereas humans can adapt effortlessly.
  - #strong[Lack of transfer learning]: Machine learning systems struggle to
    apply knowledge across different domains without undergoing retraining.
  - #strong[Massive data and compute requirements]: Machine learning requires
    enormous datasets and computational resources. For example, while a teenager
    can learn to drive in a matter of hours, self-driving systems demand
    billions of compute hours and extensive data.
  - #strong[Poor common sense and reasoning]: Machine learning lacks built-in
    world knowledge and intuitive logic.

// From: msml610/lectures_source/Lesson01.2-AI_and_Machine_Learning.smd:480 '* Limits of AI Compared to Human Intelligence (2/2)'
// Slide: Limits of AI Compared to Human Intelligence (2/2)
#strong[Limits of AI Compared to Human Intelligence (2/2)]

- #strong[Limitations]:
  - #strong[Opaque decision-making]: many machine learning models offer little
    transparency into their decision-making processes. This lack of transparency
    can limit trust, interpretability, and accountability, especially in
    critical applications where understanding the rationale behind decisions is
    essential.
  - #strong[Dependence on narrow objectives]: machine learning systems excel at
    optimizing for narrow, well-defined tasks but often struggle when faced with
    ambiguous or broader goals. For example, an algorithm designed to maximize
    user engagement might inadvertently promote harmful content, as it focuses
    solely on increasing interaction without considering the broader
    implications.
  - #strong[Susceptibility to bias and data quality]: models can inherit and
    even amplify biases present in their training data. This susceptibility can
    lead to skewed or unfair outcomes, particularly if the data used for
    training is not representative or is biased in some way.
  - #strong[Lack of embodiment and physical interaction]: human cognition is
    deeply grounded in physical and sensory experiences. Machine learning
    models, lacking this embodiment, may struggle to replicate the nuanced
    understanding that comes from interacting with the physical world.

// From: msml610/lectures_source/Lesson01.2-AI_and_Machine_Learning.smd:494 '* Key Takeaways'
// Slide: Key Takeaways
#strong[Key Takeaways]

- #strong[Key idea]: AI should focus on #strong[agents acting rationally],
  rather than on mimicking human thought or behavior.

- #strong[Definition]:
  - #strong[AI]: Machines programmed to reason, learn, and act rationally.
  - #strong[ML]: A subset of AI that performs tasks without being explicitly
    programmed.
  - #strong[DL]: A subset of ML using multi-layer neural networks.
  - #strong[LLM]: A subset of DL trained on massive text datasets to predict
    text, often further tuned with RLHF.

- #strong[Remark]: Current ML/DL systems, despite their power, still fall short
  of human intelligence in areas such as fragility, transfer learning, data
  efficiency, and common-sense reasoning.

// From: msml610/lectures_source/Lesson01.2-AI_and_Machine_Learning.smd:510 '* References'
// Slide: References
#strong[References]

#set text(size: 0.75em)
#references("/msml610/lectures_source/refs.bib")
