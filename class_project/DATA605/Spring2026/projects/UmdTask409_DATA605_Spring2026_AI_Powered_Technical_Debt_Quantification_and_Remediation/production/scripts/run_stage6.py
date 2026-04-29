"""
Standalone script for running Stage 6 on a different machine than the
rest of the pipeline. Designed for the Nexus GPU mode.

Workflow:
    On origin machine (Mac):
        Run Stages 1-5, then call save_ranked_issues() to dump issues
        to JSON. Transfer this JSON plus the source repo to Nexus.

    On Nexus:
        Run this script with --issues=<path>, --repo-root=<path>,
        --java-source-root=<path>, --output=<path>.

The script loads the issues, runs Stage 6 with the specified model,
and saves the records to JSON. The records JSON can be loaded back
on the origin machine for Stage 7 validation and demo display.

Example:
    python production/scripts/run_stage6.py \\
        --issues /fs/nexus-scratch/kakhil/td/issues.json \\
        --repo-root /fs/nexus-scratch/kakhil/td/commons-lang \\
        --java-source-root /fs/nexus-scratch/kakhil/td/commons-lang/src/main/java \\
        --output /fs/nexus-scratch/kakhil/td/records.json \\
        --model Qwen/Qwen2.5-Coder-3B-Instruct \\
        --n 10
"""

import argparse
import logging
import os
import sys

# Make production package importable.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from production.stages.refactor import (
    refactor_top_issues,
    load_ranked_issues,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
logger = logging.getLogger("run_stage6")


def main():
    parser = argparse.ArgumentParser(
        description="Run Stage 6 on issues exported from another machine."
    )
    parser.add_argument(
        "--issues", required=True,
        help="Path to ranked-issues JSON (from save_ranked_issues).",
    )
    parser.add_argument(
        "--repo-root", required=True,
        help="Absolute path to the repo on this machine.",
    )
    parser.add_argument(
        "--java-source-root", required=True,
        help="Absolute path to the Java source root on this machine.",
    )
    parser.add_argument(
        "--output", required=True,
        help="Path where the refactoring records JSON should be written.",
    )
    parser.add_argument(
        "--model", default="Qwen/Qwen2.5-Coder-3B-Instruct",
        help="Hugging Face model ID (default: 3B).",
    )
    parser.add_argument(
        "--n", type=int, default=10,
        help="Number of top issues to refactor (default: 10).",
    )
    parser.add_argument(
        "--max-per-file", type=int, default=1,
        help="Max issues per file (default: 1).",
    )
    parser.add_argument(
        "--strategies", default="zero_shot",
        help="Comma-separated strategies (default: zero_shot only).",
    )
    parser.add_argument(
        "--repo-name", default=None,
        help="Short repo name for output metadata.",
    )

    args = parser.parse_args()

    # Load issues.
    envelope = load_ranked_issues(args.issues)
    issues = envelope["issues"]
    repo_name = args.repo_name or envelope.get("repo_name")

    # Translate file_path from origin machine to this machine.
    # The saved file_path is absolute under the origin's java_source_root.
    # We rewrite it to be absolute under our java_source_root.
    origin_jsr = envelope.get("java_source_root_on_origin")
    if origin_jsr:
        for issue in issues:
            fp = issue.get("file_path", "")
            if fp.startswith(origin_jsr):
                rel = os.path.relpath(fp, origin_jsr)
                issue["file_path"] = os.path.join(
                    args.java_source_root, rel
                )

    logger.info("Loaded %d issues. Refactoring top %d.",
                len(issues), args.n)

    strategies = tuple(s.strip() for s in args.strategies.split(",") if s.strip())

    records = refactor_top_issues(
        ranked_issues=issues,
        repo_root=args.repo_root,
        n=args.n,
        max_per_file=args.max_per_file,
        strategies=strategies,
        model_name=args.model,
        log_to_feedback=False,
        repo_name=repo_name,
        save_to=args.output,
    )

    logger.info("Done. Saved %d records to %s",
                len(records), args.output)


if __name__ == "__main__":
    main()