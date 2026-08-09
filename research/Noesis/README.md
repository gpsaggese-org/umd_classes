# Noesis

Prototype implementation of the \Noesis{} protocol described in
`papers/Noesis/*.tex`: a two-sided market for LLM inference capacity.

- `NoesisMarket`: a batch call-auction that matches buyer/seller orders and
  dispatches cleared contracts to a (mocked) fulfillment layer
- `NoesisServer`: a minimal passthrough proxy that routes prompts to
  registered LLM providers and logs every request/response pair
- `NoesisPlatform`: a thin `fastapi` HTTP surface over both, run via
  `main.py`, with an optional persistent (Postgres) backend and a
  Docker Compose deployment for local dev

See `architecture.md` for the full C4-model architecture and
`plan.Noesis.md` for the milestone-by-milestone implementation roadmap.

## Structure of the Dir

- `architecture.md.figs/`
  - Rendered images embedded in `architecture.md`
- `devops/`
  - Dockerfiles, Docker Compose deployment, and container entrypoint
    scripts for `main.py`'s app plus a Postgres sidecar
- `test/`
  - Unit tests for every module below, one `test_*.py` per module

## Description of Files

- `.dockerignore`
  - Restricts the DEV Docker build context to `devops/` and
    `helpers_root/devops/`
- `architecture.md`
  - C4-model architecture (context/container/component) for the codebase
- `batch_call_auction.py`
  - `OrderBook`: pending bid/ask queue and per-tier uniform-price
    call-auction clearing
- `changelog.txt`
  - Release log for the `noesis_platform` Docker image
- `coding.create_specs.md`
  - Prompt template for generating an implementation spec for the next
    `plan.Noesis.md` PR
- `conftest.py`
  - Pytest bootstrap shared by every test module under `test/`
- `contract_dispatch.py`
  - `Contract` schema, `build_contracts()`, and stubbed fulfillment
    dispatch (stands in for `NoesisServer`)
- `invoke.yaml`
  - `pyinvoke` config (`auto_dash_names: false`, command echo on)
- `main.py`
  - `uvicorn` entry point; builds the module-level `app`, wired to the
    memory or Postgres backend selected via `NOESIS_DB_BACKEND`
- `passthrough_proxy.py`
  - `Gateway`: routes a prompt to a registered LLM provider and logs the
    request/response pair
- `plan.marketing.md`
  - Plan for bootstrapping supply/demand liquidity once `NoesisPlatform`
    exposes a public API
- `plan.Noesis.md`
  - Milestone-by-milestone implementation roadmap for the \Noesis{}
    protocol
- `platform_api.py`
  - `fastapi` app factory (`create_app()`) wrapping the auction, dispatch,
    and proxy modules behind HTTP endpoints
- `postgres_store.py`
  - Postgres-backed implementations of the three in-memory storage
    interfaces (`OrderBookStore`, `ContractStore`, `RequestLogStore`)
- `pytest.ini`
  - Pytest markers (`slow`, `superslow`, `requires_docker_in_docker`, ...)
    and CLI options
- `repo_config.yaml`
  - Repo/Docker/S3 metadata read by `helpers.repo_config_utils`
- `spec.PR_P2.md`
  - Implementation spec for `PR_P2`: containerized cloud deployment
- `spec.PR_P2b.md`
  - Implementation spec for `PR_P2b`: swap the in-memory state for a
    Postgres backend
- `tasks.py`
  - Exposes the `invoke` targets (Docker, AWS, pytest) from
    `helpers.lib_tasks`

## Description of Executables

| Command | Description |
| :------- | :------- |
| `uvicorn research.Noesis.main:app` | Serve the `NoesisPlatform` HTTP API directly (in-process, no Docker) |
| `devops/docker_run/run_docker_noesis.sh` | Build and run the dockerized API (plus a Postgres sidecar) via Docker Compose |
| `devops/docker_run/run_jupyter_server.sh` | Start a Jupyter server inside the dev container |
| `invoke run_fast_tests` | Run the fast unit test suite under `test/` |

### `main.py`

What it does:
- Builds the `fastapi` `app` object that `uvicorn` serves
- Selects the `OrderBook`/`Gateway`/`ContractStore` backend from the
  `NOESIS_DB_BACKEND` env var (`"memory"` default or `"postgres"`)
- Parses `NOESIS_API_KEYS` into the `{api_key: account_id}` map
  `platform_api.create_app()` uses for `X-API-Key` auth

Examples:
- Run with the default in-memory backend, no auth configured:
  ```bash
  > uvicorn research.Noesis.main:app --host 0.0.0.0 --port 8000
  ```
- Run against Postgres, with one API key mapped to `acct_1`:
  ```bash
  > export NOESIS_DB_BACKEND=postgres
  > export POSTGRES_HOST=localhost POSTGRES_DB=noesis POSTGRES_PORT=5432 \
      POSTGRES_USER=noesis POSTGRES_PASSWORD=secret
  > export NOESIS_API_KEYS="key1:acct_1"
  > uvicorn research.Noesis.main:app --host 0.0.0.0 --port 8000
  ```

### `devops/docker_run/run_docker_noesis.sh`

What it does:
- Starts `noesis_api` (and its `noesis_postgres` dependency) via
  `docker compose`, using `devops/compose/docker-compose.noesis.yml` as an
  override on top of the base dev-container compose file
- Prints container status, then tails `noesis_api` logs
- Stops the containers on `Ctrl-C` (`SIGINT`/`SIGTERM` trap)

Examples:
- Run with the default image tag (`1.0.0`):
  ```bash
  > devops/docker_run/run_docker_noesis.sh
  ```
- Run a specific local image version:
  ```bash
  > devops/docker_run/run_docker_noesis.sh 1.2.0
  ```

## Description of Workflows

- Local, in-memory dev loop
  - `> uvicorn research.Noesis.main:app --reload` serves the API with the
    default `NOESIS_DB_BACKEND=memory`; state resets on every restart
  - Exercise it with `POST /bids`, `POST /asks`, `POST /rounds/clear`,
    then `GET /contracts/{contract_id}`, or run `test/` directly
- Containerized dev loop with a persistent backend
  - `devops/docker_run/run_docker_noesis.sh` brings up `noesis_api` next
    to a `noesis_postgres` sidecar, wired together via the
    `NOESIS_DB_BACKEND`/`POSTGRES_*` env vars in
    `devops/compose/docker-compose.noesis.yml`
  - `main.py` calls `postgres_store.init_schema()` at startup, so no
    manual migration step is needed
- Order-to-contract flow (see `architecture.md`'s C3 diagram for detail)
  - `OrderBook.submit_bid()`/`submit_ask()` queue orders in the active
    `OrderBookStore`
  - `OrderBook.clear_round()` buckets pending orders by tier and clears
    each with `_match_orders_in_tier()`
  - `build_contracts()` turns the tier results into `Contract`s;
    `dispatch_contract()` mutates each in place via the injected
    `fulfillment_func` (`mock_fulfill()` by default)
  - `platform_api._MarketState.clear_round()` is the HTTP-facing
    orchestration point tying the steps above together and persisting
    the result via `ContractStore`

## Description of Architecture

Full C1 (context), C2 (container), and C3 (component) diagrams, plus the
design rationale behind each, live in `architecture.md`. In short:

- Every stateful store (`OrderBook`'s order queue, `platform_api`'s
  contract/round log, `Gateway`'s request log) sits behind a pluggable
  `abc.ABC`, with an in-memory default and a `postgres_store.py`
  implementation; the three business-logic modules never import
  `postgres_store.py`, so a caller that never selects the Postgres
  backend never picks up a `psycopg2` dependency
- `passthrough_proxy.py` (`NoesisServer`) has no import relationship
  with `batch_call_auction.py`/`contract_dispatch.py` (`NoesisMarket`);
  `platform_api.py` unifies both only as two independent route groups on
  one HTTP app, not as a shared dependency graph
- Every side effect that would be non-deterministic in a test
  (fulfillment outcome, provider network call, wall-clock time) is
  injected as a callable, so tests control it directly
- `main.py` is the single place that selects the storage backend, once,
  at import time, from `NOESIS_DB_BACKEND`; every other module is
  unaware which backend is active
