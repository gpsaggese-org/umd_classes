# gCastle Tutorial

A hands-on tutorial for learning **causal structure discovery** with gCastle,
Huawei's comprehensive causal discovery toolchain. Learn to identify causal
relationships in your data using multiple algorithms and evaluation metrics.

## Quick Start

From the root of the repository:

```bash
cd tutorials/gCastle
./docker_build.sh
./docker_jupyter.sh
```

Then open your browser to http://localhost:8888 and work through the notebooks
in order:

1. **`gCastle.API.ipynb`** (20 minutes)
   - Learn the core gCastle APIs
   - Generate synthetic causal data
   - Run constraint-based (PC), score-based (GES), and gradient-based (NOTEARS) algorithms
   - Evaluate results with standard metrics (F1, SHD, TPR, FDR)

2. **`gCastle.example.ipynb`** (25 minutes)
   - Complete application: discovering causal relationships in economic data
   - Compare algorithm performance on realistic data
   - Interpret and visualize learned causal structures

## Key Concepts

**gCastle** provides tools for causal discovery—learning the causal structure
of a system from observational data:

- **Constraint-based methods** (e.g., PC): Use independence tests to discover
  structure
- **Score-based methods** (e.g., GES): Optimize over possible DAG structures
- **Gradient-based methods** (e.g., NOTEARS): Use continuous optimization with
  acyclicity constraints

Each approach has different computational profiles and assumptions, making them
suitable for different data scenarios.
