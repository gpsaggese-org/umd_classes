"""
causalnex_utils.py

This file contains utility functions that support the causalnex tutorial
notebooks.

Import as:

import tutorials.causalnex.causalnex_utils as tcacauti
"""

import logging
import os
import urllib.request
import zipfile

import pandas as pd

import helpers.hdbg as hdbg
import helpers.hnotebook as hnotebo

_LOG = logging.getLogger(__name__)


def init_loggers(notebook_log: logging.Logger) -> None:
    global _LOG
    hnotebo.init_loggers(notebook_log, utils_log=_LOG)


# #############################################################################
# Download and load student performance dataset
# #############################################################################


def _download_file(url: str, *, output_path: str) -> None:
    """
    Download a file from the given URL if it doesn't already exist.

    :param url: URL of the file to download
    :param output_path: Local path where the file should be saved
    """
    if os.path.exists(output_path):
        _LOG.info("File already exists at '%s', skipping download", output_path)
        return
    _LOG.info("Downloading file from '%s' to '%s'", url, output_path)
    urllib.request.urlretrieve(url, output_path)
    _LOG.info("Download complete")


def _decompress_zip(zip_path: str, *, extract_dir: str) -> None:
    """
    Decompress a zip file to the specified directory.

    :param zip_path: Path to the zip file
    :param extract_dir: Directory where the zip file should be extracted
    """
    hdbg.dassert_file_exists(zip_path, "Zip file does not exist")
    _LOG.info("Extracting zip file from '%s' to '%s'", zip_path, extract_dir)
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(extract_dir)
    _LOG.info("Extraction complete")


def load_student_performance_data(*, data_dir: str = "data") -> pd.DataFrame:
    """
    Download and load the student performance dataset from UCI.

    Downloads the student performance dataset if it doesn't exist locally,
    decompresses the zip file, and loads the CSV data into a DataFrame.

    :param data_dir: Directory where the dataset will be stored
        - Default: `"data"`
    :return: DataFrame containing the student performance data
    """
    if not os.path.isabs(data_dir):
        module_dir = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.join(module_dir, data_dir)
    os.makedirs(data_dir, exist_ok=True)
    url = "https://archive.ics.uci.edu/static/public/320/student+performance.zip"
    zip_path = os.path.join(data_dir, "student_performance.zip")
    extract_dir = os.path.join(data_dir, "student_performance")
    _download_file(url, output_path=zip_path)
    if not os.path.exists(extract_dir):
        _decompress_zip(zip_path, extract_dir=extract_dir)
    csv_path = os.path.join(extract_dir, "student-mat.csv")
    if not os.path.exists(csv_path):
        nested_zip_path = os.path.join(extract_dir, "student.zip")
        if os.path.exists(nested_zip_path):
            _decompress_zip(nested_zip_path, extract_dir=extract_dir)
    _LOG.info("Loading student performance data from '%s'", csv_path)
    df = pd.read_csv(csv_path, sep=";")
    _LOG.info("Data loaded: %s rows, %s columns", len(df), len(df.columns))
    return df
