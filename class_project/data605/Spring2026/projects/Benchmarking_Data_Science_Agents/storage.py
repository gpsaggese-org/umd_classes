"""
storage.py
----------
PyArrow storage layer.

Handles reading and writing Parquet files for the 4 benchmarks:
  - chatbot_arena, swe_bench, mle_bench, gaia

All paths are relative to the project root (same folder as this file).
"""

import pyarrow as pa
import pyarrow.csv as pa_csv
import pyarrow.parquet as pq
import pandas as pd
from pathlib import Path

ROOT          = Path(__file__).resolve().parent
RAW_DIR       = ROOT / "data" / "raw"
PROCESSED_DIR = ROOT / "data" / "processed"
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


def write_table(table: pa.Table, name: str) -> Path:
    """Write an Arrow Table to data/processed/<name>.parquet."""
    path = PROCESSED_DIR / f"{name}.parquet"
    pq.write_table(table, path, compression="snappy", write_statistics=True)
    print(f"  💾 {name}.parquet ({table.num_rows} rows, {table.num_columns} cols)")
    return path


def read_table(name: str) -> pa.Table:
    """Read data/processed/<name>.parquet as an Arrow Table."""
    path = PROCESSED_DIR / f"{name}.parquet"
    if not path.exists():
        raise FileNotFoundError(f"Not found: {path}\nRun collect.py first.")
    return pq.read_table(path)


def read_as_pandas(name: str) -> pd.DataFrame:
    """Read a Parquet file as pandas DataFrame (for plotting only)."""
    return read_table(name).to_pandas()


def parquet_path(name: str) -> str:
    """Return string path to data/processed/<name>.parquet for DuckDB SQL."""
    return str(PROCESSED_DIR / f"{name}.parquet")


def raw_parquet_glob() -> str:
    """Glob matching all bench_*.parquet files for DuckDB."""
    return str(PROCESSED_DIR / "bench_*.parquet")
