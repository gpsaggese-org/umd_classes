In notes_to_pdf.py add an option --slides_engine auto that
recognizes the engine to use

If there are metadata then use the engine that is required

// slides_engine=typst

if there is no metadata then use beamer

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
