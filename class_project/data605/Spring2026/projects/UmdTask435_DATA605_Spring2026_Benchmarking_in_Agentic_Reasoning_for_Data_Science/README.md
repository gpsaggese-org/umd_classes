# Benchmarking-in-Agentic-Reasoning-for-Data-Science-

## Description

This project moves beyond evaluating third-party "black box" tools to engineering a custom, stateful multi-agent system using LangGraph. While standard agents (like ChatGPT) follow linear, one-shot processes, this research builds a cyclic architecture where agents can plan, execute, critique, and self-correct. By developing an internal "Analyst-Reviewer" loop, the project explores the frontier of Agentic Reasoning—testing whether a structured graph of specialized agents can outperform monolithic AI models in reliability, code quality, and handling "adversarial" or "noisy" data science tasks.

| Type                        | Name                                              | Description                                                                                            | Website                                  | Strength                      |
| --------------------------- | ------------------------------------------------- | ------------------------------------------------------------------------------------------------------ | ---------------------------------------- | -------------|
| Notebook agent              | Data Interpreter (ChatGPT Advanced Data Analysis) | Upload data → automatic cleaning, analysis, modeling, and visualization                                | https://chat.openai.com                  | Fast        exploratory analysis     |
| AutoML agent                | AutoGluon                                         | Automated model selection, feature engineering, and tuning pipelines                                   | https://auto.gluon.ai                    | Strong tabular ML performance |
| Multi-agent research system | Microsoft AutoGen                                 | Agents collaborate to plan experiments, write code, and critique results                               | https://github.com/microsoft/autogen     | Research workflows            |
| Workflow agent              | LangGraph                                         | Stateful agent graphs for long-running analytical pipelines                                            | https://langchain-ai.github.io/langgraph | Persistent reasoning loops    |


## Project Objective 

The primary goal is to benchmark the efficacy of stateful multi-agent orchestration against single-agent and AutoML baselines. This project aims to answer:
Can a cyclic multi-agent graph (LangGraph) significantly reduce "hallucinations" and logical errors compared to single-agent assistants?
Does a "Reviewer" node in an agentic workflow produce more production-ready, modular code than one-shot generation?
How do different agent architectures (Linear vs. Cyclic vs. AutoML) recover when faced with corrupted or ambiguous data?

## Dataset Suggestions
- **Heart Disease Prediction (UCI / Kaggle)**
  - Source: Kaggle — UCI Heart Disease Dataset
  - URL: https://www.kaggle.com/datasets/redwankarimsony/heart-disease-uci
  - Contains: 14 clinical features (age, cholesterol, chest pain type, etc.)
    with a binary target indicating presence of heart disease; ~300 rows
  - Access: Free Kaggle account required; download via
    `kaggle datasets download` CLI or direct CSV link; no authentication token
    needed for manual download

- **NYC Yellow Taxi Trip Records**
  - Source: NYC Open Data / TLC Trip Record Data
  - URL: https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page
  - Contains: Pick-up/drop-off timestamps, GPS coordinates, trip distance, fare
    amount, tip, and passenger count; monthly Parquet files (~millions of rows —
    use one month's subset)
  - Access: Fully public, no authentication; direct Parquet download links
    available on the page; recommend sampling 50k rows for laptop use

- **Air Quality — OpenAQ**
  - Source: OpenAQ public API
  - URL: https://api.openaq.org/v2/measurements (REST, no key required for basic
    access)
  - Contains: Real-time and historical PM2.5, PM10, NO₂, O₃, CO readings from
    thousands of global monitoring stations with timestamps and GPS
  - Access: Free tier with no API key; query by city, parameter, and date range;
    returns JSON easily loaded with `requests` + `pandas`

- **Amazon Product Reviews — HuggingFace Datasets**
  - Source: HuggingFace Hub — `McAuley-Lab/Amazon-Reviews-2023`
  - URL: https://huggingface.co/datasets/McAuley-Lab/Amazon-Reviews-2023
  - Contains: Product ratings (1–5 stars), review text, verified purchase flag,
    product category; load a small subset (e.g., "All_Beauty", ~500k rows) with
    `datasets.load_dataset()`
  - Access: Free, no authentication; streamed or downloaded via `datasets`
    library

## Breakdown of the Nodes 

* The Planner (Node 1): Analyzes the dataset schema and sets the strategy (e.g., "This is a classification problem with imbalanced data").
* The EDA Analyst (Node 2): Performs exploratory data analysis, cleans data, and identifies outliers.
* The ML Architect (Node 3): Selects algorithms (e.g., XGBoost, Random Forest), performs hyperparameter tuning, and trains the model.
* The Quality Reviewer (Node 4): Acts as the scientific "guardrail." It inspects the Analyst's results—if Accuracy is high but Recall is low on imbalanced data, it triggers a loop back to the Architect.
* The Report Writer (Node 5): Synthesizes the final journey, documenting both the results and the errors caught/corrected by the Reviewer.

## The Quality Reviewer Rules (Guardrails)

### Code Integrity (The "Compiler" Gate)

* Syntax & Execution: Verified execution in a containerized Python environment.
* Modularity: Checks if code follows DRY (Don't Repeat Yourself) principles and proper function definitions.
* Library Hygiene: Ensures no unauthorized or deprecated packages are used.

### Statistical Logic (The "Data Scientist" Gate)
* Leakage Detection: Scans for target variables accidentally included in the feature set.
* Imbalance Audit: Rejects models that only report "Accuracy" for imbalanced clinical datasets like Heart Disease Prediction.
* Impossible Values: Flags unrealistic data points (e.g., negative taxi fares) for re-cleaning.

### Explainability (The "Researcher" Gate)

* Narrative Consistency: Verifies that the written report matches the generated SHAP/Feature Importance plots.
* Logical Grounding: Rejects generic explanations in favor of data-backed insights.

## Benchmark Comparison Framework

We benchmark the custom LangGraph system against three distinct philosophies of AI:

1. Single-Agent Baseline: ChatGPT (Advanced Data Analysis) – Testing monolithic performance.
2. Conversational Multi-Agent: Microsoft AutoGen – Testing "Group Chat" vs. "Graph-based" logic.
3. Standard AutoML: AutoGluon – Testing AI reasoning vs. mathematical automation.

## Tasks & Implementation

1. Environment Setup: Version pinning for reproducibility across all agents.
2. Graph Construction: Implementing the StateGraph and Conditional Edges in LangGraph.
3. Benchmarking Execution: Running all competitors against Amazon Reviews, NYC Taxi, and Heart Disease datasets.
4. Adversarial Reliability Test: Introducing mislabeled data and extreme outliers to test system resilience.
5. Interpretability Audit: Analyzing the "thought logs" to determine which architecture is most transparent for human researchers.

## Useful Resources
- **AutoGluon Documentation** — Tabular prediction quickstart and benchmarks:
  https://auto.gluon.ai/stable/tutorials/tabular/tabular-quick-start.html
- **Microsoft AutoGen GitHub** — Multi-agent conversation examples including
  data science workflows: https://github.com/microsoft/autogen
- **OpenML Benchmark Suite** — Curated tabular datasets and standardized
  evaluation protocols for AutoML comparison studies:
  https://www.openml.org/search?type=benchmark
