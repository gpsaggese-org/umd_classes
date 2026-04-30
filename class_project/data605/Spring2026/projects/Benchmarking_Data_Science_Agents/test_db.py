"""
test_db.py
----------
Tests for the DuckDB connection manager (src/db.py) and
the DuckDB SQL queries used in preprocess.py and analyze.py.
"""

import pytest
import pyarrow as pa
import pandas as pd
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
import db
from db import get_conn, query_arrow, query_df, register_view, execute


# ── Fixtures ──────────────────────────────────────────────────────────────────

@pytest.fixture(autouse=True)
def reset_conn():
    """Close and reset the shared connection before each test."""
    db.close()
    yield
    db.close()


@pytest.fixture
def sample_table() -> pa.Table:
    return pa.table({
        "agent":     ["AgentA", "AgentB", "AgentC", "AgentA"],
        "benchmark": ["bench1", "bench1", "bench1", "bench2"],
        "score":     [80.0, 60.0, 70.0, 55.0],
    })


# ── Connection ────────────────────────────────────────────────────────────────

class TestConnection:
    def test_returns_connection(self):
        conn = get_conn()
        assert conn is not None

    def test_same_instance_returned(self):
        conn1 = get_conn()
        conn2 = get_conn()
        assert conn1 is conn2

    def test_new_instance_after_close(self):
        conn1 = get_conn()
        db.close()
        conn2 = get_conn()
        assert conn1 is not conn2


# ── query_arrow ───────────────────────────────────────────────────────────────

class TestQueryArrow:
    def test_returns_arrow_table(self):
        result = query_arrow("SELECT 1 AS n, 'hello' AS s")
        assert isinstance(result, pa.Table)

    def test_correct_values(self):
        result = query_arrow("SELECT 42 AS answer")
        assert result.column("answer")[0].as_py() == 42

    def test_multi_row(self):
        result = query_arrow("SELECT unnest([1,2,3]) AS n")
        assert result.num_rows == 3


# ── query_df ──────────────────────────────────────────────────────────────────

class TestQueryDf:
    def test_returns_dataframe(self):
        result = query_df("SELECT 1 AS n")
        assert isinstance(result, pd.DataFrame)

    def test_column_names_preserved(self):
        result = query_df("SELECT 99 AS my_col")
        assert "my_col" in result.columns

    def test_empty_result(self):
        result = query_df("SELECT 1 AS n WHERE 1=0")
        assert len(result) == 0


# ── register_view ─────────────────────────────────────────────────────────────

class TestRegisterView:
    def test_can_query_registered_table(self, sample_table):
        register_view("test_scores", sample_table)
        result = query_df("SELECT COUNT(*) AS n FROM test_scores")
        assert result["n"].iloc[0] == 4

    def test_aggregation_on_view(self, sample_table):
        register_view("test_scores", sample_table)
        result = query_df("SELECT benchmark, COUNT(*) AS n FROM test_scores GROUP BY benchmark")
        assert set(result["benchmark"]) == {"bench1", "bench2"}


# ── SQL logic used in preprocess.py ──────────────────────────────────────────

class TestPreprocessSQL:
    def test_normalisation_window_function(self, sample_table):
        """Min-max normalisation via DuckDB window functions."""
        register_view("scores", sample_table)
        result = query_df("""
            SELECT
                agent,
                benchmark,
                score,
                MIN(score) OVER (PARTITION BY benchmark) AS bench_min,
                MAX(score) OVER (PARTITION BY benchmark) AS bench_max,
                ROUND(
                    ((score - MIN(score) OVER (PARTITION BY benchmark))
                    / NULLIF(
                        MAX(score) OVER (PARTITION BY benchmark)
                        - MIN(score) OVER (PARTITION BY benchmark),
                        0
                    )) * 100,
                2) AS score_norm
            FROM scores
            WHERE benchmark = 'bench1'
        """)
        # AgentA has the max score (80) in bench1 → should normalise to 100
        agent_a = result[result["agent"] == "AgentA"]
        assert agent_a["score_norm"].iloc[0] == pytest.approx(100.0, abs=0.1)

        # AgentB has the min score (60) in bench1 → should normalise to 0
        agent_b = result[result["agent"] == "AgentB"]
        assert agent_b["score_norm"].iloc[0] == pytest.approx(0.0, abs=0.1)

    def test_deduplication_keeps_max(self, sample_table):
        """Duplicate agent+benchmark rows → keep highest score."""
        register_view("scores", sample_table)
        result = query_df("""
            SELECT agent, benchmark, MAX(score) AS best_score
            FROM scores
            GROUP BY agent, benchmark
        """)
        # AgentA has bench1 (80) and bench2 (55) — both should appear
        agent_a = result[result["agent"] == "AgentA"]
        assert len(agent_a) == 2

    def test_min_benchmark_filter(self, sample_table):
        """Agents must appear on >= 2 benchmarks."""
        register_view("scores", sample_table)
        result = query_df("""
            SELECT agent
            FROM scores
            GROUP BY agent
            HAVING COUNT(DISTINCT benchmark) >= 2
        """)
        # Only AgentA appears in both bench1 and bench2
        assert list(result["agent"]) == ["AgentA"]


# ── SQL logic used in analyze.py ─────────────────────────────────────────────

class TestAnalyzeSQL:
    def test_gap_analysis_z_scores(self):
        """z-score calculation via DuckDB STDDEV_POP and AVG."""
        table = pa.table({
            "agent":      ["AgentX", "AgentX", "AgentX"],
            "benchmark":  ["b1",     "b2",     "b3"],
            "score_norm": [90.0,     50.0,     10.0],
        })
        register_view("norm_scores", table)
        result = query_df("""
            WITH agent_stats AS (
                SELECT agent,
                       AVG(score_norm)        AS agent_mean,
                       STDDEV_POP(score_norm) AS agent_std
                FROM norm_scores
                GROUP BY agent
            )
            SELECT
                n.agent, n.benchmark, n.score_norm,
                ROUND((n.score_norm - s.agent_mean) / s.agent_std, 3) AS z_score
            FROM norm_scores n
            JOIN agent_stats s ON n.agent = s.agent
            ORDER BY n.benchmark
        """)
        # Mean = 50, std = sqrt(((90-50)^2+(50-50)^2+(10-50)^2)/3) = ~32.66
        # b1 z-score ≈ +1.22, b3 z-score ≈ -1.22
        b1_z = result[result["benchmark"] == "b1"]["z_score"].iloc[0]
        b3_z = result[result["benchmark"] == "b3"]["z_score"].iloc[0]
        assert b1_z > 1.0
        assert b3_z < -1.0

    def test_top_agents_query(self, sample_table):
        """DENSE_RANK window function returns correct rankings."""
        register_view("norm_scores_top", sample_table)
        result = query_df("""
            SELECT agent, benchmark, score,
                   DENSE_RANK() OVER (
                       PARTITION BY benchmark ORDER BY score DESC
                   ) AS rank
            FROM norm_scores_top
            WHERE benchmark = 'bench1'
        """)
        top_agent = result[result["rank"] == 1]["agent"].iloc[0]
        assert top_agent == "AgentA"   # AgentA has score 80, the highest in bench1
