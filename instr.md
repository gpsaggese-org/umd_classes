In linters2/cc_lint.py 

1) Add a switch --add_todos so that instead of modifying the file
the action is to add comments in the right place like
```
# TODO(ai_gp): Do this and that (link to the rule)

E.g.,
# TODO(ai_gp): Do this and that (testing.rules.md:1081:## Use Context Manager Syntax for Multiple Mocks)
```

2) Rename the current --mode one_shot to --one_shot_with_cc

3) Add another --mode one_shot to make a single call to the PromptSequencer
   (in practice this is equivalent to the --one_shot_with_cc, but instead of
   calling cc through a system call, uses the PromptSequencer)

# Conventions
- When writing code you must always follow the instructions in
  `.claude/skills/coding.rules.md`
- When writing testing code you must always follow the instructions in
  `.claude/skills/testing.rules.md`

# Create a plan, if needed
- If the task is not perfectly clear
  - You MUST not perform it
  - Ask for clarifications
  - Create a `plan.md` in the same directory with 5 bullet points explaining what
    the plan is
