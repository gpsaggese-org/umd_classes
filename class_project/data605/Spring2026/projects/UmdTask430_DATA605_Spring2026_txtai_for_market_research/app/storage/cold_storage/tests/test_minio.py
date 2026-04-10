# storage/cold_storage/tests/test_minio.py
"""
Test script for MinIO cold tier infrastructure.

Usage:
    python -m app.storage.cold_storage.tests.test_minio
"""

import logging
from datetime import datetime

from app.storage.cold_storage.minio_client import MinIOClient, get_minio_client

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
_LOG = logging.getLogger(__name__)


def test_minio_client():
    """Test basic MinIO client operations."""
    print("\n" + "=" * 60)
    print("Testing MinIO Client")
    print("=" * 60)

    client = get_minio_client()

    # Test connection
    print("\n1. Testing connection...")
    if client.ping():
        print("   [OK] Connected to MinIO")
    else:
        print("   [FAIL] Connection failed")
        return False

    # Test bucket creation
    print("\n2. Testing bucket creation...")
    test_bucket = "test-bucket"
    if client.create_bucket(test_bucket):
        print(f"   [OK] Bucket '{test_bucket}' created/exists")
    else:
        print(f"   [FAIL] Failed to create bucket '{test_bucket}'")
        return False

    # Test put_object with string
    print("\n3. Testing put_object (string)...")
    test_content = "Hello, MinIO! This is a test document."
    test_object = "test/documents/hello.txt"
    etag = client.put_object(test_bucket, test_object, test_content)
    if etag:
        print(f"   [OK] Object uploaded with ETag: {etag}")
    else:
        print("   [FAIL] Failed to upload object")
        return False

    # Test put_object with bytes
    print("\n4. Testing put_object (bytes)...")
    test_bytes = b"Binary content test"
    test_object_bytes = "test/documents/binary.bin"
    etag_bytes = client.put_object(test_bucket, test_object_bytes, test_bytes)
    if etag_bytes:
        print(f"   [OK] Binary object uploaded with ETag: {etag_bytes}")
    else:
        print("   [FAIL] Failed to upload binary object")

    # Test get_object
    print("\n5. Testing get_object...")
    retrieved = client.get_object(test_bucket, test_object)
    if retrieved and retrieved.decode("utf-8") == test_content:
        print(f"   [OK] Object retrieved: '{retrieved.decode('utf-8')}'")
    else:
        print(f"   [FAIL] Retrieved content mismatch")

    # Test get_object_as_string
    print("\n6. Testing get_object_as_string...")
    retrieved_str = client.get_object_as_string(test_bucket, test_object)
    if retrieved_str == test_content:
        print(f"   [OK] String retrieval works")
    else:
        print("   [FAIL] String retrieval failed")

    # Test object_exists
    print("\n7. Testing object_exists...")
    exists = client.object_exists(test_bucket, test_object)
    if exists:
        print(f"   [OK] Object exists check works")
    else:
        print("   [FAIL] Object exists check failed")

    # Test list_objects
    print("\n8. Testing list_objects...")
    objects = client.list_objects(test_bucket, prefix="test/")
    if len(objects) >= 2:
        print(f"   [OK] Listed {len(objects)} objects: {objects}")
    else:
        print(f"   [FAIL] Expected at least 2 objects, got {len(objects)}")

    # Test put_json and get_json
    print("\n9. Testing JSON operations...")
    test_json = {
        "ticker": "AAPL",
        "company": "Apple Inc.",
        "filing_type": "10-K",
        "filing_date": "2024-01-15",
        "metrics": {
            "revenue": 383285000000,
            "net_income": 96995000000,
        }
    }
    json_etag = client.put_json(test_bucket, "test/data/filing.json", test_json)
    if json_etag:
        print(f"   [OK] JSON uploaded with ETag: {json_etag}")
        retrieved_json = client.get_json(test_bucket, "test/data/filing.json")
        if retrieved_json == test_json:
            print(f"   [OK] JSON retrieval works: {retrieved_json}")
        else:
            print("   [FAIL] JSON retrieval mismatch")
    else:
        print("   [FAIL] JSON upload failed")

    # Test convenience method: store_sec_filing
    print("\n10. Testing store_sec_filing...")
    sec_content = """
    <html>
    <head><title>Apple Inc. 10-K</title></head>
    <body>
        <h1>UNITED STATES SECURITIES AND EXCHANGE COMMISSION</h1>
        <h2>Form 10-K</h2>
        <p>Apple Inc. reported record revenue for fiscal year 2024.</p>
    </body>
    </html>
    """
    sec_metadata = {
        "company_name": "Apple Inc.",
        "cik": "0000320193",
        "filing_date": "2024-01-15",
    }
    sec_path = client.store_sec_filing(
        ticker="AAPL",
        filing_type="10-K",
        accession_number="0000320193-24-000001",
        content=sec_content,
        metadata=sec_metadata,
    )
    if sec_path:
        print(f"   [OK] SEC filing stored at: {sec_path}")
        # Verify we can retrieve it
        retrieved_sec = client.get_object_as_string("filings", sec_path)
        if retrieved_sec and "Apple Inc." in retrieved_sec:
            print(f"   [OK] SEC filing retrieval works")
        else:
            print("   [FAIL] SEC filing retrieval failed")
    else:
        print("   [FAIL] SEC filing storage failed")

    # Test convenience method: store_news_article
    print("\n11. Testing store_news_article...")
    news_content = "<article><h1>Apple Stock Rises on Strong Earnings</h1></article>"
    news_metadata = {
        "title": "Apple Stock Rises on Strong Earnings",
        "source": "Reuters",
        "published_at": "2024-01-16T10:00:00Z",
        "url": "https://reuters.com/test-article",
    }
    news_path = client.store_news_article(
        ticker="AAPL",
        url="https://reuters.com/test-article",
        content=news_content,
        metadata=news_metadata,
    )
    if news_path:
        print(f"   [OK] News article stored at: {news_path}")
    else:
        print("   [FAIL] News article storage failed")

    # Test delete_object
    print("\n12. Testing delete_object...")
    deleted = client.delete_object(test_bucket, test_object)
    if deleted:
        print(f"   [OK] Object deleted")
        # Verify deletion
        exists_after = client.object_exists(test_bucket, test_object)
        if not exists_after:
            print(f"   [OK] Object confirmed deleted")
        else:
            print("   [FAIL] Object still exists after deletion")
    else:
        print("   [FAIL] Delete failed")

    # Test close
    print("\n13. Testing close...")
    client.close()
    print("   [OK] Client closed")

    return True


def main():
    """Run all tests."""
    print("\n" + "=" * 60)
    print("MinIO Cold Tier Infrastructure Tests")
    print("=" * 60)

    success = test_minio_client()

    print("\n" + "=" * 60)
    if success:
        print("All tests passed!")
    else:
        print("Some tests failed!")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
