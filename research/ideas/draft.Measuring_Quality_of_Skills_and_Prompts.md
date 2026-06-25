# Measuring Quality of LLM Skills and Prompts

## Description

- Develop quantitative metrics for prompt/skill quality beyond simple accuracy:
  robustness to paraphrasing, consistency across runs, sensitivity to irrelevant
  context, and instruction-following fidelity
- Build an automated pipeline that runs a skill against a held-out evaluation set
  and reports a quality score, enabling A/B comparison of prompt versions
- Investigate LLM-as-judge approaches: use a stronger model to rate skill outputs
  on dimensions like correctness, completeness, conciseness, and style
- Research how to decompose skill quality into sub-dimensions (e.g., a coding
  skill: does it produce runnable code? Does it follow style conventions? Does it
  handle edge cases?)
- Study how prompt quality degrades as the underlying model is updated or
  replaced, enabling "quality drift" detection
- Explore automated prompt optimization: use quality metrics as a reward signal
  to iteratively improve prompt wording via DSPy-style compilation or
  evolutionary search

## Project Objective

The goal is to build a quality measurement system for LLM skills and prompts that
produces interpretable, reproducible scores across multiple quality dimensions,
enabling data-driven prompt engineering and skill maintenance at scale.

## Dataset Suggestions

1. **MT-Bench**
   - Source: LMSYS
   - URL: https://github.com/lm-sys/FastChat/tree/main/fastchat/llm_judge
   - Content: Multi-turn conversation benchmark with GPT-4 as judge; useful for
     studying LLM-as-judge methodology
   - Access: Public GitHub repository

2. **AlpacaEval**
   - Source: Tatsu Lab (Stanford)
   - URL: https://github.com/tatsu-lab/alpaca_eval
   - Content: Automated evaluation of instruction-following quality using
     win-rate against a reference model
   - Access: Public GitHub repository

3. **DSPy Optimization Traces**
   - Source: Stanford NLP
   - URL: https://github.com/stanfordnlp/dspy
   - Content: Prompt optimization traces showing how prompt rewrites affect
     downstream task performance
   - Access: Public GitHub repository, generate custom traces

## Related Work

- DSPy (Khattab et al., 2023): compiles high-level programs to optimized prompts
  using metrics
- Promptfoo: open-source prompt testing with custom evaluators
- RAGAS: evaluation framework for RAG pipeline quality
- G-Eval (Liu et al., 2023): GPT-4-based evaluation framework with
  chain-of-thought scoring

## Open Questions

- What is the ground truth for prompt quality when task outputs are subjective?
- How many evaluation samples are needed for a statistically reliable quality
  estimate?
- Can quality scores generalize across models, or are they model-specific?
- How do you avoid reward hacking when optimizing prompts against the quality
  metric?
