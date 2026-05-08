#!/usr/bin/env python3
"""
Storage Status Check Script

Displays content statistics across all storage tiers:
- Hot Tier: KeyDB (cache, sessions, prices)
- Warm Tier: PostgreSQL (filings, chunks, XBRL facts)
- Cold Tier: MinIO (raw document archive)
- Search Tier: txtai (semantic search index)

Usage:
    python -m scripts.check_storage_status
"""

import json
import logging
import sys
from pathlib import Path

from dotenv import load_dotenv

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app.storage import get_keydb_client, get_postgres_client, get_minio_client
from app.pipeline.embeddings import get_embeddings

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
_LOG = logging.getLogger(__name__)


def check_hot_tier_keydb() -> dict:
    """Check KeyDB (hot tier) content."""
    result = {
        "status": "unknown",
        "keys": {},
        "total_keys": 0,
    }

    try:
        client = get_keydb_client()
        if not client.ping():
            result["status"] = "disconnected"
            return result

        result["status"] = "connected"

        # Count keys by pattern
        patterns = {
            "prices:*": "Price Cache",
            "cache:*": "Semantic Cache",
            "session:*": "Sessions",
            "fetch:*": "Fetch Cache",
        }

        for pattern, label in patterns.items():
            keys = list(client.scan_iter(pattern))
            result["keys"][pattern] = len(keys)
            result["total_keys"] += len(keys)

        # Get some sample keys
        all_keys = list(client.scan_iter("*", count=100))
        result["sample_keys"] = all_keys[:10]

        # Get KeyDB info
        info = client._get_client().info()
        result["memory_used"] = info.get("used_memory_human", "unknown")
        result["connected_clients"] = info.get("connected_clients", 0)

    except Exception as e:
        result["status"] = f"error: {e}"

    return result


def check_warm_tier_postgres() -> dict:
    """Check PostgreSQL (warm tier) content."""
    result = {
        "status": "unknown",
        "tables": {},
        "total_records": 0,
    }

    try:
        client = get_postgres_client()
        if not client.ping():
            result["status"] = "disconnected"
            return result

        result["status"] = "connected"

        # Get stats from each table
        queries = {
            "companies": "SELECT COUNT(*) FROM companies",
            "filings": "SELECT COUNT(*) FROM filings",
            "chunks": "SELECT COUNT(*) FROM chunks",
            "document_metadata": "SELECT COUNT(*) FROM document_metadata",
            "xbrl_facts": "SELECT COUNT(*) FROM xbrl_facts",
            "collection_runs": "SELECT COUNT(*) FROM collection_runs",
        }

        with client.get_cursor() as cur:
            for table, query in queries.items():
                try:
                    cur.execute(query)
                    count = cur.fetchone()[0]
                    result["tables"][table] = count
                    result["total_records"] += count
                except Exception as e:
                    result["tables"][table] = f"error: {e}"

        # Get filings by ticker
        try:
            cur.execute("""
                SELECT ticker, COUNT(*) as count,
                       STRING_AGG(DISTINCT filing_type, ', ') as types
                FROM filings
                GROUP BY ticker
                ORDER BY count DESC
                LIMIT 10
            """)
            result["filings_by_ticker"] = [
                {"ticker": row[0], "count": row[1], "types": row[2]}
                for row in cur.fetchall()
            ]
        except Exception:
            pass

        # Get chunks with embeddings
        try:
            cur.execute("SELECT COUNT(*) FROM chunks WHERE embedding IS NOT NULL")
            result["chunks_with_embeddings"] = cur.fetchone()[0]
        except Exception:
            pass

        # Get recent collection runs
        try:
            cur.execute("""
                SELECT collector, ticker, status, records_written, started_at
                FROM collection_runs
                ORDER BY started_at DESC
                LIMIT 5
            """)
            result["recent_runs"] = [
                {
                    "collector": row[0],
                    "ticker": row[1],
                    "status": row[2],
                    "records": row[3],
                    "started_at": str(row[4]),
                }
                for row in cur.fetchall()
            ]
        except Exception:
            pass

    except Exception as e:
        result["status"] = f"error: {e}"

    return result


def check_cold_tier_minio() -> dict:
    """Check MinIO (cold tier) content."""
    result = {
        "status": "unknown",
        "buckets": {},
        "total_objects": 0,
    }

    try:
        client = get_minio_client()
        if not client.ping():
            result["status"] = "disconnected"
            return result

        result["status"] = "connected"

        minio_client = client._get_client()

        # Check each expected bucket
        bucket_names = ["filings", "articles", "raw_docs"]

        for bucket_name in bucket_names:
            try:
                # Check if bucket exists
                exists = minio_client.bucket_exists(bucket_name)
                if not exists:
                    result["buckets"][bucket_name] = {"exists": False, "objects": 0}
                    continue

                # Count objects
                objects = list(minio_client.list_objects(bucket_name, recursive=True))
                result["buckets"][bucket_name] = {
                    "exists": True,
                    "objects": len(objects),
                }
                result["total_objects"] += len(objects)

            except Exception as e:
                result["buckets"][bucket_name] = {"exists": False, "error": str(e)}

        # Get bucket with most objects
        if result["buckets"]:
            max_bucket = max(
                [(k, v.get("objects", 0)) for k, v in result["buckets"].items()],
                key=lambda x: x[1],
                default=(None, 0),
            )
            result["largest_bucket"] = max_bucket[0]
            result["largest_bucket_count"] = max_bucket[1]

    except Exception as e:
        result["status"] = f"error: {e}"

    return result


def check_search_tier_txtai() -> dict:
    """Check txtai (search tier) content."""
    result = {
        "status": "unknown",
        "index_count": 0,
    }

    try:
        embeddings = get_embeddings()

        # Check if index exists and get count.
        try:
            # Use the public count attribute when txtai exposes it.
            if hasattr(embeddings, "index") and embeddings.index is not None:
                if hasattr(embeddings.index, "count"):
                    result["index_count"] = embeddings.index.count
                elif hasattr(embeddings.index, "__len__"):
                    result["index_count"] = len(embeddings.index)
        except Exception:
            pass

        # Check data directory
        from app.pipeline.embeddings import get_data_dir

        data_dir = get_data_dir()
        index_file = data_dir / "index.db"

        result["data_dir"] = str(data_dir)
        result["index_file_exists"] = index_file.exists()
        result["index_file_size"] = (
            index_file.stat().st_size if index_file.exists() else 0
        )

        result["status"] = "connected"

    except Exception as e:
        result["status"] = f"error: {e}"

    return result


def print_summary(hot, warm, cold, search) -> None:
    """Print formatted summary."""
    print("\n" + "=" * 70)
    print("STORAGE TIER STATUS SUMMARY")
    print("=" * 70)

    # Hot Tier
    print("\n🔥 HOT TIER (KeyDB)")
    print(f"   Status: {hot['status'].upper()}")
    if hot["status"] == "connected":
        print(f"   Total Keys: {hot['total_keys']}")
        print(f"   Memory Used: {hot.get('memory_used', 'N/A')}")
        print(f"   Connected Clients: {hot.get('connected_clients', 'N/A')}")
        for pattern, count in hot.get("keys", {}).items():
            print(f"   - {pattern}: {count}")

    # Warm Tier
    print("\n📊 WARM TIER (PostgreSQL)")
    print(f"   Status: {warm['status'].upper()}")
    if warm["status"] == "connected":
        print(f"   Total Records: {warm['total_records']}")
        for table, count in warm.get("tables", {}).items():
            print(f"   - {table}: {count}")
        if warm.get("chunks_with_embeddings"):
            print(f"   Chunks with Embeddings: {warm['chunks_with_embeddings']}")
        if warm.get("filings_by_ticker"):
            print("\n   Filings by Ticker:")
            for item in warm["filings_by_ticker"]:
                print(f"   - {item['ticker']}: {item['count']} ({item['types']})")
        if warm.get("recent_runs"):
            print("\n   Recent Collection Runs:")
            for run in warm["recent_runs"]:
                print(
                    f"   - {run['collector']} ({run['ticker']}): {run['status']} - {run['records']} records"
                )

    # Cold Tier
    print("\n❄️ COLD TIER (MinIO)")
    print(f"   Status: {cold['status'].upper()}")
    if cold["status"] == "connected":
        print(f"   Total Objects: {cold['total_objects']}")
        for bucket, info in cold.get("buckets", {}).items():
            if info.get("exists"):
                print(f"   - {bucket}: {info['objects']} objects")
            else:
                print(f"   - {bucket}: (not created)")

    # Search Tier
    print("\n🔍 SEARCH TIER (txtai)")
    print(f"   Status: {search['status'].upper()}")
    if search["status"] == "connected":
        print(f"   Index Count: {search['index_count']}")
        print(f"   Data Dir: {search['data_dir']}")
        print(
            f"   Index File: {search['index_file_exists']} ({search['index_file_size']} bytes)"
        )

    print("\n" + "=" * 70)


def main() -> int:
    """Main entry point."""
    load_dotenv()

    _LOG.info("Checking storage tiers...")

    # Check all tiers
    hot_status = check_hot_tier_keydb()
    warm_status = check_warm_tier_postgres()
    cold_status = check_cold_tier_minio()
    search_status = check_search_tier_txtai()

    # Print summary
    print_summary(hot_status, warm_status, cold_status, search_status)

    # Save detailed status
    detailed_status = {
        "timestamp": Path().stat().st_mtime,
        "hot_tier": hot_status,
        "warm_tier": warm_status,
        "cold_tier": cold_status,
        "search_tier": search_status,
    }

    status_file = Path("storage_status.json")
    with open(status_file, "w") as f:
        json.dump(detailed_status, f, indent=2, default=str)
    _LOG.info(f"Detailed status saved to {status_file}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
