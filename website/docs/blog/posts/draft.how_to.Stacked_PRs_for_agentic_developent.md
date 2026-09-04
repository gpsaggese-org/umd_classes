- On one side we want AI agents to run as long as possible (ideally all day)
- On the other side we want to be able to review 

- As humans we want to minimize interrupts and create blocks of "similar work"
  instead of context switch / multi-tasking

- If tasks are independent we can simply have agents run in parallel

- If tasks are sequential 

- One solution is an interactive workflow
  - Have a list of tasks, then assign one at the time to the agent,
    review it and then launch the next one
  - One optimization is to have a pre-built list of tasks so we don't have
    to alternate writing specs, run agent, review but we have only
    run agent, review loop (and you consolidate)

- Another solution is stacked PRs

- We let the agent run for longer on a sequence of tasks
  - The problems are that it's more likely for the agent to diverge
    (the longer the list of tasks and the less feedback from us), the
    increase costs of applying our changes once we review things
- In this case the specs need to be all written at once

// TODO(ai_gp): Explain how to use GitHub new stacked PR feature

// TODO(ai_gp): Explain how to use git-spice

