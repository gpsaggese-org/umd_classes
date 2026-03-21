---
title: "Getting Started with LangChain"
draft: true
authors:
  - indro
  - gpsaggese
date: 2026-03-19
description: A story-driven starter on the LangChain building blocks we found useful while automating analytical workflows at Causify.
categories:
  - AI Research
  - Software Engineering
---

TL;DR: LangChain starts making sense when you stop looking at it as "agent magic"
and start looking at it as a small set of composable pieces: prompts,
runnables, tools, grounding, and a loop that knows when to act.

<!-- more -->

## Introduction

Some problems do not arrive dramatically. They slip in quietly.

At Causify, a lot of the work we wanted to automate was not flashy. It was the
kind of analytical work that repeats just enough to deserve structure: inspect a
dataset, read some documentation, summarize the result, compute a few numbers,
and decide what to do next. None of these steps is individually hard. What gets
hard is the handoff between them.

That is where LangChain started becoming useful for us.

Yes, the documentation already contains the APIs. But when you first encounter
`ChatPromptTemplate`, `RunnableParallel`, `@tool`, and `create_agent`, it is
easy to understand each name in isolation and still not see the larger rhythm.
This post is my attempt to make that rhythm visible.

Everything here is derived from `tutorials/LangChain_LangGraph/`, especially
`langchain.API.py` and `langchain.example.py`. I am leaving out Deep Agents for
now and focusing on the LangChain layer itself.

## The Mental Model

The simplest way I have found to think about LangChain is this:

- **Prompts** decide how work is framed
- **Runnables** decide how steps compose
- **Tools** let the model touch the outside world
- **Agents** decide when to think and when to act

Once this clicks, most of the syntax stops feeling ornamental.

## 1. Start With a Prompt Pipeline

The first useful LangChain primitive is not the agent. It is the pipe.

```python
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a concise tutor. Answer clearly."),
        ("human", "{question}"),
    ]
)

chain = prompt | llm | StrOutputParser()
chain.invoke({"question": "Explain LCEL in one sentence."})
```

This `prompt | llm | parser` pattern is LCEL, the LangChain Expression
Language. It looks small because it is small. That is the point.

For analytical workflows, this is often the first moment things become
repeatable. You stop pasting prompts manually and start treating prompt logic as
an object you can reuse.

## 2. Runnables Make the Workflow Feel Real

Once a pipeline exists, the next question is almost always: can I call it once,
many times, stream it, or run multiple branches side by side?

That is what runnables standardize.

```python
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
```

This is one of those pieces that sounds minor until you need it. In workflow
automation, parallel summaries, caveat extraction, classification, and schema
generation show up constantly. `RunnableParallel` gives that fan-out pattern a
very clean shape.

## 3. Ground the Model Before You Ask It to Help

One thing we kept rediscovering is that agentic systems become more useful the
moment they stop speaking from memory alone.

In the tutorial, even before the richer orchestration shows up, the workflow is
grounded using local data and tutorial documents. A tiny example is the docs-RAG
mini pipeline:

```python
docs_paths = [
    Path("README.md"),
    Path("langchain.API.md"),
    Path("langchain.example.md"),
]
raw_docs = tut_utils.load_markdown_documents(docs_paths)
chunked_docs = tut_utils.split_documents(
    raw_docs, chunk_size=900, chunk_overlap=120
)

embeddings = tut_utils.make_embeddings()
docs_store = tut_utils.build_vector_store(chunked_docs, embeddings)
retriever = docs_store.as_retriever(search_kwargs={"k": 3})
```

There is nothing mystical here. Read documents, split them, embed them, index
them, retrieve them. What matters is not the novelty of the idea, but how often
this becomes the difference between a helpful system and a confident hallucination.

## 4. Tools Are Where the Model Stops Narrating and Starts Acting

If LCEL is the clean thought, tools are the first clean action.

```python
from datetime import datetime, timezone
from langchain_core.tools import tool

@tool
def utc_now() -> str:
    """Return the current UTC time as an ISO string."""
    return datetime.now(timezone.utc).isoformat()


@tool
def mean(xs: list[float]) -> float:
    """Return the arithmetic mean of a non-empty list of numbers."""
    if not xs:
        raise ValueError("xs must be non-empty")
    return sum(float(x) for x in xs) / len(xs)
```

I like tools because they force honesty.

A model can describe how to compute a mean. A tool actually computes it. A
model can say what time it thinks it is. A tool returns the time. That
distinction matters a lot when the workflow is supposed to be trusted by people
who are already tired of checking everything twice.

## 5. `ToolNode` Connects Tool Calls to Execution

This is the first bridge between "the model requested something" and "the
system actually did it."

```python
from langchain_core.messages import AIMessage
from langgraph.graph import END, START, StateGraph
from langgraph.prebuilt import ToolNode

tool_node = ToolNode([mean, zscore])

g = StateGraph(ToolState)
g.add_node("tools", tool_node)
g.add_edge(START, "tools")
g.add_edge("tools", END)
graph = g.compile()

tool_calls = [
    {"name": "mean", "args": {"xs": [1, 2, 3, 4]}, "id": "t1", "type": "tool_call"},
]
out = graph.invoke({"messages": [AIMessage(content="", tool_calls=tool_calls)]})
```

Strictly speaking, `ToolNode` lives in LangGraph, but I wanted it in this post
because it clarifies an important idea early: tool calls are not magic side
effects. They are message-driven operations with a concrete execution path.

That idea becomes crucial later when the workflow grows beyond one prompt and
one reply.

## 6. `InjectedState` Lets the System Keep Ownership

One of the subtler but more important patterns in the tutorial is runtime
injection.

Sometimes the tool needs context that the model should not be allowed to invent.
Dataset metadata is a good example.

```python
import json

from langgraph.prebuilt import InjectedState
from typing_extensions import Annotated as TxAnnotated

@tool
def dataset_brief(
    question: str,
    dataset_meta: TxAnnotated[dict, InjectedState("dataset_meta")],
) -> str:
    payload = {
        "question": question,
        "n_rows": dataset_meta.get("n_rows"),
        "n_cols": dataset_meta.get("n_cols"),
        "columns": dataset_meta.get("columns"),
        "freq": dataset_meta.get("freq"),
    }
    return json.dumps(payload)
```

The model can choose the question. It cannot spoof the metadata.

This sounds like a small implementation detail until you build anything
production-facing. Then it becomes one of the clearest separations in the
system: what the model is allowed to decide, and what the runtime still owns.

## 7. `InjectedStore` Gives You Small, Durable Memory

Another recurring need in real workflows is to preserve small facts across
calls: a user preference, a chosen frequency, a known label, a saved mapping.

```python
from langgraph.prebuilt import InjectedStore
from langgraph.store.base import BaseStore
from typing_extensions import Annotated as TxAnnotated

@tool
def save_pref(
    user_id: str,
    key: str,
    value: str,
    store: TxAnnotated[BaseStore, InjectedStore()],
) -> str:
    namespace = ("prefs", user_id)
    store.put(namespace, key, {"value": value})
    return f"saved {key}={value} for user_id={user_id}"
```

In the tutorial, this is demonstrated with `InMemoryStore`, which is simple on
purpose. The larger point is that memory does not have to mean "the model
remembers." Often it just means the runtime has somewhere disciplined to keep a
few important things.

## 8. `create_agent` Is Where the Pieces Start Breathing Together

After prompts, runnables, tools, and runtime injection, the agent loop stops
feeling abstract.

```python
from math import sqrt

from langchain.agents import create_agent
from langchain_core.messages import HumanMessage

agent = create_agent(
    model=llm,
    tools=[utc_now, mean, sqrt],
    system_prompt=(
        "You are a careful assistant. Use tools when computation or time is "
        "required. When you call a tool, use its output in your final answer."
    ),
)

final_state = agent.invoke(
    {
        "messages": [
            HumanMessage(
                content="Compute mean([1,2,3,4,10]) and sqrt(49). "
                "Also tell me the current UTC time."
            )
        ]
    }
)
```

This is the version of agentic behavior that I think most people should start
with.

Not a giant framework.
Not a massive graph.
Not a dozen workers.

Just enough structure for the model to decide when it should stop speaking in
generalities and call the right function instead.

## 9. What We Found Useful in Practice

If I had to compress the LangChain part of the tutorial into one observation, it
would be this: the useful moving parts are smaller than they first appear.

- LCEL makes prompts reusable instead of fragile
- Runnables make flow explicit instead of improvised
- Tools make answers checkable instead of rhetorical
- Injected state and stores keep the runtime in charge of what the model should
  not fabricate
- `create_agent(...)` gives you a strong first version of an agent loop without
  demanding that you build the entire orchestration layer on day one

That was the layer we kept reaching for while trying to automate analytical
workflows. Not because it was dramatic, but because it turned repeated work into
structured work.

In the next post, [Getting Started with LangGraph](draft.get_started_with_langgraph.md),
I will pick up from here and move into the part where structure becomes a real
workflow: state, routing, memory, interrupts, and control over what happens
next.
