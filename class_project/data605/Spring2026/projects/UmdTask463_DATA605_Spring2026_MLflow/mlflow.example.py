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
import pandas as pd
import mlflow_utils as mltuti
from sklearn.model_selection import train_test_split

# Load clean data
df = pd.read_csv('train_clean.csv')

# Define Features (X) and Target (y)
X = df.drop(columns=['SalePrice', 'Id'])
y = df['SalePrice']

# Perform 80/20 train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=12)

print(f"Training on {X_train.shape[0]} houses.")
print(f"Testing on {X_test.shape[0]} houses.")

# %%
