# Tutorial Plan: Decision-Making Algorithms (Lesson 10.01)

// From book.springer/lectures_source/Lesson10.01_Taxonomy_of_Decision_Problems.txt

- This plan covers the algorithms listed in the lecture

- For each algorithm the plan gives:
  - A simple example problem
  - A brute-force baseline
  - The Python packages that apply
  - A sketch of a package-based solution

```
- Read the algorithms in
  book.springer/lectures_source/Lesson10.01_Taxonomy_of_Decision_Problems.txt

- Come up with a plan for each of the algorithms to
  - Have the description of a simple Python example of a problem explaining the
    algorithm (using the example in the slides or a "famous one" in the literature)
  - A "brute" force solution
  - Point to the Python packages that can be used to solve the problem
  - Sketch how to solve the problem using one of the packages

- Do not write code, but only write 10 nested bullet points per algorithm
```

## 1. Q-Learning

- **Example problem**:
  - `FrozenLake` grid navigation
  - An agent crosses a slippery frozen lake to a goal without falling into holes
    (a canonical off-policy control benchmark that mirrors the slides' grid
    world)
  - State is the tile index on a 4x4 grid, actions are $\{$left, down, right,
    up$\}$, and reward is 1 only on reaching the goal
- **Brute-force solution**:
  - Enumerate every deterministic policy (one action per state)
  - Score each by many Monte Carlo rollouts, keeping the best
  - Infeasible: with 16 states and 4 actions there are $4^{16}$ policies, and
    each needs many noisy rollouts to rank reliably
- **Python packages**:
  - `gymnasium`
  - `pymdptoolbox`
- **Solution sketch**: learn the Q-table online with `gymnasium`
  - Initialize $Q$ to zeros and, for each episode, pick actions
    $\varepsilon$-greedily from the current $Q$
  - After each transition apply the TD update
    $$
    Q(s,a) \leftarrow Q(s,a) + \alpha[r + \gamma \max_{a'} Q(s',a') - Q(s,a)]
    $$
  - Decay $\varepsilon$ over episodes, then read off the greedy policy
    $\argmax_a Q(s,a)$

## 2. SARSA

- **Example problem**:
  - `CliffWalking` gridworld navigation where an agent walks an edge next to a
    cliff and falling off costs -100 (Sutton and Barto's classic
    SARSA-vs-Q-Learning example)
  - SARSA learns the safer path away from the cliff because it accounts for its
    own exploratory missteps
  - State is the tile position, actions are $\{$left, down, right, up$\}$, and
    reward is -1 per step with -100 penalty for cliff
- **Brute-force solution**:
  - Enumerate all deterministic policies and evaluate each by averaging returns
    over many rollouts
  - Select the highest-valued policy
  - Exponential in the number of states and wasteful because it ignores the
    structure TD updates exploit
- **Python packages**:
  - `gymnasium` (`CliffWalking-v0`) for the environment
  - `numpy` for the Q-table storage
- **Solution sketch**: on-policy TD control with `gymnasium` and `numpy`
  - Initialize $Q$ to zeros and, for each episode, choose action $a$
    $\varepsilon$-greedily from current $Q$
  - After the step, choose the next action $a'$ from the same $\varepsilon$-greedy
    policy (on-policy property)
  - Apply the TD update: $Q(s,a) \leftarrow Q(s,a) + \alpha[r + \gamma Q(s',a') - Q(s,a)]$
  - Decay $\varepsilon$ over episodes so the learned policy stays near the safe
    route away from the cliff

## 3. Value Iteration

- **Example problem**:
  - 4x3 grid world MDP (Russell and Norvig) with known transition noise (80%
    intended, 20% slip) and +1/-1 terminals matching the slides' inventory MDP
  - The dynamics $P(s'|s,a)$ and reward $R(s,a)$ are fully known
  - No environment interaction needed, only computation over the known model
- **Brute-force solution**:
  - Enumerate all deterministic policies and solve each policy's value exactly
  - Select the highest-valued policy
  - Combinatorial explosion: there are $|\mathcal{A}|^{|\mathcal{S}|}$ policies,
    each requiring a linear-system solve
- **Python packages**:
  - `pymdptoolbox` for value iteration algorithm
  - `numpy` for the $P$ (transition) and $R$ (reward) arrays
- **Solution sketch**: iterate the Bellman optimality backup with `pymdptoolbox`
  - Encode $P$ as an $|\mathcal{A}| \times |\mathcal{S}| \times |\mathcal{S}|$
    array and $R$ as a matrix
  - Repeatedly apply $V(s) \leftarrow \max_a [R(s,a) + \gamma \sum_{s'} P(s'|s,a) V(s')]$
    until convergence (value change drops below threshold)
  - Extract the greedy policy from the converged value function

## 4. Policy Iteration

- **Example problem**:
  - Jack's Car Rental (Sutton and Barto) — move cars between two lots overnight
    to maximize rental income, a known-model MDP
  - The 4x3 grid world also works as a simpler alternative
  - The rewards and Poisson rental/return dynamics are fully known, enabling
    planning without environment interaction
- **Brute-force solution**:
  - Enumerate every deterministic policy and evaluate each exactly
  - Select the best policy
  - Suffers combinatorial blow-up like value iteration, but policy iteration
    converges in far fewer sweeps
- **Python packages**:
  - `pymdptoolbox` (`mdptoolbox.mdp.PolicyIteration`)
  - `numpy` for the $P$ and $R$ arrays
- **Solution sketch**: alternate evaluation and improvement with `pymdptoolbox`
  - Start from an arbitrary policy and evaluate it by solving the linear Bellman
    system for $V^\pi$
  - Improve greedily: $\pi(s) \leftarrow \argmax_a [R(s,a) + \gamma \sum_{s'} P(s'|s,a) V^\pi(s')]$
  - Repeat evaluation and improvement until the policy stops changing, which
    converges in finite steps

## 5. Monte Carlo Tree Search (MCTS)

- **Example problem**:
  - Tic-Tac-Toe move selection (the slides' running example) to search which
    move to play from the current board
  - The same method scales to Connect Four and Go
  - State is a board configuration, actions are empty cells, and reward is +1
    for win / 0 for draw / -1 for loss at terminal state
- **Brute-force solution**:
  - Full minimax over the entire game tree, backing up win/loss values from
    leaves
  - Works for Tic-Tac-Toe but branching factor makes it intractable for larger
    games like Go
- **Python packages**:
  - `mcts` for generic UCT algorithm
  - `open_spiel` (DeepMind) for game algorithms
  - `easyAI` for minimax baseline comparison
- **Solution sketch**: run UCT with the `mcts` package
  - Selection: descend the tree by the UCB score $\frac{Q(s,a)}{N(s,a)} + c\sqrt{\frac{\ln N(s)}{N(s,a)}}$
  - Expansion and simulation: add a child node and play a random rollout to
    terminal reward
  - Backpropagate the result up the visited path, then after fixed iteration
    budget play the most-visited child

## 6. Multi-Armed Bandits (ε-Greedy, UCB, Thompson Sampling)

- **Example problem**:
  - Online ad selection across $k$ ads (one-step, no state)
  - Agent must trade off exploration and exploitation over $T$ rounds to
    maximize clicks
  - No transitions, only a reward distribution $\mu_a$ per arm $a$
- **Brute-force solution**:
  - Round-robin every arm equally for the whole horizon
  - Pick the empirically best arm only at the very end
  - Wastes reward pulling visibly bad arms the entire time: regret grows
    linearly in $T$ instead of logarithmically
- **Python packages**:
  - `mabwiser`
  - `river` (bandit module)
- **Solution sketch**: run UCB1 with `mabwiser`
  - Track pull count $N(a)$ and empirical mean reward $\hat\mu(a)$ per arm
  - Each round pick $a^* = \argmax_a \hat\mu(a) + c\sqrt{\ln t / N(a)}$
  - Update $\hat\mu(a)$ after observing the reward; the confidence bonus
    shrinks as an arm is pulled more, forcing exploration only while uncertain

## 7. Minimax and Alpha-Beta Pruning

- **Example problem**:
  - Tic-Tac-Toe or a small Chess endgame move selection
  - Zero-sum, perfect-information, two-player game
  - State is the board, actions are legal moves, reward is +1/0/-1 at a
    terminal state
- **Brute-force solution**:
  - Expand the entire game tree to terminal states
  - Back up win/loss/draw values without pruning
  - Branching factor $b$ and depth $d$ give $O(b^d)$ nodes, intractable beyond
    small games like Tic-Tac-Toe
- **Python packages**:
  - `easyAI`
  - `python-chess` for board representation
- **Solution sketch**: alpha-beta search with `easyAI`
  - Maintain bounds $\alpha$ (best guaranteed for the maximizer) and $\beta$
    (best guaranteed for the minimizer) while recursing
  - Prune a branch once $\alpha \geq \beta$, since it cannot change the final
    decision
  - Order moves (e.g., captures first) to prune earlier, approaching the
    $O(b^{d/2})$ best case

## 8. A\* Search and RRT

- **Example problem**:
  - Grid/graph shortest-path robot navigation with a known map (A\*)
  - Continuous-space motion planning for a robot arm around obstacles (RRT)
  - State is a node or configuration, actions move to a neighbor, cost is path
    length
- **Brute-force solution**:
  - Uniform-cost search (Dijkstra): explore every node in non-decreasing cost
    order
  - No heuristic guidance toward the goal
  - Wastes work exploring irrelevant directions
- **Python packages**:
  - `networkx` (`astar_path`) for discrete graphs
  - `ompl` bindings for RRT in continuous configuration spaces
- **Solution sketch**: A\* with `networkx`
  - Maintain an open set ordered by $f(n) = g(n) + h(n)$ (cost so far plus an
    admissible heuristic)
  - Pop the lowest-$f$ node, expand its neighbors, update $g$ if improved
  - Terminate when the goal is popped; the heuristic (e.g., Euclidean
    distance) directs search toward the goal, pruning irrelevant expansion

## 9. Particle Filter

- **Example problem**:
  - Robot localization in a known map from noisy sensor readings
  - Partially observable, continuous hidden state (position)
  - Observation is a noisy sensor reading, hidden state is the true pose
- **Brute-force solution**:
  - Discretize the state space into a fine grid
  - Update the entire probability grid via Bayes' rule at every step
  - Grid size scales exponentially with state dimension, infeasible beyond
    2-3 continuous dimensions
- **Python packages**:
  - `filterpy`
  - `pfilter`
- **Solution sketch**: sequential importance resampling with `filterpy`
  - Maintain a weighted particle set $\{s^{(i)}, w^{(i)}\}$ approximating the
    belief
  - Propagate each particle through the motion model, then reweight by the
    observation likelihood $O(o|s^{(i)})$
  - Resample particles proportional to weight to avoid degeneracy, then
    estimate the state as the weighted mean

## 10. Kalman Filter (and Extended / Unscented Variants)

- **Example problem**:
  - Tracking a moving object's position and velocity from noisy sensor
    readings
  - Linear-Gaussian dynamics for the standard Kalman filter, nonlinear
    dynamics for EKF/UKF
  - Hidden state is the true position/velocity, observation is a noisy sensor
    reading
- **Brute-force solution**:
  - Full Bayesian update over a discretized state grid, same as the particle
    filter case
  - Recompute the full posterior every step
  - Exponential cost in state dimension, wasteful when dynamics are
    linear-Gaussian and admit a closed form
- **Python packages**:
  - `filterpy` (`KalmanFilter`, `ExtendedKalmanFilter`, `UnscentedKalmanFilter`)
- **Solution sketch**: linear Kalman filter with `filterpy`
  - Predict: propagate mean and covariance through the linear dynamics
    $x_{t+1} = Ax_t + w$
  - Update: compute the Kalman gain from the measurement noise covariance,
    correct the prediction with the new observation
  - For nonlinear dynamics, linearize with EKF (Jacobians) or use
    unscented sigma-points with UKF, keeping the same predict/update structure

## 11. Hidden Markov Model (Forward-Backward and Viterbi)

- **Example problem**:
  - Speech recognition: infer the true phoneme sequence from noisy acoustic
    features
  - Weather inference from a drifting sensor
  - Hidden state transitions latently, observations are noisy emissions
- **Brute-force solution**:
  - Enumerate every possible hidden state sequence
  - Score each of $|\mathcal{S}|^T$ sequences by its joint likelihood and keep
    the best (or sum for the marginal)
  - Exponential in sequence length $T$, infeasible beyond a handful of steps
- **Python packages**:
  - `hmmlearn`
  - `pomegranate`
- **Solution sketch**: dynamic programming with `hmmlearn`
  - Forward-backward computes marginals $\Pr(s_t | o_{1:T})$ in
    $O(T|\mathcal{S}|^2)$ via recursive forward $\alpha_t$ and backward
    $\beta_t$ messages
  - Viterbi finds the single most likely hidden sequence by replacing sums
    with max in the same recursion
  - Baum-Welch (EM) fits the transition/emission parameters when unknown

## 12. POMCP (Partially Observable Monte Carlo Planning)

- **Example problem**:
  - Robot navigation with uncertain sensor readings (Tiger problem or a
    partially observable grid world)
  - Belief over hidden states must be tracked and planned over
  - Actions affect both the true state and future observations
- **Brute-force solution**:
  - Convert the belief distribution into a continuous belief-MDP state
  - Run value iteration over the belief simplex
  - Belief space is continuous and high-dimensional; exact solution suffers
    the "curse of dimensionality" and "curse of history"
- **Python packages**:
  - `pomdp-py`
- **Solution sketch**: run POMCP with `pomdp-py`
  - Represent the belief implicitly as a particle set sampled from the
    posterior over states
  - Run MCTS over histories: sample a state from the belief particles, act,
    observe, and descend the matching observation branch
  - Backpropagate returns as in MCTS; after a fixed budget, act with the
    most-visited action and update the belief particles with the real
    observation

## 13. Deep Q-Network (DQN) and Variants

- **Example problem**:
  - Atari game playing from raw pixels
  - Large discrete action space, high-dimensional observation
  - State is the stacked screen frames, actions are the joystick/button
    combinations
- **Brute-force solution**:
  - Tabular Q-Learning treating every distinct pixel frame as a separate
    table row
  - State space is astronomically large; the table never fits in memory
  - States are essentially never revisited exactly, so the table never fills
    in
- **Python packages**:
  - `stable-baselines3`
  - `gymnasium`
- **Solution sketch**: train DQN with `stable-baselines3`
  - Approximate $Q(s,a;\theta)$ with a CNN taking stacked frames as input
  - Store transitions in a replay buffer, sample random minibatches to
    decorrelate updates
  - Use a slowly-updated target network to compute the TD target, stabilizing
    the moving-target problem
  - Variants: Double DQN reduces overestimation, Dueling DQN separates
    value/advantage streams, Prioritized/Rainbow DQN combine several such
    improvements

## 14. REINFORCE (Policy Gradient)

- **Example problem**:
  - Game NPC or robot arm control learning a stochastic policy directly
  - Episodic task with a well-defined return at the end
  - Actions sampled from a parameterized distribution $\pi_\theta(a|s)$
- **Brute-force solution**:
  - Random search over policy parameters
  - Sample random parameter vectors, run full episodes, keep the
    best-scoring parameters
  - No gradient signal used; sample-inefficient and does not scale past a
    handful of parameters
- **Python packages**:
  - `tianshou`
  - `torch` for a custom training loop
- **Solution sketch**: Monte Carlo policy gradient with `tianshou`
  - Parameterize $\pi_\theta(a|s)$, roll out a full episode, compute the
    return $G_t$ from each timestep onward
  - Update $\theta \leftarrow \theta + \alpha \nabla_\theta \log
    \pi_\theta(a_t|s_t)\, G_t$, an unbiased but high-variance gradient
    estimator
  - Subtract a baseline (e.g., average return) to reduce variance without
    introducing bias

## 15. Proximal Policy Optimization (PPO)

- **Example problem**:
  - Robot locomotion or continuous control (e.g., MuJoCo Humanoid)
  - Also used on Atari for stable large-scale training
  - Needs stable updates across many parallel environment workers
- **Brute-force solution**:
  - Vanilla policy gradient with large, unconstrained steps
  - Apply REINFORCE-style updates with a fixed large learning rate
  - Large updates can collapse the policy irrecoverably since the state
    distribution shifts with the new policy
- **Python packages**:
  - `stable-baselines3`
  - `ray[rllib]`
- **Solution sketch**: train PPO with `stable-baselines3`
  - Collect rollouts with the current policy, compute advantage estimates
    (e.g., GAE)
  - Optimize a clipped surrogate objective
    $\min(r_t(\theta)A_t, \text{clip}(r_t(\theta), 1-\epsilon, 1+\epsilon)A_t)$
    where $r_t(\theta) = \pi_\theta / \pi_{\theta_{old}}$
  - Run several epochs of minibatch SGD per rollout batch; the clip keeps the
    new policy close to the old one, avoiding destructive updates

## 16. Trust Region Policy Optimization (TRPO)

- **Example problem**:
  - Same continuous-control benchmarks as PPO (its predecessor)
  - Cases where a monotonic-improvement guarantee matters
  - Needs updates that provably do not degrade the policy
- **Brute-force solution**:
  - Unconstrained policy gradient ascent (vanilla or natural gradient)
  - Take a step with no explicit constraint on how far the policy moves
  - Can overshoot and degrade performance irrecoverably, the same failure
    mode PPO/TRPO were designed to avoid
- **Python packages**:
  - `sb3-contrib` (`TRPO`)
  - `garage`
- **Solution sketch**: constrained natural-gradient step with `sb3-contrib`
  - Estimate the policy gradient and the Fisher information matrix over
    sampled trajectories
  - Solve for the step direction via conjugate gradient, then line-search the
    step size subject to a KL-divergence trust-region constraint
    $D_{KL}(\pi_{old}, \pi_{new}) \leq \delta$
  - The trust region provably guarantees the new policy's performance does
    not decrease

## 17. Deep Deterministic Policy Gradient (DDPG)

- **Example problem**:
  - Continuous robot arm control (e.g., reaching a target with continuous
    joint torques)
  - Off-policy learning from a replay buffer
  - Deterministic action output rather than a distribution
- **Brute-force solution**:
  - Discretize the continuous action space into bins
  - Apply tabular/DQN-style Q-Learning over the binned actions
  - Fine discretization needed for precision blows up the action count
    exponentially with action dimension
- **Python packages**:
  - `stable-baselines3`
- **Solution sketch**: train DDPG with `stable-baselines3`
  - Learn a deterministic actor $\mu_\theta(s)$ and a critic $Q_\phi(s,a)$
    off-policy from a replay buffer
  - Critic update: minimize the TD error using a target actor/critic pair for
    stability
  - Actor update: ascend $\nabla_\theta J = \EE[\nabla_a Q_\phi(s,a)
    |_{a=\mu_\theta(s)} \nabla_\theta \mu_\theta(s)]$
  - Add exploration noise (e.g., Ornstein-Uhlenbeck) to the deterministic
    action during data collection

## 18. Twin Delayed DDPG (TD3)

- **Example problem**:
  - Same continuous-control tasks as DDPG, where DDPG's value overestimation
    causes instability
  - Needs more stable critic estimates
  - Off-policy learning from a replay buffer
- **Brute-force solution**:
  - Same discretized-action tabular approach as DDPG
  - Same combinatorial blow-up in the action count
- **Python packages**:
  - `stable-baselines3`
- **Solution sketch**: train TD3 with `stable-baselines3`
  - Maintain twin critics $Q_{\phi_1}, Q_{\phi_2}$ and take their minimum as
    the TD target to counter overestimation bias
  - Delay actor (and target network) updates relative to critic updates for
    more stable learning
  - Add clipped noise to the target action ("target policy smoothing") to
    avoid exploiting sharp Q-function errors

## 19. Soft Actor-Critic (SAC)

- **Example problem**:
  - Continuous control (e.g., robot locomotion) where sample efficiency and
    stable exploration both matter
  - Off-policy learning with a stochastic policy
  - Maximum-entropy objective favoring diverse behavior
- **Brute-force solution**:
  - Same discretized-action enumeration as DDPG/TD3
  - Same exponential blow-up in the action count
- **Python packages**:
  - `stable-baselines3`
- **Solution sketch**: train SAC with `stable-baselines3`
  - Learn a stochastic actor $\pi_\theta(a|s)$ and twin critics with the
    maximum-entropy objective
    $J = \EE[\sum_t r_t + \alpha \mathcal{H}(\pi(\cdot|s_t))]$
  - The entropy bonus keeps exploration high and avoids premature
    convergence to a deterministic policy
  - The temperature $\alpha$ is auto-tuned to hit a target entropy, removing
    a sensitive hyperparameter

## 20. Advantage Actor-Critic (A2C / A3C)

- **Example problem**:
  - General RL benchmark (e.g., Atari) where policy-gradient variance needs
    reduction without a full replay buffer
  - Needs decorrelated experience without storing transitions
  - Suits many parallel environment workers
- **Brute-force solution**:
  - REINFORCE without a critic baseline
  - Use only the raw Monte Carlo return as the learning signal
  - High variance from full-episode returns makes learning slow and
    unstable, especially with long episodes
- **Python packages**:
  - `stable-baselines3` (A2C)
  - `ray[rllib]` (A3C)
- **Solution sketch**: train A2C with `stable-baselines3`
  - Actor and critic share a network trunk; the critic estimates $V_\phi(s)$
  - Compute the advantage $A(s,a) = r + \gamma V_\phi(s') - V_\phi(s)$ and use
    it in place of the raw return in the policy gradient
  - A3C parallelizes many workers with asynchronous gradient updates to a
    shared model (A2C synchronizes them instead), decorrelating experience
    without a replay buffer

## 21. Evolutionary Strategies

- **Example problem**:
  - Continuous control or neural network policy optimization when gradients
    are unavailable or unreliable
  - Non-differentiable reward signal
  - Black-box optimization of policy parameters
- **Brute-force solution**:
  - Random restart hill climbing
  - Randomly perturb parameters, keep the perturbation only if it improves
    the return, else discard it
  - No use of population structure or ranking; converges slowly and gets
    stuck in local optima
- **Python packages**:
  - `cma` (CMA-ES)
  - `deap`, `evosax`
- **Solution sketch**: run CMA-ES with `cma`
  - Sample a population of parameter vectors from a multivariate Gaussian
    $\theta_i \sim \mathcal{N}(m, \sigma^2 C)$
  - Evaluate each candidate's episodic return, then update the mean toward
    the top-ranked candidates
  - Adapt the covariance matrix $C$ to reshape the search distribution along
    promising directions, repeat until convergence

## 22. Dyna-Q

- **Example problem**:
  - Grid-world navigation where both real environment interaction and a
    learned model can be exploited
  - Model-based planning combined with model-free learning
  - Wants faster convergence than pure Q-Learning
- **Brute-force solution**:
  - Pure model-free Q-Learning with no planning
  - Only update $Q$ from real environment transitions, one per real step
  - Wastes the information already gathered in the model; needs many more
    real-world samples to converge
- **Python packages**:
  - `gymnasium` with a custom loop and `numpy` (no widely-used dedicated
    package)
- **Solution sketch**: interleave real and simulated updates
  - After each real transition $(s,a,r,s')$, apply the normal Q-Learning
    update and also record it in a learned model $\hat{P}, \hat{R}$
  - Between real steps, sample $k$ previously-seen $(s,a)$ pairs and replay
    simulated transitions from $\hat{P}, \hat{R}$ through the same
    Q-Learning update
  - The simulated ("planning") updates accelerate convergence without any
    extra real-environment interaction

## 23. AlphaZero and MuZero

- **Example problem**:
  - Go/Chess/Shogi move selection with known rules (AlphaZero)
  - Atari-style games with unknown dynamics (MuZero)
  - Huge branching factor where plain MCTS rollouts are too noisy
- **Brute-force solution**:
  - Full MCTS with random rollouts and no learned evaluation
  - Use a uniform random rollout policy with no value network to guide search
  - Needs enormous simulation counts to get a reliable estimate in games with
    huge branching factor like Go
- **Python packages**:
  - `open_spiel` (DeepMind)
- **Solution sketch**: train self-play MCTS with a learned model using
  `open_spiel`
  - Guide MCTS's selection step with a policy-value network
    $(\pi_\theta, v_\theta)$ instead of random rollouts
  - Generate training data via self-play games, then fit $\theta$ so
    $\pi_\theta$ matches the MCTS visit-count policy and $v_\theta$ matches
    the game outcome
  - MuZero extends this by additionally learning a latent dynamics model, so
    planning happens in a learned representation rather than requiring known
    game rules

## 24. Counterfactual Regret Minimization (CFR) and Self-Play

- **Example problem**:
  - Heads-up poker betting strategy
  - Imperfect information: hidden hole cards
  - Two-player zero-sum extensive-form game
- **Brute-force solution**:
  - Enumerate and solve the full extensive-form game as a linear program
  - Solve for a Nash equilibrium directly over the full strategy space
  - Strategy space is exponential in the number of information sets;
    infeasible for real poker-sized games
- **Python packages**:
  - `open_spiel` (CFR solvers)
- **Solution sketch**: run CFR self-play with `open_spiel`
  - Track cumulative regret per information set for each action not taken
  - Update the current strategy proportional to positive regret (regret
    matching), average strategies over iterations
  - Repeated self-play iterations converge the average strategy to a Nash
    equilibrium in two-player zero-sum games

## 25. Mechanism Design (Principal-Agent Contracts)

- **Example problem**:
  - Employer designs a compensation contract for a worker whose effort is
    unobserved (moral hazard)
  - Insurer screens buyers of unknown risk (adverse selection)
  - Principal must incentivize an agent it cannot fully observe
- **Brute-force solution**:
  - Enumerate all possible contracts over a discretized payment grid
  - Grid every possible payment schedule $c(y)$ over discretized output
    levels and check the agent's best response for each
  - Contract space is a function, so the grid size explodes with the number
    of output levels and precision needed
- **Python packages**:
  - `scipy.optimize`
  - `cvxpy`, `pyomo`
- **Solution sketch**: solve the constrained optimization with
  `scipy.optimize`
  - Formulate the principal's objective subject to the agent's
    incentive-compatibility and participation constraints
  - Solve the agent's best-response problem for a candidate contract family
  - Optimize the contract parameters (e.g., linear-in-output payment) via
    constrained nonlinear programming subject to those constraints

## 26. Multi-Agent Cooperative RL (QMIX, MAPPO)

- **Example problem**:
  - Warehouse robot team jointly minimizing delivery time
  - Single shared team reward across $n$ agents
  - Decentralized execution required at deployment
- **Brute-force solution**:
  - Centralized joint-action Q-Learning
  - Treat the joint action space $\mathcal{A}_1 \times \cdots \times
    \mathcal{A}_n$ as one giant discrete action set and run tabular
    Q-Learning over it
  - Joint action space grows exponentially with the number of agents;
    infeasible beyond a couple of agents
- **Python packages**:
  - `ray[rllib]` (QMix, MADDPG)
  - `pymarl`, `epymarl`
- **Solution sketch**: train QMIX with `ray[rllib]`
  - Each agent learns its own local $Q_i(s_i, a_i)$ using only local
    observations (decentralized execution)
  - A mixing network combines the per-agent $Q_i$ into a joint $Q_{tot}$
    during centralized training, constrained to be monotonic in each $Q_i$
  - Train the mixing network end-to-end on the shared team reward; at
    execution time agents act only on their local $Q_i$, no communication
    needed

## 27. Conservative Q-Learning (Offline RL)

- **Example problem**:
  - Learning a medical treatment policy from a fixed historical dataset
  - No ability to experiment on new patients
  - Purely offline, off-policy data
- **Brute-force solution**:
  - Standard off-policy Q-Learning treated as if the static dataset were
    online replay
  - Run vanilla Q-Learning updates over the fixed dataset
  - The learned policy exploits over-optimistic Q-values on state-actions
    absent from the data (distribution shift), performing badly once
    deployed
- **Python packages**:
  - `d3rlpy`
- **Solution sketch**: train CQL with `d3rlpy`
  - Fit $Q_\phi$ on the fixed dataset via the standard TD loss
  - Add a conservative penalty that pushes down Q-values for actions not seen
    in the data (and up for actions that were), producing a lower-bound
    estimate
  - Extract the greedy policy from the conservative Q-function; the
    pessimism keeps it from favoring unseen, unreliable actions

## 28. Model Predictive Control (MPC)

- **Example problem**:
  - Trajectory optimization for a robot or vehicle with a known dynamics
    model
  - Needs continuous replanning to react to disturbances
  - Known transition dynamics, continuous state and action
- **Brute-force solution**:
  - Solve the entire infinite-horizon control problem once and fix the plan
  - Optimize one long open-loop trajectory upfront and execute it without
    ever replanning
  - Cannot react to disturbances or model error; small deviations compound
    over a long open-loop trajectory
- **Python packages**:
  - `do-mpc`
  - `casadi`
- **Solution sketch**: receding-horizon control with `do-mpc`
  - At each timestep, optimize a finite-horizon (e.g., $H=10$) sequence of
    actions against the known dynamics model
  - Execute only the first action from the optimized sequence
  - Re-optimize from the new state at the next timestep, continually
    correcting for any drift or disturbance

## 29. Hierarchical RL

- **Example problem**:
  - Manufacturing robot choosing a tool (discrete) and then a continuous
    trajectory speed/position for it
  - Two-level, mixed discrete-continuous decision
  - Long-horizon task decomposed into subtasks
- **Brute-force solution**:
  - Flat policy over the full joint discrete-continuous action space
  - Learn one monolithic policy that must directly output both the tool
    choice and the continuous trajectory in one shot
  - Long-horizon credit assignment across the two decision levels is
    difficult to learn from a single flat reward signal
- **Python packages**:
  - `stable-baselines3` for the low-level controllers
  - `hbaselines` for the option/goal framework
- **Solution sketch**: two-level option framework
  - A high-level policy selects a discrete option/tool over a coarse
    timescale
  - A low-level policy (one per option) outputs the continuous trajectory
    conditioned on the selected option
  - Train both levels jointly (or the low level first, then the high level),
    so credit assignment happens separately at each timescale

## 30. Anytime Algorithms and Approximate Dynamic Programming

- **Example problem**:
  - Real-time chess engine that must return a move within a strict time
    budget
  - Robot obstacle avoidance needing a reaction within 50 ms
  - Optimal solution is too slow; a bounded-suboptimal one is acceptable
- **Brute-force solution**:
  - Run the exact/optimal algorithm (full minimax or exact value iteration)
    to completion regardless of the time budget
  - Ignore the deadline and let full search run to termination
  - Misses the deadline entirely for any nontrivial problem size, which is
    unacceptable in a real-time setting
- **Python packages**:
  - `python-chess` (iterative-deepening search)
  - Custom truncated value iteration with `numpy`
- **Solution sketch**: iterative deepening with a value bound
  - Run the search (e.g., minimax or value iteration) to depth 1, record the
    best answer found so far
  - Increase depth incrementally, always keeping the best answer available if
    interrupted
  - Stop as soon as the time budget is hit and return the best answer found
    so far, with an error bound that shrinks as depth increases
    ($\varepsilon/(1-\gamma)$ for truncated value iteration)

## 31. Linear Function Approximation (TD with Linear FA / LSTD)

- **Example problem**:
  - Online resource allocation where state is described by continuous
    features (load, queue length, time of day)
  - Too many feature combinations to tabulate
  - Needs generalization across similar states
- **Brute-force solution**:
  - Tabular Q-Learning/Value Iteration over a discretized state
  - Discretize each continuous feature into bins and treat every bin
    combination as one table row
  - Table size grows exponentially with the number of features, infeasible
    beyond a couple of features
- **Python packages**:
  - `numpy` for the manual linear TD update
  - `scikit-learn` for feature/basis fitting
- **Solution sketch**: linear TD with hand-designed features
  - Design a feature map $\phi(s) \in \mathbb{R}^d$ with $d \ll |\mathcal{S}|$
    (e.g., tile coding or polynomial features)
  - Approximate $V(s) \approx w^\top\phi(s)$ and update
    $w \leftarrow w + \alpha[r + \gamma V(s') - V(s)]\phi(s)$ after each
    transition
  - LSTD instead solves for the fixed-point $w$ directly in closed form from
    accumulated feature statistics, avoiding step-size tuning
