---
title: "Programming by Mixing Python and LLM calls"
draft: true
authors:
    - gpsaggese
date: 2026-06-13
description:
categories:
    - LLM
    - Python
---

TL;DR The `@llm` decorator transforms a Python function stub into an LLM call
automatically, using type hints and docstrings as the prompt specification

<!-- more -->

# Introduction

## What Is `@llm`?

- The `@llm` decorator turns a Python function stub into a call to an LLM
- You write a standard Python function with:
    - A docstring describing what the function should do
    - Type annotations for inputs and the return type
- The decorator replaces the function body with an LLM
    - Builds a prompt from the docstring and call arguments
    - Sends the prompt to an LLM via
      [`helpers/hllm.py`](https://github.com/causify-ai/helpers/blob/master/helpers/hllm.py)
    - Coerces the LLM response to match the declared return type
- The result is a function that _looks_ and _behaves_ like regular Python code
  but is backed by an LLM at runtime

## Examples

// TODO(ai_gp): This is not an interesting one. Come up with 2-3 more interesting
// examples.
- A minimal example:

    ```python
    import helpers.hllm_decorator as hllmdec

    @hllmdec.llm()
    def summarize(text: str) -> str:
        """
        Summarize the given text in one sentence.
        """

    result = summarize("Long article about distributed systems...")
    # Returns: "The article covers key distributed systems concepts..."
    ```

## When To Use `@llm`

- `@llm` is a good fit when:
    - **You are prototyping rapidly**: Replace placeholder implementations with
      real LLM behavior in seconds without writing prompts by hand
    - **Path from LLM to code**: Incrementally convert code from LLM prompts
      into code to turn prototypes into production systems
    - **You need caching for free**: Every LLM call is automatically cached to
      disk, saving cost during development and testing
    - **You want testable LLM code**: The built-in `mock_apply_llm()` function
      lets tests inject expected responses without hitting an API
    - **You have many small, typed LLM tasks**: Classification, extraction,
      summarization: each becomes a single decorated function
    - **You work within the helpers ecosystem**: `@llm` integrates with
      `hcache_simple`, `hllm_cost`, and `hunit_test`
    - **Robust conversion from and to LLM**

## When NOT To Use `@llm`

- Use a different approach when:
    - **You need complex agentic workflows**: Multi-step tool use, ReAct loops,
      or branching chains are better served by LangChain or raw API calls
    - **You require streaming responses**: `@llm` waits for the full completion
      before returning
    - **You need guaranteed structured output**: For production-grade structured
      output, consider Marvin or Outlines which constrain generation at the
      token level
    - **You want prompt optimization**: DSPy automatically tunes prompts; `@llm`
      uses your docstring verbatim

# How It Works

- The decorator operates in four stages:
    1. **Decoration time**: When Python loads your module, `@llm()`:
        - Extracts the function signature and type hints via `inspect`
        - Computes a hash of the function source for cache invalidation
        - Wraps the internal LLM call with `@simple_cache` from `hcache_simple`

    2. **Call time**: When you invoke the decorated function:
        - Arguments are bound to the function signature
        - A prompt is built from the docstring and argument values
        - A format instruction is appended based on the return type

    3. **LLM execution**: The prompt is sent to the LLM:
        - If caching is enabled, identical calls return cached responses
        - The raw text response is returned

    4. **Coercion**: The raw response is parsed into the declared return type:
        - `int`, `float`, `bool`, `str` are extracted via regex
        - `List[T]` and `Dict[K,V]` are parsed as JSON arrays and objects
        - `Optional[T]` handles `null` responses gracefully

- The prompt built for a function call looks like:

    ```verbatim
    Summarize the given text in one sentence.

    Input:
      text = 'Long article about distributed systems...'

    Return ONLY the requested string value, no extra commentary.
    ```

- The complete flow is summarized below:

    ```mermaid
    flowchart TD
        A[Function Call] --> B[Bind Arguments]
        B --> C[Build Prompt from Docstring + Args]
        C --> D{Cache Hit?}
        D -->|Yes| E[Return Cached Response]
        D -->|No| F[Call LLM via hllm.get_completion]
        F --> G[Cache Raw Response]
        G --> H[Coerce Response to Return Type]
        E --> H
        H --> I[Return Typed Value]
    ```

# Real-World Scenarios

## Scenario 1: Text Classification

- Instead of training a classifier, define the task as a typed function:

    ```python
    @hllmdec.llm(model="gpt-4o-mini")
    def classify_sentiment(review: str) -> str:
        """
        Classify the product review sentiment as POSITIVE, NEGATIVE,
        or NEUTRAL. Return only the label.
        """

    sentiment = classify_sentiment(
        "The build quality is solid but the battery drains too fast."
    )
    # Returns: "NEUTRAL"
    ```

## Scenario 2: Structured Data Extraction

- Use `List` and `Dict` return types to extract structured data:

    ```python
    from typing import List, Dict

    @hllmdec.llm(model="gpt-4o")
    def extract_entities(paragraph: str) -> List[Dict[str, str]]:
        """
        Extract all named entities from the paragraph. For each entity,
        return a JSON object with 'name', 'type', and 'description' keys.
        Return a JSON array of these objects.
        """

    entities = extract_entities(
        "Apple Inc. announced that Tim Cook will speak at WWDC in Cupertino."
    )
    # Returns: [
    #   {"name": "Apple Inc.", "type": "Organization", "description": "..."},
    #   {"name": "Tim Cook", "type": "Person", "description": "..."},
    #   ...
    # ]
    ```

## Scenario 3: Unit Testing with Mock Responses

- `mock_apply_llm()` lets you inject expected LLM responses without API calls:

    ```python
    import helpers.hllm_decorator as hllmdec

    @hllmdec.llm()
    def add(a: int, b: int) -> int:
        """Add two integers."""

    # In your test:
    hllmdec.mock_apply_llm(add, args=(2, 3), response=5)
    assert add(2, 3) == 5  # Returns 5 without any LLM call
    ```

- Benefits for testing:
    - Tests run offline and deterministically
    - No API costs during CI runs
    - You control exactly what the LLM "returns" for each test case

# Advanced Features

## Caching and Cache Control

- The decorator integrates with
  [`helpers/hcache_simple.py`](https://github.com/causify-ai/helpers/blob/master/helpers/hcache_simple.py)
  for on-disk caching
- Cache behavior:
    - **Default**: Responses are cached to disk with write-through semantics
    - **Cache key**: Hash of function source code, model name, and call
      arguments
    - **Force refresh**: Pass `force_refresh=True` to bypass cache for a
      specific call:

        ```python
        result = summarize(text, force_refresh=True)  # Always calls the LLM
        ```

    - **Disable caching**: Pass `use_cache=False` to the decorator:

        ```python
        @hllmdec.llm(use_cache=False)
        def no_cache_summarize(text: str) -> str:
            """Summarize text."""
        ```

## Type Coercion System

- The decorator parses LLM text responses into the declared Python return type:

// TODO(ai_gp): Use two columns "Input" and "Output"

| Return Type   | Coercion Strategy                 | Example Response             |
| :------------ | :-------------------------------- | :--------------------------- |
| `str`         | Return raw text as-is             | `"Hello world"`              |
| `int`         | Extract digits, strip non-numeric | `"The answer is 42"` -> `42` |
| `float`       | Extract numeric with decimal      | `"3.14 is pi"` -> `3.14`     |
| `bool`        | Match true/false/yes/no/1/0       | `"true"` -> `True`           |
| `List[T]`     | Extract and parse JSON array      | `"[1, 2, 3]"` -> `[1, 2, 3]` |
| `Dict[K,V]`   | Extract and parse JSON object     | `"{\"a\": 1}"` -> `{"a": 1}` |
| `Optional[T]` | Handle `null` or missing values   | `"null"` -> `None`           |

- The coercer can be forgiving or stricts: it extracts JSON from surrounding text
  and strips noise before parsing

## Source-Change Detection

- The decorator computes a hash of the function's source code at decoration time
- When the function body or model changes, the cache key changes, so:
    - Old cached responses are automatically invalidated
    - New calls generate fresh LLM responses

## Custom LLM Parameters

- All parameters are configurable at decoration time:

    ```python
    @hllmdec.llm(
        model="gpt-4o",
        system_prompt="You are a helpful data analyst.",
        temperature=0.3,
        use_cache=True,
    )
    def analyze_data(query: str) -> str:
        """Analyze the data based on the query."""
    ```

- Parameters:
    - `model`: LLM model name (empty for default, e.g., `"gpt-4o-mini"`)
    - `system_prompt`: System-level instruction for the LLM
    - `temperature`: Sampling temperature for response variability
    - `use_cache`: Enable or disable disk caching

## Introspection and Metadata

- Each decorated function carries metadata for tooling and debugging:

    ```python
    config = summarize._llm_decorator_config
    # {
    #     "use_cache": True,
    #     "model": "",
    #     "temperature": 0.1,
    #     "system_prompt": "",
    #     "return_type": <class 'str'>,
    #     "func_source_hash": "a1b2c3d4...",
    #     "cache_func_name": "_llm_call_summarize",
    # }
    ```

- The original function is available via `wrapper._llm_decorator_original_func`

# Comparison with Alternatives

- `@llm` occupies a distinct niche among LLM-calling libraries:

| Library   | Style            | Caching         | Type Coercion            | Best For                        |
| :-------- | :--------------- | :-------------- | :----------------------- | :------------------------------ |
| `@llm`    | Decorator        | Built-in (disk) | Runtime string parsing   | Prototyping, simple typed calls |
| Marvin    | Decorator        | None            | Pydantic-native          | Structured output               |
| DSPy      | Signatures       | Compiler cache  | `TypedPredictor`         | Prompt optimization             |
| LangChain | Chain syntax     | Optional        | `with_structured_output` | Complex agent workflows         |
| Outlines  | Generation model | None            | Regex/grammar-guaranteed | Constrained generation          |

- `@llm` is the right choice when:
    - You want a zero-boilerplate decorator with type coercion
    - You need automatic disk caching without extra setup
    - You work within the helpers Python ecosystem
    - You want testable LLM code with mock injection

# References

- Source code:
    - [`helpers/hllm_decorator.py`](https://github.com/causify-ai/helpers/blob/master/helpers/hllm_decorator.py):
      The core `@llm` decorator implementation
    - [`helpers/hllm.py`](https://github.com/causify-ai/helpers/blob/master/helpers/hllm.py):
      Underlying LLM completion interface
    - [`helpers/hcache_simple.py`](https://github.com/causify-ai/helpers/blob/master/helpers/hcache_simple.py):
      Caching layer used by `@llm`
- Documentation:
    - [`docs/tools/helpers/all.hllm.explanation.md`](https://github.com/causify-ai/helpers/blob/master/docs/tools/helpers/all.hllm.explanation.md):
      Detailed explanation of the `hllm` module
- Tutorials:
    - [`notebooks/hllm.tutorial.ipynb`](https://github.com/causify-ai/helpers/blob/master/helpers/notebooks/hllm.tutorial.ipynb):
      Jupyter notebook with `hllm` usage examples
