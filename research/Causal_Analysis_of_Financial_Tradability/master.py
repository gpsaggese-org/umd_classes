# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.19.0
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %% [markdown]
# # Causal Analysis of Financial Tradability
#
# Complete analysis framework covering:
# - Data collection and preprocessing
# - Feature engineering (25+ technical indicators)
# - Predictability analysis across multiple horizons
# - Hit rate and PnL analysis
# - Causal inference methods
# - Market regime detection
# - Transaction cost impact
# - Monte Carlo simulation
# - Walk-forward validation
# - Cross-market correlation analysis

# %%
# !pip install stats

# %% [markdown]
# # Exercise 1

# %%
# %load_ext autoreload
# %autoreload 2
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import financial_trading_utils as ftu
from scipy import stats

import warnings

warnings.filterwarnings("ignore")

sns.set_style("whitegrid")
plt.rcParams["figure.figsize"] = (14, 8)

print("All utilities loaded successfully")

# %%
# EXERCISE #1: Hit Rate → PnL Simulation Framework
# Import all necessary functions from financial_trading_utils
# %load_ext autoreload
# %autoreload 2
from financial_trading_utils import (
    SimulationConfig,
    load_exercise_data,
    compute_returns,
    simulate_trading_with_hit_rate,
)

print("Exercise #1 functions imported successfully!")
print("Ready to run simulations...")

# %%
# Configure Exercise #1 simulation
config_ex1 = SimulationConfig(
    asset="BTC", frequency="1h", start_date="2023-01-01", end_date="2023-12-31"
)

# Load data
df_ex1 = load_exercise_data(config_ex1)
print(f"Data loaded: {len(df_ex1)} bars")
print(f"Date range: {df_ex1['timestamp'].min()} to {df_ex1['timestamp'].max()}")
print("\nFirst few records:")
df_ex1.head()

# %%
# Compute returns
returns, timestamps = compute_returns(df_ex1)

print("Returns Statistics:")
print(f"  Count: {len(returns)}")
print(f"  Mean: {returns.mean():.6f} ({returns.mean() * 100:.4f}%)")
print(f"  Std Dev: {returns.std():.6f} ({returns.std() * 100:.4f}%)")
print(f"  Min: {returns.min():.6f} ({returns.min() * 100:.4f}%)")
print(f"  Max: {returns.max():.6f} ({returns.max() * 100:.4f}%)")
print(f"  Skewness: {stats.skew(returns):.4f}")
print(f"  Kurtosis: {stats.kurtosis(returns):.4f}")

# %%
# Visualize returns distribution
fig, axes = plt.subplots(1, 2, figsize=(14, 4))

axes[0].hist(
    returns * 100, bins=50, alpha=0.7, color="steelblue", edgecolor="black"
)
axes[0].set_xlabel("Return (%)")
axes[0].set_ylabel("Frequency")
axes[0].set_title(
    f"{config_ex1.asset} {config_ex1.frequency} Returns Distribution"
)
axes[0].axvline(
    returns.mean() * 100,
    color="red",
    linestyle="--",
    label=f"Mean: {returns.mean() * 100:.4f}%",
)
axes[0].legend()

axes[1].plot(
    timestamps, np.cumsum(returns) * 100, linewidth=1, color="darkgreen"
)
axes[1].set_xlabel("Time")
axes[1].set_ylabel("Cumulative Return (%)")
axes[1].set_title(f"{config_ex1.asset} Cumulative Returns")
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

# %%
# Run simulations for range of hit rates
hit_rates = np.arange(0.45, 0.80, 0.01)  # 45% to 55%
results_list = []
all_pnl_arrays = {}  # Store full PnL arrays for visualization

for hr in hit_rates:
    pnl_array, stats = simulate_trading_with_hit_rate(
        returns, hit_rate=hr, num_simulations=10000, transaction_cost=0.001
    )
    results_list.append(stats)
    all_pnl_arrays[hr] = pnl_array

# Create results dataframe
results_df = pd.DataFrame(results_list)

print("\nHit Rate Sensitivity Analysis:")
print(
    results_df[
        ["hit_rate", "mean_pnl", "std_pnl", "prob_profit", "sharpe_ratio"]
    ].to_string(index=False)
)

# %%
# Visualize PnL distributions for selected hit rates
selected_hrs = [0.45, 0.50, 0.51, 0.52, 0.55]

fig, axes = plt.subplots(2, 3, figsize=(16, 10))
axes = axes.flatten()

for idx, hr in enumerate(selected_hrs):
    if hr not in all_pnl_arrays:
        continue

    pnl_array = all_pnl_arrays[hr]

    axes[idx].hist(
        pnl_array, bins=50, alpha=0.7, color="steelblue", edgecolor="black"
    )
    axes[idx].axvline(
        np.mean(pnl_array),
        color="red",
        linestyle="--",
        linewidth=2,
        label=f"Mean: {np.mean(pnl_array):.4f}",
    )
    axes[idx].axvline(
        np.median(pnl_array),
        color="orange",
        linestyle="--",
        linewidth=2,
        label=f"Median: {np.median(pnl_array):.4f}",
    )
    axes[idx].axvline(0, color="black", linestyle="-", linewidth=1, alpha=0.5)

    axes[idx].set_xlabel("PnL")
    axes[idx].set_ylabel("Frequency")
    axes[idx].set_title(f"Hit Rate = {hr:.2%}")
    axes[idx].legend()
    axes[idx].grid(True, alpha=0.3)

axes[5].axis("off")

plt.suptitle(
    "PnL Distribution by Hit Rate (10,000 simulations each)",
    fontsize=14,
    fontweight="bold",
)
plt.tight_layout()
plt.show()

# %%
# Create sensitivity analysis plots
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Plot 1: Mean PnL vs Hit Rate
axes[0, 0].plot(
    results_df["hit_rate"] * 100,
    results_df["mean_pnl"],
    marker="o",
    linewidth=2,
    markersize=8,
    color="steelblue",
)
axes[0, 0].axhline(0, color="red", linestyle="--", linewidth=1, alpha=0.5)
axes[0, 0].set_xlabel("Hit Rate (%)")
axes[0, 0].set_ylabel("Mean PnL")
axes[0, 0].set_title("Expected PnL vs Hit Rate")
axes[0, 0].grid(True, alpha=0.3)

# Plot 2: Probability of Profit
axes[0, 1].plot(
    results_df["hit_rate"] * 100,
    results_df["prob_profit"] * 100,
    marker="s",
    linewidth=2,
    markersize=8,
    color="darkgreen",
)
axes[0, 1].axhline(
    50,
    color="orange",
    linestyle="--",
    linewidth=1,
    alpha=0.5,
    label="50% (neutral)",
)
axes[0, 1].set_xlabel("Hit Rate (%)")
axes[0, 1].set_ylabel("Probability of Profit (%)")
axes[0, 1].set_title("Probability of Profit vs Hit Rate")
axes[0, 1].set_ylim([0, 100])
axes[0, 1].legend()
axes[0, 1].grid(True, alpha=0.3)

# Plot 3: Sharpe Ratio
axes[1, 0].plot(
    results_df["hit_rate"] * 100,
    results_df["sharpe_ratio"],
    marker="^",
    linewidth=2,
    markersize=8,
    color="purple",
)
axes[1, 0].axhline(0, color="red", linestyle="--", linewidth=1, alpha=0.5)
axes[1, 0].set_xlabel("Hit Rate (%)")
axes[1, 0].set_ylabel("Sharpe Ratio")
axes[1, 0].set_title("Risk-Adjusted Return (Sharpe Ratio)")
axes[1, 0].grid(True, alpha=0.3)

# Plot 4: Risk Metrics
ax_std = axes[1, 1]
ax_dd = ax_std.twinx()

line1 = ax_std.plot(
    results_df["hit_rate"] * 100,
    results_df["std_pnl"],
    marker="o",
    linewidth=2,
    markersize=8,
    color="steelblue",
    label="Std Dev",
)
line2 = ax_dd.plot(
    results_df["hit_rate"] * 100,
    results_df["avg_max_drawdown"],
    marker="s",
    linewidth=2,
    markersize=8,
    color="darkred",
    label="Max Drawdown",
)

ax_std.set_xlabel("Hit Rate (%)")
ax_std.set_ylabel("PnL Std Dev", color="steelblue")
ax_dd.set_ylabel("Max Drawdown", color="darkred")
ax_std.set_title("Risk Metrics")
ax_std.tick_params(axis="y", labelcolor="steelblue")
ax_dd.tick_params(axis="y", labelcolor="darkred")
ax_std.grid(True, alpha=0.3)

lines = line1 + line2
labels = [l.get_label() for l in lines]
ax_std.legend(lines, labels, loc="upper left")

plt.suptitle("Hit Rate Sensitivity Analysis", fontsize=14, fontweight="bold")
plt.tight_layout()
plt.show()

# %%
# Summary of Exercise #1
print("\n" + "=" * 80)
print("EXERCISE #1 SUMMARY: Hit Rate → PnL Framework")
print("=" * 80)

# Find breakeven hit rate
zero_crossing_idx = np.where(np.diff(np.sign(results_df["mean_pnl"])))[0]
if len(zero_crossing_idx) > 0:
    be_idx = zero_crossing_idx[0]
    be_hr = results_df.iloc[be_idx]["hit_rate"]
    print("\n1. BREAKEVEN HIT RATE")
    print(f"   Approximately {be_hr:.2%} (accounting for transaction costs)")
else:
    print("\n1. BREAKEVEN HIT RATE")
    print("   All hit rates tested are either profitable or unprofitable")

# Maximum Sharpe ratio
max_sharpe_idx = results_df["sharpe_ratio"].idxmax()
max_sharpe_hr = results_df.loc[max_sharpe_idx, "hit_rate"]
max_sharpe = results_df.loc[max_sharpe_idx, "sharpe_ratio"]
print("\n2. OPTIMAL HIT RATE (Maximum Sharpe Ratio)")
print(f"   Hit Rate: {max_sharpe_hr:.2%}")
print(f"   Sharpe Ratio: {max_sharpe:.4f}")

# Sensitivity to hit rate change
hr_diff_pct = 100 * (
    results_df["hit_rate"].iloc[-1] - results_df["hit_rate"].iloc[0]
)
pnl_diff = results_df["mean_pnl"].iloc[-1] - results_df["mean_pnl"].iloc[0]
sensitivity = pnl_diff / hr_diff_pct if hr_diff_pct != 0 else 0
print("\n3. SENSITIVITY: PnL Change per 1% Hit Rate Increase")
print(f"   Δ(Mean PnL) / Δ(Hit Rate %) = {sensitivity:.6f}")

# Risk-adjusted metrics at 51%
print("\n4. RISK METRICS at 51% Hit Rate (benchmark)")
hr_51_stats = results_df[results_df["hit_rate"].round(2) == 0.51].iloc[0]
print(f"   Mean PnL: {hr_51_stats['mean_pnl']:.6f}")
print(f"   Std Dev: {hr_51_stats['std_pnl']:.6f}")
print(f"   P(Profit): {hr_51_stats['prob_profit']:.2%}")
# print(f'   VaR(95%): {hr_51_stats["var_95"]:.6f}')
print(f"   Sharpe Ratio: {hr_51_stats['sharpe_ratio']:.4f}")

print("\n5. KEY INSIGHTS")
print("   • Profitability is highly sensitive to small changes in hit rate")
print("   • Transaction costs significantly impact breakeven threshold")
print(
    "   • Even small positive expected value can be valuable with low volatility"
)
print("   • Risk-adjusted returns matter more than raw PnL")

print("\n" + "=" * 80)

# %%
# Load Bitcoin data from Kaggle (mczielinski/bitcoin-historical-data)
# Data: OHLCV at 1-minute granularity from 2013-2021
# Source: https://www.kaggle.com/datasets/mczielinski/bitcoin-historical-data

try:
    # Load from Kaggle using kagglehub
    df_raw = ftu.load_kaggle_bitcoin_data(
        start_date="2021-01-01", end_date="2021-01-28"
    )
    print(f"Loaded {len(df_raw)} records from Kaggle")
except Exception as e:
    print(f"Kaggle load failed ({e}). Using synthetic data for testing.")
    df_raw = ftu.generate_synthetic_bitcoin_data("2021-01-01", "2021-01-28")

# Resample to hourly if needed (1-minute data is very large)
# Uncomment to resample:
# df_raw = resample_to_interval(df_raw, '1h')

print(f"Raw data shape: {df_raw.shape}")
print(f"Date range: {df_raw['timestamp'].min()} to {df_raw['timestamp'].max()}")
df_raw.head()
