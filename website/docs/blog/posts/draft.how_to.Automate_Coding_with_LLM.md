---
draft: true
title: "Automate Coding with LLM: Scripts and Tools for AI-Powered Code Transformation"
authors:
  - gpsaggese
date: 2026-07-12
description: "A comprehensive guide to using LLM scripts and decorators for automating code review, refactoring, and transformation tasks."
categories:
  - Automation
  - LLM
  - Development Tools
---

TL;DR: Stop copying code to ChatGPT. Use `llm_cli.py` for text transformation, `llm_transform.py` for code review, `@llm` decorator for typed function stubs, and `lint_cc.py` to batch-apply style rules.

<!-- more -->

## Introduction

Writing code is only half the battle. Code review, refactoring, documentation, and style enforcement can consume more time than the initial implementation. Large Language Models (LLMs) are perfect for these repetitive, high-context tasks—but only if you integrate them into your workflow instead of copy-pasting into web UIs.

This post covers the suite of LLM automation tools built into the `helpers` library:

- **`llm_cli.py`** - General-purpose text transformation CLI
- **`llm_transform.py`** - Code review and refactoring with structured output
- **`@llm` decorator** - Type-driven LLM calls in Python code
- **`lint_cc.py`** - Batch apply Claude Code style rules to files
- **`hllm` library** - Core LLM abstraction with cost tracking

Whether you're refactoring a legacy module, generating documentation, or enforcing coding standards across a team, these tools eliminate the friction of manual LLM interactions.

---

## Tool Overview

### 1. `llm_cli.py` – The Workhorse

**What it does:** Reads text (file, stdin, or inline), sends it to an LLM, and writes back the result.

**When to use:** Text summarization, translation, style fixes, documentation generation, prompt engineering experiments.

**Key features:**
- 3 input sources: file, stdin, piped text
- 3 output destinations: file, stdout, in-place edit
- Chunk selection (select a specific section of a file)
- Flexible prompts: inline, file-based, rules, skills
- Cost tracking per call
- Progress bars and dry-run mode

**Basic examples:**

```bash
# Simplest test
llm_cli.py --input_text "Explain recursion" -o -

# File transformation
llm_cli.py -i input.txt -o output.txt -p "Summarize this in 5 bullets"

# In-place edit
llm_cli.py -i slides.txt

# Read from stdin, write to stdout
cat notes.txt | llm_cli.py -i - -o - -p "Fix grammar"

# Edit a chunk of a file
llm_cli.py -i doc.txt --select "## Introduction" -pf prompt.txt -m

# Apply a coding rule from .claude/skills/
llm_cli.py -i file.py --rule "coding.rules.md:58:## Mark Private Functions" -m

# Test a specific model
llm_cli.py --input_text "Say hello" --model "openrouter/anthropic/claude-haiku-4.5" -o -

# Preview before spending credits
llm_cli.py -i input.txt -p "Translate to French" --dry_run
```

**Architecture:**
```
llm_cli.py (151 lines)
  ↓
lib_llm_cli.py (637 lines) — Orchestration
  ↓
hllm_cli.py (1625+ lines) — Core library + backends
```

The 5-stage pipeline:
1. **Input Resolution** → Read from file/stdin/text
2. **Chunk Extraction** (optional) → Select a slice of the input
3. **Prompt Resolution** → Pick inline/file/rule/skill prompt
4. **LLM Call** → Apply transformation
5. **Output Writing** → File/stdout/in-place

---

### 2. `llm_transform.py` – Code Review and Refactoring

**What it does:** Reads code, applies LLM transformation (code review, refactoring suggestions), and outputs a **cfile** (structured list of issues and fixes).

**When to use:** Code review, refactoring proposals, linting with custom rules, identifying tech debt.

**Key features:**
- Predefined transformations: `code_review`, `code_propose_refactoring`, `uppercase`, etc.
- Generates cfiles (line-by-line change lists) for batch processing
- Docker-based execution (dependencies isolated)
- Supports custom transformations

**Examples:**

```bash
# List available transformations
llm_transform.py --list

# Code review → outputs cfile
llm_transform.py -i render_images.py -o cfile -p code_review

# Propose refactoring
llm_transform.py -i render_images.py -o cfile -p code_propose_refactoring

# Transform and compare side-by-side
llm_transform.py -i input.txt -o output.txt -p uppercase --compare
```

The output cfile can then be processed by **`llm_apply_cfile.py`** to batch-apply all changes, or by **`inject_todos.py`** to convert findings into TODO comments.

---

### 3. `@llm` Decorator – Type-Driven Function Calls

**What it does:** Turns a Python function stub into an LLM-powered function.

**When to use:** Anywhere you'd hardcode a prompt + manual type coercion.

**Key features:**
- Type annotations drive output format and coercion
- Caching via `simple_cache` (same args = cached result)
- `mock_apply_llm()` for testing (no API calls)
- Force refresh with `force_refresh=True`

**Example:**

```python
from helpers.hllm_decorator import llm

@llm(use_cache=True, model="gpt-4o-mini")
def classify_sentiment(text: str) -> str:
    """Classify text sentiment as 'positive', 'negative', or 'neutral'."""

@llm()
def extract_keywords(text: str) -> list[str]:
    """Extract key terms as a list."""

@llm()
def summarize_json(text: str) -> dict:
    """Summarize and return a dict with 'summary' and 'key_points' keys."""

# Usage
result = classify_sentiment("I love this product!")  # → "positive"
keywords = extract_keywords(text)  # → ["product", "love", ...]
summary = summarize_json(text)  # → {"summary": "...", "key_points": [...]}

# Bypass cache if needed
fresh = classify_sentiment(text, force_refresh=True)
```

**Under the hood:**
1. Docstring becomes task description
2. Function args become prompt inputs
3. Return type annotation → format instruction + auto-coercion
4. Result cached by prompt hash
5. Cache invalidation: source code change or explicit `force_refresh`

**Key design:** Type coercion is **resilient** — parsers strip extra text that LLMs add (e.g., "The sentiment is positive." → "positive").

---

### 4. `lint_cc.py` – Batch Style Rules

**What it does:** Applies Claude Code style rules (from `.claude/skills/`) to a set of files.

**When to use:** Team-wide code style enforcement, consistent rule application across projects.

**Key features:**
- File selection: modified, branched, explicit list
- Topic-based rules (coding, testing, slides, etc.)
- Skill-specific transformations
- Integrates with Claude Code rule system

**Examples:**

```bash
# Lint modified files
lint_cc.py --modified

# Lint files in current branch
lint_cc.py --branch

# Apply a specific skill to one file
lint_cc.py --skill coding.fix_inline --files "file.py"

# Apply a topic rule (e.g., Python coding style)
lint_cc.py --topic coding --files "file1.py file2.py"

# Apply a specific rule section
lint_cc.py --rule "coding.rules.md:58:## Mark Private Functions" --files "file.py"
```

---

### 5. `hllm` Library – Core Infrastructure

**What it does:** Provides low-level LLM abstractions with token cost tracking.

**Key components:**

| Module | Purpose |
|--------|---------|
| `hllm.py` | `get_completion()`, model stats, vector store integration |
| `hllm_cli.py` | `apply_llm()` with 3 backends (library, executable, mock) |
| `hllm_decorator.py` | `@llm` decorator (type-driven calls) |
| `hllm_cost.py` | Token accounting across providers |
| `llm_prompts.py` | Predefined transformation prompts (76KB) |
| `llm_compare.py` | Compare models side-by-side |

**Example: Direct library usage**

```python
import helpers.hllm_cli as hllmcli

response, token_stats = hllmcli.apply_llm(
    input_str="Summarize this article",
    system_prompt="Be concise.",
    model="gpt-4o-mini",
    backend="library"  # or "executable", "mock"
)

print(f"Response: {response}")
print(f"Cost: {token_stats.to_str()}")  # "$0.05", "1.23c", "5.2u$"
```

**Batch Processing (DataFrame):**

```python
import pandas as pd
import helpers.hllm_cli as hllmcli

df = pd.DataFrame({"text": ["article1", "article2", ...]})

# Apply LLM to each row
df["summary"] = hllmcli.apply_llm_prompt_to_df(
    df=df,
    column="text",
    prompt="Summarize in 1 sentence",
    mode="individual",  # individual | shared_prompt | combined
    batch_size=10
)
```

---

## Workflow Patterns

### Pattern 1: Code Review + Auto-Fix

```bash
# 1. Generate cfile with issues
llm_transform.py -i mymodule.py -o cfile -p code_review

# 2. Review the cfile, edit if needed
vi cfile

# 3. Apply all fixes
llm_apply_cfile.py --cfile cfile

# 4. Commit
git add mymodule.py
git commit -m "Apply automated code review suggestions"
```

### Pattern 2: Chunk Editing in Vim

Edit a specific section of a file with LLM:

```bash
# Edit lines 50-100 with a custom prompt
llm_cli.py -i document.txt --select 50:100 -p "Improve clarity" -m

# Edit by header name
llm_cli.py -i doc.txt --select "## Results" -p "Expand findings" -m
```

### Pattern 3: Style Enforcement Across Team

```bash
# Apply consistent style to all Python files
lint_cc.py --branch --topic coding

# Or apply a specific rule
lint_cc.py --modified --skill coding.fix_docstring
```

### Pattern 4: Function Decoration for ML Tasks

```python
@llm(model="gpt-4o-mini")
def extract_entities(text: str) -> dict:
    """Extract named entities from text."""

@llm(use_cache=True)
def classify_intent(message: str) -> str:
    """Classify user intent: 'support', 'sales', 'billing'."""

# In your app
for user_message in messages:
    intent = classify_intent(user_message)
    route_to_team(intent)
```

---

## Cost Tracking

All tools report token costs. Example output:

```
Total cost: Cost: 0.05$, Elapsed: 2.31s
  (input_tokens=1250, output_tokens=450, cost_from_llm_library=0.05, cost_from_tokencost=0.05)
```

For batch runs, track aggregate costs:

```bash
# Save stats to file
llm_cli.py -i input.txt -o output.txt -p "Summarize" --stat_file stats.json

# Combine stats across runs
python -c "
import json
costs = [json.load(open(f)) for f in ['stats1.json', 'stats2.json']]
total = sum(c['cost_from_llm_library'] for c in costs)
print(f'Total cost: \${total:.2f}')
"
```

---

## Advanced Features

### Dry-Run Preview

Before spending API credits, preview what will be sent:

```bash
llm_cli.py -i input.txt -p "Translate to Spanish" --dry_run
```

### Progress Bars

For long-running transformations:

```bash
llm_cli.py -i large_file.txt -o output.txt -p "Process" --progress_bar

# Or with explicit output size estimate
llm_cli.py -i file.txt -o out.txt -p "Summarize" --expected_num_chars 5000
```

### Model Selection

Test different models easily:

```bash
# Use Claude Haiku via OpenRouter (fast, cheap)
llm_cli.py -i input.txt -o output.txt -p "Fix style" \
  --model "openrouter/anthropic/claude-haiku-4.5"

# Use OpenAI GPT-4o
llm_cli.py -i input.txt -o output.txt -p "Review code" \
  --model "gpt-4o"

# Use local reasoning model
llm_cli.py -i input.txt -o output.txt -p "Complex analysis" \
  --model "openrouter/deepseek/deepseek-r1"
```

### Linting Output

Auto-format the LLM's response:

```bash
llm_cli.py -i slides.txt -o output.txt --lint
```

---

## When to Use Each Tool

| Tool | Best For | Speed | Cost |
|------|----------|-------|------|
| `llm_cli.py` | General text transformation, prototyping | Flexible | Per-call tracking |
| `llm_transform.py` | Code review, refactoring proposals | Batch | Tracked per file |
| `@llm` decorator | Integration into Python code, caching | Fast (cached) | Per-call, cached |
| `lint_cc.py` | Team-wide style enforcement | Batch | Bulk |
| `hllm` library | Custom workflows, batch DataFrame ops | Flexible | Per-operation |

---

## Getting Started

1. **Set up API keys:**
   ```bash
   export OPENAI_API_KEY="sk-..."
   export ANTHROPIC_API_KEY="sk-ant-..."
   ```

2. **Try the simplest example:**
   ```bash
   llm_cli.py --input_text "Explain recursion" -o -
   ```

3. **Review a file:**
   ```bash
   llm_transform.py -i myfile.py -o cfile -p code_review
   ```

4. **Decorate a function:**
   ```python
   from helpers.hllm_decorator import llm
   
   @llm()
   def my_function(arg: str) -> str:
       """Do something with LLM."""
   ```

5. **Enforce style:**
   ```bash
   lint_cc.py --branch --topic coding
   ```

---

## Key Takeaways

- **`llm_cli.py`** is your Swiss Army knife for one-off transformations and experiments
- **`llm_transform.py`** turns code review into a batch operation with structured output
- **`@llm` decorator** embeds LLM calls directly into Python logic
- **`lint_cc.py`** applies consistent style rules across projects
- **Cost tracking** comes built-in — no surprises

These tools eliminate the friction of manual LLM interaction and make LLM-powered automation feel native to your development workflow.

Stop copy-pasting to ChatGPT. Automate it.

---

## Further Reading

- `helpers_root/dev_scripts_helpers/llms/README.llm_cli.md` — Full CLI documentation
- `helpers_root/helpers/README.hllm_decorator.md` — Decorator architecture and design
- `tutorials/OpenAI/hllm.example.py` — Example usage patterns
- `helpers_root/linters2/README.md` — Linting framework overview
