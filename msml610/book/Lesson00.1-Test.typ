// git_hash=918a6541e-i5t timestamp=20260830_174545
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

#chapter(00, "L01.2: AI and Machine Learning")

// From: msml610/lectures_source/Lesson00.1-Test.smd:10 '# AI and Machine Learning'
// Slide: AI and Machine Learning
#strong[AI and Machine Learning]

// From: msml610/lectures_source/Lesson00.1-Test.smd:12 '## What Is AI?'
// Slide: What Is AI?
== What Is AI?

// From: msml610/lectures_source/Lesson00.1-Test.smd:14 '* ML, AI, and Intelligence'
// Slide: ML, AI, and Intelligence
#strong[ML, AI, and Intelligence]

#strong[Machine learning] is a subset of artificial intelligence (AI). Although
the term is frequently conflated with deep learning, large-language models,
predictive analytics, and other neighboring fields, it is worth drawing careful
boundaries: machine learning refers specifically to algorithms that improve
their performance on a task through experience, without being explicitly
programmed for every contingency.

What is artificial intelligence? Answering that question starts with
understanding what #strong[human intelligence] is — because AI, at its core, is
an attempt to replicate or approximate capabilities we first observed in
ourselves.

What, then, is human intelligence? We call ourselves #emph[homo sapiens] — "wise
humans" — precisely because intelligence is the trait we believe sets us apart
from other animals. For thousands of years, philosophers, scientists, and
theologians have tried to understand how we think, and the question remains one
of the biggest mysteries in science. The human brain is a remarkably small piece
of biological matter, yet it has managed to grasp some of nature's deepest
secrets: the theory of relativity, quantum mechanics, the physics of black
holes. How can a three-pound organ understand, predict, and even manipulate a
world far more complex than itself? That puzzle — how a system can model
something larger and more intricate than its own substrate — is not merely
philosophical; it sits at the heart of why building artificial intelligence is
so challenging and so fascinating.

// From: msml610/lectures_source/Lesson00.1-Test.smd:33 '* Artificial Intelligence'
// Slide: Artificial Intelligence
#strong[Artificial Intelligence]

#grid(
  columns: (80%, 20%),
  gutter: 1em,
  [
    The term #strong[Artificial Intelligence] was coined in 1956 #cite(
      "mccarthy1955dartmouth",
    ), marking the formal birth of a field whose ambitions remain remarkably
    broad. At its core, AI pursues two intertwined goals: understanding human
    intelligence and building entities that exhibit intelligent behavior.
    Richard Feynman's dictum — "What I cannot create, I do not understand" —
    captures the spirit well: constructing an intelligent system is itself a
    path toward deeper comprehension of what intelligence means.

    AI is not confined to a narrow technical niche. It applies, in principle, to
    any activity or task that humans perform — from recognizing faces and
    translating languages to diagnosing diseases and proving theorems. In sheer
    scope of potential impact, the field arguably exceeds any single event in
    recorded history. It already generates hundreds of billions of dollars in
    annual market revenue, and projections place its cumulative global economic
    impact in the trillions by 2030 #cite("bughin2018aifrontier").

    Yet for all its momentum, AI remains a discipline with many open questions.
    Unlike arithmetic, whose foundations were settled millennia ago, or
    Newtonian mechanics, which is essentially complete within its domain of
    validity, AI has no settled core theory that everyone agrees on. Fundamental
    debates — what the right learning paradigm is, how to represent knowledge,
    whether current approaches can ever reach general intelligence — are very
    much alive. That combination of extraordinary practical success and deep
    theoretical uncertainty is part of what makes the field so compelling to
    study.
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
