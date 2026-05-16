- Write a Python script class_scripts/count_pdf_pages.py similar to
  class_scripts/count_lecture_slides.py that given a dir, for each lecture
  like msml610/lectures_source/Lesson01.1-AI_and_Machine_Learning.txt

  - counts all the slides
  grep "^* " <file>

  - counts all the headers of different level
  grep "^# " <file>
  grep "^## " <file>
  grep "^### " <file>

extract_toc_from_txt.py -i msml610/lectures_source/Lesson01.1-AI_and_Machine_Learning.txt --max_level 5 --warn_on_malformed

  - count the lines, words, characters in
  wc  msml610/lectures_source/Lesson01.1-AI_and_Machine_Learning.txt
  375    1684   12000 msml610/lectures_source/Lesson01.1-AI_and_Machine_Learning.txt

- Read class_scripts/README.md

- Reuse the functions in
  > ls class_scripts/*utils*
  class_scripts/common_utils.py          class_scripts/gen_slides_test_utils.py

- Report the results in a table using tabulate like
  <file>   <num_slides>   <num_words>    <num_lines>
  
- The interface is like:
  ...

- If the task is not perfectly clear, you MUST not perform it, but ask for
  clarifications
  - When the task is complex, create a plan.md with 5 bullet points explaining
    what the plan is

- When writing code you must always follow the instructions in
  `@.claude/skills/coding.rules.md`

- Generate unit tests for the new code following the instructions in
  `@.claude/skills/testing.rules.md`
