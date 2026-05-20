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
import os

import pandas as pd


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

import helpers.htutorial as ut
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
df = pd.read_csv(os.path.join(dir_name, "management_training.csv"))
import helpers.hpandas_display as hpandisp

hpandisp.display_df(df)

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

hpanstat.explore_dataframe(
    df,
    show_distributions=show_distributions,
    show_correlations=show_correlations,
)

# %%
import statsmodels.formula.api as smf

# %%
model = smf.ols("engagement_score ~ intervention", data=df).fit()
print("ATE:", model.params["intervention"])
print("95% CI:", model.conf_int().loc["intervention", :].values.T)

smf.ols("engagement_score ~ intervention", data=df).fit().summary().tables[1]

# %%
mtl0cire05.plot_engagement_vs_intervention(df)

# %%
# Density curves comparing distributions
mtl0cire05.plot_engagement_vs_intervention(df)

# %%
mtl0cire05.plot_engagement_vs_intervention_by_department(df)

# %%
# mtl0cire05.plot_all_variables_vs_intervention(df)

# %%
mtl0cire05.plot_all_variables_density_by_intervention(df)

# %%
# To reduce this bias, you can adjust for the covariates you have in your data.
model = smf.ols(
    """
    engagement_score ~ intervention
        + tenure + last_engagement_score + department_score
        + n_of_reports + C(gender) + C(role)""",
    data=df,
).fit()

print("ATE:", model.params["intervention"])
print("95% CI:", model.conf_int().loc["intervention", :].values.T)

# %%
model = smf.ols("engagement_score ~ intervention", data=df).fit()
print("ATE:", model.params["intervention"])
print("95% CI:", model.conf_int().loc["intervention", :].values.T)

# %% [markdown]
# - The effect estimate here is considerably smaller than the one you got earlier.
# - This is some indication of positive bias, which means that managers whose
#   employees were already more engaged are more likely to have participated in the
#   manager training program

# %% [markdown]
# ## Propensity score

# %%
ps_model = smf.logit(
    """
    intervention ~
        tenure + last_engagement_score + department_score
        + C(n_of_reports) + C(gender) + C(role)""",
    data=df,
).fit(disp=0)

data_ps = df.copy()
data_ps["propensity_score"] = ps_model.predict(df)

data_ps[["intervention", "engagement_score", "propensity_score"]].head()

# %%
# Estimate using propensity score as confounder / covariate.
model = smf.ols(
    """
    engagement_score ~ intervention + propensity_score
    """,
    data=data_ps,
).fit()
print(model.params["intervention"])

# %% [markdown]
# ## Propensity score matching

# %%
# Perform 1-nearest neighbor propensity score matching.
predicted = mtl0cire05.propensity_score_matching(data_ps)
predicted.head()

# %%
# Calculate average treatment effect from propensity score matching.
hat_ATE = mtl0cire05.calculate_psm_ate(predicted)
print(f"ATE (Propensity Score Matching): {hat_ATE:.4f}")

# %%
# Plot inverse probability of treatment weighting results.
mtl0cire05.plot_iptw(data_ps)

# %%
# Estimate ATE using IPTW.
weighted_e_y1, weighted_e_y0, hat_ATE = mtl0cire05.estimate_ate_iptw(data_ps)

print("E[Y1]:", weighted_e_y1)
print("E[Y0]:", weighted_e_y0)
print("ATE:", hat_ATE)

# %% [markdown]
# # Variance

# %%
# Prepare formula and variables for IPW estimation.
formula = """
tenure + last_engagement_score + department_score
    + C(n_of_reports) + C(gender) + C(role)
"""
T = "intervention"
Y = "engagement_score"

# %%
# Estimate ATE using IPW estimator.
ate_ipw = mtl0cire05.estimate_ate_with_ps(
    df, formula, treatment_col=T, outcome_col=Y
)
print(f"ATE (IPW): {ate_ipw:.4f}")

# %%
# Compute bootstrap 95% confidence interval for ATE using IPW.
print(f"ATE: {ate_ipw:.4f}")

# Define bootstrap function that resamples data and computes ATE.
est_fn = lambda data: mtl0cire05.estimate_ate_with_ps(
    data, ps_formula=formula, treatment_col=T, outcome_col=Y
)

# Estimate confidence interval using bootstrap resampling.
ci = mtl0cire05.estimate_confidence_interval_bootstrap(
    df, est_fn, rounds=200, seed=123, n_jobs=4, pcts=[2.5, 97.5]
)
print(f"95% Confidence interval: {ci}")

# %% [markdown]
# # Stabilized Propensity Weights

# %%
# Show sample sizes for original and pseudo-population.
print("Original Sample Size:", data_ps.shape[0])

# Compute sample sizes after IPTW weighting.
treated = data_ps.query("intervention==1")
control = data_ps.query("intervention==0")

weight_t = 1 / treated["propensity_score"]
weight_nt = 1 / (1 - control["propensity_score"])

print("Treated Pseudo-Population Sample Size:", sum(weight_t))
print("Untreated Pseudo-Population Sample Size:", sum(weight_nt))

# %%
# Estimate ATE using stabilized propensity weights.
ate_stabilized = mtl0cire05.estimate_ate_stabilized_weights(data_ps)

print(f"ATE (Stabilized Weights): {ate_stabilized:.4f}")

# %%
# Plot propensity score distributions before and after weighting.
mtl0cire05.plot_propensity_distributions(data_ps)

# %%
