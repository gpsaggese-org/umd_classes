"""
Utility functions for L08_02 causal inference tutorial.

Import as:

import msml610.tutorials.L08_02_causal_inference_utils as mtl0cireout
"""

import logging
from typing import Iterable, Optional

import matplotlib.pyplot as plt
import networkx as nx

_LOG = logging.getLogger(__name__)


# #############################################################################
# Graph visualization
# #############################################################################


def plot_graph_highlight(
    graph: nx.Graph,
    *,
    node1: Optional[str] = None,
    node2: Optional[str] = None,
    conditioning_node_set: Optional[Iterable[str]] = None,
    layout: str = "shell",
    figsize: tuple = (6, 4),
) -> None:
    """
    Plot a graph with highlighted nodes.

    :param graph: directed graph to plot
    :param node1: node colored green
    :param node2: node colored blue
    :param conditioning_node_set: iterable of nodes colored red
    :param layout: layout algorithm ("shell", "spring", "kamada_kawai")
    :param figsize: figure size
    """
    conditioning_node_set = set(conditioning_node_set) if conditioning_node_set else set()
    plt.figure(figsize=figsize)
    # Choose layout.
    if layout == "spring":
        pos = nx.spring_layout(graph)
    elif layout == "kamada_kawai":
        pos = nx.kamada_kawai_layout(graph)
    else:
        pos = nx.shell_layout(graph)
    # Assign colors.
    node_colors = []
    for node in graph.nodes():
        if node == node1:
            node_colors.append("green")
        elif node == node2:
            node_colors.append("blue")
        elif node in conditioning_node_set:
            node_colors.append("red")
        else:
            node_colors.append("lightblue")
    # Draw.
    nx.draw(
        graph,
        pos,
        with_labels=True,
        node_color=node_colors,
        node_size=2000,
        font_size=12,
        font_weight="bold",
        edge_color="gray",
        edgecolors="black",
        linewidths=2,
    )
    plt.show()


# #############################################################################
# Graph utilities
# #############################################################################


def reachable_subgraph(graph: nx.DiGraph, nodes: Iterable[str]) -> nx.Graph:
    """
    Return the subgraph containing all nodes reachable from the given nodes.

    :param graph: directed graph
    :param nodes: source nodes to start from (included in result)
    :return: subgraph of reachable nodes
    """
    reachable = set(nodes)
    for node in nodes:
        reachable |= nx.descendants(graph, node)
    return graph.subgraph(reachable).copy()
