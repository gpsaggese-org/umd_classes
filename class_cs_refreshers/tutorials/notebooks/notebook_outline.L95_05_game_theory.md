---
name: L95_05_game_theory
description: Interactive Jupyter notebook outline for a game theory refresher covering payoff matrices, dominant strategies, Nash equilibrium, classic 2x2 games, mixed strategies, sequential games, evolutionary game theory, and network routing
metadata:
  type: notebook_outline
  lesson: CS Refreshers Lesson 95 Game Theory
  libraries: numpy, pandas, seaborn, matplotlib, ipywidgets, networkx
  domain: game_theory
---

# Game Theory: From Payoff Matrices to Evolutionary Dynamics

- This notebook builds strategic-reasoning intuition around one reusable tool:
  an editable 2x2 payoff-matrix sandbox
- The pedagogical arc is:
  - Read a payoff matrix -> detect dominant strategies -> find Nash equilibria
    by best response -> recognize classic games as points in the same payoff
    space -> mix strategies when no pure equilibrium exists -> solve
    sequential games by backward induction -> watch equilibrium emerge from
    selection instead of reasoning -> see decentralized play fail to reach the
    social optimum
- Focus is on hands-on discovery: students edit payoffs and watch best
  responses, equilibria, and classifications update live, rather than
  re-deriving results already shown in the lecture
- Scope: the notebook covers the foundational, most visualizable chapters
  (normal form, equilibrium concepts, classic games, sequential games,
  evolutionary game theory, network games). Cooperative game theory
  (Shapley value, bargaining), Bayesian/signaling games, and the applied
  economics/politics/business chapters are left to the lecture slides since
  they do not reduce to a single interactive running example as cleanly

# Part 1: The Payoff Matrix and the Game Sandbox

## Cell 1.1: Reading a Payoff Matrix

**Goal**:
- Ground the normal-form representation with a concrete example (Prisoners'
  Dilemma) before any interactivity is introduced
- Understand that each cell holds (row player payoff, column player payoff)
  and that a player's payoff depends on both players' choices

**Plots and their descriptions**:
- _Payoff matrix_: 2x2 table for the Prisoners' Dilemma with rows = Player 1's
  action (Cooperate/Defect), columns = Player 2's action, each cell annotated
  with (P1 payoff, P2 payoff) and shaded by the row player's payoff
- _Comments_: payoff convention (row player's payoff listed first), which axis
  belongs to which player

**Widgets**: none (reference cell)

**Key observations**:
- The matrix packs 4 numbers per outcome (2 per player) into one compact
  structure
- Player 1's best cell in one column is not necessarily best in another
  column: payoffs are interdependent
- Reading a payoff matrix is the prerequisite for every equilibrium concept
  that follows

**Implementation**: `matplotlib` table/heatmap with text annotations,
`pandas.DataFrame` for the raw table shown beside the plot

## Cell 1.2: The 2x2 Game Sandbox: Editable Payoffs

**Goal**:
- Build the reusable tool used through Parts 1-3: an editable 2x2 normal-form
  game where changing any payoff instantly updates the picture
- Build intuition that Prisoners' Dilemma, Battle of the Sexes, and other
  classic games are all points in the same 8-dimensional payoff space

**Plots and their descriptions**:
- _Payoff matrix_: live-updating 2x2 grid, matching the style of Cell 1.1
- _Comments_: current 8 payoff values, whether the game is currently zero-sum
  (row payoff + column payoff constant across all 4 cells)

**Widgets**:
- `game`: dropdown to load a preset (Custom, Prisoners' Dilemma, Battle of the
  Sexes, Stag Hunt, Matching Pennies); loading a preset overwrites all 8
  sliders below
- `p1_11, p1_12, p1_21, p1_22`: row player's payoff in each of the 4 outcomes
  (-5 to 5)
- `p2_11, p2_12, p2_21, p2_22`: column player's payoff in each of the 4
  outcomes (-5 to 5)

**Key observations**:
- Every classic game in this notebook is one setting of these 8 numbers
- A small change (turning +1 into -1 in one cell) can flip a game from
  non-zero-sum to zero-sum
- This sandbox is reused with different lenses in Cells 2.1, 2.2, and 3.1

**Implementation**: `ipywidgets` sliders via `htutori.build_widget_control`
(one per payoff), `ipywidgets.Dropdown` for presets with an observe callback
that overwrites slider values, `matplotlib` for the live matrix, the Output
widget pattern for a single re-rendered figure

# Part 2: Dominant Strategies and Nash Equilibrium

## Cell 2.1: Highlighting Dominant and Dominated Strategies

**Goal**:
- Apply the sandbox from Cell 1.2 to detect a dominant strategy: an action
  that is best against every opponent action
- Extend Cell 1.2 by adding automatic classification instead of plain display

**Plots and their descriptions**:
- _Payoff matrix_: same grid as Cell 1.2, with the dominant row and/or column
  (if one exists) outlined in a bold border
- _Comments_: whether Player 1 has a dominant strategy, whether Player 2 has
  one, and which action it is

**Widgets**:
- Reuses the 8 payoff sliders and `game` preset dropdown from Cell 1.2

**Key observations**:
- Prisoners' Dilemma preset: Defect is dominant for both players even though
  mutual cooperation is better for both
- Not every game has a dominant strategy: switch to Battle of the Sexes and
  watch the outline disappear
- A dominant strategy makes prediction trivial since a rational player needs
  no belief about the opponent at all

**Implementation**: same `matplotlib` matrix renderer as Cell 1.2 extended
with a dominance-check function in utils, `matplotlib.patches.Rectangle` for
the outline

## Cell 2.2: Finding Nash Equilibria via Best Response

**Goal**:
- Introduce the best-response method: underline each player's best action
  given every opponent choice, and mark cells where both underlines coincide
- Connect dominant strategies (Cell 2.1) to the more general Nash equilibrium
  concept, since a dominant strategy always yields a Nash equilibrium but not
  the reverse

**Plots and their descriptions**:
- _Payoff matrix_: row-player payoff underlined where it is Player 1's best
  response to that column, column-player payoff underlined where it is Player
  2's best response to that row; cells with both underlines shaded gold as
  Nash equilibria
- _Comments_: number of pure-strategy Nash equilibria found and their
  coordinates

**Widgets**:
- Reuses the 8 payoff sliders and `game` preset dropdown from Cell 1.2

**Key observations**:
- Prisoners' Dilemma has exactly one Nash equilibrium, (Defect, Defect),
  matching its dominant strategy
- Battle of the Sexes has two pure Nash equilibria: multiplicity creates an
  equilibrium-selection problem
- Matching Pennies has zero pure Nash equilibria: the best-response marks
  chase each other around the matrix with no cell where both coincide

**Implementation**: `matplotlib` annotated matrix with underline/highlight
logic in utils, best-response computation shared with Cell 2.1

# Part 3: A Gallery of Classic 2x2 Games

## Cell 3.1: Prisoners' Dilemma, Battle of the Sexes, and Stag Hunt Side by Side

**Goal**:
- Compare three canonical games at once to see how equilibrium structure
  differs even though all three are 2x2 games
- Apply the best-response/Nash analysis from Cells 2.1-2.2 to three games
  simultaneously instead of one at a time

**Plots and their descriptions**:
- _Three payoff matrices_: Prisoners' Dilemma, Battle of the Sexes, and Stag
  Hunt shown side by side, each with best-response underlines and Nash cells
  shaded gold
- _Comments_: for each game, the number of pure Nash equilibria and whether
  each is Pareto optimal

**Widgets**:
- `highlight`: toggle to show or hide the best-response underlines on all
  three panels at once

**Key observations**:
- Prisoners' Dilemma: unique Nash equilibrium, not Pareto optimal since
  mutual cooperation is better for both but unreachable
- Battle of the Sexes: two Nash equilibria, both Pareto optimal, but the
  players disagree on which they prefer
- Stag Hunt: two Nash equilibria, one payoff dominant (Stag, Stag) and one
  risk dominant (Hare, Hare)

**Implementation**: `matplotlib` 1x3 subplot grid reusing the Cell 2.2
rendering function per axis, fixed preset payoffs, `ipywidgets.ToggleButton`

## Cell 3.2: Stag Hunt: Payoff Dominance vs Risk Dominance

**Goal**:
- Zoom into the equilibrium-selection problem left open by Cell 3.1's Stag
  Hunt panel: which of the two Nash equilibria should rational players expect
- Show that the answer depends on trust in the opponent, not on the payoff
  matrix alone

**Plots and their descriptions**:
- _Expected payoff vs belief_: line plot of the expected payoff from choosing
  Stag as a function of the believed probability $q$ that the opponent
  chooses Stag, compared against the constant payoff from choosing Hare
- _Comments_: current stag payoff $V$, current belief $q$, and which action
  currently has the higher expected payoff

**Widgets**:
- `V`: slider for the stag payoff when both players hunt stag (2-6)
- `q`: slider for the believed probability the opponent chooses Stag
  (0.0-1.0)

**Key observations**:
- The crossing point of the two lines is the belief threshold above which
  Stag becomes the rational choice
- A higher $V$ shifts the threshold, making Stag rational under more doubt
  about the opponent
- Payoff dominant does not mean safe: below the threshold, Hare remains the
  individually rational choice

**Implementation**: `matplotlib` line plot, `htutori.build_widget_control`
sliders, expected-payoff formulas computed in utils

# Part 4: Mixed Strategy Equilibria

## Cell 4.1: Why Randomize? Matching Pennies Has No Pure Equilibrium

**Goal**:
- Show, by exhaustive best response, that Matching Pennies has no pure Nash
  equilibrium, motivating randomization as the only stable strategy
- Apply the Cell 2.2 best-response method to a game where it fails to find
  a pure Nash equilibrium

**Plots and their descriptions**:
- _Payoff matrix_: Matching Pennies with best-response underlines chasing
  each other with no coinciding cell
- _Comments_: confirmation that 0 pure Nash equilibria exist

**Widgets**: none (fixed example reusing the Cell 2.2 renderer)

**Key observations**:
- Whatever the row player is expected to do, switching is always profitable:
  the best response cycles Heads -> Tails -> Heads
- This cycling is the signature of a game with no pure Nash equilibrium
- The next cell shows that allowing randomization restores an equilibrium

**Implementation**: `matplotlib` matrix renderer reused from Cell 2.2

## Cell 4.2: Computing the Equilibrium Mix by Indifference

**Goal**:
- Derive the mixed Nash equilibrium via the indifference principle: find the
  opponent's mixing probability that makes both of your actions equally good
- Compute and visualize the crossing point students predicted qualitatively
  in Cell 4.1

**Plots and their descriptions**:
- _Expected payoff vs opponent's probability_: two lines, expected payoff
  from Heads and from Tails, plotted against $q$ = probability the opponent
  plays Heads, crossing at the equilibrium $q^*$
- _Comments_: computed $q^*$, expected value of the game at equilibrium

**Widgets**:
- `stakes`: slider for the win/lose payoff magnitude of the game (1-5),
  rescales both lines without moving the crossing point

**Key observations**:
- The crossing point is exactly $q^* = 1/2$ for symmetric Matching Pennies,
  matching the lecture's derivation
- Changing the stakes rescales both lines but never moves the equilibrium
  probability: mixing probabilities are pinned down by the opponent's
  payoffs, not your own
- At the crossing, both actions give equal expected payoff: exactly the
  definition of indifference

**Implementation**: `matplotlib` line plot, `htutori.build_widget_control`
slider, $\mathbb{E}[\text{Heads}]$ and $\mathbb{E}[\text{Tails}]$ formulas
computed in utils

# Part 5: Sequential Games and Backward Induction

## Cell 5.1: Solving the Entry Game by Backward Induction

**Goal**:
- Introduce the extensive form (game tree) using the market-entry example
  from the lecture, and solve it by reasoning from the leaves back to the
  root
- Contrast with Parts 1-4, where every game was simultaneous: here timing
  matters

**Plots and their descriptions**:
- _Game tree_: Entrant's node at the root branching to Out / Enter; Enter
  leads to the Incumbent's node branching to Accommodate / Fight; each leaf
  labeled with (Entrant, Incumbent) payoffs
- _Comments_: payoff at each leaf and which branch backward induction selects
  at each internal node

**Widgets**:
- `out_payoff`: slider for the Entrant's payoff if it stays Out (-2 to 2)
- `fight_payoff`: slider for the Incumbent's payoff if it Fights (-3 to 1)

**Key observations**:
- Backward induction solves the Incumbent's node first (Accommodate beats
  Fight when fighting is costly), then the Entrant's node using that result
- The solved path (Enter, Accommodate) highlights in green while the pruned
  branch (Fight) grays out
- Raising the Incumbent's fight payoff above its accommodate payoff flips the
  solved path entirely, showing how one number changes the whole game

**Implementation**: `networkx` plus `matplotlib` for the tree layout,
backward-induction solver in utils that returns the winning path at each node

## Cell 5.2: Non-Credible Threats and Subgame Perfection

**Goal**:
- Show why the Nash equilibrium (Out, Fight) is not subgame perfect: the
  threat to Fight is not credible once the Entrant has actually entered
- Contrast Cell 5.1's solved tree with an unsolved, threat-based Nash
  equilibrium on the same game

**Plots and their descriptions**:
- _Two trees side by side_: left tree shows the subgame perfect outcome
  (Enter, Accommodate) from Cell 5.1; right tree shows the (Out, Fight) Nash
  equilibrium with the Fight branch marked non-credible in red since it is
  never actually tested off the equilibrium path
- _Comments_: payoff comparison of the two equilibria for the Entrant

**Widgets**:
- `commitment`: toggle for whether the Incumbent has a credible commitment
  device (e.g., sunk capacity); switching it on raises the Fight payoff
  enough to make Fight genuinely optimal, which in turn makes Out rational
  for the Entrant

**Key observations**:
- A strategy profile can be a Nash equilibrium and still rely on a threat the
  threatener would not actually carry out
- Every subgame perfect equilibrium is a Nash equilibrium, but this example
  is a Nash equilibrium that is not subgame perfect
- Toggling on a genuine commitment device is what turns an empty threat into
  a credible one, changing the subgame perfect equilibrium itself

**Implementation**: two-panel `matplotlib`/`networkx` tree rendering reusing
the Cell 5.1 layout function, `ipywidgets.ToggleButton`

# Part 6: Evolutionary Game Theory

## Cell 6.1: Hawk-Dove and Evolutionarily Stable Strategies

**Goal**:
- Introduce equilibrium without rationality: the Hawk-Dove game, where
  fitness rather than reasoning determines which strategy survives
- Connect the evolutionarily stable strategy condition to the Nash
  equilibrium concept from Part 2, since every evolutionarily stable strategy
  is a Nash equilibrium

**Plots and their descriptions**:
- _Payoff matrix_: Hawk-Dove matrix with cells computed from $V$ and $C$
- _Fitness vs population share_: line plot of a Hawk's expected fitness
  against a Dove's expected fitness as a function of the population fraction
  playing Hawk, crossing at the mixed evolutionarily stable strategy when
  $V < C$
- _Comments_: current $V$, current $C$, whether pure Hawk is evolutionarily
  stable or a mixed evolutionarily stable strategy exists, and its value

**Widgets**:
- `V`: slider for resource value (1-10)
- `C`: slider for fight cost (1-10)

**Key observations**:
- When $V > C$, Hawk is a pure evolutionarily stable strategy: escalation
  always pays
- When $V < C$, the evolutionarily stable strategy is a mix of Hawks and
  Doves at the fraction where both have equal fitness
- The evolutionarily stable fraction depends only on the ratio $V/C$, not on
  the absolute payoff scale

**Implementation**: `matplotlib` matrix plus line plot, `htutori` sliders,
evolutionarily stable fraction formula ($V/C$) computed in utils

## Cell 6.2: Replicator Dynamics: Watching a Population Converge

**Goal**:
- Simulate how the population share of Hawks evolves over time under the
  replicator equation, showing convergence to the evolutionarily stable
  strategy found in Cell 6.1 without any individual doing the reasoning
- Make the fixed point from Cell 6.1 concrete as a trajectory that starts
  anywhere and ends at the same place

**Plots and their descriptions**:
- _Population trajectory_: line plot of the Hawk fraction $x_t$ over
  generations, starting from the chosen initial fraction and converging to
  the evolutionarily stable fraction (shown as a dashed reference line)
- _Comments_: current generation, current Hawk fraction, distance remaining
  to the evolutionarily stable fraction

**Widgets**:
- `x0`: slider for the initial fraction of Hawks (0.0-1.0)
- `V`: slider for resource value (1-10)
- `C`: slider for fight cost (1-10)
- `n_generations`: slider for the number of generations simulated (10-200)

**Key observations**:
- Every starting fraction $x_0$ converges to the same evolutionarily stable
  fraction: the fixed point is stable to perturbation, exactly what
  evolutionary stability means
- Convergence is fast near the middle of the range and slows near the
  boundaries (0 or 1)
- No individual animal computes a best response: selection alone drives the
  population toward the same point Nash equilibrium analysis predicts

**Implementation**: `numpy` for iterating the discrete replicator update,
`matplotlib` line plot, `htutori.build_widget_control` sliders

# Part 7: Price of Anarchy in Network Routing

## Cell 7.1: Braess's Paradox: Adding a Road That Hurts Everyone

**Goal**:
- Close with a network game showing decentralized optimization can fail even
  without any single irrational player, tying back to the lecture's network
  games chapter
- Contrast selfish equilibrium routing against the socially optimal routing

**Plots and their descriptions**:
- _Network diagram_: 4-node network (source, two middle nodes, sink) with two
  original routes and a toggleable shortcut edge, edges labeled with their
  travel-time functions
- _Travel time comparison_: bar chart comparing total travel time under
  selfish equilibrium routing with the shortcut off vs on, next to the
  socially optimal routing

**Widgets**:
- `shortcut`: toggle to add or remove the zero-cost shortcut edge between the
  two middle nodes
- `n_drivers`: slider for the number of drivers (10-100)

**Key observations**:
- Adding the shortcut edge makes every driver's equilibrium travel time go
  up, not down
- Once the shortcut exists, the socially optimal routing (drivers split
  evenly, ignoring the shortcut) beats the selfish equilibrium for everyone
- Price of anarchy formalizes this gap as selfish equilibrium cost divided by
  optimal cost, here strictly greater than 1

**Implementation**: `networkx` for the graph layout and edge-cost functions,
`matplotlib` for the diagram and bar chart, equilibrium flow computed in
utils via a simple fixed-point search

# Summary: The Mental Model

- A normal-form game is a payoff matrix; a dominant strategy is a row or
  column that wins against everything; a Nash equilibrium is a cell where
  every player's best response coincides
- Classic games (Prisoners' Dilemma, Battle of the Sexes, Stag Hunt, Matching
  Pennies) are not special mechanisms: they are specific points in the same
  payoff space, distinguished only by how many pure equilibria they have and
  whether those equilibria are efficient
- When no pure equilibrium exists, the indifference principle pins down a
  mixed equilibrium: the opponent's payoffs, not your own, determine your
  mixing probability
- Sequential games add timing: backward induction finds the subgame perfect
  equilibrium, which rules out empty threats that ordinary Nash equilibrium
  allows
- Evolutionary game theory reaches the same equilibrium concepts through
  population dynamics instead of individual rationality, and network games
  show that decentralized equilibrium play can be strictly worse than the
  social optimum
