# Benchmark Scoping for RL-based Auto-EDA / Structure Discovery

**Author:** @Delvitron1019
**Issue:** #506 — RL agents for EDA and ML
**Scope:** Step 2 ("find a benchmark"). What to measure the agent against, which datasets and
baselines to adopt, and two technical issues in `draft.RL_for_auto_EDA.md` that the benchmark
literature forces us to fix.
**Status:** first pass for GP review.

## TL;DR

Don't build a benchmark from scratch — **adopt an existing causal-discovery harness**. The task
in the draft (recover a graph, score against a known `G*` with structural Hamming distance) is
exactly what the causal-discovery community already benchmarks, with settled datasets, baselines,
and metrics. Recommendation: use **gCastle** (generators + baselines + metrics in one package,
and it already contains the most important baseline) plus **causal-learn** (hosts the standard
ground-truth datasets). Evaluate on three tiers: synthetic random DAGs (train + primary eval),
standard discrete Bayesian networks (external validity), and **SACHS** (the one real dataset with
a validated ground-truth graph). Primary metric: **SHD**, plus TPR/FDR and out-of-sample
prediction.

Two things this step surfaced that matter more than the benchmark choice itself, both flagged
here for discussion rather than settled:

1. **The closest prior art is RL-BIC (Zhu et al., ICLR 2020)** — RL + causal discovery + a
   score-based reward with acyclicity penalties. It sits outside the autoEDA list, so the step-1
   review didn't reach it. Usefully, it uses RL as a **per-instance search** rather than a learned
   transferable policy — the same distinction that separates this project from AlphaClean — so it
   sharpens our novelty claim rather than threatening it. Worth adding to both the SOTA review and
   the draft.
2. **An identifiability question on the first worked example.** From purely observational
   linear-Gaussian data, DAGs are identifiable only up to the Markov equivalence class, so edge
   *direction* may not be recoverable as that example describes. A couple of ways to resolve it
   below — flagging for GP to confirm which was intended.

## Recommended harnesses (adopt, don't reinvent)

- **gCastle** (Huawei Noah's Ark Lab; Zhang et al., 2021). One package with (a) synthetic data
  simulation — Erdős–Rényi and scale-free random DAGs, linear/nonlinear SEMs, configurable node
  count, edge density, sample size, and noise; (b) baseline algorithms — PC, GES, LiNGAM,
  Direct-LiNGAM, NOTEARS, DAG-GNN, GraN-DAG, GOLEM; and (c) metrics — SHD, TPR, FDR. Crucially it
  is from the **same group that wrote RL-BIC**, so our key RL baseline lives here too. This single
  package covers Milestone-1 (environment), Milestone-2 (scoring), and the baseline suite.
- **causal-learn** (py-why / DoWhy ecosystem). Maintained Python library that **hosts the standard
  ground-truth benchmark datasets** (ASIA, CHILD, ALARM, HEPAR2 as CSV + ground-truth graphs) and
  independence tests (Fisher-Z, etc.) that map directly onto the draft's toolbox.

Using these two means "find a benchmark" is mostly a decision to adopt, not a build — which is
the right call given the 0.5-day ETA.

## Benchmark tiers

| Tier | Datasets | Ground truth | Role |
|---|---|---|---|
| 1. Synthetic random DAGs | ER / scale-free graphs, linear-Gaussian **and** LiNGAM (non-Gaussian) SEMs | Exact (we generate `G*`) | **Training + primary eval.** This *is* Milestone-1's environment; gCastle generates it natively |
| 2. Standard discrete BNs | ASIA (8 nodes), CHILD (20), ALARM (37), HEPAR2 (70) | Known consensus DAG | External validity on realistic structures of increasing size |
| 3. Real data, known graph | **SACHS** (11 nodes, ~17 edges, protein signaling) | Experimentally validated | **Sim-to-real crown jewel** — the one place real messy data meets a trusted graph |
| 4. Stretch / later | SynTReN, SERGIO (gene-net simulators); CausalDynamics (NeurIPS 2025), TimeGraph (KDD 2025) | Semi-synthetic / synthetic | Only if we extend to time-series or gene-regulatory settings — beyond the current i.i.d. scope |

## Baselines to beat

- **Classical**: PC (constraint-based, independence tests) and GES (score-based). The floor.
- **Continuous-optimization**: NOTEARS, and newer GOLEM / DAG-GNN / GraN-DAG. The modern bar.
- **RL-BIC (Zhu et al., 2020)** — the direct ancestor and the baseline that matters most. It uses
  an encoder-decoder over observed data to emit adjacency matrices, scored by BIC plus acyclicity
  penalties, optimized with actor-critic. Notably, its own paper describes RL used "as a search
  strategy," with the output being the best graph found during training rather than a learned
  policy. Matching or beating it *with a transferable policy that generalizes to unseen graphs*
  would be a clean headline result.
- **Scripted/heuristic agent** — the draft's own Milestone-2 baseline. Establishes that learning
  beats a fixed script.

Documented RL-BIC limitations we should heed: it works only up to ~30 nodes, its action space
(whole directed graphs) explodes with size, and reward computation dominates runtime. Our tool-use
action space (a sequence of statistical operations) is smaller and more structured than "emit an
adjacency matrix," which may be an advantage worth stating explicitly — but the compute warning is
real. **Start with small graphs (≤10–15 nodes).**

## Metrics

- **SHD (Structural Hamming Distance)** — primary; edge additions + deletions + reversals to turn
  `Ĝ` into `G*`. Lower is better. This is the field standard and matches the draft's reward.
- **TPR / FDR** — precision/recall on edges; standard companions to SHD.
- **SID** — penalizes causal-ordering errors; complements SHD.
- **Out-of-sample prediction on `D_test`** — the draft's second reward component; keep it, it
  captures predictive usefulness even where structure is only partially identifiable.
- **Important subtlety**: when the model is identifiable only to the Markov equivalence class,
  score **SHD between CPDAGs** (not raw DAGs), or you penalize the agent for orientations that are
  fundamentally unrecoverable from observational data. This directly affects reward design.

## Two proposals for the draft (for GP to confirm)

1. **Linear-Gaussian example (Key Examples #1).** The draft has the agent recover "both edge
   existence and direction" on a linear-Gaussian DAG via repeated `y`-`x` regression. From purely
   observational linear-Gaussian data, edge direction is identifiable only up to the Markov
   equivalence class (the CPDAG), so full-direction recovery there may not be attainable unless
   interventional data was intended. Three ways forward, if this is worth changing: (a) switch the
   default generative model to **LiNGAM** (non-Gaussian noise, which *is* fully identifiable — and
   is exactly where RL-BIC beat GES), (b) use nonlinear SEMs, or (c) allow interventional data.
   Suggested default: LiNGAM for Tier-1, so direction is identifiable and we line up against
   RL-BIC's strongest published result. **GP — was the linear-Gaussian example meant to be
   observational, or did you have interventions in mind?**

2. **Consider a CPDAG-aware reward.** Following from the above, where direction isn't identifiable
   the verifiable reward likely wants to compare equivalence classes (CPDAGs) rather than raw DAGs,
   so the agent isn't penalized for orientations no method could recover from observational data.
   Small change, meaningful effect on training stability — worth a quick decision before Milestone-2
   scoring is wired up.

## Positioning update (feeds back into SOTA review + draft)

The novelty claim is now crisper and defensible against the *closest* possible prior art:

> Prior RL-for-causal-discovery (RL-BIC) and prior search-against-objective systems (AlphaClean)
> both run a **fresh per-instance search** and score against a **proxy** objective (BIC / a
> user-defined quality function). This project trains a **transferable policy** with a
> **verifiable** reward from a known generating process, so it amortizes discovery across datasets
> instead of re-searching each one. That combination — verifiable reward + transferable policy for
> structure discovery — is what's missing from both the autoEDA and causal-discovery literatures.

## Honest caveats

- **Real ground-truth benchmarks are genuinely scarce.** The causal-discovery literature says this
  repeatedly; Tier 3 is essentially just SACHS. Sim-to-real claims (Milestone-4) rest on a narrow
  base — that milestone is the project's riskiest, and GP should know it going in.
- I confirmed the harnesses and datasets against 2025 survey/benchmark papers, but I have **not yet
  run gCastle** to verify its generators expose `G*` in the form our scorer needs. That is the
  concrete next sub-step and overlaps Milestone-1.
- Tier-4 datasets are time-series; adopting them would change the problem scope. Flagged, not
  recommended yet.

## Suggested checklist updates for #506

- [x] Step 2: benchmark scoping (this document)
- [ ] Add RL-BIC (Zhu et al. 2020) to the SOTA review + draft as closest prior art
- [ ] Confirm with GP: linear-Gaussian example → LiNGAM, and CPDAG-aware reward
- [ ] Install gCastle + causal-learn; confirm generators expose ground-truth `G*` for scoring
- [ ] Pull SACHS + one discrete BN (ASIA) as the first external-validity checks
