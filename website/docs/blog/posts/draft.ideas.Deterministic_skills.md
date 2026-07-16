---
title: "Ideas Deterministic Skills"
authors:
  - gpsaggese
date: 2026-01-01
description:
draft: true
categories:
  - AI Research
---

TL;DR: Ideas Deterministic Skills.

<!-- more -->

./helpers/hllm_decorator.py

research/ideas/draft.Language_Mixing_LLM_and_Code.md

- LLM are interpolators and sometimes you don't want to interpolate

- A clear interface to call a skill (maybe it's MCP?) and pass parameters

- E.g., there should be static pass to customize the instructions based on
  the parameters

- See .claude/skills/markdown.summarize/SKILL.md

  ```
  interface(file, num_words, max_header_level)

  if ...
    if max_header_level not specified:
      ...
  ```

- How to express sequence

- Compile these into 
