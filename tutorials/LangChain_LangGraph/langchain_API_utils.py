"""
Utility library for langchain.API.ipynb.

All reusable functions and classes extracted from the notebook live here,
organised in the same order as the notebook sections they belong to.

Import as:

import tutorials.LangChain_LangGraph.langchain_API_utils as tlllaput
"""

import base64
import json
import logging
import os
import platform
import shutil
import sys
from dataclasses import dataclass
from math import sqrt as _sqrt
from pathlib import Path
from typing import Annotated, Any, Literal, Sequence, TypedDict
from typing_extensions import Annotated as TxAnnotated

import nbformat
import helpers.hdbg as hdbg
import langchain_core.tools
from langchain_core.tools import tool
import langgraph.graph.message
import langgraph.prebuilt
import langgraph.store.base
import nbclient

_LOG = logging.getLogger(__name__)


# ##############################################################################
# Logging utilities
# ##############################################################################


def print_environment_info() -> None:
    """
    Print Python version, platform, and library versions.
    """
    import langchain
    import langchain_core
    import langgraph

    print(f"python={sys.version.split()[0]}")
    print(f"platform={platform.platform()}")
    print(f"langchain={getattr(langchain, '__version__', 'unknown')}")
    print(f"langchain_core={getattr(langchain_core, '__version__', 'unknown')}")
    print(f"langgraph={getattr(langgraph, '__version__', 'unknown')}")


def init_logger(
    name: str,
    *,
    level: int = logging.INFO,
    format_str: str = "%(asctime)s %(levelname)s %(name)s - %(message)s",
) -> logging.Logger:
    """
    Initialize and configure a logger for the tutorial notebooks.

    :param name: the name of the logger (typically __name__)
    :param level: the logging level (default: logging.INFO)
    :param format_str: the format string for log messages
    :return: the configured logger instance
    """
    logging.basicConfig(level=level, format=format_str)
    logger = logging.getLogger(name)
    # Suppress verbose logs from external libraries.
    logging.getLogger("openai").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)
    return logger


# //////////////////////////////////////////////////////////////////////////////
# LLM Configuration
# //////////////////////////////////////////////////////////////////////////////


# #############################################################################
# LlmConfig
# #############################################################################


@dataclass(frozen=True)
class LlmConfig:
    """
    Configuration for selecting an LLM provider + model from environment
    variables.
    """

    provider: str
    model: str
    temperature: float


def load_llm_config() -> LlmConfig:
    """
    Load `LlmConfig` from environment variables.
    """
    hdbg.dassert_in("LLM_PROVIDER", os.environ)
    provider = os.environ["LLM_PROVIDER"].lower()
    temperature = float(os.getenv("LLM_TEMPERATURE", "0"))
    default_models = {
        "openai": "gpt-4.1-mini",
        "anthropic": "claude-3-5-sonnet-latest",
        "ollama": "llama3.1:8b",
    }
    model = os.getenv("LLM_MODEL", default_models.get(provider, ""))
    if not model:
        raise RuntimeError(
            f"Missing `LLM_MODEL` for provider={provider!r}. See `.env.example`."
        )
    return LlmConfig(provider=provider, model=model, temperature=temperature)


def get_chat_model():
    """
    Create a tool-calling-capable chat model using env configuration.
    """
    cfg = load_llm_config()
    if cfg.provider == "openai":
        from langchain_openai import ChatOpenAI

        hdbg.dassert_in("OPENAI_API_KEY", os.environ)
        return ChatOpenAI(
            model=cfg.model,
            temperature=cfg.temperature,
            timeout=60,
            max_retries=2,
        )
    elif cfg.provider == "anthropic":
        from langchain_anthropic import ChatAnthropic

        hdbg.dassert_in("ANTHROPIC_API_KEY", os.environ)
        return ChatAnthropic(
            model=cfg.model,
            temperature=cfg.temperature,
            timeout=60,
            max_retries=2,
        )
    else:
        raise ValueError(f"Unsupported `LLM_PROVIDER={cfg.provider}`")


# ##############################################################################
# Dataset utilities
# ##############################################################################


def load_and_prepare_dataset(
    dataset_path: str = "data/T1_slice.csv",
    *,
    workspace_dir: str = "workspace",
) -> dict:
    """
    Load a CSV dataset, parse datetime columns, and prepare workspace copy.

    :param dataset_path: path to the CSV file to load
    :param workspace_dir: base directory for workspace data
    :return: dict with keys: df, dataset_path, workspace_dataset_path
    """
    import pandas as pd

    # Load dataset and parse the date/time column.
    dataset_path_obj = Path(dataset_path).resolve()
    df = pd.read_csv(dataset_path_obj)
    time_col = "Date/Time"
    if time_col in df.columns:
        df[time_col] = pd.to_datetime(
            df[time_col], format="%d %m %Y %H:%M", errors="coerce"
        )
    # Make the dataset visible to Deep Agents filesystem tools under `/workspace/...`.
    workspace_dir_obj = Path(workspace_dir).resolve()
    workspace_data_dir = workspace_dir_obj / "data"
    workspace_data_dir.mkdir(parents=True, exist_ok=True)
    workspace_dataset_path = workspace_data_dir / dataset_path_obj.name
    if not workspace_dataset_path.exists():
        shutil.copyfile(str(dataset_path_obj), str(workspace_dataset_path))
    return {
        "df": df,
        "dataset_path": dataset_path_obj,
        "workspace_dir": workspace_dir_obj,
        "workspace_data_dir": workspace_data_dir,
        "workspace_dataset_path": workspace_dataset_path,
    }


def build_dataset_meta(df) -> dict:
    """
    Build a compact JSON-serializable dataset metadata dict for demos.
    """
    cols = list(df.columns)
    dtypes = {c: str(df[c].dtype) for c in cols}
    sample_rows = df.head(3).to_dict(orient="records")
    freq = None
    if "Date/Time" in df.columns:
        ts = df["Date/Time"].dropna().sort_values()
        if len(ts) >= 3:
            # Estimate the most common sampling delta.
            deltas = ts.diff().dropna()
            freq = str(deltas.value_counts().idxmax())
    return {
        "path": "data/T1_slice.csv",
        "workspace_path": "workspace/data/T1_slice.csv",
        "tool_path": "/workspace/data/T1_slice.csv",
        "n_rows": int(df.shape[0]),
        "n_cols": int(df.shape[1]),
        "columns": cols,
        "dtypes": dtypes,
        "sample_rows": sample_rows,
        "time_col": "Date/Time" if "Date/Time" in df.columns else None,
        "freq": freq,
    }


# //////////////////////////////////////////////////////////////////////////////
# Graph states
# //////////////////////////////////////////////////////////////////////////////


# #############################################################################
# ToolState
# #############################################################################


class ToolState(TypedDict):
    messages: Annotated[list, langgraph.graph.message.add_messages]


# #############################################################################
# InjectedStateState
# #############################################################################


class InjectedStateState(TypedDict):
    messages: Annotated[list, langgraph.graph.message.add_messages]
    dataset_meta: dict


# #############################################################################
# StoreState
# #############################################################################


class StoreState(TypedDict):
    messages: Annotated[list, langgraph.graph.message.add_messages]


# #############################################################################
# ToolGraphState
# #############################################################################


class ToolGraphState(TypedDict):
    messages: Annotated[list, langgraph.graph.message.add_messages]
    workspace_dir: str


# //////////////////////////////////////////////////////////////////////////////
# Tools: math (mean, zscore)
# //////////////////////////////////////////////////////////////////////////////


def _as_floats(xs: Sequence[float]) -> list[float]:
    """
    Validate `xs` and return it as a non-empty `list[float]`.
    """
    if xs is None:
        raise ValueError("xs must not be None")
    xs_list = [float(x) for x in xs]
    if len(xs_list) == 0:
        raise ValueError("xs must be non-empty")
    return xs_list


@langchain_core.tools.tool
def mean(xs: Sequence[float]) -> float:
    """
    Compute the arithmetic mean of a non-empty list of numbers.
    """
    xs_list = _as_floats(xs)
    return sum(xs_list) / len(xs_list)


@tool
def zscore(xs: Sequence[float], x: float) -> float:
    """
    Compute z = (x - mean(xs)) / std(xs).
    """
    xs_list = _as_floats(xs)
    mu = sum(xs_list) / len(xs_list)
    var = sum((v - mu) ** 2 for v in xs_list) / len(xs_list)
    std = _sqrt(var)
    if std == 0.0:
        raise ValueError("std(xs) is 0; z-score undefined for constant sample")
    return (float(x) - mu) / std


# ##############################################################################
# Tools: InjectedState demo
# ##############################################################################


@langchain_core.tools.tool
def dataset_brief(
    question: str,
    dataset_meta: TxAnnotated[
        dict, langgraph.prebuilt.InjectedState("dataset_meta")
    ],
) -> str:
    """
    Answer a question using injected dataset metadata (InjectedState).
    """
    payload = {
        "question": question,
        "n_rows": dataset_meta.get("n_rows"),
        "n_cols": dataset_meta.get("n_cols"),
        "columns": dataset_meta.get("columns"),
        "dtypes": dataset_meta.get("dtypes"),
        "time_col": dataset_meta.get("time_col"),
        "freq": dataset_meta.get("freq"),
    }
    return json.dumps(payload)


# ##############################################################################
# Tools: InjectedStore demo
# ##############################################################################


@langchain_core.tools.tool
def save_pref(
    user_id: str,
    key: str,
    value: str,
    store: TxAnnotated[
        langgraph.store.base.BaseStore, langgraph.prebuilt.InjectedStore()
    ],
) -> str:
    """
    Save a user preference (key/value) into an injected store.
    """
    namespace = ("prefs", user_id)
    store.put(namespace, key, {"value": value})
    return f"saved {key}={value} for user_id={user_id}"


@langchain_core.tools.tool
def load_pref(
    user_id: str,
    key: str,
    store: TxAnnotated[
        langgraph.store.base.BaseStore, langgraph.prebuilt.InjectedStore()
    ],
) -> str:
    """
    Load a user preference (key) from an injected store.
    """
    namespace = ("prefs", user_id)
    item = store.get(namespace, key)
    if not item:
        return f"(missing) {key}"
    return str(item.value.get("value", f"(missing) {key}"))


# ##############################################################################
# Tools: agent / datetime
# ##############################################################################


@langchain_core.tools.tool
def utc_now() -> str:
    """
    Return the current UTC time as an ISO string.
    """
    from datetime import datetime, timezone

    return datetime.now(timezone.utc).isoformat()


# //////////////////////////////////////////////////////////////////////////////
# Advanced agent state and tools
# //////////////////////////////////////////////////////////////////////////////


def make_custom_state_and_tool():
    """
    Return `(CustomState, extract_facts)` built from tutorial agent imports.

    Wrapped in a function so the module-level import of langchain.agents does
    not fail in environments where the tutorial package is not installed.
    """
    from langchain.agents import AgentState
    from langchain.tools import InjectedToolCallId, ToolRuntime
    from langchain.tools import tool as lc_tool
    from langchain_core.messages import ToolMessage
    from langgraph.types import Command

    class CustomState(AgentState):
        user_prefs: dict
        facts: list[str]

    @lc_tool(
        "extract_facts",
        description="Extract 2 facts, store them in state, and emit a ToolMessage.",
    )
    def extract_facts(
        text: str,
        tool_call_id: TxAnnotated[str, InjectedToolCallId],
        runtime: ToolRuntime[None, CustomState],
    ) -> Command:
        """
        Extract simple facts and update the graph state via `Command(update=...)`.
        """
        tone = runtime.state.get("user_prefs", {}).get("tone", "neutral")
        facts = [f"tone={tone}", f"n_chars={len(text)}"]
        return Command(
            update={
                "facts": facts,
                "messages": [
                    ToolMessage(
                        content=json.dumps({"facts": facts}),
                        tool_call_id=tool_call_id,
                    )
                ],
            }
        )

    return CustomState, extract_facts


# //////////////////////////////////////////////////////////////////////////////
# Human-in-the-loop (HITL)
# //////////////////////////////////////////////////////////////////////////////


# #############################################################################
# HITLState
# #############################################################################


class HITLState(TypedDict):
    target_path: str
    decision: Literal["approve", "reject", ""]


def propose_delete(state: HITLState) -> dict:
    """
    Ask for approval to delete a file.
    """
    from langgraph.types import interrupt

    payload = {
        "action": "delete_file",
        "target_path": state["target_path"],
        "message": "Approve deletion?",
    }
    decision = interrupt(payload)
    return {"decision": decision}


def do_delete(state: HITLState) -> dict:
    """
    Delete the file if approved.
    """
    if state["decision"] != "approve":
        return {}
    p = Path(state["target_path"])
    if p.exists() and p.is_file():
        p.unlink()
    return {}


# //////////////////////////////////////////////////////////////////////////////
# Notebook operations
# //////////////////////////////////////////////////////////////////////////////


def _safe_path(workspace: Path, rel_path: str) -> Path:
    """
    Resolve `rel_path` under `workspace` and reject path traversal.
    """
    p = (workspace / rel_path).resolve()
    if not str(p).startswith(str(workspace)):
        raise ValueError("Path escapes workspace")
    return p


def _safe_injected_path(workspace_dir: str, rel_path: str) -> Path:
    """
    Resolve `rel_path` under `workspace_dir` and reject path traversal.
    """
    root = Path(workspace_dir).resolve()
    p = (root / rel_path).resolve()
    if not str(p).startswith(str(root)):
        raise ValueError("Path escapes injected workspace")
    return p


@langchain_core.tools.tool
def write_notebook(spec: dict[str, Any], out_rel: str) -> str:
    """
    Write a notebook from a small spec into a safe workspace path.
    """
    workspace = Path("notebooks").resolve()
    workspace.mkdir(parents=True, exist_ok=True)
    out_path = _safe_path(workspace, out_rel)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    nb = nbformat.v4.new_notebook()
    cells = []
    for c in spec.get("cells", []):
        t: Literal["markdown", "code"] = c["type"]
        src = c.get("source", "")
        if t == "markdown":
            cells.append(nbformat.v4.new_markdown_cell(src))
        elif t == "code":
            cells.append(nbformat.v4.new_code_cell(src))
        else:
            raise ValueError(f"Unknown cell type: {t}")
    nb.cells = cells
    nbformat.validate(nb)
    nbformat.write(nb, str(out_path))
    return str(out_path)


@langchain_core.tools.tool
def nb_write(
    spec: dict[str, Any],
    out_rel: str,
    workspace_dir: TxAnnotated[
        str, langgraph.prebuilt.InjectedState("workspace_dir")
    ],
) -> str:
    """
    Write a notebook under an injected workspace_dir.
    """
    out_path = _safe_injected_path(workspace_dir, out_rel)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    nb = nbformat.v4.new_notebook()
    cells = []
    for c in spec.get("cells", []):
        if c["type"] == "markdown":
            cells.append(nbformat.v4.new_markdown_cell(c.get("source", "")))
        elif c["type"] == "code":
            cells.append(nbformat.v4.new_code_cell(c.get("source", "")))
        else:
            raise ValueError(f"Unknown cell type: {c['type']}")
    nb.cells = cells
    nb.metadata["kernelspec"] = {
        "name": "python3",
        "display_name": "Python 3",
        "language": "python",
    }
    validate(nb)
    nbformat.write(nb, str(out_path))
    return str(out_path)


@langchain_core.tools.tool
def nb_run(
    in_rel: str,
    out_rel: str,
    timeout_s: int,
    workspace_dir: TxAnnotated[
        str, langgraph.prebuilt.InjectedState("workspace_dir")
    ],
) -> str:
    """
    Execute a notebook with nbclient and save the executed copy under
    workspace_dir.
    """
    in_path = _safe_injected_path(workspace_dir, in_rel)
    out_path = _safe_injected_path(workspace_dir, out_rel)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    nb = nbformat.read(str(in_path), as_version=4)
    client = nbclient.NotebookClient(
        nb,
        timeout=int(timeout_s),
        resources={"metadata": {"path": str(out_path.parent)}},
    )
    client.execute()
    nbformat.write(nb, str(out_path))
    return str(out_path)


@langchain_core.tools.tool
def nb_extract_errors(
    executed_rel: str,
    workspace_dir: TxAnnotated[
        str, langgraph.prebuilt.InjectedState("workspace_dir")
    ],
) -> str:
    """
    Extract per-cell error metadata from an executed notebook (JSON string).
    """
    p = _safe_injected_path(workspace_dir, executed_rel)
    nb = nbformat.read(str(p), as_version=4)
    errs = []
    for i, cell in enumerate(nb.cells):
        if cell.get("cell_type") != "code":
            continue
        for out in cell.get("outputs", []):
            if out.get("output_type") == "error":
                errs.append(
                    {
                        "cell_index": i,
                        "ename": out.get("ename"),
                        "evalue": out.get("evalue"),
                    }
                )
    return json.dumps(errs)


@langchain_core.tools.tool
def nb_extract_artifacts(
    executed_rel: str,
    artifacts_rel_dir: str,
    workspace_dir: TxAnnotated[
        str, langgraph.prebuilt.InjectedState("workspace_dir")
    ],
) -> str:
    """
    Extract stdout + inline PNGs from an executed notebook into
    artifacts_rel_dir (JSON manifest).
    """
    p = _safe_injected_path(workspace_dir, executed_rel)
    out_dir = _safe_injected_path(workspace_dir, artifacts_rel_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    nb = nbformat.read(str(p), as_version=4)
    manifest = []
    for i, cell in enumerate(nb.cells):
        if cell.get("cell_type") != "code":
            continue
        for j, out in enumerate(cell.get("outputs", [])):
            if out.get("output_type") == "stream":
                txt = out.get("text", "")
                fp = out_dir / f"cell_{i}_stream_{j}.txt"
                fp.write_text(txt if isinstance(txt, str) else "".join(txt))
                manifest.append({"cell": i, "kind": "stream", "path": str(fp)})
            if out.get("output_type") in ("display_data", "execute_result"):
                data = out.get("data", {})
                if "image/png" in data:
                    b64 = data["image/png"]
                    b = base64.b64decode(
                        b64 if isinstance(b64, str) else "".join(b64)
                    )
                    fp = out_dir / f"cell_{i}_img_{j}.png"
                    fp.write_bytes(b)
                    manifest.append(
                        {"cell": i, "kind": "image/png", "path": str(fp)}
                    )
    (out_dir / "manifest.json").write_text(json.dumps(manifest, indent=2))
    return json.dumps(
        {"n": len(manifest), "manifest": str(out_dir / "manifest.json")}
    )


@langchain_core.tools.tool
def nb_list_files(
    workspace_dir: TxAnnotated[
        str, langgraph.prebuilt.InjectedState("workspace_dir")
    ],
) -> str:
    """
    List files under workspace_dir (JSON).
    """
    root = Path(workspace_dir).resolve()
    files = []
    for p in root.rglob("*"):
        if p.is_file():
            files.append({"path": str(p), "size": p.stat().st_size})
    return json.dumps(files[:200])


def extract_errors(nb) -> list[dict]:
    """
    Extract cell execution errors from an executed notebook.
    """
    errs = []
    for i, cell in enumerate(nb.cells):
        if cell.get("cell_type") != "code":
            continue
        for out in cell.get("outputs", []):
            if out.get("output_type") == "error":
                errs.append(
                    {
                        "cell_index": i,
                        "ename": out.get("ename"),
                        "evalue": out.get("evalue"),
                    }
                )
    return errs
