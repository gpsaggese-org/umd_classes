# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.19.3
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %% [markdown]
# # Performing Causal Tasks with DoWhy
#
# - This notebook teaches how to use causal inference to answer real-world questions
#   - Estimating causal effects using multiple identification strategies
#   - Quantifying the strength of causal relationships
#   - Explaining system behavior through causal mechanisms
#   - Answering counterfactual and policy questions
#   - Making robust predictions under distribution shift

# %% [markdown]
# ## Imports

# %%
# %load_ext autoreload
# %autoreload 2

# System libraries.
import logging

# Third-party libraries.
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# %%
# Helpers imports.
import helpers.hdbg as hdbg
import helpers.hnotebook as hnotebook
import helpers.hgraphviz as hgraphviz

# Notebook-specific utilities.
import dowhy_03_causal_tasks_utils as utils

try:
    from IPython.display import display
except ImportError:
    def display(obj):
        print(obj)

_LOG = logging.getLogger(__name__)

# Initialize notebook configuration and logging.
hnotebook.config_notebook()
hdbg.init_logger(verbosity=logging.INFO, use_exec_path=False)

_LOG.info("Notebook initialized")

# %% [markdown]
# # Part 1: Estimating Causal Effects
#
# - The **fundamental problem of causal inference**: we can't observe all potential outcomes
# - Learn strategies to estimate causal effects from observational data
#   - Backdoor adjustment: condition on confounders
#   - Instrumental variables: use exogenous variation
#   - Natural experiments: exploit as-if-random assignment
#   - Graphical causal models: use fitted mechanisms

# %% [markdown]
# # Cell 1: The Fundamental Problem of Causal Inference
#
# - Visual explanation: potential outcomes framework
#   - Define treatment, outcome, and counterfactual scenarios
#   - Show why we can't observe both Y(T=1) and Y(T=0) for the same unit
# - Illustrate the difference between naive comparison and causal inference
#   - Naive: correlation due to confounding is biased
#   - Adjusted: conditioning on confounder removes bias
# - **Key insight**:
#   - assumptions + data + adjustment strategy = identifiability

# %%
# #utils.cell1_plot_potential_outcomes??

# %%
utils.cell1_plot_potential_outcomes()

# %% [markdown]
# Visualize the fundamental problem of causal inference using confounded healthcare data.
# - Left panel: naive comparison showing biased ATE due to disease severity confounding.
# - Right panel: adjusted comparison using stratification to remove bias and recover true effect.

# %% [markdown]
# # Cell 2: Backdoor Criterion and Confounding
#
# - Scenario: healthcare treatment with confounding by disease severity
# - Learn when and how to use backdoor adjustment
#   - Identify confounder paths in the causal graph
#   - Block backdoor paths by conditioning on confounders
# - Compare adjustment methods (regression, stratification, IPW)
#   - Interactive widget to explore method sensitivity
# - Discuss interpretation: what does the adjusted estimate mean?

# %%
# Generate healthcare dataset with confounded treatment.
df_health, G_health = utils.cell2_healthcare_dataset(n_samples=500)

display(df_health.head())
print(f"\nDataset shape: {df_health.shape}")

# %%
utils.cell2_plot_backdoor_dag(G_health)

# %%
# Compute naive ATE and show the bias.
naive_ate = utils.cell2_compute_naive_ate(df_health)
print(f"Naive ATE (biased): {naive_ate:.3f}")
print("This estimate is biased because severity confounds the medication-recovery relationship.")

# %%
# Interactive widget: compare different adjustment methods.
utils.cell2_interactive_adjustment_methods(df_health)

# %% [markdown]
# # Cell 3: Natural Experiments and Instrumental Variables
#
# - Scenario: estimating effect of education on earnings with unobserved ability
# - Problem: ability is unobserved confounder (causes both education and earnings)
# - Solution: find an instrumental variable (IV)
#   - Distance to college affects education but not earnings directly
#   - Valid IV: affects outcome only through treatment
# - 2SLS: two-stage least squares estimation
#   - First stage: predict treatment from instrument
#   - Second stage: use predicted treatment to estimate outcome effect
# - Interactive widget: vary instrument strength, observe effect on estimate stability

# %%
# Generate education-earnings dataset with unobserved ability.
df_edu, G_edu = utils.cell3_education_earnings_dataset(n_samples=500)

display(df_edu.head())
print(f"\nNote: Ability is unobserved; Distance is the instrument.")

# %%
# Compute 2SLS estimate of education effect on earnings.
iv_results = utils.cell3_compute_2sls(df_edu)
print(f"First-stage coefficient (Distance → Education): {iv_results['first_stage']:.3f}")
print(f"2SLS estimate (LATE): {iv_results['late']:.0f}")
print(f"True effect: ~15000 (education increases earnings by ~$15k)")

# %%
# Interactive widget: explore IV strength sensitivity.
utils.cell3_interactive_iv_strength(df_edu)

# %% [markdown]
# # Cell 4: Natural Experiments and Quasi-Experimental Designs
#
# - Scenario: policy rollout that affects some units but not others
# - Difference-in-differences (DiD) estimation
#   - Compare treated vs control groups before and after intervention
#   - Estimate effect as the difference in trends
# - Diagnostic: parallel trends assumption (trends should align pre-treatment)
# - Example: regional policy rollout or cohort-based policy change

# %%
# Generate policy intervention dataset.
df_did = utils.cell4_policy_dataset(n_units=200, n_periods=3)

display(df_did.head(10))

# %%
# Visualize the DiD trends.
utils.cell4_plot_did_trends(df_did)

# %%
# Compute difference-in-differences estimate.
did_estimate = utils.cell4_compute_did(df_did)
print(f"DiD estimate: {did_estimate:.2f}")
print(f"True treatment effect: ~15 (policy increases outcome by 15 units)")
print(f"The estimate is valid if the parallel trends assumption holds.")

# %% [markdown]
# # Cell 5: Conditional Average Treatment Effects (CATE)
#
# - Question: does treatment work equally for everyone?
# - Heterogeneous treatment effects: effects vary across subgroups
# - CATE: estimate effect separately for each subgroup (by age, severity, etc.)
# - Visualize: heatmap showing effect heterogeneity
# - Interactive tool: select patient profile, see predicted personalized effect
# - Interpretation: which subgroups benefit most? Which least?

# %%
# Estimate CATE by disease severity.
cate_df = utils.cell5_estimate_cate(df_health, by_var="Severity", n_groups=3)

display(cate_df)

# %%
# Plot treatment effect heterogeneity.
utils.cell5_plot_cate_heterogeneity(cate_df)

# %%
# Interactive tool: predict treatment effect for specific patient profile.
utils.cell5_interactive_patient_profile(df_health)

# %% [markdown]
# # Cell 6: Causal Effects Using Graphical Causal Models
#
# - Use fitted structural causal model (SCM) to estimate treatment effects
# - Advantage: can answer effects without observational data once model is fitted
# - Method: do-calculus via Monte Carlo
#   - Define intervention: set treatment to specific value
#   - Generate counterfactual samples under intervention
#   - Compute ATE as difference between do(T=1) and do(T=0)
# - Compare estimates across methods: regression, IV, GCM
# - Discussion: when is each method most reliable?

# %%
# Generate synthetic dataset from known SCM.
df_scm, G_scm = utils.cell6_synthetic_scm_dataset(n_samples=300)

display(df_scm.head())

# %%
# Estimate treatment effect via GCM (do-calculus).
gcm_results = utils.cell6_estimate_effect_via_gcm(df_scm, G_scm)
print(f"GCM-based ATE (X → Y): {gcm_results['ate']:.3f}")
print(f"E[Y | do(X=1)]: {gcm_results['mean_y_do_1']:.3f}")
print(f"E[Y | do(X=0)]: {gcm_results['mean_y_do_0']:.3f}")

# %%
# Compare estimates across different methods.
comparison_df = utils.cell6_compare_methods(df_scm, G_scm)

display(comparison_df)

# %% [markdown]
# # Part 2: Quantifying Causal Influence
#
# - Move beyond average effects to understand system structure
# - Learn which variables most influence others
# - Quantify strength of individual causal arrows
# - Measure how much of variable's behavior is determined vs. stochastic

# %% [markdown]
# # Cell 7: Mediation Analysis – Direct vs. Indirect Effects
#
# - Decompose causal effect into pathways
#   - Direct effect (NDE): effect without going through mediator
#   - Indirect effect (NIE): effect that works through mediator
#   - Total effect = NDE + NIE
# - Example: does education affect earnings directly, or through experience?
# - Regression-based decomposition: sequential OLS models
# - Visualization: pathway diagram with effect sizes
# - Interactive: toggle mediators to see contribution changes

# %%
# Generate education-earnings-experience dataset.
df_mediation, G_mediation = utils.cell7_mediation_dataset(n_samples=400)

display(df_mediation.head())

# %%
# Estimate mediation effects.
med_results = utils.cell7_estimate_mediation(df_mediation)
print(f"Natural Direct Effect (NDE): {med_results['nde']:.0f}")
print(f"Natural Indirect Effect (NIE): {med_results['nie']:.0f}")
print(f"Total Effect: {med_results['total_effect']:.0f}")
print(f"Percent Mediated: {med_results['pct_mediated']:.1f}%")

# %%
# Visualize mediation pathways.
utils.cell7_plot_mediation_pathways(df_mediation, med_results)

# %% [markdown]
# # Cell 8: Direct Effect / Quantifying Arrow Strength
#
# - In complex systems, which causal arrows matter most?
# - Measure arrow strength: regression coefficient per edge
# - Interpret: percentage change in outcome per unit change in input
# - Visualization: DAG with edge thickness/color proportional to strength
# - Application: identify key control points and leverage points in system

# %%
# Generate supply chain dataset.
df_supply, G_supply = utils.cell8_supply_chain_dataset(n_samples=300)

display(df_supply.head())

# %%
# Estimate arrow strengths for each causal edge.
arrow_strengths = utils.cell8_estimate_arrow_strengths(df_supply, G_supply)

print("Arrow Strengths (regression coefficients):")
for (parent, child), strength in arrow_strengths.items():
    print(f"  {parent} → {child}: {strength:.4f}")

# %%
# Plot weighted DAG with arrows colored/sized by strength.
utils.cell8_plot_weighted_dag(G_supply, arrow_strengths)

# %% [markdown]
# # Cell 9: Intrinsic Causal Influence (ICC)
#
# - How much of a variable's variation is caused by upstream nodes vs. noise?
# - ICC: measure of causal "control" over a variable
#   - High ICC: variable is tightly determined by its causes (predictable)
#   - Low ICC: variable has intrinsic randomness (stochastic)
# - Estimate: R² of regression on parents
# - Visualization: node coloring by ICC (dark = high ICC, light = low ICC)
# - Interpretation: which variables are most "controlled"?

# %%
# Compute intrinsic causal influence for each node.
icc_scores = utils.cell9_compute_icc(df_supply, G_supply)

print("Intrinsic Causal Influence (R² of fit):")
for node, icc in icc_scores.items():
    print(f"  {node}: {icc:.3f}")

# %%
# Visualize nodes colored by ICC.
utils.cell9_plot_icc(G_supply, icc_scores)

# %% [markdown]
# # Part 3: Root-Cause Analysis and Explanation
#
# - When things go wrong: what caused the problem?
# - Trace anomalies back through causal mechanisms
# - Decompose distributional shifts into feature contributions
# - Distinguish causally relevant features from proxy variables

# %% [markdown]
# # Cell 10: Anomaly Attribution
#
# - Scenario: system latency spike—which input caused it?
# - Approach: counterfactual reasoning
#   - Baseline: what is normal operation?
#   - Anomaly: what actually happened?
#   - Counterfactual: if only input X had been anomalous, what outcome?
# - Attribution: assign responsibility to each causal input
# - Interactive dashboard: explore anomaly contributions

# %%
# Generate system metrics dataset.
df_sys, G_sys = utils.cell10_system_metrics_dataset(n_samples=200)

display(df_sys.head())

# %%
# Inject an anomaly and attribute it.
baseline, anomaly = utils.cell10_inject_anomaly(df_sys)

print("Baseline conditions (normal operation):")
for var in ["CpuUsage", "MemoryUsage", "NetworkLatency"]:
    print(f"  {var}: {baseline[var]:.1f}")

print("\nAnomaly values:")
for var in ["CpuUsage", "MemoryUsage", "NetworkLatency"]:
    print(f"  {var}: {anomaly[var]:.1f}")

# %%
# Interactive anomaly attribution dashboard.
utils.cell10_interactive_anomaly_dashboard(df_sys, G_sys)

# %% [markdown]
# # Cell 11: Attributing Distributional Changes
#
# - Problem: population-level outcomes changed; which feature changes drove it?
# - Example: customer base ages, satisfaction drops—how much is due to age?
# - Method: causal decomposition
#   - Quantify how each feature distribution changed
#   - Use causal model to predict outcome impact of each change
#   - Decompose: ΔOutcome ≈ Σ CausalEffect(Feature) × ΔFeatureDistribution
# - Application: diagnose what's driving business metric changes

# %%
# Generate before/after customer datasets with distributional shift.
df_before, df_after = utils.cell11_customer_shift_dataset()

print("Before: Younger, lower-income customers")
print(f"  Mean Age: {df_before['Age'].mean():.1f}, Mean Satisfaction: {df_before['Satisfaction'].mean():.2f}")

print("\nAfter: Older, higher-income customers")
print(f"  Mean Age: {df_after['Age'].mean():.1f}, Mean Satisfaction: {df_after['Satisfaction'].mean():.2f}")

# %%
# Compute distribution shift attribution.
shift_results = utils.cell11_compute_shift_attribution(df_before, df_after)

display(shift_results)

# %%
# Visualize shift attribution.
utils.cell11_plot_shift_attribution(shift_results)

# %% [markdown]
# # Cell 12: Feature Relevance in Causal Context
#
# - Not all correlates are causes; ML models may rely on proxies
# - Problem: which features actually cause the outcome?
# - Solution: compare causal vs. statistical relevance
#   - Causal: direct effect after adjusting for confounders
#   - Statistical: correlation or feature importance
#   - Divergence: feature is a proxy, not a cause
# - Example: ML says ZIP code is most important for loan approval
#   - But causally, only income and credit score matter
#   - ZIP code is a proxy that happens to correlate

# %%
# Generate loan dataset with proxy variable.
df_loan, G_loan = utils.cell12_loan_dataset(n_samples=400)

display(df_loan.head())

# %%
# Compute causal relevance for each feature.
causal_rel = utils.cell12_compute_causal_relevance(df_loan, G_loan)

print("Causal Relevance (direct effects):")
display(causal_rel)

# %%
# Compute statistical relevance for comparison.
stat_rel = utils.cell12_compute_statistical_relevance(df_loan)

print("Statistical Relevance (correlations):")
display(stat_rel)

# %%
# Compare causal vs. statistical importance side-by-side.
utils.cell12_plot_causal_vs_statistical(causal_rel, stat_rel)

# %% [markdown]
# # Part 4: Answering What-If Questions
#
# - Use causal models to predict outcomes under hypothetical interventions
# - Design optimal policies by understanding heterogeneous treatment effects
# - Make robust recommendations for decision-making

# %% [markdown]
# # Cell 13: Simulating Impact of Interventions
#
# - Business planning: "What if we increase marketing spend by 50%?"
# - Method: causal simulation
#   - Intervene on policy variable (set to specific value)
#   - Use fitted model to predict outcome under that intervention
#   - Simulate multiple scenarios: spend at 50%, 100%, 150%, 200% levels
#   - Visualize dose-response curve
# - Application: budget allocation, policy design, scenario planning

# %%
# Generate marketing dataset.
df_marketing, G_marketing = utils.cell13_marketing_dataset(n_samples=300)

display(df_marketing.head())

# %%
# Simulate dose-response curve.
dose_response = utils.cell13_simulate_dose_response(df_marketing, G_marketing)

display(dose_response)

# %%
# Plot dose-response curve.
utils.cell13_plot_dose_response(dose_response)

# %%
# Interactive widget to explore interventions.
utils.cell13_interactive_intervention(df_marketing, G_marketing)

# %% [markdown]
# # Cell 14: Computing Counterfactuals
#
# - Individual-level what-if: "If this patient had taken Drug A instead of B, would they recover?"
# - Method: counterfactual reasoning
#   - Observe: actual treatment and outcome
#   - Intervene: set treatment to alternative value
#   - Predict: outcome under alternative treatment using fitted SCM
#   - Compare: actual vs. counterfactual
# - Application: treatment optimization, regret analysis, accountability

# %%
# Interactive tool for individual counterfactual analysis.
utils.cell14_interactive_counterfactual(df_sys, G_sys)

# %% [markdown]
# # Cell 15: Optimal Policy Estimation
#
# - Resource allocation: "Which customers should receive premium support?"
# - Strategy: estimate conditional treatment effects (CATE)
#   - For each unit, estimate how much their outcome improves with treatment
#   - Optimal policy: assign treatment to units with highest predicted benefit
#   - Estimate value of optimal policy vs. actual allocation
# - Application: customer prioritization, intervention targeting, resource optimization

# %%
# Generate customer support dataset.
df_support, G_support = utils.cell15_customer_support_dataset(n_samples=300)

display(df_support.head())

# %%
# Plot actual vs. optimal treatment allocation.
utils.cell15_plot_policy_comparison(df_support)

# %%
# Interactive widget for exploring policy thresholds.
utils.cell15_interactive_policy(df_support)

# %% [markdown]
# # Part 5: Causal Prediction
#
# - ML models fail under distribution shift; causal models are more robust
# - Learn when to trust causal predictions for out-of-distribution data
# - Understand transportability: when do results generalize across populations?

# %% [markdown]
# # Cell 16: Predicting Outcomes for Out-of-Distribution Inputs
#
# - Problem: ML model trained on historical data fails in new population
#   - Reason: model captures correlations, which don't hold OOD
# - Solution: use causal model based on mechanisms
#   - Causal model captures functional relationships (mechanisms)
#   - Mechanisms generalize even under distribution shift
# - Comparison: ML vs causal prediction accuracy on OOD data
# - Discussion: when should you trust causal predictions?

# %%
# Generate training and OOD test datasets.
df_train, df_test = utils.cell16_generate_ood_data(n_train=300, n_test=100)

print(f"Training data range: X ∈ [{df_train['X'].min():.2f}, {df_train['X'].max():.2f}]")
print(f"Test data range (OOD): X ∈ [{df_test['X'].min():.2f}, {df_test['X'].max():.2f}]")

# %%
# Fit ML and causal models.
ml_params, causal_params = utils.cell16_fit_ml_and_causal_models(df_train)

print(f"Fitted models:")
print(f"  Intercept: {ml_params['intercept']:.2f}")
print(f"  Slope: {ml_params['slope']:.2f}")

# %%
# Compare predictions on OOD data.
perf_df = utils.cell16_compare_ood_predictions(df_test, ml_params, causal_params)

display(perf_df)

# %%
# Plot OOD prediction comparison.
utils.cell16_plot_ood_comparison(df_train, df_test)

# %% [markdown]
# # Cell 17: Transportability and Generalization
#
# - Question: does treatment effect from Population A apply to Population B?
# - Challenge: populations may differ in covariate distributions
# - Solution: assess transportability
#   - Check if mechanisms differ between populations
#   - Reweight treatment effect using target population covariate distribution
#   - Compute adjusted estimate for target population
# - Discussion: assumptions for valid transport and generalization

# %%
# Generate datasets from two populations with different distributions.
pop_a, pop_b = utils.cell17_two_population_dataset()

print("Population A: Mean age = {:.1f}".format(pop_a['Age'].mean()))
print("Population B: Mean age = {:.1f}".format(pop_b['Age'].mean()))

# %%
# Interactive widget comparing populations.
utils.cell17_interactive_population_comparison(pop_a, pop_b)

# %% [markdown]
# # Part 6: Integration and Application
#
# - Synthesize understanding of all methods
# - Learn when to apply each method to real problems
# - Run complete end-to-end causal analysis

# %% [markdown]
# # Cell 18: Choosing the Right Method for Your Causal Question
#
# - Decision tree: what is your question? What data do you have?
#   - Estimating effects? → Backdoor, IV, DiD, GCM, CATE
#   - Explaining system? → Mediation, arrow strength, ICC, feature relevance
#   - Finding root causes? → Anomaly attribution, shift decomposition
#   - Answering what-if? → Counterfactuals, interventions, optimal policy
# - For each method: when applicable, data requirements, assumptions, limitations
# - Interactive quiz: given scenario, select appropriate method
# - Insight: multiple methods may apply with different trade-offs

# %%
# Interactive decision tree for method selection.
utils.cell18_interactive_decision_tree()

# %% [markdown]
# # Cell 19: Comprehensive Case Study – End-to-End Causal Analysis
#
# - Scenario: e-commerce platform wants to understand marketing ROI
# - Workflow
#   1. Define causal question: "What is the effect of marketing budget on revenue?"
#   2. Specify causal graph from domain knowledge
#   3. Collect data and fit structural causal model
#   4. Estimate treatment effects using multiple methods
#   5. Conduct mediation analysis: which pathways matter? (traffic or conversion?)
#   6. Perform subgroup analysis: which customer segments benefit most?
#   7. Design optimal allocation policy
#   8. Assess robustness: sensitivity to unobserved confounding
# - Deliverables: actionable insights and policy recommendations

# %%
# Generate e-commerce dataset.
df_ecommerce, G_ecommerce = utils.cell19_ecommerce_dataset(n_samples=500)

display(df_ecommerce.head())

# %%
# Run comprehensive causal analysis.
analysis_results = utils.cell19_run_full_analysis(df_ecommerce, G_ecommerce)

print("Case Study: E-Commerce Marketing ROI")
print(f"  Regression-based ATE: {analysis_results['regression_ate']:.2f}")
print(f"  GCM-based ATE: {analysis_results['gcm_ate']:.2f}")
print(f"  Estimates are similar, suggesting robust effect")

# %%
# Plot comprehensive summary.
utils.cell19_plot_case_study_summary(analysis_results)

# %% [markdown]
# # Cell 20: Limitations, Assumptions, and When Causal Methods Fail
#
# - Key assumptions underlying causal inference
#   - Causal Markov condition: no hidden common causes
#   - Causal sufficiency: all confounders are measured
#   - SUTVA: treatment of one unit doesn't affect others
#   - Consistency: treatment is well-defined
#   - Positivity: all subgroups have positive probability of treatment
# - Consequences of violated assumptions
#   - Unobserved confounding → biased estimates
#   - Indirect effects / spillovers → invalid treatment definitions
#   - Mechanism instability → predictions fail OOD
#   - Model misspecification → wrong causal conclusions
# - Real-world examples where causal methods failed
#   - Policy that worked in one context failed in another
#   - Treatment effect flipped when analyzed in subgroups
#   - Mediation mechanism was later disproven
# - Practical guidance
#   - Assess plausibility of assumptions (domain expertise, sensitivity analysis)
#   - Red flags: when to be skeptical of causal conclusions
#   - Complementary approaches: combine methods, triangulate, fail-safe strategies
#   - When to pause: what evidence would change your conclusion?
