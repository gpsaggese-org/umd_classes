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

from db import query_df
from storage import parquet_path, write_table, read_as_pandas

ROOT = Path(__file__).resolve().parent
TABLES_DIR = ROOT / "outputs" / "tables"
TABLES_DIR.mkdir(parents=True, exist_ok=True)


def benchmark_stats():
    print("\n-- BENCHMARK STATS --")
    path = parquet_path("unified_data")
    df = query_df(f"""
        SELECT
            benchmark,
            COUNT(*) AS total_rows,
            COUNT(DISTINCT agent) AS unique_agents,
            COUNT(DISTINCT task) AS unique_tasks,
            ROUND(AVG(score), 4) AS mean_score,
            ROUND(STDDEV(score), 4) AS std_score,
            ROUND(MIN(score), 4) AS min_score,
            ROUND(MAX(score), 4) AS max_score
        FROM read_parquet('{path}')
        GROUP BY benchmark
        ORDER BY benchmark
    """)
    write_table(pa.Table.from_pandas(df), "benchmark_stats")
    print(df.to_string())
    return df


def top_agents():
    print("\n-- TOP AGENTS --")
    path = parquet_path("unified_data")
    df = query_df(f"""
        WITH ranked AS (
            SELECT
                benchmark,
                agent,
                ROUND(AVG(score), 4) AS mean_score,
                COUNT(*) AS n_tasks,
                DENSE_RANK() OVER (
                    PARTITION BY benchmark
                    ORDER BY AVG(score) DESC
                ) AS rank
            FROM read_parquet('{path}')
            WHERE agent IS NOT NULL
            GROUP BY benchmark, agent
        )
        SELECT * FROM ranked
        WHERE rank <= 20
        ORDER BY benchmark, rank
    """)
    write_table(pa.Table.from_pandas(df), "top_agents")
    print(f"  OK: {len(df)} rows")
    return df


def chatbot_arena_winrates():
    print("\n-- CHATBOT ARENA WIN RATES --")
    path = parquet_path("bench_chatbot_arena")
    df = query_df(f"""
        WITH model_scores AS (
            SELECT model_a AS model,
                CASE WHEN winner = 'model_a' THEN 1.0
                     WHEN winner = 'tie' THEN 0.5
                     ELSE 0.0 END AS won
            FROM read_parquet('{path}')
            WHERE model_a IS NOT NULL
            UNION ALL
            SELECT model_b AS model,
                CASE WHEN winner = 'model_b' THEN 1.0
                     WHEN winner = 'tie' THEN 0.5
                     ELSE 0.0 END AS won
            FROM read_parquet('{path}')
            WHERE model_b IS NOT NULL
        )
        SELECT
            model,
            COUNT(*) AS total_battles,
            ROUND(SUM(won), 0) AS wins,
            ROUND(AVG(won) * 100, 2) AS win_rate_pct
        FROM model_scores
        GROUP BY model
        HAVING COUNT(*) >= 10
        ORDER BY win_rate_pct DESC
        LIMIT 50
    """)
    write_table(pa.Table.from_pandas(df), "chatbot_arena_winrates")
    print(f"  OK: {len(df)} models")
    return df


def mle_bench_stats():
    print("\n-- MLE-BENCH STATS --")
    path = parquet_path("bench_mle_bench")
    df = query_df(f"""
        SELECT
            competition,
            COUNT(*) AS n_teams,
            ROUND(AVG(CAST(score AS DOUBLE)), 4) AS mean_score,
            ROUND(STDDEV(CAST(score AS DOUBLE)), 4) AS std_score,
            ROUND(MIN(CAST(score AS DOUBLE)), 4) AS min_score,
            ROUND(MAX(CAST(score AS DOUBLE)), 4) AS max_score
        FROM read_parquet('{path}')
        WHERE score IS NOT NULL
        GROUP BY competition
        ORDER BY n_teams DESC
    """)
    write_table(pa.Table.from_pandas(df), "mle_bench_stats")
    print(f"  OK: {len(df)} competitions")
    return df


def cluster_agents():
    print("\n-- CLUSTERING --")
    matrix_df = read_as_pandas("unified_scores")
    agents = matrix_df["agent"].tolist()
    score_cols = [c for c in matrix_df.columns if c != "agent"]
    X_raw = matrix_df[score_cols].values

    X = SimpleImputer(strategy="mean").fit_transform(X_raw)
    X_scaled = StandardScaler().fit_transform(X)

    sil_scores = {}
    for k in range(2, 6):
        km = KMeans(n_clusters=k, random_state=42, n_init=10)
        labels = km.fit_predict(X_scaled)
        if len(set(labels)) > 1:
            sil_scores[k] = round(silhouette_score(X_scaled, labels), 4)
            print(f"  K={k} silhouette={sil_scores[k]:.4f}")

    best_k = max(sil_scores, key=sil_scores.get) if sil_scores else 2
    km_best = KMeans(n_clusters=best_k, random_state=42, n_init=10)
    km_labels = km_best.fit_predict(X_scaled).tolist()
    linkage_matrix = linkage(X_scaled, method="ward")
    hier_labels = fcluster(linkage_matrix, best_k, criterion="maxclust").tolist()

    cluster_df = pd.DataFrame({
        "agent": agents,
        "kmeans_cluster": km_labels,
        "hier_cluster": hier_labels,
    })
    write_table(pa.Table.from_pandas(cluster_df), "cluster_labels")
    np.save(str(TABLES_DIR / "linkage_matrix.npy"), linkage_matrix)
    with open(TABLES_DIR / "silhouette_scores.json", "w") as f:
        json.dump({str(k): v for k, v in sil_scores.items()}, f, indent=2)
    print(f"  OK: best_k={best_k}")
    return cluster_df


def capability_gaps():
    print("\n-- CAPABILITY GAPS --")
    path = parquet_path("unified_scores")
    matrix_df = read_as_pandas(path.replace(str(ROOT / "data" / "processed") + "/", "").replace(".parquet", ""))
    benchmarks = [c for c in pd.read_parquet(path).columns if c != "agent"]

    frames = []
    for bench in benchmarks:
        try:
            df = query_df(f"""
                WITH stats AS (
                    SELECT
                        AVG("{bench}") AS mean_score,
                        STDDEV("{bench}") AS std_score
                    FROM read_parquet('{path}')
                    WHERE "{bench}" IS NOT NULL
                )
                SELECT
                    agent,
                    '{bench}' AS benchmark,
                    "{bench}" AS score_norm,
                    CASE
                        WHEN s.std_score = 0 THEN 0.0
                        ELSE ROUND(("{bench}" - s.mean_score) / s.std_score, 3)
                    END AS z_score,
                    CASE
                        WHEN s.std_score = 0 THEN 'average'
                        WHEN ("{bench}" - s.mean_score) / s.std_score >= 1 THEN 'strength'
                        WHEN ("{bench}" - s.mean_score) / s.std_score <= -1 THEN 'gap'
                        ELSE 'average'
                    END AS flag
                FROM read_parquet('{path}'), stats s
                WHERE "{bench}" IS NOT NULL
            """)
            frames.append(df)
        except Exception as e:
            print(f"  SKIP {bench}: {e}")

    if frames:
        result = pd.concat(frames, ignore_index=True)
        write_table(pa.Table.from_pandas(result), "capability_gaps")
        print(f"  OK: {len(result)} rows")
        return result
    return pd.DataFrame()


def run_analysis():
    print("=" * 50)
    print("ANALYZE")
    print("=" * 50)

    benchmark_stats()
    top_agents()
    chatbot_arena_winrates()
    mle_bench_stats()
    cluster_agents()
    capability_gaps()

    print("\n✅ Analysis complete")


if __name__ == "__main__":
    run_analysis()
