# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.19.3
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %% [markdown]
# # Description
#
# - Bayesian networks for probabilistic inference with pgmpy:
#   - Building networks and defining conditional relationships
#   - Conditional probability tables (CPDs)
#   - Exact and approximate inference algorithms
#   - MAP queries and interactive visualizations

# %% [markdown]
# ## Imports

# %%
# %load_ext autoreload
# %autoreload 2

# System libraries.
import logging

# Third-party libraries.
import matplotlib.pyplot as plt

# %%
# # To install additional packages, use:
# import helpers.hmodule as hmodule
# hmodule.install_module_if_not_present(
#     ["graphviz"],
#     use_activate=True,
#     use_sudo=False,
#     venv_path="/opt/venv",
# )

# %%
# Use this for most notebooks.
import helpers.hdbg as hdbg
import helpers.hnotebook as hnotebook

_LOG = logging.getLogger(__name__)

# Initialize notebook configuration and logging.
# hnotebook.config_notebook()
# hdbg.init_logger(verbosity=logging.INFO, use_exec_path=False)
# hnotebook.set_logger_to_print(_LOG)

import probabilistic_inference_utils as utils

# Convert `display` into `print()`.
try:
    from IPython.display import display
except ImportError:
    display = print  # type: ignore

import warnings

warnings.filterwarnings("ignore")

# %% [markdown]
# - **Definition**: Bayesian networks are directed acyclic graphs encoding conditional relationships
#   - Nodes represent random variables
#   - Edges represent conditional dependencies
#   - Structure encodes independence assumptions
#
# - **Medical diagnosis example**: Infer disease status from observable symptoms and test results
#   - Disease: Hidden cause we want to infer
#   - Symptom: Observable sign depending on disease status
#   - Test: Diagnostic test result depending on disease status
#
# - **Key insight**: Given disease status, symptom and test are conditionally independent
#   - Enables efficient inference algorithms
#   - Order of evidence doesn't matter for combining observations

# %%
# Build the medical diagnosis network
model = utils.create_medical_network()

# Visualize the network structure
utils.visualize_network(model)
plt.show()

# %% [markdown]
# - **Network structure encodes independence**: The visualization shows how graph structure represents conditional relationships
#   - Given Disease status, Symptom and Test observations become independent of each other
#   - This independence assumption is critical for efficient inference algorithms
#   - The graph structure encodes domain knowledge about relationships between variables

# %% [markdown]
# - **CPD**: Conditional probability table assigns numerical beliefs to network structure
#   - Root nodes (no parents): Prior probability distribution
#   - Non-root nodes: Conditional probability given parent values
#
# - **Medical domain knowledge encoded in CPDs**:
#   - Disease prevalence in population
#   - Symptom likelihood given disease status
#   - Diagnostic test accuracy
#
# - **Key concept**: CPDs + network structure = complete probabilistic model
#   - Enables queries about unobserved variables given evidence

# %%
# #utils.create_cpd_widget??

# %%
# Interactive CPD visualization
# TODO(ai_gp): Explain what utils.create_cpd_widget does, what the plots mean, what the widget do
utils.create_cpd_widget(disease_prior=0.05)

# %%
# Sample from the prior distribution.
model = utils.create_medical_network()
utils.forward_sample_and_plot(model, n_samples=1000)
plt.show()

# %% [markdown]
# - **Sampling reveals prior beliefs**: The distribution shows what the network believes in a vacuum without any observations
#   - Disease is rare (5% prior), so both Symptom and Test mostly indicate Absent status
#   - Base rate dominance: the rare disease prior overwhelms the samples
#   - Each sample represents one hypothetical patient drawn from the network's generative model

# %%
# Compare exact inference with forward sampling
model = utils.create_medical_network()
utils.compare_exact_and_sampling(model)
plt.show()

# %% [markdown]
# - **Exact inference vs forward sampling**: Both methods answer what we believe about the prior distribution
#   - Exact results (blue line) computed with Variable Elimination, guaranteed correct
#   - Forward sampling results (orange) match exactly; accuracy improves with more samples
#   - Scaling comparison: Exact scales poorly as network grows (exponential), sampling scales better but needs many samples
#
# - **Algorithm tradeoffs**:
#   - **Variable Elimination**: Guaranteed correct, fast for small networks, intractable for large networks
#   - **Forward Sampling**: Approximate, scales to large networks, needs more samples for same accuracy

# %% [markdown]
# # Show effect of conditioning on evidence
# model = utils.create_medical_network()
# utils.condition_on_evidence(model)
# plt.show()

# %% [markdown]
# - **Bayes' rule in action**: Observing evidence shifts posterior probabilities away from prior beliefs
#   - Formula: $\Pr(\text{Disease} | \text{Evidence}) = \frac{\Pr(\text{Evidence} | \text{Disease}) \Pr(\text{Disease})}{\Pr(\text{Evidence})}$
#   - Positive test shifts disease probability from 5% (prior) to ~45% (posterior)
#   - Negative test dramatically reduces disease probability to <1%
#
# - **Evidence informativeness**: The strength of the shift depends on test accuracy and base rate
#   - Test is fairly informative: 95% sensitivity (true positive), 90% specificity (true negative)
#   - But base rate effect still matters: rare diseases stay rare unless evidence is overwhelming

# %%
# Compare exact inference with forward sampling
model = utils.create_medical_network()
utils.compare_exact_and_sampling(model)
plt.show()

print("Exact Inference: Variable Elimination")
print("- Guaranteed correct")
print("- Scales poorly with network size")
print("- Fast for small networks")
print("\nForward Sampling: Approximate")
print("- Gets more accurate with more samples")
print("- Scales to large networks")
print("- Slower per query but parallelizable")

# %% [markdown]
# - **Core inference concept**: Observing evidence shifts what we believe about unobserved variables
#   - Prior: Disease probability = 5%
#   - Positive test: Disease probability = ~45%
#   - Negative test: Disease probability = <1%
#
# - **Strength of shift depends on evidence informativeness**:
#   - Test accuracy: 95% for positives, 90% for negatives
#   - Fairly informative about disease status
#
# - **Bayes' rule in action**: $\Pr(\text{Disease} | \text{Evidence}) = \frac{\Pr(\text{Evidence} | \text{Disease}) \Pr(\text{Disease})}{\Pr(\text{Evidence})}$
#   - Prior beliefs updated using observed evidence

# %%
# Compare inference algorithms
model = utils.create_medical_network()
utils.compare_inference_algorithms()
plt.show()

# %% [markdown]
# - **Algorithm equivalence on small networks**: All inference methods answer the same question correctly
#   - Variable Elimination: Exact, efficient for small networks
#   - Belief Propagation: Exact for tree networks, efficient structure exploitation
#   - Sampling (Forward, Gibbs): Approximate, more accurate with more samples
#
# - **Practical algorithm selection**:
#   - Small networks (≤15 variables): Use exact methods (Variable Elimination)
#   - Larger networks (>15 variables): Use approximate methods (Sampling, Variational Inference)
#   - Network topology matters: Tree networks have faster exact algorithms than general loopy networks

# %% [markdown]
# - **Interactive exploration**: Combine different evidence and observe posterior probability updates in real time
#
# - **Try these combinations**:
#   - Positive test alone
#   - Positive test + symptom present (strong evidence)
#   - Positive test + symptom absent (conflicting evidence)
#
# - **Network behavior**: Combines evidence probabilistically
#   - Order of evidence doesn't matter
#   - Encodes probability, not causality in time

# %%
# Interactive evidence explorer
model = utils.create_medical_network()
utils.create_evidence_explorer()

# %% [markdown]
# - **Inference algorithms**: Different approaches with different performance tradeoffs
#
# - **Exact methods**:
#   - Variable Elimination: Efficient for small networks
#   - Belief Propagation: Efficient for tree-structured networks
#
# - **Approximate methods**:
#   - Sampling: Scales to large networks, requires more samples for accuracy
#
# - **Small networks**: All methods give identical results
#   - Choice of algorithm driven by network size and structure

# %%
# Compare inference algorithms
model = utils.create_medical_network()
utils.compare_inference_algorithms()
plt.show()

print("All methods answer the same question correctly.")
print("Choice of algorithm is driven by network size and structure.")
print("\nRule of thumb:")
print("- <=15 variables: Exact methods (Variable Elimination)")
print("- >15 variables: Approximate methods (Sampling, Variational)")

# %% [markdown]
# # MAP query demonstration
# model = utils.create_medical_network()
# utils.map_query_demo()
# plt.show()

# %% [markdown]
# - **MAP query finds single best explanation**: Different from marginal inference which computes individual probabilities
#   - Marginal: $\Pr(\text{Disease} = \text{Yes} | \text{Evidence})$ for individual variables
#   - MAP: $\arg\max_{\text{all vars}} \Pr(\text{Disease}, \text{Symptom}, ... | \text{Evidence})$ single joint assignment
#   - Practical use: Diagnostics want single best explanation, not individual probability distributions
#
# - **Interpretation**: The result shows the joint state that maximizes posterior probability
#   - Most likely to occur given the evidence
#   - Useful when you need one actionable answer, not a full probability distribution

# %%
# Gibbs sampling interactive visualization
model = utils.create_medical_network()
utils.gibbs_sampling_interactive()

# %% [markdown]
# - **Real inference problems**: Multiple observed variables with joint distribution over unobserved variables
#   - Full joint contains more information than individual marginals
#   - Different observation combinations reveal different dependencies
#
# - **Explore combinations**:
#   - Disease alone
#   - Disease + Symptom
#   - Disease + Test
#
# - **Visualization**: Heatmap shows joint probability distribution
#   - Marginal bar plots show what we learn about individual variables

# %%
# Joint distribution explorer
model = utils.create_medical_network()
utils.joint_distribution_explorer()

# %% [markdown]
# - **MAP query**: Find single most likely explanation for evidence
#
# - **Distinction from marginal inference**:
#   - Marginal: $\Pr(\text{Disease} = \text{Yes} | \text{Evidence})$ for individual variables
#   - MAP: $\arg\max \Pr(\text{Disease}, \text{Symptom} | \text{Evidence})$ single joint assignment
#
# - **Practical use**: Diagnostics want single best explanation
#   - "What's most likely disease state and symptom combination?"

# %%
# MAP query demonstration
model = utils.create_medical_network()
utils.map_query_demo()
plt.show()

print("MAP finds the single most likely joint assignment.")
print("Useful for diagnosis: 'What's the best explanation for the observations?'")

# %% [markdown]
# - **Real-world networks**: Many variables: genetic factors, lifestyle, multiple tests, symptoms, environmental factors
#
# - **Computational challenges at scale**:
#   - Exact inference becomes intractable (exponential in variables)
#   - Network topology (tree vs loopy) matters for algorithm efficiency
#   - Must choose algorithm carefully based on problem size
#
# - **Scaling rules of thumb**:
#   - Up to 15 variables: Exact methods (Variable Elimination)
#   - Beyond 15: Approximate methods (Sampling, Variational)

# %%
# Larger network interactive demo
utils.larger_network_interactive()

# %% [markdown]
# - **Practical workflow**: From model to inference and interpretation
#
# - **Steps**:
#   1. Load pre-trained or pre-built Bayesian network
#   2. Inspect model structure and probability tables
#   3. Validate CPDs are well-formed (sum to 1)
#   4. Choose inference algorithm based on network size
#   5. Query with evidence to answer domain questions
#   6. Interpret results in context

# %%
# Practical workflow demonstration
model = utils.larger_network_demo()
utils.practical_workflow_demo()

# %% [markdown]
# - **Structure**: Bayesian networks encode conditional relationships and independence assumptions
#
# - **Probabilities**: CPDs assign numerical beliefs to network structure
#
# - **Inference**: Computing $\Pr(\text{unobserved} | \text{observed})$ using Bayes' rule
#
# - **Algorithms**: Different exact/approximate methods with different tradeoffs
#   - Exact methods for small networks
#   - Approximate methods for large networks
#
# - **Key insights**:
#   - Same network + different evidence = different conclusions
#   - Algorithm choice depends on network size
#   - Order of evidence doesn't matter
#
# - **Next steps**:
#   - Build networks for your domain
#   - Compare MAP and marginal inference
#   - Learn parameter learning (fitting CPDs from data)
#   - Explore structure learning (discovering network structure from data)
