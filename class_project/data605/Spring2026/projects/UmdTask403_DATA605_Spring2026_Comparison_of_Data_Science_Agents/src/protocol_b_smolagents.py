"""
Smolagents native-paradigm sub-experiment.

Goal: demonstrate that smolagents succeeds when given prompts framed in
its native code-iterative style, contradicting its same-prompt-rule
failure mode where it hallucinates import restrictions and hand-rolls
broken TF-IDF.

Native paradigm conventions:
- Conversational task description, not "you are given file X"
- Explicit named imports (avoid the "constraints on imports" hallucination)
- Per-step reasoning hints (smolagents iterates so make iteration easy)
- Plain success criterion (F1 weighted, save predictions.csv)

Output: results/protocol_b/smolagents_native_results.json plus printed summary.

Usage:
    .venv/bin/python -m src.protocol_b_smolagents
"""
import os, sys, time, json, shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.utils import DATA_RAW
from src.cost_tracker import calculate_cost

# Native-style prompts. Avoid the "you are given a file" framing that
# triggered smolagents to claim it had import restrictions; use
# conversational task framing with explicit library availability.
NATIVE_TASKS = {
    "HD-PRED": {
        "csv": "heart_disease.csv",
        "prompt": (
            "I want you to build a binary classifier for heart disease. "
            "The data is in heart_disease.csv (303 rows). The 'target' column "
            "is 1 (disease) or 0 (no disease). You have full access to sklearn, "
            "pandas, numpy. Use sklearn.ensemble.RandomForestClassifier or "
            "LogisticRegression. Split 80/20 with random_state=42. Train, "
            "predict on the test split, and save the predictions to predictions.csv "
            "in the working directory with columns y_true and y_pred. "
            "Print the weighted F1 score on the test set as your final result."
        ),
        "metric": "f1_weighted",
    },
    "AR-PRED": {
        "csv": "amazon_reviews.csv",
        "prompt": (
            "I want you to build a sentiment classifier on Amazon reviews. "
            "The data is in amazon_reviews.csv. Use sklearn.feature_extraction.text.TfidfVectorizer "
            "to vectorize the 'text' column. Convert the 'rating' column to binary: "
            "rating >= 4 is positive (1), rating <= 2 is negative (0), and DROP rating == 3. "
            "Use sklearn.linear_model.LogisticRegression. Split 80/20 with random_state=42. "
            "Save predictions.csv with columns y_true and y_pred (both binary 0/1). "
            "Print the weighted F1 score on the test set as your final result."
        ),
        "metric": "f1_weighted",
    },
}


def run_native_smolagents(task_name, task_def, n_runs=3, max_steps=8):
    """Run smolagents with a paradigm-native prompt against a workspace
    containing the named CSV. Returns a list of per-run dicts."""
    from smolagents import CodeAgent, OpenAIServerModel
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY not set")

    from sklearn.metrics import f1_score
    import pandas as pd

    runs = []
    for run_id in range(1, n_runs + 1):
        # Fresh workspace per run
        ws = ROOT / "results" / "protocol_b" / "smolagents_native_workspace" / f"{task_name}_run{run_id}"
        ws.mkdir(parents=True, exist_ok=True)
        for f in ws.glob("*"):
            f.unlink()
        shutil.copy2(DATA_RAW / task_def["csv"], ws / task_def["csv"])

        original_cwd = os.getcwd()
        os.chdir(ws)
        try:
            model = OpenAIServerModel(model_id="gpt-4o", api_key=api_key)
            agent = CodeAgent(
                tools=[], model=model, max_steps=max_steps,
                additional_authorized_imports=[
                    "pandas", "numpy", "sklearn", "matplotlib", "seaborn",
                    "sklearn.ensemble", "sklearn.linear_model",
                    "sklearn.feature_extraction.text", "sklearn.metrics",
                    "sklearn.model_selection",
                ],
            )
            start = time.perf_counter()
            try:
                result_text = agent.run(task_def["prompt"])
                elapsed = time.perf_counter() - start
                err = None
            except Exception as e:
                elapsed = time.perf_counter() - start
                result_text = ""
                err = str(e)[:300]

            in_tok = getattr(agent.monitor, "total_input_token_count", 0) or 0
            out_tok = getattr(agent.monitor, "total_output_token_count", 0) or 0

            # Score the predictions.csv if it exists
            f1 = None
            score_err = None
            pred_path = ws / "predictions.csv"
            if pred_path.exists():
                try:
                    df = pd.read_csv(pred_path)
                    if "y_true" in df.columns and "y_pred" in df.columns:
                        f1 = round(float(f1_score(df["y_true"], df["y_pred"], average="weighted", zero_division=0)), 4)
                    else:
                        score_err = f"missing y_true / y_pred; columns: {list(df.columns)}"
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
            "result_text_head": str(result_text or "")[:300],
        })
    return runs


def main():
    out = {"per_task": {}, "summary": {}}
    for task_name, task_def in NATIVE_TASKS.items():
        print(f"\n=== smolagents native: {task_name} ===")
        runs = run_native_smolagents(task_name, task_def)
        out["per_task"][task_name] = runs
        for r in runs:
            print(f"  run{r['run_id']}  F1={r['f1_weighted']!r}  "
                  f"elapsed={r['elapsed_sec']}s  tokens={r['input_tokens'] + r['output_tokens']}  "
                  f"score_err={r['score_error'][:60] if r['score_error'] else None}")

    # Summary
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
        "total_cost_usd": calculate_cost("smolagents", in_tok, out_tok),
    }

    out_path = ROOT / "results" / "protocol_b" / "smolagents_native_results.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(out, indent=2, default=str))

    s = out["summary"]
    print(f"\n{'='*60}")
    print("SMOLAGENTS NATIVE-PARADIGM SUMMARY")
    print(f"{'='*60}")
    print(f"Total runs:    {s['total_runs']}")
    print(f"Successes:     {s['successes']}")
    print(f"Success rate:  {s['successes'] / max(s['total_runs'], 1):.1%}")
    print(f"Total cost:    ${s['total_cost_usd']:.4f}")
    print(f"Saved: {out_path}")


if __name__ == "__main__":
    main()
