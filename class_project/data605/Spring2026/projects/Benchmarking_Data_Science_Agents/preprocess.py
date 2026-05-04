"""
preprocess.py
-------------
Stage 2: Clean and standardise the 4 benchmark datasets using DuckDB SQL.

Each benchmark has a different schema:
  - chatbot_arena : model_a, model_b, winner, language, turn, toxic
  - swe_bench     : instance_id, repo, problem_statement, created_at
  - mle_bench     : competition, team, score, benchmark
  - gaia          : question, level, final_answer, annotator_metadata

This script:
  1. Reads all bench_*.parquet files via DuckDB
  2. Extracts a common schema: benchmark, model/agent, score (where available)
  3. Builds per-benchmark summary tables
  4. Saves unified_scores.parquet and benchmark_metadata.parquet
"""

import pyarrow as pa
import pandas as pd
from pathlib import Path

from db      import get_conn, query_arrow, query_df
from storage import write_table, raw_parquet_glob, parquet_path, read_as_pandas

ROOT          = Path(__file__).resolve().parent
PROCESSED_DIR = ROOT / "data" / "processed"


def process_mle_bench() -> pd.DataFrame:
    """
    MLE-bench: competition leaderboard scores.
    Schema: competition, team, score
    We treat each team's score as their performance metric.
    """
    path = parquet_path("bench_mle_bench")
    df = query_df(f"""
        SELECT
            team                    AS agent,
            competition             AS task,
            CAST(score AS DOUBLE)   AS score,
            'mle_bench'             AS benchmark
        FROM read_parquet('{path}')
        WHERE score IS NOT NULL
          AND team IS NOT NULL
    """)
    print(f"  ✓ mle_bench: {len(df)} rows")
    return df


def process_swe_bench() -> pd.DataFrame:
    """
    SWE-bench: GitHub issue resolution tasks.
    Schema: instance_id, repo, problem_statement, created_at
    No score column — we treat repo as the grouping variable.
    """
    path = parquet_path("bench_swe_bench")
    df = query_df(f"""
        SELECT
            repo                    AS agent,
            instance_id             AS task,
            0.0                     AS score,
            'swe_bench'             AS benchmark
        FROM read_parquet('{path}')
        WHERE instance_id IS NOT NULL
    """)
    print(f"  ✓ swe_bench: {len(df)} rows")
    return df


def process_gaia() -> pd.DataFrame:
    path = parquet_path("bench_gaia")
    df_raw = pd.read_parquet(path)
    df = pd.DataFrame({
        "agent":     df_raw["Level"].astype(str),
        "task":      df_raw["task_id"].astype(str),
        "score":     pd.to_numeric(df_raw["Level"], errors="coerce"),
        "benchmark": "gaia",
    }).dropna(subset=["score"])
    print(f"  ✓ gaia: {len(df)} rows")
    return df


def process_chatbot_arena() -> pd.DataFrame:
    path = parquet_path("bench_chatbot_arena")
    df_a = query_df(f"""
        SELECT
            model_a         AS agent,
            question_id     AS task,
            CASE WHEN winner = 'model_a' THEN 1.0
                 WHEN winner = 'tie' THEN 0.5
                 ELSE 0.0 END AS score,
            'chatbot_arena'  AS benchmark
        FROM read_parquet('{path}')
        WHERE model_a IS NOT NULL
    """)
    df_b = query_df(f"""
        SELECT
            model_b         AS agent,
            question_id     AS task,
            CASE WHEN winner = 'model_b' THEN 1.0
                 WHEN winner = 'tie' THEN 0.5
                 ELSE 0.0 END AS score,
            'chatbot_arena'  AS benchmark
        FROM read_parquet('{path}')
        WHERE model_b IS NOT NULL
    """)
    df = pd.concat([df_a, df_b], ignore_index=True)
    print(f"  ✓ chatbot_arena: {len(df)} rows")
    return df
def build_agent_benchmark_matrix(frames: list) -> pd.DataFrame:
    """
    Build agent x benchmark win rate matrix.
    For each agent x benchmark, compute their mean score.
    Only include agents appearing in 2+ benchmarks.
    """
    combined = pd.concat(frames, ignore_index=True)

    matrix = combined.groupby(["agent", "benchmark"])["score"].mean().reset_index()
    matrix = matrix.pivot(index="agent", columns="benchmark", values="score")
    matrix.columns.name = None

    # Keep agents in 2+ benchmarks
    valid = matrix.notna().sum(axis=1) >= 2
    matrix = matrix[valid]
    print(f"  ✓ Matrix: {len(matrix)} agents x {len(matrix.columns)} benchmarks")
    return matrix


def build_benchmark_metadata() -> pa.Table:
    records = [
        {"benchmark": "chatbot_arena", "full_name": "Chatbot Arena",
         "source": "lmsys/HuggingFace", "rows": 33000,
         "task_type": "Human preference voting",
         "metric": "Win rate", "domain": "General LLM evaluation"},
        {"benchmark": "swe_bench", "full_name": "SWE-bench Verified",
         "source": "princeton-nlp/HuggingFace", "rows": 500,
         "task_type": "GitHub issue resolution",
         "metric": "% issues resolved", "domain": "Software engineering"},
        {"benchmark": "mle_bench", "full_name": "MLE-bench",
         "source": "Kaggle API", "rows": 1520,
         "task_type": "ML competition tasks",
         "metric": "Competition score", "domain": "ML engineering"},
        {"benchmark": "gaia", "full_name": "GAIA",
         "source": "gaia-benchmark/HuggingFace", "rows": 165,
         "task_type": "Multi-step reasoning",
         "metric": "Exact match accuracy", "domain": "General AI reasoning"},
    ]
    return pa.Table.from_pylist(records)


def run_preprocessing():
    print("=" * 50)
    print("PREPROCESS: Clean + Normalise + Build Matrix")
    print("=" * 50)

    print("\n── PROCESSING EACH BENCHMARK ──")
    frames = []
    for fn in [process_mle_bench, process_swe_bench, process_gaia, process_chatbot_arena]:
        try:
            df = fn()
            frames.append(df)
        except Exception as e:
            print(f"  ⚠ {fn.__name__} failed: {e}")

    if not frames:
        raise RuntimeError("No data processed. Run collect.py first.")

    print("\n── BUILDING UNIFIED DATASET ──")
    combined = pd.concat(frames, ignore_index=True)
    write_table(pa.Table.from_pandas(combined), "unified_data")
    print(f"  ✓ unified_data.parquet: {len(combined)} rows")

    print("\n── BUILDING AGENT x BENCHMARK MATRIX ──")
    try:
        matrix = build_agent_benchmark_matrix(frames)
        write_table(pa.Table.from_pandas(matrix.reset_index()), "unified_scores")
    except Exception as e:
        print(f"  ⚠ Matrix failed: {e}")

    print("\n── BENCHMARK METADATA ──")
    metadata = build_benchmark_metadata()
    write_table(metadata, "benchmark_metadata")

    print("\n✅ Preprocessing complete")
    return combined


if __name__ == "__main__":
    run_preprocessing()
