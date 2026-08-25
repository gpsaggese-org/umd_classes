"""
Notebook utilities for `mcts.API.ipynb`.

See `mcts_utils.py` for the game-agnostic MCTS engine, `game_examples.py`
for the concrete `Game` implementations these widgets operate on, and
`README.md` for a description of every file in this directory.

Import as:

import research.Implement_MonteCarlo_Tree_Search_and_Alpha_Zero.mcts_API_utils as rimtsaazmau
"""

import logging
import random
from typing import TYPE_CHECKING, Callable, Dict, Optional, Tuple

import ipywidgets
import matplotlib.axes
import matplotlib.patches
import matplotlib.pyplot as plt
from IPython.display import clear_output, display

if TYPE_CHECKING:
    import graphviz

import helpers.hdbg as hdbg
import helpers.hprint as hprint
import helpers.htutorial as htutori
import research.Implement_MonteCarlo_Tree_Search_and_Alpha_Zero.mcts_utils as rimtsaazmu

_LOG = logging.getLogger(__name__)


# #############################################################################
# Cell 2.4: Interactive two-player board
# #############################################################################


def cell2_4_build_play_widget(game: rimtsaazmu.Game) -> "ipywidgets.VBox":
    """
    Build a clickable board where the user plays both `X` and `O`.

    Every click applies a legal move via `Game.apply_move()`, re-renders the
    3x3 grid of buttons, and updates the status line; a "New game" button
    resets to the initial state.

    :param game: game-agnostic rules implementation for a 3x3 board (e.g.,
        `TicTacToe`)
    :return: widget container to `display()` in a notebook cell
    """
    _LOG.debug(hprint.to_str("game"))
    # A cell's value is `0` (empty), `1` (X), or `-1` (O); see `Game`'s
    # docstring in `mcts_utils.py` for the player-encoding convention.
    # Use a single space (not "") for the empty label: some `ipywidgets`
    # frontends don't repaint a `Button.description` change into an empty
    # string, which would leave stale `X`/`O` labels on the board after
    # "New game".
    _empty = 0
    _player_symbols = {0: "\u00a0", 1: "X", -1: "O"}
    game_state: Dict[str, rimtsaazmu.State] = {"state": game.get_initial_state()}
    status = ipywidgets.HTML()
    cell_buttons = [
        ipywidgets.Button(
            description="",
            layout=ipywidgets.Layout(width="60px", height="60px"),
        )
        for _ in range(9)
    ]

    def _update_view() -> None:
        """
        Refresh button labels and the status line from `game_state`.
        """
        state = game_state["state"]
        for button, cell in zip(cell_buttons, state):
            button.description = _player_symbols[cell]
        if game.is_terminal(state):
            winner = game.get_winner(state)
            if winner == _empty:
                status.value = "<b>Game over: draw</b>"
            else:
                status.value = (
                    f"<b>Game over: {_player_symbols[winner]} wins</b>"
                )
        else:
            player = game.get_current_player(state)
            status.value = f"Current turn: <b>{_player_symbols[player]}</b>"

    def _make_on_click(index: int) -> Callable[["ipywidgets.Button"], None]:
        """
        Build the click handler for the cell at `index`.
        """

        def _on_click(_button: "ipywidgets.Button") -> None:
            state = game_state["state"]
            if game.is_terminal(state) or state[index] != _empty:
                # Ignore clicks on a finished game or an occupied cell.
                return
            game_state["state"] = game.apply_move(state, index)
            _update_view()

        return _on_click

    # Wire up one click handler per cell.
    for index, button in enumerate(cell_buttons):
        button.on_click(_make_on_click(index))

    def _on_reset_click(_button: "ipywidgets.Button") -> None:
        game_state["state"] = game.get_initial_state()
        _update_view()

    reset_button = ipywidgets.Button(description="New game")
    reset_button.on_click(_on_reset_click)
    # Lay out the 9 buttons as a 3x3 grid.
    grid = ipywidgets.VBox(
        [ipywidgets.HBox(cell_buttons[row : row + 3]) for row in range(0, 9, 3)]
    )
    _update_view()
    widget = ipywidgets.VBox([status, grid, reset_button])
    return widget


# #############################################################################
# Cell 4.2: Search-tree visualization
# #############################################################################


def _build_tree_graph(
    root: rimtsaazmu.MCTSNode, best_move: rimtsaazmu.Move
) -> "graphviz.Digraph":
    """
    Render `root` and its immediate children as a Graphviz tree.

    Only one ply is shown (root + children): deeper subtrees grow too large
    to read, and the immediate children are exactly what `run_mcts()` picks
    the best move from.

    :param root: fully-built MCTS root node (see `build_mcts_tree()`)
    :param best_move: move with the highest visit count, highlighted
    :return: Graphviz graph, rendered natively by Jupyter's `display()`
    """
    import graphviz

    dot = graphviz.Digraph()
    dot.attr("node", shape="box", style="rounded,filled", fontname="Helvetica")
    dot.node(
        "root",
        f"root\nN={root.visit_count}\nQ={root.mean_value:.2f}",
        fillcolor="#D9E8FB",
    )
    for move, child in sorted(root.children.items()):
        node_id = f"move_{move}"
        fillcolor = "#FDE9C8" if move == best_move else "#EFEFEF"
        dot.node(
            node_id,
            f"move={move}\nN={child.visit_count}\nQ={child.mean_value:.2f}",
            fillcolor=fillcolor,
        )
        dot.edge("root", node_id)
    return dot


def _plot_child_visits(
    ax: matplotlib.axes.Axes,
    root: rimtsaazmu.MCTSNode,
    best_move: rimtsaazmu.Move,
) -> None:
    """
    Plot a bar chart of visit_count per root child, highest first.

    :param ax: axes to plot into
    :param root: fully-built MCTS root node
    :param best_move: move with the highest visit count, highlighted
    """
    children = sorted(
        root.children.items(), key=lambda item: item[1].visit_count, reverse=True
    )
    moves = [str(move) for move, _ in children]
    visits = [child.visit_count for _, child in children]
    colors = [
        "#4C9A2A" if move == best_move else "#7FA6D9" for move, _ in children
    ]
    ax.bar(moves, visits, color=colors)
    ax.set_xlabel("move (cell index)")
    ax.set_ylabel("visit count")
    ax.set_title("Visit count per root child")


def _build_tree_widget(
    game: rimtsaazmu.Game,
    state: rimtsaazmu.State,
    *,
    board_picture_fn: Optional[Callable[..., None]] = None,
) -> "ipywidgets.VBox":
    """
    Interactive widget: run MCTS from `state` and visualize the resulting
    search tree.

    Shared by `cell4_2_build_tree_widget()` (tic-tac-toe, text-only) and
    `cell7_5_build_connect_four_tree_widget()` (Connect Four, with a board
    picture): both let the user tune the two knobs from the UCT formula
    used by `run_mcts()` / `build_mcts_tree()`, Q(s, a) + C * sqrt(ln N(s) /
    N(s, a)) (Lesson09.8):
    - `num_simulations`: the search budget (Lesson09.8: "repeat until the
      budget - number of simulations, or time - is exhausted")
    - `exploration_constant`: the `C` in the formula above
    and see how the visit count N(s, a) and mean value Q(s, a) of each root
    child respond.

    :param game: game-agnostic rules implementation
    :param state: state to search from, must not be terminal
    :param board_picture_fn: if given, a `(state, *, ax) -> None` function
        (e.g., `plot_connect_four_board()`) that draws `state` into an extra
        leftmost panel next to the visit-count bar chart, tying each
        child's move back to the board being searched
        - Default: `None` (bar chart + comments panel only, as used for
          tic-tac-toe, where the Graphviz tree diagram already shows enough
          of the board via move indices)
    :return: widget container to `display()` in a notebook cell
    """
    _LOG.debug(hprint.to_str("game state board_picture_fn"))
    hdbg.dassert(
        not game.is_terminal(state), "Cannot build a tree from a terminal state"
    )
    # Seed goes first, per notebook widget convention.
    seed_slider, seed_box = htutori.build_widget_control(
        name="seed",
        description="random seed",
        min_val=0,
        max_val=99,
        step=1,
        initial_value=0,
        is_float=False,
    )
    num_sim_exp_slider, num_sim_box = htutori.build_log_widget_control(
        name="log2(num_simulations)",
        description="search budget",
        min_exp=2,
        max_exp=9,
        initial_exp=7,
        base=2,
    )
    c_slider, c_box = htutori.build_widget_control(
        name="C",
        description="exploration constant",
        min_val=0.1,
        max_val=3.0,
        step=0.1,
        initial_value=rimtsaazmu.EXPLORATION_CONSTANT,
        is_float=True,
    )
    output = ipywidgets.Output()

    def update_plot(change: object = None) -> None:
        """
        Rebuild the tree from the current widget values and redraw it.
        """
        _ = change
        with output:
            clear_output(wait=True)
            # Read current widget values.
            seed = int(seed_slider.value)
            num_simulations = 2**num_sim_exp_slider.value
            exploration_constant = float(c_slider.value)
            # Build the tree, seeding first for reproducible rollouts.
            random.seed(seed)
            root = rimtsaazmu.build_mcts_tree(
                game,
                state,
                num_simulations=num_simulations,
                exploration_constant=exploration_constant,
            )
            best_move = max(
                root.children.items(), key=lambda item: item[1].visit_count
            )[0]
            # Tree diagram (Graphviz), then optionally a board picture, a
            # bar chart, and a comments panel.
            display(_build_tree_graph(root, best_move))
            num_panels = 3 if board_picture_fn is not None else 2
            _, axes = plt.subplots(
                1, num_panels, figsize=(5.5 * num_panels, 4.5)
            )
            if board_picture_fn is not None:
                ax_board, ax_bar, ax_comment = axes
                board_picture_fn(state, ax=ax_board)
                ax_board.set_title("Board being searched")
            else:
                ax_bar, ax_comment = axes
            _plot_child_visits(ax_bar, root, best_move)
            best_child = root.children[best_move]
            comment_text = (
                "Parameters:\n"
                f"  seed: {seed}\n"
                f"  num_simulations: {num_simulations}\n"
                f"  C: {exploration_constant:.2f}\n"
                "\n"
                "Root stats:\n"
                f"  root visit_count N(s): {root.visit_count}\n"
                f"  robust child (highest N): {best_move}\n"
                f"  N(s, a) of robust child: {best_child.visit_count}\n"
                f"  Q(s, a) of robust child: {best_child.mean_value:.2f}"
            )
            ax_comment.axis("off")
            ax_comment.set_title(
                "Comments", fontsize=14, fontweight="bold", pad=20
            )
            htutori.add_fitted_text_box(ax_comment, comment_text)
            plt.tight_layout()
            plt.show()

    # Attach observers to all widgets.
    seed_slider.observe(update_plot, names="value")
    num_sim_exp_slider.observe(update_plot, names="value")
    c_slider.observe(update_plot, names="value")
    # Initial render.
    update_plot()
    widget = ipywidgets.VBox([seed_box, num_sim_box, c_box, output])
    return widget


def cell4_2_build_tree_widget(
    game: rimtsaazmu.Game, state: rimtsaazmu.State
) -> "ipywidgets.VBox":
    """
    Interactive widget: run MCTS from `state` and visualize the resulting
    search tree as a Graphviz diagram plus a visit-count bar chart.

    See `_build_tree_widget()` for the shared implementation.

    :param game: game-agnostic rules implementation
    :param state: state to search from, must not be terminal
    :return: widget container to `display()` in a notebook cell
    """
    widget = _build_tree_widget(game, state)
    return widget


# #############################################################################
# Part 7: Connect Four
# #############################################################################


# Board geometry mirrors `game_examples.ConnectFour`'s hardcoded 6x7 layout;
# kept as separate constants here since this module only deals with
# presentation, not game rules.
_CONNECT_FOUR_NUM_ROWS = 6
_CONNECT_FOUR_NUM_COLS = 7

# Disc colors follow the physical game (red vs. yellow discs on a blue
# board), not the muted palette used for charts elsewhere in this module:
# a literal, recognizable board is the whole point of a board picture.
_CONNECT_FOUR_DISC_COLORS = {0: "#F5F5F5", 1: "#D6402C", -1: "#F4C542"}
_CONNECT_FOUR_BOARD_COLOR = "#2F6FBB"
_CONNECT_FOUR_PLAYER_NAMES = {1: "red", -1: "yellow"}


def plot_connect_four_board(
    state: rimtsaazmu.State,
    *,
    ax: Optional[matplotlib.axes.Axes] = None,
    figsize: Optional[Tuple[int, int]] = None,
) -> None:
    """
    Draw `state` as a Connect Four board: colored discs on a blue grid.

    A picture reads a Connect Four position far faster than the text grid
    `ConnectFour.render()` produces, which is why every Connect Four cell in
    this notebook shows the board this way.

    :param state: length-42 Connect Four state (see
        `game_examples.ConnectFour`), row-major with row `0` at the top
    :param ax: axes to draw into
        - Default: `None` (create a standalone figure and `plt.show()` it;
          pass an `ax` instead to embed the board in a larger figure, e.g.,
          a multi-panel widget)
    :param figsize: figure size, only used when `ax` is `None`
        - Default: `None` (uses `plt.rcParams["figure.figsize"]`)
    """
    standalone = ax is None
    if standalone:
        if figsize is None:
            figsize = plt.rcParams["figure.figsize"]
        _, ax = plt.subplots(figsize=figsize)
    ax.set_facecolor(_CONNECT_FOUR_BOARD_COLOR)
    for row in range(_CONNECT_FOUR_NUM_ROWS):
        for col in range(_CONNECT_FOUR_NUM_COLS):
            cell = state[row * _CONNECT_FOUR_NUM_COLS + col]
            # Flip the row so row 0 (top of the board) is drawn at the top
            # of the axes instead of matplotlib's default bottom-up y-axis.
            y = _CONNECT_FOUR_NUM_ROWS - 1 - row
            disc = matplotlib.patches.Circle(
                (col, y),
                0.42,
                facecolor=_CONNECT_FOUR_DISC_COLORS[cell],
                edgecolor="#1B4A80",
                linewidth=1.0,
                zorder=2,
            )
            ax.add_patch(disc)
    ax.set_xlim(-0.6, _CONNECT_FOUR_NUM_COLS - 0.4)
    ax.set_ylim(-0.6, _CONNECT_FOUR_NUM_ROWS - 0.4)
    ax.set_aspect("equal")
    ax.set_xticks(range(_CONNECT_FOUR_NUM_COLS))
    ax.set_xlabel("column")
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)
    if standalone:
        plt.show()


# #############################################################################
# Cell 7.3: Interactive Connect Four board
# #############################################################################


def cell7_3_build_connect_four_play_widget(
    game: rimtsaazmu.Game,
) -> "ipywidgets.VBox":
    """
    Build a clickable Connect Four board where the user plays both colors.

    One button per column drops the current player's disc via
    `Game.apply_move()`, gravity included; the board picture
    (`plot_connect_four_board()`) and status line refresh after every move;
    a "New game" button resets to the initial state.

    :param game: game-agnostic rules implementation for Connect Four
        (`ConnectFour`)
    :return: widget container to `display()` in a notebook cell
    """
    _LOG.debug(hprint.to_str("game"))
    game_state: Dict[str, rimtsaazmu.State] = {"state": game.get_initial_state()}
    status = ipywidgets.HTML()
    output = ipywidgets.Output()

    def _update_view() -> None:
        """
        Redraw the board picture and refresh the status line from
        `game_state`.
        """
        state = game_state["state"]
        with output:
            clear_output(wait=True)
            plot_connect_four_board(state, figsize=(6, 5))
        if game.is_terminal(state):
            winner = game.get_winner(state)
            if winner == 0:
                status.value = "<b>Game over: draw</b>"
            else:
                status.value = f"<b>Game over: {_CONNECT_FOUR_PLAYER_NAMES[winner]} wins</b>"
        else:
            player = game.get_current_player(state)
            status.value = (
                f"Current turn: <b>{_CONNECT_FOUR_PLAYER_NAMES[player]}</b>"
            )

    def _make_on_click(col: int) -> Callable[["ipywidgets.Button"], None]:
        """
        Build the click handler that drops a disc into column `col`.
        """

        def _on_click(_button: "ipywidgets.Button") -> None:
            state = game_state["state"]
            if game.is_terminal(state) or col not in game.get_legal_moves(state):
                # Ignore clicks on a finished game or a full column.
                return
            game_state["state"] = game.apply_move(state, col)
            _update_view()

        return _on_click

    # Wire up one click handler per column.
    column_buttons = [
        ipywidgets.Button(
            description=f"drop {col}",
            layout=ipywidgets.Layout(width="70px"),
        )
        for col in range(_CONNECT_FOUR_NUM_COLS)
    ]
    for col, button in enumerate(column_buttons):
        button.on_click(_make_on_click(col))

    def _on_reset_click(_button: "ipywidgets.Button") -> None:
        game_state["state"] = game.get_initial_state()
        _update_view()

    reset_button = ipywidgets.Button(description="New game")
    reset_button.on_click(_on_reset_click)
    buttons_row = ipywidgets.HBox(column_buttons)
    _update_view()
    widget = ipywidgets.VBox([status, buttons_row, output, reset_button])
    return widget


# #############################################################################
# Cell 7.5: Connect Four search-tree visualization
# #############################################################################


def cell7_5_build_connect_four_tree_widget(
    game: rimtsaazmu.Game, state: rimtsaazmu.State
) -> "ipywidgets.VBox":
    """
    Interactive widget: run MCTS from a Connect Four `state` and visualize
    the resulting search tree next to a picture of the board being
    searched.

    Same knobs and Graphviz/bar-chart layout as `cell4_2_build_tree_widget()`;
    the extra `plot_connect_four_board()` panel ties each child's move (a
    column) back to where the disc would land.

    :param game: game-agnostic rules implementation, `ConnectFour`
    :param state: state to search from, must not be terminal
    :return: widget container to `display()` in a notebook cell
    """
    widget = _build_tree_widget(
        game, state, board_picture_fn=plot_connect_four_board
    )
    return widget
