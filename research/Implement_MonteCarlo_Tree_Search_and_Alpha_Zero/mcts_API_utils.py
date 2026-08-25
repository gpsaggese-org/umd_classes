"""
Notebook utilities for `mcts.API.ipynb`.

See `mcts_utils.py` for the game-agnostic MCTS engine and `game_examples.py`
for the concrete `Game` implementations these widgets operate on.

Import as:

import research.Implement_MonteCarlo_Tree_Search_and_Alpha_Zero.mcts_API_utils as rimtsaazmau
"""

import logging
import random
from typing import TYPE_CHECKING, Callable, Dict

import ipywidgets
import matplotlib.axes
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
                status.value = f"<b>Game over: {_player_symbols[winner]} wins</b>"
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


def cell4_2_build_tree_widget(
    game: rimtsaazmu.Game, state: rimtsaazmu.State
) -> "ipywidgets.VBox":
    """
    Interactive widget: run MCTS from `state` and visualize the resulting
    search tree.

    Lets the user tune the two knobs from the UCT formula used by
    `run_mcts()` / `build_mcts_tree()`:
    - `num_simulations`: the search budget (Lesson09.8: "repeat until the
      budget - number of simulations, or time - is exhausted")
    - `exploration_constant`: the `C` in `Q/N + C * sqrt(ln(N_parent) / N)`
    and see how the visit count and mean value of each root child respond.

    :param game: game-agnostic rules implementation
    :param state: state to search from, must not be terminal
    :return: widget container to `display()` in a notebook cell
    """
    _LOG.debug(hprint.to_str("game state"))
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
            # Tree diagram (Graphviz), then a bar chart + comments panel.
            display(_build_tree_graph(root, best_move))
            _, (ax_bar, ax_comment) = plt.subplots(1, 2, figsize=(11, 4))
            _plot_child_visits(ax_bar, root, best_move)
            best_child = root.children[best_move]
            comment_text = (
                "Parameters:\n"
                f"  seed: {seed}\n"
                f"  num_simulations: {num_simulations}\n"
                f"  C: {exploration_constant:.2f}\n"
                "\n"
                "Root stats:\n"
                f"  root visit_count: {root.visit_count}\n"
                f"  best move: {best_move}\n"
                f"  best move visit_count: {best_child.visit_count}\n"
                f"  best move mean_value: {best_child.mean_value:.2f}"
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
