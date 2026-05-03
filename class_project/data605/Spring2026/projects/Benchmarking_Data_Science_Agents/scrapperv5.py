import os
import time
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
RAW_DIR = Path("data/raw")
RAW_DIR.mkdir(parents=True, exist_ok=True)


def scrape_gaia():
    print("\n-- GAIA --")
    try:
        from datasets import load_dataset
        from huggingface_hub import login
        token = os.getenv("HF_TOKEN")
        if token:
            login(token=token)
        frames = []
        for level in ["2023_level1", "2023_level2", "2023_level3"]:
            try:
                ds = load_dataset("gaia-benchmark/GAIA", level, split="validation")
                df = ds.to_pandas()
                df["level"] = level.split("_")[1]
                frames.append(df)
                print(f"  OK {level}: {len(df)} rows")
            except Exception as e:
                print(f"  SKIP {level}: {e}")
        if not frames:
            raise RuntimeError("no data")
        result = pd.concat(frames, ignore_index=True)
        result["benchmark"] = "gaia"
        result.to_csv(RAW_DIR / "gaia.csv", index=False)
        print(f"  SAVED {len(result)} rows")
        return result
    except Exception as e:
        print(f"  FAIL: {e}")
        return pd.DataFrame()


def scrape_swe_bench():
    print("\n-- SWE-BENCH --")
    try:
        from datasets import load_dataset
        ds = load_dataset("princeton-nlp/SWE-bench_Verified", split="test")
        df = ds.to_pandas()
        df["benchmark"] = "swe_bench"
        df.to_csv(RAW_DIR / "swe_bench.csv", index=False)
        print(f"  SAVED {len(df)} rows")
        return df
    except Exception as e:
        print(f"  FAIL: {e}")
        return pd.DataFrame()


def scrape_mle_bench():
    print("\n-- MLE-BENCH (75 competitions) --")
    try:
        import kaggle
        kaggle.api.authenticate()

        comps = [
            "titanic",
            "digit-recognizer",
            "house-prices-advanced-regression-techniques",
            "spaceship-titanic",
            "nlp-getting-started",
            "store-sales-time-series-forecasting",
            "dogs-vs-cats",
            "facial-keypoints-detection",
            "leaf-classification",
            "forest-cover-type-prediction",
            "bike-sharing-demand",
            "porto-seguro-safe-driver-prediction",
            "allstate-claims-severity",
            "shelter-animal-outcomes",
            "quora-question-pairs",
            "march-machine-learning-mania-2017",
            "contradictory-my-dear-watson",
            "tabular-playground-series-jan-2021",
            "tabular-playground-series-feb-2021",
            "tabular-playground-series-mar-2021",
            "tabular-playground-series-apr-2021",
            "tabular-playground-series-may-2021",
            "tabular-playground-series-jun-2021",
            "tabular-playground-series-jul-2021",
            "tabular-playground-series-aug-2021",
            "tabular-playground-series-sep-2021",
            "tabular-playground-series-oct-2021",
            "tabular-playground-series-nov-2021",
            "tabular-playground-series-dec-2021",
            "tabular-playground-series-jan-2022",
            "tabular-playground-series-feb-2022",
            "tabular-playground-series-mar-2022",
            "tabular-playground-series-apr-2022",
            "tabular-playground-series-may-2022",
            "tabular-playground-series-jun-2022",
            "tabular-playground-series-jul-2022",
            "tabular-playground-series-aug-2022",
            "tabular-playground-series-sep-2022",
            "tabular-playground-series-oct-2022",
            "tabular-playground-series-nov-2022",
            "tabular-playground-series-dec-2022",
            "playground-series-s3e1",
            "playground-series-s3e2",
            "playground-series-s3e3",
            "playground-series-s3e4",
            "playground-series-s3e5",
            "playground-series-s3e6",
            "playground-series-s3e7",
            "playground-series-s3e8",
            "playground-series-s3e9",
            "playground-series-s3e10",
            "playground-series-s3e11",
            "playground-series-s3e12",
            "playground-series-s3e13",
            "playground-series-s3e14",
            "playground-series-s3e15",
            "playground-series-s3e16",
            "playground-series-s3e17",
            "playground-series-s3e18",
            "playground-series-s3e19",
            "playground-series-s3e20",
            "playground-series-s3e21",
            "playground-series-s3e22",
            "playground-series-s3e23",
            "playground-series-s3e24",
            "playground-series-s3e25",
            "playground-series-s3e26",
            "playground-series-s4e1",
            "playground-series-s4e2",
            "playground-series-s4e3",
            "playground-series-s4e4",
            "playground-series-s4e5",
            "playground-series-s4e6",
            "playground-series-s4e7",
            "playground-series-s4e8",
            "playground-series-s4e9",
            "playground-series-s4e10",
        ]

        frames = []
        for comp in comps:
            try:
                lb = kaggle.api.competition_leaderboard_view(comp)
                rows = []
                for e in lb:
                    row = {"competition": comp, "score": e.score}
                    for attr in ["team_name", "teamName", "team"]:
                        if hasattr(e, attr):
                            row["team"] = getattr(e, attr)
                            break
                    rows.append(row)
                if rows:
                    frames.append(pd.DataFrame(rows))
                    print(f"  OK {comp}: {len(rows)} rows")
                time.sleep(0.3)
            except Exception as e:
                print(f"  SKIP {comp}: {e}")

        if not frames:
            raise RuntimeError("no data")
        result = pd.concat(frames, ignore_index=True)
        result["benchmark"] = "mle_bench"
        result.to_csv(RAW_DIR / "mle_bench.csv", index=False)
        print(f"  SAVED {len(result)} rows")
        return result
    except Exception as e:
        print(f"  FAIL: {e}")
        return pd.DataFrame()


def scrape_datasci_bench():
    print("\n-- DATASCIBENCH --")
    print("  SKIP - broken schema in source dataset")
    return pd.DataFrame()


def scrape_dsbench():
    print("\n-- DSBENCH --")
    print("  SKIP - broken dataset")
    return pd.DataFrame()


def scrape_all():
    print("=" * 40)
    print("BENCHMARK DATA COLLECTION")
    print("=" * 40)
    results = {}
    for name, fn in [
        ("gaia", scrape_gaia),
        ("swe_bench", scrape_swe_bench),
        ("mle_bench", scrape_mle_bench),
        ("datasci_bench", scrape_datasci_bench),
        ("dsbench", scrape_dsbench),
    ]:
        df = fn()
        if not df.empty:
            results[name] = df
    print("\nDONE:", len(results), "/5")
    print("TOTAL ROWS:", sum(len(v) for v in results.values()))
    return results


if __name__ == "__main__":
    scrape_all()
