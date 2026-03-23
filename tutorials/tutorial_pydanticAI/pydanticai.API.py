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

import logging

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

import helpers.hnotebook as ut

ut.config_notebook()

# Initialize logger.
logging.basicConfig(level=logging.INFO)
_LOG = logging.getLogger(__name__)

# %%
import pydanticai_API_utils as utils

# %% [markdown]
# ## PydanticAI API Tutorial Introduction
#
# PydanticAI is a lightweight framework for building LLM-powered applications with **structured outputs using Pydantic models**.
#
# Unlike traditional LLM APIs that return unstructured text, PydanticAI ensures responses conform to a predefined schema.
#
# This notebook covers:
#
# - Core concepts
# - Agent API
# - Structured outputs
# - Tool usage
# - Validation and retries
# - Async execution
#
# By the end, you will understand how to build reliable LLM pipelines using structured outputs.

# %% [markdown]
# # Table of Contents
#
# 1. Introduction
# 2. Why PydanticAI exists
# 3. Installation
# 4. Minimal Example
# 5. Core Concepts
# 6. Structured Outputs
# 7. Validation
# 8. Tools
# 9. Dependencies
# 10. Async Execution
# 11. Advanced Features
# 12. Best Practices
# 13. Summary

# %% [markdown]
# ### Why PydanticAI Exists
#
# LLMs typically return unstructured text.
#
# Example:
#
# User prompt:
# "Extract product information from this description"
#
# LLM output:
# "The product is an iPhone 15 priced at $999."
#
# This output is difficult to use programmatically.
#
# What we want instead:
#
# {
#   "product_name": "iPhone 15",
#   "price": 999
# }
#
# PydanticAI solves this problem by:
#
# - Defining schemas using **Pydantic models**
# - Enforcing structured outputs
# - Automatically retrying when validation fails
# - Providing a simple agent abstraction for LLM interaction

# %% [markdown]
# ### Mental Model
#
# ```
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

# %% [markdown]
# ## Installation
#
# We install a minimal set of packages to keep the notebook self-contained and reproducible.
#
# This notebook uses `pydantic-ai`, `pydantic`, and `python-dotenv`.
#

# %%
# !pip install -q pydantic-ai

# %%
import os
from dotenv import load_dotenv, find_dotenv
import nest_asyncio
nest_asyncio.apply()


env_path = find_dotenv(usecwd=True)
load_dotenv(env_path, override=True)

MODEL_ID = os.getenv("PYDANTIC_AI_MODEL", "openai:gpt-4.1-mini")
print("dotenv path:", env_path or "<not found>")
print("PYDANTIC_AI_MODEL:", MODEL_ID)
print("OPENAI_API_KEY:", utils._mask(os.getenv("OPENAI_API_KEY")))

# %% [markdown]
# ### Running the Notebook
#
# To run the examples you must set your API key.
#
# Example:
# ```
# export OPENAI_API_KEY="your_key_here"
# ```

# %% [markdown]
# ## Minimal Example
#
# The quickest way to understand PydanticAI is through a small example.
#
# We define a schema using Pydantic and instruct the agent to produce that structured output.

# %%
from pydantic import BaseModel
from pydantic_ai import Agent

class City(BaseModel):
    name: str
    country: str
    population: int

agent = Agent(
    "openai:gpt-4o-mini",
    output_type=City
)

result = agent.run_sync("Tell me about Paris")

result.output

# %% [markdown]
# ### What Happened?
#
# 1. A Pydantic schema (`City`) defines the expected output structure.
# 2. The `Agent` sends the prompt to the LLM.
# 3. The LLM response is validated against the schema.
# 4. If validation succeeds, the structured result is returned.

# %% [markdown]
# ## Core Concepts
#
# PydanticAI revolves around a few important abstractions.
#
# ### Agent
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
# ### output_type
#
# Defines the expected structured output.
#
# This must be a Pydantic model.
#
# ### Tools
#
# Functions that the agent can call during reasoning.
#
# Tools allow agents to interact with external systems such as APIs or databases.
#
#

# %% [markdown]
# ## Structured Outputs with Pydantic

# %%
from pydantic import BaseModel

class Product(BaseModel):
    name: str
    price: float
    category: str

agent = Agent(
    "openai:gpt-4o-mini",
    output_type=Product
)

agent.run_sync("Describe the Apple AirPods Pro").output


# %% [markdown]
# ### What happened in the code
#
# - We defined a `Product` schema (name, price, category).
# - The agent is configured to produce outputs that conform to this schema.
# - When the model answers, PydanticAI validates that:
#   - `price` is a number
#   - fields exist with the right types
#   - the structure matches exactly
#
# **Why PydanticAI is useful here:**  
# This turns LLM responses into structured data you can store in databases, feed into analytics, or pass downstream in an application without brittle string parsing.

# %% [markdown]
# ## Validation and Retries
#
# If the LLM produces an output that does not match the schema, PydanticAI automatically retries.
#
# This greatly improves reliability.

# %%
class Person(BaseModel):
    name: str
    age: int

agent = Agent(
    "openai:gpt-4o-mini",
    output_type=Person,
    retries=2
)

agent.run_sync("Tell me about Albert Einstein")


# %% [markdown]
# ### What happened in the code
#
# - We defined a `Person` schema with `name` and `age`.
# - We set `retries=2` on the agent.
# - If the model output fails schema validation (missing fields, wrong types), PydanticAI automatically retries the model call to get a valid output.
#
# **Why PydanticAI is useful here:**  
# Real LLM outputs are inconsistent. Automatic schema validation + retry gives you reliability without writing custom parsing and retry logic for every prompt.

# %% [markdown]
# ## Tools
#
# Agents can call Python functions as tools.

# %%
agent = Agent(
    "openai:gpt-4o-mini",
    tools=[utils.get_weather]
)

agent.run_sync("What is the weather in Tokyo?")

# %% [markdown]
# ### What happened in the code
#
# - We defined a Python function `get_weather(city)` that returns a deterministic string.
# - We passed it into the agent via `tools=[get_weather]`.
# - When the user asks about weather, the agent can choose to call the tool to get the answer instead of hallucinating.
#
# **Why PydanticAI is useful here:**  
# Tools let the model interact with real functions and external systems. This is how you build agents that do real work (APIs, databases, calculations) rather than confidently inventing facts.

# %% [markdown]
# ## Dependencies
#
# Dependencies allow agents to access external resources or shared state.

# %%
from dataclasses import dataclass
from pydantic_ai import Agent

@dataclass
class Config:
    company: str

agent = Agent("openai:gpt-4o-mini", deps_type=Config, tools=[utils.company_name])

result = agent.run_sync("What company is configured?", deps=Config(company="OpenAI"))
print(result.output)

# %% [markdown]
# ### What happened in the code
#
# - `deps_type=Config` declares the *shape* of runtime context the agent can receive.
# - At run time, we pass an instance like `Config(company="OpenAI")`.
# - Tools (or other agent logic) can access this via `RunContext.deps`, so the agent can use configuration/state without hardcoding it into prompts.
#
# **Why PydanticAI is useful here:**  
# Dependencies are a clean way to inject runtime configuration (tenant ID, API clients, feature flags, environment context) into agents and tools without relying on global variables or string formatting prompts.

# %% [markdown]
# ## Async Execution
#
# PydanticAI supports asynchronous execution for scalable applications.

# %%
import asyncio

asyncio.run(utils.run_agent(agent))

# %% [markdown]
# ### What happened in the code
#
# - We defined an async function that calls `await agent.run(...)`.
# - Async execution is helpful for applications that need concurrency (web servers, batch pipelines, background jobs).
# - `asyncio.run(...)` runs the coroutine in a notebook-safe way.
#
# **Why PydanticAI is useful here:**  
# Most real systems are async. PydanticAI supports async natively, so you can run many agent calls concurrently without blocking your app.

# %% [markdown]
# ## Advanced API Features
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
# ## Result Validators
#
# Result validators allow you to enforce additional rules on model outputs.
#
# Even if the response matches the Pydantic schema, we may still want to verify
# logical constraints.
#
# Example: if an answer claims to use documents, it must include at least one source.

# %%
from pydantic import BaseModel
from pydantic_ai import Agent

MODEL_ID = "openai:gpt-4o-mini"


class SourceRef(BaseModel):
    doc_id: str
    quote: str


class AnswerWithSources(BaseModel):
    answer: str
    sources: list[SourceRef]


validator_agent = Agent(
    MODEL_ID,
    output_type=AnswerWithSources,
    instructions=(
        "Answer with short factual statements. "
        "If you reference documents, include sources."
    ),
)
validator_agent.output_validator(utils.validate_sources)


# %%
try:
    utils.validate_sources(
        AnswerWithSources(
            answer="According to the documents...",
            sources=[]
        )
    )
except Exception as e:
    print("Validator failure example:", e)

# %% [markdown]
# ### What happened in the code
#
# - We defined a schema `AnswerWithSources` where the model must return:
#   - `answer` (string)
#   - `sources` (list of `{doc_id, quote}`)
# - We attached an `output_validator` that enforces *logical rules* beyond the schema:
#   - if the answer mentions docs, sources must not be empty
#   - max 3 sources
#   - no duplicate sources
# - If rules fail, we raise `ModelRetry`, which tells PydanticAI to retry the model call.
#
# **Why PydanticAI is useful here:**  
# Schemas catch structural mistakes. Validators catch logical mistakes. Together, they make LLM outputs production-grade by enforcing business rules automatically.

# %% [markdown]
# ### Validator Failure Example
#
# The validator can also be tested manually.
#
# If the validation rule fails, the validator raises `ModelRetry`, which instructs the agent to retry the LLM call with improved instructions.

# %%
import asyncio

asyncio.run(utils.run_validator_example(validator_agent))

# %% [markdown]
# ## Streaming
#
# Streaming allows tokens to be returned as they are generated.
#
# Benefits:
#
# - lower perceived latency
# - better user experience in chat interfaces
# - progressive display of responses

# %%

stream_agent = Agent(MODEL_ID, instructions="Write one short paragraph about unit tests.")

if not hasattr(stream_agent, "run_stream"):
    print("Streaming API not available; falling back to run().")
    result = await stream_agent.run("What are unit tests?")
    _print_result("Non-streamed:", result)
else:
    try:
        async with stream_agent.run_stream("What are unit tests?") as stream:
            print("Streaming:")
            async for chunk in stream.stream_text():
                print(chunk, end="", flush=True)
            print("---")
            result = await stream.get_final_result()
            print("\n\nFinal result:", result)
    except Exception as e:
        print("Streaming failed; falling back to run().", e)
        result = await stream_agent.run("What are unit tests?")
        print("\n\nNon-streamed:", result)


# %% [markdown]
# ### What happened in the code
#
# - We created an agent and attempted to call the model using streaming mode.
# - With streaming, tokens are yielded as the model generates them instead of waiting for the full response.
# - This improves perceived responsiveness for chat apps and UIs.
#
# **Why PydanticAI is useful here:**  
# Streaming helps build better user experiences. You can display partial output instantly while the model continues generating, which is critical for interactive assistants.

# %% [markdown]
# ## Provider Configuration
#
# Model objects let you configure providers directly (e.g., base URLs).
#
# You can supply an explicit model object instead of a string ID. This is where you would set provider-specific options (e.g., `base_url`).
#

# %%

explicit_model = None
try:
    from pydantic_ai.models.openai import OpenAIModel
    explicit_model = OpenAIModel(
        model=MODEL_ID.split(":", 1)[-1],
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("OPENAI_BASE_URL"),
    )
    print("Using explicit OpenAIModel.")
except Exception as e1:
    try:
        from pydantic_ai.models.openai import OpenAIChatModel
        explicit_model = OpenAIChatModel(
            model=MODEL_ID.split(":", 1)[-1],
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url=os.getenv("OPENAI_BASE_URL"),
        )
        print("Using explicit OpenAIChatModel.")
    except Exception as e2:
        print("Explicit model unavailable; using string model ID.", e2)

agent = Agent(explicit_model or MODEL_ID, instructions="Be concise.")
try:
    result = await agent.run("Say hello in one sentence.")
    print("Explicit model (or fallback):", result)
except Exception as e:
    print("Error: ", e)


# %% [markdown]
# ### What happened in the code
#
# - Instead of using a string model ID, we attempted to create an explicit provider model object.
# - This allows provider-specific configuration such as:
#   - custom base URLs
#   - custom API keys
#   - proxy settings
# - If explicit model classes aren't available in the installed version, we fall back to using the string model ID.
#
# **Why PydanticAI is useful here:**  
# Explicit provider configuration is what you use in real deployments: enterprise gateways, self-hosted endpoints, proxies, and custom routing.

# %% [markdown]
# ## 11) AgentRun
#
# AgentRun objects contain metadata about an agent execution.
#
# This includes:
#
# - token usage
# - message history
# - tool calls
# - final output

# %%

meta_agent = Agent(MODEL_ID, instructions="Answer in one sentence.")
result = await meta_agent.run("What is a unit test?")
usage = getattr(result, "usage", None)
message_count = len(result.new_messages())
print("Output:", result.output)
print("Messages (new):", message_count)
print("Usage:", usage)


# %% [markdown]
# ### What happened in the code
#
# - We ran an agent and inspected the returned result object.
# - The result object can include metadata such as:
#   - token usage (cost visibility)
#   - message history (debugging)
#   - tool calls (auditing agent behavior)
#
# **Why PydanticAI is useful here:**  
# When agents behave unexpectedly, metadata is how you debug and control them. This is essential for observability, cost tracking, and governance.

# %% [markdown]
# ## 12) Usage limits and model settings
#
# Usage limits help control:
#
# - API cost
# - runaway loops
# - excessive token usage

# %%
from pydantic_ai import Agent



# Version-tolerant imports for ModelSettings + UsageLimits
try:
    # common in newer versions
    from pydantic_ai import ModelSettings, UsageLimits
except Exception:
    # fallback seen in some versions
    from pydantic_ai.models import ModelSettings  # type: ignore
    from pydantic_ai.usage import UsageLimits     # type: ignore


settings_agent = Agent(
    MODEL_ID,
    instructions="Answer in a single sentence.",
    model_settings=ModelSettings(temperature=0.2),
)

result = await settings_agent.run(
    "Explain what unit tests are.",
    usage_limits=UsageLimits(request_limit=3),
)

print("Model settings + usage limits:")
print(result.output)

# %% [markdown]
# ### What happened in the code
#
# - `ModelSettings(temperature=0.2)` controls response randomness:
#   - lower temperature = more deterministic outputs
# - `UsageLimits(request_limit=3)` sets guardrails on usage:
#   - helps prevent runaway retries or excessive calls
# - We ran the agent with these settings applied.
#
# **Why PydanticAI is useful here:**  
# PydanticAI makes it easy to add safety and cost controls to LLM systems. These controls matter in production where reliability and spend both need limits.

# %% [markdown]
# ## Best Practices
#
# 1. Always define clear schemas using Pydantic models.
# 2. Keep schemas simple and explicit.
# 3. Use retries for robustness.
# 4. Add tools for external integrations.
# 5. Use async execution for production systems.

# %% [markdown]
# ## Troubleshooting
# - Missing API key: set `OPENAI_API_KEY` (or your provider-specific key).
# - Event loop errors in notebooks: use `await agent.run(...)` instead of `run_sync`.
# - Validation errors: revise `output_type` or the validator to match expected output.
#
