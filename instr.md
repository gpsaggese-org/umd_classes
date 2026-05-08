Extend extract_text_from_txt.py to accept also a slide
(e.g., `* Conditionally Random Experiments`)

Extend llm_transform.py to accept a txt / md file and a --slide_name "Conditionally Random Experiments"

Look for the slide content (e.g,.

Extract the text until the next slide or markdown header #, ##

Then apply the transform based on the prompt and update the content
or print the output depending on the prompt

- When writing code you must always follow the instructions in
  `@.claude/skills/coding.rules.md`

- Generate unit tests for the new code following the instructions in
  `@.claude/skills/testing.rules.md`
