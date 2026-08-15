---
title: "Self-Play Monte Carlo Tree Search with Neural Guidance for the Traveling Salesman Problem"
author:
  - name: Giacinto Paolo (GP) Saggese
    department: "Department of Computer Science"
    organization: "University of Maryland, College Park"
    location: "College Park, MD, USA"
    email: "`gsaggese@umd.edu`{=typst}"
abstract: |
  The Traveling Salesman Problem (TSP) is a canonical NP-hard combinatorial
  problem, and neural approaches to it fall into two camps: constructive
  policies trained by supervision or policy-gradient reinforcement learning,
  which decode a tour in a single forward pass without a search-based
  improvement step, and Monte Carlo Tree Search (MCTS) applied at inference
  time on top of a network already trained by one of those two recipes. In
  neither camp does search itself supply the training target the way it does
  in AlphaZero, where a self-play loop repeatedly turns MCTS's own
  search-improved move distribution into the next training signal for the
  network that guides the search.
  <!-- -->
  This paper proposes closing that gap by adapting the AlphaZero recipe to
  TSP tour construction, treated as a single-player sequential decision
  process. A policy-value network guided by PUCT-based MCTS constructs tours
  through self-play; because a single-player construction task has no
  opponent to supply a win/loss signal, we adopt a ranked-reward transform
  that turns each episode's tour length into a self-relative pseudo-outcome
  against a running buffer of recent tours, making the AlphaZero training
  loop applicable without modification. Because the optimal tour length for
  random instances scales with the square root of the number of cities, we
  further propose training under an explicit curriculum over instance size,
  so the network and its ranked-reward buffer are never asked to compare
  costs across incommensurate scales.
  <!-- -->
  We formalize this framework, work through a hand-traced five-city example
  illustrating the search and the ranked-reward computation, and discuss the
  calibration and scalability questions a working implementation would need
  to resolve. No computational implementation or empirical evaluation has
  been carried out; this paper is a framework proposal.
keywords:
  - Monte Carlo tree search
  - AlphaZero
  - traveling salesman problem
  - self-play
  - neural combinatorial optimization
  - curriculum learning
bibliography: references.bib
---

# Introduction

The Traveling Salesman Problem asks for the shortest closed tour visiting
each of $n$ given cities exactly once, a combinatorial problem whose search
space grows as $(n-1)!/2$ and which is NP-hard in general. It is also one of
the most heavily used testbeds for neural combinatorial optimization, because
a tour's quality can be measured exactly and cheaply, which makes it
attractive for both supervised and reinforcement-learning approaches.

Prior work on solving TSP with learned models falls into three categories.

The first category is classical local-search heuristics, which iteratively
improve a tour through hand-designed edge-exchange moves, most notably the
Lin-Kernighan heuristic and its refined implementation, LKH
[@linkernighan1973heuristic; @helsgaun2000lkh]. These methods produce very
strong tours but encode no learned model: every instance is solved from
scratch by the same fixed move set, with no mechanism to improve from
experience across instances.

The second category is constructive neural policies, which learn to build a
tour one city at a time, trained either by supervision on reference tours, by
policy-gradient reinforcement learning, or by a graph-embedding value
function learned through fitted Q-iteration
[@vinyals2015pointernet; @bello2016neuralco; @khalil2017graphco;
@kool2019attention]. These policies decode a tour in a single forward pass
(optionally followed by sampling or beam search at inference time), so the
network's output is never refined by a search procedure during training: the
training signal is the raw episode return or a supervised label, not a
search-improved target.

The third category is MCTS-augmented neural TSP solvers, which apply Monte
Carlo Tree Search at inference time to refine tours produced by an already
-trained network, either by using a graph neural network's output as move
priors inside the tree search [@xing2020gnnmcts] or by using MCTS as a local
-search step on top of a heatmap predicted by a network trained via
supervised learning on reference solutions and then fine-tuned to generalize
to much larger instances [@fu2021generalize]. In both cases the network is
trained before search is introduced, and MCTS improves the network's
decisions at test time without feeding search-improved targets back into
network training.

This paper proposes filling the gap between the second and third categories:
a genuine AlphaZero-style self-play loop for TSP, in which MCTS's own
search-improved visit distribution over each partial tour is the target used
to train the very network that guides the search, iterated until the policy
improves on its own past self [@silver2016go; @silver2017gozero;
@silver2017alphazero]. Because TSP tour construction is a single-player task
with no adversary to supply a natural win/loss outcome, we adapt the ranked
-reward mechanism proposed for single-player combinatorial self-play
[@laterre2018rankedreward] to convert each episode's tour length into a
bounded, self-relative outcome, and because the scale of that outcome shifts
with instance size [@beardwood1959shortest], we propose training under an
explicit curriculum over the number of cities [@bengio2009curriculum].

This framework rests on the following simplifying assumptions.

- **Euclidean, symmetric instances.** Cities are points in the plane and
  edge cost is symmetric Euclidean distance, the standard setting for the
  neural TSP literature cited above.
- **Fixed instance size within an episode.** The number of cities $n$ is
  fixed for the duration of one self-play episode; only the curriculum stage
  changes $n$ across episodes, not within one.
- **Full observability.** The policy observes all city coordinates from the
  first decision; nothing is revealed incrementally as in a partially
  observable routing setting.
- **Single vehicle, no side constraints.** The formulation excludes time
  windows, capacities, or multiple vehicles, which distinguish TSP from the
  broader vehicle-routing family.

This paper makes the following contributions.

- We formalize TSP tour construction as a single-player MDP suitable for
  AlphaZero-style self-play, and identify the reward-normalization problem
  this single-player setting introduces (Section III).
- We adapt the ranked-reward mechanism to this setting and propose a
  PUCT-based search, policy-value network, and self-play training loop for
  it (Section IV).
- We propose an explicit curriculum over instance size, motivated by the
  known scaling of optimal tour length with $\sqrt{n}$, and discuss its
  extension to zero-shot generalization beyond the training range (Sections
  IV and V).
- We work through a hand-traced five-city example illustrating the search
  and the ranked-reward computation (Section VI), and discuss the
  calibration and scalability questions the framework leaves open (Section
  VII).

The remainder of the paper is organized as follows. Section II surveys
related work in more detail. Section III formalizes the tour-construction
MDP and the reward-normalization problem. Section IV describes the proposed
search, network, self-play loop, and curriculum. Section V discusses
generalization beyond the training curriculum. Section VI works through the
illustrative example. Section VII discusses limitations. Section VIII
concludes and outlines an implementation plan.

# Related Work

**Classical TSP heuristics.** The Lin-Kernighan heuristic improves a tour
through variable-depth edge-exchange moves, and its LKH implementation
remains among the strongest known heuristics for large Euclidean instances
[@linkernighan1973heuristic; @helsgaun2000lkh]. TSPLIB supplies the standard
benchmark instances against which such heuristics, and the neural methods
below, are typically compared [@reinelt1991tsplib]. These methods are the
natural baseline for any learned solver but encode no trainable model: they
neither improve with additional training data nor transfer knowledge across
instances beyond what is hand-coded into the move set.

**Constructive neural policies.** Pointer Networks first showed that an
attention-based sequence model could learn to output a permutation of input
points via supervised training on reference tours [@vinyals2015pointernet].
Bello et al. replaced supervision with policy-gradient reinforcement
learning, removing the need for optimal-tour labels [@bello2016neuralco].
Khalil et al. instead learn a value function over partial solutions with a
graph embedding network trained by fitted Q-iteration, applicable to TSP and
related graph problems alike [@khalil2017graphco]. Kool et al. combine an
attention-based encoder-decoder with a REINFORCE estimator using a
deterministic greedy rollout as a variance-reducing baseline, and remains a
common backbone architecture for later work, including the network
formulation adapted in Section IV.2 of this paper [@kool2019attention].
Across this line of work, a tour is decoded in one pass through the network,
optionally followed by inference-time sampling or beam search; the network
is never trained on a target improved by an explicit search procedure.

**MCTS-augmented neural TSP solvers.** Xing and Tu combine a graph neural
network's move priors with MCTS to construct a tour, improving on the
network's greedy decoding, but train the network by supervised or
policy-gradient methods prior to introducing search [@xing2020gnnmcts]. Fu et
al. train a small network on small supervised instances to predict a
heatmap over promising edges, then use MCTS purely as a local-search refiner
at inference time, which lets a network trained at one scale generalize to
much larger instances [@fu2021generalize]. In both cases, search sits
downstream of a fixed, already-trained network rather than supplying the
training signal itself: search-time improvements do not flow back into
future versions of the network the way they do in an AlphaZero policy
-iteration loop.

**Self-play for single-player combinatorial optimization.** AlphaZero
demonstrates that a policy-value network trained purely from MCTS-improved
self-play targets, with no supervision beyond the game rules, can reach
superhuman performance in Go, chess, and shogi
[@silver2016go; @silver2017gozero; @silver2017alphazero]. Applying this
recipe outside two-player zero-sum games requires resolving the absence of a
natural win/loss outcome. Schadd et al. address this for single-player
puzzle-solving MCTS by modifying the backup rule itself, using a max-based
backup with a meta-search extension rather than average backup
[@schadd2008spmcts]. Laterre et al. instead keep the standard AlphaZero
average backup and transform the continuous episode return into a bounded
win/loss-like outcome by comparing it against a running percentile of recent
returns, the ranked-reward mechanism, applied to 2D and 3D bin packing
[@laterre2018rankedreward]. This paper adopts the ranked-reward approach
because it composes directly with an unmodified AlphaZero training loop, but
neither of these two single-player self-play lines has, to our knowledge,
been applied to TSP or combined with an explicit curriculum over instance
size, which is the gap this paper's proposal fills.

# Problem Formulation

## Notation and Setup

Let an instance consist of $n$ city coordinates $c_1, \dots, c_n \in
\mathbb{R}^2$. A tour is a permutation $\sigma$ of $\{1, \dots, n\}$, and its
length is
$$
L(\sigma) = \sum_{i=1}^{n-1} \lVert c_{\sigma(i)} - c_{\sigma(i+1)} \rVert
  + \lVert c_{\sigma(n)} - c_{\sigma(1)} \rVert .
$$
We formulate tour construction as an episodic single-player Markov decision
process. A state $s_t$ at step $t$ is the partial tour
$(\sigma(1), \dots, \sigma(t))$ together with the set of unvisited cities;
$s_0$ fixes $\sigma(1)$ to an arbitrary start city, removing the rotational
symmetry of the tour. An action $a_t$ at state $s_t$ selects the next city
from the unvisited set, so $|A(s_t)| = n - t$. The transition is
deterministic: $s_{t+1}$ appends $a_t$ to the partial tour. No reward is
given until the terminal state $s_n$, at which point the episode reward is
$-L(\sigma)$, the negative length of the completed tour. Let $\pi_\theta$
denote a policy-value network, parametrized by $\theta$, that maps a state
$s_t$ to a prior distribution $P(s_t, \cdot)$ over $A(s_t)$ and a scalar
value estimate $v(s_t)$.

## Simplifying Assumptions

- **Deterministic transitions.** Appending a chosen city to the partial tour
  is the only transition dynamic; there is no environment stochasticity
  beyond the randomness of instance sampling and network-guided search.
- **Reward available only at termination.** Intermediate states carry no
  reward signal, consistent with tour length being a property of the
  completed cycle rather than any prefix of it.
- **A single fixed instance size per self-play episode.** As stated in
  Section I, $n$ is constant within an episode; Section IV.4 addresses how
  $n$ changes across episodes.

## Problem 1: Tour Construction as a Single-Player MDP

Given the MDP of Section III.1, find a policy $\pi_\theta$ maximizing
expected terminal reward,
$$
\theta^* = \arg\max_\theta \; \mathbb{E}_{c_1,\dots,c_n \sim \mathcal{D}}
  \big[ -L(\sigma_{\pi_\theta}) \big],
$$
where $\mathcal{D}$ is a distribution over instances (e.g., cities sampled
uniformly at random in the unit square) and $\sigma_{\pi_\theta}$ is the tour
produced by executing $\pi_\theta$-guided search to termination.

## Problem 2: Reward Normalization for Self-Play Without an Opponent

AlphaZero's training loop treats the game outcome, a value in $\{-1, 0,
+1\}$ supplied by the rules of a two-player zero-sum game, as the target for
the network's value head, and the MCTS visit distribution as the target for
its policy head [@silver2017alphazero]. TSP tour construction supplies
neither a natural opponent nor a bounded outcome: $-L(\sigma)$ is a
continuous, unbounded-below quantity, and there is no second player whose
loss defines the agent's win. By the Beardwood-Halton-Hammersley result, the
expected length of an optimal tour over $n$ points sampled uniformly in the
unit square grows as $\Theta(\sqrt{n})$ [@beardwood1959shortest], so this
quantity is not even on a comparable scale across curriculum stages of
different $n$. The second sub-problem this paper addresses is therefore:
given a stream of completed episode lengths $L(\sigma)$ at a fixed curriculum
stage $n_k$, define a transform
$$
z = \text{rank}\big(L(\sigma), B_k\big) \in \{-1, +1\}
$$
of the episode length into a bounded, stage-relative outcome, where $B_k$ is
a buffer of recent tour lengths at stage $n_k$, so that $z$ can serve as the
value-head training target in an otherwise unmodified AlphaZero loop.

# Neural-Guided MCTS for Self-Play Tour Construction

## PUCT Selection over Partial Tours

At each state $s_t$ encountered during search, the tree policy selects the
action
$$
a_t = \arg\max_{a \in A(s_t)} \; \left[ Q(s_t, a) + c_{\text{puct}} \cdot
  P(s_t, a) \cdot \frac{\sqrt{\sum_b N(s_t, b)}}{1 + N(s_t, a)} \right],
$$
the PUCT rule used by AlphaZero [@silver2017alphazero], itself a refinement
of the UCT selection rule originally proposed for Monte Carlo planning
[@kocsis2006bandit] and surveyed broadly by Browne et al.
[@browne2012mctssurvey]. Here $N(s_t, a)$ is the visit count of action $a$ at
$s_t$, $Q(s_t, a)$ is its mean backed-up value, $P(s_t, a)$ is the network's
prior probability of selecting $a$, and $c_{\text{puct}}$ trades exploration
against exploitation. At a leaf, the network is evaluated once to obtain
$(P(s_t, \cdot), v(s_t))$; $v(s_t)$ is backed up along the traversed path in
place of a random rollout, exactly as in AlphaZero. Because the value target
$z$ of Section III.2 is bounded in $\{-1, +1\}$, the same averaged backup
rule AlphaZero uses for two-player games applies unmodified; this is the
sense in which ranked reward lets this framework avoid the max-based backup
rule Schadd et al. found necessary for single-player MCTS without such a
transform [@schadd2008spmcts].

## Policy and Value Network

We adopt an attention-based encoder-decoder architecture as the network
backbone, following the construction used by Kool et al. for one-shot tour
decoding [@kool2019attention]: an encoder produces a permutation
-equivariant embedding of all $n$ city coordinates, and a decoder,
conditioned on the partial tour represented by $s_t$, attends over the
embeddings of unvisited cities to produce $P(s_t, \cdot)$, masking already
-visited cities. A value head reads a pooled representation of the encoder
output together with the current partial-tour embedding to produce
$v(s_t) \in [-1, 1]$. Unlike Kool et al.'s use of this architecture, here
$P(s_t, \cdot)$ and $v(s_t)$ serve as MCTS priors and leaf values rather than
being read out directly as the executed policy; the graph-embedding network
of Khalil et al. is a viable alternative encoder for the same role
[@khalil2017graphco].

## Self-Play Data Generation with Ranked-Reward Targets

At curriculum stage $n_k$ (Section IV.4), each self-play episode runs PUCT
-guided MCTS with $m$ simulations per decision to construct a complete tour
$\sigma$, storing the visit-count distribution $\pi_{\text{MCTS}}(s_t, \cdot)
\propto N(s_t, \cdot)^{1/\tau}$ at every visited state, where $\tau$ is a
temperature parameter. On completion, $L(\sigma)$ is appended to the
buffer $B_k$, and every stored state in the episode is labeled with the
ranked-reward outcome $z$ of Section III.2, computed by comparing
$L(\sigma)$ against the $\alpha$-quantile of $B_k$ (Laterre et al. use
$\alpha = 0.5$ as a default [@laterre2018rankedreward]):
$$
z =
\begin{cases}
  +1 & \text{if } L(\sigma) \le \text{quantile}_\alpha(B_k) \\
  -1 & \text{otherwise.}
\end{cases}
$$
The network is trained on batches of $(s_t, \pi_{\text{MCTS}}(s_t, \cdot),
z)$ tuples with the AlphaZero loss
$$
\ell(\theta) = \left(z - v_\theta(s_t)\right)^2
  - \pi_{\text{MCTS}}(s_t, \cdot)^\top \log P_\theta(s_t, \cdot)
  + \lambda \lVert \theta \rVert^2,
$$
combining a value-regression term, a policy cross-entropy term against the
search-improved visit distribution, and L2 regularization
[@silver2017alphazero]. Each simulation requires one network forward pass, so
one self-play episode at stage $n_k$ costs $O(n_k \cdot m)$ network
evaluations; this cost, not any change in the algorithm itself, is the
reason Section IV.4 proposes starting the curriculum at small $n$.

## Curriculum Schedule over Instance Size

Because the ranked-reward buffer $B_k$ is only meaningful when the lengths
it contains are commensurate, and because optimal tour length scales with
$\sqrt{n}$ [@beardwood1959shortest], we propose maintaining a separate
buffer $B_k$ per curriculum stage and advancing from stage $n_k$ to $n_{k+1}
> n_k$ only once the network's win rate against its own buffer at $n_k$
exceeds a fixed threshold, mirroring the stage-advancement criterion used
for curriculum learning generally [@bengio2009curriculum] and directly
extending the small-to-large game-complexity progression (Tic-Tac-Toe to
Connect Four to Chess) proposed for the general MCTS/AlphaZero tutorial this
paper's framework was drafted alongside. Network weights carry over across
stages so that representations learned on small instances seed training on
larger ones, rather than each stage training a network from a random
initialization.

# Extension: Zero-Shot Generalization Beyond the Curriculum

A natural extension of the curriculum in Section IV.4 is to evaluate the
final-stage network zero-shot on instance sizes larger than any curriculum
stage it was trained on, the same generalization question Fu et al. address
for their heatmap-plus-MCTS solver [@fu2021generalize]. Two obstacles are
specific to this framework and not addressed by the core methodology above.
First, the branching factor $|A(s_t)| = n - t$ grows with $n$, so full MCTS
becomes impractical at large $n$; a candidate action list restricted to each
city's $k$-nearest unvisited neighbors, as used in several of the
constructive-policy architectures surveyed in Section II
[@kool2019attention], would need to be adopted to keep simulation cost
bounded. Second, the ranked-reward buffer $B_k$ built during training has no
analogue at a held-out instance size, so an evaluation-time proxy, such as
comparing the discovered tour length against a fast heuristic like LKH
[@helsgaun2000lkh] rather than against a training buffer, would be needed to
report a meaningful score. Neither extension has been designed in detail or
evaluated here.

# Illustrative Worked Example

This section hand-traces the search and ranked-reward computation of
Sections III-IV on a five-city instance small enough to reason about by
inspection. This is a hand-constructed illustration of the intended
mechanics, not the output of a trained network or an executed search; no
computational implementation has been built to generate it.

**Instance.** Let $c_1 = (0,0)$, $c_2 = (2,0)$, $c_3 = (2,2)$, $c_4 = (0,2)$,
$c_5 = (1,3)$. All five points lie in convex position (in this cyclic
order), so the optimal tour is exactly the convex-hull cycle
$c_1 \to c_2 \to c_3 \to c_5 \to c_4 \to c_1$, a standard fact for points in
convex position. Its length is
$2 + 2 + \sqrt{2} + \sqrt{2} + 2 = 8.83$, which by symmetry is matched
exactly by the reverse tour $c_1 \to c_4 \to c_5 \to c_3 \to c_2 \to c_1$. So
the two optimal first moves from $s_0$ (with $\sigma(1) = c_1$ fixed) are
$c_2$ and $c_4$; the remaining first moves, $c_3$ and $c_5$, both lead only
to strictly longer tours.

**Root expansion.** Suppose the network's prior at $s_0$, not yet fully
trained, already weakly favors the two optimal moves,
$P(s_0, \cdot) = (0.35, 0.15, 0.35, 0.15)$ over $(c_2, c_3, c_4, c_5)$.
Table I shows an illustrative snapshot of the four children's search
statistics after ten simulations, hand-constructed to reflect the fact that
rollouts through $c_2$ and $c_4$ reach the optimal-length tour (ranked
-reward $z = +1$ against a buffer whose quantile is set near 8.83) while
rollouts through $c_3$ and $c_5$ reach strictly longer tours ($z = -1$).

: Illustrative child-node statistics at the root after ten simulations. $N$
is visit count, $Q$ is mean backed-up value, $P$ is the network prior.

| Child | $N$ | $Q$ | $P$ |
| :--- | ---: | ---: | ---: |
| $c_2$ | 4 | $+0.75$ | 0.35 |
| $c_3$ | 1 | $-1.00$ | 0.15 |
| $c_4$ | 4 | $+0.75$ | 0.35 |
| $c_5$ | 1 | $-1.00$ | 0.15 |

Figure 1 sketches the corresponding search tree: the root's two optimal
children accumulate most of the visit count, one of them (arbitrarily,
$c_2$) is expanded one level further to a leaf representing the completed
optimal tour, and the other two children remain shallow, low-visit branches.
The resulting visit distribution
$\pi_{\text{MCTS}}(s_0, \cdot) \propto (4, 1, 4, 1)^{1/\tau}$ is the policy
target used to train the network at $s_0$, sharpening its prior toward the
two moves search has confirmed are optimal.

![Illustrative PUCT search tree at the root of the five-city example after
ten simulations. Solid nodes ($c_2$, $c_4$) accumulate high visit count and
positive backed-up value; dashed nodes ($c_3$, $c_5$) remain shallow. The
$c_2$ branch is expanded to a leaf representing the completed optimal
tour.](figures/mcts_tree_schematic.png)

**Ranked-reward computation and curriculum loop.** Once the episode
completes with $\sigma = (c_1, c_2, c_3, c_5, c_4)$, $L(\sigma) = 8.83$ is
compared against $\text{quantile}_{0.5}(B_k)$; if this instance's length is
at or below the running median of stage $n_k = 5$'s buffer, every visited
state in this episode is labeled $z = +1$, otherwise $z = -1$, and $L(\sigma)$
is appended to $B_k$ for the next episode's comparison. Figure 2 summarizes
the full loop these steps instantiate across curriculum stages: an instance
generator produces a size-$n_k$ instance, self-play MCTS constructs a tour
against the current network, the ranked-reward buffer $B_k$ converts the
tour length into $z$, the network is updated on the resulting
$(\pi_{\text{MCTS}}, z)$ targets, and once the win rate at stage $n_k$
crosses the advancement threshold of Section IV.4, the curriculum moves to
$n_{k+1}$ with a fresh buffer $B_{k+1}$.

![The proposed curriculum self-play loop: an instance generator produces a
size-$n_k$ instance; self-play MCTS, guided by the current network,
constructs a tour; the ranked-reward buffer $B_k$ converts the tour length
into a bounded outcome $z$; the network is updated on the resulting
targets; and the curriculum advances to stage $n_{k+1}$ once the
win-rate threshold is met.](figures/curriculum_selfplay_loop.png)

# Discussion and Limitations

**No implementation or empirical evaluation.** This paper proposes a
framework and works through a hand-traced illustrative example; no
tour-construction environment, network, MCTS implementation, or self-play
loop has been built, and no reported number in Section VI is measured. All
quantitative claims there are illustrative of intended behavior.

**Ranked-reward calibration is unvalidated.** The quantile level $\alpha$
and buffer size $|B_k|$ jointly determine how quickly the value target
reacts to policy improvement versus how noisy that target is; Laterre et
al. report that these choices matter for training stability on bin packing
[@laterre2018rankedreward], and neither has been tuned or validated for TSP
tour construction, where episode returns are continuous and instance
-dependent in a way single-container bin packing's discrete fill fraction is
not.

**Curriculum stage-advancement criterion is heuristic.** The win-rate
threshold proposed in Section IV.4 for advancing from $n_k$ to $n_{k+1}$ has
no principled derivation here; too low a threshold risks advancing before
the network has learned generalizable structure at the current scale, and
too high a threshold wastes training compute polishing performance at a
scale the final deployment does not need. This is a direct instance of
Question 3 in the note this paper's framework was drafted from, how the
size/complexity progression affects learning speed, applied specifically to
instance-size rather than game-family curricula.

**Branching factor limits scalability without restriction.** Because
$|A(s_t)| = n - t$, full MCTS over all unvisited cities becomes
computationally impractical well before $n$ reaches the sizes classical
heuristics like LKH handle routinely [@helsgaun2000lkh]; Section V's proposed
candidate-list restriction is a plausible mitigation but is not designed in
enough detail here to bound the resulting approximation error.

# Conclusion and Future Work

This paper proposed adapting the AlphaZero self-play recipe to the Traveling
Salesman Problem, formalizing tour construction as a single-player MDP,
adapting the ranked-reward mechanism to supply the bounded, self-relative
outcome that this single-player setting lacks, and proposing an explicit
curriculum over instance size motivated by the known $\sqrt{n}$ scaling of
optimal tour length. We worked through a hand-traced five-city example
illustrating the search, the resulting policy target, and the ranked-reward
computation. No computational implementation or empirical evaluation has
been carried out; the contribution of this paper is the framework and the
open calibration questions it makes precise, not a validated result.

Future work follows the implementation plan below.

1. Implement the tour-construction MDP of Section III and a plain, network
   -free MCTS baseline (uniform priors, rollout-based leaf evaluation) on
   small instances ($n \le 10$), to obtain a working search implementation
   before introducing a network.
2. Integrate the policy-value network of Section IV.2 as MCTS priors and
   leaf values, and verify that network-guided MCTS improves over the plain
   baseline of step 1 at matched simulation budgets.
3. Implement the self-play loop and ranked-reward transform of Section IV.3,
   and empirically tune the quantile level $\alpha$ and buffer size $|B_k|$
   for training stability, the open question identified in Section VII.
4. Introduce the curriculum of Section IV.4, train through a schedule of
   increasing $n$, and evaluate both in-curriculum tour quality and
   zero-shot generalization (Section V) against LKH and the supervised
   MCTS baselines of Xing and Tu and Fu et al. on TSPLIB instances
   [@helsgaun2000lkh; @xing2020gnnmcts; @fu2021generalize; @reinelt1991tsplib].
