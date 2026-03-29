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

# %%
## Transformations

# %%
## Actions

# %%
## Shuffle operation

# %%
## RDD persistence

# %%
## Shared variables

# %%
# Spark SQL

# %%
# Structured Streaming

# %%
# MLlib

# %%
# GraphX

# %% [markdown]
# # pyspark
#
# https://spark.apache.org/docs/latest/api/python/getting_started/index.html

# %%
# !pip install pandas

# %%
from pyspark.sql import SparkSession

spark = SparkSession.builder.getOrCreate()
# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.19.1
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %%
# https://spark.apache.org/docs/latest/quick-start.html

# %% [markdown]
# # Interactive analysis

# %% [markdown]
# ## Basics

# %%
textFile = spark.read.text("README.md")

# %%
# !head -5 README.md

# %%
print(textFile)

# %%
textFile.show()

# %%
# Print number of rows.
print(textFile.count())

# %%
textFile.collect()

# %%
textFile.first()

# %%
linesWithSpark = textFile.filter(textFile.value.contains("Spark"))
print(linesWithSpark.count())

# %% [markdown]
# ## More on Dataset Operations

# %%
from pyspark.sql.functions import *

# Split each line in words and count.
df = textFile.select(size(split(textFile.value, "\s+")))
df.show()

# %%
df = textFile.select(size(split(textFile.value, "\s+")).name("numWords"))
df.show()

# %%
# Find the max.
df.agg(max(col("numWords"))).collect()

# %%
# Implement map-reduce in one line.
wordCounts = (
    textFile.select(explode(split(textFile.value, "\s+")).alias("word"))
    .groupBy("word")
    .count()
)
wordCounts.show()

# %%
# Convert a dataset of lines into a dataset of words.
map_ = textFile.select(explode(split(textFile.value, "\s+")).alias("word"))
map_.show()

# %%
result = map_.groupBy("word").count()

# result.show()
result.collect()


# %% [markdown]
# # RDD Programming guide


# %%
class DisplayRDD:
    def __init__(self, rdd):
        self.rdd = rdd

    def _repr_html_(self):
        x = self.rdd.mapPartitionsWithIndex(lambda i, x: [(i, [y for y in x])])
        l = x.collect()
        s = "<table><tr>{}</tr><tr><td>".format(
            "".join(["<th>Partition {}".format(str(j)) for (j, r) in l])
        )
        s += '</td><td valign="bottom" halignt="left">'.join(
            [
                "<ul><li>{}</ul>".format("<li>".join([str(rr) for rr in r]))
                for (j, r) in l
            ]
        )
        s += "</td></table>"
        return s


# %%
data = list(range(20))

data_rdd = sc.parallelize(data)
print(data_rdd)

DisplayRDD(data_rdd)

# %%
data = list(range(20))

data_rdd = sc.parallelize(data, 10)
print(data_rdd)

DisplayRDD(data_rdd)

# %%
# Return one record per line.
states_rdd = sc.textFile("states.txt", 10)
print(states_rdd)
DisplayRDD(states_rdd)

# %% [markdown]
# ## Basics

# %%
# lines and lineLengths are not computed immediately (due to lazy execution).
lines = sc.textFile("states.txt")
lineLengths = lines.map(lambda s: len(s))
# reduce is an aciton and triggers the execution.
totalLength = lineLengths.reduce(lambda a, b: a + b)
print(totalLength)


# %% [markdown]
# ## Passing functions.


# %%
def myFunc(s):
    words = s.split(" ")
    return len(words)


lines = sc.textFile("states.txt")
lineLengths = lines.map(lambda s: myFunc(s))
# reduce is an aciton and triggers the execution.
totalLength = lineLengths.reduce(lambda a, b: a + b)
print(totalLength)

# %%
counter = 0
print(data)
rdd = sc.parallelize(data)


# Wrong: Don't do this!!
def increment_counter(x):
    global counter
    counter += x


rdd.foreach(increment_counter)

# The output is zero since the executors are updating the copy.
print("Counter value: ", counter)

# %%
lines = sc.textFile("states.txt") + sc.textFile("states.txt")
pairs = lines.map(lambda s: (s, 1))
counts = pairs.reduceByKey(lambda a, b: a + b)
print(counts.collect())

# %% [markdown]
# ## Pi

# %%
# Estimate π (compute-intensive task).
# Pick random points in the unit square [(0,0)-(1,1)].
# See how many fall in the unit circle center=(0, 0), radius=1.
# The fraction should be π / 4.

import random

random.seed(314)


def sample(p):
    x, y = random.random(), random.random()
    in_unit_circle = 1 if x * x + y * y < 1 else 0
    return in_unit_circle


# “parallelize” method creates an RDD.
NUM_SAMPLES = int(1e6)
count = (
    sc.parallelize(range(0, NUM_SAMPLES)).map(sample).reduce(lambda a, b: a + b)
)
approx_pi = 4.0 * count / NUM_SAMPLES
print("pi is roughly %f" % approx_pi)

# %% [markdown]
# ## Working with key-value pairs

# %%
# !more data.txt

# %%
lines = sc.textFile("data.txt").flatMap(lambda line: line.split(" "))
pairs = lines.map(lambda s: (s, 1))
counts = pairs.reduceByKey(lambda a, b: a + b)
result = counts.collect()
print(result)

# %%
result = (
    sc.textFile("data.txt")
    .flatMap(lambda line: line.split(" "))
    .map(lambda s: (s, 1))
    .reduceByKey(lambda a, b: a + b)
)
#     .collect()
print(result)
print(spark)

# %%
from datetime import datetime, date
from pyspark.sql import Row

df = spark.createDataFrame(
    [
        Row(
            a=1,
            b=2.0,
            c="string1",
            d=date(2000, 1, 1),
            e=datetime(2000, 1, 1, 12, 0),
        ),
        Row(
            a=2,
            b=3.0,
            c="string2",
            d=date(2000, 2, 1),
            e=datetime(2000, 1, 2, 12, 0),
        ),
        Row(
            a=4,
            b=5.0,
            c="string3",
            d=date(2000, 3, 1),
            e=datetime(2000, 1, 3, 12, 0),
        ),
    ]
)
df
