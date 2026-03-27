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
# # TorchRL and PettingZoo MPE API Tutorial: Multi-Agent Cooperation

# %% [markdown]
# ### Goal of this tutorial
#
# This API tutorial introduces a lightweight wrapper layer for **training and evaluating cooperative multi-agent RL policies with communication** on PettingZoo's MPE tasks using TorchRL-friendly primitives.
#
# The focus is on:
#
# - configuring the training run using a single config object,
# - running training end-to-end through one clean entrypoint,
# - producing standardized plots and evaluation metrics,
# - validating communication behavior with measurable signals.
#
# This file explains the interface and design decisions, and demonstrates minimal usage.

# %% [markdown]
# ### Function imports

# %% [markdown]
# The notebook uses **two public functions**:
#
# - `default_cfg()`
#   Returns a configuration object with sane defaults.
#
# - `train_wrapper(cfg)`
#   Runs the full training loop and produces:
#   - training curves (loss, return, entropy),
#   - checkpointing (saved automatically after training).

# %%
from TorchRL_MAC_utils import train_wrapper, default_cfg

# %% [markdown]
# ### Configuration object (what you control)
#
# The API notebook demonstrates editing these fields for stability and reproducibility:

# %% [markdown]
#
# #### Data per update (critical for stability)
#
# - `cfg.rollout_len`: number of steps collected per environment per update
# - `cfg.num_envs`: number of parallel environments
#
# In the notebook we explicitly set:
#
# ```python
# rollout_len = 128
# num_envs = 4
# ```
#
# This yields 128 * 4 = 512 samples per update, which is typically much more stable than very small on-policy batches.
#

# %% [markdown]
#
# #### PPO-style optimization knobs (as used in the notebook)
#
# - `cfg.ppo_epochs`: number of optimization epochs per collected batch
# - `cfg.clip_param`: PPO clipping parameter for stable policy updates
# - `cfg.entropy_coef`: exploration regularization
#

# %% [markdown]
#
# #### Training runtime knobs
#
# - `cfg.num_iters`: total training iterations
# - `cfg.lr`: learning rate
# - `cfg.hidden_dim`: network width
# - `cfg.log_interval`: print/log frequency
#

# %% [markdown]
#
# #### Evaluation knobs
#
# - `cfg.eval_episodes`: number of eval episodes per evaluation phase (used when calling `evaluate()` separately)
# - `cfg.eval_interval`: evaluation interval (currently set in notebook but evaluation is done separately after training)
#

# %%
# Create configuration
cfg = default_cfg()

# --- CRITICAL FOR PPO STABILITY ---
# PPO needs more data per update.
# 128 steps * 4 envs = 512 total samples per update (Minimum for stable PPO)
cfg.rollout_len = 128
cfg.num_envs = 4

# PPO Hyperparameters
cfg.ppo_epochs = 4
cfg.clip_param = 0.2
cfg.entropy_coef = 0.01

# Training run
cfg.num_iters = 2000
cfg.lr = 3e-4
cfg.hidden_dim = 128
cfg.log_interval = 10

# Evaluation settings
cfg.eval_episodes = 20
cfg.eval_interval = 200

print("Configuration:")
print(f"  Training iterations: {cfg.num_iters}")
print(f"  Batch size (steps * envs): {cfg.rollout_len * cfg.num_envs}")
print(f"  Learning rate: {cfg.lr}")

# %% [markdown]
# ### Function call to training wrapper
#
# This runs the training loop and plots training curves (training loss, episode returns, and policy entropy).

# %% [markdown]
# #### What train_wrapper(cfg) does
#
# At a high level, `train_wrapper(cfg)` performs:
#
# 1. Initialize env(s) + policy/value networks from config
# 2. For each training iteration:
#    - Collect rollouts across `num_envs * rollout_len` steps
#    - Update policy/value using PPO-style minibatch optimization for `ppo_epochs`
#    - Log training metrics (loss, return, entropy) at `log_interval`
# 3. Generate and display training curves (loss, return, entropy plots)
# 4. Save checkpoint with trained models
#
# > **Note:** Evaluation (success metrics, communication statistics) is performed separately using the `evaluate()` function after training completes. See `TorchRL_MAC.example.ipynb` for examples of post-training evaluation.

# %%
train_wrapper(cfg)
