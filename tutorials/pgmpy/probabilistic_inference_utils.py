"""Utility functions for the Probabilistic Inference notebook.

Handles interactive widgets, visualizations, and Bayesian network operations.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
from ipywidgets import FloatSlider, IntSlider, Dropdown, Button, VBox, HBox, HTML, Output, ToggleButtons
from IPython.display import display, HTML as IPhtml
import networkx as nx
from pgmpy.models import DiscreteBayesianNetwork
from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import VariableElimination, BeliefPropagation, ApproxInference
import time
import warnings
warnings.filterwarnings('ignore')


def create_medical_network():
    """Create the medical diagnosis Bayesian network."""
    model = DiscreteBayesianNetwork([
        ('Disease', 'Symptom'),
        ('Disease', 'Test')
    ])

    cpd_disease = TabularCPD(
        'Disease', 2, [[0.95], [0.05]],
        state_names={'Disease': ['Absent', 'Present']}
    )
    cpd_symptom = TabularCPD(
        'Symptom', 2,
        [[0.95, 0.2], [0.05, 0.8]],
        evidence=['Disease'],
        evidence_card=[2],
        state_names={'Symptom': ['Absent', 'Present'], 'Disease': ['Absent', 'Present']}
    )
    cpd_test = TabularCPD(
        'Test', 2,
        [[0.95, 0.1], [0.05, 0.9]],
        evidence=['Disease'],
        evidence_card=[2],
        state_names={'Test': ['Negative', 'Positive'], 'Disease': ['Absent', 'Present']}
    )

    model.add_cpds(cpd_disease, cpd_symptom, cpd_test)
    model.check_model()
    return model


def visualize_network(model, evidence=None, figsize=(10, 6)):
    """Visualize Bayesian network structure."""
    fig, ax = plt.subplots(figsize=figsize)

    G = nx.DiGraph()
    G.add_edges_from(model.edges())

    pos = nx.spring_layout(G, k=2, iterations=50)

    node_colors = []
    for node in G.nodes():
        if evidence and node in evidence:
            node_colors.append('#ff6b6b')
        else:
            node_colors.append('#4ecdc4')

    nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=2000, ax=ax)
    nx.draw_networkx_labels(G, pos, font_size=10, font_weight='bold', ax=ax)
    nx.draw_networkx_edges(G, pos, edge_color='gray', arrows=True,
                           arrowsize=20, arrowstyle='->', ax=ax, width=2)

    ax.set_title('Bayesian Network Structure', fontsize=14, fontweight='bold')
    ax.axis('off')

    return fig


def display_cpd_tables(model):
    """Display CPD tables in formatted HTML."""
    print("Conditional Probability Tables\n" + "="*50)
    for cpd in model.get_cpds():
        print(f"\n{cpd.variable}:")
        print(cpd)
        print()


def create_cpd_widget(disease_prior=0.05):
    """Create interactive CPD visualization with slider."""
    output = Output()

    slider = FloatSlider(
        value=disease_prior,
        min=0.0,
        max=1.0,
        step=0.01,
        description='P(Disease):',
        style={'description_width': '100px'},
        layout={'width': '400px'}
    )

    toggle = ToggleButtons(
        options=['None', 'Present', 'Absent'],
        description='Disease:',
        style={'description_width': '100px'}
    )

    def update_display(change=None):
        with output:
            output.clear_output(wait=True)
            p_disease = slider.value

            fig, axes = plt.subplots(1, 3, figsize=(14, 4))

            data_prior = pd.DataFrame(
                {'Present': [p_disease], 'Absent': [1 - p_disease]},
                index=pd.Index(['P(Disease)'])
            )

            sns.heatmap(data_prior, annot=True, fmt='.3f', cmap='RdYlGn',
                       vmin=0, vmax=1, ax=axes[0], cbar=False)
            axes[0].set_title('P(Disease)', fontweight='bold')

            symptom_given_disease = pd.DataFrame(
                {'Symptom': [0.05, 0.8], 'No Symptom': [0.95, 0.2]},
                index=pd.Index(['Disease', 'No Disease'])
            )

            sns.heatmap(symptom_given_disease, annot=True, fmt='.2f', cmap='Blues',
                       vmin=0, vmax=1, ax=axes[1], cbar=False)
            axes[1].set_title('P(Symptom | Disease)', fontweight='bold')

            test_given_disease = pd.DataFrame(
                {'Positive': [0.05, 0.9], 'Negative': [0.95, 0.1]},
                index=pd.Index(['Disease', 'No Disease'])
            )

            sns.heatmap(test_given_disease, annot=True, fmt='.2f', cmap='Oranges',
                       vmin=0, vmax=1, ax=axes[2], cbar=False)
            axes[2].set_title('P(Test | Disease)', fontweight='bold')

            plt.tight_layout()
            plt.show()

    slider.observe(update_display, 'value')
    toggle.observe(update_display, 'value')

    update_display()

    return VBox([
        HBox([slider, toggle]),
        output
    ])


def forward_sample_and_plot(model, n_samples=1000):
    """Sample from prior and plot marginal distributions."""
    samples = model.simulate(n_samples=n_samples, show_progress=False)

    fig, axes = plt.subplots(1, 3, figsize=(14, 4))

    for idx, (col, ax) in enumerate(zip(samples.columns, axes)):
        counts = samples[col].value_counts(normalize=True).sort_index()
        colors = ['#4ecdc4', '#ff6b6b']
        bars = ax.bar(range(len(counts)), counts.values, color=colors[:len(counts)])
        ax.set_xticks(range(len(counts)))
        state_labels = ['Absent', 'Present']
        ax.set_xticklabels(state_labels[:len(counts)])
        ax.set_ylabel('Probability')
        ax.set_title(f'{col}', fontweight='bold')
        ax.set_ylim([0, 1])

        for i, bar in enumerate(bars):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{height:.3f}', ha='center', va='bottom')

    fig.suptitle('Belief Before Any Observations (Forward Sampling)',
                fontweight='bold', fontsize=14)
    plt.tight_layout()

    return fig


def compare_exact_and_sampling(model):
    """Compare exact inference with forward sampling."""
    inference = VariableElimination(model)

    n_samples = 1000
    samples = model.simulate(n_samples=n_samples, show_progress=False)

    fig, axes = plt.subplots(1, 3, figsize=(14, 4))

    for idx, var in enumerate(model.nodes()):
        ax = axes[idx]

        exact_result = inference.query(variables=[var])
        exact_probs = exact_result.values.flatten()

        sample_counts = samples[var].value_counts(normalize=True).sort_index()
        sample_probs = sample_counts.values

        x = np.arange(2)
        width = 0.35

        ax.bar(x - width/2, sample_probs, width, label='Forward Sampling', alpha=0.7)
        ax.bar(x + width/2, exact_probs, width, label='Variable Elimination', alpha=0.7)

        ax.set_ylabel('Probability')
        ax.set_title(f'{var}', fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels(['Absent', 'Present'])
        ax.set_ylim([0, 1])
        ax.legend()

    fig.suptitle('Exact vs. Sampling Inference', fontweight='bold', fontsize=14)
    plt.tight_layout()

    return fig


def condition_on_evidence(model):
    """Show effect of conditioning on single evidence."""
    inference = VariableElimination(model)

    fig, axes = plt.subplots(1, 3, figsize=(14, 4))

    prior = inference.query(variables=['Disease'])
    posterior_pos = inference.query(variables=['Disease'], evidence={'Test': 'Positive'})
    posterior_neg = inference.query(variables=['Disease'], evidence={'Test': 'Negative'})

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

    for ax, prob, title in zip(axes, probs, titles):
        colors = ['#4ecdc4', '#ff6b6b']
        bars = ax.bar(['Absent', 'Present'], prob, color=colors)
        ax.set_ylabel('Probability')
        ax.set_title(title, fontweight='bold')
        ax.set_ylim([0, 1])

        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{height:.3f}', ha='center', va='bottom')

    fig.suptitle('How Evidence Changes Beliefs', fontweight='bold', fontsize=14)
    plt.tight_layout()

    return fig


def create_evidence_explorer():
    """Interactive widget for exploring evidence combinations."""
    output = Output()

    test_dropdown = Dropdown(
        options=[('No Test', None), ('Positive', 'Positive'), ('Negative', 'Negative')],
        description='Test Result:',
        style={'description_width': '120px'}
    )

    symptom_dropdown = Dropdown(
        options=[('No Symptom', None), ('Present', 'Present'), ('Absent', 'Absent')],
        description='Symptom:',
        style={'description_width': '120px'}
    )

    clear_button = Button(description='Clear Evidence', button_style='danger')

    def update_plot(change=None):
        with output:
            output.clear_output(wait=True)

            model = create_medical_network()
            inference = VariableElimination(model)

            evidence = {}
            if test_dropdown.value is not None:
                evidence['Test'] = test_dropdown.value
            if symptom_dropdown.value is not None:
                evidence['Symptom'] = symptom_dropdown.value

            result = inference.query(variables=['Disease'], evidence=evidence)

            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))

            visualize_network(model, evidence=list(evidence.keys()))
            plt.sca(ax1)

            colors = ['#4ecdc4', '#ff6b6b']
            bars = ax2.bar(['Absent', 'Present'], result.values.flatten(), color=colors)
            ax2.set_ylabel('Probability')
            ax2.set_title('P(Disease | Evidence)', fontweight='bold')
            ax2.set_ylim([0, 1])

            for bar in bars:
                height = bar.get_height()
                ax2.text(bar.get_x() + bar.get_width()/2., height,
                        f'{height:.4f}', ha='center', va='bottom')

            if evidence:
                evidence_str = ', '.join([f'{k}={v}' for k, v in evidence.items()])
                fig.suptitle(f'Evidence: {evidence_str}', fontweight='bold', fontsize=12)

            plt.tight_layout()
            plt.show()

    def on_clear_click(change=None):
        test_dropdown.value = None
        symptom_dropdown.value = None

    test_dropdown.observe(update_plot, 'value')
    symptom_dropdown.observe(update_plot, 'value')
    clear_button.on_click(on_clear_click)

    update_plot()

    return VBox([
        HBox([test_dropdown, symptom_dropdown, clear_button]),
        output
    ])


def compare_inference_algorithms():
    """Compare Variable Elimination, Belief Propagation, and Sampling."""
    model = create_medical_network()
    evidence = {'Test': 'Positive'}

    results = {}
    times = {}

    ve_inference = VariableElimination(model)
    start = time.time()
    ve_result = ve_inference.query(variables=['Disease'], evidence=evidence)
    times['Variable Elimination'] = (time.time() - start) * 1000
    results['Variable Elimination'] = ve_result.values.flatten()

    bp_inference = BeliefPropagation(model)
    start = time.time()
    bp_result = bp_inference.query(variables=['Disease'], evidence=evidence)
    times['Belief Propagation'] = (time.time() - start) * 1000
    results['Belief Propagation'] = bp_result.values.flatten()

    samples = model.simulate(n_samples=10000, evidence=evidence, show_progress=False)
    sampling_result = samples['Disease'].value_counts(normalize=True).sort_index()
    times['Sampling'] = 10
    results['Sampling'] = sampling_result.values

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 4))

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

    colors = ['#4ecdc4', '#ff6b6b', '#95e1d3']
    ax2.bar(results.keys(), times.values(), color=colors)
    ax2.set_ylabel('Time (ms)')
    ax2.set_title('Computation Time per Query', fontweight='bold')
    ax2.set_yscale('log')

    fig.suptitle('Comparing Inference Algorithms', fontweight='bold', fontsize=14)
    plt.tight_layout()

    return fig


def gibbs_sampling_interactive():
    """Interactive sampling visualization showing convergence."""
    output = Output()

    samples_slider = IntSlider(
        value=1000,
        min=100,
        max=10000,
        step=100,
        description='Samples:',
        style={'description_width': '100px'}
    )

    burnin_slider = IntSlider(
        value=200,
        min=0,
        max=2000,
        step=100,
        description='Burn-in:',
        style={'description_width': '100px'}
    )

    run_button = Button(description='Run Sampling', button_style='info')

    def update_gibbs(change=None):
        with output:
            output.clear_output(wait=True)

            model = create_medical_network()
            n_samples = samples_slider.value
            burn_in = burnin_slider.value

            samples_df = model.simulate(n_samples=n_samples,
                                       evidence={'Test': 'Positive'},
                                       show_progress=False, seed=42)

            disease_values = (samples_df['Disease'] == 'Present').astype(int).values

            fig, ax = plt.subplots(figsize=(12, 4))

            running_mean = np.cumsum(disease_values) / np.arange(1, len(disease_values) + 1)

            ax.axvspan(0, burn_in, alpha=0.2, color='gray', label='Burn-in')
            ax.plot(running_mean, linewidth=1, label='Running Mean', color='#4ecdc4')

            true_posterior = 0.9 * 0.05 / (0.9 * 0.05 + 0.1 * 0.95)
            ax.axhline(y=true_posterior, color='red', linestyle='--',
                      linewidth=2, label=f'True Posterior ({true_posterior:.3f})')

            ax.fill_between(range(len(running_mean)),
                            true_posterior - 0.1, true_posterior + 0.1,
                            alpha=0.1, color='red')

            ax.set_xlabel('Sample Number')
            ax.set_ylabel('P(Disease=Present | Test+)')
            ax.set_title('Sampling Convergence', fontweight='bold')
            ax.legend()
            ax.set_ylim([0, 1])

            plt.tight_layout()
            plt.show()

    samples_slider.observe(update_gibbs, 'value')
    burnin_slider.observe(update_gibbs, 'value')
    run_button.on_click(update_gibbs)

    update_gibbs()

    return VBox([
        HBox([samples_slider, burnin_slider, run_button]),
        output
    ])


def joint_distribution_explorer():
    """Interactive joint distribution visualization."""
    output = Output()

    disease_dropdown = Dropdown(
        options=[('None', None), ('Present', 'Present'), ('Absent', 'Absent')],
        description='Disease:',
        style={'description_width': '100px'}
    )

    symptom_dropdown = Dropdown(
        options=[('None', None), ('Present', 'Present'), ('Absent', 'Absent')],
        description='Symptom:',
        style={'description_width': '100px'}
    )

    def update_joint(change=None):
        with output:
            output.clear_output(wait=True)

            model = create_medical_network()
            inference = VariableElimination(model)

            evidence = {}
            if disease_dropdown.value is not None:
                evidence['Disease'] = disease_dropdown.value
            if symptom_dropdown.value is not None:
                evidence['Symptom'] = symptom_dropdown.value

            joint_result = inference.query(
                variables=['Disease', 'Symptom'],
                evidence=evidence
            )

            fig, axes = plt.subplots(1, 2, figsize=(12, 4))

            joint_array = joint_result.values.reshape(2, 2)
            sns.heatmap(joint_array, annot=True, fmt='.4f', cmap='YlOrRd',
                       ax=axes[0], cbar_kws={'label': 'Probability'},
                       xticklabels=['Symptom Absent', 'Symptom Present'],
                       yticklabels=['Disease Absent', 'Disease Present'])
            axes[0].set_title('Joint Distribution P(Disease, Symptom)', fontweight='bold')

            disease_marg = joint_array.sum(axis=1)
            symptom_marg = joint_array.sum(axis=0)

            axes[1].bar(['Disease Absent', 'Disease Present'], disease_marg,
                       alpha=0.6, label='P(Disease)', color='#4ecdc4')
            ax2 = axes[1].twinx()
            ax2.bar(['Symptom Absent', 'Symptom Present'], symptom_marg,
                   alpha=0.6, label='P(Symptom)', color='#ff6b6b')

            axes[1].set_ylabel('P(Disease)')
            ax2.set_ylabel('P(Symptom)')
            axes[1].set_title('Marginal Distributions', fontweight='bold')
            axes[1].set_ylim([0, 1])
            ax2.set_ylim([0, 1])

            plt.tight_layout()
            plt.show()

    disease_dropdown.observe(update_joint, 'value')
    symptom_dropdown.observe(update_joint, 'value')

    update_joint()

    return VBox([
        HBox([disease_dropdown, symptom_dropdown]),
        output
    ])


def map_query_demo():
    """Demonstrate MAP (Maximum A Posteriori) queries."""
    model = create_medical_network()
    inference = VariableElimination(model)

    evidence = {'Test': 'Positive'}
    map_result = inference.map_query(variables=['Disease', 'Symptom'],
                                    evidence=evidence)

    fig, ax = plt.subplots(figsize=(10, 4))

    all_combos = [
        'Disease Absent, Symptom Absent',
        'Disease Absent, Symptom Present',
        'Disease Present, Symptom Absent',
        'Disease Present, Symptom Present'
    ]

    joint_result = inference.query(
        variables=['Disease', 'Symptom'],
        evidence=evidence
    )
    probs = joint_result.values

    colors = ['lightgray'] * 4
    disease_idx = 1 if map_result['Disease'] == 'Present' else 0
    symptom_idx = 1 if map_result['Symptom'] == 'Present' else 0
    map_idx = disease_idx * 2 + symptom_idx
    colors[map_idx] = '#ff6b6b'

    bars = ax.bar(range(len(all_combos)), probs, color=colors)
    ax.set_xticks(range(len(all_combos)))
    ax.set_xticklabels(all_combos, rotation=45, ha='right')
    ax.set_ylabel('Probability')
    ax.set_title(f'MAP Assignment: {map_result}', fontweight='bold')

    for i, (bar, prob) in enumerate(zip(bars, probs)):
        ax.text(bar.get_x() + bar.get_width()/2., prob,
               f'{prob:.4f}', ha='center', va='bottom')

    plt.tight_layout()

    return fig


def larger_network_demo():
    """Create and visualize a larger Bayesian network."""
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

    cpds = [
        TabularCPD('Genetics', 2, [[0.8], [0.2]],
                   state_names={'Genetics': ['Low', 'High']}),
        TabularCPD('Environment', 2, [[0.7], [0.3]],
                   state_names={'Environment': ['Good', 'Bad']}),
        TabularCPD('Protein', 2, [[0.85, 0.3], [0.15, 0.7]],
                   evidence=['Genetics'], evidence_card=[2],
                   state_names={'Protein': ['Low', 'High'], 'Genetics': ['Low', 'High']}),
        TabularCPD('Lifestyle', 2, [[0.9, 0.4], [0.1, 0.6]],
                   evidence=['Environment'], evidence_card=[2],
                   state_names={'Lifestyle': ['Good', 'Bad'], 'Environment': ['Good', 'Bad']}),
        TabularCPD('Disease', 2,
                   [[0.99, 0.8, 0.7, 0.1], [0.01, 0.2, 0.3, 0.9]],
                   evidence=['Protein', 'Lifestyle'], evidence_card=[2, 2],
                   state_names={'Disease': ['Absent', 'Present'],
                               'Protein': ['Low', 'High'], 'Lifestyle': ['Good', 'Bad']}),
        TabularCPD('Symptom1', 2, [[0.9, 0.2], [0.1, 0.8]],
                   evidence=['Disease'], evidence_card=[2],
                   state_names={'Symptom1': ['Absent', 'Present'], 'Disease': ['Absent', 'Present']}),
        TabularCPD('Symptom2', 2, [[0.8, 0.1], [0.2, 0.9]],
                   evidence=['Disease'], evidence_card=[2],
                   state_names={'Symptom2': ['Absent', 'Present'], 'Disease': ['Absent', 'Present']}),
        TabularCPD('Test1', 2, [[0.95, 0.05], [0.05, 0.95]],
                   evidence=['Disease'], evidence_card=[2],
                   state_names={'Test1': ['Negative', 'Positive'], 'Disease': ['Absent', 'Present']}),
        TabularCPD('Test2', 2, [[0.85, 0.2], [0.15, 0.8]],
                   evidence=['Symptom1'], evidence_card=[2],
                   state_names={'Test2': ['Negative', 'Positive'], 'Symptom1': ['Absent', 'Present']}),
    ]

    model.add_cpds(*cpds)
    model.check_model()

    return model


def larger_network_interactive():
    """Interactive demo for larger network."""
    output = Output()

    scenario_dropdown = Dropdown(
        options=[('Positive Test Only', {'Test1': 'Positive'}),
                ('Test and Symptoms', {'Test1': 'Positive', 'Symptom1': 'Present'}),
                ('Test but No Symptom', {'Test1': 'Positive', 'Symptom1': 'Absent'})],
        description='Scenario:',
        style={'description_width': '100px'}
    )

    method_dropdown = Dropdown(
        options=[('Variable Elimination', 'VE'), ('Sampling', 'Sampling')],
        description='Method:',
        style={'description_width': '100px'}
    )

    def update_larger_net(change=None):
        with output:
            output.clear_output(wait=True)

            model = larger_network_demo()
            evidence = scenario_dropdown.value

            if method_dropdown.value == 'VE':
                inference = VariableElimination(model)
                start = time.time()
                result = inference.query(variables=['Disease'], evidence=evidence)
                elapsed = (time.time() - start) * 1000
                result_vals = result.values.flatten()
            else:
                start = time.time()
                samples = model.simulate(n_samples=5000, evidence=evidence,
                                        show_progress=False)
                elapsed = (time.time() - start) * 1000
                disease_counts = (samples['Disease'] == 'Present').sum() / len(samples)
                result_vals = np.array([1 - disease_counts, disease_counts])

            fig, axes = plt.subplots(1, 2, figsize=(14, 4))

            visualize_network(model, evidence=list(evidence.keys()))
            plt.sca(axes[0])

            colors = ['#4ecdc4', '#ff6b6b']
            bars = axes[1].bar(['Absent', 'Present'], result_vals, color=colors)
            axes[1].set_ylabel('Probability')
            axes[1].set_title(f'P(Disease | Evidence)\nTime: {elapsed:.2f}ms', fontweight='bold')
            axes[1].set_ylim([0, 1])

            for bar in bars:
                height = bar.get_height()
                axes[1].text(bar.get_x() + bar.get_width()/2., height,
                           f'{height:.3f}', ha='center', va='bottom')

            plt.tight_layout()
            plt.show()

    scenario_dropdown.observe(update_larger_net, 'value')
    method_dropdown.observe(update_larger_net, 'value')

    update_larger_net()

    return VBox([
        HBox([scenario_dropdown, method_dropdown]),
        output
    ])


def practical_workflow_demo():
    """Demonstrate practical inference workflow."""
    model = larger_network_demo()

    print("Step 1: Load and Inspect Model")
    print("="*50)
    print(f"Model has {len(model.nodes())} nodes and {len(model.edges())} edges")
    print(f"Nodes: {list(model.nodes())}")
    print(f"\nModel validity: ", end="")
    try:
        model.check_model()
        print("VALID")
    except Exception as e:
        print(f"ERROR: {e}")

    print("\n\nStep 2: Choose Inference Algorithm")
    print("="*50)
    print("For an 8-node network: Variable Elimination is exact and fast")

    print("\n\nStep 3: Query with Evidence")
    print("="*50)
    evidence = {'Test1': 'Positive', 'Symptom1': 'Present'}
    print(f"Evidence: {evidence}")

    inference = VariableElimination(model)
    start = time.time()
    result = inference.query(variables=['Disease'], evidence=evidence)
    elapsed = (time.time() - start) * 1000

    print(f"\nResult P(Disease | Evidence):")
    print(result)
    print(f"\nTime: {elapsed:.3f}ms")

    print("\n\nStep 4: Visualize Results")
    print("="*50)

    fig, ax = plt.subplots(figsize=(10, 4))
    colors = ['#4ecdc4', '#ff6b6b']
    bars = ax.bar(['Absent', 'Present'], result.values.flatten(), color=colors)
    ax.set_ylabel('Probability')
    ax.set_title('P(Disease | Test1+ and Symptom1+)', fontweight='bold')
    ax.set_ylim([0, 1])

    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
               f'{height:.4f}', ha='center', va='bottom')

    plt.tight_layout()
    plt.show()

    print(f"\nConclusion: {result.values.flatten()[1]:.1%} probability of disease given evidence")
