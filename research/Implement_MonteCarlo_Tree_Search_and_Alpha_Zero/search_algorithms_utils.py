"""
Classical adversarial search: minimax, alpha-beta pruning, depth-limited
search, and flat Monte Carlo.

All four algorithms plug into the same game-agnostic `Game` interface that
`mcts_utils.py`'s MCTS engine uses (see `game.Game` and `game_examples.py`
for concrete games).

See `README.md` for a description of every file in this directory.

Import as:

import research.Implement_MonteCarlo_Tree_Search_and_Alpha_Zero.search_algorithms_utils as rimtsaazsau
"""

# Value convention: unlike `MCTSNode.value_sum` (which is stored from the
# perspective of the player who moved into that node, flipping sign at every
# level during backpropagation), `SearchNode.value` below is always the
# classical minimax convention: the exact or estimated outcome from player
# `1` (X)'s perspective, in `{-1, 0, 1}` (or, at a depth-limited cut, a
# heuristic estimate in `[-1, 1]`). A node alternates between taking the `max`
# (player `1` to move) and the `min` (player `-1` to move) of its children's
# values, which is equivalent to sign-flipping but needs no extra bookkeeping
# since `Game.get_current_player()` already reports whose turn it is.


import logging
import math
from typing import TYPE_CHECKING, Callable, List, Optional, Tuple, cast

if TYPE_CHECKING:
    import graphviz

import helpers.hdbg as hdbg
import research.Implement_MonteCarlo_Tree_Search_and_Alpha_Zero.game as rimtsaazg
import research.Implement_MonteCarlo_Tree_Search_and_Alpha_Zero.mcts_utils as rimtsaazmu

_LOG = logging.getLogger(__name__)

# #############################################################################
# Constants
# #############################################################################


# Default depth cut for depth-limited search (Lesson09.8's "Phase 2:
# Expansion" / "Depth-limited search" use a small cut so the evaluation
# function, not exhaustive search, does most of the work).
DEFAULT_MAX_DEPTH = 2

# Default number of random playouts per root action for flat Monte Carlo
# (Lesson09.8: "For each action a at s0: Run N random playouts").
DEFAULT_NUM_ROLLOUTS = 200

# Default number of tree levels rendered by `build_tree_graph()`.
DEFAULT_RENDER_DEPTH = 2


# #############################################################################
# SearchNode
# #############################################################################


class SearchNode:
    """
    A node of a fully-materialized search tree.

    Unlike `mcts_utils.MCTSNode` (which grows one node per simulation),
    minimax, alpha-beta, and depth-limited search each visit (or, for a
    pruned branch, at least record) every node of the tree they build in a
    single recursive pass, so this node stores the backed-up `value`
    directly rather than a running `visit_count` / `value_sum`.
    """

    def __init__(
        self,
        state: rimtsaazg.State,
        *,
        parent: Optional["SearchNode"] = None,
        move: Optional[rimtsaazg.Move] = None,
    ) -> None:
        """
        Initialize a node for `state`.

        :param state: game state this node represents
        :param parent: predecessor node in the tree
            - Default: `None` (root node)
        :param move: move applied to `parent` to reach `state`
            - Default: `None` (root node)
        """
        self.state = state
        self.parent = parent
        self.move = move
        self.children: List["SearchNode"] = []
        # Backed-up value: exact in `{-1, 0, 1}` for minimax/alpha-beta, a
        # heuristic estimate in `[-1, 1]` at a depth-limited cut, or
        # `Q_hat(state, move)` for a flat Monte Carlo child. `None` until
        # computed, and stays `None` for a pruned node (see below).
        self.value: Optional[float] = None
        # True once alpha-beta proves this branch cannot affect the result;
        # a pruned node is recorded (so the diagram can show what was
        # skipped) but never expanded, so it has no children and no value.
        self.pruned = False
        # True when `value` is a depth-limited cut's heuristic estimate,
        # rather than an exact backed-up or terminal value.
        self.is_heuristic = False

    @property
    def node_count(self) -> int:
        """
        Count this node and every descendant recorded in the tree.

        Includes pruned placeholder nodes, so `node_count` measures the
        shape of the full tree the algorithm reasoned about, as opposed to
        `num_explored_nodes` below.
        """
        count = 1 + sum(child.node_count for child in self.children)
        return count

    @property
    def num_explored_nodes(self) -> int:
        """
        Count this node and every descendant actually evaluated.

        Excludes pruned nodes (and, transitively, everything under them,
        which is empty anyway since a pruned node is never expanded). For
        minimax and depth-limited search, where nothing is ever pruned,
        this equals `node_count`; for alpha-beta the gap between the two is
        the whole point (Lesson09.8: alpha-beta "can drop to `O(b^{d/2})`").
        """
        if self.pruned:
            count = 0
        else:
            count = 1 + sum(
                child.num_explored_nodes for child in self.children
            )
        return count

    def add_child(
        self, move: rimtsaazg.Move, state: rimtsaazg.State
    ) -> "SearchNode":
        """
        Append and return a new child of `move` -> `state`.

        :param move: move applied to reach `state`
        :param state: resulting game state
        :return: the newly created child node
        """
        child = SearchNode(state, parent=self, move=move)
        self.children.append(child)
        return child

    def __str__(self) -> str:
        """
        Return a human-readable summary of the node for debugging/logging.

        :return: node summary, e.g., "SearchNode(move=3, value=1.00,
            children=2, pruned=False)"
        """
        txt = "SearchNode(move=%s, value=%s, children=%d, pruned=%s)" % (
            self.move,
            f"{self.value:.2f}" if self.value is not None else None,
            len(self.children),
            self.pruned,
        )
        return txt


# #############################################################################
# Minimax
# #############################################################################


def _minimax(node: SearchNode, game: rimtsaazg.Game) -> float:
    """
    Recursively back up the exact minimax value of `node.state`.

    Lesson09.8: "minimax computes the value of a state by backing terminal
    values up the tree"; every legal move is explored, so the cost is
    `O(b^d)`.

    :param node: node to expand and score, `.children` populated in place
    :param game: game-agnostic rules implementation
    :return: minimax value of `node.state` from X's perspective
    """
    state = node.state
    if game.is_terminal(state):
        value = float(game.get_winner(state))
    else:
        current_player = game.get_current_player(state)
        values = []
        for move in game.get_legal_moves(state):
            child_state = game.apply_move(state, move)
            child = node.add_child(move, child_state)
            values.append(_minimax(child, game))
        value = max(values) if current_player == 1 else min(values)
    node.value = value
    return value


def build_minimax_tree(
    game: rimtsaazg.Game, state: rimtsaazg.State
) -> SearchNode:
    """
    Run exact minimax from `state` and return the fully-built search tree.

    :param game: game-agnostic rules implementation
    :param state: state to search from, must not be terminal
    :return: root node, with every descendant's `.value` backed up
    """
    hdbg.dassert(
        not game.is_terminal(state), "Cannot search from a terminal state"
    )
    root = SearchNode(state)
    _minimax(root, game)
    return root


def run_minimax(game: rimtsaazg.Game, state: rimtsaazg.State) -> rimtsaazg.Move:
    """
    Run exact minimax from `state` and return the best move at the root.

    :param game: game-agnostic rules implementation
    :param state: state to search from, must not be terminal
    :return: move maximizing (minimizing) the root value for player `1`
        (`-1`)
    """
    root = build_minimax_tree(game, state)
    best_move = pick_best_move(game, root)
    return best_move


def make_minimax_player() -> Callable[[rimtsaazg.Game, rimtsaazg.State], rimtsaazg.Move]:
    """
    Build a `(game, state) -> move` player function backed by minimax.

    :return: player function suitable for `mcts_utils.play_game()`
    """

    def player(game: rimtsaazg.Game, state: rimtsaazg.State) -> rimtsaazg.Move:
        move = run_minimax(game, state)
        return move

    return player


# #############################################################################
# Alpha-beta pruning
# #############################################################################


def _alpha_beta(
    node: SearchNode, game: rimtsaazg.Game, alpha: float, beta: float
) -> float:
    """
    Recursively back up the minimax value of `node.state`, skipping any
    remaining sibling once its value can no longer change the result.

    Lesson09.8: `alpha` is the best value the maximizing player can already
    guarantee, `beta` the best value the minimizing player can already
    guarantee; once `alpha >= beta`, the rest of the current node's
    children are "proven worse than a move already found" and are recorded
    as pruned rather than explored.

    :param node: node to expand and score, `.children` populated in place
    :param game: game-agnostic rules implementation
    :param alpha: best value the maximizing player can already guarantee
        on the path to `node`
    :param beta: best value the minimizing player can already guarantee on
        the path to `node`
    :return: minimax value of `node.state` from X's perspective
    """
    state = node.state
    if game.is_terminal(state):
        value = float(game.get_winner(state))
        node.value = value
        return value
    current_player = game.get_current_player(state)
    is_maximizing = current_player == 1
    value = -math.inf if is_maximizing else math.inf
    pruning = False
    for move in game.get_legal_moves(state):
        child_state = game.apply_move(state, move)
        child = node.add_child(move, child_state)
        if pruning:
            # A cutoff already happened among this node's earlier children:
            # record the remaining moves without exploring them.
            child.pruned = True
            continue
        child_value = _alpha_beta(child, game, alpha, beta)
        if is_maximizing:
            value = max(value, child_value)
            alpha = max(alpha, value)
        else:
            value = min(value, child_value)
            beta = min(beta, value)
        if alpha >= beta:
            pruning = True
    node.value = value
    return node.value


def build_alpha_beta_tree(
    game: rimtsaazg.Game, state: rimtsaazg.State
) -> SearchNode:
    """
    Run alpha-beta pruning from `state` and return the search tree.

    :param game: game-agnostic rules implementation
    :param state: state to search from, must not be terminal
    :return: root node; every explored descendant's `.value` is backed up,
        pruned descendants are recorded with `.pruned = True` and no
        children
    """
    hdbg.dassert(
        not game.is_terminal(state), "Cannot search from a terminal state"
    )
    root = SearchNode(state)
    _alpha_beta(root, game, -math.inf, math.inf)
    return root


def run_alpha_beta(
    game: rimtsaazg.Game, state: rimtsaazg.State
) -> rimtsaazg.Move:
    """
    Run alpha-beta pruning from `state` and return the best move at the
    root.

    The root's own children are never pruned (`alpha=-inf, beta=+inf` at
    the first call, and only one of the two bounds tightens per level), so
    this always agrees with `run_minimax()` while exploring fewer nodes.

    :param game: game-agnostic rules implementation
    :param state: state to search from, must not be terminal
    :return: move maximizing (minimizing) the root value for player `1`
        (`-1`)
    """
    root = build_alpha_beta_tree(game, state)
    best_move = pick_best_move(game, root)
    return best_move


def make_alpha_beta_player() -> Callable[[rimtsaazg.Game, rimtsaazg.State], rimtsaazg.Move]:
    """
    Build a `(game, state) -> move` player function backed by alpha-beta
    pruning.

    :return: player function suitable for `mcts_utils.play_game()`
    """

    def player(game: rimtsaazg.Game, state: rimtsaazg.State) -> rimtsaazg.Move:
        move = run_alpha_beta(game, state)
        return move

    return player


# #############################################################################
# Depth-limited search
# #############################################################################


def _depth_limited(
    node: SearchNode,
    game: rimtsaazg.Game,
    depth: int,
    max_depth: int,
    evaluate_fn: Callable[[rimtsaazg.State], float],
) -> float:
    """
    Recursively back up the value of `node.state`, cutting at `max_depth`
    and scoring the cut with `evaluate_fn`.

    :param node: node to expand and score, `.children` populated in place
    :param game: game-agnostic rules implementation
    :param depth: number of moves already applied since the search root
    :param max_depth: depth at which to stop expanding and call
        `evaluate_fn` instead
    :param evaluate_fn: `state -> heuristic score` used to score a
        non-terminal state at the cut depth
    :return: exact or heuristic value of `node.state` from X's perspective
    """
    state = node.state
    if game.is_terminal(state):
        value = float(game.get_winner(state))
    elif depth >= max_depth:
        value = evaluate_fn(state)
        node.is_heuristic = True
    else:
        current_player = game.get_current_player(state)
        values = []
        for move in game.get_legal_moves(state):
            child_state = game.apply_move(state, move)
            child = node.add_child(move, child_state)
            values.append(
                _depth_limited(child, game, depth + 1, max_depth, evaluate_fn)
            )
        value = max(values) if current_player == 1 else min(values)
    node.value = value
    return value


def build_depth_limited_tree(
    game: rimtsaazg.Game,
    state: rimtsaazg.State,
    evaluate_fn: Callable[[rimtsaazg.State], float],
    *,
    max_depth: int = DEFAULT_MAX_DEPTH,
) -> SearchNode:
    """
    Run depth-limited minimax from `state` and return the search tree.

    :param game: game-agnostic rules implementation
    :param state: state to search from, must not be terminal
    :param evaluate_fn: `state -> heuristic score` used to score a
        non-terminal state at the cut depth, e.g.,
        `game_examples.evaluate_tic_tac_toe`
    :param max_depth: number of plies to search before cutting and calling
        `evaluate_fn`
        - Default: `DEFAULT_MAX_DEPTH`
    :return: root node, with every descendant's `.value` backed up (exact
        at a terminal, heuristic -- `.is_heuristic = True` -- at a cut)
    """
    hdbg.dassert(
        not game.is_terminal(state), "Cannot search from a terminal state"
    )
    hdbg.dassert_lte(1, max_depth)
    root = SearchNode(state)
    _depth_limited(root, game, 0, max_depth, evaluate_fn)
    return root


def run_depth_limited(
    game: rimtsaazg.Game,
    state: rimtsaazg.State,
    evaluate_fn: Callable[[rimtsaazg.State], float],
    *,
    max_depth: int = DEFAULT_MAX_DEPTH,
) -> rimtsaazg.Move:
    """
    Run depth-limited minimax from `state` and return the best move.

    :param game: game-agnostic rules implementation
    :param state: state to search from, must not be terminal
    :param evaluate_fn: `state -> heuristic score` used at the cut depth
    :param max_depth: number of plies to search before cutting
        - Default: `DEFAULT_MAX_DEPTH`
    :return: move maximizing (minimizing) the root value for player `1`
        (`-1`)
    """
    root = build_depth_limited_tree(
        game, state, evaluate_fn, max_depth=max_depth
    )
    best_move = pick_best_move(game, root)
    return best_move


def make_depth_limited_player(
    evaluate_fn: Callable[[rimtsaazg.State], float],
    *,
    max_depth: int = DEFAULT_MAX_DEPTH,
) -> Callable[[rimtsaazg.Game, rimtsaazg.State], rimtsaazg.Move]:
    """
    Build a `(game, state) -> move` player function backed by depth-limited
    search.

    :param evaluate_fn: `state -> heuristic score` used at the cut depth
    :param max_depth: number of plies to search before cutting
        - Default: `DEFAULT_MAX_DEPTH`
    :return: player function suitable for `mcts_utils.play_game()`
    """

    def player(game: rimtsaazg.Game, state: rimtsaazg.State) -> rimtsaazg.Move:
        move = run_depth_limited(game, state, evaluate_fn, max_depth=max_depth)
        return move

    return player


# #############################################################################
# Flat Monte Carlo
# #############################################################################


def _estimate_action_value(
    game: rimtsaazg.Game,
    state: rimtsaazg.State,
    move: rimtsaazg.Move,
    *,
    num_rollouts: int,
) -> float:
    """
    Estimate `Q_hat(state, move)` as the mean outcome, from the mover's
    perspective, over `num_rollouts` random playouts through `move`.

    Lesson09.8: "For each action a at s0: Run N random playouts to a
    terminal state, estimate Q_hat(s0, a) as the mean terminal outcome."
    Reuses `mcts_utils.random_rollout()`, MCTS's own default policy.

    :param game: game-agnostic rules implementation
    :param state: state the action is taken from
    :param move: action to evaluate
    :param num_rollouts: number of random playouts to average over
    :return: mean outcome in `[-1, 1]` from the mover's perspective
    """
    mover = game.get_current_player(state)
    total = 0.0
    for _ in range(num_rollouts):
        rollout_state = game.apply_move(state, move)
        winner = rimtsaazmu.random_rollout(game, rollout_state)
        if winner == mover:
            total += 1.0
        elif winner != 0:
            total -= 1.0
    q_hat = total / num_rollouts
    return q_hat


def build_flat_mc_tree(
    game: rimtsaazg.Game,
    state: rimtsaazg.State,
    *,
    num_rollouts: int = DEFAULT_NUM_ROLLOUTS,
) -> SearchNode:
    """
    Score every legal move at `state` by flat Monte Carlo and return the
    resulting depth-one search tree.

    Lesson09.8: "Flat Monte Carlo is exactly MCTS with a tree of depth
    one": one child per root action, no further expansion.

    :param game: game-agnostic rules implementation
    :param state: state to search from, must not be terminal
    :param num_rollouts: number of random playouts averaged per action
        - Default: `DEFAULT_NUM_ROLLOUTS`
    :return: root node with one scored child per legal move
    """
    hdbg.dassert(
        not game.is_terminal(state), "Cannot search from a terminal state"
    )
    root = SearchNode(state)
    child_values = []
    for move in game.get_legal_moves(state):
        child_state = game.apply_move(state, move)
        child = root.add_child(move, child_state)
        value = _estimate_action_value(
            game, state, move, num_rollouts=num_rollouts
        )
        child.value = value
        child_values.append(value)
    current_player = game.get_current_player(state)
    root.value = max(child_values) if current_player == 1 else min(child_values)
    return root


def run_flat_mc(
    game: rimtsaazg.Game,
    state: rimtsaazg.State,
    *,
    num_rollouts: int = DEFAULT_NUM_ROLLOUTS,
) -> rimtsaazg.Move:
    """
    Run flat Monte Carlo from `state` and return `argmax_a Q_hat(s0, a)`.

    :param game: game-agnostic rules implementation
    :param state: state to search from, must not be terminal
    :param num_rollouts: number of random playouts averaged per action
        - Default: `DEFAULT_NUM_ROLLOUTS`
    :return: best-estimated move for the player to move at `state`
    """
    root = build_flat_mc_tree(game, state, num_rollouts=num_rollouts)
    best_move = pick_best_move(game, root)
    return best_move


def make_flat_mc_player(
    *, num_rollouts: int = DEFAULT_NUM_ROLLOUTS
) -> Callable[[rimtsaazg.Game, rimtsaazg.State], rimtsaazg.Move]:
    """
    Build a `(game, state) -> move` player function backed by flat Monte
    Carlo.

    :param num_rollouts: number of random playouts averaged per action
        - Default: `DEFAULT_NUM_ROLLOUTS`
    :return: player function suitable for `mcts_utils.play_game()`
    """

    def player(game: rimtsaazg.Game, state: rimtsaazg.State) -> rimtsaazg.Move:
        move = run_flat_mc(game, state, num_rollouts=num_rollouts)
        return move

    return player


# #############################################################################
# Shared helpers
# #############################################################################


def pick_best_move(game: rimtsaazg.Game, root: SearchNode) -> rimtsaazg.Move:
    """
    Pick the move of the root child with the best value for the player to
    move at `root.state`.

    Public (unlike the rest of this section's `build_*_tree()` internals)
    since it is also how a caller reads a move back off a tree it built
    directly, e.g., to label a `build_tree_graph()` diagram without paying
    for the search twice by also calling the matching `run_*()`.

    Pruned children (alpha-beta) are excluded: they were proven worse than
    an already-explored sibling, so they were never assigned a `.value`.

    :param game: game-agnostic rules implementation
    :param root: root node with at least one explored child
    :return: `.move` of the best child
    """
    children = [child for child in root.children if not child.pruned]
    hdbg.dassert(children, "No explored child to pick a move from")
    current_player = game.get_current_player(root.state)
    if current_player == 1:
        best_child = max(children, key=lambda child: cast(float, child.value))
    else:
        best_child = min(children, key=lambda child: cast(float, child.value))
    return cast(rimtsaazg.Move, best_child.move)


# #############################################################################
# Visualization
# #############################################################################


def _node_style(node: SearchNode) -> Tuple[str, str]:
    """
    Pick the fill color and Graphviz style for `node`.

    :param node: node to style
    :return: `(fillcolor, style)` pair for `graphviz.Digraph.node()`
    """
    if node.pruned:
        # Grey, dashed: recorded but never explored.
        fillcolor, style = "#E0E0E0", "rounded,filled,dashed"
    elif node.is_heuristic:
        # Amber: a depth-limited cut, scored by the evaluation function.
        fillcolor, style = "#FFC98A", "rounded,filled"
    elif not node.children:
        # Green: an explored terminal node, exact outcome.
        fillcolor, style = "#A9DDB0", "rounded,filled"
    else:
        # Blue: an explored internal node, backed-up value.
        fillcolor, style = "#D9E8FB", "rounded,filled"
    return fillcolor, style


def _node_label(node: SearchNode) -> str:
    """
    Build the multi-line label Graphviz draws inside `node`'s box.

    :param node: node to label
    :return: label text, e.g., "move=2\\nvalue=1.00"
    """
    prefix = "root" if node.parent is None else f"move={node.move}"
    if node.pruned:
        label = f"{prefix}\npruned"
    else:
        value_str = f"{node.value:.2f}" if node.value is not None else "?"
        label = f"{prefix}\nvalue={value_str}"
    return label


def _add_node_to_graph(
    dot: "graphviz.Digraph",
    node: SearchNode,
    node_id: str,
    depth: int,
    max_depth: int,
    best_move: Optional[rimtsaazg.Move],
) -> None:
    """
    Recursively add `node` and its descendants (up to `max_depth`) to `dot`.

    :param dot: Graphviz graph being built, mutated in place
    :param node: node to add next
    :param node_id: unique Graphviz node id for `node`
    :param depth: number of levels already added above `node`
    :param max_depth: number of levels below the root to render
    :param best_move: move chosen at the root, its direct child outlined
    """
    fillcolor, style = _node_style(node)
    is_best_root_child = depth == 1 and node.move == best_move
    penwidth = "2.5" if is_best_root_child else "1.0"
    dot.node(
        node_id,
        _node_label(node),
        fillcolor=fillcolor,
        style=style,
        penwidth=penwidth,
    )
    if node.pruned:
        return
    if depth >= max_depth:
        if node.children:
            more_id = f"{node_id}_more"
            dot.node(
                more_id,
                f"... {len(node.children)} more",
                shape="plaintext",
                style="",
            )
            dot.edge(node_id, more_id, style="dotted", label="  cut  ")
        return
    for i, child in enumerate(node.children):
        child_id = f"{node_id}_{i}"
        dot.edge(node_id, child_id)
        _add_node_to_graph(dot, child, child_id, depth + 1, max_depth, best_move)


def build_tree_graph(
    root: SearchNode,
    *,
    best_move: Optional[rimtsaazg.Move] = None,
    max_depth: int = DEFAULT_RENDER_DEPTH,
) -> "graphviz.Digraph":
    """
    Render `root` and up to `max_depth` levels of its descendants as a
    Graphviz tree.

    Shared by minimax, alpha-beta, and depth-limited search (flat Monte
    Carlo's tree is depth one, so `max_depth=1` shows all of it). A search
    tree can have thousands of nodes, so rendering stops at `max_depth` and
    shows a "... N more" placeholder instead (Lesson09.8: "the shape of the
    tree is the allocation of the budget" -- the shape is what matters,
    not every node).

    Node color/style encodes what happened to it:
    - blue: an explored internal node, labeled with its backed-up value
    - green: an explored terminal node (exact `get_winner()` value)
    - amber: a depth-limited cut node, labeled with its heuristic value
    - grey, dashed: a node alpha-beta recorded but never explored (pruned)
    - a heavier border marks the best move's direct root child

    :param root: root of a tree built by `build_minimax_tree()`,
        `build_alpha_beta_tree()`, `build_depth_limited_tree()`, or
        `build_flat_mc_tree()`
    :param best_move: move chosen at the root, highlighted if given
        - Default: `None` (no highlight)
    :param max_depth: number of levels below the root to render
        - Default: `DEFAULT_RENDER_DEPTH`
    :return: Graphviz graph, rendered natively by Jupyter's `display()`
    """
    import graphviz

    dot = graphviz.Digraph()
    dot.attr("node", shape="box", fontname="Helvetica")
    _add_node_to_graph(dot, root, "root", 0, max_depth, best_move)
    return dot
