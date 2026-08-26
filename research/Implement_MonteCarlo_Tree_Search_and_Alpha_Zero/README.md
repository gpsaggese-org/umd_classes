# Implement Monte Carlo Tree Search and Alpha Zero

This project implements the Monte Carlo Tree Search (MCTS) algorithm and the Alpha
Zero algorithm for game playing

- A game-agnostic `Game` interface (`game.py`) is the contract every search
  algorithm below is built against

- Two concrete games (`game_examples.py`) plug into that interface:
  - Tic-tac-toe
  - Connect Four

- `search_algorithms_utils.py`
  - Classical searches: minimax, alpha-beta pruning, depth-limited search,
    and flat Monte Carlo

- `mcts_utils.py`
  - Game-agnostic MCTS engine: selection, expansion, rollout, backpropagation

## Structure of the Dir

| File    | Description                                                         |
| ------- | ------------------------------------------------------------------- |
| `test/` | Docker-based end-to-end test that runs every notebook top to bottom |

## Description of Files

| File                 | Description                                                | Cluster            |
| -------------------- | ------------------------------------------------------------------------------------------------------------------------ | ------------------ |
| `game.py`            | `Game` interface (`State`, `Move`, 6 abstract methods)      | Core Engine        |
| `game_examples.py`   | `TicTacToe` and `ConnectFour` implementations                | Game Rules         |
| `game_API_utils.py`  | Widget helpers for `game.API.ipynb`                          | Notebook Utilities |
| `game.API.ipynb`     | API tour of `game.py`; frames both games as an AND-OR tree   | Notebooks |
| `mcts_API_utils.py`  | Widget and search-tree plotting helpers for `mcts.API.ipynb` | Notebook Utilities |
| `mcts_utils.py`      | Game-agnostic MCTS engine: `MCTSNode`, `run_mcts()`           | Core Engine        |
| `mcts.API.ipynb`     | API tour of `mcts_utils.py`                                   | Notebooks          |
| `mcts.example.ipynb` | Milestone 1: MCTS vs. a random player on tic-tac-toe          | Notebooks          |
| `search_algorithms_utils.py` | Minimax, alpha-beta, depth-limited search, flat Monte Carlo, and the search-tree renderer | Core Engine |
| `search_algorithms.example.ipynb` | Classical searches on tic-tac-toe, each with its search tree, compared against MCTS | Notebooks |

## Flow of the Notebooks

The four notebooks run as two back-to-back arcs on the same `Game` interface:
- **Search exactly and approximately** (`search_algorithms.example`): solve
  the same game with minimax / alpha-beta / depth-limited search / flat Monte
  Carlo, then compare all of them against MCTS
- **Frame + sample** (`game.API` $\to$ `mcts.API` $\to$ `mcts.example`): define
  a game as a search problem, then solve it by sampling (MCTS)

1. `game.API.ipynb`: the `Game` interface
   - Part 1: Library overview and mental model
   - Part 2: `Game` and `TicTacToe`
   - Part 3: Connect Four (same interface, bigger board)
   - Part 4: Framing the game as a search problem ($s_0$, $Actions$,
     $Result$, $IsTerminal$, $Utility$), naming the tree an AND-OR tree

2. `search_algorithms.example.ipynb`: classical and adversarial search
   - Part 2: The game
   - Part 3: Minimax
   - Part 4: Alpha-beta pruning
   - Part 5: Depth-limited search
   - Part 6: Flat Monte Carlo
   - Part 7: Comparing all four (plus MCTS)
   - Part 8: Full-game sanity check

3. `mcts.API.ipynb`: the MCTS engine
   - Part 1: Library overview and mental model
   - Part 2: `MCTSNode`
   - Part 3: `run_mcts()`
   - Part 4: Composing players and games
   - Part 5: Evaluation API (win rate over games)
   - Part 6: Connect Four (same engine, bigger board)

4. `mcts.example.ipynb`: MCTS end to end
   - Part 2: The game
   - Part 3: MCTS on a single position
   - Part 4: Full games (MCTS vs. random, MCTS vs. MCTS)
   - Part 5: Evaluation (win rate over 300 games)

## Running the Notebooks

- Build the Docker image:

  ```bash
  > ./docker_build.sh
  ```

- Launch Jupyter inside the container:

  ```bash
  > ./docker_jupyter.sh
  ```

- From the Jupyter file browser, open the 4 notebooks in the order listed in
  "Flow of the Notebooks" above

- For more information on the Docker build system refer to
  [Project template readme](https://github.com/gpsaggese/umd_classes/blob/master/class_project/project_template/docker_scripts.README.md)
