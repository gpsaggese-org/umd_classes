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

# %% [markdown]
# This Notebook shows introduces the basic concepts of RDDs and operations on them visually, by showing the contents of the RDDs as a table.

# %% [markdown]
# ### Display RDD
# The following helper functions displays the current contents of an RDD (partition-by-partition). This is best used for small RDDs with manageable number of partitions.

# %%
class DisplayRDD:
    def __init__(self, rdd):
        self.rdd = rdd

    def _repr_html_(self):                                  
        x = self.rdd.mapPartitionsWithIndex(lambda i, x: [(i, [y for y in x])])
        l = x.collect()
        s = "<table><tr>{}</tr><tr><td>".format("".join(["<th>Partition {}".format(str(j)) for (j, r) in l]))
        s += '</td><td valign="bottom" halignt="left">'.join(["<ul><li>{}</ul>".format("<li>".join([str(rr) for rr in r])) for (j, r) in l])
        s += "</td></table>"
        return s


# %% [markdown]
# ### Basics 1
# Lets start with some basic operations using a small RDD to visualize what's going on. We will create a RDD of Strings, using the `states.txt` file which contains a list of the state names.
#
# The notebook has already initialized a SparkContext, and we can refer to it as `sc`.
#
# We will use `sc.textFile` to create this RDD. This operations reads the file and treats every line as a separate object. We will use DisplayRDD() to visualize it. The second argument of `sc.textFile` is the number of partitions. We will set this as 10 to get started. If we don't do that, Spark will only create a single partition given the file is pretty small.

# %%
states_rdd = sc.textFile('states.txt', 10)
DisplayRDD(states_rdd)

# %% [markdown]
# The above table shows the contents of each partition as a list -- so the first Partition has 5 elements in it ('Alabama', ...). We can `repartition` the RDD to get a fewer partitions so it will be easier to see.

# %%
states_rdd = states_rdd.repartition(5)
DisplayRDD(states_rdd)

# %% [markdown]
# Let's do a transformation where we convert a string to a 2-tuple, where the second value is the length of the string. We will just use a `map` for this -- we have to provide a function as the input that transforms each element of the RDD. In this case, we are using the `lambda` keyword to define a function inline.
#
# The below lambda function is simply taking in a string: s, and returning a 2-tuple: (s, len(s))

# %%
states1 = states_rdd.map(lambda s: (s, len(s)))
DisplayRDD(states1)

# %% [markdown]
# Lets collect all the names with the same length together using a group by operation. 
# ```
# groupByKey([numTasks])
# ```
# When called on a dataset of (K, V) pairs, returns a dataset of (K, Iterable<V>) pairs. 
# This wouldn't work as is, because `states1` is using the name as the key. Let's change that around.

# %%
states2 = states1.map(lambda t: (t[1], t[0]))
DisplayRDD(states2)

# %% [markdown]
# Note above that Spark did not do a shuffle to ensure that the same `keys` end up on the same partition. In fact, the `map` operation does not do a shuffle. 
#
# Now we can do a groupByKey. 

# %%
states3 = states2.groupByKey()
DisplayRDD(states3)

# %% [markdown]
# That looks weird... it seems to have done a group by, but we are missing the groups themselves. This is because the type of the value is a `pyspark.resultiterable.ResultIterable` which our DisplayRDD code does not translate into strings. We can fix that by converting the `values` to lists, and then doing DisplayRDD.

# %%
DisplayRDD(states3.mapValues(list))

# %% [markdown]
# There it goes. Now we can see that the operation properly grouped together the state names by their lengths. This operation required a `shuffle` since originally all names with length, say 10, were all over the place.
#
# `groupByKey` does not reduce the size of the RDD. If we were interested in `counting` the number of states with a given length (i.e., a `group by count` query), we can use `reduceByKey` instead. However that requires us to do a map first.

# %%
states4 = states2.mapValues(lambda x: 1)
DisplayRDD(states4)

# %% [markdown]
# `reduceByKey` takes in a single reduce function as the input which tells us what to do with any two values. In this case, we are simply going to use sum them up.

# %%
DisplayRDD(states4.reduceByKey(lambda v1, v2: v1 + v2))

# %% [markdown]
# These operations could be done faster through using `aggregateByKey`, but the syntax takes some getting used to. `aggregateByKey` takes a `start` value, a function that tells it what to do for a given element in the RDD, and another reduce function. 

# %%
DisplayRDD(
    states2.aggregateByKey(0, lambda k, v: k + 1, lambda v1, v2: v1 + v2))

# %% [markdown]
# ### Basics 2: FlatMap
#
# Unlike a `map`, the function used for `flatMap` returns a list -- this is used to allow for the possibility that we will generate different numbers of outputs for different elements. Here is an example where we split each string in `states_rdd` into multiple substrings.
#
# The lambda function below splits a string into chunks of size 5: so 'South Dakota' gets split into 'South', ' Dako', 'ta', and so on. The lambda function itself returns a list. If you try this with 'map' the result would not be the same.

# %%
DisplayRDD(
    states_rdd.flatMap(
        lambda x: [str(x[i:i + 5]) for i in range(0, len(x), 5)]))

# %% [markdown]
# ### Basics 3: Joins
#
# Finally, lets look at an example of joins. We will still use small RDDs, but we now need two of them. We will just use `sc.parallelize` to create those RDDs. That functions takes in a list and creates an RDD of that by creating partitions and splitting them across machines. It takes the number of partitions as the second argument (optional).
#
# Note again that Spark made no attempt to co-locate the objects (i.e., the tuples) with the same key.

# %%
rdd1 = sc.parallelize([('alpha', 1), ('beta', 2), ('gamma', 3), ('alpha', 5), ('beta', 6)], 3)
DisplayRDD(rdd1)

# %%
rdd2 = sc.parallelize([('alpha', 'South Dakota'), ('beta', 'North Dakota'), ('zeta', 'Maryland'), ('beta', 'Washington')], 3)
DisplayRDD(rdd2)

# %% [markdown]
# Here is the definition of join from the programming guide.
# ```
# When called on datasets of type (K, V) and (K, W), returns a dataset of (K, (V, W)) pairs with all pairs of elements for each key. Outer joins are supported through leftOuterJoin, rightOuterJoin, and fullOuterJoin. 
# ```
# We want to join on the first attributes, so we can just call join directly, otherwise a map may have been required.

# %%
rdd3 = rdd1.join(rdd2)
DisplayRDD(rdd3)

# %% [markdown]
# There is a bunch of empty partitions. We could have controlled the number of partitions with an optional argument to join. But in any case, the output looks like what we were trying to do. Using `outerjoins` behaves as you would expect, with two extra tuples for fullOuterJoin.

# %%
DisplayRDD(rdd1.fullOuterJoin(rdd2))

# %% [markdown]
# `cogroup` is a related function, but basically creates two lists with each key. The `value` in that case is more complex, and our code above can't handle it. As we can see, there is a single object corresponding to each key, and the values are basically a pair of `iterables`.

# %%
DisplayRDD(rdd1.cogroup(rdd2).mapValues(lambda x: (list(x[0]), list(x[1]))))

# %% [markdown]
# ### Basics 4: Word count
#
# Here we will run some of the commands from the README file. This uses an RDD created from the lines of README.md file. You can use the DisplayRDD function here, but the output is rather large.

# %%
textFile = sc.textFile("README.md", 10)

# %%
textFile.count()

# %%
textFile.take(5)

# %% [markdown]
# As described in the README file, the following command does a word count, by first separating out the words using a `flatMap`, and then using a `reduceByKey`.

# %%
counts = textFile.flatMap(lambda line: line.split(" ")).map(lambda word: (word, 1)).reduceByKey(lambda a, b: a + b)
DisplayRDD(counts)

# %%
