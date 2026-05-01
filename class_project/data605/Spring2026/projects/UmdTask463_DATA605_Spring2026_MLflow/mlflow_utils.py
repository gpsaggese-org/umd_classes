import logging
import sys
import os
import mlflow

# Path inside the Docker container
sys.path.append('/git_root')

try:
    import helpers.hdbg as hdbg
    _HELPERS = True
except ImportError:
    _HELPERS = False

_LOG = logging.getLogger(__name__)

def start_mlflow_run(experiment_name: str):
    if _HELPERS:
        hdbg.dassert_isinstance(experiment_name, str)
        hdbg.dassert(len(experiment_name) > 0, "Experiment name cannot be empty")

    _LOG.info("Starting MLflow experiment: %s", experiment_name)
    mlflow.set_experiment(experiment_name)
    return mlflow.start_run()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
    
    if not _HELPERS:
        print("❌ Error: helpers_root not found in /git_root")
    
    try:
        with start_mlflow_run("Housing_Price_Test"):
            mlflow.log_param("status", "successfully_initialized")
            _LOG.info("Successfully logged parameter to MLflow.")
    except Exception as e:
        _LOG.error("Failed to start MLflow: %s", e)
