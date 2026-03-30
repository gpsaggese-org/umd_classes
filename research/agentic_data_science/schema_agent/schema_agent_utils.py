import helpers.hpandas_conversion as hpandas_conversion
import helpers.hpandas_stats as hpanstat
import helpers.hpandas_io as hpanio
import helpers.hlogging as hloggin

import pandas as pd
import typing


_LOG = hloggin.getLogger(__name__)

def load_employee_data(csv_path: str) -> pd.DataFrame:
    """
    Load employee data from CSV. Raises FileNotFoundError if the file does not exist.
    """
    try:
        df = hpanio.read_csv_to_df(csv_path)
    except FileNotFoundError:
        _LOG.error("CSV not found at '%s'.", csv_path)
        raise
    return df

def compute_llm_agent_stats(
    tag_to_df: typing.Dict[str, pd.DataFrame],
    categorical_cols_map: typing.Optional[typing.Dict[str, typing.List[str]]] = None,
) -> typing.Dict[str, typing.Any]:
    """
    Computes a comprehensive statistical profile of dataframes for LLM context.
    Produces: temporal boundaries, data quality (zeros/nans/infs), categorical
    distributions, and a numeric summary — all formatted for LLM prompt injection.
    """
    dataframe_stats: typing.Dict[str, typing.Any] = {}

    # 1. Temporal boundaries
    try:
        duration_stats, _ = hpanstat.compute_duration_df(tag_to_df)
        dataframe_stats["temporal_boundaries"] = duration_stats
        print("\n=== Temporal Boundaries ===")
        print(duration_stats.to_string())
    except Exception as e:
        _LOG.warning("Skipping duration stats: %s", e)
        dataframe_stats["temporal_boundaries"] = None

    # 2. Data quality profiling (zeros / nans / infs)
    dataframe_stats["quality_reports"] = {}
    for tag, df in tag_to_df.items():
        # Only numeric columns — report_zero_nan_inf_stats uses np.isnan/isinf
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
                as_txt=True,        # plain text — avoids IPython display entirely
            )
            dataframe_stats["quality_reports"][tag] = quality
            print(f"\n=== Quality Report: {tag} ===")
            print(quality.to_string())
        except Exception as e:
            _LOG.warning("Quality report failed for '%s': %s", tag, e)

    # 3. Categorical distributions
    dataframe_stats["categorical_distributions"] = {}
    if categorical_cols_map:
        for tag, cols in categorical_cols_map.items():
            if tag not in tag_to_df:
                continue
            dataframe_stats["categorical_distributions"][tag] = {}
            for col in cols:
                if col in tag_to_df[tag].columns:
                    dist = hpanstat.get_value_counts_stats_df(tag_to_df[tag], col)
                    dataframe_stats["categorical_distributions"][tag][col] = dist
                    print(f"\n=== Distribution: {tag} / {col} ===")
                    print(dist.to_string())

    # 4. Numeric summary (mean / std / min / max / median)
    dataframe_stats["numeric_summary"] = {}
    for tag, df in tag_to_df.items():
        numeric_df = df.select_dtypes(include="number")
        if not numeric_df.empty:
            summary = numeric_df.describe().T[["mean", "std", "min", "50%", "max"]]
            summary.rename(columns={"50%": "median"}, inplace=True)
            dataframe_stats["numeric_summary"][tag] = summary
            print(f"\n=== Numeric Summary: {tag} ===")
            print(summary.to_string())

    return dataframe_stats

def main():
    df = load_employee_data("global_ecommerce_forecasting.csv")

    # Dynamically convert datetime-like columns and set best index

    df_typed = hpandas_conversion.convert_df(df)
    # df = convert_flexible_datetime(df)
    
    print(df_typed.dtypes)
    # Select categorical columns excluding datetime
    categorical_cols = df_typed.select_dtypes(include=["object", "category"]).columns.tolist()

    stats = compute_llm_agent_stats(
        {"ecommerce_data": df_typed},
        categorical_cols_map={"ecommerce_data": categorical_cols},
    )


    print(df_typed.head())
    return df_typed, stats

if __name__ == "__main__":
    main()