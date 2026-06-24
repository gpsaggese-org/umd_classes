I really don't like when coding agents make (the requested) change and then
commit code to git, since my rule is to review every change made by the agent
to make sure I update my mental model.

Since my PRs have grown large with coding agents, I prefer to review the
code close to the change, like:
- create a prompt to do a self-contained change
- the agent does its thing
- review the change
- test
- commit

Also I am big fan of --dangerously_skip_permissions / --yolo (the whole point
is to get the agent to operate independently), (I am also working on
contenairing the agent to avoid to have it marauding my system)

I've tried to add this in the CLAUDE.md at project, at user level, but nothing
the agent keept committing the code (current generation of LLMs are still
difficult to steer and follow complex commands).

The best solution I've found to avoid committing is to add 
in `.claude/settings.local.json` something like

```
{
  "permissions": {
    "allow": [
    ...
    "deny": [
      "Bash(*git commit:*)",
      "Bash(*git push:*)"
    ]
  },
```

No commit and absolutely no pushing in my Git branches.
