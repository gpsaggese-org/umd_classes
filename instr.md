Create a script 

./helpers_root/dev_scripts_helpers/thin_client/tmux_reset.py

that for each tmux window sets the name to an empty string.

The first window to have pwd end with helpers_root should
e.g., /Users/saggese/src/umd_classes1/helpers_root
be called *helpers* and the remaining empty string

## Plan

- [x] Create `helpers_root/dev_scripts_helpers/thin_client/tmux_reset.py`
  following the `_parse()` / `_main(parser)` script skeleton
  - [x] List the windows of the current tmux session (`tmux list-windows`),
    getting each window's index and the current working directory of its
    active pane
  - [x] Compute the new name for each window:
    - The first window whose pane working directory basename is
      `helpers_root` is named `helpers`
    - Every other window (including further `helpers_root` matches) is
      named `""` (empty string)
  - [x] Rename each window (`tmux rename-window`), honoring a `--dry_run`
    flag that only logs what would be renamed
- [x] Make the script executable (`chmod +x`)
- [x] `git add` the new file (do not commit)
- [x] Scope: operate only on the tmux session the script runs in (not all
  sessions), per user confirmation

## Result

- Done this
  - Created `helpers_root/dev_scripts_helpers/thin_client/tmux_reset.py`,
    following the repo's `_parse()` / `_main(parser)` script skeleton and
    `dassert`/logging conventions
  - Script lists the windows of the tmux session it runs in, renames the
    first window whose active pane is in a `helpers_root` directory to
    `helpers`, and clears the name of every other window
  - Added a `--dry_run` flag (per `script.rules.md`) that logs, per window,
    the window index, its current working directory, and the name it would
    get, without renaming anything
  - Verified both `--dry_run` and the real run against a scratch tmux
    session with 3 windows (two under `helpers_root`, one elsewhere): only
    the first `helpers_root` window was named `helpers`, the rest were
    cleared, and `--dry_run` left names untouched
  - Made the script executable and `git add`ed it inside the `helpers_root`
    submodule (not committed)
- Done that
  - N/A: no part of the plan was skipped
