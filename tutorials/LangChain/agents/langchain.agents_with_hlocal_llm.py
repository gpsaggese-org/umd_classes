# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.19.0
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %% [markdown]
# # Agents with `helpers.hlocal_llm` (Ollama/Qwen/Gemma supported)
#
# This notebook implements a **minimal ReAct-style agent executor** that uses your `helpers.hlocal_llm` wrapper for LLM calls.
#
# Key features:
# - Simple **tool registry** (Python functions) with JSON inputs.
# - Deterministic **ReAct loop**: `Action` → `Observation` → … → `Final Answer`.
# - Local-friendly defaults (e.g., `model='ollama/qwen2.5:7b-instruct'`).
#

# %% [markdown]
# ## 0) Helpers hlocal_llm
#
#
# ```python
# import helpers.hlocal_llm as hlocal_llm
# ```

# %% [markdown]
# ## 1) Environment & model selection
#
# You can target different providers by **encoding the provider** in the `model` string (as supported by `hllm.py`):
#
# - `openai/gpt-4o-mini`
# - `openrouter/<provider>/<model>`
# - `ollama/qwen2.5:7b-instruct`  *(local)*
# - `lmstudio/gemma2:9b-instruct` *(local)*
# - `openai_compat/<your-model>` *(generic OpenAI-compatible server; set `OPENAI_COMPAT_BASE_URL`)*
#
# Set provider-specific env vars if needed:
# - OpenAI: `OPENAI_API_KEY`
# - OpenRouter: `OPENROUTER_API_KEY`
# - Ollama: `OLLAMA_BASE_URL` (default `http://localhost:11434/v1`), `OLLAMA_API_KEY` (not required)
# - LM Studio: `LMSTUDIO_BASE_URL` (default `http://localhost:1234/v1`)

# %%
import json
import re
from typing import Any, Dict, Optional
from datetime import datetime

import helpers.hlocal_llm as hlocal_llm


# %% [markdown]
# ## 2) Tool registry
#
# Define **small, deterministic** tools with JSON-serializable inputs/outputs. Keep docstrings precise, `hlocal_llm` will pass your prompts to the model, which reads these descriptions to choose and format calls.


# %%
def tool_calc(expression: str) -> str:
    """Evaluate a simple Python arithmetic expression like '37*42'. Returns the result as string. Strictly deterministic."""
    try:
        return str(eval(expression, {"__builtins__": {}}))
    except Exception as e:
        return f"error: {e}"


def tool_now() -> str:
    """Return current local datetime ISO string (YYYY-MM-DDTHH:MM:SS)."""
    return datetime.now().isoformat(timespec="seconds")


def tool_read_file(path: str, max_chars: int = 4000) -> str:
    """Read a small UTF-8 text file from disk. Return up to max_chars characters."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            txt = f.read()
        return txt[:max_chars]
    except Exception as e:
        return f"error: {e}"


TOOLS: Dict[str, Dict[str, Any]] = {
    "calc": {
        "fn": tool_calc,
        "schema": {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "Python arithmetic expression like '37*42'",
                }
            },
            "required": ["expression"],
            "additionalProperties": False,
        },
        "desc": "Compute an arithmetic expression and return the numeric result as text.",
    },
    "now": {
        "fn": tool_now,
        "schema": {
            "type": "object",
            "properties": {},
            "required": [],
            "additionalProperties": False,
        },
        "desc": "Return current local datetime ISO string.",
    },
    "read_file": {
        "fn": tool_read_file,
        "schema": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Relative or absolute file path.",
                },
                "max_chars": {
                    "type": "integer",
                    "description": "Max characters to return (default 4000).",
                },
            },
            "required": ["path"],
            "additionalProperties": False,
        },
        "desc": "Read a small UTF-8 text file (safe paths only).",
    },
}
print("Registered tools:", list(TOOLS.keys()))

# %% [markdown]
# ## 3) Agent policy and loop
#
# We prompt the model to follow a strict format for **tool calls** and the **final answer**.
#
# **When using a tool**, the model must output exactly:
# ```
# Action: <tool_name>
# Input: {"arg": "value", ...}
# ```
# Then we execute the tool and append an `Observation: ...` back into the transcript.
#
# **When done**, the model must output exactly:
# ```
# Final Answer: <text>
# ```
#
# We implement a small executor around `hlocal_llm.get_completion()`.

# %%
import traceback
from typing import Tuple

MODEL = "ollama/qwen3:latest"

# ---- Local model selection (Ollama) -----------------------------------------


def _tools_manifest() -> str:
    lines = []
    for name, meta in TOOLS.items():
        lines.append(f"- {name}: {meta['desc']}")
        lines.append(
            "  JSON schema: " + json.dumps(meta["schema"], ensure_ascii=False)
        )
    return "\n".join(lines)


SYSTEM_PROMPT = (
    "You are a precise ReAct agent. You may call tools to solve the task.\n"
    "When you need a tool, output EXACTLY:\n"
    "Action: <tool_name>\nInput: <JSON object strictly matching the tool schema>\n"
    "Do not add extra text around the Action/Input block.\n"
    "After the tool is executed, you will receive an Observation. Continue reasoning if needed.\n"
    "When you are ready to answer, output EXACTLY:\n"
    "Final Answer: <your concise answer>\n"
)


def _compose_user_prompt(question: str, transcript: str = "") -> str:
    tools = _tools_manifest()
    header = (
        "Available tools (name, description, schema):\n" + tools + "\n\n"
        "Follow the required output formats strictly.\n"
        "Begin.\n"
        f"Question: {question}\n"
    )
    return header + ("\n" + transcript if transcript else "")


def _parse_action_or_final(
    text: str,
) -> Tuple[Optional[str], Optional[dict], Optional[str]]:
    """Return (tool_name, json_args, final_answer) depending on the content."""
    m_final = re.search(r"Final Answer:\s*(.*)", text, flags=re.DOTALL)
    if m_final:
        return (None, None, m_final.group(1).strip())
    m_action = re.search(
        r"Action:\s*(\w+)\s*\nInput:\s*(\{.*?\})", text, flags=re.DOTALL
    )
    if m_action:
        tool_name = m_action.group(1).strip()
        raw = m_action.group(2).strip()
        try:
            args = json.loads(raw)
        except Exception:
            try:
                if raw.startswith('"') and raw.endswith('"'):
                    args = {"text": json.loads(raw)}
                else:
                    args = {"text": raw}
            except Exception:
                args = {"malformed": raw}
        return (tool_name, args, None)
    return (None, None, None)


def run_agent(
    question: str,
    model: str = MODEL,  # <- default local model
    max_iters: int = 6,
    temperature: float = 0.0,
) -> str:
    transcript = ""
    for _ in range(max_iters):
        user_prompt = _compose_user_prompt(question, transcript)
        try:
            reply = hlocal_llm.get_completion(
                user_prompt,
                system_prompt=SYSTEM_PROMPT,
                model=model,  # <- uses local Ollama model
                cache_mode="DISABLE_CACHE",
                temperature=temperature,
                print_cost=True,
            )
        except Exception as e:
            # Helpful traceback when local server/mode misbehaves
            return f"(engine error) {e}\n{traceback.format_exc(limit=2)}"

        tool_name, args, final_answer = _parse_action_or_final(reply)
        if final_answer is not None:
            return final_answer
        if tool_name is None:
            transcript += "\nAssistant: (invalid format)\n"
            break

        tool = TOOLS.get(tool_name)
        if not tool:
            observation = f"error: unknown tool '{tool_name}'"
        else:
            fn = tool["fn"]
            try:
                observation = fn(**args) if isinstance(args, dict) else fn(args)
            except TypeError:
                observation = f"error: invalid args {args} for tool {tool_name}"
            except Exception as e:
                observation = f"error: {e}"

        transcript += (
            f"\nAction: {tool_name}\n"
            f"Input: {json.dumps(args, ensure_ascii=False)}\n"
            f"Observation: {str(observation)[:4000]}\n"
        )
    return "(No final answer; max iterations reached)"


# %% [markdown]
# ## 4) Quick tests

# %%
print(run_agent("Compute (37*42)+5 using calc.", model="ollama/gemma3:latest"))

# %%
# Create a demo file and ask the agent to use read_file and now.
with open("demo.txt", "w", encoding="utf-8") as f:
    f.write("LangChain-style agents can be built without LangChain, too.\n")
    f.write("This is a simple local test file.\n")
    f.write("The agent will read and summarize it.\n")

q = "Read ./demo.txt, summarize it briefly, then tell me the current time using now tool."
print(run_agent(q, model="ollama/gemma3:latest"))

# %%
# Create a demo file and ask the agent to use read_file and now.
with open("demo.txt", "w", encoding="utf-8") as f:
    f.write("LangChain-style agents can be built without LangChain, too.\n")
    f.write("This is a simple local test file.\n")
    f.write("The agent will read and summarize it.\n")

q = "Read ./demo.txt, summarize it briefly, then tell me the current time using now tool."
print(run_agent(q, model="ollama/qwen3:latest"))

# %%
