Create a script lesson/for_loop_slides.py

--input ./msml610/lectures_source/Lesson10.2-Causal_Discovery.txt
--prompt rule.md

that reads the input slides with hmarkdown_slide_iterator and transform each
slide with hllm_cli.py using _process_batches from hllm_cli.py

- If the task is not perfectly clear, you MUST not perform it, but ask for
  clarifications

- When writing code you must always follow the instructions in
  `@.claude/skills/coding.rules.md`

- Generate unit tests for the new code following the instructions in
  `@.claude/skills/testing.rules.md`
