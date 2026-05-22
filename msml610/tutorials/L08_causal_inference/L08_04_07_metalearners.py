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

from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

try:
    from IPython.display import display
except ImportError:
    display = print  # type: ignore


# %%
import helpers.hdbg as hdbg
import helpers.hnotebook as hnotebo

import helpers.htutorial as ut
import L08_04_07_metalearners_utils as mtl

ut.config_notebook()

# Initialize logger.
logging.basicConfig(level=logging.INFO)
_LOG = logging.getLogger(__name__)
hnotebo.set_logger_to_print(_LOG)
hnotebo.set_all_loggers_to_print()

# %%
import warnings

import helpers.hmodule as hmodule
from lightgbm import LGBMRegressor

warnings.filterwarnings("ignore", category=UserWarning, module="lightgbm")
warnings.filterwarnings(
    "ignore",
    message="X does not have valid feature names",
    category=UserWarning,
)
logging.getLogger("lightgbm").setLevel(logging.ERROR)

hmodule.install_module_if_not_present(
    ["lightgbm", "fklearn"],
    use_activate=True,
    use_sudo=False,
    venv_path="/opt/venv",
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
np.random.seed(123)

m0 = LGBMRegressor()
m1 = LGBMRegressor()

m0.fit(train.query(f"{T}==0")[X].values, train.query(f"{T}==0")[y].values)
m1.fit(train.query(f"{T}==1")[X].values, train.query(f"{T}==1")[y].values);

# %%
m0

# %%
t_learner_cate_test = test.assign(
    cate=m1.predict(test[X].values) - m0.predict(test[X].values)
)

# %%
_ = mtl.plot_gain_curve_analysis(t_learner_cate_test, T, y, title="T-Learner")

# %%
# Generate synthetic data with treatment heterogeneity.
df = mtl.generate_synthetic_treatment_data(n0=500, n1=50, seed=123)

# Fit separate outcome models for control and treatment groups.
m0, m1, m0_hat, m1_hat = mtl.fit_tlearner_models(df, min_child_samples=25)

# Visualize outcome models and heterogeneous treatment effects.
mtl.plot_tlearner_treatment_effect_analysis(df, m0, m1, m0_hat, m1_hat)

# %% [markdown]
# # X-Learner

# %%
# Calculate heterogeneous treatment effects.
# np.random.seed(1)

tau_0, tau_1 = mtl.calculate_xlearner_heterogeneous_treatment_effects(df, m0, m1)

# Fit X-Learner models.

mu_tau0, mu_tau1, mu_tau0_hat, mu_tau1_hat = mtl.fit_xlearner_models(
    df, tau_0, tau_1, min_child_samples=25
)
# Plot heterogeneous treatment effect estimates.
mtl.plot_xlearner_effect_estimates(df, tau_0, tau_1, mu_tau0_hat, mu_tau1_hat)

# %%
# Plot X-Learner CATE with propensity score weighting.
mtl.plot_xlearner_with_propensity_scores(df, mu_tau0, mu_tau1, tau_0, tau_1)

# %%
# Fit propensity score model and first-stage outcome models with inverse
# probability weighting.
ps_model, m0, m1 = mtl.fit_propensity_score_and_weighted_outcome_models(
    train, X, T, y
)

# %%
# Fit second-stage models on residual treatment effects.
m_tau_0, m_tau_1 = mtl.fit_xlearner_second_stage_models(train, X, T, y, m0, m1)

# %%
# Estimate the CATE using propensity-score-weighted X-Learner effects.
x_cate_test = mtl.estimate_xlearner_cate(test, X, ps_model, m_tau_0, m_tau_1)

# %%
_ = mtl.plot_gain_curve_analysis(x_cate_test, T, y, title="X-Learner")

# %% [markdown]
# # S-Learner

# %%
data_cont = pd.read_csv(f"{dir_name}/discount_data.csv")
print(data_cont.shape[0])
data_cont.head()

# %%
train = data_cont.query("day<'2018-01-01'")
print(train.shape[0])
test = data_cont.query("day>='2018-01-01'")
print(test.shape[0])

# %%
X = ["month", "weekday", "is_holiday", "competitors_price"]
T = "discounts"
y = "sales"

s_learner = mtl.fit_slearner_model(train, X, T, y)

# %%
test_cf = mtl.generate_slearner_counterfactual_predictions(
    test, X, T, y, s_learner, np.array([0, 10, 20, 30, 40])
)

test_cf.head(8)

# %%
days = ["2018-12-25", "2018-01-01", "2018-06-01", "2018-06-18"]

plt.figure(figsize=(10, 4))
sns.lineplot(
    data=test_cf.query("day.isin(@days)").query("rest_id==2"),
    y="sales_hat",
    x="discounts",
    style="day",
);

# %%
test_s_learner_pred = mtl.estimate_slearner_cate(test_cf, test, T, y)

test_s_learner_pred.head()

# %%
_ = mtl.plot_gain_curve_analysis(test_s_learner_pred, T, y, title="S-Learner")

# %% [markdown]
# # Double ML / R-Learner

# %%
X = ["month", "weekday", "is_holiday", "competitors_price"]
T = "discounts"
y = "sales"

# Fit debiasing and denoising models.
debias_m, denoise_m = mtl.fit_rlearner_models(train, X, T, y)

# %%
# Fit R-Learner CATE model.
cate_model, t_res, y_res = mtl.fit_rlearner_cate_model(
    train, X, T, y, debias_m, denoise_m
)

# %%
# Check coefficients via OLS regression (optional diagnostic).
import statsmodels.api as sm

sm.OLS(y_res, t_res).fit().summary().tables[1]

# %%
# Estimate CATE on test set.
test_r_learner_pred = mtl.estimate_rlearner_cate(test, X, cate_model)

# %%
# Plot gain curve analysis for R-Learner.
_ = mtl.plot_gain_curve_analysis(test_r_learner_pred, T, y, title="R-Learner")
