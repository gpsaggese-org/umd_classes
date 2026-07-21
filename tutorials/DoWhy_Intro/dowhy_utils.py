"""
Utility functions for DoWhy-based causal inference workflows.

Import as:

import dowhy_utils as ut
"""
import logging
from typing import Any, Dict, List, Optional

import dowhy
import helpers.hdbg as hdbg
import helpers.hnotebook as hnotebook
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from dowhy import datasets

_LOG = logging.getLogger(__name__)


# #########################################################################
# Logging and notebook configuration
# #########################################################################


def init_logger(notebook_log: logging.Logger) -> None:
    """
    Configure notebook display settings and the assertion logger.

    :param notebook_log: logger instance from the calling notebook
    """
    hnotebook.config_notebook()
    hdbg.init_logger(verbosity=logging.INFO, use_exec_path=False)
    notebook_log.setLevel(logging.INFO)
    _LOG.setLevel(logging.INFO)


# #########################################################################
# Data loading
# #########################################################################


def load_lalonde_dataset() -> pd.DataFrame:
    """
    Load the Lalonde job training dataset.

    The Lalonde dataset is a standard benchmark for causal inference methods.
    Treatment is participation in a job training program, outcome is
    post-intervention earnings.

    :return: DataFrame with treatment, outcome, and covariate columns
    """
    data = datasets.lalonde_dataset()
    _LOG.info(
        "Loaded Lalonde dataset: %d rows, %d columns",
        data.shape[0],
        data.shape[1],
    )
    return data


def load_linear_dataset(
    *,
    n_samples: int = 1000,
    beta: float = 10.0,
    num_common_causes: int = 3,
    seed: int = 42,
) -> Dict[str, Any]:
    """
    Generate a synthetic linear dataset for API demonstrations.

    :param n_samples: number of observations to generate
    :param beta: true causal effect of treatment on outcome
    :param num_common_causes: number of confounding variables
    :param seed: random seed for reproducibility
    :return: dictionary with keys 'df', 'dot_graph', 'gml_graph', 'ate'
    """
    hdbg.dassert_lt(0, n_samples, "n_samples must be positive")
    np.random.seed(seed)
    data = datasets.linear_dataset(
        beta=beta,
        num_common_causes=num_common_causes,
        num_samples=n_samples,
        treatment_is_binary=True,
    )
    _LOG.info(
        "Generated linear dataset: n=%d, true ATE=%.2f",
        n_samples,
        beta,
    )
    return data


def load_iv_dataset(
    *,
    n_samples: int = 1000,
    beta: float = 10.0,
    num_common_causes: int = 1,
    num_instruments: int = 1,
    seed: int = 42,
) -> Dict[str, Any]:
    """
    Generate a synthetic dataset with instrumental variables.

    Use when the backdoor path is blocked by unobserved confounding but an
    instrument is available. An instrument affects treatment but not outcome
    directly.

    :param n_samples: number of observations to generate
    :param beta: true causal effect of treatment on outcome
    :param num_common_causes: number of confounding variables
    :param num_instruments: number of instrumental variables
    :param seed: random seed for reproducibility
    :return: dictionary with keys 'df', 'dot_graph', 'gml_graph', 'ate'
    """
    hdbg.dassert_lt(0, n_samples, "n_samples must be positive")
    hdbg.dassert_lt(0, num_instruments, "num_instruments must be positive")
    np.random.seed(seed)
    data = datasets.linear_dataset(
        beta=beta,
        num_common_causes=num_common_causes,
        num_instruments=num_instruments,
        num_samples=n_samples,
        treatment_is_binary=True,
    )
    _LOG.info(
        "Generated IV dataset: n=%d, instruments=%d, true ATE=%.2f",
        n_samples,
        num_instruments,
        beta,
    )
    return data


def load_frontdoor_dataset(
    *,
    n_samples: int = 1000,
    beta: float = 10.0,
    num_frontdoor_variables: int = 1,
    seed: int = 42,
) -> Dict[str, Any]:
    """
    Generate a synthetic dataset with a frontdoor mediator.

    Use when unobserved confounding blocks the backdoor path but a measured
    mediator carries the full effect of treatment on outcome.

    :param n_samples: number of observations to generate
    :param beta: true causal effect of treatment on outcome
    :param num_frontdoor_variables: number of mediator variables
    :param seed: random seed for reproducibility
    :return: dictionary with keys 'df', 'dot_graph', 'gml_graph', 'ate'
    """
    hdbg.dassert_lt(0, n_samples, "n_samples must be positive")
    hdbg.dassert_lt(
        0, num_frontdoor_variables, "num_frontdoor_variables must be positive"
    )
    np.random.seed(seed)
    data = datasets.linear_dataset(
        beta=beta,
        num_common_causes=0,
        num_frontdoor_variables=num_frontdoor_variables,
        num_samples=n_samples,
        treatment_is_binary=True,
    )
    _LOG.info(
        "Generated frontdoor dataset: n=%d, mediators=%d, true ATE=%.2f",
        n_samples,
        num_frontdoor_variables,
        beta,
    )
    return data


# #########################################################################
# Causal model construction
# #########################################################################


def build_causal_model(
    df: pd.DataFrame,
    treatment: str,
    outcome: str,
    *,
    graph: Optional[str] = None,
    common_causes: Optional[List[str]] = None,
) -> dowhy.CausalModel:
    """
    Build a DoWhy CausalModel from data and causal assumptions.

    :param df: observational data
    :param treatment: name of the treatment column
    :param outcome: name of the outcome column
    :param graph: optional DOT-format causal graph string
    :param common_causes: optional list of confounder column names
    :return: configured CausalModel instance
    """
    hdbg.dassert_isinstance(df, pd.DataFrame)
    hdbg.dassert_in(treatment, df.columns, "Treatment column not found in data")
    hdbg.dassert_in(outcome, df.columns, "Outcome column not found in data")
    model = dowhy.CausalModel(
        data=df,
        treatment=treatment,
        outcome=outcome,
        graph=graph,
        common_causes=common_causes,
    )
    _LOG.info(
        "Built causal model: treatment=%s, outcome=%s",
        treatment,
        outcome,
    )
    return model


# #########################################################################
# Identification
# #########################################################################


def identify_effect(
    model: dowhy.CausalModel,
) -> Any:
    """
    Identify the causal effect from the graph.

    DoWhy auto-detects which criterion applies based on the graph topology:
    backdoor when the relevant confounders are observed, frontdoor when a
    mediator carries the full effect, and instrumental variable when an
    instrument is present.

    :param model: a configured CausalModel
    :return: identified estimand object
    """
    hdbg.dassert_isinstance(model, dowhy.CausalModel)
    estimand = model.identify_effect(
        proceed_when_unidentifiable=True,
    )
    _LOG.info("Identified estimand.")
    return estimand


# #########################################################################
# Estimation
# #########################################################################


def estimate_effect(
    model: dowhy.CausalModel,
    estimand: Any,
    *,
    method_name: str = "backdoor.propensity_score_matching",
) -> Any:
    """
    Estimate the causal effect using the specified method.

    :param model: a configured CausalModel
    :param estimand: identified estimand from identify_effect
    :param method_name: estimation method string
    :return: estimate object with value attribute
    """
    estimate = model.estimate_effect(
        estimand,
        method_name=method_name,
    )
    _LOG.info(
        "Estimated effect using %s: %.4f",
        method_name,
        estimate.value,
    )
    return estimate


def compare_estimators(
    model: dowhy.CausalModel,
    estimand: Any,
    *,
    methods: Optional[List[str]] = None,
) -> pd.DataFrame:
    """
    Run multiple estimation methods and compare results.

    :param model: a configured CausalModel
    :param estimand: identified estimand
    :param methods: list of method name strings to compare
    :return: DataFrame with method names and estimated effects
    """
    if methods is None:
        methods = [
            "backdoor.propensity_score_matching",
            "backdoor.linear_regression",
            "backdoor.propensity_score_weighting",
        ]
    results = []
    for method in methods:
        estimate = model.estimate_effect(
            estimand,
            method_name=method,
        )
        results.append({
            "method": method,
            "estimate": estimate.value,
        })
        _LOG.info("Method %s: estimate=%.4f", method, estimate.value)
    return pd.DataFrame(results)


# #########################################################################
# Refutation
# #########################################################################


def run_refutation(
    model: dowhy.CausalModel,
    estimand: Any,
    estimate: Any,
    *,
    method_name: str = "random_common_cause",
    **kwargs: Any,
) -> Any:
    """
    Run a refutation test on a causal estimate.

    :param model: a configured CausalModel
    :param estimand: identified estimand
    :param estimate: estimate to refute
    :param method_name: refutation method string
    :param kwargs: additional arguments passed to the refutation method
    :return: refutation result object
    """
    refutation = model.refute_estimate(
        estimand,
        estimate,
        method_name=method_name,
        **kwargs,
    )
    _LOG.info("Refutation (%s): %s", method_name, refutation)
    return refutation


def run_all_refutations(
    model: dowhy.CausalModel,
    estimand: Any,
    estimate: Any,
) -> Dict[str, Any]:
    """
    Run all standard refutation tests.

    :param model: a configured CausalModel
    :param estimand: identified estimand
    :param estimate: estimate to refute
    :return: dictionary mapping refutation names to result objects
    """
    refutation_methods = [
        "random_common_cause",
        "placebo_treatment_refuter",
        "data_subset_refuter",
    ]
    results = {}
    for method in refutation_methods:
        ref = run_refutation(
            model,
            estimand,
            estimate,
            method_name=method,
        )
        results[method] = ref
    return results


# #########################################################################
# Counterfactuals
# #########################################################################


def compute_counterfactual(
    df: pd.DataFrame,
    treatment: str,
    outcome: str,
    estimate: Any,
    *,
    treatment_value: float = 1.0,
    control_value: float = 0.0,
) -> pd.DataFrame:
    """
    Compute approximate counterfactual outcomes from a causal estimate.

    For each observation, approximate the counterfactual outcome (what the
    outcome would have been under the alternative treatment) by applying the
    estimated average treatment effect as a linear adjustment. This assumes
    a constant treatment effect and is intended as a tutorial illustration
    of the counterfactual concept. For per-individual counterfactuals that
    condition on covariates, use `compute_scm_counterfactual`.

    :param df: observational data
    :param treatment: name of the treatment column
    :param outcome: name of the outcome column
    :param estimate: causal estimate object with a `value` attribute
    :param treatment_value: value representing the treated state
    :param control_value: value representing the control state
    :return: DataFrame with observed treatment, observed outcome, and a
        counterfactual_outcome column
    """
    hdbg.dassert_isinstance(df, pd.DataFrame)
    hdbg.dassert_in(treatment, df.columns, "Treatment column not found in data")
    hdbg.dassert_in(outcome, df.columns, "Outcome column not found in data")
    ate = float(estimate.value)
    treatment_delta = treatment_value - control_value
    result = df[[treatment, outcome]].copy()
    # If observed as treated, subtract the ATE; if observed as control, add it.
    is_treated = df[treatment] == treatment_value
    result["counterfactual_outcome"] = np.where(
        is_treated,
        df[outcome] - ate * treatment_delta,
        df[outcome] + ate * treatment_delta,
    )
    _LOG.info("Computed counterfactuals using ATE=%.4f", ate)
    return result


def compute_scm_counterfactual(
    df: pd.DataFrame,
    treatment: str,
    outcome: str,
    common_causes: List[str],
    *,
    n_samples: Optional[int] = None,
) -> pd.DataFrame:
    """
    Compute counterfactual outcomes using a fitted structural causal model.

    Unlike `compute_counterfactual`, this does not assume a constant treatment
    effect. The function builds a `dowhy.gcm.StructuralCausalModel` from the
    treatment-outcome-confounder graph, fits causal mechanisms to the data,
    and queries the counterfactual outcome obtained by flipping the treatment
    of each observation.

    :param df: observational data
    :param treatment: name of the treatment column
    :param outcome: name of the outcome column
    :param common_causes: confounder column names
    :param n_samples: optional cap on rows; gcm fitting cost is roughly linear
    :return: DataFrame with observed treatment, observed outcome, and a
        counterfactual_outcome column
    """
    # gcm and networkx are heavyweight imports; defer them until used.
    import dowhy.gcm as gcm
    import networkx as nx

    hdbg.dassert_isinstance(df, pd.DataFrame)
    hdbg.dassert_in(treatment, df.columns, "Treatment column not found in data")
    hdbg.dassert_in(outcome, df.columns, "Outcome column not found in data")
    if n_samples is not None and n_samples < len(df):
        df = df.head(n_samples)
    # Cast treatment to float so dowhy's auto mechanism selection picks a
    # regression (invertible) rather than a classifier; gcm cannot recover
    # noise from a non-invertible classification mechanism.
    df = df.copy()
    df[treatment] = df[treatment].astype(float)
    edges = [(treatment, outcome)]
    for w in common_causes:
        hdbg.dassert_in(w, df.columns, "Confounder column not found in data")
        edges.append((w, treatment))
        edges.append((w, outcome))
    causal_graph = nx.DiGraph(edges)
    # InvertibleStructuralCausalModel is required because counterfactual_samples
    # recovers per-observation noise terms from observed data.
    scm = gcm.InvertibleStructuralCausalModel(causal_graph)
    gcm.auto.assign_causal_mechanisms(scm, df)
    gcm.fit(scm, df)
    # Counterfactual: flip the treatment for every observation.
    cf_samples = gcm.counterfactual_samples(
        scm,
        {treatment: lambda t: 1.0 - t},
        observed_data=df,
    )
    result = df[[treatment, outcome]].copy()
    result["counterfactual_outcome"] = cf_samples[outcome].values
    _LOG.info("Computed SCM counterfactuals on %d rows.", len(df))
    return result


# #########################################################################
# Visualization
# #########################################################################


def plot_causal_graph(model: dowhy.CausalModel) -> None:
    """
    Display the causal graph from a CausalModel.

    :param model: a configured CausalModel with a defined graph
    """
    model.view_model()
    _LOG.info("Displayed causal graph.")


def plot_estimate_comparison(results_df: pd.DataFrame) -> None:
    """
    Bar plot comparing estimates from different methods.

    :param results_df: DataFrame with 'method' and 'estimate' columns
    """
    hdbg.dassert_in("method", results_df.columns)
    hdbg.dassert_in("estimate", results_df.columns)
    _, ax = plt.subplots(figsize=(8, 4))
    ax.barh(results_df["method"], results_df["estimate"])
    ax.set_xlabel("Estimated Causal Effect")
    ax.set_title("Estimator Comparison")
    plt.tight_layout()
    plt.show()
