---
title: "How to Use Simon Willison's llm CLI"
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

The terminal is where most developers already live, and large language models
deserve to be there too. Opening a browser tab to ask a quick question is slow,
breaks flow, and makes it almost impossible to integrate the model's output
with the rest of a workflow. Simon Willison's `llm` CLI solves this by wrapping
OpenAI, Anthropic, Gemini, local Ollama models, and many others behind a single
command-line interface.

What makes `llm` stand out is not just that it exists, but that it feels like a
proper Unix tool. It reads from stdin, writes to stdout, supports templates and
fragments, and can be composed with `grep`, `jq`, `tee`, and friends. This post
walks through installation, the core concepts, and a handful of recipes that
make `llm` genuinely useful in day-to-day work.

The official project lives at
[github.com/simonw/llm](https://github.com/simonw/llm) with documentation at
[llm.datasette.io](https://llm.datasette.io/en/stable/).

## Installation

The cleanest way to install `llm` is with `uv`, the fast Python package manager
from Astral. The `uv tool install` command sets up an isolated environment for
each tool, so `llm` and its plugins do not pollute your global Python
environment:

```bash
> uv tool install llm
> export PATH="$HOME/.local/bin:$PATH"
```

Confirm the install by checking the version:

```bash
> uvx llm --version
llm version 0.27.1
```

If you prefer not to manage an install at all, `uvx llm ...` will fetch and run
`llm` on demand. That is convenient for trying it out without committing, at
the cost of a short cold-start each invocation.

## Getting Help

Every subcommand has a built-in help page, and the top-level help is a good
starting map of the tool:

```bash
> llm --help
```

Every subcommand supports `--help` as well, so `llm models --help` or
`llm templates --help` will tell you everything you need to know without
leaving the terminal.

## Working With Models

The `models` subcommand lists every model `llm` can currently reach, grouped
by provider:

```bash
> llm models
OpenAI Chat: gpt-4o (aliases: 4o)
OpenAI Chat: chatgpt-4o-latest (aliases: chatgpt-4o)
OpenAI Chat: gpt-4o-mini (aliases: 4o-mini)
…
OpenAI Chat: gpt-5
OpenAI Chat: gpt-5-mini
OpenAI Chat: gpt-5-nano
Default: gpt-4o-mini
```

A few things to notice:

- **Aliases**: A model like `gpt-4o` can be called as `4o`, which keeps the
  command line short
- **Default model**: The last line shows which model runs when you do not
  specify one
- **Plugin-provided models**: Anthropic, Gemini, Ollama, and other providers
  show up once their plugin is installed (e.g., `llm install llm-anthropic`)

To change the default model for the session use `llm models default <name>`, or
pass `-m <name>` on any single invocation:

```bash
> llm -m 4o "Summarize the theory of relativity in two sentences."
```

| Flag            | Purpose                                      |
| :-------------- | :------------------------------------------- |
| `-m <model>`    | Select the model for this invocation         |
| `-s <system>`   | Provide a system prompt                      |
| `-c`            | Continue the previous conversation           |
| `--no-stream`   | Disable token streaming, print all at once   |

## Fragments: Reusable Prompt Pieces

A common pattern is to feed the model a block of reference text and then ask
questions against it. Rather than pasting the text into every prompt, `llm`
supports **fragments**, which are named chunks of text loaded from files:

```bash
> cat my_fragment.txt
The solar eclipse will occur on April 8, 2024, visible across North America.
> llm -f my_fragment.txt "Summarize the above in one sentence."
```

Fragments can also be URLs or GitHub blob references, which is handy when you
want the model to reason about a specific file without copying it locally:

```bash
> llm -f https://raw.githubusercontent.com/simonw/llm/main/README.md \
    "What are the top three features mentioned here?"
```

Multiple `-f` flags can be stacked, which is useful for comparing documents or
giving the model several pieces of context at once.

## Piping, Files, and Templates

Because `llm` reads from stdin, you can pipe anything into it. The simplest
recipe sends a prompt from a file and saves the response:

```bash
> cat prompt.txt | llm | tee output.txt
```

The `tee` step keeps the response on the terminal and also writes it to disk,
which is useful when the response is long enough that scrollback might lose it.

**Templates** let you bundle a system prompt, default model, and parameters
into a reusable unit stored in a YAML file:

```bash
> cat prompt.txt | llm -t llm-markdown.yaml | tee output.txt
```

A template typically looks like:

```yaml
system: |
  You are a careful technical editor. Rewrite the user's text as clean
  Markdown with headings, bullet lists, and fenced code blocks where
  appropriate.
model: 4o
```

With the template defined, the same command can be dropped into any shell
script or Makefile without repeating the prompt configuration.

To use the template:

```bash
> cat prompt.txt | llm -t llm-markdown.yaml | tee output.txt
```

## Practical Recipes

**Explain a diff before committing:**

```bash
> git diff --staged | llm "Write a short, precise commit message for this diff."
```

**Summarize a long log file:**

```bash
> tail -n 500 server.log | llm -s "You are an SRE on call." "What went wrong?"
```

**Run the same prompt against several models and compare:**

```bash
> for m in 4o 4o-mini gpt-5-mini; do
>     echo "=== $m ==="
>     cat prompt.txt | llm -m "$m"
> done
```

**Start a continuing conversation:**

```bash
> llm "What is entropy in information theory?"
> llm -c "Give me a Python example."
```

## Why This Matters

The real power of `llm` is not any single feature but the fact that it behaves
like every other tool on the command line. Once a model is a pipe you can
compose with `grep`, `sed`, `jq`, and your own scripts, it stops being a chat
companion and starts being a piece of infrastructure. That shift opens the door
to automated code review, log triage, document summarization, and dozens of
small personal tools that would be too tedious to build against a raw HTTP
API.

If you already live in the terminal, `llm` is the shortest path from "I wish a
model could do this" to "here is a one-liner that does it".
