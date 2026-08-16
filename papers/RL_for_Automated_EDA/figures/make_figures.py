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


def _node(ax, xy, label, *, dashed=False, radius=0.42):
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
        fontsize=9,
        color=color,
        zorder=4,
    )
    return circ


def _edge(ax, p0, p1, *, dashed=False, color=None, rad=0.0, shrink=16):
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
# Figure 1: confounder example -- correct vs. spurious discovered graph
# (Section V, "Confounded features").
# #############################################################################

fig, axes = plt.subplots(1, 2, figsize=(5.2, 2.4))

for ax, title, spurious in zip(
    axes, ["(a) Correct: $\\hat{G}$ matches $G^*$", "(b) Naive: spurious edge added"], [False, True]
):
    ax.set_xlim(-0.2, 2.2)
    ax.set_ylim(-0.3, 1.9)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title(title, fontsize=8.5)

    u = (1.0, 1.5)
    x1 = (0.1, 0.1)
    x2 = (1.9, 0.1)

    _node(ax, u, "$U$", dashed=True)
    _node(ax, x1, "$X_1$")
    _node(ax, x2, "$X_2$")

    _edge(ax, u, x1, dashed=True)
    _edge(ax, u, x2, dashed=True)
    if spurious:
        _edge(ax, x1, x2, color="#c0392b")

fig.tight_layout()
fig.savefig("figures/confounder_example.png", dpi=300)
plt.close(fig)

print("Wrote figures/confounder_example.png")

# #############################################################################
# Figure 2: RLVR training-loop schematic (Section V, overview figure).
# #############################################################################

fig, ax = plt.subplots(figsize=(6.8, 3.2))
ax.set_xlim(0, 11.4)
ax.set_ylim(-1.9, 3.0)
ax.set_aspect("equal")
ax.axis("off")

boxes = [
    (0.2, 1.2, 2.1, 1.3, "Graph\ngenerator $\\mathcal{G}$"),
    (3.0, 1.2, 2.1, 1.3, "$G^*,\\ D_{train},\\ D_{test}$"),
    (5.8, 1.2, 2.3, 1.3, "Policy $\\pi_\\theta$\ntool calls over $T$"),
    (8.8, 1.2, 2.3, 1.3, "Discovered\ngraph $\\hat{G}$"),
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

# Reward box below, spanning under the policy/discovered-graph boxes.
rbox = (5.8, -1.5, 5.3, 1.3)
box = FancyBboxPatch(
    (rbox[0], rbox[1]),
    rbox[2],
    rbox[3],
    boxstyle="round,pad=0.08,rounding_size=0.08",
    facecolor="#fdebd0",
    edgecolor="#af601a",
    linewidth=1.4,
    zorder=3,
)
ax.add_patch(box)
rcx, rcy = rbox[0] + rbox[2] / 2, rbox[1] + rbox[3] / 2
ax.text(
    rcx,
    rcy,
    "Reward\n$r=\\mathrm{score}(\\hat{G}, G^*, D_{test})$",
    ha="center",
    va="center",
    fontsize=8,
    zorder=4,
)

# Discovered graph -> reward (straight down).
dcx, dcy, dx, dw = centers[3]
_edge(ax, (dcx, dcy - 0.65), (rcx + 1.3, rcy + 0.65), shrink=2)
# Reward -> back to policy, a curved feedback (policy-gradient update) arrow.
pcx, pcy, px, pw = centers[2]
_edge(
    ax,
    (rcx - 1.3, rcy + 0.65),
    (pcx, pcy - 0.65),
    color="#af601a",
    rad=0.25,
    shrink=2,
)

fig.tight_layout()
fig.savefig("figures/training_loop_schematic.png", dpi=300)
plt.close(fig)

print("Wrote figures/training_loop_schematic.png")
