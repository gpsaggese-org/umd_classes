"""
Utility functions for tutorials/tutorial_pydanticAI/pydanticai.API notebook.

Import as:

import tutorials.tutorial_pydanticAI.pydanticai_API_utils as ttppaput
"""

import importlib
import importlib.util
import inspect
import logging
import os
from pathlib import Path
from typing import Any

from pydantic_ai import ModelRetry, RunContext

import helpers.hdbg as hdbg
import helpers.hnotebook as hnotebo

_LOG = logging.getLogger(__name__)
_DOCUMENTS_CACHE: dict[str, str] | None = None


# #############################################################################
# Code for setup and masking.
# #############################################################################
def init_logger(notebook_log: logging.Logger) -> None:
    """
    Initialize notebook and utility logging.

    :param notebook_log: logger from the paired notebook
    """
    global _LOG
    hnotebo.config_notebook()
    hdbg.init_logger(verbosity=logging.INFO, use_exec_path=False)
    hnotebo.set_logger_to_print(notebook_log)
    configured_log = _LOG
    hnotebo.set_logger_to_print(configured_log)
    _LOG = configured_log


def _mask(value: str | None) -> str:
    """
    Mask a secret value for notebook display.

    :param value: value to mask
    :return: masked value
    """
    if not value:
        return "<not set>"
    if len(value) <= 6:
        return "*" * len(value)
    return f"{value[:3]}...{value[-2:]}"


def log_environment(env_path: str, model_id: str) -> None:
    """
    Log notebook environment settings.

    :param env_path: dotenv file path
    :param model_id: configured model identifier
    """
    _LOG.info("dotenv path: %s", env_path or "<not found>")
    _LOG.info("PYDANTIC_AI_MODEL: %s", model_id)
    _LOG.info("OPENAI_API_KEY: %s", _mask(os.getenv("OPENAI_API_KEY")))


# #############################################################################
# Code for tools and dependencies.
# #############################################################################
def get_weather(city: str) -> str:
    """
    Get deterministic demo weather for a city.

    :param city: city name
    :return: weather response
    """
    weather = f"The weather in {city} is sunny."
    return weather


def company_name(ctx: RunContext[Any]) -> str:
    """
    Get the configured company from an agent run context.

    :param ctx: PydanticAI run context
    :return: configured company name
    """
    company = ctx.deps.company
    return company


# #############################################################################
# Code for async execution and validation demos.
# #############################################################################
def load_example_documents() -> dict[str, str]:
    """
    Load tutorial documents used by validator and retrieval demos.

    :return: mapping from document id to document text
    """
    global _DOCUMENTS_CACHE
    if _DOCUMENTS_CACHE is not None:
        return _DOCUMENTS_CACHE
    dataset_dir = Path(__file__).resolve().parent / "example_dataset"
    documents = {}
    for path in sorted(dataset_dir.glob("*.md")):
        documents[path.stem] = path.read_text()
    _DOCUMENTS_CACHE = documents
    return documents


def get_available_document_ids() -> list[str]:
    """
    Get sorted document ids from the example dataset.

    :return: sorted list of document ids
    """
    document_ids = sorted(load_example_documents())
    return document_ids


def search_documents(query: str, max_results: int = 3) -> str:
    """
    Search local tutorial documents and return snippets for citation.

    :param query: search query
    :param max_results: maximum number of snippets to return
    :return: formatted snippets with doc ids and quotes
    """
    documents = load_example_documents()
    query_terms = [term for term in query.lower().split() if len(term) > 2]
    candidates = []
    for doc_id, content in documents.items():
        for line in content.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            line_l = line.lower()
            score = sum(1 for term in query_terms if term in line_l)
            if score == 0 and query_terms:
                continue
            candidates.append((score, doc_id, line))
    candidates.sort(key=lambda item: (-item[0], item[1], item[2]))
    if not candidates:
        return "No matching snippets found."
    snippets = []
    for _, doc_id, line in candidates[:max_results]:
        snippets.append(f"doc_id={doc_id} | quote={line}")
    snippets_out = "\n".join(snippets)
    return snippets_out


async def run_agent(agent: Any, *, prompt: str = "Tell me about Tokyo") -> Any:
    """
    Run an agent asynchronously.

    :param agent: PydanticAI agent
    :param prompt: prompt to send to the agent
    :return: agent output
    """
    result = await agent.run(prompt)
    output = result.output
    return output


def validate_sources(result: Any) -> Any:
    """
    Validate answer source references.

    :param result: model output to validate
    :return: validated model output
    """
    answer_l = result.answer.lower()
    mentions_docs = any(
        token in answer_l for token in ["doc", "document", "according", "source"]
    )
    if mentions_docs and not result.sources:
        raise ModelRetry("Answer references documents but sources are empty.")
    if len(result.sources) > 3:
        raise ModelRetry("Too many sources. Maximum allowed is 3.")
    seen: set[tuple[str, str]] = set()
    for source in result.sources:
        key = (source.doc_id, source.quote)
        if key in seen:
            raise ModelRetry("Duplicate sources found.")
        seen.add(key)
    return result


def validate_document_sources(result: Any) -> Any:
    """
    Validate sources against local tutorial documents.

    :param result: model output to validate
    :return: validated model output
    """
    result = validate_sources(result)
    documents = load_example_documents()
    for source in result.sources:
        if source.doc_id not in documents:
            raise ModelRetry(
                f"Unknown doc_id '{source.doc_id}'. Use ids from example_dataset."
            )
        doc_text = " ".join(documents[source.doc_id].lower().split())
        quote_text = " ".join(source.quote.lower().split())
        if quote_text not in doc_text:
            raise ModelRetry(
                f"Quote not found in cited document '{source.doc_id}'."
            )
    return result


def build_missing_sources_retry() -> ModelRetry:
    """
    Build the retry exception used by the missing-sources demo.

    :return: retry exception
    """
    retry = ModelRetry("Answer references documents but sources are empty.")
    return retry


async def run_validator_example(
    validator_agent: Any,
    *,
    prompt: str = "Use local documents to explain Atlas billing plans and cite sources.",
) -> Any:
    """
    Run the result validator example.

    :param validator_agent: configured validator agent
    :return: validated output
    """
    result = await validator_agent.run(prompt)
    output = result.output
    return output


# #############################################################################
# Code for advanced API demos.
# #############################################################################
async def run_streaming_demo(stream_agent: Any) -> Any:
    """
    Run a streaming demo and log streamed text.

    :param stream_agent: configured streaming agent
    :return: final streaming result or non-streamed result
    """
    if not hasattr(stream_agent, "run_stream"):
        _LOG.info("Streaming API not available; falling back to run().")
        result = await stream_agent.run("What are unit tests?")
        return result
    async with stream_agent.run_stream("What are unit tests?") as stream:
        stream_text = stream.stream_text
        parameters = inspect.signature(stream_text).parameters
        if "delta" in parameters:
            text_stream = stream_text(delta=True)
        else:
            text_stream = stream_text()
        chunks = []
        async for chunk in text_stream:
            chunks.append(chunk)
        if hasattr(stream, "get_final_result"):
            result = await stream.get_final_result()
        else:
            result = "".join(chunks)
    _LOG.info("Streaming output:\n%s", "".join(chunks))
    return result


def _get_openai_model_class() -> Any | None:
    """
    Get the available explicit OpenAI model class.

    :return: model class, or None if unavailable
    """
    if importlib.util.find_spec("pydantic_ai") is None:
        return None
    if importlib.util.find_spec("pydantic_ai.models.openai") is None:
        return None
    module = importlib.import_module("pydantic_ai.models.openai")
    for class_name in ("OpenAIModel", "OpenAIChatModel"):
        if hasattr(module, class_name):
            model_class = getattr(module, class_name)
            return model_class
    return None


def build_explicit_openai_model(model_id: str) -> Any | None:
    """
    Build an explicit OpenAI model object when the installed API supports it.

    :param model_id: configured model identifier
    :return: explicit model object, or None
    """
    model_class = _get_openai_model_class()
    if model_class is None:
        return None
    hdbg.dassert_isinstance(model_id, str)
    hdbg.dassert_ne(model_id, "", "Model id cannot be empty")
    model_name = model_id.removeprefix("openai:")
    _LOG.info("Using OpenAI model with model_name='%s'.", model_name)
    signature = inspect.signature(model_class)
    parameters = signature.parameters
    base_kwargs = {
        "api_key": os.getenv("OPENAI_API_KEY"),
        "base_url": os.getenv("OPENAI_BASE_URL"),
    }
    args = []
    kwargs = {}
    if "model_name" in parameters:
        kwargs["model_name"] = model_name
    elif "model" in parameters:
        kwargs["model"] = model_name
    else:
        args.append(model_name)
    for key, value in base_kwargs.items():
        if key in parameters:
            kwargs[key] = value
    model = model_class(*args, **kwargs)
    return model


def get_settings_classes() -> tuple[Any, Any]:
    """
    Get ModelSettings and UsageLimits classes for the installed version.

    :return: ModelSettings and UsageLimits classes
    """
    module = importlib.import_module("pydantic_ai")
    if hasattr(module, "ModelSettings") and hasattr(module, "UsageLimits"):
        return module.ModelSettings, module.UsageLimits
    models_module = importlib.import_module("pydantic_ai.models")
    usage_module = importlib.import_module("pydantic_ai.usage")
    return models_module.ModelSettings, usage_module.UsageLimits
