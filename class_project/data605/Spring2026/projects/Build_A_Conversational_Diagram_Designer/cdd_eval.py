# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
# ---

# %% [markdown]
# # CDD Evaluation Harness
#
# Two layers of evaluation:
#
# 1. **Per-output metrics:** for each generated diagram, compute lightweight
#    automatic metrics (syntax validity, node count, edge count, has labels,
#    has styles, render success). These are cheap and don't require an LLM judge.
#
# 2. **Vision-on vs vision-off study:** the centerpiece. For each prompt, run
#    the full pipeline twice: once with the vision-feedback loop disabled
#    (single-shot), once with it enabled (up to 3 iterations). Compare metrics
#    and optionally use an LLM-as-judge to score quality.
#
# The benchmark is intentionally small: three prompts, one per supported
# format. This keeps the run inside Gemini's free-tier rate limit (5
# requests per minute) and finishes in roughly 6 to 8 minutes end to end.
# Larger sweeps are easy to add by passing a custom `test_cases` list.

# %%
import json
import re
import time
from dataclasses import dataclass, field
from typing import Optional

import cdd_config as config
import cdd_llm as llm
import cdd_renderer as renderer
from cdd_orchestrator import CDDOrchestrator


# %% [markdown]
# ## Throttle configuration
#
# Free-tier Gemini allows 5 requests/minute. With vision feedback enabled,
# each case can fire up to 3 generations + 3 vision critiques = 6 calls.
# A 20-second wait between cases keeps us well within budget on free tier.
# Set throttle_seconds=0 explicitly when calling the runner if you're on
# a paid tier.

# %%
THROTTLE_SECONDS = 20


# %% [markdown]
# ## Result schemas

# %%
@dataclass
class EvalResult:
    """Single-prompt evaluation result."""
    prompt: str
    format: str
    condition: str  # "vision_off" or "vision_on"
    diagram_source: str
    syntax_valid: bool
    node_count: int
    edge_count: int
    has_labels: bool
    has_styles: bool
    render_success: bool
    iterations_used: int = 1
    llm_judge_score: Optional[float] = None
    llm_judge_feedback: Optional[str] = None
    error: Optional[str] = None  # set when the case threw

    @property
    def dot_source(self) -> str:
        return self.diagram_source

    def to_dict(self) -> dict:
        return {
            "prompt": self.prompt,
            "format": self.format,
            "condition": self.condition,
            "syntax_valid": self.syntax_valid,
            "node_count": self.node_count,
            "edge_count": self.edge_count,
            "has_labels": self.has_labels,
            "has_styles": self.has_styles,
            "render_success": self.render_success,
            "iterations_used": self.iterations_used,
            "llm_judge_score": self.llm_judge_score,
            "llm_judge_feedback": self.llm_judge_feedback,
            "error": self.error,
        }


# %% [markdown]
# ## Lightweight automatic metrics

# %%
def count_nodes(source: str, format: str = "graphviz") -> int:
    """Heuristic node count for the given format."""
    if format == "graphviz":
        return _count_nodes_dot(source)
    if format == "mermaid":
        return _count_nodes_mermaid(source)
    if format == "plantuml":
        return _count_nodes_plantuml(source)
    return 0


def _count_nodes_dot(source: str) -> int:
    count = 0
    for line in source.split("\n"):
        line = line.strip()
        if not line or line.startswith(("//", "#", "/*")):
            continue
        if "->" in line or "--" in line:
            continue
        if line.startswith(("digraph", "graph", "subgraph", "}", "{")):
            continue
        if "[" in line or re.match(r"^\w+\s*;?\s*$", line):
            count += 1
    return count


def _count_nodes_mermaid(source: str) -> int:
    tokens = re.findall(r"\b([A-Za-z_]\w*)\s*[\[\(\{]?", source)
    reserved = {
        "graph", "flowchart", "TD", "TB", "BT", "LR", "RL",
        "sequenceDiagram", "classDiagram", "stateDiagram",
        "erDiagram", "gantt", "pie", "journey", "mindmap", "timeline",
        "participant", "actor", "class", "state", "note", "loop", "alt", "else",
        "end", "rgb", "rgba",
    }
    return len({t for t in tokens if t not in reserved})


def _count_nodes_plantuml(source: str) -> int:
    pattern = r"\b(?:actor|participant|class|state|component|node|database|interface|entity)\b\s+(\w+)"
    matches = re.findall(pattern, source, re.IGNORECASE)
    if matches:
        return len(set(matches))
    arrows = re.findall(r"\b(\w+)\s*-+>", source)
    targets = re.findall(r"-+>\s*(\w+)", source)
    return len(set(arrows + targets))


def count_edges(source: str, format: str = "graphviz") -> int:
    if format == "graphviz":
        return len(re.findall(r"(->|--)", source))
    if format == "mermaid":
        return len(re.findall(r"(-->|---|-\.->|==>)", source))
    if format == "plantuml":
        return len(re.findall(r"(-+>|<-+|\.\.>|\.\.\.)", source))
    return 0


def has_labels(source: str, format: str = "graphviz") -> bool:
    if format == "graphviz":
        return bool(re.search(r"label\s*=", source))
    if format == "mermaid":
        return bool(re.search(r"[\[\(\{]\s*[A-Za-z]", source))
    if format == "plantuml":
        return ':"' in source or '"' in source
    return False


def has_styles(source: str, format: str = "graphviz") -> bool:
    if format == "graphviz":
        attrs = ["color", "fillcolor", "shape", "style", "fontcolor"]
        return any(a in source.lower() for a in attrs)
    if format == "mermaid":
        return bool(re.search(r"(classDef|style\s+\w+|stroke|fill)", source))
    if format == "plantuml":
        return "skinparam" in source.lower() or "<<" in source
    return False


# %% [markdown]
# ## Single-prompt evaluation

# %%
def evaluate_single(
    prompt: str,
    diagram_source: str,
    format: str = "graphviz",
    condition: str = "vision_off",
    iterations_used: int = 1,
    use_llm_judge: bool = False,
) -> EvalResult:
    """Score a single generated diagram on automatic metrics."""
    is_valid, _ = renderer.validate(diagram_source, format)
    render_ok = False
    if is_valid:
        try:
            renderer.render(diagram_source, format)
            render_ok = True
        except Exception:
            render_ok = False

    result = EvalResult(
        prompt=prompt,
        format=format,
        condition=condition,
        diagram_source=diagram_source,
        syntax_valid=is_valid,
        node_count=count_nodes(diagram_source, format),
        edge_count=count_edges(diagram_source, format),
        has_labels=has_labels(diagram_source, format),
        has_styles=has_styles(diagram_source, format),
        render_success=render_ok,
        iterations_used=iterations_used,
    )

    if use_llm_judge and is_valid:
        score, feedback = _llm_judge(prompt, diagram_source, format)
        result.llm_judge_score = score
        result.llm_judge_feedback = feedback
    return result


# %%
def _llm_judge(prompt: str, diagram_source: str, format: str) -> tuple:
    """LLM-as-judge: ask the model to rate the diagram on a 1-5 scale."""
    judge_prompt = f"""You are evaluating a generated {format} diagram.

Original request: "{prompt}"

Generated code:
```
{diagram_source}
```

Score on completeness, accuracy, readability, and style.
Respond with ONLY a JSON object: {{"score": <float 1-5>, "feedback": "<brief reason>"}}"""
    try:
        raw = llm.generate(judge_prompt, format=format)
        match = re.search(r"\{.*\}", raw, re.DOTALL)
        if match:
            data = json.loads(match.group())
            return float(data.get("score", 0.0)), data.get("feedback", "")
    except Exception:
        pass
    return None, None


# %% [markdown]
# ## Benchmark prompt set
#
# Three prompts, one per supported format. Mid-complexity targets that
# exercise the orchestrator across all rendering paths (local Graphviz,
# Kroki for Mermaid, PlantUML server for PlantUML) without burning
# Gemini free-tier quota.
#
# To run a larger sweep, pass a custom `test_cases` list to the runners:
#
#     extra = [{"prompt": "...", "format": "graphviz"}, ...]
#     evaluation.run_eval_suite(test_cases=EVAL_TEST_CASES + extra)

# %%
EVAL_TEST_CASES = [
    {
        "prompt": "Draw a simple flowchart for making coffee: start, boil water, add grounds, pour water, serve",
        "format": "graphviz",
        "expected_min_nodes": 5,
        "expected_min_edges": 4,
    },
    {
        "prompt": "Create a flowchart for a user signup flow: form, validate email, save to database, send welcome email, redirect to dashboard",
        "format": "mermaid",
        "expected_min_nodes": 5,
        "expected_min_edges": 4,
    },
    {
        "prompt": "Sequence diagram: A user logs into a web app. Client sends credentials to server, server queries the database, returns a session token.",
        "format": "plantuml",
        "expected_min_nodes": 3,
        "expected_min_edges": 4,
    },
]


# %% [markdown]
# ## Run the eval suite
#
# Two entry points:
#   - `run_eval_suite`: runs all benchmark prompts in a single condition
#   - `run_vision_comparison`: runs each prompt in BOTH conditions
#
# Both throttle between cases to avoid free-tier rate limits.

# %%
def run_eval_suite(
    provider: Optional[str] = None,
    use_llm_judge: bool = False,
    condition: str = "vision_off",
    test_cases: Optional[list] = None,
    throttle_seconds: Optional[int] = None,
    verbose: bool = True,
) -> list:
    """Run all benchmark prompts in one condition.

    Throttles between cases to respect free-tier rate limits.
    Pass throttle_seconds=0 if you're on a paid tier.
    """
    cases = test_cases if test_cases is not None else EVAL_TEST_CASES
    delay = THROTTLE_SECONDS if throttle_seconds is None else throttle_seconds
    results = []

    for i, tc in enumerate(cases):
        fmt = tc.get("format", "graphviz")
        if verbose:
            print(f"  [{i+1}/{len(cases)}] {fmt} | {tc['prompt'][:60]}...")
        try:
            orch = CDDOrchestrator(
                provider=provider,
                format=fmt,
                vision_feedback=(condition == "vision_on"),
            )
            diagram_source, _ = orch.process_message(tc["prompt"])
            iterations = orch.state.revision_count
            result = evaluate_single(
                tc["prompt"], diagram_source, fmt, condition,
                iterations_used=iterations,
                use_llm_judge=use_llm_judge,
            )
            results.append(result)
            if verbose:
                ok = "OK" if result.render_success else "FAIL"
                print(f"      {ok} syntax={result.syntax_valid} render={result.render_success} "
                      f"nodes={result.node_count} edges={result.edge_count}")
        except Exception as e:
            err_msg = str(e)[:200]
            if verbose:
                print(f"      FAIL ERROR: {err_msg}")
            results.append(EvalResult(
                prompt=tc["prompt"], format=fmt, condition=condition,
                diagram_source="", syntax_valid=False,
                node_count=0, edge_count=0, has_labels=False,
                has_styles=False, render_success=False,
                error=err_msg,
            ))

        # Throttle between cases (skip after the last one)
        if delay > 0 and i < len(cases) - 1:
            if verbose:
                print(f"      [throttle] waiting {delay}s before next case...")
            time.sleep(delay)

    return results


def run_vision_comparison(
    provider: Optional[str] = None,
    use_llm_judge: bool = False,
    test_cases: Optional[list] = None,
    throttle_seconds: Optional[int] = None,
) -> dict:
    """Run each benchmark prompt in BOTH vision-off and vision-on conditions."""
    print("=" * 60)
    print("Running vision-OFF baseline...")
    print("=" * 60)
    off = run_eval_suite(
        provider=provider, use_llm_judge=use_llm_judge,
        condition="vision_off", test_cases=test_cases,
        throttle_seconds=throttle_seconds,
    )
    print()
    print("=" * 60)
    print("Running vision-ON...")
    print("=" * 60)
    on = run_eval_suite(
        provider=provider, use_llm_judge=use_llm_judge,
        condition="vision_on", test_cases=test_cases,
        throttle_seconds=throttle_seconds,
    )
    return {"vision_off": off, "vision_on": on}


# %% [markdown]
# ## Summarization

# %%
def summarize_eval(results: list) -> dict:
    n = len(results)
    if n == 0:
        return {}
    judge_scores = [r.llm_judge_score for r in results if r.llm_judge_score is not None]
    return {
        "total_cases": n,
        "syntax_valid_pct": sum(r.syntax_valid for r in results) / n * 100,
        "render_success_pct": sum(r.render_success for r in results) / n * 100,
        "avg_nodes": sum(r.node_count for r in results) / n,
        "avg_edges": sum(r.edge_count for r in results) / n,
        "has_labels_pct": sum(r.has_labels for r in results) / n * 100,
        "has_styles_pct": sum(r.has_styles for r in results) / n * 100,
        "avg_iterations": sum(r.iterations_used for r in results) / n,
        "avg_llm_judge_score": (
            sum(judge_scores) / len(judge_scores) if judge_scores else None
        ),
    }


def summarize_comparison(comparison: dict) -> dict:
    return {
        "vision_off": summarize_eval(comparison["vision_off"]),
        "vision_on": summarize_eval(comparison["vision_on"]),
    }
