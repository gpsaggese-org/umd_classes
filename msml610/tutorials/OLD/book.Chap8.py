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
# !sudo /bin/bash -c "(source /venv/bin/activate; pip install --quiet jupyterlab-vim)"
# !jupyter labextension enable

# %%
# %load_ext autoreload
# %autoreload 2


import arviz as az
import pandas as pd
import pymc as pm
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt

# %%


# %%
def exp_quad_kernel(x, knots, l=1):
    """
    Exponentiated quadratic kernel.
    """
    return np.array([np.exp(-((x - k) ** 2) / (2 * l**2)) for k in knots])


# %%
data = np.array([-1, 0, 1, 2])  # np.random.normal(size=4)
cov = exp_quad_kernel(data, data, 1)

print(cov)

# %%
np.random.seed(24)
test_points = np.linspace(0, 10, 200)
fig, ax = plt.subplots(
    2, 2, figsize=(12, 6), sharex=True, sharey=True, constrained_layout=True
)
ax = np.ravel(ax)
num_examples = 3

for idx, l in enumerate((0.2, 1, 2, 10)):
    cov = exp_quad_kernel(test_points, test_points, l)
    y = stats.multivariate_normal.rvs(cov=cov, size=num_examples).T
    ax[idx].plot(test_points, y)
    ax[idx].set_title(f"l ={l}")
fig.text(0.51, -0.03, "x", fontsize=16)
fig.text(-0.03, 0.5, "f(x)", fontsize=16)

# %% [markdown]
# ## Gaussian process regression

# %%
np.random.seed(42)
# Plot the true distribution.
true_x = np.linspace(0, 10, 200)
plt.plot(true_x, np.sin(true_x), "k--")

# Sample points with noise.
x = np.random.uniform(0, 10, size=15)
y = np.random.normal(np.sin(x), 0.1)
plt.plot(x, y, "o")

plt.xlabel("x")
plt.ylabel("f(x)", rotation=0)

# %%
# A one dimensional column vector of inputs.
X = x[:, None]

with pm.Model() as model_reg:
    # Hyperprior for lengthscale kernel parameter
    l = pm.Gamma("l", 2, 0.5)
    # Instantiate a covariance function.
    cov = pm.gp.cov.ExpQuad(1, ls=l)
    # Instantiate a GP prior.
    gp = pm.gp.Marginal(cov_func=cov)
    # Prior on noise.
    eps = pm.HalfNormal("eps", 25)
    # Likelihood
    y_pred = gp.marginal_likelihood("y_pred", X=X, y=y, sigma=eps)
    trace_reg = pm.sample(2000)

# %%
az.plot_trace(trace_reg)

# %%
# Generate 100 evenly spaced values between floor(min(x)) and ceil(max(x)).
# Reshape the result into a column vector for prediction input.
X_new = np.linspace(np.floor(x.min()), np.ceil(x.max()), 100)[:, None]

with model_reg:
    # If 'f_pred' already exists in the model, delete it to avoid duplication.
    if "f_pred" in model_reg:
        del model_reg.named_vars["f_pred"]
    # Create a new GP conditional distribution for predictions at X_new.
    f_pred = gp.conditional("f_pred", X_new)

# %%
with model_reg:
    # Select the first 80 draws from the posterior trace for faster prediction.
    short_trace = trace_reg.sel(draw=slice(0, 80))
    # Sample from the posterior predictive distribution using the shortened trace.
    pred_samples = pm.sample_posterior_predictive(
        short_trace, var_names=["f_pred"]
    )

# %%
_, ax = plt.subplots(figsize=(12, 5))
# TODO(gp): We should flatten.
values = pred_samples["posterior_predictive"]["f_pred"][2]
ax.plot(X_new, values.T, "C1-", alpha=0.3)
ax.plot(X, y, "ko")
ax.set_xlabel("X")

# %%
_, ax = plt.subplots(figsize=(12, 5))
# Plot the distribution of Gaussian process predictions over new input points.
pm.gp.util.plot_gp_dist(ax, values, X_new, plot_samples=False)
# Plot the original training data as black dots for reference.
ax.plot(X, y, "ko")
ax.set_xlabel("x")
ax.set_ylabel("f(x)", rotation=0, labelpad=15)

# %%
trace_reg["posterior"]["l"]

# %%
# plot the results
_, ax = plt.subplots(figsize=(12, 5))

# predict
with model_reg:
    point = {
        "l": trace_reg["posterior"]["l"].mean(),
        "eps": trace_reg["posterior"]["eps"].mean(),
    }
    mu, var = gp.predict(X_new, point=point, diag=True)
    sd = var**0.5

# plot mean and 1σ and 2σ intervals
ax.plot(X_new, mu, "C1")
ax.fill_between(X_new.flatten(), mu - sd, mu + sd, color="C1", alpha=0.3)

ax.fill_between(X_new.flatten(), mu - 2 * sd, mu + 2 * sd, color="C1", alpha=0.3)

ax.plot(X, y, "ko")
ax.set_xlabel("X")

# %% [markdown]
# ## Classification

# %%
dir_name = "/app/code/book.2018.Martin.Bayesian_Analysis_with_Python.2e"
iris = pd.read_csv(dir_name + "/data2/iris.csv")
iris.head()

# %%
# Filter the DataFrame to include only 'setosa' and 'versicolor' species.
df = iris.query("species == ('setosa', 'versicolor')")

# Convert species labels to categorical integer codes (e.g., 0 and 1).
y = pd.Categorical(df["species"]).codes

# Extract sepal length values as a 1D NumPy array.
x_1 = df["sepal_length"].values

# Reshape the 1D array to a 2D column vector for modeling input.
X_1 = x_1[:, None]

# %%
with pm.Model() as model_iris:
    # Define a Gamma prior for the lengthscale parameter in the covariance function.
    l = pm.Gamma("l", 2, 0.5)
    # Create an exponential quadratic (RBF) covariance function with the lengthscale.
    cov = pm.gp.cov.ExpQuad(1, l)
    # Define a latent Gaussian process using the specified covariance function.
    gp = pm.gp.Latent(cov_func=cov)
    # Place a GP prior over the latent function values at the input locations X_1.
    f = gp.prior("f", X=X_1)
    # Define a Bernoulli likelihood with a logistic link function over latent f.
    y_ = pm.Bernoulli("y", p=pm.math.sigmoid(f), observed=y)
    # Sample from the posterior using 1 chain and 1000 samples without convergence checks.
    trace_iris = pm.sample(1000, chains=1, compute_convergence_checks=False)
