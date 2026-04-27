"""
Metric and churn computation for Stage 4 (fault prediction).

This module computes the 19 code metrics and 5 churn features that the
MVP's fault predictor was trained on, but reconstructs them from real
source code (via javalang) and real git history (via subprocess) instead
of looking them up in the dataset.

The 19 metrics are computed for the entire Java source tree at HEAD.
The 5 churn features are commit-specific (per (repo, commit_sha) pair).

This is the simplification we agreed on: rather than checking out each
historical commit to compute metrics there, we use HEAD metrics for all
issues and pair them with per-commit churn. Calibration drift relative
to the trained model is documented as a known limitation.

Usage:
    from production.lib.metrics import (
        compute_repo_metrics,
        compute_commit_churn,
        find_last_touch_commit,
    )

    metrics = compute_repo_metrics("/path/to/src/main/java")
    sha = find_last_touch_commit("/path/to/repo", "src/main/java/Foo.java")
    churn = compute_commit_churn("/path/to/repo", sha)
"""

import logging
import os
import subprocess
from pathlib import Path
from typing import Optional

import javalang

logger = logging.getLogger(__name__)


# The 19 SonarQube-style metric column names the trained model expects.
METRIC_COLUMNS = [
    "COMPLEXITY",
    "FILE_COMPLEXITY",
    "CLASS_COMPLEXITY",
    "FUNCTION_COMPLEXITY",
    "COMPLEXITY_IN_CLASSES",
    "COMPLEXITY_IN_FUNCTIONS",
    "COGNITIVE_COMPLEXITY",
    "NCLOC",
    "LINES",
    "STATEMENTS",
    "FUNCTIONS",
    "CLASSES",
    "FILES",
    "COMMENT_LINES",
    "COMMENT_LINES_DENSITY",
    "DUPLICATED_LINES",
    "DUPLICATED_LINES_DENSITY",
    "DUPLICATED_BLOCKS",
    "DUPLICATED_FILES",
]

# The 5 churn column names. files_changed, lines_added, lines_removed come
# from `git log`. churn_total and churn_ratio are derived.
CHURN_COLUMNS = [
    "files_changed",
    "lines_added",
    "lines_removed",
    "churn_total",
    "churn_ratio",
]


# ---------------------------------------------------------------------------
# Public functions.
# ---------------------------------------------------------------------------


def compute_repo_metrics(java_source_root: str) -> dict:
    """Compute the 19 metrics over an entire Java source tree at HEAD.

    Walks all .java files under java_source_root, parses each with javalang,
    aggregates per-file counts and complexities into a single 19-metric dict.

    DUPLICATED_* metrics are set to 0 by design. We do not run a duplication
    detector. This is documented as a known gap.

    Args:
        java_source_root: absolute path to a Java source root (typically
            ending in src/main/java).

    Returns:
        dict with keys in METRIC_COLUMNS, each mapped to a numeric value.

    Raises:
        FileNotFoundError: if java_source_root does not exist.
        RuntimeError: if no .java files are found under the path.
    """
    if not os.path.isdir(java_source_root):
        raise FileNotFoundError(
            f"Java source root not found: {java_source_root}"
        )

    java_files = _list_java_files(java_source_root)
    if not java_files:
        raise RuntimeError(
            f"No .java files found under {java_source_root}"
        )

    logger.info("Computing metrics over %d Java files", len(java_files))

    totals = {
        "COMPLEXITY": 0,
        "COGNITIVE_COMPLEXITY": 0,
        "NCLOC": 0,
        "LINES": 0,
        "STATEMENTS": 0,
        "FUNCTIONS": 0,
        "CLASSES": 0,
        "COMMENT_LINES": 0,
    }
    files_processed = 0

    for path in java_files:
        try:
            per_file = _compute_file_metrics(path)
        except (javalang.parser.JavaSyntaxError, javalang.tokenizer.LexerError) as e:
            logger.warning("Skipping unparseable file %s: %s", path, e)
            continue
        for k in totals:
            totals[k] += per_file[k]
        files_processed += 1

    if files_processed == 0:
        raise RuntimeError(
            "All Java files failed to parse; cannot compute metrics."
        )

    metrics = {
        "COMPLEXITY": totals["COMPLEXITY"],
        "FILE_COMPLEXITY": totals["COMPLEXITY"] / files_processed,
        "CLASS_COMPLEXITY": _safe_div(totals["COMPLEXITY"], totals["CLASSES"]),
        "FUNCTION_COMPLEXITY": _safe_div(
            totals["COMPLEXITY"], totals["FUNCTIONS"]
        ),
        "COMPLEXITY_IN_CLASSES": totals["COMPLEXITY"],
        "COMPLEXITY_IN_FUNCTIONS": totals["COMPLEXITY"],
        "COGNITIVE_COMPLEXITY": totals["COGNITIVE_COMPLEXITY"],
        "NCLOC": totals["NCLOC"],
        "LINES": totals["LINES"],
        "STATEMENTS": totals["STATEMENTS"],
        "FUNCTIONS": totals["FUNCTIONS"],
        "CLASSES": totals["CLASSES"],
        "FILES": files_processed,
        "COMMENT_LINES": totals["COMMENT_LINES"],
        "COMMENT_LINES_DENSITY": _comment_density(
            totals["COMMENT_LINES"], totals["NCLOC"]
        ),
        "DUPLICATED_LINES": 0,
        "DUPLICATED_LINES_DENSITY": 0,
        "DUPLICATED_BLOCKS": 0,
        "DUPLICATED_FILES": 0,
    }
    return metrics


def compute_commit_churn(repo_root: str, commit_sha: str) -> dict:
    """Compute churn features for a specific commit.

    Uses `git log -1 --numstat` to fetch added/removed line counts and
    file count for the given commit. Derives churn_total and churn_ratio.

    Args:
        repo_root: absolute path to a git repository root.
        commit_sha: full or short commit SHA.

    Returns:
        dict with keys in CHURN_COLUMNS.

    Raises:
        RuntimeError: if git fails or the commit is not found.
    """
    cmd = [
        "git", "-C", repo_root,
        "log", "-1", "--numstat", "--format=",
        commit_sha,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(
            f"git log failed for {commit_sha} in {repo_root}: "
            f"{result.stderr.strip()}"
        )

    files_changed = 0
    lines_added = 0
    lines_removed = 0
    for line in result.stdout.strip().splitlines():
        line = line.strip()
        if not line:
            continue
        parts = line.split("\t")
        if len(parts) < 3:
            continue
        added_str, removed_str = parts[0], parts[1]
        # Binary files show "-" instead of a count; skip them.
        if added_str == "-" or removed_str == "-":
            continue
        try:
            lines_added += int(added_str)
            lines_removed += int(removed_str)
            files_changed += 1
        except ValueError:
            continue

    churn_total = lines_added + lines_removed
    # Match the MVP's formula exactly: lines_added / (churn_total + 1).
    # The +1 prevents division by zero for empty commits.
    churn_ratio = lines_added / (churn_total + 1)

    return {
        "files_changed": files_changed,
        "lines_added": lines_added,
        "lines_removed": lines_removed,
        "churn_total": churn_total,
        "churn_ratio": churn_ratio,
    }


def find_last_touch_commit(repo_root: str, file_relative: str) -> Optional[str]:
    """Return the SHA of the most recent commit that touched a file.

    Args:
        repo_root: absolute path to a git repository root.
        file_relative: path to the file relative to repo_root, OR an
            absolute path that is inside repo_root.

    Returns:
        The full commit SHA as a string. Returns None if the file has
        never been committed (e.g., uncommitted new file).

    Raises:
        RuntimeError: if git itself fails.
    """
    if os.path.isabs(file_relative):
        try:
            file_relative = os.path.relpath(file_relative, repo_root)
        except ValueError:
            pass

    cmd = [
        "git", "-C", repo_root,
        "log", "-1", "--format=%H", "--", file_relative,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(
            f"git log failed for {file_relative} in {repo_root}: "
            f"{result.stderr.strip()}"
        )
    sha = result.stdout.strip()
    if not sha:
        return None
    return sha


# ---------------------------------------------------------------------------
# Internal helpers: file walking, parsing, complexity.
# ---------------------------------------------------------------------------


def _list_java_files(root: str) -> list:
    """Return a sorted list of all .java files under root."""
    matches = []
    for dirpath, _, filenames in os.walk(root):
        for fn in filenames:
            if fn.endswith(".java"):
                matches.append(os.path.join(dirpath, fn))
    return sorted(matches)


def _compute_file_metrics(path: str) -> dict:
    """Compute per-file metrics from a single .java file.

    Returns a dict with keys: COMPLEXITY, COGNITIVE_COMPLEXITY, NCLOC,
    LINES, STATEMENTS, FUNCTIONS, CLASSES, COMMENT_LINES.
    """
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        text = f.read()

    total_lines, comment_lines, ncloc = _count_lines(text)
    tree = javalang.parse.parse(text)

    classes = sum(
        1
        for _, node in tree.filter(javalang.tree.TypeDeclaration)
    )
    functions = sum(
        1
        for _, node in tree.filter(javalang.tree.MethodDeclaration)
    )
    statements = sum(
        1
        for _, node in tree.filter(javalang.tree.Statement)
    )

    cyclomatic = 0
    cognitive = 0
    for _, method in tree.filter(javalang.tree.MethodDeclaration):
        cyclomatic += _cyclomatic_complexity(method)
        cognitive += _cognitive_complexity_approx(method)
    # Constructors contribute too.
    for _, ctor in tree.filter(javalang.tree.ConstructorDeclaration):
        cyclomatic += _cyclomatic_complexity(ctor)
        cognitive += _cognitive_complexity_approx(ctor)

    return {
        "COMPLEXITY": cyclomatic,
        "COGNITIVE_COMPLEXITY": cognitive,
        "NCLOC": ncloc,
        "LINES": total_lines,
        "STATEMENTS": statements,
        "FUNCTIONS": functions,
        "CLASSES": classes,
        "COMMENT_LINES": comment_lines,
    }


def _count_lines(text: str) -> tuple:
    """Return (total_lines, comment_lines, ncloc).

    NCLOC is non-blank, non-comment lines. comment_lines is lines fully
    inside a comment (line or block). Lines containing both code and an
    end-of-line comment count as NCLOC, not comment.
    """
    lines = text.split("\n")
    total = len(lines)
    comment = 0
    code = 0
    in_block_comment = False
    for raw in lines:
        stripped = raw.strip()
        if not stripped:
            continue
        if in_block_comment:
            comment += 1
            if "*/" in stripped:
                in_block_comment = False
            continue
        if stripped.startswith("/*"):
            comment += 1
            if "*/" not in stripped[2:]:
                in_block_comment = True
            continue
        if stripped.startswith("//"):
            comment += 1
            continue
        # Has code; trailing // does not change classification.
        code += 1
    return total, comment, code


def _cyclomatic_complexity(method) -> int:
    """McCabe cyclomatic complexity for a single method or constructor.

    Counts: 1 base + 1 per decision point (if, for, while, do-while,
    case label, catch, &&, ||, ternary).
    """
    complexity = 1
    if method.body is None:
        return complexity

    for _, node in method:
        if isinstance(node, javalang.tree.IfStatement):
            complexity += 1
        elif isinstance(node, (javalang.tree.ForStatement,
                               javalang.tree.WhileStatement,
                               javalang.tree.DoStatement)):
            complexity += 1
        elif isinstance(node, javalang.tree.SwitchStatementCase):
            # Each case label adds a path.
            if node.case:
                complexity += len(node.case)
        elif isinstance(node, javalang.tree.CatchClause):
            complexity += 1
        elif isinstance(node, javalang.tree.TernaryExpression):
            complexity += 1
        elif isinstance(node, javalang.tree.BinaryOperation):
            if node.operator in ("&&", "||"):
                complexity += 1
    return complexity


def _cognitive_complexity_approx(method) -> int:
    """Approximate cognitive complexity.

    This is NOT Campbell's full algorithm. It is cyclomatic-minus-1, which
    gives the same order of magnitude. The approximation is documented in
    LIMITATIONS_AND_FUTURE_IMPROVEMENTS.md. See the module docstring.
    """
    return max(0, _cyclomatic_complexity(method) - 1)


def _safe_div(numerator: float, denominator: float) -> float:
    """Return numerator/denominator, or 0 if denominator is 0."""
    if denominator == 0:
        return 0.0
    return numerator / denominator


def _comment_density(comment_lines: int, ncloc: int) -> float:
    """SonarQube formula: comment_lines / (comment_lines + ncloc) * 100."""
    denom = comment_lines + ncloc
    if denom == 0:
        return 0.0
    return 100.0 * comment_lines / denom