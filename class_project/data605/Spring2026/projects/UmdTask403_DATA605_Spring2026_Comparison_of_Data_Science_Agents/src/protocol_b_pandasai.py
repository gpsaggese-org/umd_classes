"""
PandasAI native-paradigm sub-experiment.

Research goal: characterize PandasAI's behavior under prompts written in
its native paradigm (in-memory DataFrame.chat() with conversational
queries returning dict results) versus the same-prompt benchmark
convention (file-based outputs).

Key research finding aimed for: PandasAI is paradigm-locked. It fails
uniformly under the benchmark's same-prompt rule (see findings_step5
F4 and findings_adversarial A2) but succeeds when given conversational
queries in its native style. This characterizes WHEN pandasai is
useful, which is itself a publishable contribution.

Output: results/protocol_b/pandasai_native_results.json plus a printed
summary.

Usage:
    .venv/bin/python -m src.protocol_b_pandasai
"""
import os
import sys
import time
import json
import traceback
from pathlib import Path

# Project root
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.utils import DATA_RAW
from src.cost_tracker import calculate_cost

import pandas as pd

# Native pandasai paradigm: ask questions that return a dict result.
# These mirror the categories of tasks in tasks.yaml (descriptive, EDA,
# predictive, prescriptive) but rephrased for pandasai's native interface.
NATIVE_QUERIES = {
    "heart_disease": [
        # Descriptive
        "What is the average age of patients in this dataset? Return as a number.",
        "What percentage of patients have heart disease (target = 1)? Return as a percentage.",
        # EDA-style
        "Which feature has the highest correlation with the target? Return the feature name and its correlation value.",
        "Among patients with heart disease, what is the average cholesterol level? Return as a number.",
        # Comparison
        "Compare the average age of patients with and without heart disease. Return both numbers.",
    ],
    "amazon_reviews": [
        "What is the average rating in this dataset? Return as a number.",
        "What percentage of reviews are 5-star? Return as a percentage.",
        "What is the longest review's character count? Return as a number.",
        "Compare average review length between 1-star and 5-star reviews. Return both numbers.",
    ],
}


def _make_usage_tracking_llm(api_key):
    """Same wrapper as in agents/pandasai/run_task.py for cumulative tokens."""
    from pandasai_openai import OpenAI

    class _UsageTrackingOpenAI(OpenAI):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.cumulative_usage = {"input_tokens": 0, "output_tokens": 0}

        def chat_completion(self, value, memory):
            messages = memory.to_openai_messages() if memory else []
            messages.append({"role": "user", "content": value})
            params = {**self._invocation_params, "messages": messages}
            if self.stop is not None:
                params["stop"] = [self.stop]
            response = self.client.create(**params)
            usage = getattr(response, "usage", None)
            if usage:
                self.cumulative_usage["input_tokens"]  += getattr(usage, "prompt_tokens",     0) or 0
                self.cumulative_usage["output_tokens"] += getattr(usage, "completion_tokens", 0) or 0
            return response.choices[0].message.content

    return _UsageTrackingOpenAI(api_token=api_key)


def run_native_query(df, query, llm):
    """Run one pandasai native query. Return (success, result_str, elapsed,
    in_tokens, out_tokens, error)."""
    from pandasai import SmartDataframe
    sdf = SmartDataframe(df, config={"llm": llm})
    start = time.perf_counter()
    in_before  = llm.cumulative_usage["input_tokens"]
    out_before = llm.cumulative_usage["output_tokens"]
    try:
        result = sdf.chat(query)
        elapsed = time.perf_counter() - start
        in_used  = llm.cumulative_usage["input_tokens"]  - in_before
        out_used = llm.cumulative_usage["output_tokens"] - out_before
        return {
            "success": True,
            "result": str(result)[:1000],
            "elapsed_sec": round(elapsed, 2),
            "input_tokens": in_used,
            "output_tokens": out_used,
            "error": None,
        }
    except Exception as e:
        elapsed = time.perf_counter() - start
        in_used  = llm.cumulative_usage["input_tokens"]  - in_before
        out_used = llm.cumulative_usage["output_tokens"] - out_before
        return {
            "success": False,
            "result": None,
            "elapsed_sec": round(elapsed, 2),
            "input_tokens": in_used,
            "output_tokens": out_used,
            "error": str(e)[:300],
        }


def main():
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("ERROR: OPENAI_API_KEY not set")
        sys.exit(1)

    out = {
        "summary": {
            "total_queries": 0,
            "successes": 0,
            "failures": 0,
            "total_input_tokens": 0,
            "total_output_tokens": 0,
            "total_cost_usd": 0.0,
            "total_elapsed_sec": 0.0,
        },
        "per_dataset": {},
    }

    for dataset_name, queries in NATIVE_QUERIES.items():
        if dataset_name == "heart_disease":
            df = pd.read_csv(DATA_RAW / "heart_disease.csv")
        elif dataset_name == "amazon_reviews":
            df = pd.read_csv(DATA_RAW / "amazon_reviews.csv")
        else:
            continue

        print(f"\n=== {dataset_name} ({len(df)} rows) ===")
        ds_out = {"queries": [], "n_success": 0, "n_fail": 0}
        # Fresh LLM per dataset so we can attribute usage cleanly
        llm = _make_usage_tracking_llm(api_key)

        for q in queries:
            print(f"  Q: {q[:80]}...")
            res = run_native_query(df, q, llm)
            ds_out["queries"].append({"query": q, **res})
            if res["success"]:
                ds_out["n_success"] += 1
                print(f"    PASS  ({res['elapsed_sec']}s, {res['input_tokens'] + res['output_tokens']} tok)")
                print(f"    A: {res['result'][:200]}")
            else:
                ds_out["n_fail"] += 1
                print(f"    FAIL  ({res['elapsed_sec']}s)  err: {res['error'][:100]}")

            out["summary"]["total_queries"] += 1
            out["summary"]["total_input_tokens"]  += res["input_tokens"]
            out["summary"]["total_output_tokens"] += res["output_tokens"]
            out["summary"]["total_elapsed_sec"]   += res["elapsed_sec"]

        out["summary"]["successes"] += ds_out["n_success"]
        out["summary"]["failures"]  += ds_out["n_fail"]
        out["per_dataset"][dataset_name] = ds_out

    out["summary"]["total_cost_usd"] = calculate_cost(
        "pandasai",
        out["summary"]["total_input_tokens"],
        out["summary"]["total_output_tokens"],
    )

    out_path = ROOT / "results" / "protocol_b" / "pandasai_native_results.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(out, indent=2, default=str))

    print("\n" + "=" * 60)
    print("PANDASAI NATIVE-PARADIGM SUMMARY")
    print("=" * 60)
    s = out["summary"]
    print(f"Total queries: {s['total_queries']}")
    print(f"Successes:     {s['successes']}")
    print(f"Failures:      {s['failures']}")
    print(f"Success rate:  {s['successes'] / max(s['total_queries'], 1):.1%}")
    print(f"Total tokens:  in {s['total_input_tokens']}, out {s['total_output_tokens']}")
    print(f"Total cost:    ${s['total_cost_usd']:.4f}")
    print(f"Total time:    {s['total_elapsed_sec']:.1f}s")
    print(f"\nResults saved: {out_path}")


if __name__ == "__main__":
    main()
