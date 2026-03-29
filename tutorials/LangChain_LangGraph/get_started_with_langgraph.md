---
title: "Getting Started with LangGraph"
draft: true
authors:
  - "Indrayudd Roy Chowdhury"
  - "<Author2>"
date: 2026-03-19
description: A story-driven starter on the LangGraph patterns we found useful for turning LangChain components into stateful agent workflows.
categories:
  - AI Research
  - Software Engineering
---

TL;DR: If LangChain gives you the pieces, LangGraph gives you the choreography:
state, routing, reducers, memory, interrupts, and control to make agentic
workflows deliberate.

<!-- more -->

# Summary
- This document covers core patterns in LangGraph for building stateful,
  controlled agentic workflows
- LangGraph extends LangChain by adding explicit state, routing logic, and
  memory management
- The patterns shown here (StateGraph, conditional routing, reducers,
  interrupts) apply to analytical and automation workflows
- Content derived from `tutorials/LangChain_LangGraph/`, particularly
  `langgraph.example.py`

# When to Use LangGraph
- LangChain handles individual pieces: prompts, runnables, tools, initial agent
  loops
- LangGraph handles workflow coordination when you need:
  - Steps that depend on previous outcomes
  - State that persists across turns
  - Pauses before destructive actions
  - Separation of concerns between workers
  - Systems that proceed methodically, not just answer

# The Conceptual Shift
- **LangChain**: define the pieces of behavior
- **LangGraph**: define what happens next, and with what state
- Graphs become essential when you care about loops, branching, memory, or
  approval gates

# 1. StateGraph Is the Foundation
- The first LangGraph example is deliberately minimal
```python
from typing import TypedDict
from langgraph.graph import END, START, StateGraph

class S(TypedDict):
    n: int
    msg: str

def inc(state: S) -> dict:
    return {"n": state.get("n", 0) + 1}

def set_msg(state: S) -> dict:
    return {"msg": f"n={state.get('n', 0)}"}

g = StateGraph(S)
g.add_node("inc", inc)
g.add_node("msg", set_msg)
g.add_edge(START, "inc")
g.add_edge("inc", "msg")
g.add_edge("msg", END)
graph = g.compile()
```

- Introduces three essential concepts:
  - Explicit **state** (TypedDict defining workflow data)
  - **State updates** returned by node functions
  - **Execution order** determined by edges
- Explicitness prevents hidden control flow once workflows become critical

# 2. Conditional Routing
- A graph becomes agentic when the next step depends on current state
- Routing enables decision points in the workflow
```python
from typing import Literal

class R(TypedDict):
    flag: bool
    out: str

def route(state: R) -> Literal["a", "b"]:
    return "a" if state.get("flag") else "b"

g = StateGraph(R)
g.add_node("a", a)
g.add_node("b", b)
g.add_conditional_edges(START, route, {"a": "a", "b": "b"})
g.add_edge("a", END)
g.add_edge("b", END)
```

- Common routing patterns:
  - Model called a tool: route to tool execution
  - Validation failed: route back to repair
  - Request is risky: route to approval gate
  - Branch complete: route to END
- Agent behavior is controlled branching with meaningful names

# 3. Reducers
- State updates do not always overwrite; they can accumulate
- Reducers combine old and new state values instead of replacing them
```python
from typing import Annotated, List

def add_list(old: List[str], new: List[str]) -> List[str]:
    return old + new

class ReducerState(TypedDict):
    evidence: Annotated[List[str], add_list]
```

- Analytical workflows collect signals progressively, not answer monolithically
- Example: gather evidence of missingness and outliers across steps
- Accumulation becomes explicit instead of improvised

# 4. The ReAct Loop
- ReAct becomes concrete when you write the graph yourself
- Avoids mystique by showing the actual structure
```python
from typing import Annotated as Ann
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode

class RS(TypedDict):
    messages: Ann[list, add_messages]

tools = [utc_now, mean, sqrt]
tool_node = ToolNode(tools)

def call_model(state: RS) -> dict:
    bound = llm.bind_tools(tools)
    ai = bound.invoke(state["messages"])
    return {"messages": [ai]}

def needs_tools(state: RS) -> str:
    last = state["messages"][-1]
    return "tools" if getattr(last, "tool_calls", None) else "end"
```

- Graph loop structure:
  1. Model node (reason, optionally request tools)
  2. Router (check if tool calls exist)
  3. Tool node (if tools called, execute them)
  4. Back to model (continue until no tool calls)
- An agent is a loop that reasons, acts, observes, and continues until stopping

# 5. Subagents
- Keep worker responsibilities small and focused
- Common pattern: supervisor with specialized worker subagents
```python
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

@lc_tool("summarize_text", description="Summarize long text.")
def summarize_text(text: str) -> str:
    return _last_text(
        worker_agent.invoke({"messages": [{"role": "user", "content": text}]})
    )
```

- Each worker specializes in one task
- Supervisor avoids intermediate noise
- System becomes easier to debug: each component has smaller scope and failure
  surface

# 6. Tools That Update State
- Simple return values are sometimes insufficient
- Tools can update graph state using `ToolRuntime` and `Command(update=...)`
```python
from langchain.agents import AgentState
from langchain.tools import InjectedToolCallId, ToolRuntime
from langchain_core.messages import ToolMessage
from langgraph.types import Command
from typing_extensions import Annotated as TxAnnotated

class CustomState(AgentState):
    user_prefs: dict
    facts: list[str]

@lc_tool(
    "extract_facts",
    description="Extract facts and update supervisor state via Command(update=...).",
)
def extract_facts(
    text: str, tool_call_id: TxAnnotated[str, InjectedToolCallId]
) -> Command:
    return Command(
        update={
            "facts": ["LangGraph supports interrupts."],
            "messages": [
                ToolMessage(
                    content="Stored 1 facts.",
                    tool_call_id=tool_call_id,
                )
            ],
        }
    )
```

- Tools transition from helpers to workflow participants
- Critical for automation: results become durable state, not buried in message
  history
- Workflow captures evidence progressively as state, not just conversation

# 7. Subgraphs
- Large graphs become difficult to reason about
- Solution: treat a graph as a node in another graph
- Enables modular composition
```python
class SubState(TypedDict):
    raw: str
    parsed: dict
    formatted: str

sub = StateGraph(SubState)
sub.add_node("parse", parse_node)
sub.add_node("format", format_node)
sub.add_edge(START, "parse")
sub.add_edge("parse", "format")
sub.add_edge("format", END)
subgraph = sub.compile()
```

- Parent graph calls subgraph and projects output into parent state
- Analytical workflows naturally partition into subgraphs:
  - One subgraph for extraction
  - One for summarization
  - One for verification
  - Parent graph handles orchestration

# 8. Checkpointers
- Memory requires explicit design; workflows misremember without clear
  boundaries
- Checkpointers decide what persists and what scope each thread has
```python
from langgraph.checkpoint.memory import MemorySaver

sub_private = sub_builder.compile(checkpointer=MemorySaver())
parent = parent_builder.compile(checkpointer=MemorySaver())

out = parent.invoke(
    {"mode": "private", "sub_n": 0},
    config={"configurable": {"thread_id": "PARENT_private"}},
)
```

- Practical scoping questions:
  - What does `thread_id` scope?
  - When do two runs share memory?
  - When should a subgraph keep private memory instead of inheriting parent
    history?
- Memory errors occur when boundaries are unclear, not when design is
  overcomplicated

# 9. Interrupts and Human-in-the-Loop
- Human-in-the-loop gates require explicit pause and resume mechanics
- Interrupts provide this primitive for controlled workflow pausing
```python
from langgraph.types import Command, interrupt

def propose_delete(state: HITLState) -> dict:
    payload = {
        "action": "delete_file",
        "target_path": state["target_path"],
        "message": "Approve deletion?",
    }
    decision = interrupt(payload)
    return {"decision": decision}

out1 = hitl_graph.invoke(
    {"target_path": str(victim), "decision": ""},
    config={"configurable": {"thread_id": thread_id}},
)

out2 = hitl_graph.invoke(
    Command(resume="approve"),
    config={"configurable": {"thread_id": thread_id}},
)
```

- Graph emits interrupt payload and pauses
- Workflow resumes only when human decision arrives
- Enables powerful workflows without assuming full autonomy

# Why These Patterns Matter
- Automation of analytical workflows has two hard problems:
  - Generating answers (solved by LLMs)
  - Making workflow steps legible and controllable (requires explicit structure)

- LangGraph provides this explicitly:
  - `StateGraph`: workflow spine
  - Routers: explicit choices
  - Reducers: evidence accumulation
  - Subagents and subgraphs: modularity
  - Checkpointers: explicit persistence
  - Interrupts: safety as first-class design element

- If LangChain is the toolkit, LangGraph teaches workflows to proceed
  deliberately
