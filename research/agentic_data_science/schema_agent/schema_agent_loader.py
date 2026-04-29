"""
Data loading and preprocessing for the profiler agent.

Handles CSV loading, datetime inference, and type coercion.

Import as:

import research.agentic_data_science.schema_agent.schema_agent_loader as radsasal
"""

import datetime
import typing

import pandas as pd

import helpers.hlogging as hloggin
import helpers.hpandas_conversion as hpanconv
import helpers.hpandas_io as hpanio

_LOG = hloggin.getLogger(__name__)


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
    _LOG.info(
        "Loaded '%s': %d rows × %d columns.", csv_path, len(df), len(df.columns)
    )
    return df


# keep legacy name for backwards compatibility
load_employee_data = load_csv


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
            success = sum(1 for val in sample if _try_strptime(val, fmt))
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
    """
    Return True if val parses under fmt, False otherwise.
    """
    try:
        datetime.datetime.strptime(val, fmt)
        return True
    except Exception:  # pylint: disable=broad-exception-caught
        return False


def prepare_dataframes(
    csv_paths: typing.List[str],
    tags: typing.Optional[typing.List[str]] = None,
) -> typing.Tuple[
    typing.Dict[str, pd.DataFrame], typing.Dict[str, typing.List[str]]
]:
    """
    Load and prepare all CSV files in one pass.

    Applies type coercion, datetime inference, and categorical detection.

    Parameters
    ----------
    csv_paths : list of str
    tags : list of str, optional
        Human-readable tags; defaults to filename stems.

    Returns
    -------
    (dict of tag → df, dict of tag → categorical_columns)
    """
    tag_to_df: typing.Dict[str, pd.DataFrame] = {}
    cat_cols_map: typing.Dict[str, typing.List[str]] = {}

    for path, tag in zip(csv_paths, tags):
        df = load_csv(path)
        df = hpanconv.convert_df(df)
        df, _ = infer_and_convert_datetime_columns(df)
        tag_to_df[tag] = df

        cat_cols_map[tag] = df.select_dtypes(
            include=["object", "category", "string"]
        ).columns.tolist()

    return tag_to_df, cat_cols_map
