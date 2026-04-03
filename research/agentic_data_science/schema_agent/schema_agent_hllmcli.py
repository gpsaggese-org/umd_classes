"""
Import as:

import research.agentic_data_science.schema_agent.schema_agent_hllmcli as radsasah
"""

import json
import typing

import langchain_core.output_parsers as lcop
import langchain_core.prompts as lcpr
import langchain_openai as lco
import pydantic
import schema_agent_models as radsasam

import helpers.hllm_cli as hllmcli
import helpers.hlogging as hloggin

_LOG = hloggin.getLogger(__name__)


def _select_columns_for_llm(
    df,  # pd.DataFrame
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
            col for col in df.columns if df[col].isnull().mean() > null_threshold
        ]
        _LOG.info(
            "LLM scope='nulls' (threshold=%.0f%%): %d columns selected.",
            null_threshold * 100,
            len(cols),
        )
        return cols

    _LOG.warning("Unknown LLM scope '%s'; falling back to 'all'.", scope)
    return list(df.columns)


def build_llm_prompt(
    stats: typing.Dict[str, typing.Any],
    columns_to_include: typing.Optional[typing.List[str]] = None,
) -> str:
    """
    Serialize statistical data into a structured string prompt for LLM
    consumption.

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
                summary_df = summary_df[summary_df.index.isin(columns_to_include)]
            prompt_segments.append(
                f"\nDataset [{tag}] Numeric Summary:\n{summary_df.to_string()}"
            )

    if "categorical_distributions" in stats:
        for tag, cols in stats["categorical_distributions"].items():
            for col_name, dist in cols.items():
                if (
                    columns_to_include is not None
                    and col_name not in columns_to_include
                ):
                    continue
                prompt_segments.append(
                    f"\nDistribution for [{col_name}]:\n{dist.to_string()}"
                )

    return "\n".join(prompt_segments)


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

    schema_json = radsasam.atasetInsights.model_json_schema()
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
        validated = radsasam.DatasetInsights.model_validate(raw)
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
    Process dataset metadata via LangChain to extract structured semantic
    insights.

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
    parser = lcop.JsonOutputParser(pydantic_object=radsasam.DatasetInsights)

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
        validated = radsasam.DatasetInsights.model_validate(result)
        return validated.model_dump()
    except pydantic.ValidationError as e:
        _LOG.error("LangChain output failed Pydantic validation: %s", e)
        return {"error": str(e)}
    except Exception as e:  # pylint: disable=broad-exception-caught
        _LOG.error("LangChain invocation failed: %s", e)
        return {"error": str(e)}
