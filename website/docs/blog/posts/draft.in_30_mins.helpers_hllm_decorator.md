# `@llm` Decorator — Comparison with Alternatives

<!-- toc -->

- [Overview](#overview)
- [Comparison Matrix](#comparison-matrix)
- [Detailed Per-Dimension Analysis](#detailed-per-dimension-analysis)
  * [Decorator-Based API (Native Python)](#decorator-based-api-native-python)
  * [Type Safety](#type-safety)
  * [Caching](#caching)
  * [Batching / Vectorization](#batching--vectorization)
  * [Tool Use (Function Calling)](#tool-use-function-calling)
  * [Compilation (LLM → Pure Python)](#compilation-llm--pure-python)
  * [Python Integration](#python-integration)
  * [Learning Curve](#learning-curve)
  * [Structured Output Support](#structured-output-support)
  * [Async Support](#async-support)
  * [Ecosystem Maturity](#ecosystem-maturity)
- [When to Use Each Tool](#when-to-use-each-tool)
- [Summary](#summary)
- [Qualitative Positioning](#qualitative-positioning)

<!-- tocstop -->

# Overview

This document compares `@llm` (the proposed LLM-as-Function decorator library in
`helpers/hllm_decorator.py`) against seven alternative frameworks for structuring
and controlling LLM calls.

The `@llm` approach is distinct: it **wraps a Python function stub as an LLM
prompt**, using the function's type hints and docstring as the prompt
specification. It layers caching, batching, tool use, and a **compilation**
pipeline (LLM → recorded I/O pairs → pure Python function) on top of the
existing `helpers.hllm` infrastructure.

# Comparison Matrix

| Dimension | `@llm` | DSPy | LMQL | Guidance | Marvin | Outlines | LangChain LCEL | Semantic Kernel |
|-----------|--------|------|------|----------|--------|----------|----------------|-----------------|
| **Decorator-based API** | ★★★ First-class | ★☆☆ Via `@predict` | ☆☆☆ No decorator | ☆☆☆ No decorator | ★★★ `@fn` decorator | ☆☆☆ No decorator | ☆☆☆ Chain syntax | ★☆☆ `[KernelFunction]` |
| **Type safety** | ★★☆ Python type hints + runtime coercion | ★★☆ `TypedPredictor` | ★☆☆ LMQL constraint language | ★★☆ Grammar-constrained | ★★★ Pydantic-native | ★★★ Regex/grammar-guaranteed | ★☆☆ Optional `with_structured_output` | ★☆☆ Optional schema |
| **Caching** | ★★★ `hcache_simple` (hash of fn+args) | ★★☆ Built-in compiler cache | ★☆☆ Manual | ☆☆☆ None built-in | ☆☆☆ None built-in | ☆☆☆ None built-in | ★☆☆ LangSmith caching | ★☆☆ Semantic caching |
| **Batching / vectorization** | ★★☆ `vectorize=True` — single batch call | ★★★ Native `BatchedSignature` | ☆☆☆ Single-prompt only | ☆☆☆ Single-prompt only | ☆☆☆ Loop-based | ☆☆☆ Single-prompt only | ★★☆ `Runnable.map()` | ★★☆ `InvokeAsync` loop |
| **Tool use** | ★★☆ `tools=[fn1, fn2]` — native Python fns | ★★☆ Tools via signatures | ☆☆☆ Not supported | ★☆☆ Manual interleaving | ★★☆ `@fn(tools=[...])` | ☆☆☆ Not supported | ★★★ Built-in `bind_tools()` | ★★★ Native plugins |
| **Compilation (LLM→code)** | ★★★ `compile()`: I/O→tests→Python fn | ★★★ `teleprompter` + `compile` | ☆☆☆ No compilation | ☆☆☆ No compilation | ★☆☆ Distillation only | ☆☆☆ No compilation | ☆☆☆ No compilation | ☆☆☆ No compilation |
| **Python integration** | ★★★ Decorator, inspect-based, no DSL | ★★☆ Pythonic, but prompt-optimized | ★★★ Embedded in Python | ★★☆ Hybrid DSL | ★★★ Native Python | ★★☆ Python callbacks | ★★☆ LCEL expression language | ★★☆ .NET-native, Python bridge |
| **Learning curve** | ★★★ Low (standard decorator) | ★★☆ Moderate (signatures, modules) | ★★☆ Moderate (query language) | ★☆☆ High (guidance grammar) | ★★★ Low (standard decorator) | ★★☆ Moderate (generation model) | ★☆☆ Steep (chain abstractions) | ★☆☆ Steep (.NET/plugin model) |
| **Structured output** | ★★☆ Pydantic via type hints | ★★★ Pydantic `TypedPredictor` | ★★★ Constrained LMQL grammar | ★★★ Guidance grammar | ★★★ Pydantic-native | ★★★ Regex/JSON schema | ★★☆ `with_structured_output()` | ★★☆ Schema-based |
| **Async support** | ★★☆ Via underlying `hllm` (sync) | ★☆☆ Experimental | ☆☆☆ None | ☆☆☆ None | ★★☆ `async fn` | ☆☆☆ None | ★★☆ `ainvoke()` | ★★★ Native `InvokeAsync` |
| **Ecosystem maturity** | ☆☆☆ Pre-release (in design) | ★★☆ Active research community | ★★☆ Research, limited prod | ★★☆ Microsoft-backed | ★★★ Prefect-backed, stable | ★★☆ Active, growing | ★★★ Very large community | ★★★ Microsoft production |
| **Multi-shot prompting** | ★★★ `examples=[...]` injected as system prompt | ★★★ `dspy.Example` with labels | ★☆☆ Manual | ★☆☆ Manual | ★☆☆ Manual | ☆☆☆ Not supported | ★★☆ Few-shot chat templates | ★★☆ Few-shot templates |
| **Cost tracking** | ★★★ `hllm_cost.LLMCostTracker` built-in | ★☆☆ Manual via callbacks | ☆☆☆ None built-in | ☆☆☆ None built-in | ☆☆☆ None built-in | ☆☆☆ None built-in | ★★☆ LangSmith tracing | ☆☆☆ None built-in |
| **Provider portability** | ★★☆ OpenAI + OpenRouter (via helpers) | ★★★ OpenAI, Anthropic, HF, local | ★★☆ OpenAI, local models | ★★☆ OpenAI, Transformers | ★★☆ OpenAI, Anthropic, local | ★★★ Nearly all via backends | ★★★ Many integrations | ★★★ OpenAI, Azure, many |
| **Unit test generation** | ★★★ Auto-generate from cached I/O pairs | ★☆☆ Manual | ☆☆☆ None | ☆☆☆ None | ☆☆☆ None | ☆☆☆ None | ☆☆☆ Manual | ☆☆☆ None |

**Legend**: ★★★ = Excellent | ★★☆ = Good | ★☆☆ = Partial/Basic | ☆☆☆ = None/Not applicable

# Detailed Per-Dimension Analysis

## Decorator-Based API (Native Python)

- **`@llm`**: The defining feature. A standard `@llm(model="gpt-4o",
  use_cache=True)` transforms a Python function stub into an LLM-powered
  implementation. Type hints and docstrings become the prompt. No DSL, no
  template language — just Python.

  ```python
  @llm(model="gpt-4o")
  def summarize(text: str, max_words: int = 50) -> str:
      """Summarize the text concisely, respecting the word limit."""
      ...
  ```
- **DSPy**: Has `dspy.Predict` and `@dspy.predict` but the primary usage is
  through `Signature` classes rather than plain Python functions.
- **Marvin**: Has `@fn` which is the closest analog — wraps a Python function as
  an LLM call. Strong Pydantic integration.
- **LangChain / Semantic Kernel**: Use chain/plugin abstractions rather than
  decorators — more verbose for simple use cases.

## Type Safety

- **`@llm`**: Uses Python's standard `typing` module (`int`, `float`, `bool`,
  `List[T]`, `Dict[K,V]`, Pydantic `BaseModel`). Coerces string responses to the
  declared return type. Runtime validation via `hdbg` assertions.
- **Marvin / Outlines**: The gold standard — Pydantic-native structured output
  guaranteed by the LLM output being constrained to the schema.
- **DSPy**: Has `TypedPredictor` for typed inputs/outputs but requires explicit
  setup.
- **LMQL**: Uses its own constraint language rather than Python types.
- **Guidance**: Grammar-constrained generation — very powerful but requires
  learning the Guidance grammar DSL.

## Caching

- **`@llm`**: Integrates with `hcache_simple.simple_cache()` (hash of function
  source + model + args + kwargs). Supports `force_refresh`, `DISABLE_CACHE`,
  `HIT_CACHE_OR_ABORT`, and `NORMAL` modes. Cache is keyed by function identity
  + arguments.
- **DSPy**: Has a compiler cache that stores optimized prompts — but it's for
  compiled prompts, not raw call results.
- **Others**: Most frameworks lack built-in caching. LangChain has optional
  LangSmith caching; Semantic Kernel has semantic caching (different concept —
  caches semantically similar queries).

## Batching / Vectorization

- **`@llm`**: When `@llm(vectorize=True)` is used, the decorator detects batch
  inputs and makes a single LLM call with all elements, amortizing overhead
  across the batch.

  ```python
  @llm(vectorize=True)
  def classify_sentiment(texts: List[str]) -> List[str]:
      """Classify each text as POSITIVE, NEGATIVE, or NEUTRAL."""
      ...
  ```
- **DSPy**: Has `BatchedSignature` which automatically batches across inputs — a
  mature implementation.
- **LangChain**: `Runnable.map()` provides concurrent fan-out for batched
  operations.
- **Semantic Kernel**: Requires manual `for` loop with `InvokeAsync` per item.

## Tool Use (Function Calling)

- **`@llm`**: The `tools` parameter accepts a list of Python callables. The
  decorator interleaves LLM generation with tool execution — the LLM requests a
  tool call, the decorator executes the Python function, and feeds the result
  back for further reasoning.

  ```python
  @llm(tools=[search_web, calculator])
  def answer_question(query: str) -> str:
      """Answer the user's question using available tools."""
      ...
  ```
- **LangChain / Semantic Kernel**: Mature, production-hardened tool/plugin
  systems. LangChain's `bind_tools()` and Semantic Kernel's plugin model are
  the most complete in the ecosystem.
- **Marvin**: Has `@fn(tools=[...])` which is a direct analog.
- **DSPy**: Supports tool use via signatures but it's not the primary use case.

## Compilation (LLM → Pure Python)

- **`@llm`**: Unique three-stage pipeline:
  1. **Record**: Cache all (input, output) pairs from LLM calls over time
  2. **Test**: Auto-generate a `Test_<FunctionName>` class from recorded I/O
     following `testing.rules.md` conventions
  3. **Generate**: Feed I/O pairs + tests to a code-generating LLM to produce a
     pure Python function that replaces the LLM-backed stub

  This enables the "from all LLM to all code" evolution — rapid prototyping via
  LLM, then compilation to deterministic code.
- **DSPy**: Compiles/optimizes prompts (not Python code). Finds better
  few-shot examples and prompt structures but still calls an LLM at runtime.
- **Marvin**: Can distill a trained model but doesn't generate pure Python code.
- **Others**: No compilation feature.

## Python Integration

- **`@llm`**: Uses Python's `inspect` module at decoration time to extract
  signature, types, and docstring. The decorator is standard Python — no custom
  DSL, no template language.
- **DSPy**: Pythonic abstractions but requires understanding of `Signatures`,
  `Modules`, and `Optimizers` — a distinct conceptual model.
- **LMQL**: Embeds a query language inside Python string literals via `@lmql.query`.
- **Guidance**: Hybrid DSL — you write programs mixing Python and Guidance
  grammar.
- **Marvin**: Very Pythonic; `@fn` feels like standard Python.
- **LangChain**: LCEL (LangChain Expression Language) is a pipe-based DSL
  (`chain | step1 | step2`).
- **Semantic Kernel**: .NET-native with Python bridge — the plugin/kernel model
  is foreign to Python developers.

## Learning Curve

- **`@llm` (Low)**: If you know Python decorators, you know `@llm`. The API
  surface is minimal: one decorator, a few parameters.
- **Marvin (Low)**: Similar decorator-based approach.
- **DSPy (Moderate)**: Requires understanding of signatures, modules, metrics,
  and optimizers — powerful but not trivial.
- **LMQL / Guidance (High)**: Require learning domain-specific constraint
  languages.
- **LangChain (Steep)**: LCEL, chains, agents, tools, callbacks — many
  abstractions to learn before being productive.
- **Semantic Kernel (Steep)**: .NET-first design with plugin, kernel, and
  planner abstractions.

## Structured Output Support

- **`@llm`**: Declares output type via Python return annotation. Uses
  `get_structured_computation()` (OpenAI Structured Outputs) for Pydantic models
  and string coercion for primitives.
- **Marvin / Outlines**: Best-in-class. Marvin uses Pydantic natively; Outlines
  guarantees the LLM output matches the regex/grammar.
- **DSPy**: `TypedPredictor` with Pydantic — strong but requires explicit setup.
- **LangChain**: `with_structured_output()` is a recent addition, not as seamless
  as Marvin/Outlines.
- **LMQL / Guidance**: Constraint-based generation but not Python-type-driven.

## Async Support

- **`@llm`**: The underlying `hllm` module is synchronous. Async support would
  be added in a future iteration.
- **Semantic Kernel**: Best async support — `InvokeAsync` is the primary API.
- **LangChain**: `ainvoke()`, `astream()`, etc.
- **Marvin**: Supports `async fn`.
- **Others**: Mostly synchronous.

## Ecosystem Maturity

- **`@llm` (Pre-release)**: In design phase. Not production-ready.
- **LangChain / Semantic Kernel (Production)**: Very large communities, extensive
  integrations, production battle-tested.
- **Marvin (Stable)**: Prefect-backed; stable for production use.
- **DSPy (Research)**: Active research community; used in production by some
  teams; evolving rapidly.
- **LMQL / Guidance (Research)**: Primarily research tools; limited production
  adoption.

# When to Use Each Tool

| Use Case | Best Tool | Why |
|----------|-----------|-----|
| **Rapid prototyping with LLMs** | `@llm`, Marvin | Decorator-based, minimal boilerplate |
| **Prompt optimization / automatic few-shot** | DSPy | Purpose-built for prompt optimization |
| **Constrained generation (grammar/regex)** | Outlines, LMQL | Guaranteed output structure |
| **Complex agent workflows** | LangChain, Semantic Kernel | Mature agent/tool/chaining infrastructure |
| **Pydantic-native structured output** | Marvin, Outlines | First-class Pydantic integration |
| **LLM → deterministic code evolution** | `@llm` | Unique compilation pipeline |
| **Enterprise .NET applications** | Semantic Kernel | .NET-native with Python bridge |
| **Research / experimentation** | DSPy, LMQL, Guidance | Flexible, designed for exploration |
| **Simple LLM wrappers with caching** | `@llm` | Built-in caching, cost tracking, test generation |
| **Production multi-model deployments** | LangChain | Broadest provider/model support |

# Summary

`@llm` occupies a unique niche: **LLM-as-decorator with compilation to pure
Python**. Its closest competitors are **Marvin** (decorator-based, Pydantic-native)
and **DSPy** (compilation concept, though of prompts not code).

Key differentiators of `@llm`:

1. **Compilation pipeline**: The LLM → I/O pairs → tests → pure Python function
   path is unique. No other framework generates deterministic Python code from
   LLM behavior.

2. **Integration with helpers infrastructure**: Leverages `hcache_simple`,
   `hllm_cost`, `hunit_test`, and `hdbg` — tight integration with the existing
   helpers ecosystem.

3. **Decorator-first design**: Uses Python's `inspect` to make function
   signatures dual-purpose (both runtime API and LLM prompt specification).

4. **Auto test generation**: Uses cached I/O pairs to auto-generate test classes
   following `testing.rules.md` conventions — combining LLM usage with
   deterministic testing.

Key limitations:

1. **Pre-release**: Not production-ready.
2. **Sync-only**: No async support (blocked on underlying `hllm`).
3. **OpenAI-centric**: Currently tied to OpenAI/OpenRouter providers.
4. **No prompt optimization**: Unlike DSPy, doesn't automatically optimize
   prompts — relies on user-written docstrings.

# Qualitative Positioning

```
                     Learning Curve
                     Low ← → High
                          │
               Marvin/@llm│         DSPy
          ────────────────┼───────────────
                          │
            Outlines/LMQL │    LangChain
                          │  Semantic Kernel
                          │
              Python Integration
              Native ← → Framework-bound

                     Runtime Behavior
                     LLM-driven ← → Deterministic
                          │
            LangChain/   │         @llm (compiled)
            Marvin/DSPy  │
          ───────────────┼───────────────
                          │
            LMQL/Guidance│
                          │
                          │         Outlines
                          │
              Structured Output
              Flexible ← → Guaranteed
```