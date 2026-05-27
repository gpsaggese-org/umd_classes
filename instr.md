# Step 1
Factor out the logic to select a chunk of file from extract_from_md.py,
in --md_start and --md_end

Move the code to add the options and the selection logic to hmarkdown_select.py

# Step 2
Merge the two options --md_start ABC and --md_end XYZ into a single one
--select XYZ:ABC
- If the first extreme is not specified then it means the beginning
- if the second extreme is not specified, it means extract text from a slide
  until next same-level slide (no explicit end)

- If the first is specified, but the second is EOF, then it means until the end
  of the file

XYZ can be a full header (starting with #, ##, *) in which case the match is from
the beginning including the header (it needs to match the first part of the
title)
- E.g., `# Chapter 1" matches "# Chapter 1: hello", but not "## Chapter 1: hello"

If the string XYZ doesn't start with #, ##, ..., * then the match is done in
the middle of the title (and there needs to be a single match)

# Step 3
Add unit tests

In llm_cli.py add an option

--input_lines X:Y to extract a chunk of the inputs between
--slide_line X

  --md_start MD_START   Starting header: either full format (e.g., '## Section
  1') or partial match (e.g., 'Section 1'). Partial match must be unique.
  --md_end MD_END       Ending header: either full format (e.g., '## Section
  2') or partial match (e.g., 'Section 2'). If not provided, extracts until the
  next header at the same or higher level. Partial match must be unique.

Transform with an LLM and then update the file in place, if one of those options
where specified

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
