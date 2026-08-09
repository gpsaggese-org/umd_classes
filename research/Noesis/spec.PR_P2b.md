# `PR_P2b`: Use Postgres Backend - Implementation Spec

- This document specifies the Python code, schema, and Docker changes needed to
  implement `PR_P2b` from `research/Noesis/plan.Noesis.md`
- Scope, as stated in the plan:
  - Externalize the in-memory state of `NoesisMarket` and `NoesisServer` (order
    book, contract log, request log) to a real datastore (e.g. Postgres or Redis)
  - Result: a `NoesisMarket`/`NoesisServer` instance backed by persistent storage
    instead of the current in-process `List`/`Dict` state
- This is a specification only: no code in this document has been implemented; it
  describes what `PR_P2b` needs to add on top of the current `research/Noesis/*.py`
  code
- Roadmap position: `PR_P2b` is not listed under any `v0.x` roadmap bullet in
  `plan.Noesis.md`; it is sequenced directly after `PR_P2` (Cloud Deployment) in
  the `NoesisPlatform` PR list, and its own `TODO(gp)` note points at how to
  "inject a Postgres instance in the container", i.e. `PR_P2`'s Docker/devops
  scaffold. This spec therefore assumes `PR_P2` lands first and describes its own
  Docker/config deltas on top of `spec.PR_P2.md`'s design (`main.py`, `devops/`,
  `docker-compose.noesis.yml`, `GET /health`) rather than on top of the code
  actually on disk today, since `spec.PR_P2.md` is itself still a specification
  only, per its own header, not implemented code

## Design Decision: Postgres via `helpers.hsql`, Not Redis or an ORM
- The plan says "e.g. Postgres or Redis"; this PR's own title ("Use Postgres
  Backend") already picks Postgres, and this repo ships a first-class Postgres
  client already used across the wider Causify ecosystem this repo's dev-system
  is modeled on:
  - `helpers.hsql` / `helpers.hsql_implementation` (`psycopg2`-based, function
    style: `get_connection_from_env_vars()`, `wait_db_connection()`,
    `execute_query_to_df()`, `execute_insert_query()`, etc.), gated so importing
    `helpers.hsql` does not require `psycopg2` unless it is actually installed
    (`hsql.py`'s `hmodule.has_module("psycopg2")` check)
  - `helpers.hsql_test.TestDbHelper` / `TestImOmsDbHelper`: a test harness that
    spins up an ephemeral Postgres via `docker-compose` for tests that need a
    real DB (see "Unit Tests" below)
  - A concrete precedent for wiring a Postgres-backed service into this
    ecosystem's `invoke`/Docker flow: `datapull/im_lib_tasks.py` (per-stage env
    file at `devops/env/{stage}.im_db_config.env`, an `im_postgres`
    `docker-compose` service, `im_docker_up`/`im_docker_down` invoke tasks)
  - No comparable Redis client/test-harness module exists anywhere in
    `helpers_root`
- No new ORM (SQLAlchemy, etc.) is introduced: `helpers.hsql_implementation`'s
  functions operate on `pandas.DataFrame`s and raw SQL strings, not mapped
  classes, which is a smaller diff on top of this codebase's existing plain
  dataclasses (`Bid`, `Ask`, `Contract`, `RequestLogEntry`) than introducing a
  second object-mapping layer on top of them

## Out of Scope
- Redis as an alternative backend: this spec picks Postgres per the PR's own
  title (see "Design Decision" above)
- A schema migration/versioning framework (e.g. Alembic): `init_schema()`'s
  `CREATE TABLE IF NOT EXISTS` DDL (below) is enough for this prototype's first
  schema; a real migration tool is a follow-up if the schema changes later
- Connection pooling: one shared `psycopg2` connection per process, matching how
  `main.py` already builds one process-lifetime `OrderBook`/`Gateway` singleton
  (`spec.PR_P2.md`); revisit if load testing shows a single connection is a
  bottleneck
- Provisioning a managed Postgres instance (e.g. AWS RDS) for the `PR_P2`
  ECS deployment path: one-time AWS infra setup, out of scope for this PR's
  Python/schema code, same caveat `spec.PR_P2.md`'s "Cloud Target" section
  raises for the ECS cluster itself
- Any change to the matching algorithm, contract schema shape, or HTTP surface:
  this PR only changes *where* state lives, not what the state means or how
  `_match_orders_in_tier()` clears a tier
- `PR_M8`'s real fulfillment wiring: dispatch still calls `mock_fulfill()`;
  persisting a `Contract.fulfilled` value does not make the value itself real
- A `/ready` endpoint distinct from `PR_P2`'s `GET /health`: this PR keeps
  `/health` DB-agnostic (a liveness check, not a readiness check per "Risks"
  below), since adding a DB-probing endpoint is an orthogonal concern `PR_P2`
  did not scope either

## Current State (What This PR Builds On)
- Three separate in-memory state surfaces, matching the plan's "order book,
  contract log, request log" list exactly, all lost on process exit
  (`architecture.md` Weakness 6):
  - `batch_call_auction.OrderBook.__init__` (`batch_call_auction.py:317-319`):
    `self._bids: List[Bid] = []` / `self._asks: List[Ask] = []`, appended to by
    `submit_bid()`/`submit_ask()` and unconditionally emptied by
    `clear_round()` (`batch_call_auction.py:371-373`)
  - `platform_api._MarketState.__init__` (`platform_api.py:206-211`):
    `self._contracts_by_id: Dict[int, Contract] = {}`,
    `self._next_contract_id = 0`,
    `self._latest_round_by_tier: Dict[str, RoundClearResponse] = {}`,
    `self._next_round_id = 0`; this is the "contract log" plus the per-tier
    "latest cleared round" cache standing in for `NoesisMarket`'s pricing feed
    (`PR_M4`, not implemented yet)
  - `passthrough_proxy.Gateway.__init__` (`passthrough_proxy.py:128-130`):
    `self._log: List[RequestLogEntry] = []`, `self._next_request_id = 0`
- All three ids (`contract_id`, `round_id`, `request_id`) are assigned by a
  plain Python counter starting at `0` on every process start; a naive
  persistence layer that keeps these counters as-is would start reassigning
  colliding ids after every restart, silently corrupting the very persistence
  this PR is meant to add (see "Risks" below)
- No Postgres/SQL dependency anywhere in `research/Noesis` today: `helpers.hsql`
  is available repo-wide but unused by any of the four existing modules

## Storage Abstraction
- Follows this codebase's existing dependency-injection idiom
  (`architecture.md`'s "Key design decisions": "every side effect that would be
  non-deterministic in a test ... is injected as a callable"), extended from
  injected *callables* (`FulfillmentFn`, `ProviderCallFn`) to injected *storage
  objects*: one small `abc.ABC` per state surface, colocated with the class
  that owns it, plus an `_InMemory*Store` default that is today's plain
  `List`/`Dict` code extracted unchanged, so every existing test keeps passing
  with no behavior change
- A new module, `research/Noesis/postgres_store.py` (import alias `rnpost`),
  holds only the Postgres-specific pieces: the schema DDL, `init_schema()`, and
  one `Postgres*Store` class per `ABC`. It imports the three owning modules to
  implement their `ABC`s; none of the three owning modules import it, so there
  is no import cycle and no new dependency on `psycopg2` for a caller that
  never touches the Postgres backend (matches `helpers.hsql`'s own optional-import
  gating)

### `batch_call_auction.py`: `OrderBookStore`
```python
import abc

class OrderBookStore(abc.ABC):
    """
    Pluggable storage backend for `OrderBook`'s pending `Bid`/`Ask` queues.
    """

    @abc.abstractmethod
    def add_bid(self, bid: Bid) -> None:
        ...

    @abc.abstractmethod
    def add_ask(self, ask: Ask) -> None:
        ...

    @abc.abstractmethod
    def get_bids(self) -> List[Bid]:
        """
        :return: pending bids, in submission order
        """
        ...

    @abc.abstractmethod
    def get_asks(self) -> List[Ask]:
        """
        :return: pending asks, in submission order
        """
        ...

    @abc.abstractmethod
    def clear(self) -> None:
        """
        Drop every stored bid/ask (`OrderBook.clear_round()`'s existing
        drop-everything semantics; see `architecture.md` Weakness 4).
        """
        ...


class _InMemoryOrderBookStore(OrderBookStore):
    """
    Default `OrderBookStore`: today's plain `List[Bid]`/`List[Ask]`, extracted
    unchanged.
    """
    # `add_bid()`/`add_ask()`/`get_bids()`/`get_asks()`/`clear()` reproduce
    # exactly what `OrderBook.submit_bid()`/`submit_ask()`/
    # `get_pending_bids()`/`get_pending_asks()`/`clear_round()`'s
    # `self._bids = []` do today.
```
- `OrderBook.__init__(self, *, store: Optional[OrderBookStore] = None)`: `if
  store is None: store = _InMemoryOrderBookStore()`. The `Optional[...] = None`
  default here is a deliberate exception to
  `.claude/skills/coding.rules.md`'s "Minimize Default Values of None": a
  stateful default (`store: OrderBookStore = _InMemoryOrderBookStore()`) would
  create **one** store instance at function-definition time, shared and
  mutated by every `OrderBook()` call, exactly the mutable-default-argument
  pitfall `contract_dispatch.mock_fulfill()`'s existing `rng: Optional[
  random.Random] = None` parameter already works around the same way in this
  codebase
- `submit_bid()`/`submit_ask()`/`get_pending_bids()`/`get_pending_asks()`
  become one-line delegations to `self._store.add_bid()` /
  `self._store.get_bids()` / etc.
- `clear_round()` changes minimally: replace `self._bids`/`self._asks` reads
  with `self._store.get_bids()`/`get_asks()`, and the trailing `self._bids =
  []; self._asks = []` with `self._store.clear()`; `_match_orders_in_tier()`
  itself (the pure matching algorithm) is untouched

### `platform_api.py`: `ContractStore`
```python
class ContractStore(abc.ABC):
    """
    Pluggable storage backend for `_MarketState`'s contract log and per-tier
    "latest cleared round" cache.
    """

    @abc.abstractmethod
    def save_contract(self, contract: rnocodis.Contract) -> int:
        """
        :return: the `contract_id` assigned to `contract`
        """
        ...

    @abc.abstractmethod
    def get_contract(self, contract_id: int) -> rnocodis.Contract:
        ...

    @abc.abstractmethod
    def next_round_id(self) -> int:
        """
        Assign one new `round_id`, shared by every tier cleared in the same
        `clear_round()` call (see the note on `round_id` below).
        """
        ...

    @abc.abstractmethod
    def save_round(self, round_response: RoundClearResponse) -> None:
        ...

    @abc.abstractmethod
    def get_latest_round(self, tier: str) -> RoundClearResponse:
        ...


class _InMemoryContractStore(ContractStore):
    """
    Default `ContractStore`: today's `_contracts_by_id`/`_next_contract_id`/
    `_latest_round_by_tier`/`_next_round_id`, extracted unchanged.
    """
```
- `_MarketState.__init__(self, order_book, *, fulfillment_fn=..., store:
  Optional[ContractStore] = None)`: same `None`-default rationale as
  `OrderBook.store` above
- `clear_round()` changes: `round_id = self._next_round_id; self.
  _next_round_id += 1` becomes `round_id = self._store.next_round_id()`
  (called once, before the per-tier loop, exactly where today's counter
  increment happens); the per-contract `self._contracts_by_id[self.
  _next_contract_id] = contract; self._next_contract_id += 1` loop becomes
  `contract_id = self._store.save_contract(contract)` (the store assigns the
  id); `self._latest_round_by_tier[c_level] = round_response` becomes `self.
  _store.save_round(round_response)`
- `get_contract()`/`get_latest_round()` delegate to `self._store.get_contract()`
  /`get_latest_round()`, raising the same `hdbg.dassert_in(...)`-driven
  `AssertionError` on an unknown id/tier as today (the `_InMemoryContractStore`
  keeps the existing `hdbg.dassert_in` checks; `PostgresContractStore` raises
  the same way on an empty query result, see below)
- `create_app()`'s signature grows one new keyword parameter,
  `contract_store: Optional[ContractStore] = None`, threaded through to `
  _MarketState(order_book, fulfillment_fn=fulfillment_fn, store=contract_store)`
  so `main.py` (below) can inject `PostgresContractStore` without `_MarketState`
  needing to be constructed outside `create_app()`

### `passthrough_proxy.py`: `RequestLogStore`
```python
class RequestLogStore(abc.ABC):
    """
    Pluggable storage backend for `Gateway`'s request/response log.
    """

    @abc.abstractmethod
    def append(
        self,
        provider: str,
        model: str,
        prompt: str,
        response: str,
        latency_in_secs: float,
        cost: float,
    ) -> RequestLogEntry:
        """
        Persist one logged request/response pair.

        :return: the persisted `RequestLogEntry`, with `request_id` assigned
            by the store
        """
        ...

    @abc.abstractmethod
    def get_all(self) -> List[RequestLogEntry]:
        """
        :return: every logged entry, in call order
        """
        ...

    @abc.abstractmethod
    def query(
        self, *, provider: str = "", model: str = ""
    ) -> List[RequestLogEntry]:
        ...


class _InMemoryRequestLogStore(RequestLogStore):
    """
    Default `RequestLogStore`: today's `_log`/`_next_request_id`, extracted
    unchanged; `append()` builds the same `RequestLogEntry` `Gateway.call()`
    builds today and keeps its own counter.
    """
```
- `Gateway.__init__(self, *, clock_fn=time.perf_counter, store: Optional[
  RequestLogStore] = None)`: same `None`-default rationale as above
- `call()` changes: the `entry = RequestLogEntry(self._next_request_id, ...);
  self._next_request_id += 1; self._log.append(entry)` block becomes `entry =
  self._store.append(provider_name, model, prompt, response, latency_in_secs,
  cost)`
- `get_log()`/`query_log()` delegate to `self._store.get_all()`/`query(
  provider=provider, model=model)`

## Schema
- One new module, `research/Noesis/postgres_store.py`, owns the DDL, run by
  `init_schema(connection)` (idempotent: every statement is `CREATE TABLE IF
  NOT EXISTS`, safe to call on every `main.py` startup, no migration framework
  needed for this prototype's first schema per "Out of Scope" above)
- `noesis_` prefix on every table, since this may run against a shared Postgres
  instance alongside other projects' tables (matches the `im_postgres_db_local`
  style naming already used elsewhere in this ecosystem)
```sql
CREATE TABLE IF NOT EXISTS noesis_bids (
    id BIGSERIAL PRIMARY KEY,
    buyer_id TEXT NOT NULL,
    n_tasks INTEGER NOT NULL,
    c_level_min TEXT NOT NULL,
    l_max DOUBLE PRECISION NOT NULL,
    r_min DOUBLE PRECISION NOT NULL,
    p_max DOUBLE PRECISION NOT NULL
);

CREATE TABLE IF NOT EXISTS noesis_asks (
    id BIGSERIAL PRIMARY KEY,
    seller_id TEXT NOT NULL,
    n_tasks INTEGER NOT NULL,
    c_level TEXT NOT NULL,
    l_typical DOUBLE PRECISION NOT NULL,
    r_typical DOUBLE PRECISION NOT NULL,
    p_min DOUBLE PRECISION NOT NULL
);

CREATE TABLE IF NOT EXISTS noesis_contracts (
    contract_id BIGSERIAL PRIMARY KEY,
    buyer_id TEXT NOT NULL,
    seller_id TEXT NOT NULL,
    n_tasks INTEGER NOT NULL,
    c_level TEXT NOT NULL,
    l_max DOUBLE PRECISION NOT NULL,
    r_min DOUBLE PRECISION NOT NULL,
    price DOUBLE PRECISION NOT NULL,
    fulfilled BOOLEAN
);

-- `round_id` is NOT `SERIAL` on this table: one `clear_round()` call clears
-- every tier under the SAME round_id (see `next_round_id()` below), so the id
-- is generated once per round, not once per row.
CREATE SEQUENCE IF NOT EXISTS noesis_round_id_seq;

CREATE TABLE IF NOT EXISTS noesis_tier_rounds (
    tier TEXT NOT NULL,
    round_id BIGINT NOT NULL,
    clearing_price DOUBLE PRECISION,
    matched_volume INTEGER NOT NULL,
    cleared_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    PRIMARY KEY (tier, round_id)
);

CREATE TABLE IF NOT EXISTS noesis_request_log (
    request_id BIGSERIAL PRIMARY KEY,
    provider TEXT NOT NULL,
    model TEXT NOT NULL,
    prompt TEXT NOT NULL,
    response TEXT NOT NULL,
    latency_in_secs DOUBLE PRECISION NOT NULL,
    cost DOUBLE PRECISION NOT NULL
);
```
- `contract_id`/`request_id` are `BIGSERIAL` (one id per row, matching today's
  1:1 counter-per-record); `round_id` is a separate `noesis_round_id_seq`,
  fetched once per `clear_round()` call via `next_round_id()` (`SELECT
  nextval('noesis_round_id_seq')`) and reused for every tier's row in that
  round, replicating `platform_api.py:238-239`'s current
  "`round_id` assigned once, before the per-tier loop" behavior exactly

## New Python Code

### `research/Noesis/postgres_store.py` (new)
- Module docstring: points back to this file (`spec.PR_P2b.md`) and to the
  three `ABC`s it implements
- `init_schema(connection: hsql.DbConnection) -> None`: runs the DDL above via
  `connection.cursor().execute(...)`, one statement at a time, then `connection.
  commit()` (or relies on the `autocommit=True` connections `hsql.
  get_connection*()` already returns by default)
- `PostgresOrderBookStore(connection)`:
  - `add_bid(bid)` / `add_ask(ask)`: `hsqlimpl.execute_insert_query(connection,
    pd.DataFrame([dataclasses.asdict(bid)]), "noesis_bids")` (and the `asks`
    equivalent); `execute_insert_query()` is a bulk-row helper built on
    `psycopg2.extras.execute_values`, which fits a single-row insert fine and
    needs no `RETURNING` here since bid/ask ids are never read back
  - `get_bids()` / `get_asks()`: `hsqlimpl.execute_query_to_df(connection,
    "SELECT buyer_id, n_tasks, c_level_min, l_max, r_min, p_max FROM
    noesis_bids ORDER BY id")`, then one `Bid(**row)` per DataFrame row.
    **The `ORDER BY id` is required, not cosmetic**: `_match_orders_in_tier()`'s
    docstring states "`sorted()` is stable, so ties fall back to submission
    order" — without an explicit `ORDER BY`, Postgres does not guarantee row
    order, which would make tie-breaking within a price-tied tier
    nondeterministic and silently diverge from `_InMemoryOrderBookStore`'s
    list-append order
  - `clear()`: `DELETE FROM noesis_bids; DELETE FROM noesis_asks;` (matches
    `OrderBook.clear_round()`'s "drop everything" semantics exactly; a
    `TRUNCATE` would work too but `DELETE` keeps the `BIGSERIAL` sequence
    monotonically increasing across rounds, which is harmless here since bid/ask
    ids are never surfaced)
- `PostgresContractStore(connection)`:
  - `save_contract(contract)`: a raw `cursor.execute("INSERT INTO
    noesis_contracts(...) VALUES (...) RETURNING contract_id", (...)); return
    cursor.fetchone()[0]`, **not** `hsqlimpl.execute_insert_query()`, since that
    helper is a bulk multi-row insert built on `execute_values()` with no
    `RETURNING` support, and this call specifically needs the generated
    `contract_id` back
  - `get_contract(contract_id)`: `hsqlimpl.execute_query_to_df(connection,
    f"SELECT ... FROM noesis_contracts WHERE contract_id = {contract_id}")`;
    `hdbg.dassert_lt(0, len(df), "Unknown contract_id '%s'", contract_id)` (same
    "unknown id" contract `_MarketState.get_contract()` already documents,
    still surfaced as an HTTP 400 by `platform_api.py`'s existing
    `AssertionError` handler) then `Contract(**df.iloc[0].to_dict())`
  - `next_round_id()`: `cursor.execute("SELECT nextval('noesis_round_id_seq')")
    ; return cursor.fetchone()[0]`
  - `save_round(round_response)`: raw insert into `noesis_tier_rounds` (needs
    no `RETURNING`; `round_id` is already known from `next_round_id()`)
  - `get_latest_round(tier)`: `SELECT ... FROM noesis_tier_rounds WHERE tier =
    %s ORDER BY round_id DESC LIMIT 1`, `hdbg.dassert_lt(0, len(df), "No
    cleared round yet for tier '%s'", tier)`, matching `_MarketState.
    get_latest_round()`'s existing assertion
- `PostgresRequestLogStore(connection)`:
  - `append(...)`: raw `INSERT INTO noesis_request_log(...) VALUES (...)
    RETURNING request_id`, same `RETURNING`-needs-raw-SQL reasoning as
    `save_contract()`; builds and returns the `RequestLogEntry` with the
    returned id
  - `get_all()`: `SELECT ... FROM noesis_request_log ORDER BY request_id` (the
    same "in call order" invariant as `get_bids()`/`get_asks()` above, and for
    the same reason: `Gateway.get_log()`'s docstring promises call order)
  - `query(provider="", model="")`: builds the `WHERE` clause conditionally
    (skip a clause for each empty filter), matching `Gateway.query_log()`'s
    existing semantics exactly, still `ORDER BY request_id`

### `research/Noesis/main.py` (extends `PR_P2`'s spec)
- New env var `NOESIS_DB_BACKEND` (`os.environ.get("NOESIS_DB_BACKEND",
  "memory")`): `"memory"` (default, today's behavior, no Postgres dependency)
  or `"postgres"`
- When `"postgres"`:
  - Read the same five `POSTGRES_HOST`/`POSTGRES_DB`/`POSTGRES_PORT`/
    `POSTGRES_USER`/`POSTGRES_PASSWORD` env vars `hsql_implementation.
    get_connection_from_env_vars()` already expects (fixed names, not
    `research/Noesis`-specific, since they come from the official Postgres
    Docker image's own env var convention that `hsql_implementation.
    get_connection_info_from_env_file()`'s comment already cites)
  - `hsqlimpl.wait_db_connection(host, dbname, port, user, password)` before
    proceeding, so `main.py` fails fast with a clear timeout instead of the
    first request hitting a connection error if the `noesis_postgres` container
    is still starting
  - `connection = hsqlimpl.get_connection_from_env_vars()`
  - `rnpost.init_schema(connection)`
  - `order_book = rnbacaau.OrderBook(store=rnpost.PostgresOrderBookStore(
    connection))`
  - `gateway = rnopapro.Gateway(store=rnpost.PostgresRequestLogStore(
    connection))`
  - `contract_store = rnpost.PostgresContractStore(connection)`
- When `"memory"` (default): `order_book = rnbacaau.OrderBook()`, `gateway =
  rnopapro.Gateway()`, `contract_store = None` — byte-for-byte `PR_P2`'s
  existing spec, unchanged
- `app = rnoplapi.create_app(order_book, gateway, api_keys, contract_store=
  contract_store)`
- `_LOG.info("NOESIS_DB_BACKEND=%s", _DB_BACKEND)` at startup, so a deployment's
  logs make the active backend obvious without inspecting env vars directly

## Docker
- Extends `spec.PR_P2.md`'s `research/Noesis/devops/compose/
  docker-compose.noesis.yml` with one new service and one new volume, modeled
  on `datapull/im_lib_tasks.py`'s `im_postgres` service and the ecosystem's
  standard `postgres:<version>` image usage
  (`helpers_root/dev_scripts_helpers/update_devops_packages/test/db_example/
  docker-compose.yml`):
  ```yaml
  services:
    noesis_api:
      # ... existing PR_P2 fields (extends, command, ports) ...
      environment:
        - POSTGRES_HOST=noesis_postgres
        - POSTGRES_DB=${POSTGRES_DB}
        - POSTGRES_PORT=5432
        - POSTGRES_USER=${POSTGRES_USER}
        - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
        - NOESIS_DB_BACKEND=${NOESIS_DB_BACKEND}
      depends_on:
        noesis_postgres:
          condition: service_healthy

    noesis_postgres:
      image: postgres:16
      restart: "no"
      environment:
        - POSTGRES_DB=${POSTGRES_DB}
        - POSTGRES_USER=${POSTGRES_USER}
        - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
      volumes:
        - noesis_postgres_data:/var/lib/postgresql/data
      healthcheck:
        test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER}"]
        interval: 5s
        timeout: 5s
        retries: 5

  volumes:
    noesis_postgres_data: {}
  ```
- `research/Noesis/devops/env/default.env` (`PR_P2` created a placeholder) gets
  `POSTGRES_DB`/`POSTGRES_USER`/`NOESIS_DB_BACKEND` added for local dev
  defaults; `POSTGRES_PASSWORD` stays out of the committed file, same treatment
  `PR_P2` already gives `NOESIS_API_KEYS` (passed via `docker compose run -e` /
  the shell environment instead)
- Local persistence caveat: `noesis_postgres_data` is a plain Docker volume, so
  `docker compose down` (no `-v`) preserves it across a restart, but it is still
  node-local, not replicated; a host disk failure loses it the same as today's
  in-memory state would on a crash. This is fine for local dev but not a
  substitute for a managed DB in production (see below)
- Production (the `PR_P2` "Cloud Target" ECS path): do **not** run
  `noesis_postgres` as a sidecar container in the same ECS task; use AWS RDS
  (managed Postgres) instead, with the five `POSTGRES_*` values set as ECS task
  definition `secrets` entries, the same treatment `PR_P2` already specifies for
  `NOESIS_API_KEYS`. Provisioning the RDS instance itself is one-time AWS infra
  setup, out of scope here (same caveat `spec.PR_P2.md` raises for the ECS
  cluster/service themselves)

## Configuration and Secrets
- New required env vars when `NOESIS_DB_BACKEND=postgres`: `POSTGRES_HOST`,
  `POSTGRES_DB`, `POSTGRES_PORT`, `POSTGRES_USER`, `POSTGRES_PASSWORD` (names
  fixed by `hsql_implementation.get_connection_from_env_vars()`, not renamable
  without also changing that shared helper)
- `NOESIS_DB_BACKEND` itself defaults to `"memory"`, so an existing `PR_P2`
  deployment that never sets it keeps running exactly as before this PR lands;
  this is the rollback path if the Postgres backend misbehaves in production
- `POSTGRES_PASSWORD`: local dev via `docker compose run -e` / shell env
  (never committed); production via ECS `secrets` backed by AWS Secrets
  Manager or Parameter Store, matching `NOESIS_API_KEYS`'s existing treatment

## Unit Tests
- New file `research/Noesis/test/test_postgres_store.py`, naming per
  `.claude/skills/testing.rules.md`
- Uses `helpers.hsql_test.TestDbHelper` (or its `TestImOmsDbHelper` concrete
  subclass, adapted with a `noesis_postgres` service name/env file) rather than
  mocking Postgres: this is a deliberate call worth flagging against
  `.claude/skills/testing.rules.md`'s general "Mock Only External Dependencies"
  guidance, which lists databases as something to mock. `TestDbHelper` is this
  ecosystem's own established, already-maintained mechanism specifically for
  testing code that talks to a real Postgres (spins up an ephemeral
  `docker-compose` Postgres per test class, torn down after), and exercising
  the actual DDL/SQL in `postgres_store.py` against a mock would not catch a
  real SQL error; if this tradeoff is rejected at implementation time, mocking
  `psycopg2` at the call site is the fallback, at the cost of not testing the
  DDL/SQL itself
  - `@pytest.mark.requires_docker_in_docker` (inherited from `TestDbHelper`)
  - `TestPostgresOrderBookStore`:
    - `test1`: `add_bid()`/`add_ask()` then `get_bids()`/`get_asks()` round-trip
      the same `Bid`/`Ask` fields back
    - `test2`: three bids added in a known order come back from `get_bids()`
      in that same order (guards the `ORDER BY id` requirement above)
    - `test3`: `clear()` empties both tables; a subsequent `get_bids()`/
      `get_asks()` returns `[]`
  - `TestPostgresContractStore`:
    - `test1`: `save_contract()` returns an id that `get_contract()` resolves
      back to an equal `Contract`
    - `test2`: a fresh `PostgresContractStore(connection)` instance (same
      connection, new Python object, simulating a process restart) still
      resolves a `contract_id` saved by a prior instance, the behavior
      `_InMemoryContractStore` cannot offer and the whole point of this PR
    - `test3`: `next_round_id()` called twice returns two different, increasing
      ids; `save_round()`/`get_latest_round()` round-trip a `RoundClearResponse`
    - `test4`: `get_contract()` on an unknown id raises `AssertionError`
  - `TestPostgresRequestLogStore`:
    - `test1`: `append()` then `get_all()` round-trips the logged fields,
      `request_id` assigned by the store
    - `test2`: `query(provider=...)`/`query(model=...)` filter as `Gateway.
      query_log()` already does today
  - `Test_init_schema`:
    - `test1`: calling `init_schema()` twice on the same connection does not
      raise (idempotency of `CREATE TABLE IF NOT EXISTS`)
- `research/Noesis/test/test_batch_call_auction.py`,
  `test/test_contract_dispatch.py`, `test/test_passthrough_proxy.py`, and
  `test/test_platform_api.py`: **no changes expected**. `OrderBook()`,
  `Gateway()`, and `_MarketState(order_book)` called with no `store=` argument
  default to the extracted `_InMemory*Store`s, byte-for-byte the same list/dict
  behavior as today; this is the regression signal that the default backend
  truly did not change, not just an assumption
- Extend `research/Noesis/test/test_main.py` (from `PR_P2`'s spec): a case
  covering `NOESIS_DB_BACKEND` defaulting to `"memory"` when unset, exercised
  the same way `PR_P2`'s `Test__parse_api_keys` isolates a pure env-parsing
  function from `main.py`'s import-time side effects

## Risks and Limitations to Call Out
- **Id-counter correctness is the main risk of a shallow implementation**: if
  `contract_id`/`round_id`/`request_id` are kept as Python-side counters seeded
  at `0` on every process start (today's behavior) instead of moved to
  DB-generated ids (`BIGSERIAL`/`nextval()` as specced above), persisted rows
  from a prior process would collide with ids reassigned after a restart; this
  spec's `save_contract()`/`next_round_id()`/`append()` all return a
  DB-assigned id specifically to avoid this
- `round_id` must be assigned once per `clear_round()` call and shared across
  every tier's row in that round, not once per row; using a per-row `SERIAL` on
  `noesis_tier_rounds` (an easy mistake, since `contract_id`/`request_id` *are*
  fine as per-row `SERIAL`s) would silently change `round_id`'s meaning
- `ORDER BY` is required, not optional, on every `get_bids()`/`get_asks()`/
  `get_all()`/`get_latest_round()` query: Postgres row order is otherwise
  unspecified, which would make the auction's price-tie-breaking and the
  request log's "in call order" contract nondeterministic in a way the
  in-memory list never was
- `GET /health` stays DB-agnostic (a liveness check per `spec.PR_P2.md`'s
  design, not extended into a readiness check here): a container can report
  `{"status": "ok"}` while `NOESIS_DB_BACKEND=postgres` and the DB connection is
  actually down, since `main.py` only calls `wait_db_connection()` once at
  startup, not on every health check
- Local dev persistence is a single Docker volume, not a replicated/managed
  datastore; production should use RDS, not the compose `noesis_postgres`
  service, per "Docker" above
- No connection pooling: a single shared `psycopg2` connection serves every
  request for the process lifetime; acceptable for this prototype's expected
  load, a bottleneck if concurrent request volume grows (see "Out of Scope")
- This PR does not address `architecture.md`'s other open weaknesses
  (exact-tier-only matching, at-most-one-bid-per-buyer assumption, no
  reputation filtering, no rate limiting): it only changes where the three
  state surfaces live, not the business logic operating on them

## Result (to Fill in Once Implemented)
- A `NoesisMarket`/`NoesisServer` instance backed by persistent Postgres storage
  instead of the current in-process `List`/`Dict` state, per `plan.Noesis.md`'s
  `PR_P2b` Result line
- Record what was actually implemented vs. deferred, e.g. whether
  `NOESIS_DB_BACKEND=postgres` was exercised against a real cloud Postgres
  (RDS or otherwise) or only against the local `docker-compose` service, and
  whether the id-counter correctness point above was implemented as specced
