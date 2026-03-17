<!-- TODO(gp): For me this belongs to the notebooks -->
## The Problem with Most MARL Tutorials
Most multi-agent reinforcement learning tutorials show:

- Moving loss curves
- Increasing rewards
- "Healthy-looking" training

But they rarely verify:

- Whether agents truly coordinate
- Whether communication carries useful information
- Whether evaluation-time success improves

In multi-agent RL, training curves are not proof of cooperation.

This tutorial focuses on measurable coordination.

## What You'll Build in 60 Minutes

### 1. Environment + Wrapper Layer
- PettingZoo MPE task (e.g., `simple_reference`)
- TorchRL-compatible wrappers
- Explicit message-channel wiring

### 2. CTDE Training Setup
- Decentralized per-agent actors
- Centralized critic
- Stable policy optimization

### 3. Outcome-Aligned Evaluation
- Binary success rate
- Goal-distance debugging
- Structured communication metrics

### 4. Communication Verification
- `message_entropy`
- `message_change_rate`
- Observation-derived verification checks

### 5. Optional Causal Ablations
- `full_comm`
- `disable_comm`
- `random_comm`

If communication matters, success should drop when it is removed.

## Why TorchRL + PettingZoo (MPE)?
This stack provides:

- A clean multi-agent API (PettingZoo)
- A PyTorch-native RL pipeline (TorchRL)
- Full control over observations, actions, and message channels
- Lightweight local reproducibility

MPE is ideal for:

- Studying coordination failure modes
- Debugging communication mechanisms
- Practicing CTDE engineering patterns

## Final Takeaway
In multi-agent reinforcement learning:

- Loss curves are not evidence of coordination.
- Reward trends are not proof of cooperation.

**Success metrics, diagnostics, and ablations are.**

## Evaluation Metrics
This tutorial prioritizes structured evaluation over noisy return curves:

- **success**: Binary success based on goal distance threshold
- **distances**: Debug visibility into goal proximity across episodes
- **Communication structure**:
  - Message_entropy: Entropy of agent communication
  - Message_change_rate: Frequency of communication changes
  - Observation-derived variants: Alternative metrics based on observations

## Troubleshooting
- **Success rate always 0.0**
  - Check `success_dist` threshold in config
  - Print goal distances to verify environment dynamics
  - Verify environment version (simple_reference_v3)

- **Communication metrics look random**
  - Increase training duration
  - Tune entropy coefficient in loss function
  - Run communication sanity checks in the API notebook

- **Wrapper or spec errors**
  - Confirm installed versions with `pip freeze`
  - Run the API notebook first to inspect environment specs

