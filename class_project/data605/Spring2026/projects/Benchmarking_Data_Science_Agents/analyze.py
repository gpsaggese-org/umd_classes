"""
analyze.py
----------
Stage 3: Statistical analysis on the 4 real benchmarks.

Benchmarks: chatbot_arena, swe_bench, mle_bench, gaia
Data: 68,185 rows in unified_data.parquet
      1,274 agents x 4 benchmarks in unified_scores.parquet

Analysis:
  1. Per-benchmark statistics via DuckDB SQL
  2. Agent win rate analysis (chatbot_arena)
  3. Competition score distribution (mle_bench)
  4. Spearman correlation between benchmarks
  5. K-Means clustering of agents
  6. Capability gap analysis
"""

import json
import numpy as np
import pandas as pd
import pyarrow as pa
from pathlib import Path
from scipy.stats import spearmanr
from sklearn.cluster import KMeans
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
from scipy.cluster.hierarchy import linkage, fcluster

from db      import query_df, query_arrow, get_conn
from storage import parquet_path, write_table, read_as_pandas

ROOT        = Path(__file__).resolve().parent
TABLES_DIR  = ROOT / "outputs" / "tables"
TABLES_DIR.mkdir(parents=True, exist_ok=True)


# ── 1. Per-benchmark statistics ───────────────────────────────────────────────

def benchmark_stats() -> pd.DataFrame:
    """Compute summary statistics for each benchmark using DuckDB."""
    path = parquet_path("unified_data")
    df = query_df(f"""
        SELECT
            benchmark,
            COUNT(*)                    AS total_rows,
            COUNT(DISTINCT agent)       AS unique_agents,
            COUNT(DISTINCT task)        AS unique_tasks,
            ROUND(AVG(score), 4)        AS mean_score,
            ROUND(STDDEV(score), 4)     AS std_score,
            ROUND(MIN(score), 4)        AS min_score,
            ROUND(MAX(score), 4)        AS max_score
        FROM read_parquet('{path}')
        GROUP BY benchmark
        ORDER BY benchmark
    """)
    print("  ✓ Benchmark statistics computed")
    return df


# ── 2. Top agents per benchmark ───────────────────────────────────────────────

def top_agents_per_benchmark(top_n: int = 20) -> pd.DataFrame:
    """Find top performing agents in each benchmark."""
    path = parquet_path("unified_data")
    df = query_df(f"""
        WITH ranked AS (
            SELECT
                benchmark,
                agent,
                ROUND(AVG(score), 4)    AS mean_score,
                COUNT(*)                AS n_tasks,
                DENSE_RANK() OVER (
                    PARTITION BY benchmark
                    ORDER BY AVG(score) DESC
                )                       AS rank
            FROM read_parquet('{path}')
            WHERE agent IS NOT NULL
            GROUP BY benchmark, agent
        )
        SELECT * FROM ranked
        WHERE rank <= {top_n}
        ORDER BY benchmark, rank
    """)
    print(f"  ✓ Top {top_n} agents per benchmark computed")
    return df


# ── 3. Chatbot Arena win rate analysis ────────────────────────────────────────

def chatbot_arena_analysis() -> pd.DataFrame:
    """
    Analyse win rates per model in Chatbot Arena.
    Uses DuckDB window functions for efficiency.
    """
    path = parquet_path("bench_chatbot_arena")
    df = query_df(f"""
        WITH model_scores AS (
            SELECT
                model_a AS model,
                CASE WHEN winner = 'model_a' THEN 1.0
                     WHEN winner = 'tie' THEN 0.5
                     ELSE 0.0 END AS won
            FROM read_parquet('{path}')
            WHERE model_a IS NOT NULL
            UNION ALL
            SELECT
                model_b AS model,
                CASE WHEN winner = 'model_b' THEN 1.0
                     WHEN winner = 'tie' THEN 0.5
                     ELSE 0.0 END AS won
            FROM read_parquet('{path}')
            WHERE model_b IS NOT NULL
        )
        SELECT
            model,
            COUNT(*)                        AS total_battles,
            ROUND(SUM(won), 0)              AS wins,
            ROUND(AVG(won) * 100, 2)        AS win_rate_pct
        FROM model_scores
        GROUP BY model
        HAVING COUNT(*) >= 10
        ORDER BY win_rate_pct DESC
        LIMIT 50
    """)
    print(f"  ✓ Chatbot Arena win rates: {len(df)} models")
    return df


# ── 4. MLE-bench competition analysis ────────────────────────────────────────

def mle_bench_analysis() -> pd.DataFrame:
    """Analyse score distributions across Kaggle competitions."""
    path = parquet_path("bench_mle_bench")
    df = query_df(f"""
        SELECT
            competition,
            COUNT(*)                    AS n_teams,
            ROUND(AVG(score), 4)        AS mean_score,
            ROUND(STDDEV(score), 4)     AS std_score,
            ROUND(MIN(score), 4)        AS min_score,
            ROUND(MAX(score), 4)        AS max_score
        FROM read_parquet('{path}')
        WHERE score IS NOT NULL
        GROUP BY competition
        ORDER BY n_teams DESC
    """)
    print(f"  ✓ MLE-bench competition stats: {len(df)} competitions")
    return df


# ── 5. Spearman correlation ───────────────────────────────────────────────────

def benchmark_correlation(matrix_df: pd.DataFrame) -> pd.DataFrame:
    """Spearman rank correlation between benchmarks."""
    benchmarks = [c for c in matrix_df.columns if c != "agent"]
    n = len(benchmarks)
    corr_mat = np.full((n, n), np.nan)
    for i, b1 in enumerate(benchmarks):
        for j, b2 in enumerate(benchmarks):
            both = matrix_df[[b1, b2]].dropna()
            if len(both) >= 3:
                rho, _ = spearmanr(both[b1], both[b2])
                corr_mat[i, j] = round(rho, 4)
    corr_df = pd.DataFrame(corr_mat, index=benchmarks, columns=benchmarks)
    print(f"  ✓ Spearman correlation matrix computed")
    return corr_df


# ── 6. K-Means clustering ────────────────────────────────────────────────────

def cluster_agents(matrix_df: pd.DataFrame, k_range: tuple = (2, 6)) -> dict:
    """Cluster agents by benchmark performance profile."""
    agents = matrix_df["agent"].tolist() if "agent" in matrix_df.columns else matrix_df.index.tolist()
    score_cols = [c for c in matrix_df.columns if c != "agent"]
    X_raw = matrix_df[score_cols].values

    X = SimpleImputer(strategy="mean").fit_transform(X_raw)
    X_scaled = StandardScaler().fit_transform(X)

    sil_scores = {}
    for k in range(k_range[0], k_range[1] + 1):
        km = KMeans(n_clusters=k, random_state=42, n_init=10)
        labels = km.fit_predict(X_scaled)
        if len(set(labels)) > 1:
            sil_scores[k] = round(silhouette_score(X_scaled, labels), 4)
            print(f"  K={k} silhouette={sil_scores[k]:.4f}")

    best_k = max(sil_scores, key=sil_scores.get) if sil_scores else 2
    km_best = KMeans(n_clusters=best_k, random_state=42, n_init=10)
    km_labels = km_best.fit_predict(X_scaled)
    linkage_matrix = linkage(X_scaled, method="ward")
    hier_labels = fcluster(linkage_matrix, best_k, criterion="maxclust")

    print(f"  ✓ Best k={best_k} (silhouette={sil_scores.get(best_k, 'N/A')})")
    return {
        "agents":         agents,
        "km_labels":      km_labels.tolist(),
        "hier_labels":    hier_labels.tolist(),
        "best_k":         best_k,
        "sil_scores":     sil_scores,
        "linkage_matrix": linkage_matrix,
    }


# ── 7. Capability gap analysis ───────────────────────────────────────────────

def capability_gap_analysis() -> pd.DataFrame:
    """
    Z-score based gap analysis using DuckDB.
    Identifies where each agent over/underperforms vs their own average.
    """
    path = parquet_path("unified_scores")
    benchmarks = [c for c in pd.read_parquet(path).columns if c != "agent"]

    frames = []
    for bench in benchmarks:
        try:
            df = query_df(f"""
                WITH stats AS (
                    SELECT
                        AVG("{bench}")      AS mean_score,
                        STDDEV("{bench}")   AS std_score
                    FROM read_parquet('{path}')
                    WHERE "{bench}" IS NOT NULL
                )
                SELECT
                    agent,
                    '{bench}'                           AS benchmark,
                    "{bench}"                           AS score_norm,
                    CASE
                        WHEN s.std_score = 0 THEN 0
                        ELSE ROUND(("{bench}" - s.mean_score) / s.std_score, 3)
                    END                                 AS z_score,
                    CASE
                        WHEN s.std_score = 0 THEN 'average'
                        WHEN ("{bench}" - s.mean_score) / s.std_score >= 1 THEN 'strength'
                        WHEN ("{bench}" - s.mean_score) / s.std_score <= -1 THEN 'gap'
                        ELSE 'average'
                    END                                 AS flag
                FROM read_parquet('{path}'), stats s
                WHERE "{bench}" IS NOT NULL
            """)
            frames.append(df)
        except Exception as e:
            print(f"  ⚠ Gap analysis failed for {bench}: {e}")

    if not frames:
        return pd.DataFrame()
    result = pd.concat(frames, ignore_index=True)
    print(f"  ✓ Gap analysis: {len(result)} rows")
    return result


# ── Orchestrator ──────────────────────────────────────────────────────────────

def run_analysis() -> dict:
    print("=" * 50)
    print("ANALYZE: Statistics + Clustering + Gaps")
    print("=" * 50)

    print("\n── BENCHMARK STATS ──")
    stats = benchmark_stats()
    write_table(pa.Table.from_pandas(stats), "benchmark_stats")
    print(stats.to_string())

    print("\n── TOP AGENTS ──")
    top = top_agents_per_benchmark()
    write_table(pa.Table.from_pandas(top), "top_agents")

    print("\n── CHATBOT ARENA WIN RATES ──")
    arena = chatbot_arena_analysis()
    write_table(pa.Table.from_pandas(arena), "chatbot_arena_winrates")

    print("\n── MLE-BENCH COMPETITIONS ──")
    mle = mle_bench_analysis()
    write_table(pa.Table.from_pandas(mle), "mle_bench_stats")

    print("\n── CORRELATION ──")
    matrix_df = read_as_pandas("unified_scores")
    corr = benchmark_correlation(matrix_df)
    write_table(pa.Table.from_pandas(corr.reset_index().rename(columns={"index": "benchmark"})), "benchmark_correlation")

    print("\n── CLUSTERING ──")
    clustering = cluster_agents(matrix_df)
    cluster_df = pd.DataFrame({
        "agent":          clustering["agents"],
        "kmeans_cluster": clustering["km_labels"],
        "hier_cluster":   clustering["hier_labels"],
    })
    write_table(pa.Table.from_pandas(cluster_df), "cluster_labels")
    np.save(str(TABLES_DIR / "linkage_matrix.npy"), clustering["linkage_matrix"])
    with open(TABLES_DIR / "silhouette_scores.json", "w") as f:
        json.dump({str(k): v for k, v in clustering["sil_scores"].items()}, f, indent=2)

    print("\n── CAPABILITY GAPS ──")
    gaps = capability_gap_analysis()
    if not gaps.empty:
        write_table(pa.Table.from_pandas(gaps), "capability_gaps")

    print("\n✅ Analysis complete")
    return {
        "stats":      stats,
        "top_agents": top,
        "arena":      arena,
        "mle":        mle,
        "corr":       corr,
        "clustering": clustering,
        "gaps":       gaps,
    }


if __name__ == "__main__":
    run_analysis()
