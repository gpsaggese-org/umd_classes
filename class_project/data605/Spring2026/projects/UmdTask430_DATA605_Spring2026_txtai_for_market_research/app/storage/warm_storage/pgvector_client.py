"""
PostgreSQL client with pgvector support for warm tier storage.

Provides connection pooling and vector operations for:
- Storing document chunks with embeddings
- Semantic similarity search
- XBRL facts storage
- Filing metadata management

Environment Variables:
- POSTGRES_HOST: Database host (default: localhost)
- POSTGRES_PORT: Database port (default: 5432)
- POSTGRES_DB: Database name (default: financial_kb)
- POSTGRES_USER: Database user (default: fin)
- POSTGRES_PASSWORD: Database password (default: fin_local)
"""

import logging
import os
from contextlib import contextmanager
from typing import Any, Dict, List, Optional, Tuple
from dotenv import load_dotenv

import psycopg2
from psycopg2 import pool, sql
from psycopg2.extras import RealDictCursor, execute_batch

load_dotenv()

_LOG = logging.getLogger(__name__)

# Default embedding dimensions for sentence-transformers/all-mpnet-base-v2
DEFAULT_EMBEDDING_DIM = 768


class PostgresClient:
    """
    PostgreSQL client with connection pooling and pgvector support.

    Manages connections to the warm tier database with automatic
    reconnection and connection pooling.
    """

    def __init__(
        self,
        host: Optional[str] = None,
        port: Optional[int] = None,
        database: Optional[str] = None,
        user: Optional[str] = None,
        password: Optional[str] = None,
        min_connections: int = 1,
        max_connections: int = 10,
    ):
        """
        Initialize PostgreSQL client with connection pool.

        Args:
            host: Database host (default: POSTGRES_HOST env var or localhost)
            port: Database port (default: POSTGRES_PORT env var or 5432)
            database: Database name (default: POSTGRES_DB env var or financial_kb)
            user: Database user (default: POSTGRES_USER env var or fin)
            password: Database password (default: POSTGRES_PASSWORD env var)
            min_connections: Minimum connections in pool
            max_connections: Maximum connections in pool
        """
        self.host = host or os.getenv("POSTGRES_HOST", "localhost")
        self.port = port or int(os.getenv("POSTGRES_PORT", "5432"))
        self.database = database or os.getenv("POSTGRES_DB", "financial_kb")
        self.user = user or os.getenv("POSTGRES_USER", "fin")
        self.password = password or os.getenv("POSTGRES_PASSWORD", "fin_local")

        self._pool: Optional[pool.SimpleConnectionPool] = None
        self._min_connections = min_connections
        self._max_connections = max_connections

    def _get_pool(self) -> pool.SimpleConnectionPool:
        """Get or create connection pool."""
        if self._pool is None:
            self._pool = pool.SimpleConnectionPool(
                minconn=self._min_connections,
                maxconn=self._max_connections,
                host=self.host,
                port=self.port,
                database=self.database,
                user=self.user,
                password=self.password,
            )
            _LOG.info(
                "PostgreSQL connection pool created: min=%d, max=%d",
                self._min_connections,
                self._max_connections,
            )
        return self._pool

    @contextmanager
    def get_connection(self):
        """
        Context manager for database connections.

        Yields:
            psycopg2 connection object

        Example:
            with client.get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT 1")
        """
        conn = None
        try:
            conn = self._get_pool().getconn()
            yield conn
        finally:
            if conn:
                self._get_pool().putconn(conn)

    @contextmanager
    def get_cursor(self, cursor_factory=RealDictCursor):
        """
        Context manager for database cursors with automatic commit/rollback.

        Args:
            cursor_factory: Cursor class to use (default: RealDictCursor)

        Yields:
            psycopg2 cursor object
        """
        with self.get_connection() as conn:
            cursor = conn.cursor(cursor_factory=cursor_factory)
            try:
                yield cursor
                conn.commit()
            except Exception:
                conn.rollback()
                raise
            finally:
                cursor.close()

    def ping(self) -> bool:
        """
        Test connection to PostgreSQL server.

        Returns:
            True if connection successful
        """
        try:
            with self.get_cursor() as cur:
                cur.execute("SELECT 1")
                result = cur.fetchone()
                return result is not None
        except psycopg2.OperationalError as e:
            _LOG.error("PostgreSQL connection failed: %s", e)
            return False

    def execute_many(
        self,
        query: str,
        params_list: List[Tuple],
        batch_size: int = 100,
    ) -> int:
        """
        Execute a query with multiple parameter sets using batch operations.

        Args:
            query: SQL query with placeholders
            params_list: List of parameter tuples
            batch_size: Number of rows per batch

        Returns:
            Number of rows inserted/updated
        """
        count = 0
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                for i in range(0, len(params_list), batch_size):
                    batch = params_list[i : i + batch_size]
                    execute_batch(cur, query, batch)
                    count += len(batch)
            conn.commit()
        return count

    # -------------------------------------------------------------------------
    # Vector Operations
    # -------------------------------------------------------------------------

    def insert_embedding(
        self,
        table: str,
        chunk_id: str,
        embedding: List[float],
        extra_columns: Optional[Dict[str, Any]] = None,
    ) -> bool:
        """
        Insert a chunk with its vector embedding.

        Args:
            table: Target table name (e.g., "chunks")
            chunk_id: Unique chunk identifier
            embedding: Vector embedding as list of floats
            extra_columns: Additional column values

        Returns:
            True if successful
        """
        columns = ["id", "embedding"]
        values = [chunk_id, psycopg2.extensions.adapt(embedding).getquoted().decode()]

        if extra_columns:
            for key, value in extra_columns.items():
                columns.append(key)
                values.append(value)

        columns_sql = sql.SQL(", ").join(sql.Identifier(col) for col in columns)
        placeholders = sql.SQL(", ").join(sql.Placeholder() for _ in values)

        query = sql.SQL("INSERT INTO {table} ({columns}) VALUES ({placeholders})")
        query = query.format(
            table=sql.Identifier(table),
            columns=columns_sql,
            placeholders=placeholders,
        )

        try:
            with self.get_cursor() as cur:
                cur.execute(query, values)
            return True
        except psycopg2.Error as e:
            _LOG.error("Failed to insert embedding: %s", e)
            return False

    def search_similar(
        self,
        query_embedding: List[float],
        table: str = "chunks",
        limit: int = 10,
        threshold: float = 0.5,
        ticker_filter: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Search for similar chunks using vector similarity.

        Uses pgvector's cosine distance (<=>) for similarity search.

        Args:
            query_embedding: Query vector as list of floats
            table: Table to search (default: chunks)
            limit: Maximum results to return
            threshold: Minimum similarity threshold (0-1)
            ticker_filter: Optional ticker symbol to filter by

        Returns:
            List of matching chunks with metadata and similarity scores
        """
        embedding_sql = psycopg2.extensions.adapt(query_embedding).getquoted().decode()

        if ticker_filter:
            query = f"""
                SELECT
                    c.id,
                    c.filing_id,
                    c.text,
                    c.section,
                    c.chunk_index,
                    1 - (c.embedding <=> %s::vector) AS similarity,
                    f.ticker,
                    f.filing_type,
                    f.filing_date,
                    f.company_name
                FROM {table} c
                JOIN filings f ON c.filing_id = f.id
                WHERE 1 - (c.embedding <=> %s::vector) > %s
                  AND f.ticker = %s
                ORDER BY c.embedding <=> %s::vector
                LIMIT %s
            """
            params = [
                embedding_sql,
                embedding_sql,
                threshold,
                ticker_filter,
                embedding_sql,
                limit,
            ]
        else:
            query = f"""
                SELECT
                    c.id,
                    c.filing_id,
                    c.text,
                    c.section,
                    c.chunk_index,
                    1 - (c.embedding <=> %s::vector) AS similarity,
                    f.ticker,
                    f.filing_type,
                    f.filing_date,
                    f.company_name
                FROM {table} c
                JOIN filings f ON c.filing_id = f.id
                WHERE 1 - (c.embedding <=> %s::vector) > %s
                ORDER BY c.embedding <=> %s::vector
                LIMIT %s
            """
            params = [embedding_sql, embedding_sql, threshold, embedding_sql, limit]

        try:
            with self.get_cursor() as cur:
                cur.execute(query, params)
                results = cur.fetchall()
                return [dict(row) for row in results]
        except psycopg2.Error as e:
            _LOG.error("Vector search failed: %s", e)
            return []

    # -------------------------------------------------------------------------
    # Filing Operations
    # -------------------------------------------------------------------------

    def insert_filing(self, filing_data: Dict[str, Any]) -> Optional[str]:
        """
        Insert a filing record.

        Args:
            filing_data: Dict with filing metadata

        Returns:
            Filing ID if successful, None otherwise
        """
        query = """
            INSERT INTO filings (
                id, ticker, company_name, filing_type, cik,
                accession_number, filing_date, period_of_report,
                document_url, file_size_bytes
            ) VALUES (
                %(id)s, %(ticker)s, %(company_name)s, %(filing_type)s,
                %(cik)s, %(accession_number)s, %(filing_date)s,
                %(period_of_report)s, %(document_url)s, %(file_size_bytes)s
            )
            ON CONFLICT (id) DO UPDATE SET
                updated_at = CURRENT_TIMESTAMP,
                ticker = EXCLUDED.ticker,
                company_name = EXCLUDED.company_name,
                filing_type = EXCLUDED.filing_type
            RETURNING id
        """
        try:
            with self.get_cursor() as cur:
                cur.execute(query, filing_data)
                result = cur.fetchone()
                return result["id"] if result else None
        except psycopg2.Error as e:
            _LOG.error("Failed to insert filing: %s", e)
            return None

    def get_filing(self, filing_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a filing by ID.

        Args:
            filing_id: Filing identifier

        Returns:
            Filing data dict or None
        """
        query = "SELECT * FROM filings WHERE id = %s"
        try:
            with self.get_cursor() as cur:
                cur.execute(query, [filing_id])
                result = cur.fetchone()
                return dict(result) if result else None
        except psycopg2.Error as e:
            _LOG.error("Failed to get filing: %s", e)
            return None

    def get_filings_by_ticker(
        self,
        ticker: str,
        filing_types: Optional[List[str]] = None,
        limit: int = 10,
    ) -> List[Dict[str, Any]]:
        """
        Get filings for a ticker.

        Args:
            ticker: Stock ticker symbol
            filing_types: Optional list of filing types to filter
            limit: Maximum results

        Returns:
            List of filing records
        """
        if filing_types:
            placeholders = ", ".join(["%s"] * len(filing_types))
            query = f"""
                SELECT * FROM filings
                WHERE ticker = %s AND filing_type IN ({placeholders})
                ORDER BY filing_date DESC
                LIMIT %s
            """
            params = [ticker] + filing_types + [limit]
        else:
            query = """
                SELECT * FROM filings
                WHERE ticker = %s
                ORDER BY filing_date DESC
                LIMIT %s
            """
            params = [ticker, limit]

        try:
            with self.get_cursor() as cur:
                cur.execute(query, params)
                return [dict(row) for row in cur.fetchall()]
        except psycopg2.Error as e:
            _LOG.error("Failed to get filings: %s", e)
            return []

    # -------------------------------------------------------------------------
    # Chunk Operations
    # -------------------------------------------------------------------------

    def insert_chunks(self, chunks: List[Dict[str, Any]]) -> int:
        """
        Insert multiple chunks with embeddings.

        Args:
            chunks: List of chunk dicts with keys:
                - id, filing_id, chunk_index, text, section, embedding

        Returns:
            Number of chunks inserted
        """
        if not chunks:
            return 0

        query = """
            INSERT INTO chunks (
                id, filing_id, chunk_index, text, section, embedding
            ) VALUES (
                %(id)s, %(filing_id)s, %(chunk_index)s, %(text)s,
                %(section)s, %(embedding)s
            )
            ON CONFLICT (id) DO UPDATE SET
                text = EXCLUDED.text,
                section = EXCLUDED.section,
                embedding = EXCLUDED.embedding,
                updated_at = CURRENT_TIMESTAMP
        """

        # Convert embeddings to pgvector format (strip ARRAY prefix)
        for chunk in chunks:
            if "embedding" in chunk and isinstance(chunk["embedding"], list):
                embedding_str = (
                    psycopg2.extensions.adapt(chunk["embedding"]).getquoted().decode()
                )
                # pgvector expects '[...]' not 'ARRAY[...]'.
                if embedding_str.startswith("ARRAY["):
                    embedding_str = embedding_str[5:]  # Remove "ARRAY" prefix
                chunk["embedding"] = embedding_str

        count = 0
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                for chunk in chunks:
                    try:
                        cur.execute(query, chunk)
                        count += 1
                    except psycopg2.Error as e:
                        _LOG.error("Failed to insert chunk %s: %s", chunk.get("id"), e)
            conn.commit()
        return count

    def insert_filings(self, rows: list[dict]) -> int:
        """INSERT INTO filings ON CONFLICT (id) DO NOTHING."""
        if not rows:
            return 0
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.executemany(
                    """
                    INSERT INTO filings
                    (id, ticker, company_name, filing_type, cik,
                    accession_number, filing_date, period_of_report,
                    document_url, file_size_bytes)
                    VALUES
                    (%(id)s, %(ticker)s, %(company_name)s, %(filing_type)s,
                    %(cik)s, %(accession_number)s, %(filing_date)s,
                    %(period_of_report)s, %(document_url)s, %(file_size_bytes)s)
                    ON CONFLICT (id) DO NOTHING
                    """,
                    rows,
                )
            conn.commit()
        return len(rows)

    def insert_document_metadata(self, rows: list[dict]) -> int:
        """INSERT INTO document_metadata ON CONFLICT (id) DO NOTHING."""
        if not rows:
            return 0
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.executemany(
                    """
                    INSERT INTO document_metadata (id, chunk_id, key, value)
                    VALUES (%(id)s, %(chunk_id)s, %(key)s, %(value)s)
                    ON CONFLICT (id) DO NOTHING
                    """,
                    rows,
                )
            conn.commit()
        return len(rows)

    def get_chunks_by_filing(
        self,
        filing_id: str,
        include_embedding: bool = False,
    ) -> List[Dict[str, Any]]:
        """
        Get all chunks for a filing.

        Args:
            filing_id: Filing identifier
            include_embedding: Whether to include embedding vectors

        Returns:
            List of chunk records
        """
        columns = ["id", "filing_id", "chunk_index", "text", "section"]
        if include_embedding:
            columns.append("embedding")

        query = f"""
            SELECT {", ".join(columns)}
            FROM chunks
            WHERE filing_id = %s
            ORDER BY chunk_index
        """

        try:
            with self.get_cursor() as cur:
                cur.execute(query, [filing_id])
                return [dict(row) for row in cur.fetchall()]
        except psycopg2.Error as e:
            _LOG.error("Failed to get chunks: %s", e)
            return []

    # -------------------------------------------------------------------------
    # XBRL Facts Operations
    # -------------------------------------------------------------------------

    def insert_xbrl_facts(self, facts: List[Dict[str, Any]]) -> int:
        """
        Insert multiple XBRL facts.

        Args:
            facts: List of fact dicts with keys:
                - id, filing_id, concept_name, value, value_numeric,
                  unit, period_start, period_end, instant_date, axis, member

        Returns:
            Number of facts inserted
        """
        if not facts:
            return 0

        query = """
            INSERT INTO xbrl_facts (
                id, filing_id, concept_name, value, value_numeric,
                unit, period_start, period_end, instant_date, axis, member
            ) VALUES (
                %(id)s, %(filing_id)s, %(concept_name)s, %(value)s,
                %(value_numeric)s, %(unit)s, %(period_start)s, %(period_end)s,
                %(instant_date)s, %(axis)s, %(member)s
            )
            ON CONFLICT (id) DO NOTHING
        """

        count = 0
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                for fact in facts:
                    try:
                        cur.execute(query, fact)
                        count += 1
                    except psycopg2.Error as e:
                        _LOG.error(
                            "Failed to insert XBRL fact %s: %s", fact.get("id"), e
                        )
            conn.commit()
        return count

    def get_xbrl_facts_by_concept(
        self,
        filing_id: str,
        concepts: List[str],
    ) -> List[Dict[str, Any]]:
        """
        Get XBRL facts for specific concepts in a filing.

        Args:
            filing_id: Filing identifier
            concepts: List of concept names to retrieve

        Returns:
            List of XBRL fact records
        """
        placeholders = ", ".join(["%s"] * len(concepts))
        query = f"""
            SELECT * FROM xbrl_facts
            WHERE filing_id = %s AND concept_name IN ({placeholders})
        """
        params = [filing_id] + concepts

        try:
            with self.get_cursor() as cur:
                cur.execute(query, params)
                return [dict(row) for row in cur.fetchall()]
        except psycopg2.Error as e:
            _LOG.error("Failed to get XBRL facts: %s", e)
            return []

    # -------------------------------------------------------------------------
    # Statistics and Maintenance
    # -------------------------------------------------------------------------

    def get_stats(self) -> Dict[str, Any]:
        """
        Get storage statistics.

        Returns:
            Dict with counts for filings, chunks, and XBRL facts
        """
        stats = {}

        queries = {
            "filings": "SELECT COUNT(*) FROM filings",
            "chunks": "SELECT COUNT(*) FROM chunks",
            "xbrl_facts": "SELECT COUNT(*) FROM xbrl_facts",
            "unique_tickers": "SELECT COUNT(DISTINCT ticker) FROM filings",
        }

        try:
            with self.get_cursor(cursor_factory=psycopg2.extensions.cursor) as cur:
                for key, query in queries.items():
                    cur.execute(query)
                    result = cur.fetchone()
                    stats[key] = result[0] if result else 0
        except psycopg2.Error as e:
            _LOG.error("Failed to get stats: %s", e)

        return stats

    def delete_filing(self, filing_id: str) -> bool:
        """
        Delete a filing and all associated data.

        Args:
            filing_id: Filing to delete

        Returns:
            True if successful
        """
        # Cascading deletes handle chunks and XBRL facts
        query = "DELETE FROM filings WHERE id = %s"
        try:
            with self.get_cursor() as cur:
                cur.execute(query, [filing_id])
            return True
        except psycopg2.Error as e:
            _LOG.error("Failed to delete filing: %s", e)
            return False

    def close(self) -> None:
        """Close all connections in the pool."""
        if self._pool:
            self._pool.closeall()
            self._pool = None
            _LOG.info("PostgreSQL connections closed")


# Global singleton instance
_postgres_client: Optional[PostgresClient] = None


def get_postgres_client() -> PostgresClient:
    """
    Get the singleton PostgreSQL client instance.

    Returns:
        PostgresClient instance
    """
    global _postgres_client
    if _postgres_client is None:
        _postgres_client = PostgresClient()
        if _postgres_client.ping():
            _LOG.info(
                "Connected to PostgreSQL at %s:%d/%s",
                _postgres_client.host,
                _postgres_client.port,
                _postgres_client.database,
            )
        else:
            _LOG.warning("PostgreSQL connection test failed")
    return _postgres_client
