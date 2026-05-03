"""
collect.py
----------
Stage 1: Load the 4 real scraped CSVs and convert each to Parquet.

Benchmarks:
  - chatbot_arena  : 33,000 rows - HuggingFace lmsys
  - swe_bench      : 500 rows    - HuggingFace princeton-nlp
  - mle_bench      : 1,520 rows  - Kaggle API
  - gaia           : 165 rows    - HuggingFace gaia-benchmark

All CSVs live in data/raw/ and were created by scrapperv5.py.
This script converts them to Parquet for DuckDB querying.
"""

import pyarrow as pa
import pyarrow.csv as pa_csv
import pyarrow.parquet as pq
from pathlib import Path

ROOT          = Path(__file__).resolve().parent
RAW_DIR       = ROOT / "data" / "raw"
PROCESSED_DIR = ROOT / "data" / "processed"
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

# The 4 benchmarks we actually have
BENCHMARKS = {
    "chatbot_arena": {
        "csv": "chatbot_arena.csv",
        "description": "33k human preference votes between LLMs",
    },
    "swe_bench": {
        "csv": "swe_bench.csv",
        "description": "500 GitHub issue resolution tasks",
    },
    "mle_bench": {
        "csv": "mle_bench.csv",
        "description": "1520 Kaggle competition leaderboard entries",
    },
    "gaia": {
        "csv": "gaia.csv",
        "description": "165 multi-step reasoning tasks",
    },
}


def csv_to_parquet(name: str, csv_path: Path) -> Path:
    """Convert a raw CSV to Snappy-compressed Parquet using PyArrow."""
    parquet_path = PROCESSED_DIR / f"bench_{name}.parquet"

    convert_opts = pa_csv.ConvertOptions(
        null_values=["", "NA", "N/A", "null", "None", "-"],
        strings_can_be_null=True,
    )
    table = pa_csv.read_csv(csv_path, convert_options=convert_opts)

    # Normalise column names
    table = table.rename_columns(
        [c.strip().lower().replace(" ", "_") for c in table.schema.names]
    )

    # Tag every row with benchmark name
    if "benchmark" not in table.schema.names:
        table = table.append_column(
            "benchmark",
            pa.array([name] * table.num_rows, type=pa.string())
        )

    pq.write_table(table, parquet_path, compression="snappy", write_statistics=True)
    size_kb = parquet_path.stat().st_size / 1024
    print(f"  ✓ {csv_path.name} → bench_{name}.parquet ({table.num_rows} rows, {size_kb:.1f} KB)")
    return parquet_path


def collect_all() -> dict:
    """Convert all 4 benchmark CSVs to Parquet."""
    print("=" * 50)
    print("COLLECT: CSV → Parquet")
    print("=" * 50)

    results = {}
    for name, cfg in BENCHMARKS.items():
        print(f"\n── {name.upper()} ──")
        csv_path = RAW_DIR / cfg["csv"]
        if not csv_path.exists():
            print(f"  ⚠ Not found: {csv_path}")
            print(f"  → Run scrapperv5.py first")
            continue
        try:
            parquet_path = csv_to_parquet(name, csv_path)
            results[name] = parquet_path
        except Exception as e:
            print(f"  ✗ Failed: {e}")

    print(f"\n✅ {len(results)}/{len(BENCHMARKS)} benchmarks converted to Parquet")
    return results


if __name__ == "__main__":
    collect_all()

