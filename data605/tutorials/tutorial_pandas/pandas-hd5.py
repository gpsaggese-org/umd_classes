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
#  <p><div class="lev2 toc-item"><a href="#Imports" data-toc-modified-id="Imports-01"><span class="toc-item-num">0.1&nbsp;&nbsp;</span>Imports</a></div><div class="lev1 toc-item"><a href="#Misc" data-toc-modified-id="Misc-1"><span class="toc-item-num">1&nbsp;&nbsp;</span>Misc</a></div><div class="lev2 toc-item"><a href="#Multiply-df-by-series" data-toc-modified-id="Multiply-df-by-series-11"><span class="toc-item-num">1.1&nbsp;&nbsp;</span>Multiply df by series</a></div><div class="lev2 toc-item"><a href="#Index-minute-and-hour" data-toc-modified-id="Index-minute-and-hour-12"><span class="toc-item-num">1.2&nbsp;&nbsp;</span>Index minute and hour</a></div><div class="lev3 toc-item"><a href="#Merging-a-column-to-all-dfs-into-a-panel" data-toc-modified-id="Merging-a-column-to-all-dfs-into-a-panel-121"><span class="toc-item-num">1.2.1&nbsp;&nbsp;</span>Merging a column to all dfs into a panel</a></div><div class="lev1 toc-item"><a href="#hdf5-format" data-toc-modified-id="hdf5-format-2"><span class="toc-item-num">2&nbsp;&nbsp;</span>hdf5 format</a></div><div class="lev2 toc-item"><a href="#Write-/-read-h5-objects" data-toc-modified-id="Write-/-read-h5-objects-21"><span class="toc-item-num">2.1&nbsp;&nbsp;</span>Write / read h5 objects</a></div><div class="lev2 toc-item"><a href="#Read-/-write-objects" data-toc-modified-id="Read-/-write-objects-22"><span class="toc-item-num">2.2&nbsp;&nbsp;</span>Read / write objects</a></div><div class="lev2 toc-item"><a href="#Fixed-vs-table-format." data-toc-modified-id="Fixed-vs-table-format.-23"><span class="toc-item-num">2.3&nbsp;&nbsp;</span>Fixed vs table format.</a></div><div class="lev3 toc-item"><a href="#Fixed-format." data-toc-modified-id="Fixed-format.-231"><span class="toc-item-num">2.3.1&nbsp;&nbsp;</span>Fixed format.</a></div><div class="lev3 toc-item"><a href="#Table-format" data-toc-modified-id="Table-format-232"><span class="toc-item-num">2.3.2&nbsp;&nbsp;</span>Table format</a></div><div class="lev2 toc-item"><a href="#Table-format" data-toc-modified-id="Table-format-24"><span class="toc-item-num">2.4&nbsp;&nbsp;</span>Table format</a></div><div class="lev3 toc-item"><a href="#Hierarchical-keys" data-toc-modified-id="Hierarchical-keys-241"><span class="toc-item-num">2.4.1&nbsp;&nbsp;</span>Hierarchical keys</a></div><div class="lev3 toc-item"><a href="#Querying" data-toc-modified-id="Querying-242"><span class="toc-item-num">2.4.2&nbsp;&nbsp;</span>Querying</a></div>

# %% [markdown]
# ## Imports

# %% run_control={"marked": false}

import numpy as np
import pandas as pd

# %matplotlib inline

# %%
import notebook_utils

notebook_utils.notebook_config()

from notebook_utils import display_df, delete_file_name

# %% [markdown]
# # Misc

# %% [markdown]
# ## Multiply df by series

# %%
index = pd.date_range("2010-01-01", "2010-01-10")

np.random.seed(42)

df = pd.DataFrame(np.random.rand(len(index), 2), index=index, columns=["a", "b"])
srs = pd.Series(np.random.rand(len(index)), index=index)

display_df(df)
display_df(srs)

# %%
df.multiply(srs, axis=0)

# %% [markdown]
# ## Index minute and hour

# %%
index = pd.date_range("2010-01-01", "2010-01-02", freq="2H")

np.random.seed(42)

df = pd.DataFrame(np.random.rand(len(index), 2), index=index, columns=["a", "b"])
display_df(df)

# %%
print(df.index.hour)

# %%
print(df.index.minute)

# %% [markdown]
# ### Merging a column to all dfs into a panel

# %%
panel = notebook_utils.get_random_panel()

print(panel)

# %%
index_rets = pd.date_range("2001-01-01", "2001-01-7")
columns = ["c"]
rets = notebook_utils.get_random_dataframe(index=index_rets, columns=columns)
print(rets)

# %%
panel_tmp = panel.copy()
panel_tmp.loc[:, :, "c"] = rets["c"]
print(panel_tmp)

# Note that the new column is not merged.

# %%
panel_tmp = panel.copy()
panel_tmp.join(df)

# %%
pd.concat([rets, panel_tmp], join="outer")

# %% [markdown]
# # hdf5 format
#
# - reading, saving slicing columns and indices

# %% [markdown]
# ## Write / read h5 objects

# %%
file_name = "store.h5"

store = pd.HDFStore(file_name)

print(store)

# %%
np.random.seed(1234)

index = pd.date_range("1/1/2000", periods=8)
s = pd.Series(randn(5), index="a b c d e".split())
print("# s=\n", s)

df = pd.DataFrame(randn(8, 3), index=index, columns="A B C".split())
print()
print("# df=\n", df)

wp = pd.Panel(
    rand(2, 5, 4),
    items="Item1 Item2".split(),
    major_axis=pd.date_range("1/1/2000", periods=5),
    minor_axis="A B C D".split(),
)
print()
print("# wp=\n", wp)

# %%
store["s"] = s
store["df"] = df
store["wp"] = wp

print(store)

# %%
store.close()

# %%
# Using context manager.
with pd.HDFStore(file_name) as store:
    print(list(store.keys()))

# %%
delete_file_name(file_name)

# %% [markdown]
# ## Read / write objects

# %%
file_name = "store_t1.h5"
delete_file_name(file_name)

# Write.
df_tl = pd.DataFrame(dict(A=list(range(5)), B=list(range(5))))
display(df_tl)
df_tl.to_hdf(file_name, "table", append=True)

# Read with filtering.
pd.read_hdf(file_name, "table", where=["index>2"])

# %%
df_with_missing = pd.DataFrame(
    {
        "col1": [0, np.nan, 2],
        "col2": [1, np.nan, np.nan],
    }
)

display_df(df_with_missing)

df_with_missing.to_hdf(
    # File.
    file_name,
    # Name of dict key.
    "df_with_missing",
    #
    format="table",
    mode="w",
)

df = pd.read_hdf(file_name, "df_with_missing")
display_df(df)

# %%
delete_file_name(file_name)

# %% [markdown]
# ## Fixed vs table format.

# %% run_control={"marked": false}
from timeit import default_timer
import time


def _convert_bytes(nbytes, unit="B"):
    if unit == "B":
        res = nbytes
    elif unit == "MB":
        res = float(nbytes / (1024 * 1024))
    else:
        raise ValueError("Invalid unit='%s'" % unit)
    return res


def pd_size(df, unit="B"):
    # nbytes obj.values.nbytes + obj.index.nbytes + obj.columns.nbytes
    nbytes = df.memory_usage().sum()
    res = _convert_bytes(nbytes, unit=unit)
    return res


def file_size(file_name, unit="B"):
    nbytes = os.stat(file_name).st_size
    res = _convert_bytes(nbytes, unit=unit)
    return res


class timer:
    def __init__(self):
        pass

    def __enter__(self):
        self.start = default_timer()
        return self

    def __exit__(self, *args):
        self.end = default_timer()
        self.elapsed = self.end - self.start
        print("time=%.1f s" % self.elapsed)


with timer() as timer_:
    print("test")
    time.sleep(0.1)


print(timer_)

# %%
exps = []

# %%
with timer() as timer_:
    idx = pd.date_range("1/1/2010", "1/1/2017", freq="1Min")
    cols = ["bid", "ask"]
    df = pd.DataFrame(
        np.random.randn(len(idx), len(cols)), index=idx, columns=cols
    )
    df["start.dt"] = df.index
    df["end.dt"] = df.index.shift(1)

print(idx[:5])
print("shape=", idx.shape)
display(df.head())

with timer() as timer_:
    mem = pd_size(df, unit="MB")
    print("memory=%.1f MB" % mem)

exps.append(["create_df", timer_.elapsed, mem])

orig_df = df.copy()

# %% [markdown]
# ### Fixed format.
#
# - fixed stores
#   - are not appendable once written: one needs to remove and rewrite
#   - are not queryable: they must be retrieve in their entirety
#   - do not support data frames with duplicated column names
#   - very fast writing and slightly faster reading than table stores

# %% run_control={"marked": false}
file_name = "./test.fixed.h5"
delete_file_name(file_name)

exp = "write_all_data.fixed"
print("#", exp)

# Write all data.
with timer() as timer_:
    df.to_hdf(file_name, "df", format="fixed")

mem = file_size(file_name, unit="MB")
print("size=%.1f MB" % mem)

exps.append([exp, timer_.elapsed, mem])

# %%
# Read all data.

exp = "read_all_data.fixed"
print("#", exp)

with timer() as timer_:
    df = pd.read_hdf(file_name, "df")
    _ = df.head(), df.tail()

mem = pd_size(df, unit="MB")
print("memory=%.1f MB" % mem)

exps.append([exp, timer_.elapsed, mem])

# %% [markdown]
# ### Table format

# %%
file_name = "./test.table.h5"
delete_file_name(file_name)

exp = "write_all_data.table"

# Write all data.
print("# ", exp)
with timer() as timer_:
    df.to_hdf(file_name, "df", format="table")

mem = file_size(file_name, unit="MB")
print("size=%.1f MB" % mem)

exps.append([exp, timer_.elapsed, mem])

# %%
# Read all data.
exp = "read_all_data.table"
print("#", exp)

with timer() as timer_:
    df = pd.read_hdf(file_name, "df")
    _ = df.head(), df.tail()

mem = pd_size(df, unit="MB")
print("memory=%.1f MB" % mem)

exps.append([exp, timer_.elapsed, mem])

# %%
# Read all with index.
exp = "read_all_data_with_index.table"
print("#", exp)

with timer() as timer_:
    df = pd.read_hdf(file_name, "df", where="index > pd.Timestamp('2010-01-01')")
    _ = df.head(), df.tail()

mem = pd_size(df, unit="MB")
print("memory=%.1f MB" % mem)

exps.append([exp, timer_.elapsed, mem])

# %%
# Read 1/2 data with index.
exp = "read_1/2_data_with_index.table"
print("#", exp)

with timer() as timer_:
    df = pd.read_hdf(file_name, "df", where="index > pd.Timestamp('2013-06-01')")
    _ = df.head(), df.tail()

mem = pd_size(df, unit="MB")
print("memory=%.1f MB" % mem)

exps.append([exp, timer_.elapsed, mem])

# %%
exps_df = pd.DataFrame(exps, columns=["exp", "time [s]", "size [MB]"])
display(exps_df)

# %%
col = exps_df[["exp", "time [s]"]]
col.set_index("exp", inplace=True)


def print_stats(c1, c2):
    speedup = (float(col.loc[c1]) / col.loc[c2]).values[0]
    tag = "slower"
    if speedup < 1:
        speedup = 1.0 / speedup
        tag = "faster"
    print("%s / %s = %.1fx %s" % (c1, c2, speedup, tag))


print_stats("write_all_data.fixed", "read_all_data.fixed")
print_stats("write_all_data.table", "read_all_data.table")

print()
print_stats("write_all_data.fixed", "write_all_data.table")
print_stats("read_all_data.fixed", "read_all_data.table")

print()
print_stats("read_all_data.table", "read_all_data_with_index.table")

# %% [markdown]
# ## Table format
#
# - table is shaped like a data frame with rows and columns
# - one can add, delete and query

# %%
file_name = "store.h5"
delete_file_name(file_name)

store = pd.HDFStore(file_name)

df = pd.DataFrame(randn(8, 3), index=index, columns=["A", "B", "C"])

# Append to a df.
df1 = df[0:4]
store.append("df", df1)

df2 = df[4:]
store.append("df", df2)

print(store)
print(store.select("df"))

# %% [markdown]
# ### Hierarchical keys
#
# - keys are string that can be path-name like format

# %%
store.put("foo/bar/bah", df)
store.append("food/orange", df)
store.append("food/apple", df)

print("store=\n", store)
print("\nstore.keys=", list(store.keys()))

# Remove everything under the hierarchy 'food'.
store.remove("food")

print("\nstore=\n", store)

# %% [markdown]
# ### Querying

# %%
file_name = "./test.table.h5"
store = pd.HDFStore(file_name)

print("store=\n", store)

# %%
df_tmp = store.select("df", "index > pd.Timestamp('2013-06-01')")

print(df_tmp.shape)
display_df(df_tmp.head())

# %%
df_tmp = store.select("df", "index == pd.Timestamp('2013-06-01')")

print(df_tmp.shape)
display_df(df_tmp.head())

# %%
df_tmp = store.select(
    "df", "index > pd.Timestamp('2013-06-01') & columns == ['bid']"
)

print(df_tmp.shape)
display_df(df_tmp.head())

# %%
# TODO: Finish this.
