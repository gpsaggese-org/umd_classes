# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.19.5
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %% [markdown]
# # Monte Carlo Tree Search (MCTS) Engine API
#
# A guided tour of the game-agnostic MCTS engine in `mcts_utils.py`:
# - `Game`: the 6-method interface any two-player, zero-sum game implements
# - `MCTSNode`: one node of the search tree (visit count, value, children)
# - `run_mcts()`: selection -> expansion -> rollout -> backpropagation, repeated
# - `play_game()` / `evaluate_win_rate()`: compose player functions into games
#   and games into statistics
#
# The concrete game used throughout is `TicTacToe` from `game_examples.py`
#
# Part 7 swaps in `ConnectFour` to show that the engine itself never changes.

# %% [markdown]
# ## Imports

# %%
# %load_ext autoreload
# %autoreload 2

import logging

import helpers.hdbg as hdbg
import helpers.hnotebook as hnotebook

_LOG = logging.getLogger(__name__)

hdbg.init_logger(verbosity=logging.INFO)
hnotebook.config_notebook()

# %%
# The base image runs `apt-get update && ... && rm -rf /var/lib/apt/lists/*`
# at build time, which deletes the package-list cache; without a fresh
# `apt-get update` here, `apt-get install` below fails to find `graphviz`
# (silently, from the notebook's point of view) and only the Python bindings
# get installed, leaving the `dot` binary missing.
# !apt-get update --quiet
# !apt-get install --quiet --yes --no-install-recommends graphviz
# !/bin/bash -c "(source /venv/bin/activate; pip install --quiet graphviz)"

# %%
import random

import helpers.hintrospection as hintros
import research.Implement_MonteCarlo_Tree_Search_and_Alpha_Zero.game_examples as rimtsaazge
import research.Implement_MonteCarlo_Tree_Search_and_Alpha_Zero.mcts_API_utils as rimtsaazmau
import research.Implement_MonteCarlo_Tree_Search_and_Alpha_Zero.mcts_utils as rimtsaazmu

# %% [markdown]
# # Part 1: Library Overview
#
# ## What problem does `mcts_utils.py` solve?
#
# - Pick a good move in a two-player game without a hand-written evaluation
#   function, by running many random-rollout simulations from each candidate
#   move and leveraging the law of large numbers
# - Balance trying new moves (exploration) against refining promising ones
#   (exploitation) via the UCT formula
# - Stay game-agnostic: the search code only calls the 6 `Game` methods, so a
#   new game plugs in without touching `mcts_utils.py`
#
# ## Mental model
#
# | Object | Description | Type / Comments |
# |--------|-------------|------------------|
# | `Game` | Game-rules interface | ABC with 6 abstract methods |
# | `State` | A board position | `Tuple[int, ...]`, game-specific layout |
# | `Move` | An action | `int` (cell index, column, ...) |
# | `MCTSNode` | One tree node | tracks `state`, `children`, `visit_count`, `value_sum` |
# | `build_mcts_tree(game, state)` | Search primitive | returns the built root `MCTSNode` for inspection |
# | `run_mcts(game, state)` | Search entry point | returns the most-visited `Move` at the root |
# | `random_player(game, state)` | Uniform-random player | matches the player-function signature |
# | `make_mcts_player(...)` | MCTS player factory | returns a player function backed by `run_mcts()` |
# | `play_game(game, p1, p2)` | Play one game | alternates two player functions to a terminal state |
# | `evaluate_win_rate(...)` | Play many games | returns win/draw/loss rates |
# | `plot_win_rate_results(...)` | Visualize `evaluate_win_rate()` | bar chart |

# %% [markdown]
# # Part 2: `Game`
#
# **Mental model**: `Game` is the contract between a game's rules and the
# search code
# - anything implementing its 6 methods can be searched by `run_mcts()`
# - `TicTacToe` (from `game_examples.py`) is the concrete example used below.

# %%
# Link to the interface definition and list its abstract methods.
hintros.print_obj_info(rimtsaazmu.Game)

# %% [markdown]
# ## Cell 2.1: Construct a `TicTacToe` game and its initial state

# %%
# Link to the concrete implementation.
hintros.print_obj_info(rimtsaazge.TicTacToe)

# %%
game = rimtsaazge.TicTacToe()
state = game.get_initial_state()
print(f"Type: {type(game)}")
# Print the internal state.
print(f"State: {state}")
# Visualize the game.
print(game.render(state))

# %% [markdown]
# ## Cell 2.2: The `Game` methods

# %%
legal_moves = game.get_legal_moves(state)
print("Legal moves from the empty board:", legal_moves)

# %%
state = game.apply_move(state, 4)
print("After X plays the center cell:")
print(game.render(state))

# %%
print("is_terminal:", game.is_terminal(state))
print("current player to move:", game.get_current_player(state))

# %% [markdown]
# ## Cell 2.3: A full game without MCTS
#
# **Goal**:
# - Play a full tic-tac-toe game using only the `Game` methods
# - See `X` and `O` alternate turns via `get_current_player()`, with no
#   search involved yet: each move is picked uniformly at random

# %%
random.seed(0)
demo_game_state = game.get_initial_state()
first_player = game.get_current_player(demo_game_state)
print(f"The first player is: {first_player}")
cnt = 0
while not game.is_terminal(demo_game_state):
    cnt += 1
    # Find the legal moves.
    legal_moves = game.get_legal_moves(demo_game_state)
    current_player = game.get_current_player(demo_game_state)
    # Pick a move at random.
    move = random.choice(legal_moves)
    demo_game_state = game.apply_move(demo_game_state, move)
    print(f"\nAfter move #{cnt}: {move} by {current_player}, state:\n{game.render(demo_game_state)}")
winner = game.get_winner(demo_game_state)
print("\nwinner:", winner)

# %% [markdown]
# ## Cell 2.4: Play tic-tac-toe yourself
#
# **Goal**:
# - Play both `X` and `O` by clicking cells, using the same `Game` methods
#   as Cell 2.3, this time driven by mouse clicks instead of `random.choice()`

# %%
rimtsaazmau.cell2_4_build_play_widget(game)

# %% [markdown]
# # Part 3: `MCTSNode`
#
# **Mental model**:
# - each `MCTSNode` wraps one `State` plus the running statistics (`visit_count`,
#   `value_sum`) the UCT formula needs
# - `run_mcts()` grows a tree of these nodes rooted at the state being searched.
#
# ## Cell 3.1: Construct a node directly

# %%
hintros.print_obj_info(rimtsaazmu.MCTSNode)

# %%
root = rimtsaazmu.MCTSNode(
    game.get_initial_state(), untried_moves=game.get_legal_moves(state)
)
print(f"Type: {type(root)}")
print("visit_count:", root.visit_count)
print("is_fully_expanded:", root.is_fully_expanded)
print("mean_value (no visits yet):", root.mean_value)

# %% [markdown]
# ## Cell 3.2: A node's stats update as simulations backpropagate through it
#
# - `run_mcts()` mutates a tree of nodes like `root` in place
# - a node visited once with a win backpropagated has `visit_count == 1` and `mean_value == 1.0`.

# %%
root.visit_count += 1
root.value_sum += 1.0
print("visit_count:", root.visit_count)
print("mean_value:", root.mean_value)

# %%
print(root)

# %% [markdown]
# # Part 4: `run_mcts()`
#
# **Mental model**:
# - `run_mcts()` runs `num_simulations` rounds of
#   select/expand/rollout/backpropagate from `state`
# - then returns the root child with the highest visit count.
#
# ## Cell 4.1: Find an immediate winning move
#
# X already has two in a row; playing the third cell wins immediately.

# %%
demo_state = (1, 1, 0, -1, -1, 0, 0, 0, 0)
print(game.render(demo_state))

# %%
move = rimtsaazmu.run_mcts(game, demo_state, num_simulations=200)
print("MCTS move:", move)

# %%
# TODO(ai_gp): Print state

# %% [markdown]
# ## Cell 4.2: Visualizing the search tree
#
# **Goal**:
# - See the actual search tree `run_mcts()` builds from `demo_state`: the
#   root and its immediate children, annotated with visit count `N` and mean
#   value `Q`
# - Control the two knobs from the UCT formula
#   ($Q/N + C \sqrt{\ln N(s) / N(s, a)}$) and watch how the visit counts
#   respond:
#   - `num_simulations`: the search budget
#   - `C`: the exploration constant (theory suggests $C = \sqrt{2}$ for
#     rewards in $[0, 1]$)
# - Increasing `num_simulations` is literally "how MCTS nodes are updated":
#   each simulation runs one more selection/expansion/rollout/backpropagation
#   pass and adds to the `visit_count` / `value_sum` of every node it touches

# %%
rimtsaazmau.cell4_2_build_tree_widget(game, demo_state)

# %% [markdown]
# ## Cell 4.3: The exploration/simulation-count knobs

# %%
print("EXPLORATION_CONSTANT (the `C` in UCT):", rimtsaazmu.EXPLORATION_CONSTANT)
print("DEFAULT_NUM_SIMULATIONS:", rimtsaazmu.DEFAULT_NUM_SIMULATIONS)

# %%
hintros.print_obj_info(rimtsaazmu.run_mcts)

# %% [markdown]
# # Part 5: Composing players and games
#
# **Mental model**: a "player" is any `(game, state) -> Move` function;
# `play_game()` alternates two of them until the board is terminal, so a
# uniformly-random player and an MCTS-backed player are interchangeable.
#
# ## Cell 5.1: `random_player` and `make_mcts_player()`

# %%
mcts_player = rimtsaazmu.make_mcts_player(num_simulations=100)
print("random_player move:", rimtsaazmu.random_player(game, state))
print("mcts_player move:", mcts_player(game, state))

# %% [markdown]
# ## Cell 5.2: `play_game()` runs one full game

# %%
winner, history = rimtsaazmu.play_game(
    game, mcts_player, rimtsaazmu.random_player
)
print("winner:", winner)
print("number of states visited:", len(history))
print(game.render(history[-1]))

# %%
hintros.print_obj_info(rimtsaazmu.play_game)

# %% [markdown]
# # Part 6: Evaluation API
#
# **Mental model**: `evaluate_win_rate()` calls `play_game()` many times and
# reports outcome rates; `plot_win_rate_results()` turns that dict into a bar
# chart.
#
# ## Cell 6.1: Win rate over 100 games

# %%
results = rimtsaazmu.evaluate_win_rate(
    game, mcts_player, rimtsaazmu.random_player, num_games=100
)
print(results)

# %% [markdown]
# ## Cell 6.2: Plot the results

# %%
rimtsaazmu.plot_win_rate_results(results)

# %% [markdown]
# # Part 7: Swapping in a different `Game`
#
# **Mental model**: none of Parts 3-6 mentioned `TicTacToe` by name; the same
# `run_mcts()` / `play_game()` code works unchanged against `ConnectFour`,
# because both only go through the `Game` interface.
#
# ## Cell 7.1: The same engine, a different game

# %%
connect_four = rimtsaazge.ConnectFour()
cf_state = connect_four.get_initial_state()
cf_mcts_player = rimtsaazmu.make_mcts_player(num_simulations=100)

move = rimtsaazmu.run_mcts(connect_four, cf_state, num_simulations=100)
print("MCTS move on an empty Connect Four board (column):", move)

winner, history = rimtsaazmu.play_game(
    connect_four, cf_mcts_player, rimtsaazmu.random_player
)
print("\nwinner:", winner)
print(connect_four.render(history[-1]))
