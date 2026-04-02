"""
Data Profiler Agent — single-file implementation.

Import as:
    import research.agentic_data_science.schema_agent.schema_agent_utils as radssasau

CLI usage:
    python schema_agent_utils.py data.csv
    python schema_agent_utils.py data.csv --model gpt-4o-mini --llm-scope nulls
    python schema_agent_utils.py data.csv --metrics mean std min max --output-json out.json
    python schema_agent_utils.py data.csv data2.csv --tags sales inventory
"""

import argparse
import datetime
import json
import logging
import os
import sys
import typing

import dotenv
import langchain_core.output_parsers as lcop
import langchain_core.prompts as lcpr
import langchain_openai as lco
import openai
import pandas as pd
import pydantic

import helpers.hllm_cli as hllmcli
import helpers.hlogging as hloggin
import helpers.hpandas_conversion as hpanconv
import helpers.hpandas_io as hpanio
import helpers.hpandas_stats as hpanstat


# =============================================================================
# Configuration & Logging
# =============================================================================

dotenv.load_dotenv()
api_key = os.environ.get("OPENAI_API_KEY")
if not api_key:
    print("Error: OPENAI_API_KEY not found in environment.")
    sys.exit(1)

client = openai.OpenAI(api_key=api_key)
_LOG = hloggin.getLogger(__name__)
_LOG.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler(sys.stdout)
hloggin.set_v2_formatter(
    ch=console_handler,
    root_logger=_LOG,
    force_no_warning=False,
    force_print_format=False,
    force_verbose_format=True,
    report_memory_usage=True,
    report_cpu_usage=True,
)

# Allowed metric names for numeric summaries.
VALID_METRICS: typing.List[str] = ["mean", "std", "min", "25%", "50%", "75%", "max"]

# Default metric subset shown in reports.
DEFAULT_METRICS: typing.List[str] = ["mean", "std", "min", "50%", "max"]


# =============================================================================
# Pydantic schemas
# =============================================================================


class ColumnInsight(pydantic.BaseModel):
    semantic_meaning: str = pydantic.Field(
        description="Brief description of what the data represents"
    )
    role: str = pydantic.Field(
        description="One of [ID, Feature, Target, Timestamp]"
    )
    data_quality_notes: str = pydantic.Field(
        description="Any concerns based on the stats (e.g. high nulls, outliers)"
    )
    hypotheses: typing.List[str] = pydantic.Field(
        description="List of testable hypotheses regarding the column's relationship "
        "to business outcomes."
    )


class DatasetInsights(pydantic.BaseModel):
    columns: typing.Dict[str, ColumnInsight]


# =============================================================================
# Data loading
# =============================================================================


def load_csv(csv_path: str) -> pd.DataFrame:
    """
    Load a CSV into a DataFrame with clear error handling.

    Parameters
    ----------
    csv_path : str
        Path to the CSV file.

    Returns
    -------
    pd.DataFrame
    """
    try:
        df = hpanio.read_csv_to_df(csv_path)
    except FileNotFoundError:
        _LOG.error("CSV not found at '%s'.", csv_path)
        raise
    if df.empty:
        raise ValueError(f"CSV at '{csv_path}' loaded as an empty DataFrame.")
    _LOG.info("Loaded '%s': %d rows × %d columns.", csv_path, len(df), len(df.columns))
    return df


# keep legacy name for backwards compatibility
load_employee_data = load_csv


# =============================================================================
# Datetime inference
# =============================================================================


def infer_and_convert_datetime_columns(
    df: pd.DataFrame,
    sample_size: int = 100,
    threshold: float = 0.8,
) -> typing.Tuple[pd.DataFrame, typing.Dict[str, typing.Any]]:
    """
    Detect and convert date/datetime columns in a DataFrame.

    Uses sampling for performance. Returns the updated DataFrame and a
    metadata dict with inference details per column.

    Parameters
    ----------
    df : pd.DataFrame
    sample_size : int
        Number of rows to sample when testing format compliance.
    threshold : float
        Minimum fraction of parsed values required to accept a column as temporal.

    Returns
    -------
    (pd.DataFrame, dict)
        Updated DataFrame with converted columns + metadata per column.
    """
    COMMON_FORMATS = [
        "%Y-%m-%d",
        "%d-%m-%Y",
        "%m-%d-%Y",
        "%Y/%m/%d",
        "%d/%m/%Y",
        "%m/%d/%Y",
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d %H:%M",
        "%d-%m-%Y %H:%M:%S",
        "%m/%d/%Y %H:%M:%S",
    ]

    metadata: typing.Dict[str, typing.Any] = {}
    df_out = df.copy()

    for col in df.columns:
        if not (
            pd.api.types.is_object_dtype(df[col])
            or pd.api.types.is_string_dtype(df[col])
        ):
            continue

        series = df[col].dropna().astype(str)
        if series.empty:
            continue

        sample = series.head(sample_size)
        best_format: typing.Optional[str] = None
        best_score = 0.0

        for fmt in COMMON_FORMATS:
            success = sum(
                1
                for val in sample
                if _try_strptime(val, fmt)
            )
            score = success / len(sample)
            if score > best_score:
                best_score = score
                best_format = fmt

        if best_score >= threshold:
            parsed = pd.to_datetime(df[col], format=best_format, errors="coerce")
            used_format = best_format
        else:
            parsed = pd.to_datetime(df[col], errors="coerce")
            used_format = None

        confidence = float(parsed.notna().mean())
        if confidence < threshold:
            continue

        has_time = (parsed.dt.time != pd.Timestamp("00:00:00").time()).any()
        col_type = "datetime" if has_time else "date"
        df_out[col] = parsed

        metadata[col] = {
            "semantic_type": "temporal",
            "granularity": col_type,
            "format": used_format,
            "confidence": confidence,
        }
        _LOG.info(
            "Column '%s' detected as %s (format=%s, confidence=%.2f)",
            col,
            col_type,
            used_format,
            confidence,
        )

    return df_out, metadata


def _try_strptime(val: str, fmt: str) -> bool:
    """Return True if val parses under fmt, False otherwise."""
    try:
        datetime.datetime.strptime(val, fmt)
        return True
    except Exception:  # pylint: disable=broad-exception-caught
        return False


# =============================================================================
# Stats computation
# =============================================================================


def compute_llm_agent_stats(
    tag_to_df: typing.Dict[str, pd.DataFrame],
    categorical_cols_map: typing.Optional[typing.Dict[str, typing.List[str]]] = None,
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
            _LOG.warning("No numeric columns in '%s'; skipping quality report", tag)
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
                print(f"\n=== Distribution: {tag} / {col} ===\n", dist.to_string())

    # 4. Numeric summary (customisable metric subset)
    dataframe_stats["numeric_summary"] = {}
    for tag, df in tag_to_df.items():
        numeric_df = df.select_dtypes(include="number")
        if numeric_df.empty:
            continue
        full_summary = numeric_df.describe().T
        available = [m for m in metrics if m in full_summary.columns]
        if not available:
            _LOG.warning("None of the requested metrics %s are available.", metrics)
        summary = full_summary[available].copy()
        if "50%" in summary.columns:
            summary = summary.rename(columns={"50%": "median"})
        dataframe_stats["numeric_summary"][tag] = summary
        print(f"\n=== Numeric Summary: {tag} ===\n", summary.to_string())

    return dataframe_stats


def _resolve_metrics(metrics: typing.Optional[typing.List[str]]) -> typing.List[str]:
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


# =============================================================================
# LLM scope filtering
# =============================================================================


def _select_columns_for_llm(
    df: pd.DataFrame,
    scope: str,
    null_threshold: float = 0.05,
) -> typing.List[str]:
    """
    Return the list of column names that should be sent to the LLM.

    Parameters
    ----------
    df : pd.DataFrame
    scope : str
        "all"      — every column
        "semantic" — non-numeric columns only (object / category / string)
        "nulls"    — columns with null fraction above null_threshold
    null_threshold : float
        Fraction of nulls required for "nulls" scope. Default 5 %.

    Returns
    -------
    list of str
    """
    if scope == "all":
        return list(df.columns)

    if scope == "semantic":
        cols = df.select_dtypes(
            include=["object", "category", "string"]
        ).columns.tolist()
        _LOG.info("LLM scope='semantic': %d columns selected.", len(cols))
        return cols

    if scope == "nulls":
        cols = [
            col
            for col in df.columns
            if df[col].isnull().mean() > null_threshold
        ]
        _LOG.info(
            "LLM scope='nulls' (threshold=%.0f%%): %d columns selected.",
            null_threshold * 100,
            len(cols),
        )
        return cols

    _LOG.warning("Unknown LLM scope '%s'; falling back to 'all'.", scope)
    return list(df.columns)


# =============================================================================
# Prompt building
# =============================================================================


def build_llm_prompt(
    stats: typing.Dict[str, typing.Any],
    columns_to_include: typing.Optional[typing.List[str]] = None,
) -> str:
    """
    Serialize statistical data into a structured string prompt for LLM consumption.

    Parameters
    ----------
    stats : dict
        Output of compute_llm_agent_stats().
    columns_to_include : list of str, optional
        Subset of column names to include in the prompt. None = all.

    Returns
    -------
    str
    """
    prompt_segments = [
        "You are a Senior Data Scientist and Domain Expert.",
        "Analyze the provided dataset statistics and generate a profile for each column.",
        "For each column, provide 2-3 testable hypotheses.",
        "Example: 'Higher discount rates correlate with higher volume but lower margins.'",
        "\n--- DATASET STATISTICS ---",
    ]

    if "datetime_columns" in stats and stats["datetime_columns"]:
        prompt_segments.append(
            f"\nDetected Datetime Columns:\n"
            f"{json.dumps(stats['datetime_columns'], indent=2)}"
        )

    if "numeric_summary" in stats:
        for tag, summary_df in stats["numeric_summary"].items():
            if columns_to_include is not None:
                summary_df = summary_df[
                    summary_df.index.isin(columns_to_include)
                ]
            prompt_segments.append(
                f"\nDataset [{tag}] Numeric Summary:\n{summary_df.to_string()}"
            )

    if "categorical_distributions" in stats:
        for tag, cols in stats["categorical_distributions"].items():
            for col_name, dist in cols.items():
                if columns_to_include is not None and col_name not in columns_to_include:
                    continue
                prompt_segments.append(
                    f"\nDistribution for [{col_name}]:\n{dist.to_string()}"
                )

    return "\n".join(prompt_segments)


# =============================================================================
# LLM calls
# =============================================================================


def generate_hypotheses_via_cli(
    stats: typing.Dict[str, typing.Any],
    model: str = "gpt-4o",
    columns_to_include: typing.Optional[typing.List[str]] = None,
) -> typing.Dict[str, typing.Any]:
    """
    Generate insights and hypotheses using internal hllmcli logic.

    Parses and Pydantic-validates the LLM response against DatasetInsights.

    Parameters
    ----------
    stats : dict
    model : str
    columns_to_include : list of str, optional
        If provided, only these columns are sent to the LLM (cost control).

    Returns
    -------
    dict  — DatasetInsights-shaped dict, or {"error": ...} on failure.
    """
    _LOG.info("Generating hypotheses via hllmcli (model=%s)...", model)

    schema_json = DatasetInsights.model_json_schema()
    user_prompt = build_llm_prompt(stats, columns_to_include=columns_to_include)
    system_prompt = (
        "You are a Senior Data Scientist. Analyze the following data statistics.\n"
        "Generate a set of 2-3 predictive or causal hypotheses for EVERY column.\n"
        f"Return the output strictly in JSON matching this schema:\n"
        f"{json.dumps(schema_json)}"
    )

    try:
        response_text, cost = hllmcli.apply_llm(
            input_str=user_prompt,
            system_prompt=system_prompt,
            model=model,
            use_llm_executable=False,
        )
        _LOG.info("LLM call successful. Estimated cost: $%.6f", cost)

        cleaned = (
            response_text.strip()
            .removeprefix("```json")
            .removesuffix("```")
            .strip()
        )
        raw = json.loads(cleaned)

        # Pydantic validation — raises ValidationError on schema mismatch.
        validated = DatasetInsights.model_validate(raw)
        return validated.model_dump()

    except pydantic.ValidationError as e:
        _LOG.error("LLM output failed Pydantic validation: %s", e)
        return {"error": str(e)}
    except json.JSONDecodeError as e:
        _LOG.error("LLM returned invalid JSON: %s", e)
        return {"error": f"JSON parse error: {e}"}
    except Exception as e:  # pylint: disable=broad-exception-caught
        _LOG.error("hllmcli call failed: %s", e)
        return {"error": str(e)}


def get_llm_semantic_insights_langchain(
    prompt_text: str,
    model: str = "gpt-4o",
) -> typing.Dict[str, typing.Any]:
    """
    Process dataset metadata via LangChain to extract structured semantic insights.

    Uses JsonOutputParser alongside the Pydantic schema. Validates output.

    Parameters
    ----------
    prompt_text : str
        Serialized stats from build_llm_prompt().
    model : str

    Returns
    -------
    dict
    """
    _LOG.info("Querying LLM via LangChain (%s)...", model)
    llm = lco.ChatOpenAI(model=model, temperature=0)
    parser = lcop.JsonOutputParser(pydantic_object=DatasetInsights)

    prompt = lcpr.ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a Senior Data Scientist. Answer in JSON format.\n"
                "{format_instructions}",
            ),
            ("user", "{metadata_stats}"),
        ]
    ).partial(format_instructions=parser.get_format_instructions())

    chain = prompt | llm | parser
    try:
        result = chain.invoke({"metadata_stats": prompt_text})
        # Validate against Pydantic schema.
        validated = DatasetInsights.model_validate(result)
        return validated.model_dump()
    except pydantic.ValidationError as e:
        _LOG.error("LangChain output failed Pydantic validation: %s", e)
        return {"error": str(e)}
    except Exception as e:  # pylint: disable=broad-exception-caught
        _LOG.error("LangChain invocation failed: %s", e)
        return {"error": str(e)}


# =============================================================================
# Column profiles
# =============================================================================


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


# =============================================================================
# Export helpers
# =============================================================================


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


# =============================================================================
# Pipeline
# =============================================================================


def run_pipeline(
    csv_paths: typing.List[str],
    tags: typing.Optional[typing.List[str]] = None,
    model: str = "gpt-4o",
    metrics: typing.Optional[typing.List[str]] = None,
    llm_scope: str = "all",
    output_json: str = "data_profile_report.json",
    output_md: str = "data_profile_summary.md",
    use_langchain: bool = False,
) -> typing.Tuple[typing.Dict[str, pd.DataFrame], typing.Dict[str, typing.Any]]:
    """
    Execute the full data profiling pipeline over one or more CSV files.

    Parameters
    ----------
    csv_paths : list of str
        One or more CSV file paths to profile.
    tags : list of str, optional
        Human-readable tag for each CSV. Defaults to filename stems.
    model : str
        LLM model name passed to OpenAI / hllmcli.
    metrics : list of str, optional
        Numeric metrics to include. Defaults to DEFAULT_METRICS.
    llm_scope : str
        "all", "semantic", or "nulls" — controls which columns are LLM-profiled.
    output_json : str
        Path for the merged JSON report.
    output_md : str
        Path for the Markdown summary.
    use_langchain : bool
        Use LangChain chain instead of hllmcli for LLM calls.

    Returns
    -------
    (dict of tag → df, stats dict)
    """
    if tags is None:
        tags = [os.path.splitext(os.path.basename(p))[0] for p in csv_paths]

    if len(tags) != len(csv_paths):
        raise ValueError(
            f"Length of tags ({len(tags)}) must match csv_paths ({len(csv_paths)})."
        )

    # --- Load & type-coerce ---
    tag_to_df: typing.Dict[str, pd.DataFrame] = {}
    for path, tag in zip(csv_paths, tags):
        df = load_csv(path)
        df = hpanconv.convert_df(df)
        df, datetime_meta_partial = infer_and_convert_datetime_columns(df)
        tag_to_df[tag] = df

    # Merge datetime metadata across all DataFrames (using the last loaded tag
    # as the primary df for single-dataset runs; full merge for multi).
    _, datetime_meta = infer_and_convert_datetime_columns(
        pd.concat(list(tag_to_df.values()), axis=0, ignore_index=True)
    )

    # --- Categorical column map ---
    cat_cols_map: typing.Dict[str, typing.List[str]] = {
        tag: df.select_dtypes(
            include=["object", "category", "string"]
        ).columns.tolist()
        for tag, df in tag_to_df.items()
    }

    # --- Compute stats ---
    stats = compute_llm_agent_stats(
        tag_to_df,
        categorical_cols_map=cat_cols_map,
        metrics=metrics,
    )
    stats["datetime_columns"] = datetime_meta

    # --- LLM scope ---
    # Use the concatenated DataFrame to decide which columns to send.
    combined_df = pd.concat(list(tag_to_df.values()), axis=0, ignore_index=True)
    columns_for_llm = _select_columns_for_llm(combined_df, scope=llm_scope)
    _LOG.info(
        "LLM will profile %d / %d columns (scope=%s).",
        len(columns_for_llm),
        len(combined_df.columns),
        llm_scope,
    )

    # --- LLM call ---
    if use_langchain:
        prompt_text = build_llm_prompt(stats, columns_to_include=columns_for_llm)
        semantic_insights = get_llm_semantic_insights_langchain(
            prompt_text, model=model
        )
    else:
        semantic_insights = generate_hypotheses_via_cli(
            stats,
            model=model,
            columns_to_include=columns_for_llm,
        )

    # --- Build column profiles (use first / primary df for column ordering) ---
    primary_df = list(tag_to_df.values())[0]
    column_profiles = build_column_profiles(
        df=primary_df,
        stats=stats,
        insights=semantic_insights,
    )

    # --- Export ---
    merge_and_export_results(
        stats=stats,
        insights=semantic_insights,
        column_profiles=column_profiles,
        output_path=output_json,
    )
    export_markdown_from_profiles(
        column_profiles,
        numeric_stats=stats.get("numeric_summary", {}),
        output_path=output_md,
    )

    return tag_to_df, stats


# =============================================================================
# CLI
# =============================================================================


def _build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="schema_agent_utils",
        description="Data Profiler Agent — statistical + LLM column profiling",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    # --- Inputs ---
    parser.add_argument(
        "csv_paths",
        nargs="+",
        metavar="CSV",
        help="One or more CSV file paths to profile.",
    )
    parser.add_argument(
        "--tags",
        nargs="+",
        metavar="TAG",
        help="Human-readable tag for each CSV (must match number of csv_paths).",
    )

    # --- LLM options ---
    parser.add_argument(
        "--model",
        default="gpt-4o",
        help="LLM model for semantic analysis.",
    )
    parser.add_argument(
        "--llm-scope",
        choices=["all", "semantic", "nulls"],
        default="all",
        dest="llm_scope",
        help=(
            "Which columns to send to the LLM. "
            "'all'=every column, 'semantic'=non-numeric only, "
            "'nulls'=high-null columns only (saves cost)."
        ),
    )
    parser.add_argument(
        "--use-langchain",
        action="store_true",
        dest="use_langchain",
        help="Use LangChain pipeline instead of hllmcli for LLM calls.",
    )

    # --- Stat options ---
    parser.add_argument(
        "--metrics",
        nargs="+",
        choices=VALID_METRICS,
        default=None,
        metavar="METRIC",
        help=(
            f"Numeric metrics to include in the summary. "
            f"Valid: {', '.join(VALID_METRICS)}. "
            f"Default: {', '.join(DEFAULT_METRICS)}."
        ),
    )

    # --- Output options ---
    parser.add_argument(
        "--output-json",
        default="data_profile_report.json",
        dest="output_json",
        metavar="PATH",
        help="Output path for the merged JSON report.",
    )
    parser.add_argument(
        "--output-md",
        default="data_profile_summary.md",
        dest="output_md",
        metavar="PATH",
        help="Output path for the Markdown summary.",
    )

    return parser


def main() -> None:
    """
    CLI entry point. Parses arguments and delegates to run_pipeline().
    """
    parser = _build_arg_parser()
    args = parser.parse_args()

    run_pipeline(
        csv_paths=args.csv_paths,
        tags=args.tags,
        model=args.model,
        metrics=args.metrics,
        llm_scope=args.llm_scope,
        output_json=args.output_json,
        output_md=args.output_md,
        use_langchain=args.use_langchain,
    )


if __name__ == "__main__":
    main()