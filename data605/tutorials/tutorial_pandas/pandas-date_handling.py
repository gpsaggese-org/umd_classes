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
#  <p><div class="lev2 toc-item"><a href="#Imports" data-toc-modified-id="Imports-01"><span class="toc-item-num">0.1&nbsp;&nbsp;</span>Imports</a></div><div class="lev2 toc-item"><a href="#TODOs" data-toc-modified-id="TODOs-02"><span class="toc-item-num">0.2&nbsp;&nbsp;</span>TODOs</a></div><div class="lev1 toc-item"><a href="#Intro-to-data-structures" data-toc-modified-id="Intro-to-data-structures-1"><span class="toc-item-num">1&nbsp;&nbsp;</span>Intro to data structures</a></div><div class="lev2 toc-item"><a href="#Series" data-toc-modified-id="Series-11"><span class="toc-item-num">1.1&nbsp;&nbsp;</span>Series</a></div><div class="lev2 toc-item"><a href="#DataFrame" data-toc-modified-id="DataFrame-12"><span class="toc-item-num">1.2&nbsp;&nbsp;</span>DataFrame</a></div><div class="lev3 toc-item"><a href="#Df-from-dict" data-toc-modified-id="Df-from-dict-121"><span class="toc-item-num">1.2.1&nbsp;&nbsp;</span>Df from dict</a></div><div class="lev2 toc-item"><a href="#Panel" data-toc-modified-id="Panel-13"><span class="toc-item-num">1.3&nbsp;&nbsp;</span>Panel</a></div><div class="lev3 toc-item"><a href="#Panel-from-dfs-with-different-indices." data-toc-modified-id="Panel-from-dfs-with-different-indices.-131"><span class="toc-item-num">1.3.1&nbsp;&nbsp;</span>Panel from dfs with different indices.</a></div><div class="lev3 toc-item"><a href="#Panel-from-data-frame-with-same-index." data-toc-modified-id="Panel-from-data-frame-with-same-index.-132"><span class="toc-item-num">1.3.2&nbsp;&nbsp;</span>Panel from data frame with same index.</a></div><div class="lev3 toc-item"><a href="#Transposing." data-toc-modified-id="Transposing.-133"><span class="toc-item-num">1.3.3&nbsp;&nbsp;</span>Transposing.</a></div><div class="lev3 toc-item"><a href="#Selecting-an-index-programmatically-by-integer" data-toc-modified-id="Selecting-an-index-programmatically-by-integer-134"><span class="toc-item-num">1.3.4&nbsp;&nbsp;</span>Selecting an index programmatically by integer</a></div><div class="lev1 toc-item"><a href="#Date-functionality" data-toc-modified-id="Date-functionality-2"><span class="toc-item-num">2&nbsp;&nbsp;</span>Date functionality</a></div><div class="lev2 toc-item"><a href="#Overview" data-toc-modified-id="Overview-21"><span class="toc-item-num">2.1&nbsp;&nbsp;</span>Overview</a></div><div class="lev2 toc-item"><a href="#Time-stamps-vs-time-spans" data-toc-modified-id="Time-stamps-vs-time-spans-22"><span class="toc-item-num">2.2&nbsp;&nbsp;</span>Time stamps vs time spans</a></div><div class="lev2 toc-item"><a href="#to_datetime()" data-toc-modified-id="to_datetime()-23"><span class="toc-item-num">2.3&nbsp;&nbsp;</span>to_datetime()</a></div><div class="lev2 toc-item"><a href="#date_range()" data-toc-modified-id="date_range()-24"><span class="toc-item-num">2.4&nbsp;&nbsp;</span>date_range()</a></div><div class="lev2 toc-item"><a href="#DatetimeIndex" data-toc-modified-id="DatetimeIndex-25"><span class="toc-item-num">2.5&nbsp;&nbsp;</span>DatetimeIndex</a></div><div class="lev2 toc-item"><a href="#Time/date-components." data-toc-modified-id="Time/date-components.-26"><span class="toc-item-num">2.6&nbsp;&nbsp;</span>Time/date components.</a></div><div class="lev2 toc-item"><a href="#Offset-objects." data-toc-modified-id="Offset-objects.-27"><span class="toc-item-num">2.7&nbsp;&nbsp;</span>Offset objects.</a></div><div class="lev2 toc-item"><a href="#Time-series-related-operations" data-toc-modified-id="Time-series-related-operations-28"><span class="toc-item-num">2.8&nbsp;&nbsp;</span>Time series-related operations</a></div><div class="lev2 toc-item"><a href="#Frequency-conversion" data-toc-modified-id="Frequency-conversion-29"><span class="toc-item-num">2.9&nbsp;&nbsp;</span>Frequency conversion</a></div><div class="lev2 toc-item"><a href="#Time-span-representation" data-toc-modified-id="Time-span-representation-210"><span class="toc-item-num">2.10&nbsp;&nbsp;</span>Time span representation</a></div><div class="lev2 toc-item"><a href="#Time-zone-handling" data-toc-modified-id="Time-zone-handling-211"><span class="toc-item-num">2.11&nbsp;&nbsp;</span>Time zone handling</a></div>

# %% [markdown]
# ## Imports

# %%
# !conda info --envs

# %% run_control={"marked": false}
import datetime

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# %matplotlib inline

# %%
import notebook_utils

notebook_utils.notebook_config()
# matplotlib.rcParams["figure.figsize"] = (15, 6)

# assert np.__version__ == "1.13.3"
assert pd.__version__ == "0.20.3"
# assert matplotlib.__version__ == "2.0.2"

# %%


# def display_df(df):
#     display(df)

# %% [markdown]
# ## TODOs

# %% [markdown]
# # Intro to data structures

# %% [markdown]
# ## Series
#
# - Series is a one-dimensional labeled array holding any data type (integers, strings, floats, objects)
# - Axis labels are referred to as the index

# %%
np.random.seed(1000)
# Realizations from standard normal.
s = pd.Series(np.random.randn(5))
s

# %%
np.random.seed(1000)
s = pd.Series(np.random.randn(5), index="a b c d e".split())
s

# %%
# From dictionary.
d = {"a": 0.0, "b": 1.0, "c": 2.0}
s = pd.Series(d)
s

# %% [markdown]
# ## DataFrame

# %%
df = pd.DataFrame("a b c d e".split())
print("df.index.is_unique=", df.index.is_unique)
print("df.index.is_monotonic=", df.index.is_monotonic)
print("df.index.is_monotonic_increasing=", df.index.is_monotonic_increasing)

# %%
df = pd.DataFrame("a b c d e".split(), index=[0, 2, 1, 3, 4])
print("df.index.is_unique=", df.index.is_unique)
print("df.index.is_monotonic=", df.index.is_monotonic)
print("df.index.is_monotonic_increasing=", df.index.is_monotonic_increasing)

# %% [markdown]
# ### Df from dict

# %%
df1 = pd.DataFrame("a b c d".split(), index=[0, 1, 2, 3], columns=["val1"])
dict_ = df1.to_dict()["val1"]
print(dict_)

# %%
pd.DataFrame.from_dict({"weight": dict_})

# %% [markdown]
# ## Panel
#
# - A panel automatically aligns on union of all indices

# %% [markdown]
# ### Panel from dfs with different indices.

# %%
df1 = pd.DataFrame("a b c d".split(), index=[0, 1, 2, 3], columns=["val1"])
print(df1)
df2 = pd.DataFrame("e f g h".split(), index=[0, 1, 2, 4], columns=["val2"])
print(df2)

# %%
panel = pd.Panel({"foo": df1, "bar": df2})
# item axis -> key
# major axis -> index of df
# minor axis -> column of df
print("panel=", panel)

# %%
print("panel['foo']=\n", panel["foo"])
print("\npanel['bar']=\n", panel["bar"])

# Note the union of the indices.

# %% [markdown]
# ### Panel from data frame with same index.

# %%
df1 = pd.DataFrame(
    [["a", "A"], ["b", "B"], ["c", "C"], ["d", "D"]],
    index=[0, 1, 2, 3],
    columns=["val1", "val2"],
)
print(df1)


df2 = pd.DataFrame(
    [["e", "E"], ["f", "F"], ["g", "G"], ["h", "H"]],
    index=[0, 1, 2, 3],
    columns=["val1", "val2"],
)
print(df2)

# %%
panel = pd.Panel({"foo": df1, "bar": df2})
# item axis -> key
# major axis -> index of df
# minor axis -> column of df
print(panel)

# %%
print("panel['foo']=\n", panel["foo"])
print("\npanel['bar']=\n", panel["bar"])

# %%
# Slice using loc[].
print(panel.loc[:, :, ["val1"]])

# %% [markdown]
# ### Transposing.

# %%
rng = pd.date_range("1/1/2014", periods=100, freq="D")
cols = ["A", "B", "C", "D"]

np.random.seed(42)
df1 = pd.DataFrame(np.random.randn(100, len(cols)), rng, cols)
df2 = pd.DataFrame(np.random.randn(100, len(cols)), rng, cols)
df3 = pd.DataFrame(np.random.randn(100, len(cols)), rng, cols)

pf = pd.Panel({"df1": df1, "df2": df2, "df3": df3})

print(pf)

# %%
print(list(pf.keys()))
print(pf["df1"].head())

# %%
pf2 = pf.transpose(2, 0, 1)
print(pf2)

print("\n", pf2["A"].head())

# %%
pf2 = pf.transpose(2, 1, 0)
print(pf2)

print("\n", pf2["A"].head())

# %%
pf2 = pf.transpose(1, 2, 0)
print(pf2)

# %% [markdown]
# ### Selecting an index programmatically by integer
#
# - Sometimes we want to select programatically an index by order

# %%
print(pf2)

print()
print("items=%s\n" % pf2.items)
print("major_axis=%s\n" % pf2.major_axis)
print("minor_axis=%s\n" % pf2.minor_axis)

# %%
print(len(pf2.axes))
print(pf2.axes)

# %%
print("items=%s\n", pf2.axes[0])
print("major=%s\n", pf2.axes[1])
print("minor=%s\n", pf2.axes[2])

# %% [markdown] run_control={"marked": false}
# # Date functionality
#
# http://pandas.pydata.org/pandas-docs/stable/timeseries.html
#
# - Generate sequence of fixed-frequency dates and time spans
# - Conform / convert time-series to a particular frequency
# - Compute relative dates based on non-standard time incrementens

# %% [markdown] run_control={"marked": false}
# ## Overview

# %% run_control={"marked": false}
# 72 hours data on hourly frequency.
rng = pd.date_range("2011-01-01", periods=72, freq="H")

print(type(rng))
print(len(rng))
print(rng[:2])
print(rng[-2:])

# %% run_control={"marked": false}
# Build a time series from random data.
np.random.seed(1000)
ts = pd.Series(np.random.rand(len(rng)), index=rng)

print(type(ts.index))
ts.head()

# %% run_control={"marked": false}
ts.plot()

# %%
# Change frequency.
converted = ts.asfreq("45Min")
converted.head(10)

# %% run_control={"marked": false}
# Change frequency and fill gaps.
# ffill: fills forward the nans (causal).
converted = ts.asfreq("45Min", method="ffill")
converted.head(10)

# %% run_control={"marked": false}
# Resample daily using mean() to aggregate.
ts.resample("D").mean()

# %% run_control={"marked": false}
ts.plot(label="ts")
converted.plot(label="converted")
ts.resample("D").mean().plot(label="daily mean")
plt.legend(loc="best")

# %% [markdown] run_control={"marked": false}
# ## Time stamps vs time spans
#
# http://pandas.pydata.org/pandas-docs/stable/timeseries.html#time-stamps-vs-time-spans
#
# - Timestamp = represents a single point in time
#     - create with: to_datetime(), Timestamp()
# - DatetimeIndex = index of Timestamp
#     - create with: to_datetime(), date_range(), DatetimeIndex()
#
# - Period = represents a single time span
#     - create with: Period()
# - PeriodIndex = index of Period
#     - create with: period_range(), PeriodIndex()

# %% run_control={"marked": false}
pd.Timestamp(datetime.datetime(2012, 5, 1))

# %% run_control={"marked": false}
pd.Timestamp("2012-05-01")

# %% run_control={"marked": false}
pd.Timestamp(2012, 5, 1)

# %% run_control={"marked": false}
pd.Period("2011-01", freq="D")

# %% run_control={"marked": false}
# Timestamp is coerced to DatetimeIndex when used as index in DataFrame and Series.
dates = [pd.Timestamp(d) for d in "2015-05-01 2015-05-02 2015-05-03".split()]

np.random.seed(1000)
ts = pd.Series(np.random.randn(len(dates)), dates)

print("ts=", ts)

print("type(ts.index)=", type(ts.index))

# Note that there is no frequency inferred.
print("ts.index=", ts.index)

# %%
# Extract a np.array of datetime.date.
ts.index.date

# %% run_control={"marked": false}
# Period is coerced to PeriodIndex.
periods = [pd.Period(d) for d in "2012-01 2012-02 2012-03".split()]
ts = pd.Series(np.random.randn(len(periods)), periods)

print("ts=", ts)

print("type(ts.index)=", type(ts.index))

# Note that a month frequency is inferred.
print("ts.index=", ts.index)

# %% [markdown] run_control={"marked": false}
# ## to_datetime()
#
# http://pandas.pydata.org/pandas-docs/stable/timeseries.html#converting-to-timestamps
#
# - Used to convert to pd.Timestamp objects

# %% run_control={"marked": false}
# Series with a bunch of strings (objects).
srs = pd.Series(["Jul 31, 2009", "2010-01-10", None])
print("srs=", srs)

# Convert to string with timestamps.
print(pd.to_datetime(srs))

# %% run_control={"marked": false}
# pd.to_datetime() returns a list or a single element.
print(pd.to_datetime("2010-11-12"))
print(pd.to_datetime(["2010-11-12", "2010-11-13", "2010-11-14"]))

# %% run_control={"marked": false}
# Using Epochs.
pd.to_datetime(
    [1349720105, 1349806505, 1349892905, 1349979305, 1350065705], unit="s"
)

# %% run_control={"marked": false}
pd.to_datetime(
    [
        dt * 1000
        for dt in [1349720105, 1349806505, 1349892905, 1349979305, 1350065705]
    ],
    unit="ms",
)

# %% run_control={"marked": false}
# ??? Not working in 0.19
if False:
    dts = pd.to_datetime(["2010-11-12", "2010-11-13", "2010-11-14"])
    pd.to_pydatetime(dts)

# %% [markdown] run_control={"marked": false}
# ## date_range()
#
# http://pandas.pydata.org/pandas-docs/stable/timeseries.html#generating-ranges-of-timestamps
#
# - date_range() is used to generate ranges of Timestamps
# - date_range() is inclusive

# %%
# Beginning of month (MS=month start).
idx = pd.date_range("2000-1-1", periods=10, freq="MS")
idx

# %% run_control={"marked": false}
# End of month.
idx = pd.date_range("2000-1-1", periods=10, freq="M")
idx

# %% run_control={"marked": false}
# All (calendar) days.
idx = pd.date_range("2000-1-1", periods=10, freq="D")
idx

# %% run_control={"marked": false}
# All business days.
idx = pd.bdate_range("2000-1-1", periods=1000)
idx

# %% run_control={"marked": false}
# Specify [start, end].
start = datetime.datetime(2011, 1, 1)
end = datetime.datetime(2012, 1, 1)
idx = pd.date_range(start, end)
idx

# %% run_control={"marked": false}
# Beginning of month.
pd.date_range(start, end, freq="MS")

# %% run_control={"marked": false}
# Every week (starting from Sunday).
pd.date_range(start, end, freq="W")

# %%
print(pd.to_datetime("2011-01-02").dayofweek)

# %% run_control={"marked": false}
# Start from beginning for 20 business days.
pd.bdate_range(start=start, periods=20)

# %% run_control={"marked": false}
# Start from end for 20 business days.
pd.bdate_range(end=end, periods=20)

# %% [markdown] run_control={"marked": false}
# ## DatetimeIndex
#
# http://pandas.pydata.org/pandas-docs/stable/timeseries.html#datetimeindex
#
# - DatetimeIndex is index of pandas objects
# - It supports union / intersection operations, shifting operations

# %% run_control={"marked": false}
# Build a df with an index every last day of the month.
idx = pd.date_range(start, end, freq="BM")
ts = pd.Series(np.random.randn(len(idx)), index=idx)
ts.index

# %% run_control={"marked": false}
ts[:5].index

# %% run_control={"marked": false}
# Skip 2.
ts[::2].index

# %% run_control={"marked": false}
# Index with string representing a date.
ts["1/31/2011"]

# %%
# Index with datetime.
ts[datetime.date(2011, 1, 31)]

# %%
# Slice with string.
ts["2011-12-25":]

# %% run_control={"marked": false}
# Slice with datetime().
ts[datetime.datetime(2011, 12, 25) :]

# %% run_control={"marked": false}
# Slice with partial string.
ts["2011"]

# %% run_control={"marked": false}
# Select with partial string.
ts["2011-06"]

# %% run_control={"marked": false}
# Label slicing implies that endpoints are included
# (different from python convention, but same as np).
ts["2011-01-31":"2011-03-31"]

# %% run_control={"marked": false}
# truncate() is equivalent to slicing (both endpoints are included in the sliced object).
ts.truncate(before="10/31/2011", after="12/31/2011")

# %% [markdown] run_control={"marked": false}
# ## Time/date components.
#
# http://pandas.pydata.org/pandas-docs/stable/timeseries.html#time-date-components

# %%
dt = pd.Timestamp("2012-05-01")
print(type(dt), dt)

dt = pd.to_datetime("2012-05-01")
print(type(dt), dt)

# %% run_control={"marked": false}
dt = pd.Timestamp("2012-05-01")

print("year=", dt.year)
print("microsecond=", dt.microsecond)
print("date=", dt.date())
print("dayofyear=", dt.dayofyear)
print("weekofyear=", dt.weekofyear)
print("week=", dt.week)
print("dayofweek=", dt.dayofweek)
print("weekday=", dt.weekday())
print("weekday_name=", dt.weekday_name)
# Number of days in the month of dt.
print("days_in_month=", dt.days_in_month)
print("is_month_start=", dt.is_month_start)
print("is_month_end=", dt.is_month_end)
print("is_leap_year=", dt.is_leap_year)

# %% [markdown] run_control={"marked": false}
# ## Offset objects.
#
# http://pandas.pydata.org/pandas-docs/stable/timeseries.html#dateoffset-objects
#
# - Frequency strings (e.g., M, W, BM) are converted to pandas pd.offsets.DateOffset(), which represents a regular frequency increment
# - DateOffset() keeps results as Timestamp (differently from timedelta)
#
# - Offset information are at
#   - http://pandas.pydata.org/pandas-docs/stable/timeseries.html#offset-aliases
#   - http://pandas.pydata.org/pandas-docs/stable/timeseries.html#anchored-offsets

# %% run_control={"marked": false}
# Using pd.offsets.DateOffset() returns a Timestamp.
d = datetime.datetime(2008, 8, 18, 19, 0)
print(type(d), d)

next_d = d + pd.offsets.DateOffset(months=4, days=5)
print(type(next_d), next_d)

# %% run_control={"marked": false}
print("BDay=", d + pd.offsets.BDay())
print("Week=", d + pd.offsets.Week())
# print "WeekOfMonth=", d + pd.offsets.WeekOfMonth()

# %% run_control={"marked": false}
# Use DateOffset() to align to month.
print("d=", d)
print("MonthEnd=", d + pd.offsets.MonthEnd())
print("MonthBegin=", d + pd.offsets.MonthBegin())

# Align to first / last business day.
print("BMonthEnd=", d + pd.offsets.BMonthEnd())
print("BMonthBegin=", d + pd.offsets.BMonthBegin())

# %% run_control={"marked": false}
# Offset can be manipulated with arithmetic.
offset = 5 * pd.offsets.BDay()
print(type(offset))
print(offset)

# %% run_control={"marked": false}
# Some offsets can be parametrized.
print(d)

# Preserve the hour.
print(d + pd.offsets.Week())

# Align to a specific day of the week
print(d + pd.offsets.Week(weekday=4))
print((d + pd.offsets.Week(weekday=4)).dayofweek)

# This aligns to midnight.
print(d + pd.offsets.Week(normalize=True))

# %% run_control={"marked": false}
# Offsets also works with Series / DataFrames (although might be slow since it is not vectorized).
rng = pd.date_range(start="2012-01-01", end="2012-01-03", freq="1D")
s = pd.Series(rng)
print(s)

print(s + pd.offsets.DateOffset(months=1))

# %% run_control={"marked": false}
# In general string aliases and offset objects are interchangeable.
print(pd.date_range(start="2012-01-01", end="2012-01-10", freq="3D"))
print(
    pd.date_range(
        start="2012-01-01", end="2012-01-10", freq=3 * pd.offsets.Day()
    )
)

# %% run_control={"marked": false}
# One can combine day and intraday offsets in string offsets.
pd.date_range(start, periods=10, freq="2h20min")

# %% [markdown] run_control={"marked": false}
# ## Time series-related operations

# %% run_control={"marked": false}
idx = pd.date_range(start="2012-01-01", end="2012-01-07", freq="1D")
ts = pd.Series(list(range(len(idx))), index=idx)
ts

# %% run_control={"marked": false}
# Shift back, i.e., yesterday becomes today.
# shift() doesn't change the time scale.
ts.shift(1)

# %% run_control={"marked": false}
# By specifying a freq one can shift the time series, by shifting the time scale.
# Note that the first element is not NA since the data is not being realigned.
# ??? Weird that there are two 2012-01-09 now...
ts.shift(1, freq=pd.offsets.BDay())

# %% [markdown] run_control={"marked": false}
# ## Frequency conversion
#
# http://pandas.pydata.org/pandas-docs/stable/timeseries.html#frequency-conversion
#
# - asfreq() allows to change frequency of a time series.
# - in practice it is equivalent to a call to date_range() and a call to reindex()

# %% run_control={"marked": false}
np.random.seed(1000)
idx = pd.date_range("1/1/2010", periods=3, freq=3 * pd.offsets.BDay())
ts = pd.Series(np.random.randn(len(idx)), index=idx)

ts

# %%
# Sample using calendar days.
ts.asfreq(pd.offsets.Day())

# %% run_control={"marked": false}
# Sample using business days.
ts.asfreq(pd.offsets.BDay())

# %% run_control={"marked": false}
ts.asfreq(pd.offsets.BDay(), method="ffill")

# %% [markdown] run_control={"marked": false}
# ## Time span representation
#
# http://pandas.pydata.org/pandas-docs/stable/timeseries.html#time-span-representation
#
# - Period() represents a span of time
# - Regular intervals of time are represented by Period objects

# %% run_control={"marked": false}
# Arithmetic operations on periods.
p = pd.Period("2012-1-1", freq="D")
print(type(p), p)
print(p + 1)
print(p - 3)

# %%
p = pd.Timestamp("2012-1-1", freq="D")
print(type(p), p)
print(p + 1)
print(p - 3)

# %% run_control={"marked": false}
prng = pd.period_range("1/1/2011", "1/1/2012", freq="M")
prng

# %% run_control={"marked": false}
np.random.seed(1000)
ts = pd.Series(np)

# %% [markdown]
# ## Time zone handling

# %%
# By default pandas objects are time zone unaware.
rng = pd.date_range("3/6/2012 00:00", periods=15, freq="D")
print(rng)
print(rng.tz is None)

# %%
# Using pandas timezone support.
rng = pd.date_range("3/6/2012 00:00", periods=10, freq="D", tz="Europe/London")
print(rng)
print(rng.tz is None)
print(rng.tz)

# %%
# Using pytz timezone.
import pytz

pytz_ = pytz.timezone("Europe/London")
rng_pytz = pd.date_range("3/6/2012 00:00", periods=10, freq="D", tz=pytz_)
print(rng_pytz)

# %%
# tz_localize() just forces a tz-unaware datetime to become aware of
# the passed tz. It's up to the caller to know how to interpret the
# date time.
# datetime() doesn't have tz_localize method.
dt = pd.to_datetime(datetime.date(2000, 2, 1))
print("dt=", type(dt), dt)

# datetime() doesn't have tz_localize method.
print("dt=", type(dt), dt.tz_localize("US/Eastern"))

# %%
# Once a datetime is localized, one can represent the same data with
# different timezones.
dt = pd.to_datetime(datetime.date(2000, 2, 1))
print("dt=", type(dt), dt)

dt = dt.tz_localize("UTC")
print("dt=", type(dt), dt)

dt = dt.tz_convert("US/Eastern")
print("dt=", type(dt), dt)

# %%
# Localize and convert to timezone aware.
np.random.seed(1000)
rng = pd.date_range("3/6/2012 00:00", periods=15, freq="D")
ts = pd.Series(np.random.randn(len(rng)), rng)
print(ts.head(3))

ts_utc = ts.tz_localize("UTC")
print("\n", ts_utc.head(3))

print("\n", ts_utc.tz_convert("US/Eastern").head(3))

# %%
# To remove localization.
ts_utc.tz_localize(None).head(3)
