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
# <div class="toc"><ul class="toc-item"><li><ul class="toc-item"><li><span><a href="#Import" data-toc-modified-id="Import-0.1"><span class="toc-item-num">0.1&nbsp;&nbsp;</span>Import</a></span></li></ul></li><li><span><a href="#Grouping" data-toc-modified-id="Grouping-1"><span class="toc-item-num">1&nbsp;&nbsp;</span>Grouping</a></span><ul class="toc-item"><li><span><a href="#Grouping-series" data-toc-modified-id="Grouping-series-1.1"><span class="toc-item-num">1.1&nbsp;&nbsp;</span>Grouping series</a></span></li><li><span><a href="#Grouping-df" data-toc-modified-id="Grouping-df-1.2"><span class="toc-item-num">1.2&nbsp;&nbsp;</span>Grouping df</a></span></li><li><span><a href="#Groupby-+-select" data-toc-modified-id="Groupby-+-select-1.3"><span class="toc-item-num">1.3&nbsp;&nbsp;</span>Groupby + select</a></span></li><li><span><a href="#Groupby-+-plot." data-toc-modified-id="Groupby-+-plot.-1.4"><span class="toc-item-num">1.4&nbsp;&nbsp;</span>Groupby + plot.</a></span></li><li><span><a href="#Groupby-+-aggregation" data-toc-modified-id="Groupby-+-aggregation-1.5"><span class="toc-item-num">1.5&nbsp;&nbsp;</span>Groupby + aggregation</a></span></li><li><span><a href="#groupby-+-transform." data-toc-modified-id="groupby-+-transform.-1.6"><span class="toc-item-num">1.6&nbsp;&nbsp;</span>groupby + transform.</a></span></li><li><span><a href="#Apply-rolling-function-generating-multiple-values." data-toc-modified-id="Apply-rolling-function-generating-multiple-values.-1.7"><span class="toc-item-num">1.7&nbsp;&nbsp;</span>Apply rolling function generating multiple values.</a></span></li><li><span><a href="#groupby-+-filter" data-toc-modified-id="groupby-+-filter-1.8"><span class="toc-item-num">1.8&nbsp;&nbsp;</span>groupby + filter</a></span></li><li><span><a href="#Groupby-+-apply" data-toc-modified-id="Groupby-+-apply-1.9"><span class="toc-item-num">1.9&nbsp;&nbsp;</span>Groupby + apply</a></span></li><li><span><a href="#Grouper" data-toc-modified-id="Grouper-1.10"><span class="toc-item-num">1.10&nbsp;&nbsp;</span>Grouper</a></span></li></ul></li><li><span><a href="#Resample" data-toc-modified-id="Resample-2"><span class="toc-item-num">2&nbsp;&nbsp;</span>Resample</a></span><ul class="toc-item"><li><span><a href="#Downsampling-with-resample()" data-toc-modified-id="Downsampling-with-resample()-2.1"><span class="toc-item-num">2.1&nbsp;&nbsp;</span>Downsampling with resample()</a></span></li><li><span><a href="#Upsampling-with-resample()." data-toc-modified-id="Upsampling-with-resample().-2.2"><span class="toc-item-num">2.2&nbsp;&nbsp;</span>Upsampling with resample().</a></span></li><li><span><a href="#Sparse-resampling" data-toc-modified-id="Sparse-resampling-2.3"><span class="toc-item-num">2.3&nbsp;&nbsp;</span>Sparse resampling</a></span></li><li><span><a href="#Resample-starting-from-a-given-offset-(e.g.,-minutes,-hours,-days)" data-toc-modified-id="Resample-starting-from-a-given-offset-(e.g.,-minutes,-hours,-days)-2.4"><span class="toc-item-num">2.4&nbsp;&nbsp;</span>Resample starting from a given offset (e.g., minutes, hours, days)</a></span></li><li><span><a href="#Resample-dataframes." data-toc-modified-id="Resample-dataframes.-2.5"><span class="toc-item-num">2.5&nbsp;&nbsp;</span>Resample dataframes.</a></span></li><li><span><a href="#Resample-with-asfreq()" data-toc-modified-id="Resample-with-asfreq()-2.6"><span class="toc-item-num">2.6&nbsp;&nbsp;</span>Resample with asfreq()</a></span></li><li><span><a href="#Resample-using-groupby()." data-toc-modified-id="Resample-using-groupby().-2.7"><span class="toc-item-num">2.7&nbsp;&nbsp;</span>Resample using groupby().</a></span></li></ul></li><li><span><a href="#Reshaping" data-toc-modified-id="Reshaping-3"><span class="toc-item-num">3&nbsp;&nbsp;</span>Reshaping</a></span><ul class="toc-item"><li><span><a href="#Reshaping-by-pivoting" data-toc-modified-id="Reshaping-by-pivoting-3.1"><span class="toc-item-num">3.1&nbsp;&nbsp;</span>Reshaping by pivoting</a></span></li><li><span><a href="#Reshaping-by-stacking-/-unstacking" data-toc-modified-id="Reshaping-by-stacking-/-unstacking-3.2"><span class="toc-item-num">3.2&nbsp;&nbsp;</span>Reshaping by stacking / unstacking</a></span></li><li><span><a href="#Reshaping-by-melt." data-toc-modified-id="Reshaping-by-melt.-3.3"><span class="toc-item-num">3.3&nbsp;&nbsp;</span>Reshaping by melt.</a></span></li></ul></li><li><span><a href="#Merge,-join" data-toc-modified-id="Merge,-join-4"><span class="toc-item-num">4&nbsp;&nbsp;</span>Merge, join</a></span><ul class="toc-item"><li><span><a href="#concat()" data-toc-modified-id="concat()-4.1"><span class="toc-item-num">4.1&nbsp;&nbsp;</span>concat()</a></span></li><li><span><a href="#append()" data-toc-modified-id="append()-4.2"><span class="toc-item-num">4.2&nbsp;&nbsp;</span>append()</a></span></li></ul></li><li><span><a href="#Multiindex" data-toc-modified-id="Multiindex-5"><span class="toc-item-num">5&nbsp;&nbsp;</span>Multiindex</a></span><ul class="toc-item"><li><span><a href="#Make-df-multi-level" data-toc-modified-id="Make-df-multi-level-5.1"><span class="toc-item-num">5.1&nbsp;&nbsp;</span>Make df multi-level</a></span></li></ul></li><li><span><a href="#&quot;Align&quot;-data-frames" data-toc-modified-id="&quot;Align&quot;-data-frames-6"><span class="toc-item-num">6&nbsp;&nbsp;</span>"Align" data frames</a></span></li></ul></div>

# %% [markdown]
# ## Import

# %%
import datetime

import numpy as np
import pandas as pd

# %load_ext autoreload
# %autoreload 2

# %matplotlib inline

# %%
import notebook_utils

notebook_utils.notebook_config()
# matplotlib.rcParams["figure.figsize"] = (15, 6)

# %%
from notebook_utils import display_df

from IPython.display import display

# %% [markdown] run_control={"marked": false}
# # Grouping
#
# - groupby = split + apply + combine

# %% run_control={"marked": false}
np.random.seed(10)
df = pd.DataFrame(
    {
        "A": ["foo", "bar", "foo", "bar", "foo", "bar", "foo", "foo"],
        "B": ["one", "one", "two", "three", "two", "two", "one", "three"],
        "C": np.random.randn(8),
        "D": np.random.randn(8),
    }
)
df

# %% run_control={"marked": false}
grouped = df.groupby("A")

print("keys=", list(grouped.groups.keys()))

display_df(grouped.get_group("foo"))

# %% [markdown] run_control={"marked": false}
# ## Grouping series

# %% run_control={"marked": false}
idx = [1, 2, 3, 1, 2, 3]
s = pd.Series([1, 2, 3, 10, 20, 30], idx)
s

# %% run_control={"marked": false}
# groupby() by index values.
grouped = s.groupby(level=0)

print("keys=", list(grouped.groups.keys()))

print("first=\n", grouped.first())
print("last=\n", grouped.last())

# %% [markdown] run_control={"marked": false}
# ## Grouping df

# %% run_control={"marked": false}
df2 = pd.DataFrame({"X": ["B", "B", "A", "A"], "Y": [1, 2, 3, 4]})
df2

# %% run_control={"marked": false}
# Note that groupby() sorts the group keys.
df2.groupby(["X"]).sum()

# %% run_control={"marked": false}
# Observations are kept sorted within each group according to the original df.
df2.groupby("X").get_group("A")

# %% run_control={"marked": false}
# Get a single group.
df2.groupby("X").get_group("B")

# %% run_control={"marked": false}
# Get all groups and mapping.
df2.groupby("X").groups

# %% run_control={"marked": false}
# Group on two columns.
df2.groupby(["X", "Y"]).groups

# %% run_control={"marked": false}
# Iterate over groups.
grouped = df2.groupby("X")

for name, group in grouped:
    print("\nname=", name)
    print(group)

# %% [markdown] run_control={"marked": false}
# ## Groupby + select

# %% run_control={"marked": false}
df_buyer = pd.DataFrame(
    {
        "Branch": "A A A A A A A B".split(),
        "Buyer": "Carl Mark Carl Carl Joe Joe Joe Carl".split(),
        "Quantity": [1, 3, 5, 1, 8, 1, 9, 3],
        "Date": [
            datetime.datetime(2013, 1, 1, 13, 0),
            datetime.datetime(2013, 1, 1, 13, 5),
            datetime.datetime(2013, 10, 1, 20, 0),
            datetime.datetime(2013, 10, 2, 10, 0),
            datetime.datetime(2013, 10, 1, 20, 0),
            datetime.datetime(2013, 10, 2, 10, 0),
            datetime.datetime(2013, 12, 2, 12, 0),
            datetime.datetime(2013, 12, 2, 14, 0),
        ],
    }
)

df_buyer

# %% run_control={"marked": false}
# Group, transform, concat.
df_buyer.groupby("Buyer").head(1)

# %%
# Group, transform, concat.
df_buyer.groupby("Buyer").head(2)

# %% run_control={"marked": false}
df_buyer.groupby("Buyer").nth(2)

# %% [markdown] run_control={"marked": false}
# ## Groupby + plot.

# %% run_control={"marked": false}
_ = df_buyer.groupby("Buyer").boxplot()

# %% [markdown] run_control={"marked": false}
# ## Groupby + aggregation

# %% run_control={"marked": false}
# Group and then aggregate groups with generic function.
display_df(grouped.aggregate(np.sum))
# print grouped.agg(np.sum)

# %% run_control={"marked": false}
# Use pandas function.
grouped.sum()

# %%
df.groupby(["A", "B"]).sum()

# %% run_control={"marked": false}
# Group-by, accumulate, and then convert multi-index into a regular column (opposite of set_index()).
df.groupby(["A", "B"]).sum().reset_index()

# %% run_control={"marked": false}
# Since size() generates a single columns, the result is a multi-index series, instead of a df.
df.groupby(["A", "B"]).size()

# %% run_control={"marked": false}
# Apply multiple functions to each group, producing hierarchical columns.
df.groupby("A").agg([np.sum, np.mean, np.std])

# %% run_control={"marked": false}
# Use names from dict for columns.
# It doesn't seem to work.
if False:
    df.groupby("A").agg({"sum_": np.sum, "mean_": np.mean, "std_": np.std})

# %% [markdown] run_control={"marked": false}
# ## groupby + transform.
#
# - transform() returns an object that is indexed in the same way as the original one
# - so groupby() + transform(), applies a function to each group.

# %% run_control={"marked": false}
np.random.seed(5)
index = pd.date_range("10/1/1999", periods=1100)
ts = pd.Series(np.random.normal(0.05, 2, 1100), index)
ts.cumsum().plot()

# %% run_control={"marked": false}
# Iterate by year.
sorted(ts.groupby(lambda x: x.year).groups.keys())

# %% run_control={"marked": false}
# This is an object computing a rolling window on the data.
rolling = ts.rolling(window=100, min_periods=100)
print(type(rolling))

# %% run_control={"marked": false}
# Compute a rolling window and apply mean: i.e., a rolling mean.
ts2 = rolling.mean()
ts2.plot()

# %% run_control={"marked": false}
# Group by year.
key = lambda x: x.year
grouped = ts2.groupby(key)

# Transform each group by zscoring within the group.
zscore = lambda x: (x - x.mean()) / x.std()
transformed = grouped.transform(zscore)
transformed.plot()

# %%
df

# %%
if False:

    def print_(x):
        print("\n", x)

    df.groupby("A").transform(print_)

# %% [markdown]
# ## Apply rolling function generating multiple values.

# %%
np.random.seed(0)
df = pd.DataFrame(np.random.rand(100, 1))
f = lambda df: df.mean()
# res = pd.rolling_apply(df, 3, f, min_periods=3)
res = df.rolling(min_periods=3, window=3).apply(f)
res.head(10)

# %%
df = pd.DataFrame(np.random.rand(100, 1))
# f = lambda df: [df.mean(), df.std()]
f = lambda df: df.mean()
# res = pd.rolling_apply(df, 3, f, min_periods=3)
res = df.rolling(min_periods=3, window=3).apply(f)
res.head(10)

# %%
# It doesn't seem to work for

# %% [markdown] run_control={"marked": false}
# ## groupby + filter
#
# - We filter a groupby based on their value

# %% run_control={"marked": false}
sf = pd.Series([1, 1, 2, 3, 3, 3])
print(sf.groupby(sf).groups)

# %% run_control={"marked": false}
# Filter groupby by picking only groups with a sum larger.
sf.groupby(sf).filter(lambda x: x.sum() > 2)

# %% [markdown] run_control={"marked": false}
# ## Groupby + apply
#
# - apply() can act as a reducer, transformer or filter

# %%
np.random.seed(10)
df = pd.DataFrame(
    {
        "A": ["foo", "bar", "foo", "bar", "foo", "bar", "foo", "foo"],
        "B": ["one", "one", "two", "three", "two", "two", "one", "three"],
        "C": np.random.randn(8),
        "D": np.random.randn(8),
    }
)
df

# %% run_control={"marked": false}
df

# %% run_control={"marked": false}
# Apply calls describe on each group and concat the results.
df.groupby("A").apply(lambda x: x.describe())

# %% [markdown] run_control={"marked": false}
# ## Grouper
#
# - If one needs more control of grouping, an object pd.Grouper can be used.

# %% run_control={"marked": false}
df_buyer = pd.DataFrame(
    {
        "Branch": "A A A A A A A B".split(),
        "Buyer": "Carl Mark Carl Carl Joe Joe Joe Carl".split(),
        "Quantity": [1, 3, 5, 1, 8, 1, 9, 3],
        "Date": [
            datetime.datetime(2013, 1, 1, 13, 0),
            datetime.datetime(2013, 1, 1, 13, 5),
            datetime.datetime(2013, 10, 1, 20, 0),
            datetime.datetime(2013, 10, 2, 10, 0),
            datetime.datetime(2013, 10, 1, 20, 0),
            datetime.datetime(2013, 10, 2, 10, 0),
            datetime.datetime(2013, 12, 2, 12, 0),
            datetime.datetime(2013, 12, 2, 14, 0),
        ],
    }
)

df_buyer

# %% run_control={"marked": false}
# This is like resampling.
grouper = pd.Grouper(freq="1M", key="Date")

df_tmp = df_buyer.groupby(grouper).sum().dropna()
df_tmp

# %% run_control={"marked": false}
df_tmp2 = df_tmp.copy()
df_tmp2.index += pd.offsets.MonthEnd(1)
df_tmp2

# %% [markdown] run_control={"marked": false}
# TODO: finish

# %% [markdown] run_control={"marked": false}
# # Resample
#
# http://pandas.pydata.org/pandas-docs/stable/timeseries.html#timeseries-resampling

# %% [markdown] run_control={"marked": false}
# ## Downsampling with resample()
#
# - resample() is conceptually a time-based groupby() followed by a transformation on each group
#     - downsample and use reduction method
#     - upsample and interpolate / fill values

# %% run_control={"marked": false}
# Build a df with 100 seconds worth of (random) data.
np.random.seed(1000)
rng = pd.date_range("1/1/2012", periods=100, freq="S")
ts0 = pd.Series(np.random.randint(0, 500, len(rng)), index=rng)
print(ts0.head())
print(ts0.tail())

# %% run_control={"marked": false}
# Summarize in 1 minute intervals.
ts0.resample("1Min").sum()

# %% run_control={"marked": false}
ts0.resample("1Min").max()

# %% run_control={"marked": false}
# 'label' and 'loffset' can be used to manipulate the labels used to mark the intervals.
print(ts0.resample("1Min", label="right").mean())

print(ts0.resample("1Min", label="left").mean())

print(ts0.resample("1Min", label="left", loffset="1s").mean())

# %%
# Resample without summarizing.

# Build a df with 100 seconds worth of data.
np.random.seed(1000)
rng = pd.date_range("1/1/2012", periods=100, freq="2Min")
ts0_1 = pd.Series(np.arange(0, len(rng)) ** 2, index=rng)
ts0_1.plot(style=".-", lw=3)

# pandas 0.14 uses this syntax.
ts1_1 = ts0_1.resample("1H", how="last", closed="right", label="right")
ts1_1.plot(kind="line", style="o--")

# %% [markdown] run_control={"marked": false}
# ## Upsampling with resample().

# %% run_control={"marked": false}
# Get a df with 2 seconds worth of data.
ts[:2]

# %% hide_input=false hide_output=false run_control={"marked": false}
# 'closed' can be used to specify which end of the interval is closed.

# By default intervals are [a, b)
print(ts.resample("1Min").mean().head(10))
print(ts.resample("1Min", closed="left").mean().head(10))

# closed=right => (a, b]
print(ts.resample("1Min", closed="right").mean().head(10))

# %% run_control={"marked": false}
# Resample from seconds to 250 millisecs.
# asfreq() is used to expand the resampler.
ts[:2].resample("250L").asfreq().head(10)

# %% run_control={"marked": false}
ts[:2].resample("250L").ffill().head(10)

# %% run_control={"marked": false}
ts[:2].resample("250L").ffill(limit=2).head(10)

# %% [markdown] run_control={"marked": false}
# ## Sparse resampling
#
# sparse timeseries are ones with fewer points relative to the amount of time

# %% run_control={"marked": false}
rng = pd.date_range("2014-1-1", periods=100, freq="D")
rng += pd.Timedelta("1s")
print(rng[:5])

# %% run_control={"marked": false}
ts3 = pd.Series(list(range(100)), index=rng)
ts3.head()

# %% run_control={"marked": false}
# Upsample the daily ts every 3 mins, getting a very sparse time series.
ts4 = ts3.resample("3T").sum()

# %% run_control={"marked": false}
ts4.index

# %% [markdown] run_control={"marked": false}
# ## Resample starting from a given offset (e.g., minutes, hours, days)

# %% run_control={"marked": false}
# Get a data frame with 60 hours.
idx = pd.date_range("2012-01-01-17", freq="H", periods=60)
ts5 = pd.Series(data=[1] * 60, index=idx)
print(ts5.head())
print(ts5.tail())

# %% run_control={"marked": false}
ts5.resample("D").sum()

# %% run_control={"marked": false}
# By specifying a period in hours and setting the initial hour, one can shift the sampling intervals.
ts5.resample("24H", base=17).sum()

# %% run_control={"marked": false}
# Resample daily starting from 7:45am (= 60 * 24 + 45 = 465).
ts5.resample("1440Min", base=465).sum()

# %% [markdown] run_control={"marked": false}
# ## Resample dataframes.
#
# http://pandas.pydata.org/pandas-docs/stable/timeseries.html#aggregation

# %% run_control={"marked": false}
# Df with 1000 seconds worth of data and multiple columns.
np.random.seed(1000)
df = pd.DataFrame(
    np.random.randn(1000, 3),
    index=pd.date_range("1/1/2012", freq="S", periods=1000),
    columns="A B C".split(" "),
)
print(df.head(2))
print("...")
print(df.tail(2))

# %% run_control={"marked": false}
# Apply the same function to each column.
df.resample("3T").mean()

# %% run_control={"marked": false}
# Specify custom function.
df.resample("3T").agg(lambda x: x.mean())

# %% run_control={"marked": false}
# Apply function to only certain columns.
# NOTE: we tell the resampler which columns to resample instead of selecting columns first.
df.resample("3T")[["A", "B"]].mean()

# %% run_control={"marked": false}
# Apply multiple functions to a single column.
df.resample("3T")["A"].agg([np.sum, np.mean, np.std])

# %% run_control={"marked": false}
# Assign names to columns.
df.resample("3T")["A"].agg({"res1": np.sum, "res2": np.mean})

# %% run_control={"marked": false}
# Apply multiple functions to each column, returning a hierarchical index.
df.resample("3T").agg([np.sum, np.mean])

# %% run_control={"marked": false}
# Specify different multiple functions for each column, returning a hierarchical index.
df.resample("3T").agg({"A": [np.sum, np.mean], "B": [np.mean]})

# %% [markdown] run_control={"marked": false}
# ## Resample with asfreq()

# %% run_control={"marked": false}
np.random.seed(1000)
idx = pd.date_range("1/1/2010", periods=10, freq=pd.offsets.BDay())
ts6 = pd.Series(np.random.rand(idx.shape[0]), index=idx)
ts6

# %% run_control={"marked": false}
# Resample using a certain frequency: from business days to calendar days.
ts6.asfreq(pd.offsets.Day())

# %% [markdown] run_control={"marked": false}
# ## Resample using groupby().

# %% run_control={"marked": false}
# groupby using time intervals and compute a function for each group.
# Note that we keep all dates.
grouper = pd.TimeGrouper("1W")

ts6.groupby(grouper).transform(lambda x: x.mean())

# %% [markdown] run_control={"marked": false}
# http://pandas.pydata.org/pandas-docs/stable/cookbook.html#resampling

# %% [markdown] run_control={"marked": false}
# TODO: finish

# %% [markdown]
# # Reshaping

# %% [markdown]
# ## Reshaping by pivoting

# %%
# Data in "stacked" or "record" format.
# For each date and each variable there is an observation.
idx = pd.date_range(start="20010101", end="20010103").tolist() * 4
np.random.seed(1000)
df = pd.DataFrame(np.random.rand(len(idx), 1), columns="value".split())
df.insert(0, "date", idx)
df.insert(1, "variable", ["A"] * 3 + ["B"] * 3 + ["C"] * 3 + ["D"] * 3)
df.index.name = "date"
print(df)

# %%
# Assume we are interested in observations for variable "A".
df[df["variable"] == "A"]

# %%
# The index is date, the values in "variable" become columns, and the values in "value"
# become the values in the df.
df.pivot(index="date", columns="variable", values="value")

# %%
# If there are more than one value (i.e., more type of observations for a variable)
# one gets multi-index columns.
df["value2"] = df["value"] * 2.0
print(df)

df.pivot(index="date", columns="variable")

# %% [markdown]
# ## Reshaping by stacking / unstacking

# %%
# zip(list1, list2) creates pairs iterating on the lists.
# In other words it iterates on the columns of the stacked versions of the lists,
# effectively transposing.
list(zip("a b c d".split(), "1 2 3 4".split()))

# %%
list(zip("a b c d".split(), "1 2 3 4".split(), "x y z w".split()))

# %%
tuples = [("a", "1"), ("b", "2"), ("c", "3"), ("d", "4")]
print(list(zip(*tuples))[0])
print(list(zip(*tuples))[1])

# %%
tuples = list(
    zip(
        *[
            ["bar", "bar", "baz", "baz", "foo", "foo", "qux", "qux"],
            ["one", "two", "one", "two", "one", "two", "one", "two"],
        ]
    )
)
print(tuples)
index = pd.MultiIndex.from_tuples(tuples, names=["first", "second"])

np.random.seed(1000)
df = pd.DataFrame(np.random.randn(8, 2), index=index, columns=["A", "B"])

print(df)

df2 = df[:4]
print(df2)

# %%
# stack() compresses a level in the df columns, producing a series or a df.
# This is opposite of pivot() since it converts the df into records.

# In this case, columns A and B become values in a single column.
# Since now observations are now a single value, the return value is a series
# with a multi-index.
stacked = df2.stack()

print(type(stacked))
print(type(stacked.index))
print(stacked)

# %%
# Unstack is equivalent to pivot, but it works on the last level.
stacked.unstack()

# %%
#
stacked.unstack(1)

# %%
stacked.unstack(0)

# %% [markdown]
# ## Reshaping by melt.
#
# - melt() massages a df into a format where one or more columns are identifier variables, while all other columns are unpivoted leaving just two columns 'variable' and 'value'.

# %%
cheese = pd.DataFrame(
    {
        "first": ["John", "Mary"],
        "last": ["Doe", "Bo"],
        "height": [5.5, 6.0],
        "weight": [130, 150],
    }
)
cheese

# %%

pd.melt(cheese, id_vars=["first", "last"])

# %% [markdown]
# # Merge, join

# %% [markdown]
# ## concat()

# %%
df1 = pd.DataFrame(
    {
        "A": ["A0", "A1", "A2", "A3"],
        "B": ["B0", "B1", "B2", "B3"],
        "C": ["C0", "C1", "C2", "C3"],
        "D": ["D0", "D1", "D2", "D3"],
    },
    index=[0, 1, 2, 3],
)


df2 = pd.DataFrame(
    {
        "A": ["A4", "A5", "A6", "A7"],
        "B": ["B4", "B5", "B6", "B7"],
        "C": ["C4", "C5", "C6", "C7"],
        "D": ["D4", "D5", "D6", "D7"],
    },
    index=[4, 5, 6, 7],
)


df3 = pd.DataFrame(
    {
        "A": ["A8", "A9", "A10", "A11"],
        "B": ["B8", "B9", "B10", "B11"],
        "C": ["C8", "C9", "C10", "C11"],
        "D": ["D8", "D9", "D10", "D11"],
    },
    index=[8, 9, 10, 11],
)

result = pd.concat([df1, df2, df3])
result

# %%
# To track the origin of each record, one can use key to create a multiindex.
result = pd.concat([df1, df2, df3], keys="1 2 3".split())
result

# %%
result.loc["1"]

# %%
# When gluing together dfs, one can decide how to handle the other axes,
# e.g., union (outer join), intersection (inner join) or picking index of
# a specific df (right, left join).

# %%
# Index has some intersectio, but the columns are not exactly the same.
df4 = pd.DataFrame(
    {
        "B": ["B2", "B3", "B6", "B7"],
        "D": ["D2", "D3", "D6", "D7"],
        "F": ["F2", "F3", "F6", "F7"],
    },
    index=[2, 3, 6, 7],
)

print(df1)
print(df4)

# %%
pd.concat([df1, df4], axis=1, join="outer")

# %%
pd.concat([df1, df4], axis=1, join="inner")

# %%
pd.concat([df1, df4], axis=1, join_axes=[df1.index])

# %% [markdown]
# ## append()

# %%
print(df1)
print(df2)

# %%
# The indices are disjoint and the columns are the same.
df1.append(df2)

# %%
df1.append(df4)

# %%
# TODO

# %% [markdown]
# # Multiindex

# %% [markdown]
# ## Make df multi-level

# %%
df = pd.DataFrame(np.random.rand(5, 2))
display(df)

df.index.name = ""
df.reset_index(inplace=True)
df.insert(0, "datetime", pd.to_datetime("2001-01-1"))
df.set_index(["datetime", ""], inplace=True)

display(df)

# %%
isinstance(np.mean, object)

# %% [markdown]
# # "Align" data frames

# %%
import helpers.unit_test as hut

# %%
df1 = hut.get_random_df(
    2, start="2010-01-01 09:00", end="2010-01-03 09:00", freq="30T"
)

df2 = hut.get_random_df(
    3, start="2010-01-02 09:05", end="2010-01-03 00:00", freq="30T"
)

# %%
display(df1.head())

display(df2.head())
