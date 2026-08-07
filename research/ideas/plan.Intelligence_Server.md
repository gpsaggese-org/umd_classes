# Intelligence Server

## Goal
- Build a lightweight LLM API gateway (modeled on OpenRouter) that proxies
  requests to multiple providers, logs every prompt/response pair, adds
  difficulty-aware routing, and serves as the fulfillment/monitoring layer
  for [[draft.Intelligence_Market]]
- Background/formalization: [[draft.Intelligence_Server]]

## Solution

### PR1: [ ] Minimal passthrough proxy with logging
- Support 2-3 providers behind one API
- Define the storage schema for prompt, response, and metadata (provider,
  model, latency, cost)
- Log raw, unscrubbed prompt/response pairs for now, scoped to
  synthetic/test traffic only; add PII scrubbing as a follow-up before any
  real non-synthetic traffic is logged (tracked as an open question below)
- Unit tests (per `testing.rules.md`): request routed to each configured
  provider is logged with correct schema and fields
- Result: every request/response pair is logged and queryable

### PR2: [ ] Routing policy + cost/quality measurement
- Add a simple routing policy (e.g., a task classifier): route to a cheap
  or fast model vs. a stronger model
- Measure cost and quality against an always-call-the-strong-model
  baseline, using logged data from PR1
- Unit tests: routing policy selects the expected model per test-case
  classification; cost/quality metrics computed correctly on a fixture log
- Result: a measured cost/quality frontier for at least one routing policy

### PR3: [ ] Difficulty estimator + distillation experiment (prototype)
- Exploratory/research PR, lighter bar than PR1/PR2: tests cover pipeline
  plumbing (data loads, estimator trains, metrics compute), not a model
  quality bar
- Train `q(prompt) -> required capability level` from logged agreement
  between cheap and strong models (PR2's routing data)
- Explore distilling a small model from the collected dataset
- Result: a difficulty-aware router with a measured saving, and a first
  distillation experiment with reported (not necessarily strong) results

### PR4: [ ] Fulfillment monitoring wired to the market (stubbed both sides)
- Track measured reliability and latency per contract, flag a violation
  when `measured_reliability < R_min` or `measured_latency > L_max`
- Report violations via a **mocked** market-facing interface, matching the
  mock fulfillment interface on the [[draft.Intelligence_Market]] side
  (its PR2) — real integration is deferred until both plans reach this
  point together
- Unit tests: violation correctly flagged/not-flagged against fixture
  contracts and measured outcomes; mocked report call invoked with the
  right payload
- Result: closed loop between a matched contract and its measured
  fulfillment, real once both sides swap the mock for the real interface

## Open questions
- Not blocking PR1-PR4 as scoped above; track before broader rollout
1. Is a simple pass-through logger already useful for dataset building, or
   does routing quality matter for data diversity? (affects how much PR2
   matters before starting PR3's dataset use)
2. Can request difficulty be estimated cheaply enough that difficulty-aware
   routing nets a real cost saving? (PR3's core research question)
3. Fusion vs. routing: for a fixed budget, is it better to pick one model
   well or query several cheap models and combine answers? (not yet
   scoped into any PR — candidate for a PR5 if PR3 shows routing alone is
   insufficient)
4. **PII/data-handling safeguards** before logging real (non-synthetic)
   prompt/response pairs — PR1 defers scrubbing and stays on
   synthetic/test traffic only until this is resolved; must be answered
   before enabling real traffic logging
5. Can a distilled model match routed "best model per task" quality at a
   fraction of the cost? (PR3's distillation sub-question)
6. How reliably can the server attribute a quality/latency shortfall to a
   specific provider vs. noise, so fulfillment reporting to
   [[draft.Intelligence_Market]] is trustworthy enough to affect pricing?
   (affects whether PR4's real integration, once un-mocked, can be trusted)

## Conventions
- Code: `.claude/skills/coding.rules.md`
- Tests: `.claude/skills/testing.rules.md`

## References
- Background/formalization: [[draft.Intelligence_Server]]
- Market this fulfills: [[draft.Intelligence_Market]] (see its own
  `plan.Intelligence_Market.md` — PR2 there mocks the fulfillment call
  this plan's PR4 answers)
- OpenRouter: unified API for multiple LLM providers (reference only)
- Chen, L., et al., _FrugalGPT: How to Use Large Language Models While
  Reducing Cost and Improving Performance_. (2023)
- Ong, I., et al., _RouteLLM: Learning to Route LLMs with Preference Data_.
  (2024)
