Modify the script llm_cli.py to accept a parameter rule
--rule or -r (instead of -p and -pf)
that extracts the part of the rules in .claude and then
uses that to call the LLM as prompt

Apply only 
--rule '.claude/skills/slides.rules.md:58:# Slide Organization'
--rule '.claude/skills/slides.rules.md:58'

Apply all the rules in the file
--rule '.claude/skills/slides.rules.md'

- If the task is not perfectly clear, you MUST not perform it, but ask for
  clarifications

- When writing code you must always follow the instructions in
  `@.claude/skills/coding.rules.md`

- Generate unit tests for the new code following the instructions in
  `@.claude/skills/testing.rules.md`
