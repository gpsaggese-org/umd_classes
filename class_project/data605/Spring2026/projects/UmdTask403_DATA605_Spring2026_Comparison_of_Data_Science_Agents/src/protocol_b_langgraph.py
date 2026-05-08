"""
LangGraph native-paradigm sub-experiment.

Goal: demonstrate that langgraph succeeds on the AR-ROBU task when given
prompts framed in its native ReAct (reasoning + acting) style with
explicit step decomposition and clear label-type spec, contradicting
its same-prompt-rule failure where it solved binary sentiment when the
benchmark expected 5-class rating.

Native paradigm conventions:
- Step-by-step task decomposition (1, 2, 3, ...)
- Explicit success criterion
- Explicit label types and column names
- Step-wise tool/library naming

Output: results/protocol_b/langgraph_native_results.json plus printed summary.

Usage:
    .venv/bin/python -m src.protocol_b_langgraph
"""
import os, sys, time, json, shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.utils import DATA_ADVERSARIAL, DATA_RAW
from src.cost_tracker import calculate_cost

NATIVE_TASKS = {
    "AR-ROBU": {
        "csv": "amazon_reviews.csv",
        "data_dir": DATA_ADVERSARIAL,  # adversarial variant
        "prompt": (
            "Task: Sentiment classification on Amazon reviews under adversarial "
            "label perturbation.\n\n"
            "Step 1: Load amazon_reviews.csv into a pandas DataFrame. The 'rating' "
            "column is integer 1 through 5; the 'text' column is review text.\n\n"
            "Step 2: Create a binary label `y` from rating: y = 1 if rating >= 4 "
            "(positive), y = 0 if rating <= 2 (negative). Drop rows where rating == 3.\n\n"
            "Step 3: Vectorize the text using sklearn.feature_extraction.text.TfidfVectorizer "
            "with max_features=5000 and ngram_range=(1, 2).\n\n"
            "Step 4: Split into train and test with sklearn.model_selection.train_test_split, "
            "test_size=0.2, random_state=42.\n\n"
            "Step 5: Train sklearn.linear_model.LogisticRegression with max_iter=1000 on the "
            "training set.\n\n"
            "Step 6: Predict on the test set and save predictions to predictions.csv with "
            "columns y_true (binary 0 or 1, integer dtype), y_pred (binary 0 or 1, integer "
            "dtype), y_prob (float probability of class 1).\n\n"
            "Success criterion: predictions.csv exists and has the three columns above with "
            "the specified dtypes."
        ),
    },
    "HD-PRED": {
        "csv": "heart_disease.csv",
        "data_dir": DATA_RAW,
        "prompt": (
            "Task: Build a binary classifier on heart_disease data.\n\n"
            "Step 1: Load heart_disease.csv into a pandas DataFrame. The 'target' column is "
            "binary (1 = disease, 0 = no disease).\n\n"
            "Step 2: Encode any categorical features (string-typed columns) using "
            "sklearn.preprocessing.LabelEncoder or pandas.get_dummies.\n\n"
            "Step 3: Split features X and target y. Train/test split with test_size=0.2 and "
            "random_state=42.\n\n"
            "Step 4: Train sklearn.ensemble.RandomForestClassifier with random_state=42.\n\n"
            "Step 5: Predict on test set, predict probabilities for class 1.\n\n"
            "Step 6: Save predictions.csv with columns y_true (int 0 or 1), y_pred (int 0 or 1), "
            "y_prob (float in [0, 1]).\n\n"
            "Success criterion: predictions.csv exists with the three columns matching the spec."
        ),
    },
}


def run_native_langgraph(task_name, task_def, n_runs=3):
    from langgraph.prebuilt import create_react_agent
    from langchain_anthropic import ChatAnthropic
    from sklearn.metrics import f1_score
    import pandas as pd

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("ANTHROPIC_API_KEY not set")

    runs = []
    for run_id in range(1, n_runs + 1):
        ws = ROOT / "results" / "protocol_b" / "langgraph_native_workspace" / f"{task_name}_run{run_id}"
        ws.mkdir(parents=True, exist_ok=True)
        for f in ws.glob("*"):
            if f.is_file():
                f.unlink()
        shutil.copy2(task_def["data_dir"] / task_def["csv"], ws / task_def["csv"])

        original_cwd = os.getcwd()
        os.chdir(ws)
        try:
            llm = ChatAnthropic(
                model="claude-sonnet-4-6", api_key=api_key,
                temperature=0, max_tokens=8192,
            )
            agent = create_react_agent(llm, tools=[])
            start = time.perf_counter()
            try:
                result = agent.invoke({"messages": [{"role": "user", "content": task_def["prompt"]}]})
                elapsed = time.perf_counter() - start
                err = None
                last_message = result["messages"][-1]
                text = last_message.content if hasattr(last_message, "content") else str(last_message)
                usage = last_message.usage_metadata if hasattr(last_message, "usage_metadata") else {}
                in_tok = usage.get("input_tokens", 0) if isinstance(usage, dict) else 0
                out_tok = usage.get("output_tokens", 0) if isinstance(usage, dict) else 0
            except Exception as e:
                elapsed = time.perf_counter() - start
                text = ""
                in_tok = out_tok = 0
                err = str(e)[:300]

            # Code in `text` between ```python ... ``` -- extract and execute it
            import re
            code_blocks = re.findall(r"```python\s*\n(.*?)```", text or "", re.DOTALL)
            code = "\n\n".join(code_blocks) if code_blocks else None
            if code:
                (ws / "solution.py").write_text(code)
                # Execute with timeout
                import subprocess, signal
                try:
                    proc = subprocess.Popen(
                        [sys.executable, "solution.py"],
                        cwd=str(ws),
                        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                        text=True, start_new_session=True,
                    )
                    proc.communicate(timeout=600)
                except subprocess.TimeoutExpired:
                    try:
                        os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
                    except Exception:
                        pass
                except Exception:
                    pass

            f1 = None
            score_err = None
            pred_path = ws / "predictions.csv"
            if pred_path.exists():
                try:
                    df = pd.read_csv(pred_path)
                    if "y_true" in df.columns and "y_pred" in df.columns:
                        f1 = round(float(f1_score(df["y_true"], df["y_pred"], average="weighted", zero_division=0)), 4)
                    else:
                        score_err = f"missing y_true/y_pred; columns: {list(df.columns)}"
                except Exception as e:
                    score_err = str(e)[:200]
            else:
                score_err = "predictions.csv not produced"
        finally:
            os.chdir(original_cwd)

        runs.append({
            "run_id": run_id,
            "elapsed_sec": round(elapsed, 2),
            "input_tokens": in_tok,
            "output_tokens": out_tok,
            "agent_error": err,
            "predictions_csv_present": pred_path.exists(),
            "f1_weighted": f1,
            "score_error": score_err,
        })
    return runs


def main():
    out = {"per_task": {}, "summary": {}}
    for task_name, task_def in NATIVE_TASKS.items():
        print(f"\n=== langgraph native: {task_name} ===")
        runs = run_native_langgraph(task_name, task_def)
        out["per_task"][task_name] = runs
        for r in runs:
            print(f"  run{r['run_id']}  F1={r['f1_weighted']!r}  "
                  f"elapsed={r['elapsed_sec']}s  tokens={r['input_tokens'] + r['output_tokens']}  "
                  f"score_err={r['score_error'][:60] if r['score_error'] else None}")

    n_total = sum(len(v) for v in out["per_task"].values())
    n_success = sum(1 for v in out["per_task"].values() for r in v if r["f1_weighted"] is not None)
    in_tok = sum(r["input_tokens"]  for v in out["per_task"].values() for r in v)
    out_tok = sum(r["output_tokens"] for v in out["per_task"].values() for r in v)
    out["summary"] = {
        "total_runs": n_total,
        "successes": n_success,
        "failures": n_total - n_success,
        "input_tokens": in_tok,
        "output_tokens": out_tok,
        "total_cost_usd": calculate_cost("langgraph", in_tok, out_tok),
    }

    out_path = ROOT / "results" / "protocol_b" / "langgraph_native_results.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(out, indent=2, default=str))

    s = out["summary"]
    print(f"\n{'='*60}")
    print("LANGGRAPH NATIVE-PARADIGM SUMMARY")
    print(f"{'='*60}")
    print(f"Total runs:    {s['total_runs']}")
    print(f"Successes:     {s['successes']}")
    print(f"Success rate:  {s['successes'] / max(s['total_runs'], 1):.1%}")
    print(f"Total cost:    ${s['total_cost_usd']:.4f}")
    print(f"Saved: {out_path}")


if __name__ == "__main__":
    main()
