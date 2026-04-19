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
- `llm` is a Python package typically installed in a virtual environment
- Install with `uv` in the current virtual environment:
  ```bash
  # Install using uv tool.
  > uv tool install llm
  ```
- Benefits of using `uv tool install`:
  - Isolated environments for each tool
  - No pollution of global Python packages
  - Clean uninstall and updates
- Verify installation:
  ```bash
  # Check installed version.
  > llm --version
  llm version 0.27.1
  ```
- Alternative: Run without installing using `uvx` to fetch and run `llm` on
  demand without managing an installation:
  ```bash
  # Fetch and run directly.
  > uvx llm --version
  ```
  - Convenient for testing, but trades cold-start time for zero setup overhead

- Quick test:
  ```bash
  # Test basic functionality.
  > llm "Hi"
  Hello! How can I assist you today?
  ```

## Getting Help
- Every subcommand has a built-in help page:
  ```bash
  # Show main help.
  > llm --help
  Usage: llm [OPTIONS] COMMAND [ARGS]...

  Access Large Language Models from the command-line

  Options:
    --version   Show the version and exit.
    -h, --help  Show this message and exit.

  Commands:
    prompt*       Execute a prompt
    aliases       Manage model aliases
    chat          Hold an ongoing chat with a model.
    collections   View and manage collections of embeddings
    embed         Embed text and store or return the result
    embed-models  Manage available embedding models
    embed-multi   Store embeddings for multiple strings at once in the...
    fragments     Manage fragments that are stored in the database
    install       Install packages from PyPI into the same environment as LLM
    keys          Manage stored API keys for different models
    logs          Tools for exploring logged prompts and responses
    models        Manage available models
    ollama        Commands for working with models hosted on Ollama server.
    openai        Commands for working directly with the OpenAI API
    openrouter    Commands relating to the llm-openrouter plugin
    plugins       List installed plugins
    schemas       Manage stored schemas
    similar       Return top N similar IDs from a collection using cosine...
    templates     Manage stored prompt templates
    tools         Manage tools that can be made available to LLMs
    uninstall     Uninstall Python packages from the LLM environment
  ```
- Subcommands support `--help` for detailed information:
  ```bash
  # Show models subcommand help.
  > llm models --help
  Usage: llm models [OPTIONS] COMMAND [ARGS]...

  Manage available models

  Options:
    -h, --help  Show this message and exit.

  Commands:
    list*    List available models
    default  Show or set the default model
    options  Manage default options for models
  ```

## Managing API Keys
**Using environment variables**

- Pass API keys through environment variables such as:
  - `OPENAI_API_KEY`
  - `ANTHROPIC_KEY`
  - `OPENROUTER_KEY`
  
- Note that `llm` uses `OPENROUTER_KEY`, while usually this is variable is called
  `OPENROUTER_API_KEY`

**Using the `keys` command**

- API keys are stored securely and required for cloud-based models (OpenAI,
  Anthropic, etc.)
- The `keys` command manages them:
  ```bash
  # Set OpenAI key.
  > llm keys set openai
  Password: [paste your OpenAI API key]
  # List stored keys.
  > llm keys list
  openai
  ```
- Set keys for any provider:
  ```bash
  # Set Anthropic key.
  > llm keys set anthropic
  Password: [paste your Anthropic API key]
  # Set OpenRouter key.
  > llm keys set openrouter
  Password: [paste your OpenRouter API key]
  ```
- Keys are stored in the LLM database (with location varying by OS) and are
  never logged or cached insecurely
- Once set, models from that provider work automatically:
  ```bash
  # Use Anthropic key automatically.
  > llm -m claude-3-5-sonnet "Hello"
  ```

## Working with Models
- List available models grouped by provider:
  ```bash
  # Show all available models.
  > llm models
  OpenAI Chat: gpt-4o (aliases: 4o)
  OpenAI Chat: chatgpt-4o-latest (aliases: chatgpt-4o)
  OpenAI Chat: gpt-4o-mini (aliases: 4o-mini)
  ...
  OpenAI Chat: gpt-5
  OpenAI Chat: gpt-5-mini
  OpenAI Chat: gpt-5-nano
  Default: gpt-4o-mini
  ```
- Key features:
  - **Aliases**: Model names like `gpt-4o` can be called as `4o` for shorter
    commands
  - **Default model**: The last line shows which model runs when not specified
  - **Plugin-provided models**: Anthropic, Gemini, Ollama available after
    installing plugins (e.g., `llm install llm-anthropic`)
- Change the default model:
  ```bash
  # Set new default model.
  > llm models default 4o
  # Use model for a single invocation.
  > llm -m 4o "Summarize the theory of relativity in two sentences."
  ```
- Common flags:
  - `-m <model>`: Select the model for this invocation
  - `-s <system>`: Provide a system prompt
  - `-c`: Continue the previous conversation
  - `--no-stream`: Disable token streaming, print all at once
  - `-o <key>=<value>`: Pass model-specific options (temperature, max_tokens,
    etc.)
  - `--json`: Output response as JSON for programmatic parsing

## Chat Mode: Multi-turn Conversations
- Use `llm chat` for back-and-forth dialogue instead of one-off prompts:
  ```bash
  # Start interactive chat session.
  > llm chat
  Chatting with gpt-4o-mini
  Type 'exit' to quit, '/help' for help
  You: What is entropy?
  Model: Entropy is a measure of disorder or randomness in a system...
  You: Give me a Python example.
  Model: Here's a simple example...
  ```
- Chat maintains conversation history across turns, so context carries forward
  automatically
- Pick a model or set a system prompt for the conversation:
  ```bash
  # Start chat with specific model and system prompt.
  > llm chat -m 4o -s "You are a Python expert."
  ```
- Chat sessions are logged to the database for later review:
  ```bash
  # Show last 10 logged conversations.
  > llm logs -n 10
  ```

## Plugins to Unlock More Models
- Plugins expand `llm` with support for additional model providers
- View installed plugins:
  ```bash
  # List all plugins.
  > llm plugins
  [
    {
      "name": "llm-ollama",
      "hooks": [
        "register_commands",
        "register_embedding_models",
        "register_models",
        "register_tools"
      ],
      "version": "0.15.1"
    },
    {
      "name": "llm-openrouter",
      "hooks": [
        "register_commands",
        "register_models"
      ],
      "version": "0.5"
    }
  ]
  ```
- Install plugins for other providers:
  ```bash
  # Anthropic Claude models.
  > llm install llm-anthropic
  # OpenRouter models.
  > llm install llm-openrouter
  # Google Gemini.
  > llm install llm-gemini
  ```
- After installation, new models appear in `llm models`:
  ```bash
  # Install plugin.
  > llm install llm-anthropic
  # List models including new plugin.
  > llm models
  OpenAI Chat: gpt-4o (aliases: 4o)
  ...
  Anthropic Chat: claude-3-5-sonnet (aliases: claude)
  Anthropic Chat: claude-3-5-haiku
  ```
- Use plugin models like any other:
  ```bash
  # Use Claude for PDF summarization.
  > llm -m claude "Summarize this PDF"
  # Start chat with security expert prompt.
  > llm chat -m claude-3-opus -s "You are a security expert"
  ```

## Local Models with Ollama
- Run open-source models locally without API keys or costs using Ollama:
  ```bash
  # Install and start Ollama.
  > ...
  # Download a model from `ollama.ai`.
  > ollama pull mistral
  # Start the Ollama server.
  > ollama serve
  ```
- In another terminal, use the model via `llm`:
  ```bash
  # Show available models.
  > llm models
  Ollama (via Ollama): mistral
  # Run mistral model.
  > llm -m mistral "What is Rust?"
  Rust is a systems programming language...
  ```
- Benefits of local models:
  - No API costs: Run as many times as you want for free
  - No rate limits: Process large batches without hitting API ceilings
  - Privacy: Your prompts never leave your machine
  - Offline: Works without internet connectivity
- Drawbacks of local models:
  - Generally less capable than GPT-4o or Claude (but improving rapidly)
  - Slower than models served by providers

## Fragments: Reusable Prompt Pieces
- Fragments are named chunks of text loaded from files, useful for giving the
  model reference context:
  ```bash
  # View fragment file.
  > cat my_fragment.txt
  The solar eclipse will occur on April 8, 2024, visible across North America.
  # Use fragment in prompt.
  > llm -f my_fragment.txt "Summarize the above in one sentence."
  ```
- Fragments support multiple sources:
  - **Local files**: Load text directly from the filesystem
  - **URLs**: Reference remote content without copying locally:
    ```bash
    > llm -f https://raw.githubusercontent.com/simonw/llm/main/README.md \
        "What are the top three features mentioned here?"     `
    ```
  - **Multiple fragments**: Stack `-f` flags to compare documents or provide
    multiple context pieces at once

## Piping, Files, and Templates
- Because `llm` reads from stdin, you can Unix-style pipe anything into it:
  ```bash
  > cat prompt.txt | llm | tee output.txt
  ```

- The `tee` step keeps the response on the terminal and also writes it to disk,
  preventing long output from being lost to scrollback

## Templates
- Templates bundle a system prompt, default model, and parameters into a single
  reusable YAML file:
  ```yaml
  system: |
    You are a careful technical editor. Rewrite the user's text as clean Markdown
    with headings, bullet lists, and fenced code blocks where appropriate.
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

## Logging and History
- Every prompt and response is logged automatically to a local database for
  reproducibility and auditing:
  ```bash
  # Show all logged interactions.
  > llm logs
  41  2026-04-19 10:22:34  gpt-4o-mini  "What is entropy?"
  40  2026-04-19 10:21:15  gpt-4o-mini  "Summarize this article..."
  39  2026-04-19 10:20:02  claude       "Help debug this Python error"
  ```
- Retrieve a specific logged response:
  ```bash
  # View specific log entry.
  > llm logs 41
  Model: gpt-4o-mini
  Prompt: What is entropy?
  Response: Entropy is a measure of disorder or randomness...
  ```
- View responses in JSON format for parsing:
  ```bash
  # Filter logs by model in JSON.
  > llm logs --json | jq '.[] | select(.model == "claude")'
  ```
- Logging is valuable for:
  - Auditing: Track what models were asked and when
  - Cost analysis: See which models consume tokens
  - Reproducibility: Retrieve exact prompts later
  - Learning: Review patterns in what works well

## Practical Recipes
- Explain a diff before committing:
  ```bash
  # Generate commit message from staged changes.
  > git diff --staged | llm "Write a short, precise commit message for this diff."
  ```
- Summarize a long log file:
  ```bash
  # Analyze error logs.
  > tail -n 500 server.log | llm -s "You are an SRE on call. What went wrong?"
  ```
- Run the same prompt against several models and compare:
  ```bash
  # Test prompt across models.
  > for m in 4o 4o-mini gpt-5-mini; do \
      echo "=== $m ===" \
      cat prompt.txt | llm -m "$m" \
    done
  ```
- Start a continuing conversation:
  ```bash
  # First turn.
  > llm "What is entropy in information theory?"
  # Continue with context.
  > llm -c "Give me a Python example."
  ```
- Batch process multiple items:
  ```bash
  # Process multiple URLs.
  > cat urls.txt | while read url; do \
      echo "Processing: $url" \
      curl -s "$url" | llm "Summarize the main point" \
    done
  ```

## Advanced Piping Patterns
- Combine `llm` with `jq` to extract structured data:
  ```bash
  # Get JSON output and extract first item.
  > llm --json "List 3 Python libraries for data science" | jq -r '.[0].content'
  Pandas: A library for data manipulation and analysis
  ```
- Parse CSV and enrich it with LLM analysis:
  ```bash
  # Classify customers from CSV.
  > cat customers.csv | while IFS=, read id name; do \
      echo "Classifying customer: $name" \
      echo "$name" | llm "Assign one industry category" >> results.txt \
    done
  ```
- Chain multiple models and compare outputs:
  ```bash
  # Compare model responses.
  > PROMPT="Explain quantum entanglement simply"
  > echo "OpenAI:" && echo "$PROMPT" | llm -m 4o
  > echo "Anthropic:" && echo "$PROMPT" | llm -m claude
  > echo "Ollama:" && echo "$PROMPT" | llm -m mistral
  ```
- Extract structured output and feed downstream:
  ```bash
  # Analyze git log and save results.
  > git log --oneline -10 | llm "Group these by feature/fix/refactor" --json | \
    jq '.content' | tee git_summary.txt
  ```
- Monitor logs in real-time and trigger actions:
  ```bash
  # Analyze errors as they occur.
  > tail -f app.log | while read line; do \
      if echo "$line" | grep -q ERROR; then \
        echo "$line" | llm "Is this a critical error?" \
      fi \
    done
  ```

## Cost Awareness
- Cloud models charge per token; monitor your usage:
  ```bash
  # Summarize usage by model.
  > llm logs --json | jq '[.[].model] | group_by(.) | map({model: .[0], count: length})'
  [
    {"model": "gpt-4o-mini", "count": 42},
    {"model": "claude-3-5-haiku", "count": 15}
  ]
  ```
- Cheaper alternatives for common tasks:
  - **Summarization**: Use `gpt-4o-mini` or Haiku instead of GPT-4o
  - **Simple questions**: Local Ollama models cost $0
  - **Batch processing**: Use cheaper models, save GPT-4o for complex reasoning
  - **Prototyping**: Test with OpenRouter's cheaper provider options
- Track spending by monitoring regularly:
  ```bash
  # Count total interactions.
  > llm logs --json | jq '[.[].model] | length'
  3
  ```

## Why This Matters
- The power of `llm` lies in its Unix philosophy: it behaves like every other
  command-line tool
  - Rather than a chat interface, `llm` becomes infrastructure that composes
    with `grep`, `sed`, `jq`, and custom scripts
- This shift unlocks:
  - Automated workflows: Code review, log triage, document summarization
  - Personal tools: Custom scripts that would be too tedious to build against an
    HTTP API
  - Faster iteration: Go from "I wish a model could do this" to a working
    one-liner in minutes
  - Integration ease: Pipe model output into your existing Unix toolchain
- For developers living in the terminal, `llm` is the shortest path from idea to
  implementation
