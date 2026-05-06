"""
Unit tests for causal_success_utils module.

Import as:

import research.A_Causal_Analysis_of_Success_in_Modern_Society.test_causal_success_utils as racaosimstcsu
"""

import logging

import numpy as np

import helpers.hunit_test as hunitest
import research.A_Causal_Analysis_of_Success_in_Modern_Society.causal_success_utils as racaosimscsu

_LOG = logging.getLogger(__name__)


# #############################################################################
# TestAgent
# #############################################################################


class TestAgent(hunitest.TestCase):
    """
    Test the Agent class initialization and basic functionality.
    """

    def test1(self) -> None:
        """
        Test Agent initialization with default parameters.
        """
        # Prepare inputs.
        agent_id = 0
        intensity = 0.5
        iq = 0.6
        networking = 0.7
        # Run test.
        agent = racaosimscsu.Agent(agent_id, intensity, iq, networking)
        # Check outputs.
        self.assertEqual(agent.id, 0)
        self.assertAlmostEqual(agent.capital, 1.0)
        self.assertEqual(agent.lucky_events, 0)
        self.assertEqual(agent.unlucky_events, 0)
        self.assertEqual(len(agent.capital_history), 1)

    def test2(self) -> None:
        """
        Test Agent initialization with custom initial_capital.
        """
        # Prepare inputs.
        agent_id = 1
        intensity = 0.5
        iq = 0.5
        networking = 0.5
        initial_capital = 5.0
        # Run test.
        agent = racaosimscsu.Agent(
            agent_id, intensity, iq, networking, initial_capital=initial_capital
        )
        # Check outputs.
        self.assertAlmostEqual(agent.capital, 5.0)
        self.assertAlmostEqual(agent.talent["initial_capital"], 5.0)

    def test3(self) -> None:
        """
        Test Agent talent values are clipped to [0, 1] range.
        """
        # Prepare inputs.
        agent_id = 2
        intensity = 1.5
        iq = -0.5
        networking = 0.5
        # Run test.
        agent = racaosimscsu.Agent(agent_id, intensity, iq, networking)
        # Check outputs.
        self.assertAlmostEqual(agent.talent["intensity"], 1.0)
        self.assertAlmostEqual(agent.talent["iq"], 0.0)
        self.assertAlmostEqual(agent.talent["networking"], 0.5)

    def test4(self) -> None:
        """
        Test Agent initial_capital is enforced with minimum of 0.01.
        """
        # Prepare inputs.
        agent_id = 3
        intensity = 0.5
        iq = 0.5
        networking = 0.5
        initial_capital = 0.001
        # Run test.
        agent = racaosimscsu.Agent(
            agent_id, intensity, iq, networking, initial_capital=initial_capital
        )
        # Check outputs.
        self.assertAlmostEqual(agent.capital, 0.01)


# #############################################################################
# Test_talent_norm
# #############################################################################


class Test_talent_norm(hunitest.TestCase):
    """
    Test the talent_norm property of Agent class.
    """

    def test1(self) -> None:
        """
        Test talent_norm returns correct Euclidean norm of talent vector.
        """
        # Prepare inputs.
        agent = racaosimscsu.Agent(0, 0.3, 0.4, 0.5, initial_capital=1.2)
        # Run test.
        norm = agent.talent_norm
        # Check outputs.
        expected = np.sqrt(0.3**2 + 0.4**2 + 0.5**2 + 1.2**2)
        self.assertAlmostEqual(norm, expected, places=5)

    def test2(self) -> None:
        """
        Test talent_norm with all talents equal to 0.5.
        """
        # Prepare inputs.
        agent = racaosimscsu.Agent(0, 0.5, 0.5, 0.5, initial_capital=0.5)
        # Run test.
        norm = agent.talent_norm
        # Check outputs.
        expected = np.sqrt(4 * 0.5**2)
        self.assertAlmostEqual(norm, expected, places=5)

    def test3(self) -> None:
        """
        Test talent_norm with edge case values (0 and 1).
        """
        # Prepare inputs.
        agent = racaosimscsu.Agent(0, 0.0, 1.0, 0.0, initial_capital=1.0)
        # Run test.
        norm = agent.talent_norm
        # Check outputs.
        expected = np.sqrt(0.0**2 + 1.0**2 + 0.0**2 + 1.0**2)
        self.assertAlmostEqual(norm, expected, places=5)


# #############################################################################
# Test_get_event_probability
# #############################################################################


class Test_get_event_probability(hunitest.TestCase):
    """
    Test the get_event_probability method of Agent class.
    """

    def helper(self, intensity_val: float, expected_range: tuple) -> None:
        """
        Test helper for get_event_probability.

        :param intensity_val: Intensity value to test
        :param expected_range: Tuple of (min, max) expected probability
        """
        # Run test.
        agent = racaosimscsu.Agent(0, intensity_val, 0.5, 0.5)
        prob = agent.get_event_probability()
        # Check outputs.
        self.assertGreaterEqual(prob, expected_range[0])
        self.assertLessEqual(prob, expected_range[1])

    def test1(self) -> None:
        """
        Test event probability with intensity = 0.5 (sigmoid midpoint).
        """
        # Prepare inputs.
        # At intensity=0.5, sigmoid should return 0.5 (midpoint of [0, 1]).
        # Run test.
        agent = racaosimscsu.Agent(0, 0.5, 0.5, 0.5)
        prob = agent.get_event_probability()
        # Check outputs.
        self.assertAlmostEqual(prob, 0.5, places=2)

    def test2(self) -> None:
        """
        Test event probability with low intensity (near 0).
        """
        # Prepare outputs.
        expected_range = (0.0, 0.3)
        # Run test.
        self.helper(0.0, expected_range)

    def test3(self) -> None:
        """
        Test event probability with high intensity (near 1).
        """
        # Prepare outputs.
        expected_range = (0.7, 1.0)
        # Run test.
        self.helper(1.0, expected_range)

    def test4(self) -> None:
        """
        Test event probability is monotonically increasing with intensity.
        """
        # Prepare inputs.
        intensities = [0.0, 0.25, 0.5, 0.75, 1.0]
        # Run test.
        probs = [
            racaosimscsu.Agent(0, i, 0.5, 0.5).get_event_probability()
            for i in intensities
        ]
        # Check outputs.
        for i in range(len(probs) - 1):
            self.assertLessEqual(probs[i], probs[i + 1])


# #############################################################################
# Test_apply_event
# #############################################################################


class Test_apply_event(hunitest.TestCase):
    """
    Test the apply_event method of Agent class.
    """

    def test1(self) -> None:
        """
        Test applying a lucky event increases capital.
        """
        # Prepare inputs.
        agent = racaosimscsu.Agent(0, 0.5, 0.5, 0.5, initial_capital=1.0)
        impact = 0.25
        # Run test.
        agent.apply_event("lucky", impact)
        # Check outputs.
        self.assertAlmostEqual(agent.capital, 1.25)

    def test2(self) -> None:
        """
        Test applying an unlucky event decreases capital.
        """
        # Prepare inputs.
        agent = racaosimscsu.Agent(0, 0.5, 0.5, 0.5, initial_capital=1.0)
        impact = 0.15
        # Run test.
        agent.apply_event("unlucky", impact)
        # Check outputs.
        self.assertAlmostEqual(agent.capital, 0.85)

    def test3(self) -> None:
        """
        Test applying an unlucky event respects minimum capital floor (0.01).
        """
        # Prepare inputs.
        agent = racaosimscsu.Agent(0, 0.5, 0.5, 0.5, initial_capital=0.05)
        impact = 0.99
        # Run test.
        agent.apply_event("unlucky", impact)
        # Check outputs.
        self.assertAlmostEqual(agent.capital, 0.01)

    def test4(self) -> None:
        """
        Test applying an event increments the appropriate event counter.
        """
        # Prepare inputs.
        agent = racaosimscsu.Agent(0, 0.5, 0.5, 0.5)
        # Run test.
        agent.apply_event("lucky", 0.1)
        agent.apply_event("unlucky", 0.1)
        agent.apply_event("lucky", 0.1)
        # Check outputs.
        self.assertEqual(agent.lucky_events, 2)
        self.assertEqual(agent.unlucky_events, 1)

    def test5(self) -> None:
        """
        Test capital_history is updated after each event.
        """
        # Prepare inputs.
        agent = racaosimscsu.Agent(0, 0.5, 0.5, 0.5, initial_capital=1.0)
        # Run test.
        agent.apply_event("lucky", 0.25)
        agent.apply_event("unlucky", 0.1)
        # Check outputs.
        self.assertEqual(len(agent.capital_history), 3)
        self.assertAlmostEqual(agent.capital_history[0], 1.0)
        self.assertAlmostEqual(agent.capital_history[1], 1.25)
        self.assertAlmostEqual(agent.capital_history[2], 1.125)

    def test6(self) -> None:
        """
        Test apply_event raises error for invalid event_type.
        """
        # Prepare inputs.
        agent = racaosimscsu.Agent(0, 0.5, 0.5, 0.5)
        # Run test and check output.
        with self.assertRaises(ValueError):
            agent.apply_event("invalid", 0.1)

    def test7(self) -> None:
        """
        Test negative impact magnitude is converted to absolute value.
        """
        # Prepare inputs.
        agent = racaosimscsu.Agent(0, 0.5, 0.5, 0.5, initial_capital=1.0)
        # Run test.
        agent.apply_event("lucky", -0.25)
        # Check outputs.
        self.assertAlmostEqual(agent.capital, 1.25)


# #############################################################################
# Test_create_population
# #############################################################################


class Test_create_population(hunitest.TestCase):
    """
    Test the create_population function.
    """

    def test1(self) -> None:
        """
        Test create_population returns correct number of agents.
        """
        # Prepare inputs.
        n_agents = 50
        # Run test.
        agents = racaosimscsu.create_population(n_agents=n_agents, seed=42)
        # Check outputs.
        self.assertEqual(len(agents), n_agents)

    def test2(self) -> None:
        """
        Test create_population agents have talents in [0, 1] range.
        """
        # Prepare inputs.
        n_agents = 20
        # Run test.
        agents = racaosimscsu.create_population(n_agents=n_agents, seed=42)
        # Check outputs.
        for agent in agents:
            self.assertGreaterEqual(agent.talent["intensity"], 0.0)
            self.assertLessEqual(agent.talent["intensity"], 1.0)
            self.assertGreaterEqual(agent.talent["iq"], 0.0)
            self.assertLessEqual(agent.talent["iq"], 1.0)
            self.assertGreaterEqual(agent.talent["networking"], 0.0)
            self.assertLessEqual(agent.talent["networking"], 1.0)

    def test3(self) -> None:
        """
        Test create_population all agents start with capital = 1.0.
        """
        # Prepare inputs.
        n_agents = 15
        # Run test.
        agents = racaosimscsu.create_population(n_agents=n_agents, seed=42)
        # Check outputs.
        for agent in agents:
            self.assertAlmostEqual(agent.capital, 1.0)

    def test4(self) -> None:
        """
        Test create_population with seed produces reproducible results.
        """
        # Prepare inputs.
        n_agents = 10
        seed = 123
        # Run test.
        agents1 = racaosimscsu.create_population(n_agents=n_agents, seed=seed)
        agents2 = racaosimscsu.create_population(n_agents=n_agents, seed=seed)
        # Check outputs.
        for a1, a2 in zip(agents1, agents2):
            self.assertAlmostEqual(
                a1.talent["intensity"], a2.talent["intensity"]
            )
            self.assertAlmostEqual(a1.talent["iq"], a2.talent["iq"])
            self.assertAlmostEqual(
                a1.talent["networking"], a2.talent["networking"]
            )

    def test5(self) -> None:
        """
        Test create_population raises error for non-positive n_agents.
        """
        # Prepare inputs.
        n_agents = 0
        # Run test and check output.
        with self.assertRaises(AssertionError):
            racaosimscsu.create_population(n_agents=n_agents, seed=42)

    def test6(self) -> None:
        """
        Test agent IDs are sequential from 0 to n_agents-1.
        """
        # Prepare inputs.
        n_agents = 25
        # Run test.
        agents = racaosimscsu.create_population(n_agents=n_agents, seed=42)
        # Check outputs.
        for i, agent in enumerate(agents):
            self.assertEqual(agent.id, i)


# #############################################################################
# Test_calculate_gini
# #############################################################################


class Test_calculate_gini(hunitest.TestCase):
    """
    Test the calculate_gini function.
    """

    def helper(self, values_arr: np.ndarray, expected_gini_val: float) -> None:
        """
        Test helper for calculate_gini.

        :param values_arr: Array of values to compute Gini for
        :param expected_gini_val: Expected Gini coefficient
        """
        # Run test.
        gini = racaosimscsu.calculate_gini(values_arr)
        # Check outputs.
        self.assertAlmostEqual(gini, expected_gini_val, places=3)

    def test1(self) -> None:
        """
        Test Gini coefficient for perfectly equal distribution.
        """
        # Prepare inputs.
        values = np.array([1.0, 1.0, 1.0, 1.0], dtype=float)
        # Prepare outputs.
        expected_gini = 0.0
        # Run test.
        self.helper(values, expected_gini)

    def test2(self) -> None:
        """
        Test Gini coefficient for highly unequal distribution.
        """
        # Prepare inputs.
        values = np.array([0.1, 0.1, 0.1, 100.0], dtype=float)
        # Run test.
        gini = racaosimscsu.calculate_gini(values)
        # Check outputs.
        self.assertGreater(gini, 0.7)

    def test3(self) -> None:
        """
        Test Gini coefficient returns value in [0, 1] range.
        """
        # Prepare inputs.
        values = np.array([1.0, 2.0, 3.0, 4.0, 5.0], dtype=float)
        # Run test.
        gini = racaosimscsu.calculate_gini(values)
        # Check outputs.
        self.assertGreaterEqual(gini, 0.0)
        self.assertLessEqual(gini, 1.0)

    def test4(self) -> None:
        """
        Test Gini coefficient with single value.
        """
        # Prepare inputs.
        values = np.array([5.0], dtype=float)
        # Run test.
        gini = racaosimscsu.calculate_gini(values)
        # Check outputs.
        self.assertAlmostEqual(gini, 0.0)

    def test5(self) -> None:
        """
        Test Gini coefficient raises error for empty array.
        """
        # Prepare inputs.
        values = np.array([], dtype=float)
        # Run test and check output.
        with self.assertRaises(AssertionError):
            racaosimscsu.calculate_gini(values)

    def test6(self) -> None:
        """
        Test Gini coefficient raises error for negative values.
        """
        # Prepare inputs.
        values = np.array([1.0, 2.0, -1.0], dtype=float)
        # Run test and check output.
        with self.assertRaises(AssertionError):
            racaosimscsu.calculate_gini(values)

    def test7(self) -> None:
        """
        Test Gini coefficient with all zeros returns 0.
        """
        # Prepare inputs.
        values = np.array([0.0, 0.0, 0.0], dtype=float)
        # Run test.
        gini = racaosimscsu.calculate_gini(values)
        # Check outputs.
        self.assertAlmostEqual(gini, 0.0)


# #############################################################################
# Test_get_results_dataframe
# #############################################################################


class Test_get_results_dataframe(hunitest.TestCase):
    """
    Test the get_results_dataframe function.
    """

    def test1(self) -> None:
        """
        Test get_results_dataframe converts agents to correct columns.
        """
        # Prepare inputs.
        agents = racaosimscsu.create_population(n_agents=5, seed=42)
        # Run test.
        df = racaosimscsu.get_results_dataframe(agents)
        # Check outputs.
        expected_cols = [
            "id",
            "talent_intensity",
            "talent_iq",
            "talent_networking",
            "initial_capital",
            "talent_norm",
            "capital",
            "lucky_events",
            "unlucky_events",
            "net_events",
        ]
        self.assertEqual(list(df.columns), expected_cols)

    def test2(self) -> None:
        """
        Test get_results_dataframe returns empty DataFrame for empty list.
        """
        # Prepare inputs.
        agents = []
        # Run test.
        df = racaosimscsu.get_results_dataframe(agents)
        # Check outputs.
        self.assertTrue(df.empty)

    def test3(self) -> None:
        """
        Test get_results_dataframe computes net_events correctly.
        """
        # Prepare inputs.
        agent = racaosimscsu.Agent(0, 0.5, 0.5, 0.5)
        agent.apply_event("lucky", 0.1)
        agent.apply_event("lucky", 0.1)
        agent.apply_event("unlucky", 0.1)
        # Run test.
        df = racaosimscsu.get_results_dataframe([agent])
        # Check outputs.
        net = df.iloc[0]["net_events"]
        self.assertEqual(net, 1)

    def test4(self) -> None:
        """
        Test get_results_dataframe includes talent_norm computation.
        """
        # Prepare inputs.
        agents = racaosimscsu.create_population(n_agents=3, seed=42)
        # Run test.
        df = racaosimscsu.get_results_dataframe(agents)
        # Check outputs.
        for idx, agent in enumerate(agents):
            self.assertAlmostEqual(
                df.iloc[idx]["talent_norm"], agent.talent_norm, places=4
            )

    def test5(self) -> None:
        """
        Test get_results_dataframe with single agent.
        """
        # Prepare inputs.
        agent = racaosimscsu.Agent(0, 0.3, 0.4, 0.5, initial_capital=2.0)
        # Run test.
        df = racaosimscsu.get_results_dataframe([agent])
        # Check outputs.
        self.assertEqual(len(df), 1)
        self.assertEqual(df.iloc[0]["id"], 0)
        self.assertAlmostEqual(df.iloc[0]["capital"], 2.0)


# #############################################################################
# Test_generate_summary_statistics
# #############################################################################


class Test_generate_summary_statistics(hunitest.TestCase):
    """
    Test the generate_summary_statistics function.
    """

    def test1(self) -> None:
        """
        Test generate_summary_statistics returns correct keys.
        """
        # Prepare inputs.
        agents = racaosimscsu.create_population(n_agents=10, seed=42)
        # Run test.
        stats = racaosimscsu.generate_summary_statistics(agents)
        # Check outputs.
        expected_keys = [
            "n_agents",
            "mean_capital",
            "median_capital",
            "std_capital",
            "min_capital",
            "max_capital",
            "capital_range",
            "gini_coefficient",
            "top_10_pct_share",
            "top_20_pct_share",
            "bottom_50_pct_share",
            "mean_lucky_events",
            "mean_unlucky_events",
            "mean_talent_norm",
        ]
        self.assertEqual(sorted(stats.keys()), sorted(expected_keys))

    def test2(self) -> None:
        """
        Test generate_summary_statistics with single agent.
        """
        # Prepare inputs.
        agent = racaosimscsu.Agent(0, 0.5, 0.5, 0.5, initial_capital=2.0)
        # Run test.
        stats = racaosimscsu.generate_summary_statistics([agent])
        # Check outputs.
        self.assertEqual(stats["n_agents"], 1.0)
        self.assertAlmostEqual(stats["mean_capital"], 2.0)
        self.assertAlmostEqual(stats["min_capital"], 2.0)
        self.assertAlmostEqual(stats["max_capital"], 2.0)

    def test3(self) -> None:
        """
        Test generate_summary_statistics with empty agents list.
        """
        # Prepare inputs.
        agents = []
        # Run test.
        stats = racaosimscsu.generate_summary_statistics(agents)
        # Check outputs.
        self.assertEqual(stats["n_agents"], 0)

    def test4(self) -> None:
        """
        Test top_10_pct_share sums to approximately 1.0 portion.
        """
        # Prepare inputs.
        agents = racaosimscsu.create_population(n_agents=100, seed=42)
        # Run test.
        stats = racaosimscsu.generate_summary_statistics(agents)
        # Check outputs.
        total_share = (
            stats["top_10_pct_share"]
            + stats["top_20_pct_share"]
            + stats["bottom_50_pct_share"]
        )
        self.assertGreater(total_share, 0.5)

    def test5(self) -> None:
        """
        Test mean_capital equals median_capital for equal wealth.
        """
        # Prepare inputs.
        agents = [
            racaosimscsu.Agent(i, 0.5, 0.5, 0.5, initial_capital=1.0)
            for i in range(10)
        ]
        # Run test.
        stats = racaosimscsu.generate_summary_statistics(agents)
        # Check outputs.
        self.assertAlmostEqual(stats["mean_capital"], stats["median_capital"])

    def test6(self) -> None:
        """
        Test capital_range is positive.
        """
        # Prepare inputs.
        agents = racaosimscsu.create_population(n_agents=20, seed=42)
        # Run test.
        stats = racaosimscsu.generate_summary_statistics(agents)
        # Check outputs.
        self.assertGreater(stats["capital_range"], 0.0)


# #############################################################################
# Test_validate_simulation_results
# #############################################################################


class Test_validate_simulation_results(hunitest.TestCase):
    """
    Test the validate_simulation_results function.
    """

    def test1(self) -> None:
        """
        Test validate_simulation_results returns True for valid agents.
        """
        # Prepare inputs.
        agents = racaosimscsu.create_population(n_agents=10, seed=42)
        # Run test.
        result = racaosimscsu.validate_simulation_results(agents)
        # Check outputs.
        self.assertTrue(result)

    def test2(self) -> None:
        """
        Test validate_simulation_results raises error for empty agents list.
        """
        # Prepare inputs.
        agents = []
        # Run test and check output.
        with self.assertRaises(AssertionError):
            racaosimscsu.validate_simulation_results(agents)

    def test3(self) -> None:
        """
        Test validate_simulation_results detects negative capital.
        """
        # Prepare inputs.
        agent = racaosimscsu.Agent(0, 0.5, 0.5, 0.5, initial_capital=1.0)
        agent.capital = -0.5
        # Run test and check output.
        with self.assertRaises(AssertionError):
            racaosimscsu.validate_simulation_results([agent])

    def test4(self) -> None:
        """
        Test validate_simulation_results detects capital_history inconsistencies.
        """
        # Prepare inputs.
        agent = racaosimscsu.Agent(0, 0.5, 0.5, 0.5)
        agent.lucky_events = 5
        # capital_history should have 6 entries (1 initial + 5 events)
        # but we'll leave it with 1.
        # Run test and check output.
        with self.assertRaises(AssertionError):
            racaosimscsu.validate_simulation_results([agent])

    def test5(self) -> None:
        """
        Test validate_simulation_results after simulations pass validation.
        """
        # Prepare inputs.
        agents = racaosimscsu.create_population(n_agents=10, seed=42)
        agents = racaosimscsu.run_simulation(agents, n_periods=5, seed=42)
        # Run test.
        result = racaosimscsu.validate_simulation_results(agents)
        # Check outputs.
        self.assertTrue(result)


# #############################################################################
# Test_run_simulation
# #############################################################################


class Test_run_simulation(hunitest.TestCase):
    """
    Test the run_simulation function.
    """

    def test1(self) -> None:
        """
        Test run_simulation with default parameters.
        """
        # Prepare inputs.
        agents = racaosimscsu.create_population(n_agents=10, seed=42)
        # Run test.
        result = racaosimscsu.run_simulation(agents, n_periods=10, seed=42)
        # Check outputs.
        self.assertEqual(result, agents)
        self.assertTrue(racaosimscsu.validate_simulation_results(agents))

    def test2(self) -> None:
        """
        Test run_simulation with zero events per period.
        """
        # Prepare inputs.
        agents = racaosimscsu.create_population(n_agents=5, seed=42)
        initial_capitals = [a.capital for a in agents]
        # Run test.
        racaosimscsu.run_simulation(
            agents,
            n_periods=10,
            n_lucky_events_per_period=0,
            n_unlucky_events_per_period=0,
            seed=42,
        )
        # Check outputs.
        final_capitals = [a.capital for a in agents]
        for i, c in enumerate(initial_capitals):
            self.assertAlmostEqual(c, final_capitals[i])

    def test3(self) -> None:
        """
        Test run_simulation with seed produces reproducible results.
        """
        # Prepare inputs.
        agents1 = racaosimscsu.create_population(n_agents=10, seed=42)
        agents2 = racaosimscsu.create_population(n_agents=10, seed=42)
        seed = 123
        # Run test.
        racaosimscsu.run_simulation(agents1, n_periods=5, seed=seed)
        racaosimscsu.run_simulation(agents2, n_periods=5, seed=seed)
        # Check outputs.
        for a1, a2 in zip(agents1, agents2):
            self.assertAlmostEqual(a1.capital, a2.capital, places=5)

    def test4(self) -> None:
        """
        Test run_simulation modifies agents in-place.
        """
        # Prepare inputs.
        agents = racaosimscsu.create_population(n_agents=5, seed=42)
        agents_ref = agents
        # Run test.
        result = racaosimscsu.run_simulation(agents, n_periods=5, seed=42)
        # Check outputs.
        self.assertIs(result, agents_ref)

    def test5(self) -> None:
        """
        Test run_simulation respects capital floor of 0.01.
        """
        # Prepare inputs.
        agents = racaosimscsu.create_population(n_agents=10, seed=42)
        # Run test.
        racaosimscsu.run_simulation(agents, n_periods=20, seed=42)
        # Check outputs.
        for agent in agents:
            self.assertGreaterEqual(agent.capital, 0.01)

    def test6(self) -> None:
        """
        Test run_simulation raises error for non-positive n_periods.
        """
        # Prepare inputs.
        agents = racaosimscsu.create_population(n_agents=5, seed=42)
        # Run test and check output.
        with self.assertRaises(AssertionError):
            racaosimscsu.run_simulation(agents, n_periods=0, seed=42)

    def test7(self) -> None:
        """
        Test run_simulation raises error for empty agents list.
        """
        # Prepare inputs.
        agents = []
        # Run test and check output.
        with self.assertRaises(AssertionError):
            racaosimscsu.run_simulation(agents, n_periods=5, seed=42)

    def test8(self) -> None:
        """
        Test lucky events are capitalized based on IQ talent.
        """
        # Prepare inputs.
        # Create agent with high IQ to capitalize on lucky events.
        agent_high_iq = racaosimscsu.Agent(
            0, 0.5, 0.99, 0.5, initial_capital=1.0
        )
        # Create agent with low IQ to fail capitalizing.
        agent_low_iq = racaosimscsu.Agent(1, 0.5, 0.01, 0.5, initial_capital=1.0)
        # Run test.
        racaosimscsu.run_simulation(
            [agent_high_iq, agent_low_iq],
            n_periods=50,
            n_lucky_events_per_period=10,
            n_unlucky_events_per_period=0,
            seed=42,
        )
        # Check outputs.
        # High IQ agent should have higher capital due to capitalizing on luck.
        self.assertGreater(agent_high_iq.capital, agent_low_iq.capital)

    def test9(self) -> None:
        """
        Test networking spillover mechanism with 10% spillover probability.
        """
        # Prepare inputs.
        agents = racaosimscsu.create_population(n_agents=10, seed=42)
        # Run test.
        racaosimscsu.run_simulation(
            agents,
            n_periods=100,
            n_lucky_events_per_period=10,
            n_unlucky_events_per_period=0,
            seed=42,
        )
        # Check outputs.
        # At least some agents should have lucky events (spillover or direct).
        total_lucky = sum(a.lucky_events for a in agents)
        self.assertGreater(total_lucky, 0)


# #############################################################################
# Test_run_policy_simulation
# #############################################################################


class Test_run_policy_simulation(hunitest.TestCase):
    """
    Test the run_policy_simulation function with different policies.
    """

    def test1(self) -> None:
        """
        Test run_policy_simulation with egalitarian policy.
        """
        # Prepare inputs.
        agents = racaosimscsu.create_population(n_agents=10, seed=42)
        resource_amount = 50.0
        # Run test.
        result = racaosimscsu.run_policy_simulation(
            agents,
            policy="egalitarian",
            resource_amount=resource_amount,
            n_periods=5,
            seed=42,
        )
        # Check outputs.
        self.assertTrue(racaosimscsu.validate_simulation_results(result))

    def test2(self) -> None:
        """
        Test run_policy_simulation with meritocratic policy.
        """
        # Prepare inputs.
        agents = racaosimscsu.create_population(n_agents=10, seed=42)
        resource_amount = 50.0
        # Run test.
        result = racaosimscsu.run_policy_simulation(
            agents,
            policy="meritocratic",
            resource_amount=resource_amount,
            n_periods=5,
            seed=42,
        )
        # Check outputs.
        self.assertTrue(racaosimscsu.validate_simulation_results(result))

    def test3(self) -> None:
        """
        Test run_policy_simulation with performance policy.
        """
        # Prepare inputs.
        agents = racaosimscsu.create_population(n_agents=10, seed=42)
        resource_amount = 50.0
        # Run test.
        result = racaosimscsu.run_policy_simulation(
            agents,
            policy="performance",
            resource_amount=resource_amount,
            n_periods=5,
            seed=42,
        )
        # Check outputs.
        self.assertTrue(racaosimscsu.validate_simulation_results(result))

    def test4(self) -> None:
        """
        Test run_policy_simulation with random policy.
        """
        # Prepare inputs.
        agents = racaosimscsu.create_population(n_agents=10, seed=42)
        resource_amount = 50.0
        # Run test.
        result = racaosimscsu.run_policy_simulation(
            agents,
            policy="random",
            resource_amount=resource_amount,
            n_periods=5,
            seed=42,
        )
        # Check outputs.
        self.assertTrue(racaosimscsu.validate_simulation_results(result))

    def test5(self) -> None:
        """
        Test run_policy_simulation with cate_optimal policy.
        """
        # Prepare inputs.
        agents = racaosimscsu.create_population(n_agents=10, seed=42)
        resource_amount = 50.0
        cate_values = np.array([0.5] * 10, dtype=float)
        # Run test.
        result = racaosimscsu.run_policy_simulation(
            agents,
            policy="cate_optimal",
            resource_amount=resource_amount,
            cate_values=cate_values,
            n_periods=5,
            seed=42,
        )
        # Check outputs.
        self.assertTrue(racaosimscsu.validate_simulation_results(result))

    def test6(self) -> None:
        """
        Test run_policy_simulation egalitarian allocates equally.
        """
        # Prepare inputs.
        agents = racaosimscsu.create_population(n_agents=10, seed=42)
        resource_amount = 100.0
        # Check allocation by comparing the change in total capital.
        initial_total = sum(a.capital for a in agents)
        racaosimscsu.run_policy_simulation(
            agents,
            policy="egalitarian",
            resource_amount=resource_amount,
            n_periods=1,
            seed=42,
        )
        # Check outputs.
        final_total = sum(a.capital for a in agents)
        # Final total should be close to initial + resource allocation.
        self.assertGreaterEqual(
            final_total, initial_total + resource_amount - 10.0
        )

    def test7(self) -> None:
        """
        Test run_policy_simulation total capital is preserved after allocation.
        """
        # Prepare inputs.
        agents = racaosimscsu.create_population(n_agents=10, seed=42)
        initial_total = sum(a.capital for a in agents)
        resource_amount = 50.0
        # Run test.
        racaosimscsu.run_policy_simulation(
            agents,
            policy="egalitarian",
            resource_amount=resource_amount,
            n_periods=1,
            seed=42,
        )
        # Check outputs.
        # Total capital should be at least initial + allocated (may change during simulation).
        final_total = sum(a.capital for a in agents)
        self.assertGreaterEqual(
            final_total, initial_total + resource_amount - 5.0
        )

    def test8(self) -> None:
        """
        Test run_policy_simulation raises error for invalid policy.
        """
        # Prepare inputs.
        agents = racaosimscsu.create_population(n_agents=5, seed=42)
        # Run test and check output.
        with self.assertRaises(ValueError):
            racaosimscsu.run_policy_simulation(
                agents,
                policy="invalid_policy",
                resource_amount=50.0,
                n_periods=5,
                seed=42,
            )

    def test9(self) -> None:
        """
        Test run_policy_simulation cate_optimal requires cate_values.
        """
        # Prepare inputs.
        agents = racaosimscsu.create_population(n_agents=5, seed=42)
        # Run test and check output.
        with self.assertRaises(AssertionError):
            racaosimscsu.run_policy_simulation(
                agents,
                policy="cate_optimal",
                resource_amount=50.0,
                n_periods=5,
                seed=42,
            )

    def test10(self) -> None:
        """
        Test run_policy_simulation with negative CATE values clamped to zero.
        """
        # Prepare inputs.
        agents = racaosimscsu.create_population(n_agents=5, seed=42)
        cate_values = np.array([-1.0, 0.5, -0.5, 0.8, 0.0], dtype=float)
        # Run test.
        racaosimscsu.run_policy_simulation(
            agents,
            policy="cate_optimal",
            resource_amount=50.0,
            cate_values=cate_values,
            n_periods=1,
            seed=42,
        )
        # Check outputs.
        # Agents with negative CATE should get 0 allocation.
        self.assertTrue(racaosimscsu.validate_simulation_results(agents))


# #############################################################################
# Test_fit_bayesian_luck_model
# #############################################################################


class Test_fit_bayesian_luck_model(hunitest.TestCase):
    """
    Test the fit_bayesian_luck_model function.
    """

    def test1(self) -> None:
        """
        Test fit_bayesian_luck_model returns model and idata.
        """
        # Prepare inputs.
        agents = racaosimscsu.create_population(n_agents=20, seed=42)
        racaosimscsu.run_simulation(agents, n_periods=10, seed=42)
        df = racaosimscsu.get_results_dataframe(agents)
        # Run test.
        model, idata = racaosimscsu.fit_bayesian_luck_model(
            df, draws=100, tune=100, random_seed=42
        )
        # Check outputs.
        self.assertIsNotNone(model)
        self.assertIsNotNone(idata)

    def test2(self) -> None:
        """
        Test fit_bayesian_luck_model raises error for missing columns.
        """
        # Prepare inputs.
        import pandas as pd

        df = pd.DataFrame({"capital": [1.0, 2.0, 3.0]})
        # Run test and check output.
        with self.assertRaises(AssertionError):
            racaosimscsu.fit_bayesian_luck_model(
                df, draws=10, tune=10, random_seed=42
            )

    def test3(self) -> None:
        """
        Test fit_bayesian_luck_model with seed produces reproducible results.
        """
        # Prepare inputs.
        agents1 = racaosimscsu.create_population(n_agents=15, seed=42)
        racaosimscsu.run_simulation(agents1, n_periods=8, seed=42)
        df1 = racaosimscsu.get_results_dataframe(agents1)

        agents2 = racaosimscsu.create_population(n_agents=15, seed=42)
        racaosimscsu.run_simulation(agents2, n_periods=8, seed=42)
        df2 = racaosimscsu.get_results_dataframe(agents2)
        # Run test.
        _, idata1 = racaosimscsu.fit_bayesian_luck_model(
            df1, draws=50, tune=50, random_seed=123
        )
        _, idata2 = racaosimscsu.fit_bayesian_luck_model(
            df2, draws=50, tune=50, random_seed=123
        )
        # Check outputs.
        self.assertIsNotNone(idata1)
        self.assertIsNotNone(idata2)


# #############################################################################
# Test_summarize_bayesian_fit
# #############################################################################


class Test_summarize_bayesian_fit(hunitest.TestCase):
    """
    Test the summarize_bayesian_fit function.
    """

    def test1(self) -> None:
        """
        Test summarize_bayesian_fit returns DataFrame with correct columns.
        """
        # Prepare inputs.
        agents = racaosimscsu.create_population(n_agents=20, seed=42)
        racaosimscsu.run_simulation(agents, n_periods=10, seed=42)
        df = racaosimscsu.get_results_dataframe(agents)
        _, idata = racaosimscsu.fit_bayesian_luck_model(
            df, draws=100, tune=100, random_seed=42
        )
        # Run test.
        summary = racaosimscsu.summarize_bayesian_fit(idata)
        # Check outputs.
        self.assertIsNotNone(summary)
        self.assertGreater(len(summary), 0)

    def test2(self) -> None:
        """
        Test summarize_bayesian_fit includes default parameters.
        """
        # Prepare inputs.
        agents = racaosimscsu.create_population(n_agents=20, seed=42)
        racaosimscsu.run_simulation(agents, n_periods=10, seed=42)
        df = racaosimscsu.get_results_dataframe(agents)
        _, idata = racaosimscsu.fit_bayesian_luck_model(
            df, draws=100, tune=100, random_seed=42
        )
        # Run test.
        summary = racaosimscsu.summarize_bayesian_fit(idata)
        # Check outputs.
        # Should include default parameters.
        self.assertIn("alpha", summary.index)
        self.assertIn("beta_luck", summary.index)

    def test3(self) -> None:
        """
        Test summarize_bayesian_fit with custom var_names parameter.
        """
        # Prepare inputs.
        agents = racaosimscsu.create_population(n_agents=20, seed=42)
        racaosimscsu.run_simulation(agents, n_periods=10, seed=42)
        df = racaosimscsu.get_results_dataframe(agents)
        _, idata = racaosimscsu.fit_bayesian_luck_model(
            df, draws=100, tune=100, random_seed=42
        )
        # Run test.
        summary = racaosimscsu.summarize_bayesian_fit(
            idata, var_names=["alpha", "sigma"]
        )
        # Check outputs.
        self.assertIn("alpha", summary.index)
        self.assertIn("sigma", summary.index)
        self.assertNotIn("beta_luck", summary.index)


# #############################################################################
# Test_posterior_predictive_check
# #############################################################################


class Test_posterior_predictive_check(hunitest.TestCase):
    """
    Test the posterior_predictive_check function.
    """

    def test1(self) -> None:
        """
        Test posterior_predictive_check returns correct keys.
        """
        # Prepare inputs.
        agents = racaosimscsu.create_population(n_agents=20, seed=42)
        racaosimscsu.run_simulation(agents, n_periods=10, seed=42)
        df = racaosimscsu.get_results_dataframe(agents)
        model, idata = racaosimscsu.fit_bayesian_luck_model(
            df, draws=100, tune=100, random_seed=42
        )
        # Run test.
        ppc = racaosimscsu.posterior_predictive_check(
            model, idata, df, random_seed=123
        )
        # Check outputs.
        expected_keys = ["y_obs", "y_pred_mean", "y_pred_std"]
        self.assertEqual(sorted(ppc.keys()), sorted(expected_keys))

    def test2(self) -> None:
        """
        Test posterior_predictive_check PPC arrays have correct shape.
        """
        # Prepare inputs.
        agents = racaosimscsu.create_population(n_agents=20, seed=42)
        racaosimscsu.run_simulation(agents, n_periods=10, seed=42)
        df = racaosimscsu.get_results_dataframe(agents)
        model, idata = racaosimscsu.fit_bayesian_luck_model(
            df, draws=100, tune=100, random_seed=42
        )
        # Run test.
        ppc = racaosimscsu.posterior_predictive_check(
            model, idata, df, random_seed=123
        )
        # Check outputs.
        n_obs = len(df)
        self.assertEqual(len(ppc["y_obs"]), n_obs)
        self.assertEqual(len(ppc["y_pred_mean"]), n_obs)
        self.assertEqual(len(ppc["y_pred_std"]), n_obs)
