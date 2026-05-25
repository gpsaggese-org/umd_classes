"""
Utility functions for the Graphical Causal Models notebook.

Import as:

import tutorials.dowhy.dowhy_02_gcm_utils as tdd0gcut
"""

import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from typing import Callable, Dict, Tuple, Optional, Any

import helpers.hgraphviz as hgraphviz

# Constants for visualization.
DAG_FIGSIZE = (10, 8)

# #############################################################################
# Cell 1: What are Graphical Causal Models?
# #############################################################################


def cell1_plot_relationship(
    ax: Axes,
    x_data: Any,
    y_data: Any,
    *,
    x_label: Optional[str] = None,
    y_label: Optional[str] = None,
    title: str = "",
) -> None:
    """
    Plot a scatter plot showing relationship between two variables.

    :param ax: Matplotlib axes to plot on
    :param x_data: X-axis data
    :param y_data: Y-axis data
    :param x_label: Label for X-axis
        - Default: `None` (derived from `x_data.name` if available)
    :param y_label: Label for Y-axis
        - Default: `None` (derived from `y_data.name` if available)
    :param title: Title for the plot
        - Default: `""`
    :return: None
    """
    x_label_str: str = (
        x_label if x_label is not None else str(getattr(x_data, "name", "X"))
    )
    y_label_str: str = (
        y_label if y_label is not None else str(getattr(y_data, "name", "Y"))
    )
    ax.scatter(x_data, y_data, alpha=0.6)
    ax.set_xlabel(x_label_str)
    ax.set_ylabel(y_label_str)
    ax.set_title(title)


def cell1_create_health_dag() -> nx.DiGraph:
    """
    Create a simple health causal DAG.

    :return: Directed acyclic graph with health-related causal relationships
    """
    G = nx.DiGraph()
    G.add_edges_from(
        [
            ("Age", "Health"),
            ("Diet", "Health"),
            ("Exercise", "Health"),
            ("Genetics", "Health"),
        ]
    )
    return G


def cell1_plot_correlation_vs_causation() -> None:
    """
    Plot ice cream sales vs drowning example.

    Demonstrates the difference between statistical correlation and causal
    inference by showing how temperature confounds the relationship between
    ice cream sales and drownings.
    """
    _, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))
    # Generate synthetic temperature-driven data.
    np.random.seed(42)
    temperature = np.linspace(20, 35, 100) + np.random.normal(0, 1, 100)
    ice_cream_sales = 50 + 10 * temperature + np.random.normal(0, 10, 100)
    drownings = 5 + 0.5 * temperature + np.random.normal(0, 1, 100)
    # Plot 1: Correlation perspective (ignoring causal structure).
    ax1.scatter(ice_cream_sales, drownings, alpha=0.6, s=50)
    z = np.polyfit(ice_cream_sales, drownings, 1)
    p = np.poly1d(z)
    ax1.plot(ice_cream_sales, p(ice_cream_sales), "r--", lw=2)
    ax1.set_xlabel("Ice Cream Sales", fontsize=11)
    ax1.set_ylabel("Drownings", fontsize=11)
    ax1.set_title("Statistical correlation", fontsize=12, fontweight="bold")
    # Plot 2: Causal perspective (showing true causal structure).
    G = nx.DiGraph()
    G.add_edges_from(
        [("Temperature", "Ice Cream"), ("Temperature", "Drownings")]
    )
    hgraphviz.plot_causal_dag(
        G,
        "Causal structure",
        mode="graphviz",
        ax=ax2,
        figsize=(13, 5),
    )
    # Display the plots.
    plt.tight_layout()
    plt.show()


# #############################################################################
# Cell 2: Building a Simple GCM by Hand
# #############################################################################


def cell2_create_simple_gcm() -> Tuple[nx.DiGraph, Dict[str, Callable]]:
    """
    Create a simple causal graph with manually defined mechanisms.

    :return: Tuple of (directed acyclic graph, dictionary of mechanism functions)
    """
    G = nx.DiGraph()
    G.add_edges_from(
        [
            ("Temperature", "IceCreamSales"),
            ("Temperature", "Activity"),
            ("Activity", "IceCreamSales"),
        ]
    )
    mechanisms = {
        "Temperature": lambda n: np.random.normal(25, 5, n),
        "Activity": lambda t: 50 + 2 * t + np.random.normal(0, 5, len(t)),
        "IceCreamSales": lambda t, a: 100
        + 3 * t
        + 0.5 * a
        + np.random.normal(0, 10, len(t)),
    }
    return G, mechanisms


def cell2_generate_samples_from_gcm(
    G: nx.DiGraph,
    mechanisms: Dict[str, Callable],
    n_samples: int = 100,
) -> pd.DataFrame:
    """
    Generate samples from a structural causal model.

    Iterates through nodes in topological order and applies their mechanisms
    to generate synthetic samples respecting the causal structure.

    :param G: Directed acyclic graph representing the causal structure
    :param mechanisms: Dictionary mapping node names to mechanism functions
    :param n_samples: Number of samples to generate
        - Default: `100`
    :return: DataFrame with generated samples for each node
    """
    data = {}
    topo_order = list(nx.topological_sort(G))
    # Generate data for each node in topological order.
    for node in topo_order:
        parents = list(G.predecessors(node))
        if not parents:
            data[node] = mechanisms[node](n_samples)
        else:
            parent_data = [data[p] for p in parents]
            data[node] = mechanisms[node](*parent_data)
    return pd.DataFrame(data)


def cell2_plot_relationships(
    df: pd.DataFrame,
    x_var: str,
    y_var1: str,
    y_var2: str,
) -> None:
    """
    Plot three causal relationships for a simple GCM.

    Creates a 1x3 subplot showing relationships between an exogenous variable
    and two endogenous variables, plus their interaction.

    :param df: DataFrame with the data
    :param x_var: Name of the exogenous variable (e.g., "Temperature")
    :param y_var1: Name of first endogenous variable (e.g., "Activity")
    :param y_var2: Name of second endogenous variable (e.g., "IceCreamSales")
    :return: None
    """
    fig, axes = plt.subplots(1, 3, figsize=(14, 4))
    # Plot 1: exogenous → first endogenous.
    cell1_plot_relationship(
        axes[0],
        df[x_var],
        df[y_var1],
        title=f"{x_var} → {y_var1}",
    )
    # Plot 2: exogenous → second endogenous (direct effect).
    cell1_plot_relationship(
        axes[1],
        df[x_var],
        df[y_var2],
        title=f"{x_var} → {y_var2} (direct)",
    )
    # Plot 3: first endogenous → second endogenous (mediated effect).
    cell1_plot_relationship(
        axes[2],
        df[y_var1],
        df[y_var2],
        title=f"{y_var1} → {y_var2}",
    )
    plt.tight_layout()
    plt.show()


# #############################################################################
# Cell 3: Automatic Mechanism Assignment
# #############################################################################


def cell3_load_sample_dataset(
    dataset_name: str = "sachs",
) -> Tuple[pd.DataFrame, nx.DiGraph]:
    """
    Load a sample causal discovery dataset.

    Generates a synthetic version of the Sachs et al. protein signaling dataset
    with a known causal structure suitable for testing causal inference methods.

    :param dataset_name: Name of the dataset to load
        - Default: `"sachs"`
    :return: Tuple of (DataFrame with synthetic data, causal DAG)
    """
    np.random.seed(42)
    if dataset_name != "sachs":
        raise ValueError(f"Unknown dataset: {dataset_name}")
    # Simplified version of Sachs et al. protein signaling data.
    n = 200
    data = {}
    # Generate exogenous variables (no parents).
    data["PKC"] = np.random.normal(0, 1, n)
    data["PKA"] = np.random.normal(0, 1, n)
    # Generate endogenous variables following the causal structure.
    data["RAF"] = 0.5 * data["PKC"] + np.random.normal(0, 0.5, n)
    data["MEK"] = (
        0.6 * data["RAF"] + 0.3 * data["PKA"] + np.random.normal(0, 0.5, n)
    )
    data["ERK"] = 0.7 * data["MEK"] + np.random.normal(0, 0.5, n)
    data["AKT"] = (
        0.4 * data["PKA"] + 0.2 * data["ERK"] + np.random.normal(0, 0.5, n)
    )
    # Define the causal structure.
    G = nx.DiGraph()
    G.add_edges_from(
        [
            ("PKC", "RAF"),
            ("PKA", "RAF"),
            ("PKA", "MEK"),
            ("RAF", "MEK"),
            ("MEK", "ERK"),
            ("ERK", "AKT"),
            ("PKA", "AKT"),
        ]
    )
    return pd.DataFrame(data), G


def cell3_assign_mechanisms_automatically(
    G: nx.DiGraph,
    _df: pd.DataFrame,
) -> Dict[str, Dict[str, Any]]:
    """
    Assign causal mechanisms automatically based on data.

    Infers the type of mechanism (exogenous vs. endogenous linear) for each node
    based on its position in the causal graph.

    :param G: Directed acyclic graph representing the causal structure
    :param _df: DataFrame with data (unused, for interface compatibility)
    :return: Dictionary mapping node names to mechanism specifications
    """
    mechanisms = {}
    # Assign mechanisms based on node parentage.
    for node in nx.topological_sort(G):
        parents = list(G.predecessors(node))
        if not parents:
            mechanisms[node] = {
                "type": "exogenous",
                "form": "standard normal",
            }
        else:
            mechanisms[node] = {
                "type": "linear",
                "form": f"{node} = f({', '.join(parents)}) + noise",
                "parents": parents,
            }
    return mechanisms


# #############################################################################
# Cell 4: Fitting an SCM to Data
# #############################################################################


def cell4_fit_scm_simple(
    G: nx.DiGraph,
    df: pd.DataFrame,
) -> Dict[str, Dict[str, Any]]:
    """
    Fit a simple linear SCM to data.

    Estimates mean and standard deviation for exogenous variables, and fits
    linear regression models for endogenous variables conditioned on their parents.

    :param G: Directed acyclic graph representing the causal structure
    :param df: DataFrame containing the data to fit
    :return: Dictionary mapping node names to fitted model parameters
    """
    fitted_params = {}
    # Fit mechanisms for each node in topological order.
    for node in nx.topological_sort(G):
        parents = list(G.predecessors(node))
        if not parents:
            # Fit exogenous variables.
            fitted_params[node] = {
                "mean": float(df[node].mean()),
                "std": float(df[node].std()),
            }
        else:
            # Fit linear regression for endogenous variables.
            X = np.asarray(df[parents].values, dtype=float)
            y = np.asarray(df[node].values, dtype=float)
            X = np.column_stack([np.ones(len(X)), X])
            # Solve least squares problem.
            coeffs = np.linalg.lstsq(X, y, rcond=None)[0]
            residuals = y - X @ coeffs
            y_mean = np.mean(y)
            fitted_params[node] = {
                "coefficients": coeffs,
                "residual_std": float(np.std(residuals)),
                "r_squared": float(
                    1 - (np.sum(residuals**2) / np.sum((y - y_mean) ** 2))
                ),
            }
    return fitted_params


# #############################################################################
# Cell 5: Generating Samples from a Fitted Model
# #############################################################################


def cell5_generate_synthetic_samples(
    G: nx.DiGraph,
    fitted_params: Dict[str, Dict[str, Any]],
    n_samples: int = 100,
) -> pd.DataFrame:
    """
    Generate synthetic samples from a fitted SCM.

    Samples from exogenous variables and propagates samples through the causal
    structure using fitted linear models to generate endogenous variables.

    :param G: Directed acyclic graph representing the causal structure
    :param fitted_params: Dictionary with fitted parameters for each node
    :param n_samples: Number of samples to generate
        - Default: `100`
    :return: DataFrame with generated synthetic samples
    """
    data = {}
    # Generate samples for each node in topological order.
    for node in nx.topological_sort(G):
        params = fitted_params[node]
        if "mean" in params:
            # Sample exogenous variables.
            data[node] = np.random.normal(
                params["mean"], params["std"], n_samples
            )
        else:
            # Sample endogenous variables using fitted linear model.
            parents = list(G.predecessors(node))
            X = np.column_stack(
                [np.ones(n_samples), np.array([data[p] for p in parents]).T]
            )
            noise = np.random.normal(0, params["residual_std"], n_samples)
            data[node] = X @ params["coefficients"] + noise
    return pd.DataFrame(data)


def cell5_compare_distributions(
    df_original: pd.DataFrame,
    df_synthetic: pd.DataFrame,
    figsize: Optional[Tuple[float, float]] = None,
) -> None:
    """
    Compare original vs synthetic data distributions.

    Plots histograms side-by-side for each variable to visually assess how well
    the synthetic data matches the original data distribution.

    :param df_original: DataFrame with original data
    :param df_synthetic: DataFrame with synthetic data
    :param figsize: Figure size (width, height)
        - Default: `None` (uses (14, 4))
    :return: None
    """
    if figsize is None:
        figsize = (14, 4)
    # Create subplots for each variable.
    n_vars = len(df_original.columns)
    _, axes = plt.subplots(1, n_vars, figsize=figsize)
    # Handle single-column case.
    if n_vars == 1:
        axes = [axes]
    # Plot histograms for each variable.
    for ax, col in zip(axes, df_original.columns):
        ax.hist(
            df_original[col], alpha=0.5, bins=20, label="Original", color="blue"
        )
        ax.hist(
            df_synthetic[col],
            alpha=0.5,
            bins=20,
            label="Synthetic",
            color="orange",
        )
        ax.set_xlabel(col, fontsize=10)
        ax.set_ylabel("Frequency", fontsize=10)
        ax.legend()
    # Display the plots.
    plt.tight_layout()
    plt.show()


# #############################################################################
# Cell 6: Evaluating Model Quality
# #############################################################################


def cell6_evaluate_model_quality(
    G: nx.DiGraph,
    fitted_params: Dict[str, Dict[str, Any]],
    _df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Evaluate the quality of a fitted SCM.

    Computes quality metrics for each node: R² and residual standard deviation
    for linear fits, and mean/std for exogenous variables.

    :param G: Directed acyclic graph representing the causal structure
    :param fitted_params: Dictionary with fitted parameters for each node
    :param _df: DataFrame with data (unused, for interface compatibility)
    :return: DataFrame with quality metrics for each node
    """
    metrics = []
    # Compute quality metrics for each node.
    for node in nx.topological_sort(G):
        params = fitted_params[node]
        if "r_squared" in params:
            metrics.append(
                {
                    "Variable": node,
                    "Type": "linear fit",
                    "R²": params["r_squared"],
                    "Residual Std": params["residual_std"],
                }
            )
        else:
            metrics.append(
                {
                    "Variable": node,
                    "Type": "exogenous",
                    "Mean": params["mean"],
                    "Std": params["std"],
                }
            )
    return pd.DataFrame(metrics)


# #############################################################################
# Cell 7: Confidence Intervals for Causal Estimates
# #############################################################################


def cell7_bootstrap_confidence_intervals(
    _G: nx.DiGraph,
    df: pd.DataFrame,
    treatment_var: str,
    outcome_var: str,
    n_bootstrap: int = 100,
) -> Tuple[float, Tuple[float, float]]:
    """
    Estimate confidence intervals via bootstrap.

    Performs nonparametric bootstrap to estimate the confidence interval for a
    simple treatment effect (difference in means between treatment groups).

    :param _G: Directed acyclic graph (unused, for interface compatibility)
    :param df: DataFrame containing the data
    :param treatment_var: Name of the treatment variable
    :param outcome_var: Name of the outcome variable
    :param n_bootstrap: Number of bootstrap samples
        - Default: `100`
    :return: Tuple of (point estimate, (lower CI, upper CI))
    """
    effects = []
    # Perform bootstrap resampling.
    for _ in range(n_bootstrap):
        # Resample with replacement.
        idx = np.random.choice(len(df), size=len(df), replace=True)
        df_boot = df.iloc[idx]
        # Compute simple treatment effect.
        treated = float(
            df_boot[df_boot[treatment_var] > df_boot[treatment_var].median()][
                outcome_var
            ].mean()
        )
        control = float(
            df_boot[df_boot[treatment_var] <= df_boot[treatment_var].median()][
                outcome_var
            ].mean()
        )
        effect = treated - control
        effects.append(effect)
    # Compute point estimate and confidence interval.
    point_estimate = float(np.mean(effects))
    ci_lower = float(np.percentile(effects, 2.5))
    ci_upper = float(np.percentile(effects, 97.5))
    return point_estimate, (ci_lower, ci_upper)


# #############################################################################
# Cell 8: Customizing Causal Mechanism Assignment
# #############################################################################


def cell8_custom_mechanism_example() -> Tuple[nx.DiGraph, Dict[str, Callable]]:
    """
    Create a GCM with custom nonlinear mechanisms.

    Demonstrates how to define custom (nonlinear) causal mechanisms using
    lambda functions for more flexible structural causal models.

    :return: Tuple of (directed acyclic graph, dictionary of mechanism functions)
    """
    G = nx.DiGraph()
    G.add_edges_from(
        [
            ("Input", "Output1"),
            ("Input", "Output2"),
        ]
    )
    mechanisms = {
        "Input": lambda n: np.random.uniform(0, 10, n),
        "Output1": lambda x: np.sin(x / 5) * 100
        + np.random.normal(0, 10, len(x)),
        "Output2": lambda x: np.exp(x / 10) + np.random.normal(0, 2, len(x)),
    }
    return G, mechanisms


# #############################################################################
# Cell 9: Root Cause Analysis Example
# #############################################################################


def cell9_system_metrics_dataset(
    n_samples: int = 200,
) -> Tuple[pd.DataFrame, nx.DiGraph]:
    """
    Generate synthetic system metrics dataset.

    Creates a synthetic dataset of system performance metrics with known causal
    relationships suitable for root cause analysis examples.

    :param n_samples: Number of samples to generate
        - Default: `200`
    :return: Tuple of (DataFrame with synthetic metrics, causal DAG)
    """
    np.random.seed(42)
    data = {}
    # Generate exogenous variable.
    data["CpuUsage"] = np.random.uniform(10, 80, n_samples)
    # Generate endogenous variables following causal structure.
    data["MemoryUsage"] = (
        30 + 0.3 * data["CpuUsage"] + np.random.normal(0, 5, n_samples)
    )
    data["NetworkLatency"] = (
        10
        + 0.2 * data["CpuUsage"]
        + 0.15 * data["MemoryUsage"]
        + np.random.normal(0, 2, n_samples)
    )
    data["ApiLatency"] = (
        50
        + 0.5 * data["CpuUsage"]
        + 0.3 * data["NetworkLatency"]
        + np.random.normal(0, 5, n_samples)
    )
    # Define the causal structure.
    G = nx.DiGraph()
    G.add_edges_from(
        [
            ("CpuUsage", "MemoryUsage"),
            ("CpuUsage", "NetworkLatency"),
            ("MemoryUsage", "NetworkLatency"),
            ("NetworkLatency", "ApiLatency"),
            ("CpuUsage", "ApiLatency"),
        ]
    )
    return pd.DataFrame(data), G


# #############################################################################
# Cell 10: Medical Counterfactual Example
# #############################################################################


def cell10_medical_dataset(
    n_samples: int = 300,
) -> Tuple[pd.DataFrame, nx.DiGraph]:
    """
    Generate synthetic medical records dataset.

    Creates a synthetic medical dataset with confounded treatment assignment
    and causal relationships suitable for causal inference exercises.

    :param n_samples: Number of samples to generate
        - Default: `300`
    :return: Tuple of (DataFrame with synthetic medical data, causal DAG)
    """
    np.random.seed(42)
    data = {}
    # Generate exogenous variable.
    data["Age"] = np.random.uniform(30, 80, n_samples)
    # Generate confounders.
    data["BloodPressure"] = (
        120 + 0.3 * data["Age"] + np.random.normal(0, 10, n_samples)
    )
    data["Cholesterol"] = (
        180 + 0.5 * data["Age"] + np.random.normal(0, 20, n_samples)
    )
    # Generate confounded treatment assignment.
    treatment_prob = 1 / (1 + np.exp(-(data["Age"] - 60) / 10))
    data["Treatment"] = (np.random.random(n_samples) < treatment_prob).astype(
        int
    )
    # Generate outcome: depends on age, cholesterol, and treatment.
    data["Outcome"] = (
        50
        + 0.2 * data["Age"]
        + 0.1 * data["Cholesterol"]
        + 20 * data["Treatment"]
        + np.random.normal(0, 10, n_samples)
    )
    # Define the causal structure.
    G = nx.DiGraph()
    G.add_edges_from(
        [
            ("Age", "BloodPressure"),
            ("Age", "Cholesterol"),
            ("Age", "Treatment"),
            ("BloodPressure", "Outcome"),
            ("Cholesterol", "Outcome"),
            ("Treatment", "Outcome"),
        ]
    )
    return pd.DataFrame(data), G


# #############################################################################
# Cell 11: Model Limitations and When GCMs Fail
# #############################################################################


def cell11_demonstrate_unobserved_confounder() -> Tuple[
    pd.DataFrame, nx.DiGraph
]:
    """
    Demonstrate the effect of an unobserved confounder.

    Creates data where an unobserved confounder affects both X and Y, leading to
    spurious correlation when the true causal structure is unknown.

    :return: Tuple of (DataFrame with data showing confounder effect, observed DAG)
    """
    np.random.seed(42)
    n = 500
    # True causal structure includes unobserved confounder.
    unobserved_confounder = np.random.normal(0, 1, n)
    data = {}
    # Both X and Y are caused by the unobserved confounder.
    data["X"] = 0.5 * unobserved_confounder + np.random.normal(0, 1, n)
    data["Y"] = 0.5 * unobserved_confounder + np.random.normal(0, 1, n)
    # Define the observed graph (confounder is hidden).
    G_observed = nx.DiGraph()
    G_observed.add_nodes_from(["X", "Y"])
    return pd.DataFrame(data), G_observed


# #############################################################################
# Cell 12: Putting It All Together
# #############################################################################


def cell12_workflow_summary() -> Dict[str, str]:
    """
    Provide a summary of the complete GCM workflow.

    :return: Dictionary mapping workflow steps to their descriptions
    """
    workflow = {
        "Step 1": "Define causal graph from domain knowledge or discovery",
        "Step 2": "Specify or customize causal mechanisms",
        "Step 3": "Fit the model to available data",
        "Step 4": "Evaluate model quality and identify weak points",
        "Step 5": "Generate counterfactual predictions for decision-making",
    }
    return workflow
