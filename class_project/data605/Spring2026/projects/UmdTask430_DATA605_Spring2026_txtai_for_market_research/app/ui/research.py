"""
Streamlit UI for the agentic research API.

While the agent runs, a "thinking" panel shows each step live (route,
per-agent retrieval, synthesis). When the answer arrives, the thinking
panel collapses into a small expander and the clean answer + sources are
rendered prominently.

Run:
  streamlit run app/ui/research.py
"""

import json
import os
import time

import httpx
import streamlit as st

API_URL = os.getenv("API_URL", "http://localhost:8000")

# #############################################################################
# Page setup
# #############################################################################

st.set_page_config(
    page_title="Market Research Agent",
    page_icon="🔎",
    layout="wide",
)
st.title("Market Research Agent")
st.caption(
    "Ask a question about any of our 67 tracked tickers. The agent picks "
    "sub-agents, retrieves evidence, and writes a cited answer."
)

# #############################################################################
# Sidebar: status + examples
# #############################################################################

with st.sidebar:
    st.subheader("Status")
    try:
        ping = httpx.get(f"{API_URL}/", timeout=2.0)
        if ping.status_code == 200:
            st.success(f"API: connected\n\n`{API_URL}`")
        else:
            st.error(f"API: HTTP {ping.status_code}")
    except Exception as e:
        st.error(f"API unreachable: {e}")
    st.divider()
    st.subheader("Examples")
    examples = [
        "What does Apple disclose as risk factors?",
        "Recent NVDA news sentiment?",
        "How does JPMorgan describe regulatory risk?",
        "What are analysts saying about Tesla?",
        "Summarize Microsoft 8-K disclosures",
    ]
    for ex in examples:
        if st.button(ex, key=f"ex_{ex[:18]}"):
            st.session_state["query_text"] = ex

# #############################################################################
# Query input
# #############################################################################

query = st.text_input(
    "Your question",
    key="query_text",
    placeholder="e.g. What are AAPL's main risk factors?",
)
go = st.button("Research", type="primary")

# #############################################################################
# Pipeline runner
# #############################################################################


def _format_thinking_line(step: str, payload: dict) -> str:
    """
    Render one streaming event as a single line in the live "thinking"
    transcript.

    :param step: event step name from the API
    :param payload: event payload from the API
    :return: human-readable line; empty string if the event isn't worth
             showing in the live transcript
    """
    elapsed = payload.get("elapsed_ms")
    elapsed_str = f"`{elapsed:.0f}ms`" if elapsed is not None else ""
    if step == "route" and "agents" in payload:
        ticker = payload.get("ticker") or "—"
        agents = ", ".join(payload.get("agents", []))
        return (
            f"**Routed** {elapsed_str} → ticker=`{ticker}`, agents=`{agents}`. "
            f"_{payload.get('reason', '')}_"
        )
    if step == "retrieve" and payload.get("status") == "running":
        return f"**Retrieving** {elapsed_str} from `{payload.get('agent')}` agent…"
    if step == "retrieve" and payload.get("status") == "complete":
        return (
            f"**Retrieved** {elapsed_str} from `{payload.get('agent')}` "
            f"agent → {payload.get('count', 0)} chunk(s) in "
            f"`{payload.get('step_ms', 0):.0f}ms`"
        )
    if step == "synthesize" and payload.get("status") == "running":
        return f"**Synthesizing** {elapsed_str}…"
    if step == "synthesize" and payload.get("status") == "complete":
        mode = "LLM" if payload.get("used_llm") else "extractive"
        return (
            f"**Synthesized** {elapsed_str} ({mode}) in "
            f"`{payload.get('step_ms', 0):.0f}ms`"
        )
    return ""


def _run(query: str) -> None:
    """
    Hit ``/research/stream`` and render each event live in a "thinking"
    panel; collapse it once the final answer arrives.

    :param query: user query (already non-empty)
    """
    thinking_holder = st.empty()
    answer_holder = st.empty()
    thinking_lines: list[str] = []
    final_payload: dict | None = None
    final_timings: dict | None = None
    wall_t0 = time.perf_counter()
    try:
        with httpx.stream(
            "POST",
            f"{API_URL}/research/stream",
            json={"query": query},
            timeout=120.0,
        ) as response:
            response.raise_for_status()
            for raw in response.iter_lines():
                line = raw.decode() if isinstance(raw, bytes) else raw
                if not line or not line.startswith("data:"):
                    continue
                event = json.loads(line[5:].strip())
                step = event["step"]
                payload = event["payload"]
                # Keep the live transcript updated.
                tl = _format_thinking_line(step, payload)
                if tl:
                    thinking_lines.append(tl)
                    with thinking_holder.container():
                        st.markdown("**Thinking…**")
                        for ln in thinking_lines:
                            st.markdown(f"- {ln}")
                if step == "synthesize" and payload.get("status") == "complete":
                    final_payload = payload
                elif step == "done":
                    final_timings = payload.get("timings", {})
                elif step == "error":
                    st.error(payload.get("message", "server-side error"))
                    return
    except httpx.HTTPError as e:
        st.error(f"Network error talking to {API_URL}: {e}")
        return
    except json.JSONDecodeError as e:
        st.error(f"Could not parse server response: {e}")
        return
    if final_payload is None:
        st.warning("Stream ended before the agent produced an answer.")
        return
    # Collapse the live thinking transcript into a small expander.
    wall_ms = (time.perf_counter() - wall_t0) * 1000.0
    with thinking_holder.container():
        with st.expander(
            f"Show agent trace ({len(thinking_lines)} steps, "
            f"{wall_ms:.0f}ms wall time)",
            expanded=False,
        ):
            for ln in thinking_lines:
                st.markdown(f"- {ln}")
            if final_timings:
                st.markdown("**Timing breakdown**")
                cols = st.columns(len(final_timings))
                for col, (k, v) in zip(cols, final_timings.items()):
                    col.metric(k, f"{v:.0f}ms")
    # Render the clean answer + sources.
    with answer_holder.container():
        st.markdown("### Answer")
        if final_payload.get("used_llm"):
            st.caption("Generated with LLM synthesis")
        else:
            st.caption(
                "Extractive synthesis — set LLM_BASE_URL / LLM_API_KEY / "
                "LLM_MODEL on the API server to enable LLM prose generation"
            )
        st.markdown(final_payload.get("answer", ""))
        sources = final_payload.get("sources", [])
        if sources:
            st.markdown("### Sources")
            for s in sources:
                ticker = s.get("ticker") or "?"
                src = s.get("source") or "?"
                ftype = s.get("filing_type") or ""
                date = (s.get("filing_date") or "")[:10]
                score = s.get("score") or 0.0
                idx = s.get("id")
                header_bits = [f"[{idx}]", ticker, src]
                if ftype:
                    header_bits.append(ftype)
                if date:
                    header_bits.append(date)
                header_bits.append(f"score={score:.3f}")
                with st.expander(" · ".join(header_bits)):
                    st.write(s.get("snippet", ""))
                    if s.get("accession_number"):
                        st.caption(f"Accession: {s['accession_number']}")
                    if s.get("url"):
                        st.markdown(f"[Open source]({s['url']})")


if go and query and query.strip():
    _run(query.strip())
elif go and not query.strip():
    st.warning("Type a question first.")
