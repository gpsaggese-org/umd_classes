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

Coding agents shouldn't auto-commit. I learned this the hard way after watching
agents complete tasks perfectly and then thoughtlessly commit changes without
waiting for my review.

For me **the review _is_ the value**, not just for catching bugs, but for keeping
my mental model synchronized with the codebase. When an agent makes a change and
immediately commits, I lose the opportunity to fully understand what happened and
why.

There are several reasons why agent auto-commits break my workflow:

**1. Mental Model Drift** Every change an agent makes should integrate into my
understanding of the codebase. If the agent commits before I review, I might
miss why a particular approach was chosen, what edge cases were considered, or
how it affects surrounding code. This gap accumulates.

**2. Large, Opaque PRs** When agents auto-commit multiple changes, you end up
with large PRs that are hard to review. My preference is for targeted,
self-contained prompts that result in reviewable diffs, not batches of
auto-committed changes.

**3. Loss of Agency** The whole point of using coding agents with something like
`--yolo` mode is to give them independence. But that independence should be
bounded—agents should execute tasks autonomously without permission prompts, yet
remain under _your_ control when it comes to git history.

## The Problem: Current LLM Behavior

Current-generation LLMs are difficult to steer toward complex instructions. I
tried:

- Adding rules to project-level `CLAUDE.md`
- Adding rules to user-level `~/.claude/CLAUDE.md`
- Writing explicit instructions in prompts

The agents still committed. They followed the "make the change" instruction
perfectly but glossed over the "don't commit" instruction in the noise of other
guidance.

## The Solution: Permission Denies

The most reliable solution I found: explicitly deny git commits and pushes in
`.claude/settings.local.json`:

```json
{
    "permissions": {
        "deny": ["Bash(*git commit:*)", "Bash(*git push:*)"]
    }
}
```

This works because it's a hard boundary enforced at the permission level, not a
behavioral instruction the agent might misinterpret.

**References:**

- [Claude Code Documentation](https://claude.ai/code) — Permission and settings
  configuration
- [Claude Code Permission System](https://claude.ai/code) — How to configure
  deny rules
