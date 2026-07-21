# DoWhy Tutorial

Dockerized tutorial for [DoWhy](https://github.com/py-why/dowhy), the PyWhy
library for causal inference. Pairs with the "Causal AI and Decision Making"
book; Part 8 of the example notebook lists the chapter mapping.

## Quick Start

- Build and launch the container:
  ```bash
  > cd tutorials/DoWhy
  > ./docker_build.sh
  > ./docker_jupyter.sh
  ```
- Work through the notebooks in order:
  1. [`dowhy.API.ipynb`](dowhy.API.ipynb): model, identify (backdoor, frontdoor,
     IV), estimate, and refute on synthetic data with a known ground truth.
  2. [`dowhy.example.ipynb`](dowhy.example.ipynb): end-to-end causal analysis
     of the Lalonde job training program, covering estimation, the refutation
     suite, sensitivity to unobserved confounding, and SCM-based
     counterfactuals via `dowhy.gcm`.
- [`dowhy_utils.py`](dowhy_utils.py) holds the helper functions both notebooks
  call.

For Docker build-system details, see the
[project template README](../../class_project/project_template/README.md). See
[CHANGELOG.md](CHANGELOG.md) for revision history.
