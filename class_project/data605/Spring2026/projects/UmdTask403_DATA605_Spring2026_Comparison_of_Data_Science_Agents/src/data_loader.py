"""

Download, load, and profile all datasets.

Usage:
    python src/data_loader.py --download-all
    python src/data_loader.py --profile
"""
import os
import json
import argparse
import pandas as pd
import numpy as np
from pathlib import Path
import pyarrow.parquet as pq

from src.utils import DATA_RAW, DATA_ADVERSARIAL, load_datasets_config, log, save_json, ensure_dir


# =============================================================================
# Individual Loaders
# =============================================================================

def load_heart_disease(forced_redownload=False):
    """UCI Heart Disease — binary classification, ~303 rows."""
    path = DATA_RAW / "heart_disease.csv"
    if forced_redownload or not path.exists():
        log.info("Downloading Heart Disease dataset...")
        url = "https://archive.ics.uci.edu/ml/machine-learning-databases/heart-disease/processed.cleveland.data"
        cols = ["age", "sex", "cp", "trestbps", "chol", "fbs", "restecg",
                "thalach", "exang", "oldpeak", "slope", "ca", "thal", "target"]
        df = pd.read_csv(url, names=cols, na_values="?")
        # Binarize target (0 = no disease, 1+ = disease)
        df["target"] = (df["target"] > 0).astype(int)
        ensure_dir(DATA_RAW)
        df.to_csv(path, index=False)
        log.info(f"Saved: {path} ({len(df)} rows)")
    else:
        df = pd.read_csv(path)
    meta = {"name": "heart_disease", "rows": len(df), "cols": len(df.columns),
            "modality": "tabular", "target": "target"}
    return df, meta


def load_nyc_taxi(forced_redownload=False, n_rows=50_000):
    """NYC Yellow Taxi — regression, sample to n_rows."""
    path = DATA_RAW / "nyc_taxi_sample.parquet"
    if forced_redownload or not path.exists():
        log.info("Downloading NYC Taxi dataset (this may take a minute)...")
        url = "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-01.parquet"
        raw_path = DATA_RAW / "yellow_tripdata_2024-01.parquet"
        ensure_dir(DATA_RAW)
        import urllib.request
        urllib.request.urlretrieve(url, raw_path)
        parquet_file = pq.ParquetFile(raw_path)
        df = next(parquet_file.iter_batches(batch_size=n_rows)).to_pandas()
        # Basic cleaning before sampling
        df = df[(df["fare_amount"] > 0) & (df["fare_amount"] < 200) & (df["trip_distance"] > 0)]
        df = df.sample(n=min(n_rows, len(df)), random_state=42)
        df.to_parquet(path, index=False)
        log.info(f"Saved: {path} ({len(df)} rows)")
    else:
        df = pd.read_parquet(path)
    meta = {"name": "nyc_taxi", "rows": len(df), "cols": len(df.columns),
            "modality": "tabular", "target": "fare_amount"}
    return df, meta


def load_air_quality(forced_redownload=False):
    """OpenAQ PM2.5 — time series."""
    path = DATA_RAW / "air_quality.csv"
    if forced_redownload or not path.exists():
        log.info("Downloading Air Quality data from OpenAQ API...")
        import requests
        ensure_dir(DATA_RAW)
        all_rows = []
        page = 1
        while len(all_rows) < 5000 and page <= 10:
            url = (
                f"https://api.openaq.org/v2/measurements"
                f"?city=Los Angeles&parameter=pm25&limit=1000&page={page}&order_by=datetime"
            )
            try:
                resp = requests.get(url, timeout=30)
                data = resp.json().get("results", [])
                if not data:
                    break
                for r in data:
                    all_rows.append({
                        "datetime": r.get("date", {}).get("utc"),
                        "value": r.get("value"),
                        "unit": r.get("unit"),
                        "latitude": r.get("coordinates", {}).get("latitude"),
                        "longitude": r.get("coordinates", {}).get("longitude"),
                        "location": r.get("location"),
                    })
                page += 1
            except Exception as e:
                log.warning(f"OpenAQ API error on page {page}: {e}")
                break
        df = pd.DataFrame(all_rows)
        if len(df) == 0:
            # Fallback: generate synthetic time-series data
            log.warning("OpenAQ API returned no data. Generating synthetic PM2.5 data.")
            dates = pd.date_range("2024-01-01", periods=2000, freq="h")
            np.random.seed(42)
            values = 30 + 15 * np.sin(np.arange(2000) * 2 * np.pi / 168) + np.random.normal(0, 5, 2000)
            df = pd.DataFrame({"datetime": dates, "value": values, "unit": "µg/m³",
                               "location": "Synthetic-LA"})
        df.to_csv(path, index=False)
        log.info(f"Saved: {path} ({len(df)} rows)")
    else:
        df = pd.read_csv(path)
    meta = {"name": "air_quality", "rows": len(df), "cols": len(df.columns),
            "modality": "time_series", "target": "value"}
    return df, meta


def load_amazon_reviews(forced_redownload=False, n_rows=10_000):
    """Amazon Reviews — NLP sentiment classification."""
    path = DATA_RAW / "amazon_reviews.csv"
    if forced_redownload or not path.exists():
        log.info("Downloading Amazon Reviews from HuggingFace...")
        ensure_dir(DATA_RAW)
        try:
            from datasets import load_dataset
            ds = load_dataset(
                "McAuley-Lab/Amazon-Reviews-2023",
                "raw_review_All_Beauty",
                split="full",
                streaming=True,
                trust_remote_code=True,
            )
            rows = []
            for i, row in enumerate(ds):
                if i >= n_rows:
                    break
                rows.append({
                    "rating": row.get("rating"),
                    "text": row.get("text", ""),
                    "verified_purchase": row.get("verified_purchase"),
                    "title": row.get("title", ""),
                })
            df = pd.DataFrame(rows)
        except Exception as e:
            log.warning(f"HuggingFace load failed: {e}. Generating synthetic reviews.")
            np.random.seed(42)
            ratings = np.random.choice([1, 2, 3, 4, 5], size=n_rows, p=[0.05, 0.05, 0.10, 0.30, 0.50])
            texts = [f"This is a sample review with rating {r}. " * np.random.randint(3, 15) for r in ratings]
            df = pd.DataFrame({"rating": ratings, "text": texts, "verified_purchase": True})
        df.to_csv(path, index=False)
        log.info(f"Saved: {path} ({len(df)} rows)")
    else:
        df = pd.read_csv(path)
    meta = {"name": "amazon_reviews", "rows": len(df), "cols": len(df.columns),
            "modality": "nlp", "target": "rating"}
    return df, meta


def load_cifar10(forced_redownload=False):
    """CIFAR-10 — image classification."""
    meta = {"name": "cifar10", "rows": 5000, "modality": "image", "target": "label"}
    if not forced_redownload:
        return None, meta
    log.info("Loading CIFAR-10 from HuggingFace...")
    try:
        from datasets import load_dataset
        ds = load_dataset("cifar10", split="test[:5000]")
        return ds, meta
    except Exception as e:
        log.warning(f"CIFAR-10 load failed: {e}")
        return None, meta


def load_urbansound8k(forced_redownload=False):
    """UrbanSound8K — audio classification. Requires manual download."""
    meta = {"name": "urbansound8k", "rows": 8732, "modality": "audio", "target": "classID"}
    log.info("UrbanSound8K requires manual download from https://zenodo.org/record/1203745")
    return None, meta


# =============================================================================
# Registry
# =============================================================================

LOADERS = {
    "heart_disease": {"func": load_heart_disease, "type": "tabular"},
    "nyc_taxi": {"func": load_nyc_taxi, "type": "tabular"},
    "air_quality": {"func": load_air_quality, "type": "time_series"},
    "amazon_reviews": {"func": load_amazon_reviews, "type": "nlp"},
    "cifar10": {"func": load_cifar10, "type": "image"},
    "urbansound8k": {"func": load_urbansound8k, "type": "audio"},
}


def load_dataset_by_name(name, forced_redownload=False):
    """Load a dataset by its config name."""
    if name not in LOADERS:
        raise ValueError(f"Unknown dataset: {name}. Available: {list(LOADERS.keys())}")
    return LOADERS[name]["func"](forced_redownload=forced_redownload)


# =============================================================================
# Adversarial Variants
# =============================================================================

def flip_labels(df, target_col, flip_pct=0.20, seed=42):
    """Randomly flip flip_pct of target labels."""
    rng = np.random.RandomState(seed)
    df_adv = df.copy()
    n_flip = int(len(df) * flip_pct)
    flip_idx = rng.choice(df.index, size=n_flip, replace=False)
    unique_labels = df[target_col].unique()
    for idx in flip_idx:
        current = df_adv.loc[idx, target_col]
        others = [l for l in unique_labels if l != current]
        if others:
            df_adv.loc[idx, target_col] = rng.choice(others)
    return df_adv


def inject_missing(df, target_col, missing_pct=0.15, seed=42):
    """Randomly set missing_pct of values to NaN."""
    rng = np.random.RandomState(seed)
    df_adv = df.copy()
    mask = rng.random(df.shape) < missing_pct
    # Don't mask the target column entirely
    target_idx = df.columns.get_loc(target_col)
    mask[:, target_idx] = False
    df_adv = df_adv.mask(mask)
    return df_adv


def create_adversarial_datasets():
    """Generate corrupted versions of datasets for robustness testing."""
    ensure_dir(DATA_ADVERSARIAL)

    # Heart Disease: flip labels + inject missing
    df_hd, _ = load_heart_disease()
    df_hd_adv = inject_missing(flip_labels(df_hd, "target", flip_pct=0.20),target_col="target", missing_pct=0.15)
    df_hd_adv.to_csv(DATA_ADVERSARIAL / "heart_disease.csv", index=False)
    log.info(f"Created adversarial heart_disease: {len(df_hd_adv)} rows, 20% flipped, 15% missing")

    # NYC Taxi: inject missing only (regression, no label flipping)
    df_taxi, _ = load_nyc_taxi()
    df_taxi_adv = inject_missing(df_taxi, target_col="fare_amount", missing_pct=0.20)
    df_taxi_adv.to_parquet(DATA_ADVERSARIAL / "nyc_taxi_sample.parquet", index=False)
    log.info(f"Created adversarial nyc_taxi: {len(df_taxi_adv)} rows, 20% missing")

    # Air Quality: inject missing
    df_aq, _ = load_air_quality()
    df_aq_adv = inject_missing(df_aq, target_col="value", missing_pct=0.20)
    df_aq_adv.to_csv(DATA_ADVERSARIAL / "air_quality.csv", index=False)
    log.info(f"Created adversarial air_quality: {len(df_aq_adv)} rows, 20% missing")

    # Amazon Reviews: flip ratings
    df_ar, _ = load_amazon_reviews()
    df_ar_adv = flip_labels(df_ar, "rating", flip_pct=0.15)
    df_ar_adv.to_csv(DATA_ADVERSARIAL / "amazon_reviews.csv", index=False)
    log.info(f"Created adversarial amazon_reviews: {len(df_ar_adv)} rows, 15% flipped")


# =============================================================================
# Profiler
# =============================================================================

def profile_all_datasets(forced_redownload=False):
    """Download and profile all datasets. Save profiles to data/dataset_profiles.json."""
    profiles = {}
    for name, loader in LOADERS.items():
        log.info(f"Profiling {name}...")
        try:
            data, meta = loader["func"](forced_redownload=forced_redownload)
            if isinstance(data, pd.DataFrame):
                meta["missing_total"] = int(data.isnull().sum().sum())
                meta["missing_pct"] = round(data.isnull().sum().sum() / data.size * 100, 2)
                meta["memory_mb"] = round(data.memory_usage(deep=True).sum() / 1e6, 2)
                meta["dtypes"] = dict(data.dtypes.astype(str).value_counts())
            profiles[name] = meta
            log.info(f"{name}: {meta.get('rows', '?')} rows")
        except Exception as e:
            log.error(f"{name}: {e}")
            profiles[name] = {"name": name, "error": str(e)}

    save_json(profiles, DATA_RAW.parent / "dataset_profiles.json")
    return profiles


# =============================================================================
# CLI
# =============================================================================

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Data Loader")
    parser.add_argument("--download-all", action="store_true", help="Download all datasets")
    parser.add_argument("--profile", action="store_true", help="Profile all datasets")
    parser.add_argument("--adversarial", action="store_true", help="Create adversarial variants")
    parser.add_argument("--dataset", type=str, help="Download a specific dataset")
    args = parser.parse_args()

    if args.download_all:
        profiles = profile_all_datasets(forced_redownload=True)
        print(json.dumps(profiles, indent=2, default=str))
    elif args.profile:
        profiles = profile_all_datasets(forced_redownload=False)
        print(json.dumps(profiles, indent=2, default=str))

    if args.adversarial:
        create_adversarial_datasets()

    if args.dataset:
        df, meta = load_dataset_by_name(args.dataset, forced_redownload=True)
        print(json.dumps(meta, indent=2, default=str))
        if isinstance(df, pd.DataFrame):
            print(f"\n{df.head()}")