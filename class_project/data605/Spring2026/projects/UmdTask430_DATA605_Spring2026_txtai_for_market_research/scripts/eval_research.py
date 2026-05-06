#!/usr/bin/env python3
"""
Eval harness for the agentic research pipeline.

Runs a fixed set of benchmark queries, repeats each ``--repeats`` times to
average out noise, then reports:

  - p50 / p95 / p99 total latency
  - Per-step latency breakdown (route / retrieve / synthesize)
  - Routing accuracy (extracted ticker matches expected; selected agents
    match expected set)
  - Retrieval health (% queries returning >= 1 chunk, mean top-1 score)
  - Answer length distribution

Usage:
    python -m scripts.eval_research                     # full benchmark
    python -m scripts.eval_research --repeats 5         # 5 runs/query
    python -m scripts.eval_research --json out.json     # also dump JSON
"""

import argparse
import json
import logging
import statistics
import sys
import time
from pathlib import Path

from dotenv import load_dotenv

# Make ``app`` importable when run from the repo root.
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app.agents.research_agent import run_research_sync

logging.basicConfig(level=logging.WARNING, format="%(message)s")
_LOG = logging.getLogger(__name__)

# #############################################################################
# Benchmark set
# #############################################################################

# (query, expected_ticker, expected_agents_subset)
# ``expected_agents_subset`` is a set of agents the router *must* fire; extra
# agents are OK (e.g. if the router defaults to both, that's fine when only
# {"sec"} was expected).
_BENCHMARK = [
    (
        "What does Apple disclose as risk factors in its 10-K?",
        "AAPL", {"sec"},
    ),
    (
        "What is the recent NVDA news sentiment?",
        "NVDA", {"news"},
    ),
    (
        "How does JPMorgan describe regulatory risk?",
        "JPM", {"sec"},
    ),
    (
        "What are analysts saying about Tesla?",
        "TSLA", {"news"},
    ),
    (
        "Summarize Microsoft 8-K disclosures",
        "MSFT", {"sec"},
    ),
    (
        "Tell me about NVIDIA",
        "NVDA", {"sec", "news"},
    ),
    (
        "Recent news around $AMD",
        "AMD", {"news"},
    ),
    (
        "What does Goldman Sachs say in its filings about market risk?",
        "GS", {"sec"},
    ),
    (
        "Wells Fargo earnings outlook",
        "WFC", {"news"},
    ),
    (
        "Pfizer 10-K risk factors",
        "PFE", {"sec"},
    ),
]


# #############################################################################
# Stat helpers
# #############################################################################


def _percentile(values: list[float], p: float) -> float:
    """
    Compute a percentile without numpy.

    :param values: sample values
    :param p: percentile in [0, 100]
    :return: percentile value (0.0 if the input is empty)
    """
    if not values:
        return 0.0
    s = sorted(values)
    k = (len(s) - 1) * (p / 100.0)
    lo = int(k)
    hi = min(lo + 1, len(s) - 1)
    frac = k - lo
    return s[lo] * (1 - frac) + s[hi] * frac


def _summary(label: str, values: list[float], unit: str = "ms") -> str:
    """
    Format a one-line summary of a numeric distribution.

    :param label: column label printed at the start of the line
    :param values: sample values
    :param unit: unit suffix (e.g. "ms", "chunks")
    :return: tab-aligned summary line
    """
    if not values:
        return f"{label:<24} (no data)"
    mean = statistics.fmean(values)
    p50 = _percentile(values, 50)
    p95 = _percentile(values, 95)
    p99 = _percentile(values, 99)
    return (
        f"{label:<24} mean={mean:7.1f}{unit}  "
        f"p50={p50:7.1f}{unit}  "
        f"p95={p95:7.1f}{unit}  "
        f"p99={p99:7.1f}{unit}  "
        f"n={len(values)}"
    )


# #############################################################################
# Main
# #############################################################################


def _parse_args() -> argparse.Namespace:
    """
    Parse CLI args.
    """
    parser = argparse.ArgumentParser(
        description="Eval the agentic research pipeline."
    )
    parser.add_argument(
        "--repeats",
        type=int,
        default=3,
        help="Number of runs per query (default: 3)",
    )
    parser.add_argument(
        "--json",
        type=str,
        default=None,
        help="Optional path to dump the full per-run JSON",
    )
    parser.add_argument(
        "--warmup",
        action="store_true",
        help="Run one extra warmup pass before timing",
    )
    return parser.parse_args()


def _main() -> int:
    """
    Run the benchmark and print the report.
    """
    load_dotenv()
    args = _parse_args()
    if args.warmup:
        print("Warming up…")
        run_research_sync(_BENCHMARK[0][0])
    print(
        f"Running {len(_BENCHMARK)} queries x {args.repeats} repeats = "
        f"{len(_BENCHMARK) * args.repeats} total runs"
    )
    print("─" * 80)
    runs: list[dict] = []
    bench_t0 = time.perf_counter()
    for query, expected_ticker, expected_agents in _BENCHMARK:
        print(f"\n>>> {query}")
        for r in range(args.repeats):
            t0 = time.perf_counter()
            result = run_research_sync(query)
            wall_ms = (time.perf_counter() - t0) * 1000.0
            timings = result.get("timings", {})
            route = result.get("route", {})
            actual_ticker = route.get("ticker")
            actual_agents = set(route.get("agents", []))
            ticker_ok = actual_ticker == expected_ticker
            agents_ok = expected_agents.issubset(actual_agents)
            top_score = (
                result["sources"][0]["score"] if result.get("sources") else 0.0
            )
            runs.append({
                "query": query,
                "repeat": r,
                "wall_ms": wall_ms,
                "timings": timings,
                "expected_ticker": expected_ticker,
                "actual_ticker": actual_ticker,
                "ticker_ok": ticker_ok,
                "expected_agents": sorted(expected_agents),
                "actual_agents": sorted(actual_agents),
                "agents_ok": agents_ok,
                "chunk_count": result.get("chunk_count", 0),
                "top_score": top_score,
                "answer_len": len(result.get("answer", "")),
                "used_llm": result.get("used_llm", False),
            })
            ok = "✓" if (ticker_ok and agents_ok) else "✗"
            print(
                f"  [{r + 1}/{args.repeats}] {ok} ticker={actual_ticker} "
                f"agents={sorted(actual_agents)} chunks={result.get('chunk_count', 0)} "
                f"top={top_score:.3f} wall={wall_ms:.0f}ms"
            )
    bench_total_s = time.perf_counter() - bench_t0
    print("\n" + "═" * 80)
    print(f"REPORT  ({len(runs)} runs in {bench_total_s:.1f}s)")
    print("═" * 80)
    # Latency.
    print("\n— Latency —")
    print(_summary("total wall", [r["wall_ms"] for r in runs]))
    for key in ["route_ms", "retrieve_sec_ms", "retrieve_news_ms", "synthesize_ms"]:
        vals = [r["timings"][key] for r in runs if key in r["timings"]]
        print(_summary(key, vals))
    # Routing accuracy.
    print("\n— Routing accuracy —")
    ticker_acc = sum(r["ticker_ok"] for r in runs) / len(runs)
    agents_acc = sum(r["agents_ok"] for r in runs) / len(runs)
    both_acc = sum(r["ticker_ok"] and r["agents_ok"] for r in runs) / len(runs)
    print(f"  ticker correct        {ticker_acc:6.1%}")
    print(f"  agents superset       {agents_acc:6.1%}")
    print(f"  both correct          {both_acc:6.1%}")
    misses = [r for r in runs if not (r["ticker_ok"] and r["agents_ok"])]
    if misses:
        print("  failures:")
        seen = set()
        for r in misses:
            key = (r["query"], r["actual_ticker"], tuple(r["actual_agents"]))
            if key in seen:
                continue
            seen.add(key)
            print(
                f"    - {r['query'][:55]:<55} "
                f"got ticker={r['actual_ticker']} agents={r['actual_agents']}"
            )
    # Retrieval.
    print("\n— Retrieval —")
    nonempty = [r for r in runs if r["chunk_count"] > 0]
    print(f"  queries w/ chunks     {len(nonempty) / len(runs):6.1%}")
    print(_summary("chunks/query", [r["chunk_count"] for r in runs], unit=" "))
    print(_summary("top-1 score", [r["top_score"] for r in nonempty], unit=""))
    # Answer.
    print("\n— Answer —")
    print(_summary("answer length (chars)", [r["answer_len"] for r in runs], unit=""))
    llm_pct = sum(r["used_llm"] for r in runs) / len(runs)
    print(f"  used LLM synthesis    {llm_pct:6.1%}")
    print()
    if args.json:
        Path(args.json).write_text(json.dumps(runs, indent=2))
        print(f"Wrote per-run JSON to {args.json}")
    return 0


if __name__ == "__main__":
    sys.exit(_main())
