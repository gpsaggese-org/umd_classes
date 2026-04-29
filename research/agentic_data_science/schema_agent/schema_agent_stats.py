"""
Statistical profiling for the data profiler agent.

Computes numeric summaries, quality reports, and categorical
distributions.

Import as:

import research.agentic_data_science.schema_agent.schema_agent_stats as radsasas
"""

import typing

import pandas as pd

import helpers.hlogging as hloggin
import helpers.hpandas_stats as hpanstat

_LOG = hloggin.getLogger(__name__)

# Allowed metric names for numeric summaries.
VALID_METRICS: typing.List[str] = [
    "mean",
    "std",
    "min",
    "25%",
    "50%",
    "75%",
    "max",
]

# Default metric subset shown in reports.
DEFAULT_METRICS: typing.List[str] = ["mean", "std", "min", "50%", "max"]


def compute_llm_agent_stats(
    tag_to_df: typing.Dict[str, pd.DataFrame],
    categorical_cols_map: typing.Optional[
        typing.Dict[str, typing.List[str]]
    ] = None,
    metrics: typing.Optional[typing.List[str]] = None,
) -> typing.Dict[str, typing.Any]:
    """
    Compute a statistical profile including temporal boundaries, data quality,
    categorical distributions, and numeric summaries for LLM injection.

    Parameters
    ----------
    tag_to_df : dict
        Mapping of dataset tag → DataFrame. Supports multiple datasets.
    categorical_cols_map : dict, optional
        Mapping of tag → list of categorical column names to profile.
    metrics : list of str, optional
        Subset of numeric metrics to include. Must be from VALID_METRICS.
        Defaults to DEFAULT_METRICS.

    Returns
    -------
    dict
        Keys: temporal_boundaries, quality_reports, categorical_distributions,
        numeric_summary.
    """
    metrics = _resolve_metrics(metrics)
    dataframe_stats: typing.Dict[str, typing.Any] = {}

    # 1. Temporal boundaries
    try:
        duration_stats, _ = hpanstat.compute_duration_df(tag_to_df)
        dataframe_stats["temporal_boundaries"] = duration_stats
        print("\n=== Temporal Boundaries ===\n", duration_stats.to_string())
    except Exception as e:  # pylint: disable=broad-exception-caught
        _LOG.warning("Skipping duration stats: %s", e)
        dataframe_stats["temporal_boundaries"] = None

    # 2. Data quality
    dataframe_stats["quality_reports"] = {}
    for tag, df in tag_to_df.items():
        numeric_df = df.select_dtypes(include="number")
        if numeric_df.empty:
            _LOG.warning(
                "No numeric columns in '%s'; skipping quality report", tag
            )
            continue
        df_stamped = hpanstat.add_end_download_timestamp(numeric_df.copy())
        try:
            quality = hpanstat.report_zero_nan_inf_stats(
                df_stamped,
                zero_threshold=1e-9,
                verbose=True,
                as_txt=True,
            )
            dataframe_stats["quality_reports"][tag] = quality
            print(f"\n=== Quality Report: {tag} ===\n", quality.to_string())
        except Exception as e:  # pylint: disable=broad-exception-caught
            _LOG.warning("Quality report failed for '%s': %s", tag, e)

    # 3. Categorical distributions
    dataframe_stats["categorical_distributions"] = {}
    if categorical_cols_map:
        for tag, cols in categorical_cols_map.items():
            if tag not in tag_to_df:
                _LOG.warning("Tag '%s' not found in tag_to_df; skipping.", tag)
                continue
            dataframe_stats["categorical_distributions"][tag] = {}
            for col in cols:
                if col not in tag_to_df[tag].columns:
                    _LOG.warning("Column '%s' not in '%s'; skipping.", col, tag)
                    continue
                dist = hpanstat.get_value_counts_stats_df(tag_to_df[tag], col)
                dataframe_stats["categorical_distributions"][tag][col] = dist
                print(
                    f"\n=== Distribution: {tag} / {col} ===\n", dist.to_string()
                )

    # 4. Numeric summary (customisable metric subset)
    dataframe_stats["numeric_summary"] = {}
    for tag, df in tag_to_df.items():
        numeric_df = df.select_dtypes(include="number")
        if numeric_df.empty:
            continue
        full_summary = numeric_df.describe().T
        available = [m for m in metrics if m in full_summary.columns]
        if not available:
            _LOG.warning(
                "None of the requested metrics %s are available.", metrics
            )
        summary = full_summary[available].copy()
        if "50%" in summary.columns:
            summary = summary.rename(columns={"50%": "median"})
        dataframe_stats["numeric_summary"][tag] = summary
        print(f"\n=== Numeric Summary: {tag} ===\n", summary.to_string())

    return dataframe_stats


def _resolve_metrics(
    metrics: typing.Optional[typing.List[str]],
) -> typing.List[str]:
    """
    Validate and return the metric list, falling back to DEFAULT_METRICS.
    """
    if metrics is None:
        return DEFAULT_METRICS
    invalid = [m for m in metrics if m not in VALID_METRICS]
    if invalid:
        _LOG.warning(
            "Unknown metrics %s will be ignored. Valid options: %s",
            invalid,
            VALID_METRICS,
        )
    resolved = [m for m in metrics if m in VALID_METRICS]
    return resolved if resolved else DEFAULT_METRICS
