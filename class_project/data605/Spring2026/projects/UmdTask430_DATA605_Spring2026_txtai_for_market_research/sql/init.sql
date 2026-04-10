cat > sql/init.sql << 'EOF'
CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE IF NOT EXISTS companies (
    cik           VARCHAR(10)  PRIMARY KEY,
    ticker        VARCHAR(10)  UNIQUE,
    name          TEXT         NOT NULL,
    sic_code      VARCHAR(4),
    sector        TEXT,
    sub_industry  TEXT,
    exchange      VARCHAR(10),
    created_at    TIMESTAMPTZ  DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS filings (
    id                UUID        PRIMARY KEY DEFAULT uuid_generate_v4(),
    cik               VARCHAR(10) REFERENCES companies(cik),
    form_type         VARCHAR(20) NOT NULL,
    filing_date       DATE        NOT NULL,
    period_of_report  DATE,
    accession         VARCHAR(25) UNIQUE NOT NULL,
    primary_doc       TEXT,
    s3_raw_path       TEXT,
    processed_at      TIMESTAMPTZ,
    chunk_count       INT DEFAULT 0
);
CREATE INDEX IF NOT EXISTS idx_filings_cik_form ON filings(cik, form_type);
CREATE INDEX IF NOT EXISTS idx_filings_date ON filings(filing_date DESC);

CREATE TABLE IF NOT EXISTS chunks (
    id           UUID    PRIMARY KEY DEFAULT uuid_generate_v4(),
    filing_id    UUID    REFERENCES filings(id) ON DELETE CASCADE,
    section      TEXT,
    chunk_index  INT,
    text         TEXT    NOT NULL,
    token_count  INT,
    embedding    vector(768),
    metadata     JSONB   DEFAULT '{}'
);
CREATE INDEX IF NOT EXISTS idx_chunks_embedding
    ON chunks USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);
CREATE INDEX IF NOT EXISTS idx_chunks_filing  ON chunks(filing_id);
CREATE INDEX IF NOT EXISTS idx_chunks_section ON chunks(section);

CREATE TABLE IF NOT EXISTS xbrl_facts (
    id            UUID        PRIMARY KEY DEFAULT uuid_generate_v4(),
    cik           VARCHAR(10) REFERENCES companies(cik),
    taxonomy      VARCHAR(20) DEFAULT 'us-gaap',
    concept       VARCHAR(100) NOT NULL,
    period_type   VARCHAR(10),
    period_start  DATE,
    period_end    DATE        NOT NULL,
    value         NUMERIC,
    unit          VARCHAR(20),
    form_type     VARCHAR(20),
    accession     VARCHAR(25),
    UNIQUE (cik, concept, period_end, unit, form_type)
);
CREATE INDEX IF NOT EXISTS idx_xbrl_cik_concept ON xbrl_facts(cik, concept);
CREATE INDEX IF NOT EXISTS idx_xbrl_period ON xbrl_facts(period_end DESC);

CREATE TABLE IF NOT EXISTS articles (
    id                 UUID        PRIMARY KEY DEFAULT uuid_generate_v4(),
    source             VARCHAR(50),
    url                TEXT        UNIQUE,
    title              TEXT,
    published_at       TIMESTAMPTZ,
    body_text          TEXT,
    sentiment          VARCHAR(10),
    tickers_mentioned  TEXT[],
    s3_raw_path        TEXT,
    ingested_at        TIMESTAMPTZ DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_articles_published ON articles(published_at DESC);
CREATE INDEX IF NOT EXISTS idx_articles_tickers
    ON articles USING GIN(tickers_mentioned);

CREATE TABLE IF NOT EXISTS collection_runs (
    id               UUID        PRIMARY KEY DEFAULT uuid_generate_v4(),
    collector        VARCHAR(50) NOT NULL,
    started_at       TIMESTAMPTZ DEFAULT NOW(),
    finished_at      TIMESTAMPTZ,
    records_written  INT         DEFAULT 0,
    status           VARCHAR(20) DEFAULT 'running',
    error_msg        TEXT
);
EOF