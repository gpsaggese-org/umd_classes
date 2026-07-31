Implement unit tests for extract_cc_log.py

1) A unit test that runs for a given prompt the different configurations saving
   the results in a dir

cc -p "Describe recursion in 100 words" 2>&1 | tee tmp1.txt
cc -p "Describe recursion in 100 words" --verbose 2>&1 | tee tmp2.txt
cc -p "Describe recursion in 100 words" --debug 2>&1 | tee tmp3.txt
cc -p "Describe recursion in 100 words" --output-format=stream-json 2>&1 | tee tmp4.txt
cc -p "Describe recursion in 100 words" --output-format=stream-json --include-partial-messages 2>&1 | tee tmp5.txt
cc -p "Describe recursion in 100 words" --verbose --output-format=stream-json --include-partial-messages 2>&1 | tee tmp6.txt

2) A unit test that runs extract_cc_log.py on all the files in a dir
  and saves the results in a different dir

  extract_cc_log.py -i .../tmpXYZ.txt | tee .../tmpXYZ.output.txt

3) Create a unit test that runs extract_cc_log.py on each of tmp?.txt
   and dumps statistics (e.g., number of tokens, number of messages from user and
   assistant)

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
