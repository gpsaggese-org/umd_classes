"""
scraper.py
----------
Data collection script for all 5 benchmarks.

Sources:
  - GAIA        : HuggingFace datasets API (gated, needs HF token)
  - SWE-bench   : HuggingFace datasets API (princeton-nlp/SWE-bench)
  - MLE-bench   : Kaggle API (75 competitions x all submissions)
  - DataSciBench: HuggingFace datasets API (zd21/DataSciBench)
  - DSBench     : GitHub raw files

Output:
  data/raw/<benchmark>.csv for each benchmark

Usage:
  python scraper.py

Environment variables needed in .env:
  HF_TOKEN       = your HuggingFace token (for GAIA)
  KAGGLE_USERNAME = your Kaggle username (for MLE-bench)
  KAGGLE_KEY      = your Kaggle API key (for MLE-bench)
"""

import os
import time
import requests
import pandas as pd
import pyarrow as pa
import pyarrow.csv as pa_csv
import pyarrow.parquet as pq
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

RAW_DIR = Path("data/raw")
RAW_DIR.mkdir(parents=True, exist_ok=True)


# ── 1. GAIA ───────────────────────────────────────────────────────────────────

def scrape_gaia() -> pd.DataFrame:
    """
    Download GAIA benchmark tasks from HuggingFace.
    Requires HF_TOKEN in .env (get from huggingface.co/settings/tokens).
    Returns task-level data: question, level, category, annotator metadata.
    """
    print("\n── GAIA ──")
    try:
        from datasets import load_dataset
        from huggingface_hub import login

        token = os.getenv("HF_TOKEN")
        if token:
            login(token=token)

        frames = []
        for level in ["2023_level1", "2023_level2", "2023_level3"]:
            print(f"  ↓ Downloading {level}...")
            try:
                ds = load_dataset("gaia-benchmark/GAIA", level, split="validation")
                df = ds.to_pandas()
                df["level"] = level.split("_")[1]
                frames.append(df)
                print(f"  ✓ {level}: {len(df)} rows")
            except Exception as e:
                print(f"  ⚠ {level} failed: {e}")

        if not frames:
            raise RuntimeError("No GAIA data loaded")

        result = pd.concat(frames, ignore_index=True)
        result["benchmark"] = "gaia"
        path = RAW_DIR / "gaia.csv"
        result.to_csv(path, index=False)
        print(f"  💾 Saved {len(result)} rows → {path}")
        return result

    except Exception as e:
        print(f"  ✗ GAIA failed: {e}")
        print("  → Make sure HF_TOKEN is set in .env and you have access to gaia-benchmark/GAIA")
        return pd.DataFrame()


# ── 2. SWE-bench ─────────────────────────────────────────────────────────────

def scrape_swe_bench() -> pd.DataFrame:
    """
    Download SWE-bench Verified from HuggingFace.
    No token needed — public dataset.
    Returns issue-level data: repo, problem statement, difficulty.
    """
    print("\n── SWE-BENCH ──")
    try:
        from datasets import load_dataset

        print("  ↓ Downloading SWE-bench Verified...")
        ds = load_dataset("princeton-nlp/SWE-bench_Verified", split="test")
        df = ds.to_pandas()
        df["benchmark"] = "swe_bench"

        # Keep relevant columns
        cols = ["instance_id", "repo", "problem_statement",
                "created_at", "benchmark"]
        df = df[[c for c in cols if c in df.columns]]

        path = RAW_DIR / "swe_bench.csv"
        df.to_csv(path, index=False)
        print(f"  ✓ {len(df)} rows → {path}")
        return df

    except Exception as e:
        print(f"  ✗ SWE-bench failed: {e}")
        return pd.DataFrame()


# ── 3. MLE-bench (Kaggle) ─────────────────────────────────────────────────────

# The 75 Kaggle competitions used in MLE-bench
MLE_BENCH_COMPETITIONS = [
    "contradictory-my-dear-watson", "digit-recognizer", "titanic",
    "house-prices-advanced-regression-techniques", "spaceship-titanic",
    "nlp-getting-started", "store-sales-time-series-forecasting",
    "dogs-vs-cats", "facial-keypoints-detection", "leaf-classification",
    "forest-cover-type-prediction", "bike-sharing-demand",
    "porto-seguro-safe-driver-prediction", "instacart-market-basket-analysis",
    "allstate-claims-severity", "liberty-mutual-group-property-inspection-prediction",
    "shelter-animal-outcomes", "march-machine-learning-mania-2017",
    "two-sigma-financial-news", "quora-question-pairs",
]  # Subset of 20 for speed — expand to all 75 when needed


def scrape_mle_bench() -> pd.DataFrame:
    """
    Download public Kaggle competition leaderboards for MLE-bench competitions.
    Requires KAGGLE_USERNAME and KAGGLE_KEY in .env.
    Get API key from kaggle.com/settings → API → Create New Token.
    """
    print("\n── MLE-BENCH (Kaggle) ──")
    try:
        import kaggle
        from kaggle.api.kaggle_api_extended import KaggleApiClient

        username = os.getenv("KAGGLE_USERNAME")
        key      = os.getenv("KAGGLE_KEY")
        if not username or not key:
            raise EnvironmentError("KAGGLE_USERNAME and KAGGLE_KEY not set in .env")

        os.environ["KAGGLE_USERNAME"] = username
        os.environ["KAGGLE_KEY"]      = key

        from kaggle.api.kaggle_api_extended import KaggleApiExtended
        api = KaggleApiExtended()
        api.authenticate()

        all_frames = []
        for comp in MLE_BENCH_COMPETITIONS:
            try:
                print(f"  ↓ {comp}...")
                lb = api.competition_leaderboard_view(comp)
                rows = [{"competition": comp,
                         "team_name":   e.teamName,
                         "rank":        e.rank,
                         "score":       e.score,
                         "entries":     e.totalEntries,
                         "last_submission": str(e.lastSubmissionDate)}
                        for e in lb]
                df = pd.DataFrame(rows)
                all_frames.append(df)
                print(f"  ✓ {comp}: {len(df)} submissions")
                time.sleep(0.5)   # be polite to the API
            except Exception as e:
                print(f"  ⚠ {comp}: {e}")

        if not all_frames:
            raise RuntimeError("No MLE-bench data loaded")

        result = pd.concat(all_frames, ignore_index=True)
        result["benchmark"] = "mle_bench"
        path = RAW_DIR / "mle_bench.csv"
        result.to_csv(path, index=False)
        print(f"  💾 Saved {len(result)} rows → {path}")
        return result

    except ImportError:
        print("  ✗ kaggle package not installed. Run: pip install kaggle")
        return pd.DataFrame()
    except Exception as e:
        print(f"  ✗ MLE-bench failed: {e}")
        return pd.DataFrame()


# ── 4. DataSciBench ───────────────────────────────────────────────────────────

def scrape_datasci_bench() -> pd.DataFrame:
    print("\n── DATASCIBENCH ──")
    try:
        from datasets import load_dataset
        from huggingface_hub import login
        token = os.getenv("HF_TOKEN")
        if token:
            login(token=token)
        print("  ↓ Downloading DataSciBench...")
        # Use ignore_verifications to handle inconsistent columns
        ds = load_dataset(
            "zd21/DataSciBench",
            split="train",
            token=token,
            ignore_verifications=True,
            trust_remote_code=True,
        )
        df = ds.to_pandas()
        df["benchmark"] = "datasci_bench"
        path = RAW_DIR / "datasci_bench.csv"
        df.to_csv(path, index=False)
        print(f"  ✓ {len(df)} rows → {path}")
        return df
    except Exception as e:
        print(f"  ✗ DataSciBench failed: {e}")
        return pd.DataFrame()


# ── 5. DSBench ────────────────────────────────────────────────────────────────

DSBENCH_URLS = [
    "https://raw.githubusercontent.com/LiqiangJing/DSBench/main/data_analysis/tasks.json",
    "https://raw.githubusercontent.com/LiqiangJing/DSBench/main/data_modeling/tasks.json",
]

def scrape_dsbench() -> pd.DataFrame:
    """
    Download DSBench task data directly from GitHub raw files.
    No token needed — public repo.
    """
    print("\n── DSBENCH ──")
    try:
        import json
        frames = []
        for url in DSBENCH_URLS:
            print(f"  ↓ {url.split('/')[-1]}...")
            resp = requests.get(url, timeout=15)
            resp.raise_for_status()
            data = resp.json()
            if isinstance(data, list):
                df = pd.DataFrame(data)
            else:
                df = pd.DataFrame([data])
            task_type = "data_analysis" if "da_tasks" in url else "model_prediction"
            df["task_type"] = task_type
            frames.append(df)
            print(f"  ✓ {task_type}: {len(df)} rows")

        result = pd.concat(frames, ignore_index=True)
        result["benchmark"] = "dsbench"
        path = RAW_DIR / "dsbench.csv"
        result.to_csv(path, index=False)
        print(f"  💾 Saved {len(result)} rows → {path}")
        return result

    except Exception as e:
        print(f"  ✗ DSBench failed: {e}")
        return pd.DataFrame()


# ── Orchestrator ──────────────────────────────────────────────────────────────

def scrape_all() -> dict[str, pd.DataFrame]:
    """Run all scrapers and return results."""
    print("="*50)
    print("BENCHMARK DATA COLLECTION")
    print("="*50)

    results = {}

    df = scrape_gaia()
    if not df.empty:
        results["gaia"] = df

    df = scrape_swe_bench()
    if not df.empty:
        results["swe_bench"] = df

    df = scrape_mle_bench()
    if not df.empty:
        results["mle_bench"] = df

    df = scrape_datasci_bench()
    if not df.empty:
        results["datasci_bench"] = df

    df = scrape_dsbench()
    if not df.empty:
        results["dsbench"] = df

    print("\n" + "="*50)
    print(f"DONE: {len(results)}/5 benchmarks collected")
    total_rows = sum(len(v) for v in results.values())
    print(f"TOTAL ROWS: {total_rows:,}")
    for name, df in results.items():
        print(f"  {name}: {len(df):,} rows")
    print("="*50)

    return results


if __name__ == "__main__":
    scrape_all()

# ── OVERRIDE: Fixed DSBench using HuggingFace ─────────────────────────────────
def scrape_dsbench():
    print("\n── DSBENCH ──")
    try:
        from datasets import load_dataset
        print("  ↓ Downloading DSBench from HuggingFace...")
        ds = load_dataset("liqiang888/DSBench", split="train")
        df = ds.to_pandas()
        df["benchmark"] = "dsbench"
        path = RAW_DIR / "dsbench.csv"
        df.to_csv(path, index=False)
        print(f"  ✓ {len(df)} rows → {path}")
        return df
    except Exception as e:
        print(f"  ✗ DSBench failed: {e}")
        return pd.DataFrame()
