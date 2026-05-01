## [2026-04-29]
- Restored project from backup directory to primary repository.
- Updated `requirements.txt` to include `mlflow`, `scikit-learn`, and `pyyaml`.
- Modified `Dockerfile` to align with `docker.use_standard_style`.
- Initialized `helpers_root` submodule and verified `hdbg` integration.
- Confirmed MLflow functionality by running `mlflow_utils.py` inside the container and logging test parameters.

## [2026-04-30]
- Successfully added Kaggle House Prices dataset (train.csv, test.csv).
- Developed `data_loader.py` utilizing `helpers.hdbg` for file validation.
- Verified data integrity (1460 rows, 81 columns).
