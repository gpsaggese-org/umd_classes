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

Run the demo notebook to verify search functionality:

```bash
jupyter notebook notebooks/demo.ipynb
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
