// git_hash=0c2bbccf6-d9s timestamp=20260829_225551
// Import AIMA style formatting and macros.
#import "../../helpers_root/dev_scripts_helpers/typst/aima_style.typ": aima-style, algorithm, chapter, glossary

// Document metadata
#set document(
  title: "[L01.2: AI and Machine Learning]",
  author: "[MSML610: Advanced Machine Learning]",
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

- #strong[Machine Learning] is a subset of #strong[Artificial Intelligence (AI)].
  - It is often confused with #emph[deep learning], #emph[large-language models], #emph[predictive analytics], and other related fields.

- What is artificial intelligence?
  - To answer this, we must first understand what #strong[human intelligence] is.

- What is human intelligence?
  - We refer to ourselves as #"homo sapiens" because our intelligence distinguishes us from other animals.
  - Throughout history, we have sought to comprehend how we think, which remains one of the biggest mysteries.
    - The brain is a small matter yet manages to grasp the secrets of nature, such as the #emph[theory of relativity], #emph[quantum mechanics], and #emph[black holes].
    - A question arises: How can the brain understand, predict, and manipulate a world that is more complex than itself?


// From: msml610/lectures_source/Lesson01.2-AI_and_Machine_Learning.smd:33 '* Artificial Intelligence'
// Slide: Artificial Intelligence
#strong[Artificial Intelligence]

::: columns
:::: {.column width=80%}

// From: msml610/lectures_source/Lesson01.2-AI_and_Machine_Learning.smd:38 '- @Definition@: The term _"Artificial Intelligence"_ was coined in 1956'
// Slide: Definition of Artificial Intelligence
- #strong[Definition]: The term "Artificial Intelligence" was coined in 1956 [@mccarthy1955dartmouth].

- #strong[Goal]
  - Understand human intelligence.
  - Create intelligent entities.
  - #"What I cannot create, I do not understand" (Feynman, 1988).

- #strong[Characteristics]
  - AI applies to any human activity and task.
  - Its impact exceeds that of any past historical event.
  - It generates hundreds of billions of dollars in annual market revenue, with trillions projected in global economic impact by 2030 [@bughin2018aifrontier].
  - Unlike well-defined disciplines such as arithmetic or Newtonian mechanics, AI has many unresolved problems.

:::: {.column width=20%}

// From: msml610/lectures_source/Lesson01.2-AI_and_Machine_Learning.smd:58 '![](msml610/lectures_source/figures/L01.2.Richard_Feynman.jpg)'
// Slide: Richard Feynman
#figure(
  image("msml610/lectures_source/figures/L01.2.Richard_Feynman.jpg", width: 80%),
  caption: [_"Richard Feynman (1965)"],
  kind: "figure",
  supplement: [Fig.],
  placement: auto,
) <fig:feynman>

:::: 
:::


// From: msml610/lectures_source/Lesson01.2-AI_and_Machine_Learning.smd:64 '* AI Formal Definition'
// Slide: AI Formal Definition
#strong[AI Formal Definition]

::: columns
:::: {.column width=65%}

// From: msml610/lectures_source/Lesson01.2-AI_and_Machine_Learning.smd:69 '- @Definition@: AI is characterized along **two key axes** [@russell2020aima]'
// Slide: Definition of AI
- #strong[Definition]: AI is characterized along two key axes [@russell2020aima].
  - #emph[Thinking vs. Acting].
  - #emph[Human vs. Rational (ideal performance)].

- **Four resulting definitions**: AI as a machine that can:
  1. Think humanly.
  2. Think rationally.
  3. Act humanly.
  4. Act rationally.

- Which definition best captures what AI should aim for?
  
- The #strong[key idea]: Building machines that act rationally is the ultimate goal of AI.

:::: {.column width=30%}

// From: msml610/lectures_source/Lesson01.2-AI_and_Machine_Learning.smd:87 '```{=typst} #styled-table(... ```' 
// Slide: AI formal definition table
```{=typst}
#styled-table(
  headers: ("", "Human", "Rational"),
  rows: (
    ("Thinking", "Think humanly", "Think rationally"),
    ("Acting", "Act humanly", "Act rationally"),
  ),
  bold-first-col: true,
)
```
:::: 
:::


// From: msml610/lectures_source/Lesson01.2-AI_and_Machine_Learning.smd:101 '* 1. AI as Thinking Humanly'
// Slide: AI as Thinking Humanly
#strong[1. AI as Thinking Humanly]

- The problem to address: To build machines that think like humans, we must first determine how humans think.

- **Pros**:
  - This approach allows for expressing a precise theory of the human mind as a computer program.

- **Cons**:
  - The workings of the human mind are still unknown.
  - This definition is anthropocentric and may not encompass other forms of intelligence.

  
// From: msml610/lectures_source/Lesson01.2-AI_and_Machine_Learning.smd:113 '* 2. AI as Thinking Rationally'
// Slide: AI as Thinking Rationally
#strong[2. AI as Thinking Rationally]

::: columns
:::: {.column width=65%}

// From: msml610/lectures_source/Lesson01.2-AI_and_Machine_Learning.smd:118 '- @Question@: What are the rules of **correct thinking**?'
// Slide: Question about correct thinking
- What are the rules of #strong[correct thinking]?
  - Given correct premises, one must yield correct conclusions.

- The #strong[Techniques]: #strong[Logic] studies the "laws of thought".
  - This involves formalizing statements about objects and their relations.

- Another #strong[Technique]: #strong[Automatic theorem proving].
  - These programs solve problems expressed in logical notation.
  - They may run indefinitely if no solution exists, as first-order validity is only semi-decidable.

:::: {.column width=30%}

// From: msml610/lectures_source/Lesson01.2-AI_and_Machine_Learning.smd:132 '```graphviz digraph laws_of_thought { ... ```' 
// Slide: Laws of Thought diagram
```graphviz
digraph laws_of_thought {
    bgcolor="transparent";
    pad="0.15";
    splines=spline;
    nodesep=0.4;
    ranksep=0.5;
    rankdir=TB;

    node [shape=box,
          style="rounded,filled",
          penwidth=1.8,
          fontname="Helvetica",
          fontsize=12,
          margin="0.22,0.14",
          height=0.50];

    edge [color="#A3B1C0",
          penwidth=1.3,
          arrowhead=vee,
          arrowsize=0.75,
          fontname="Helvetica",
          fontsize=10,
          fontcolor="#7B8794"];

    premises [label="Correct\npremises", fillcolor="#A9DDB0", color="#4F9A5C", fontcolor="#1F4E2E"];
    logic [label="Logic", fillcolor="#FFC98A", color="#D98E2B", fontcolor="#6B4517"];
    conclusion [label="Correct\nconclusions", fillcolor="#9CC4F2", color="#3C6FB0", fontcolor="#1F4E79"];

    premises -> logic -> conclusion;
}
```
:::: 
:::


// From: msml610/lectures_source/Lesson01.2-AI_and_Machine_Learning.smd:168 '* Thinking Rationally: Challenges'
// Slide: Thinking Rationally: Challenges
#strong[Thinking Rationally: Challenges]

- #strong[Challenges]:
  1. Formalizing informal knowledge is difficult.
     - _Example_: "A handshake occurs when two people extend, grip, shake hands, then release."
     $$
     \begin{aligned}
       & \exists \; x, y, h_x, h_y \\
       & \quad Person(x) \land Person(y) \land x \neq y \land {}
       Hand(x, h_x) \land Hand(y, h_y) \land {} \\
       & \quad MoveToward(h_x, h_y) \land Contact(h_x, h_y) \land {}
       Shake(h_x, h_y) \land {} \\
       & \quad Release(h_x, h_y)
     \end{aligned}
     $$
  2. The probabilistic nature of knowledge presents challenges.
     - _Example_: In medicine, "Fever, cough, and fatigue could indicate flu, COVID-19, or another illness."
  3. Scalability challenges arise in large problems that may require heuristics for practical solutions.
  4. Intelligence encompasses more than just rational thinking.
     - An agent must interact with the world, leading to the issue of the "embodiment of AI".


// From: msml610/lectures_source/Lesson01.2-AI_and_Machine_Learning.smd:193 '* 3. AI as Acting Humanly'
// Slide: AI as Acting Humanly
#strong[3. AI as Acting Humanly]

- #strong[Definition]: An #strong[agent] is something that perceives and acts to achieve a goal.

- #strong[Goal]: AI designs agents that can act like humans.

- #strong[Techniques]: The #strong[Turing test] [@turing1950computing].
  - A computer passes the Turing test if a human cannot discern whether the answers to questions are from a person or a computer.

::: columns
:::: {.column width=75%}

// From: msml610/lectures_source/Lesson01.2-AI_and_Machine_Learning.smd:206 '- @Components@: Passing the **(embodied) Turing test** requires'
// Slide: Components of Passing Turing Test
- #strong[Components]: To pass the embodied Turing test, an agent must have:
  1. Natural language processing to communicate.
  2. Knowledge representation to store information.
  3. Automated reasoning to utilize knowledge and answer questions.
  4. Machine learning to detect patterns.
  5. Computer vision and speech recognition to perceive and interpret speech.
  6. Robotics to manipulate objects and move.

:::: {.column width=25%}

// From: msml610/lectures_source/Lesson01.2-AI_and_Machine_Learning.smd:218 '![](msml610/lectures_source/figures/L01.1.Ex_machina.jpg)'
// Slide: Ex Machina Image
#figure(
  image("msml610/lectures_source/figures/L01.1.Ex_machina.jpg", width: 80%),
  caption: [Image from "Ex Machina"],
  kind: "figure",
  supplement: [Fig.],
  placement: auto,
) <fig:exmachina>

:::: 
:::


// From: msml610/lectures_source/Lesson01.2-AI_and_Machine_Learning.smd:223 '* Turing Test: Pros and Cons'
// Slide: Turing Test: Pros and Cons
#strong[Turing Test: Pros and Cons]

::: columns
:::: {.column width=50%}

// From: msml610/lectures_source/Lesson01.2-AI_and_Machine_Learning.smd:228 '- @Pros@'
// Slide: Pros of the Turing Test
- #strong[Pros]:
  - Provides an operational definition of intelligence.
  - Avoids philosophical vagueness (e.g., questions like what consciousness is and whether machines can think).

:::: {.column width=50%}

// From: msml610/lectures_source/Lesson01.2-AI_and_Machine_Learning.smd:236 '- @Cons@'
// Slide: Cons of the Turing Test
- #strong[Cons]:
  - Intelligence is defined using anthropomorphic criteria anchored in human terms, despite the existence of multiple forms of non-human intelligence.
  - Passing the test means fooling humans into believing it is human.

:::: 
:;

// From: msml610/lectures_source/Lesson01.2-AI_and_Machine_Learning.smd:244 '- @Example@: Aeronautical engineering is about'
// Slide: Example from Aeronautical Engineering
- #strong[Example]: In aeronautical engineering:
  - Correct: Focus on wind tunnels and aerodynamics.
  - Incorrect: Designing machines that imitate birds.


// From: msml610/lectures_source/Lesson01.2-AI_and_Machine_Learning.smd:248 '* 4. AI as Acting Rationally'
// Slide: AI as Acting Rationally
#strong[4. AI as Acting Rationally]

- #strong[Definition]: #strong[Rational agents] are those that do the "right thing" given their knowledge.

- #strong[Characteristics]: Agents that act rationally should:
  1. Operate autonomously.
  2. Perceive their environment.
  3. Persist over time.
  4. Adapt to change.
  5. Create and pursue goals.

  
// From: msml610/lectures_source/Lesson01.2-AI_and_Machine_Learning.smd:260 '* Acting Rationally as Ultimate Goal of AI'
// Slide: Acting Rationally as Ultimate Goal of AI
#strong[Acting Rationally as Ultimate Goal of AI]

::: columns
:::: {.column width=65%}

// From: msml610/lectures_source/Lesson01.2-AI_and_Machine_Learning.smd:265 '- @Question@: Which definition of AI best captures what we should build?'
// Slide: Question about AI Definition
- Which definition of AI best captures our objectives?
  - Acting vs. Thinking.
  - Rational vs. Human.

- **Acting is more fundamental than Thinking**.
  - Acting rationally encompasses a broader concept than thinking rationally.

- **Rational is more objective than Human**.
  - Rationality can be mathematically defined, whereas human behavior is often shaped by evolutionary conditions.

- The #strong[key idea]: AI should focus on agents acting rationally.

:::: {.column width=30%}

// From: msml610/lectures_source/Lesson01.2-AI_and_Machine_Learning.smd:281 '```{=typst} #styled-table(... ```' 
// Slide: Rationality table
```{=typst}
#styled-table(
  headers: ("", "Human", "Rational"),
  rows: (
    ("Thinking", "Think humanly", "Think rationally"),
    ("Acting", "Act humanly", "*Act rationally*"),
  ),
  bold-first-col: true,
)
```
:::: 
:::


// From: msml610/lectures_source/Lesson01.2-AI_and_Machine_Learning.smd:295 '* Rationality Is Not Absolute'
// Slide: Rationality Is Not Absolute
#strong[Rationality Is Not Absolute]

- The problem: AI aims to construct agents that do the right thing, but what defines the "right thing"?

- #strong[Example]: You leave your house and a tree branch strikes you.
  - Did you act rationally? Probably.
  
- #strong[Example]: You cross the street without checking for traffic, resulting in being hit by a car.
  - Did you act rationally? It depends (probably not, given that checking was a low-cost option).

- #strong[Challenges]: There are moral issues related to self-driving cars, such as:
  - Should a self-driving car swerve to hit a pedestrian in order to avoid a frontal crash that would kill two people?


// From: msml610/lectures_source/Lesson01.2-AI_and_Machine_Learning.smd:313 '* Problems of a Rational Agent'
// Slide: Problems of a Rational Agent
#strong[Problems of a Rational Agent]

- #strong[Challenges]: In a probabilistic environment, a rational agent's goals must cover:
  - Best outcome in a deterministic scenario.
  - Best expected outcome in uncertain situations.

- What does "best" mean?
  - Classically, "best" is determined by the #strong[objective function].
    - Examples include the cost function, sum of rewards, loss function, and utility.
  - However, these considerations are more nuanced.

- #strong[Limitations]:
  - Omniscience vs. no-regrets: The best decision stems from available information rather than perfect knowledge.
  - In some scenarios, no provably correct action exists, yet a decision must be made.
  - Even with complete information, optimal rationality may be unattainable due to:
    - The cost of gathering all necessary data (e.g., in medical settings).
    - Computational burdens (e.g., navigating a search tree that may have more branches than atoms in the observable universe, approximately $10^{80}$).
    - Time-sensitive needs (e.g., making decisions within one microsecond in high-frequency trading, or HFT).

- #strong[Solution]: "Satisficing": Achieving "good enough" instead of "perfect" [@simon1956satisficing].
  - This approach involves acting suitably within established constraints.

  
// From: msml610/lectures_source/Lesson01.2-AI_and_Machine_Learning.smd:340 '## What Is Machine Learning?'
// Slide: What Is Machine Learning?
== What Is Machine Learning?

// From: msml610/lectures_source/Lesson01.2-AI_and_Machine_Learning.smd:342 '* Machine Learning: Definitions'
// Slide: Machine Learning: Definitions
#strong[Machine Learning: Definitions]

::: columns
:::: {.column width=75%}

// From: msml610/lectures_source/Lesson01.2-AI_and_Machine_Learning.smd:347 '- @Question@: How should we **define machine learning**?'
// Slide: Defining machine learning
- How should we define #strong[machine learning]?

- #strong[Definition]: 
   - "Machine learning is the field of study that enables computers to learn without being explicitly programmed" (Samuel, 1959) [@samuel1959checkers].
   - Machine learning builds machines to perform useful tasks without being explicitly programmed.
     - For instance, a computer learns to play checkers by leveraging self-play to memorize winning strategies.
   - More formally, "A computer program is said to learn from experience $E$ with respect to a particular task $T$ and a performance measure $P$, if $P(T)$ improves as a result of experience $E$" (Mitchell, 1997) [@mitchell1997machinelearning].

- #strong[Applications]: Common examples of machine learning include:
  - Computer vision.
  - Speech recognition.
  - Natural language processing.

:::: {.column width=20%}

// From: msml610/lectures_source/Lesson01.2-AI_and_Machine_Learning.smd:368 '![](msml610/lectures_source/figures/L01.2.Tom_Mitchell.jpg)'
// Slide: Tom Mitchell Image
#figure(
  image("msml610/lectures_source/figures/L01.2.Tom_Mitchell.jpg", width: 80%),
  caption: [_"Tom Mitchell (2025)"],
  kind: "figure",
  supplement: [Fig.],
  placement: auto,
) <fig:mitchell>

:::: 
:::


// From: msml610/lectures_source/Lesson01.2-AI_and_Machine_Learning.smd:374 '* The 3 Machine Learning Assumptions'
// Slide: The 3 Machine Learning Assumptions
#strong[The 3 Machine Learning Assumptions]

- #strong[Fact]: Machine learning addresses practical problems that include:
  - Gathering a dataset.
  - Building a statistical model algorithmically from that dataset.
  - Evaluating the model.
  - Deploying and monitoring the model.

- #strong[Problem] (Abu-Mostafa, 2012) [@abumostafa2012learning]:
  - While many phases are largely "engineering", the process of building the model is the "research" aspect.
  - The **three core assumptions** of machine learning are:
    1. A pattern exists.
    2. The pattern cannot be precisely defined mathematically.
    3. Data is available.

- #strong[Question]: Which assumption is essential?
  1. If no pattern exists, is there any point in running learning algorithms?
  2. Is there an issue in utilizing machine learning even if mathematics can define the pattern?
  3. Can progress be achieved without data?

- #strong[Remark]: Without data, no progress is achievable; hence, data availability is the truly vital assumption.

  
// From: msml610/lectures_source/Lesson01.2-AI_and_Machine_Learning.smd:399 '* AI vs ML vs Deep Learning'
// Slide: AI vs ML vs Deep Learning
#strong[AI vs ML vs Deep Learning]

::: columns
:::: {.column width=65%}

// From: msml610/lectures_source/Lesson01.2-AI_and_Machine_Learning.smd:404 '- @Definition@'
// Slide: Definitions in AI, ML, and DL
- #strong[Definition]:
  - #strong[AI (Artificial Intelligence)]: Machines programmed to reason, learn, and act rationally.
  - #strong[ML (Machine Learning)]: Machines capable of performing tasks without being explicitly programmed.
  - It is feasible to have AI models that do not fall under the remit of ML.
    - For example, handcrafted rule-based systems, such as IBM Deep Blue in chess, do not learn from data but are still classified as AI systems.

:::: {.column width=30%}

// From: msml610/lectures_source/Lesson01.2-AI_and_Machine_Learning.smd:426 '```tikz % Define colors. ... ```'
// Slide: Venn Diagram for AI, ML, and DL
```tikz
% Define colors.
  \definecolor{AIcolor}{RGB}{244,166,166}    % Red/Pink
  \definecolor{MLcolor}{RGB}{178,226,178}    % Green
  \definecolor{DLcolor}{RGB}{160,214,209}    % Teal
  \definecolor{LLMcolor}{RGB}{198,166,244}   % Purple

  % Draw AI circle
  \fill[AIcolor] (0,0) circle (3);
  \draw (0,0) circle (3);
  \node[above] at (0,2) {\textbf{AI}};

  % Draw ML circle inside AI
  \fill[MLcolor] (0.5,-0.5) circle (2);
  \draw (0.5,-0.5) circle (2);
  \node[above] at (0.5,0.5) {\textbf{ML}};

  % Draw DL circle inside ML
  \fill[DLcolor] (1,-1) circle (1);
  \draw (1,-1) circle (1);
  \node[above] at (1,-0.6) {\textbf{DL}};

  % Draw LLM circle inside DL
  \fill[LLMcolor] (1.2,-1.2) circle (0.6);
  \draw (1.2,-1.2) circle (0.6);
  \node[above] at (1.2,-1.4) {\textbf{LLMs}};
```
:::: 
:::


// From: msml610/lectures_source/Lesson01.2-AI_and_Machine_Learning.smd:457 '* Limits of AI Compared to Human Intelligence (1/2)'
// Slide: Limits of AI Compared to Human Intelligence
#strong[Limits of AI Compared to Human Intelligence (1/2)]

- #strong[Problem]: AI and ML fundamentally differ from human intelligence.
  - Machines do not learn in the same manner as humans (e.g., LLMs), leading to different limitations.
  - It remains unclear if the human brain employs gradient descent.
  - Reinforcement learning-like processes may exist within human cognition, in a specific sense.

- #strong[Limitations]:
  - **Fragility to input variations**: 
     - ML models are sensitive to minor input alterations; even slight distortions can lead to failures.
     - Adversarial attacks can misclassify inputs by changing a single pixel [@su2019onepixel].
     - Models trained on specific tasks, like video games, fail if screen conditions change even slightly, whereas humans adapt seamlessly.
  - **Lack of transfer learning**:
     - ML systems struggle to apply knowledge across different domains without retraining.
  - **Massive data and computation requirements**:
     - In comparison to humans who can learn to drive in mere hours, self-driving systems often demand billions of compute hours and extensive datasets.
  - **Poor common sense and reasoning**:
     - ML models typically lack inherent world knowledge and intuitive logic.

  
// From: msml610/lectures_source/Lesson01.2-AI_and_Machine_Learning.smd:480 '* Limits of AI Compared to Human Intelligence (2/2)'
// Slide: Limits of AI Compared to Human Intelligence (2)
#strong[Limits of AI Compared to Human Intelligence (2/2)]

- #strong[Limitations]:
  - **Opaque decision-making**: 
      - Many ML models provide little insight into their decision-making processes, which can hinder trust, interpretability, and accountability in vital applications.
  - **Dependence on narrow objectives**: 
      - While ML systems excel at optimizing specific tasks, they struggle with broader or ambiguous goals.
      - For example, an algorithm focused on maximizing user engagement may inadvertently promote harmful content.
  - **Susceptibility to bias and data quality**:
      - ML models can inherit and magnify biases present in their training datasets.
  - **Lack of embodiment and physical interaction**:
      - Human cognition is deeply rooted in physical and sensory experiences.

  
// From: msml610/lectures_source/Lesson01.2-AI_and_Machine_Learning.smd:494 '* Key Takeaways'
// Slide: Key Takeaways
#strong[Key Takeaways]

- The key idea: AI should concentrate on **agents acting rationally**, not merely on imitating human thought or behavior.

- #strong[Definition]:
  - **AI**: Machines programmed for reasoning, learning, and rational action.
  - **ML**: A subset of AI that performs tasks without explicit programming.
  - **DL**: A subset of ML that utilizes multi-layer neural networks.
  - **LLM**: A specific subset of DL trained on vast text datasets to predict text, often refined using reinforcement learning from human feedback (RLHF).

- #strong[Remark]: Despite the impressive capabilities of current ML and DL systems, they still fall short in areas such as fragility, transfer learning, data efficiency, and common-sense reasoning.

  
// From: msml610/lectures_source/Lesson01.2-AI_and_Machine_Learning.smd:510 '* References'
// Slide: References
#strong[References]

```{=typst}
#set text(size: 0.75em)
#bibliography(
  "/msml610/lectures_source/refs.bib",
  style: "/helpers_root/dev_scripts_helpers/typst/umd-references.csl",
  title: none,
)