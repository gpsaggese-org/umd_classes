"""
Utility functions for metalearners tutorial (L08_04_07).

Import as:

import msml610.tutorials.L08_causal_inference.L08_04_07_metalearners_utils as mtlcil00mu
"""

from typing import Tuple

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from lightgbm import LGBMRegressor
from sklearn.linear_model import LogisticRegression

# Plot styling constants.
MARKER = ["o", "s"]  # Circle for T=0, Square for T=1.
COLOR = ["#FF6B6B", "#4ECDC4"]  # Red for T=1, Teal for T=0.


# #############################################################################
# Cell 2: T-Learner with Synthetic Data
# #############################################################################


def _g_kernel(x: np.ndarray, *, c: float = 0, s: float = 0.05) -> np.ndarray:
    """
    Gaussian kernel function.

    Computes a Gaussian kernel centered at c with scale s.

    :param x: Input values.
    :param c: Center of the kernel.
    :param s: Scale parameter (smaller s = sharper kernel).
    :return: Kernel values.
    """
    return np.exp((-((x - c) ** 2)) / s)


def generate_synthetic_treatment_data(
    n0: int,
    n1: int,
    *,
    seed: int = 123,
) -> pd.DataFrame:
    """
    Generate synthetic treatment/control data.

    Creates data with:
    - Control group (T=0): n0 samples from a Gaussian kernel-based model.
    - Treated group (T=1): n1 samples with a shifted mean (+1).

    :param n0: Number of control samples.
    :param n1: Number of treated samples.
    :param seed: Random seed for reproducibility.
    :return: DataFrame with columns 'x', 'y', 't'.

    Example:
        >>> df = generate_synthetic_treatment_data(n0=500, n1=50, seed=123)
        >>> df.head()
               x         y  t
        0 -0.977578  0.271234  0
        1 -0.968858  0.289456  0
        2 -0.965465  0.303221  0
        3 -0.960224  0.315678  0
        4 -0.958736  0.321890  0
    """
    np.random.seed(seed)
    # Control group follows a Gaussian kernel-based model.
    x0 = np.random.uniform(-1, 1, n0)
    y0 = np.random.normal(0.3 * _g_kernel(x0), 0.1, n0)
    # Treated group has the same functional form but shifted up by 1.
    x1 = np.random.uniform(-1, 1, n1)
    y1 = np.random.normal(0.3 * _g_kernel(x1), 0.1, n1) + 1
    # Combine groups and sort for consistent visualization and analysis.
    df = pd.concat(
        [
            pd.DataFrame(dict(x=x0, y=y0, t=0)),
            pd.DataFrame(dict(x=x1, y=y1, t=1)),
        ]
    ).sort_values(by="x")
    return df


def fit_tlearner_models(
    df: pd.DataFrame,
    min_child_samples: int = 25,
) -> Tuple[LGBMRegressor, LGBMRegressor, np.ndarray, np.ndarray]:
    """
    Fit outcome models for each treatment group.

    Trains separate `LGBMRegressor` models for control (T=0) and treated (T=1)
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
    # Train separate outcome models for each treatment group.
    m0 = LGBMRegressor(min_child_samples=min_child_samples, verbosity=-1)
    m1 = LGBMRegressor(min_child_samples=min_child_samples, verbosity=-1)
    m0.fit(x0, y0)
    m1.fit(x1, y1)
    # Generate predictions across the full dataset for both models.
    X_full = np.asarray(df[["x"]])
    m0_hat = m0.predict(X_full)
    m1_hat = m1.predict(X_full)
    return m0, m1, m0_hat, m1_hat


def plot_tlearner_treatment_effect_analysis(
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
    # Plot observed outcomes by treatment group for visual comparison.
    ax1.scatter(
        x0,
        y0,
        alpha=0.5,
        label="T=0",
        marker=MARKER[0],
        color=COLOR[1],
    )
    ax1.scatter(
        x1,
        y1,
        alpha=0.7,
        label="T=1",
        marker=MARKER[1],
        color=COLOR[0],
    )
    # Overlay fitted conditional expectation functions for each treatment group.
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
        marker=MARKER[0],
        color=COLOR[1],
    )
    ax2.scatter(
        x1,
        tau_1,
        label=r"$\hat{\tau}_1$",
        alpha=0.7,
        marker=MARKER[1],
        color=COLOR[0],
    )
    # Compute CATE as the difference between fitted models across the feature space.
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


# #############################################################################
# Cell 3: X-Learner
# #############################################################################


def calculate_xlearner_heterogeneous_treatment_effects(
    df: pd.DataFrame,
    m0: LGBMRegressor,
    m1: LGBMRegressor,
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Calculate heterogeneous treatment effects for X-Learner.

    Computes the estimated treatment effect for control and treated units:
    - For control units: tau_0 = m1_prediction - actual_outcome
    - For treated units: tau_1 = actual_outcome - m0_prediction

    :param df: DataFrame with columns 'x', 'y', 't'.
    :param m0: Fitted outcome model for control group.
    :param m1: Fitted outcome model for treated group.
    :return: Tuple of (tau_0, tau_1) arrays.
    """
    x0_full = np.asarray(df.query("t==0")[["x"]])
    y0_full = np.asarray(df.query("t==0")["y"])
    tau_0 = m1.predict(x0_full) - y0_full
    x1_full = np.asarray(df.query("t==1")[["x"]])
    y1_full = np.asarray(df.query("t==1")["y"])
    tau_1 = y1_full - m0.predict(x1_full)
    return tau_0, tau_1


def fit_xlearner_models(
    df: pd.DataFrame,
    tau_0: np.ndarray,
    tau_1: np.ndarray,
    min_child_samples: int = 25,
) -> Tuple[LGBMRegressor, LGBMRegressor, np.ndarray, np.ndarray]:
    """
    Fit X-Learner models on heterogeneous treatment effects.

    Trains separate models to predict the heterogeneous treatment effects
    for each treatment group.

    :param df: DataFrame with columns 'x', 't'.
    :param tau_0: Heterogeneous treatment effects for control units.
    :param tau_1: Heterogeneous treatment effects for treated units.
    :param min_child_samples: LightGBM min_child_samples parameter.
    :return: Tuple of (mu_tau0, mu_tau1, mu_tau0_hat, mu_tau1_hat).
    """
    x0 = np.asarray(df.query("t==0")[["x"]])
    x1 = np.asarray(df.query("t==1")[["x"]])
    mu_tau0 = LGBMRegressor(min_child_samples=min_child_samples, verbosity=-1)
    mu_tau1 = LGBMRegressor(min_child_samples=min_child_samples, verbosity=-1)
    mu_tau0.fit(x0, tau_0)
    mu_tau1.fit(x1, tau_1)
    mu_tau0_hat = mu_tau0.predict(x0)
    mu_tau1_hat = mu_tau1.predict(x1)
    return mu_tau0, mu_tau1, mu_tau0_hat, mu_tau1_hat


def plot_xlearner_effect_estimates(
    df: pd.DataFrame,
    tau_0: np.ndarray,
    tau_1: np.ndarray,
    mu_tau0_hat: np.ndarray,
    mu_tau1_hat: np.ndarray,
) -> None:
    """
    Plot X-Learner heterogeneous treatment effect estimates.

    Visualizes the estimated heterogeneous effects and fitted models.

    :param df: DataFrame with columns 'x', 't'.
    :param tau_0: Heterogeneous effects for control units.
    :param tau_1: Heterogeneous effects for treated units.
    :param mu_tau0_hat: Fitted effect predictions for control group.
    :param mu_tau1_hat: Fitted effect predictions for treated group.
    """
    plt.figure(figsize=(10, 4))
    x0 = np.asarray(df.query("t==0")[["x"]])
    x1 = np.asarray(df.query("t==1")[["x"]])
    # Plot heterogeneous effect estimates for each treatment group.
    plt.scatter(
        x0,
        tau_0,
        label=r"$\hat{\tau}_0$",
        alpha=0.5,
        marker=MARKER[0],
        color=COLOR[1],
    )
    plt.scatter(
        x1,
        tau_1,
        label=r"$\hat{\tau}_1$",
        alpha=0.8,
        marker=MARKER[1],
        color=COLOR[0],
    )
    # Overlay fitted X-Learner models showing estimated treatment effects.
    plt.plot(
        x0,
        mu_tau0_hat,
        color="black",
        linestyle="solid",
        label=r"$\hat{\mu}_{\tau_0}$",
    )
    plt.plot(
        x1,
        mu_tau1_hat,
        color="black",
        linestyle="dashed",
        label=r"$\hat{\mu}_{\tau_1}$",
    )
    plt.ylabel("Estimated Effect")
    plt.xlabel("X")
    plt.legend(fontsize=14)


def plot_xlearner_with_propensity_scores(
    df: pd.DataFrame,
    mu_tau0: LGBMRegressor,
    mu_tau1: LGBMRegressor,
    tau_0: np.ndarray,
    tau_1: np.ndarray,
) -> None:
    """
    Plot X-Learner CATE with propensity score weighting.

    Visualizes the conditional average treatment effect (CATE) computed
    as a propensity-score-weighted average of the treatment effect
    estimates.

    :param df: DataFrame with columns 'x', 't'.
    :param mu_tau0: X-Learner model for control group effects.
    :param mu_tau1: X-Learner model for treated group effects.
    :param tau_0: Heterogeneous effects for control units.
    :param tau_1: Heterogeneous effects for treated units.
    """
    plt.figure(figsize=(10, 4))
    # Fit propensity score model and extract treatment probabilities.
    ps_model = LogisticRegression(penalty=None)
    ps_model.fit(df[["x"]], df["t"])
    ps = ps_model.predict_proba(df[["x"]])[:, 1]
    # Compute CATE as propensity-score-weighted average of treatment effects.
    X_full = np.asarray(df[["x"]])
    cate = (1 - ps) * mu_tau1.predict(X_full) + ps * mu_tau0.predict(X_full)
    x0 = np.asarray(df.query("t==0")[["x"]])
    x1 = np.asarray(df.query("t==1")[["x"]])
    ps_0 = ps[df["t"] == 0]
    ps_1 = ps[df["t"] == 1]
    plt.scatter(
        x0,
        tau_0,
        label=r"$\hat{\tau}_0$",
        alpha=0.5,
        s=100 * (ps_0),
        marker=MARKER[0],
        color=COLOR[1],
    )
    plt.scatter(
        x1,
        tau_1,
        label=r"$\hat{\tau}_1$",
        alpha=0.5,
        s=100 * (1 - ps_1),
        marker=MARKER[1],
        color=COLOR[0],
    )
    plt.plot(df[["x"]], cate, label="x-learner", color="black")
    plt.ylabel("Estimated Effect")
    plt.xlabel("X")
    plt.legend(fontsize=14)


# #############################################################################
# Cell 4: X-Learner with Real Data and Propensity Score Weighting
# #############################################################################


def fit_propensity_score_and_weighted_outcome_models(
    train: pd.DataFrame,
    X: list,
    T: str,
    y: str,
) -> Tuple[LogisticRegression, LGBMRegressor, LGBMRegressor]:
    """
    Fit propensity score and weighted first-stage outcome models for X-Learner.

    Fits a propensity score model to estimate treatment probability, then fits
    separate outcome models for control and treated groups using inverse
    probability weighting.

    :param train: Training DataFrame with features X, treatment T, and outcome y.
    :param X: List of feature column names.
    :param T: Treatment column name.
    :param y: Outcome column name.
    :return: Tuple of (ps_model, m0, m1) where ps_model is the fitted propensity
             score model and m0, m1 are the weighted outcome models.
    """
    ps_model = LogisticRegression(penalty=None)
    ps_model.fit(train[X], train[T])
    train_t0 = train.query(f"{T}==0")
    train_t1 = train.query(f"{T}==1")
    m0 = LGBMRegressor()
    m1 = LGBMRegressor()
    np.random.seed(123)
    m0.fit(
        train_t0[X],
        train_t0[y],
        sample_weight=1 / ps_model.predict_proba(train_t0[X])[:, 0],
    )
    m1.fit(
        train_t1[X],
        train_t1[y],
        sample_weight=1 / ps_model.predict_proba(train_t1[X])[:, 1],
    )
    return ps_model, m0, m1


def fit_xlearner_second_stage_models(
    train: pd.DataFrame,
    X: list,
    T: str,
    y: str,
    m0: LGBMRegressor,
    m1: LGBMRegressor,
) -> Tuple[LGBMRegressor, LGBMRegressor]:
    """
    Fit second-stage X-Learner models on residual treatment effects.

    Computes residual treatment effects (tau_hat) for each group and fits
    separate models to predict these effects.

    :param train: Training DataFrame with features X, treatment T, and outcome y.
    :param X: List of feature column names.
    :param T: Treatment column name.
    :param y: Outcome column name.
    :param m0: Fitted outcome model for control group.
    :param m1: Fitted outcome model for treated group.
    :return: Tuple of (m_tau_0, m_tau_1) models for predicting treatment effects.
    """
    train_t0 = train.query(f"{T}==0")
    train_t1 = train.query(f"{T}==1")
    tau_hat_0 = m1.predict(train_t0[X]) - train_t0[y]
    tau_hat_1 = train_t1[y] - m0.predict(train_t1[X])
    m_tau_0 = LGBMRegressor()
    m_tau_1 = LGBMRegressor()
    np.random.seed(123)
    m_tau_0.fit(train_t0[X], tau_hat_0)
    m_tau_1.fit(train_t1[X], tau_hat_1)
    return m_tau_0, m_tau_1


def estimate_xlearner_cate(
    test: pd.DataFrame,
    X: list,
    ps_model: LogisticRegression,
    m_tau_0: LGBMRegressor,
    m_tau_1: LGBMRegressor,
) -> pd.DataFrame:
    """
    Estimate CATE using propensity-score-weighted X-Learner effects.

    Combines the second-stage treatment effect models with propensity score
    weighting to produce final CATE estimates.

    :param test: Test DataFrame with features X.
    :param X: List of feature column names.
    :param ps_model: Fitted propensity score model.
    :param m_tau_0: Fitted effect model for control group.
    :param m_tau_1: Fitted effect model for treated group.
    :return: DataFrame with CATE predictions in 'cate' column.
    """
    ps_test = ps_model.predict_proba(test[X])[:, 1]
    cate = ps_test * m_tau_0.predict(test[X]) + (1 - ps_test) * m_tau_1.predict(
        test[X]
    )
    return test.assign(cate=cate)
