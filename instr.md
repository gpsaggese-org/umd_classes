Step 1
> llm_cli.py -i msml610/lectures_source/Lesson06.2-Using_Bayesian_Networks.txt -pf .claude/templates/graphviz.template.md -o - --select 205
WARNING: Can't find s3fs: continuing
Traceback (most recent call last):
  File "/Users/saggese/src/umd_classes1/helpers_root/dev_scripts_helpers/llms/llm_cli.py", line 362, in <module>
    _main(_parse())
  File "/Users/saggese/src/umd_classes1/helpers_root/dev_scripts_helpers/llms/llm_cli.py", line 325, in _main
    expected_num_chars,
    ^^^^^^^^^^^^^^^^^^
AttributeError: 'bool' object has no attribute 'expected_num_chars'

Step 2
Add an option --dry_run for llm_cli.py to skip calling the LLM, but show what would be done

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
