---
title: "Reducing hllm CLI Import Time"
authors:
  - gpsaggese
date: 2026-06-22
description:
categories:
  - "Python"
  - "Developer Tools"
draft: true
---

TL;DR: Optimize LLM CLI startup time using importtime profiling and lazy imports.

<!-- more -->

python -X importtime -c "import llm"

python -X importtime -c "from llm import get_model"

> time llm -h

real    0m1.290s
user    0m0.869s
sys     0m0.165s
