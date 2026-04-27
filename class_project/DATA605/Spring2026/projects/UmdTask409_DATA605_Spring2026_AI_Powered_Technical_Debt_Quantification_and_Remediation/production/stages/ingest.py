"""
Stage 1: Ingest a Java repository and resolve the local Java source root.

This stage accepts either a git URL (which it clones to a local scratch
directory) or a local filesystem path (which it uses directly), then
locates the Java source root within that repository so downstream stages
(analyze, predict, refactor) can work against a well-known path.

Usage:
    from production.stages.ingest import ingest_repository
    result = ingest_repository("https://github.com/apache/commons-lang.git")
    # result["java_source_root"] is the path downstream stages consume.
"""

import logging
import os
import re
import subprocess
from pathlib import Path
from typing import Optional
from urllib.parse import urlparse
logger = logging.getLogger(__name__)

DEFAULT_SCRATCH_DIR = "/data/production/scratch"


def ingest_repository(
    source: str,
    dest_dir: Optional[str] = None,
    java_source_subpath: Optional[str] = None,
) -> dict:
    """Ingest a Java repository and return resolved paths for downstream stages.

    Args:
        source: a git URL (https://, http://, git@, ssh://) or an absolute
            local filesystem path to an existing directory.
        dest_dir: destination for git clone output; defaults to
            /data/production/scratch/<repo-name>/. Ignored when source is a
            local path.
        java_source_subpath: explicit subpath (relative to repo root) to use
            as the Java source root. If None, auto-detects using Maven/Gradle
            layout heuristics.

    Returns:
        dict with keys:
            repo_root        -- absolute path to the repository top-level dir.
            java_source_root -- absolute path to the Java source root.
            source_input     -- the original source argument.
            was_cloned       -- True if git clone was executed, False otherwise.
            repo_name        -- basename used to identify this repo.

    Raises:
        FileNotFoundError: if source does not look like a URL and does not
            exist as a local directory.
        RuntimeError: if cloning fails, dest_dir exists but is not a git repo,
            or no Java source root can be found.
    """
    is_url = _is_url(source)

    if not is_url and not os.path.isdir(source):
        raise FileNotFoundError(
            f"Source '{source}' does not exist on disk and does not look like "
            "a git URL. Cannot determine whether it is a URL or a missing "
            "local path."
        )

    repo_name = _extract_repo_name(source)

    if is_url:
        if dest_dir is None:
            dest_dir = os.path.join(DEFAULT_SCRATCH_DIR, repo_name)

        was_cloned = False
        if os.path.exists(dest_dir):
            if not _is_valid_git_repo(dest_dir):
                raise RuntimeError(
                    f"Destination '{dest_dir}' already exists but is not a "
                    "valid git repository (no .git directory)."
                )
            logger.info(
                "Destination %s already exists and is a git repo; "
                "skipping clone.",
                dest_dir,
            )
        else:
            logger.info("Cloning %s -> %s", source, dest_dir)
            _run_git_clone(source, dest_dir)
            was_cloned = True

        repo_root = os.path.realpath(dest_dir)
    else:
        repo_root = os.path.realpath(source)
        was_cloned = False
        logger.info("Using local repository at %s", repo_root)

    if java_source_subpath is not None:
        java_source_root = os.path.realpath(
            os.path.join(repo_root, java_source_subpath)
        )
        logger.info("Using explicit Java source subpath: %s", java_source_root)
    else:
        java_source_root = _find_java_source_root(repo_root)
        logger.info("Auto-detected Java source root: %s", java_source_root)

    return {
        "repo_root": repo_root,
        "java_source_root": java_source_root,
        "source_input": source,
        "was_cloned": was_cloned,
        "repo_name": repo_name,
    }


def _is_url(source: str) -> bool:
    """Return True if source looks like a git URL rather than a local path."""
    if source.startswith(("https://", "http://", "git://", "ssh://")):
        return True
    # git@ style: git@github.com:user/repo.git
    if re.match(r"^git@[\w.\-]+:", source):
        return True
    return False


def _extract_repo_name(source: str) -> str:
    """Extract the bare repository name from a URL or local path.

    Args:
        source: git URL or local filesystem path.

    Returns:
        Repository basename without .git suffix or trailing slashes.

    Examples:
        https://github.com/apache/commons-lang.git -> commons-lang
        git@github.com:apache/commons-lang.git     -> commons-lang
        /some/local/commons-lang/                  -> commons-lang
    """
    source = source.rstrip("/")

    if _is_url(source):
        # git@ URLs: git@github.com:apache/commons-lang.git
        if re.match(r"^git@[\w.\-]+:", source):
            path_part = source.split(":", 1)[1]
        else:
            parsed = urlparse(source)
            path_part = parsed.path

        name = os.path.basename(path_part)
        if name.endswith(".git"):
            name = name[:-4]
        return name

    return os.path.basename(source)


def _find_java_source_root(repo_root: str) -> str:
    """Locate the Java source root inside a Maven/Gradle repository.

    Detection rules (applied in order):
    1. <repo_root>/src/main/java/ exists and contains .java files.
    2. First directory found by tree-walk whose name is 'java' and whose
       parent directory is named 'main' (i.e., any */main/java/ path).

    Args:
        repo_root: absolute path to the repository root.

    Returns:
        Absolute path to the Java source root.

    Raises:
        RuntimeError: if no Java source root can be found.
    """
    # Rule 1: standard Maven/Gradle top-level layout.
    candidate = os.path.join(repo_root, "src", "main", "java")
    if os.path.isdir(candidate) and _has_java_files(candidate):
        return os.path.realpath(candidate)

    # Rule 2: walk the tree for any */main/java/ path (multi-module projects).
    for dirpath, dirnames, _ in os.walk(repo_root):
        # Skip hidden directories (e.g., .git) to speed up traversal.
        dirnames[:] = [d for d in dirnames if not d.startswith(".")]
        for dname in dirnames:
            if dname == "java" and os.path.basename(dirpath) == "main":
                found = os.path.join(dirpath, dname)
                if _has_java_files(found):
                    return os.path.realpath(found)

    raise RuntimeError(
        f"No Java source root found in '{repo_root}'. "
        "Expected a Maven/Gradle layout with src/main/java or */main/java/."
    )


def _has_java_files(directory: str) -> bool:
    """Return True if directory contains at least one .java file recursively."""
    for _, _, files in os.walk(directory):
        if any(f.endswith(".java") for f in files):
            return True
    return False


def _is_valid_git_repo(path: str) -> bool:
    """Return True if path has a .git directory, indicating a git repository."""
    return os.path.isdir(os.path.join(path, ".git"))


def _run_git_clone(url: str, dest: str) -> None:
    """Clone a git repository to dest via subprocess.

    Args:
        url: git repository URL.
        dest: local destination path.

    Raises:
        RuntimeError: if git clone exits with a non-zero exit code.
    """
    cmd = ["git", "clone", url, dest]
    logger.debug("Executing: %s", " ".join(cmd))
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(
            f"git clone failed (exit code {result.returncode}).\n"
            f"stderr:\n{result.stderr}"
        )
