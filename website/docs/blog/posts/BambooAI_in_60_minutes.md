---
title: "BambooAI in 60 Minutes"
authors:
  - aver81
  - gpsaggese
date: 2026-03-15
description:
categories:
  - AI Research
---

TL;DR: Learn how to build intelligent data analysis systems with BambooAI in 60
minutes with hands-on examples covering multi-agent workflows, dataframe
analysis, and dynamic code generation.

<!-- more -->

This tutorial's goal is to show you in 60 minutes:

- The basic API of BambooAI (a framework for building multi-agent AI systems
  that can reason over data)
- Concrete examples of using BambooAI to build specialized agents that analyze
  dataframes, generate code, and execute complex workflows

## BambooAI in 30 Seconds
BambooAI is a flexible framework for building intelligent systems made of
multiple collaborating LLM agents that can reason over data and execute code.

Key capabilities:

- **Multi-agent orchestration**: Expert Selector, Code Generator, Error
  Corrector, and other specialized agents working together
- **Data-aware reasoning**: Dataframe Inspector and Analyst agents that
  understand and explore tabular data
- **Dynamic code generation and execution**: Planner and Code Generator agents
  that create and run Python code
- **Multi-provider support**: Works with OpenAI, Anthropic Claude, Google
  Gemini, Mistral, DeepSeek, and more
- **Extensible architecture**: Easy to add custom agents and integrate with
  external tools like Google Search

## Official References
- [BambooAI GitHub Repository](https://github.com/bamboo-ai/bamboo)
- [BambooAI Documentation](https://bamboo-ai.github.io/)

## Tutorial Content
This tutorial includes all the code, notebooks, and Docker containers in the
`tutorials/BambooAI/` directory of the repository.

- **README.md**: Instructions and setup for the tutorial environment
- A Docker system to build and run the environment using our standardized approach
- **bambooai.API.ipynb**: Tutorial notebook focusing on fundamental classes,
  methods, and API configurations
- **bambooai.example.ipynb**: Complete real-world application workflow using
  BambooAI
- **bambooai.example.py**: Stand-alone script version of the example for quick
  reference or automation
- **bambooai_utils.py**: Utility functions required by the example notebooks

## Getting Started with BambooAI APIs
Start here to master the fundamental classes, methods, and basic configurations
of the BambooAI framework.

This notebook covers:

- Core API concepts and agent configuration
- How to initialize and configure specialized agents
- Basic agent interactions and message passing
- Integration with different LLM providers (OpenAI, Gemini, Claude, etc.)

## End-to-End Data Analysis Workflow
Proceed to this notebook to explore a complete, real-world application workflow
using BambooAI.

This example demonstrates:

- **Data exploration**: Using Dataframe Inspector and Analyst agents to
  understand your data
- **Dynamic planning**: Planner agent that decomposes complex analysis tasks
  into steps
- **Code generation**: Code Generator agent that writes and proposes solutions
- **Error handling**: Error Corrector agent that fixes and improves generated
  code
- **Collaborative reasoning**: Multiple agents working together to analyze data
  and produce insights
- **External integrations**: Leveraging Google Search Executor for web-based
  research integrated into workflows
