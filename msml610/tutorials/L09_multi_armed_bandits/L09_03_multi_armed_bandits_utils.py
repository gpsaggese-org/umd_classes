"""
Utility functions for Multi-Armed Bandits lesson.

Import as:

import msml610.tutorials.L09_multi_armed_bandits.L09_03_multi_armed_bandits_utils as mtlmabl0mabu
"""

import logging
from typing import List, Tuple

import ipywidgets
import matplotlib.pyplot as plt
import numpy as np
from IPython.display import clear_output, display

import helpers.htutorial as htutori
import L09_03_multi_armed_bandits_sim as sim

_LOG = logging.getLogger(__name__)


# #############################################################################
# Cell 1: Introduction: Casino Slot Machines
# #############################################################################


def cell1_casino_slot_machines() -> None:
    """
    Interactive casino slot machine visualization.

    Display 3 slot machines with fixed true means generating random rewards.
    User can:
    - Click a machine directly to play it.
    - Toggle showing true means.
    - Reset total winnings and coin budget.
    """
    # Initialize state.
    true_means = [-0.2, 0.0, 0.5]
    state = {
        "total_winnings": 0.0,
        "coins_remaining": 10,
        "initial_coins": 10,
        "machine_last_rewards": [None, None, None],
        "bandit": None,
        "show_true_means": False,
    }
    # Create seed widget.
    seed_slider, seed_box = htutori.build_widget_control(
        name="seed",
        description="random seed",
        min_val=0,
        max_val=100,
        step=1,
        initial_value=42,
        is_float=False,
    )
    # Create coins widget.
    coins_slider, coins_box = htutori.build_widget_control(
        name="coins",
        description="number of coins",
        min_val=5,
        max_val=50,
        step=1,
        initial_value=10,
        is_float=False,
    )
    # Create widgets for showing true means.
    show_means_toggle = ipywidgets.Checkbox(
        value=False,
        description="Show True Means",
        style={"description_width": "120px"},
    )
    # Create one button per machine so the user clicks the machine directly
    # to play it, instead of picking it from a selector.
    machine_buttons = [
        ipywidgets.Button(
            description=f"Play Machine {i + 1}",
            button_style="success",
            layout={"width": "150px"},
        )
        for i in range(3)
    ]
    reset_button = ipywidgets.Button(
        description="Reset Game",
        button_style="warning",
        layout={"width": "200px"},
    )
    # Output widget for plots.
    output = ipywidgets.Output()

    def update_plot() -> None:
        """
        Update the visualization.
        """
        with output:
            clear_output(wait=True)
            # Create figure with subplots.
            fig, axes = plt.subplots(1, 3, figsize=(12, 4))
            # Plot slot machines.
            for i in range(3):
                ax = axes[i]
                ax.set_xlim(0, 1)
                ax.set_ylim(0, 1)
                ax.axis("off")
                # Draw slot machine frame.
                machine_rect = plt.Rectangle(
                    (0.1, 0.2),
                    0.8,
                    0.6,
                    linewidth=3,
                    edgecolor="black",
                    facecolor="lightgray",
                )
                ax.add_patch(machine_rect)
                # Display a fixed placeholder (the machine face never reveals
                # the reward value; the reward is printed below the machine
                # instead).
                ax.text(
                    0.5,
                    0.5,
                    "?",
                    ha="center",
                    va="center",
                    fontsize=32,
                    weight="bold",
                )
                # Machine label.
                ax.text(
                    0.5,
                    0.9,
                    f"Machine {i + 1}",
                    ha="center",
                    va="center",
                    fontsize=14,
                    weight="bold",
                )
                # Display the last reward obtained from this machine, below
                # the machine (not inside it).
                last_reward = state["machine_last_rewards"][i]
                if last_reward is None:
                    reward_text = "Last reward: ?"
                else:
                    reward_text = f"Last reward: {last_reward:.2f}"
                ax.text(
                    0.5,
                    0.13,
                    reward_text,
                    ha="center",
                    va="center",
                    fontsize=11,
                    color="darkgreen",
                    weight="bold",
                )
                # Calculate and display sample mean and number of pulls.
                if state["bandit"] is not None:
                    rewards = state["bandit"].machine_rewards[i]
                    num_pulls = state["bandit"].machine_pulls[i]
                    if num_pulls > 0:
                        sample_mean = np.mean(rewards)
                        stats_text = f"n={num_pulls}, mean={sample_mean:.2f}"
                    else:
                        stats_text = "n=0, mean=?"
                else:
                    stats_text = "n=0, mean=?"
                ax.text(
                    0.5,
                    0.03,
                    stats_text,
                    ha="center",
                    va="bottom",
                    fontsize=10,
                    color="blue",
                    weight="bold",
                )
                # Show true mean if enabled.
                if state["show_true_means"]:
                    ax.text(
                        0.5,
                        -0.08,
                        f"true mu={true_means[i]:.2f}",
                        ha="center",
                        va="top",
                        fontsize=9,
                        color="red",
                        weight="bold",
                    )
            # Add game status as title.
            fig.suptitle(
                f"Total Winnings: {state['total_winnings']:.2f} | "
                f"Coins Remaining: {state['coins_remaining']}",
                fontsize=16,
                weight="bold",
            )
            plt.tight_layout()
            plt.show()

    def make_on_play_clicked(machine_idx: int):
        """
        Build a click handler that plays a specific machine.

        :param machine_idx: index of the machine this button plays (0 to 2)
        :return: click handler for `machine_buttons[machine_idx]`
        """

        def on_play_clicked(b: ipywidgets.Button) -> None:
            """
            Handle a click on one machine's play button.

            :param b: button widget (unused)
            """
            if state["coins_remaining"] <= 0:
                _LOG.warning("No coins remaining!")
                return
            # Initialize bandit if needed.
            if state["bandit"] is None:
                state["bandit"] = sim.MultiArmedBandit(
                    k_machines=3,
                    mu_values=true_means,
                    seed=seed_slider.value,
                    width=0.3,
                )
            # Pull the machine.
            reward = state["bandit"].pull(machine_idx)
            # Update state.
            state["total_winnings"] += reward
            state["coins_remaining"] -= 1
            state["machine_last_rewards"][machine_idx] = reward
            # Increment seed for next play.
            seed_slider.value = seed_slider.value + 1
            # Update plot.
            update_plot()

        return on_play_clicked

    def on_reset_clicked(b: ipywidgets.Button) -> None:
        """
        Handle reset button click.

        :param b: button widget (unused)
        """
        state["total_winnings"] = 0.0
        state["initial_coins"] = coins_slider.value
        state["coins_remaining"] = coins_slider.value
        state["machine_last_rewards"] = [None, None, None]
        # Reset bandit with current seed.
        state["bandit"] = sim.MultiArmedBandit(
            k_machines=3,
            mu_values=true_means,
            seed=seed_slider.value,
            width=0.3,
        )
        update_plot()

    def on_show_means_changed(change: dict) -> None:
        """
        Handle toggle for showing true means.

        :param change: dictionary with change information
        """
        state["show_true_means"] = change["new"]
        update_plot()

    # Connect callbacks.
    for machine_idx, button in enumerate(machine_buttons):
        button.on_click(make_on_play_clicked(machine_idx))
    reset_button.on_click(on_reset_clicked)
    show_means_toggle.observe(on_show_means_changed, names="value")
    # Layout widgets.
    controls = ipywidgets.VBox(
        [
            seed_box,
            coins_box,
            show_means_toggle,
            ipywidgets.HBox(machine_buttons + [reset_button]),
        ]
    )
    # Display widgets and initial plot.
    display(controls, output)
    update_plot()


def plot_epsilon_sweep(
    *,
    sweep_results: dict,
    n_coins: int,
) -> None:
    """
    Plot comparison of strategies across epsilon values.

    :param sweep_results: results from BanditSimulation.epsilon_sweep()
    :param n_coins: number of coins used in simulation
    """
    epsilon_values = sweep_results["epsilon_values"]
    exploration = sweep_results["exploration"]
    exploitation = sweep_results["exploitation"]
    balanced_list = sweep_results["balanced"]
    # Create figure with 2 subplots.
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    # Plot 1: Mean final reward vs epsilon.
    ax = axes[0]
    balanced_means = [b["mean_final"] for b in balanced_list]
    balanced_stds = [b["std_final"] for b in balanced_list]
    ax.errorbar(
        epsilon_values,
        balanced_means,
        yerr=balanced_stds,
        label="Epsilon-Greedy",
        marker="o",
        linewidth=2,
        capsize=5,
    )
    ax.axhline(
        exploration["mean_final"],
        color="blue",
        linestyle="--",
        linewidth=2,
        label=f"Pure Exploration (mean={exploration['mean_final']:.2f})",
    )
    ax.axhline(
        exploitation["mean_final"],
        color="red",
        linestyle="--",
        linewidth=2,
        label=f"Pure Exploitation (mean={exploitation['mean_final']:.2f})",
    )
    ax.set_xlabel("Epsilon", fontsize=12)
    ax.set_ylabel("Mean Final Reward", fontsize=12)
    ax.set_title("Strategy Performance vs Epsilon", fontsize=14, weight="bold")
    ax.grid(True, alpha=0.3)
    ax.legend(loc="best", fontsize=10)
    # Plot 2: Cumulative reward over time for best epsilon.
    ax = axes[1]
    best_idx = np.argmax(balanced_means)
    best_epsilon = epsilon_values[best_idx]
    best_balanced = balanced_list[best_idx]
    # Plot mean with error bands.
    trials = np.arange(1, n_coins + 1)
    ax.plot(
        trials,
        exploration["mean_cumulative"],
        label="Pure Exploration",
        color="blue",
        linewidth=2,
        alpha=0.8,
    )
    ax.fill_between(
        trials,
        exploration["mean_cumulative"] - exploration["std_cumulative"],
        exploration["mean_cumulative"] + exploration["std_cumulative"],
        color="blue",
        alpha=0.2,
    )
    ax.plot(
        trials,
        exploitation["mean_cumulative"],
        label="Pure Exploitation",
        color="red",
        linewidth=2,
        alpha=0.8,
    )
    ax.fill_between(
        trials,
        exploitation["mean_cumulative"] - exploitation["std_cumulative"],
        exploitation["mean_cumulative"] + exploitation["std_cumulative"],
        color="red",
        alpha=0.2,
    )
    ax.plot(
        trials,
        best_balanced["mean_cumulative"],
        label=f"Balanced (epsilon={best_epsilon:.1f})",
        color="green",
        linewidth=2,
        alpha=0.8,
    )
    ax.fill_between(
        trials,
        best_balanced["mean_cumulative"] - best_balanced["std_cumulative"],
        best_balanced["mean_cumulative"] + best_balanced["std_cumulative"],
        color="green",
        alpha=0.2,
    )
    ax.set_xlabel("Trial", fontsize=12)
    ax.set_ylabel("Mean Cumulative Reward", fontsize=12)
    ax.set_title(
        "Best Strategy Performance Over Time", fontsize=14, weight="bold"
    )
    ax.grid(True, alpha=0.3)
    ax.legend(loc="upper left", fontsize=10)
    plt.tight_layout()
    plt.show()


# #############################################################################
# Cell 2: Exploration vs Exploitation Dilemma
# #############################################################################


def cell2_exploration_vs_exploitation() -> None:
    """
    Demonstrate exploration vs exploitation tradeoff with three strategies.

    Visualize three strategies:
    - Pure exploration: randomly select machines.
    - Pure exploitation: always select best known machine.
    - Balanced (epsilon-greedy): explore with probability epsilon.

    Show cumulative rewards over multiple trials to compare performance.
    """
    # Initialize state.
    true_means = [-0.2, 0.0, 0.5]
    state = {
        "num_machines": 3,
        "num_trials": 100,
    }

    # Create seed widget.
    seed_slider, seed_box = htutori.build_widget_control(
        name="seed",
        description="random seed",
        min_val=0,
        max_val=100,
        step=1,
        initial_value=42,
        is_float=False,
    )

    # Create coins widget.
    coins_slider, coins_box = htutori.build_widget_control(
        name="coins",
        description="number of coins",
        min_val=10,
        max_val=200,
        step=10,
        initial_value=100,
        is_float=False,
    )

    # Create epsilon slider.
    epsilon_slider, epsilon_box = htutori.build_widget_control(
        name="epsilon",
        description="exploration probability",
        min_val=0.0,
        max_val=1.0,
        step=0.05,
        initial_value=0.1,
        is_float=True,
    )

    # Output widget for plots.
    output = ipywidgets.Output()

    def run_strategy_experiment(
        num_coins: int,
        seed: int,
        strategy: sim.Strategy,
    ) -> Tuple[List[float], List[float]]:
        """
        Run experiment with given strategy.

        :param num_coins: number of coins to play
        :param seed: random seed
        :param strategy: Strategy instance to use
        :return: (rewards, cumulative_rewards)
        """
        bandit = sim.MultiArmedBandit(
            k_machines=state["num_machines"],
            mu_values=true_means,
            seed=seed,
            width=0.3,
        )
        experiment = sim.BanditExperiment(
            bandit=bandit,
            strategy=strategy,
            n_coins=num_coins,
        )
        rewards, cumulative_rewards, _ = experiment.run()
        return rewards, cumulative_rewards

    def update_plot() -> None:
        """
        Update the visualization showing all three strategies.
        """
        with output:
            clear_output(wait=True)

            # Run all three strategies.
            seed = seed_slider.value
            num_coins = coins_slider.value
            epsilon = epsilon_slider.value

            # Create strategies.
            exploration_strategy = sim.ExplorationStrategy(seed=seed)
            exploitation_strategy = sim.ExploitationStrategy()
            balanced_strategy = sim.EpsilonGreedyStrategy(
                epsilon=epsilon,
                seed=seed + 2,
            )

            # Run experiments.
            _, exploration_cumulative = run_strategy_experiment(
                num_coins, seed, exploration_strategy
            )
            _, exploitation_cumulative = run_strategy_experiment(
                num_coins, seed + 1, exploitation_strategy
            )
            _, balanced_cumulative = run_strategy_experiment(
                num_coins, seed + 2, balanced_strategy
            )

            # Create figure with 2 subplots.
            fig, axes = plt.subplots(1, 2, figsize=(14, 5))

            # Plot 1: All three strategies on same plot.
            ax = axes[0]
            ax.plot(
                range(1, num_coins + 1),
                exploration_cumulative,
                label="Pure Exploration (Random)",
                color="blue",
                linewidth=2,
                alpha=0.8,
            )
            ax.plot(
                range(1, num_coins + 1),
                exploitation_cumulative,
                label="Pure Exploitation (Greedy)",
                color="red",
                linewidth=2,
                alpha=0.8,
            )
            ax.plot(
                range(1, num_coins + 1),
                balanced_cumulative,
                label=f"Balanced (epsilon={epsilon:.2f})",
                color="green",
                linewidth=2,
                alpha=0.8,
            )
            ax.set_xlabel("Trial", fontsize=12)
            ax.set_ylabel("Cumulative Reward", fontsize=12)
            ax.set_title(
                "Exploration vs Exploitation Strategies",
                fontsize=14,
                weight="bold",
            )
            ax.set_ylim(0, num_coins)
            ax.grid(True, alpha=0.3)
            ax.legend(loc="upper left", fontsize=10)

            # Plot 2: Comments box comparing all strategies.
            ax = axes[1]
            ax.axis("off")

            # Calculate final rewards.
            final_exploration = exploration_cumulative[-1]
            final_exploitation = exploitation_cumulative[-1]
            final_balanced = balanced_cumulative[-1]

            # Create comparison text.
            comment_lines = [
                "Strategy Comparison",
                "=" * 35,
                "",
                f"Pure Exploration: {final_exploration:.2f}",
                "- Tries all machines randomly",
                "- Learns but earns little",
                "",
                f"Pure Exploitation: {final_exploitation:.2f}",
                "- Sticks with first good option",
                "- Can get stuck on suboptimal choice",
                "",
                f"Balanced (epsilon={epsilon:.2f}): {final_balanced:.2f}",
                f"- Explores {epsilon * 100:.0f}% of time",
                f"- Exploits {(1 - epsilon) * 100:.0f}% of time",
                "- Balance is key!",
                "",
                "True means:",
                f"Machine 1: {true_means[0]:.2f}",
                f"Machine 2: {true_means[1]:.2f}",
                f"Machine 3: {true_means[2]:.2f} (best)",
            ]

            comment_text = "\n".join(comment_lines)
            ax.text(
                0.05,
                0.95,
                comment_text,
                transform=ax.transAxes,
                fontsize=11,
                verticalalignment="top",
                family="monospace",
                bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.5),
            )

            plt.tight_layout()
            plt.show()

    def on_widget_change(change) -> None:
        """
        Handle widget value changes.
        """
        update_plot()

    # Connect callbacks to automatically update when widgets change.
    seed_slider.observe(on_widget_change, names="value")
    coins_slider.observe(on_widget_change, names="value")
    epsilon_slider.observe(on_widget_change, names="value")

    # Layout widgets.
    controls = ipywidgets.VBox(
        [
            seed_box,
            coins_box,
            epsilon_box,
        ]
    )

    # Display widgets and initial plot.
    display(controls, output)
    update_plot()


# #############################################################################
# Interactive Widget Functions
# #############################################################################


def cell3_strategy_comparison() -> None:
    """
    Interactive widget for comparing strategies with epsilon sweep.

    User can:
    - Set number of machines and coins.
    - Configure mu values.
    - Set number of trials.
    - Run epsilon sweep and visualize results.
    """
    # Initialize state.
    state = {
        "k_machines": 3,
        "mu_values": [-0.2, 0.0, 0.5],
        "n_coins": 100,
        "n_trials": 10,
        "results": None,
    }
    # Create widgets.
    k_machines_slider, k_machines_box = htutori.build_widget_control(
        name="k_machines",
        description="number of machines (K)",
        min_val=2,
        max_val=10,
        step=1,
        initial_value=3,
        is_float=False,
    )
    n_coins_slider, n_coins_box = htutori.build_widget_control(
        name="n_coins",
        description="number of coins (N)",
        min_val=50,
        max_val=500,
        step=50,
        initial_value=100,
        is_float=False,
    )
    n_trials_slider, n_trials_box = htutori.build_widget_control(
        name="n_trials",
        description="number of trials",
        min_val=5,
        max_val=50,
        step=5,
        initial_value=10,
        is_float=False,
    )
    seed_slider, seed_box = htutori.build_widget_control(
        name="seed",
        description="random seed",
        min_val=0,
        max_val=100,
        step=1,
        initial_value=42,
        is_float=False,
    )
    # Create mu values text input.
    mu_text = ipywidgets.Text(
        value="-0.2, 0.0, 0.5",
        description="mu values:",
        style={"description_width": "120px"},
    )
    # Create run button.
    run_button = ipywidgets.Button(
        description="Run Epsilon Sweep",
        button_style="success",
        layout={"width": "200px"},
    )
    # Output widget.
    output = ipywidgets.Output()

    def on_run_clicked(b) -> None:
        """
        Handle run button click.
        """
        with output:
            clear_output(wait=True)
            # Parse mu values.
            try:
                mu_values = [float(x.strip()) for x in mu_text.value.split(",")]
                k_machines = k_machines_slider.value
                if len(mu_values) != k_machines:
                    _LOG.warning(
                        "Number of mu values (%d) must equal k_machines (%d)",
                        len(mu_values),
                        k_machines,
                    )
                    return
            except ValueError:
                _LOG.warning(
                    "Invalid mu values format. Use comma-separated numbers."
                )
                return
            # Update state.
            state["k_machines"] = k_machines
            state["mu_values"] = mu_values
            state["n_coins"] = n_coins_slider.value
            state["n_trials"] = n_trials_slider.value
            # Run simulation.
            _LOG.info(
                "Running epsilon sweep with %d trials...", state["n_trials"]
            )
            simulation = sim.BanditSimulation(
                k_machines=state["k_machines"],
                mu_values=state["mu_values"],
                n_coins=state["n_coins"],
                base_seed=seed_slider.value,
            )
            results = simulation.epsilon_sweep(
                n_trials=state["n_trials"],
            )
            state["results"] = results
            # Plot results.
            plot_epsilon_sweep(sweep_results=results, n_coins=state["n_coins"])

    # Connect callback.
    run_button.on_click(on_run_clicked)
    # Layout widgets.
    controls = ipywidgets.VBox(
        [
            k_machines_box,
            mu_text,
            n_coins_box,
            n_trials_box,
            seed_box,
            run_button,
        ]
    )
    # Display widgets.
    display(controls, output)


def cell4_ensemble_comparison() -> None:
    """
    Interactive widget for comparing strategies over random mu configs.

    User can:
    - Set number of machines and coins
    - Configure number of trials and mu configurations
    - Set epsilon value
    - Run ensemble comparison and visualize results
    """
    # Initialize state.
    state = {
        "k_machines": 3,
        "n_coins": 100,
        "n_trials": 10,
        "n_mu_configs": 10,
        "epsilon": 0.1,
        "results": None,
    }
    # Create widgets.
    k_machines_slider, k_machines_box = htutori.build_widget_control(
        name="k_machines",
        description="number of machines (K)",
        min_val=2,
        max_val=10,
        step=1,
        initial_value=3,
        is_float=False,
    )
    n_coins_slider, n_coins_box = htutori.build_widget_control(
        name="n_coins",
        description="number of coins (N)",
        min_val=50,
        max_val=500,
        step=50,
        initial_value=100,
        is_float=False,
    )
    n_trials_slider, n_trials_box = htutori.build_widget_control(
        name="n_trials",
        description="number of trials",
        min_val=5,
        max_val=50,
        step=5,
        initial_value=10,
        is_float=False,
    )
    n_mu_configs_slider, n_mu_configs_box = htutori.build_widget_control(
        name="n_mu_configs",
        description="number of mu configs",
        min_val=5,
        max_val=50,
        step=5,
        initial_value=10,
        is_float=False,
    )
    epsilon_slider, epsilon_box = htutori.build_widget_control(
        name="epsilon",
        description="epsilon value",
        min_val=0.0,
        max_val=1.0,
        step=0.1,
        initial_value=0.1,
        is_float=True,
    )
    seed_slider, seed_box = htutori.build_widget_control(
        name="seed",
        description="random seed",
        min_val=0,
        max_val=100,
        step=1,
        initial_value=42,
        is_float=False,
    )
    # Create run button.
    run_button = ipywidgets.Button(
        description="Run Ensemble Comparison",
        button_style="success",
        layout={"width": "200px"},
    )
    # Output widget.
    output = ipywidgets.Output()

    def on_run_clicked(b) -> None:
        """
        Handle run button click.
        """
        with output:
            clear_output(wait=True)
            # Update state.
            state["k_machines"] = k_machines_slider.value
            state["n_coins"] = n_coins_slider.value
            state["n_trials"] = n_trials_slider.value
            state["n_mu_configs"] = n_mu_configs_slider.value
            state["epsilon"] = epsilon_slider.value
            # Run ensemble.
            _LOG.info(
                "Running ensemble with %d trials and %d mu configs...",
                state["n_trials"],
                state["n_mu_configs"],
            )
            ensemble = sim.BanditEnsemble(
                k_machines=state["k_machines"],
                n_coins=state["n_coins"],
                base_seed=seed_slider.value,
            )
            results = ensemble.compare_strategies_ensemble(
                n_trials=state["n_trials"],
                n_mu_configs=state["n_mu_configs"],
                epsilon=state["epsilon"],
            )
            state["results"] = results
            # Plot results.
            ensemble.plot_ensemble_comparison(
                ensemble_results=results,
                epsilon=state["epsilon"],
            )

    # Connect callback.
    run_button.on_click(on_run_clicked)
    # Layout widgets.
    controls = ipywidgets.VBox(
        [
            k_machines_box,
            n_coins_box,
            n_trials_box,
            n_mu_configs_box,
            epsilon_box,
            seed_box,
            run_button,
        ]
    )
    # Display widgets.
    display(controls, output)
