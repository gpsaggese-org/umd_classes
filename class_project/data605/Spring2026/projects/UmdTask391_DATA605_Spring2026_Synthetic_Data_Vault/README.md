# DATA605 Spring 2026: Synthetic Data Vault Privacy Classification Project

## Project Overview

This project explores the use of Synthetic Data Vault (SDV) for privacy-preserving synthetic data generation.

The main goal is to generate a synthetic version of a real-world dataset and test whether the synthetic data can still support a machine learning classification task. I used the Adult Income dataset, generated synthetic training data using SDV, and compared models trained on real data versus synthetic data.

## Dataset

The project uses the Adult Income dataset. The dataset contains demographic and employment-related features such as age, education, occupation, work hours, and income class.

The target variable is:

- `<=50K`
- `>50K`

This is a binary classification problem.

I selected this dataset because it contains both numerical and categorical features, making it a good example for testing synthetic tabular data generation.

## Tools and Libraries

Main tools used in this project:

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Scikit-learn
- Synthetic Data Vault
- SDMetrics
- Jupyter Notebook

## Project Workflow

The project follows these steps:

1. Load the Adult Income dataset.
2. Clean missing and inconsistent values.
3. Explore the dataset using summary statistics and visualizations.
4. Split the real data into training and testing sets.
5. Fit an SDV Gaussian Copula synthesizer on the real training data.
6. Generate a synthetic training dataset.
7. Evaluate synthetic data quality using SDMetrics.
8. Train classification models on real and synthetic data.
9. Evaluate all models on the same real test set.
10. Compare accuracy, precision, recall, and F1-score.
11. Run a small hyperparameter tuning experiment.
12. Interpret results, limitations, and conclusions.

## Main Experiment

The most important experiment is:

> Train a machine learning model on synthetic data and test it on real unseen test data.

This checks whether the synthetic data preserves useful predictive patterns from the original dataset.

## Files

```text
notebooks/Synthetic_Data_Vault.ipynb
    Main notebook containing the full SDV workflow, EDA, model training, evaluation, and interpretation.

outputs/model_comparison_results.csv
    Initial model comparison results.

outputs/final_model_comparison_results.csv
    Final results including the hyperparameter tuning experiment.

requirements.txt
    Python libraries required to run the project.

synthetic_data_vault_utils.py
    Utility file reserved for helper functions.

Dockerfile
docker_build.sh
docker_run.sh
    Docker-related project files.

## Additional Tutorial Notebook

I also included a shorter API-focused notebook:

```text
notebooks/synthetic_data_vault.API.ipynb
