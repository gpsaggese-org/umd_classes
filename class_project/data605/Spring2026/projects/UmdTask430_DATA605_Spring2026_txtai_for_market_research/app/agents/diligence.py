"""
Due Diligence Agent for M&A analysis.

This agent specializes in:
- Risk identification and flagging
- Synergy opportunity assessment
- Red-flag language pattern detection vs historical deal failures
"""

import logging
from typing import Any

from txtai import LLM

from app.pipeline.embeddings import search

_LOG = logging.getLogger(__name__)


# System prompt for the diligence agent
SYSTEM_PROMPT = """You are an M&A analyst specializing in risk identification and synergy assessment.

Your role is to:
1. Identify potential risks in acquisition targets or deals
2. Assess synergy opportunities (cost, revenue, technology)
3. Detect red-flag language patterns that resemble historical deal failures
4. Provide actionable due diligence findings

Focus on:
- Financial risks (debt levels, cash flow issues, accounting irregularities)
- Operational risks (customer concentration, supply chain, key person risk)
- Legal/regulatory risks (pending litigation, antitrust concerns)
- Cultural risks (integration challenges, talent retention)

Be specific and cite evidence from SEC filings and earnings transcripts.
"""


def run(query: str, context: dict | None = None) -> dict[str, Any]:
    """
    Run due diligence analysis for a query.

    Args:
        query: The user's question (e.g., "What are the risks in acquiring Company X?")
        context: Optional context dict with:
            - ticker: Target company ticker
            - acquirer_ticker: Acquiring company ticker (if applicable)
            - deal_type: Type of deal (merger, acquisition, etc.)

    Returns:
        Dict with:
            - risk_flags: List of identified risks with severity levels
            - synergies: List of potential synergy opportunities
            - red_flags: Language patterns matching historical deal failures
            - financial_health: Assessment of financial stability
            - summary: Natural language due diligence summary
    """
    if context is None:
        context = {}

    ticker = context.get("ticker", "")
    acquirer = context.get("acquirer_ticker", "")

    # Search SEC filings and earnings transcripts
    sec_results = search(query, source_filter="sec", limit=15)
    earnings_results = search(
        "earnings call transcript", source_filter="earnings", limit=10
    )

    all_results = sec_results + earnings_results

    if not all_results:
        return {
            "risk_flags": [],
            "synergies": [],
            "red_flags": [],
            "financial_health": "No data available",
            "summary": f"No due diligence data available for {ticker}"
            if ticker
            else "No data available.",
        }

    # Build context for LLM
    context_text = _build_context_string(all_results)

    # Use LLM for analysis
    llm = _get_llm()

    prompt = f"""{SYSTEM_PROMPT}

Query: {query}
Target: {ticker}
Acquirer: {acquirer}

Relevant documents from SEC filings and earnings calls:
{context_text}

Provide your due diligence analysis in this exact JSON format:
{{
    "risk_flags": [
        {{"category": "financial|operational|legal|cultural", "severity": "high|medium|low", "description": "...", "evidence": "quote or reference"}}
    ],
    "synergies": [
        {{"type": "cost|revenue|technology|talent", "description": "...", "estimated_impact": "..."}}
    ],
    "red_flags": [
        {{"pattern": "...", "similarity_to_historical_failures": "high|medium|low", "explanation": "..."}}
    ],
    "financial_health": "assessment summary",
    "summary": "2-3 sentence due diligence summary"
}}

Be specific and cite filing dates or earnings call quarters where possible.
"""

    response = llm(prompt)

    # Parse the response
    result = _parse_response(response, all_results)

    return result


def _build_context_string(results: list[dict]) -> str:
    """Build formatted context string from search results."""
    lines = []

    for i, result in enumerate(results, 1):
        metadata = result.get("metadata", {})
        source = metadata.get("source", "unknown")
        form_type = metadata.get("form_type", "")
        filing_date = metadata.get("filing_date", "")
        text = result.get("text", "")[:600]

        lines.append(f"[{i}] [{source}] {form_type} - Filed: {filing_date}")
        lines.append(f"    Content: {text}")
        lines.append("")

    return "\n".join(lines)


def _get_llm() -> LLM:
    """Get configured LLM using Ollama."""
    import os

    ollama_host = os.getenv("OLLAMA_HOST", "http://localhost:11434")
    ollama_model = os.getenv("OLLAMA_LLM_MODEL", "qwen2.5:7b")

    # Try Ollama first
    try:
        return LLM(model=f"ollama:{ollama_model}@{ollama_host}")
    except Exception:
        # Fallback to OpenAI
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key:
            return LLM(model="openai:gpt-4o-mini", api_key=api_key)
        else:
            return LLM(model="mistralai/Mistral-7B-Instruct-v0.2")


def _parse_response(response: str, results: list[dict]) -> dict[str, Any]:
    """Parse LLM response into structured due diligence analysis."""
    import json
    import re

    json_match = re.search(r"\{.*\}", response, re.DOTALL)

    if json_match:
        try:
            parsed = json.loads(json_match.group())
            return {
                "risk_flags": parsed.get("risk_flags", []),
                "synergies": parsed.get("synergies", []),
                "red_flags": parsed.get("red_flags", []),
                "financial_health": parsed.get("financial_health", ""),
                "summary": parsed.get("summary", response),
            }
        except json.JSONDecodeError:
            pass

    # Fallback: return basic structure
    return {
        "risk_flags": [
            {
                "category": "unknown",
                "severity": "medium",
                "description": "Analysis unavailable",
                "evidence": "LLM parsing failed",
            }
        ],
        "synergies": [],
        "red_flags": [],
        "financial_health": "Unable to assess",
        "summary": response[:500],
    }


if __name__ == "__main__":
    # Test the agent.
    from dotenv import load_dotenv

    load_dotenv()
    logging.basicConfig(level=logging.INFO)
    result = run("What are the key risks for AAPL?", context={"ticker": "AAPL"})
    _LOG.info("Risk flags: %d", len(result["risk_flags"]))
    for risk in result["risk_flags"][:3]:
        _LOG.info(
            "  - [%s] %s: %s",
            risk["severity"],
            risk["category"],
            risk["description"][:100],
        )
    _LOG.info("Summary: %s", result["summary"])
