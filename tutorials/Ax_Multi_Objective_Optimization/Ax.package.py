# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.19.0
#   kernelspec:
#     display_name: msml610-project
#     language: python
#     name: python3
# ---

# %% [markdown]
# # 1. Ax - Multi-Objective Optimization for Marketing Campaigns
#
# Adaptive Experimentation (Ax) is an open-source tool created and maintained by The Meta Adaptive Experimentation Team initially for internal use and open to the public.
#
# Ax is a platform to optimize almost any type of experiment. It's well suited when the experiment complies with a few characteristics:
#
# - The **benefit** or **outcome** can be measured or quantified.
# - The **benefit** or **outcome** cannot be calculated from the **inputs**. There is no formula that can be used to calculate the **benefit** or **outcome** from the **inputs**. The only way to know the result is to run an experiment.
# - The **cost** of running an experiment is elevated and the number of experiments has to be reduced to a minimum.

# %% [markdown]
# ## 1.1. Bayesian Optimization
#
# Ax optimization algorithms are based on Bayesian Optimization. Internal implementation is based on [BoTorch](https://botorch.org/) a library for Bayesian Optimization built on top of PyTorch.

# %% [markdown]
# ## 1.2. Adaptive Experimentation
#
# Adaptive Experimentation is a technique to optimize experiments based on the results of the previous experiments. It is a way to find the best configuration of the experiment parameters to maximize the **benefit** or **outcome** while minimizing the **cost** of running the experiment.
#
# The basic adaptive experimentation flow works as follows (2):
# - Configure your optimization experiment, defining the space of values to search over, objective(s), constraints, etc.
# - Suggest new trials, to be evaluated one at a time or in a parallel (a “batch”)
# - Evaluate the suggested trials by executing the black box function and reporting the results back to the optimization algorithm
# - Repeat steps 2 and 3 until a stopping condition is met or the evaluation budget is exhausted
#
# Bayesian optimization, one of the most effective forms of adaptive experimentation, intelligently balances tradeoffs between exploration (learning how new parameterizations perform) and exploitation (refining parameterizations previously observed to be good).

# %% [markdown]
# # 2. Ax API
#
# ## 2.1. Overview
#
# The following diagram shows the main components of the Ax API and the steps to run an Adaptive Experiment:
#
# ![Ax API](images/ax-api.png)
#
# The library is organized around the following main components:
#
# - **Client**: The main module that will create an Experiment, return the Trials to be evaluated and store the results.
# - **Experiment**: The entity that contains the configuration and all the information about the current experiment.
# - **OptimizationConfig**: Defines the optimization problem, the inputs, outputs, and constraints.
# - **Trial**: A new trial is generated on each iteration. It contains the inputs to be evaluated (Also called Arm)
# - **GenerationStrategy**: The entity that generates the new inputs to be evaluated. It leverages different strategies on different stages (Sobol, Transfer-Learning BayesOpt, BoTorch)
#
# ![image](images/ax-api-experiment.png)
#
# For more information, see the [Ax Glossary](https://ax.dev/docs/glossary)

# %% [markdown]
# ## 2.2. API Reference
#
# Only the most important modules and methods are documented here. For more detailed information, see the [Ax API Reference](https://ax.readthedocs.io/en/stable/)
#
# - `Client`
#   - `configure_experiment`: Receives an ExperimentConfig. Creates the Experiment Object. No value is returned, the Client is stateful.
#   - `configure_optimization`: Receives the `objective` expression and outcome constraints. Outcome constraints are optional and define when the optimization should stop.
#   - `get_next_trials`: Receives the number of trials to generate in parallel. Returns a list of Trials. Each Trial will contain a suggested input to be evaluated.
#   - `complete_trial`: Receives the result of the evaluation of the Trial. Ax will update the Experiment with the result. Metadata can be attached for future reference.
#   - `get_best_parameterization`: Returns the Trial or input values that maximized the objective function.
#   - `compute_analyses`: Renders multiple visualizations of the experiment results. The visualization methods to render can be passed as a parameter.
#   - `get_pareto_frontier`: If the Experiment has been defined with two or more objectives, this method returns the list of tuples which are part of the Pareto frontier.
# - `IRunner`: Abstract class that can be implemented to define a experiment that's delegated to an external service to be completed asynchronously. Defines the methods `run_trial` and `poll_trial`.
# - `IMetric`: Abstract class that works together with the `IRunner` object to retrieve the results from an external service.

# %% [markdown]
# # 3. Hartmann Function Optimization
#
# To demonstrate the usage of the Ax API, we will use the Hartmann Function in 6 dimensions. This function is a common benchmark for optimization problems and it's demonstrated in the Ax documentation.
#
# The Hartmann Function is defined as:
#
# $$
# f(\mathbf{x}) = -\sum_{i=1}^{4} \alpha_i \exp \left( -\sum_{j=1}^{6} A_{ij} (x_j - P_{ij})^2 \right)
# $$
#
# It's definition makes this function to have multiple local optima and one global optima.
#
# The following is a visualization of a Hartmann Function in 2 dimensions:
#
# ![Hartmann Function](images/hartmann-2d.png)
#
# ## 3.1. Install Dependencies

# %%
# # %load_ext autoreload
# # %autoreload 2
# %matplotlib inline

# Install AX with the extension for Jupyter notebooks
# ! pip3 install "ax-platform[notebook]" joblib --break-system-packages

# Import the necessary packages

from Ax_utils import hartmann6
import numpy as np
from ax.api.client import Client
from ax.api.configs import RangeParameterConfig
import matplotlib.pyplot as plt

# %% [markdown]
# ## 3.2. Initialize the Client and Setup the Experiment

# %%
# Create the Ax Client
client = Client()

# The Hartmann function has 6 variables that go between 0 and 1.
parameters = [
    RangeParameterConfig(name="x1", parameter_type="float", bounds=(0, 1)),
    RangeParameterConfig(name="x2", parameter_type="float", bounds=(0, 1)),
    RangeParameterConfig(name="x3", parameter_type="float", bounds=(0, 1)),
    RangeParameterConfig(name="x4", parameter_type="float", bounds=(0, 1)),
    RangeParameterConfig(name="x5", parameter_type="float", bounds=(0, 1)),
    RangeParameterConfig(name="x6", parameter_type="float", bounds=(0, 1)),
]

client.configure_experiment(parameters=parameters)

# %% [markdown]
# ## 3.3. Configure the Optimization Problem
#
# In this case we want to minimize the result of the Hartmann function.

# %%
# The "-" sign transforms this into a minimization problem.
client.configure_optimization(objective="-hartmann")

# %% [markdown]
# Call the Hartmann function in the Utils file to verify it works.

# %%
hartmann6(0.1, 0.45, 0.8, 0.25, 0.552, 1.0)

# %% [markdown]
# ## 3.4. Define the Optimization Loop
#
# N number of trials can be run in parallel. This may accelerate the optimization process but will require more experiments to be conducted in total.

# %%
for _ in range(10):
    # Request a series of inputs to Ax client
    trials = client.get_next_trials(max_trials=5)

    # Conduct the experiments (5 times in this case)
    for trial_index, parameters in trials.items():
        x1 = parameters["x1"]
        x2 = parameters["x2"]
        x3 = parameters["x3"]
        x4 = parameters["x4"]
        x5 = parameters["x5"]
        x6 = parameters["x6"]

        result = hartmann6(x1, x2, x3, x4, x5, x6)

        # Send the results back to Ax with the trial index for reference
        client.complete_trial(
            trial_index=trial_index, raw_data={"hartmann": result}
        )

# %% [markdown]
# The logs show how Ax tells us to try different values combinating Exploration and Exploitation. This means, finding a balance between trying the best values known at the moment and exploring new ones.

# %%
best_parameters, prediction, index, name = client.get_best_parameterization()
print("Best Parameters:", best_parameters)
print("Prediction (mean, variance):", prediction)

# %% [markdown]
# The experiment, after 95 trials defined the minimum value found for the Hartmann function is -3.31.
#
# We known the global minimum is -3.32, so the experiment found a good solution in a limited number of trials, taking into consideration it had to navigate 6 dimensions in a problem with multiple local optima.

# %% [markdown]
# ## 3.5. Get Visualizations
#
# Ax default visualizations show many aspects of the optimization process. Among them, the evolution of the output metric over time.

# %%
cards = client.compute_analyses(display=True)

# %% [markdown]
# ## 4. Multi-Objective Optimization
#
# Now we will define a Multi-Objective Optimization problem. We will still use the Hartmann function but we will define two objectives:
#
# - Minimize the Hartmann function
# - Minimize the distance to the point (0.1, 0.1, 0.1, 0.1, 0.1, 0.1)
#
# The last objective is something we just made up to test the multi-objective capabilities of Ax.

# %%
client = Client()

parameters = [
    RangeParameterConfig(name="x1", parameter_type="float", bounds=(0, 1)),
    RangeParameterConfig(name="x2", parameter_type="float", bounds=(0, 1)),
    RangeParameterConfig(name="x3", parameter_type="float", bounds=(0, 1)),
    RangeParameterConfig(name="x4", parameter_type="float", bounds=(0, 1)),
    RangeParameterConfig(name="x5", parameter_type="float", bounds=(0, 1)),
    RangeParameterConfig(name="x6", parameter_type="float", bounds=(0, 1)),
]

client.configure_experiment(parameters=parameters)

# Minimize the Hartmann function and the distance
# Multi-Objective Optimization allows us to define constraints in the objective function. In this case we are not making use of it
client.configure_optimization(
    objective="-hartmann, -distance", outcome_constraints=[]
)

# In this case we may need more trials for the multi-objective optimization to converge
for _ in range(20):
    # Request a series of inputs to Ax client
    trials = client.get_next_trials(max_trials=5)

    # Conduct the experiments (5 times in this case)
    for trial_index, parameters in trials.items():
        x1 = parameters["x1"]
        x2 = parameters["x2"]
        x3 = parameters["x3"]
        x4 = parameters["x4"]
        x5 = parameters["x5"]
        x6 = parameters["x6"]

        result = hartmann6(x1, x2, x3, x4, x5, x6)

        distance = np.linalg.norm(
            np.array([x1, x2, x3, x4, x5, x6])
            - np.array([0.1, 0.1, 0.1, 0.1, 0.1, 0.1])
        )

        # Send the results back to Ax with the trial index for reference
        client.complete_trial(
            trial_index=trial_index,
            raw_data={"hartmann": result, "distance": distance},
        )

# %%
frontier = client.get_pareto_frontier()
for parameters, metrics, trial_index, arm_name in frontier:
    print(
        f"Trial {trial_index} - {arm_name} - Metrics: {metrics} - Parameters: {parameters}"
    )

# %%
distances = []
hartmanns = []
for parameters, metrics, trial_index, arm_name in frontier:
    distances.append(metrics["distance"])
    hartmanns.append(metrics["hartmann"])

plt.figure(figsize=(8, 6))
plt.scatter(distances, hartmanns, c="blue", edgecolor="k", alpha=0.7)
plt.xlabel("distance")
plt.ylabel("hartmann")
plt.title("Pareto Frontier: Distance vs Hartmann")
plt.grid(True)
plt.show()

# %% [markdown]
# The previous plot shows the Pareto Frontier and how we can find a better minimum for the Hartmann function while a larger distance is allowed. This will tell us how much we can keep optimizing as we keep moving from the epicenter.
#
# In this case much more experiments have to be conducted and they are not enough to find the global minimum.

# %% [markdown]
# # 5. References
#
# 1. [Ax - Why Ax?](https://ax.dev/docs/why-ax)
# 2. [Ax - Adaptive Experimentation](https://ax.dev/docs/intro-to-ae)
# 3. [BoTorch: A Framework for Efficient Monte-Carlo Bayesian Optimization](https://arxiv.org/abs/1910.06403)
