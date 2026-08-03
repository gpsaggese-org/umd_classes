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
2. What privacy/data-handling safeguards are needed before logging real
   prompt/response pairs (PII scrubbing, opt-in/opt-out)?
3. Can a distilled small model trained on the logged data match the routed
   "best model per task" quality at a fraction of the cost?

## Research Topics
- LLM API gateway/proxy architecture (streaming passthrough, provider
  abstraction)
- Cost/latency-aware routing policies (bandit-style online learning)
- Knowledge distillation from logged prompt/response pairs

## Next steps
- [ ] Build a minimal passthrough proxy for 2-3 providers with logging
- [ ] Define the storage schema for prompt/response/metadata
- [ ] Add a simple routing policy and measure cost/quality tradeoff
- [ ] Explore distillation from the collected dataset

## References
- OpenRouter — unified API for multiple LLM providers (for reference, not
  reuse of proprietary code)
