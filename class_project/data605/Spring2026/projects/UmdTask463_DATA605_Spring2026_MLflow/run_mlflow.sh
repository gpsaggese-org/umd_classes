#!/bin/bash
# Wipe temporary folder to ensure a clean slate
rm -rf /tmp/mlflow_data
mkdir -p /tmp/mlflow_data

# Start MLflow UI
mlflow ui \
  --host 0.0.0.0 \
  --backend-store-uri file:///tmp/mlflow_data \
  --allowed-hosts "*" \
  --cors-allowed-origins "*"