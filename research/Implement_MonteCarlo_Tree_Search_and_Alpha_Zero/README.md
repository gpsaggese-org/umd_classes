# Implement Monte Carlo Tree Search and Alpha Zero

This project implements the Monte Carlo Tree Search (MCTS) algorithm and the Alpha
Zero algorithm for game playing

- A game-agnostic MCTS engine (`mcts_utils.py`) plays any two-player, zero-sum,
  perfect-information game exposed through a small `Game` interface

- Two concrete games (`game_examples.py`) plug into that engine:
  - Tic-tac-toe
  - Connect Four

- Two paired notebooks cover, respectively, the engine's API and an end-to-end
  tic-tac-toe demo
[(Plan)](https://github.com/gpsaggese/gpsaggese.github.io/blob/master/research/ideas/draft.Implement_MonteCarlo_Tree_Search_and_Alpha_Zero.md)

## Structure of the Dir

| File    | Description                                                         |
| ------- | ------------------------------------------------------------------- |
| `test/` | Docker-based end-to-end test that runs both notebooks top to bottom |

## Description of Files

// TODO(ai_gp): Shorter

| File                 | Description                                                                                                              | Cluster            |
| -------------------- | ------------------------------------------------------------------------------------------------------------------------ | ------------------ |
| `game_examples.py`   | `Game` implementations for `TicTacToe` and `ConnectFour`, plugged into the MCTS engine                                   | Game Rules         |
| `mcts_API_utils.py`  | Widget and plotting helpers (clickable boards, search-tree diagrams, board pictures) backing `mcts.API.ipynb`            | Notebook Utilities |
| `mcts_utils.py`      | Game-agnostic MCTS engine: the `Game` interface, `MCTSNode`, the UCT search loop, and evaluation helpers                 | Core Engine        |
| `mcts.API.ipynb`     | Interactive API tour of `mcts_utils.py`: `Game`, `MCTSNode`, `run_mcts()`, with widgets for tic-tac-toe and Connect Four | Notebooks          |
| `mcts.API.py`        | Jupytext-paired plain-text mirror of `mcts.API.ipynb`, edited in an IDE and synced back to the notebook                  | Notebooks          |
| `mcts.example.ipynb` | Milestone 1 end-to-end demo: MCTS vs. a random player on tic-tac-toe, no neural network involved                         | Notebooks          |
| `mcts.example.py`    | Jupytext-paired plain-text mirror of `mcts.example.ipynb`, edited in an IDE and synced back to the notebook              | Notebooks          |

## Running the Notebooks

- Build the Docker image:

  ```bash
  > ./docker_build.sh
  ```

- Launch Jupyter inside the container:

  ```bash
  > ./docker_jupyter.sh
  ```

- From the Jupyter file browser, open, in order:
  1. `mcts.API.ipynb`: the engine's API, with interactive widgets for both
     `TicTacToe` and `ConnectFour`
  2. `mcts.example.ipynb`: a full MCTS-vs-random run on tic-tac-toe

- For more information on the Docker build system refer to
  [Project template readme](https://github.com/gpsaggese/umd_classes/blob/master/class_project/project_template/docker_scripts.README.md)
