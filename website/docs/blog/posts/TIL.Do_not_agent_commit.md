---
title: "Do Not Let Coding Agents Commit Code Automatically"
date: 2026-06-24
author: GP Saggese
category: coding-best-practices
tags:
    - ai-agents
    - git
    - workflow
    - claude-code
---

## TL;DR

Disable coding agents from committing code automatically. Use git permission
denies in `.claude/settings.local.json` to prevent auto-commits and force a
review-before-commit workflow. This keeps you in control of your codebase and
maintains your understanding of each change.

## What I Learned

Coding agents shouldn't auto-commit. 

The review itself is the value, not just for catching bugs, but for keeping my
mental model synchronized with the codebase. When an agent changes code and
commits immediately, I lose the chance to understand what happened and why.

This breaks my workflow in three ways:

**1. Mental Model Drift** Each agent change should integrate into my
understanding of the codebase. If the agent commits before I review, I miss why a
particular approach was chosen, what edge cases were considered, or how it
affects surrounding code.

**2. Large, Opaque PRs** Auto-committed batches create large PRs that are hard
to review. I prefer targeted, self-contained prompts that produce reviewable
diffs, not stacks of committed changes.

**3. Loss of Agency** The point of agents with `--yolo` mode is independence.
But that independence needs bounds: agents execute tasks autonomously without
permission prompts, yet stay under _your_ control when it comes to git history.

## The Problem: Current LLM Behavior

Current-generation LLMs still don't follow complex instructions reliably. I tried:

- Adding rules to project-level `CLAUDE.md`
- Adding rules to user-level `~/.claude/CLAUDE.md`
- Writing explicit instructions in prompts

Agents committed anyway. They nailed the "make the change" part but buried the
"don't commit" instruction in the noise.

## The Solution: Permission Denies

The most reliable fix: explicitly deny git commits and pushes in
`.claude/settings.local.json`:

```json
{
    "permissions": {
        "deny": ["Bash(*git commit:*)", "Bash(*git push:*)"]
    }
}
```

This works because it's a hard boundary at the permission level, not a
behavioral instruction the agent can misread.

**References:**

- [Claude Code Documentation](https://claude.ai/code) — Permission and settings
  configuration
- [Claude Code Permission System](https://claude.ai/code) — How to configure
  deny rules
