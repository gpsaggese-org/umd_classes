---
title: "llm CLI in 30 minutes"
draft: true
authors:
  - gpsaggese
date: 2026-04-19
description:
categories:
  - Developer Tools
  - Productivity
---

TL;DR: Simon Willison's `llm` CLI turns any large language model into a
composable Unix tool you can pipe, script, and template from the terminal.

<!-- more -->

## Summary
- `llm` CLI brings large language models to the terminal, eliminating context
  switches and enabling integration with Unix tools.

- Official resources:
  - **Project**: [github.com/simonw/llm](https://github.com/simonw/llm)
  - **Documentation**: [llm.datasette.io](https://llm.datasette.io/en/stable/)

## Installation
- Install with `uv` (recommended):
  ```bash
  > uv tool install llm
  > export PATH="$HOME/.local/bin:$PATH"
  ```

- Benefits of using `uv tool install`:
  - Isolated environments for each tool
  - No pollution of global Python packages
  - Clean uninstall and updates

- Verify installation:
  ```bash
  > llm --version
  llm version 0.27.1
  ```

- **Alternative: Run without installing** using `uvx` to fetch and run `llm` on
  demand without managing an installation:
  ```bash
  > uvx llm --version
  ```
  - Convenient for testing, but trades cold-start time for zero setup overhead

## Getting Help
- Every subcommand has a built-in help page:
  ```bash
  > llm --help
  ```

- Subcommands support `--help` for detailed information:
  ```bash
  > llm models --help
  > llm templates --help
  ```

## Working with Models
- List available models grouped by provider:
  ```bash
  > llm models
  OpenAI Chat: gpt-4o (aliases: 4o)
  OpenAI Chat: chatgpt-4o-latest (aliases: chatgpt-4o)
  OpenAI Chat: gpt-4o-mini (aliases: 4o-mini)
  ...truncated output...
  OpenAI Chat: gpt-5
  OpenAI Chat: gpt-5-mini
  OpenAI Chat: gpt-5-nano
  Default: gpt-4o-mini
  ```

- Key features to notice:
  - **Aliases**: Model names like `gpt-4o` can be called as `4o` for shorter
    commands
  - **Default model**: The last line shows which model runs when not specified
  - **Plugin-provided models**: Anthropic, Gemini, Ollama, and others available
    after installing their plugins (e.g., `llm install llm-anthropic`)

- Change the default model for the session or per invocation:
  ```bash
  > llm models default 4o
  > llm -m 4o "Summarize the theory of relativity in two sentences."
  ```

- Common flags:
  - `-m <model>`: Select the model for this invocation
  - `-s <system>`: Provide a system prompt
  - `-c`: Continue the previous conversation
  - `--no-stream`: Disable token streaming, print all at once

## Fragments: Reusable Prompt Pieces
- Fragments are named chunks of text loaded from files, useful for giving the
  model reference context:
  ```bash
  > cat my_fragment.txt
  The solar eclipse will occur on April 8, 2024, visible across North America.
  > llm -f my_fragment.txt "Summarize the above in one sentence."
  ```

- Fragments support multiple sources:
  - **Local files**: Load text directly from the filesystem
  - **URLs**: Reference remote content without copying locally:
    `bash     > llm -f https://raw.githubusercontent.com/simonw/llm/main/README.md \
        "What are the top three features mentioned here?"     `
  - **GitHub blob references**: Easy access to specific repository files
  - **Multiple fragments**: Stack `-f` flags to compare documents or provide
    multiple context pieces at once

## Piping, Files, and Templates
**Unix-style piping**

- Because `llm` reads from stdin, you can pipe anything into it:
  ```bash
  > cat prompt.txt | llm | tee output.txt
  ```

- The `tee` step keeps the response on the terminal and also writes it to disk,
  preventing long output from being lost to scrollback

**Templates for reusable configurations**

- Templates bundle a system prompt, default model, and parameters into a single
  reusable YAML file:
  ```yaml
  system: |
    You are a careful technical editor. Rewrite the user's text as clean
    Markdown with headings, bullet lists, and fenced code blocks where
    appropriate.
  model: 4o
  ```

- Use the template in any command, shell script, or Makefile:
  ```bash
  > cat prompt.txt | llm -t llm-markdown.yaml | tee output.txt
  ```

- Benefits:
  - Standardize configurations across projects
  - Reduce repetition in scripts and automation
  - Share template definitions with team members

## Practical Recipes
- **Explain a diff before committing**:
  ```bash
  > git diff --staged | llm "Write a short, precise commit message for this diff."
  ```

- **Summarize a long log file**:
  ```bash
  > tail -n 500 server.log | llm -s "You are an SRE on call." "What went wrong?"
  ```

- **Run the same prompt against several models and compare**:
  ```bash
  > for m in 4o 4o-mini gpt-5-mini; do
  >     echo "=== $m ==="
  >     cat prompt.txt | llm -m "$m"
  > done
  ```

- **Start a continuing conversation**:
  ```bash
  > llm "What is entropy in information theory?"
  > llm -c "Give me a Python example."
  ```

## Why This Matters
- The power of `llm` lies in its Unix philosophy: it behaves like every other
  command-line tool
  - Rather than a chat interface, `llm` becomes infrastructure that composes
    with `grep`, `sed`, `jq`, and custom scripts

- This shift unlocks:
  - **Automated workflows**: Code review, log triage, document summarization
  - **Personal tools**: Custom scripts that would be too tedious to build
    against an HTTP API
  - **Faster iteration**: Go from "I wish a model could do this" to a working
    one-liner in minutes
  - **Integration ease**: Pipe model output into your existing Unix toolchain

- For developers living in the terminal, `llm` is the shortest path from idea to
  implementation
