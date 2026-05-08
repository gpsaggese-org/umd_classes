brew install ollama

Start the server

OLLAMA_FLASH_ATTENTION="1" OLLAMA_KV_CACHE_TYPE="q8_0" /opt/homebrew/opt/ollama/bin/ollama serve

> ollama pull llama3
pulling manifest
pulling 6a0746a1ec1a:  48% ▕██████████████████████████████████████████████████████████████████████                                                                            ▏ 2.3 GB/4.7 GB   17 MB/s   2m19s

ollama run llama3

Fast models
	•	llama3:8b (Meta)
	•	mistral:7b
	•	gemma:2b from Google

Check that it works

> pip install llm

> llm "Hello"

Install the plugin

> llm install llm-ollama

Collecting llm-ollama

Installing collected packages: ollama, llm-ollama
Successfully installed llm-ollama-0.15.1 ollama-0.6.1

Besides Ollama, you can use plugins for:
	•	llm-gpt4all → runs GPT4All
	•	llm-llama-cpp → runs via llama.cpp
	•	llm-mlx → Apple Silicon optimized models

# Oolama

> ollama
Ollama 0.21.0

  Chat with a model
    Start an interactive chat with a model

  Launch OpenClaw (install)
    Personal AI with 100+ skills

  Launch Claude Code
    Anthropic's coding tool with subagents

  Launch OpenCode (not installed)
    Anomaly's open-source coding agent

  Launch Hermes Agent (install)
    Self-improving AI agent built by Nous Research

  Launch Codex (not installed)
    OpenAI's open-source coding agent

  Launch Copilot CLI (not installed)
    GitHub's AI coding agent for the terminal

  Launch Droid (not installed)
    Factory's coding agent across terminal and IDEs

▸ Launch Pi (install)
    Press enter to install


> ollama -h
Large language model runner

Usage:
  ollama [flags]
  ollama [command]

Available Commands:
  serve       Start Ollama
  create      Create a model
  show        Show information for a model
  run         Run a model
  stop        Stop a running model
  pull        Pull a model from a registry
  push        Push a model to a registry
  signin      Sign in to ollama.com
  signout     Sign out from ollama.com
  list        List models
  ps          List running models
  cp          Copy a model
  rm          Remove a model
  launch      Launch the Ollama menu or an integration
  help        Help about any command

Flags:
  -h, --help         help for ollama
      --nowordwrap   Don't wrap words to the next line automatically
      --verbose      Show timings for response
  -v, --version      Show version information

Use "ollama [command] --help" for more information about a command.


ollama pull phi3:mini


https://ollama.com/search

Compare models

| Platform / Website            | URL                                  | Covers Open | Covers Closed | Key Focus                          | Quality (High/Med/Low) | Notes                                                                 |
|-----------------------------|--------------------------------------|-------------|---------------|------------------------------------|------------------------|----------------------------------------------------------------------|
| Vellum LLM Leaderboard      | https://vellum.ai/llm-leaderboard    | Yes         | Yes           | Benchmarks, cost, latency          | High                   | Frequently updated, practical metrics for real-world use              |
| Artificial Analysis         | https://artificialanalysis.ai        | Yes         | Yes           | Intelligence, speed, pricing       | High                   | One of the most comprehensive and structured comparisons              |
| Onyx Leaderboard            | https://onyx.app/llm-leaderboard     | Yes         | Yes           | Task-specific evaluation           | Medium                 | Useful breakdowns, but less widely cited                             |
| LLM Stats                   | https://llm-stats.com                | Yes         | Yes           | Aggregated benchmarks and pricing  | Medium                 | Good aggregation, depends on external benchmark quality              |
| OpenRouter Rankings         | https://openrouter.ai/rankings       | Yes         | Yes           | Real-world usage data              | Medium                 | Reflects usage trends, not pure capability                           |
| LMArena (Chatbot Arena)     | https://lmarena.ai                  | Yes         | Yes           | Human preference voting            | Very High              | Considered one of the most reliable real-world evaluation signals     |
| Hugging Face Open LLM LB    | https://huggingface.co/open-llm-leaderboard | Yes | No            | Standardized benchmarks            | High                   | Gold standard for open models, though benchmarks can saturate        |
| Vellum Open LLM Leaderboard | https://vellum.ai/open-llm-leaderboard | Yes      | No            | Updated open model evals           | High                   | Focuses on newer, less-contaminated benchmarks                        |
| Onyx Open LLM Leaderboard   | https://onyx.app/open-llm-leaderboard | Yes       | No            | Task and size breakdown            | Medium                 | Helpful but smaller ecosystem                                        |
| LangSmith                   | https://smith.langchain.com          | Yes         | Yes           | Custom evaluation pipelines        | High                   | Widely used in production LLM systems                                |
| Weights & Biases (W&B)      | https://wandb.ai                     | Yes         | Yes           | Experiment tracking and evals      | Very High              | Industry-standard ML tooling                                         |
| Arize Phoenix               | https://phoenix.arize.com            | Yes         | Yes           | Observability and evaluation       | High                   | Strong for debugging and monitoring                                  |
| Galileo                     | https://galileo.ai                   | Yes         | Yes           | Hallucination and quality testing  | High                   | Focused on reliability and eval quality                              |

## Using llm

> llm -m ollama/llama3 "Explain recursion simply"
Error: 'Unknown model: ollama/llama3'



https://www.vellum.ai/llm-leaderboard


ollama run mistral:7b-instruct-q4_K_M


Measure tokens per sec

llm -m llama3 --log "Explain recursion simply"

#!/bin/bash
START=$(date +%s)

llm -m ollama/llama3 --stream \
  "Explain recursion in 100 words" | tee output.txt

END=$(date +%s)
DURATION=$((END - START))

WORDS=$(wc -w < output.txt)

# Convert words → tokens (approx: 1 token ≈ 0.75 words)
TOKENS=$(awk "BEGIN {print $WORDS / 0.75}")

TPS=$(awk "BEGIN {print $TOKENS / $DURATION}")

echo "Duration: ${DURATION}s"
echo "Words: $WORDS"
echo "Estimated tokens: $TOKENS"
echo "Tokens/sec: $TPS"


ollama3
Tokens/sec: 6.86665

> run_eval.sh
Recursion is a powerful concept in computer science that allows a function to call itself repeatedly until a specific condition is met. This technique can be used to solve problems by breaking them down into smaller, more manageable subproblems of the same type. The key to recursion is finding a base case, which is a condition that stops the recursive loop from continuing indefinitely, and an induction step, which shows how to apply the recursive solution to a larger problem based on the solution to a smaller one. Recursive algorithms can be used for a wide range of tasks, including sorting, searching, and generating
 mathematical sequences.
Duration: 43s
Words:      106
Estimated tokens: 141.333
Tokens/sec: 3.28681

phi3:mini
Duration: 10s
Words:       88
Estimated tokens: 117.333
Tokens/sec: 11.7333

tinyllama
Duration: 19s
Words:      376
Estimated tokens: 501.333
Tokens/sec: 26.3859

# llama.cpp

how to run tinyllama on mac m2 using llama.cpp
