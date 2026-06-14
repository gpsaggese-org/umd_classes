# Comparison of AI Code Refactoring Agents

## Description

- **AI Refactoring Agents** are systems that automatically improve code quality by
  eliminating duplication, reducing cyclomatic complexity, improving variable
  naming, restructuring modules, and applying design patterns with minimal manual
  intervention
- They range from rule-based linters with AI enhancement (e.g., `pylint` + LLM
  backends, `Semgrep` with explanations) to full autonomous refactoring engines
  (e.g., `Cognition AI's Devin`, `Copilot refactoring`, `Tuple`—experimental
  Databricks tools)
- Key capabilities include identifying code smells (dead code, long methods,
  complex conditionals), suggesting refactoring operations (extract method,
  consolidate duplicates, rename for clarity, replace magic numbers), estimating
  refactoring impact (will tests still pass?), preserving behavior (all tests
  pass after refactoring), and explaining rationale for changes in natural
  language
- Agents differ in refactoring ambition (cosmetic cleanup vs. architectural
  redesign), safety (does refactored code have identical behavior?), code review
  compatibility (can humans easily understand and approve the changes?), and
  runtime performance impact (does refactoring improve efficiency?)
- This project develops critical skills in measuring non-functional code quality
  improvements and trade-offs—good refactoring is hard to measure and easy to get
  wrong

## Comparison of Refactoring Agents

| Type             | Name              | Description                                                                            | Website                                | Strength                      |
| ---------------- | ----------------- | -------------------------------------------------------------------------------------- | -------------------------------------- | ----------------------------- |
| IDE-integrated   | GitHub Copilot    | AI-powered refactoring suggestions within IDEs with one-click application               | https://github.com/features/copilot    | Seamless workflow             |
| Rule-based + LLM | Semgrep           | Static analysis with LLM-powered explanations and automated fix suggestions            | https://semgrep.dev                    | Rule-driven precision         |
| Autonomous agent | Devin             | Fully autonomous refactoring, including complex multi-file restructuring                | https://cognition.ai                   | End-to-end transformation     |
| Specialized tool | Rope (Python)     | Python refactoring library with AST-based transformations, LLM-enhanced discovery      | https://github.com/python-rope/rope    | Language-specific safety      |
| IDE tool         | Cursor            | AI IDE with refactoring suggestions and one-click application                          | https://www.cursor.com                 | Integrated debugging          |
| Experimental     | Tuple (Databricks)| Experimental multi-agent system for code improvement and refactoring                   | https://databricks.com                 | Research-grade autonomy       |

## Refactoring Agent Capabilities

| Level                      | Capability                    | Example behaviors                                          |
| -------------------------- | ----------------------------- | ---------------------------------------------------------- |
| L0 -- Suggest              | Highlight code smells         | "This method is 150 lines, consider extracting"            |
| L1 -- Suggest fix           | Propose a single refactoring  | "Extract method `_validate_input()` from line 20–45"       |
| L2 -- Apply refactoring     | Execute refactoring operation | Automatically rename variable `x` → `user_id` across file  |
| L3 -- Multi-file refactoring| Coordinate refactoring across files | Consolidate duplicate classes into shared base class        |
| L4 -- Autonomous redesign   | Plan & execute architectural changes | Redesign module structure, move classes to new files        |

## Project Objective

Design a controlled empirical study that benchmarks at least three AI refactoring
agents on a curated set of Python codebases with intentional quality issues. The
project aims to answer: _Which agents identify the most impactful refactoring
opportunities, execute them safely (tests still pass), produce readable changes,
and improve code quality metrics?_ Students will select agents from different
categories (IDE, rule-based, autonomous), apply each to the same set of
codebases, and systematically compare: code smell detection accuracy, correctness
of refactoring (behavior preservation), code quality improvements (measured by
cyclomatic complexity, duplication, maintainability index), review-ability of
generated changes, and performance impact.

## Tasks

- **Agent Setup & Configuration**: Install and configure at least three chosen
  refactoring agents (e.g., GitHub Copilot, Semgrep, Devin/Cursor) in isolated
  environments; document version, dependencies, and cost/API limits

- **Codebase Selection & Baseline**: Select 3–5 Python codebases with known
  quality issues (high complexity, duplication, poor naming); measure baseline
  metrics: cyclomatic complexity, code duplication ratio (via `radon`, `pylint`,
  `SonarQube`), maintainability index (via `lizard`, `mi`), lines of code,
  number of violations

- **Code Smell Detection**: For each agent, identify and document all code smells
  detected (long methods, high complexity, duplication, dead code, unclear
  naming); measure: (a) sensitivity (did agent find real smells?), (b)
  specificity (how many false positives?)

- **Refactoring Suggestion & Execution**: For each detected code smell, have the
  agent suggest and apply a refactoring; record: (a) type of refactoring
  (extract method, rename, consolidate, etc.), (b) lines of code changed, (c)
  number of files affected

- **Behavior Preservation Testing**: After each refactoring, run the full test
  suite; measure: (a) do all tests pass? (b) are there any new test failures
  (regressions)? (c) does performance degrade (runtime, memory)?

- **Code Quality Metrics**: After refactoring, re-measure code quality metrics;
  calculate improvement in: cyclomatic complexity, duplication ratio,
  maintainability index, readability (using `readability` libraries)

- **Change Review-ability**: Assess how easy the refactored code is to review:
  (a) are changes logical and incremental? (b) can a human understand the intent
  without seeing the original code? (c) are there unnecessary changes?

- **Correctness of Reasoning**: For each refactoring, extract agent's explanation
  of why the change improves code quality; score on technical accuracy and
  clarity

- **Comparative Scorecard**: Build a rubric weighing: code smell detection
  accuracy, refactoring correctness, quality improvement, change review-ability,
  and performance impact; rank agents and identify specialization

## Codebase Selection Strategies

### Create Intentional Quality Issues

- **Method Too Long** (>50 lines, multiple concerns)
  ```python
  def process_user_data(user_input):
      # Validation logic (10 lines)
      # Database query (5 lines)
      # Data transformation (15 lines)
      # Email notification (10 lines)
      # Logging (5 lines)
      # Ideal refactoring: extract into _validate(), _transform(), _notify_user(), etc.
  ```

- **Code Duplication** (same logic in multiple functions)
  ```python
  def validate_email(email): ...
  def validate_email_v2(email): ...  # Almost identical
  # Ideal refactoring: consolidate to single function
  ```

- **High Cyclomatic Complexity** (deeply nested conditionals)
  ```python
  def check_access(user, resource, action):
      if user is not None:
          if user.is_active:
              if user.has_role('admin'):
                  return True
              elif user.has_role('editor'):
                  if resource.is_editable:
                      return True
      return False
      # Ideal refactoring: guard clauses, extract logic
  ```

- **Poor Naming** (unclear variable names)
  ```python
  def f(x, y):
      z = x * 0.15
      return y - z
      # Ideal refactoring: rename to calculate_discount(), apply_tax(), etc.
  ```

- **Dead Code** (unused imports, variables, functions)
  ```python
  import unused_module  # Ideal: remove
  def old_function():  # Ideal: remove or deprecate
      pass
  ```

### Use Real Codebases

- **Small open-source projects** with known issues:
  - https://github.com/pallets/click (CLI framework)
  - https://github.com/psf/requests (HTTP client)
  - https://github.com/encode/httpx
  - Typically 5k–20k lines, well-tested, moderate complexity

## Code Quality Metrics & Tools

| Metric                   | Tool               | Description                                     | Good Target |
| ------------------------ | ------------------ | ----------------------------------------------- | ----------- |
| Cyclomatic Complexity    | `radon cc`         | Number of decision points; lower is better      | < 10        |
| Maintainability Index    | `radon mi`         | Composite metric based on complexity, LOC       | > 80        |
| Code Duplication         | `pylint` `dupdup`  | Percentage of duplicated code; lower is better  | < 5%        |
| Lines of Code (per func) | `radon metrics`    | Average function length; lower is better        | < 30 LOC    |
| Code Coverage           | `coverage.py`      | % of code executed by tests; higher is better   | > 80%       |

## Bonus Ideas

- **Refactoring Impact Analysis**: For each refactoring, measure impact on:
  performance (runtime, memory), test execution time, build time, deployment risk

- **Multi-Layer Refactoring**: Create codebases with issues spanning multiple
  layers (API → business logic → database) and measure which agents can identify
  and refactor across layers

- **Style Guide Conformance**: Test whether refactorings maintain project style
  (indentation, naming conventions, code organization) or introduce inconsistency

- **Incremental Refactoring**: Measure which agents prefer small, incremental
  refactorings (easier to review) vs. large rewrites (higher risk but more impact)

- **Performance Optimization**: Introduce intentionally slow code (O(n²) algorithm,
  inefficient data structures) and measure whether agents detect and optimize

- **Architectural Patterns**: Test whether agents can refactor code to follow
  design patterns (Factory, Observer, Strategy) without changing behavior

- **Automated Refactoring Chains**: Test whether agents can chain multiple
  refactorings (e.g., extract method → introduce strategy pattern → consolidate
  classes)

- **Rollback Analysis**: Introduce refactorings, break functionality, and measure
  which agents can diagnose and revert the issue

## Useful Resources

- **Code Quality Tools**:
  - `radon`: Cyclomatic complexity & maintainability index: https://radon.readthedocs.io
  - `pylint`: Code analysis for Python: https://pylint.pycqa.org
  - `SonarQube`: Full code quality platform: https://www.sonarqube.org
  - `Code Climate`: Web-based quality metrics: https://codeclimate.com

- **Refactoring Reference**:
  - *Refactoring* by Martin Fowler: https://refactoring.com
  - Refactoring Guru Patterns: https://refactoring.guru/refactoring

- **AST & Code Transformation**:
  - `libcst` (Concrete Syntax Tree for Python): https://github.com/Instagram/LibCST
  - `ast` (Python's Abstract Syntax Tree): https://docs.python.org/3/library/ast.html
  - `tree-sitter` (Language-agnostic parser): https://tree-sitter.github.io

- **Agent Resources**:
  - GitHub Copilot API: https://docs.github.com/en/copilot/quickstart
  - Semgrep Documentation: https://semgrep.dev/docs
  - Devin/Cursor Documentation: https://docs.cognition.ai

- **Testing & Behavior Preservation**:
  - pytest: https://docs.pytest.org
  - `coverage.py`: https://coverage.readthedocs.io
  - `pytest-benchmark`: Performance testing: https://pytest-benchmark.readthedocs.io
