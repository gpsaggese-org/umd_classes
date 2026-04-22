"""
Utility functions for YData-profiling tutorial.

Import as:

import src.ydata_profiling_utils as ydputi
"""

from pathlib import Path

import pandas as pd
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
    :param exploratory: Whether to use exploratory mode.
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