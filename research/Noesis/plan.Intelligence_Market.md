# Intelligence Market

## Goal
- Build a minimal working intelligence market: a batch call-auction that
  matches buyer/seller contracts for LLM inference bundling capability
  tier, latency, and reliability guarantees, dispatches cleared contracts
  for fulfillment, and feeds delivery performance back into pricing
- Background/formalization: [[draft.Intelligence_Market]]

## Solution

### PR1: [x] Minimal batch call-auction simulator
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

### PR2: [ ] Contract schema + dispatch to a stubbed fulfillment layer
- Define the contract schema `(N_tasks, C_level, L_max, R_min, P)` from a
  cleared PR1 match
- Dispatch each cleared contract to a **mock** fulfillment interface
  (fixed or randomized pass/fail outcomes), standing in for
  [[draft.Intelligence_Server]], which has no implementation yet
- Log the (mocked) fulfillment result back onto the contract record
- Result: closed loop match → contract → dispatch → logged outcome, mocked
  past the auction boundary; swap-in point for the real
  [[draft.Intelligence_Server]] once it exists

### PR3: [ ] Reputation and pricing feedback loop
- Feed logged fulfillment outcomes (from PR2, mocked or real) into
  per-seller eligibility and a pricing adjustment for future auction
  rounds
- Sellers whose measured reliability drops below `R_min` on repeated
  contracts are priced out or excluded from subsequent rounds
- Result: sellers that under-deliver lose eligibility/priority in later
  auctions

## Open questions
- Not blocking PR1 (covered by defaults above); must be resolved before
  PR2/PR3 lock in the real contract schema and before
  [[draft.Intelligence_Server]] replaces the PR2 mock
1. Task unit for cross-provider comparability: tokens vs. wall-clock
   compute vs. benchmark-normalized task-equivalent
2. Auction mechanism/frequency: uniform-price batch call auction vs.
   continuous double auction, and whether 5 min is the right cadence
3. Anti-gaming: how to stop capability misrepresentation or bid shading
   without a heavy onboarding/reputation system
4. Pricing denomination: real currency vs. synthetic task-credit
5. Batch vs. hybrid: does a spot market need to sit alongside the batch
   auction for latency-sensitive buyers

## Conventions
- Code: `.claude/skills/coding.rules.md`
- Tests: `.claude/skills/testing.rules.md`

## References
- Background/formalization: [[draft.Intelligence_Market]]
- Fulfillment layer (not yet implemented): [[draft.Intelligence_Server]]
