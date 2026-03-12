---
title: "Autogen in 60 Minutes"
authors:
  - PranavShashidhara
  - gpsaggese
date: 2026-02-21
description:
categories:
  - AI Research
  - Software Engineering
---
TL;DR: Learn how to build machine learning models using TensorFlow in 60 minutes with
hands-on examples including neural networks and structural time series
forecasting.
 
<!-- more -->
 
This tutorial's goal is to show you in 60 minutes:
 
  - The core APIs of TensorFlow (tensors, variables, automatic differentiation)
  - How to build and train neural networks with Keras
  - Probabilistic modeling with TensorFlow Probability distributions and
    Bayesian inference
 
## TensorFlow in 30 Seconds
 
TensorFlow is an open-source machine learning framework from Google for building
and training neural networks and probabilistic models.
 
Key capabilities:
 
- **Tensors and automatic differentiation**: Immutable multi-dimensional arrays
  optimized for CPUs, GPUs, and TPUs with efficient gradient computation
- **Keras API**: High-level interface for rapidly building and training neural
  networks
- **TensorFlow Probability**: Probabilistic programming for Bayesian inference
  and uncertainty quantification
- **Interpretable models**: Structural decomposition reveals which components
  drive predictions
 
## Official References
 
- [TensorFlow: An Open Source Machine Learning Framework](https://www.tensorflow.org/)
- [TensorFlow Probability](https://www.tensorflow.org/probability)
 
## Tutorial Content
 
This tutorial includes all the code, notebooks, and Docker containers in
`tutorials/tensorflow/`.
 
- `tutorials/tensorflow/README.md`: Instructions and setup for the tutorial
  environment
- A Docker system to build and run the environment using our standardized
  approach
- `tensorflow.API.ipynb`: Tutorial notebook focusing on core APIs and
  fundamentals
- `tensorflow.example.ipynb`: Advanced end-to-end structural time series
  forecasting example
- `tensorflow_utils.py`: Utility functions required by `tensorflow.example.ipynb`
 
## `tensorflow.example.ipynb`
 
This notebook provides a practical, end-to-end example of using TensorFlow
Probability to demonstrate structural time series forecasting.
 
### Part 1: Data Generation
 
We generate a realistic synthetic daily time series that combines:
- A linear trend (slow upward drift)
- Weekly seasonality with stochastic drift
- Holiday effects (additive spikes on Christmas each year)
- AR(1) autoregression to capture temporal dependence
- Gaussian observation noise 

### Part 2: Model Building
 
The STS model decomposes the observed series into four interpretable components:
 
| Component | Purpose |
|---|---|
| `LocalLinearTrend` | Captures slow-moving level and slope |
| `Seasonal` (7 seasons) | Weekly day-of-week effects |
| `Autoregressive` (AR-1) | Short-term temporal dependence |
| `LinearRegression` | Additive holiday spikes |
 
The components are summed into a `tfp.sts.Sum` model.
 
**Variational Inference**
 
We approximate the posterior over model parameters using Variational Inference (VI):
1. Define a factored surrogate posterior `q(θ)` (one Normal per parameter)
2. Maximise the ELBO: `ELBO = E_q[log p(y, θ)] - KL(q || prior)`
3. Use the Adam optimiser for gradient-based optimisation
 
### Part 3: Forecasting and Evaluation
 
With the fitted posterior we:
1. Decompose the training signal into its constituent components
2. Forecast `num_steps_forecast` steps into the future
3. Evaluate using MAE and MSE