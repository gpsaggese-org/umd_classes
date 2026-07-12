# Decision-Making Problem Categories: Examples & Solutions

Taxonomy of decision-making problems organized by key structural dimensions.
Each category shows concrete examples and key solution algorithms.

## Structural Dimensions Overview

Decision-making problems vary along 10 _orthogonal dimensions_:

- _Observability_: What information is available to the agent
  - Full (MDP – Markov Decision Process): Agent observes complete state; all needed information available
    each step
  - Partial (POMDP – Partially Observable Markov Decision Process): Observations don't uniquely determine state; must maintain
    belief state
  - Hidden/Noisy: Environment has hidden state; observations are
    corrupted/stochastic
  
- _Time Horizon_: Planning window and reward accumulation
  - One-step (Bandit): Optimize immediate reward only (greedy decisions)
  - Multi-step (finite): Consider consequences over fixed lookahead horizon
  - Infinite (discounted): Long-term optimization with discount factor $\gamma$
  
- _Action Space_: Structure of available decisions
  - Discrete: Finite set of actions (can enumerate)
  - Continuous: Action space $\mathbb{R}^n$ (uncountably infinite)
  - Hybrid (mixed): Some actions discrete, some continuous
  
- _Multi-Agent_: Number and objectives of decision-makers
  - Single-agent: One decision-maker, one objective → no strategic interaction
  - Cooperative: Multiple agents, shared objective → must coordinate
  - Competitive/Mixed: Agents with conflicting or mixed objectives; game theory
    applies
  
- _Information Structure_: Symmetry and knowledge distribution
  - Perfect info: All players know all relevant information
  - Imperfect info: Players have asymmetric or hidden information
  - Asymmetric: Players have fundamentally different information sets and
    capabilities
  
- _Model Availability_: Access to world model/dynamics
  - Model-based: Agent has (or learns) transition model $p(s'|s,a)$ (state transition probability) and reward
    $r(s,a)$ (reward function)
  - Model-free: Agent learns directly from experience; no explicit model
  - Hybrid: Learns approximate model or uses model selectively
  
- _Update Mechanism_: When and how learning occurs
  - Online: Agent learns and acts in real-time; single trajectory
  - Batch: Agent trains on fixed dataset; replay or offline learning
  - Replay-based: Agent stores experiences and replays for training
  
- _Solution Concept_: How policy is represented/optimized
  - Value-based: Learn state or state-action values; derive policy from values
  - Policy-based: Learn policy directly without explicit value function
  - Actor-Critic: Combine value function and policy learning
  - Search/Planning: Use tree search or planning to find optimal actions
  
- _Optimality Criterion_: Policy structure and goal
  - Deterministic: Policy outputs single action per state
  - Stochastic: Policy outputs probability distribution over actions
  - Optimal: Find best possible policy (exact or approximate)
  - Approximate: Satisfice with good-enough policy; bounded suboptimality
    acceptable
  
- _Scalability_: State/action space size and representation
  - Tabular: |S| and |A| small enough for lookup tables (<10k states)
  - Linear FA (Function Approximation): Medium-scale; use linear function approximation V(s) = w·φ(s)
  - Deep NN (Neural Network): Large/high-dimensional; use deep neural networks

## 1. Observability: Full Vs. Partial

### 1A. Fully Observable (MDP)

- **Setup**:
  - Agent sees complete state
  - All needed information available each step

- **Example**: Tic-Tac-Toe
  - Board state fully visible to both players
  - All moves and outcomes deterministic and known
  - Perfect information game

- **Algorithms**:
  - Q-Learning
  - SARSA (State-Action-Reward-State-Action)
  - Value Iteration
  - Policy Iteration
  - MCTS (Monte Carlo Tree Search)

### 1B. Partially Observable (POMDP)

- **Setup**:
  - Observations don't uniquely determine state
  - Must maintain belief state (probability distribution)

- **Example**: Robot Localization
  - Robot receives noisy sensor readings (how far to walls, objects)
  - Doesn't know exact location, but multiple positions consistent with
    observations
  - Must track probability distribution over possible locations

- **Algorithms**:
  - Particle Filtering
  - Kalman Filter
  - POMCP (Partially Observable Monte Carlo Planning)
  - Belief State Planning

### 1C. Stochastic Observations with Hidden State

- **Setup**:
  - Environment has hidden state
  - Observations are noisy/corrupted

- **Example**: Weather Prediction from Noisy Thermometer
  - True weather has hidden state (hot/cold/rainy)
  - Observe thermometer reading, but sensor is noisy
  - Need to infer hidden state from noisy observations over time

- **Algorithms**:
  - Kalman Filter (linear Gaussian)
  - Extended/Unscented Kalman Filter (nonlinear)
  - Hidden Markov Models
  - Particle Filters

## 2. Time Horizon: One-Step Vs. Multi-Step

### 2A. One-Step / Myopic Decision

- **Setup**:
  - Optimize immediate reward only
  - No consideration of future

- **Example**: Email Spam Filter (Per-Email Classification)
  - Classify email as spam/not-spam
  - Decision affects only that email; no long-term consequences
  - Optimize accuracy on current email

- **Algorithms**:
  - Greedy
  - ε-Greedy (Epsilon-Greedy)
  - UCB (Upper Confidence Bound)
  - Thompson Sampling
  - Contextual Bandits

### 2B. Multi-Step Lookahead (Finite Horizon)

- **Setup**:
  - Consider future consequences over fixed horizon

- **Example**: Chess Move Selection (20 moves ahead)
  - Current move affects board state for next moves
  - Cannot evaluate single move in isolation
  - Need to lookahead 20+ moves to find good strategy

- **Algorithms**:
  - Minimax
  - Alpha-Beta Pruning
  - A* (A-Star)
  - RRT (Rapidly-exploring Random Tree)
  - MCTS (Monte Carlo Tree Search)

### 2C. Infinite Horizon (Discounted)

- **Setup**:
  - Long-term optimization
  - Infinite horizon with discount factor $\gamma \in [0, 1)$

- **Example**: Portfolio Management
  - Allocate investments today to maximize wealth forever
  - Future rewards discounted: γ^t reduces weight of distant rewards
  - Stationary optimal policy (doesn't change over time)

- **Algorithms**:
  - Q-Learning
  - SARSA (State-Action-Reward-State-Action)
  - Value Iteration
  - Policy Iteration
  - Actor-Critic methods
  - Deep RL: DQN (Deep Q-Network), PPO (Proximal Policy Optimization), SAC (Soft Actor-Critic)

### 2D. Episodic / Finite Horizon

- **Setup**:
  - Fixed episode length T
  - Sum undiscounted rewards (or discounted differently)

- **Example**: Video Game Level
  - Game episode lasts exactly 300 steps (frames)
  - Optimize total score over that episode
  - After 300 steps, episode ends

- **Algorithms**:
  - Monte Carlo Methods
  - MCTS (Monte Carlo Tree Search)
  - Policy Gradient (REINFORCE)
  - Episodic RL variants

## 3. Action Space: Discrete Vs. Continuous

### 3A. Discrete Actions

- **Setup**:
  - Finite set of actions {a₁, a₂, ..., aₙ}
  - Can enumerate and compare

- **Example**: Traffic Light Controller
  - Actions: {Green, Yellow, Red}
  - Discrete choices; can try each one
  - Small branching factor

- **Algorithms**:
  - Q-Learning
  - DQN (Deep Q-Network)
  - MCTS (Monte Carlo Tree Search)
  - Minimax
  - Value Iteration (when feasible)

### 3B. Continuous Actions

- **Setup**:
  - Action space $\mathbb{R}^n$ (uncountably infinite)
  - Cannot enumerate

- **Example**: Robot Arm Control
  - Continuous joint angles $(\theta_1, \theta_2, \theta_3) \in \mathbb{R}^3$
  - Infinite possible actions
  - Must learn function, not table

- **Algorithms**:
  - Policy Gradient (REINFORCE)
  - Actor-Critic: A3C (Asynchronous Advantage Actor-Critic), SAC (Soft Actor-Critic)
  - DDPG (Deep Deterministic Policy Gradient)
  - TD3 (Twin Delayed DDPG)
  - PPO (Proximal Policy Optimization, with continuous output)
  - Evolutionary Strategies

### 3C. Hybrid (Mixed Discrete-Continuous)

- **Setup**:
  - Some actions discrete
  - Some actions continuous

- **Example**: Robotic Gripper with Mode Selection
  - Discrete: Which object to grasp (5 objects)
  - Continuous: Grasp force and angle
  - Two-level decision

- **Algorithms**:
  - Branching DQN (Deep Q-Network)
  - Hierarchical RL (Reinforcement Learning)
  - Multi-task Learning with shared base

## 4. Multi-Agent Interaction

### 4A. Single-Agent

- **Setup**:
  - One decision-maker, one objective
  - No strategic interaction

- **Example**: Personalized Movie Recommendation
  - System recommends movies to single user
  - No other agents; no strategic interaction
  - Optimize user satisfaction

- **Algorithms**:
  - Q-Learning
  - PPO (Proximal Policy Optimization)
  - DQN (Deep Q-Network)
  - SARSA (State-Action-Reward-State-Action)
  - Actor-Critic

### 4B. Multi-Agent Cooperative

- **Setup**:
  - Multiple agents, shared objective
  - Must coordinate

- **Example**: Warehouse Robot Team
  - 5 robots move packages together
  - Shared goal: minimize delivery time
  - Robots must coordinate to avoid collisions, deadlocks
  - One reward signal for whole team

- **Algorithms**:
  - MAAC (Multi-Agent Actor-Critic)
  - MAPPO (Multi-Agent Proximal Policy Optimization)
  - QMIX (Q-value Mixing)
  - CommNet (Communication Network)
  - MADDPG (Multi-Agent Deep Deterministic Policy Gradient)

### 4C. Multi-Agent Competitive

- **Setup**:
  - Agents with conflicting objectives
  - Game theory, Nash equilibrium applies

- **Example**: Chess Match
  - Two players, zero-sum game (one wins, one loses)
  - Each player wants to maximize own score
  - Optimal solution is Nash equilibrium (neither can unilaterally improve)

- **Algorithms**:
  - Minimax with Alpha-Beta Pruning
  - Self-Play
  - Nash Equilibrium Solvers
  - CFR (Counterfactual Regret Minimization)

## 5. Model Knowledge: Model-Based Vs. Model-Free

### 5A. Model-Based (Planning)

- **Setup**:
  - Agent has or learns transition model p(s'|s,a) and reward r(s,a)
  - Uses model to plan

- **Example**: GPS Route Planner
  - Model: road network, travel times, traffic patterns
  - Uses model to find fastest route without driving all routes
  - Sample-efficient

- **Algorithms**:
  - Value/Policy Iteration
  - Dyna-Q
  - MCTS (Monte Carlo Tree Search)
  - AlphaGo
  - MuZero

### 5B. Model-Free (Learning)

- **Setup**:
  - No model available
  - Agent learns directly from experience

- **Example**: Learning to Play Atari from Pixels
  - No access to game code or physics
  - Learns Q-values directly from screen + rewards
  - Trial-and-error

- **Algorithms**:
  - Q-Learning
  - SARSA (State-Action-Reward-State-Action)
  - Policy Gradient (REINFORCE)
  - Actor-Critic
  - DQN (Deep Q-Network)
  - PPO (Proximal Policy Optimization)
  - SAC (Soft Actor-Critic)
  - A3C (Asynchronous Advantage Actor-Critic)

## 6. State & Action Space Size: Scalability

### 6A. Small Tabular Problem

- **Setup**:
  - |S| and |A| small enough to store in table (e.g., <10,000 states)

- **Example**: Simple Grid World
  - 10x10 grid = 100 states
  - 4 actions (up, down, left, right)
  - Can store full Q-table

- **Algorithms**:
  - Tabular Q-Learning
  - Tabular Value Iteration
  - Tabular Policy Iteration
  - MCTS (Monte Carlo Tree Search)

### 6B. Medium: Linear Function Approximation

- **Setup**:
  - |S| or |A| too large for table
  - Use linear function approximation

- **Example**: Adaptive Auction Bidding
  - State features: [price_history, competitor_bids, budget_remaining, ...]
  - Too many unique combinations for table
  - Use linear function: V(s) = w·φ(s)

- **Algorithms**:
  - Q-Learning with FA (Function Approximation)
  - SARSA (State-Action-Reward-State-Action) with FA
  - Linear Bandits
  - Contextual Bandits
  - Least-Squares Temporal Difference (LSTD)

### 6C. Large: Deep Neural Networks

- **Setup**:
  - High-dimensional state (images, speech)
  - Large action space; use deep NN

- **Example**: Self-Driving Car
  - State: camera image (1920×1440×3 pixels = huge)
  - Action: continuous steering/acceleration
  - Need deep network to extract features

- **Algorithms**:
  - DQN (Deep Q-Network, variants: Double, Dueling, Rainbow)
  - Policy Gradient with NN (Neural Network)
  - A3C (Asynchronous Advantage Actor-Critic)
  - PPO (Proximal Policy Optimization)
  - TRPO (Trust Region Policy Optimization)
  - SAC (Soft Actor-Critic)
  - TD3 (Twin Delayed DDPG)
  - Evolutionary Strategies

## Quick Reference: Problem Type → Algorithm

- **Full observability, small state**
  - Example: Tic-tac-toe
  - Algorithms: Q-Learning (tabular), Value Iteration, MCTS (Monte Carlo Tree Search)
- **Full observability, large state (pixels)**
  - Example: Atari game
  - Algorithms: DQN (Deep Q-Network), A3C (Asynchronous Advantage Actor-Critic), PPO (Proximal Policy Optimization)
- **Partially observable**
  - Example: Robot localization
  - Algorithms: Particle Filter, POMCP (Partially Observable Monte Carlo Planning), HMM (Hidden Markov Model)
- **Continuous control, known model**
  - Example: Trajectory optimization
  - Algorithms: MPC (Model Predictive Control), iLQR (iterative Linear Quadratic Regulator)
- **Continuous control, unknown model**
  - Example: Robotic arm
  - Algorithms: PPO (Proximal Policy Optimization), SAC (Soft Actor-Critic), DDPG (Deep Deterministic Policy Gradient), TD3 (Twin Delayed DDPG)
- **Discrete actions, exploration**
  - Example: Web ads (bandit)
  - Algorithms: UCB (Upper Confidence Bound), Thompson Sampling, ε-Greedy (Epsilon-Greedy)
- **Game playing (perfect info)**
  - Example: Chess
  - Algorithms: Minimax, Alpha-Beta, MCTS (Monte Carlo Tree Search), AlphaZero
- **Game playing (imperfect info)**
  - Example: Poker
  - Algorithms: CFR (Counterfactual Regret Minimization), Nash Solver
- **Multi-agent cooperative**
  - Example: Warehouse robots
  - Algorithms: MAAC (Multi-Agent Actor-Critic), MAPPO (Multi-Agent Proximal Policy Optimization), QMIX (Q-value Mixing)
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
  - Single → standard RL (Reinforcement Learning)
  - Multi-cooperative → shared reward, coordinated learning
  - Multi-competitive → game theory, Nash equilibrium
- **Model**
  - Model-based (planning): sample-efficient but requires accurate model
  - Model-free (learning): asymptotically optimal but needs more data
- **Scalability**
  - Tabular → small problems only
  - Linear FA (Function Approximation) → medium
  - Deep NN (Neural Network) → large, high-dimensional spaces
