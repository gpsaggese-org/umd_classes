---
title: "Why Should I Trust You: Explaining the Predictions of Any Classifier"
authors:
  - gpsaggese
date: 2026-01-15
description:
draft: true
categories:
  - AI Research
  - Machine Learning
---

TL;DR: LIME explains predictions of any classifier by fitting interpretable local models around specific instances.

<!-- more -->

Source: https://arxiv.org/pdf/1602.04938

# Introduction

- Trusting a prediction (so one can take some action based on it)
- Trusting a model (trust a model to behave in a reasonable way if deployed)

- How much the human understands a model's behavior?
  - Instead of seeing it as black box

- High stake decisions, e.g.,
  - Medical diagnosis
  - Terrorism detection

- Models are evaluated using accuracy metrics on validation data

# The case for explanations

- Explaining a prediction means presenting artifacts (text or images)
  to provide qualitative understanding between inputs and outputs

- Humans trust a prediction if an intelligible explanation is provided
  - E.g., providing explanations increases the acceptance of movie
    recommendations

- Interpretable:
  - must provide qualitative understanding between input variables and response
  - depends on the target audience, e.g., machine learning practitioners vs
    layman

- Local fidelity:
  - Often impossible to be completely faithful unless using the model itself
  - Locally faithful

- Model-agnostic
  - Treat the model as black box

# 3. LIME

## 3.1. Interpretable Data Representations

- Difference between
  - Features (what the model actually uses internally)
  - interpretable data representations (what humans can understand)

- For an explanation to be interpretable, it must be expressed in a
  representation a human can make sense of

- E.g.,
  - Text classification example:
    - A model might use word embeddings (complex, not human-friendly)
    - the interpretable representation = a binary vector showing whether each
      word is present or absent

  - Image classification example
    - A model might represent an image as a tensor of pixel
    - Interpretable representation: a binary vector indicating whether a patch of
      similar, contiguous pixels is present or absent.

## 3.2. Fidelity-Interpretability Trade-off

- LIME produces an explanation $\xi(x)$ by finding an interpretable model
  $g \in G$ that approximates the black-box model $f$ locally:
  $$
  \xi(x) = \arg\min_{g \in G} L(f, g, \pi_x) + \Omega(g)
  $$
- Key components:
  - **$G$**: class of interpretable models (linear models, decision trees,
    falling rule lists)
    - Domain of $g$ is $\{0,1\}^{d'}$: presence/absence of interpretable
      components
  - **$f: \mathbb{R}^d \to \mathbb{R}$**: black-box model being explained
    - In classification, $f(x)$ = probability or binary indicator for a class
  - **$\pi_x(z)$**: proximity measure between instance $z$ and point $x$,
    defines locality
  - **$L(f, g, \pi_x)$**: unfaithfulness of $g$ in approximating $f$ in the
    local neighborhood
  - **$\Omega(g)$**: complexity of explanation $g$
    - Decision tree: $\Omega(g)$ = tree depth
    - Linear model: $\Omega(g)$ = number of non-zero weights
- Objective: minimize $L$ (local fidelity) while keeping $\Omega(g)$ low
  (interpretability)
  - Both terms must be balanced: faithful but simple
- Formulation is general: supports different $G$, $L$, and $\Omega$

## 3.3 Sampling for Local Exploration
- Key intuition: LIME samples both near and far from $x$, then fits a
  locally faithful linear model (dashed line) that approximates the complex
  black-box boundary only in the local region

- Want to minimize $\mathcal{L}(f, g, \pi_x)$ without making assumptions about
  $f$ (model-agnostic requirement)

- Approach: approximate $\mathcal{L}$ by drawing samples weighted by $\pi_x$:
  - Sample instances around $x'$ by drawing nonzero elements of $x'$ uniformly
    at random
  - Given perturbed sample $z' \in \{0,1\}^{d'}$ (fraction of nonzero elements
    of $x'$), recover sample $z$ in original representation $\mathbb{R}^d$
  - Obtain label $f(z)$ from the black-box classifier
  - Repeat $N$ times to build dataset $\mathcal{Z}$

- Proximity kernel: $\pi_x(z) = \exp(-D(x,z)^2/\sigma^2)$
  - $D$ = cosine distance for text, $L2$ distance for images
  - Samples close to $x$ get high weight; samples far away get low weight

