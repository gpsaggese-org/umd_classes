# Comparison of Data Science Agents

## DS-RouteBench: Preference-Aware Routing via Multi-Dimensional Benchmarking

Empirical study benchmarking 8+ data science agents across real-world tasks,
evaluating them on 6 dimensions (accuracy, code quality, explainability, speed,
cost, robustness). The central contribution is a preference-aware routing
framework that recommends the optimal agent given a user's task and optimization
priorities using Multi-Criteria Decision Making (MCDM).

## Research Questions

- **RQ1:** How do current DS agents compare across accuracy, code quality,
  explainability, speed, cost, and robustness on real-world tasks?
- **RQ2:** Does any single agent dominate across all task categories AND all
  evaluation dimensions simultaneously?
- **RQ3:** Given a user's task and preference weights, which agent is
  Pareto-optimal — and how does the optimal choice shift as preferences change?
- **RQ4:** Does agentic scaffolding (file access, bash, self-correction)
  measurably improve DS task performance over raw LLM prompting?

**Hypothesis:** No single agent dominates across all task categories and all
preference dimensions. The "best" agent changes depending on what the user
optimizes for.

## Agents Under Study

| Agent | Category | Architecture | Local/Cloud |
|-------|----------|-------------|-------------|
| AutoGluon | AutoML | Programmatic | Local |
| PyCaret | AutoML / Low-code | Programmatic | Local |
| ChatGPT Code Interpreter (GPT-4o) | LLM Notebook Agent | Conversational | Cloud |
| Claude Code | Agentic Coding System | Agentic loop (file access, bash, self-correction) | Both |
| Claude API (raw) | Direct LLM | Single-turn prompt → response | Cloud |
| Microsoft AutoGen | Multi-Agent Framework | Collaborative agents | Both |
| smolagents (HuggingFace) | Code-first Agent | Iterative code execution | Both |
| PandasAI | NL→pandas | Lightweight | Local |

**Key comparison pair:** Claude Code vs Claude API Raw — same underlying model
(Sonnet), different architecture. Isolates the measurable value of agentic
scaffolding over raw LLM capability.

## Datasets

| Dataset | Source | Modality | Primary Task |
|---------|--------|----------|-------------|
| Heart Disease UCI | Kaggle / UCI | Tabular | Binary classification |
| NYC Yellow Taxi | NYC TLC | Tabular | Regression |
| Air Quality | OpenAQ API | Time Series | Forecasting |
| Amazon Product Reviews | HuggingFace | NLP/Text | Sentiment classification |
| CIFAR-10 | HuggingFace | Image | Classification (extension) |
| UrbanSound8K | Zenodo | Audio | Classification (extension) |

## Analytics Hierarchy

Tasks span the full analytics maturity model:
- **Descriptive** — "What happened?" (aggregations, summaries)
- **EDA** — "What patterns exist?" (profiling, visualization, anomaly detection)
- **Predictive** — "What will happen?" (classification, regression, forecasting)
- **Prescriptive** — "What should we do?" (optimization, recommendations)

## Evaluation Dimensions (6)

| # | Dimension | Method | Automated? |
|---|-----------|--------|-----------|
| D1 | Accuracy / Quality | F1, RMSE, AUC-ROC (task-specific) | Yes |
| D2 | Code Quality | pylint score + LLM-as-Judge (2 judges, Cohen's κ) | Partial |
| D3 | Explainability | SHAP detection + explanation quality scoring | Partial |
| D4 | Speed | Wall-clock seconds | Yes |
| D5 | Cost | USD = API tokens × price; CodeCarbon for local | Yes |
| D6 | Robustness | CV across runs + adversarial degradation % | Yes |

## Routing Framework (Novel Contribution)

Preference-aware agent selection formalized as Multi-Criteria Decision Making:
- **WSM** (Weighted Sum Model) — baseline
- **TOPSIS** (distance from ideal/anti-ideal solution)
- **PROMETHEE** (pairwise preference flows)

Given user preferences `w = (w_accuracy, w_code, w_explain, w_speed, w_cost,
w_robust)`, the framework recommends the Pareto-optimal agent backed by
empirical benchmark data.

## Project Structure

```
├── configs/                   # Agent, dataset, and task definitions (YAML)
│   ├── agents.yaml
│   ├── datasets.yaml
│   └── tasks.yaml
├── src/                       # Core evaluation engine
│   ├── data_loader.py         # Download + load + profile all datasets
│   ├── task_runner.py         # Orchestrator: agent × task → scored result
│   ├── evaluator.py           # 6-dimension scorer (D1-D6)
│   ├── scorecard.py           # Aggregate results → master comparison table
│   ├── llm_judge.py           # Dual-LLM judge (Claude + GPT-4o) for D2, D3
│   ├── cost_tracker.py        # API cost calculation from token usage
│   ├── smoke_test.py          # Verify all agents work
│   ├── run_benchmark.py       # Batch runner with --pilot mode
│   └── utils.py               # Config loading, timing, I/O helpers
├── agents/                    # Per-agent wrappers (standardized interface)
│   ├── autogluon/run_task.py
│   ├── pycaret/run_task.py
│   ├── chatgpt_ada/run_task.py
│   ├── claude_code/run_task.py
│   ├── claude_api_raw/run_task.py
│   ├── autogen/run_task.py
│   ├── smolagents/run_task.py
│   ├── pandasai/run_task.py
│   └── langgraph/run_task.py
├── data/                      # Downloaded datasets (gitignored)
│   ├── raw/
│   ├── processed/
│   └── adversarial/
├── results/                   # Experiment outputs (gitignored)
└── evaluation/                # Rubrics and ground truth
```

## Quick Start

```bash
# Build and enter the Docker container
> docker_build.sh
> docker_bash.sh

# Inside the container:
# Download all datasets
> python -m src.data_loader --download-all

# Smoke-test all agents
> python -m src.smoke_test

# Run pilot benchmark (3 agents × 2 tasks × 1 run)
> python -m src.run_benchmark --pilot

# Run specific experiment
> python -m src.task_runner --agent autogluon --task HD-PRED-01 --runs 3

# Generate master scorecard with agent rankings
> python -m src.scorecard
```

## Statistical Analysis Plan

- Friedman test + Nemenyi post-hoc (agent ranking significance)
- Critical Difference diagrams (standard in AutoML literature)
- Pareto frontier analysis across preference profiles
- Kendall's τ (routing method agreement across WSM, TOPSIS, PROMETHEE)
- Cohen's κ (inter-rater agreement between LLM judges)

## References

- DSBench: How Far Are Data Science Agents from Becoming Data Science Experts?
  (ICLR 2025) — arxiv.org/abs/2409.07703
- KRAMABENCH: A Benchmark for AI Systems on Data Intensive Tasks (2025) —
  arxiv.org/pdf/2506.06541
- TML-Bench: Benchmark for Data Science Agents on Tabular ML Tasks (2026) —
  arxiv.org/html/2603.05764v1
- DSCodeBench: A Realistic Benchmark for Data Science Code Generation (2025) —
  arxiv.org/abs/2505.15621
- MLE-bench: Evaluating Machine Learning Agents on Machine Learning Engineering
  (OpenAI, 2024) — arxiv.org/abs/2410.07095
- SWE-bench: Can Language Models Resolve Real-World GitHub Issues? —
  swebench.com

---

# Docker Environment

This directory uses a Docker-based development environment template with utility
scripts for Docker operations, Jupyter notebook templates, and shell utilities
for container-based workflows.

## Description of Files

### Project-Specific Files

- `configs/agents.yaml`
  - Agent metadata: IDs, categories, pricing per million tokens, install
    commands, supported modalities

- `configs/datasets.yaml`
  - Dataset metadata: source URLs, download instructions, modality, target
    columns, sample sizes

- `configs/tasks.yaml`
  - 20+ standardized task prompts with analytics level, primary metric, split
    seed, and adversarial flags

- `src/task_runner.py`
  - Core orchestrator: loads task config, dispatches to agent wrapper, captures
    output, scores on 6 dimensions, saves result and scorecard JSON

- `src/evaluator.py`
  - Multi-dimensional evaluator: D1 accuracy (sklearn metrics), D2 code quality
    (pylint), D3 explainability (SHAP detection), D4 speed, D5 cost, D6
    robustness

- `src/data_loader.py`
  - Unified data loader for all 6 datasets with download, profiling, and
    adversarial data generation (label flipping + missing value injection)

- `src/scorecard.py`
  - Aggregates all result JSONs into master comparison CSV with per-dimension
    agent rankings

- `src/llm_judge.py`
  - Dual-LLM judge using Claude + GPT-4o for code quality and explanation
    quality scoring with Cohen's kappa inter-rater agreement

- `agents/*/run_task.py`
  - Standardized wrapper per agent, all sharing the same interface:
    `run(prompt, task_config, work_dir, output_dir) → result dict`

### Template Files

- `bashrc`
  - Bash configuration file enabling `vi` mode for command-line editing

- `copy_docker_files.py`
  - Python script for copying Docker configuration files to destination
    directories

- `docker_build.version.log`
  - Log file containing Python, `pip`, Jupyter, and package version information
    from Docker build

- `docker_cmd.sh`
  - Shell script for executing arbitrary commands inside Docker containers with
    volume mounting

- `docker_jupyter.sh`
  - Shell script for launching Jupyter Lab server inside Docker containers

- `docker_name.sh`
  - Configuration file defining Docker repository and image naming variables

- `Dockerfile`
  - Docker image build configuration with Ubuntu, Python, Jupyter, and project
    dependencies

- `etc_sudoers`
  - Sudoers configuration file granting passwordless sudo access for postgres
    user

- `template_utils.py`
  - Python utility functions supporting tutorial notebooks with data processing
    and modeling helpers

- `template.API.ipynb`
  - Jupyter notebook template for API exploration and library usage examples

- `template.example.ipynb`
  - Jupyter notebook template for project examples and demonstrations

- `utils.sh`
  - Bash utility library with reusable functions for Docker operations
  - Provides centralized argument parsing (`parse_default_args`) for `-h` and
    `-v` flags used by all `docker_*.sh` scripts

## Workflows

- Build and enter the container
  ```bash
  > docker_build.sh
  > docker_bash.sh
  ```

- Start Jupyter
  ```bash
  > docker_jupyter.sh
  # Go to localhost:8888
  ```

- Run experiments inside the container
  ```bash
  > python -m src.task_runner --agent autogluon --task HD-PRED-01 --runs 3
  > python -m src.scorecard
  ```

## Description of Executables

### `docker_bash.sh`
- Launches an interactive bash shell inside a Docker container
- Mounts the current working directory as `/data` inside the container

### `docker_build.sh`
- Builds Docker container images using Docker BuildKit
- Supports single-architecture builds (default) or multi-architecture builds

### `docker_clean.sh`
- Removes all Docker images matching the project's full image name

### `docker_cmd.sh`
- Executes arbitrary commands inside a Docker container
- Mounts current directory as `/data` for accessing project files

### `docker_exec.sh`
- Attaches to an already running Docker container with an interactive bash shell

### `docker_jupyter.sh`
- Launches Jupyter Lab server inside a Docker container
- Supports custom port configuration, vim keybindings, and custom directory
  mounting

### `docker_push.sh`
- Authenticates to Docker registry and pushes the project's Docker image

### `run_jupyter.sh`
- Launches Jupyter Lab server with configurable options