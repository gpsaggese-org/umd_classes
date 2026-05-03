"""
Utility functions for MLflow-based workflows.

Import as:
import mlflow_utils as mltuti
"""

import logging
import mlflow
import mlflow.sklearn
from sklearn.metrics import mean_squared_error
import numpy as np

# Path inside the Docker container
import sys
sys.path.append('/git_root')

try:
    import helpers.hdbg as hdbg
    _HELPERS = True
except ImportError:
    _HELPERS = False

_LOG = logging.getLogger(__name__)

# ### ####################################################################
# MLflow Lifecycle Management
# ### ####################################################################

def start_mlflow_run(experiment_name: str):
    """
    Sets the experiment and starts a new MLflow run.

    :param experiment_name: Name of the experiment in MLflow
    :return: An active MLflow run object
    """
    if _HELPERS:
        hdbg.dassert_isinstance(experiment_name, str)
    
    mlflow.set_experiment(experiment_name)
    return mlflow.start_run()

# ### ####################################################################
# Logging & Metrics
# ### ####################################################################

def log_regression_metrics(y_true: np.ndarray, y_pred: np.ndarray):
    """
    Calculates and logs RMSE and MSE to the active MLflow run.

    :param y_true: Actual target values
    :param y_pred: Predicted target values
    """
    mse = mean_squared_error(y_true, y_pred)
    rmse = np.sqrt(mse)
    
    mlflow.log_metric("mse", mse)
    mlflow.log_metric("rmse", rmse)
    
    _LOG.info("Logged metrics - RMSE: %.4f, MSE: %.4f", rmse, mse)

def save_model(model, artifact_path: str = "model"):
    """
    Serializes and logs a scikit-learn model to MLflow.

    :param model: The trained sklearn model object
    :param artifact_path: The directory path within the MLflow run for the model
    """
    mlflow.sklearn.log_model(model, artifact_path)
    _LOG.info("Model logged to artifact path: %s", artifact_path)