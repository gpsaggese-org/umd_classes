# ---
# jupyter:
#   jupytext:
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
# # DSP Simulator - pCTR prediction model
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
# There are different algorithms that can be used to decide the bid amount, but all of them require first to estimate the probability of click (pCTR) of an impression.
#
# For this reason, in order to create a simulation of the DSP, which is required to use the Bayesian Optimization technique, first we need to create a pCTR prediction model.
#
# The literature reference above discuss different models to predict the pCTR, but this prediction is done with all the information available. In this case we're trying to simulate an Adaptive Experiment where the pCTR is predicted based on the available information at the moment of the bid. This means, on June 7th, we only have information from June 6th to predict the pCTR of the bids of June 7th.
#
# At the end of this process we'll obtain a model file that can be used to obtain the pCTR that a DSP would use to decide whether to bid for an impression and the bid amount.
#
# The Jupyter Notebook requires the "ipinyou.contest.dataset" to create the models, which weighs several GBs. For this reason the dataset is not included in the repository.
#
# This Notebook also generates a cleaner dataset with feature engineering done that can be used to simulate the DSP.
#

# %% [markdown]
# ## Prepare pCTR prediction model and dataset

# %%
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, roc_auc_score
import xgboost as xgb
import joblib
import glob

# %% [markdown]
# ### Extract dataset for advertiser 1458

# %% [markdown]
# Decompress the training2 dataset and filter the rows containing the advertiser id 1458. This reduces the dataset from 21 to 5.4 GB.
#
# Then I use AWK to parse the files and obtain the ones where the Advertiser ID is 1458 (Column 20)

# %%
# # !bunzip2 ipinyou.contest.dataset/training2nd/*.txt.bz2
# # ! for file in ipinyou.contest.dataset/training2nd/*.txt; do grep $'\t1458\t' "$file" > "${file%.txt}_1458.txt"; done
# # ! for file in ipinyou.contest.dataset/training2nd/bid.*_1458.txt; do awk -F'\t' '$20 ~ /1458/ {print}' "$file" > "${file/_1458.txt/_1458.tsv}"; done
# # ! for file in ipinyou.contest.dataset/training2nd/imp.*_1458.txt; do awk -F'\t' '$23 ~ /1458/ {print}' "$file" > "${file/_1458.txt/_1458.tsv}"; done
# # ! for file in ipinyou.contest.dataset/training2nd/clk.*_1458.txt; do awk -F'\t' '$23 ~ /1458/ {print}' "$file" > "${file/_1458.txt/_1458.tsv}"; done

# %% [markdown]
# ## Train pCTR prediction model with day 1 data
#
# ### Prepare Dataset

# %%
# Load the tab separated file in ./ipinyou.contest.txt/training2nd
df_bids = pd.read_csv(
    "ipinyou.contest.dataset/training2nd/bid.20130606_1458.tsv",
    sep="\t",
    header=None,
    low_memory=False,
)
df_imps = pd.read_csv(
    "ipinyou.contest.dataset/training2nd/imp.20130606_1458.tsv",
    sep="\t",
    header=None,
    low_memory=False,
)
df_clks = pd.read_csv(
    "ipinyou.contest.dataset/training2nd/clk.20130606_1458.tsv",
    sep="\t",
    header=None,
    low_memory=False,
)

# %%
# Rename the columns
df_bids.columns = [
    "bid_id",
    "timestamp",
    "ipinyou_id",
    "user_agent",
    "ip_address",
    "region_id",
    "city_id",
    "ad_exchange_id",
    "domain",
    "url",
    "anon_url",
    "slot_id",
    "slot_width",
    "slot_height",
    "slot_visibility",
    "slot_format",
    "slot_floor_price",
    "creative_id",
    "bidding_price",
    "advertiser_id",
    "user_profile_ids",
]

# Drop the user_profile_ids column as it's always empty
df_bids = df_bids.drop(columns=["user_profile_ids"])

df_bids.info()

# %%
df_imps.columns = [
    "bid_id",
    "timestamp",
    "log_type",
    "ipinyou_id",
    "user_agent",
    "ip_address",
    "region_id",
    "city_id",
    "ad_exchange_id",
    "domain",
    "url",
    "anon_url",
    "slot_id",
    "slot_width",
    "slot_height",
    "slot_visibility",
    "slot_format",
    "slot_floor_price",
    "creative_id",
    "bidding_price",
    "pay_price",
    "landing_page_url",
    "advertiser_id",
    "user_profile_ids",
]

df_imps.info()

# %%
df_clks.columns = [
    "bid_id",
    "timestamp",
    "log_type",
    "ipinyou_id",
    "user_agent",
    "ip_address",
    "region_id",
    "city_id",
    "ad_exchange_id",
    "domain",
    "url",
    "anon_url",
    "slot_id",
    "slot_width",
    "slot_height",
    "slot_visibility",
    "slot_format",
    "slot_floor_price",
    "creative_id",
    "bidding_price",
    "pay_price",
    "landing_page_url",
    "advertiser_id",
    "user_profile_ids",
]

df_clks.info()

# %%
# From df_imps keep only "bid_id", "pay_price", "user_profile_ids"
df_imps = df_imps[["bid_id", "pay_price", "user_profile_ids"]]
# From df_clks keep only "bid_id". I'm only interested in the clicks
df_clks = df_clks[["bid_id"]]

# Merge the impressions and clicks, add "clicked" column as 1 if matched, 0 otherwise
df_imp_with_clk = pd.merge(
    df_imps,
    df_clks,
    on="bid_id",
    how="left",
    indicator=True,
    suffixes=("_imp", "_clk"),
)
df_imp_with_clk["clicked"] = (df_imp_with_clk["_merge"] == "both").astype(int)
df_imp_with_clk = df_imp_with_clk.drop(columns=["_merge"])

# Free the memory
del df_clks, df_imps

df_imp_with_clk.info()

# %%
df_imp_with_clk["clicked"].value_counts()

# %%
# Now merge the bids with the impressions
# We only get those who are in both, we're not interested on getting the bids without impressions for the CTR prediction
df_bids_imp_with_clk = pd.merge(
    df_bids, df_imp_with_clk, on="bid_id", how="inner", suffixes=("_bid", "_imp")
)
df_bids_imp_with_clk.info()

# Free the memory
del df_bids, df_imp_with_clk

# %%
print("Region IDs:")
print(df_bids_imp_with_clk["region_id"].unique())
print("City IDs:")
print(df_bids_imp_with_clk["city_id"].unique())
print("Ad Exchange IDs:")
print(df_bids_imp_with_clk["ad_exchange_id"].unique())
print("Slot IDs:")
print(df_bids_imp_with_clk["slot_id"].unique())
print("Slot Formats:")
print(df_bids_imp_with_clk["slot_format"].unique())
print("Slot Visibilities:")
print(df_bids_imp_with_clk["slot_visibility"].unique())
print("Slot Widths:")
print(df_bids_imp_with_clk["slot_width"].unique())
print("Slot Heights:")
print(df_bids_imp_with_clk["slot_height"].unique())
print("Creative IDs:")
print(df_bids_imp_with_clk["creative_id"].unique())
print("User Profile IDs:")
print(df_bids_imp_with_clk["user_profile_ids"].unique())

# %% [markdown]
# ### Feature Engineering

# %%
# Transform timestamp to datetime
df_bids_imp_with_clk["timestamp"] = pd.to_datetime(
    df_bids_imp_with_clk["timestamp"], errors="coerce"
)

# Create a new column with the hour of the day
df_bids_imp_with_clk["hour"] = df_bids_imp_with_clk["timestamp"].dt.hour

# Create a new column with the day of the week
df_bids_imp_with_clk["day_of_week"] = df_bids_imp_with_clk[
    "timestamp"
].dt.dayofweek


def get_browser(user_agent):
    if pd.isna(user_agent):
        return "Unknown"
    ua = user_agent.lower()
    if "chrome" in ua:
        return "Chrome"
    elif "firefox" in ua:
        return "Firefox"
    elif "safari" in ua and "chrome" not in ua:
        return "Safari"
    elif "msie" in ua or "trident" in ua:
        return "Explorer"
    elif "edge" in ua:
        return "Edge"
    elif "opera" in ua:
        return "Opera"
    else:
        return "Other"


def get_os(user_agent):
    if pd.isna(user_agent):
        return "Unknown"
    ua = user_agent.lower()
    if "windows" in ua:
        return "Windows"
    elif "mac os x" in ua:
        return "MacOS"
    elif "linux" in ua:
        return "Linux"
    elif "android" in ua:
        return "Android"
    elif "iphone" in ua or "ios" in ua:
        return "iOS"
    else:
        return "Other"


# Create new columns for browser and operating system
df_bids_imp_with_clk["browser"] = df_bids_imp_with_clk["user_agent"].apply(
    get_browser
)
df_bids_imp_with_clk["os"] = df_bids_imp_with_clk["user_agent"].apply(get_os)

df_bids_imp_with_clk.head()

# %%
# Create one-hot encoding
one_hot_cols = [
    "browser",
    "os",
    "region_id",
    "ad_exchange_id",
    "slot_visibility",
    "slot_format",
    "slot_width",
    "slot_height",
    "creative_id",
]

df_bids_imp_with_clk = pd.get_dummies(
    df_bids_imp_with_clk, columns=one_hot_cols, prefix=one_hot_cols
)
# Convert boolean hot-encoded columns to int
for col in df_bids_imp_with_clk.columns:
    if df_bids_imp_with_clk[col].dtype == "bool":
        df_bids_imp_with_clk[col] = df_bids_imp_with_clk[col].astype(int)

df_bids_imp_with_clk.info()

# %%
# List of features as specified
features = ["hour", "day_of_week"]

# Dynamically add all columns that start with the specified prefixes
prefixes = [
    "browser_",
    "os_",
    "ad_exchange_id_",
    "slot_visibility_",
    "slot_format_",
    "slot_width_",
    "slot_height_",
    "creative_id_",
]

dynamic_features = []
for prefix in prefixes:
    dynamic_features.extend(
        [col for col in df_bids_imp_with_clk.columns if col.startswith(prefix)]
    )

features.extend(dynamic_features)

# Drop rows with missing required feature columns, if any
initial_row_count = len(df_bids_imp_with_clk)
df = df_bids_imp_with_clk.dropna(subset=features + ["clicked"])
dropped_rows = initial_row_count - len(df)
print(f"Rows dropped due to missing features or clicked label: {dropped_rows}")

# Prepare X and y
X = df[features]
y = df["clicked"]

# Split data into train and test
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Train an XGBoost model for binary classification
xgb_model = xgb.XGBClassifier(
    n_estimators=100,
    max_depth=5,
    learning_rate=0.1,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=42,
    eval_metric="logloss",
)

xgb_model.fit(X_train, y_train)

# Predict on test set
y_pred = xgb_model.predict(X_test)
y_pred_proba = xgb_model.predict_proba(X_test)[:, 1]

# Display results
print(classification_report(y_test, y_pred, zero_division=0))
print("ROC AUC:", roc_auc_score(y_test, y_pred_proba))

# %% [markdown]
# ### Create CTR Prediction Model with XGBoost

# %%
y_pred_proba.mean()

# %%
# Store the trained XGBoost model in a file
joblib.dump(xgb_model, "xgb_model.joblib")

# %%
# Load the trained model
loaded_model = joblib.load("xgb_model.joblib")

# Select a few records from the original dataset for inference
X_few = X_test.head(100)

# Predict probabilities and classes for these records
few_pred_proba = loaded_model.predict_proba(X_few)[:, 1]
few_pred = loaded_model.predict(X_few)

# Display the results
inference_df = X_few.copy()
inference_df["predicted_clicked"] = few_pred
inference_df["predicted_proba"] = few_pred_proba

print(inference_df[["predicted_clicked", "predicted_proba"]])

print(y_pred_proba.mean())

print("ROC AUC:", roc_auc_score(y_test, y_pred_proba))

# %% [markdown]
# The ROC AUC is better than random. The mean predicted probability of click is 0.0007, the same than the average click rate of the advertiser. This is a good sign.

# %% [markdown]
# ## Train models for each day
#
# In the experiment we're going to simulate, we need to estimate the CTR given a Bid. The dataset contains bids, impressions and clicks data from June 6th to June 12th.
#
# The simulation will start on day 2 (June 7th) and run the bids registered on that day. At that point we should only have access to the previous day's data to predict the CTR.
#
# I'm going to create 6 different models:
# - June 6th -> To use on June 7th
# - June 6th and 7th -> To use on June 8th
# - June 6th to 8th -> To use on June 9th
# - June 6th to 9th -> To use on June 10th
# - June 6th to 10th -> To use on June 11th
# - June 6th to 11th -> To use on June 12th
#
# The code to create the models will be packaged as a function to be called multiple times.
#

# %%
TRAINING_DATA_DIR = "ipinyou.contest.dataset/training2nd"


def get_browser(user_agent):
    if pd.isna(user_agent):
        return "Unknown"
    ua = user_agent.lower()
    if "chrome" in ua:
        return "Chrome"
    elif "firefox" in ua:
        return "Firefox"
    elif "safari" in ua and "chrome" not in ua:
        return "Safari"
    elif "msie" in ua or "trident" in ua:
        return "Explorer"
    elif "edge" in ua:
        return "Edge"
    elif "opera" in ua:
        return "Opera"
    else:
        return "Other"


def get_os(user_agent):
    if pd.isna(user_agent):
        return "Unknown"
    ua = user_agent.lower()
    if "windows" in ua:
        return "Windows"
    elif "mac os x" in ua:
        return "MacOS"
    elif "linux" in ua:
        return "Linux"
    elif "android" in ua:
        return "Android"
    elif "iphone" in ua or "ios" in ua:
        return "iOS"
    else:
        return "Other"


def create_model(dates: list[str]):
    print("====================================================")
    print(f"Create prediction model from {dates[0]} to {dates[-1]}")
    print("====================================================")

    all_bids_imp_with_clk = []
    for date in dates:
        df_bids = pd.read_csv(
            f"{TRAINING_DATA_DIR}/bid.{date}_1458.tsv",
            sep="\t",
            header=None,
            low_memory=False,
        )
        df_imps = pd.read_csv(
            f"{TRAINING_DATA_DIR}/imp.{date}_1458.tsv",
            sep="\t",
            header=None,
            low_memory=False,
        )
        df_clks = pd.read_csv(
            f"{TRAINING_DATA_DIR}/clk.{date}_1458.tsv",
            sep="\t",
            header=None,
            low_memory=False,
        )

        df_bids.columns = [
            "bid_id",
            "timestamp",
            "ipinyou_id",
            "user_agent",
            "ip_address",
            "region_id",
            "city_id",
            "ad_exchange_id",
            "domain",
            "url",
            "anon_url",
            "slot_id",
            "slot_width",
            "slot_height",
            "slot_visibility",
            "slot_format",
            "slot_floor_price",
            "creative_id",
            "bidding_price",
            "advertiser_id",
            "user_profile_ids",
        ]
        df_bids = df_bids.drop(columns=["user_profile_ids"])
        df_imps.columns = [
            "bid_id",
            "timestamp",
            "log_type",
            "ipinyou_id",
            "user_agent",
            "ip_address",
            "region_id",
            "city_id",
            "ad_exchange_id",
            "domain",
            "url",
            "anon_url",
            "slot_id",
            "slot_width",
            "slot_height",
            "slot_visibility",
            "slot_format",
            "slot_floor_price",
            "creative_id",
            "bidding_price",
            "pay_price",
            "landing_page_url",
            "advertiser_id",
            "user_profile_ids",
        ]
        df_clks.columns = [
            "bid_id",
            "timestamp",
            "log_type",
            "ipinyou_id",
            "user_agent",
            "ip_address",
            "region_id",
            "city_id",
            "ad_exchange_id",
            "domain",
            "url",
            "anon_url",
            "slot_id",
            "slot_width",
            "slot_height",
            "slot_visibility",
            "slot_format",
            "slot_floor_price",
            "creative_id",
            "bidding_price",
            "pay_price",
            "landing_page_url",
            "advertiser_id",
            "user_profile_ids",
        ]
        df_imps = df_imps[["bid_id", "pay_price", "user_profile_ids"]]
        df_clks = df_clks[["bid_id"]]

        # Merge the impressions and clicks, add "clicked" column as 1 if matched, 0 otherwise
        df_imp_with_clk = pd.merge(
            df_imps,
            df_clks,
            on="bid_id",
            how="left",
            indicator=True,
            suffixes=("_imp", "_clk"),
        )
        df_imp_with_clk["clicked"] = (
            df_imp_with_clk["_merge"] == "both"
        ).astype(int)
        df_imp_with_clk = df_imp_with_clk.drop(columns=["_merge"])
        del df_clks, df_imps

        # Now merge the bids with the impressions
        # We only get those who are in both, we're not interested on getting the bids without impressions for the CTR prediction
        df_bids_imp_with_clk = pd.merge(
            df_bids,
            df_imp_with_clk,
            on="bid_id",
            how="inner",
            suffixes=("_bid", "_imp"),
        )
        del df_bids, df_imp_with_clk

        # Feature Engineering
        df_bids_imp_with_clk["timestamp"] = pd.to_datetime(
            df_bids_imp_with_clk["timestamp"], errors="coerce"
        )
        df_bids_imp_with_clk["hour"] = df_bids_imp_with_clk["timestamp"].dt.hour
        df_bids_imp_with_clk["day_of_week"] = df_bids_imp_with_clk[
            "timestamp"
        ].dt.dayofweek

        # Create new columns for browser and operating system
        df_bids_imp_with_clk["browser"] = df_bids_imp_with_clk[
            "user_agent"
        ].apply(get_browser)
        df_bids_imp_with_clk["os"] = df_bids_imp_with_clk["user_agent"].apply(
            get_os
        )

        # Create one-hot encoding
        one_hot_cols = [
            "browser",
            "os",
            "region_id",
            "ad_exchange_id",
            "slot_visibility",
            "slot_format",
            "slot_width",
            "slot_height",
            "creative_id",
        ]

        df_bids_imp_with_clk = pd.get_dummies(
            df_bids_imp_with_clk, columns=one_hot_cols, prefix=one_hot_cols
        )
        # Convert boolean hot-encoded columns to int
        for col in df_bids_imp_with_clk.columns:
            if df_bids_imp_with_clk[col].dtype == "bool":
                df_bids_imp_with_clk[col] = df_bids_imp_with_clk[col].astype(int)

        # Append for later concatenation
        all_bids_imp_with_clk.append(df_bids_imp_with_clk)

    # Concatenate all DataFrames into a single DataFrame
    df_bids_imp_with_clk = pd.concat(all_bids_imp_with_clk, ignore_index=True)

    avg_spent_per_day = df_bids_imp_with_clk["pay_price"].sum() / len(dates)

    # Start training the XGBoost model
    features = ["hour", "day_of_week"]

    # Define the columns dynamically based on the one-hot encoding
    prefixes = [
        "browser_",
        "os_",
        "ad_exchange_id_",
        "slot_visibility_",
        "slot_format_",
        "slot_width_",
        "slot_height_",
        "creative_id_",
    ]

    dynamic_features = []
    for prefix in prefixes:
        dynamic_features.extend(
            [
                col
                for col in df_bids_imp_with_clk.columns
                if col.startswith(prefix)
            ]
        )

    features.extend(dynamic_features)

    print(
        f"Training CTR prediction model from {dates[0]} to {dates[-1]} with features: {features}"
    )

    # Drop rows with missing required feature columns, if any
    initial_row_count = len(df_bids_imp_with_clk)
    df = df_bids_imp_with_clk.dropna(subset=features + ["clicked"])
    dropped_rows = initial_row_count - len(df)
    print(
        f"Rows dropped due to missing features or clicked label: {dropped_rows}"
    )

    # Prepare X and y
    X = df[features]
    y = df["clicked"]

    # Split data into train and test
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # Train an XGBoost model for binary classification
    xgb_model = xgb.XGBClassifier(
        n_estimators=100,
        max_depth=5,
        learning_rate=0.1,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=42,
        eval_metric="logloss",
    )

    xgb_model.fit(X_train, y_train)

    # Predict on test set
    y_pred = xgb_model.predict(X_test)
    y_pred_proba = xgb_model.predict_proba(X_test)[:, 1]

    # Display results
    print(classification_report(y_test, y_pred, zero_division=0))
    print("ROC AUC:", roc_auc_score(y_test, y_pred_proba))
    print(f"Avg ground truth CTR: {y_test.mean()}")
    print(f"Avg predicted CTR: {y_pred_proba.mean()}")

    # Store the model in a file
    joblib.dump(xgb_model, f"xgb_model_{dates[-1]}.joblib")

    # Store the features used by this model in a file
    with open(f"features_{dates[-1]}.txt", "w") as f:
        f.write("\n".join(features))

    # Store the average CTR and the bid to pay ratio
    average_ctr = df["clicked"].mean()
    bid_to_pay_ratio = df["bidding_price"].mean() / df["pay_price"].mean()

    # Store average_ctr and bid_to_pay_ratio in a file
    import json

    with open(f"average_ctr_and_bid_to_pay_ratio_{dates[-1]}.json", "w") as f:
        json.dump(
            {
                "average_ctr": average_ctr,
                "bid_to_pay_ratio": bid_to_pay_ratio,
                "avg_spent_per_day": avg_spent_per_day,
            },
            f,
            indent=4,
        )

    return xgb_model, average_ctr, bid_to_pay_ratio


# %%
create_model(["20130606"])
create_model(["20130606", "20130607"])
create_model(["20130606", "20130607", "20130608"])
create_model(["20130606", "20130607", "20130608", "20130609"])
create_model(["20130606", "20130607", "20130608", "20130609", "20130610"])
create_model(
    ["20130606", "20130607", "20130608", "20130609", "20130610", "20130611"]
)

# %% [markdown]
# ## Evaluate predicted CTR
#
# Supposing we are on June 12th, we receive a bid, we want to predict the CTR of the bid.
#
# We need to use the model trained on data from June 6th to June 11th, read a line from the June 12th bid file, and extract the features from the bid

# %%
LAST_DATE = "20130611"
SIMULATION_DATE = "20130612"
df_bids = pd.read_csv(
    f"ipinyou.contest.dataset/training2nd/bid.{SIMULATION_DATE}_1458.tsv",
    sep="\t",
    header=None,
    low_memory=False,
)
df_bids.columns = [
    "bid_id",
    "timestamp",
    "ipinyou_id",
    "user_agent",
    "ip_address",
    "region_id",
    "city_id",
    "ad_exchange_id",
    "domain",
    "url",
    "anon_url",
    "slot_id",
    "slot_width",
    "slot_height",
    "slot_visibility",
    "slot_format",
    "slot_floor_price",
    "creative_id",
    "bidding_price",
    "advertiser_id",
    "user_profile_ids",
]

# Load the model
model = joblib.load(f"xgb_model_{LAST_DATE}.joblib")

# Load the features
features = open(f"features_{LAST_DATE}.txt", "r").read().splitlines()

# %%
first_bid = df_bids.iloc[[0]].copy()


def predict_ctr(
    bid: pd.DataFrame, model: xgb.XGBClassifier, features: list[str]
):
    # Process the fields appropriately on that DataFrame row
    bid["timestamp"] = pd.to_datetime(bid["timestamp"], errors="coerce")
    bid["hour"] = bid["timestamp"].dt.hour
    bid["day_of_week"] = bid["timestamp"].dt.dayofweek
    bid["browser"] = bid["user_agent"].apply(get_browser)
    bid["os"] = bid["user_agent"].apply(get_os)

    # Create one-hot encoding
    one_hot_cols = [
        "browser",
        "os",
        "region_id",
        "ad_exchange_id",
        "slot_visibility",
        "slot_format",
        "slot_width",
        "slot_height",
        "creative_id",
    ]
    bid = pd.get_dummies(bid, columns=one_hot_cols, prefix=one_hot_cols)
    # Convert boolean hot-encoded columns to int
    for col in bid.columns:
        if bid[col].dtype == "bool":
            bid[col] = bid[col].astype(int)

    missing_features = [f for f in features if f not in bid.columns]
    for f in missing_features:
        bid[f] = False

    # Select features in correct order for the model
    X_bid = bid[features]

    # Predict CTR using the loaded model
    predicted_ctr = model.predict_proba(X_bid)[:, 1][0]

    print("Predicted CTR for first bid:", predicted_ctr)


# %%
predict_ctr(first_bid, model, features)
second_bid = df_bids.iloc[[1]].copy()
predict_ctr(second_bid, model, features)
third_bid = df_bids.iloc[[2]].copy()
predict_ctr(third_bid, model, features)
fourth_bid = df_bids.iloc[[3]].copy()
predict_ctr(fourth_bid, model, features)
fifth_bid = df_bids.iloc[[4]].copy()
predict_ctr(fifth_bid, model, features)

# %% [markdown]
# ## Create feature engineered dataset
#
# The following code creates a new dataset with the feature engineered columns, that can be used to simulate the DSP.

# %%
# Read all the feature files to discover all the possible features generated by the one-hot encoding
feature_files = glob.glob("features_*.txt")
features = []
for file in feature_files:
    # I don't use a set because I want to keep the order of the features
    with open(file, "r") as f:
        for line in f:
            a_feature = line.strip()
            if a_feature not in features:
                features.append(a_feature)

average_ctrs = {}

for date in [
    "20130606",
    "20130607",
    "20130608",
    "20130609",
    "20130610",
    "20130611",
    "20130612",
]:
    df_bids = pd.read_csv(
        f"{TRAINING_DATA_DIR}/bid.{date}_1458.tsv",
        sep="\t",
        header=None,
        low_memory=False,
    )
    df_imps = pd.read_csv(
        f"{TRAINING_DATA_DIR}/imp.{date}_1458.tsv",
        sep="\t",
        header=None,
        low_memory=False,
    )
    df_clks = pd.read_csv(
        f"{TRAINING_DATA_DIR}/clk.{date}_1458.tsv",
        sep="\t",
        header=None,
        low_memory=False,
    )
    df_bids.columns = [
        "bid_id",
        "timestamp",
        "ipinyou_id",
        "user_agent",
        "ip_address",
        "region_id",
        "city_id",
        "ad_exchange_id",
        "domain",
        "url",
        "anon_url",
        "slot_id",
        "slot_width",
        "slot_height",
        "slot_visibility",
        "slot_format",
        "slot_floor_price",
        "creative_id",
        "bidding_price",
        "advertiser_id",
        "user_profile_ids",
    ]
    df_bids = df_bids.drop(columns=["user_profile_ids"])
    df_imps.columns = [
        "bid_id",
        "timestamp",
        "log_type",
        "ipinyou_id",
        "user_agent",
        "ip_address",
        "region_id",
        "city_id",
        "ad_exchange_id",
        "domain",
        "url",
        "anon_url",
        "slot_id",
        "slot_width",
        "slot_height",
        "slot_visibility",
        "slot_format",
        "slot_floor_price",
        "creative_id",
        "bidding_price",
        "pay_price",
        "landing_page_url",
        "advertiser_id",
        "user_profile_ids",
    ]
    df_clks.columns = [
        "bid_id",
        "timestamp",
        "log_type",
        "ipinyou_id",
        "user_agent",
        "ip_address",
        "region_id",
        "city_id",
        "ad_exchange_id",
        "domain",
        "url",
        "anon_url",
        "slot_id",
        "slot_width",
        "slot_height",
        "slot_visibility",
        "slot_format",
        "slot_floor_price",
        "creative_id",
        "bidding_price",
        "pay_price",
        "landing_page_url",
        "advertiser_id",
        "user_profile_ids",
    ]
    df_imps = df_imps[["bid_id", "pay_price", "user_profile_ids"]]
    df_clks = df_clks[["bid_id"]]

    # Merge the impressions and clicks, add "clicked" column as 1 if matched, 0 otherwise
    df_imp_with_clk = pd.merge(
        df_imps,
        df_clks,
        on="bid_id",
        how="left",
        indicator=True,
        suffixes=("_imp", "_clk"),
    )
    df_imp_with_clk["clicked"] = (df_imp_with_clk["_merge"] == "both").astype(
        int
    )
    df_imp_with_clk = df_imp_with_clk.drop(columns=["_merge"])
    del df_clks, df_imps

    # Now merge the bids with the impressions
    # We only get those who are in both, we're not interested on getting the bids without impressions for the CTR prediction
    df_bids_imp_with_clk = pd.merge(
        df_bids,
        df_imp_with_clk,
        on="bid_id",
        how="inner",
        suffixes=("_bid", "_imp"),
    )
    del df_bids, df_imp_with_clk

    # Feature Engineering
    df_bids_imp_with_clk["timestamp"] = pd.to_datetime(
        df_bids_imp_with_clk["timestamp"], errors="coerce"
    )
    df_bids_imp_with_clk["hour"] = df_bids_imp_with_clk["timestamp"].dt.hour
    df_bids_imp_with_clk["day_of_week"] = df_bids_imp_with_clk[
        "timestamp"
    ].dt.dayofweek

    # Create new columns for browser and operating system
    df_bids_imp_with_clk["browser"] = df_bids_imp_with_clk["user_agent"].apply(
        get_browser
    )
    df_bids_imp_with_clk["os"] = df_bids_imp_with_clk["user_agent"].apply(get_os)

    # Create one-hot encoding
    one_hot_cols = [
        "browser",
        "os",
        "region_id",
        "ad_exchange_id",
        "slot_visibility",
        "slot_format",
        "slot_width",
        "slot_height",
        "creative_id",
    ]
    df_bids_imp_with_clk = pd.get_dummies(
        df_bids_imp_with_clk, columns=one_hot_cols, prefix=one_hot_cols
    )

    # Convert boolean hot-encoded columns to int
    for col in df_bids_imp_with_clk.columns:
        if df_bids_imp_with_clk[col].dtype == "bool":
            df_bids_imp_with_clk[col] = df_bids_imp_with_clk[col].astype(int)

    missing_features = [
        f for f in features if f not in df_bids_imp_with_clk.columns
    ]
    for f in missing_features:
        df_bids_imp_with_clk[f] = False

    # Now, I only want to keep the columns that are in the features list plus the clicked column
    df_bids_imp_with_clk = df_bids_imp_with_clk[
        ["clicked", "slot_floor_price", "bidding_price", "pay_price"] + features
    ]

    # Save the dataset
    # Convert boolean columns to integers (0/1)
    bool_cols = df_bids_imp_with_clk.select_dtypes(include=["bool"]).columns
    df_bids_imp_with_clk[bool_cols] = df_bids_imp_with_clk[bool_cols].astype(int)
    df_bids_imp_with_clk.to_csv(f"bid_with_features_{date}.csv", index=False)

    # Calculate the average CTR for all the days
    average_ctrs[date] = df_bids_imp_with_clk["clicked"].mean()

# Store the average CTRs
import json

with open("average_ctrs.json", "w") as f:
    json.dump(average_ctrs, f)

# %% [markdown]
# ## Add Predicted CTR to the feature engineered dataset
#
# The model created for each day is used by the DSP to predict the CTR of a bid. To simplify the simulation, and avoid uploading the model to the repository, we will run the model now and add the predicted CTR to the feature engineered dataset.

# %%
from Ax_utils import load_pctr_prediction_model

for date in [
    "20130607",
    "20130608",
    "20130609",
    "20130610",
    "20130611",
    "20130612",
]:
    df_bids = pd.read_csv(f"dataset/bid_with_features_{date}.csv")

    model, features, average_ctr, bid_to_pay_ratio = load_pctr_prediction_model(
        date
    )

    df_bids["pctr"] = model.predict_proba(df_bids[features])[:, 1]

    # Save the dataset
    df_bids.to_csv(f"dataset/bid_with_features_and_pctr_{date}.csv", index=False)
