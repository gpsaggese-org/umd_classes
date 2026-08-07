# Noesis implementation plan

## Goal
- Build a working prototype of the \Noesis{} protocol

- The \Noesis{} protocol overview is in `papers/Noesis/01_introduction.tex`

## Roadmap

- **Milestone 1: a minimal batch call-auction simulator.** An in-memory
  order book with bid/ask submission and per-tier uniform-price clearing,
  implementing the clearing problem for the complete-compatibility-graph
  case of the existence-of-a-clearing-price proposition. Result: a
  unit-tested auction that clears correctly on synthetic order books, with
  no real settlement (`NoesisMarket` PR1).

- **Milestone 2: a minimal passthrough proxy with logging.** A gateway
  supporting two or three providers behind one API, implementing the
  logging schema of the gateway architecture. Result: every
  request/response pair is logged and queryable, independent of
  Milestone 1 (`NoesisServer` PR1).

- **Milestone 3: contract schema and dispatch integration.** Wire
  Milestone 1's cleared bids to Milestone 2's proxy: define the contract
  schema in code, and hand off a cleared contract from `NoesisMarket` to
  `NoesisServer` for execution. Result: a closed loop in which a matched
  contract is dispatched and executed, though not yet monitored for
  fulfillment (`NoesisMarket` PR2).

- **Milestone 4: a routing experiment.** Add a simple routing policy
  (e.g., a task classifier standing in for the difficulty estimator
  $\hat d$) to the proxy from Milestone 2, and measure cost against
  quality relative to always calling the strongest model. Result: a
  measured cost/quality frontier for at least one routing policy
  (`NoesisServer` PR2).

- **Milestone 5: fulfillment monitoring and the reputation feedback
  loop.** Implement the measured-reliability computation and the
  reliability lower-bound violation test in `NoesisServer`, and the
  reputation update in `NoesisMarket`. Result: a contract dispatched under
  Milestone 3 has its fulfillment measured, and a seller that
  under-delivers is priced out or excluded from subsequent rounds
  (`NoesisServer` PR4, `NoesisMarket` PR3).

- **Milestone 6: a difficulty estimator and a first distillation
  experiment.** Train the difficulty estimator $\hat d$ from the logged
  agreement label, evaluate the routing saving condition on real traffic,
  and run a first distillation experiment on the logged corpus (training
  signal and distillation). Result: a difficulty-aware router with a
  measured saving, and a first distilled model (`NoesisServer` PR3).

- **Milestone 7: the full closed loop.** With Milestones 1 through 6 in
  place, run `NoesisMarket` and `NoesisServer` together end to end: bids
  and asks clear into contracts, contracts are executed and monitored,
  fulfillment results feed back into pricing and eligibility, and routing
  and fusion decisions are informed by the accumulating logged corpus.
  Result: a working prototype exercising every mechanism described in the
  `NoesisMarket` and `NoesisServer` sections of the paper.

- **Milestone 8: post-closed-loop extensions.** With Milestone 7's closed
  loop in place, five further mechanisms described in the paper but not
  yet exercised by the prototype: answer fusion, a statistically sound
  fulfillment violation test, pricing dissemination, cross-tier
  compatibility, and a commit-reveal blind-bid simulation (`NoesisServer`
  PR5-PR6, `NoesisMarket` PR4-PR6 below). Unlike Milestones 1-7, these do
  not depend on each other and can be built in any order.

- **Milestone 9: productization.** Wrap the closed loop of Milestone 7
  behind a public API, deploy it to a cloud target, and let a buyer fund
  an account with a credit card or crypto before bidding (`NoesisPlatform`
  PR1-PR3 below). This is orthogonal to Milestone 8: it makes the
  Milestone 7 loop reachable by a real external caller rather than adding
  a new market or server mechanism.

- **Milestone 10: OpenRouter interoperability.** Two independent additions
  that connect `NoesisServer` to the real OpenRouter service instead of
  test stand-ins: back `Gateway`'s provider pool with a real OpenRouter
  call for real multi-provider liquidity (`01_introduction.tex`'s
  "provider-agnostic liquidity pooling" property), and expose an
  OpenRouter-shaped API surface so an existing OpenRouter client can
  consume `NoesisServer` unmodified (`NoesisServer` PR7-PR8 below). Like
  Milestone 8, this does not depend on Milestone 7's closed loop and can
  be built before or after it.

Each milestone is scoped to be independently demonstrable within one to two
days of focused work, consistent with the goal of showing progress
incrementally rather than attempting the full closed loop in one step.

## NoesisMarket

### Goal
- Build a minimal working intelligence market: a batch call-auction that
  matches buyer/seller contracts for LLM inference bundling capability
  tier, latency, and reliability guarantees, dispatches cleared contracts
  for fulfillment, and feeds delivery performance back into pricing
- Background/formalization: [[draft.Intelligence_Market]],
  `papers/Noesis/04_noesis_market.tex`

### Solution

#### PR1: [x] Minimal batch call-auction simulator
- In-memory order book: bid `(N_tasks, C_level_min, L_max, R_min, P_max)`
  and ask `(N_tasks, C_level, L_typical, R_typical, P_min)` submission
- Bucket bids/asks by capability tier `C_level`; every `T = 5` min, clear
  each tier at a single uniform price (highest-bid-first vs.
  lowest-ask-first) until supply and demand cross
- Defaults, pending the open questions below: task unit = tokens, no
  anti-gaming checks, single currency, fixed 5-min batch cadence
- Unit tests (per `testing.rules.md`): clears correctly on synthetic order
  books — single tier, multiple tiers, no-match case, partial fill
- Result: unit-tested auction library; no real settlement yet

#### PR2: [x] Contract schema + dispatch to a stubbed fulfillment layer
- Define the contract schema `(N_tasks, C_level, L_max, R_min, P)` from a
  cleared PR1 match
- Dispatch each cleared contract to a **mock** fulfillment interface
  (fixed or randomized pass/fail outcomes), standing in for
  [[draft.Intelligence_Server]], which has no implementation yet
- Log the (mocked) fulfillment result back onto the contract record
- Result: closed loop match -> contract -> dispatch -> logged outcome,
  mocked past the auction boundary; swap-in point for the real
  [[draft.Intelligence_Server]] once it exists

#### PR3: [ ] Reputation and pricing feedback loop
- Feed logged fulfillment outcomes (from PR2, mocked or real) into
  per-seller eligibility and a pricing adjustment for future auction
  rounds
- Sellers whose measured reliability drops below `R_min` on repeated
  contracts are priced out or excluded from subsequent rounds
- Result: sellers that under-deliver lose eligibility/priority in later
  auctions

#### PR4: [ ] Pricing dissemination feed
- Background: `papers/Noesis/02_market_design.tex` lists pricing
  dissemination as one of the protocol's five pluggable components: each
  round's cleared price $p^*(c, t)$ per tier is a useful signal beyond the
  bidders and sellers of the round that produced it
- Publish each round's per-tier `(tier, round_id, clearing_price,
  matched_volume)` outcome (from PR1's `clear_round()`) to subscribers
  through a simple pub/sub interface (e.g., an in-memory event bus or
  callback registry), so a buyer timing a future bid, another market
  maker, or a monitoring dashboard does not need to poll `NoesisMarket` or
  wait for the next round to see the previous one's price
- Unit tests: a subscriber registered before a round receives exactly one
  event per cleared tier with the correct fields; a subscriber registered
  after a round does not receive past events by default, but can retrieve
  them from a bounded history buffer
- Result: cleared prices are queryable/subscribable independent of
  winning or losing a match; a real-time push feed is the default
  implementation here, with an on-chain event log flagged in
  `papers/Noesis/08_decentralized_extension.tex` as the pluggable
  alternative

#### PR5: [ ] Cross-tier compatibility (generalized bucketing)
- Background: `papers/Noesis/04_noesis_market.tex`'s Remark on tier
  generalization notes that a bid's compatibility definition already
  allows a higher-tier ask to satisfy a lower-tier bid ($c_\alpha \succeq
  c_\beta$), so "a full implementation would ... let a tier-$c$ bucket
  draw on asks from tier $c$ and above"
- Extend PR1's per-tier compatibility-graph construction, today an
  exact-string `C_level` match per `architecture.md`'s Weakness 2, to
  build each tier's bucket from bids at tier $c$ against asks at tier $c$
  and every tier above it, while keeping the existing single
  uniform-price-per-bucket clearing rule
- Unit tests: a bid at tier `cheap` is filled by an ask at tier
  `frontier` when no `cheap`-tier ask is available and the frontier
  seller's limit price clears the `cheap` bucket; a rational
  `frontier`-tier seller with a marginal cost above the `cheap` clearing
  price is not drawn into serving `cheap` demand
- Result: matched volume increases relative to PR1's exact-tier-only
  baseline without introducing a new price axis, closing
  `architecture.md`'s Weakness 2

#### PR6: [ ] Commit-reveal blind-bid auction simulation (exploratory)
- Exploratory/research PR, lighter bar than PR1-PR5: no real cryptography
  or on-chain settlement, tests cover protocol plumbing (commit is
  rejected without a later matching reveal, front-running is or is not
  blocked), not a security audit
- Background: `papers/Noesis/08_decentralized_extension.tex`'s blind-bid
  definition wraps a bid/ask in a commit-reveal scheme, commit a hash
  $h_\beta = H(\beta \,\|\, \nu_\beta)$ during a commit window, disclose
  $(\beta, \nu_\beta)$ during a reveal window, to prevent a party that
  sees a pending bid from front-running it (e.g., submitting a marginally
  better ask to snipe a favorable price)
- Wrap PR1's `OrderBook` with a commit window, in which bidders/askers
  post a hash commitment, followed by a reveal window, in which they
  disclose the order tuple and salt; only revealed orders matching a
  posted commitment are passed into `clear_round()`
- Unit tests: an order revealed without a matching prior commitment is
  rejected; a simulated "sniper" that observes revealed orders and
  submits a new order before the reveal window closes is measurably
  blocked when the reveal window is a single tick, and not blocked when
  it spans multiple ticks, reproducing the mempool-monitoring risk the
  paper flags as still open
- Result: a measured front-running-resistance comparison between the
  plain PR1 order book and commit-reveal; stake-backed slashing (the
  paper's staked-ask definition) and real on-chain deployment are out of
  scope for this PR

### Open questions
- Not blocking PR1 (covered by defaults above); must be resolved before
  PR2/PR3 lock in the real contract schema and before
  [[draft.Intelligence_Server]] replaces the PR2 mock
1. Task unit for cross-provider comparability: tokens vs. wall-clock
   compute vs. benchmark-normalized task-equivalent
2. Auction mechanism/frequency: uniform-price batch call auction vs.
   continuous double auction, and whether 5 min is the right cadence
3. Anti-gaming: how to stop capability misrepresentation or bid shading
   without a heavy onboarding/reputation system
4. Pricing denomination: real currency vs. synthetic task-credit;
   `NoesisPlatform` PR3 below resolves this operationally by supporting
   both a credit-card and a crypto funding rail rather than forcing a
   single choice at the protocol level
5. Batch vs. hybrid: does a spot market need to sit alongside the batch
   auction for latency-sensitive buyers
6. On-chain settlement and anonymity: are PR6's commit-reveal gas costs,
   redundancy defaults, and stake asymmetries (see
   `papers/Noesis/08_decentralized_extension.tex`) compatible with the
   auction frequency in open question 2

## NoesisServer

### Goal
- Build a lightweight LLM API gateway (modeled on OpenRouter) that proxies
  requests to multiple providers, logs every prompt/response pair, adds
  difficulty-aware routing, and serves as the fulfillment/monitoring layer
  for [[draft.Intelligence_Market]]
- Background/formalization: [[draft.Intelligence_Server]],
  `papers/Noesis/05_noesis_server.tex`

### Solution

#### PR1: [x] Minimal passthrough proxy with logging
- Support 2-3 providers behind one API
- Define the storage schema for prompt, response, and metadata (provider,
  model, latency, cost)
- Log raw, unscrubbed prompt/response pairs for now, scoped to
  synthetic/test traffic only; add PII scrubbing as a follow-up before any
  real non-synthetic traffic is logged (tracked as an open question below)
- Unit tests (per `testing.rules.md`): request routed to each configured
  provider is logged with correct schema and fields
- Result: every request/response pair is logged and queryable

#### PR2: [ ] Routing policy + cost/quality measurement
- Add a simple routing policy (e.g., a task classifier): route to a cheap
  or fast model vs. a stronger model
- Measure cost and quality against an always-call-the-strong-model
  baseline, using logged data from PR1
- Unit tests: routing policy selects the expected model per test-case
  classification; cost/quality metrics computed correctly on a fixture log
- Result: a measured cost/quality frontier for at least one routing policy

#### PR3: [ ] Difficulty estimator + distillation experiment (prototype)
- Exploratory/research PR, lighter bar than PR1/PR2: tests cover pipeline
  plumbing (data loads, estimator trains, metrics compute), not a model
  quality bar
- Train `q(prompt) -> required capability level` from logged agreement
  between cheap and strong models (PR2's routing data)
- Explore distilling a small model from the collected dataset
- Result: a difficulty-aware router with a measured saving, and a first
  distillation experiment with reported (not necessarily strong) results

#### PR4: [ ] Fulfillment monitoring wired to the market (stubbed both sides)
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

#### PR5: [ ] Answer fusion prototype
- Background: `papers/Noesis/05_noesis_server.tex`'s answer-fusion section
  describes fusion as the complementary lever to routing: instead of
  picking one tier per request, fan a request out to a set of providers
  $S(x)$ and combine their answers through an aggregator $g$ (majority
  vote, a verifier model, or a learned combiner); a high-`R_min` contract
  may only be economically served through fusion, while a low-price,
  low-`R_min` contract favors PR2's routing instead
- Extend the PR1 gateway's `Gateway.call()` with a `call_fused()` that
  dispatches the same prompt to every provider in `S(x)`, collects
  responses, and applies a pluggable aggregator (majority vote / exact
  match to start; a verifier-model or learned combiner deferred)
- Unit tests: the majority-vote aggregator picks the modal response on a
  fixture with a clear majority; ties are broken deterministically; cost
  accounting sums the cost of every fanned-out call, not just one
- Result: a working fan-out/fan-in path measured against a
  single-provider baseline on cost and on a simple correctness proxy
  (agreement with a fixed reference answer), giving a first cost/
  reliability trade-off for fusion, analogous to PR2's cost/quality
  frontier for routing

#### PR6: [ ] Statistical fulfillment violation test
- Background: `papers/Noesis/05_noesis_server.tex`'s fulfillment
  monitoring section notes that PR4's naive rule, flagging $\kappa$
  whenever `measured_reliability < R_min`, conflates genuine
  under-delivery with sampling noise on a small fulfillment window;
  the paper proposes a one-sided hypothesis test instead
- Replace PR4's threshold with a normal-approximation lower confidence
  bound $\hat r_{\text{lower}}(\kappa, W)$, computed from
  `measured_reliability` and the window size `|W|` at a configurable
  confidence level $1 - \delta$; flag $\kappa$ only when
  $\hat r_{\text{lower}}(\kappa, W) < R_{\min}(\kappa)$; fall back to an
  exact Clopper-Pearson interval when `|W|` is small
- Unit tests: a contract with a small window and a borderline sample
  reliability is NOT flagged when the confidence interval still clears
  `R_min` (a case that PR4's naive rule would have flagged as a false
  positive); a contract with a large window and the same sample
  reliability IS flagged
- Result: fewer false-positive violation reports feeding
  `NoesisMarket` PR3's reputation update, addressing the "attribution
  reliability" open question below

#### PR7: [ ] Real provider liquidity via an OpenRouter-backed `ProviderConfig`
- Background: `05_noesis_server.tex` models `NoesisServer` "on multi-provider
  routers such as OpenRouter" precisely because a router like OpenRouter
  already pools dozens of providers and models behind one API key,
  matching the paper's "provider-agnostic liquidity pooling" property
  (`01_introduction.tex`); PR1's `ProviderConfig.call_fn` today wraps only
  test stand-ins, so `Gateway` has no real liquidity yet
- Add an `OpenRouterProviderConfig` (or a `call_fn` factory) whose
  `call_fn` forwards `(model, prompt)` to OpenRouter's real chat-
  completions endpoint (`model` formatted as `"<upstream_provider>/
  <model>"`, e.g. `"openai/gpt-4o"`), parses the response back into the
  raw text `Gateway.call()` returns today, and replaces PR1's placeholder
  `cost_per_char` with the real per-token cost OpenRouter reports in
  `usage` (`architecture.md` Weakness 7)
- One registered `OpenRouterProviderConfig` covers every model OpenRouter
  lists (`GET /api/v1/models`), so `Gateway` gets real multi-provider
  liquidity from a single integration instead of one bespoke
  `ProviderConfig` per upstream provider
- Unit tests keep injecting a fixture `ProviderCallFn` per the existing
  convention (no live network call in the default suite); a
  `requires_openrouter_key`-marked integration test, skipped unless an API
  key is present in the environment, exercises one real OpenRouter call
- Result: `Gateway` is backed by real, multi-provider liquidity instead of
  test stand-ins; once wired to `NoesisMarket` (PR3/PR4 above), a cleared
  ask can be fulfilled by an actual OpenRouter call in place of
  `mock_fulfill()`

#### PR8: [ ] OpenRouter-compatible API interface for `NoesisServer`
- Background: `NoesisPlatform` PR1 sketches a bespoke HTTP wrapper around
  `Gateway.call()` without specifying its wire format; adopting
  OpenRouter's own REST contract instead means any existing OpenRouter
  client (SDK, LangChain provider config, curl script) can point its
  `base_url` at a `NoesisServer` deployment and work unmodified
- Add `POST /api/v1/chat/completions` matching OpenRouter's request shape
  (`model: "<provider>/<model>"`, `messages`, `stream`) and response shape
  (`id`, `choices[].message`, `usage.{prompt,completion,total}_tokens`),
  translating to/from `Gateway.call()`'s `(provider_name, model, prompt)`
  signature internally
- Add `GET /api/v1/models` mirroring OpenRouter's model-listing endpoint,
  sourced from `Gateway`'s registered `ProviderConfig`s (name and, once
  PR7 lands, a real per-token price instead of PR1's placeholder)
- Auth: `Authorization: Bearer <api_key>` header, OpenRouter's own
  convention, checked the same way as `NoesisPlatform` PR1's per-account
  API key
- Unit tests: a request built with an OpenRouter client's request shape
  round-trips through `Gateway.call()` and returns an OpenRouter-shaped
  response on a local test server; an unknown `model` string is rejected
  with OpenRouter's error-response shape, not a bare 500
- Result: `NoesisServer` is a drop-in replacement for OpenRouter from the
  caller's point of view; supersedes the wire format of `NoesisPlatform`
  PR1's passthrough-completion endpoint once this lands

### Open questions
- Not blocking PR1-PR6 as scoped above; track before broader rollout
1. Is a simple pass-through logger already useful for dataset building, or
   does routing quality matter for data diversity? (affects how much PR2
   matters before starting PR3's dataset use)
2. Can request difficulty be estimated cheaply enough that difficulty-aware
   routing nets a real cost saving? (PR3's core research question)
3. Routing vs. fusion under a fixed budget: for a fixed per-request
   budget, is it better to route to one well-chosen model (PR2) or to
   query several cheaper models and combine their answers (PR5)? PR5
   above turns this question into a measurable comparison rather than
   leaving it open
4. **PII/data-handling safeguards** before logging real (non-synthetic)
   prompt/response pairs — PR1 defers scrubbing and stays on
   synthetic/test traffic only until this is resolved; must be answered
   before enabling real traffic logging
5. Can a distilled model match routed "best model per task" quality at a
   fraction of the cost? (PR3's distillation sub-question)
6. Attribution reliability: how reliably can the server attribute a
   quality/latency shortfall to a specific provider vs. noise, so
   fulfillment reporting to [[draft.Intelligence_Market]] is trustworthy
   enough to affect pricing? PR6 above answers the noise-vs-signal half of
   this question; attributing a confirmed shortfall to the right provider
   among several serving the same contract remains open
7. OpenRouter dependency risk: PR7 makes `Gateway`'s real liquidity depend
   on one third party's uptime, pricing, and model catalog; is a single-
   upstream dependency acceptable for the prototype, or does it need a
   fallback provider before real (non-synthetic) traffic relies on it?
8. Fidelity vs. scope of PR8's compatibility: targeting chat completions
   and model listing only; does divergence from OpenRouter's exact error
   codes/streaming semantics break real OpenRouter clients in practice,
   before advertising `NoesisServer` as a drop-in replacement?

## NoesisPlatform

### Goal
- Turn the `NoesisMarket`/`NoesisServer` prototypes into a service an
  external caller can actually reach: a public API over both components,
  a cloud deployment target, and a way for a buyer to fund an account with
  a credit card or crypto before bidding
- Unlike `NoesisMarket` and `NoesisServer`, this section is not grounded in
  a specific mechanism from `papers/Noesis/*.tex`; it is the productization
  layer both component plans assume but neither scopes (`architecture.md`
  notes "there is no CLI or script entry point yet")
- Background: `NoesisMarket`'s pricing-denomination open question (real
  currency vs. synthetic task-credit) and `08_decentralized_extension.tex`'s
  staked-ask escrow design, for the crypto funding rail in PR3

### Solution

#### PR1: [x] Public API surface for NoesisMarket and NoesisServer
- Background: PR1-PR6 of `NoesisMarket` and `NoesisServer` expose Python
  library calls only (`OrderBook.submit_bid()`, `Gateway.call()`, etc.); an
  external caller cannot reach either component today
- Wrap the existing modules behind a thin HTTP API (e.g., FastAPI):
  - `NoesisMarket`: `POST /bids`, `POST /asks`, `GET /contracts/{id}`,
    `GET /rounds/{tier}/latest` (`NoesisMarket` PR4's pricing-dissemination
    feed)
  - `NoesisServer`: a passthrough completion endpoint wrapping
    `Gateway.call()`, `GET /logs`
  - Auth: a per-account API key, checked before accepting a bid/ask or a
    gateway call
- Unit tests: each endpoint round-trips to the underlying library call with
  the same validation (`hdbg.dassert_*`) surfaced as an HTTP 4xx, not a
  stack trace; a request with a missing/invalid API key is rejected before
  reaching the underlying call
- Result: `NoesisMarket` and `NoesisServer` are callable over HTTP by an
  external client, not just from within the same Python process
- Implementation note (`research/Noesis/platform_api.py`): added an
  unauthenticated `POST /rounds/clear` beyond the list above, since
  `OrderBook.clear_round()` is the only thing that produces a
  `Contract`/`TierClearResult` and none of the listed endpoints call it;
  without it, `GET /contracts/{id}` and `GET /rounds/{tier}/latest` could
  never be populated by an external caller. `GET /rounds/{tier}/latest`
  reads from an in-process per-tier cache populated by `POST
  /rounds/clear`, standing in for PR4's pub/sub feed until PR4 lands.

#### PR2: [ ] Cloud deployment
- Containerize PR1's API into a single Docker image, following this repo's
  existing Docker template conventions (`class_project/project_template/Dockerfile*`)
- Deploy to a cloud target (a single-node container service, e.g. AWS ECS,
  Fly.io, or Render, to start; Kubernetes deferred until there is more than
  one process to orchestrate)
- Externalize the in-memory state PR1-PR6 of `NoesisMarket`/`NoesisServer`
  assume (order book, contract log, request log) to a real datastore (e.g.
  Postgres or Redis): a cloud deployment cannot rely on a single
  long-lived process the way the current test suites do
- Unit tests: a smoke test that boots the container and round-trips one
  bid/ask pair through the deployed API image locally (`docker run` + one
  HTTP call), not a real cloud test
- Result: a `NoesisMarket`/`NoesisServer` instance reachable at a public
  URL, backed by persistent storage instead of the current in-process
  `List`/`Dict` state (`architecture.md` Weakness 6)

#### PR3: [ ] Buying credits (credit card and crypto)
- Background: resolves `NoesisMarket` open question 4 (pricing
  denomination) operationally, by supporting both a real-currency and a
  crypto funding rail instead of forcing a single choice
- Add a funding flow so a buyer can pre-purchase task-credit before
  submitting a bid:
  - Credit card: a hosted checkout (e.g. Stripe Checkout) that credits the
    buyer's account balance on a successful payment webhook
  - Crypto: a deposit address per account, or the escrow contract sketched
    in `08_decentralized_extension.tex`'s staked-ask design, that credits
    the account once a deposit transaction confirms
- Gate `POST /bids` (PR1) on `account_balance >= n_beta * p_beta`, debiting
  the balance only once a bid is matched into a contract
  (Definition~contract), not at submission time
- Unit tests: a mocked card-webhook credits the right account for the right
  amount and is idempotent on webhook retry; a mocked on-chain deposit
  event credits the account once, not once per confirmation; a bid
  exceeding the account's balance is rejected before reaching the auction
- Result: a buyer can fund an account through either rail and see the
  balance gate bid submission

### Open questions
1. Custody: does `NoesisMarket` hold buyer funds in escrow between funding
   and settlement, or only check a balance and settle out-of-band? (affects
   PR3's debit timing and regulatory exposure)
2. Refunds and chargebacks: how does a credit-card chargeback interact with
   credit already spent on a matched contract?
3. Cloud target for PR2: which provider to standardize on, and whether the
   in-memory-to-datastore migration should land before or after the first
   public deployment
4. KYC/compliance: does accepting real-currency payments (credit card or
   crypto) trigger money-transmitter obligations that a synthetic
   task-credit avoids? (sharpens `NoesisMarket` open question 4)

## Conventions
- Code: `.claude/skills/coding.rules.md`
- Tests: `.claude/skills/testing.rules.md`

## References
- Background/formalization: [[draft.Intelligence_Market]],
  [[draft.Intelligence_Server]]
- The full \Noesis{} paper: `papers/Noesis/paper.tex` (sections
  `01_introduction.tex` through `11_conclusion.tex`)
- OpenRouter: unified API for multiple LLM providers; design reference for
  `NoesisServer` PR1, and the real integration target for `NoesisServer`
  PR7 (backend liquidity) and PR8 (compatible API interface)
- Stripe Checkout: hosted credit-card payment flow (reference only, for
  `NoesisPlatform` PR3)
- Chen, L., et al., _FrugalGPT: How to Use Large Language Models While
  Reducing Cost and Improving Performance_. (2023)
- Ong, I., et al., _RouteLLM: Learning to Route LLMs with Preference Data_.
  (2024)
