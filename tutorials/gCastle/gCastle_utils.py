"""
Utility functions for gCastle-based causal structure learning workflows.

Import as:

import tutorials.gCastle.gCastle_utils as tgcutil
"""

import logging
from typing import Any, Callable, Dict, List, Optional, Tuple

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd
from gcastle.metrics import MetricsDAG
from sklearn.preprocessing import StandardScaler

import helpers.hdbg as hdbg

_LOG = logging.getLogger(__name__)


# ###...### / Data Generation and Preparation / ###...###


def generate_linear_gaussian_data(
    num_samples: int,
    num_vars: int,
    edge_density: float = 0.3,
    random_state: Optional[int] = None,
) -> Tuple[np.ndarray, nx.DiGraph]:
    """
    Generate synthetic data from a linear Gaussian model with a random DAG.

    :param num_samples: Number of samples to generate
    :param num_vars: Number of variables
    :param edge_density: Probability of edge existence (0 to 1)
    :param random_state: Random seed for reproducibility
    :return: Tuple of (data array, true causal graph)
    """
    hdbg.dassert_lt(0, num_samples)
    hdbg.dassert_lt(0, num_vars)
    hdbg.dassert_lte(0, edge_density)
    hdbg.dassert_lte(edge_density, 1)

    np.random.seed(random_state)

    # Generate random DAG
    dag = nx.DiGraph()
    dag.add_nodes_from(range(num_vars))

    for i in range(num_vars):
        for j in range(i + 1, num_vars):
            if np.random.random() < edge_density:
                weight = np.random.uniform(-1, 1)
                dag.add_edge(i, j, weight=weight)

    # Generate data from linear Gaussian model
    topological_order = list(nx.topological_sort(dag))
    data = np.zeros((num_samples, num_vars))

    for node in topological_order:
        parents = list(dag.predecessors(node))
        if parents:
            weights = np.array([dag[p][node]["weight"] for p in parents])
            parent_data = data[:, parents]
            data[:, node] = parent_data @ weights + np.random.normal(0, 1, num_samples)
        else:
            data[:, node] = np.random.normal(0, 1, num_samples)

    return data, dag


def normalize_data(data: np.ndarray) -> np.ndarray:
    """
    Normalize data to have zero mean and unit variance.

    :param data: Input data array
    :return: Normalized data array
    """
    hdbg.dassert_isinstance(data, np.ndarray)
    hdbg.dassert_eq(data.ndim, 2)

    scaler = StandardScaler()
    return scaler.fit_transform(data)


def dag_to_adjacency(dag: nx.DiGraph, num_vars: int) -> np.ndarray:
    """
    Convert NetworkX DAG to adjacency matrix.

    :param dag: NetworkX directed graph
    :param num_vars: Number of variables
    :return: Adjacency matrix
    """
    hdbg.dassert_isinstance(dag, nx.DiGraph)
    hdbg.dassert_lt(0, num_vars)

    adj = np.zeros((num_vars, num_vars))
    for i, j in dag.edges():
        adj[i, j] = 1

    return adj


# ###...### / Causal Structure Learning / ###...###


def run_causal_algorithm(
    data: np.ndarray,
    algorithm_class: Callable,
    **kwargs: Any,
) -> np.ndarray:
    """
    Run a causal discovery algorithm on data.

    :param data: Input data array (samples x variables)
    :param algorithm_class: gCastle algorithm class
    :param kwargs: Additional arguments to pass to algorithm
    :return: Estimated adjacency matrix
    """
    hdbg.dassert_isinstance(data, np.ndarray)
    hdbg.dassert_eq(data.ndim, 2)

    algorithm = algorithm_class(**kwargs)
    algorithm.learn(data)
    return algorithm.causal_matrix


# ###...### / Evaluation and Metrics / ###...###


def compute_dag_metrics(
    estimated_adj: np.ndarray,
    true_adj: np.ndarray,
) -> Dict[str, float]:
    """
    Compute metrics comparing estimated and true DAGs.

    :param estimated_adj: Estimated adjacency matrix
    :param true_adj: True adjacency matrix
    :return: Dictionary of metrics (FDR, TPR, FPR, etc.)
    """
    hdbg.dassert_isinstance(estimated_adj, np.ndarray)
    hdbg.dassert_isinstance(true_adj, np.ndarray)
    hdbg.dassert_eq(estimated_adj.shape, true_adj.shape)

    metrics_dag = MetricsDAG(estimated_adj, true_adj)
    return {
        "fdr": metrics_dag.metrics["fdr"],
        "tpr": metrics_dag.metrics["tpr"],
        "fpr": metrics_dag.metrics["fpr"],
        "shd": metrics_dag.metrics["shd"],
    }


def compare_algorithms(
    data: np.ndarray,
    true_adj: np.ndarray,
    algorithms: Dict[str, Tuple[Callable, Dict]],
) -> pd.DataFrame:
    """
    Compare multiple causal discovery algorithms.

    :param data: Input data array
    :param true_adj: True adjacency matrix
    :param algorithms: Dict of {name: (algorithm_class, params)}
    :return: DataFrame with performance metrics
    """
    hdbg.dassert_isinstance(data, np.ndarray)
    hdbg.dassert_isinstance(true_adj, np.ndarray)
    hdbg.dassert_isinstance(algorithms, dict)

    results = []
    for name, (algo_class, params) in algorithms.items():
        _LOG.info(f"Running algorithm: {name}")
        estimated_adj = run_causal_algorithm(data, algo_class, **params)
        metrics = compute_dag_metrics(estimated_adj, true_adj)
        metrics["algorithm"] = name
        results.append(metrics)

    return pd.DataFrame(results)


# ###...### / Visualization / ###...###


def plot_dag(
    adj: np.ndarray,
    title: str = "Causal Graph",
    figsize: Tuple[int, int] = (8, 6),
) -> None:
    """
    Visualize a DAG from adjacency matrix.

    :param adj: Adjacency matrix
    :param title: Plot title
    :param figsize: Figure size
    """
    hdbg.dassert_isinstance(adj, np.ndarray)
    hdbg.dassert_eq(adj.ndim, 2)

    dag = nx.DiGraph()
    num_vars = adj.shape[0]
    dag.add_nodes_from(range(num_vars))

    for i in range(num_vars):
        for j in range(num_vars):
            if adj[i, j] != 0:
                dag.add_edge(i, j)

    plt.figure(figsize=figsize)
    pos = nx.spring_layout(dag, seed=42)
    nx.draw_networkx_nodes(dag, pos, node_color="lightblue", node_size=1500)
    nx.draw_networkx_labels(dag, pos, font_size=12, font_weight="bold")
    nx.draw_networkx_edges(dag, pos, edge_color="gray", arrows=True, arrowsize=20)

    plt.title(title, fontsize=14, fontweight="bold")
    plt.axis("off")
    plt.tight_layout()


def plot_comparison_metrics(
    metrics_df: pd.DataFrame,
    metrics_to_plot: List[str] = ["fdr", "tpr", "fpr"],
    figsize: Tuple[int, int] = (12, 4),
) -> None:
    """
    Plot comparison of algorithm metrics.

    :param metrics_df: DataFrame with metrics from compare_algorithms
    :param metrics_to_plot: List of metric names to plot
    :param figsize: Figure size
    """
    hdbg.dassert_isinstance(metrics_df, pd.DataFrame)
    hdbg.dassert_isinstance(metrics_to_plot, list)

    _, axes = plt.subplots(1, len(metrics_to_plot), figsize=figsize)
    if len(metrics_to_plot) == 1:
        axes = [axes]

    for ax, metric in zip(axes, metrics_to_plot):
        metrics_df.plot(x="algorithm", y=metric, kind="bar", ax=ax, legend=False)
        ax.set_title(metric.upper(), fontweight="bold")
        ax.set_xlabel("Algorithm")
        ax.set_ylabel(metric)
        ax.tick_params(axis="x", rotation=45)

    plt.tight_layout()
