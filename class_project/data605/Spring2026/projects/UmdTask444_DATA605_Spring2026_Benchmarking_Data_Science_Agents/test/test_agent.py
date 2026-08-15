"""
test_agent.py
-------------
Tests for the LangGraph pipeline nodes (src/agent.py) and
LLM tools (src/llm_tools.py).

All tests run with LLM_DRY_RUN=true so no real API calls are made.
The dry-run mode returns predictable placeholder strings, letting us
verify that the pipeline wiring is correct without spending tokens.
"""

import os
import pytest
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

# Force dry-run before importing anything that loads dotenv
os.environ["LLM_DRY_RUN"] = "true"
os.environ["ANTHROPIC_API_KEY"] = "test-key-not-real"

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import db
from db import get_conn


# ── Fixtures ──────────────────────────────────────────────────────────────────

@pytest.fixture(autouse=True)
def reset_db():
    db.close()
    yield
    db.close()


# ── llm_tools: dry-run mode ───────────────────────────────────────────────────

class TestLLMToolsDryRun:
    def test_interpret_clusters_returns_string(self):
        from llm_tools import interpret_clusters
        result = interpret_clusters.invoke({"cluster_summary": '{"cluster_1": {"agents": ["A"], "mean_scores": {"bench1": 80}}}'})
        assert isinstance(result, str)
        assert len(result) > 0

    def test_analyse_gaps_returns_string(self):
        from llm_tools import analyse_gaps
        result = analyse_gaps.invoke({"gaps_summary": '{"AgentA": {"strengths": ["bench1"], "gaps": ["bench2"]}}'})
        assert isinstance(result, str)
        assert len(result) > 0

    def test_write_summary_returns_string(self):
        from llm_tools import write_summary
        result = write_summary.invoke({"findings": '{"n_agents": 10, "top_agent": "GPT-4o"}'})
        assert isinstance(result, str)
        assert len(result) > 0

    def test_dry_run_label_in_output(self):
        """Dry-run responses should be clearly marked."""
        from llm_tools import write_summary
        result = write_summary.invoke({"findings": "{}"})
        assert "DRY RUN" in result


# ── llm_tools: helper builders ────────────────────────────────────────────────

class TestLLMToolHelpers:
    def _make_matrix_df(self):
        import pandas as pd
        return pd.DataFrame({
            "agent":      ["AgentA", "AgentB", "AgentC"],
            "bench1":     [80.0, 60.0, 40.0],
            "bench2":     [70.0, 55.0, 90.0],
        })

    def _make_cluster_df(self):
        import pandas as pd
        return pd.DataFrame({
            "agent":          ["AgentA", "AgentB", "AgentC"],
            "kmeans_cluster": [0, 0, 1],
            "hier_cluster":   [1, 1, 2],
        })

    def _make_gaps_df(self):
        import pandas as pd
        return pd.DataFrame({
            "agent":      ["AgentA", "AgentA", "AgentB"],
            "benchmark":  ["bench1", "bench2", "bench1"],
            "score_norm": [80.0, 40.0, 60.0],
            "z_score":    [1.2, -1.2, 0.0],
            "flag":       ["strength", "gap", "average"],
        })

    def test_build_cluster_summary_is_valid_json(self):
        import json
        from llm_tools import build_cluster_summary
        summary = build_cluster_summary(self._make_matrix_df(), self._make_cluster_df())
        parsed = json.loads(summary)
        assert "cluster_0" in parsed or "cluster_1" in parsed

    def test_build_cluster_summary_contains_agents(self):
        import json
        from llm_tools import build_cluster_summary
        summary = json.loads(build_cluster_summary(self._make_matrix_df(), self._make_cluster_df()))
        all_agents = []
        for cluster in summary.values():
            all_agents.extend(cluster["agents"])
        assert "AgentA" in all_agents

    def test_build_gaps_summary_is_valid_json(self):
        import json
        from llm_tools import build_gaps_summary
        summary = build_gaps_summary(self._make_gaps_df(), top_n=2)
        parsed = json.loads(summary)
        assert "AgentA" in parsed

    def test_build_gaps_summary_strength_and_gap(self):
        import json
        from llm_tools import build_gaps_summary
        summary = json.loads(build_gaps_summary(self._make_gaps_df(), top_n=2))
        assert "bench1" in summary["AgentA"]["strengths"]
        assert "bench2" in summary["AgentA"]["gaps"]


# ── LangGraph pipeline nodes ──────────────────────────────────────────────────

class TestPipelineNodes:
    """
    Test each node in isolation by mocking the modules they call.
    This verifies state wiring without running actual data processing.
    """

    def test_node_collect_adds_benchmarks_loaded(self):
        from agent import node_collect
        with patch("agent._collect.collect_all") as mock_collect:
            mock_collect.return_value = {
                "datasci_bench": None, "dsbench": None, "gaia": None
            }
            state = node_collect({"errors": []})
        assert "benchmarks_loaded" in state
        assert len(state["benchmarks_loaded"]) == 3

    def test_node_collect_handles_error_gracefully(self):
        from agent import node_collect
        with patch("agent._collect.collect_all", side_effect=RuntimeError("disk full")):
            state = node_collect({"errors": []})
        assert len(state["errors"]) == 1
        assert "collect failed" in state["errors"][0]

    def test_node_preprocess_adds_n_agents(self):
        import pandas as pd
        import pyarrow as pa
        from agent import node_preprocess
        mock_matrix = pa.table({
            "agent": ["A", "B", "C"],
            "bench1": [80.0, 60.0, 70.0],
            "bench2": [75.0, 55.0, 65.0],
        })
        with patch("agent._preprocess.run_preprocessing") as mock_prep:
            mock_prep.return_value = {"matrix": mock_matrix, "metadata": pa.table({"benchmark": ["b1"]})}
            state = node_preprocess({"errors": []})
        assert state["n_agents"] == 3
        assert state["n_benchmarks"] == 2

    def test_node_analyze_adds_clustering(self):
        from agent import node_analyze
        mock_clustering = {"best_k": 3, "km_labels": [0,1,2], "sil_scores": {2: 0.4, 3: 0.6}}
        with patch("agent._analyze.run_analysis") as mock_analyze:
            mock_analyze.return_value = {"clustering": mock_clustering, "gaps": None, "top_agents": None, "correlation": None}
            state = node_analyze({"errors": []})
        assert state["clustering"]["best_k"] == 3

    def test_node_llm_interpret_adds_text_fields(self):
        import pandas as pd
        from agent import node_llm_interpret
        mock_df = pd.DataFrame({
            "agent": ["A", "B"], "bench1": [80.0, 60.0], "bench2": [70.0, 55.0]
        })
        mock_cluster_df = pd.DataFrame({
            "agent": ["A", "B"], "kmeans_cluster": [0, 1], "hier_cluster": [1, 2]
        })
        mock_gaps_df = pd.DataFrame({
            "agent": ["A"], "benchmark": ["bench1"],
            "score_norm": [80.0], "z_score": [1.5], "flag": ["strength"]
        })
        mock_corr_df = pd.DataFrame({
            "benchmark": ["bench1", "bench2"],
            "bench1": [1.0, 0.8], "bench2": [0.8, 1.0]
        })
        with patch("agent.query_df", return_value=mock_df), \
             patch("agent.read_as_pandas", side_effect=[mock_cluster_df, mock_gaps_df, mock_corr_df]):
            state = node_llm_interpret({"errors": [], "clustering": {"best_k": 2, "sil_scores": {2: 0.5}}})

        assert "cluster_interpretation" in state
        assert "gap_analysis" in state
        assert "executive_summary" in state

    def test_node_report_writes_file(self, tmp_path):
        """node_report should inject LLM text into the template and save."""
        from agent import node_report
        import agent as agent_module

        # Temporarily point REPORT_DIR to tmp_path
        original = agent_module.REPORT_DIR
        agent_module.REPORT_DIR = tmp_path
        template = tmp_path / "report.md"
        template.write_text("# Report\n> _To be written after analysis is complete._\n")

        state = node_report({
            "errors": [],
            "n_agents": 10,
            "n_benchmarks": 5,
            "executive_summary": "This is a test summary.",
            "cluster_interpretation": "",
            "gap_analysis": "",
        })
        agent_module.REPORT_DIR = original

        assert "report_path" in state
        output = Path(state["report_path"]).read_text()
        assert "This is a test summary." in output

    def test_pipeline_state_flows_end_to_end(self):
        """Smoke test: build the pipeline graph without errors."""
        from agent import build_pipeline
        pipeline = build_pipeline()
        assert pipeline is not None


# ── Pipeline graph structure ──────────────────────────────────────────────────

class TestPipelineStructure:
    def test_all_nodes_present(self):
        from agent import build_pipeline
        pipeline = build_pipeline()
        graph = pipeline.get_graph()
        node_names = {n.name for n in graph.nodes.values()}
        expected = {"collect", "preprocess", "analyze", "llm_interpret", "visualize", "report"}
        assert expected.issubset(node_names)
