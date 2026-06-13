# Plan: LLM-as-Function Decorator Library

## 1. Design the core `@llm` decorator (`helpers/hllm_decorator.py`)
- Decorator wraps a function stub (type hints + docstring = LLM prompt)
- Uses `inspect` to extract signature, types, and docstring at decoration time
- At call time: serializes args/kwargs, constructs prompt, calls `apply_llm()`, parses response to return type

- The decorator accepts a use_cache: bool = True
- Layers caching via `hcache_simple.py` (keyed on function hash + arguments)

## 2. Implement type coercion and validation
- Map Python type annotations to output parsing instructions in the LLM prompt
- After LLM response: coerce string to `int`, `float`, `bool`, `List`, `Dict`, etc.

## 3. Implement caching layer
- Integrate with `hcache_simple.simple_cache` — each decorated function auto-cached
- Cache key: hash of (function source, model, args, kwargs)
- Support `force_refresh` to bypass cache

## 4. Implement batching / vectorization
- Queue LLM calls when multiple `@llm` functions are called in sequence
- Flush batch to LLM with structured prompt for parallel returns
- Collect and dispatch results back to individual callers

## 5. Implement multi-shot prompting
- Allow user to register example input/output pairs via decorator param: `@llm(examples=[...])`
- Inject examples into the system prompt to guide LLM behavior

## 6. Implement tool-use (LLM calls Python)
- Register callable Python functions as tools the LLM can invoke
- Parse LLM tool-call requests, execute them, feed results back

## 7. Implement compilation (`@llm.compile()`)
- Record all LLM calls for a function
- Generate a pure Python function from the cached I/O pairs (e.g., via fine-tuning or rule extraction)

## 8. Implement unit test auto-generation
- `@llm` decorator auto-generates test class with input/output pairs
- Uses the caching layer's recorded calls as test fixtures

## 9. Create comparison matrix with alternatives
- Compare against: DSPy, LMQL, Guidance, Marvin, Outlines, LangChain LCEL, Semantic Kernel
- Dimensions: type safety, caching, batching, tool use, compilation, Python integration, learning curve

## 10. Write unit tests
- Follow `testing.rules.md` conventions
- Test each component: decorator, type coercion, caching, batching, multi-shot, tool use
