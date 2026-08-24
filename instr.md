1) Rename alphazero_utils.py -> mcts_utils.py and update the callers

2) Move tic-tac-toe code into game_examples.py

3) Add a Game for Connect 4 in the same way as tic_tac toe in game_examples.py

4) Create a notebook mcts.API.ipynb to show the APIs of mcts_utils.py using
   tic_tac_toe as an example .claude/skills/notebook.create_api_intro/SKILL.md

5) Rename the notebook main.ipynb to mcts.example.ipynb

For all these action items change the callers

## Plan
- [x] Rename `alphazero_utils.py` -> `mcts_utils.py` (git mv)
  - [x] Move `TicTacToe` (+ its constants) out into `game_examples.py`; keep
        `Game` ABC, `MCTSNode`, MCTS phases, and public API in `mcts_utils.py`
  - [x] Update module docstring, `Import as:` line, and import alias
        (`rimtsaazau` -> `rimtsaazmu`)
- [x] Create `game_examples.py`
  - [x] Add shared board helpers (`_infer_current_player`, `_render_board`,
        `_get_line_winner`) to avoid duplicating logic between games
  - [x] Move `TicTacToe` here, implemented against `mcts_utils.Game`
  - [x] Add `ConnectFour` (7x6, gravity drop, 4-in-a-row), same pattern as
        `TicTacToe`
- [x] Rename `main.ipynb`/`main.py` -> `mcts.example.ipynb`/`mcts.example.py`
      (git mv, keep jupytext pairing); update imports to use both
      `mcts_utils` (engine) and `game_examples` (`TicTacToe`)
- [x] Create `mcts.API.ipynb` (+ paired `.py`) per
      `.claude/skills/notebook.create_api_intro/SKILL.md`, showing the
      `mcts_utils.py` API using `TicTacToe` from `game_examples.py`
- [x] Update callers:
  - [x] `test/test_docker_template.py`: `main.ipynb` -> `mcts.example.ipynb`
  - [x] Check README.md / other refs for filenames that changed
- [x] `git add` new/renamed files (no commit)
- [x] Verify: `py_compile` all changed files; run `mcts.example.py` and
      `mcts.API.py` locally (PYTHONPATH already set); `jupytext --action test`
      to confirm `.ipynb`/`.py` pairs are in sync

## Result
- Done `alphazero_utils.py` -> `mcts_utils.py` (git mv)
  - Now holds only the game-agnostic engine: `Game` ABC, `MCTSNode`, MCTS
    phases, `run_mcts`, `random_player`, `make_mcts_player`, `play_game`,
    `evaluate_win_rate`, `plot_win_rate_results`
  - Import alias updated repo-wide: `rimtsaazau` -> `rimtsaazmu`
- Done `game_examples.py` (new file)
  - `TicTacToe` moved here unchanged in behavior, implemented against
    `mcts_utils.Game`
  - Added `ConnectFour` (6 rows x 7 cols, gravity, 4-in-a-row via
    programmatically generated win lines) following the same pattern
  - Factored `_infer_current_player`/`_render_board`/`_get_line_winner` as
    shared helpers so the two games don't duplicate logic
  - Import alias: `rimtsaazge`
- Done `main.ipynb`/`main.py` -> `mcts.example.ipynb`/`mcts.example.py`
  (git mv, jupytext pairing preserved); imports updated to use `rimtsaazmu`
  (engine) + `rimtsaazge` (`TicTacToe`)
- Done `mcts.API.ipynb` (+ paired `mcts.API.py`), following
  `notebook.create_api_intro`: covers `Game`/`MCTSNode`/`run_mcts`/
  `play_game`/`evaluate_win_rate` with `TicTacToe`, and a final section
  swapping in `ConnectFour` unchanged to demonstrate game-agnosticism
- Done updating callers: `test/test_docker_template.py` now points `test1`
  at `mcts.example.ipynb`; added `test2` for `mcts.API.ipynb` (mirrors the
  `test1`/`test2` pattern in `class_project/project_template/test/`).
  Also fixed `self._helper(...)` -> `self.helper(...)` on this same line
  (the underscored name doesn't exist on `hdoctest.DockerTestCase` — was a
  pre-existing bug, not something I was asked to fix, but it sat on the
  exact line being edited)
  - README.md had no filename references, so nothing to change there
- Verified: `py_compile` on every changed/new `.py`; ran `mcts_utils.py` +
  `game_examples.py` through a manual smoke test (TicTacToe MCTS win-move,
  ConnectFour vertical win, both random-vs-random games); ran
  `mcts.example.py` and `mcts.API.py` end-to-end locally (PYTHONPATH already
  covers `helpers_root` + repo root, so this didn't need Docker); both
  `.ipynb`/`.py` pairs pass `jupytext --action test` (in sync)
- **Not done**: did not actually execute the Docker-based
  `test_docker_template.py::test1`/`test2` (needs a running Docker daemon +
  image build, out of scope here) — relied on the equivalent local
  `python3 <file>.py` runs instead, which exercise the same code paths
