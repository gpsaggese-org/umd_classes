# Class Projects — Conference / Journal Paper Candidates

- Screen of `README.md` ("Done" projects, DATA605 + MSML610) for candidates that
  could plausibly become a conference or journal paper
- This is a **title/description-level screen**, not a code review
  - Before drafting a paper, open the candidate's `Result` notebook/README and
    verify: real dataset (not synthetic/toy), reproducible results, and a claim
    beyond "ran library X"

## Criteria used

Not defined in `README.md` itself — inferred:

- **Novelty**: new domain/problem, not a repeat of the same tutorial theme with
  a different library
- **Methodological rigor**: uses a real research method (causal inference, RL,
  GNN, distributed training) vs. a thin wrapper around a library's quickstart
- **Real-world significance**: applied to a consequential domain (health,
  finance/fraud, drug discovery, security)
- **Completion evidence**: `Done` status, named author(s), actual `Result` dir
  (unattributed `—` rows are weaker evidence of vetted work)

## Tier 1 — strongest paper candidates

### Spring2023 quant-finance research set
(`data605/Spring2023/ml_projects/`) — actual open-research-question projects,
not tool tutorials; closest to publishable quant-finance work

- `Implement_Avellaneda_model` — market-making model, well-known
  microstructure literature to position against
- `Predict_bid_ask_with_order_book_data` — order-book microstructure
  prediction
- `Predict_Intraday_Trading_Volume`
- `Predict_large_asset_movements_with_NLP`
- Caveat: authors listed as `—` (unattributed); confirm who actually did the
  work before pitching

### MSML610 causal-inference / GNN / RLHF projects
Genuine research methods on consequential domains

- `EconML` (3 results: health interventions, education outcomes) — causal ML +
  econometrics, strong journal fit (health econ / causal inference venues)
- `CausalML` — lifestyle programs vs. diabetes outcomes
- `Tetrad` — causal discovery in social-media sentiment
- `causal-learn` — causal discovery, economic factors vs. employment
- `PyTorch Geometric` — GNN drug-drug interaction prediction (bio/pharma
  novelty)
- `DGL` — GNN fraud detection in credit-card transactions
- `NetworkX` — graph-based financial fraud detection
- `BoTorch` (2 results) — Bayesian optimization for ChEMBL compound selection
  (drug discovery)
- `trl` / `trlx` (3 results) — RLHF: dialogue enhancement, sentiment RL,
  summarization w/ feedback loop — hot research area

## Tier 2 — solid applied-ML candidates (MSML610)

Real technique + real domain, less headline-novel

- `Horovod`, `DeepSpeed` — distributed-training systems angle (transformer
  text-gen, ViT fine-tuning)
- `HMMlearn` — network-traffic anomaly detection (security)
- `tsfresh` — IoT anomaly detection
- `LakeFS` — financial-transaction anomaly detection
- `Optuna` (2 results) — HPO for customer segmentation
- `auto-sklearn` (2 results) — AutoML, traffic-flow anomaly / housing
- `ONNX` (2 results) — fake-news detection, stock forecasting
- `JAX` — wildlife image classification (conservation angle)
- `flash-attn` — efficient attention for scientific-paper topic modeling
- `TorchRL` — multi-agent cooperation

## Tier 3 — weak candidates (DATA605 Bitcoin tutorials)

~90% of DATA605 "Done" rows apply a different library to the **same**
real-time-Bitcoin-pipeline problem. Low novelty as a set — one tool swapped for
another, no new method or finding. Skip these for papers unless the
*systems/engineering* angle itself is the contribution (e.g., a
benchmark/comparison paper across tools).

Exceptions that break the Bitcoin template (worth a second look):

- `Dataprep` (2026) — housing price prediction
- `Clickhouse` (2026) — user-engagement prediction
- `Ansible` (2026) — deployment automation (systems paper angle, not ML)
- `DocsGPT`, `txtai`, `HuggingFace`, `Gensim`, `FastText` — NLP-task variants
  (classification / topic-modeling / RAG), moderate novelty

## Recommendation

Shortlist = Tier 1. Next step: open the Tier 1 result notebooks and do a deep
review pass to confirm dataset quality, reproducibility, and a contribution
beyond "ran library X".
