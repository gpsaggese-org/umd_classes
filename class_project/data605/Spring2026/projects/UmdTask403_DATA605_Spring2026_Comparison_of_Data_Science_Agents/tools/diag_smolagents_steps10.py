"""
Diagnostic: run smolagents on HD-PRED-01 with max_steps=10 to test whether
the cap is the bottleneck for D1=NaN. Bypasses the canonical task_runner
flow because we want to override max_steps without permanently mutating
configs/tasks.yaml. Results land at results/smolagents/HD-PRED-01_diag10/run_1/.
"""
import sys, shutil, importlib.util
from pathlib import Path

sys.path.insert(0, ".")

from src.utils import (
    load_tasks_config, get_result_dir, save_json, Timer, DATA_RAW,
)
from src.evaluator import evaluate_result
from src.task_runner import _hydrate_generated_code, _hydrate_predictions

AGENT_ID = "smolagents"
TASK_ID = "HD-PRED-01"
DIAG_TASK_ID = "HD-PRED-01_diag10"
MAX_STEPS = 10

tasks = load_tasks_config()
task_cfg = dict(tasks[TASK_ID])
task_cfg["max_steps"] = MAX_STEPS

out_dir = get_result_dir(AGENT_ID, DIAG_TASK_ID, 1)
work_dir = out_dir / "workspace"
work_dir.mkdir(exist_ok=True)
shutil.copy2(DATA_RAW / "heart_disease.csv", work_dir / "heart_disease.csv")

spec = importlib.util.spec_from_file_location("smol_runner", f"agents/{AGENT_ID}/run_task.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

with Timer() as t:
    result = mod.run(
        prompt=task_cfg["prompt"],
        task_config=task_cfg,
        work_dir=str(work_dir),
        output_dir=str(out_dir),
    )

result.setdefault("agent", AGENT_ID)
result.setdefault("task_id", DIAG_TASK_ID)
result.setdefault("run_id", 1)
result.setdefault("wall_clock_sec", t.elapsed)

_hydrate_generated_code(result, work_dir, out_dir)
_hydrate_predictions(result, work_dir, out_dir)

save_json(result, out_dir / "result.json")
sc = evaluate_result(result, task_cfg)
save_json(sc, out_dir / "scorecard.json")

print(f"\n=== smolagents diagnostic (max_steps={MAX_STEPS}) ===")
print(f"wall_clock: {t.elapsed:.1f}s")
print(f"tokens:     {result.get('tokens_used')}")
print(f"cost_usd:   ${result.get('cost_usd', 0):.4f}")
print(f"D1:         {sc.get('D1_accuracy')}")
print(f"D2:         {sc.get('D2_code_quality')}")
print(f"D5:         {sc.get('D5_cost')}")
print(f"predictions present: {result.get('predictions') is not None}")
