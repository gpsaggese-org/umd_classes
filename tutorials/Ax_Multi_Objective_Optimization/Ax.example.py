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
#     display_name: msml610-project
#     language: python
#     name: python3
# ---

# %% [markdown]
# # 1. Ax - Multi-Objective Optimization for Marketing Campaigns

# %% [markdown]
# ## 1. Introduction to Bayesian Optimization
#
# ### 1.1. Optimization Problem
#
# We have an optimization problem:
#
# $\min_{x} f(x)$
#
# Where $f(x)$ is the objective function to minimize.
#
# Gradient method -> $x_{t+1} = x_t - \alpha \nabla f(x_t)$
#
# **Requires a differentiable objective function!**
#
# ### 1.2. Black-Box Optimization
#
# In a black-box optimization problem, we don't have a differentiable objective function. The relation between input and output is unknown.
#
# This relation is modeled as an unknown function $f(x)$ that predicts the outcome.
#
# **Surrogate model:** $y = f(x) + \epsilon$
#
# How do we obtain the surrogate model?
#
# #### 1.2.1. Surrogate Model
#
# ![Surrogate Model](images/surrogate-model.png)
#
# Given hyperparameters $x$, we want obtain a function $f(x)$ that predicts the outcome of the objective function.
#
# We have a set of points $x_1, x_2, ..., x_n$ and the corresponding outcomes $y_1, y_2, ..., y_n$.
#
# #### 1.2.2. Gaussian Process (GP)
#
# Define $f(x) \sim GP(m(x), k(x, x'))$ where:
#
# - $m(x)$ is the mean function
# - $k(x, x')$ is the covariance function
#
# Most common kernel: RBF kernel $k(x, x') = \sigma^2 \exp(-\frac{||x - x'||^2}{2l^2})$
#
# - Gaussian kernel
# - Smoothness
#
# In other words:
# - Mean defined at each point $x_i$
# - Uncertainty defined at each point $x_i$
# - Covariance allows interpolation of unknown $f(x_i)$, with some uncertainty
#
# ### 1.3. Bayesian Optimization
#
# Bayesian optimization is a sequential optimization technique that uses a probabilistic model to guide the search for the optimal solution. In order to do this, first, an Acquisition Function has to be defined.
#
# #### 1.3.1. Acquisition Function
#
# The acquisition function is the function used to define the next point to evaluate.
#
# Note: $f^* = \max_i y_i$ -> Best observed outcome
#
# Different types of acquisition functions are:
#
# **Expected Improvement (EI):** $EI(x)=E[\max(f(x)−f^*, 0)]$
#
# **Probability of Improvement (PI):** $PI(x)=P(f(x) \geq f^*)$
#
# **Upper Confidence Bound (UCB):** $UCB(x) = \mu(x) + \kappa \sigma(x)$
#
# Expected Improvement is the acquisition function used by Ax.
#
# ![Acquisition Function](images/acquisition-function.png)
#
# #### 1.3.2. Sequential Optimization
#
# Bayesian optimization leads to a sequential optimization process where the Acquisition Function is applied to define the next point to evaluate. After the evaluation, the result is fed back to the model to adjust the Surrogate Model.
#
# ![Sequential Exploration](images/sequential-exploration.gif)

# %% [markdown]
#
# ## 2. Real-Time Bidding Algorithms with Bayesian Optimization
#
# ### 2.1. Real-Time Bidding (RTB)
#
# Real-Time Bidding (RTB) is a programmatic advertising technique where advertisers bid on ad inventory in real-time. The advertiser pays only when the ad is clicked.
#
# There are four actors in the RTB process:
# - Publisher: The website or app that sells the ad inventory.
# - Advertiser: The advertiser that wants to display their ad.
# - Ad Exchange: Works on the Publisher side. It's the platform that starts the auction when a space is available, receives the bids from the DSP and decides which ad will be published.
# - DSP (Demand Side Platform): Works on the Advertiser side. It receives the auction request from the Ad Exchange and makes a bid to show the ad.
#
# The Ad Exchange shares the Auction with multiple DSPs. Each DSP, which represents an advertiser, makes a bid. The highest bid wins the auction and the ad is published.
#
# **Note:** The bid done by the DSP is not the final price of the Impression. A common practice is the use the second highest bid as the price of the Impression. This is called the "Second Price Auction".
#
# ![RTB Process](images/rtb-process.png)
#
# A different but more simple diagram:
#
# ![RTB Process](images/rtb-process-2.png)
#
# ### 2.2. Acronyms
#
# - DSP: Demand Side Platform. Works on the Advertiser side. It's what we're going to optimize.
# - RTB: Real-Time Bidding. The process of bidding for an impression in real-time.
# - CTR: Click-Through Rate. The probability of a user clicking on an ad.
# - CVR: Conversion Rate. The probability of a user converting (Buying) given that they clicked on the ad.
# - CPC: Cost Per Click. The cost of a click.
# - CPM: Cost Per Mile Impressions. The cost of 1000 impressions.
# - eCPC: effective Cost Per Click (The value paid for the impression is usually not the bid price, but the second highest bid)
# - pCTR: predicted Click-Through Rate. The probability of a user clicking on an ad, predicted by a machine learning model.
#
# ### 2.3. Bidding Strategy
#
# A DSP is running a campaign for an advertiser. It receives an auction and has to make a bid. A bidding strategy is used to determine the bid amount. The DSP wants to maximize the revenue while minimizing the cost for the advertiser. The revenue can be measured in Impressions, Clicks, or Conversions, depending on the campaign objective.
#
# ![Bidding Strategy](images/bidding-strategy.png)
#
# The steps in the bidding strategy are:
# - Learn from existing data, this includes information about the publisher, users, cookies, the content to advertise, etc.
# - Receive an auction request from the Ad Exchange.
# - Predict a potential CTR
# - Define a formula to calculate the bid amount. If it's to high, we may be spending the advertiser's budget without getting good results. If it's to low, we may be losing the auction.
#
# **Important:** Given that we had predicted the CTR, we want to calculate the bid amount to an optimal value. This is what we're trying to achieve.
#
# Classic algorithms to define the bid amount are:
# - **Constant bidding (Const):** Bid a constant value for all the bid requests
# - **Random bidding (Rand):** Randomly choose a bid value in a given range.
# - **Bidding below max eCPC (Mcpc):** The goal of bid optimisation is to reduce the eCPC (Effective Cost Per Click). The Mcpc is what the advertiser is willing to pay for the impression at most. The bid price on an impression is obtained by multiplying the Mcpc and the pCTR.
# - **Linear-form bidding of pCTR (Lin):** Bid a linear function of the predicted CTR. The bid amount increases with a higher predicted CTR.
#
# Lin has demonstrated to be one of the best and simplest bidding strategies.
#
# #### 2.3.1. Linear-form bidding of pCTR (Lin)
#
# The basic formula is:
#
# $bid = base\_bid + \frac{pCTR}{avg\_CTR}$
#
# - $base\_bid$: A constant value for all the bid requests. The average bid value of the campaign.
# - $pCTR$: The predicted Click-Through Rate.
# - $avg\_CTR$: The average Click-Through Rate of the campaign, or the advertiser.
#
# The rationale within this formula is that a campaign naturally has an average probability of a click (Average CTR). Some bids, based on the data provided by the publisher, may have a higher probability of a click. On those we want to bid higher.
#
# The coefficient $ctr\_reg\_coef$ is used to regulate how much the predicted CTR is going to affect the final bid price. This is a hyperparameter that can be tuned to optimize the campaign. It's between 0.5 and 2.
#
# In order to improve this bidding algorithm, we'll introduce more concepts.
#
# ##### 2.3.1.1. Base Bid
#
# $base\_bid$ represents how much the DSP (Or the advertiser) is willing to pay per thousand impressions of average quality.
#
# ##### 2.3.1.2. Pay to Bid Ratio
#
# As explained in the previous section, the bid price is not the final price of the impression. The final price is the second highest bid. This means we can always aim a little bit higher to win the auction as it's not the price we're going to pay.
#
# To take advantage of this, we introduce the concept of "Pay to Bid Ratio". Which means, how much more we can bid in order to win the auction assuming we're not going to pay the full price.
#
# Complex machine learning models can be used to predict how much other DSPs could be bidding for the same impression. In this case we'll just keep a simple ratio.
#
# $pay\_to\_bid\_ratio = \frac{raw\_bid}{pay\_bid}$
#
# If the pay price is much lower than the raw bid, the ratio will be higher. This ratio is always greater than 1. This means we can increase the bid price to win the auction.
#
# In this case we'll keep an average of the historic ratio.
#
# $pay\_to\_bid\_ratio$ is clipped between 0.5 and 2.
#
# The coefficient $pay\_to\_bid\_reg\_coef$ is used to regulate how much the pay to bid ratio is going to affect the final bid price. This is a hyperparameter that can be tuned to optimize the campaign. It's also limited between 0.5 and 2.
#
# $final\_bid = raw\_bid \times (1 + pay\_to\_bid\_reg\_coef \times (pay\_to\_bid\_ratio - 1))$
#
# $raw\_bid$ is the bid amount obtained from the basic "Lin" formula.
#
# ##### 2.3.1.3. Pacing
#
# The advertiser usually sets a budget for the campaign. The DSP needs to ensure that the bid amount is within the budget and calculate how much is left. This introduces the concept of "pay_price", which is the price paid for an impression, not the price of the bid.
#
# If the `base_bid` is too high, the budget could be consumed early in the day, while the majority of the conversions happen at night. To correct this, the DSP can use "pacing". The pacing is a coefficient calculated over the time of the day based on the expected budget to be spent.
#
# $pacing\_coefficient$: A coefficient between 0.5 and 2 that is calculated over the time of the day based on the expected budget to be spent.
#
# $pacing\_coefficient = \frac{expected\_budget\_to\_be\_spent}{actual\_budget\_spent}$
#
# With $expected\_budget\_to\_be\_spent = \frac{budget}{24} \times hour\_of\_day$
#
# This means, we try to fraction the budget for each hour of the day.
#
# $pacing\_coefficient$ is clipped between 0.5 and 2.
#
# $final\_bid = raw\_bid \times pacing\_coefficient$
#
# The coefficient $pacing\_reg\_coef$ is used to regulate how much the pacing is going to affect the final bid price. This is a hyperparameter that can be tuned to optimize the campaign. It's also limited between 0.5 and 2.
#
# ##### 2.3.1.4. Final Bid Formula
#
# The final bid formula without the regulation coefficients is:
#
# $final\_bid = base\_bid \times \frac{pCTR}{avg\_CTR} \times pay\_to\_bid\_ratio \times pacing\_coefficient$
#
# With the regulation coefficients:
#
# $final\_bid = base\_bid \times \left(1 + ctr\_reg\_coef \times \left(\frac{pCTR}{avg\_CTR} - 1\right)\right) \times \left(1 + pay\_to\_bid\_reg\_coef \times (pay\_to\_bid\_ratio - 1)\right) \times \left(1 + pacing\_reg\_coef \times (pacing\_coefficient - 1)\right)$
#
# - Hyperparameters:
#   - $base\_bid$: How much the DSP (Or the advertiser) is willing to pay per thousand impressions of average quality
#   - $ctr\_reg\_coef$: A coefficient to regulate the importance of the predicted CTR. (0.5 to 2)
#   - $pay\_to\_bid\_reg\_coef$: A coefficient to regulate the importance of the pay to bid ratio. (0.5 to 2)
#   - $pacing\_reg\_coef$: A coefficient to regulate the importance of the pacing. (0.5 to 2)
#   - $budget$: The budget set by the advertiser.
# - Calculated values:
#   - $pCTR$: The predicted Click-Through Rate.
#   - $avg\_CTR$: The average Click-Through Rate of the campaign, or the advertiser.
#   - $pay\_to\_bid\_ratio$: The ratio of the pay price to the raw bid.
#   - $pacing\_coefficient$: The coefficient to regulate the pacing.

# %% [markdown]
# ### 2.4. DSP Simulation
#
# ### 2.4.1. iPinYou Dataset
#
# This simulation is based on the iPinYou dataset, described in these publications:
#
# - iPinYou Global RTB Bidding Algorithm Competition Dataset (Hairen Liao, Lingxiao Peng, Zhenchuan Liu, Xuehua Shen)
# - Real-Time Bidding Benchmarking with iPinYou Dataset (Weinan Zhang, Shuai Yuan, Jun Wang)
#
# For more information:
# - [iPinYou Global RTB Bidding Algorithm Competition](https://contest.ipinyou.com/)
# - [Github - wnzhang/make-ipinyou-data](https://github.com/wnzhang/make-ipinyou-data)
# - [Github - wnzhang/optimal-rtb](https://github.com/wnzhang/optimal-rtb)
#
# iPinYou is a DSP (Demand Side Platform) for RTB (Real-Time Bidding) in China that published in 2014 a complete dataset of individual bids, impressions and clicks for a certain group of advertisers during a week.
#
# iPinYou opened this dataset for a competition to create the best bidding algorithm. A bidding algorithm is a function that, based on some information given by the Ad Exchange, decides whether to bid for an impression and the bid amount.
#
# The analysis and processing of the dataset is done in the Jupyter Notebook [dsp_pctr_prediction_model.ipynb](dsp_pctr_prediction_model.ipynb).
#
# **Important:** The bid and paid price are measured in CNY (Chinese Yuan) per 1000 impressions.
#
# ### 2.4.2. Prediction Model
#
# A requirement for the simulation is to predict the Click-Through Rate (CTR) of an impression. This is a classic machine learning problem. A model using XGBoost has been created to predict the CTR based on the auction request provided by the Ad Exchange.
#
# The model training and evaluation is done in the Jupyter Notebook [dsp_pctr_prediction_model.ipynb](dsp_pctr_prediction_model.ipynb).
#
# The dataset has been updated to include the predicted CTR. This new feature will be used by the DSP to calculate the bid amount. The dataset is available in the [dataset](dataset) folder.
#
# ### 2.4.3. Dataset
#
# The iPinYou dataset has been reduced to a smaller dataset files (From 4GB to 300MB) to only contain the features that are used to predict the CTR, plus other features required for the simulation:
#
# - Paid price
# - Clicked or not
# - Floor price
#
# Original iPinYou dataset contains:
#
# - Bid logs: Every auction request from the Ad Exchange, with some data about the ad, the amount bidded by the DSP.
# - Impression logs: Every won bid generates an impression, this adds the paid price data.
# - Click logs: Some impressions generate a click, this is logged here.
#
# The new dataset is reduced to a file per day. The dataset contains all this information for **one** advertiser and from June 6th 2013 to June 12th 2013.
#
# The dataset is available in the [dataset](dataset) folder.

# %% [markdown]
# ### 2.4.4 Simulation for 06/10/2013 with fixed hyperparameters
#
# The simulation will run for a given date (E.g. 06/10/2013). It will start processing the dataset which contains one line per bid. Then, for each bid:
# - Predict the CTR using the prediction model.
# - Calculate the bid amount using the bidding strategy.
# - Verify if the bid was won, based on the paid price and the floor price.
#
# The base_bid, budget and coefficients are fixed for the simulation.

# %% [markdown]
# **Initialize environment**

# %%
# %reload_ext autoreload
# %load_ext autoreload
# %autoreload 2
# %matplotlib inline

# %%
# Install AX with the extension for Jupyter notebooks
# ! pip3 install "ax-platform[notebook]" joblib --break-system-packages

# %%
import numpy as np
from ax.api.client import Client
from ax.api.configs import RangeParameterConfig
import matplotlib.pyplot as plt
import pandas as pd
from IPython.display import display
from Ax_utils import (
    AB_Testing,
    UCB1,
    ThompsonSampling,
    GP_Bandit,
    SimulationExperiment,
    dsp_simulation,
    get_avg_spent_per_day,
)

# %% [markdown]
# **Download dataset**
#
# *If the files are not available in the dataset folder, download them*

# %%
# Download dataset
# ! wget -P dataset/ https://storage.googleapis.com/msml610-assets/bid_with_features_and_pctr_20130607.csv
# ! wget -P dataset/ https://storage.googleapis.com/msml610-assets/bid_with_features_and_pctr_20130608.csv
# ! wget -P dataset/ https://storage.googleapis.com/msml610-assets/bid_with_features_and_pctr_20130609.csv
# ! wget -P dataset/ https://storage.googleapis.com/msml610-assets/bid_with_features_and_pctr_20130610.csv
# ! wget -P dataset/ https://storage.googleapis.com/msml610-assets/bid_with_features_and_pctr_20130611.csv
# ! wget -P dataset/ https://storage.googleapis.com/msml610-assets/bid_with_features_and_pctr_20130612.csv

# %% [markdown]
# **Restrict the budget**
#
# The machine learning model created in "dsp_pctr_prediction_model.ipynb" also extracts some information about the dataset. Part of this information is how much has been spent by the DSP in the real scenario.
#
# The number of bids we can simulate is limited by the number of bids in the dataset. For this reason, we'll restrict the daily budget to a percentage of budget spent in the real scenario.
#
# If we don't restrict the budget, we could run into an escenario where ads budget is left but we don't have more information to simulate the bidding.
#
# **dsp_simulation**
#
# The *dsp_simulation* is available in the [Ax_utils.py](Ax_utils.py) file.
#
# The function receives the date, and the hyperparameters. Then, as it goes through the bid requests it predicts the CTR (Using the created XGBoost model), calculates the bid amount, considering the pay to bid ratio, and pacing. Then, it compares the calculated bid with the price that was really paid in the dataset. If it's a win, it considers the dataset paid price for the budget, not the bid, as the second highest bid is the one used for the payment.

# %% [markdown]
# **Simulation #1**
#
# - Base bid: 50
# - Date: 2013/06/10

# %%
avg_spent_per_day = get_avg_spent_per_day("20130610")
# The budget has to be much lower than the budget spent per day, otherwise we'll run out of bids in the simulation without exhausting the budget and we cannot keep trying.
budget = avg_spent_per_day * 0.2

total_bids, total_bids_done, total_bids_won, total_budget_spent, total_clicks = (
    dsp_simulation("20130610", 50, budget, 0.0, 0.0, 0.0)
)

# %%
print(f"Total budget: {budget}")
print(f"Total bids: {total_bids}")
print(f"Total bids done: {total_bids_done}")
print(f"Total bids won: {total_bids_won}")
print(f"Total budget spent: {total_budget_spent}")
print(f"Total clicks: {total_clicks}")

# %% [markdown]
# Now I'll run a simulation where I pay more per click. The budget will be consumed faster, but we have better chances of winning bids.
#
# **Simulation #2**
#
# - Base bid: 100
# - Date: 2013/06/10
#

# %%
total_bids, total_bids_done, total_bids_won, total_budget_spent, total_clicks = (
    dsp_simulation("20130610", 100, budget, 0.0, 0.0, 0.0)
)
print(f"Total budget: {budget}")
print(f"Total bids: {total_bids}")
print(f"Total bids done: {total_bids_done}")
print(f"Total bids won: {total_bids_won}")
print(f"Total budget spent: {total_budget_spent}")
print(f"Total clicks: {total_clicks}")

# %% [markdown]
# The number of total bids won is lower because the budget was consumed faster.
#
# Keep increasing the amount to pay per click.
#
# **Simulation #3**
#
# - Base bid: 400
# - Date: 2013/06/10

# %%
total_bids, total_bids_done, total_bids_won, total_budget_spent, total_clicks = (
    dsp_simulation("20130610", 400, budget, 0.0, 0.0, 0.0)
)
print(f"Total budget: {budget}")
print(f"Total bids: {total_bids}")
print(f"Total bids done: {total_bids_done}")
print(f"Total bids won: {total_bids_won}")
print(f"Total budget spent: {total_budget_spent}")
print(f"Total clicks: {total_clicks}")

# %% [markdown]
# The number of bids won and clicks went down. We consumed the budget much faster.
#
# Let's try some enabling the CTR coefficient, which should make this more efficient (It makes use of the predicted CTR)
#
# **Simulation #4**
#
# - Base bid: 400
# - Date: 2013/06/10
# - CTR coefficient: 1.0

# %%
total_bids, total_bids_done, total_bids_won, total_budget_spent, total_clicks = (
    dsp_simulation("20130610", 400, budget, 1.0, 0.0, 0.0)
)
print(f"Total budget: {budget}")
print(f"Total bids: {total_bids}")
print(f"Total bids done: {total_bids_done}")
print(f"Total bids won: {total_bids_won}")
print(f"Total budget spent: {total_budget_spent}")
print(f"Total clicks: {total_clicks}")

# %% [markdown]
# Great, the number of bids won and clicks went up. It means the CTR prediction is helping.
#
# I'll try to increase bid to pay ratio coefficient, this may help to win some bids even when the paid price won't increase.
#
# **Simulation #5**
# - Base bid: 400
# - Date: 2013/06/10
# - CTR coefficient: 1.0
# - Bid to pay ratio coefficient: 1.0

# %%
total_bids, total_bids_done, total_bids_won, total_budget_spent, total_clicks = (
    dsp_simulation("20130610", 400, budget, 1.0, 1.0, 0.0)
)
print(f"Total budget: {budget}")
print(f"Total bids: {total_bids}")
print(f"Total bids done: {total_bids_done}")
print(f"Total bids won: {total_bids_won}")
print(f"Total budget spent: {total_budget_spent}")
print(f"Total clicks: {total_clicks}")

# %% [markdown]
# It didn't help. The budget was consumed faster.
#
# Now, what happens if I increase the bid to pay ratio coefficient when the bid base was much lower (50 vs 400)
#
# **Simulation #6**
# - Base bid: 50
# - Date: 2013/06/10
# - CTR coefficient: 1.0
# - Bid to pay ratio coefficient: 1.0

# %%
total_bids, total_bids_done, total_bids_won, total_budget_spent, total_clicks = (
    dsp_simulation("20130610", 50, budget, 1.0, 1.0, 0.0)
)
print(f"Total budget: {budget}")
print(f"Total bids: {total_bids}")
print(f"Total bids done: {total_bids_done}")
print(f"Total bids won: {total_bids_won}")
print(f"Total budget spent: {total_budget_spent}")
print(f"Total clicks: {total_clicks}")

# %% [markdown]
# Here, with a lower bid base, the bid to pay ratio helped. We can see the relationship is not linear, and they aren't independent.
#
# Now we'll try increasing the pacing coefficient, without the pay to bid ratio.
#
# **Simulation #7**
# - Base bid: 50
# - Date: 2013/06/10
# - CTR coefficient: 1.0
# - Pacing coefficient: 1.0

# %%
total_bids, total_bids_done, total_bids_won, total_budget_spent, total_clicks = (
    dsp_simulation("20130610", 50, budget, 1.0, 0.0, 1.0)
)
print(f"Total budget: {budget}")
print(f"Total bids: {total_bids}")
print(f"Total bids done: {total_bids_done}")
print(f"Total bids won: {total_bids_won}")
print(f"Total budget spent: {total_budget_spent}")
print(f"Total clicks: {total_clicks}")

# %% [markdown]
# Here the pacing was incredibly helpful. We got the best results among all the simulations. It was totally unexpected.

# %% [markdown]
# #### 2.4.4.1 Analysis
#
# The results for different hyperparameters are very different. Each parameter affects how the other parameters perform. This couldn't be analyzed with a simple linear regression.
#
# Now, in a real experiment we can't do this, we cannot go back in time to see how different parameters perform. We need to do adaptive experiments. For Adaptive Experimentation, we can use Bayesian Optimization.

# %% [markdown]
# ### 2.4.5. Bayesian Optimization
#
# **Experiment Simulation**
#
# In this section we're not going to simulate using the same dataset again and again. We're going to simulate the experiment as if it was real. We cannot go back in time to see how different parameters perform.
#
# The simulation will be run for a given date (E.g. 06/07/2013). Then, it will run for a new set of hyperparameters the next day, and so on.
#
# **Note:** We only have data for 6 days of testing. A Trial is set to last 1 day. Running a simulation period of less than 1 day won't work properly as  we want to maximize the number of clicks, and the number of clicks in one day is already too low. To test a better simulation we do a rolling use of the dataset, starting again from the first day.
#
# The simulation will run for a given date (E.g. 06/10/2013). It will start processing the dataset which contains one line per bid request. Then, for each bid request:
# - Predict the CTR using the prediction model.
# - Calculate the bid amount using the bidding strategy.
# - Verify if the bid was won, based on the paid price and the floor price.
# - Update the budget based on the paid price.
# - If it was clicked, update the CTR and average CTR.
#
# **About the model predictions:**
# - The pCTR can only be predicted with the information from the previous days.
# - If the current simulation day is 06/10/2013, the model `2013-06-06_2013-06-09` will be loaded
#
# #### 2.4.5.1 Maximize the number of clicks
#
# In this case the budget is fixed to `6019776.0` and the goal is to maximize the number of clicks.

# %%
budget = 6019776.0

client = Client()

parameters = [
    RangeParameterConfig(
        name="base_bid", parameter_type="float", bounds=(20, 100)
    ),
    RangeParameterConfig(
        name="bid_to_pay_ratio", parameter_type="float", bounds=(0, 1)
    ),
    RangeParameterConfig(
        name="ctr_coefficient", parameter_type="float", bounds=(0, 1)
    ),
    RangeParameterConfig(
        name="pacing_coefficient", parameter_type="float", bounds=(0, 1)
    ),
]

client.configure_experiment(parameters=parameters)
client.configure_optimization(objective="clicks")

# The experiment runs over 18 days. The dataset only contains 6 days of data, so we roll the dataset.
for date in [
    "20130607",
    "20130608",
    "20130609",
    "20130610",
    "20130611",
    "20130612",
    "20130607",
    "20130608",
    "20130609",
    "20130610",
    "20130611",
    "20130612",
    "20130607",
    "20130608",
    "20130609",
    "20130610",
    "20130611",
    "20130612",
]:
    trials = client.get_next_trials(max_trials=1)
    trial_index = list(trials.keys())[0]
    parameters = trials[trial_index]

    # These are the optimized parameters
    base_bid = parameters["base_bid"]
    bid_to_pay_ratio = parameters["bid_to_pay_ratio"]
    ctr_coefficient = parameters["ctr_coefficient"]
    pacing_coefficient = parameters["pacing_coefficient"]

    print(
        f"Simulating date: {date} with base_bid: {base_bid}, bid_to_pay_ratio: {bid_to_pay_ratio}, ctr_coefficient: {ctr_coefficient}, pacing_coefficient: {pacing_coefficient}"
    )
    (
        total_bids,
        total_bids_done,
        total_bids_won,
        total_budget_spent,
        total_clicks,
    ) = dsp_simulation(
        date,
        base_bid,
        budget,
        bid_to_pay_ratio,
        ctr_coefficient,
        pacing_coefficient,
    )
    print(
        f"Total clicks: {total_clicks}, impressions: {total_bids_won}, budget spent: {total_budget_spent}"
    )

    client.complete_trial(
        trial_index=trial_index,
        raw_data={
            "clicks": total_clicks,
            "impressions": total_bids_won,
            "budget_spent": total_budget_spent,
        },
    )

# %%
best_parameters, prediction, index, name = client.get_best_parameterization()
print("Best Parameters:", best_parameters)
print("Prediction (mean, variance):", prediction)

# %% [markdown]
# Surprisingly, the best result was obtained when the base bid was lower and bid to pay ratio was leveraged.
#
# In the **manual search** for the best hyperparameters we reached a maximum of **103 clicks**. Using **Bayesian Optimization**, we reached an experimental result of **126 clicks**.
#

# %%
from ax.analysis.plotly.surface.slice import SlicePlot

analysis = SlicePlot("base_bid")

analysis.compute(
    experiment=client._experiment,
    generation_strategy=client._generation_strategy,
    adapter=None,
)

# %% [markdown]
# This plot shows that, for lower base bids, the number of clicks has a lot of uncertainty, because it's very dependent on the other parameters.

# %%
from ax.analysis.plotly.arm_effects import ArmEffectsPlot

analysis = ArmEffectsPlot()

analysis.compute(
    experiment=client._experiment,
    generation_strategy=client._generation_strategy,
    adapter=None,
)

# %% [markdown]
# #### 2.4.5.2 Maximize the number of impressions
#
# Assuming we want to maximize the number of impressions. The number of impressions is much higher, so we can use shorter time periods for the trials.
#
# I'll run experiments of 10K bids each.

# %%
# In this case we make the budget 10x lower as the trials are for 100K bids, much smaller. The budget is not per day now.
budget = 601977.6
trial_size = 100000

client = Client()

parameters = [
    RangeParameterConfig(
        name="base_bid", parameter_type="float", bounds=(20, 500)
    ),
    RangeParameterConfig(
        name="bid_to_pay_ratio", parameter_type="float", bounds=(0, 1)
    ),
    RangeParameterConfig(
        name="ctr_coefficient", parameter_type="float", bounds=(0, 1)
    ),
    RangeParameterConfig(
        name="pacing_coefficient", parameter_type="float", bounds=(0, 1)
    ),
]

client.configure_experiment(parameters=parameters)
client.configure_optimization(objective="impressions")

for date in [
    "20130607",
    "20130608",
    "20130609",
    "20130610",
    "20130611",
    "20130612",
]:
    offset = 0
    while True:
        trials = client.get_next_trials(max_trials=1)
        trial_index = list(trials.keys())[0]
        parameters = trials[trial_index]

        base_bid = parameters["base_bid"]
        bid_to_pay_ratio = parameters["bid_to_pay_ratio"]
        ctr_coefficient = parameters["ctr_coefficient"]
        pacing_coefficient = parameters["pacing_coefficient"]

        print(
            f"Simulating date: {date}, offset: {offset} with base_bid: {base_bid}, bid_to_pay_ratio: {bid_to_pay_ratio}, ctr_coefficient: {ctr_coefficient}, pacing_coefficient: {pacing_coefficient}"
        )
        (
            total_bids,
            total_bids_done,
            total_bids_won,
            total_budget_spent,
            total_clicks,
        ) = dsp_simulation(
            date,
            base_bid,
            budget,
            bid_to_pay_ratio,
            ctr_coefficient,
            pacing_coefficient,
            offset=offset,
            limit=trial_size,
        )
        offset += trial_size
        if total_bids <= 0:
            break
        print(
            f"Total clicks: {total_clicks}, impressions: {total_bids_won}, budget spent: {total_budget_spent}"
        )

        client.complete_trial(
            trial_index=trial_index,
            raw_data={
                "clicks": total_clicks,
                "impressions": total_bids_won,
                "budget_spent": total_budget_spent,
            },
        )

# %% [markdown]
# Here we're trying to maximize the number of impressions with a much more limited budget.
#
# If the bid is too low, we risk losing the auction. If it's too high, the budget will be consumed faster in expensive bids.
#
# **Note:** To maximize the impressions we should have use a different formula, predicting the CTR will take us to bet on potentially better impressions, but not to increase the number of impressions.

# %%
best_parameters, prediction, index, name = client.get_best_parameterization()
print("Best Parameters:", best_parameters)
print("Prediction (mean, variance):", prediction)

# %%
from ax.analysis.plotly.arm_effects import ArmEffectsPlot

analysis = ArmEffectsPlot()

analysis.compute(
    experiment=client._experiment,
    generation_strategy=client._generation_strategy,
    adapter=None,
)

# %%
from ax.analysis.plotly.surface.slice import SlicePlot

analysis = SlicePlot("base_bid")

analysis.compute(
    experiment=client._experiment,
    generation_strategy=client._generation_strategy,
    adapter=None,
)

# %% [markdown]
# We can see how the number of impressions went up when it started to try lower base bids, opposite to what I expected.
#
# It can also be seen that other coefficients are low, because they don't provide an advantage to maximize the number of impressions.

# %% [markdown]
# ### 2.4.6. Multi-Objective Optimization
#
# #### 2.4.6.1. Maximize the number of clicks while minimizing the budget spent
#
# All the previous experiments run with a fixed budget. What happens if we want to decide the budget and see how the budget increase would generate a growth in clicks (Or not).
#
# Running multi-objective optimization requires much more trials, as we have two dimensions to explore. For this reason, and given that we only have 6 days of data, we'll do a rolling experiment and start again from the first day. The experiment will run for 30 days.

# %%
# Now the budget should be set to a number that doesn't limit the bids. We still have to provide one.
budget = 100000000000.0
# In this case the pacing_coefficient should be 0 because the budget is already too large.

client = Client()

parameters = [
    RangeParameterConfig(
        name="base_bid", parameter_type="float", bounds=(1, 100)
    ),  # The minimum bid is lowered too to allow budget reduction
    RangeParameterConfig(
        name="bid_to_pay_ratio", parameter_type="float", bounds=(0, 1)
    ),
    RangeParameterConfig(
        name="ctr_coefficient", parameter_type="float", bounds=(0, 1)
    ),
    RangeParameterConfig(
        name="pacing_coefficient", parameter_type="float", bounds=(0, 1)
    ),
]

client.configure_experiment(parameters=parameters)
client.configure_optimization(
    objective="-budget_spent, clicks",
    outcome_constraints=["budget_spent <= 6009888.0", "clicks >= 1"],
)

for date in [
    "20130607",
    "20130608",
    "20130609",
    "20130610",
    "20130611",
    "20130612",
    "20130607",
    "20130608",
    "20130609",
    "20130610",
    "20130611",
    "20130612",
    "20130607",
    "20130608",
    "20130609",
    "20130610",
    "20130611",
    "20130612",
    "20130607",
    "20130608",
    "20130609",
    "20130610",
    "20130611",
    "20130612",
    "20130607",
    "20130608",
    "20130609",
    "20130610",
    "20130611",
    "20130612",
]:
    trials = client.get_next_trials(max_trials=1)
    trial_index = list(trials.keys())[0]
    parameters = trials[trial_index]

    base_bid = parameters["base_bid"]
    bid_to_pay_ratio = parameters["bid_to_pay_ratio"]
    ctr_coefficient = parameters["ctr_coefficient"]

    print(
        f"Simulating date: {date} with base_bid: {base_bid}, bid_to_pay_ratio: {bid_to_pay_ratio}, ctr_coefficient: {ctr_coefficient}"
    )
    (
        total_bids,
        total_bids_done,
        total_bids_won,
        total_budget_spent,
        total_clicks,
    ) = dsp_simulation(
        date, base_bid, budget, bid_to_pay_ratio, ctr_coefficient, 0
    )
    print(
        f"Total clicks: {total_clicks}, impressions: {total_bids_won}, budget spent: {total_budget_spent}"
    )

    client.complete_trial(
        trial_index=trial_index,
        raw_data={
            "clicks": total_clicks,
            "impressions": total_bids_won,
            "budget_spent": total_budget_spent,
        },
    )

# %%
frontier = client.get_pareto_frontier()

data = []
for parameters, metrics, trial_index, arm_name in frontier:
    data.append(
        {
            "budget_spent": metrics["budget_spent"][0],
            "clicks": metrics["clicks"][0],
            "trial_index": trial_index,
            "base_bid": parameters["base_bid"],
            "bid_to_pay_ratio": parameters["bid_to_pay_ratio"],
            "ctr_coefficient": parameters["ctr_coefficient"],
        }
    )

df_pareto = pd.DataFrame(data)
df_pareto = df_pareto[df_pareto["budget_spent"] > 0]

display(df_pareto.sort_values(by="budget_spent", ascending=True))

# %%
plt.figure(figsize=(8, 6))
plt.scatter(
    df_pareto["budget_spent"],
    df_pareto["clicks"],
    c="blue",
    edgecolor="k",
    alpha=0.7,
)
plt.xlabel("budget_spent")
plt.ylabel("clicks")
plt.title("Pareto Frontier: budget_spent vs clicks")
plt.grid(True)
plt.show()

# %% [markdown]
# Here we can see only a few set of hyperparameters were found in the Pareto Frontier.
#
# The limitation with the optimization of clicks is that the number of clicks is usually low, so to get a good number of them we need to run each trial for a long time.

# %% [markdown]
# #### 2.4.6.2 Maximize the number of impressions while minimizing the budget spent
#
# This time, minimizing the budget spent and maximizing the number of impressions.

# %%
# Now the budget should be set to a number that doesn't limit the bids. We still have to provide one.
budget = 100000000000.0
trial_size = 100000
# In this case the pacing_coefficient should be 0 because the budget is already too large.
# Learning from the previous experiment, we don't care about the predicted CTR, so the coefficient is set to 0.

client = Client()

parameters = [
    RangeParameterConfig(
        name="base_bid", parameter_type="float", bounds=(1, 100)
    ),
    RangeParameterConfig(
        name="bid_to_pay_ratio", parameter_type="float", bounds=(0, 1)
    ),
]

client.configure_experiment(parameters=parameters)
client.configure_optimization(
    objective="-budget_spent, impressions",
    outcome_constraints=["budget_spent <= 6009888.0", "impressions >= 1"],
)

for date in [
    "20130607",
    "20130608",
    "20130609",
    "20130610",
    "20130611",
    "20130612",
]:
    offset = 0
    while True:
        trials = client.get_next_trials(max_trials=1)
        trial_index = list(trials.keys())[0]
        parameters = trials[trial_index]

        base_bid = parameters["base_bid"]
        bid_to_pay_ratio = parameters["bid_to_pay_ratio"]

        print(
            f"Simulating date: {date}, offset: {offset} with base_bid: {base_bid}, bid_to_pay_ratio: {bid_to_pay_ratio}"
        )
        (
            total_bids,
            total_bids_done,
            total_bids_won,
            total_budget_spent,
            total_clicks,
        ) = dsp_simulation(
            date,
            base_bid,
            budget,
            bid_to_pay_ratio,
            0,
            0,
            offset=offset,
            limit=trial_size,
        )
        offset += trial_size
        if total_bids <= 0:
            break
        print(
            f"Total clicks: {total_clicks}, impressions: {total_bids_won}, budget spent: {total_budget_spent}"
        )

        client.complete_trial(
            trial_index=trial_index,
            raw_data={
                "clicks": total_clicks,
                "impressions": total_bids_won,
                "budget_spent": total_budget_spent,
            },
        )

# %%
frontier = client.get_pareto_frontier()

data = []
for parameters, metrics, trial_index, arm_name in frontier:
    data.append(
        {
            "budget_spent": metrics["budget_spent"][0],
            "impressions": metrics["impressions"][0],
            "trial_index": trial_index,
            "base_bid": parameters["base_bid"],
            "bid_to_pay_ratio": parameters["bid_to_pay_ratio"],
        }
    )

df_pareto = pd.DataFrame(data)
df_pareto = df_pareto[df_pareto["budget_spent"] > 0]

display(df_pareto.sort_values(by="budget_spent", ascending=True))

# %%
plt.figure(figsize=(8, 6))
plt.scatter(
    df_pareto["budget_spent"],
    df_pareto["impressions"],
    c="blue",
    edgecolor="k",
    alpha=0.7,
)
plt.xlabel("budget_spent")
plt.ylabel("impressions")
plt.title("Pareto Frontier: budget_spent vs clicks")
plt.grid(True)
plt.show()

# %% [markdown]
# For impressions the optimization algorithm was able to find more optimal results. This is because the higher number of impressions gives more information to the Bayesian Optimization about the relationship between input and outcomes.

# %% [markdown]
# # 3. Bayesian Optimization on Multi-Armed Bandits
#
# A Multi-Armed Bandit is a problem where there are multiple arms (actions) to choose from. A/B Testing is a special case of them.
#
# ## 3.1. A/B Testing
#
# In A/B Testing, we have a set of arms $A_1, A_2, ..., A_n$ and we want to find the best arm.
#
# The arms are the different versions of the product or feature that we want to test. The outcome is the success of the arm.
#
# The goal is to find the best arm to maximize the success.
#
# The problem is that we don't know the success of the arms before running the test.
#
# In A/B Testing the criteria to present an arm to the user is randomized to eliminate potential confounders, similar to an RCT.
#
# ![A/B Testing](images/ab-testing.png)
#
# ## 3.2. Policy Exploration Problem
#
# Through exploration, we want to find the best policy to maximize the outcome. The policy is defined by a "scoring function".
#
# This means, we have a set of features about the user and the content, then a prediction model will return a series of predictions from those features (E.g.: click probability, share probability, etc). We want to define how those predictions will be weighted to select the arm to maximize the outcome. Examples of this are:
# - Facebook feed: Decide which content to show to the user.
# - LinkedIn search results: Who should appear first in the search results.
# - Netflix recommendations: Which movies to recommend to the user.
#
# We define the features corresponding to the User (Who is receiving the content) and the ones corresponding to the Content (What is being shown to the user) as $u$ and $c$.
#
# A Prediction Model generates $d$ predictions $f_i(u, c)$ (E.g.: click probability, share probability, etc.) based on the user and content.
#
# We have to weigh in those predictions to calculate the score $s(u, c) = \sum_{i=1}^d x_i f_i(u, c)$. The score will decide which content is shown to the user.
#
# The policy is the definition of $x_i$ which are the weights assigned to each prediction.
#
# ## 3.3. Sequential Optimization
#
# A/B Testing models can be used to optimize the policy. This is what the Meta Adaptive Experimentation Team currently does.
#
# Bayesian Optimization can be used to test different policies in a sequential manner.
#
# ![sequential-optimization](images/sequential-optimization.png)
#
# Bayesian Optimization does exploration and exploitation, this means, it will try to use the policies that are returning the best results but also try new policies to explore the input space.
#
# ## 3.4. Literature
#
# The following literature shows how Bayesian Optimization techniques have been applied by top companies to optimize their advertising algorithms.
#
# - **Google Vizier: A Service for Black-Box Optimization (2017)**: Google. Comparison of Bayesian Optimization vs Simulated Annealing. Initial definitions of Bayesian Optimization.
# - **Online Parameter Selection for Web-based Ranking Problems (2018)**: LinkedIn. Select the policy to score and rank search results.
# - **Constrained Bayesian Optimization with Noisy Experiments (2018)**: Meta. Improvements to Bayesian Optimization. Quasi-Monte Carlo sampling.
# - **Bayesian Optimization for Policy Search via Online-Offline Experimentation (2019)**: Meta. Mix online (Real users) and offline (Simulations) experiments. Use Multi-task Gaussian Process (MTGP) to combine the results and model the response surface.
# - **Experimenting, Fast and Slow: Bayesian Optimization of Long-term Outcomes with Online Experiments (2025)**: Combine short-run experiments (SRE) and long-run experiments (LRE) with MTGP and Target-Aware Gaussian Process Model (TAGP) to model the response surface. Use proxy metrics for short-run experiments.
#
# ## 3.5. Multi-Armed Bandit Problem
#
# ![Multi-Armed Bandit](images/multi-armed-bandit.png)
#
# We have $n$ Arms -> $A_1, A_2, ..., A_n$, and we need to find the best arm.
#
# Maximizing $Reward(A_i)$ requires testing, but the number of tests is limited.
#
# **Every time we didn't pull the best arm, we incur a regret.**
#
# **Regret:** The difference between the best arm and the arm we chose.
#
# In other words, how much we would have won if we used the best arm instead of the one we tried.
#
# ### 3.5.1. Traditional Exploration-Exploitation Algorithms
#
# To minimize the regret we need to exploit the arm with highest rewards, but we also need to explore to be sure we are not missing any arm that could give us better results.
#
# There are different techniques to balance exploration and exploitation.
#
# **Classic A/B Testing**
#
# All bandits are tried equally often. The policy doesn't adapt to the results. Regret increases linearly $O(T)$
#
# **UCB1 (Upper Confidence Bound)**
#
# On each iteration, the expected reward of each arm is calculated based on the mean reward and the number of times the arm has been pulled.
#
# If we have an arm $A_i$, at iteration $t$, then:
#
# $UCB(A_i) = \hat{\mu}_i + \kappa \sqrt{\frac{2 \log(t)}{N_i(t)}}$
#
# - $\kappa$ -> exploration vs exploitation trade-off
# - $\hat{\mu}_i$ -> the mean reward of arm $A_i$ (Frequentist estimator)
# - $N_i(t)$ -> the number of times arm $A_i$ has been pulled until time $t$
#
# Without uncertainty (The mean reward is stable) regret is $O(log T)$. This technique is a frequentist approach, and widely used in the field. It assumes there is a ground truth for the reward of each arm. (E.g., CTR is 0.1 for a given arm and we can estimate it)
#
# *Ref: Finite-time Analysis of the Multiarmed Bandit Problem (Peter Auer, 2002)*
#
# *Ref: Introduction to Multi-Armed Bandits (Aleksandrs Slivkins, 2019)*
#
# ### 3.5.2. Bayesian Algorithms
#
# Bayesian algorithms consider the uncertainty of the rewards. This means, there isn't a simple "ground truth", like a single expected CTR for an arm, but a distribution of possible CTRs.
#
# #### 3.5.2.1. Thompson Sampling
#
# This algorithm defines a prior that is updated on each iteration.
#
# **Prior:** $P(A_i) \sim Beta(\alpha_i, \beta_i)$ | $\alpha_i = 1, \beta_i = 1$
#
# **Arm Selection:** Evaluate the Beta distribution for each $A_i$, should return a value for $P(A_i)$. The arm with the highest value is selected.
#
# **Evaluation:** Evaluate A_i in a real experiment. If it's a simulation do $Bernoulli(P(A_i))$.
#
# **Posterior:** If $Bernoulli(P(A_i))$ is 1, update $\alpha_i = \alpha_i + 1$ else $\beta_i = \beta_i + 1$
#
# Regret is $O(log T)$. Thompson Sampling supports higher variance.
#
# **Note:** Thompson Sampling is a simplified version of the analytical solution for the Probabilistic Programming scenario of the coin toss problem. It's a Heuristic approach.
#
# *Ref: Analysis of Thompson Sampling for the Multi-armed Bandit Problem (Shipra Agrawal and Navin Goyal, 2012)*
#
# *Ref: A Tutorial on Thompson Sampling (Russo, 2018)*
#
# #### 3.5.2.2. Gaussian Process Bandit
#
# Gaussian Process Bandit is a Bayesian approach to the Multi-Armed Bandit problem. It uses a Gaussian Process to model the uncertainty of the rewards.
#
# *Reminder:* GP is defined by $f(x) \sim GP(m(x), k(x, x'))$ where:
# - $x$ represents the arm
# - $f(x)$ represents the reward of the arm, is maximized
# - Regret is minimized
#
# In the Multi-Armed Bandit problem, the input $x_i$ is the probability of choosing arm $A_i$.
#
# In a classic Multi-Armed Bandit with $n$ options, the Gaussian Process will be linear. One of the solutions is better and the maximum is on the border of the search space. The ideal function would be an hyperplane of the search space.
#
# Compared to Thompson Sampling, a GP Bandit supports the case where there is a non-linear relationship between the chosen arm and the reward.
#
# Example of Gaussian Process Bandit:
# - Arm 1 has a CTR of 0.1 and Arm 2 has a CTR of 0.2, they are unknown.
# - The bandit will explore both arms, with a probability for each one $P(A_1)$ and $P(A_2)$.
# - The function $f(P(A_1),P(A_2))$ is the reward based on the probability of choosing Arm 1 or Arm 2.
# - The function is linear, assuming each Arm has a constant CTR.
#
# *Ref: Weighted Gaussian Process Bandits for Non-stationary Environments (2021)*
#
# ### 3.5.3. Hypothesis
#
# We start with a Multi-Armed Bandit problem, and define a hypothesis. Then we'll run a simulation to test this hypothesis.
#
# **Scenario**
#
# - We have $n$ Arms $A_1, A_2, ..., A_n$
# - Each arm has an unknown reward $f(A_i)$ (E.g.: Click-through rate)
# - $T$: Total number of pulls (Number of times one of the arms is presented to the user)
# - Experiment: Variation of the frequency of the arms  $x_1, x_2, ..., x_n$ (Each arm has a probability of being chosen)
# - Exploitation: Pull the arm with the estimated best reward
# - Exploration: Pull the arm with the highest uncertainty
# - Regret: At the end of the experiment we can get the reward of the best arm, and calculate the regret if we have always pulled the best arm.
#
# **Hypothesis**
#
# - UCB1 is the best algorithm when each Arm has a constant reward.
# - Reward is linear in theory but not in practice due to variance (E.g.: CTR isn't really constant).
# - Thompson Sampling and GP-Bandit are more robust to non-linear relationships with high variance.
#
# **Note:** Records show that GP-Bandit achieves better results in practice but it's not guaranteed by the theoretical analysis.
#
# *Ref: Weighted Gaussian Process Bandits for Non-stationary Environments (2021)*
#
# *Ref: Gaussian Process Upper Confidence Bound Achieves Nearly-Optimal Regret in Noise-Free Gaussian Process Bandits (2025)*

# %% [markdown]
# ### 3.5.1 Simulation with minimal uncertainty
#
# We'll run and compare the performance of the following algorithms:
#
# - A/B Testing
# - UCB1
# - Thompson Sampling
# - GP Bandit
#
# The arms being tested are defined by a ground truth, constant CTR of 0.1, 0.2 and 0.3. The uncertainty is minimal, with a standard deviation of 0.01.
#
# Based on the hypothesis, UCB1 should perform better than A/B Testing and Bayesian Optimization methods (Thompson Sampling and GP Bandit).
#
# The code implemented for the simulation can be found in `Ax_utils.py`. The code is based on the `SimulationExperiment` abstract class with concrete implementations for each algorithm.
#
# The **GP Bandit** algorithm makes use of the Ax library.

# %%
print("Starting Simulation Experiment")
print("Initialize algorithms")
ab_testing = AB_Testing(n_arms=3)
ucb1 = UCB1(n_arms=3)
thompson_sampling = ThompsonSampling(n_arms=3)
gp_bandit = GP_Bandit(n_arms=3, batch_size=1000)

print("Setup AB Testing Experiment")
ab_testing_experiment = SimulationExperiment(
    ctr_means=[0.1, 0.2, 0.3], ctr_stds=[0.01, 0.01, 0.01], algorithm=ab_testing
)

print("Setup UCB1 Experiment")
ucb1_experiment = SimulationExperiment(
    ctr_means=[0.1, 0.2, 0.3], ctr_stds=[0.01, 0.01, 0.01], algorithm=ucb1
)

print("Setup Thompson Sampling Experiment")
thompson_sampling_experiment = SimulationExperiment(
    ctr_means=[0.1, 0.2, 0.3],
    ctr_stds=[0.01, 0.01, 0.01],
    algorithm=thompson_sampling,
)

print("Setup GP Bandit Experiment")
gp_bandit_experiment = SimulationExperiment(
    ctr_means=[0.1, 0.2, 0.3], ctr_stds=[0.01, 0.01, 0.01], algorithm=gp_bandit
)

# %%
(
    ab_testing_total_reward,
    ab_testing_total_trials,
    ab_testing_accum_rewards_per_trial,
    ab_testing_pulls_per_arm_per_trial,
    ab_testing_expected_rewards_per_arm,
    ab_testing_regret_per_trial,
) = ab_testing_experiment.run_experiment(n_trials=20000)
print(
    f"AB Testing - Reward: {ab_testing_total_reward}, Trials: {ab_testing_total_trials}"
)

# %%
(
    ucb1_total_reward,
    ucb1_total_trials,
    ucb1_accum_rewards_per_trial,
    ucb1_pulls_per_arm_per_trial,
    ucb1_expected_rewards_per_arm,
    ucb1_regret_per_trial,
) = ucb1_experiment.run_experiment(n_trials=20000)
print(f"UCB1 - Reward: {ucb1_total_reward}, Trials: {ucb1_total_trials}")

# %%
(
    thompson_sampling_total_reward,
    thompson_sampling_total_trials,
    thompson_sampling_accum_rewards_per_trial,
    thompson_sampling_pulls_per_arm_per_trial,
    thompson_sampling_expected_rewards_per_arm,
    thompson_sampling_regret_per_trial,
) = thompson_sampling_experiment.run_experiment(n_trials=20000)
print(
    f"Thompson Sampling - Reward: {thompson_sampling_total_reward}, Trials: {thompson_sampling_total_trials}"
)

# %%
(
    gp_bandit_total_reward,
    gp_bandit_total_trials,
    gp_bandit_accum_rewards_per_trial,
    gp_bandit_pulls_per_arm_per_trial,
    gp_bandit_expected_rewards_per_arm,
    gp_bandit_regret_per_trial,
) = gp_bandit_experiment.run_experiment(n_trials=20000)
print(
    f"GP Bandit - Reward: {gp_bandit_total_reward}, Trials: {gp_bandit_total_trials}"
)

# %% [markdown]
# #### 3.5.1.1 Compare Results
#
# We'll plot the results of the experiments.

# %%
# Plot accumulated clicks and regret side by side
fig, axes = plt.subplots(1, 2, figsize=(16, 5))

# Accumulated clicks
axes[0].plot(ab_testing_accum_rewards_per_trial, label="AB Testing")
axes[0].plot(ucb1_accum_rewards_per_trial, label="UCB1")
axes[0].plot(
    thompson_sampling_accum_rewards_per_trial, label="Thompson Sampling"
)
axes[0].plot(gp_bandit_accum_rewards_per_trial, label="GP Bandit")
axes[0].set_title("Accumulated Clicks")
axes[0].set_xlabel("Trial")
axes[0].set_ylabel("Accumulated clicks")
axes[0].legend()

# Accumulated regret
axes[1].plot(ab_testing_regret_per_trial, label="AB Testing")
axes[1].plot(ucb1_regret_per_trial, label="UCB1")
axes[1].plot(thompson_sampling_regret_per_trial, label="Thompson Sampling")
axes[1].plot(gp_bandit_regret_per_trial, label="GP Bandit")
axes[1].set_title("Accumulated Regret")
axes[1].set_xlabel("Trial")
axes[1].set_ylabel("Regret")
axes[1].legend()

plt.tight_layout()

# %% [markdown]
# Now we'll plot how each arm was pulled for each algorithm.

# %%
# Plot ab_testing_pulls_per_arm_per_trial
fig, axes = plt.subplots(2, 2, figsize=(16, 5))

# AB Testing
for i in range(3):
    axes[0][0].plot(
        ab_testing_pulls_per_arm_per_trial[:, i], label=f"Arm {i + 1}"
    )
axes[0][0].set_title("AB Testing - Arm pulls per trial")
axes[0][0].set_xlabel("Trial")
axes[0][0].set_ylabel("Accumulated Pulls")
axes[0][0].legend()

# UCB1
for i in range(3):
    axes[0][1].plot(ucb1_pulls_per_arm_per_trial[:, i], label=f"Arm {i + 1}")
axes[0][1].set_title("UCB1 - Arm pulls per trial")
axes[0][0].set_xlabel("Trial")
axes[0][0].set_ylabel("Accumulated Pulls")
axes[0][0].legend()

# Thompson Sampling
for i in range(3):
    axes[1][0].plot(
        thompson_sampling_pulls_per_arm_per_trial[:, i], label=f"Arm {i + 1}"
    )
axes[1][0].set_title("Thompson Sampling - Arm pulls per trial")
axes[0][0].set_xlabel("Trial")
axes[0][0].set_ylabel("Accumulated Pulls")
axes[0][0].legend()

# GP Bandit
for i in range(3):
    axes[1][1].plot(
        gp_bandit_pulls_per_arm_per_trial[:, i], label=f"Arm {i + 1}"
    )
axes[1][1].set_title("GP Bandit - Arm pulls per trial")
axes[0][0].set_xlabel("Trial")
axes[0][0].set_ylabel("Accumulated Pulls")
axes[0][0].legend()

plt.tight_layout()

# %% [markdown]
# #### 3.5.1.2 Analysis of the results
#
# Under a certain and constant CTR with minimal uncertainty, Bayes Optimization (GP Bandit) doesn't perform well. Statistically it learns which arm is the best, but it keeps exploring other arms.
#
# UCB1 performs better because it's more focused on exploitation, and assumes that the expected reward is constant, which is the case.
#
# Thompson Sampling surprisingly performs better than UCB1. My hypothesis was that it would have a similar performance or slightly worse, as it doesn't pick the best arm always, it just runs a probability to do it.

# %% [markdown]
# #### 3.5.2 Simulation with higher uncertainty
#
# Now we're going to simulate a different scenario. It tooks real CTRs from the Upworthy Research Archive dataset, where the CTRs are much more close.
#
# The Upworthy Research Archive dataset has been recorded by a viral news website which did A/B testing for news headlines and tried to identify which headlines had a higher click ratio. Here we took one of the articles as an example.
#
# - Headline 1: 0.049
# - Headline 2: 0.040
# - Headline 3: 0.035
#
# Now, the dataset only contains the final CTR, not the uncertainty. We'll assume the CTR is not constant, it has a variance, and the probability of the CTR for each headline may even overlap.
#
# Here we're assuming CTRs distributions are constant over time. In reality they are not, at a different time of the day some headlines could gain more attention as they audience changes.
#
# Std will be 0.01 for all headlines.
#

# %%
# Visualize CTR priors as normal distributions
ctr_means = [0.049, 0.040, 0.035]
ctr_stds = [0.01, 0.01, 0.01]
x = np.linspace(0.0, 0.1, 400)

plt.figure(figsize=(5, 3))
i = 0
for m, s in zip(ctr_means, ctr_stds):
    # Calculate the probability density function for the normal distribution
    pdf = (1 / (s * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - m) / s) ** 2)
    plt.plot(x, pdf, label=f"Arm {i}")
    i += 1

plt.title("CTR Normal Distributions")
plt.legend()
plt.tight_layout()

# %%
print("Starting Simulation Experiment")
print("Initialize algorithms")
ab_testing = AB_Testing(n_arms=3)
ucb1 = UCB1(n_arms=3)
thompson_sampling = ThompsonSampling(n_arms=3)
gp_bandit = GP_Bandit(n_arms=3, batch_size=1000)

print("Setup AB Testing Experiment")
ab_testing_experiment = SimulationExperiment(
    ctr_means=ctr_means, ctr_stds=ctr_stds, algorithm=ab_testing
)

print("Setup UCB1 Experiment")
ucb1_experiment = SimulationExperiment(
    ctr_means=ctr_means, ctr_stds=ctr_stds, algorithm=ucb1
)

print("Setup Thompson Sampling Experiment")
thompson_sampling_experiment = SimulationExperiment(
    ctr_means=ctr_means, ctr_stds=ctr_stds, algorithm=thompson_sampling
)

print("Setup GP Bandit Experiment")
gp_bandit_experiment = SimulationExperiment(
    ctr_means=ctr_means, ctr_stds=ctr_stds, algorithm=gp_bandit
)

# %%
(
    ab_testing_total_reward,
    ab_testing_total_trials,
    ab_testing_accum_rewards_per_trial,
    ab_testing_pulls_per_arm_per_trial,
    ab_testing_expected_rewards_per_arm,
    ab_testing_regret_per_trial,
) = ab_testing_experiment.run_experiment(n_trials=20000)
print(
    f"AB Testing - Reward: {ab_testing_total_reward}, Trials: {ab_testing_total_trials}"
)

# %%
(
    ucb1_total_reward,
    ucb1_total_trials,
    ucb1_accum_rewards_per_trial,
    ucb1_pulls_per_arm_per_trial,
    ucb1_expected_rewards_per_arm,
    ucb1_regret_per_trial,
) = ucb1_experiment.run_experiment(n_trials=20000)
print(f"UCB1 - Reward: {ucb1_total_reward}, Trials: {ucb1_total_trials}")

# %%
(
    thompson_sampling_total_reward,
    thompson_sampling_total_trials,
    thompson_sampling_accum_rewards_per_trial,
    thompson_sampling_pulls_per_arm_per_trial,
    thompson_sampling_expected_rewards_per_arm,
    thompson_sampling_regret_per_trial,
) = thompson_sampling_experiment.run_experiment(n_trials=20000)
print(
    f"Thompson Sampling - Reward: {thompson_sampling_total_reward}, Trials: {thompson_sampling_total_trials}"
)

# %%
(
    gp_bandit_total_reward,
    gp_bandit_total_trials,
    gp_bandit_accum_rewards_per_trial,
    gp_bandit_pulls_per_arm_per_trial,
    gp_bandit_expected_rewards_per_arm,
    gp_bandit_regret_per_trial,
) = gp_bandit_experiment.run_experiment(n_trials=20000)
print(
    f"GP Bandit - Reward: {gp_bandit_total_reward}, Trials: {gp_bandit_total_trials}"
)

# %% [markdown]
# #### 3.5.2.1 Compare Results
#
# We'll plot the results of the experiments.

# %%
# Plot accumulated clicks and regret side by side
fig, axes = plt.subplots(1, 2, figsize=(16, 5))

# Accumulated clicks
axes[0].plot(ab_testing_accum_rewards_per_trial, label="AB Testing")
axes[0].plot(ucb1_accum_rewards_per_trial, label="UCB1")
axes[0].plot(
    thompson_sampling_accum_rewards_per_trial, label="Thompson Sampling"
)
axes[0].plot(gp_bandit_accum_rewards_per_trial, label="GP Bandit")
axes[0].set_title("Accumulated Clicks")
axes[0].set_xlabel("Trial")
axes[0].set_ylabel("Accumulated clicks")
axes[0].legend()

# Accumulated regret
axes[1].plot(ab_testing_regret_per_trial, label="AB Testing")
axes[1].plot(ucb1_regret_per_trial, label="UCB1")
axes[1].plot(thompson_sampling_regret_per_trial, label="Thompson Sampling")
axes[1].plot(gp_bandit_regret_per_trial, label="GP Bandit")
axes[1].set_title("Accumulated Regret")
axes[1].set_xlabel("Trial")
axes[1].set_ylabel("Regret")
axes[1].legend()

plt.tight_layout()

# %% [markdown]
# Now we'll plot how each arm was pulled for each algorithm.

# %%
# Plot ab_testing_pulls_per_arm_per_trial
fig, axes = plt.subplots(2, 2, figsize=(16, 5))

# AB Testing
for i in range(3):
    axes[0][0].plot(
        ab_testing_pulls_per_arm_per_trial[:, i], label=f"Arm {i + 1}"
    )
axes[0][0].set_title("AB Testing - Arm pulls per trial")
axes[0][0].set_xlabel("Trial")
axes[0][0].set_ylabel("Accumulated Pulls")
axes[0][0].legend()

# UCB1
for i in range(3):
    axes[0][1].plot(ucb1_pulls_per_arm_per_trial[:, i], label=f"Arm {i + 1}")
axes[0][1].set_title("UCB1 - Arm pulls per trial")
axes[0][0].set_xlabel("Trial")
axes[0][0].set_ylabel("Accumulated Pulls")
axes[0][0].legend()

# Thompson Sampling
for i in range(3):
    axes[1][0].plot(
        thompson_sampling_pulls_per_arm_per_trial[:, i], label=f"Arm {i + 1}"
    )
axes[1][0].set_title("Thompson Sampling - Arm pulls per trial")
axes[0][0].set_xlabel("Trial")
axes[0][0].set_ylabel("Accumulated Pulls")
axes[0][0].legend()

# GP Bandit
for i in range(3):
    axes[1][1].plot(
        gp_bandit_pulls_per_arm_per_trial[:, i], label=f"Arm {i + 1}"
    )
axes[1][1].set_title("GP Bandit - Arm pulls per trial")
axes[0][0].set_xlabel("Trial")
axes[0][0].set_ylabel("Accumulated Pulls")
axes[0][0].legend()

plt.tight_layout()

# %% [markdown]
# #### 3.5.2.2 Analysis of the results
#
# I ran these tests several times, and the results are very similar.
#
# **UCB1** doesn't adapt well in this case where the performance difference between the arms is not very large, and there isn't one precise "expected CTR" in reality. On top of that, once it has decided what's the best arm, it will keep exploring the other options without a probability consideration.
#
# **Thompson Sampling** as expected, gave us the best results. It's specifically designed for this scenario as it assumes that the CTR is a Beta distribution that will be similar to a Normal distribution after learning, and the CTR is in fact a normal distribution in the simulation.
#
# **GP Bandit (Ax)** performs pretty well, but it's not as good as Thompson Sampling. It's more flexible and as such, it keeps exploring the other options.
#
# Something very important to notice is that looking at the **accumulated regret** we can see how both **Thompson Sampling** and **GP Bandit** converge. They could keep running for a longer time and the regret would keep decreasing.
#
# This is very important, one of the challenges in A/B testing is to know when to stop the experiment, to understand if we're wasting clicks, or we need to keep trying to be sure we've already discovered the best option.
