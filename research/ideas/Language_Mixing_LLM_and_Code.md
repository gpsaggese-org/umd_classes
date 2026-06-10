# A Language for Mixing LLM and Code

## Description

- Design a programming language or DSL where LLM calls and deterministic code are
  first-class citizens that interleave naturally, rather than LLMs being called
  via awkward API wrappers
- Formalize the semantics of LLM-as-interpolator: given a structured input and
  output type, the LLM fills in the gap between them, analogous to function
  application but with learned rather than programmed behavior
- Build a type system that tracks which values are "LLM-produced" (uncertain,
  non-deterministic) vs "code-produced" (deterministic), enabling static analysis
  of program reliability
- Investigate syntax designs: inline LLM blocks in Python-like syntax (e.g.,
  `result = llm(prompt, input, output_type)`), or a fully new language with
  native `ask` / `infer` / `generate` keywords
- Research compilation strategies: LLM calls can be cached, batched, retried, or
  replaced with fine-tuned models — the compiler manages this transparently
- Explore how the interpolator view of LLMs (they interpolate between training
  examples) shapes language design: what operations are safe to delegate to
  interpolation vs requiring deterministic code?

## Project Objective

The goal is to design and prototype a language where mixing LLM inference and
deterministic computation is as natural as mixing functions and data structures
in Python, with a type system that makes the uncertainty boundary explicit and a
runtime that optimizes LLM call execution.

## Dataset Suggestions

1. **DSPy Programs Corpus**
   - Source: Stanford NLP / DSPy community
   - URL: https://github.com/stanfordnlp/dspy
   - Content: Real programs that mix LLM modules and Python code; useful as
     design inspiration and evaluation corpus
   - Access: Public GitHub repository

2. **LCEL (LangChain Expression Language) Pipelines**
   - Source: LangChain
   - URL: https://python.langchain.com/docs/expression_language/
   - Content: Examples of chaining LLM calls with tools, parsers, and code in a
     compositional style
   - Access: Public documentation and GitHub examples

3. **Semantic Kernel Programs**
   - Source: Microsoft
   - URL: https://github.com/microsoft/semantic-kernel
   - Content: Programs mixing "semantic functions" (LLM) and "native functions"
     (code) in a shared kernel
   - Access: Public GitHub repository

## Related Work

- DSPy: Python-embedded LLM programming with module composition and compilation
- LMQL (Beurer-Kellner et al., 2022): query language for LLMs with constraints
  and control flow
- Guidance (Microsoft, 2023): language for constraining and interleaving LLM
  generation with code
- Marvin: Python library for LLM-as-function with type annotations
- Outlines: structured generation library treating LLM as typed function

## Open Questions

- What is the right abstraction boundary between the LLM and the surrounding
  program?
- How do you handle LLM non-determinism in a language with referential
  transparency?
- Can a compiler statically bound the cost (tokens, latency) of an LLM-mixed
  program?
- Is the interpolator framing (LLMs generalize between training points) useful
  for formal semantics?
