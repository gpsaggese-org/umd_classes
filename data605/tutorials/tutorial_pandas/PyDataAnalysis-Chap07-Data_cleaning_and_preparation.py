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

# %%
import pandas as pd

# import pandas_datareader.data as web
print(pd.__version__)

from numpy import nan as NA
import numpy as np


# %% [markdown]
# # Data cleaning and preparation
#
# - Significant amount of time (80%) is spent on data prep (loading, cleaning, transform, rearrange)

# %% [markdown]
# ## Handling missing data
#
# - Missing data occurs commonly
# - pandas tries to make working with missing data as painless as possible
#     - E.g., descr stats exclude missing data by default

# %%
data = pd.Series([1, NA, 3.5, NA, 7])

data

# %%
data.isnull()

# %%
data.notnull()

# %%
# Equivalent to: data[data.notnull()]
data.dropna()

# %% [markdown]
# ### Filling in missing data

# %% [markdown]
# #### pd.obj.fillna

# %%
# Create a random data frame with missing data.
df = pd.DataFrame(np.random.randn(7, 3))

df.iloc[:4, 1] = df.iloc[:2, 2] = NA

df

# %%
df.fillna(0)

# %%
df = pd.DataFrame(np.random.randn(6, 3))
df.iloc[2:, 1] = NA
df.iloc[4:, 2] = NA

df

# %%
# Fill nans using forward fill.
df.fillna(method="ffill")

# %%
# Use forward fill but with a limit.
df.fillna(method="ffill", limit=2)

# %% [markdown]
# ## Data transformation

# %% [markdown]
# ### Removing dups

# %% [markdown]
# #### pd.obj.duplicated()

# %%
data = pd.DataFrame(
    {"k1": ["one", "two"] * 3 + ["two"], "k2": [1, 1, 2, 3, 3, 4, 4]}
)

data

# %%
# Return if a row has been observed in a previous row or not.
data.duplicated()

# %% [markdown]
# #### pd.drop_duplicates()

# %%
# Remove the rows where `duplicated` is True.
data.drop_duplicates()

# %%
# By default the method considers all the columns.
# One can specify a subset of duplicates.

data.duplicated(["k1"])

# %%
data.duplicated(["k1"], keep="last")

# %%
print(data)

# By default drop_duplicates keeps the first obeserved value combination
print("\n", data.drop_duplicates(keep="first"))

# keep='last' return the last one
print("\n", data.drop_duplicates(keep="last"))

# %% [markdown]
# ### Transforming data using function or mapping

# %%
data = pd.DataFrame(
    {
        "food": [
            "bacon",
            "pulled pork",
            "bacon",
            "Pastrami",
            "corned beef",
            "Bacon",
            "pastrami",
            "honey ham",
            "nova lox",
        ],
        "ounces": [4, 3, 12, 6, 7.5, 8, 3, 5, 6],
    }
)
data

# %%
# Suppose you want to add a column indicating the animal each food came from.

meat_to_animal = {
    "bacon": "pig",
    "pulled pork": "pig",
    "pastrami": "cow",
    "corned beef": "cow",
    "honey ham": "pig",
    "nova lox": "salmon",
}

# %%
data["food"].str

# %%
# Get the lower case of one column.
# ".str" and ".dt" allow to select a column the algos for a given type.
lowercased = data["food"].str.lower()

print(lowercased)

data["animal"] = lowercased.map(meat_to_animal)

data

# %% [markdown]
# #### pd.obj.map()

# %%
# Using a single function.

# map() is called on each element of the obj.
# MEM: It's like python map()
data["food"].map(lambda x: meat_to_animal[x.lower()])

# %% [markdown]
# ### Replacing values
# - fillna is a special case of a more general replacement.

# %% [markdown]
# #### pd.obj.replace()

# %%
data = pd.Series([1.0, -999.0, 2.0, -999.0, -1000.0, 3.0])
data

# %%
# Replace -999 with nan.
data.replace(-999, np.nan)

# %%
# Replacing multiple values.
data.replace({-999: np.nan, -1000: 0})

# %%
# Also columns and index can be replaced using .replace()

# %% [markdown]
# ### Discretization and binning

# %% [markdown]
# #### pd.cut()

# %%
ages = [20, 22, 25, 27, 21, 23, 37, 31, 61, 45, 41, 32]

bins = [18, 25, 35, 60, 100]

# From "bins" create various categorical variables, then assign
# "ages" to the variables, returning a pd.Categorical array.
cats = pd.cut(ages, bins)

# pd.Categorical.
print(type(cats))
print("cats=\n", cats)

# %%
# Use int representation of the bins.
cats.codes

# %%
# Print the categorical values.
# They are upper close (a, b].
cats.categories

# %%
pd.value_counts(cats)

# %%
# Using lower close intervals.
cats = pd.cut(ages, bins, right=False)

cats

# %%
# Using custom labels for the categorical variables.
group_names = ["Youth", "YoungAdult", "MiddleAged", "Senior"]
cats = pd.cut(ages, bins, labels=group_names)

cats

# %%
# Using an integer number of bins will make compute equal-length bins
# between min and max values in the data.

# %%
# Uniform distributed numbers between 0 and 1.
np.random.seed(10)
data = np.random.rand(20)

print(data)

# %%
print(min(data), max(data))

# %%
pd.cut(data, bins=4, precision=2)

# %% [markdown]
# #### pd.qcut()

# %%
# qcut() uses sample quantiles instead of fixed intervals.

data = np.random.randn(1000)

# Use 4 equally space quantiles.
cats = pd.qcut(data, 4)

cats

# %%
# Since the distribution is Gaussian there should be exactly the same proportion
# of numbers in each category.
pd.value_counts(cats)

# %%
# Passing custom quantiles.
cats = pd.qcut(data, [0, 0.1, 0.5, 0.9, 1.0])
cats

# %%
pd.value_counts(cats)

# %% [markdown]
# ### Outliers

# %%
# Mean 0 and std 1.
data = pd.DataFrame(np.random.randn(1000, 4))
data.describe()

# %%
data.hist(bins=30)

# %%
# Find values in one of the columns exceeding 2.7 in abs value.
# Extract data in the pandas way.
col = data[2]
col[np.abs(col) > 2.7]

# %%
# Use pandas data inside numpy functions.
(np.abs(data) > 2.9).head()

# %%
# Find rows with at least one value larger than 2.9 in abs value.
data[(np.abs(data) > 2.9).any(axis=1)]

# %% [markdown]
# ### Permutation

# %% [markdown]
# ### Indicator / Dummy variables
#
# - Convert a categorical variable into a dummy (or indicator) variable
# - If a column has k distinct values, then k columns with one-hot encoding will be added

# %% [markdown]
# #### pd.get_dummies()

# %%
df = pd.DataFrame(
    {"key": ["b", "b", "a", "c", "a", "b"], "data1": list(range(6))}
)

df

# %%
pd.get_dummies(df["key"])

# %%
# One can add a prefix with "prefix".
pd.get_dummies(df["key"], prefix="key")

# %%
# One can combine pd.cut() to discretize with a pd.get_dummies() to compute indicator vars.

# Compute 10 random numbers.
np.random.seed(12345)
values = np.random.rand(10)

print("values=", values)

# Discretize with the given bins.
bins = [0, 0.2, 0.4, 0.6, 0.8, 1]
pd.get_dummies(pd.cut(values, bins))

# %% [markdown]
# ## String manipulation

# %% [markdown]
# ### String methods
#
# - split()
# - join()

# %%
string = "hello my name is guido"
"guido" in string

# %%
# Find the index of a substring.
print(string.index("guido"))

print(string.find("guido"))

# %%
# Raises "ValueError: substring not found"
# string.index('Guido')

string.find("Guido")

# %%
# Strip removes spaces on both sides.
" Guido    ".strip()

# %% [markdown]
# ### Regex

# %%
import re

text = "foo bar\t baz \tqux"
# Split using 1 or more spaces as separator.
re.split("\s+", text)

# %%
# If you want to call a regex several times, re.compile() speeds up things.
regex = re.compile("\s+")
regex.split(text)
regex.split(text)

# %%
# re.findall() finds all the matching substrings.
print(re.findall("\s", text))

# %%
# re.finditer() returns an iterator to the regex matches.
print(re.finditer("\s", text))
print(list(re.finditer("\s", text)))

# %%
# re.search() finds only the first.
m = re.search("\s", text)
m

# %%
print(m.start(), m.end())

# %%
# Extract the match.
text[m.start() : m.end()]

# %%
# re.match() finds only the first, starting from the beginning of the string.

# %%
# Email pattern match.
# - alphanumerical chars . _ % + -
# - alphanumerical interspersed with .
# - capture the groups
pattern = r"([A-Z0-9._%+-]+)@([A-Z0-9.-]+)\.([A-Z]{2,4})"

regex = re.compile(pattern, flags=re.IGNORECASE)
m = regex.match("saggese@gmail.com")

m.groups()

# %%
text = """Dave dave@google.com
    Steve steve@gmail.com
    Rob rob@gmail.com
    Ryan ryan@yahoo.com
    """

# One can look for the patterns multiple times in the string.
regex.findall(text)

# %% [markdown]
# ### Vectorized string functions in pandas

# %%
data = {
    "Dave": "dave@google.com",
    "Steve": "steve@gmail.com",
    "Rob": "rob@gmail.com",
    "Wes": np.nan,
}
data = pd.Series(data)

data

# %%
data.isnull()

# %%
# You can use map() and string manipulation. The problem is that nan create problems,
# so one needs to handle it.
data.map(lambda x: x.lower() if isinstance(x, str) else "")

# %%
data.str.contains("gmail")

# %%
# Lots of string function have a wrapper.
data.str.__dir__()
