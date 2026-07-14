# Algorithm Reference: Papers, Authors, Implementations

## Template

- Prefer arXiv links whenever available for direct access to preprints and
  published papers

- The citation format is
  ```
  Author(s), "Title" (Year) - arxiv.org/abs/1509.06461
  ```
  - If there are more than one author use the last name and "et al."
  - E.g.,
  ```
  Watkins et al., "Q-learning" (1992) - arxiv.org/abs/1509.06461
  ```

- The format for each algorithm is the following
  ```
  ### <topic>
  - **Short description**:
    - ...
  - **Key papers:**
    - Watkins et al., "Q-learning" (1992) - arxiv.org/abs/1509.06461
  - **Key Authors:**
    - Christopher Watkins, Peter Dayan
  - **Key Variants:**
    - van Hasselt et al., "Deep Reinforcement Learning with Double Q-learning" (2015) ...
  - **Python Packages:**
    - `stable-baselines3` (DQN variants)
    - `tensorflow-agents`
    - `pytorch-dqn` (custom implementations)
  ```
- Keep the references in reverse chronological order

## Core Value-Based RL Algorithms

### Q-Learning
- **Paper:** Watkins & Dayan, "Q-learning" (1992) - *Machine Learning*, 8(3-4), 279-292
- **Key Authors:** Christopher Watkins, Peter Dayan
- **Python Packages:** 
  - `stable-baselines3` (DQN variants)
  - `tensorflow-agents`
  - `pytorch-dqn` (custom implementations)
- **Key Variants:** van Hasselt et al., "Deep Reinforcement Learning with Double Q-learning" (2015) - arXiv:1509.06461

### SARSA (State-Action-Reward-State-Action)
- **Original Paper:** "Reinforcement Learning in the Presence of Noise and Uncertainty" - Rummery & Niranjan (1994)
- **Key Authors:** Gavin Rummery, Mahesan Niranjan
- **Python Packages:**
  - `stable-baselines3`
  - Custom RL libraries
- **Context:** First on-policy TD learning algorithm

### Value Iteration / Policy Iteration
- **Foundation:** Bellman Equation & Dynamic Programming
- **Key Papers:**
  - Bellman, R. E. (1957) - "Dynamic Programming"
  - Puterman, M. L. (2005) - "Markov Decision Processes: Discrete Stochastic Dynamic Programming"
- **Key Authors:** Richard Bellman, Martin Puterman
- **Python Packages:**
  - `scipy` (for small MDPs)
  - Custom implementations in NumPy
- **Use Case:** Planning with known models

### DQN (Deep Q-Networks)
- **Paper:** Mnih et al., "Playing Atari with Deep Reinforcement Learning" (2013) - arXiv:1312.5602
- **Key Authors:** Volodymyr Mnih, Koray Kavukcuoglu, David Silver, et al.
- **Improvements:**
  - van Hasselt et al., "Deep Reinforcement Learning with Double Q-learning" (2015) - arXiv:1509.06461
  - Wang et al., "Dueling Network Architectures for Deep Reinforcement Learning" (2015) - arXiv:1511.06581
  - Schaul et al., "Prioritized Experience Replay" (2015) - arXiv:1511.05952
  - Hessel et al., "Rainbow: Combining Improvements in Deep Reinforcement Learning" (2017) - arXiv:1710.02298
- **Python Packages:**
  - `stable-baselines3` (DQN, Double DQN)
  - `tensorflow-agents` (Multiple variants)
  - `pytorch-dqn`
  - `rllib` (Ray RLlib)
  - `keras-rl2`
- **Popular Environments:** Atari-2600, OpenAI Gym

## Policy-Based Algorithms

### REINFORCE (Policy Gradient)
- **Paper:** Williams, "Simple statistical gradient-following algorithms for connectionist reinforcement learning" (1992) - *Machine Learning*, 8(3-4), 229-256
- **Key Authors:** Ronald J. Williams
- **Python Packages:**
  - `stable-baselines3` (A2C, A3C implementations)
  - `tensorflow-agents`
  - `pytorch` tutorials
- **Characteristics:** On-policy, high variance, foundational for modern policy gradients

### PPO (Proximal Policy Optimization)
- **Paper:** Schulman et al., "Proximal Policy Optimization Algorithms" (2017) - arXiv:1707.06347
- **Key Authors:** John Schulman, Filip Wolski, Prafulla Dhariwal, Alec Radford, Oleg Klimov
- **Python Packages:**
  - `stable-baselines3` (PPO)
  - `rllib` (Ray RLlib)
  - `tensorflow-agents`
  - `openai-baselines`
  - `pytorch-ppo`
- **Applications:** Robotics, game AI, continuous control
- **GitHub:** https://github.com/openai/baselines

### TRPO (Trust Region Policy Optimization)
- **Paper:** Schulman et al., "Trust Region Policy Optimization" (2015) - arXiv:1502.05477
- **Key Authors:** John Schulman, Sergey Levine, Pieter Abbeel, Michael Jordan, Philipp Moritz
- **Python Packages:**
  - `stable-baselines3` (TRPO)
  - `rllib`
  - `garage` (Reinforcement Learning Toolkit)
- **Predecessor to:** PPO

### Natural Policy Gradient
- **Original Paper:** "Natural Gradient Works Efficiently in Learning" - Amari (1998)
- **RL Application:** Kakade (2001) - "A Natural Policy Gradient"
- **Key Authors:** Shun-ichi Amari, Sham Kakade
- **Characteristics:** Uses Fisher information matrix for gradient scaling

### Evolutionary Strategies (ES)
- **Modern Application:** "Evolution Strategies as a Scalable Alternative to Reinforcement Learning" - Salimans et al. (2016)
- **Publication:** *arXiv:1703.03400*
- **Key Authors:** Tim Salimans, Jonathan Ho, Xi Chen, Ilya Sutskever
- **Python Packages:**
  - `evosax` (JAX-based ES)
  - `deap` (Distributed Evolutionary Algorithms in Python)
  - Custom PyTorch implementations
- **Use Case:** Black-box optimization, gradient-free learning

## Actor-Critic Methods

### Actor-Critic (General Framework)
- **Foundational Paper:** "Actor-Critic Algorithms" - Konda & Tsitsiklis (2000)
- **Publication:** *SIAM Journal on Control and Optimization*, 42(4), 1143-1166
- **Key Authors:** Vijay Konda, John Tsitsiklis
- **Python Packages:** Various (see specific variants below)

### A2C (Advantage Actor-Critic)
- **Based on:** Asynchronous Methods for Deep RL - Mnih et al. (2016)
- **Key Authors:** Volodymyr Mnih, Adrià Puigdomènech Badia, et al.
- **Python Packages:**
  - `stable-baselines3` (A2C)
  - `tensorflow-agents`
  - `rllib`
  - `keras-rl2`

### A3C (Asynchronous Advantage Actor-Critic)
- **Paper:** Mnih et al., "Asynchronous Methods for Deep Reinforcement Learning" (2016) - arXiv:1602.01783
- **Key Authors:** Volodymyr Mnih, Adrià Badia, Mircea Gheorghe, et al.
- **Python Packages:**
  - `stable-baselines3` (A3C)
  - `tensorflow-agents`
  - `rllib`
  - OpenAI Baselines
- **Key Feature:** Asynchronous parallel training

### DDPG (Deep Deterministic Policy Gradient)
- **Paper:** Lillicrap et al., "Continuous control with deep reinforcement learning" (2015) - arXiv:1509.02971
- **Key Authors:** Timothy P. Lillicrap, Jonathan J. Hunt, Alexander Pritzel, Nicolas Heess, et al.
- **Python Packages:**
  - `stable-baselines3` (DDPG)
  - `tensorflow-agents`
  - `rllib`
  - `spinningup` (OpenAI Spinning Up)
- **Application:** Continuous control (robotics, manipulation)

### TD3 (Twin Delayed DDPG)
- **Paper:** Fujimoto et al., "Addressing Function Approximation Error in Actor-Critic Methods" (2018) - arXiv:1802.09477
- **Key Authors:** Scott Fujimoto, Herke van Hoof, David Meger
- **Python Packages:**
  - `stable-baselines3` (TD3)
  - `tensorflow-agents`
  - `rllib`
  - `spinningup`
- **Improvement Over:** DDPG

### SAC (Soft Actor-Critic)
- **Paper:** Haarnoja et al., "Soft Actor-Critic: Off-Policy Deep Reinforcement Learning with a Stochastic Actor" (2018) - arXiv:1801.01290
- **Key Authors:** Tuomas Haarnoja, Aurick Zhou, Pieter Abbeel, Sergey Levine
- **Extensions:**
  - Haarnoja et al., "Soft Actor-Critic Algorithms and Applications" (2018) - arXiv:1812.05905
- **Python Packages:**
  - `stable-baselines3` (SAC)
  - `tensorflow-agents`
  - `rllib`
  - `spinningup`
- **Characteristics:** Maximum entropy framework, sample-efficient

## Planning and Search Algorithms

### MCTS (Monte Carlo Tree Search)
- **Original Paper:** "Efficient Selectivity and Backup Operators in Monte-Carlo Tree Search" - Coulom (2006)
- **Key Formalization:** "Bandit based Monte-Carlo Tree Search" - Kocsis & Szepesvári (2006)
- **Publication:** *ECML 2006*
- **Key Authors:** Rémi Coulom, Levente Kocsis, Csaba Szepesvári
- **Python Packages:**
  - `pommerman` (with MCTS agents)
  - `mcts` (Pure Python implementation)
  - `alphago-zero-pytorch` (custom)
  - `gym-chess` (chess with MCTS)
- **Applications:** Game playing (AlphaGo), planning

### Minimax / Alpha-Beta Pruning
- **Foundation:** Game Theory & Artificial Intelligence
- **Key Papers:**
  - Shannon, C. E. (1950) - "Programming a Computer for Playing Chess"
  - Knuth & Moore (1975) - "An Analysis of Alpha-Beta Pruning"
- **Key Authors:** Claude Shannon, Donald Knuth, Donald Moore
- **Python Packages:**
  - `python-chess` (Chess engine with minimax)
  - `stockfish` (UCI engine wrapper)
  - Custom game-specific implementations
- **Use Cases:** Chess, checkers, tic-tac-toe

### A* Search
- **Original Paper:** "A Formal Basis for the Heuristic Determination of Minimum Cost Paths" - Hart et al. (1968)
- **Key Authors:** Peter Hart, Nils Nilsson, Bertram Raphael
- **Python Packages:**
  - `heapq` (Python standard library)
  - `astar` (Pure Python)
  - `networkx` (Graph algorithms)
  - `prm` (Probabilistic Roadmaps)
- **Applications:** Pathfinding, navigation, game AI

### MPC (Model Predictive Control)
- **Survey:** "An overview of nonlinear model predictive control applications" - Qin & Badgwell (2003)
- **Key Authors:** S. Joe Qin, Thomas A. Badgwell
- **Python Packages:**
  - `casadi` (Numeric optimization)
  - `cvxpy` (Convex optimization)
  - `scipy.optimize`
  - `gekko` (Dynamic optimization)
- **Applications:** Robotics, industrial process control

### iLQR (iterative Linear Quadratic Regulator)
- **Original Paper:** "Differential Dynamic Programming" - Mayne (1966)
- **Modern Treatment:** Li & Todorov (2004) - "Iterative Linear Quadratic Regulator Design for Nonlinear Biological Movement Systems"
- **Key Authors:** David Q. Mayne, Yuval Tassa, Emanuel Todorov
- **Python Packages:**
  - `ilqr` (Pure Python)
  - `PyTorch-based implementations`
  - Part of robotics libraries (Drake, MuJoCo)
- **Applications:** Trajectory optimization, robotics

### RRT (Rapidly-Exploring Random Tree)
- **Original Paper:** "Rapidly-exploring random trees: A new tool for path planning" - LaValle (1998)
- **Key Authors:** Steven M. LaValle
- **Extensions:** RRT*, Informed RRT*
- **Python Packages:**
  - `pyrrt` (Pure Python)
  - `pybullet` (Includes RRT planning)
  - `ompl` (Open Motion Planning Library)
  - `moveit` (ROS motion planning)
- **Applications:** Robot motion planning, high-dimensional spaces

## Deep RL and Foundational Models

### AlphaGo
- **Paper:** Silver et al., "Mastering the game of Go with deep neural networks and tree search" (2016) - *Nature*, 529(7587), 484-489
- **Key Authors:** David Silver, Aja Huang, Chris J. Maddison, Arthur Guez, et al.
- **Techniques:** Deep CNNs + Policy Network + Value Network + MCTS
- **Successor:** AlphaGo Zero, AlphaZero

### AlphaZero
- **Paper:** Silver et al., "Mastering Chess and Shogi by Self-Play with a General Reinforcement Learning Algorithm" (2017) - arXiv:1712.01724
- **Key Authors:** David Silver, Thomas Hubert, Julian Schrittwieser, Ioannis Antonoglou, et al.
- **Key Feature:** General algorithm for multiple games (Chess, Shogi, Go)
- **Techniques:** Self-play + Neural Networks + MCTS
- **Open Source:** 
  - `leela-zero` (Open source Go engine)
  - `leela-chess-zero` (Chess)

### MuZero
- **Paper:** Schrittwieser et al., "Mastering Atari, Go, Chess and Shogi by Planning with a Learned Model" (2019) - arXiv:1911.08265
- **Key Authors:** Julian Schrittwieser, Thomas Hubert, Amol Mandhane, et al.
- **Key Feature:** Value-equivalent models (no explicit environment model)
- **Python Packages:**
  - `mcts` (General MCTS)
  - Custom implementations based on paper

### Hindsight Experience Replay (HER)
- **Paper:** Andrychowicz et al., "Hindsight Experience Replay" (2017) - arXiv:1707.01495
- **Key Authors:** Marcin Andrychowicz, Filip Wolski, Alex Ray, Jonas Schneider, et al.
- **Python Packages:**
  - `stable-baselines3` (DDPG + HER, SAC + HER)
  - `tensorflow-agents`
- **Use Case:** Goal-conditioned RL with sparse rewards

## Partially Observable / Hidden State Algorithms

### Hidden Markov Models (HMM)
- **Foundation:** Markov Chains & Probability Theory
- **Key Papers:**
  - Rabiner, L. R. (1989) - "A tutorial on hidden Markov models and selected applications in speech recognition" - *IEEE*, 77(2), 257-286
- **Key Authors:** Lawrence Rabiner
- **Python Packages:**
  - `hmmlearn` (scikit-learn HMM)
  - `pomegranate` (Probabilistic models)
  - `pymc` (Bayesian inference)
- **Applications:** Speech recognition, sequence labeling

### Kalman Filter
- **Original Paper:** "A new approach to linear filtering and prediction problems" - Kalman (1960)
- **Publication:** *Journal of Basic Engineering*, 82(1), 35-45
- **Key Authors:** Rudolf Kálmán
- **Extensions:**
  - Extended Kalman Filter (EKF) - Jazwinski (1970)
  - Unscented Kalman Filter (UKF) - Julier & Uhlmann (1997)
- **Python Packages:**
  - `filterpy` (Kalman filters and Bayesian filtering)
  - `scipy.linalg` (Linear algebra for KF)
  - `numpy` (Manual implementations)
- **Applications:** Tracking, robotics localization, sensor fusion

### Particle Filtering
- **Original Paper:** "Novel approach to nonlinear/non-Gaussian Bayesian state estimation" - Gordon et al. (1993)
- **Publication:** *IEE Proceedings-F*, 140(2), 107-113
- **Key Authors:** Neil J. Gordon, David J. Salmond, Adrian F. M. Smith
- **Python Packages:**
  - `filterpy` (Particle filters)
  - `particles` (Sequential Monte Carlo)
  - `PyMC` (Probabilistic inference)
- **Applications:** Tracking, localization, non-linear filtering

### POMDP (Partially Observable MDP)
- **Original Paper:** "The complexity of solving partially observable Markov decision problems and belief updating" - Kaelbling et al. (1998)
- **Publication:** *Journal of Artificial Intelligence Research*, 11, 99-143
- **Key Authors:** Leslie Pack Kaelbling, Michael L. Littman, Anthony R. Cassandra
- **Solvers:**
  - `pomdp-solve` (Exact POMDP solver)
  - `pomcpow` (Online planning for POMDPs)
- **Applications:** Robot navigation, partial observability problems

### POMCP (Partially Observable Monte Carlo Planning)
- **Paper:** "Monte-Carlo Planning in Large POMDPs" - Silver & Veness (2010)
- **Publication:** *NIPS 2010*
- **Key Authors:** David Silver, Joel Veness
- **Python Packages:**
  - Custom implementations
  - `mcts` (General MCTS adaptable to POMDPs)

## Game Theory & Multi-Agent Algorithms

### CFR (Counterfactual Regret Minimization)
- **Paper:** Zinkevich et al., "Regret Minimization in Games with Incomplete Information" (2007) - *NIPS 2007*
- **Key Authors:** Michael Zinkevich, Michael Bowling
- **Advances:**
  - Hladík et al., "Solving Imperfect Information Games" (2017)
  - Brown et al., "Neural Replicator Dynamics" (2019)
- **Python Packages:**
  - `poker-cfr` (Pure Python CFR)
  - `pykerflop` (Poker with CFR)
  - `imarl` (Imperfect information MARL)
- **Applications:** Poker solving, imperfect information games

### Nash Equilibrium Solvers
- **General Theory:** Nash, J. F. (1950) - "Equilibrium points in n-person games"
- **Computation:** 
  - Lemke & Howson (1964) - Pivoting algorithm
  - Porter, Nudelman & Shoham (2008) - Support enumeration
- **Python Packages:**
  - `nashpy` (Lemke-Howson algorithm)
  - `gambit` (Gambit Project - equilibrium computation)
  - `pygambit` (Python interface to Gambit)

### QMIX (Mixing Q-Functions)
- **Paper:** Rashid et al., "QMIX: Monotonic Value Function Factorisation for Decentralised Multi-Agent Reinforcement Learning" (2018) - arXiv:1803.11485
- **Key Authors:** Tabish Rashid, Mikayel Samvelyan, Christian Schroeder de Witt, Gregory Farquhar, et al.
- **Python Packages:**
  - `pymarl` (PyMARL - Multi-Agent RL Research Library)
  - `smac` (StarCraft Multi-Agent Challenge)
- **Applications:** Cooperative multi-agent control

### MAPPO (Multi-Agent PPO)
- **Paper:** "The Surprising Effectiveness of PPO in Cooperative Multi-Agent Games" - Yu et al. (2021)
- **Publication:** *arXiv:2108.02556*
- **Key Authors:** Chao Yu, Akash Velu, Eugene Vinitsky, Jiaxuan Wang, et al.
- **Python Packages:**
  - `pymarl2`
  - `mappo` (Official implementation)
  - `cleanrl` (Clean implementations of RL algorithms)
- **Observations:** Simple PPO scales well for cooperative multi-agent tasks

### MAAC (Multi-Agent Actor-Critic)
- **Paper:** Iqbal & Sha, "Actor-Attention-Critic for Multi-Agent Reinforcement Learning" (2019) - arXiv:1810.02912
- **Key Authors:** Shariq Iqbal, Fei Sha
- **Python Packages:**
  - `maac` (Official PyTorch implementation)
  - `pymarl`

### MADDPG (Multi-Agent DDPG)
- **Paper:** Lowe et al., "Multi-Agent Actor-Critic for Mixed Cooperative-Competitive Environments" (2017) - arXiv:1706.02891
- **Key Authors:** Ryan Lowe, Yi Wu, Aviv Tamar, Jean Harb, et al.
- **Python Packages:**
  - `maddpg` (Official TensorFlow implementation)
  - `pytorch-maddpg`
  - `openai-multi-agent-particle-envs`

### CommNet (Communication Neural Networks)
- **Paper:** Sukhbaatar et al., "Learning to Communicate with Deep Multi-Agent Reinforcement Learning" (2016) - arXiv:1605.06676
- **Key Authors:** Sainbayar Sukhbaatar, Arthur Szlóthy, Gabriel Synnaeve, Rob Fergus
- **Techniques:** Graph neural networks for multi-agent coordination
- **Python Packages:**
  - `pytorch-geometric` (Graph neural networks)
  - Custom implementations

## Offline / Batch Learning

### Batch Q-Learning / Offline RL
- **Survey:** Levine et al., "Offline Reinforcement Learning: Tutorial, Review, and Perspectives on Open Problems" (2020) - arXiv:2005.01643
- **Key Authors:** Sergey Levine, Aviral Kumar, George Tucker, Justin Fu
- **Key Papers:**
  - Lange et al., "Batch Reinforcement Learning" (2012) - *Journal of Machine Learning Research*, 13(4), 1–45
  - Kumar et al., "Conservative Q-Learning for Offline Reinforcement Learning" (2020) - arXiv:2006.04779

### Behavior Cloning
- **Foundation:** Supervised learning on expert demonstrations
- **Modern Application:** Torabi et al., "Behavioral Cloning from Observation" (2018) - arXiv:1805.01954
- **Python Packages:**
  - `imitation` (Imitation learning library)
  - Custom implementations with PyTorch/TensorFlow

### CQL (Conservative Q-Learning)
- **Paper:** Kumar et al., "Conservative Q-Learning for Offline Reinforcement Learning" (2020) - arXiv:2006.04779
- **Key Authors:** Aviral Kumar, Aurick Zhou, George Tucker, Sergey Levine
- **Python Packages:**
  - `cql` (Official implementation)
  - `d3rlpy` (Offline RL library)
  - `pyrl` (Policy learning library)

## Integrated Learning & Planning

### Dyna-Q (Integration of Learning and Planning)
- **Paper:** Moore & Atkeson, "Integrating Learning and Planning in the Dyna Architecture" (1993) - *Artificial Intelligence*, 72(1-2), 49-80
- **Key Authors:** Andrew W. Moore, Christopher G. Atkeson
- **Python Packages:**
  - Custom implementations
  - Part of general RL frameworks
- **Characteristics:** Model-free learning + model-based planning

## Hierarchical & Modular Approaches

### Hierarchical Reinforcement Learning
- **Survey:** Dietterich, "Hierarchical Reinforcement Learning with the MAXQ Value Function Decomposition" (2000) - *Journal of Artificial Intelligence Research*, 13, 227-303
- **Key Authors:** Tom Dietterich
- **Frameworks:**
  - Sutton et al., "Between MDPs and semi-MDPs" (1999) - Options Framework
  - Dietterich, "The MAXQ Method for Hierarchical Reinforcement Learning" (2000)
  - Vezhnevets et al., "Feudal Networks for Hierarchical Reinforcement Learning" (2017) - arXiv:1703.03400

### Options Framework
- **Paper:** Sutton et al., "Between MDPs and semi-MDPs: Learning, Planning, and Representing Knowledge at Multiple Temporal Scales" (1999) - *JMLR*, 2000, 201-240
- **Key Authors:** Richard S. Sutton, Doina Precup, Satinder Singh

## Bandit Algorithms

### ε-Greedy
- **Foundation:** Exploration-exploitation tradeoff
- **Key Reference:** Sutton & Barto (2018) - "Reinforcement Learning: An Introduction" (2nd Edition)
- **Use:** Baseline exploration strategy

### Upper Confidence Bound (UCB)
- **Paper:** Auer et al., "Finite-Time Analysis of the Multiarmed Bandit Problem" (2002) - *Machine Learning*, 47(2/3), 235-256
- **Key Authors:** Peter Auer, Nicolò Cesa-Bianchi, Paul Fischer
- **Variants:**
  - Auer et al., "UCB1: Upper Confidence Bound" (2002)
  - Garivier & Kaufmann, "Optimal Best Arm Identification with Fixed Budget" (2016) - arXiv:1505.04627
- **Python Packages:**
  - `vowpalwabbit` (Bandit algorithms)
  - `contextual` (Contextual bandits)
  - `bandito` (Bandit optimization)

### Thompson Sampling
- **Original Work:** Thompson, W. R., "On the likelihood that one unknown probability exceeds another" (1933) - *Biometrika*, 25(3/4), 285-294
- **Modern Application:** Chapelle & Li, "An Empirical Evaluation of Thompson Sampling" (2011) - *NIPS 2011*
- **Key Authors:** William R. Thompson, Olivier Chapelle, Lihong Li
- **Python Packages:**
  - `vowpalwabbit`
  - `thompson-sampling` (Pure Python)
  - `contextual`

### Contextual Bandits
- **Paper:** Li et al., "A Contextual-Bandit Approach to Personalized News Recommendation" (2010) - *WWW 2010*
- **Key Authors:** Lihong Li, Wei Chu, John Langford, Robert E. Schapire
- **Python Packages:**
  - `vowpalwabbit`
  - `contextual` (Full library)
  - `bandit` (Python Bandit)
  - `ml-logger` (Experiment tracking for bandits)

## Foundational References & Textbooks

### Core Textbooks
1. **Reinforcement Learning: An Introduction** - Sutton & Barto (2nd Edition, 2018)
   - ISBN: 978-0262039246
   - Python Code: https://github.com/ShangtongZhang/reinforcement-learning-an-introduction

2. **Algorithms for Reinforcement Learning** - Szepesvári (2010)
   - arXiv: https://arxiv.org/abs/1802.09477

3. **Deep Reinforcement Learning Hands-On** - Lapan (2nd Edition, 2020)
   - ISBN: 978-1838826994
   - GitHub: https://github.com/PacktPublishing/Deep-Reinforcement-Learning-Hands-On

### Survey Papers
- Li et al., "Deep Reinforcement Learning: An Overview" (2017) - arXiv:1701.07274
- Arulkumaran et al., "A Brief Survey of Deep Reinforcement Learning" (2017) - arXiv:1708.05866
- Khetarpal et al., "Towards Generalist Robots via Foundation Models" (2023) - arXiv:2307.15818

## Integrated Python Libraries & Frameworks

### All-In-One RL Frameworks
- **Stable-Baselines3** (PyTorch-based) - https://github.com/DLR-RM/stable-baselines3
- **Ray RLlib** (Distributed) - https://docs.ray.io/en/latest/rllib/
- **TensorFlow Agents** - https://github.com/tensorflow/agents
- **OpenAI Baselines** (Reference implementations) - https://github.com/openai/baselines
- **PyMARL** (Multi-agent) - https://github.com/oxwhirl/pymarl
- **Garage** (Academic toolkit) - https://github.com/rlworkgroup/garage

### Environment & Simulation
- **OpenAI Gym** (Standard RL environments) - https://gym.openai.com/
- **Atari-py** (Atari game environments) - https://github.com/openai/atari-py
- **PyBullet** (Physics simulation) - https://pybullet.org/
- **CARLA** (Autonomous driving simulator) - http://carla.org/
- **MuJoCo** (Physics engine) - https://mujoco.org/
- **DeepMind Lab** (3D environment) - https://github.com/deepmind/lab
- **Procgen** (Procedural environments) - https://github.com/openai/procgen
