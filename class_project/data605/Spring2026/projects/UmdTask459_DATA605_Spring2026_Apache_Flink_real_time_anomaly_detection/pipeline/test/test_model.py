import time
import json
import pandas as pd
import joblib
from datetime import datetime
from sklearn.metrics import precision_score, recall_score, f1_score, confusion_matrix, accuracy_score

model = joblib.load("models/isolation_forest.pkl")
feature_names = ["temperature", "humidity", "pressure"]

# -- Load logs - only NORMAL/ALERT rows with known injection ground truth -----
df = pd.read_csv("logs/weather_alerts.csv")
df = df[df["status"].isin(["NORMAL", "ALERT"])].copy()
df = df.dropna(subset=feature_names)

if df.empty:
    print("No NORMAL/ALERT records in logs yet. Run the app longer before evaluating.")
    exit()

X = df[feature_names]

# Ground truth: injected=True -> anomaly (1), injected=False -> normal (0)
y_true = df["injected"].astype(bool).astype(int).values

# -- Single-record response time -----------------------------------------------
single = X.iloc[[0]]
times = []
for _ in range(100):
    t0 = time.perf_counter()
    model.predict(single)
    times.append((time.perf_counter() - t0) * 1000)  # ms

avg_response_ms  = round(sum(times) / len(times), 4)
min_response_ms  = round(min(times), 4)
max_response_ms  = round(max(times), 4)

# -- Batch prediction ----------------------------------------------------------
t0 = time.perf_counter()
raw_preds = model.predict(X)
batch_time_ms = round((time.perf_counter() - t0) * 1000, 4)

# Convert Isolation Forest output (-1 anomaly, 1 normal) -> (1 anomaly, 0 normal)
y_pred = (raw_preds == -1).astype(int)

# -- Metrics -------------------------------------------------------------------
precision = precision_score(y_true, y_pred, zero_division=0)
recall    = recall_score(y_true, y_pred, zero_division=0)
f1        = f1_score(y_true, y_pred, zero_division=0)
accuracy  = accuracy_score(y_true, y_pred)
tn, fp, fn, tp = confusion_matrix(y_true, y_pred, labels=[0, 1]).ravel()

total      = len(y_true)
n_anomaly  = int(y_true.sum())
n_normal   = total - n_anomaly

metrics = {
    "evaluated_at": datetime.utcnow().isoformat(),
    "dataset": {
        "total_records": total,
        "normal_records": n_normal,
        "injected_anomalies": n_anomaly
    },
    "classification": {
        "true_positives":  int(tp),
        "true_negatives":  int(tn),
        "false_positives": int(fp),
        "false_negatives": int(fn),
        "accuracy":        round(accuracy, 4),
        "precision":       round(precision, 4),
        "recall":          round(recall, 4),
        "f1_score":        round(f1, 4)
    },
    "response_time_ms": {
        "single_record_avg": avg_response_ms,
        "single_record_min": min_response_ms,
        "single_record_max": max_response_ms,
        "batch_total":       batch_time_ms,
        "batch_per_record":  round(batch_time_ms / total, 4)
    }
}

# -- Save ----------------------------------------------------------------------
output_path = "logs/model_metrics.json"
with open(output_path, "w") as f:
    json.dump(metrics, f, indent=2)

# -- Print ---------------------------------------------------------------------
print("=" * 50)
print("  Isolation Forest - Model Evaluation")
print("=" * 50)
print(f"  Records evaluated : {total}  (normal={n_normal}, anomaly={n_anomaly})")
print(f"  Accuracy          : {accuracy:.4f}")
print(f"  Precision         : {precision:.4f}")
print(f"  Recall            : {recall:.4f}")
print(f"  F1 Score          : {f1:.4f}")
print(f"  True Positives    : {tp}")
print(f"  True Negatives    : {tn}")
print(f"  False Positives   : {fp}")
print(f"  False Negatives   : {fn}")
print("-" * 50)
print(f"  Response time (single) avg : {avg_response_ms} ms")
print(f"  Response time (single) min : {min_response_ms} ms")
print(f"  Response time (single) max : {max_response_ms} ms")
print(f"  Batch time ({total} records) : {batch_time_ms} ms")
print(f"  Batch per record            : {batch_time_ms / total:.4f} ms")
print("=" * 50)
print(f"\nMetrics saved to {output_path}")
