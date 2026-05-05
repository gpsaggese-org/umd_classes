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
from contextlib import contextmanager

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

@contextmanager
def start_mlflow_run(experiment_name: str, run_name: str = None):
    """
    Sets the experiment and starts a new MLflow run using a context manager.
    Usage:
        with mltuti.start_mlflow_run("Exp", "Run1"):
            # code here
    """
    if _HELPERS:
        hdbg.dassert_isinstance(experiment_name, str)
    
    mlflow.set_experiment(experiment_name)
    
    # Using 'with' here ensures the run closes even if an error occurs
    with mlflow.start_run(run_name=run_name) as run:
        _LOG.info("Started MLflow run: %s in experiment: %s", run_name, experiment_name)
        yield run

# ### ####################################################################
# Logging & Metrics
# ### ####################################################################

def log_regression_metrics(y_true: np.ndarray, y_pred: np.ndarray):
    """Calculates and logs RMSE and MSE to the active MLflow run."""
    mse = mean_squared_error(y_true, y_pred)
    rmse = np.sqrt(mse)
    
    mlflow.log_metric("mse", mse)
    mlflow.log_metric("rmse", rmse)
    
    _LOG.info("Logged metrics - RMSE: %.4f, MSE: %.4f", rmse, mse)

def save_model(model, artifact_path: str = "model"):
    """Serializes and logs a scikit-learn model to MLflow."""
    mlflow.sklearn.log_model(model, artifact_path)
    _LOG.info("Model logged to artifact path: %s", artifact_path)