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
# # Exact Inference in Bayesian Networks
#
# - This notebook teaches how to compute exact posteriors $P(X \mid \mathbf{e})$
#   in a discrete Bayesian network
# - Concepts are built on the the burglary-alarm network and the query
#   $P(Burglary \mid JohnCalls, MaryCalls)$
# - The flow is:
#   - Inference by enumeration (brute force)
#   - Variable elimination (caching)
#   - Irrelevant-variable pruning
#   - Complexity and limits

# %% [markdown]
# ## Imports

# %%
# %load_ext autoreload
# %autoreload 2

# System libraries.
import logging

# Third-party libraries.
import matplotlib.pyplot as plt
import seaborn as sns

# %%
# Use this for most notebooks.
import helpers.htutorial as htutori

import exact_inference_utils as utils

htutori.config_notebook()

# Initialize logger.
logging.basicConfig(level=logging.INFO)
_LOG = logging.getLogger(__name__)
utils.init_loggers(_LOG)

# Convert `display` into `print()` when running outside IPython.
try:
    from IPython.display import display
except ImportError:
    display = print  # type: ignore

# %% [markdown]
# # Part 1: Setting Up the Inference Problem

# %% [markdown]
# ## Cell 1.1: The Burglary Alarm Network and Its CPTs
#
# - The five variables are:
#   - Root causes: $Burglary$, $Earthquake$ (blue)
#   - The $Alarm$ (orange)
#   - The calls: $JohnCalls$, $MaryCalls$ (purple)
# - The joint factorizes into five small CPTs:
#   $$P(B,E,A,J,M) = P(B)\,P(E)\,P(A \mid B,E)\,P(J \mid A)\,P(M \mid A)$$

# %%
# Display the DAG and its five conditional probability tables.
utils.cell1_1_show_network_and_cpts()

# TODO(ai_gp): The prob for P(Alarm | Burglary, Earthquake) do not match the slides in L06.1
# TODO(ai_gp): The colors of the nodes are different than the slides

# %% [markdown]
# - The joint over five variables factorizes into five small CPTs
# - Calls depend on the world only through $Alarm$: they are conditionally
#   independent of $Burglary$ and $Earthquake$ given $Alarm$
# - Storing 5 small CPTs (10 independent numbers) is far cheaper than the full
#   joint ($2^5 - 1 = 31$ numbers)
# - Inference never touches the full joint directly: it works with the factored
#   form, a product of the small CPTs attached to each node

# %% [markdown]
# ## Cell 1.2: Query, Evidence, and Hidden Variables
#
# **Goal**:
# - Build intuition for which variables must be summed out
#
# **Plots**:
# - _Roles DAG_: nodes recolored by role: query (blue), evidence (red), hidden
#   (grey)
# - _Comments_: restates the query in math and counts the hidden terms
#
# **Parameters**:
# - `Query X`: the single node being asked about
# - `observe <node>`: checkbox marking a node as evidence, with a True/False value
#
# **Key observations**:
# - Every node is exactly one of: query, evidence, or hidden
# - The posterior we want is $P(X \mid \mathbf{e})$; hidden variables are not in
#   the answer but cannot simply be dropped
# - Changing the evidence changes which variables are hidden

# %%
# Assign each node a role and recolor the DAG for the current query.
utils.cell1_2_query_roles_widget()

# %% [markdown]
# - The posterior we want is $P(X \mid \mathbf{e})$
# - Hidden variables $\mathbf{Y}$ are nuisances we must marginalize (sum) away to
#   get an answer about $X$ alone
# - The number of summed terms grows as $2^{|\mathbf{Y}|}$, so more hidden
#   variables means more work

# %% [markdown]
# # Part 2: Inference by Enumeration

# %% [markdown]
# ## Cell 2.1: From Conditional to Joint via Normalization
#
# **Goal**:
# - Derive why a conditional query reduces to summing the joint and normalizing
# - Show the role of the normalization constant $\alpha$
# - Set up the formula computed in the next cell
#
# **Plots**:
# - _Derivation_: the three equation lines of the derivation
# - _Value bars_: unnormalized joint values or the normalized posterior
# - _Comments_: the value of $\alpha$ and the resulting posterior
#
# **Parameters**:
# - `show normalization`: toggle between unnormalized joint and normalized
#   posterior
#
# **Key observations**:
# - $P(X \mid \mathbf{e}) = \alpha\, P(X, \mathbf{e})$
# - $P(X, \mathbf{e}) = \sum_{\mathbf{y}} P(X, \mathbf{e}, \mathbf{y})$
# - $\alpha$ removes the need to ever compute $P(\mathbf{e})$ directly

# %%
# Toggle between the unnormalized joint and the normalized posterior.
utils.cell2_1_normalization_widget()

# %% [markdown]
# - A conditional query is a slice of the joint (fix evidence), a sum over hidden
#   variables, and a rescale
# - The constant $\alpha = 1 / \sum_x P(x, \mathbf{e})$ is fixed at the end so the
#   posterior sums to 1
# - The joint slice is evaluated as a product of CPT lookups, never as one giant
#   table

# %% [markdown]
# ## Cell 2.2: Computing the Posterior by Enumeration
#
# **Goal**:
# - Compute the exact posterior by summing CPT products over hidden variables
# - Confirm the hand computation against the `pgmpy` engine
# - See how the number of summed rows grows with the hidden-variable count
#
# **Plots**:
# - _Sum for X=T_ and _Sum for X=F_: the hidden-assignment tables and products
# - _Posterior_: the resulting posterior bars with the `pgmpy` reference overlaid
# - _Comments_: row counts and the validated posterior
#
# **Parameters**:
# - `Query X`: the query variable
# - `observe <node>`: evidence selection and value
#
# **Key observations**:
# - The exact posterior $P(b \mid j,m) \approx 0.28$ matches the AIMA result
# - The number of rows summed is $2^{|\mathbf{Y}|}$ and grows fast
# - Hand computation and the `pgmpy` engine agree

# %%
# Compute the posterior by enumeration and validate against pgmpy.
utils.cell2_2_enumeration_widget()

# %% [markdown]
# - Enumeration is correct and simple: list every hidden-world combination,
#   multiply the CPTs, sum, normalize
# - Its weakness is the row count, which doubles with each extra hidden variable
# - The famous result $P(Burglary \mid j,m) \approx 0.284$ falls out directly

# %% [markdown]
# ## Cell 2.3: Visualizing the Enumeration Tree
#
# **Goal**:
# - Expose the enumeration computation as a tree
# - See the repeated subexpressions that motivate variable elimination
# - Relate the summation order to the shape of the tree
#
# **Plots**:
# - _Enumeration evaluation tree_: branches over hidden values, leaves are CPT
#   products, repeated factors share a color
# - _Comments_: the operation count and why the repeats are wasteful
#
# **Parameters**:
# - `Sum order`: which hidden variable branches first
# - `highlight repeated work`: shades the identical leaf subexpressions
#
# **Key observations**:
# - Enumeration recomputes the same factor products in many branches
# - The repeated subtrees are exactly what the next algorithm caches
# - Caching the shared factor is the single idea behind variable elimination

# %%
# Draw the enumeration tree and highlight the repeated subexpressions.
utils.cell2_3_enumeration_tree_widget()

# %% [markdown]
# - The same $P(j \mid a)P(m \mid a)$ factors recur under every value of the other
#   hidden variable
# - This repeated work is wasted: it is computed again and again
# - Variable elimination computes each shared factor once and reuses it

# %% [markdown]
# # Part 3: Variable Elimination

# %% [markdown]
# ## Cell 3.1: Factors as the Unit of Computation
#
# **Goal**:
# - Introduce the factor as the data structure manipulated by variable
#   elimination
# - Show that CPTs and intermediate results are both factors
# - Illustrate the operation of summing a variable out of a factor
#
# **Plots**:
# - _Before_: the selected factor as a table with its scope
# - _After_: the same factor once a variable is summed out
# - _Comments_: how the table shrinks and the two core operations
#
# **Parameters**:
# - `Factor`: which CPT to view as a factor
# - `Sum out`: which variable in the factor's scope to marginalize away
#
# **Key observations**:
# - A factor is just a table over a subset of variables
# - Two operations suffice for inference: pointwise product and summing out
# - Summing out a variable shrinks the table along that dimension

# %%
# Explore factors and the summing-out operation.
utils.cell3_1_factor_operations_widget()

# %% [markdown]
# - Everything in variable elimination is a factor
# - Multiply factors that share variables, then sum out the variable to remove
# - The result is a smaller factor, exactly the cached intermediate result

# %% [markdown]
# ## Cell 3.2: Variable Elimination Step by Step
#
# **Goal**:
# - Walk through variable elimination on the alarm query
# - Show how caching intermediate factors avoids the repeated enumeration work
# - Compare the operation count with enumeration
#
# **Plots**:
# - _Active factors_: the current factor scopes after each elimination step
# - _New factor_: the factor created at this step
# - _Posterior and op count_: the running posterior and the enumeration-vs-VE
#   operation comparison
# - _Comments_: order, step, and operation counts
#
# **Parameters**:
# - `Order`: the elimination order over the hidden variables
# - `step`: how many variables have been eliminated so far
#
# **Key observations**:
# - Variable elimination returns the identical posterior as enumeration
# - It uses far fewer operations by reusing cached factors
# - A good order keeps the intermediate factors small

# %%
# Step through variable elimination one variable at a time.
utils.cell3_2_variable_elimination_widget()

# %% [markdown]
# - Same answer, less work: variable elimination is enumeration with the repeated
#   subexpressions cached as intermediate factors
# - Order matters: it controls how big those factors get
# - The operation count is well below enumeration on this network

# %% [markdown]
# ## Cell 3.3: Pruning Irrelevant Variables
#
# **Goal**:
# - Show that variables that are not ancestors of the query or evidence
#   contribute nothing
# - Demonstrate that such variables can be removed before any computation
# - Confirm the posterior is unchanged after pruning
#
# **Plots**:
# - _Relevance DAG_: ancestors of query-or-evidence kept (green), the rest faded
# - _Full vs pruned posterior_: identical bars on the full and pruned networks
# - _Comments_: the irrelevant nodes and the unchanged posterior
#
# **Parameters**:
# - `Query X` and `observe <node>`: query and evidence (now over an extended
#   network with an extra $Neighbor$ leaf)
# - `prune irrelevant variables`: switch between full and pruned network
#
# **Key observations**:
# - A variable that is not an ancestor of the query or evidence sums to 1
# - Pruning is a free, correctness-preserving speedup
# - An unobserved effect node we are not asking about can be ignored

# %%
# Shade nodes by relevance and compare full vs pruned posteriors.
utils.cell3_3_pruning_widget()

# %% [markdown]
# - If a variable is neither asked about, observed, nor an ancestor of something
#   that is, it cannot affect the answer
# - Deleting it first leaves the posterior identical
# - This is why the unobserved $Neighbor$ leaf drops out of the computation

# %% [markdown]
# # Part 4: Complexity and Limits

# %% [markdown]
# ## Cell 4.1: Complexity: Polytrees vs General Graphs
#
# **Goal**:
# - Make concrete that exact inference is cheap on tree-shaped networks
# - Show that it blows up on densely connected networks
# - Relate elimination-order quality to the cost
#
# **Plots**:
# - _Polytree_: a chain network of the chosen size
# - _Dense network_: a fully connected network of the same node count
# - _Cost vs network size_: linear $O(n)$ vs exponential $O(2^n)$ on a log y-axis
# - _Comments_: the operating-point cost and the role of order quality
#
# **Parameters**:
# - `n`: number of nodes
# - `Structure`: polytree vs fully connected (sets the operating point)
# - `Order quality`: good vs bad (scales the constant)
#
# **Key observations**:
# - On polytrees exact inference is $O(n)$
# - On general networks cost can grow as $O(2^n)$: exact inference is NP-hard
# - Elimination order strongly affects cost

# %%
# Compare exact-inference cost on polytrees vs dense networks.
utils.cell4_1_complexity_widget()

# %% [markdown]
# - Exact inference is fast when the network is tree-like and intermediate
#   factors stay small
# - Dense connectivity makes those factors explode, and cost grows exponentially
# - Finding the optimal elimination order is itself a hard problem

# %% [markdown]
# ## Cell 4.2: When Exact Inference Breaks Down
#
# **Goal**:
# - Summarize the boundaries of exact inference
# - Motivate the approximate (sampling) methods covered next
# - Recall that continuous variables turn sums into integrals
#
# **Plots**:
# - _Regimes_: a table contrasting three regimes and their recommendation
# - _Continuous case_: a sketch showing $\sum_y \to \int dy$
# - _Comments_: the recommendation banner for the selected scenario
#
# **Parameters**:
# - `Scenario`: selects one of the three regimes and updates the recommendation
#
# **Key observations**:
# - Exact inference fails for large dense networks and for continuous variables
# - These failures motivate Monte Carlo and MCMC sampling
# - Exact methods remain the gold-standard reference on small networks

# %%
# Select a regime and read off the exact-vs-approximate recommendation.
utils.cell4_2_breakdown_widget()

# %% [markdown]
# - Exact inference is the right tool for small, discrete, tree-like networks
# - When the graph is large and dense, or variables are continuous, switch to the
#   approximate sampling methods covered next
# - Exact methods still validate the approximate ones on small problems
