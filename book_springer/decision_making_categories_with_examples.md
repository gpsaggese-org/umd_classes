# Decision-Making Problem Categories: Examples & Solutions
Taxonomy of decision-making problems organized by key structural dimensions
Each category shows concrete examples and key solution algorithms

## Structural Dimensions Overview
Decision-making problems vary along 10 _orthogonal dimensions_:

1. **_Observability_**: What information is available to the agent
  - Full (MDP – Markov Decision Process): Agent observes complete state; all
    needed information available each step
  - Partial (POMDP – Partially Observable Markov Decision Process): Observations
    don't uniquely determine state; must maintain belief state
  - Hidden/Noisy: Environment has hidden state; observations are
    corrupted/stochastic

2. **_Time Horizon_**: Planning window and reward accumulation
  - One-step (Bandit): Optimize immediate reward only (greedy decisions)
  - Multi-step (finite): Consider consequences over fixed lookahead horizon
  - Infinite (discounted): Long-term optimization with discount factor $\gamma$

3. **_Action Space_**: Structure of available decisions
  - Discrete: Finite set of actions (can enumerate)
  - Continuous: Action space $\mathbb{R}^n$ (uncountably infinite)
  - Hybrid (mixed): Some actions discrete, some continuous

4. **_Multi-Agent_**: Number and objectives of decision-makers
  - Single-agent: One decision-maker, one objective → no strategic interaction
  - Cooperative: Multiple agents, shared objective → must coordinate
  - Competitive/Mixed: Agents with conflicting or mixed objectives; game theory
    applies

5. **_Information Structure_**: Symmetry and knowledge distribution
  - Perfect info: All players know all relevant information
  - Imperfect info: Players have asymmetric or hidden information
  - Asymmetric: Players have fundamentally different information sets and
    capabilities

6. **_Model Availability_**: Access to world model/dynamics
  - Model-based: Agent has (or learns) transition model $p(s'|s,a)$ (state
    transition probability) and reward $r(s,a)$ (reward function)
  - Model-free: Agent learns directly from experience; no explicit model
  - Hybrid: Learns approximate model or uses model selectively

7. **_Update Mechanism_**: When and how learning occurs
  - Online: Agent learns and acts in real-time; single trajectory
  - Batch: Agent trains on fixed dataset; replay or offline learning
  - Replay-based: Agent stores experiences and replays for training

8. **_Solution Concept_**: How policy is represented/optimized
  - Value-based: Learn state or state-action values; derive policy from values
  - Policy-based: Learn policy directly without explicit value function
  - Actor-Critic: Combine value function and policy learning
  - Search/Planning: Use tree search or planning to find optimal actions

9. **_Optimality Criterion_**: Policy structure and goal
  - Deterministic: Policy outputs single action per state
  - Stochastic: Policy outputs probability distribution over actions
  - Optimal: Find best possible policy (exact or approximate)
  - Approximate: Satisfice with good-enough policy; bounded suboptimality
    acceptable

10. **_Scalability_**: State/action space size and representation
  - Tabular: |S| and |A| small enough for lookup tables (<10k states)
  - Linear FA (Function Approximation): Medium-scale; use linear function
    approximation V(s) = w·φ(s)
  - Deep NN (Neural Network): Large/high-dimensional; use deep neural networks

## 1. Observability: Full Vs. Partial

### 1A. Fully Observable (MDP)

- **Setup**:
  - Agent sees complete state
  - All needed information available each step

- **Formulation**:
  - MDP tuple: $(\mathcal{S}, \mathcal{A}, P, R, \gamma)$
  - Agent observes: complete state $s_t \in \mathcal{S}$ each step
  - Transition dynamics: $P(s'|s,a)$ and rewards $R(s,a)$ fully known
  - No hidden state or partial observability

- **Example 1**: Tic-Tac-Toe
  - Board state fully visible to both players
  - All moves and outcomes deterministic and known
  - Perfect information game

- **Example 2**: Inventory Management
  - Current inventory level fully observed
  - Customer demand known/predictable
  - Order quantities, lead times, holding costs fully specified
  - Decisions: how much to order each period

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

- **Formulation**:
  - POMDP tuple: $(\mathcal{S}, \mathcal{A}, P, R, \Omega, O, \gamma)$
  - Agent observes: $o_t \sim O(\cdot | s_t)$, not true state $s_t$
  - Must maintain belief: $b_t(s) = P(s_t = s | o_1, a_1, \ldots, o_t)$ over possible states

- **Example 1**: Robot Localization
  - Robot receives noisy sensor readings (how far to walls, objects)
  - Doesn't know exact location, but multiple positions consistent with
    observations
  - Must track probability distribution over possible locations

- **Example 2**: Card Game (Poker)
  - Player observes own hand and community cards
  - Cannot see opponent's hole cards
  - Must infer opponent's hand distribution from betting behavior
  - Maintains belief distribution over opponent hand strength

- **Algorithms**:
  - Particle Filtering
  - Kalman Filter
  - POMCP (Partially Observable Monte Carlo Planning)
  - Belief State Planning

### 1C. Stochastic Observations with Hidden State

- **Setup**:
  - Environment has hidden state
  - Observations are noisy/corrupted

- **Formulation**:
  - Hidden Markov Model (HMM)
  - True state transition: $P(s_{t+1} | s_t)$
  - Observations: $o_t \sim O(\cdot | s_t)$ are corrupted/stochastic
  - Goal: infer hidden state sequence from noisy observations via filtering/smoothing

- **Example 1**: Weather Prediction from Noisy Thermometer
  - True weather has hidden state (hot/cold/rainy)
  - Observe thermometer reading, but sensor is noisy
  - Need to infer hidden state from noisy observations over time

- **Example 2**: Speech Recognition
  - True phoneme sequence is hidden
  - Microphone records acoustic signal corrupted by noise
  - Observations: mel-spectrogram features (noisy)
  - Task: infer true phoneme sequence from noisy audio features

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

- **Formulation**:
  - Bandit problem: maximize $\mathbb{E}[R(a)]$ for single action $a$
  - No sequential dependence; no state transition
  - Action and reward independent of history
  - Problem: $\max_a R(a)$ or learn $\mu_a = \mathbb{E}[R(a)]$ for each arm $a$

- **Example 1**: Email Spam Filter (Per-Email Classification)
  - Classify email as spam/not-spam
  - Decision affects only that email; no long-term consequences
  - Optimize accuracy on current email

- **Example 2**: Online Advertising (Ad Selection)
  - Select which ad to show to user
  - User sees ad, may click or not (reward signal)
  - No effect on future user state or ad performance
  - Maximize click-through rate for current user

- **Algorithms**:
  - Greedy
  - Ε-Greedy (Epsilon-Greedy)
  - UCB (Upper Confidence Bound)
  - Thompson Sampling
  - Contextual Bandits

### 2B. Multi-Step Lookahead (Finite Horizon)

- **Setup**:
  - Consider future consequences over fixed horizon

- **Formulation**:
  - Finite-horizon MDP with lookahead depth $H$
  - Maximize cumulative reward: $\sum_{t=0}^{H} R(s_t, a_t)$ over trajectory
  - State transitions: $s_{t+1} \sim P(\cdot | s_t, a_t)$
  - Optimal value: $V_h(s) = \max_a [R(s,a) + V_{h-1}(s')]$ via backward induction

- **Example 1**: Chess Move Selection (20 moves ahead)
  - Current move affects board state for next moves
  - Cannot evaluate single move in isolation
  - Need to lookahead 20+ moves to find good strategy

- **Example 2**: Robotic Manipulation (Grasp Planning)
  - Robot must plan sequence of moves to grasp and move object
  - Each action changes object position/gripper state
  - Fixed horizon (e.g., 10 steps to grasp and place)
  - Lookahead through movement sequence to find feasible grasp

- **Algorithms**:
  - Minimax
  - Alpha-Beta Pruning
  - A\* (A-Star)
  - RRT (Rapidly-exploring Random Tree)
  - MCTS (Monte Carlo Tree Search)

### 2C. Infinite Horizon (Discounted)

- **Setup**:
  - Long-term optimization
  - Infinite horizon with discount factor $\gamma \in [0, 1)$

- **Formulation**:
  - Infinite-horizon discounted MDP
  - Maximize: $J = \mathbb{E}[\sum_{t=0}^{\infty} \gamma^t R(s_t, a_t)]$
  - Bellman equation: $V^*(s) = \max_a [R(s,a) + \gamma \mathbb{E}_{s' \sim P(\cdot|s,a)}[V^*(s')]]$
  - Optimal policy: $\pi^*(s) = \argmax_a [R(s,a) + \gamma \mathbb{E}[V^*(s')]]$ is stationary

- **Example 1**: Portfolio Management
  - Allocate investments today to maximize wealth forever
  - Future rewards discounted: $\gamma^t$ reduces weight of distant rewards
  - Stationary optimal policy (doesn't change over time)

- **Example 2**: Autonomous Navigation
  - Robot navigates continuously in environment
  - Reward: reach goal state with minimal energy cost
  - Infinite horizon: never truly terminal, always operating
  - Discount factor $\gamma$ balances immediate vs. long-term goals

- **Algorithms**:
  - Q-Learning
  - SARSA (State-Action-Reward-State-Action)
  - Value Iteration
  - Policy Iteration
  - Actor-Critic methods
  - Deep RL: DQN (Deep Q-Network), PPO (Proximal Policy Optimization), SAC (Soft
    Actor-Critic)

### 2D. Episodic / Finite Horizon

- **Setup**:
  - Fixed episode length $T$
  - Sum undiscounted rewards (or discounted differently)

- **Formulation**:
  - Episodic task with fixed terminal step $T$
  - Maximize: $J = \mathbb{E}[\sum_{t=0}^{T} R(s_t, a_t)]$ per episode
  - No discounting (or weak discounting)
  - Agent resets to initial state after step $T$

- **Example 1**: Video Game Level
  - Game episode lasts exactly 300 steps (frames)
  - Optimize total score over that episode
  - After 300 steps, episode ends

- **Example 2**: Curriculum Learning (Student Exam)
  - Student studies for exam (fixed time/resources)
  - Episode ends when exam time limit reached
  - Maximize exam score over study period
  - Next episode: new exam with reset knowledge state

- **Algorithms**:
  - Monte Carlo Methods
  - MCTS (Monte Carlo Tree Search)
  - Policy Gradient (REINFORCE)
  - Episodic RL variants

## 3. Action Space: Discrete Vs. Continuous

### 3A. Discrete Actions

- **Setup**:
  - Finite set of actions $\mathcal{A} = \{a_1, a_2, \ldots, a_n\}$
  - Can enumerate and compare

- **Formulation**:
  - Action space: $|\mathcal{A}| = n$ is finite
  - Agent selects: $a_t \in \mathcal{A}$ at each step
  - Q-function representation: table with $|\mathcal{S}| \times n$ entries
  - Optimal action: $a^* = \argmax_{a \in \mathcal{A}} Q(s, a)$ via enumeration

- **Example 1**: Traffic Light Controller
  - Actions: {Green (NS), Green (EW), Yellow, Red}
  - Discrete choices; can try each one
  - Small branching factor

- **Example 2**: Document Recommendation
  - User action space: {Like, Dislike, Bookmark, Share, Ignore}
  - Each action discrete; agent selects one per document shown
  - Bounded, enumerable action set
  - Learn Q(user_state, action) for each of 5 actions

- **Algorithms**:
  - Q-Learning
  - DQN (Deep Q-Network)
  - MCTS (Monte Carlo Tree Search)
  - Minimax
  - Value Iteration (when feasible)

### 3B. Continuous Actions

- **Setup**:
  - Action space $\mathcal{A} \subseteq \mathbb{R}^n$ (uncountably infinite)
  - Cannot enumerate

- **Formulation**:
  - Action space is continuous: $a \in \mathbb{R}^n$ or bounded $a \in [-1, 1]^n$
  - Cannot represent as Q-table
  - Learn policy: $\pi(a | s)$ (stochastic) or $a = \mu(s)$ (deterministic)
  - Approximation: via neural networks

- **Example 1**: Robot Arm Control
  - Continuous joint angles $(\theta_1, \theta_2, \theta_3) \in \mathbb{R}^3$
  - Infinite possible actions
  - Must learn function, not table

- **Example 2**: Autonomous Vehicle Control
  - Action: steering angle $\alpha \in [-\pi/4, \pi/4]$ (continuous)
  - Throttle/brake: acceleration $a \in [-10, 5]$ m/s² (continuous)
  - State-action mapping learned via neural network policy
  - Infinite action combinations possible

- **Algorithms**:
  - Policy Gradient (REINFORCE)
  - Actor-Critic: A3C (Asynchronous Advantage Actor-Critic), SAC (Soft
    Actor-Critic)
  - DDPG (Deep Deterministic Policy Gradient)
  - TD3 (Twin Delayed DDPG)
  - PPO (Proximal Policy Optimization, with continuous output)
  - Evolutionary Strategies

### 3C. Hybrid (Mixed Discrete-Continuous)

- **Setup**:
  - Some actions discrete, some continuous
  - Two-level hierarchical decision

- **Formulation**:
  - Action space: $\mathcal{A} = \mathcal{A}_{\text{discrete}} \times \mathcal{A}_{\text{continuous}}$
  - Two-level selection: discrete $a_d \in \{1, \ldots, n_d\}$, then continuous $a_c \in \mathbb{R}^{n_c}$
  - Continuous action conditioned on discrete: $a_c$ given $a_d$
  - Policy factorization: $\pi(a_d, a_c | s) = \pi_d(a_d | s) \pi_c(a_c | s, a_d)$

- **Example 1**: Robotic Gripper with Mode Selection
  - Discrete: Which object to grasp (5 objects)
  - Continuous: Grasp force and angle
  - Two-level decision

- **Example 2**: Manufacturing Robot
  - Discrete: Select tool (gripper, welding torch, paint sprayer)
  - Continuous: Trajectory parameters (speed, position offsets, force)
  - Policy: first choose tool, then learn continuous trajectory

- **Algorithms**:
  - Branching DQN (Deep Q-Network)
  - Hierarchical RL (Reinforcement Learning)
  - Multi-task Learning with shared base

## 4. Multi-Agent Interaction

### 4A. Single-Agent

- **Setup**:
  - One decision-maker, one objective
  - No strategic interaction

- **Formulation**:
  - Standard MDP with single agent
  - Maximize: $J = \mathbb{E}[\sum_t \gamma^t R(s_t, a_t)]$
  - Optimal policy $\pi^*$ satisfies Bellman equation
  - No game theory; fixed environment (stochastic but non-adversarial)

- **Example 1**: Personalized Movie Recommendation
  - System recommends movies to single user
  - No other agents; no strategic interaction
  - Optimize user satisfaction

- **Example 2**: Inventory Management System
  - Single company manages warehouse
  - No competing agents
  - Minimize inventory cost + stockout penalties
  - Environment: customer demand, supplier lead times

- **Algorithms**:
  - Q-Learning
  - PPO (Proximal Policy Optimization)
  - DQN (Deep Q-Network)
  - SARSA (State-Action-Reward-State-Action)
  - Actor-Critic

### 4B. Multi-Agent Cooperative

- **Setup**:
  - Multiple agents $\{1, 2, \ldots, n\}$, shared objective
  - Must coordinate actions

- **Formulation**:
  - Cooperative multi-agent MDP
  - All agents share reward: $R(s, a_1, \ldots, a_n)$
  - Maximize: $J = \mathbb{E}[\sum_t R(s_t, a_{1,t}, \ldots, a_{n,t})]$
  - Challenge: decentralized execution; learn via communication/parameter sharing

- **Example 1**: Warehouse Robot Team
  - 5 robots move packages together
  - Shared goal: minimize delivery time
  - Robots must coordinate to avoid collisions, deadlocks
  - One reward signal for whole team

- **Example 2**: Multi-Agent Network Optimization
  - Multiple autonomous vehicles communicating on shared network
  - Shared objective: maximize network throughput with low latency
  - Each vehicle learns to route packets cooperatively
  - Joint reward: total throughput - total delay

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

- **Formulation**:
  - Multi-agent game where each agent $i$ maximizes: $J_i = \mathbb{E}[\sum_t R_i(s_t, a_{1,t}, \ldots, a_{n,t})]$
  - Zero-sum case: $R_1 + R_2 = \text{const}$
  - Nash equilibrium $\pi^*$: no agent can unilaterally improve by deviating
  - Optimal play: $R_i(s, \pi_i^*, \pi_{-i}^*) \geq R_i(s, \pi_i, \pi_{-i}^*)$ for all $\pi_i$

- **Example 1**: Chess Match
  - Two players, zero-sum game (one wins, one loses)
  - Each player wants to maximize own score
  - Optimal solution is Nash equilibrium (neither can unilaterally improve)

- **Example 2**: Auction Bidding
  - Multiple bidders competing for item
  - Each bidder wants to win at lowest cost
  - Conflicting objectives: your gain is others' loss
  - Nash equilibrium: truthful bidding (in second-price auction)

- **Algorithms**:
  - Minimax with Alpha-Beta Pruning
  - Self-Play
  - Nash Equilibrium Solvers
  - CFR (Counterfactual Regret Minimization)

## 5. Information Structure: Perfect Vs. Imperfect Vs. Asymmetric

### 5A. Perfect Information

- **Setup**:
  - All players know all relevant information
  - No hidden state or hidden actions
  - Complete game tree visibility

- **Formulation**:
  - Each player observes complete game history: $(s_0, a_{1,0}, a_{2,0}, \ldots, s_t)$
  - Information set: $I_i(h) = \{h' : \text{player } i \text{ cannot distinguish } h \text{ from } h'\}$ is singleton
  - Optimal play: computed via backward induction on game tree

- **Example 1**: Chess Match
  - Both players see entire board
  - All past moves known to both
  - No hidden pieces or secret moves
  - Perfect information game

- **Example 2**: Tic-Tac-Toe
  - Full board visibility at all times
  - All prior moves recorded
  - No chance/randomness
  - Fully solvable: can compute all Nash equilibria via minimax

- **Algorithms**:
  - Minimax with Alpha-Beta Pruning
  - MCTS (Monte Carlo Tree Search)
  - AlphaZero
  - Exact Game Solvers
  - Negamax

### 5B. Imperfect Information

- **Setup**:
  - Players have asymmetric or incomplete information
  - Hidden moves or hidden state
  - Information gap between players

- **Formulation**:
  - Players have non-singleton information sets
  - Player $i$ at history $h$ cannot distinguish from $h' \in I_i(h)$
  - Belief: $b_i(h) = P(h | \text{player } i \text{'s observations})$ over possible true states
  - Strategy equilibrium: mixed strategy $\sigma_i^*$ with no profitable unilateral deviation

- **Example 1**: Poker Match
  - Players don't see opponents' hole cards
  - Betting history is visible but card values hidden
  - Uncertainty over opponent's hand strength
  - Information asymmetry drives strategy

- **Example 2**: Strategic Business Competition
  - Firms make pricing decisions without knowing competitors' costs
  - Only observe market prices, not cost structures
  - Firms have private information (production efficiency)
  - Equilibrium: firms randomize pricing to avoid being exploited

- **Algorithms**:
  - CFR (Counterfactual Regret Minimization)
  - Nash Equilibrium Solvers
  - Regret Matching
  - Self-Play in imperfect information games
  - Information Set Abstractions

### 5C. Asymmetric Information

- **Setup**:
  - Players have fundamentally different information sets
  - Different access to actions or observations
  - Capabilities differ by player type

- **Formulation**:
  - Two-player game: player 1 (principal) does not observe player 2 (agent)
  - Principal cannot observe: agent's action $a_2$ or private information $\theta_2$
  - Principal designs: contract/mechanism to incentivize agent
  - Optimal contract: $\max_{c} u_1(c(y)) - c(y)$ subject to agent IC: $a_2^* = \argmax_{a} u_2(c(y(a))) - \psi(a)$

- **Example 1**: Principal-Agent Problem
  - Principal (employer) cannot directly observe agent (employee) effort
  - Agent knows own effort level; principal only sees output
  - Different information available to each party
  - Creates incentive alignment problem

- **Example 2**: Insurance Market
  - Insurance buyer knows health status; insurer does not (adverse selection)
  - Insurer designs deductible/coverage to screen types
  - Buyers self-select by choosing contract
  - Equilibrium: separating contract where high-risk buy full coverage

- **Algorithms**:
  - Mechanism Design
  - Game Theory with Asymmetric Info
  - Signaling Equilibrium Solvers
  - Information-dependent policies
  - Bayesian Games

## 6. Model Knowledge: Model-Based Vs. Model-Free

### 6A. Model-Based (Planning)

- **Setup**:
  - Agent has or learns transition model $p(s'|s,a)$ and reward $r(s,a)$
  - Uses model to plan

- **Formulation**:
  - Agent has/learns world model: $\hat{P}(s' | s, a)$ and $\hat{R}(s, a)$
  - Solves planning problem offline
  - Computes optimal policy via value iteration on learned model
  - Value function: $V(s) = \max_a [\hat{R}(s,a) + \gamma \mathbb{E}_{s' \sim \hat{P}}[V(s')]]$ without environment interaction

- **Example 1**: GPS Route Planner
  - Model: road network, travel times, traffic patterns
  - Uses model to find fastest route without driving all routes
  - Sample-efficient

- **Example 2**: Game AI Lookahead (Video Game)
  - Model: learned dynamics of game (unit movements, collisions)
  - Plans by simulating future game states
  - Evaluates action sequences without trying them in real game
  - Avoids risky actions in simulation

- **Algorithms**:
  - Value/Policy Iteration
  - Dyna-Q
  - MCTS (Monte Carlo Tree Search)
  - AlphaGo
  - MuZero

### 6B. Model-Free (Learning)

- **Setup**:
  - No model available
  - Agent learns directly from experience

- **Formulation**:
  - Agent observes trajectory: $(s_t, a_t, r_t, s_{t+1})$ from environment
  - Learns value/policy directly without constructing $\hat{P}$ or $\hat{R}$
  - Q-learning update: $Q(s, a) \leftarrow Q(s,a) + \alpha[r + \gamma \max_a' Q(s', a') - Q(s,a)]$
  - Policy gradient: $\theta \leftarrow \theta + \alpha \nabla \log \pi_\theta(a|s) R_t$

- **Example 1**: Learning to Play Atari from Pixels
  - No access to game code or physics
  - Learns Q-values directly from screen + rewards
  - Trial-and-error

- **Example 2**: Robot Manipulation Learning
  - Robot learns to grasp from trial-and-error interactions
  - No explicit model of object physics
  - Learns policy via reward signals (grasp success/failure)
  - Data-intensive but no need for hand-crafted dynamics

- **Algorithms**:
  - Q-Learning
  - SARSA (State-Action-Reward-State-Action)
  - Policy Gradient (REINFORCE)
  - Actor-Critic
  - DQN (Deep Q-Network)
  - PPO (Proximal Policy Optimization)
  - SAC (Soft Actor-Critic)
  - A3C (Asynchronous Advantage Actor-Critic)

## 7. Update Mechanism: Online Vs. Batch Vs. Replay

### 7A. Online Learning

- **Setup**:
  - Agent learns and acts in real-time
  - Single trajectory; immediate feedback
  - No stored experience buffer

- **Formulation**:
  - Agent follows policy $\pi_t$ at time $t$
  - Observes: $(s_t, a_t, r_t, s_{t+1})$ and immediately updates $\theta_t \rightarrow \theta_{t+1}$
  - No replay buffer; each sample used once
  - On-policy algorithms: SARSA, REINFORCE
  - High variance but low memory; must handle non-stationary data

- **Example 1**: Autonomous Vehicle Learning to Brake
  - Must learn immediately from driving interactions
  - Cannot wait for batch processing
  - Single continuous trajectory through environment

- **Example 2**: Live Online Customer Support
  - Agent learns to respond to customer queries in real-time
  - Receives immediate feedback (customer satisfaction rating)
  - Updates response strategy after each interaction
  - Cannot replay past conversations during deployment

- **Algorithms**:
  - Q-Learning (on-policy)
  - SARSA (State-Action-Reward-State-Action)
  - Policy Gradient (REINFORCE)
  - Actor-Critic (A3C, on-policy variants)
  - Temporal Difference (TD) Learning

### 7B. Batch Learning / Offline RL

- **Setup**:
  - Agent trains on fixed dataset
  - No interaction with environment
  - All data collected in advance

- **Formulation**:
  - Given fixed dataset: $\mathcal{D} = \{(s_i, a_i, r_i, s_i')\}$
  - Optimize offline: $\max_\theta \sum_{(s,a,r,s') \in \mathcal{D}} \log \pi_\theta(a|s) R$
  - Challenge: off-policy learning (data from old policy)
  - Solution: importance sampling or conservative Q-learning to prevent distribution shift

- **Example 1**: Movie Recommendation System
  - Training on historical user interactions
  - No access to live users during training
  - Prevent bad recommendations in production

- **Example 2**: Medical Treatment Policy Learning
  - Historical patient data: (medical state, treatment given, outcome)
  - Cannot experiment on new patients
  - Learn policy from observational data
  - Risk: dataset biases (doctors only tried certain treatments)

- **Algorithms**:
  - Batch Q-Learning
  - Offline RL
  - Behavior Cloning
  - Batch Policy Gradient
  - Conservative Q-Learning (CQL)

### 7C. Replay-based / Experience Replay

- **Setup**:
  - Agent stores experiences in replay buffer
  - Replays for training; combines online and batch
  - Decorrelates samples for stable learning

- **Formulation**:
  - Maintain buffer: $\mathcal{B} = \{(s_i, a_i, r_i, s_i')\}$ of size $N$
  - At each step: (1) act via $\pi_t$, add $(s_t, a_t, r_t, s_{t+1})$ to $\mathcal{B}$
  - (2) sample minibatch from $\mathcal{B}$; (3) update $\theta$ on minibatch
  - Benefits: breaks sample correlation, enables off-policy learning, reuses samples
  - Trade-off: memory overhead, potential stale experience

- **Example 1**: DQN Training on Atari
  - Interacts online with game (stores frames)
  - Stores (state, action, reward, next_state) tuples
  - Trains on random minibatches from replay buffer

- **Example 2**: Robot Learning Manipulation with Data Reuse
  - Robot performs grasping attempts, stores (image, action, success) in buffer
  - Between attempts, trains on past experiences
  - Reuses old grasp attempts multiple times
  - Improves sample efficiency vs. pure online learning

- **Algorithms**:
  - DQN (Deep Q-Network) with Experience Replay
  - Prioritized Experience Replay (PER)
  - Hindsight Experience Replay (HER)
  - Rainbow DQN
  - Off-policy methods with replay buffer

## 8. Solution Concept: How Policy is Represented

### 8A. Value-based Methods

- **Setup**:
  - Learn state or state-action value functions
  - Derive policy greedily from values
  - No explicit policy representation

- **Formulation**:
  - Learn Q-values or state values: $Q(s, a) \approx \mathbb{E}[\sum_t \gamma^t r_t | s_t=s, a_t=a]$ or $V(s) \approx \mathbb{E}[\sum_t \gamma^t r_t | s_t = s]$
  - Deterministic policy: $\pi(s) = \argmax_a Q(s, a)$
  - TD update: $Q(s,a) \leftarrow Q(s,a) + \alpha [r + \gamma \max_a' Q(s', a') - Q(s,a)]$
  - Off-policy and sample-efficient

- **Example 1**: Chess Position Evaluator
  - Assigns numerical value to each board position
  - Policy: play move leading to highest-value next position
  - Value function captures position quality

- **Example 2**: Traffic Signal Control
  - Value function: Q(intersection_state, signal_choice) predicts queue length reduction
  - Policy: select signal that maximizes expected queue clearance
  - Learns which state-action combinations reduce congestion

- **Algorithms**:
  - Q-Learning
  - Value Iteration
  - DQN (Deep Q-Network)
  - Dueling DQN
  - Double Q-Learning

### 8B. Policy-based Methods

- **Setup**:
  - Learn policy directly without explicit value function
  - No intermediate value function needed
  - Direct policy parameterization

- **Formulation**:
  - Parameterize policy: $\pi_\theta(a | s)$ directly
  - Optimize: $\max_\theta \mathbb{E}_{\pi_\theta}[\sum_t \gamma^t r_t]$ via policy gradient
  - Update: $\nabla_\theta J = \mathbb{E}[\nabla_\theta \log \pi_\theta(a|s) Q(s,a)]$ (REINFORCE)
  - On-policy; handles continuous actions; higher variance; no value function

- **Example 1**: Robot Arm Joint Control
  - Learns probability distribution over joint angles
  - Policy outputs action directly (not via value function)
  - Handles continuous action exploration naturally

- **Example 2**: Game NPC Strategy
  - Learns stochastic strategy distribution (aggressive, defensive, evasive)
  - No value function; policy sampled at each decision
  - Exploration comes from action distribution (not epsilon-greedy)
  - Unpredictable to player but learned strategically

- **Algorithms**:
  - Policy Gradient (REINFORCE)
  - PPO (Proximal Policy Optimization)
  - TRPO (Trust Region Policy Optimization)
  - Evolutionary Strategies
  - Natural Policy Gradient

### 8C. Actor-Critic Methods

- **Setup**:
  - Learn both policy (actor) and value function (critic)
  - Critic guides actor training via TD error
  - Combines benefits of value and policy methods

- **Formulation**:
  - Two networks: policy $\pi_\theta(a|s)$ (actor) and value $V_\phi(s)$ (critic)
  - Actor learns: $\nabla_\theta \log \pi_\theta(a|s) A(s,a)$ where advantage $A(s,a) = r + \gamma V_\phi(s') - V_\phi(s)$
  - Critic learns: $V_\phi(s) \leftarrow V_\phi(s) + \alpha [r + \gamma V_\phi(s') - V_\phi(s)]$
  - Benefits: reduces variance vs. policy gradient; more stable than pure value methods

- **Example 1**: Game Playing with Separate Evaluator
  - Actor network: selects moves
  - Critic network: evaluates board positions
  - Critic provides learning signal for actor

- **Example 2**: Robot Locomotion
  - Actor: outputs joint torques for walking
  - Critic: predicts value of current state (how far forward will robot go?)
  - TD error from critic guides actor to take better steps
  - Lower variance than pure policy gradient

- **Algorithms**:
  - A3C (Asynchronous Advantage Actor-Critic)
  - A2C (Advantage Actor-Critic)
  - SAC (Soft Actor-Critic)
  - DDPG (Deep Deterministic Policy Gradient)
  - TD3 (Twin Delayed DDPG)
  - PPO (also uses value baseline)

### 8D. Search/Planning Methods

- **Setup**:
  - Use forward search or tree planning to find actions
  - May use learned model or environment simulator
  - Explicit look-ahead before committing to action

- **Formulation**:
  - Build search tree via simulation at each state $s_t$
  - Expand nodes via model $P(s' | s, a)$ or environment
  - Evaluate leaf at depth $d$ via value function $V(s_d)$ or rollout
  - Backpropagate value up tree
  - Select action: $a^* = \argmax_a N(s,a)$ (visits) or $\argmax_a \frac{Q(s,a)}{N(s,a)} + c\sqrt{\frac{\ln N(s)}{N(s,a)}}$ (UCB)
  - Sample-heavy but asymptotically optimal

- **Example 1**: AlphaGo Playing Chess
  - Uses MCTS to search game tree
  - Searches before playing each move
  - Evaluates leaf nodes with neural network

- **Example 2**: Robot Task Planning (Temporal Reasoning)
  - Robot searches sequence of moves to accomplish multi-step task
  - Uses forward model to predict outcomes
  - Looks ahead 5-10 steps before executing
  - Backtracks if plan leads to failure state

- **Algorithms**:
  - MCTS (Monte Carlo Tree Search)
  - Minimax with Alpha-Beta Pruning
  - A* (A-Star) Search
  - MPC (Model Predictive Control)
  - AlphaGo / AlphaZero
  - MuZero

## 9. Optimality Criterion: Policy Structure and Goal

### 9A. Deterministic Policies

- **Setup**:
  - Policy outputs single action per state
  - No randomness (except in exploration)
  - Greedy policy maximizes value

- **Formulation**:
  - Deterministic policy: $\mu(s) \in \mathcal{A}$
  - Value function: $V(s) = \mathbb{E}[r + \gamma V(s')]$ under $a = \mu(s)$
  - Deterministic policy gradient: $\nabla_\theta J = \mathbb{E}[\nabla_a Q(s,a) \nabla_\theta \mu_\theta(s)|_{a=\mu_\theta(s)}]$
  - Off-policy, sample-efficient
  - Exploration: via epsilon-greedy or noise injection during learning

- **Example 1**: Traffic Light Controller
  - Given road state, always choose same action
  - {State = heavy_left_traffic} → {Action = green_left}
  - No randomness in operation

- **Example 2**: Robot End-Effector Control
  - Learned policy: given vision input, deterministically output target gripper position
  - No stochasticity; same input always produces same action
  - Exploration during training via noise; deterministic during deployment

- **Algorithms**:
  - Deterministic Policy Gradient (DPG)
  - DDPG (Deep Deterministic Policy Gradient)
  - TD3 (Twin Delayed DDPG)
  - Q-Learning (greedy policy)
  - Minimax

### 9B. Stochastic Policies

- **Setup**:
  - Policy outputs probability distribution over actions
  - Agent samples actions from distribution
  - Exploration built into policy

- **Formulation**:
  - Stochastic policy: $\pi(a|s)$
  - Agent samples: $a \sim \pi(\cdot|s)$
  - Value: $V(s) = \mathbb{E}_{a \sim \pi}[r + \gamma V(s')]$
  - Policy gradient: $\nabla_\theta J = \mathbb{E}_{a \sim \pi}[\nabla_\theta \log \pi_\theta(a|s) Q(s,a)]$
  - Exploration intrinsic to policy; handles multimodal actions; more stable

- **Example 1**: Card Game Strategy
  - Randomizes strategy to avoid being predictable
  - Policy outputs: {play_aggressive: 30%, play_conservative: 70%}
  - Exploits opponent's inability to predict exactly

- **Example 2**: Recommendation System with Diversity
  - Stochastic policy: outputs soft distribution over content types
  - Samples recommendations: 40% news, 30% entertainment, 30% educational
  - Exploration avoids getting stuck in local optima
  - Users see diverse content; policy adapts based on long-term preferences

- **Algorithms**:
  - Policy Gradient (REINFORCE)
  - PPO (Proximal Policy Optimization)
  - A3C (Asynchronous Advantage Actor-Critic)
  - SAC (Soft Actor-Critic)
  - Thompson Sampling

### 9C. Optimal Policies

- **Setup**:
  - Find provably best policy
  - Exact optimality or ε-optimal guarantee
  - May be computationally expensive

- **Formulation**:
  - Optimal policy: $\pi^* = \argmax_\pi J(\pi)$ where $J(\pi) = \mathbb{E}[\sum_t \gamma^t r_t]$
  - Optimal value satisfies: $V^*(s) = \max_a [r(s,a) + \gamma \mathbb{E}[V^*(s')]]$ (Bellman)
  - Convergence: value iteration in finite MDPs
  - Continuous spaces: epsilon-optimal via function approximation with error bounds

- **Example 1**: Chess Solver
  - Finding perfect play from any position
  - Can prove move is optimal for that state
  - Uses exhaustive search or strong bounds

- **Example 2**: Optimal Control (Trajectory Optimization)
  - Find exact optimal trajectory minimizing cost: $\min_{a_0, \ldots, a_T} \sum_t c(s_t, a_t)$
  - Uses dynamic programming or gradient-based methods
  - Guarantees solution is globally optimal (for convex cost)
  - Example: power-minimal path for autonomous vehicle

- **Algorithms**:
  - Value Iteration (exact solution)
  - Policy Iteration (exact solution)
  - Minimax with Alpha-Beta Pruning
  - AlphaZero (near-optimal via search + learning)
  - Exhaustive Search (when feasible)

### 9D. Approximate / Satisficing Policies

- **Setup**:
  - Good-enough policy; bounded suboptimality
  - Not necessarily optimal
  - Practical for time/compute constraints

- **Formulation**:
  - $\epsilon$-optimal policy: $\pi^\epsilon$ with guarantee $V^\epsilon(s) \geq V^*(s) - \epsilon$
  - Bounded-depth lookahead: search tree to depth $d$ with error $\leq \epsilon / (1 - \gamma)$
  - Anytime algorithms: stop search after time $T$, return best-found policy
  - Trade-off: suboptimality $\epsilon$ vs. computational cost

- **Example 1**: Real-time Chess Engine
  - Cannot search entire game tree
  - Searches fixed depth in time limit
  - Guaranteed suboptimality, but practical

- **Example 2**: Real-time Robot Obstacle Avoidance
  - Robot must avoid collision within 50ms
  - Cannot compute optimal long-term plan in time
  - Uses greedy/myopic approach: avoid immediate obstacles
  - Satisfactory for safety, not optimal trajectory

- **Algorithms**:
  - Anytime Algorithms
  - Bounded Suboptimality Algorithms
  - Approximate Dynamic Programming
  - Greedy with bounded approximation ratio
  - Satisficing (good enough) methods

## 10. State & Action Space Size: Scalability

### 10A. Small Tabular Problem

- **Setup**:
  - $|S|$ and $|A|$ small enough to store in table (e.g., <10,000 states)

- **Formulation**:
  - Tabular representation: Q-table is $|S| \times |A|$ matrix
  - Value function: $V(s)$ represented as vector of size $|S|$
  - Learning via value iteration: $V(s) \leftarrow \max_a [R(s,a) + \gamma \sum_{s'} P(s'|s,a) V(s')]$
  - Guaranteed convergence to optimal value in finite iterations
  - Exact solution possible

- **Example 1**: Simple Grid World
  - 10x10 grid = 100 states
  - 4 actions (up, down, left, right)
  - Can store full Q-table

- **Example 2**: Simple Inventory Problem
  - 20 possible inventory levels (small state space)
  - 5 order quantities (small action space)
  - Q-table: $20 \times 5$ entries
  - Solves via tabular Q-learning exactly

- **Algorithms**:
  - Tabular Q-Learning
  - Tabular Value Iteration
  - Tabular Policy Iteration
  - MCTS (Monte Carlo Tree Search)

### 10B. Medium: Linear Function Approximation

- **Setup**:
  - $|S|$ or $|A|$ too large for table
  - Use linear function approximation

- **Formulation**:
  - Value approximation: $V(s) \approx w^T \phi(s)$
  - Feature vector: $\phi(s) \in \mathbb{R}^d$ with weights $w \in \mathbb{R}^d$ ($d \ll |S|$)
  - TD learning: $w \leftarrow w + \alpha [r + \gamma V(s') - V(s)] \phi(s)$
  - Covers medium-scale problems; convergence guaranteed under conditions
  - Basis function design is key

- **Example 1**: Adaptive Auction Bidding
  - State features: [price_history, competitor_bids, budget_remaining, ...]
  - Too many unique combinations for table
  - Use linear function: $V(s) = w^T \phi(s)$

- **Example 2**: Online Resource Allocation
  - State: [current_load, queue_length, time_of_day, user_priority, ...]
  - Too many state combinations for table
  - Features: normalize each dimension; use polynomial features
  - Learn weight vector for linear value function

- **Algorithms**:
  - Q-Learning with FA (Function Approximation)
  - SARSA (State-Action-Reward-State-Action) with FA
  - Linear Bandits
  - Contextual Bandits
  - Least-Squares Temporal Difference (LSTD)

### 10C. Large: Deep Neural Networks

- **Setup**:
  - High-dimensional state (images, speech)
  - Large action space; use deep NN

- **Formulation**:
  - Value function: $V(s) = f_\theta(s)$ where $f_\theta$ is deep neural network
  - CNN for image inputs
  - Learning: $\theta \leftarrow \theta + \alpha [r + \gamma \max_a f_{\theta'}(s') - f_\theta(s)] \nabla_\theta f_\theta(s)$
  - Challenges: non-stationary targets, off-policy data
  - Solutions: experience replay, target networks
  - Asymptotically optimal but high sample complexity

- **Example 1**: Self-Driving Car
  - State: camera image (1920×1440×3 pixels = huge)
  - Action: continuous steering/acceleration
  - Need deep network to extract features

- **Example 2**: Playing Atari Games
  - State: game screen (84x84 pixels, 3 color channels)
  - Action: 18 discrete actions (game-specific)
  - CNN extracts visual features (sprites, terrain, items)
  - DQN learns Q-values for different game situations

- **Algorithms**:
  - DQN (Deep Q-Network, variants: Double, Dueling, Rainbow)
  - Policy Gradient with NN (Neural Network)
  - A3C (Asynchronous Advantage Actor-Critic)
  - PPO (Proximal Policy Optimization)
  - TRPO (Trust Region Policy Optimization)
  - SAC (Soft Actor-Critic)
  - TD3 (Twin Delayed DDPG)
  - Evolutionary Strategies
