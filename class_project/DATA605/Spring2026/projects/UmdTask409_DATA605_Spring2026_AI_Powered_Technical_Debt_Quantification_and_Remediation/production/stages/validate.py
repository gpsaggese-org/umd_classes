"""
Stage 7: Validate Stage 6 refactorings by compiling (and optionally testing).

For each Stage 6 record with best_strategy != None, this stage:
  1. Copies the repo to a temp directory (preserving the original).
  2. Splices the refactored method into the temp copy at the right line range.
  3. Detects the build system (Maven, Gradle wrapper, system Gradle).
  4. Runs the appropriate build target (compile by default; tests if requested).
  5. Captures success/failure, error output, and timing.
  6. Logs a 'validated' event to Stage 8.
  7. Cleans up the temp directory.

This is the gate that makes Stage 6's "incremental refactoring while
maintaining test coverage and backward compatibility" claim real.
A refactoring that compiles AND passes tests has demonstrated both.

Build-system support:
  - Maven projects (pom.xml): uses 'mvn'.
  - Gradle projects with gradlew: uses './gradlew'.
  - Gradle projects without gradlew: uses system 'gradle' (4.4.1 in this
    container; many modern Gradle projects will fail here).
  - No build system: validation is skipped with a clear reason.

Documented in LIMITATIONS_AND_FUTURE_IMPROVEMENTS.md.

Usage:
    from production.stages.validate import validate_refactor_records
    validations = validate_refactor_records(
        records=stage_6_records,
        repo_root=ingest_result["repo_root"],
        repo_name="commons-lang",
        run_tests=False,
    )
"""

import logging
import os
import shutil
import subprocess
import sys
import tempfile
import time
from typing import Optional

sys.path.insert(0, "/data")

from production.stages.feedback import log_event

logger = logging.getLogger(__name__)


DEFAULT_TIMEOUT_SECONDS = 180


def validate_refactor_records(
    records: list,
    repo_root: str,
    java_source_root: str,
    repo_name: Optional[str] = None,
    run_tests: bool = False,
    timeout_seconds: int = DEFAULT_TIMEOUT_SECONDS,
    log_to_feedback: bool = True,
) -> list:
    """Validate Stage 6 refactorings by patching and compiling.

    Args:
        records: list of Stage 6 refactoring records.
        repo_root: absolute path to the original git repository.
        repo_name: short name for feedback logging.
        run_tests: if True, run 'mvn test' (or equivalent) instead of
            just compile. Slower but checks behavior preservation.
        timeout_seconds: per-record timeout for the build command.
        log_to_feedback: if True, write a 'validated' event per record.

    Returns:
        list of validation records, one per input record (same order).
        Each has: succeeded, skipped, skip_reason, build_system,
        target, elapsed_s, error_summary, stdout_tail, stderr_tail,
        timed_out, issue_id, file_relative.
    """
    if not records:
        return []

    if not os.path.isdir(repo_root):
        raise FileNotFoundError(f"repo_root not found: {repo_root}")

    target = "test" if run_tests else "compile"
    logger.info(
        "Validating %d records with target=%s, timeout=%ds",
        len(records), target, timeout_seconds,
    )

    validations = []
    for i, record in enumerate(records, start=1):
        issue = record.get("issue", {})
        rule = issue.get("rule", "<unknown>")
        file_rel = issue.get("file_relative", "<unknown>")
        logger.info("[%d/%d] Validating %s on %s",
                    i, len(records), rule, file_rel)

        validation = _validate_one_record(
            record, repo_root, java_source_root,
            run_tests, timeout_seconds,
        )
        validations.append(validation)

        if log_to_feedback:
            _log_to_feedback(validation, issue, repo_name)

    n_succeeded = sum(1 for v in validations if v.get("succeeded"))
    n_skipped = sum(1 for v in validations if v.get("skipped"))
    n_failed = len(validations) - n_succeeded - n_skipped
    logger.info(
        "Validation summary: %d succeeded, %d failed, %d skipped",
        n_succeeded, n_failed, n_skipped,
    )

    return validations


# ---------------------------------------------------------------------------
# Per-record validation.
# ---------------------------------------------------------------------------


def _validate_one_record(record, repo_root, java_source_root, run_tests, timeout_seconds):
    """Validate one refactoring record. Returns a validation dict."""
    issue = record.get("issue", {})
    issue_id = issue.get("issue_id", "<no-id>")
    file_rel = issue.get("file_relative", "<no-file>")

    base = {
        "issue_id": issue_id,
        "file_relative": file_rel,
        "succeeded": False,
        "skipped": False,
        "skip_reason": None,
        "build_system": None,
        "target": "test" if run_tests else "compile",
        "elapsed_s": 0.0,
        "error_summary": None,
        "stdout_tail": "",
        "stderr_tail": "",
        "timed_out": False,
    }

    # Skip if Stage 6 didn't pick a best strategy.
    if record.get("best_strategy") is None:
        base["skipped"] = True
        base["skip_reason"] = "no best strategy from Stage 6"
        return base

    strategy = _find_strategy(record, record["best_strategy"])
    if strategy is None:
        base["skipped"] = True
        base["skip_reason"] = "best strategy not found in record"
        return base

    refactored = strategy.get("generated_clean", "")
    if not refactored.strip():
        base["skipped"] = True
        base["skip_reason"] = "refactored output is empty"
        return base

    # Copy repo to tempdir.
    t0 = time.time()
    try:
        tmpdir = _copy_repo_to_tempdir(repo_root)
    except OSError as e:
        base["error_summary"] = f"copy failed: {e}"
        return base

    try:
        # Splice the refactored method. The file_relative is relative to
        # java_source_root, not repo_root. We compute the path inside the
        # tempdir copy by transposing the source root prefix.
        source_root_in_copy = _resolve_source_root_in_copy(
            tmpdir, repo_root, java_source_root
        )
        target_file = os.path.join(source_root_in_copy, file_rel)
        if not os.path.exists(target_file):
            base["skipped"] = True
            base["skip_reason"] = f"target file missing in copy: {target_file}"
            return base


        try:
            _splice_method(
                target_file,
                record["method_start_line"],
                record["method_end_line"],
                refactored,
            )
        except (ValueError, OSError) as e:
            base["error_summary"] = f"splice failed: {e}"
            return base

        # Detect build system.
        build_system = _detect_build_system(tmpdir)
        base["build_system"] = build_system
        if build_system == "none":
            base["skipped"] = True
            base["skip_reason"] = "no Maven or Gradle build files detected"
            return base

        # Run build.
        target = "test" if run_tests else "compile"
        result = _run_build(tmpdir, build_system, target, timeout_seconds)
        base["elapsed_s"] = time.time() - t0
        base["succeeded"] = result["succeeded"]
        base["timed_out"] = result.get("timed_out", False)
        base["stdout_tail"] = _tail(result.get("stdout", ""), 2000)
        base["stderr_tail"] = _tail(result.get("stderr", ""), 2000)
        if not result["succeeded"]:
            base["error_summary"] = _summarize_error(
                result.get("stderr", "") or result.get("stdout", "")
            )

    finally:
        # Always clean up.
        try:
            shutil.rmtree(tmpdir, ignore_errors=True)
        except Exception:
            pass

    return base


def _find_strategy(record, name):
    for s in record.get("strategies", []):
        if s.get("strategy_name") == name:
            return s
    return None


# ---------------------------------------------------------------------------
# Repo copying and patching.
# ---------------------------------------------------------------------------


def _copy_repo_to_tempdir(repo_root: str) -> str:
    """Copy the repo to a fresh /tmp directory, excluding heavy folders.

    Excludes: .git, target/ (Maven), build/ (Gradle), node_modules.
    Returns the path to the copy.
    """
    tmpdir = tempfile.mkdtemp(prefix="td_validate_")
    repo_name = os.path.basename(os.path.normpath(repo_root))
    dest = os.path.join(tmpdir, repo_name)
    shutil.copytree(
        repo_root, dest,
        ignore=shutil.ignore_patterns(
            ".git", "target", "build", "node_modules", ".gradle",
        ),
    )
    return dest


def _splice_method(file_path: str, start_line: int, end_line: int,
                   replacement: str) -> None:
    """Replace lines [start_line..end_line] (1-indexed inclusive) with replacement.

    Args:
        file_path: absolute path to the file.
        start_line: 1-indexed start line.
        end_line: 1-indexed end line (inclusive).
        replacement: text to insert. Trailing newline is added if missing.

    Raises:
        ValueError: if line range is invalid.
        OSError: on file I/O errors.
    """
    if start_line < 1 or end_line < start_line:
        raise ValueError(
            f"Invalid line range: start={start_line}, end={end_line}"
        )

    with open(file_path, "r", encoding="utf-8", errors="replace") as f:
        lines = f.readlines()

    if end_line > len(lines):
        raise ValueError(
            f"end_line {end_line} > file length {len(lines)}"
        )

    if not replacement.endswith("\n"):
        replacement = replacement + "\n"

    before = lines[:start_line - 1]
    after = lines[end_line:]
    new_content = "".join(before) + replacement + "".join(after)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(new_content)


# ---------------------------------------------------------------------------
# Build-system detection and execution.
# ---------------------------------------------------------------------------


def _detect_build_system(repo_root: str) -> str:
    """Return one of: 'maven', 'gradle_wrapper', 'gradle_system', 'none'."""
    if os.path.isfile(os.path.join(repo_root, "pom.xml")):
        return "maven"
    has_gradle = (
        os.path.isfile(os.path.join(repo_root, "build.gradle"))
        or os.path.isfile(os.path.join(repo_root, "build.gradle.kts"))
    )
    if has_gradle:
        gradlew = os.path.join(repo_root, "gradlew")
        if os.path.isfile(gradlew) and os.access(gradlew, os.X_OK):
            return "gradle_wrapper"
        return "gradle_system"
    return "none"


def _run_build(repo_root: str, build_system: str, target: str,
               timeout_seconds: int) -> dict:
    """Run the appropriate build command. Returns a dict with results.

    For Maven we invoke specific plugin goals rather than lifecycle
    phases. This skips project-specific phases (rat-check, checkstyle,
    enforcer, etc.) that may require plugin versions newer than the
    container's Maven, and focuses Stage 7's question to: "does this
    patch compile?" Lifecycle phases would also run plugins that test
    things we don't care about for refactoring validation.
    """
    if build_system == "maven":
        if target == "compile":
            cmd = ["mvn", "compiler:compile", "-q", "-B"]
        elif target == "test":
            cmd = [
                "mvn",
                "compiler:compile",
                "compiler:testCompile",
                "surefire:test",
                "-q", "-B",
            ]
        else:
            cmd = ["mvn", target, "-q", "-B"]
    elif build_system == "gradle_wrapper":
        gradle_target = {"compile": "compileJava", "test": "test"}.get(
            target, target
        )
        cmd = ["./gradlew", gradle_target, "--no-daemon"]
    elif build_system == "gradle_system":
        gradle_target = {"compile": "compileJava", "test": "test"}.get(
            target, target
        )
        cmd = ["gradle", gradle_target, "--no-daemon"]
    else:
        return {
            "succeeded": False,
            "timed_out": False,
            "stdout": "",
            "stderr": f"unknown build system: {build_system}",
        }

    return _run_command(cmd, repo_root, timeout_seconds)


def _run_command(cmd: list, cwd: str, timeout_seconds: int) -> dict:
    """Run a command with a timeout. Capture stdout/stderr."""
    try:
        result = subprocess.run(
            cmd,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
        )
        return {
            "succeeded": result.returncode == 0,
            "timed_out": False,
            "stdout": result.stdout or "",
            "stderr": result.stderr or "",
        }
    except subprocess.TimeoutExpired as e:
        return {
            "succeeded": False,
            "timed_out": True,
            "stdout": (e.stdout or b"").decode(errors="replace")
                if isinstance(e.stdout, bytes) else (e.stdout or ""),
            "stderr": (e.stderr or b"").decode(errors="replace")
                if isinstance(e.stderr, bytes) else (e.stderr or ""),
        }
    except FileNotFoundError as e:
        return {
            "succeeded": False,
            "timed_out": False,
            "stdout": "",
            "stderr": f"command not found: {e}",
        }


# ---------------------------------------------------------------------------
# Helpers.
# ---------------------------------------------------------------------------

def _resolve_source_root_in_copy(repo_copy: str, repo_root: str,
                                 java_source_root: str) -> str:
    """Translate java_source_root into its location inside the repo copy.

    The copy at repo_copy mirrors the original repo_root. The source
    root keeps the same relative path inside.
    """
    rel = os.path.relpath(java_source_root, repo_root)
    return os.path.join(repo_copy, rel)

def _tail(text: str, max_chars: int) -> str:
    """Keep the last max_chars characters of a string."""
    if len(text) <= max_chars:
        return text
    return "...[truncated]...\n" + text[-max_chars:]


def _summarize_error(text: str) -> str:
    """Extract a one-line summary from build error output.

    Looks for the first "ERROR" or "error:" line; falls back to the
    first non-empty line.
    """
    if not text:
        return "build failed (no error output)"
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        if "error" in line.lower() or "ERROR" in line:
            return line[:200]
    for line in text.splitlines():
        line = line.strip()
        if line:
            return line[:200]
    return "build failed"


# ---------------------------------------------------------------------------
# Feedback logging.
# ---------------------------------------------------------------------------


def _log_to_feedback(validation, issue, repo_name):
    """Write a 'validated' event for this validation."""
    payload = {
        "succeeded": validation.get("succeeded"),
        "skipped": validation.get("skipped"),
        "skip_reason": validation.get("skip_reason"),
        "build_system": validation.get("build_system"),
        "target": validation.get("target"),
        "elapsed_s": validation.get("elapsed_s"),
        "error_summary": validation.get("error_summary"),
        "timed_out": validation.get("timed_out"),
    }
    log_event(
        event_type="validated",
        issue=issue,
        repo_name=repo_name,
        payload=payload,
    )