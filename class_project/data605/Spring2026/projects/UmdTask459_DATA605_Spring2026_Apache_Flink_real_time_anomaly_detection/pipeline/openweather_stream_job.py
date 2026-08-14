import os
import time
import json
import random
import csv
import smtplib
import requests
import pandas as pd
import joblib
from datetime import datetime, date
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
from collections import defaultdict, deque

from pyflink.datastream import StreamExecutionEnvironment
from pyflink.common.typeinfo import Types

from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

load_dotenv()

# -- Config --------------------------------------------------------------------
INFLUX_URL    = "http://influxdb:8086"
INFLUX_TOKEN  = "weather-token-123"
INFLUX_ORG    = "weather-org"
INFLUX_BUCKET = "weather-data"

API_KEY               = os.getenv("OPENWEATHER_API_KEY")
GMAIL_USER            = os.getenv("GMAIL_USER")
GMAIL_APP_PASSWORD    = os.getenv("GMAIL_APP_PASSWORD")
ALERT_RECIPIENT       = os.getenv("ALERT_RECIPIENT")
CITIES                = ["College Park", "New York", "Boston", "Chicago"]
POLL_INTERVAL_SECONDS = 600
MAX_DAILY_CALLS       = 800
BASELINE_WINDOW       = 5
ENABLE_INJECTION      = True
FEATURES              = ["temperature", "humidity", "pressure"]
EMAIL_COOLDOWN_SECS   = 1800  # max one email per city every 30 minutes

# -- Module-level state (persistent across Flink batches in local mode) --------
_model              = joblib.load("models/isolation_forest.pkl")
_city_history       = defaultdict(lambda: deque(maxlen=BASELINE_WINDOW))
_influx_client      = None
_write_api          = None
_last_email_sent    = {}  # city -> timestamp of last alert email


def _get_write_api():
    global _influx_client, _write_api
    if _write_api is None:
        _influx_client = InfluxDBClient(url=INFLUX_URL, token=INFLUX_TOKEN, org=INFLUX_ORG)
        _write_api     = _influx_client.write_api(write_options=SYNCHRONOUS)
    return _write_api


def _baseline_ready():
    return all(len(_city_history[c]) >= BASELINE_WINDOW for c in CITIES)


# -- Helpers -------------------------------------------------------------------

def send_alert_email(record):
    city = record["city"]
    now  = time.time()

    # Cooldown - avoid flooding inbox
    if now - _last_email_sent.get(city, 0) < EMAIL_COOLDOWN_SECS:
        return

    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = f" Weather Anomaly Alert - {city}"
        msg["From"]    = GMAIL_USER
        msg["To"]      = ALERT_RECIPIENT

        body = f"""
Weather Anomaly Detected!

City       : {city}
Time       : {record['timestamp']}
Status     : {record['status']}

Temperature : {record['temperature']}°C  (diff: {record.get('temp_diff', 0)})
Humidity    : {record['humidity']}%       (diff: {record.get('humidity_diff', 0)})
Pressure    : {record['pressure']} hPa   (diff: {record.get('pressure_diff', 0)})

Isolation Forest : {'ANOMALY' if record.get('iso_prediction') == -1 else 'NORMAL'}
Injected         : {record.get('injected', False)}

-- Real-Time Weather Anomaly Detection System
"""
        msg.attach(MIMEText(body, "plain"))

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
            server.sendmail(GMAIL_USER, ALERT_RECIPIENT, msg.as_string())

        _last_email_sent[city] = now
        print(f"Alert email sent for {city}")

    except Exception as e:
        print(f"Email error for {city}: {e}")


def fetch_weather(city, call_count):
    params = {"q": city, "appid": API_KEY, "units": "metric"}
    try:
        r = requests.get("https://api.openweathermap.org/data/2.5/weather",
                         params=params, timeout=10)
    except Exception as e:
        print(f"Request error for {city}: {e}")
        return None

    if r.status_code != 200:
        print(f"API error for {city}: {r.status_code}")
        return None

    d = r.json()
    return {
        "city":            city,
        "temperature":     d["main"]["temp"],
        "humidity":        d["main"]["humidity"],
        "pressure":        d["main"]["pressure"],
        "timestamp":       datetime.utcnow().isoformat(),
        "api_calls_today": call_count,
        "injected":        False
    }


def maybe_inject_anomaly(record, probability=0.10):
    if random.random() > probability:
        return record
    anomaly_type = random.choice(FEATURES)
    if anomaly_type == "temperature":
        record["temperature"] = round(record["temperature"] + random.choice([-1, 1]) * random.uniform(8, 14), 2)
    elif anomaly_type == "humidity":
        record["humidity"] = max(0, min(100, round(record["humidity"] + random.choice([-1, 1]) * random.uniform(25, 45))))
    elif anomaly_type == "pressure":
        record["pressure"] = round(record["pressure"] + random.choice([-1, 1]) * random.uniform(18, 35))
    record["injected"]       = True
    record["injection_type"] = anomaly_type
    return record


def log_result(result):
    path       = "logs/weather_alerts.csv"
    fieldnames = ["timestamp", "city", "temperature", "humidity", "pressure",
                  "status", "temp_diff", "humidity_diff", "pressure_diff",
                  "iso_prediction", "injected", "api_calls_today"]
    row        = {k: result.get(k, 0) for k in fieldnames}
    exists     = os.path.exists(path)
    with open(path, "a", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        if not exists:
            w.writeheader()
        w.writerow(row)


def print_result(r):
    inj = f" | Injected={r.get('injection_type')}" if r.get("injected") else ""
    if r["status"] == "WARMUP":
        print(f"WARMUP | City={r['city']} | Temp={r['temperature']}°C | "
              f"Humidity={r['humidity']} | Pressure={r['pressure']} | "
              f"Baseline={r.get('baseline_count','?')}/{BASELINE_WINDOW} | "
              f"CallsToday={r['api_calls_today']}")
    else:
        print(f"{r['status']} | City={r['city']} | Temp={r['temperature']}°C | "
              f"Humidity={r['humidity']} | Pressure={r['pressure']} | "
              f"TempDiff={r.get('temp_diff',0)} | HumDiff={r.get('humidity_diff',0)} | "
              f"PressDiff={r.get('pressure_diff',0)} | Iso={r.get('iso_prediction',0)} | "
              f"CallsToday={r['api_calls_today']}{inj}")


# -- Flink map function --------------------------------------------------------

def detect_and_sink(json_str: str) -> str:
    """
    Flink map function: detects anomalies, writes to InfluxDB + CSV, returns result.
    Runs inside Flink's DataStream pipeline via PyFlink local execution.
    """
    record  = json.loads(json_str)
    city    = record["city"]
    history = _city_history[city]

    if len(history) < BASELINE_WINDOW:
        record["status"]         = "WARMUP"
        record["baseline_count"] = len(history) + 1
        record.setdefault("temp_diff", 0)
        record.setdefault("humidity_diff", 0)
        record.setdefault("pressure_diff", 0)
        record.setdefault("iso_prediction", 0)
        history.append({k: record[k] for k in FEATURES})
    else:
        baseline      = pd.DataFrame(list(history))
        temp_diff     = abs(record["temperature"] - baseline["temperature"].mean())
        humidity_diff = abs(record["humidity"]    - baseline["humidity"].mean())
        pressure_diff = abs(record["pressure"]    - baseline["pressure"].mean())

        iso_pred = _model.predict(pd.DataFrame([{k: record[k] for k in FEATURES}]))[0]

        is_alert = (temp_diff >= 7 or humidity_diff >= 25 or
                    pressure_diff >= 15 or iso_pred == -1)

        record["status"]         = "ALERT" if is_alert else "NORMAL"
        record["temp_diff"]      = round(temp_diff, 2)
        record["humidity_diff"]  = round(humidity_diff, 2)
        record["pressure_diff"]  = round(pressure_diff, 2)
        record["iso_prediction"] = int(iso_pred)

        if record["status"] == "NORMAL" and not record.get("injected", False):
            history.append({k: record[k] for k in FEATURES})

    print_result(record)
    log_result(record)

    if record["status"] == "ALERT":
        send_alert_email(record)

    # InfluxDB write
    write_api = _get_write_api()
    point = (
        Point("weather_readings")
        .tag("city",   record["city"])
        .tag("status", record["status"])
        .field("temperature",     float(record["temperature"]))
        .field("humidity",        float(record["humidity"]))
        .field("pressure",        float(record["pressure"]))
        .field("temp_diff",       float(record.get("temp_diff", 0)))
        .field("humidity_diff",   float(record.get("humidity_diff", 0)))
        .field("pressure_diff",   float(record.get("pressure_diff", 0)))
        .field("api_calls_today", int(record["api_calls_today"]))
        .field("injected",        int(record.get("injected", False)))
        .field("is_alert",        1 if record["status"] == "ALERT" else 0)
        .time(datetime.utcnow(), WritePrecision.NS)
    )
    write_api.write(bucket=INFLUX_BUCKET, org=INFLUX_ORG, record=point)

    return json.dumps(record)


# -- Main ----------------------------------------------------------------------

def main():
    if not API_KEY:
        raise ValueError("OPENWEATHER_API_KEY not set. Check your .env file.")

    # Create Flink environment once - reused across all polling batches
    env = StreamExecutionEnvironment.get_execution_environment()
    env.set_parallelism(1)

    call_count   = 0
    current_day  = date.today()

    while True:
        if date.today() != current_day:
            current_day = date.today()
            call_count  = 0

        if call_count >= MAX_DAILY_CALLS:
            print("Daily API limit reached. Sleeping 60s.")
            time.sleep(60)
            continue

        print("\n--- New API Batch ---")
        ready = _baseline_ready()
        print("Baseline ready. Injection active." if ready else "Baseline not ready. Injection OFF.")

        json_records = []
        for city in CITIES:
            record = fetch_weather(city, call_count)
            if record is None:
                continue
            call_count += 1
            record["api_calls_today"] = call_count
            if ENABLE_INJECTION and ready:
                record = maybe_inject_anomaly(record)
            json_records.append(json.dumps(record))

        if json_records:
            # -- Flink pipeline ----------------------------------------------
            # Source  : in-memory collection of JSON weather records
            # Map     : anomaly detection (baseline + Isolation Forest)
            # Sink    : written inside map (InfluxDB + CSV); print() for logging
            # Execute : blocking call - completes before next sleep
            # ---------------------------------------------------------------
            env.from_collection(json_records, type_info=Types.STRING()) \
               .map(detect_and_sink, output_type=Types.STRING())

            env.execute("Real-Time Weather Anomaly Detection")

        print(f"Sleeping for {POLL_INTERVAL_SECONDS}s...")
        time.sleep(POLL_INTERVAL_SECONDS)


if __name__ == "__main__":
    main()
