"""
Utility functions for the Synthetic Data Vault privacy classification project.

These helpers keep repeated notebook logic organized and easier to understand.
"""

import os
import numpy as np
import pandas as pd

from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report


def clean_adult_income_dataframe(df, target_col="class"):
    """
    Clean the Adult Income dataset.

    Steps:
    - standardize column names
    - replace '?' with missing values
    - drop missing rows
    - convert categorical columns to string format

    Args:
        df: Raw pandas DataFrame.
        target_col: Name of the target column.

    Returns:
        Cleaned pandas DataFrame.
    """
    clean_df = df.copy()

    clean_df.columns = (
        clean_df.columns
        .str.strip()
        .str.lower()
        .str.replace("-", "_")
        .str.replace(" ", "_")
    )

    clean_df = clean_df.replace("?", np.nan)
    clean_df = clean_df.dropna().reset_index(drop=True)

    for column in clean_df.columns:
        if str(clean_df[column].dtype) == "category":
            clean_df[column] = clean_df[column].astype(str)

    clean_df[target_col] = clean_df[target_col].astype(str).str.strip()

    return clean_df


def split_features_and_target(dataframe, target_column):
    """
    Separate a dataframe into features and target.

    Args:
        dataframe: Input pandas DataFrame.
        target_column: Name of the target column.

    Returns:
        X, y
    """
    X = dataframe.drop(columns=[target_column])
    y = dataframe[target_column]
    return X, y


def evaluate_classifier(model_name, training_data_name, model, X_train, y_train, X_test, y_test, positive_label=">50K"):
    """
    Train a classifier and evaluate it on a test set.

    Args:
        model_name: Name of the classifier.
        training_data_name: Label for the training data source.
        model: Scikit-learn model or pipeline.
        X_train, y_train: Training data.
        X_test, y_test: Testing data.
        positive_label: Positive class label.

    Returns:
        Dictionary of evaluation metrics.
    """
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)

    scores = {
        "model": model_name,
        "training_data": training_data_name,
        "accuracy": accuracy_score(y_test, predictions),
        "precision": precision_score(y_test, predictions, pos_label=positive_label, zero_division=0),
        "recall": recall_score(y_test, predictions, pos_label=positive_label, zero_division=0),
        "f1_score": f1_score(y_test, predictions, pos_label=positive_label, zero_division=0),
    }

    print("=" * 70)
    print(f"{model_name} trained on {training_data_name}")
    print("=" * 70)
    print(classification_report(y_test, predictions, zero_division=0))

    return scores


def save_results(results_df, output_path):
    """
    Save model results to a CSV file.

    Args:
        results_df: Results dataframe.
        output_path: Location where the CSV should be saved.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    results_df.to_csv(output_path, index=False)
    print(f"Results saved to: {output_path}")
