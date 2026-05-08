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

# %%
# %load_ext autoreload
# %autoreload 2

import os
import pandas as pd
import numpy as np
import mlflow
import mlflow_utils as mltuti
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.metrics import r2_score

# Environment setup
mlflow.set_tracking_uri("file:///tmp/mlflow_data")
mlflow.set_experiment("Ames_Housing_Analysis") 

# Load and split data
df = pd.read_csv('train_clean.csv')
cols_to_drop = [col for col in df.columns if 'price' in col.lower() or col == 'Id']
X = df.drop(columns=cols_to_drop)
y = df['SalePrice']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=12)

# Log transform targets for better regression performance
y_train_log = np.log1p(y_train)
y_test_log = np.log1p(y_test)

print(f"Dataset ready: {X_train.shape[0]} training samples.")

# %% [markdown]
# ## Baseline Model: Linear Regression
# Before we try to optimize our predictions with tuning, we start with a **Linear Regression** baseline. This gives us a starting point for our **RMSE** (error) and **R²** (accuracy) metrics. We will log this run to MLflow so we can compare it against our later experiments.

# %%
with mltuti.start_mlflow_run(experiment_name="Ames_Housing_Analysis", 
                             run_name="Linear_Regression_Baseline"):
    
    # Initialize and train the linear regression model
    lr_model = LinearRegression()
    lr_model.fit(X_train, y_train_log)
    
    # Predict on the test set
    y_pred_lr = lr_model.predict(X_test)
    
    # Log the results
    mltuti.log_regression_metrics(y_test_log, y_pred_lr)
    
    # Log the model type
    mlflow.log_param("model_type", "LinearRegression")
    
    print("Run completed for linear regression.")

# %% [markdown]
# ## Comparing Models: Ridge vs. Linear Regression
# Standard Linear Regression can sometimes "overfit" if there are too many features. **Ridge Regression** solves this by adding a penalty (Alpha) to the model. We will use MLflow to track how different Alpha values affect our **RMSE** and **R²**.

# %%
# Define range of alphas to test
alphas = [0.01, 0.1, 1.0, 10.0, 100.0]

for a in alphas:
    with mltuti.start_mlflow_run(experiment_name="Ames_Housing_Analysis", 
                                 run_name=f"Ridge_Alpha_{a}"):
        
        model = Ridge(alpha=a)
        model.fit(X_train, y_train_log)
        y_pred = model.predict(X_test)
        
        # Log metrics using our custom utility helper!
        mltuti.log_regression_metrics(y_test_log, y_pred)
        
        # Log specific parameters for this run
        mlflow.log_param("alpha", a)
        mlflow.log_param("model_type", "Ridge")
        
        print(f"Run completed for Alpha: {a}")

# %% [markdown]
# ## Conclusion
# By reviewing the MLflow dashboard, we can see how **RMSE** and **R²** change as **Alpha** increases. This tracking allows us to pick the most "reproducible" model for production.
