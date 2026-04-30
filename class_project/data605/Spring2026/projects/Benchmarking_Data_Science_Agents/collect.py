"""
collect.py
----------
Stage 1: load raw leaderboard CSVs and convert each one to Parquet.

What changed from v1
--------------------
- Every CSV is immediately converted to Parquet via PyArrow after loading.
  All downstream stages (preprocess, analyze, visualize) read Parquet only.
- PyArrow's CSV reader handles type inference and null normalisation,
  replacing manual pandas string-cleaning.
- HuggingFace datasets are also written to Parquet so all downstream
  code sees a single uniform format regardless of source.

Output
------
  data/processed/bench_<name>.parquet  for each benchmark
"""

import time
import requests
import pyarrow as pa
import pyarrow.csv as pa_csv
from pathlib import Path

from storage import csv_to_parquet, write_table

RAW_DIR       = Path(__file__).resolve().parents[1] / "data" / "raw"
PROCESSED_DIR = Path(__file__).resolve().parents[1] / "data" / "processed"

BENCHMARKS = {
    "datasci_bench": {"method": "csv"},
    "dsbench":       {"method": "csv"},
    "mle_bench":     {"method": "csv"},
    "gaia":          {"method": "csv"},
    "swe_bench":     {"method": "csv"},
}


def load_csv(name: str) -> pa.Table:
    """Load a raw CSV as an Arrow Table using PyArrow's vectorised reader."""
    path = RAW_DIR / f"{name}.csv"
    if not path.exists():
        raise FileNotFoundError(
            f"Raw CSV not found: {path}\n"
            "Place the leaderboard CSV here before running collect.py"
        )
    convert_opts = pa_csv.ConvertOptions(
        null_values=["", "NA", "N/A", "null", "None", "-"],
        strings_can_be_null=True,
    )
    table = pa_csv.read_csv(path, convert_options=convert_opts)
    # Normalise column names
    table = table.rename_columns(
        [c.strip().lower().replace(" ", "_") for c in table.schema.names]
    )
    # Tag every row with its benchmark name so we know the source after merging
    table = table.append_column(
        "benchmark",
        pa.array([name] * table.num_rows, type=pa.string())
    )
    print(f"  ✓ Loaded {table.num_rows} rows from {path.name}")
    return table


def load_from_huggingface(dataset_name: str, split: str = "validation") -> pa.Table:
    """Download a HuggingFace dataset and return it as an Arrow Table."""
    try:
        from datasets import load_dataset
    except ImportError:
        raise ImportError("Run: pip install datasets huggingface-hub")

    print(f"  ↓ Downloading {dataset_name} [{split}] from HuggingFace...")
    ds = load_dataset(dataset_name, split=split)
    table = ds.data.table   # returns pyarrow.Table directly — no pandas needed
    print(f"  ✓ Loaded {table.num_rows} rows from HuggingFace")
    return table


def collect_all(save: bool = True) -> dict[str, pa.Table]:
    """
    Collect all benchmark leaderboards and write each to Parquet.

    Returns
    -------
    dict mapping benchmark name → Arrow Table
    """
    results: dict[str, pa.Table] = {}

    for name, cfg in BENCHMARKS.items():
        print(f"\n── {name.upper()} ──")
        try:
            if cfg["method"] == "csv":
                table = load_csv(name)
            elif cfg["method"] == "huggingface":
                table = load_from_huggingface(cfg["dataset"], cfg.get("split", "validation"))
                table = table.append_column(
                    "benchmark",
                    pa.array([name] * table.num_rows, type=pa.string())
                )
            else:
                raise ValueError(f"Unknown method: {cfg['method']}")

            results[name] = table

            if save:
                # Save as bench_<name>.parquet so the glob bench_*.parquet
                # picks up all benchmark files and nothing else
                write_table(table, f"bench_{name}")

        except Exception as exc:
            print(f"  ⚠ Skipped {name}: {exc}")

    print(f"\n✅ Collection complete — {len(results)}/{len(BENCHMARKS)} benchmarks loaded")
    return results


if __name__ == "__main__":
    collect_all(save=True)
