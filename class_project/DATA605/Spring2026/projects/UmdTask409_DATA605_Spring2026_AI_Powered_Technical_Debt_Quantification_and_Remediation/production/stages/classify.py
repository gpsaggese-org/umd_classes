"""
Stage 3: Aggregate PMD-classified issues into the README-flavor categories.

PMD already classifies each issue into one of its 8 native rulesets
(Best Practices, Code Style, Design, Documentation, Error Prone,
Multithreading, Performance, Security). We map each issue to a
README-flavor category using two layers:

1. Per-rule mapping (primary). A curated CSV maps 292 specific PMD
   rules to README categories with per-rule reasoning. This is more
   accurate than ruleset-level classification because individual rules
   in the same ruleset can describe different kinds of problems.

2. Ruleset-level fallback (secondary). For any rule not in the CSV
   (for example, a new PMD rule added after the CSV was curated),
   we fall back to mapping the issue's PMD ruleset to a README
   category.

This layered approach means the CSV needs no maintenance to keep the
pipeline working when PMD adds new rules: unmapped rules still get
classified by their ruleset.

The README's framing is "code smells, architectural violations,
outdated patterns, performance issues." We extend this with a
fifth category (concurrency_issues) to honestly accommodate
multithreading findings rather than hiding them under code_smells.

Usage:
    from production.stages.classify import aggregate_to_readme_view
    view = aggregate_to_readme_view(issues)
    print(view["total"], "issues across", len(view["buckets"]), "buckets")
"""

import csv
import logging
import os
from typing import Optional

logger = logging.getLogger(__name__)


# Path to the curated per-rule mapping CSV. Loaded once at module import.
RULE_MAPPING_CSV_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "data",
    "pmd_rule_mapping.csv",
)


# PMD ruleset name -> README category. Used as fallback when a rule is
# not in the per-rule mapping CSV.
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


def _load_rule_mapping(csv_path: str) -> dict:
    """Load the per-rule mapping from CSV.

    Returns:
        dict mapping rule_id (str) to README category (str).
        Empty dict if the CSV cannot be read.
    """
    if not os.path.exists(csv_path):
        logger.warning(
            "Rule mapping CSV not found at %s. "
            "Per-rule classification disabled; only ruleset fallback used.",
            csv_path,
        )
        return {}

    mapping = {}
    try:
        with open(csv_path, "r", encoding="utf-8") as fh:
            reader = csv.DictReader(fh)
            for row in reader:
                rule_id = row.get("rule_id", "").strip()
                category = row.get("our_category", "").strip()
                if rule_id and category:
                    mapping[rule_id] = category
    except (OSError, csv.Error) as exc:
        logger.warning("Failed to load rule mapping CSV: %s", exc)
        return {}

    logger.info("Loaded %d per-rule mappings from %s", len(mapping), csv_path)
    return mapping


# Load once at module import.
RULE_TO_README = _load_rule_mapping(RULE_MAPPING_CSV_PATH)


def classify_issue(issue: dict) -> Optional[str]:
    """Determine the README category for a single issue.

    Args:
        issue: dict with at least 'rule' and 'ruleset' fields.

    Returns:
        A README category name (one of README_BUCKETS), or None if
        the issue cannot be classified by either layer.
    """
    rule = issue.get("rule")
    ruleset = issue.get("ruleset")

    # Primary: per-rule mapping from CSV.
    if rule and rule in RULE_TO_README:
        return RULE_TO_README[rule]

    # Fallback: ruleset-level mapping.
    if ruleset and ruleset in PMD_RULESET_TO_README:
        return PMD_RULESET_TO_README[ruleset]

    return None


def aggregate_to_readme_view(issues: list) -> dict:
    """Group classified issues into README-flavor buckets.

    Args:
        issues: list of issue dicts produced by Stage 2 (analyze).
            Each issue should have 'rule' and 'ruleset' fields.

    Returns:
        dict with three top-level keys:
            buckets: dict mapping README category to list of issues.
            total: int, total number of input issues.
            unmapped: list of issues that could not be classified by
                either the per-rule CSV or the ruleset fallback.
                Empty in normal operation.

    Example return shape:
        {
            "total": 522,
            "buckets": {
                "code_smells": [...],
                "architectural_violations": [...],
                "performance_issues": [...],
                "outdated_patterns": [...],
                "concurrency_issues": [...],
            },
            "unmapped": [],
        }
    """
    buckets = {name: [] for name in README_BUCKETS}
    unmapped = []

    for issue in issues:
        category = classify_issue(issue)
        if category and category in buckets:
            buckets[category].append(issue)
        else:
            unmapped.append(issue)

    return {
        "total": len(issues),
        "buckets": buckets,
        "unmapped": unmapped,
    }


def summarize_view(view: dict) -> str:
    """Format a human-readable summary of a categorized view.

    Args:
        view: output of aggregate_to_readme_view.

    Returns:
        Multi-line string suitable for printing in a notebook or log.
    """
    lines = [f"Total issues: {view['total']}"]
    for bucket_name in README_BUCKETS:
        count = len(view["buckets"].get(bucket_name, []))
        lines.append(f"  {bucket_name}: {count}")
    if view["unmapped"]:
        lines.append(f"  unmapped: {len(view['unmapped'])}")
    return "\n".join(lines)