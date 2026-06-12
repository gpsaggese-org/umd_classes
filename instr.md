Improve the output of jupytext.py by making it less verbose at INFO level

This

08:54:31 - WARN  hsystem.py remove_dirs:491                             Removed dirs: helpers_root

should be at DEBUG level

Also add a tqdm progress bar to show the progress 

- When writing code you must always follow the instructions in
  `.claude/skills/coding.rules.md`

- When writing unit tests for follow the instructions in
  `.claude/skills/testing.rules.md`

- If the task is not perfectly clear, you MUST not perform it, but ask for
  clarifications
  - When the task is complex, create a `plan.md` with 5 bullet points explaining
    what the plan is

