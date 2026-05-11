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

from matplotlib import pyplot as plt
import numpy as np
import pandas as pd


# %%
import helpers.hdbg as hdbg
import helpers.hnotebook as hnotebo

import msml610_utils as ut
import L08_04_07_metalearners_utils as mtl

ut.config_notebook()

# Initialize logger.
logging.basicConfig(level=logging.INFO)
_LOG = logging.getLogger(__name__)
hnotebo.set_logger_to_print(_LOG)
hnotebo.set_all_loggers_to_print()

# %%
import helpers.hmodule as hmodule

hmodule.install_module_if_not_present(
    ["lightgbm", "fklearn"],
    use_activate=True,
    use_sudo=False,
    venv_path="/opt/venv"
)

# %% [markdown]
# # Load data

# %%
dir_name = "L08_data"
# #!ls $dir_name

out_dir_name = "figures/"

# %%
data_biased = pd.read_csv(f"{dir_name}/email_obs_data.csv")
print("# data_biased")
print("num_rows=", len(data_biased))
display(data_biased.head())

data_rnd = pd.read_csv(f"{dir_name}/email_rnd_data.csv")
print("# data_rnd")
print("num_rows=", len(data_rnd))
display(data_rnd.head())

# %%
hdbg.dassert_eq(data_biased.columns.tolist(), data_rnd.columns.tolist())

# %%
y = "next_mnth_pv"
T = "mkt_email"
X = list(data_rnd.drop(columns=[y, T]).columns)

train, test = data_biased, data_rnd

# %%
display(train[[T, y]].head())

# %% [markdown]
# # T-Learner

# %%
from lightgbm import LGBMRegressor

np.random.seed(123)

m0 = LGBMRegressor()
m1 = LGBMRegressor()

m0.fit(train.query(f"{T}==0")[X], train.query(f"{T}==0")[y])
m1.fit(train.query(f"{T}==1")[X], train.query(f"{T}==1")[y]);

# %%
m0

# %%
t_learner_cate_test = test.assign(
    cate=m1.predict(test[X]) - m0.predict(test[X])
)

# %%
import fklearn.causal.validation.curves
import fklearn.causal.validation.auc

gain_curve_test = fklearn.causal.validation.curves.relative_cumulative_gain_curve(t_learner_cate_test, T, y, prediction="cate")
auc = fklearn.causal.validation.auc.area_under_the_relative_cumulative_gain_curve(t_learner_cate_test, T, y, prediction="cate")

plt.figure(figsize=(10,4))
plt.plot(gain_curve_test, color="C0", label=f"AUC: {auc:.2f}")
plt.hlines(0, 0, 100, linestyle="--", color="black", label="Baseline")

plt.legend();
_ = plt.title("T-Learner")

# %%
import warnings, logging
warnings.filterwarnings('ignore', category=UserWarning, module='lightgbm')

logging.getLogger("lightgbm").setLevel(logging.ERROR)

# %%
# TODO(ai_gp): Make the plots smaller.

# Generate synthetic data with treatment heterogeneity.
df = mtl.generate_synthetic_treatment_data(n0=500, n1=50, seed=123)

# Fit separate outcome models for control and treatment groups.
m0, m1, m0_hat, m1_hat = mtl.fit_outcome_models(df, min_child_samples=25)

# Visualize outcome models and heterogeneous treatment effects.
mtl.plot_treatment_effect_analysis(df, m0, m1, m0_hat, m1_hat)

# %% [markdown]
# # X-Learner

# %%
# TODO(ai_gp): Move to utils and add comments.

from sklearn.linear_model import LogisticRegression

np.random.seed(1)

mu_tau0 = LGBMRegressor(min_child_samples=25)
mu_tau1 = LGBMRegressor(min_child_samples=25)

mu_tau0.fit(df.query("t==0")[["x"]], tau_0)
mu_tau1.fit(df.query("t==1")[["x"]], tau_1)

mu_tau0_hat = mu_tau0.predict(df.query("t==0")[["x"]])
mu_tau1_hat = mu_tau1.predict(df.query("t==1")[["x"]])

plt.figure(figsize=(10, 4))
plt.scatter(df.query("t==0")[["x"]], tau_0, label="$\hat{\\tau_0}$", alpha=0.5, marker=marker[0], color=color[1])
plt.scatter(df.query("t==1")[["x"]], tau_1, label="$\hat{\\tau_1}$", alpha=0.8, marker=marker[1], color=color[0])
plt.plot(df.query("t==0")[["x"]], mu_tau0_hat, color="black", linestyle="solid", label="$\hat{\mu}\\tau 0$")
plt.plot(df.query("t==1")[["x"]], mu_tau1_hat, color="black", linestyle="dashed", label="$\hat{\mu}\\tau_1$")
plt.ylabel("Estimated Effect")
plt.xlabel("X")
plt.legend(fontsize=14)

# %%
# TODO(ai_gp): Move to utils and add comments.

plt.figure(figsize=(10, 4))

ps_model = LogisticRegression(penalty="none")
ps_model.fit(df[["x"]], df["t"])

ps = ps_model.predict_proba(df[["x"]])[:, 1]

cate = ((1-ps)*mu_tau1.predict(df[["x"]]) +
        ps*mu_tau0.predict(df[["x"]]))

plt.scatter(df.query("t==0")[["x"]], tau_0, label="$\hat{\\tau_0}$", alpha=0.5, s=100*(ps[df["t"]==0]),   marker=marker[0], color=color[1])
plt.scatter(df.query("t==1")[["x"]], tau_1, label="$\hat{\\tau_1}$", alpha=0.5, s=100*(1-ps[df["t"]==1]), marker=marker[1], color=color[0])

plt.plot(df[["x"]], cate, label="x-learner", color="black")
plt.ylabel("Estimated Effect")
plt.xlabel("X")
plt.legend(fontsize=14)
