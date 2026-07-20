# Implementing Monte Carlo Tree Search and AlphaZero

## Status
**Status**: draft
**Complete Specs**: 20%
**Assignee**: TBD

## Core Idea [REQUIRED]

Create an accessible, step-by-step tutorial implementing Monte Carlo Tree Search (MCTS) and AlphaZero from scratch. The goal is to make these powerful game-playing algorithms understandable through hands-on Python code, starting with simple games (Tic-Tac-Toe) and progressing to more complex domains (Chess, Go). This addresses the gap between theoretical papers and practical implementation, enabling students and practitioners to understand the interplay between tree search, neural networks, and self-play learning.

The core insight: AlphaZero's power comes from combining three ideas—MCTS for efficient exploration, neural network guidance, and self-play iteration—each learnable independently and then integrated. Breaking this into digestible pieces makes the algorithm both understandable and implementable.

## Formalization

AlphaZero combines three components:

**Tree Search**: MCTS balances exploration vs. exploitation using Upper Confidence bounds applied to Trees (UCT):
```
UCT(node) = Q(node)/N(node) + C * sqrt(ln(N(parent))/N(node))
```

**Neural Network**: Policy and value heads trained on self-play:
```
p, v = network(state)
p: probability distribution over actions
v: scalar value estimate for the position
```

**Self-Play Update**: Each iteration improves the network by playing against itself:
```
For each game:
  - Use MCTS + current network to generate moves
  - Collect (state, action, result) tuples
  - Retrain network on collected data
```

## Key Examples

- **Example 1**: Tic-Tac-Toe with pure MCTS. Shows tree search working without neural networks; playable in seconds.
- **Example 2**: Tic-Tac-Toe with AlphaZero. Shows how adding a small network + self-play improves performance and learning speed.
- **Example 3**: Connect Four or simple Chess variant. Demonstrates scaling challenges and how network size/training time matter.

## Questions

1. How do we balance MCTS simulation count vs. network quality in early training?
2. What is the minimum network architecture needed to beat strong MCTS-only baselines?
3. How does the curriculum (game complexity progression) affect learning speed?
4. Can we extract interpretable insights about optimal game strategy from trained networks?

## Research Topics

- **MCTS Variants**: Parallel MCTS, progressive widening, rave (rapid action value estimation)
- **Network Architecture**: How shallow can networks be? Effect of network width on sample efficiency
- **Self-Play Curriculum**: Temperature in move selection, training data retention, online vs. offline learning
- **Game Abstractions**: Can networks learn generalizable patterns across similar games?

## Next steps

- [ ] Look for related research (what has already been done)
- [ ] Finalize the implementation plan
- [ ] GP to review / approve the plan
- [ ] Hack a quick end-to-end prototype (e.g., Tic-Tac-Toe MCTS in 1-2 days)
- [ ] Break the problem down in phases and milestones
- [ ] Execute one step at a time

## Implementation plan

- **Phase 1: Pure MCTS (Tic-Tac-Toe)**
  - Implement game state, rules, and basic MCTS algorithm
  - Result: Playable, unbeaten MCTS player

- **Phase 2: Neural Network Integration**
  - Add small conv/dense network for policy and value prediction
  - Integrate network guidance into MCTS tree
  - Result: MCTS + network baseline

- **Phase 3: Self-Play Training**
  - Implement self-play loop and network training
  - Add move generation and data collection
  - Result: Trained AlphaZero playing against itself with improving performance

- **Phase 4: Scaling & Analysis**
  - Extend to Connect Four or chess variants
  - Analyze learned representations and strategy patterns
  - Result: Reproducible, generalizable implementation

## References

- Silver, D., et al. _Mastering the game of Go with deep neural networks and tree search_. Nature (2016)
- Silver, D., et al. _Mastering Chess and Shogi by Self-Play with a General Reinforcement Learning Algorithm_. arXiv (2017)
- Surag Nair. _AlphaZero General_. GitHub repository with clean implementation
- freeCodeCamp. _AlphaZero from Scratch_. 4-5 hour YouTube tutorial covering TicTacToe, neural networks, self-play
- Browne, C., et al. _A Survey of Monte Carlo Tree Search Methods_. IEEE Transactions on Computational Intelligence and AI in Games (2012)

## Resources

### Academic/Tutorial Papers
- IEEE Conference tutorials providing comprehensive introductions to MCTS
  - Covers history and relationship to simulation-based algorithms for Markov decision processes
  - Demonstrations using tic-tac-toe and applications in AlphaGo/AlphaZero
- INFORMS tutorial PDF with MCTS fundamentals
  - Decision tree demonstrations
  - Tic-tac-toe examples
  - Available at informs-sim.org

### Practical Implementations
- **ai-boson.github.io/mcts/** - Python code tutorial
  - Explains MCTS algorithm design for games
  - Games covered: Go, Sudoku Tic Tac Toe, Chess
  - Beginner-friendly (no ML background required)

---

## AlphaZero

https://www.dwarkesh.com/p/eric-jang
https://evjang.com/2026/04/28/autogo.html#cover

### Official Learning Resources
- **Surag Nair's tutorial** - Short and effective introduction to AlphaZero
- **JuliaCon 2021 talk** - Ten-minute overview of AlphaZero fundamentals
- **GitHub: suragnair/alpha-zero-general** - Clean implementation
  - Works with any game and any framework
  - Includes comprehensive tutorial
  - Sample implementations: Othello, GoBang, TicTacToe
  - Languages: PyTorch and Keras

### Video Courses
- **freeCodeCamp YouTube: "AlphaZero from Scratch"**
  - 4-5 hour comprehensive tutorial
  - Topics: TicTacToe, neural networks, self-play, training, ConnectFour
  - Includes code and trained models

### Written Tutorials
- **Medium by Darin Straus** - AlphaZero implementation details
  - Python with TensorFlow
  - Code available on GitHub
- **Kaggle Tutorial: "AlphaZero from Scratch"**
  - Theory and references included
