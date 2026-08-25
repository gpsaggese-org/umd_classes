1) In ./research/Implement_MonteCarlo_Tree_Search_and_Alpha_Zero/ 
  add a notebook using minimax, alpha-beta pruning, depth-limited search, and flat
  montecarlo using the same structure of Game

- Show how the search tree is built

Use notation and concepts aligned with /Users/saggese/src/umd_classes1/msml610/lectures_source/Lesson09.8-MonteCarlo_Tree_Search.smd

## Plan

- [x] Read `mcts_utils.py`, `game_examples.py`, `mcts.example.py`,
      `mcts_API_utils.py`, `README.md` to match the existing `Game`
      interface, module layout, and notebook conventions
- [x] Read `Lesson09.8-MonteCarlo_Tree_Search.smd` for notation: `b`, `d`,
      `O(b^d)`, alpha-beta bounds, depth-limited cut + evaluation function,
      flat MC's `Q_hat(s0, a)` definition
- [x] `mcts_utils.py`: rename the private rollout helper `_simulate` to
      public `random_rollout` (unchanged body) so flat Monte Carlo can reuse
      the exact same default policy MCTS uses (Lesson09.8: "Flat Monte Carlo
      is exactly MCTS with a tree of depth one")
- [x] `game_examples.py`: add `evaluate_tic_tac_toe(state)`, a cheap
      open-lines heuristic in `[-1, 1]` for depth-limited search's cut nodes
      (Lesson09.8: "every cut node must be scored by a hand-built evaluation
      function")
- [x] New `search_algorithms_utils.py`, mirroring `mcts_utils.py`'s
      structure (`Game`-agnostic, a tree-node class, `build_*_tree()` /
      `run_*()` / `make_*_player()` per algorithm):
  - [x] `SearchNode`: state/parent/move/children plus a backed-up `value`,
        a `pruned` flag, and an `is_heuristic` flag, so one node class and
        one Graphviz renderer cover all four algorithms
  - [x] Minimax: `build_minimax_tree()`, `run_minimax()`
  - [x] Alpha-beta pruning: `build_alpha_beta_tree()`, `run_alpha_beta()`,
        recording pruned siblings as unexplored placeholder nodes so the
        diagram can show what was skipped
  - [x] Depth-limited search: `build_depth_limited_tree()`,
        `run_depth_limited()`, taking an `evaluate_fn` for cut nodes
  - [x] Flat Monte Carlo: `build_flat_mc_tree()`, `run_flat_mc()`, reusing
        `mcts_utils.random_rollout()`
  - [x] `make_minimax_player()` / `make_alpha_beta_player()` /
        `make_depth_limited_player()` / `make_flat_mc_player()` for
        `mcts_utils.play_game()`
  - [x] `build_tree_graph()`: depth-capped Graphviz renderer shared by all
        four (explored / terminal / heuristic-cut / pruned node styles)
- [x] New `search_algorithms.example.ipynb` / `.py` (Jupytext `py:percent`
      pair, following `mcts.example.py`'s Part/Cell structure):
  - [x] Imports, Part 2 (the game, same as `mcts.example.py`)
  - [x] Part 3: Minimax on the same tactical `demo_state` as
        `mcts.example.py` Cell 3.1, with its search-tree diagram
  - [x] Part 4: Alpha-beta pruning on the same state, node-count comparison
        against Part 3 and its pruned-tree diagram
  - [x] Part 5: The evaluation function, then depth-limited search compared
        to the exact minimax value
  - [x] Part 6: Flat Monte Carlo, `Q_hat(s0, a)` per action and its
        depth-one tree
  - [x] Part 7: Side-by-side comparison of all four plus MCTS on the same
        position (move, value, nodes explored), tying back to Lesson09.8's
        "MCTS vs Exhaustive Search" table
  - [x] Part 8: Full-game sanity check (alpha-beta / depth-limited / flat MC
        vs. random); raw minimax excluded from full games with a note on why
        (exponential cost from an empty board vs. alpha-beta's `O(b^{d/2})`)
  - [x] Sync `.py` -> `.ipynb` with `jupytext` and execute the notebook
        top to bottom to confirm it runs
- [x] `README.md`: add the two new files to the file table, update
      "Running the Notebooks" with the new notebook as step 3
- [x] `test/test_docker_template.py`: add `test3` running
      `search_algorithms.example.ipynb`, matching `test1`/`test2`
- [x] `git add` all new files (per `.claude/instr.md`, no commit)

## Result

- Done: `search_algorithms_utils.py`, a game-agnostic module (reusing
  `mcts_utils.Game`) implementing all four algorithms, mirroring
  `mcts_utils.py`'s own shape:
  - A `SearchNode` tree class (state/parent/move/children, a backed-up
    `value`, a `pruned` flag, an `is_heuristic` flag) shared by all four
  - `build_minimax_tree()` / `build_alpha_beta_tree()` /
    `build_depth_limited_tree()` / `build_flat_mc_tree()`, `run_*()` /
    `make_*_player()` counterparts, and `pick_best_move()`
  - `build_tree_graph()`: a depth-capped Graphviz renderer (blue explored /
    green terminal / amber heuristic-cut / grey-dashed pruned), shared by
    all four -- this is what "shows how the search tree is built"
  - `mcts_utils.py`: `_simulate` renamed to public `random_rollout()` so
    flat MC reuses MCTS's own default policy, no duplication
  - `game_examples.py`: added `evaluate_tic_tac_toe()`, the heuristic
    depth-limited search's cut nodes use
- Done: `search_algorithms.example.ipynb` / `.py` (8 parts, Jupytext-paired,
  same `demo_state` as `mcts.example.py` Cell 3.1 plus a second `fork_state`
  for Part 5): minimax, alpha-beta (with a real empty-board timing/node-count
  comparison: ~550k vs. ~18k nodes, ~30x), depth-limited search (shown
  missing then, at higher `max_depth`, recovering a forced win), flat Monte
  Carlo, a 5-way comparison table against MCTS, and a full-game sanity check
  - Verified by converting to `.ipynb` with `jupytext` and executing it
    end to end locally (`jupyter nbconvert --execute`) -- 0 error cells,
    values cross-checked by hand; also re-ran the existing
    `mcts.example.ipynb` to confirm the `random_rollout` rename didn't
    break it
  - `ruff` and `pyright` clean on every touched/new file (remaining E402 /
    import-resolution / unused-`_LOG` diagnostics are the same pre-existing
    pattern already present in `mcts.example.py` / `mcts.API.py`)
- Done: `README.md` file table + "Running the Notebooks" step 3;
  `test/test_docker_template.py` `test3` for the new notebook (mirrors
  `test1`/`test2`)
- Not done: no unit tests for `search_algorithms_utils.py` itself -- this
  matches the existing convention in this directory, where `mcts_utils.py`
  and `game_examples.py` also have no dedicated unit tests, only the
  Docker end-to-end notebook test
- Not done: no Connect Four coverage in the new notebook or evaluation
  function -- `mcts.example.py`, whose structure this mirrors, is also
  tic-tac-toe-only; Connect Four support stays in `mcts.API.ipynb`
