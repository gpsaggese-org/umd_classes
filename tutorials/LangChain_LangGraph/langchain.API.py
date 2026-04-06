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

import dotenv

import langchain
import langchain_core
import langgraph

import langchain_API_utils as ut

# Initialize logger.
_LOG = ut.init_logger("learn_langchain.api")

ut.print_environment_info()


# %% [markdown]
# ## Model

# %%
# Customize langchain.env to configure model.
dotenv.load_dotenv("langchain.env")


# %%
# !cat langchain.env

# %%
llm = ut.get_chat_model()
llm


# %% [markdown]
# ## LangChain Expression Language (LCEL)
#
# LCEL is a _pipe_ syntax for composing steps, like a Unix pipe (`a | b | c`):
# - build a prompt
# - call a model
# - parse the result

# %%
import langchain_core.prompts
import langchain_core.output_parsers

# Create a prompt template with system and human messages.
prompt = langchain_core.prompts.ChatPromptTemplate.from_messages(
    [
        ("system", "You are a concise tutor. Answer clearly."),
        ("human", "{question}"),
    ]
)
# Create a chain by piping: prompt -> model -> string output parser.
chain = prompt | llm | langchain_core.output_parsers.StrOutputParser()
chain.invoke({"question": "Explain LCEL in one sentence."})


# %% [markdown]
# ## Runnables: invoke / batch / stream / RunnableParallel
#
# A “runnable” is anything you can _call_.
#
# LangChain standardizes that with a few common methods:
# - `.invoke(input)` → one input, one output
# - `.batch([inputs])` → many inputs at once (often more efficient)
# - `.stream(input)` → yield partial outputs as they arrive
# - `RunnableParallel(...)` → run independent chains side-by-side and combine the results

# %%
import pprint

import langchain_core.prompts
import langchain_core.output_parsers

# Create a prompt for summarizing text into bullet points.
summary_prompt = langchain_core.prompts.ChatPromptTemplate.from_messages(
    [
        ("system", "You write crisp summaries."),
        ("human", "Summarize in 3 bullets:\n\n{text}"),
    ]
)

# Create a chain: prompt -> model -> parser.
summary_chain = (
    summary_prompt | llm | langchain_core.output_parsers.StrOutputParser()
)
pprint.pprint(summary_chain)


# %%
# Create a prompt for risks and caveats.
risks_prompt = langchain_core.prompts.ChatPromptTemplate.from_messages(
    [
        ("system", "You list caveats."),
        ("human", "List 3 risks/caveats:\n\n{text}"),
    ]
)

# Create a chain: prompt -> model -> parser.
risks_chain = (
    risks_prompt | llm | langchain_core.output_parsers.StrOutputParser()
)
print("Risks chain created.")

# %%
import langchain_core.runnables

# RunnableParallel runs both chains concurrently and returns both results.
parallel = langchain_core.runnables.RunnableParallel(
    summary=summary_chain, risks=risks_chain
)

# Invoke with shared input and max concurrency limit.
ret = parallel.invoke(
    {"text": "LangChain provides composable building blocks for LLM apps."},
    config={"max_concurrency": 2},
)

# Display the structured results.
pprint.pprint(ret)

# %%
# Prepare multiple questions to process in a batch.
questions = [
    {"question": "What is a tool in LangChain?"},
    {"question": "What is ToolNode in LangGraph?"},
    {"question": "What does InjectedState do?"},
]
# Process all questions concurrently (more efficient than invoking one at a time).
ret = chain.batch(
    questions, return_exceptions=True, config={"max_concurrency": 3}
)

pprint.pprint(ret)


# %%
# Stream token-by-token output to receive partial responses in real-time.
chunks = []
for chunk in chain.stream(
    {"question": "Give me a 2-bullet explanation of RunnableParallel."}
):
    chunks.append(chunk)
# Combine all chunks into the final response.
final = "".join(chunks)
final[:300] + ("..." if len(final) > 300 else "")


# %% [markdown]
# ## Tools
#
# A *tool* is a normal Python function with a schema.
# The LLM can “ask” to call a tool (with arguments), and your code executes it.
#
# Two ways you’ll see tools used:
#
# 1) **Directly** (call the function yourself)
# 2) **Inside a graph** via `ToolNode` (LangGraph executes any requested tool calls and feeds results back)

# %% [markdown]
# We’ll use a local CSV so the examples feel concrete.

# %%
# Load and prepare the dataset (load CSV, parse datetime, copy to workspace).
dataset_result = ut.load_and_prepare_dataset()
df = dataset_result["df"]


# %%
df.head(5)

# %%
# Build metadata about the dataset (columns, types, sample rows, frequency).
dataset_meta = ut.build_dataset_meta(df)
dataset_meta


# %%
# Demonstrate the mean and zscore tools.
# The mean of [1, 2, 3, 4] is 2.5.
mean_result = ut.mean.invoke({"xs": [1, 2, 3, 4]})
print(f"mean([1, 2, 3, 4]) = {mean_result}")

# The z-score measures how many standard deviations a value is from the mean.
# For xs=[1, 2, 3, 4], std ≈ 1.118, so zscore(xs, x=4) ≈ (4 - 2.5) / 1.118 ≈ 1.34.
zscore_result = ut.zscore.invoke({"xs": [1, 2, 3, 4], "x": 4})
print(f"zscore([1, 2, 3, 4], x=4) = {zscore_result}")

# %%
import langgraph.prebuilt

# Create a ToolNode that can execute the mean and zscore tools.
tool_node = langgraph.prebuilt.ToolNode([ut.mean, ut.zscore])
print(f"ToolNode created with {len([ut.mean, ut.zscore])} tools.")


# %%
import langgraph.graph

# Build a simple graph that routes all messages to the tool node.
g = langgraph.graph.StateGraph(ut.ToolState)
g.add_node("tools", tool_node)
g.add_edge(langgraph.graph.START, "tools")
g.add_edge("tools", langgraph.graph.END)
graph = g.compile()
print("Graph compiled: START -> tools -> END")

# %%
import langchain_core.messages

# Create two tool calls: mean (succeeds) and zscore (fails due to zero std).
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
print(
    f"Prepared {len(tool_calls)} tool calls: {[tc['name'] for tc in tool_calls]}"
)

# %%
# Invoke the graph with the tool calls; it returns messages with results/errors.
out = graph.invoke(
    {
        "messages": [
            langchain_core.messages.AIMessage(content="", tool_calls=tool_calls)
        ]
    }
)
[
    type(m).__name__ + ":" + (getattr(m, "content", "")[:80])
    for m in out["messages"]
]

# %% [markdown]
# ## InjectedState.
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

# %%
# Demonstrate the dataset_brief tool.
# This tool answers questions about injected dataset metadata.
# We'll show how to build a graph and invoke the tool with a question.
result = ut.dataset_brief(
    question="How many rows and columns?", dataset_meta=dataset_meta
)
import json

print(json.dumps(json.loads(result), indent=2))

# %%
import langgraph.prebuilt

# Create a ToolNode that executes the dataset_brief tool.
tool_node = langgraph.prebuilt.ToolNode([ut.dataset_brief])
print("ToolNode created for dataset_brief tool.")


# %%
import langgraph.graph

# Build a graph that injects state (dataset_meta) into the tool at runtime.
g = langgraph.graph.StateGraph(ut.InjectedStateState)
g.add_node("tools", tool_node)
g.add_edge(langgraph.graph.START, "tools")
g.add_edge("tools", langgraph.graph.END)
graph = g.compile()
print("Graph compiled: injects dataset_meta into tools at runtime.")

# %%
import json

# Prepare state with injected dataset metadata and a tool call request.
state_in: ut.InjectedStateState = {
    "dataset_meta": dataset_meta,
    "messages": [
        langchain_core.messages.AIMessage(
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

# Invoke the graph and show the result.
out = graph.invoke(state_in)
result = json.loads(out["messages"][-1].content)
print("Result from dataset_brief tool:")
print(json.dumps(result, indent=2))

# %% [markdown]
# ## InjectedStore
#
# A store is a place to keep small bits of information across calls (like preferences, cached results, or “facts we’ve already extracted”).
#
# `InjectedStore` lets a tool receive a store handle **without** the model being able to fabricate it.
#
# In this tutorial we use `InMemoryStore` for simplicity, but the pattern generalizes to other persistence layers.

# %%
# Demonstrate save_pref and load_pref tools.
# These tools manage user preferences in an injected store.
# save_pref stores a key/value pair, and load_pref retrieves it.
import langgraph.store.memory

store_demo = langgraph.store.memory.InMemoryStore()

# Save a preference.
save_result = ut.save_pref(
    user_id="alice", key="theme", value="dark", store=store_demo
)
print(f"Save: {save_result}")

# Load the preference.
load_result = ut.load_pref(user_id="alice", key="theme", store=store_demo)
print(f"Load: {load_result}")

# %%
import langgraph.store.memory
import langgraph.prebuilt

# Create an in-memory store for persisting preferences.
store = langgraph.store.memory.InMemoryStore()

# Create a ToolNode that can save/load preferences using the store.
tool_node = langgraph.prebuilt.ToolNode([ut.save_pref, ut.load_pref])
print(
    f"Created InMemoryStore and ToolNode with {len([ut.save_pref, ut.load_pref])} tools."
)


# %%
import langgraph.graph

# Build a graph that injects the store handle into the tools.
g = langgraph.graph.StateGraph(ut.StoreState)
g.add_node("tools", tool_node)
g.add_edge(langgraph.graph.START, "tools")
g.add_edge("tools", langgraph.graph.END)
graph = g.compile(store=store)
print("Graph compiled with store: tools can now access store at runtime.")

# %%
# First invoke: save a preference to the store.
out1 = graph.invoke(
    {
        "messages": [
            langchain_core.messages.AIMessage(
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
print(out1["messages"][-1].content)

# %%
# Second invoke: load the preference we just saved.
out2 = graph.invoke(
    {
        "messages": [
            langchain_core.messages.AIMessage(
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
print(out2["messages"][-1].content)

# %% [markdown]
# ## Agent APIs
#
# An *agent* is a loop: the model looks at the conversation + available tools, chooses an action, and repeats until it’s done.
#
# In this tutorial we use a helper, `create_agent(...)`, to build a tool-calling agent quickly.

# %%
import langchain.agents
import langchain_core.messages

# Create an agent that can use the utc_now tool when needed.
agent = langchain.agents.create_agent(
    model=llm,
    tools=[ut.utc_now],
    system_prompt="Use tools when a tool can answer the question more reliably than guessing.",
)

# Ask the agent to call the tool and return the exact value.
out = agent.invoke(
    {
        "messages": [
            langchain_core.messages.HumanMessage(
                content="Call utc_now and return the exact value."
            )
        ]
    }
)

# Show the agent's message history, formatted as type:content pairs.
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
import langchain.agents
import langchain_core.messages

# Create an agent with a system prompt that asks it to return a reproducible call snippet.
contract_agent = langchain.agents.create_agent(
    model=llm,
    tools=[ut.utc_now],
    system_prompt=(
        "When time is requested, call utc_now. "
        "In your final answer, include a fenced python block with the exact tool call used."
    ),
)

# Invoke the agent with a request that requires the tool.
contract_out = contract_agent.invoke(
    {
        "messages": [
            langchain_core.messages.HumanMessage(
                content="What is the current UTC time? Use your tool."
            )
        ]
    }
)

# Print the agent's final response (should include a fenced python code block).
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
# Create a custom state schema and a tool that uses it.
CustomState, extract_facts = ut.make_custom_state_and_tool()
print(f"Custom state created with fields: {CustomState.__annotations__.keys()}")


# %%
import langchain.agents

# Create an agent with a custom state that can call extract_facts.
supervisor = langchain.agents.create_agent(
    llm,
    tools=[extract_facts],
    system_prompt="First call extract_facts, then summarize the returned facts.",
    state_schema=CustomState,
)
print("Agent created with custom state and extract_facts tool.")

# %%
# Invoke the agent with initial custom state (user preferences and empty facts list).
state = supervisor.invoke(
    {
        "messages": [
            {"role": "user", "content": "Text: LangGraph supports interrupts."}
        ],
        "user_prefs": {"tone": "formal"},
        "facts": [],
    }
)

# Show the extracted facts and the agent's final response.
print("Extracted facts:")
print(state.get("facts"))
print("\nAgent's final response:")
print(getattr(state["messages"][-1], "content", "")[:160])

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
import langgraph.checkpoint.memory
import langgraph.graph

# Build a simple HITL graph: propose deletion, then execute if approved.
builder = langgraph.graph.StateGraph(ut.HITLState)
builder.add_node("propose", ut.propose_delete)
builder.add_node("delete", ut.do_delete)
builder.add_edge(langgraph.graph.START, "propose")
builder.add_edge("propose", "delete")
builder.add_edge("delete", langgraph.graph.END)

# Compile with a checkpointer for resuming from interrupts.
graph = builder.compile(checkpointer=langgraph.checkpoint.memory.MemorySaver())
print(
    "HITL graph compiled: propose -> delete -> END (with checkpointing for interrupts)."
)

# %%
import pathlib

# Create a temporary file to demonstrate the HITL pattern.
tmp_dir = pathlib.Path("tmp_runs/hitl").resolve()
tmp_dir.mkdir(parents=True, exist_ok=True)
victim = tmp_dir / "victim.txt"
victim.write_text("delete me", encoding="utf-8")

print(f"Created temporary file at: {victim}")
print(f"File exists: {victim.exists()}")

# %%
# First invoke: propose the deletion (will interrupt and ask for approval).
thread_id = "HITL_API_DEMO"
out1 = graph.invoke(
    {"target_path": str(victim), "decision": ""},
    config={"configurable": {"thread_id": thread_id}},
)

# Extract the pending decision from the interrupt payload.
pending = (
    out1.get("__interrupt__", [])[0].value if "__interrupt__" in out1 else None
)

print(f"Graph interrupted with decision pending: {pending}")

# %%
import langgraph.types

# Second invoke: resume with approval decision.
out2 = graph.invoke(
    langgraph.types.Command(resume="approve"),
    config={"configurable": {"thread_id": thread_id}},
)

# Check if the file was deleted after resuming with approval.
file_deleted = not victim.exists()
print(f"File deleted after approval: {file_deleted}")
print(f"Decision was executed: {'approve' in str(out2)}")
