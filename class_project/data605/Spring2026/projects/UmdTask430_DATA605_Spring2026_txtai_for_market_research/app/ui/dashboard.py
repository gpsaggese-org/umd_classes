"""
Dashboard UI component for Streamlit.

Renders:
- Risk flags (from due diligence agent)
- Earnings KPI table (from earnings agent)
"""

from typing import Any

import streamlit as st

from app.agents.diligence import run as run_diligence
from app.agents.earnings import run as run_earnings


def render(ticker: str) -> None:
    """
    Render the dashboard for a given ticker.

    :param ticker: stock ticker symbol (e.g., ``"AAPL"``)
    """
    st.header(f"Market Research Dashboard: {ticker}")
    # Run the agents that have data sources wired up.
    with st.spinner(f"Analyzing {ticker}..."):
        diligence_result = run_diligence(
            f"What are the key risks for {ticker}?",
            context={"ticker": ticker},
        )
        earnings_result = run_earnings(
            f"What are the latest earnings for {ticker}?",
            context={"ticker": ticker},
        )
    # Risk flags occupy the top of the page.
    st.subheader("Risk Flags")
    _render_risk_flags(diligence_result)
    # Earnings KPI table follows.
    st.subheader("Earnings KPIs")
    _render_earnings_table(earnings_result)


def _render_risk_flags(result: dict[str, Any]) -> None:
    """
    Render risk flags from due diligence analysis grouped by severity.
    """
    risk_flags = result.get("risk_flags", [])
    if not risk_flags:
        st.info("No significant risks identified")
        return
    high_risks = [r for r in risk_flags if r.get("severity") == "high"]
    medium_risks = [r for r in risk_flags if r.get("severity") == "medium"]
    low_risks = [r for r in risk_flags if r.get("severity") == "low"]
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
    """
    Render the earnings KPI table.
    """
    kpi_trends = result.get("kpi_trends", [])
    earnings_summary = result.get("earnings_summary", "")
    if not kpi_trends:
        st.info(earnings_summary or "No earnings data available")
        return
    rows = []
    for kpi in kpi_trends:
        rows.append(
            {
                "Metric": kpi.get("metric", "N/A"),
                "Current": kpi.get("current_value", "N/A"),
                "Prior": kpi.get("prior_value", "N/A"),
                "Change": kpi.get("change", "N/A"),
            }
        )
    st.table(rows)
    tone = result.get("management_tone", "")
    if tone:
        st.caption(f"Management tone: {tone[:200]}")
