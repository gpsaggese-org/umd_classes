"""
Utility functions for S&P 500 market direction forecasting and intelligent
sector rotation using Darts.

This module contains all reusable helper functions for data download,
preprocessing, feature engineering, model training, evaluation, and
visualization. Functions are imported and called from `darts.example.ipynb`.
"""

import logging
import os

import fredapi
import numpy as np
import pandas as pd
import tqdm
import yfinance as yf

_LOG = logging.getLogger(__name__)

def download_sp500(
    ticker: str,
    start_date: str,
    end_date: str,
) -> pd.DataFrame:
    """
    Download S&P 500 historical price data from Yahoo Finance.

    The data is downloaded for the given date range and returned as a
    DataFrame with a DatetimeIndex. The `Close` column contains the
    daily closing price used for forecasting.

    :param ticker: Yahoo Finance ticker symbol for S&P 500 index
    :param start_date: start date in 'YYYY-MM-DD' format
    :param end_date: end date in 'YYYY-MM-DD' format
    :return: DataFrame with OHLCV columns indexed by date
    """
    # Download raw S&P 500 price data from Yahoo Finance.
    _LOG.info("Downloading S&P 500 data from %s to %s.", start_date, end_date)
    df = yf.download(
        ticker,
        start=start_date,
        end=end_date,
        auto_adjust=True,
        progress=False,
    )
    # Flatten the column MultiIndex that yfinance returns by default.
    df.columns = df.columns.get_level_values(0)
    # Convert the index to a DatetimeIndex for Darts compatibility.
    df.index = pd.DatetimeIndex(df.index)
    # Rename the index to Date for clarity.
    df.index.name = "Date"
    _LOG.info("Downloaded %d rows of S&P 500 data.", len(df))
    return df

def download_sectors(
    tickers: list,
    start_date: str,
    end_date: str,
) -> pd.DataFrame:
    """
    Download historical price data for all sector ETFs from Yahoo Finance.

    Each ticker is downloaded individually and the closing prices are
    combined into a single DataFrame where each column represents one
    sector ETF. A progress bar tracks the download of each ticker.

    :param tickers: list of sector ETF ticker symbols to download
    :param start_date: start date in 'YYYY-MM-DD' format
    :param end_date: end date in 'YYYY-MM-DD' format
    :return: DataFrame with one closing price column per sector ETF,
        indexed by date
    """
    # Initialize an empty dictionary to collect each sector's closing price.
    sector_data = {}
    # Download closing price for each sector ETF individually.
    _LOG.info("Downloading %d sector ETFs.", len(tickers))
    for ticker in tqdm.tqdm(tickers, desc="Downloading sectors"):
        # Download raw price data for the current ticker.
        df = yf.download(
            ticker,
            start=start_date,
            end=end_date,
            auto_adjust=True,
            progress=False,
        )
        # Flatten the MultiIndex columns that yfinance returns.
        df.columns = df.columns.get_level_values(0)
        # Store only the closing price column named after the ticker.
        sector_data[ticker] = df["Close"]
    # Combine all sector closing prices into a single DataFrame.
    sectors_df = pd.DataFrame(sector_data)
    # Convert the index to a DatetimeIndex for Darts compatibility.
    sectors_df.index = pd.DatetimeIndex(sectors_df.index)
    # Rename the index to Date for clarity.
    sectors_df.index.name = "Date"
    _LOG.info(
        "Downloaded %d rows for %d sectors.",
        len(sectors_df),
        len(tickers),
    )
    return sectors_df

def download_daily_macro(
    tickers: dict,
    start_date: str,
    end_date: str,
) -> pd.DataFrame:
    """
    Download daily macroeconomic indicators from Yahoo Finance.

    Each indicator is downloaded individually using its Yahoo Finance
    ticker symbol and combined into a single DataFrame. The columns are
    named using the clean indicator names defined in `tickers` dictionary
    rather than the raw Yahoo Finance symbols.

    :param tickers: dictionary mapping clean indicator names to Yahoo
        Finance ticker symbols, e.g. `{'VIX': '^VIX', 'OIL': 'CL=F'}`
    :param start_date: start date in 'YYYY-MM-DD' format
    :param end_date: end date in 'YYYY-MM-DD' format
    :return: DataFrame with one column per macro indicator indexed by date
    """
    # Initialize an empty dictionary to collect each indicator's data.
    macro_data = {}
    # Download closing price for each macro indicator individually.
    _LOG.info("Downloading %d daily macro indicators.", len(tickers))
    for name, symbol in tqdm.tqdm(
        tickers.items(), desc="Downloading daily macro"
    ):
        # Download raw price data for the current macro indicator.
        df = yf.download(
            symbol,
            start=start_date,
            end=end_date,
            auto_adjust=True,
            progress=False,
        )
        # Flatten the MultiIndex columns that yfinance returns.
        df.columns = df.columns.get_level_values(0)
        # Store only the closing price using the clean indicator name.
        macro_data[name] = df["Close"]
    # Combine all macro indicators into a single DataFrame.
    macro_df = pd.DataFrame(macro_data)
    # Convert the index to a DatetimeIndex for Darts compatibility.
    macro_df.index = pd.DatetimeIndex(macro_df.index)
    # Rename the index to Date for clarity.
    macro_df.index.name = "Date"
    _LOG.info(
        "Downloaded %d rows for %d daily macro indicators.",
        len(macro_df),
        len(tickers),
    )
    return macro_df

def download_monthly_macro(
    codes: dict,
    breakeven_code: str,
    start_date: str,
    end_date: str,
    fred_api_key: str,
) -> pd.DataFrame:
    """
    Download monthly macroeconomic indicators from the FRED API.

    Each indicator is downloaded individually using its FRED series code
    and combined into a single DataFrame. The 10Y breakeven inflation rate
    is also downloaded as it is available daily from FRED. All monthly
    indicators are forward filled to daily frequency after download to
    align with the daily S&P 500 price data.

    Note: Forward fill is applied only as a temporary alignment step here.
    Release-date-aware forward fill with binary `_released` flags is
    applied in the preprocessing phase to avoid data leakage.

    :param codes: dictionary mapping clean indicator names to FRED series
        codes, e.g. `{'CPI': 'CPIAUCSL', 'FED_RATE': 'FEDFUNDS'}`
    :param breakeven_code: FRED series code for 10Y breakeven inflation
        rate which is available at daily frequency
    :param start_date: start date in 'YYYY-MM-DD' format
    :param end_date: end date in 'YYYY-MM-DD' format
    :param fred_api_key: FRED API key for authentication
    :return: DataFrame with one column per macro indicator indexed by
        business day frequency
    """
    # Initialize the FRED API client with the provided key.
    fred = fredapi.Fred(api_key=fred_api_key)
    # Initialize an empty dictionary to collect each indicator's data.
    macro_data = {}
    # Download each monthly macro indicator from FRED individually.
    _LOG.info("Downloading %d monthly macro indicators from FRED.", len(codes))
    for name, code in tqdm.tqdm(
        codes.items(), desc="Downloading monthly macro"
    ):
        # Download the raw series data for the current indicator.
        series = fred.get_series(
            code,
            observation_start=start_date,
            observation_end=end_date,
        )
        # Store the series using the clean indicator name as the key.
        macro_data[name] = series
    # Download the daily breakeven inflation rate separately.
    _LOG.info("Downloading 10Y breakeven inflation from FRED.")
    macro_data["BREAKEVEN"] = fred.get_series(
        breakeven_code,
        observation_start=start_date,
        observation_end=end_date,
    )
    # Combine all indicators into a single DataFrame.
    macro_df = pd.DataFrame(macro_data)
    # Convert the index to a DatetimeIndex for Darts compatibility.
    macro_df.index = pd.DatetimeIndex(macro_df.index)
    # Rename the index to Date for clarity.
    macro_df.index.name = "Date"
    # Reindex to business day frequency to align with S&P 500 data.
    business_days = pd.bdate_range(start=start_date, end=end_date)
    macro_df = macro_df.reindex(business_days)
    # Rename the index to Date after reindexing.
    macro_df.index.name = "Date"
    _LOG.info(
        "Downloaded %d rows for %d monthly macro indicators.",
        len(macro_df),
        len(codes) + 1,
    )
    return macro_df

def save_data(
    df: pd.DataFrame,
    file_name: str,
    data_dir: str,
) -> None:
    """
    Save a DataFrame to a CSV file in the specified data directory.

    The file is saved with the index included so the date column is
    preserved when the file is read back. If the file already exists
    it is overwritten to ensure the saved data is always up to date.

    :param df: DataFrame to save to CSV
    :param file_name: name of the CSV file including `.csv` extension
    :param data_dir: path to the directory where the file is saved
    :return: None
    """
    # Build the full file path from the directory and file name.
    file_path = os.path.join(data_dir, file_name)
    # Save the DataFrame to CSV with the date index included.
    df.to_csv(file_path, index=True)
    _LOG.info("Saved %d rows to %s.", len(df), file_path)