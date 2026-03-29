## Introduction

## The Mental Model
- **Prompts**: decide how work is framed
- **Runnables**: decide how steps compose
- **Tools**: let the model access the outside world
- **Agents**: decide when to think and when to act

Once understood, the syntax becomes functional rather than ornamental

## 2. Runnables Make the Workflow Feel Real
- Common workflow question: Can a pipeline run once, multiple times, as a
  stream, or with parallel branches?

- Runnables standardize these execution patterns

- Example with `RunnableParallel`:
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

- Use cases in workflow automation:
  - Parallel summaries
  - Caveat extraction
  - Classification
  - Schema generation

- `RunnableParallel` provides a clean pattern for fan-out operations

## 3. Ground the Model Before You Ask It to Help
- Agentic systems become more useful when they access external data instead of
  relying on memory alone

- Tutorial example: docs-RAG mini pipeline grounding:
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

- Grounding process: read -> split -> embed -> index -> retrieve

- Significance:
  - No novel technique
  - Practical impact: difference between helpful systems and confident
    hallucinations

## 4. Tools Are Where the Model Stops Narrating and Starts Acting
- Tools provide clean action alongside LCEL as clean thought

- Example:
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

- Why tools matter:
  - A model can describe computing a mean; a tool actually computes it
  - A model can claim current time; a tool returns actual time
  - This distinction is critical when workflows must be trusted by users
    verifying results

## 5. `ToolNode` Connects Tool Calls to Execution
- `ToolNode` bridges model requests and system execution

- Example:
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

- Key concept:
  - Tool calls are not magic side effects but message-driven operations with
    explicit execution paths
  - This becomes critical when workflows extend beyond single prompt-reply pairs

- Note: `ToolNode` is from LangGraph but clarifies a core LangChain pattern

## 6. `InjectedState` Lets the System Keep Ownership
- Runtime injection: a subtle but important pattern

- Use case: Tool needs context the model should not fabricate

- Example: Dataset metadata:
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

- Model authority:
  - Model chooses: the question
  - Model cannot spoof: the metadata

- Production impact:
  - Clear separation: what model decides vs what runtime controls
  - Critical for systems that must be trusted

## 7. `InjectedStore` Gives You Small, Durable Memory
- Recurring workflow need: preserve small facts across calls
  - User preferences
  - Chosen frequency
  - Known labels
  - Saved mappings

- Example:
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

- Memory semantics:
  - Does not require model to remember facts
  - Runtime maintains a disciplined location for important state
  - Tutorial uses `InMemoryStore` for simplicity

## 8. `create_agent` Is Where the Pieces Start Breathing Together
- After prompts, runnables, tools, and runtime injection, agent loops become
  concrete

- Example:
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

- Recommended starting point for agentic behavior:
  - Not a giant framework
  - Not a massive graph
  - Not a dozen workers
  - Just enough structure for model to decide when to call functions instead of
    speaking in generalities

## 9. What We Found Useful in Practice
- Core observation: useful moving parts are smaller than they appear

- Key components:
  - **LCEL**: makes prompts reusable instead of fragile
  - **Runnables**: make flow explicit instead of improvised
  - **Tools**: make answers checkable instead of rhetorical
  - **Injected state and stores**: keep runtime control over what model should
    not fabricate
  - **`create_agent(...)`**: provides strong first agent loop without requiring
    complete orchestration layer on day one

- Practical value:
  - Layer repeatedly used for automating analytical workflows
  - Not because of novelty but because it transforms repeated work into
    structured work

## Next Steps
- [Getting Started with LangGraph](draft.get_started_with_langgraph.md)
  continues from here
  - Covers state, routing, memory, interrupts, and execution control
