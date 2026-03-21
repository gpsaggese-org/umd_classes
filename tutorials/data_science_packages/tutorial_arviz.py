# ---
# jupyter:
#   jupytext:
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
# # Imports

# %%
try:
    import arviz as az
except ModuleNotFoundError:
    # !sudo /bin/bash -c "(source /venv/bin/activate; pip install --quiet arviz)"
    pass

try:
    import graphviz
except ModuleNotFoundError:
    # !sudo /bin/bash -c "(source /venv/bin/activate; pip install --quiet graphviz)"
    pass

# %% [markdown]
# ## Print config

# %%
# !python --version

# !uname -a

#
import numpy as np

print("numpy version=", np.__version__)

#
import pymc as pm

print("pymc3 version=", pm.__version__)

import matplotlib

print("matplotlib version=", matplotlib.__version__)

#
import arviz as az

print("arviz version=", az.__version__)

#
import graphviz

print("graphviz version=", graphviz.__version__)

# %%
plt.rcParams["figure.figsize"] = [8, 3]

# %% [markdown]
# From https://python.arviz.org/en/latest/index.html
#
# - ArviZ is a package for exploratory analysis of Bayesian models.
# - It is backend agnostic (e.g., PyStan, PyMC, raw `numpy` arrays)

# %% [markdown]
# # Getting Started
#
# From https://python.arviz.org/en/latest/getting_started/index.html#

# %% [markdown]
# ## ArviZ quickstart
#
# https://python.arviz.org/en/latest/getting_started/Introduction.html

# %% [markdown]
# ### Get started with plotting

# %%
# - Plot a distribution with some info about HDI (highest density interval).

# Sample a Gaussian.
np.random.seed(42)
vals = np.random.randn(100_000)
print("vals.shape=", vals.shape)
print("vals=", vals)

# Plot PDF.
az.plot_posterior(vals);

# %%
# `arviz` interprets a 2d array as "chain x draws".
# Build 10 chains and 50 draws each.
size = (10, 50)
vals = np.random.randn(*size)

# When plotting all the samples are flattened.
az.plot_posterior(vals);

# %%
# /venv/lib/python3.9/site-packages/arviz/plots/backends/matplotlib/forestplot.py:545: UserWarning: The `squeeze` kwarg to GroupBy is being
# removed.Pass .groupby(..., squeeze=False) to disable squeezing, which is the new default, and to silence this warning.
# for _, sub_data in grouped_datum:
# warnings.filterwarnings("error", category=FutureWarning, message="Series.__getitem__")

# %%
size = (5, 50)

# A dict is interpreted as multiple random vars, each with different "chains x draws".
data = {
    "normal": np.random.randn(*size),
    "gumbel": np.random.gumbel(size=size),
    # "student t": np.random.standard_t(df=6, size=size),
    # "exponential": np.random.exponential(size=size),
}
az.plot_forest(data);
# There are several RVs, each with 5 realizations, each realization with 50 samples.

# %%
az.plot_posterior(data["normal"][0])
az.plot_posterior(data["normal"][1]);

# %%
# data["normal"] is a 10 chains x 50 samples, but when plotting all the data is concat.
az.plot_posterior(data["normal"]);

# %% [markdown]
# ### PyMC integration

# %%

# %% [markdown]
# ### InferenceData
#
# From https://python.arviz.org/en/latest/getting_started/Introduction.html#convert-to-inferencedata
#
# The object returned by most PyMC sampling methods is `arviz.InferenceData`.

# %%
# 8 school examples
# - there are 8 schools (each with a name)
# -

J = 8
# Observations.
# - Mean (unknown).
y = np.array([28.0, 8.0, -3.0, 7.0, -1.0, 1.0, 18.0, 12.0])
# - Std dev (is known).
sigma = np.array([15.0, 10.0, 16.0, 11.0, 9.0, 11.0, 10.0, 18.0])

schools = np.array(
    [
        "Choate",
        "Deerfield",
        "Phillips Andover",
        "Phillips Exeter",
        "Hotchkiss",
        "Lawrenceville",
        "St. Paul's",
        "Mt. Hermon",
    ]
)

# with pm.Model() as centered_eight:
#    # 8 normal RVs for the mean.
#    mu = pm.Normal("mu", mu=0, sigma=5)
#    tau = pm.HalfCauchy("tau", beta=5)
#    theta = pm.Normal("theta", mu=mu, sigma=tau, shape=J)
#    # The observed data has:
#    # - random means and
#    # - known std dev.
#    obs = pm.Normal("obs", mu=theta, sigma=sigma, observed=y)
#    # This pattern is useful in PyMC3.
#    #prior = pm.sample_prior_predictive()
#    # Sample the posterior.
#    centered_eight_trace = pm.sample(
#        # Return data as arviz.InferenceData instead of MultiTrace.
#        return_inferencedata=False)
#    posterior_predictive = pm.sample_posterior_predictive(centered_eight_trace)

# %%
# pm.model_to_graphviz(centered_eight)

# %% [markdown]
# - Most ArviZ functions accept `trace` objects.
# - It can be converted into `InferenceData`

# %%
# print(type(centered_eight))
# print(centered_eight)

# print(type(centered_eight_trace))
# print(centered_eight_trace)

# %%
with pm.Model(coords={"school": schools}) as centered_eight:
    mu = pm.Normal("mu", mu=0, sigma=5)
    tau = pm.HalfCauchy("tau", beta=5)
    theta = pm.Normal("theta", mu=mu, sigma=tau, dims="school")
    pm.Normal("obs", mu=theta, sigma=sigma, observed=y, dims="school")

    # This pattern can be useful in PyMC
    idata = pm.sample_prior_predictive()
    idata.extend(pm.sample())
    pm.sample_posterior_predictive(idata, extend_inferencedata=True)

# %%
idata

# %%
az.plot_autocorr(centered_eight_trace)

# %%
# Build the inference data from PyMC3 run.
data = az.from_pymc(
    trace=centered_eight_trace,
    prior=prior,
    posterior_predictive=posterior_predictive,
    model=centered_eight,
    coords={"school": schools},
    dims={"theta": ["school"], "obs": ["school"]},
)
data

# %% [markdown]
# ## Introduction to xarray, InferenceData, netCDF
#
# https://python.arviz.org/en/latest/getting_started/XarrayforArviZ.html

# %% [markdown]
# There are several data structures that `ArviZ` relies on:
# - NumPy arrays
# - xarray.Dataset
# - arviz.InferenceData
# - netCDF

# %% [markdown]
# Bayesian inference generates numerous datasets:
# - Prior / posterior distribution for N variables
# - Observed data
# - Prior / posterior predictive distribution
# - Trace data for each inference run
# - Sample statistics for each inference run
#
# Data from probabilistic programming is high-dimensional
# - Use `xarray` to store high-dimensional data with human readable dimensions and coordinates
#
# Different Bayesian modeling libraries (e.g., PyMC3, Pyro, PyStan) generate data in different formats

# %%
print(az.list_datasets()[:1000])

# %%
# From Bayesian Data Analysis, section 5.5 (Gelman et al. 2013):

# Analyze the effects of special coaching programs for SAT-V (Scholastic Aptitude Test-Verbal) in each of eight high schools.
# - The outcome variable in each study was the score on a special administration of the SAT-V
# - the scores can vary between 200 and 800, with mean about 500 and standard deviation about 100

# %%
data = az.load_arviz_data("centered_eight")
data

# %% [markdown]
# - There are multiple datasets (e.g., posterior, prior, observed data)
# - Each dataset is a `xarray.Dataset`
#     - There are 8 schools
#     - There are 3 variables (mu, theta, tau)
#     - 4 chains
#     - Each chain has 500 draws
#
# - Each dataset has different sizes, so we can't store them in a single xarray

# %%
# Print prior.
data.prior

# %%
# Print one dataset.
data.observed_data

# %% [markdown]
# ### netCDF
#
# - `arviz.InferenceData` and `xarray.Dataset` store data in memory
# - netCDF is a standard for serializing array oriented files
#     - netCDF corresponds to a `arviz.InferenceData`

# %% [markdown]
# ## Creating InferenceData
#
# https://python.arviz.org/en/latest/getting_started/CreatingInferenceData.html

# %% [markdown]
# - `arviz.InferenceData` is the central format of Arviz
# - It is a container that maintains references to one or more `xarray.Dataset`

# %%
# Build from 1D numpy array
size = 100
data = np.random.randn(size)
dataset = az.convert_to_inference_data(data)
dataset

# %%
# Build from nD numpy array
shape = (1, 2, 3, 4, 5)
data = np.random.randn(*shape)
print("data.shape=", data.shape)
dataset = az.convert_to_inference_data(data)
dataset

# %% [markdown]
# The 5 dimensions are interpreted as "chain", "draw" and the rests are dimensions of the data

# %% [markdown]
# InferenceData can also be built from dictionary and pd.DataFrame

# %%
# Build from PyMC.

import pymc as pm

draws = 500
chains = 2
data = {
    "J": 8,
    "y": np.array([28.0, 8.0, -3.0, 7.0, -1.0, 1.0, 18.0, 12.0]),
    "sigma": np.array([15.0, 10.0, 16.0, 11.0, 9.0, 11.0, 10.0, 18.0]),
}

with pm.Model() as model:
    mu = pm.Normal("mu", mu=0, sigma=5)
    tau = pm.HalfCauchy("tau", beta=5)
    theta_tilde = pm.Normal("theta_tilde", mu=0, sigma=1, shape=data["J"])
    theta = pm.Deterministic("theta", mu + tau * theta_tilde)
    pm.Normal("obs", mu=theta, sigma=data["sigma"], observed=data["y"])
    #
    idata = pm.sample(draws, chains=chains)
    pm.sample_posterior_predictive(idata, extend_inferencedata=True)
    # prior = pm.sample_prior_predictive()
    # posterior_predictive = pm.sample_posterior_predictive(trace)

    # pm_data = az.from_pymc3(
    #     trace=trace,
    #     prior=prior,
    #     posterior_predictive=posterior_predictive,
    #     coords={"school": np.arange(data["J"])},
    #     dims={"theta": ["school"], "theta_tilde": ["school"]})

# %%
idata

# %% [markdown]
# ## Working with InferenceData
#
# https://python.arviz.org/en/latest/getting_started/WorkingWithInferenceData.html

# %%
# Combine chains and draws.
stacked = az.extract(idata)
stacked

# %%
# Extract a NumPy array for a param.
stacked.mu.values[:10]

# %%
idata.observed_data

# %% [markdown]
# # Example gallery
#
# https://python.arviz.org/en/latest/examples/index.html

# %% [markdown]
# # User guide

# %% [markdown]
# ## Plotting
#
# https://python.arviz.org/en/latest/user_guide/plotting.html

# %% [markdown]
# ## Data structures
#
# https://python.arviz.org/en/latest/user_guide/data_structures.html

# %% [markdown]
# ### Label guide
#
# https://python.arviz.org/en/latest/user_guide/label_guide.html

# %% [markdown]
# ### InferenceData schema
#
# https://python.arviz.org/en/latest/schema/schema.html#schema

# %% [markdown]
# ## Computation
#
# https://python.arviz.org/en/latest/user_guide/computation.html

# %% [markdown]
# ## Sampling wrappers
#
# https://python.arviz.org/en/latest/user_guide/sampling_wrappers.html

# %%
