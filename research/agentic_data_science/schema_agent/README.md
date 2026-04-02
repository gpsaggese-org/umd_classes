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
> cd research/agentic_data_science/schema_agent
```

Install the requirements with the command: 
```bash
> pip install -r requirements.txt
```
Set the OPENAI_API_KEY in the .env file: 
```bash 
> export OPENAI_API_KEY=sk-...
```
## Usage

### Basic

```bash
python schema_agent_utils.py data.csv
```

Outputs:
- `data_profile_report.json` — Machine-readable report
- `data_profile_summary.md` — Human-readable summary

### Advanced

```bash
# Multiple files with tags
python schema_agent_utils.py dataset1.csv dataset2.csv --tags sales_2024 inv_q1

# Cost-optimized: only high-null columns
python schema_agent_utils.py data.csv --llm-scope nulls --model gpt-4o-mini

# Custom metrics and output
python schema_agent_utils.py data.csv --metrics mean std max --output-json my_report.json
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

```python
import research.agentic_data_science.schema_agent.schema_agent_utils as radssasau

tag_to_df, stats = radssasau.run_pipeline(
    csv_paths=["data.csv"],
    model="gpt-4o-mini",
    llm_scope="semantic"
)
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