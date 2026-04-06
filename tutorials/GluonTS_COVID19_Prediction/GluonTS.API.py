# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.19.0
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %% [markdown]
# # GluonTS API Tutorial: Probabilistic Time Series Forecasting
#
# **Welcome!** This hands-on tutorial teaches you how to build probabilistic time series forecasts with [GluonTS](https://ts.gluon.ai/), an open-source Python library from AWS. You'll go from raw data to evaluated predictions — learning the *why* alongside the *how* at every step.
#
# ## Prerequisites
#
# - Basic Python and pandas knowledge
# - Familiarity with machine learning concepts (training, testing, epochs)
# - No prior time series experience needed — we'll explain everything as we go
#
# ## What You'll Learn
#
# 1. How to prepare time series data for GluonTS (`ListDataset`)
# 2. How to configure, train, and evaluate three different forecasting models
# 3. When to pick each model for your problem
# 4. How to interpret **probabilistic** forecasts (confidence intervals, quantiles)
#
# ## The Three Models
#
# | Model | Summary | Best for |
# |-------|---------|----------|
# | **DeepAR** | RNN that "remembers" past patterns | Complex seasonality, long-term dependencies |
# | **SimpleFeedForward** | Direct mapping from recent history to future | Quick baselines, stable trends |
# | **DeepNPTS** | Learns the data distribution without assumptions | Regime shifts, unusual distributions |
#
# ## Why Synthetic Data?
#
# We start with synthetic time series instead of real-world data. This lets you focus on **how GluonTS works** without getting distracted by domain complexity (missing values, reporting artifacts, policy effects, etc.).
#
# We'll progress through three levels of difficulty:
#
# | Level | Pattern | What it tests |
# |-------|---------|---------------|
# | 1 | **Sinusoid** | Can the model learn a clean periodic signal? |
# | 2 | **Multi-frequency** | Can it handle trend + seasonality + weekly cycles + noise? |
# | 3 | **Regime change** | Can it adapt when the data's behavior changes midway? |
#
# Once you're comfortable with the mechanics here, move to `GluonTS.example.ipynb` to see these models applied to real COVID-19 data.

# %% [markdown]
# ---
#
# ## Setup

# %%
import warnings

warnings.filterwarnings("ignore")

# Core GluonTS components for the API tutorial
from gluonts.torch.model.deepar import DeepAREstimator
from gluonts.torch.model.simple_feedforward import SimpleFeedForwardEstimator
from gluonts.torch.model.deep_npts import DeepNPTSEstimator
from gluonts.evaluation import make_evaluation_predictions

# All our utilities are in one place - much cleaner!
import GluonTS_utils as gluonts

print("Setup complete. Ready to explore GluonTS.")

# %% [markdown]
# ## The GluonTS Workflow
#
# Every GluonTS model follows the same five steps. We'll walk through each one in detail as we go, but here's the big picture:
#
# ```
# Step 1  Prepare data      →  ListDataset({"start", "target"}, freq)
# Step 2  Configure model    →  SomeEstimator(prediction_length, context_length, ...)
# Step 3  Train              →  predictor = estimator.train(train_ds)
# Step 4  Generate forecasts →  make_evaluation_predictions(test_ds, predictor, num_samples)
# Step 5  Evaluate           →  forecast.mean, forecast.quantile(q), forecast.samples
# ```
#
# Let's see this in action, starting with the simplest possible time series.

# %% [markdown]
# ---
#
# # Level 1: Sinusoid — The Simplest Pattern
#
# We begin with a pure sine wave plus a small amount of Gaussian noise. This is the easiest pattern a model can encounter: perfectly periodic, no trend, no regime changes.
#
# **Why start here?** If a model can't forecast a sinusoid, something is fundamentally wrong. This gives us a clean baseline to verify our pipeline works before increasing complexity.

# %% [markdown]
# ## Generate and Visualize the Sinusoid

# %%
sin_df = gluonts.generate_sinusoid(
    n_points=365,
    period=30,
    amplitude=10.0,
    noise_std=1.0,
    seed=42,
)

gluonts.plot_synthetic_series(sin_df, title="Sinusoid: 30-day cycle, low noise")

# %% [markdown]
# ## Prepare for GluonTS — The `ListDataset`
#
# Before any model can train, your data must be in GluonTS's `ListDataset` format. Each entry is a dictionary with:
#
# - **`start`** — the first timestamp (string or `pd.Timestamp`)
# - **`target`** — a 1-D array of the values you want to forecast
# - **`freq`** — the time series frequency (`"D"` for daily, `"H"` for hourly, `"W"` for weekly)
#
# Under the hood, this is what GluonTS sees:
#
# ```python
# from gluonts.dataset.common import ListDataset
#
# train_ds = ListDataset([
#     {"start": "2020-01-01", "target": [50.1, 48.3, 52.7, ...]}
# ], freq="D")
# ```
#
# Our `prepare_synthetic_dataset` utility handles the train/test split and conversion for you. The last `prediction_length` days become the test set.
#
# > **Note:** Some models (like DeepAR) also support **external features** via `feat_dynamic_real` — we'll cover that in the example notebook with real COVID-19 covariates. For now, we're keeping it simple: just a target series.

# %%
PREDICTION_LENGTH = 30

sin_data = gluonts.prepare_synthetic_dataset(
    sin_df,
    prediction_length=PREDICTION_LENGTH,
)

gluonts.plot_train_test_split(sin_data, title="Sinusoid - Train / Test Split")

# %% [markdown]
# ## DeepAR on the Sinusoid
#
# **Analogy:** Think of DeepAR like reading a book — it processes the story *sequentially*, remembering earlier chapters so it can predict what comes next. Technically, it uses a **Recurrent Neural Network (RNN)** that keeps a hidden state as it moves through your time series.
#
# ### When to reach for DeepAR
#
# - Your data has **complex patterns** — seasonality, multiple waves, trends that shift
# - **Long-term memory** matters — what happened weeks ago still influences today
# - You want to include **external features** (e.g., mobility data alongside case counts)
#
# ### Key parameters
#
# | Parameter | What it controls | Our value |
# |-----------|-----------------|-----------|
# | `prediction_length` | How far ahead to forecast | 30 days |
# | `context_length` | How far back the model looks (rule of thumb: 2–4× prediction_length) | 60 days |
# | `freq` | Data frequency | `"D"` (daily) |
# | `num_layers` | RNN depth — more layers = more capacity | 2 |
# | `hidden_size` | Neurons per layer | 40 |
# | `trainer_kwargs` | Training config (epochs, learning rate, etc.) | `{"max_epochs": 5}` |
#
# ### Configure DeepAR

# %%
deepar_estimator = DeepAREstimator(
    prediction_length=PREDICTION_LENGTH,
    context_length=60,
    freq="D",
    num_layers=2,
    hidden_size=40,
    trainer_kwargs={"max_epochs": 5},
)

# %% [markdown]
# ### Train DeepAR
#
# Calling `.train()` runs the full training loop (powered by PyTorch Lightning).

# %%
deepar_predictor = deepar_estimator.train(sin_data["train_ds"])
print("DeepAR training complete")

# %% [markdown]
# ### Generate Forecasts
#
# Unlike traditional models that output a single number per time step, GluonTS models produce **probabilistic forecasts** — a *distribution* of possible futures. Here's what that means in practice:
#
# - `make_evaluation_predictions(...)` generates `num_samples` possible future trajectories (e.g., 100 different "what-if" scenarios).
# - From those samples you can extract:
#   - **`forecast.mean`** — the average prediction (point forecast)
#   - **`forecast.quantile(0.5)`** — the median prediction
#   - **`forecast.quantile(0.1)` / `forecast.quantile(0.9)`** — 80% confidence interval
#   - **`forecast.quantile(0.05)` / `forecast.quantile(0.95)`** — 90% confidence interval
#   - **`forecast.samples`** — all raw samples, shape `(num_samples, prediction_length)`
#
# This is powerful because it tells you not just *what* the model expects, but *how confident* it is. Wide intervals = high uncertainty; narrow intervals = the model is more sure.

# %%
forecast_it, ts_it = make_evaluation_predictions(
    dataset=sin_data["test_ds"],
    predictor=deepar_predictor,
    num_samples=100,
)

deepar_forecasts = list(forecast_it)
deepar_ts = list(ts_it)
deepar_forecast = deepar_forecasts[0]

print(f"Forecast shape: {deepar_forecast.samples.shape}")
print(
    f"  = {deepar_forecast.samples.shape[0]} sample paths, each {deepar_forecast.samples.shape[1]} steps"
)

# %% [markdown]
# ### Visualize DeepAR on Sinusoid
#
# The shaded region shows the 80% confidence interval — the model's estimate of where the true value is likely to fall.

# %%
gluonts.plot_forecast_result(sin_data, deepar_forecast, model_name="DeepAR")

# %% [markdown]
# ### Evaluate DeepAR
#
# We use three standard metrics to measure forecast quality:
#
# - **MAE** (Mean Absolute Error) — average absolute difference, in original units. Easy to interpret.
# - **RMSE** (Root Mean Square Error) — like MAE, but penalizes large errors more heavily.
# - **MAPE** (Mean Absolute Percentage Error) — percentage error, so you can compare across different scales.

# %%
sin_actuals = sin_data["test_df"]["value"].values
deepar_sin_metrics = gluonts.calculate_metrics(deepar_forecast.mean, sin_actuals)

gluonts.print_metrics(deepar_sin_metrics, model_name="DeepAR on Sinusoid")

# %% [markdown]
# > **Checkpoint:** You just completed the full GluonTS workflow — configure, train, forecast, visualize, evaluate. This is the same 5-step pattern for *every* GluonTS model. From here on we'll move faster since you know the drill. What changes is the **data** (increasing complexity) and the **model** (different architectures), not the workflow itself.
#
# ---
#
# # Level 2: Multi-Frequency — Adding Realism
#
# Real time series rarely consist of a single clean cycle. This synthetic series combines four components you'll encounter in real data:
#
# - **Linear trend** — a slow upward drift over time
# - **30-day seasonal cycle** — the dominant pattern (like monthly seasonality)
# - **7-day weekly cycle** — a secondary oscillation (like weekend effects)
# - **Gaussian noise** — random variation
#
# This is much closer to what you'd see in business metrics, health data, or economic indicators.

# %% [markdown]
# ## Generate and Visualize

# %%
multi_df = gluonts.generate_multi_frequency(
    n_points=365,
    noise_std=1.5,
    seed=42,
)

gluonts.plot_synthetic_series(
    multi_df, title="Multi-Frequency: trend + seasonal + weekly + noise"
)

# %%
multi_data = gluonts.prepare_synthetic_dataset(
    multi_df,
    prediction_length=PREDICTION_LENGTH,
)

gluonts.plot_train_test_split(
    multi_data, title="Multi-Frequency - Train / Test Split"
)

# %% [markdown]
# ## DeepAR on Multi-Frequency
#
# We use the same DeepAR configuration. The question is: can it decompose the overlapping cycles and extrapolate the trend?

# %%
deepar_multi_est = DeepAREstimator(
    prediction_length=PREDICTION_LENGTH,
    context_length=60,
    freq="D",
    num_layers=2,
    hidden_size=40,
    trainer_kwargs={"max_epochs": 5},
)

deepar_multi_pred = deepar_multi_est.train(multi_data["train_ds"])
print("DeepAR training complete")

# %%
forecast_it, ts_it = make_evaluation_predictions(
    dataset=multi_data["test_ds"],
    predictor=deepar_multi_pred,
    num_samples=100,
)
deepar_multi_fc = list(forecast_it)[0]

gluonts.plot_forecast_result(multi_data, deepar_multi_fc, model_name="DeepAR")

# %%
multi_actuals = multi_data["test_df"]["value"].values
deepar_multi_metrics = gluonts.calculate_metrics(
    deepar_multi_fc.mean, multi_actuals
)

gluonts.print_metrics(
    deepar_multi_metrics, model_name="DeepAR on Multi-Frequency"
)

# %% [markdown]
# ## SimpleFeedForward on Multi-Frequency
#
# Now let's try a different model on the same data. **SimpleFeedForward** takes a fixed window of recent history and maps it directly to the future through a basic neural network. No memory of what came before that window — think of it as glancing at the last few pages of a book instead of reading the whole thing.
#
# ### When to reach for SimpleFeedForward
#
# - You need **fast training** — results in seconds, not minutes
# - Your data has **stable, smooth trends** without complex seasonality
# - You want a **quick baseline** to compare fancier models against
#
# ### How it differs from DeepAR
#
# | | DeepAR | SimpleFeedForward |
# |---|---|---|
# | Architecture | RNN (sequential memory) | Feedforward (snapshot) |
# | Hidden layers | `hidden_size` (single int) | `hidden_dimensions` (list of ints) |
# | External features | Supported | **Not supported** |
# | `freq` parameter | Required | **Not accepted** |
# | Training speed | Minutes | Seconds |

# %%
ff_estimator = SimpleFeedForwardEstimator(
    prediction_length=PREDICTION_LENGTH,
    context_length=60,
    hidden_dimensions=[40, 40],
    trainer_kwargs={"max_epochs": 5},
)

ff_predictor = ff_estimator.train(multi_data["train_ds"])
print("SimpleFeedForward training complete")

# %%
forecast_it, ts_it = make_evaluation_predictions(
    dataset=multi_data["test_ds"],
    predictor=ff_predictor,
    num_samples=100,
)
ff_multi_fc = list(forecast_it)[0]

gluonts.plot_forecast_result(
    multi_data, ff_multi_fc, model_name="SimpleFeedForward"
)

# %%
ff_multi_metrics = gluonts.calculate_metrics(ff_multi_fc.mean, multi_actuals)

gluonts.print_metrics(
    ff_multi_metrics, model_name="SimpleFeedForward on Multi-Frequency"
)

# %% [markdown]
# ---
#
# # Level 3: Regime Change — The Hard Problem
#
# This is where things get interesting. The series behaves one way for the first half, then **abruptly shifts** to a different baseline, amplitude, and frequency.
#
# Think of real-world analogs:
# - A new COVID variant causing a sudden surge
# - A product going viral and changing demand patterns
# - A policy change shifting economic indicators
#
# Most models struggle here because their training data comes from the old regime, but they need to forecast in the new one.

# %% [markdown]
# ## Generate and Visualize

# %%
regime_df = gluonts.generate_regime_change(
    n_points=365,
    changepoint_frac=0.6,
    noise_std=1.5,
    seed=42,
)

gluonts.plot_synthetic_series(
    regime_df, title="Regime Change: behavior shifts at day ~219"
)

# %%
regime_data = gluonts.prepare_synthetic_dataset(
    regime_df,
    prediction_length=PREDICTION_LENGTH,
)

gluonts.plot_train_test_split(
    regime_data, title="Regime Change - Train / Test Split"
)

# %% [markdown]
# ## DeepNPTS on Regime Change
#
# DeepAR and SimpleFeedForward assume the future follows a *known* shape (like a bell curve). **DeepNPTS** says "I'll figure out the shape from the data itself." It's **non-parametric** — it learns the distribution directly without assuming normal, Poisson, or any other family.
#
# This makes it especially powerful when your data doesn't behave "normally" — sudden regime shifts, heavy tails, or distributions that change over time.
#
# ### When to reach for DeepNPTS
#
# - The **distribution changes** over time (e.g., calm periods vs. surges)
# - You expect **regime shifts** — the data behaves differently before and after some event
# - Your data has **unusual shapes** — heavy tails, multi-modal, skewed
#
# ### How it differs from DeepAR
#
# | | DeepAR | DeepNPTS |
# |---|---|---|
# | Distribution | Parametric (assumes Gaussian) | Non-parametric (learned from data) |
# | Epochs config | `trainer_kwargs={"max_epochs": N}` | `epochs=N` (direct parameter) |
# | Hidden layers | `hidden_size` (single int) | `num_hidden_nodes` (list of ints) |
# | Regime shifts | Can struggle | Designed for this |
#
# > **Watch the code below** — notice the two API quirks: `epochs` is a direct parameter (not inside `trainer_kwargs`), and the hidden layer parameter is called `num_hidden_nodes` instead of `hidden_size`.

# %%
npts_estimator = DeepNPTSEstimator(
    prediction_length=PREDICTION_LENGTH,
    context_length=60,
    freq="D",
    num_hidden_nodes=[40, 40],
    epochs=5,
)

npts_predictor = npts_estimator.train(regime_data["train_ds"])
print("DeepNPTS training complete")

# %%
forecast_it, ts_it = make_evaluation_predictions(
    dataset=regime_data["test_ds"],
    predictor=npts_predictor,
    num_samples=100,
)
npts_regime_fc = list(forecast_it)[0]

gluonts.plot_forecast_result(regime_data, npts_regime_fc, model_name="DeepNPTS")

# %%
regime_actuals = regime_data["test_df"]["value"].values
npts_regime_metrics = gluonts.calculate_metrics(
    npts_regime_fc.mean, regime_actuals
)

print("DeepNPTS on Regime Change")
print("=" * 40)
print(f"  MAE:  {npts_regime_metrics['mae']:.2f}")
print(f"  RMSE: {npts_regime_metrics['rmse']:.2f}")
print(f"  MAPE: {npts_regime_metrics['mape']:.2f}%")

# %% [markdown]
# ## DeepAR on Regime Change (Contrast)
#
# Let's run DeepAR on the same regime-change data to see how it compares. Because DeepAR assumes a parametric distribution learned from the full training set, it may struggle with the post-shift behavior.

# %%
deepar_regime_est = DeepAREstimator(
    prediction_length=PREDICTION_LENGTH,
    context_length=60,
    freq="D",
    num_layers=2,
    hidden_size=40,
    trainer_kwargs={"max_epochs": 5},
)

deepar_regime_pred = deepar_regime_est.train(regime_data["train_ds"])

forecast_it, ts_it = make_evaluation_predictions(
    dataset=regime_data["test_ds"],
    predictor=deepar_regime_pred,
    num_samples=100,
)
deepar_regime_fc = list(forecast_it)[0]

gluonts.plot_forecast_result(regime_data, deepar_regime_fc, model_name="DeepAR")

# %%
deepar_regime_metrics = gluonts.calculate_metrics(
    deepar_regime_fc.mean, regime_actuals
)

print("DeepAR on Regime Change")
print("=" * 40)
print(f"  MAE:  {deepar_regime_metrics['mae']:.2f}")
print(f"  RMSE: {deepar_regime_metrics['rmse']:.2f}")
print(f"  MAPE: {deepar_regime_metrics['mape']:.2f}%")

# %% [markdown]
# ---
#
# # Model Comparison
#
# Let's bring all results together. Each model was tested on the data type that best highlights its strengths and weaknesses.

# %%
import pandas as pd

comparison = pd.DataFrame(
    {
        "Model": [
            "DeepAR (sinusoid)",
            "DeepAR (multi-freq)",
            "SimpleFeedForward (multi-freq)",
            "DeepNPTS (regime change)",
            "DeepAR (regime change)",
        ],
        "MAE": [
            deepar_sin_metrics["mae"],
            deepar_multi_metrics["mae"],
            ff_multi_metrics["mae"],
            npts_regime_metrics["mae"],
            deepar_regime_metrics["mae"],
        ],
        "RMSE": [
            deepar_sin_metrics["rmse"],
            deepar_multi_metrics["rmse"],
            ff_multi_metrics["rmse"],
            npts_regime_metrics["rmse"],
            deepar_regime_metrics["rmse"],
        ],
        "MAPE (%)": [
            deepar_sin_metrics["mape"],
            deepar_multi_metrics["mape"],
            ff_multi_metrics["mape"],
            npts_regime_metrics["mape"],
            deepar_regime_metrics["mape"],
        ],
    }
)

print(comparison.to_string(index=False, float_format="%.2f"))

# %% [markdown]
# ---
#
# # Summary
#
# ## What You Learned
#
# 1. **Data preparation** — GluonTS uses `ListDataset` with `start`, `target`, and optional `feat_dynamic_real`
# 2. **Three models** — DeepAR (RNN, complex patterns), SimpleFeedForward (fast baseline), DeepNPTS (flexible, non-parametric)
# 3. **One workflow** — `estimator.train()` then `make_evaluation_predictions()` — same pattern for every model
# 4. **Probabilistic output** — every forecast gives you means, medians, quantiles, and raw samples
# 5. **Model choice matters** — the right model depends on your data's characteristics
#
# ---
#
# ## Which Model Should You Choose?
#
# | If your data has... | Try this model | Why |
# |---------------------|---------------|-----|
# | Complex seasonality, multiple waves | **DeepAR** | RNN captures long-range dependencies |
# | Stable trends, need fast results | **SimpleFeedForward** | Trains in seconds, good baseline |
# | Regime shifts, unusual distributions | **DeepNPTS** | Non-parametric — adapts to changing behavior |
# | No idea yet | **Start with SimpleFeedForward** | Fast to test, then try DeepAR for more accuracy |
#
# ---
#
# ## Quick Reference
#
# | Task | Code |
# |------|------|
# | Point forecast (mean) | `forecast.mean` |
# | Median forecast | `forecast.quantile(0.5)` |
# | 80% confidence interval | `forecast.quantile(0.1)` to `forecast.quantile(0.9)` |
# | Raw sample paths | `forecast.samples` (shape: `num_samples × prediction_length`) |
#
# ---
#
# ## Tips for Better Results
#
# | Area | Tip |
# |------|-----|
# | **Context length** | Start at 2× your `prediction_length`, try 3× and 4× |
# | **Epochs** | 5–10 for experiments, 20–30 for final models |
# | **Features** | More isn't always better — test with and without |
# | **Data quality** | Handle missing values and normalize if needed |
#
# ---
#
# ## Troubleshooting
#
# | Problem | Fix |
# |---------|-----|
# | *"Wrong number of features"* | `num_feat_dynamic_real` must match the rows in your `feat_dynamic_real` array |
# | *Training too slow* | Reduce epochs, shrink `context_length`, or use SimpleFeedForward |
# | *Poor forecast quality* | Increase `context_length`, train longer, or try DeepNPTS for regime changes |
# | *"Unexpected keyword argument"* | DeepAR: `trainer_kwargs={"max_epochs": N}`. DeepNPTS: `epochs=N`. SimpleFeedForward: no `freq` parameter |
#
# ---
#
# ## Resources
#
# - [GluonTS Documentation](https://ts.gluon.ai/) · [GitHub](https://github.com/awslabs/gluonts) · [PyTorch Lightning](https://lightning.ai/docs/pytorch/stable/)
#
# ---
#
# ## What's Next?
#
# Now that you understand how GluonTS works on clean synthetic data, move to **`GluonTS.example.ipynb`** to see these same models applied to real **COVID-19 case prediction** — with feature engineering, multiple covariates, scenario analysis, and all the messiness of real-world data.

# %%
