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
import L08_04_05_causal_inference_utils as mtl0cire05

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

# %% [markdown]
# The dataset contains information on managers with the following variables:
#
# - **intervention**: Binary treatment indicator (1 = received training, 0 =
#   control)
# - **engagement_score**: Primary outcome—average standardized engagement score of
#   manager's employees
# - **department_id**: Unique department identifier
# - **tenure**: Years the manager has been with the company
# - **n_of_reports**: Number of direct reports the manager has
# - **gender**: Manager's identified gender (categorical)
# - **role**: Job category within the company (categorical)
# - **department_size**: Number of employees in the department
# - **department_score**: Average engagement score in the department
# - **last_engagement_score**: Previous period's engagement score for the manager

# %%
import helpers.hpandas_stats as hpanstat

show_distributions = True
show_correlations = True

hpanstat.explore_dataframe(df, show_distributions=show_distributions, show_correlations=show_correlations)

# %%
model = smf.ols("engagement_score ~ intervention",
        data=df).fit()
print("ATE:", model.params["intervention"])
print("95% CI:", model.conf_int().loc["intervention", :].values.T)

# %%
import statsmodels.formula.api as smf

smf.ols("engagement_score ~ intervention",
        data=df).fit().summary().tables[1]

# %%
mtl0cire05.plot_engagement_vs_intervention(df)

# %%
# Density curves comparing distributions
mtl0cire05.plot_engagement_density_by_intervention(df)

# %%
# TODO(gp): Switch to pdfs
mtl0cire05.plot_engagement_vs_intervention_by_department(df)

# %%
#mtl0cire05.plot_all_variables_vs_intervention(df)

# %%
mtl0cire05.plot_all_variables_density_by_intervention(df)

# %%
# To reduce this bias, you can adjust for the covariates you have in your data.
model = smf.ols("""
engagement_score ~ intervention
    + tenure + last_engagement_score + department_score
    + n_of_reports + C(gender) + C(role)""", data=df).fit()

print("ATE:", model.params["intervention"])
print("95% CI:", model.conf_int().loc["intervention", :].values.T)

# %%
model = smf.ols("engagement_score ~ intervention",
        data=df).fit()
print("ATE:", model.params["intervention"])
print("95% CI:", model.conf_int().loc["intervention", :].values.T)

# %%
- The effect estimate here is considerably smaller than the one you got earlier.
- This is some indication of positive bias, which means that managers whose
  employees were already more engaged are more likely to have participated in the
  manager training program

# %%
## Propensity score

# %%
ps_model = smf.logit("""
intervention ~ 
    tenure + last_engagement_score + department_score
    + C(n_of_reports) + C(gender) + C(role)""", data=df).fit(disp=0)

data_ps = df.copy()
data_ps["propensity_score"] = ps_model.predict(df)

data_ps[["intervention", "engagement_score", "propensity_score"]].head()

# %%
# Estimate using propensity score as confounder / covariate.
model = smf.ols("""
    engagement_score ~ intervention + propensity_score
    """, data=data_ps).fit()
print(model.params["intervention"])

# %%
## Propensity score matching

# %%
from sklearn.neighbors import KNeighborsRegressor

T = "intervention"
X = "propensity_score"
Y = "engagement_score"
treated = data_ps.query(f"{T}==1")
untreated = data_ps.query(f"{T}==0")
mt0 = KNeighborsRegressor(n_neighbors=1).fit(untreated[[X]],
untreated[Y])
mt1 = KNeighborsRegressor(n_neighbors=1).fit(treated[[X]], treated[Y])
predicted = pd.concat([
# find matches for the treated looking at the untreated knn model
treated.assign(match=mt0.predict(treated[[X]])),
# find matches for the untreated looking at the treated knn model
untreated.assign(match=mt1.predict(untreated[[X]]))
])
predicted.head()

# %%
hat_ATE = np.mean((predicted[Y] - predicted["match"])*predicted[T] 
        + (predicted["match"] - predicted[Y])*(1-predicted[T]))
print(hat_ATE)

# %%
