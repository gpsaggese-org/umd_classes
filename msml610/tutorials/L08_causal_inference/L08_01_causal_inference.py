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

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

# Set plotting style.
sns.set_style("whitegrid")
plt.rcParams["figure.figsize"] = (12, 6)

# %%
import helpers.hmatplotlib as hmatplo
import helpers.hmodule as hmodule
import helpers.hpandas_display as hpandisp

import msml610.tutorials.msml610_utils as ut
import L08_01_causal_inference_utils as mtl0cireout

ut.config_notebook()

# Initialize logger.
logging.basicConfig(level=logging.INFO)
_LOG = logging.getLogger(__name__)

# %%
hmodule.install_module_if_not_present(
  "dataframe_image",
  use_activate=True,
)

# %% [markdown]
# # Cell 1: Sales example

# %%
dir_name = "L08_data"
# #!ls $dir_name

out_dir_name = "figures/"

markdown_path_prefix="msml610/lectures_source"
# # cp msml610/lectures_source/figures/L08*.png msml610/lectures_source/figures

# %%
data = mtl0cireout.load_xmas_sales_data(dir_name)
print(data.shape)
data.head(6)

# %%
xmas_sales_df_png = os.path.join(out_dir_name, 'L08.4.xmas_sales_df.png')
hpandisp.convert_df_to_png(
    data.head(6),
    xmas_sales_df_png,
    index=True,
    print_markdown=True,
    markdown_path_prefix=markdown_path_prefix
)

# %% [markdown]
# - **Purpose**: Compare sales outcomes between stores with and without price cuts
# - **What it shows**: Box plots of weekly sales amounts for treated (cut prices) and control (no price cut) groups
# - **Key insight**: Visual evidence suggesting price cuts increase sales, but this may reflect confounding rather than true causal effect

# %%
fig = mtl0cireout.plot_xmas_sales_boxplot(data)
xmas_boxplot_png = os.path.join(out_dir_name, "L08.4.xmas_boxplot.png")
hmatplo.save_fig(
    fig,
    xmas_boxplot_png,
    print_markdown=True,
    path_prefix=markdown_path_prefix
)

# %% [markdown]
# ## Cell 2: Conceptual Example

# %%
# # i = unit identifier
# # y0, y1 = potential outcomes under control and treatment (idealized situation)
# # t = treatment indicator
# # x = group
# df1 = pd.DataFrame(
#     dict(
#         i=[1, 2, 3, 4, 5, 6],
#         y0=[200, 120, 300, 450, 600, 600],
#         y1=[220, 140, 400, 500, 600, 800],
#         t=[0, 0, 0, 1, 1, 1],
#         x=[0, 0, 1, 0, 0, 1],
#     )
# )
# df1

# %%
# # Select the outcome based on the treatment.
# df1["y"] = (df1["t"] * df1["y1"] + (1 - df1["t"]) * df1["y0"]).astype(int)

# # Treatment effect.
# df1["te"] = df1["y1"] - df1["y0"]

# df1

# %%
# df2 = pd.DataFrame(
#     dict(
#         i=[1, 2, 3, 4, 5, 6],
#         y0=[
#             200,
#             120,
#             300,
#             np.nan,
#             np.nan,
#             np.nan,
#         ],
#         y1=[np.nan, np.nan, np.nan, 500, 600, 800],
#         t=[0, 0, 0, 1, 1, 1],
#         x=[0, 0, 1, 0, 0, 1],
#     )
# )
# df2

# %%
# # Select the outcome based on the treatment.
# df2["y"] = (df2["t"] * df2["y1"] + (1 - df2["t"]) * df2["y0"]).astype(int)

# # Treatment effect.
# df2["te"] = df2["y1"] - df2["y0"]

# df2

# %% [markdown]
# ## Cell 3: Visual Analysis of Bias in Sales Example

# %% [markdown]
# - **Purpose**: Visualize scatter points and regression lines for treated and control stores
# - **What it shows**: Treated stores (red) and control stores (blue) with their respective regression trends
# - **Key insight**: Within each group, the relationship between baseline sales and treatment appears similar, but overall pooled relationship is different

# %%
fig = mtl0cireout.plot_sales_bias_analysis(data)
bias_analysis0_png = os.path.join(out_dir_name, "L08.4.Association_Causation_Bias0.png")
hmatplo.save_fig(
    fig,
    bias_analysis0_png,
    print_markdown=True,
    path_prefix=markdown_path_prefix
)

# %% [markdown]
# - **Purpose**: Compare pooled vs. stratified regression models with synthetic data
# - **What it shows**: Left panel shows single trend line across all data; right panel shows separate trend lines for large and small businesses
# - **Key insight**: Simpson's paradox emerges when aggregation obscures group-level trends; stratification reveals the true relationships

# %%
fig = mtl0cireout.plot_single_vs_separate_trends()
bias_analysis1_png = os.path.join(out_dir_name, "L08.4.Association_Causation_Bias1.png")
hmatplo.save_fig(
    fig,
    bias_analysis1_png,
    print_markdown=True,
    path_prefix=markdown_path_prefix
)

# %% [markdown]
# ## Cell 4: Simpson's Paradox
#
# - **Purpose**: Illustrate Simpson's paradox where aggregate and group-level trends contradict
# - **What it shows**: Two groups (blue and red) with positive within-group trends, but negative overall trend
# - **Key insight**: Ignoring confounding variables (like business size) leads to contradictory causal conclusions

# %%
fig = mtl0cireout.plot_simpsons_paradox()
simpsons_paradox_png = os.path.join(out_dir_name, "L08.4.Simpson_Paradox.png")
hmatplo.save_fig(
    fig,
    simpsons_paradox_png,
    print_markdown=True,
    path_prefix=markdown_path_prefix
)

# %% [markdown]
# ## Cell 5: University Simpson's Paradox
#
# - **Purpose**: Demonstrate Simpson's paradox in university admissions context with two different groups
# - **What it shows**: Left panel shows two groups (A and B) each with positive admission trends; right panel shows aggregated data with reversed negative overall trend
# - **Key insight**: Simpson's paradox reveals how ignoring group differences (e.g., selectivity, baseline rates) leads to reversed causal conclusions in aggregate data

# %%
fig = mtl0cireout.plot_university_simpsons_paradox()

# %% [markdown]
# # Cell 2: A/B testing

# %%
data = pd.read_csv("L08_data/cross_sell_email.csv")
print(data.shape)
display(data.head(3))

# %%
data.groupby(["cross_sell_email"]).mean()

# %%
# Evaluate balance co-variate.
X = ["gender", "age"]
mu = data.groupby("cross_sell_email")[X].mean()
var = data.groupby("cross_sell_email")[X].var()
norm_diff = ((mu - mu.loc["no_email"])/
    np.sqrt((var + var.loc["no_email"])/2))
norm_diff

# %% [markdown]
# ## School scores

# %%
df = pd.read_csv("L08_data/enem_scores.csv")
print(df.shape)
df.head(3)

# %%
df.sort_values(by="avg_score", ascending=False).head(5)

# %%
threshold_score = np.quantile(df["avg_score"], 0.99)
threshold_students = np.quantile(df["number_of_students"], 0.98)
plot_data = df[["avg_score", "number_of_students"]].copy()
plot_data["top_school"] = plot_data["avg_score"] >= threshold_score
# Remove outliers.
plot_data = plot_data[plot_data["number_of_students"] < threshold_students][
    ["top_school", "number_of_students"]
]

plt.figure(figsize=(8,4))
ax = sns.boxplot(x="top_school", y="number_of_students", data=plot_data)

plt.title("Number of Students of 1% Top Schools (Right)")

# %%
q_99 = np.quantile(df["avg_score"], 0.99)
q_01 = np.quantile(df["avg_score"], 0.01)
plot_data = df.sample(10000).copy()
is_extreme = (plot_data["avg_score"] > q_99) | (plot_data["avg_score"] < q_01)
plot_data["Group"] = np.where(is_extreme, "Top and Bottom", "Middle")
plt.figure(figsize=(10,5))
sns.scatterplot(y="avg_score", x="number_of_students", data=plot_data.query("Group=='Middle'"), label="Middle")
ax = sns.scatterplot(y="avg_score", x="number_of_students", data=plot_data.query("Group!='Middle'"), color="0.7", label="Top and Bottom")

plt.title("School Score by Number of Students in the School")

bias_analysis0_png = os.path.join(out_dir_name, "L08.4.School_score_by_number_students.png")
hmatplo.save_fig(
    fig,
    bias_analysis0_png,
    print_markdown=True,
    path_prefix=markdown_path_prefix
)

# %%
## Standard Error of Estimate

# %%
data = pd.read_csv("./L08_data/cross_sell_email.csv")

short_email = data.query("cross_sell_email=='short'")["conversion"]
long_email = data.query("cross_sell_email=='long'")["conversion"]
email = data.query("cross_sell_email!='no_email'")["conversion"]
no_email = data.query("cross_sell_email=='no_email'")["conversion"]

data.groupby("cross_sell_email").size()


# %%
# This is equivalent to long_email.sem()
def se(y: pd.Series):
    return y.std() / np.sqrt(len(y))

print("SE for Long Email:", se(long_email))
print("SE for Short Email:", se(short_email))

# %%
## Confidence Intervals

# %% [markdown]
# - In the frequentist view, the data is generated by a process, which is governed by true (unknown) parameters
#   - Assume the conversion rate is a Bernoulli distribution with an unknown parameter
#
# - You can run 10,000 experiments each with 100 customers
#   - You collect the data and you get a mean close to the "true" mean
#   - The std dev of the mean is a measure of the uncertainty
#
# - Even if the Bernoulli can only be 0 or 1, the average of the data is asymptotically normally distributed

# %%
n = 100
conv_rate = 0.08

def run_experiment():
    return np.random.binomial(1, conv_rate, size=n)

np.random.seed(42)

experiments = [run_experiment().mean() for _ in range(10000)]

plt.figure(figsize=(10,4))
freq, bins, img = plt.hist(experiments, bins=20, label="Experiment Means", color="0.6")
plt.vlines(conv_rate, ymin=0, ymax=freq.max(), linestyles="dashed", label="True Mean", color="0.3")
plt.legend();

# %% [markdown]
# - With the SEM you can create an interval that contains the true mean 95% of the experiments
# - In real life, you often have a single experiment, but you can construct a confidence interval

# %%
# Using 1.96 std dev to capture 95% of the density.
exp_se = short_email.sem()
exp_mu = short_email.mean()
ci = (exp_mu - 1.96 * exp_se, exp_mu + 1.96 * exp_se)
print("95% CI for Short Email: ", ci)

# %%
from scipy import stats

# 99%
conf = 0.95
#conf = 0.99
z = np.abs(stats.norm.ppf((1-conf)/2))
print(z)
ci = (exp_mu - z * exp_se, exp_mu + z * exp_se)
ci


# %%
def ci(y: pd.Series):
    return (y.mean() - 2 * y.sem(), y.mean() + 2 * y.sem())

print("95% CI for Short Email:", ci(short_email))
print("95% CI for Long Email:", ci(long_email))
print("95% CI for No Email:", ci(no_email))

# %%
plt.figure(figsize=(10,4))
linestyle=['-', '--', ':', '-.']

x = np.linspace(-0.05, .25, 100)
short_dist = stats.norm.pdf(x, short_email.mean(), short_email.sem())
plt.plot(x, short_dist, lw=2, label="Short", linestyle=linestyle[0])
plt.fill_between(x.clip(ci(short_email)[0], ci(short_email)[1]), 0, short_dist, alpha=0.2, color="0.0")

long_dist = stats.norm.pdf(x, long_email.mean(), long_email.sem())
plt.plot(x, long_dist, lw=2, label="Long", linestyle=linestyle[1])
plt.fill_between(x.clip(ci(long_email)[0], ci(long_email)[1]), 0, long_dist, alpha=0.2, color="0.4")

no_email_dist = stats.norm.pdf(x, no_email.mean(), no_email.sem())
plt.plot(x, no_email_dist, lw=2, label="No email", linestyle=linestyle[2])
plt.fill_between(x.clip(ci(no_email)[0], ci(no_email)[1]), 0, no_email_dist, alpha=0.2, color="0.8")

plt.xlabel("Conversion")
plt.legend();

# %% [markdown]
# ## Hypothesis testing
#
# - Assume that H_0 is that conv(no_email) = conv(short_email)

# %%
diff_mu = short_email.mean() - no_email.mean()
diff_se = np.sqrt(no_email.sem()**2 + short_email.sem()**2)

ci = (diff_mu - 1.96*diff_se, diff_mu + 1.96*diff_se)
print(f"95% CI for the differece (short email - no email):\n{ci}")

# %% [markdown]
# - 0 is not included in the CI interval so H_0 can be rejected at 95% confidence

# %%
- Test if the "lift" between sending short email and no email is more than 1%

# %%
# Shifting the CI.
diff_mu_shifted =  short_email.mean() - no_email.mean() - 0.01
diff_se = np.sqrt(no_email.sem()**2 + short_email.sem()**2)

ci = (diff_mu_shifted - 1.96*diff_se, diff_mu_shifted + 1.96*diff_se)
print(f"95% CI 1% difference between (short email - no email):\n{ci}")

# %% [markdown]
# ## Test statistic
#
# - Typically a higher value means rejecting the null hypothesis
# - E.g., t-stat

# %%
t_stat = (diff_mu - 0) / diff_se
t_stat

# %% [markdown]
# ## P-value
#
# - Measure how likely is to see an extreme value under the null hypothesis, i.e., $P(data | H_0)$

# %%
print("p-value:", (1 - stats.norm.cdf(t_stat))*2)

# %% [markdown]
# ## Power
#
# - When designing an experiment, you might need to decide the sample size to reject the null hypothesis

# %%
# Graphical Causal Models
