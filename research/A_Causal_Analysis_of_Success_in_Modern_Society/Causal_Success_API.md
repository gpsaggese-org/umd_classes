# API Reference

**For comprehensive documentation, see the source code docstrings in `causal_success_utils.py`**

Each function has detailed docstrings explaining:
- What it does and why
- Parameters and return values
- Typical results and interpretation
- Usage examples

**For interactive demos and working examples, see `causal_success_API.ipynb`**

## Quick Function List

### Simulation
- `create_population(n_agents, seed)` - Generate agents
- `run_simulation(agents, n_periods, ...)` - Run simulation
- `run_policy_simulation(agents, policy, resource_amount, ...)` - With resource allocation

### Analysis
- `calculate_gini(values)` - Inequality metric
- `get_results_dataframe(agents)` - Convert to DataFrame
- `generate_summary_statistics(agents)` - Summary metrics
- `validate_simulation_results(agents)` - Data integrity checks

### Bayesian (optional)
- `fit_bayesian_luck_model(df, ...)` - Fit Bayesian model
- `summarize_bayesian_fit(idata)` - Posterior summaries
- `posterior_predictive_check(model, idata, df)` - Model validation

**To view full documentation:** `help(causal_success_utils.create_population)` etc.
