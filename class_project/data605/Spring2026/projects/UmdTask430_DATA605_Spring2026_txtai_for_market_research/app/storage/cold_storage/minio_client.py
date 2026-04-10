"""
MinIO client for cold tier storage.

Provides object storage operations for archiving raw documents:
- SEC filings (original HTML/XML)
- News articles (HTML snapshots)
- Web scraped content
- Social media snapshots

Environment Variables:
    MINIO_ENDPOINT: MinIO server endpoint (default: localhost:9000)
    MINIO_ACCESS_KEY: Access key (default: minioadmin)
    MINIO_SECRET_KEY: Secret key (default: minioadmin)
    MINIO_SECURE: Use HTTPS (default: false)

Bucket Structure:
    sec/{ticker}/{filing_type}/{accession_number}.html
    news/{ticker}/{date}/{article_id}.html
    web/{ticker}/{domain}/{url_hash}.html
    social/{platform}/{ticker}/{post_id}.json
"""

import hashlib
import io
import json
import logging
import os
from datetime import datetime
from typing import Any, Optional

from minio import Minio
from minio.error import S3Error

_LOG = logging.getLogger(__name__)


class MinIOClient:
    """
    MinIO client for cold tier object storage.

    Manages bucket creation and object operations with automatic
    retry and error handling.
    """

    def __init__(
        self,
        endpoint: Optional[str] = None,
        access_key: Optional[str] = None,
        secret_key: Optional[str] = None,
        secure: bool = False,
    ):
        """
        Initialize MinIO client.

        Args:
            endpoint: MinIO server endpoint (default: MINIO_ENDPOINT env var or localhost:9000)
            access_key: Access key (default: MINIO_ACCESS_KEY env var or minioadmin)
            secret_key: Secret key (default: MINIO_SECRET_KEY env var or minioadmin)
            secure: Use HTTPS (default: False)
        """
        self.endpoint = endpoint or os.getenv("MINIO_ENDPOINT", "localhost:9000")
        self.access_key = access_key or os.getenv("MINIO_ACCESS_KEY", "minioadmin")
        self.secret_key = secret_key or os.getenv("MINIO_SECRET_KEY", "minioadmin")
        self.secure = secure

        self._client: Optional[Minio] = None
        self._buckets_created: set[str] = set()

    def _get_client(self) -> Minio:
        """Get or create Minio client."""
        if self._client is None:
            self._client = Minio(
                self.endpoint,
                access_key=self.access_key,
                secret_key=self.secret_key,
                secure=self.secure,
            )
            _LOG.info("MinIO client created for endpoint: %s", self.endpoint)
        return self._client

    def ping(self) -> bool:
        """
        Test connection to MinIO server.

        Returns:
            True if connection successful
        """
        try:
            client = self._get_client()
            # List buckets to test connection
            list(client.list_buckets())
            return True
        except S3Error as e:
            _LOG.error("MinIO connection failed: %s", e)
            return False

    def create_bucket(self, bucket_name: str) -> bool:
        """
        Create a bucket if it doesn't exist.

        Args:
            bucket_name: Name of the bucket to create

        Returns:
            True if bucket exists or was created successfully
        """
        client = self._get_client()

        if bucket_name in self._buckets_created:
            return True

        try:
            if not client.bucket_exists(bucket_name):
                client.make_bucket(bucket_name)
                _LOG.info("Bucket '%s' created", bucket_name)
            self._buckets_created.add(bucket_name)
            return True
        except S3Error as e:
            _LOG.error("Failed to create bucket '%s': %s", bucket_name, e)
            return False

    def put_object(
        self,
        bucket: str,
        object_name: str,
        data: str | bytes,
        content_type: str = "application/octet-stream",
        metadata: Optional[dict[str, str]] = None,
    ) -> Optional[str]:
        """
        Upload an object to a bucket.

        Args:
            bucket: Bucket name
            object_name: Object path within bucket
            data: Data to upload (string or bytes)
            content_type: MIME type of the content
            metadata: Optional metadata headers

        Returns:
            ETag of the uploaded object, or None on failure
        """
        client = self._get_client()

        # Ensure bucket exists
        if not self.create_bucket(bucket):
            return None

        # Convert string to bytes
        if isinstance(data, str):
            data = data.encode("utf-8")

        try:
            # Wrap data in BytesIO for compatibility with minio API
            data_stream = io.BytesIO(data)
            result = client.put_object(
                bucket,
                object_name,
                data_stream,
                length=len(data),
                content_type=content_type,
                metadata=metadata,
            )
            _LOG.debug("Uploaded '%s/%s' (%d bytes)", bucket, object_name, len(data))
            return result.etag
        except S3Error as e:
            _LOG.error("Failed to upload '%s/%s': %s", bucket, object_name, e)
            return None

    def get_object(self, bucket: str, object_name: str) -> Optional[bytes]:
        """
        Download an object from a bucket.

        Args:
            bucket: Bucket name
            object_name: Object path within bucket

        Returns:
            Object content as bytes, or None on failure
        """
        client = self._get_client()

        try:
            response = client.get_object(bucket, object_name)
            data = response.read()
            response.close()
            response.release_conn()
            return data
        except S3Error as e:
            _LOG.error("Failed to get '%s/%s': %s", bucket, object_name, e)
            return None

    def get_object_as_string(self, bucket: str, object_name: str) -> Optional[str]:
        """
        Download an object and return as string.

        Args:
            bucket: Bucket name
            object_name: Object path within bucket

        Returns:
            Object content as string, or None on failure
        """
        data = self.get_object(bucket, object_name)
        if data:
            return data.decode("utf-8")
        return None

    def delete_object(self, bucket: str, object_name: str) -> bool:
        """
        Delete an object from a bucket.

        Args:
            bucket: Bucket name
            object_name: Object path within bucket

        Returns:
            True if deleted successfully
        """
        client = self._get_client()

        try:
            client.remove_object(bucket, object_name)
            _LOG.debug("Deleted '%s/%s'", bucket, object_name)
            return True
        except S3Error as e:
            _LOG.error("Failed to delete '%s/%s': %s", bucket, object_name, e)
            return False

    def list_objects(
        self,
        bucket: str,
        prefix: str = "",
        recursive: bool = True,
    ) -> list[str]:
        """
        List objects in a bucket.

        Args:
            bucket: Bucket name
            prefix: Optional prefix to filter objects
            recursive: Whether to list recursively

        Returns:
            List of object names
        """
        client = self._get_client()
        objects = []

        try:
            for obj in client.list_objects(bucket, prefix=prefix, recursive=recursive):
                objects.append(obj.object_name)
        except S3Error as e:
            _LOG.error("Failed to list objects in '%s': %s", bucket, e)

        return objects

    def object_exists(self, bucket: str, object_name: str) -> bool:
        """
        Check if an object exists in a bucket.

        Args:
            bucket: Bucket name
            object_name: Object path within bucket

        Returns:
            True if object exists
        """
        client = self._get_client()

        try:
            client.stat_object(bucket, object_name)
            return True
        except S3Error as e:
            if e.code == "NoSuchKey":
                return False
            _LOG.error("Failed to check object '%s/%s': %s", bucket, object_name, e)
            return False

    def put_json(
        self,
        bucket: str,
        object_name: str,
        data: dict[str, Any],
    ) -> Optional[str]:
        """
        Upload JSON data to a bucket.

        Args:
            bucket: Bucket name
            object_name: Object path within bucket
            data: Dictionary to serialize and upload

        Returns:
            ETag of the uploaded object, or None on failure
        """
        json_str = json.dumps(data, indent=2, default=str)
        return self.put_object(
            bucket,
            object_name,
            json_str,
            content_type="application/json",
        )

    def get_json(self, bucket: str, object_name: str) -> Optional[dict[str, Any]]:
        """
        Download and parse JSON from a bucket.

        Args:
            bucket: Bucket name
            object_name: Object path within bucket

        Returns:
            Parsed JSON as dict, or None on failure
        """
        json_str = self.get_object_as_string(bucket, object_name)
        if json_str:
            try:
                return json.loads(json_str)
            except json.JSONDecodeError as e:
                _LOG.error("Failed to parse JSON from '%s/%s': %s", bucket, object_name, e)
        return None

    # -------------------------------------------------------------------------
    # Convenience Methods for Document Storage
    # -------------------------------------------------------------------------

    def store_sec_filing(
        self,
        ticker: str,
        filing_type: str,
        accession_number: str,
        content: str | bytes,
        metadata: Optional[dict[str, Any]] = None,
    ) -> Optional[str]:
        """
        Store a SEC filing in cold storage.

        Args:
            ticker: Stock ticker symbol
            filing_type: Form type (e.g., "10-K", "8-K")
            accession_number: SEC accession number
            content: Filing content (HTML/XML text or bytes)
            metadata: Optional metadata to store alongside

        Returns:
            Object path if successful
        """
        # Normalize accession number (remove dashes for filename)
        filename = accession_number.replace("-", "")
        object_name = f"sec/{ticker}/{filing_type}/{filename}.html"

        etag = self.put_object(
            "filings",
            object_name,
            content,
            content_type="text/html",
        )

        if etag and metadata:
            # Store metadata as separate JSON
            metadata_path = f"sec/{ticker}/{filing_type}/{filename}.meta.json"
            self.put_json("filings", metadata_path, metadata)

        return object_name if etag else None

    def store_news_article(
        self,
        ticker: str,
        url: str,
        content: str,
        metadata: dict[str, Any],
    ) -> Optional[str]:
        """
        Store a news article in cold storage.

        Args:
            ticker: Stock ticker symbol
            url: Article URL
            content: Article HTML or text content
            metadata: Article metadata

        Returns:
            Object path if successful
        """
        # Generate deterministic filename from URL
        url_hash = hashlib.md5(url.encode()).hexdigest()[:12]
        date = metadata.get("published_at", datetime.utcnow().isoformat())[:10]
        object_name = f"news/{ticker}/{date}/{url_hash}.html"

        etag = self.put_object(
            "articles",
            object_name,
            content,
            content_type="text/html",
        )

        if etag:
            # Store metadata as separate JSON
            metadata_path = f"news/{ticker}/{date}/{url_hash}.meta.json"
            self.put_json("articles", metadata_path, metadata)

        return object_name if etag else None

    def store_web_content(
        self,
        ticker: str,
        url: str,
        content: str | bytes,
        metadata: Optional[dict[str, Any]] = None,
    ) -> Optional[str]:
        """
        Store scraped web content in cold storage.

        Args:
            ticker: Stock ticker symbol
            url: Source URL
            content: Scraped content
            metadata: Optional metadata

        Returns:
            Object path if successful
        """
        url_hash = hashlib.md5(url.encode()).hexdigest()[:12]
        object_name = f"web/{ticker}/{url_hash}.html"

        etag = self.put_object(
            "web_scrapes",
            object_name,
            content,
            content_type="text/html",
        )

        if etag and metadata:
            metadata_path = f"web/{ticker}/{url_hash}.meta.json"
            self.put_json("web_scrapes", metadata_path, metadata)

        return object_name if etag else None

    def store_social_post(
        self,
        platform: str,
        ticker: str,
        post_id: str,
        content: dict[str, Any],
    ) -> Optional[str]:
        """
        Store a social media post in cold storage.

        Args:
            platform: Platform name (reddit, stocktwits, twitter)
            ticker: Stock ticker symbol
            post_id: Platform-specific post ID
            content: Full post data as dict

        Returns:
            Object path if successful
        """
        object_name = f"social/{platform}/{ticker}/{post_id}.json"

        etag = self.put_json("social", object_name, content)
        return object_name if etag else None

    def close(self) -> None:
        """Close MinIO client connections."""
        self._client = None
        self._buckets_created.clear()
        _LOG.info("MinIO client closed")


# Global singleton instance
_minio_client: Optional[MinIOClient] = None


def get_minio_client() -> MinIOClient:
    """
    Get the singleton MinIO client instance.

    Returns:
        MinIOClient instance
    """
    global _minio_client
    if _minio_client is None:
        _minio_client = MinIOClient()
        if _minio_client.ping():
            _LOG.info("Connected to MinIO at %s", _minio_client.endpoint)
        else:
            _LOG.warning("MinIO connection test failed")
    return _minio_client
