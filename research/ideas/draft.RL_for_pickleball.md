# RL for Pickleball Strategy

## Objective
- Model baseline rallies using RL to learn optimal strategies for shot selection
  and court positioning

## Approximation 1: 1D Simplified Game

**Game Model**
- 1D analog of pickleball (similar to Pong)
  - Ball moves along baseline from player 1 to player 2
  - We don't simulate the trajectory of the ball
  - It's like a multi-turn game
    - Player 1
      - Aim ball to position $x$
      - Move to position $x$
    - Player 2
      - Move from position $x_2(t)$ to ball, assuming has enough time given the
        their speed and the distance of the ball
      - Aim ball to position $x$
- Point terminates when:
  - a player commits an unforced error
  - the ball is a winner (i.e., one player can't reach it)
  - the ball is out (due to stochastic error)

- The ball has a fixed speed so the time the player has to move depends on
  the distance

## State Space
- `x_ball`: ball position on baseline $[0, L]$ (L = baseline length)
- `x_p1`, `x_p2`: player positions on baseline

## Action Space
- Move to $x$
- Effect with noise: player intends position $x_{target}$ but hits position
  $$x_{target} + \mathcal{N}(0, \sigma_{precision})$$
  - $\sigma_{precision}$ depends on player skill

## Player Models

### Option A: Aggregate Skill
- Movement speed $\speed$ (how fast they reach target position)
- Shot precision $\sigma_{precision}$
- Unforced error probability $p_{error}$ decreasing in skill
  
### Option B: Shot-Type Breakdown
- Separate skill for forehand vs backhand
- Each shot has inherent error rate and precision depending on type
  - Forehand error rate: $p_{FH}$; backhand error rate: $p_{BH}$
- Strategy must learn to exploit weak side

## Reward Function

**Per rally**:
- +1: win rally (opponent error)
- -1: lose rally (own error)
- Small per-step penalty: $-0.01 \cdot \text{action\_cost}$ (to prefer simpler strategies)

## Key Assumptions
1. Both players know opponent skill (perfect information)
   - **Relax later**: add learning component to estimate opponent skill from play
2. Deterministic player positions
3. No multi-rally memory (state reset per rally)

- Train single agent vs two agents (self-play)
