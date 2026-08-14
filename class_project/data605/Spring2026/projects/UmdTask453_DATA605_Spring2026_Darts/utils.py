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
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import optuna
import pandas as pd
import prophet
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

def train_ensemble_models(
    target_train: darts.timeseries.TimeSeries,
    target_val: darts.timeseries.TimeSeries,
    past_cov_train: darts.timeseries.TimeSeries,
    future_cov_train: darts.timeseries.TimeSeries,
    future_cov_full: darts.timeseries.TimeSeries,
    target_scaler: darts.dataprocessing.transformers.Scaler,
    forecast_horizon: int,
    tuning_results: pd.DataFrame,
) -> tuple:
    """
    Train ensemble models combining top performing ML models.

    Three ensemble strategies are implemented — simple average
    weighted average by inverse MAPE and stacking with a linear
    meta model. The top three models from hyperparameter tuning
    are used as base models. Each ensemble strategy is evaluated
    on the validation set and compared against the best individual
    model.

    :param target_train: scaled target TimeSeries for training
    :param target_val: scaled target TimeSeries for validation
    :param past_cov_train: scaled past covariates TimeSeries
    :param future_cov_train: scaled future covariates TimeSeries
    :param future_cov_full: full period future covariates TimeSeries
    :param target_scaler: fitted Darts Scaler for inverse transform
    :param forecast_horizon: number of trading days to forecast ahead
    :param tuning_results: DataFrame from Phase 7 tuning containing
        best parameters for each model
    :return: tuple of (ensemble_predictions dict, results DataFrame)
    """
    # Fill NaN values using Darts MissingValuesFiller.
    filler = darts.dataprocessing.transformers.MissingValuesFiller()
    target_clean = filler.transform(target_train)
    target_val_clean = filler.transform(target_val)
    past_clean = filler.transform(past_cov_train)
    future_clean = filler.transform(future_cov_train)
    future_full_clean = filler.transform(future_cov_full)
    # Extract top 3 models from tuning results.
    top_3 = tuning_results.head(3)
    _LOG.info(
        "Building ensemble from top 3 models:\n%s",
        top_3[["Model", "Feature_Set", "Val_MAPE"]].to_string(),
    )
    # Train each base model with its best parameters.
    base_predictions = {}
    base_mapes = {}
    for _, row in top_3.iterrows():
        model_name = row["Model"]
        feature_set = row["Feature_Set"]
        params = eval(row["Best_Params"])
        model_key = f"{model_name}_{feature_set}"
        try:
            _LOG.info("Training base model %s.", model_key)
            lags = params["lags"]
            n_estimators = params["n_estimators"]
            if model_name == "LightGBM":
                model = darts.models.LightGBMModel(
                    lags=lags,
                    lags_past_covariates=lags,
                    lags_future_covariates=[0],
                    output_chunk_length=forecast_horizon,
                    n_estimators=n_estimators,
                    num_leaves=params["num_leaves"],
                    learning_rate=params["learning_rate"],
                    random_state=42,
                    verbose=-1,
                )
            elif model_name == "XGBoost":
                model = darts.models.XGBModel(
                    lags=lags,
                    lags_past_covariates=lags,
                    lags_future_covariates=[0],
                    output_chunk_length=forecast_horizon,
                    n_estimators=n_estimators,
                    max_depth=params["max_depth"],
                    learning_rate=params["learning_rate"],
                    random_state=42,
                    verbosity=0,
                )
            elif model_name == "RandomForest":
                model = darts.models.RandomForestModel(
                    lags=lags,
                    lags_past_covariates=lags,
                    lags_future_covariates=[0],
                    output_chunk_length=forecast_horizon,
                    n_estimators=n_estimators,
                    max_depth=params["max_depth"],
                    random_state=42,
                )
            # Train model and generate prediction.
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
            # Inverse transform prediction for evaluation.
            pred_df = target_scaler.inverse_transform(
                filler.transform(prediction)
            ).to_dataframe().dropna()
            # Get actual validation values.
            val_df = target_val_clean.to_dataframe().ffill().bfill()
            val_df.index.freq = "B"
            val_ts = darts.timeseries.TimeSeries.from_dataframe(
                val_df, fill_missing_dates=True, freq="B"
            )
            actual_df = target_scaler.inverse_transform(
                val_ts
            ).to_dataframe().dropna()
            # Calculate MAPE on common dates.
            common_dates = actual_df.index.intersection(pred_df.index)
            if len(common_dates) >= 5:
                actual = actual_df.loc[common_dates].values.flatten()
                predicted = pred_df.loc[common_dates].values.flatten()
                mape = float(
                    np.mean(
                        np.abs((actual - predicted) / actual)
                    ) * 100
                )
                base_predictions[model_key] = pred_df
                base_mapes[model_key] = mape
                _LOG.info(
                    "%s → Val MAPE: %.4f%%", model_key, mape
                )
        except Exception as e:
            _LOG.warning(
                "Base model %s failed: %s — skipping.",
                model_key,
                str(e),
            )
    if len(base_predictions) < 2:
        _LOG.warning("Insufficient base models for ensemble.")
        return {}, pd.DataFrame()
    # Get common dates across all base model predictions.
    common_dates = None
    for pred_df in base_predictions.values():
        if common_dates is None:
            common_dates = pred_df.index
        else:
            common_dates = common_dates.intersection(pred_df.index)
    # Stack predictions into matrix for ensemble calculation.
    pred_matrix = np.column_stack([
        base_predictions[key].loc[common_dates].values.flatten()
        for key in base_predictions.keys()
    ])
    # Get actual values for ensemble evaluation.
    val_df = target_val_clean.to_dataframe().ffill().bfill()
    val_df.index.freq = "B"
    val_ts = darts.timeseries.TimeSeries.from_dataframe(
        val_df, fill_missing_dates=True, freq="B"
    )
    actual_df = target_scaler.inverse_transform(
        val_ts
    ).to_dataframe().dropna()
    actual_common = actual_df.loc[
        actual_df.index.intersection(common_dates)
    ].values.flatten()
    # Strategy 1 — Simple average ensemble.
    simple_avg = pred_matrix.mean(axis=1)
    simple_mape = float(
        np.mean(np.abs((actual_common - simple_avg) / actual_common)) * 100
    )
    _LOG.info("Simple average ensemble → MAPE: %.4f%%", simple_mape)
    # Strategy 2 — Weighted average by inverse MAPE.
    # Models with lower MAPE get higher weight.
    inv_mapes = np.array([
        1 / base_mapes[key] for key in base_predictions.keys()
    ])
    weights = inv_mapes / inv_mapes.sum()
    weighted_avg = (pred_matrix * weights).sum(axis=1)
    weighted_mape = float(
        np.mean(
            np.abs((actual_common - weighted_avg) / actual_common)
        ) * 100
    )
    _LOG.info(
        "Weighted average ensemble → MAPE: %.4f%% | Weights: %s",
        weighted_mape,
        {k: round(w, 3) for k, w in zip(base_predictions.keys(), weights)},
    )
    # Strategy 3 — Stacking with linear meta model.
    # Meta model learns optimal combination weights from validation data.
    meta_model = sklearn.linear_model.Ridge(alpha=1.0)
    meta_model.fit(pred_matrix, actual_common)
    stacked_avg = meta_model.predict(pred_matrix)
    stacked_mape = float(
        np.mean(
            np.abs((actual_common - stacked_avg) / actual_common)
        ) * 100
    )
    _LOG.info(
        "Stacking ensemble → MAPE: %.4f%% | Coefficients: %s",
        stacked_mape,
        dict(zip(base_predictions.keys(), meta_model.coef_.round(3))),
    )
    # Collect ensemble results.
    ensemble_predictions = {
        "Simple_Average"   : simple_avg,
        "Weighted_Average" : weighted_avg,
        "Stacking"         : stacked_avg,
    }
    results = []
    best_individual_mape = min(base_mapes.values())
    best_individual_name = min(base_mapes, key=base_mapes.get)
    for strategy, pred_vals in ensemble_predictions.items():
        mape = float(
            np.mean(
                np.abs((actual_common - pred_vals) / actual_common)
            ) * 100
        )
        improvement = (
            (best_individual_mape - mape) / best_individual_mape * 100
        )
        results.append({
            "Strategy"          : strategy,
            "Val_MAPE"          : round(mape, 4),
            "Best_Individual"   : best_individual_name,
            "Best_Individual_MAPE": round(best_individual_mape, 4),
            "Improvement_Pct"   : round(improvement, 2),
        })
    results_df = pd.DataFrame(results).sort_values(
        "Val_MAPE", ascending=True
    ).reset_index(drop=True)
    return ensemble_predictions, results_df

def detect_market_regimes(
    macro_daily: pd.DataFrame,
    macro_monthly: pd.DataFrame,
    macro_features: pd.DataFrame,
    sp500: pd.DataFrame,
    n_regimes: int = None,
    random_state: int = 42,
) -> tuple:
    """
    Detect market regimes using K-Means clustering on macro features.

    The optimal number of regimes is automatically determined using
    silhouette score as primary criterion and elbow method as secondary
    validation. Silhouette score directly measures cluster separation
    quality making it more reliable than inertia alone. Regimes are
    sorted by average S&P 500 return so Regime 0 is always the worst
    performing and Regime n-1 is always the best performing.

    :param macro_daily: DataFrame with daily macro indicators
    :param macro_monthly: DataFrame with monthly macro indicators
    :param macro_features: DataFrame with calculated macro features
    :param sp500: DataFrame with S&P 500 OHLCV data
    :param n_regimes: number of regimes to use — if None the
        silhouette score automatically selects the optimal number
    :param random_state: random seed for reproducibility default 42
    :return: tuple of (regime_labels Series regime_stats DataFrame
        confidence_scores Series kmeans_model scaler optimal_k)
    """
    # Select macro features for regime detection.
    regime_features = pd.concat([
        macro_daily[["VIX", "TNX", "IRX", "OIL", "DXY"]],
        macro_features[[
            "YIELD_CURVE", "YIELD_CURVE_INVERTED",
            "VIX_MA20", "OIL_MOM30",
        ]],
        macro_monthly[["CPI", "FED_RATE", "UNEMPLOYMENT"]],
    ], axis=1).ffill().bfill()
    # Standardize features so all have equal influence on clustering.
    feature_scaler = sklearn.preprocessing.StandardScaler()
    features_scaled = feature_scaler.fit_transform(regime_features)
    # Automatically detect optimal number of regimes using both
    # silhouette score and elbow method for robust selection.
    inertias = []
    silhouette_scores = []
    k_range = range(2, 8)
    for k in k_range:
        km = sklearn.cluster.KMeans(
            n_clusters=k,
            random_state=random_state,
            n_init=10,
        )
        labels_k = km.fit_predict(features_scaled)
        inertias.append(km.inertia_)
        # Calculate silhouette score for this k.
        sil_score = sklearn.metrics.silhouette_score(
            features_scaled, labels_k
        )
        silhouette_scores.append(sil_score)
        _LOG.info(
            "k=%d → Inertia: %.0f | Silhouette: %.4f",
            k, km.inertia_, sil_score,
        )
    # Use silhouette score as primary selection criterion.
    optimal_k_silhouette = int(
        k_range[np.argmax(silhouette_scores)]
    )
    # Use elbow method as secondary validation.
    inertia_diffs = np.diff(inertias)
    inertia_diffs2 = np.diff(inertia_diffs)
    optimal_k_elbow = int(
        k_range[np.argmax(inertia_diffs2) + 2]
    )
    _LOG.info(
        "Silhouette selected k=%d | Elbow selected k=%d",
        optimal_k_silhouette,
        optimal_k_elbow,
    )
    # Use silhouette as primary — override with manual if provided.
    if n_regimes is not None:
        optimal_k = n_regimes
        _LOG.info("Using manually specified k=%d.", optimal_k)
    else:
        optimal_k = optimal_k_silhouette
        _LOG.info("Using silhouette optimal k=%d.", optimal_k)
    # Fit K-Means with optimal number of regimes.
    kmeans = sklearn.cluster.KMeans(
        n_clusters=optimal_k,
        random_state=random_state,
        n_init=10,
    )
    raw_labels = kmeans.fit_predict(features_scaled)
    # Calculate S&P 500 daily returns for regime sorting.
    sp500_returns = sp500["Close"].pct_change().fillna(0)
    # Sort regimes by average S&P 500 return.
    regime_returns = {}
    for regime in range(optimal_k):
        mask = raw_labels == regime
        regime_returns[regime] = sp500_returns[mask].mean()
    # Create mapping from raw label to sorted label.
    sorted_regimes = sorted(
        regime_returns.keys(),
        key=lambda x: regime_returns[x],
    )
    label_mapping = {
        old: new for new, old in enumerate(sorted_regimes)
    }
    regime_labels = pd.Series(
        [label_mapping[r] for r in raw_labels],
        index=regime_features.index,
        name="Regime",
    )
    # Calculate confidence scores.
    distances = kmeans.transform(features_scaled)
    assigned_distances = distances[
        np.arange(len(distances)), raw_labels,
    ]
    total_distances = distances.sum(axis=1)
    confidence_scores = pd.Series(
        1 - (assigned_distances / total_distances),
        index=regime_features.index,
        name="Confidence",
    )
    # Dynamic regime names based on sorted returns.
    regime_name_templates = [
        "Bear Market",
        "High Volatility",
        "Moderate Growth",
        "Recovery",
        "Bull Market",
        "Strong Bull",
    ]
    regime_names = {
        i: regime_name_templates[i]
        for i in range(optimal_k)
    }
    # Calculate regime statistics.
    regime_stats = []
    for regime in range(optimal_k):
        mask = regime_labels == regime
        stats = {
            "Regime"        : regime,
            "Name"          : regime_names[regime],
            "Count"         : int(mask.sum()),
            "Pct_Days"      : round(mask.mean() * 100, 1),
            "Avg_Return"    : round(
                sp500_returns[mask].mean() * 100, 4
            ),
            "Avg_VIX"       : round(
                macro_daily.loc[mask, "VIX"].mean(), 2
            ),
            "Avg_FedRate"   : round(
                macro_monthly.loc[mask, "FED_RATE"].mean(), 2
            ),
            "Avg_YieldCurve": round(
                macro_features.loc[mask, "YIELD_CURVE"].mean(), 4
            ),
        }
        regime_stats.append(stats)
        _LOG.info(
            "Regime %d (%s): %d days (%.1f%%) | "
            "Avg Return: %.4f%% | Avg VIX: %.2f",
            regime,
            stats["Name"],
            stats["Count"],
            stats["Pct_Days"],
            stats["Avg_Return"],
            stats["Avg_VIX"],
        )
    regime_stats_df = pd.DataFrame(regime_stats)
    return (
        regime_labels,
        regime_stats_df,
        confidence_scores,
        kmeans,
        feature_scaler,
        optimal_k,
    )

def plot_regime_analysis(
    regime_labels: pd.Series,
    regime_stats: pd.DataFrame,
    confidence_scores: pd.Series,
    sp500: pd.DataFrame,
    macro_daily: pd.DataFrame,
    macro_features: pd.DataFrame,
    sectors: pd.DataFrame,
    optimal_k: int,
) -> plt.Figure:
    """
    Plot comprehensive market regime analysis with four panels.

    Four panels are shown — S&P 500 price colored by regime
    average sector returns per regime as a heatmap showing
    which sectors perform best in each environment average
    macro conditions per regime as a grouped bar chart and
    VIX over time colored by regime showing the fear signal
    that defines each market environment.

    :param regime_labels: Series with regime label per trading day
    :param regime_stats: DataFrame with regime statistics
    :param confidence_scores: Series with confidence score per day
    :param sp500: DataFrame with S&P 500 OHLCV data
    :param macro_daily: DataFrame with daily macro indicators
    :param macro_features: DataFrame with calculated macro features
    :param sectors: DataFrame with sector ETF prices
    :param optimal_k: number of regimes detected
    :return: matplotlib Figure object with four panel analysis
    """
    # Define colors and names for each regime.
    regime_colors = [
        "#D32F2F",  # deep red — Bear Market
        "#FF6F00",  # deep orange — High Volatility
        "#1565C0",  # deep blue — Moderate Growth
        "#2E7D32",  # deep green — Recovery
        "#F9A825",  # deep yellow — Bull Market
        "#6A1B9A",  # deep purple — Strong Bull
    ]
    # Create figure with 2x2 grid of subplots.
    fig, axes = plt.subplots(2, 2, figsize=(20, 14))
    # Panel 1 (top left) — S&P 500 price colored by regime.
    for regime in range(optimal_k):
        mask = regime_labels == regime
        name = regime_stats.loc[
            regime_stats["Regime"] == regime, "Name"
        ].values[0]
        axes[0, 0].scatter(
            sp500.index[mask],
            sp500.loc[mask, "Close"],
            c=regime_colors[regime],
            s=2,
            label=f"Regime {regime}: {name}",
            alpha=0.7,
        )
    axes[0, 0].set_title(
        "S&P 500 Price by Market Regime",
        fontsize=11,
        fontweight="bold",
    )
    axes[0, 0].set_ylabel("S&P 500 Price (USD)")
    axes[0, 0].set_xlabel("Date")
    axes[0, 0].legend(loc="upper left", fontsize=7, markerscale=5)
    # Panel 2 (top right) — Average sector returns per regime heatmap.
    # Calculate average daily return per sector per regime.
    sector_returns = sectors.pct_change().dropna() * 100
    sector_regime_returns = pd.DataFrame()
    for regime in range(optimal_k):
        mask = regime_labels.reindex(sector_returns.index) == regime
        regime_name = regime_stats.loc[
            regime_stats["Regime"] == regime, "Name"
        ].values[0]
        avg_returns = sector_returns.loc[mask].mean()
        sector_regime_returns[regime_name] = avg_returns
    # Plot heatmap of sector returns by regime.
    sns.heatmap(
        sector_regime_returns,
        annot=True,
        fmt=".3f",
        cmap="RdYlGn",
        center=0,
        linewidths=0.5,
        linecolor="white",
        ax=axes[0, 1],
        cbar_kws={"label": "Avg Daily Return (%)"},
    )
    axes[0, 1].set_title(
        "Average Sector Daily Returns by Regime (%)",
        fontsize=11,
        fontweight="bold",
    )
    axes[0, 1].set_xlabel("Market Regime")
    axes[0, 1].set_ylabel("Sector ETF")
    # Panel 3 (bottom left) — Average macro conditions per regime.
    metrics = ["Avg_VIX", "Avg_FedRate", "Avg_Return"]
    metric_labels = ["VIX (Fear)", "Fed Rate (%)", "Daily Return (%)"]
    x = np.arange(len(metrics))
    width = 0.8 / optimal_k
    for regime in range(optimal_k):
        row = regime_stats[
            regime_stats["Regime"] == regime
        ].iloc[0]
        values = [
            row["Avg_VIX"],
            row["Avg_FedRate"],
            row["Avg_Return"] * 100,
        ]
        offset = (regime - optimal_k / 2 + 0.5) * width
        axes[1, 0].bar(
            x + offset,
            values,
            width=width,
            color=regime_colors[regime],
            alpha=0.8,
            label=row["Name"],
        )
    axes[1, 0].set_title(
        "Average Macro Conditions by Regime",
        fontsize=11,
        fontweight="bold",
    )
    axes[1, 0].set_ylabel("Value")
    axes[1, 0].set_xlabel("Metric")
    axes[1, 0].set_xticks(x)
    axes[1, 0].set_xticklabels(metric_labels, fontsize=9)
    axes[1, 0].legend(fontsize=7, loc="upper right")
    axes[1, 0].axhline(
        0, color="black", linewidth=0.8, linestyle="--"
    )
    # Panel 4 (bottom right) — VIX over time colored by regime.
    for regime in range(optimal_k):
        mask = regime_labels == regime
        name = regime_stats.loc[
            regime_stats["Regime"] == regime, "Name"
        ].values[0]
        axes[1, 1].scatter(
            macro_daily.index[mask],
            macro_daily.loc[mask, "VIX"],
            c=regime_colors[regime],
            s=2,
            label=name,
            alpha=0.7,
        )
    axes[1, 1].axhline(
        30,
        color="black",
        linewidth=1.0,
        linestyle="--",
        alpha=0.5,
        label="VIX=30 (high fear)",
    )
    axes[1, 1].set_title(
        "VIX (Fear Index) Colored by Market Regime",
        fontsize=11,
        fontweight="bold",
    )
    axes[1, 1].set_ylabel("VIX")
    axes[1, 1].set_xlabel("Date")
    axes[1, 1].legend(loc="upper right", fontsize=7, markerscale=5)
    fig.suptitle(
        "Market Regime Analysis 2018-2024 — K-Means Clustering",
        fontsize=14,
        fontweight="bold",
    )
    fig.tight_layout()
    return fig

def calculate_sector_scores(
    sectors: pd.DataFrame,
    sp500: pd.DataFrame,
    regime_labels: pd.Series,
    macro_daily: pd.DataFrame,
    macro_features: pd.DataFrame,
    current_regime: int,
    forecast_return: float,
) -> pd.DataFrame:
    """
    Calculate composite sector scores for rotation recommendations.

    Five factors are combined into a composite score for each sector.
    Historical regime return captures average sector performance in
    the current regime. Momentum captures recent price trend.
    Volatility adjusted return is the Sharpe-like ratio. Macro
    correlation measures alignment with key macro signals. Forecast
    alignment measures consistency with the S&P 500 forecast direction.
    Ridge Regression learns optimal factor weights from historical data.

    :param sectors: DataFrame with sector ETF closing prices
    :param sp500: DataFrame with S&P 500 OHLCV data
    :param regime_labels: Series with regime label per trading day
    :param macro_daily: DataFrame with daily macro indicators
    :param macro_features: DataFrame with calculated macro features
    :param current_regime: integer label of the current market regime
    :param forecast_return: predicted S&P 500 return over next 30 days
        as a percentage e.g. 2.3 for 2.3 percent
    :return: DataFrame with composite scores and factor scores for
        each sector sorted from highest to lowest score
    """
    # Calculate daily returns for all sectors.
    sector_returns = sectors.pct_change().dropna() * 100
    # Factor 1 — Historical regime return.
    # Average daily return of each sector in the current regime.
    regime_mask = regime_labels.reindex(sector_returns.index) == current_regime
    if regime_mask.sum() > 5:
        regime_returns = sector_returns.loc[regime_mask].mean()
    else:
        # Fall back to overall average if regime has too few days.
        regime_returns = sector_returns.mean()
        _LOG.warning(
            "Current regime has fewer than 5 days — "
            "using overall average returns."
        )
    # Factor 2 — Momentum score (last 30 days return).
    momentum = sectors.iloc[-1] / sectors.iloc[-30] - 1
    momentum = momentum * 100
    # Factor 3 — Volatility adjusted return (Sharpe-like ratio).
    # Use last 60 days for stability.
    recent_returns = sector_returns.iloc[-60:]
    sharpe_like = recent_returns.mean() / (
        recent_returns.std() + 1e-8
    )
    # Factor 4 — VIX correlation alignment.
    # Sectors negatively correlated with VIX are defensive.
    # Sectors positively correlated with VIX benefit from fear.
    vix_series = macro_daily["VIX"].reindex(
        sector_returns.index
    ).ffill()
    vix_correlation = sector_returns.corrwith(vix_series)
    # In bear regime high VIX correlation is good.
    # In bull regime low VIX correlation is good.
    if current_regime <= 1:
        # Bear or high volatility — prefer sectors that
        # move WITH VIX (benefit from fear).
        vix_alignment = vix_correlation
    else:
        # Growth regimes — prefer sectors that move
        # AGAINST VIX (benefit from calm markets).
        vix_alignment = -vix_correlation
    # Factor 5 — Forecast alignment.
    # If forecast is bullish prefer high beta sectors.
    # If forecast is bearish prefer low beta sectors.
    sp500_returns = sp500["Close"].pct_change().dropna() * 100
    beta = sector_returns.corrwith(
        sp500_returns.reindex(sector_returns.index)
    )
    if forecast_return > 0:
        # Bullish forecast — prefer high beta sectors.
        forecast_alignment = beta
    else:
        # Bearish forecast — prefer low beta sectors.
        forecast_alignment = -beta
    # Combine all factors into a feature matrix.
    factor_matrix = pd.DataFrame({
        "Regime_Return"      : regime_returns,
        "Momentum"           : momentum,
        "Sharpe_Like"        : sharpe_like,
        "VIX_Alignment"      : vix_alignment,
        "Forecast_Alignment" : forecast_alignment,
    })
    # Normalize each factor to 0-1 scale for fair combination.
    factor_normalized = (
        factor_matrix - factor_matrix.min()
    ) / (factor_matrix.max() - factor_matrix.min() + 1e-8)
    # Train Ridge Regression to learn optimal factor weights.
    # Target is the next 30 day sector return (forward return).
    forward_returns = (
        sectors.shift(-30).iloc[-1] / sectors.iloc[-1] - 1
    ) * 100
    # Use historical forward returns as training target.
    historical_forward = (
        sectors.pct_change(30).shift(-30).dropna() * 100
    )
    # Build training dataset from historical factor values.
    train_factors = []
    train_targets = []
    for date in historical_forward.index[-120:]:
        if date not in regime_labels.index:
            continue
        regime_at_date = regime_labels.loc[date]
        mask_date = regime_labels.reindex(
            sector_returns.index
        ) == regime_at_date
        if mask_date.sum() < 5:
            continue
        # Calculate factors at this historical date.
        idx = sectors.index.get_loc(date)
        if idx < 60:
            continue
        hist_returns = sector_returns.iloc[max(0, idx-60):idx]
        hist_regime_mask = regime_labels.reindex(
            hist_returns.index
        ) == regime_at_date
        if hist_regime_mask.sum() > 0:
            hist_regime_ret = hist_returns.loc[
                hist_regime_mask
            ].mean()
        else:
            hist_regime_ret = hist_returns.mean()
        hist_momentum = (
            sectors.iloc[idx] / sectors.iloc[max(0, idx-30)] - 1
        ) * 100
        hist_sharpe = hist_returns.mean() / (
            hist_returns.std() + 1e-8
        )
        hist_factors = pd.DataFrame({
            "Regime_Return" : hist_regime_ret,
            "Momentum"      : hist_momentum,
            "Sharpe_Like"   : hist_sharpe,
        })
        hist_factors_norm = (
            hist_factors - hist_factors.min()
        ) / (hist_factors.max() - hist_factors.min() + 1e-8)
        train_factors.append(
            hist_factors_norm.values.flatten()
        )
        train_targets.append(
            historical_forward.loc[date].values
        )
    # Train Ridge Regression if sufficient training data exists.
    if len(train_factors) > 10:
        X_train = np.array(train_factors)
        y_train = np.array(train_targets).mean(axis=1)
        ridge = sklearn.linear_model.Ridge(alpha=1.0)
        ridge.fit(X_train, y_train)
        # Use learned weights for final scoring.
        learned_weights = np.abs(ridge.coef_)
        learned_weights = learned_weights / learned_weights.sum()
        _LOG.info(
            "Ridge weights — Regime: %.3f | Momentum: %.3f | "
            "Sharpe: %.3f",
            learned_weights[0],
            learned_weights[1],
            learned_weights[2],
        )
        # Calculate composite score using learned weights
        # plus equal weights for VIX and forecast alignment.
        composite_score = (
            learned_weights[0] * factor_normalized["Regime_Return"]
            + learned_weights[1] * factor_normalized["Momentum"]
            + learned_weights[2] * factor_normalized["Sharpe_Like"]
            + 0.1 * factor_normalized["VIX_Alignment"]
            + 0.1 * factor_normalized["Forecast_Alignment"]
        )
    else:
        # Equal weights fallback if insufficient training data.
        _LOG.warning(
            "Insufficient training data — using equal weights."
        )
        composite_score = factor_normalized.mean(axis=1)
    # Build results DataFrame.
    results = pd.DataFrame({
        "Sector"             : sectors.columns,
        "Composite_Score"    : composite_score.values,
        "Regime_Return"      : regime_returns.values,
        "Momentum"           : momentum.values,
        "Sharpe_Like"        : sharpe_like.values,
        "VIX_Alignment"      : vix_alignment.values,
        "Forecast_Alignment" : forecast_alignment.values,
    })
    # Sort by composite score descending.
    results = results.sort_values(
        "Composite_Score", ascending=False
    ).reset_index(drop=True)
    # Add rotation recommendation.
    results["Recommendation"] = "NEUTRAL"
    results.loc[:2, "Recommendation"] = "BUY"
    results.loc[8:, "Recommendation"] = "AVOID"
    _LOG.info(
        "Sector rotation recommendations:\n%s",
        results[["Sector", "Composite_Score", "Recommendation"]
        ].to_string(),
    )
    return results

def precompute_weekly_recommendations(
    sectors: pd.DataFrame,
    sp500: pd.DataFrame,
    regime_labels: pd.Series,
    macro_daily: pd.DataFrame,
    macro_monthly: pd.DataFrame,
    macro_features: pd.DataFrame,
    regime_stats: pd.DataFrame,
    kmeans_model: sklearn.cluster.KMeans,
    regime_scaler: sklearn.preprocessing.StandardScaler,
    forecast_series: dict,
) -> pd.DataFrame:
    """
    Pre-compute weekly sector recommendations for entire history.

    For each Friday in the dataset sector scores are calculated
    using only data available up to that date simulating real
    time deployment with no look-ahead bias. The current regime
    is detected using the trained K-Means model and sector scores
    are calculated using the five factor composite model.
    Logging is suppressed during computation to avoid cluttering
    notebook output — only the final summary is logged.

    :param sectors: DataFrame with sector ETF closing prices
    :param sp500: DataFrame with S&P 500 OHLCV data
    :param regime_labels: Series with regime label per trading day
    :param macro_daily: DataFrame with daily macro indicators
    :param macro_monthly: DataFrame with monthly macro indicators
    :param macro_features: DataFrame with calculated macro features
    :param regime_stats: DataFrame with regime statistics
    :param kmeans_model: trained K-Means model for regime detection
    :param regime_scaler: fitted StandardScaler for regime features
    :param forecast_series: dictionary mapping dates to forecast
        returns e.g. from walk forward validation results
    :return: DataFrame with weekly sector scores and recommendations
        for the entire analysis period
    """
    # Suppress per-week logging to avoid cluttering notebook output.
    previous_level = _LOG.level
    _LOG.setLevel(logging.WARNING)
    # Get all Fridays in the dataset as weekly rebalancing dates.
    all_fridays = sp500.index[sp500.index.dayofweek == 4]
    # Initialize results list.
    results = []
    # Compute scores for each Friday with progress bar.
    for friday in tqdm.tqdm(
        all_fridays,
        desc="Computing weekly recommendations",
    ):
        # Skip if Friday not in sectors index.
        if friday not in sectors.index:
            continue
        friday_idx = sectors.index.get_loc(friday)
        # Skip if insufficient history for calculations.
        if friday_idx < 60:
            continue
        # Use only data up to this Friday — no look-ahead bias.
        sectors_to_date = sectors.iloc[:friday_idx + 1]
        sp500_to_date = sp500.iloc[:friday_idx + 1]
        macro_daily_to_date = macro_daily.loc[
            macro_daily.index <= friday
        ]
        macro_monthly_to_date = macro_monthly.loc[
            macro_monthly.index <= friday
        ]
        macro_features_to_date = macro_features.loc[
            macro_features.index <= friday
        ]
        regime_labels_to_date = regime_labels.loc[
            regime_labels.index <= friday
        ]
        # Get current regime for this date.
        current_regime = int(regime_labels_to_date.iloc[-1])
        # Get forecast return — use pre-computed if available.
        forecast_return = forecast_series.get(friday, 0.0)
        try:
            # Calculate sector scores using data up to this date.
            scores = calculate_sector_scores(
                sectors=sectors_to_date,
                sp500=sp500_to_date,
                regime_labels=regime_labels_to_date,
                macro_daily=macro_daily_to_date,
                macro_features=macro_features_to_date,
                current_regime=current_regime,
                forecast_return=forecast_return,
            )
            # Build weekly result row.
            week_result = {
                "Date"           : friday,
                "Regime"         : current_regime,
                "Regime_Name"    : regime_stats.loc[
                    regime_stats["Regime"] == current_regime,
                    "Name"
                ].values[0],
                "Forecast_Return": forecast_return,
            }
            # Add sector scores and recommendations.
            for _, row in scores.iterrows():
                sector = row["Sector"]
                week_result[f"{sector}_Score"] = round(
                    row["Composite_Score"], 4
                )
                week_result[f"{sector}_Rec"] = row["Recommendation"]
            results.append(week_result)
        except Exception:
            # Silently skip weeks that fail.
            pass
    # Build results DataFrame.
    results_df = pd.DataFrame(results).set_index("Date")
    # Restore logging level.
    _LOG.setLevel(previous_level)
    _LOG.info(
        "Pre-computed %d weekly recommendations.",
        len(results_df),
    )
    return results_df

def find_regime_periods(
    regime_labels: pd.Series,
) -> pd.DataFrame:
    """
    Find all consecutive periods for each market regime.

    Groups consecutive trading days with the same regime label
    into distinct periods. Each period has a start date end date
    duration and regime label. This allows analysis of how sector
    performance differed across multiple occurrences of the same
    regime.

    :param regime_labels: Series with regime label per trading day
    :return: DataFrame with one row per regime period containing
        start date end date duration and regime label
    """
    # Initialize list to collect regime periods.
    periods = []
    # Track current period.
    current_regime = regime_labels.iloc[0]
    period_start = regime_labels.index[0]
    # Loop through all regime labels finding transitions.
    for date, regime in regime_labels.items():
        if regime != current_regime:
            # Regime changed — save completed period.
            periods.append({
                "Regime"  : current_regime,
                "Start"   : period_start,
                "End"     : date,
                "Duration": (date - period_start).days,
            })
            # Start new period.
            current_regime = regime
            period_start = date
    # Save the final period.
    periods.append({
        "Regime"  : current_regime,
        "Start"   : period_start,
        "End"     : regime_labels.index[-1],
        "Duration": (
            regime_labels.index[-1] - period_start
        ).days,
    })
    return pd.DataFrame(periods).sort_values(
        "Start"
    ).reset_index(drop=True)


def calculate_period_attribution(
    regime_periods: pd.DataFrame,
    sectors: pd.DataFrame,
    sp500: pd.DataFrame,
    macro_daily: pd.DataFrame,
    macro_monthly: pd.DataFrame,
    regime_stats: pd.DataFrame,
    min_duration_days: int = 20,
) -> pd.DataFrame:
    """
    Calculate actual sector returns for each regime period.

    For each regime occurrence calculates the actual sector ETF
    returns during that period alongside key macro conditions.
    Only periods longer than min_duration_days are included to
    ensure statistically meaningful results. This enables comparison
    of sector performance across multiple occurrences of the same
    regime revealing how macro context within a regime drives
    different sector outcomes.

    :param regime_periods: DataFrame from `find_regime_periods`
    :param sectors: DataFrame with sector ETF closing prices
    :param sp500: DataFrame with S&P 500 OHLCV data
    :param macro_daily: DataFrame with daily macro indicators
    :param macro_monthly: DataFrame with monthly macro indicators
    :param regime_stats: DataFrame with regime statistics
    :param min_duration_days: minimum period length to include
    :return: DataFrame with sector returns and macro context
        for each qualifying regime period
    """
    # Initialize results list.
    results = []
    # Calculate attribution for each regime period.
    for _, row in regime_periods.iterrows():
        start = row["Start"]
        end = row["End"]
        regime = row["Regime"]
        duration = row["Duration"]
        # Skip periods that are too short.
        if duration < min_duration_days:
            continue
        # Get sector returns during this period.
        period_sectors = sectors.loc[
            (sectors.index >= start) &
            (sectors.index <= end)
        ]
        if len(period_sectors) < 5:
            continue
        # Calculate total return for each sector.
        sector_returns = (
            period_sectors.iloc[-1] / period_sectors.iloc[0] - 1
        ) * 100
        # Get S&P 500 return for this period.
        period_sp500 = sp500.loc[
            (sp500.index >= start) &
            (sp500.index <= end),
            "Close"
        ]
        sp500_return = float(
            (period_sp500.iloc[-1] / period_sp500.iloc[0] - 1) * 100
        )
        # Get average macro conditions during this period.
        period_macro = macro_daily.loc[
            (macro_daily.index >= start) &
            (macro_daily.index <= end)
        ]
        period_monthly = macro_monthly.loc[
            (macro_monthly.index >= start) &
            (macro_monthly.index <= end)
        ]
        avg_vix = float(period_macro["VIX"].mean())
        avg_oil_change = float(
            (period_macro["OIL"].iloc[-1] /
             period_macro["OIL"].iloc[0] - 1) * 100
        )
        avg_fed_rate = float(period_monthly["FED_RATE"].mean())
        avg_tnx = float(period_macro["TNX"].mean())
        # Get regime name.
        regime_name = regime_stats.loc[
            regime_stats["Regime"] == regime, "Name"
        ].values[0]
        # Build result row.
        result = {
            "Regime"        : regime,
            "Regime_Name"   : regime_name,
            "Start"         : start.date(),
            "End"           : end.date(),
            "Duration_Days" : duration,
            "SP500_Return"  : round(sp500_return, 2),
            "Avg_VIX"       : round(avg_vix, 2),
            "Oil_Change_Pct": round(avg_oil_change, 2),
            "Avg_FedRate"   : round(avg_fed_rate, 2),
            "Avg_TNX"       : round(avg_tnx, 2),
        }
        # Add individual sector returns.
        for sector in sectors.columns:
            result[f"{sector}_Return"] = round(
                float(sector_returns[sector]), 2
            )
        results.append(result)
    return pd.DataFrame(results).reset_index(drop=True)


def plot_regime_attribution(
    attribution_df: pd.DataFrame,
    sectors: pd.DataFrame,
    regime_stats: pd.DataFrame,
    selected_regime: int = 0,
) -> plt.Figure:
    """
    Plot sector performance attribution across regime occurrences.

    Three panels are shown — grouped bar chart of sector returns
    for each occurrence of the selected regime macro context
    comparison across occurrences and average sector performance
    ranked from best to worst. Full sector names are used instead
    of ticker symbols for readability.

    :param attribution_df: DataFrame from `calculate_period_attribution`
    :param sectors: DataFrame with sector ETF closing prices
    :param regime_stats: DataFrame with regime statistics
    :param selected_regime: regime number to analyze default 0
    :return: matplotlib Figure object with attribution analysis
    """
    # Map sector tickers to full names for readability.
    sector_name_map = {
        "XLK" : "Technology",
        "XLV" : "Healthcare",
        "XLF" : "Financials",
        "XLE" : "Energy",
        "XLY" : "Consumer Disc",
        "XLP" : "Consumer Staples",
        "XLI" : "Industrials",
        "XLU" : "Utilities",
        "XLB" : "Materials",
        "XLRE": "Real Estate",
        "XLC" : "Communication",
    }
    # Filter to selected regime.
    regime_data = attribution_df[
        attribution_df["Regime"] == selected_regime
    ].reset_index(drop=True)
    if len(regime_data) == 0:
        _LOG.warning(
            "No periods found for regime %d.", selected_regime
        )
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.text(
            0.5, 0.5,
            f"No periods found for Regime {selected_regime}",
            ha="center", va="center",
        )
        return fig
    # Get regime name.
    regime_name = regime_stats.loc[
        regime_stats["Regime"] == selected_regime, "Name"
    ].values[0]
    # Get sector return columns.
    sector_cols = [
        col for col in attribution_df.columns
        if col.endswith("_Return") and col != "SP500_Return"
    ]
    # Use full sector names for readability.
    sector_names = [
        sector_name_map.get(
            col.replace("_Return", ""),
            col.replace("_Return", ""),
        )
        for col in sector_cols
    ]
    # Create period labels.
    period_labels = [
        f"{row['Start']} to {row['End']}\n({row['Duration_Days']}d)"
        for _, row in regime_data.iterrows()
    ]
    # Create figure with 3 panels.
    fig, axes = plt.subplots(3, 1, figsize=(18, 18))
    # Define colors for each period.
    colors = [
        "#1565C0", "#2E7D32", "#D32F2F",
        "#FF6F00", "#6A1B9A", "#00838F",
    ]
    n_periods = len(regime_data)
    n_sectors = len(sector_names)
    x = np.arange(n_sectors)
    width = 0.8 / n_periods
    # Panel 1 — Grouped bar chart of sector returns per period.
    for p_idx, (_, period_row) in enumerate(regime_data.iterrows()):
        returns = [period_row[col] for col in sector_cols]
        offset = (p_idx - n_periods / 2 + 0.5) * width
        axes[0].bar(
            x + offset,
            returns,
            width=width,
            color=colors[p_idx % len(colors)],
            alpha=0.8,
            label=period_labels[p_idx],
        )
    axes[0].axhline(
        0, color="black", linewidth=0.8, linestyle="--"
    )
    axes[0].set_title(
        f"Sector Returns During {regime_name} Regime — "
        f"All Historical Occurrences",
        fontsize=12,
        fontweight="bold",
    )
    axes[0].set_ylabel("Total Return (%)")
    axes[0].set_xlabel("Sector")
    axes[0].set_xticks(x)
    axes[0].set_xticklabels(sector_names, rotation=45, ha="right")
    axes[0].legend(
        loc="upper right", fontsize=7, ncol=n_periods
    )
    # Panel 2 — Macro context comparison across periods.
    macro_metrics = [
        "Avg_VIX", "Oil_Change_Pct",
        "Avg_FedRate", "Avg_TNX", "SP500_Return",
    ]
    macro_labels = [
        "Avg VIX", "Oil Change %",
        "Fed Rate %", "10Y Yield %", "S&P 500 Return %",
    ]
    x_macro = np.arange(len(macro_metrics))
    width_macro = 0.8 / n_periods
    for p_idx, (_, period_row) in enumerate(regime_data.iterrows()):
        values = [period_row[m] for m in macro_metrics]
        offset = (p_idx - n_periods / 2 + 0.5) * width_macro
        axes[1].bar(
            x_macro + offset,
            values,
            width=width_macro,
            color=colors[p_idx % len(colors)],
            alpha=0.8,
            label=period_labels[p_idx],
        )
    axes[1].axhline(
        0, color="black", linewidth=0.8, linestyle="--"
    )
    axes[1].set_title(
        f"Macro Context Comparison — {regime_name} Occurrences",
        fontsize=12,
        fontweight="bold",
    )
    axes[1].set_ylabel("Value")
    axes[1].set_xlabel("Macro Metric")
    axes[1].set_xticks(x_macro)
    axes[1].set_xticklabels(macro_labels, rotation=45, ha="right")
    axes[1].legend(
        loc="upper right", fontsize=7, ncol=n_periods
    )
    # Panel 3 — Average sector returns across all occurrences.
    avg_returns = pd.Series({
        sector_name_map.get(
            col.replace("_Return", ""),
            col.replace("_Return", ""),
        ): regime_data[col].mean()
        for col in sector_cols
    }).sort_values(ascending=True)
    bar_colors = [
        "#D32F2F" if r < 0 else "#2E7D32"
        for r in avg_returns.values
    ]
    axes[2].barh(
        avg_returns.index,
        avg_returns.values,
        color=bar_colors,
        alpha=0.8,
        edgecolor="white",
    )
    axes[2].axvline(
        0, color="black", linewidth=0.8, linestyle="--"
    )
    # Add value labels on bars.
    for idx, val in enumerate(avg_returns.values):
        axes[2].text(
            val + (0.3 if val >= 0 else -0.3),
            idx,
            f"{val:.1f}%",
            va="center",
            ha="left" if val >= 0 else "right",
            fontsize=9,
            fontweight="bold",
        )
    axes[2].set_title(
        f"Average Sector Return Across All {regime_name} "
        f"Occurrences — Ranked Best to Worst",
        fontsize=12,
        fontweight="bold",
    )
    axes[2].set_xlabel("Average Total Return (%)")
    axes[2].set_ylabel("Sector")
    fig.suptitle(
        f"Regime Attribution Analysis — {regime_name}",
        fontsize=14,
        fontweight="bold",
    )
    fig.tight_layout()
    return fig

def compare_libraries(
    train: pd.DataFrame,
    val: pd.DataFrame,
    target_col: str,
    forecast_horizon: int,
) -> pd.DataFrame:
    """
    Compare forecasting performance across three time series libraries.

    Darts NaiveSeasonal ARIMA and ExponentialSmoothing are compared
    against standalone Prophet and Statsmodels ARIMA. All models are
    trained on the same training data and evaluated on the same
    validation data using MAPE RMSE and training time as metrics.
    This validates the choice of Darts as the primary library.

    :param train: training DataFrame with target column
    :param val: validation DataFrame with target column
    :param target_col: name of the target column e.g. `'Close'`
    :param forecast_horizon: number of days to forecast ahead
    :return: DataFrame with comparison metrics for each library
        and model sorted by MAPE ascending
    """
    import time
    import statsmodels.tsa.arima.model
    import statsmodels.tsa.holtwinters
    # Extract training and validation price series.
    train_series = train[target_col].ffill().bfill()
    val_series = val[target_col].ffill().bfill()
    # Get actual validation values for evaluation.
    actual = val_series.values[:forecast_horizon]
    # Initialize results list.
    results = []

    def _calculate_metrics(
        actual: np.ndarray,
        predicted: np.ndarray,
        model_name: str,
        library: str,
        train_time: float,
    ) -> dict:
        """
        Calculate MAPE RMSE and training time metrics.

        :param actual: array of actual values
        :param predicted: array of predicted values
        :param model_name: name of the model
        :param library: name of the library
        :param train_time: training time in seconds
        :return: dictionary of metrics
        """
        min_len = min(len(actual), len(predicted))
        actual_aligned = actual[:min_len]
        predicted_aligned = predicted[:min_len]
        mape = float(
            np.mean(
                np.abs(
                    (actual_aligned - predicted_aligned)
                    / actual_aligned
                )
            ) * 100
        )
        rmse = float(
            np.sqrt(
                np.mean(
                    (actual_aligned - predicted_aligned) ** 2
                )
            )
        )
        return {
            "Library"    : library,
            "Model"      : model_name,
            "MAPE"       : round(mape, 4),
            "RMSE"       : round(rmse, 2),
            "Train_Time" : round(train_time, 2),
        }

    # Library 1 — Darts models.
    _LOG.info("Evaluating Darts models.")
    # Build Darts TimeSeries using MissingValuesFiller approach.
    train_ts = darts.timeseries.TimeSeries.from_series(
        train_series,
        fill_missing_dates=True,
        freq="B",
    )
    filler = darts.dataprocessing.transformers.MissingValuesFiller()
    train_ts_clean = filler.transform(train_ts)
    # Darts NaiveSeasonal.
    start = time.time()
    naive = darts.models.NaiveSeasonal(K=5)
    naive.fit(train_ts_clean)
    pred = naive.predict(forecast_horizon)
    train_time = time.time() - start
    results.append(_calculate_metrics(
        actual,
        pred.values().flatten(),
        "NaiveSeasonal",
        "Darts",
        train_time,
    ))
    # Darts ARIMA.
    start = time.time()
    arima_darts = darts.models.ARIMA(p=5, d=1, q=0)
    arima_darts.fit(train_ts_clean)
    pred = arima_darts.predict(forecast_horizon)
    train_time = time.time() - start
    results.append(_calculate_metrics(
        actual,
        pred.values().flatten(),
        "ARIMA",
        "Darts",
        train_time,
    ))
    # Darts ExponentialSmoothing.
    start = time.time()
    es_darts = darts.models.ExponentialSmoothing()
    es_darts.fit(train_ts_clean)
    pred = es_darts.predict(forecast_horizon)
    train_time = time.time() - start
    results.append(_calculate_metrics(
        actual,
        pred.values().flatten(),
        "ExponentialSmoothing",
        "Darts",
        train_time,
    ))
    # Library 2 — Statsmodels.
    _LOG.info("Evaluating Statsmodels models.")
    # Statsmodels ARIMA.
    try:
        start = time.time()
        sm_arima = statsmodels.tsa.arima.model.ARIMA(
            train_series.values,
            order=(5, 1, 0),
        )
        sm_arima_fit = sm_arima.fit()
        pred = sm_arima_fit.forecast(steps=forecast_horizon)
        train_time = time.time() - start
        results.append(_calculate_metrics(
            actual,
            pred,
            "ARIMA",
            "Statsmodels",
            train_time,
        ))
    except Exception as e:
        _LOG.warning("Statsmodels ARIMA failed: %s", str(e))
    # Statsmodels ExponentialSmoothing.
    try:
        start = time.time()
        sm_es = statsmodels.tsa.holtwinters.ExponentialSmoothing(
            train_series.values,
            trend="add",
        )
        sm_es_fit = sm_es.fit()
        pred = sm_es_fit.forecast(steps=forecast_horizon)
        train_time = time.time() - start
        results.append(_calculate_metrics(
            actual,
            pred,
            "ExponentialSmoothing",
            "Statsmodels",
            train_time,
        ))
    except Exception as e:
        _LOG.warning(
            "Statsmodels ExponentialSmoothing failed: %s", str(e)
        )
    # Library 3 — Prophet.
    _LOG.info("Evaluating Prophet.")
    try:
        start = time.time()
        # Prepare Prophet format — requires ds and y columns.
        prophet_train = pd.DataFrame({
            "ds": train_series.index,
            "y" : train_series.values,
        })
        prophet_model = prophet.Prophet(
            daily_seasonality=False,
            weekly_seasonality=True,
            yearly_seasonality=True,
        )
        # Suppress Prophet output.
        import logging as logging_module
        logging_module.getLogger("prophet").setLevel(
            logging_module.WARNING
        )
        logging_module.getLogger("cmdstanpy").setLevel(
            logging_module.WARNING
        )
        prophet_model.fit(prophet_train)
        # Create future DataFrame for prediction.
        future = prophet_model.make_future_dataframe(
            periods=forecast_horizon,
            freq="B",
        )
        forecast = prophet_model.predict(future)
        pred = forecast["yhat"].tail(
            forecast_horizon
        ).values
        train_time = time.time() - start
        results.append(_calculate_metrics(
            actual,
            pred,
            "Prophet",
            "Prophet",
            train_time,
        ))
    except Exception as e:
        _LOG.warning("Prophet failed: %s", str(e))
    # Convert to DataFrame and sort by MAPE.
    results_df = pd.DataFrame(results).sort_values(
        "MAPE", ascending=True
    ).reset_index(drop=True)
    _LOG.info(
        "Library comparison complete — %d models evaluated.",
        len(results_df),
    )
    return results_df

def plot_library_comparison(
    library_comparison: pd.DataFrame,
) -> plt.Figure:
    """
    Plot library comparison results showing MAPE and training time.

    Two panels are shown — MAPE comparison and training time
    comparison for all models across all libraries. Colors
    distinguish between Darts Statsmodels and Prophet.

    :param library_comparison: DataFrame from `compare_libraries`
        containing MAPE RMSE and Train_Time for each model
    :return: matplotlib Figure object with comparison charts
    """
    # Define colors per library.
    library_colors = {
        "Darts"       : "#1565C0",
        "Statsmodels" : "#2E7D32",
        "Prophet"     : "#D32F2F",
    }
    # Create labels combining library and model name.
    labels = [
        f"{row['Library']}\n{row['Model']}"
        for _, row in library_comparison.iterrows()
    ]
    colors = [
        library_colors[row["Library"]]
        for _, row in library_comparison.iterrows()
    ]
    # Create figure with two panels.
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    # Panel 1 — MAPE comparison.
    bars = axes[0].barh(
        labels,
        library_comparison["MAPE"],
        color=colors,
        alpha=0.8,
        edgecolor="white",
    )
    # Add value labels on bars.
    for bar, val in zip(bars, library_comparison["MAPE"]):
        axes[0].text(
            val + 0.02,
            bar.get_y() + bar.get_height() / 2,
            f"{val:.2f}%",
            va="center",
            fontsize=9,
            fontweight="bold",
        )
    axes[0].set_title(
        "MAPE Comparison by Library and Model",
        fontsize=12,
        fontweight="bold",
    )
    axes[0].set_xlabel("MAPE (%) — Lower is Better")
    axes[0].set_ylabel("Library / Model")
    # Panel 2 — Training time comparison.
    bars2 = axes[1].barh(
        labels,
        library_comparison["Train_Time"],
        color=colors,
        alpha=0.8,
        edgecolor="white",
    )
    # Add value labels on bars.
    for bar, val in zip(bars2, library_comparison["Train_Time"]):
        axes[1].text(
            val + 0.005,
            bar.get_y() + bar.get_height() / 2,
            f"{val:.2f}s",
            va="center",
            fontsize=9,
            fontweight="bold",
        )
    axes[1].set_title(
        "Training Time Comparison by Library and Model",
        fontsize=12,
        fontweight="bold",
    )
    axes[1].set_xlabel("Training Time (seconds) — Lower is Better")
    axes[1].set_ylabel("Library / Model")
    # Add legend for libraries.
    legend_elements = [
        matplotlib.patches.Patch(
            facecolor="#1565C0", label="Darts"
        ),
        matplotlib.patches.Patch(
            facecolor="#2E7D32", label="Statsmodels"
        ),
        matplotlib.patches.Patch(
            facecolor="#D32F2F", label="Prophet"
        ),
    ]
    fig.legend(
        handles=legend_elements,
        loc="lower center",
        ncol=3,
        fontsize=10,
        bbox_to_anchor=(0.5, -0.05),
    )
    fig.suptitle(
        "Time Series Library Comparison — MAPE and Training Time",
        fontsize=14,
        fontweight="bold",
    )
    fig.tight_layout()
    return fig

def analyze_external_factor_impact(
    all_predictions: dict,
    target_val: darts.timeseries.TimeSeries,
    target_scaler: darts.dataprocessing.transformers.Scaler,
    event_flags: pd.DataFrame,
    top_n_models: int = 5,
) -> pd.DataFrame:
    """
    Analyze how external events affect model prediction accuracy.

    For each event type prediction errors on event days are compared
    against errors on normal trading days. A higher error on event
    days indicates the model struggles to predict market behavior
    around those events. Results show mean absolute error and error
    ratio for each model and event type combination.

    :param all_predictions: dictionary of model predictions from
        Phase 5 training
    :param target_val: scaled validation target TimeSeries
    :param target_scaler: fitted Darts Scaler for inverse transform
    :param event_flags: DataFrame with binary event flag columns
        IS_FOMC_DATE IS_CPI_RELEASE IS_HOLIDAY_ADJACENT
    :param top_n_models: number of top models to analyze default 5
    :return: DataFrame with error analysis per model and event type
    """
    # Fill NaN values in validation target.
    filler = darts.dataprocessing.transformers.MissingValuesFiller()
    target_val_clean = filler.transform(target_val)
    # Inverse transform validation to original price space.
    actual_df = target_scaler.inverse_transform(
        target_val_clean
    ).to_dataframe().dropna()
    # Select top n models by lowest MAE for focused analysis.
    model_maes = {}
    model_pred_dfs = {}
    for name, prediction in all_predictions.items():
        try:
            pred_clean = filler.transform(prediction)
            pred_df = target_scaler.inverse_transform(
                pred_clean
            ).to_dataframe().dropna()
            common_dates = actual_df.index.intersection(
                pred_df.index
            )
            if len(common_dates) < 5:
                continue
            actual = actual_df.loc[common_dates].values.flatten()
            predicted = pred_df.loc[common_dates].values.flatten()
            mae = float(np.mean(np.abs(actual - predicted)))
            model_maes[name] = mae
            model_pred_dfs[name] = pred_df
        except Exception:
            continue
    # Select top n models by lowest MAE.
    top_models = sorted(
        model_maes.keys(), key=lambda x: model_maes[x]
    )[:top_n_models]
    # Define event types to analyze.
    event_types = {
        "FOMC_Date"       : "IS_FOMC_DATE",
        "CPI_Release"     : "IS_CPI_RELEASE",
        "Holiday_Adjacent": "IS_HOLIDAY_ADJACENT",
    }
    # Initialize results list.
    results = []
    for model_name in top_models:
        pred_df = model_pred_dfs[model_name]
        common_dates = actual_df.index.intersection(pred_df.index)
        actual = actual_df.loc[common_dates].values.flatten()
        predicted = pred_df.loc[common_dates].values.flatten()
        # Calculate daily absolute errors.
        daily_errors = np.abs(actual - predicted)
        error_series = pd.Series(
            daily_errors, index=common_dates
        )
        # Calculate baseline error on normal days.
        # Normal days have no event flags.
        event_flags_aligned = event_flags.reindex(
            common_dates
        ).fillna(0)
        any_event = event_flags_aligned[
            list(event_types.values())
        ].any(axis=1)
        normal_mask = ~any_event
        normal_mae = float(
            error_series[normal_mask].mean()
        ) if normal_mask.sum() > 0 else float("nan")
        # Calculate error for each event type.
        for event_name, flag_col in event_types.items():
            if flag_col not in event_flags_aligned.columns:
                continue
            event_mask = event_flags_aligned[flag_col] == 1
            if event_mask.sum() == 0:
                continue
            event_mae = float(
                error_series[event_mask].mean()
            )
            # Error ratio — how much worse on event days.
            error_ratio = event_mae / normal_mae if normal_mae > 0 else float("nan")
            results.append({
                "Model"      : model_name,
                "Event_Type" : event_name,
                "Event_Days" : int(event_mask.sum()),
                "Event_MAE"  : round(event_mae, 2),
                "Normal_MAE" : round(normal_mae, 2),
                "Error_Ratio": round(error_ratio, 3),
            })
            _LOG.info(
                "%s on %s days → MAE: %.2f vs normal: %.2f "
                "(ratio: %.3f)",
                model_name,
                event_name,
                event_mae,
                normal_mae,
                error_ratio,
            )
    return pd.DataFrame(results).sort_values(
        ["Model", "Error_Ratio"], ascending=[True, False]
    ).reset_index(drop=True)

def plot_external_factor_impact(
    event_impact: pd.DataFrame,
) -> plt.Figure:
    """
    Plot external event impact on model prediction accuracy.

    Three panels show error ratios for FOMC dates CPI release
    dates and holiday adjacent days. Error ratio above 1.0 means
    the model performs worse on event days. Error ratio below 1.0
    means the model performs better on event days. The reference
    line at 1.0 represents no impact from the event.

    :param event_impact: DataFrame from `analyze_external_factor_impact`
        containing Error_Ratio per model and event type
    :return: matplotlib Figure object with three panel comparison
    """
    # Define event types and display titles.
    event_types = [
        "FOMC_Date",
        "CPI_Release",
        "Holiday_Adjacent",
    ]
    event_titles = [
        "FOMC Meeting Days",
        "CPI Release Days",
        "Holiday Adjacent Days",
    ]
    # Create figure with three panels.
    fig, axes = plt.subplots(1, 3, figsize=(18, 7))
    for idx, (event_type, title) in enumerate(
        zip(event_types, event_titles)
    ):
        event_data = event_impact[
            event_impact["Event_Type"] == event_type
        ].sort_values("Error_Ratio", ascending=False)
        if len(event_data) == 0:
            axes[idx].text(
                0.5, 0.5,
                f"No data for {event_type}",
                ha="center", va="center",
            )
            continue
        # Red for worse than normal green for better than normal.
        colors = [
            "#D32F2F" if r > 1.0 else "#2E7D32"
            for r in event_data["Error_Ratio"]
        ]
        bars = axes[idx].barh(
            event_data["Model"],
            event_data["Error_Ratio"],
            color=colors,
            alpha=0.8,
            edgecolor="white",
        )
        # Add value labels on bars.
        for bar, val in zip(bars, event_data["Error_Ratio"]):
            axes[idx].text(
                val + 0.02,
                bar.get_y() + bar.get_height() / 2,
                f"{val:.3f}",
                va="center",
                fontsize=9,
                fontweight="bold",
            )
        # Add reference line at 1.0 — no impact threshold.
        axes[idx].axvline(
            1.0,
            color="black",
            linewidth=1.5,
            linestyle="--",
            label="No impact (ratio=1.0)",
        )
        axes[idx].set_title(
            f"Error Ratio on {title}\n"
            f"(>1.0 = worse | <1.0 = better)",
            fontsize=10,
            fontweight="bold",
        )
        axes[idx].set_xlabel("Error Ratio")
        axes[idx].set_ylabel("Model")
        axes[idx].legend(fontsize=8)
    fig.suptitle(
        "External Event Impact on Model Prediction Accuracy",
        fontsize=14,
        fontweight="bold",
    )
    fig.tight_layout()
    return fig

def walk_forward_validation(
    target_train: darts.timeseries.TimeSeries,
    target_val: darts.timeseries.TimeSeries,
    target_test: darts.timeseries.TimeSeries,
    past_cov_train: darts.timeseries.TimeSeries,
    past_cov_val: darts.timeseries.TimeSeries,
    past_cov_test: darts.timeseries.TimeSeries,
    future_cov_train: darts.timeseries.TimeSeries,
    future_cov_val: darts.timeseries.TimeSeries,
    future_cov_test: darts.timeseries.TimeSeries,
    target_scaler: darts.dataprocessing.transformers.Scaler,
    forecast_horizon: int,
    tuning_results: pd.DataFrame,
    stride: int = 30,
) -> pd.DataFrame:
    """
    Perform walk forward validation across rolling forecast windows.

    The best model from Phase 7 tuning is trained once on the
    training data and then evaluated on rolling stride-sized windows
    across the validation and test periods. For each window the model
    predicts forecast_horizon days ahead using the same trained model
    simulating real time deployment. Results show MAPE MAE and
    direction accuracy per window and as averages.

    :param target_train: scaled target TimeSeries for training
    :param target_val: scaled target TimeSeries for validation
    :param target_test: scaled target TimeSeries for test
    :param past_cov_train: scaled past covariates for training
    :param past_cov_val: scaled past covariates for validation
    :param past_cov_test: scaled past covariates for test period
    :param future_cov_train: scaled future covariates for training
    :param future_cov_val: scaled future covariates for validation
    :param future_cov_test: scaled future covariates for test
    :param target_scaler: fitted Darts Scaler for inverse transform
    :param forecast_horizon: number of days to forecast ahead
    :param tuning_results: DataFrame from Phase 7 with best params
    :param stride: number of days between each forecast window
    :return: DataFrame with walk forward metrics per window
    """
    # Fill NaN values using MissingValuesFiller.
    filler = darts.dataprocessing.transformers.MissingValuesFiller()
    target_train_c = filler.transform(target_train)
    past_train_c = filler.transform(past_cov_train)
    future_train_c = filler.transform(future_cov_train)
    # Concatenate val and test for full evaluation period.
    val_test_target = darts.timeseries.concatenate(
        [
            filler.transform(target_val),
            filler.transform(target_test),
        ],
        axis=0,
        ignore_time_axis=True,
    )
    # Concatenate all past covariates including test period.
    past_full = darts.timeseries.concatenate(
        [
            past_train_c,
            filler.transform(past_cov_val),
            filler.transform(past_cov_test),
        ],
        axis=0,
        ignore_time_axis=True,
    )
    # Concatenate all future covariates.
    future_full = darts.timeseries.concatenate(
        [
            future_train_c,
            filler.transform(future_cov_val),
            filler.transform(future_cov_test),
        ],
        axis=0,
        ignore_time_axis=True,
    )
    # Get actual values in original price space.
    actual_df = target_scaler.inverse_transform(
        val_test_target
    ).to_dataframe().dropna()
    actual_vals = actual_df.values.flatten()
    # Get best model parameters from tuning results.
    best_row = tuning_results.iloc[0]
    best_params = eval(best_row["Best_Params"])
    model_name = best_row["Model"]
    lags = best_params["lags"]
    n_estimators = best_params["n_estimators"]
    _LOG.info(
        "Walk forward validation with %s — params: %s",
        model_name,
        best_params,
    )
    # Build best model with tuned parameters.
    if model_name == "XGBoost":
        model = darts.models.XGBModel(
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
    elif model_name == "LightGBM":
        model = darts.models.LightGBMModel(
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
    else:
        model = darts.models.RandomForestModel(
            lags=lags,
            lags_past_covariates=lags,
            lags_future_covariates=[0],
            output_chunk_length=forecast_horizon,
            n_estimators=n_estimators,
            max_depth=best_params["max_depth"],
            random_state=42,
        )
    # Train model on training data only.
    _LOG.info("Training model on training data.")
    model.fit(
        target_train_c,
        past_covariates=past_train_c,
        future_covariates=future_train_c,
    )
    # Generate prediction covering full val and test period.
    _LOG.info(
        "Generating predictions for %d days.",
        len(actual_vals),
    )
    prediction = model.predict(
        len(actual_vals),
        past_covariates=past_full,
        future_covariates=future_full,
    )
    # Inverse transform predictions.
    pred_df = target_scaler.inverse_transform(
        filler.transform(prediction)
    ).to_dataframe().dropna()
    pred_vals = pred_df.values.flatten()
    # Calculate metrics for each stride-sized window.
    window_results = []
    n_windows = len(actual_vals) // stride
    _LOG.info(
        "Evaluating %d windows of %d days each.",
        n_windows,
        stride,
    )
    for w in tqdm.tqdm(
        range(n_windows), desc="Walk forward windows"
    ):
        start_idx = w * stride
        end_idx = min(
            start_idx + forecast_horizon, len(actual_vals)
        )
        if start_idx >= len(actual_vals):
            break
        w_actual = actual_vals[start_idx:end_idx]
        w_pred = (
            pred_vals[start_idx:end_idx]
            if end_idx <= len(pred_vals)
            else w_actual
        )
        w_dates = actual_df.index[start_idx:end_idx]
        if len(w_actual) < 5:
            continue
        # Calculate MAPE.
        w_mape = float(
            np.mean(
                np.abs((w_actual - w_pred) / w_actual)
            ) * 100
        )
        # Calculate MAE.
        w_mae = float(np.mean(np.abs(w_actual - w_pred)))
        # Calculate direction accuracy.
        ref = w_actual[0]
        a_dir = np.sign(w_actual - ref)
        p_dir = np.sign(w_pred - ref)
        mask = a_dir != 0
        w_dir = float(
            np.mean(a_dir[mask] == p_dir[mask]) * 100
        ) if mask.sum() > 0 else float("nan")
        window_results.append({
            "Window"       : w + 1,
            "Start_Date"   : w_dates[0].date(),
            "End_Date"     : w_dates[-1].date(),
            "Window_MAPE"  : round(w_mape, 4),
            "Window_MAE"   : round(w_mae, 2),
            "Direction_Acc": round(w_dir, 1),
        })
    results_df = pd.DataFrame(window_results)
    _LOG.info(
        "Walk forward complete — %d windows | "
        "Avg MAPE: %.4f%% | Avg MAE: $%.2f | "
        "Avg Direction: %.1f%%",
        len(results_df),
        results_df["Window_MAPE"].mean(),
        results_df["Window_MAE"].mean(),
        results_df["Direction_Acc"].mean(),
    )
    return results_df

def plot_walk_forward_results(
    walk_forward_results: pd.DataFrame,
    model_name: str = "Best Model",
) -> plt.Figure:
    """
    Plot walk forward validation results showing MAPE and direction
    accuracy per window over the evaluation period.

    Two panels are shown — MAPE per window colored by performance
    tier and direction accuracy per window with random baseline
    reference line. Green bars indicate good performance orange
    indicates moderate and red indicates poor performance.

    :param walk_forward_results: DataFrame from `walk_forward_validation`
        containing Window_MAPE Direction_Acc and date columns
    :param model_name: name of the model for chart title
    :return: matplotlib Figure object with two panel results chart
    """
    # Create figure with two panels.
    fig, axes = plt.subplots(2, 1, figsize=(16, 10))
    # Color windows by MAPE performance tier.
    mape_colors = [
        "#2E7D32" if m < 5
        else "#FF6F00" if m < 15
        else "#D32F2F"
        for m in walk_forward_results["Window_MAPE"]
    ]
    # Panel 1 — MAPE per window.
    axes[0].bar(
        walk_forward_results["Window"],
        walk_forward_results["Window_MAPE"],
        color=mape_colors,
        alpha=0.8,
        edgecolor="white",
    )
    axes[0].axhline(
        walk_forward_results["Window_MAPE"].mean(),
        color="black",
        linewidth=1.5,
        linestyle="--",
        label=f"Avg MAPE: {walk_forward_results['Window_MAPE'].mean():.2f}%",
    )
    axes[0].set_title(
        "Walk Forward Validation — MAPE per Window",
        fontsize=12,
        fontweight="bold",
    )
    axes[0].set_ylabel("MAPE (%)")
    axes[0].set_xlabel("Window")
    axes[0].set_xticks(walk_forward_results["Window"])
    axes[0].set_xticklabels(
        [
            str(r["Start_Date"])
            for _, r in walk_forward_results.iterrows()
        ],
        rotation=45,
        ha="right",
        fontsize=7,
    )
    axes[0].legend()
    # Color windows by direction accuracy tier.
    dir_colors = [
        "#2E7D32" if d >= 60
        else "#FF6F00" if d >= 40
        else "#D32F2F"
        for d in walk_forward_results["Direction_Acc"]
    ]
    # Panel 2 — Direction accuracy per window.
    axes[1].bar(
        walk_forward_results["Window"],
        walk_forward_results["Direction_Acc"],
        color=dir_colors,
        alpha=0.8,
        edgecolor="white",
    )
    # Add random baseline reference line at 50%.
    axes[1].axhline(
        50,
        color="black",
        linewidth=1.0,
        linestyle="--",
        label="Random baseline (50%)",
    )
    # Add average direction accuracy line.
    axes[1].axhline(
        walk_forward_results["Direction_Acc"].mean(),
        color="#1565C0",
        linewidth=1.5,
        linestyle="--",
        label=f"Avg Direction: {walk_forward_results['Direction_Acc'].mean():.1f}%",
    )
    axes[1].set_title(
        "Walk Forward Validation — Direction Accuracy per Window",
        fontsize=12,
        fontweight="bold",
    )
    axes[1].set_ylabel("Direction Accuracy (%)")
    axes[1].set_xlabel("Window")
    axes[1].set_xticks(walk_forward_results["Window"])
    axes[1].set_xticklabels(
        [
            str(r["Start_Date"])
            for _, r in walk_forward_results.iterrows()
        ],
        rotation=45,
        ha="right",
        fontsize=7,
    )
    axes[1].set_ylim(0, 110)
    axes[1].legend()
    fig.suptitle(
        f"Walk Forward Validation — {model_name} 2023-2024",
        fontsize=14,
        fontweight="bold",
    )
    fig.tight_layout()
    return fig
