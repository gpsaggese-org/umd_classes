# Create a Tutorial About Sampling

## Description

- Comprehensive tutorial covering fundamental and advanced sampling techniques used in probabilistic inference and machine learning
- Covers both foundational methods (uniform sampling, rejection sampling, importance sampling) and modern approaches (Gibbs sampling, MCMC, Hamiltonian Monte Carlo)
- Includes practical implementations with Python examples and visualizations to illustrate how different sampling methods behave
- Demonstrates when and why to use each sampling technique through real-world examples from Bayesian inference, generative models, and reinforcement learning
- Provides interactive code examples showing convergence behavior, computational efficiency, and accuracy trade-offs
- Suitable for students learning probabilistic graphical models, Bayesian statistics, and advanced machine learning

## Project Objective

Create an educational tutorial that teaches practitioners how to understand, implement, and apply sampling methods for probabilistic inference. The goal is to bridge theory and practice by explaining the mathematical foundations of sampling techniques while providing working code implementations and visual demonstrations of their behavior on real-world problems.

## Dataset Suggestions

- **UCI Machine Learning Repository**: https://archive.ics.uci.edu/ml/index.php
  - Contains diverse datasets for Bayesian inference tasks such as classification and clustering
  - Access: Free, direct download available
  - Use case: Demonstrate MCMC sampling on real classification problems

- **Kaggle Datasets**: https://www.kaggle.com/datasets
  - Wide variety of datasets for probabilistic modeling and inference tasks
  - Access: Free registration required
  - Use case: Apply importance sampling and Gibbs sampling to real-world prediction problems

- **PyMC Example Data**: https://github.com/pymc-devs/pymc/tree/main/pymc/data
  - Curated datasets specifically designed for Bayesian modeling tutorials
  - Access: Free, included with PyMC library
  - Use case: Follow established best practices with data used in production Bayesian workflows

- **Synthetic Toy Datasets**: Generate custom distributions programmatically
  - Create controlled examples with known ground truth distributions for visualization
  - Access: Generate on demand
  - Use case: Clearly demonstrate sampling behavior and convergence on simple, interpretable problems

## Tasks

- Implement and visualize uniform random sampling, rejection sampling, and importance sampling with example distributions
- Create interactive demonstrations showing convergence behavior of different MCMC methods (Metropolis-Hastings, Gibbs sampling)
- Build a comparison framework measuring computational cost and accuracy across sampling techniques
- Implement Hamiltonian Monte Carlo (HMC) and contrast with simpler MCMC approaches
- Develop tutorials covering sampling in mixture models, latent variable models, and Bayesian regression
- Create visualizations showing how proposal distributions affect MCMC acceptance rates and mixing

## Bonus Ideas

- Implement variational inference methods and compare with sampling-based approaches
- Add adaptive sampling techniques that learn proposal distributions during inference
- Build a practical guide on diagnosing MCMC convergence using trace plots and diagnostics
- Implement parallel tempering for sampling from multimodal distributions
- Create a web-based interactive tool for visualizing sampling in 2D and 3D distributions
- Develop benchmarks comparing sampling speed and accuracy on high-dimensional problems
- Include modern methods like automatic differentiation variational inference (ADVI) or neural posterior estimation

## Previous Research

- 2016, Stefano Ermon, CS 228 - Probabilistic Graphical Models, https://ermongroup.github.io/cs228-notes/inference/sampling/
  - Covers fundamental sampling algorithms and their application to probabilistic graphical models
  - Provides clear mathematical exposition of rejection sampling, importance sampling, and MCMC methods

- 2011, Andrew Gelman et al., "Bayesian Data Analysis", Chapman and Hall/CRC
  - Comprehensive textbook with chapters dedicated to MCMC methods and their practical implementation
  - Discusses convergence diagnostics, multiple chains, and best practices for Bayesian computation

- 2013, Yuri Burda et al., "Importance Weighted Autoencoders", https://arxiv.org/abs/1509.00519
  - Explores importance sampling in the context of deep generative models
  - Shows how to combine sampling with neural networks for flexible posterior approximation

- 2014, Alp Kucukelbir et al., "Automatic Variational Inference in Stan", https://arxiv.org/abs/1506.03431
  - Presents automatic differentiation variational inference as an alternative to sampling
  - Provides practical implementation details and comparisons with MCMC methods

- 2017, Michael Betancourt, "A Conceptual Introduction to Hamiltonian Monte Carlo", https://arxiv.org/abs/1701.02434
  - Clear exposition of Hamiltonian Monte Carlo with geometric intuition
  - Explains why HMC is more efficient than simpler MCMC methods for high-dimensional problems

- PyMC Documentation - Sampling and Inference, https://docs.pymc.io/
  - Production-ready implementations of modern sampling methods with practical examples
  - Extensive tutorials showing how to apply these methods to real Bayesian models
