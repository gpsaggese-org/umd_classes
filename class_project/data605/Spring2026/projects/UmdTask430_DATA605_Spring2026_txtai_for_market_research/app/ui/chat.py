"""
Chat UI component for Streamlit.

Provides a Q&A interface backed by the orchestrator agent.
Supports streaming responses with source citations.
"""

import streamlit as st

from app.agents.orchestrator import run as run_orchestrator


def render() -> None:
    """Render the research chat interface."""
    st.header("Research Chat")
    st.caption("Ask questions about companies, markets, or investments")

    # Initialize chat history in session state
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if message.get("sources"):
                _render_sources(message["sources"])

    # Chat input
    if prompt := st.chat_input("Ask about a company or market..."):
        # Add user message to history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate assistant response
        with st.chat_message("assistant"):
            with st.spinner("Researching..."):
                response = _generate_response(prompt)

            st.markdown(response["content"])
            if response.get("sources"):
                _render_sources(response["sources"])

        # Add assistant response to history
        st.session_state.messages.append(response)


def _generate_response(prompt: str) -> dict:
    """
    Generate a response using the orchestrator agent.

    Args:
        prompt: User's question

    Returns:
        Dict with content and sources
    """
    # Extract ticker from prompt if present
    ticker = _extract_ticker(prompt)

    # Run orchestrator
    result = run_orchestrator(prompt, context={"ticker": ticker} if ticker else {})

    return {
        "role": "assistant",
        "content": result.get("response", "I couldn't generate a response."),
        "sources": result.get("sources", []),
        "agents_used": result.get("agents_used", []),
    }


def _extract_ticker(prompt: str) -> str | None:
    """
    Extract stock ticker from user prompt.

    Simple heuristic: look for uppercase 1-5 letter words.
    """
    import re

    # Common ticker patterns
    patterns = [
        r"\$([A-Z]{1,5})\b",  # $AAPL
        r"\b([A-Z]{1,5})\b",  # AAPL (standalone uppercase)
    ]

    for pattern in patterns:
        matches = re.findall(pattern, prompt)
        if matches:
            return matches[0]

    return None


def _render_sources(sources: list[str]) -> None:
    """Render source citations."""
    if not sources:
        return

    with st.expander("Sources", expanded=False):
        for i, source in enumerate(sources, 1):
            st.markdown(f"{i}. {source}")


def clear_chat() -> None:
    """Clear chat history."""
    st.session_state.messages = []
