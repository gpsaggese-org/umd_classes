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

# %% [markdown]
# # MLflow API Overview
#
# This notebook provides a hands-on walkthrough of the core MLflow API components: **Experiments**, **Runs**, and **Logging**. MLflow is a platform for managing the machine learning lifecycle, primarily used for tracking how different versions of models perform.

# %%
# %load_ext autoreload
# %autoreload 2

import os
import logging
import mlflow
import mlflow_utils as mltuti

# Ensure custom tracking directory exists
tracking_path = "/tmp/mlflow_data"
if not os.path.exists(tracking_path):
    os.makedirs(tracking_path)

# Set the tracking URI
mlflow.set_tracking_uri(f"file://{tracking_path}")

# Configure logging
logging.basicConfig(level=logging.INFO)
_LOG = logging.getLogger(__name__)

print(f"Tracking URI: {mlflow.get_tracking_uri()}")

# %% [markdown]
# ## Tracking Experiments
#
# Experiments are the highest level of organization in MLflow. Every time you try a new idea, you record it as a **Run** inside an **Experiment**.

# %%
# Start a test experiment
with mltuti.start_mlflow_run("Verification Test"):
    
    # Log a dummy parameter (input)
    mlflow.log_param("test_mode", "manual_verification")
    
    # Log a dummy metric (output)
    mlflow.log_metric("fake_rmse", 0.5)
    
    print("Verification run completed.")
