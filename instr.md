Update the rules so that the size of each figure is always passed
from the interface using

def ...
  *
  figsize: Optional[Tuple[int, int]] = None,
):

  if figsize is None:
      figsize = plt.rcParams["figure.figsize"]

.claude/skills/notebook.rules.md
.claude/skills/interactive_notebook.format/SKILL.md
.claude/skills/notebook.implement_outline/SKILL.md

.claude/templates/interactive_notebook_template.ipynb
.claude/templates/interactive_notebook_template.py
.claude/templates/interactive_notebook_template_utils.py

- If the task is not perfectly clear, you MUST not perform it, but ask for
  clarifications

- When writing code you must always follow the instructions in
  `@.claude/skills/coding.rules.md`
