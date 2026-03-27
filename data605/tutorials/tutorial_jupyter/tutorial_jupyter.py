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
# There are many excellent Python and Jupyter/IPython tutorials out there. This Notebook contains a few snippets of code from here and there, but we suggest you go over some in-depth tutorials, especially if you are not familiar with Python.
#
# Here we borrow some material from:
#
# - [A Crash Course in Python for Scientists](http://nbviewer.ipython.org/gist/rpmuller/5920182) (which itself contains some nice links to other tutorials),
# - [matplotlib examples](http://matplotlib.org/gallery.html#),
# - [Chapter 1 from Pandas Cookbook](http://nbviewer.ipython.org/github/jvns/pandas-cookbook/tree/master/cookbook/)
#
# This short introduction is itself written in Jupyter Notebook.
#
# As a starting point, you can simply type in expressions into the python shell in the browser.

# %%
2 + 2

# %% [markdown]
# Enter will continue the **cell**. If you want to execute the commands, you can either press the **play** button, or use Shift+Enter

# %%
days_of_the_week = [
    "Sunday",
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
]
for day in days_of_the_week:
    statement = "Today is " + day
    print(statement)

# %% [markdown]
# The above code uses a List. In case you haven't realized this yet, Python uses "indentation" to decide the scope, so there is no need to enclose code within {} or similar constructs.
#
# The other data structures in Python include Tuples and Dictionaries. Tuples are similar to Lists, but are immutable so we can't modify it (say by appending). Dictionaries are similar to Maps.

# %%
tuple1 = (1, 2, "hi", 9.0)
tuple1

# %%
# The following code will give an error since we are trying to change an immutable object
try:
    tuple1.append(7)
except Exception as e:
    print(e)

# %%
ages_dictionary = {"Rick": 46, "Bob": 86, "Fred": 21}
print("Rick's age is ", ages_dictionary["Rick"])


# %% [markdown]
# ### Functions


# %%
def fibonacci(sequence_length):
    "Return the Fibonacci sequence of length *sequence_length*"
    sequence = [0, 1]
    if sequence_length < 1:
        print("Fibonacci sequence only defined for length 1 or greater")
        return
    if 0 < sequence_length < 3:
        return sequence[:sequence_length]
    for i in range(2, sequence_length):
        sequence.append(sequence[i - 1] + sequence[i - 2])
    return sequence


# %%
help(fibonacci)

# %%
fibonacci(10)

# %% [markdown]
# The following function shows several interesting features, including the ability to return multiple values as a tuple, and the idea of "tuple assignment", where objects are unpacked into variables (the first line after for).

# %%
positions = [("Bob", 0.0, 21.0), ("Cat", 2.5, 13.1), ("Dog", 33.0, 1.2)]


def minmax(objects):
    minx = 1e20  # These are set to really big numbers
    miny = 1e20
    for obj in objects:
        name, x, y = obj
        if x < minx:
            minx = x
        if y < miny:
            miny = y
    return minx, miny


x, y = minmax(positions)
print(x, y)
