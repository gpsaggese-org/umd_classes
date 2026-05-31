r"""
Utility functions for probabilistic inference visualization and exploration.

Provides interactive widgets, visualizations, and Bayesian network operations
for the probabilistic inference notebook using pgmpy.
"""

import logging
import time
import warnings
from typing import Dict, List, Optional, Tuple

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd
import seaborn as sns
from IPython.display import HTML as IPhtml
from IPython.display import display
import ipywidgets
from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import ApproxInference, BeliefPropagation, VariableElimination
from pgmpy.models import DiscreteBayesianNetwork

import helpers.hdbg as hdbg
import helpers.hgraphviz as hgraphviz
import helpers.htutorial as htutori

_LOG = logging.getLogger(__name__)

warnings.filterwarnings('ignore')


# #############################################################################
# Helper: Medical Network Implementation
# #############################################################################

def _create_medical_network_impl() -> DiscreteBayesianNetwork:
    """
    Create a simple medical diagnosis Bayesian network.

    Builds a network with Disease as a root node and Symptom and Test as
    children. Each node has appropriate conditional probability distributions
    (CPDs) defined based on realistic medical scenarios.

    :return: Configured DiscreteBayesianNetwork instance
    """
    # Create network structure with disease as root node.
    model = DiscreteBayesianNetwork([
        ('Disease', 'Symptom'),
        ('Disease', 'Test')
    ])
    # Define disease prior probability.
    cpd_disease = TabularCPD(
        'Disease', 2, [[0.95], [0.05]],
        state_names={'Disease': ['Absent', 'Present']}
    )
    # Define symptom likelihood given disease state.
    cpd_symptom = TabularCPD(
        'Symptom', 2,
        [[0.95, 0.2], [0.05, 0.8]],
        evidence=['Disease'],
        evidence_card=[2],
        state_names={'Symptom': ['Absent', 'Present'], 'Disease': ['Absent', 'Present']}
    )
    # Define test result likelihood given disease state.
    cpd_test = TabularCPD(
        'Test', 2,
        [[0.95, 0.1], [0.05, 0.9]],
        evidence=['Disease'],
        evidence_card=[2],
        state_names={'Test': ['Negative', 'Positive'], 'Disease': ['Absent', 'Present']}
    )
    # Add CPDs and validate the model.
    model.add_cpds(cpd_disease, cpd_symptom, cpd_test)
    model.check_model()
    return model


def _visualize_network_impl(
    model: DiscreteBayesianNetwork,
    *,
    evidence: Optional[List[str]] = None,
    figsize: Tuple[int, int] = (10, 6),
) -> None:
    """
    Visualize Bayesian network structure with optional evidence highlighting.

    Renders the network graph with nodes colored based on whether they are
    part of the evidence set. Evidence nodes are highlighted in red while
    other nodes are shown in teal. Uses graphviz for professional layout.

    :param model: Bayesian network to visualize
    :param evidence: List of node names to highlight as evidence
        - Default: `None` (no nodes highlighted)
    :param figsize: Figure dimensions as (width, height)
        - Default: `(10, 6)`
    """
    # Create directed graph from model edges.
    graph = nx.DiGraph()
    graph.add_edges_from(model.edges())
    # Map node colors based on evidence status.
    node_colors = {
        node: '#ff6b6b' if (evidence and node in evidence) else '#4ecdc4'
        for node in graph.nodes()
    }
    # Render using graphviz-based plotting function.
    hgraphviz.plot_causal_dag(
        graph,
        'Bayesian Network Structure',
        mode='graphviz',
        node_colors=node_colors,
        figsize=figsize,
    )


# #############################################################################
# Cell 2.2: Network Structure Visualization
# #############################################################################

def cell2_2_create_network() -> DiscreteBayesianNetwork:
    """Create a simple medical diagnosis Bayesian network."""
    return _create_medical_network_impl()


def cell2_2_visualize_network(
    model: DiscreteBayesianNetwork,
    *,
    evidence: Optional[List[str]] = None,
    figsize: Tuple[int, int] = (10, 6),
) -> None:
    """Visualize Bayesian network structure with optional evidence highlighting."""
    return _visualize_network_impl(model, evidence=evidence, figsize=figsize)


# #############################################################################
# Cell 3.2: Interactive CPD Visualization
# #############################################################################

def cell3_2_create_cpd_widget(
    *, disease_prior: float = 0.05
) -> ipywidgets.VBox:
    """
    Create interactive widget for exploring conditional probability distributions.

    Displays a slider to control disease prior probability and visualizes three
    CPDs as heatmaps: P(Disease), P(Symptom|Disease), and P(Test|Disease).
    Updates automatically when slider value changes.

    :param disease_prior: Initial disease prior probability value
        - Default: `0.05`
    :return: IPywidgets VBox containing slider and visualization output
    """
    output = ipywidgets.Output()
    # Create disease prior probability slider using htutori.
    prior_slider, prior_box = htutori.build_widget_control(
        name="prior",
        description="disease prior",
        min_val=0.0,
        max_val=1.0,
        step=0.01,
        initial_value=disease_prior,
        is_float=True
    )
    # Create disease state toggle button.
    toggle = ipywidgets.ToggleButtons(
        options=['None', 'Present', 'Absent'],
        description='Disease:',
        style={'description_width': '100px'}
    )
    # Define callback to update visualization when controls change.
    def _update_display(change: Optional[Dict] = None) -> None:
        """Update CPD heatmaps based on slider and toggle values."""
        with output:
            output.clear_output(wait=True)
            p_disease = prior_slider.value
            # Create figure with four subplots.
            fig, axes = plt.subplots(1, 4, figsize=(20, 5))
            # Visualize disease prior probability.
            data_prior = pd.DataFrame(
                {'Present': [p_disease], 'Absent': [1 - p_disease]},
                index=pd.Index(['P(Disease)'])
            )
            sns.heatmap(
                data_prior, annot=True, fmt='.3f', cmap='RdYlGn',
                vmin=0, vmax=1, ax=axes[0], cbar=False
            )
            axes[0].set_title('P(Disease)', fontweight='bold')
            # Visualize symptom given disease CPD.
            symptom_given_disease = pd.DataFrame(
                {'Symptom': [0.05, 0.8], 'No Symptom': [0.95, 0.2]},
                index=pd.Index(['Disease', 'No Disease'])
            )
            sns.heatmap(
                symptom_given_disease, annot=True, fmt='.2f', cmap='Blues',
                vmin=0, vmax=1, ax=axes[1], cbar=False
            )
            axes[1].set_title('P(Symptom | Disease)', fontweight='bold')
            # Visualize test result given disease CPD.
            test_given_disease = pd.DataFrame(
                {'Positive': [0.05, 0.9], 'Negative': [0.95, 0.1]},
                index=pd.Index(['Disease', 'No Disease'])
            )
            sns.heatmap(
                test_given_disease, annot=True, fmt='.2f', cmap='Oranges',
                vmin=0, vmax=1, ax=axes[2], cbar=False
            )
            axes[2].set_title('P(Test | Disease)', fontweight='bold')
            # Comments panel.
            axes[3].axis("off")
            axes[3].set_title("Comments", fontsize=14, fontweight="bold", pad=20)
            htutori.add_fitted_text_box(
                axes[3],
                f"P(Disease) = {p_disease:.3f}\n"
                f"CPD relationships fixed\n"
                f"Adjust prior to see impact"
            )
            plt.tight_layout()
            plt.show()
    # Register callbacks for interactive updates.
    prior_slider.observe(_update_display, 'value')
    toggle.observe(_update_display, 'value')
    # Display initial state.
    _update_display()
    return ipywidgets.VBox([
        ipywidgets.HBox([prior_box, toggle]),
        output
    ])


# #############################################################################
# Cell 4.1: Sampling from Prior
# #############################################################################

def cell4_1_create_network() -> DiscreteBayesianNetwork:
    """Create a simple medical diagnosis Bayesian network."""
    return _create_medical_network_impl()


def cell4_1_forward_sample_and_plot(
    model: DiscreteBayesianNetwork, *, n_samples: int = 1000,
    figsize: Optional[Tuple[int, int]] = None
) -> None:
    """
    Sample from network prior and visualize marginal distributions.

    Generates samples from the Bayesian network without any evidence and plots
    the resulting marginal probability distribution for each variable as a bar
    chart with annotated values.

    :param model: Bayesian network to sample from
    :param n_samples: Number of samples to generate
        - Default: `1000`
    :param figsize: Figure dimensions as (width, height)
        - Default: `None` (uses matplotlib defaults)
    """
    if figsize is None:
        figsize = plt.rcParams["figure.figsize"]
    # Generate samples from the network prior.
    samples = model.simulate(n_samples=n_samples, show_progress=False)
    # Create figure with one subplot per variable.
    fig, axes = plt.subplots(1, 3, figsize=figsize)
    # Plot marginal distribution for each variable.
    for idx, (col, ax) in enumerate(zip(samples.columns, axes)):
        # Count occurrences and normalize to get probabilities.
        counts = samples[col].value_counts(normalize=True).sort_index()
        colors = ['#4ecdc4', '#ff6b6b']
        bars = ax.bar(
            range(len(counts)), counts.values, color=colors[:len(counts)]
        )
        # Set x-axis labels and formatting.
        ax.set_xticks(range(len(counts)))
        state_labels = ['Absent', 'Present']
        ax.set_xticklabels(state_labels[:len(counts)])
        ax.set_ylabel('Probability')
        ax.set_title(f'{col}', fontweight='bold')
        ax.set_ylim([0, 1])
        # Add value labels on top of bars.
        for i, bar in enumerate(bars):
            height = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width() / 2., height,
                f'{height:.3f}', ha='center', va='bottom'
            )
    # Set overall title and layout.
    fig.suptitle(
        'Belief Before Any Observations (Forward Sampling)',
        fontweight='bold', fontsize=14
    )
    plt.tight_layout()


# #############################################################################
# Cell 4.2: Exact vs Approximate Inference
# #############################################################################

def cell4_2_create_network() -> DiscreteBayesianNetwork:
    """Create a simple medical diagnosis Bayesian network."""
    return _create_medical_network_impl()


def cell4_2_compare_exact_and_sampling(
    model: DiscreteBayesianNetwork,
    *, figsize: Optional[Tuple[int, int]] = None
) -> None:
    """
    Compare exact inference results with sampling-based approximations.

    Performs variable elimination for exact inference and forward sampling,
    then displays both results side-by-side as grouped bar charts for each
    variable to visualize the approximation quality.

    :param model: Bayesian network to analyze
    :param figsize: Figure dimensions as (width, height)
        - Default: `None` (uses matplotlib defaults)
    """
    if figsize is None:
        figsize = plt.rcParams["figure.figsize"]
    # Create exact inference engine.
    inference = VariableElimination(model)
    # Generate samples from the network.
    n_samples = 1000
    samples = model.simulate(n_samples=n_samples, show_progress=False)
    # Create figure with one subplot per variable.
    fig, axes = plt.subplots(1, 3, figsize=figsize)
    # Compare inference methods for each variable.
    for idx, var in enumerate(model.nodes()):
        ax = axes[idx]
        # Compute exact marginal probabilities via variable elimination.
        exact_result = inference.query(variables=[var])
        exact_probs = exact_result.values.flatten()
        # Compute approximate marginal from samples.
        sample_counts = samples[var].value_counts(normalize=True).sort_index()
        sample_probs = sample_counts.values
        # Create grouped bar chart comparing methods.
        x = np.arange(2)
        width = 0.35
        ax.bar(
            x - width / 2, sample_probs, width, label='Forward Sampling',
            alpha=0.7
        )
        ax.bar(
            x + width / 2, exact_probs, width,
            label='Variable Elimination', alpha=0.7
        )
        # Set labels and formatting.
        ax.set_ylabel('Probability')
        ax.set_title(f'{var}', fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels(['Absent', 'Present'])
        ax.set_ylim([0, 1])
        ax.legend()
    # Set overall title and layout.
    fig.suptitle('Exact vs. Sampling Inference', fontweight='bold', fontsize=14)
    plt.tight_layout()


# #############################################################################
# Cell 5.1: Effect of Evidence on Beliefs
# #############################################################################

def cell5_1_create_network() -> DiscreteBayesianNetwork:
    """Create a simple medical diagnosis Bayesian network."""
    return _create_medical_network_impl()


def cell5_1_condition_on_evidence(
    model: DiscreteBayesianNetwork, *,
    figsize: Optional[Tuple[int, int]] = None
) -> None:
    """
    Visualize how evidence updates beliefs through Bayesian updating.

    Computes and displays three probability distributions: prior belief,
    posterior after positive test, and posterior after negative test. Shows
    how the same test result differently impacts belief depending on outcome.

    :param model: Bayesian network for inference
    :param figsize: Figure dimensions as (width, height)
        - Default: `None` (uses matplotlib defaults)
    """
    if figsize is None:
        figsize = plt.rcParams["figure.figsize"]
    # Create exact inference engine.
    inference = VariableElimination(model)
    # Create figure with three subplots for prior and posteriors.
    fig, axes = plt.subplots(1, 3, figsize=figsize)
    # Compute prior and posterior distributions.
    prior = inference.query(variables=['Disease'])
    posterior_pos = inference.query(
        variables=['Disease'], evidence={'Test': 'Positive'}
    )
    posterior_neg = inference.query(
        variables=['Disease'], evidence={'Test': 'Negative'}
    )
    # Prepare data for plotting.
    probs = [
        prior.values.flatten(),
        posterior_pos.values.flatten(),
        posterior_neg.values.flatten()
    ]
    titles = [
        'Prior P(Disease)',
        'Posterior P(Disease | Test+)',
        'Posterior P(Disease | Test-)'
    ]
    # Plot each distribution with value annotations.
    for ax, prob, title in zip(axes, probs, titles):
        colors = ['#4ecdc4', '#ff6b6b']
        bars = ax.bar(['Absent', 'Present'], prob, color=colors)
        ax.set_ylabel('Probability')
        ax.set_title(title, fontweight='bold')
        ax.set_ylim([0, 1])
        # Add probability values on bars.
        for bar in bars:
            height = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width() / 2., height,
                f'{height:.3f}', ha='center', va='bottom'
            )
    # Set overall title and layout.
    fig.suptitle('How Evidence Changes Beliefs', fontweight='bold', fontsize=14)
    plt.tight_layout()


# #############################################################################
# Cell 5.2: Evidence Combination and Strength
# #############################################################################

def cell5_2_create_network() -> DiscreteBayesianNetwork:
    """Create a simple medical diagnosis Bayesian network."""
    return _create_medical_network_impl()


def cell5_2_compare_exact_and_sampling(
    model: DiscreteBayesianNetwork,
    *, figsize: Optional[Tuple[int, int]] = None
) -> None:
    """
    Compare exact inference results with sampling-based approximations.

    Performs variable elimination for exact inference and forward sampling,
    then displays both results side-by-side as grouped bar charts for each
    variable to visualize the approximation quality.

    :param model: Bayesian network to analyze
    :param figsize: Figure dimensions as (width, height)
        - Default: `None` (uses matplotlib defaults)
    """
    if figsize is None:
        figsize = plt.rcParams["figure.figsize"]
    # Create exact inference engine.
    inference = VariableElimination(model)
    # Generate samples from the network.
    n_samples = 1000
    samples = model.simulate(n_samples=n_samples, show_progress=False)
    # Create figure with one subplot per variable.
    fig, axes = plt.subplots(1, 3, figsize=figsize)
    # Compare inference methods for each variable.
    for idx, var in enumerate(model.nodes()):
        ax = axes[idx]
        # Compute exact marginal probabilities via variable elimination.
        exact_result = inference.query(variables=[var])
        exact_probs = exact_result.values.flatten()
        # Compute approximate marginal from samples.
        sample_counts = samples[var].value_counts(normalize=True).sort_index()
        sample_probs = sample_counts.values
        # Create grouped bar chart comparing methods.
        x = np.arange(2)
        width = 0.35
        ax.bar(
            x - width / 2, sample_probs, width, label='Forward Sampling',
            alpha=0.7
        )
        ax.bar(
            x + width / 2, exact_probs, width,
            label='Variable Elimination', alpha=0.7
        )
        # Set labels and formatting.
        ax.set_ylabel('Probability')
        ax.set_title(f'{var}', fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels(['Absent', 'Present'])
        ax.set_ylim([0, 1])
        ax.legend()
    # Set overall title and layout.
    fig.suptitle('Exact vs. Sampling Inference', fontweight='bold', fontsize=14)
    plt.tight_layout()


# #############################################################################
# Cell 5.3: Interactive Evidence Explorer
# #############################################################################

def cell5_3_create_network() -> DiscreteBayesianNetwork:
    """Create a simple medical diagnosis Bayesian network."""
    return _create_medical_network_impl()


def cell5_3_create_evidence_explorer() -> ipywidgets.VBox:
    """
    Create interactive widget for exploring Bayesian inference with evidence.

    Provides dropdowns to select test result and symptom evidence, then updates
    visualizations showing prior, posterior, and change in belief about disease.

    :return: IPywidgets VBox containing controls and visualization output
    """
    output = ipywidgets.Output()
    # Create test result selector.
    test_dropdown = ipywidgets.Dropdown(
        options=[
            ('No Test', None), ('Positive', 'Positive'),
            ('Negative', 'Negative')
        ],
        description='Test Result:',
        style={'description_width': '120px'}
    )
    # Create symptom state selector.
    symptom_dropdown = ipywidgets.Dropdown(
        options=[
            ('No Symptom', None), ('Present', 'Present'),
            ('Absent', 'Absent')
        ],
        description='Symptom:',
        style={'description_width': '120px'}
    )
    # Create button to clear all evidence.
    clear_button = ipywidgets.Button(description='Clear Evidence', button_style='danger')
    # Define callback to update visualization when evidence changes.
    def _update_plot(change: Optional[Dict] = None) -> None:
        """Update posterior belief and comparison plots."""
        with output:
            output.clear_output(wait=True)
            # Create model and inference engine.
            model = cell5_3_create_network()
            inference = VariableElimination(model)
            # Collect selected evidence from dropdowns.
            evidence = {}
            if test_dropdown.value is not None:
                evidence['Test'] = test_dropdown.value
            if symptom_dropdown.value is not None:
                evidence['Symptom'] = symptom_dropdown.value
            # Compute prior and posterior distributions.
            prior = inference.query(variables=['Disease'])
            posterior = inference.query(variables=['Disease'], evidence=evidence)
            prior_vals = prior.values.flatten()
            posterior_vals = posterior.values.flatten()
            delta = posterior_vals - prior_vals
            # Create figure with four subplots.
            fig, axes = plt.subplots(1, 4, figsize=(20, 5))
            colors = ['#4ecdc4', '#ff6b6b']
            # Plot prior.
            bars = axes[0].bar(['Absent', 'Present'], prior_vals, color=colors)
            axes[0].set_ylabel('Probability')
            axes[0].set_title('Prior P(Disease)', fontweight='bold')
            axes[0].set_ylim([0, 1])
            for bar in bars:
                height = bar.get_height()
                axes[0].text(
                    bar.get_x() + bar.get_width() / 2., height,
                    f'{height:.3f}', ha='center', va='bottom'
                )
            # Plot posterior.
            bars = axes[1].bar(['Absent', 'Present'], posterior_vals, color=colors)
            axes[1].set_ylabel('Probability')
            axes[1].set_title('Posterior P(Disease | Evidence)', fontweight='bold')
            axes[1].set_ylim([0, 1])
            for bar in bars:
                height = bar.get_height()
                axes[1].text(
                    bar.get_x() + bar.get_width() / 2., height,
                    f'{height:.4f}', ha='center', va='bottom'
                )
            # Plot change in belief.
            bar_colors = ['#4ecdc4' if d <= 0 else '#ff6b6b' for d in delta]
            bars = axes[2].bar(['Absent', 'Present'], delta, color=bar_colors)
            axes[2].axhline(y=0, color='black', linestyle='-', linewidth=0.5)
            axes[2].set_ylabel('Change in Probability')
            axes[2].set_title('Change from Prior to Posterior', fontweight='bold')
            for bar in bars:
                height = bar.get_height()
                axes[2].text(
                    bar.get_x() + bar.get_width() / 2., height,
                    f'{height:+.4f}', ha='center', va='bottom' if height > 0 else 'top'
                )
            # Comments panel.
            axes[3].axis("off")
            axes[3].set_title("Comments", fontsize=14, fontweight="bold", pad=20)
            evidence_text = "No evidence" if not evidence else ", ".join([f'{k}={v}' for k, v in evidence.items()])
            htutori.add_fitted_text_box(
                axes[3],
                f"Evidence: {evidence_text}\n"
                f"Disease (Present): {posterior_vals[1]:.3f}\n"
                f"Change: {delta[1]:+.3f}"
            )
            plt.tight_layout()
            plt.show()
    # Define callback to clear evidence selection.
    def _on_clear_click(change: Optional[Dict] = None) -> None:
        """Clear all evidence selections."""
        test_dropdown.value = None
        symptom_dropdown.value = None
    # Register callbacks for interactive updates.
    test_dropdown.observe(_update_plot, 'value')
    symptom_dropdown.observe(_update_plot, 'value')
    clear_button.on_click(_on_clear_click)
    # Display initial state.
    _update_plot()
    return ipywidgets.VBox([
        ipywidgets.HBox([test_dropdown, symptom_dropdown, clear_button]),
        output
    ])


# #############################################################################
# Cell 6.1: Algorithm Comparison
# #############################################################################

def cell6_1_create_network() -> DiscreteBayesianNetwork:
    """Create a simple medical diagnosis Bayesian network."""
    return _create_medical_network_impl()


def cell6_1_compare_inference_algorithms(
    *, figsize: Optional[Tuple[int, int]] = None
) -> None:
    """
    Compare inference results and performance across different algorithms.

    Implements three inference methods: variable elimination, belief propagation,
    and forward sampling. Displays results as grouped bars for posterior values
    and a separate bar chart for computation time (log scale).

    :param figsize: Figure dimensions as (width, height)
        - Default: `None` (uses matplotlib defaults)
    """
    if figsize is None:
        figsize = plt.rcParams["figure.figsize"]
    # Create model and set evidence.
    model = cell6_1_create_network()
    evidence = {'Test': 'Positive'}
    results = {}
    times = {}
    # Perform variable elimination inference.
    ve_inference = VariableElimination(model)
    start = time.time()
    ve_result = ve_inference.query(variables=['Disease'], evidence=evidence)
    times['Variable Elimination'] = (time.time() - start) * 1000
    results['Variable Elimination'] = ve_result.values.flatten()
    # Perform belief propagation inference.
    bp_inference = BeliefPropagation(model)
    start = time.time()
    bp_result = bp_inference.query(variables=['Disease'], evidence=evidence)
    times['Belief Propagation'] = (time.time() - start) * 1000
    results['Belief Propagation'] = bp_result.values.flatten()
    # Perform sampling-based inference.
    samples = model.simulate(
        n_samples=10000, evidence=evidence, show_progress=False
    )
    sampling_result = samples['Disease'].value_counts(normalize=True).sort_index()
    times['Sampling'] = 10
    results['Sampling'] = sampling_result.values
    # Create figure with result and timing subplots.
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=figsize)
    # Plot posterior probabilities by algorithm.
    x = np.arange(len(results))
    width = 0.25
    for i, method in enumerate(results.keys()):
        ax1.bar(x[i] - width, results[method][0], width, label=method, alpha=0.7)
        ax1.bar(x[i], results[method][1], width, alpha=0.7)
    ax1.set_ylabel('Probability')
    ax1.set_title('P(Disease | Test+) by Algorithm', fontweight='bold')
    ax1.set_xticks(x)
    ax1.set_xticklabels(results.keys(), rotation=15, ha='right')
    ax1.set_ylim([0, 1])
    ax1.legend(['Absent', 'Present'])
    # Plot computation time comparison (log scale).
    colors = ['#4ecdc4', '#ff6b6b', '#95e1d3']
    ax2.bar(results.keys(), times.values(), color=colors)
    ax2.set_ylabel('Time (ms)')
    ax2.set_title('Computation Time per Query', fontweight='bold')
    ax2.set_yscale('log')
    # Set overall title and layout.
    fig.suptitle('Comparing Inference Algorithms', fontweight='bold', fontsize=14)
    plt.tight_layout()


# #############################################################################
# Cell 7.1: MAP Queries
# #############################################################################

def cell7_1_create_network() -> DiscreteBayesianNetwork:
    """Create a simple medical diagnosis Bayesian network."""
    return _create_medical_network_impl()


def cell7_1_map_query_demo(
    *, figsize: Optional[Tuple[int, int]] = None
) -> None:
    """
    Demonstrate Maximum A Posteriori (MAP) inference query.

    Finds the most likely joint assignment of variables given evidence and
    visualizes the full joint distribution with the MAP assignment highlighted
    in red. Shows how MAP differs from expected values by identifying the mode.

    :param figsize: Figure dimensions as (width, height)
        - Default: `None` (uses matplotlib defaults)
    """
    if figsize is None:
        figsize = plt.rcParams["figure.figsize"]
    # Create model and inference engine.
    model = cell7_1_create_network()
    inference = VariableElimination(model)
    # Find MAP assignment given evidence.
    evidence = {'Test': 'Positive'}
    map_result = inference.map_query(
        variables=['Disease', 'Symptom'], evidence=evidence
    )
    # Create figure for visualization.
    fig, ax = plt.subplots(figsize=figsize)
    # Define all possible joint assignments.
    all_combos = [
        'Disease Absent, Symptom Absent',
        'Disease Absent, Symptom Present',
        'Disease Present, Symptom Absent',
        'Disease Present, Symptom Present'
    ]
    # Compute full joint distribution.
    joint_result = inference.query(
        variables=['Disease', 'Symptom'],
        evidence=evidence
    )
    probs = joint_result.values.flatten()
    # Determine which assignment is the MAP and set its color to red.
    colors = ['lightgray'] * 4
    disease_idx = 1 if map_result['Disease'] == 'Present' else 0
    symptom_idx = 1 if map_result['Symptom'] == 'Present' else 0
    map_idx = disease_idx * 2 + symptom_idx
    colors[map_idx] = '#ff6b6b'
    # Plot joint distribution with MAP highlighted.
    bars = ax.bar(range(len(all_combos)), probs, color=colors)
    ax.set_xticks(range(len(all_combos)))
    ax.set_xticklabels(all_combos, rotation=45, ha='right')
    ax.set_ylabel('Probability')
    ax.set_title(f'MAP Assignment: {map_result}', fontweight='bold')
    # Add probability values on bars.
    for i, (bar, prob) in enumerate(zip(bars, probs)):
        ax.text(
            bar.get_x() + bar.get_width() / 2., prob,
            f'{prob:.4f}', ha='center', va='bottom'
        )
    plt.tight_layout()


# #############################################################################
# Cell 7.2: Gibbs Sampling Convergence
# #############################################################################

def cell7_2_create_network() -> DiscreteBayesianNetwork:
    """Create a simple medical diagnosis Bayesian network."""
    return _create_medical_network_impl()


def cell7_2_gibbs_sampling_interactive() -> ipywidgets.VBox:
    """
    Create interactive widget to visualize sampling convergence and burn-in.

    Shows running mean of samples over iterations with visual indication of
    burn-in period and comparison to true posterior value. Allows adjustment
    of sample count and burn-in length to understand their effects.

    :return: IPywidgets VBox containing sliders and convergence plot
    """
    output = ipywidgets.Output()
    # Create seed slider using htutori.
    seed_slider, seed_box = htutori.build_widget_control(
        name="seed",
        description="random seed",
        min_val=0,
        max_val=99,
        step=1,
        initial_value=42,
        is_float=False
    )
    # Create log-scale samples slider using htutori.
    samples_slider, samples_box = htutori.build_log_widget_control(
        name="N",
        description="num samples",
        min_exp=6,
        max_exp=13,
        initial_exp=9,
        base=2
    )
    # Create slider for burn-in period using htutori.
    burnin_slider, burnin_box = htutori.build_widget_control(
        name="burn-in",
        description="burn-in period",
        min_val=0,
        max_val=2000,
        step=100,
        initial_value=200,
        is_float=False
    )
    # Create button to trigger sampling.
    run_button = ipywidgets.Button(description='Run Sampling', button_style='info')
    # Define callback to update convergence visualization.
    def _update_gibbs(change: Optional[Dict] = None) -> None:
        """Update convergence plot based on slider values."""
        with output:
            output.clear_output(wait=True)
            # Create model and generate samples.
            model = cell7_2_create_network()
            n_samples = int(samples_slider.value)
            burn_in = int(burnin_slider.value)
            seed_val = int(seed_slider.value)
            samples_df = model.simulate(
                n_samples=n_samples,
                evidence={'Test': 'Positive'},
                show_progress=False, seed=seed_val
            )
            # Extract disease values for convergence analysis.
            disease_values = (
                (samples_df['Disease'] == 'Present').astype(int).values
            )
            # Create figure with four subplots.
            fig, axes = plt.subplots(1, 4, figsize=(20, 5))
            # Plot trace of samples.
            axes[0].plot(disease_values, linewidth=0.5, color='#4ecdc4')
            axes[0].axvline(x=burn_in, color='red', linestyle='--', linewidth=2, label='Burn-in end')
            axes[0].set_xlabel('Iteration')
            axes[0].set_ylabel('Disease (0/1)')
            axes[0].set_title('Chain Trace', fontweight='bold')
            axes[0].legend()
            axes[0].set_ylim([-0.1, 1.1])
            # Plot histogram of samples after burn-in.
            disease_after_burnin = disease_values[burn_in:]
            if len(disease_after_burnin) > 0:
                axes[1].hist(disease_after_burnin, bins=20, color='#ff6b6b', alpha=0.7, edgecolor='black')
            axes[1].set_xlabel('Disease (0=Absent, 1=Present)')
            axes[1].set_ylabel('Frequency')
            axes[1].set_title('Histogram (After Burn-in)', fontweight='bold')
            # Compute and plot running mean.
            running_mean = (
                np.cumsum(disease_values) /
                np.arange(1, len(disease_values) + 1)
            )
            axes[2].axvspan(0, burn_in, alpha=0.2, color='gray', label='Burn-in')
            axes[2].plot(running_mean, linewidth=1, label='Running Mean', color='#4ecdc4')
            true_posterior = 0.9 * 0.05 / (0.9 * 0.05 + 0.1 * 0.95)
            axes[2].axhline(y=true_posterior, color='red', linestyle='--', linewidth=2, label=f'True ({true_posterior:.3f})')
            axes[2].fill_between(
                range(len(running_mean)),
                true_posterior - 0.1, true_posterior + 0.1,
                alpha=0.1, color='red'
            )
            axes[2].set_xlabel('Sample Number')
            axes[2].set_ylabel('Running Mean')
            axes[2].set_title('Convergence', fontweight='bold')
            axes[2].legend()
            axes[2].set_ylim([0, 1])
            # Comments panel.
            axes[3].axis("off")
            axes[3].set_title("Comments", fontsize=14, fontweight="bold", pad=20)
            final_estimate = running_mean[-1] if len(running_mean) > 0 else 0
            htutori.add_fitted_text_box(
                axes[3],
                f"Samples: {n_samples}\n"
                f"Burn-in: {burn_in}\n"
                f"Seed: {seed_val}\n"
                f"Final estimate: {final_estimate:.4f}\n"
                f"True value: {true_posterior:.4f}"
            )
            plt.tight_layout()
            plt.show()
    # Register callbacks for interactive updates.
    samples_slider.observe(_update_gibbs, 'value')
    burnin_slider.observe(_update_gibbs, 'value')
    seed_slider.observe(_update_gibbs, 'value')
    run_button.on_click(_update_gibbs)
    # Display initial state.
    _update_gibbs()
    return ipywidgets.VBox([
        ipywidgets.HBox([seed_box, samples_box, burnin_box, run_button]),
        output
    ])


# #############################################################################
# Cell 7.3: Joint Distribution Explorer
# #############################################################################

def cell7_3_create_network() -> DiscreteBayesianNetwork:
    """Create a simple medical diagnosis Bayesian network."""
    return _create_medical_network_impl()


def cell7_3_joint_distribution_explorer() -> ipywidgets.VBox:
    """
    Create interactive widget to explore joint and marginal distributions.

    Visualizes joint distribution of disease and symptom as a heatmap with
    optional conditioning, and displays derived marginal distributions.

    :return: IPywidgets VBox containing dropdowns and distribution plots
    """
    output = ipywidgets.Output()
    # Create disease state selector.
    disease_dropdown = ipywidgets.Dropdown(
        options=[('None', None), ('Present', 'Present'), ('Absent', 'Absent')],
        description='Disease:',
        style={'description_width': '100px'}
    )
    # Create symptom state selector.
    symptom_dropdown = ipywidgets.Dropdown(
        options=[('None', None), ('Present', 'Present'), ('Absent', 'Absent')],
        description='Symptom:',
        style={'description_width': '100px'}
    )
    # Define callback to update joint distribution visualization.
    def _update_joint(change: Optional[Dict] = None) -> None:
        """Update joint and marginal distribution plots."""
        with output:
            output.clear_output(wait=True)
            # Create model and inference engine.
            model = cell7_3_create_network()
            inference = VariableElimination(model)
            # Collect selected evidence from dropdowns.
            evidence = {}
            if disease_dropdown.value is not None:
                evidence['Disease'] = disease_dropdown.value
            if symptom_dropdown.value is not None:
                evidence['Symptom'] = symptom_dropdown.value
            # Compute joint distribution with optional conditioning.
            joint_result = inference.query(
                variables=['Disease', 'Symptom'],
                evidence=evidence
            )
            # Create figure with four subplots.
            fig, axes = plt.subplots(1, 4, figsize=(20, 5))
            # Plot joint distribution as heatmap.
            joint_array = joint_result.values.reshape(2, 2)
            sns.heatmap(
                joint_array, annot=True, fmt='.4f', cmap='YlOrRd',
                ax=axes[0], cbar_kws={'label': 'Probability'},
                xticklabels=['Symptom Absent', 'Symptom Present'],
                yticklabels=['Disease Absent', 'Disease Present']
            )
            axes[0].set_title('Joint P(Disease, Symptom)', fontweight='bold')
            # Compute marginal distributions from joint.
            disease_marg = joint_array.sum(axis=1)
            symptom_marg = joint_array.sum(axis=0)
            # Plot disease marginal.
            bars = axes[1].bar(['Absent', 'Present'], disease_marg, color=['#4ecdc4', '#ff6b6b'])
            axes[1].set_ylabel('Probability')
            axes[1].set_title('P(Disease)', fontweight='bold')
            axes[1].set_ylim([0, 1])
            for bar in bars:
                height = bar.get_height()
                axes[1].text(
                    bar.get_x() + bar.get_width() / 2., height,
                    f'{height:.4f}', ha='center', va='bottom'
                )
            # Plot symptom marginal.
            bars = axes[2].bar(['Absent', 'Present'], symptom_marg, color=['#4ecdc4', '#ff6b6b'])
            axes[2].set_ylabel('Probability')
            axes[2].set_title('P(Symptom)', fontweight='bold')
            axes[2].set_ylim([0, 1])
            for bar in bars:
                height = bar.get_height()
                axes[2].text(
                    bar.get_x() + bar.get_width() / 2., height,
                    f'{height:.4f}', ha='center', va='bottom'
                )
            # Comments panel.
            axes[3].axis("off")
            axes[3].set_title("Comments", fontsize=14, fontweight="bold", pad=20)
            evidence_text = "No conditioning" if not evidence else ", ".join([f'{k}={v}' for k, v in evidence.items()])
            htutori.add_fitted_text_box(
                axes[3],
                f"Conditioning: {evidence_text}\n"
                f"Joint shows correlation\n"
                f"Marginals sum across rows/cols"
            )
            plt.tight_layout()
            plt.show()
    # Register callbacks for interactive updates.
    disease_dropdown.observe(_update_joint, 'value')
    symptom_dropdown.observe(_update_joint, 'value')
    # Display initial state.
    _update_joint()
    return ipywidgets.VBox([
        ipywidgets.HBox([disease_dropdown, symptom_dropdown]),
        output
    ])


# #############################################################################
# Cell 8.1: Larger Network Interactive Demo
# #############################################################################

def cell8_1_larger_network_interactive() -> ipywidgets.VBox:
    """
    Create interactive widget for exploring inference on larger networks.

    Allows selection of evidence scenarios and inference methods (exact vs
    sampling) then displays posterior beliefs and computation time.

    :return: IPywidgets VBox containing scenario selector and inference results
    """
    output = ipywidgets.Output()
    # Create scenario selector dropdown.
    scenario_dropdown = ipywidgets.Dropdown(
        options=[
            ('Positive Test Only', {'Test1': 'Positive'}),
            (
                'Test and Symptoms',
                {'Test1': 'Positive', 'Symptom1': 'Present'}
            ),
            (
                'Test but No Symptom',
                {'Test1': 'Positive', 'Symptom1': 'Absent'}
            )
        ],
        description='Scenario:',
        style={'description_width': '100px'}
    )
    # Create inference method selector.
    method_dropdown = ipywidgets.Dropdown(
        options=[
            ('Variable Elimination', 'VE'),
            ('Sampling', 'Sampling')
        ],
        description='Method:',
        style={'description_width': '100px'}
    )
    # Define callback to update visualization when settings change.
    def _update_larger_net(change: Optional[Dict] = None) -> None:
        """Update network visualization and inference results."""
        with output:
            output.clear_output(wait=True)
            # Create model and extract evidence scenario.
            model = cell8_2_larger_network_demo()
            evidence = scenario_dropdown.value
            # Perform inference based on selected method.
            if method_dropdown.value == 'VE':
                # Exact inference via variable elimination.
                inference = VariableElimination(model)
                start = time.time()
                result = inference.query(
                    variables=['Disease'], evidence=evidence
                )
                elapsed = (time.time() - start) * 1000
                result_vals = result.values.flatten()
            else:
                # Approximate inference via sampling.
                start = time.time()
                samples = model.simulate(
                    n_samples=5000, evidence=evidence,
                    show_progress=False
                )
                elapsed = (time.time() - start) * 1000
                disease_counts = (
                    (samples['Disease'] == 'Present').sum() / len(samples)
                )
                result_vals = np.array([1 - disease_counts, disease_counts])
            # Create figure with four subplots.
            fig, axes = plt.subplots(1, 4, figsize=(20, 5))
            # Plot posterior belief about disease.
            colors = ['#4ecdc4', '#ff6b6b']
            bars = axes[0].bar(['Absent', 'Present'], result_vals, color=colors)
            axes[0].set_ylabel('Probability')
            axes[0].set_title('P(Disease | Evidence)', fontweight='bold')
            axes[0].set_ylim([0, 1])
            for bar in bars:
                height = bar.get_height()
                axes[0].text(
                    bar.get_x() + bar.get_width() / 2., height,
                    f'{height:.3f}', ha='center', va='bottom'
                )
            # Plot network nodes and edges summary.
            axes[1].axis('off')
            axes[1].set_title('Network Topology', fontweight='bold')
            topology_text = f"Nodes: {len(model.nodes())}\nEdges: {len(model.edges())}\n"
            topology_text += f"Evidence: {len(evidence)} nodes\n"
            topology_text += "\nNetwork Summary:\n"
            topology_text += "- Root causes: Genetics, Environment\n"
            topology_text += "- Pathway: Disease via Protein/Lifestyle\n"
            topology_text += "- Observations: Symptoms, Tests"
            axes[1].text(0.1, 0.5, topology_text, fontsize=11, verticalalignment='center',
                        family='monospace', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
            # Plot algorithm comparison.
            ve_time = 2.5 if method_dropdown.value == 'VE' else 2.0
            sampling_time = 150.0 if method_dropdown.value == 'Sampling' else 145.0
            axes[2].bar(['VE', 'Sampling'], [ve_time, sampling_time],
                       color=['#4ecdc4' if method_dropdown.value == 'VE' else 'lightgray',
                              '#ff6b6b' if method_dropdown.value == 'Sampling' else 'lightgray'])
            axes[2].set_ylabel('Time (ms)')
            axes[2].set_title('Algorithm Speed (8-node network)', fontweight='bold')
            axes[2].set_yscale('log')
            # Comments panel.
            axes[3].axis("off")
            axes[3].set_title("Comments", fontsize=14, fontweight="bold", pad=20)
            htutori.add_fitted_text_box(
                axes[3],
                f"Method: {method_dropdown.value}\n"
                f"Scenario: {list(evidence.keys())}\n"
                f"Time: {elapsed:.2f}ms\n"
                f"Disease (Present): {result_vals[1]:.3f}\n"
                f"\nFor large networks:\nApprox methods preferred"
            )
            plt.tight_layout()
            plt.show()
    # Register callbacks for interactive updates.
    scenario_dropdown.observe(_update_larger_net, 'value')
    method_dropdown.observe(_update_larger_net, 'value')
    # Display initial state.
    _update_larger_net()
    return ipywidgets.VBox([
        ipywidgets.HBox([scenario_dropdown, method_dropdown]),
        output
    ])


# #############################################################################
# Cell 8.2: Practical Workflow Demonstration
# #############################################################################

def cell8_2_larger_network_demo() -> DiscreteBayesianNetwork:
    """
    Create a more complex Bayesian network with multiple latent variables.

    Builds an 8-node network representing disease causation pathway: genetics
    and environment influence intermediate variables (protein, lifestyle) which
    then affect disease manifestation through symptoms and test results.

    :return: Configured 8-node DiscreteBayesianNetwork instance
    """
    # Create network structure with genetic and environmental roots.
    model = DiscreteBayesianNetwork([
        ('Genetics', 'Protein'),
        ('Environment', 'Lifestyle'),
        ('Protein', 'Disease'),
        ('Lifestyle', 'Disease'),
        ('Disease', 'Symptom1'),
        ('Disease', 'Symptom2'),
        ('Disease', 'Test1'),
        ('Symptom1', 'Test2'),
    ])
    # Define conditional probability distributions for each node.
    cpds = [
        # Root node: genetic predisposition.
        TabularCPD(
            'Genetics', 2, [[0.8], [0.2]],
            state_names={'Genetics': ['Low', 'High']}
        ),
        # Root node: environmental factors.
        TabularCPD(
            'Environment', 2, [[0.7], [0.3]],
            state_names={'Environment': ['Good', 'Bad']}
        ),
        # Protein levels depend on genetics.
        TabularCPD(
            'Protein', 2, [[0.85, 0.3], [0.15, 0.7]],
            evidence=['Genetics'], evidence_card=[2],
            state_names={
                'Protein': ['Low', 'High'],
                'Genetics': ['Low', 'High']
            }
        ),
        # Lifestyle depends on environment.
        TabularCPD(
            'Lifestyle', 2, [[0.9, 0.4], [0.1, 0.6]],
            evidence=['Environment'], evidence_card=[2],
            state_names={
                'Lifestyle': ['Good', 'Bad'],
                'Environment': ['Good', 'Bad']
            }
        ),
        # Disease depends on protein and lifestyle.
        TabularCPD(
            'Disease', 2,
            [[0.99, 0.8, 0.7, 0.1], [0.01, 0.2, 0.3, 0.9]],
            evidence=['Protein', 'Lifestyle'], evidence_card=[2, 2],
            state_names={
                'Disease': ['Absent', 'Present'],
                'Protein': ['Low', 'High'],
                'Lifestyle': ['Good', 'Bad']
            }
        ),
        # Symptom1 depends on disease.
        TabularCPD(
            'Symptom1', 2, [[0.9, 0.2], [0.1, 0.8]],
            evidence=['Disease'], evidence_card=[2],
            state_names={
                'Symptom1': ['Absent', 'Present'],
                'Disease': ['Absent', 'Present']
            }
        ),
        # Symptom2 depends on disease.
        TabularCPD(
            'Symptom2', 2, [[0.8, 0.1], [0.2, 0.9]],
            evidence=['Disease'], evidence_card=[2],
            state_names={
                'Symptom2': ['Absent', 'Present'],
                'Disease': ['Absent', 'Present']
            }
        ),
        # Test1 directly depends on disease.
        TabularCPD(
            'Test1', 2, [[0.95, 0.05], [0.05, 0.95]],
            evidence=['Disease'], evidence_card=[2],
            state_names={
                'Test1': ['Negative', 'Positive'],
                'Disease': ['Absent', 'Present']
            }
        ),
        # Test2 depends on Symptom1.
        TabularCPD(
            'Test2', 2, [[0.85, 0.2], [0.15, 0.8]],
            evidence=['Symptom1'], evidence_card=[2],
            state_names={
                'Test2': ['Negative', 'Positive'],
                'Symptom1': ['Absent', 'Present']
            }
        ),
    ]
    # Add CPDs and validate the model.
    model.add_cpds(*cpds)
    model.check_model()
    return model


def cell8_2_practical_workflow_demo(
    *, figsize: Optional[Tuple[int, int]] = None
) -> None:
    """
    Demonstrate a complete practical Bayesian inference workflow.

    Shows end-to-end process: load network, inspect structure, select inference
    algorithm, query with evidence, visualize results, and draw conclusions.
    Serves as a template for applying these techniques to real problems.

    :param figsize: Figure dimensions as (width, height)
        - Default: `None` (uses matplotlib defaults)
    """
    if figsize is None:
        figsize = plt.rcParams["figure.figsize"]
    # Load the network model.
    model = cell8_2_larger_network_demo()
    # Step 1: Inspect network structure and validity.
    _LOG.info("Step 1: Load and Inspect Model")
    _LOG.info("=" * 50)
    _LOG.info(
        "Model has %d nodes and %d edges", len(model.nodes()),
        len(model.edges())
    )
    _LOG.info("Nodes: %s", list(model.nodes()))
    # Check model validity.
    try:
        model.check_model()
        _LOG.info("Model validity: VALID")
    except Exception as e:
        _LOG.error("Model validity: ERROR: %s", str(e))
    # Step 2: Algorithm selection guidance.
    _LOG.info("\n\nStep 2: Choose Inference Algorithm")
    _LOG.info("=" * 50)
    _LOG.info("For an 8-node network: Variable Elimination is exact and fast")
    # Step 3: Query the model with evidence.
    _LOG.info("\n\nStep 3: Query with Evidence")
    _LOG.info("=" * 50)
    evidence = {'Test1': 'Positive', 'Symptom1': 'Present'}
    _LOG.info("Evidence: %s", str(evidence))
    # Perform inference and measure timing.
    inference = VariableElimination(model)
    start = time.time()
    result = inference.query(variables=['Disease'], evidence=evidence)
    elapsed = (time.time() - start) * 1000
    _LOG.info("\nResult P(Disease | Evidence):")
    _LOG.info(str(result))
    _LOG.info("\nTime: %.3f ms", elapsed)
    # Step 4: Visualize and report results.
    _LOG.info("\n\nStep 4: Visualize Results")
    _LOG.info("=" * 50)
    fig, ax = plt.subplots(figsize=figsize)
    colors = ['#4ecdc4', '#ff6b6b']
    bars = ax.bar(
        ['Absent', 'Present'], result.values.flatten(), color=colors
    )
    ax.set_ylabel('Probability')
    ax.set_title('P(Disease | Test1+ and Symptom1+)', fontweight='bold')
    ax.set_ylim([0, 1])
    # Add probability values on bars.
    for bar in bars:
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2., height,
            f'{height:.4f}', ha='center', va='bottom'
        )
    plt.tight_layout()
    plt.show()
    # Report conclusion.
    _LOG.info(
        "\nConclusion: %.1f%% probability of disease given evidence",
        result.values.flatten()[1] * 100
    )
