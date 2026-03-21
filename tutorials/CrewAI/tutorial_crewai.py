# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.19.0
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %% [markdown]
# # Crew AI Agents, Local LLMs (Ollama: Qwen, Gemma)

# %%
from crewai import Agent, Task, Crew, Process, LLM

# Local Ollama config
llm = LLM(
    model="ollama/gemma3:latest",
    base_url="http://host.docker.internal:11434",
    temperature=0.2,
)

# Simple agent
summarizer = Agent(
    role="Summarizer",
    goal="Produce concise bullet summaries of provided text.",
    backstory="A careful analyst who only outputs essential points.",
    llm=llm,
    verbose=True,
)

with open("data/sample.txt") as f:
    doc_text = f.read()

task = Task(
    description=(
        f"Summarize the following text into exactly 3 concise bullet points:\n\n{doc_text}"
    ),
    expected_output="Exactly three bullet points.",
    agent=summarizer,
)

crew = Crew(
    agents=[summarizer],
    tasks=[task],
    process=Process.sequential,
    verbose=True,
)

if __name__ == "__main__":
    result = crew.kickoff()
    print("\n=== RESULT ===\n", result)

# %% [markdown]
# ## Agentic EDA Demo

# %%
# main.py
import os
import io
import numpy as np
import pandas as pd
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from crewai import Agent, Task, Crew, Process, LLM
from crewai.tools import tool  # <-- CrewAI's tool decorator

# ---------- demo data ----------
os.makedirs("artifacts", exist_ok=True)
demo_csv_path = "data/sales.csv"
rng = np.random.default_rng(42)
pd.DataFrame(
    {
        "region": (["Northeast", "Midwest", "South", "West"] * 5)[:20],
        "month": list(range(1, 21)),
        "units_sold": rng.integers(10, 500, size=20),
        "price": rng.uniform(5.0, 30.0, size=20).round(2),
    }
).to_csv(demo_csv_path, index=False)


# ---------- CrewAI tools ----------
@tool
def read_head(path: str, n: int = 5) -> str:
    """Preview the top rows of a CSV. Returns a table string."""
    if not os.path.exists(path):
        return f"ERROR: file not found: {path}"
    df = pd.read_csv(path).head(int(n))
    buf = io.StringIO()
    df.to_string(buf, index=False)
    return buf.getvalue()


@tool
def plot_histogram(path: str, column: str, bins: int = 20) -> str:
    """Save a histogram PNG for a numeric column. Returns saved path."""
    if not os.path.exists(path):
        return f"ERROR: file not found: {path}"
    df = pd.read_csv(path)
    if column not in df.columns:
        return f"ERROR: column '{column}' not in CSV"
    values = pd.to_numeric(df[column], errors="coerce").dropna()
    if values.empty:
        return f"ERROR: column '{column}' has no numeric data"
    plt.figure()
    plt.hist(values, bins=int(bins))
    plt.xlabel(column)
    plt.ylabel("Count")
    plt.title(f"Histogram of {column}")
    plt.tight_layout()
    out_path = f"artifacts/hist_{column}.png"
    plt.savefig(out_path, dpi=150)
    plt.close()
    return f"SAVED:{out_path}"


@tool
def groupby_agg(path: str, by: str, metric: str) -> str:
    """Mean(metric) grouped by 'by'. Returns a table string."""
    if not os.path.exists(path):
        return f"ERROR: file not found: {path}"
    df = pd.read_csv(path)
    if by not in df.columns:
        return f"ERROR: group-by column '{by}' not in CSV"
    if metric not in df.columns:
        return f"ERROR: metric column '{metric}' not in CSV"
    grouped = df.groupby(by, dropna=False)[metric].mean().reset_index()
    grouped.rename(columns={metric: f"mean_{metric}"}, inplace=True)
    buf = io.StringIO()
    grouped.to_string(buf, index=False)
    return buf.getvalue()


EDA_TOOLS = [read_head, plot_histogram, groupby_agg]

# ---------- local LLM via Ollama ----------
llm = LLM(
    model="ollama/gemma3:latest",
    base_url="http://host.docker.internal:11434",
    temperature=0,
)

# ---------- agent & task ----------
analyst = Agent(
    role="Data Analyst",
    goal="Perform lightweight EDA on local CSVs via tools and report succinct results.",
    backstory="Prefers precise, minimal outputs. Uses tools exactly as requested.",
    tools=EDA_TOOLS,  # <-- CrewAI tools, not LangChain tools
    llm=llm,
    verbose=True,
)

task = Task(
    description=(
        "1) Use read_head on './data/sales.csv' (n=5).\n"
        "2) Use plot_histogram on column 'price' with 20 bins.\n"
        "3) Use groupby_agg by 'region' on metric 'units_sold'.\n"
        "Return three sections: PREVIEW, HISTOGRAM_PATH, GROUPED_MEANS, "
        "each containing only the respective tool output."
    ),
    expected_output="Sections: PREVIEW, HISTOGRAM_PATH, GROUPED_MEANS.",
    agent=analyst,
)

crew = Crew(
    agents=[analyst], tasks=[task], process=Process.sequential, verbose=True
)

if __name__ == "__main__":
    result = crew.kickoff()
    print("\n=== RESULT ===\n", result)

# %%
