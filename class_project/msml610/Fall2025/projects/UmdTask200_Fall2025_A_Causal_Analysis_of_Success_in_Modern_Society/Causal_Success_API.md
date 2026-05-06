## Complete Example Workflow

```python
import numpy as np
import pandas as pd
from causal_success_utils import (
    create_population,
    run_simulation,
    get_results_dataframe,
    calculate_gini,
    generate_summary_statistics,
    validate_simulation_results,
)

agents = create_population(n_agents=100, seed=42)
agents = run_simulation(agents, n_periods=80, seed=42, verbose=True)

validate_simulation_results(agents)

df = get_results_dataframe(agents)
gini = calculate_gini(df["capital"].values)
stats = generate_summary_statistics(agents)

print("Gini:", gini)
print("Top 10% share:", stats["top_10_pct_share"])
```

---

## Bayesian Inference API

In addition to the simulation and descriptive statistics, the project includes a **Bayesian regression layer** that estimates the effect of luck on log-capital while controlling for talent.

All Bayesian functions live in `causal_success_utils.py` and rely on **PyMC** and **ArviZ**. They are **optional**: if these libraries are not installed, you can still run the simulation and summary functions.

### Overview of the Model

The Bayesian model is a linear regression on the log of final capital:

\[
\log(\text{capital}_i) =
\alpha
+ \beta_{\text{luck}} \cdot \text{lucky\_events}_i
+ \beta_{\text{intensity}} \cdot \text{talent\_intensity}_i
+ \beta_{\text{iq}} \cdot \text{talent\_iq}_i
+ \beta_{\text{networking}} \cdot \text{talent\_networking}_i
+ \varepsilon_i
\]

- `beta_luck` is the primary quantity of interest: the (log-scale) effect of one additional lucky event, holding talent constant.  
- Priors are weakly informative, centered at 0.

### `fit_bayesian_luck_model`

```python
from causal_success_utils import (
    create_population,
    run_simulation,
    get_results_dataframe,
    fit_bayesian_luck_model,
)

# Simulate data
agents = create_population(n_agents=100, seed=42)
agents = run_simulation(agents, n_periods=80, seed=42)
df = get_results_dataframe(agents)

# Fit Bayesian model
model, idata = fit_bayesian_luck_model(
    df,
    draws=1000,
    tune=1000,
    target_accept=0.9,
    random_seed=42,
)
```

**Arguments:**

- `df: pd.DataFrame` – output from `get_results_dataframe`  
- `draws: int` – posterior draws per chain (default 1000)  
- `tune: int` – warm-up / burn-in iterations (default 1000)  
- `target_accept: float` – NUTS target acceptance rate (default 0.9)  
- `random_seed: int` – random seed

**Returns:**

- `model` – PyMC model object  
- `idata` – ArviZ `InferenceData` with posterior samples

> Note: If PyMC or ArviZ are not installed, this function will raise an `ImportError`.

### `summarize_bayesian_fit`

Get a tidy summary table (posterior mean, standard deviation, and credible intervals) for the main parameters.

```python
from causal_success_utils import summarize_bayesian_fit

summary = summarize_bayesian_fit(idata)
print(summary)
```

By default, it summarizes:

- `alpha`  
- `beta_luck`  
- `beta_intensity`  
- `beta_iq`  
- `beta_networking`  
- `sigma`

You can also pass a custom `var_names` list if you want to restrict the summary.

### `posterior_predictive_check`

Run a basic posterior predictive check (PPC) by simulating log-capital from the model and comparing to the observed log-capital.

```python
from causal_success_utils import posterior_predictive_check

ppc_results = posterior_predictive_check(model, idata, df)

y_obs = ppc_results["y_obs"]
y_pred_mean = ppc_results["y_pred_mean"]
y_pred_std = ppc_results["y_pred_std"]

print("Observed log-capital (first 5):", y_obs[:5])
print("Predicted mean log-capital (first 5):", y_pred_mean[:5])
```

**Returns a dictionary with:**

- `"y_obs"` – observed log-capital  
- `"y_pred_mean"` – posterior predictive mean log-capital per agent  
- `"y_pred_std"` – posterior predictive standard deviation per agent  

This is useful for checking how well the model captures the distribution of outcomes.

---

## When to Use What

- Use the **simulation functions** (`create_population`, `run_simulation`, `run_policy_simulation`) to generate data and explore how talent and luck interact in the model world.  
- Use the **summary and inequality functions** (`get_results_dataframe`, `generate_summary_statistics`, `calculate_gini`) to quantify emergent patterns (inequality, top shares, etc.).  
- Use the **Bayesian functions** (`fit_bayesian_luck_model`, `summarize_bayesian_fit`, `posterior_predictive_check`) when you want:
  - a principled posterior over the effect of luck,  
  - credible intervals around effect sizes,  
  - and basic model checking via posterior predictive simulations.

Together, these APIs give you a complete pipeline from simulation → descriptive analysis → causal and Bayesian inference.
