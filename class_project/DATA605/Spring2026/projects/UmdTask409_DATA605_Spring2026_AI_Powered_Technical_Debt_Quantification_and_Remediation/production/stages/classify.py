"""
Stage 3: Aggregate PMD-classified issues into the README-flavor categories.

PMD already classifies each issue into one of its 8 native rulesets
(Best Practices, Code Style, Design, Documentation, Error Prone,
Multithreading, Performance, Security). The pipeline uses PMD's
ruleset field directly for downstream decisions; this module only
exists to produce a README-flavor view for reports and writeups.

The README's framing is "code smells, architectural violations,
outdated patterns, performance issues." We extend this with a
fifth category (concurrency_issues) to honestly accommodate
multithreading findings rather than hiding them under code_smells.

Usage:
    from production.stages.classify import aggregate_to_readme_view
    view = aggregate_to_readme_view(issues)
    print(view["total"], "issues across", len(view["buckets"]), "buckets")
"""

import logging
from typing import Optional

logger = logging.getLogger(__name__)


# PMD ruleset name -> README category.
# Documentation, Security, and rules from Best Practices/Code Style/Error Prone
# all roll into "code_smells" because they are local quality issues.
# Design rules roll into "architectural_violations" because they describe
# structural problems. Performance and Multithreading get their own buckets.
# "outdated_patterns" stays empty by design: PMD does not have a coherent
# ruleset for deprecated APIs or obsolete idioms; we acknowledge this as a
# known gap rather than mapping arbitrary rules into it.
PMD_RULESET_TO_README = {
    "Best Practices": "code_smells",
    "Code Style": "code_smells",
    "Design": "architectural_violations",
    "Documentation": "code_smells",
    "Error Prone": "code_smells",
    "Multithreading": "concurrency_issues",
    "Performance": "performance_issues",
    "Security": "code_smells",
}

README_BUCKETS = (
    "code_smells",
    "architectural_violations",
    "performance_issues",
    "outdated_patterns",
    "concurrency_issues",
)


def aggregate_to_readme_view(issues: list) -> dict:
    """Group classified issues into README-flavor buckets.

    Args:
        issues: list of issue dicts produced by Stage 2 (analyze).
            Each issue must have a 'ruleset' field with the PMD
            ruleset name.

    Returns:
        dict with two top-level keys:
            buckets: dict mapping README category name to list of issues.
            total: int, total number of input issues.
            unmapped: list of issues whose ruleset was not recognized.
                Empty in normal operation; populated if PMD adds new
                rulesets we have not seen.

    Example return shape:
        {
            "total": 522,
            "buckets": {
                "code_smells": [...],
                "architectural_violations": [...],
                "performance_issues": [...],
                "outdated_patterns": [],
                "concurrency_issues": [...],
            },
            "unmapped": [],
        }
    """
    buckets = {name: [] for name in README_BUCKETS}
    unmapped = []

    for issue in issues:
        ruleset = issue.get("ruleset")
        if ruleset is None:
            unmapped.append(issue)
            logger.warning(
                "Issue %s has no ruleset field; not aggregated.",
                issue.get("issue_id", "<unknown>"),
            )
            continue

        readme_category = PMD_RULESET_TO_README.get(ruleset)
        if readme_category is None:
            unmapped.append(issue)
            logger.warning(
                "PMD ruleset %r not recognized; issue %s left unmapped.",
                ruleset,
                issue.get("issue_id", "<unknown>"),
            )
            continue

        buckets[readme_category].append(issue)

    return {
        "total": len(issues),
        "buckets": buckets,
        "unmapped": unmapped,
    }


def summarize_view(view: dict) -> str:
    """Produce a short text summary of an aggregated view, for printing."""
    lines = [f"Total issues: {view['total']}"]
    for bucket_name, items in view["buckets"].items():
        lines.append(f"  {bucket_name}: {len(items)}")
    if view["unmapped"]:
        lines.append(f"  unmapped (ruleset not recognized): {len(view['unmapped'])}")
    return "\n".join(lines)