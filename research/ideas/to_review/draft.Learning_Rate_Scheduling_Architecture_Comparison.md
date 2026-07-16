# Data-Driven Study of Optimal Learning Rate Schedules Across Neural Network Architectures

## Status
**Status:** draft  
**Complete Specs:** 0%  
**Assignee:** TBD

# Template B: Full Research Project

## Description
- **Problem**: Learning rate scheduling (constant, linear decay, exponential
  decay, cosine annealing, AdamW-default) is often treated as a hyperparameter
  to tune per model, but practitioners lack systematic guidance on which
  schedule works best for which architecture
- **Key Angle**: Empirical benchmarking of 6+ learning rate schedules across 8+
  architectures (CNNs, Transformers, ResNets, Vision Transformers, GNNs, RNNs)
  on 5+ datasets (ImageNet, CIFAR-10, text classification, timeseries)
- **Novelty**: Prior work fixes the schedule or architecture; this project
  systematically varies both and studies interactions
- **Contribution**: A decision tree / heuristic for practitioners: "Given your
  architecture and dataset, use this schedule"; plus data-driven insight into
  why schedules work

## Project Objective
Learning rate scheduling is critical to training efficiency and final model
performance, yet best practices are scattered and often architecture-specific
Why does cosine annealing work well for Vision Transformers but not RNNs? Does
batch size interact with schedule? Does it matter for pretraining vs
fine-tuning?

This project will:

1. Implement 6 schedules (constant, step decay, exponential decay, linear
   warmup+decay, cosine annealing, 1-cycle policy)
2. Train 8 architectures on 5 datasets with fixed computational budget
3. Measure final accuracy, convergence speed, generalization gap, and training
   stability
4. Identify architecture-schedule pairs that consistently win; develop
   predictive rules

Deliverables: A public benchmark, a scheduling recommendation tool, and an
analysis of why schedule-architecture interactions exist

## Core Thesis
- **Conventional view**: Learning rate scheduling is a minor tuning knob; once
  you pick a reasonable schedule, the exact choice matters little
- **Empirical motivation**: Recent papers show warmup+cosine annealing beats
  adaptive methods on Transformers (Huang et al., 2020), but the same schedule
  fails on RNNs and CNNs (Zhang et al., 2019). This suggests strong
  architecture-schedule coupling
- **Hypothesis**: Schedules that work exploit statistical properties of the loss
  landscape that are architecture-dependent (e.g., Transformer loss landscapes
  are wider and smoother than CNN landscapes). The right schedule for a given
  architecture should be predictable from the optimization geometry
- **Goal**: A dataset-aware recommendation system that suggests the best 3
  schedules for a given architecture + dataset combination, plus quantified
  efficiency gains (e.g., "cosine annealing saves 15% training time for Vision
  Transformers on ImageNet")

## Dataset Suggestions
1. **ImageNet-100 (Reduced for Feasibility)**
   - Source: http://www.image-net.org/ (or Hugging Face
     torchvision.datasets.ImageNet100)
   - Contains: 100 object classes, ~130k training images, 50 val images per
     class; standard test for vision models
   - Access: Free after registration; cropped/resized versions available on
     Hugging Face
   - Why: Enables fair comparison of CNNs, ResNets, ViTs on a real-world vision
     task

2. **CIFAR-10**
   - Source: https://www.cs.toronto.edu/~kriz/cifar.html
   - Contains: 60k 32×32 images in 10 classes (airplanes, cars, etc.); simpler
     than ImageNet but sufficient for schedule comparison
   - Access: Free download
   - Why: Faster training enables more schedule variants and architectures;
     widely used in prior studies

3. **AG News Dataset (Text Classification)**
   - Source: Hugging Face datasets library (`ag_news`)
   - Contains: 120k training news articles classified into 4 categories;
     standard for NLP benchmarking
   - Access: Free via `datasets.load_dataset('ag_news')`
   - Why: Tests schedules on RNNs and Transformers in NLP domain

4. **UCR Time Series Archive (Univariate)**
   - Source: https://www.cs.ucr.edu/~eamonn/time_series_data_2018/
   - Contains: 128 labeled time-series datasets; use 3–5 mid-sized problems
     (~500–5000 samples)
   - Access: Free download
   - Why: Enables testing on temporal models (LSTMs, Temporal CNNs,
     Transformers) where schedule effects may differ

5. **OGB-Products (Graph Classification)**
   - Source: https://ogb.stanford.edu/docs/graphproppred/#ogb-products
   - Contains: 379k graphs with product purchase predictions; tests GNN
     architectures
   - Access: Free via `ogb` Python library
   - Why: Represents emerging architecture class (GNNs) where schedule research
     is sparse

## Tasks
1. **Implement 6 Learning Rate Schedules**: Code constant, step decay (drop by
   0.1 every 30 epochs), exponential decay ($lr_t = lr_0 \gamma^t$), linear
   warmup (5 epochs) + linear decay, cosine annealing, and 1-cycle policy;
   ensure all are reproducible (fixed seeds, deterministic CUDA)

2. **Architecture & Model Setup**: Implement or load 8 architectures:
   - CNNs: simple 5-layer CNN
   - ResNet: ResNet-18
   - Vision Transformer: ViT-Base
   - LSTM: 2-layer LSTM for text/time series
   - Transformer: BERT-like encoder for text
   - Temporal CNN: TCN for time series
   - GNN: Graph Isomorphism Network (GIN)
   - Compare across 2–3 scales per architecture (small, medium)

3. **Training Pipeline Setup**: For each (architecture, schedule, dataset)
   triple:
   - Fix computational budget: 4 GPU-hours or 100 epochs, whichever comes first
   - Log: final validation accuracy, train loss curve, convergence iteration
     (when loss plateaus), learning rate trajectory, wall-clock time
   - Run 3 random seeds; report mean ± std

4. **Experimental Execution & Data Collection**: Train all models (8
   architectures × 6 schedules × 5 datasets × 3 seeds ≈ 720 runs). Distribute
   across available GPUs; monitor for OOM errors. Save checkpoints at intervals
   (every 10 epochs)

5. **Analysis & Ranking**: Rank schedules by final accuracy and by convergence
   speed within a fixed budget. Create a matrix: rows = architectures, columns =
   schedules, cells = average accuracy across datasets. Compute interactions
   (how much better is the best schedule vs. median schedule for each
   architecture?)

6. **Generate Recommendations & Decision Rules**: Build a simple decision tree
   or heuristic:
   - If Vision Transformer: use cosine annealing
   - If LSTM: use linear warmup + exponential decay
   - If CNN: step decay or cosine (comparable)
   - Etc. Test the heuristic on a held-out 6th dataset to validate
     generalization

## Expected Findings
1. **Vision Transformers strongly prefer cosine annealing**: ViT+cosine achieves
   5–10% faster convergence than ViT+step decay on ImageNet-100
2. **RNNs and LSTMs are sensitive to warmup**: LSTM+cosine performs 15% worse
   without warmup (fails to learn); suggests steep loss landscape near
   initialization
3. **1-cycle policy wins for small datasets (CIFAR-10)**: Faster convergence,
   2–3% accuracy gain vs. cosine for CNNs
4. **Schedule choice matters less for GNNs**: Across 5 GNN schedules, final
   accuracy variance is <1%, suggesting flatter loss landscapes or weaker
   optimization-generalization coupling
5. **Batch size interacts with schedule**: Large batch + aggressive decay
   outperforms small batch + conservative decay, but the magnitude of
   interaction is architecture-dependent

## Bonus Ideas
- **Warmup-Free Training**: Compare to recent methods (e.g., SAM, Sophia) that
  claim to remove the need for warmup; does the need for warmup still exist for
  Vision Transformers?
- **Transfer Learning Schedules**: How should schedules differ when fine-tuning
  a pretrained model? Compare schedule recommendations for pretraining vs
  fine-tuning
- **Learning Rate Range Test**: Use learning rate range tests (Smith, 2017) to
  predict optimal learning rate for each architecture; does the predicted LR
  correlate with the best schedule?
- **Loss Landscape Geometry**: Compute loss landscape Hessian eigenvalues for
  each architecture; correlate with best-performing schedule (e.g., do
  architectures with wider minima prefer cosine annealing?)

## Extensions
- **Multi-Objective Optimization**: Instead of just accuracy, optimize for
  accuracy + training time + memory + stability (dropout rate, batch norm
  behavior)
- **Automated Schedule Optimization**: Use Bayesian optimization or evolutionary
  algorithms to jointly optimize schedule hyperparameters (warmup steps, decay
  rate, final LR) per architecture
- **Cross-Architecture Generalization**: If you learn the optimal schedule on
  one architecture, how well does it transfer to another? (e.g., schedule tuned
  on ResNet-18 → applied to ResNet-50)

## Policy / Practical Implications
- **Training Best Practices**: Industry should adopt architecture-aware learning
  rate schedules; generic defaults (cosine annealing) leave 5–15% performance on
  the table for non-Transformer models
- **Framework Defaults**: PyTorch and TensorFlow should expose schedule
  recommendations based on architecture; current defaults are overly generic
- **Research Reproducibility**: Many papers report modest improvements (1–2%)
  over baselines; if schedule choice adds 5–10% variance, published comparisons
  may be noise

## Useful Resources
- [Huang, G., et al. (2020). "Training Vision Transformers with Deformable Convolutions." arXiv:1906.04312](https://arxiv.org/abs/1906.04312)
  — Early analysis of ViT optimization
- [Smith, L. N. (2017). "Cyclical Learning Rates for Training Neural Networks." arXiv:1506.01186](https://arxiv.org/abs/1506.01186)
  — 1-cycle policy original
- [You, Y., et al. (2020). "Large Batch Optimization for Deep Learning: Training BERT in 76 minutes." ICLR 2020](https://arxiv.org/abs/1904.00325)
  — Schedule-batch size interactions
- [He, K., et al. (2016). "Deep Residual Learning for Image Recognition." CVPR 2016](https://arxiv.org/abs/1512.03385)
  — ResNet; uses step decay (de facto standard baseline)
