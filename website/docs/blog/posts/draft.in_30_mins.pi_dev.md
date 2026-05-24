---
title: "Pi.dev in 30 minutes"
draft: true
authors:
  - gpsaggese
date: 2026-05-23
categories:
  - Developer Tools
  - AI Coding
---

TL;DR: `pi.dev` is a lightweight, open-source AI coding agent that runs entirely
on your machine. You can pick an LLM provider and let `pi.dev` handle debugging,
refactoring, and code generation without any cloud dependency. It is great when
you want full control

<!-- more -->

## Introduction
`pi.dev` is an open-source AI coding agent. Unlike cloud-based tools, `pi.dev`
runs entirely on your machine with no backend, no telemetry, no vendor lock-in.
You choose your LLM provider (OpenAI, Anthropic, Ollama, or 15+ others), and
`pi.dev` integrates with it seamlessly

### Why Use `pi.dev`?
- **Your data stays yours**: Everything runs locally or on your infrastructure
- **Works offline**: Use self-hosted models like Ollama or vLLM with no internet
  required
- **Regulated environments**: Complies with data residency, air-gap, and audit
  requirements
- **Fully extensible**: Write Python extensions to add custom tools and
  workflows
- **Multi-provider**: Switch LLM providers without changing your workflow
- **Open-source**: Source-available, no licensing costs

### When NOT to Use `pi.dev`
- You want a polished IDE with a file explorer and diff viewer (use Claude Code)
- You prefer minimal setup and zero configuration (use Claude Code)
- You work on small, one-off tasks where setup overhead isn't worth it (use
  Claude Code)
- Your team needs shared workspaces (use Claude Code)

### Related Tools
- **Claude Code**: Full-featured SaaS IDE with Anthropic models (cloud-based)
- **GitHub Copilot**: Autocomplete tool embedded in your editor
- **Continue.dev**: Local-first IDE extension for coding assistance
- **LangChain / CrewAI**: Frameworks for building custom AI agents

**Official Resources:**

- [Pi.dev Website](https://pi.dev/)
- [Pi GitHub Repository](https://github.com/earendil-works/pi)
- [Pi Documentation](https://github.com/earendil-works/pi/tree/main/docs)

## Prerequisites

### What You Need
- **Python 3.10+** (or Node.js 18+ for the TypeScript version)
- **An LLM API key** from any supported provider:
  - OpenAI (GPT-4, GPT-4o)
  - Anthropic (Claude)
  - Together.ai, Groq, etc
  - Local Ollama or vLLM (no API key needed)
- **Basic terminal skills** (running commands, setting environment variables)
- **Git** (optional, but recommended for version control)

## Installation & Setup

### Step 1: Install `pi.dev`
- Via `npm` (Node.js/TypeScript version):
  ```bash
  > npm install -g --ignore-scripts @earendil-works/pi-coding-agent
  ```

- From source (for developers):
  ```bash
  > git clone https://github.com/earendil-works/pi.git
  > cd pi
  > pip install -e .
  ```

### Step 2: Configure Your LLM Provider
- `pi.dev` doesn't come with a built-in model—you choose. Set environment
  variables for your chosen provider

- Using OpenAI (e.g., GPT-4o)
  ```bash
  > export OPENAI_API_KEY="sk-proj-..."
  > pi --provider openai --model gpt-4o
  ```

- Using Anthropic (Claude)
  ```bash
  > export ANTHROPIC_API_KEY="sk-ant-..."
  > pi --provider anthropic --model claude-3-5-sonnet-20241022
  ```

- Local Ollama
  - First, install and run Ollama
    ```bash
    # Install from https://ollama.ai
    # Then in one terminal:
    > ollama serve

    # In another terminal:
    > ollama pull llama2  # or any model you want
    ```
  - Then configure `pi.dev`:
    ```bash
    > pi --provider ollama --model llama2 --base-url http://localhost:11434
    ```

### Step 3: Verify Setup
- Create a test project and run pi:
  ```bash
  > mkdir test-pi && cd test-pi
  > git init
  > echo 'print("hello world")' > test.py
  > pi
  ```

- You should see pi's prompt. Try a simple interaction:
  ```
  User: "What's in test.py?"

  Pi: <reads test.py and responds>
  ```

- Type `exit` to quit

## Core Concepts

### `pi.dev`'s Design Philosophy
- `pi.dev` is built on radical simplicity:
  - four tools
  - a message loop
  - extensions

- This makes it lightweight, predictable, and easy to customize

### The Four Core Tools
1. **Read**: Read files or directories
2. **Write**: Create or overwrite files
3. **Edit**: Make precise changes to existing files
4. **Bash**: Run shell commands

### Extensions: Where Pi Gets Smart
- Everything beyond those four tools comes from extensions:
  - Safety checks (permission gates)
  - Custom tools (database queries, API calls, internal tools)
  - Persistence (remembering state across sessions)
  - Workflow automation (CI/CD, code generation, etc.)

- You write extensions in Python. We'll see an example below

### The Session Model
- Each time you run `pi`, it:
  1. Reads your project structure
  2. Starts a message loop with the LLM
  3. You type prompts; `pi` executes tools and responds
  4. Sessions are stateless—no context persists between runs (unless you use
     extensions for state management)

## Hands-On Examples

### Example 1: Debug a Failing Test
- **Scenario**: You have a broken unit test and want pi to find the bug

- Create a test file with a bug:
  ```bash
  > mkdir debug-example && cd debug-example
  ```

- Create `calculator.py`:
  ```python
  def add(a, b):
      return a + b - 1  # Bug: subtracts 1

  def multiply(a, b):
      return a * b

  def divide(a, b):
      if b == 0:
          raise ValueError("Division by zero")
      return a / b
  ```

- Create `test_calculator.py`:
  ```python
  import pytest
  from calculator import add, multiply, divide

  def test_add():
      assert add(2, 3) == 5  # Will fail: gets 4

  def test_multiply():
      assert multiply(3, 4) == 12

  def test_divide():
      assert divide(10, 2) == 5.0
  ```

- Now run pi:
  ```bash
  > pi
  ```

- In the pi session:
  ```
  User: "Run the tests and tell me which one is failing and why"

  Pi:
  - Runs: python -m pytest test_calculator.py -v
  - Sees: test_add FAILED (expected 5, got 4)
  - Reads: calculator.py, test_calculator.py
  - Identifies: add() is subtracting 1
  - Proposes: Remove the "- 1" from the return statement

  User: "Fix it"

  Pi:
  - Edits: calculator.py (removes "- 1")
  - Runs: pytest again
  - Confirms: All tests pass!
  ```

- **Output:**
  ```
  tests passed! ✓
  ```

### Example 2: Refactor with a Self-hosted Model
- **Scenario**: You want to improve code quality but can't send it to the cloud
  (healthcare data, compliance, etc.)

- Set up Ollama locally:
  ```bash
  # Terminal 1: Run the model
  > ollama serve

  # Terminal 2: Configure pi.dev
  > export OLLAMA_MODEL="neural-chat"
  > pi --provider ollama --model neural-chat --base-url http://localhost:11434
  ```

- Create a messy function `process_data.py`:
  ```python
  def process(d):
      result = []
      for i in d:
          if i['status'] == 'active' and i['age'] > 18:
              x = i['salary'] * 1.1
              result.append({'name': i['name'], 'new_salary': x})
      return result
  ```

- In pi:
  ```
  User: "Refactor this code to be more readable. Use type hints and better names."

  Pi:
  - Reads: process_data.py
  - Suggests: Use TypedDict, extract magic numbers, add docstrings
  - Proposes: Refactored version with type hints

  User: "Apply it"

  Pi:
  - Writes: refactored code
  ```

### Example 3: Generate Boilerplate with a Custom Extension
- **Scenario**: Your team has a proprietary code generator for microservices. You
  want `pi` to use it

- Create a custom tool `pi_extensions/service_generator.py`:
  ```python
  from pi.core import Tool

  class GenerateService(Tool):
      name = "generate_service"
      description = "Generate TypeScript microservice boilerplate"
      
      def run(self, service_name: str, **kwargs):
          """Generate boilerplate for a new service."""
          template = f"""
  // Auto-generated service: {service_name}
  import express from 'express';

  const app = express();

  app.get('/health', (req, res) => {{
    res.json({{"status": "ok", "service": "{service_name}"}});
  }});

  app.listen(3000, () => {{
    console.log('{service_name} service running on port 3000');
  }});
  """
          return template
  ```

- Register it in pi:
  ```bash
  > pi --extensions pi_extensions
  ```

- In pi session:
  ```
  User: "Generate boilerplate for a new service called 'payment-api'"

  Pi:
  - Uses: generate_service with service_name="payment-api"
  - Returns: TypeScript template
  - Offers to write to: payment-api/index.ts

  User: "Write it and create a package.json too"

  Pi:
  - Writes: payment-api/index.ts
  - Writes: payment-api/package.json (with express, TypeScript deps)
  ```

### Example 4: Code Review and Cleanup
- **Scenario**: You have a messy script `batch_processor.py` and want pi to
  suggest improvements

- In pi:
  ```
  User: "Review this code and suggest improvements. Focus on safety, readability, 
         and error handling."

  Pi:
  - Identifies: bare except, unsafe file handling, no logging, unclear variable names
  - Suggests: Context manager, specific exceptions, type hints, docstring
  - Proposes improved version

  User: "Make the changes"

  Pi:
  - Writes: refactored version
  ```

## Tips & Gotchas

### Tip 1: Keep Your Editor Open
- `pi.dev` is terminal-only. Open your editor (VS Code, Vim, etc.) in another
  pane or window so you can see changes as they happen

- This way, when `pi` makes changes, you can see them immediately and catch any
  mistakes

### Tip 2: Choose the Right Model
- The quality of pi's output depends entirely on your LLM:
  - **Weak models** (gpt-3.5-turbo, Llama 2): Slow, make obvious mistakes
  - **Good models** (GPT-4o, Claude 3.5 Sonnet): Fast, reliable, worth the cost
  - **Self-hosted**: Slower (1-5 min per task) but private; good for prototyping,
    not real work

- Start with GPT-4o or Claude 3.5 Sonnet

### Tip 3: Break Large Tasks Into Small Prompts
- Don't ask pi to refactor a 50-file project in one go. Instead:
  ```
  User: "List all files in src/"
  User: "Show me the structure of database.py"
  User: "Refactor the Database class to use context managers"
  User: "Fix type hints in utils.py"
  ```

- Smaller prompts = better focus and fewer mistakes

### Gotcha 3: Extensions Are Optional, but Powerful
- If pi feels limited, you're probably missing an extension. Write one:
  ```python
  # my_tool.py
  from pi.core import Tool

  class MyTool(Tool):
      name = "my_tool"
      description = "What this does"
      
      def run(self, arg1, arg2, **kwargs):
          return f"Did something with {arg1} and {arg2}"
  ```

  Register it:
  ```bash
  > pi --extensions my_tool
  ```
