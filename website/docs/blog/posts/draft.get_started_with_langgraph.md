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
state, routing, reducers, memory, interrupts, and enough control to make an
agentic workflow feel deliberate instead of accidental.

<!-- more -->

## Introduction

In [the LangChain post](draft.get_started_with_langchain.md), I stayed with the
pieces: prompts, runnables, tools, and the first agent loop.

But there is a point where a neat tool-calling loop stops being enough.

You want one step to happen only if another step succeeded. You want context to
survive between turns. You want a workflow to pause before doing something
destructive. You want one worker to stay noisy and another to stay clean. You
want a system that does not just answer, but proceeds.

That is where LangGraph started becoming useful for us.

This post is again derived from `tutorials/LangChain_LangGraph/`, especially
`langgraph.example.py`. I am leaving out Deep Agents here as well, because I
think the LangGraph layer deserves to be seen clearly on its own first.

## The Mental Shift

The mental shift from LangChain to LangGraph is simple:

- LangChain helps you define the pieces of behavior
- LangGraph helps you define what happens next, and with what state

Once you care about loops, branching, memory, or approval gates, graphs stop
feeling like overengineering and start feeling like relief.

## 1. `StateGraph` Is the First Honest Workflow

The first LangGraph example in the tutorial is deliberately tiny, and I think
that is why it works.

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

The graph is simple enough to look almost unnecessary. But it introduces the
three things that matter:

- there is an explicit **state**
- nodes return **state updates**
- edges decide **execution order**

That explicitness is the whole point. Once a workflow matters, hidden control
flow stops being elegant.

## 2. Conditional Routing Is Where the Workflow Starts Making Decisions

A graph becomes genuinely agentic when the next step depends on what just
happened.

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

This routing pattern is the seed of many larger workflows:

- if the model asked for a tool, go to tools
- if validation failed, go back and repair
- if the request is risky, pause for approval
- if a branch is complete, end

A lot of "agent behavior" is really just controlled branching dressed in better
language.

## 3. Reducers Let State Accumulate Instead of Reset

One of my favorite LangGraph ideas is that state updates do not always overwrite
each other. Sometimes they should accumulate.

```python
from typing import Annotated, List

def add_list(old: List[str], new: List[str]) -> List[str]:
    return old + new


class ReducerState(TypedDict):
    evidence: Annotated[List[str], add_list]
```

In the tutorial, reducers are used to gather evidence such as missingness and
outlier findings from a dataset. That is a very realistic pattern. In analytical
workflows, we are rarely looking for one monolithic answer. We are collecting
signals, one step at a time, until a summary becomes justified.

Reducers make that accumulation explicit instead of improvised.

## 4. The ReAct Loop Stops Feeling Mystical When You Write It Yourself

This was one of the most useful sections for me. ReAct is often explained in
high-level language, but the graph version makes it tangible.

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

From there, the graph just loops:

- model node
- tool node
- router
- back to model until there are no more tool calls

Once you see that, a lot of the mystery disappears. An agent is not a
supernatural object. It is a loop that reasons, acts, observes the result, and
continues until it can stop.

## 5. Subagents Keep Responsibilities Small

The tutorial then moves into a pattern we found genuinely useful: the
supervisor-worker split.

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

This looks almost too straightforward, but that is exactly why it is useful.

You let one worker be good at one thing. The supervisor does not need to carry
all the intermediate noise. The system becomes easier to debug because each part
has a smaller job and a smaller failure surface.

## 6. `ToolRuntime` and `Command(update=...)` Let Tools Change State

Sometimes returning a string is not enough. The tool should also update the
graph state itself.

That is where this pattern becomes powerful:

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

This is the point where tools stop being mere helpers and start becoming real
participants in the workflow.

For automation work, this matters a lot. You often want the result of one step
to become durable workflow state, not just a sentence buried in a message
history.

## 7. Subgraphs Help You Build Without Tangling Everything Together

Once a system grows, one giant graph becomes hard to reason about. LangGraph's
answer is pleasantly literal: treat a graph like a node.

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

Then a parent graph calls it and projects its output into parent state.

This composition pattern felt especially natural for analytical workflows, where
one subgraph can own extraction, another summarization, another verification,
and the parent graph can stay focused on orchestration.

## 8. Checkpointers Decide What the Workflow Remembers

Memory is one of those words that sounds intuitive until the workflow
misremembers something.

The tutorial's `MemorySaver` example makes the boundary much clearer:

```python
from langgraph.checkpoint.memory import MemorySaver

sub_private = sub_builder.compile(checkpointer=MemorySaver())
parent = parent_builder.compile(checkpointer=MemorySaver())

out = parent.invoke(
    {"mode": "private", "sub_n": 0},
    config={"configurable": {"thread_id": "PARENT_private"}},
)
```

This section answers practical questions that show up almost immediately in real
systems:

- what exactly does `thread_id` scope
- when do two runs share memory
- when should a subgraph keep private memory instead of inheriting the parent's
  history

If an agent ever "remembered the wrong thing" in your hands, you already know
why this is not an academic detail.

## 9. `interrupt(...)` and `Command(resume=...)` Are the Safety Valve

The final pattern I want to highlight is the human-in-the-loop gate.

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

I think this is one of the clearest examples of why LangGraph is more than
"LangChain but more complicated."

It gives you a primitive for controlled pausing. The graph emits an interrupt
payload, waits, and resumes only when a human decision arrives. That makes it
possible to keep workflows powerful without pretending every action should be
fully autonomous.

## 10. Why This Layer Mattered to Us

When we were trying to automate analytical workflows at Causify, the hard part
was not generating one nice answer. The hard part was making the steps legible:
what state exists, what branch we are in, what evidence has accumulated, what
should happen next, and where a human should still intervene.

That is what LangGraph gave us.

- `StateGraph` gave the workflow a spine
- routers gave it choices
- reducers gave it memory of evidence
- subagents and subgraphs kept it modular
- checkpointers made persistence explicit
- interrupts made safety a first-class part of the design

If LangChain is the toolkit, LangGraph is the part that taught the workflow how
to proceed without losing itself.
