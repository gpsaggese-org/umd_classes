"""
Generate the two figures used in `paper.md`.

Run with:
> python3 figures/make_figures.py
"""

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

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


def _box(ax, xy, w, h, label, *, dashed=False, face="#eaf2f8", edge="#1a5276"):
    x, y = xy
    box = FancyBboxPatch(
        (x - w / 2, y - h / 2),
        w,
        h,
        boxstyle="round,pad=0.06,rounding_size=0.08",
        facecolor=face,
        edgecolor=edge,
        linewidth=1.5,
        linestyle="--" if dashed else "-",
        zorder=3,
    )
    ax.add_patch(box)
    ax.text(x, y, label, ha="center", va="center", fontsize=8, zorder=4)


def _edge(ax, p0, p1, *, dashed=False, color="#1a5276", rad=0.0, shrink=14, lw=1.4):
    arrow = FancyArrowPatch(
        p0,
        p1,
        arrowstyle="-|>",
        mutation_scale=10,
        linewidth=lw,
        linestyle="--" if dashed else "-",
        color=color,
        shrinkA=shrink,
        shrinkB=shrink,
        connectionstyle=f"arc3,rad={rad}",
        zorder=2,
    )
    ax.add_patch(arrow)


# #############################################################################
# Figure 1: causal DAG relating confounders X, treatment T (founder age),
# mediator M (prior industry experience), outcome Y (startup success), and
# an unmeasured confounder U (founder ability). Section III.
# #############################################################################

fig, ax = plt.subplots(figsize=(6.6, 3.8))
ax.set_xlim(-1.0, 7.6)
ax.set_ylim(-2.6, 3.4)
ax.set_aspect("equal")
ax.axis("off")

X = (0.6, 1.9)
U = (4.4, 2.6)
T = (0.6, 0.0)
M = (3.0, 1.05)
Y = (6.0, 0.0)

_box(ax, X, 2.2, 0.9, "Confounders $X$\n(industry, team size,\nyear, geography)")
_box(ax, U, 2.3, 0.75, "Unmeasured $U$\n(founder ability)", dashed=True, face="white", edge="#7f8c8d")
_box(ax, T, 1.5, 0.75, "Age $T$", face="#fdebd0", edge="#af601a")
_box(ax, M, 2.0, 0.75, "Experience $M$")
_box(ax, Y, 1.6, 0.75, "Success $Y$", face="#fdebd0", edge="#af601a")

_edge(ax, X, T, rad=0.0)
_edge(ax, X, Y, rad=-0.32)
_edge(ax, T, M, rad=0.0)
_edge(ax, M, Y, rad=0.0)
_edge(ax, T, Y, rad=0.16, color="#c0392b", lw=1.8)
_edge(ax, U, T, dashed=True, color="#7f8c8d", rad=0.1)
_edge(ax, U, Y, dashed=True, color="#7f8c8d", rad=-0.1)

ax.text(3.0, -2.2, "Confounders (solid, blue) satisfy the backdoor criterion for the\n"
                    "total effect $T \\to Y$ (red); $M$ is a mediator, not a confounder,\n"
                    "and must be excluded from the adjustment set; $U$ is unobserved.",
        ha="center", va="center", fontsize=7.3, color="#333333")

fig.tight_layout()
fig.savefig("figures/causal_dag.png", dpi=300)
plt.close(fig)

print("Wrote figures/causal_dag.png")

# #############################################################################
# Figure 2: toy-example naive vs. propensity-score-matched (ATT) estimate of
# the age effect on the illustrative 10-founder dataset. Section VI.
# #############################################################################

labels = ["Naive\n(unadjusted)", "ATT\n(PSM-matched)"]
values = [0.267, 0.20]
colors = ["#95a5a6", "#1a5276"]

fig, ax = plt.subplots(figsize=(3.2, 2.4))
bars = ax.bar(labels, values, color=colors, width=0.55, zorder=3)
for bar, v in zip(bars, values):
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        v + 0.01,
        f"{v:.2f}",
        ha="center",
        va="bottom",
        fontsize=8.5,
    )
ax.axhline(0, color="black", linewidth=0.8, zorder=1)
ax.set_ylabel("Effect on P(success)")
ax.set_ylim(0, 0.34)
ax.spines[["top", "right"]].set_visible(False)
fig.tight_layout()
fig.savefig("figures/toy_example_att.png", dpi=300)
plt.close(fig)

print("Wrote figures/toy_example_att.png")
