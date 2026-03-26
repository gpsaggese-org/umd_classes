"""
Utility Module for Causal Analysis of Financial Tradability
Contains all helper functions for data collection, preprocessing, feature engineering,
analysis, and causal inference.

EXERCISE #1 ADDITION: Hit Rate → PnL Simulation Framework
New functions added for Monte Carlo simulation and analysis

Data Source: Kaggle Bitcoin Historical Data (mczielinski/bitcoin-historical-data)
Using exact kagglehub code from Kaggle documentation

Import as:

import research.Causal_Analysis_of_Financial_Tradability.financial_trading_utils as rcaoftftu
"""

import pandas as pd
import numpy as np
import logging
from datetime import datetime
from typing import List, Tuple, Dict
from dataclasses import dataclass
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    roc_auc_score,
    precision_score,
    recall_score,
    f1_score,
)
from scipy import stats
import warnings

warnings.filterwarnings("ignore")

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# =============================================================================
# EXERCISE #1: SIMULATION CONFIGURATION
# =============================================================================


# #############################################################################
# SimulationConfig
# #############################################################################


@dataclass
class SimulationConfig:
    """Configuration for Exercise #1 simulation."""

    asset: str = "BTC"  # Asset symbol
    frequency: str = "1h"  # Time frequency
    start_date: str = "2023-01-01"
    end_date: str = "2023-12-31"
    hit_rates: List[float] = None  # Hit rates to test
    commission: float = 0.001  # 0.1% per trade
    slippage: float = 0.0005  # 0.05% per trade
    num_simulations: int = 10000  # Monte Carlo runs
    seed: int = 42

    def __post_init__(self):
        if self.hit_rates is None:
            self.hit_rates = np.arange(
                0.45, 0.56, 0.01
            )  # 45% to 55% in 1% steps


# =============================================================================
# DATA COLLECTION FUNCTIONS - KAGGLE DATASET
# =============================================================================


def load_kaggle_bitcoin_data(
    start_date: str = None, end_date: str = None
) -> pd.DataFrame:
    """
    Load Bitcoin historical data from Kaggle dataset.
    Uses exact code from: https://www.kaggle.com/datasets/mczielinski/bitcoin-historical-data

    Dataset: mczielinski/bitcoin-historical-data
    Data: OHLCV at 1-minute granularity from 2013-2021

    Parameters:
    -----------
    start_date : str
        Start date in 'YYYY-MM-DD' format (optional)
    end_date : str
        End date in 'YYYY-MM-DD' format (optional)

    Returns:
    --------
    pd.DataFrame
        Bitcoin OHLCV data
    """
    try:
        # Install dependencies as needed:
        # pip install kagglehub[pandas-datasets]
        import kagglehub
        from kagglehub import KaggleDatasetAdapter

        logger.info("Loading Kaggle Bitcoin historical data...")

        # Set the path to the file you'd like to load
        file_path = "btcusd_1-min_data.csv"

        # Load the latest version
        df = kagglehub.load_dataset(
            KaggleDatasetAdapter.PANDAS,
            "mczielinski/bitcoin-historical-data",
            file_path,
        )

        logger.info(f"Raw data shape: {df.shape}")
        logger.info(f"Columns: {df.columns.tolist()}")

        # Standardize column names to lowercase
        df.columns = df.columns.str.lower()

        # Handle timestamp column - Kaggle dataset has 'time' column with Unix timestamp
        if "time" in df.columns:
            # Original column in milliseconds
            df["timestamp"] = pd.to_datetime(df["time"], unit="s")
            df = df.drop("time", axis=1)
        elif "timestamp" in df.columns:
            # Ensure numeric timestamps are also treated as ms
            if pd.api.types.is_numeric_dtype(df["timestamp"]):
                df["timestamp"] = pd.to_datetime(df["timestamp"], unit="s")
            else:
                df["timestamp"] = pd.to_datetime(df["timestamp"])
        else:
            df["timestamp"] = pd.to_datetime(df.index)

        # Filter by start/end dates
        if start_date:
            df = df[df["timestamp"] >= pd.to_datetime(start_date)]
        if end_date:
            df = df[df["timestamp"] <= pd.to_datetime(end_date)]

        # Ensure required columns exist
        required_cols = ["timestamp", "open", "high", "low", "close", "volume"]
        missing_cols = [col for col in required_cols if col not in df.columns]

        if missing_cols:
            logger.error(f"Dataset missing required columns: {missing_cols}")
            logger.error(f"Available columns: {df.columns.tolist()}")
            raise ValueError(f"Dataset must contain: {', '.join(required_cols)}")

        # Convert numeric columns
        numeric_cols = ["open", "high", "low", "close", "volume"]
        for col in numeric_cols:
            df[col] = pd.to_numeric(df[col], errors="coerce")

        df = df.sort_values("timestamp").reset_index(drop=True)

        logger.info(
            f"Loaded {len(df)} records from {df['timestamp'].min()} to {df['timestamp'].max()}"
        )

        return df

    except ImportError:
        logger.error(
            "kagglehub not installed. Install with: pip install kagglehub[pandas-datasets]"
        )
        raise
    except Exception as e:
        logger.error(f"Error loading Kaggle data: {e}")
        raise


def resample_to_interval(df: pd.DataFrame, interval: str = "1h") -> pd.DataFrame:
    """
    Resample 1-minute Bitcoin data to desired interval.

    Parameters:
    -----------
    df : pd.DataFrame
        1-minute OHLCV data with timestamp index
    interval : str
        Target interval ('5min', '15min', '1h', '4h', '1d')

    Returns:
    --------
    pd.DataFrame
        Resampled OHLCV data
    """
    df = df.copy()
    df = df.set_index("timestamp")

    # Map intervals to pandas frequency strings (using lowercase)
    freq_map = {
        "5min": "5min",
        "15min": "15min",
        "1h": "1h",
        "4h": "4h",
        "1d": "1d",
    }
    freq = freq_map.get(interval, "1h")

    resampled = pd.DataFrame()
    resampled["open"] = df["open"].resample(freq).first()
    resampled["high"] = df["high"].resample(freq).max()
    resampled["low"] = df["low"].resample(freq).min()
    resampled["close"] = df["close"].resample(freq).last()
    resampled["volume"] = df["volume"].resample(freq).sum()

    resampled = resampled.reset_index()
    resampled = resampled.dropna()

    logger.info(f"Resampled to {interval}: {len(resampled)} records")

    return resampled


def generate_synthetic_bitcoin_data(
    start_date: str = None, end_date: str = None, interval: str = "1h"
) -> pd.DataFrame:
    """
    Generate synthetic Bitcoin OHLCV data for testing when Kaggle data unavailable.

    Parameters:
    -----------
    start_date : str
        Start date
    end_date : str
        End date
    interval : str
        Time interval

    Returns:
    --------
    pd.DataFrame
        Synthetic OHLCV data
    """
    start = datetime.strptime(start_date or "2024-02-01", "%Y-%m-%d")
    end = datetime.strptime(end_date or "2024-02-28", "%Y-%m-%d")

    # Map intervals to pandas frequency strings (lowercase for pandas 2.0+)
    freq_map = {
        "1min": "1min",
        "5min": "5min",
        "15min": "15min",
        "1h": "1h",
        "4h": "4h",
        "1d": "1d",
    }
    freq = freq_map.get(interval, "1h")

    dates = pd.date_range(start, end, freq=freq)

    np.random.seed(42)
    base_price = 45000  # Bitcoin reference price
    prices = base_price + np.cumsum(np.random.randn(len(dates)) * 100)

    df = pd.DataFrame(
        {
            "timestamp": dates,
            "open": prices,
            "high": prices + np.abs(np.random.randn(len(dates)) * 50),
            "low": prices - np.abs(np.random.randn(len(dates)) * 50),
            "close": prices + np.random.randn(len(dates)) * 50,
            "volume": np.random.uniform(1000, 5000, len(dates)),
        }
    )

    logger.info(
        f"Generated synthetic Bitcoin data: {len(df)} records for {interval} interval"
    )
    return df


# =============================================================================
# EXERCISE #1: DATA PIPELINE FUNCTIONS
# =============================================================================


def load_exercise_data(config: SimulationConfig) -> pd.DataFrame:
    """
    Load cryptocurrency data at specified frequency.
    Easy to swap: asset, frequency, date range.

    Parameters:
    -----------
    config : SimulationConfig
        Configuration with asset, frequency, dates

    Returns:
    --------
    pd.DataFrame
        OHLCV data with timestamp index
    """
    logger.info(f"Loading {config.asset} data at {config.frequency} frequency")

    try:
        # Load Bitcoin data from Kaggle
        df = load_kaggle_bitcoin_data(
            start_date=config.start_date, end_date=config.end_date
        )

        # Resample to target frequency
        if config.frequency != "1min":
            df = resample_to_interval(df, config.frequency)

        logger.info(f"Loaded {len(df)} records for {config.asset}")
        return df

    except Exception as e:
        logger.warning(f"Could not load from Kaggle: {e}. Using synthetic data.")
        df = generate_synthetic_bitcoin_data(
            start_date=config.start_date,
            end_date=config.end_date,
            interval=config.frequency,
        )
        return df


def compute_returns(df: pd.DataFrame) -> Tuple[np.ndarray, pd.Series]:
    """
    Compute percentage returns from OHLCV data.

    Parameters:
    -----------
    df : pd.DataFrame
        OHLCV data with close prices

    Returns:
    --------
    Tuple of (returns array, timestamps)
    """
    returns = df["close"].pct_change().dropna()
    timestamps = df["timestamp"].iloc[1:]  # Align with returns

    logger.info(f"Computed {len(returns)} returns")
    return returns.values, timestamps.values


# =============================================================================
# EXERCISE #1: CORE SIMULATION ENGINE
# =============================================================================


def simulate_trading_with_hit_rate(
    returns: np.ndarray,
    hit_rate: float,
    num_simulations: int = 10000,
    transaction_cost: float = 0.0015,  # 0.15% per trade
    trade_probability: float = 1.0,  # probability of taking a trade
    seed: int = 42,
) -> Tuple[np.ndarray, Dict]:
    np.random.seed(seed)

    pnl_simulations = np.zeros(num_simulations)
    winning_trades = np.zeros(num_simulations)
    losing_trades = np.zeros(num_simulations)
    max_drawdown_list = np.zeros(num_simulations)

    n_returns = len(returns)

    for sim_idx in range(num_simulations):
        # Sample returns
        sampled_returns = np.random.choice(returns, size=n_returns, replace=True)

        # True direction of returns (+1 or -1)
        true_direction = np.sign(sampled_returns)
        true_direction[true_direction == 0] = 1  # handle zero returns

        # Generate correctness (1 = correct prediction, 0 = wrong)
        is_correct = np.random.binomial(1, hit_rate, n_returns)

        # Predicted direction
        predicted_direction = np.where(
            is_correct == 1, true_direction, -true_direction
        )

        # Trade decision (optional filtering)
        trade_mask = np.random.rand(n_returns) < trade_probability

        # PnL calculation
        pnl_per_bar = trade_mask * (predicted_direction * sampled_returns)

        # Apply transaction cost ONLY when trading
        pnl_per_bar -= trade_mask * transaction_cost

        # Cumulative PnL
        cumulative_pnl = np.cumsum(pnl_per_bar)
        total_pnl = cumulative_pnl[-1]
        pnl_simulations[sim_idx] = total_pnl

        # Stats
        winning_trades[sim_idx] = np.sum(pnl_per_bar > 0)
        losing_trades[sim_idx] = np.sum(pnl_per_bar < 0)

        # Max drawdown
        running_max = np.maximum.accumulate(cumulative_pnl)
        drawdown = cumulative_pnl - running_max
        max_drawdown_list[sim_idx] = np.min(drawdown)

    # Aggregate statistics
    stats_dict = {
        "hit_rate": hit_rate,
        "mean_pnl": np.mean(pnl_simulations),
        "std_pnl": np.std(pnl_simulations),
        "min_pnl": np.min(pnl_simulations),
        "max_pnl": np.max(pnl_simulations),
        "percentile_5": np.percentile(pnl_simulations, 5),
        "percentile_50": np.percentile(pnl_simulations, 50),
        "percentile_95": np.percentile(pnl_simulations, 95),
        "prob_profit": np.mean(pnl_simulations > 0),
        "sharpe_ratio": (
            np.mean(pnl_simulations) / np.std(pnl_simulations)
            if np.std(pnl_simulations) > 0
            else 0
        ),
        "avg_winning_trades": np.mean(winning_trades),
        "avg_losing_trades": np.mean(losing_trades),
        "avg_max_drawdown": np.mean(max_drawdown_list),
    }

    return pnl_simulations, stats_dict


# =============================================================================
# DATA PREPROCESSING FUNCTIONS
# =============================================================================


def preprocess_data(
    df: pd.DataFrame,
    handle_missing: bool = True,
    remove_outliers_flag: bool = True,
    validate: bool = True,
) -> pd.DataFrame:
    """
    Complete preprocessing pipeline for cryptocurrency data.

    Parameters:
    -----------
    df : pd.DataFrame
        Raw OHLCV data
    handle_missing : bool
        Whether to handle missing values
    remove_outliers_flag : bool
        Whether to remove outliers
    validate : bool
        Whether to validate OHLC consistency

    Returns:
    --------
    pd.DataFrame
        Cleaned and validated data
    """
    df = df.copy()
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    initial_len = len(df)

    if remove_outliers_flag:
        Q1 = df[["close", "volume"]].quantile(0.25)
        Q3 = df[["close", "volume"]].quantile(0.75)
        IQR = Q3 - Q1
        mask = (
            (df[["close", "volume"]] < Q1 - 3 * IQR)
            | (df[["close", "volume"]] > Q3 + 3 * IQR)
        ).any(axis=1)
        df = df[~mask]

    if validate:
        assert (df["high"] >= df["low"]).all(), "Invalid OHLC: High < Low"
        assert (df["high"] >= df["close"]).all(), "Invalid OHLC: High < Close"

    logger.info(
        f"Preprocessed: {initial_len} -> {len(df)} records (removed {initial_len - len(df)})"
    )
    return df.reset_index(drop=True)


def synchronize_dataframes(
    dataframes: Dict[str, pd.DataFrame], method: str = "inner"
) -> Dict[str, pd.DataFrame]:
    """
    Synchronize multiple DataFrames by timestamp for multi-asset analysis.

    Parameters:
    -----------
    dataframes : Dict[str, pd.DataFrame]
        Dictionary of symbol -> DataFrame
    method : str
        Join method ('inner' or 'outer')

    Returns:
    --------
    Dict[str, pd.DataFrame]
        Synchronized DataFrames
    """
    keys = list(dataframes.keys())
    result_df = dataframes[keys[0]].set_index("timestamp")

    for key in keys[1:]:
        result_df = result_df.join(
            dataframes[key].set_index("timestamp"), how=method, rsuffix=f"_{key}"
        )

    result = {}
    for key in keys:
        df = result_df.copy()
        result[key] = df.reset_index()

    logger.info(
        f"Synchronized {len(dataframes)} dataframes using '{method}' join"
    )
    return result


# =============================================================================
# FEATURE ENGINEERING FUNCTIONS
# =============================================================================


def create_all_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create comprehensive set of technical indicators.

    Parameters:
    -----------
    df : pd.DataFrame
        Preprocessed OHLCV data

    Returns:
    --------
    pd.DataFrame
        DataFrame with all engineered features
    """
    df = df.copy()

    # Trend Indicators
    df["sma_10"] = df["close"].rolling(10).mean()
    df["sma_20"] = df["close"].rolling(20).mean()
    df["ema_12"] = df["close"].ewm(span=12).mean()
    df["momentum_10"] = df["close"].diff(10)

    # Volatility Indicators
    df["volatility_20"] = df["close"].pct_change().rolling(20).std() * np.sqrt(
        252
    )

    high_low = df["high"] - df["low"]
    high_close = np.abs(df["high"] - df["close"].shift())
    low_close = np.abs(df["low"] - df["close"].shift())
    df["atr_14"] = (
        pd.concat([high_low, high_close, low_close], axis=1)
        .max(axis=1)
        .rolling(14)
        .mean()
    )

    # Bollinger Bands
    sma = df["close"].rolling(20).mean()
    std = df["close"].rolling(20).std()
    df["bb_upper"] = sma + 2 * std
    df["bb_lower"] = sma - 2 * std
    df["bb_width"] = df["bb_upper"] - df["bb_lower"]

    # Momentum Indicators
    delta = df["close"].diff()
    gain = (delta.where(delta > 0, 0)).rolling(14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
    rs = gain / loss
    df["rsi_14"] = 100 - (100 / (1 + rs))

    ema_12 = df["close"].ewm(span=12).mean()
    ema_26 = df["close"].ewm(span=26).mean()
    df["macd"] = ema_12 - ema_26
    df["macd_signal"] = df["macd"].ewm(span=9).mean()
    df["macd_hist"] = df["macd"] - df["macd_signal"]

    # Volume Indicators
    df["obv"] = (np.sign(df["close"].diff()) * df["volume"]).fillna(0).cumsum()

    clv = ((df["close"] - df["low"]) - (df["high"] - df["close"])) / (
        df["high"] - df["low"]
    )
    df["ad_line"] = (clv.fillna(0) * df["volume"]).cumsum()

    # Returns
    df["log_return"] = np.log(df["close"] / df["close"].shift(1))
    df["simple_return"] = df["close"].pct_change()

    logger.info(
        f"Created {len([c for c in df.columns if c not in ['timestamp', 'open', 'high', 'low', 'close', 'volume']])} features"
    )
    return df.dropna()


def create_multi_horizon_targets(
    df: pd.DataFrame, horizons: List[int] = None
) -> pd.DataFrame:
    """
    Create binary classification targets for multiple prediction horizons.

    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame with features
    horizons : List[int]
        List of prediction horizons

    Returns:
    --------
    pd.DataFrame
        DataFrame with target columns for each horizon
    """
    if horizons is None:
        horizons = [1, 5, 10, 20]

    for h in horizons:
        df[f"target_h{h}"] = (df["close"].shift(-h) > df["close"]).astype(int)

    logger.info(f"Created targets for horizons: {horizons}")
    return df


# =============================================================================
# PREDICTABILITY ANALYSIS FUNCTIONS
# =============================================================================


def analyze_predictability_by_horizon(
    df: pd.DataFrame,
    horizons: List[int] = None,
    model_type: str = "logistic",
    train_ratio: float = 0.8,
    max_samples: int = None,
) -> pd.DataFrame:
    """
    Analyze predictability across multiple trading horizons.

    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame with features and targets
    horizons : List[int]
        List of horizons to analyze
    model_type : str
        'logistic' or 'random_forest'

    Returns:
    --------
    pd.DataFrame
        Results with accuracy and AUC by horizon
    """
    if horizons is None:
        horizons = [1, 5, 10, 20]

    if max_samples is not None:
        df = df.iloc[-max_samples:].copy()

    df = df.sort_values("timestamp").reset_index(drop=True)

    exclude_cols = ["timestamp", "open", "high", "low", "close", "volume"]
    exclude_cols += [col for col in df.columns if col.startswith("target_")]
    feature_cols = [col for col in df.columns if col not in exclude_cols]

    results = []

    for horizon in horizons:
        target_col = f"target_h{horizon}"
        if target_col not in df.columns:
            continue

        try:
            df_clean = df[[target_col] + feature_cols].dropna()

            X = df_clean[feature_cols]
            y = df_clean[target_col]

            split_idx = int(len(df_clean) * train_ratio)

            X_train, X_test = X.iloc[:split_idx], X.iloc[split_idx:]
            y_train, y_test = y.iloc[:split_idx], y.iloc[split_idx:]

            if model_type == "logistic":
                model = LogisticRegression(
                    max_iter=1000, random_state=42, n_jobs=-1
                )
            else:
                model = RandomForestClassifier(
                    n_estimators=100, random_state=42, n_jobs=-1
                )

            model.fit(X_train, y_train)

            y_pred = model.predict(X_test)
            y_proba = model.predict_proba(X_test)[:, 1]

            acc = accuracy_score(y_test, y_pred)
            auc = roc_auc_score(y_test, y_proba)

            precision = precision_score(y_test, y_pred, zero_division=0)
            recall = recall_score(y_test, y_pred, zero_division=0)
            f1 = f1_score(y_test, y_pred, zero_division=0)

            results.append(
                {
                    "horizon": horizon,
                    "accuracy": acc,
                    "auc": auc,
                    "precision": precision,
                    "recall": recall,
                    "f1": f1,
                    "n_samples": len(df_clean),
                }
            )

            logger.info(
                f"H{horizon}: Acc={acc:.4f}, AUC={auc:.4f}, "
                f"F1={f1:.4f}, Samples={len(df_clean)}"
            )

        except Exception as e:
            logger.error(f"Error on horizon {horizon}: {e}")
            continue

    return pd.DataFrame(results)


# =============================================================================
# HIT RATE AND PnL ANALYSIS FUNCTIONS
# =============================================================================


def calculate_hit_rate_requirement(
    avg_win: float, avg_loss: float, target_profit_factor: float = 1.0
) -> float:
    """
    Calculate minimum hit rate required for target profit factor.

    Parameters:
    -----------
    avg_win : float
        Average winning trade return (e.g., 0.01 for 1%)
    avg_loss : float
        Average losing trade return magnitude
    target_profit_factor : float
        Target profit factor (gross profit / gross loss)

    Returns:
    --------
    float
        Minimum required hit rate (0.0 to 1.0)
    """
    if avg_win <= 0 or avg_loss <= 0:
        return np.nan

    be_hit_rate = avg_loss / (avg_win + avg_loss)

    if target_profit_factor == 1.0:
        min_hit_rate = be_hit_rate
    else:
        min_hit_rate = (avg_loss * (1 + 1 / target_profit_factor)) / (
            avg_win + avg_loss
        )

    return np.clip(min_hit_rate, 0, 1)


def analyze_pnl_by_horizon(
    results_df: pd.DataFrame,
    avg_win: float = 0.005,
    avg_loss: float = 0.005,
    target_pf: float = 1.5,
) -> pd.DataFrame:
    """
    Analyze PnL requirements and achievability by horizon.

    Parameters:
    -----------
    results_df : pd.DataFrame
        Results from predictability analysis
    avg_win : float
        Average winning trade return
    avg_loss : float
        Average losing trade return
    target_pf : float
        Target profit factor

    Returns:
    --------
    pd.DataFrame
        PnL analysis results
    """
    pnl = []

    min_hr_be = calculate_hit_rate_requirement(avg_win, avg_loss, 1.0)
    min_hr_target = calculate_hit_rate_requirement(avg_win, avg_loss, target_pf)

    for _, row in results_df.iterrows():
        horizon = int(row["horizon"])
        acc = row["accuracy"]

        exp_pnl_per_trade = (acc * avg_win - (1 - acc) * avg_loss) * 100
        expected_total_pnl = exp_pnl_per_trade * 100

        prob_positive = stats.norm.sf(
            0,
            loc=exp_pnl_per_trade * 100,
            scale=np.sqrt(100 * (avg_win**2 + avg_loss**2)),
        )

        sharpe_ratio = (
            (exp_pnl_per_trade * 100) / np.sqrt(100 * (avg_win**2 + avg_loss**2))
            if np.sqrt(100 * (avg_win**2 + avg_loss**2)) > 0
            else 0
        )

        pnl.append(
            {
                "horizon": horizon,
                "accuracy": f"{acc * 100:.2f}%",
                "min_hr_breakeven": f"{min_hr_be * 100:.2f}%",
                "min_hr_target_pf": f"{min_hr_target * 100:.2f}%",
                "achievable_be": "YES" if acc >= min_hr_be else "NO",
                "achievable_target": "YES" if acc >= min_hr_target else "NO",
                "expected_pnl_per_trade": f"{exp_pnl_per_trade:.4f}%",
                "expected_total_pnl": f"{expected_total_pnl:.4f}%",
                "prob_positive_pnl": f"{prob_positive * 100:.2f}%",
                "sharpe_ratio": f"{sharpe_ratio:.4f}",
            }
        )

    return pd.DataFrame(pnl)


# =============================================================================
# CAUSAL INFERENCE FUNCTIONS
# =============================================================================


def analyze_horizon_causal_effect(
    df: pd.DataFrame, horizons: List[int] = None
) -> Dict:
    """
    Analyze causal relationship between horizon and predictability.

    Parameters:
    -----------
    df : pd.DataFrame
        Complete analysis results
    horizons : List[int]
        List of horizons to analyze

    Returns:
    --------
    Dict
        Causal analysis results
    """
    if horizons is None:
        horizons = [1, 5, 10, 20]

    results = {
        "horizon_elasticity": [],
        "accuracy_by_horizon": [],
        "predictability_decay": None,
    }

    if "accuracy" in df.columns and "horizon" in df.columns:
        accuracies = df["accuracy"].values
        hrzns = df["horizon"].values

        for i in range(len(hrzns) - 1):
            elasticity = (
                (accuracies[i + 1] - accuracies[i]) / accuracies[i]
            ) / ((hrzns[i + 1] - hrzns[i]) / hrzns[i])
            results["horizon_elasticity"].append(
                {
                    "from_horizon": hrzns[i],
                    "to_horizon": hrzns[i + 1],
                    "elasticity": elasticity,
                }
            )

        from scipy.optimize import curve_fit

        def exponential_decay(x, a, b):
            return a * np.exp(-b * x)

        try:
            popt, _ = curve_fit(
                exponential_decay,
                hrzns,
                accuracies,
                p0=[0.55, 0.01],
                maxfev=5000,
            )
            results["predictability_decay"] = {
                "amplitude": popt[0],
                "decay_rate": popt[1],
                "model": "exponential_decay",
            }
            logger.info(f"Predictability decay rate: {popt[1]:.6f}")
        except Exception as e:
            logger.warning(f"Could not fit decay model: {e}")

    return results


def estimate_instrumental_variables(df: pd.DataFrame) -> Dict:
    """
    Identify instrumental variables that affect horizon without directly affecting predictability.

    Parameters:
    -----------
    df : pd.DataFrame
        Analysis data

    Returns:
    --------
    Dict
        Instrumental variable analysis
    """
    iv_analysis = {
        "potential_instruments": [],
        "confounders": [],
        "analysis": "Instrument validity depends on empirical testing",
    }

    iv_analysis["potential_instruments"] = [
        "transaction_costs",
        "slippage_impact",
        "market_liquidity",
        "order_size_constraints",
    ]

    iv_analysis["confounders"] = [
        "market_regime",
        "volatility_state",
        "information_frequency",
        "microstructure_effects",
    ]

    logger.info("Instrumental variable analysis completed")
    return iv_analysis


# =============================================================================
# MARKET REGIME AND TRANSACTION COST FUNCTIONS
# =============================================================================


def detect_market_regimes(
    df: pd.DataFrame, volatility_window: int = 20
) -> pd.DataFrame:
    """
    Detect different market regimes (trending, mean-reverting, high volatility).

    Parameters:
    -----------
    df : pd.DataFrame
        OHLCV data with calculated indicators
    volatility_window : int
        Window for volatility calculation

    Returns:
    --------
    pd.DataFrame
        Data with regime labels
    """
    df = df.copy()

    df["volatility"] = df["close"].pct_change().rolling(volatility_window).std()
    df["returns"] = df["close"].pct_change()
    df["trend"] = df["returns"].rolling(10).mean()

    sma = df["close"].rolling(20).mean()
    df["mean_reversion_signal"] = (df["close"] - sma) / sma

    vol_high = df["volatility"] > df["volatility"].quantile(0.66)
    vol_low = df["volatility"] <= df["volatility"].quantile(0.33)
    trend_strong = df["trend"].abs() > df["trend"].abs().quantile(0.66)
    mean_rev = df["mean_reversion_signal"].abs() > df[
        "mean_reversion_signal"
    ].abs().quantile(0.5)

    df["regime"] = "mixed"
    df.loc[trend_strong & vol_high, "regime"] = "trending_volatile"
    df.loc[trend_strong & vol_low, "regime"] = "trending_stable"
    df.loc[~trend_strong & mean_rev & vol_low, "regime"] = (
        "mean_reverting_stable"
    )
    df.loc[~trend_strong & mean_rev & vol_high, "regime"] = (
        "mean_reverting_volatile"
    )

    logger.info(f"Regimes detected: {df['regime'].value_counts().to_dict()}")
    return df


def analyze_with_transaction_costs(
    pnl_df: pd.DataFrame, commission: float = 0.001, slippage: float = 0.0005
) -> pd.DataFrame:
    """
    Adjust analysis for realistic transaction costs and slippage.

    Parameters:
    -----------
    pnl_df : pd.DataFrame
        PnL analysis results (percentages can be strings, e.g., '-0.0008%')
    commission : float
        Commission per trade (fraction, e.g., 0.001 = 0.1%)
    slippage : float
        Average slippage per trade (fraction)

    Returns:
    --------
    pd.DataFrame
        Adjusted analysis with expected PnL after costs and tradeable flag
    """
    pnl_adjusted = pnl_df.copy()
    total_cost = commission + slippage

    for col in ["expected_pnl_per_trade", "expected_total_pnl"]:
        if col in pnl_adjusted.columns:
            pnl_adjusted[col] = (
                pnl_adjusted[col]
                .astype(str)
                .str.replace("%", "", regex=False)
                .astype(float)
                / 100.0
            )

    if "expected_pnl_per_trade" in pnl_adjusted.columns:
        pnl_adjusted["expected_pnl_after_costs"] = (
            pnl_adjusted["expected_pnl_per_trade"] - total_cost
        )

        pnl_adjusted["tradeable"] = pnl_adjusted["expected_pnl_after_costs"] > 0

    logger.info(
        f"Analysis adjusted for costs: commission={commission}, slippage={slippage}"
    )
    return pnl_adjusted


# =============================================================================
# MONTE CARLO SIMULATION FUNCTIONS
# =============================================================================


def run_monte_carlo_simulation(
    hit_rate: float,
    horizon: int,
    num_simulations: int = 10000,
    num_trades: int = 100,
    avg_win: float = 0.005,
    avg_loss: float = 0.005,
) -> Tuple[Dict, np.ndarray]:
    """
    Run Monte Carlo simulation of trading outcomes.

    Parameters:
    -----------
    hit_rate : float
        Win probability (0.0 to 1.0)
    horizon : int
        Trading horizon
    num_simulations : int
        Number of simulations
    num_trades : int
        Number of trades per simulation
    avg_win : float
        Average winning trade return
    avg_loss : float
        Average losing trade return

    Returns:
    --------
    Tuple[Dict, np.ndarray]
        Statistics dictionary and simulations array
    """
    np.random.seed(42)
    pnl_simulations = []

    for _ in range(num_simulations):
        trades = np.random.binomial(1, hit_rate, num_trades)
        pnl = trades * avg_win - (1 - trades) * avg_loss
        total_pnl = pnl.sum()
        pnl_simulations.append(total_pnl)

    pnl_simulations = np.array(pnl_simulations)

    stats_dict = {
        "mean": pnl_simulations.mean(),
        "std": pnl_simulations.std(),
        "min": pnl_simulations.min(),
        "max": pnl_simulations.max(),
        "percentile_5": np.percentile(pnl_simulations, 5),
        "percentile_25": np.percentile(pnl_simulations, 25),
        "percentile_50": np.percentile(pnl_simulations, 50),
        "percentile_75": np.percentile(pnl_simulations, 75),
        "percentile_95": np.percentile(pnl_simulations, 95),
        "prob_positive": (pnl_simulations > 0).mean(),
        "prob_loss": (pnl_simulations < 0).mean(),
        "var_95": np.percentile(pnl_simulations, 5),
        "cvar_95": pnl_simulations[
            pnl_simulations <= np.percentile(pnl_simulations, 5)
        ].mean(),
    }

    logger.info(
        f"Monte Carlo: {num_simulations} sims, Hit Rate={hit_rate:.2%}, "
        f"Prob(+PnL)={stats_dict['prob_positive']:.2%}"
    )

    return stats_dict, pnl_simulations


# =============================================================================
# BACKTESTING AND VALIDATION FUNCTIONS
# =============================================================================


def perform_walk_forward_validation(
    df: pd.DataFrame, model_func, window_size: int = 252, step_size: int = 50
) -> pd.DataFrame:
    """
    Perform walk-forward validation (out-of-sample testing).

    Parameters:
    -----------
    df : pd.DataFrame
        Complete dataset
    model_func : callable
        Function to train and evaluate model
    window_size : int
        Training window size
    step_size : int
        Step size for walk-forward

    Returns:
    --------
    pd.DataFrame
        Validation results for each period
    """
    results = []

    for i in range(0, len(df) - window_size, step_size):
        train_df = df.iloc[i : i + window_size]
        test_df = df.iloc[i + window_size : i + window_size + step_size]

        if len(test_df) == 0:
            continue

        try:
            period_result = model_func(train_df, test_df)
            period_result["period"] = i // step_size
            results.append(period_result)
        except Exception as e:
            logger.warning(f"Error in walk-forward period {i}: {e}")
            continue

    logger.info(f"Walk-forward validation completed: {len(results)} periods")
    return pd.DataFrame(results)


def calculate_cross_market_correlation(
    dataframes: Dict[str, pd.DataFrame],
) -> Dict:
    """
    Calculate correlations across multiple cryptocurrency pairs.

    Parameters:
    -----------
    dataframes : Dict[str, pd.DataFrame]
        Dictionary of symbol -> DataFrame

    Returns:
    --------
    Dict
        Cross-market correlation analysis
    """
    symbols = list(dataframes.keys())
    returns_dict = {}

    for symbol, df in dataframes.items():
        returns_dict[symbol] = df["close"].pct_change()

    returns_df = pd.DataFrame(returns_dict)
    correlation_matrix = returns_df.corr()

    rolling_corr = returns_df.rolling(50).corr()

    logger.info(f"Cross-market correlation analyzed for {len(symbols)} assets")

    return {
        "correlation_matrix": correlation_matrix,
        "rolling_correlation": rolling_corr,
        "symbols": symbols,
    }


# =============================================================================
# UTILITY AND HELPER FUNCTIONS
# =============================================================================


def get_summary_statistics(df: pd.DataFrame) -> Dict:
    """
    Generate summary statistics for analysis data.

    Parameters:
    -----------
    df : pd.DataFrame
        Analysis data

    Returns:
    --------
    Dict
        Summary statistics
    """
    summary = {
        "total_records": len(df),
        "date_range": f"{df['timestamp'].min()} to {df['timestamp'].max()}"
        if "timestamp" in df.columns
        else "N/A",
        "price_mean": df["close"].mean() if "close" in df.columns else None,
        "price_std": df["close"].std() if "close" in df.columns else None,
        "volume_mean": df["volume"].mean() if "volume" in df.columns else None,
        "features_count": len(
            [
                c
                for c in df.columns
                if c
                not in ["timestamp", "open", "high", "low", "close", "volume"]
            ]
        ),
        "missing_values": df.isnull().sum().sum(),
    }

    logger.info(
        f"Summary: {summary['total_records']} records, {summary['features_count']} features"
    )
    return summary


def export_results(results_dict: Dict, output_dir: str = ".") -> None:
    """
    Export analysis results to CSV files.

    Parameters:
    -----------
    results_dict : Dict
        Dictionary of analysis results
    output_dir : str
        Output directory
    """
    for name, data in results_dict.items():
        if isinstance(data, pd.DataFrame):
            filepath = f"{output_dir}/{name}.csv"
            data.to_csv(filepath, index=False)
            logger.info(f"Exported: {filepath}")


logger.info("=" * 80)
logger.info("Utility module loaded successfully")
logger.info(
    "Exercise #1 functions available: load_exercise1_data, compute_returns, simulate_trading_with_hit_rate"
)
logger.info("=" * 80)
