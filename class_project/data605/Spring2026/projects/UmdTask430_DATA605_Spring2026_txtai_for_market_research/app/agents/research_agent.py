"""
Agentic search prototype.

Pipeline:
  1. Router  - inspects the user query, decides which sub-agents to fire and
               extracts a ticker if one is mentioned.
  2. Sub-agents - SEC and News. Each runs a filtered semantic search against
                  the txtai index (and optionally narrows by ticker).
  3. Synthesizer - formats the retrieved chunks into a natural-language
                   answer with inline citations.

Each step is a generator that yields events so the FastAPI / Streamlit layer
can stream progress to the user.
"""

import logging
import os
import re
import time
from typing import Any, Iterator, Optional, TypedDict

from app.pipeline.embeddings import search

_LOG = logging.getLogger(__name__)

# #############################################################################
# Constants
# #############################################################################

# Map of common tickers we track so the router can recognise them in plain
# English (e.g. "Apple" -> "AAPL").
_COMPANY_TO_TICKER = {
    "apple": "AAPL",
    "microsoft": "MSFT",
    "google": "GOOGL",
    "alphabet": "GOOGL",
    "amazon": "AMZN",
    "meta": "META",
    "facebook": "META",
    "tesla": "TSLA",
    "nvidia": "NVDA",
    "netflix": "NFLX",
    "oracle": "ORCL",
    "intel": "INTC",
    "ibm": "IBM",
    "jpmorgan": "JPM",
    "bank of america": "BAC",
    "wells fargo": "WFC",
    "goldman sachs": "GS",
    "morgan stanley": "MS",
    "citi": "C",
    "citigroup": "C",
    "visa": "V",
    "mastercard": "MA",
    "berkshire": "BRK-B",
    "walmart": "WMT",
    "costco": "COST",
    "home depot": "HD",
    "johnson & johnson": "JNJ",
    "pfizer": "PFE",
    "merck": "MRK",
    "eli lilly": "LLY",
    "abbvie": "ABBV",
    "exxon": "XOM",
    "chevron": "CVX",
    "amd": "AMD",
    "qualcomm": "QCOM",
    "broadcom": "AVGO",
    "ford": "F",
    "general motors": "GM",
}

# Keyword -> sub-agent.  Used when the LLM router is offline.  Multiple agents
# can match a single query.
_SEC_KEYWORDS = {
    "10-k",
    "10k",
    "10-q",
    "10q",
    "8-k",
    "8k",
    "filing",
    "filings",
    "proxy",
    "def 14a",
    "annual report",
    "quarterly report",
    "risk factor",
    "sec",
    "edgar",
    "form",
    "regulator",
    "compliance",
    "audit",
    "auditor",
}

_NEWS_KEYWORDS = {
    "news",
    "headline",
    "article",
    "sentiment",
    "bullish",
    "bearish",
    "analyst",
    "upgrade",
    "downgrade",
    "rumor",
    "rumour",
    "press",
    "announcement",
    "outlook",
    "forecast",
    "target price",
}

# Maximum chunks per sub-agent fed into the synthesizer.
_MAX_CHUNKS_PER_AGENT = 5


# #############################################################################
# Event types
# #############################################################################


class ResearchEvent(TypedDict):
    """
    Streaming event emitted by `run_research`.

    :param step: which pipeline stage produced this event
                 ("route" | "retrieve" | "synthesize" | "done" | "error")
    :param payload: stage-specific data (see individual stage docs)
    """

    step: str
    payload: dict[str, Any]


# #############################################################################
# Router
# #############################################################################


def _extract_ticker(query: str) -> Optional[str]:
    """
    Pull a ticker symbol out of a query.

    :param query: raw user query
    :return: ticker (e.g. "AAPL") or None if nothing recognisable found
    """
    query_lower = query.lower()
    # Try a literal $TICKER mention first ("$AAPL").
    cashtag_match = re.search(r"\$([A-Z]{1,5}(?:-[A-Z])?)", query.upper())
    if cashtag_match:
        return cashtag_match.group(1)
    # Then look for a known company name.
    for name, ticker in _COMPANY_TO_TICKER.items():
        if name in query_lower:
            return ticker
    # Finally, look for a bare 2-5 letter uppercase token.  Skip if it's a
    # common English word that happens to be all caps in the query.
    bare_match = re.search(r"\b([A-Z]{2,5}(?:-[A-Z])?)\b", query)
    if bare_match:
        candidate = bare_match.group(1)
        if candidate not in {"SEC", "CEO", "CFO", "USA", "EU", "AI", "ML"}:
            return candidate
    return None


def _route(query: str) -> dict[str, Any]:
    """
    Decide which sub-agents to fire for this query.

    :param query: raw user query
    :return: dict with keys
        - ``ticker``  : extracted ticker symbol or None
        - ``agents``  : ordered list of sub-agent names that should run
        - ``reason``  : short human-readable explanation of the routing
                         decision (shown in the UI)
    """
    query_lower = query.lower()
    ticker = _extract_ticker(query)
    sec_hit = any(kw in query_lower for kw in _SEC_KEYWORDS)
    news_hit = any(kw in query_lower for kw in _NEWS_KEYWORDS)
    # Default routing: if neither bucket is explicitly mentioned, run both
    # because the user probably wants a broad answer.
    if sec_hit and not news_hit:
        agents = ["sec"]
        reason = "Question mentions SEC / filings keywords; routing to SEC agent only."
    elif news_hit and not sec_hit:
        agents = ["news"]
        reason = (
            "Question mentions news / sentiment keywords; routing to News agent only."
        )
    else:
        agents = ["sec", "news"]
        reason = "Generic question; routing to both SEC and News agents for coverage."
    return {"ticker": ticker, "agents": agents, "reason": reason}


# #############################################################################
# Sub-agents (retrieval)
# #############################################################################


def _filter_by_ticker(results: list[dict], ticker: Optional[str]) -> list[dict]:
    """
    Keep only chunks whose stored ticker metadata matches ``ticker``.

    :param results: raw txtai search results
    :param ticker: ticker to match (case-insensitive); pass None to skip
    :return: filtered list (same shape as input)
    """
    if not ticker:
        return results
    ticker_upper = ticker.upper()
    filtered = []
    for r in results:
        # The metadata field can be a dict or a JSON-encoded string depending
        # on how txtai stored it; handle both shapes defensively.
        md = r.get("metadata") or {}
        if isinstance(md, str):
            try:
                import json

                md = json.loads(md)
            except Exception:
                md = {}
        if md.get("ticker", "").upper() == ticker_upper:
            filtered.append(r)
    return filtered


def _run_sec_agent(query: str, ticker: Optional[str]) -> list[dict]:
    """
    Retrieve top SEC chunks for the query.

    :param query: user query, used as the semantic search input
    :param ticker: optional ticker to narrow the result set
    :return: up to _MAX_CHUNKS_PER_AGENT chunk dicts with ``score``, ``text``,
             and ``metadata``
    """
    _LOG.info("SEC agent query=%s ticker=%s", query, ticker)
    raw = search(query, source_filter="sec", limit=_MAX_CHUNKS_PER_AGENT * 4)
    if ticker:
        narrowed = _filter_by_ticker(raw, ticker)
        # If the ticker filter wipes out everything, fall back to the
        # unfiltered set so the user still sees something.
        if narrowed:
            raw = narrowed
    return raw[:_MAX_CHUNKS_PER_AGENT]


def _run_news_agent(query: str, ticker: Optional[str]) -> list[dict]:
    """
    Retrieve top news chunks for the query.

    :param query: user query, used as the semantic search input
    :param ticker: optional ticker to narrow the result set
    :return: up to _MAX_CHUNKS_PER_AGENT chunk dicts
    """
    _LOG.info("News agent query=%s ticker=%s", query, ticker)
    raw = search(query, source_filter="news", limit=_MAX_CHUNKS_PER_AGENT * 4)
    if ticker:
        narrowed = _filter_by_ticker(raw, ticker)
        if narrowed:
            raw = narrowed
    return raw[:_MAX_CHUNKS_PER_AGENT]


_AGENT_FUNCS = {
    "sec": _run_sec_agent,
    "news": _run_news_agent,
}


# #############################################################################
# Synthesizer
# #############################################################################


def _format_citation(idx: int, chunk: dict) -> str:
    """
    Render a chunk as one bullet line for the citation list.

    :param idx: 1-based citation number used in the body of the answer
    :param chunk: raw txtai search result
    :return: formatted markdown line
    """
    md = chunk.get("metadata") or {}
    if isinstance(md, str):
        try:
            import json

            md = json.loads(md)
        except Exception:
            md = {}
    ticker = md.get("ticker", "?")
    source = md.get("source") or chunk.get("tags") or "?"
    filing_type = md.get("filing_type", "")
    filing_date = md.get("filing_date") or md.get("published_at", "")
    score = chunk.get("score", 0.0)
    label_parts = [str(ticker), str(source)]
    if filing_type:
        label_parts.append(str(filing_type))
    if filing_date:
        label_parts.append(str(filing_date)[:10])
    label = " | ".join(label_parts)
    snippet = (chunk.get("text") or "").strip().replace("\n", " ")[:240]
    return f"[{idx}] **{label}** (score={score:.3f})\n    > {snippet}…"


def _first_sentences(text: str, n: int = 2) -> str:
    """
    Pull the first ``n`` sentences out of a chunk for use in a prose answer.

    Uses a simple regex split on sentence-ending punctuation, then filters
    out fragments that are too short to be real sentences (table headers,
    page numbers, etc.).

    :param text: raw chunk text
    :param n: maximum number of sentences to keep
    :return: cleaned, joined sentences (no trailing newline)
    """
    cleaned = re.sub(r"\s+", " ", text or "").strip()
    parts = re.split(r"(?<=[.!?])\s+(?=[A-Z])", cleaned)
    real = [p.strip() for p in parts if len(p.strip()) > 30]
    if not real:
        return cleaned[:300]
    return " ".join(real[:n])


def _synthesize_template(query: str, route_info: dict, all_chunks: list[dict]) -> str:
    """
    Build a clean natural-language answer from retrieved chunks.

    Without an LLM available we use an extractive strategy: take the first
    1-2 sentences of the top three chunks and stitch them into a short
    prose paragraph with inline ``[N]`` citation markers. The full source
    list is rendered separately by the API/UI and is NOT included here.

    :param query: original user question (kept for downstream LLM prompt
                  parity, not used in template output)
    :param route_info: output of ``_route``; only the ticker is used
    :param all_chunks: every chunk returned by every sub-agent, in the
                       order they should be cited
    :return: short markdown paragraph with inline ``[N]`` citations
    """
    _ = query  # kept for symmetry with the LLM synthesizer.
    if not all_chunks:
        ticker = route_info.get("ticker")
        target = f"about **{ticker}**" if ticker else "for that question"
        agents = ", ".join(route_info.get("agents", []))
        return (
            f"I couldn't find relevant documents {target}. "
            f"Searched the {agents} index. Try rephrasing or asking about "
            "a different ticker (we have data for AAPL, MSFT, NVDA, JPM, "
            "TSLA, and 60+ others)."
        )
    # Take the strongest chunks first — they're already score-ordered per
    # agent, so we just slice the top three across the merged list.
    top = all_chunks[:3]
    sentences = []
    for i, chunk in enumerate(top, start=1):
        sent = _first_sentences(chunk.get("text") or "", n=2)
        if sent:
            sentences.append(f"{sent} [{i}]")
    if not sentences:
        return "I retrieved documents but couldn't extract a coherent summary."
    return " ".join(sentences)


def _synthesize_with_llm(
    query: str, route_info: dict, all_chunks: list[dict]
) -> Optional[str]:
    """
    Try to synthesise an answer using an OpenAI-compatible LLM endpoint.

    Returns None on any error so the caller can fall back to the template.

    Reads endpoint configuration from environment:
      - ``LLM_BASE_URL``  : OpenAI-compatible base URL (e.g. http://localhost:11434/v1)
      - ``LLM_API_KEY``   : API key (use any string for local Ollama)
      - ``LLM_MODEL``     : model name to use

    :param query: user query
    :param route_info: output of ``_route``
    :param all_chunks: chunks to ground the answer in
    :return: synthesized markdown answer, or None if the LLM call fails
    """
    base_url = os.getenv("LLM_BASE_URL")
    model = os.getenv("LLM_MODEL")
    if not base_url or not model:
        return None
    api_key = os.getenv("LLM_API_KEY", "not-needed")
    try:
        import httpx
    except ImportError:
        return None
    # Build the context block: each chunk numbered so the LLM can cite it.
    context_lines = []
    for i, chunk in enumerate(all_chunks, start=1):
        md = chunk.get("metadata") or {}
        if isinstance(md, str):
            import json

            try:
                md = json.loads(md)
            except Exception:
                md = {}
        ticker = md.get("ticker", "?")
        src = md.get("source") or chunk.get("tags") or "?"
        date = md.get("filing_date") or md.get("published_at", "")
        snippet = (chunk.get("text") or "").strip()[:600]
        context_lines.append(f"[{i}] ({ticker} | {src} | {date})\n{snippet}")
    context_text = "\n\n".join(context_lines)
    system = (
        "You are a financial research assistant. Answer the user's question using "
        "ONLY the provided document excerpts. Cite each claim with [N] where N is "
        "the document number. If the documents do not answer the question, say so."
    )
    user = (
        f"Question: {query}\n\n"
        f"Documents:\n{context_text}\n\n"
        f"Write a concise answer (3-5 sentences) with inline [N] citations."
    )
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        "temperature": 0.2,
    }
    try:
        with httpx.Client(timeout=60.0) as client:
            resp = client.post(
                f"{base_url.rstrip('/')}/chat/completions",
                json=payload,
                headers={"Authorization": f"Bearer {api_key}"},
            )
            resp.raise_for_status()
            data = resp.json()
        content = data["choices"][0]["message"]["content"].strip()
    except Exception as e:
        _LOG.warning("LLM synthesis failed: %s", e)
        return None
    # Sources are rendered separately by the caller, so we return only the
    # natural-language answer (with the inline ``[N]`` citation markers).
    return content


# #############################################################################
# Public entry point
# #############################################################################


def _chunk_to_source(idx: int, chunk: dict) -> dict[str, Any]:
    """
    Project a raw chunk into a compact source record for the UI / API.

    :param idx: 1-based citation index used in the answer text
    :param chunk: raw txtai search result
    :return: dict with the fields a UI needs to render a source line
             (``id``, ``score``, ``ticker``, ``source``, ``filing_type``,
             ``filing_date``, ``url``, ``snippet``)
    """
    md = chunk.get("metadata") or {}
    if isinstance(md, str):
        try:
            import json

            md = json.loads(md)
        except Exception:
            md = {}
    snippet = (chunk.get("text") or "").strip().replace("\n", " ")[:240]
    return {
        "id": idx,
        "score": float(chunk.get("score") or 0.0),
        "ticker": md.get("ticker"),
        "source": md.get("source") or chunk.get("tags"),
        "filing_type": md.get("filing_type"),
        "filing_date": md.get("filing_date") or md.get("published_at"),
        "url": md.get("url"),
        "accession_number": md.get("accession_number"),
        "snippet": snippet,
    }


def run_research(query: str) -> Iterator[ResearchEvent]:
    """
    Run the full agentic research pipeline as a streaming generator.

    Every emitted event is annotated with ``elapsed_ms`` (milliseconds since
    the start of the run) so a UI / eval harness can plot timing without
    needing its own clock.

    :param query: raw user question
    :yields: a sequence of ``ResearchEvent`` dicts in this order:
        - ``route``       : routing decision (ticker, agents, reason)
        - ``retrieve``    : one event per sub-agent with the chunks it found
        - ``synthesize``  : the final natural-language answer
        - ``done``        : terminal marker with the full timing breakdown
    """
    t_start = time.perf_counter()

    def _now_ms() -> float:
        return (time.perf_counter() - t_start) * 1000.0

    timings: dict[str, float] = {}
    # 1. Route.
    t0 = time.perf_counter()
    yield {
        "step": "route",
        "payload": {"query": query, "status": "starting", "elapsed_ms": _now_ms()},
    }
    route_info = _route(query)
    timings["route_ms"] = (time.perf_counter() - t0) * 1000.0
    yield {
        "step": "route",
        "payload": {
            "query": query,
            **route_info,
            "elapsed_ms": _now_ms(),
            "step_ms": timings["route_ms"],
        },
    }
    # 2. Retrieve from each sub-agent.
    all_chunks: list[dict] = []
    for agent_name in route_info["agents"]:
        yield {
            "step": "retrieve",
            "payload": {
                "agent": agent_name,
                "status": "running",
                "elapsed_ms": _now_ms(),
            },
        }
        t1 = time.perf_counter()
        chunks = _AGENT_FUNCS[agent_name](query, route_info.get("ticker"))
        agent_ms = (time.perf_counter() - t1) * 1000.0
        timings[f"retrieve_{agent_name}_ms"] = agent_ms
        yield {
            "step": "retrieve",
            "payload": {
                "agent": agent_name,
                "status": "complete",
                "count": len(chunks),
                "chunks": chunks,
                "elapsed_ms": _now_ms(),
                "step_ms": agent_ms,
            },
        }
        all_chunks.extend(chunks)
    # 3. Synthesize.
    yield {
        "step": "synthesize",
        "payload": {"status": "running", "elapsed_ms": _now_ms()},
    }
    t2 = time.perf_counter()
    answer = _synthesize_with_llm(query, route_info, all_chunks)
    used_llm = answer is not None
    if not answer:
        answer = _synthesize_template(query, route_info, all_chunks)
    timings["synthesize_ms"] = (time.perf_counter() - t2) * 1000.0
    sources = [_chunk_to_source(i, c) for i, c in enumerate(all_chunks, start=1)]
    timings["total_ms"] = _now_ms()
    yield {
        "step": "synthesize",
        "payload": {
            "status": "complete",
            "answer": answer,
            "sources": sources,
            "used_llm": used_llm,
            "chunk_count": len(all_chunks),
            "elapsed_ms": _now_ms(),
            "step_ms": timings["synthesize_ms"],
        },
    }
    yield {
        "step": "done",
        "payload": {
            "chunk_count": len(all_chunks),
            "timings": timings,
        },
    }


def run_research_sync(query: str) -> dict[str, Any]:
    """
    Convenience wrapper that drains ``run_research`` into a single dict.

    :param query: raw user question
    :return: dict with keys ``query``, ``route``, ``retrievals``, ``answer``,
             ``sources``, ``used_llm``, ``chunk_count``, ``timings``
    """
    route: dict[str, Any] = {}
    retrievals: list[dict[str, Any]] = []
    answer = ""
    sources: list[dict[str, Any]] = []
    used_llm = False
    chunk_count = 0
    timings: dict[str, float] = {}
    for event in run_research(query):
        step = event["step"]
        payload = event["payload"]
        if step == "route" and "agents" in payload:
            route = payload
        elif step == "retrieve" and payload.get("status") == "complete":
            retrievals.append(payload)
        elif step == "synthesize" and payload.get("status") == "complete":
            answer = payload.get("answer", "")
            sources = payload.get("sources", [])
            used_llm = bool(payload.get("used_llm"))
            chunk_count = int(payload.get("chunk_count", 0))
        elif step == "done":
            timings = payload.get("timings", {})
    return {
        "query": query,
        "route": route,
        "retrievals": retrievals,
        "answer": answer,
        "sources": sources,
        "used_llm": used_llm,
        "chunk_count": chunk_count,
        "timings": timings,
    }
