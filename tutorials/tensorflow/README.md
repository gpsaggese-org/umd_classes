# TensorFlow & TensorFlow Probability Tutorial

This comprehensive 60-minute hands-on tutorial introduces you to TensorFlow and TensorFlow Probability through practical examples covering tensors, Keras neural networks, and structural time series forecasting.

## Getting Started

### Prerequisites

This tutorial runs in a Docker container with all dependencies pre-configured. No additional setup is required beyond the steps below.

### Setup Instructions

1. **Navigate to the tutorial directory:**
   ```bash
   cd tutorials/tensorflow
   ```

2. **Build the Docker image:**
   ```bash
   ./docker_build.sh
   ```

3. **Launch Jupyter Lab:**
   ```bash
   ./docker_jupyter.sh
   ```

## Dependency Management

This project uses `uv` for efficient Python dependency management within the Docker container. The system works as follows:

- **`requirements.in`** — Lists top-level package dependencies
- **`requirements.txt`** — Auto-generated pinned versions for reproducibility

The Docker container comes with all dependencies pre-compiled and synced. If you need to update dependencies manually:

```bash
# Compile top-level packages into pinned requirements
uv pip compile requirements.in -o requirements.txt

# Sync the environment with the compiled list
uv pip sync requirements.txt
```

## Tutorial Notebooks

Work through the following notebooks in order:

1. **`tensorflow.API.ipynb`** — Core TensorFlow fundamentals
   - Tensors and tensor operations
   - Automatic differentiation
   - Keras regression models
   - TensorFlow Probability distributions

2. **`tensorflow.example.ipynb`** — Structural time series forecasting
   - Building trend and seasonality components
   - Incorporating holiday effects
   - Autoregressive modeling
   - End-to-end forecasting pipeline

