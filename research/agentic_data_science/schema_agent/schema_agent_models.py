"""
Pydantic schemas for data profiling agent.

Provides type-safe structures for column insights and dataset metadata.

Import as:

import research.agentic_data_science.schema_agent.schema_agent_models as radsasam
"""

import typing

import pydantic


# #############################################################################
# ColumnInsight
# #############################################################################


class ColumnInsight(pydantic.BaseModel):
    """
    Semantic insight for a single column.
    """

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
    """
    Complete semantic insights for all columns in a dataset.
    """

    columns: typing.Dict[str, ColumnInsight]
