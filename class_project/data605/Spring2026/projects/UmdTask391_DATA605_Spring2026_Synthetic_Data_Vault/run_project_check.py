"""
Simple project check for the SDV privacy classification project.

This script verifies that the main required libraries are installed and that
the project folder contains the expected files.
"""

from pathlib import Path

import pandas as pd
import sklearn
import sdv
import sdmetrics


def main():
    project_root = Path(__file__).resolve().parent

    expected_files = [
        "README.md",
        "requirements.txt",
        "notebooks/Synthetic_Data_Vault.ipynb",
        "notebooks/synthetic_data_vault.API.ipynb",
        "outputs/model_comparison_results.csv",
        "outputs/final_model_comparison_results.csv",
        "synthetic_data_vault_utils.py",
    ]

    print("Checking required project files...")

    missing_files = []
    for file_path in expected_files:
        full_path = project_root / file_path
        if full_path.exists():
            print(f"FOUND: {file_path}")
        else:
            print(f"MISSING: {file_path}")
            missing_files.append(file_path)

    if missing_files:
        raise FileNotFoundError(f"Missing required files: {missing_files}")

    print("\nChecking output results...")
    results_path = project_root / "outputs" / "final_model_comparison_results.csv"
    results_df = pd.read_csv(results_path)

    print(results_df.head())
    print(f"\nRows in final results file: {len(results_df)}")

    print("\nLibrary imports successful:")
    print(f"pandas: {pd.__version__}")
    print(f"scikit-learn: {sklearn.__version__}")

    print("\nProject check completed successfully.")


if __name__ == "__main__":
    main()
