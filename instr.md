- Implement unit tests for process_jupytext.py following
  .claude/skills/testing.rules.md:704:# End-to-end Unit Tests for Executables

## Run Command Instead of Calling its Main
- Do not inject (`sys.argv = ["process_jupytext.py"] + args_list`)
  and call the main of the script (e.g., `_main(parser)`)
  - Instead call the executable directly with a call like `hsystem.system()`

- If the task is not perfectly clear, you MUST not perform it, but ask for
  clarifications

- When writing code you must always follow the instructions in
  `.claude/skills/coding.rules.md`
- When writing a notebook follow `.claude/skills/notebook.rules.md`
