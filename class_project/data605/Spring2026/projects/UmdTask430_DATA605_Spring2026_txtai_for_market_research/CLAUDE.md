# CLAUDE.md

- Guidance for Claude Code when working in this project
- The repo-wide `CLAUDE.md` at `/Users/gprakash/src/umd_classes1/CLAUDE.md` still
  applies (coding style, testing, notebook, markdown rules) — this file only
  adds project-specific context

# What This Project Is

- A txtai-based market research platform for the DATA605 Spring 2026 course
  (`UmdTask430`)
- End-to-end it does three things:
  - **Collect**: SEC EDGAR filings + news (NewsAPI, Alpha Vantage) into a
    four-tier store
  - **Search**: an agentic pipeline routes a query to sub-agents (`sec`,
    `news`), retrieves top-k chunks, and synthesizes a cited answer
  - **Serve**: a FastAPI service with a Streamlit UI
- See `RUN_INSTRUCTIONS.md` for the full quickstart, env vars, and
  troubleshooting — do not duplicate that here

# Repository Layout

- `app/`: application code (importable as `app.*`)
  - `agents/research_agent.py`: core agentic pipeline; `run_research(query)`
    streams events, `run_research_sync(query)` returns a single dict
  - `agents/{diligence,earnings,regulatory,sentiment,web_research,orchestrator}.py`:
    domain agents used by the dashboard/chat UI
  - `api/server.py`: FastAPI app — `GET /`, `POST /research`,
    `POST /research/stream` (SSE)
  - `collectors/`: `base_collector.py`, `sec_collector.py`,
    `news_collector.py`
  - `pipeline/`: `ingest.py` (chunking/normalization), `embeddings.py` (txtai
    index)
  - `storage/`: four-tier storage clients
    - `hot_storage/`: KeyDB (live prices, semantic cache, sessions)
    - `warm_storage/`: PostgreSQL + pgvector (filings, chunks, XBRL facts)
    - `cold_storage/`: MinIO (raw filings archive)
    - `cache_manager.py`: thin wrapper over KeyDB
  - `ui/`: Streamlit pages — `research.py` (agent chat), `dashboard.py`,
    `chat.py`; entrypoint is `app/main.py`
- `scripts/`: one-shot CLIs (`run_sec_collector`, `run_sec_bulk`,
  `run_all_collectors`, `backfill_txtai_from_chunks`, `eval_research`,
  `check_storage_status`)
- `sql/init.sql`: PostgreSQL schema (mounted into the postgres container)
- `data/`: persisted txtai index (`documents`, `embeddings`, `index.db`,
  `config.json`) — large binary files, do not commit
- `notebooks/`: jupytext-paired notebooks
  - `txtai.API.{ipynb,py}`: txtai library primitives in isolation
  - `txtai.example.{ipynb,py}`: full ingest → search → agent demo
- `docker-compose.yml`: brings up KeyDB, PostgreSQL+pgvector, MinIO

# Common Commands

- Bring up infra (KeyDB, Postgres+pgvector, MinIO):
  ```bash
  > docker-compose up -d
  > docker-compose ps
  ```
- Install deps (Python 3.11+):
  ```bash
  > python -m venv .venv && source .venv/bin/activate
  > pip install -r requirements.txt
  ```
- Collect data (one-time):
  ```bash
  > python -m scripts.run_sec_bulk --group all --skip-existing --limit 10
  > python -m scripts.run_all_collectors --tickers AAPL,MSFT,NVDA --skip-sec --no-search
  > python -m scripts.backfill_txtai_from_chunks --from-scratch
  ```
- Run API + UI:
  ```bash
  > uvicorn app.api.server:app --host 127.0.0.1 --port 8000 &
  > streamlit run app/ui/research.py --server.port 8501
  ```
- Evaluate the pipeline:
  ```bash
  > python -m scripts.eval_research --warmup
  > python -m scripts.eval_research --repeats 5 --json logs/eval.json
  ```
- Inspect storage state:
  ```bash
  > python -m scripts.check_storage_status
  ```

# Configuration

- Secrets and connection strings live in `.env` (template: `.env.example`)
- Required keys for a full run:
  - `SEC_USER_AGENT`: SEC EDGAR requires a real contact email
  - `NEWSAPI_KEY`, `ALPHAVANTAGE_API_KEY`: news collectors
  - `OPENAI_API_KEY`: embeddings (txtai default backend)
- Optional for LLM-backed answer synthesis:
  - `LLM_BASE_URL`, `LLM_API_KEY`, `LLM_MODEL` (any OpenAI-compatible endpoint,
    including local Ollama) — without these the synthesizer falls back to an
    extractive template
- Never read or write secrets in code; always pull from environment variables

# Conventions Specific to This Project

- Python imports use module-qualified names (`from app.storage import ...`,
  `from app.agents.research_agent import ...`) — keep it that way
- Storage clients are accessed via factory helpers (`get_keydb_client`,
  `get_postgres_client`, `get_minio_client`, `get_cache_manager`,
  `get_embeddings`) — do not instantiate clients directly in new code
- Collectors inherit from `app/collectors/base_collector.py`; new sources
  should follow the same `fetch → normalize → store` flow
- Long-running collection scripts must support `--skip-existing` and
  `--no-search` style toggles so partial runs are cheap
- Logs go to `logs/` (gitignored); persistent artifacts go to `data/`

# Things to Avoid

- Do not commit `.env`, `data/`, `logs/`, `.venv/`, or anything in
  `**/__pycache__/`
- Do not edit `data/{documents,embeddings,index.db}` by hand — rebuild via
  `scripts.backfill_txtai_from_chunks`
- Do not bypass the storage tier abstraction (e.g. talking directly to psycopg
  or boto from agent code) — go through `app.storage`
- Do not add new top-level docs files for one-off notes; extend
  `RUN_INSTRUCTIONS.md` or this file

# When in Doubt

- Architecture / data flow: `RUN_INSTRUCTIONS.md` and `app/storage/README.md`
- Schema: `sql/init.sql`
- Agent behavior: `app/agents/research_agent.py` (router → retrievers →
  synthesizer)
- Eval / benchmarks: `scripts/eval_research.py`
