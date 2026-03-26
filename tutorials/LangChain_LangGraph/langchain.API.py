# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.19.1
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %% [markdown]
# # Description
#
# ## Learn LangChain in 60 Minutes — API notebook

# %% [markdown]
# A mental model before we start:
#
# - **LangChain** is the toolkit: prompts, models, tools, and composable building blocks ("runnables").
# - **LangGraph** is the orchestrator: stateful graphs, routing, checkpointing/memory, and interrupts for human‑in‑the‑loop (HITL).
# - **Deep Agents** is an optional, higher-level layer used later in this tutorial for “agent app” patterns
#   (filesystem tools, todos, subagents, sandboxing, and HITL gates).

# %% [markdown]
# # Imports

# %%
# %load_ext autoreload
# %autoreload 2

import os
import sys

import langchain
import langchain_core
import langgraph

import langchain_API_utils as ut


# %%
import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s - %(message)s"
)
_LOG = logging.getLogger("learn_langchain.api")

ut.print_environment_info()
print(f"LLM_PROVIDER={os.getenv('LLM_PROVIDER', '(unset)')}")


# %% [markdown]
# ## Model
#
# These notebooks are provider-agnostic: you pick a provider in `.env`, and the helper function builds the right chat model.
#
# Supported now:
# - `openai`
# - `anthropic`

# %%
import os

from dotenv import load_dotenv
load_dotenv("langchain.env")

if os.getenv("LANGSMITH_TRACING", "").strip().lower() in {"1", "true", "yes"}:
    _LOG.info("LangSmith tracing requested (LANGSMITH_TRACING=true).")


# %%
# !cat langchain.env

# %%
llm = ut.get_chat_model()
llm


# %% [markdown]
# ## Local dataset (`data/T1_slice.csv`)
#
# We’ll use a local CSV so the examples feel concrete.

# %%
from pathlib import Path
import shutil

import pandas as pd

# TODO(ai_gp): Move this to a function in *_utils.py
DATASET_PATH = Path("data/T1_slice.csv").resolve()
df = pd.read_csv(DATASET_PATH)
TIME_COL = "Date/Time"
if TIME_COL in df.columns:
    df[TIME_COL] = pd.to_datetime(
        df[TIME_COL], format="%d %m %Y %H:%M", errors="coerce"
    )

# Make the dataset visible to Deep Agents filesystem tools under `/workspace/...`.
WORKSPACE_DIR = Path("workspace").resolve()
WORKSPACE_DATA_DIR = WORKSPACE_DIR / "data"
WORKSPACE_DATA_DIR.mkdir(parents=True, exist_ok=True)
WORKSPACE_DATASET_PATH = WORKSPACE_DATA_DIR / "T1_slice.csv"
if not WORKSPACE_DATASET_PATH.exists():
    shutil.copyfile(str(DATASET_PATH), str(WORKSPACE_DATASET_PATH))



# %%
df.head(5)

# %%
# TODO(ai_gp): Add explanation.
DATASET_META = ut.build_dataset_meta(df)
DATASET_META


# %% [markdown]
# ## LCEL (LangChain Expression Language)
#
# LCEL is a _pipe_ syntax for composing steps, like a Unix pipe (`a | b | c`):
# - build a prompt
# - call a model
# - parse the result

# %%
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a concise tutor. Answer clearly."),
        ("human", "{question}"),
    ]
)
chain = prompt | llm | StrOutputParser()
chain.invoke({"question": "Explain LCEL in one sentence."})


# %% [markdown]
# ## Runnables: invoke / batch / stream / RunnableParallel
#
# A “runnable” is anything you can _call_.
# LangChain standardizes that with a few common methods:
#
# - `.invoke(input)` → one input, one output
# - `.batch([inputs])` → many inputs at once (often more efficient)
# - `.stream(input)` → yield partial outputs as they arrive
# - `RunnableParallel(...)` → run independent chains side-by-side and combine the results
#
# When you’re learning, it helps to treat runnables like functions — except they can be composed and configured.
#

# %%
from langchain_core.runnables import RunnableParallel

summary_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You write crisp summaries."),
        ("human", "Summarize in 3 bullets:\n\n{text}"),
    ]
)
risks_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You list caveats."),
        ("human", "List 3 risks/caveats:\n\n{text}"),
    ]
)

summary_chain = summary_prompt | llm | StrOutputParser()
risks_chain = risks_prompt | llm | StrOutputParser()

parallel = RunnableParallel(summary=summary_chain, risks=risks_chain)
parallel.invoke(
    {"text": "LangChain provides composable building blocks for LLM apps."},
    config={"max_concurrency": 2},
)


# %%
questions = [
    {"question": "What is a tool in LangChain?"},
    {"question": "What is ToolNode in LangGraph?"},
    {"question": "What does InjectedState do?"},
]
chain.batch(questions, return_exceptions=True, config={"max_concurrency": 3})


# %%
chunks = []
for chunk in chain.stream(
    {"question": "Give me a 2-bullet explanation of RunnableParallel."}
):
    chunks.append(chunk)
final = "".join(chunks)
final[:300] + ("..." if len(final) > 300 else "")


# %% [markdown]
# ## Tools: `@tool` + ToolNode execution
#
# A *tool* is a normal Python function with a schema.
# The LLM can “ask” to call a tool (with arguments), and your code executes it.
#
# Two ways you’ll see tools used:
#
# 1) **Directly** (call the function yourself)
# 2) **Inside a graph** via `ToolNode` (LangGraph executes any requested tool calls and feeds results back)
#
# If you’re new: don’t worry about the message formats yet. Focus on the story:
# "model asks for tool" → "we run tool" → "tool returns data" → "model continues".
#

# %%
from langchain_core.messages import AIMessage
from langgraph.graph import START, END, StateGraph
from langgraph.prebuilt import ToolNode

tool_node = ToolNode([ut.mean, ut.zscore])

g = StateGraph(ut.ToolState)
g.add_node("tools", tool_node)
g.add_edge(START, "tools")
g.add_edge("tools", END)
graph = g.compile()

tool_calls = [
    {
        "name": "mean",
        "args": {"xs": [1, 2, 3, 4]},
        "id": "t1",
        "type": "tool_call",
    },
    {
        "name": "zscore",
        "args": {"xs": [9, 10, 10], "x": 10},
        "id": "t2",
        "type": "tool_call",
    },  # error (std=0)
]

out = graph.invoke({"messages": [AIMessage(content="", tool_calls=tool_calls)]})
[
    type(m).__name__ + ":" + (getattr(m, "content", "")[:80])
    for m in out["messages"]
]


# %% [markdown]
# ## InjectedState: runtime-only args (system-owned)
#
# Sometimes a tool needs access to *system-owned* context that the model shouldn’t be allowed to spoof.
#
# `InjectedState` is the pattern for that:
# - your tool signature includes an injected parameter
# - LangGraph supplies it at runtime (not from the model’s JSON arguments)
#
# Think of it like dependency injection:
# - model controls: normal tool inputs
# - system controls: injected inputs (state, stores, call IDs)
#

# %%
import json

from langchain_core.messages import AIMessage
from langgraph.graph import START, END, StateGraph
from langgraph.prebuilt import ToolNode

tool_node = ToolNode([ut.dataset_brief])
g = StateGraph(ut.InjectedStateState)
g.add_node("tools", tool_node)
g.add_edge(START, "tools")
g.add_edge("tools", END)
graph = g.compile()

state_in: ut.InjectedStateState = {
    "dataset_meta": DATASET_META,
    "messages": [
        AIMessage(
            content="",
            tool_calls=[
                {
                    "name": "dataset_brief",
                    "args": {
                        "question": "What columns exist and what is the sampling frequency?"
                    },
                    "id": "t1",
                    "type": "tool_call",
                }
            ],
        )
    ],
}
out = graph.invoke(state_in)
json.loads(out["messages"][-1].content)


# %% [markdown]
# ## InjectedStore: injected persistent store handle
#
# A store is a place to keep small bits of information across calls (like preferences, cached results, or “facts we’ve already extracted”).
#
# `InjectedStore` lets a tool receive a store handle **without** the model being able to fabricate it.
#
# In this tutorial we use `InMemoryStore` for simplicity, but the pattern generalizes to other persistence layers.
#

# %%
from langchain_core.messages import AIMessage
from langgraph.graph import START, END, StateGraph
from langgraph.prebuilt import ToolNode
from langgraph.store.memory import InMemoryStore

store = InMemoryStore()
tool_node = ToolNode([ut.save_pref, ut.load_pref])
g = StateGraph(ut.StoreState)
g.add_node("tools", tool_node)
g.add_edge(START, "tools")
g.add_edge("tools", END)
graph = g.compile(store=store)

out1 = graph.invoke(
    {
        "messages": [
            AIMessage(
                content="",
                tool_calls=[
                    {
                        "name": "save_pref",
                        "args": {
                            "user_id": "u1",
                            "key": "freq_hint",
                            "value": "1min",
                        },
                        "id": "t1",
                        "type": "tool_call",
                    }
                ],
            )
        ]
    }
)
out2 = graph.invoke(
    {
        "messages": [
            AIMessage(
                content="",
                tool_calls=[
                    {
                        "name": "load_pref",
                        "args": {"user_id": "u1", "key": "freq_hint"},
                        "id": "t2",
                        "type": "tool_call",
                    }
                ],
            )
        ]
    }
)
out1["messages"][-1].content, out2["messages"][-1].content


# %% [markdown]
# ## Agent APIs used in `langchain.example.ipynb`
#
# An *agent* is a loop: the model looks at the conversation + available tools, chooses an action, and repeats until it’s done.
#
# In this tutorial we use a helper, `create_agent(...)`, to build a tool-calling agent quickly.
# Later, in the examples notebook, you’ll see the same ideas expressed as explicit LangGraph loops.
#
# If you ever feel confused, this heuristic helps:
# - **LangChain agent helpers** get you started fast.
# - **LangGraph** is what you reach for when you want full control (state, routing, memory, HITL).
#

# %%
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage

agent = create_agent(
    model=llm,
    tools=[ut.utc_now],
    system_prompt="Use tools when a tool can answer the question more reliably than guessing.",
)
out = agent.invoke(
    {
        "messages": [
            HumanMessage(content="Call utc_now and return the exact value.")
        ]
    }
)
[(type(m).__name__, getattr(m, "content", "")[:120]) for m in out["messages"]][
    -4:
]


# %% [markdown]
# ## Tool-calling output contract (reproducible handoff)
#
# A practical pattern from production-style graph tutorials: ask agents to return a **reproducible call snippet** after using tools.
#
# Why this helps:
# - humans can verify what happened
# - downstream automation can replay behavior
# - handoffs between teammates become less ambiguous
#

# %%
contract_agent = create_agent(
    model=llm,
    tools=[ut.utc_now],
    system_prompt=(
        "When time is requested, call utc_now. "
        "In your final answer, include a fenced python block with the exact tool call used."
    ),
)
contract_out = contract_agent.invoke(
    {
        "messages": [
            HumanMessage(content="What is the current UTC time? Use your tool.")
        ]
    }
)
print(getattr(contract_out["messages"][-1], "content", ""))


# %% [markdown]
# ## Advanced agent tool plumbing: `AgentState`, `ToolRuntime`, `InjectedToolCallId`
#
# This section is here for when you’re ready to peek “under the hood”.
#
# The high-level story:
# - tool calls happen inside a conversation
# - each tool call has an ID
# - LangGraph/LangChain pass runtime helpers so tools can update state and emit the right `ToolMessage`
#
# If it feels advanced on a first read, that’s normal — the goal is to make the concepts *available*, not to memorize them.
#

# %%
import json

from langchain.agents import create_agent

CustomState, extract_facts = ut.make_custom_state_and_tool()

supervisor = create_agent(
    llm,
    tools=[extract_facts],
    system_prompt="First call extract_facts, then summarize the returned facts.",
    state_schema=CustomState,
)

state = supervisor.invoke(
    {
        "messages": [
            {"role": "user", "content": "Text: LangGraph supports interrupts."}
        ],
        "user_prefs": {"tone": "formal"},
        "facts": [],
    }
)
{
    "facts": state.get("facts"),
    "last": getattr(state["messages"][-1], "content", "")[:160],
}


# %% [markdown]
# ## Human-in-the-loop building block: `interrupt(...)` + resume
#
# Sometimes an agent should *pause* and ask a human before doing something risky:
# - deleting a file
# - sending an email
# - running a trade
# - making an irreversible change
#
# LangGraph’s low-level building block for this is `interrupt(value)`:
#
# - The first time a node calls `interrupt(...)`, execution **stops** and the graph returns an `__interrupt__` payload.
# - To continue, you call the graph again with `Command(resume=...)`.
# - When the graph resumes, the node is **re-executed**, and `interrupt(...)` returns the human’s choice.
#
# In the next cell we create a tiny file in `tmp_runs/hitl/` and only delete it if the human approves.
#

# %%
from pathlib import Path

from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.types import Command

builder = StateGraph(ut.HITLState)
builder.add_node("propose", ut.propose_delete)
builder.add_node("delete", ut.do_delete)
builder.add_edge(START, "propose")
builder.add_edge("propose", "delete")
builder.add_edge("delete", END)
graph = builder.compile(checkpointer=MemorySaver())

tmp_dir = Path("tmp_runs/hitl").resolve()
tmp_dir.mkdir(parents=True, exist_ok=True)
victim = tmp_dir / "victim.txt"
victim.write_text("delete me", encoding="utf-8")

thread_id = "HITL_API_DEMO"
out1 = graph.invoke(
    {"target_path": str(victim), "decision": ""},
    config={"configurable": {"thread_id": thread_id}},
)
pending = (
    out1.get("__interrupt__", [])[0].value if "__interrupt__" in out1 else None
)
out2 = graph.invoke(
    Command(resume="approve"), config={"configurable": {"thread_id": thread_id}}
)
{"pending": pending, "victim_exists_after": victim.exists()}
