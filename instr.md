When running lint_txt.py, the script calls an Apple container which prints
  ... [0/6] [0s]
  ... [1/6] Fetching image [0s]
  ... [2/6] Unpacking image [0s]
  ... [3/6] Fetching kernel [0s]
  ... [4/6] Fetching init image [0s]
  ... [5/6] Unpacking init image [0s]
  ... [6/6] Starting container [0s]
  ... [6/6] Starting container [0s]

Change the script so that 

  ... [0/6] [0s]
  ... [1/6] Fetching image [0s]
  ... [2/6] Unpacking image [0s]
  ... [3/6] Fetching kernel [0s]
  ... [4/6] Fetching init image [0s]
  ... [5/6] Unpacking init image [0s]
  ... [6/6] Starting container [0s]
  ... [6/6] Starting container [0s]

is removed from the output
using an already existing function in hunit test purification 

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
