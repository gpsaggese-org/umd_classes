"""
stumpy_utils.py

Utility functions used by the Stumpy tutorial notebooks
(stumpy.API.ipynb and stumpy.example.ipynb).

Notebooks call these helpers instead of writing raw logic inline so that
the notebooks stay readable and the reusable pieces can be tested.

Import as:

    import stumpy_utils as stu
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd
import stumpy
import yfinance as yf

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# -----------------------------------------------------------------------------
# Data acquisition
# -----------------------------------------------------------------------------


def load_prices(
    ticker: str,
    start: str,
    end: str,
    cache_dir: Path | str = "data/raw",
    refresh: bool = False,
) -> pd.DataFrame:
    """
    Download daily OHLCV bars for a ticker, with a local parquet cache.

    The first call hits Yahoo Finance and saves the result to disk. Later
    calls read the cached file so the notebook is reproducible offline.

    :param ticker: Yahoo Finance symbol (e.g. "SPY").
    :param start: ISO date string for the first day to include.
    :param end: ISO date string for the day after the last included.
    :param cache_dir: directory to read and write the parquet cache.
    :param refresh: if True, ignore the cache and re-download.
    :return: DataFrame of daily OHLCV indexed by date.
    """
    cache_dir = Path(cache_dir)
    cache_dir.mkdir(parents=True, exist_ok=True)
    cache = cache_dir / f"{ticker}_{start}_{end}.parquet"
    if cache.exists() and not refresh:
        logger.info("Loading cached prices for %s from %s", ticker, cache)
        return pd.read_parquet(cache)
    logger.info("Downloading %s from Yahoo Finance", ticker)
    df = yf.download(ticker, start=start, end=end, auto_adjust=False, progress=False)
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    df = df.dropna()
    df.index = pd.to_datetime(df.index)
    df.to_parquet(cache)
    return df


# -----------------------------------------------------------------------------
# Stationary feature engineering
# -----------------------------------------------------------------------------


def build_features(
    px: pd.DataFrame,
    vol_lookback: int = 20,
    volume_lookback: int = 60,
) -> pd.DataFrame:
    """
    Build a panel of stationary features from raw OHLCV.

    Three features are returned. Their levels do not trend over time, so
    they are appropriate inputs for matrix profile algorithms:

    1. log_ret: daily log return.
    2. rv: annualized rolling realized volatility.
    3. vol_z: z-score of log dollar volume vs a trailing window.

    :param px: DataFrame with at least Close and Volume columns.
    :param vol_lookback: window length for rolling realized volatility.
    :param volume_lookback: window length for the volume z-score baseline.
    :return: DataFrame indexed by date with columns
             [close, log_ret, rv, vol_z], NaN rows dropped.
    """
    close = px["Close"]
    volume = px["Volume"].replace(0, np.nan)
    log_ret = np.log(close).diff()
    rv = log_ret.rolling(vol_lookback).std() * np.sqrt(252)
    log_v = np.log(volume)
    vol_z = (log_v - log_v.rolling(volume_lookback).mean()) / log_v.rolling(
        volume_lookback
    ).std()
    return pd.concat(
        [
            close.rename("close"),
            log_ret.rename("log_ret"),
            rv.rename("rv"),
            vol_z.rename("vol_z"),
        ],
        axis=1,
    ).dropna()


# -----------------------------------------------------------------------------
# Matrix profile helpers
# -----------------------------------------------------------------------------


def causal_align(
    profile: np.ndarray,
    idx: pd.DatetimeIndex,
    window: int,
    name: str = "mp",
) -> pd.Series:
    """
    Anchor matrix profile values at the END of their subsequence.

    Stumpy returns one value per subsequence start. To use the value
    causally, attach it to the date the subsequence ends on, so the value
    at date t reflects only data available through t.

    :param profile: 1D matrix profile distance array, length n - m + 1.
    :param idx: original DatetimeIndex of the input series.
    :param window: subsequence length m.
    :param name: name for the returned Series.
    :return: Series of length n - m + 1 with end-of-window dates.
    """
    n = len(profile)
    return pd.Series(profile, index=idx[window - 1 : window - 1 + n], name=name)


def left_mp_distance(series: np.ndarray, m: int) -> np.ndarray:
    """
    LEFT matrix profile: distance from each window to its nearest PAST neighbour.

    Stumpy's stump returns the nearest-neighbour index for the left side,
    which is causal (only past windows are eligible matches). This function
    converts that index into the actual z-normalized Euclidean distance.

    Compared to the standard self-join matrix profile, the LEFT version
    gives high values at the FIRST occurrence of any pattern and low values
    at later repeats. For regime detection in time series this is exactly
    the desired behaviour.

    :param series: 1D float array of length n.
    :param m: subsequence length.
    :return: array of length n - m + 1, with NaN where no past neighbour
             exists.
    """
    full = stumpy.stump(series.astype(float), m=m)
    left_idx = full[:, 2].astype(int)
    n_sub = len(series) - m + 1
    out = np.full(n_sub, np.nan)
    for i in range(n_sub):
        j = left_idx[i]
        if j < 0:
            continue
        x = series[i : i + m].astype(float)
        y = series[j : j + m].astype(float)
        sx, sy = x.std(), y.std()
        if sx == 0 or sy == 0:
            out[i] = np.linalg.norm(x - y)
        else:
            out[i] = np.linalg.norm(
                (x - x.mean()) / sx - (y - y.mean()) / sy
            )
    return out


def joint_left_mp(
    feat: pd.DataFrame,
    feature_cols: Iterable[str],
    window: int,
) -> pd.Series:
    """
    Combine per-feature LEFT matrix profiles into one joint score.

    Computes the LEFT matrix profile separately for each column in
    feature_cols, then averages across features at every time step.

    :param feat: DataFrame indexed by date.
    :param feature_cols: column names to include in the joint score.
    :param window: subsequence length m.
    :return: causal Series of joint LEFT MP, indexed by end-of-window date.
    """
    arrays = []
    for name in feature_cols:
        arrays.append(left_mp_distance(feat[name].to_numpy(), window))
    joint = np.nanmean(np.vstack(arrays), axis=0)
    return causal_align(joint, feat.index, window, name="mp_joint_left")


# -----------------------------------------------------------------------------
# Labels and event halos
# -----------------------------------------------------------------------------


def event_label_series(
    idx: pd.DatetimeIndex,
    events: pd.DataFrame,
    halo_back: int = 2,
    halo_fwd: int = 25,
) -> pd.Series:
    """
    Build a 0/1 label series marking dates near known stress events.

    The halo is forward-asymmetric on purpose. A causal MP value at date t
    reflects the m-day window ending at t, so an event on date E elevates
    the MP signal for dates in [E, E + m - 1] rather than at E itself.
    A symmetric halo would understate detector performance.

    :param idx: target DatetimeIndex (one row per trading day).
    :param events: DataFrame with at least a "date" column (datetime).
    :param halo_back: calendar days BEFORE each event labelled positive.
    :param halo_fwd: calendar days AFTER each event labelled positive.
    :return: int Series of 0/1 with the same index as idx.
    """
    y = pd.Series(0, index=idx, dtype=int)
    for d in events["date"]:
        within = (idx >= d - pd.Timedelta(days=halo_back)) & (
            idx <= d + pd.Timedelta(days=halo_fwd)
        )
        y.loc[within] = 1
    return y


# -----------------------------------------------------------------------------
# Causal scoring and ensemble
# -----------------------------------------------------------------------------


def causal_pct_rank(score: pd.Series, min_periods: int = 252) -> pd.Series:
    """
    Causal expanding-window percentile rank of a score.

    At each date t, returns the rank of score[t] among all scores up to and
    including t, expressed as a value in [0, 1]. Uses no future information.

    :param score: numeric Series, NaNs are dropped before ranking.
    :param min_periods: minimum number of observations before a rank is
                        emitted (default = 1 trading year).
    :return: Series of percentile ranks in [0, 1].
    """
    s = score.dropna()
    return s.expanding(min_periods=min_periods).rank(pct=True).rename(score.name)


# -----------------------------------------------------------------------------
# Trading overlay helpers
# -----------------------------------------------------------------------------


def expanding_risk_off_filter(
    score: pd.Series,
    quantile: float = 0.95,
    min_periods: int = 252,
) -> pd.Series:
    """
    Causal risk-off filter from an anomaly score.

    The filter is risk-on (=1) when yesterday's score is below the expanding
    causal q-th quantile of the score history through yesterday, and
    risk-off (=0) otherwise. Yesterday's score and threshold are used to
    keep the filter applicable to today's return without look-ahead.

    :param score: anomaly score Series (higher = more anomalous).
    :param quantile: quantile that triggers risk-off (default 0.95).
    :param min_periods: minimum observations before the filter activates
                        (default = 1 trading year).
    :return: Series of 0/1 filter values, same index as score.
    """
    s_lag = score.shift(1)
    thr = s_lag.expanding(min_periods=min_periods).quantile(quantile)
    return (s_lag < thr).astype(float).fillna(1.0)


def perf_stats(eq: pd.Series) -> dict:
    """
    Compute standard performance stats from an equity curve.

    :param eq: cumulative equity curve (growth-of-1.0).
    :return: dict with CAGR, Sharpe (annualized, daily log returns), and
             MaxDD (most negative peak-to-trough drawdown).
    """
    log_r = np.log(eq).diff().dropna()
    n_y = (eq.index[-1] - eq.index[0]).days / 365.25
    cagr = eq.iloc[-1] ** (1 / n_y) - 1
    sharpe = log_r.mean() / log_r.std() * np.sqrt(252)
    drawdown = (eq / eq.cummax() - 1).min()
    return {"CAGR": cagr, "Sharpe": sharpe, "MaxDD": drawdown}
