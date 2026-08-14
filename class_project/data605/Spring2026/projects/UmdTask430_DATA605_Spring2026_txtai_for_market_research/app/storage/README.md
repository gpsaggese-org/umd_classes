# Storage Layer - Multi-Tier Architecture

This module implements a **multi-tier storage architecture** for financial market research data.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        Storage Architecture                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  HOT TIER - KeyDB (Redis-compatible)                                 │   │
│  │  ┌───────────────┬──────────────────┬────────────────────────────┐  │   │
│  │  │ prices:{ticker}│ cache:{md5_hash} │ session:{id}               │  │   │
│  │  │ TTL: 60s      │ TTL: 3600s       │ TTL: 1800s                 │  │   │
│  │  │ (live prices) │ (semantic cache) │ (agent memory)             │  │   │
│  │  └───────────────┴──────────────────┴────────────────────────────┘  │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  WARM TIER - PostgreSQL + pgvector                                   │   │
│  │  ┌────────────┬──────────────┬────────────────┬──────────────────┐  │   │
│  │  │ filings    │ chunks       │ xbrl_facts     │ articles         │  │   │
│  │  │ (metadata) │ (w/embeddings)│ (structured)   │ (news metadata)  │  │   │
│  │  └────────────┴──────────────┴────────────────┴──────────────────┘  │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  COLD TIER - MinIO (S3-compatible)                                   │   │
│  │  ┌────────────┬──────────────┬────────────────┬──────────────────┐  │   │
│  │  │ sec/       │ news/        │ web/           │ social/          │  │   │
│  │  │ (filings)  │ (articles)   │ (scrapes)      │ (posts)          │  │   │
│  │  └────────────┴──────────────┴────────────────┴──────────────────┘  │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  SEARCH - txtai EmbeddingsIndex (SQLite)                             │   │
│  │  - Embedded chunks with semantic search                              │   │
│  │  - Filterable by source (news|sec|web|social)                        │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Storage Tiers

| Tier | Technology | Purpose | TTL | Data Types |
|------|------------|---------|-----|------------|
| **Hot** | KeyDB | Live cache, sessions | 60s-3600s | Prices, semantic cache, agent state |
| **Warm** | PostgreSQL + pgvector | Structured data, embeddings | Persistent | Filings, chunks, XBRL facts, articles |
| **Cold** | MinIO | Raw document archive | Persistent | SEC filings, news HTML, web scrapes |
| **Search** | txtai (SQLite) | Semantic search index | Persistent | Embedded chunks with metadata |

## Components

### Hot Tier - KeyDB

**Files:** `hot_storage/keydb_client.py`, `cache_manager.py`

```python
from app.storage import get_keydb_client, get_cache_manager

# Low-level client
client = get_keydb_client()
client.set("key", "value", ttl=300)

# High-level cache manager
cache = get_cache_manager()
cache.set_price("AAPL", price_data)
cache.set_semantic(query, results)
```

### Warm Tier - PostgreSQL + pgvector

**Files:** `warm_storage/pgvector_client.py`, `warm_storage/filings_manager.py`

```python
from app.storage import get_postgres_client

postgres = get_postgres_client()

# Insert filing metadata
filing_id = postgres.insert_filing(filing_data)

# Insert chunks with embeddings
postgres.insert_chunks(chunks)

# Vector similarity search
results = postgres.search_similar(query_embedding, limit=10)
```

### Cold Tier - MinIO

**Files:** `cold_storage/minio_client.py`

```python
from app.storage import get_minio_client

minio = get_minio_client()

# Store SEC filing
minio.store_sec_filing(
    ticker="AAPL",
    filing_type="10-K",
    accession_number="0000320193-24-000006",
    content=html_content,
)

# Store news article
minio.store_news_article(
    ticker="AAPL",
    url="https://...",
    content=html_content,
    metadata={"title": "...", "published_at": "..."},
)
```

### Search Tier - txtai

**Files:** `../pipeline/embeddings.py`

```python
from app.pipeline.embeddings import get_embeddings, search

embeddings = get_embeddings()
results = search("Apple revenue", source_filter="sec", limit=5)
```

## Collectors - Writing to All Tiers

The `app/collectors/` module provides unified data collection that writes to all storage tiers:

```python
from app.collectors import SECCollector, NewsCollector, WebCollector, SocialCollector

# SEC filings collector
sec = SECCollector()
results = sec.collect(
    ticker="AAPL",
    filing_types=["10-K", "8-K"],
    store_cold=True,   # MinIO: raw filings
    store_warm=True,   # PostgreSQL: metadata + chunks
    store_search=True, # txtai: embeddings
)

# News collector
news = NewsCollector()
news.collect("AAPL", days_back=7)

# Web collector (press releases)
web = WebCollector()
web.collect("AAPL")

# Social collector (Reddit, StockTwits)
social = SocialCollector()
social.collect("AAPL", subreddits=["investing", "stocks"])
```

### Collector Flow

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   Fetch      │────▶│   Cold       │────▶│   Warm       │────▶│   Search     │
│   (API)      │     │   (MinIO)    │     │   (PostgreSQL)│    │   (txtai)    │
└──────────────┘     └──────────────┘     └──────────────┘     └──────────────┘
      │                      │                    │                    │
      │                      │                    │                    │
      ▼                      ▼                    ▼                    ▼
  Raw documents         Raw HTML/JSON       Structured data     Embeddings +
  with metadata         archive             + chunks            semantic index
```

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment

Copy `.env.example` to `.env` and configure:

```bash
# Hot Tier - KeyDB
KEYDB_HOST=localhost
KEYDB_PORT=6379
KEYDB_PASSWORD=

# Cold Tier - MinIO
MINIO_ENDPOINT=localhost:9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin
MINIO_SECURE=false

# Warm Tier - PostgreSQL
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=financial_kb
POSTGRES_USER=fin
POSTGRES_PASSWORD=fin_local

# Embeddings - Ollama
OLLAMA_HOST=http://localhost:11434
OLLAMA_EMBEDDING_MODEL=nomic-embed-text
```

### 3. Start Infrastructure

```bash
docker-compose up -d
```

This starts:
- KeyDB on port 6379
- PostgreSQL + pgvector on port 5432
- MinIO on ports 9000 (API) and 9001 (console)

### 4. Verify Connections

```bash
# KeyDB
redis-cli -h localhost -p 6379 ping  # Should return: PONG

# PostgreSQL
psql -h localhost -U fin -d financial_kb -c "SELECT 1"

# MinIO
curl http://localhost:9000/minio/health/live  # Should return: OK

# Or use the test scripts
python -m app.storage.hot_storage.tests.test_keydb
python -m app.storage.warm_storage.tests.test_pgvector
python -m app.storage.cold_storage.tests.test_minio
```

## Data Flow Example

Full pipeline for collecting and storing SEC filings:

```python
from app.collectors import SECCollector

# Initialize collector
sec = SECCollector()

# Collect filings - stores to ALL tiers
results = sec.collect(
    ticker="AAPL",
    filing_types=["10-K", "8-K", "DEF 14A"],
    limit=20,
    store_cold=True,   # Archive raw HTML in MinIO
    store_warm=True,   # Store metadata in PostgreSQL
    store_search=True, # Generate embeddings in txtai
)

print(f"Fetched: {results['fetched']}")
print(f"Stored in cold (MinIO): {results['stored_cold']}")
print(f"Stored in warm (PostgreSQL): {results['stored_warm']}")
print(f"Indexed for search: {results['indexed']}")
```

## Bucket Structure (MinIO)

```
filings/
├── sec/
│   ├── AAPL/
│   │   ├── 10-K/
│   │   │   └── 000032019324000006.html
│   │   └── 8-K/
│   └── MSFT/
│       └── ...
articles/
├── news/
│   ├── AAPL/
│   │   ├── 2024-01-15/
│   │   │   └── abc123def456.html
│   └── ...
web_scrapes/
├── web/
│   ├── AAPL/
│   │   └── abc123.html
social/
├── reddit/
│   └── AAPL/
│       └── post_id.json
```

## Key Design Decisions

### Why Multi-Tier?

| Tier | Use Case | Query Pattern |
|------|----------|---------------|
| Hot | Real-time data, session state | Key-value lookup, sub-millisecond |
| Warm | Structured queries, vector search | SQL, cosine similarity |
| Cold | Compliance, audit, reprocessing | Object retrieval |
| Search | Semantic search | Natural language queries |

### TTL Strategy

| Data Type | TTL | Rationale |
|-----------|-----|-----------|
| Prices | 60s | Live feeds update frequently |
| Semantic cache | 3600s | Expensive embeddings, 1hr balances cost/freshness |
| Sessions | 1800s | User sessions expire after 30min inactivity |
| Cold/Warm | Persistent | Compliance and historical analysis |

## Troubleshooting

### Connection Issues

```bash
# Check Docker containers
docker-compose ps

# View logs
docker-compose logs keydb
docker-compose logs postgres
docker-compose logs minio
```

### MinIO Browser

Access MinIO console at http://localhost:9001 with credentials:
- Username: `minioadmin`
- Password: `minioadmin`

### PostgreSQL Vector Search

```sql
-- Check pgvector extension
SELECT * FROM pg_extension WHERE extname = 'vector';

-- Check embedding dimensions
SELECT embedding::text FROM chunks LIMIT 1;
```

## Next Steps

1. **Graph Tier**: Add Kuzu for company/filing relationships
2. **Analytics Tier**: Add DuckDB + Parquet for time-series analysis
3. **Backup**: Configure MinIO bucket replication for disaster recovery
