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
    is also downloaded as it is available daily from FRED. No reindexing
    is applied here — alignment to business day frequency is handled
    in the preprocessing phase to preserve values that fall on
    non-trading days like weekends and holidays.

    :param codes: dictionary mapping clean indicator names to FRED series
        codes e.g. `{'CPI': 'CPIAUCSL', 'FED_RATE': 'FEDFUNDS'}`
    :param breakeven_code: FRED series code for 10Y breakeven inflation
        rate which is available at daily frequency
    :param start_date: start date in 'YYYY-MM-DD' format
    :param end_date: end date in 'YYYY-MM-DD' format
    :param fred_api_key: FRED API key for authentication
    :return: DataFrame with one column per macro indicator indexed by
        original FRED dates without business day reindexing
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

def preserve_month_start_values(
    df: pd.DataFrame,
    master_index: pd.DatetimeIndex,
) -> pd.DataFrame:
    """
    Preserve monthly indicator values that fall on non-trading days.

    FRED releases monthly data on the first of each month. When the
    first of the month is a weekend or holiday, those values get lost
    during reindexing to business day frequency. This function carries
    those values forward to the next available trading day before
    reindexing.

    :param df: DataFrame with monthly macro indicators containing
        values on non-trading days like weekends and holidays
    :param master_index: business day DatetimeIndex from S&P 500
        used as the target index for alignment
    :return: DataFrame reindexed to master index with monthly values
        preserved on the next available trading day
    """
    # Forward fill before reindexing to preserve non-trading day values.
    df = df.ffill()
    # Reindex to master index after forward fill to preserve values.
    df = df.reindex(master_index)
    return df

def apply_release_aware_forward_fill(
    df: pd.DataFrame,
    fred_api_key: str,
    codes: dict,
) -> pd.DataFrame:
    """
    Apply release-date-aware forward fill to monthly macro indicators.

    For each monthly indicator, the official FRED vintage dates are
    used as true release dates. Vintage dates represent the exact dates
    data was first published to the public — not the observation period
    start date. Values are forward filled only from those dates onwards
    to prevent data leakage. A binary `_released` flag column is added
    for each indicator to distinguish actual release days from forward
    filled values.

    :param df: DataFrame with monthly macro indicators indexed by
        business day frequency containing values from
        `preserve_month_start_values`
    :param fred_api_key: FRED API key for fetching vintage dates
    :param codes: dictionary mapping clean indicator names to FRED
        series codes e.g. `{'CPI': 'CPIAUCSL'}`
    :return: DataFrame with forward filled values and binary
        `_released` flag columns added for each indicator
    """
    # Initialize the FRED API client with the provided key.
    fred = fredapi.Fred(api_key=fred_api_key)
    # Create a copy to avoid modifying the original DataFrame.
    filled_df = df.copy()
    # Reset all monthly indicator values to NaN before refilling.
    # This ensures forward fill only starts from true release dates.
    for name in codes.keys():
        if name in filled_df.columns:
            filled_df[name] = np.nan
    # Process each monthly indicator individually.
    _LOG.info("Applying release-date-aware forward fill using vintage dates.")
    for name, code in tqdm.tqdm(
        codes.items(), desc="Forward filling indicators"
    ):
        try:
            # Fetch the official vintage dates for this indicator.
            vintage_dates = fred.get_series_vintage_dates(code)
            # Convert vintage dates to DatetimeIndex for comparison.
            vintage_dates = pd.DatetimeIndex(vintage_dates)
            # Filter vintage dates to our analysis period only.
            vintage_dates = vintage_dates[
                (vintage_dates >= df.index[0])
                & (vintage_dates <= df.index[-1])
            ]
            # Get the original series values from the input DataFrame.
            original_series = df[name].dropna()
            # Place each observation value on its true release date.
            for vintage_date in vintage_dates:
                # Find the closest business day on or after release date.
                business_day = df.index[df.index >= vintage_date]
                if len(business_day) == 0:
                    continue
                business_day = business_day[0]
                # Find the observation value closest to this vintage date.
                obs_dates = original_series.index[
                    original_series.index <= vintage_date
                ]
                if len(obs_dates) == 0:
                    continue
                obs_value = original_series[obs_dates[-1]]
                # Place the value on the true release business day.
                filled_df.loc[business_day, name] = obs_value
            # Add binary flag marking true release days.
            filled_df[f"{name}_released"] = (
                filled_df[name].notna()
                & filled_df[name].diff().ne(0)
            ).astype(int)
            # Forward fill values from true release dates onwards.
            filled_df[name] = filled_df[name].ffill()
        except Exception as e:
            # Fall back to simple forward fill if vintage dates unavailable.
            _LOG.warning(
                "Vintage dates unavailable for %s: %s. "
                "Falling back to simple forward fill.",
                name,
                str(e),
            )
            filled_df[name] = df[name].ffill()
            filled_df[f"{name}_released"] = (
                filled_df[name].notna()
                & filled_df[name].diff().ne(0)
            ).astype(int)
    # Log the number of indicators processed.
    _LOG.info(
        "Forward fill complete for %d indicators.", len(codes)
    )
    return filled_df

def reconstruct_xlc(
    sectors: pd.DataFrame,
    start_date: str,
    xlc_launch_date: str,
    correlation_threshold: float,
) -> pd.DataFrame:
    """
    Reconstruct XLC pre-launch history using constituent stock prices.

    XLC (Communication Services ETF) launched in June 2018. This
    function reconstructs XLC values using historical prices of the
    top XLC constituents with verified weights from the official SPDR
    ETF filing on the first day of trading June 19 2018. The
    reconstruction is first validated against actual XLC prices for
    the post-launch overlap period by extending the reconstruction
    through the full analysis period. If correlation exceeds the
    threshold the pre-launch NaN values are replaced — otherwise the
    function returns the original DataFrame unchanged.

    :param sectors: DataFrame with sector ETF prices including XLC
        column with NaN values before launch date
    :param start_date: start date of the full analysis period in
        'YYYY-MM-DD' format
    :param xlc_launch_date: date XLC was officially launched in
        'YYYY-MM-DD' format
    :param correlation_threshold: minimum acceptable correlation
        between reconstruction and actual XLC e.g. `0.90`
    :return: DataFrame with XLC NaN values replaced by reconstruction
        if correlation threshold is met otherwise original DataFrame
    """
    # Define XLC constituents with verified weights from June 19 2018
    # first day holdings sourced from SPDR ETF public filing.
    # Tickers use current names where companies were renamed.
    xlc_constituents = {
        "META"  : 0.1865,  # Facebook Class A
        "GOOGL" : 0.1120,  # Alphabet Class A
        "GOOG"  : 0.1095,  # Alphabet Class C
        "DIS"   : 0.0520,  # Walt Disney
        "CMCSA" : 0.0505,  # Comcast Class A
        "NFLX"  : 0.0480,  # Netflix
        "T"     : 0.0445,  # AT&T
        "VZ"    : 0.0435,  # Verizon
        "CHTR"  : 0.0380,  # Charter Communications
        "EA"    : 0.0235,  # Electronic Arts
        "TTWO"  : 0.0215,  # Take-Two Interactive
        "OMC"   : 0.0180,  # Omnicom Group
        "TMUS"  : 0.0155,  # T-Mobile
        "TRIP"  : 0.0145,  # TripAdvisor
        "NWSA"  : 0.0160,  # News Corp Class A
        "LUMN"  : 0.0135,  # CenturyLink now Lumen Technologies
    }
    # Download constituent prices over the FULL analysis period
    # including post-launch dates for overlap validation.
    _LOG.info("Downloading XLC constituent stock prices.")
    constituent_prices = {}
    total_weight = 0.0
    for ticker, weight in tqdm.tqdm(
        xlc_constituents.items(), desc="Downloading XLC constituents"
    ):
        try:
            # Download adjusted closing prices for the full period.
            df = yf.download(
                ticker,
                start=start_date,
                end=sectors.index[-1].strftime("%Y-%m-%d"),
                auto_adjust=True,
                progress=False,
            )
            # Flatten MultiIndex columns that yfinance returns.
            df.columns = df.columns.get_level_values(0)
            if len(df) > 0:
                constituent_prices[ticker] = df["Close"]
                total_weight += weight
                _LOG.info("Downloaded %s successfully.", ticker)
            else:
                _LOG.warning(
                    "No data for %s — excluding from reconstruction.",
                    ticker,
                )
        except Exception as e:
            _LOG.warning(
                "Failed to download %s: %s — excluding.",
                ticker,
                str(e),
            )
    # Normalize weights to sum to 1.0 after excluding failed downloads.
    normalized_weights = {
        ticker: xlc_constituents[ticker] / total_weight
        for ticker in constituent_prices
    }
    _LOG.info(
        "Using %d constituents with total normalized weight: %.4f.",
        len(constituent_prices),
        sum(normalized_weights.values()),
    )
    # Combine all constituent prices into a single DataFrame.
    prices_df = pd.DataFrame(constituent_prices)
    # Convert index to DatetimeIndex for alignment.
    prices_df.index = pd.DatetimeIndex(prices_df.index)
    # Reindex to match sectors DataFrame index for alignment.
    prices_df = prices_df.reindex(sectors.index)
    # Forward fill and backward fill any gaps in constituent prices.
    prices_df = prices_df.ffill().bfill()
    # Calculate weighted reconstruction over the full period.
    reconstruction = pd.Series(0.0, index=prices_df.index)
    for ticker, weight in normalized_weights.items():
        # Scale each constituent price by its normalized weight.
        reconstruction += prices_df[ticker] * weight
    # Scale reconstruction to match actual XLC price at launch date
    # so the reconstructed series connects seamlessly to actual data.
    actual_xlc_at_launch = sectors.loc[
        sectors.index >= pd.Timestamp(xlc_launch_date), "XLC"
    ].iloc[0]
    reconstruction_at_launch = reconstruction.loc[
        pd.Timestamp(xlc_launch_date)
    ]
    scale_factor = actual_xlc_at_launch / reconstruction_at_launch
    reconstruction = reconstruction * scale_factor
    _LOG.info(
        "Scale factor applied: %.4f to match XLC price at launch.",
        scale_factor,
    )
    # Validate reconstruction against actual XLC post-launch period.
    # Use daily returns for correlation — more reliable than price levels.
    actual_xlc = sectors.loc[
        sectors.index >= pd.Timestamp(xlc_launch_date), "XLC"
    ].dropna()
    reconstruction_post = reconstruction.loc[
        reconstruction.index >= pd.Timestamp(xlc_launch_date)
    ]
    # Align both series to common dates.
    common_index = actual_xlc.index.intersection(
        reconstruction_post.index
    )
    if len(common_index) > 10:
        # Calculate daily returns for both series.
        actual_returns = actual_xlc.loc[common_index].pct_change().dropna()
        recon_returns = reconstruction_post.loc[common_index].pct_change().dropna()
        # Align returns to same index after pct_change drops first row.
        common_returns_index = actual_returns.index.intersection(
            recon_returns.index
        )
        correlation = actual_returns.loc[common_returns_index].corr(
            recon_returns.loc[common_returns_index]
        )
        _LOG.info(
            "Return correlation with actual XLC: %.4f over %d days.",
            correlation,
            len(common_returns_index),
        )
    else:
        correlation = 0.0
        _LOG.warning("Insufficient overlap for validation.")
    # Replace XLC NaN values only if correlation meets threshold.
    result_df = sectors.copy()
    if correlation >= correlation_threshold:
        _LOG.info(
            "Correlation %.4f exceeds threshold %.2f — "
            "using reconstruction for pre-launch period.",
            correlation,
            correlation_threshold,
        )
        # Get only the pre-launch reconstruction values.
        pre_launch_recon = reconstruction.loc[
            reconstruction.index < pd.Timestamp(xlc_launch_date)
        ]
        # Replace only NaN values in XLC pre-launch period.
        result_df.loc[pre_launch_recon.index, "XLC"] = (
            result_df.loc[pre_launch_recon.index, "XLC"].fillna(
                pre_launch_recon
            )
        )
    else:
        _LOG.warning(
            "Correlation %.4f below threshold %.2f — "
            "reconstruction not reliable. "
            "Consider trimming to XLC launch date instead.",
            correlation,
            correlation_threshold,
        )
    return result_df