"""
Stage 5: Prioritize issues by impact-over-effort ratio.

For each issue from Stage 4 (which has fault_probability), compute:
    impact = fault_probability * severity_weight * ruleset_weight
    score = impact / effort_minutes
    priority_rank = sort descending by score

The severity weight comes from PMD priority on an exponential scale.
The ruleset weight modestly upweights Performance and Multithreading.
Effort minutes are smoothed values anchored on empirical medians from
the SonarQube EFFORT field across 992,704 issues in the Lenarduzzi
Technical Debt Dataset V2. See LIMITATIONS_AND_FUTURE_IMPROVEMENTS.md.

Each issue gains four fields: severity_weight, effort_minutes, impact,
priority_rank. The function returns the augmented issue list sorted
ascending by priority_rank (rank 1 first).

Also exposed: compute_pareto_front, which returns the subset of
issues lying on the Pareto front in (impact, effort) space.

Usage:
    from production.stages.prioritize import (
        prioritize_issues, compute_pareto_front,
    )
    ranked = prioritize_issues(issues_with_probability)
    front = compute_pareto_front(ranked)
"""

import logging
from typing import Optional

logger = logging.getLogger(__name__)


# PMD priority -> normalized severity weight in [0, 1].
# Exponential scale (each step halves) so high-priority issues count
# disproportionately more than low-priority ones.
SEVERITY_WEIGHT_BY_PRIORITY = {
    1: 1.0,
    2: 0.5,
    3: 0.25,
    4: 0.125,
    5: 0.0625,
}

# PMD priority -> effort minutes. Smoothed values, monotonic, anchored on
# empirical medians from the dataset. See module docstring.
EFFORT_MINUTES_BY_PRIORITY = {
    1: 20,  # anchored on BLOCKER median (n=6018)
    2: 15,  # smoothed between CRITICAL (10) and BLOCKER (20)
    3: 10,  # anchored on MAJOR median (n=490868)
    4: 5,   # smoothed between MINOR (2) and MAJOR (10)
    5: 2,   # smoothed floor
}

# PMD ruleset -> impact multiplier. Modestly upweights categories whose
# issues have customer-visible consequences (slow code, threading bugs).
RULESET_WEIGHT = {
    "Performance": 1.2,
    "Multithreading": 1.2,
}
DEFAULT_RULESET_WEIGHT = 1.0

# Floor on effort to prevent the impact/effort ratio from exploding.
MIN_EFFORT_MINUTES = 1.0

# Default fallback when an issue lacks fault_probability.
DEFAULT_FAULT_PROBABILITY_FOR_MISSING = 0.0


def prioritize_issues(issues: list) -> list:
    """Add scoring fields to each issue and return the list ranked by score.

    Args:
        issues: list of issue dicts. Each must have 'priority' (int 1-5) and
            'ruleset' (str). 'fault_probability' is optional; missing values
            are treated as 0 and a warning is logged.

    Returns:
        The same list (mutated in place) with these new fields:
            severity_weight: float in (0, 1]
            ruleset_weight: float >= 1.0
            effort_minutes: float
            impact: float = fault_probability * severity_weight * ruleset_weight
            score: float = impact / max(effort_minutes, MIN_EFFORT_MINUTES)
            priority_rank: int starting at 1 (1 = top priority)

        The returned list is sorted by priority_rank ascending.

    Raises:
        ValueError: if the issue list is empty (caller should handle).
    """
    if not issues:
        logger.info("No issues to prioritize; returning empty list.")
        return issues

    missing_prob_count = 0

    for issue in issues:
        priority = issue.get("priority")
        ruleset = issue.get("ruleset", "")
        fault_prob = issue.get("fault_probability")

        if fault_prob is None:
            fault_prob = DEFAULT_FAULT_PROBABILITY_FOR_MISSING
            missing_prob_count += 1

        sev_weight = SEVERITY_WEIGHT_BY_PRIORITY.get(priority, 0.25)
        rs_weight = RULESET_WEIGHT.get(ruleset, DEFAULT_RULESET_WEIGHT)
        effort = EFFORT_MINUTES_BY_PRIORITY.get(priority, 10)

        impact = fault_prob * sev_weight * rs_weight
        score = impact / max(effort, MIN_EFFORT_MINUTES)

        issue["severity_weight"] = sev_weight
        issue["ruleset_weight"] = rs_weight
        issue["effort_minutes"] = effort
        issue["impact"] = impact
        issue["score"] = score

    if missing_prob_count > 0:
        logger.warning(
            "%d of %d issues had fault_probability=None; treated as 0.",
            missing_prob_count, len(issues),
        )

    issues.sort(key=lambda x: x["score"], reverse=True)
    for rank, issue in enumerate(issues, start=1):
        issue["priority_rank"] = rank

    top = issues[0]
    logger.info(
        "Ranked %d issues. Top: %s on %s:%d "
        "(impact=%.4f, effort=%.1f min, score=%.5f)",
        len(issues),
        top.get("rule"),
        top.get("file_relative", top.get("file_path")),
        top.get("begin_line", 0),
        top["impact"], top["effort_minutes"], top["score"],
    )

    return issues


def compute_pareto_front(ranked_issues: list) -> list:
    """Return the Pareto-optimal subset of issues in (impact, effort) space.

    An issue is on the Pareto front if no other issue has both higher
    impact and equal-or-lower effort. We tie-break on impact (higher
    impact wins at equal effort).

    Args:
        ranked_issues: output of prioritize_issues. Must have 'impact'
            and 'effort_minutes' fields.

    Returns:
        Subset of ranked_issues lying on the front, sorted by
        effort_minutes ascending so the trade-off curve reads
        left-to-right.
    """
    if not ranked_issues:
        return []

    # Sort by effort ascending, then impact descending. Walk through and
    # keep only issues whose impact exceeds the running maximum.
    sorted_issues = sorted(
        ranked_issues,
        key=lambda x: (x["effort_minutes"], -x["impact"]),
    )

    front = []
    max_impact_seen = -float("inf")
    for issue in sorted_issues:
        if issue["impact"] > max_impact_seen:
            front.append(issue)
            max_impact_seen = issue["impact"]

    return front

def top_n_issues(
    ranked_issues: list,
    n: int = 10,
    max_per_file: Optional[int] = None,
) -> list:
    """Select the top N ranked issues, optionally capping per file.

    Args:
        ranked_issues: output of prioritize_issues. Must already be sorted
            by priority_rank ascending.
        n: maximum number of issues to return.
        max_per_file: if set, no file contributes more than this many
            issues to the output. None means no cap.

    Returns:
        The top N issues by priority rank, with the per-file cap applied.
    """
    if not ranked_issues:
        return []

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