"""
txtai Market Research Platform - Streamlit Entry Point

This is the main entry point for the Streamlit application.
It provides two tabs:
1. Dashboard: Company ticker input with risk flags and earnings KPIs
2. Research Chat: Free-text Q&A routed through the orchestrator agent

Usage:
    streamlit run app/main.py
"""

import os

import streamlit as st

from app.storage import get_cache_manager, get_keydb_client
from app.ui.dashboard import render as render_dashboard
from app.ui.chat import render as render_chat


# Page configuration
st.set_page_config(
    page_title="txtai Market Research",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)


def main():
    """Main application entry point."""
    # Initialize KeyDB connection on startup
    cache_manager = get_cache_manager()
    keydb_connected = get_keydb_client().ping()

    # Sidebar configuration
    with st.sidebar:
        st.title("txtai Market Research")
        st.markdown("Multi-agent market research platform powered by txtai")

        # KeyDB Status Indicator
        if keydb_connected:
            st.success("KeyDB: Connected")
            # Show cache stats
            stats = cache_manager.get_stats()
            with st.expander("Cache Statistics"):
                st.metric("Prices Cached", stats["prices"])
                st.metric("Semantic Cache", stats["semantic"])
                st.metric("Active Sessions", stats["sessions"])
        else:
            st.error("KeyDB: Disconnected")

        st.divider()

        # API Key configuration
        api_key = st.text_input(
            "OpenAI API Key",
            type="password",
            value=os.getenv("OPENAI_API_KEY", ""),
            help="Enter your OpenAI API key for LLM inference",
        )

        if api_key:
            os.environ["OPENAI_API_KEY"] = api_key

        st.divider()

        # Ticker input (used in Dashboard tab)
        st.subheader("Company Lookup")
        ticker = st.text_input(
            "Ticker Symbol",
            placeholder="AAPL",
            max_chars=5,
            help="Enter a stock ticker symbol",
        ).upper()

        # Store ticker in session state for dashboard to use
        st.session_state.ticker = ticker

        st.divider()

        # Utility links
        st.markdown("### Resources")
        st.markdown("- [txtai Documentation](https://neuml.github.io/txtai/)")
        st.markdown("- [GitHub Repo](#)")

    # Main content area with tabs
    tab1, tab2 = st.tabs(["📊 Dashboard", "💬 Research Chat"])

    with tab1:
        if ticker:
            render_dashboard(ticker)
        else:
            st.info("Enter a ticker symbol in the sidebar to view the dashboard")

    with tab2:
        render_chat()


if __name__ == "__main__":
    main()
