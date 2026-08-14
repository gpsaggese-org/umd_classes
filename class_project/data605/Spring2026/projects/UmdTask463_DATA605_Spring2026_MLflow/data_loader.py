import pandas as pd
import logging
import os
import helpers.hdbg as hdbg

_LOG = logging.getLogger(__name__)

def load_ames_data(train: bool = True) -> pd.DataFrame:
    """
    Loads the Ames Housing data from the current directory.
    
    :param train: If True, loads train.csv; else loads test.csv.
    :return: A pandas DataFrame containing the data.
    """
    file_name = "train.csv" if train else "test.csv"
    
    # Verify the file exists before trying to read it
    hdbg.dassert_file_exists(file_name)
    
    _LOG.info("Loading %s...", file_name)
    df = pd.read_csv(file_name)
    
    # Check that we actually got data
    hdbg.dassert(not df.empty, "The loaded dataframe is empty!")
    
    _LOG.info("Successfully loaded %s with shape %s", file_name, df.shape)
    return df

if __name__ == "__main__":
    # This block only runs if you execute this file directly
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
    
    # Test loading the training data
    df_train = load_ames_data(train=True)
    
    # Verify 'SalePrice' exists in training data
    hdbg.dassert_in("SalePrice", df_train.columns)
    
    print("\n--- First 5 rows of Training Data ---")
    print(df_train.head())