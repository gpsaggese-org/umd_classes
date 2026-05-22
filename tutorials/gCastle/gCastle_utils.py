"""
Utility functions for gCastle causal discovery workflows.

Import as:

import tutorials.gCastle.gCastle_utils as tgcgcuti
"""

from typing import Any, Dict, Optional, Tuple

import castle.algorithms
import castle.datasets
import castle.metrics
import ipywidgets
import matplotlib.pyplot as plt
import matplotlib.figure
import networkx as nx
import numpy as np
import pandas as pd
from IPython.display import clear_output, display

import helpers.htutorial as htutori


# #############################################################################
# Cell 1: Data Generation
# #############################################################################


def generate_synthetic_data(
    *,
    n_nodes: int = 5,
    n_edges: Optional[int] = None,
    noise_scale: float = 1.0,
    n_samples: int = 200,
    seed: int = 42,
) -> Tuple[pd.DataFrame, np.ndarray]:
    """
    Generate synthetic causal data using a random DAG.

    :param n_nodes: Number of nodes in the DAG
    :param n_edges: Number of edges in the DAG (defaults to n_nodes if not specified)
    :param n_samples: Number of samples to generate
    :param noise_scale: Standard deviation of Gaussian noise
    :param seed: Random seed for reproducibility
    :return: Tuple of (data_dataframe, true_dag_adjacency_matrix)
    """
    if n_edges is None:
        n_edges = n_nodes
    np.random.seed(seed)
    w_matrix = castle.datasets.DAG.erdos_renyi(
        n_nodes=n_nodes,
        n_edges=n_edges,
        seed=seed,
    )
    # Generate data from the DAG.
    # X = linear combination of parents + Gaussian noise
    simulator = castle.datasets.IIDSimulation(
        w_matrix,
        n=n_samples,
        method="linear",
        sem_type="gauss",
        noise_scale=noise_scale,
    )
    data = simulator.X
    # Create DataFrame with column names.
    columns = [f"X{i}" for i in range(n_nodes)]
    df = pd.DataFrame(data, columns=columns)
    return df, w_matrix


def _get_graph_style_config() -> Dict[str, Any]:
    """
    Get consistent styling configuration for graph visualizations.

    :return: Dictionary with graph styling parameters
    """
    return {
        "node_color": "lightblue",
        "node_color_true": "lightgreen",
        "node_size": 800,
        "edge_color": "darkgray",
        "arrow_size": 20,
        "arrow_style": "->",
    }


def _create_graph(adjacency_matrix: np.ndarray) -> nx.DiGraph:
    """
    Helper to create NetworkX graph from adjacency matrix.
    """
    n_nodes = adjacency_matrix.shape[0]
    graph = nx.DiGraph()
    graph.add_nodes_from(range(n_nodes))
    for i in range(n_nodes):
        for j in range(n_nodes):
            if adjacency_matrix[i, j] != 0:
                graph.add_edge(i, j)
    return graph


def cell1_data_generation_interactive() -> Tuple[pd.DataFrame, np.ndarray]:
    """
    Interactive data generation with adjustable parameters.

    Shows four horizontally-aligned panels:
    1. True adjacency matrix heatmap
    2. True causal DAG visualization
    3. Data correlation matrix heatmap
    4. Data DataFrame sample

    Returns the generated data and DAG for use in subsequent cells.

    :return: Tuple of (data_dataframe, true_dag_adjacency_matrix)
    """
    n_nodes_slider, n_nodes_box = htutori.build_widget_control(
        name="n_nodes",
        description="number of nodes in the DAG",
        min_val=3,
        max_val=10,
        step=1,
        initial_value=5,
        is_float=False,
    )
    n_samples_slider, n_samples_box = htutori.build_widget_control(
        name="n_samples",
        description="number of data samples",
        min_val=100,
        max_val=1000,
        step=100,
        initial_value=500,
        is_float=False,
    )
    noise_scale_slider, noise_scale_box = htutori.build_widget_control(
        name="noise_scale",
        description="standard deviation of Gaussian noise",
        min_val=0.1,
        max_val=2.0,
        step=0.1,
        initial_value=1.0,
        is_float=True,
    )
    seed_slider, seed_box = htutori.build_widget_control(
        name="seed",
        description="random seed for reproducibility",
        min_val=1,
        max_val=100,
        step=1,
        initial_value=43,
        is_float=False,
    )
    output = ipywidgets.Output()
    data_output = ipywidgets.Output()

    def update_plot(_change: dict | None = None) -> None:
        """
        Update the data generation visualization.

        :param _change: Dictionary with change information (unused)
        """
        with output:
            clear_output(wait=True)
            n_nodes = int(n_nodes_slider.value)
            n_samples = int(n_samples_slider.value)
            noise_scale = noise_scale_slider.value
            seed = int(seed_slider.value)
            data, true_dag = generate_synthetic_data(
                n_nodes=n_nodes,
                n_samples=n_samples,
                noise_scale=noise_scale,
                seed=seed,
            )
            n_nodes = true_dag.shape[0]
            style_config = _get_graph_style_config()
            _fig, (ax1, ax2, ax3, ax4) = plt.subplots(1, 4, figsize=(20, 5))
            im1 = ax1.imshow(
                true_dag,
                cmap="YlOrRd",
                aspect="equal",
                vmin=0,
                vmax=1,
            )
            ax1.set_xlabel("Target Node", fontsize=12)
            ax1.set_ylabel("Source Node", fontsize=12)
            ax1.set_title(
                "True Adjacency Matrix", fontsize=14, fontweight="bold"
            )
            ax1.set_xticks(range(n_nodes))
            ax1.set_yticks(range(n_nodes))
            ax1.set_xticklabels([f"X{i}" for i in range(n_nodes)])
            ax1.set_yticklabels([f"X{i}" for i in range(n_nodes)])
            plt.colorbar(im1, ax=ax1, label="Edge")
            graph_true = _create_graph(true_dag)
            pos = nx.spring_layout(graph_true, k=2, iterations=50, seed=seed)
            nx.draw_networkx_nodes(
                graph_true,
                pos,
                node_color=style_config["node_color_true"],
                node_size=style_config["node_size"],
                ax=ax2,
            )
            nx.draw_networkx_edges(
                graph_true,
                pos,
                arrowsize=style_config["arrow_size"],
                arrowstyle=style_config["arrow_style"],
                edge_color=style_config["edge_color"],
                ax=ax2,
            )
            node_labels = {i: f"X{i}" for i in range(n_nodes)}
            nx.draw_networkx_labels(
                graph_true, pos, node_labels, ax=ax2, font_size=10
            )
            ax2.set_title("True Causal DAG", fontsize=14, fontweight="bold")
            ax2.axis("off")
            corr_matrix = data.corr().values
            im3 = ax3.imshow(
                corr_matrix,
                cmap="coolwarm",
                aspect="equal",
                vmin=-1,
                vmax=1,
            )
            ax3.set_xlabel("Variable", fontsize=12)
            ax3.set_ylabel("Variable", fontsize=12)
            ax3.set_title(
                "Data Correlation Matrix", fontsize=14, fontweight="bold"
            )
            ax3.set_xticks(range(n_nodes))
            ax3.set_yticks(range(n_nodes))
            ax3.set_xticklabels([f"X{i}" for i in range(n_nodes)])
            ax3.set_yticklabels([f"X{i}" for i in range(n_nodes)])
            plt.colorbar(im3, ax=ax3, label="Correlation")
            ax4.axis("off")
            ax4.set_title("Data Summary", fontsize=14, fontweight="bold")
            summary_text = (
                f"Parameters:\n\n"
                f"N Nodes:     {n_nodes}\n"
                f"N Samples:   {n_samples}\n"
                f"Noise Scale: {noise_scale:.2f}\n"
                f"Seed:        {seed}\n\n"
                f"Generated Data Shape: {data.shape}\n"
                f"True Edges:  {int(np.sum(true_dag))}\n"
            )
            ax4.text(
                0.5,
                0.5,
                summary_text,
                horizontalalignment="center",
                verticalalignment="center",
                fontsize=12,
                family="monospace",
                bbox=dict(boxstyle="round", facecolor="lightgray", alpha=0.8),
            )
            plt.tight_layout()
            plt.show()
            with data_output:
                clear_output(wait=True)
                print("\nFirst 5 rows of generated data:")
                print(data.head())

    n_nodes_slider.observe(update_plot, names="value")
    n_samples_slider.observe(update_plot, names="value")
    noise_scale_slider.observe(update_plot, names="value")
    seed_slider.observe(update_plot, names="value")
    update_plot()
    display(
        ipywidgets.VBox(
            [
                ipywidgets.Label("Cell 1: Interactive Data Generation"),
                ipywidgets.Label(
                    "Adjust parameters to generate synthetic causal data:"
                ),
                n_nodes_box,
                n_samples_box,
                noise_scale_box,
                seed_box,
                output,
                data_output,
            ]
        )
    )
    n_nodes = int(n_nodes_slider.value)
    n_samples = int(n_samples_slider.value)
    noise_scale = noise_scale_slider.value
    seed = int(seed_slider.value)
    return generate_synthetic_data(
        n_nodes=n_nodes,
        n_samples=n_samples,
        noise_scale=noise_scale,
        seed=seed,
    )


# #############################################################################
# Evaluation and Metrics
# #############################################################################


def evaluate_causal_discovery(
    true_dag: np.ndarray,
    estimated_dag: np.ndarray,
) -> Dict[str, float]:
    """
    Evaluate causal discovery results using standard metrics.

    :param true_dag: True adjacency matrix
    :param estimated_dag: Estimated adjacency matrix
    :return: Dictionary with metrics (F1, SHD, FDR, TPR, NNZ)
    """
    metrics_calculator = castle.metrics.MetricsDAG(estimated_dag, true_dag)
    return {
        "F1": metrics_calculator.metrics["F1"],
        "SHD": metrics_calculator.metrics["shd"],
        "FDR": metrics_calculator.metrics["fdr"],
        "TPR": metrics_calculator.metrics["tpr"],
        "NNZ": metrics_calculator.metrics["nnz"],
    }


def thresholded_dag(
    adjacency_matrix: np.ndarray,
    *,
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
    *,
    title: str = "Causal DAG",
    figsize: Optional[Tuple[int, int]] = None,
) -> matplotlib.figure.Figure:
    """
    Visualize a DAG from an adjacency matrix.

    :param adjacency_matrix: Adjacency matrix of shape (n_nodes, n_nodes)
    :param title: Title for the plot
    :param figsize: Figure size
    :return: Matplotlib figure object
    """
    if figsize is None:
        figsize = plt.rcParams["figure.figsize"]
    n_nodes = adjacency_matrix.shape[0]
    # Create NetworkX graph.
    graph = nx.DiGraph()
    graph.add_nodes_from(range(n_nodes))
    for i in range(n_nodes):
        for j in range(n_nodes):
            if adjacency_matrix[i, j] != 0:
                graph.add_edge(i, j)
    # Create visualization.
    fig, ax = plt.subplots(figsize=figsize)
    # Use hierarchical layout.
    pos = nx.spring_layout(graph, k=2, iterations=50, seed=42)
    # Draw nodes.
    nx.draw_networkx_nodes(
        graph,
        pos,
        node_color="lightblue",
        node_size=500,
        ax=ax,
    )
    # Draw edges.
    nx.draw_networkx_edges(
        graph,
        pos,
        arrowsize=25,
        arrowstyle="-|>",
        edge_color="darkgray",
        ax=ax,
    )
    # Draw labels.
    node_labels = {i: f"X{i}" for i in range(n_nodes)}
    nx.draw_networkx_labels(graph, pos, node_labels, ax=ax)
    ax.set_title(title, fontsize=14, fontweight="bold")
    ax.axis("off")
    return fig


def compare_dags(
    true_dag: np.ndarray,
    estimated_dags: Dict[str, np.ndarray],
) -> matplotlib.figure.Figure:
    """
    Visualize multiple estimated DAGs against the true DAG.

    :param true_dag: True adjacency matrix
    :param estimated_dags: Dictionary of {algorithm_name: adjacency_matrix}
    :return: Matplotlib figure with subplots
    """
    n_plots = len(estimated_dags) + 1
    n_cols = min(3, n_plots)
    n_rows = (n_plots + n_cols - 1) // n_cols
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(15, 4 * n_rows))
    axes = axes.flatten()
    # Plot true DAG.
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
        arrowsize=35,
        arrowstyle="->",
        edge_color="darkgray",
        ax=ax,
    )
    nx.draw_networkx_labels(graph, pos, ax=ax)
    ax.set_title("True DAG", fontsize=12, fontweight="bold")
    ax.axis("off")
    # Plot estimated DAGs.
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
            arrowsize=35,
            arrowstyle="->",
            edge_color="darkgray",
            ax=ax,
        )
        nx.draw_networkx_labels(graph, pos, ax=ax)
        ax.set_title(
            f"Estimated ({algorithm_name})", fontsize=12, fontweight="bold"
        )
        ax.axis("off")
    # Hide unused subplots.
    for idx in range(n_plots, len(axes)):
        axes[idx].axis("off")
    plt.tight_layout()
    return fig


# #############################################################################
# Cell 2, 3, 4: Causal Discovery Algorithms
# #############################################################################


def run_pc_algorithm(
    data: np.ndarray,
    *,
    alpha: float = 0.05,
) -> np.ndarray:
    """
    Run the PC (Peter-Clark) constraint-based algorithm.

    :param data: Data array of shape (n_samples, n_features)
    :param alpha: Significance level for independence tests
    :return: Estimated adjacency matrix
    """
    model = castle.algorithms.PC(alpha=alpha)
    model.learn(data)
    return model.causal_matrix


def run_ges_algorithm(data: np.ndarray) -> np.ndarray:
    """
    Run the GES (Greedy Equivalence Search) score-based algorithm.

    :param data: Data array of shape (n_samples, n_features)
    :return: Estimated adjacency matrix
    """
    model = castle.algorithms.GES()
    model.learn(data)
    return model.causal_matrix


def run_notears_algorithm(
    data: np.ndarray,
    *,
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
    model = castle.algorithms.Notears(
        lambda1=lambda1,
        loss_type=loss_type,
        max_iter=100,
    )
    model.learn(data)
    return model.causal_matrix


def run_golem_algorithm(
    data: np.ndarray,
    *,
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
    model = castle.algorithms.GOLEM(
        lambda1=lambda1,
        seed=seed,
    )
    model.learn(data)
    return model.causal_matrix


def run_dag_gnn_algorithm(
    data: np.ndarray,
    *,
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
    model = castle.algorithms.DAG_GNN(
        lambda1=lambda1,
        seed=seed,
    )
    model.learn(data)
    return model.causal_matrix


def _plot_five_panel_layout(
    true_dag: np.ndarray,
    estimated_dag: np.ndarray,
    metrics: Dict[str, float],
    param_name: str = "",
    param_value: float = 0.0,
) -> None:
    """
    Plot five-panel layout with true and estimated adjacency matrices and DAGs.

    :param true_dag: True adjacency matrix
    :param estimated_dag: Estimated adjacency matrix
    :param metrics: Dictionary of performance metrics
    :param param_name: Name of the parameter being varied (for display)
    :param param_value: Value of the parameter being varied
    """
    n_nodes = true_dag.shape[0]
    style_config = _get_graph_style_config()
    _fig, (ax1, ax2, ax3, ax4, ax5) = plt.subplots(1, 5, figsize=(25, 5))
    im1 = ax1.imshow(
        true_dag,
        cmap="YlOrRd",
        aspect="equal",
        vmin=0,
        vmax=1,
    )
    ax1.set_xlabel("Target Node", fontsize=12)
    ax1.set_ylabel("Source Node", fontsize=12)
    ax1.set_title("True Adjacency Matrix", fontsize=14, fontweight="bold")
    ax1.set_xticks(range(n_nodes))
    ax1.set_yticks(range(n_nodes))
    ax1.set_xticklabels([f"X{i}" for i in range(n_nodes)])
    ax1.set_yticklabels([f"X{i}" for i in range(n_nodes)])
    plt.colorbar(im1, ax=ax1, label="Edge")
    graph_true = _create_graph(true_dag)
    pos = nx.spring_layout(graph_true, k=2, iterations=50, seed=42)
    nx.draw_networkx_nodes(
        graph_true,
        pos,
        node_color=style_config["node_color_true"],
        node_size=style_config["node_size"],
        ax=ax2,
    )
    nx.draw_networkx_edges(
        graph_true,
        pos,
        arrowsize=style_config["arrow_size"],
        arrowstyle=style_config["arrow_style"],
        edge_color=style_config["edge_color"],
        ax=ax2,
    )
    node_labels = {i: f"X{i}" for i in range(n_nodes)}
    nx.draw_networkx_labels(graph_true, pos, node_labels, ax=ax2, font_size=10)
    ax2.set_title("True Causal DAG", fontsize=14, fontweight="bold")
    ax2.axis("off")
    im3 = ax3.imshow(
        estimated_dag,
        cmap="YlOrRd",
        aspect="equal",
        vmin=0,
        vmax=1,
    )
    ax3.set_xlabel("Target Node", fontsize=12)
    ax3.set_ylabel("Source Node", fontsize=12)
    ax3.set_title("Estimated Adjacency Matrix", fontsize=14, fontweight="bold")
    ax3.set_xticks(range(n_nodes))
    ax3.set_yticks(range(n_nodes))
    ax3.set_xticklabels([f"X{i}" for i in range(n_nodes)])
    ax3.set_yticklabels([f"X{i}" for i in range(n_nodes)])
    plt.colorbar(im3, ax=ax3, label="Edge")
    graph_est = _create_graph(estimated_dag)
    nx.draw_networkx_nodes(
        graph_est,
        pos,
        node_color=style_config["node_color"],
        node_size=style_config["node_size"],
        ax=ax4,
    )
    nx.draw_networkx_edges(
        graph_est,
        pos,
        arrowsize=style_config["arrow_size"],
        arrowstyle=style_config["arrow_style"],
        edge_color=style_config["edge_color"],
        ax=ax4,
    )
    nx.draw_networkx_labels(graph_est, pos, node_labels, ax=ax4, font_size=10)
    ax4.set_title("Estimated Causal DAG", fontsize=14, fontweight="bold")
    ax4.axis("off")
    ax5.axis("off")
    metrics_text = (
        f"Performance Metrics:\n\n"
        f"F1 Score:  {metrics['F1']:.4f}\n"
        f"SHD:       {metrics['SHD']:.1f}\n"
        f"FDR:       {metrics['FDR']:.4f}\n"
        f"TPR:       {metrics['TPR']:.4f}\n"
        f"Edges:     {int(metrics['NNZ'])}\n\n"
        f"True Edges: {int(np.sum(true_dag))}\n"
    )
    if param_name:
        metrics_text += f"{param_name}: {param_value:.3f}"
    ax5.text(
        0.5,
        0.5,
        metrics_text,
        horizontalalignment="center",
        verticalalignment="center",
        fontsize=12,
        family="monospace",
        bbox=dict(boxstyle="round", facecolor="lightgray", alpha=0.8),
    )
    ax5.set_title("Metrics", fontsize=14, fontweight="bold")
    plt.tight_layout()
    plt.show()


def cell2_pc_algorithm_interactive(
    data: np.ndarray,
    true_dag: np.ndarray,
) -> None:
    """
    Interactive visualization of PC algorithm with reactive alpha parameter.

    Shows five horizontally-aligned panels:
    1. True adjacency matrix heatmap
    2. True causal DAG visualization
    3. Estimated adjacency matrix heatmap
    4. Estimated causal DAG visualization
    5. Performance metrics

    All panels update reactively when the alpha slider changes.

    :param data: Data array of shape (n_samples, n_features)
    :param true_dag: True adjacency matrix
    """
    alpha_slider, alpha_box = htutori.build_widget_control(
        name="alpha",
        description="significance level for independence tests",
        min_val=0.01,
        max_val=0.20,
        step=0.01,
        initial_value=0.05,
        is_float=True,
    )
    output = ipywidgets.Output()

    def update_plot(_change: dict | None = None) -> None:
        """
        Update the five-panel visualization when alpha changes.

        :param _change: Dictionary with change information (unused)
        """
        with output:
            clear_output(wait=True)
            alpha = alpha_slider.value
            pc_adjacency = run_pc_algorithm(data, alpha=alpha)
            pc_metrics = evaluate_causal_discovery(true_dag, pc_adjacency)
            _plot_five_panel_layout(
                true_dag,
                pc_adjacency,
                pc_metrics,
                param_name="Alpha",
                param_value=alpha,
            )

    alpha_slider.observe(update_plot, names="value")
    update_plot()
    display(
        ipywidgets.VBox(
            [
                ipywidgets.Label(
                    "PC Algorithm: Constraint-Based Causal Discovery"
                ),
                ipywidgets.Label(
                    "Adjust alpha to control sensitivity of independence tests:"
                ),
                alpha_box,
                output,
            ]
        )
    )


def cell3_ges_algorithm_interactive(
    data: np.ndarray,
    true_dag: np.ndarray,
) -> None:
    """
    Visualization of GES algorithm with five-panel layout.

    Shows five horizontally-aligned panels:
    1. True adjacency matrix heatmap
    2. True causal DAG visualization
    3. Estimated adjacency matrix heatmap
    4. Estimated causal DAG visualization
    5. Performance metrics

    :param data: Data array of shape (n_samples, n_features)
    :param true_dag: True adjacency matrix
    """
    ges_adjacency = run_ges_algorithm(data)
    ges_metrics = evaluate_causal_discovery(true_dag, ges_adjacency)
    display(ipywidgets.Label("GES Algorithm: Score-Based Causal Discovery"))
    _plot_five_panel_layout(true_dag, ges_adjacency, ges_metrics)


def cell4_notears_algorithm_interactive(
    data: np.ndarray,
    true_dag: np.ndarray,
) -> None:
    """
    Interactive visualization of NOTEARS algorithm with reactive lambda1 parameter.

    Shows five horizontally-aligned panels:
    1. True adjacency matrix heatmap
    2. True causal DAG visualization
    3. Estimated adjacency matrix heatmap
    4. Estimated causal DAG visualization
    5. Performance metrics

    All panels update reactively when the lambda1 slider changes.

    :param data: Data array of shape (n_samples, n_features)
    :param true_dag: True adjacency matrix
    """
    lambda1_slider, lambda1_box = htutori.build_widget_control(
        name="lambda1",
        description="L1 regularization parameter",
        min_val=0.0,
        max_val=0.5,
        step=0.05,
        initial_value=0.0,
        is_float=True,
    )
    output = ipywidgets.Output()

    def update_plot(_change: dict | None = None) -> None:
        """
        Update the five-panel visualization when lambda1 changes.

        :param _change: Dictionary with change information (unused)
        """
        with output:
            clear_output(wait=True)
            lambda1 = lambda1_slider.value
            notears_adjacency = run_notears_algorithm(
                data,
                lambda1=lambda1,
                loss_type="l2",
            )
            notears_metrics = evaluate_causal_discovery(
                true_dag, notears_adjacency
            )
            _plot_five_panel_layout(
                true_dag,
                notears_adjacency,
                notears_metrics,
                param_name="Lambda1",
                param_value=lambda1,
            )

    lambda1_slider.observe(update_plot, names="value")
    update_plot()
    display(
        ipywidgets.VBox(
            [
                ipywidgets.Label(
                    "NOTEARS Algorithm: Gradient-Based Causal Discovery"
                ),
                ipywidgets.Label("Adjust lambda1 to control L1 regularization:"),
                lambda1_box,
                output,
            ]
        )
    )
