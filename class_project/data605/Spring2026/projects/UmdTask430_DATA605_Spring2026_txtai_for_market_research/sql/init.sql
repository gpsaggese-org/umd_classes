-- txtai Market Research Platform - Database Schema
-- Tiers: Warm (PostgreSQL + pgvector), Graph (Kuzu - planned)
-- Note: Cold tier (MinIO) and Hot tier (KeyDB) are separate

CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- #############################################################################
-- Companies Table
-- #############################################################################
CREATE TABLE IF NOT EXISTS companies (
    cik           VARCHAR(10)  PRIMARY KEY,
    ticker        VARCHAR(10)  UNIQUE,
    name          TEXT         NOT NULL,
    sic_code      VARCHAR(4),
    sector        TEXT,
    sub_industry  TEXT,
    exchange      VARCHAR(10),
    created_at    TIMESTAMPTZ  DEFAULT NOW(),
    updated_at    TIMESTAMPTZ  DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_companies_ticker ON companies(ticker);

-- #############################################################################
-- Filings Table - Stores SEC filing metadata
-- #############################################################################
CREATE TABLE IF NOT EXISTS filings (
    id                VARCHAR(64) PRIMARY KEY,  -- SHA256 hash of ticker:accession:form_type
    ticker            VARCHAR(10) NOT NULL,
    company_name      TEXT,
    filing_type       VARCHAR(20) NOT NULL,     -- e.g., "10-K", "8-K", "DEF 14A"
    cik               VARCHAR(10),
    accession_number  VARCHAR(25) UNIQUE NOT NULL,
    filing_date       DATE,
    period_of_report  DATE,
    document_url      TEXT,
    file_size_bytes   INTEGER,
    created_at        TIMESTAMPTZ DEFAULT NOW(),
    updated_at        TIMESTAMPTZ DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_filings_ticker ON filings(ticker);
CREATE INDEX IF NOT EXISTS idx_filings_type ON filings(filing_type);
CREATE INDEX IF NOT EXISTS idx_filings_date ON filings(filing_date DESC);
CREATE INDEX IF NOT EXISTS idx_filings_cik ON filings(cik);

-- #############################################################################
-- Chunks Table - Document chunks with embeddings for semantic search
-- #############################################################################
CREATE TABLE IF NOT EXISTS chunks (
    id           VARCHAR(64) PRIMARY KEY,  -- SHA256 hash of source:ticker:chunk_text[:100]
    filing_id    VARCHAR(64) REFERENCES filings(id) ON DELETE CASCADE,
    chunk_index  INTEGER NOT NULL,
    text         TEXT NOT NULL,
    section      TEXT,
    embedding    vector(768),  -- sentence-transformers/all-mpnet-base-v2
    created_at   TIMESTAMPTZ DEFAULT NOW(),
    updated_at   TIMESTAMPTZ DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_chunks_embedding
    ON chunks USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);
CREATE INDEX IF NOT EXISTS idx_chunks_filing ON chunks(filing_id);
CREATE INDEX IF NOT EXISTS idx_chunks_section ON chunks(section);

-- #############################################################################
-- Document Metadata Table - Key/value metadata for chunks
-- #############################################################################
CREATE TABLE IF NOT EXISTS document_metadata (
    id        VARCHAR(64) PRIMARY KEY,  -- SHA256 hash of chunk_id:key
    chunk_id  VARCHAR(64) REFERENCES chunks(id) ON DELETE CASCADE,
    key       VARCHAR(255) NOT NULL,
    value     TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_document_metadata_chunk ON document_metadata(chunk_id);
CREATE INDEX IF NOT EXISTS idx_document_metadata_key ON document_metadata(key);

-- #############################################################################
-- XBRL Facts Table - Structured financial data from SEC filings
-- #############################################################################
CREATE TABLE IF NOT EXISTS xbrl_facts (
    id            VARCHAR(64) PRIMARY KEY,
    filing_id     VARCHAR(64) REFERENCES filings(id) ON DELETE CASCADE,
    concept_name  VARCHAR(100) NOT NULL,
    value         TEXT,
    value_numeric NUMERIC,
    unit          VARCHAR(20),
    period_start  DATE,
    period_end    DATE,
    instant_date  DATE,
    axis          VARCHAR(100),
    member        TEXT,
    created_at    TIMESTAMPTZ DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_xbrl_facts_filing ON xbrl_facts(filing_id);
CREATE INDEX IF NOT EXISTS idx_xbrl_concept ON xbrl_facts(concept_name);
CREATE INDEX IF NOT EXISTS idx_xbrl_period ON xbrl_facts(period_end DESC);

-- #############################################################################
-- Collection Runs Table - Track data collection job history
-- #############################################################################
CREATE TABLE IF NOT EXISTS collection_runs (
    id               UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    collector        VARCHAR(50) NOT NULL,
    ticker           VARCHAR(10),
    started_at       TIMESTAMPTZ DEFAULT NOW(),
    finished_at      TIMESTAMPTZ,
    records_written  INTEGER DEFAULT 0,
    status           VARCHAR(20) DEFAULT 'running',
    error_msg        TEXT
);
CREATE INDEX IF NOT EXISTS idx_collection_runs_collector ON collection_runs(collector);
CREATE INDEX IF NOT EXISTS idx_collection_runs_ticker ON collection_runs(ticker);