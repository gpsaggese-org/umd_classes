// git_hash=52575121d-e3r timestamp=20260830_190930
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


As @fig:airelatestomanyotherdisciplines shows, Diagram relating AI.

#figure(
  image("Lesson01.3-The_Foundations_of_AI.typ.figs/Lesson01.3-The_Foundations_of_AI.1.png", width: 70%),
  caption: [Diagram relating AI to Philosophy, Mathematics, Economics, Neuroscience, Psychology, Computer engineering, Control theory and Linguistics],
  kind: "figure",
  supplement: [Fig.],
  placement: auto,
) <fig:airelatestomanyotherdisciplines>

// From: msml610/lectures_source/Lesson01.3-The_Foundations_of_AI.smd:29 '## Philosophy'
// Slide: Philosophy
== Philosophy

// From: msml610/lectures_source/Lesson01.3-The_Foundations_of_AI.smd:31 '* AI and Philosophy (1/2)'
// Slide: AI and Philosophy (1/2)
#strong[AI and Philosophy (1/2)]

Can formal rules be used to draw valid conclusions? This question sits at the
heart of the rationalist tradition. Logic, the study of rules governing proper
reasoning, traces back to Aristotle (384–322 BCE), who formulated laws meant to
capture how a rational mind should operate. The ambition to mechanize at least
part of that reasoning is equally old in spirit: machines capable of arithmetic
operations, such as the #strong[Pascaline] built by Blaise Pascal in 1642,
showed early on that formal symbol manipulation could be offloaded from human
minds to physical devices. #strong[Rationalism] takes this further, holding that
reasoning alone — carefully applied — can yield genuine understanding of the
world.

A second, deeper question follows naturally: how does the mind arise from a
physical brain? Two classical positions frame the debate. #strong[Dualism]
accepts that nature generally follows physical laws but carves out an exception:
some part of the human mind — traditionally called "the soul" — is held to be
exempt from those laws, operating in a realm physics cannot reach.
#strong[Materialism] rejects that exemption outright, treating the mind as a
physical system governed entirely by the laws of physics. If materialism is
correct, however, an uncomfortable puzzle surfaces: where is free will? The
materialist answer reframes the question rather than dismissing it — free will
is understood not as an escape from physical causation but as the perception of
available choices. When a system is complex enough to model its own options and
select among them, the subjective experience of "choosing freely" emerges, even
though every step in the process is, in principle, physically determined. This
reframing matters for AI because it suggests that building a system capable of
representing and evaluating alternatives may be sufficient for rational action,
without needing to solve the metaphysical puzzle of consciousness first.

// From: msml610/lectures_source/Lesson01.3-The_Foundations_of_AI.smd:50 '* AI and Philosophy (2/2)'
// Slide: AI and Philosophy (2/2)
#strong[AI and Philosophy (2/2)]

Where does knowledge come from? Philosophy offers at least three influential
answers. #emph[Empiricism] holds that knowledge is acquired through the senses:
we learn that trees are green by looking at them. #emph[Induction] goes a step
further, extracting general rules from repeated associations — observing many
white swans and inferring that all swans are white. #emph[Logical positivism]
refines the picture again, treating knowledge as a body of logical theories that
must be connected to observations: scientific hypotheses earn their status by
being linked to experimental data.

As @fig:blackswans reminds us, inductive reasoning is powerful but fallible —
the discovery of black swans in Australia famously overturned the long-standing
European generalisation that all swans are white, a canonical illustration of
the problem of induction.

#figure(
  image("../lectures_source/figures/L01.2.black_swans.jpg", width: 80%),
  caption: [black swans],
  kind: "figure",
  supplement: [Fig.],
  placement: auto,
) <fig:blackswans>

A separate but equally fundamental question is how knowledge, once obtained,
should lead to action. Two broad ethical frameworks compete here.
#emph[Consequentialism] judges whether an action is right or wrong by its
expected outcomes. Its classical form, #emph[utilitarianism], says that actions
are justified by the goals and outcomes they produce: a policy is judged by
whether it raises overall well-being, not by whatever rule it happens to follow.
#emph[Deontological ethics] takes the opposite stance, grounding right action in
universal laws rather than outcomes — prohibitions such as "don't kill" or
"don't lie" hold regardless of the consequences that breaking them might avert.
The tension between these two views resurfaces throughout AI, where an agent
must decide whether to optimise a utility function (a consequentialist design)
or to respect hard constraints that are never traded away (a deontological one).

// From: msml610/lectures_source/Lesson01.3-The_Foundations_of_AI.smd:85 '## Mathematics and Computation'
// Slide: Mathematics and Computation
== Mathematics and Computation

// From: msml610/lectures_source/Lesson01.3-The_Foundations_of_AI.smd:87 '* AI and Mathematics'
// Slide: AI and Mathematics
#strong[AI and Mathematics]

What are the formal rules for drawing valid conclusions? Two traditions address
this question from different angles. #strong[Formal logic], beginning with
Boole's logical deduction rules in 1847, provides a framework for deriving new
truths from existing ones through purely symbolic manipulation. Frege extended
this in 1879 with #strong[first-order logic], which introduced objects and
relations into the logical language, vastly increasing its expressive power. Yet
deduction has inherent limits: some statements are #emph[undecidable], meaning
no finite proof can establish their truth or falsity. Gödel's
#strong[incompleteness theorem] demonstrated in 1931 that in any sufficiently
rich formal theory, there exist true statements that cannot be proved within
that theory #cite("godel1931incompleteness"). This result placed a fundamental
boundary on what pure logical reasoning can accomplish.

How, then, do we reason when the available information is uncertain?
#strong[Probability] provides the mathematical language for quantifying
uncertainty, with foundations laid by Cardano, Pascal, Bernoulli, and Bayes
across the 1500s through the 1700s. #strong[Statistics] builds on probability by
combining it with observed data, giving us tools for experiment design, data
analysis, hypothesis testing, and the study of asymptotic behavior. Where logic
offers certainty within its domain, probability and statistics offer principled
ways to act and reason when certainty is unavailable — which, in practice, is
most of the time. Together, these traditions supply the formal backbone of
modern AI: logic for structured knowledge representation and deduction, and
probability theory for learning and decision-making under uncertainty.
@tab:aiandmathematics summarizes the key contributors and eras that shaped these
mathematical foundations.

#figure(
  styled-table(
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
  ),
  caption: [Table of Field, Key Contributors, Era],
  kind: "table",
  supplement: [Table.],
  placement: auto,
) <tab:aiandmathematics>

// From: msml610/lectures_source/Lesson01.3-The_Foundations_of_AI.smd:116 '* AI and Computer Science'
// Slide: AI and Computer Science
#strong[AI and Computer Science]

What can be computed? This deceptively simple question splits into three
distinct concerns: what an algorithm is, what the fundamental limits of
computation are, and which problems are practically solvable.

An #strong[algorithm] is a well-defined procedure for solving a class of
problems. The idea is ancient: Euclid described an algorithm for computing the
greatest common divisor of two integers around 300 BCE, and it remains one of
the most elegant examples of step-by-step problem solving. But not every
well-posed question has an algorithmic answer.

Some functions are simply #strong[non-computable]. In 1936, Alan Turing
introduced the #strong[Turing machine] #cite("turing1936computable"), a
mathematical model of computation that can compute any function that is
computable at all. This universality result also revealed hard boundaries:
certain problems provably have no algorithmic solution. The most famous example
is the #strong[halting problem] — given an arbitrary program and its input,
decide whether the program eventually terminates or runs forever. Turing proved
that no general algorithm can solve this for all possible programs, establishing
that computation has inherent limits regardless of how clever or powerful the
machine. As @fig:alanturing illustrates, Turing's contributions in the early
1950s laid the theoretical groundwork that still defines what we mean by
"computable" today.

#figure(
  image("../lectures_source/figures/L01.3.Alan_Turing.jpg", width: 80%),
  caption: [Alan Turing (1951)],
  kind: "figure",
  supplement: [Fig.],
  placement: auto,
) <fig:alanturing>

Even among problems that #emph[are] computable, not all are practically
solvable. #strong[Tractability] draws a line between problems whose solving time
grows polynomially with input size and those whose time grows exponentially. A
problem is called #strong[intractable] if the best known algorithm requires
exponential time, meaning that even moderate increases in input size render it
unsolvable in any reasonable timeframe. This distinction is formalized by
complexity classes: #strong[P] contains problems solvable in polynomial time,
while #strong[NP] contains problems whose solutions can be #emph[verified] in
polynomial time but may require exponential time to #emph[find]. Whether P
equals NP — whether every problem whose solution is easy to check is also easy
to solve — remains one of the deepest open questions in computer science and
mathematics. For AI, this matters directly: many planning, reasoning, and
optimization tasks fall into NP or harder classes, so practical AI systems must
often settle for approximate or heuristic solutions rather than exact ones.

// From: msml610/lectures_source/Lesson01.3-The_Foundations_of_AI.smd:144 '## Economics'
// Slide: Economics
== Economics

// From: msml610/lectures_source/Lesson01.3-The_Foundations_of_AI.smd:146 '* AI and Economics (1/2)'
// Slide: AI and Economics (1/2)
#strong[AI and Economics (1/2)]

How should an agent make decisions to maximize its payoff given its preferences?
Two traditions address this question from complementary angles. In
#strong[economics], agents are modeled as maximizers of their own well-being —
formally captured by a #strong[utility] function — and the field studies the
structure of desires and preferences that make such maximization coherent.
#strong[Decision theory] sharpens this picture by combining probability theory
with utility theory, providing a calculus for choosing among alternatives when
outcomes are uncertain. Everyday examples include selecting an investment
portfolio under market risk or evaluating competing policy proposals whose
consequences depend on factors outside anyone's control.

A harder question arises when payoffs depend not on a single choice but on a
#strong[sequence of actions]. #strong[Operations research] tackles exactly this
setting: finding rational plans whose value accumulates over multiple steps. A
landmark formalization is the #strong[Markov Decision Process] (MDP), introduced
by Bellman #cite("bellman1957dp"), which decomposes a sequential problem into
stages so that an optimal policy can be computed recursively. Not every real
decision-maker, however, hunts for the global optimum. Herbert Simon's concept
of #strong[satisficing] #cite("simon1956satisficing") captures the observation
that humans — and many practical systems — settle for outcomes that are "good
enough" rather than provably best. Choosing a restaurant that meets basic
criteria for price, distance, and cuisine instead of exhaustively ranking every
option in the city is a canonical example. Satisficing trades optimality for
tractability and is often closer to actual human behavior than the idealized
utility maximizer of classical theory.

As @fig:aiandeconomics12 illustrates, decision theory sits at the intersection
of probability theory and utility theory: probability theory supplies beliefs
about the world, utility theory encodes preferences over outcomes, and their
combination yields a principled framework for action under uncertainty.

#figure(
  image("Lesson01.3-The_Foundations_of_AI.typ.figs/Lesson01.3-The_Foundations_of_AI.2.png", width: 60%),
  caption: [Diagram relating Probability Theory, Utility Theory and Decision Theory],
  kind: "figure",
  supplement: [Fig.],
  placement: auto,
) <fig:aiandeconomics12>

// From: msml610/lectures_source/Lesson01.3-The_Foundations_of_AI.smd:203 '* AI and Economics (2/2)'
// Slide: AI and Economics (2/2)
#strong[AI and Economics (2/2)]

How do multiple agents with different goals act in a shared environment? The
answer depends critically on how much influence each agent's decisions exert on
the others. In #strong[large economies], there are so many participants that no
single agent's choice measurably affects anyone else's outcome. A individual
consumer in a national economy, for instance, can safely ignore what every other
consumer is doing, because their purchases have negligible impact on market
prices. Each agent optimizes independently, as though the others were simply
part of the background environment.

#strong[Small economies] present a fundamentally different challenge. When the
number of participants is limited, one player's actions directly influence the
utility of the others. Consider a local market with only a handful of sellers:
if one aggressively cuts prices, the competitors immediately feel the impact on
their own revenue. Agents in this setting cannot plan in isolation; they must
anticipate and respond to what others will do.

This interdependence is precisely the domain of #strong[game theory], the
framework formalized by von Neumann and Morgenstern in 1944 #cite(
  "vonneumann1944gametheory",
), which models small economies as strategic #emph[games]. One of the most
striking insights from game theory is that rational agents may need to adopt
#strong[randomized (mixed) strategies] rather than deterministic ones.
Rock-paper-scissors illustrates why: any fixed, predictable choice is
immediately exploitable by an opponent who observes the pattern, so the only
unexploitable strategy is to choose uniformly at random. More generally,
whenever an agent's best action depends on what others choose, and vice versa,
deterministic play can be self-defeating, and introducing controlled randomness
becomes the rational response.

@tab:aiandeconomics22 summarizes how these three regimes differ along key
dimensions, from the degree of mutual influence among agents to the type of
strategy each regime demands.

#figure(
  styled-table(
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
  ),
  caption: [Table of Aspect, Large Economies, Small Economies, Game Theory],
  kind: "table",
  supplement: [Table.],
  placement: auto,
) <tab:aiandeconomics22>

// From: msml610/lectures_source/Lesson01.3-The_Foundations_of_AI.smd:230 '## Neuroscience and Psychology'
// Slide: Neuroscience and Psychology
== Neuroscience and Psychology

// From: msml610/lectures_source/Lesson01.3-The_Foundations_of_AI.smd:232 '* AI and Neuroscience'
// Slide: AI and Neuroscience
#strong[AI and Neuroscience]

The #strong[brain] is fundamentally an information-processing organ, with
different regions handling specific cognitive functions. Much of this processing
occurs in the cerebral cortex, and damage to particular areas produces
predictable deficits — a frontal lobe injury, for instance, may impair
decision-making while leaving perception largely intact. This localization of
function was one of the earliest clues that cognition is not a single
indivisible process but a collection of specialized subsystems, as illustrated
in @fig:brain.

#figure(
  image("../lectures_source/figures/L01.2.brain.jpg", width: 80%),
  caption: [brain],
  kind: "figure",
  supplement: [Fig.],
  placement: auto,
) <fig:brain>

At the hardware level, the brain is composed of roughly 100 billion neurons.
Each neuron forms between 10,000 and 100,000 synaptic connections to other
neurons, and axons enable these connections to span long distances across the
brain. Signals propagate through electrochemical reactions: a neuron integrates
incoming electrical impulses and, if a threshold is reached, fires its own
signal down the axon to downstream neighbors. @fig:neuron shows the basic
anatomy of a single neuron, including the dendrites that receive input, the cell
body that integrates it, and the axon that transmits the output signal.

#figure(
  image("../lectures_source/figures/L01.2.neuron.png", width: 80%),
  caption: [neuron],
  kind: "figure",
  supplement: [Fig.],
  placement: auto,
) <fig:neuron>

What makes this network more than a fixed circuit is its capacity for change.
Short-term signaling pathways can be strengthened or weakened over time, and
these modifications support long-term connections — the physical basis of
learning. Repeated activation of a particular pathway makes future activation
easier, a principle often summarized as "neurons that fire together wire
together."

Memory remains one of the less well-understood aspects of this system. There is
no established theory explaining how an individual memory is stored at the level
of specific neurons or synapses. The prevailing view is that memories are not
filed away like entries in a database but are #strong[reconstructed] each time
they are recalled, assembled from distributed patterns of neural activity. This
reconstructive nature helps explain why memories are malleable — prone to
distortion, blending, and revision — rather than faithful recordings of past
experience.

// From: msml610/lectures_source/Lesson01.3-The_Foundations_of_AI.smd:262 '* The Brain Causes the Mind'
// Slide: The Brain Causes the Mind
#strong[The Brain Causes the Mind]

It is truly remarkable that simple cells — neurons firing in electrochemical
patterns — give rise to thought, perception, and consciousness. Complex
cognitive processes emerge from the interaction of billions of individually
simple components, a fact that both inspires and humbles AI researchers trying
to replicate even a fraction of that capability.

Modern supercomputers can exceed the brain in raw computational throughput, yet
they still lack its flexibility, learning speed, and energy efficiency. The
human brain operates on roughly 20 watts of power while orchestrating language,
vision, motor control, and abstract reasoning simultaneously — a feat no
engineered system has come close to matching on a watt-for-watt basis.

Consider brain-machine interfaces as a striking illustration of the brain's
adaptability. When a person is fitted with a neural prosthetic, the brain
gradually adjusts its own signals to operate the device, effectively learning to
treat an artificial limb as part of the body. This plasticity — the capacity to
reorganise itself around entirely new inputs and outputs — is something current
AI systems cannot replicate without extensive retraining from scratch.

The #strong[AI singularity] refers to a hypothetical future point at which
artificial intelligence surpasses human intelligence and begins improving itself
autonomously, triggering a rapid, runaway growth in capability. The core
mechanism is #strong[recursive self-improvement]: an AI system redesigns its own
architecture or training process, each improvement making the next one easier
and faster, ultimately producing a superintelligence that far exceeds any human
cognitive ability #cite("good1965ultraintelligent"). As
@fig:thebraincausesthemind illustrates, this feedback loop — where an AI system
improves itself, its capability increases, and that increased capability feeds
back into further self-improvement — is what makes the singularity scenario
qualitatively different from ordinary technological progress.

The prospect raises urgent questions. The #strong[control problem], sometimes
called #strong[value alignment], asks how we can ensure that a recursively
self-improving system continues to pursue goals compatible with human welfare
rather than drifting toward objectives we never intended. Beyond alignment,
large-scale automation driven by superintelligent systems could reshape
economies and social structures in ways that are difficult to predict or manage.
Yet for all the speculation, achieving even the brain's baseline level of
general intelligence remains an open problem — no one knows whether current
paradigms of deep learning, symbolic reasoning, or some yet-undiscovered
approach will be the one to close the gap.

#figure(
  image("Lesson01.3-The_Foundations_of_AI.typ.figs/Lesson01.3-The_Foundations_of_AI.3.png", width: 90%),
  caption: [Diagram relating AI System, Improves Itself, Capability Increases and Superintelligence],
  kind: "figure",
  supplement: [Fig.],
  placement: auto,
) <fig:thebraincausesthemind>

// From: msml610/lectures_source/Lesson01.3-The_Foundations_of_AI.smd:322 '* AI and Cognitive Psychology'
// Slide: AI and Cognitive Psychology
#strong[AI and Cognitive Psychology]

How do humans think and act? This question sits at the intersection of several
disciplines, each offering a distinct but complementary lens on the machinery of
the mind.

#strong[Cognitive psychology] treats the brain as an information-processing
device. External stimuli are first translated into an internal representation, a
structured encoding of what has been perceived. Cognitive processes then
manipulate that representation to derive new internal representations, commonly
called #emph[beliefs]. Finally, those beliefs are translated back into actions
directed at #emph[goals]. The pipeline, stimulus → representation → belief →
action, mirrors the sense–think–act loop that appears throughout AI agent
design, and it is no coincidence: early AI researchers drew heavily on this
model when building their first systems. @fig:aiandcognitivepsychology
illustrates this flow, showing how stimuli enter the system, pass through
internal representations and cognitive processes, and ultimately produce beliefs
that guide behaviour.

#figure(
  image("Lesson01.3-The_Foundations_of_AI.typ.figs/Lesson01.3-The_Foundations_of_AI.4.png", width: 100%),
  caption: [Diagram relating Stimuli, Internal Representation, Cognitive Processes and Beliefs],
  kind: "figure",
  supplement: [Fig.],
  placement: auto,
) <fig:aiandcognitivepsychology>

#strong[Cognitive science] pushes this analogy further by using computer models
as explanatory tools for human cognition. Rather than simply claiming the brain
"is like" a computer, cognitive scientists build working programs that address
memory, language, and logical reasoning, then compare the programs' behaviour
with experimental data from human subjects. This makes cognitive science a close
cousin of AI, not its opposite: the two fields share formal methods and often
the same research questions, differing mainly in whether the goal is to
#emph[explain] human intelligence or to #emph[engineer] it.

#strong[Human-computer interaction] (HCI) reframes the relationship in yet
another way. Instead of asking whether machines can replicate human thought, HCI
asks how computers can #emph[augment] human abilities. This perspective shifts
the conversation from #emph[artificial intelligence] to what Douglas Engelbart
called #emph[intelligence augmentation]: designing systems that extend
perception, memory, and reasoning rather than replacing them. The distinction
matters practically because many of the most successful deployed systems today,
from search engines to decision-support dashboards, work #emph[with] human
operators rather than in place of them.

Taken together, these three perspectives form a useful triangle. Cognitive
psychology supplies the theoretical model of human information processing,
cognitive science tests that model computationally, and HCI applies the
resulting insights to build tools that make people more effective. AI sits at
the centre of all three, borrowing models from the first, sharing methods with
the second, and delivering technology to the third.

// From: msml610/lectures_source/Lesson01.3-The_Foundations_of_AI.smd:378 '## Engineering, Control, and Language'
// Slide: Engineering, Control, and Language
== Engineering, Control, and Language

// From: msml610/lectures_source/Lesson01.3-The_Foundations_of_AI.smd:380 '* AI and Computer Engineering (1/2)'
// Slide: AI and Computer Engineering (1/2)
#strong[AI and Computer Engineering (1/2)]

How has computing hardware evolved to become fast enough for AI? The story
begins during World War II, when the first #strong[electronic computers] were
built — room-sized machines such as ENIAC, shown in @fig:eniac, which were
designed primarily for ballistics calculations but demonstrated that large-scale
automated computation was physically feasible.

#figure(
  image("../lectures_source/figures/L01.2.eniac.png", width: 80%),
  caption: [eniac],
  kind: "figure",
  supplement: [Fig.],
  placement: auto,
) <fig:eniac>

From that point forward, hardware improved at a breathtaking pace. In 1965,
Gordon Moore observed that the number of transistors on an integrated circuit
was doubling roughly every eighteen months, an empirical trend that held
remarkably steady from about 1970 through 2005 #cite("moore1965cramming"). This
pattern, known as #strong[Moore's Law], meant that each new generation of
processors could handle substantially larger problems — and AI workloads, which
are notoriously compute-hungry, benefited directly. @fig:moorelaw illustrates
this exponential trajectory across several decades of processor development.

#figure(
  image("../lectures_source/figures/L01.2.Moore_Law.png", width: 80%),
  caption: [Moore Law],
  kind: "figure",
  supplement: [Fig.],
  placement: auto,
) <fig:moorelaw>

Around 2005, however, raw clock-speed scaling hit a wall. Power dissipation and
heat constraints made it impractical to keep pushing single-core frequencies
higher, so chip designers pivoted to #strong[multi-core] architectures: instead
of one faster core, processors offered two, four, or more cores running in
parallel. For AI this shift turned out to be fortuitous. Many machine-learning
algorithms — matrix multiplications in neural networks, parallel sampling in
probabilistic models, batch processing of training data — decompose naturally
into independent sub-tasks that map well onto multiple cores and, eventually,
onto the massively parallel architectures of modern GPUs and TPUs. The hardware
did not simply get faster in a straight line; it changed shape in a way that
happened to align with the computational structure of modern AI.

// From: msml610/lectures_source/Lesson01.3-The_Foundations_of_AI.smd:402 '* AI and Computer Engineering (2/2)'
// Slide: AI and Computer Engineering (2/2)
#strong[AI and Computer Engineering (2/2)]

What hardware trends are shaping AI systems today? The answer begins with three
families of processors that have come to define modern AI infrastructure.
#strong[Hardware for AI] today centers on GPUs (graphics processing units,
repurposed for massively parallel numerical work), TPUs (tensor processing
units, custom-designed by Google specifically for machine-learning workloads),
and wafer-scale engines such as those built by Cerebras, which dedicate an
entire silicon wafer to a single, enormous processor.

Several characteristics of these platforms stand out. First, they all exploit
#strong[massive parallelism], an architectural principle loosely analogous to
the brain's own strategy of coordinating billions of relatively slow neurons
rather than relying on a single fast serial processor. Second, the pace of
improvement has been staggering: the compute budget used in the largest AI
training runs has doubled roughly every three to four months since 2012, far
outstripping the roughly two-year doubling cadence of Moore's Law. This
acceleration does not come from silicon shrinks alone; it combines more chips,
better chips, and dramatically higher spending. Third, deep-learning workloads
lean heavily on GPUs and TPUs because these devices are optimized for the dense
matrix multiplications that dominate neural-network training. Fourth, high
numerical precision turns out to be largely unnecessary for deep learning:
64-bit floating-point arithmetic, the gold standard in scientific computing, can
often be replaced by 16-bit or even 8-bit formats with negligible loss in model
quality, which in turn doubles or quadruples the effective throughput of every
chip. @fig:cpugputpu illustrates the architectural differences among CPUs, GPUs,
and TPUs, highlighting how each successive design trades away general-purpose
flexibility for raw parallel arithmetic density.

#figure(
  image("../lectures_source/figures/L01.2.CPU_GPU_TPU.png", width: 80%),
  caption: [CPU GPU TPU],
  kind: "figure",
  supplement: [Fig.],
  placement: auto,
) <fig:cpugputpu>

Looking further ahead, #strong[quantum computing] has the potential for
significant acceleration in key computational tasks that remain intractable on
classical hardware. A canonical example is Shor's algorithm for integer
factorization #cite("shor1997factoring"), which can factor large numbers in
polynomial time on a quantum computer, a task for which no efficient classical
algorithm is known. While practical, fault-tolerant quantum machines at the
scale needed for general AI workloads remain an active area of research, the
trajectory suggests that quantum resources could eventually complement classical
accelerators for specific sub-problems inside larger AI pipelines.

// From: msml610/lectures_source/Lesson01.3-The_Foundations_of_AI.smd:434 '* AI and Control Theory'
// Slide: AI and Control Theory
#strong[AI and Control Theory]

How can artifacts operate under their own control? This question sits at the
heart of #strong[control theory], the study of self-regulating feedback control
systems. A classic example is a water regulator that maintains a constant flow
rate: the system continuously measures the actual flow, compares it to the
desired setpoint, and adjusts a valve to close the gap. More generally, control
theory provides mechanisms to minimize the error between a system's current
state and its goal state, driving the system toward the target through repeated
corrective action.

A landmark contribution in this tradition is the #strong[Kalman filter] #cite(
  "kalman1960filtering",
), which provides an optimal way to estimate the hidden state of a noisy,
dynamic system by combining predictions from a mathematical model with incoming
sensor measurements. The mathematical foundations of control theory rest on
calculus, matrix algebra, and stochastic optimal control, giving engineers
precise, well-characterized tools for designing controllers with provable
stability and performance guarantees.

As @fig:aiandcontroltheory illustrates, the feedback loop connecting a goal
state, a controller, a system, and the current state captures the essential
architecture shared by classical control and AI planning alike. Where the two
fields diverge is in the nature of their internal representations and reasoning
mechanisms. Classical control operates over continuous signals and differential
equations, whereas AI brings logical inference, symbolic planning, and
general-purpose computation to bear on the same high-level problem: steering a
system from where it is to where it should be. This difference matters most when
the environment is complex, partially observable, or requires discrete decisions
among qualitatively different actions, situations where symbolic reasoning
complements, and sometimes surpasses, the continuous optimization perspective of
traditional control.

#figure(
  image("Lesson01.3-The_Foundations_of_AI.typ.figs/Lesson01.3-The_Foundations_of_AI.5.png", width: 90%),
  caption: [Diagram relating Goal State, Controller, System and Current State],
  kind: "figure",
  supplement: [Fig.],
  placement: auto,
) <fig:aiandcontroltheory>

// From: msml610/lectures_source/Lesson01.3-The_Foundations_of_AI.smd:482 '* AI and Linguistics'
// Slide: AI and Linguistics
#strong[AI and Linguistics]

How can we create systems that understand natural language? This challenge falls
under #strong[computational linguistics], which studies sentence structure and
meaning to enable machines to process human language. Its applications are
already widespread: machine translation systems such as Google Translate convert
text between languages, sentiment analysis tools mine opinions from social
media, and automated chatbots handle customer support interactions at scale.

A deeper question follows naturally: how does language relate to thought? To
bridge that gap, #strong[knowledge representation] studies how to encode
knowledge in forms that computers can reason over. Formalisms such as
first-order logic let a system draw inferences from stated facts, while
knowledge graphs capture rich webs of relationships between entities, giving a
machine something closer to a structured understanding of the world rather than
a mere string of words. As @fig:aiandlinguistics illustrates, computational
linguistics and knowledge representation sit at the intersection of natural
language understanding and machine reasoning, with machine translation serving
as a concrete application that draws on both.

#figure(
  image("Lesson01.3-The_Foundations_of_AI.typ.figs/Lesson01.3-The_Foundations_of_AI.6.png", width: 80%),
  caption: [Diagram relating Natural Language, Computational Linguistics, Knowledge Representation and Machine Translation],
  kind: "figure",
  supplement: [Fig.],
  placement: auto,
) <fig:aiandlinguistics>

// From: msml610/lectures_source/Lesson01.3-The_Foundations_of_AI.smd:540 '## Wrap-Up'
// Slide: Wrap-Up
== Wrap-Up

// From: msml610/lectures_source/Lesson01.3-The_Foundations_of_AI.smd:542 '* Key Takeaways'
// Slide: Key Takeaways
#strong[Key Takeaways]

AI did not spring from a single discipline. Its core questions, formalisms, and
tools were inherited from a remarkably broad constellation of fields:
philosophy, mathematics, economics, neuroscience, psychology, computer science
and engineering, control theory, and linguistics. Each contributed something
essential — philosophy posed the questions of whether machines can reason and
whether mind reduces to physical process; mathematics supplied logic,
probability, and computation theory; economics formalized rational choice under
uncertainty; neuroscience and psychology offered models of how biological agents
actually perceive, learn, and decide; computer science and engineering provided
the substrates on which these ideas could be realized; control theory introduced
feedback and optimization in dynamic environments; and linguistics tackled the
structure of language and meaning that any intelligent communicator must
command.

Many of the foundational questions these fields raised — #emph[Can machines
  reason? Does the mind reduce to physics? How should a rational agent act under
  uncertainty?] — remain genuinely open. They are not historical curiosities but
live research problems that continue to shape how AI systems are designed,
evaluated, and critiqued today. The interdisciplinary character of AI is
therefore not merely a fact about its origins; it is a persistent feature of the
field itself, one that makes progress dependent on advances across multiple
fronts simultaneously.

// From: msml610/lectures_source/Lesson01.3-The_Foundations_of_AI.smd:553 '* References'
// Slide: References
#strong[References]


#set text(size: 0.75em)
#references("/msml610/lectures_source/refs.bib")
