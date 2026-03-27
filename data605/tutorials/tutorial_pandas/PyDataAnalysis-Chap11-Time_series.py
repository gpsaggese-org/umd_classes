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
#  <p><div class="lev1 toc-item"><a href="#Time-series" data-toc-modified-id="Time-series-1"><span class="toc-item-num">1&nbsp;&nbsp;</span>Time series</a></div><div class="lev2 toc-item"><a href="#Date-and-time-data-types-and-tools" data-toc-modified-id="Date-and-time-data-types-and-tools-11"><span class="toc-item-num">1.1&nbsp;&nbsp;</span>Date and time data types and tools</a></div><div class="lev3 toc-item"><a href="#Converting-between-string-and-datetime" data-toc-modified-id="Converting-between-string-and-datetime-111"><span class="toc-item-num">1.1.1&nbsp;&nbsp;</span>Converting between string and datetime</a></div><div class="lev2 toc-item"><a href="#Time-series-basics" data-toc-modified-id="Time-series-basics-12"><span class="toc-item-num">1.2&nbsp;&nbsp;</span>Time series basics</a></div><div class="lev3 toc-item"><a href="#Indexing,-selection,-subsetting" data-toc-modified-id="Indexing,-selection,-subsetting-121"><span class="toc-item-num">1.2.1&nbsp;&nbsp;</span>Indexing, selection, subsetting</a></div><div class="lev3 toc-item"><a href="#Time-series-with-duplicated-indices." data-toc-modified-id="Time-series-with-duplicated-indices.-122"><span class="toc-item-num">1.2.2&nbsp;&nbsp;</span>Time series with duplicated indices.</a></div><div class="lev2 toc-item"><a href="#Date-ranges,-freqs,-shifting" data-toc-modified-id="Date-ranges,-freqs,-shifting-13"><span class="toc-item-num">1.3&nbsp;&nbsp;</span>Date ranges, freqs, shifting</a></div><div class="lev3 toc-item"><a href="#Generating-date-ranges" data-toc-modified-id="Generating-date-ranges-131"><span class="toc-item-num">1.3.1&nbsp;&nbsp;</span>Generating date ranges</a></div><div class="lev3 toc-item"><a href="#Frequencies-and-date-offsets" data-toc-modified-id="Frequencies-and-date-offsets-132"><span class="toc-item-num">1.3.2&nbsp;&nbsp;</span>Frequencies and date offsets</a></div><div class="lev3 toc-item"><a href="#Shifting-data" data-toc-modified-id="Shifting-data-133"><span class="toc-item-num">1.3.3&nbsp;&nbsp;</span>Shifting data</a></div><div class="lev3 toc-item"><a href="#Shifting-dates-with-offsets" data-toc-modified-id="Shifting-dates-with-offsets-134"><span class="toc-item-num">1.3.4&nbsp;&nbsp;</span>Shifting dates with offsets</a></div><div class="lev2 toc-item"><a href="#Time-zone-handling" data-toc-modified-id="Time-zone-handling-14"><span class="toc-item-num">1.4&nbsp;&nbsp;</span>Time zone handling</a></div><div class="lev3 toc-item"><a href="#Time-zone-localization-and-conversion" data-toc-modified-id="Time-zone-localization-and-conversion-141"><span class="toc-item-num">1.4.1&nbsp;&nbsp;</span>Time zone localization and conversion</a></div><div class="lev3 toc-item"><a href="#Operations-with-time-zone-aware-timestamp-objects" data-toc-modified-id="Operations-with-time-zone-aware-timestamp-objects-142"><span class="toc-item-num">1.4.2&nbsp;&nbsp;</span>Operations with time zone-aware timestamp objects</a></div><div class="lev3 toc-item"><a href="#Operations-between-different-time-zones" data-toc-modified-id="Operations-between-different-time-zones-143"><span class="toc-item-num">1.4.3&nbsp;&nbsp;</span>Operations between different time zones</a></div><div class="lev2 toc-item"><a href="#Periods-and-period-arithmetic" data-toc-modified-id="Periods-and-period-arithmetic-15"><span class="toc-item-num">1.5&nbsp;&nbsp;</span>Periods and period arithmetic</a></div><div class="lev3 toc-item"><a href="#Period-frequency-conversion" data-toc-modified-id="Period-frequency-conversion-151"><span class="toc-item-num">1.5.1&nbsp;&nbsp;</span>Period frequency conversion</a></div><div class="lev3 toc-item"><a href="#Quarterly-period-frequencies" data-toc-modified-id="Quarterly-period-frequencies-152"><span class="toc-item-num">1.5.2&nbsp;&nbsp;</span>Quarterly period frequencies</a></div><div class="lev3 toc-item"><a href="#Converting-timestamps-to-periods-(and-back)" data-toc-modified-id="Converting-timestamps-to-periods-(and-back)-153"><span class="toc-item-num">1.5.3&nbsp;&nbsp;</span>Converting timestamps to periods (and back)</a></div><div class="lev3 toc-item"><a href="#Creating-a-PeriodIndex-from-arrays" data-toc-modified-id="Creating-a-PeriodIndex-from-arrays-154"><span class="toc-item-num">1.5.4&nbsp;&nbsp;</span>Creating a PeriodIndex from arrays</a></div><div class="lev2 toc-item"><a href="#Resampling-and-frequency-conversion" data-toc-modified-id="Resampling-and-frequency-conversion-16"><span class="toc-item-num">1.6&nbsp;&nbsp;</span>Resampling and frequency conversion</a></div><div class="lev3 toc-item"><a href="#Downsampling" data-toc-modified-id="Downsampling-161"><span class="toc-item-num">1.6.1&nbsp;&nbsp;</span>Downsampling</a></div><div class="lev4 toc-item"><a href="#OHLC-resampling" data-toc-modified-id="OHLC-resampling-1611"><span class="toc-item-num">1.6.1.1&nbsp;&nbsp;</span>OHLC resampling</a></div><div class="lev4 toc-item"><a href="#Resampling-with-GroupBy" data-toc-modified-id="Resampling-with-GroupBy-1612"><span class="toc-item-num">1.6.1.2&nbsp;&nbsp;</span>Resampling with GroupBy</a></div><div class="lev3 toc-item"><a href="#Upsampling" data-toc-modified-id="Upsampling-162"><span class="toc-item-num">1.6.2&nbsp;&nbsp;</span>Upsampling</a></div><div class="lev3 toc-item"><a href="#Resampling-with-periods" data-toc-modified-id="Resampling-with-periods-163"><span class="toc-item-num">1.6.3&nbsp;&nbsp;</span>Resampling with periods</a></div><div class="lev2 toc-item"><a href="#Time-series-plotting" data-toc-modified-id="Time-series-plotting-17"><span class="toc-item-num">1.7&nbsp;&nbsp;</span>Time series plotting</a></div><div class="lev2 toc-item"><a href="#Moving-window-functions" data-toc-modified-id="Moving-window-functions-18"><span class="toc-item-num">1.8&nbsp;&nbsp;</span>Moving window functions</a></div><div class="lev3 toc-item"><a href="#Exponentially-weighted-functions" data-toc-modified-id="Exponentially-weighted-functions-181"><span class="toc-item-num">1.8.1&nbsp;&nbsp;</span>Exponentially-weighted functions</a></div><div class="lev3 toc-item"><a href="#Binary-moving-window-functions" data-toc-modified-id="Binary-moving-window-functions-182"><span class="toc-item-num">1.8.2&nbsp;&nbsp;</span>Binary moving window functions</a></div><div class="lev3 toc-item"><a href="#User-defined-moving-window-functions" data-toc-modified-id="User-defined-moving-window-functions-183"><span class="toc-item-num">1.8.3&nbsp;&nbsp;</span>User-defined moving window functions</a></div>

# %%
import pandas as pd


def print_ht(df):
    print(df.head())
    print(df.tail())


# %% [markdown]
# # Time series
#
# - Anything that is observed or measured at many points in time
#     - fixed frequency
#     - irregular
#
# - One can refer to time series in terms of
#     1) timestamps: specific instant in times
#     2) intervals of time: indicated by start / end timestamps
#     3) fixed periods: e.g., months of 2010, years
#         - This is a special case of "interval of time"
#     4) delta times with respect to a beginning of time

# %% [markdown]
# ## Date and time data types and tools
#
# - date
# - time
# - datetime
# - timedelta

# %%
from datetime import datetime, timedelta

now = datetime.now()
print("now=", now)
print(now.year, now.month, now.day)

# %%
delta = datetime(2011, 1, 7) - datetime(2008, 6, 25, 8, 15)
print("delta=", delta)
print(delta.days, delta.seconds)

# %%
start = datetime(2011, 1, 7)
print(start + timedelta(12))

# %% [markdown]
# ### Converting between string and datetime

# %%
ts = datetime(2011, 1, 3)

print("str=", str(ts))
# Format using ISO C89.
# strftime = str Format time
print("strftime=", ts.strftime("%Y-%m-%d"))

# %%
# strptime = str Parse time
# It is useful to parse a date in a known format.
value = "2011-01-03"
datetime.strptime(value, "%Y-%m-%d")

# %%
# To parse data in unknown format.
import dateutil

print(dateutil.parser.parse("2011-01-03"))
print(dateutil.parser.parse("Jan 31, 1997 10:45 PM"))

# Using pandas.
print(pd.to_datetime("2011-07-06 12:00:00"))

# %%
# pd.to_datetime works also with array of strings.
datestrs = ["2011-07-06 12:00:00", "2011-08-06 00:00:00"]
print(pd.to_datetime(datestrs))

# %%
# None gets converted into a Not-A-Time.
print(pd.to_datetime(datestrs + [None]))

# %% [markdown]
# ## Time series basics

# %%
dates = [
    datetime(2011, 1, 2),
    datetime(2011, 1, 5),
    datetime(2011, 1, 7),
    datetime(2011, 1, 8),
    datetime(2011, 1, 10),
    datetime(2011, 1, 12),
]

ts = pd.Series(np.random.randn(6), index=dates)

ts

# %%
ts.index

# %%
# Arithmetic operations between differently indexed time series
# automatically align on dates.

ts + ts[::2]

# %%
ts[::2]

# %%
# Timestamps are stored using np datetime64 at ns resolution.
print("ts.index.dtype=", ts.index.dtype)

# Timestamp are derived from datetime objects.
timestamp = ts.index[0]
print(type(timestamp))
print(timestamp)

# %% [markdown]
# ### Indexing, selection, subsetting

# %%
# Time series behaves as any pd.Series.

print("ts=\n", ts)

stamp = ts.index[2]
print("\nstamp=", stamp)

# %%
# You can pass a string that will be interpreted as a date.

print(ts["1/10/2011"])

print(ts["20110110"])

# %%
longer_ts = pd.Series(
    np.random.randn(1000), index=pd.date_range("1/1/2000", periods=1000)
)

print_ht(longer_ts)

# %%
# Filter by year.
print_ht(longer_ts["2001"])

# %%
# Filter by month.
print_ht(longer_ts["2001-05"])

# %%
# Slice by datetime.
ts[datetime(2011, 1, 7) :]

# %%
# One can use date, datetime, or timestamp to slice.
# Note that slicing creates a np view on the object, and there
# is no data copied.
ts["1/6/2011":"1/11/2011"]

# %%
ts.truncate(after="1/9/2011")

# %%
# Everything works also for DataFrame indexed on datetimes.

dates = pd.date_range("1/1/2000", periods=100, freq="W-WED")

long_df = pd.DataFrame(
    np.random.randn(100, 4),
    index=dates,
    columns="Colorado Texas NY Ohio".split(),
)

print(long_df.index.is_unique)

print_ht(long_df)

# %%
long_df.loc["5-2001"]

# %% [markdown]
# ### Time series with duplicated indices.

# %%
dates = pd.DatetimeIndex(
    ["1/1/2000", "1/2/2000", "1/2/2000", "1/2/2000", "1/3/2000"]
)

dup_ts = pd.Series(np.arange(5), index=dates)

dup_ts

# %%
dup_ts.index.is_unique

# %%
# Indexing can produce scalar values or slices, depending on whether
# a timestamp is duplicated.

# Not dup.
print(dup_ts["1/3/2000"])

# Dup.
print(dup_ts["1/2/2000"])

# %%
# To aggregate the data, you can use groupby using level=0.
grouped = dup_ts.groupby(level=0)

# Count elements per date.
print(grouped.count())

# Compute mean.
print(grouped.mean())

# %% [markdown]
# ## Date ranges, freqs, shifting

# %%
# Time series in Pandas are assumed to be "irregular", i.e., having
# no fixed frequency.
# Often we want to work with time series with fixed frequency.
# Pandas has functions for:
# - resampling
# - inferring frequencies
# - generating fixed-frequency ranges

# %%
dates = [
    datetime(2011, 1, 2),
    datetime(2011, 1, 5),
    datetime(2011, 1, 7),
    datetime(2011, 1, 8),
    datetime(2011, 1, 10),
    datetime(2011, 1, 12),
]
ts = pd.Series(np.random.randn(6), index=dates)
ts

# %%
ts.resample("D")

# %% [markdown]
# ### Generating date ranges

# %%
# Sample daily (by default) a (closed) interval of dates.
pd.date_range("2012-04-01", "2012-06-01")

# %%
# If only one point of the interval is specified, periods is
# required
print(pd.date_range(start="2012-04-01", periods=5))
print(pd.date_range(end="2012-06-01", periods=5))

# %%
pd.date_range("2000-01-01", "2000-06-01", freq="BM")

# %%
# date_range() preserves the time, if present.
pd.date_range("2012-05-02 12:56:31", periods=5)

# %%
# normalize=True aligns on midnights.
pd.date_range("2012-05-02 12:56:31", periods=5, normalize=True)

# %% [markdown]
# ### Frequencies and date offsets
#
# - frequencies are composed of a base frequency and a multiplier

# %%
from pandas.tseries.offsets import Hour, Minute

hour = Hour()
print(hour)

# %%
four_hours = Hour(4)
print(four_hours)

# %%
pd.date_range("2000-01-01", "2000-01-02 23:59", freq="4h")

# %%
# Frequencies can be combined.
Hour(2) + Minute(30)

# %%
pd.date_range("2000-01-01", periods=10, freq="1h30min")

# %%
# Week of month: e.g., 3rd Friday of each month.
pd.date_range("2012-01-01", "2012-09-01", freq="WOM-3FRI")

# %% [markdown]
# ### Shifting data
#
# - shift is about moving data back and forward through time

# %%
ts = pd.Series(
    np.random.randn(4), index=pd.date_range("1/1/2000", periods=4, freq="M")
)
ts

# %%
# Shift backward 2 lags (delay).
# Note that no new timestamps is inferred, so data is lost.
ts.shift(2)

# %%
# Shift forward 2 lags.
ts.shift(-2)

# %%
# If frequency of data is known, new timestamps can be inferred.
ts.shift(2, freq="M")

# %%
ts.shift(3, freq="D")

# %%
# Shift back of 4 * 90 mins = 6hrs.
ts.shift(4, freq="90T")

# %% [markdown]
# ### Shifting dates with offsets

# %%
from pandas.tseries.offsets import Day, MonthEnd

now = datetime(2011, 11, 17)

print(now + 3 * Day())

# %%
# Anchored offsets allow to align a period of time.
print(now + MonthEnd())
# This is equivalent to:
print(MonthEnd().rollforward(now))

# %%
print(now + MonthEnd(2))

# %%
# One can use date offsets with groupby.
ts = pd.Series(
    np.random.randn(20), index=pd.date_range("1/15/2000", periods=20, freq="4d")
)
ts

# %%
offset = MonthEnd()


def print_group(df):
    print("[%s, %s]" % (df.index[0], df.index[-1]))


# print ts.groupby(offset.rollforward).first()
# print ts.groupby(offset.rollforward).last()
_ = ts.groupby(offset.rollforward).agg(print_group)

# %%
# This is equivalent to resample.
ts.resample("M").agg(print_group)

# %% [markdown]
# ## Time zone handling
#
# - Working with time zones is unpleasant
#     - One can work with UTC (Coordinated Universal Time), which is
#       an international standard
#     - Time zones are expressed as offsets from UTC
#     - E.g., NY is +4 during daylight saving time (DST), +5 otherwise
# - pytz is 3rd party library
#     - Olson db
#     - DST and UTC offsets have been changed many times
# - pandas wraps pytz

# %%
import pytz

pytz.common_timezones[-7:]

# %%
tz = pytz.timezone("America/New_York")

print(tz)
print(repr(tz))

# %% [markdown]
# ### Time zone localization and conversion
#
# - By default time series are time zone naive

# %%
rng = pd.date_range("3/9/2012 9:30", periods=6, freq="D")

print(rng)

# Note that tz field is none.
print(rng.tz)

# %%
ts = pd.Series(np.random.randn(len(rng)), index=rng)
print(ts)

# Note that tz field is none.
print("index.tz=", ts.index.tz)

# %%
# Generate data range with a UTC time zone.
rng = pd.date_range("3/9/2012 9:30", periods=6, freq="D", tz="UTC")

print(rng)
print(rng.tz)

# %%
# Generate data range with a time zone.
rng = pd.date_range("3/9/2012 9:30", periods=6, freq="D", tz="US/Pacific")

print(rng)
print(rng.tz)

# %%
# Naive times can be converted in "localized".
ts_utc = ts.tz_localize("UTC")
print(ts_utc)
print(ts_utc.index.tz)

# Once they are localized, dates can be converted into other time zones.
ts_edt = ts_utc.tz_convert("America/New_York")
print("\n", ts_edt)
print(ts_edt.index.tz)

# %%
# Add a ET timezone.
ts_edt = ts.tz_localize("America/New_York")
print(ts_edt)
print(ts_edt.index.tz)

# %%
# tz_localize and tz_convert are also methods of DateTimeIndex

# %% [markdown]
# ### Operations with time zone-aware timestamp objects
#
# - Also Timestamp can be handled in terms of time-zones

# %%
ts = pd.Timestamp("2011-03-12 04:00")
print("ts=", ts)

ts_utc = ts.tz_localize("UTC")
print("\nts_utc=", ts_utc)

print("ts_convert=", ts_utc.tz_convert("America/New_York"))

# %%
ts_moscow = pd.Timestamp("2011-03-12 04:00", tz="Europe/Moscow")
print(ts_moscow)

# %%
# Tz-aware Timestamp objects are stored a nanoseconds since Unix epoch (1970-01-01).
# This is not changed when tz conversions are applied.

print(ts_utc)
print(type(ts_utc))
print(ts_utc.value)
print(ts_utc.tz_convert("America/New_York").value)

# %% [markdown]
# ### Operations between different time zones
#
# - If two time series with different time zones are combined, the result is UTC

# %%
rng = pd.date_range("3/7/2012 9:30", periods=6, freq="B")
ts = pd.Series(np.random.randn(len(rng)), index=rng)
print(ts)

# %%
ts1 = ts.tz_localize("Europe/London")
ts2 = ts1.tz_convert("Europe/Moscow")

print(ts1)
print(ts2)

# %%
print(ts1 + ts2)

# %% [markdown]
# ## Periods and period arithmetic
#
# - Periods represent timespans (e.g., days, months, quarters, years)

# %%
# Freq is the same frequencies used for other applications.

# E.g., 'A-DEC' means annual dates anchored to the end last cander of Dec.
p = pd.Period(2007, freq="A-DEC")
p

# %%
p + 5

# %%
p - 2

# %%
# Distance of periods in terms of periods.
p2 = pd.Period("2014", freq="A-DEC")
print("p2=", p2)
print("p =", p)
print("p2-p=", p2 - p)

# %%
# Date range with monthly cadence.
rng1 = pd.date_range("2000-01-01", "2000-06-30", freq="M")
print(rng1)

# %%
ts1 = pd.Series(np.random.randn(len(rng1)), index=rng1)
print(ts1)

print(type(ts1.index))
print(type(ts1.index[0]))

# %%

# %%
# Period range with monthly cadence.
rng2 = pd.period_range("2000-01-01", "2000-06-30", freq="M")
print(rng2)

# %%
# A PeriodIndex stores a sequence of periods
# It can be used as an axis index, like a DatetimeIndex.
ts2 = pd.Series(np.random.randn(len(rng2)), index=rng2)
print(ts2)

print(type(ts2.index))
print(type(ts2.index[0]))

# %%
values = ["2001Q3", "2002Q2", "2003Q1"]

index = pd.PeriodIndex(values, freq="Q-DEC")
print(index)

# %% [markdown]
# ### Period frequency conversion
#
# - One can convert a PeriodIndex to another frequency

# %%
# A period for 2007 anchored to end of Dec.
p = pd.Period("2007", freq="A-DEC")
p

# %%
p.asfreq("M", how="start")

# %%
p.asfreq("M", how="end")

# %%
# Consider a year ending at the end of June.
p = pd.Period("2007", "A-JUN")
p

# %%
p.asfreq("M", how="start")

# %%
p.asfreq("M", how="end")

# %%
# Also PeriodIndex can be converted to

rng = pd.period_range("2006", "2009", freq="A-DEC")
ts = pd.Series(np.random.randn(len(rng)), index=rng)
print(ts)

# %%
# Pick the first month of the year period ending in Dec.
ts.asfreq("M", how="start")

# %%
# Use the last business day of the period.
ts.asfreq("B", how="end")

# %% [markdown]
# ### Quarterly period frequencies
#
# - Quarterly data is standard in accounting and finance
# - Quarterly data is reported relative to fiscal year end (typically the last calendar or business day of one of the 12 months of the year)

# %%
# 4th quarter, with fiscal year end in Jan.
p = pd.Period("2012Q4", freq="Q-JAN")
p

# %%
# The 4th quarter is:
p.asfreq("D", "start"), p.asfreq("D", "end")

# %%
# Get a timestamp at 4pm on second-to-last business day of the quarter.

ts = (p.asfreq("B", "end") - 1).asfreq("T", "s") + 16 * 60
print(ts)

# %% [markdown]
# ### Converting timestamps to periods (and back)
#
# - periods always refer to non-overlapping timestamps
# - a timestamp can only belong to a single period for a given frequency

# %%
rng = pd.date_range("1/1/2000", periods=3, freq="M")
rng

# %%
ts = pd.Series(randn(3), index=rng)
ts

# %%
# to_period() infers the frequency automatically
# In practice it uses the same frequency of the timeseries.
pts = ts.to_period()
print(pts)

# %%
rng = pd.date_range("1/29/2000", periods=6, freq="D")
ts2 = pd.Series(randn(6), index=rng)

print(ts2)

# %%
# Convert each timestamp to the including period.
# Note that the frequency of timestamp and periods are different.
ts2.to_period("M")

# %%
pts2 = ts2.to_period()
print(pts2)

# %%
pts2.index

# %%
# Converting back to timestamps.
pts2 = ts2.to_period("M")
print(pts2)

print(pts2.to_timestamp(how="end"))

# %% [markdown]
# ### Creating a PeriodIndex from arrays
#
# - If the timespan information are stored in multiple columns, the constructor of PeriodIndex can gather them and use them

# %%
# !ls /Users/gp/src/github/pydata-book/examples

# %%
data = pd.read_csv("~/src/github/pydata-book/examples/macrodata.csv")
data.head()

# %%
print(data.head()[["year", "quarter"]])

# %%
index = pd.PeriodIndex(year=data.year, quarter=data.quarter, freq="Q-DEC")

print(index)

# %%
data.index = index
data.infl.head()

# %% [markdown]
# ## Resampling and frequency conversion
#
# - Resampling = converting a time series from one frequency to another
# - Downsampling = aggregating higher frequency data to lower frequency
# - Upsampling = converting lower frequency data to higher frequency
# - Some operations are not down or upsampling
#     - E.g., converting from W-WED (weekly on Wednesday) to W-FRI

# %%
rng = pd.date_range("1/1/2000", periods=100, freq="D")

ts = pd.Series(randn(len(rng)), index=rng)
ts.head()

# %%
# Resample daily data to monthly using mean to aggregate.
# ts.resample('M', how="mean")
ts.resample("M").mean()

# %%
ts.resample("M", kind="period").mean()

# %% [markdown]
# - options for resample()
# - freq: string (e.g., 'M', '5min') or DateOffset (e.g., Second(15)) indicating resampled frequency
# - how: function name or function aggregating values
#     - e.g., mean, ohlc, np.max, first, last, median
# - fill_method: how to interpolate when upsampling
#     - e.g., ffill, bfill
# - limit: when filling the maximum number of periods to fill
# - closed: in downsampling which end of the interval is closed, i.e., inclusive
#     - e.g., right, left
# - label: in downsampling how to label the aggregated result with the right or left bin edge
#     - e.g., we can sample 5-min interval [9:30, 9:35) and label it 9:30 or 9:35
# - loffset: time adjustment to bin labels to shift aggregate labels

# %% [markdown]
# ### Downsampling
#
# - Aggregating data to a regular, lower frequency is a normal time series task
# - The data doesn't need to be fixed
#     - The desired frequency defines bin edges used to aggregate
#     - Partition
#         - Each interval is half-open, since each point can only belong to one interval
#         - The union of all intervals must make up the whole time frame
#
# - When sampling
#     - which side of each interval is closed
#     - how to label each aggregated bin (beginning or end)

# %%
# Generate minute data.
rng = pd.date_range("1/1/2000", periods=12, freq="T")
ts = pd.Series(np.arange(len(rng)), index=rng)

ts

# %%
# Aggregate data into 5-min chunks or bars by taking the sum.
# ts.resample('5min', how="sum")
print(ts.resample("5min", closed="left", label="left").sum())

# This is the default.
print(ts.resample("5min").sum())

# %%
ts.resample("5min", closed="left", label="right").sum()

# %%
ts.resample("5min", closed="right", label="left").sum()

# %%
print(ts.resample("5min", closed="right", label="right").sum())

# %%
# If you want to shift the index.
# This is equivalent to calling shift() after resampling
ts.resample("5min", how="sum", loffset="-1s")

# %% [markdown]
# #### OHLC resampling

# %%
ts.resample("5min").ohlc()

# %% [markdown]
# #### Resampling with GroupBy
#
# - One can group by and then compute mean

# %%
rng = pd.date_range("1/1/2000", periods=100, freq="D")
ts = pd.Series(np.arange(100), index=rng)
print(ts.head())

# %%
ts.groupby(lambda x: x.month).mean()

# %% [markdown]
# ### Upsampling
#
# - When converting from lower to higher frequency, no aggregation is needed

# %%
frame = pd.DataFrame(
    np.random.randn(2, 4),
    index=pd.date_range("1/1/2000", periods=2, freq="W-WED"),
    columns="Colorado Texas NY Ohio".split(),
)
frame[:5]

# %%
# When resampling to daily frequency, missing values are introduced.

# frame.resample("D", fill_method="ffill")
frame.resample("D").ffill()

# %%
frame.resample("D").ffill(limit=2)

# %% [markdown]
# ### Resampling with periods

# %%
frame = pd.DataFrame(
    np.random.randn(24, 4),
    index=pd.period_range("1-2000", "12-2001", freq="M"),
    columns="Colorado Texas NY Ohio".split(),
)
frame[:5]

# %%
annual_frame = frame.resample("A-DEC").mean()
annual_frame

# %% [markdown]
# ## Time series plotting

# %%
# !ls ~/src/github/pydata-book/examples

# %%
close_px_all = pd.read_csv(
    "~/src/github/pydata-book/examples/stock_px.csv",
    index_col=0,
    parse_dates=True,
)

close_px_all.head()

# %%
close_px = close_px_all["AAPL MSFT XOM".split()]

close_px.head()

# %%
close_px = close_px.resample("B", fill_method="ffill")

# %%
close_px.head()

# %%
close_px["AAPL"].plot()

# %%
close_px["2009"].plot()

# %%
close_px["AAPL"].loc["01-2011":"03-2011"].plot()

# %%
# Quarterly data is nicely formatted with quarterly markers.
# aapl_q = close_px["AAPL"].resample("Q-DEC", fill_method="ffill")
aapl_q = close_px["AAPL"].resample("Q-DEC").ffill()
aapl_q["2009":].plot()

# %%

# %% [markdown]
# ## Moving window functions
#
# - Common operations are statistics evaluated over a sliding window, with
#   exponentially decaying weights

# %%
close_px.AAPL.plot()

# One needs to specify the number of non-na observations.
# pd.rolling_mean(close_px.AAPL, 250).plot()
close_px.rolling(window=250, center=False).mean().plot()

# %%
# pd.rolling_std(close_px.AAPL, 250, min_periods=10).plot()
close_px.AAPL.rolling(min_periods=10, window=250, center=False).std().plot()

# %%
expanding_mean = lambda x: pd.rolling_mean(x, len(x), min_periods=1)

# %%
# pd.rolling_mean(close_px, 60).plot(logy=True)
close_px.rolling(window=60, center=False).mean().plot(logy=True)

# %%
close_px.AAPL.rolling(window=60, center=False).count().plot()

# %%
close_px.AAPL.rolling(window=60, center=False).skew().plot()

# %%
close_px.AAPL.rolling(window=60, center=False).kurt().plot()

# %%
# rolling.apply(): apply a generic function over a moving window
# ewma, ewmvar, ewmstd, ewmcorr, ewmcov: exp-weighted moving *

# %% [markdown]
# ### Exponentially-weighted functions
#
# - Instead of specifying a static window size with equally-weighted observations,
#   specify a constant decay factor to give more weight to more reent observations
#
#   $$ma_t = a \cdot ma_{t-1} + (a-1) \cdot x_t$$

# %%
fig, axes = plt.subplots(
    nrows=1, ncols=1, sharex=True, sharey=True, figsize=(12, 5)
)

aapl_px = close_px.AAPL["2005":"2009"]
ma60 = aapl_px.rolling(60, min_periods=50).mean()
ewma60 = aapl_px.ewm(span=60, min_periods=60).mean()

aapl_px.plot(style="k-", ax=axes)
ma60.plot(style="b--", ax=axes, label="ma")
ewma60.plot(style="r--", ax=axes, label="ewma")

plt.legend()

# %% [markdown]
# ### Binary moving window functions

# %%
# Some operators (e.g., corr, cov) operate on 2 time series.
spx_px = close_px_all.SPX["2005":"2009"]
spx_rets = spx_px / spx_px.shift(1) - 1

returns = close_px.pct_change()

display(spx_rets.head())
display(returns.head())

# corr = pd.rolling_corr(returns.AAPL, spx_rets, 125, min_periods=100)
corr = returns.AAPL.rolling(125, min_periods=100).corr(spx_rets)
corr.dropna().plot(figsize=(15, 6))

# %%
# Multiple columns of a data-frame vs a series.
display(returns.head())
display(spx_rets.head())

corr = returns.rolling(125, min_periods=100).corr(spx_rets)
corr.dropna().plot(figsize=(15, 6))

# %% [markdown]
# ### User-defined moving window functions

# %%
# rolling_apply)() allows to apply an array function over a moving function.
# The function needs to produce a single function

from scipy.stats import percentileofscore

score_at_2pct = lambda x: percentileofscore(x, 0.02)
# result = pd.rolling_apply(returns.AAPL, 250, score_at_2pct)
# pandas 0.22
result = returns.AAPL.rolling(250).apply(score_at_2pct)

result.plot()

# %%
TODO
