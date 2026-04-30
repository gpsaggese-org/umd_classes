"""
End-to-end pipeline runner for the AI-Powered Technical Debt project.

Runs all eight stages against a Java repository and prints a summary
showing what was found, refactored, and validated.

Two modes:
    Live: run Stage 6 with a local model (0.5B by default). Best for
        machines without GPU access; produces weak refactorings but
        the full pipeline executes end-to-end.
    Replay: load pre-computed Stage 6 records from JSON. Used when the
        records were generated on a GPU machine (Nexus). Other stages
        still run locally; only the agent inference is replayed.

Examples:
    Live mode on commons-lang3 with 0.5B:
        python run_pipeline.py --repo /path/to/commons-lang --top 5

    Replay mode with 3B records produced on Nexus:
        python run_pipeline.py --repo /path/to/commons-lang \\
          --records production/data/refactor_records_3b.json --top 10

    Live mode with tests too (slow):
        python run_pipeline.py --repo /path/to/commons-lang \\
          --top 3 --run-tests
"""

import argparse
import logging
import os
import sys
from typing import Optional

# Make production package importable.
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
))

from production.stages.ingest import ingest_repository
from production.stages.analyze import analyze_repository
from production.stages.classify import aggregate_to_readme_view, summarize_view
from production.stages.predict import predict_fault_probability
from production.stages.prioritize import (
    prioritize_issues, top_n_issues, compute_pareto_front,
)
from production.stages.refactor import (
    refactor_top_issues,
    load_refactor_records,
)
from production.stages.validate import validate_refactor_records
from production.stages.feedback import (
    get_summary_metrics, get_success_rate_by_rule,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
logger = logging.getLogger("run_pipeline")


def main():
    parser = argparse.ArgumentParser(
        description="Run the full technical-debt pipeline end-to-end."
    )
    parser.add_argument(
        "--repo", required=True,
        help="Repository URL or local path.",
    )
    parser.add_argument(
        "--top", type=int, default=10,
        help="Number of top issues to refactor (default: 10).",
    )
    parser.add_argument(
        "--max-per-file", type=int, default=1,
        help="Max issues per file in selection (default: 1).",
    )
    parser.add_argument(
        "--records", default=None,
        help="Path to pre-computed Stage 6 records JSON. "
             "If set, replay mode; otherwise live mode.",
    )
    parser.add_argument(
        "--model", default="Qwen/Qwen2.5-Coder-0.5B-Instruct",
        help="Model name for live Stage 6 (default: 0.5B).",
    )
    parser.add_argument(
        "--run-tests", action="store_true",
        help="Run mvn test in Stage 7 (slower, catches behavioral bugs).",
    )
    parser.add_argument(
        "--save-records", default=None,
        help="If in live mode, save the Stage 6 records to this path.",
    )
    parser.add_argument(
        "--repo-name", default=None,
        help="Short name for the repo (used in feedback logging).",
    )
    args = parser.parse_args()

    print()
    print("=" * 70)
    print("Technical Debt Pipeline")
    print("=" * 70)
    print(f"Repository: {args.repo}")
    print(f"Mode: {'replay' if args.records else 'live'}")
    print(f"Top issues to refactor: {args.top}")
    print()

    # Stage 1: Ingest.
    print("--- Stage 1: Ingest ---")
    ingest_result = ingest_repository(args.repo)
    print(f"  Repo root: {ingest_result['repo_root']}")
    print(f"  Java source root: {ingest_result['java_source_root']}")
    repo_name = args.repo_name or ingest_result.get("repo_name", "unknown")
    print()

    # Stage 2: Analyze.
    print("--- Stage 2: Analyze ---")
    issues = analyze_repository(ingest_result["java_source_root"])
    print(f"  Found {len(issues)} issues")
    print()

    # Stage 3: Classify.
    print("--- Stage 3: Classify ---")
    view = aggregate_to_readme_view(issues)
    print(summarize_view(view))
    print()

    # Stage 4: Predict.
    print("--- Stage 4: Predict ---")
    predict_fault_probability(
        issues,
        ingest_result["repo_root"],
        ingest_result["java_source_root"],
    )
    probs = [
        i["fault_probability"] for i in issues
        if i.get("fault_probability") is not None
    ]
    if probs:
        print(f"  Probability range: {min(probs):.3f} to {max(probs):.3f}")
        print(f"  Mean: {sum(probs)/len(probs):.3f}")
    print()

    # Stage 5: Prioritize.
    print("--- Stage 5: Prioritize ---")
    prioritize_issues(issues)
    pareto = compute_pareto_front(issues)
    print(f"  Ranked {len(issues)} issues")
    print(f"  Pareto front: {len(pareto)} issues")
    print()

    # Stage 6: Refactor.
    print("--- Stage 6: Refactor ---")
    if args.records:
        print(f"  Replay mode: loading from {args.records}")
        envelope = load_refactor_records(args.records)
        records = envelope["records"]
        print(f"  Loaded {len(records)} records "
              f"(model={envelope.get('model_name', 'unknown')})")
    else:
        print(f"  Live mode: running {args.model}")
        records = refactor_top_issues(
            ranked_issues=issues,
            repo_root=ingest_result["repo_root"],
            n=args.top,
            max_per_file=args.max_per_file,
            strategies=("zero_shot",),
            model_name=args.model,
            log_to_feedback=True,
            repo_name=repo_name,
            save_to=args.save_records,
        )
        print(f"  Produced {len(records)} records")

    n_with_best = sum(1 for r in records if r["best_strategy"] is not None)
    print(f"  {n_with_best}/{len(records)} have a best strategy")
    print()

    # Stage 7: Validate.
    print("--- Stage 7: Validate ---")
    target = "test" if args.run_tests else "compile"
    print(f"  Target: {target}")
    validations = validate_refactor_records(
        records=records,
        repo_root=ingest_result["repo_root"],
        java_source_root=ingest_result["java_source_root"],
        repo_name=repo_name,
        run_tests=args.run_tests,
        timeout_seconds=300,
        log_to_feedback=True,
    )
    n_succeeded = sum(1 for v in validations if v["succeeded"])
    n_failed = sum(
        1 for v in validations if not v["succeeded"] and not v["skipped"]
    )
    n_skipped = sum(1 for v in validations if v["skipped"])
    print(f"  Passed: {n_succeeded}/{len(validations)}")
    print(f"  Failed: {n_failed}/{len(validations)}")
    print(f"  Skipped: {n_skipped}/{len(validations)}")
    print()

    # Stage 8: Feedback summary.
    print("--- Stage 8: Feedback Summary ---")
    metrics = get_summary_metrics()
    print(f"  Total events: {metrics['total_events']}")
    print(f"  Events by type: {metrics['events_by_type']}")
    print(f"  Unique issues: {metrics['unique_issues']}")
    print(f"  Unique repos: {metrics['unique_repos']}")
    print()

    # Final per-record table.
    print("=" * 70)
    print("Per-record results")
    print("=" * 70)
    print(f"{'#':>2} {'Status':<6} {'Conf':<6} {'Rule':<40} {'Time':>6}")
    for i, (record, validation) in enumerate(
        zip(records, validations), start=1
    ):
        rule = record["issue"].get("rule", "<unknown>")[:40]
        if validation["succeeded"]:
            status = "PASS"
        elif validation["skipped"]:
            status = "SKIP"
        else:
            status = "FAIL"
        best = record.get("best_strategy")
        if best:
            strategy = next(
                (s for s in record["strategies"]
                 if s["strategy_name"] == best),
                None,
            )
            conf = strategy["confidence"]["level"] if strategy else "-"
        else:
            conf = "-"
        elapsed = validation.get("elapsed_s", 0.0)
        print(f"{i:>2} {status:<6} {conf:<6} {rule:<40} {elapsed:>5.1f}s")
    print()

    print("Done.")


if __name__ == "__main__":
    main()