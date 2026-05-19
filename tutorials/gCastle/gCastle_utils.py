"""
Utility functions for gCastle causal discovery workflows.

Import as:

import tutorials.gCastle.gCastle_utils as tgcasti
"""

import logging
import typing

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd
# TODO(ai_gp): Use import
from castle.datasets import IIDSimulation, DAG
from castle.estimators import (
    PC,
    GES,
    GOLEM,
    NOTEARS,
    DAG_GNN,
)
from castle.metrics import MetricsDAG

import helpers.hdbg as hdbg

_LOG = logging.getLogger(__name__)


# #############################################################################
# Data Generation
# #############################################################################


def generate_synthetic_data(
    n_nodes: int = 5,
    n_edges: int = 5,
    n_samples: int = 200,
    seed: int = 42,
) -> tuple[pd.DataFrame, nx.DiGraph]:
    """
    Generate synthetic causal data using a random DAG.

    :param n_nodes: Number of nodes in the DAG
    :param n_edges: Number of edges in the DAG
    :param n_samples: Number of samples to generate
    :param seed: Random seed for reproducibility
    :return: Tuple of (data_dataframe, true_dag_networkx_graph)
    """
    np.random.seed(seed)

    # Generate random DAG
    dag_generator = DAG.erdos_renyi(
        n_nodes=n_nodes,
        n_edges=n_edges,
        seed=seed,
    )

    # Generate data from the DAG
    simulator = IIDSimulation(
        W=dag_generator.W,
        noise_scale=1.0,
        seed=seed,
    )
    data = simulator.X

    # Create DataFrame with column names
    columns = [f"X{i}" for i in range(n_nodes)]
    df = pd.DataFrame(data, columns=columns)

    # Create NetworkX graph from adjacency matrix
    true_dag = nx.DiGraph()
    true_dag.add_nodes_from(range(n_nodes))
    for i in range(n_nodes):
        for j in range(n_nodes):
            if dag_generator.W[i, j] != 0:
                true_dag.add_edge(i, j)

    return df, true_dag


# #############################################################################
# Causal Discovery Algorithms
# #############################################################################


def run_pc_algorithm(
    data: np.ndarray,
    alpha: float = 0.05,
) -> np.ndarray:
    """
    Run the PC (Peter-Clark) constraint-based algorithm.

    :param data: Data array of shape (n_samples, n_features)
    :param alpha: Significance level for independence tests
    :return: Estimated adjacency matrix
    """
    model = PC(alpha=alpha)
    model.learn(data)
    return model.causal_matrix


def run_ges_algorithm(
    data: np.ndarray,
) -> np.ndarray:
    """
    Run the GES (Greedy Equivalence Search) score-based algorithm.

    :param data: Data array of shape (n_samples, n_features)
    :return: Estimated adjacency matrix
    """
    model = GES()
    model.learn(data)
    return model.causal_matrix


def run_notears_algorithm(
    data: np.ndarray,
    lambda1: float = 0.0,
    loss_type: str = "l2",
) -> np.ndarray:
    """
    Run the NOTEARS gradient-based algorithm.

    :param data: Data array of shape (n_samples, n_features)
    :param lambda1: L1 regularization parameter
    :param loss_type: Loss function type ('l2' for linear, 'logistic' for nonlinear)
    :return: Estimated adjacency matrix
    """
    model = NOTEARS(
        lambda1=lambda1,
        loss_type=loss_type,
        max_iter=100,
    )
    model.learn(data)
    return model.causal_matrix


def run_golem_algorithm(
    data: np.ndarray,
    lambda1: float = 0.0,
    seed: int = 42,
) -> np.ndarray:
    """
    Run the GOLEM (GO-Lagrangian Expectation-Maximization) algorithm.

    :param data: Data array of shape (n_samples, n_features)
    :param lambda1: L1 regularization parameter
    :param seed: Random seed for reproducibility
    :return: Estimated adjacency matrix
    """
    model = GOLEM(
        lambda1=lambda1,
        seed=seed,
    )
    model.learn(data)
    return model.causal_matrix


def run_dag_gnn_algorithm(
    data: np.ndarray,
    lambda1: float = 0.0,
    seed: int = 42,
) -> np.ndarray:
    """
    Run the DAG-GNN (DAG learning with Graph Neural Networks) algorithm.

    :param data: Data array of shape (n_samples, n_features)
    :param lambda1: L1 regularization parameter
    :param seed: Random seed for reproducibility
    :return: Estimated adjacency matrix
    """
    model = DAG_GNN(
        lambda1=lambda1,
        seed=seed,
    )
    model.learn(data)
    return model.causal_matrix


# #############################################################################
# Evaluation and Metrics
# #############################################################################


def evaluate_causal_discovery(
    true_dag: np.ndarray,
    estimated_dag: np.ndarray,
) -> dict[str, float]:
    """
    Evaluate causal discovery results using standard metrics.

    :param true_dag: True adjacency matrix
    :param estimated_dag: Estimated adjacency matrix
    :return: Dictionary with metrics (F1, SHD, FDR, TPR, NNZ)
    """
    metrics_calculator = MetricsDAG(estimated_dag, true_dag)

    return {
        "F1": metrics_calculator.metrics["F1"],
        "SHD": metrics_calculator.metrics["SHD"],
        "FDR": metrics_calculator.metrics["FDR"],
        "TPR": metrics_calculator.metrics["TPR"],
        "NNZ": metrics_calculator.metrics["NNZ"],
    }


def thresholded_dag(
    adjacency_matrix: np.ndarray,
    threshold: float = 0.3,
) -> np.ndarray:
    """
    Convert weighted adjacency matrix to binary by thresholding.

    :param adjacency_matrix: Weighted adjacency matrix
    :param threshold: Threshold value for binarization
    :return: Binary adjacency matrix
    """
    return (np.abs(adjacency_matrix) > threshold).astype(int)


# #############################################################################
# Visualization
# #############################################################################


def visualize_dag(
    adjacency_matrix: np.ndarray,
    title: str = "Causal DAG",
    node_labels: typing.Optional[list[str]] = None,
    figsize: tuple[int, int] = (10, 8),
) -> plt.Figure:
    """
    Visualize a DAG from an adjacency matrix.

    :param adjacency_matrix: Adjacency matrix of shape (n_nodes, n_nodes)
    :param title: Title for the plot
    :param node_labels: Optional labels for nodes
    :param figsize: Figure size
    :return: Matplotlib figure object
    """
    n_nodes = adjacency_matrix.shape[0]

    # Create NetworkX graph
    graph = nx.DiGraph()
    graph.add_nodes_from(range(n_nodes))

    for i in range(n_nodes):
        for j in range(n_nodes):
            if adjacency_matrix[i, j] != 0:
                graph.add_edge(i, j)

    # Create visualization
    fig, ax = plt.subplots(figsize=figsize)

    # Use hierarchical layout
    pos = nx.spring_layout(graph, k=2, iterations=50, seed=42)

    # Draw
    nx.draw_networkx_nodes(
        graph,
        pos,
        node_color="lightblue",
        node_size=1500,
        ax=ax,
    )
    nx.draw_networkx_edges(
        graph,
        pos,
        arrowsize=20,
        arrowstyle="->",
        edge_color="gray",
        ax=ax,
    )

    # Labels
    if node_labels is None:
        node_labels = {i: f"X{i}" for i in range(n_nodes)}
    nx.draw_networkx_labels(graph, pos, node_labels, ax=ax)

    ax.set_title(title, fontsize=14, fontweight="bold")
    ax.axis("off")

    return fig


def compare_dags(
    true_dag: np.ndarray,
    estimated_dags: dict[str, np.ndarray],
    node_labels: typing.Optional[list[str]] = None,
) -> plt.Figure:
    """
    Visualize multiple estimated DAGs against the true DAG.

    :param true_dag: True adjacency matrix
    :param estimated_dags: Dictionary of {algorithm_name: adjacency_matrix}
    :param node_labels: Optional labels for nodes
    :return: Matplotlib figure with subplots
    """
    n_plots = len(estimated_dags) + 1
    n_cols = min(3, n_plots)
    n_rows = (n_plots + n_cols - 1) // n_cols

    fig, axes = plt.subplots(n_rows, n_cols, figsize=(15, 4 * n_rows))
    axes = axes.flatten()

    # Plot true DAG
    ax = axes[0]
    graph = _create_graph(true_dag)
    pos = nx.spring_layout(graph, k=2, iterations=50, seed=42)
    nx.draw_networkx_nodes(
        graph,
        pos,
        node_color="lightgreen",
        node_size=1500,
        ax=ax,
    )
    nx.draw_networkx_edges(
        graph,
        pos,
        arrowsize=20,
        arrowstyle="->",
        edge_color="gray",
        ax=ax,
    )
    nx.draw_networkx_labels(graph, pos, ax=ax)
    ax.set_title("True DAG", fontsize=12, fontweight="bold")
    ax.axis("off")

    # Plot estimated DAGs
    for idx, (algorithm_name, est_dag) in enumerate(estimated_dags.items()):
        ax = axes[idx + 1]
        graph = _create_graph(est_dag)
        nx.draw_networkx_nodes(
            graph,
            pos,
            node_color="lightblue",
            node_size=1500,
            ax=ax,
        )
        nx.draw_networkx_edges(
            graph,
            pos,
            arrowsize=20,
            arrowstyle="->",
            edge_color="gray",
            ax=ax,
        )
        nx.draw_networkx_labels(graph, pos, ax=ax)
        ax.set_title(f"Estimated ({algorithm_name})", fontsize=12, fontweight="bold")
        ax.axis("off")

    # Hide unused subplots
    for idx in range(n_plots, len(axes)):
        axes[idx].axis("off")

    plt.tight_layout()
    return fig


def _create_graph(adjacency_matrix: np.ndarray) -> nx.DiGraph:
    """Helper to create NetworkX graph from adjacency matrix."""
    n_nodes = adjacency_matrix.shape[0]
    graph = nx.DiGraph()
    graph.add_nodes_from(range(n_nodes))

    for i in range(n_nodes):
        for j in range(n_nodes):
            if adjacency_matrix[i, j] != 0:
                graph.add_edge(i, j)

    return graph
