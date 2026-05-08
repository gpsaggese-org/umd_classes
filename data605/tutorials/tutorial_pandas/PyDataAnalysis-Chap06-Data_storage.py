# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.19.0
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %% [markdown]
# # Ipython (DONE)
#
# # Numpy basics (DONE)
#
# # Getting Started with pandas (DONE)
#
# # Data Loading, Storage, and File Formats

# %%
import pandas as pd

# import pandas_datareader.data as web
print(pd.__version__)


# %% [markdown]
# - Indexing
#     - which columns are index
#     - how to get column names
#
# - Type inference and data conversion
#     - user-defined value conversions
#     - custom missing values
#
# - Datetime parsing
#     - combine multiple columns into a single datetime info
#
# - Iterating
#     - support for iterating over chunks of very large files
#
# - Unclean data issues
#     - skip rows, footer, comments, thounsands separated by commas
#
# - reading function
#     - read_csv
#         - allow inference since csv has no data types
#     - read_fwf
#         - fixed width column format (no delimiters)
#     - read_clipboard
#     - read_pickle
#     - read_sql
#         - read result of SQL query (through SQLAlchemy) as pd.DataFrame

# %% [markdown]
# ## CSV

# %% [markdown]
# - read_csv
#     - header=None if there is no header
#     - names: specify column names
#     - index_col: to specify which col is the index
#         - one can specify multiple indices
#     - sep: can be a char (e.g., ",") or a regular expression (e.g., "\s+")
#     - skiprows: to skip certain rows known to store garbage
#     - na_values: allow to specify "sentinel" value for nan
#         - one can specify a dict to specify different nan for different columns
#     - comment
#     - parse_dates: try to parse all column with dates
#     - converters: function to be applied to columns to transform data
#     - nrows: max num of rows to read
#     - skip_footer: skip lines at the end
#     - encoding

# %%
# chunker = pd.read_csv("example/ex6.csv", chunksize=1000)
# returns an object that can be iterated on

# %% [markdown]
# ## JSON
#
# ## Binary format
#
# - obj.to_pickle()
# - pd.read_pickle()
#
# ## HDF5
#
# - HDF = Hierarchical Data Format
# - store large quantities of scientific array data
# - Can store multiple datasets
# - Save metadata
# - Support compression
#
# - fixed format
#     - slower
#     - supports query operations

# %% [markdown]
# ## Web APIs
#
# - Many websites have public API providing data feed via JSON or other format.
# - `requests` library

# %%
import requests

# Get last 30 GitHub issues from pandas.
url = "https://api.github.com/repos/pandas-dev/pandas/issues"

resp = requests.get(url)

# %%
resp

# %%
data = resp.json()

data[0]["title"]

# %% [markdown]
# ## Databases
