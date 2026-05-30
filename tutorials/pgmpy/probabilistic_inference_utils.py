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
from ipywidgets import (
    Button,
    Dropdown,
    FloatSlider,
    HBox,
    HTML,
    IntSlider,
    Output,
    ToggleButtons,
    VBox,
)
from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import ApproxInference, BeliefPropagation, VariableElimination
from pgmpy.models import DiscreteBayesianNetwork

import helpers.hdbg as hdbg

_LOG = logging.getLogger(__name__)

warnings.filterwarnings('ignore')


def create_medical_network() -> DiscreteBayesianNetwork:
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


def visualize_network(
    model: DiscreteBayesianNetwork,
    *,
    evidence: Optional[List[str]] = None,
    figsize: Tuple[int, int] = (10, 6),
) -> plt.Figure:
    """
    Visualize Bayesian network structure with optional evidence highlighting.

    Draws the network graph using spring layout with nodes colored based on
    whether they are part of the evidence set. Evidence nodes are highlighted
    in red while other nodes are shown in teal.

    :param model: Bayesian network to visualize
    :param evidence: List of node names to highlight as evidence
        - Default: `None` (no nodes highlighted)
    :param figsize: Figure dimensions as (width, height)
        - Default: `(10, 6)`
    :return: Matplotlib figure object
    """
    # Create figure and axis for visualization.
    fig, ax = plt.subplots(figsize=figsize)
    # Create directed graph from model edges.
    graph = nx.DiGraph()
    graph.add_edges_from(model.edges())
    # Compute spring layout for node positioning.
    pos = nx.spring_layout(graph, k=2, iterations=50)
    # Color nodes based on evidence status.
    node_colors = []
    for node in graph.nodes():
        if evidence and node in evidence:
            node_colors.append('#ff6b6b')
        else:
            node_colors.append('#4ecdc4')
    # Draw network components.
    nx.draw_networkx_nodes(
        graph, pos, node_color=node_colors, node_size=2000, ax=ax
    )
    nx.draw_networkx_labels(
        graph, pos, font_size=10, font_weight='bold', ax=ax
    )
    nx.draw_networkx_edges(
        graph, pos, edge_color='gray', arrows=True,
        arrowsize=20, arrowstyle='->', ax=ax, width=2
    )
    # Set title and remove axes.
    ax.set_title('Bayesian Network Structure', fontsize=14, fontweight='bold')
    ax.axis('off')
    return fig


def display_cpd_tables(model: DiscreteBayesianNetwork) -> None:
    """
    Display conditional probability distribution tables in formatted output.

    Prints each CPD from the model with a header and separator for readability.

    :param model: Bayesian network containing CPDs to display
    """
    _LOG.info("Conditional Probability Tables")
    _LOG.info("=" * 50)
    for cpd in model.get_cpds():
        _LOG.info("%s:", cpd.variable)
        _LOG.info(str(cpd))


def create_cpd_widget(
    *, disease_prior: float = 0.05
) -> VBox:
    """
    Create interactive widget for exploring conditional probability distributions.

    Displays a slider to control disease prior probability and visualizes three
    CPDs as heatmaps: P(Disease), P(Symptom|Disease), and P(Test|Disease).
    Updates automatically when slider value changes.

    :param disease_prior: Initial disease prior probability value
        - Default: `0.05`
    :return: IPywidgets VBox containing slider and visualization output
    """
    output = Output()
    # Create disease prior probability slider.
    slider = FloatSlider(
        value=disease_prior,
        min=0.0,
        max=1.0,
        step=0.01,
        description='P(Disease):',
        style={'description_width': '100px'},
        layout={'width': '400px'}
    )
    # Create disease state toggle button.
    toggle = ToggleButtons(
        options=['None', 'Present', 'Absent'],
        description='Disease:',
        style={'description_width': '100px'}
    )
    # Define callback to update visualization when controls change.
    def _update_display(change: Optional[Dict] = None) -> None:
        """Update CPD heatmaps based on slider and toggle values."""
        with output:
            output.clear_output(wait=True)
            p_disease = slider.value
            # Create figure with three subplots for each CPD.
            fig, axes = plt.subplots(1, 3, figsize=(14, 4))
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
            plt.tight_layout()
            plt.show()
    # Register callbacks for interactive updates.
    slider.observe(_update_display, 'value')
    toggle.observe(_update_display, 'value')
    # Display initial state.
    _update_display()
    return VBox([
        HBox([slider, toggle]),
        output
    ])


def forward_sample_and_plot(
    model: DiscreteBayesianNetwork, *, n_samples: int = 1000
) -> plt.Figure:
    """
    Sample from network prior and visualize marginal distributions.

    Generates samples from the Bayesian network without any evidence and plots
    the resulting marginal probability distribution for each variable as a bar
    chart with annotated values.

    :param model: Bayesian network to sample from
    :param n_samples: Number of samples to generate
        - Default: `1000`
    :return: Matplotlib figure with marginal distribution plots
    """
    # Generate samples from the network prior.
    samples = model.simulate(n_samples=n_samples, show_progress=False)
    # Create figure with one subplot per variable.
    fig, axes = plt.subplots(1, 3, figsize=(14, 4))
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
    return fig


def compare_exact_and_sampling(
    model: DiscreteBayesianNetwork,
) -> plt.Figure:
    """
    Compare exact inference results with sampling-based approximations.

    Performs variable elimination for exact inference and forward sampling,
    then displays both results side-by-side as grouped bar charts for each
    variable to visualize the approximation quality.

    :param model: Bayesian network to analyze
    :return: Matplotlib figure with comparative plots
    """
    # Create exact inference engine.
    inference = VariableElimination(model)
    # Generate samples from the network.
    n_samples = 1000
    samples = model.simulate(n_samples=n_samples, show_progress=False)
    # Create figure with one subplot per variable.
    fig, axes = plt.subplots(1, 3, figsize=(14, 4))
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
    return fig


def condition_on_evidence(model: DiscreteBayesianNetwork) -> plt.Figure:
    """
    Visualize how evidence updates beliefs through Bayesian updating.

    Computes and displays three probability distributions: prior belief,
    posterior after positive test, and posterior after negative test. Shows
    how the same test result differently impacts belief depending on outcome.

    :param model: Bayesian network for inference
    :return: Matplotlib figure with prior and posterior plots
    """
    # Create exact inference engine.
    inference = VariableElimination(model)
    # Create figure with three subplots for prior and posteriors.
    fig, axes = plt.subplots(1, 3, figsize=(14, 4))
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
    return fig


def create_evidence_explorer() -> VBox:
    """
    Create interactive widget for exploring Bayesian inference with evidence.

    Provides dropdowns to select test result and symptom evidence, then updates
    a joint visualization showing the network structure and the posterior belief
    about disease given the selected evidence combination.

    :return: IPywidgets VBox containing controls and visualization output
    """
    output = Output()
    # Create test result selector.
    test_dropdown = Dropdown(
        options=[
            ('No Test', None), ('Positive', 'Positive'),
            ('Negative', 'Negative')
        ],
        description='Test Result:',
        style={'description_width': '120px'}
    )
    # Create symptom state selector.
    symptom_dropdown = Dropdown(
        options=[
            ('No Symptom', None), ('Present', 'Present'),
            ('Absent', 'Absent')
        ],
        description='Symptom:',
        style={'description_width': '120px'}
    )
    # Create button to clear all evidence.
    clear_button = Button(description='Clear Evidence', button_style='danger')
    # Define callback to update visualization when evidence changes.
    def _update_plot(change: Optional[Dict] = None) -> None:
        """Update network visualization and posterior belief plot."""
        with output:
            output.clear_output(wait=True)
            # Create model and inference engine.
            model = create_medical_network()
            inference = VariableElimination(model)
            # Collect selected evidence from dropdowns.
            evidence = {}
            if test_dropdown.value is not None:
                evidence['Test'] = test_dropdown.value
            if symptom_dropdown.value is not None:
                evidence['Symptom'] = symptom_dropdown.value
            # Compute posterior disease belief given evidence.
            result = inference.query(variables=['Disease'], evidence=evidence)
            # Create figure with network visualization and belief plot.
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
            visualize_network(model, evidence=list(evidence.keys()))
            plt.sca(ax1)
            # Plot posterior belief about disease.
            colors = ['#4ecdc4', '#ff6b6b']
            bars = ax2.bar(
                ['Absent', 'Present'], result.values.flatten(), color=colors
            )
            ax2.set_ylabel('Probability')
            ax2.set_title('P(Disease | Evidence)', fontweight='bold')
            ax2.set_ylim([0, 1])
            # Add probability values on bars.
            for bar in bars:
                height = bar.get_height()
                ax2.text(
                    bar.get_x() + bar.get_width() / 2., height,
                    f'{height:.4f}', ha='center', va='bottom'
                )
            # Set title with evidence description if any.
            if evidence:
                evidence_str = ', '.join([f'{k}={v}' for k, v in evidence.items()])
                fig.suptitle(
                    f'Evidence: {evidence_str}', fontweight='bold', fontsize=12
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
    return VBox([
        HBox([test_dropdown, symptom_dropdown, clear_button]),
        output
    ])


def compare_inference_algorithms() -> plt.Figure:
    """
    Compare inference results and performance across different algorithms.

    Implements three inference methods: variable elimination, belief propagation,
    and forward sampling. Displays results as grouped bars for posterior values
    and a separate bar chart for computation time (log scale).

    :return: Matplotlib figure with comparison plots
    """
    # Create model and set evidence.
    model = create_medical_network()
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
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 4))
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
    return fig


def gibbs_sampling_interactive() -> VBox:
    """
    Create interactive widget to visualize sampling convergence and burn-in.

    Shows running mean of samples over iterations with visual indication of
    burn-in period and comparison to true posterior value. Allows adjustment
    of sample count and burn-in length to understand their effects.

    :return: IPywidgets VBox containing sliders and convergence plot
    """
    output = Output()
    # Create slider for number of samples.
    samples_slider = IntSlider(
        value=1000,
        min=100,
        max=10000,
        step=100,
        description='Samples:',
        style={'description_width': '100px'}
    )
    # Create slider for burn-in period.
    burnin_slider = IntSlider(
        value=200,
        min=0,
        max=2000,
        step=100,
        description='Burn-in:',
        style={'description_width': '100px'}
    )
    # Create button to trigger sampling.
    run_button = Button(description='Run Sampling', button_style='info')
    # Define callback to update convergence visualization.
    def _update_gibbs(change: Optional[Dict] = None) -> None:
        """Update convergence plot based on slider values."""
        with output:
            output.clear_output(wait=True)
            # Create model and generate samples.
            model = create_medical_network()
            n_samples = samples_slider.value
            burn_in = burnin_slider.value
            samples_df = model.simulate(
                n_samples=n_samples,
                evidence={'Test': 'Positive'},
                show_progress=False, seed=42
            )
            # Extract disease values for convergence analysis.
            disease_values = (
                (samples_df['Disease'] == 'Present').astype(int).values
            )
            # Create figure for convergence plot.
            fig, ax = plt.subplots(figsize=(12, 4))
            # Compute and plot running mean of samples.
            running_mean = (
                np.cumsum(disease_values) /
                np.arange(1, len(disease_values) + 1)
            )
            # Highlight burn-in period.
            ax.axvspan(0, burn_in, alpha=0.2, color='gray', label='Burn-in')
            # Plot running mean trajectory.
            ax.plot(
                running_mean, linewidth=1, label='Running Mean',
                color='#4ecdc4'
            )
            # Mark true posterior value.
            true_posterior = 0.9 * 0.05 / (0.9 * 0.05 + 0.1 * 0.95)
            ax.axhline(
                y=true_posterior, color='red', linestyle='--',
                linewidth=2, label=f'True Posterior ({true_posterior:.3f})'
            )
            # Shade region around true posterior.
            ax.fill_between(
                range(len(running_mean)),
                true_posterior - 0.1, true_posterior + 0.1,
                alpha=0.1, color='red'
            )
            # Set labels and formatting.
            ax.set_xlabel('Sample Number')
            ax.set_ylabel('P(Disease=Present | Test+)')
            ax.set_title('Sampling Convergence', fontweight='bold')
            ax.legend()
            ax.set_ylim([0, 1])
            plt.tight_layout()
            plt.show()
    # Register callbacks for interactive updates.
    samples_slider.observe(_update_gibbs, 'value')
    burnin_slider.observe(_update_gibbs, 'value')
    run_button.on_click(_update_gibbs)
    # Display initial state.
    _update_gibbs()
    return VBox([
        HBox([samples_slider, burnin_slider, run_button]),
        output
    ])


def joint_distribution_explorer() -> VBox:
    """
    Create interactive widget to explore joint and marginal distributions.

    Visualizes joint distribution of disease and symptom as a heatmap with
    optional conditioning, and displays derived marginal distributions on a
    dual-axis bar chart to show independence relationships.

    :return: IPywidgets VBox containing dropdowns and distribution plots
    """
    output = Output()
    # Create disease state selector.
    disease_dropdown = Dropdown(
        options=[('None', None), ('Present', 'Present'), ('Absent', 'Absent')],
        description='Disease:',
        style={'description_width': '100px'}
    )
    # Create symptom state selector.
    symptom_dropdown = Dropdown(
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
            model = create_medical_network()
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
            # Create figure with joint and marginal subplots.
            fig, axes = plt.subplots(1, 2, figsize=(12, 4))
            # Plot joint distribution as heatmap.
            joint_array = joint_result.values.reshape(2, 2)
            sns.heatmap(
                joint_array, annot=True, fmt='.4f', cmap='YlOrRd',
                ax=axes[0], cbar_kws={'label': 'Probability'},
                xticklabels=['Symptom Absent', 'Symptom Present'],
                yticklabels=['Disease Absent', 'Disease Present']
            )
            axes[0].set_title(
                'Joint Distribution P(Disease, Symptom)', fontweight='bold'
            )
            # Compute marginal distributions from joint.
            disease_marg = joint_array.sum(axis=1)
            symptom_marg = joint_array.sum(axis=0)
            # Plot marginal distributions on dual-axis bar chart.
            axes[1].bar(
                ['Disease Absent', 'Disease Present'], disease_marg,
                alpha=0.6, label='P(Disease)', color='#4ecdc4'
            )
            ax2 = axes[1].twinx()
            ax2.bar(
                ['Symptom Absent', 'Symptom Present'], symptom_marg,
                alpha=0.6, label='P(Symptom)', color='#ff6b6b'
            )
            # Set labels and formatting.
            axes[1].set_ylabel('P(Disease)')
            ax2.set_ylabel('P(Symptom)')
            axes[1].set_title('Marginal Distributions', fontweight='bold')
            axes[1].set_ylim([0, 1])
            ax2.set_ylim([0, 1])
            plt.tight_layout()
            plt.show()
    # Register callbacks for interactive updates.
    disease_dropdown.observe(_update_joint, 'value')
    symptom_dropdown.observe(_update_joint, 'value')
    # Display initial state.
    _update_joint()
    return VBox([
        HBox([disease_dropdown, symptom_dropdown]),
        output
    ])


def map_query_demo() -> plt.Figure:
    """
    Demonstrate Maximum A Posteriori (MAP) inference query.

    Finds the most likely joint assignment of variables given evidence and
    visualizes the full joint distribution with the MAP assignment highlighted
    in red. Shows how MAP differs from expected values by identifying the mode.

    :return: Matplotlib figure with joint distribution and MAP highlighting
    """
    # Create model and inference engine.
    model = create_medical_network()
    inference = VariableElimination(model)
    # Find MAP assignment given evidence.
    evidence = {'Test': 'Positive'}
    map_result = inference.map_query(
        variables=['Disease', 'Symptom'], evidence=evidence
    )
    # Create figure for visualization.
    fig, ax = plt.subplots(figsize=(10, 4))
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
    return fig


def larger_network_demo() -> DiscreteBayesianNetwork:
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


def larger_network_interactive() -> VBox:
    """
    Create interactive widget for exploring inference on larger networks.

    Allows selection of evidence scenarios and inference methods (exact vs
    sampling) then displays network structure, posterior beliefs, and computation
    time for comparing algorithmic approaches on a more complex network.

    :return: IPywidgets VBox containing scenario selector and inference results
    """
    output = Output()
    # Create scenario selector dropdown.
    scenario_dropdown = Dropdown(
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
    method_dropdown = Dropdown(
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
            model = larger_network_demo()
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
            # Create visualization with network and belief plots.
            fig, axes = plt.subplots(1, 2, figsize=(14, 4))
            visualize_network(model, evidence=list(evidence.keys()))
            plt.sca(axes[0])
            # Plot posterior belief about disease.
            colors = ['#4ecdc4', '#ff6b6b']
            bars = axes[1].bar(['Absent', 'Present'], result_vals, color=colors)
            axes[1].set_ylabel('Probability')
            axes[1].set_title(
                f'P(Disease | Evidence)\nTime: {elapsed:.2f}ms',
                fontweight='bold'
            )
            axes[1].set_ylim([0, 1])
            # Add probability values on bars.
            for bar in bars:
                height = bar.get_height()
                axes[1].text(
                    bar.get_x() + bar.get_width() / 2., height,
                    f'{height:.3f}', ha='center', va='bottom'
                )
            plt.tight_layout()
            plt.show()
    # Register callbacks for interactive updates.
    scenario_dropdown.observe(_update_larger_net, 'value')
    method_dropdown.observe(_update_larger_net, 'value')
    # Display initial state.
    _update_larger_net()
    return VBox([
        HBox([scenario_dropdown, method_dropdown]),
        output
    ])


def practical_workflow_demo() -> None:
    """
    Demonstrate a complete practical Bayesian inference workflow.

    Shows end-to-end process: load network, inspect structure, select inference
    algorithm, query with evidence, visualize results, and draw conclusions.
    Serves as a template for applying these techniques to real problems.
    """
    # Load the network model.
    model = larger_network_demo()
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
    fig, ax = plt.subplots(figsize=(10, 4))
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
