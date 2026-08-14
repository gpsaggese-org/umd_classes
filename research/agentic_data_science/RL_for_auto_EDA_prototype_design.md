# prototype agent design: Claude Code as the EDA agent (issue #506)

**Author:** @Delvitron1019
**Issue:** #506 — RL agents for EDA and ML
**Status:** prototype built (`cc_eda_agent.py`), agent path pending a local Claude Code run.

## What GP asked for

On #506, prototype is "an inference time loop (a prompt) to create a prototype of the
EDA agent." When I asked whether the prototype's agent should be a genuine LLM
tool-calling loop, GP's answer was: my call, we'll move to LangChain/AutoGen later,
but try it in Claude first — and he pointed at his own wrapper,
`helpers_root/dev_scripts_helpers/ai/cc_lib.py`, which he uses to loop Claude Code
over a task.

## The design decision this forced

`cc_lib.py` wraps the **claude_agent_sdk** — it drives **Claude Code**, not the bare
Messages API. Its `PromptSequencer` runs prompts against a Claude Code session that
already has built-in tools (`Read`, `Write`, `Bash`, `Edit`), with control over
allowed tools, permission mode, and session vs. stateless context.

That rules out the "register my Python functions as tools" approach and points to a
cleaner one: **the agent is Claude Code itself, writing and running its own analysis
code.** This matters because the earlier prototype was really "Python solves it, the
LLM formats it" — the model did no reasoning. Here Claude Code gets only the raw data
and has to decide what to compute, run it, read the output, and iterate.

## Architecture

```
  Environment (ours)                 Claude Code (the agent)              Scoring (ours)
  ------------------                 -----------------------              --------------
  random DAG  G*      ── data.csv ──▶  reads data, writes+runs      ── graph.json ──▶  SHD(G_hat, G*)
  LiNGAM data          (no G*)         Python: corr, CI tests,                          + edge P/R
  (Milestone 1)                        LiNGAM direction; emits DAG                      + OOS R^2
                                       (the inference-time loop)                        (Milestone 2)
```

- We write **only the data** to `data.csv`; the ground-truth graph is held out.
- `PromptSequencer(allowed_tools=["Read","Write","Bash"], permission_mode=
  "bypassPermissions", cwd=workdir, max_turns=40)` runs one prompt telling Claude Code
  to do the EDA and write the inferred DAG to `graph.json`.
- We read `graph.json`, build the adjacency matrix, and score it with the existing SHD
  pipeline. The reward stays fully verifiable because we know `G*`.

## Why this is the right shape for the project

- **Faithful to GP's workflow** — reuses his `cc_lib` exactly as documented
  (`import dev_scripts_helpers.ai.cc_lib as dshaccli`), so it slots into how he already
  runs Claude Code.
- **A real agent loop** — Claude Code chooses and runs its own tools over multiple
  turns, which is what "inference-time loop" should mean.
- **Swappable** — the scoring and environment are agent-agnostic. When we move to
  LangChain/AutoGen (GP's plan) or to the RL policy (the draft's Milestone 3), only the
  middle box changes; the harness stays.

## What runs today vs. what needs your environment

`cc_eda_agent.py` has two paths:

- `--simulate` — **tested, runs anywhere.** Stands in for Claude Code by running the
  same heuristic it should learn to run, writes `graph.json`, and scores it. This proves
  the environment → dataset → graph → score round-trip end to end (e.g. seed 2: SHD 1,
  tpr 0.833).
- default (real) — drives Claude Code via `PromptSequencer`. Needs `claude_agent_sdk`
  installed, Claude Code authenticated, and `helpers_root` on `PYTHONPATH`. It fails
  gracefully with instructions when those are missing. **I could not run this in my
  environment — it needs a live Claude Code session, so it's the one piece to try on
  your machine.**

## Open questions for GP

1. **Prompt-driven-code vs. custom tools.** I went with Claude Code writing its own
   analysis (matches `cc_lib`). If you'd rather expose our `Toolbox` functions as
   explicit callable tools, that's a different SDK setup — worth confirming.
2. **How much to hand the agent.** Right now the prompt names the methods (partial
   correlation, LiNGAM direction). Do you want it that prescriptive, or should the agent
   discover the approach with a looser prompt — which is a more honest test of the agent
   but higher variance?
3. **Cost / turn budget.** `max_turns=40` and `bypassPermissions` for unattended runs —
   fine for a prototype, but confirm before running it across many graphs.

## Next steps

- [ ] Run the real path locally (Claude Code + `claude_agent_sdk`), on one graph first.
- [ ] Compare the Claude Code agent's SHD to the scripted baseline across seeds.
- [ ] If it beats the baseline, this is the inference-time prototype the draft's
      Milestone 3 (the RL policy) then aims to match or exceed.
