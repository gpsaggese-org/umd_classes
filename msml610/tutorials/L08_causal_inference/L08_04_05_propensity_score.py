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

import numpy as np
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
# TODO(ai_gp): Simplify and comment code and move to utility.
weight_t = 1/data_ps.query("intervention==1")["propensity_score"]
weight_nt = 1/(1-data_ps.query("intervention==0")["propensity_score"])
t1 = data_ps.query("intervention==1")["engagement_score"] 
t0 = data_ps.query("intervention==0")["engagement_score"] 

y1 = sum(t1*weight_t)/len(data_ps)
y0 = sum(t0*weight_nt)/len(data_ps)

print("E[Y1]:", y1)
print("E[Y0]:", y0)
print("ATE", y1 - y0)

# %% [markdown]
# # Variance

# %%
from sklearn.linear_model import LogisticRegression
from patsy import dmatrix

# TODO(ai_gp): Simplify and comment code and move to utility.

# define function that computes the IPW estimator
def est_ate_with_ps(df, ps_formula, T, Y):
    
    X = dmatrix(ps_formula, df)
    ps_model = LogisticRegression(
                                  max_iter=1000).fit(X, df[T])
    ps = ps_model.predict_proba(X)[:, 1]
    
    # compute the ATE
    return np.mean((df[T]-ps) / (ps*(1-ps)) * df[Y]) 


# %%
formula = """tenure + last_engagement_score + department_score
+ C(n_of_reports) + C(gender) + C(role)"""
T = "intervention"
Y = "engagement_score"

est_ate_with_ps(df, formula, T, Y)

# %%
from joblib import Parallel, delayed # for parallel processing

def bootstrap(data, est_fn, rounds=200, seed=123, pcts=[2.5, 97.5]):
    np.random.seed(seed)
    
    stats = Parallel(n_jobs=4)(
        delayed(est_fn)(data.sample(frac=1, replace=True))
        for _ in range(rounds)
    )
    
    return np.percentile(stats, pcts)


# %%
print(f"ATE: {est_ate_with_ps(df, formula, T, Y)}")

est_fn = lambda data: est_ate_with_ps(data, ps_formula=formula, T=T, Y=Y)

print("95% C.I.: ", bootstrap(df, est_fn))

# %% [markdown]
# # Stabilized Propensity Weights

# %%
print("Original Sample Size:", data_ps.shape[0])
print("Treated Pseudo-Population Sample Size:", sum(weight_t))
print("Untreated Pseudo-Population Sample Size:", sum(weight_nt))

# %%
# TODO(ai_gp): Simplify and comment code and move to utility.

p_of_t = data_ps["intervention"].mean()

t1 = data_ps.query("intervention==1")
t0 = data_ps.query("intervention==0")

weight_t_stable = p_of_t/t1["propensity_score"]
weight_nt_stable = (1-p_of_t)/(1-t0["propensity_score"])

print("Treat size:", len(t1))
print("W treat", sum(weight_t_stable))

print("Control size:", len(t0))
print("W treat", sum(weight_nt_stable))

# %%
nt = len(t1)
nc = len(t0)

y1 = sum(t1["engagement_score"]*weight_t_stable)/nt
y0 = sum(t0["engagement_score"]*weight_nt_stable)/nc

print("ATE: ", y1 - y0)

# %%
# TODO(ai_gp): Simplify and comment code and move to utility.

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12,5), sharex=True, sharey=True)

sns.histplot(data_ps.query("intervention==0")["propensity_score"], stat="probability",
             label="Not Treated", color="C0", bins=30, ax=ax1, alpha=0.5)
sns.histplot(data_ps.query("intervention==1")["propensity_score"], stat="probability",
             label="Treated", color="C2", alpha=0.5, bins=30, ax=ax1)
ax1.set_title("Propensity Distribution")

sns.histplot(data_ps.query("intervention==0").assign(w=weight_nt_stable),
             x="propensity_score", stat="probability",
             color="C0", weights="w", label="Non Treated", bins=30, ax=ax2,  alpha=0.5)

sns.histplot(data_ps.query("intervention==1").assign(w=weight_t_stable),
             x="propensity_score", stat="probability",
             color="C2", weights="w", label="Treated", bins=30, alpha=0.5, ax=ax2)
ax2.set_title("Weighted Propensity Distribution")
plt.legend()

plt.tight_layout()
