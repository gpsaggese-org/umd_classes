# Running the txtai Market Research Platform

End-to-end this project does three things:

1. **Collect** SEC filings (EDGAR) and news articles (NewsAPI + Alpha Vantage)
   into a four-tier store: KeyDB (hot cache), MinIO (cold archive),
   PostgreSQL + pgvector (warm structured store), and a txtai embeddings
   index (search).
2. **Search** the index through an agentic pipeline — a router picks
   sub-agents (`sec`, `news`), each retrieves the top-k chunks, and a
   synthesizer writes a cited answer.
3. **Serve** the pipeline as a FastAPI service with a Streamlit UI on top.

## Quickstart for new users

```bash
# 1. Clone and enter the repo
git clone <repo-url>
cd class_project/data605/Spring2026/projects/UmdTask430_DATA605_Spring2026_txtai_for_market_research

# 2. Configure secrets
cp .env.example .env
# Edit .env to add NEWSAPI_KEY (https://newsapi.org/register)
# and ALPHAVANTAGE_API_KEY (https://www.alphavantage.co/support/#api-key)
# Replace SEC_USER_AGENT email with yours

# 3. Bring up storage tiers (KeyDB, MinIO, Postgres + pgvector)
docker-compose up -d

# 4. Install Python deps (Python 3.11+)
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# 5. Collect data (one-time; ~50 min for the full ticker set)
python -m scripts.run_sec_bulk --group all --skip-existing --limit 10
python -m scripts.run_all_collectors --tickers AAPL,MSFT,NVDA --skip-sec --no-search
python -m scripts.backfill_txtai_from_chunks --from-scratch

# 6. Start the API + UI
uvicorn app.api.server:app --host 127.0.0.1 --port 8000 &
streamlit run app/ui/research.py --server.port 8501
# Browse to http://localhost:8501
```

## Agent / API / UI

- **Agent core**: `app/agents/research_agent.py` — `run_research(query)`
  yields streaming events; `run_research_sync(query)` returns a single dict.
- **FastAPI**: `app/api/server.py`
  - `GET /` — health probe
  - `POST /research` — sync request, returns JSON (answer + sources + timings)
  - `POST /research/stream` — Server-Sent Events, one event per pipeline
    step (route → retrieve → synthesize → done)
- **Streamlit UI**: `app/ui/research.py` — shows the agent's live trace
  while it runs, then collapses it into an expander and renders the clean
  answer + sources.

### Optional: enable LLM-backed answer synthesis

The synthesizer falls back to an extractive template (first 1-2 sentences
of the top three chunks). Set these env vars on the API server to use any
OpenAI-compatible endpoint:

```bash
export LLM_BASE_URL=http://localhost:11434/v1   # or https://api.openai.com/v1
export LLM_API_KEY=sk-...                        # any value for local Ollama
export LLM_MODEL=qwen2.5:3b                      # or gpt-4o-mini
uvicorn app.api.server:app --host 127.0.0.1 --port 8000
```

## Eval harness

```bash
python -m scripts.eval_research --warmup
python -m scripts.eval_research --repeats 5 --json logs/eval.json
```

Prints p50/p95/p99 latency per pipeline stage, routing accuracy on a
benchmark set, and retrieval health metrics.

---

# Running the SEC EDGAR Collector

This guide explains how to run the SEC EDGAR collector to fetch and store filings.

## Prerequisites

### 1. Start Infrastructure Services

First, start all required services (KeyDB, PostgreSQL, MinIO):

```bash
docker-compose up -d
```

Verify services are running:

```bash
docker-compose ps
```

You should see:
- `keydb` - Hot tier cache (port 6379)
- `postgres` - Warm tier database with pgvector (port 5432)
- `minio` - Cold tier object storage (ports 9000, 9001)

### 2. Configure Environment

Copy the example environment file and configure:

```bash
cp .env.example .env
```

Edit `.env` with your settings:

```bash
# KeyDB Configuration (Hot Tier)
KEYDB_HOST=localhost
KEYDB_PORT=6379
KEYDB_PASSWORD=

# MinIO Configuration (Cold Tier)
MINIO_ENDPOINT=localhost:9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin
MINIO_SECURE=false

# PostgreSQL Configuration (Warm Tier)
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=financial_kb
POSTGRES_USER=fin
POSTGRES_PASSWORD=fin_local

# OpenAI API Key (required for embeddings)
OPENAI_API_KEY=sk-your-api-key-here

# SEC EDGAR User Agent (required by SEC API)
SEC_USER_AGENT=txtai-market-research (your@email.com)
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Initialize Database

The database is automatically initialized when PostgreSQL starts via the `sql/init.sql` script mounted in `docker-compose.yml`.

To manually verify initialization:

```bash
docker-compose exec postgres psql -U fin -d financial_kb -c "\dt"
```

You should see tables: `companies`, `filings`, `chunks`, `xbrl_facts`, `articles`, `collection_runs`

## Running the SEC Collector

### Basic Usage

Fetch SEC filings for Apple (AAPL):

```bash
python -m scripts.run_sec_collector --ticker AAPL
```

### Command Line Options

```
usage: run_sec_collector.py [-h] [-t TICKER] [-f FILING_TYPES] [-l LIMIT]
                            [--no-cold] [--no-warm] [--no-search]
                            [--use-cache] [-v]

options:
  -h, --help            show this help message and exit
  -t, --ticker TICKER   Stock ticker symbol (default: AAPL)
  -f, --filing-types    Comma-separated filing types (default: 10-K,8-K,DEF 14A)
  -l, --limit           Maximum filings per type (default: 20)
  --no-cold             Skip cold storage (MinIO)
  --no-warm             Skip warm storage (PostgreSQL)
  --no-search           Skip search index (txtai)
  --use-cache           Use cached results if available
  -v, --verbose         Enable debug logging
```

### Examples

**Fetch only 10-K filings for Tesla:**

```bash
python -m scripts.run_sec_collector -t TSLA -f 10-K -l 5
```

**Fetch multiple filing types for Microsoft:**

```bash
python -m scripts.run_sec_collector -t MSFT -f "10-K,10-Q,8-K" -l 10
```

**Skip search indexing (faster, just archive):**

```bash
python -m scripts.run_sec_collector -t GOOGL --no-search
```

**Enable verbose logging for debugging:**

```bash
python -m scripts.run_sec_collector -t AAPL -v
```

## Verifying Collection

### Check MinIO (Cold Storage)

Access MinIO console at http://localhost:9001 with credentials:
- Username: `minioadmin`
- Password: `minioadmin`

Browse to the `filings` bucket to see stored SEC filings.

### Check PostgreSQL (Warm Storage)

Connect to PostgreSQL and query:

```bash
docker-compose exec postgres psql -U fin -d financial_kb -c "SELECT ticker, filing_type, filing_date FROM filings ORDER BY filing_date DESC LIMIT 10;"
```

### Check Search Index

Run the example notebook to verify search functionality end-to-end:

```bash
jupyter lab notebooks/txtai.example.ipynb
```

Or do an isolated txtai-API tour without the storage tiers:

```bash
jupyter lab notebooks/txtai.API.ipynb
```

## Troubleshooting

### Connection Errors

If you see connection errors:

1. Verify Docker containers are running:
   ```bash
   docker-compose ps
   ```

2. Check service logs:
   ```bash
   docker-compose logs postgres
   docker-compose logs minio
   docker-compose logs keydb
   ```

### SEC API Rate Limiting

The SEC API may rate-limit requests. If this happens:

1. Ensure you have a valid `SEC_USER_AGENT` in `.env`
2. Reduce the `--limit` parameter
3. Wait a few minutes between requests

### Missing OpenAI API Key

Embeddings require an OpenAI API key. Set in `.env`:

```bash
OPENAI_API_KEY=sk-...
```

### pgvector Extension Not Found

If pgvector is not enabled:

```bash
docker-compose down
docker volume rm <project>_pgdata
docker-compose up -d postgres
```

This recreates the PostgreSQL volume and reinitializes with pgvector.

## Architecture Overview

```
SEC EDGAR API
     │
     ▼
┌─────────────────┐
│  SECCollector   │
└────────┬────────┘
         │
    ┌────┴────┬─────────────┬──────────────┐
    ▼         ▼             ▼              ▼
┌────────┐ ┌──────────┐ ┌─────────┐ ┌──────────┐
│ MinIO  │ │PostgreSQL│ │  txtai  │ │  KeyDB   │
│ (Cold) │ │  (Warm)  │ │ (Search)│ │  (Hot)   │
└────────┘ └──────────┘ └─────────┘ └──────────┘
```

- **Cold (MinIO)**: Raw HTML/XML filings archived
- **Warm (PostgreSQL)**: Structured metadata, chunks with embeddings
- **Search (txtai)**: Semantic search index
- **Hot (KeyDB)**: API response caching
