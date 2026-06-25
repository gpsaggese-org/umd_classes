---
title: "How to Create a Hook to Run Ruff in Claude Code"
draft: true
authors:
  - gpsaggese
date: 2026-03-02
description:
categories:
  - Causal AI
---

TL;DR: Use Claude Code's PostToolUse hook to automatically run Ruff linter after
every file edit, keeping your code clean without manual steps.

<!-- more -->

// From https://code.claude.com/docs/en/hooks-guide

{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "jq -r '.tool_input.file_path' | xargs npx prettier --write"
          }
        ]
      }
    ]
  }
}
