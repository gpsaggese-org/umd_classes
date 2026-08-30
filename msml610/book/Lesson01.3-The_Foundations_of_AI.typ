// git_hash=502eb3ce4-mjh timestamp=20260830_111947
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
  title: "L01.3: The Foundations of AI",
  author: "MSML610: Advanced Machine Learning",
)

// Apply the AIMA document template (page/text/heading set + show rules).
#show: aima-style

#chapter(01, "L01.3: The Foundations of AI")

// From: msml610/lectures_source/Lesson01.3-The_Foundations_of_AI.smd:10 '# The Foundations of AI'
// Slide: The Foundations of AI
#strong[The Foundations of AI]

// From: msml610/lectures_source/Lesson01.3-The_Foundations_of_AI.smd:12 '## Overview'
// Slide: Overview
== Overview

// From: msml610/lectures_source/Lesson01.3-The_Foundations_of_AI.smd:14 '* AI Relates to Many Other Disciplines'
// Slide: AI Relates to Many Other Disciplines
#strong[AI Relates to Many Other Disciplines]

// rendered_images:begin
// ```mermaid
// mindmap
//   root((AI))
//     Philosophy
//     Mathematics
//     Economics
//     Neuroscience
//     Psychology
//     Computer engineering
//     Control theory
//     Linguistics
// ```
// rendered_images:end
// render_images:begin
#figure(
  image("Lesson01.3-The_Foundations_of_AI.typ.figs/Lesson01.3-The_Foundations_of_AI.1.png"),
)
// render_images:end

// From: msml610/lectures_source/Lesson01.3-The_Foundations_of_AI.smd:29 '## Philosophy'
// Slide: Philosophy
== Philosophy

// From: msml610/lectures_source/Lesson01.3-The_Foundations_of_AI.smd:31 '* AI and Philosophy (1/2)'
// Slide: AI and Philosophy (1/2)
#strong[AI and Philosophy (1/2)]

- #strong[Question]: Can formal rules be used to draw valid conclusions?
  - #strong[Comparison]:
    - #emph[Reasoning]: Logic studies the rules of proper reasoning. In this
      context, Aristotle (384-322 BCE) was a pioneering figure who formulated
      basic laws governing the rational mind. His work laid the foundation for
      systematic thinking and contributed significantly to the development of
      logic as we know it today. Notably, the machines built in his era for
      arithmetic operations, such as the Pascaline in 1642, exemplify early
      attempts to create logical frameworks that could handle calculations
      mechanically.
    - #emph[Rationalism]: This school of thought asserts that reasoning is the
      primary path to understanding the world. Rationalists believe that through
      rational thought and inquiry, individuals can uncover truths about their
      environment and existence.

- #strong[Question]: How does the mind arise from a physical brain?
  - #strong[Comparison]:
    - #emph[Dualism]: This philosophical perspective posits that nature adheres
      to physical laws while suggesting that a part of the human mind—often
      referred to as "the soul"—is exempt from these constraints. Dualists argue
      that there exists a non-physical aspect of our being that interacts with
      the physical world but is not governed by its laws.
    - #emph[Materialism]: In contrast to dualism, materialism asserts that the
      mind is essentially a physical system, operating under the same laws of
      physics that govern all matter. This perspective raises important
      questions about the concept of free will, suggesting that the perception
      of available choices is merely an artifact of a complex physical system
      rather than an indication of autonomy.

// From: msml610/lectures_source/Lesson01.3-The_Foundations_of_AI.smd:50 '* AI and Philosophy (2/2)'
// Slide: AI and Philosophy (2/2)
#strong[AI and Philosophy (2/2)]

#grid(
  columns: (75%, 20%),
  gutter: 1em,
  [
    - #strong[Question]: What does knowledge come from?
      - #strong[Comparison]:
        - #emph[Empiricism]: knowledge acquired via the senses. For example, one
          learns that trees are green by observing them.
        - #emph[Induction]: involves forming general rules based on observed
          associations. For instance, if many swans are white, one might infer
          that all swans are white.
        - #emph[Logical Positivism]: posits that knowledge consists of logical
          theories that are connected to observations. An example is scientific
          hypotheses that correlate with experimental data.
  ],
  [
    #figure(
      image("../lectures_source/figures/L01.2.black_swans.jpg", width: 80%),
      caption: [black swans],
      kind: "figure",
      supplement: [Fig.],
      placement: auto,
    ) <fig:blackswans>
  ],
)

// From: msml610/lectures_source/Lesson01.3-The_Foundations_of_AI.smd:85 '## Mathematics and Computation'
// Slide: Mathematics and Computation
== Mathematics and Computation

// From: msml610/lectures_source/Lesson01.3-The_Foundations_of_AI.smd:87 '* AI and Mathematics'
// Slide: AI and Mathematics
#strong[AI and Mathematics]

- #strong[Question]: What are the formal rules to draw valid conclusions?
  - #strong[Comparison]:
    - #emph[Formal logic]: refers to logical deduction rules established by
      Boole in 1847. This framework enables us to derive conclusions from
      premises in a systematic way.
      - First-order logic is a key component of formal logic, encompassing
        objects and relations, a foundational concept introduced by Frege
        in 1879.
    - #emph[Limits to deduction]: It is essential to acknowledge that some
      statements are #emph["undecidable"]. The incompleteness theorem, proposed
      by Gödel in 1931, asserts that within any formal theory, there exist true
      statements that cannot be proved. This theorem highlights the intrinsic
      limitations of formal logical systems #cite("godel1931incompleteness").

- #strong[Question]: How do we reason with uncertain information?
  - #strong[Comparison]:
    - #emph[Probability]: This area represents the mathematics of uncertainty,
      with historical contributions from notable figures such as Cardano,
      Pascal, Bernoulli, and Bayes from the 1500s to the 1700s. Probability
      provides a framework for quantifying uncertainty and making predictions
      based on incomplete information.
    - #emph[Statistics]: Merging data with probability, statistics plays a
      critical role in extracting meaningful insights from data. It encompasses
      techniques such as experiment design, data analysis, hypothesis testing,
      and the study of asymptotic behaviors, all aimed at drawing rational
      conclusions in the presence of uncertainty.

#styled-table(
  headers: ("Field", "Key Contributors", "Era"),
  rows: (
    ("Formal Logic", "Boole, Frege, Godel", "1847 - 1931"),
    (
      "Probability & Statistics",
      "Cardano, Pascal, Bernoulli, Bayes",
      "1500s - 1700s",
    ),
  ),
  bold-first-col: true,
)

// From: msml610/lectures_source/Lesson01.3-The_Foundations_of_AI.smd:116 '* AI and Computer Science'
// Slide: AI and Computer Science
#strong[AI and Computer Science]

#grid(
  columns: (80%, 20%),
  gutter: 1em,
  [
    - #strong[Question]: What can be computed?

      - #strong[Comparison]:
        - #emph[Algorithm]: An algorithm is a finite set of well-defined
          instructions or procedures designed to solve specific problems. For
          example, the algorithm for computing the greatest common divisor (GCD)
          dates back to Euclid around 300 BCE, showcasing the longstanding
          interest in systematic methods for computation.

        - #emph[Limits to computation]: There are inherent limits to what can be
          computed; not all functions are computable. The concept of
          computability was formalized by Alan Turing in 1936 with the
          introduction of the Turing machine, a theoretical construct that can
          compute any function that is computable. This foundational work laid
          the groundwork for understanding the scope of algorithmic processes.
          One notable example of a non-computable problem is the halting
          problem, which asks whether a given program will terminate after a
          finite number of steps. This problem reveals significant limitations
          in algorithmic decision-making. #cite("turing1936computable")

        - #emph[Tractability]: Tractability refers to the feasibility of solving
          computational problems within a reasonable time frame. It is often
          assessed through complexity classes, which categorize problems based
          on the resources required to solve them. The distinction between
          polynomial and exponential complexity is crucial here; a problem is
          considered intractable if the time required to solve it grows
          exponentially with the size of the input. This leads to the classic
          question in computer science known as P vs NP, which treats the
          relationship between problems that can be solved quickly (in
          polynomial time) versus those whose solutions can be verified quickly.
  ],
  [
    #figure(
      image("../lectures_source/figures/L01.3.Alan_Turing.jpg", width: 80%),
      caption: [Alan Turing (1951)],
      kind: "figure",
      supplement: [Fig.],
      placement: auto,
    ) <fig:alanturing>
  ],
)

// From: msml610/lectures_source/Lesson01.3-The_Foundations_of_AI.smd:144 '## Economics'
// Slide: Economics
== Economics

// From: msml610/lectures_source/Lesson01.3-The_Foundations_of_AI.smd:146 '* AI and Economics (1/2)'
// Slide: AI and Economics (1/2)
#strong[AI and Economics (1/2)]

- #strong[Question]: How do we make decisions to maximize payoff given
  preferences?
  - #strong[Comparison]:
    - In the context of _economies_, agents are thought to maximize their
      economic well-being, often referred to as utility. This area of study
      focuses on understanding desires and preferences, seeking to quantify how
      different choices can lead to varying levels of satisfaction or utility.
    - _Decision theory_ addresses the process of making decisions under
      uncertainty, aiming for preferred outcomes. It combines elements of
      probability theory and utility theory to evaluate options that involve
      risk and uncertainty. Practical applications of decision theory can be
      found in various fields, such as investment choices and policy decisions,
      where the outcomes are ambiguous and the potential payoffs must be weighed
      against the risks.

- #strong[Question]: How do we make decisions when payoffs result from several
  actions?
  - #strong[Comparison]:
    - _Operations research_ focuses on making rational decisions by evaluating
      the payoffs associated with a sequence of actions. A significant
      contribution to this field is found in the work of Bellman (1957) #cite(
        "bellman1957dp",
      ), who introduced methodologies like Markov Decision Processes (MDPs) to
      model and solve problems in which outcomes depend on a series of
      interconnected actions.
    - _Satisficing_, on the other hand, refers to strategies that aim for
      satisfactory or acceptable solutions rather than optimal ones. This
      approach is often closer to human behavior, as people tend to prefer good
      enough choices over exhaustive searches for the best option. Notably, this
      concept was explored by Simon in 1956 #cite("simon1956satisficing"),
      illustrating how individuals often select options that meet basic
      criteria, such as choosing a restaurant that fulfills essential
      preferences without striving for perfection.

// rendered_images:begin
// ```graphviz
// digraph DecisionTheory {
//     bgcolor="transparent";
//     pad="0.15";
//     splines=spline;
//     nodesep=0.5;
//     ranksep=0.5;
//     rankdir=LR;
// 
//     node [shape=box,
//           style="rounded,filled",
//           penwidth=1.8,
//           fontname="Helvetica",
//           fontsize=12,
//           margin="0.22,0.14",
//           height=0.50];
// 
//     edge [color="#A3B1C0",
//           penwidth=1.3,
//           arrowhead=vee,
//           arrowsize=0.75,
//           fontname="Helvetica",
//           fontsize=10,
//           fontcolor="#7B8794"];
// 
//     Prob    [label="Probability\nTheory", fillcolor="#A6E7F4", color="#5FB0C4", fontcolor="#1F4E56"];
//     Utility [label="Utility\nTheory", fillcolor="#A6E7F4", color="#5FB0C4", fontcolor="#1F4E56"];
//     Dec     [label="Decision\nTheory", fillcolor="#A6C8F4", color="#5A85C4", fontcolor="#1F3E6B"];
// 
//     { rank=same; Prob; Utility; }
//     Prob -> Dec;
//     Utility -> Dec;
// }
// ```
// rendered_images:end
// render_images:begin
#figure(
  image("Lesson01.3-The_Foundations_of_AI.typ.figs/Lesson01.3-The_Foundations_of_AI.2.png"),
)
// render_images:end

// From: msml610/lectures_source/Lesson01.3-The_Foundations_of_AI.smd:203 '* AI and Economics (2/2)'
// Slide: AI and Economics (2/2)
#strong[AI and Economics (2/2)]

- #strong[Question]: How do multiple agents with different goals act?

  - #strong[Comparison]:
    - #emph[Large economies]: In large economies, many agents operate without
      significant mutual impact. The actions of individual agents are often too
      small to influence broader market dynamics, allowing them to ignore the
      actions of other agents entirely. For instance, in a national economy, a
      single individual's buying or selling decisions do not typically affect
      market prices or trends due to the sheer scale of the economy.

    - #emph[Small economies]: Conversely, small economies are characterized by
      the influence that one player's actions can have on another's utility. In
      such settings, the decisions made by individual agents are interconnected.
      For instance, in a local market, if one seller adjusts their pricing, it
      can directly affect competitors and alter consumer behavior, creating a
      ripple effect throughout the market.

    - #emph[Game theory]: The dynamics observed in small economies can be framed
      within the context of game theory, as they resemble a "game" where the
      strategies employed by agents depend on the actions of others. This
      concept was notably explored by von Neumann and Morgenstern in 1944 #cite(
        "vonneumann1944gametheory",
      ). In scenarios where agents act rationally, they may need to adopt
      randomized strategies to maintain a competitive edge.

      For example, in a game of rock-paper-scissors, players often resort to
      randomization. This approach helps prevent opponents from predicting their
      next move, enabling a more strategic engagement based on chance rather
      than straightforward reasoning.

#styled-table(
  headers: ("Aspect", "Large Economies", "Small Economies", "Game Theory"),
  rows: (
    (
      "Mutual impact",
      "None, agents ignored",
      "One agent affects others' utility",
      "Agents strategize against each other",
    ),
    (
      "Example",
      "National economy",
      "Local market pricing",
      "Rock-paper-scissors",
    ),
  ),
  bold-first-col: true,
)

// From: msml610/lectures_source/Lesson01.3-The_Foundations_of_AI.smd:230 '## Neuroscience and Psychology'
// Slide: Neuroscience and Psychology
== Neuroscience and Psychology

// From: msml610/lectures_source/Lesson01.3-The_Foundations_of_AI.smd:232 '* AI and Neuroscience'
// Slide: AI and Neuroscience
#strong[AI and Neuroscience]

#grid(
  columns: (65%, 35%),
  gutter: 1em,
  [
    - #strong[Definition]: The #strong[brain] processes information, with
      different parts handling specific cognitive functions. For instance,
      information processing primarily occurs in the cerebral cortex, which is
      responsible for various higher-order functions. An example of this can be
      seen in the impact of an injury to the frontal lobe, which may
      significantly impair decision-making abilities.

    - #strong[Components]: The anatomy of the brain reveals a highly complex
      structure composed of approximately 100 billion neurons. Each neuron forms
      connections with about 10,000 to 100,000 other neurons through synapses,
      allowing for intricate communication pathways. Additionally, axons play a
      crucial role in enabling long-range connections across different brain
      regions. Information signals propagate through the brain via
      electrochemical reactions, where neurotransmitters facilitate
      communication between neurons. Notably, short-term pathways formed during
      specific tasks can help develop long-term connections, which are essential
      for learning and memory retention.

    - #strong[Remark]: When it comes to #strong[memory], current understanding
      indicates there is no definitive theory explaining how individual memories
      are stored within the brain. Instead, the prevailing theory suggests that
      memories are reconstructed rather than retrieved verbatim, indicating a
      more complex and dynamic process underlying memory recall.
  ],
  [
    #figure(
      image("../lectures_source/figures/L01.2.brain.jpg", width: 80%),
      caption: [brain],
      kind: "figure",
      supplement: [Fig.],
      placement: auto,
    ) <fig:brain>
    #figure(
      image("../lectures_source/figures/L01.2.neuron.png", width: 80%),
      caption: [neuron],
      kind: "figure",
      supplement: [Fig.],
      placement: auto,
    ) <fig:neuron>
  ],
)

// From: msml610/lectures_source/Lesson01.3-The_Foundations_of_AI.smd:262 '* The Brain Causes the Mind'
// Slide: The Brain Causes the Mind
#strong[The Brain Causes the Mind]

- #strong[Remark]: Simple cells give rise to thought and consciousness.
  - It is truly amazing to observe how complex processes emerge from simple
    components. This phenomenon demonstrates how intricate behaviors and
    cognitive abilities can manifest from fundamental building blocks, inviting
    further exploration into the nature of consciousness and intelligence.

- #strong[Remark]: Supercomputers can exceed the brain in raw computational
  throughput; however, they still lack its flexibility, learning speed, and
  energy efficiency.
  - This comparison highlights the limitations of current artificial systems
    despite their superior processing capabilities. While supercomputers excel
    in performing calculations at unprecedented speeds, they do not yet possess
    the adaptability and efficiency intrinsic to biological brains.

- #strong[Example]: Brain-machine interfaces serve as a compelling illustration
  of this interaction.
  - In these systems, the brain adjusts to the devices, showcasing the
    remarkable plasticity of neural function. For instance, individuals can
    learn to operate prosthetic limbs as if they were their own, demonstrating
    the potential of technology to enhance human capabilities and restore
    functionality.

- #strong[Definition]: The #strong[AI singularity] is defined as the future
  point in time when AI surpasses human intelligence.
  - This event marks a threshold beyond which AI is expected to improve
    autonomously, resulting in rapid growth of its capabilities. Recursive
    self-improvement could lead to the emergence of superintelligence, a concept
    explored in depth by researchers such as #cite("good1965ultraintelligent").
  - The potential societal implications of reaching the singularity include
    addressing the control problem and value alignment, which involve ensuring
    that AI systems align with human values. Furthermore, it raises concerns
    about the economic and social disruptions stemming from automation and the
    achievement of intelligence comparable to that of the human brain, the
    timeline for which remains uncertain.

// rendered_images:begin
// ```graphviz
// digraph Singularity {
//     bgcolor="transparent";
//     pad="0.15";
//     splines=spline;
//     nodesep=0.4;
//     ranksep=0.5;
//     rankdir=LR;
// 
//     node [shape=box,
//           style="rounded,filled",
//           penwidth=1.8,
//           fontname="Helvetica",
//           fontsize=12,
//           margin="0.22,0.14",
//           height=0.50];
// 
//     edge [color="#A3B1C0",
//           penwidth=1.3,
//           arrowhead=vee,
//           arrowsize=0.75,
//           fontname="Helvetica",
//           fontsize=10,
//           fontcolor="#7B8794"];
// 
//     AI      [label="AI\nSystem", fillcolor="#F4A6A6", color="#D46A6A", fontcolor="#6B1F1F"];
//     Improve [label="Improves\nItself", fillcolor="#A0D6D1", color="#4F9A8C", fontcolor="#1F4E45"];
//     Capable [label="Capability\nIncreases", fillcolor="#A6C8F4", color="#5A85C4", fontcolor="#1F3E6B"];
//     Super   [label="Super-\nintelligence", fillcolor="#C6A6F4", color="#8A5FCC", fontcolor="#3E1F6B"];
// 
//     AI -> Improve;
//     Improve -> Capable;
//     Capable -> AI [style=dashed, constraint=false, label="  recursive loop"];
//     Capable -> Super [label="  over time"];
// }
// ```
// rendered_images:end
// render_images:begin
#figure(
  image("Lesson01.3-The_Foundations_of_AI.typ.figs/Lesson01.3-The_Foundations_of_AI.3.png"),
)
// render_images:end

// From: msml610/lectures_source/Lesson01.3-The_Foundations_of_AI.smd:322 '* AI and Cognitive Psychology'
// Slide: AI and Cognitive Psychology
#strong[AI and Cognitive Psychology]

- #strong[Question]: How do humans think and act?
  - #strong[Comparison]:
    - #emph[Cognitive psychology]: proposes that the brain functions as an
      information-processing device. In this view, external stimuli are
      translated into internal representations, which are then manipulated by
      cognitive processes in order to generate new internal representations,
      often referred to as "beliefs." These beliefs ultimately guide behaviors,
      with representations being transformed into actions aligned with our
      goals.
    - #emph[Cognitive science]: employs computer models to explore facets of
      human cognition such as memory, language, and logical reasoning. This
      field borrows heavily from artificial intelligence (AI) by utilizing
      computational models to help explain how humans think, indicating that
      cognitive science is closely related to AI rather than being its
      antithesis.
    - #emph[Human-computer interaction]: focuses on how computers can enhance
      human capabilities. Rather than viewing AI purely as an artificial
      construct, this perspective acknowledges the spectrum from artificial
      intelligence to intelligence augmentation, illustrating the potential of
      technology to amplify human abilities rather than replace them.

// rendered_images:begin
// ```graphviz
// digraph CognitivePsychology {
//     bgcolor="transparent";
//     pad="0.15";
//     splines=spline;
//     nodesep=0.5;
//     ranksep=0.6;
//     rankdir=LR;
// 
//     node [shape=box,
//           style="rounded,filled",
//           penwidth=1.8,
//           fontname="Helvetica",
//           fontsize=12,
//           margin="0.22,0.14",
//           height=0.50];
// 
//     edge [color="#A3B1C0",
//           penwidth=1.3,
//           arrowhead=vee,
//           arrowsize=0.75,
//           fontname="Helvetica",
//           fontsize=10,
//           fontcolor="#7B8794"];
// 
//     Stimuli [label="Stimuli", fillcolor="#FFD1A6", color="#D9A85F", fontcolor="#6B4517"];
//     Repr    [label="Internal\nRepresentation", fillcolor="#A6E7F4", color="#5FB0C4", fontcolor="#1F4E56"];
//     Process [label="Cognitive\nProcesses", fillcolor="#A0D6D1", color="#4F9A8C", fontcolor="#1F4E45"];
//     Beliefs [label="Beliefs", fillcolor="#A6C8F4", color="#5A85C4", fontcolor="#1F3E6B"];
//     Actions [label="Actions\n(Goals)", fillcolor="#B2E2B2", color="#4F9A5C", fontcolor="#1F4E2E"];
// 
//     Stimuli -> Repr;
//     Repr -> Process;
//     Process -> Beliefs [label="  new representations"];
//     Beliefs -> Actions;
//     Beliefs -> Process [style=dashed, constraint=false, label="  update"];
// }
// ```
// rendered_images:end
// render_images:begin
#figure(
  image("Lesson01.3-The_Foundations_of_AI.typ.figs/Lesson01.3-The_Foundations_of_AI.4.png"),
)
// render_images:end

// From: msml610/lectures_source/Lesson01.3-The_Foundations_of_AI.smd:378 '## Engineering, Control, and Language'
// Slide: Engineering, Control, and Language
== Engineering, Control, and Language

// From: msml610/lectures_source/Lesson01.3-The_Foundations_of_AI.smd:380 '* AI and Computer Engineering (1/2)'
// Slide: AI and Computer Engineering (1/2)
#strong[AI and Computer Engineering (1/2)]

#grid(
  columns: (55%, 40%),
  gutter: 1em,
  [
    - #strong[Question]: How has computing hardware evolved to become fast
      enough for AI?

      - #strong[Definition]: #strong[electronic computers] were built during
        World War II. This period marked a significant advancement in computing
        technology, laying the groundwork for modern computing systems. These
        early computers utilized vacuum tubes and were primarily designed for
        military and scientific calculations, demonstrating the potential of
        automated computation in complex problem-solving scenarios.

      - #strong[Definition]: #strong[Moore's Law]: asserts that performance
        doubled every 18 months between 1970 and 2005 #cite(
          "moore1965cramming",
        ). This observation has been fundamental in guiding the semiconductor
        industry, driving relentlessly forward the development of faster and
        more efficient hardware. However, as we approached the physical limits
        of how small transistors can be made, power and scaling issues began to
        surface. Consequently, the focus has shifted toward multi-core
        processors rather than solely increasing clock speeds. Multi-core
        architectures enable computers to handle multiple tasks simultaneously,
        thereby enhancing performance and efficiency without solely relying on
        higher processing speeds.
  ],
  [
    #figure(
      image("../lectures_source/figures/L01.2.eniac.png", width: 80%),
      caption: [eniac],
      kind: "figure",
      supplement: [Fig.],
      placement: auto,
    ) <fig:eniac>
    #figure(
      image("../lectures_source/figures/L01.2.Moore_Law.png", width: 80%),
      caption: [Moore Law],
      kind: "figure",
      supplement: [Fig.],
      placement: auto,
    ) <fig:moorelaw>
  ],
)

// From: msml610/lectures_source/Lesson01.3-The_Foundations_of_AI.smd:402 '* AI and Computer Engineering (2/2)'
// Slide: AI and Computer Engineering (2/2)
#strong[AI and Computer Engineering (2/2)]

#grid(
  columns: (55%, 40%),
  gutter: 1em,
  [
    - #strong[Question]: What hardware trends are shaping AI systems today?

      - #strong[Definition]: #strong[Hardware for AI] refers to specialized
        hardware that enhances the efficiency and performance of artificial
        intelligence applications. This includes:
        - #strong[GPUs] (Graphics Processing Units), which are designed to
          handle the parallel task processing required for heavy computational
          workloads, making them ideal for training neural networks.
        - #strong[TPUs] (Tensor Processing Units), which are custom hardware
          designed by Google specifically for accelerating machine learning
          tasks.
        - #strong[Wafer-scale engines], which are large-scale systems designed
          to operate on a single silicon wafer, allowing for unprecedented
          levels of integration and performance.

      - #strong[Characteristics]: Current trends in AI hardware are defined by
        several key features:
        - There is a shift towards #strong[massive parallelism], which resembles
          the way brain functions operate, paralleling the architecture of
          neural networks that benefit from concurrent processing.
        - Notably, the compute capacity used in the largest AI training runs has
          doubled approximately every 3-4 months since 2012. This rapid growth
          outstrips the historical trend predicted by Moore's Law, as it is
          driven more by the incorporation of additional and improved chips,
          accompanied by increased financial investment, rather than solely by
          advancements in silicon technology.
        - Both GPUs and TPUs are instrumental in the field of deep learning,
          facilitating complex computations that are central to model training
          and inference.
        - It is also observed that #strong[high precision] computing (e.g.,
          using 64-bit floating-point numbers) is often unnecessary for many AI
          applications, suggesting that lower precision can be viable without
          sacrificing performance.

      - #strong[Definition]: #strong[Quantum computing] holds the promise of
        delivering significant acceleration for key computational tasks.
        - For instance, #strong[Shor's algorithm], which is known for its
          efficiency in factoring large integers, demonstrates how quantum
          computing can outperform classical approaches for specific problems
          #cite("shor1997factoring").
  ],
  [
    #figure(
      image("../lectures_source/figures/L01.2.CPU_GPU_TPU.png", width: 80%),
      caption: [CPU GPU TPU],
      kind: "figure",
      supplement: [Fig.],
      placement: auto,
    ) <fig:cpugputpu>
  ],
)

// From: msml610/lectures_source/Lesson01.3-The_Foundations_of_AI.smd:434 '* AI and Control Theory'
// Slide: AI and Control Theory
#strong[AI and Control Theory]

- #strong[Question]: How can artifacts operate under their own control?

  - #strong[Definition]: #strong[Control theory] studies self-regulating
    feedback control systems. These systems automatically adjust their
    operations to maintain desired outputs or states.

    - For example, a water regulator maintains a constant water flow by
      adjusting valves based on sensor inputs, illustrating the concept of
      feedback loops.

    - Control theory employs mechanisms that minimize the error between current
      states and goal states, ensuring that systems respond effectively to
      disturbances.

    - A prominent example in this field is the #strong[Kalman Filter],
      introduced by Kalman in 1960 #cite("kalman1960filtering"). This
      mathematical algorithm is fundamental in various applications, providing
      optimal estimates of system states from noisy measurements.

    - The filter operates based on concepts from calculus and matrix algebra,
      specifically focusing on stochastic optimal control, enabling it to
      predict future states and improve the accuracy of system outputs.

    - In artificial intelligence, similar principles apply through logical
      inference, symbolic planning, and computational methods, allowing AI
      systems to operate under their own control by continuously adapting to
      changes in their environment.

// rendered_images:begin
// ```graphviz
// digraph ControlLoop {
//     bgcolor="transparent";
//     pad="0.15";
//     splines=spline;
//     nodesep=0.5;
//     ranksep=0.5;
//     rankdir=LR;
// 
//     node [shape=box,
//           style="rounded,filled",
//           penwidth=1.8,
//           fontname="Helvetica",
//           fontsize=12,
//           margin="0.22,0.14",
//           height=0.50];
// 
//     edge [color="#A3B1C0",
//           penwidth=1.3,
//           arrowhead=vee,
//           arrowsize=0.75,
//           fontname="Helvetica",
//           fontsize=10,
//           fontcolor="#7B8794"];
// 
//     Goal       [label="Goal\nState", fillcolor="#FFD1A6", color="#D9A85F", fontcolor="#6B4517"];
//     Controller [label="Controller", fillcolor="#A0D6D1", color="#4F9A8C", fontcolor="#1F4E45"];
//     System     [label="System", fillcolor="#A6C8F4", color="#5A85C4", fontcolor="#1F3E6B"];
//     Output     [label="Current\nState", fillcolor="#B2E2B2", color="#4F9A5C", fontcolor="#1F4E2E"];
// 
//     Goal -> Controller [label="  error"];
//     Controller -> System;
//     System -> Output;
//     Output -> Controller [style=dashed, constraint=false, label="  feedback"];
// }
// ```
// rendered_images:end
// render_images:begin
#figure(
  image("Lesson01.3-The_Foundations_of_AI.typ.figs/Lesson01.3-The_Foundations_of_AI.5.png"),
)
// render_images:end

// From: msml610/lectures_source/Lesson01.3-The_Foundations_of_AI.smd:482 '* AI and Linguistics'
// Slide: AI and Linguistics
#strong[AI and Linguistics]

- #strong[Question]: How can you create systems that understand natural
  language?
  - #strong[Definition]: #strong[Computational linguistics] is the field that
    studies the structure and meaning of sentences. This area of study focuses
    on understanding how language works in order to develop algorithms and
    systems capable of processing natural language.
    - The applications of computational linguistics are vast and varied. For
      instance, machine translation systems, such as Google Translate, utilize
      these principles to convert text from one language to another while
      preserving meaning. Additionally, sentiment analysis tools apply
      computational linguistics techniques to assess attitudes expressed in
      social media posts. Automated customer support chatbots also leverage this
      field to interact with users intelligently, enabling more personalized and
      efficient service.

- #strong[Question]: How does language relate to thought?
  - #strong[Definition]: #strong[Knowledge representation] is a crucial concept
    in the study of artificial intelligence that explores how to effectively
    represent knowledge in a format that computers can use for reasoning.
    - This encompasses various methodologies, such as first-order logic, which
      provides a formal system for deriving truths based on a set of axioms, and
      knowledge graphs that visually represent relationships between different
      entities and concepts.

// rendered_images:begin
// ```graphviz
// digraph Linguistics {
//     bgcolor="transparent";
//     pad="0.15";
//     splines=spline;
//     nodesep=0.4;
//     ranksep=0.5;
//     rankdir=LR;
// 
//     node [shape=box,
//           style="rounded,filled",
//           penwidth=1.8,
//           fontname="Helvetica",
//           fontsize=12,
//           margin="0.22,0.14",
//           height=0.50];
// 
//     edge [color="#A3B1C0",
//           penwidth=1.3,
//           arrowhead=vee,
//           arrowsize=0.75,
//           fontname="Helvetica",
//           fontsize=10,
//           fontcolor="#7B8794"];
// 
//     NL     [label="Natural\nLanguage", fillcolor="#FFD1A6", color="#D9A85F", fontcolor="#6B4517"];
//     CL     [label="Computational\nLinguistics", fillcolor="#A0D6D1", color="#4F9A8C", fontcolor="#1F4E45"];
//     KR     [label="Knowledge\nRepresentation", fillcolor="#A0D6D1", color="#4F9A8C", fontcolor="#1F4E45"];
//     Trans  [label="Machine\nTranslation", fillcolor="#A6C8F4", color="#5A85C4", fontcolor="#1F3E6B"];
//     Sent   [label="Sentiment\nAnalysis", fillcolor="#A6C8F4", color="#5A85C4", fontcolor="#1F3E6B"];
//     Chat   [label="Chatbots", fillcolor="#A6C8F4", color="#5A85C4", fontcolor="#1F3E6B"];
//     Reason [label="Reasoning", fillcolor="#A6C8F4", color="#5A85C4", fontcolor="#1F3E6B"];
// 
//     NL -> CL;
//     NL -> KR;
//     CL -> Trans;
//     CL -> Sent;
//     CL -> Chat;
//     KR -> Reason;
// 
//     { rank=same; Trans; Sent; Chat; Reason; }
// }
// ```
// rendered_images:end
// render_images:begin
#figure(
  image("Lesson01.3-The_Foundations_of_AI.typ.figs/Lesson01.3-The_Foundations_of_AI.6.png"),
)
// render_images:end

// From: msml610/lectures_source/Lesson01.3-The_Foundations_of_AI.smd:540 '## Wrap-Up'
// Slide: Wrap-Up
== Wrap-Up

// From: msml610/lectures_source/Lesson01.3-The_Foundations_of_AI.smd:542 '* Key Takeaways'
// Slide: Key Takeaways
#strong[Key Takeaways]

- #strong[Key idea]: AI did not emerge from a single field; rather, it has
  inherited its core questions, formalisms, and tools from a diverse array of
  disciplines, including philosophy, mathematics, economics, neuroscience,
  psychology, computer science and engineering, control theory, and linguistics.

- #strong[Remark]: Many of the foundational questions in AI, such as "Can
  machines reason?", "Does the mind reduce to physics?", and "How should a
  rational agent act under uncertainty?", remain open and continue to shape AI
  research today.

// From: msml610/lectures_source/Lesson01.3-The_Foundations_of_AI.smd:553 '* References'
// Slide: References
#strong[References]

#set text(size: 0.75em)
#references("/msml610/lectures_source/refs.bib")
