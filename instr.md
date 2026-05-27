# Step 1
Factor out the logic to select a chunk of file from extract_from_md.py,
in --md_start and --md_end

Move the code to add the options and the selection logic to hmarkdown_select.py

# Step 2
Merge the two options --md_start ABC and --md_end XYZ into a single one
--select START:END (natural order)

- If the first extreme is not specified `--select :END`
  then it means the beginning
- if the second extreme `--select START:` is not specified, it means extract text from a slide
  until next same-level slide (no explicit end)

- If the first is specified, but the second is EOF, then it means until the end
  of the file

- START / END can be a string or a number XYZ

- XYZ can be a full header starting with #, ##, * in which case the match is from
  the beginning including the header (it needs to match the first part of the
  title, the prefix)
- E.g., `# Chapter 1" matches "# Chapter 1: hello", but not "## Chapter 1: hello"
- E.g., `# Chapter 1" does not match "## Chapter 1" since the header needs to
  match exactly
- "Chapter" match "My Chapter" and also "Chapter Something"
- `* Chapter 1` means a slide

- If the string XYZ doesn't start with #, ##, ..., * then the match is done in
  the middle of the title (and there needs to be a single match)

- If the string XYZ is a number then consider that as line number in the file
  starting from 1

Update / add unit tests

# Step 3
In llm_cli.py add an option 

--select X:Y to extract a chunk of the input file

using code from  hmarkdown_select.py

Transform with the LLM according to the flow and then update the file in place,
if --select X:Y was specified and --output was not

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
