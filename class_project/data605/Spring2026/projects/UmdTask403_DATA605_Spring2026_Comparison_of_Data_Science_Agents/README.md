# PrismBench: Comparison of Data Science Agents

Course: DATA 605 Big Data Systems, Spring 2026
Instructor: Dr. GP Saggese
Authors: Jay Guwalani (UID 121479709), Anupama Sharma (UID 122241220)

## Overview

PrismBench is an empirical study benchmarking nine data science agents
across three real-world tasks under three prompt protocols, scoring each
run on six evaluation dimensions and feeding the scorecard into a
preference-aware routing framework that uses Multi-Criteria Decision
Making (MCDM) to recommend the optimal agent for a given user
preference profile.

The framework spans 165 main + Protocol C + paradigm-native cells plus
52 adversarial cells, with a theoretical proposition that pins down the
relationship between the three MCDM methods used (WSM, TOPSIS, and
PROMETHEE-II).

## Research questions

- **RQ1.** How do current data science agents compare across accuracy,
  code quality, explainability, speed, cost, and robustness on
  real-world tasks?
- **RQ2.** Does any single agent dominate across all task categories
  AND all evaluation dimensions simultaneously?
- **RQ3.** Given a user's task and preference weights, which agent is
  Pareto-optimal, and how does the optimal choice shift as preferences
  change?
- **RQ4.** Does agentic scaffolding (file access, bash execution,
  iteration) measurably improve data science task performance over raw
  LLM prompting?

**Hypothesis.** No single agent dominates across all task categories
and all preference dimensions. The "best" agent changes depending on
what the user optimizes for. Confirmed empirically: seven of nine
agents are Pareto-optimal in at least one preset weight profile, and
the optimal agent flips between Claude Code, AutoGluon, and LangGraph
across the six routing presets.

## Agents under study (nine total)

| Agent | Category | Architecture | Local / Cloud |
|-------|----------|--------------|---------------|
| AutoGluon | AutoML | Programmatic | Local |
| PyCaret | AutoML / Low-code | Programmatic | Local |
| ChatGPT ADA | Agentic Coding | OpenAI Responses API + code_interpreter | Cloud |
| Claude Code | Agentic Coding | Anthropic CLI agentic loop (file access, bash, iteration) | Both |
| Claude API (raw) | Direct LLM | Single-turn prompt with claude-sonnet-4-6 | Cloud |
| Microsoft AutoGen | Multi-Agent | Collaborative agents over gpt-4o | Both |
| smolagents (HuggingFace) | Code-iterative | Code execution + library authorization | Both |
| PandasAI | Natural language to DataFrame | DataFrame.chat queries | Local |
| LangGraph | Stateful Graph | ReAct-style claude-sonnet-4-6 agent | Both |

**Key comparison pair (RQ4).** Claude Code vs Claude API (raw) on the
same Sonnet model isolates the effect of agentic scaffolding from
model capability. Headline finding: Claude Code achieves accuracy
parity with the raw API at one-tenth the cost and one-third the
carbon (Wilcoxon signed-rank `p_adj = 0.0234` on cost across nine
paired runs).

## Datasets

| Dataset | Source | Modality | Primary task | Status |
|---------|--------|----------|--------------|--------|
| Heart Disease UCI | Kaggle / UCI | Tabular | Binary classification | Used |
| NYC Yellow Taxi | NYC TLC | Tabular | Regression | Used |
| Amazon Product Reviews | HuggingFace | NLP / Text | Sentiment classification | Used |
| Air Quality | OpenAQ API | Time series | Forecasting | Loader implemented |
| CIFAR-10 | HuggingFace | Image | Classification | Configured, not run |
| UrbanSound8K | Zenodo | Audio | Classification | Configured, not run |

The three "Used" datasets back the 81 main-benchmark cells. The
remaining datasets are configured for the cross-modal extension
described in Section 8.2 of the report.

## Six evaluation dimensions

| ID | Dimension | Method | Automated |
|----|-----------|--------|-----------|
| D1 | Accuracy / quality | F1, RMSE, AUC-ROC (task-specific) | Yes |
| D2 | Code quality | pylint static score plus dual-LLM judge | Partial |
| D3 | Explainability | SHAP detection plus dual-LLM judge | Partial |
| D4 | Speed | Wall-clock seconds | Yes |
| D5 | Cost | USD from API tokens times pricing in `agents.yaml` | Yes |
| D5 | Carbon | CodeCarbon for local, per-token literature estimate for cloud | Yes |
| D6 | Robustness | Coefficient of variation of D1 across runs | Yes |

LLM judges (Claude + GPT-4o) score five sub-dimensions for D2 and four
sub-dimensions for D3, with Cohen's kappa reported per cell.

## Routing framework (PrismBench Router)

Three Multi-Criteria Decision Making methods over the per-agent
scorecard:

- **WSM** (Weighted Sum Model): additive baseline.
- **TOPSIS**: distance from ideal and anti-ideal points after weighted
  normalization.
- **PROMETHEE-II**: pairwise net flow with linear preference function.

Six preset weight profiles ship in `src/router.py`: `balanced`,
`accuracy`, `frugal`, `quality`, `green`, `production`. Sensitivity
sweeps locate the weight value at which the top-ranked agent flips,
and a Pareto suite generates six 2D projections covering the
seven-dimensional space.

**Theoretical Proposition 1.** WSM and PROMETHEE-II with the linear
preference function produce identical rankings under min-max
normalized scores. Verified numerically by
`tests/test_router.py::test_proposition_1_wsm_promethee_kendall_tau_one`
on synthetic matrices and by
`tests/test_integration.py::test_proposition_1_holds_on_real_data` on
the committed scorecard, both asserting Kendall `tau = 1.0` across all
six presets.

## Project structure

```
configs/                       Agent, dataset, and task definitions (YAML)
  agents.yaml
  datasets.yaml
  tasks.yaml

src/                           Core engine
  data_loader.py               Dataset download, profiling, adversarial generation
  task_runner.py               Orchestrator: agent x task -> scored result
  evaluator.py                 D1-D6 scoring
  scorecard.py                 Aggregate per-run JSON into master CSV
  llm_judge.py                 Dual-LLM judge (Claude + GPT-4o) for D2 / D3
  cost_tracker.py              D5 USD + carbon kg from token usage
  router.py                    MCDM (WSM, TOPSIS, PROMETHEE-II), sensitivity, Pareto
  stats.py                     Friedman, Nemenyi, Wilcoxon
  protocol_analysis.py         Procrustes, two-way ANOVA, Kendall tau across protocols
  protocol_b_pandasai.py       Protocol B: PandasAI native-paradigm sub-experiment
  protocol_b_langgraph.py      Protocol B: LangGraph ReAct-style sub-experiment
  protocol_b_smolagents.py     Protocol B: smolagents code-iterative sub-experiment
  smoke_test.py                Verify each agent loads and runs
  run_benchmark.py             Batch driver with --pilot mode
  utils.py                     Config loading, paths, timing, I/O

agents/                        Per-agent wrappers (uniform run() interface)
  autogluon/run_task.py
  pycaret/run_task.py
  claude_code/run_task.py
  claude_api_raw/run_task.py
  chatgpt_ada/run_task.py
  autogen/run_task.py
  smolagents/run_task.py
  pandasai/run_task.py
  langgraph/run_task.py

prismbench.API.ipynb           Library tour: load scorecard, normalize,
                               WSM / TOPSIS / PROMETHEE-II, sensitivity, Pareto.
prismbench.example.ipynb       End-to-end walkthrough from one cached
                               (agent, task, run) cell up to a router
                               recommendation.
prismbench_utils.py            Public-API facade re-exporting router and
                               task-runner functions plus convenience helpers.

tests/                         pytest suite (25 tests)
  test_router.py               Unit tests for MCDM math
  test_evaluator.py            Unit tests for D1 / D5 / D6 scoring
  test_integration.py          End-to-end tests against committed scorecard

figures/                       Architecture, roadmap, sensitivity, and
                               Pareto figures (committed)

data/                          Raw and adversarial datasets (gitignored)
results/                       Per-run scorecards and master CSVs (gitignored)
environment/                   .env with API keys (gitignored)
```

## Quick start

Inside the Docker container (`./docker_build.sh && ./docker_bash.sh`):

```bash
# Smoke test all nine agents
python -m src.smoke_test

# Run the test suite (25 tests, ~1 sec)
python -m pytest tests/

# Pilot benchmark: three agents x two tasks x one run
python -m src.run_benchmark --pilot

# Single experiment
python -m src.task_runner --agent autogluon --task HD-PRED-01 --runs 3

# Aggregate per-run results into the master scorecard
python -m src.scorecard

# Run the router under a preset profile
python -m src.router --preset balanced
python -m src.router --preset frugal --all-methods

# Statistical tests on the scorecard
python -m src.stats
python -m src.protocol_analysis
```

To launch Jupyter and open the notebooks:

```bash
./docker_jupyter.sh
# Browse to http://localhost:8888 and open
#   prismbench.API.ipynb
#   prismbench.example.ipynb
```

## Verification and reproducibility

The framework ships with 25 automated tests:

- **9 unit tests for the router** (`tests/test_router.py`) covering
  preset weight sums, min-max normalization, WSM unit-weight recovery,
  TOPSIS dominance, Pareto extraction, and a synthetic numerical proof
  of Theoretical Proposition 1.
- **9 unit tests for the evaluator** (`tests/test_evaluator.py`)
  covering D1 metric correctness on classification, regression,
  string-label round-trip, missing predictions, D6 CV, and the cost /
  carbon helpers.
- **7 integration tests** (`tests/test_integration.py`) that lock down
  headline empirical claims (claude_code F1 on HD-PRED-01 = 0.9017,
  autogluon TAXI RMSE = 0.667, RQ4 cost ratio at least 10x), verify
  Proposition 1 on the real scorecard, and confirm the
  `prismbench_utils` facade matches the underlying router.

Both demonstration notebooks execute top-to-bottom inside the Docker
image. A four-stage smoke check is in `tools/_docker_smoke.py`.

## Statistical analysis

Implemented in `src/stats.py` and `src/protocol_analysis.py`:

- Friedman + Nemenyi post-hoc on D1 normalized primary metric
- Critical Difference cutoffs at `alpha = 0.05`
- Wilcoxon signed-rank pairwise (cost, carbon) with Bonferroni
- Cohen's kappa for inter-rater agreement between LLM judges
- Procrustes disparity, two-way ANOVA, and Kendall tau for the
  multi-protocol cross-comparison

## File descriptions

### Project files

- `configs/agents.yaml`: agent IDs, categories, pricing per million
  tokens, install commands, supported modalities.
- `configs/datasets.yaml`: dataset metadata (source URLs, modality,
  target columns, sample sizes).
- `configs/tasks.yaml`: 20+ standardized task prompts with analytics
  level, primary metric, split seed, adversarial flags.
- `src/task_runner.py`: orchestrator that loads a task config,
  dispatches to the agent wrapper, captures output, scores on six
  dimensions, saves `result.json` and `scorecard.json`.
- `src/router.py`: MCDM scoring functions, sensitivity sweeps, Pareto
  extraction, and the `recommend()` entry point used by the notebooks
  and CLI.
- `src/evaluator.py`: D1 (sklearn metrics), D2 (pylint + LLM judge),
  D3 (SHAP detection + LLM judge), D4 (wall-clock), D5 (cost + carbon),
  D6 (CV across runs).
- `src/llm_judge.py`: dual-LLM judge using Claude and GPT-4o for code
  quality and explanation quality scoring.
- `agents/*/run_task.py`: standardized wrapper per agent, all sharing
  the same interface
  `run(prompt, task_config, work_dir, output_dir) -> dict`.
- `prismbench_utils.py`: public-API facade for notebook and external
  callers.
- `tests/`: pytest suite covering math, scoring, and headline claims.

### Docker template files

- `Dockerfile`: Ubuntu base, Python 3.11, project dependencies via
  `uv pip install -r requirements.txt`.
- `docker_build.sh`: build the image with Docker BuildKit.
- `docker_bash.sh`: launch an interactive shell inside the container,
  with the project mounted at `/data`.
- `docker_jupyter.sh`: launch JupyterLab on port 8888.
- `docker_cmd.sh`: run an arbitrary command inside the container.
- `docker_clean.sh`, `docker_exec.sh`, `docker_push.sh`: image
  cleanup, attach to running container, and registry push.
- `run_jupyter.sh`: project-side launcher that defensively installs
  `jupyterlab` and `ipykernel` into the container venv if missing.
- `etc_sudoers`, `bashrc`, `utils.sh`: shared utility configuration
  inherited from the project template.

## Workflows

Build and enter the container:

```bash
./docker_build.sh
./docker_bash.sh
```

Run experiments inside the container:

```bash
python -m src.task_runner --agent autogluon --task HD-PRED-01 --runs 3
python -m src.scorecard
python -m src.router --preset frugal
python -m pytest tests/
```

Launch JupyterLab inside the container:

```bash
./docker_jupyter.sh
# Open http://localhost:8888 and run prismbench.API.ipynb
```

## References

- Brans, J.-P. (1982). PROMETHEE method for multi-criteria decision making.
- Demsar, J. (2006). Statistical comparisons of classifiers over multiple
  data sets. Journal of Machine Learning Research, 7, 1-30.
- Erickson et al. (2020). AutoGluon-Tabular: Robust and Accurate AutoML
  for Structured Data. arXiv:2003.06505.
- Hwang and Yoon (1981). Multiple Attribute Decision Making (TOPSIS).
- Jimenez et al. (2024). SWE-bench. ICLR.
- Kong et al. (2025). DSBench. ICLR. arXiv:2409.07703.
- Lacoste et al. (2019). Quantifying the Carbon Emissions of Machine
  Learning. NeurIPS Climate Change Workshop.
- Luccioni et al. (2023). Estimating the Carbon Footprint of BLOOM.
  Journal of Machine Learning Research.
- OpenAI (2024). MLE-bench. arXiv:2410.07095.
- Patterson et al. (2021). Carbon Emissions and Large Neural Network
  Training. arXiv:2104.10350.
- Strubell et al. (2019). Energy and Policy Considerations for Deep
  Learning in NLP. ACL.
