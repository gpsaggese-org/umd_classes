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
import mlflow_utils as mltuti
import mlflow

# Start a test experiment
with mltuti.start_mlflow_run("Verification Test"):
    
    # Log a dummy parameter
    mlflow.log_param("test_mode", "manual_verification")
    
    # Log a dummy metric
    mlflow.log_metric("fake_rmse", 0.5)
    
    print("Verification run completed.")

# %%
# Pull data from 'mlruns' folder
current_experiment = mlflow.get_experiment_by_name("Verification Test")

if current_experiment:
    print(f"✅ Success! Experiment ID: {current_experiment.experiment_id}")
    print(f"Storage Location: {current_experiment.artifact_location}")
    
    runs = mlflow.search_runs(experiment_ids=[current_experiment.experiment_id])
    print("\nRecent Runs:")
    print(runs[['params.test_mode', 'metrics.fake_rmse', 'status']])
else:
    print("❌ Experiment not found. Check your mlflow_utils.py pathing.")

# %%
