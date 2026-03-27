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
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %% [markdown]
# # 10 minutes to Dask
#
# https://docs.dask.org/en/stable/10-minutes-to-dask.html

# %%
def print_obj(obj, tag=None):
    """
    Print an object in terms of type and then display is.
    """
    if tag:
        print(tag)
    print("type=", type(obj))
    display(obj)


def print_dask(obj):
    """
    Print information about a dask task graph.
    """
    print("type=", type(obj))
    print("obj=", obj)
    #
    print("# display")
    display(obj)
    #
    print("# dask")
    display(obj.dask)
    #
    print("# visualize")
    display(obj.visualize())
    #
    print("# compute")
    res = obj.compute()
    print(type(res))
    print(res)


# %% [markdown]
# ## DataFrame

# %% [markdown]
# ### Creating an object

# %%
import numpy as np
import pandas as pd

import dask.dataframe as dd
import dask.array as da
import dask.bag as db

# %%
# Create a df with 2400 rows indexed in datetimes.
index = pd.date_range("2021-09-01", periods=2400, freq="1H")
df = pd.DataFrame(
    {"a": np.arange(2400), "b": list("abcaddbe" * 300)}, index=index
)

# Print the df as Pandas and Dask df.
print_obj(df, "# Pandas df")

# %%
# Convert object into Dask.
ddf = dd.from_pandas(df, npartitions=10)
print_dask(ddf)

# %%
# Print the partitions, in terms of indices covered by each partition.
obj = ddf.divisions
print_obj(obj)

# %%
# Print one partition.
obj = ddf.partitions[1]
print_obj(obj)

# %% [markdown]
# ### Indexing

# %%
obj = ddf["b"]
print_dask(obj)

# %%
# This doesn't force to execute.
obj = ddf["2021-10-01":"2021-10-09 5:00"]
print_obj(obj)

# %%
print_dask(obj)

# %% [markdown]
# ### Computation

# %%
# Force to read, in fact the output is a Pandas DataFrame.
obj = ddf["2021-10-01":"2021-10-09 5:00"].compute()
print_obj(obj)

# %% [markdown]
# ### Methods

# %%
# Compute the mean of a column (delayed).
obj = ddf.a.mean()
print_obj(obj)

# %%
print_dask(obj)

# %%
# Note that the types are different.
obj = ddf["b"].unique().compute()
print_obj(obj)

obj = ddf["b"].compute().unique()
print_obj(obj)

# %%
# Methods can be chained together like in Pandas.
result = ddf["2021-10-01":"2021-10-09 5:00"].a.cumsum() - 100
print_obj(result)

# %%
# Materialize.
obj = result.compute()
print_obj(obj)

# %% [markdown]
# ### Visualize the Task Graph

# %%
# result = ddf["2021-10-01": "2021-10-09 5:00"].a.cumsum() - 100
# result is a graph.
print_dask(result)

# %% [markdown]
# ## Array

# %%
import numpy as np

# Create a 200 x 500 array.
data = np.arange(100_000).reshape(200, 500)
print(type(data), data.shape)
print("data=\n%s" % data)

# %%
# Split in 100x100 chunks.
a = da.from_array(data, chunks=(100, 100))
print_dask(a)

# There are 10 chunks.

# %%
a.chunksize

# %%
a.chunks

# %%
# Extract a block.
a.blocks[1, 3]

# %% [markdown]
# ### Indexing

# %%
# Slice.
# No computation is performed.
y = a[:50, 200]

# %%
print_dask(y)

# %%
# Computation.
a[:50, 200].compute()

# %% [markdown]
# ### Methods

# %%
y = a.mean()
print_dask(y)

# Returns a scalar.

# %%
y = np.sin(a)
print_dask(y)

# %%
y = a.T
print_dask(y)

# %%
b = a.max(axis=1)[::-1] + 10
print_dask(b)

# %% [markdown]
# ### Visualize the Task Graph

# %%
b.dask

# %%
b.visualize()

# %% [markdown]
# ## Bag

# %% [markdown]
# ### Creating a Dask object

# %%
# 8 items in two partitions.
b = db.from_sequence([1, 2, 3, 4, 5, 6, 2, 1], npartitions=2)

print_dask(b)

# %% [markdown]
# ### Indexing

# %% [markdown]
# ### Computation

# %%
b.compute()

# %% [markdown]
# ### Methods

# %%
obj = b.filter(lambda x: x % 2)

print_dask(obj)

# %%
obj.compute()

# %%
obj = b.distinct()
print_dask(obj)

# %%
obj.compute()

# %%
obj = db.zip(b, b.map(lambda x: x * 10))
print_dask(obj)


# %% [markdown]
# # Low-level interfaces

# %% [markdown]
# ## Delayed

# %%
# In the following example there is parallelism to exploit, but it doesn't fit one of
# the native Dask data structures.


def inc(x):
    return x + 1


def double(x):
    return x * 2


def add(x, y):
    return x + y


data = [1, 2, 3, 4, 5]

output = []
for x in data:
    # (x + 1) + (x * 2) = 3x + 1
    a = inc(x)
    b = double(x)
    c = add(a, b)
    # 1 -> 4
    # 2 -> 7
    # 3 -> 10
    # 4 -> 13
    # 5 -> 16
    output.append(c)

# 4 + 7 + 10 + 13 + 16 = 20 + 20 + 10 = 50
total = sum(output)
print(total)

# %%
# Decorate

import dask

# This is equivalent to the decorator.
# @dask.delayed
# def inc(x):
#     return x + 1


output = []
for x in data:
    a = dask.delayed(inc)(x)
    b = dask.delayed(double)(x)
    c = dask.delayed(add)(a, b)
    output.append(c)

total = dask.delayed(sum)(output)

total.dask

# %%
# This is the computation inside a node.
c.visualize()

# %%
# This is the unrolled computation.
total.visualize()

# %%
# Trigger the computation.
total.compute()

# %% [markdown]
# ## Futures

# %%
# https://stackoverflow.com/questions/59070260/dask-client-detect-local-default-cluster-already-running
import os

os.environ["DASK_SCHEDULER_ADDRESS"] = "tcp://localhost:8786"

if not ("cluster" in globals() and "client" in globals()):
    from dask.distributed import Client, LocalCluster

    cluster = LocalCluster(dashboard_address=":8787")
    client = Client(cluster)
    print(client, client.dashboard_link)

# %%
# import time
# from dask.distributed import Client, LocalCluster
# with LocalCluster(dashboard_address=':8787') as cluster:
#    with Client(cluster) as client:
#        print(client, client.dashboard_link)
# time.sleep(1)
# with LocalCluster(dashboard_address=':8787') as cluster:
#    with Client(cluster) as client:
#        print(client, client.dashboard_link)

# %%
from dask.distributed import Client, LocalCluster


def inc(x):
    return x + 1


def add(x, y):
    return x + y


# Submit and start eagerly.
a = client.submit(inc, 1)
b = client.submit(inc, 2)
c = client.submit(add, a, b)


# This is blocking until everything is completed.
c = c.result()

# %% [markdown]
# # Scheduling

# %%
# from dask.distributed import Client

# client = Client()
# client

# %%
client.dashboard_link
