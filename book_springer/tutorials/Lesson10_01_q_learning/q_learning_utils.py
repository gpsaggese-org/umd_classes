"""
Utility functions for the Q-learning FrozenLake notebook (Lesson 10.01,
Algorithm 1).

Implements the FrozenLake grid rendering, the brute-force policy-enumeration
baseline, and tabular Q-learning (TD update, epsilon-greedy exploration,
training loop), matching the cell-by-cell pedagogical flow of the paired
notebook.

Import as:

import q_learning_utils as utils
"""

import logging
from typing import Any, Dict, List, Optional, Tuple

import gymnasium as gym
import ipywidgets
import matplotlib.axes
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from IPython.display import clear_output, display

import helpers.hnotebook as hnotebo
import helpers.hprint as hprint
import helpers.htutorial as htutori

_LOG = logging.getLogger(__name__)


def init_loggers(notebook_log: logging.Logger) -> None:
    """
    Wire the notebook logger into the utils logger.
    """
    global _LOG
    hnotebo.init_loggers(notebook_log, utils_log=_LOG)


# #############################################################################
# Constants: FrozenLake layout and action geometry
# #############################################################################

# Default 4x4 FrozenLake map (S=start, F=frozen, H=hole, G=goal).
FROZEN_LAKE_MAP = ["SFFF", "FHFH", "FFFH", "HFFG"]
N_ROW = 4
N_COL = 4
N_STATES = N_ROW * N_COL
N_ACTIONS = 4

# Gymnasium's `FrozenLake-v1` action convention.
ACTION_ID_TO_NAME = {0: "Left", 1: "Down", 2: "Right", 3: "Up"}
NAME_TO_ACTION_ID = {v: k for k, v in ACTION_ID_TO_NAME.items()}
ACTIONS = list(ACTION_ID_TO_NAME.values())

# Per-action (d_row, d_col) arrow-tip offset for drawing a policy arrow inside
# a grid cell (row increases downward, matching the array layout of `desc`).
ARROW_DELTA = {
    "Left": (0.0, -0.3),
    "Down": (0.3, 0.0),
    "Right": (0.0, 0.3),
    "Up": (-0.3, 0.0),
}

# Cell fill color keyed by tile type.
TILE_COLOR = {
    "S": "#cfe8ff",
    "F": "#ffffff",
    "H": "#9e9e9e",
    "G": "#a8e6a3",
}


# #############################################################################
# Environment helpers
# #############################################################################


def make_env(*, is_slippery: bool = True) -> gym.Env:
    """
    Create a 4x4 `FrozenLake-v1` environment.

    :param is_slippery: if True, the intended action succeeds only 1/3 of the
        time, with the two perpendicular slips splitting the rest equally; if
        False, actions are deterministic
    :return: the gymnasium environment
    """
    _LOG.debug(hprint.to_str("is_slippery"))
    env = gym.make("FrozenLake-v1", map_name="4x4", is_slippery=is_slippery)
    return env


def get_desc(env: gym.Env) -> List[str]:
    """
    Return the FrozenLake tile grid as a list of row strings.

    :param env: a `FrozenLake-v1` environment
    :return: e.g. `["SFFF", "FHFH", "FFFH", "HFFG"]`
    """
    desc = env.unwrapped.desc  # type: ignore[attr-defined]
    rows = ["".join(c.decode("utf-8") for c in row) for row in desc]
    return rows


def state_to_rc(state: int) -> Tuple[int, int]:
    """
    Convert a flat state id into `(row, col)` on the 4x4 grid.
    """
    row, col = divmod(state, N_COL)
    return row, col


def is_terminal_tile(tile: str) -> bool:
    """
    Return True if a tile ends the episode (a hole or the goal).
    """
    return tile in ("H", "G")


# #############################################################################
# Drawing helpers
# #############################################################################


def draw_grid(
    ax: matplotlib.axes.Axes,
    desc: List[str],
    *,
    highlight: Optional[int] = None,
    agent_state: Optional[int] = None,
    title: str = "",
) -> None:
    """
    Draw the FrozenLake grid with tiles colored by type.

    :param ax: axes to draw on
    :param desc: tile grid, e.g. `["SFFF", "FHFH", "FFFH", "HFFG"]`
    :param highlight: optional state id to outline in bold
    :param agent_state: optional state id to mark with an agent dot
    :param title: optional axes title
    """
    # Draw one colored, labeled rectangle per tile.
    for row in range(N_ROW):
        for col in range(N_COL):
            tile = desc[row][col]
            rect = mpatches.Rectangle(
                (col - 0.5, row - 0.5),
                1.0,
                1.0,
                facecolor=TILE_COLOR[tile],
                edgecolor="black",
                linewidth=1.5,
            )
            ax.add_patch(rect)
            ax.text(
                col,
                row,
                tile,
                ha="center",
                va="center",
                fontsize=11,
                fontweight="bold",
            )
    if highlight is not None:
        row, col = state_to_rc(highlight)
        rect = mpatches.Rectangle(
            (col - 0.5, row - 0.5),
            1.0,
            1.0,
            fill=False,
            edgecolor="darkblue",
            linewidth=3.5,
        )
        ax.add_patch(rect)
    if agent_state is not None:
        row, col = state_to_rc(agent_state)
        ax.plot(col, row, marker="o", color="darkorange", markersize=16)
    # Row 0 is drawn at the top, matching the grid's array layout.
    ax.set_xlim(-0.6, N_COL - 0.4)
    ax.set_ylim(N_ROW - 0.4, -0.6)
    ax.set_xticks(range(N_COL))
    ax.set_yticks(range(N_ROW))
    ax.set_aspect("equal")
    if title:
        ax.set_title(title, fontsize=13, fontweight="bold")


def draw_policy_arrows(
    ax: matplotlib.axes.Axes,
    policy: Dict[int, str],
    *,
    color: str = "black",
) -> None:
    """
    Draw an arrow for each non-terminal state showing its policy action.
    """
    for state, action in policy.items():
        row, col = state_to_rc(state)
        d_row, d_col = ARROW_DELTA[action]
        ax.annotate(
            "",
            xy=(col + d_col, row + d_row),
            xytext=(col - d_col, row - d_row),
            arrowprops=dict(arrowstyle="-|>", color=color, linewidth=2.5),
        )


def _values_to_grid(values: Dict[int, float]) -> np.ndarray:
    """
    Reshape a per-state value dict into a `(N_ROW, N_COL)` array.
    """
    grid = np.array(
        [
            [values.get(row * N_COL + col, 0.0) for col in range(N_COL)]
            for row in range(N_ROW)
        ]
    )
    return grid


def draw_value_heatmap(
    ax: matplotlib.axes.Axes,
    values: Dict[int, float],
    *,
    title: str,
    cmap: str = "RdYlGn",
) -> None:
    """
    Draw a heatmap of a per-state scalar (e.g., `max_a Q(s,a)`).
    """
    grid = _values_to_grid(values)
    sns.heatmap(
        grid,
        ax=ax,
        cmap=cmap,
        annot=True,
        fmt=".2f",
        cbar=False,
        linewidths=1.0,
        linecolor="black",
        annot_kws={"fontsize": 9},
    )
    ax.set_title(title, fontsize=13, fontweight="bold")
    ax.set_xlabel("col")
    ax.set_ylabel("row")


def draw_visit_heatmap(
    ax: matplotlib.axes.Axes,
    visit_counts: Dict[int, int],
    *,
    title: str,
) -> None:
    """
    Draw a heatmap of per-state visit counts.
    """
    grid = _values_to_grid({s: float(c) for s, c in visit_counts.items()})
    sns.heatmap(
        grid,
        ax=ax,
        cmap="viridis",
        annot=True,
        fmt=".0f",
        cbar=False,
        linewidths=1.0,
        linecolor="black",
    )
    ax.set_title(title, fontsize=13, fontweight="bold")
    ax.set_xlabel("col")
    ax.set_ylabel("row")


def comment_panel(ax: matplotlib.axes.Axes, text: str) -> None:
    """
    Render a wheat-colored comment panel with a bold "Comments" title.
    """
    ax.axis("off")
    ax.set_title("Comments", fontsize=14, fontweight="bold", pad=20)
    htutori.add_fitted_text_box(ax, text, max_fontsize=12, min_fontsize=8)


def make_param_info(descriptions: Dict[str, str]) -> ipywidgets.HTML:
    """
    Build a styled HTML info box for notebook cell control panels.

    Each `(name, desc)` pair renders as `<b>name</b>: desc<br>`.

    :param descriptions: mapping from parameter name to its description text
    :return: styled HTML widget ready for display
    """
    body = "\n".join(
        "<b>%s</b>: %s<br>" % (name, desc) for name, desc in descriptions.items()
    )
    html = (
        "<div style='background:#f5f5f5; padding:10px 14px; "
        "border-radius:4px; border-left:3px solid #4682b4; "
        "font-size:13px; line-height:1.8'>"
        "%s"
        "</div>"
    ) % body
    return ipywidgets.HTML(html)


# #############################################################################
# Tabular Q-learning (uses env.step() -- no access to the transition model)
# #############################################################################


def _greedy_action(
    q: Dict[int, float], state: int, rng: np.random.RandomState
) -> int:
    """
    Return the action with the highest Q-value at `state`.

    Ties are broken randomly. Without this, an all-zero Q-row (e.g., before
    any reward has ever been observed) always resolves to action 0 via plain
    `max()`, systematically biasing early training toward one fixed action
    instead of behaving like an unbiased random walk.

    Q-values are stored under the flat key `state * N_ACTIONS + action`.
    """
    values = [q[state * N_ACTIONS + a] for a in range(N_ACTIONS)]
    best_value = max(values)
    best_actions = [a for a, v in enumerate(values) if v == best_value]
    best_a = int(rng.choice(best_actions))
    return best_a


def extract_policy(
    q: Dict[int, float], desc: List[str], *, seed: int = 0
) -> Dict[int, str]:
    """
    Extract the greedy policy `argmax_a Q(s,a)` for every non-terminal state.

    :param seed: seed for the random tie-breaker in `_greedy_action()`
    """
    rng = np.random.RandomState(seed)
    policy: Dict[int, str] = {}
    for state in range(N_STATES):
        row, col = state_to_rc(state)
        if is_terminal_tile(desc[row][col]):
            continue
        policy[state] = ACTION_ID_TO_NAME[_greedy_action(q, state, rng)]
    return policy


def q_learning(
    env: gym.Env,
    desc: List[str],
    *,
    n_episodes: int,
    alpha: float,
    seed: int,
    gamma: float = 0.99,
    epsilon_start: float = 1.0,
    epsilon_min: float = 0.05,
    epsilon_decay: float = 0.01,
    max_steps: int = 100,
) -> Dict[str, Any]:
    """
    Learn Q-values via tabular Q-learning from `env.step()` experience alone.

    Epsilon decays exponentially every episode:
    `epsilon_t = epsilon_min + (epsilon_start - epsilon_min) *
    exp(-epsilon_decay * episode)`.

    :param env: a `FrozenLake-v1` environment
    :param desc: tile grid used to identify terminal states
    :param n_episodes: number of training episodes
    :param alpha: learning rate
    :param seed: random seed for reproducibility
    :param gamma: discount factor
    :param epsilon_start: initial exploration probability
    :param epsilon_min: floor exploration probability after decay
    :param epsilon_decay: exponential decay rate applied per episode
    :param max_steps: max steps per episode before truncation
    :return: dict with `q` (flat Q-table), `returns` (per-episode reward,
        0.0/1.0 for FrozenLake), `visit_counts` (per-state visit count),
        `policy` (final greedy policy)
    """
    _LOG.debug(hprint.to_str("n_episodes alpha gamma seed epsilon_decay"))
    rng = np.random.RandomState(seed)
    q: Dict[int, float] = {
        s * N_ACTIONS + a: 0.0 for s in range(N_STATES) for a in range(N_ACTIONS)
    }
    visit_counts: Dict[int, int] = {s: 0 for s in range(N_STATES)}
    returns: List[float] = []
    # Each episode rolls out a trajectory via env.step(), applying an
    # epsilon-greedy TD update at every transition.
    for episode in range(n_episodes):
        epsilon = epsilon_min + (epsilon_start - epsilon_min) * np.exp(
            -epsilon_decay * episode
        )
        state, _ = env.reset(seed=seed + episode)
        total_reward = 0.0
        for _ in range(max_steps):
            visit_counts[state] += 1
            # Epsilon-greedy: explore randomly with prob epsilon, else greedy.
            if rng.rand() < epsilon:
                action = rng.randint(N_ACTIONS)
            else:
                action = _greedy_action(q, state, rng)
            next_state, reward_raw, terminated, truncated, _ = env.step(action)
            reward = float(reward_raw)
            total_reward += reward
            # Terminal transitions have no bootstrapped next-state value.
            if terminated or truncated:
                td_target = reward
            else:
                best_next = max(
                    q[next_state * N_ACTIONS + a2] for a2 in range(N_ACTIONS)
                )
                td_target = reward + gamma * best_next
            q[state * N_ACTIONS + action] += alpha * (
                td_target - q[state * N_ACTIONS + action]
            )
            state = next_state
            if terminated or truncated:
                break
        returns.append(total_reward)
    policy = extract_policy(q, desc)
    result = {
        "q": q,
        "returns": returns,
        "visit_counts": visit_counts,
        "policy": policy,
    }
    _LOG.debug("return: len(q)=%s len(returns)=%s", len(q), len(returns))
    return result


# #############################################################################
# Brute-force policy enumeration baseline
# #############################################################################


def random_policy(desc: List[str], *, seed: int) -> Dict[int, str]:
    """
    Build one random deterministic policy over the non-terminal states.
    """
    rng = np.random.RandomState(seed)
    policy: Dict[int, str] = {}
    for state in range(N_STATES):
        row, col = state_to_rc(state)
        if is_terminal_tile(desc[row][col]):
            continue
        policy[state] = ACTIONS[rng.randint(N_ACTIONS)]
    return policy


def rollout_policy(
    env: gym.Env,
    policy: Dict[int, str],
    *,
    seed: int,
    max_steps: int = 100,
) -> float:
    """
    Roll out a fixed policy for one episode.

    :return: total reward for the episode (0.0 or 1.0 for FrozenLake)
    """
    state, _ = env.reset(seed=seed)
    total_reward = 0.0
    for _ in range(max_steps):
        action_name = policy.get(state)
        if action_name is None:
            # Reached a state without a policy entry (a terminal tile).
            break
        action = NAME_TO_ACTION_ID[action_name]
        state, reward, terminated, truncated, _ = env.step(action)
        total_reward += float(reward)
        if terminated or truncated:
            break
    return total_reward


def evaluate_policy(
    env: gym.Env,
    policy: Dict[int, str],
    *,
    n_eval_episodes: int,
    seed: int,
) -> float:
    """
    Estimate a policy's success rate by averaging over `n_eval_episodes`
    rollouts.
    """
    rng = np.random.RandomState(seed)
    successes = [
        rollout_policy(env, policy, seed=int(rng.randint(0, 1_000_000)))
        for _ in range(n_eval_episodes)
    ]
    return float(np.mean(successes))


def score_random_policies(
    env: gym.Env,
    desc: List[str],
    *,
    n_policies: int,
    n_rollouts: int,
    seed: int,
) -> List[Dict[str, Any]]:
    """
    Score `n_policies` random deterministic policies via Monte Carlo rollouts.

    This is the brute-force baseline: no update rule improves a policy, each
    candidate is scored independently from scratch.

    :return: list of `{'policy', 'mean_return'}` dicts, sorted by descending
        `mean_return`
    """
    _LOG.debug(hprint.to_str("n_policies n_rollouts seed"))
    results = []
    for i in range(n_policies):
        policy = random_policy(desc, seed=seed * 1000 + i)
        mean_return = evaluate_policy(
            env, policy, n_eval_episodes=n_rollouts, seed=seed * 1000 + i
        )
        results.append({"policy": policy, "mean_return": mean_return})
    results.sort(key=lambda r: r["mean_return"], reverse=True)
    return results


def _cumulative_rollout_means(
    env: gym.Env,
    policy: Dict[int, str],
    *,
    n_rollouts: int,
    seed: int,
) -> np.ndarray:
    """
    Roll out a policy `n_rollouts` times and return the running mean return
    after each rollout, showing how the score estimate wobbles early on.
    """
    rng = np.random.RandomState(seed)
    rewards = [
        rollout_policy(env, policy, seed=int(rng.randint(0, 1_000_000)))
        for _ in range(n_rollouts)
    ]
    running_mean = np.cumsum(rewards) / np.arange(1, n_rollouts + 1)
    return running_mean


# #############################################################################
# Cell 1.1: the FrozenLake environment: states, actions, rewards
# #############################################################################


def cell1_1_show_environment(
    *,
    figsize: Optional[Tuple[float, float]] = None,
) -> None:
    """
    Draw the FrozenLake grid and print its observation/action spaces.
    """
    if figsize is None:
        figsize = (14, 5)
    is_slippery_toggle = ipywidgets.ToggleButton(
        value=True,
        description="is_slippery",
        style={"description_width": "initial"},
    )
    seed_slider, seed_box = htutori.build_widget_control(
        name="seed",
        description="random seed",
        min_val=0,
        max_val=100,
        step=1,
        initial_value=0,
        is_float=False,
    )
    output = ipywidgets.Output()

    def update_plot(change: Optional[Any] = None) -> None:
        _ = change
        with output:
            clear_output(wait=True)
            env = make_env(is_slippery=is_slippery_toggle.value)
            desc = get_desc(env)
            state, _ = env.reset(seed=seed_slider.value)
            _, (ax1, ax2) = plt.subplots(1, 2, figsize=figsize)
            draw_grid(
                ax1,
                desc,
                agent_state=state,
                title="FrozenLake 4x4 (S=start, F=frozen, H=hole, G=goal)",
            )
            # Draw the 4 possible moves from the start tile.
            row, col = state_to_rc(state)
            for action in ACTIONS:
                d_row, d_col = ARROW_DELTA[action]
                ax1.annotate(
                    "",
                    xy=(col + d_col, row + d_row),
                    xytext=(col, row),
                    arrowprops=dict(
                        arrowstyle="-|>", color="darkblue", linewidth=1.8
                    ),
                )
            ax1.set_xlabel(
                "col\n\n"
                "_Grid layout_: tiles colored by type, agent marker at the "
                "start, arrows show the 4 possible moves",
                fontsize=9,
            )
            text = (
                "n_states: %d\n"
                "n_actions: %d\n"
                "is_slippery: %s\n\n"
                "Reward:\n"
                "  +1 on reaching goal\n"
                "  0 otherwise\n\n"
                "Episode ends on:\n"
                "  falling in a hole\n"
                "  reaching the goal"
                % (N_STATES, N_ACTIONS, is_slippery_toggle.value)
            )
            comment_panel(ax2, text)
            plt.tight_layout()
            plt.show()

    param_info = make_param_info(
        {
            "is_slippery": "toggle stochastic ice (intended action succeeds 1/3 of the time) vs deterministic movement",
            "seed": "random seed for the environment reset shown on the grid",
        }
    )
    is_slippery_toggle.observe(update_plot, names="value")
    seed_slider.observe(update_plot, names="value")
    update_plot()
    controls = ipywidgets.VBox([is_slippery_toggle, seed_box])
    top_row = ipywidgets.HBox([controls, param_info])
    display(ipywidgets.VBox([top_row, output]))


# #############################################################################
# Cell 1.2: why enumerating every policy is infeasible
# #############################################################################


def cell1_2_bruteforce_infeasibility(
    *,
    figsize: Optional[Tuple[float, float]] = None,
) -> None:
    """
    Show the policy-count blow-up and how noisy Monte Carlo scoring stays
    even as rollouts per policy grow.
    """
    if figsize is None:
        figsize = (16, 5)
    env = make_env(is_slippery=True)
    desc = get_desc(env)
    # A "reasonable" brute-force budget: this many policies can actually be
    # scored within a notebook cell.
    n_afforded = 30
    # Fix the 3 top-ranked example policies once, using a large scoring
    # budget purely to rank a larger pool. Most random deterministic policies
    # score exactly 0 (they walk straight into a hole on the first slip), so
    # the top 3 of a 25-policy pool are the ones worth watching converge.
    pool = score_random_policies(env, desc, n_policies=25, n_rollouts=500, seed=3)
    example_policies = [p["policy"] for p in pool[:3]]
    example_labels = ["policy rank 1", "policy rank 2", "policy rank 3"]
    n_exp_slider, n_box = htutori.build_log_widget_control(
        name="log(n_rollouts)",
        description="rollouts per policy",
        min_exp=2,
        max_exp=10,
        initial_exp=7,
        base=2,
    )
    seed_slider, seed_box = htutori.build_widget_control(
        name="seed",
        description="random seed",
        min_val=0,
        max_val=100,
        step=1,
        initial_value=0,
        is_float=False,
    )
    output = ipywidgets.Output()

    def update_plot(change: Optional[Any] = None) -> None:
        _ = change
        with output:
            clear_output(wait=True)
            n_rollouts = 2**n_exp_slider.value
            seed = seed_slider.value
            _, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=figsize)
            # Panel 1: policy count blow-up (log scale).
            total_policies = N_ACTIONS ** (N_STATES - 2)  # 2 terminal tiles
            ax1.bar(
                ["Total policies\n(4^14)", "Policies scored\nin one cell"],
                [total_policies, n_afforded],
                color=["firebrick", "steelblue"],
            )
            ax1.set_yscale("log")
            ax1.set_ylabel("number of policies (log scale)")
            ax1.set_title("Policy count", fontsize=13, fontweight="bold")
            ax1.set_xlabel(
                "\n_Policy count_: total deterministic policies vs a "
                "practical scoring budget",
                fontsize=9,
            )
            for i, val in enumerate([total_policies, n_afforded]):
                ax1.text(
                    i, val, "%.2e" % val, ha="center", va="bottom", fontsize=9
                )
            # Panel 2: noisy ranking for the 3 fixed example policies.
            for label, policy in zip(example_labels, example_policies):
                running_mean = _cumulative_rollout_means(
                    env, policy, n_rollouts=n_rollouts, seed=seed
                )
                ax2.plot(range(1, n_rollouts + 1), running_mean, label=label)
            ax2.set_xlabel(
                "rollouts\n\n"
                "_Noisy ranking_: estimated success rate for 3 candidate "
                "policies as rollouts accumulate",
                fontsize=9,
            )
            ax2.set_ylabel("estimated success rate")
            ax2.set_title("Score stability", fontsize=13, fontweight="bold")
            ax2.legend(fontsize=9)
            ax2.grid(True, alpha=0.3)
            text = (
                "Parameters:\n"
                "  n_rollouts: %d\n"
                "  seed: %d\n\n"
                "|policies| = 4^14\n"
                "  (14 non-terminal states)\n"
                "  ~ %.2e\n\n"
                "Scored here: %d policies\n"
                "Each needs many rollouts\n"
                "to rank reliably."
                % (n_rollouts, seed, total_policies, n_afforded)
            )
            comment_panel(ax3, text)
            plt.tight_layout()
            plt.show()

    param_info = make_param_info(
        {
            "n_rollouts": "rollouts used to estimate each of the 3 example policies' success rate (log scale); more rollouts reduce noise but cost more samples",
            "seed": "random seed controlling the rollout sequence used for the estimate",
        }
    )
    n_exp_slider.observe(update_plot, names="value")
    seed_slider.observe(update_plot, names="value")
    update_plot()
    controls = ipywidgets.VBox([n_box, seed_box])
    top_row = ipywidgets.HBox([controls, param_info])
    display(ipywidgets.VBox([top_row, output]))


# #############################################################################
# Cell 2.1: the Q-learning TD update rule
# #############################################################################


def cell2_1_q_update_rule(
    *,
    figsize: Optional[Tuple[float, float]] = None,
) -> None:
    """
    Show how a single experience tuple nudges one Q-value.
    """
    if figsize is None:
        figsize = (14, 5)
    # A deterministic environment keeps the illustrative transition clean.
    env = make_env(is_slippery=False)
    desc = get_desc(env)
    # Pretrain a small Q-table snapshot once so the demo numbers look like a
    # partially-learned table rather than all zeros.
    snapshot = q_learning(
        env, desc, n_episodes=300, alpha=0.5, seed=1, epsilon_decay=0.02
    )
    q_snapshot = snapshot["q"]
    # Illustrative non-terminal transition: state 9 -> Right -> state 10.
    state, action_name, next_state, reward = 9, "Right", 10, 0.0
    action_id = NAME_TO_ACTION_ID[action_name]
    alpha_slider, alpha_box = htutori.build_widget_control(
        name="alpha",
        description="learning rate",
        min_val=0.0,
        max_val=1.0,
        step=0.05,
        initial_value=0.5,
        is_float=True,
    )
    gamma_slider, gamma_box = htutori.build_widget_control(
        name="gamma",
        description="discount factor",
        min_val=0.0,
        max_val=1.0,
        step=0.05,
        initial_value=0.9,
        is_float=True,
    )
    output = ipywidgets.Output()

    def update_plot(change: Optional[Any] = None) -> None:
        _ = change
        with output:
            clear_output(wait=True)
            alpha = alpha_slider.value
            gamma = gamma_slider.value
            q_old = q_snapshot[state * N_ACTIONS + action_id]
            best_next = max(
                q_snapshot[next_state * N_ACTIONS + a2]
                for a2 in range(N_ACTIONS)
            )
            td_target = reward + gamma * best_next
            td_error = td_target - q_old
            q_new = q_old + alpha * td_error
            _, (ax1, ax2) = plt.subplots(1, 2, figsize=figsize)
            draw_grid(ax1, desc, highlight=state)
            row, col = state_to_rc(state)
            d_row, d_col = ARROW_DELTA[action_name]
            ax1.annotate(
                "",
                xy=(col + d_col, row + d_row),
                xytext=(col, row),
                arrowprops=dict(arrowstyle="-|>", color="darkblue", linewidth=3.0),
            )
            ax1.set_title("One env.step() tuple", fontsize=13, fontweight="bold")
            ax1.set_xlabel(
                "col\n\n"
                "_Transition diagram_: one step s -> a -> s' with reward r",
                fontsize=9,
            )
            text = (
                "Update: Q <- Q + alpha[r +\n"
                "      gamma max Q(s',.) - Q]\n\n"
                "Parameters:\n"
                "  alpha: %.2f  gamma: %.2f\n\n"
                "For state=%d, action=%s:\n"
                "  old Q: %.3f\n"
                "  TD target: %.3f\n"
                "  TD error: %.3f\n"
                "  new Q: %.3f"
                % (alpha, gamma, state, action_name, q_old, td_target, td_error, q_new)
            )
            comment_panel(ax2, text)
            plt.tight_layout()
            plt.show()

    param_info = make_param_info(
        {
            "alpha": "learning rate; near 0 the estimate barely moves, near 1 it jumps to the TD target",
            "gamma": "discount factor weighting the bootstrapped next-state value in the TD target",
        }
    )
    alpha_slider.observe(update_plot, names="value")
    gamma_slider.observe(update_plot, names="value")
    update_plot()
    controls = ipywidgets.VBox([alpha_box, gamma_box])
    top_row = ipywidgets.HBox([controls, param_info])
    display(ipywidgets.VBox([top_row, output]))


# #############################################################################
# Cell 2.2: exploration vs exploitation with epsilon-greedy
# #############################################################################


def cell2_2_exploration_exploitation(
    *,
    figsize: Optional[Tuple[float, float]] = None,
) -> None:
    """
    Compare state coverage under low vs high epsilon (fixed epsilon, no
    decay, to isolate the exploration-rate effect).
    """
    if figsize is None:
        figsize = (16, 5)
    env = make_env(is_slippery=True)
    desc = get_desc(env)
    epsilon_slider, epsilon_box = htutori.build_widget_control(
        name="epsilon",
        description="exploration probability",
        min_val=0.0,
        max_val=1.0,
        step=0.05,
        initial_value=0.1,
        is_float=True,
    )
    n_exp_slider, n_box = htutori.build_log_widget_control(
        name="log(n_episodes)",
        description="training episodes",
        min_exp=4,
        max_exp=11,
        initial_exp=8,
        base=2,
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
    output = ipywidgets.Output()

    def update_plot(change: Optional[Any] = None) -> None:
        _ = change
        with output:
            clear_output(wait=True)
            n_episodes = 2**n_exp_slider.value
            eps = epsilon_slider.value
            seed = seed_slider.value
            # Fixed epsilon (no decay) isolates the effect of the chosen rate.
            low = q_learning(
                env,
                desc,
                n_episodes=n_episodes,
                alpha=0.1,
                seed=seed,
                epsilon_start=eps,
                epsilon_min=eps,
                epsilon_decay=0.0,
            )
            high = q_learning(
                env,
                desc,
                n_episodes=n_episodes,
                alpha=0.1,
                seed=seed,
                epsilon_start=0.9,
                epsilon_min=0.9,
                epsilon_decay=0.0,
            )
            _, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=figsize)
            draw_visit_heatmap(
                ax1, low["visit_counts"], title="Visits at epsilon=%.2f" % eps
            )
            ax1.set_xlabel(
                "col\n\n_Low-epsilon visits_: visit counts at the chosen rate",
                fontsize=9,
            )
            draw_visit_heatmap(
                ax2, high["visit_counts"], title="Visits at epsilon=0.90"
            )
            ax2.set_xlabel(
                "col\n\n_High-epsilon visits_: visit counts under broad "
                "exploration",
                fontsize=9,
            )
            # Holes and the goal end the episode on entry, so they are never
            # "visited" by construction; only count non-terminal states.
            nonterm_states = [
                s
                for s in range(N_STATES)
                if not is_terminal_tile(desc[state_to_rc(s)[0]][state_to_rc(s)[1]])
            ]
            n_unvisited_low = sum(
                1 for s in nonterm_states if low["visit_counts"][s] == 0
            )
            n_unvisited_high = sum(
                1 for s in nonterm_states if high["visit_counts"][s] == 0
            )
            text = (
                "Parameters:\n"
                "  epsilon: %.2f\n"
                "  n_episodes: %d\n"
                "  seed: %d\n\n"
                "Unvisited non-terminal states\n"
                "(out of %d reachable):\n"
                "  low epsilon: %d\n"
                "  high epsilon: %d"
                % (
                    eps,
                    n_episodes,
                    seed,
                    len(nonterm_states),
                    n_unvisited_low,
                    n_unvisited_high,
                )
            )
            comment_panel(ax3, text)
            plt.tight_layout()
            plt.show()

    param_info = make_param_info(
        {
            "epsilon": "exploration probability (held fixed, no decay); low values concentrate visits on a narrow path, high values spread visits broadly",
            "n_episodes": "number of training episodes (log scale)",
            "seed": "random seed for reproducible training runs",
        }
    )
    epsilon_slider.observe(update_plot, names="value")
    n_exp_slider.observe(update_plot, names="value")
    seed_slider.observe(update_plot, names="value")
    update_plot()
    controls = ipywidgets.VBox([epsilon_box, n_box, seed_box])
    top_row = ipywidgets.HBox([controls, param_info])
    display(ipywidgets.VBox([top_row, output]))


# #############################################################################
# Cell 2.3: training the Q-table and watching convergence
# #############################################################################


def cell2_3_training_convergence(
    *,
    figsize: Optional[Tuple[float, float]] = None,
) -> None:
    """
    Run full Q-learning training and show the learning curve and Q-table
    heatmap.
    """
    if figsize is None:
        figsize = (18, 5)
    env = make_env(is_slippery=True)
    desc = get_desc(env)
    n_exp_slider, n_box = htutori.build_log_widget_control(
        name="log(n_episodes)",
        description="training episodes",
        min_exp=6,
        max_exp=14,
        initial_exp=11,
        base=2,
    )
    alpha_slider, alpha_box = htutori.build_widget_control(
        name="alpha",
        description="learning rate",
        min_val=0.0,
        max_val=1.0,
        step=0.05,
        initial_value=0.1,
        is_float=True,
    )
    decay_slider, decay_box = htutori.build_widget_control(
        name="epsilon_decay",
        description="epsilon decay rate",
        min_val=0.001,
        max_val=0.05,
        step=0.001,
        initial_value=0.002,
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
    output = ipywidgets.Output()

    def update_plot(change: Optional[Any] = None) -> None:
        _ = change
        with output:
            clear_output(wait=True)
            n_episodes = 2**n_exp_slider.value
            result = q_learning(
                env,
                desc,
                n_episodes=n_episodes,
                alpha=alpha_slider.value,
                seed=seed_slider.value,
                epsilon_decay=decay_slider.value,
            )
            returns = result["returns"]
            max_q = {
                s: max(result["q"][s * N_ACTIONS + a] for a in range(N_ACTIONS))
                for s in range(N_STATES)
            }
            _, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=figsize)
            window = max(1, len(returns) // 50)
            smooth = pd.Series(returns).rolling(window, min_periods=1).mean()
            ax1.plot(smooth, color="seagreen")
            ax1.set_xlabel(
                "episode\n\n"
                "_Learning curve_: rolling-average success rate per episode",
                fontsize=9,
            )
            ax1.set_ylabel("success rate (smoothed)")
            ax1.set_title("Learning curve", fontsize=13, fontweight="bold")
            ax1.grid(True, alpha=0.3)
            draw_value_heatmap(ax2, max_q, title="max_a Q(s,a)")
            ax2.set_xlabel(
                "col\n\n"
                "_Q-table heatmap_: best action value learned per state",
                fontsize=9,
            )
            final_epsilon = 0.05 + (1.0 - 0.05) * np.exp(
                -decay_slider.value * (n_episodes - 1)
            )
            text = (
                "Parameters:\n"
                "  n_episodes: %d\n"
                "  alpha: %.2f\n"
                "  epsilon_decay: %.3f\n\n"
                "final epsilon: %.3f\n"
                "rolling success rate\n"
                "  (last %d ep): %.2f"
                % (
                    n_episodes,
                    alpha_slider.value,
                    decay_slider.value,
                    final_epsilon,
                    window,
                    float(np.asarray(smooth)[-1]),
                )
            )
            comment_panel(ax3, text)
            plt.tight_layout()
            plt.show()

    param_info = make_param_info(
        {
            "n_episodes": "number of training episodes (log scale); more episodes give the Q-table time to converge",
            "alpha": "learning rate controlling how much each experience updates the Q-value",
            "epsilon_decay": "exponential decay rate for epsilon; larger values shift from exploring to exploiting sooner",
            "seed": "random seed for reproducible training",
        }
    )
    n_exp_slider.observe(update_plot, names="value")
    alpha_slider.observe(update_plot, names="value")
    decay_slider.observe(update_plot, names="value")
    seed_slider.observe(update_plot, names="value")
    update_plot()
    controls = ipywidgets.VBox([n_box, alpha_box, decay_box, seed_box])
    top_row = ipywidgets.HBox([controls, param_info])
    display(ipywidgets.VBox([top_row, output]))


# #############################################################################
# Cell 2.4: the learned policy vs the brute-force baseline
# #############################################################################


def cell2_4_policy_vs_bruteforce(
    *,
    figsize: Optional[Tuple[float, float]] = None,
) -> None:
    """
    Compare the trained Q-learning policy against a random policy and the
    best of a small brute-force sample.
    """
    if figsize is None:
        figsize = (16, 5)
    env = make_env(is_slippery=True)
    desc = get_desc(env)
    n_eval_slider, n_eval_box = htutori.build_widget_control(
        name="n_eval_episodes",
        description="evaluation episodes",
        min_val=100,
        max_val=5000,
        step=100,
        initial_value=1000,
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
    output = ipywidgets.Output()
    # Train once: this is the same training run shown in Cell 2.3, reused
    # here as the "payoff" policy to compare against brute force.
    q_result = q_learning(
        env, desc, n_episodes=4000, alpha=0.1, seed=42, epsilon_decay=0.002
    )
    q_policy = q_result["policy"]
    max_q = {
        s: max(q_result["q"][s * N_ACTIONS + a] for a in range(N_ACTIONS))
        for s in range(N_STATES)
    }

    def update_plot(change: Optional[Any] = None) -> None:
        _ = change
        with output:
            clear_output(wait=True)
            n_eval = n_eval_slider.value
            seed = seed_slider.value
            # Brute-force baseline: score a small sample of random policies
            # and keep the best one (mirrors Cell 1.2's approach).
            sample = score_random_policies(
                env, desc, n_policies=30, n_rollouts=n_eval, seed=seed
            )
            best_bruteforce = sample[0]["policy"]
            random_baseline = random_policy(desc, seed=seed + 999)
            rate_random = evaluate_policy(
                env, random_baseline, n_eval_episodes=n_eval, seed=seed
            )
            rate_bruteforce = evaluate_policy(
                env, best_bruteforce, n_eval_episodes=n_eval, seed=seed
            )
            rate_q = evaluate_policy(
                env, q_policy, n_eval_episodes=n_eval, seed=seed
            )
            _, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=figsize)
            draw_value_heatmap(ax1, max_q, title="Q-learning policy")
            draw_policy_arrows(ax1, q_policy, color="black")
            ax1.set_xlabel(
                "col\n\n"
                "_Policy grid_: greedy actions over the learned Q-table",
                fontsize=9,
            )
            labels = ["random", "brute-force\n(best of 30)", "Q-learning"]
            rates = [rate_random, rate_bruteforce, rate_q]
            colors = ["firebrick", "darkorange", "seagreen"]
            ax2.bar(labels, rates, color=colors)
            ax2.set_ylim(0.0, 1.0)
            ax2.set_ylabel("success rate")
            ax2.set_title("Success rate comparison", fontsize=13, fontweight="bold")
            ax2.set_xlabel(
                "\n_Success-rate comparison_: over %d evaluation episodes each"
                % n_eval,
                fontsize=9,
            )
            for i, val in enumerate(rates):
                ax2.text(i, val, "%.2f" % val, ha="center", va="bottom", fontsize=9)
            text = (
                "Parameters:\n"
                "  n_eval_episodes: %d\n"
                "  seed: %d\n\n"
                "Success rate:\n"
                "  random: %.2f\n"
                "  brute-force (30 policies): %.2f\n"
                "  Q-learning: %.2f\n\n"
                "Q-learning trained once\n"
                "(4000 episodes), reused here."
                % (n_eval, seed, rate_random, rate_bruteforce, rate_q)
            )
            comment_panel(ax3, text)
            plt.tight_layout()
            plt.show()

    param_info = make_param_info(
        {
            "n_eval_episodes": "rollouts used to estimate each policy's success rate",
            "seed": "random seed for the brute-force sample and evaluation rollouts",
        }
    )
    n_eval_slider.observe(update_plot, names="value")
    seed_slider.observe(update_plot, names="value")
    update_plot()
    controls = ipywidgets.VBox([n_eval_box, seed_box])
    top_row = ipywidgets.HBox([controls, param_info])
    display(ipywidgets.VBox([top_row, output]))
