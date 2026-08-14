"""
preprocess.py
-------------
Stage 2: clean, normalise, and build the unified agent x benchmark matrix.

What changed from v1
--------------------
All pandas groupby / merge / pivot logic is replaced with DuckDB SQL.
DuckDB reads the Parquet files written by collect.py directly — no
loading into memory, no type conversions, no intermediate DataFrames.

The SQL queries are intentionally verbose and commented so they read
as documentation of the transformation logic.

Output
------
  data/processed/unified_scores.parquet   -- agent x benchmark score matrix
  data/processed/benchmark_metadata.parquet
"""

import pyarrow as pa
import pandas as pd
from pathlib import Path

from db      import get_conn, query_arrow, query_df, execute
from storage import write_table, raw_parquet_glob, parquet_path

PROCESSED_DIR = Path(__file__).resolve().parents[1] / "data" / "processed"


# ── Step 1: Clean and standardise column names via DuckDB ─────────────────────

CLEAN_SQL = """
-- Standardise every benchmark file to: agent, score, benchmark
-- We use COALESCE to handle the many column name variants found in
-- different leaderboard CSVs (accuracy, resolved, pass_rate, etc.)

SELECT
    TRIM(COALESCE(agent, model, name, agent_name, system, submission))   AS agent,
    CAST(
        REPLACE(REPLACE(
            COALESCE(
                TRY_CAST(score      AS VARCHAR),
                TRY_CAST(accuracy   AS VARCHAR),
                TRY_CAST(resolved   AS VARCHAR),
                TRY_CAST(pass_rate  AS VARCHAR),
                TRY_CAST(overall    AS VARCHAR),
                TRY_CAST(total      AS VARCHAR)
            ),
        '%', ''), ',', '')
    AS DOUBLE)                                                            AS score,
    benchmark
FROM read_parquet('{glob}')
WHERE agent IS NOT NULL
  AND score  IS NOT NULL
"""

# ── Step 2: Normalise scores to 0-100 within each benchmark ───────────────────
# Min-max normalisation using DuckDB window functions.
# No Python loops, no pandas apply — one SQL pass over all benchmarks.

NORMALISE_SQL = """
WITH cleaned AS (
    SELECT
        agent,
        score,
        benchmark,
        MIN(score) OVER (PARTITION BY benchmark) AS bench_min,
        MAX(score) OVER (PARTITION BY benchmark) AS bench_max
    FROM cleaned_scores
),
normalised AS (
    SELECT
        agent,
        benchmark,
        score                                                    AS score_raw,
        CASE
            WHEN bench_max = bench_min THEN 50.0
            ELSE ROUND(
                ((score - bench_min) / (bench_max - bench_min)) * 100,
                2
            )
        END                                                      AS score_norm
    FROM cleaned
)
SELECT * FROM normalised
"""

# ── Step 3: Pivot into agent x benchmark matrix ───────────────────────────────
# PIVOT is a DuckDB built-in — does the full wide-format transform in SQL.

PIVOT_SQL = """
-- Keep only agents that appear in at least 2 benchmarks so we can compare them.
-- Agents seen on only 1 benchmark are analytically useless for cross-comparison.

WITH ranked AS (
    -- If an agent appears twice on the same benchmark (different versions),
    -- keep only their best score.
    SELECT agent, benchmark, MAX(score_norm) AS score_norm
    FROM normalised_scores
    GROUP BY agent, benchmark
),
multi_bench_agents AS (
    SELECT agent
    FROM ranked
    GROUP BY agent
    HAVING COUNT(DISTINCT benchmark) >= 2
)
PIVOT (
    SELECT r.agent, r.benchmark, r.score_norm
    FROM ranked r
    INNER JOIN multi_bench_agents m ON r.agent = m.agent
)
ON benchmark
USING MAX(score_norm)
ORDER BY agent
"""


def build_benchmark_metadata() -> pa.Table:
    """
    Static design-comparison table for all five benchmarks.
    Returned as an Arrow Table and written to Parquet.
    """
    records = [
        {"benchmark": "datasci_bench", "full_name": "DataSciBench",
         "task_types": "Data analysis, code generation, ML modelling",
         "primary_metric": "Accuracy / pass rate", "difficulty_levels": 3,
         "n_tasks": 500, "domain_focus": "Data science",
         "evaluation_mode": "Automated", "open_source": True},

        {"benchmark": "dsbench", "full_name": "DSBench",
         "task_types": "Data understanding, model training, debugging",
         "primary_metric": "Accuracy", "difficulty_levels": 3,
         "n_tasks": 74, "domain_focus": "Data science + ML engineering",
         "evaluation_mode": "Automated", "open_source": True},

        {"benchmark": "mle_bench", "full_name": "MLE-Bench",
         "task_types": "Kaggle competition ML pipelines",
         "primary_metric": "Percentile vs human Kaggle submissions",
         "difficulty_levels": 5, "n_tasks": 75,
         "domain_focus": "ML engineering",
         "evaluation_mode": "Competition scoring", "open_source": True},

        {"benchmark": "gaia", "full_name": "GAIA",
         "task_types": "Multi-step reasoning, tool use, web search",
         "primary_metric": "Exact match accuracy", "difficulty_levels": 3,
         "n_tasks": 450, "domain_focus": "General AI reasoning",
         "evaluation_mode": "Human-validated", "open_source": True},

        {"benchmark": "swe_bench", "full_name": "SWE-bench",
         "task_types": "GitHub issue resolution, code repair",
         "primary_metric": "% issues resolved", "difficulty_levels": 2,
         "n_tasks": 2294, "domain_focus": "Software engineering",
         "evaluation_mode": "Automated test suite", "open_source": True},
    ]
    return pa.Table.from_pylist(records)


def run_preprocessing() -> dict[str, pa.Table]:
    """
    Full preprocessing pipeline using DuckDB SQL throughout.

    Steps
    -----
    1. Read all bench_*.parquet files with a single DuckDB scan
    2. Clean and standardise column names (SQL COALESCE)
    3. Normalise scores 0-100 using SQL window functions
    4. Pivot to agent x benchmark matrix using DuckDB PIVOT
    5. Write all outputs as Parquet

    Returns
    -------
    dict with keys: cleaned, normalised, matrix, metadata
    """
    conn = get_conn()
    glob = raw_parquet_glob()

    print("── STEP 1: CLEAN ──")
    cleaned = query_arrow(CLEAN_SQL.format(glob=glob))
    conn.register("cleaned_scores", cleaned)
    print(f"  ✓ {cleaned.num_rows} rows after cleaning")

    print("\n── STEP 2: NORMALISE ──")
    normalised = query_arrow(NORMALISE_SQL)
    conn.register("normalised_scores", normalised)
    print(f"  ✓ {normalised.num_rows} rows normalised")

    print("\n── STEP 3: PIVOT MATRIX ──")
    # DuckDB PIVOT returns a wide DataFrame — convert to Arrow
    matrix_df = conn.execute(PIVOT_SQL).df()
    matrix_df = matrix_df.set_index("agent")
    dropped = normalised.to_pandas()["agent"].nunique() - len(matrix_df)
    if dropped > 0:
        print(f"  ⚠ Dropped {dropped} agents present on fewer than 2 benchmarks")
    print(f"  ✓ Matrix: {len(matrix_df)} agents x {len(matrix_df.columns)} benchmarks")
    matrix_arrow = pa.Table.from_pandas(matrix_df.reset_index())

    print("\n── STEP 4: BENCHMARK METADATA ──")
    metadata = build_benchmark_metadata()

    print("\n── SAVING PARQUET ──")
    write_table(cleaned,      "cleaned_scores")
    write_table(normalised,   "normalised_scores")
    write_table(matrix_arrow, "unified_scores")
    write_table(metadata,     "benchmark_metadata")

    print("\n✅ Preprocessing complete")
    return {
        "cleaned":    cleaned,
        "normalised": normalised,
        "matrix":     matrix_arrow,
        "metadata":   metadata,
    }


if __name__ == "__main__":
    run_preprocessing()
