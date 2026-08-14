"""
Category: Lightweight NL→pandas (local)
"""
import os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from src.utils import make_result, log
import pandas as pd

def run(prompt, task_config, work_dir, output_dir):
    try:
        from pandasai import SmartDataframe
    except ImportError:
        return make_result("pandasai", task_config.get("task_id", "?"), error="pandasai not installed")

    data_files = [f for f in os.listdir(work_dir) if f.endswith((".csv", ".parquet"))] if os.path.exists(work_dir) else []
    if not data_files:
        return make_result("pandasai", task_config.get("task_id", "?"), error="No data files")

    data_file = os.path.join(work_dir, data_files[0])
    df = pd.read_csv(data_file) if data_file.endswith(".csv") else pd.read_parquet(data_file)

    start = time.perf_counter()
    try:
        sdf = SmartDataframe(df)
        result_text = sdf.chat(prompt)
        elapsed = time.perf_counter() - start
        return make_result(agent_id="pandasai", task_id=task_config.get("task_id", "?"),
                           generated_code=None, wall_clock_sec=elapsed, cost_usd=0.0,
                           raw_output=str(result_text)[:10000])
    except Exception as e:
        return make_result("pandasai", task_config.get("task_id", "?"),
                           wall_clock_sec=time.perf_counter() - start, error=str(e))
