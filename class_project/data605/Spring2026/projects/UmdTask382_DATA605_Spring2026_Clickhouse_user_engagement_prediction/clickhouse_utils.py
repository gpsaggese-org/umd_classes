import os
from dataclasses import dataclass
from typing import Any, Optional, Sequence

import pandas as pd
from clickhouse_driver import Client


@dataclass(frozen=True)
class ClickHouseConfig:
    host: str
    port: int
    user: str
    password: str
    database: str


def get_ch_config() -> ClickHouseConfig:
    return ClickHouseConfig(
        host=os.getenv("CLICKHOUSE_HOST", "clickhouse"),
        port=int(os.getenv("CLICKHOUSE_PORT", "9000")),
        user=os.getenv("CLICKHOUSE_USER", "default"),
        password=os.getenv("CLICKHOUSE_PASSWORD", ""),
        database=os.getenv("CLICKHOUSE_DB", "ecomm"),
    )


def get_client(cfg: Optional[ClickHouseConfig] = None) -> Client:
    cfg = cfg or get_ch_config()
    client = Client(host=cfg.host, port=cfg.port, user=cfg.user, password=cfg.password)
    client.execute(f"CREATE DATABASE IF NOT EXISTS {cfg.database}")
    client.execute(f"USE {cfg.database}")
    return client


def ch_df(client: Client, query: str, columns: Optional[Sequence[str]] = None) -> pd.DataFrame:
    if columns is None or len(columns) == 0 or (len(columns) == 1 and columns[0] == "*"):
        rows, col_types = client.execute(query, with_column_types=True)
        inferred_cols = [c for c, _t in col_types]
        return pd.DataFrame(rows, columns=inferred_cols)
    rows = client.execute(query)
    return pd.DataFrame(rows, columns=list(columns))


def print_kv(title: str, value: Any) -> None:
    print(f"{title}: {value}")

