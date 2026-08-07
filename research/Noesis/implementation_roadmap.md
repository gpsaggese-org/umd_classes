# Implementation roadmap

The implementation plans in the underlying design notes for NoesisMarket and
NoesisServer were written independently. This section merges them into a
single sequence in which each milestone is a result that can be demonstrated
on its own, and later milestones wire earlier ones together into the closed
loop described in the Noesis protocol overview.

- **Milestone 1: a minimal batch call-auction simulator.** An in-memory
  order book with bid/ask submission and per-tier uniform-price clearing,
  implementing the clearing problem for the complete-compatibility-graph
  case of the existence-of-a-clearing-price proposition. Result: a
  unit-tested auction that clears correctly on synthetic order books, with
  no real settlement.

- **Milestone 2: a minimal passthrough proxy with logging.** A gateway
  supporting two or three providers behind one API, implementing the
  logging schema of the gateway architecture. Result: every
  request/response pair is logged and queryable, independent of
  Milestone 1.

- **Milestone 3: contract schema and dispatch integration.** Wire
  Milestone 1's cleared bids to Milestone 2's proxy: define the contract
  schema in code, and hand off a cleared contract from NoesisMarket to
  NoesisServer for execution. Result: a closed loop in which a matched
  contract is dispatched and executed, though not yet monitored for
  fulfillment.

- **Milestone 4: a routing experiment.** Add a simple routing policy
  (e.g., a task classifier standing in for the difficulty estimator
  $\hat d$) to the proxy from Milestone 2, and measure cost against
  quality relative to always calling the strongest model. Result: a
  measured cost/quality frontier for at least one routing policy.

- **Milestone 5: fulfillment monitoring and the reputation feedback
  loop.** Implement the measured-reliability computation and the
  reliability lower-bound violation test in NoesisServer, and the
  reputation update in NoesisMarket. Result: a contract dispatched under
  Milestone 3 has its fulfillment measured, and a seller that
  under-delivers is priced out or excluded from subsequent rounds.

- **Milestone 6: a difficulty estimator and a first distillation
  experiment.** Train the difficulty estimator $\hat d$ from the logged
  agreement label, evaluate the routing saving condition on real traffic,
  and run a first distillation experiment on the logged corpus (training
  signal and distillation). Result: a difficulty-aware router with a
  measured saving, and a first distilled model.

- **Milestone 7: the full closed loop.** With Milestones 1 through 6 in
  place, run NoesisMarket and NoesisServer together end to end: bids and
  asks clear into contracts, contracts are executed and monitored,
  fulfillment results feed back into pricing and eligibility, and routing
  and fusion decisions are informed by the accumulating logged corpus.
  Result: a working prototype exercising every mechanism described in the
  NoesisMarket and NoesisServer sections.

Each milestone is scoped to be independently demonstrable within one to two
days of focused work, consistent with the goal of showing progress
incrementally rather than attempting the full closed loop in one step.
