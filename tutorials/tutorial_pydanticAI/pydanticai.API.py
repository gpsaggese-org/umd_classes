# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.19.1
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %%
# %load_ext autoreload
# %autoreload 2

# System libraries.
import logging

# Third party libraries.
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Common plotting and dataframe libraries are loaded for notebook exploration.

# %%
# System libraries.
import asyncio
import os

# Third party libraries.
from dataclasses import dataclass

import nest_asyncio
from dotenv import find_dotenv, load_dotenv
from pydantic import BaseModel
from pydantic_ai import Agent

# Local utilities.
import pydanticai_API_utils as utils

# Notebook-specific imports are ready for tutorial examples.

# %%
# Configure notebook logging.
import logging

# Local utility.
import pydanticai_API_utils as utils

_LOG = logging.getLogger(__name__)
utils.init_logger(_LOG)
_LOG.info("Notebook logger initialized.")
# Notebook and utility logs now print in Jupyter.

# %% [markdown]
# # Summary
#
# This notebook introduces `PydanticAI` APIs for building LLM workflows.
#
# Topics include structured outputs, tools, dependencies, validators, streaming,
# provider configuration, run metadata, and usage limits.

# %% [markdown]
# # PydanticAI API Tutorial Introduction
#
# `PydanticAI` is a lightweight framework for building LLM-powered applications
# with structured outputs using `Pydantic` models.
#
# Unlike traditional LLM APIs that return unstructured text, `PydanticAI`
# ensures responses conform to a predefined schema.

# %% [markdown]
# ## Why PydanticAI Exists
#
# Key problem: LLMs typically return unstructured text.
#
# Example prompt:
#
# "Extract product information from this description"
#
# Example LLM output:
#
# "The product is an iPhone 15 priced at $999."
#
# This output is difficult to use programmatically.
#
# Desired structured output:
#
# ```json
# {
#   "product_name": "iPhone 15",
#   "price": 999
# }
# ```
#
# `PydanticAI` solves this problem by:
#
# - Defining schemas using Pydantic models
# - Enforcing structured outputs
# - Automatically retrying when validation fails
# - Providing a simple agent abstraction for LLM interaction

# %% [markdown]
# ## Mental Model
#
# ```text
# User Prompt
#      v
# PydanticAI Agent
#      v
# LLM
#      v
# Raw Response
#      v
# Pydantic Validation
#      v
# Structured Output
# ```

# %%
# Load environment variables from a local dotenv file if one exists.
env_path = find_dotenv(usecwd=True)
load_dotenv(env_path, override=True)
_LOG.info("dotenv path: %s", env_path or "<not found>")
env_path or "<not found>"
# Environment variables are available to the model configuration cells.

# %%
# Read the model identifier from the environment.
MODEL_ID = os.getenv("PYDANTIC_AI_MODEL")
utils.log_environment(env_path, MODEL_ID)
{"model_id": MODEL_ID}
# The tutorial examples will use the configured model identifier.

# %% [markdown]
# # Core Concepts
#
# PydanticAI revolves around a few important abstractions.
#
# ## Agent
#
# The `Agent` is the main interface for interacting with the model.
#
# It manages:
#
# - LLM calls
# - structured outputs
# - retries
# - tool usage
#
# ## output_type
#
# Defines the expected structured output.
#
# This must be a Pydantic model.
#
# ## Tools
#
# Functions that the agent can call during reasoning.
#
# Tools allow agents to interact with external systems such as APIs or databases.
#
#

# %% [markdown]
# # Minimal Example
#
# The quickest way to understand PydanticAI is through a small example.
#
# We define a schema using Pydantic and instruct the agent to produce that structured output.

# %%
# Define the output schema for the minimal example.
class City(BaseModel):
    name: str
    country: str
    population: int


City
# The schema defines the exact output shape expected from the model.


# %%
# Create an agent that must return `City`.
agent = Agent(MODEL_ID, output_type=City)
agent
# The agent is configured to validate model output against class `City`.

# %%
# Run the minimal example agent.
result = agent.run_sync("Tell me about Paris")

result.output
# The result is a validated `City` object.

# %% [markdown]
# # Resolving the RuntimeError in Jupyter

# %% [markdown]
# Key thing to remember: Jupyter already runs an active event loop.
#
# - `agent.run_sync()` can raise a `RuntimeError` in notebook environments
# - `nest_asyncio` patches the notebook event loop so nested async execution can work
# - After applying `nest_asyncio`, the async `PydanticAI` examples can run inside cells

# %%
# Enable nested event loops for notebook execution.
nest_asyncio.apply()
_LOG.info("Nested event loop support enabled.")
# Async PydanticAI examples can now run from notebook cells.

# %% [markdown]
# Now try running the previous cell that had the error.

# %% [markdown]
# # Structured Outputs with Pydantic
#
# `PydanticAI` turns LLM responses into structured data.
#
# - Store validated outputs in databases
# - Feed typed objects into analytics
# - Pass structured data downstream without brittle string parsing

# %%
# Define a product schema for structured extraction.
class Product(BaseModel):
    name: str
    price: float
    category: str


Product
# The schema captures the product fields we want to extract.


# %%
# Create an agent that must return `Product`.
agent = Agent(MODEL_ID, output_type=Product)
agent
# The agent is configured to return product data with typed fields.

# %%
# Ask the model for structured product information.
agent.run_sync("Describe the Apple AirPods Pro").output
# The response is validated as a `Product` class object.

# %% [markdown]
# # Validation and Retries
#
# Real LLM outputs are inconsistent.
#
# - Schema validation checks the generated structure
# - Retries let `PydanticAI` ask the model to repair invalid output
# - The notebook avoids custom parsing and retry logic in each prompt

# %%
# Define a schema that requires an integer age.
class Person(BaseModel):
    name: str
    age: int


Person
# The schema enforces integer typing for age values.


# %%
# Configure retries so schema validation failures can be corrected.
agent = Agent(MODEL_ID, output_type=Person, retries=2)
agent
# The agent can retry when model output does not match `Person`.

# %%
# Run the retry-enabled agent.
agent.run_sync("Tell me about Albert Einstein")
# The result is a validated `Person` run result.

# %% [markdown]
# # Tools
#
# Agents can call Python functions as tools.
#
# - Tools let the model interact with real functions and external systems
# - Tools are useful for APIs, databases, calculations, and deterministic helpers
# - Tool calls reduce the chance that the model invents facts

# %%
# Create an agent with a deterministic weather tool.
agent = Agent(MODEL_ID, tools=[utils.get_weather])
agent
# The agent can call `utils.get_weather()` while answering.

# %%
# Ask a question that should use the weather tool.
agent.run_sync("What is the weather in Tokyo?")
# The run result includes the tool-backed weather answer.

# %% [markdown]
# # Dependencies
#
# Dependencies inject runtime context into agents and tools.
#
# - Example values: tenant IDs, API clients, feature flags, and environment context
# - Benefit: tools can access context without global variables or prompt string formatting

# %%
# Define the dependency object passed into the agent at run time.
@dataclass
class Config:
    company: str


Config
# The dependency schema describes runtime context available to tools.


# %%
# Create an agent that receives `Config` dependencies.
# `deps_type=Config` declares the shape of runtime context the agent can receive.
agent = Agent(MODEL_ID, deps_type=Config, tools=[utils.company_name])
agent
# Tools can access `Config` through the PydanticAI run context.

# %%
# Run the dependency-aware agent with a concrete configuration.
result = agent.run_sync(
    "What company is configured?", deps=Config(company="OpenAI")
)
result.output
# The answer reflects the runtime dependency value.

# %% [markdown]
# # Advanced API Features
#
# The following sections demonstrate more advanced capabilities of PydanticAI.
#
# These features are useful when building production-grade systems:
#
# - custom validation
# - streaming outputs
# - model configuration
# - usage tracking
# - runtime limits
#
# Beginners can safely skip this section on a first read.

# %% [markdown]
# # Result Validators
#
# Result validators allow you to enforce additional rules on model outputs.
#
# Even if the response matches the Pydantic schema, we may still want to verify
# logical constraints.
#
# Example: if an answer claims to use documents, it must include at least one source.

# %% [markdown]
# ## Validation Flow
#
# In this section, validation happens in two stages:
#
# 1. `Schema validation`: the model output must match `AnswerWithSources`.
# 2. `Business-rule validation`: the registered `output_validator` enforces
#    citation quality rules that schema alone cannot enforce.
#
# Execution order:
#
# ```text
# model output -> Pydantic schema validation -> output_validator -> final result
# ```

# %%
# Define source citation schemas for validator examples.
class SourceRef(BaseModel):
    doc_id: str
    quote: str


class AnswerWithSources(BaseModel):
    answer: str
    sources: list[SourceRef]


AnswerWithSources
# The schemas describe answers that include source citations.

# %%
# Build validator instructions from local document ids.
available_doc_ids = utils.get_available_document_ids()
validator_instructions = (
    "Use the search_documents tool to retrieve evidence from local documents. "
    f"Cite only these doc ids: {available_doc_ids}. "
    "For each source, copy the quote text exactly from tool output."
)
{
    "available_doc_ids": available_doc_ids,
    "validator_instruction_length": len(validator_instructions),
}
# The instructions constrain citations to the local document ids.

# %%
# Create an agent that returns answers with source references.
validator_agent = Agent(
    MODEL_ID,
    output_type=AnswerWithSources,
    instructions=validator_instructions,
    tools=[utils.search_documents],
)
validator_agent
# The validator agent can retrieve documents and return cited answers.


# %%
# Register a result validator that checks citations against local documents.
@validator_agent.output_validator
def validate_output(
    result: AnswerWithSources,
) -> AnswerWithSources:
    result = utils.validate_document_sources(result)
    return result


{"validator_registered": True}
# The validator agent now enforces schema and source-reference rules.


# %% [markdown]
# ## What `@validator_agent.output_validator` Does
#
# The `@validator_agent.output_validator` decorator registers a post-processing
# validator for this specific agent.
#
# The validator receives the already schema-validated `AnswerWithSources` object.
# Then the validator calls `utils.validate_document_sources(...)` to enforce:
#
# - Source list required when answer claims document-backed statements
# - Maximum number of sources
# - No duplicate `(doc_id, quote)` pairs
# - Each `doc_id` must exist in the local dataset
# - Each `quote` must appear in the cited document

# %% [markdown]
# ## Why `ModelRetry` Is Important
#
# When a rule is violated, the validator raises `ModelRetry`.
#
# `ModelRetry` tells `PydanticAI` to ask the model for another attempt instead
# of accepting bad output.
#
# ## Why `available_doc_ids` Is Included in Instructions
#
# `available_doc_ids` constrains citations to known local documents.
#
# - Reduces hallucinated references
# - Gives the model a concrete allowed set of document identifiers

# %% [markdown]
# ## Purpose of the Manual Failure Cell
#
# The manual failure example builds the same retry object used by the validator path.
#
# - Bypasses the model call
# - Shows the retry message used when citation requirements are not met
# - Keeps the notebook executable without intentionally raising an exception

# %%
# Build the retry exception used by the missing-sources validator path.
retry = utils.build_missing_sources_retry()
_LOG.info("Validator failure example: %s", retry)
retry
# The retry object shows the message returned when sources are missing.

# %%
# Run the validator example through the async API helper.
asyncio.run(utils.run_validator_example(validator_agent))
# The output has passed both Pydantic schema validation and custom validation.

# %% [markdown]
# # Streaming
#
# Streaming returns tokens as the model generates them.
#
# Benefits:
#
# - lower perceived latency
# - better user experience in chat interfaces
# - progressive display of responses

# %%
# Create an agent for the streaming example.
stream_agent = Agent(
    MODEL_ID, instructions="Write one short paragraph about unit tests."
)
stream_agent
# The streaming agent is ready to produce incremental text.

# %%
# Run the streaming helper and return the final result.
asyncio.run(utils.run_streaming_demo(stream_agent))
# The helper logs streamed text and returns the final result.

# %% [markdown]
# # Provider Configuration
#
# Model objects let you configure providers directly, such as base URLs.
#
# Use an explicit model object when provider-specific options, such as `base_url`, are needed.
#

# %%
# Build an explicit provider model object when the installed API supports it.
explicit_model = utils.build_explicit_openai_model(MODEL_ID)
if explicit_model is None:
    _LOG.info("Explicit model unavailable; using string model ID.")
else:
    _LOG.info("Using explicit model object.")
{"explicit_model_available": explicit_model is not None}
# Provider configuration is either explicit or falls back to `MODEL_ID`.

# %%
# Run an agent with the explicit provider model when available.
agent = Agent(explicit_model or MODEL_ID, instructions="Be concise.")
result = asyncio.run(agent.run("Say hello in one sentence."))
result
# The result confirms that the provider configuration can execute a request.


# %% [markdown]
# # AgentRun
#
# AgentRun objects contain metadata about an agent execution.
#
# This includes:
#
# - token usage
# - message history
# - tool calls
# - final output
#
# Run metadata helps debug and control agents.
#
# - Observability: inspect messages and tool calls
# - Cost tracking: inspect token usage
# - Governance: keep execution details available for review

# %%
# Run an agent and collect execution metadata.
meta_agent = Agent(MODEL_ID, instructions="Answer in one sentence.")
result = asyncio.run(meta_agent.run("What is a unit test?"))
usage = getattr(result, "usage", None)
message_count = len(result.new_messages())
run_metadata = {
    "output": result.output,
    "messages_new": message_count,
    "usage": usage,
}
run_metadata
# The metadata summarizes output, message count, and usage details.


# %% [markdown]
# # Usage Limits and Model Settings
#
# Usage limits help control:
#
# - API cost
# - runaway loops
# - excessive token usage
#
# `PydanticAI` supports safety and cost controls for production LLM systems.

# %%
# Load version-tolerant classes for model settings and usage limits.
ModelSettings, UsageLimits = utils.get_settings_classes()
_LOG.info("Loaded ModelSettings and UsageLimits classes.")
{
    "model_settings_class": ModelSettings.__name__,
    "usage_limits_class": UsageLimits.__name__,
}
# The installed PydanticAI version determines where these classes come from.


# %%
# Create an agent with deterministic model settings.
settings_agent = Agent(
    MODEL_ID,
    instructions="Answer in a single sentence.",
    model_settings=ModelSettings(temperature=0.2),
)
settings_agent
# The agent has a low-temperature model setting.

# %%
# Run the settings example with a request limit.
result = asyncio.run(
    settings_agent.run(
        "Explain what unit tests are.",
        usage_limits=UsageLimits(request_limit=3),
    )
)

result.output
# The response was generated with model settings and usage limits applied.

# %% [markdown]
# # Troubleshooting
# - Missing API key: set `OPENAI_API_KEY` (or your provider-specific key).
# - Event loop errors in notebooks: use `await agent.run(...)` instead of `run_sync`.
# - Validation errors: revise `output_type` or the validator to match expected output.
#
