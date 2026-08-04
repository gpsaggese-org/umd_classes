<!-- git_hash=484fdb2b-k1z timestamp=20260803_162527 -->

<center>

![](book_springer/lecture_commentary/Lesson04.1_Knowledge_Representation.jpg/slides001.jpg){width=80%}

</center>
<center>

# 2 / 31: Why Knowledge Representation Matters

</center>
<center>

![](book_springer/lecture_commentary/Lesson04.1_Knowledge_Representation.jpg/slides002.jpg){width=80%}

</center>
- **Motivation: Why KR is essential to AI**

1. **Learning alone is not enough**: Machines need to _reason_ about the world
   - When we talk about machine learning, we often focus on how machines can
     learn from data. For instance, a medical AI system might be trained on vast
     amounts of patient data to predict diseases. However, predicting is just
     one part of the equation. To be truly useful, especially in fields like
     medicine, the AI needs to explain its predictions. This is where knowledge
     representation (KR) comes in, as it helps structure the information in a
     way that can be communicated and understood by humans, like doctors.

2. **Bridges perception and reasoning**
   - Machines often gather raw data through sensors, which is known as
     perception. However, raw data alone isn't very useful. KR helps transform
     this data into knowledge that machines can use to make decisions. This
     process is what we call reasoning, and it's crucial for machines to act
     intelligently.

3. **Enables explainability**
   - Explainability is about making sure users understand why a machine made a
     certain decision. This is especially important in areas where decisions can
     have significant consequences, such as healthcare, law, or autonomous
     vehicles. KR provides the framework that allows machines to explain their
     reasoning in a way that humans can understand.

4. **Enables white-box learning**
   - In white-box learning, the internal workings of the system are transparent
     and understandable. For example, robots use abstract symbolic knowledge to
     plan their actions, and conversational agents use KR to understand and
     reason about user intent and context. This transparency is crucial for
     building trust and ensuring that AI systems behave as expected.

<center>

# 3 / 31: What Is Knowledge Representation?

</center>
<center>

![](book_springer/lecture_commentary/Lesson04.1_Knowledge_Representation.jpg/slides003.jpg){width=80%}

</center>
- **Definition**: **Knowledge Representation (KR)** is essentially about how we can encode information in a way that machines can understand and use it to make decisions. 
  - For example, this can be done through rules, logic, ontologies, and semantic networks. These are different methods or structures that help organize and define the information.
  - KR involves two main components:
    - *Structure*: This refers to how the information is organized. Think of it like a filing system where everything has its place.
    - *Semantics*: This is about the meaning of the information. It's not just about storing data but understanding what that data represents.

- **Fact**: **Knowledge Representation** is crucial in the field of Artificial
  Intelligence (AI).
  - It works alongside learning-based methods to enhance AI capabilities.
  - KR acts as a link between raw data (what the machine perceives) and the
    logical reasoning (how the machine thinks).
  - It is vital for making AI systems understandable and transparent, which is
    important for trust and accountability.

- **Example**: Machines use knowledge representation to perform various tasks:
  - They can draw conclusions from the information they have, similar to how
    humans make decisions.
  - They can plan actions based on the knowledge they possess.
  - They can answer questions by retrieving and processing relevant information.
  - These capabilities show how KR enables machines to function intelligently in
    different scenarios.

<center>

# 4 / 31: Expressiveness vs. Tractability

</center>
<center>

![](book_springer/lecture_commentary/Lesson04.1_Knowledge_Representation.jpg/slides004.jpg){width=80%}

</center>
- **Expressiveness vs. Tractability**: This slide discusses a fundamental tradeoff in artificial intelligence (AI) and machine learning (ML). The tradeoff is between how *expressive* a language or model is, meaning how richly it can capture concepts, and how *tractable* it is, meaning how efficiently it can perform reasoning or computations. More expressive systems can describe more complex ideas but often require more computational resources, making them harder to work with.

- **Key Insight**: The choice of knowledge representation should be guided by
  the specific needs of the application. This means that depending on what you
  are trying to achieve, you might prioritize expressiveness or tractability
  differently.

- **Example**:
  - **Atomic**: This approach treats each state as a single, indivisible unit.
    It's simple and easy to work with but doesn't capture complex relationships.
    An example is depth-first search algorithms, like those used in chess, where
    each board position is a distinct state.
  - **Factored**: This method captures relationships between variables but is
    limited in expressing complex structures. An example is propositional logic,
    such as in the game Minesweeper, where a breeze at a location indicates a
    pit in adjacent cells.
  - **Structured**: This is the most expressive form, capable of representing
    complex relationships and structures, but it can be undecidable, meaning not
    all problems can be solved. An example is first-order logic, which can
    express statements like "A father of a person is their parent."

This slide emphasizes the importance of balancing expressiveness and
tractability to suit the needs of different AI and ML applications.

<center>

# 5 / 31: Symbolic vs. Sub-symbolic Representation

</center>
<center>

![](book_springer/lecture_commentary/Lesson04.1_Knowledge_Representation.jpg/slides005.jpg){width=80%}

</center>
- **Symbolic Knowledge Representation (KR)**:
  - Uses discrete, human-readable symbols to represent knowledge.
  - Examples include logic and knowledge graphs.
  - *Interpretable* and suitable for rule-based reasoning, making it easier for humans to understand and verify.
  - Struggles with ambiguity and the complexity of real-world scenarios.

- **Sub-symbolic Knowledge Representation**:
  - Utilizes learned, distributed representations like vector embeddings.
  - Often referred to as "black-box" AI due to its lack of transparency.
  - Powerful in handling complex patterns and large datasets but difficult to
    interpret.

- **Neuro-symbolic Knowledge Representation**:
  - Combines symbolic and sub-symbolic approaches.
  - Aims to reason over learned concepts using structured logic, potentially
    offering the best of both worlds.

- **Diagram Explanation**:
  - The diagram illustrates the overlap between symbolic and sub-symbolic
    methods.
  - _Symbolic_ methods like decision trees are explainable.
  - _Sub-symbolic_ methods like neural networks are more opaque.
  - Machine learning sits at the intersection, incorporating elements of both.

<center>

# 6 / 31: Neuro-symbolic Approach: Conceptual Spaces

</center>
<center>

![](book_springer/lecture_commentary/Lesson04.1_Knowledge_Representation.jpg/slides006.jpg){width=80%}

</center>
- **Conceptual Spaces**: These are frameworks that use geometric structures to represent knowledge. Each dimension in this space corresponds to an interpretable feature, such as color or size. The similarity between objects is represented by how close they are in this space. A *concept* is essentially a region within this multidimensional space, grouping similar items together.

- **Pros**:
  - This approach naturally models similarity and vagueness, which are often
    challenging for traditional symbolic systems. Symbolic systems typically use
    discrete symbols without inherent structure, like simply labeling something
    as `Car` or `Bicycle`, without capturing the nuances between them.

- **Example**: Transportation methods are used to illustrate conceptual spaces.
  Here, dimensions like `Environmental Friendliness` and
  `Technological Advancement` are considered. Different types of transportation,
  such as wooden transportation (e.g., dugout canoes) and vehicles (e.g., cars,
  bicycles), are represented as regions within this space. Advanced vehicles,
  like electric and self-driving cars, form nested subsets within the broader
  vehicle category, showing their specific characteristics in relation to the
  dimensions.

<center>

# 7 / 31: Procedural vs. Declarative Representation

</center>
<center>

![](book_springer/lecture_commentary/Lesson04.1_Knowledge_Representation.jpg/slides007.jpg){width=80%}

</center>
- **Procedural approach**: This method is all about detailing *how* to perform a task. 
  - It involves encoding the specific steps or instructions directly into the program. 
  - For example, if you have a robot that needs to navigate a maze, a procedural approach would involve programming each step the robot must take to reach the end.

- **Declarative approach**: This method focuses on defining _what_ the desired
  outcome is, without specifying the steps to achieve it.
  - It describes the relationships between actions and goals, allowing the
    system to figure out the steps on its own.
  - For instance, you might tell a robot that the goal is to "reach the exit of
    the maze," and the robot would determine the best path to take.

- **Comparison**:
  - Procedural: Offers more control over the process but is less flexible
    because changes require reprogramming specific steps.
  - Declarative: Provides more abstraction, making it easier to modify or extend
    since the system handles the solution search.

- **Approach**: Many AI systems successfully combine both methods.
  - Declarative knowledge can be transformed into procedural code, allowing for
    flexibility and control.
  - For example, a planner might generate specific procedures (or plans) from a
    set of declarative goals, effectively using both approaches.

<center>

# 8 / 31: Natural Language as a Representation

</center>
<center>

![](book_springer/lecture_commentary/Lesson04.1_Knowledge_Representation.jpg/slides008.jpg){width=80%}

</center>
- **Natural languages** are languages like English or Italian that we use every day.
  - They are _expressive_, meaning they are great for communication but not always for precise representation. This means they can convey emotions and complex ideas but might not always be clear-cut.
  - They are _ambiguous_, which means a single word can have multiple meanings. For example, the word _"spring"_ can refer to the season or a coil that bounces.
  - They are _context-dependent_, meaning the meaning of words can change based on the situation or sentence. For example, the word "Look!" can be a command or an expression of surprise, depending on the context.

- The **Sapir-Whorf hypothesis** suggests that the language you speak influences
  how you see and understand the world.
  - This means that even small grammatical features, like whether nouns have
    gender, can shape your thoughts and perceptions.

- **Examples** of language influencing thought:
  - Some languages might not have words for certain concepts, like specific
    directions, which can affect how speakers of those languages think about
    space.
  - Conversely, some languages have many words for a single concept, like Arctic
    languages having numerous words for different types of snow, which allows
    for more nuanced understanding.
  - In George Orwell's "1984," the fictional language Newspeak is designed to
    limit thought by eliminating words for certain concepts, illustrating how
    language can restrict or expand our ability to think.

<center>

# 9 / 31: Programming Languages as a Representation

</center>
<center>

![](book_springer/lecture_commentary/Lesson04.1_Knowledge_Representation.jpg/slides009.jpg){width=80%}

</center>
- **Concept**: A *programming language* like C++ or Python is a structured way to communicate instructions to a computer.
  - **Data structures**: These are used to store and organize data, representing facts about the world or a problem.
  - **Code**: This is the set of instructions that manipulate these data structures, allowing us to perform tasks or solve problems in a specific domain.

- **Limitations**: Programming languages have certain constraints:
  1. They lack a general _mechanism for deriving new facts_ from existing ones.
     - This means that any updates or changes to data structures rely heavily on
       the programmer's understanding and input, rather than being automatically
       inferred.
  2. They are not expressive enough to _handle partial information_.
     - Variables in programming languages typically hold a single value or are
       undefined, which makes it difficult to represent uncertainty or
       incomplete information.
     - For example, expressing that "A white knight is in `b1` or in `f6`" is
       challenging because it involves uncertainty and multiple possibilities.

- **Concept**: In a _declarative language_, the separation of knowledge and
  inference is emphasized:
  1. **Knowledge**: This involves representing the specific problem or domain,
     where the meaning of a statement is derived from its components (known as
     compositional semantics).
  2. **Inference**: This process is independent of the domain, meaning it can be
     applied broadly without needing specific domain knowledge.
  - Examples include logical systems like propositional logic and first-order
    logic, which focus on the relationships between statements rather than the
    specific steps to achieve a result.

<center>

# 10 / 31: Propositional Logic: Syntax and Semantics

</center>
<center>

![](book_springer/lecture_commentary/Lesson04.1_Knowledge_Representation.jpg/slides010.jpg){width=80%}

</center>
- **Propositional Logic**: This is a system used to reason about statements that can be either true or false. It's like a language for logic where we can express and evaluate statements.

- **Syntax**: This refers to the rules that define how sentences in
  propositional logic are constructed. It includes:
  - **Proposition Symbols**: These are basic statements that can be true or
    false, like "P" or "Q".
  - **Logical Connectives**: These are symbols used to connect propositions,
    such as "and" ($\land$), "or" ($\lor$), and "not" ($\neg$). For example,
    "$P \land Q$" means "P and Q".

- **Semantics**: This is about understanding what the sentences mean and how to
  determine their truth value.
  - **Truth Tables**: These are tables used to show how the truth value of a
    complex sentence depends on the truth values of its components. For example,
    if "P" is true and "Q" is false, then "$P \land Q$" is false.
  - **Deduction Rules**: These are rules used to infer the truth of a sentence
    from other sentences.

- **Applications**: Propositional logic is used in various practical
  applications:
  - _SAT Solvers_: These are tools that check if there is a way to make a
    propositional logic formula true. They are used in fields like hardware
    verification and solving scheduling problems.

  - _Expert Systems_: These systems use logic rules to simulate human
    decision-making, such as in medical diagnosis systems where they help in
    identifying diseases based on symptoms.

  - _Rule-based Agents_: These are systems that operate based on a set of
    predefined rules, like automated customer service chatbots that respond to
    queries based on specific rules.

<center>

# 11 / 31: First-Order Logic: Quantifiers and Inference

</center>
<center>

![](book_springer/lecture_commentary/Lesson04.1_Knowledge_Representation.jpg/slides011.jpg){width=80%}

</center>
- **Quantifiers** are tools used in logic to describe properties of groups of objects rather than listing each object individually. This is different from propositional logic, where each object is named specifically. Quantifiers help us make broader statements about collections.

- **Universal quantifier**: Represented as $\forall x\, P(x)$, this quantifier
  is used to make statements that apply to _every_ object in a set. For example,
  if we say $\forall x\, P(x)$, it means that the property $P(x)$ holds true for
  all possible values of $x$. This is a powerful way to express general truths
  or rules.

- **Existential quantifier**: Represented as $\exists x\, P(x)$, this quantifier
  is used to assert that there is _at least one_ object for which the property
  $P(x)$ is true. It doesn't specify which object, just that such an object
  exists. This is useful for expressing the existence of something without
  needing to identify it specifically.

- Variables in logic can be **bound** or **free**. A variable is bound when it
  is associated with a quantifier, like in
  $\forall x (Cat(x) \rightarrow Mammal(x))$, where $x$ is bound by the
  universal quantifier. If a variable is not associated with a quantifier, it is
  considered free, meaning it doesn't have a specific value or range defined by
  the logic statement.

<center>

# 12 / 31: Logical Entailment and Inference

</center>
<center>

![](book_springer/lecture_commentary/Lesson04.1_Knowledge_Representation.jpg/slides012.jpg){width=80%}

</center>
- **Logical Entailment**: This concept is about understanding how one statement can logically follow from another within a knowledge base (KB). 
  - When we say "$\alpha$ **entails** $\beta$" (written as $\alpha \models \beta$), it means that in every possible scenario where $\alpha$ is true, $\beta$ must also be true. This is like saying that the truth of $\alpha$ guarantees the truth of $\beta".
  - The notation $M(\alpha) \subseteq M(\beta)$ means that the set of all scenarios where $\alpha$ is true is a subset of those where $\beta$ is true.

- **Example**: In a scenario where it rains and the ground is wet:
  - If $\alpha$ is "Rain = True, WetGround = True", it entails $\beta$, which is
    "Rain implies WetGround".
  - This means if you observe rain and wet ground, you can logically conclude
    that the rule "if it rains, then the ground is wet" holds true in this
    context.
  - Here, a specific observation supports a more general rule.

- **Example**: In a mathematical context:
  - If $\alpha$ is "$x = 0$", it entails $\beta$, which is "$x \cdot y = 0$".
  - This is because if $x$ is zero, then $x \cdot y$ will always be zero, no
    matter what $y$ is.

- **Intuition**:
  - Entailment is about maintaining truth across all possible scenarios, not
    about proving something.
  - It acts as a guideline for what beliefs should be consistent within a
    knowledge base.
  - If you trust your knowledge base, you should also trust the conclusions that
    logically follow from it.

<center>

# 13 / 31: Non-Monotonic Logic and Default Reasoning

</center>
<center>

![](book_springer/lecture_commentary/Lesson04.1_Knowledge_Representation.jpg/slides013.jpg){width=80%}

</center>
- **Non-monotonic logic** is a type of logic where adding new information can change or invalidate conclusions that were previously drawn. This is different from classical logic, where once something is proven true, it remains true regardless of any new information.

- **Comparison**:
  - In _classical logic_, once you reach a conclusion, it stays valid even if
    you learn new things. This is because classical logic assumes that all
    relevant information is already known.
  - In _non-monotonic logic_, conclusions can change when new facts are
    introduced. This reflects a more realistic approach to reasoning, as it
    acknowledges that our understanding of the world can evolve with new
    information.

- **Example**:
  - Imagine you have a knowledge base (KB) that includes the statements: "Birds
    typically fly" and "Tweety is a bird." From this, you might conclude that
    "Tweety can fly."
  - However, if you learn a new fact, such as "Tweety is a penguin" and
    "penguins cannot fly," you would revise your conclusion to "Tweety cannot
    fly." This shows how non-monotonic logic allows for conclusions to be
    updated with new information.

- **Intuition**:
  - In the real world, we often have incomplete or changing knowledge.
    Non-monotonic logic is useful because it allows reasoning systems to be
    flexible and adapt to new circumstances, much like how humans adjust their
    beliefs when they learn new things. This adaptability is crucial for
    creating systems that can operate effectively in dynamic environments.

<center>

# 14 / 31: Open World vs. Closed World Assumptions

</center>
<center>

![](book_springer/lecture_commentary/Lesson04.1_Knowledge_Representation.jpg/slides014.jpg){width=80%}

</center>
- **Closed World Assumption (CWA)**: This is a way of thinking where if we don't have information about something, we assume it to be false. This is common in systems like relational databases, where if a piece of data isn't present, it's assumed not to exist. For example, if a database tells us "Alice takes CS101" but says nothing about Bob, under CWA, we conclude that "Bob does not take CS101." This assumption works well in environments where the data is complete and static.

- **Open World Assumption (OWA)**: In contrast, OWA assumes that missing
  information is simply unknown, not false. This is useful in contexts like the
  semantic web, where data is often incomplete or constantly being updated. For
  instance, if we know "Alice takes CS101" and have no information about Bob,
  under OWA, we conclude that "Bob's enrollment is unknown." This approach is
  more flexible and realistic in dynamic and evolving data environments.

- **Key Differences**: The main difference between CWA and OWA is how they
  handle missing information. CWA assumes absence means false, while OWA treats
  it as unknown. Understanding these assumptions is crucial when designing
  systems that rely on data, as they affect how conclusions are drawn from
  incomplete information.

<center>

# 15 / 31: Inductive Logic Programming: Learning Rules from Examples

</center>
<center>

![](book_springer/lecture_commentary/Lesson04.1_Knowledge_Representation.jpg/slides015.jpg){width=80%}

</center>
- **Inductive Logic Programming (ILP)** is a method in machine learning that focuses on learning logical rules from examples and existing knowledge.
  - It works by taking a set of positive and negative examples, along with some background facts, and then inferring rules that can explain these examples. This is useful for creating models that can make predictions or decisions based on logical reasoning.

- **Example**:
  - _Background knowledge_ might include facts like "Birds have wings."
  - A _positive example_ could be "Tweety is a bird that can fly," indicating
    that Tweety fits the rule.
  - A _negative example_ might be "Penguin cannot fly," showing an exception to
    the general rule.
  - From these, ILP might learn a rule such as "Birds can fly unless they are
    penguins," which captures both the general case and the exception.

- **Pros**:
  - ILP produces rules that are easy for humans to read and understand, which is
    beneficial for transparency and interpretability.
  - It combines learning with symbolic reasoning, allowing for more
    sophisticated decision-making.
  - It can incorporate existing knowledge, making it more efficient and
    effective in certain contexts.

- **Challenges**:
  - ILP can be computationally intensive, especially when dealing with large
    datasets, as it requires searching through many possible rules.
  - It can handle noisy or incomplete data, but this can complicate the learning
    process and affect the accuracy of the rules generated.

- **Knowledge Representation Frameworks** like Description Logics are important
  in the context of ILP as they provide a structured way to represent and reason
  about the knowledge that ILP uses to learn rules.

<center>

# 16 / 31: Rule-Based Systems and Knowledge-Based Agents

</center>
<center>

![](book_springer/lecture_commentary/Lesson04.1_Knowledge_Representation.jpg/slides016.jpg){width=80%}

</center>
- **Definition**: A *rule-based system* is a type of artificial intelligence that uses "if-then" rules to make decisions or draw conclusions.
  - These systems are designed to mimic how humans make decisions by applying logical rules to a set of known facts. Essentially, they follow a structured approach to problem-solving, similar to how a person might use a checklist or a flowchart to reach a decision.

- **Key components**:
  - _Knowledge base_: This is where all the facts and rules are stored. Think of
    it as a library of information that the system can refer to when making
    decisions.
  - _Inference engine_: This component is responsible for applying the rules to
    the facts stored in the knowledge base. It’s like the brain of the system,
    figuring out what new information can be inferred or what actions should be
    taken.
  - _Working memory_: This is where the current facts being considered are
    temporarily held. It’s similar to a notepad where the system jots down what
    it knows at the moment.

- **Algorithm**:
  - _Match_: The system looks for rules that match the current facts. This is
    the first step in determining what actions to take.
  - _Conflict resolution_: If multiple rules match, the system must decide which
    one to apply. This step ensures that the system makes the best decision when
    faced with multiple options.
  - _Act_: The chosen rule is applied, which may modify the current facts or
    trigger an action. This is where the system actually does something based on
    its decision.
  - _Repeat_: The process continues until no more rules can be applied, ensuring
    that all possible conclusions or actions are considered.

- **Example**:
  - _Rule_: If a patient has a fever and a rash, then suggest measles.
  - _Fact_: The patient currently has a fever and a rash.
  - _Conclusion_: Based on the rule, the system suggests that the patient might
    have measles. This example illustrates how rule-based systems can be used in
    medical diagnosis by applying logical rules to symptoms.

<center>

# 17 / 31: Grounding: Connecting Symbols to the World

</center>
<center>

![](book_springer/lecture_commentary/Lesson04.1_Knowledge_Representation.jpg/slides017.jpg){width=80%}

</center>
- **Grounding**: This concept is about connecting abstract symbols, like those found in a knowledge base (KB), to real-world entities or observations. For example, when we have the symbol `Apple` in a KB, grounding ensures that this symbol is linked to the actual fruit "apple" that we can see and touch. This connection is crucial because it acts as a bridge between how we represent information in a KB and how it exists in the real world.

- **Goals**: The main aim of grounding is to make sure that the representations
  we use are meaningful and not just empty symbols. This is important because it
  allows agents, like robots or software, to interact with the real world in a
  meaningful way. Without grounding, these agents might end up manipulating
  symbols without any real-world relevance, which would limit their usefulness.

- **Limitations**: Grounding is not without its challenges. One major issue is
  dealing with noisy or incomplete sensory data, which can make it hard to
  accurately connect symbols to real-world entities. Additionally, the mapping
  from inputs (like sensory data) to concepts can be complex and dependent on
  context, making it a difficult task.

- **Applications**: Grounding is used in various fields. In robotics, it helps
  with object recognition and manipulation, allowing robots to understand and
  interact with their environment. In natural language understanding, grounding
  helps systems comprehend and process human language in a way that relates to
  the real world. It is also crucial for autonomous agents and cognitive
  systems, enabling them to operate effectively in dynamic environments.

<center>

# 18 / 31: Ontologies: Components and Structure

</center>
<center>

![](book_springer/lecture_commentary/Lesson04.1_Knowledge_Representation.jpg/slides018.jpg){width=80%}

</center>
- **Classes / Concepts**: These are the broad categories or types of things within a particular domain. Think of them as the general ideas or groups that you can use to categorize specific items. For example, in the domain of transportation, `Car` would be a class that includes all types of cars.

- **Individuals / Instances**: These are the specific examples or members of a
  class. If `Person` is a class, then `GP` could be an individual, representing
  a specific person. Similarly, `Rome` is an instance of the class `City`, and
  `Ferrari 458` is an instance of the class `Car`.

- **Properties / Relations**: These define how classes or instances are
  connected or interact with each other. For example, `isMortal` might be a
  property that applies to the class `Person`, indicating that all people are
  mortal. `locatedIn` could describe the relationship between a `City` and a
  `Country`.

- **Attributes / Data values**: These are specific pieces of information
  associated with an instance. For example, the attribute `hasAge` might be used
  to specify the age of a person, such as `GP`.

- **Constraints**: These are rules that limit what values properties can have.
  For instance, a constraint might specify that a `Ferrari 458` must be `red`,
  meaning that this particular car model is only available in that color.

- **Axioms**: These are logical statements that establish rules or truths within
  the ontology. An example is the axiom that states all humans are mortal, which
  can be expressed in logical terms as: for every `x`, if `x` is a `Person`,
  then `x` is `Mortal`.

- **Hierarchies**: These are structures that organize classes and properties
  into levels of generality or specificity. For example, `Student` might be a
  subclass of `Person`, indicating that every student is also a person, but not
  every person is a student. This helps in understanding the relationships and
  inheritance of properties within the ontology.

<center>

# 19 / 31: Ontologies: A Worked Example (University Domain)

</center>
<center>

![](book_springer/lecture_commentary/Lesson04.1_Knowledge_Representation.jpg/slides019.jpg){width=80%}

</center>
- **Classes**
  - **Student, Professor, Course, Department**: These are the main categories or types of entities in the university domain. Each class represents a group of similar objects or concepts. For example, the `Student` class includes all individuals who are students.

- **Graph Representation**
  - The diagram uses a graph to visually represent the ontology. Each node
    represents a class or an individual, and the edges show relationships
    between them. The nodes are styled with different colors to distinguish
    between classes and individuals.

- **Properties**
  - **takesCourse**: This property links a `Student` to a `Course`, indicating
    which courses a student is enrolled in.
  - **teachesCourse**: This property connects a `Professor` to a `Course`,
    showing which courses a professor is responsible for teaching.
  - **belongsToDepartment**: This property associates both `Students` and
    `Professors` with a `Department`, indicating their departmental affiliation.

- **Individuals**
  - **Student**: Alice and Bob are specific examples of the `Student` class.
  - **Professor**: GP and DrNo are specific examples of the `Professor` class.
  - **Course**: DATA605 and MSML610 are specific examples of the `Course` class.

- **Axioms**
  - These are rules that define constraints within the ontology. For instance,
    every `Course` must have exactly one `Professor` teaching it, and every
    `Student` must be part of exactly one `Department`. These axioms ensure
    consistency and logical structure within the ontology.

- **Reasoning in Ontologies**
  - This involves using the defined classes, properties, individuals, and axioms
    to infer new information or check the consistency of the data. For example,
    reasoning can help determine if a student is taking a course that is not
    offered by their department, which might indicate an error in the data.

<center>

# 20 / 31: Reasoning in Ontologies: Inference Tasks

</center>
<center>

![](book_springer/lecture_commentary/Lesson04.1_Knowledge_Representation.jpg/slides020.jpg){width=80%}

</center>
- **Subsumption**
  - This task asks the question: _"Is class `A` a subclass of `B`?"_ It involves determining if one concept is more general than another. For example, if `Person` subsumes `Student`, it means every `Student` is also a `Person`. This is crucial for building taxonomies and ontologies because it helps in organizing concepts into a hierarchy where more specific concepts are nested under more general ones. Understanding subsumption is key to structuring knowledge in a way that reflects real-world relationships.

- **Satisfiability**
  - This task addresses the question: _"Can an instance of a concept exist?"_ It
    involves testing if a concept is logically consistent, meaning it doesn't
    contain contradictions. For instance, if you define a `FlyingPenguin` that
    requires flying but also define it as a penguin (which cannot fly), the
    concept might be unsatisfiable. Ensuring satisfiability is important to
    avoid logical errors in knowledge representation, ensuring that the concepts
    we define can exist in reality.

- **Classification**
  - This task involves _organizing concepts into a hierarchy_. It automatically
    arranges concepts by checking subsumption relationships. For example, with
    definitions of `Animal`, `Bird`, and `Penguin`, classification would place
    `Penguin` under `Bird`, and `Bird` under `Animal`. This process helps in
    understanding and visualizing the relationships between different concepts,
    making it easier to navigate and utilize the knowledge structure
    effectively.

<center>

# 21 / 31: Description Logics and OWL

</center>
<center>

![](book_springer/lecture_commentary/Lesson04.1_Knowledge_Representation.jpg/slides021.jpg){width=80%}

</center>
- **Description Logic**: This is a type of logic used to represent structured knowledge about a specific domain. It aims to strike a balance between being expressive enough to capture complex ideas and being computationally efficient so that it can be used effectively in real-world applications. It is more expressive than propositional logic, which deals with simple true/false statements, but less expressive than first-order logic, which can handle more complex relationships and quantifications.

- **Components**:
  - _Classes_: These are abstract groups or categories, like $Person$ or
    $Animal$, that help organize knowledge into meaningful categories.
  - _Properties_: These are binary relations that describe how two things are
    related, such as $hasChild$ or $ownsPet$.
  - _Instances_: These are specific objects or entities within the domain, like
    a particular person $GP$ or GP's dog $Nuvolo$.

- **Reasoning tasks**:
  - _Concept subsumption_: This involves determining whether one class is a
    subset of another, essentially asking if all members of class $A$ are also
    members of class $B$.
  - _Instance checking_: This involves verifying whether a specific instance
    belongs to a particular class.

- **Syntax**: Description logic uses a combination of atomic concepts and roles
  along with logical constructors like $\sqcap$ (and), $\sqcup$ (or), $\neg$
  (not), $\forall$ (for all), and $\exists$ (there exists). For example, the
  expression $Father \equiv Man \sqcap \exists hasChild.Person$ defines a father
  as a man who has at least one child.

- **Examples**: Description logic is widely used in creating ontologies, such as
  the Web Ontology Language (OWL), which is used to define and share web-based
  knowledge.

<center>

# 22 / 31: RDF and SPARQL: Representation Standards

</center>
<center>

![](book_springer/lecture_commentary/Lesson04.1_Knowledge_Representation.jpg/slides022.jpg){width=80%}

</center>
- **Statements form directed graphs of nodes and edges**
  - RDF, or Resource Description Framework, is a way to represent information about resources on the web. It uses a structure similar to a graph, where each piece of information is a statement made up of nodes (the resources or subjects) and edges (the relationships or predicates). This graph structure allows for flexible and powerful data representation.

- **Components are URIs to ensure global uniqueness or literals**
  - In RDF, each resource is identified by a URI (Uniform Resource Identifier),
    which ensures that every resource is globally unique. This is crucial for
    maintaining consistency and avoiding confusion when data is shared across
    different systems. For example, a URI like `http://example.org/Nuvolo`
    uniquely identifies a specific resource. Literals, on the other hand, are
    used for values like strings or numbers.

- **Building knowledge graphs**
  - RDF is often used to create knowledge graphs, which are networks of
    interconnected data that represent real-world entities and their
    relationships. These graphs are valuable for organizing and retrieving
    complex information.

- **Semantic search**
  - RDF supports semantic search, which goes beyond traditional keyword-based
    search by understanding the meaning and context of the search terms. This
    leads to more accurate and relevant search results.

- **Supporting ontologies**
  - RDF is also used to support ontologies, which are formal representations of
    knowledge within a domain. Ontologies define the types of entities and
    relationships that can exist, providing a framework for organizing and
    interpreting data.

<center>

# 23 / 31: Semantic Networks and Knowledge Graphs

</center>
<center>

![](book_springer/lecture_commentary/Lesson04.1_Knowledge_Representation.jpg/slides023.jpg){width=80%}

</center>
- **Semantic Networks**: These are a way to represent knowledge using graphs. In these graphs, the *nodes* are the concepts or entities, and the *edges* are the relationships between these concepts. For example, in a semantic network, you might have a node for "Dog" and another for "Animal," with an edge labeled "is-a" connecting them. This edge indicates that a dog is a type of animal, and it helps in understanding that dogs inherit traits common to animals.

- **Components**:
  - _Nodes_: These are the individual concepts or entities within the network.
    Think of them as the nouns in a sentence.
  - _Edges_: These represent the relationships between the nodes. They can be
    thought of as the verbs or prepositions that connect the nouns. Common
    relationships include "is-a" (indicating a hierarchical relationship) and
    "part-of" (indicating a component relationship).

- **Examples**:
  - _WordNet_: A large lexical database of English where words are grouped into
    sets of synonyms.
  - _ConceptNet_: A semantic network that connects words and phrases with
    labeled edges, representing common sense knowledge.

- **Pros**:
  - They are easy to visualize, making it simple to see how concepts are
    related.
  - They support reasoning, allowing systems to infer new information based on
    existing relationships.
  - They have been used in both early artificial intelligence systems and modern
    knowledge graph applications, showing their versatility and enduring
    usefulness.

<center>

# 24 / 31: Why Logic Fails Under Uncertainty

</center>
<center>

![](book_springer/lecture_commentary/Lesson04.1_Knowledge_Representation.jpg/slides024.jpg){width=80%}

</center>
- **Logic-based AI systems**:
  - These systems rely on propositional logic, which is a type of logic that uses statements that can be either true or false. 
  - They use rules to represent actions, meaning they follow a structured approach where specific conditions lead to specific outcomes. For example, a rule might state that if certain conditions (preconditions P) are met, then a particular action (A) will lead to a specific effect (E).

- **Example**:
  - Consider the statement, _"If I turn the car key, the engine starts"_. This
    is a straightforward logical rule. However, in reality, this rule might not
    always hold true because there are other factors that can affect the
    outcome. For instance, the battery might be dead, there might be no fuel, or
    the starter could be broken. These factors introduce uncertainty that logic
    alone cannot handle.

- **Problem**: Real-world agents face _uncertainty_ due to several factors:
  1. **Partial observability**: Agents often cannot see or know everything about
     the environment they are in. This means they have to make decisions based
     on incomplete information, which can lead to unexpected outcomes.
  2. **Non-determinism**: In the real world, actions do not always lead to
     predictable results. Even if the same action is taken under the same
     conditions, the outcome might vary due to unforeseen variables.
  3. **Adversarial conditions**: Sometimes, other agents or factors actively
     work against the agent's goals. This can include competition or
     interference from other entities, making it difficult to predict outcomes
     using simple logic.

<center>

# 25 / 31: Bayesian Networks: Definition and Structure

</center>
<center>

![](book_springer/lecture_commentary/Lesson04.1_Knowledge_Representation.jpg/slides025.jpg){width=80%}

</center>
- **Aka**: Bayesian networks are also known by several other names. These include *"Bayes nets"*, *"Belief networks"*, *"Probabilistic networks"*, and *"Graphical models"*. The term *"Causal networks"* is used when the arrows in the network have a special meaning, indicating causal relationships.

- **Definition**: A _Bayesian network_ is a type of graph called a Directed
  Acyclic Graph (DAG). This means:
  1. **Nodes**: Each node in the graph represents a random variable. These
     variables can be either discrete (like a coin flip) or continuous (like
     temperature).
  2. **Edges**: The arrows or lines connecting the nodes show dependencies
     between the variables. For example, if there is an arrow from node X to
     node Y, X is considered a _parent_ of Y, and Y is a _child_ of X. This can
     also extend to terms like ancestors and spouses, which describe more
     complex relationships.
  3. **Conditional Probability Table (CPT)**: Each node has an associated table
     that shows the probability of the node given its parents. This table
     quantifies how the parent nodes influence the node. If a node does not have
     any parents, it is assigned a prior probability, which is its probability
     without any other influences.

- **Causal Graphical Models**: These are a specific type of Bayesian network
  where the arrows are interpreted as causal relationships, meaning they show
  how one variable can directly affect another.

<center>

# 26 / 31: Causal Networks (Causal DAGs): Definition and Structure

</center>
<center>

![](book_springer/lecture_commentary/Lesson04.1_Knowledge_Representation.jpg/slides026.jpg){width=80%}

</center>
- **Causal DAG**
  - *Directed*: In a Causal Directed Acyclic Graph (DAG), the arrows indicate the direction of causation, meaning one variable causes another. For example, if you have an arrow from A to B, it means A causes B.
  - *Acyclic*: This means there are no loops in the graph. You can't have a situation where a variable eventually causes itself. This is important because it reflects the natural order of events where causes happen before their effects. If there were cycles, it would imply a variable is causing itself, which doesn't make sense in a causal context.

- **Benefits**
  - Causal DAGs clearly show the causal relationships between variables, which
    helps in understanding how changes in one variable might affect others.
  - They are useful in creating AI models that are easier to interpret because
    they show how different factors are related causally.
  - These graphs help in making stable predictions about probabilities when
    conditions change, which is crucial for reliable decision-making.
  - They allow us to think about what might happen if we change something
    (interventions) or what could have happened under different circumstances
    (counterfactuals).

- **Limitations**
  - Building a Causal DAG requires a good understanding of the domain because
    you need to know how variables are causally related.
  - The model assumes that all important variables are included. If there are
    hidden variables that affect the relationships, the model might give
    incorrect conclusions. This is a significant challenge because missing
    variables can lead to misleading causal inferences.

<center>

# 27 / 31: The Ladder of Causation: Association, Intervention, Counterfactual

</center>
<center>

![](book_springer/lecture_commentary/Lesson04.1_Knowledge_Representation.jpg/slides027.jpg){width=80%}

</center>
- **Example**: Severe weather alert to the public
  - This example illustrates how information about a tornado is communicated to the public. It shows the steps involved in alerting residents about severe weather conditions, specifically a tornado.

- **Causal diagram**:
  - **$T$**: Tornado forms
    - This is the initial event where a tornado develops. It is the starting
      point of the causal chain.
  - **$W$**: National Weather Service issues tornado warning
    - Once a tornado forms, the National Weather Service issues a warning. This
      is a crucial step in the process as it triggers further actions.
  - **$A, B$**: Radio and TV broadcast emergency
    - After the warning is issued, radio and TV channels broadcast the emergency
      alert. These are the mediums through which the warning reaches the public.
  - **$R$**: Residents warned
    - The final outcome is that residents receive the warning and can take
      necessary precautions.

- **Assumptions**
  - **Channels broadcast only on official order**
    - This means that radio and TV will only broadcast the warning if it comes
      from an official source, ensuring the information is accurate and
      reliable.
  - **Delivery systems never fail**
    - It is assumed that the communication systems (radio and TV) are always
      operational and do not experience technical failures.
  - **If either channel activates, residents warned**
    - This assumption ensures redundancy; if either the radio or TV broadcasts
      the warning, residents will be informed, increasing the likelihood that
      the message is received.

This slide uses a causal diagram to visually represent the flow of information
from the formation of a tornado to residents being warned. It highlights the
importance of each step in the communication process and the assumptions that
ensure the system's effectiveness.

<center>

# 28 / 31: Structural Causal Models (SCM): Definition

</center>
<center>

![](book_springer/lecture_commentary/Lesson04.1_Knowledge_Representation.jpg/slides028.jpg){width=80%}

</center>
- **Structural Causal Model (SCM)**: This is a way to take a causal Directed Acyclic Graph (DAG) and turn it into mathematical equations. These equations help us understand how different variables in a system are connected and influence each other.

- **Structure of SCMs**:
  - _Variables_ like $X_1, X_2, ..., X_n$ are used to represent different parts
    or quantities within a system. Think of them as the pieces of a puzzle.
  - _Equations_ are used to describe each variable. They show how a variable is
    affected by its direct causes, which are other variables that have a direct
    impact on it.
  - Formally, each variable $X_i$ is expressed as:
    $$X_i = f_i(Parents(X_i), \varepsilon_i)$$
    - _Parents(X_i)_ are the direct causes of $X_i$. These are the variables
      that directly influence $X_i$.
    - _$\varepsilon_i$_ is a noise term. It represents random factors that
      affect $X_i$ but are not observed directly.

- **Properties**:
  - SCMs share properties with causal networks. They help explain how variables
    are causally related and allow us to reason about and simulate these
    relationships.
  - They also help in quantifying the effect of one variable on another, which
    is crucial for understanding causality.

- SCMs have been used for a long time in fields like econometrics and genetics,
  even before the formal theory of causality was developed. This shows their
  importance and utility in understanding complex systems.

<center>

# 29 / 31: Markov Logic Networks: Combining Logic and Probability

</center>
<center>

![](book_springer/lecture_commentary/Lesson04.1_Knowledge_Representation.jpg/slides029.jpg){width=80%}

</center>
- **Markov Logic Networks (MLNs)**:
  - MLNs are a way to combine two powerful concepts: *first-order logic* and *probability*. First-order logic helps us express complex relationships and rules using logical statements, while Markov Random Fields allow us to handle uncertainty by assigning probabilities.
  
- **Elements of MLNs**:
  - Each part of an MLN is a pair $(F_i, w_i)$:
    - **$F_i$**: This is a logical formula, like a rule. For example, "If two people are friends, they are likely to be similar" can be written as "$Friends(x,y) \implies Similar(x,y)$".
    - **$w_i$**: This is a weight that tells us how strong our belief is in the formula $F_i$. A higher weight means the formula has a bigger impact on the probability distribution.

- **Semantics**:
  - MLNs help us define a probability distribution over all possible scenarios,
    called _possible worlds_. A possible world is just a way of assigning true
    or false to every statement we can make.
  - If a world satisfies many formulas with high weights, it is considered more
    likely.

- **Joint distribution**:
  - The probability of a particular world $x$ is given by a formula:
    $\Pr(X=x) = \frac{1}{Z} \exp\left(\sum_i w_i n_i(x)\right)$.
  - Here, $n_i(x)$ is the count of how many times the formula $F_i$ is true in
    the world $x$. For example, if the formula "Friends(x,y) → Similar(x,y)" is
    true for 7 out of 10 pairs in world $x$, then $n_i(x)=7$.

- **Special cases**:
  - If all weights $w_i$ are very large, the MLN behaves like classical logic,
    meaning only worlds where all formulas are true have any chance of
    occurring.
  - If weights are finite, the MLN allows some formulas to be false, but these
    worlds are less likely. This flexibility is what makes MLNs powerful for
    real-world applications where not everything is black and white.

<center>

# 30 / 31: From Correlation to Causal Reasoning: What Graphs Add

</center>
<center>

![](book_springer/lecture_commentary/Lesson04.1_Knowledge_Representation.jpg/slides030.jpg){width=80%}

</center>
- **Bayesian networks** are a way to represent how different variables might be related in terms of probability.
  - The arrows in these networks show *conditional dependence*, meaning how one variable might depend on another, but they do not show *causality*. For example, an arrow from $A$ to $B$ means we need to know the probability of $A$ given $B$, written as $\Pr(A | B)$.

- **Many possible Bayesian networks** can be created using the same variables
  but with different connections between them. These different networks can all
  explain the same situation or data.

- **Example**:
  - Consider a scenario with two variables: $Fire$ and $Smoke$. These are
    dependent on each other.
  - In one network, $Fire \to Smoke$, you need to know the probability of $Fire$
    and the probability of $Smoke$ given $Fire$ to find the joint probability of
    both happening together.
  - In another network, $Smoke \to Fire$, you need the probability of $Smoke$
    and the probability of $Fire$ given $Smoke$.

- **Different Bayesian networks**:
  - Although they might look different, these networks can be equivalent in
    terms of the information they provide.
  - However, some networks might be easier or harder to estimate based on the
    data available.

- There is an **asymmetry in nature**:
  - For example, if you put out a fire, the smoke will stop. But if you clear
    the smoke, it doesn't necessarily mean the fire will stop. This highlights
    that while Bayesian networks can show dependencies, they don't inherently
    show cause and effect.

<center>

# 31 / 31: Choosing a Representation: Logic, Probability, or Causal Graphs

</center>
<center>

![](book_springer/lecture_commentary/Lesson04.1_Knowledge_Representation.jpg/slides031.jpg){width=80%}

</center>
- **Causal networks are Bayesian networks with only causal edges**
  - Causal networks focus on understanding the *cause-and-effect* relationships rather than just statistical correlations.
  - For example, instead of merely asking if two variables like $Smoke$ and $Fire$ are correlated, we aim to determine the direction of causality: does $Fire$ cause $Smoke$, or vice versa?

- **"Dependency in nature" is like assignment in programming**
  - This concept suggests that nature has a way of assigning outcomes based on
    certain conditions, similar to how variables are assigned values in
    programming.
  - For instance, $Smoke$ is a result of $Fire$, represented as
    $Smoke := f(Fire)$, indicating that $Smoke$ depends on $Fire$.

- **Structural equations describe "assignment mechanism" in causal graphs**
  - Structural equations are used to express how one variable causally
    influences another in a causal graph.
  - The notation $X_i := f(X_j) \iff X_j \to X_i$ means that $X_j$ causes $X_i$,
    establishing a direct causal link between the two variables.
