"""
Utility functions for S&P 500 market direction forecasting and intelligent
sector rotation using Darts.

This module contains all reusable helper functions for data download,
preprocessing, feature engineering, model training, evaluation, and
visualization. Functions are imported and called from `darts.example.ipynb`.
"""

import logging
import os

import darts.dataprocessing.transformers
import darts.timeseries
import fredapi
import holidays
import matplotlib.pyplot as plt
import numpy as np
import optuna
import pandas as pd
import seaborn as sns
import shap
import sklearn.ensemble
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

def load_data(
    file_name: str,
    data_dir: str,
) -> pd.DataFrame:
    """
    Load a DataFrame from a CSV file in the specified data directory.

    The date column is parsed as a DatetimeIndex automatically. This
    function is used to load previously downloaded or processed data
    instead of re-downloading from external APIs on every notebook run.
    Using saved CSV files makes the notebook idempotent and eliminates
    unnecessary API calls on every kernel restart.

    :param file_name: name of the CSV file including `.csv` extension
    :param data_dir: path to the directory where the file is saved
    :return: DataFrame with DatetimeIndex loaded from CSV file
    """
    # Build the full file path from the directory and file name.
    file_path = os.path.join(data_dir, file_name)
    # Load the CSV file with the Date column parsed as DatetimeIndex.
    df = pd.read_csv(file_path, index_col="Date", parse_dates=True)
    # Convert index to DatetimeIndex for Darts compatibility.
    df.index = pd.DatetimeIndex(df.index)
    _LOG.info("Loaded %d rows from %s.", len(df), file_path)
    return df

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

def plot_sp500_history(
    sp500: pd.DataFrame,
    ax: plt.Axes = None,
) -> plt.Figure:
    """
    Plot S&P 500 price history and daily returns in a single figure.

    Two subplots are created — the top panel shows the closing price
    over time and the bottom panel shows the daily percentage returns.
    This gives a clear picture of both the price trend and the
    volatility pattern over the analysis period.

    :param sp500: DataFrame with S&P 500 OHLCV data indexed by date
    :param ax: optional matplotlib Axes object for embedding in a
        larger figure — if None a new figure is created
    :return: matplotlib Figure object with both subplots
    """
    # Calculate daily percentage returns from closing prices.
    returns = sp500["Close"].pct_change().dropna() * 100
    # Create a figure with two vertically stacked subplots.
    fig, axes = plt.subplots(2, 1, figsize=(14, 8))
    # Plot closing price on the top subplot.
    axes[0].plot(
        sp500.index,
        sp500["Close"],
        color="steelblue",
        linewidth=1.2,
        label="S&P 500 Close",
    )
    axes[0].set_title(
        "S&P 500 Closing Price 2018-2024",
        fontsize=13,
        fontweight="bold",
    )
    axes[0].set_ylabel("Price (USD)")
    axes[0].set_xlabel("")
    axes[0].legend(loc="upper left", fontsize=9)
    # Plot daily returns on the bottom subplot.
    axes[1].bar(
        returns.index,
        returns.values,
        color=["crimson" if r < 0 else "steelblue" for r in returns],
        width=1.0,
        alpha=0.7,
        label="Daily Return %",
    )
    axes[1].axhline(0, color="black", linewidth=0.8, linestyle="--")
    axes[1].set_title(
        "S&P 500 Daily Returns 2018-2024",
        fontsize=13,
        fontweight="bold",
    )
    axes[1].set_ylabel("Return (%)")
    axes[1].set_xlabel("Date")
    axes[1].legend(loc="upper left", fontsize=9)
    fig.tight_layout()
    return fig

def plot_sector_performance(
    sectors: pd.DataFrame,
    sector_names: dict,
    ax: plt.Axes = None,
) -> plt.Figure:
    """
    Plot sector ETF performance using a heatmap and bar chart.

    Two visualizations are created — a heatmap showing annual returns
    per sector per year and a horizontal bar chart showing total
    return over the full period ranked from best to worst. This
    layout clearly shows which sectors led and lagged each year
    and over the full analysis period.

    :param sectors: DataFrame with sector ETF closing prices indexed
        by date with one column per sector ticker
    :param sector_names: dictionary mapping ticker symbols to full
        sector names e.g. `{'XLK': 'Technology'}`
    :param ax: optional matplotlib Axes object for embedding in a
        larger figure — if None a new figure is created
    :return: matplotlib Figure object with heatmap and bar chart
    """
    # Calculate annual returns for each sector.
    annual_returns = sectors.resample("YE").last().pct_change() * 100
    # Drop the first row which is NaN after pct_change.
    annual_returns = annual_returns.dropna()
    # Rename columns to full sector names for readability.
    annual_returns.columns = [
        sector_names.get(col, col) for col in annual_returns.columns
    ]
    # Format index to show year only.
    annual_returns.index = annual_returns.index.year
    # Calculate total return over full period for bar chart.
    total_returns = (
        (sectors.iloc[-1] / sectors.iloc[0] - 1) * 100
    )
    # Rename total returns index to full sector names.
    total_returns.index = [
        sector_names.get(col, col) for col in total_returns.index
    ]
    # Sort total returns from highest to lowest.
    total_returns = total_returns.sort_values(ascending=True)
    # Create figure with two subplots side by side.
    fig, axes = plt.subplots(1, 2, figsize=(20, 7))
    # Plot annual returns heatmap on the left subplot.
    sns.heatmap(
        annual_returns.T,
        annot=True,
        fmt=".1f",
        cmap="RdYlGn",
        center=0,
        linewidths=0.5,
        linecolor="white",
        ax=axes[0],
        cbar_kws={"label": "Annual Return (%)"},
    )
    axes[0].set_title(
        "Sector Annual Returns by Year (%)",
        fontsize=13,
        fontweight="bold",
    )
    axes[0].set_xlabel("Year")
    axes[0].set_ylabel("Sector")
    # Plot total returns horizontal bar chart on right subplot.
    colors = [
        "crimson" if r < 0 else "steelblue"
        for r in total_returns.values
    ]
    axes[1].barh(
        total_returns.index,
        total_returns.values,
        color=colors,
        edgecolor="white",
        height=0.6,
    )
    axes[1].axvline(0, color="black", linewidth=0.8, linestyle="--")
    # Add value labels on each bar.
    for idx, val in enumerate(total_returns.values):
        axes[1].text(
            val + (2 if val >= 0 else -2),
            idx,
            f"{val:.1f}%",
            va="center",
            ha="left" if val >= 0 else "right",
            fontsize=9,
            fontweight="bold",
        )
    axes[1].set_title(
        "Total Return by Sector 2018-2024 (%)",
        fontsize=13,
        fontweight="bold",
    )
    axes[1].set_xlabel("Total Return (%)")
    axes[1].set_ylabel("")
    fig.tight_layout()
    return fig

def plot_macro_trends(
    macro_daily: pd.DataFrame,
    macro_monthly: pd.DataFrame,
) -> plt.Figure:
    """
    Plot key macroeconomic indicator trends over the analysis period.

    Two separate figures are created — one for daily indicators and
    one for monthly indicators. Each figure uses subplots to show
    each indicator individually with its own scale so trends are
    clearly visible without compression from different value ranges.

    :param macro_daily: DataFrame with daily macro indicators indexed
        by date including VIX, yields, oil, gold, and DXY
    :param macro_monthly: DataFrame with monthly macro indicators
        indexed by date including CPI, Fed rate, and unemployment
    :return: matplotlib Figure object with all macro trend subplots
    """
    # Define which daily indicators to plot with their display names.
    daily_indicators = {
        "VIX"       : "VIX (Fear Index)",
        "TNX"       : "10Y Treasury Yield (%)",
        "IRX"       : "2Y Treasury Yield (%)",
        "OIL"       : "Oil Price WTI (USD)",
        "GOLD"      : "Gold Price (USD)",
        "DXY"       : "Dollar Index (DXY)",
    }
    # Define which monthly indicators to plot with display names.
    monthly_indicators = {
        "CPI"           : "CPI Inflation",
        "FED_RATE"      : "Fed Funds Rate (%)",
        "UNEMPLOYMENT"  : "Unemployment Rate (%)",
        "NFP"           : "Non-Farm Payrolls (K)",
    }
    # Create figure for daily macro indicators with 6 subplots.
    fig, axes = plt.subplots(3, 2, figsize=(16, 12))
    axes = axes.flatten()
    # Plot each daily indicator in its own subplot.
    for idx, (col, title) in enumerate(daily_indicators.items()):
        axes[idx].plot(
            macro_daily.index,
            macro_daily[col],
            color="steelblue",
            linewidth=1.2,
        )
        axes[idx].set_title(title, fontsize=11, fontweight="bold")
        axes[idx].set_ylabel("Value")
        axes[idx].set_xlabel("Date")
        # Add shaded region for COVID crash period.
        axes[idx].axvspan(
            pd.Timestamp("2020-02-01"),
            pd.Timestamp("2020-06-01"),
            alpha=0.1,
            color="red",
            label="COVID crash",
        )
        # Add shaded region for rate hiking cycle.
        axes[idx].axvspan(
            pd.Timestamp("2022-03-01"),
            pd.Timestamp("2023-07-01"),
            alpha=0.1,
            color="orange",
            label="Rate hike cycle",
        )
        axes[idx].legend(fontsize=7, loc="upper left")
    fig.suptitle(
        "Daily Macroeconomic Indicators 2018-2024",
        fontsize=14,
        fontweight="bold",
    )
    fig.tight_layout()
    return fig

def plot_macro_correlation(
    sp500: pd.DataFrame,
    macro_daily: pd.DataFrame,
    macro_monthly: pd.DataFrame,
) -> plt.Figure:
    """
    Plot correlation heatmap between macro indicators and S&P 500 returns.

    Daily S&P 500 returns are calculated and correlated against all
    macro indicators. The heatmap shows which indicators have the
    strongest positive or negative relationship with market returns
    providing insight into which features will be most valuable
    for our forecasting models.

    :param sp500: DataFrame with S&P 500 OHLCV data indexed by date
    :param macro_daily: DataFrame with daily macro indicators
    :param macro_monthly: DataFrame with monthly macro indicators
        excluding binary release flag columns
    :return: matplotlib Figure object with correlation heatmap
    """
    # Calculate daily S&P 500 returns as the target variable.
    sp500_returns = sp500["Close"].pct_change().dropna()
    # Combine all macro indicators into a single DataFrame.
    macro_combined = pd.concat(
        [macro_daily, macro_monthly], axis=1
    )
    # Exclude binary release flag columns from correlation analysis
    # since they are event markers not continuous indicators.
    non_flag_cols = [
        col for col in macro_combined.columns
        if not col.endswith("_released")
    ]
    macro_combined = macro_combined[non_flag_cols]
    # Align macro data with S&P 500 returns on common dates.
    combined = pd.concat(
        [sp500_returns.rename("SP500_Return"), macro_combined],
        axis=1,
    ).dropna()
    # Calculate correlation matrix.
    corr_matrix = combined.corr()
    # Extract only correlations with S&P 500 returns.
    sp500_corr = corr_matrix["SP500_Return"].drop("SP500_Return")
    # Sort by absolute correlation value for better readability.
    sp500_corr = sp500_corr.reindex(
        sp500_corr.abs().sort_values(ascending=False).index
    )
    # Create figure with a single heatmap.
    fig, ax = plt.subplots(figsize=(10, 8))
    # Plot horizontal heatmap of correlations with S&P 500.
    sns.heatmap(
        sp500_corr.to_frame(),
        annot=True,
        fmt=".3f",
        cmap="RdYlGn",
        center=0,
        vmin=-0.3,
        vmax=0.3,
        linewidths=0.5,
        linecolor="white",
        ax=ax,
        cbar_kws={"label": "Correlation with S&P 500 Returns"},
    )
    ax.set_title(
        "Macro Indicator Correlation with S&P 500 Daily Returns",
        fontsize=13,
        fontweight="bold",
    )
    ax.set_xlabel("Correlation")
    ax.set_ylabel("Macro Indicator")
    fig.tight_layout()
    return fig

def plot_rolling_correlations(
    sp500: pd.DataFrame,
    macro_daily: pd.DataFrame,
    macro_monthly: pd.DataFrame,
    window: int = 63,
) -> plt.Figure:
    """
    Plot rolling correlations between key macro indicators and S&P 500.

    Rolling correlations reveal how the relationship between macro
    indicators and market returns changes across different market
    regimes. A static correlation hides these dynamic relationships
    which are critical for understanding regime dependent behavior.
    Daily indicators use daily returns with a 63 day window (3 months)
    and monthly indicators use monthly returns with a 6 month window.

    :param sp500: DataFrame with S&P 500 OHLCV data indexed by date
    :param macro_daily: DataFrame with daily macro indicators
    :param macro_monthly: DataFrame with monthly macro indicators
    :param window: rolling window size in trading days for daily
        indicators default is 63 trading days (3 months)
    :return: matplotlib Figure object with rolling correlation subplots
    """
    # Calculate daily S&P 500 returns for daily indicator correlation.
    sp500_daily_returns = sp500["Close"].pct_change().dropna()
    # Calculate monthly S&P 500 returns for monthly indicator correlation.
    sp500_monthly = sp500["Close"].resample("ME").last()
    sp500_monthly_returns = sp500_monthly.pct_change().dropna()
    # Calculate yield curve as difference between 10Y and 2Y yields.
    yield_curve = macro_daily["TNX"] - macro_daily["IRX"]
    # Define daily indicators to show rolling correlations for.
    daily_indicators = {
        "VIX"        : ("VIX (Fear Index)", macro_daily["VIX"]),
        "Yield Curve": ("Yield Curve (10Y-2Y)", yield_curve),
        "OIL"        : ("Oil Price WTI", macro_daily["OIL"]),
    }
    # Define monthly indicators to show rolling correlations for.
    monthly_indicators = {
        "CPI"         : ("CPI Inflation", macro_monthly["CPI"]),
        "FED_RATE"    : ("Fed Funds Rate", macro_monthly["FED_RATE"]),
        "UNEMPLOYMENT": ("Unemployment Rate", macro_monthly["UNEMPLOYMENT"]),
    }
    # Create figure with 2 rows and 3 columns — 6 subplots total.
    fig, axes = plt.subplots(2, 3, figsize=(18, 10))
    # Plot rolling correlations for daily indicators on top row.
    for idx, (key, (title, series)) in enumerate(
        daily_indicators.items()
    ):
        # Align series with S&P 500 returns on common dates.
        aligned = pd.concat(
            [sp500_daily_returns, series], axis=1
        ).dropna()
        aligned.columns = ["returns", "indicator"]
        # Calculate rolling correlation over the window period.
        rolling_corr = aligned["returns"].rolling(window).corr(
            aligned["indicator"]
        )
        # Plot rolling correlation line.
        axes[0, idx].plot(
            rolling_corr.index,
            rolling_corr.values,
            color="steelblue",
            linewidth=1.2,
            label=f"{window}d rolling correlation",
        )
        # Add horizontal reference line at zero.
        axes[0, idx].axhline(
            0, color="black", linewidth=0.8, linestyle="--"
        )
        # Add shaded regions for key market events.
        axes[0, idx].axvspan(
            pd.Timestamp("2020-02-01"),
            pd.Timestamp("2020-06-01"),
            alpha=0.1,
            color="red",
            label="COVID crash",
        )
        axes[0, idx].axvspan(
            pd.Timestamp("2022-03-01"),
            pd.Timestamp("2023-07-01"),
            alpha=0.1,
            color="orange",
            label="Rate hike cycle",
        )
        axes[0, idx].set_title(
            f"Rolling Correlation: {title} vs S&P 500",
            fontsize=10,
            fontweight="bold",
        )
        axes[0, idx].set_ylabel("Correlation")
        axes[0, idx].set_xlabel("Date")
        axes[0, idx].set_ylim(-1, 1)
        axes[0, idx].legend(fontsize=7, loc="upper left")
    # Plot rolling correlations for monthly indicators on bottom row.
    monthly_window = 6
    for idx, (key, (title, series)) in enumerate(
        monthly_indicators.items()
    ):
        # Resample indicator to monthly frequency.
        series_monthly = series.resample("ME").last()
        # Align with monthly S&P 500 returns on common dates.
        aligned = pd.concat(
            [sp500_monthly_returns, series_monthly], axis=1
        ).dropna()
        aligned.columns = ["returns", "indicator"]
        # Calculate rolling correlation over 6 month window.
        rolling_corr = aligned["returns"].rolling(
            monthly_window
        ).corr(aligned["indicator"])
        # Plot rolling correlation line.
        axes[1, idx].plot(
            rolling_corr.index,
            rolling_corr.values,
            color="darkorange",
            linewidth=1.5,
            label=f"{monthly_window}m rolling correlation",
        )
        # Add horizontal reference line at zero.
        axes[1, idx].axhline(
            0, color="black", linewidth=0.8, linestyle="--"
        )
        # Add shaded regions for key market events.
        axes[1, idx].axvspan(
            pd.Timestamp("2020-02-01"),
            pd.Timestamp("2020-06-01"),
            alpha=0.1,
            color="red",
            label="COVID crash",
        )
        axes[1, idx].axvspan(
            pd.Timestamp("2022-03-01"),
            pd.Timestamp("2023-07-01"),
            alpha=0.1,
            color="orange",
            label="Rate hike cycle",
        )
        axes[1, idx].set_title(
            f"Rolling Correlation: {title} vs S&P 500",
            fontsize=10,
            fontweight="bold",
        )
        axes[1, idx].set_ylabel("Correlation")
        axes[1, idx].set_xlabel("Date")
        axes[1, idx].set_ylim(-1, 1)
        axes[1, idx].legend(fontsize=7, loc="upper left")
    fig.suptitle(
        "Rolling Macro Correlations with S&P 500 Returns 2018-2024",
        fontsize=14,
        fontweight="bold",
    )
    fig.tight_layout()
    return fig

def calculate_macro_features(
    macro_daily: pd.DataFrame,
    macro_monthly: pd.DataFrame,
) -> pd.DataFrame:
    """
    Calculate derived macro features from downloaded indicators.

    Six new features are calculated from existing macro indicators.
    The yield curve is calculated as the spread between 10Y and 2Y
    treasury yields. A binary inversion flag marks periods where the
    curve is inverted — a historically reliable recession signal.
    Month over month changes capture acceleration or deceleration
    in key indicators rather than just their absolute levels.
    Moving averages and momentum smooth out noise in volatile series.

    :param macro_daily: DataFrame with daily macro indicators
        including `TNX`, `IRX`, `VIX`, and `OIL` columns
    :param macro_monthly: DataFrame with monthly macro indicators
        including `CPI` and `NFP` columns
    :return: DataFrame containing all six calculated macro features
        indexed by the same business day dates as the input data
    """
    # Initialize output DataFrame with same index as daily macro data.
    features = pd.DataFrame(index=macro_daily.index)
    # Calculate yield curve as spread between 10Y and 2Y yields.
    features["YIELD_CURVE"] = macro_daily["TNX"] - macro_daily["IRX"]
    # Flag yield curve inversion as binary signal where 2Y exceeds 10Y.
    features["YIELD_CURVE_INVERTED"] = (
        features["YIELD_CURVE"] < 0
    ).astype(int)
    # Calculate CPI month over month change to capture inflation trend.
    features["CPI_MOM"] = macro_monthly["CPI"].pct_change() * 100
    # Calculate VIX 20 day moving average to smooth daily fear spikes.
    features["VIX_MA20"] = macro_daily["VIX"].rolling(20).mean()
    # Calculate oil 30 day momentum to capture energy price trends.
    features["OIL_MOM30"] = macro_daily["OIL"].pct_change(30) * 100
    # Calculate NFP month over month change to capture jobs acceleration.
    features["NFP_MOM"] = macro_monthly["NFP"].diff()
    # Forward fill any NaN values created by rolling calculations.
    features = features.ffill().bfill()
    return features

def calculate_technical_indicators(
    sp500: pd.DataFrame,
) -> pd.DataFrame:
    """
    Calculate technical indicators from S&P 500 closing prices.

    Nine technical indicators are calculated covering trend direction,
    momentum, and volatility. Moving averages capture the price trend
    at different time horizons. RSI measures overbought and oversold
    conditions. MACD captures momentum shifts. Bollinger Bands measure
    volatility and price extremes relative to recent history.

    :param sp500: DataFrame with S&P 500 OHLCV data indexed by date
        containing a `Close` column with daily closing prices
    :return: DataFrame containing all nine technical indicators
        indexed by the same business day dates as the input data
    """
    # Initialize output DataFrame with same index as S&P 500 data.
    features = pd.DataFrame(index=sp500.index)
    # Extract closing prices for all calculations.
    close = sp500["Close"]
    # Calculate simple moving averages at three time horizons.
    features["MA5"]  = close.rolling(5).mean()
    features["MA20"] = close.rolling(20).mean()
    features["MA50"] = close.rolling(50).mean()
    # Calculate exponential moving averages for MACD calculation.
    features["EMA12"] = close.ewm(span=12, adjust=False).mean()
    features["EMA26"] = close.ewm(span=26, adjust=False).mean()
    # Calculate MACD as difference between fast and slow EMAs.
    features["MACD"] = features["EMA12"] - features["EMA26"]
    # Calculate RSI using average gains and losses over 14 days.
    delta = close.diff()
    # Separate positive and negative price changes.
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    # Calculate average gain and loss over 14 day window.
    avg_gain = gain.rolling(14).mean()
    avg_loss = loss.rolling(14).mean()
    # Calculate relative strength and convert to RSI scale.
    rs = avg_gain / avg_loss
    features["RSI"] = 100 - (100 / (1 + rs))
    # Calculate Bollinger Bands using 20 day rolling statistics.
    bb_mid = close.rolling(20).mean()
    bb_std = close.rolling(20).std()
    features["BB_UPPER"] = bb_mid + (2 * bb_std)
    features["BB_LOWER"] = bb_mid - (2 * bb_std)
    # Forward fill then backward fill NaN values from rolling windows.
    features = features.ffill().bfill()
    return features

def calculate_calendar_features(
    index: pd.DatetimeIndex,
) -> pd.DataFrame:
    """
    Calculate calendar based features from a DatetimeIndex.

    Three calendar features are extracted from the date index.
    Day of week captures weekly seasonality — Mondays and Fridays
    historically show different return patterns than midweek days.
    Month captures monthly seasonality — the January effect and
    September weakness are well documented market patterns.
    Quarter captures quarterly seasonality driven by earnings seasons
    and institutional rebalancing at quarter end.

    :param index: DatetimeIndex from any of our aligned DataFrames
        containing business day dates for the analysis period
    :return: DataFrame with three calendar feature columns indexed
        by the same DatetimeIndex as the input
    """
    # Initialize output DataFrame with same index as input.
    features = pd.DataFrame(index=index)
    # Extract day of week where Monday is 0 and Friday is 4.
    features["DAY_OF_WEEK"] = index.dayofweek
    # Extract month of year where January is 1 and December is 12.
    features["MONTH"] = index.month
    # Extract quarter where Q1 is 1 and Q4 is 4.
    features["QUARTER"] = index.quarter
    return features

def calculate_event_flags(
    index: pd.DatetimeIndex,
    fred_api_key: str,
) -> pd.DataFrame:
    """
    Calculate binary event flags for known market moving dates.

    Three event flags are created — US federal holidays, FOMC meeting
    dates, and CPI release dates. These flags help models learn that
    market behavior around these events differs systematically from
    normal trading days. FOMC and CPI dates are fetched from FRED
    to ensure accuracy. Holiday flags use the `holidays` library.

    :param index: DatetimeIndex from any of our aligned DataFrames
        containing business day dates for the analysis period
    :param fred_api_key: FRED API key for fetching FOMC and CPI
        release dates
    :return: DataFrame with three binary event flag columns indexed
        by the same DatetimeIndex as the input
    """
    # Initialize output DataFrame with same index as input.
    features = pd.DataFrame(index=index)
    # Get the start and end years from the index for holiday generation.
    start_year = index.year.min()
    end_year = index.year.max()
    # Generate US federal holiday dates for the full analysis period.
    us_holidays = holidays.US(
        years=range(start_year, end_year + 1)
    )
    # Create binary flag for trading days adjacent to US holidays.
    features["IS_HOLIDAY_ADJACENT"] = index.map(
        lambda d: 1 if (
            d in us_holidays
            or (d - pd.Timedelta(days=1)) in us_holidays
            or (d + pd.Timedelta(days=1)) in us_holidays
        ) else 0
    )
    # Fetch FOMC meeting dates from FRED using the federal funds
    # rate vintage dates as a proxy for meeting announcement dates.
    fred = fredapi.Fred(api_key=fred_api_key)
    try:
        # Use Fed Funds Rate vintage dates as FOMC meeting proxy.
        fomc_dates = pd.DatetimeIndex(
            fred.get_series_vintage_dates("FEDFUNDS")
        )
        # Filter to our analysis period only.
        fomc_dates = fomc_dates[
            (fomc_dates >= index[0]) & (fomc_dates <= index[-1])
        ]
        # Create binary flag for FOMC meeting dates.
        features["IS_FOMC_DATE"] = index.isin(fomc_dates).astype(int)
    except Exception as e:
        _LOG.warning(
            "Could not fetch FOMC dates: %s — setting flag to zero.",
            str(e),
        )
        features["IS_FOMC_DATE"] = 0
    # Fetch CPI release dates from FRED using CPI vintage dates.
    try:
        cpi_dates = pd.DatetimeIndex(
            fred.get_series_vintage_dates("CPIAUCSL")
        )
        # Filter to our analysis period only.
        cpi_dates = cpi_dates[
            (cpi_dates >= index[0]) & (cpi_dates <= index[-1])
        ]
        # Create binary flag for CPI release dates.
        features["IS_CPI_RELEASE"] = index.isin(cpi_dates).astype(int)
    except Exception as e:
        _LOG.warning(
            "Could not fetch CPI release dates: %s — setting flag to zero.",
            str(e),
        )
        features["IS_CPI_RELEASE"] = 0
    # Log summary of event flags created.
    _LOG.info(
        "Holiday adjacent days: %d",
        features["IS_HOLIDAY_ADJACENT"].sum(),
    )
    _LOG.info(
        "FOMC meeting dates: %d",
        features["IS_FOMC_DATE"].sum(),
    )
    _LOG.info(
        "CPI release dates: %d",
        features["IS_CPI_RELEASE"].sum(),
    )
    return features

def build_master_dataframe(
    sp500: pd.DataFrame,
    macro_daily: pd.DataFrame,
    macro_monthly: pd.DataFrame,
    macro_features: pd.DataFrame,
    technical_features: pd.DataFrame,
    calendar_features: pd.DataFrame,
    event_flags: pd.DataFrame,
) -> pd.DataFrame:
    """
    Combine all feature groups into a single master DataFrame.

    All feature DataFrames are concatenated column wise into one
    master DataFrame containing the S&P 500 target variable and
    all 46 features. The target variable `Close` is kept as the
    first column for clarity. All DataFrames must share the same
    DatetimeIndex before calling this function.

    :param sp500: DataFrame with S&P 500 OHLCV data
    :param macro_daily: DataFrame with daily macro indicators
    :param macro_monthly: DataFrame with monthly macro indicators
        and binary release flags
    :param macro_features: DataFrame with calculated macro features
    :param technical_features: DataFrame with technical indicators
    :param calendar_features: DataFrame with calendar features
    :param event_flags: DataFrame with binary event flags
    :return: master DataFrame with target variable and all features
        combined into a single structure indexed by business day dates
    """
    # Extract only the closing price as the target variable.
    target = sp500[["Close"]].copy()
    # Combine all feature groups column wise into master DataFrame.
    master = pd.concat(
        [
            target,
            macro_daily,
            macro_monthly,
            macro_features,
            technical_features,
            calendar_features,
            event_flags,
        ],
        axis=1,
    )
    # Verify no NaN values exist in the master DataFrame.
    nan_count = master.isnull().sum().sum()
    if nan_count > 0:
        _LOG.warning(
            "Master DataFrame has %d NaN values — forward filling.",
            nan_count,
        )
        master = master.ffill().bfill()
    _LOG.info(
        "Master DataFrame shape: %s", master.shape
    )
    _LOG.info(
        "Total features: %d (excluding target variable)",
        master.shape[1] - 1,
    )
    return master

def split_data(
    master: pd.DataFrame,
    test_size: int,
    val_size: int,
) -> tuple:
    """
    Split master DataFrame into train, validation, and test sets.

    A strict time based split is used where training data comes first,
    validation data comes next, and test data comes last. This prevents
    any form of data leakage where future information influences the
    model during training. The test set is never used during training
    or hyperparameter tuning — only for final evaluation.

    :param master: master DataFrame with target variable and all
        features indexed by business day dates
    :param test_size: number of trading days to hold out for testing
        — these days are never seen during training or tuning
    :param val_size: number of trading days to hold out for validation
        — used for hyperparameter tuning and early stopping
    :return: tuple of (train, validation, test) DataFrames in
        chronological order with no overlap between splits
    """
    # Calculate split indices from the end of the DataFrame.
    total_rows = len(master)
    test_start = total_rows - test_size
    val_start = test_start - val_size
    # Split into train, validation, and test sets.
    train = master.iloc[:val_start]
    val = master.iloc[val_start:test_start]
    test = master.iloc[test_start:]
    # Log split details for verification.
    _LOG.info(
        "Train: %d rows | %s to %s",
        len(train),
        train.index[0].date(),
        train.index[-1].date(),
    )
    _LOG.info(
        "Validation: %d rows | %s to %s",
        len(val),
        val.index[0].date(),
        val.index[-1].date(),
    )
    _LOG.info(
        "Test: %d rows | %s to %s",
        len(test),
        test.index[0].date(),
        test.index[-1].date(),
    )
    _LOG.info(
        "Train: %.1f%% | Val: %.1f%% | Test: %.1f%%",
        len(train) / total_rows * 100,
        len(val) / total_rows * 100,
        len(test) / total_rows * 100,
    )
    return train, val, test

def build_timeseries(
    train: pd.DataFrame,
    val: pd.DataFrame,
    test: pd.DataFrame,
    target_col: str,
    future_cov_cols: list,
    past_cov_cols: list,
) -> tuple:
    """
    Build Darts TimeSeries objects from train, validation, and test sets.

    Three types of TimeSeries are created for each split — the target
    series containing S&P 500 closing prices, future covariates
    containing features known in advance like calendar and event flags,
    and past covariates containing features only known historically
    like technical indicators and macro values. All series are scaled
    using Darts Scaler to normalize values for better model performance.

    :param train: training DataFrame with target and all features
    :param val: validation DataFrame with target and all features
    :param test: test DataFrame with target and all features
    :param target_col: name of the target column e.g. `'Close'`
    :param future_cov_cols: list of column names for future covariates
        — features whose future values are known at prediction time
    :param past_cov_cols: list of column names for past covariates
        — features whose future values are unknown at prediction time
    :return: tuple of scaled TimeSeries objects in order:
        (target_train, target_val, target_test,
         future_cov_train, future_cov_val, future_cov_test,
         past_cov_train, past_cov_val, past_cov_test,
         target_scaler, cov_scaler)
    """
    # Concatenate all splits for building full covariates series.
    full_data = pd.concat([train, val, test])
    # Build target TimeSeries for each split.
    target_train = darts.timeseries.TimeSeries.from_dataframe(
        train, value_cols=target_col,
        fill_missing_dates=True, freq="B"
    )
    target_val = darts.timeseries.TimeSeries.from_dataframe(
        val, value_cols=target_col,
        fill_missing_dates=True, freq="B"
    )
    target_test = darts.timeseries.TimeSeries.from_dataframe(
        test, value_cols=target_col,
        fill_missing_dates=True, freq="B"
    )
    # Build future covariates TimeSeries for each split.
    future_cov_train = darts.timeseries.TimeSeries.from_dataframe(
        train, value_cols=future_cov_cols,
        fill_missing_dates=True, freq="B"
    )
    future_cov_val = darts.timeseries.TimeSeries.from_dataframe(
        val, value_cols=future_cov_cols,
        fill_missing_dates=True, freq="B"
    )
    future_cov_test = darts.timeseries.TimeSeries.from_dataframe(
        test, value_cols=future_cov_cols,
        fill_missing_dates=True, freq="B"
    )
    # Build past covariates TimeSeries for each split.
    past_cov_train = darts.timeseries.TimeSeries.from_dataframe(
        train, value_cols=past_cov_cols,
        fill_missing_dates=True, freq="B"
    )
    past_cov_val = darts.timeseries.TimeSeries.from_dataframe(
        val, value_cols=past_cov_cols,
        fill_missing_dates=True, freq="B"
    )
    past_cov_test = darts.timeseries.TimeSeries.from_dataframe(
        test, value_cols=past_cov_cols,
        fill_missing_dates=True, freq="B"
    )
    # Scale target series using Darts Scaler.
    target_scaler = darts.dataprocessing.transformers.Scaler()
    target_train_scaled = target_scaler.fit_transform(target_train)
    target_val_scaled = target_scaler.transform(target_val)
    target_test_scaled = target_scaler.transform(target_test)
    # Scale covariate series using a separate Scaler.
    cov_scaler = darts.dataprocessing.transformers.Scaler()
    future_cov_train_scaled = cov_scaler.fit_transform(
        future_cov_train
    )
    future_cov_val_scaled = cov_scaler.transform(future_cov_val)
    future_cov_test_scaled = cov_scaler.transform(future_cov_test)
    past_cov_train_scaled = cov_scaler.fit_transform(past_cov_train)
    past_cov_val_scaled = cov_scaler.transform(past_cov_val)
    past_cov_test_scaled = cov_scaler.transform(past_cov_test)
    # Log summary of TimeSeries objects created.
    _LOG.info(
        "Target train length: %d", len(target_train_scaled)
    )
    _LOG.info(
        "Future covariates: %d columns", len(future_cov_cols)
    )
    _LOG.info(
        "Past covariates: %d columns", len(past_cov_cols)
    )
    return (
        target_train_scaled,
        target_val_scaled,
        target_test_scaled,
        future_cov_train_scaled,
        future_cov_val_scaled,
        future_cov_test_scaled,
        past_cov_train_scaled,
        past_cov_val_scaled,
        past_cov_test_scaled,
        target_scaler,
        cov_scaler,
    )

def train_baseline_models(
    target_train: darts.timeseries.TimeSeries,
    forecast_horizon: int,
) -> dict:
    """
    Train all baseline forecasting models on the training series.

    Baseline models make simple predictions without learning complex
    patterns. They serve as benchmarks that all other models must
    outperform to demonstrate genuine predictive value. Holiday gap
    NaN values are filled before training since baseline models
    cannot handle missing values in the target series.

    :param target_train: scaled target TimeSeries for training
        containing S&P 500 closing prices
    :param forecast_horizon: number of trading days to forecast
        ahead e.g. `30` for a 30 day forecast
    :return: dictionary mapping model names to their predictions
        as Darts TimeSeries objects
    """
    # Fill holiday gap NaN values before training since baseline
    # models cannot handle missing values in the target series.
    target_df = target_train.to_dataframe().ffill().bfill()
    target_df.index.freq = "B"
    target_clean = darts.timeseries.TimeSeries.from_dataframe(
        target_df, fill_missing_dates=True, freq="B"
    )
    # Initialize dictionary to store model predictions.
    predictions = {}
    # Train NaiveSeasonal model — repeats value from K periods ago.
    _LOG.info("Training NaiveSeasonal model.")
    naive_seasonal = darts.models.NaiveSeasonal(K=5)
    naive_seasonal.fit(target_clean)
    predictions["NaiveSeasonal"] = naive_seasonal.predict(
        forecast_horizon
    )
    # Train NaiveDrift model — extrapolates the linear trend.
    _LOG.info("Training NaiveDrift model.")
    naive_drift = darts.models.NaiveDrift()
    naive_drift.fit(target_clean)
    predictions["NaiveDrift"] = naive_drift.predict(forecast_horizon)
    # Train NaiveMean model — always predicts the training mean.
    _LOG.info("Training NaiveMean model.")
    naive_mean = darts.models.NaiveMean()
    naive_mean.fit(target_clean)
    predictions["NaiveMean"] = naive_mean.predict(forecast_horizon)
    # Train NaiveMovingAverage — predicts average of last N values.
    _LOG.info("Training NaiveMovingAverage model.")
    naive_ma = darts.models.NaiveMovingAverage(input_chunk_length=5)
    naive_ma.fit(target_clean)
    predictions["NaiveMovingAverage"] = naive_ma.predict(
        forecast_horizon
    )
    _LOG.info(
        "Baseline models trained successfully — %d models.",
        len(predictions),
    )
    return predictions

def train_statistical_models(
    target_train: darts.timeseries.TimeSeries,
    forecast_horizon: int,
) -> dict:
    """
    Train all classical statistical forecasting models on the training series.

    Statistical models capture linear time series patterns using
    mathematical formulations. They operate on price history only
    and cannot accept external covariates. Holiday gap NaN values
    are filled before training since statistical models cannot
    handle missing values in the target series.

    :param target_train: scaled target TimeSeries for training
        containing S&P 500 closing prices
    :param forecast_horizon: number of trading days to forecast
        ahead e.g. `30` for a 30 day forecast
    :return: dictionary mapping model names to their predictions
        as Darts TimeSeries objects
    """
    # Fill holiday gap NaN values before training since statistical
    # models cannot handle missing values in the target series.
    target_df = target_train.to_dataframe().ffill().bfill()
    target_df.index.freq = "B"
    target_clean = darts.timeseries.TimeSeries.from_dataframe(
        target_df, fill_missing_dates=True, freq="B"
    )
    # Initialize dictionary to store model predictions.
    predictions = {}
    # Define all statistical models with their configurations.
    models = {
        "ARIMA": darts.models.ARIMA(p=5, d=1, q=0),
        "AutoARIMA": darts.models.AutoARIMA(
            start_p=1, max_p=5, max_q=3, d=1,
        ),
        "ExponentialSmoothing": darts.models.ExponentialSmoothing(),
        "Theta": darts.models.Theta(),
        "FourTheta": darts.models.FourTheta(),
        "FFT": darts.models.FFT(nr_freqs_to_keep=10),
        "TBATS": darts.models.TBATS(
            season_length=5,
            use_boxcox=True,
            use_trend=True,
            use_damped_trend=True,
            use_arma_errors=True,
        ),
    }
    # Train each statistical model and store predictions.
    for name, model in models.items():
        try:
            _LOG.info("Training %s model.", name)
            model.fit(target_clean)
            predictions[name] = model.predict(forecast_horizon)
            _LOG.info("%s trained successfully.", name)
        except Exception as e:
            _LOG.warning(
                "%s failed to train: %s — skipping.", name, str(e)
            )
    _LOG.info(
        "Statistical models trained successfully — %d models.",
        len(predictions),
    )
    return predictions


def train_probabilistic_models(
    target_train: darts.timeseries.TimeSeries,
    forecast_horizon: int,
) -> dict:
    """
    Train probabilistic forecasting models on the training series.

    Probabilistic models estimate a distribution over future values
    rather than a single point forecast. KalmanForecaster uses a
    state space model to track the latent state of the S&P 500 and
    naturally quantifies prediction uncertainty. It handles irregular
    frequencies and missing observations natively making it well
    suited for stock market data.

    :param target_train: scaled target TimeSeries for training
        containing S&P 500 closing prices
    :param forecast_horizon: number of trading days to forecast
        ahead e.g. `30` for a 30 day forecast
    :return: dictionary mapping model names to their predictions
        as Darts TimeSeries objects
    """
    # Initialize dictionary to store model predictions.
    predictions = {}
    try:
        # Fill any NaN values from holiday gaps before training
        # since KalmanForecaster cannot handle null values.
        target_df = target_train.to_dataframe().ffill().bfill()
        target_df.index.freq = "B"
        target_clean = darts.timeseries.TimeSeries.from_dataframe(
            target_df, fill_missing_dates=True, freq="B"
        )
        # Train KalmanForecaster with 4 dimensional state space.
        # dim_x=4 models position velocity acceleration and jerk
        # of the price series capturing different orders of price
        # change dynamics simultaneously.
        _LOG.info("Training KalmanForecaster model.")
        kalman = darts.models.KalmanForecaster(dim_x=4)
        kalman.fit(target_clean)
        predictions["KalmanForecaster"] = kalman.predict(
            forecast_horizon
        )
        _LOG.info("KalmanForecaster trained successfully.")
    except Exception as e:
        _LOG.warning(
            "KalmanForecaster failed to train: %s — skipping.",
            str(e),
        )
    return predictions

def train_ml_models(
    target_train: darts.timeseries.TimeSeries,
    past_cov_train: darts.timeseries.TimeSeries,
    future_cov_train: darts.timeseries.TimeSeries,
    future_cov_full: darts.timeseries.TimeSeries,
    forecast_horizon: int,
) -> dict:
    """
    Train all machine learning forecasting models on the training series.

    ML models use the full 41 feature set including macro indicators
    technical indicators calendar features and event flags. NaN values
    from holiday gaps are filled using Darts MissingValuesFiller
    which preserves the TimeSeries frequency attribute unlike
    DataFrame conversion approaches.

    :param target_train: scaled target TimeSeries for training
        containing 30 day forward S&P 500 returns
    :param past_cov_train: scaled past covariates TimeSeries
        containing macro and technical features
    :param future_cov_train: scaled future covariates TimeSeries
        containing calendar and event features
    :param future_cov_full: scaled future covariates TimeSeries
        containing calendar and event features for full period
    :param forecast_horizon: number of trading days to forecast
        ahead e.g. `30` for a 30 day forecast
    :return: dictionary mapping model names to their predictions
        as Darts TimeSeries objects
    """
    # Fill NaN values using Darts MissingValuesFiller which
    # preserves TimeSeries frequency unlike DataFrame conversion.
    filler = darts.dataprocessing.transformers.MissingValuesFiller()
    target_clean = filler.transform(target_train)
    past_clean = filler.transform(past_cov_train)
    future_clean = filler.transform(future_cov_train)
    future_full_clean = filler.transform(future_cov_full)
    # Initialize dictionary to store model predictions.
    predictions = {}
    # Define all ML models with their configurations.
    models = {
        "LinearRegression": darts.models.LinearRegressionModel(
            lags=30,
            lags_past_covariates=30,
            lags_future_covariates=[0],
            output_chunk_length=forecast_horizon,
        ),
        "RandomForest": darts.models.RandomForestModel(
            lags=30,
            lags_past_covariates=30,
            lags_future_covariates=[0],
            output_chunk_length=forecast_horizon,
            n_estimators=100,
            random_state=42,
        ),
        "LightGBM": darts.models.LightGBMModel(
            lags=30,
            lags_past_covariates=30,
            lags_future_covariates=[0],
            output_chunk_length=forecast_horizon,
            n_estimators=200,
            num_leaves=31,
            learning_rate=0.05,
            random_state=42,
            verbose=-1,
        ),
        "XGBoost": darts.models.XGBModel(
            lags=30,
            lags_past_covariates=30,
            lags_future_covariates=[0],
            output_chunk_length=forecast_horizon,
            n_estimators=200,
            learning_rate=0.05,
            max_depth=6,
            random_state=42,
            verbosity=0,
        ),
        "CatBoost": darts.models.CatBoostModel(
            lags=30,
            lags_past_covariates=30,
            lags_future_covariates=[0],
            output_chunk_length=forecast_horizon,
            iterations=200,
            learning_rate=0.05,
            depth=6,
            random_seed=42,
            verbose=False,
        ),
    }
    # Train each ML model with cleaned past and future covariates.
    for name, model in models.items():
        try:
            _LOG.info("Training %s model.", name)
            model.fit(
                target_clean,
                past_covariates=past_clean,
                future_covariates=future_clean,
            )
            predictions[name] = model.predict(
                forecast_horizon,
                past_covariates=past_clean,
                future_covariates=future_full_clean,
            )
            _LOG.info("%s trained successfully.", name)
        except Exception as e:
            _LOG.warning(
                "%s failed to train: %s — skipping.", name, str(e)
            )
    _LOG.info(
        "ML models trained successfully — %d models.",
        len(predictions),
    )
    return predictions

def train_prophet_model(
    target_train: darts.timeseries.TimeSeries,
    future_cov_full: darts.timeseries.TimeSeries,
    forecast_horizon: int,
) -> dict:
    """
    Train Prophet model with event flags as additional regressors.

    Prophet is designed for time series with strong seasonal patterns
    and known holiday effects. Event flags for FOMC meetings CPI
    release dates and US holidays are passed as future covariates
    allowing Prophet to model the systematic impact of these known
    market moving events on S&P 500 returns.

    :param target_train: scaled target TimeSeries for training
        containing S&P 500 closing prices
    :param future_cov_full: scaled future covariates TimeSeries
        containing calendar and event features for the full period
        including dates beyond the training end for prediction
    :param forecast_horizon: number of trading days to forecast
        ahead e.g. `30` for a 30 day forecast
    :return: dictionary mapping model name to its prediction
        as a Darts TimeSeries object
    """
    # Initialize dictionary to store model predictions.
    predictions = {}
    try:
        # Clean target series to remove holiday gap NaN values.
        target_df = target_train.to_dataframe().ffill().bfill()
        target_df.index.freq = "B"
        target_clean = darts.timeseries.TimeSeries.from_dataframe(
            target_df, fill_missing_dates=True, freq="B"
        )
        # Clean full future covariates for Prophet regressors.
        future_df = future_cov_full.to_dataframe().ffill().bfill()
        future_df.index.freq = "B"
        future_clean = darts.timeseries.TimeSeries.from_dataframe(
            future_df, fill_missing_dates=True, freq="B"
        )
        # Train Prophet with future covariates as additional regressors.
        # add_encoders encodes future covariate columns as regressors
        # that Prophet uses alongside its built in seasonality components.
        _LOG.info("Training Prophet model.")
        prophet_model = darts.models.Prophet(
            add_seasonalities={
                "name"            : "monthly",
                "seasonal_periods": 21,
                "fourier_order"   : 5,
            },
        )
        prophet_model.fit(
            target_clean,
            future_covariates=future_clean,
        )
        predictions["Prophet"] = prophet_model.predict(
            forecast_horizon,
            future_covariates=future_clean,
        )
        _LOG.info("Prophet trained successfully.")
    except Exception as e:
        _LOG.warning(
            "Prophet failed to train: %s — skipping.", str(e)
        )
    return predictions

def evaluate_models(
    predictions: dict,
    target_val: darts.timeseries.TimeSeries,
    target_scaler: darts.dataprocessing.transformers.Scaler,
) -> pd.DataFrame:
    """
    Evaluate all model predictions against the validation target series.

    Predictions are aligned with validation data by date before computing
    metrics. All predictions are inverse transformed from scaled space
    back to original price space before computing metrics. Six metrics
    are calculated — MAE RMSE MAPE Direction Accuracy and R squared.
    Direction accuracy measures whether the model correctly predicted
    the implied 30 day return direction — the most business relevant
    metric. Results are sorted by MAPE ascending.

    :param predictions: dictionary mapping model names to their
        Darts TimeSeries predictions in scaled space
    :param target_val: scaled validation target TimeSeries containing
        actual S&P 500 closing prices for the validation period
    :param target_scaler: fitted Darts Scaler used to inverse transform
        predictions back to original price space
    :return: DataFrame with evaluation metrics for each model sorted
        by MAPE from lowest to highest
    """
    # Initialize list to collect metric rows for each model.
    results = []
    # Fill NaN values in validation target using Darts filler.
    filler = darts.dataprocessing.transformers.MissingValuesFiller()
    target_val_clean = filler.transform(target_val)
    # Inverse transform validation to original price space.
    actual_df = target_scaler.inverse_transform(
        target_val_clean
    ).to_dataframe().dropna()
    # Evaluate each model prediction against actual values.
    for name, prediction in predictions.items():
        try:
            # Fill NaN values in prediction.
            pred_clean = filler.transform(prediction)
            # Inverse transform prediction to original price space.
            pred_inverse_df = target_scaler.inverse_transform(
                pred_clean
            ).to_dataframe().dropna()
            # Align prediction and actual by common dates.
            common_dates = actual_df.index.intersection(
                pred_inverse_df.index
            )
            # Skip model if insufficient common dates.
            if len(common_dates) < 5:
                _LOG.warning(
                    "%s has fewer than 5 common dates — skipping.",
                    name,
                )
                continue
            # Extract aligned values for metric computation.
            actual = actual_df.loc[common_dates].values.flatten()
            predicted = pred_inverse_df.loc[
                common_dates
            ].values.flatten()
            # Calculate MAE in price units.
            mae = float(np.mean(np.abs(actual - predicted)))
            # Calculate RMSE in price units.
            rmse = float(
                np.sqrt(np.mean((actual - predicted) ** 2))
            )
            # Calculate MAPE as percentage of actual price.
            mape = float(
                np.mean(np.abs((actual - predicted) / actual)) * 100
            )
            # Calculate sMAPE.
            smape = float(
                np.mean(
                    2 * np.abs(actual - predicted)
                    / (np.abs(actual) + np.abs(predicted) + 1e-8)
                ) * 100
            )
            # Calculate direction accuracy across all prediction days.
            # Each day check if predicted price is above or below
            # starting price in same direction as actual price.
            reference_price = actual[0]
            actual_directions = np.sign(actual - reference_price)
            predicted_directions = np.sign(predicted - reference_price)
            # Only evaluate days where market actually moved.
            valid_mask = actual_directions != 0
            if valid_mask.sum() > 0:
                direction_accuracy = float(
                    np.mean(
                        actual_directions[valid_mask]
                        == predicted_directions[valid_mask]
                    ) * 100
                )
            else:
                direction_accuracy = 0.0
    
            # Calculate R squared.
            ss_res = np.sum((actual - predicted) ** 2)
            ss_tot = np.sum((actual - np.mean(actual)) ** 2)
            r2 = float(1 - ss_res / ss_tot)
            results.append({
                "Model"     : name,
                "MAE"       : round(mae, 2),
                "RMSE"      : round(rmse, 2),
                "MAPE"      : round(mape, 2),
                "sMAPE"     : round(smape, 2),
                "Direction" : round(direction_accuracy, 1),
                "R2"        : round(r2, 4),
                "Days"      : len(common_dates),
            })
            _LOG.info(
                "%s → MAPE: %.2f%% | Direction: %.1f%% | R2: %.4f",
                name, mape, direction_accuracy, r2,
            )
        except Exception as e:
            _LOG.warning(
                "Could not evaluate %s: %s — skipping.",
                name, str(e),
            )
    # Return empty DataFrame if no results.
    if not results:
        _LOG.warning("No models evaluated successfully.")
        return pd.DataFrame(
            columns=[
                "Model", "MAE", "RMSE", "MAPE",
                "sMAPE", "Direction", "R2", "Days"
            ]
        )
    # Sort by MAPE ascending.
    return pd.DataFrame(results).sort_values(
        "MAPE", ascending=True
    ).reset_index(drop=True)

def plot_predictions_vs_actual(
    predictions: dict,
    target_val: darts.timeseries.TimeSeries,
    target_scaler: darts.dataprocessing.transformers.Scaler,
    n_models: int = 6,
) -> plt.Figure:
    """
    Plot model predictions against actual S&P 500 prices.

    Only the prediction period is shown for clarity. The top n
    models by MAE are selected and their predictions plotted
    alongside actual prices. The actual price series is shown
    in black and each model prediction in a distinct color.
    A shaded confidence band shows the MAE range around the
    best model prediction.

    :param predictions: dictionary mapping model names to their
        Darts TimeSeries predictions in scaled space
    :param target_val: scaled validation target TimeSeries
    :param target_scaler: fitted Darts Scaler for inverse transform
    :param n_models: number of top models to plot default is 6
    :return: matplotlib Figure object with clean prediction chart
    """
    # Fill NaN values in validation target.
    filler = darts.dataprocessing.transformers.MissingValuesFiller()
    target_val_clean = filler.transform(target_val)
    # Inverse transform validation to original price space.
    actual_df = target_scaler.inverse_transform(
        target_val_clean
    ).to_dataframe().dropna()
    # Collect all model predictions in original price space.
    model_predictions = {}
    model_errors = {}
    for name, prediction in predictions.items():
        try:
            pred_clean = filler.transform(prediction)
            pred_df = target_scaler.inverse_transform(
                pred_clean
            ).to_dataframe().dropna()
            # Find common dates with actual values.
            common_dates = actual_df.index.intersection(
                pred_df.index
            )
            if len(common_dates) >= 5:
                aligned_actual = actual_df.loc[common_dates].values.flatten()
                aligned_pred = pred_df.loc[common_dates].values.flatten()
                mae = float(np.mean(np.abs(aligned_actual - aligned_pred)))
                model_predictions[name] = pred_df.loc[common_dates]
                model_errors[name] = mae
        except Exception as e:
            _LOG.warning(
                "Could not process %s for plotting: %s", name, str(e)
            )
    # Sort by MAE and take top n models.
    top_models = sorted(
        model_errors.keys(), key=lambda x: model_errors[x]
    )[:n_models]
    # Get prediction date range.
    pred_start = min(
        model_predictions[name].index[0] for name in top_models
    )
    pred_end = max(
        model_predictions[name].index[-1] for name in top_models
    )
    # Add 3 day buffer on each side for context.
    buffer = pd.tseries.offsets.BusinessDay(3)
    # Filter actual prices to prediction period only.
    actual_in_range = actual_df.loc[
        (actual_df.index >= pred_start - buffer) &
        (actual_df.index <= pred_end + buffer)
    ]
    # Define distinct colors for each model.
    colors = [
        "steelblue", "crimson", "forestgreen",
        "darkorange", "purple", "brown",
    ]
    # Create single clean figure.
    fig, ax = plt.subplots(figsize=(16, 7))
    # Plot actual prices in thick black line.
    ax.plot(
        actual_in_range.index,
        actual_in_range.values.flatten(),
        color="black",
        linewidth=2.5,
        label="Actual S&P 500",
        zorder=5,
    )
    # Add shaded confidence band around best model prediction.
    best_model = top_models[0]
    best_pred = model_predictions[best_model]
    best_mae = model_errors[best_model]
    ax.fill_between(
        best_pred.index,
        best_pred.values.flatten() - best_mae,
        best_pred.values.flatten() + best_mae,
        alpha=0.15,
        color=colors[0],
        label=f"±MAE ${best_mae:.0f} confidence band",
    )
    # Plot each top model prediction as dashed line.
    for idx, name in enumerate(top_models):
        pred_df = model_predictions[name]
        mae = model_errors[name]
        ax.plot(
            pred_df.index,
            pred_df.values.flatten(),
            color=colors[idx % len(colors)],
            linewidth=1.8,
            linestyle="--",
            label=f"{name} (MAE=${mae:.0f} | MAPE={mae/actual_in_range.values.mean()*100:.2f}%)",
            alpha=0.85,
        )
    # Add vertical line showing prediction start.
    ax.axvline(
        pred_start,
        color="gray",
        linewidth=1.0,
        linestyle=":",
        alpha=0.7,
        label="Prediction start",
    )
    # Configure axes and labels.
    ax.set_xlim(pred_start - buffer, pred_end + buffer)
    # Set y axis to prediction price range with padding.
    all_values = np.concatenate([
        model_predictions[name].values.flatten()
        for name in top_models
    ] + [actual_in_range.values.flatten()])
    y_min = all_values.min() * 0.992
    y_max = all_values.max() * 1.008
    ax.set_ylim(y_min, y_max)
    ax.set_title(
        f"Model Predictions vs Actual S&P 500 | "
        f"{pred_start.date()} to {pred_end.date()}",
        fontsize=14,
        fontweight="bold",
    )
    ax.set_ylabel("S&P 500 Price (USD)", fontsize=11)
    ax.set_xlabel("Date", fontsize=11)
    ax.legend(
        loc="upper left",
        fontsize=8,
        ncol=2,
        framealpha=0.9,
    )
    fig.tight_layout()
    return fig

def select_features_shap(
    master: pd.DataFrame,
    target_col: str,
    past_cov_cols: list,
    correlation_threshold: float,
    shap_importance_threshold: float,
) -> list:
    """
    Select optimal features using correlation filtering and SHAP values.

    Two step feature selection is applied. First features with
    correlation above the threshold are identified and the less
    important one from each correlated pair is removed. Second
    a LightGBM model is trained on remaining features and SHAP
    values identify the features contributing the most predictive
    power. Features explaining the top fraction of total SHAP
    importance are retained.

    :param master: master DataFrame containing target and all features
    :param target_col: name of the target column e.g. `'Close'`
    :param past_cov_cols: list of past covariate column names to
        evaluate for selection
    :param correlation_threshold: remove one feature from pairs with
        absolute correlation above this threshold e.g. `0.95`
    :param shap_importance_threshold: retain features explaining at
        least this fraction of total SHAP importance e.g. `0.90`
    :return: list of selected feature column names after both
        correlation filtering and SHAP selection
    """
    # Extract feature matrix from master DataFrame.
    features = master[past_cov_cols].copy()
    target = master[target_col].copy()
    # Step 1 — Remove highly correlated features.
    _LOG.info(
        "Step 1: Removing features with correlation above %.2f.",
        correlation_threshold,
    )
    # Calculate absolute correlation matrix between all features.
    corr_matrix = features.corr().abs()
    # Find upper triangle of correlation matrix to avoid duplicates.
    upper_triangle = corr_matrix.where(
        np.triu(np.ones(corr_matrix.shape), k=1).astype(bool)
    )
    # Identify features with correlation above threshold.
    to_drop = [
        col for col in upper_triangle.columns
        if any(upper_triangle[col] > correlation_threshold)
    ]
    # Remove highly correlated features from feature set.
    features_filtered = features.drop(columns=to_drop)
    _LOG.info(
        "Removed %d highly correlated features — %d remaining.",
        len(to_drop),
        len(features_filtered.columns),
    )
    _LOG.info("Dropped correlated features: %s", to_drop)
    # Step 2 — SHAP feature importance on remaining features.
    _LOG.info("Step 2: Calculating SHAP values using LightGBM.")
    # Calculate daily returns as target for SHAP analysis since
    # returns are more stationary than price levels.
    returns = target.pct_change().dropna()
    features_aligned = features_filtered.loc[returns.index]
    # Train LightGBM on returns with all remaining features.
    lgbm = sklearn.ensemble.GradientBoostingRegressor(
        n_estimators=100,
        learning_rate=0.05,
        max_depth=4,
        random_state=42,
    )
    lgbm.fit(features_aligned.ffill().bfill(), returns)
    # Calculate SHAP values using TreeExplainer.
    explainer = shap.TreeExplainer(lgbm)
    shap_values = explainer.shap_values(
        features_aligned.ffill().bfill()
    )
    # Calculate mean absolute SHAP value per feature.
    mean_shap = np.abs(shap_values).mean(axis=0)
    shap_df = pd.DataFrame({
        "Feature"    : features_aligned.columns,
        "SHAP_Value" : mean_shap,
    }).sort_values("SHAP_Value", ascending=False).reset_index(
        drop=True
    )
    # Calculate cumulative importance as percentage of total.
    total_shap = shap_df["SHAP_Value"].sum()
    shap_df["SHAP_Pct"] = shap_df["SHAP_Value"] / total_shap * 100
    shap_df["Cumulative_Pct"] = shap_df["SHAP_Pct"].cumsum()
    _LOG.info(
        "SHAP importance calculated for %d features.",
        len(shap_df),
    )
    # Select features explaining top fraction of total importance.
    selected = shap_df[
        shap_df["Cumulative_Pct"] <= shap_importance_threshold * 100
    ]["Feature"].tolist()
    # Always include at least the top 5 features.
    if len(selected) < 5:
        selected = shap_df["Feature"].head(5).tolist()
    _LOG.info(
        "Selected %d features explaining %.0f%% of predictions.",
        len(selected),
        shap_importance_threshold * 100,
    )
    _LOG.info("Selected features: %s", selected)
    return selected, shap_df

def compare_feature_versions(
    target_train: darts.timeseries.TimeSeries,
    target_val: darts.timeseries.TimeSeries,
    past_cov_train: darts.timeseries.TimeSeries,
    future_cov_train: darts.timeseries.TimeSeries,
    future_cov_full: darts.timeseries.TimeSeries,
    train: pd.DataFrame,
    val: pd.DataFrame,
    test: pd.DataFrame,
    target_col: str,
    future_cov_cols: list,
    past_cov_cols: list,
    shap_df: pd.DataFrame,
    forecast_horizon: int,
    target_scaler: darts.dataprocessing.transformers.Scaler,
) -> pd.DataFrame:
    """
    Compare ML model performance across different feature set sizes.

    Four versions are trained and evaluated — all features as baseline
    and three SHAP selected subsets at 90 95 and 98 percent cumulative
    importance thresholds. LightGBM is used as the representative ML
    model for comparison since it is the fastest to train. Pre-built
    Darts TimeSeries objects are used directly to avoid frequency
    inference issues with irregular stock market calendars.

    :param target_train: scaled target TimeSeries for training
    :param target_val: scaled target TimeSeries for validation
    :param past_cov_train: scaled past covariates TimeSeries
    :param future_cov_train: scaled future covariates TimeSeries
    :param future_cov_full: scaled full period future covariates
    :param train: training DataFrame for extracting feature subsets
    :param val: validation DataFrame for extracting feature subsets
    :param test: test DataFrame for extracting feature subsets
    :param target_col: name of the target column e.g. `'Close'`
    :param future_cov_cols: list of future covariate column names
    :param past_cov_cols: list of all past covariate column names
    :param shap_df: DataFrame with SHAP importance values
    :param forecast_horizon: number of trading days to forecast ahead
    :param target_scaler: fitted Darts Scaler for inverse transform
    :return: DataFrame comparing validation metrics across all four
        feature versions sorted by MAPE ascending
    """
    # Ensure all selected features exist in past covariate columns.
    valid_past_cols = set(past_cov_cols)
    # Define the four feature versions to compare.
    versions = {
        "All_40_Features": past_cov_cols,
        "SHAP_90pct_Features": [
            f for f in shap_df[
                shap_df["Cumulative_Pct"] <= 90
            ]["Feature"].tolist()
            if f in valid_past_cols
        ],
        "SHAP_95pct_Features": [
            f for f in shap_df[
                shap_df["Cumulative_Pct"] <= 95
            ]["Feature"].tolist()
            if f in valid_past_cols
        ],
        "SHAP_98pct_Features": [
            f for f in shap_df[
                shap_df["Cumulative_Pct"] <= 98
            ]["Feature"].tolist()
            if f in valid_past_cols
        ],
    }
    # Log the number of features per version.
    for name, cols in versions.items():
        _LOG.info("%s → %d features", name, len(cols))
    # Get column names from existing past covariates TimeSeries.
    all_past_cols = past_cov_train.components.tolist()
    # Initialize results list.
    results = []
    # Train and evaluate LightGBM for each feature version.
    for version_name, feature_cols in versions.items():
        try:
            _LOG.info(
                "Training LightGBM with %s (%d features).",
                version_name, len(feature_cols),
            )
            # Find indices of selected features in past covariates.
            feature_indices = [
                all_past_cols.index(f)
                for f in feature_cols
                if f in all_past_cols
            ]
            if not feature_indices:
                _LOG.warning(
                    "%s has no valid feature indices — skipping.",
                    version_name,
                )
                continue
            # Extract feature subset from existing TimeSeries.
            past_subset = past_cov_train.univariate_component(
                feature_indices[0]
            )
            for idx in feature_indices[1:]:
                past_subset = past_subset.stack(
                    past_cov_train.univariate_component(idx)
                )
            # Clean NaN values from target and covariates.
            target_df = target_train.to_dataframe().ffill().bfill()
            target_df.index.freq = "B"
            target_clean = darts.timeseries.TimeSeries.from_dataframe(
                target_df, fill_missing_dates=True, freq="B"
            )
            past_df = past_subset.to_dataframe().ffill().bfill()
            past_df.index.freq = "B"
            past_clean = darts.timeseries.TimeSeries.from_dataframe(
                past_df, fill_missing_dates=True, freq="B"
            )
            future_df = future_cov_train.to_dataframe().ffill().bfill()
            future_df.index.freq = "B"
            future_clean = darts.timeseries.TimeSeries.from_dataframe(
                future_df, fill_missing_dates=True, freq="B"
            )
            future_full_df = future_cov_full.to_dataframe().ffill().bfill()
            future_full_df.index.freq = "B"
            future_full_clean = darts.timeseries.TimeSeries.from_dataframe(
                future_full_df, fill_missing_dates=True, freq="B"
            )
            # Train LightGBM with this feature subset.
            model = darts.models.LightGBMModel(
                lags=30,
                lags_past_covariates=30,
                lags_future_covariates=[0],
                output_chunk_length=forecast_horizon,
                n_estimators=200,
                num_leaves=31,
                learning_rate=0.05,
                random_state=42,
                verbose=-1,
            )
            model.fit(
                target_clean,
                past_covariates=past_clean,
                future_covariates=future_clean,
            )
            prediction = model.predict(
                forecast_horizon,
                past_covariates=past_clean,
                future_covariates=future_full_clean,
            )
            # Evaluate prediction against validation set.
            val_df = target_val.to_dataframe().ffill().bfill()
            val_df.index.freq = "B"
            val_clean = darts.timeseries.TimeSeries.from_dataframe(
                val_df, fill_missing_dates=True, freq="B"
            )
            actual_df = target_scaler.inverse_transform(
                val_clean
            ).to_dataframe().dropna()
            pred_df = prediction.to_dataframe().ffill().bfill()
            pred_df.index.freq = "B"
            pred_clean_ts = darts.timeseries.TimeSeries.from_dataframe(
                pred_df, fill_missing_dates=True, freq="B"
            )
            pred_inverse_df = target_scaler.inverse_transform(
                pred_clean_ts
            ).to_dataframe().dropna()
            # Align by common dates.
            common_dates = actual_df.index.intersection(
                pred_inverse_df.index
            )
            if len(common_dates) < 5:
                _LOG.warning(
                    "%s insufficient common dates — skipping.",
                    version_name,
                )
                continue
            actual = actual_df.loc[common_dates].values.flatten()
            predicted = pred_inverse_df.loc[
                common_dates
            ].values.flatten()
            # Calculate evaluation metrics.
            mae = float(np.mean(np.abs(actual - predicted)))
            rmse = float(
                np.sqrt(np.mean((actual - predicted) ** 2))
            )
            mape = float(
                np.mean(
                    np.abs((actual - predicted) / actual)
                ) * 100
            )
            r2 = float(
                1 - np.sum((actual - predicted) ** 2)
                / np.sum((actual - np.mean(actual)) ** 2)
            )
            results.append({
                "Version"  : version_name,
                "Features" : len(feature_cols),
                "MAE"      : round(mae, 2),
                "RMSE"     : round(rmse, 2),
                "MAPE"     : round(mape, 2),
                "R2"       : round(r2, 4),
                "Days"     : len(common_dates),
            })
            _LOG.info(
                "%s → MAPE: %.2f%% | RMSE: %.2f | R2: %.4f",
                version_name, mape, rmse, r2,
            )
        except Exception as e:
            _LOG.warning(
                "%s failed: %s — skipping.", version_name, str(e)
            )
    # Return empty DataFrame if no results.
    if not results:
        _LOG.warning("No feature versions completed successfully.")
        return pd.DataFrame(
            columns=[
                "Version", "Features", "MAE",
                "RMSE", "MAPE", "R2", "Days"
            ]
        )
    # Sort by MAPE ascending.
    return pd.DataFrame(results).sort_values(
        "MAPE", ascending=True
    ).reset_index(drop=True)

def tune_ml_models(
    target_train: darts.timeseries.TimeSeries,
    target_val: darts.timeseries.TimeSeries,
    past_cov_train: darts.timeseries.TimeSeries,
    future_cov_train: darts.timeseries.TimeSeries,
    future_cov_full: darts.timeseries.TimeSeries,
    target_scaler: darts.dataprocessing.transformers.Scaler,
    forecast_horizon: int,
    feature_set_name: str,
    n_trials: int = 20,
) -> pd.DataFrame:
    """
    Tune hyperparameters for LightGBM XGBoost and RandomForest
    using Optuna Bayesian optimization.

    Optuna intelligently searches the hyperparameter space by
    learning from previous trial results — finding better parameters
    in fewer iterations than grid or random search. For each model
    both validation MAPE and the train versus validation gap are
    recorded to detect overfitting. Results are sorted by validation
    MAPE ascending.

    :param target_train: scaled target TimeSeries for training
    :param target_val: scaled target TimeSeries for validation
    :param past_cov_train: scaled past covariates TimeSeries
    :param future_cov_train: scaled future covariates TimeSeries
    :param future_cov_full: full period future covariates TimeSeries
    :param target_scaler: fitted Darts Scaler for inverse transform
    :param forecast_horizon: number of trading days to forecast ahead
    :param feature_set_name: name of feature set for logging
        e.g. `'7_features'` or `'10_features'`
    :param n_trials: number of Optuna trials per model default is 20
    :return: DataFrame with tuning results sorted by val MAPE
    """
    # Fill NaN values using Darts MissingValuesFiller.
    filler = darts.dataprocessing.transformers.MissingValuesFiller()
    target_clean = filler.transform(target_train)
    target_val_clean = filler.transform(target_val)
    past_clean = filler.transform(past_cov_train)
    future_clean = filler.transform(future_cov_train)
    future_full_clean = filler.transform(future_cov_full)
    # Initialize results list.
    results = []

    def _evaluate_prediction(
        prediction: darts.timeseries.TimeSeries,
        actual_df: pd.DataFrame,
    ) -> float:
        """
        Evaluate a prediction against actual values returning MAPE.

        :param prediction: Darts TimeSeries prediction
        :param actual_df: DataFrame with actual values
        :return: MAPE as float or infinity if evaluation fails
        """
        try:
            pred_df = target_scaler.inverse_transform(
                filler.transform(prediction)
            ).to_dataframe().dropna()
            common_dates = actual_df.index.intersection(pred_df.index)
            if len(common_dates) < 5:
                return float("inf")
            actual = actual_df.loc[common_dates].values.flatten()
            predicted = pred_df.loc[common_dates].values.flatten()
            return float(
                np.mean(np.abs((actual - predicted) / actual)) * 100
            )
        except Exception:
            return float("inf")

    # Pre-compute actual validation values once for efficiency.
    val_df = target_val_clean.to_dataframe().ffill().bfill()
    val_df.index.freq = "B"
    val_ts = darts.timeseries.TimeSeries.from_dataframe(
        val_df, fill_missing_dates=True, freq="B"
    )
    actual_val_df = target_scaler.inverse_transform(
        val_ts
    ).to_dataframe().dropna()
    # Pre-compute actual training values for overfitting check.
    train_df = target_clean.to_dataframe().ffill().bfill()
    train_df.index.freq = "B"
    train_ts = darts.timeseries.TimeSeries.from_dataframe(
        train_df, fill_missing_dates=True, freq="B"
    )
    actual_train_df = target_scaler.inverse_transform(
        train_ts
    ).to_dataframe().dropna()

    def _make_objective(model_name: str):
        """
        Create Optuna objective function for a specific model.

        :param model_name: name of the model to tune
        :return: objective function for Optuna to minimize
        """
        def objective(trial: optuna.Trial) -> float:
            """
            Objective function minimizing validation MAPE.

            :param trial: Optuna trial object for parameter suggestion
            :return: validation MAPE to minimize
            """
            # Define hyperparameter search space per model.
            lags = trial.suggest_int("lags", 10, 60)
            n_estimators = trial.suggest_int("n_estimators", 50, 400)
            if model_name == "LightGBM":
                num_leaves = trial.suggest_int("num_leaves", 10, 80)
                learning_rate = trial.suggest_float(
                    "learning_rate", 0.005, 0.1, log=True
                )
                model = darts.models.LightGBMModel(
                    lags=lags,
                    lags_past_covariates=lags,
                    lags_future_covariates=[0],
                    output_chunk_length=forecast_horizon,
                    n_estimators=n_estimators,
                    num_leaves=num_leaves,
                    learning_rate=learning_rate,
                    random_state=42,
                    verbose=-1,
                )
            elif model_name == "XGBoost":
                max_depth = trial.suggest_int("max_depth", 3, 10)
                learning_rate = trial.suggest_float(
                    "learning_rate", 0.005, 0.1, log=True
                )
                model = darts.models.XGBModel(
                    lags=lags,
                    lags_past_covariates=lags,
                    lags_future_covariates=[0],
                    output_chunk_length=forecast_horizon,
                    n_estimators=n_estimators,
                    max_depth=max_depth,
                    learning_rate=learning_rate,
                    random_state=42,
                    verbosity=0,
                )
            elif model_name == "RandomForest":
                max_depth = trial.suggest_int("max_depth", 5, 30)
                model = darts.models.RandomForestModel(
                    lags=lags,
                    lags_past_covariates=lags,
                    lags_future_covariates=[0],
                    output_chunk_length=forecast_horizon,
                    n_estimators=n_estimators,
                    max_depth=max_depth,
                    random_state=42,
                )
            # Train model and generate predictions.
            model.fit(
                target_clean,
                past_covariates=past_clean,
                future_covariates=future_clean,
            )
            val_pred = model.predict(
                forecast_horizon,
                past_covariates=past_clean,
                future_covariates=future_full_clean,
            )
            return _evaluate_prediction(val_pred, actual_val_df)
        return objective

    # Run Optuna optimization for each model.
    for model_name in ["LightGBM", "XGBoost", "RandomForest"]:
        _LOG.info(
            "Tuning %s on %s with %d trials.",
            model_name,
            feature_set_name,
            n_trials,
        )
        # Create Optuna study minimizing validation MAPE.
        # Suppress Optuna logging to keep output clean.
        optuna.logging.set_verbosity(optuna.logging.WARNING)
        study = optuna.create_study(
            direction="minimize",
            sampler=optuna.samplers.TPESampler(seed=42),
        )
        study.optimize(
            _make_objective(model_name),
            n_trials=n_trials,
            show_progress_bar=True,
        )
        # Get best parameters from study.
        best_params = study.best_params
        best_val_mape = study.best_value
        _LOG.info(
            "%s best params: %s → Val MAPE: %.4f%%",
            model_name,
            best_params,
            best_val_mape,
        )
        # Retrain best model to get train MAPE for overfitting check.
        lags = best_params["lags"]
        n_estimators = best_params["n_estimators"]
        try:
            if model_name == "LightGBM":
                best_model = darts.models.LightGBMModel(
                    lags=lags,
                    lags_past_covariates=lags,
                    lags_future_covariates=[0],
                    output_chunk_length=forecast_horizon,
                    n_estimators=n_estimators,
                    num_leaves=best_params["num_leaves"],
                    learning_rate=best_params["learning_rate"],
                    random_state=42,
                    verbose=-1,
                )
            elif model_name == "XGBoost":
                best_model = darts.models.XGBModel(
                    lags=lags,
                    lags_past_covariates=lags,
                    lags_future_covariates=[0],
                    output_chunk_length=forecast_horizon,
                    n_estimators=n_estimators,
                    max_depth=best_params["max_depth"],
                    learning_rate=best_params["learning_rate"],
                    random_state=42,
                    verbosity=0,
                )
            elif model_name == "RandomForest":
                best_model = darts.models.RandomForestModel(
                    lags=lags,
                    lags_past_covariates=lags,
                    lags_future_covariates=[0],
                    output_chunk_length=forecast_horizon,
                    n_estimators=n_estimators,
                    max_depth=best_params["max_depth"],
                    random_state=42,
                )
            # Retrain best model.
            best_model.fit(
                target_clean,
                past_covariates=past_clean,
                future_covariates=future_clean,
            )
            # Get train prediction for overfitting check.
            train_pred = best_model.predict(
                forecast_horizon,
                past_covariates=past_clean,
                future_covariates=future_full_clean,
            )
            train_mape = _evaluate_prediction(
                train_pred, actual_train_df
            )
            overfit_gap = best_val_mape - train_mape
        except Exception as e:
            _LOG.warning(
                "Could not compute train MAPE for %s: %s",
                model_name,
                str(e),
            )
            train_mape = float("nan")
            overfit_gap = float("nan")
        results.append({
            "Model"        : model_name,
            "Feature_Set"  : feature_set_name,
            "Best_Params"  : str(best_params),
            "Val_MAPE"     : round(best_val_mape, 4),
            "Train_MAPE"   : round(train_mape, 4),
            "Overfit_Gap"  : round(overfit_gap, 4),
            "N_Trials"     : n_trials,
        })
    # Sort by validation MAPE ascending.
    if not results:
        _LOG.warning("No tuning results produced.")
        return pd.DataFrame()
    return pd.DataFrame(results).sort_values(
        "Val_MAPE", ascending=True
    ).reset_index(drop=True)
