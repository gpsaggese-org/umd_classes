Change the typst template so that

1) When running

run_typst.py --input msml610/book/Lesson01.2-AI_and_Machine_Learning.typ

I want to allow a macro

#chapter("L01.2: AI and Machine Learning")

so that instead of "Chapter 1" in the purple bar, I get "L01.2: AI and Machine Learning"

error: invalid integer: L01.2
   ┌─ helpers_root/dev_scripts_helpers/typst/aima_style.typ:83:31
   │
83 │   counter(heading).update((int(num),))
   │                                ^^^

help: error occurred in this call of function `chapter`
   ┌─ msml610/book/Lesson01.2-AI_and_Machine_Learning.typ:20:1
   │
20 │ #chapter("L01.2: AI and Machine Learning")
   │  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

2) A subchapter like

= What Is Intelligence? What is AI?

should have the format that now == has (i.e., purple with the line)

Make the font bigger

Move the line closer to the text

3) A subchapter like

== ML, AI, and Intelligence

should have a lighter color and no line

4) Remove the empty page at the very beginning

