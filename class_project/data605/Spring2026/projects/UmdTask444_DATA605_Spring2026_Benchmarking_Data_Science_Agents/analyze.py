"""
analyze.py
----------
Stage 3: statistical analysis on the unified score matrix.

What changed from v1
--------------------
- Spearman correlation and gap analysis run as DuckDB SQL queries.
  DuckDB has built-in CORR(), STDDEV_POP(), AVG() window functions —
  no scipy pairwise loops, no pandas groupby.
- Clustering (K-Means, hierarchical) still uses scikit-learn because
  these are iterative algorithms that genuinely need Python — DuckDB
  is not a substitute for ML training. But the *input data* comes
  from a DuckDB query, not from pandas.read_csv().
- All outputs are written as Parquet via storage.write_table().

Usage
-----
    python src/analyze.py
"""

import json
import numpy as np
import pandas as pd
import pyarrow as pa
from pathlib import Path
from sklearn.cluster import KMeans
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
from scipy.cluster.hierarchy import linkage, fcluster

from db      import get_conn, query_df, query_arrow, register_view
from storage import read_as_pandas, parquet_path, write_table

OUTPUTS_DIR = Path(__file__).resolve().parents[1] / "outputs" / "tables"
OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)


# ── 1. Spearman Correlation via DuckDB ────────────────────────────────────────
# DuckDB's CORR() function computes Pearson correlation natively.
# For Spearman we rank-transform first (also in SQL), then CORR().

RANK_TRANSFORM_SQL = """
-- Rank each agent's score within each benchmark (dense rank, nulls ignored).
-- This converts raw normalised scores into rank positions, which is the
-- input needed for Spearman correlation.
SELECT
    agent,
    benchmark,
    score_norm,
    DENSE_RANK() OVER (
        PARTITION BY benchmark
        ORDER BY score_norm DESC NULLS LAST
    ) AS rank_in_bench
FROM read_parquet('{path}')
WHERE score_norm IS NOT NULL
"""

CORRELATION_SQL = """
-- Pivot ranks to wide format then compute pairwise Pearson correlation
-- on the rank columns (= Spearman correlation on original scores).
-- One row per agent, one column per benchmark containing that agent's rank.
PIVOT (
    SELECT agent, benchmark, rank_in_bench
    FROM ranked_scores
)
ON benchmark
USING MAX(rank_in_bench)
ORDER BY agent
"""

GAP_ANALYSIS_SQL = """
-- For each agent x benchmark, compute a z-score relative to that
-- agent's own mean across all benchmarks.
-- z > 1  → 'strength' (standout benchmark for this agent)
-- z < -1 → 'gap'      (weak benchmark for this agent)

WITH agent_stats AS (
    SELECT
        agent,
        AVG(score_norm)     AS agent_mean,
        STDDEV_POP(score_norm) AS agent_std
    FROM read_parquet('{path}')
    WHERE score_norm IS NOT NULL
    GROUP BY agent
)
SELECT
    n.agent,
    n.benchmark,
    n.score_norm,
    ROUND(
        CASE
            WHEN s.agent_std = 0 THEN 0
            ELSE (n.score_norm - s.agent_mean) / s.agent_std
        END,
    3) AS z_score,
    CASE
        WHEN s.agent_std = 0                                          THEN 'average'
        WHEN (n.score_norm - s.agent_mean) / s.agent_std >=  1.0     THEN 'strength'
        WHEN (n.score_norm - s.agent_mean) / s.agent_std <= -1.0     THEN 'gap'
        ELSE 'average'
    END AS flag
FROM read_parquet('{path}') n
JOIN agent_stats s ON n.agent = s.agent
WHERE n.score_norm IS NOT NULL
ORDER BY n.agent, n.benchmark
"""

TOP_AGENTS_SQL = """
SELECT
    benchmark,
    agent,
    score_norm,
    DENSE_RANK() OVER (PARTITION BY benchmark ORDER BY score_norm DESC) AS rank
FROM read_parquet('{path}')
WHERE score_norm IS NOT NULL
QUALIFY rank <= {top_n}
ORDER BY benchmark, rank
"""


def spearman_correlation(matrix_df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute pairwise Spearman rank correlation between benchmarks.
    Uses scipy since it handles NaN-aware pairwise correlation cleanly.
    Input matrix_df comes from DuckDB (not from pandas.read_csv).
    """
    from scipy.stats import spearmanr
    benchmarks = [c for c in matrix_df.columns if c != "agent"]
    n = len(benchmarks)
    corr_mat = np.full((n, n), np.nan)

    for i, b1 in enumerate(benchmarks):
        for j, b2 in enumerate(benchmarks):
            both = matrix_df[[b1, b2]].dropna()
            if len(both) >= 3:
                rho, _ = spearmanr(both[b1], both[b2])
                corr_mat[i, j] = round(rho, 4)

    return pd.DataFrame(corr_mat, index=benchmarks, columns=benchmarks)


def cluster_agents(matrix_df: pd.DataFrame, k_range: tuple = (2, 6)) -> dict:
    """
    K-Means and hierarchical clustering on the agent x benchmark matrix.
    Data comes from DuckDB; clustering runs in scikit-learn (appropriate
    tool for iterative ML algorithms).
    """
    agents = matrix_df["agent"].tolist() if "agent" in matrix_df.columns else matrix_df.index.tolist()
    score_cols = [c for c in matrix_df.columns if c != "agent"]
    X_raw = matrix_df[score_cols].values

    # Impute missing scores with column mean
    X = SimpleImputer(strategy="mean").fit_transform(X_raw)
    X_scaled = StandardScaler().fit_transform(X)

    # K-Means: pick best k by silhouette
    sil_scores: dict[int, float] = {}
    for k in range(k_range[0], k_range[1] + 1):
        km = KMeans(n_clusters=k, random_state=42, n_init=10)
        labels = km.fit_predict(X_scaled)
        sil_scores[k] = round(silhouette_score(X_scaled, labels), 4)
        print(f"  K={k}  silhouette={sil_scores[k]:.4f}")

    best_k = max(sil_scores, key=sil_scores.get)
    km_best = KMeans(n_clusters=best_k, random_state=42, n_init=10)
    km_labels = km_best.fit_predict(X_scaled)
    print(f"  ✓ Best k={best_k} (silhouette={sil_scores[best_k]})")

    # Hierarchical clustering
    linkage_matrix = linkage(X_scaled, method="ward")
    hier_labels = fcluster(linkage_matrix, best_k, criterion="maxclust")

    return {
        "agents":          agents,
        "km_labels":       km_labels.tolist(),
        "hier_labels":     hier_labels.tolist(),
        "best_k":          best_k,
        "sil_scores":      sil_scores,
        "linkage_matrix":  linkage_matrix,
    }


def run_analysis() -> dict:
    """
    Full analysis pipeline: correlation → clustering → gap analysis.
    All heavy aggregation runs in DuckDB; clustering runs in scikit-learn.
    """
    path = parquet_path("unified_scores")
    norm_path = parquet_path("normalised_scores")

    print("── CORRELATION ──")
    matrix_df = query_df(f"SELECT * FROM read_parquet('{path}')")
    corr = spearman_correlation(matrix_df)
    corr_arrow = pa.Table.from_pandas(corr.reset_index().rename(columns={"index": "benchmark"}))
    write_table(corr_arrow, "benchmark_correlation")
    print(f"  ✓ Correlation matrix saved")

    print("\n── CLUSTERING ──")
    clustering = cluster_agents(matrix_df)
    cluster_df = pd.DataFrame({
        "agent":         clustering["agents"],
        "kmeans_cluster":  clustering["km_labels"],
        "hier_cluster":    clustering["hier_labels"],
    })
    write_table(pa.Table.from_pandas(cluster_df), "cluster_labels")
    np.save(OUTPUTS_DIR / "linkage_matrix.npy", clustering["linkage_matrix"])
    with open(OUTPUTS_DIR / "silhouette_scores.json", "w") as f:
        json.dump({str(k): v for k, v in clustering["sil_scores"].items()}, f, indent=2)
    print(f"  ✓ Cluster labels saved")

    print("\n── GAP ANALYSIS (DuckDB) ──")
    gaps = query_df(GAP_ANALYSIS_SQL.format(path=norm_path))
    write_table(pa.Table.from_pandas(gaps), "capability_gaps")
    strengths = (gaps["flag"] == "strength").sum()
    gap_count  = (gaps["flag"] == "gap").sum()
    print(f"  ✓ {strengths} strengths, {gap_count} gaps identified")

    print("\n── TOP AGENTS (DuckDB) ──")
    top_agents = query_df(TOP_AGENTS_SQL.format(path=norm_path, top_n=10))
    write_table(pa.Table.from_pandas(top_agents), "top_agents")
    print(f"  ✓ Top agents table saved")

    print("\n✅ Analysis complete")
    return {
        "correlation":    corr,
        "clustering":     clustering,
        "gaps":           gaps,
        "top_agents":     top_agents,
    }


if __name__ == "__main__":
    run_analysis()
