import pandas as pd
import numpy as np
import joblib
from sklearn.ensemble import IsolationForest

# -- 1. Real collected data (non-injected only) ------------------------------
logs = pd.read_csv("logs/weather_alerts.csv")
real = logs[logs["injected"] == False][["temperature", "humidity", "pressure"]].copy()
print(f"Real non-injected readings: {len(real)}")

# -- 2. Synthetic normal data per city across all seasons --------------------
# Ranges derived from real climate data for each city
# (winter low -> summer high, realistic humidity/pressure bands)
rng = np.random.default_rng(42)

city_profiles = {
    "College Park": dict(
        temp=(-5, 36), humidity=(35, 92), pressure=(995, 1028)
    ),
    "New York": dict(
        temp=(-8, 36), humidity=(40, 90), pressure=(990, 1030)
    ),
    "Boston": dict(
        temp=(-12, 33), humidity=(45, 95), pressure=(985, 1030)
    ),
    "Chicago": dict(
        temp=(-18, 36), humidity=(30, 88), pressure=(983, 1035)
    ),
}

synthetic_rows = []
per_city = 600  # readings per city

for city, p in city_profiles.items():
    temps    = rng.uniform(*p["temp"],     per_city)
    humidity = rng.uniform(*p["humidity"], per_city).astype(int)
    pressure = rng.uniform(*p["pressure"], per_city).astype(int)

    for t, h, pr in zip(temps, humidity, pressure):
        synthetic_rows.append({
            "temperature": round(float(t), 2),
            "humidity":    int(h),
            "pressure":    int(pr)
        })

synthetic = pd.DataFrame(synthetic_rows)
print(f"Synthetic normal readings: {len(synthetic)}")

# -- 3. Combine and train -----------------------------------------------------
X = pd.concat([real, synthetic], ignore_index=True)[["temperature", "humidity", "pressure"]]
print(f"Total training samples: {len(X)}")

model = IsolationForest(
    n_estimators=200,
    contamination=0.05,   # lower = less aggressive flagging
    random_state=42
)
model.fit(X)

joblib.dump(model, "models/isolation_forest.pkl")
print("Model retrained and saved to models/isolation_forest.pkl")

# -- 4. Quick sanity check ----------------------------------------------------
test_normal  = pd.DataFrame([{"temperature": 15.0, "humidity": 85, "pressure": 1005}])
test_anomaly = pd.DataFrame([{"temperature": 50.0, "humidity": 5,  "pressure": 870}])
print(f"Sanity - normal reading (Boston-like):  {model.predict(test_normal)[0]}")   # expect 1
print(f"Sanity - obvious anomaly:               {model.predict(test_anomaly)[0]}")  # expect -1
