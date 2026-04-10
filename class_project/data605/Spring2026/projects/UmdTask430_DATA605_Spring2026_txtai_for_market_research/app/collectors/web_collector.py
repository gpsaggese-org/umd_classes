"""
Web collector for investor relations pages and press releases.

Uses httpx + BeautifulSoup to scrape:
- Company investor relations pages
- Press release archives
- Financial news sites

Stores across all storage tiers.
"""

import logging
import os
import re
from typing import Optional
from urllib.parse import urljoin

import httpx
from bs4 import BeautifulSoup

from app.collectors.base_collector import BaseCollector

_LOG = logging.getLogger(__name__)

# Common investor relations URL patterns
IR_PATHS = [
    "investors",
    "investor-relations",
    "investor",
    "ir",
]

# Common press release patterns
PRESS_RELEASE_PATHS = [
    "press-releases",
    "news-releases",
    "news",
    "press",
    "releases",
]


class WebCollector(BaseCollector):
    """
    Collector for web-scraped content.

    Stores:
    - Cold: Scraped HTML in MinIO
    - Warm: Metadata in PostgreSQL
    - Search: Embedded chunks in txtai
    - Hot: Fetch cache in KeyDB
    """

    def _get_source_tag(self) -> str:
        return "web"

    def _fetch_data(
        self,
        ticker: str,
        limit: int = 20,
    ) -> list[dict]:
        """
        Scrape web content for a given ticker.

        Args:
            ticker: Stock ticker symbol
            limit: Maximum number of documents to return

        Returns:
            List of dicts with text and metadata
        """
        company_name = self._ticker_to_company_name(ticker)
        ir_url = self._find_ir_url(company_name)

        if not ir_url:
            return []

        press_releases = self._scrape_press_releases(ir_url, limit)
        return press_releases

    def _ticker_to_company_name(self, ticker: str) -> str:
        """Convert ticker to company name for searching."""
        mapping = {
            "AAPL": "Apple",
            "MSFT": "Microsoft",
            "GOOGL": "Google",
            "AMZN": "Amazon",
            "META": "Meta",
            "TSLA": "Tesla",
            "NVDA": "NVIDIA",
            "JPM": "JPMorgan",
            "V": "Visa",
            "WMT": "Walmart",
        }
        return mapping.get(ticker.upper(), ticker)

    def _find_ir_url(self, company_name: str) -> Optional[str]:
        """Find a company's investor relations URL."""
        company_domain = f"{company_name.lower()}.com"

        # Try to find the actual IR page
        for path in IR_PATHS:
            candidate = f"https://{company_domain}/{path}"
            if self._url_exists(candidate):
                return candidate

        # Fallback: try to scrape from known financial sites
        return self._search_for_ir_page(company_name)

    def _url_exists(self, url: str) -> bool:
        """Check if a URL exists."""
        try:
            with httpx.Client(timeout=5.0) as client:
                response = client.head(url)
                return response.status_code == 200
        except httpx.HTTPError:
            return False

    def _search_for_ir_page(self, company_name: str) -> Optional[str]:
        """Search for a company's IR page."""
        query = f"{company_name} investor relations site:{company_name.lower()}.com"
        search_url = "https://html.duckduckgo.com/html"

        headers = {
            "User-Agent": "Mozilla/5.0 (compatible; txtai-bot/1.0)",
        }

        data = {"q": query}

        try:
            with httpx.Client(timeout=10.0) as client:
                response = client.post(search_url, headers=headers, data=data)
                soup = BeautifulSoup(response.text, "html.parser")

            result = soup.find("a", class_="result__url")
            if result and result.get("href"):
                return result["href"]

            return None

        except httpx.HTTPError:
            return None

    def _scrape_press_releases(self, ir_url: str, limit: int) -> list[dict]:
        """Scrape press releases from an IR page."""
        press_releases = []

        try:
            with httpx.Client(timeout=10.0) as client:
                headers = {"User-Agent": "Mozilla/5.0 (compatible; txtai-bot/1.0)"}
                response = client.get(ir_url, headers=headers)
                response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")

            # Find press release links
            pr_links = []

            # Strategy 1: Find links containing press release keywords
            for link in soup.find_all("a", href=True):
                href = link.get("href", "").lower()
                text = link.get_text().lower()

                if any(kw in href for kw in PRESS_RELEASE_PATHS) or \
                   any(kw in text for kw in ["press release", "news release"]):
                    full_url = urljoin(ir_url, link["href"])
                    pr_links.append((full_url, link.get_text().strip()))

            # Strategy 2: Find press release section and scrape links
            for path in PRESS_RELEASE_PATHS:
                pr_page_url = urljoin(ir_url, path)
                try:
                    with httpx.Client(timeout=5.0) as client:
                        resp = client.get(pr_page_url)
                        if resp.status_code == 200:
                            pr_soup = BeautifulSoup(resp.text, "html.parser")
                            for link in pr_soup.find_all("a", href=True):
                                full_url = urljoin(pr_page_url, link["href"])
                                pr_links.append((full_url, link.get_text().strip()))
                except httpx.HTTPError:
                    continue

            # Deduplicate and limit
            seen = set()
            unique_links = []
            for url, title in pr_links:
                if url not in seen:
                    seen.add(url)
                    unique_links.append((url, title))

            # Fetch individual press releases
            for url, title in unique_links[:limit]:
                content = self._fetch_page_content(url)
                if content:
                    press_releases.append({
                        "text": f"{title}\n{content}",
                        "metadata": {
                            "title": title,
                            "url": url,
                            "source": "web_scrape",
                        },
                    })

        except httpx.HTTPError as e:
            _LOG.error("Error scraping IR page: %s", e)

        return press_releases

    def _fetch_page_content(self, url: str) -> Optional[str]:
        """Fetch and extract main content from a page."""
        try:
            with httpx.Client(timeout=10.0) as client:
                headers = {"User-Agent": "Mozilla/5.0 (compatible; txtai-bot/1.0)"}
                response = client.get(url, headers=headers)
                response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")

            # Remove script, style, nav elements
            for element in soup(["script", "style", "nav", "header", "footer"]):
                element.decompose()

            # Get main content
            main = soup.find("article") or soup.find("main") or soup.find("div", class_="content")

            if main:
                text = main.get_text(separator="\n")
            else:
                text = soup.get_text(separator="\n")

            # Clean up whitespace
            text = re.sub(r"\n\s*\n", "\n\n", text)
            text = text.strip()

            return text[:5000]  # Limit content length

        except httpx.HTTPError:
            return None

    def collect(
        self,
        ticker: str,
        limit: int = 20,
        store_cold: bool = True,
        store_warm: bool = True,
        store_search: bool = True,
        use_cache: bool = False,
    ) -> dict[str, int]:
        """
        Run the full web collection pipeline.

        Args:
            ticker: Stock ticker symbol
            limit: Maximum documents
            store_cold: Store in MinIO
            store_warm: Store in PostgreSQL
            store_search: Index in txtai
            use_cache: Use cached results

        Returns:
            Dict with counts
        """
        return super().collect(
            ticker=ticker,
            limit=limit,
            store_cold=store_cold,
            store_warm=store_warm,
            store_search=store_search,
            use_cache=use_cache,
        )
