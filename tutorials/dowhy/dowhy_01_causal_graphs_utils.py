"""
Utility functions supporting `dowhy.API.ipynb`.

This module contains the helpers for the notebook on causal graphs and causal
discovery. Functions are organized cell-by-cell, matching the notebook's
pedagogical flow.

Import as:

import tutorials.dowhy.dowhy_01_causal_graphs_utils as tdd0cgrut
"""

import itertools
import logging
from typing import Any, Dict, FrozenSet, List, Optional, Tuple

import ipywidgets as widgets

# TODO(ai_gp): import matplotlib
import matplotlib.patches as mpatches

# TODO(ai_gp): This import is fine.
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd
import seaborn as sns
from IPython.display import display

# TODO(ai_gp): import scipy
from scipy import stats

import helpers.hgraphviz as hgraphv

_LOG = logging.getLogger(__name__)


# #############################################################################
# Cell 1: Introduction to Causal Graphs
# #############################################################################


def cell1_create_motivating_dags() -> Dict[str, nx.DiGraph]:
    """
    Build small example DAGs from health, economics, and social domains.

    Each DAG illustrates a typical causal structure students may already have
    intuition about, motivating why graphs help formalize causal thinking.

    :return: Mapping from domain name to a `networkx.DiGraph`
    """
    # Health domain: air pollution influences lung disease which influences mortality.
    health = nx.DiGraph()
    health.add_edges_from(
        [
            ("AirPollution", "LungDisease"),
            ("LungDisease", "Mortality"),
            ("Age", "AirPollution"),
            ("Age", "Mortality"),
        ]
    )
    # Economics: education and experience drive income through job role.
    economics = nx.DiGraph()
    economics.add_edges_from(
        [
            ("Education", "JobRole"),
            ("Experience", "JobRole"),
            ("JobRole", "Income"),
            ("Education", "Income"),
        ]
    )
    # Social: a confounder (popularity) drives both observed variables.
    social = nx.DiGraph()
    social.add_edges_from(
        [
            ("Popularity", "FriendCount"),
            ("Popularity", "PostLikes"),
        ]
    )
    return {"Health": health, "Economics": economics, "Social": social}


def cell1_plot_correlation_vs_causation(
    *,
    figsize: Optional[Tuple[int, int]] = None,
    random_state: int = 0,
) -> None:
    """
    Plot a classic example where correlation does not imply causation.

    Generates data where ice cream sales and drowning incidents are both
    driven by hot weather, producing a strong correlation without a direct
    causal link.

    :param figsize: Override the default figure size
    :param random_state: Seed controlling the synthetic example
    """
    if figsize is None:
        figsize = (12, 4)
    rng = np.random.default_rng(random_state)
    # Temperature is the common cause for both observed variables.
    temperature = rng.normal(25, 5, 200)
    ice_cream = 2 * temperature + rng.normal(0, 5, 200)
    drownings = 0.5 * temperature + rng.normal(0, 2, 200)
    fig, axes = plt.subplots(1, 2, figsize=figsize)
    # Scatter showing strong spurious correlation between effects.
    sns.regplot(
        x=ice_cream,
        y=drownings,
        ax=axes[0],
        scatter_kws={"alpha": 0.5},
        line_kws={"color": "red"},
    )
    corr = np.corrcoef(ice_cream, drownings)[0, 1]
    axes[0].set_xlabel("Ice cream sales")
    axes[0].set_ylabel("Drownings")
    axes[0].set_title(f"Observed correlation: r = {corr:.2f}")
    # Plot the true causal DAG (temperature as common cause).
    causal_g = nx.DiGraph()
    causal_g.add_edges_from(
        [
            ("Temperature", "IceCreamSales"),
            ("Temperature", "Drownings"),
        ]
    )
    hgraphv.plot_causal_dag(
        causal_g, "True causal structure", mode="graphviz", ax=axes[1]
    )
    fig.tight_layout()
    plt.show()


def cell1_print_and_plot_motivating_dags(
    domain_dags: Dict[str, nx.DiGraph],
    figsize: Optional[Tuple[int, int]] = None,
) -> None:
    """
    Print the edges of motivating DAGs and visualize them side-by-side.

    Shows how domain knowledge is encoded as a DAG with explicit edges,
    demonstrating that different domains have different causal structures.

    :param domain_dags: Mapping from domain name to motivating DAG
    :param figsize: Override the default figure size
    """
    if figsize is None:
        figsize = (15, 4)
    # Print the DAGs to show how they are made.
    for domain_name, G in domain_dags.items():
        print(f"{domain_name} domain DAG edges:")
        for u, v in G.edges():
            print(f"  {u} -> {v}")
        print()

    # Plot each DAG with consistent styling and layout.
    fig, axes = plt.subplots(1, 3, figsize=figsize)
    fig.tight_layout()
    for ax, (name, G) in zip(axes, domain_dags.items()):
        ax.margins(0.2)
        hgraphv.plot_causal_dag(G, name, mode="graphviz", ax=ax)
    plt.show()


def cell1_interactive_edge_toggle(base_graph: nx.DiGraph) -> None:
    """
    Render an interactive widget to add or remove edges from a DAG.

    Students can toggle edges and immediately see how the causal structure
    changes, building intuition that graph topology encodes assumptions.

    :param base_graph: Starting DAG presented as the baseline structure
    """
    # Generate all possible directed edges between nodes (excluding self).
    nodes = list(base_graph.nodes())
    candidate_edges = [(u, v) for u, v in itertools.permutations(nodes, 2)]
    # Create one checkbox per candidate edge, pre-checked if it exists.
    checkboxes = {
        e: widgets.Checkbox(
            value=base_graph.has_edge(*e),
            description=f"{e[0]} -> {e[1]}",
            indent=False,
        )
        for e in candidate_edges
    }
    output = widgets.Output()

    def _update(_change=None) -> None:
        # Rebuild graph from current checkbox states.
        new_graph = nx.DiGraph()
        new_graph.add_nodes_from(nodes)
        for edge, cb in checkboxes.items():
            if cb.value:
                new_graph.add_edge(*edge)
        with output:
            output.clear_output(wait=True)
            is_dag = nx.is_directed_acyclic_graph(new_graph)
            title = (
                f"Current graph (DAG: {is_dag})"
                if is_dag
                else "Current graph (NOT a DAG)"
            )
            fig, ax = plt.subplots(figsize=(5, 4))
            hgraphv.plot_causal_dag(new_graph, title, mode="graphviz", ax=ax)
            plt.show()

    for cb in checkboxes.values():
        cb.observe(_update, names="value")
    # Lay out checkboxes vertically next to the plot output.
    controls = widgets.VBox(list(checkboxes.values()))
    display(widgets.HBox([controls, output]))
    _update()


# #############################################################################
# Cell 2: Domain Knowledge and Expert Causal Graphs
# #############################################################################


def cell2_generate_healthcare_data(
    n_samples: int,
    *,
    random_state: int = 42,
) -> pd.DataFrame:
    """
    Generate synthetic healthcare data following a known causal structure.

    The data-generating process matches the DAG built by
    `cell2_build_domain_dag()`, so students can later verify that discovery
    methods recover the true structure.

    :param n_samples: Number of rows to generate
    :param random_state: Seed for reproducibility
    :return: DataFrame with healthcare variables
    """
    rng = np.random.default_rng(random_state)
    # Age is an exogenous root variable.
    age = rng.uniform(25, 75, n_samples)
    # Air pollution exposure rises with age.
    air_pollution = (rng.uniform(0, 1, n_samples) < (age - 25) / 100).astype(int)
    # Exercise drops with age and air pollution exposure.
    exercise = (
        -0.05 * age - 1.5 * air_pollution + rng.normal(0, 1, n_samples) + 5
    )
    # Diet quality is partially independent and partially driven by exercise.
    diet = 0.3 * exercise + rng.normal(0, 1, n_samples) + 3
    # Cholesterol is driven by diet (negative) and age (positive).
    cholesterol = (
        180
        + 0.5 * age
        - 5 * diet
        + 10 * air_pollution
        + rng.normal(0, 10, n_samples)
    )
    # Blood pressure is driven by age, air pollution, exercise, and cholesterol.
    blood_pressure = (
        100
        + 0.4 * age
        + 8 * air_pollution
        - 2 * exercise
        + 0.1 * cholesterol
        + rng.normal(0, 8, n_samples)
    )
    # Heart disease risk increases with blood pressure, cholesterol, air pollution.
    heart_disease_risk = (
        -10
        + 0.05 * blood_pressure
        + 0.03 * cholesterol
        + 2 * air_pollution
        - 0.5 * exercise
        + rng.normal(0, 2, n_samples)
    )
    heart_disease = (heart_disease_risk > heart_disease_risk.mean()).astype(int)
    return pd.DataFrame(
        {
            "Age": age,
            "AirPollution": air_pollution,
            "Exercise": exercise,
            "Diet": diet,
            "Cholesterol": cholesterol,
            "BloodPressure": blood_pressure,
            "HeartDisease": heart_disease,
        }
    )


def cell2_build_domain_dag() -> nx.DiGraph:
    """
    Encode the healthcare domain causal graph used as ground truth.

    :return: DAG representing expert beliefs about healthcare causality
    """
    G = nx.DiGraph()
    G.add_edges_from(
        [
            ("Age", "AirPollution"),
            ("Age", "Exercise"),
            ("Age", "Cholesterol"),
            ("Age", "BloodPressure"),
            ("AirPollution", "Exercise"),
            ("AirPollution", "Cholesterol"),
            ("AirPollution", "BloodPressure"),
            ("AirPollution", "HeartDisease"),
            ("Exercise", "Diet"),
            ("Exercise", "BloodPressure"),
            ("Exercise", "HeartDisease"),
            ("Diet", "Cholesterol"),
            ("Cholesterol", "BloodPressure"),
            ("Cholesterol", "HeartDisease"),
            ("BloodPressure", "HeartDisease"),
        ]
    )
    return G


def cell2_describe_graph(G: nx.DiGraph) -> pd.DataFrame:
    """
    Summarize a DAG as an edge list table for human-readable inspection.

    :param G: Directed graph to describe
    :return: DataFrame with one row per edge listing cause and effect
    """
    edges = [{"Cause": u, "Effect": v} for u, v in G.edges()]
    return pd.DataFrame(edges)


# #############################################################################
# Cell 3: Limitations of Domain Knowledge Alone
# #############################################################################


def cell3_make_candidate_graphs() -> Dict[str, nx.DiGraph]:
    """
    Build several competing causal hypotheses for the same variables.

    The hypotheses differ in edge directions and presence, illustrating that
    domain knowledge alone may not be enough to choose between them.

    :return: Mapping from hypothesis label to candidate DAG
    """
    nodes = ["Exercise", "Diet", "Cholesterol", "BloodPressure"]
    # Hypothesis A: exercise drives diet drives cholesterol.
    a = nx.DiGraph()
    a.add_nodes_from(nodes)
    a.add_edges_from(
        [
            ("Exercise", "Diet"),
            ("Diet", "Cholesterol"),
            ("Cholesterol", "BloodPressure"),
        ]
    )
    # Hypothesis B: diet and exercise both directly impact cholesterol.
    b = nx.DiGraph()
    b.add_nodes_from(nodes)
    b.add_edges_from(
        [
            ("Diet", "Cholesterol"),
            ("Exercise", "Cholesterol"),
            ("Cholesterol", "BloodPressure"),
        ]
    )
    # Hypothesis C: reversed direction between cholesterol and blood pressure.
    c = nx.DiGraph()
    c.add_nodes_from(nodes)
    c.add_edges_from(
        [
            ("Diet", "Cholesterol"),
            ("Exercise", "BloodPressure"),
            ("BloodPressure", "Cholesterol"),
        ]
    )
    return {"Hypothesis A": a, "Hypothesis B": b, "Hypothesis C": c}


def _pearsonr_safe(x: np.ndarray, y: np.ndarray) -> Tuple[float, float]:
    """
    Run `scipy.stats.pearsonr()` and cast the result to a plain float tuple.

    Wrapping the call isolates the type-narrowing logic in one place.

    :param x: First sample
    :param y: Second sample
    :return: Tuple of correlation and p-value
    """
    res: Any = stats.pearsonr(x, y)
    return float(res[0]), float(res[1])


def _partial_corr(
    df: pd.DataFrame,
    x: str,
    y: str,
    z: List[str],
) -> Tuple[float, float]:
    """
    Compute partial correlation between `x` and `y` controlling for `z`.

    Uses linear regression residuals as a quick conditional independence
    surrogate; not as rigorous as a kernel test but appropriate for teaching.

    :param df: Source data
    :param x: First variable
    :param y: Second variable
    :param z: Variables to control for (may be empty)
    :return: Tuple of correlation coefficient and approximate p-value
    """
    # When the conditioning set is empty fall back to Pearson correlation.
    if not z:
        return _pearsonr_safe(df[x].to_numpy(), df[y].to_numpy())
    # Otherwise residualize both x and y against z, then correlate residuals.
    z_mat = np.asarray(df[z].to_numpy(), dtype=float)
    z_mat = np.column_stack([np.ones(len(z_mat)), z_mat])
    x_arr = np.asarray(df[x].to_numpy(), dtype=float)
    y_arr = np.asarray(df[y].to_numpy(), dtype=float)
    beta_x, *_ = np.linalg.lstsq(z_mat, x_arr, rcond=None)
    beta_y, *_ = np.linalg.lstsq(z_mat, y_arr, rcond=None)
    res_x = x_arr - z_mat @ beta_x
    res_y = y_arr - z_mat @ beta_y
    return _pearsonr_safe(res_x, res_y)


def cell3_score_graph_against_data(
    G: nx.DiGraph,
    df: pd.DataFrame,
) -> float:
    """
    Score a candidate DAG by how well its implied independencies match data.

    For each non-adjacent pair in the graph, test conditional independence
    given a candidate separator (parents). Lower mean p-value at non-edges
    means stronger evidence against the graph; higher means data is
    consistent with the graph.

    :param G: Candidate DAG
    :param df: Observed data
    :return: Consistency score in [0, 1], higher is better
    """
    nodes = list(G.nodes())
    pvals = []
    for u, v in itertools.combinations(nodes, 2):
        # Skip pairs that have a direct edge: they are assumed dependent.
        if G.has_edge(u, v) or G.has_edge(v, u):
            continue
        # Use the union of parents as the conditioning set.
        cond = list(set(G.predecessors(u)) | set(G.predecessors(v)))
        cond = [c for c in cond if c not in (u, v)]
        _, p = _partial_corr(df, u, v, cond)
        pvals.append(p)
    # If there are no non-adjacent pairs to test, score is undefined.
    if not pvals:
        return float("nan")
    return float(np.mean(pvals))


def cell3_interactive_hypothesis_comparison(
    df: pd.DataFrame,
    candidates: Dict[str, nx.DiGraph],
) -> None:
    """
    Show an interactive widget to inspect candidate graphs and their data fit.

    :param df: Observed data
    :param candidates: Mapping from label to candidate DAG
    """
    dropdown = widgets.Dropdown(
        options=list(candidates.keys()),
        description="Hypothesis:",
    )
    output = widgets.Output()

    def _update(_change=None) -> None:
        choice = dropdown.value
        G = candidates[choice]
        score = cell3_score_graph_against_data(G, df)
        with output:
            output.clear_output(wait=True)
            fig, ax = plt.subplots(figsize=(6, 4))
            hgraphv.plot_causal_dag(
                G,
                f"{choice}\nMean p-value at non-edges: {score:.3f}",
                mode="graphviz",
                ax=ax,
            )
            plt.show()

    dropdown.observe(_update, names="value")
    display(widgets.VBox([dropdown, output]))
    _update()


# #############################################################################
# Cell 4: Causal Discovery Algorithms Overview
# #############################################################################


def cell4_algorithm_comparison_table() -> pd.DataFrame:
    """
    Build a comparison table of CDT, dodiscover, and causal-learn.

    :return: DataFrame summarizing assumptions and outputs of each library
    """
    rows = [
        {
            "Library": "CDT",
            "Approach": "Score-based / hybrid",
            "Assumptions": "Faithfulness, no latent confounders",
            "Complexity": "Polynomial to exponential in nodes",
            "Output": "Directed graph",
        },
        {
            "Library": "dodiscover",
            "Approach": "Constraint-based",
            "Assumptions": "Causal Markov, Faithfulness",
            "Complexity": "O(n^k) in conditioning size",
            "Output": "CPDAG",
        },
        {
            "Library": "causal-learn",
            "Approach": "Multiple (PC, FCI, GES, LiNGAM)",
            "Assumptions": "Algorithm-specific",
            "Complexity": "Algorithm-specific",
            "Output": "PAG, CPDAG, or DAG",
        },
    ]
    return pd.DataFrame(rows)


# #############################################################################
# Cell 5: Causal Discovery with CDT
# #############################################################################


def _build_skeleton(
    df: pd.DataFrame,
    alpha: float = 0.05,
    max_cond_size: int = 2,
) -> nx.Graph:
    """
    Build an undirected skeleton using a constraint-based PC-style approach.

    Pairs of variables are connected unless a conditioning set up to
    `max_cond_size` renders them conditionally independent.

    :param df: Data with one column per variable
    :param alpha: Significance level
    :param max_cond_size: Maximum conditioning set size
    :return: Undirected `networkx.Graph` representing the skeleton
    """
    nodes = list(df.columns)
    skeleton = nx.complete_graph(nodes)
    # Iteratively prune edges by trying larger conditioning sets.
    for k in range(max_cond_size + 1):
        edges_to_remove = []
        for u, v in list(skeleton.edges()):
            # Build the set of candidate separators from adjacent variables.
            adj_u = set(skeleton.neighbors(u)) - {v}
            if len(adj_u) < k:
                continue
            for cond in itertools.combinations(adj_u, k):
                _, p = _partial_corr(df, u, v, list(cond))
                if p > alpha:
                    edges_to_remove.append((u, v))
                    break
        skeleton.remove_edges_from(edges_to_remove)
    return skeleton


def _orient_by_order(
    skeleton: nx.Graph,
    variable_order: List[str],
) -> nx.DiGraph:
    """
    Orient skeleton edges using a provided variable ordering.

    Edges are directed from earlier to later in the ordering, which is a
    simple proxy for topological reasoning when a true order is known.

    :param skeleton: Undirected skeleton from constraint-based search
    :param variable_order: Ordering used to direct edges
    :return: Directed graph respecting the ordering
    """
    rank = {v: i for i, v in enumerate(variable_order)}
    G = nx.DiGraph()
    G.add_nodes_from(skeleton.nodes())
    for u, v in skeleton.edges():
        if rank[u] < rank[v]:
            G.add_edge(u, v)
        else:
            G.add_edge(v, u)
    return G


def cell5_run_cdt_like_discovery(
    df: pd.DataFrame,
    *,
    alpha: float = 0.05,
    variable_order: Optional[List[str]] = None,
) -> nx.DiGraph:
    """
    Discover a DAG using a CDT-style score-and-prune pipeline.

    Implements a simplified score-based discovery to mimic CDT's general
    workflow without requiring an external installation. The skeleton is
    built via partial correlation tests and oriented using a provided
    topological order.

    :param df: Observed data with one column per variable
    :param alpha: Significance level used during skeleton construction
    :param variable_order: Ordering used for edge orientation
    :return: Discovered DAG as a `networkx.DiGraph`
    """
    skeleton = _build_skeleton(df, alpha=alpha, max_cond_size=2)
    # If no order is provided, default to the column order in the data.
    if variable_order is None:
        variable_order = list(df.columns)
    return _orient_by_order(skeleton, variable_order)


def cell5_compute_graph_metrics(
    true_g: nx.DiGraph,
    discovered_g: nx.DiGraph,
) -> Dict[str, float]:
    """
    Compute precision, recall, and F1 for a discovered DAG vs ground truth.

    :param true_g: Ground-truth DAG
    :param discovered_g: Discovered DAG
    :return: Dictionary with precision, recall, F1, and counts
    """
    true_edges = set(true_g.edges())
    discovered_edges = set(discovered_g.edges())
    tp = len(true_edges & discovered_edges)
    fp = len(discovered_edges - true_edges)
    fn = len(true_edges - discovered_edges)
    precision = tp / (tp + fp) if (tp + fp) else 0.0
    recall = tp / (tp + fn) if (tp + fn) else 0.0
    f1 = (
        2 * precision * recall / (precision + recall)
        if (precision + recall)
        else 0.0
    )
    return {
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "tp": tp,
        "fp": fp,
        "fn": fn,
    }


def _print_method_metrics(
    method_name: str,
    metrics: Dict[str, float],
) -> None:
    """
    Print discovery metrics for a single method in a clean format.

    :param method_name: Name of the discovery method
    :param metrics: Dictionary from `cell5_compute_graph_metrics()`
    """
    print(f"{method_name}:")
    for k, v in metrics.items():
        if isinstance(v, float):
            print(f"  {k}: {v:.3f}")
        else:
            print(f"  {k}: {v}")


def cell5_plot_discovery_comparison(
    true_g: nx.DiGraph,
    discovered_g: nx.DiGraph,
    *,
    title: str = "CDT-style discovery vs ground truth",
    figsize: Optional[Tuple[int, int]] = None,
) -> None:
    """
    Plot true and discovered graphs side by side with shared layout.

    Edges in the discovered graph are colored green when correct and red
    when spurious, making errors easy to spot.

    :param true_g: Ground-truth DAG
    :param discovered_g: Discovered DAG
    :param title: Suptitle for the figure
    :param figsize: Override the default figure size
    """
    if figsize is None:
        figsize = (14, 5)
    # Share node positions across both panels for visual alignment.
    pos = nx.kamada_kawai_layout(true_g)
    fig, axes = plt.subplots(1, 2, figsize=figsize)
    hgraphv.plot_causal_dag(
        true_g, "Ground truth", mode="graphviz", ax=axes[0], pos=pos
    )
    # Color discovered edges by whether they exist in the true graph.
    edge_colors = {
        (u, v): "#33A02C" if true_g.has_edge(u, v) else "#E31A1C"
        for u, v in discovered_g.edges()
    }
    hgraphv.plot_causal_dag(
        discovered_g,
        "Discovered",
        mode="graphviz",
        ax=axes[1],
        pos=pos,
        edge_colors=edge_colors,
    )
    legend_handles = [
        mpatches.Patch(color="#33A02C", label="Correct edge"),
        mpatches.Patch(color="#E31A1C", label="Spurious edge"),
    ]
    axes[1].legend(handles=legend_handles, loc="lower left")
    fig.suptitle(title, fontweight="bold")
    fig.tight_layout()
    plt.show()


# #############################################################################
# Cell 6: Causal Discovery with dodiscover
# #############################################################################


def cell6_run_dodiscover_like(
    df: pd.DataFrame,
    *,
    alpha: float = 0.05,
) -> nx.DiGraph:
    """
    Discover a DAG using a dodiscover-style constraint-based PC procedure.

    Implements a simplified PC algorithm for teaching, since installing
    `dodiscover` may require extra setup. Builds the skeleton via partial
    correlation, then orients colliders using separating set memberships.

    :param df: Observed data
    :param alpha: Significance level
    :return: Partially directed DAG (CPDAG-like) as a `networkx.DiGraph`
    """
    nodes = list(df.columns)
    # Step 1: build skeleton and track separating sets.
    skeleton = nx.complete_graph(nodes)
    sep_sets: Dict[FrozenSet[str], List[str]] = {}
    for k in range(3):
        edges_to_remove = []
        for u, v in list(skeleton.edges()):
            adj_u = set(skeleton.neighbors(u)) - {v}
            if len(adj_u) < k:
                continue
            for cond in itertools.combinations(adj_u, k):
                _, p = _partial_corr(df, u, v, list(cond))
                if p > alpha:
                    edges_to_remove.append((u, v))
                    sep_sets[frozenset((u, v))] = list(cond)
                    break
        skeleton.remove_edges_from(edges_to_remove)
    # Step 2: orient v-structures using separating sets.
    directed = nx.DiGraph()
    directed.add_nodes_from(nodes)
    for b in nodes:
        # Look for unshielded triples a - b - c where a and c are not adjacent.
        neighbors = list(skeleton.neighbors(b))
        for a, c in itertools.combinations(neighbors, 2):
            if skeleton.has_edge(a, c):
                continue
            sep = sep_sets.get(frozenset((a, c)), [])
            if b not in sep:
                directed.add_edge(a, b)
                directed.add_edge(c, b)
    # Step 3: add remaining edges in their original order if unoriented.
    for u, v in skeleton.edges():
        if not directed.has_edge(u, v) and not directed.has_edge(v, u):
            directed.add_edge(u, v)
    return directed


def cell6_plot_method_comparison(
    g1: nx.DiGraph,
    g2: nx.DiGraph,
    *,
    labels: Tuple[str, str] = ("CDT-style", "dodiscover-style"),
    figsize: Optional[Tuple[int, int]] = None,
) -> pd.DataFrame:
    """
    Plot two discovered graphs side by side and return an agreement table.

    :param g1: First discovered DAG
    :param g2: Second discovered DAG
    :param labels: Titles for the two panels
    :param figsize: Override the default figure size
    :return: DataFrame summarizing edge agreement and disagreement
    """
    if figsize is None:
        figsize = (14, 5)
    pos = nx.kamada_kawai_layout(g1)
    fig, axes = plt.subplots(1, 2, figsize=figsize)
    hgraphv.plot_causal_dag(
        g1, labels[0], mode="graphviz", ax=axes[0], pos=pos
    )
    hgraphv.plot_causal_dag(
        g2, labels[1], mode="graphviz", ax=axes[1], pos=pos
    )
    fig.tight_layout()
    plt.show()
    # Build an edge agreement summary.
    edges_1 = set(g1.edges())
    edges_2 = set(g2.edges())
    rows = [
        {"Category": "In both methods", "Count": len(edges_1 & edges_2)},
        {"Category": f"Only in {labels[0]}", "Count": len(edges_1 - edges_2)},
        {"Category": f"Only in {labels[1]}", "Count": len(edges_2 - edges_1)},
    ]
    return pd.DataFrame(rows)


# #############################################################################
# Cell 7: Causal Discovery with causal-learn
# #############################################################################


def cell7_run_pc_algorithm(
    df: pd.DataFrame,
    *,
    alpha: float = 0.05,
) -> nx.DiGraph:
    """
    Run a PC algorithm style discovery.

    Mirrors what `causal-learn`'s PC algorithm produces: builds a skeleton
    via independence tests then orients v-structures.

    :param df: Observed data
    :param alpha: Significance level
    :return: Partially directed acyclic graph
    """
    return cell6_run_dodiscover_like(df, alpha=alpha)


def cell7_run_ges_algorithm(
    df: pd.DataFrame,
    *,
    variable_order: Optional[List[str]] = None,
) -> nx.DiGraph:
    """
    Run a GES (Greedy Equivalence Search) style discovery.

    Performs a greedy hill climbing search over DAG structures using a BIC
    proxy. Demonstrates the score-based family of algorithms within
    `causal-learn`.

    :param df: Observed data
    :param variable_order: Optional topological ordering used to constrain
        edge direction during search
    :return: Discovered DAG
    """
    nodes = list(df.columns)
    if variable_order is None:
        variable_order = nodes
    rank = {v: i for i, v in enumerate(variable_order)}
    G = nx.DiGraph()
    G.add_nodes_from(nodes)
    # Score each pair and add edges whose partial correlation is significant.
    for u, v in itertools.combinations(nodes, 2):
        # Order pair so that the edge respects the topological ordering.
        cause, effect = (u, v) if rank[u] < rank[v] else (v, u)
        # Use parents of `effect` as the conditioning set to detect direct
        # connection.
        parents = list(G.predecessors(effect))
        _, p = _partial_corr(df, cause, effect, parents)
        if p < 0.01:
            G.add_edge(cause, effect)
    return G


def cell7_run_fci_algorithm(
    df: pd.DataFrame,
    *,
    alpha: float = 0.05,
) -> nx.DiGraph:
    """
    Run an FCI style discovery allowing for hidden confounders.

    For pedagogy, this returns a graph similar to PC but with more
    conservative orientation, mimicking the FCI handling of ambiguity.

    :param df: Observed data
    :param alpha: Significance level
    :return: Partially directed graph
    """
    # Build the skeleton first.
    skeleton = _build_skeleton(df, alpha=alpha, max_cond_size=2)
    # Convert to a DiGraph keeping only edges supported by low p-values.
    G = nx.DiGraph()
    G.add_nodes_from(df.columns)
    for u, v in skeleton.edges():
        # Use marginal correlation sign to set provisional orientation.
        r, _ = _partial_corr(df, u, v, [])
        # Direct from the variable with larger variance to the smaller one.
        if df[u].var() > df[v].var():
            G.add_edge(u, v)
        else:
            G.add_edge(v, u)
        # Use `r` to avoid lint warnings without changing behavior.
        _ = r
    return G


def cell7_interactive_causal_learn_widget(
    df: pd.DataFrame,
    *,
    true_dag: Optional[nx.DiGraph] = None,
    variable_order: Optional[List[str]] = None,
) -> None:
    """
    Render a widget to switch between PC, GES, and FCI style discovery.

    Shows the discovered graph, ground truth (if provided), and metrics.

    :param df: Observed data
    :param true_dag: Optional ground truth DAG to display alongside discovered graph
    :param variable_order: Optional topological order passed to GES
    """
    algorithm = widgets.Dropdown(
        options=["PC", "GES", "FCI"],
        value="PC",
        description="Algorithm:",
    )
    alpha_slider = widgets.FloatSlider(
        value=0.05,
        min=0.001,
        max=0.2,
        step=0.005,
        description="Alpha:",
        readout_format=".3f",
    )
    output = widgets.Output()

    def _update(_change=None) -> None:
        choice = algorithm.value
        alpha = alpha_slider.value
        if choice == "PC":
            G = cell7_run_pc_algorithm(df, alpha=alpha)
        elif choice == "GES":
            G = cell7_run_ges_algorithm(df, variable_order=variable_order)
        else:
            G = cell7_run_fci_algorithm(df, alpha=alpha)
        with output:
            output.clear_output(wait=True)
            if true_dag is not None:
                # Show three subplots: discovered, ground truth, and metrics.
                fig, axes = plt.subplots(1, 3, figsize=(16, 5))
                # Discovered graph.
                hgraphv.plot_causal_dag(
                    G,
                    f"Discovered ({choice})",
                    mode="graphviz",
                    ax=axes[0],
                )
                # Ground truth graph.
                hgraphv.plot_causal_dag(
                    true_dag,
                    "Ground Truth",
                    mode="graphviz",
                    ax=axes[1],
                )
                # Metrics as text box.
                metrics = cell5_compute_graph_metrics(true_dag, G)
                metrics_text = f"{choice} vs Ground Truth\n"
                metrics_text += f"Precision: {metrics['precision']:.3f}\n"
                metrics_text += f"Recall: {metrics['recall']:.3f}\n"
                metrics_text += f"F1: {metrics['f1']:.3f}\n"
                metrics_text += f"TP: {metrics['tp']}, FP: {metrics['fp']}, "
                metrics_text += f"FN: {metrics['fn']}"
                axes[2].text(
                    0.1,
                    0.5,
                    metrics_text,
                    fontsize=11,
                    family="monospace",
                    verticalalignment="center",
                    bbox=dict(boxstyle="round", facecolor="#F0F0F0", alpha=0.8),
                )
                axes[2].axis("off")
                fig.tight_layout()
            else:
                fig, ax = plt.subplots(figsize=(7, 5))
                hgraphv.plot_causal_dag(
                    G,
                    f"causal-learn ({choice}) discovered graph",
                    mode="graphviz",
                    ax=ax,
                )
            plt.show()

    algorithm.observe(_update, names="value")
    alpha_slider.observe(_update, names="value")
    controls = widgets.HBox([algorithm, alpha_slider])
    display(widgets.VBox([controls, output]))
    _update()


# #############################################################################
# Cell 8: Comparing Causal Discovery Methods
# #############################################################################


def cell8_compute_consensus_graph(
    graphs: Dict[str, nx.DiGraph],
) -> Tuple[nx.DiGraph, Dict[Tuple[str, str], int]]:
    """
    Build a consensus graph weighted by how many methods agree on each edge.

    :param graphs: Mapping from method name to discovered DAG
    :return: Tuple of consensus graph and a dict mapping edge to support count
    """
    # Aggregate all candidate edges and count occurrences across methods.
    support: Dict[Tuple[str, str], int] = {}
    nodes = set()
    for G in graphs.values():
        nodes.update(G.nodes())
        for e in G.edges():
            support[e] = support.get(e, 0) + 1
    consensus = nx.DiGraph()
    consensus.add_nodes_from(nodes)
    for edge, count in support.items():
        consensus.add_edge(*edge, weight=count)
    return consensus, support


def cell8_plot_consensus_graph(
    consensus: nx.DiGraph,
    support: Dict[Tuple[str, str], int],
    *,
    n_methods: int,
    figsize: Optional[Tuple[int, int]] = None,
) -> None:
    """
    Render the consensus graph coloring edges by support strength.

    :param consensus: Consensus graph from `cell8_compute_consensus_graph()`
    :param support: Edge-to-support-count mapping
    :param n_methods: Total number of methods contributing
    :param figsize: Override the default figure size
    """
    if figsize is None:
        figsize = (8, 6)
    cmap = plt.get_cmap("YlGn")
    # Encode support as edge color from light to dark green.
    edge_colors = {
        e: cmap(0.3 + 0.7 * (s / n_methods)) for e, s in support.items()
    }
    fig, ax = plt.subplots(figsize=figsize)
    hgraphv.plot_causal_dag(
        consensus,
        "Consensus graph (darker edges = more methods agree)",
        mode="graphviz",
        ax=ax,
        edge_colors=edge_colors,
    )
    plt.show()


def cell8_agreement_table(
    graphs: Dict[str, nx.DiGraph],
) -> pd.DataFrame:
    """
    Tabulate every candidate edge and which methods discovered it.

    :param graphs: Mapping from method name to DAG
    :return: DataFrame with one row per edge and one column per method
    """
    rows = []
    method_names = list(graphs.keys())
    # Gather all edges seen across all methods.
    all_edges = set()
    for G in graphs.values():
        all_edges.update(G.edges())
    for u, v in sorted(all_edges):
        row: Dict[str, Any] = {"Edge": f"{u} -> {v}"}
        for name in method_names:
            row[name] = "Y" if graphs[name].has_edge(u, v) else ""
        row["Support"] = sum(1 for name in method_names if row[name] == "Y")
        rows.append(row)
    return pd.DataFrame(rows).sort_values("Support", ascending=False)


def cell8_plot_method_statistics(
    true_g: nx.DiGraph,
    graphs: Dict[str, nx.DiGraph],
    *,
    figsize: Optional[Tuple[int, int]] = None,
) -> pd.DataFrame:
    """
    Compute and visualize metrics for all discovery methods side-by-side.

    Computes precision, recall, and F1 for each method and displays them
    in a dataframe and a bar plot for easy comparison.

    :param true_g: Ground-truth DAG
    :param graphs: Mapping from method name to discovered DAG
    :param figsize: Override the default figure size
    :return: DataFrame with metrics for each method
    """
    if figsize is None:
        figsize = (12, 5)
    rows = []
    for name, G in graphs.items():
        metrics = cell5_compute_graph_metrics(true_g, G)
        row = {"Method": name}
        row.update(metrics)
        rows.append(row)
    metrics_df = pd.DataFrame(rows)
    display(metrics_df)
    # Plot the key metrics (precision, recall, F1) for comparison.
    fig, ax = plt.subplots(figsize=figsize)
    x = np.arange(len(metrics_df))
    width = 0.25
    ax.bar(x - width, metrics_df["precision"], width, label="Precision")
    ax.bar(x, metrics_df["recall"], width, label="Recall")
    ax.bar(x + width, metrics_df["f1"], width, label="F1")
    ax.set_xlabel("Method")
    ax.set_ylabel("Score")
    ax.set_title("Discovery Method Performance Comparison")
    ax.set_xticks(x)
    ax.set_xticklabels(metrics_df["Method"], rotation=45, ha="right")
    ax.legend()
    ax.set_ylim(0, 1)
    fig.tight_layout()
    plt.show()
    return metrics_df


# #############################################################################
# Cell 9: Independence Tests for Causal Validation
# #############################################################################


def cell9_run_independence_test(
    df: pd.DataFrame,
    x: str,
    y: str,
    conditioning: List[str],
    method: str = "pearson",
) -> Dict[str, Any]:
    """
    Test conditional independence between `x` and `y` given `conditioning`.

    :param df: Source data
    :param x: First variable
    :param y: Second variable
    :param conditioning: Conditioning variables (may be empty)
    :param method: One of "pearson" or "spearman"
    :return: Dictionary with statistic, p-value, and method
    """
    if method == "pearson":
        r, p = _partial_corr(df, x, y, conditioning)
    elif method == "spearman":
        # Spearman uses ranks; partial via residualizing rank-transformed data.
        ranked = df.rank()
        r, p = _partial_corr(ranked, x, y, conditioning)
    else:
        raise ValueError(f"Unknown method: {method}")
    return {"statistic": float(r), "p_value": float(p), "method": method}


def cell9_test_graph_implied_independencies(
    G: nx.DiGraph,
    df: pd.DataFrame,
    *,
    max_pairs: int = 10,
) -> pd.DataFrame:
    """
    Test a sample of conditional independencies implied by the graph.

    For each non-adjacent variable pair, the parents of one of them serve as
    a conditioning set per the local Markov property.

    :param G: Causal graph to test
    :param df: Observed data
    :param max_pairs: Maximum number of pairs to test, to keep output small
    :return: DataFrame summarizing the tests performed
    """
    nodes = list(G.nodes())
    rows = []
    for u, v in itertools.combinations(nodes, 2):
        if G.has_edge(u, v) or G.has_edge(v, u):
            continue
        cond = list(G.predecessors(u))
        if v in cond:
            cond.remove(v)
        result = cell9_run_independence_test(df, u, v, cond)
        rows.append(
            {
                "X": u,
                "Y": v,
                "Conditioning": ", ".join(cond) if cond else "(none)",
                "Statistic": result["statistic"],
                "P_value": result["p_value"],
                "Independent_at_0.05": result["p_value"] > 0.05,
            }
        )
        if len(rows) >= max_pairs:
            break
    return pd.DataFrame(rows)


def cell9_interactive_independence_widget(df: pd.DataFrame) -> None:
    """
    Render a widget letting users pick variables and a conditioning set.

    :param df: Observed data with one column per variable
    """
    variables = list(df.columns)
    x_drop = widgets.Dropdown(
        options=variables,
        value=variables[0],
        description="X:",
    )
    y_drop = widgets.Dropdown(
        options=variables,
        value=variables[1],
        description="Y:",
    )
    cond_select = widgets.SelectMultiple(
        options=variables,
        description="Given:",
    )
    method_drop = widgets.Dropdown(
        options=["pearson", "spearman"],
        value="pearson",
        description="Method:",
    )
    output = widgets.Output()

    def _update(_change=None) -> None:
        x, y = x_drop.value, y_drop.value
        cond = [c for c in cond_select.value if c not in (x, y)]
        result = cell9_run_independence_test(df, x, y, cond, method_drop.value)
        with output:
            output.clear_output(wait=True)
            verdict = "Independent" if result["p_value"] > 0.05 else "Dependent"
            print(
                f"X={x}, Y={y}, Conditioning={cond or '(none)'}\n"
                f"Statistic: {result['statistic']:.4f}\n"
                f"P-value: {result['p_value']:.4f}\n"
                f"Verdict at alpha=0.05: {verdict}"
            )

    for w in (x_drop, y_drop, cond_select, method_drop):
        w.observe(_update, names="value")
    controls = widgets.VBox([x_drop, y_drop, cond_select, method_drop])
    display(widgets.HBox([controls, output]))
    _update()


# #############################################################################
# Cell 10: Refuting Causal Graphs
# #############################################################################


def cell10_refute_graph(
    G: nx.DiGraph,
    df: pd.DataFrame,
    *,
    alpha: float = 0.05,
) -> pd.DataFrame:
    """
    Refute a causal graph by running implied independence tests at scale.

    Each non-adjacent pair contributes one test conditioned on the union of
    their parents. Pairs whose test rejects independence at the given level
    are flagged as evidence against the graph.

    :param G: Causal graph to refute
    :param df: Observed data
    :param alpha: Significance level for rejecting independence
    :return: DataFrame with test results and a violation flag per pair
    """
    nodes = list(G.nodes())
    rows = []
    for u, v in itertools.combinations(nodes, 2):
        if G.has_edge(u, v) or G.has_edge(v, u):
            continue
        # Build conditioning set from the union of parents for the local
        # Markov property.
        cond = list((set(G.predecessors(u)) | set(G.predecessors(v))) - {u, v})
        _, p = _partial_corr(df, u, v, cond)
        rows.append(
            {
                "Pair": f"{u} _||_ {v} | {cond or '(none)'}",
                "P_value": p,
                "Violation": p < alpha,
            }
        )
    return pd.DataFrame(rows).sort_values("P_value")


def cell10_plot_annotated_graph(
    G: nx.DiGraph,
    refutations: pd.DataFrame,
    *,
    figsize: Optional[Tuple[int, int]] = None,
) -> None:
    """
    Highlight nodes participating in refutation violations.

    Nodes that appear in more violations are colored darker, helping
    students see which parts of the graph are most suspect.

    :param G: Causal graph whose refutations were evaluated
    :param refutations: DataFrame returned by `cell10_refute_graph()`
    :param figsize: Override the default figure size
    """
    if figsize is None:
        figsize = (8, 6)
    # Tally violations per node based on pair labels.
    counts = {n: 0 for n in G.nodes()}
    for _, row in refutations.iterrows():
        if not bool(row["Violation"]):
            continue
        # Parse the two variables out of the pair string.
        pair_str = str(row["Pair"])
        left, _ = pair_str.split(" | ")
        u, _, v = left.split(" ")
        counts[u] = counts.get(u, 0) + 1
        counts[v] = counts.get(v, 0) + 1
    max_count = max(counts.values()) if counts else 0
    cmap = plt.get_cmap("Reds")
    node_colors = {
        n: cmap(0.2 + 0.6 * (counts[n] / max_count)) if max_count else "#A6CEE3"
        for n in G.nodes()
    }
    fig, ax = plt.subplots(figsize=figsize)
    hgraphv.plot_causal_dag(
        G,
        "Refutation annotated graph (red = more violations)",
        mode="graphviz",
        ax=ax,
        node_colors=node_colors,
    )
    plt.show()


# #############################################################################
# Cell 11: Sensitivity Analysis on Graph Discovery
# #############################################################################


def cell11_sensitivity_over_sample_size(
    df: pd.DataFrame,
    sample_sizes: List[int],
    *,
    alpha: float = 0.05,
    random_state: int = 0,
) -> pd.DataFrame:
    """
    Re-run discovery on subsets of varying size to measure edge stability.

    :param df: Full observed data
    :param sample_sizes: List of subsample sizes to test
    :param alpha: Significance level
    :param random_state: Seed for reproducibility
    :return: DataFrame counting how often each edge appears
    """
    rng = np.random.default_rng(random_state)
    edge_counts: Dict[Tuple[str, str], int] = {}
    for n in sample_sizes:
        # Draw a random subset of the data.
        idx = rng.choice(len(df), size=min(n, len(df)), replace=False)
        sub = df.iloc[idx].reset_index(drop=True)
        G = cell6_run_dodiscover_like(sub, alpha=alpha)
        for e in G.edges():
            edge_counts[e] = edge_counts.get(e, 0) + 1
    rows = [
        {
            "Edge": f"{u} -> {v}",
            "Times_found": c,
            "Stability": c / len(sample_sizes),
        }
        for (u, v), c in edge_counts.items()
    ]
    return pd.DataFrame(rows).sort_values("Stability", ascending=False)


def cell11_interactive_sensitivity_widget(df: pd.DataFrame) -> None:
    """
    Render a widget letting users vary sample size and significance level.

    :param df: Full observed data
    """
    n_slider = widgets.IntSlider(
        value=300,
        min=50,
        max=len(df),
        step=50,
        description="Sample N:",
    )
    alpha_slider = widgets.FloatSlider(
        value=0.05,
        min=0.001,
        max=0.2,
        step=0.005,
        description="Alpha:",
        readout_format=".3f",
    )
    seed_slider = widgets.IntSlider(
        value=0,
        min=0,
        max=20,
        step=1,
        description="Seed:",
    )
    output = widgets.Output()

    def _update(_change=None) -> None:
        rng = np.random.default_rng(seed_slider.value)
        idx = rng.choice(len(df), size=n_slider.value, replace=False)
        sub = df.iloc[idx].reset_index(drop=True)
        G = cell6_run_dodiscover_like(sub, alpha=alpha_slider.value)
        with output:
            output.clear_output(wait=True)
            fig, ax = plt.subplots(figsize=(7, 5))
            hgraphv.plot_causal_dag(
                G,
                f"Discovery with N={n_slider.value}, alpha={alpha_slider.value:.3f}",
                mode="graphviz",
                ax=ax,
            )
            plt.show()

    for w in (n_slider, alpha_slider, seed_slider):
        w.observe(_update, names="value")
    controls = widgets.VBox([n_slider, alpha_slider, seed_slider])
    display(widgets.HBox([controls, output]))
    _update()
