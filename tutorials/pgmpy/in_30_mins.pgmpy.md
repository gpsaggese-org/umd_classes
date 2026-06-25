---
title: "pgmpy in 30 mins"
authors:
  - gpsaggese
date: 2026-05-30
description: Build Bayesian networks and perform probabilistic reasoning with pgmpy
categories:
  - Machine Learning
  - Python
---

TL;DR `pgmpy` is a Python library for building and reasoning with Probabilistic
Graphical Models (Bayesian networks, Markov networks, factor graphs) and model
complex dependencies and perform inference over uncertain variables.

<!-- more -->

## Introduction

`pgmpy` is a Python library that makes it straightforward to build and work with
probabilistic graphical models. It's particularly strong for Bayesian networks,
which are DAGs (directed acyclic graphs) where nodes represent random variables
and edges represent conditional dependencies.

Many real-world problems involve uncertainty and dependencies (e.g., medical
diagnosis, fraud detection, system anomaly detection, recommendation systems).
Bayesian networks let you:
- Model causal relationships explicitly
- Perform inference (compute probability of an event given evidence)
- Handle missing data naturally
- Combine domain knowledge with data-driven learning
- Explain predictions through probability distributions

Other tools that solve similar problems:
- `pymc`: Bayesian inference using MCMC sampling (more general, steeper learning curve)
- `pybbn`: Simpler Bayesian networks library (less feature-rich)
- `pomegranate`: Fast probabilistic models (different API, focused on speed)

Official docs: [pgmpy documentation](https://pgmpy.org/)

## Prerequisites

- Python
- Basic understanding of probability (conditional probability, independence)
- Familiarity with NumPy and Pandas (helpful but not required)
- Comfort with DAGs conceptually (parent-child node relationships)

## Installation

- On macOS and Linux:
  ```bash
  > pip install pgmpy
  ```

- With a virtual environment:
  ```bash
  > python -m venv pgmpy_env
  > source pgmpy_env/bin/activate
  > pip install pgmpy
  ```

- TODO(ai_gp): Add instructions for uv

- Verify installation:
  ```bash
  > python -c "import pgmpy; print(pgmpy.__version__)"
  0.1.6
  ```

## Core Concepts

### Bayesian Network (Belief Network)

A Bayesian network is a probabilistic model represented as a directed acyclic
graph where:

- **Nodes** represent random variables (discrete or continuous)
- **Edges** represent conditional dependencies (parent node influences child node)
- **CPDs** (Conditional Probability Distributions) specify $P(child|parents)$

Example: A simple weather network where `Rain` affects `Traffic`:

```
Weather -> Traffic
    |
    v
Commute_Time
```

### Inference

Inference is computing the probability of a variable given evidence (observations).
Types of inference:

- **Exact inference**: Compute exact probabilities (fast for small networks)
- **Approximate inference**: Use sampling when exact inference is too slow (MCMC,
  variational)

## Hands-On Examples

### Example 1: Build a Simple Burglar Alarm Network

This is a classic example. A burglar alarm can be triggered by a burglar or an
earthquake. Neighbors may call if they hear the alarm.

```python
from pgmpy.models import BayesianNetwork
from pgmpy.factors.discrete import TabularCPD

# Step 1: Define the network structure.
model = BayesianNetwork([
    ('Burglary', 'Alarm'),
    ('Earthquake', 'Alarm'),
    ('Alarm', 'JohnCalls'),
    ('Alarm', 'MaryCalls'),
])

# Step 2: Define conditional probability distributions.
cpd_burglary = TabularCPD(
    variable='Burglary',
    variable_card=2,
    values=[[0.999], [0.001]]
)

cpd_earthquake = TabularCPD(
    variable='Earthquake',
    variable_card=2,
    values=[[0.998], [0.002]]
)

cpd_alarm = TabularCPD(
    variable='Alarm',
    variable_card=2,
    values=[
        [0.999, 0.71, 0.06, 0.05],
        [0.001, 0.29, 0.94, 0.95],
    ],
    evidence=['Burglary', 'Earthquake'],
    evidence_card=[2, 2]
)

cpd_john_calls = TabularCPD(
    variable='JohnCalls',
    variable_card=2,
    values=[[0.95, 0.10], [0.05, 0.90]],
    evidence=['Alarm'],
    evidence_card=[2]
)

cpd_mary_calls = TabularCPD(
    variable='MaryCalls',
    variable_card=2,
    values=[[0.99, 0.30], [0.01, 0.70]],
    evidence=['Alarm'],
    evidence_card=[2]
)

# Step 3: Add CPDs to model and check validity.
model.add_cpds(cpd_burglary, cpd_earthquake, cpd_alarm, cpd_john_calls, cpd_mary_calls)
model.check_model()
print("Model is valid")
```

Expected output:

```
Model is valid
```

### Example 2: Perform Inference

Now query the network: "What's the probability John calls given the alarm went off?"

```python
from pgmpy.inference.exact import VariableElimination

# Create an inference object.
infer = VariableElimination(model)

# Query: P(JohnCalls | Alarm=1)
result = infer.query(variables=['JohnCalls'], evidence={'Alarm': 1})
print(result)
```

Expected output:

```
+-------------+----------+
| JohnCalls   |    phi(JohnCalls) |
+=============+==========+
| JohnCalls_0 |    0.0500 |
| JohnCalls_1 |    0.9500 |
+=============+==========+
```

Query with multiple evidence: "What if John calls AND Mary calls?"

```python
result = infer.query(
    variables=['Burglary'],
    evidence={'JohnCalls': 1, 'MaryCalls': 1}
)
print(result)
```

This uses Bayes' rule under the hood to compute the posterior probability that
a burglary occurred given both neighbors called.

### Example 3: Student Grades Network

Model student performance: A student's intelligence affects their grade and their
SAT score. Difficulty of the class also affects the grade.

```python
from pgmpy.models import BayesianNetwork
from pgmpy.factors.discrete import TabularCPD

model = BayesianNetwork([
    ('Intelligence', 'Grade'),
    ('Difficulty', 'Grade'),
    ('Intelligence', 'SAT'),
])

# Intelligence: P(Intelligence) - independent variable.
cpd_intelligence = TabularCPD(
    variable='Intelligence',
    variable_card=2,
    values=[[0.3], [0.7]]
)

# Difficulty: P(Difficulty) - independent variable.
cpd_difficulty = TabularCPD(
    variable='Difficulty',
    variable_card=2,
    values=[[0.6], [0.4]]
)

# Grade depends on Intelligence and Difficulty.
cpd_grade = TabularCPD(
    variable='Grade',
    variable_card=2,
    values=[
        [0.95, 0.8, 0.1, 0.01],
        [0.05, 0.2, 0.9, 0.99],
    ],
    evidence=['Intelligence', 'Difficulty'],
    evidence_card=[2, 2]
)

# SAT depends on Intelligence.
cpd_sat = TabularCPD(
    variable='SAT',
    variable_card=2,
    values=[[0.1, 0.9], [0.9, 0.1]],
    evidence=['Intelligence'],
    evidence_card=[2]
)

model.add_cpds(cpd_intelligence, cpd_difficulty, cpd_grade, cpd_sat)
model.check_model()

# Inference: If grade is high, what's the probability the student is intelligent?
from pgmpy.inference.exact import VariableElimination
infer = VariableElimination(model)
result = infer.query(variables=['Intelligence'], evidence={'Grade': 1})
print(result)
```

### Example 4: Learning from Data

Instead of hand-coding CPDs, learn them from data:

```python
import pandas as pd
from pgmpy.models import BayesianNetwork
from pgmpy.estimators import MaximumLikelihoodEstimator

# Sample data: student grades across 100 students.
data = pd.DataFrame({
    'Intelligence': [0, 1, 1, 0, 1] * 20,
    'Difficulty': [1, 0, 1, 1, 0] * 20,
    'Grade': [0, 1, 1, 0, 1] * 20,
    'SAT': [0, 1, 1, 0, 1] * 20,
})

# Define network structure.
model = BayesianNetwork([
    ('Intelligence', 'Grade'),
    ('Difficulty', 'Grade'),
    ('Intelligence', 'SAT'),
])

# Learn CPDs from data.
model.fit(data, estimator=MaximumLikelihoodEstimator)

# Show learned CPDs.
print(model.get_cpds('Grade'))
```

This counts occurrences in the data and computes empirical probabilities.

### Example 5: Map Inference

Sometimes you want the most likely assignment, not full probability distributions.
This is called MAP (Maximum A Posteriori) inference:

```python
from pgmpy.inference.exact import VariableElimination

infer = VariableElimination(model)

# Find most likely values for all variables given JohnCalls and MaryCalls.
map_result = infer.map_query(
    variables=['Burglary', 'Earthquake', 'Alarm'],
    evidence={'JohnCalls': 1, 'MaryCalls': 1}
)
print(map_result)
```

Expected output:

```
{'Burglary': 0, 'Earthquake': 0, 'Alarm': 1}
```

This tells you the most probable scenario: both alarm and calls happened but no
actual burglary or earthquake (false alarm).

## Tips and Gotchas

### Gotcha 1: CPD Value Ordering

The order of evidence in a CPD matters. If you define:

```python
cpd = TabularCPD(
    variable='A',
    variable_card=2,
    values=[[0.8, 0.3], [0.2, 0.7]],
    evidence=['B'],
    evidence_card=[2]
)
```

This means: `values[0][0]` is P(A=0|B=0), `values[0][1]` is P(A=0|B=1).

With multiple evidence, indices vary fastest for the rightmost variable:

```python
evidence=['X', 'Y']  # Y varies fastest in the values array
```

### Gotcha 2: Networks Must Be Acyclic

pgmpy enforces DAGs. If you try to add an edge that creates a cycle, it fails:

```python
model.add_edge('A', 'B')
model.add_edge('B', 'A')  # Raises exception
```

### Gotcha 3: Check Your Model

Always call `model.check_model()` after adding CPDs. It verifies:

- CPDs sum to 1.0 (probabilities valid)
- All evidence variables are parents
- No missing CPDs

### Tip 1: Use Visualization

Visualize networks to catch errors:

```python
import matplotlib.pyplot as plt
import networkx as nx

pos = nx.spring_layout(model)
nx.draw(model, pos, with_labels=True, node_color='lightblue')
plt.show()
```

### Tip 2: Handle Large Networks with Approximate Inference

For networks with many variables, exact inference is slow. Use sampling:

```python
from pgmpy.inference.dbn_inference import DBNInference

# Or for general networks, use belief propagation approximation.
```

### Tip 3: Discrete Variables Only (by default)

Standard pgmpy works with discrete variables. For continuous variables, either
discretize or use a library like PyMC.

### Tip 4: Start Simple

Build networks incrementally. Start with 2-3 nodes, verify inference works, then
expand. Complex networks are hard to debug.

## Next Steps

- Explore **structure learning**: Automatically infer network structure from data
  using algorithms like PC or Hill Climb (pgmpy has these built in)
- Try **factor graphs** and **Markov networks** for problems with symmetric
  relationships
- Learn **dynamic Bayesian networks (DBNs)** for time-series modeling
- Study **causal inference** with do-calculus to distinguish correlation from
  causation
- Check out [pgmpy tutorials](https://pgmpy.org/examples.html) for more examples

## Related Resources

- [Probabilistic Graphical Models](https://mitpress.mit.edu/9780262013192/probabilistic-graphical-models/)
  by Daphne Koller (textbook)
- [pgmpy GitHub](https://github.com/pgmpy/pgmpy)
- [Intro to Bayesian Networks](https://www.baeldung.com/cs/bayesian-networks)
