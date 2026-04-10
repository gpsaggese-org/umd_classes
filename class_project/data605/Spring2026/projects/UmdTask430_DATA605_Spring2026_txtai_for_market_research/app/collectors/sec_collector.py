"""
SEC EDGAR collector for filings.

Fetches 10-K, 8-K, and DEF 14A filings via the SEC's public API
and stores across all storage tiers.

Reference: https://www.sec.gov/search-filings/edgar-full-text-search-api
"""

import logging
import os
from datetime import datetime
from typing import Optional

import httpx

from app.collectors.base_collector import BaseCollector

_LOG = logging.getLogger(__name__)

# SEC requires a User-Agent with company email
DEFAULT_USER_AGENT = "txtai-market-research (your@email.com)"


class SECCollector(BaseCollector):
    """
    Collector for SEC EDGAR filings.

    Stores:
    - Cold: Raw filing HTML/XML in MinIO
    - Warm: Filing metadata and chunks in PostgreSQL
    - Search: Embedded chunks in txtai
    - Hot: Fetch cache in KeyDB
    """

    def _get_source_tag(self) -> str:
        return "sec"

    def _fetch_data(
        self,
        ticker: str,
        filing_types: Optional[list[str]] = None,
        limit: int = 20,
    ) -> list[dict]:
        """
        Fetch SEC filings for a given ticker.

        Args:
            ticker: Stock ticker symbol
            filing_types: List of filing types (default: ["10-K", "8-K", "DEF 14A"])
            limit: Maximum number of filings to return

        Returns:
            List of dicts with text and metadata
        """
        if filing_types is None:
            filing_types = ["10-K", "8-K", "DEF 14A"]

        filings = []

        for filing_type in filing_types:
            fetched = self._fetch_filing_type(ticker, filing_type, limit // len(filing_types))
            filings.extend(fetched)

        # Sort by date, newest first
        filings.sort(
            key=lambda x: x["metadata"].get("filing_date", ""),
            reverse=True,
        )

        return filings[:limit]

    def _fetch_filing_type(
        self,
        ticker: str,
        filing_type: str,
        limit: int,
    ) -> list[dict]:
        """Fetch a specific filing type from SEC EDGAR."""
        url = "https://efts.sec.gov/LATEST/search-index"

        # Build query: search for ticker in specific filing type
        query = f'(cikOrName:"{ticker}" OR ticker:"{ticker}") AND formType:"{filing_type}"'

        params = {
            "keys": "formType,companyName,fileNumber,items,filedAt,displayNames,description",
            "q": query,
            "from": 0,
            "size": min(limit, 100),
            "sort": "filedAt:desc",
        }

        headers = {
            "User-Agent": os.getenv("SEC_USER_AGENT", DEFAULT_USER_AGENT),
            "Accept": "application/json",
        }

        try:
            with httpx.Client(timeout=10.0) as client:
                response = client.get(url, params=params, headers=headers)
                response.raise_for_status()
                data = response.json()

            filings = []
            for item in data.get("hits", []):
                source = item.get("_source", {})
                filing_date = source.get("filedAt", "")[:10] if source.get("filedAt") else ""

                # Build search text from available fields
                text_parts = [
                    source.get("companyName", ""),
                    source.get("formType", ""),
                    source.get("description", ""),
                    source.get("displayNames", ""),
                    self._items_to_text(source.get("items", [])),
                ]
                text = " ".join(filter(None, text_parts))

                if text:
                    filings.append({
                        "text": text,
                        "metadata": {
                            "company_name": source.get("companyName", ""),
                            "form_type": source.get("formType", ""),
                            "file_number": source.get("fileNumber", ""),
                            "filing_date": filing_date,
                            "items": source.get("items", []),
                            "description": source.get("description", ""),
                            "accession_number": item.get("_id", ""),
                        },
                    })

            return filings

        except httpx.HTTPError as e:
            _LOG.error("SEC EDGAR error for %s: %s", filing_type, e)
            return []

    def _items_to_text(self, items: Optional[list]) -> str:
        """Convert SEC items list to searchable text."""
        if not items:
            return ""
        return " ".join(items)

    def collect(
        self,
        ticker: str,
        filing_types: Optional[list[str]] = None,
        limit: int = 20,
        store_cold: bool = True,
        store_warm: bool = True,
        store_search: bool = True,
        use_cache: bool = False,
    ) -> dict[str, int]:
        """
        Run the full SEC collection pipeline.

        Args:
            ticker: Stock ticker symbol
            filing_types: List of filing types to fetch
            limit: Maximum number of filings
            store_cold: Store raw filings in MinIO
            store_warm: Store structured data in PostgreSQL
            store_search: Index in txtai for semantic search
            use_cache: Use cached results if available

        Returns:
            Dict with counts: {'fetched', 'stored_cold', 'stored_warm', 'indexed'}
        """
        if filing_types is None:
            filing_types = ["10-K", "8-K", "DEF 14A"]

        return super().collect(
            ticker=ticker,
            filing_types=filing_types,
            limit=limit,
            store_cold=store_cold,
            store_warm=store_warm,
            store_search=store_search,
            use_cache=use_cache,
        )
