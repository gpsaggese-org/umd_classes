When running

notes_to_pdf.py --input=msml610/lectures_source/Lesson08.6-Causal_inference.txt --output=msml610/lectures/Lesson08.6-Causal_inference.pdf --type=slides --toc_type=navigation --debug_on_error --skip_action=cleanup_before --skip_action=cleanup_after --slides_engine typst --no_fail_on_warnings

The text

```
No email (`no_email`)
```

is not rendered properly but is left like

#text(fill: blue)[no_email]: control


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
