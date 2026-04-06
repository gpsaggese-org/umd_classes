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
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %% [markdown]
# # COVID-19 Forecasting with GluonTS
#
# Complete example showcasing GluonTS for real-world pandemic forecasting.
#
# **What we'll do:** Build an end-to-end forecasting application that predicts U.S. daily COVID-19 cases 14 days ahead, with uncertainty quantification. Public health officials use such systems for resource planning and intervention strategies.
#
# **Data sources:** JHU cases and deaths (aggregated nationally), Google Mobility (6 metrics). Our features—deaths, CFR, mobility—are chosen because they lag or lead case trends and capture behavioral response.
#
# **Models:** We compare DeepAR (complex patterns), SimpleFeedForward (fast baseline), and DeepNPTS (regime changes).

# %% [markdown]
# ---
#
# ## 1. Setup and Imports
#
# Let's get everything set up for our COVID-19 forecasting analysis.

# %%
import warnings

warnings.filterwarnings("ignore")

# All our utilities in one place - much cleaner!
import GluonTS_utils as gluonts

# Explicit imports for functions called without gluonts. prefix
from GluonTS_utils import (
    train_deepar_covid,
    train_feedforward_covid,
    train_deepnpts_covid,
    compare_models,
    print_model_comparison,
    run_all_scenarios,
    print_scenario_summary,
    print_policy_insights,
)

print("Setup complete. Ready to forecast COVID-19 cases.")

# %% [markdown]
# ---
#
# ## 2. Load and Explore COVID-19 Data
#
# Let's load our real COVID-19 data and take a look at what we're working with.
#
# Our data pipeline loads and merges:
# - **Cases**: Daily confirmed COVID-19 cases
# - **Deaths**: Daily COVID-19 deaths
# - **Mobility**: Google mobility data (6 metrics showing how people moved during the pandemic)
#
# All data is aggregated to the **national (US) level** for this example.

# %%
print("Loading COVID-19 data...")
print("=" * 70)

data = gluonts.load_covid_data_for_gluonts(
    data_dir="data",
    prediction_length=14,
)

print("\nData loaded successfully!")
print("\nDataset summary:")
print(f"  Total observations: {len(data['merged_df'])}")
print(
    f"  Date range: {data['merged_df']['Date'].min()} to {data['merged_df']['Date'].max()}"
)
print(f"  Number of features: {len(data['features'])}")
print(f"  Feature names: {', '.join(data['features'])}")

# %% [markdown]
# ### Data Exploration
#
# Let's visualize our data to understand the patterns we're trying to forecast.

# %%
display_cols = [
    "Date",
    "Daily_Cases_MA7",
    "Daily_Deaths_MA7",
    "CFR",
    "retail and recreation",
    "workplaces",
]

print("First few rows of our dataset:")
print("=" * 70)
print(data["merged_df"][display_cols].head(10))

print("\nStatistical summary:")
print(
    data["merged_df"][["Daily_Cases_MA7", "Daily_Deaths_MA7", "CFR"]].describe()
)

# %%
gluonts.plot_data_exploration(data["merged_df"])

# %% [markdown]
# **Why these features?** Target (7-day MA) smooths reporting; deaths lag cases and correlate with outcomes; CFR indicates strain; mobility captures lockdown effects.

# %% [markdown]
# ---
#
# ## 3. Feature Engineering
#
# Our data pipeline has already engineered several features to improve model performance:
#
# ### Features Created:
#
# 1. **Daily_Cases_MA7**: 7-day moving average of cases (smooths noisy daily data)
# 2. **Daily_Deaths**: Raw daily death counts
# 3. **Daily_Deaths_MA7**: 7-day moving average of deaths
# 4. **Cumulative_Deaths**: Total deaths up to each date
# 5. **CFR (Case Fatality Ratio)**: Deaths / Cases ratio (severity indicator)
# 6. **Mobility Metrics**: 6 Google mobility indicators
#
# ### Why These Features Matter:
#
# - **Deaths data**: Strong leading indicator of case severity
# - **CFR**: Captures how deadly the virus is at different times
# - **Mobility**: Shows behavioral changes (lockdowns, reopenings)
# - **Moving averages**: Remove weekly reporting artifacts
#
# Let's look at feature correlations to understand relationships:

# %%
correlations = gluonts.analyze_feature_correlation(
    data["merged_df"],
    target_col=data["target"],
    features=data["features"],
)

# %% [markdown]
# ---
#
# ## 4. Train All Three Models
#
# **Model choice:** DeepAR for complex wave patterns; SimpleFeedForward for a fast baseline; DeepNPTS for regime shifts across COVID variants.
#
# We'll train:
# 1. **DeepAR**: Our most sophisticated model (uses all features)
# 2. **SimpleFeedForward**: Fast baseline (no external features)
# 3. **DeepNPTS**: Non-parametric approach (uses all features)
#
# Each model will:
# - Train on historical data (up to the test period)
# - Generate 14-day probabilistic forecasts
# - Provide uncertainty estimates (confidence intervals)

# %% [markdown]
# ### 4.1 Training DeepAR
#
# DeepAR is our most advanced model - an autoregressive RNN that:
# - Learns temporal patterns in the data
# - Uses external features (deaths, mobility)
# - Generates probabilistic forecasts (with uncertainty)

# %%
deepar_results = train_deepar_covid(
    train_ds=data["train_ds"],
    test_ds=data["test_ds"],
    prediction_length=14,
    num_feat_dynamic_real=len(data["features"]),
    epochs=10,
    learning_rate=0.001,
    context_length=60,
    num_layers=2,
    hidden_size=40,
    dropout_rate=0.1,
    verbose=True,
)

# %% [markdown]
# ### 4.2 Training SimpleFeedForward
#
# SimpleFeedForward is our baseline model - a simple neural network that:
# - Only uses historical case values (no external features)
# - Trains very quickly
# - Good for comparison and quick experiments

# %%
feedforward_results = train_feedforward_covid(
    train_ds=data["train_ds"],
    test_ds=data["test_ds"],
    prediction_length=14,
    epochs=20,
    learning_rate=0.001,
    context_length=60,
    hidden_dimensions=[40, 40],
    verbose=True,
)

# %% [markdown]
# ### 4.3 Training DeepNPTS
#
# DeepNPTS is our non-parametric model - it doesn't assume any specific distribution:
# - Great for data with shifting patterns (COVID waves!)
# - Uses external features
# - Flexible approach to uncertainty

# %%
deepnpts_results = train_deepnpts_covid(
    train_ds=data["train_ds"],
    test_ds=data["test_ds"],
    prediction_length=14,
    num_feat_dynamic_real=len(data["features"]),
    epochs=15,
    learning_rate=0.001,
    context_length=60,
    num_hidden_nodes=[40],
    dropout_rate=0.1,
    verbose=True,
)

# %% [markdown]
# ---
#
# ## 5. Compare Models
#
# Now that we've trained all three models, let's compare their performance!
#
# We'll look at:
# - **MAE (Mean Absolute Error)**: Average prediction error (lower is better)
# - **RMSE (Root Mean Squared Error)**: Penalizes large errors more (lower is better)
# - **MAPE (Mean Absolute Percentage Error)**: Error as a percentage (lower is better)
# - **Training time**: How long each model took to train

# %%
comparison = compare_models(
    [deepar_results, feedforward_results, deepnpts_results]
)
print_model_comparison(comparison)

print("\nBest Model by Metric:")
print("=" * 70)
for metric in ["MAE", "RMSE", "MAPE (%)"]:
    best_idx = comparison[metric].argmin()
    best_model = comparison["Model"].iloc[best_idx]
    best_value = comparison[metric].iloc[best_idx]
    print(f"  {metric:12s}: {best_model:20s} ({best_value:.2f})")

# %% [markdown]
#
# ### Interpreting the Metrics
#
# When comparing models we use three common error statistics:
#
# - **MAPE (Mean Absolute Percentage Error)** – expresses error as a percentage of the
#   actual value.  Lower is better.  As a rough guide:
#   - <10 % is highly accurate
#   - 10–20 % is good
#   - 21–50 % is reasonable/fair
#   - >50 % is considered inaccurate
#
# - **RMSE (Root Mean Square Error)** – gives more weight to large errors.  There is
#   no universal cutoff; the number should be small relative to the range or standard
#   deviation of your target variable.  A model with RMSE lower than a naive baseline
#   or the data’s volatility is usually acceptable.
#
# - **MAE (Mean Absolute Error)** – the average magnitude of errors in the same units
#   as the target.  It is easier to interpret than RMSE since it doesn’t square errors.
#   Again, smaller is better; compare it to the scale of your series.
#
# These guidelines are context–dependent – high‑volatility series tolerate higher
# errors, and some applications (e.g. finance) demand very low MAPE (<10 %) while
# others may accept 30 % or more.

# %% [markdown]
# ### 5.1 Visual Comparison
#
# Let's visualize the forecasts from all three models side by side.

# %%
gluonts.plot_model_comparison_3panel(
    deepar_results, feedforward_results, deepnpts_results
)

# %% [markdown]
# ---
#
# ## 6. Scenario Analysis: Simulating Interventions
#
# One of the most powerful applications of forecasting is **scenario analysis** -
# answering "what if?" questions about public health interventions.
#
# ### Why Scenario Analysis Matters
#
# During the pandemic, policymakers faced difficult decisions:
# - "If we implement a lockdown, how many cases will we prevent?"
# - "What happens if we reopen schools and businesses?"
# - "How does hospital capacity affect outcomes?"
#
# Our models can help answer these questions by **modifying the input features**
# (mobility, CFR) and re-running forecasts under different assumptions.
#
# ### The Five Scenarios
#
# We'll test five scenarios using DeepAR (which uses external features):
#
# | Scenario | Description | Mobility Change | CFR Change |
# |----------|-------------|-----------------|------------|
# | **1. Baseline** | No intervention, current trends | 0% | 0% |
# | **2. Moderate Intervention** | Masks, capacity limits | -15% | 0% |
# | **3. Strong Intervention** | Lockdowns, closures | -30% | 0% |
# | **4. Relaxation** | Reopening, holidays | +20% | 0% |
# | **5. Healthcare Strain** | Hospital capacity stressed | 0% | +15% |
#
# ### How It Works
#
# ```
# Original Data ──► Trained Model ──► Baseline Forecast
#                        │
# Modified Data          │
# (adjust features) ─────┴─────────► Scenario Forecast
#                                          │
#                                          ▼
#                               Compare: Cases prevented?
#                               Additional risk from relaxation?
# ```
#
# Let's run all five scenarios and compare the results!

# %%
scenario_results = run_all_scenarios(
    predictor=deepar_results.predictor,
    merged_df=data["merged_df"],
    feature_columns=data["features"],
    target_column=data["target"],
    prediction_length=14,
    verbose=True,
)

# %% [markdown]
# ### 6.1 Scenario Summary
#
# Let's look at a summary table comparing all scenarios and their projected case counts.

# %%
scenario_summary_df = print_scenario_summary(scenario_results)

# %% [markdown]
# ### 6.2 Scenario Visualization
#
# Now let's visualize the forecast trajectories for all scenarios side-by-side.

# %%
gluonts.plot_scenario_comparison(scenario_results, prediction_length=14)

# %% [markdown]
# ### 6.3 Policy Insights
#
# Based on our scenario analysis, here are key takeaways for decision-makers:

# %%
print_policy_insights(scenario_results)

# %% [markdown]
# ---
#
# ## 7. Conclusions and Recommendations
#
# ### Key Takeaways
#
# - **Feature engineering matters:** Deaths and mobility significantly improve forecasts
# - **Model choice depends on context:** Stable periods → SimpleFeedForward; complex patterns → DeepAR; regime changes → DeepNPTS
# - **Uncertainty is critical:** Point forecasts alone are insufficient for planning
# - **14-day horizon** matches public health planning; scenario analysis quantifies intervention impact
#
# ### Key Findings
#
# From our complete COVID-19 forecasting application, we learned:
#
# 1. **Model Performance**
#  - All three models successfully forecast COVID-19 cases
#  - DeepAR and DeepNPTS leverage external features (deaths, mobility)
#  - SimpleFeedForward provides a fast baseline
#
# 2. **Feature Importance**
#  - Deaths data is a strong predictor of case trends
#  - Mobility patterns correlate with transmission
#  - CFR (Case Fatality Ratio) captures disease severity changes
#
# 3. **Uncertainty Quantification**
#  - Probabilistic forecasts provide confidence intervals
#  - Wider intervals during high volatility (new variants, waves)
#  - Critical for risk assessment and resource planning
#
# 4. **Scenario Analysis**
#  - Models can simulate intervention impacts
#  - Helps quantify tradeoffs between policies
#  - Provides data-driven evidence for decision-making
#
# ### Recommendations for Public Health Officials
#
# 1. **Use Multiple Models**: Different models capture different patterns
# 2. **Monitor Uncertainty**: Wide confidence intervals = higher risk
# 3. **Update Frequently**: Retrain models as new data arrives
# 4. **Combine with Domain Expertise**: Models inform but don't replace human judgment
# 5. **Scenario Planning**: Use forecasts to evaluate intervention strategies
#
# ### Next Steps
#
# **Immediate improvements:**
# - Incorporate more granular data (state-level, county-level)
# - Add vaccination data for post-2021 forecasting
# - Experiment with longer forecast horizons (28 days)
# - Include additional features (testing rates, hospitalizations)
#
# **Advanced techniques:**
# - Ensemble multiple models for better accuracy
# - Hierarchical forecasting (national → state → county)
# - Real-time model updates (online learning)
# - Anomaly detection for new variants
#
# ### Production Deployment Considerations
#
# For real-world deployment:
# 1. **Automation**: Schedule daily model retraining
# 2. **Monitoring**: Track forecast accuracy over time
# 3. **Alerting**: Flag significant deviations from forecasts
# 4. **Scalability**: Use GPU acceleration for faster training
# 5. **Interpretability**: Provide explanations alongside forecasts
#
# ---
#
# ## Congratulations!
#
# You've completed a full end-to-end COVID-19 forecasting application!
#
# You now know how to:
# - Build complete data pipelines for time series forecasting
# - Engineer features to improve model performance
# - Train and compare multiple GluonTS models
# - Evaluate models comprehensively
# - Perform scenario analysis for decision support
# - Generate actionable insights from forecasts
#
# **Ready to apply these skills to your own forecasting problems?**

# %% [markdown]
# ---
#
# ## Additional Resources
#
# **GluonTS Documentation**
# - Official Docs: https://ts.gluon.ai/
# - Tutorials: https://ts.gluon.ai/stable/tutorials/index.html
# - API Reference: https://ts.gluon.ai/stable/api/index.html
#
# **COVID-19 Data Sources**
# - Johns Hopkins: https://github.com/CSSEGISandData/COVID-19
# - Google Mobility: https://www.google.com/covid19/mobility/
# - CDC Data: https://covid.cdc.gov/covid-data-tracker/
#
# **Time Series Forecasting**
# - "Forecasting: Principles and Practice" (Hyndman & Athanasopoulos)
# - GluonTS Paper: https://arxiv.org/abs/1906.05264
# - DeepAR Paper: https://arxiv.org/abs/1704.04110
#
# **Questions or Issues?**
# - Check the README.md for setup instructions
# - Review the API documentation in GluonTS.API.ipynb
# - Consult the utility function documentation in the code

# %%
