# Comparison of AI Code Debugging Agents

## Description

- **AI Debugging Agents** are tools that automatically diagnose root causes of
  software failures, suggest fixes, and explain error patterns with minimal human
  intervention
- They range from lightweight error message analyzers (e.g., `GitHub Copilot
  Diagnostics`, IDE integrations) to full autonomous debugging environments
  (e.g., `Devin`, `OpenDevin`, `Cursor`)
- Key capabilities include stack trace interpretation, root cause localization
  across multiple files, hypothesis generation for bug fixes, code patch
  suggestion, reproduction of failure conditions, and explanation of failure
  modes in natural language
- Agents differ in inference latency, accuracy of root cause pinpointing (does it
  identify the correct file/line?), quality of proposed fixes (do fixes actually
  work without side effects?), explainability of debugging reasoning, and ability
  to handle complex bugs spanning multiple layers (UI, backend, database)
- This project develops critical skills in evaluating AI for safety-critical
  tasks where incorrect debugging suggestions could mask real problems or
  introduce new bugs

## Comparison of Debugging Agents

| Type             | Name               | Description                                                                           | Website                              | Strength                      |
| ---------------- | ------------------ | ------------------------------------------------------------------------------------- | ------------------------------------ | ----------------------------- |
| IDE-integrated   | GitHub Copilot     | AI-powered code completion and diagnostics for debugging within IDEs                  | https://github.com/features/copilot  | Developer workflow integration |
| Autonomous agent | Devin              | Fully autonomous software engineer that debugs, tests, and iterates on bug fixes      | https://cognition.ai                 | End-to-end debugging          |
| Open-source      | OpenDevin          | Open alternative to Devin with debugging, planning, and code execution capabilities   | https://github.com/OpenDevin/OpenDevin | Customizable, transparent     |
| IDE tool         | Cursor             | IDE with integrated AI assistant for debugging and code improvement                   | https://www.cursor.com               | Seamless editor integration   |
| Static analysis  | Semgrep + LLM      | Rule-based bug detection enhanced with LLM explanations and fix suggestions           | https://semgrep.dev                  | Pattern-based reliability     |
| Specialized      | Tabnine Debugger   | LLM-powered debugging suggestions in development environments                         | https://www.tabnine.com              | Fast, lightweight             |

## Debugging Agent Capabilities

| Level                       | Capability                         | Example behaviors                                     |
| --------------------------- | ---------------------------------- | ----------------------------------------------------- |
| L0 -- Suggest cause         | Suggest likely root cause          | "Undefined variable on line 42"                       |
| L1 -- Propose fix           | Generate a patch                   | "Add null check before accessing property"            |
| L2 -- Localize & explain    | Trace root cause across files      | "Variable mutated at line 20, leading to crash at 50" |
| L3 -- Test & validate       | Verify fix works without regressions | Apply fix, run tests, measure performance impact     |
| L4 -- Autonomous debugging  | Reproduce, debug, fix, test        | Find and ship bug fix end-to-end                      |

## Project Objective

Design a controlled empirical study that benchmarks at least three AI debugging
agents on a curated dataset of real and synthetic bugs. The project aims to
answer: _Which agents accurately pinpoint root causes, propose working fixes, and
explain failures in a way developers can understand?_ Students will create a bug
benchmark (intentionally seeded bugs + real bugs from open-source projects),
apply each agent to reproduce and fix the bugs, and systematically compare: root
cause localization accuracy, correctness of proposed fixes, explanation quality,
and false positive rate (flagging non-existent bugs).

## Tasks

- **Bug Benchmark Creation**: Curate or seed 20–30 reproducible bugs with known
  fixes, covering multiple categories (logic errors, boundary conditions,
  concurrency, memory, API misuse, performance); document expected root cause,
  impact severity, and correct fix for each bug

- **Agent Setup & Execution**: Install and configure at least three debugging
  agents (e.g., Devin, OpenDevin, Cursor); run each agent with a bug reproduction
  script/test case and error message; record: time to identify root cause,
  proposed fix, and any partial or incorrect suggestions

- **Root Cause Accuracy**: For each bug, measure whether the agent correctly
  identified: (a) the file containing the bug, (b) the function/method, (c) the
  line number or code expression, and (d) the root cause category (logic error,
  off-by-one, null dereference, etc.)

- **Fix Correctness Validation**: For each proposed fix, apply it to the codebase
  and measure: (a) does the test suite pass? (b) are there regressions (new test
  failures)? (c) does the fix address the root cause or just mask the symptom?

- **Explanation Quality Assessment**: Extract the agent's explanation of the
  failure and root cause; score on clarity, technical accuracy, and usefulness
  for a developer to understand _why_ the bug occurred; use LLM-as-judge or
  manual review by experienced developers

- **False Positive & False Negative Analysis**: Introduce code that appears buggy
  but is actually correct (false positive test) and code with subtle bugs the
  agent might miss (false negative test); measure precision and recall

- **Comparative Scorecard**: Build a rubric weighing root cause accuracy, fix
  correctness, explanation quality, and false positive rate; rank agents and
  identify which bug categories each agent handles best/worst

## Bug Benchmark Categories

- **Logic Errors**
  - Off-by-one in loops
  - Incorrect conditional branches
  - Wrong operator (e.g., `==` vs. `=`)
  - Incorrect return value or side effect

- **Boundary Conditions**
  - Empty input handling
  - Null/None dereference
  - Integer overflow/underflow
  - Array index out of bounds

- **API Misuse**
  - Incorrect function call signature
  - Forgetting required initialization
  - Using deprecated API
  - Incorrect state machine transitions

- **Concurrency**
  - Race condition (shared mutable state)
  - Deadlock in locking
  - Missing synchronization

- **Resource Management**
  - Memory leak (object not freed)
  - File handle not closed
  - Connection pool exhaustion

- **Integration Bugs**
  - Type mismatch between modules
  - Data format incompatibility
  - Timing dependency (events out of order)

## Sample Bug Scenarios

### Example 1: Off-by-One Loop

```python
def find_max(arr: List[int]) -> int:
    max_val = arr[0]
    for i in range(len(arr)):  # Should be range(1, len(arr))
        if arr[i] > max_val:
            max_val = arr[i]
    return max_val

# Bug: arr[len(arr)] is out of bounds on first iteration when i == len(arr)
```

### Example 2: Null Dereference

```python
def get_user_email(user_id: int) -> str:
    user = database.find_user(user_id)
    return user.email  # Bug: user can be None if not found

# Correct fix: Check if user is None
```

### Example 3: Resource Leak

```python
def read_config(path: str) -> dict:
    file = open(path, 'r')
    data = json.load(file)
    return data
    # Bug: file handle not closed; should use 'with' statement
```

## Bonus Ideas

- **Multi-File Bug Tracing**: Create bugs that require tracing across 3+ files
  (e.g., data flows from API layer → business logic → database); measure which
  agents can trace dependencies across module boundaries

- **Performance Bug Detection**: Introduce intentional performance regressions
  (O(n²) algorithm, memory leak causing GC pressure); evaluate whether agents
  identify these as bugs and suggest optimization

- **Reproduction Time**: Measure how many agent "turns" (prompts/iterations) are
  needed to reach correct diagnosis; shorter paths indicate more efficient
  reasoning

- **Adversarial Tests**: Introduce bugs that are intentionally obfuscated (e.g.,
  bug triggered only under rare conditions); evaluate robustness and false
  positive rate

- **Explanation Clarity**: Have human developers rate agent explanations
  independently; measure whether explanation clarity correlates with fix
  correctness

- **Domain-Specific Bugs**: Create bug sets for specific domains (web services,
  data pipelines, ML model training) and measure agent specialization

- **Fix Quality Rubric**: Beyond "does it pass tests?", score fixes on: elegance,
  performance impact, readability, and adherence to project style

## Useful Resources

- **Real Bug Datasets**:
  - Defects4J (Java bugs): https://github.com/rjust/defects4j
  - BugsInPy (Python bugs): https://github.com/soarsmu/BugsInPy
  - GitHub Issues (labeled bugs): Search GitHub for `label:bug`

- **Debugging Tools & Analysis**:
  - `pdb` (Python Debugger): https://docs.python.org/3/library/pdb.html
  - `gdb` (C/C++ Debugger): https://www.gnu.org/software/gdb/
  - Valgrind (Memory analysis): https://valgrind.org
  - `strace` / `ltrace` (System call tracing): For understanding OS-level failures

- **Test Frameworks for Validation**:
  - pytest: https://docs.pytest.org
  - unittest: https://docs.python.org/3/library/unittest.html
  - Hypothesis (property-based testing): https://hypothesis.readthedocs.io

- **Agent Platforms**:
  - Devin Documentation: https://docs.cognition.ai
  - OpenDevin GitHub: https://github.com/OpenDevin/OpenDevin
  - Cursor Docs: https://docs.cursor.com

- **LLM-as-Judge**:
  - Claude API: https://anthropic.com/api
  - OpenAI API: https://platform.openai.com/docs
