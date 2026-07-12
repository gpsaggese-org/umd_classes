# Decision-Making Problem Categories: Examples & Solutions

Taxonomy of decision-making problems organized by key structural dimensions.
Each category shows concrete examples and key solution algorithms.

## Structural Dimensions Overview

Decision-making problems vary along **10 orthogonal dimensions**:
- **Observability**: What information is available to the agent
  - Full (MDP) ← → Partial (POMDP) ← → Hidden/Noisy
- **Time Horizon**: Planning window and reward accumulation
  - One-step ← → Multi-step (finite) ← → Infinite (discounted)
- **Action Space**: Structure of available decisions
  - Discrete ← → Continuous ← → Hybrid (mixed)
- **Multi-Agent**: Number and objectives of decision-makers
  - Single-agent ← → Multi-agent (cooperative/competitive/mixed)
- **Information Structure**: Symmetry and knowledge distribution
  - Perfect info ← → Imperfect info ← → Asymmetric
- **Model Availability**: Access to world model/dynamics
  - Model-based ← → Model-free ← → Hybrid
- **Update Mechanism**: When and how learning occurs
  - Online ← → Batch ← → Replay-based
- **Solution Concept**: How policy is represented/optimized
  - Value-based ← → Policy-based ← → Actor-Critic ← → Search
- **Optimality Criterion**: Policy structure and goal
  - Deterministic ← → Stochastic; Optimal ← → Approximate
- **Scalability**: State/action space size and representation
  - Tabular ← → Linear FA ← → Deep NN

## 1. Observability: Full Vs. Partial

### 1A. Fully Observable (MDP)

Agent sees complete state; all needed information available each step

- **Example: Tic-Tac-Toe**
  - Board state fully visible to both players
  - All moves and outcomes deterministic and known
  - Perfect information game
- **Algorithms**: Q-Learning, SARSA, Value Iteration, Policy Iteration, MCTS

### 1B. Partially Observable (POMDP)

Observations don't uniquely determine state; must maintain belief state (probability distribution)

- **Example: Robot Localization**
  - Robot receives noisy sensor readings (how far to walls, objects)
  - Doesn't know exact location; multiple positions consistent with observations
  - Must track probability distribution over possible locations
- **Algorithms**: Particle Filtering, Kalman Filter, POMCP (Partially Observable Monte Carlo Planning), Belief Planning

### 1C. Stochastic Observations with Hidden State

Environment has hidden state; observations are noisy/corrupted

- **Example: Weather Prediction from Noisy Thermometer**
  - True weather has hidden state (hot/cold/rainy)
  - Observe thermometer reading, but sensor is noisy
  - Need to infer hidden state from noisy observations over time
- **Algorithms**: Kalman Filter (linear Gaussian), Extended/Unscented Kalman Filter (nonlinear), Hidden Markov Models, Particle Filters

## 2. Time Horizon: One-Step Vs. Multi-Step

### 2A. One-Step / Myopic Decision

Optimize immediate reward only; no consideration of future

- **Example: Email Spam Filter (Per-Email Classification)**
  - Classify email as spam/not-spam
  - Decision affects only that email; no long-term consequences
  - Optimize accuracy on current email
- **Algorithms**: Greedy, ε-Greedy, UCB, Thompson Sampling, Contextual Bandits

### 2B. Multi-Step Lookahead (Finite Horizon)

Consider future consequences over fixed horizon

- **Example: Chess Move Selection (20 moves ahead)**
  - Current move affects board state for next moves
  - Cannot evaluate single move in isolation
  - Need to lookahead 20+ moves to find good strategy
- **Algorithms**: Minimax, Alpha-Beta Pruning, A*, RRT (Rapidly-exploring Random Trees), MCTS

### 2C. Infinite Horizon (Discounted)

Long-term optimization; infinite horizon with discount factor γ ∈ [0,1)

- **Example: Portfolio Management**
  - Allocate investments today to maximize wealth forever
  - Future rewards discounted: γ^t reduces weight of distant rewards
  - Stationary optimal policy (doesn't change over time)
- **Algorithms**: Q-Learning, SARSA, Value Iteration, Policy Iteration, Actor-Critic methods, Deep RL (DQN, PPO, SAC)

### 2D. Episodic / Finite Horizon

Fixed episode length T; sum undiscounted rewards (or discounted differently)

- **Example: Video Game Level**
  - Game episode lasts exactly 300 steps (frames)
  - Optimize total score over that episode
  - After 300 steps, episode ends
- **Algorithms**: Monte Carlo Methods, MCTS, Policy Gradient (REINFORCE), Episodic RL variants

## 3. Action Space: Discrete Vs. Continuous

### 3A. Discrete Actions

Finite set of actions {a₁, a₂, ..., aₙ}; can enumerate and compare

- **Example: Traffic Light Controller**
  - Actions: {Green (NS), Green (EW), Yellow, Red}
  - Discrete choices; can try each one
  - Small branching factor
- **Algorithms**: Q-Learning, DQN, MCTS, Minimax, Value Iteration (when feasible)

### 3B. Continuous Actions

Action space ℝⁿ (uncountably infinite); cannot enumerate

- **Example: Robot Arm Control**
  - Continuous joint angles (θ₁, θ₂, θ₃) ∈ ℝ³
  - Infinite possible actions
  - Must learn function, not table
- **Algorithms**: Policy Gradient (REINFORCE), Actor-Critic (A3C, SAC), DDPG, TD3, PPO (with continuous output), Evolutionary Strategies

### 3C. Hybrid (Mixed Discrete-Continuous)

Some actions discrete, some continuous

- **Example: Robotic Gripper with Mode Selection**
  - Discrete: Which object to grasp (5 objects)
  - Continuous: Grasp force and angle
  - Two-level decision
- **Algorithms**: Branching DQN, Hierarchical RL, Multi-task Learning with shared base

## 4. Multi-Agent Interaction

### 4A. Single-Agent

One decision-maker, one objective; no strategic interaction

- **Example: Personalized Movie Recommendation**
  - System recommends movies to single user
  - No other agents; no strategic interaction
  - Optimize user satisfaction
- **Algorithms**: All standard RL algorithms (Q-Learning, PPO, DQN, etc.)

### 4B. Multi-Agent Cooperative

Multiple agents, shared objective; must coordinate

- **Example: Warehouse Robot Team**
  - 5 robots move packages together
  - Shared goal: minimize delivery time
  - Robots must coordinate to avoid collisions, deadlocks
  - One reward signal for whole team
- **Algorithms**: MAAC (Multi-Agent Actor-Critic), MAPPO (Multi-Agent PPO), QMIX, CommNet, MADDPG

### 4C. Multi-Agent Competitive

Agents with conflicting objectives; game theory, Nash equilibrium

- **Example: Chess Match**
  - Two players, zero-sum game (one wins, one loses)
  - Each player wants to maximize own score
  - Optimal solution is Nash equilibrium (neither can unilaterally improve)
- **Algorithms**: Minimax with Alpha-Beta Pruning, Self-Play, Nash Equilibrium Solvers, Counterfactual Regret Minimization (CFR)

## 5. Model Knowledge: Model-Based Vs. Model-Free

### 5A. Model-Based (Planning)

Agent has or learns transition model p(s'|s,a) and reward r(s,a); uses it to plan

- **Example: GPS Route Planner**
  - Model: road network, travel times, traffic patterns
  - Uses model to find fastest route without driving all routes
  - Sample-efficient
- **Algorithms**: Value/Policy Iteration, Dyna-Q, MCTS, AlphaGo, MuZero

### 5B. Model-Free (Learning)

No model; agent learns directly from experience

- **Example: Learning to Play Atari from Pixels**
  - No access to game code or physics
  - Learns Q-values directly from screen + rewards
  - Trial-and-error
- **Algorithms**: Q-Learning, SARSA, Policy Gradient (REINFORCE), Actor-Critic, DQN, PPO, SAC, A3C

## 6. State & Action Space Size: Scalability

### 6A. Small Tabular Problem

|S| and |A| small enough to store in table (e.g., <10,000 states)

- **Example: Simple Grid World**
  - 10x10 grid = 100 states
  - 4 actions (up, down, left, right)
  - Can store full Q-table
- **Algorithms**: Tabular Q-Learning, Tabular Value Iteration, Tabular Policy Iteration, MCTS

### 6B. Medium: Linear Function Approximation

|S| or |A| too large for table; use linear function

- **Example: Adaptive Auction Bidding**
  - State features: [price_history, competitor_bids, budget_remaining, ...]
  - Too many unique combinations for table
  - Use linear function: V(s) = w·φ(s)
- **Algorithms**: Q-Learning with FA, SARSA with FA, Linear Bandits, Contextual Bandits, Least-Squares Temporal Difference

### 6C. Large: Deep Neural Networks

High-dimensional state (images, speech) or large action space; use deep NN

- **Example: Self-Driving Car**
  - State: camera image (1920×1440×3 pixels = huge)
  - Action: continuous steering/acceleration
  - Need deep network to extract features
- **Algorithms**: DQN (and variants: Double, Dueling, Rainbow), Policy Gradient with NN, A3C, PPO, TRPO, SAC, TD3, Evolutionary Strategies

## Quick Reference: Problem Type → Algorithm

- **Full observability, small state**
  - Example: Tic-tac-toe
  - Algorithms: Q-Learning (tabular), Value Iteration, MCTS
- **Full observability, large state (pixels)**
  - Example: Atari game
  - Algorithms: DQN, A3C, PPO
- **Partially observable**
  - Example: Robot localization
  - Algorithms: Particle Filter, POMCP, HMM
- **Continuous control, known model**
  - Example: Trajectory optimization
  - Algorithms: MPC (Model Predictive Control), iLQR
- **Continuous control, unknown model**
  - Example: Robotic arm
  - Algorithms: PPO, SAC, DDPG, TD3
- **Discrete actions, exploration**
  - Example: Web ads (bandit)
  - Algorithms: UCB, Thompson Sampling, ε-Greedy
- **Game playing (perfect info)**
  - Example: Chess
  - Algorithms: Minimax, Alpha-Beta, MCTS, AlphaZero
- **Game playing (imperfect info)**
  - Example: Poker
  - Algorithms: CFR, Nash Solver
- **Multi-agent cooperative**
  - Example: Warehouse robots
  - Algorithms: MAAC, MAPPO, QMIX
- **Multi-agent competitive**
  - Example: Video game enemy AI
  - Algorithms: Self-Play, Nash Learning

## Key Takeaways

- **Observable vs. Partial**
  - Full observability enables direct value/policy learning
  - Partial observability requires belief state tracking
- **Time Horizon**
  - Myopic (bandit) → simple greedy/UCB
  - Multi-step finite → lookahead search
  - Infinite → stationary policy with discounting
- **Action Space**
  - Discrete → enumerate
  - Continuous → learn policy distribution
  - Mixed → hierarchical or branching policies
- **Agents**
  - Single → standard RL
  - Multi-cooperative → shared reward, coordinated learning
  - Multi-competitive → game theory, Nash equilibrium
- **Model**
  - Model-based (planning): sample-efficient but requires accurate model
  - Model-free (learning): asymptotically optimal but needs more data
- **Scalability**
  - Tabular → small problems only
  - Linear FA → medium
  - Deep NN → large, high-dimensional spaces
