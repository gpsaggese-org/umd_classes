"""
Generate the two figures used in `paper.md`.

Run with:
> python3 figures/make_figures.py
"""

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Circle

plt.rcParams.update(
    {
        "font.size": 9,
        "axes.titlesize": 9,
        "axes.labelsize": 9,
        "legend.fontsize": 8,
        "xtick.labelsize": 8,
        "ytick.labelsize": 8,
        "figure.dpi": 200,
    }
)


def _node(ax, xy, label, *, dashed=False, radius=0.5, fontsize=7.5):
    color = "#7f8c8d" if dashed else "#1a5276"
    circ = Circle(
        xy,
        radius,
        facecolor="white",
        edgecolor=color,
        linewidth=1.6,
        linestyle="--" if dashed else "-",
        zorder=3,
    )
    ax.add_patch(circ)
    ax.text(
        xy[0],
        xy[1],
        label,
        ha="center",
        va="center",
        fontsize=fontsize,
        color=color,
        zorder=4,
    )
    return circ


def _edge(ax, p0, p1, *, dashed=False, color=None, rad=0.0, shrink=18):
    color = color or ("#7f8c8d" if dashed else "#1a5276")
    arrow = FancyArrowPatch(
        p0,
        p1,
        arrowstyle="-|>",
        mutation_scale=10,
        linewidth=1.4,
        linestyle="--" if dashed else "-",
        color=color,
        shrinkA=shrink,
        shrinkB=shrink,
        connectionstyle=f"arc3,rad={rad}",
        zorder=2,
    )
    ax.add_patch(arrow)


# #############################################################################
# Figure 1: illustrative PUCT search tree at the root of the five-city
# worked example (Section VI, Table I).
# #############################################################################

fig, ax = plt.subplots(figsize=(6.8, 4.1))
ax.set_xlim(-0.6, 6.6)
ax.set_ylim(-1.1, 3.8)
ax.set_aspect("equal")
ax.axis("off")

root = (3.0, 3.2)
c2 = (0.6, 1.6)
c3 = (2.2, 1.6)
c4 = (3.8, 1.6)
c5 = (5.4, 1.6)
leaf = (0.6, -0.5)

_node(ax, root, "$s_0$\n(start $c_1$)", radius=0.55, fontsize=7.5)
_node(ax, c2, "$c_2$\n$N{=}4,Q{=}{+}0.75$", radius=0.58, fontsize=6.8)
_node(ax, c3, "$c_3$\n$N{=}1,Q{=}{-}1.00$", dashed=True, radius=0.58, fontsize=6.8)
_node(ax, c4, "$c_4$\n$N{=}4,Q{=}{+}0.75$", radius=0.58, fontsize=6.8)
_node(ax, c5, "$c_5$\n$N{=}1,Q{=}{-}1.00$", dashed=True, radius=0.58, fontsize=6.8)
_node(ax, leaf, "tour complete\n$L{=}8.83,z{=}{+}1$", radius=0.62, fontsize=6.8)

_edge(ax, root, c2)
_edge(ax, root, c3, dashed=True)
_edge(ax, root, c4)
_edge(ax, root, c5, dashed=True)
_edge(ax, c2, leaf)

fig.tight_layout()
fig.savefig("figures/mcts_tree_schematic.png", dpi=300)
plt.close(fig)

print("Wrote figures/mcts_tree_schematic.png")

# #############################################################################
# Figure 2: curriculum self-play loop schematic (Section VI, overview
# figure).
# #############################################################################

fig, ax = plt.subplots(figsize=(6.8, 3.4))
ax.set_xlim(0, 11.4)
ax.set_ylim(-1.9, 3.0)
ax.set_aspect("equal")
ax.axis("off")

boxes = [
    (0.2, 1.2, 2.5, 1.3, "Instance generator\n(stage $n_k$)"),
    (3.3, 1.2, 2.7, 1.3, "Self-play MCTS\n+ network $\\pi_\\theta$"),
    (6.6, 1.2, 2.6, 1.3, "Ranked-reward\nbuffer $B_k$"),
]

centers = []
for x, y, w, h, label in boxes:
    box = FancyBboxPatch(
        (x, y),
        w,
        h,
        boxstyle="round,pad=0.08,rounding_size=0.08",
        facecolor="#eaf2f8",
        edgecolor="#1a5276",
        linewidth=1.4,
        zorder=3,
    )
    ax.add_patch(box)
    cx, cy = x + w / 2, y + h / 2
    centers.append((cx, cy, x, w))
    ax.text(cx, cy, label, ha="center", va="center", fontsize=8, zorder=4)

for i in range(len(centers) - 1):
    _, cy_i, x_i, w_i = centers[i]
    _, cy_j, x_j, _ = centers[i + 1]
    _edge(ax, (x_i + w_i, cy_i), (x_j, cy_j), shrink=2)

# Network-update box below, spanning under the self-play/buffer boxes.
ubox = (3.3, -1.5, 5.9, 1.3)
box = FancyBboxPatch(
    (ubox[0], ubox[1]),
    ubox[2],
    ubox[3],
    boxstyle="round,pad=0.08,rounding_size=0.08",
    facecolor="#fdebd0",
    edgecolor="#af601a",
    linewidth=1.4,
    zorder=3,
)
ax.add_patch(box)
ucx, ucy = ubox[0] + ubox[2] / 2, ubox[1] + ubox[3] / 2
ax.text(
    ucx,
    ucy,
    "Update $\\pi_\\theta$ on $(\\pi_{\\mathrm{MCTS}}, z)$",
    ha="center",
    va="center",
    fontsize=8,
    zorder=4,
)

# Buffer -> update (straight down).
bcx, bcy, bx, bw = centers[2]
_edge(ax, (bcx, bcy - 0.65), (ucx + 1.6, ucy + 0.65), shrink=2)

# Update -> self-play (curved feedback, same-stage inner loop).
scx, scy, sx, sw = centers[1]
_edge(
    ax,
    (ucx - 1.6, ucy + 0.65),
    (scx, scy - 0.65),
    color="#af601a",
    rad=0.25,
    shrink=2,
)

# Update -> instance generator (dashed outer loop: curriculum advance).
gcx, gcy, gx, gw = centers[0]
_edge(
    ax,
    (ubox[0], ucy - 0.35),
    (gcx - 0.3, gcy - 0.65),
    color="#7f8c8d",
    dashed=True,
    rad=-0.45,
    shrink=2,
)
ax.text(
    0.2,
    -1.75,
    "advance $n_k \\to n_{k+1}$ once win-rate threshold met",
    ha="left",
    va="center",
    fontsize=7,
    color="#7f8c8d",
    zorder=4,
)

fig.tight_layout()
fig.savefig("figures/curriculum_selfplay_loop.png", dpi=300)
plt.close(fig)

print("Wrote figures/curriculum_selfplay_loop.png")
