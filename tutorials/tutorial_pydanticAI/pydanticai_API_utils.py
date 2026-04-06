"""Utility functions for tutorials/tutorial_pydanticAI/pydanticai.API notebook."""

from typing import Any

from pydantic_ai import ModelRetry, RunContext


# #########################################################################
# Code for setup and masking.
# #########################################################################
def _mask(value: str | None) -> str:
    if not value:
        return "<not set>"
    if len(value) <= 6:
        return "*" * len(value)
    return f"{value[:3]}...{value[-2:]}"


# #########################################################################
# Code for tools and dependencies.
# #########################################################################
def get_weather(city: str) -> str:
    return f"The weather in {city} is sunny."


def company_name(ctx: RunContext[Any]) -> str:
    return ctx.deps.company


# #########################################################################
# Code for async execution and validation demos.
# #########################################################################
async def run_agent(agent: Any) -> Any:
    result = await agent.run("Tell me about Tokyo")
    return result.output


def validate_sources(result: Any) -> Any:
    answer_l = result.answer.lower()
    mentions_docs = any(
        token in answer_l for token in ["doc", "document", "according", "source"]
    )
    if mentions_docs and not result.sources:
        raise ModelRetry("Answer references documents but sources are empty.")
    if len(result.sources) > 3:
        raise ModelRetry("Too many sources. Maximum allowed is 3.")
    seen = set()
    for s in result.sources:
        key = (s.doc_id, s.quote)
        if key in seen:
            raise ModelRetry("Duplicate sources found.")
        seen.add(key)
    return result


async def run_validator_example(validator_agent: Any) -> None:
    result = await validator_agent.run(
        "Explain something using documents and cite sources."
    )
    print("\nValidated output:\n")
    print(result.output)
