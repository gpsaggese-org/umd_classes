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
import os

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
import helpers.hnotebook as hnotebo

import msml610_utils as ut
#import L08_04_05_causal_inference_utils as mtl0cireout

ut.config_notebook()

# Initialize logger.
logging.basicConfig(level=logging.INFO)
_LOG = logging.getLogger(__name__)
hnotebo.set_logger_to_print(_LOG)
hnotebo.set_all_loggers_to_print()

# %%
dir_name = "L08_data"
# #!ls $dir_name

out_dir_name = "figures/"

# %%
import pandas as pd
import numpy as np

df = pd.read_csv(os.path.join(dir_name, "management_training.csv"))
import helpers.hpandas_display as hpanddis

hpanddis.display_df(df)

# %%
import helpers.hpandas_stats as hpanstat

hpanstat.explore_dataframe(df)

# %%
import statsmodels.formula.api as smf

smf.ols("engagement_score ~ intervention",
        data=df).fit().summary().tables[1]
