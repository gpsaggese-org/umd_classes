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
# ## Imports

# %%
# %load_ext autoreload
# %autoreload 2

import logging

import pandas as pd

try:
    from IPython.display import display
except ImportError:
    display = print  # type: ignore


# %%
import helpers.hnotebook as hnotebo

import helpers.htutorial as ut
# import L08_04_08_difference_in_difference_utils as mtl

ut.config_notebook()

# Initialize logger.
logging.basicConfig(level=logging.INFO)
_LOG = logging.getLogger(__name__)
hnotebo.set_logger_to_print(_LOG)
hnotebo.set_all_loggers_to_print()

# %%
# import warnings

# import helpers.hmodule as hmodule
# from lightgbm import LGBMRegressor
# import fklearn.causal.validation.curves
# import fklearn.causal.validation.auc

# warnings.filterwarnings("ignore", category=UserWarning, module="lightgbm")
# warnings.filterwarnings(
#    "ignore",
#    message="X does not have valid feature names",
#    category=UserWarning,
# )
# logging.getLogger("lightgbm").setLevel(logging.ERROR)

# hmodule.install_module_if_not_present(
#    ["lightgbm", "fklearn"],
#    use_activate=True,
#    use_sudo=False,
#    venv_path="/opt/venv",
# )

# %% [markdown]
# # Load data

# %%
dir_name = "L08_data"
# #!ls $dir_name

out_dir_name = "figures/"

# %%
mkt_data = pd.read_csv(f"{dir_name}/short_offline_mkt_south.csv").astype(
    {"date": "datetime64[ns]"}
)
print("mkt_data=", mkt_data.shape)
display(mkt_data.head())

# Marketing data in a panel format.
# - Each line is a (`date`, `city`)
# - The outcome to predict is `downloads`
# - `treated` is the indicator of the intervention
# - `tau` is the treatment effect

# %%
# Compute pre- and post-intervention period.
(
    mkt_data.assign(w=lambda d: d["treated"] * d["post"])
    .groupby(["w"])
    .agg({"date": ["min", "max"]})
)

# %%
## Canonical DiD

# %%
did_data = mkt_data.groupby(["treated", "post"]).agg(
    {"downloads": "mean", "date": "min"}
)

did_data

# %%
y0_est = (
    did_data.loc[1].loc[0, "downloads"]  # treated baseline
    # control evolution
    + did_data.loc[0].diff().loc[1, "downloads"]
)

att = did_data.loc[1].loc[1, "downloads"] - y0_est
att

# %%
mkt_data.query("post==1").query("treated==1")["tau"].mean()
