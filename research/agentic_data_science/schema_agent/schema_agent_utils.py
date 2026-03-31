import logging
import sys
import os 
import json
import typing
import pandas as pd
from openai import OpenAI
from dotenv import load_dotenv

# LangChain Imports
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field
# Internal helper imports
import helpers.hpandas_conversion as hpandas_conversion
import helpers.hpandas_stats as hpanstat
import helpers.hpandas_io as hpanio
import helpers.hlogging as hloggin
import helpers.hllm_cli as hllmcli

load_dotenv()
api_key = os.environ.get("OPENAI_API_KEY")
if not api_key:
    print("Error: OPENAI_API_KEY not found.")
    sys.exit(1)
client = OpenAI(api_key=api_key)

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
    report_cpu_usage=True
)

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
                as_txt=True,        
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

def build_llm_prompt(stats: typing.Dict[str, typing.Any]) -> str:
    """Serializes stats into a prompt block with instructions for hypothesis generation."""
    prompt_segments = [
        "You are a Senior Data Scientist and Domain Expert.",
        "Analyze the provided dataset statistics and generate a profile for each column.",
        "For each column, provide 2-3 testable hypotheses. For example, if the column is 'Discount', "
        "a hypothesis might be: 'Higher discount rates correlate with higher sales volume but lower profit margins.'",
        "\n--- DATASET STATISTICS ---"
    ]
    
    if "numeric_summary" in stats:
        for tag, summary in stats["numeric_summary"].items():
            prompt_segments.append(f"\nDataset [{tag}] Numeric Summary:\n{summary.to_string()}")
            
    if "categorical_distributions" in stats:
        for tag, cols in stats["categorical_distributions"].items():
            for col_name, dist in cols.items():
                prompt_segments.append(f"\nDistribution for [{col_name}]:\n{dist.to_string()}")
                
    return "\n".join(prompt_segments)

# --- Structured Output Schema ---
class ColumnInsight(BaseModel):
    semantic_meaning: str = Field(description="Brief description of what the data represents")
    role: str = Field(description="One of [ID, Feature, Target, Timestamp]")
    data_quality_notes: str = Field(description="Any concerns based on the stats (e.g. high nulls, outliers)")
    hypotheses: typing.List[str] = Field(
        description="A list of testable hypotheses about this column's relationship to the business outcome or target variable."
    )

class DatasetInsights(BaseModel):
    columns: typing.Dict[str, ColumnInsight]

def get_llm_semantic_insights_langchain(prompt_text: str, model: str = "gpt-4o") -> typing.Dict[str, typing.Any]:
    """
    Uses LangChain to process metadata and return structured insights.
    """
    _LOG.info("Querying LLM via LangChain (%s)...", model)
    
    # 1. Initialize the Model
    llm = ChatOpenAI(model=model, temperature=0)
    
    # 2. Set up the Parser and Prompt
    parser = JsonOutputParser(pydantic_object=DatasetInsights)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a Senior Data Scientist. Answer in JSON format.\n{format_instructions}"),
        ("user", "{metadata_stats}")
    ]).partial(format_instructions=parser.get_format_instructions())

    # 3. Create the Chain
    chain = prompt | llm | parser

    # 4. Invoke
    try:
        insights = chain.invoke({"metadata_stats": prompt_text})
        return insights
    except Exception as e:
        _LOG.error("LangChain invocation failed: %s", e)
        return {"error": str(e)}

def merge_and_export_results(
    stats: typing.Dict[str, typing.Any], 
    insights: typing.Dict[str, typing.Any],
    output_path: str = "data_profile_report.json"
):
    """
    Merges technical pandas stats with LangChain-generated semantic insights.
    
    :param stats: The dictionary returned by compute_llm_agent_stats (contains DataFrames)
    :param insights: The dictionary returned by the LangChain invocation
    :param output_path: Path to save the final JSON report
    """
    _LOG.info("Merging technical stats with LLM insights...")

    # 1. Prepare the final structure
    # We convert DataFrames to dicts/JSON-serializable formats within the 'stats' object
    serializable_stats = {}
    for key, value in stats.items():
        if isinstance(value, pd.DataFrame):
            serializable_stats[key] = value.to_dict(orient="index")
        elif isinstance(value, dict):
            # Handle nested dictionaries that might contain DataFrames (like quality_reports)
            inner_dict = {}
            for k, v in value.items():
                inner_dict[k] = v.to_dict(orient="index") if isinstance(v, pd.DataFrame) else v
            serializable_stats[key] = inner_dict
        else:
            serializable_stats[key] = value

    # 2. Combine into one master object
    final_report = {
        "report_metadata": {
            "version": "1.0",
            "agent": "LangChain-Data-Profiler"
        },
        "technical_stats": serializable_stats,
        "semantic_insights": insights
    }

    # 3. Export to JSON
    try:
        with open(output_path, "w") as f:
            json.dump(final_report, f, indent=4, default=str)
        _LOG.info("Successfully exported merged profile to: %s", output_path)
    except Exception as e:
        _LOG.error("Failed to export results: %s", e)

def generate_hypotheses_via_cli(
    stats: typing.Dict[str, typing.Any], 
    model: str = "gpt-4o"
) -> typing.Dict[str, typing.Any]:
    """
    Generates semantic insights and hypotheses using the underlying 
    logic of llm_cli (hllmcli).
    """
    _LOG.info("Generating hypotheses via hllmcli logic...")

    # 1. Prepare the Schema
    # We use Pydantic's schema to force the LLM into the correct JSON structure
    schema_json = DatasetInsights.model_json_schema()

    # 2. Build the Prompts
    user_prompt = build_llm_prompt(stats)
    
    system_prompt = (
        "You are a Senior Data Scientist. Analyze the following data statistics.\n"
        "Generate a set of 2-3 predictive or causal hypotheses for EVERY column.\n"
        f"Return the output strictly     in JSON matching this schema: {json.dumps(schema_json)}"
    )

    # 3. Call the library function used by llm_cli
    try:
        # apply_llm returns a Tuple[str, float] (response_text, cost)
        response_text, cost = hllmcli.apply_llm(
            input_str=user_prompt,
            system_prompt=system_prompt,
            model=model,
            use_llm_executable=False # Use the Python library for better error handling
        )
        
        _LOG.info("LLM Call successful. Cost: $%.6f", cost)

        # 4. Parse the result
        cleaned_response = response_text.strip().removeprefix("```json").removesuffix("```").strip()
        parsed_data = json.loads(cleaned_response)
        
        return parsed_data
        
    except Exception as e:
        _LOG.error("hllmcli call failed: %s", e)
        return {"error": str(e)}

# Update main to use the new CLI-based function if desired
def main():
    # 1. Load & Process Data
    df = hpanio.read_csv_to_df("global_ecommerce_forecasting.csv")
    df_typed = hpandas_conversion.convert_df(df)

    # 2. Compute Deterministic Stats
    cat_cols = df_typed.select_dtypes(include=["object", "category", "string"]).columns.tolist()
    stats = compute_llm_agent_stats(
        {"ecommerce_data": df_typed},
        categorical_cols_map={"ecommerce_data": cat_cols},
    )

    # 3. Call LLM via our new CLI-based helper
    semantic_insights = generate_hypotheses_via_cli(stats)

    # 4. Export
    merge_and_export_results(stats, semantic_insights)
    
    return df_typed, stats

if __name__ == "__main__":
    main()