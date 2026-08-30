Fix run_typst.py --input msml610/book/Lesson01.2-AI_and_Machine_Learning.typ --output msml610/book/Lesson01.2-AI_and_Machine_Learning.pdf --skip_action open_pdf which now it's returning error: label `<fig:2aiasthinkingrationally>` does not exist in the document
    ┌─ msml610/book/Lesson01.2-AI_and_Machine_Learning.typ:208:3
    │
208 │ As @fig:2aiasthinkingrationally illustrates, the relationship is
    │    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^

error: label `<fig:aivsmlvsdeeplearning>` does not exist in the document
    ┌─ msml610/book/Lesson01.2-AI_and_Machine_Learning.typ:639:3
    │
639 │ As @fig:aivsmlvsdeeplearning illustrates, these categories nest concentrically —
    │    ^^^^^^^^^^^^^^^^^^^^^^^^^ 

1) Why is the script 
gen_book_chapter.py  msml610/01.2 --mode typst_aima --llm_backend hllm_cli_exec --model openrouter/anthropic/claude-opus-4.6

generating a broken typst file?

Debug and propose a fix

2) Propse a fix for run_typst to not abort on errors

3) Fix the file msml610/book/Lesson01.2-AI_and_Machine_Learning.typ so that it
   compiles
