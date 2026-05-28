the --select mode with a start pattern (without a :
range specifier) currently extracts to the end of the file instead of stopping at
the next paragraph with the same heading level.

Instead When --select <start> without a : it should stop at the next paragraph with the same level

--select should consider the text until the end only if it's like <start>:END

Update the documentation and the docstrings

- When writing code you must always follow the instructions in
  `.claude/skills/coding.rules.md`

- When writing unit tests for follow the instructions in
  `.claude/skills/testing.rules.md`

- When implementing notebooks follow the instructions in
  `.claude/skills/notebook.rules.md`

- If the task is not perfectly clear, you MUST not perform it, but ask for
  clarifications
  - When the task is complex, create a `plan.md` with 5 bullet points explaining
    what the plan is
