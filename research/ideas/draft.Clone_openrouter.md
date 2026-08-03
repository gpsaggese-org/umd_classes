# OpenRouter Clone for Collecting Prompt/Response Training Data

## Status
- **Status**: draft
- **Complete Specs**: 15%
- **Assignee**: TBD

## Core Idea
- Build a lightweight LLM API gateway, modeled on OpenRouter, that proxies
  requests to multiple providers/models behind a single API, but with the
  explicit goal of logging every prompt/response pair to build a proprietary
  dataset for fine-tuning or evaluation
- Beyond pure logging, add routing logic: pick which underlying model to use
  per-request based on cost, latency, or task type, and measure whether
  routing decisions can be learned from the collected data itself
  (self-improving router)

## Difficulty-Aware Routing and Model Fusion
- The interesting research question inside the gateway is not "which model is
  best" but "how much intelligence does *this* request actually need"
- Train a difficulty estimator `q(prompt) -> required capability level`, then
  route: cheap/small model below a threshold, frontier model above it
- Fusion variant: send the request to several models and combine their answers
  (majority vote, verifier model, or a learned combiner) instead of picking one
  — trading cost for accuracy in the opposite direction from routing
- The estimator has to be *cheaper than the saving*, otherwise the router costs
  more than routing to the strong model every time, which is the trap this
  design must measure explicitly
- Training signal comes for free from the logged data: for prompts answered by
  several models, whether the cheap model's answer matched the strong model's
  is a label for "this prompt was easy"
- Related: an arena backend ([[draft.Build_an_LLM_Arena]]) gives the pairwise
  quality judgments needed to score routing decisions

## Key Examples
- **Passive logging mode**: every request/response pair (with provider,
  model, latency, cost, and any user feedback signal) is stored, without
  changing behavior — just for future dataset construction
- **Routing experiment**: given a task classifier, route "easy" requests to a
  cheap/fast model and "hard" ones to a stronger model; measure cost savings
  vs. quality degradation
- **Dataset reuse**: use the logged prompt/response pairs to fine-tune a
  smaller model to approximate a stronger model's outputs on the observed
  task distribution (distillation)

## Questions
1. How much of OpenRouter's value is the unified API vs. the routing
   intelligence — is a simple pass-through logger already useful for dataset
   building, or does routing quality matter for data diversity?
2. Can request difficulty be estimated cheaply enough that difficulty-aware
   routing nets a real cost saving, and what fraction of traffic can be served
   by a small model with no measurable quality loss?
3. Fusion vs. routing: for a fixed budget, is it better to pick one model well
   or to query several cheap models and combine their answers?
4. What privacy/data-handling safeguards are needed before logging real
   prompt/response pairs (PII scrubbing, opt-in/opt-out)?
5. Can a distilled small model trained on the logged data match the routed
   "best model per task" quality at a fraction of the cost?

## Research Topics
- LLM API gateway/proxy architecture (streaming passthrough, provider
  abstraction)
- Cost/latency-aware routing policies (bandit-style online learning)
- Prompt difficulty estimation and cascade/deferral policies (RouteLLM,
  FrugalGPT-style cascades)
- Answer fusion: majority vote, verifier-based selection, learned combiners
- Knowledge distillation from logged prompt/response pairs, with corpora from
  [[draft.Datasets_for_Training_and_Distilling_LLMs]]

## Next steps
- [ ] Build a minimal passthrough proxy for 2-3 providers with logging
- [ ] Define the storage schema for prompt/response/metadata
- [ ] Add a simple routing policy and measure cost/quality tradeoff
- [ ] Train a difficulty estimator from logged agreement between cheap and
      strong models, and measure the cost/quality frontier it produces
- [ ] Explore distillation from the collected dataset

## References
- OpenRouter — unified API for multiple LLM providers (for reference, not
  reuse of proprietary code)
- Chen, L., et al., _FrugalGPT: How to Use Large Language Models While Reducing
  Cost and Improving Performance_. (2023)
- Ong, I., et al., _RouteLLM: Learning to Route LLMs with Preference Data_.
  (2024)
