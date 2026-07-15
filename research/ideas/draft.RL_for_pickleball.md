# RL for Pickleball Strategy

## Objective
Model baseline rallies using RL to learn optimal strategies for shot selection and court positioning.

## Approximation 1: 1D Simplified Game

**Game Model**
- 1D analog of pickleball (similar to Pong): ball moves along baseline from player 1 to player 2
- Ball terminates when it hits baseline or goes out of bounds
- Rally ends when player commits unforced error or ball goes dead

## State Space
- `x_ball`: ball position on baseline $[0, L]$ (L = baseline length)
- `v_ball`: ball velocity (direction toward player 1 or 2)
- `x_p1`, `x_p2`: player positions on baseline
- `last_shot_quality`: [forehand, backhand, unknown] (inferred from last action)

## Action Space
- Move left/right/stay
- Choose shot type: [aggressive, defensive, target_opponent]
- **Effect with noise**: player intends position $x_{target}$ but hits position $x_{target} + \mathcal{N}(0, \sigma_{precision})$
  - $\sigma_{precision}$ depends on shot type and player skill

## Player Models

### Option A: Aggregate Skill
- Single parameter `skill ∈ [0, 1]` governing:
  - Movement speed (how fast they reach target position)
  - Shot precision $\sigma_{precision} = (1 - skill) \cdot \sigma_{max}$
  - Unforced error probability $p_{error}(skill)$ decreasing in skill
  
### Option B: Shot-Type Breakdown
- Separate skill for forehand vs backhand: `skill_{FH}`, `skill_{BH}`
- Each shot has inherent error rate depending on type
- Strategy must learn to exploit weak side

### Option C: Asymmetric (Recommended for Start)
- Each player has fixed skill profile: `skill, prefer_forehand_prob`
- Forehand error rate: $p_{FH}$; backhand error rate: $p_{BH}$ with $p_{BH} > p_{FH}$
- Player strategy learns when to move opponent to backhand

## Reward Function

**Per rally**:
- +1: win rally (opponent error)
- -1: lose rally (own error)
- Small per-step penalty: $-0.01 \cdot \text{action\_cost}$ (to prefer simpler strategies)

**Alternative**: shape reward by shot difficulty
- Large reward for winning against high-skill opponent
- Small penalty for winning against low-skill opponent (discourage relying on opponent mistakes)

## Key Assumptions
1. Both players know opponent skill (perfect information)
   - **Relax later**: add learning component to estimate opponent skill from play
2. Deterministic player positions (no lag in reaching target)
3. No multi-rally memory (state reset per rally)

## Questions to Resolve
- What is ball physics? Constant velocity? Linear deceleration?
- Does shot placement distribution matter? (target center vs edge)
- Should we model momentum / set/match context, or just rally-by-rally?
- Train single agent vs two agents (self-play)?
