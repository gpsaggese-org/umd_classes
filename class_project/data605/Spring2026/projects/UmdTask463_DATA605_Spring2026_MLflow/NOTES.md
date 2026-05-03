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

## [2026-05-01]
- Fixed docker working directory.
- Removed outliers where GrLivArea > 4000.
- Applied log transformation to SalePrice to address skewness.
- Created df_no_outliers and saved progress to train_clean.csv.

## [2026-05-02]
- Finalized EDA by imputing missing values and one-hot encoding categorical values.
- Saved final model-ready data to train_clean.csv.
- Updated mlflow_utils.py to handle experiment lifecycle, metrics logging, and model artifact serialization.
- Implemented mlflow.API.ipynb and tested by logging test parameters and metrics.
- Configured Jupytext pairing for all notebooks.