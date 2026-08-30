// git_hash=454afea6c-tny timestamp=20260830_180501
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

#strong[Machine Learning] is a subset of Artificial Intelligence (AI). Although
the term is widely used, it is often confused with related but distinct fields
such as #emph[deep learning], #emph[large-language models], and #emph[predictive
  analytics]. Each of these represents a different slice of the broader AI
landscape, and understanding where machine learning fits requires first stepping
back to ask a more fundamental question.

What is artificial intelligence? Answering that starts with understanding what
#strong[human intelligence] is. After all, much of AI research draws inspiration
— directly or indirectly — from the capacities of the human mind.

What, then, is human intelligence? We call ourselves #emph["homo sapiens"] —
"wise humans" — precisely because intelligence is the trait we believe sets us
apart from other animals. For thousands of years, philosophers, scientists, and
theologians have tried to understand how we think, and the question remains one
of the #emph[biggest mysteries] we face. The human brain is a remarkably small
piece of matter, roughly 1.4 kilograms on average, yet it is capable of grasping
nature's deepest secrets: the theory of relativity, quantum mechanics, the
physics of black holes. This raises a profound puzzle: how can the brain
understand, predict, and even manipulate a world that is vastly more complex
than itself? Any serious attempt to build artificial intelligence must at least
grapple with this question, even if the engineering path ultimately diverges
from the biological one.

// From: msml610/lectures_source/Lesson00.1-Test.smd:33 '* Artificial Intelligence'
// Slide: Artificial Intelligence
#strong[Artificial Intelligence]

The term #strong[Artificial Intelligence] was coined in 1956 #cite(
  "mccarthy1955dartmouth",
), marking the formal birth of a field whose ambitions remain breathtaking: to
understand human intelligence and, ultimately, to create intelligent entities.
Richard Feynman's famous dictum — "What I cannot create, I do not understand" —
captures the dual nature of the enterprise. Building an intelligent system is
not merely an engineering goal; it is a way of testing whether we truly grasp
the principles that make intelligence possible in the first place.

What sets AI apart from most scientific disciplines is the sheer breadth of its
scope. It applies, in principle, to any human activity and any task a person can
perform — from diagnosing diseases to composing music, from driving a car to
proving mathematical theorems. That universality gives the field an economic
footprint to match: AI already generates hundreds of billions of dollars
annually in market revenue, with projections placing its global economic impact
in the trillions by 2030 #cite("bughin2018aifrontier"). Many observers argue
that its long-term societal impact will exceed that of any past historical
event, including the Industrial Revolution and the advent of the internet.

At the same time, AI remains a discipline with many unresolved problems. This
distinguishes it sharply from fields that possess settled core theories —
arithmetic rests on axioms that have been stable for millennia, and Newtonian
mechanics delivers exact predictions within its domain. AI has no comparable
bedrock. Fundamental questions about representation, learning, reasoning under
uncertainty, and the nature of general intelligence are still actively debated,
and new sub-problems surface as quickly as old ones are partially solved. That
openness is part of what makes the field both exciting and challenging for
newcomers: there is no single textbook derivation you can memorize and be done
with.

#figure(
  image("../lectures_source/figures/L01.2.Richard_Feynman.jpg", width: 80%),
  caption: [Richard Feynman (1965)],
  kind: "figure",
  supplement: [Fig.],
  placement: auto,
) <fig:richardfeynman>
