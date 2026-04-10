"""
Earnings Agent for earnings call and KPI analysis.

This agent specializes in:
- KPI trend analysis
- Guidance language changes quarter-over-quarter
- Management tone shift detection
- Earnings beat/miss analysis
"""

from typing import Any

from txtai import LLM

from app.pipeline.embeddings import search


# System prompt for the earnings agent
SYSTEM_PROMPT = """You are a financial analyst specializing in earnings call analysis.

Your role is to:
1. Analyze KPI trends quarter-over-quarter
2. Detect changes in guidance language vs prior quarters
3. Assess management tone shifts (confidence, caution, optimism)
4. Identify earnings beats/misses and analyst reactions

Focus on:
- Revenue and EPS vs expectations
- Forward guidance changes
- Management commentary on headwinds/tailwinds
- Analyst questions and concerns
- Segment-level performance

Be specific and cite exact language from earnings transcripts.
"""


def run(query: str, context: dict | None = None) -> dict[str, Any]:
    """
    Run earnings analysis for a query.

    Args:
        query: The user's question (e.g., "How did AAPL's earnings go?")
        context: Optional context dict with:
            - ticker: Company ticker
            - quarter: Specific quarter (e.g., "Q4 2024")
            - compare_prior: Whether to compare to prior quarter

    Returns:
        Dict with:
            - kpi_trends: List of KPI changes quarter-over-quarter
            - guidance_changes: Changes in forward guidance language
            - management_tone: Assessment of management tone
            - earnings_summary: Beat/miss analysis
            - summary: Natural language earnings summary
    """
    if context is None:
        context = {}

    ticker = context.get("ticker", "")
    quarter = context.get("quarter", "")

    # Search earnings transcripts
    earnings_query = f"{ticker} earnings call" if ticker else query
    earnings_results = search(earnings_query, source_filter="earnings", limit=15)

    # Also search news for earnings coverage
    news_results = search(f"{ticker} earnings", source_filter="news", limit=5)

    all_results = earnings_results + news_results

    if not all_results:
        return {
            "kpi_trends": [],
            "guidance_changes": [],
            "management_tone": "No data available",
            "earnings_summary": "No earnings data available",
            "summary": f"No earnings data available for {ticker}" if ticker else "No data available.",
        }

    # Build context for LLM
    context_text = _build_context_string(all_results)

    # Use LLM for analysis
    llm = _get_llm()

    prompt = f"""{SYSTEM_PROMPT}

Query: {query}
Company: {ticker}
Quarter: {quarter if quarter else 'Most recent'}

Relevant documents from earnings transcripts and news:
{context_text}

Provide your earnings analysis in this exact JSON format:
{{
    "kpi_trends": [
        {{"metric": "...", "current_value": "...", "prior_value": "...", "change": "...", "direction": "improving|declining|stable"}}
    ],
    "guidance_changes": [
        {{"area": "...", "prior_guidance": "...", "current_guidance": "...", "change_type": "raised|lowered|unchanged|narrowed|widened"}}
    ],
    "management_tone": "description of tone (confident/cautious/optimistic/concerned) with evidence",
    "earnings_summary": "beat/miss analysis with specific numbers",
    "summary": "2-3 sentence earnings summary"
}}

Be specific and cite exact language from the transcript where possible.
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
        title = metadata.get("title", "")
        text = result.get("text", "")[:600]

        lines.append(f"[{i}] [{source}] {title}")
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
    """Parse LLM response into structured earnings analysis."""
    import json
    import re

    json_match = re.search(r"\{.*\}", response, re.DOTALL)

    if json_match:
        try:
            parsed = json.loads(json_match.group())
            return {
                "kpi_trends": parsed.get("kpi_trends", []),
                "guidance_changes": parsed.get("guidance_changes", []),
                "management_tone": parsed.get("management_tone", ""),
                "earnings_summary": parsed.get("earnings_summary", ""),
                "summary": parsed.get("summary", response),
            }
        except json.JSONDecodeError:
            pass

    # Fallback: return basic structure
    return {
        "kpi_trends": [],
        "guidance_changes": [],
        "management_tone": "Unable to assess",
        "earnings_summary": "Data unavailable",
        "summary": response[:500],
    }


if __name__ == "__main__":
    # Test the agent
    from dotenv import load_dotenv
    load_dotenv()

    result = run("How did AAPL's latest earnings go?", context={"ticker": "AAPL"})
    print(f"Earnings summary: {result['earnings_summary']}")
    print(f"KPI trends: {len(result['kpi_trends'])}")
    print(f"\nSummary: {result['summary']}")
