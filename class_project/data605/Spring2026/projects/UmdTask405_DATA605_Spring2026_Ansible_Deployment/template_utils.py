"""
template_utils.py

This file contains utility functions that support the House Price Prediction
tutorial notebooks.

- Notebooks should call these functions instead of writing raw logic inline.
- This helps keep the notebooks clean, modular, and easier to debug.
- Functions cover data loading, preprocessing, model training, evaluation,
  and REST API interaction for the Kaggle House Prices regression task.

Import from the project root as:

import template_utils as cpptteut
"""

import logging
import os
import pickle
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
import pandas as pd
import requests
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

# -----------------------------------------------------------------------------
# Logging
# -----------------------------------------------------------------------------

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# -----------------------------------------------------------------------------
# Constants
# -----------------------------------------------------------------------------

# Features used for training and inference.
NUMERIC_FEATURES: List[str] = [
    "LotArea",
    "OverallQual",
    "OverallCond",
    "YearBuilt",
    "TotalBsmtSF",
    "GrLivArea",
    "FullBath",
    "BedroomAbvGr",
    "GarageCars",
    "GarageArea",
]
CATEGORICAL_FEATURES: List[str] = [
    "Neighborhood",
    "HouseStyle",
    "RoofStyle",
    "ExterQual",
    "KitchenQual",
]
ALL_FEATURES: List[str] = NUMERIC_FEATURES + CATEGORICAL_FEATURES
TARGET_COLUMN: str = "SalePrice"

# Default feature values used when a field is omitted from an API request.
FEATURE_DEFAULTS: Dict[str, Any] = {
    "LotArea": 9600,
    "OverallQual": 6,
    "OverallCond": 5,
    "YearBuilt": 2000,
    "TotalBsmtSF": 900,
    "GrLivArea": 1500,
    "FullBath": 2,
    "BedroomAbvGr": 3,
    "GarageCars": 2,
    "GarageArea": 480,
    "Neighborhood": "CollgCr",
    "HouseStyle": "1Story",
    "RoofStyle": "Gable",
    "ExterQual": "TA",
    "KitchenQual": "TA",
}

# Valid quality codes accepted by the API.
VALID_QUALITY_CODES: set = {"Ex", "Gd", "TA", "Fa", "Po"}

# Default path to the saved model artifact.
DEFAULT_MODEL_PATH: str = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "ml", "house_price_model.pkl"
)

# Default API base URL.
DEFAULT_API_URL: str = "http://localhost:5000"

# Candidate models compared in compare_models().
_CANDIDATE_MODELS: Dict[str, Any] = {
    "GradientBoosting": GradientBoostingRegressor(
        n_estimators=200, max_depth=4, learning_rate=0.05,
        subsample=0.8, random_state=42,
    ),
    "RandomForest": RandomForestRegressor(
        n_estimators=200, max_depth=8, random_state=42, n_jobs=-1,
    ),
    "Ridge": Ridge(alpha=100.0),
}


# -----------------------------------------------------------------------------
# Data loading
# -----------------------------------------------------------------------------


def load_data(data_path: str) -> pd.DataFrame:
    """
    Load the House Prices dataset from a CSV file.

    If the file does not exist, generate a synthetic dataset with realistic
    distributions so that the notebook can run end-to-end without Kaggle
    credentials.

    :param data_path: path to train.csv (Kaggle House Prices dataset)
    :return: DataFrame containing features and the SalePrice target column
    """
    if os.path.exists(data_path):
        logger.info("Loading dataset from '%s'.", data_path)
        df = pd.read_csv(data_path)
        # Keep only the columns required for this project.
        available = [c for c in ALL_FEATURES + [TARGET_COLUMN] if c in df.columns]
        return df[available]
    logger.warning("File '%s' not found – generating synthetic dataset.", data_path)
    return _generate_synthetic_data()


def _generate_synthetic_data(n: int = 1460) -> pd.DataFrame:
    """
    Generate a synthetic House Prices dataset when train.csv is unavailable.

    The distributions and sale-price formula approximate those of the real
    Kaggle dataset so that model metrics are representative.

    :param n: number of rows to generate
    :return: synthetic DataFrame with the same schema as the Kaggle dataset
    """
    rng = np.random.default_rng(42)
    neighborhoods = [
        "CollgCr", "Veenker", "Crawfor", "NoRidge",
        "Mitchel", "Somerst", "NWAmes", "OldTown", "BrkSide", "Sawyer",
    ]
    house_styles = ["1Story", "2Story", "1.5Fin", "SFoyer", "SLvl"]
    roof_styles  = ["Gable", "Hip", "Flat", "Gambrel", "Mansard"]
    qualities    = ["Ex", "Gd", "TA", "Fa", "Po"]
    qual_map     = {"Ex": 5, "Gd": 4, "TA": 3, "Fa": 2, "Po": 1}
    overall_qual = rng.integers(1, 11, n)
    gr_liv_area  = rng.integers(500, 4500, n)
    ext_qual     = rng.choice(qualities, n)
    kit_qual     = rng.choice(qualities, n)
    sale_price   = (
        50000
        + overall_qual * 8000
        + gr_liv_area  * 60
        + np.array([qual_map[q] for q in ext_qual]) * 5000
        + rng.normal(0, 15000, n)
    ).clip(50000, 800000).astype(int)
    return pd.DataFrame({
        "LotArea":      rng.integers(2000, 215000, n),
        "OverallQual":  overall_qual,
        "OverallCond":  rng.integers(1, 10, n),
        "YearBuilt":    rng.integers(1872, 2011, n),
        "TotalBsmtSF":  rng.integers(0, 6110, n),
        "GrLivArea":    gr_liv_area,
        "FullBath":     rng.integers(0, 4, n),
        "BedroomAbvGr": rng.integers(0, 8, n),
        "GarageCars":   rng.integers(0, 5, n),
        "GarageArea":   rng.integers(0, 1418, n),
        "Neighborhood": rng.choice(neighborhoods, n),
        "HouseStyle":   rng.choice(house_styles, n),
        "RoofStyle":    rng.choice(roof_styles, n),
        "ExterQual":    ext_qual,
        "KitchenQual":  kit_qual,
        "SalePrice":    sale_price,
    })


# -----------------------------------------------------------------------------
# Data splitting
# -----------------------------------------------------------------------------


def split_data(
    df: pd.DataFrame,
    target_column: str = TARGET_COLUMN,
    test_size: float = 0.2,
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    """
    Split the dataset into training and testing sets.

    :param df: full dataset including the target column
    :param target_column: name of the target column
    :param test_size: proportion of data to reserve for testing
    :return: X_train, X_test, y_train, y_test
    """
    logger.info("Splitting data into train and test sets.")
    X = df.drop(columns=[target_column])
    y = df[target_column]
    return train_test_split(X, y, test_size=test_size, random_state=42)


def load_test_data(test_data_path: str) -> Tuple[pd.DataFrame, pd.Series]:
    """
    Load test data from a CSV file and separate features from target.

    If the file does not exist, generate synthetic test data.

    :param test_data_path: path to test.csv (Kaggle House Prices test data)
    :return: (X_test, y_test) tuple with features and target values
    """
    if os.path.exists(test_data_path):
        logger.info("Loading test dataset from '%s'.", test_data_path)
        df = pd.read_csv(test_data_path)
        # Keep only the columns required for this project.
        available = [c for c in ALL_FEATURES + [TARGET_COLUMN] if c in df.columns]
        df = df[available]
    else:
        logger.warning("File '%s' not found – generating synthetic test data.", test_data_path)
        df = _generate_synthetic_data(n=500)
    
    X_test = df.drop(columns=[TARGET_COLUMN])
    y_test = df[TARGET_COLUMN]
    logger.info("Test set: %d rows", len(X_test))
    return X_test, y_test


# -----------------------------------------------------------------------------
# Example 2: PyCaret classification pipeline
# -----------------------------------------------------------------------------


def run_pycaret_classification(
    df: pd.DataFrame, target_column: str
) -> pd.DataFrame:
    """
    Run a basic PyCaret classification experiment.

    :param df: dataset containing features and target
    :param target_column: name of the target column

    :return: comparison of top-performing models
    """
    logger.info("Initializing PyCaret classification setup")
    ...

    logger.info("Comparing models")
    results = compare_models()
    ...

    return results

# -----------------------------------------------------------------------------
# Sklearn pipeline builder
# -----------------------------------------------------------------------------


def _build_pipeline(estimator: Any) -> Pipeline:
    """
    Wrap an estimator in a full preprocessing + regression pipeline.

    Numeric features are median-imputed and scaled. Categorical features are
    mode-imputed and one-hot encoded.

    :param estimator: sklearn-compatible regressor
    :return: fitted-ready Pipeline
    """
    numeric_transformer = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler",  StandardScaler()),
    ])
    categorical_transformer = Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("onehot",  OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
    ])
    preprocessor = ColumnTransformer([
        ("num", numeric_transformer,     NUMERIC_FEATURES),
        ("cat", categorical_transformer, CATEGORICAL_FEATURES),
    ])
    return Pipeline([
        ("preprocessor", preprocessor),
        ("regressor",    estimator),
    ])


# -----------------------------------------------------------------------------
# Model training and comparison
# -----------------------------------------------------------------------------


def compare_models(
    df: pd.DataFrame,
    target_column: str = TARGET_COLUMN,
    fold: int = 5,
) -> pd.DataFrame:
    """
    Cross-validate all candidate models and return a leaderboard DataFrame.

    Mirrors the PyCaret ``compare_models`` interface so notebooks need
    minimal changes. Candidates are GradientBoosting, RandomForest, Ridge.

    :param df: dataset containing features and the target column
    :param target_column: name of the target column
    :param fold: number of cross-validation folds
    :return: DataFrame with columns Model, RMSE, MAE, R2 sorted by RMSE
    """
    X = df.drop(columns=[target_column])[ALL_FEATURES]
    y = df[target_column]
    rows = []
    for name, estimator in _CANDIDATE_MODELS.items():
        logger.info("Cross-validating %s (%d folds)…", name, fold)
        pipeline = _build_pipeline(estimator)
        rmse_scores = np.sqrt(
            -cross_val_score(pipeline, X, y, cv=fold, scoring="neg_mean_squared_error")
        )
        mae_scores = -cross_val_score(pipeline, X, y, cv=fold, scoring="neg_mean_absolute_error")
        r2_scores  =  cross_val_score(pipeline, X, y, cv=fold, scoring="r2")
        rows.append({
            "Model": name,
            "RMSE":  round(rmse_scores.mean(), 2),
            "MAE":   round(mae_scores.mean(),  2),
            "R2":    round(r2_scores.mean(),   4),
        })
    leaderboard = (
        pd.DataFrame(rows)
        .sort_values("RMSE")
        .reset_index(drop=True)
    )
    logger.info("Leaderboard:\n%s", leaderboard.to_string(index=False))
    return leaderboard


def run_pycaret_regression(
    df: pd.DataFrame,
    n_select: int = 3,
    fold: int = 5,
    target_column: str = TARGET_COLUMN,
) -> Pipeline:
    """
    Run a PyCaret-style regression experiment: compare models and train the best.

    This is a convenience wrapper that:
    1. Runs cross-validation on all candidate models (compare_models)
    2. Selects the top performer by RMSE
    3. Trains the best model on the full dataset
    4. Stores the leaderboard for later retrieval via get_model_results()

    :param df: dataset containing features and target column
    :param n_select: (unused, for PyCaret compatibility) number of top models
    :param fold: number of cross-validation folds
    :param target_column: name of the target column
    :return: fitted sklearn Pipeline for the best model
    """
    global _model_leaderboard, _best_model_pipeline

    # Run comparison and get leaderboard
    leaderboard = compare_models(df, target_column=target_column, fold=fold)
    _model_leaderboard = leaderboard

    # Train the best model (top row after sorting by RMSE)
    best_model_name = leaderboard.iloc[0]["Model"]
    logger.info("Training best model: %s", best_model_name)
    best_pipeline = train_best_model(df, target_column=target_column, model_name=best_model_name)
    _best_model_pipeline = best_pipeline

    return best_pipeline


def get_model_results() -> pd.DataFrame:
    """
    Retrieve the leaderboard from the last run_pycaret_regression() call.

    :return: DataFrame with columns Model, RMSE, MAE, R2 sorted by RMSE
    :raises RuntimeError: if run_pycaret_regression() has not been called yet
    """
    if _model_leaderboard is None:
        raise RuntimeError(
            "No model results available. Call run_pycaret_regression() first."
        )
    return _model_leaderboard


def train_best_model(
    df: pd.DataFrame,
    target_column: str = TARGET_COLUMN,
    model_name: str = "GradientBoosting",
) -> Pipeline:
    """
    Train the chosen model on the full dataset and return the fitted pipeline.

    :param df: full dataset including the target column
    :param target_column: name of the target column
    :param model_name: key from _CANDIDATE_MODELS to use
    :return: fitted sklearn Pipeline
    """
    if model_name not in _CANDIDATE_MODELS:
        raise ValueError(
            f"Unknown model '{model_name}'. "
            f"Choose from: {list(_CANDIDATE_MODELS.keys())}"
        )
    X = df.drop(columns=[target_column])[ALL_FEATURES]
    y = df[target_column]
    logger.info("Training %s on full dataset (%d rows)…", model_name, len(df))
    pipeline = _build_pipeline(_CANDIDATE_MODELS[model_name])
    pipeline.fit(X, y)
    return pipeline


def evaluate_model(
    pipeline: Pipeline,
    X_test: pd.DataFrame,
    y_test: pd.Series,
) -> Dict[str, float]:
    """
    Evaluate a fitted pipeline on a held-out test set.

    :param pipeline: fitted sklearn Pipeline
    :param X_test: test features
    :param y_test: true target values
    :return: dict with keys RMSE, MAE, R2
    """
    preds = pipeline.predict(X_test[ALL_FEATURES])
    metrics = {
        "RMSE": round(float(np.sqrt(mean_squared_error(y_test, preds))), 2),
        "MAE":  round(float(mean_absolute_error(y_test, preds)),         2),
        "R2":   round(float(r2_score(y_test, preds)),                    4),
    }
    logger.info("Test metrics: %s", metrics)
    return metrics


# -----------------------------------------------------------------------------
# Model persistence
# -----------------------------------------------------------------------------


def finalize_and_save(
    pipeline: Pipeline,
    model_path: str = DEFAULT_MODEL_PATH,
) -> None:
    """
    Save the fitted pipeline to disk as a pickle file.

    :param pipeline: fitted sklearn Pipeline to persist
    :param model_path: full destination path including the .pkl extension
    :return: None
    """
    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    with open(model_path, "wb") as fh:
        pickle.dump(pipeline, fh)
    logger.info("Model saved to '%s'.", model_path)


def load_model_artifact(model_path: str = DEFAULT_MODEL_PATH) -> Pipeline:
    """
    Load a saved sklearn pipeline from disk.

    :param model_path: path to the .pkl file
    :return: loaded sklearn Pipeline
    """
    if not os.path.exists(model_path):
        raise FileNotFoundError(
            f"Model not found at '{model_path}'. "
            "Run train_best_model() and finalize_and_save() first."
        )
    logger.info("Loading model from '%s'.", model_path)
    with open(model_path, "rb") as fh:
        return pickle.load(fh)


# -----------------------------------------------------------------------------
# Inference
# -----------------------------------------------------------------------------


def predict_price(
    payload: Dict[str, Any],
    model: Optional[Pipeline] = None,
    model_path: str = DEFAULT_MODEL_PATH,
) -> float:
    """
    Predict the sale price for a single house.

    Missing feature values are filled with FEATURE_DEFAULTS before inference
    so callers only need to supply the fields they care about.

    :param payload: dict of feature name → value pairs
    :param model: pre-loaded pipeline; loaded from disk if None
    :param model_path: path used when model is None
    :return: predicted sale price in USD
    """
    if model is None:
        model = load_model_artifact(model_path)
    row = {**FEATURE_DEFAULTS, **payload}
    df  = pd.DataFrame([row])[ALL_FEATURES]
    return round(float(model.predict(df)[0]), 2)


# -----------------------------------------------------------------------------
# Feature validation
# -----------------------------------------------------------------------------


def validate_features(payload: Dict[str, Any]) -> List[str]:
    """
    Validate a prediction request payload and return a list of error strings.

    An empty list means the payload is valid.

    :param payload: dict of feature name → value pairs
    :return: list of human-readable validation error messages
    """
    errors: List[str] = []
    for field in ("OverallQual", "OverallCond"):
        val = payload.get(field)
        if val is not None and not (1 <= float(val) <= 10):
            errors.append(f"{field} must be between 1 and 10 (got {val}).")
    if "GrLivArea" in payload and float(payload["GrLivArea"]) <= 0:
        errors.append("GrLivArea must be greater than 0.")
    for field in ("ExterQual", "KitchenQual"):
        val = payload.get(field)
        if val is not None and val not in VALID_QUALITY_CODES:
            errors.append(
                f"{field} must be one of {sorted(VALID_QUALITY_CODES)}"
                f" (got '{val}')."
            )
    return errors


# -----------------------------------------------------------------------------
# REST API helpers (call the live Flask server from a notebook)
# -----------------------------------------------------------------------------


def api_health(base_url: str = DEFAULT_API_URL) -> Dict[str, Any]:
    """
    Call the /health endpoint of the running prediction API.

    :param base_url: base URL of the Flask API
    :return: parsed JSON response dict
    """
    resp = requests.get(f"{base_url}/health", timeout=5)
    resp.raise_for_status()
    return resp.json()


def api_predict(
    payload: Dict[str, Any],
    base_url: str = DEFAULT_API_URL,
) -> Dict[str, Any]:
    """
    POST a single prediction request to the running API.

    Example usage in a notebook::

        result = cpptteut.api_predict({"OverallQual": 8, "GrLivArea": 2200})
        print(result["predicted_price"])

    :param payload: dict of feature name → value pairs (all fields optional)
    :param base_url: base URL of the Flask API
    :return: parsed JSON response dict containing predicted_price
    """
    resp = requests.post(f"{base_url}/predict", json=payload, timeout=10)
    resp.raise_for_status()
    return resp.json()


def api_predict_batch(
    instances: List[Dict[str, Any]],
    base_url: str = DEFAULT_API_URL,
) -> Dict[str, Any]:
    """
    POST a batch of prediction requests to the running API.

    :param instances: list of feature dicts, one per house
    :param base_url: base URL of the Flask API
    :return: parsed JSON response dict containing a predictions list
    """
    resp = requests.post(
        f"{base_url}/predict/batch",
        json={"instances": instances},
        timeout=10,
    )
    resp.raise_for_status()
    return resp.json()