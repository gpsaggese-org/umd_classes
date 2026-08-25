"""
Monte Carlo Tree Search (MCTS): a game-agnostic tree search engine.

Defines the `Game` interface and the MCTS algorithm (selection, expansion,
rollout, backpropagation) used to play any two-player, zero-sum,
perfect-information game against it. See `game_examples.py` for concrete
`Game` implementations (tic-tac-toe, Connect Four) and
`research/ideas/draft.Implement_MonteCarlo_Tree_Search_and_Alpha_Zero.md` for
the full project spec.

Import as:

import research.Implement_MonteCarlo_Tree_Search_and_Alpha_Zero.mcts_utils as rimtsaazmu
"""

import abc
import logging
import math
import random
from typing import Callable, Dict, List, Optional, Tuple

import matplotlib.pyplot as plt
import numpy as np
import tqdm

import helpers.hdbg as hdbg

_LOG = logging.getLogger(__name__)

# A game state is a flat tuple of cell values and a move is an integer
# identifying the action (e.g., a cell index or a column); see
# `game_examples.py` for concrete `Game` implementations.
State = Tuple[int, ...]
Move = int

# #############################################################################
# Constants
# #############################################################################


# Exploration constant `C` in the UCT formula: higher values favor trying
# less-visited moves over exploiting the current best estimate.
EXPLORATION_CONSTANT = math.sqrt(2)

# Default number of MCTS simulations run per move when the caller does not
# override it.
DEFAULT_NUM_SIMULATIONS = 500


# #############################################################################
# Game
# #############################################################################


class Game(abc.ABC):
    """
    Game-agnostic interface for a two-player, zero-sum, perfect-information
    game usable by MCTS.

    A concrete game (e.g., `TicTacToe`, later Connect Four) implements these
    six methods; `run_mcts()` and the rest of the search code only depend on
    this interface, so a new game can be plugged in without touching the
    search logic. Players are represented as `1` and `-1`; a draw is `0`.
    """

    @abc.abstractmethod
    def get_initial_state(self) -> State:
        """
        Build the starting state of a new game.

        :return: initial game state
        """

    @abc.abstractmethod
    def get_legal_moves(self, state: State) -> List[Move]:
        """
        List the moves available from `state`.

        :param state: game state to query
        :return: legal moves, empty if `state` is terminal
        """

    @abc.abstractmethod
    def apply_move(self, state: State, move: Move) -> State:
        """
        Apply `move` to `state` and return the resulting state.

        :param state: game state before the move
        :param move: move to apply, must be legal in `state`
        :return: new game state after the move
        """

    @abc.abstractmethod
    def is_terminal(self, state: State) -> bool:
        """
        Check whether `state` ends the game.

        :param state: game state to query
        :return: True if no more moves can be made from `state`
        """

    @abc.abstractmethod
    def get_winner(self, state: State) -> int:
        """
        Determine the outcome of a terminal state.

        :param state: terminal game state
        :return: `1` or `-1` for the winning player, `0` for a draw
        """

    @abc.abstractmethod
    def get_current_player(self, state: State) -> int:
        """
        Report whose turn it is to move in `state`.

        :param state: game state to query
        :return: `1` or `-1`
        """

    @abc.abstractmethod
    def render(self, state: State) -> str:
        """
        Render `state` as a human-readable board.

        :param state: game state to render
        :return: printable board representation
        """


# #############################################################################
# MCTSNode
# #############################################################################


class MCTSNode:
    """
    A single node in the MCTS search tree.

    Tracks the game state it represents, its position in the tree, and the
    running visit count / value total used by the UCT formula.
    """

    def __init__(
        self,
        state: State,
        *,
        parent: Optional["MCTSNode"] = None,
        move: Optional[Move] = None,
        untried_moves: Optional[List[Move]] = None,
    ) -> None:
        """
        Initialize a node for `state`.

        :param state: game state this node represents
        :param parent: predecessor node in the tree
            - Default: `None` (root node)
        :param move: move applied to `parent` to reach `state`
            - Default: `None` (root node)
        :param untried_moves: legal moves from `state` not yet expanded
            - Default: `None` (treated as no moves, e.g., a terminal state)
        """
        self.state = state
        self.parent = parent
        self.move = move
        self.children: Dict[Move, "MCTSNode"] = {}
        self.visit_count = 0
        self.value_sum = 0.0
        self.untried_moves: List[Move] = list(untried_moves or [])

    @property
    def is_fully_expanded(self) -> bool:
        """
        Check whether every legal move from this node already has a child.
        """
        fully_expanded = not self.untried_moves
        return fully_expanded

    @property
    def mean_value(self) -> float:
        """
        Average simulation outcome observed through this node so far.
        """
        mean = self.value_sum / self.visit_count if self.visit_count else 0.0
        return mean

    def __str__(self) -> str:
        """
        Return a human-readable summary of the node for debugging/logging.

        :return: node summary, e.g.,
            "MCTSNode(move=3, visits=12, mean_value=0.42, children=2,
            untried=1)"
        """
        txt = (
            "MCTSNode(move=%s, visits=%d, mean_value=%.2f, children=%d,"
            " untried=%d)"
            % (
                self.move,
                self.visit_count,
                self.mean_value,
                len(self.children),
                len(self.untried_moves),
            )
        )
        return txt


# #############################################################################
# MCTS phases
# #############################################################################


def _uct_score(
    child: MCTSNode,
    parent_visit_count: int,
    *,
    exploration_constant: float = EXPLORATION_CONSTANT,
) -> float:
    """
    Score a child node using the UCT formula:
    `Q/N + C * sqrt(ln(N_parent) / N)`.

    An unvisited child gets an infinite score so every move is tried at least
    once before any move is revisited.

    :param child: candidate child node
    :param parent_visit_count: visit count of the parent node
    :param exploration_constant: the `C` in the UCT formula, trades off
        exploration (higher) against exploitation (lower)
        - Default: `EXPLORATION_CONSTANT`
    :return: UCT score, higher is more promising to explore
    """
    if child.visit_count == 0:
        score = math.inf
    else:
        exploitation = child.mean_value
        exploration = exploration_constant * math.sqrt(
            math.log(parent_visit_count) / child.visit_count
        )
        score = exploitation + exploration
    return score


def _select(
    node: MCTSNode,
    game: Game,
    *,
    exploration_constant: float = EXPLORATION_CONSTANT,
) -> MCTSNode:
    """
    Descend the tree from `node`, following the highest-UCT child at each
    step, until reaching a node that still has untried moves or is terminal.

    :param node: node to start the descent from (typically the root)
    :param game: game rules, used to check terminality
    :param exploration_constant: the `C` in the UCT formula, forwarded to
        `_uct_score()`
        - Default: `EXPLORATION_CONSTANT`
    :return: node ready for expansion (or simulation, if terminal)
    """
    while not game.is_terminal(node.state) and node.is_fully_expanded:
        node = max(
            node.children.values(),
            key=lambda child: _uct_score(
                child, node.visit_count, exploration_constant=exploration_constant
            ),
        )
    return node


def _expand(node: MCTSNode, game: Game) -> MCTSNode:
    """
    Add one new child to `node` for a randomly chosen untried move.

    :param node: node with at least one untried move
    :param game: game rules, used to apply the move
    :return: newly created child node
    """
    move_idx = random.randrange(len(node.untried_moves))
    move = node.untried_moves.pop(move_idx)
    child_state = game.apply_move(node.state, move)
    child = MCTSNode(
        child_state,
        parent=node,
        move=move,
        untried_moves=game.get_legal_moves(child_state),
    )
    node.children[move] = child
    return child


def _simulate(game: Game, state: State) -> int:
    """
    Play out `state` to a terminal state using uniformly random moves.

    :param game: game rules, used to generate and apply moves
    :param state: state to roll out from
    :return: outcome of the rollout: `1`, `-1`, or `0` for a draw
    """
    while not game.is_terminal(state):
        moves = game.get_legal_moves(state)
        move = random.choice(moves)
        state = game.apply_move(state, move)
    winner = game.get_winner(state)
    return winner


def _backpropagate(node: MCTSNode, value: float) -> None:
    """
    Propagate a simulation result up the tree to the root.

    `value` is the outcome from the perspective of the player who made the
    move leading into `node`. Since players alternate at every ply, that
    perspective flips (the sign is negated) at each step up the tree.

    :param node: node the simulation was run from
    :param value: simulation outcome (`1.0` win / `-1.0` loss / `0.0` draw)
        from the perspective of the player who moved into `node`
    """
    current: Optional[MCTSNode] = node
    while current is not None:
        current.visit_count += 1
        current.value_sum += value
        value = -value
        current = current.parent


# #############################################################################
# Public API
# #############################################################################


def build_mcts_tree(
    game: Game,
    state: State,
    *,
    num_simulations: int = DEFAULT_NUM_SIMULATIONS,
    exploration_constant: float = EXPLORATION_CONSTANT,
) -> MCTSNode:
    """
    Run MCTS from `state` and return the fully-built search tree.

    Runs `num_simulations` iterations of selection, expansion, random-rollout
    simulation, and backpropagation from a fresh root, then returns that
    root node itself, rather than only the best move: `run_mcts()` picks the
    best move from it, and a notebook can instead inspect the tree (e.g., to
    visualize visit counts and mean values per child).

    :param game: game-agnostic rules implementation
    :param state: state to search from, must not be terminal
    :param num_simulations: number of MCTS iterations to run
        - Default: `DEFAULT_NUM_SIMULATIONS`
    :param exploration_constant: the `C` in the UCT formula, forwarded to
        `_select()`
        - Default: `EXPLORATION_CONSTANT`
    :return: root node of the search tree, with `num_simulations` simulations
        backpropagated through it
    """
    hdbg.dassert(
        not game.is_terminal(state), "Cannot run MCTS from a terminal state"
    )
    root = MCTSNode(state, untried_moves=game.get_legal_moves(state))
    for _ in range(num_simulations):
        leaf = _select(root, game, exploration_constant=exploration_constant)
        if not game.is_terminal(leaf.state):
            leaf = _expand(leaf, game)
        winner = _simulate(game, leaf.state)
        # `value` must be from the perspective of the player who moved into
        # `leaf`, i.e., the opponent of the player to move at `leaf.state`.
        mover_into_leaf = -game.get_current_player(leaf.state)
        if winner == 0:
            value = 0.0
        elif winner == mover_into_leaf:
            value = 1.0
        else:
            value = -1.0
        _backpropagate(leaf, value)
    return root


def run_mcts(
    game: Game,
    state: State,
    *,
    num_simulations: int = DEFAULT_NUM_SIMULATIONS,
    exploration_constant: float = EXPLORATION_CONSTANT,
) -> Move:
    """
    Run MCTS from `state` and return the most-visited move at the root.

    Builds the search tree via `build_mcts_tree()`, then returns the root
    child with the highest visit count (the standard, low-variance choice,
    as opposed to the child with the highest mean value).

    :param game: game-agnostic rules implementation
    :param state: state to search from, must not be terminal
    :param num_simulations: number of MCTS iterations to run
        - Default: `DEFAULT_NUM_SIMULATIONS`
    :param exploration_constant: the `C` in the UCT formula, trades off
        exploration (higher) against exploitation (lower)
        - Default: `EXPLORATION_CONSTANT`
    :return: move with the highest visit count at the root
    """
    root = build_mcts_tree(
        game,
        state,
        num_simulations=num_simulations,
        exploration_constant=exploration_constant,
    )
    best_move = max(root.children.items(), key=lambda item: item[1].visit_count)[
        0
    ]
    return best_move


def random_player(game: Game, state: State) -> Move:
    """
    Select a uniformly random legal move.

    Matches the `(game, state) -> move` signature expected by `play_game()`.

    :param game: game-agnostic rules implementation
    :param state: current game state, must not be terminal
    :return: randomly chosen legal move
    """
    moves = game.get_legal_moves(state)
    hdbg.dassert(moves, "No legal moves available to choose from")
    move = random.choice(moves)
    return move


def make_mcts_player(
    *, num_simulations: int = DEFAULT_NUM_SIMULATIONS
) -> Callable[[Game, State], Move]:
    """
    Build a `(game, state) -> move` player function backed by MCTS.

    :param num_simulations: number of MCTS simulations to run per move
        - Default: `DEFAULT_NUM_SIMULATIONS`
    :return: player function suitable for `play_game()`
    """

    def player(game: Game, state: State) -> Move:
        move = run_mcts(game, state, num_simulations=num_simulations)
        return move

    return player


def play_game(
    game: Game,
    player1: Callable[[Game, State], Move],
    player2: Callable[[Game, State], Move],
    *,
    verbose: bool = False,
) -> Tuple[int, List[State]]:
    """
    Play one full game between two players, alternating moves.

    :param game: game-agnostic rules implementation
    :param player1: move-selection function for player `1`
    :param player2: move-selection function for player `-1`
    :param verbose: if True, print the board after every move
        - Default: `False`
    :return: tuple `(winner, history)`
        - `winner`: `1`, `-1`, or `0` for a draw
        - `history`: states visited, from the initial state to the terminal
          state (inclusive)
    """
    state = game.get_initial_state()
    history = [state]
    players = {1: player1, -1: player2}
    if verbose:
        print(game.render(state))
    while not game.is_terminal(state):
        current_player = game.get_current_player(state)
        move = players[current_player](game, state)
        state = game.apply_move(state, move)
        history.append(state)
        if verbose:
            print()
            print(game.render(state))
    winner = game.get_winner(state)
    return winner, history


def evaluate_win_rate(
    game: Game,
    player_under_test: Callable[[Game, State], Move],
    opponent: Callable[[Game, State], Move],
    *,
    num_games: int = 200,
    show_progress: bool = True,
) -> Dict[str, float]:
    """
    Play many games of `player_under_test` (as player `1`) against
    `opponent` (as player `-1`) and report outcome statistics.

    :param game: game-agnostic rules implementation
    :param player_under_test: move-selection function to evaluate, plays as
        player `1`
    :param opponent: move-selection function to evaluate against, plays as
        player `-1`
    :param num_games: number of games to play
        - Default: `200`
    :param show_progress: if True, display a `tqdm` progress bar
        - Default: `True`
    :return: dict with keys `num_games`, `win_rate`, `loss_rate`, `draw_rate`
        (rates measured from `player_under_test`'s perspective)
    """
    outcomes = np.zeros(num_games)
    game_range = tqdm.trange(num_games) if show_progress else range(num_games)
    for i in game_range:
        winner, _ = play_game(game, player_under_test, opponent)
        outcomes[i] = winner
    results = {
        "num_games": float(num_games),
        "win_rate": float(np.mean(outcomes == 1)),
        "loss_rate": float(np.mean(outcomes == -1)),
        "draw_rate": float(np.mean(outcomes == 0)),
    }
    return results


def plot_win_rate_results(
    results: Dict[str, float], *, figsize: Optional[Tuple[int, int]] = None
) -> None:
    """
    Plot a bar chart of win / draw / loss rates from `evaluate_win_rate()`.

    :param results: dict as returned by `evaluate_win_rate()`
    :param figsize: figure size passed to `plt.subplots()`
        - Default: `None` (uses `plt.rcParams["figure.figsize"]`)
    """
    if figsize is None:
        figsize = plt.rcParams["figure.figsize"]
    labels = ["win", "draw", "loss"]
    rates = [results["win_rate"], results["draw_rate"], results["loss_rate"]]
    colors = ["#4C9A2A", "#B0B0B0", "#C0392B"]
    _, ax = plt.subplots(figsize=figsize)
    bars = ax.bar(labels, rates, color=colors)
    ax.set_ylim(0, 1)
    ax.set_ylabel("Fraction of games")
    ax.set_title(f"MCTS vs. random over {int(results['num_games'])} games")
    for bar, rate in zip(bars, rates):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            rate + 0.02,
            f"{rate:.1%}",
            ha="center",
        )
    plt.show()
