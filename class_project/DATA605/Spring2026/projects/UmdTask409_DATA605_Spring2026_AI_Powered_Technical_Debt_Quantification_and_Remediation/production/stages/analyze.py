"""
Stage 2: Analyze a Java source tree with PMD and return a flat list
of structured debt issues.

This stage is repo-agnostic. It expects a path to a Java source root
(typically ending in src/main/java for Maven-style projects) and runs
PMD against the configured rulesets.

Usage:
    from production.stages.analyze import analyze_repository
    issues = analyze_repository("/path/to/repo/src/main/java")
    # issues is a list of dicts, one per detected debt instance.
"""

import hashlib
import json
import logging
import os
import subprocess
import tempfile
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)


# Defaults. The PMD path is the version we installed in the container.
# When we add PMD to the Dockerfile, we'll pin this version there.
DEFAULT_PMD_PATH = "/opt/pmd-bin-7.23.0/bin/pmd"

# Wide-net ruleset that covers all four README debt categories:
#   - code_smells, architectural_violations: covered by quickstart
#   - performance_issues: covered by performance.xml
#   - outdated_patterns: deprecation rules within quickstart's BestPractices
#   - security findings: covered by security.xml (none expected for
#     pure-utility code, but included so the pipeline can detect them
#     if a different repo has them)
DEFAULT_RULESETS = [
    "rulesets/java/quickstart.xml",
    "category/java/performance.xml",
    "category/java/security.xml",
]


def analyze_repository(
    source_path: str,
    pmd_path: str = DEFAULT_PMD_PATH,
    rulesets: Optional[list] = None,
    report_path: Optional[str] = None,
) -> list:
    """Run PMD against a Java source tree and return a normalized issue list.

    Args:
        source_path: absolute path to the Java source root.
        pmd_path: absolute path to the pmd binary.
        rulesets: list of PMD ruleset references; defaults to DEFAULT_RULESETS.
        report_path: where to save PMD's raw JSON report; if None, uses a
            temp file that is left in /tmp for inspection.

    Returns:
        list of issue dicts with keys: issue_id, file_path, file_relative,
        rule, ruleset, begin_line, end_line, begin_column, end_column,
        priority, description, external_info_url.

    Raises:
        FileNotFoundError: if source_path or pmd_path doesn't exist.
        RuntimeError: if PMD fails or produces unparseable output.
    """
    if rulesets is None:
        rulesets = DEFAULT_RULESETS

    # Validate inputs early so failures are clear.
    if not os.path.exists(source_path):
        raise FileNotFoundError(f"Source path does not exist: {source_path}")
    if not os.path.exists(pmd_path):
        raise FileNotFoundError(f"PMD binary does not exist: {pmd_path}")

    # If no report_path, use a tempfile we leave behind for debugging.
    if report_path is None:
        fd, report_path = tempfile.mkstemp(
            suffix=".json", prefix="pmd_report_", dir="/tmp"
        )
        os.close(fd)

    logger.info("Running PMD on %s", source_path)
    logger.info("Rulesets: %s", rulesets)
    logger.info("Report will be saved to %s", report_path)

    _run_pmd(source_path, pmd_path, rulesets, report_path)
    issues = _parse_pmd_report(report_path, source_path)

    logger.info("Analysis complete: %d issues across %d files",
                len(issues),
                len({i["file_path"] for i in issues}))

    return issues


def _run_pmd(source_path: str, pmd_path: str,
             rulesets: list, output_path: str) -> None:
    """Execute PMD via subprocess. Raises on failure."""
    rulesets_arg = ",".join(rulesets)
    cmd = [
        pmd_path,
        "check",
        "-d", source_path,
        "-R", rulesets_arg,
        "-f", "json",
        "-r", output_path,
    ]

    logger.debug("Executing: %s", " ".join(cmd))
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
    )

    # PMD returns 4 when it finds violations; that's not an error, it's
    # the expected outcome. Exit code 0 means no violations. Exit codes
    # other than 0 or 4 indicate a real problem (couldn't parse, ran out
    # of memory, bad ruleset path, etc.)
    if result.returncode not in (0, 4):
        raise RuntimeError(
            f"PMD failed with exit code {result.returncode}.\n"
            f"stdout:\n{result.stdout}\n"
            f"stderr:\n{result.stderr}"
        )


def _parse_pmd_report(report_path: str, source_path: str) -> list:
    """Read PMD's JSON report and flatten into a list of issue dicts."""
    if not os.path.exists(report_path):
        raise RuntimeError(f"PMD did not produce a report at {report_path}")

    try:
        with open(report_path, "r") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        raise RuntimeError(f"PMD report is not valid JSON: {e}") from e

    source_path_abs = os.path.abspath(source_path)
    issues = []
    for file_entry in data.get("files", []):
        file_path = file_entry["filename"]
        # Build a path relative to source_path for cleaner display.
        try:
            file_relative = os.path.relpath(file_path, source_path_abs)
        except ValueError:
            file_relative = file_path

        for v in file_entry.get("violations", []):
            issues.append({
                "issue_id": _compute_issue_id(
                    file_path, v["rule"], v["beginline"]
                ),
                "file_path": file_path,
                "file_relative": file_relative,
                "rule": v["rule"],
                "ruleset": v.get("ruleset", "Unknown"),
                "begin_line": v["beginline"],
                "end_line": v["endline"],
                "begin_column": v.get("begincolumn"),
                "end_column": v.get("endcolumn"),
                "priority": v.get("priority"),
                "description": v.get("description", "").strip(),
                "external_info_url": v.get("externalInfoUrl"),
            })

    return issues


def _compute_issue_id(file_path: str, rule: str, begin_line: int) -> str:
    """Deterministic hash for issue identity across runs."""
    payload = f"{file_path}:{rule}:{begin_line}"
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]