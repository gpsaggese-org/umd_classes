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
import matplotlib.pyplot as plt
import seaborn as sns

# Load the training data
df = pd.read_csv('train.csv')

# Show the first 5 rows
display(df.head())

# List all the columns
print(df.columns.tolist())

# %%
# Get the correlations of all numerical features with SalePrice
numeric_df = df.select_dtypes(include=['number'])
corr_matrix = numeric_df.corr()
top_correlations = corr_matrix['SalePrice'].sort_values(ascending=False)

# Display the top 10 most influential features
print("Top 10 Features most correlated with SalePrice:")
print(top_correlations.head(12))

# %%
# Check and remove outliers per Dean De Cock's suggestion
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x='GrLivArea', y='SalePrice')
plt.title('GrLivArea vs SalePrice')
plt.axvline(x=4000, color='r', linestyle='--')
plt.show()

# %%
# Remove outliers
df_no_outliers = df[df['GrLivArea'] < 4000].copy()

# %%
# Graph sale price distribution
plt.figure(figsize=(10, 6))
sns.histplot(df_no_outliers['SalePrice'], kde=True)
plt.title('Distribution of Sale Price (Excluding Outliers)')
plt.show()

# %%
import numpy as np

# Create a figure with two plots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

# Plot 1: Original Skewed Data
sns.histplot(df_no_outliers['SalePrice'], kde=True, ax=ax1)
ax1.set_title(f"Cleaned SalePrice (Skew: {df_no_outliers['SalePrice'].skew():.2f})")

# Plot 2: Log Transformed Data
df_no_outliers['LogSalePrice'] = np.log1p(df_no_outliers['SalePrice'])
sns.histplot(df_no_outliers['LogSalePrice'], kde=True, ax=ax2, color='red')
ax2.set_title(f"Log Transformed SalePrice (Skew: {df_no_outliers['LogSalePrice'].skew():.2f})")

plt.show()

# %%
df_no_outliers.to_csv('train_clean.csv', index=False)

print("Saved cleaned data to train_clean.csv.")

# %%
# Check for missing values and sort by highest percentage
missing_data = df_no_outliers.isnull().sum().sort_values(ascending=False)
missing_percentage = (missing_data / len(df_no_outliers)) * 100

# Combine into a table
missing_df = pd.concat([missing_data, missing_percentage], axis=1, keys=['Total', 'Percent'])
print(missing_df[missing_df['Total'] > 0])

# %%
# Handle categorical missing values by setting to 'None'
cols_to_none = [
    'PoolQC', 'MiscFeature', 'Alley', 'Fence', 'MasVnrType', 
    'FireplaceQu', 'GarageType', 'GarageFinish', 'GarageQual', 
    'GarageCond', 'BsmtQual', 'BsmtCond', 'BsmtExposure', 
    'BsmtFinType1', 'BsmtFinType2'
]
for col in cols_to_none:
    df_no_outliers[col] = df_no_outliers[col].fillna('None')

# Handle MasVnrArea missing values by setting to 0
df_no_outliers['MasVnrArea'] = df_no_outliers['MasVnrArea'].fillna(0)

# Handle LotFrontage missing values by using neighborhood median
df_no_outliers["LotFrontage"] = df_no_outliers.groupby("Neighborhood")["LotFrontage"].transform(
    lambda x: x.fillna(x.median())
)

# Handle Electrical missing values by using overall mode
df_no_outliers['Electrical'] = df_no_outliers['Electrical'].fillna(df_no_outliers['Electrical'].mode()[0])

# Handle GarageYrBlt missing values by using YearBuilt
df_no_outliers['GarageYrBlt'] = df_no_outliers['GarageYrBlt'].fillna(df_no_outliers['YearBuilt'])

print(f"Remaining missing values: {df_no_outliers.isnull().sum().sum()}")

# %%
# Convert categorical variables using one-hot encoding
df_final = pd.get_dummies(df_no_outliers)

# Save as train_clean.csv
df_final.to_csv('train_clean.csv', index=False)

print(f"Final shape after encoding: {df_final.shape}")
print("Cleaned data has been saved to artifacts/train_clean.csv. You are now ready to run mlflow.example.ipynb.")
