---
title: "TIL: Auto-Reload Files in Vim When Working With AI Agents"
authors:
    - gpsaggese
date: 2026-06-17
description:
draft: true
categories:
    - Developer Tools
    - Productivity
---

TL;DR A 3-line vimscript snippet that polls `checktime` every second keeps vim
buffers in sync when AI agents modify files on disk.

<!-- more -->

- I learned a practical vim trick that solves a common friction point when
  collaborating with AI coding agents with `vim`: automatic file reloading

## What I Learned

- When working with AI agents on code, a common workflow emerges:
    - The AI agent edits a file on disk
    - I have that same file open in vim
    - Vim detects the external modification and prompts:
      ```
      "File changed since last read. Reload? (Y/N)"
      ```
    - This creates awkward back-and-forth: approve the reload, lose your cursor
      position, risk overwriting the agent's changes, ...

- The fix is a simple vimscript snippet that polls for file changes every second:

    ```vim
    function! AutoReload()
      silent! checktime
    endfunction

    call timer_start(1000, {-> AutoReload()}, {'repeat': -1})
    ```

- `checktime` checks if any open buffers have been modified externally and
  reloads them silently
- The `timer_start` with `{'repeat': -1}` runs it every 1000ms indefinitely
- No more prompts, no more manual reloads

## Why It Matters

- AI coding agents work best when they can edit files incrementally and see
  their changes reflected

- The bottleneck is often not the agent's speed but the human's ability to keep
  their editor in sync with what the agent is doing

- This small change eliminates a constant source of friction

## Key Takeaways

- Vim's `checktime` is powerful for keeping buffers in sync with the filesystem
- `timer_start` with infinite repeat is a clean way to implement polling in vim
- A simple 3-line config change can significantly improve the human-AI pairing
  experience

- **Trade-off**: You lose the ability to use vim's in-memory state to override
  git operations (e.g., keeping a file open in vim, running `git reset --hard`,
  then writing the vim buffer to restore it)
    - For me, the convenience of auto-reload outweighs this edge case

## References and Further Reading

- `:help checktime` in vim
- `:help timer_start` in vim
- `.vimrc` documentation on GitHub
