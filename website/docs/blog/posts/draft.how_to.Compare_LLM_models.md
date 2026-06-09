---
title: "How to Compare LLM Models"
draft: true
authors:
  - gpsaggese
date: 2026-06-09
description: Comparison of LLM models using various benchmarks and tools
categories:
  - LLM
  - AI Tools
---

- There are multiple websites that rank AI models

| Site | Address | Best For |
|------|---------|----------|
| Artificial Analysis | https://artificialanalysis.ai | Comparing quality, cost, speed, latency, context window, and benchmarks across models. Great for production model selection. |
| Arena (formerly LM Arena / Chatbot Arena) | https://arena.ai | Human preference rankings based on blind head-to-head evaluations. Useful for measuring real-world user preference. |
| LiveBench | https://livebench.ai | Contamination-resistant benchmarking with frequently refreshed test sets and objective scoring. |
| Hugging Face Open LLM Leaderboard | https://huggingface.co/spaces/open-llm-leaderboard/open_llm_leaderboard | Comparing open-source and open-weight models with transparent evaluation methodology. |
| Vellum LLM Leaderboard | https://www.vellum.ai/llm-leaderboard | Quick comparison of frontier models across reasoning, coding, and general capabilities. |
| LiveCodeBench | https://livecodebench.github.io | Coding-focused benchmarking using fresh programming problems. |
| OpenRouter Rankings | https://openrouter.ai/rankings | Real-world usage, popularity, and provider adoption metrics. |
| Stanford AI Index | https://hai.stanford.edu/ai-index | Industry trends, model ecosystem analysis, and AI market context. |

My favorite are
OpenRouter Rankings and Artificial Analysis

In fact I've put together a small script to allow to compare multiple classes of
models I use on a daily basis for:
- Reasoning 
- Agentic coding
- Text processing

To make decisions on which model is "best" I use an "efficiency" metric like
- Quality (measured as IQ for the task)
- Cost (1/3 weighted between inputs and outputs)
- Speed

- The metrics are:
  - In_Cost, Out_Cost
  - ...

according to the formula

This is my preference
<!-- TODO(ai_gp): Add formula -->


<!-- TODO(ai_gp): Add a link helpers_root/dev_scripts_helpers/llms/openrouter_models_table.py -->

```
> openrouter_models_table.py --models_from_file helpers_root/dev_scripts_helpers/llms/agentic_coding_models.txt
```

<!-- TODO(ai_gp): Convert to markdown -->

```
               AA_Slug                               Permaslug In_Cost Out_Cost Context    Released Coding_IQ General_IQ Speed Week_Toks Month_Toks Efficiency
       claude-opus-4-7      anthropic/claude-4.7-opus-20260416    5.00     25.0      1M  2026-04-16      52.5       57.3  90.0   1504.7B    7671.2B        158
     claude-sonnet-4-6    anthropic/claude-4.6-sonnet-20260217    3.00     15.0      1M  2026-02-17      46.4       44.4  42.5   1849.1B    7614.3B        110
     deepseek-v4-flash     deepseek/deepseek-v4-flash-20260423   0.098    0.197      1M  2026-04-23      38.7       46.5  50.0   4066.7B   13216.4B       6562
       deepseek-v4-pro       deepseek/deepseek-v4-pro-20260423   0.435    0.870      1M  2026-04-23      47.5       51.5  43.0   1861.1B    5387.6B       1565
        gemini-2-5-pro                   google/gemini-2.5-pro    1.25     10.0      1M  2025-06-17      32.0       34.6  84.0         0       9.8B        239
gemini-3-1-pro-preview  google/gemini-3.1-pro-preview-20260219    2.00     12.0      1M  2026-02-19      55.5       57.2  95.0    239.3B    1423.5B        377
      kat-coder-pro-v2                                           0.300     1.20    256K  2026-03-27      45.6       43.8  16.0         0          0        486
             kimi-k2-6           moonshotai/kimi-k2.6-20260420   0.680     3.41    262K  2026-04-20      47.1       53.9  43.0    342.0B    2818.1B        495
                                                                  1.04     6.24    262K  2026-04-26       nan        nan  46.0         0          0        N/A
           qwen3-7-max               qwen/qwen3.7-max-20260520    1.25     3.75      1M  2026-05-21      50.1       56.6  45.0    178.3B     368.3B        451
         mimo-v2-5-pro           xiaomi/mimo-v2.5-pro-20260422   0.435    0.870      1M  2026-04-22      45.5       53.8  29.0    519.0B    2467.9B       1011
```

```
> openrouter_models_table.py --models_from_file helpers_root/dev_scripts_helpers/llms/text_models.txt
```

```
     AA_Slug                         Permaslug In_Cost Out_Cost Context    Released Coding_IQ General_IQ Speed Week_Toks Month_Toks Efficiency
gpt-oss-120b               openai/gpt-oss-120b   0.039    0.180    131K  2025-08-05      28.6       33.3  10.0    424.1B    1746.0B       1306
 gpt-oss-20b                openai/gpt-oss-20b   0.029    0.140    131K  2025-08-05      18.5       24.5  59.0         0      28.3B       6459
                                                 0.080    0.280    131K  2025-04-28       nan        nan  18.0         0          0        N/A
              meta-llama/llama-3.1-8b-instruct   0.100    0.320    131K  2024-12-06       nan        nan  12.0    144.9B     314.8B        N/A
              meta-llama/llama-3.1-8b-instruct   0.020    0.030    131K  2024-07-22       nan        nan  30.0    144.9B     314.8B        N/A
```

```
> openrouter_models_table.py --models_from_file helpers_root/dev_scripts_helpers/llms/reasoning_models.txt
```

```
                   AA_Slug                               Permaslug In_Cost Out_Cost Context    Released Coding_IQ General_IQ  Speed Week_Toks Month_Toks Efficiency
0         claude-3-5-haiku                                           0.800     4.00    200K  2024-11-03      10.7       18.7   38.0         0          0         85
1        claude-sonnet-4-6    anthropic/claude-4.6-sonnet-20260217    3.00     15.0      1M  2026-02-17      46.4       44.4   42.5   1849.1B    7614.3B        110
2          claude-opus-4-7      anthropic/claude-4.7-opus-20260416    5.00     25.0      1M  2026-04-16      52.5       57.3   90.0   1504.7B    7671.2B        158
3          deepseek-v4-pro       deepseek/deepseek-v4-pro-20260423   0.435    0.870      1M  2026-04-23      47.5       51.5   43.0   1861.1B    5387.6B       1565
4           gemini-2-5-pro                   google/gemini-2.5-pro    1.25     10.0      1M  2025-06-17      32.0       34.6   84.0         0       9.8B        239
5   gemini-3-1-pro-preview  google/gemini-3.1-pro-preview-20260219    2.00     12.0      1M  2026-02-19      55.5       57.2   95.0    239.3B    1423.5B        377
6         gemini-3-5-flash        google/gemini-3.5-flash-20260519    1.50     9.00      1M  2026-05-19      45.0       55.3  170.0    492.7B    1371.3B        729
7         kat-coder-pro-v2                                           0.300     1.20    256K  2026-03-27      45.6       43.8   16.0         0          0        486
8                kimi-k2-6           moonshotai/kimi-k2.6-20260420   0.680     3.41    262K  2026-04-20      47.1       53.9   43.0    342.0B    2818.1B        495
9                  gpt-5-2                 openai/gpt-5.1-20251113    1.75     14.0    400K  2025-12-10      48.7       51.3   41.0     67.6B     103.4B        127
10           gpt-5-3-codex           openai/gpt-5.3-codex-20260224    1.75     14.0    400K  2026-02-24      53.1       53.6   41.0     81.4B     337.6B        138
11                 gpt-5-4                 openai/gpt-5.4-20260305    2.50     15.0      1M  2026-03-05      57.2       56.8   42.0    241.0B    1133.9B        137
12                 gpt-5-5                 openai/gpt-5.5-20260423    5.00     30.0      1M  2026-04-24      59.1       60.2   33.0    447.2B    1979.6B         56
13                                                                    1.04     6.24    262K  2026-04-26       nan        nan   46.0         0          0        N/A
14             qwen3-7-max               qwen/qwen3.7-max-20260520    1.25     3.75      1M  2026-05-21      50.1       56.6   45.0    178.3B     368.3B        451
15            qwen3-7-plus                                           0.400     1.60      1M  2026-06-03      46.5       53.3   11.0         0          0        256
16           mimo-v2-5-pro           xiaomi/mimo-v2.5-pro-20260422   0.435    0.870      1M  2026-04-22      45.5       53.8   29.0    519.0B    2467.9B       1011
```

Informally

- I use Claude Opus / Sonnet for reasoning / planning (e.g., plan for a
  refactoring or for architecture)

- Most of my daily workload is writing code and I use 
  Deepseek-v4-flash max effort (which I find slightly slower / worse than Claude Haiku
  4.5, but almost 10x cheaper)

- With this set-up I spend around $10 / day in tokens

- My goal is to write code with AI that has the same, if not higher quality, than
  what I write by hand
  - I review and edit every single line of code generated by the machine (in the
    same way I review and edit PRs from humans)
  - I've measured a productivity increase of ~10x in terms of high-quality LOC
    (I used to write around 150 lines of new code a day, and now it's close to
    3000 LOCs)
