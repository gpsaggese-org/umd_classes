# ---
# jupyter:
#   jupytext:
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
try:
    import xarray
except ModuleNotFoundError:
    # !sudo /bin/bash -c "(source /venv/bin/activate; pip install --quiet xarray)"
    pass

# %%
#
import numpy as np

print("numpy version=", np.__version__)

#
import xarray as xr

print("xarray version=", xr.__version__)

# %%
# from IPython.display import HTML, display

# display(HTML("<style>.container { width:77% !important; }</style>"))

# %% [markdown]
# # Overview: why xarray?
#
# From https://docs.xarray.dev/en/stable/getting-started-guide/why-xarray.html

# %% [markdown]
# - `numpy` N-dim arrays (aka tensors) are used in many parts of computational science
#
# - `numpy` provides raw N-dimensional arrays
# - Real-world datasets need labels to encode information about how array values map to actual data
# - `xarray` adds labels (e.g., dimensions, coordinates, attributes) to `numpy` N-dim arrays
#
# - `xarray`:
#     - applies operations over dimensions by name
#     - uses dimension names (e.g., `dim='time'` vs `axis=0`)
#     - selects values by label (instead of integer location)
#     - vectorizes operations based on dimension names and not shape
#     - implements split-apply-combine paradigm

# %% [markdown]
# ## Core data structures
# - `DataArray` is labeled N-dimensional array
#     - generalizes `pd.Series` to N dimensions
#     - attaches labels to `np.ndarray`
#
# - `Dataset` is dict-like container of `DataArray`
#     - arrays in `Dataset` can have different number of dimensions
#
# - `xarray` integrates with the Pydata ecosystem (`numpy`, `pandas`, `Dask`, `matplotlib`)
#     - It's easy to get data in and out

# %% [markdown]
# # Quick overview
#
# https://docs.xarray.dev/en/stable/getting-started-guide/quick-overview.html

# %% [markdown]
# ## Create a DataArray

# %%
np.random.seed(314)

# Create a 2D array.
data = np.array([[1, 2, 3], [4, 5, 6]])
print("data=", data)

# Create an xarray.
data = xr.DataArray(
    data,
    # - Assign x and y to the dimensions.
    dims=("x", "y"),
    # - Assign coordinate labels 10 and 20 to locations along x dimension.
    coords={"x": [10, 20]},
)

# %%
# Show as HTML.
data

# %% [markdown]
# - `data` has 2 dimensions `x`, `y`, with 2 and 3 elements, respectively
# - The `x` dimension has coordinates/names
#     - `x` has an Pandas index using ints
# - The `y` domension has no coordinates
# - `data` has no attributes

# %%
print(type(data))

# %%
# Print as string.
print(data)

# %%
# Extract the numpy data structure.
vals = data.values
print("type(vals)=", type(vals))
print("vals=\n", vals)

# %%
# Extract the dimension names which are a tuple.
print(data.dims)

# %%
# Extract the coordinates.
print("# type(data.coords)=\n%s" % type(data.coords))
print("# data.coords=\n%s" % data.coords)

# %%
# Extract the attributes, which can store arbitrary metadata.
data.attrs

# %% [markdown]
# ### Indexing
#
# - Slicing an xarray returns another xarray with the slice

# %%
data

# %%
# Slice like NumPy-style.
# Set the x dimension to be 0, so get the first row.
data[0, :]

# %%
# Set the x dimension to be 1 (like numpy), so get the second row.
data[1, :]

# %%
# loc, "location": select by coordinate label (like pandas)
# Get data along the first dimension for the index called `10`.
data.loc[10]

# %%
# isel, "integer select": select by dimension name and integer label
# Get data along the dimension `x` for the first index
data.isel(x=0)

# %%
# isel, "integer select": select by dimension name and integer label
# Get data along the dimension `y` for the second index
data.isel(y=1)

# %%
# sel, "select", by dimension name and coordinate label
# Get data along the dimension `x` and the index `10`
data.sel(x=10)

# %% [markdown]
# ### Attributes
#
# - You can add metadata attributes to `DataArray` or to coordinates
# - Some of them are used automatically in the plots

# %%
data.attrs["long_name"] = "random_velocity"
data.attrs["units"] = "m/s"
data.attrs["description"] = "A random var created as an example"

print(data.attrs)

# %%
data

# %%
data.x.attrs["units"] = "x units"

# %%
data

# %% [markdown]
# ### Computation
#
# - Data arrays work very similarly to numpy ndarrays

# %%
# Sum 10 element-wise.
data + 10

# %%
# Sum elements across all the dimensions
data.sum()

# %%
# Compute mean along one dimension by label.
data.mean(dim="x")

# %%
# Transpose.
data.T

# %% [markdown]
# - Arithmetic operations broadcast based on dimension name
# - You don't need to insert dummy dimensions for alignment

# %%
# Create a 1-vector with coordinates along the `y` axis.
a = xr.DataArray([1, 2, 3], {"y": [0, 1, 2]})

# Create a 1-vector with dimension `z` and no coordinates.
b = xr.DataArray([10, 20, 30, 40], dims="z")

# %%
display(a)
display(b)

# %%
# The broadcast happens along the dimensions by name, without worrying about the order.
a + b

# %% [markdown]
# The dimensions don't have the same name.

# %%
# Create a 1-vector with coordinates along `z`.
a = xr.DataArray([1, 2, 3], {"z": [0, 1, 2]})
# Create a 1-vector with `z` dimension.
b = xr.DataArray([10, 20, 30], dims="z")

a + b

# %% [markdown]
# ### Plotting

# %%
# The plot uses the attributes.
data.plot();

# %% [markdown]
# ### Pandas interaction

# %%
# From xarray to multi-index pd.Series.
srs = data.to_series()
srs

# %%
# From pd.Series to xarray.
srs.to_xarray()

# %%
df = data.to_dataframe(name="hello")
df

# %% [markdown]
# ## Datasets
#
# - `xarray.Dataset` is a dict-like container of aligned `xarray.DataArray`
#     - It is like a generalization of a `pd.DataFrame`
# - Variables in a `Dataset` can have different dimensions and dtypes
# - If two variables have the same dimension (e.g., `x`) the dimension must be identical in both variables

# %% [markdown]
# ### Build from dictionary

# %%
# Create a dictionary with heterogeneous data.
dict_ = dict(foo=data, bar=("x", [1, 2]), baz=np.pi)
print(dict_)

# %%
# Create a `xarray.Dataset` from the dictionary.
# - `foo` is a DataArray (with 2 dimensions `x` and `y`)
# - `bar` is a one-dimensional array with dimension `x`
# - `baz` is a scalar (with no dimensions)
ds = xr.Dataset(dict_)
ds

# %% [markdown]
# ### Extract one variable

# %%
# Extract one variable from the dataset.
ds["foo"]
# This is equivalent to
# ds.foo
assert str(ds.foo) == str(ds["foo"])

# %%
ds["bar"]

# %%
ds["baz"]

# %% [markdown]
# ### Extract multiple vars

# %%
ds[["foo", "bar"]].to_dataframe().values

# %% [markdown]
# ### Slicing

# %%
# Both `foo` and `bar` variables have the same coordinate `x`, so we can use `x` to slice the data.
ds["x"]
# ds.bar["x"]
# ds.foo["x"]

# %% [markdown]
# ### Computation
#
# Most of the computations for `DataArray` are possible also on `Dataset`

# %% [markdown]
# # FAQ
#
# https://docs.xarray.dev/en/stable/getting-started-guide/faq.html

# %% [markdown]
# - `xarray` API is inspired by Pandas
# - Pandas dataframe is focused on low-dimensional tabular data, where there is a rows-and-columns structure
#     - Pandas N-dimensional panels were deprecated in favor of `xarray.DataArray`
# - `xarray` allows ndim > 2 dimensional array for which the order of dimensions doesn't really matter
#     - E.g., a movie is represented as a 4-dim array with time, row, column, color

# %% [markdown]
# # User Guide
#
# https://docs.xarray.dev/en/stable/user-guide/index.html

# %% [markdown]
# ## Terminology
#
# https://docs.xarray.dev/en/stable/user-guide/terminology.html

# %% [markdown]
# - `DataArray`
#     - A multidimensional array with labeled dimensions
#     - It contains metadata, such as dimension, names, coordinates, and attributes to the data
#
# - `Dataset`
#     - A dict-like collection of `DataArray` objects with aligned dimensions
#
# - Dimension
#     - The dimension of data is related to the number of degrees of freedom of it
#
# - Dimension axis
#     - Set of all points in which all but one of the degrees of freedom is fixed
#     - Each dimension axis has a name (e.g., "x dimension")
#     - The dimensions are stored in `da.dims`
#
# - Coordinate
#     - An array that labels a dimension (like tick labels along a dimension)
#     - A dimension can have a coordinate or not
#     - A dimension can have an index (to use selection and alignment) or not
