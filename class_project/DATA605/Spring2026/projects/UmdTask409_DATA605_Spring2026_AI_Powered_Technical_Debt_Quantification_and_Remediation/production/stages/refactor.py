"""
Stage 6: Refactor the top-priority issues using the Qwen-Coder agent.

For each of the top N issues from Stage 5, this stage:
  1. Locates the smallest enclosing method/class around the issue line.
  2. Extracts the method source by reading from the file.
  3. Builds an issue-aware prompt naming the rule and description.
  4. Runs the agent under one or more strategies (zero_shot, retrieval).
  5. Validates each output (Java syntax, signature preserved).
  6. Produces a unified diff.
  7. Picks the best strategy by confidence score.
  8. Logs the refactoring event to Stage 8.

Each refactoring record contains the original method, the candidate
refactorings (one per strategy), confidence scores, and diffs. The
caller decides which refactoring to act on; Stage 6 does not write
back to source files.

Stage 6 uses Qwen-Coder-0.5B-Instruct (validated in the Q1 spike).
The 3B model produces richer outputs but is too slow on CPU.
Documented in LIMITATIONS_AND_FUTURE_IMPROVEMENTS.md.

Usage:
    from production.stages.refactor import refactor_top_issues
    records = refactor_top_issues(
        ranked_issues=stage_5_issues,
        repo_root="/path/to/repo",
        n=5,
    )
"""
import difflib
import logging
import re
import time
from typing import Optional
import json
import os

import javalang

# Make MVP utils importable.
import ai_technical_debt_utils as utils

from production.stages.feedback import log_event

logger = logging.getLogger(__name__)


DEFAULT_MODEL = utils.AGENT_DEFAULT_MODEL  # Qwen2.5-Coder-0.5B-Instruct
DEFAULT_MAX_NEW_TOKENS = utils.AGENT_DEFAULT_MAX_NEW_TOKENS
DEFAULT_SEED = utils.AGENT_DEFAULT_SEED
DEFAULT_N_RETRIEVAL = utils.AGENT_DEFAULT_N_RETRIEVAL_EXAMPLES

DEFAULT_STRATEGIES = ("zero_shot", "few_shot_retrieval")
DEFAULT_RETRIEVAL_CACHE = "/data/retrieval_cache"
# Threshold matches the 0.5B model's realistic output budget. The 3B model
# (used for pre-computed Nexus outputs) handles longer methods cleanly,
# but at the cost of significantly longer inference time.
MAX_METHOD_LINES_FOR_REFACTORING = 40

# PMD rules that the method-only agent cannot safely refactor. These are
# rules whose fix requires changes outside the local method:
#   - Renames need to update every callsite (the agent sees only one method)
#   - Class-level structural changes need to modify the class declaration
#   - Constructor/instantiation changes affect callers
# Issues matching these rules are skipped at selection time. Documented
# in LIMITATIONS_AND_FUTURE_IMPROVEMENTS.md.
UNREFACTORABLE_RULES = {
    "MethodNamingConventions",
    "TypeParameterNamingConventions",
    "LocalVariableNamingConventions",
    "ClassWithOnlyPrivateConstructorsShouldBeFinal",
    "UseUtilityClass",
    "UnnecessaryConstructor",
    "UncommentedEmptyConstructor",
    "FieldNamingConventions",
}


# ---------------------------------------------------------------------------
# Public entry point.
# ---------------------------------------------------------------------------


def refactor_top_issues(
    ranked_issues: list,
    repo_root: str,
    n: int = 5,
    max_per_file: int = 1,
    strategies: tuple = DEFAULT_STRATEGIES,
    model_name: str = DEFAULT_MODEL,
    log_to_feedback: bool = True,
    repo_name: Optional[str] = None,
    save_to: Optional[str] = None,
) -> list:
    """Refactor the top N issues and return refactoring records.

    Args:
        ranked_issues: output of Stage 5's prioritize_issues.
        repo_root: absolute path to the git repo (for resolving file paths).
        n: maximum number of issues to refactor.
        max_per_file: max issues to refactor per file (deduplication).
        strategies: tuple of strategy names to run per issue. Each must
            be one of "zero_shot" or "few_shot_retrieval".
        model_name: Hugging Face model ID. Defaults to MVP's 0.5B model.
        log_to_feedback: if True, write a 'refactored' event for each
            attempted issue.
        repo_name: short repo name for feedback logging.

    Returns:
        list of refactoring records, one per issue. Each record has the
        keys documented in the module docstring.
    """
    if not ranked_issues:
        return []

    selected = []
    file_counts = {}
    skipped_too_large = 0
    skipped_unparseable = 0
    skipped_unrefactorable_rule = 0
    for issue in ranked_issues:
        if len(selected) >= n:
            break

        # Skip rules the method-only agent cannot safely fix.
        if issue.get("rule") in UNREFACTORABLE_RULES:
            skipped_unrefactorable_rule += 1
            continue

        file_path = issue.get("file_path")
        if max_per_file is not None and file_path is not None:
            count = file_counts.get(file_path, 0)
            if count >= max_per_file:
                continue

        extraction = _is_refactorable(issue)
        if extraction is None:
            skipped_unparseable += 1
            continue
        span = extraction["end_line"] - extraction["start_line"] + 1
        if span > MAX_METHOD_LINES_FOR_REFACTORING:
            skipped_too_large += 1
            continue

        if max_per_file is not None and file_path is not None:
            file_counts[file_path] = file_counts.get(file_path, 0) + 1
        # Stash the extraction so _refactor_one_issue doesn't redo it.
        issue["_extraction"] = extraction
        selected.append(issue)

    logger.info(
        "Refactoring %d issues with strategies %s "
        "(skipped %d unrefactorable rules, %d too-large scopes, %d unparseable)",
        len(selected), strategies,
        skipped_unrefactorable_rule, skipped_too_large, skipped_unparseable,
    )

    model, tokenizer = _load_model(model_name)

    retrieval_index = None
    if "few_shot_retrieval" in strategies:
        logger.info("Loading retrieval index...")
        retrieval_index = utils.build_retrieval_index(
            cache_dir=DEFAULT_RETRIEVAL_CACHE,
            subset=utils.AGENT_RETRIEVAL_SUBSET,
            force_rebuild=False,
        )

    records = []
    for i, issue in enumerate(selected, start=1):
        logger.info("[%d/%d] Refactoring issue %s on %s:%d",
                    i, len(selected),
                    issue.get("rule"),
                    issue.get("file_relative", issue.get("file_path")),
                    issue.get("begin_line", 0))
        record = _refactor_one_issue(
            issue, repo_root, model, tokenizer,
            retrieval_index, strategies,
        )
        records.append(record)
        if log_to_feedback:
            _log_to_feedback(record, issue, repo_name)
    
    if save_to is not None:
        save_refactor_records(
            records,
            output_path=save_to,
            model_name=model_name,
            repo_name=repo_name,
            strategies=strategies,
        )

    return records


# ---------------------------------------------------------------------------
# Issue selection.
# ---------------------------------------------------------------------------

def _is_refactorable(issue: dict) -> Optional[dict]:
    """Return method extraction result, or None if the file is unreadable
    or no method contains the issue's line. Caller checks size separately."""
    file_path = issue.get("file_path")
    line = issue.get("begin_line")
    if not file_path or not line:
        return None
    try:
        with open(file_path, "r", encoding="utf-8", errors="replace") as f:
            text = f.read()
    except OSError:
        return None
    return _extract_method_source(text, line)

def _select_top_issues(ranked_issues, n, max_per_file):
    """Take top N with optional max-per-file cap (same logic as Stage 5)."""
    selected = []
    file_counts = {}
    for issue in ranked_issues:
        if len(selected) >= n:
            break
        file_path = issue.get("file_path")
        if max_per_file is not None and file_path is not None:
            count = file_counts.get(file_path, 0)
            if count >= max_per_file:
                continue
            file_counts[file_path] = count + 1
        selected.append(issue)
    return selected


# ---------------------------------------------------------------------------
# Method extraction.
# ---------------------------------------------------------------------------


def _refactor_one_issue(issue, repo_root, model, tokenizer,
                        retrieval_index, strategies):
    """Run all strategies on one issue and return a refactoring record."""
    file_path = issue["file_path"]

    # Read source file once.
    try:
        with open(file_path, "r", encoding="utf-8", errors="replace") as f:
            file_text = f.read()
    except OSError as e:
        return _empty_record(issue, error=f"could not read file: {e}")

    # Use cached extraction from the selection step if available;
    # otherwise compute fresh.
    extraction = issue.get("_extraction")
    if extraction is None:
        extraction = _extract_method_source(file_text, issue["begin_line"])
    if extraction is None:
        return _empty_record(
            issue,
            error="no method/class contains this issue's line",
        )

    method_source = extraction["source"]
    method_name = extraction["method_name"]
    method_start_line = extraction["start_line"]
    method_end_line = extraction["end_line"]

    # Run each strategy and collect results.
    strategy_results = []
    for strategy in strategies:
        retrieval = retrieval_index if strategy == "few_shot_retrieval" else None
        result = _run_one_strategy(
            method_source, issue, model, tokenizer,
            retrieval, strategy,
        )
        strategy_results.append(result)

    # Pick the best strategy by confidence score.
    best = _pick_best(strategy_results)

    return {
        "issue": issue,
        "method_source": method_source,
        "method_start_line": method_start_line,
        "method_end_line": method_end_line,
        "method_name": method_name,
        "strategies": strategy_results,
        "best_strategy": best["strategy_name"] if best else None,
        "error": None,
    }


def _empty_record(issue, error):
    """Return a refactoring record marking that we couldn't refactor."""
    return {
        "issue": issue,
        "method_source": None,
        "method_start_line": None,
        "method_end_line": None,
        "method_name": None,
        "strategies": [],
        "best_strategy": None,
        "error": error,
    }


def _extract_method_source(file_text: str, line_number: int) -> Optional[dict]:
    """Locate the smallest enclosing method or class around line_number.

    Returns a dict with keys: source, start_line, end_line, method_name.
    Returns None if no method/class contains this line.

    Strategy:
      1. Parse file with javalang to find the smallest enclosing
         MethodDeclaration, ConstructorDeclaration, or TypeDeclaration
         whose start position is at or before line_number.
      2. Extract source by reading from that line and counting braces
         forward until they balance.
    """
    try:
        tree = javalang.parse.parse(file_text)
    except (javalang.parser.JavaSyntaxError, javalang.tokenizer.LexerError):
        return None

    candidates = []
    for path, node in tree:
        if not isinstance(node, (
            javalang.tree.MethodDeclaration,
            javalang.tree.ConstructorDeclaration,
            javalang.tree.ClassDeclaration,
            javalang.tree.InterfaceDeclaration,
            javalang.tree.EnumDeclaration,
        )):
            continue
        if node.position is None:
            continue
        start = node.position.line
        if start > line_number:
            continue
        candidates.append((start, node))

    if not candidates:
        return None

    # Smallest enclosing = highest start line that is <= line_number.
    candidates.sort(key=lambda x: x[0], reverse=True)
    for start_line, node in candidates:
        end_line = _find_method_end(file_text, start_line)
        if end_line is None:
            continue
        if start_line <= line_number <= end_line:
            source = _slice_lines(file_text, start_line, end_line)
            method_name = getattr(node, "name", "<unknown>")
            return {
                "source": source,
                "start_line": start_line,
                "end_line": end_line,
                "method_name": method_name,
            }
    return None


def _find_method_end(file_text: str, start_line: int) -> Optional[int]:
    """Find the closing brace line for a method/class starting at start_line.

    Reads forward from start_line, counting braces. Returns the line
    number of the closing brace. Returns None if braces don't balance.
    """
    lines = file_text.split("\n")
    if start_line - 1 >= len(lines):
        return None

    depth = 0
    seen_open = False
    in_block_comment = False
    in_line_comment = False
    in_string = False
    in_char = False
    string_quote = None

    for i in range(start_line - 1, len(lines)):
        line = lines[i]
        j = 0
        while j < len(line):
            c = line[j]
            nxt = line[j+1] if j+1 < len(line) else ""

            # Ignore content inside strings, chars, comments.
            if in_block_comment:
                if c == "*" and nxt == "/":
                    in_block_comment = False
                    j += 2
                    continue
                j += 1
                continue
            if in_line_comment:
                break
            if in_string:
                if c == "\\":
                    j += 2
                    continue
                if c == string_quote:
                    in_string = False
                    string_quote = None
                j += 1
                continue
            if in_char:
                if c == "\\":
                    j += 2
                    continue
                if c == "'":
                    in_char = False
                j += 1
                continue
            # Detect comment/string starts.
            if c == "/" and nxt == "*":
                in_block_comment = True
                j += 2
                continue
            if c == "/" and nxt == "/":
                in_line_comment = True
                break
            if c == '"':
                in_string = True
                string_quote = '"'
                j += 1
                continue
            if c == "'":
                in_char = True
                j += 1
                continue
            # Track braces.
            if c == "{":
                depth += 1
                seen_open = True
            elif c == "}":
                depth -= 1
                if seen_open and depth == 0:
                    return i + 1  # 1-indexed line number
            j += 1
        in_line_comment = False

    return None


def _slice_lines(file_text: str, start_line: int, end_line: int) -> str:
    """Return lines [start_line..end_line] inclusive (1-indexed)."""
    lines = file_text.split("\n")
    return "\n".join(lines[start_line - 1: end_line])


def _check_signature_preserved(original: str, refactored: str) -> bool:
    """Compare method signatures (name + parameter types) between two snippets."""
    orig_sig = _extract_signature(original)
    new_sig = _extract_signature(refactored)
    if orig_sig is None or new_sig is None:
        return False
    return orig_sig == new_sig


def _extract_signature(java_snippet: str) -> Optional[tuple]:
    """Extract (method_name, [param_types]) from a Java method snippet.

    Returns None if the snippet can't be parsed. We wrap the snippet in a
    class so javalang accepts a raw method declaration.
    """
    wrapped = f"public class _SigCheck {{ {java_snippet} }}"
    try:
        tree = javalang.parse.parse(wrapped)
    except (javalang.parser.JavaSyntaxError, javalang.tokenizer.LexerError):
        return None

    for _, m in tree.filter(javalang.tree.MethodDeclaration):
        params = tuple(
            (p.type.name if hasattr(p.type, "name") else str(p.type))
            for p in m.parameters
        )
        return (m.name, params)
    for _, c in tree.filter(javalang.tree.ConstructorDeclaration):
        params = tuple(
            (p.type.name if hasattr(p.type, "name") else str(p.type))
            for p in c.parameters
        )
        return (c.name, params)
    return None

# ---------------------------------------------------------------------------
# Agent execution.
# ---------------------------------------------------------------------------


def _load_model(model_name: str):
    """Load the HuggingFace causal LM and tokenizer."""
    from transformers import AutoModelForCausalLM, AutoTokenizer
    logger.info("Loading tokenizer for %s...", model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    logger.info("Loading model %s...", model_name)
    t0 = time.time()
    model = AutoModelForCausalLM.from_pretrained(model_name)
    model.eval()
    logger.info("Model loaded in %.1fs", time.time() - t0)
    return model, tokenizer


def _run_one_strategy(method_source, issue, model, tokenizer,
                      retrieval_index, strategy_name):
    """Generate a refactoring under one strategy and evaluate it."""
    t0 = time.time()
    prompt = _build_prompt(method_source, issue, retrieval_index)

    generated_raw = _run_agent(prompt, model, tokenizer)
    generated_clean = _extract_java_from_response(generated_raw)
    elapsed = time.time() - t0

    # Validation.
    syntax = utils.validate_java_syntax(generated_clean)
    is_valid = syntax["is_valid"]

    bleu = utils.compute_bleu_against_reference(generated_clean, method_source)
    exact = utils.is_exact_match(generated_clean, method_source)
    confidence = utils.compute_confidence_score(is_valid, exact, bleu)

    sig_preserved = _check_signature_preserved(method_source, generated_clean)
    diff = _produce_diff(method_source, generated_clean,
                         issue.get("file_relative",
                                   issue.get("file_path", "method.java")))

    retrieved = []
    if retrieval_index is not None:
        # Pull the actual retrieved examples for inspection/logging.
        retrieved = utils.retrieve_similar_examples(
            method_source, retrieval_index,
            k=DEFAULT_N_RETRIEVAL,
        )

    return {
        "strategy_name": strategy_name,
        "generated_raw": generated_raw,
        "generated_clean": generated_clean,
        "is_valid_java": is_valid,
        "syntax_error": syntax.get("error"),
        "signature_preserved": sig_preserved,
        "bleu_vs_input": bleu,
        "exact_match_vs_input": exact,
        "confidence": confidence,
        "diff": diff,
        "elapsed_s": elapsed,
        "retrieved_count": len(retrieved),
        "retrieved_similarities": [
            ex.get("similarity") for ex in retrieved
        ] if retrieved else [],
    }


def _build_prompt(method_source: str, issue: dict,
                  retrieval_index: Optional[dict]) -> list:
    """Build the chat-message list for the agent.

    The prompt names the rule, gives the description, shows the
    method, and asks for a refactoring. If retrieval is provided,
    includes a few buggy/fixed example pairs as multi-turn context.
    """
    rule = issue.get("rule", "<unknown rule>")
    description = issue.get("description", "")

    user_content_parts = [
        "The following Java method has a static-analysis issue.",
        f"\nRule: {rule}",
    ]
    if description:
        user_content_parts.append(f"Description: {description}")
    user_content_parts.append(
        "\nRefactor the method to address this issue while preserving "
        "its functionality and signature. Return only the refactored "
        "method, no explanation."
    )
    user_content_parts.append(f"\nMethod:\n\n{method_source}")
    user_content = "\n".join(user_content_parts)

    messages = []

    # Few-shot retrieval examples, if any.
    if retrieval_index is not None:
        examples = utils.retrieve_similar_examples(
            method_source, retrieval_index,
            k=DEFAULT_N_RETRIEVAL,
        )
        for ex in examples:
            messages.append({
                "role": "user",
                "content": f"Fix this Java method:\n\n{ex['buggy']}",
            })
            messages.append({
                "role": "assistant",
                "content": ex["fixed"],
            })

    messages.append({"role": "user", "content": user_content})
    return messages


def _run_agent(messages: list, model, tokenizer) -> str:
    """Apply chat template and run the model."""
    import torch
    prompt = tokenizer.apply_chat_template(
        messages, tokenize=False, add_generation_prompt=True
    )
    inputs = tokenizer(prompt, return_tensors="pt")
    with torch.no_grad():
        out = model.generate(
            **inputs,
            max_new_tokens=DEFAULT_MAX_NEW_TOKENS,
            do_sample=False,
        )
    generated = tokenizer.decode(
        out[0][inputs.input_ids.shape[1]:], skip_special_tokens=True
    )
    return generated


def _extract_java_from_response(response: str) -> str:
    """Strip markdown fences and leading imports from the model's output.

    Implements the fixes we found in the Q1 spike:
      - Handles asymmetric fences (lone closing fence).
      - Strips top-level imports that would break the class-wrap parser.

    The MVP utility module has the un-fixed version of this function.
    Stage 6 uses this local version. Documented in
    LIMITATIONS_AND_FUTURE_IMPROVEMENTS.md.
    """
    text = response.strip()

    # Case: explicit ```java fence.
    if "```java" in text:
        after = text.split("```java", 1)[1]
        if "```" in after:
            inner = after.split("```", 1)[0].strip()
        else:
            inner = after.strip()
        return _strip_leading_imports(inner).strip()

    # Case: plain fences anywhere.
    if text.startswith("```"):
        text = text[3:].lstrip()
    if text.rstrip().endswith("```"):
        idx = text.rstrip().rfind("```")
        text = text[:idx].rstrip()
    if text.endswith("```"):
        text = text[:-3].rstrip()

    return _strip_leading_imports(text).strip()


def _strip_leading_imports(text: str) -> str:
    """Strip leading import/package lines and blank lines."""
    lines = text.split("\n")
    while lines and (
        lines[0].strip().startswith("import ")
        or lines[0].strip().startswith("package ")
        or not lines[0].strip()
    ):
        lines.pop(0)
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Diff and selection.
# ---------------------------------------------------------------------------


def _produce_diff(original: str, refactored: str, file_label: str) -> str:
    """Return a unified diff string."""
    orig_lines = original.splitlines(keepends=True)
    new_lines = refactored.splitlines(keepends=True)
    diff = difflib.unified_diff(
        orig_lines,
        new_lines,
        fromfile=f"a/{file_label} (original)",
        tofile=f"b/{file_label} (refactored)",
        lineterm="",
    )
    return "\n".join(diff)


def _pick_best(strategy_results: list) -> Optional[dict]:
    """Pick the strategy with the highest confidence score.

    A strategy is eligible only if it is valid Java AND preserves the
    method signature. Strategies that change the signature are never
    chosen as best, even if they parse, because a signature change
    silently breaks callers.
    """
    if not strategy_results:
        return None
    eligible = [
        s for s in strategy_results
        if s["confidence"]["level"] != "FAILED"
        and s["signature_preserved"]
    ]
    if not eligible:
        return None
    return max(eligible, key=lambda s: s["confidence"]["score"])

# ---------------------------------------------------------------------------
# Feedback logging.
# ---------------------------------------------------------------------------


def _log_to_feedback(record: dict, issue: dict, repo_name: Optional[str]):
    """Write a 'refactored' event for this issue to Stage 8's database."""
    payload = {
        "method_name": record.get("method_name"),
        "method_start_line": record.get("method_start_line"),
        "method_end_line": record.get("method_end_line"),
        "best_strategy": record.get("best_strategy"),
        "error": record.get("error"),
        "strategies": [
            {
                "strategy_name": s["strategy_name"],
                "is_valid_java": s["is_valid_java"],
                "signature_preserved": s["signature_preserved"],
                "bleu_vs_input": s["bleu_vs_input"],
                "confidence_level": s["confidence"]["level"],
                "confidence_score": s["confidence"]["score"],
                "elapsed_s": s["elapsed_s"],
                "retrieved_count": s["retrieved_count"],
            }
            for s in record.get("strategies", [])
        ],
    }
    log_event(
        event_type="refactored",
        issue=issue,
        repo_name=repo_name,
        payload=payload,
    )

# ---------------------------------------------------------------------------
# JSON save and load.
# ---------------------------------------------------------------------------


SCHEMA_VERSION = 1


def save_refactor_records(
    records: list,
    output_path: str,
    model_name: str,
    repo_name: Optional[str] = None,
    strategies: tuple = DEFAULT_STRATEGIES,
) -> None:
    """Save refactoring records to JSON with self-describing metadata.

    The saved file can be loaded later with load_refactor_records and
    used in place of running the agent live. This lets the demo
    notebook display 3B Nexus outputs without requiring a GPU.

    Internal cache fields (e.g., _extraction on each issue) are
    stripped from the saved file because they are not stable artifacts.
    """
    from datetime import datetime, timezone

    cleaned_records = []
    for record in records:
        issue_clean = {
            k: v for k, v in record["issue"].items() if k != "_extraction"
        }
        cleaned = {**record, "issue": issue_clean}
        cleaned_records.append(cleaned)

    envelope = {
        "schema_version": SCHEMA_VERSION,
        "model_name": model_name,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "repo_name": repo_name,
        "strategies": list(strategies),
        "n_records": len(cleaned_records),
        "records": cleaned_records,
    }

    output_dir = os.path.dirname(output_path)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(envelope, f, indent=2)

    logger.info(
        "Saved %d refactoring records to %s",
        len(cleaned_records), output_path,
    )


def load_refactor_records(input_path: str) -> dict:
    """Load a refactor-records envelope from JSON.

    Returns the full envelope including metadata. The records are at
    envelope["records"]; metadata is at top level.

    Raises:
        FileNotFoundError: if input_path does not exist.
        ValueError: if the file is not a valid refactor-records envelope.
    """
    if not os.path.exists(input_path):
        raise FileNotFoundError(
            f"Refactor records file not found: {input_path}"
        )

    with open(input_path, "r", encoding="utf-8") as f:
        envelope = json.load(f)

    if not isinstance(envelope, dict):
        raise ValueError(
            f"Expected a JSON object in {input_path}; got {type(envelope)}"
        )
    if "records" not in envelope:
        raise ValueError(
            f"{input_path} is not a refactor-records file: missing 'records'"
        )
    if "schema_version" not in envelope:
        raise ValueError(
            f"{input_path} is missing schema_version"
        )
    if envelope["schema_version"] != SCHEMA_VERSION:
        logger.warning(
            "Loading records with schema_version %s; expected %s. "
            "Some fields may be missing or differ.",
            envelope["schema_version"], SCHEMA_VERSION,
        )

    logger.info(
        "Loaded %d refactoring records from %s (model=%s, generated_at=%s)",
        len(envelope["records"]),
        input_path,
        envelope.get("model_name", "<unknown>"),
        envelope.get("generated_at", "<unknown>"),
    )
    return envelope

def save_ranked_issues(
    ranked_issues: list,
    output_path: str,
    repo_root: str,
    java_source_root: str,
    repo_name: Optional[str] = None,
) -> None:
    """Save Stage 5's ranked issues to JSON for cross-machine handoff.

    Used to ship the issue list from a CPU machine (where Stages 1-5
    ran) to a GPU machine (where Stage 6 runs). Includes repo metadata
    so the GPU machine knows where the repo lives in its own filesystem.
    """
    from datetime import datetime, timezone

    cleaned = []
    for issue in ranked_issues:
        # Strip internal cache fields. Keep all derived fields from
        # earlier stages (fault_probability, score, priority_rank, etc.).
        clean = {k: v for k, v in issue.items() if not k.startswith("_")}
        cleaned.append(clean)

    envelope = {
        "schema_version": SCHEMA_VERSION,
        "saved_at": datetime.now(timezone.utc).isoformat(),
        "repo_name": repo_name,
        "repo_root_on_origin": repo_root,
        "java_source_root_on_origin": java_source_root,
        "n_issues": len(cleaned),
        "issues": cleaned,
    }

    output_dir = os.path.dirname(output_path)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(envelope, f, indent=2)

    logger.info(
        "Saved %d ranked issues to %s",
        len(cleaned), output_path,
    )


def load_ranked_issues(input_path: str) -> dict:
    """Load Stage 5 issues from a JSON envelope.

    Returns the full envelope. Issues are at envelope["issues"];
    repo metadata is at top level. The caller is responsible for
    overriding repo_root and java_source_root if the repo lives at
    a different absolute path on this machine.
    """
    if not os.path.exists(input_path):
        raise FileNotFoundError(
            f"Issues file not found: {input_path}"
        )

    with open(input_path, "r", encoding="utf-8") as f:
        envelope = json.load(f)

    if "issues" not in envelope:
        raise ValueError(
            f"{input_path} is not a ranked-issues file: missing 'issues'"
        )
    if "schema_version" not in envelope:
        raise ValueError(
            f"{input_path} is missing schema_version"
        )

    logger.info(
        "Loaded %d ranked issues from %s (saved_at=%s)",
        len(envelope["issues"]),
        input_path,
        envelope.get("saved_at", "<unknown>"),
    )
    return envelope