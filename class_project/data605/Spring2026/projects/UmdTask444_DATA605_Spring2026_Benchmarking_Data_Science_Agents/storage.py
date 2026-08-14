"""
storage.py
----------
PyArrow-backed storage layer.

Responsibility: convert raw CSVs to Parquet and provide a single
read/write interface used by every other module.

Why Parquet over CSV?
  - Columnar: DuckDB querying 'score' only reads the score bytes
  - Snappy compression: typically 3-5x smaller than CSV
  - Schema embedded: no re-inferring types on every read
  - Native to PyArrow and DuckDB: zero-copy sharing between them

Nothing upstream of this file touches CSV again after collect.py runs.
"""

import pyarrow as pa
import pyarrow.csv as pa_csv
import pyarrow.parquet as pq
import pandas as pd
from pathlib import Path

ROOT          = Path(__file__).resolve().parents[1]
RAW_DIR       = ROOT / "data" / "raw"
PROCESSED_DIR = ROOT / "data" / "processed"
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


def csv_to_parquet(csv_path: Path, parquet_path: Path | None = None) -> Path:
    """
    Read a raw CSV with PyArrow and write it as Snappy-compressed Parquet.

    Parameters
    ----------
    csv_path     : source CSV file
    parquet_path : destination; defaults to data/processed/<stem>.parquet
    """
    if parquet_path is None:
        parquet_path = PROCESSED_DIR / f"{csv_path.stem}.parquet"

    convert_opts = pa_csv.ConvertOptions(
        null_values=["", "NA", "N/A", "null", "None", "-"],
        strings_can_be_null=True,
    )
    table = pa_csv.read_csv(csv_path, convert_options=convert_opts)
    table = table.rename_columns(
        [c.strip().lower().replace(" ", "_") for c in table.schema.names]
    )
    pq.write_table(table, parquet_path, compression="snappy", write_statistics=True)
    size_kb = parquet_path.stat().st_size / 1024
    print(f"  ✓ {csv_path.name} → {parquet_path.name} ({table.num_rows} rows, {size_kb:.1f} KB)")
    return parquet_path


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
        raise FileNotFoundError(f"Parquet not found: {path}\nRun collect.py first.")
    return pq.read_table(path)


def read_as_pandas(name: str) -> pd.DataFrame:
    """
    Read a Parquet file as pandas DataFrame.
    Use ONLY for small final result sets going into matplotlib/seaborn.
    For aggregation and querying, use DuckDB via db.py instead.
    """
    return read_table(name).to_pandas()


def parquet_path(name: str) -> str:
    """Return string path to data/processed/<name>.parquet for use in SQL."""
    return str(PROCESSED_DIR / f"{name}.parquet")


def raw_parquet_glob() -> str:
    """Glob string matching all per-benchmark Parquet files for DuckDB."""
    return str(PROCESSED_DIR / "bench_*.parquet")
