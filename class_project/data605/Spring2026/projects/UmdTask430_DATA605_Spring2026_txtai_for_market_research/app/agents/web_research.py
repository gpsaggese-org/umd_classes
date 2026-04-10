"""
Web Research Agent for competitive intelligence.

This agent specializes in:
- Competitor move analysis
- Product launch tracking
- Executive commentary extraction
- Market positioning assessment
"""

from typing import Any

from txtai import LLM

from app.pipeline.embeddings import search


# System prompt for the web research agent
SYSTEM_PROMPT = """You are a research analyst specializing in competitive intelligence from public web sources.

Your role is to:
1. Track competitor moves and strategic shifts
2. Identify product launches and feature announcements
3. Extract executive commentary on strategy and market outlook
4. Assess market positioning relative to competitors

Focus on:
- New product/service announcements
- Partnership and collaboration news
- Executive statements on strategy
- Market share and competitive dynamics
- Pricing and positioning changes

Be specific and cite sources (press release titles, URLs, dates).
"""


def run(query: str, context: dict | None = None) -> dict[str, Any]:
    """
    Run web research analysis for a query.

    Args:
        query: The user's question (e.g., "What are competitors doing in AI?")
        context: Optional context dict with:
            - ticker: Company ticker
            - competitors: List of competitor tickers
            - industry: Industry sector

    Returns:
        Dict with:
            - competitor_moves: List of recent competitor actions
            - product_launches: List of new products/features
            - executive_commentary: Key executive statements
            - market_positioning: Assessment of market position
            - summary: Natural language research summary
    """
    if context is None:
        context = {}

    ticker = context.get("ticker", "")
    competitors = context.get("competitors", [])

    # Search web scrape and news sources
    web_results = search(query, source_filter="web", limit=10)
    news_results = search(query, source_filter="news", limit=10)

    all_results = web_results + news_results

    if not all_results:
        return {
            "competitor_moves": [],
            "product_launches": [],
            "executive_commentary": [],
            "market_positioning": "No data available",
            "summary": f"No web research data available for {ticker}" if ticker else "No data available.",
        }

    # Build context for LLM
    context_text = _build_context_string(all_results)

    # Use LLM for analysis
    llm = _get_llm()

    prompt = f"""{SYSTEM_PROMPT}

Query: {query}
Company: {ticker}
Competitors: {', '.join(competitors) if competitors else 'Not specified'}

Relevant documents from web sources and news:
{context_text}

Provide your competitive intelligence analysis in this exact JSON format:
{{
    "competitor_moves": [
        {{"company": "...", "action": "...", "date": "...", "source": "source name", "strategic_implication": "..."}}
    ],
    "product_launches": [
        {{"company": "...", "product": "...", "description": "...", "date": "...", "source": "..."}}
    ],
    "executive_commentary": [
        {{"executive": "...", "company": "...", "statement": "...", "context": "...", "source": "..."}}
    ],
    "market_positioning": "assessment of competitive position",
    "summary": "2-3 sentence research summary"
}}

Be specific and cite sources with dates where available.
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
        title = metadata.get("title", "No title")
        url = metadata.get("url", "")
        published = metadata.get("published_at", "")
        text = result.get("text", "")[:500]

        lines.append(f"[{i}] [{source}] {title}")
        if published:
            lines.append(f"    Date: {published}")
        if url:
            lines.append(f"    URL: {url}")
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
    """Parse LLM response into structured web research analysis."""
    import json
    import re

    json_match = re.search(r"\{.*\}", response, re.DOTALL)

    if json_match:
        try:
            parsed = json.loads(json_match.group())
            return {
                "competitor_moves": parsed.get("competitor_moves", []),
                "product_launches": parsed.get("product_launches", []),
                "executive_commentary": parsed.get("executive_commentary", []),
                "market_positioning": parsed.get("market_positioning", ""),
                "summary": parsed.get("summary", response),
            }
        except json.JSONDecodeError:
            pass

    # Fallback: return basic structure
    return {
        "competitor_moves": [],
        "product_launches": [],
        "executive_commentary": [],
        "market_positioning": "Unable to assess",
        "summary": response[:500],
    }


if __name__ == "__main__":
    # Test the agent
    from dotenv import load_dotenv
    load_dotenv()

    result = run("What are Apple's competitors doing in AI?", context={"ticker": "AAPL"})
    print(f"Competitor moves: {len(result['competitor_moves'])}")
    print(f"Product launches: {len(result['product_launches'])}")
    print(f"\nSummary: {result['summary']}")
