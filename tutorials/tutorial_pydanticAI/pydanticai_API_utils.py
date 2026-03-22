"""
Utilities for pydanticai.API.ipynb / pydanticai.API.py.
"""

from __future__ import annotations

from typing import Any


def mask(value: str | None) -> str:
    if not value:
        return "<not set>"
    if len(value) <= 6:
        return "*" * len(value)
    return f"{value[:3]}...{value[-2:]}"


def get_weather(city: str) -> str:
    return f"The weather in {city} is sunny."


def company_name(ctx: Any) -> str:
    return ctx.deps.company


async def run_agent(agent: Any) -> Any:
    result = await agent.run("Tell me about Tokyo")
    return result.output


def validate_sources(result: Any, model_retry_cls: Any) -> Any:
    answer_l = result.answer.lower()
    mentions_docs = any(
        token in answer_l for token in ["doc", "document", "according", "source"]
    )

    if mentions_docs and not result.sources:
        raise model_retry_cls("Answer references documents but sources are empty.")

    if len(result.sources) > 3:
        raise model_retry_cls("Too many sources. Maximum allowed is 3.")

    seen = set()
    for s in result.sources:
        key = (s.doc_id, s.quote)
        if key in seen:
            raise model_retry_cls("Duplicate sources found.")
        seen.add(key)

    return result


async def run_validator_example(validator_agent: Any) -> None:
    result = await validator_agent.run(
        "Explain something using documents and cite sources."
    )

    print("\nValidated output:\n")
    print(result.output)
