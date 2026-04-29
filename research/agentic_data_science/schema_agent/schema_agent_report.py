"""
Report generation and export for the data profiler agent.

Creates column profiles, JSON reports, and Markdown summaries.

Import as:

import research.agentic_data_science.schema_agent.schema_agent_report as radsasar
"""

import datetime
import json
import typing

import pandas as pd

import helpers.hlogging as hloggin

_LOG = hloggin.getLogger(__name__)


def build_column_profiles(
    df: pd.DataFrame,
    stats: typing.Dict[str, typing.Any],
    insights: typing.Dict[str, typing.Any],
) -> typing.List[typing.Dict[str, typing.Any]]:
    """
    Convert stat-centric structure into per-column profiles.

    Merges numeric stats, categorical distributions, datetime metadata,
    and LLM semantic insights keyed on column name.

    Parameters
    ----------
    df : pd.DataFrame
    stats : dict
    insights : dict  — output of generate_hypotheses_via_cli()

    Returns
    -------
    list of dict, one entry per column.
    """
    profiles: typing.List[typing.Dict[str, typing.Any]] = []

    numeric_summary = stats.get("numeric_summary", {})
    categorical_stats = stats.get("categorical_distributions", {})
    datetime_meta = stats.get("datetime_columns", {})

    for col in df.columns:
        profile: typing.Dict[str, typing.Any] = {
            "column": col,
            "dtype": str(df[col].dtype),
            "null_pct": float(df[col].isnull().mean()),
            "unique_count": int(df[col].nunique()),
            "sample_values": df[col].dropna().head(3).tolist(),
        }

        # Numeric stats
        for _, summary_df in numeric_summary.items():
            if col in summary_df.index:
                col_stats = summary_df.loc[col]
                for metric in col_stats.index:
                    profile[metric] = col_stats[metric]

        # Categorical top values
        for _, cols in categorical_stats.items():
            if col in cols:
                dist = cols[col]
                try:
                    profile["top_values"] = (
                        dist.head(3).to_dict()
                        if hasattr(dist, "head")
                        else dict(list(dist.items())[:3])
                    )
                except Exception:  # pylint: disable=broad-exception-caught
                    pass

        # Datetime metadata
        if col in datetime_meta:
            profile["temporal"] = datetime_meta[col]

        # LLM insights
        if "columns" in insights and col in insights["columns"]:
            insight = insights["columns"][col]
            if hasattr(insight, "dict"):
                insight = insight.dict()
            profile.update(
                {
                    "semantic_meaning": insight.get("semantic_meaning"),
                    "role": insight.get("role"),
                    "data_quality_notes": insight.get("data_quality_notes"),
                    "hypotheses": insight.get("hypotheses", []),
                }
            )

        profiles.append(profile)

    return profiles


def merge_and_export_results(
    stats: typing.Dict[str, typing.Any],
    insights: typing.Dict[str, typing.Any],
    column_profiles: typing.List[typing.Dict[str, typing.Any]],
    output_path: str = "data_profile_report.json",
) -> None:
    """
    Merge stats + insights + column_profiles and export to JSON.

    Parameters
    ----------
    stats : dict
    insights : dict
    column_profiles : list of dict
    output_path : str
    """
    _LOG.info("Merging results...")
    serializable_stats = _make_serializable(stats)

    final_report = {
        "report_metadata": {
            "version": "1.2",
            "agent": "Data-Profiler-Agent",
            "generated_at": datetime.datetime.utcnow().isoformat() + "Z",
        },
        "column_profiles": column_profiles,
        "technical_stats": serializable_stats,
        "semantic_insights": insights,
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(final_report, f, indent=4, default=str)

    _LOG.info("Exported JSON report to '%s'.", output_path)


def _make_serializable(obj: typing.Any) -> typing.Any:
    """
    Recursively convert DataFrames and nested dicts to JSON-safe structures.
    """
    if isinstance(obj, pd.DataFrame):
        return obj.to_dict(orient="index")
    if isinstance(obj, dict):
        return {k: _make_serializable(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_make_serializable(v) for v in obj]
    return obj


def export_markdown_from_profiles(
    column_profiles: typing.List[typing.Dict[str, typing.Any]],
    numeric_stats: typing.Optional[typing.Dict[str, pd.DataFrame]] = None,
    output_path: str = "data_profile_summary.md",
) -> None:
    """
    Generate a readable Markdown report from column profiles and numeric stats.

    Parameters
    ----------
    column_profiles : list of dict
    numeric_stats : dict of str → DataFrame, optional
    output_path : str
    """

    def _clean(val: typing.Any) -> str:
        if val is None:
            return ""
        return str(val).replace("|", "\\|").replace("\n", " ")

    def _fmt(val: typing.Any) -> str:
        if isinstance(val, int):
            return str(val)
        if isinstance(val, float):
            return f"{val:,.2f}" if abs(val) >= 1 else f"{val:.4f}"
        return str(val)

    lines = ["# Data Profile Summary\n"]

    # Column profiles table
    lines.append("## Column Profiles\n")
    lines.append("| Column | Meaning | Role | Quality | Hypotheses |")
    lines.append("|--------|---------|------|---------|------------|")

    for p in column_profiles:
        hypotheses = p.get("hypotheses", [])
        if isinstance(hypotheses, list) and hypotheses:
            hyp_str = "<br>".join(
                f"{i+1}. {_clean(h)}" for i, h in enumerate(hypotheses[:3])
            )
        else:
            hyp_str = _clean(hypotheses) or "N/A"

        row = [
            _clean(p.get("column")),
            _clean(p.get("semantic_meaning")),
            _clean(p.get("role")),
            _clean(p.get("data_quality_notes")),
            hyp_str,
        ]
        lines.append("| " + " | ".join(row) + " |")

    # Numeric stats table
    if numeric_stats:
        lines.append("\n## Numeric Column Statistics\n")
        for tag, df in numeric_stats.items():
            lines.append(f"### {tag}\n")
            lines.append("| Column | Metric | Value |")
            lines.append("|--------|--------|-------|")
            for col_name in df.index:
                for metric in df.columns:
                    val = df.loc[col_name, metric]
                    lines.append(f"| {col_name} | {metric} | {_fmt(val)} |")
            lines.append("")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    _LOG.info("Exported Markdown report to '%s'.", output_path)
