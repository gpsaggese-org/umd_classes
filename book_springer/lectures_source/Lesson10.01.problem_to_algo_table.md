# Taxonomy of Decision-Making Problems and Algorithm Solutions

## 1. Observability

| Problem Type | Characteristics | Potential Algorithms |
|---|---|---|
| **Fully Observable (MDP)** | Agent observes complete state each step; no hidden information | Q-Learning, SARSA, Value Iteration, Policy Iteration, MCTS |
| **Partially Observable (POMDP)** | Observations don't uniquely determine state; agent maintains belief state | Particle Filtering, Kalman Filter, POMCP, Belief-State Planning |
| **Hidden State (HMM)** | Environment has hidden state; observations are noisy/stochastic | Hidden Markov Models, Kalman Filter, Extended/Unscented KF, Particle Filters |

## 2. Time Horizon

| Problem Type | Characteristics | Potential Algorithms |
|---|---|---|
| **One-Step (Bandit)** | No future consequences; optimize immediate reward only | ε-Greedy, UCB (Upper Confidence Bound), Thompson Sampling, Contextual Bandits |
| **Finite Horizon** | Fixed number of steps H; consider consequences over horizon | Minimax, Alpha-Beta Pruning, A*, RRT, MCTS |
| **Infinite Horizon** | Process never terminates; balance immediate vs. long-term via discount γ | Q-Learning, SARSA, Value/Policy Iteration, Actor-Critic, DQN, PPO, SAC |
| **Episodic/Fixed Episode Length** | Task runs for fixed episode length T, then resets | Monte Carlo methods, MCTS, Policy Gradient (REINFORCE) |

## 3. Action Space

| Problem Type | Characteristics | Potential Algorithms |
|---|---|---|
| **Discrete** | Action set is finite and enumerable | Q-Learning, DQN, MCTS, Minimax, Value Iteration |
| **Continuous** | Action space is uncountably infinite ℝⁿ | DDPG, TD3, SAC, PPO (continuous), Policy Gradient, Evolutionary Strategies |
| **Hybrid (Mixed Discrete-Continuous)** | Some actions discrete, some continuous; hierarchical decision | Branching DQN, Hierarchical RL, Multi-task Learning |

## 4. Multi-Agent Interaction

| Problem Type | Characteristics | Potential Algorithms |
|---|---|---|
| **Single-Agent** | One decision-maker, one objective; no strategic interaction | Q-Learning, DQN, SARSA, PPO, Actor-Critic |
| **Multi-Agent Cooperative** | n agents share one objective; must coordinate actions | QMIX, MAPPO, MAAC, MADDPG, CommNet |
| **Multi-Agent Competitive** | Agents have conflicting objectives; game theory and Nash equilibrium apply | Minimax + Alpha-Beta, Self-Play, CFR (Counterfactual Regret Minimization), Nash Solvers |

## 5. Information Structure

| Problem Type | Characteristics | Potential Algorithms |
|---|---|---|
| **Perfect Information** | All players know all relevant information; entire game tree visible | Minimax + Alpha-Beta, Negamax, MCTS, AlphaZero, Exact solvers |
| **Imperfect Information** | Hidden moves or hidden state; players act on beliefs | CFR, Regret Matching, Nash Solvers, Information-Set Abstraction |
| **Asymmetric Information** | Players have fundamentally different information sets; principal-agent problems | Mechanism Design, Bayesian Games, Signaling Equilibria, Information-dependent policies |

## 6. Model Knowledge

| Problem Type | Characteristics | Potential Algorithms |
|---|---|---|
| **Model-Based** | Agent has (or learns) a world model; plans without touching real environment | Value/Policy Iteration, Dyna-Q, MCTS, AlphaGo, MuZero |
| **Model-Free** | Agent has no model; learns directly from trial-and-error experience | Q-Learning, SARSA, REINFORCE, Actor-Critic, DQN, PPO, SAC, A3C |

## 7. Update Mechanism

| Problem Type | Characteristics | Potential Algorithms |
|---|---|---|
| **Online Learning** | Learn and act in real time on single trajectory; each sample used once | SARSA, TD Learning, REINFORCE, on-policy Actor-Critic (A3C) |
| **Batch Learning (Offline RL)** | Train on fixed dataset with no environment interaction; addresses distribution shift | Batch Q-Learning, Offline RL, Behavior Cloning, Conservative Q-Learning (CQL) |
| **Replay-based (Experience Replay)** | Store experiences in buffer and replay; combines online acting with batch updates | DQN with Experience Replay, Prioritized ER (PER), Hindsight ER (HER), Rainbow DQN |

## 8. Solution Concept

| Problem Type | Characteristics | Potential Algorithms |
|---|---|---|
| **Value-based Methods** | Learn Q/V values, then act greedily; no explicit policy stored | Q-Learning, Value Iteration, DQN, Double DQN, Dueling DQN |
| **Policy-based Methods** | Learn policy directly; no intermediate value function | REINFORCE, PPO, TRPO, Natural Policy Gradient, Evolutionary Strategies |
| **Actor-Critic Methods** | Actor picks actions, critic evaluates them; critic reduces variance | A2C, A3C, SAC, DDPG, TD3, PPO (with value baseline) |
| **Search/Planning Methods** | Look ahead by building tree at decision time; use model or simulator | MCTS, Minimax + Alpha-Beta, A*, MPC, AlphaZero, MuZero |

## 9. Optimality Criterion

| Problem Type | Characteristics | Potential Algorithms |
|---|---|---|
| **Deterministic Policies** | One fixed action per state; randomness only during exploration | DPG, DDPG, TD3, greedy Q-Learning, Minimax |
| **Stochastic Policies** | Output distribution over actions; exploration built into policy | REINFORCE, PPO, A3C, SAC, Thompson Sampling |
| **Optimal Policies** | Find provably best policy—exact or ε-optimal | Value/Policy Iteration, Minimax + Alpha-Beta, AlphaZero, Exhaustive Search |
| **Approximate/Satisficing Policies** | Accept good-enough policy with bounded suboptimality; limited time/compute | Anytime Algorithms, Approximate Dynamic Programming, Bounded Suboptimality |

## 10. State-Action Space Size

| Problem Type | Characteristics | Potential Algorithms |
|---|---|---|
| **Small Tabular** | State and action spaces small enough for lookup table (<10k states) | Tabular Q-Learning, Tabular Value/Policy Iteration, MCTS |
| **Medium: Linear Function Approximation** | State space too large for table; compress via features | Q-Learning/SARSA with FA, LSTD, Linear Bandits, Contextual Bandits |
| **Large: Deep Neural Networks** | High-dimensional inputs (images, speech); learned feature extraction | DQN, A3C, PPO, TRPO, SAC, TD3, Rainbow DQN |
