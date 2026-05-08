"""Utility functions for MLflow-based workflows.

Import as:
import class_project.DATA605.Spring2026.projects.UmdTask463_DATA605_Spring2026_MLflow.mlflow_utils as mltuti
"""

import logging
import sys
from contextlib import contextmanager

import mlflow
import mlflow.sklearn
import numpy as np
from sklearn.metrics import mean_squared_error

# Path inside the Docker container to find the 'helpers' library.
sys.path.append('/git_root')

try:
    import helpers.hdbg as hdbg
    _HELPERS = True
except ImportError:
    _HELPERS = False

_LOG = logging.getLogger(__name__)

###########################################################################
# MLflow Lifecycle Management
###########################################################################

@contextmanager
def start_mlflow_run(experiment_name: str, run_name: str = None):
    """Sets the experiment and starts a new MLflow run.

    :param experiment_name: Name of the MLflow experiment group
    :param run_name: Optional name for this specific execution run
    :yield: The active MLflow run object
    """
    if _HELPERS:
        hdbg.dassert_isinstance(experiment_name, str)
    
    mlflow.set_experiment(experiment_name)
    
    # Using 'with' here ensures the run closes even if an error occurs.
    with mlflow.start_run(run_name=run_name) as run:
        _LOG.info("Started MLflow run: %s in experiment: %s", run_name, experiment_name)
        yield run

###########################################################################
# Logging & Metrics
###########################################################################

def log_regression_metrics(y_true: np.ndarray, y_pred: np.ndarray):
    """Calculates and logs RMSE and MSE to the active MLflow run.

    :param y_true: Ground truth (correct) target values
    :param y_pred: Estimated target values from the model
    :return: None
    """
    mse = mean_squared_error(y_true, y_pred)
    rmse = np.sqrt(mse)
    
    mlflow.log_metric("mse", mse)
    mlflow.log_metric("rmse", rmse)
    
    _LOG.info("Logged metrics - RMSE: %.4f, MSE: %.4f", rmse, mse)

def save_model(model, artifact_path: str = "model"):
    """Serializes and logs a scikit-learn model to MLflow.

    :param model: The trained scikit-learn model object
    :param artifact_path: String path where model will be stored
    :return: None
    """
    mlflow.sklearn.log_model(model, artifact_path)
    _LOG.info("Model logged to artifact path: %s", artifact_path)