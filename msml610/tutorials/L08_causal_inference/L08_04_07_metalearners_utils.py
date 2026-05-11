"""
Utility functions for metalearners tutorial (L08_04_07).

Import as:

import msml610.tutorials.L08_causal_inference.L08_04_07_metalearners_utils as ml
"""

from typing import Tuple

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# TODO(ai_gp): Use import lightgbm as lgb
from lightgbm import LGBMRegressor

# Plot styling constants.
_MARKER = ["o", "s"]  # Circle for T=0, Square for T=1.
_COLOR = ["#FF6B6B", "#4ECDC4"]  # Red for T=1, Teal for T=0.


# #############################################################################
# Cell 2: T-Learner with Synthetic Data
# #############################################################################


def _g_kernel(x: np.ndarray, c: float = 0, s: float = 0.05) -> np.ndarray:
    """
    Gaussian kernel function.

    Computes a Gaussian kernel centered at c with scale s.

    :param x: Input values.
    :param c: Center of the kernel.
    :param s: Scale parameter (smaller s = sharper kernel).
    :return: Kernel values.
    """
    return np.exp((-(x - c) ** 2) / s)


def generate_synthetic_treatment_data(
    n0: int = 500,
    n1: int = 50,
    seed: int = 123,
) -> pd.DataFrame:
    """
    Generate synthetic treatment/control data.

    Creates data with:
    - Control group (T=0): 500 samples from a Gaussian kernel-based model.
    - Treated group (T=1): 50 samples with a shifted mean (+1).

    :param n0: Number of control samples.
    :param n1: Number of treated samples.
    :param seed: Random seed for reproducibility.
    :return: DataFrame with columns 'x', 'y', 't'.
    """
    np.random.seed(seed)
    # Generate control group data.
    x0 = np.random.uniform(-1, 1, n0)
    y0 = np.random.normal(0.3 * _g_kernel(x0), 0.1, n0)
    # Generate treated group data with shifted mean.
    x1 = np.random.uniform(-1, 1, n1)
    y1 = np.random.normal(0.3 * _g_kernel(x1), 0.1, n1) + 1
    # Combine and sort by x.
    df = pd.concat(
        [
            pd.DataFrame(dict(x=x0, y=y0, t=0)),
            pd.DataFrame(dict(x=x1, y=y1, t=1)),
        ]
    ).sort_values(by="x")
    return df


def fit_outcome_models(
    df: pd.DataFrame,
    min_child_samples: int = 25,
) -> Tuple[LGBMRegressor, LGBMRegressor, np.ndarray, np.ndarray]:
    """
    Fit outcome models for each treatment group.

    Trains separate LGBMRegressor models for control (T=0) and treated (T=1)
    groups to estimate conditional outcome expectations.

    :param df: DataFrame with columns 'x', 'y', 't'.
    :param min_child_samples: LightGBM min_child_samples parameter.
    :return: Tuple of (m0, m1, m0_predictions, m1_predictions) where
             m0 and m1 are fitted regressors and predictions are on the
             full dataset.
    """
    x0 = np.asarray(df.query("t==0")["x"]).reshape(-1, 1)
    y0 = np.asarray(df.query("t==0")["y"])
    x1 = np.asarray(df.query("t==1")["x"]).reshape(-1, 1)
    y1 = np.asarray(df.query("t==1")["y"])
    # Fit models.
    m0 = LGBMRegressor(min_child_samples=min_child_samples, verbosity=-1)
    m1 = LGBMRegressor(min_child_samples=min_child_samples, verbosity=-1)
    m0.fit(x0, y0)
    m1.fit(x1, y1)
    # Get predictions on the full dataset.
    X_full = np.asarray(df[["x"]])
    m0_hat = m0.predict(X_full)
    m1_hat = m1.predict(X_full)
    return m0, m1, m0_hat, m1_hat


def plot_treatment_effect_analysis(
    df: pd.DataFrame,
    m0: LGBMRegressor,
    m1: LGBMRegressor,
    m0_hat: np.ndarray,
    m1_hat: np.ndarray,
) -> None:
    """
    Plot outcome models and treatment effect heterogeneity.

    Visualizes:
    - Top subplot: Scatter plots of control/treated outcomes and fitted models.
    - Bottom subplot: Estimated heterogeneous treatment effects.

    :param df: DataFrame with columns 'x', 'y', 't'.
    :param m0: Fitted outcome model for control group.
    :param m1: Fitted outcome model for treated group.
    :param m0_hat: Predictions from m0 on full dataset.
    :param m1_hat: Predictions from m1 on full dataset.
    """
    _ = plt.subplots(2, 1, figsize=(10, 10))
    ax1, ax2 = plt.gcf().axes[:2]
    # Top subplot: Outcome data and fitted models.
    x0 = np.asarray(df.query("t==0")["x"])
    y0 = np.asarray(df.query("t==0")["y"])
    x1 = np.asarray(df.query("t==1")["x"])
    y1 = np.asarray(df.query("t==1")["y"])
    # Scatter plots for each treatment group.
    ax1.scatter(
        x0,
        y0,
        alpha=0.5,
        label="T=0",
        marker=_MARKER[0],
        color=_COLOR[1],
    )
    ax1.scatter(
        x1,
        y1,
        alpha=0.7,
        label="T=1",
        marker=_MARKER[1],
        color=_COLOR[0],
    )
    # Fitted outcome models.
    x_vals = np.asarray(df["x"])
    x_sort_idx = np.argsort(x_vals)
    x_sorted = x_vals[x_sort_idx]
    m0_hat_sorted = m0_hat[x_sort_idx]
    m1_hat_sorted = m1_hat[x_sort_idx]
    ax1.plot(
        x_sorted,
        m0_hat_sorted,
        color="black",
        linestyle="solid",
        label=r"$\hat{\mu}_0$",
    )
    ax1.plot(
        x_sorted,
        m1_hat_sorted,
        color="black",
        linestyle="--",
        label=r"$\hat{\mu}_1$",
    )
    ax1.set_ylabel("Y", fontsize=12)
    ax1.set_xlabel("X", fontsize=12)
    ax1.legend(fontsize=14)
    # Bottom subplot: Heterogeneous treatment effects.
    # Effect for control units: prediction gap between models.
    x0_full = np.asarray(df.query("t==0")[["x"]])
    y0_full = np.asarray(df.query("t==0")["y"])
    tau_0 = m1.predict(x0_full) - y0_full
    # Effect for treated units: actual outcome gap.
    x1_full = np.asarray(df.query("t==1")[["x"]])
    y1_full = np.asarray(df.query("t==1")["y"])
    tau_1 = y1_full - m0.predict(x1_full)
    # Plot heterogeneous effects.
    ax2.scatter(
        x0,
        tau_0,
        label=r"$\hat{\tau}_0$",
        alpha=0.5,
        marker=_MARKER[0],
        color=_COLOR[1],
    )
    ax2.scatter(
        x1,
        tau_1,
        label=r"$\hat{\tau}_1$",
        alpha=0.7,
        marker=_MARKER[1],
        color=_COLOR[0],
    )
    # Conditional Average Treatment Effect (CATE).
    X_full = np.asarray(df[["x"]])
    cate = m1.predict(X_full) - m0.predict(X_full)
    ax2.plot(
        x_sorted,
        cate[x_sort_idx],
        label=r"$\hat{CATE}$",
        color="black",
    )
    ax2.set_ylabel("Estimated Effect", fontsize=12)
    ax2.set_xlabel("X", fontsize=12)
    ax2.legend(fontsize=14)
    plt.tight_layout()
