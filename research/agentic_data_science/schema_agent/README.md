# Data Profiler Agent

Automated statistical profiling and LLM-powered semantic analysis for CSV datasets. Generates column-level insights including semantic meaning, data quality assessment, and testable business hypotheses.

## Features

- **Temporal Detection:** Auto-detects and converts date/datetime columns across multiple formats
- **Statistical Profiling:** Computes numeric summaries, data quality metrics, and categorical distributions
- **LLM Semantic Analysis:** Generates column roles (ID, Feature, Target, Timestamp), semantic meaning, and hypotheses
- **Cost Optimization:** Filter columns before LLM analysis to control token usage and API costs
- **Multi-Format Output:** JSON reports and Markdown summaries

## Setup

Go into the schema folder:
```bash
cd research/agentic_data_science/schema_agent
```

Install the requirements:
```bash
pip install -r requirements.txt
```

Set the `OPENAI_API_KEY` in your environment:
```bash
export OPENAI_API_KEY=sk-...
```

## Module Structure

The agent is split into six focused modules:

| Module | Responsibility |
|--------|---------------|
| `schema_agent_models.py` | Pydantic schemas for type-safe column/dataset insights |
| `schema_agent_loader.py` | CSV loading, type inference, datetime detection |
| `schema_agent_stats.py` | Numeric summaries, quality reports, categorical distributions |
| `schema_agent_llm.py` | Prompt building, OpenAI/LangChain calls, structured output parsing |
| `schema_agent_report.py` | Column profiles, JSON and Markdown export |
| `schema_agent.py` | Pipeline orchestration and CLI entry point |

## Usage

### Basic

```bash
python schema_agent.py data.csv
```

Outputs:
- `data_profile_report.json` — Machine-readable report
- `data_profile_summary.md` — Human-readable summary

### Advanced

```bash
# Multiple files with tags
python schema_agent.py dataset1.csv dataset2.csv --tags sales_2024 inv_q1

# Cost-optimized: only high-null columns
python schema_agent.py data.csv --llm-scope nulls --model gpt-4o-mini

# Custom metrics and output
python schema_agent.py data.csv --metrics mean std max --output-json my_report.json

# LangChain backend
python schema_agent.py data.csv --use-langchain
```

## Command-Line Arguments

| Argument | Default | Description |
|----------|---------|-------------|
| `csv_paths` | Required | One or more CSV file paths |
| `--tags` | File stems | Tags for each CSV (must match count) |
| `--model` | `gpt-4o` | LLM model (`gpt-4o`, `gpt-4o-mini`, etc.) |
| `--llm-scope` | `all` | Which columns to profile: `all`, `semantic`, `nulls` |
| `--metrics` | Subset | Numeric metrics: `mean`, `std`, `min`, `25%`, `50%`, `75%`, `max` |
| `--use-langchain` | False | Use LangChain instead of hllmcli |
| `--output-json` | `data_profile_report.json` | JSON report path |
| `--output-md` | `data_profile_summary.md` | Markdown summary path |

## LLM Scoping

- **`all`** — Every column (highest cost, comprehensive)
- **`semantic`** — Non-numeric columns only
- **`nulls`** — Columns with >5% null values (cost-optimized)

## Python API

### Full pipeline

```python
import schema_agent as radsasag
tag_to_df, stats = radsasag.run_pipeline(
    csv_paths=["data.csv"],
    model="gpt-4o-mini",
    llm_scope="semantic"
)
```

### Individual modules

Each module can be imported independently for exploratory use or testing:

```python
import schema_agent_loader as radsasal
import schema_agent_stats as radsasas
import schema_agent_llm as radsasal
import schema_agent_report as radsasar
```

## Output

### data_profile_report.json
Structured report with column profiles, technical stats, and LLM insights.

### data_profile_summary.md
Formatted table summary: Column | Meaning | Role | Quality | Hypotheses

## Troubleshooting

**API Key Error:**
```bash
export OPENAI_API_KEY=sk-...
```

**Validation Errors:**
- Use `--llm-scope nulls` or `--llm-scope semantic` to reduce columns
- Try `--model gpt-4o-mini`

**Datetime Detection:**
Skipped automatically if no temporal columns detected.