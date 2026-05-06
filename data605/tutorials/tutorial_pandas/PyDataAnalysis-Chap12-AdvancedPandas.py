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
# <div class="toc"><ul class="toc-item"><li><span><a href="#Table-of-Contents" data-toc-modified-id="Table-of-Contents-1"><span class="toc-item-num">1&nbsp;&nbsp;</span>Table of Contents</a></span></li><li><span><a href="#Categorical-Data" data-toc-modified-id="Categorical-Data-2"><span class="toc-item-num">2&nbsp;&nbsp;</span>Categorical Data</a></span><ul class="toc-item"><li><span><a href="#Background" data-toc-modified-id="Background-2.1"><span class="toc-item-num">2.1&nbsp;&nbsp;</span>Background</a></span></li><li><span><a href="#Categorical-type-in-pandas" data-toc-modified-id="Categorical-type-in-pandas-2.2"><span class="toc-item-num">2.2&nbsp;&nbsp;</span>Categorical type in pandas</a></span></li><li><span><a href="#Computations-with-Categoricals" data-toc-modified-id="Computations-with-Categoricals-2.3"><span class="toc-item-num">2.3&nbsp;&nbsp;</span>Computations with Categoricals</a></span></li><li><span><a href="#Categorical-methods" data-toc-modified-id="Categorical-methods-2.4"><span class="toc-item-num">2.4&nbsp;&nbsp;</span>Categorical methods</a></span></li><li><span><a href="#Creating-dummy-variables-for-modeling" data-toc-modified-id="Creating-dummy-variables-for-modeling-2.5"><span class="toc-item-num">2.5&nbsp;&nbsp;</span>Creating dummy variables for modeling</a></span></li></ul></li><li><span><a href="#Advanced-GroupBy-use" data-toc-modified-id="Advanced-GroupBy-use-3"><span class="toc-item-num">3&nbsp;&nbsp;</span>Advanced GroupBy use</a></span><ul class="toc-item"><li><span><a href="#Transform" data-toc-modified-id="Transform-3.1"><span class="toc-item-num">3.1&nbsp;&nbsp;</span>Transform</a></span></li><li><span><a href="#Grouped-time-resampling" data-toc-modified-id="Grouped-time-resampling-3.2"><span class="toc-item-num">3.2&nbsp;&nbsp;</span>Grouped time resampling</a></span></li></ul></li><li><span><a href="#Techniques-for-method-chaining" data-toc-modified-id="Techniques-for-method-chaining-4"><span class="toc-item-num">4&nbsp;&nbsp;</span>Techniques for method chaining</a></span></li></ul></div>

# %%
import numpy as np
import pandas as pd

# %% [markdown]
# # Categorical Data

# %% [markdown]
# ## Background
#
# - A column in a table can contain repeated instances of a smaller set of distinct values
# - Categorical data used in df and series can lead to increase in performance and
# reduction in memory

# %%
values = pd.Series(["apple", "orange", "apple", "apple"] * 2)
values

# %%
pd.unique(values)

# %%
pd.value_counts(values)

# %%
# We can represent categorical data more efficiently with "dictionary-encoded"
# representations.

# categories = levels
values = pd.Series([0, 1, 0, 0] * 2)
dim = pd.Series(["apple", "orange"])
dim.take(values)

# %% [markdown]
# ## Categorical type in pandas

# %%
fruits = ["apple", "orange", "apple", "apple"] * 2

N = len(fruits)

# Note that the order of the columns relies on the dictionary being evaluated
# by sorted key.
df = pd.DataFrame(
    {
        "fruit": fruits,
        "basket_id": np.arange(N),
        "count": np.random.randint(3, 15, size=N),
        "weight": np.random.uniform(0, 4, size=N),
    },
    columns="basket_id fruit count weight".split(),
)

df

# %%
# The columns is an array of string objects.
df["fruit"]

# %%
fruit_col = df["fruit"]

print("fruit_col.values=", fruit_col.values)
print("type(fruit_col.values)=", type(fruit_col.values))
print("fruit_col.values[0]=", type(fruit_col.values[0]), fruit_col.values[0])

# %%
# Convert into a category.
fruit_cat = df["fruit"].astype("category")
fruit_cat

# %%
fruit_col = fruit_cat

print("fruit_col.values=", fruit_col.values)
print("type(fruit_col.values)=", type(fruit_col.values))
print("fruit_col.values[0]=", type(fruit_col.values[0]), fruit_col.values[0])

# %%
# Show the encoding.
c = fruit_cat.values

print(c.categories)
print(c.codes)

# %%
# Create categorical data from other sequences.

my_categories = pd.Categorical("foo bar baz foo bar".split())

my_categories

# %%
# Create categorical data from categories and codes.

categories = "foo bar baz".split()
codes = [0, 1, 2, 0, 0, 1]
my_cats_2 = pd.Categorical.from_codes(codes, categories)

my_cats_2

# %%
# We can indicate that categories have a meaningful ordering.

ordered_cat = pd.Categorical.from_codes(codes, categories, ordered=True)

ordered_cat

# %% [markdown]
# ## Computations with Categoricals

# %%
np.random.seed(12345)

draws = np.random.randn(1000)

draws[:5]

# %%
pd.Series(draws).hist()

# %%
# Split in 4 bins using quantiles.
bins = pd.qcut(draws, 4)
bins

# %%
x = pd.Series(sorted([x.mid for x in bins.get_values()])).unique()
x = pd.Series(x)
x.plot(marker="o")

# %%
# Assign labels to the quantiles.
bins = pd.qcut(draws, 4, labels="Q1 Q2 Q3 Q4".split())
bins

# %%
bins.codes[:10]

# %%
srs = pd.Series(bins, name="quartile")

srs.head()

# %%
# We can use the bins to groupby.
results = pd.Series(srs).groupby(bins).agg(["count", "min", max]).reset_index()

results

# %%
# The column retains categorical information.
results["index"]

# %% [markdown]
# ## Categorical methods

# %%
s = pd.Series("a b c d".split() * 2)

cat_s = s.astype("category")
cat_s

# %%
# Use .cat to access categorical methods.
cat_s.cat.codes

# %%
cat_s.cat.categories

# %%
# .set_categories() allows to increase the number of possible categories.
# .remove_unused_categories()

# %% [markdown]
# ## Creating dummy variables for modeling
#
# - Often in statistics or ML one transforms categorical data into dummy vars,
#   aka one-hot encoding

# %%
cat_s = pd.Series("a b c d".split() * 2, dtype="category")

cat_s

# %%
pd.get_dummies(cat_s)

# %% [markdown]
# # Advanced GroupBy use

# %% [markdown]
# ## Transform
#
# - apply() is applied to grouped operations
# - transform() is similar to apply() but imposes more constraints
#   1) it can produce a scalar value to be broadcasted to the shape of the group
#   2) it can produce an object of the same shape of the group
#   3) it must not mutate its input

# %%
df = pd.DataFrame({"key": "a b c".split() * 4, "value": np.arange(12.0)})

df

# %%
g = df.groupby("key").value

g.mean()

# %%
# If we want to produce a series with the same shape, but with values replaced
# by average grouped by 'key'.
# g.transform('mean')
g.transform(lambda x: x.mean())


# %%
def normalize(x):
    return (x - x.mean()) / x.std()


g.transform(normalize)

# %% [markdown]
# ## Grouped time resampling
#
# - resample() is a group operation based on time intrvalization

# %%
n = 15
times = pd.date_range("2017-05-20 00:00", freq="1min", periods=n)

df = pd.DataFrame({"time": times, "value": np.arange(n)})

df

# %%
df.set_index("time").resample("5min").count()

# %%
df2 = pd.DataFrame(
    {
        "time": times.repeat(3),
        "key": np.tile("a b c".split(), n),
        "value": np.arange(n * 3.0),
    }
)

df2[:7]

# %%
time_key = pd.TimeGrouper("5min")

resampled = df2.set_index("time").groupby(["key", time_key]).sum()

resampled

# %% [markdown]
# # Techniques for method chaining

# %%
