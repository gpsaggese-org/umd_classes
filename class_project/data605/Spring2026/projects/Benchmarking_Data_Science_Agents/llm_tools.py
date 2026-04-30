"""
llm_tools.py
------------
Claude API integration via langchain-anthropic.

Defines three LangChain tools that the LangGraph agent calls at
specific pipeline nodes to generate natural-language analysis:

  1. interpret_clusters  -- describe what each agent cluster means
  2. analyse_gaps        -- explain capability strengths and weaknesses
  3. write_summary       -- produce the executive summary for the report

Why Claude over OpenAI?
  - langchain-anthropic is a drop-in replacement for langchain-openai
  - Same LangChain tool/chain interface, different model underneath
  - Set ANTHROPIC_API_KEY in .env to use

Dry-run mode
  Set LLM_DRY_RUN=true in .env to skip real API calls and return
  placeholder text. Useful for testing the pipeline without spending tokens.
"""

import os
import json
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain_anthropic import ChatAnthropic

load_dotenv()

DRY_RUN    = os.getenv("LLM_DRY_RUN", "false").lower() == "true"
MODEL_NAME = os.getenv("CLAUDE_MODEL", "claude-sonnet-4-20250514")


def get_llm() -> ChatAnthropic:
    """Initialise the Claude LLM client."""
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key and not DRY_RUN:
        raise EnvironmentError(
            "ANTHROPIC_API_KEY not set.\n"
            "Add it to your .env file or set LLM_DRY_RUN=true to skip LLM calls."
        )
    return ChatAnthropic(
        model=MODEL_NAME,
        api_key=api_key or "dry-run-key",
        max_tokens=1024,
        temperature=0.3,    # Low temperature: analytical, consistent output
    )


def _call_llm(prompt: str) -> str:
    """Internal helper — call Claude or return dry-run placeholder."""
    if DRY_RUN:
        return f"[DRY RUN] LLM response for prompt starting: {prompt[:80]}..."
    llm = get_llm()
    response = llm.invoke(prompt)
    return response.content


# ── Tool 1: Interpret Clusters ────────────────────────────────────────────────

@tool
def interpret_clusters(cluster_summary: str) -> str:
    """
    Given a JSON summary of agent clusters and their mean scores per benchmark,
    return a plain-English description of what each cluster represents
    in terms of capability profile.

    Parameters
    ----------
    cluster_summary : JSON string with structure:
        { "cluster_1": {"agents": [...], "mean_scores": {...}}, ... }
    """
    prompt = f"""You are analysing AI agent benchmark results for a data science research report.

Below is a summary of agent clusters based on their performance across 5 benchmarks
(DataSciBench, DSBench, MLE-Bench, GAIA, SWE-bench). Each benchmark tests different
capabilities: data analysis, ML engineering, reasoning, and software engineering.

Cluster summary (JSON):
{cluster_summary}

For each cluster, write 2-3 sentences describing:
1. What capability profile defines this cluster (strong/weak on which benchmarks)
2. What type of AI agent this cluster likely represents
3. A short label for the cluster (e.g. "General-purpose leaders", "ML specialists")

Be specific and analytical. Use benchmark names directly."""

    return _call_llm(prompt)


# ── Tool 2: Analyse Capability Gaps ──────────────────────────────────────────

@tool
def analyse_gaps(gaps_summary: str) -> str:
    """
    Given a summary of agent strengths and gaps across benchmarks,
    return an analytical narrative suitable for the research report.

    Parameters
    ----------
    gaps_summary : JSON string listing agents with their strength/gap benchmarks
    """
    prompt = f"""You are writing a capability gap analysis for a research report comparing
AI agents across 5 data science benchmarks.

Below is a summary of each agent's benchmark strengths (z-score > 1) and
gaps (z-score < -1) relative to their own average performance.

Gap summary (JSON):
{gaps_summary}

Write a 3-4 paragraph analysis covering:
1. General patterns: which benchmarks most frequently appear as gaps vs strengths
2. Notable agents: who is the most consistent performer, who is the most specialised
3. What these gaps reveal about the differences between benchmarks
4. Any surprising findings

Write in an academic but readable tone, suitable for a data systems research report."""

    return _call_llm(prompt)


# ── Tool 3: Write Executive Summary ──────────────────────────────────────────

@tool
def write_summary(findings: str) -> str:
    """
    Given a JSON object summarising all analysis findings, write a concise
    executive summary for the final research report.

    Parameters
    ----------
    findings : JSON string with keys: n_agents, n_benchmarks, top_agent,
               most_correlated_pair, least_correlated_pair, n_clusters,
               biggest_gap_agent
    """
    prompt = f"""You are writing the executive summary of a research report titled
"Comparative Analysis of AI Data Science Benchmarks".

The report studied {5} benchmarks (DataSciBench, DSBench, MLE-Bench, GAIA, SWE-bench)
and compared AI agent performance across them.

Key findings (JSON):
{findings}

Write a concise executive summary (4-5 sentences) that:
1. States what was studied and how many agents/benchmarks were analysed
2. Highlights the most important finding about benchmark correlation or similarity
3. Describes the main capability gap or specialisation pattern found
4. Draws one actionable conclusion for a practitioner choosing which benchmark to trust

Write in clear, academic English. No bullet points — flowing prose only."""

    return _call_llm(prompt)


# ── Utility: build cluster summary from DataFrames ───────────────────────────

def build_cluster_summary(matrix_df: pd.DataFrame, cluster_df: pd.DataFrame) -> str:
    """
    Build the JSON input for interpret_clusters() from DataFrames.
    Called by the LangGraph agent node before invoking the tool.
    """
    merged = matrix_df.merge(cluster_df[["agent", "kmeans_cluster"]], on="agent", how="left")
    score_cols = [c for c in matrix_df.columns if c not in ("agent",)]
    summary = {}
    for cluster_id in sorted(merged["kmeans_cluster"].dropna().unique()):
        group = merged[merged["kmeans_cluster"] == cluster_id]
        summary[f"cluster_{int(cluster_id)}"] = {
            "agents":      group["agent"].tolist(),
            "mean_scores": {
                col: round(group[col].mean(), 1)
                for col in score_cols
                if col in group.columns
            }
        }
    return json.dumps(summary, indent=2)


def build_gaps_summary(gaps_df: pd.DataFrame, top_n: int = 8) -> str:
    """
    Build the JSON input for analyse_gaps() from the gaps DataFrame.
    """
    top_agents = (
        gaps_df.groupby("agent")["score_norm"].mean()
        .nlargest(top_n).index.tolist()
    )
    summary = {}
    for agent in top_agents:
        agent_gaps = gaps_df[gaps_df["agent"] == agent]
        summary[agent] = {
            "strengths": agent_gaps[agent_gaps["flag"] == "strength"]["benchmark"].tolist(),
            "gaps":      agent_gaps[agent_gaps["flag"] == "gap"]["benchmark"].tolist(),
        }
    return json.dumps(summary, indent=2)


def build_findings_summary(
    matrix_df: pd.DataFrame,
    corr_df: pd.DataFrame,
    clustering: dict,
    gaps_df: pd.DataFrame,
) -> str:
    """Build the JSON input for write_summary()."""
    score_cols = [c for c in matrix_df.columns if c not in ("agent",)]
    top_agent  = matrix_df.set_index("agent")[score_cols].mean(axis=1).idxmax()

    corr_vals = corr_df.set_index(corr_df.columns[0]) if corr_df.columns[0] != corr_df.index[0] else corr_df
    np_corr = corr_vals.values
    np.fill_diagonal(np_corr, np.nan)
    idx = np.unravel_index(np.nanargmax(np_corr), np_corr.shape)
    most_corr   = f"{corr_vals.index[idx[0]]} & {corr_vals.columns[idx[1]]}"
    idx2 = np.unravel_index(np.nanargmin(np_corr), np_corr.shape)
    least_corr  = f"{corr_vals.index[idx2[0]]} & {corr_vals.columns[idx2[1]]}"

    biggest_gap = (
        gaps_df[gaps_df["flag"] == "gap"]
        .groupby("agent").size().idxmax()
    )

    import numpy as np
    findings = {
        "n_agents":              len(matrix_df),
        "n_benchmarks":          len(score_cols),
        "top_agent":             top_agent,
        "most_correlated_pair":  most_corr,
        "least_correlated_pair": least_corr,
        "n_clusters":            clustering["best_k"],
        "biggest_gap_agent":     biggest_gap,
    }
    return json.dumps(findings, indent=2)
