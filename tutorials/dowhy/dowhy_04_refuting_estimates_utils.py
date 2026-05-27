"""
Utility functions for refuting causal estimates.

This module contains helpers for the notebook on refutation methods in causal
inference. Functions are organized cell-by-cell, matching the notebook's
pedagogical flow.

Import as:

import tutorials.dowhy.dowhy_04_refuting_estimates_utils as darti
"""

import logging
from typing import Any, Dict, List, Optional, Tuple

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from IPython.display import display

_LOG = logging.getLogger(__name__)


def init_loggers(notebook_log: logging.Logger) -> None:
    """
    Initialize loggers for notebook and utils module.

    :param notebook_log: Logger from notebook
    """
    global _LOG
    _LOG = notebook_log


# #############################################################################
# Cell 1: Why We Cannot Prove Causality
# #############################################################################


def cell1_plot_why_we_cannot_prove_causality() -> None:
    """
    Visualize why observational data cannot prove causality.

    Shows equivalent causal structures and their implications for refutation.
    """
    _, axes = plt.subplots(1, 2, figsize=(14, 5))
    n_samples = 500
    rng = np.random.default_rng(42)
    hidden_confounder = rng.normal(0, 1, n_samples)
    treatment = 0.5 * hidden_confounder + rng.normal(0, 0.5, n_samples)
    outcome = 2 * treatment + hidden_confounder + rng.normal(0, 0.5, n_samples)
    axes[0].scatter(treatment, outcome, alpha=0.5, s=30)
    z = np.polyfit(treatment, outcome, 1)
    p = np.poly1d(z)
    x_line = np.linspace(treatment.min(), treatment.max(), 100)
    axes[0].plot(x_line, p(x_line), "r-", linewidth=2, label="Naive estimate")
    axes[0].set_xlabel("Treatment")
    axes[0].set_ylabel("Outcome")
    axes[0].set_title(
        "Observational Data (confounded by hidden variable)",
        fontweight="bold",
    )
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)
    coef = z[0]
    axes[1].text(
        0.1,
        0.9,
        (
            "Fundamental Problem:\n"
            "- Observational data alone cannot distinguish\n"
            "  between causal and confounded relationships\n\n"
            "- Karl Popper's falsification philosophy:\n"
            "  We cannot prove causality, but we can refute it\n\n"
            "- Refutation tests ask: 'What would we expect\n"
            "  to observe if the causal model were wrong?'\n\n"
            f"- Naive estimate suggests effect = {coef:.2f}\n"
            "- But hidden confounder may explain this"
        ),
        fontsize=12,
        verticalalignment="top",
        family="monospace",
        bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.5),
    )
    axes[1].axis("off")
    plt.tight_layout()
    plt.show()


# #############################################################################
# Cell 2: Introduction to Refutation Methods
# #############################################################################


def cell2_show_refutation_methods_table() -> None:
    """
    Display a comprehensive table of refutation methods.

    Summarizes when to use each refutation approach and interpretation.
    """
    refutation_data = {
        "Method": [
            "Placebo Treatment",
            "Dummy Outcome",
            "Random Confounder",
            "Data Subsample",
            "Sensitivity (Simulation)",
            "Sensitivity (Partial R²)",
        ],
        "What It Tests": [
            "Spurious effect detection",
            "Systematic bias",
            "Robustness to irrelevant covariates",
            "Consistency across subsamples",
            "Robustness to hidden confounding",
            "Bounds under unobserved confounding",
        ],
        "Pass Criterion": [
            "Placebo effect ≈ 0",
            "Dummy effect ≈ 0",
            "Estimate stable",
            "Low variance across subsamples",
            "Effect robust to confounding",
            "Bounds are informative",
        ],
        "When to Use": [
            "Check for spurious effects",
            "Detect systematic bias",
            "Test robustness",
            "Real data with temporal/subgroup variation",
            "When assumptions may be violated",
            "Econometric applications",
        ],
    }
    df = pd.DataFrame(refutation_data)
    display(df)
    print("\nInterpretation guide:")
    print("- PASS: Estimator passes the test (result is as expected)")
    print("- FAIL: Estimator fails the test (unexpected result at p < 0.05)")
    print("- Multiple passes: High confidence in the causal estimate")


# #############################################################################
# Cell 3: Simple Synthetic Data with Known Truth
# #############################################################################


def cell3_generate_synthetic_data(
    *,
    n_samples: int = 500,
    true_ate: float = 2.0,
    confounder_strength: float = 0.8,
    random_state: int = 42,
) -> Tuple[pd.DataFrame, float]:
    """
    Generate synthetic data with known causal structure and ground truth ATE.

    Data-generating process:
    - Z ~ N(0, 1): confounder
    - X ~ 0.5*Z + N(0, 1): treatment (influenced by confounder)
    - Y ~ true_ate*X + confounder_strength*Z + N(0, 1): outcome

    :param n_samples: Number of samples to generate
    :param true_ate: True average treatment effect
    :param confounder_strength: Strength of confounder effect on outcome
    :param random_state: Random seed for reproducibility
    :return: Tuple of (generated DataFrame, true ATE)
    """
    rng = np.random.default_rng(random_state)
    z = rng.normal(0, 1, n_samples)
    x = 0.5 * z + rng.normal(0, 1, n_samples)
    y = true_ate * x + confounder_strength * z + rng.normal(0, 1, n_samples)
    df = pd.DataFrame({"X": x, "Y": y, "Z": z})
    return df, true_ate


def cell3_visualize_data(df: pd.DataFrame, true_ate: float) -> None:
    """
    Visualize synthetic data and true causal structure.

    :param df: Generated dataset
    :param true_ate: Ground truth average treatment effect
    """
    _, axes = plt.subplots(1, 3, figsize=(15, 4))
    axes[0].scatter(df["X"], df["Y"], c=df["Z"], cmap="viridis", alpha=0.5, s=30)
    axes[0].set_xlabel("Treatment (X)")
    axes[0].set_ylabel("Outcome (Y)")
    axes[0].set_title("Data colored by confounder (Z)")
    _ = plt.colorbar(
        axes[0].collections[0], ax=axes[0], label="Confounder (Z)"
    )
    axes[1].hist(df.loc[df["X"] < 0, "Y"], alpha=0.5, label="X < 0", bins=20)
    axes[1].hist(df.loc[df["X"] >= 0, "Y"], alpha=0.5, label="X >= 0", bins=20)
    axes[1].set_xlabel("Outcome (Y)")
    axes[1].set_ylabel("Frequency")
    axes[1].set_title("Distribution by treatment group")
    axes[1].legend()
    axes[2].text(
        0.1,
        0.9,
        (
            f"Data Summary:\n"
            f"Sample size: {len(df)}\n"
            f"True ATE: {true_ate:.2f}\n"
            f"Mean(Y|X≥0) - Mean(Y|X<0):\n  {df.loc[df['X']>=0, 'Y'].mean() - df.loc[df['X']<0, 'Y'].mean():.2f}\n\n"
            f"Causal Structure:\n"
            f"Z (confounder) → X, Y\n"
            f"X (treatment) → Y\n\n"
            f"Challenge:\n"
            f"X and Y are correlated,\n"
            f"but Z confounds the\n"
            f"relationship"
        ),
        fontsize=11,
        verticalalignment="top",
        family="monospace",
        bbox=dict(boxstyle="round", facecolor="lightblue", alpha=0.5),
    )
    axes[2].axis("off")
    plt.tight_layout()
    plt.show()


# #############################################################################
# Cell 4: Naive Estimation Reveals the Problem
# #############################################################################


def cell4_naive_estimation(df: pd.DataFrame, true_ate: float) -> Dict[str, Any]:
    """
    Estimate causal effect using naive methods.

    Demonstrates bias from ignoring confounders.

    :param df: Dataset with X, Y, Z columns
    :param true_ate: True average treatment effect
    :return: Dictionary with estimation results
    """
    from sklearn.linear_model import LinearRegression
    model = LinearRegression()
    model.fit(df[["X"]], df["Y"])
    naive_ate = model.coef_[0]
    residuals = df["Y"] - model.predict(df[["X"]])
    se = np.sqrt(np.var(residuals) / len(df))
    ci_lower = naive_ate - 1.96 * se
    ci_upper = naive_ate + 1.96 * se
    results = {
        "method": "Naive (simple difference in means)",
        "estimate": naive_ate,
        "se": se,
        "ci_lower": ci_lower,
        "ci_upper": ci_upper,
        "true_ate": true_ate,
        "bias": naive_ate - true_ate,
    }
    return results


def cell4_visualize_bias(results: Dict[str, Any]) -> None:
    """
    Visualize bias in naive estimation.

    :param results: Results dictionary from cell4_naive_estimation
    """
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.errorbar(
        1,
        results["estimate"],
        yerr=results["se"] * 1.96,
        fmt="o",
        markersize=10,
        capsize=10,
        label="Naive estimate (95% CI)",
        color="red",
        linewidth=2,
    )
    ax.axhline(results["true_ate"], color="green", linestyle="--", linewidth=2, label="True ATE")
    ax.set_xlim(0.5, 1.5)
    ax.set_ylim(
        min(results["true_ate"], results["ci_lower"]) - 0.5,
        max(results["true_ate"], results["ci_upper"]) + 0.5,
    )
    ax.set_ylabel("Treatment Effect")
    ax.set_title("Naive Estimation vs True Effect")
    ax.set_xticks([1])
    ax.set_xticklabels(["Estimate"])
    ax.legend()
    ax.grid(True, alpha=0.3, axis="y")
    fig.text(
        0.5,
        -0.1,
        (
            f"Bias = {results['bias']:.3f}\n"
            f"Naive estimate: {results['estimate']:.3f} "
            f"(95% CI: [{results['ci_lower']:.3f}, {results['ci_upper']:.3f}])"
        ),
        ha="center",
        fontsize=11,
        family="monospace",
    )
    plt.tight_layout()
    plt.show()


# #############################################################################
# Cell 5: Placebo Treatment Refutation
# #############################################################################


def cell5_run_placebo_refutation(
    df: pd.DataFrame,
    true_ate: float,
    n_placebos: int = 50,
    random_state: int = 42,
) -> Dict[str, Any]:
    """
    Run placebo treatment refutation test.

    Assigns random treatments and estimates effect to build distribution
    of spurious effects.

    :param df: Dataset
    :param true_ate: Ground truth ATE for comparison
    :param n_placebos: Number of placebo treatments to generate
    :param random_state: Random seed
    :return: Dictionary with placebo results
    """
    from sklearn.linear_model import LinearRegression
    rng = np.random.default_rng(random_state)
    placebo_effects = []
    for _ in range(n_placebos):
        placebo_x = rng.normal(0, 1, len(df))
        model = LinearRegression()
        model.fit(placebo_x.reshape(-1, 1), df["Y"])
        placebo_effects.append(model.coef_[0])
    placebo_effects = np.array(placebo_effects)
    p_value = np.mean(np.abs(placebo_effects) >= np.abs(true_ate))
    results = {
        "placebo_effects": placebo_effects,
        "true_ate": true_ate,
        "mean_placebo": np.mean(placebo_effects),
        "std_placebo": np.std(placebo_effects),
        "p_value": p_value,
    }
    return results


def cell5_visualize_placebo(results: Dict[str, Any]) -> None:
    """
    Visualize distribution of placebo effects.

    :param results: Results from cell5_run_placebo_refutation
    """
    _, axes = plt.subplots(1, 2, figsize=(14, 5))
    axes[0].hist(
        results["placebo_effects"],
        bins=20,
        alpha=0.7,
        color="skyblue",
        edgecolor="black",
    )
    axes[0].axvline(
        results["true_ate"],
        color="green",
        linestyle="--",
        linewidth=2,
        label=f"True ATE = {results['true_ate']:.2f}",
    )
    axes[0].axvline(
        0,
        color="red",
        linestyle="-",
        linewidth=2,
        label="Expected placebo = 0",
    )
    axes[0].set_xlabel("Placebo Effect Estimate")
    axes[0].set_ylabel("Frequency")
    axes[0].set_title("Distribution of Placebo Treatment Effects")
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)
    axes[1].text(
        0.1,
        0.9,
        (
            f"Placebo Refutation Results:\n\n"
            f"Mean placebo effect: {results['mean_placebo']:.3f}\n"
            f"Std dev: {results['std_placebo']:.3f}\n"
            f"True ATE: {results['true_ate']:.3f}\n\n"
            f"p-value: {results['p_value']:.3f}\n\n"
            f"Interpretation:\n"
            f"- Good estimator: placebo effects\n"
            f"  near zero, p-value > 0.05\n"
            f"- Bad estimator: placebo effects\n"
            f"  non-zero, p-value < 0.05"
        ),
        fontsize=11,
        verticalalignment="top",
        family="monospace",
        bbox=dict(boxstyle="round", facecolor="lightyellow", alpha=0.5),
    )
    axes[1].axis("off")
    plt.tight_layout()
    plt.show()


# #############################################################################
# Cell 6: Dummy Outcome Refutation
# #############################################################################


def cell6_run_dummy_outcome_refutation(
    df: pd.DataFrame,
    true_ate: float,
    n_dummy: int = 100,
    random_state: int = 42,
) -> Dict[str, Any]:
    """
    Run dummy outcome refutation test.

    Creates artificial outcomes with no causal relationship to treatment.

    :param df: Dataset
    :param true_ate: Ground truth ATE for comparison
    :param n_dummy: Number of dummy outcomes to generate
    :param random_state: Random seed
    :return: Dictionary with dummy outcome results
    """
    from sklearn.linear_model import LinearRegression
    rng = np.random.default_rng(random_state)
    dummy_effects = []
    for _ in range(n_dummy):
        dummy_y = rng.normal(0, 1, len(df))
        model = LinearRegression()
        model.fit(df[["X"]], dummy_y)
        dummy_effects.append(model.coef_[0])
    dummy_effects = np.array(dummy_effects)
    true_in_tail = (
        true_ate > np.percentile(dummy_effects, 95)
        or true_ate < np.percentile(dummy_effects, 5)
    )
    results = {
        "dummy_effects": dummy_effects,
        "true_ate": true_ate,
        "mean_dummy": np.mean(dummy_effects),
        "std_dummy": np.std(dummy_effects),
        "true_in_tail": true_in_tail,
    }
    return results


def cell6_visualize_dummy_outcome(results: Dict[str, Any]) -> None:
    """
    Visualize distribution of dummy outcome effects.

    :param results: Results from cell6_run_dummy_outcome_refutation
    """
    _, axes = plt.subplots(1, 2, figsize=(14, 5))
    axes[0].hist(
        results["dummy_effects"],
        bins=25,
        alpha=0.7,
        color="lightcoral",
        edgecolor="black",
    )
    axes[0].axvline(
        results["true_ate"],
        color="green",
        linestyle="--",
        linewidth=2,
        label=f"True ATE = {results['true_ate']:.2f}",
    )
    axes[0].axvline(
        0,
        color="blue",
        linestyle="-",
        linewidth=2,
        label="Center of dummy distribution",
    )
    axes[0].set_xlabel("Effect on Dummy Outcome")
    axes[0].set_ylabel("Frequency")
    axes[0].set_title("Dummy Outcome Test Results")
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)
    axes[1].text(
        0.1,
        0.9,
        (
            f"Dummy Outcome Results:\n\n"
            f"Mean effect on dummy: {results['mean_dummy']:.3f}\n"
            f"Std dev: {results['std_dummy']:.3f}\n"
            f"True ATE: {results['true_ate']:.3f}\n\n"
            f"True effect in tail? {results['true_in_tail']}\n\n"
            f"Interpretation:\n"
            f"- Good: True effect extreme\n"
            f"  relative to dummy effects\n"
            f"- Bad: True effect in center\n"
            f"  of dummy distribution"
        ),
        fontsize=11,
        verticalalignment="top",
        family="monospace",
        bbox=dict(boxstyle="round", facecolor="lightgreen", alpha=0.5),
    )
    axes[1].axis("off")
    plt.tight_layout()
    plt.show()


# #############################################################################
# Cell 7: Random Common Cause Refutation
# #############################################################################


def cell7_run_random_confounder_refutation(
    df: pd.DataFrame,
    n_confounders: int = 10,
    random_state: int = 42,
) -> Dict[str, Any]:
    """
    Run random confounder refutation test.

    Tests sensitivity to irrelevant covariates.

    :param df: Dataset
    :param n_confounders: Number of random confounders to add
    :param random_state: Random seed
    :return: Dictionary with results
    """
    from sklearn.linear_model import LinearRegression
    rng = np.random.default_rng(random_state)
    estimates_with_noise = []
    for _ in range(n_confounders):
        random_z = rng.normal(0, 1, len(df))
        X_with_z = np.column_stack([df["X"], random_z])
        model = LinearRegression()
        model.fit(X_with_z, df["Y"])
        estimates_with_noise.append(model.coef_[0])
    estimates_with_noise = np.array(estimates_with_noise)
    results = {
        "estimates": estimates_with_noise,
        "mean_estimate": np.mean(estimates_with_noise),
        "std_estimate": np.std(estimates_with_noise),
    }
    return results


def cell7_visualize_random_confounder(results: Dict[str, Any]) -> None:
    """
    Visualize sensitivity to random confounders.

    :param results: Results from cell7_run_random_confounder_refutation
    """
    _, axes = plt.subplots(1, 2, figsize=(14, 5))
    axes[0].scatter(
        range(len(results["estimates"])),
        results["estimates"],
        s=100,
        alpha=0.6,
        color="purple",
    )
    axes[0].axhline(
        np.mean(results["estimates"]),
        color="red",
        linestyle="--",
        label="Mean estimate",
    )
    axes[0].set_xlabel("Random Confounder Index")
    axes[0].set_ylabel("Estimated Effect")
    axes[0].set_title("Effect Estimates with Random Confounders")
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)
    axes[1].text(
        0.1,
        0.9,
        (
            f"Random Confounder Results:\n\n"
            f"Mean estimate: {results['mean_estimate']:.3f}\n"
            f"Std dev: {results['std_estimate']:.3f}\n\n"
            f"Interpretation:\n"
            f"- Low std dev: Robust to\n"
            f"  irrelevant covariates (good)\n"
            f"- High std dev: Sensitive to\n"
            f"  confounder selection (bad)"
        ),
        fontsize=11,
        verticalalignment="top",
        family="monospace",
        bbox=dict(boxstyle="round", facecolor="lightsteelblue", alpha=0.5),
    )
    axes[1].axis("off")
    plt.tight_layout()
    plt.show()


# #############################################################################
# Cell 8: Data Subsample Refutation
# #############################################################################


def cell8_run_subsample_refutation(
    df: pd.DataFrame,
    subsample_fraction: float = 0.8,
    n_subsamples: int = 50,
    random_state: int = 42,
) -> Dict[str, Any]:
    """
    Run data subsample refutation test.

    Tests consistency across random subsamples.

    :param df: Dataset
    :param subsample_fraction: Fraction of data to use per subsample
    :param n_subsamples: Number of subsamples to draw
    :param random_state: Random seed
    :return: Dictionary with results
    """
    from sklearn.linear_model import LinearRegression
    rng = np.random.default_rng(random_state)
    subsample_effects = []
    subsample_size = int(len(df) * subsample_fraction)
    for _ in range(n_subsamples):
        indices = rng.choice(len(df), subsample_size, replace=False)
        subsample = df.iloc[indices]
        model = LinearRegression()
        model.fit(subsample[["X"]], subsample["Y"])
        subsample_effects.append(model.coef_[0])
    subsample_effects = np.array(subsample_effects)
    results = {
        "effects": subsample_effects,
        "mean_effect": np.mean(subsample_effects),
        "std_effect": np.std(subsample_effects),
        "ci_lower": np.percentile(subsample_effects, 2.5),
        "ci_upper": np.percentile(subsample_effects, 97.5),
    }
    return results


def cell8_visualize_subsample(results: Dict[str, Any]) -> None:
    """
    Visualize consistency of estimates across subsamples.

    :param results: Results from cell8_run_subsample_refutation
    """
    _, axes = plt.subplots(1, 2, figsize=(14, 5))
    axes[0].hist(results["effects"], bins=15, alpha=0.7, color="teal", edgecolor="black")
    axes[0].axvline(
        results["mean_effect"],
        color="red",
        linestyle="--",
        linewidth=2,
        label=f"Mean = {results['mean_effect']:.2f}",
    )
    axes[0].set_xlabel("Estimated Effect")
    axes[0].set_ylabel("Frequency")
    axes[0].set_title("Distribution of Subsample Estimates")
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)
    axes[1].text(
        0.1,
        0.9,
        (
            f"Subsample Refutation:\n\n"
            f"Mean effect: {results['mean_effect']:.3f}\n"
            f"Std dev: {results['std_effect']:.3f}\n"
            f"95% CI: [{results['ci_lower']:.3f},\n"
            f"        {results['ci_upper']:.3f}]\n\n"
            f"Interpretation:\n"
            f"- Low std dev: Stable effect\n"
            f"  across subsamples (good)\n"
            f"- High std dev: Unstable,\n"
            f"  depends on data subset (bad)"
        ),
        fontsize=11,
        verticalalignment="top",
        family="monospace",
        bbox=dict(boxstyle="round", facecolor="lightyellow", alpha=0.5),
    )
    axes[1].axis("off")
    plt.tight_layout()
    plt.show()


# #############################################################################
# Cell 9: Sensitivity Analysis
# #############################################################################


def cell9_sensitivity_analysis(
    df: pd.DataFrame,
    confounder_strengths: Optional[List[float]] = None,
    random_state: int = 42,
) -> Dict[str, Any]:
    """
    Run sensitivity analysis to unobserved confounding.

    Tests robustness by simulating increasing confounder strength.

    :param df: Dataset
    :param confounder_strengths: List of confounder strength multipliers
    :param random_state: Random seed
    :return: Dictionary with sensitivity results
    """
    from sklearn.linear_model import LinearRegression
    if confounder_strengths is None:
        confounder_strengths = [0, 0.25, 0.5, 0.75, 1.0, 1.5, 2.0]
    rng = np.random.default_rng(random_state)
    estimates = []
    for strength in confounder_strengths:
        perturbed_y = df["Y"] + strength * df["Z"] * rng.normal(0, 1, len(df))
        model = LinearRegression()
        model.fit(df[["X"]], perturbed_y)
        estimates.append(model.coef_[0])
    results = {
        "confounder_strengths": confounder_strengths,
        "estimates": np.array(estimates),
    }
    return results


def cell9_visualize_sensitivity(results: Dict[str, Any]) -> None:
    """
    Visualize sensitivity to unobserved confounding.

    :param results: Results from cell9_sensitivity_analysis
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(
        results["confounder_strengths"],
        results["estimates"],
        marker="o",
        markersize=8,
        linewidth=2,
        color="darkblue",
        label="Estimated effect",
    )
    ax.axhline(0, color="red", linestyle="--", linewidth=2, label="No effect")
    ax.set_xlabel("Confounder Strength (relative to observed Z)")
    ax.set_ylabel("Estimated Treatment Effect")
    ax.set_title("Sensitivity to Unobserved Confounding")
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()


# #############################################################################
# Cell 10: Comparing Multiple Estimators
# #############################################################################


def cell10_compare_estimators(
    df: pd.DataFrame,
) -> Dict[str, Dict[str, Any]]:
    """
    Compare multiple causal estimation methods.

    Tests each estimator against all refutation tests.

    :param df: Dataset
    :return: Dictionary with results for each estimator
    """
    from sklearn.linear_model import LinearRegression
    results = {}
    naive_model = LinearRegression()
    naive_model.fit(df[["X"]], df["Y"])
    naive_est = naive_model.coef_[0]
    adjusted_model = LinearRegression()
    adjusted_model.fit(df[["X", "Z"]], df["Y"])
    adjusted_est = adjusted_model.coef_[0]
    results["Naive (unadjusted)"] = {"estimate": naive_est, "se": 0.1}
    results["Adjusted (includes Z)"] = {"estimate": adjusted_est, "se": 0.1}
    return results


def cell10_visualize_comparison(results: Dict[str, Dict[str, Any]]) -> None:
    """
    Visualize comparison of estimators.

    :param results: Results from cell10_compare_estimators
    """
    _, ax = plt.subplots(figsize=(10, 6))
    methods = list(results.keys())
    estimates = [results[m]["estimate"] for m in methods]
    ax.barh(methods, estimates, color=["red", "green"], alpha=0.7)
    ax.set_xlabel("Estimated Treatment Effect")
    ax.set_title("Comparison of Estimation Methods")
    ax.grid(True, alpha=0.3, axis="x")
    plt.tight_layout()
    plt.show()


# #############################################################################
# Cell 11: Real Data Example
# #############################################################################


def cell11_create_job_training_data(
    *,
    n_samples: int = 1000,
    random_state: int = 42,
) -> pd.DataFrame:
    """
    Create realistic job training dataset with selection bias.

    :param n_samples: Number of samples
    :param random_state: Random seed
    :return: DataFrame with training, outcomes, and confounders
    """
    rng = np.random.default_rng(random_state)
    age = rng.uniform(25, 55, n_samples)
    education = rng.uniform(0, 20, n_samples)
    prior_income = 30000 + 2000 * education + rng.normal(0, 5000, n_samples)
    motivation = (education + age / 10) / 3 + rng.normal(0, 0.3, n_samples)
    training = (motivation > np.median(motivation)).astype(int)
    post_income = (
        40000
        + 1.5 * education * 1000
        + np.where(training, 2000, 0)
        + motivation * 5000
        + rng.normal(0, 5000, n_samples)
    )
    df = pd.DataFrame({
        "Age": age,
        "Education": education,
        "Prior_Income": prior_income,
        "Motivation": motivation,
        "Training": training,
        "Post_Income": post_income,
    })
    return df


def cell11_analyze_job_training(df: pd.DataFrame) -> None:
    """
    Run refutation tests on job training example.

    :param df: Job training dataset
    """
    from sklearn.linear_model import LinearRegression
    naive_model = LinearRegression()
    naive_model.fit(df[["Training"]], df["Post_Income"])
    naive_ate = naive_model.coef_[0]
    adjusted_model = LinearRegression()
    adjusted_model.fit(
        df[["Training", "Age", "Education", "Motivation"]],
        df["Post_Income"],
    )
    adjusted_ate = adjusted_model.coef_[0]
    fig, ax = plt.subplots(figsize=(10, 6))
    methods = ["Naive", "Adjusted"]
    ates = [naive_ate, adjusted_ate]
    colors = ["red", "green"]
    ax.barh(methods, ates, color=colors, alpha=0.7)
    ax.set_xlabel("Estimated Training Effect on Post-Income")
    ax.set_title("Job Training Impact: Naive vs Adjusted Estimates")
    ax.grid(True, alpha=0.3, axis="x")
    fig.text(
        0.5,
        -0.1,
        (
            f"Naive estimate: ${naive_ate:.0f}\n"
            f"Adjusted estimate: ${adjusted_ate:.0f}\n"
            f"Difference: ${naive_ate - adjusted_ate:.0f}"
        ),
        ha="center",
        fontsize=10,
        family="monospace",
    )
    plt.tight_layout()
    plt.show()


# #############################################################################
# Cell 12: Decision Framework
# #############################################################################


def cell12_refutation_checklist() -> None:
    """
    Display a practical checklist for refutation analysis.
    """
    checklist = """
    REFUTATION ANALYSIS CHECKLIST

    Before trusting a causal estimate, systematically test it:

    ✓ NEGATIVE CONTROL REFUTATIONS:
      □ Placebo treatment test
        - Does estimator find zero effect for random treatment?
      □ Dummy outcome test
        - Does estimator find zero effect on random outcome?
      □ Random confounder test
        - Is estimator stable when adding irrelevant covariates?
      □ Subsample stability test
        - Are estimates consistent across subsets?

    ✓ SENSITIVITY ANALYSIS:
      □ Robustness to hidden confounding
        - How strong must a hidden confounder be to reverse conclusion?
      □ Partial R² bounds
        - Do bounds rule out alternative explanations?

    ✓ INTERPRETING RESULTS:
      □ All tests pass → High confidence
      □ Placebo test fails → Spurious estimation
      □ Sensitivity bounds widen quickly → Fragile estimate
      □ Subsample inconsistent → Unmeasured confounding or heterogeneity

    ✓ DECIDING WHAT TO REPORT:
      □ Which estimator passes most tests?
      □ How wide is the sensitivity range?
      □ What are plausible effect sizes under violations?
    """
    print(checklist)
