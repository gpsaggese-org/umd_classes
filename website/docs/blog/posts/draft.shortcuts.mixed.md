---
title: "Mixed Keyboard Shortcuts"
draft: true
authors:
  - gpsaggese
date: 2026-08-20
categories:
  - Productivity
---

TL;DR: A cheat sheet of keyboard shortcuts across tools.

<!-- more -->

# Conventions

* Shortcuts: Conventions
- Combinations to be pressed together are enclosed into parentheses:
  - E.g., `(CTRL + x)`
  - E.g., `(CTRL + x) + b`

- Letters are non capitalized and `SHIFT` is explicitly used
  - For MEM: it is ok to use capital letters to aid remembering

- For the non-letter (e.g., `1`, `!`, `;`) we use the char directly
  - E.g., we write `CTRL + !` and not `CTRL + SHIFT + 1`

- It can a good idea to specify `L_` / `R_` for `CMD` or `CTRL` to help muscle
  memory

* Shortcuts: Use keys in alphabetical order
- Use the combination in terms of the sequence of keys in alphabetical order:
  - `CMD` (Apple, Command)
  - `CTRL` (`^`)
  - `OPT` (Alt, Option, `\=`)
  - `SHIFT`

* Shortcuts: Abbreviations of modifiers
```
Symbol | Name    | Aka      | MEM
--------------------------------------------
⌘, #   | Command | Apple    | (Command)er (Pound) of (Apple)
⌥, \=  | Option  | Alt      | You have the (Option) to h(Alt) in front of the (Slide \=)
⇧      | Shift   |          |
^      | Control |          | (Chevron) (^) to be in (Control)
Fn     | Fn      | Function |
       | Escape  | Esc      |
```

```
Name       Aka          Abbreviation
------------------------------------
Command    Apple, #     CMD, R_CMD, L_CMD
Option     Alt, \=      OPT
Shift                   SHIFT, R_SHIFT, L_SHIFT
Control    ^            CTRL
Fn         Function     FN
Escape     Esc
```

- On the keyboard the keys are in order from left to right:
  - L_SHIFT (S)
  - CTRL (CT)
  - OPT (O)
  - L_CMD (CM)
  - R_CMD
  - R_SHIFT (S)

# macOS

// `https://support.apple.com/en-us/HT201236`

## Windows

* macOS: Close window
- `CMD + w`

* macOS: Minimize window
- `CMD + m`

* macOS: Cycle through windows
- `CMD +` `

* macOS: Move among tabs of an app
- `CMD + {}` i.e., `R_CMD + R_SHIFT + []`
- E.g., Chrome, Preview

* macOS: Select block area in terminal
- `CMD + OPT + mouse`

## Screenshot

// From https://support.apple.com/guide/mac-help/take-a-screenshot-or-screen-recording-mh26782/mac

* macOS: Screenshot mem
- Base keystrokes `(R_CMD + L_OPT)`
- 3: dir
- 4: portion
- 5: screenshot
- `L_SHIFT`: clipboard vs screen
  - File looks like `Screen Shot 2021-01-26 at 5.11.55 PM`

* macOS: Open the Screenshot app
- `R_CMD + R_SHIFT + 5`

* macOS: Take a screenshot to dir / clipboard
- To Screenshot app dir: `CMD + CTRL + 3`
- To Clipboard: `CMD + CTRL + SHIFT + 3`

* macOS: Take a screenshot of a portion of a screen
- To Screenshot app dir: `CMD + CTRL + 4`
- To Clipboard: `CMD + CTRL + SHIFT + 4`

## Misc

* macOS: Get definition of a word
- `CTRL + CMD + d`
- MEM: ccd = definition

* macOS: Get pronunciation
- `CTRL + CMD + p`
- You need to enable this in Preferences -> Speech
- MEM: ccp = pronunciation

* macOS: Turn off screen
- `> pmset displaysleepnow`

* macOS: Enable / disable do not disturb
- `CTRL + F10`

## Spaces

* macOS: Move among Spaces
- `CTRL + arrows`

* macOS: All windows of same app across Spaces
- `CTRL + down`

* macOS: Apps in one space and move apps across Spaces
- `CTRL + up`

* macOS: Switch among applications
- `CMD + TAB`, `CMD + SHIFT + TAB`

* macOS: Spectacle align windows
- `CMD + OPT + arrows`
- MEM: co

* macOS: Spectacle full-window
- `CMD + OPT + f`
- MEM: cof

# Apple Preview

* Preview: Continuous scroll / single page
- Continuous scroll: `CMD + 1`
- Single page: `CMD + 2`

* Preview: Side bar
- No side bar: `CMD + OPT + 1`
- Miniatures: `CMD + OPT + 2`
- Table of contents: `CMD + OPT + 3`

# Google Chrome

* Chrome: Moving across tabs
- Move among tabs: `CMD + {}`, i.e., `CMD + SHIFT + []`
- Jump to first tab: `CMD + 1`

* Chrome: History
- Go back in history: `CMD + [`
- Go forward in history: `CMD + ]`
- MEM: Like move among tabs but without `SHIFT`

* Chrome: Re-open last closed tab and jump to it
- `CTRL + SHIFT + t`

* Chrome: Show / hide the bookmarks table
- `CMD + SHIFT + b`

* Chrome: Open the bookmarks manager in a tab
- `CMD + OPT + b`

* Chrome: Jump to address bar
- `CMD + l`

* Chrome: Search in page
- Search in page: `CMD + f`
- Search next: `CMD + g`
- Search previous: `CMD + SHIFT + g`

* Chrome: Search / jump to tabs
- `CMD + SHIFT + a`: search in all tabs

* Chrome: Zoom page
- Zoom in: `CMD + +`, i.e., `CMD + SHIFT + =`
- Zoom out: `CMD + -`
- Reset zoom: `CMD + 0`

# Chrome Vimium

// `https://github.com/philc/vimium/wiki`

* vimium: Invariants
- With `SHIFT`: there in new tab
- Without `SHIFT`: here in current tab
- MEM: the default (i.e., no shift) means here

* vimium: Help
- Get help: `?`

* vimium: History
- Go back in history: `H` (or `CTRL + [` for Chrome shortcut)
- Go forward in history: `L` (or `CTRL + ]` for Chrome shortcut)

* vimium: Navigate page
- Move in the page: `hjkl`
- Scroll half-page up / down: `u` / `d`
- Scroll full-page up / down: `space` / `SHIFT + space`
- Top / bottom: `gg` / `G`

* vimium: Open new tab
- `t` (same as `CMD + t`)

* vimium: Close tab
- Close current tab: `x` (same as `CMD + w`)
- Restore closed tab: `X` (same as `CMD + SHIFT + t`)

* vimium: Navigate tabs
- Go to first / last tab: `g0`, `g$`
- Duplicate current tab: `yt`
  - This is equivalent to `yy` (copy URL) + `P` (open copied URL in new tab)

* vimium: Duplicate current tab
- `yt`

* vimium: Move tab to new window
- `W`

* vimium: Open link
- Open links: `f`
- Open in current tab: lower-case letters for links 
- Open in new tab: upper-case letters for links

* vimium: Search in open tabs
- `SHIFT + t`
- MEM: `t` = tabs

* vimium: Search bookmark
- Search and open in current tab: `b`
- Search and open in new tab: `B`
- MEM: `b` = bookmarks

* vimium: Search everywhere
- Search in URL, bookmark, history 
- Search and open in current tab: `o`
- Search and open in new tab: `O`
- MEM: `o` = omni-search

* vimium: Find in page
- Find mode: `/`
- Enter and then use vim shortcuts to navigate: `/`, `?`, `n`, `N`

* vimium: Copy / open URL
- Copy URL to clipboard: `yy`
- Open URL in clipboard here: `p`
- Open URL in clipboard in new tab: `P`

* vimium: Visual mode
- Visual mode: `v`
- Visual mode line-by-line: `V`
- Copy / paste selected part of page with usual vim shortcuts: `yy`, `p`

# Gdocs

* gdocs: Open / search shortcuts
- `CMD + /`

* Search menu
- `OPT + /`

* gdocs: Zoom
- Zoom in: `CMD + OPT + =`
- Zoom out: `CMD + OPT + -`

* gdocs: Font size
- Increase font size: `CMD + >`, `CMD + SHIFT + ,`
- Decrease font size: `CMD + <`, `CMD + SHIFT + .`

* gdocs: Formatting text
- Apply the "normal style": `CMD + OPT + 0`
- Apply header 1: `CMD + OPT + 1`

* 
- Suggesting mode: `CMD + OPT + SHIFT + x`
- Editing mode: `CMD + OPT + SHIFT + z` (but doesn't work?)

# Jupyter

* Jupyter: Vim bindings
- `H`, `F1`: shortcut help

* Jupyter: Go in Jupyter mode
- `SHIFT + ESC`

* Jupyter: Go in vim navigation mode
- `ESC`

* Jupyter: Run cell
- `CMD + return`

* Jupyter: Reset the kernel
- `0`, `0`

* Jupyter: Run all cells
- `CMD + SHIFT + return`

* Jupyter: Header level
- `CMD + 1`

# Tmux

* tmux: Create a session
- `tmux new -s SESSION`

* tmux: Attach a session
- `tmux attach -t SESSION`

* tmux: Kill a session
- `tmux kill-session -t SESSION`

* tmux: Leader key
- `(CTRL + g)`

* tmux: Help
- `(CTRL + g) + ?`

* tmux: Disconnect
- `(CTRL + g) + d`

* tmux: Execute command
- `(CTRL + g) :`

* tmux: Apply new config
- `(CTRL + g) :source ~/.tmux.conf`

* tmux: Move among tabs
- `(CTRL + g) + p, n`

* tmux: Jump to window
- `(CTRL + g) + 0, ..., 9`
- With high index: `(CTRL + g) + '10`

* tmux: Alternate window
- `(CTRL + g) + l`

* tmux: Copy / paste
- Copy mode: `(CTRL + g) + [`
- Paste mode: `(CTRL + g) + ]`

* tmux: Move inside window
- `(CTRL + g) + [ + (CTRL + u, d)`
- MEM: `(CTRL + g) + [` to go in copy mode. Then `(CTRL + u, d)` to move up and
  down

* tmux: Rename window
- `(CTRL + g) + ,`

* tmux: Monitoring for silence
- Start `(CTRL + g) :setw monitor-silence 30`
- Stop: `(CTRL + g) :setw monitor-silence 0`

* tmux: Vertical split pane
- `(CTRL + g) + %`

* tmux: Horizontal split pane
- `(CTRL + g) + "`

* tmux: Move between splits
- `(CTRL + g) + o`
