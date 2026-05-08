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
#     display_name: Python [default]
#     language: python
#     name: python3
# ---

# %% [markdown] toc="true"
# # Table of Contents
#  <p><div class="lev2 toc-item"><a href="#Imports" data-toc-modified-id="Imports-01"><span class="toc-item-num">0.1&nbsp;&nbsp;</span>Imports</a></div><div class="lev2 toc-item"><a href="#TODOs" data-toc-modified-id="TODOs-02"><span class="toc-item-num">0.2&nbsp;&nbsp;</span>TODOs</a></div><div class="lev1 toc-item"><a href="#Selection" data-toc-modified-id="Selection-1"><span class="toc-item-num">1&nbsp;&nbsp;</span>Selection</a></div><div class="lev2 toc-item"><a href="#.loc,-.iloc,-.ix" data-toc-modified-id=".loc,-.iloc,-.ix-11"><span class="toc-item-num">1.1&nbsp;&nbsp;</span>.loc, .iloc, .ix</a></div><div class="lev2 toc-item"><a href="#Selecting-rows" data-toc-modified-id="Selecting-rows-12"><span class="toc-item-num">1.2&nbsp;&nbsp;</span>Selecting rows</a></div><div class="lev2 toc-item"><a href="#Selecting-columns" data-toc-modified-id="Selecting-columns-13"><span class="toc-item-num">1.3&nbsp;&nbsp;</span>Selecting columns</a></div><div class="lev2 toc-item"><a href="#Find-minimum" data-toc-modified-id="Find-minimum-14"><span class="toc-item-num">1.4&nbsp;&nbsp;</span>Find minimum</a></div><div class="lev1 toc-item"><a href="#Adding-columns" data-toc-modified-id="Adding-columns-2"><span class="toc-item-num">2&nbsp;&nbsp;</span>Adding columns</a></div><div class="lev2 toc-item"><a href="#Using-applymap()" data-toc-modified-id="Using-applymap()-21"><span class="toc-item-num">2.1&nbsp;&nbsp;</span>Using applymap()</a></div><div class="lev1 toc-item"><a href="#MultiIndex" data-toc-modified-id="MultiIndex-3"><span class="toc-item-num">3&nbsp;&nbsp;</span>MultiIndex</a></div><div class="lev2 toc-item"><a href="#Example-with-multi-index-columns" data-toc-modified-id="Example-with-multi-index-columns-31"><span class="toc-item-num">3.1&nbsp;&nbsp;</span>Example with multi-index columns</a></div><div class="lev2 toc-item"><a href="#Simple-example-of-stack()" data-toc-modified-id="Simple-example-of-stack()-32"><span class="toc-item-num">3.2&nbsp;&nbsp;</span>Simple example of stack()</a></div><div class="lev2 toc-item"><a href="#Example-of-multi-index" data-toc-modified-id="Example-of-multi-index-33"><span class="toc-item-num">3.3&nbsp;&nbsp;</span>Example of multi-index</a></div><div class="lev2 toc-item"><a href="#Slicing-using-xs" data-toc-modified-id="Slicing-using-xs-34"><span class="toc-item-num">3.4&nbsp;&nbsp;</span>Slicing using xs</a></div><div class="lev2 toc-item"><a href="#Slicing-with-loc" data-toc-modified-id="Slicing-with-loc-35"><span class="toc-item-num">3.5&nbsp;&nbsp;</span>Slicing with loc</a></div><div class="lev1 toc-item"><a href="#Misc-ops" data-toc-modified-id="Misc-ops-4"><span class="toc-item-num">4&nbsp;&nbsp;</span>Misc ops</a></div><div class="lev2 toc-item"><a href="#Sorting" data-toc-modified-id="Sorting-41"><span class="toc-item-num">4.1&nbsp;&nbsp;</span>Sorting</a></div><div class="lev2 toc-item"><a href="#Levels" data-toc-modified-id="Levels-42"><span class="toc-item-num">4.2&nbsp;&nbsp;</span>Levels</a></div><div class="lev2 toc-item"><a href="#apply(),-applymap()" data-toc-modified-id="apply(),-applymap()-43"><span class="toc-item-num">4.3&nbsp;&nbsp;</span>apply(), applymap()</a></div><div class="lev1 toc-item"><a href="#Missing-data" data-toc-modified-id="Missing-data-5"><span class="toc-item-num">5&nbsp;&nbsp;</span>Missing data</a></div><div class="lev2 toc-item"><a href="#Datetimes" data-toc-modified-id="Datetimes-51"><span class="toc-item-num">5.1&nbsp;&nbsp;</span>Datetimes</a></div><div class="lev2 toc-item"><a href="#Inserting-missing-data" data-toc-modified-id="Inserting-missing-data-52"><span class="toc-item-num">5.2&nbsp;&nbsp;</span>Inserting missing data</a></div><div class="lev2 toc-item"><a href="#Cleaning-nans" data-toc-modified-id="Cleaning-nans-53"><span class="toc-item-num">5.3&nbsp;&nbsp;</span>Cleaning nans</a></div><div class="lev2 toc-item"><a href="#Dropping-axis-with-missing-data." data-toc-modified-id="Dropping-axis-with-missing-data.-54"><span class="toc-item-num">5.4&nbsp;&nbsp;</span>Dropping axis with missing data.</a></div>

# %% [markdown]
# ## Imports

# %%
# !conda info --envs

# %% run_control={"marked": false}
import functools

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# %matplotlib inline

# %%
import notebook_utils

notebook_utils.notebook_config()
# matplotlib.rcParams["figure.figsize"] = (15, 6)

# assert np.__version__ == "1.33.3"
assert pd.__version__ == "0.20.3"
# assert matplotlib.__version__ == "2.0.2"

# %%
from notebook_utils import display_df

from IPython.display import display

# def display_df(df):
#     display(df)

# %% [markdown]
# ## TODOs

# %% [markdown] run_control={"marked": false}
# # Selection

# %% [markdown]
# ## .loc, .iloc, .ix

# %%
# .loc[] vs .ix[] vs .iloc[]

# .ix supports mixed integer and label based access
# It is primarily label based, but will fall back to integer positional access unless the
# corresponding axis is of integer type.
# .ix is the most general and will support any of the inputs in .loc and .iloc.
# .ix also supports floating point label schemes.
# .ix is exceptionally useful when dealing with mixed positional and label based hierachical indexes.

# When an axis is integer based, ONLY label based access and not positional access is supported.
# Thus, in such cases, it’s usually better to be explicit and use .iloc or .loc.

# %%
# TODO: Add examples.

# %%

# %%
df = pd.DataFrame(
    [[1, 2, 0], [3, 4, 0], [5, 6, 0]],
    index="a b c".split(),
    columns="A B C".split(),
)
df

# %%
df.xs("a", axis=0)

# %%
df.xs("A", axis=1)

# %%
df.xs(["A", "B"], axis=1)

# %%
# # ?
df.xs(slice("A", "C"), axis=1)

# %%
df.loc["a"]

# %%
df["A"]

# %%
df.iloc[0]

# %% [markdown]
# ## Selecting rows

# %%
df_orig = pd.DataFrame(
    {"AAA": [4, 5, 6, 7], "BBB": [10, 20, 30, 40], "CCC": [100, 50, -30, -50]}
)

# %%
# These are equivalent syntax.
print(df_orig["AAA"])

print(df_orig.AAA)

# %% run_control={"marked": false}
df = df_orig.copy()
df

# %% run_control={"marked": false}
# Select a piece of the df and overwrite part of it.
# .ix[] is the same as .loc[]
df.ix[df.AAA >= 5, "BBB"] = -1
df

# %%
# Select a piece of the df and overwrite part of it.
df.loc[df.AAA >= 5, "BBB"] = -1
df

# %% run_control={"marked": false}
# Select a piece of df and overwrite it.
df.ix[df.AAA >= 5, ["BBB", "CCC"]] = 555
df

# %% run_control={"marked": false}
# Selecting a df through a mask.
df = df_orig.copy()
mask = pd.DataFrame(
    {"AAA": [True] * 4, "BBB": [False] * 4, "CCC": [True, False] * 2}
)
mask

# %% run_control={"marked": false}
# Filter df using df.where() and a boolean mask.
# nan is returned where the mask is False, the value of the df
# where the mask is True.
df.where(mask)

# %%
# Return a different value for when the mask is False.
df.where(mask, other="high")

# %% run_control={"marked": false}
# Use np.where().

column = df.AAA
np.where(column, "high", "low")

# %% run_control={"marked": false}
# Select rows based on certain criteria.
df = df_orig.copy()

dflow = df[df.AAA <= 5]
dfhigh = df[df.AAA > 5]

print(dflow)
print(dfhigh)

# %% run_control={"marked": false}
mask = (df.BBB < 25) & (df.CCC >= -40)
df.loc[mask, "AAA"]

# %% run_control={"marked": false}
df.loc[mask, "AAA":"BBB"]

# %% run_control={"marked": false}
df[mask][["AAA", "BBB"]]

# %% run_control={"marked": false}
df.ix[(df.CCC - 43.0).abs().argsort()]

# %% run_control={"marked": false}
c1 = df.AAA <= 5.5
c2 = df.BBB == 10.0
c3 = df.CCC > -40.0
cs = [c1, c2, c3]

# %% run_control={"marked": false}
print(functools.reduce(lambda x, y: x & y, cs))

print(c1 & c2 & c3)

# %% run_control={"marked": false}
df.index.isin([0, 2, 4])

# %% run_control={"marked": false}
df = df_orig.copy()
df = pd.DataFrame(
    df.values, index=["foo", "bar", "boo", "kar"], columns=df.columns
)
df

# %% run_control={"marked": false}
df.loc["bar":"kar"]

# %% run_control={"marked": false}
df.ix[0:3]

# %% run_control={"marked": false}
df.iloc[0:3]

# %% [markdown]
# ## Selecting columns

# %%
df = df_orig.copy()
df

# %%
# Select columns where the column-wise column is larger than 30.
col_mask = df.sum() > 30

df.loc[:, col_mask]

# %% [markdown]
# ## Find minimum

# %% run_control={"marked": false}
df = pd.DataFrame(
    {"AAA": [1, 1, 1, 2, 2, 2, 3, 3], "BBB": [2, 1, 3, 4, 5, 1, 2, 3]}
)

df

# %% run_control={"marked": false}
# Find index of the min of one column.
np.argmin(df["BBB"])

# %% run_control={"marked": false}
# Find rows where there is a minimum of df["BBB"].
mask = df["BBB"] == np.min(df["BBB"])
df[mask]

# %% run_control={"marked": false}
df = pd.DataFrame(
    {"AAA": [1, 2, 1, 3], "BBB": [1, 1, 2, 2], "CCC": [2, 1, 3, 1]}
)

# %% run_control={"marked": false}
df["CCC"].idxmin()

# %% run_control={"marked": false}
# groupby AAA values and find the min in BBB.
df.groupby("AAA")["BBB"].idxmin()

# %% run_control={"marked": false}
df.sort_values(by=["BBB", "CCC"])

# %% [markdown] run_control={"marked": false}
# # Adding columns

# %% run_control={"marked": false}
mask = df["AAA"] == np.min(df["AAA"])
df[mask]

# %% [markdown]
# ## Using applymap()
#
# - applymap() applies a function to each element of a df returning another df.

# %% run_control={"marked": false}
# Add new cols converting numbers into greek letters.
df = pd.DataFrame(
    {"AAA": [1, 2, 1, 3], "BBB": [1, 1, 2, 2], "CCC": [2, 1, 3, 1]}
)
print("before=\n", df.to_string())

source_cols = df.columns
new_cols = [str(x) + "_cat" for x in source_cols]
categories = {1: "Alpha", 2: "Beta", 3: "Charlie"}
df[new_cols] = df[source_cols].applymap(lambda x: categories[x])
print("after=\n", df.to_string())

# %% [markdown] run_control={"marked": false}
# # MultiIndex
#
# - A multi-index is just a subset of the cartesian product of values

# %% [markdown]
# ## Example with multi-index columns

# %% run_control={"marked": false}
# This df uses a _ to separate and encode conceptually the multi-index.
# Construct the df by columns.
df = pd.DataFrame(
    {
        "row": [0, 1, 2],
        "One_X": [1.1, 1.1, 1.1],
        "One_Y": [1.2, 1.2, 1.2],
        "Two_X": [1.11, 1.11, 1.11],
        "Two_Y": [1.22, 1.22, 1.22],
    }
)
df = df.set_index("row")
display_df(df)

# print "columns=", df.columns
# print "index=", df.index

# %% run_control={"marked": false}
# Split the columns into tuples.
new_cols = [c.split("_") for c in df.columns]
print("new_cols=", new_cols)
tuples = list(map(tuple, new_cols))
print("tuples=", tuples)

# %% run_control={"marked": false}
# Convert the columns into a multi-index.
midx = pd.MultiIndex.from_tuples(tuples)
print("midx=", midx)
df2 = df.copy()
df2.columns = midx

# Note that the multi-index is represented as a cartesian product of labels
# (each of them associated to an index for uniqueness).
display_df(df2)

# %% run_control={"marked": false}
# stack() moves a level of column multi-indexing to the index (i.e., pivot)
df3 = df2.stack(0)
# print "columns=", df3.columns
# print "index=", df3.index
df3.head()

# %% run_control={"marked": false}
# reset_index() converts a level of indexing into a column.
# Conceptually reset_index() is the opposite of set_index() using multiple columns.
df4 = df3.reset_index(1)

df4

# %%
df5 = df3.reset_index(0)

df5

# %% [markdown]
# ## Simple example of stack()
#
# - stack() simply pivot a level of (possibly hierarchical) column labels, returning
#   a DataFrame or Series having a hierarchical index with a new inner-most level

# %%
# help(pd.DataFrame.stack)

# %%
df = pd.DataFrame([[1, 2], [3, 4]], index=["one", "two"], columns=["a", "b"])
df

# %%
# stack() moves the column index into rows getting a pd.Series.
srs = df.stack()
print("srs=\n", srs)

print("\nindex=\n", srs.index)

# %% [markdown]
# ## Example of multi-index index

# %%
np.random.seed(42)
df = pd.DataFrame(np.random.randint(0, 10, (5, 3)), columns="a b c".split())

display(df)

# %%
tuples = [(x, y) for x in "A B C".split() for y in "O I".split()]
print("tuples=", tuples)

cols = pd.MultiIndex.from_tuples(tuples)
print("cols=", cols)

# %% run_control={"marked": false}
# To get the values of the multi-index columns.
cols.get_values()

# %% run_control={"marked": false}
# Build a df with the given multi-index as columns.
np.random.seed(1000)
df = pd.DataFrame(
    np.random.randn(2, len(cols.get_values())), index="n m".split(), columns=cols
)
df

# %% run_control={"marked": false}
# Broadcast each level.
df.div(df["C"], level=1)

# %% [markdown] run_control={"marked": false}
# ## Slicing using xs

# %% run_control={"marked": false}
coords = [
    ("AA", "one"),
    ("AA", "six"),
    ("BB", "one"),
    ("BB", "two"),
    ("BB", "six"),
]

# Use multi-index index.
index = pd.MultiIndex.from_tuples(coords)

df = pd.DataFrame([11, 22, 33, 44, 55], index, columns=["data"])
df

# %% run_control={"marked": false}
# Select a row with .loc
df.loc["BB"]

# %% run_control={"marked": false}
# Select a row with xs using innermost index.
df.xs("BB", level=0, axis=0)

# %% run_control={"marked": false}
# Select a row using outermost index.
df.xs("six", level=1, axis=0)

# %% [markdown] run_control={"marked": false}
# ## Slicing with loc
#
# loc accepts rows and columns and they can be specified as tuples with slices

# %% run_control={"marked": false}
import itertools

# Build multi-index for index (using Cartesian product).
index = list(
    itertools.product(["Ada", "Quinn", "Violet"], ["Comp", "Math", "Sci"])
)
print("index=", index)

index = pd.MultiIndex.from_tuples(index, names=["Student", "Course"])
print("midx=", index)

# %% run_control={"marked": false}
# Build another multi-index for columns.
columns = list(itertools.product(["Exams", "Labs"], ["I", "II"]))
print("columns=", columns)

# Cols are not named.
cols = pd.MultiIndex.from_tuples(columns)
print("midx=", cols)

# %% run_control={"marked": false}
# Build df.
data = [
    [70 + x + y + (x * y) % 3 for x in range(len(cols))]
    for y in range(len(index))
]
df = pd.DataFrame(data, index, cols)
df

# %% run_control={"marked": false}
# Select one row.
df.loc["Violet"]

# %% run_control={"marked": false}
# Select various cubes.
all_ = slice(None)
df.loc[(all_, "Math"), all_]

# %% run_control={"marked": false}
df.loc[(slice("Ada", "Violet"), "Math"), all_]

# %% run_control={"marked": false}
df.loc[(all_, "Math"), ("Exams")]

# %% run_control={"marked": false}
df.loc[(all_, "Math"), (all_, "II")]

# %% [markdown]
# # Misc ops

# %% [markdown] run_control={"marked": false}
# ## Sorting

# %% run_control={"marked": false}
df

# %% run_control={"marked": false}
# Sort by last columns.
df.sort_values(by=("Labs", "II"), ascending=False)

# %% [markdown] run_control={"marked": false}
# ## Levels

# %% run_control={"marked": false}
np.random.seed(1000)
df = pd.DataFrame(
    {
        "A": "a1 a1 a2 a3".split(),
        "B": "b1 b2 b3 b4".split(),
        "Vals": np.random.rand(4),
    }
)
df

# %% run_control={"marked": false}
# Group by column "A" and sum.
df.groupby("A").sum()

# %% run_control={"marked": false}
# Split by two columns.
df.groupby("A B".split()).sum()

# %% run_control={"marked": false}
df["firstLevel"] = "foo"
df

# %% run_control={"marked": false}
df.set_index("firstLevel")

# %% run_control={"marked": false}
df2 = df.groupby("A B".split()).sum()
df2["firstLevel"] = "foo"
df2 = df2.set_index("firstLevel", append=True)

# reorder_levels() reorder the levels in an index.
df2.reorder_levels(["firstLevel", "A", "B"])

# %% [markdown]
# ## apply(), applymap()

# %%
df = pd.DataFrame([[5, 6, 7], [0, 1, 2]], columns=list("abc"), index=list("12"))
df

# %%
df.applymap(lambda x: x + 1)


# %%
def reduce_(x):
    return sum(x)


display_df(df)
print(df.apply(reduce_, axis=0))
print(df.apply(reduce_, axis=1))

# %% [markdown] run_control={"marked": false}
# # Missing data

# %% run_control={"marked": false}
np.random.seed(1000)

index = "a c e f h".split()
print("index", index)

columns = "one two three".split()
print("cols", columns)

df = pd.DataFrame(np.random.randn(5, 3), index=index, columns=columns)
display_df(df)

# %% run_control={"marked": false}
# Add column.
df["four"] = "bar"
df

# %% run_control={"marked": false}
# Add column function of another column.
df["five"] = df["one"] > 0
df

# %% run_control={"marked": false}
# Add more indices by re-indexing.
df2 = df.reindex("a b c d e f g h".split())
df2

# %% run_control={"marked": false}
df2["one"].isnull()

# %% run_control={"marked": false}
df2["one"].notnull()

# %% run_control={"marked": false}
df2.empty

# %% run_control={"marked": false}
df2.isnull()

# %% run_control={"marked": false}
print("None == None:", None == None)
print("np.nan == np.nan:", np.nan == np.nan)

# %% run_control={"marked": false}
# Can't check for nan-ness by comparison.
# Need to use isnull() or np.isnan().
df2["one"] == np.nan

# %% [markdown] run_control={"marked": false}
# ## Datetimes

# %% run_control={"marked": false}
df2["timestamp"] = pd.Timestamp("20120101")
display_df(df2)
print(df.dtypes)

# %% run_control={"marked": false}
pd.Timestamp("2012-01-01 05:00", tz="EST")

# %% run_control={"marked": false}
# Setting a nan automatically get converted in the proper value depending on the
# column type.
df2.ix[["a", "c", "h"], ["one", "timestamp"]] = np.nan
display_df(df2)
print(df2.dtypes)

# %% run_control={"marked": false}
print("pd.NaT == np.nan:", pd.NaT == np.nan)
print("pd.isnull(pd.NaT):", pd.isnull(pd.NaT))

# %% run_control={"marked": false}
print(df2.dtypes)

print(df2.get_dtype_counts())

# %% [markdown] run_control={"marked": false}
# ## Inserting missing data

# %% run_control={"marked": false}
s = pd.Series([1, 2, 3])
print(s)

# Since it is a container for floats None -> nan.
s.loc[0] = None
print(s)

# %% run_control={"marked": false}
s = pd.Series([1, 2, 3])
print(s)
# writing a char forces a type conversion of the container
s.loc[0] = "a"
print(s)

# %% run_control={"marked": false}
s = pd.Series([1, "a", 3])
s.loc[0] = None
s.loc[2] = np.nan
print(s)

# %% run_control={"marked": false}
np.random.seed(1000)
df = pd.DataFrame(np.random.rand(5, 3))
df

# %% run_control={"marked": false}
df.loc[0:1, 1:2]

# %% run_control={"marked": false}
df.loc[[0, 1], [0, 2]]

# %% run_control={"marked": false}
df.loc[[0, 2], [0, 2]] = np.nan
df

# %% run_control={"marked": false}
df[0] + df[1]

# %% run_control={"marked": false}
# cumsum / cumprod data handles nans as zero for the running sum, but
# propagate nans when are there.
print(df[0][::-1].cumsum())
print(df[0].cumsum())

# %% run_control={"marked": false}
df.cumsum()

# %% run_control={"marked": false}
# nan groups are excluded when grouping.
df.groupby(0).mean()

# %% [markdown] run_control={"marked": false}
# ## Cleaning nans

# %% run_control={"marked": false}
df2

# %% run_control={"marked": false}
# Note that 0 for timestamp is in epochs.
df2.fillna(0)

# %% run_control={"marked": false}
df2.fillna("** MISSING **")

# %% run_control={"marked": false}
df.loc[3, 0] = np.nan
df

# %% run_control={"marked": false}
# Fill forward.
df.fillna(method="pad")

# %% run_control={"marked": false}
# Limit number of fills.
df.fillna(method="pad", limit=1)

# %%
list("ABC")

# %% run_control={"marked": false}
np.random.seed(10)
df = pd.DataFrame(np.random.randn(10, 3), columns=list("ABC"))
df

# %% run_control={"marked": false}
df.iloc[3:5, 0] = np.nan
df.iloc[4:6, 1] = np.nan
df.iloc[5:8, 2] = np.nan
df

# %% run_control={"marked": false}
df.sum()

# %% run_control={"marked": false}
# Count the non-null elements.
df.notnull().sum()

# %% run_control={"marked": false}
# Note that mean counts nans as elements at the denominator.
df.mean()

# %% run_control={"marked": false}
# Skip nans in the count at the denominator.
df.mean() / df.notnull().sum()

# %% run_control={"marked": false}
# Count all elements.
df.mean() / df.shape[0]

# %% run_control={"marked": false}
df

# %% run_control={"marked": false}
# DataFrame.where() is an extension of np.where.
# if pd.notnull(elem) returns 'elem' otherwise 'other'.
df.where(pd.notnull(df), other="missing")

# %% run_control={"marked": false}
# Non-numeric values are still counted at the denominator.
df.mean()

# %% run_control={"marked": false}
# Fill with function of a column, similar to imputation.
df.where(pd.notnull(df), df.mean(), axis=1)

# %% [markdown] run_control={"marked": false}
# ## Dropping axis with missing data.

# %% run_control={"marked": false}
df

# %% run_control={"marked": false}
# Drop rows with any nan.
df.dropna(how="any")

# %% run_control={"marked": false}
# Drop rows with all nans.
df.dropna(how="all")

# %% run_control={"marked": false}
# Drop along columns.
df.dropna(how="any", axis="columns")

# %% run_control={"marked": false}
np.random.seed(1000)
idx = pd.date_range("2000-01-01", periods=30)
ts = pd.Series(np.random.rand(len(idx)) * 2 - 1.0, index=idx)
ts.cumsum().plot(label="without nans")

ts.iloc[10:20] = np.nan
ts.fillna(0).cumsum().plot(label="with nans")
plt.legend(loc="best")

# %% run_control={"marked": false}
ts.count()

# %% run_control={"marked": false}
ts.notnull().sum()

# %% run_control={"marked": false}
ts.cumsum().fillna(method="ffill").plot()

# %% run_control={"marked": false}
ts.cumsum().fillna(method="ffill", limit=3).plot()

# %% run_control={"marked": false}
# Anti-causal fill!
ts.cumsum().fillna(method="bfill", limit=3).plot()

# %% run_control={"marked": false}
# Before cumsum.
ts.plot()

# %% run_control={"marked": false}
ts.interpolate(method="linear").plot()

# %% run_control={"marked": false}
np.random.seed(2)
ser = pd.Series(np.arange(1, 10.1, 0.25) ** 2 + np.random.randn(37))
bad = np.array([4, 13, 14, 15, 16, 17, 18, 20, 29])
ser[bad] = np.nan
ser.plot()
