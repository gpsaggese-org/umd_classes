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
# # Dask Array in 3 minutes
#
# // From https://www.youtube.com/watch?v=9h_61hXCDuI)

# %%
def print_obj(obj, tag=None):
    """
    Print an object in terms of type and then display is.
    """
    if tag:
        print(tag)
    print("type=", type(obj))
    display(obj)


def print_dask(obj, visualize_graph=True, compute=True):
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
    if visualize_graph:
        print("# visualize")
        display(obj.visualize())
    #
    if compute:
        print("# compute")
        res = obj.compute()
        print(type(res))
        print(res)


# %%
# https://stackoverflow.com/questions/59070260/dask-client-detect-local-default-cluster-already-running
import os

os.environ["DASK_SCHEDULER_ADDRESS"] = "tcp://localhost:8787"

if not ("cluster" in globals() and "client" in globals()):
    from dask.distributed import Client, LocalCluster

    cluster = LocalCluster(dashboard_address=":8787")
    client = Client(cluster)
    print(client, client.dashboard_link)

# %% [markdown]
# ## Small array

# %%
import numpy as np

x = np.ones(15)
x

# %%
import dask.array as da

x = da.ones(15, chunks=(5,))
x

# %%
# The return type is a scalar.
x.sum()

# %%
# Dask is lazy by default.
x.sum().compute()

# %% [markdown]
# ## Medium array

# %%
x = da.ones((10_000, 10_000), chunks=(5000, 5000))
print_dask(x)

# %%
y = x + x.T

print_dask(y)

# %%
y.compute()

# %% [markdown]
# ## Larger array

# %%
x = da.ones((10_000, 10_000), chunks=(1000, 1000))
x

# %%
y = x + x.T
print_dask(y)

# %%
y.compute()

# %% [markdown]
# # Dask DataFrame: An introduction
#
# // https://www.youtube.com/watch?v=AT2XtFehFSQ&t=37s

# %%
import dask
import dask.dataframe as dd

# Get an example large dataset.
df_orig = dask.datasets.timeseries()
print_obj(df_orig)

# It has 30 partitions.

# %%
# Save to disk in chunks.
df_orig.to_csv("data")
# !ls -lh data

# %%
# Load one chunk.
import pandas as pd

df = pd.read_csv("data/00.part", parse_dates=["timestamp"])
df

# %%
df.x.mean()

# %%
df.groupby("name").x.std()

# %%

# Read one partition with Dask.
# df = dd.read_csv("data/00.part", parse_dates=["timestamp"])

# Read all partitions with Dask.
df = dd.read_csv("data/*.part", parse_dates=["timestamp"])

print_obj(df)

# head() materializes the data.
df.head()

# %%
# We get a "lazy result". Dask reads from disk only when one asks for a result.
obj = df.x.mean()

print_obj(obj)

# %%
print_dask(obj, compute=False)

# %%
df.x.mean().compute()

# %%
obj = df.groupby("name").x.std()

obj.compute()

# %% [markdown]
# ## Index, partitions, and sorting

# %%
# The original data read is made of 30 partitions.
# Each partition can be read in parallel and independently.
df

# %%
df.partitions[5]

# %%
obj = df.partitions[5].compute()

print_obj(obj)

# %%
# Apply a function across all the partitions.
# df.map_partitions(type).compute()
df.map_partitions(len).compute()

# %%
# Read the first partition.
df.head()

# %%
# Read the last partition.
df.tail()

# %%
# This forces Dask to read the data but it doesn't compute.
df = df.set_index("timestamp")
print_obj(df)

# The partitions host data between two different timestamps.
# In this way Dask knows in which file chunks of data.

# %%
# Save files to Parquet.
df.to_parquet("myfile.parquet")

# %%
# !ls myfile.parquet

# %% [markdown]
# # Dask Bag
#
# From https://www.youtube.com/watch?v=-qIiJ1XtSv0

# %%
import dask.bag as db

# Create a bag storing 10 elements.
b = db.from_sequence([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], npartitions=4)
print_obj(b)

# %%
# This produces a new bag.
obj = b.map(lambda x: x**2)

print_obj(b)

# %%
# Execute.
obj.compute()

# %%
# One can chain computations: e.g., filter, square and sum.
obj = b.filter(lambda x: x % 2 == 0).map(lambda x: x**2).sum()
print_obj(obj)

# %%
print_dask(obj)

# %%
obj.compute()

# %% [markdown]
# ## An example with JSON data

# %%
# #!wget https://archive.analytics.mybinder.org/events-2019-06-17.jsonl

# %%
# !pip install aiohttp requests

# %%
import os
import requests

# os.system("rm -rf data_json")
os.system("mkdir data_json")

for month in range(6, 7):
    for day in range(1, 30):
        file = "events-2019-%02d-%02d.jsonl" % (month, day)
        dst_file = f"data_json/{file}"
        print(dst_file)
        if os.path.exists(dst_file):
            continue
        url = "https://archive.analytics.mybinder.org/%s" % file
        print(url)
        r = requests.get(url, allow_redirects=True)
        open(dst_file, "wb").write(r.content)


# %%
# !ls data_json/*
# !du -h data_json

# %%
# !head data_json/events-2019-06-14.jsonl

# !du -h data_json/events-2019-06-14.jsonl

# %%
import dask.bag as db

# Read a single file.
# lines = db.read_text("data_json/events-2019-06-14.jsonl")

# Read all files.
lines = db.read_text("data_json/events-*.jsonl")

# Read the first 2 lines.
lines.take(2)

# %%
# It has a certain number of partitions, one per original file.
lines

# %%
# Transform the JSON lines into structured data.
import json

records = lines.map(json.loads)
records.take(2)

# %%
# Do a frequency count to find binders that run the most often.
records.map(lambda d: d["spec"]).frequencies(sort=True).compute()

# %%
# Look for records that have "dask" in the specs.
obj = records.filter(lambda d: "dask" in d["spec"])

# Convert to strings and saves.
obj = obj.map(json.dumps).to_textfiles("data/analysis/*.json")

# %%
# !ls -l data/analysis

# %%
# !head -20 data/analysis/00.json

# %%
# Instead of using Bag, one can use DataFrame.

df = records.to_dataframe()
print_obj(df)

# It still a lazy result.

# %%
df.spec.value_counts().nlargest(20).to_frame().compute()

# %% [markdown]
# # Dask Futures in 11 minutes
#
# https://www.youtube.com/watch?v=07EiCpdhtDE

# %%
import time


def inc(x):
    """
    Take some time to compute and do a small computation.
    """
    time.sleep(1)
    return x + 1


# %%
# %%time
inputs = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
results = []

for x in inputs:
    result = inc(x)
    results.append(result)


# This should take 10 secs since everything is executed serially.

# %% [markdown]
# ## concurrent.futures

# %%
# Dask Futures has the same interface as concurrent.futures.
# if True:
if False:
    from concurrent.futures import ThreadPoolExecutor

    e = ThreadPoolExecutor(4)
else:
    from concurrent.futures import ProcessPoolExecutor

    e = ProcessPoolExecutor(4)

# Threads and processes have the same interface but different performance characteristics.
e

# %%
# %%time

future = e.submit(inc, 10)
future

# Submit is instantaneous, but you can see that the future is still running.

# %%
# After a bit of time, the task is done.
print(future)
print(future.result())

# %%
# %%time

# Run the workload above in parallel.

inputs = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
futures = []

for x in inputs:
    future = e.submit(inc, x)
    futures.append(future)

results = [future.result() for future in futures]
print(results)

# With 4 threads and 10 pieces of workload, it takes at least 3 batches (i.e., 3 secs).

# %% [markdown]
# ## Dask Futures

# %%
client

# %%
# %%time

futures = []

for x in inputs:
    # Dask Client has the same interface as futures.concurrent and can be used as an Executor.
    future = client.submit(inc, x)
    futures.append(future)

results = [future.result() for future in futures]
print(results)

# %% [markdown]
# ## Executing work remotely

# %%
import numpy as np

# This creates an array on a remote worker.
future = client.submit(np.arange, 100)
future

# %%
# When the future is finished, the data is not moved back to the client.
future

# %%
client.submit(np.sum, [1, 2, 3]).result()

# %%
# We can call np.sum on the remote array and bring back only the result.
client.submit(np.sum, future).result()

# %%
##
import numpy as np


def load(x):
    """
    Get a sizable array.
    """
    time.sleep(0.2)
    return np.arange(1_000_000) + x


def process(x):
    time.sleep(0.1)
    return x + 1


def save(x):
    time.sleep(0.4)


# %%
# %%time

inputs = range(50)

for i in inputs:
    x = load(i)
    y = process(x)
    save(y)

# It takes (0.2 + 0.1 + 0.4) * 50 = 0.7 * 50 = 35s

# %%
# %%time

inputs = range(50)

futures = []
for i in inputs:
    x = client.submit(load, i)
    y = client.submit(process, x)
    z = client.submit(save, y)
    futures.append(z)

result = [future.result() for future in futures]

# %%
## The same code can be written in a similar way as in the following.

L = [client.submit(load, i) for i in range(200)]
# The following line is equivalent to:
# L2 = [client.submit(process, x) for x in futures]
L2 = client.map(process, L)
L3 = client.map(save, L2)

# The problem is that the memory increases since we keep the futures are kept around
# and thus Dask can't allocate the memory.

# %%
# In fact
L[:5]

# %%
L[3].result()

# %%
# If you delete the futures, Dask can remove them.
del L
del L2
