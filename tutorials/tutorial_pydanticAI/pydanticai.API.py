# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.16.4
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
from pydantic_ai import ModelRetry

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
_LOG
# Notebook logging is configured for the tutorial cells.

# %% [markdown]
# # Summary
#
# - This notebook introduces `PydanticAI` APIs for building LLM workflows, including structured outputs, tools, dependencies, validators, streaming, provider configuration, run metadata, and usage limits

# %% [markdown]
# # PydanticAI API Introduction
#
# - `PydanticAI` is a lightweight framework for building LLM-powered applications with structured outputs
# - `PydanticAI` uses `Pydantic` models to define response schemas
# - Traditional LLM APIs often return unstructured text
# - `PydanticAI` keeps responses aligned with a predefined schema

# %% [markdown]
# ## Why PydanticAI Exists
#
# - Key problem: LLMs typically return unstructured text
# - Example prompt:
#   - "Extract product information from this description"
# - Example LLM output:
#   - "The product is an iPhone 15 priced at $999."
# - Problem with the example LLM output:
#   - The example LLM output is difficult to use programmatically
# - Desired structured output:
#
#   ```json
#   {
#     "product_name": "iPhone 15",
#     "price": 999
#   }
#   ```
#
# - `PydanticAI` solves this problem with:
#   - Schema definitions with `Pydantic` models
#   - Structured output enforcement
#   - Automatic retries after validation failures
#   - A simple agent abstraction for LLM interaction

# %% [markdown]
# ## Mental Model
#
# - `PydanticAI` flow:
#   ```mermaid
#   flowchart TD
#       A[User Prompt] --> B[PydanticAI Agent]
#       B --> C[LLM]
#       C --> D[Raw Response]
#       D --> E[Pydantic Validation]
#       E --> F[Structured Output]
#   ```

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
# - `PydanticAI` revolves around a few important abstractions
#
# ## Agent
#
# - `Agent` is the main interface for interacting with the model
# - `Agent` manages:
#   - LLM calls
#   - Structured outputs
#   - Retries
#   - Tool usage
#
# ## output_type
#
# - `output_type` defines the expected structured output
# - `output_type` must be a `Pydantic` model
#
# ## Tools
#
# - Tools are functions that the agent can call during reasoning
# - Tools let agents interact with external systems such as APIs or databases
#
#

# %% [markdown]
# # Minimal Example
#
# - The quickest way to understand `PydanticAI` is a small example
# - This section defines a schema with `Pydantic` and asks the agent to produce that structured output

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
# # Resolving the Above RuntimeError in Jupyter
#
# - Key thing to remember: Jupyter already runs an active event loop

# %% [markdown]
# - `agent.run_sync()` can raise a `RuntimeError` in notebook environments
# - `nest_asyncio` patches the notebook event loop so nested async execution can work
# - After `nest_asyncio.apply()`, async `PydanticAI` examples can run inside notebook cells

# %%
# Enable nested event loops for notebook execution.
nest_asyncio.apply()
nested_event_loop_enabled = True
_LOG.info("Nested event loop support enabled.")
nested_event_loop_enabled
# Async PydanticAI examples can now run from notebook cells.

# %% [markdown]
# - Re-run the previous cell that raised the `RuntimeError`

# %% [markdown]
# # Structured Outputs with Pydantic
#
# - `PydanticAI` turns LLM responses into structured data
# - Structured outputs help you:
#   - Store validated outputs in databases
#   - Feed typed objects into analytics
#   - Pass structured data downstream without brittle string parsing

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
# - Real LLM outputs are inconsistent
# - Schema validation checks the generated structure
# - Retries let `PydanticAI` ask the model to repair invalid output
# - This notebook avoids custom parsing and retry logic in each prompt

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
# - Agents can call Python functions as tools
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
# - Dependencies inject runtime context into agents and tools
# - Example dependency values:
#   - Tenant IDs
#   - API clients
#   - Feature flags
#   - Environment context
# - Dependencies let tools access context without global variables or prompt string formatting

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
# # Advanced Features
#
# - The following sections demonstrate more advanced `PydanticAI` capabilities
# - These features are useful for production-grade systems:
#   - Custom validation
#   - Streaming outputs
#   - Model configuration
#   - Usage tracking
#   - Runtime limits
# - Beginners can safely skip this section on a first read

# %% [markdown]
# # Result Validators
#
# - Result validators are used to check model outputs after schema validation
# - `Pydantic` validates structure automatically, but result validators enforce business rules
# - A response can match the `Pydantic` schema and still fail logical constraints
# - For example, this output may be valid according to the schema:
#     - it has an `answer`
#     - it has a `sources` list
# - But it can still be logically wrong if:
#     - the source list is empty
#     - the `doc_id` does not exist
#     - the quote does not actually appear in the cited document
#
# - Result validators handle this second layer of validation

# %% [markdown]
# ## Validation Flow
#
# - Validation happens in two stages:
#   - `Schema validation`: the model output must match `AnswerWithSources`
#   - `Business-rule validation`: the registered `output_validator` enforces citation quality rules that schema alone cannot enforce
# - Execution order:
#   ```mermaid
#   flowchart LR
#       A[Model Output] --> B[Pydantic Schema Validation]
#       B --> C[output_validator]
#       C --> D[Final Result]
#   ```

# %%
# Define source citation schemas with explicit references for validator examples.
class SourceRef(BaseModel):
    doc_id: str
    quote: str


class AnswerWithSources(BaseModel):
    answer: str
    sources: list[SourceRef]


AnswerWithSources
# The schemas describe answers that include source citations.

# %% [markdown]
# ## Prepare Validation Context
#
# - We fetch the list of valid document IDs and include it in the agent instructions
# - This helps:
#     - reduce hallucinated references
#     - constrain the model to known documents

# %%
# Build validator instructions from local document ids.
available_doc_ids = utils.get_available_document_ids()
# Build instructions that restrict citations to the local dataset.
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

# %% [markdown]
# ### Create the Validator Agent
# - This agent:
#     - generates structured output
#     - retrieves documents using a tool
#     - follows constrained citation rules
#
#

# %%
# Create an agent that returns answers with source references.
# The agent uses structured output plus the local document-search tool.
validator_agent = Agent(
    MODEL_ID,
    output_type=AnswerWithSources,
    instructions=validator_instructions,
    tools=[utils.search_documents],
)
validator_agent
# The validator agent can retrieve documents and return cited answers.


# %% [markdown]
# ## Add Result Validator
#
# - The `@output_validator` runs after schema validation and enforces business rules:
#     - sources must be present
#     - document IDs must exist
#     - quotes must match source documents
#     - duplicates are not allowed
# - If validation fails, `ModelRetry` is raised, and the model is asked to generate a corrected answer.

# %%
# Register a result validator that checks citations against local documents.
@validator_agent.output_validator
def _validate_answer_sources(
    result: AnswerWithSources,
) -> AnswerWithSources:
    # Validate citations against the local document dataset.
    validated_result = utils.validate_document_sources(result)
    return validated_result


{"validator_registered": True}
# The validator agent now enforces schema and source-reference rules.


# %% [markdown]
# ## Manual Failure Example
#
# - We intentionally create an invalid output to demonstrate how the validator triggers a retry.
# - This example bypasses the model and directly tests the validator logic.

# %%
# Build an invalid answer object for the validator demo.
bad_answer = AnswerWithSources(
    answer="PydanticAI supports structured outputs.",
    sources=[],
)
bad_answer
# The invalid answer is missing source citations.

# %%
# Trigger the validator on the intentionally invalid answer.
_LOG.info("Triggering the validator with an intentionally invalid answer.")
_validate_answer_sources(bad_answer)
# The validator raises `ModelRetry` for the missing sources.

# %% [markdown]
# ## Run the Agent
#
# - The agent will:
#     - Generate structured output
#     
#     - Validate it against the schema
#     
#     - Apply business rules
#     
#     - Retry automatically if validation fails

# %%
# Run the validator agent with the local document search tool.
validator_result = asyncio.run(utils.run_validator_example(validator_agent))
validator_result
# The validator agent returns a cited answer that passed validation.

# %% [markdown]
# # Streaming
#
# - Streaming returns tokens as the model generates them
# - Streaming benefits:
#   - Lower perceived latency
#   - Better user experience in chat interfaces
#   - Progressive display of responses

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
# - Model objects let you configure providers directly, such as `base_url`
# - Use an explicit model object when provider-specific options are needed
#

# %%
# Build an explicit provider model object when the installed API supports it.
explicit_model = utils.build_explicit_openai_model(MODEL_ID)
# Log which provider configuration path is active.
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
# - `AgentRun` objects contain metadata about an agent execution
# - `AgentRun` metadata includes:
#   - Token usage
#   - Message history
#   - Tool calls
#   - Final output
# - Run metadata helps with:
#   - Observability: inspect messages and tool calls
#   - Cost tracking: inspect token usage
#   - Governance: keep execution details available for review

# %%
# Run an agent and collect execution metadata.
meta_agent = Agent(MODEL_ID, instructions="Answer in one sentence.")
result = asyncio.run(meta_agent.run("What is a unit test?"))
# Extract execution metadata that helps inspect the run.
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
# - Usage limits help control:
#   - API cost
#   - Runaway loops
#   - Excessive token usage
# - `PydanticAI` supports safety and cost controls for production LLM systems

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

# Show the constrained response text.
result.output
# The response was generated with model settings and usage limits applied.

# %% [markdown]
# # Troubleshooting
#
# - Missing API key: set `OPENAI_API_KEY` or the provider-specific key
# - Event loop errors in notebooks: use `await agent.run(...)` instead of `run_sync`
# - Validation errors: revise `output_type` or the validator to match expected output
#
