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
#     display_name: .venv (3.12.3)
#     language: python
#     name: python3
# ---

# %% [markdown]
# # YData-profiling Example: Baltimore Housing Data
#
# This notebook shows a complete example of using YData-profiling
# on a real dataset.
#
# We will:
# - load the Baltimore housing dataset
# - generate a profiling report
# - inspect the dataset
# - prepare features for modeling
# - train a regression model
# - evaluate the model

# %%
import sys
from pathlib import Path

sys.path.append(str(Path("src").resolve()))
import ydata_profiling_utils as ydputi

# %% [markdown]
# ## 1. Load the dataset
#
# We load the Baltimore housing dataset and inspect its basic structure.

# %%
df = ydputi.load_baltimore_data()
ydputi.print_basic_info(df)

# %% [markdown]
# ## 2. Generate a profiling report
#
# We generate a full YData-profiling report for the real dataset.
# This helps us inspect variable types, distributions, and potential data issues.

# %%
profile = ydputi.create_profile_report(
    df,
    title="Baltimore Housing Data Profiling Report"
)
output_path = ydputi.save_profile_report(
    profile,
    output_filename="baltim_example_profile.html"
)
print(f"Report saved to: {output_path}")

# %% [markdown]
# ## 3. Review profiling insights
#
# The generated YData-profiling report helps identify important data quality and modeling issues before building a regression model.
#
# In this dataset, the report is useful for checking:
#
# - variable types and numeric ranges
# - missing values
# - duplicate rows
# - skewed distributions
# - correlations between predictors and `PRICE`
#
# These checks help us decide how to clean the data and prepare it for modeling.
#

# %% [markdown]
# ## 4. Clean and prepare the data
#
# We clean the dataset by removing duplicate rows and keeping numeric columns for regression modeling.

# %%
df_clean = ydputi.clean_baltimore_data(df)

print("Original shape:", df.shape)
print("Cleaned shape:", df_clean.shape)
df_clean.head()

# %% [markdown]
# ## 5. Prepare regression features
#
# The target variable is `PRICE`. All other numeric columns are used as predictors.

# %%
X, y = ydputi.prepare_regression_data(
    df_clean,
    target_col="PRICE",
)

print("Feature matrix shape:", X.shape)
print("Target vector shape:", y.shape)
print("Target variable:", y.name)

# %% [markdown]
# ## 6. Train a regression model
#
# We train a Random Forest regression model. Missing feature values are filled with median values before training.

# %%
model, X_train, X_test, y_train, y_test = ydputi.train_regression_model(
    X,
    y,
    test_size=0.2,
    random_state=42,
)

print("Training rows:", X_train.shape[0])
print("Testing rows:", X_test.shape[0])

# %% [markdown]
# ## 7. Evaluate the model
#
# We evaluate the model using RMSE and R-squared.
#
# - RMSE measures the typical prediction error in the same unit as `PRICE`.
# - R-squared measures how much variation in `PRICE` is explained by the model.

# %%
metrics = ydputi.evaluate_regression_model(
    model,
    X_test,
    y_test,
)

for metric_name, metric_value in metrics.items():
    print(f"{metric_name}: {metric_value:.4f}")

# %% [markdown]
# ## 8. Summary
#
# YData-profiling supports the modeling workflow by providing a fast overview of the dataset before model training. The profile report helps identify variable types, missing values, distributions, and correlations. These insights make the cleaning and feature preparation steps more systematic.
#
# In this example, we used the Baltimore housing dataset, generated an automated profile report, cleaned the data, trained a regression model, and evaluated its predictive performance using RMSE and R-squared.
