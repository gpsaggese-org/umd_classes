# MLflow Housing Price Prediction Tutorial

This project teaches how to manage the machine learning lifecycle using MLflow. It demonstrates how to track experiments, log metrics, and package models using a housing price prediction dataset.

## Quick Start
*   `cd class_project/DATA605/Spring2026/projects/UmdTask463_DATA605_Spring2026_MLflow`
*   `./docker_build.sh`
*   `./docker_jupyter.sh`

## Notebooks
1.  **mlflow.API.ipynb**
    *   A walkthrough of the core MLflow API.
    *   Covers experiment creation, starting runs, and basic logging of parameters and metrics.
2.  **mlflow.example.ipynb**
    *   An end-to-end application predicting housing prices.
    *   Demonstrates hyperparameter tuning, model comparison, and saving models to the MLflow Registry.

## Implementation Details
*   `mlflow_utils.py`: Contains helper functions for lifecycle management and logging metrics.
*   `requirements.txt`: Environment dependencies with pinned versions.
*   Uses Docker to ensure a reproducible development environment.