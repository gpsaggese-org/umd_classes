"""
Regulatory Agent for SEC and regulatory filing analysis.

This agent specializes in:
- Flagged filing identification
- Enforcement risk signal detection
- Material disclosure language analysis
- Compliance monitoring
"""

from typing import Any

from txtai import LLM

from app.pipeline.embeddings import search


# System prompt for the regulatory agent
SYSTEM_PROMPT = """You are a compliance analyst monitoring regulatory and policy risk.

Your role is to:
1. Identify flagged filings that warrant attention
2. Detect enforcement risk signals
3. Analyze material disclosure language
4. Monitor regulatory and policy changes

Focus on:
- SEC comment letters and responses
- Restatements and amendments
- Risk factor changes (Item 1A in 10-K)
- Legal proceedings disclosures
- Related party transactions
- Going concern qualifications

Be specific and cite filing types, dates, and exact disclosure language.
"""


def run(query: str, context: dict | None = None) -> dict[str, Any]:
    """
    Run regulatory analysis for a query.

    Args:
        query: The user's question (e.g., "Any regulatory issues with AAPL?")
        context: Optional context dict with:
            - ticker: Company ticker
            - filing_type: Specific filing type to focus on
            - risk_areas: Specific risk areas to investigate

    Returns:
        Dict with:
            - flagged_filings: List of filings that warrant attention
            - enforcement_signals: Signs of potential enforcement action
            - disclosure_changes: Material changes in disclosure language
            - risk_assessment: Overall regulatory risk level
            - summary: Natural language regulatory summary
    """
    if context is None:
        context = {}

    ticker = context.get("ticker", "")
    filing_type = context.get("filing_type", "")

    # Search SEC filings
    sec_query = f"{ticker} SEC filing" if ticker else query
    sec_results = search(sec_query, source_filter="sec", limit=15)

    if not sec_results:
        return {
            "flagged_filings": [],
            "enforcement_signals": [],
            "disclosure_changes": [],
            "risk_assessment": "No data available",
            "summary": f"No regulatory data available for {ticker}" if ticker else "No data available.",
        }

    # Build context for LLM
    context_text = _build_context_string(sec_results)

    # Use LLM for analysis
    llm = _get_llm()

    prompt = f"""{SYSTEM_PROMPT}

Query: {query}
Company: {ticker}
Filing Type Focus: {filing_type if filing_type else 'All types'}

Relevant SEC filings:
{context_text}

Provide your regulatory analysis in this exact JSON format:
{{
    "flagged_filings": [
        {{"filing_type": "...", "filing_date": "...", "issue": "...", "severity": "high|medium|low", "reference": "specific section or item"}}
    ],
    "enforcement_signals": [
        {{"signal": "...", "type": "comment_letter|restatement|investigation|warning", "description": "...", "severity": "high|medium|low"}}
    ],
    "disclosure_changes": [
        {{"area": "...", "change_type": "added|removed|modified", "prior_language": "...", "current_language": "...", "implication": "..."}}
    ],
    "risk_assessment": "overall regulatory risk level (low/medium/high) with explanation",
    "summary": "2-3 sentence regulatory summary"
}}

Be specific and cite filing dates, form types, and exact disclosure language.
Flag any unusual patterns or changes from standard disclosure practices.
"""

    response = llm(prompt)

    # Parse the response
    result = _parse_response(response, sec_results)

    return result


def _build_context_string(results: list[dict]) -> str:
    """Build formatted context string from search results."""
    lines = []

    for i, result in enumerate(results, 1):
        metadata = result.get("metadata", {})
        form_type = metadata.get("form_type", "")
        company = metadata.get("company_name", "")
        filing_date = metadata.get("filing_date", "")
        items = metadata.get("items", [])
        text = result.get("text", "")[:600]

        lines.append(f"[{i}] {company} - {form_type}")
        lines.append(f"    Filed: {filing_date}")
        if items:
            lines.append(f"    Items: {', '.join(items)}")
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
    """Parse LLM response into structured regulatory analysis."""
    import json
    import re

    json_match = re.search(r"\{.*\}", response, re.DOTALL)

    if json_match:
        try:
            parsed = json.loads(json_match.group())
            return {
                "flagged_filings": parsed.get("flagged_filings", []),
                "enforcement_signals": parsed.get("enforcement_signals", []),
                "disclosure_changes": parsed.get("disclosure_changes", []),
                "risk_assessment": parsed.get("risk_assessment", ""),
                "summary": parsed.get("summary", response),
            }
        except json.JSONDecodeError:
            pass

    # Fallback: return basic structure
    return {
        "flagged_filings": [],
        "enforcement_signals": [],
        "disclosure_changes": [],
        "risk_assessment": "Unable to assess",
        "summary": response[:500],
    }


if __name__ == "__main__":
    # Test the agent
    from dotenv import load_dotenv
    load_dotenv()

    result = run("Any regulatory issues for AAPL?", context={"ticker": "AAPL"})
    print(f"Flagged filings: {len(result['flagged_filings'])}")
    print(f"Enforcement signals: {len(result['enforcement_signals'])}")
    print(f"Risk assessment: {result['risk_assessment']}")
    print(f"\nSummary: {result['summary']}")
