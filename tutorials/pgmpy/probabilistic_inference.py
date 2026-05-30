# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.19.0
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %% [markdown]
# # Probabilistic Inference with pgmpy: Interactive Tutorial
#
# Learn how to build Bayesian networks and answer questions about uncertain variables using probabilistic inference. This notebook guides you from intuition to practical algorithms.

# %%
import warnings
warnings.filterwarnings('ignore')
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from probabilistic_inference_utils import *

# %% [markdown]
# ## Cell 1: Building Your First Bayesian Network
#
# A Bayesian network is a directed acyclic graph where nodes represent random variables and edges represent conditional relationships. Let's build a simple medical diagnosis network: does a patient have a disease? We'll observe symptoms and test results to infer the presence or absence of disease.
#
# The network structure shows:
# - **Disease**: The hidden cause we want to infer
# - **Symptom**: Observable sign that depends on Disease
# - **Test**: Diagnostic test whose result depends on Disease
#
# This structure encodes independence assumptions: given the disease status, symptom and test are independent.

# %%
# Build the medical diagnosis network
model = create_medical_network()

# Visualize the network structure
visualize_network(model)
plt.show()

print("Network structure encodes independence:")
print("Given Disease, Symptom and Test are independent of each other.")
print("\nThis is critical for efficient inference!")

# %% [markdown]
# ## Cell 2: Defining Conditional Probability Tables
#
# Each node in the network has a probability table that defines how likely its values are. For root nodes (no parents), this is a prior probability. For other nodes, it's a conditional probability given the parents.
#
# These tables encode domain knowledge:
# - How common is the disease in the population?
# - If someone has the disease, how likely are they to show a symptom?
# - How accurate is the diagnostic test?
#
# Try adjusting the disease prior and see how the tables change.

# %%
# Interactive CPD visualization
create_cpd_widget(disease_prior=0.05)

# %% [markdown]
# ## Cell 3: Forward Simulation From the Prior
#
# What does the network "believe" before we observe any data? We can sample from the network to find out. Each sample represents one hypothetical patient drawn from our prior beliefs.
#
# Notice that rare diseases stay rare in samples, even when they cause symptoms. That's because the disease base rate (5%) dominates.

# %%
# Sample from the prior distribution
model = create_medical_network()
forward_sample_and_plot(model, num_samples=1000)
plt.show()

print("This is what the network believes in a vacuum.")
print("Disease is rare (5%), so both Symptom and Test mostly indicate Absent.")

# %% [markdown]
# ## Cell 4: Exact Inference Without Evidence
#
# We can compute exact probabilities instead of sampling. The pgmpy library uses algorithms like Variable Elimination that compute probabilities efficiently without drawing samples.
#
# Notice how the exact results (blue) line up perfectly with the forward samples (orange). Both methods answer the same question: "What do we believe?"

# %%
# Compare exact inference with forward sampling
model = create_medical_network()
compare_exact_and_sampling(model)
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
# ## Cell 5: Conditioning on Evidence Changes Everything
#
# This is the core of inference: observing evidence dramatically shifts what we believe about unobserved variables.
#
# - A **positive test** increases disease probability from 5% to ~45%
# - A **negative test** decreases it to <1%
#
# The strength of the shift depends on how strongly the evidence relates to the hidden variable. A test that's 95% accurate for positive cases and 90% for negative cases is fairly informative.

# %%
# Show effect of conditioning on evidence
model = create_medical_network()
condition_on_evidence(model)
plt.show()

print("This is Bayes' rule in action:")
print("P(Disease | Evidence) = P(Evidence | Disease) * P(Disease) / P(Evidence)")
print("\nWe update prior beliefs using observed evidence.")

# %% [markdown]
# ## Cell 6: Interactive Evidence Explorer
#
# Now it's your turn! Combine different evidence and watch the posterior probability update in real time.
#
# Try these combinations:
# - Positive test alone
# - Positive test + symptom present (strong evidence)
# - Positive test + symptom absent (conflicting evidence)
#
# Notice how the network combines evidence. Order doesn't matter—Bayesian networks encode probability, not causality in time.

# %%
# Interactive evidence explorer
model = create_medical_network()
create_evidence_explorer()

# %% [markdown]
# ## Cell 7: Comparing Inference Algorithms
#
# There are many algorithms for probabilistic inference:
#
# 1. **Variable Elimination**: Exact, efficient for small networks
# 2. **Belief Propagation**: Exact, efficient for tree-structured networks
# 3. **Sampling**: Approximate, scales to large networks
#
# For our small network, all methods give identical results. The differences appear when networks grow larger or have complex structure (loops).

# %%
# Compare inference algorithms
model = create_medical_network()
compare_inference_algorithms()
plt.show()

print("All methods answer the same question correctly.")
print("Choice of algorithm is driven by network size and structure.")
print("\nRule of thumb:")
print("- <=15 variables: Exact methods (Variable Elimination)")
print("- >15 variables: Approximate methods (Sampling, Variational)")

# %% [markdown]
# ## Cell 8: Approximate Inference With Gibbs Sampling
#
# Gibbs sampling is a Markov Chain Monte Carlo (MCMC) algorithm that generates samples from the posterior distribution.
#
# Key points:
# - **Burn-in**: Early samples depend on initialization; discard them
# - **Convergence**: With enough samples, empirical frequencies match true probabilities
# - **Trade-off**: More samples = more accurate, but slower
#
# Adjust the sliders to see how burn-in and sample count affect convergence.

# %%
# Gibbs sampling interactive visualization
model = create_medical_network()
gibbs_sampling_interactive()

# %% [markdown]
# ## Cell 9: When Evidence is Complex: Multiple Constraints
#
# Real inference problems often involve multiple observed variables. The full joint distribution over unobserved variables contains more information than individual marginals.
#
# Try observing different combinations:
# - Disease alone
# - Disease + Symptom
# - Disease + Test
#
# The heatmap shows how probability is distributed across combinations. The marginal bar plots show what we learn about individual variables.

# %%
# Joint distribution explorer
model = create_medical_network()
joint_distribution_explorer()

# %% [markdown]
# ## Cell 10: Maximum A Posteriori (MAP) Queries
#
# Sometimes we don't need the full probability distribution. We just want: "What is the single most likely explanation for the evidence?"
#
# **MAP vs. Marginal Inference:**
# - **Marginal**: P(Disease=Yes | Evidence) — probability for each variable independently
# - **MAP**: argmax P(Disease, Symptom | Evidence) — single most likely joint assignment
#
# Diagnostics usually want MAP: "What's the most likely disease state and symptom combination?"

# %%
# MAP query demonstration
model = create_medical_network()
map_query_demo()
plt.show()

print("MAP finds the single most likely joint assignment.")
print("Useful for diagnosis: 'What's the best explanation for the observations?'")

# %% [markdown]
# ## Cell 11: Building Intuition for Larger Networks
#
# Real-world Bayesian networks have many variables: genetic factors, lifestyle, multiple tests and symptoms, environmental factors, etc.
#
# **Challenges at scale:**
# - Exact inference becomes intractable (exponential in variables)
# - Network topology (tree vs. loopy) matters for algorithm efficiency
# - Must choose algorithm carefully
#
# Try different evidence scenarios and inference methods to see how computation time grows.

# %%
# Larger network interactive demo
larger_network_interactive()

# %% [markdown]
# ## Cell 12: Practical Workflow: From Model to Inference
#
# In practice, you'll follow this workflow:
#
# 1. **Load** a pre-trained or pre-built Bayesian network
# 2. **Inspect** the model structure and probability tables
# 3. **Validate** that all CPDs are well-formed (sum to 1)
# 4. **Choose** an inference algorithm based on network size
# 5. **Query** with evidence to answer domain questions
# 6. **Interpret** results in context
#
# Let's walk through a complete example.

# %%
# Practical workflow demonstration
model = larger_network_demo()
practical_workflow_demo()

# %% [markdown]
# ## Summary
#
# You've learned:
#
# 1. **Structure**: Bayesian networks encode conditional relationships and independence assumptions
# 2. **Probabilities**: CPDs assign numerical beliefs to network structure
# 3. **Inference**: Computing P(unobserved | observed) using Bayes' rule
# 4. **Algorithms**: Different exact/approximate methods with different tradeoffs
# 5. **Practice**: Building networks, observing evidence, and interpreting results
#
# ### Key Takeaways:
# - Bayesian networks automate probabilistic reasoning
# - Same network structure + different evidence → different conclusions
# - Algorithm choice (exact vs. approximate) depends on network size
# - Order of evidence doesn't matter; combine observations probabilistically
#
# ### Next Steps:
# - Build your own Bayesian network for a domain you care about
# - Compare MAP and marginal inference on your model
# - Learn about parameter learning (fitting CPDs from data)
# - Explore structure learning (discovering network structure from data)
