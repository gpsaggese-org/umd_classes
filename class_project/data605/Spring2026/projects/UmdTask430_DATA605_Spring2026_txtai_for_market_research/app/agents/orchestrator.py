"""
Orchestrator Agent for txtai market research platform.

This is the main routing agent that:
1. Receives user queries
2. Classifies intent (sentiment / diligence / web research / earnings / regulatory)
3. Calls relevant sub-agents via txtai Agent tool calling
4. Merges and ranks results before returning to UI
"""

import os
from typing import Any

from txtai import Agent, LLM

from app.agents.sentiment import run as run_sentiment
from app.agents.diligence import run as run_diligence
from app.agents.web_research import run as run_web_research
from app.agents.earnings import run as run_earnings
from app.agents.regulatory import run as run_regulatory


# System prompt for the orchestrator
SYSTEM_PROMPT = """You are the Orchestrator for a market research platform.

Your role is to:
1. Analyze the user's query to determine their intent
2. Route to the appropriate specialist agent(s):
   - SENTIMENT: Market sentiment, investor psychology, bullish/bearish analysis
   - DILIGENCE: M&A due diligence, risk identification, synergy assessment
   - WEB_RESEARCH: Competitive intelligence, product launches, market positioning
   - EARNINGS: Earnings call analysis, KPI trends, guidance changes, management tone
   - REGULATORY: SEC filings, regulatory risk, compliance issues, enforcement signals

3. Merge and synthesize results from multiple agents when needed
4. Provide clear, actionable insights with source citations

Always be specific and cite your sources. If multiple agents provide relevant
information, synthesize their findings into a coherent response.
"""


def create_agent() -> Agent:
    """
    Create and configure the orchestrator Agent.

    Uses txtai's Agent class with:
    - Ollama qwen2.5:7b as primary LLM
    - OpenAI gpt-4o-mini as fallback
    - Tool bindings for each sub-agent
    """
    # Configure LLM with fallback
    llm = get_llm()

    # Define tools for each sub-agent
    # txtai Agent tools are functions that the LLM can call
    tools = {
        "sentiment_analysis": {
            "function": run_sentiment,
            "description": "Analyze market sentiment and investor psychology. Use for questions about bullish/bearish trends, market mood, or investor sentiment.",
        },
        "due_diligence": {
            "function": run_diligence,
            "description": "Perform M&A due diligence analysis. Use for questions about risks, synergies, deal assessment, or acquisition targets.",
        },
        "web_research": {
            "function": run_web_research,
            "description": "Research competitive intelligence from public web sources. Use for questions about competitors, product launches, or market positioning.",
        },
        "earnings_analysis": {
            "function": run_earnings,
            "description": "Analyze earnings calls and KPIs. Use for questions about earnings results, guidance changes, management tone, or financial metrics.",
        },
        "regulatory_analysis": {
            "function": run_regulatory,
            "description": "Analyze SEC filings and regulatory risk. Use for questions about compliance, enforcement, regulatory issues, or filing disclosures.",
        },
    }

    # Create the txtai Agent
    # The Agent class handles:
    # - LLM invocation
    # - Tool routing based on LLM decisions
    # - Response synthesis
    agent = Agent(
        llm=llm,
        tools=tools,
        system_prompt=SYSTEM_PROMPT,
    )

    return agent


def get_llm() -> LLM:
    """
    Get configured LLM using Ollama.

    Primary: Ollama qwen2.5:7b (or custom model via OLLAMA_LLM_MODEL)
    Fallback: OpenAI gpt-4o-mini (if Ollama not configured)
    """
    ollama_host = os.getenv("OLLAMA_HOST", "http://localhost:11434")
    ollama_model = os.getenv("OLLAMA_LLM_MODEL", "qwen2.5:7b")

    # Try Ollama first
    try:
        return LLM(
            model=f"ollama:{ollama_model}@{ollama_host}",
        )
    except Exception:
        # Fallback to OpenAI if Ollama is not available
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key:
            return LLM(
                model="openai:gpt-4o-mini",
                api_key=api_key,
            )
        else:
            # Final fallback to HuggingFace
            return LLM(
                model="mistralai/Mistral-7B-Instruct-v0.2",
            )


# Global singleton agent instance
_orchestrator: Agent | None = None


def get_orchestrator() -> Agent:
    """Get or create the singleton orchestrator agent."""
    global _orchestrator
    if _orchestrator is None:
        _orchestrator = create_agent()
    return _orchestrator


def run(query: str, context: dict | None = None) -> dict[str, Any]:
    """
    Run the orchestrator with a user query.

    Args:
        query: The user's question or request
        context: Optional context dict with:
            - ticker: Stock ticker symbol (e.g., "AAPL")
            - time_range: Time range for analysis (e.g., "last 30 days")

    Returns:
        Dict with:
            - response: The synthesized response text
            - sources: List of source documents cited
            - agents_used: List of sub-agents that were called
            - confidence: Confidence score (0-1) in the response
    """
    if context is None:
        context = {}

    # Add context to the query
    ticker = context.get("ticker", "")
    if ticker:
        enhanced_query = f"For {ticker}: {query}"
    else:
        enhanced_query = query

    # Run the orchestrator agent
    # txtai's Agent.__call__ handles the full workflow:
    # 1. LLM analyzes query and decides which tools to call
    # 2. Tools are executed with LLM-provided arguments
    # 3. LLM synthesizes final response from tool results
    agent = get_orchestrator()
    response = agent(enhanced_query)

    # Parse the response to extract metadata
    # txtai returns the raw LLM response, we need to structure it
    result = {
        "response": response if isinstance(response, str) else str(response),
        "sources": [],
        "agents_used": [],
        "confidence": 0.8,  # Default confidence
    }

    # Try to extract sources from the response
    # Sub-agents should include source markers in their output
    if "[Sources:" in result["response"]:
        sources_section = result["response"].split("[Sources:")[1].split("]")[0]
        result["sources"] = [s.strip() for s in sources_section.split(",") if s.strip()]

    # Detect which agents were used based on response content
    agent_indicators = {
        "sentiment": ["sentiment", "bullish", "bearish", "neutral"],
        "diligence": ["risk", "synergy", "due diligence", "M&A"],
        "web_research": ["competitor", "product launch", "market position"],
        "earnings": ["earnings", "KPI", "guidance", "revenue"],
        "regulatory": ["SEC", "filing", "regulatory", "compliance"],
    }

    response_lower = result["response"].lower()
    for agent_name, indicators in agent_indicators.items():
        if any(ind in response_lower for ind in indicators):
            result["agents_used"].append(agent_name)

    return result


if __name__ == "__main__":
    # Test the orchestrator
    from dotenv import load_dotenv
    load_dotenv()

    result = run("What is the sentiment around AAPL?", context={"ticker": "AAPL"})
    print(f"Response: {result['response']}")
    print(f"Agents used: {result['agents_used']}")
    print(f"Sources: {result['sources']}")
