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
# <div class="toc"><ul class="toc-item"><li><span><a href="#Data-wrangling:-join,-combine,-reshape" data-toc-modified-id="Data-wrangling:-join,-combine,-reshape-1"><span class="toc-item-num">1&nbsp;&nbsp;</span>Data wrangling: join, combine, reshape</a></span><ul class="toc-item"><li><span><a href="#Hierarchical-indexing" data-toc-modified-id="Hierarchical-indexing-1.1"><span class="toc-item-num">1.1&nbsp;&nbsp;</span>Hierarchical indexing</a></span><ul class="toc-item"><li><span><a href="#Series-hierarchical-index" data-toc-modified-id="Series-hierarchical-index-1.1.1"><span class="toc-item-num">1.1.1&nbsp;&nbsp;</span>Series hierarchical index</a></span></li><li><span><a href="#Partial-indexing" data-toc-modified-id="Partial-indexing-1.1.2"><span class="toc-item-num">1.1.2&nbsp;&nbsp;</span>Partial indexing</a></span></li><li><span><a href="#Dataframe-hierarchical-index" data-toc-modified-id="Dataframe-hierarchical-index-1.1.3"><span class="toc-item-num">1.1.3&nbsp;&nbsp;</span>Dataframe hierarchical index</a></span></li><li><span><a href="#Reordering-and-sorting-levels" data-toc-modified-id="Reordering-and-sorting-levels-1.1.4"><span class="toc-item-num">1.1.4&nbsp;&nbsp;</span>Reordering and sorting levels</a></span><ul class="toc-item"><li><span><a href="#swaplevel()" data-toc-modified-id="swaplevel()-1.1.4.1"><span class="toc-item-num">1.1.4.1&nbsp;&nbsp;</span>swaplevel()</a></span></li><li><span><a href="#sort_index" data-toc-modified-id="sort_index-1.1.4.2"><span class="toc-item-num">1.1.4.2&nbsp;&nbsp;</span>sort_index</a></span></li></ul></li><li><span><a href="#Summary-statistics-by-level" data-toc-modified-id="Summary-statistics-by-level-1.1.5"><span class="toc-item-num">1.1.5&nbsp;&nbsp;</span>Summary statistics by level</a></span></li><li><span><a href="#Indexing-with-df-columns" data-toc-modified-id="Indexing-with-df-columns-1.1.6"><span class="toc-item-num">1.1.6&nbsp;&nbsp;</span>Indexing with df columns</a></span><ul class="toc-item"><li><span><a href="#DataFrame.set_index()" data-toc-modified-id="DataFrame.set_index()-1.1.6.1"><span class="toc-item-num">1.1.6.1&nbsp;&nbsp;</span>DataFrame.set_index()</a></span></li><li><span><a href="#DataFrame.reset_index()" data-toc-modified-id="DataFrame.reset_index()-1.1.6.2"><span class="toc-item-num">1.1.6.2&nbsp;&nbsp;</span>DataFrame.reset_index()</a></span></li></ul></li></ul></li><li><span><a href="#Combining-and-merging-datasets" data-toc-modified-id="Combining-and-merging-datasets-1.2"><span class="toc-item-num">1.2&nbsp;&nbsp;</span>Combining and merging datasets</a></span><ul class="toc-item"><li><span><a href="#Db-style-df-joins" data-toc-modified-id="Db-style-df-joins-1.2.1"><span class="toc-item-num">1.2.1&nbsp;&nbsp;</span>Db-style df joins</a></span></li><li><span><a href="#Concatenating-along-an-axis" data-toc-modified-id="Concatenating-along-an-axis-1.2.2"><span class="toc-item-num">1.2.2&nbsp;&nbsp;</span>Concatenating along an axis</a></span><ul class="toc-item"><li><span><a href="#Concat-in-numpy" data-toc-modified-id="Concat-in-numpy-1.2.2.1"><span class="toc-item-num">1.2.2.1&nbsp;&nbsp;</span>Concat in numpy</a></span></li><li><span><a href="#Concat-in-pandas-Series" data-toc-modified-id="Concat-in-pandas-Series-1.2.2.2"><span class="toc-item-num">1.2.2.2&nbsp;&nbsp;</span>Concat in pandas Series</a></span></li><li><span><a href="#Concat-in-pandas-DataFrame" data-toc-modified-id="Concat-in-pandas-DataFrame-1.2.2.3"><span class="toc-item-num">1.2.2.3&nbsp;&nbsp;</span>Concat in pandas DataFrame</a></span></li></ul></li><li><span><a href="#Combining-data-with-overlap" data-toc-modified-id="Combining-data-with-overlap-1.2.3"><span class="toc-item-num">1.2.3&nbsp;&nbsp;</span>Combining data with overlap</a></span></li></ul></li><li><span><a href="#Reshaping-and-pivoting" data-toc-modified-id="Reshaping-and-pivoting-1.3"><span class="toc-item-num">1.3&nbsp;&nbsp;</span>Reshaping and pivoting</a></span><ul class="toc-item"><li><span><a href="#Reshaping-with-hierarchical-indexing" data-toc-modified-id="Reshaping-with-hierarchical-indexing-1.3.1"><span class="toc-item-num">1.3.1&nbsp;&nbsp;</span>Reshaping with hierarchical indexing</a></span></li><li><span><a href="#Pivoting-&quot;long&quot;-to-&quot;wide&quot;-format" data-toc-modified-id="Pivoting-&quot;long&quot;-to-&quot;wide&quot;-format-1.3.2"><span class="toc-item-num">1.3.2&nbsp;&nbsp;</span>Pivoting "long" to "wide" format</a></span></li><li><span><a href="#Pivoting-&quot;wide&quot;-to-&quot;long&quot;-format" data-toc-modified-id="Pivoting-&quot;wide&quot;-to-&quot;long&quot;-format-1.3.3"><span class="toc-item-num">1.3.3&nbsp;&nbsp;</span>Pivoting "wide" to "long" format</a></span></li></ul></li></ul></li></ul></div>

# %%
import pandas as pd

# import pandas_datareader.data as web
print(pd.__version__)

import numpy as np


# %% [markdown]
# # Data wrangling: join, combine, reshape
#
# - Data can be spread across files or databases, or in a way that is difficult to analyze

# %% [markdown]
# ## Hierarchical indexing
#
# - Two or more index levels on an axis
#   - Allows to work with high dimensional data using a lower dimensional form
#
# - Used in:
#     - group based operations
#     - pivot tables
#     - reshaping
#
# - INV: A hierarchical index comes when a list of lists is used (instead of a simple list)
# - INV: Indexing in a hierarchical index is like indexing in a np array

# %% [markdown]
# ### Series hierarchical index

# %%
# Create a hierarchical index.
np.random.seed(10)

data = pd.Series(
    np.random.randn(9),
    index=[
        ["a", "a", "a", "b", "b", "c", "c", "d", "d"],
        [1, 2, 3, 1, 3, 1, 2, 2, 3],
    ],
)

data

# %%
# There are
# - "levels", i.e., the values that are used as Cartesian product.
# - the subset of the indices (in the "labels" sets).
# E.g.,
#   (0, 0) -> (a, 1)
#   (0, 1) -> (a, 2)
# ...

data.index

# %% [markdown]
# ### Partial indexing

# %%
# Partial indexing.

# Extract the values for the first level.
data["b"]

# %%
# Range of one level of an index.
data["b":"c"]

# %%
# Select some indices with .loc[list].
data.loc[["b", "d"]]

# %%
# Select all the first level and part of the second.
# Indexing works like a numpy array.
data.loc[:, 2]

# %%
# .unstack() moves one level of indexing into the columns.
data2 = data.unstack()
data2

# %%
# .stack() moves the column index into a hierarchical index.
data2.stack()

# %% [markdown]
# ### Dataframe hierarchical index
#
# - In a df both columns and rows can have a hierarchical index
#     - Note that indices in pandas have "values" and "names"

# %%
frame = pd.DataFrame(np.arange(12).reshape((4, 3)))
frame

# %%
frame = pd.DataFrame(
    np.arange(12).reshape((4, 3)),
    index=["a a b b".split(), list(map(int, "1 2 1 2".split()))],
    columns=["Ohio Ohio Colorado".split(), "Green Red Green".split()],
)
frame

# %%
frame.index

# %%
frame.columns

# %%
# The levels have no name.
print(frame.index.names)
print(frame.columns.names)

# %%
# Assign names to hierarchical levels.
frame.index.names = ["key1", "key2"]
frame.columns.names = ["state", "color"]

frame

# %%
# A multiindex can be created by itself and used.

# %%
print(frame.columns)

# %%
pd.MultiIndex.from_arrays(
    ["Ohio Ohio Colorado".split(), "Green Red Green".split()],
    names=["state", "color"],
)

# %% [markdown]
# ### Reordering and sorting levels

# %% [markdown]
# #### swaplevel()

# %%
# Swap (or reorder) the order of the levels on an axis.
display(frame)
frame.swaplevel("key1", "key2")

# %% [markdown]
# #### sort_index

# %%
# Sort the values in one specific level.
display(frame)
frame2 = frame.sort_index(
    # level=1 is key2
    # level="key2")
    level=1
)

frame2

# %%
frame2.sort_index(
    # level=0 is key1
    level=0
)

# %% [markdown]
# ### Summary statistics by level

# %%
frame

# %%
# frame.sum(level='key2')
frame.sum(level=1)

# %%
frame.sum(level="color", axis=1)

# %% [markdown]
# ### Indexing with df columns
#
# - One can create an index from a column

# %% [markdown]
# #### DataFrame.set_index()

# %%
# Build from dictionary: each (key, value) becomes a column.
# A new index is added.
frame = pd.DataFrame(
    {
        "a": list(range(7)),
        "b": list(range(7, 0, -1)),
        "c": ["one", "one", "one", "two", "two", "two", "two"],
        "d": [0, 1, 2, 0, 1, 2, 3],
    }
)

frame

# %%
# Use two columns as index.
frame2 = frame.set_index(["c", "d"])

frame2

# %% [markdown]
# #### DataFrame.reset_index()

# %%
# Move index to columns and reindex with unique integer
frame2.reset_index()

# %%
# Two reset index creates two indices.
frame2.reset_index().reset_index()

# %% [markdown]
# ## Combining and merging datasets

# %% [markdown]
# ### Db-style df joins

# %%
df1 = pd.DataFrame(
    {"key": ["b", "b", "a", "c", "a", "a", "b"], "data1": list(range(7))}
)
df2 = pd.DataFrame({"key": ["a", "b", "d"], "data2": list(range(3))})

print("df1=")
display(df1)
print("\ndf2=")
display(df2)

# %%
# We want to merge on column "key"
# This is a many-to-one join
# - the data in df1['key'] has multiple rows with 'a', and 'b'
# - df2['key'] has fewer
# so there will be a partial Cartesian product.

# Default values
# - Without specifying the columns to join, the common columns are used
# - inner join

# pd.merge(df1, df2, on='key')
pd.merge(df1, df2)

# %%
# One can specify explicitly different column names
# E.g.,
#   pd.merge(df3, df4, left_on='lkey', right_on='rkey')

# - Indexes are discarded
# - Common columns not used for joined are renamed _x, _y

# %%
# To merge on index
#   pd.merge(df1, df2, left_on='key', right_index=True)

# Merge on index with multi-index
#   pd.merge(df1, df2, left_on=['key1', 'key2'], right_index=True)

# Merge on both indices
#   pd.merge(df1, df2, how='outer', left_index=True, right_index=True)

# %% [markdown]
# ### Concatenating along an axis
#
# - Aka stacking

# %% [markdown]
# #### Concat in numpy

# %%
arr = np.arange(12)
arr

# %%
arr = np.arange(12).reshape((3, 4))
arr

# %%
# Concatenate horizontally.
np.concatenate([arr, arr], axis=1)

# %%
# Concatenate vertically.
np.concatenate([arr, arr], axis=0)

# %% [markdown]
# #### Concat in pandas Series
#
# - Since pandas objects (e.g., Series and DataFrame) have labeled axis
#     - If indexes are different, should do union or intersection of labels?
#     - Should we preserve the labels or discard it after concatenation?

# %%
s1 = pd.Series([0, 1], index="a b".split())
print("s1=\n%s" % s1)

s2 = pd.Series([2, 3, 4], index="c d e".split())
print("\ns2=\n%s" % s2)

s3 = pd.Series([5, 6], index="f g".split())
print("\ns3=\n%s" % s3)

# %%
# Concat series along axis=0 producing another Series with index and values glued together.
pd.concat([s1, s2, s3], axis=0)

# %%
# Concat series along axis=1, does a union of the indices and then merges into a DataFrame
# (sorted outer join).
pd.concat([s1, s2, s3], axis=1, sort=True)

# %%
# concat() can also do a inner join.
pd.concat([s1, s2, s3], axis=1, join="inner")

# %%
# If you want to identify where the data came from, you can use
# a hierarchical axis.
result = pd.concat([s1, s1, s3], keys="one two three".split())
print(result.index)
result

# %%
# Unstack moves a level of hierarchical indexing into columns.
result.unstack()

# %% [markdown]
# #### Concat in pandas DataFrame

# %%
df1 = pd.DataFrame(
    np.arange(6).reshape(3, 2), index=["a", "b", "c"], columns=["one", "two"]
)

print("df1=")
display(df1)

df2 = pd.DataFrame(
    5 + np.arange(4).reshape(2, 2), index=["a", "c"], columns=["three", "four"]
)

print("\ndf2=")
display(df2)

# %%
# Merge using hierarchical columns to track where the data is coming from.
# axis=1 means (columns)
pd.concat([df1, df2], axis=1, keys=["level1", "level2"])

# %%
# "ignore_index=True" is used to ignore the indices and create a new
# numeric index.
pd.concat([df1, df2], axis=0, sort=True)

# %%
pd.concat([df1, df2], axis=0, ignore_index=True, sort=True)

# %%
# Check if there are duplicated indices.
# pd.concat([df1, df2], axis=0, verify_integrity=True)

# %% [markdown]
# ### Combining data with overlap

# %%
# np.where() performs a vectorized if-then-else operation.

a = pd.Series(
    [np.nan, 2.5, np.nan, 3.5, 4.5, np.nan], index="f e d c b a".split()
)
print(a)

# %% run_control={"marked": false}
b = pd.Series(np.arange(len(a), dtype=np.float64), index="f e d c b a".split())
b[-1] = np.nan

display(b)

# %%
# We can combine the two series by using the values from a and
# using values from b to fill the nan.

# Compute the null values
np.where(pd.isnull(a), b, a)

# %%
a.combine_first(b)

# %% [markdown]
# ## Reshaping and pivoting

# %% [markdown]
# ### Reshaping with hierarchical indexing
#
# - `stack`: rotates (or pivots) from the columns to the rows
# - `unstack`: pivots from the rows into the columns

# %%
data = pd.DataFrame(
    np.arange(6).reshape((2, 3)),
    index=pd.Index(["Ohio", "Colorado"], name="state"),
    columns=pd.Index(["one", "two", "three"], name="number"),
)

data

# %%
# Note that it produces a Series since it has a single column.
result = data.stack()

print(type(result))
print(type(result.index))
result

# %%
result.unstack()

# %%
# One can unstack a different level than the innermost.
# Level 0 is the outermost.
result.unstack(0)

# %%
# unstack() can produce nan if there are missing values.
s1 = pd.Series([0, 1, 2, 3], index=["a", "b", "c", "d"])
s2 = pd.Series([4, 5, 6], index=["c", "d", "e"])
# Concat vertically the series.
data2 = pd.concat([s1, s2], keys=["one", "two"])

print("data2=")
print(type(data2))
display(data2)

print("data2.unstack=")
data2.unstack()

# %%
print("data2=")
# gives the original object.
data2.unstack().stack()

# %% [markdown]
# ### Pivoting "long" to "wide" format

# %%
# git clone https://github.com/wesm/pydata-book
data = pd.read_csv("/Users/saggese/src/pydata-book/examples/macrodata.csv")

display(data.head())
display(data.tail())

# %%
# Combine year and quarter to create a kind of time interval type.
periods = pd.PeriodIndex(year=data.year, quarter=data.quarter, name="date")
print(periods)

data2 = data.copy()
data2.index = periods.to_timestamp("D", "end")

# The data is in "wide" format.
data2.head()

# %%
# We need to assign a name to the column otherwise when we "melt"
# the column is not going to have a name.
columns = pd.Index(["realgdp", "infl", "unemp"], name="item")
# Use reindex to extract columns.
data2 = data2.reindex(columns=columns)
print("columns=", columns)

data2.head()

# %%
# Put data in "long" format by moving the three columns into one.
ldata = data2.stack().reset_index()
# Rename column to value.
ldata = ldata.rename(columns={0: "value"})
ldata.head()

# %%
# pivot() allows to transform from long format to wide format.
pivoted = ldata.pivot("date", "item", "value")
pivoted.head()

# %%
# Add another row: now we have an item and 2 values for each.
ldata2 = ldata.copy()
ldata2["value2"] = np.random.randn(len(ldata))

display(ldata2.head())

# %%
# Pivoting when there are multiple values creates a hierarchical
# data frame.
pivoted = ldata2.pivot("date", "item")

pivoted.head()

# %% [markdown]
# ### Pivoting "wide" to "long" format

# %%
# The inverse operation to "pivot" is "melt".

df = pd.DataFrame(
    {
        "key": ["foo", "bar", "baz"],
        "A": [1, 2, 3],
        "B": [4, 5, 6],
        "C": [7, 8, 9],
    }
)

df

# %%
# We need to decide which column is:
# - the variable
# - the value

melted = pd.melt(df, ["key"])

melted
