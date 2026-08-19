# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.16.0
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %% [markdown]
# # CDD Example - Evaluation Harness
#
# Runs the CDD evaluation suite. Two layers:
#
# 1. **Per-output metrics:** automatic metrics on each generated diagram
#    (syntax validity, node count, edge count, has labels, has styles, render
#    success). These do not require an LLM judge.
#
# 2. **Vision-on vs vision-off study:** the centerpiece. Each benchmark
#    prompt is run twice — once with the vision-feedback loop disabled,
#    once with it enabled — and the results are compared.
#
# This notebook is the canonical example notebook (paired with `cdd.example.ipynb`).

# %% [markdown]
# ## 1. Setup

# %%
import os
import sys
import json

sys.path.insert(0, os.path.dirname(os.path.abspath("__file__")))

import cdd_config as config
import cdd_eval as evaluation
import cdd_renderer as renderer
from cdd_orchestrator import CDDOrchestrator
from IPython.display import Image, display
import pandas as pd

print(f"Provider: {config.LLM_PROVIDER}")
print(f"Total benchmark prompts: {len(evaluation.EVAL_TEST_CASES)}")
print(f"Formats covered: {sorted({c['format'] for c in evaluation.EVAL_TEST_CASES})}")

# %% [markdown]
# ## 2. Run the eval suite (single condition: vision off)
#
# Start with the baseline. This is what you'd get without the vision feedback
# loop — single-shot generation.

# %%
print("Running baseline (vision off)...")
results_off = evaluation.run_eval_suite(
    use_llm_judge=False, condition="vision_off",
)
print(f"Completed: {len(results_off)} cases")

# %% [markdown]
# ## 3. Per-prompt results table

# %%
def results_to_dataframe(results, label):
    rows = []
    for r in results:
        rows.append({
            "Prompt": r.prompt[:55] + "...",
            "Format": r.format,
            "Condition": r.condition,
            "Syntax": "✅" if r.syntax_valid else "❌",
            "Renders": "✅" if r.render_success else "❌",
            "Nodes": r.node_count,
            "Edges": r.edge_count,
            "Labels": "✅" if r.has_labels else "❌",
            "Styled": "✅" if r.has_styles else "❌",
        })
    df = pd.DataFrame(rows)
    df.attrs["label"] = label
    return df


df_off = results_to_dataframe(results_off, "vision_off")
display(df_off)

# %% [markdown]
# ## 4. Run with vision feedback on

# %%
print("Running with vision feedback on...")
results_on = evaluation.run_eval_suite(
    use_llm_judge=False, condition="vision_on",
)
print(f"Completed: {len(results_on)} cases")
df_on = results_to_dataframe(results_on, "vision_on")
display(df_on)

# %% [markdown]
# ## 5. Side-by-side summary
#
# This is the key comparison for the report: do the vision-on results
# improve any of the metrics over vision-off?

# %%
summary_off = evaluation.summarize_eval(results_off)
summary_on = evaluation.summarize_eval(results_on)
comparison = pd.DataFrame({
    "vision_off": summary_off,
    "vision_on": summary_on,
})
print("Aggregate metrics by condition:")
display(comparison)

# %% [markdown]
# ## 6. Visual inspection — vision-off vs vision-on per prompt
#
# For each benchmark prompt, render both conditions side-by-side. Useful
# for the human-rated subset of the evaluation.

# %%
for i, (r_off, r_on) in enumerate(zip(results_off, results_on)):
    print(f"\n--- Prompt {i+1}: {r_off.prompt[:80]}... [{r_off.format}] ---")

    if r_off.render_success:
        print("  Vision OFF:")
        try:
            img_off = renderer.render(r_off.diagram_source, r_off.format)
            display(Image(data=img_off))
        except Exception as e:
            print(f"    Render error: {e}")
    else:
        print("  Vision OFF: failed to render")

    if r_on.render_success:
        print("  Vision ON:")
        try:
            img_on = renderer.render(r_on.diagram_source, r_on.format)
            display(Image(data=img_on))
        except Exception as e:
            print(f"    Render error: {e}")
    else:
        print("  Vision ON: failed to render")

    print(f"  Iterations used (vision on): {r_on.iterations_used}")

# %% [markdown]
# ## 7. Multi-turn refinement test
#
# Smoke test that conversation continuity still works.

# %%
orch = CDDOrchestrator(format="graphviz")
src1, img1 = orch.process_message(
    "Simple flowchart: Start -> Process Data -> Analyze -> Report -> End"
)
print(f"Turn 1 — Nodes: {evaluation.count_nodes(src1, 'graphviz')}, "
      f"Edges: {evaluation.count_edges(src1, 'graphviz')}")
display(Image(data=img1))

# %%
src2, img2 = orch.process_message(
    "Add error handling: if Process Data fails, Log Error then Retry"
)
print(f"Turn 2 — Nodes: {evaluation.count_nodes(src2, 'graphviz')}, "
      f"Edges: {evaluation.count_edges(src2, 'graphviz')}")
display(Image(data=img2))

# %%
src3, img3 = orch.process_message("Make error path red and success path green")
print(f"Turn 3 — Has styles: {evaluation.has_styles(src3, 'graphviz')}")
display(Image(data=img3))

# %% [markdown]
# ## 8. Final summary

# %%
print("=" * 60)
print("EVALUATION SUMMARY")
print("=" * 60)
print("\nVision OFF:")
for k, v in summary_off.items():
    print(f"  {k}: {v}")
print("\nVision ON:")
for k, v in summary_on.items():
    print(f"  {k}: {v}")
print("=" * 60)

# %% [markdown]
# ## 9. Save results to JSON
#
# Persist results for the report. Comparing JSON snapshots across runs
# also lets us track regression / improvement over time.

# %%
output = {
    "config": {
        "provider": config.LLM_PROVIDER,
        "vision_max_iterations": config.VISION_MAX_ITERATIONS,
    },
    "vision_off": [r.to_dict() for r in results_off],
    "vision_on": [r.to_dict() for r in results_on],
    "summary_off": summary_off,
    "summary_on": summary_on,
}
out_path = "/tmp/cdd_eval_results.json"
with open(out_path, "w") as f:
    json.dump(output, f, indent=2)
print(f"Saved results to {out_path}")
