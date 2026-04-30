"""
db.py
-----
DuckDB connection manager.
"""

import duckdb
import pyarrow as pa
import pandas as pd
from pathlib import Path
from typing import Any

_CONN: duckdb.DuckDBPyConnection | None = None


def get_conn() -> duckdb.DuckDBPyConnection:
    global _CONN
    if _CONN is None:
        _CONN = duckdb.connect(database=":memory:", read_only=False)
        _CONN.execute("INSTALL parquet; LOAD parquet;")
        _CONN.execute("PRAGMA threads=4;")
        _CONN.execute("PRAGMA memory_limit='1GB';")
    return _CONN


def query_arrow(sql: str, params: list[Any] | None = None) -> pa.Table:
    return get_conn().execute(sql, params or []).arrow()


def query_df(sql: str, params: list[Any] | None = None) -> pd.DataFrame:
    return get_conn().execute(sql, params or []).df()


def register_view(name: str, table: pa.Table) -> None:
    get_conn().register(name, table)


def execute(sql: str, params: list[Any] | None = None) -> None:
    get_conn().execute(sql, params or [])


def close() -> None:
    global _CONN
    if _CONN is not None:
        _CONN.close()
        _CONN = None
