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
# <div class="toc"><ul class="toc-item"><li><span><a href="#Data-aggregation-and-group-operations" data-toc-modified-id="Data-aggregation-and-group-operations-1"><span class="toc-item-num">1&nbsp;&nbsp;</span>Data aggregation and group operations</a></span><ul class="toc-item"><li><span><a href="#GroupBy-mechanics" data-toc-modified-id="GroupBy-mechanics-1.1"><span class="toc-item-num">1.1&nbsp;&nbsp;</span>GroupBy mechanics</a></span><ul class="toc-item"><li><span><a href="#Iterating-over-groups" data-toc-modified-id="Iterating-over-groups-1.1.1"><span class="toc-item-num">1.1.1&nbsp;&nbsp;</span>Iterating over groups</a></span></li><li><span><a href="#Selecting-a-column-or-subset-of-columns" data-toc-modified-id="Selecting-a-column-or-subset-of-columns-1.1.2"><span class="toc-item-num">1.1.2&nbsp;&nbsp;</span>Selecting a column or subset of columns</a></span></li><li><span><a href="#Grouping-with-dicts-and-series" data-toc-modified-id="Grouping-with-dicts-and-series-1.1.3"><span class="toc-item-num">1.1.3&nbsp;&nbsp;</span>Grouping with dicts and series</a></span></li><li><span><a href="#Grouping-with-functions" data-toc-modified-id="Grouping-with-functions-1.1.4"><span class="toc-item-num">1.1.4&nbsp;&nbsp;</span>Grouping with functions</a></span></li><li><span><a href="#Grouping-by-index-level" data-toc-modified-id="Grouping-by-index-level-1.1.5"><span class="toc-item-num">1.1.5&nbsp;&nbsp;</span>Grouping by index level</a></span></li></ul></li><li><span><a href="#Data-aggregation" data-toc-modified-id="Data-aggregation-1.2"><span class="toc-item-num">1.2&nbsp;&nbsp;</span>Data aggregation</a></span><ul class="toc-item"><li><span><a href="#Column-wise-and-multiple-function-application" data-toc-modified-id="Column-wise-and-multiple-function-application-1.2.1"><span class="toc-item-num">1.2.1&nbsp;&nbsp;</span>Column-wise and multiple function application</a></span></li><li><span><a href="#Returning-aggregated-data-without-row-indexes" data-toc-modified-id="Returning-aggregated-data-without-row-indexes-1.2.2"><span class="toc-item-num">1.2.2&nbsp;&nbsp;</span>Returning aggregated data without row indexes</a></span></li></ul></li><li><span><a href="#Apply:-General-split-apply-combine" data-toc-modified-id="Apply:-General-split-apply-combine-1.3"><span class="toc-item-num">1.3&nbsp;&nbsp;</span>Apply: General split-apply-combine</a></span><ul class="toc-item"><li><span><a href="#Suppressing-the-group-keys" data-toc-modified-id="Suppressing-the-group-keys-1.3.1"><span class="toc-item-num">1.3.1&nbsp;&nbsp;</span>Suppressing the group keys</a></span></li><li><span><a href="#Quantile-and-bucket-analysis" data-toc-modified-id="Quantile-and-bucket-analysis-1.3.2"><span class="toc-item-num">1.3.2&nbsp;&nbsp;</span>Quantile and bucket analysis</a></span></li><li><span><a href="#Example:-filling-missing-values-with-group-specific-values" data-toc-modified-id="Example:-filling-missing-values-with-group-specific-values-1.3.3"><span class="toc-item-num">1.3.3&nbsp;&nbsp;</span>Example: filling missing values with group-specific values</a></span></li><li><span><a href="#Example:-random-sampling-and-permutation" data-toc-modified-id="Example:-random-sampling-and-permutation-1.3.4"><span class="toc-item-num">1.3.4&nbsp;&nbsp;</span>Example: random sampling and permutation</a></span></li><li><span><a href="#Example:-group-weighted-average-and-correlation" data-toc-modified-id="Example:-group-weighted-average-and-correlation-1.3.5"><span class="toc-item-num">1.3.5&nbsp;&nbsp;</span>Example: group weighted average and correlation</a></span></li><li><span><a href="#Example:-group-wise-linear-regression" data-toc-modified-id="Example:-group-wise-linear-regression-1.3.6"><span class="toc-item-num">1.3.6&nbsp;&nbsp;</span>Example: group-wise linear regression</a></span></li></ul></li><li><span><a href="#Pivot-tables-and-cross-tabulation" data-toc-modified-id="Pivot-tables-and-cross-tabulation-1.4"><span class="toc-item-num">1.4&nbsp;&nbsp;</span>Pivot tables and cross-tabulation</a></span><ul class="toc-item"><li><span><a href="#Crosstab" data-toc-modified-id="Crosstab-1.4.1"><span class="toc-item-num">1.4.1&nbsp;&nbsp;</span>Crosstab</a></span></li></ul></li></ul></li></ul></div>

# %%
import numpy as np
import pandas as pd

# %% [markdown]
# # Data aggregation and group operations
#
# - After loading, merging, cleaning a dataset
#     - compute group statistics
#
# - pandas (like SQL) has flexible operations for joining, filtering, aggregating data

# %% [markdown]
# ## GroupBy mechanics
#
# - Group operations are also called `split-apply-combine`
#
#     1. split data (from DataFrame or Series) into groups:
#         - based on certain keys
#         - along rows or columns
#     2. apply a function to each group producing a new value
#         - E.g., sum()
#     3. combine the results into a series / df object
#
# - Grouping can happen in many ways:
#     - list or array with values encoding the groups (same length as
#       the axis being grouped)
#     - a dict or a Series giving the correspondence between values
#       on the axes and group names
#     - the name of the column to be used for the split
#     - a function invoked on the index or on the rows / columns

# %%
np.random.seed(10)

df = pd.DataFrame({
    'key1': ['a', 'a', 'b', 'b', 'a'],
    'key2': ['one', 'two', 'one', 'two', 'one'],
    'data1': np.random.randn(5),
    'data2': np.random.randn(5)
})

df

# %%
# 1)
# - We want to compute the mean of the values in "data1" grouping by values of "key1"
# - groupby() computes the mapping between keys of the groups and rows of the dataframe
grouped = df['data1'].groupby(df['key1'])

# We are grouping a Series since we have a single column.
grouped

# %%
grouped2 = df[['data1', 'data2']].groupby(df['key1'])

# We are grouping a DataFrame since we have two columns.
grouped2

# %%
# For each value of the group we compute the mean of the corresponding rows.
grouped.mean()

# %%
# If we group by 2 keys, we end up with a hierarchical index Series.
means = df['data1'].groupby([df['key1'], df['key2']]).mean()

means

# %%
means.unstack()

# %%
df['data1']

# %%
# 2)
# We can also use arrays to infer the groups, as long as the size is
# the same as the number of rows.
states = np.array(['Ohio', 'California', 'California', 'Ohio', 'Ohio'])
years = np.array([2005, 2005, 2006, 2005, 2006])

print(len(states), len(years), len(df['data1']))

df['data1'].groupby([states, years]).mean()

# %%
# 3)
# The grouping information can be stored in the same data frame as the data
# Note that df['key2'] is excluded from the mean since it is not numerical.
df.groupby('key1').mean()

# %%
# Group by 2 keys the entire df.
df.groupby(['key1', 'key2']).mean()

# %%
# We can count the number of elements with size().
# Note that nan are excluded.
df.groupby(['key1', 'key2']).size()

# %% [markdown]
# ### Iterating over groups
#
# - groupby object supports iteration.

# %%
df

# %%
for name, group in df.groupby('key1'):
    # group is the dataframe.
    print("\n# key=", name)
    print("group=\n", group)

# %%
# In case of grouping by multiple keys, the "key" is a tuple of values.
for (k1, k2), group in df.groupby(['key1', 'key2']):
    print("\n# key=", (k1, k2))
    print("group=\n", group)

# %%
# One can compute a dict out of the groupby in one line.
pieces = dict(list(df.groupby('key1')))

import pprint

pprint.pprint(pieces)

# %% [markdown]
# ### Selecting a column or subset of columns

# %%
df

# %%
# Group by "key1".
grouped = df.groupby('key1')

# .groups.keys() to get the keys.
print("keys=", list(grouped.groups.keys()))

# A groupby object can be split by column after being computed.
print(df.groupby('key1')["data1"])

# %%
print(df.groupby('key1')["data1"].mean())
print(df.groupby('key1')["data2"].mean())

# %%
# It is equivalent to
# - "split and then select" and
# - "select and then split"
print(df.groupby('key1')["data1"].mean())

# Once we have selected "data1" there is no "key1" anymore so we use the array
# df["key1"] to label the values and group.
print(df["data1"].groupby(df['key1']).mean())

# %% [markdown]
# ### Grouping with dicts and series

# %%
np.random.seed(10)

people = pd.DataFrame(
    np.random.randn(5, 5),
    columns=list("abcde"),
    index="Joe Steve Wes Jim Travis".split())

# Add NAs at row = 2 and columns = [1, 3]
people.iloc[2:3, [1, 3]] = np.nan

people

# %% [markdown]
# Finish

# %%
# Build a map from columns to group and aggregate.
mapping = {
    'a': 'red',
    'b': 'red',
    'c': 'blue',
    'd': 'blue',
    'e': 'red',
    'f': 'orange'
}

by_column = people.groupby(mapping, axis=1)

by_column.sum()

# %%
# Transform the dict into a fixed mapping series.
map_series = pd.Series(mapping)

print(map_series)

display(people.groupby(map_series, axis=1).sum())

# %% [markdown]
# ### Grouping with functions
#
# - Instead of a fixed mapping through dict or Series, a function can be used
# - When passing a function to groupby(), the function is called on the
#   index and the result is the group

# %%
# Group by length of name
people.groupby(len).sum()

# %% [markdown]
# ### Grouping by index level
#
# - One can use the hierarchical index to aggregate using one of the
#   levels
#

# %%
columns = pd.MultiIndex.from_arrays(
    [['US', 'US', 'US', 'JP', 'JP'], [1, 3, 5, 1, 3]],
    names=['cty', 'tenor'])

columns

# %%
hier_df = pd.DataFrame(np.random.randn(4, 5), columns=columns)

hier_df

# %%
hier_df.groupby(level='cty', axis=1).count()

# %% [markdown]
# ## Data aggregation
#
# - aggregation = transformation from arrays to scalar value
#     - E.g., mean, count, min, sum, first, last

# %%
df

# %%
# split by values of key1 and compute quantile.
df.groupby('key1').quantile(0.9)


# %%
# One can use any custom function.
def peak_to_peak(arr):
    return arr.max() - arr.min()

df.groupby('key1').agg(peak_to_peak)

# %%
# Also functions like describe() work, although they are not
# aggregations.

df.groupby('key1')["data1"].describe()

# %%
df.groupby('key1').describe()

# %% [markdown]
# ### Column-wise and multiple function application

# %%
tips = pd.read_csv('~/src/github/pydata-book/examples/tips.csv')

tips['tip_pct'] = tips['tip'] / tips['total_bill']

tips.head()

# %%
grouped = tips.groupby(['day', 'smoker'])

# Select a column.
grouped_pct = grouped['tip_pct']
print("keys=", list(grouped_pct.groups.keys()))

# Equivalent.
grouped_pct.agg('mean')
grouped_pct.mean()

# %%
# Pass a list of aggregation functions.
funcs = ['mean', 'std', peak_to_peak]
grouped_pct.agg(funcs)

# %%
# Assign name to the functions.
funcs = [
    ('foo', 'mean'),
    ('bar', np.std)
]
grouped_pct.agg(funcs)

# %%
funcs = ['count', 'mean', 'max']
result = grouped['tip_pct', 'total_bill'].agg(funcs)

# It has hierarchical columns for both rows and columns.
result

# %%
# Aggregation functions can also be specified by dict.
funcs = {'tip': np.max, 'size': 'sum'}
grouped.agg(funcs)

# %%
funcs = {'tip_pct': ['min', 'max', 'mean', 'std'], 'size': 'sum'}
grouped.agg(funcs)

# %% [markdown]
# ### Returning aggregated data without row indexes

# %%
tips.groupby(['day', 'smoker'], as_index=True).mean()

# %%
# Returning a hierarchical index can be disabled.
tips.groupby(['day', 'smoker'], as_index=False).mean()

# %%
# This is equivalent to call reset_index().

tips.groupby(['day', 'smoker'], as_index=True).mean().reset_index()


# %% [markdown]
# ## Apply: General split-apply-combine

# %%
# You want to select the top five tip_pct values by group.

def top(df, n=2, column='tip_pct'):
    return df.sort_values(by=column)[-n:]

top(tips, n=6)

# %%
# top() is called on each row group and then results
# are concat with pandas.concat, using labels from group name.
tips.groupby('smoker').apply(top)

# %%
# You can pass params to the function using **kwargs.
tips.groupby('smoker').apply(top, n=1, column='total_bill')

# %%
# This operation is what describe() does.
display(tips.groupby('smoker')["tip_pct"].describe())

df2 = tips.groupby('smoker')["tip_pct"].apply(lambda x: x.describe())
display(df2)


# %% [markdown]
# ### Suppressing the group keys

# %%
# Disable the hierarchial indexing.

df = tips.groupby('smoker', group_keys=True).apply(top)
display(df)

df = tips.groupby('smoker', group_keys=False).apply(top)
display(df)

# %% [markdown]
# ### Quantile and bucket analysis

# %%
df = pd.DataFrame({
    "data1": np.random.randn(100),
    "data2": np.random.randn(100)
})

display(df.head())

# %%
quartiles = pd.cut(df.data1, 4)

print(type(quartiles))

quartiles[:4]

# %%
# We can use the series above to groupby.

# We can filter by data2 since we already know the mapping.
grouped = df["data2"].groupby(quartiles)

for k, v in grouped:
    print(k)
    print(v.head(2))


# %%
def get_stats(group):
    #print group
    #assert 0
    return pd.Series({
        'min': group.min(),
        'max': group.max(),
        'count': group.count(),
        'mean': group.mean()
    })

df2 = grouped.apply(get_stats)

display(df2)

# Move one level of index to columns.
df2.unstack()

# %%
pd.qcut(df.data1, 4).head()

# %%
pd.cut(df.data1, 4).head()

# %% [markdown]
# ### Example: filling missing values with group-specific values

# %%
s = pd.Series(np.random.randn(6))
s[::2] = np.nan

s

# %%
s.fillna(s.mean())

# %%
# One can fill nans based on the group.

states = [
    'Ohio', 'New York', 'Vermont', 'Florida', 'Oregon', 'Nevada', 'California',
    'Idaho'
]
group_key = ['East'] * 4 + ['West'] * 4
data = pd.Series(np.random.randn(8), index=states)

data

# %%
data[['Vermont', "Nevada", "Idaho"]] = np.nan

data

# %%
data.groupby(group_key).mean()

# %%
fill_mean = lambda g: g.fillna(g.mean())

data.groupby(group_key).apply(fill_mean)

# %% [markdown]
# ### Example: random sampling and permutation

# %%
# Hearts
# Spades
# Clubs
# Diamonds
suits = list("HSCD")
# Values.
card_val = list(list(range(1, 10 + 1)) + [10] * 3)
base_names = ['A'] + list(range(2, 10 + 1)) + list("JQK")
assert len(card_val) == len(base_names)

cards = []
for suit in suits:
    cards.extend(str(num) + suit for num in base_names)

deck = pd.Series(card_val * 4, index=cards)
assert len(deck) == 52
deck.head()


# %%
# Draw two cards without replacement.

def draw(deck, n=5):
    return deck.sample(n)


draw(deck)

# %%
# Last letter is suit.
get_suit = lambda card: card[-1]

# %%
# Draw 2 cards per suit.
# Group by suit, and then get 2 cards from each group.
deck.groupby(get_suit, group_keys=False).apply(draw, n=2)

# %% [markdown]
# ### Example: group weighted average and correlation

# %%
df = pd.DataFrame({
    'category': ['a', 'a', 'a', 'a', 'b', 'b', 'b', 'b'],
    'data': np.random.randn(8),
    'weights': np.random.rand(8)
})

df

# %%
grouped = df.groupby('category')

# Aggregation function: dot product between data and weights.
get_wavg = lambda g: np.average(g['data'], weights=g['weights'])

grouped.apply(get_wavg)

# %%
close_px = pd.read_csv(
    '~/src/github/pydata-book/examples/stock_px_2.csv',
    parse_dates=True,
    index_col=0)

close_px.head()

# %%
close_px.info()

# %%
close_px.describe()

# %%
# Compute rets.

rets = close_px.pct_change().dropna()

rets.head()

# %%
# For each stock compute the correlation with SPX.
spx_corr = lambda x: x.corrwith(x['SPX'])

# Groupby year.
get_year = lambda x: x.year

# For each year, compute the correlation of each stock to SPX.
by_year = rets.groupby(get_year)
by_year.apply(spx_corr)

# %%
# For each year, compute the correlation of AAPL and MSFT.
by_year.apply(lambda x: x['AAPL'].corr(x['MSFT']))

# %% [markdown]
# ### Example: group-wise linear regression
#
# - You can use groupby to perform more complex analysis, as long
#   as function returns a pandas object (Series or DataFrame) or
#   scalar value

# %%
import statsmodels.api as sm

def regress(data, yvar, xvars):
    Y = data[yvar]
    X = data[xvars]
    X['intercept'] = 1.0
    result = sm.OLS(Y, X).fit()
    return result.params

by_year.apply(regress, 'AAPL', ['SPX'])

# %% [markdown]
# ## Pivot tables and cross-tabulation
#
# - A pivot table aggregates a table of data by one or more keys
#   arranging results for rows and columns

# %%
tips.head()

# %%
# Aggregate through mean by two indices.
tips.pivot_table(index=['day', 'smoker'])

# %%
# #?tips.pivot_table

# %%
# Compute two metrics by
# - 3 vars: 2 on the index and 1 on the columns
tips.pivot_table(['tip_pct', 'size'],
                 index=['time', 'day'],
                 columns='smoker')

# %%
# We can also add summation over each var, so that
# there are values for 2 variables.
tips.pivot_table(['tip_pct', 'size'],
                 index=['time', 'day'],
                 columns='smoker',
                 margins=True)

# %%
# You can specify the aggregation function by passing aggfunc.
tips.pivot_table('tip_pct',
                 index=['time', 'smoker'],
                 columns='day',
                 aggfunc=len, margins=True)

# %% [markdown]
# ### Crosstab
#
# - Special case of pivot table that computes group frequencies

# %%
pd.crosstab([tips.time, tips.day], tips.smoker, margins=True)q
