"""
Import as:

import research.agentic_data_science.schema_agent.schema_agent_utils as radsasau
"""

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

# --- Configuration & Logging ---
dotenv.load_dotenv()
api_key = os.environ.get("OPENAI_API_KEY")
if not api_key:
    print("Error: OPENAI_API_KEY not found.")
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


# #############################################################################
# ColumnInsight
# #############################################################################


# --- Schemas ---
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


# #############################################################################
# DatasetInsights
# #############################################################################


class DatasetInsights(pydantic.BaseModel):
    columns: typing.Dict[str, ColumnInsight]


# --- Core Logic ---
def load_employee_data(csv_path: str) -> pd.DataFrame:
    """
    Load employee data from CSV with error handling for missing files.
    """
    try:
        return hpanio.read_csv_to_df(csv_path)
    except FileNotFoundError:
        _LOG.error("CSV not found at '%s'.", csv_path)
        raise


def compute_llm_agent_stats(
    tag_to_df: typing.Dict[str, pd.DataFrame],
    categorical_cols_map: typing.Optional[
        typing.Dict[str, typing.List[str]]
    ] = None,
) -> typing.Dict[str, typing.Any]:
    """
    Compute a statistical profile including temporal boundaries, data quality,
    categorical distributions, and numeric summaries for LLM injection.
    """
    dataframe_stats: typing.Dict[str, typing.Any] = {}

    # 1. Temporal Analysis
    try:
        duration_stats, _ = hpanstat.compute_duration_df(tag_to_df)
        dataframe_stats["temporal_boundaries"] = duration_stats
        print("\n=== Temporal Boundaries ===\n", duration_stats.to_string())
    except Exception as e:  # pylint: disable=broad-exception-caught
        _LOG.warning("Skipping duration stats: %s", e)
        dataframe_stats["temporal_boundaries"] = None

    # 2. Data Quality Profiling
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

    # 3. Categorical Distributions
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
                    print(
                        f"\n=== Distribution: {tag} / {col} ===\n",
                        dist.to_string(),
                    )

    # 4. Numeric Summary
    dataframe_stats["numeric_summary"] = {}
    for tag, df in tag_to_df.items():
        numeric_df = df.select_dtypes(include="number")
        if not numeric_df.empty:
            summary = numeric_df.describe().T[
                ["mean", "std", "min", "50%", "max"]
            ]
            summary.rename(columns={"50%": "median"}, inplace=True)
            dataframe_stats["numeric_summary"][tag] = summary
            print(f"\n=== Numeric Summary: {tag} ===\n", summary.to_string())

    return dataframe_stats


def build_llm_prompt(stats: typing.Dict[str, typing.Any]) -> str:
    """
    Serialize statistical data into a structured prompt for hypothesis
    generation.
    """
    prompt_segments = [
        "You are a Senior Data Scientist and Domain Expert.",
        "Analyze the provided dataset statistics and generate a profile for each column.",
        "For each column, provide 2-3 testable hypotheses. "
        "Example: 'Higher discount rates correlate with higher volume but lower margins.'",
        "\n--- DATASET STATISTICS ---",
    ]
    if "numeric_summary" in stats:
        for tag, summary in stats["numeric_summary"].items():
            prompt_segments.append(
                f"\nDataset [{tag}] Numeric Summary:\n{summary.to_string()}"
            )
    if "categorical_distributions" in stats:
        for tag, cols in stats["categorical_distributions"].items():
            for col_name, dist in cols.items():
                prompt_segments.append(
                    f"\nDistribution for [{col_name}]:\n{dist.to_string()}"
                )
    return "\n".join(prompt_segments)


def get_llm_semantic_insights_langchain(
    prompt_text: str, model: str = "gpt-4o"
) -> typing.Dict[str, typing.Any]:
    """
    Process dataset metadata via LangChain to extract structured semantic
    insights.
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
        return typing.cast(typing.Dict[str, typing.Any], result)
    except Exception as e:  # pylint: disable=broad-exception-caught
        _LOG.error("LangChain invocation failed: %s", e)
        return {"error": str(e)}


def merge_and_export_results(
    stats: typing.Dict[str, typing.Any],
    insights: typing.Dict[str, typing.Any],
    output_path: str = "data_profile_report.json",
) -> None:
    """
    Merge pandas statistics with LLM insights and export to a JSON report.
    """
    _LOG.info("Merging technical stats with LLM insights...")

    serializable_stats = {}
    for key, value in stats.items():
        if isinstance(value, pd.DataFrame):
            serializable_stats[key] = value.to_dict(orient="index")
        elif isinstance(value, dict):
            inner_dict = {}
            for k, v in value.items():
                inner_dict[k] = (
                    v.to_dict(orient="index")
                    if isinstance(v, pd.DataFrame)
                    else v
                )
            serializable_stats[key] = inner_dict
        else:
            serializable_stats[key] = value

    final_report = {
        "report_metadata": {"version": "1.0", "agent": "LangChain-Data-Profiler"},
        "technical_stats": serializable_stats,
        "semantic_insights": insights,
    }

    try:
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(final_report, f, indent=4, default=str)
        _LOG.info("Successfully exported merged profile to: %s", output_path)
    except Exception as e:  # pylint: disable=broad-exception-caught
        _LOG.error("Failed to export results: %s", e)


def generate_hypotheses_via_cli(
    stats: typing.Dict[str, typing.Any], model: str = "gpt-4o"
) -> typing.Dict[str, typing.Any]:
    """
    Generate insights and hypotheses using internal hllmcli logic.
    """
    _LOG.info("Generating hypotheses via hllmcli logic...")

    schema_json = DatasetInsights.model_json_schema()
    user_prompt = build_llm_prompt(stats)
    system_prompt = (
        "You are a Senior Data Scientist. Analyze the following data statistics.\n"
        "Generate a set of 2-3 predictive or causal hypotheses for EVERY column.\n"
        f"Return the output strictly in JSON matching this schema: {json.dumps(schema_json)}"
    )

    try:
        response_text, cost = hllmcli.apply_llm(
            input_str=user_prompt,
            system_prompt=system_prompt,
            model=model,
            use_llm_executable=False,
        )

        _LOG.info("LLM Call successful. Cost: $%.6f", cost)
        cleaned_response = (
            response_text.strip()
            .removeprefix("```json")
            .removesuffix("```")
            .strip()
        )
        parsed = json.loads(cleaned_response)
        return typing.cast(typing.Dict[str, typing.Any], parsed)

    except Exception as e:  
        _LOG.error("hllmcli call failed: %s", e)
        return {"error": str(e)}


def main() -> typing.Tuple[pd.DataFrame, typing.Dict[str, typing.Any]]:
    """
    Execute entry point for the data profiling pipeline.
    """
    df = hpanio.read_csv_to_df("global_ecommerce_forecasting.csv")
    df_typed = hpanconv.convert_df(df)
    cat_cols = df_typed.select_dtypes(
        include=["object", "category", "string"]
    ).columns.tolist()
    stats = compute_llm_agent_stats(
        {"ecommerce_data": df_typed},
        categorical_cols_map={"ecommerce_data": cat_cols},
    )
    semantic_insights = generate_hypotheses_via_cli(stats)
    merge_and_export_results(stats, semantic_insights)
    return df_typed, stats


if __name__ == "__main__":
    main()
