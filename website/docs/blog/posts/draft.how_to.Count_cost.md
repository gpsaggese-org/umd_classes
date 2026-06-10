---
title: "How to Count LLM Usage Costs"
draft: true
authors:
    - gpsaggese
date: 2026-06-09
description: Tools for tracking LLM API usage costs
categories:
    - LLM
    - Developer Tools
---


## Overview

- LLM-powered coding assistants like Claude Code, GitHub Copilot, and Codex CLI
  boost productivity tremendously

- However, the cost of API usage can add up quickly, especially when working on
  complex tasks that consume hundreds of thousands of tokens per session

- Without tracking, it is easy to lose visibility into:
    - How much you are spending per day, week, or month
    - Which models are driving the costs
    - Whether your usage patterns are efficient

- Fortunately, several open-source tools exist to help you monitor and analyze
  your LLM usage

- In this post, we explore two practical tools for counting LLM costs:
    - **ccusage**: A CLI tool for generating usage reports across coding agent CLIs
    - **OpenUsage**: A terminal-based dashboard for monitoring AI tool usage and
      spend

<!-- more -->

# Comparison of LLM Cost Computation Methods

| Method | OpenAI Direct | Anthropic Direct | OpenRouter | Accuracy | Implementation Effort | Notes |
|----------|----------|----------|----------|----------|----------|----------|
| Provider-reported cost | Yes | Limited | Yes | Very High | Low | Best source when available |
| Response usage fields + pricing table | Yes | Yes | Yes | High | Low | Most common approach |
| Cost returned in API response | No | No | Sometimes | Very High | Very Low | Depends on provider or gateway |
| LiteLLM cost calculator | Yes | Yes | Yes | High | Low | Centralized multi-provider accounting |
| Langfuse cost tracking | Yes | Yes | Yes | High | Medium | Production observability and attribution |
| Helicone cost tracking | Yes | Yes | Yes | High | Medium | Request-level analytics |
| OpenRouter Analytics | No | No | Yes | Very High | Very Low | Includes provider-specific costs |
| Custom token accounting | Yes | Yes | Yes | Medium | Medium | Requires maintaining pricing catalog |
| CCUsage | No | Yes (Claude Code) | Partial | Medium | Very Low | Developer-focused usage tracking |
| OpenCost (Kubernetes) | No | No | No | N/A | Medium | Measures infrastructure, not token costs |
| GPU runtime accounting | Self-hosted only | Self-hosted only | Self-hosted only | High | Medium | For vLLM, TGI, SGLang, etc. |

# Typical Cost Formula

## OpenAI / Anthropic Direct

```text
Cost =
(input_tokens × input_price_per_million / 1,000,000)
+
(output_tokens × output_price_per_million / 1,000,000)
```

Example:

```text
GPT-4o

Input:
100,000 tokens × $2.50 / 1M = $0.25

Output:
50,000 tokens × $10.00 / 1M = $0.50

Total = $0.75
```

# OpenRouter Cost Computation

## Option 1: OpenRouter Analytics

```text
Cost = provider-reported cost
```

Advantages:

- Actual routed provider
- Actual model pricing
- Cached token discounts
- Provider-specific adjustments

## Option 2: Response Usage Data

Example response:

```json
{
  "usage": {
    "prompt_tokens": 1234,
    "completion_tokens": 567
  }
}
```

Then:

```text
Cost =
(prompt_tokens × model_input_price)
+
(completion_tokens × model_output_price)
```

using the OpenRouter model pricing catalog.

# What Each Tool Measures

| Tool | Token Cost | Infrastructure Cost | User Attribution | Multi-provider |
|--------|--------|--------|--------|--------|
| OpenAI Usage API | Yes | No | Limited | No |
| Anthropic Usage API | Yes | No | Limited | No |
| OpenRouter Analytics | Yes | No | Yes | Yes |
| LiteLLM | Yes | No | Yes | Yes |
| Langfuse | Yes | No | Yes | Yes |
| Helicone | Yes | No | Yes | Yes |
| CCUsage | Yes | No | Limited | Partial |
| OpenCost | No | Yes | Namespace/Team | N/A |
| Prometheus/Grafana | Custom | Yes | Custom | N/A |

# Recommended Approaches

| Scenario | Recommended Solution |
|-----------|----------------------|
| OpenAI only | Usage API + pricing table |
| Anthropic only | Usage fields + pricing table |
| OpenRouter only | OpenRouter Analytics |
| Multi-provider gateway | LiteLLM + Langfuse |
| Claude Code usage | CCUsage |
| Self-hosted models | OpenCost + Prometheus |
| Enterprise FinOps | Langfuse + OpenCost + billing APIs |

# Decision Matrix

| Requirement | Recommended Tool |
|------------|-----------|
| Exact billing amount | OpenRouter Analytics |
| Lowest implementation effort | Provider-reported cost |
| Multi-provider visibility | LiteLLM |
| User/team attribution | Langfuse |
| Claude Code tracking | CCUsage |
| Kubernetes GPU costs | OpenCost |
| Self-hosted inference costs | OpenCost + Prometheus |
| Enterprise cost governance | Langfuse + OpenCost + billing APIs |

## ccusage: CLI Usage Reports

### What It Does

- [ccusage](https://ccusage.com) is an open-source CLI tool that:
    - Reads local usage logs from supported coding agent CLIs
    - Estimates USD spend from token counts and model pricing
    - Generates reports across daily, weekly, monthly, and session timeframes
    - Tracks cache creation and cache read tokens separately
    - Exports data in structured JSON format for programmatic use

- It supports a wide range of coding assistants, including:
    - Claude Code, Codex CLI, OpenCode
    - Amp, Droid, Codebuff
    - Hermes Agent, pi-agent, Goose
    - GitHub Copilot CLI, Gemini CLI, Qwen, Kilo
    - And several others

- A key design principle is privacy: all data is read from local logs, and
  nothing is uploaded to external servers

### Installation

- ccusage can be installed globally via npm:

    ```bash
    > npm install -g ccusage
    ```

- Alternatively, you can run it without installation using package runners like
  `bunx`, `pnpm dlx`, or `npx`

- It requires either Bun 1.3+ (recommended) or Node.js as a runtime

### Basic Usage

- Generate a daily usage report with cost breakdown:

    ```bash
    > ccusage daily --breakdown --no-color
    ```

- The output is a terminal table showing:
    - Date and models used
    - Input and output token counts
    - Estimated cost in USD

- Example output (simplified):

    ```text
    ┌──────────┬──────────────────────┬────────────┬──────────┬─────────────┐
    │ Date     │ Models                │      Input │   Output │  Cost (USD) │
    ├──────────┼──────────────────────┼────────────┼──────────┼─────────────┤
    │ 2026-06-10│ - 4.5-haiku          │  8,790,570 │  123,784 │       $4.12 │
    │          │ - 4.6-sonnet          │            │          │             │
    │          │ - deepseek-v4-flash   │            │          │             │
    ├──────────┼──────────────────────┼────────────┼──────────┼─────────────┤
    │ Total    │                      │  8,790,570 │  123,784 │       $4.12 │
    └──────────┴──────────────────────┴────────────┴──────────┴─────────────┘
    ```

- The tool also supports:
    - `ccusage weekly` and `ccusage monthly` for longer timeframes
    - `--breakdown` flag for per-model cost breakdowns
    - `--json` flag for structured data export
    - `--since` flag to specify a start date
    - Offline mode using pre-cached pricing data

### Live Monitoring

- ccusage offers a `blocks --live` command for real-time monitoring of Claude
  Code sessions

- This is particularly useful for keeping an eye on costs during active
  development sessions

## OpenUsage: Terminal Dashboard

### What It Does

- [OpenUsage](https://github.com/janekbaraniewski/openusage) is an open-source,
  terminal-first dashboard for monitoring spend across AI coding tools and API
  platforms

- Unlike ccusage, which focuses on CLI reports, OpenUsage provides a full
  terminal user interface (TUI) with real-time updates

- It auto-detects installed AI tools and API keys on your workstation and shows
  live quota, usage, spend, resets, and rate limits

### Installation

- OpenUsage can be installed via npm:

    ```bash
    > npm install -g openusage
    ```

- It runs entirely locally with zero configuration required

### Key Features

- **Live TUI dashboard**: Real-time display of spend, quotas, rate limits,
  tokens, and per-model breakdowns
    - Supports 17 built-in themes with custom theme file support

- **Auto-detection**: Automatically detects installed AI tools and environment
  variables containing API keys

- **Background daemon**: Continuously collects data into a local SQLite database
  for historical tracking

- **Headless reports**: CLI commands for `daily`, `weekly`, `monthly`,
  `session`, and `blocks` reports in table or JSON format

- **Claude Code integration**:
    - Statusline support showing session cost, burn rate, and context window usage
    - Tmux status bar integration with provider-specific logos

- **Export capabilities**: Export to JSON or CSV, plus Prometheus metrics
  support

- **Supported providers** (34 total):
    - Coding agents and IDEs: Claude Code, Cursor, GitHub Copilot, Codex CLI,
      Gemini CLI, OpenCode, Ollama
    - API platforms: OpenAI, Anthropic, OpenRouter, Groq, Mistral, DeepSeek,
      Grok, Perplexity, Google Gemini API, and many more

### Use Cases

- OpenUsage is ideal for developers who:
    - Want a real-time dashboard they can leave running in a terminal window
    - Use multiple AI tools and want a unified view of all spending
    - Need to track usage across both coding agents and direct API access
    - Want to integrate cost metrics into their existing monitoring
      infrastructure via Prometheus

## Choosing Between ccusage and OpenUsage

- Both tools serve the same general purpose but have different strengths:

    | Aspect               | ccusage                 | OpenUsage                       |
    | :------------------- | :---------------------- | :------------------------------ |
    | Primary interface    | CLI reports             | TUI dashboard + CLI reports     |
    | Real-time monitoring | `blocks --live` command | Live dashboard with daemon      |
    | Model coverage       | Coding assistants focus | 34 providers, including APIs    |
    | Data export          | JSON                    | JSON, CSV, Prometheus           |
    | Auto-detection       | Manual source selection | Auto-detects tools and API keys |
    | Historical tracking  | Per-report queries      | SQLite-backed daemon            |
    | Theme support        | Terminal tables         | 17 built-in themes + custom     |

- **Use ccusage if** you need quick, one-off reports and primarily use coding
  assistant CLIs

- **Use OpenUsage if** you want a persistent dashboard, use multiple AI tools,
  and need real-time visibility into costs

- There is no reason not to install both -- they complement each other well

## Practical Tips for Managing LLM Costs

- Track costs regularly:
    - Run `ccusage daily` at the end of each day
    - Keep OpenUsage running in the background for continuous awareness

- Understand which models drive your costs:
    - Use the `--breakdown` flag to see per-model costs
    - Expensive frontier models (Opus, Sonnet) can dominate spend even with
      minimal usage

- Monitor cache efficiency:
    - Both tools track cache creation and cache read tokens
    - A high cache hit rate reduces costs significantly
    - Claude Code automatically caches prompts, so reusing context across
      sessions helps

- Set mental budgets:
    - Once you know your typical daily spend, you can spot anomalies quickly
    - A sudden spike often indicates an inefficient workflow or a runaway agent
      loop

## Conclusion

- LLM-powered coding assistants are transformative, but their costs need
  visibility

- **ccusage** provides clean, focused CLI reports for tracking usage across
  coding agent CLIs

- **OpenUsage** offers a richer real-time dashboard with broader provider
  coverage and historical data collection

- Both tools are open-source, run locally, and complement each other well

- Installing both gives you a complete picture of your AI tool spending, from
  quick daily reports to continuous monitoring


## OpenRouter Logs

# How to View OpenRouter Logs

## 1. Activity Page (Usage Logs)

Open the OpenRouter dashboard and navigate to **Activity**. There you can view:

- Requests made
- Models used
- Providers used
- API key activity
- Token usage
- Costs

---

## 2. Enable Full Prompt & Response Logging

To view prompts and completions:

1. Open OpenRouter Dashboard.
2. Go to **Settings** → **Observability**.
3. Enable **Input & Output Logging**.
4. Open the **Logs** page.

You will be able to inspect:

- Prompt
- Completion
- Model
- Provider
- Token counts
- Request cost

> Note: Logging only applies to requests made after the feature is enabled.

---

## 3. Retrieve Logs Programmatically

Analytics endpoints require a **Management Key** (not a standard API key).

Example:

```bash
curl https://openrouter.ai/api/v1/analytics/activity \
  -H "Authorization: Bearer YOUR_MANAGEMENT_KEY"
```

Available filters include:

- Date range
- API key
- User
- Endpoint
- Model

---

## 4. Log Usage Per API Request

Every OpenRouter response includes usage information:

```json
{
  "usage": {
    "prompt_tokens": 125,
    "completion_tokens": 342,
    "total_tokens": 467
  }
}
```

Example in Python:

```python
response = client.chat.completions.create(
    model="openai/gpt-4o",
    messages=[
        {"role": "user", "content": "Hello"}
    ]
)

print(response.usage)
```

This allows you to track:

- Prompt tokens
- Completion tokens
- Total tokens
- Cost (when available)
- Cached tokens
- Reasoning tokens (supported models)

---

## Useful Dashboard Pages

- Activity → Usage history
- Logs → Prompts and completions
- Analytics → Cost and token breakdown
- Settings → Observability → Input & Output Logging
