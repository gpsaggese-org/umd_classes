# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.19.1
#   kernelspec:
#     display_name: .venv (3.12.3)
#     language: python
#     name: python3
# ---

# %% [markdown]
# # YData-profiling API Overview
#
# This notebook introduces the core API of YData-profiling.
# It shows how to create a profiling report from a pandas DataFrame
# and how to export the report as an HTML file.

# %%
import sys
from pathlib import Path

import pandas as pd
from ydata_profiling import ProfileReport

PROJECT_ROOT = Path.cwd()
SRC_DIR = PROJECT_ROOT / "src"

if str(SRC_DIR) not in sys.path:
    sys.path.append(str(SRC_DIR))

import ydata_profiling_utils as ydputi

# %% [markdown]
# ## 1. Create a simple DataFrame
#
# We start with a small synthetic dataset.
# This makes it easy to understand the basic workflow of YData-profiling.
#

# %%
df_demo = pd.DataFrame(
    {
        "age": [23, 25, 31, 40, 29],
        "income": [50000, 52000, 61000, 73000, 58000],
        "owns_house": [0, 1, 1, 1, 0],
    }
)

df_demo

# %% [markdown]
# ## 2. Generate a profiling report
#
# The `ProfileReport` function creates a summary of the dataset.
# It includes variable types, descriptive statistics, missing values,
# and correlations.

# %%
profile_demo = ProfileReport(
    df_demo,
    title="Simple YData-profiling Demo",
    explorative=True,
)

profile_demo

# %%
output_path = Path("outputs") / "simple_demo_profile.html"
output_path.parent.mkdir(parents=True, exist_ok=True)

profile_demo.to_file(output_path)

print(f"Report saved to: {output_path}")

# %% [markdown]
# ## 3. Use the project wrapper function
#
# The tutorial includes a small wrapper function around `ProfileReport`.
#
# The wrapper keeps report creation consistent across notebooks and makes the example notebook easier to read.

# %%
profile_from_wrapper = ydputi.create_profile_report(
    df_demo,
    title="Simple Profile Report Created with Wrapper",
    explorative=True,
)

profile_from_wrapper

# %% [markdown]
# ## 4. Export a report with the project helper
#
# The helper function saves HTML reports into the project `outputs/` directory.

# %%
wrapper_output_path = ydputi.save_profile_report(
    profile_from_wrapper,
    output_filename="simple_demo_profile_from_wrapper.html",
)

print(f"Report saved to: {wrapper_output_path}")

# %% [markdown]
# ## 5. API workflow summary
#
# The basic YData-profiling workflow is:
#
# 1. Load or create a pandas DataFrame.
# 2. Pass the DataFrame to `ProfileReport`.
# 3. Review the generated report.
# 4. Export the report as an HTML file.
#
# This workflow is used in the example notebook on the Baltimore housing dataset.
