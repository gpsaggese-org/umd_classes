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

# %% [markdown] toc="true"
# <h1>Table of Contents<span class="tocSkip"></span></h1>
# <div class="toc"><ul class="toc-item"><li><span><a href="#numpy-ndarray" data-toc-modified-id="numpy-ndarray-1"><span class="toc-item-num">1&nbsp;&nbsp;</span>numpy ndarray</a></span><ul class="toc-item"><li><span><a href="#Creating-arrays" data-toc-modified-id="Creating-arrays-1.1"><span class="toc-item-num">1.1&nbsp;&nbsp;</span>Creating arrays</a></span></li><li><span><a href="#Data-types" data-toc-modified-id="Data-types-1.2"><span class="toc-item-num">1.2&nbsp;&nbsp;</span>Data types</a></span></li><li><span><a href="#Operations-between-Arrays-and-Scalar" data-toc-modified-id="Operations-between-Arrays-and-Scalar-1.3"><span class="toc-item-num">1.3&nbsp;&nbsp;</span>Operations between Arrays and Scalar</a></span></li><li><span><a href="#Basic-index-and-slicing" data-toc-modified-id="Basic-index-and-slicing-1.4"><span class="toc-item-num">1.4&nbsp;&nbsp;</span>Basic index and slicing</a></span><ul class="toc-item"><li><span><a href="#Indexing-with-slices." data-toc-modified-id="Indexing-with-slices.-1.4.1"><span class="toc-item-num">1.4.1&nbsp;&nbsp;</span>Indexing with slices.</a></span></li></ul></li><li><span><a href="#Boolean-indexing" data-toc-modified-id="Boolean-indexing-1.5"><span class="toc-item-num">1.5&nbsp;&nbsp;</span>Boolean indexing</a></span></li><li><span><a href="#Fancy-indexing" data-toc-modified-id="Fancy-indexing-1.6"><span class="toc-item-num">1.6&nbsp;&nbsp;</span>Fancy indexing</a></span></li><li><span><a href="#Transposing-arrays-and-swapping-axes." data-toc-modified-id="Transposing-arrays-and-swapping-axes.-1.7"><span class="toc-item-num">1.7&nbsp;&nbsp;</span>Transposing arrays and swapping axes.</a></span></li><li><span><a href="#Universal-functions" data-toc-modified-id="Universal-functions-1.8"><span class="toc-item-num">1.8&nbsp;&nbsp;</span>Universal functions</a></span></li></ul></li><li><span><a href="#Data-processing-using-arrays" data-toc-modified-id="Data-processing-using-arrays-2"><span class="toc-item-num">2&nbsp;&nbsp;</span>Data processing using arrays</a></span><ul class="toc-item"><li><span><a href="#Expressing-conditional-logic-as-array-operations." data-toc-modified-id="Expressing-conditional-logic-as-array-operations.-2.1"><span class="toc-item-num">2.1&nbsp;&nbsp;</span>Expressing conditional logic as array operations.</a></span></li><li><span><a href="#Mathematical-and-statistical-methods" data-toc-modified-id="Mathematical-and-statistical-methods-2.2"><span class="toc-item-num">2.2&nbsp;&nbsp;</span>Mathematical and statistical methods</a></span></li><li><span><a href="#Unique-and-set-logic" data-toc-modified-id="Unique-and-set-logic-2.3"><span class="toc-item-num">2.3&nbsp;&nbsp;</span>Unique and set logic</a></span></li></ul></li><li><span><a href="#File-input-and-output" data-toc-modified-id="File-input-and-output-3"><span class="toc-item-num">3&nbsp;&nbsp;</span>File input and output</a></span><ul class="toc-item"><li><span><a href="#Storing-arrays-on-disk-in-binary-form." data-toc-modified-id="Storing-arrays-on-disk-in-binary-form.-3.1"><span class="toc-item-num">3.1&nbsp;&nbsp;</span>Storing arrays on disk in binary form.</a></span></li></ul></li><li><span><a href="#Linear-algebra" data-toc-modified-id="Linear-algebra-4"><span class="toc-item-num">4&nbsp;&nbsp;</span>Linear algebra</a></span></li><li><span><a href="#Random-number-generator" data-toc-modified-id="Random-number-generator-5"><span class="toc-item-num">5&nbsp;&nbsp;</span><strong>Random number generator</strong></a></span><ul class="toc-item"><li><span><a href="#Random-walks" data-toc-modified-id="Random-walks-5.1"><span class="toc-item-num">5.1&nbsp;&nbsp;</span><strong>Random walks</strong></a></span></li></ul></li></ul></div>

# %% [markdown]
# - numpy (numerical python)
#
# - high performance scientific computing and data analysis
# - `ndarray` = fast space-efficient multidim array with
#     - vectorized arithmetic operations (no loops)
#     - sophisticated broadcasting capabilities
# - sorting, unique, set operation
# - data alignment
# - reading / writing arrays to disk and memory-mapped files
# - linear algebra
# - random number generation
# - FFT, ...
# - tools for integrating code with C, C++, Fortran
#     - easy C API to call external libraries

# %%
import numpy as np

# %% [markdown]
# # numpy ndarray
#
# - ndarray = N-Dim array object

# %% [markdown]
# ## Creating arrays

# %%
# From sequence-like object to ndarray.
data1 = [6, 7.5, 8, 0, 1]

arr1 = np.array(data1)

print("arr1=", arr1)
# It's like a vector not a matrix.
print("arr1.shape=", arr1.shape)
print("arr1.dtype=", arr1.dtype)

# %%
data2 = [[1, 2, 3, 4], [5, 6, 7, 8]]
arr2 = np.array(data2)

print("arr2=\n", arr2)
print("arr2.shape=", arr2.shape)
# np.array() tries to infer the right type, if not done explicitly.
print("arr2.dtype=", arr2.dtype)

# %%
np.zeros(10)

# %%
np.zeros((3, 6))

# %%
np.zeros_like(arr2)

# %%
# Returns unitialized garbage values.
np.empty((2, 3, 2))

# %%
np.arange(15)

# %%
np.eye(5)

# %% [markdown]
# ## Data types
#
# - map directly onto machine representation
#     - `int*, uint*`
#     - `float*`
#     - `complex*`
#     - `bool`
#     - `object` (python object)
#     - `string*` (fixed length string)
#     - `unicode*` (fixed length unicode, num of bytes depending on machine)
# - easy to read / write to disk
# - easy to interface with low-level code in C and Fortran
#

# %%
arr1 = np.array([1, 2, 3], dtype=np.float64)
print(arr1)

# %%
arr2 = np.array([-1, 2, 3], dtype=np.int32)
print(arr2)

# %%
arr2 = np.array([-1, 2, 3], dtype=np.uint32)
print(arr2)

# %%
# Cast an array from one type to another.
# It always create a new array even if dtype is not changed.
arr = np.array([1, 2, 3, 4, 5])
print(arr)
print(arr.dtype)

float_arr = arr.astype(np.float64)
print(float_arr)
print(float_arr.dtype)

# %%
str_arr = np.array(["1.25", "-9.6", "42"], dtype=np.string_)
print(str_arr)
print(str_arr.dtype)

print(str_arr.astype(float))

# %% [markdown]
# ## Operations between Arrays and Scalar
#
# - One can express operations on data without for loops

# %%
arr = np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])

print(arr + arr)
# Broadcast.
print(1 / arr)
print(arr * arr)
print(arr**0.5)

# %% [markdown]
# ## Basic index and slicing

# %%
arr = np.arange(10)

print(arr)

print(arr[5])
print(arr[5:8])

# %%
# Broadcasting write.
arr[5:8] = 12
print(arr)

# %%
# Slices are "views" on the original array. No data is copied.

arr_slice = arr[5:8]
print(arr_slice)

arr_slice[1] = 12345
print(arr_slice)

arr_slice[:] = 64
print(arr_slice)

print(arr)

# %%
arr2d = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
print(arr2d)

# %%
print(arr2d[2])

# %%
print(arr2d[2][0])

# %%
arr3d = np.array([[[1, 2, 3], [4, 5, 6]], [[7, 8, 9], [10, 11, 12]]])
print(arr3d)
print(arr3d.shape)

# %%
# Fixing the first index, returns a 2x3 array.
print(arr3d[0])

# %%
arr3d[0] = 42

print(arr3d)

# %%
# Return all the values whose indices start with (1, 0), i.e.,
# a 1-d array.
print(arr3d[1][0])
print(arr3d[1, 0])

# %% [markdown]
# ### Indexing with slices.

# %%
arr2d

# %%
# Slice first index, i.e., columns.
print(arr2d[:2])
print(arr2d[:2].shape)

# %%
arr2d[:2, 1:]

# %%
arr2d[1, :2]

# %%
arr2d[2, :1]

# %%
# A colon : means "the entire axis"
arr2d[:, :1]

# %% [markdown]
# ## Boolean indexing

# %%
names = np.array(["Bob", "Joe", "Will", "Bob", "Will", "Joe", "Joe"])

print(str(names))
print(repr(names))

# %%
np.random.seed(42)
# Normal data.
data = np.random.randn(7, 4)
print(data)

# %%
print(names)
names == "Bob"

# %%
data[names == "Bob"]

# %%
data[names == "Bob", 2:]

# %%
names != "Bob"

# %%
print(~(names == "Bob"))
data[~(names == "Bob")]

# %%
data

# %%
data[data < 0] = 0
data

# %% [markdown]
# ## Fancy indexing
#
# - One can index using integer arrays

# %%
arr = np.empty((8, 4))

# %%
for i in range(8):
    arr[i] = i

print(arr)

# %%
# Select rows using certain indices.
arr[[4, 3, 0, 6]]

# %%
# Negative indices work as expected.
arr[[-3, -5, -7]]

# %%
arr = np.arange(32).reshape((8, 4))

print(str(arr))

# %%
# WARNING: It doesn't select 4 rows and 4 columns.
# It gets elements (1, 0), (5, 3), (7, 1), (2, 2).
arr[[1, 5, 7, 2], [0, 3, 1, 2]]

# %%
# To select 4 rows and 4 columns.
arr[[1, 5, 7, 2]][:, [0, 3, 1, 2]]

# %%
help(np.ix_)

# %%
# np.ix_() converts indices.
idxs = np.ix_([1, 5, 7, 2], [0, 3, 1, 2])
print(idxs)

print(arr[idxs])

# %% [markdown]
# ## Transposing arrays and swapping axes.

# %%
arr = np.arange(15).reshape((3, 5))
print(arr)

# %%
print(arr.T)

# %%
np.dot(arr.T, arr)

# %%
arr = np.arange(16).reshape((2, 2, 4))
print(arr)

# %% [markdown]
# ## Universal functions
#
# - ufunc performs elementwise operations on data in ndarrays

# %%
arr = np.arange(10)

print(np.sqrt(arr))
print(np.exp(arr))

# %%
np.random.seed(42)
x = np.random.randn(8)
y = np.random.randn(8)

print(x)
print(y)

print(np.maximum(x, y))

# %%
np.add(x, y)

# %%
np.greater(x, y)

# %%
np.not_equal(x, y)

# %%
np.logical_xor(np.not_equal(x, y), np.greater(x, y))

# %% [markdown]
# # Data processing using arrays

# %%
# Evaluate

# - Pick 1000 equi-spaced points between [-5, 5].
points = np.arange(-5, 5, 0.01)
print("points=", points[:5])

# - Create a grid of points.
xs, ys = np.meshgrid(points, points)
print("xs=\n", xs)
print("ys=\n", ys)

# - Evaluate function on a grid.
z = np.sqrt(xs**2 + ys**2)

# %%
import matplotlib.pyplot as plt

plt.imshow(z, cmap=plt.cm.gray)
plt.colorbar()
plt.title("hello")

# %% [markdown]
# ## Expressing conditional logic as array operations.
#
# - `numpy.where` is vectorized form of `if-then-else`

# %%
xarr = np.array([1.1, 1.2, 1.3, 1.4, 1.5])
yarr = np.array([2.1, 2.2, 2.3, 2.4, 2.5])
cond = np.array([True, False, True, True, False])

result = [(x if c else y) for x, y, c in zip(xarr, yarr, cond)]
print([round(x, 3) for x in result])

# This is an array.
print(np.where(cond, xarr, yarr))

# %%
np.random.seed(42)
arr = np.random.randn(4, 4)

print(arr)

# %%
np.where(arr > 0, 2, -2)

# %%
# Note that the operation is vectorized, thus one array is let pass.
np.where(arr > 0, 2, arr)

# %% [markdown]
# ## Mathematical and statistical methods

# %%
np.random.seed(42)
arr = np.random.randn(5, 4)

# One can call the method on the array or the np function.
print(arr.mean())
print(np.mean(arr))

# %%
arr.mean(axis=1)

# %%
arr = np.array([[0, 1, 2], [3, 4, 5], [6, 7, 8]])
print(arr)

# Cumsum on different axis.
print(arr.cumsum(axis=0))
print(arr.cumsum(axis=1))

# %%
arr = np.random.randn(100)

# Sum all positive numbers.
(arr > 0).sum()

# %%
bools = np.array([False, False, True, False])

print(bools.any())
print(bools.all())

# %%
## Sorting.

# %%
np.random.seed(8)
arr = np.random.randn(8)
print(arr)
arr.sort()
print(arr)

# %%
arr = np.random.randn(5, 3)
print(arr)

# %%
arr.sort(axis=1)
print(arr)

# %% [markdown]
# ## Unique and set logic

# %%
names = np.array(["Bob", "Joe", "Will", "Bob", "Will", "Joe", "Joe"])

print(np.unique(names))

# %%
values1 = np.array([6, 0, 0, 3, 2, 5, 6])
print(values1)

# Check memership of values in values1 wrt a given set.
print(np.in1d(values1, [2, 3, 6]))

# %%
values2 = np.array([6, 1, 7, 3, 2, 5, 6])
print("values1=", values1)
print("values2=", values2)

print("intersect=", np.intersect1d(values1, values2))
print("union=", np.union1d(values1, values2))
# A - B
print("diff=", np.setdiff1d(values1, values2))
# Symmetric difference: elements that in either of arrays, but not both.
print("xor=", np.setxor1d(values1, values2))

# %% [markdown]
# # File input and output

# %% [markdown]
# ## Storing arrays on disk in binary form.

# %%
arr = np.arange(10)
print(arr)
np.save("some_array.npy", arr)

# %%
arr2 = np.load("some_array.npy")
print(arr2)

# %%
np.savez("some_array_lazy.npz", arr2)

# %% [markdown]
# # Linear algebra

# %%
x = np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])
print("x=\n", x)
y = np.array([[6.0, 23.0], [-1, 7], [8, 9]])
print("y=\n", y)

# %%
print(x.dot(y))
print(np.dot(x, y))

# %%
from numpy.linalg import inv, qr

np.random.seed(42)

X = np.random.randn(5, 5)
mat = X.T.dot(X)
print("mat=\n", mat)

# %%
# Inverse.
inv(mat)

# %%
q, r = qr(mat)
print("q=\n", q)
print("r=\n", r)

# %%
print(np.diag(mat))

# %%
print(np.trace(mat))

# %%
# print(np.eig(mat))

# %%
# print(np.svd(mat))

# %% [markdown]
# # **Random number generator**

# %% [markdown]
# ## **Random walks**
