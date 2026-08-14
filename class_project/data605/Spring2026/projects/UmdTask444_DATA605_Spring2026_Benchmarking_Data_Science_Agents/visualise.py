"""
visualize.py
------------
Stage 5: generate all figures from Parquet data.

What changed from v1
--------------------
- All data loading now uses DuckDB queries on Parquet files.
  No pandas.read_csv() anywhere in this file.
- Pandas DataFrames only appear at the very end when matplotlib/seaborn
  need them as plotting inputs — this is the correct architectural role
  for pandas in this stack.
- Figure data queries are small (final aggregates), so DuckDB returns
  them in microseconds.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
from pathlib import Path
from scipy.cluster.hierarchy import dendrogram

from db      import query_df
from storage import read_as_pandas, parquet_path

FIGURES_DIR = Path(__file__).resolve().parents[1] / "outputs" / "figures"
TABLES_DIR  = Path(__file__).resolve().parents[1] / "outputs" / "tables"
FIGURES_DIR.mkdir(parents=True, exist_ok=True)
TABLES_DIR.mkdir(parents=True, exist_ok=True)

PALETTE = {
    "datasci_bench": "#4C72B0",
    "dsbench":       "#DD8452",
    "mle_bench":     "#55A868",
    "gaia":          "#C44E52",
    "swe_bench":     "#8172B2",
}
LABELS = {
    "datasci_bench": "DataSciBench",
    "dsbench":       "DSBench",
    "mle_bench":     "MLE-Bench",
    "gaia":          "GAIA",
    "swe_bench":     "SWE-bench",
}

sns.set_theme(style="whitegrid", font_scale=1.1)
plt.rcParams.update({"figure.dpi": 150, "savefig.bbox": "tight"})


def _load_matrix() -> pd.DataFrame:
    """Load unified score matrix via DuckDB (small final result → pandas OK)."""
    return query_df(f"SELECT * FROM read_parquet('{parquet_path('unified_scores')}')")


def plot_score_heatmap(top_n: int = 25) -> str:
    """Heatmap of agent × benchmark normalised scores."""
    # DuckDB query: top N agents by mean score
    sql = f"""
    SELECT *
    FROM read_parquet('{parquet_path('unified_scores')}')
    ORDER BY (
        SELECT AVG(v) FROM (
            SELECT UNNEST(list_apply(
                list_filter(columns(*), c -> c != 'agent'), x -> x::DOUBLE
            )) AS v
        )
    ) DESC NULLS LAST
    LIMIT {top_n}
    """
    # DuckDB UNNEST on dynamic columns is complex; use pandas for the top-n sort
    df = _load_matrix()
    score_cols = [c for c in df.columns if c != "agent"]
    df = df.set_index("agent")
    df["_mean"] = df[score_cols].mean(axis=1)
    display = df.nlargest(top_n, "_mean").drop(columns="_mean")
    display.columns = [LABELS.get(c, c) for c in display.columns]

    fig, ax = plt.subplots(figsize=(10, max(6, top_n * 0.35)))
    sns.heatmap(display, ax=ax, cmap="YlOrRd", annot=True, fmt=".1f",
                linewidths=0.4, vmin=0, vmax=100,
                cbar_kws={"label": "Normalised Score (0–100)"})
    ax.set_title("Agent Performance Across Benchmarks", fontsize=14, pad=12)
    ax.tick_params(axis="x", rotation=30)
    ax.tick_params(axis="y", rotation=0)
    path = str(FIGURES_DIR / "heatmap_scores.png")
    fig.savefig(path)
    plt.close(fig)
    print(f"  💾 heatmap_scores.png")
    return path


def plot_correlation_heatmap() -> str:
    """Pairwise Spearman correlation between benchmarks."""
    corr = read_as_pandas("benchmark_correlation")
    # First column may be the index label
    if corr.columns[0] in ("benchmark", "index", ""):
        corr = corr.set_index(corr.columns[0])
    corr.index   = [LABELS.get(c, c) for c in corr.index]
    corr.columns = [LABELS.get(c, c) for c in corr.columns]

    mask = np.triu(np.ones_like(corr, dtype=bool), k=1)
    fig, ax = plt.subplots(figsize=(7, 6))
    sns.heatmap(corr, ax=ax, mask=mask, cmap="coolwarm", center=0,
                vmin=-1, vmax=1, annot=True, fmt=".2f", square=True,
                linewidths=0.5, cbar_kws={"label": "Spearman ρ"})
    ax.set_title("Benchmark Rank Correlation (Spearman ρ)", fontsize=13)
    ax.tick_params(axis="x", rotation=30)
    ax.tick_params(axis="y", rotation=0)
    path = str(FIGURES_DIR / "correlation_benchmarks.png")
    fig.savefig(path)
    plt.close(fig)
    print(f"  💾 correlation_benchmarks.png")
    return path


def plot_radar_chart(top_n: int = 6) -> str:
    """Radar chart: per-agent capability profiles."""
    df = _load_matrix()
    score_cols = [c for c in df.columns if c != "agent"]
    df = df.set_index("agent")
    agents = df.fillna(0).mean(axis=1).nlargest(top_n).index.tolist()
    labels = [LABELS.get(b, b) for b in score_cols]
    N = len(score_cols)
    angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw={"polar": True})
    cmap = plt.cm.get_cmap("tab10", top_n)
    for idx, agent in enumerate(agents):
        vals = [df.loc[agent, b] if pd.notna(df.loc[agent, b]) else 0 for b in score_cols]
        vals += vals[:1]
        ax.plot(angles, vals, "o-", lw=1.8, color=cmap(idx), label=agent, alpha=0.85)
        ax.fill(angles, vals, alpha=0.08, color=cmap(idx))
    ax.set_thetagrids(np.degrees(angles[:-1]), labels, fontsize=10)
    ax.set_ylim(0, 100)
    ax.set_title("Agent Capability Profiles", fontsize=14, pad=20)
    ax.legend(loc="upper right", bbox_to_anchor=(1.35, 1.15), fontsize=9)
    path = str(FIGURES_DIR / "radar_agent_profiles.png")
    fig.savefig(path)
    plt.close(fig)
    print(f"  💾 radar_agent_profiles.png")
    return path


def plot_top_agents_bar() -> str:
    """Grouped bar chart: top 8 agents per benchmark."""
    # DuckDB query — data already computed in analyze.py
    top = query_df(f"SELECT * FROM read_parquet('{parquet_path('top_agents')}')")
    benchmarks = top["benchmark"].unique().tolist()
    ncols = 2
    nrows = int(np.ceil(len(benchmarks) / ncols))

    fig, axes = plt.subplots(nrows, ncols, figsize=(14, nrows * 4.5))
    axes = axes.flatten()

    for i, bench in enumerate(benchmarks):
        ax   = axes[i]
        data = top[top["benchmark"] == bench].sort_values("score_norm")
        color = PALETTE.get(bench, "#4C72B0")
        bars = ax.barh(data["agent"], data["score_norm"], color=color, alpha=0.85, edgecolor="white")
        ax.set_xlim(0, 105)
        ax.set_title(LABELS.get(bench, bench), fontsize=12, fontweight="bold")
        ax.set_xlabel("Normalised Score")
        ax.bar_label(bars, fmt="%.1f", padding=3, fontsize=8)
        ax.tick_params(axis="y", labelsize=8)

    for j in range(len(benchmarks), len(axes)):
        axes[j].set_visible(False)

    fig.suptitle("Top Agents per Benchmark", fontsize=15, y=1.01)
    fig.tight_layout()
    path = str(FIGURES_DIR / "top_agents_bar.png")
    fig.savefig(path)
    plt.close(fig)
    print(f"  💾 top_agents_bar.png")
    return path


def plot_dendrogram(linkage_matrix: np.ndarray, agent_names: list[str]) -> str:
    """Hierarchical clustering dendrogram."""
    fig, ax = plt.subplots(figsize=(14, max(5, len(agent_names) * 0.25)))
    dendrogram(linkage_matrix, labels=agent_names, orientation="right", ax=ax,
               leaf_font_size=8, color_threshold=0.7 * max(linkage_matrix[:, 2]))
    ax.set_title("Agent Clustering Dendrogram (Ward Linkage)", fontsize=13)
    ax.set_xlabel("Distance")
    fig.tight_layout()
    path = str(FIGURES_DIR / "dendrogram_clustering.png")
    fig.savefig(path)
    plt.close(fig)
    print(f"  💾 dendrogram_clustering.png")
    return path


def plot_capability_gaps(top_n: int = 20) -> str:
    """Bubble chart: strengths and gaps per agent."""
    # DuckDB query: top N agents by mean score
    gaps = query_df(f"""
        WITH top_agents AS (
            SELECT agent, AVG(score_norm) AS mean_score
            FROM read_parquet('{parquet_path('capability_gaps')}')
            GROUP BY agent
            ORDER BY mean_score DESC
            LIMIT {top_n}
        )
        SELECT g.*
        FROM read_parquet('{parquet_path('capability_gaps')}') g
        INNER JOIN top_agents t ON g.agent = t.agent
    """)

    color_map = {"strength": "#2ecc71", "average": "#95a5a6", "gap": "#e74c3c"}
    gaps["color"] = gaps["flag"].map(color_map)
    gaps["size"]  = (gaps["z_score"].abs() * 200).clip(50, 600)

    agents     = gaps["agent"].unique().tolist()
    benchmarks = gaps["benchmark"].unique().tolist()
    bench_idx  = {b: i for i, b in enumerate(benchmarks)}
    agent_idx  = {a: i for i, a in enumerate(agents)}

    fig, ax = plt.subplots(figsize=(11, max(6, len(agents) * 0.45)))
    for _, row in gaps.iterrows():
        ax.scatter(bench_idx[row["benchmark"]], agent_idx[row["agent"]],
                   s=row["size"], c=row["color"], alpha=0.75,
                   edgecolors="white", linewidths=0.5)
    ax.set_xticks(range(len(bench_idx)))
    ax.set_xticklabels([LABELS.get(b, b) for b in bench_idx], rotation=25, ha="right")
    ax.set_yticks(range(len(agent_idx)))
    ax.set_yticklabels(list(agent_idx.keys()), fontsize=8)
    ax.set_title("Capability Strengths & Gaps (bubble size = |z-score|)", fontsize=13)
    handles = [
        mpatches.Patch(color="#2ecc71", label="Strength (z > 1)"),
        mpatches.Patch(color="#95a5a6", label="Average"),
        mpatches.Patch(color="#e74c3c", label="Gap (z < −1)"),
    ]
    ax.legend(handles=handles, loc="lower right", fontsize=9)
    fig.tight_layout()
    path = str(FIGURES_DIR / "capability_gaps.png")
    fig.savefig(path)
    plt.close(fig)
    print(f"  💾 capability_gaps.png")
    return path


def generate_all_figures() -> list[str]:
    """Generate all figures. Called by the LangGraph visualize node."""
    TABLES_DIR_PATH = Path(__file__).resolve().parents[1] / "outputs" / "tables"
    linkage_path = TABLES_DIR_PATH / "linkage_matrix.npy"
    saved = []

    print("── HEATMAP ──")
    saved.append(plot_score_heatmap())

    print("── CORRELATION ──")
    saved.append(plot_correlation_heatmap())

    print("── RADAR ──")
    saved.append(plot_radar_chart())

    print("── BAR CHART ──")
    saved.append(plot_top_agents_bar())

    print("── DENDROGRAM ──")
    if linkage_path.exists():
        lm     = np.load(str(linkage_path))
        matrix = query_df(f"SELECT * FROM read_parquet('{parquet_path('unified_scores')}')")
        agents = matrix["agent"].tolist()
        saved.append(plot_dendrogram(lm, agents))
    else:
        print("  ⚠ linkage_matrix.npy not found — skipping dendrogram")

    print("── GAPS ──")
    saved.append(plot_capability_gaps())

    print(f"\n✅ {len(saved)} figures saved to outputs/figures/")
    return saved


if __name__ == "__main__":
    generate_all_figures()
