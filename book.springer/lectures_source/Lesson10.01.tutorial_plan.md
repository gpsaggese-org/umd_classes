# Tutorial Plan: Decision-Making Algorithms (Lesson 10.01)

This plan covers the algorithms listed in the lecture

For each algorithm the plan gives
- a simple example problem
- a brute-force baseline
- the Python packages that apply
- a sketch of a package-based solution

```
Read the first 5 algorithms of
book.springer/lectures_source/Lesson10.01_Taxonomy_of_Decision_Problems.txt

Come up with a plan for each of the algorithms to
- Have the description of a simple Python example of a problem explaining the
  algorithm (using the example in the slides or a "famous one" in the literature)
- A "brute" force solution
- Point to the Python packages that can be used to solve the problem
- Sketch how to solve the problem using one of the packages

Do not write code, but only write 10 nested bullet points per algorithm

Write the result using .claude/skills/markdown.rules.md in
book.springer/lectures_source/Lesson10.01.tutorial_plan.md
```

## 1. Q-Learning

- **Example problem**: `FrozenLake` grid navigation — an agent crosses a slippery
  frozen lake to a goal without falling into holes (a canonical off-policy
  control benchmark that mirrors the slides' grid world)
  - State is the tile index on a 4x4 grid, actions are $\{$left, down, right,
    up$\}$, and reward is 1 only on reaching the goal
- **Brute-force solution**: enumerate every deterministic policy (one action per
  state) and score each by many Monte Carlo rollouts, keeping the best
  - Infeasible: with 16 states and 4 actions there are $4^{16}$ policies, and
    each needs many noisy rollouts to rank reliably
- **Python packages**: `gymnasium` for the environment, `numpy` for the Q-table,
  and `pymdptoolbox` which ships a ready `QLearning` class
  - `gymnasium` supplies the `reset` and `step` dynamics while `numpy` holds the
    $|\mathcal{S}| \times |\mathcal{A}|$ table
- **Solution sketch**: learn the Q-table online with `gymnasium` and `numpy`
  - Initialize $Q$ to zeros and, for each episode, pick actions $\varepsilon$-greedily from
    the current $Q$
  - After each transition apply the TD update $Q(s,a) \leftarrow Q(s,a) + \alpha[r + \gamma \max_{a'} Q(s',a') - Q(s,a)]$
  - Decay $\varepsilon$ over episodes, then read off the greedy policy $\arg\max_a Q(s,a)$

## 2. SARSA

- **Example problem**: `CliffWalking` — an agent walks a gridworld edge next to a
  cliff where falling off costs -100 (Sutton and Barto's classic
  SARSA-vs-Q-Learning example)
  - SARSA learns the safer path away from the cliff because it accounts for its
    own exploratory missteps
- **Brute-force solution**: enumerate deterministic policies and evaluate each by
  averaging returns over many rollouts, then choose the best
  - Exponential in the number of states and wasteful, since it ignores the shared
    structure the TD update exploits
- **Python packages**: `gymnasium` (`CliffWalking-v0`) for the environment and
  `numpy` for the Q-table
  - `gymnasium` provides the reward and cliff-reset dynamics while `numpy` stores
    $Q$
- **Solution sketch**: on-policy TD control with `gymnasium` and `numpy`
  - Choose $a$ $\varepsilon$-greedily, take the step, then choose the next action $a'$ from
    the same $\varepsilon$-greedy policy
  - Update toward the action actually taken: $Q(s,a) \leftarrow Q(s,a) + \alpha[r + \gamma Q(s',a') - Q(s,a)]$
  - Repeat across episodes while decaying $\varepsilon$, so the learned policy hugs the
    safe route

## 3. Value Iteration

- **Example problem**: the 4x3 grid world MDP (Russell and Norvig) with known
  transition noise (80% intended, 20% slip) and +1/-1 terminals; this matches
  the slides' inventory MDP
  - The dynamics $P(s'|s,a)$ and reward $R(s,a)$ are fully known, so no
    environment interaction is needed
- **Brute-force solution**: enumerate all deterministic policies, solve each
  policy's value exactly, and keep the highest-valued one
  - There are $|\mathcal{A}|^{|\mathcal{S}|}$ policies, each requiring a
    linear-system solve — a combinatorial explosion
- **Python packages**: `pymdptoolbox` (`mdptoolbox.mdp.ValueIteration`) and
  `numpy` for the $P$ and $R$ arrays
  - `pymdptoolbox` takes the transition and reward matrices and returns the
    optimal value and policy
- **Solution sketch**: iterate the Bellman optimality backup with `pymdptoolbox`
  - Encode $P$ as an $|\mathcal{A}| \times |\mathcal{S}| \times |\mathcal{S}|$
    array and $R$ as a matrix
  - Repeatedly apply $V(s) \leftarrow \max_a [R(s,a) + \gamma \sum_{s'} P(s'|s,a) V(s')]$ until the change drops below a threshold
  - Extract the greedy policy from the converged $V$

## 4. Policy Iteration

- **Example problem**: Jack's Car Rental (Sutton and Barto) — move cars between
  two lots overnight to maximize rental income, a known-model MDP; the 4x3 grid
  world works too
  - The rewards and Poisson rental/return dynamics are known, so the optimal
    policy can be computed by planning
- **Brute-force solution**: enumerate every deterministic policy, evaluate each
  exactly, and select the best
  - The same combinatorial blow-up applies, whereas policy iteration converges in
    very few sweeps
- **Python packages**: `pymdptoolbox` (`mdptoolbox.mdp.PolicyIteration`) and
  `numpy`
  - The class alternates evaluation and improvement internally, given $P$ and $R$
- **Solution sketch**: alternate evaluation and improvement with `pymdptoolbox`
  - Start from an arbitrary policy and evaluate it by solving the linear Bellman
    system for $V^\pi$
  - Improve greedily: $\pi(s) \leftarrow \arg\max_a [R(s,a) + \gamma \sum_{s'} P(s'|s,a) V^\pi(s')]$
  - Repeat until the policy stops changing, which is guaranteed in finite steps

## 5. Monte Carlo Tree Search (MCTS)

- **Example problem**: Tic-Tac-Toe move selection (the slides' running example) —
  search which move to play from the current board; the same method scales to
  Connect Four and Go
  - State is a board configuration, actions are the empty cells, and reward is +1
    win / 0 draw / -1 loss at a terminal state
- **Brute-force solution**: full minimax over the entire game tree, backing up
  win/loss values from the leaves
  - Fine for Tic-Tac-Toe, but the branching factor makes it intractable for
    larger games like Go
- **Python packages**: `mcts` (generic UCT), `open_spiel` (DeepMind game
  algorithms), and `easyAI` for the minimax baseline
  - `mcts` needs only a state class exposing the legal actions, the transition,
    and the terminal reward
- **Solution sketch**: run UCT with the `mcts` package
  - Selection: descend the tree by the UCB score $\frac{Q(s,a)}{N(s,a)} + c\sqrt{\frac{\ln N(s)}{N(s,a)}}$
  - Expansion then simulation: add a child node and play a random rollout to a
    terminal reward
  - Backpropagate the result up the visited path, and after a fixed budget of
    iterations play the most-visited child
