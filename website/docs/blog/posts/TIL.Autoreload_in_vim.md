---
title: "TIL: Auto-Reload Files in Vim When Working With AI Agents"
authors:
    - gpsaggese
date: 2026-06-24
description:
draft: false
categories:
    - Developer Tools
    - Productivity
---

TL;DR A 3-line vimscript snippet that polls `checktime` every second keeps vim
buffers in sync when AI agents modify files on disk.

<!-- more -->

- I discovered a vim trick that eliminates a common annoyance when working with
  AI coding agents: automatic file reloading

## What I Learned

- When working with AI agents on code, a familiar loop happens:
    - AI agent edits a file on disk
    - I have that same file open in vim
    - Vim detects the change and prompts:
        ```
        "File changed since last read. Reload? (Y/N)"
        ```
    - Then comes the back-and-forth: approve the reload, lose your cursor
      position, risk overwriting the agent's work, ...

- The fix is three lines of vimscript that check for file changes every second:

    ```vim
    function! AutoReload()
      silent! checktime
    endfunction

    call timer_start(1000, {-> AutoReload()}, {'repeat': -1})
    ```

- `checktime` reloads any buffers that changed on disk
- `timer_start` runs it every 1000ms, forever
- Prompts gone, no more manual reloads

## Why It Matters

- AI agents work best when they can edit files incrementally and watch the
  changes land

- The real constraint isn't agent speed—it's keeping your editor in sync with
  what it's doing

- This small change removes a constant annoyance

## The Tradeoff

- You lose vim's ability to override git operations. For instance, you can't
  keep a file open in vim, run `git reset --hard`, then write the vim buffer to
  restore it
- For me, the convenience outweighs this edge case

## References and Further Reading

- `:help checktime` in vim
- `:help timer_start` in vim
- `.vimrc` documentation on GitHub
