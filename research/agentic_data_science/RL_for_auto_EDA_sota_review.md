# SOTA Review: Automated EDA and the Gap for RLVR-Based Structure Discovery

**Author:** @Delvitron1019
**Issue:** #506 — RL agents for EDA and ML
**Scope:** Review of `mstaniak/autoEDA-resources` against the `draft.RL_for_auto_EDA.md` framing, plus the adjacent literature the list does not cover.
**Status:** first pass for GP review.

## TL;DR

The `autoEDA-resources` list is a near-complete map of one thing: **descriptive, heuristic
auto-EDA** — tools that summarize a dataset (stats, univariate/bivariate plots, correlation)
and emit a report. Almost nothing in the list *learns* a policy, and nothing scores its output
against a known data-generating process. The project's framing — a learned policy over tool
calls, trained with a **verifiable reward** against a synthetic ground-truth graph — sits in a
gap this list does not cover. The two nearest neighbors are (a) the recent LLM-based EDA work
and (b) pipeline-search systems like AlphaClean. The reward metric the draft proposes
(structural Hamming distance to a DAG) actually belongs to the **causal structure discovery**
literature, which this list omits entirely and which we will need to review separately.

## How the landscape breaks down

The ~60 resources cluster into five groups. The relevant axis for us is not R-vs-Python but
**descriptive vs. inferential** and **heuristic vs. learned**.

### 1. Descriptive report generators (the bulk of the list) — heuristic
`pandas-profiling`, `SmartEDA`, `DataExplorer`, `sweetviz`, `DataPrep`, `AutoViz`, `dlookr`,
`skimr`, `funModeling`, and ~20 more. These apply a **fixed rule set**: compute summary stats,
plot every variable, plot pairwise relationships, flag missingness/outliers. No decisions are
learned; the "analysis" is a predetermined template. They answer *"what does this data look
like"*, never *"what process generated it"*. This is precisely the hand-crafted-heuristic
category the draft's Question 3 aims to replace.

### 2. Visualization recommendation — mostly optimization/heuristic, one learned
`Voyager` / `Voyager 2`, `Foresight`, `DIVE`, `VizDeck`, `Datamations`, and the
"Task-Oriented Optimal Sequencing of Visualization Charts" paper. These rank or recommend
*charts* by an interestingness/optimization objective. The outlier is **VizML** (Hu et al.),
which *learns* viz recommendation from a large corpus of human-made plots — the closest thing
in the list to a learned EDA policy, but the target is chart choice, not structure recovery.

### 3. Pipeline search / cleaning / feature engineering — search-based
`AlphaClean`, `TPOT`, `featuretools`, `vtreat`. **AlphaClean is the most methodologically
relevant item on the entire list, and I read it.** It uses a **generate-then-search**
framework: cleaning operators each propose candidate cell-level edits into a shared pool, and a
tree-search algorithm sequences them into a pipeline that **maximizes a user-defined quality
measure** (expressed as weighted sums of SQL aggregate queries). Reported up to 9x higher
quality than black-box parameter tuning.

Why it matters for us: the skeleton is *exactly* our MDP — a set of operations, a scored
objective, and a search over operation sequences to maximize it. Two differences define our
contribution against it: (1) AlphaClean's objective is a **user-specified** quality function,
whereas ours is a **verifiable** reward from a known generating process — no human has to
define "good"; (2) AlphaClean **searches per-instance** (re-runs search on every new dataset),
whereas RLVR trains a **transferable policy** meant to generalize to unseen graphs. So
AlphaClean is the right thing to cite as "search-against-an-objective prior art," and the
contrast (verifiable vs. user-defined, learned policy vs. per-instance search) is a clean way
to state our delta. TPOT does genetic-programming search over ML pipelines — same per-instance,
non-verifiable pattern.

### 4. Insight extraction / augmented analytics — heuristic
"Extracting Top-K Insights from Multi-dimensional Data", `Voder`, Foresight. These define an
"insight" (e.g., an unusually high aggregate) and mine for it. Useful for thinking about what
counts as a *finding*, but the insight definitions are hand-specified, not learned or verified.

### 5. LLM-based EDA (newest) — read in depth; less of a competitor than the title suggests
"Towards Automated Cross-domain Exploratory Data Analysis through Large Language Models"
(arXiv 2412.07214, Dec 2024, VLDB 2025) and `Chat2Query`. **I read the first one.** It's the
**TiInsight** system from PingCAP, and its "EDA" is specifically *SQL-based database
exploration*: four stages — hierarchical data context (LLM-summarized schema for cross-domain
generalization), question clarification/decomposition, **text-to-SQL** (TiSQL), and
**text-to-visualization** (TiChart). It's evaluated on Spider (86.3% execution accuracy with
GPT-4) and Bird — i.e., query-correctness benchmarks, not structure recovery.

**Important correction to my first pass:** this is *not* a direct competitor to what the draft
proposes. Its task is "turn a user question into the right SQL + chart," not "recover the
process that generated the data." So it's a weaker baseline than the title implies, and its
existence actually *strengthens* our novelty claim — even the flagship LLM-EDA system stops at
querying and charting, not at inferring structure. It's still worth citing as the state of
LLM-driven EDA, but GP's step-3 prototype isn't competing with it head-to-head.

## Mapping to the draft's framing

| Draft ingredient | Covered by this list? | Where |
|---|---|---|
| Descriptive EDA automation | Yes, exhaustively | groups 1–2 |
| Learned policy over actions | Barely | VizML (viz only) |
| Search against an objective | Partially | AlphaClean, TPOT |
| LLM agent doing EDA | Yes, recent | 2412.07214, Chat2Query |
| **Verifiable reward vs. known ground-truth graph** | **No** | — |
| **Structure / causal discovery as the target output** | **No** | — |
| RL / policy-gradient training for EDA | No | — |

The bottom two rows are the project's actual contribution, and neither appears in the list.

## The gap this list doesn't show (important)

This is an **auto-EDA** resource list, so it stops at description. But the draft's reward is
`structural Hamming distance between Ĝ and G*` — that is a **causal structure discovery**
metric, and that entire field is absent here. Before finalizing the reward and the Milestone-2
scoring pipeline, we should do a second, separate SOTA pass on:

- **Constraint-based discovery**: PC, FCI algorithms (independence-test driven — directly
  relevant since the draft's toolbox is built on independence tests).
- **Score-based discovery**: GES, and **NOTEARS** (continuous-optimization structure learning)
  — the modern baseline our learned policy would be compared against.
- **Metrics**: structural Hamming distance, SID, and why predictive-on-`D_test` is a needed
  complement (the draft already intuits this by combining both).
- **Synthetic-graph generation**: `pgmpy` random BNs and `sklearn` generators are named in the
  draft; worth confirming they give controllable-complexity DAGs with known edges.

Framing point for GP: the project is best positioned as sitting at the **intersection of
auto-EDA (this list) and causal discovery (not in this list)** — using an RLVR recipe borrowed
from math/code to bridge them. That intersection is empty in both literatures, which is the
strongest version of the novelty claim.

## Recommended reading shortlist (not all 60)

Prioritized for the reward/eval design we need next:

1. **AlphaClean** (arXiv 1904.11827) — *read.* Generate-then-search over operations vs. a
   quality objective; closest methodological cousin. See group 3 above.
2. **Towards Automated Cross-domain EDA through LLMs / TiInsight** (arXiv 2412.07214) — *read.*
   SQL + viz automation, not structure discovery; a citable baseline but not a head-to-head
   competitor. See group 5 above.
3. **Issues in Automating Exploratory Data Analysis** (Semantic Scholar) — foundational
   framing of why EDA resists automation; useful for the write-up's motivation.
4. **The Landscape of R Packages for Automated EDA** (R Journal 2019) — read this *instead of*
   the ~30 individual descriptive-package docs; it summarizes group 1 in one pass.
5. **VizML** — the one learned-policy example in the list.
6. **Extracting Top-K Insights** — for defining what counts as a "finding."

Plus, from outside this list, the pre-LLM AutoML survey GP already sent (arXiv 2010.10777) and
the causal-discovery sources above.

## Honest caveats

- The list is **dated** — mostly 2018–2019, with only two 2024 additions (2412.07214,
  Chat2Query). The RL/agentic angle is essentially post-dates it, which is good for novelty but
  means this list alone is not a sufficient related-work section.
- Several links are R-package CRAN pages, not research; skimmable, low priority.
- I have now read the **two most relevant** papers in full (AlphaClean and the TiInsight
  LLM-EDA paper); the other four on the shortlist are read only at abstract/description level.
  Reading those four is a small remaining sub-step that feeds Milestone-2 reward design.

## Suggested checklist updates for #506 / #509

- [x] SOTA review of the autoEDA landscape (this document)
- [ ] Second SOTA pass: causal structure discovery (PC / GES / NOTEARS + SHD metric)
- [ ] Read the six-paper shortlist, extract reward-design implications
- [ ] Confirm `pgmpy` / `sklearn` generators expose ground-truth edges for scoring
