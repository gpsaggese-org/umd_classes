"""
Shared constants and utility functions for the 4x3 grid world RL lesson.

Used by both the from-scratch AIMA implementation (L12_01) and the gymnasium
implementation (L12_02).  Kept in a separate file so each notebook-style
utils module can import the shared pieces without duplicating them.

Import as:

import msml610.tutorials.L12_reinforcement_learning.L12_01_utils as mtlrll0ut
"""

import logging
from typing import Any, Dict, Optional, Tuple

import ipywidgets
import matplotlib.axes
import matplotlib.patches as mpatches
import numpy as np
import seaborn as sns

import helpers.hnotebook as hnotebo
import helpers.htutorial as htutori

_LOG = logging.getLogger(__name__)

# #############################################################################
# Action names and their geometry on the 4x3 grid
# #############################################################################

# List of direction names.
ACTIONS = ["Up", "Down", "Left", "Right"]

# Displacement (d_col, d_row) for each action.
ACTION_DELTA = {
    "Up": (0, 1),
    "Down": (0, -1),
    "Left": (-1, 0),
    "Right": (1, 0),
}

# Perpendicular slip directions used by the stochastic transition model.
PERPENDICULAR = {
    "Up": ["Left", "Right"],
    "Down": ["Left", "Right"],
    "Left": ["Up", "Down"],
    "Right": ["Up", "Down"],
}

# Arrow-tip offset when drawing a policy action arrow in a grid cell.
ARROW_DELTA = {
    "Up": (0.0, 0.3),
    "Down": (0.0, -0.3),
    "Left": (-0.3, 0.0),
    "Right": (0.3, 0.0),
}

# Integer-action <-> name mapping (gymnasium convention).
ACTION_ID_TO_NAME = {0: "Up", 1: "Down", 2: "Left", 3: "Right"}
NAME_TO_ACTION_ID = {v: k for k, v in ACTION_ID_TO_NAME.items()}

# #############################################################################
# Cell fill colours used when drawing the grid
# #############################################################################

COLOR_START = "#cfe8ff"
COLOR_GOAL = "#a8e6a3"
COLOR_PIT = "#f4a6a6"
COLOR_WALL = "#9e9e9e"
COLOR_EMPTY = "#ffffff"

# #############################################################################
# Logger initialisation
# #############################################################################


def init_loggers(notebook_log: logging.Logger) -> None:
    """
    Wire the notebook logger into the utils logger so notebook cells see
    debug / info output from these utility functions.
    """
    global _LOG
    hnotebo.init_loggers(notebook_log, utils_log=_LOG)


# #############################################################################
# Grid helpers
# #############################################################################


def to_grid(
    values: Dict[Tuple[int, int], float],
    n_rows: int,
    n_cols: int,
    *,
    fill: float = np.nan,
) -> np.ndarray:
    """
    Convert a dict over (col, row) cells into a 2-D array for heatmap plots.

    Row ``n_rows`` (the visual top of the grid) is placed in the first array
    row so the heatmap orientation matches the drawn grid.

    :param values: mapping from cell to a scalar value
    :param n_rows: number of grid rows
    :param n_cols: number of grid columns
    :param fill: value used for walls / missing cells
    :return: array of shape ``(n_rows, n_cols)``
    """
    grid = np.full((n_rows, n_cols), fill, dtype=float)
    for (col, row), val in values.items():
        grid[n_rows - row, col - 1] = val
    return grid


def _cell_facecolor(
    cell: Tuple[int, int],
    walls: set,
    terminals: Dict[Tuple[int, int], float],
    start: Tuple[int, int],
) -> str:
    """
    Return the fill colour for a cell based on its role in the environment.
    """
    if cell in walls:
        return COLOR_WALL
    if cell == (4, 3):
        return COLOR_GOAL
    if cell == (4, 2):
        return COLOR_PIT
    if cell == start:
        return COLOR_START
    return COLOR_EMPTY


def draw_grid_base(
    env: Any,
    ax: matplotlib.axes.Axes,
    *,
    annotate_coords: bool = False,
    highlight: Optional[Tuple[int, int]] = None,
) -> None:
    """
    Draw the empty 4x3 grid with coloured special cells.

    .. note::

        This version works with *any* environment object that exposes the
        following API:

        - ``env.n_cols``, ``env.n_rows``
        - ``env.walls`` (or ``env.wall_cells`` for ``_cell_facecolor``)
        - ``env.terminals`` (or ``env.terminal_cells``)
        - ``env.start`` (or ``env.start_cell``)

    :param env: grid-world environment
    :param ax: axes to draw on
    :param annotate_coords: if True, label each cell with its ``(col, row)``
    :param highlight: optional cell to outline in bold
    """
    # Resolve attribute names that differ between env classes.
    walls = getattr(env, "walls", getattr(env, "wall_cells", set()))
    terminals = getattr(env, "terminals", getattr(env, "terminal_cells", {}))
    start = getattr(env, "start", getattr(env, "start_cell", (1, 1)))

    for col in range(1, env.n_cols + 1):
        for row in range(1, env.n_rows + 1):
            cell = (col, row)
            rect = mpatches.Rectangle(
                (col - 0.5, row - 0.5),
                1.0,
                1.0,
                facecolor=_cell_facecolor(cell, walls, terminals, start),
                edgecolor="black",
                linewidth=1.5,
            )
            ax.add_patch(rect)
            # Label the terminals and the start with their role.
            label = None
            if cell == (4, 3):
                label = "+1"
            elif cell == (4, 2):
                label = "-1"
            elif cell == start:
                label = "START"
            elif cell in walls:
                label = "WALL"
            if label is not None:
                ax.text(
                    col,
                    row + 0.32,
                    label,
                    ha="center",
                    va="center",
                    fontsize=9,
                    fontweight="bold",
                )
            if annotate_coords:
                ax.text(
                    col,
                    row - 0.32,
                    f"({col},{row})",
                    ha="center",
                    va="center",
                    fontsize=8,
                    color="dimgray",
                )
    if highlight is not None:
        rect = mpatches.Rectangle(
            (highlight[0] - 0.5, highlight[1] - 0.5),
            1.0,
            1.0,
            fill=False,
            edgecolor="darkblue",
            linewidth=3.5,
        )
        ax.add_patch(rect)
    ax.set_xlim(0.4, env.n_cols + 0.6)
    ax.set_ylim(0.4, env.n_rows + 0.6)
    ax.set_xticks(range(1, env.n_cols + 1))
    ax.set_yticks(range(1, env.n_rows + 1))
    ax.set_aspect("equal")


def draw_policy_arrows(
    env: Any,
    ax: matplotlib.axes.Axes,
    policy: Dict[Tuple[int, int], str],
    *,
    color: str = "black",
) -> None:
    """
    Draw an arrow for each non-terminal cell showing its policy action.

    Works with both ``GridWorld`` (``env.walls``, ``env.is_terminal()``)
    and ``GridWorldEnv`` (``env.wall_cells``, ``env.terminal_cells``).
    """
    walls = getattr(env, "walls", getattr(env, "wall_cells", set()))
    terminals = getattr(env, "terminals", getattr(env, "terminal_cells", {}))

    for s, a in policy.items():
        if s in walls or s in terminals:
            continue
        d_x, d_y = ARROW_DELTA[a]
        ax.annotate(
            "",
            xy=(s[0] + d_x, s[1] + d_y),
            xytext=(s[0] - d_x, s[1] - d_y),
            arrowprops=dict(arrowstyle="-|>", color=color, linewidth=2.5),
        )


def draw_policy_arrows_heatmap(
    env: Any,
    ax: matplotlib.axes.Axes,
    policy: Dict[Tuple[int, int], str],
) -> None:
    """
    Overlay policy arrows on a heatmap plot (inverted-y coordinate system).

    The heatmap's array row 0 is the top of the grid, so the y-coordinate
    is flipped compared to :func:`draw_policy_arrows`.
    """
    for s, a in policy.items():
        d_x, d_y = ARROW_DELTA[a]
        x = s[0] - 0.5
        y = env.n_rows - s[1] + 0.5
        ax.annotate(
            "",
            xy=(x + d_x, y - d_y),
            xytext=(x - d_x, y + d_y),
            arrowprops=dict(arrowstyle="-|>", color="black", linewidth=2.0),
        )


def draw_value_heatmap(
    env: Any,
    ax: matplotlib.axes.Axes,
    u: Dict[Tuple[int, int], float],
    *,
    title: str,
    cmap: str = "RdYlGn",
) -> None:
    """
    Draw a utility heatmap with per-cell value annotations.
    """
    grid = to_grid(u, env.n_rows, env.n_cols)
    sns.heatmap(
        grid,
        ax=ax,
        cmap=cmap,
        center=0.0,
        annot=True,
        fmt=".2f",
        cbar=False,
        linewidths=1.0,
        linecolor="black",
        annot_kws={"fontsize": 10},
        mask=np.isnan(grid),
    )
    # Mark the wall cell explicitly since it is masked in the heatmap.
    walls = getattr(env, "walls", getattr(env, "wall_cells", set()))
    for wall in walls:
        ax.add_patch(
            mpatches.Rectangle(
                (wall[0] - 1, env.n_rows - wall[1]),
                1.0,
                1.0,
                facecolor=COLOR_WALL,
                edgecolor="black",
            )
        )
    ax.set_title(title, fontsize=13, fontweight="bold")
    ax.set_xticklabels([str(c) for c in range(1, env.n_cols + 1)])
    ax.set_yticklabels([str(r) for r in range(env.n_rows, 0, -1)], rotation=0)
    ax.set_xlabel("col")
    ax.set_ylabel("row")


def draw_visit_heatmap(
    env: Any,
    ax: matplotlib.axes.Axes,
    visit_counts: Dict[Any, int],
    *,
    title: str,
) -> None:
    """
    Draw a heatmap of per-state visit counts.

    ``visit_counts`` can be keyed by state-id (gymnasium) or by
    ``(col, row)`` cell (from-scratch).  Cell-keyed dicts are used
    directly; id-keyed dicts are converted via ``env.id_to_cell()``.
    """
    # Detect key type and convert if needed.
    if visit_counts and not isinstance(next(iter(visit_counts)), tuple):
        # Keys are state ids -> convert to cell keys.
        cell_counts = {
            env.id_to_cell(s_id): float(c) for s_id, c in visit_counts.items()
        }
    else:
        cell_counts = {s: float(c) for s, c in visit_counts.items()}
    grid = to_grid(cell_counts, env.n_rows, env.n_cols)
    sns.heatmap(
        grid,
        ax=ax,
        cmap="viridis",
        annot=True,
        fmt=".0f",
        cbar=False,
        linewidths=1.0,
        linecolor="black",
        mask=np.isnan(grid),
    )
    ax.set_title(title, fontsize=13, fontweight="bold")
    ax.set_xticklabels([str(c) for c in range(1, env.n_cols + 1)])
    ax.set_yticklabels([str(r) for r in range(env.n_rows, 0, -1)], rotation=0)
    ax.set_xlabel("col")
    ax.set_ylabel("row")


def comment_panel(ax: matplotlib.axes.Axes, text: str) -> None:
    """
    Render a wheat-coloured comment panel with a bold "Comments" title.
    """
    ax.axis("off")
    ax.set_title("Comments", fontsize=14, fontweight="bold", pad=20)
    htutori.add_fitted_text_box(ax, text, max_fontsize=12, min_fontsize=8)


def make_param_info(descriptions: Dict[str, str]) -> ipywidgets.HTML:
    """
    Build a styled HTML info box for notebook cell control panels.

    Each ``(name, desc)`` pair renders as ``<b>name</b> — desc<br>``.
    Description values may contain inline HTML (``<code>``, ``&minus;``, etc.).

    :param descriptions: mapping from parameter name to its description text
    :return: styled HTML widget ready for display
    """
    body = "\n".join(
        "<b>%s</b>: %s<br>" % (name, desc) for name, desc in descriptions.items()
    )
    html = (
        "<div style='background:#f5f5f5; padding:10px 14px; "
        "border-radius:4px; border-left:3px solid #4682b4; "
        "font-size:13px; line-height:1.8'>"
        "%s"
        "</div>"
    ) % body
    return ipywidgets.HTML(html)
