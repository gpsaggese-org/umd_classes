# storage/warm_storage/tests/test_pgvector.py
import logging
import os
import pytest

_LOG = logging.getLogger(__name__)

pytestmark = pytest.mark.skipif(
    not os.getenv("POSTGRES_HOST"),
    reason="POSTGRES_HOST not set - skipping PostgreSQL tests",
)


@pytest.fixture(scope="module")
def pg():
    from app.storage.warm_storage.pgvector_client import get_postgres_client
    client = get_postgres_client()
    yield client
    client.close()


# ── connection ────────────────────────────────────────────────────────────────

def test_ping(pg):
    assert pg.ping() is True


# ── companies ─────────────────────────────────────────────────────────────────

def test_upsert_and_get_company(pg):
    pg.upsert_company(
        cik="0000320193",
        ticker="AAPL",
        name="Apple Inc.",
        sic_code="3571",
        sector="Information Technology",
        sub_industry="Technology Hardware",
    )
    company = pg.get_company("0000320193")
    assert company is not None
    assert company["ticker"] == "AAPL"
    assert company["name"] == "Apple Inc."


# ── filings ───────────────────────────────────────────────────────────────────

def test_upsert_and_get_filing(pg):
    pg.upsert_company(
        cik="0000320193",
        ticker="AAPL",
        name="Apple Inc.",
    )
    filing_id = pg.upsert_filing(
        cik="0000320193",
        form_type="10-K",
        filing_date="2024-01-01",
        accession="0000320193-24-000001",
        s3_raw_path="s3://raw-edgar/0000320193/primary.htm",
        period_of_report="2023-09-30",
    )
    assert filing_id is not None

    filings = pg.get_filings("0000320193", form_type="10-K")
    assert len(filings) >= 1
    assert filings[0]["form_type"] == "10-K"
    _LOG.info("Filing id: %s", filing_id)


# ── chunks + embeddings ───────────────────────────────────────────────────────

def test_insert_chunk_single(pg):
    filings = pg.get_filings("0000320193", form_type="10-K")
    filing_id = str(filings[0]["id"])
    dummy_embedding = [0.1] * 768

    chunk_id = pg.insert_chunk(
        filing_id=filing_id,
        text="Apple faces intense competition in all markets.",
        embedding=dummy_embedding,
        section="Risk Factors",
        chunk_index=0,
        token_count=8,
        metadata={"cik": "0000320193", "form": "10-K"},
    )
    assert chunk_id is not None
    _LOG.info("Chunk id: %s", chunk_id)


def test_insert_chunks_batch(pg):
    filings = pg.get_filings("0000320193", form_type="10-K")
    filing_id = str(filings[0]["id"])
    dummy_embedding = [0.1] * 768

    chunks = [
        {
            "filing_id":   filing_id,
            "section":     "MD&A",
            "chunk_index": 1,
            "text":        "Revenue increased 8 percent year over year.",
            "token_count": 9,
            "embedding":   dummy_embedding,
            "metadata":    {"cik": "0000320193"},
        },
        {
            "filing_id":   filing_id,
            "section":     "MD&A",
            "chunk_index": 2,
            "text":        "Gross margin expanded to 44 percent driven by services growth.",
            "token_count": 11,
            "embedding":   dummy_embedding,
            "metadata":    {"cik": "0000320193"},
        },
    ]
    count = pg.insert_chunks_batch(chunks)
    assert count == 2
    _LOG.info("Batch inserted %d chunks", count)


def test_semantic_search(pg):
    dummy_embedding = [0.1] * 768

    results = pg.semantic_search(
        embedding=dummy_embedding,
        limit=5,
        cik="0000320193",
    )
    assert len(results) >= 1
    assert "text" in results[0]
    assert "score" in results[0]
    assert "section" in results[0]
    _LOG.info(
        "Top result: '%s' (score=%.4f)",
        results[0]["text"][:60],
        results[0]["score"],
    )


def test_semantic_search_with_section_filter(pg):
    dummy_embedding = [0.1] * 768

    results = pg.semantic_search(
        embedding=dummy_embedding,
        limit=5,
        section="Risk Factors",
        cik="0000320193",
    )
    assert all(r["section"] == "Risk Factors" for r in results)
    _LOG.info("Section filtered results: %d", len(results))


# ── xbrl facts ────────────────────────────────────────────────────────────────

def test_upsert_xbrl_facts(pg):
    count = pg.upsert_xbrl_facts([
        {
            "cik":        "0000320193",
            "concept":    "Revenues",
            "period_end": "2023-09-30",
            "value":      383285000000,
            "unit":       "USD",
            "form_type":  "10-K",
            "accession":  "0000320193-24-000001",
        },
        {
            "cik":        "0000320193",
            "concept":    "Assets",
            "period_end": "2023-09-30",
            "value":      352583000000,
            "unit":       "USD",
            "form_type":  "10-K",
            "accession":  "0000320193-24-000001",
        },
    ])
    assert count == 2


def test_get_xbrl_facts(pg):
    facts = pg.get_xbrl_facts("0000320193", concept="Revenues")
    assert len(facts) >= 1
    assert float(facts[0]["value"]) == 383285000000.0
    _LOG.info("Revenues: %s %s", facts[0]["value"], facts[0]["unit"])


def test_get_all_xbrl_facts_for_company(pg):
    facts = pg.get_xbrl_facts("0000320193")
    assert len(facts) >= 2
    concepts = {f["concept"] for f in facts}
    assert "Revenues" in concepts
    assert "Assets" in concepts


# ── articles ──────────────────────────────────────────────────────────────────

def test_upsert_article(pg):
    article_id = pg.upsert_article(
        source="reuters",
        url="https://reuters.com/test-article-pgvector-001",
        title="Apple reports record revenue",
        published_at="2024-01-15 10:00:00",
        body_text="Apple Inc. reported record quarterly revenue.",
        sentiment="positive",
        tickers_mentioned=["AAPL"],
    )
    assert article_id is not None
    _LOG.info("Article id: %s", article_id)


def test_upsert_article_duplicate(pg):
    # second insert of same url should return None (ON CONFLICT DO NOTHING)
    duplicate = pg.upsert_article(
        source="reuters",
        url="https://reuters.com/test-article-pgvector-001",
        title="Apple reports record revenue",
        published_at="2024-01-15 10:00:00",
    )
    assert duplicate is None


# ── audit log ─────────────────────────────────────────────────────────────────

def test_collection_run_lifecycle(pg):
    run_id = pg.start_collection_run("test_pgvector_collector")
    assert run_id is not None

    pg.finish_collection_run(
        run_id=run_id,
        records_written=42,
        status="success",
    )
    _LOG.info("Run %s completed", run_id)


def test_collection_run_failure(pg):
    run_id = pg.start_collection_run("test_pgvector_collector_fail")
    assert run_id is not None

    pg.finish_collection_run(
        run_id=run_id,
        records_written=0,
        status="failed",
        error_msg="Simulated failure for test",
    )
    _LOG.info("Failed run %s logged", run_id)