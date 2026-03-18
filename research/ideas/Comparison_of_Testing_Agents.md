# Comparison of AI Testing Agents

## Description

- **AI Testing Agents** are autonomous systems that generate, maintain, and validate
  unit, integration, and end-to-end tests with minimal manual intervention
- They span from lightweight test generators (e.g., `pytest-codemod` with LLM
  backends, `Copilot for Tests`) to full autonomous test orchestration platforms
  (e.g., `Diffblue Cover`, `Symflower`)
- Key capabilities include test case generation from code, test maintenance when
  code evolves, flaky test detection, coverage optimization, and intelligent test
  data generation
- Agents differ in test type coverage (unit vs. integration), reproducibility
  across codebases, ability to detect and fix failing tests, and integration with
  CI/CD pipelines
- Most tools expose Python SDKs or CLI interfaces, making them accessible in
  standard test environments (pytest, unittest, Jest, etc.)
- This project teaches students to rigorously benchmark testing tools rather than
  relying on vendor marketing claims—good tests are hard to measure, and false
  claims about coverage can mask real gaps

## Comparison of Testing Agents

| Type             | Name                       | Description                                                                              | Website                                         | Strength                    |
| ---------------- | -------------------------- | ---------------------------------------------------------------------------------------- | ----------------------------------------------- | --------------------------- |
| Code-based       | Diffblue Cover             | AI-powered unit test generation for Java and C# with automatic coverage optimization     | https://www.diffblue.com/cover                  | High coverage, production   |
| LLM-assisted     | GitHub Copilot for Tests   | IDE-integrated test generation via natural language prompts                              | https://github.com/features/copilot             | Developer-friendly          |
| Open-source      | TestMe (IntelliJ)          | IDE plugin that generates unit tests using AST analysis and heuristics                   | https://plugins.jetbrains.com/plugin/9471-testme | Local, lightweight          |
| Specialized      | Symflower                  | Autonomous test generation for any programming language using symbolic execution         | https://www.symflower.com                       | Language-agnostic           |
| CLI-based        | Mintlify Test Generator    | API-based test generation from docstrings and type hints                                 | https://www.mintlify.com                        | Documentation-driven        |
| Framework        | pytest-codemod + LLM       | Open-source pytest refactoring with LLM-powered test suggestions                        | https://github.com/asottile/pyupgrade           | Highly customizable         |

## Autonomy Levels for Testing

| Level                   | Capability                      | Example behaviors                                |
| ----------------------- | ------------------------------- | ------------------------------------------------ |
| L0 -- Suggest           | Suggest next test case          | IDE autocomplete for assertions                  |
| L1 -- Generate one test | Generate a single test method   | "Generate test for this function"                |
| L2 -- Generate suite    | Generate full test class        | Auto-generate 5+ test cases for a class          |
| L3 -- Maintain          | Update tests when code changes  | Refactor test suite after API change             |
| L4 -- Autonomous tester | Plan test strategy, fix failures | Achieve target coverage, detect flaky tests      |

## Project Objective

Design a controlled empirical study that benchmarks at least three AI testing
agents across multiple Python codebases of varying complexity. The project aims
to answer: _Which agents produce the most reliable tests, highest coverage, and
most maintainable test code — and under what conditions?_ Students will select
agents from different categories (code-based, LLM-assisted, framework-based),
apply each to the same set of functions and classes, and systematically compare
test coverage achieved, pass@1 (tests pass without modification), readability and
maintainability of generated tests, and cost/time to generate.

## Tasks

- **Agent Setup & Configuration**: Install and configure at least three chosen
  testing agents (e.g., Diffblue Cover, GitHub Copilot for Tests, Symflower) in
  isolated environments; document version pinning, dependencies, and cost (cloud
  API calls vs. local execution)

- **Test Generation on Benchmark Functions**: Select 10–15 Python functions of
  varying complexity (simple getters, complex logic, edge case handling,
  concurrency) and run each agent to generate test suites; record: number of test
  cases generated, lines of test code, execution time, and whether tests execute
  without error (pass@1)

- **Coverage Comparison**: Measure code coverage (branch, line, path coverage)
  achieved by each agent's test suite using `coverage.py`; compare coverage depth
  and identify which agent produces the most thorough tests

- **Test Maintainability & Flakiness**: Intentionally modify source code (change
  function behavior, add edge cases, refactor) and measure how well each agent's
  tests: (a) catch the regression, (b) require modification to pass, (c) avoid
  flaky assertions (e.g., time-dependent checks, random output)

- **Code Quality Review**: Examine the generated test code for: readability
  (naming, structure), modularity (DRY principle, helper functions), presence of
  comments/docstrings, and whether tests can be debugged or modified by humans
  independently of the agent

- **Comparative Scorecard**: Build a rubric that weights coverage, pass@1,
  readability, maintainability, and runtime; score each agent and discuss
  trade-offs (e.g., higher coverage at cost of unreadable tests)

## Test Functions & Benchmark Suite

- **Simple functions** (edge case detection)
  - `extract_email_from_text(text: str) -> str | None`
  - `parse_date_string(date_str: str) -> datetime | None`
  - `clamp(value: float, min_val: float, max_val: float) -> float`

- **Complex logic** (branching, loops)
  - `calculate_shipping_cost(weight: float, zone: int, expedited: bool) -> float`
  - `merge_sorted_lists(list1: List[int], list2: List[int]) -> List[int]`
  - `validate_credit_card(card_number: str) -> bool`

- **Data structure operations** (mutation, invariants)
  - `insert_in_sorted_array(arr: List[int], value: int) -> List[int]`
  - `remove_duplicates(items: List[str]) -> List[str]`
  - Class: `LRUCache` with `get()`, `put()`, `evict()`

- **Concurrent / stateful code**
  - `thread_safe_counter` class with increment/decrement
  - `async_fetch_and_cache(url: str) -> str`

## Bonus Ideas

- **Mutation Testing**: Use a mutation testing framework (e.g., `mutmut` for
  Python) to inject bugs into source code and measure whether each agent's test
  suite detects the mutation; rank agents by mutation kill rate

- **Flaky Test Detection**: Run each agent's generated tests 10+ times and measure
  flakiness rate (percentage of tests that fail intermittently); document which
  agents produce deterministic vs. non-deterministic tests

- **Integration Test Generation**: Challenge each agent to generate integration
  tests that span multiple functions/classes; evaluate correctness and complexity
  of generated integration scenarios

- **Test Readability Scoring**: Use an LLM-as-judge to score test code quality
  (clarity, naming conventions, documentation) independent of coverage metrics

- **Maintenance Simulation**: Create a version of the codebase 6-12 months into
  development (with refactoring, API changes, new features); measure which
  agent's test suite requires the least modification to remain valid

- **Cost & Performance Analysis**: If cloud-based agents are included, estimate
  API call costs and wall-clock time to generate test suites; discuss ROI of
  automated testing vs. manual test authoring

## Useful Resources

- **Diffblue Cover Documentation**: https://docs.diffblue.com
- **GitHub Copilot API & Examples**: https://docs.github.com/en/copilot/quickstart
- **pytest Documentation**: https://docs.pytest.org
- **Coverage.py**: https://coverage.readthedocs.io
- **mutmut (Mutation Testing)**: https://mutmut.readthedocs.io
- **OpenML Test Suites**: Real benchmark datasets for algorithm evaluation: https://www.openml.org
- **LeetCode / HackerRank**: Curated coding problems with reference solutions for testing agent evaluation
