# Schema Agent

The primary purpose of this agent is to analyze dataset schemas, generate column-level hypotheses, and guide the user on how to proceed with planning or exploration.

## Current Files

- **`requirements.txt`** – Lists the Python dependencies required to run the agent.  
- **`schema_agent_utils.py`** – Contains functions for parsing data, computing column statistics, and preparing summaries for LLM-based analysis.
- **global_ecommerce_forecasting.csv** - the dataset used for testing.

## Workflow Overview

1. **Load CSV**
   - Read into a `pandas.DataFrame`.
   - Ensure the DataFrame is non-empty.

2. **Compute Column Stats**
   - Identify column types: numeric, categorical, datetime.
   - Compute per-column statistics:
     - Numeric: min, max, mean, median
     - Categorical: unique count, top values
     - Datetime: ranges, durations
   - Capture null percentages and sample values.

3. **Build LLM Prompt**
   - Serialize per-column stats with optional user context.
   - Designed for efficient LLM input (summaries only, not full data).

4. **LLM Analysis**
   - Generate hypotheses about each column’s meaning.
   - Suggest semantic roles (identifier, timestamp, category, etc.).
   - Highlight data quality concerns.

5. **Merge Results**
   - Combine pandas statistics and LLM output by column name.

6. **Export**
   - Human-readable Markdown tables.
   - JSON output for downstream automation or agents.