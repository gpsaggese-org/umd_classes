# ---
# jupyter:
#   jupytext:
#     default_lexer: ipython3
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
# # Bayesian Coin

# %% tags=["remove-cell"]
# !sudo /bin/bash -c "(source /venv/bin/activate; pip install --quiet jupyterlab-vim)"
# !jupyter labextension enable

# %% tags=["remove-cell"]
# !sudo /bin/bash -c "(source /venv/bin/activate; pip install --quiet graphviz)"

# %% tags=["remove-cell"]
# !sudo /bin/bash -c "(source /venv/bin/activate; pip install --quiet dataframe_image)"

# %% [markdown]
# ### Import modules

# %% tags=["remove-cell"]
# %load_ext autoreload
# %autoreload 2


import arviz as az
import pymc as pm
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
import preliz as pz

# %% tags=["remove-cell"]
import msml610_utils as ut

ut.config_notebook()

# %% [markdown] heading_collapsed=true
# # Chap1: Thinking probabilistically

# %% [markdown]
# ## Binomial
#
# Probability of $k$ heads out of $n$ tosses given bias $p$
#
# \begin{align*}
#   & X \sim Binomial(n, p) \\
#   & \Pr(k) = \frac{n!}{k! (n - k)!} p^k (1 - p)^{n-k} \\
# \end{align*}

# %%
# help(pz.Binomial.plot_interactive)

# %%
np.random.seed(42)

# Create a Normal Gaussian.
n = 8
# p = 0.25
p = 0.01
X = stats.binom(n, p)

# Print 3 realizations.
x = X.rvs(n)
print(x)

# %%
ut.plot_binomial()

# %%
params = {
    # "kind": "cdf",
    "kind": "pdf",
    "pointinterval": False,
    "interval": "hdi",  # Highest density interval.
    # "interval": "eti",  # Equal tailed interval.
    "xy_lim": "auto",
}

# Probability of k successes on N trial flipping a coin with p success
pz.Binomial(p=0.5, n=5).plot_interactive(**params)

# %% [markdown]
# ## Beta
#
# - Continuous prob distribution defined in [0, 1]
# - It is useful to model probability or proportion
#     - E.g., the probability of success in a Bernoulli trial
#
# - alpha represents "success" parameter
# - beta represents "failure" parameter
#     - When alpha is larger than beta the distribution skews toward 1, indicating a higher probability of success
#     - When alpha = beta the distribution is symmetric and centered around 0.5

# %%
np.random.seed(123)

trials = 4
# Unknown value.
theta_real = 0.35

# Generate some values.
data = stats.bernoulli.rvs(p=theta_real, size=trials)
print(data)

# %%
ut.plot_beta()

# %%
params = {
    # "kind": "cdf",
    "kind": "pdf",
    "pointinterval": False,
    "interval": "hdi",  # Highest density interval.
    # "interval": "eti",  # Equal tailed interval.
    "xy_lim": "auto",
}

alpha = 3.0
beta = 1.0

pz.Beta(alpha=alpha, beta=beta).plot_interactive(**params)

# %% [markdown]
# # Coin problem: analytical solution

# %%
ut.update_prior()

# %%
import inspect

func = ut.update_prior
code = inspect.getsource(func)
# display(Code(code))

# %%
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter
from IPython.core.display import HTML

formatter = HtmlFormatter(style="default", full=True, cssclass="codehilite")
highlighted_code = highlight(code, PythonLexer(), formatter)
display(HTML(highlighted_code))

# %% [markdown]
# ## Coin problem: PyMC solution

# %%
np.random.seed(123)
n = 4
# Unknown value.
theta_real = 0.35

# Generate some observational data.
data1 = stats.bernoulli.rvs(p=theta_real, size=n)
data1

# %%
with pm.Model() as model1:
    # Prior.
    theta = pm.Beta("theta", alpha=1.0, beta=1.0)
    # Likelihood.
    y = pm.Bernoulli("y", p=theta, observed=data1)
    # (Numerical) Inference to estimate the posterior distribution through samples.
    idata1 = pm.sample(1000, random_seed=123)

# %%
az.plot_trace(idata1)

# %%
# #?az.summary

# %%
az.summary(idata1, kind="stats")

# %%
az.plot_trace(idata1, kind="rank_bars", combined=True)

# %%
az.plot_posterior(idata1)

# %% [markdown]
# ## More data

# %%
np.random.seed(123)
n = 20
# Unknown value.
theta_real = 0.35

# Generate some observational data.
data2 = stats.bernoulli.rvs(p=theta_real, size=n)
data2

# %%
with pm.Model() as model2:
    # Prior.
    theta = pm.Beta("theta", alpha=1.0, beta=1.0)
    # Likelihood.
    y = pm.Bernoulli("y", p=theta, observed=data2)
    # (Numerical) Inference to estimate the posterior distribution through samples.
    idata2 = pm.sample(1000, random_seed=123)

# %%
az.summary(idata2, kind="stats")

# %%
az.plot_posterior(idata2)

# %% [markdown]
# ## Even more data

# %%
np.random.seed(123)
n = 100
# Unknown value.
theta_real = 0.35

# Generate some observational data.
data3 = stats.bernoulli.rvs(p=theta_real, size=n)
data3

# %%
with pm.Model() as model3:
    # Prior.
    theta = pm.Beta("theta", alpha=1.0, beta=1.0)
    # Likelihood.
    y = pm.Bernoulli("y", p=theta, observed=data3)
    # (Numerical) Inference to estimate the posterior distribution through samples.
    idata3 = pm.sample(1000, random_seed=123)

# %%
az.summary(idata3, kind="stats")

# %%
az.plot_posterior(idata3)

# %% [markdown]
# ## Savage-Dickey ratio

# %%
for idata in [idata1, idata2, idata3]:
    az.plot_bf(
        idata,
        var_name="theta",
        prior=np.random.uniform(0, 1, 10000),
        ref_val=0.5,
    )
    plt.xlim(0, 1)

# %% [markdown]
# ## ROPE

# %%
for idata in [idata1, idata2, idata3]:
    az.plot_posterior(idata, rope=[0.45, 0.55], ref_val=0.5)
    plt.xlim(0, 1)
