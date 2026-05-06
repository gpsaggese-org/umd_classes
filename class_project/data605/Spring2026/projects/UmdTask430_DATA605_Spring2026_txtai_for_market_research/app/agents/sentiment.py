"""
Sentiment Agent for market sentiment and investor psychology analysis.

This agent specializes in:
- Bullish/bearish/neutral sentiment classification
- Key theme extraction from news articles
- Evidence snippet retrieval for sentiment claims
"""

from typing import Any

from txtai import LLM

from app.pipeline.embeddings import search


# System prompt for the sentiment agent
SYSTEM_PROMPT = """You are an expert in market sentiment and investor psychology.

Your role is to:
1. Analyze sentiment from news articles
2. Classify overall sentiment as Bullish, Neutral, or Bearish
3. Extract key themes driving sentiment
4. Provide evidence snippets that support your analysis

Be specific and data-driven. Always cite your sources (article titles, URLs).
If sentiment is mixed, explain the divergence and what each side is arguing.
"""


def run(query: str, context: dict | None = None) -> dict[str, Any]:
    """
    Run sentiment analysis for a query.

    Args:
        query: The user's question (e.g., "What's the sentiment on AAPL?")
        context: Optional context dict with:
            - ticker: Stock ticker symbol
            - time_range: Time range for analysis

    Returns:
        Dict with:
            - sentiment: "Bullish" | "Neutral" | "Bearish"
            - sentiment_score: Float 0-1 (0=bearish, 0.5=neutral, 1=bullish)
            - key_themes: List of key themes driving sentiment
            - evidence: List of supporting text snippets with sources
            - summary: Natural language summary of sentiment
    """
    if context is None:
        context = {}

    ticker = context.get("ticker", "")

    # Search for relevant news documents (not SEC filings).
    all_results = search(query, source_filter="news", limit=20)

    if not all_results:
        return {
            "sentiment": "Neutral",
            "sentiment_score": 0.5,
            "key_themes": ["No data available"],
            "evidence": [],
            "summary": f"No sentiment data available for {ticker}" if ticker else "No sentiment data available.",
        }

    # Build context string for LLM
    context_text = _build_context_string(all_results)

    # Use LLM to analyze sentiment
    llm = _get_llm()

    prompt = f"""{SYSTEM_PROMPT}

Query: {query}
Ticker: {ticker}

Relevant documents:
{context_text}

Analyze the sentiment and provide your response in this exact JSON format:
{{
    "sentiment": "Bullish" | "Neutral" | "Bearish",
    "sentiment_score": 0.0-1.0,
    "key_themes": ["theme 1", "theme 2", ...],
    "evidence": [
        {{"text": "snippet", "source": "source name", "url": "url if available"}}
    ],
    "summary": "2-3 sentence summary of overall sentiment"
}}

Be specific and cite sources. If sentiment is mixed, explain both sides.
"""

    response = llm(prompt)

    # Parse the response
    # txtai LLM returns a string, we need to extract JSON
    result = _parse_sentiment_response(response, all_results)

    return result


def _build_context_string(results: list[dict]) -> str:
    """Build a formatted context string from search results."""
    lines = []

    for i, result in enumerate(results, 1):
        metadata = result.get("metadata", {})
        source = metadata.get("source", "unknown")
        title = metadata.get("title", "No title")
        url = metadata.get("url", "")
        text = result.get("text", "")[:500]  # Limit text length

        lines.append(f"[{i}] [{source}] {title}")
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


def _parse_sentiment_response(response: str, results: list[dict]) -> dict[str, Any]:
    """Parse LLM response into structured sentiment analysis."""
    import json
    import re

    # Try to extract JSON from response
    json_match = re.search(r"\{.*\}", response, re.DOTALL)

    if json_match:
        try:
            parsed = json.loads(json_match.group())

            # Build evidence from results if not provided
            evidence = parsed.get("evidence", [])
            if not evidence and results:
                for r in results[:5]:
                    metadata = r.get("metadata", {})
                    evidence.append({
                        "text": r.get("text", "")[:200],
                        "source": metadata.get("title", "Unknown"),
                        "url": metadata.get("url", ""),
                    })

            return {
                "sentiment": parsed.get("sentiment", "Neutral"),
                "sentiment_score": float(parsed.get("sentiment_score", 0.5)),
                "key_themes": parsed.get("key_themes", []),
                "evidence": evidence,
                "summary": parsed.get("summary", response),
            }
        except json.JSONDecodeError:
            pass

    # Fallback: simple heuristic analysis
    return _heuristic_sentiment(results)


def _heuristic_sentiment(results: list[dict]) -> dict[str, Any]:
    """Fallback sentiment analysis using keyword heuristics."""
    bullish_keywords = ["beat", "growth", "strong", "bullish", "upgrade", "outperform",
                        "buy", "positive", "exceeds", "record", "surge"]
    bearish_keywords = ["miss", "decline", "weak", "bearish", "downgrade", "underperform",
                        "sell", "negative", "disappointing", "low", "drop"]

    bullish_count = 0
    bearish_count = 0
    evidence = []

    for r in results[:10]:
        text = r.get("text", "").lower()
        metadata = r.get("metadata", {})

        bullish_count += sum(1 for kw in bullish_keywords if kw in text)
        bearish_count += sum(1 for kw in bearish_keywords if kw in bearish_keywords)

        evidence.append({
            "text": r.get("text", "")[:200],
            "source": metadata.get("title", "Unknown"),
            "url": metadata.get("url", ""),
        })

    total = bullish_count + bearish_count
    if total == 0:
        score = 0.5
        sentiment = "Neutral"
    else:
        score = bullish_count / total
        if score > 0.6:
            sentiment = "Bullish"
        elif score < 0.4:
            sentiment = "Bearish"
        else:
            sentiment = "Neutral"

    return {
        "sentiment": sentiment,
        "sentiment_score": score,
        "key_themes": ["Automated analysis"],
        "evidence": evidence[:5],
        "summary": f"Sentiment analysis based on {len(results)} documents: {sentiment}",
    }


if __name__ == "__main__":
    # Test the agent
    from dotenv import load_dotenv
    load_dotenv()

    result = run("What is the sentiment around AAPL?", context={"ticker": "AAPL"})
    print(f"Sentiment: {result['sentiment']} (score: {result['sentiment_score']})")
    print(f"Key themes: {result['key_themes']}")
    print(f"Summary: {result['summary']}")
