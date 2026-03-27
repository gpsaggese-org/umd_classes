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

# %%
# !sudo /bin/bash -c "(source /venv/bin/activate; pip install --quiet pymc-bart)"

import pymc_bart as pmb

print(pmb.__version__)

# %%
# %load_ext autoreload
# %autoreload 2


import arviz as az
import pandas as pd
import pymc as pm

# %%
dir_name = "/app/code/book.2018.Martin.Bayesian_Analysis_with_Python.2e"
# #!ls $dir_name/data2
data = pd.read_csv(dir_name + "/data2/penguins.csv")
data.head()

# %%
data_tmp = data[
    ["flipper_length", "bill_depth", "bill_length", "body_mass"]
].dropna()
X = data_tmp[["flipper_length", "bill_depth", "bill_length"]]
Y = data_tmp["body_mass"]

# %%
Y

# %%
# Create a probabilistic model context.
with pm.Model() as model_pen:
    # Define a HalfNormal prior for the observation noise standard deviation.
    sigma = pm.HalfNormal("sigma", 1)
    # Use Bayesian Additive Regression Trees (BART) to model the mean function mu from predictors X and response Y.
    mu = pmb.BART("mu", X, Y)
    # Define a Normal likelihood with mean mu and standard deviation mu, conditioned on observed data Y.
    y = pm.Normal("y", mu=mu, sigma=mu, observed=Y)
    # Sample from the posterior distribution using default settings.
    idata_pen = pm.sample()
    # Generate posterior predictive samples and add them to the inference data.
    pm.sample_posterior_predictive(idata_pen, extend_inferencedata=True)

# %%
az.plot_ppc(idata_pen)

# %%
pmb.plot_pdp(mu, X, Y)

# %%
pmb.plot_ice(mu, X, Y)

# %%
pmb.plot_variable_importance(idata_pen, mu, X)
