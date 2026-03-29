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
# # Description
#
# ## Learn LangChain in 60 Minutes — examples notebook
#
# What you’ll build (incrementally):
# - a tool-calling agent loop
# - LangGraph workflows: state, routing, reducers, and a ReAct loop from scratch
# - subagents + subgraphs (composition)
# - memory boundaries via checkpointers
# - human-in-the-loop interrupts + resume
# - Deep Agents demos (todos/filesystem/subagents/HITL/sandboxing)

# %% [markdown]
# ## LangGraph: StateGraph (hello)
#
# LangGraph is a way to express workflows as a **stateful graph**.
#
# If you’ve ever thought “I wish this agent had a clear structure and memory,” this is the tool.
#
# A tiny checklist as you read the next cell:
# - What does “state” look like? (a dict / TypedDict)
# - What are the nodes? (functions that read + return updates)
# - How do edges determine what runs next?

# %%
from typing import TypedDict
import langgraph.graph


class S(TypedDict):
    """Simple state with counter and message."""

    n: int
    msg: str


print("State schema S defined with fields 'n' (int) and 'msg' (str)")


# %%
def inc(state: S) -> dict:
    """Increment `state['n']` by 1."""
    return {"n": state.get("n", 0) + 1}


def set_msg(state: S) -> dict:
    """Set `state['msg']` to a string derived from the current counter."""
    return {"msg": f"n={state.get('n', 0)}"}


print("Node functions defined: inc() and set_msg()")

# %%
g = langgraph.graph.StateGraph(S)
g.add_node("inc", inc)
g.add_node("msg", set_msg)
g.add_edge(langgraph.graph.START, "inc")
g.add_edge("inc", "msg")
g.add_edge("msg", langgraph.graph.END)
graph = g.compile()

print("Graph constructed: START -> inc -> msg -> END")

# Test invocation.
result = graph.invoke({"n": 0, "msg": ""})
print(f"Invocation result: {result}")

# %% [markdown]
# ## LangGraph: conditional routing
#
# Graphs get interesting when the next step depends on state.
#
# In this section you’ll see:
# - a node returns an update
# - a router looks at state and chooses the next node
#
# This is the foundation for “if the model asked for a tool, run tools; otherwise, finish.”

# %%
from typing import Literal


# #############################################################################
# State Schema with Routing
# #############################################################################


class R(TypedDict):
    """State for routing example."""

    flag: bool
    out: str


print("State schema R defined with fields 'flag' (bool) and 'out' (str)")


# %%
def a(state: R) -> dict:
    """Write a marker output for the `A` branch."""
    return {"out": "path=A"}


def b(state: R) -> dict:
    """Write a marker output for the `B` branch."""
    return {"out": "path=B"}


def route(state: R) -> Literal["a", "b"]:
    """Route based on the boolean `state['flag']`."""
    return "a" if state.get("flag") else "b"


print("Node functions defined: a(), b(), and route()")

# %%
g = StateGraph(R)
g.add_node("a", a)
g.add_node("b", b)
g.add_conditional_edges(langgraph.graph.START, route, {"a": "a", "b": "b"})
g.add_edge("a", langgraph.graph.END)
g.add_edge("b", langgraph.graph.END)
graph = g.compile()

print("Graph constructed with conditional routing")

# Test both branches.
result_true = graph.invoke({"flag": True, "out": ""})
result_false = graph.invoke({"flag": False, "out": ""})
print(f"Path A (flag=True): {result_true}")
print(f"Path B (flag=False): {result_false}")

# %% [markdown]
# ## LangGraph: reducers (accumulate evidence)
#
# Reducers are how you *accumulate* state across steps.
#
# Common uses:
# - collect “evidence” across iterations
# - build up a list of intermediate results
# - append messages rather than overwrite
#
# In the next cell, focus on how state updates combine rather than replace.

# %%
from typing import Annotated, List


def add_list(old: List[str], new: List[str]) -> List[str]:
    """Reducer that concatenates two evidence lists."""
    return old + new


# #############################################################################
# ReducerState
# #############################################################################


class ReducerState(TypedDict):
    """State with reducer for accumulating evidence."""

    evidence: Annotated[List[str], add_list]


print(
    "State schema ReducerState defined with evidence field using add_list reducer"
)


# %%
def find_missingness(_: ReducerState) -> dict:
    """Compute missingness findings from the local dataset."""
    miss = (df.isna().mean() * 100).sort_values(ascending=False)
    top = miss.head(3)
    evidence = [
        f"missingness: {idx} has {val:.2f}% missing" for idx, val in top.items()
    ]
    return {"evidence": evidence}


def find_outliers(_: ReducerState) -> dict:
    """Compute a simple outlier finding using z-scores on one numeric column."""
    numeric_cols = [c for c in df.columns if c != "Date/Time"]
    col = None
    if "Wind Speed (m/s)" in df.columns:
        col = "Wind Speed (m/s)"
    elif numeric_cols:
        col = numeric_cols[0]
    if not col:
        return {"evidence": ["outliers: no numeric columns found"]}
    s = df[col].astype(float)
    mu = float(s.mean())
    sigma = float(s.std(ddof=0))
    if sigma == 0.0:
        return {
            "evidence": [f"outliers: std({col}) is 0, cannot compute z-scores"]
        }
    z = ((s - mu) / sigma).abs()
    idx = int(z.idxmax())
    ts = None
    if "Date/Time" in df.columns:
        ts = df.loc[idx, "Date/Time"]
    evidence = [
        f"outliers: max |z| for {col} at row={idx} ts={ts} value={s.loc[idx]:.3f} z={z.loc[idx]:.2f}"
    ]
    return {"evidence": evidence}


print("Analysis functions defined: find_missingness() and find_outliers()")

# %%
g = StateGraph(ReducerState)
g.add_node("missingness", find_missingness)
g.add_node("outliers", find_outliers)
g.add_edge(langgraph.graph.START, "missingness")
g.add_edge("missingness", "outliers")
g.add_edge("outliers", langgraph.graph.END)
graph = g.compile()

print("Graph constructed: START -> missingness -> outliers -> END")

# Test invocation and display results.
result = graph.invoke({"evidence": []})
print("Evidence collected:")
for item in result["evidence"]:
    print(f"  - {item}")

# %% [markdown]
# ## ReAct loop from scratch: model node + ToolNode
#
# ReAct (“Reason + Act”) is a simple pattern:
#
# - the model thinks about what to do
# - if it needs information, it calls a tool
# - it repeats until it can answer
#
# Here we build that loop explicitly with LangGraph:
# - a model node that proposes tool calls
# - a `ToolNode` that executes them
# - routing logic that decides whether to continue looping
#
# This is one of the best places to pause and say: “Ah — *this* is what an agent really is.”

# %%
from typing import Annotated as Ann
import langgraph.graph.message
import langgraph.prebuilt


# #############################################################################
# State Schema with Message History
# #############################################################################


class RS(TypedDict):
    """State with messages accumulated using add_messages reducer."""

    messages: Ann[list, langgraph.graph.message.add_messages]


print("State schema RS defined with messages field")


# %%
tools = [utc_now, mean, sqrt]
tool_node = langgraph.prebuilt.ToolNode(tools)


def call_model(state: RS) -> dict:
    """Call the model with bound tools and append the AI message."""
    bound = llm.bind_tools(tools)
    ai = bound.invoke(state["messages"])
    return {"messages": [ai]}


def needs_tools(state: RS) -> str:
    """Route to tools if the last AI message contains tool calls."""
    last = state["messages"][-1]
    return "tools" if getattr(last, "tool_calls", None) else "end"


print("Tools defined and node functions created: call_model() and needs_tools()")

# %%
g = StateGraph(RS)
g.add_node("model", call_model)
g.add_node("tools", tool_node)
g.add_edge(langgraph.graph.START, "model")
g.add_conditional_edges(
    "model", needs_tools, {"tools": "tools", "end": langgraph.graph.END}
)
g.add_edge("tools", "model")
graph = g.compile()

print("Graph constructed with conditional tool execution")

# Test invocation with multiple tool requests.
out = graph.invoke(
    {
        "messages": [
            langchain_core.messages.HumanMessage(
                content="Compute mean([1,2,3,4,10]) and sqrt(49). Also tell me the current UTC time."
            )
        ]
    }
)

# Display message summary.
summary = [
    (type(m).__name__, getattr(m, "content", "")[:120]) for m in out["messages"]
][-4:]
for msg_type, content in summary:
    print(f"{msg_type}: {content}")

# %% [markdown]
# ## Subagents: supervisor + worker tools
#
# A helpful pattern is to split responsibilities:
# - a **supervisor** decides what needs doing
# - **workers** do specialized tasks (often via tools)
#
# This keeps each piece simpler and makes debugging much easier.

# %%
import langchain.tools


def _last_text(result: dict) -> str:
    """
    Return the final message text/content from an agent result state.
    """
    msg = result["messages"][-1]
    return (
        getattr(msg, "text", None) or getattr(msg, "content", None) or str(msg)
    )


# Create worker agent specialized in summarization.
worker_agent = create_agent(
    llm,
    tools=[],
    system_prompt=(
        "You are a summarization specialist.\n"
        "Given text, return:\n"
        "- 1 sentence summary\n"
        "- 3 bullet key points\n"
        "Return only the summary + bullets."
    ),
)

print("Worker agent created for summarization tasks")


# %%
@langchain.tools.tool(
    "summarize_text",
    description="Summarize long text into a short summary + 3 bullet points.",
)
def summarize_text(text: str) -> str:
    """
    Summarize `text` using the worker agent and return a plain string.
    """
    return _last_text(
        worker_agent.invoke({"messages": [{"role": "user", "content": text}]})
    )


print("Tool defined: summarize_text wraps worker agent")

# %%
supervisor = create_agent(
    llm,
    tools=[summarize_text],
    system_prompt="If asked to summarize, call summarize_text and return the tool output.",
)

print("Supervisor agent created with summarize_text tool")

# Test invocation.
out = supervisor.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": "Summarize: LangChain provides building blocks for LLM apps.",
            }
        ]
    }
)
result = _last_text(out)
print(f"Supervisor response:\n{result}")

# %% [markdown]
# ## Subagents: ToolRuntime state + Command(update=...)
#
# Sometimes you want a tool to do more than return a value — you want it to update graph state.
#
# In LangGraph that’s expressed with `Command(update=...)`.
#
# You’ll also see `ToolRuntime`, which gives the tool access to useful runtime context (like the current state).

# %%
import json
from typing_extensions import Annotated as TxAnnotated

import langchain.agents
import langchain.tools
import langchain_core.messages
import langgraph.types


# #############################################################################
# CustomState with Runtime-Aware Tools
# #############################################################################


class CustomState(langchain.agents.AgentState):
    """Extended state with user preferences and facts accumulator."""

    user_prefs: dict
    facts: list[str]


print("CustomState defined with user_prefs and facts fields")


# %%
worker = create_agent(
    llm, tools=[], system_prompt="Rewrite text. Return only rewritten text."
)


@langchain.tools.tool(
    "rewrite_with_prefs",
    description="Rewrite text following preferences from supervisor state.",
)
def rewrite_with_prefs(
    text: str, runtime: langchain.tools.ToolRuntime[None, CustomState]
) -> str:
    """
    Rewrite `text` using supervisor preferences available via `runtime.state`.
    """
    tone = runtime.state.get("user_prefs", {}).get("tone", "neutral")
    result = worker.invoke(
        {
            "messages": [
                {"role": "system", "content": f"Tone must be: {tone}."},
                {"role": "user", "content": text},
            ]
        }
    )
    return _last_text(result)


print("Rewrite worker and rewrite_with_prefs tool defined")

# %%
fact_worker = create_agent(
    llm, tools=[], system_prompt='Return ONLY JSON: {"facts": ["..."]}'
)


@langchain.tools.tool(
    "extract_facts",
    description="Extract facts and update supervisor state via Command(update=...).",
)
def extract_facts(
    text: str, tool_call_id: TxAnnotated[str, langchain.tools.InjectedToolCallId]
) -> langgraph.types.Command:
    """
    Extract facts and store them in the supervisor state via `Command(update=...)`.
    """
    raw = _last_text(
        fact_worker.invoke({"messages": [{"role": "user", "content": text}]})
    )
    try:
        facts = list(json.loads(raw).get("facts", []))
    except Exception:
        facts = [raw]
    return langgraph.types.Command(
        update={
            "facts": facts,
            "messages": [
                langchain_core.messages.ToolMessage(
                    content=f"Stored {len(facts)} facts.",
                    tool_call_id=tool_call_id,
                )
            ],
        }
    )


print("Fact worker and extract_facts tool defined with Command return")

# %%
supervisor = create_agent(
    llm,
    tools=[rewrite_with_prefs, extract_facts],
    system_prompt="Use rewrite_with_prefs for rewrite requests; use extract_facts for 'read and explain'.",
    state_schema=CustomState,
)

print("Supervisor agent created with both tools")

# Test rewrite with preferences.
out1 = supervisor.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": "Rewrite: please send me the report by tonight.",
            }
        ],
        "user_prefs": {"tone": "formal"},
        "facts": [],
    }
)
print(f"Rewrite result (formal tone): {_last_text(out1)}")

# Test fact extraction.
out2 = supervisor.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": "Read this and explain it: LangGraph supports interrupts.",
            }
        ],
        "user_prefs": {"tone": "neutral"},
        "facts": [],
    }
)
print(f"Facts extracted: {out2.get('facts')}")

# %%
# Example: Two subagents (date normalization + email drafting)

# Define specialized subagent for date normalization.
date_agent = create_agent(
    llm,
    tools=[],
    system_prompt='Return ONLY JSON: {"normalized": "...", "notes": "..."}',
)


@langchain.tools.tool(
    "normalize_datetime",
    description="Normalize informal date/time mentions into an explicit format. Returns JSON.",
)
def normalize_datetime(request: str) -> str:
    """
    Normalize an informal date/time request using a specialized subagent.
    """
    return _last_text(
        date_agent.invoke({"messages": [{"role": "user", "content": request}]})
    )


print("Date normalization agent and tool defined")

# Define specialized subagent for email drafting.
email_agent = create_agent(
    llm,
    tools=[],
    system_prompt="Draft a short professional email body. Return only the email body.",
)


@langchain.tools.tool(
    "draft_email_body",
    description="Draft a concise professional email body for a user request.",
)
def draft_email_body(request: str) -> str:
    """
    Draft a short professional email body for `request`.
    """
    return _last_text(
        email_agent.invoke({"messages": [{"role": "user", "content": request}]})
    )


print("Email drafting agent and tool defined")

# %%
sup = create_agent(
    llm,
    tools=[normalize_datetime, draft_email_body],
    system_prompt="Pick the right tool for the user's intent.",
)

print("Supervisor agent created with both tools")

# Test date normalization.
a = sup.invoke(
    {
        "messages": [
            {"role": "user", "content": "Normalize: next Tuesday at 2pm."}
        ]
    }
)
print(f"Date normalization: {_last_text(a)}")

# Test email drafting.
b = sup.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": "Write an email to my professor asking for a 2-day extension.",
            }
        ]
    }
)
print(f"Email draft: {_last_text(b)}")


# %%
# Example: Context isolation (noisy worker, clean supervisor)


# Define a tool that generates noise to simulate intermediate work.
@langchain.tools.tool(
    "generate_noise",
    description="Generate a long string to simulate noisy intermediate work.",
)
def generate_noise(n_chars: int) -> str:
    """
    Generate a long string used to simulate irrelevant intermediate work.
    """
    return "X" * int(n_chars)


print("Noise generation tool defined")

# Create a noisy worker agent that produces intermediate noise.
noisy_worker_agent = create_agent(
    llm,
    tools=[generate_noise],
    system_prompt=(
        "You MUST call generate_noise with n_chars=8000 exactly once, then ignore it.\n"
        "Return ONLY a concise 2-sentence answer."
    ),
)


@langchain.tools.tool(
    "noisy_worker",
    description="Do a task in an isolated context and return a concise final answer.",
)
def noisy_worker(task: str) -> str:
    """
    Run `task` in an isolated subagent context and return the final answer.
    """
    return _last_text(
        noisy_worker_agent.invoke(
            {"messages": [{"role": "user", "content": task}]}
        )
    )


print("Noisy worker agent and tool defined")


# %%
sup = create_agent(
    llm,
    tools=[noisy_worker],
    system_prompt="Call noisy_worker for the user's request.",
)

print("Supervisor agent created with noisy_worker tool")

# Invoke supervisor with a request.
out = sup.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": "Explain in plain English what 'context isolation' means in subagents.",
            }
        ]
    }
)

result = _last_text(out)
print(f"Final answer (noisy intermediate work isolated):\n{result}")

# %%
# Example: Parallel tool calls (one AI turn emits multiple tool calls)

# Create three specialized subagents.
sum_agent = create_agent(
    llm,
    tools=[],
    system_prompt="Summarize in 2 sentences. Return only the summary.",
)
act_agent = create_agent(
    llm,
    tools=[],
    system_prompt="Extract action items as bullets. Return only bullets.",
)
reply_agent = create_agent(
    llm,
    tools=[],
    system_prompt="Draft a short reply email. Return only the email body.",
)

print("Three specialized subagents defined: sum_agent, act_agent, reply_agent")


# %%
@langchain.tools.tool(
    "sub_summarize", description="Summarize the text in 2 sentences."
)
def sub_summarize(text: str) -> str:
    """
    Summarize `text` in 2 sentences.
    """
    return _last_text(
        sum_agent.invoke({"messages": [{"role": "user", "content": text}]})
    )


@langchain.tools.tool(
    "sub_action_items", description="Extract action items as bullet points."
)
def sub_action_items(text: str) -> str:
    """
    Extract action items from `text` as bullet points.
    """
    return _last_text(
        act_agent.invoke({"messages": [{"role": "user", "content": text}]})
    )


@langchain.tools.tool(
    "sub_draft_reply",
    description="Draft a short email reply addressing the content.",
)
def sub_draft_reply(text: str) -> str:
    """
    Draft a short email reply based on `text`.
    """
    return _last_text(
        reply_agent.invoke({"messages": [{"role": "user", "content": text}]})
    )


print("Three tools defined: sub_summarize, sub_action_items, sub_draft_reply")

# %%
sup = create_agent(
    llm,
    tools=[sub_summarize, sub_action_items, sub_draft_reply],
    system_prompt="Use tools as needed and return a clean final response.",
)

print("Supervisor agent created with three parallel tools")

# Test with email thread that triggers all three tools.
email_thread = (
    "Call ALL THREE tools (sub_summarize, sub_action_items, sub_draft_reply). "
    "Text: We need to ship the notebook execution feature by Friday. Please confirm papermill works."
)
out = sup.invoke({"messages": [{"role": "user", "content": email_thread}]})

result = _last_text(out)
print(f"Supervisor response with parallel tool results:\n{result}")

# %% [markdown]
# ## Subgraphs (graph-as-node composition)
#
# A subgraph is just a graph you treat like a node.
#
# This is how you build larger systems without everything becoming one giant tangle:
# - small graph for “extract facts”
# - small graph for “summarize”
# - parent graph that composes them
#
#
#
# #############################################################################
# SubState
# #############################################################################


# %%
# Example: Subgraph Composition

# ##########################################################
# Define SubState and subgraph for parsing and formatting.
# ##########################################################


class SubState(TypedDict):
    """State for subgraph: raw text -> parsed dict -> formatted output."""

    raw: str
    parsed: dict
    formatted: str


def parse_node(state: SubState) -> dict:
    """Parse `key: value` lines from `state['raw']` into a dict."""
    raw = state["raw"]
    parsed = {}
    for line in raw.splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            parsed[k.strip()] = v.strip()
    return {"parsed": parsed}


def format_node(state: SubState) -> dict:
    """Format the parsed fields as a bullet list."""
    parsed = state.get("parsed", {})
    lines = [f"- {k}: {v}" for k, v in parsed.items()]
    return {"formatted": "Parsed fields:\n" + "\n".join(lines)}


print("SubState and node functions defined")


# %%
sub = StateGraph(SubState)
sub.add_node("parse", parse_node)
sub.add_node("format", format_node)
sub.add_edge(langgraph.graph.START, "parse")
sub.add_edge("parse", "format")
sub.add_edge("format", langgraph.graph.END)
subgraph = sub.compile()

print("Subgraph constructed: START -> parse -> format -> END")

# %%
# ##########################################################
# Define ParentState and parent graph that calls subgraph.
# ##########################################################


class ParentState(TypedDict):
    """Parent state that calls subgraph and receives formatted output."""

    user_text: str
    result: str


def call_subgraph(state: ParentState) -> dict:
    """Call `subgraph` and project its formatted output into the parent state."""
    out = subgraph.invoke({"raw": state["user_text"]})
    return {"result": out["formatted"]}


parent = StateGraph(ParentState)
parent.add_node("worker", call_subgraph)
parent.add_edge(langgraph.graph.START, "worker")
parent.add_edge("worker", langgraph.graph.END)
parent_graph = parent.compile()

print("Parent graph constructed with subgraph call node")

# %%
# Test the parent graph with sample input.
result = parent_graph.invoke(
    {
        "user_text": "name: Indro\nrole: ML engineer\nlocation: Kolkata",
        "result": "",
    }
)

print("Parent graph result:")
print(result["result"])

# %% [markdown]
# ## Shared vs private memory boundaries (checkpointers)
#
# Checkpointers are how LangGraph remembers state across runs.
#
# This section helps answer:
# - what does `thread_id` do?
# - when do two runs share memory vs start fresh?
# - how do you keep different users/sessions isolated?
#
# If you’ve ever debugged an agent that “remembered the wrong thing,” this is the antidote.

# %%


# ##########################################################
# Setup: Subgraph state and shared vs private instances.
# ##########################################################


class CSub(TypedDict):
    """Simple counter state for subgraph."""

    n: int


def bump(state: CSub) -> dict:
    """Increment a counter used to demonstrate subgraph memory behavior."""
    return {"n": state.get("n", 0) + 1}


# Create two instances: shared (stateless) and private (with memory).
sub_builder = StateGraph(CSub)
sub_builder.add_node("bump", bump)
sub_builder.add_edge(langgraph.graph.START, "bump")
sub_builder.add_edge("bump", langgraph.graph.END)

sub_shared = sub_builder.compile()
sub_private = sub_builder.compile(
    checkpointer=langgraph.checkpoint.memory.MemorySaver()
)

print(
    "Subgraph instances created: sub_shared (stateless) and sub_private (with memory)"
)


# %%
# ##########################################################
# Parent state and node that calls shared vs private.
# ##########################################################


class P(TypedDict):
    """Parent state for switching between shared/private subgraphs."""

    mode: str
    sub_n: int


def call_sub(state: P) -> dict:
    """Call the shared or private subgraph depending on `state['mode']`."""
    if state["mode"] == "shared":
        out = sub_shared.invoke({"n": state.get("sub_n", 0)})
        return {"sub_n": out["n"]}
    out = sub_private.invoke(
        {"n": 0}, config={"configurable": {"thread_id": "SUBGRAPH_THREAD"}}
    )
    return {"sub_n": out["n"]}


print("Parent state P and call_sub node defined")

# %%
parent_builder = StateGraph(P)
parent_builder.add_node("call_sub", call_sub)
parent_builder.add_edge(langgraph.graph.START, "call_sub")
parent_builder.add_edge("call_sub", langgraph.graph.END)
parent = parent_builder.compile(
    checkpointer=langgraph.checkpoint.memory.MemorySaver()
)

print("Parent graph constructed with checkpoint memory")


def run_twice(mode: str):
    """Invoke the parent graph twice and return the two observed sub-counters."""
    out1 = parent.invoke(
        {"mode": mode, "sub_n": 0},
        config={"configurable": {"thread_id": f"PARENT_{mode}"}},
    )
    out2 = parent.invoke(
        {"mode": mode, "sub_n": out1["sub_n"]},
        config={"configurable": {"thread_id": f"PARENT_{mode}"}},
    )
    return out1["sub_n"], out2["sub_n"]


# Test both shared and private modes.
shared_results = run_twice("shared")
private_results = run_twice("private")

print(f"Shared subgraph (stateless) results: {shared_results}")
print(f"Private subgraph (with memory) results: {private_results}")

# %% [markdown]
# ## Human-in-the-loop gate (interrupt + resume)
#
# HITL isn’t about slowing you down — it’s about making powerful agents *safe*.
#
# In this section, the graph will:
# - pause with an interrupt payload
# - wait for a human decision
# - resume using `Command(resume=...)`
#
# If you’re wondering “where does the UI come from?” — great question.
# LangGraph gives you the **primitive** (interrupt + resume). You can surface that in a notebook, a web app, Slack, etc.

# %%
from pathlib import Path
from typing import Literal as Lit

import langgraph.types
import langgraph.checkpoint.memory


# ##########################################################
# HITL (Human-In-The-Loop) State and Nodes
# ##########################################################


class HITLState(TypedDict):
    """State for human-in-the-loop file deletion workflow."""

    target_path: str
    decision: Lit["approve", "reject", ""]


def propose_delete(state: HITLState) -> dict:
    """Emit an interrupt asking for approval to delete `state['target_path']`."""
    payload = {
        "action": "delete_file",
        "target_path": state["target_path"],
        "message": "Approve deletion?",
    }
    decision = langgraph.types.interrupt(payload)
    return {"decision": decision}


def do_delete(state: HITLState) -> dict:
    """Delete the file if the prior interrupt decision was `approve`."""
    if state["decision"] != "approve":
        return {}
    p = Path(state["target_path"])
    if p.exists() and p.is_file():
        p.unlink()
    return {}


print("HITL state and node functions defined")


# %%
builder = StateGraph(HITLState)
builder.add_node("propose", propose_delete)
builder.add_node("delete", do_delete)
builder.add_edge(langgraph.graph.START, "propose")
builder.add_edge("propose", "delete")
builder.add_edge("delete", langgraph.graph.END)

hitl_graph = builder.compile(
    checkpointer=langgraph.checkpoint.memory.MemorySaver()
)

print("HITL graph constructed with checkpoint memory")

# %%
# Setup test file and invoke with interrupt.
tmp_dir = Path("tmp_runs").resolve()
tmp_dir.mkdir(parents=True, exist_ok=True)
victim = tmp_dir / "victim.txt"
victim.write_text("delete me", encoding="utf-8")

print(f"Test file created at: {victim}")

thread_id = "HITL_NOTEBOOK_DEMO"

# First invocation: propose deletion (will hit interrupt).
out1 = hitl_graph.invoke(
    {"target_path": str(victim), "decision": ""},
    config={"configurable": {"thread_id": thread_id}},
)

# Extract the interrupt payload.
pending = (
    out1.get("__interrupt__", [])[0].value if "__interrupt__" in out1 else None
)
print(f"Interrupt triggered with payload: {pending}")

# %%
out2 = hitl_graph.invoke(
    langgraph.types.Command(resume="approve"),
    config={"configurable": {"thread_id": thread_id}},
)
victim.exists()
