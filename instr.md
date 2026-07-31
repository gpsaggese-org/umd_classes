- Create a unit test to check why this is not converted by pandoc into typst with
  small font code

````
- Fit the CATE model on training data
  \begingroup \scriptfont
  ```python
  regr_model = smf.ols("sales ~ discounts*(month + weekday + ...)",
                       data=train).fit()
  ```
  \endgroup
````

The code should go in and reuse some of the test code
- test_lib_notes_to_pdf.py — markdown to PDF/HTML pipeline
- test_notes_to_pdf.py — end-to-end integration tests

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
