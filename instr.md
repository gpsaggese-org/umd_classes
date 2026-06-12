Create a bash script website/publish_blog.py that accepts
a --file XYZ.md

The file must have the format with draft.XYZ.md

The action of publishing means

removing the draft. prefix
(e.g., 
draft.how_to.Use_Claude_Code_with_Openrouter.md
-> 
how_to.Use_Claude_Code_with_Openrouter.md)

and switching the 'draft: true' to 'draft: false'

Add an option --undo to reverse the transformation and get a blog
from published to unpublished (adding back `draft.` and flipping
'draft: false' to 'draft: true')

- When writing code you must always follow the instructions in
  `.claude/skills/coding.rules.md`

- If the task is not perfectly clear, you MUST not perform it, but ask for
  clarifications
  - When the task is complex, create a `plan.md` with 5 bullet points explaining
    what the plan is

