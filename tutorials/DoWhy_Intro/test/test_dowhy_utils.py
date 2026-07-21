import logging

import helpers.hunit_test as hunitest
import pandas as pd

import dowhy_utils as ut

_LOG = logging.getLogger(__name__)


class Test_load_linear_dataset(hunitest.TestCase):
    """
    Test synthetic data generation.
    """

    def test1(self) -> None:
        """
        Test that the linear dataset returns the expected structure.
        """
        # Run test.
        data = ut.load_linear_dataset(
            n_samples=100, beta=5.0, num_common_causes=2, seed=42,
        )
        # Check outputs.
        self.assertIn("df", data)
        self.assertIn("dot_graph", data)
        self.assertIsInstance(data["df"], pd.DataFrame)
        self.assertEqual(data["df"].shape[0], 100)

    def test2(self) -> None:
        """
        Test that different seeds produce different data.
        """
        # Run test.
        data1 = ut.load_linear_dataset(n_samples=50, seed=1)
        data2 = ut.load_linear_dataset(n_samples=50, seed=2)
        # Check outputs.
        self.assertFalse(data1["df"].equals(data2["df"]))


class Test_load_iv_dataset(hunitest.TestCase):
    """
    Test synthetic IV dataset generation.
    """

    def test1(self) -> None:
        """
        Test that the IV dataset contains instrument columns.
        """
        # Run test.
        data = ut.load_iv_dataset(
            n_samples=100, beta=5.0, num_instruments=1, seed=42,
        )
        # Check outputs.
        self.assertIn("df", data)
        self.assertIn("dot_graph", data)
        self.assertIsInstance(data["df"], pd.DataFrame)
        self.assertEqual(data["df"].shape[0], 100)
        # Instrument columns are prefixed with "Z" by dowhy's linear_dataset.
        instrument_cols = [c for c in data["df"].columns if c.startswith("Z")]
        self.assertGreaterEqual(len(instrument_cols), 1)


class Test_load_frontdoor_dataset(hunitest.TestCase):
    """
    Test synthetic frontdoor dataset generation.
    """

    def test1(self) -> None:
        """
        Test that the frontdoor dataset contains mediator columns.
        """
        # Run test.
        data = ut.load_frontdoor_dataset(
            n_samples=100, beta=5.0, num_frontdoor_variables=1, seed=42,
        )
        # Check outputs.
        self.assertIn("df", data)
        self.assertIn("dot_graph", data)
        self.assertIsInstance(data["df"], pd.DataFrame)
        self.assertEqual(data["df"].shape[0], 100)
        # Frontdoor mediator columns are prefixed with "FD" by dowhy's linear_dataset.
        mediator_cols = [c for c in data["df"].columns if c.startswith("FD")]
        self.assertGreaterEqual(len(mediator_cols), 1)


class Test_build_causal_model(hunitest.TestCase):
    """
    Test causal model construction.
    """

    def helper(self, n_samples: int, num_common_causes: int) -> None:
        """
        Test helper for building a causal model.

        :param n_samples: number of observations
        :param num_common_causes: number of confounders
        """
        # Prepare inputs.
        data = ut.load_linear_dataset(
            n_samples=n_samples,
            num_common_causes=num_common_causes,
            seed=42,
        )
        # Run test.
        model = ut.build_causal_model(
            data["df"],
            treatment="v0",
            outcome="y",
            graph=data["dot_graph"],
        )
        # Check outputs.
        self.assertIsNotNone(model)

    def test1(self) -> None:
        """
        Test model construction with small dataset.
        """
        self.helper(n_samples=50, num_common_causes=2)

    def test2(self) -> None:
        """
        Test model construction with larger dataset.
        """
        self.helper(n_samples=200, num_common_causes=5)


class Test_identify_effect(hunitest.TestCase):
    """
    Test causal effect identification.
    """

    def test1(self) -> None:
        """
        Test that identification returns a non-None estimand.
        """
        # Prepare inputs.
        data = ut.load_linear_dataset(n_samples=100, seed=42)
        model = ut.build_causal_model(
            data["df"],
            treatment="v0",
            outcome="y",
            graph=data["dot_graph"],
        )
        # Run test.
        estimand = ut.identify_effect(model)
        # Check outputs.
        self.assertIsNotNone(estimand)


class Test_estimate_effect(hunitest.TestCase):
    """
    Test causal effect estimation.
    """

    def helper(self, method_name: str) -> None:
        """
        Test helper for estimating causal effect with a given method.

        :param method_name: estimation method string
        """
        # Prepare inputs.
        data = ut.load_linear_dataset(
            n_samples=200, beta=10.0, seed=42,
        )
        model = ut.build_causal_model(
            data["df"],
            treatment="v0",
            outcome="y",
            graph=data["dot_graph"],
        )
        estimand = ut.identify_effect(model)
        # Run test.
        estimate = ut.estimate_effect(
            model, estimand, method_name=method_name,
        )
        # Check outputs.
        self.assertIsNotNone(estimate.value)

    def test1(self) -> None:
        """
        Test estimation with linear regression.
        """
        self.helper("backdoor.linear_regression")

    def test2(self) -> None:
        """
        Test estimation with propensity score weighting.
        """
        self.helper("backdoor.propensity_score_weighting")


class Test_compare_estimators(hunitest.TestCase):
    """
    Test multi-estimator comparison.
    """

    def test1(self) -> None:
        """
        Test that compare_estimators returns a DataFrame with expected columns.
        """
        # Prepare inputs.
        data = ut.load_linear_dataset(n_samples=200, seed=42)
        model = ut.build_causal_model(
            data["df"],
            treatment="v0",
            outcome="y",
            graph=data["dot_graph"],
        )
        estimand = ut.identify_effect(model)
        # Run test.
        results = ut.compare_estimators(model, estimand)
        # Check outputs.
        self.assertIsInstance(results, pd.DataFrame)
        self.assertIn("method", results.columns)
        self.assertIn("estimate", results.columns)
        self.assertEqual(len(results), 3)


class Test_run_refutation(hunitest.TestCase):
    """
    Test refutation methods.
    """

    def helper(self, method_name: str) -> None:
        """
        Test helper for running a refutation test.

        :param method_name: refutation method string
        """
        # Prepare inputs.
        data = ut.load_linear_dataset(n_samples=200, seed=42)
        model = ut.build_causal_model(
            data["df"],
            treatment="v0",
            outcome="y",
            graph=data["dot_graph"],
        )
        estimand = ut.identify_effect(model)
        estimate = ut.estimate_effect(
            model, estimand, method_name="backdoor.linear_regression",
        )
        # Run test.
        ref = ut.run_refutation(
            model, estimand, estimate, method_name=method_name,
        )
        # Check outputs.
        self.assertIsNotNone(ref)

    def test1(self) -> None:
        """
        Test random common cause refutation.
        """
        self.helper("random_common_cause")

    def test2(self) -> None:
        """
        Test placebo treatment refutation.
        """
        self.helper("placebo_treatment_refuter")

    def test3(self) -> None:
        """
        Test data subset refutation.
        """
        self.helper("data_subset_refuter")


class Test_compute_counterfactual(hunitest.TestCase):
    """
    Test counterfactual outcome computation.
    """

    def test1(self) -> None:
        """
        Test that counterfactual outcomes flip the ATE in the right direction.
        """
        # Prepare inputs.
        df = pd.DataFrame({
            "v0": [0, 1, 0, 1],
            "y": [5.0, 15.0, 7.0, 20.0],
        })

        class _MockEstimate:
            value = 10.0

        # Run test.
        result = ut.compute_counterfactual(
            df,
            "v0",
            "y",
            _MockEstimate(),
            treatment_value=1.0,
            control_value=0.0,
        )
        # Check outputs.
        self.assertIn("counterfactual_outcome", result.columns)
        # Row 0 is control, so counterfactual should be outcome + 10.
        self.assertEqual(result.iloc[0]["counterfactual_outcome"], 15.0)
        # Row 1 is treated, so counterfactual should be outcome - 10.
        self.assertEqual(result.iloc[1]["counterfactual_outcome"], 5.0)


class Test_compute_scm_counterfactual(hunitest.TestCase):
    """
    Test SCM-based counterfactual computation.
    """

    def test1(self) -> None:
        """
        Test that SCM counterfactuals return one row per observation with
        the expected columns.
        """
        # Prepare inputs.
        data = ut.load_linear_dataset(
            n_samples=100, beta=10.0, num_common_causes=2, seed=42,
        )
        df = data["df"]
        confounders = [c for c in df.columns if c.startswith("W")]
        # Run test.
        result = ut.compute_scm_counterfactual(
            df, "v0", "y", confounders, n_samples=50,
        )
        # Check outputs.
        self.assertEqual(len(result), 50)
        self.assertIn("counterfactual_outcome", result.columns)
        self.assertIn("v0", result.columns)
        self.assertIn("y", result.columns)
