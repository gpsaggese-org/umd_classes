#!/bin/bash
# Start MLflow UI with the correct paths and permissions
mlflow ui \
  --host 0.0.0.0 \
  --backend-store-uri file:///project/mlruns \
  --allowed-hosts "*" \
  --cors-allowed-origins "*"
