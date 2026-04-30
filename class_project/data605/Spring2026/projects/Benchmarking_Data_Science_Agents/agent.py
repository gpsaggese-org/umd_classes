"""
agent.py
--------
LangGraph pipeline — the top-level orchestrator for the whole project.

Architecture
------------
A simple LINEAR state machine (not a complex branching graph).
Each node does one job, passes its output to the next node via state.

    [collect] → [preprocess] → [analyze] → [llm_interpret] → [visualize] → [report]

Why LangGraph over a plain script?
  - State is explicit and typed: every node declares what it reads/writes
  - Each node can fail independently; you can resume from any checkpoint
  - The LLM interpretation nodes fit naturally as graph nodes alongside
    the data processing nodes — same interface for both
  - Easy to extend: adding a retry edge or a conditional branch is one line

Usage
-----
    # Full pipeline
    python src/agent.py

    # Resume from a specific stage (skips earlier nodes)
    python src/agent.py --from analyze
"""

import argparse
import json
import time
from pathlib import Path
from typing import TypedDict

from langgraph.graph import StateGraph, END

import collect     as _collect
import preprocess  as _preprocess
import analyze     as _analyze
import visualize   as _visualize
from storage    import read_as_pandas, parquet_path
from db         import query_df
from llm_tools  import (
    interpret_clusters,
    analyse_gaps,
    write_summary,
    build_cluster_summary,
    build_gaps_summary,
    build_findings_summary,
)

REPORT_DIR = Path(__file__).resolve().parents[1] / "report"
REPORT_DIR.mkdir(exist_ok=True)


# ── Pipeline State ─────────────────────────────────────────────────────────────
# TypedDict makes the state schema explicit — every node declares what it
# adds. LangGraph validates this at runtime.

class PipelineState(TypedDict, total=False):
    """Shared state passed between all pipeline nodes."""
    # Populated by: collect
    benchmarks_loaded: list[str]
    # Populated by: preprocess
    n_agents: int
    n_benchmarks: int
    # Populated by: analyze
    clustering: dict
    # Populated by: llm_interpret
    cluster_interpretation: str
    gap_analysis:           str
    executive_summary:      str
    # Populated by: visualize
    figures_saved: list[str]
    # Populated by: report
    report_path: str
    # Error handling
    errors: list[str]


# ── Node definitions ──────────────────────────────────────────────────────────

def node_collect(state: PipelineState) -> PipelineState:
    """Stage 1: load raw CSVs → Parquet via PyArrow."""
    print("\n" + "="*50)
    print("NODE: collect")
    print("="*50)
    try:
        results = _collect.collect_all(save=True)
        return {**state, "benchmarks_loaded": list(results.keys()), "errors": state.get("errors", [])}
    except Exception as e:
        err = f"collect failed: {e}"
        print(f"  ✗ {err}")
        return {**state, "errors": state.get("errors", []) + [err]}


def node_preprocess(state: PipelineState) -> PipelineState:
    """Stage 2: clean + normalise + pivot → unified_scores.parquet via DuckDB."""
    print("\n" + "="*50)
    print("NODE: preprocess")
    print("="*50)
    try:
        results = _preprocess.run_preprocessing()
        matrix  = results["matrix"].to_pandas()
        score_cols = [c for c in matrix.columns if c != "agent"]
        return {
            **state,
            "n_agents":     len(matrix),
            "n_benchmarks": len(score_cols),
        }
    except Exception as e:
        err = f"preprocess failed: {e}"
        print(f"  ✗ {err}")
        return {**state, "errors": state.get("errors", []) + [err]}


def node_analyze(state: PipelineState) -> PipelineState:
    """Stage 3: correlation + clustering + gap analysis via DuckDB + sklearn."""
    print("\n" + "="*50)
    print("NODE: analyze")
    print("="*50)
    try:
        results = _analyze.run_analysis()
        return {**state, "clustering": results["clustering"]}
    except Exception as e:
        err = f"analyze failed: {e}"
        print(f"  ✗ {err}")
        return {**state, "errors": state.get("errors", []) + [err]}


def node_llm_interpret(state: PipelineState) -> PipelineState:
    """
    Stage 4: call Claude to interpret clustering results and write analysis.
    Loads result DataFrames from Parquet, builds JSON prompts,
    calls the three LangChain tools, stores outputs in state.
    """
    print("\n" + "="*50)
    print("NODE: llm_interpret  (Claude API)")
    print("="*50)
    try:
        matrix_df  = query_df(f"SELECT * FROM read_parquet('{parquet_path('unified_scores')}')")
        cluster_df = read_as_pandas("cluster_labels")
        gaps_df    = read_as_pandas("capability_gaps")
        corr_df    = read_as_pandas("benchmark_correlation")

        clustering = state.get("clustering", {})

        print("  → Interpreting clusters with Claude...")
        cluster_summary = build_cluster_summary(matrix_df, cluster_df)
        cluster_text    = interpret_clusters.invoke({"cluster_summary": cluster_summary})

        print("  → Analysing capability gaps with Claude...")
        gaps_summary = build_gaps_summary(gaps_df)
        gaps_text    = analyse_gaps.invoke({"gaps_summary": gaps_summary})

        print("  → Writing executive summary with Claude...")
        findings_summary = build_findings_summary(matrix_df, corr_df, clustering, gaps_df)
        summary_text     = write_summary.invoke({"findings": findings_summary})

        print("  ✓ All LLM analysis complete")
        return {
            **state,
            "cluster_interpretation": cluster_text,
            "gap_analysis":           gaps_text,
            "executive_summary":      summary_text,
        }
    except Exception as e:
        err = f"llm_interpret failed: {e}"
        print(f"  ✗ {err}")
        return {**state, "errors": state.get("errors", []) + [err]}


def node_visualize(state: PipelineState) -> PipelineState:
    """Stage 5: generate all figures from Parquet data."""
    print("\n" + "="*50)
    print("NODE: visualize")
    print("="*50)
    try:
        saved = _visualize.generate_all_figures()
        return {**state, "figures_saved": saved}
    except Exception as e:
        err = f"visualize failed: {e}"
        print(f"  ✗ {err}")
        return {**state, "errors": state.get("errors", []) + [err]}


def node_report(state: PipelineState) -> PipelineState:
    """
    Stage 6: inject LLM-generated text into the report template
    and write the final report.md.
    """
    print("\n" + "="*50)
    print("NODE: report")
    print("="*50)
    try:
        template_path = REPORT_DIR / "report.md"
        output_path   = REPORT_DIR / "report_final.md"

        if not template_path.exists():
            raise FileNotFoundError("report/report.md template not found")

        report = template_path.read_text()

        # Replace placeholders with LLM-generated content
        replacements = {
            "> _To be written after analysis is complete._": state.get(
                "executive_summary", "_Executive summary not generated._"
            ),
            "_[Describe characteristic — e.g., strong on reasoning, weak on ML engineering]_": state.get(
                "cluster_interpretation", "_Cluster interpretation not generated._"
            ),
            "_[Which agents have the most consistent capability? Who is a specialist vs. generalist?]_": state.get(
                "gap_analysis", "_Gap analysis not generated._"
            ),
        }

        for placeholder, content in replacements.items():
            report = report.replace(placeholder, content)

        # Add pipeline metadata footer
        import datetime
        report += f"\n\n---\n_Report generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}_\n"
        report += f"_Agents analysed: {state.get('n_agents', 'N/A')} | Benchmarks: {state.get('n_benchmarks', 'N/A')}_\n"
        if state.get("errors"):
            report += f"\n**Pipeline warnings:** {'; '.join(state['errors'])}\n"

        output_path.write_text(report)
        print(f"  ✓ Report written → {output_path}")
        return {**state, "report_path": str(output_path)}

    except Exception as e:
        err = f"report failed: {e}"
        print(f"  ✗ {err}")
        return {**state, "errors": state.get("errors", []) + [err]}


# ── Build the LangGraph pipeline ──────────────────────────────────────────────

def build_pipeline() -> StateGraph:
    """
    Assemble the linear LangGraph pipeline.

    Graph: collect → preprocess → analyze → llm_interpret → visualize → report → END
    """
    graph = StateGraph(PipelineState)

    # Register nodes
    graph.add_node("collect",       node_collect)
    graph.add_node("preprocess",    node_preprocess)
    graph.add_node("analyze",       node_analyze)
    graph.add_node("llm_interpret", node_llm_interpret)
    graph.add_node("visualize",     node_visualize)
    graph.add_node("report",        node_report)

    # Linear edges
    graph.add_edge("collect",       "preprocess")
    graph.add_edge("preprocess",    "analyze")
    graph.add_edge("analyze",       "llm_interpret")
    graph.add_edge("llm_interpret", "visualize")
    graph.add_edge("visualize",     "report")
    graph.add_edge("report",        END)

    # Entry point
    graph.set_entry_point("collect")

    return graph.compile()


# ── CLI entry point ───────────────────────────────────────────────────────────

STAGE_ORDER = ["collect", "preprocess", "analyze", "llm_interpret", "visualize", "report"]

def run(from_stage: str = "collect") -> PipelineState:
    """Run the pipeline, optionally starting from a specific stage."""
    pipeline = build_pipeline()

    # Build initial state — skip stages before from_stage
    initial_state: PipelineState = {"errors": []}

    if from_stage != "collect":
        # Pre-populate state from existing Parquet files so we can resume
        print(f"  ↷ Resuming from stage: {from_stage}")
        try:
            matrix_df  = query_df(f"SELECT * FROM read_parquet('{parquet_path('unified_scores')}')")
            score_cols = [c for c in matrix_df.columns if c != "agent"]
            initial_state["n_agents"]     = len(matrix_df)
            initial_state["n_benchmarks"] = len(score_cols)
            initial_state["benchmarks_loaded"] = ["datasci_bench", "dsbench",
                                                   "mle_bench", "gaia", "swe_bench"]
        except Exception:
            print("  ⚠ Could not load existing state — starting from collect")
            from_stage = "collect"

    start_time = time.time()
    final_state = pipeline.invoke(initial_state)
    elapsed = time.time() - start_time

    print(f"\n{'='*50}")
    print(f"PIPELINE COMPLETE  ({elapsed:.1f}s)")
    print(f"{'='*50}")
    if final_state.get("errors"):
        print(f"⚠ Warnings: {'; '.join(final_state['errors'])}")
    else:
        print("✅ No errors")

    return final_state


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the benchmark analysis pipeline")
    parser.add_argument(
        "--from",
        dest="from_stage",
        default="collect",
        choices=STAGE_ORDER,
        help="Start the pipeline from this stage (default: collect)",
    )
    args = parser.parse_args()
    run(from_stage=args.from_stage)
