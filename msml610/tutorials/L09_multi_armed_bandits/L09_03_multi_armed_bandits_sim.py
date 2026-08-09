"""
Simulation classes for Multi-Armed Bandits lesson.

Import as:

import msml610.tutorials.L09_multi_armed_bandits.L09_03_multi_armed_bandits_sim as mtlmabl0mabs
"""

import abc
from typing import List, Optional, Tuple

import matplotlib.pyplot as plt
import numpy as np

import helpers.hdbg as hdbg


# #############################################################################
# MultiArmedBandit
# #############################################################################


class MultiArmedBandit:
    """
    Multi-armed bandit environment with K machines.

    Each machine has an unknown probability distribution with mean mu_i.
    Rewards are drawn from a uniform distribution in [mu_i - width, mu_i +
    width], clipped to [-1, 1].
    """

    def __init__(
        self,
        *,
        k_machines: int,
        mu_values: List[float],
        seed: int,
        width: float = 0.3,
    ) -> None:
        """
        Initialize multi-armed bandit.

        :param k_machines: number of machines (K)
        :param mu_values: true mean values for each machine
        :param seed: random seed for reproducibility
        :param width: half-width of uniform distribution around mean
        """
        hdbg.dassert_eq(
            len(mu_values),
            k_machines,
            "Number of mu values must equal k_machines:",
            len(mu_values),
            k_machines,
        )
        hdbg.dassert_lte(1, k_machines, "Must have at least 1 machine")
        hdbg.dassert_lt(0.0, width, "Width must be positive")
        self.k_machines = k_machines
        self.mu_values = list(mu_values)
        self.width = width
        self.seed = seed
        # Initialize random state.
        self._rng = np.random.RandomState(seed)
        # Track statistics per machine.
        self.machine_pulls = [0] * k_machines
        self.machine_rewards = [[] for _ in range(k_machines)]

    def pull(self, machine_idx: int) -> float:
        """
        Pull a specific machine and get reward.

        :param machine_idx: index of machine to pull (0 to K-1)
        :return: reward value in [-1, 1]
        """
        hdbg.dassert_lte(
            0,
            machine_idx,
            "Machine index must be non-negative:",
            machine_idx,
        )
        hdbg.dassert_lt(
            machine_idx,
            self.k_machines,
            "Machine index out of range:",
            machine_idx,
        )
        # Generate reward from uniform distribution.
        true_mean = self.mu_values[machine_idx]
        reward = np.clip(
            self._rng.uniform(true_mean - self.width, true_mean + self.width),
            -1.0,
            1.0,
        )
        # Update statistics.
        self.machine_pulls[machine_idx] += 1
        self.machine_rewards[machine_idx].append(reward)
        return reward

    def get_empirical_means(self) -> List[float]:
        """
        Get empirical mean reward for each machine.

        :return: list of empirical means (or 0.0 if machine not pulled)
        """
        means = []
        for rewards in self.machine_rewards:
            if len(rewards) > 0:
                means.append(np.mean(rewards))
            else:
                means.append(0.0)
        return means

    def reset(self, seed: Optional[int] = None) -> None:
        """
        Reset all statistics but keep mu values.

        :param seed: optional new seed; if None, use original seed
        """
        if seed is not None:
            self.seed = seed
        self.machine_pulls = [0] * self.k_machines
        self.machine_rewards = [[] for _ in range(self.k_machines)]
        # Reset random state.
        self._rng = np.random.RandomState(self.seed)


# #############################################################################
# Strategy
# #############################################################################


class Strategy(abc.ABC):
    """
    Abstract base class for bandit selection strategies.
    """

    @abc.abstractmethod
    def select_machine(
        self,
        bandit: MultiArmedBandit,
    ) -> int:
        """
        Select which machine to pull next.

        :param bandit: MultiArmedBandit instance with current state
        :return: index of machine to pull (0 to K-1)
        """
        pass

    def reset(self) -> None:
        """
        Reset any internal state of the strategy.
        """
        pass


# #############################################################################
# ExplorationStrategy
# #############################################################################


class ExplorationStrategy(Strategy):
    """
    Pure exploration strategy: randomly select machines.
    """

    def __init__(self, *, seed: int) -> None:
        """
        Initialize exploration strategy.

        :param seed: random seed for machine selection
        """
        self.seed = seed
        self._rng = np.random.RandomState(seed)

    def select_machine(
        self,
        bandit: MultiArmedBandit,
    ) -> int:
        """
        Randomly select a machine with equal probability.

        :param bandit: MultiArmedBandit instance
        :return: randomly selected machine index
        """
        return self._rng.randint(0, bandit.k_machines)

    def reset(self) -> None:
        """
        Reset random state.
        """
        self._rng = np.random.RandomState(self.seed)


# #############################################################################
# ExploitationStrategy
# #############################################################################


class ExploitationStrategy(Strategy):
    """
    Pure exploitation strategy: always select best known machine.

    Start with one pull of each machine for initialization.
    """

    def __init__(self) -> None:
        """
        Initialize exploitation strategy.
        """
        self.initialized = False

    def select_machine(
        self,
        bandit: MultiArmedBandit,
    ) -> int:
        """
        Select machine with highest empirical mean.

        Initially pulls each machine once for initialization.

        :param bandit: MultiArmedBandit instance
        :return: machine index with highest empirical mean
        """
        # Initialize by pulling each machine once.
        if not self.initialized:
            for machine_idx in range(bandit.k_machines):
                if bandit.machine_pulls[machine_idx] == 0:
                    return machine_idx
            self.initialized = True
        # Select machine with highest empirical mean.
        empirical_means = bandit.get_empirical_means()
        return int(np.argmax(empirical_means))

    def reset(self) -> None:
        """
        Reset initialization state.
        """
        self.initialized = False


# #############################################################################
# EpsilonGreedyStrategy
# #############################################################################


class EpsilonGreedyStrategy(Strategy):
    """
    Epsilon-greedy strategy: explore with probability epsilon.

    Balances exploration and exploitation.
    """

    def __init__(self, *, epsilon: float, seed: int) -> None:
        """
        Initialize epsilon-greedy strategy.

        :param epsilon: exploration probability (0 to 1)
        :param seed: random seed for exploration decisions
        """
        hdbg.dassert_lte(
            0.0,
            epsilon,
            "Epsilon must be non-negative:",
            epsilon,
        )
        hdbg.dassert_lte(
            epsilon,
            1.0,
            "Epsilon must be at most 1.0:",
            epsilon,
        )
        self.epsilon = epsilon
        self.seed = seed
        self._rng = np.random.RandomState(seed)
        self.initialized = False

    def select_machine(
        self,
        bandit: MultiArmedBandit,
    ) -> int:
        """
        Select machine using epsilon-greedy policy.

        With probability epsilon, explore (random selection).
        With probability 1-epsilon, exploit (best known machine).

        :param bandit: MultiArmedBandit instance
        :return: selected machine index
        """
        # Initialize by pulling each machine once.
        if not self.initialized:
            for machine_idx in range(bandit.k_machines):
                if bandit.machine_pulls[machine_idx] == 0:
                    return machine_idx
            self.initialized = True
        # Epsilon-greedy selection.
        if self._rng.random() < self.epsilon:
            # Explore.
            return self._rng.randint(0, bandit.k_machines)
        else:
            # Exploit.
            empirical_means = bandit.get_empirical_means()
            return int(np.argmax(empirical_means))

    def reset(self) -> None:
        """
        Reset random state and initialization.
        """
        self._rng = np.random.RandomState(self.seed)
        self.initialized = False


# #############################################################################
# BanditExperiment
# #############################################################################


class BanditExperiment:
    """
    Run a single experiment with a bandit and strategy.
    """

    def __init__(
        self,
        *,
        bandit: MultiArmedBandit,
        strategy: Strategy,
        n_coins: int,
    ) -> None:
        """
        Initialize experiment.

        :param bandit: MultiArmedBandit instance
        :param strategy: Strategy instance
        :param n_coins: number of coins to play (N)
        """
        hdbg.dassert_lte(1, n_coins, "Must play at least 1 coin")
        self.bandit = bandit
        self.strategy = strategy
        self.n_coins = n_coins

    def run(self) -> Tuple[List[float], List[float], float]:
        """
        Run the experiment for n_coins trials.

        :return: tuple of (rewards, cumulative_rewards, final_total)
        """
        # Reset bandit and strategy state.
        self.bandit.reset()
        self.strategy.reset()
        rewards = []
        cumulative_rewards = []
        cumulative = 0.0
        # Run trials.
        for _ in range(self.n_coins):
            # Strategy selects machine.
            machine_idx = self.strategy.select_machine(self.bandit)
            # Pull machine and get reward.
            reward = self.bandit.pull(machine_idx)
            # Track results.
            rewards.append(reward)
            cumulative += reward
            cumulative_rewards.append(cumulative)
        return rewards, cumulative_rewards, cumulative


# #############################################################################
# BanditSimulation
# #############################################################################


class BanditSimulation:
    """
    Run multiple experiments for statistical analysis.
    """

    def __init__(
        self,
        *,
        k_machines: int,
        mu_values: List[float],
        n_coins: int,
        base_seed: int = 0,
    ) -> None:
        """
        Initialize simulation parameters.

        :param k_machines: number of machines (K)
        :param mu_values: true mean values for each machine
        :param n_coins: number of coins per experiment (N)
        :param base_seed: base seed for reproducibility
        """
        self.k_machines = k_machines
        self.mu_values = mu_values
        self.n_coins = n_coins
        self.base_seed = base_seed

    def run_trials(
        self,
        *,
        strategy_class: type,
        strategy_params: dict,
        n_trials: int,
    ) -> dict:
        """
        Run n_trials experiments with the same setup, varying seed.

        :param strategy_class: Strategy class to instantiate
        :param strategy_params: parameters to pass to strategy
        :param n_trials: number of trials to run
        :return: dictionary with statistics and results
        """
        hdbg.dassert_lte(1, n_trials, "Must run at least 1 trial")
        final_totals = []
        all_cumulative_rewards = []
        # Run trials with different seeds.
        for trial_idx in range(n_trials):
            # Create bandit with unique seed.
            bandit_seed = self.base_seed + trial_idx
            bandit = MultiArmedBandit(
                k_machines=self.k_machines,
                mu_values=self.mu_values,
                seed=bandit_seed,
            )
            # Create strategy with unique seed if needed.
            if "seed" in strategy_params:
                strategy_params_trial = strategy_params.copy()
                strategy_params_trial["seed"] = bandit_seed + 1000
                strategy = strategy_class(**strategy_params_trial)
            else:
                strategy = strategy_class(**strategy_params)
            # Run experiment.
            experiment = BanditExperiment(
                bandit=bandit,
                strategy=strategy,
                n_coins=self.n_coins,
            )
            _, cumulative_rewards, final_total = experiment.run()
            final_totals.append(final_total)
            all_cumulative_rewards.append(cumulative_rewards)
        # Compute statistics.
        final_totals_array = np.array(final_totals)
        all_cumulative_array = np.array(all_cumulative_rewards)
        return {
            "final_totals": final_totals,
            "mean_final": np.mean(final_totals_array),
            "std_final": np.std(final_totals_array),
            "all_cumulative_rewards": all_cumulative_rewards,
            "mean_cumulative": np.mean(all_cumulative_array, axis=0),
            "std_cumulative": np.std(all_cumulative_array, axis=0),
        }

    def epsilon_sweep(
        self,
        *,
        n_trials: int,
        epsilon_values: List[float] = None,
    ) -> dict:
        """
        Run simulations for multiple epsilon values.

        Compare exploration, exploitation, and balanced strategies.

        :param n_trials: number of trials per epsilon value
        :param epsilon_values: list of epsilon values to test
        :return: dictionary with results for each epsilon
        """
        if epsilon_values is None:
            epsilon_values = np.arange(0.0, 1.1, 0.1).tolist()
        results = {
            "epsilon_values": epsilon_values,
            "exploration": None,
            "exploitation": None,
            "balanced": [],
        }
        # Run pure exploration.
        exploration_results = self.run_trials(
            strategy_class=ExplorationStrategy,
            strategy_params={"seed": self.base_seed},
            n_trials=n_trials,
        )
        results["exploration"] = exploration_results
        # Run pure exploitation.
        exploitation_results = self.run_trials(
            strategy_class=ExploitationStrategy,
            strategy_params={},
            n_trials=n_trials,
        )
        results["exploitation"] = exploitation_results
        # Run balanced for each epsilon.
        for epsilon in epsilon_values:
            balanced_results = self.run_trials(
                strategy_class=EpsilonGreedyStrategy,
                strategy_params={"epsilon": epsilon, "seed": self.base_seed},
                n_trials=n_trials,
            )
            results["balanced"].append(balanced_results)
        return results


# #############################################################################
# BanditEnsemble
# #############################################################################


class BanditEnsemble:
    """
    Average results over multiple random mu_i configurations.
    """

    def __init__(
        self,
        *,
        k_machines: int,
        n_coins: int,
        mu_range: Tuple[float, float] = (-0.5, 0.5),
        base_seed: int = 0,
    ) -> None:
        """
        Initialize ensemble parameters.

        :param k_machines: number of machines (K)
        :param n_coins: number of coins per experiment (N)
        :param mu_range: range for random mu values (min, max)
        :param base_seed: base seed for reproducibility
        """
        self.k_machines = k_machines
        self.n_coins = n_coins
        self.mu_range = mu_range
        self.base_seed = base_seed

    def run_ensemble(
        self,
        *,
        strategy_class: type,
        strategy_params: dict,
        n_trials: int,
        n_mu_configs: int,
    ) -> dict:
        """
        Run trials across multiple random mu configurations.

        :param strategy_class: Strategy class to instantiate
        :param strategy_params: parameters to pass to strategy
        :param n_trials: number of trials per mu configuration
        :param n_mu_configs: number of random mu configurations
        :return: dictionary with aggregated statistics
        """
        hdbg.dassert_lte(1, n_trials, "Must run at least 1 trial")
        hdbg.dassert_lte(1, n_mu_configs, "Must run at least 1 mu config")
        all_mean_finals = []
        all_std_finals = []
        # Generate random mu configurations.
        mu_rng = np.random.RandomState(self.base_seed)
        for mu_config_idx in range(n_mu_configs):
            # Generate random mu values.
            mu_values = mu_rng.uniform(
                self.mu_range[0],
                self.mu_range[1],
                self.k_machines,
            ).tolist()
            # Run simulation for this mu configuration.
            simulation = BanditSimulation(
                k_machines=self.k_machines,
                mu_values=mu_values,
                n_coins=self.n_coins,
                base_seed=self.base_seed + mu_config_idx * 10000,
            )
            results = simulation.run_trials(
                strategy_class=strategy_class,
                strategy_params=strategy_params,
                n_trials=n_trials,
            )
            all_mean_finals.append(results["mean_final"])
            all_std_finals.append(results["std_final"])
        # Aggregate statistics across mu configurations.
        all_mean_finals_array = np.array(all_mean_finals)
        return {
            "mean_finals_per_config": all_mean_finals,
            "overall_mean": np.mean(all_mean_finals_array),
            "overall_std": np.std(all_mean_finals_array),
            "std_finals_per_config": all_std_finals,
        }

    def compare_strategies_ensemble(
        self,
        *,
        n_trials: int,
        n_mu_configs: int,
        epsilon: float = 0.1,
    ) -> dict:
        """
        Compare strategies averaged over random mu configurations.

        :param n_trials: number of trials per mu configuration
        :param n_mu_configs: number of random mu configurations
        :param epsilon: epsilon value for balanced strategy
        :return: dictionary with results for each strategy
        """
        results = {}
        # Run exploration.
        results["exploration"] = self.run_ensemble(
            strategy_class=ExplorationStrategy,
            strategy_params={"seed": self.base_seed},
            n_trials=n_trials,
            n_mu_configs=n_mu_configs,
        )
        # Run exploitation.
        results["exploitation"] = self.run_ensemble(
            strategy_class=ExploitationStrategy,
            strategy_params={},
            n_trials=n_trials,
            n_mu_configs=n_mu_configs,
        )
        # Run balanced.
        results["balanced"] = self.run_ensemble(
            strategy_class=EpsilonGreedyStrategy,
            strategy_params={"epsilon": epsilon, "seed": self.base_seed},
            n_trials=n_trials,
            n_mu_configs=n_mu_configs,
        )
        return results

    def plot_ensemble_comparison(
        self,
        *,
        ensemble_results: dict,
        epsilon: float = 0.1,
    ) -> None:
        """
        Plot comparison of strategies across random mu configurations.

        :param ensemble_results: results from compare_strategies_ensemble()
        :param epsilon: epsilon value used for balanced strategy
        """
        strategies = ["exploration", "exploitation", "balanced"]
        labels = [
            "Pure Exploration",
            "Pure Exploitation",
            f"Balanced (epsilon={epsilon:.1f})",
        ]
        colors = ["blue", "red", "green"]
        means = [ensemble_results[s]["overall_mean"] for s in strategies]
        stds = [ensemble_results[s]["overall_std"] for s in strategies]
        # Create bar plot.
        fig, ax = plt.subplots(figsize=(10, 6))
        x_pos = np.arange(len(strategies))
        bars = ax.bar(
            x_pos, means, yerr=stds, capsize=10, color=colors, alpha=0.7
        )
        ax.set_xlabel("Strategy", fontsize=12)
        ax.set_ylabel(
            "Mean Final Reward (averaged over mu configs)", fontsize=12
        )
        ax.set_title(
            "Strategy Comparison Across Random Mu Configurations",
            fontsize=14,
            weight="bold",
        )
        ax.set_xticks(x_pos)
        ax.set_xticklabels(labels)
        ax.grid(True, alpha=0.3, axis="y")
        # Add value labels on bars.
        for bar, mean, std in zip(bars, means, stds):
            height = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width() / 2.0,
                height,
                f"{mean:.2f}\n±{std:.2f}",
                ha="center",
                va="bottom",
                fontsize=10,
                weight="bold",
            )
        plt.tight_layout()
        plt.show()
