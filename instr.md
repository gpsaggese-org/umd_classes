- Update running notes_to_pdf.py so that instead of running pandoc in one shot
  create the AST and then convert it to the proper

- For example
  > pandoc input.md -t json -o ast.json
  > pandoc ast.json -f json -t typst -o out.typ

# Conventions
- When writing code you must always follow the instructions in
  `.claude/skills/coding.rules.md`

- When writing unit tests for follow the instructions in
  `.claude/skills/testing.rules.md`

- When implementing notebooks follow the instructions in
  - `.claude/skills/notebook.rules.md`

# Create a plan, if needed
- If the task is not perfectly clear, you MUST not perform it, but ask for
  clarifications
  - When the task is complex, create a `plan.md` with 5 bullet points explaining
    what the plan is
