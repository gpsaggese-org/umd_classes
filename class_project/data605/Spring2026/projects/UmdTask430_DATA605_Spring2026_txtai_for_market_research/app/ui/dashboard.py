"""
Dashboard UI component for Streamlit.

Renders:
- Sentiment gauge
- Risk flags
- Earnings KPI table
- Top news feed
"""

from typing import Any

import plotly.graph_objects as go
import streamlit as st

from app.agents.orchestrator import run as run_orchestrator
from app.agents.sentiment import run as run_sentiment
from app.agents.diligence import run as run_diligence
from app.agents.earnings import run as run_earnings


def render(ticker: str) -> None:
    """
    Render the dashboard for a given ticker.

    Args:
        ticker: Stock ticker symbol (e.g., "AAPL")
    """
    st.header(f"Market Research Dashboard: {ticker}")

    # Run all agents in parallel
    with st.spinner(f"Analyzing {ticker}..."):
        sentiment_result = run_sentiment(
            f"What is the sentiment for {ticker}?",
            context={"ticker": ticker}
        )
        diligence_result = run_diligence(
            f"What are the key risks for {ticker}?",
            context={"ticker": ticker}
        )
        earnings_result = run_earnings(
            f"What are the latest earnings for {ticker}?",
            context={"ticker": ticker}
        )

    # Create dashboard columns
    col1, col2 = st.columns(2)

    with col1:
        _render_sentiment_gauge(sentiment_result)

    with col2:
        _render_risk_flags(diligence_result)

    # Earnings KPI table
    st.subheader("Earnings KPIs")
    _render_earnings_table(earnings_result)

    # Top news feed
    st.subheader("Recent News & Insights")
    _render_news_feed(sentiment_result)


def _render_sentiment_gauge(result: dict[str, Any]) -> None:
    """Render a sentiment gauge chart using Plotly."""
    sentiment = result.get("sentiment", "Neutral")
    score = result.get("sentiment_score", 0.5)

    # Map sentiment to color
    if sentiment == "Bullish":
        color = "#00CC96"  # Green
    elif sentiment == "Bearish":
        color = "#EF553B"  # Red
    else:
        color = "#636EFA"  # Blue

    # Create gauge chart
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=score,
        domain={"x": [0, 1], "y": [0, 1]},
        title={
            "text": f"Market Sentiment: {sentiment}",
            "font": {"size": 16}
        },
        number={"prefix": "", "suffix": "", "font": {"size": 30}},
        gauge={
            "axis": {
                "range": [0, 1],
                "tickwidth": 1,
                "tickcolor": "white"
            },
            "bar": {"color": color},
            "bgcolor": "white",
            "borderwidth": 2,
            "bordercolor": "gray",
            "steps": [
                {"range": [0, 0.4], "color": "#EF553B40"},  # Bearish zone
                {"range": [0.4, 0.6], "color": "#636EFA40"},  # Neutral zone
                {"range": [0.6, 1], "color": "#00CC9640"},  # Bullish zone
            ],
        }
    ))

    fig.update_layout(height=250, margin={"l": 20, "r": 20, "t": 40, "b": 20})
    st.plotly_chart(fig, use_container_width=True)

    # Show key themes
    themes = result.get("key_themes", [])
    if themes:
        st.caption("Key themes: " + ", ".join(themes[:3]))


def _render_risk_flags(result: dict[str, Any]) -> None:
    """Render risk flags from due diligence analysis."""
    risk_flags = result.get("risk_flags", [])

    if not risk_flags:
        st.info("No significant risks identified")
        return

    # Categorize by severity
    high_risks = [r for r in risk_flags if r.get("severity") == "high"]
    medium_risks = [r for r in risk_flags if r.get("severity") == "medium"]
    low_risks = [r for r in risk_flags if r.get("severity") == "low"]

    # Display by severity
    if high_risks:
        st.error(f"**High Risk ({len(high_risks)})**")
        for risk in high_risks[:3]:
            st.write(f"- {risk.get('description', 'N/A')[:150]}")

    if medium_risks:
        st.warning(f"**Medium Risk ({len(medium_risks)})**")
        for risk in medium_risks[:3]:
            st.write(f"- {risk.get('description', 'N/A')[:150]}")

    if low_risks:
        st.success(f"**Low Risk ({len(low_risks)})**")
        for risk in low_risks[:3]:
            st.write(f"- {risk.get('description', 'N/A')[:150]}")


def _render_earnings_table(result: dict[str, Any]) -> None:
    """Render earnings KPI table."""
    kpi_trends = result.get("kpi_trends", [])
    earnings_summary = result.get("earnings_summary", "")

    if not kpi_trends:
        st.info(earnings_summary if earnings_summary else "No earnings data available")
        return

    # Create table data
    data = []
    for kpi in kpi_trends:
        data.append({
            "Metric": kpi.get("metric", "N/A"),
            "Current": kpi.get("current_value", "N/A"),
            "Prior": kpi.get("prior_value", "N/A"),
            "Change": kpi.get("change", "N/A"),
        })

    st.table(data)

    # Show management tone
    tone = result.get("management_tone", "")
    if tone:
        st.caption(f"Management tone: {tone[:200]}")


def _render_news_feed(result: dict[str, Any]) -> None:
    """Render news feed from sentiment analysis."""
    evidence = result.get("evidence", [])

    if not evidence:
        st.info("No recent news available")
        return

    for item in evidence[:5]:
        source = item.get("source", "Unknown")
        text = item.get("text", "")[:200]
        url = item.get("url", "")

        col1, col2 = st.columns([4, 1])
        with col1:
            st.write(f"**{source}**")
            st.write(text + "...")
        with col2:
            if url:
                st.markdown(f"[Read more]({url})")

        st.divider()
