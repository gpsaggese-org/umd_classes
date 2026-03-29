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

# %% [markdown] toc="true"
# <h1>Table of Contents<span class="tocSkip"></span></h1>
# <div class="toc"><ul class="toc-item"><li><span><a href="#Ipython-(DONE)" data-toc-modified-id="Ipython-(DONE)-1"><span class="toc-item-num">1&nbsp;&nbsp;</span>Ipython (DONE)</a></span></li><li><span><a href="#Numpy-basics-(DONE)" data-toc-modified-id="Numpy-basics-(DONE)-2"><span class="toc-item-num">2&nbsp;&nbsp;</span>Numpy basics (DONE)</a></span></li><li><span><a href="#Pandas" data-toc-modified-id="Pandas-3"><span class="toc-item-num">3&nbsp;&nbsp;</span>Pandas</a></span></li><li><span><a href="#Introduction-to-pandas-Data-Structures" data-toc-modified-id="Introduction-to-pandas-Data-Structures-4"><span class="toc-item-num">4&nbsp;&nbsp;</span>Introduction to pandas Data Structures</a></span><ul class="toc-item"><li><span><a href="#Series" data-toc-modified-id="Series-4.1"><span class="toc-item-num">4.1&nbsp;&nbsp;</span>Series</a></span></li><li><span><a href="#Data-frame" data-toc-modified-id="Data-frame-4.2"><span class="toc-item-num">4.2&nbsp;&nbsp;</span>Data frame</a></span></li><li><span><a href="#Index-objects" data-toc-modified-id="Index-objects-4.3"><span class="toc-item-num">4.3&nbsp;&nbsp;</span>Index objects</a></span></li></ul></li><li><span><a href="#Essential-functionality" data-toc-modified-id="Essential-functionality-5"><span class="toc-item-num">5&nbsp;&nbsp;</span>Essential functionality</a></span><ul class="toc-item"><li><span><a href="#Reindexing" data-toc-modified-id="Reindexing-5.1"><span class="toc-item-num">5.1&nbsp;&nbsp;</span>Reindexing</a></span></li><li><span><a href="#Dropping-entries" data-toc-modified-id="Dropping-entries-5.2"><span class="toc-item-num">5.2&nbsp;&nbsp;</span>Dropping entries</a></span></li><li><span><a href="#Indexing,-selection,-filtering" data-toc-modified-id="Indexing,-selection,-filtering-5.3"><span class="toc-item-num">5.3&nbsp;&nbsp;</span>Indexing, selection, filtering</a></span><ul class="toc-item"><li><span><a href="#Series" data-toc-modified-id="Series-5.3.1"><span class="toc-item-num">5.3.1&nbsp;&nbsp;</span>Series</a></span></li><li><span><a href="#DataFrame" data-toc-modified-id="DataFrame-5.3.2"><span class="toc-item-num">5.3.2&nbsp;&nbsp;</span>DataFrame</a></span></li></ul></li><li><span><a href="#Arithmetic-and-data-alignment" data-toc-modified-id="Arithmetic-and-data-alignment-5.4"><span class="toc-item-num">5.4&nbsp;&nbsp;</span>Arithmetic and data alignment</a></span></li><li><span><a href="#Function-application-and-mapping." data-toc-modified-id="Function-application-and-mapping.-5.5"><span class="toc-item-num">5.5&nbsp;&nbsp;</span>Function application and mapping.</a></span><ul class="toc-item"><li><span><a href="#apply()" data-toc-modified-id="apply()-5.5.1"><span class="toc-item-num">5.5.1&nbsp;&nbsp;</span>apply()</a></span></li><li><span><a href="#applymap()" data-toc-modified-id="applymap()-5.5.2"><span class="toc-item-num">5.5.2&nbsp;&nbsp;</span>applymap()</a></span></li></ul></li><li><span><a href="#Sorting-and-ranking" data-toc-modified-id="Sorting-and-ranking-5.6"><span class="toc-item-num">5.6&nbsp;&nbsp;</span>Sorting and ranking</a></span><ul class="toc-item"><li><span><a href="#Series" data-toc-modified-id="Series-5.6.1"><span class="toc-item-num">5.6.1&nbsp;&nbsp;</span>Series</a></span><ul class="toc-item"><li><span><a href="#DataFrame" data-toc-modified-id="DataFrame-5.6.1.1"><span class="toc-item-num">5.6.1.1&nbsp;&nbsp;</span>DataFrame</a></span></li></ul></li></ul></li><li><span><a href="#Axis-indexes-with-duplicate-values." data-toc-modified-id="Axis-indexes-with-duplicate-values.-5.7"><span class="toc-item-num">5.7&nbsp;&nbsp;</span>Axis indexes with duplicate values.</a></span></li><li><span><a href="#Summarizing-and-descriptive-statistics" data-toc-modified-id="Summarizing-and-descriptive-statistics-5.8"><span class="toc-item-num">5.8&nbsp;&nbsp;</span>Summarizing and descriptive statistics</a></span></li><li><span><a href="#Correlation-and-covariance." data-toc-modified-id="Correlation-and-covariance.-5.9"><span class="toc-item-num">5.9&nbsp;&nbsp;</span>Correlation and covariance.</a></span></li><li><span><a href="#Unique-values,-counts,-and-membership" data-toc-modified-id="Unique-values,-counts,-and-membership-5.10"><span class="toc-item-num">5.10&nbsp;&nbsp;</span>Unique values, counts, and membership</a></span></li></ul></li></ul></div>

# %% [markdown]
# # Ipython (DONE)

# %% [markdown]
# # Numpy basics (DONE)

# %% [markdown]
# # Pandas
#
# - high level data structures for data analysis
# - built on top of numpy
#
# - Specs
#     - Labeled axes supporting automatic or explicit data alignement
#     - Time series functionalities
#     - Support data as both time series and non-time series
#     - Handling of missing data
#     - Merge operation like in SQL dbs

# %%
# from pandas import Series, DataFrame

import pandas as pd
import pandas_datareader.data as web

import numpy as np

print(pd.__version__)

import pprint

# %% [markdown]
# # Introduction to pandas Data Structures

# %% [markdown]
# ## Series

# %%
obj = pd.Series([4, 7, -5, 3])

obj

# An index is assigned automatically.

# %%
# Print numpy underlying data struct.
obj.values

# %%
# Index is a special pandas object.
obj.index

# %%
# Assign index explicitly.
obj2 = pd.Series([4, 7, -5, 3], index="d b a c".split())

obj2

# %%
# Access by index.
obj2["a"]

# %%
obj2["d"] = 6

obj2

# %%
# Select slice.
obj2[["c", "a", "d"]]

# %%
# numpy operations preserve index-value link.
obj2

# %%
obj2[obj2 > 0]

# %%
obj2 * 2

# %%
print("b" in obj2)
print("e" in obj2)

# %%
# Build from dict.
sdata = {"Ohio": 35000, "Texas": 71000, "Oregon": 16000, "Utah": 5000}

obj3 = pd.Series(sdata)

print(obj3)

# %%
# Build from dict with explicit index.

states = ["California", "Ohio", "Oregon", "Texas"]
# Note that since data for California doesn't exist.
obj4 = pd.Series(sdata, index=states)

print(obj4)

# %%
obj4.isnull()

# %%
# Data are aligned automatically, merging indices using "outer".
print("obj3=\n", obj3)
print("\nobj4=\n", obj4)

obj3 + obj4

# %%
print(obj4)

# Set name of the series.
obj4.name = "population"
print("\n", obj4)

# Set name of the index.
obj4.index.name = "state"
print("\n", obj4)

# %% [markdown]
# ## Data frame
#
# - Tabular data structure with ordered collection of columns and indexes.
#     - Index and columns are rather symmetric
#     - One can represent higher dimensional data using multi-indexing
#
# - Df can be built from:
#     - 2d ndarray
#     - dict of arrays / lists / tuples
#     - dict of Series / dicts
#     - list of Series / dicts
#     - list of lists / tuples (like the 2d ndarray)
#     - another DataFrame

# %%
# Build from dict of arrays.
data = {
    "state": ["Ohio", "Ohio", "Ohio", "Nevada", "Nevada"],
    "year": [2000, 2001, 2002, 2001, 2002],
    "pop": [1.5, 1.7, 3.6, 2.4, 2.9],
}
frame = pd.DataFrame(data)

print(frame)

# %%
# Change order of columns and set index.
frame2 = pd.DataFrame(
    data,
    columns="year state pop test".split(),
    index="one two three four five".split(),
)

print(frame2)

# %%
# Access row, which is returned as series.
print(frame2.loc["three"])

# %%
# Assigning a column that doesn't exist creates a new column, broadcasting the value.
frame2["debt"] = 16.5

print(frame2)

# %%
# Assign a range.
frame2["debt"] = np.arange(5)

print(frame2)

# %%
# Assign a series.
val = pd.Series([-1.2, -1.5, -1.7], index=["two", "four", "five"])

frame2["debt"] = val

print(frame2)

# %%
# One can use the dot notation besides the index notation.
# print frame2["debt"]
print(frame2.debt)

# %%
frame2["is_Ohio"] = frame2["state"] == "Ohio"

print(frame2)

# %%
# To delete a column.
del frame2["is_Ohio"]

print(frame2)

# %%
# WARNING: this is a view not a copy.
frame2.columns

# %%
# Build a df from a dictionary of dicts.
# Rows are unioned and sorted.
pop = {
    "Nevada": {2001: 2.4, 2002: 2.9},
    "Ohio": {2000: 1.5, 2001: 1.7, 2002: 3.6},
}
print("pop=", pprint.pformat(pop))

frame3 = pd.DataFrame(pop)
print(frame3)

# %%
# Build a df from a dictionary of rows.
frame3 = pd.DataFrame(pop).T

display(frame3)

# %%
# #?pd.Series

# %%
# Build series from dict.
Ohio_srs = pd.Series({2000: 1.5, 2001: 1.7, 2002: 3.6}, name="Ohio")
print(Ohio_srs)

Nevada_srs = pd.Series({2001: 2.4, 2002: 2.9}, name="Nevada")
print(Nevada_srs)

# %%
# Build df from a dict of Series.
frame4 = pd.DataFrame(
    {
        "Ohio": Ohio_srs,
        "Nevada": Nevada_srs,
    }
)

display(frame4)

# %% [markdown]
# ## Index objects
#
# - Index objects hold
#     - axis labels and
#     - metadata (e.g., axis name)
#
# - Indices are specialized for containing different values
#     - Index: axis labels for nparray of Python objects
#     - Int64Index: index for int values
#     - MultiIndex: hierarchical index representing multiple levels of indexing
#         - Similar to an array of tuples
#     - DatetimeIndex: stores ns timestamps (np.datetime64)
#     - PeriodIndex: stores period data, i.e., timespans

# %%
obj = pd.Series(list(range(3)), index="a b c".split())

index = obj.index

index

# %%
# Index objects are immutable.
# raise
#   TypeError: Index does not support mutable operations

# index[1] = 'd'

# %%
index = pd.Index(np.arange(3))

obj2 = pd.Series([1.5, -2.5, 0], index=index)

obj2.index

# %%
# There is also a in function

print(2 in obj2.index)
print(4 in obj2.index)

# %%
index1 = pd.Index(np.arange(3))
print("index1=", index1)
index2 = pd.Index(np.arange(5, 2, -1))
print("index2=", index2)

print("intersection=", index1.intersection(index2))

print("is_monotonic=", index1.is_monotonic, index2.is_monotonic)
print("is_unique=", index1.is_unique, index2.is_unique)

# %% [markdown]
# # Essential functionality

# %% [markdown]
# ## Reindexing
#
# - reindexing = create a new object with data conformed to a new index

# %%
obj = pd.Series([4.5, 7.2, -5.3, 3.6], index="d b a c".split())

obj

# %%
# Re-arrange data according to new index, introducing missing values.
obj2 = obj.reindex("a b c d e".split())

obj2

# %%
obj2 = obj.reindex("a b c d e".split(), fill_value=0)

obj2

# %%
obj3 = pd.Series("b p y".split(), index=[0, 2, 4])
print(obj3)

obj4 = obj3.reindex(list(range(6)), method="ffill")

print(obj4)

# %% [markdown]
# ## Dropping entries

# %%
obj = pd.Series(np.arange(5.0), index="a b c d e".split())
print(obj)

# Drop element by label.
new_obj = obj.drop("c")
print(new_obj)

new_obj = obj.drop("c d".split())
print(new_obj)

# %% [markdown]
# ## Indexing, selection, filtering
#
# - obj[...] works as NumPy array indexing, but you can use also index values instead of integers

# %% [markdown]
# ### Series

# %%
obj = pd.Series(np.arange(4.0), index="a b c d".split())
print(obj)

# %%
# Index by label or index.
print(obj["b"])
print(obj[1])

# %%
# Slicing with int indices or boolean mask.
print(obj[[1, 3]])

print(obj[obj < 2])

# %%
# In slicing note that the endpoint is inclusive.
print(obj["b":"c"])

# %%
obj2 = obj.copy()
obj2["b":"c"] = 5

obj2

# %% [markdown]
# ### DataFrame

# %%
data = pd.DataFrame(
    np.arange(16).reshape((4, 4)),
    index=["Ohio", "Colorado", "Utah", "New York"],
    columns=["one", "two", "three", "four"],
)

print(data)

# %%
# Select one column.
data["two"]

# %%
# Select two columns.
data[["three", "one"]]

# %%
# Note that this int or boolean indexing selects rows.
data[:2]

# %%
data[data["three"] > 5]

# %%
# Select with a boolean "mask" df.
mask = data < 5
print(mask)

data[mask]

# %%
data

# %%
# To select using label indexing.
data.loc["Colorado", ["two", "three"]]

# %%
# This is deprecated.
data.ix[["Colorado", "Utah"], [3, 0, 1]]

# %%
data.iloc[2]

# %%
data.loc[:"Utah", "two"]

# %% [markdown]
# - obj[val]:
#     - select column by value
#     - select rows by bool array / data frame
#
# - obj.loc[val], obj.iloc[val]
#     - select row by label / index
#
# - obj.loc[:, val], obj.iloc[:, val]
#     - select column by label / index
#
# - obj.loc[val1, val2]
#     - select element

# %% [markdown]
# ## Arithmetic and data alignment
#
# - When doing arithmetic between objects with different indexes, the union of the index is peformed

# %%
# Operations between DataFrame and Series imply broadcasting.

df = pd.DataFrame(
    np.arange(12).reshape(4, 3),
    columns=list("bde"),
    index="Utah Ohio Texas Oregon".split(),
)

df

# %%
series = df.iloc[0]

series

# %%
# Broadcasting is by rows.
df - series

# %% [markdown]
# ## Function application and mapping.

# %%
np.random.seed(42)

frame = pd.DataFrame(
    np.random.randn(4, 3),
    columns=list("bde"),
    index=["Utah", "Ohio", "Texas", "Oregon"],
)

frame

# %%
# NumpPy functions work element-wise.
np.abs(frame)

# %% [markdown]
# ### apply()

# %%
# A function returning a single value.
f = lambda x: x.max() - x.min()

# DataFrame.apply() uses the row / column labels to build the resulting
# Series.
frame.apply(f)

# %%
frame.apply(f, axis=1)


# %%
# Using a function that returns a Series of two values.
# DataFrame.apply() uses the row / column labels to build the resulting
# DataFrame.
def f(x):
    return pd.Series([x.min(), x.max()], index="min max".split())


print(frame.apply(f))

print(frame.apply(f, axis=1))

# %% [markdown]
# ### applymap()

# %%
# Element-wise transformation.
format_ = lambda x: "%.2f" % x

print(frame.applymap(format_))

# %% [markdown]
# ## Sorting and ranking

# %% [markdown]
# ### Series

# %%
obj = pd.Series(list(range(4)), index="d a b c".split())

obj

# %%
# Sort by index.
obj.sort_index()

# %%
obj.sort_values()

# %% [markdown]
# #### DataFrame

# %%
frame = pd.DataFrame(
    np.arange(8).reshape((2, 4)),
    index=["three", "one"],
    columns=["d", "a", "b", "c"],
)

frame

# %%
# Sort rows.
display(frame.sort_index())

# Sort columns.
display(frame.sort_index(axis=1))

# %%
frame = pd.DataFrame({"b": [4, 7, -3, 2], "a": [0, 1, 0, 1]})

frame

# %%
# Sort by multiple columns.
frame.sort_values(by=["a", "b"])

# %%
# There are multiple ways of breaking ties.
frame.rank(axis=1)

# %% [markdown]
# ## Axis indexes with duplicate values.

# %%
obj = pd.Series(list(range(5)), index=["a", "a", "b", "b", "c"])

obj

# %%
# Verify that it has multiple indices.
obj.index.is_unique

# %%
# Indexing returns different objects (Series or scalar), depending
# if the values are unique or not.
obj["a"]

# %%
obj["c"]

# %% [markdown]
# ## Summarizing and descriptive statistics
#
# - pd objects have math and stat methods
#     - summary statistics
#     - handle missing data better than np

# %%
df = pd.DataFrame(
    [[1.4, np.nan], [7.1, -4.5], [np.nan, np.nan], [0.75, -1.3]],
    index="a b c d".split(),
    columns="one two".split(),
)

df

# %%
df.sum()

# %%
# NAs are skipped automatically.

# df.sum(axis=1)
df.sum(axis="columns")

# %%
# skipna gives a np behavior.
df.sum(axis=1, skipna=False)

# %%
df.max()

# %%
# df.argmax()

# %%
# Max value per column.
df.idxmax()

# %%
# Accumulate along columns.
df.cumsum()

# %%
print(df.describe())

# %% [markdown]
# ## Correlation and covariance.

# %%
all_data = {
    ticker: web.get_data_yahoo(ticker)
    for ticker in ["AAPL", "IBM", "MSFT", "GOOG"]
}

print(list(all_data.keys()))

print(all_data["GOOG"].head())

# %%
price = pd.DataFrame(
    {ticker: data["Adj Close"] for ticker, data in list(all_data.items())}
)
print(price.head())

volume = pd.DataFrame(
    {ticker: data["Volume"] for ticker, data in list(all_data.items())}
)
print(volume.head())

# %%
returns = price.pct_change()

print(returns.tail())

# %%
returns["MSFT"].corr(returns["IBM"])

# %%
returns["MSFT"].cov(returns["IBM"])

# %%
returns.corr()

# %%
returns.cov()

# %%
returns.corrwith(returns.IBM)

# %% [markdown]
# ## Unique values, counts, and membership

# %%
srs = pd.Series("c a d a a b b c c".split())
srs

# %%
srs.unique()

# %%
pd.value_counts(srs.values, sort=False)

# %%
# isin() vectorized set membership applied to each element of the series.
srs.isin(["b", "c"])

# %%
# Index.get_indexer() allows to establish mapping between them.

to_match = pd.Series("c a b b c a".split())
unique_vals = pd.Series("c b a".split())

pd.Index(unique_vals).get_indexer(to_match)
