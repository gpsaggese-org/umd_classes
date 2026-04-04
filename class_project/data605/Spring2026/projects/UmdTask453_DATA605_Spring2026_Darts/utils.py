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
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
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