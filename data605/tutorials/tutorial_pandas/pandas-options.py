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
#     display_name: Python [default]
#     language: python
#     name: python3
# ---

# %% [markdown] toc="true"
# # Table of Contents
#  <p><div class="lev1 toc-item"><a href="#Refs" data-toc-modified-id="Refs-1"><span class="toc-item-num">1&nbsp;&nbsp;</span>Refs</a></div><div class="lev1 toc-item"><a href="#Assigning-directly" data-toc-modified-id="Assigning-directly-2"><span class="toc-item-num">2&nbsp;&nbsp;</span>Assigning directly</a></div><div class="lev1 toc-item"><a href="#get-/-set" data-toc-modified-id="get-/-set-3"><span class="toc-item-num">3&nbsp;&nbsp;</span>get / set</a></div><div class="lev1 toc-item"><a href="#describe_option" data-toc-modified-id="describe_option-4"><span class="toc-item-num">4&nbsp;&nbsp;</span>describe_option</a></div><div class="lev1 toc-item"><a href="#Context" data-toc-modified-id="Context-5"><span class="toc-item-num">5&nbsp;&nbsp;</span>Context</a></div><div class="lev1 toc-item"><a href="#Typical-settings" data-toc-modified-id="Typical-settings-6"><span class="toc-item-num">6&nbsp;&nbsp;</span>Typical settings</a></div><div class="lev1 toc-item"><a href="#Plot" data-toc-modified-id="Plot-7"><span class="toc-item-num">7&nbsp;&nbsp;</span>Plot</a></div>

# %% [markdown]
# # Refs
#
# https://pandas.pydata.org/pandas-docs/stable/options.html

# %%
import pandas as pd
import numpy as np

# %% [markdown]
# # Assigning directly

# %%
print(pd.options.display.max_rows)

pd.options.display.max_rows = 999

print(pd.options.display.max_rows)

# %% [markdown]
# # get / set

# %%
pd.get_option("display.max_rows")

# %%
pd.set_option("display.max_rows", 5)

# %%
pd.get_option("display.max_rows")

# %% [markdown]
# # describe_option

# %%
pd.describe_option("display.max_rows")

# %%
pd.describe_option()

# %% [markdown]
# # Context

# %%
print("\ndisplay.max_rows=", pd.get_option("display.max_rows"))
print("display.max_columns=", pd.get_option("display.max_columns"))

with pd.option_context("display.max_rows", 10, "display.max_columns", 5):
    print("\ndisplay.max_rows=", pd.get_option("display.max_rows"))
    print("display.max_columns=", pd.get_option("display.max_columns"))

print("\ndisplay.max_rows=", pd.get_option("display.max_rows"))
print("display.max_columns=", pd.get_option("display.max_columns"))

# %% [markdown]
# # Typical settings

# %%
pd.set_option("display.max_rows", 500)
pd.set_option("display.max_columns", 500)
pd.set_option("display.width", 1000)

# %% [markdown]
# # Plot

# %%
pd.Series(np.random.randn(1000)).hist()

# %%
pd.Series(np.random.randn(1000)).plot()

# %%
# Passing matplotlib / pd options.
pd_params = {"fontsize": 20, "rot": 0}

pd.Series(np.random.randn(1000)).plot(**pd_params)

# %%
# pd.describe_option("fontsize")
