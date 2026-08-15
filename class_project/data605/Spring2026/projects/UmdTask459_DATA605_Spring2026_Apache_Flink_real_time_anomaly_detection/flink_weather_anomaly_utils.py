"""
Helper functions for data loading, model training, anomaly detection,
metric computation, and visualization used across the project notebooks.
"""

import time
import json
from collections import defaultdict, deque
from typing import Dict, List, Optional, Tuple

import joblib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.ensemble import IsolationForest
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)

# Columns used as model input.
FEATURE_NAMES = ["temperature", "humidity", "pressure"]

# Baseline anomaly detection thresholds (per city rolling window).
TEMP_THRESHOLD     = 7.0   # degrees Celsius
HUMIDITY_THRESHOLD = 25.0  # percentage points
PRESSURE_THRESHOLD = 15.0  # hPa


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------


def load_weather_data(path: str = "data/weather_data.csv") -> pd.DataFrame:
    """Load the weather training dataset.

    Parameters
    ----------
    path:
        Path to the CSV file containing temperature, humidity, and pressure
        columns.

    Returns
    -------
    pd.DataFrame
        DataFrame with columns ``temperature``, ``humidity``, ``pressure``.
    """
    df = pd.read_csv(path)
    return df[FEATURE_NAMES].copy()


def load_weather_logs(path: str = "data/weather_logs_sample.csv") -> pd.DataFrame:
    """Load the collected weather event log.

    Parameters
    ----------
    path:
        Path to the CSV file produced by the live pipeline.

    Returns
    -------
    pd.DataFrame
        Full log DataFrame parsed with a datetime ``timestamp`` column.
    """
    df = pd.read_csv(path)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    return df


# ---------------------------------------------------------------------------
# Model training
# ---------------------------------------------------------------------------


def train_isolation_forest(
    X: pd.DataFrame,
    n_estimators: int = 200,
    contamination: float = 0.05,
    random_state: int = 42,
) -> IsolationForest:
    """Train an Isolation Forest model on the provided feature matrix.

    Parameters
    ----------
    X:
        Feature matrix with columns ``temperature``, ``humidity``,
        ``pressure``.
    n_estimators:
        Number of trees in the forest.
    contamination:
        Expected proportion of anomalies in the dataset.
    random_state:
        Random seed for reproducibility.

    Returns
    -------
    IsolationForest
        Fitted model instance.
    """
    model = IsolationForest(
        n_estimators=n_estimators,
        contamination=contamination,
        random_state=random_state,
    )
    model.fit(X)
    return model


def load_model(path: str = "models/isolation_forest.pkl") -> IsolationForest:
    """Load a pre-trained Isolation Forest model from disk.

    Parameters
    ----------
    path:
        File path to the serialised model.

    Returns
    -------
    IsolationForest
        Loaded model instance.
    """
    return joblib.load(path)


def save_model(model: IsolationForest, path: str = "models/isolation_forest.pkl") -> None:
    """Persist a trained model to disk.

    Parameters
    ----------
    model:
        Fitted Isolation Forest instance.
    path:
        Destination file path.
    """
    joblib.dump(model, path)


# ---------------------------------------------------------------------------
# Anomaly detection (used inside Flink map functions)
# ---------------------------------------------------------------------------


def detect_anomaly_batch(
    records: List[Dict],
    model: IsolationForest,
    baseline_window: int = 5,
) -> List[Dict]:
    """Run anomaly detection on a list of weather records.

    This function replicates the dual-detector logic used in the live Flink
    pipeline so that the same detection can be demonstrated in a notebook
    without a running Flink cluster.

    Parameters
    ----------
    records:
        List of weather record dicts (city, temperature, humidity, pressure, ...).
    model:
        Trained Isolation Forest model.
    baseline_window:
        Number of recent normal readings used to compute per-city baseline.

    Returns
    -------
    list[dict]
        Records enriched with ``status``, ``temp_diff``, ``humidity_diff``,
        ``pressure_diff``, and ``iso_prediction`` fields.
    """
    city_history: Dict[str, deque] = defaultdict(lambda: deque(maxlen=baseline_window))
    results = []

    for record in records:
        rec = dict(record)
        city    = rec["city"]
        history = city_history[city]

        if len(history) < baseline_window:
            rec["status"]         = "WARMUP"
            rec["baseline_count"] = len(history) + 1
            rec.setdefault("temp_diff", 0.0)
            rec.setdefault("humidity_diff", 0.0)
            rec.setdefault("pressure_diff", 0.0)
            rec.setdefault("iso_prediction", 0)
            history.append({k: rec[k] for k in FEATURE_NAMES})
            results.append(rec)
            continue

        baseline      = pd.DataFrame(list(history))
        temp_diff     = abs(rec["temperature"] - baseline["temperature"].mean())
        humidity_diff = abs(rec["humidity"]    - baseline["humidity"].mean())
        pressure_diff = abs(rec["pressure"]    - baseline["pressure"].mean())

        input_df = pd.DataFrame([{k: rec[k] for k in FEATURE_NAMES}])
        iso_pred = model.predict(input_df)[0]

        is_alert = (
            temp_diff     >= TEMP_THRESHOLD     or
            humidity_diff >= HUMIDITY_THRESHOLD or
            pressure_diff >= PRESSURE_THRESHOLD or
            iso_pred == -1
        )

        rec["status"]         = "ALERT" if is_alert else "NORMAL"
        rec["temp_diff"]      = round(temp_diff, 2)
        rec["humidity_diff"]  = round(humidity_diff, 2)
        rec["pressure_diff"]  = round(pressure_diff, 2)
        rec["iso_prediction"] = int(iso_pred)

        if rec["status"] == "NORMAL" and not rec.get("injected", False):
            history.append({k: rec[k] for k in FEATURE_NAMES})

        results.append(rec)

    return results


def flink_map_fn(json_str: str, model: IsolationForest, city_history: Dict) -> str:
    """Flink map function for anomaly detection on a single JSON record.

    Called inside a PyFlink DataStream ``map()`` operation.
    Uses module-level state (city_history) which persists across calls in
    PyFlink local mode with parallelism=1.

    Parameters
    ----------
    json_str:
        JSON-encoded weather record string emitted by the source.
    model:
        Loaded Isolation Forest model.
    city_history:
        Per-city deque of recent readings (maintained across map calls).

    Returns
    -------
    str
        JSON-encoded result record with detection fields appended.
    """
    rec     = json.loads(json_str)
    city    = rec["city"]
    history = city_history[city]

    if len(history) < 5:
        rec["status"]         = "WARMUP"
        rec["baseline_count"] = len(history) + 1
        rec.setdefault("temp_diff", 0.0)
        rec.setdefault("humidity_diff", 0.0)
        rec.setdefault("pressure_diff", 0.0)
        rec.setdefault("iso_prediction", 0)
        history.append({k: rec[k] for k in FEATURE_NAMES})
        return json.dumps(rec)

    baseline      = pd.DataFrame(list(history))
    temp_diff     = abs(rec["temperature"] - baseline["temperature"].mean())
    humidity_diff = abs(rec["humidity"]    - baseline["humidity"].mean())
    pressure_diff = abs(rec["pressure"]    - baseline["pressure"].mean())

    input_df = pd.DataFrame([{k: rec[k] for k in FEATURE_NAMES}])
    iso_pred = model.predict(input_df)[0]

    is_alert = (
        temp_diff >= TEMP_THRESHOLD or
        humidity_diff >= HUMIDITY_THRESHOLD or
        pressure_diff >= PRESSURE_THRESHOLD or
        iso_pred == -1
    )

    rec["status"]         = "ALERT" if is_alert else "NORMAL"
    rec["temp_diff"]      = round(temp_diff, 2)
    rec["humidity_diff"]  = round(humidity_diff, 2)
    rec["pressure_diff"]  = round(pressure_diff, 2)
    rec["iso_prediction"] = int(iso_pred)

    if rec["status"] == "NORMAL" and not rec.get("injected", False):
        history.append({k: rec[k] for k in FEATURE_NAMES})

    return json.dumps(rec)


# ---------------------------------------------------------------------------
# Metrics
# ---------------------------------------------------------------------------


def compute_metrics(df: pd.DataFrame) -> Dict:
    """Compute classification metrics using the ``injected`` column as ground
    truth.

    Parameters
    ----------
    df:
        Log DataFrame containing ``injected`` and ``iso_prediction`` columns.
        Only NORMAL and ALERT rows (not WARMUP) are considered.

    Returns
    -------
    dict
        Dictionary with accuracy, precision, recall, f1_score, and confusion
        matrix components.
    """
    eval_df = df[df["status"].isin(["NORMAL", "ALERT"])].copy()

    y_true = eval_df["injected"].astype(bool).astype(int).values
    y_pred = (eval_df["iso_prediction"] == -1).astype(int).values

    tn, fp, fn, tp = confusion_matrix(y_true, y_pred, labels=[0, 1]).ravel()

    return {
        "total":          len(y_true),
        "n_anomalies":    int(y_true.sum()),
        "n_normal":       int((y_true == 0).sum()),
        "true_positives":  int(tp),
        "true_negatives":  int(tn),
        "false_positives": int(fp),
        "false_negatives": int(fn),
        "accuracy":   round(accuracy_score(y_true, y_pred),   4),
        "precision":  round(precision_score(y_true, y_pred, zero_division=0), 4),
        "recall":     round(recall_score(y_true, y_pred, zero_division=0),    4),
        "f1_score":   round(f1_score(y_true, y_pred, zero_division=0),        4),
    }


def measure_response_time(
    model: IsolationForest,
    sample: pd.DataFrame,
    n_trials: int = 100,
) -> Dict:
    """Measure single-record and batch prediction latency.

    Parameters
    ----------
    model:
        Fitted Isolation Forest instance.
    sample:
        DataFrame of weather features (at least one row).
    n_trials:
        Number of single-record prediction repetitions for averaging.

    Returns
    -------
    dict
        Response time statistics in milliseconds.
    """
    single = sample.iloc[[0]]
    times  = []
    for _ in range(n_trials):
        t0 = time.perf_counter()
        model.predict(single)
        times.append((time.perf_counter() - t0) * 1000)

    t0         = time.perf_counter()
    model.predict(sample)
    batch_ms   = (time.perf_counter() - t0) * 1000

    return {
        "single_avg_ms": round(sum(times) / len(times), 4),
        "single_min_ms": round(min(times), 4),
        "single_max_ms": round(max(times), 4),
        "batch_total_ms": round(batch_ms, 4),
        "batch_per_record_ms": round(batch_ms / len(sample), 4),
    }


# ---------------------------------------------------------------------------
# Visualisation
# ---------------------------------------------------------------------------


def plot_temperature_by_city(df: pd.DataFrame) -> None:
    """Plot temperature over time for each monitored city.

    Parameters
    ----------
    df:
        Log DataFrame with ``timestamp``, ``city``, and ``temperature``
        columns.
    """
    fig, ax = plt.subplots(figsize=(14, 5))
    for city, grp in df.groupby("city"):
        ax.plot(grp["timestamp"], grp["temperature"], marker="o",
                markersize=3, linewidth=1.5, label=city)
    ax.set_title("Temperature over Time by City", fontsize=14)
    ax.set_xlabel("Timestamp")
    ax.set_ylabel("Temperature (°C)")
    ax.legend(title="City")
    plt.tight_layout()
    plt.show()


def plot_alert_timeline(df: pd.DataFrame) -> None:
    """Scatter plot showing ALERT events across cities over time.

    Parameters
    ----------
    df:
        Log DataFrame with ``timestamp``, ``city``, and ``status`` columns.
    """
    colour_map = {"ALERT": "red", "NORMAL": "green", "WARMUP": "steelblue"}
    fig, ax    = plt.subplots(figsize=(14, 4))
    for status, grp in df.groupby("status"):
        ax.scatter(grp["timestamp"], grp["city"],
                   c=colour_map.get(status, "grey"),
                   label=status, alpha=0.7, s=30)
    ax.set_title("Alert Timeline by City", fontsize=14)
    ax.set_xlabel("Timestamp")
    ax.set_ylabel("City")
    ax.legend(title="Status")
    plt.tight_layout()
    plt.show()


def plot_deviation_histograms(df: pd.DataFrame) -> None:
    """Histogram of per-city deviations for temperature, humidity, pressure.

    Parameters
    ----------
    df:
        Log DataFrame containing deviation columns.
    """
    eval_df = df[df["status"].isin(["NORMAL", "ALERT"])]
    fig, axes = plt.subplots(1, 3, figsize=(15, 4))
    cols = ["temp_diff", "humidity_diff", "pressure_diff"]
    titles = ["Temperature Deviation (°C)", "Humidity Deviation (%)", "Pressure Deviation (hPa)"]
    thresholds = [TEMP_THRESHOLD, HUMIDITY_THRESHOLD, PRESSURE_THRESHOLD]

    for ax, col, title, thresh in zip(axes, cols, titles, thresholds):
        eval_df[col].hist(bins=30, ax=ax, color="steelblue", edgecolor="white")
        ax.axvline(thresh, color="red", linestyle="--", label=f"Threshold ({thresh})")
        ax.set_title(title)
        ax.set_xlabel("Deviation")
        ax.set_ylabel("Count")
        ax.legend()

    plt.tight_layout()
    plt.show()


def plot_confusion_matrix(metrics: Dict) -> None:
    """Visualise the confusion matrix from computed metrics.

    Parameters
    ----------
    metrics:
        Dictionary returned by :func:`compute_metrics`.
    """
    cm = np.array([
        [metrics["true_negatives"],  metrics["false_positives"]],
        [metrics["false_negatives"], metrics["true_positives"]],
    ])
    fig, ax = plt.subplots(figsize=(5, 4))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
                xticklabels=["Predicted Normal", "Predicted Anomaly"],
                yticklabels=["Actual Normal", "Actual Anomaly"], ax=ax)
    ax.set_title("Isolation Forest: Confusion Matrix")
    plt.tight_layout()
    plt.show()


def plot_anomaly_score_distribution(
    model: IsolationForest,
    X: pd.DataFrame,
) -> None:
    """Plot the distribution of Isolation Forest anomaly scores.

    Parameters
    ----------
    model:
        Fitted Isolation Forest instance.
    X:
        Feature matrix.
    """
    scores = model.decision_function(X)
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.hist(scores, bins=40, color="steelblue", edgecolor="white")
    ax.axvline(0, color="red", linestyle="--", label="Decision boundary")
    ax.set_title("Isolation Forest Anomaly Score Distribution")
    ax.set_xlabel("Anomaly Score (lower = more anomalous)")
    ax.set_ylabel("Count")
    ax.legend()
    plt.tight_layout()
    plt.show()
