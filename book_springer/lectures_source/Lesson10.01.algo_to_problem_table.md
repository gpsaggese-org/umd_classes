# Algorithm to Problem Mapping: Which Algorithm Solves What?

## Core Value-based RL Algorithms

| Algorithm | Problem Dimensions | Suitable For | Key Characteristics |
|---|---|---|---|
| **Q-Learning** | Fully observable, discrete/continuous actions, infinite horizon, model-free, tabular/FA | Standard MDPs, learning from experience | Off-policy, sample-efficient, handles discrete actions well |
| **SARSA** | Fully observable, discrete actions, infinite horizon, model-free, online learning | Real-time decision-making, online systems | On-policy, learns from sequential experience |
| **Value Iteration** | Fully observable, known model, finite/infinite horizon, discrete actions | Planning with known environment model | Guaranteed convergence, model-required |
| **Policy Iteration** | Fully observable, known model, infinite horizon, discrete actions | Planning with exact model | Iterative policy evaluation and improvement |
| **Double DQN** | Fully observable, discrete actions, large state space (deep NN) | High-dimensional problems with overestimation issues | Reduces overestimation in Q-values |
| **Dueling DQN** | Fully observable, discrete actions, large state space (deep NN) | Value-action decomposition problems | Separates value and advantage streams |
| **DQN (Deep Q-Network)** | Fully observable, discrete actions, large state space (deep NN), model-free | Atari games, vision-based control, high-dimensional inputs | Experience replay, target networks, handles images |

## Policy-based RL Algorithms

| Algorithm | Problem Dimensions | Suitable For | Key Characteristics |
|---|---|---|---|
| **REINFORCE** | Any observability, continuous/discrete actions, episodic horizon, model-free | Policy gradient learning, stochastic policies | On-policy, high variance |
| **Policy Gradient** | Any observability, continuous actions, infinite/finite horizon | Continuous control, differentiable policies | On-policy, stable gradient estimation |
| **PPO (Proximal Policy Optimization)** | Any observability, continuous/discrete actions, infinite horizon, model-free | Robotic control, game playing, continuous control | On-policy, stable, sample-efficient |
| **TRPO (Trust Region Policy Optimization)** | Continuous actions, infinite horizon, model-free | Complex continuous control tasks | Stable updates with trust region |
| **Natural Policy Gradient** | Continuous actions, infinite horizon | Policy optimization with natural gradient | Fisher information metric |
| **Evolutionary Strategies** | Hybrid/continuous actions, finite horizon | Black-box optimization, continuous control | Gradient-free, population-based |

## Actor-Critic Algorithms

| Algorithm | Problem Dimensions | Suitable For | Key Characteristics |
|---|---|---|---|
| **Actor-Critic (General)** | Any observability, continuous/discrete actions, infinite horizon | Reduces policy gradient variance | Combines value and policy learning |
| **A2C (Advantage Actor-Critic)** | Fully observable, continuous/discrete actions, episodic | Parallel environments, sample efficiency | Synchronous updates, reduced variance |
| **A3C (Asynchronous Advantage Actor-Critic)** | Fully observable, continuous/discrete actions, infinite horizon, online | Parallel training, continuous learning | Asynchronous updates, on-policy |
| **SAC (Soft Actor-Critic)** | Fully observable, continuous actions, infinite horizon, model-free | Continuous control, exploration-exploitation | Maximum entropy framework, stable |
| **DDPG (Deep Deterministic Policy Gradient)** | Fully observable, continuous actions, infinite horizon, deterministic policy | Continuous control with deterministic actions | Off-policy, sample-efficient |
| **TD3 (Twin Delayed DDPG)** | Fully observable, continuous actions, infinite horizon, deterministic policy | High-dimensional continuous control | Reduces overestimation, delayed updates |

## Planning and Search Algorithms

| Algorithm | Problem Dimensions | Suitable For | Key Characteristics |
|---|---|---|---|
| **MCTS (Monte Carlo Tree Search)** | Any observability, discrete/continuous actions, finite horizon, known/unknown model | Perfect/imperfect information games, planning | Asymptotically optimal, lookahead |
| **Minimax** | Perfect information, discrete actions, finite horizon, zero-sum games | Game playing with perfect info | Optimal play via backward induction |
| **Alpha-Beta Pruning** | Perfect information, discrete actions, finite horizon | Game playing (e.g., Chess) | Efficient Minimax with pruning |
| **Negamax** | Perfect information, discrete actions, finite horizon | Game playing with alternating scores | Simplified Minimax variant |
| **A*** | Discrete actions, pathfinding, known cost model | Robot navigation, trajectory planning | Optimal path with heuristics |
| **MPC (Model Predictive Control)** | Known model, continuous actions, finite horizon | Real-time control with explicit models | Receding horizon planning |
| **iLQR (iterative Linear Quadratic Regulator)** | Continuous actions, known model, trajectory optimization | Smooth trajectory optimization | Local optimal trajectory |
| **RRT (Rapidly-exploring Random Tree)** | Continuous actions, high-dimensional spaces, finite horizon | Motion planning, robot path planning | Probabilistically complete |

## Deep RL Algorithms

| Algorithm | Problem Dimensions | Suitable For | Key Characteristics |
|---|---|---|---|
| **DQN with Experience Replay** | Fully observable, discrete actions, large state space | Atari, vision-based games | Decorrelates samples via buffering |
| **Prioritized Experience Replay (PER)** | Fully observable, discrete actions, large state space | Important transition sampling | Prioritizes high-error transitions |
| **Hindsight Experience Replay (HER)** | Fully observable, discrete/continuous, goal-conditioned | Goal-reaching tasks with sparse rewards | Relabels failed trajectories |
| **Rainbow DQN** | Fully observable, discrete actions, large state space | Atari games, vision-based control | Combines multiple DQN improvements |
| **AlphaGo** | Perfect information, discrete actions, finite horizon, model-based + search | Complex game playing (Go) | Neural networks + MCTS |
| **AlphaZero** | Perfect information, discrete actions, finite horizon, self-play | Perfect-info games (Chess, Shogi, Go) | Self-play + neural networks + MCTS |
| **MuZero** | Any observability, discrete/continuous actions, model-free yet planning | General decision-making, model-free planning | Learns value without explicit model |

## Bandit Algorithms

| Algorithm | Problem Dimensions | Suitable For | Key Characteristics |
|---|---|---|---|
| **ε-Greedy** | One-step decision, discrete actions, immediate reward | Simple exploration-exploitation | Exploration with fixed probability |
| **Upper Confidence Bound (UCB)** | One-step decision, discrete actions, bandit problem | Exploration-exploitation with optimism | Optimistic action selection |
| **Thompson Sampling** | One-step decision, discrete/stochastic actions, uncertainty | Bayesian bandits, probabilistic decision | Posterior sampling for exploration |
| **Contextual Bandits** | One-step decision with state/context, discrete actions | Recommendations with context | Context-dependent action selection |
| **Linear Bandits** | Medium state space with linear structure, one-step | Feature-based bandits | Linear value functions |

## Partially Observable / Hidden State Algorithms

| Algorithm | Problem Dimensions | Suitable For | Key Characteristics |
|---|---|---|---|
| **Hidden Markov Models (HMM)** | Hidden state, stochastic observations, sequential decision | Speech recognition, state inference | Probabilistic state representation |
| **Particle Filtering** | Partially observable, hidden state, stochastic observations | Non-linear filtering, belief tracking | Non-parametric Bayesian filtering |
| **Kalman Filter** | Partially observable, linear-Gaussian dynamics | Tracking, localization with Gaussian noise | Optimal linear filtering |
| **Extended Kalman Filter (EKF)** | Partially observable, nonlinear dynamics, Gaussian noise | Nonlinear state estimation | Linearization of nonlinear models |
| **Unscented Kalman Filter (UKF)** | Partially observable, nonlinear dynamics | Nonlinear filtering without linearization | Unscented transform |
| **POMCP (Partially Observable Monte Carlo Planning)** | Partially observable, discrete actions, planning | Decision-making under partial observability | MCTS for POMDPs |
| **Belief-State Planning** | Partially observable, discrete actions, planning | Optimal planning under uncertainty | Planning over belief states |

## Game Theory & Multi-Agent Algorithms

| Algorithm | Problem Dimensions | Suitable For | Key Characteristics |
|---|---|---|---|
| **CFR (Counterfactual Regret Minimization)** | Imperfect information, discrete actions, multi-agent | Poker, imperfect-info games, Nash equilibrium | Regret minimization for games |
| **Regret Matching** | Imperfect information, multi-agent, game theory | Mixed-strategy equilibria | Minimizes regret over time |
| **Nash Solvers** | Competitive multi-agent, perfect/imperfect information | Finding Nash equilibria | Exact or approximate equilibrium |
| **Self-Play** | Competitive multi-agent, discrete/continuous actions | Game playing, competitive learning | Agents learn by playing each other |
| **Information-Set Abstraction** | Imperfect information, multi-agent | Large imperfect-info games | Reduces game tree size |
| **QMIX** | Multi-agent cooperative, discrete actions | Cooperative multi-agent systems | Decentralized execution via mixing |
| **MAPPO (Multi-Agent Proximal Policy Optimization)** | Multi-agent cooperative, continuous/discrete actions | Cooperative multi-agent control | Multi-agent PPO variant |
| **MAAC (Multi-Agent Actor-Critic)** | Multi-agent cooperative, continuous actions | Continuous cooperative control | Centralized training, decentralized execution |
| **MADDPG (Multi-Agent DDPG)** | Multi-agent competitive/cooperative, continuous actions | Mixed multi-agent scenarios | Multi-agent DDPG variant |
| **CommNet** | Multi-agent cooperative, communication | Cooperative agents with learning communication | Graph neural networks for coordination |

## Offline / Batch Learning Algorithms

| Algorithm | Problem Dimensions | Suitable For | Key Characteristics |
|---|---|---|---|
| **Batch Q-Learning** | Fully observable, discrete actions, offline dataset | Learning from logged data | Batch updates on fixed data |
| **Offline RL** | Any observability, discrete/continuous actions, offline data | Policy learning without environment interaction | Addresses distribution shift |
| **Behavior Cloning** | Offline learning, imitation | Learning from demonstrations | Supervised learning on expert data |
| **Conservative Q-Learning (CQL)** | Fully observable, offline data, discrete actions | Safe offline learning | Conservative value estimates |
| **Dyna-Q** | Model-free + model-based, planning | Combining real and simulated experience | Integrates learning and planning |

## Model-Based Algorithms

| Algorithm | Problem Dimensions | Suitable For | Key Characteristics |
|---|---|---|---|
| **Value/Policy Iteration** | Fully observable, known model, discrete actions | Planning with exact environment model | Guaranteed convergence |
| **Dyna-Q** | Model-based planning, discrete actions | Learning world model + planning | Simulates experience |
| **AlphaGo** | Model-based + search, perfect information | Complex planning with neural guidance | Neural network + MCTS combination |
| **MuZero** | Model-free yet planning, discrete/continuous | Learning implicit models for planning | Value-equivalent models |

## Hierarchical / Modular Algorithms

| Algorithm | Problem Dimensions | Suitable For | Key Characteristics |
|---|---|---|---|
| **Hierarchical RL** | Hybrid actions, multi-level decisions | Hierarchical decision-making | Options/skills framework |
| **Branching DQN** | Hybrid (discrete-continuous) actions | Two-stage action selection | Discrete then continuous |
| **Multi-task Learning** | Multiple related problems | Shared representation across tasks | Shared features, task-specific heads |

## Mechanism Design & Contract Theory

| Algorithm | Problem Dimensions | Suitable For | Key Characteristics |
|---|---|---|---|
| **Mechanism Design** | Asymmetric information, principal-agent problems | Contract design, incentive alignment | Mathematical design of institutions |
| **Bayesian Games** | Asymmetric information, uncertainty over types | Games with incomplete information | Belief hierarchies |
| **Signaling Equilibria** | Asymmetric information, sequential moves | Reputation, screening, signaling | Perfect Bayesian equilibrium |
| **Information-dependent Policies** | Asymmetric information | Policies that depend on information sets | Conditional on private information |

## Function Approximation Methods

| Algorithm | Problem Dimensions | Suitable For | Key Characteristics |
|---|---|---|---|
| **Linear Function Approximation (FA)** | Medium state space, feature-based | Scalable value learning | Linear value functions |
| **LSTD (Least Squares Temporal Difference)** | Medium state space, linear FA | Off-policy learning with FA | Least-squares solution |
| **Deep Neural Networks** | Large state space, high-dimensional inputs | Vision, complex feature learning | Universal function approximation |
| **Contextual Bandits** | One-step with context/features | Personalized recommendations | Feature-based action selection |
