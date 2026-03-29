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

# %% [markdown] toc=true
# <h1>Table of Contents<span class="tocSkip"></span></h1>
# <div class="toc"><ul class="toc-item"><li><span><a href="#Ipython" data-toc-modified-id="Ipython-1"><span class="toc-item-num">1&nbsp;&nbsp;</span>Ipython</a></span><ul class="toc-item"><li><span><a href="#Tab-completion" data-toc-modified-id="Tab-completion-1.1"><span class="toc-item-num">1.1&nbsp;&nbsp;</span>Tab completion</a></span></li><li><span><a href="#Introspection" data-toc-modified-id="Introspection-1.2"><span class="toc-item-num">1.2&nbsp;&nbsp;</span>Introspection</a></span></li><li><span><a href="#The-%run-command" data-toc-modified-id="The-%run-command-1.3"><span class="toc-item-num">1.3&nbsp;&nbsp;</span>The %run command</a></span></li><li><span><a href="#Magic-commands" data-toc-modified-id="Magic-commands-1.4"><span class="toc-item-num">1.4&nbsp;&nbsp;</span>Magic commands</a></span></li></ul></li></ul></div>

# %% [markdown]
# # Ipython
#
# - Execute-explore workflow vs edit-compile-run workflow
#
# - Data analysis requires trial and error, iteration
#
# ## Tab completion
#
# - To show a private method, you need to type the underscore
# - Works for file system too

# %% [markdown]
# ## Introspection

# %%
b = 5

# %%
# ?b

# %%
# b?

# %%
??b

# %%
help(b)

# %%
# One can use * and ? to search namespace using regex.

import numpy as np

# np.*load*?

# %% [markdown]
# ## The %run command
#
# - One can run a python program inside an ipython session
# - The script is run in an empty namespace, so that the behavior should be identical to running the script as `python script.py`
# - `%run -i` starts from current namespace
# - one can also pass values that are readh through `sys.argv`

# %% [markdown]
# ## Magic commands

# %%
a = np.random.randn(100, 100)

# %timeit np.dot(a, a)

# %%
# #%reset?

# %%
# Short doc.
# #%quickref

# Long doc.
# #%magic
