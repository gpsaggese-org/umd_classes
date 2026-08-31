"""
Adapters that run four third-party MCTS libraries against our own
`TicTacToe` game.

Each `*_player()` function below has the same `(game, state) -> move`
signature as `alphazero_utils.random_player()`, so it can be dropped
directly into `alphazero_utils.play_game()` / `evaluate_win_rate()`.

See `research/ideas/in_progress.Implement_MonteCarlo_Tree_Search_and_Alpha_Zero.md`
for the project spec and `alphazero_utils.py` for the game/MCTS this survey
compares against.

Import as:

import research.Implement_MonteCarlo_Tree_Search_and_Alpha_Zero.mcts_library_survey_utils as rimtsaazmlsu
"""

import logging
import random
from typing import List, Optional

import pandas as pd

import helpers.hdbg as hdbg
import research.Implement_MonteCarlo_Tree_Search_and_Alpha_Zero.alphazero_utils as rimtsaazau

_LOG = logging.getLogger(__name__)

# #############################################################################
# Constants
# #############################################################################


# Simulation budget used for every library, so the head-to-head comparison
# is apples-to-apples.
NUM_SIMULATIONS = 200

# Number of games played against a random opponent when comparing libraries.
NUM_EVAL_GAMES = 30


# #############################################################################
# kstruempf/monte-carlo-tree-search (PyPI: monte-carlo-tree-search)
# #############################################################################


def _build_kstruempf_state(game: rimtsaazau.Game, state: rimtsaazau.State):
    """
    Wrap our `State` in the library's `BaseState` interface.

    :param game: game-agnostic rules implementation
    :param state: game state to wrap
    :return: `mcts.base.base.BaseState` backed by `game`/`state`
    """
    import mcts.base.base as mcts_base

    class _KstruempfState(mcts_base.BaseState):
        def __init__(self, state: rimtsaazau.State) -> None:
            self.state = state

        def get_current_player(self) -> int:
            return game.get_current_player(self.state)

        def get_possible_actions(self) -> List[rimtsaazau.Move]:
            return game.get_legal_moves(self.state)

        def take_action(self, action: rimtsaazau.Move) -> "_KstruempfState":
            return _KstruempfState(game.apply_move(self.state, action))

        def is_terminal(self) -> bool:
            return game.is_terminal(self.state)

        def get_reward(self) -> float:
            return float(game.get_winner(self.state))

    wrapped_state = _KstruempfState(state)
    return wrapped_state


def kstruempf_player(
    game: rimtsaazau.Game, state: rimtsaazau.State
) -> rimtsaazau.Move:
    """
    Choose a move using the `monte-carlo-tree-search` package (PyPI), a
    maintained continuation of int8's original minimal MCTS implementation.

    :param game: game-agnostic rules implementation
    :param state: current game state, must not be terminal
    :return: move chosen by the library's own search
    """
    import mcts.searcher.mcts as mcts_searcher

    searcher = mcts_searcher.MCTS(iteration_limit=NUM_SIMULATIONS)
    move = searcher.search(initial_state=_build_kstruempf_state(game, state))
    return move


# #############################################################################
# mctspy
# #############################################################################


def _build_mctspy_state(game: rimtsaazau.Game, state: rimtsaazau.State):
    """
    Wrap our `State` in the library's `TwoPlayersAbstractGameState` interface.

    :param game: game-agnostic rules implementation
    :param state: game state to wrap
    :return: `mctspy.games.common.TwoPlayersAbstractGameState` backed by
        `game`/`state`
    """
    import mctspy.games.common as mctspy_common

    class _MctspyState(mctspy_common.TwoPlayersAbstractGameState):
        def __init__(self, state: rimtsaazau.State) -> None:
            self.state = state
            # mctspy reads `next_to_move` directly (not via a method).
            self.next_to_move = game.get_current_player(state)

        @property
        def game_result(self) -> Optional[float]:
            if not game.is_terminal(self.state):
                return None
            return float(game.get_winner(self.state))

        def is_game_over(self) -> bool:
            return game.is_terminal(self.state)

        def move(self, action: rimtsaazau.Move) -> "_MctspyState":
            return _MctspyState(game.apply_move(self.state, action))

        def get_legal_actions(self) -> List[rimtsaazau.Move]:
            return game.get_legal_moves(self.state)

    wrapped_state = _MctspyState(state)
    return wrapped_state


def mctspy_player(
    game: rimtsaazau.Game, state: rimtsaazau.State
) -> rimtsaazau.Move:
    """
    Choose a move using `mctspy`, which ships tic-tac-toe/Connect4 examples
    of its own and returns the chosen child node rather than a raw move.

    :param game: game-agnostic rules implementation
    :param state: current game state, must not be terminal
    :return: move chosen by the library's own search
    """
    import mctspy.tree.nodes as mctspy_nodes
    import mctspy.tree.search as mctspy_search

    root = mctspy_nodes.TwoPlayersGameMonteCarloTreeSearchNode(
        _build_mctspy_state(game, state)
    )
    searcher = mctspy_search.MonteCarloTreeSearch(root)
    best_child = searcher.best_action(NUM_SIMULATIONS)
    # `best_action()` returns the chosen child node, not the move that led to
    # it, so recover the move by matching the resulting state.
    move = next(
        candidate_move
        for candidate_move in game.get_legal_moves(state)
        if game.apply_move(state, candidate_move) == best_child.state.state
    )
    return move


# #############################################################################
# mcts-simple
# #############################################################################


def _build_mcts_simple_game(game: rimtsaazau.Game, state: rimtsaazau.State):
    """
    Wrap our `State` in the library's mutable `Game` interface.

    Unlike `alphazero_utils.Game`, `mcts_simple.Game` is stateful:
    `take_action()` mutates the wrapped state in place instead of returning a
    new one, and players are labelled `0`/`1` instead of `1`/`-1`.

    :param game: game-agnostic rules implementation
    :param state: game state to wrap
    :return: `mcts_simple.Game` backed by `game`/`state`
    """
    import mcts_simple

    class _SimpleGame(mcts_simple.Game):
        def __init__(self, state: rimtsaazau.State) -> None:
            self.state = state

        def render(self) -> None:
            print(game.render(self.state))

        def get_state(self) -> rimtsaazau.State:
            return self.state

        def number_of_players(self) -> int:
            return 2

        def current_player(self) -> int:
            return 0 if game.get_current_player(self.state) == 1 else 1

        def possible_actions(self) -> List[rimtsaazau.Move]:
            return game.get_legal_moves(self.state)

        def take_action(self, action: rimtsaazau.Move) -> None:
            self.state = game.apply_move(self.state, action)

        def has_outcome(self) -> bool:
            return game.is_terminal(self.state)

        def winner(self) -> List[int]:
            if not game.is_terminal(self.state):
                return []
            game_winner = game.get_winner(self.state)
            if game_winner == 0:
                return [0, 1]
            return [0] if game_winner == 1 else [1]

    wrapped_game = _SimpleGame(state)
    return wrapped_game


def mcts_simple_player(
    game: rimtsaazau.Game, state: rimtsaazau.State
) -> rimtsaazau.Move:
    """
    Choose a move using `mcts-simple`, which builds its tree through an
    explicit `self_play()` training loop rather than a one-shot search call.

    :param game: game-agnostic rules implementation
    :param state: current game state, must not be terminal
    :return: move chosen by the library's own search
    """
    import mcts_simple

    uct = mcts_simple.UCT(
        _build_mcts_simple_game(game, state),
        training=True,
        seed=random.randint(0, 2**31 - 1),
    )
    uct.self_play(iterations=NUM_SIMULATIONS)
    move = uct.root.choose_best_action(training=False)
    return move


# #############################################################################
# imparaai-montecarlo
# #############################################################################


def imparaai_player(
    game: rimtsaazau.Game, state: rimtsaazau.State
) -> rimtsaazau.Move:
    """
    Choose a move using `imparaai-montecarlo`, which exposes `child_finder`
    and `node_evaluator` hooks so the same engine can run either plain
    rollouts (as here) or a neural-network policy.

    `player_number` must be set to whoever is to move at each node (matching
    `game.get_current_player()`); the library flips win values at
    selection time by comparing a node's `player_number` to the root's,
    rather than negating them during backpropagation.

    :param game: game-agnostic rules implementation
    :param state: current game state, must not be terminal
    :return: move chosen by the library's own search
    """
    import montecarlo.montecarlo as imparaai_montecarlo
    import montecarlo.node as imparaai_node

    def child_finder(
        node: imparaai_node.Node, montecarlo: imparaai_montecarlo.MonteCarlo
    ) -> None:
        for candidate_move in game.get_legal_moves(node.state):
            child_state = game.apply_move(node.state, candidate_move)
            child = imparaai_node.Node(child_state)
            child.player_number = game.get_current_player(child_state)
            child.move = candidate_move
            node.add_child(child)

    def node_evaluator(
        node: imparaai_node.Node, montecarlo: imparaai_montecarlo.MonteCarlo
    ) -> Optional[float]:
        if game.is_terminal(node.state):
            return float(game.get_winner(node.state))
        return None

    root = imparaai_node.Node(state)
    root.player_number = game.get_current_player(state)
    searcher = imparaai_montecarlo.MonteCarlo(root)
    searcher.child_finder = child_finder
    searcher.node_evaluator = node_evaluator
    searcher.simulate(NUM_SIMULATIONS)
    move = searcher.make_choice().move
    return move


# #############################################################################
# Head-to-head comparison
# #############################################################################


# Every library under test, alongside our own MCTS for reference.
LIBRARY_PLAYERS = {
    "alphazero_utils (ours)": rimtsaazau.make_mcts_player(
        num_simulations=NUM_SIMULATIONS
    ),
    "monte-carlo-tree-search": kstruempf_player,
    "mctspy": mctspy_player,
    "mcts-simple": mcts_simple_player,
    "imparaai-montecarlo": imparaai_player,
}


def evaluate_all_libraries(*, num_games: int = NUM_EVAL_GAMES) -> pd.DataFrame:
    """
    Play each library in `LIBRARY_PLAYERS` against a random opponent and
    collect win/draw/loss rates into a single comparison table.

    :param num_games: number of games to play per library
        - Default: `NUM_EVAL_GAMES`
    :return: DataFrame indexed by library name with columns `win_rate`,
        `draw_rate`, `loss_rate`
    """
    hdbg.dassert_lt(0, num_games, "num_games must be positive")
    game = rimtsaazau.TicTacToe()
    rows = {}
    for library_name, player in LIBRARY_PLAYERS.items():
        _LOG.info("Evaluating '%s'", library_name)
        results = rimtsaazau.evaluate_win_rate(
            game,
            player,
            rimtsaazau.random_player,
            num_games=num_games,
            show_progress=False,
        )
        rows[library_name] = {
            "win_rate": results["win_rate"],
            "draw_rate": results["draw_rate"],
            "loss_rate": results["loss_rate"],
        }
    comparison_df = pd.DataFrame(rows).T
    return comparison_df
