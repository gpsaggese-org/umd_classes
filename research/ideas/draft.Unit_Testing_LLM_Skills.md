# Unit Testing LLM Skills

## Description

- Design a framework for writing unit tests for LLM skills (prompt-based agents),
  analogous to how pytest tests Python functions
- Define what "correct behavior" means for a skill: exact output match, semantic
  equivalence, structural constraints (e.g., output must be valid JSON), or
  behavioral invariants
- Build a test runner that executes a skill against a set of input fixtures and
  evaluates outputs against expected results using both rule-based and
  LLM-as-judge checks
- Investigate snapshot testing for LLM outputs: store a "golden" output and flag
  when outputs drift beyond a threshold
- Research property-based testing for skills: instead of fixed examples, generate
  inputs that probe boundary conditions (empty input, very long input,
  adversarial prompts)
- Explore how to isolate skills from external dependencies (API calls, file
  system) in tests, analogous to mocking in traditional unit tests

## Project Objective

The goal is to build a testing framework — `skilltest` or similar — that lets
developers write deterministic, repeatable unit tests for LLM skills, enabling
CI/CD pipelines to catch skill regressions before deployment, just as pytest
catches code regressions.

## Dataset Suggestions

1. **PromptBench**
   - Source: Microsoft Research
   - URL: https://github.com/microsoft/promptbench
   - Content: Adversarial prompt benchmarks for robustness testing across NLP
     tasks
   - Access: Public GitHub repository

2. **HELM (Holistic Evaluation of Language Models)**
   - Source: Stanford CRFM
   - URL: https://crfm.stanford.edu/helm/
   - Content: Standardized scenarios and metrics for LLM evaluation
   - Access: Public, full benchmark suite available

3. **BIG-Bench**
   - Source: Google
   - URL: https://github.com/google/BIG-bench
   - Content: 200+ diverse tasks for probing LLM capabilities, usable as skill
     test fixtures
   - Access: Public GitHub repository

## Related Work

- LangChain evaluation module: basic input/output evaluation for chains
- DeepEval: pytest-style LLM evaluation framework
- Promptfoo: CLI tool for testing and comparing prompts
- Evals (OpenAI): framework for evaluating LLM outputs against rubrics

## Open Questions

- What is the minimal set of assertions needed to declare a skill "passing"?
- How do you handle the non-determinism of LLM outputs in a deterministic test
  suite?
- Should tests use a cheap fast model for CI and the real model for pre-release?
- How do you version skill tests alongside skill prompts?
