# gCastle Tutorial

Learn causal structure discovery with gCastle in 60 minutes. gCastle is a causal
structure learning toolchain that enables researchers to discover causal
relationships in data through various algorithms and evaluation metrics.

## Quick Start

From the root of the repository, navigate to the gCastle tutorial folder and
build the Docker container:

```bash
cd tutorials/gCastle
./docker_build.sh
```

Once the Docker image is built, launch Jupyter Lab:

```bash
./docker_jupyter.sh
```

Open your browser to `http://localhost:8888` and work through the following
notebooks in order:

1. **`gCastle.API.ipynb`**: Learn the core APIs, data generation, normalization,
   and evaluation metrics. Discover how to run individual causal discovery
   algorithms and visualize causal graphs.

2. **`gCastle.example.ipynb`**: Complete end-to-end workflow including data
   generation, causal discovery with multiple algorithms, algorithm comparison,
   and interpretation of results.

For more information about the Docker setup, refer to the [Project template
readme](/class_project/project_template/README.md).

## References

- **gCastle Documentation**: https://gcastle.readthedocs.io
- **Published Paper**: Jiang et al. (2021) "gCastle: A Python Toolchain for
  Causal Structure Learning and Causal Effect Estimation"
