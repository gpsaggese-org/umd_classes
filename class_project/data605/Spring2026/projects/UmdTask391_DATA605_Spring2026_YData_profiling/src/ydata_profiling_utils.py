"""
Utility functions for YData-profiling tutorial.

Import as:

import src.ydata_profiling_utils as ydputi
"""

from pathlib import Path

import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from ydata_profiling import ProfileReport


def get_project_root() -> Path:
    """
    Return the project root directory.

    :return: Path to the project root.
    """
    return Path(__file__).resolve().parents[1]


def load_baltimore_data() -> pd.DataFrame:
    """
    Load the Baltimore housing dataset.

    :return: Loaded pandas DataFrame.
    """
    data_path = get_project_root() / "data" / "baltim.csv"
    df = pd.read_csv(data_path)
    return df


def print_basic_info(df: pd.DataFrame) -> None:
    """
    Print basic dataset information.

    :param df: Input DataFrame.
    :return: None.
    """
    print("Data shape:", df.shape)
    print("\nColumns:")
    print(df.columns.tolist())
    print("\nFirst 5 rows:")
    print(df.head())


def create_profile_report(
    df: pd.DataFrame,
    title: str = "Baltimore Housing Data Profiling Report",
    explorative: bool = True,
) -> ProfileReport:
    """
    Create a YData-profiling report.

    :param df: Input DataFrame.
    :param title: Report title.
    :param explorative: Whether to use explorative mode.
    :return: ProfileReport object.
    """
    profile = ProfileReport(
        df,
        title=title,
        explorative=explorative,
    )
    return profile


def save_profile_report(
    profile: ProfileReport,
    output_filename: str = "baltim_profile_report.html",
) -> Path:
    """
    Save the profile report to the outputs directory.

    :param profile: ProfileReport object.
    :param output_filename: Output HTML file name.
    :return: Path to the saved report.
    """
    output_path = get_project_root() / "outputs" / output_filename
    output_path.parent.mkdir(parents=True, exist_ok=True)
    profile.to_file(output_path)
    return output_path


def clean_baltimore_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the Baltimore housing dataset for modeling.

    The cleaning step removes duplicate rows and keeps numeric columns that can
    be used for regression modeling.

    :param df: Raw input DataFrame.
    :return: Cleaned DataFrame.
    """
    df_clean = df.copy()
    df_clean = df_clean.drop_duplicates()
    df_clean = df_clean.select_dtypes(include="number")
    return df_clean


def prepare_regression_data(
    df: pd.DataFrame,
    target_col: str = "PRICE",
) -> tuple[pd.DataFrame, pd.Series]:
    """
    Prepare feature matrix and target vector for regression.

    :param df: Cleaned input DataFrame.
    :param target_col: Name of the target variable.
    :return: Feature matrix X and target vector y.
    """
    if target_col not in df.columns:
        raise ValueError(
            f"Target column '{target_col}' was not found. "
            f"Available columns are: {df.columns.tolist()}"
        )

    df_model = df.dropna(subset=[target_col]).copy()
    X = df_model.drop(columns=[target_col])
    y = df_model[target_col]
    return X, y


def train_regression_model(
    X: pd.DataFrame,
    y: pd.Series,
    test_size: float = 0.2,
    random_state: int = 42,
) -> tuple[RandomForestRegressor, pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    """
    Train a Random Forest regression model.

    Missing feature values are filled with median values before training.

    :param X: Feature matrix.
    :param y: Target vector.
    :param test_size: Fraction of data used for testing.
    :param random_state: Random seed for reproducibility.
    :return: Trained model, X_train, X_test, y_train, and y_test.
    """
    imputer = SimpleImputer(strategy="median")
    X_imputed = pd.DataFrame(
        imputer.fit_transform(X),
        columns=X.columns,
        index=X.index,
    )

    X_train, X_test, y_train, y_test = train_test_split(
        X_imputed,
        y,
        test_size=test_size,
        random_state=random_state,
    )

    model = RandomForestRegressor(
        n_estimators=100,
        random_state=random_state,
    )
    model.fit(X_train, y_train)

    return model, X_train, X_test, y_train, y_test


def evaluate_regression_model(
    model: RandomForestRegressor,
    X_test: pd.DataFrame,
    y_test: pd.Series,
) -> dict[str, float]:
    """
    Evaluate a regression model using RMSE and R-squared.

    :param model: Trained regression model.
    :param X_test: Test feature matrix.
    :param y_test: Test target vector.
    :return: Dictionary with RMSE and R-squared values.
    """
    y_pred = model.predict(X_test)

    mse = mean_squared_error(y_test, y_pred)
    rmse = mse ** 0.5
    r2 = r2_score(y_test, y_pred)

    metrics = {
        "RMSE": rmse,
        "R2": r2,
    }
    return metrics