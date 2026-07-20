In notes_to_pdf.py --input=msml610/lectures_source/Lesson03.2-Propositional_and_first_order_logic.txt --output=msml610/lectures/Lesson03.2-Propositional_and_first_order_logic.pdf --type=slides --to
c_type=navigation --debug_on_error --skip_action=cleanup_before --skip_action=cleanup_after --slides_engine typst --no_fail_on_warning --skip_action=open

the table of content is still generated incorrectly when there are the same
subsections names

E.g.,
```
513 ==== Table of Content
514 <table-of-content-3>
515 - Propositional logic
516   - Syntax
517   - Semantics
518 - #text(fill: red, weight: "bold")[#emph[First-order Logic]]
519   - Syntax
520   - Semantics
521
522 ==== Table of Content
523 <table-of-content-4>
524 - Propositional logic
525   - #text(fill: red, weight: "bold")[#emph[Syntax]]
526   - Semantics
527 - First-order Logic
528   - Syntax
529   - Semantics
```

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
