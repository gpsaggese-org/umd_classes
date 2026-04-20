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
# ## Imports

# %%
# %load_ext autoreload
# %autoreload 2

import logging

import matplotlib.pyplot as plt
import seaborn as sns

# %%
# import helpers.hmodule as hmodule

# hmodule.install_module_if_not_present(
#     "networkx",
#     use_activate=True,
# )
# hmodule.install_module_if_not_present(
#     "pgmpy",
#     use_activate=True,
# )

# %%
import msml610_utils as ut
import L08_04_05_causal_inference_utils as mtl0cireout

ut.config_notebook()

# Initialize logger.
logging.basicConfig(level=logging.INFO)
_LOG = logging.getLogger(__name__)
