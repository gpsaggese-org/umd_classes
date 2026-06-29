# Model Explainability Tutorial

Learn how to explain machine learning models in 60 minutes using interpretable
models, SHAP, LIME, permutation importance, and counterfactuals.

## Quick Start

- From the root of the repository:
  ```bash
  > cd tutorials/ml_explainability
  > ./docker_build.sh
  > ./docker_jupyter.sh
  ```

- Open your browser to http://localhost:8888 and work through the notebooks in
  order:
  1. `explainability_shap_lime.API.ipynb`: core API of each explainability tool
  2. `explainability_shap_lime.example.ipynb`: end-to-end explanation of a model
     trained on a real dataset

- For Docker build system details see the
  [project template README](../../class_project/project_template/README.md)

## Introduction

- Model explainability answers a simple question: _why did the model make this
  prediction?_

- Modern models (gradient boosting, random forests, neural nets) are accurate
  but opaque. You get a number out, with no reason attached. Explainability
  techniques recover that reason, either for the model as a whole (global) or for
  a single prediction (local).

- Use explainability when:
  - You must justify a decision to a regulator, customer, or domain expert (e.g.,
    loan denial, medical diagnosis)
  - You want to debug a model that performs well on metrics but behaves strangely
  - You want to check that the model relies on sensible features, not on leakage
    or spurious correlations
  - You need to build trust with stakeholders before deploying

- Do not reach for explainability when a simple, inherently interpretable model
  (linear regression, a small decision tree) already meets your accuracy target.
  In that case the model explains itself.

- This tutorial covers five complementary approaches:
  - Interpretable models (`sklearn.linear_model`, `pygam`)
  - Permutation importance (`sklearn.inspection`)
  - SHAP (`shap`)
  - LIME (`lime`)
  - Counterfactual explanations (`dice-ml`)

- Other tools in this space:
  - `eli5`: unified API over several explainers
  - `interpret` (Microsoft): glassbox models and dashboards
  - `captum`: gradient-based attribution for PyTorch models
  - `alibi`: counterfactuals, anchors, and trust scores

## Official References

- SHAP: [docs](https://shap.readthedocs.io/),
  [GitHub](https://github.com/shap/shap),
  [paper](https://arxiv.org/abs/1705.07874)
- LIME: [GitHub](https://github.com/marcotcr/lime),
  [paper](https://arxiv.org/abs/1602.04938)
- pyGAM: [docs](https://pygam.readthedocs.io/)
- scikit-learn inspection:
  [permutation importance](https://scikit-learn.org/stable/modules/permutation_importance.html)
- DiCE: [docs](https://interpret.ml/DiCE/),
  [GitHub](https://github.com/interpretml/DiCE)

## Prerequisites

- Comfort with Python and `numpy` / `pandas`
- Basic familiarity with training a model in `scikit-learn`
- No prior knowledge of explainability methods is assumed

## Installation

- Inside the tutorial container everything is preinstalled. To run the examples
  outside Docker:
  ```bash
  > pip install scikit-learn pygam shap lime dice-ml matplotlib pandas
  ```

- Verify the install:
  ```bash
  > python -c "import shap, lime, pygam, dice_ml; print('ok')"
  ```
  ```text
  ok
  ```

## Core Concepts

- Two axes organize every method in this tutorial:
  - Global vs local:
    - Global: explains the model's overall behavior across all data
    - Local: explains one specific prediction
  - Model-specific vs model-agnostic:
    - Model-specific: exploits model internals (e.g., linear coefficients, tree
      structure)
    - Model-agnostic: treats the model as a black box, probing it with perturbed
      inputs

- A third idea, feature attribution, runs through SHAP and LIME: split a
  prediction into per-feature contributions that sum to the output. SHAP grounds
  this split in game theory (Shapley values), giving it consistency guarantees
  that ad-hoc methods lack.

## Interpretable Models: Linear and GAM

- The cheapest explanation is a model that needs none. Linear models expose a
  coefficient per feature; the sign and magnitude are the explanation.

- Fit a linear model and read the coefficients:
  ```python
  from sklearn.datasets import load_diabetes
  from sklearn.linear_model import LinearRegression
  import pandas as pd

  data = load_diabetes(as_frame=True)
  X, y = data.data, data.target
  model = LinearRegression().fit(X, y)
  coefs = pd.Series(model.coef_, index=X.columns).sort_values()
  print(coefs)
  ```
  ```text
  s1   -792.18
  age    -0.48
  sex  -239.81
  ...
  bmi   519.84
  s5    751.27
  bp    324.39
  ```

- A positive coefficient means the target rises with the feature; `bmi` and `s5`
  drive disease progression up, `sex` and `s1` pull it down.

- Linear models miss nonlinear effects. A Generalized Additive Model (GAM) keeps
  interpretability while fitting a smooth, nonlinear shape per feature:
  ```python
  from pygam import LinearGAM, s
  import numpy as np

  X_np = X.to_numpy()
  gam = LinearGAM(s(0) + s(1) + s(2) + s(3)).fit(X_np, y)
  # Inspect the partial-dependence shape of feature 2 (bmi).
  XX = gam.generate_X_grid(term=2)
  print(gam.partial_dependence(term=2, X=XX)[:3])
  ```
  ```text
  [-43.21 -42.88 -42.55]
  ```

- Each GAM term is a function you can plot, so you see _how_ a feature acts (e.g.,
  flat then sharply rising), not just a single slope.

- Use these when accuracy allows: a model that is interpretable by construction
  beats a black box plus a post-hoc explainer.

## Permutation Importance

- Permutation importance is the fastest global, model-agnostic check. It shuffles
  one feature, measures how much the score drops, and repeats. A big drop means
  the model leaned on that feature.

- It works on any fitted estimator:
  ```python
  from sklearn.ensemble import RandomForestRegressor
  from sklearn.inspection import permutation_importance
  from sklearn.model_selection import train_test_split

  X_tr, X_te, y_tr, y_te = train_test_split(X, y, random_state=0)
  rf = RandomForestRegressor(random_state=0).fit(X_tr, y_tr)
  result = permutation_importance(rf, X_te, y_te, n_repeats=10, random_state=0)
  imp = pd.Series(result.importances_mean, index=X.columns).sort_values()
  print(imp.tail(3))
  ```
  ```text
  bp     0.07
  bmi    0.18
  s5     0.21
  ```

- Prefer permutation importance over a tree's built-in `feature_importances_`:
  the built-in version is biased toward high-cardinality features and is computed
  on training data, while permutation importance can be measured on held-out
  data.

- Caveat: correlated features split their importance, so two redundant features
  can both look unimportant.

## SHAP

- SHAP assigns each feature a contribution to a single prediction, with the
  contributions summing to the prediction minus a baseline. It unifies several
  earlier methods and comes with optimized explainers per model type
  (`TreeExplainer` for trees, `DeepExplainer` for nets, `KernelExplainer` as the
  agnostic fallback).

- Explain a tree model:
  ```python
  import shap

  explainer = shap.TreeExplainer(rf)
  shap_values = explainer.shap_values(X_te)
  # Global importance: mean absolute SHAP value per feature.
  shap.summary_plot(shap_values, X_te, plot_type="bar", show=False)
  # Local explanation for the first test row.
  print(dict(zip(X.columns, shap_values[0].round(1))))
  ```
  ```text
  {'age': -2.1, 'sex': -8.4, 'bmi': 41.7, 'bp': 12.3, 's5': 33.9, ...}
  ```

- The same `shap_values` array powers both views:
  - Global: `summary_plot` ranks features by mean absolute contribution
  - Local: a single row shows which features pushed _this_ prediction up or down

- SHAP is the default when you need trustworthy local explanations and can afford
  the compute. `TreeExplainer` is fast; `KernelExplainer` is general but slow, so
  pass it a small background sample.

## LIME

- LIME explains one prediction by fitting a simple linear model in the
  neighborhood of that point. It perturbs the input, sees how predictions change,
  and reports the local linear weights. It is fully model-agnostic and works on
  tabular, text, and image data.

- Tabular example:
  ```python
  from lime.lime_tabular import LimeTabularExplainer

  explainer = LimeTabularExplainer(
      X_tr.to_numpy(),
      feature_names=list(X.columns),
      mode="regression",
  )
  exp = explainer.explain_instance(X_te.to_numpy()[0], rf.predict, num_features=5)
  print(exp.as_list())
  ```
  ```text
  [('bmi > 0.01', 38.2), ('s5 > 0.02', 27.5), ('bp <= -0.01', -14.1), ...]
  ```

- Text example, explaining a sentiment classifier:
  ```python
  from sklearn.pipeline import make_pipeline
  from sklearn.feature_extraction.text import TfidfVectorizer
  from sklearn.linear_model import LogisticRegression
  from lime.lime_text import LimeTextExplainer

  docs = ["great film, loved it", "boring and far too long", "a brilliant story"]
  labels = [1, 0, 1]
  clf = make_pipeline(TfidfVectorizer(), LogisticRegression()).fit(docs, labels)
  explainer = LimeTextExplainer(class_names=["neg", "pos"])
  exp = explainer.explain_instance("a brilliant boring story", clf.predict_proba)
  print(exp.as_list())
  ```
  ```text
  [('boring', -0.41), ('brilliant', 0.33), ('story', 0.05)]
  ```

- LIME is intuitive and cheap to run on one instance, but its explanations can be
  unstable: rerunning with different random perturbations may shift the weights.
  When stability matters, prefer SHAP.

## Counterfactual Explanations

- A counterfactual answers an actionable question: _what is the smallest change
  to the input that flips the prediction?_ Instead of attributing the current
  outcome, it tells the user what to do differently (e.g., "raise income by 8k to
  get approved").

- Generate counterfactuals with DiCE:
  ```python
  import dice_ml
  from sklearn.datasets import load_breast_cancer
  from sklearn.ensemble import RandomForestClassifier

  bc = load_breast_cancer(as_frame=True)
  df = bc.frame
  clf = RandomForestClassifier(random_state=0).fit(bc.data, bc.target)
  d = dice_ml.Data(
      dataframe=df,
      continuous_features=list(bc.data.columns),
      outcome_name="target",
  )
  m = dice_ml.Model(model=clf, backend="sklearn")
  exp = dice_ml.Dice(d, m, method="random")
  cf = exp.generate_counterfactuals(
      bc.data.iloc[0:1], total_CFs=2, desired_class="opposite"
  )
  cf.visualize_as_dataframe(show_only_changes=True)
  ```
  ```text
  Query instance (original outcome: 0)
  ...
  Counterfactual set (new outcome: 1)
  mean radius: 13.1, worst concave points: 0.09, ...
  ```

- `show_only_changes=True` highlights just the features DiCE altered, so the
  required change is easy to read.

- Use counterfactuals when the audience wants recourse, not just attribution.
  They pair well with constraints (mark some features immutable, e.g., age) so the
  suggested change is realistic.

## Choosing a Technique

| Technique | Scope | Model | Best for |
| :-------- | :---- | :---- | :------- |
| Linear / GAM | Global | Specific | Inherently interpretable models |
| Permutation importance | Global | Agnostic | Fast feature ranking |
| SHAP | Global and local | Agnostic (fast for trees) | Trustworthy attributions |
| LIME | Local | Agnostic | Quick single-instance, text and images |
| Counterfactuals | Local | Agnostic | Actionable recourse |

- A practical workflow:
  - Start with permutation importance to rank features globally
  - Use SHAP for reliable local and global attributions
  - Reach for LIME on text or images, or for a fast second opinion
  - Add counterfactuals when users need to know what to change

## Tutorial Content

- This tutorial includes all the code, notebooks, and Docker container in
  [tutorials/ml_explainability](https://github.com/gpsaggese/umd_classes/tree/master/tutorials/ml_explainability):
  - `explainability_shap_lime.API.ipynb`: core API of each explainability tool
  - `explainability_shap_lime.example.ipynb`: end-to-end explanation of a model
    on a real dataset
  - `explainability_shap_lime_utils.py`: shared helper functions
  - A Docker system to build and run the environment using the standardized
    approach

## Changelog

- 2026-06-29: Initial release
