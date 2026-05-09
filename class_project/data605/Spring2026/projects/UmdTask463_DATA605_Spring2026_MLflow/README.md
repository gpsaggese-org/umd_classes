# MLflow Housing Price Prediction Tutorial

This project teaches how to manage the machine learning lifecycle using MLflow. It demonstrates how to track experiments, log metrics, and package models using a housing price prediction dataset.

## Reader Experience
The 60-minute tutorial follows this breakdown:
*   **Setup (5 min):** Build the Docker environment and verify the MLflow tracking server.
*   **Introduction (10 min):** Understand the core components (Tracking, Models, Projects).
*   **API Exploration (20 min):** Work through `mlflow.API.ipynb` to learn native logging.
*   **Complete Example (25 min):** Run `mlflow.example.ipynb` to predict housing prices using Ridge Regression.

## Quick Start
*   `cd class_project/DATA605/Spring2026/projects/UmdTask463_DATA605_Spring2026_MLflow`
*   `./docker_build.sh`
*   `./docker_jupyter.sh`

## Notebooks
1.  **mlflow.eda.ipynb**
    *   Prepares the raw housing data.
    *   Handles outliers, missing values, and saves the cleaned dataset to `artifacts/`.
2.  **mlflow.API.ipynb**
    *   A walkthrough of the core MLflow API.
    *   Covers experiment creation and basic logging of parameters and metrics.
3.  **mlflow.example.ipynb**
    *   An end-to-end application predicting housing prices using the cleaned data.
    *   Demonstrates hyperparameter tuning (Ridge Alpha) and model comparison.

## Implementation Details
*   `mlflow_utils.py`: Contains helper functions for lifecycle management and logging metrics.
*   `requirements.txt`: Environment dependencies with pinned versions.
*   Uses Docker to ensure a reproducible development environment.