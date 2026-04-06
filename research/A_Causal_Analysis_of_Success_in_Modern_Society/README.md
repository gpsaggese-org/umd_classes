# A Causal Analysis of Success in Modern Society

This project simulates talent-versus-luck dynamics in an agent-based model and
uses causal inference to quantify how much luck actually drives inequality.

## Quick Start

Build the image and launch Jupyter from the project directory.

```bash
cd research/A_Causal_Analysis_of_Success_in_Modern_Society
./docker_build.sh
./docker_jupyter.sh
```

For Docker build-system details, see the
[project template README](../../class_project/project_template/README.md).

## Notebooks

Work through the notebooks in the order listed below.

1. [`causal_success.API.ipynb`](causal_success.API.ipynb) walks through every
   building block on its own: the Agent class, the simulation engine, Gini
   metrics, policy simulation, and the Bayesian inference helpers.
2. [`causal_success.example.ipynb`](causal_success.example.ipynb) runs the
   full pipeline end to end, including DML and Causal Forest estimation and
   a comparison of five allocation strategies.

Reusable logic lives in [`causal_success_utils.py`](causal_success_utils.py).

## Changelog

2026-04-05: Cleanup pass against tutorial format rules. 2026-02-25: Initial release.
