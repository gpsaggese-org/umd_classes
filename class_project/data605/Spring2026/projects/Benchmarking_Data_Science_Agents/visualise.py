"""
visualize.py
------------
Stage 4: Generate all figures from the 4 benchmark analysis.

Figures:
  1. Benchmark size comparison (bar chart)
  2. Chatbot Arena top model win rates (horizontal bar)
  3. MLE-bench score distributions (box plot)
  4. Agent clustering heatmap
  5. Benchmark correlation heatmap
  6. Capability gaps bubble chart
  7. GAIA difficulty level distribution
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
from pathlib import Path
from scipy.cluster.hierarchy import dendrogram

from db      import query_df
from storage import parquet_path, read_as_pandas

ROOT        = Path(__file__).resolve().parent
FIGURES_DIR = ROOT / "outputs" / "figures"
TABLES_DIR  = ROOT / "outputs" / "tables"
FIGURES_DIR.mkdir(parents=True, exist_ok=True)

PALETTE = {
    "chatbot_arena": "#4C72B0",
    "swe_bench":     "#DD8452",
    "mle_bench":     "#55A868",
    "gaia":          "#C44E52",
}
LABELS = {
    "chatbot_arena": "Chatbot Arena",
    "swe_bench":     "SWE-bench",
    "mle_bench":     "MLE-bench",
    "gaia":          "GAIA",
}

sns.set_theme(style="whitegrid", font_scale=1.1)
plt.rcParams.update({"figure.dpi": 150, "savefig.bbox": "tight"})


def plot_benchmark_sizes() -> str:
    """Bar chart showing row counts per benchmark."""
    df = read_as_pandas("benchmark_stats")
    fig, ax = plt.subplots(figsize=(8, 5))
    colors = [PALETTE.get(b, "#888") for b in df["benchmark"]]
    bars = ax.bar(
        [LABELS.get(b, b) for b in df["benchmark"]],
        df["total_rows"],
        color=colors, alpha=0.85, edgecolor="white"
    )
    ax.bar_label(bars, fmt="%,.0f", padding=5, fontsize=10)
    ax.set_title("Dataset Size per Benchmark", fontsize=14, pad=12)
    ax.set_ylabel("Number of Rows")
    ax.tick_params(axis="x", rotation=15)
    path = str(FIGURES_DIR / "benchmark_sizes.png")
    fig.savefig(path)
    plt.close(fig)
    print(f"  💾 benchmark_sizes.png")
    return path


def plot_chatbot_arena_winrates(top_n: int = 20) -> str:
    """Horizontal bar chart of top model win rates in Chatbot Arena."""
    df = read_as_pandas("chatbot_arena_winrates").head(top_n)
    df = df.sort_values("win_rate_pct")
    fig, ax = plt.subplots(figsize=(10, max(6, top_n * 0.4)))
    bars = ax.barh(df["model"], df["win_rate_pct"],
                   color=PALETTE["chatbot_arena"], alpha=0.85, edgecolor="white")
    ax.bar_label(bars, fmt="%.1f%%", padding=3, fontsize=8)
    ax.set_title(f"Top {top_n} Models — Chatbot Arena Win Rate", fontsize=14)
    ax.set_xlabel("Win Rate (%)")
    ax.axvline(50, color="red", linestyle="--", alpha=0.5, label="50% baseline")
    ax.legend(fontsize=9)
    path = str(FIGURES_DIR / "chatbot_arena_winrates.png")
    fig.savefig(path)
    plt.close(fig)
    print(f"  💾 chatbot_arena_winrates.png")
    return path


def plot_mle_bench_scores() -> str:
    """Box plot of score distributions across MLE-bench competitions."""
    path = parquet_path("bench_mle_bench")
    df = query_df(f"""
        SELECT competition, CAST(score AS DOUBLE) AS score
        FROM read_parquet('{path}')
        WHERE score IS NOT NULL
        ORDER BY competition
        LIMIT 5000
    """)
    top_comps = df.groupby("competition").size().nlargest(15).index.tolist()
    df = df[df["competition"].isin(top_comps)]

    fig, ax = plt.subplots(figsize=(14, 6))
    df.boxplot(column="score", by="competition", ax=ax, rot=45,
               boxprops=dict(color=PALETTE["mle_bench"]),
               medianprops=dict(color="red"))
    ax.set_title("Score Distribution per Kaggle Competition (MLE-bench)", fontsize=13)
    ax.set_xlabel("")
    ax.set_ylabel("Score")
    plt.suptitle("")
    path_out = str(FIGURES_DIR / "mle_bench_scores.png")
    fig.savefig(path_out)
    plt.close(fig)
    print(f"  💾 mle_bench_scores.png")
    return path_out


def plot_correlation_heatmap() -> str:
    """Benchmark correlation heatmap."""
    corr = read_as_pandas("benchmark_correlation")
    if "benchmark" in corr.columns:
        corr = corr.set_index("benchmark")
    corr.index   = [LABELS.get(c, c) for c in corr.index]
    corr.columns = [LABELS.get(c, c) for c in corr.columns]

    fig, ax = plt.subplots(figsize=(7, 6))
    mask = np.triu(np.ones_like(corr, dtype=bool), k=1)
    sns.heatmap(corr, ax=ax, mask=mask, cmap="coolwarm", center=0,
                vmin=-1, vmax=1, annot=True, fmt=".2f", square=True,
                linewidths=0.5, cbar_kws={"label": "Spearman rho"})
    ax.set_title("Benchmark Rank Correlation", fontsize=13)
    ax.tick_params(axis="x", rotation=30)
    path = str(FIGURES_DIR / "correlation_heatmap.png")
    fig.savefig(path)
    plt.close(fig)
    print(f"  💾 correlation_heatmap.png")
    return path


def plot_agent_clusters() -> str:
    """Scatter plot of agent clusters."""
    matrix  = read_as_pandas("unified_scores")
    cluster = read_as_pandas("cluster_labels")
    merged  = matrix.merge(cluster, on="agent", how="left")

    score_cols = [c for c in matrix.columns if c != "agent"]
    if len(score_cols) < 2:
        print("  ⚠ Not enough benchmarks for scatter plot")
        return ""

    x_col = score_cols[0]
    y_col = score_cols[1] if len(score_cols) > 1 else score_cols[0]

    fig, ax = plt.subplots(figsize=(9, 7))
    for cluster_id in sorted(merged["kmeans_cluster"].dropna().unique()):
        group = merged[merged["kmeans_cluster"] == cluster_id]
        ax.scatter(group[x_col], group[y_col],
                   label=f"Cluster {int(cluster_id)}",
                   alpha=0.6, s=30)
    ax.set_xlabel(LABELS.get(x_col, x_col))
    ax.set_ylabel(LABELS.get(y_col, y_col))
    ax.set_title("Agent Clusters by Benchmark Performance", fontsize=13)
    ax.legend(fontsize=9)
    path = str(FIGURES_DIR / "agent_clusters.png")
    fig.savefig(path)
    plt.close(fig)
    print(f"  💾 agent_clusters.png")
    return path


def plot_gaia_difficulty() -> str:
    """Bar chart of GAIA task difficulty distribution."""
    path = parquet_path("bench_gaia")
    df = query_df(f"""
        SELECT Level, COUNT(*) AS count
        FROM read_parquet('{path}')
        WHERE Level IS NOT NULL
        GROUP BY Level
        ORDER BY Level
    """)
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.bar(df["Level"].astype(str), df["count"],
           color=PALETTE["gaia"], alpha=0.85, edgecolor="white")
    ax.set_title("GAIA Task Difficulty Distribution", fontsize=13)
    ax.set_xlabel("Difficulty Level")
    ax.set_ylabel("Number of Tasks")
    for i, (_, row) in enumerate(df.iterrows()):
        ax.text(i, row["count"] + 1, str(row["count"]), ha="center", fontsize=10)
    path_out = str(FIGURES_DIR / "gaia_difficulty.png")
    fig.savefig(path_out)
    plt.close(fig)
    print(f"  💾 gaia_difficulty.png")
    return path_out


def plot_dendrogram() -> str:
    """Hierarchical clustering dendrogram of agents."""
    linkage_path = TABLES_DIR / "linkage_matrix.npy"
    if not linkage_path.exists():
        print("  ⚠ linkage_matrix.npy not found — skipping dendrogram")
        return ""
    lm     = np.load(str(linkage_path))
    matrix = read_as_pandas("unified_scores")
    agents = matrix["agent"].tolist()

    fig, ax = plt.subplots(figsize=(14, max(5, len(agents[:50]) * 0.3)))
    dendrogram(lm, labels=agents[:50], orientation="right", ax=ax,
               leaf_font_size=7,
               color_threshold=0.7 * max(lm[:, 2]))
    ax.set_title("Agent Clustering Dendrogram (Ward Linkage)", fontsize=13)
    ax.set_xlabel("Distance")
    fig.tight_layout()
    path = str(FIGURES_DIR / "dendrogram.png")
    fig.savefig(path)
    plt.close(fig)
    print(f"  💾 dendrogram.png")
    return path


def generate_all_figures() -> list:
    print("=" * 50)
    print("VISUALIZE: Generating all figures")
    print("=" * 50)
    saved = []

    print("\n── BENCHMARK SIZES ──")
    saved.append(plot_benchmark_sizes())

    print("\n── CHATBOT ARENA WIN RATES ──")
    saved.append(plot_chatbot_arena_winrates())

    print("\n── MLE-BENCH SCORES ──")
    saved.append(plot_mle_bench_scores())

    print("\n── CORRELATION HEATMAP ──")
    saved.append(plot_correlation_heatmap())

    print("\n── AGENT CLUSTERS ──")
    saved.append(plot_agent_clusters())

    print("\n── GAIA DIFFICULTY ──")
    saved.append(plot_gaia_difficulty())

    print("\n── DENDROGRAM ──")
    saved.append(plot_dendrogram())

    saved = [s for s in saved if s]
    print(f"\n✅ {len(saved)} figures saved to outputs/figures/")
    return saved


if __name__ == "__main__":
    generate_all_figures()
