"""
SEC EDGAR collector — built on official data.sec.gov APIs only.

Official API reference:
  https://www.sec.gov/search-filings/edgar-application-programming-interfaces

Endpoints used:
  CIK lookup:    https://www.sec.gov/files/company_tickers.json
  Submissions:   https://data.sec.gov/submissions/CIK{cik}.json
  Filing docs:   https://www.sec.gov/Archives/edgar/data/{cik}/{accession}/

Rate limit:  10 req/s (SEC documented max)
Concurrency: 8 parallel fetches (safely under limit with per-request delay)
"""

import asyncio
import concurrent.futures
import logging
import os
import re
import time
from typing import Any, Coroutine, Optional

import httpx

from app.collectors.base_collector import BaseCollector

_LOG = logging.getLogger(__name__)

# ── Official SEC constants ────────────────────────────────────────────────────
# User-Agent format required by SEC: "Company Name email@domain.com"
DEFAULT_USER_AGENT = os.getenv(
    "SEC_USER_AGENT",
    "txtai-market-research security-research@proton.me",
)

# SEC allows max 10 req/s; stay safely under with 8 workers + 110ms delay
SEC_RATE_LIMIT_DELAY = 0.11  # 110ms proactive throttle per request
SEC_MAX_RETRIES = 4
SEC_CONCURRENCY = 8  # semaphore cap

# Default limits for large-scale collection
DEFAULT_FILING_TYPES = ["10-K", "10-Q", "8-K", "DEF 14A", "S-1", "10-K/A", "10-Q/A"]
DEFAULT_LARGE_SCALE_LIMIT = 5000  # Default for large-scale collection

# Official API base URLs (data.sec.gov — documented public REST API)
DATA_API_BASE = "https://data.sec.gov"
SEC_BASE = "https://www.sec.gov"
SUBMISSIONS_URL = f"{DATA_API_BASE}/submissions/CIK{{cik}}.json"
COMPANY_TICKERS_URL = f"{SEC_BASE}/files/company_tickers.json"

# Required headers per SEC developer FAQ
BASE_HEADERS = {
    "User-Agent": DEFAULT_USER_AGENT,
    "Accept-Encoding": "gzip, deflate",
    "Host": "data.sec.gov",  # overridden per-request where needed
}


def _run_async(coro: Coroutine[Any, Any, Any]) -> Any:
    """
    Run an async coroutine from sync code, regardless of caller context.

    ``asyncio.run`` raises if a loop is already running (Jupyter, FastAPI
    handlers, async test harnesses). This helper transparently dispatches
    such calls to a worker thread that owns its own loop, leaving the
    parent loop untouched.

    :param coro: coroutine to execute to completion
    :return: whatever the coroutine returns
    """
    try:
        asyncio.get_running_loop()
    except RuntimeError:
        # No loop running — typical CLI / script case.
        return asyncio.run(coro)
    # A loop is already running. Spin up a worker thread that owns its own
    # loop so the running loop stays untouched.
    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
        return executor.submit(asyncio.run, coro).result()


class SECCollector(BaseCollector):
    """
    Collector for SEC EDGAR filings using the official data.sec.gov REST APIs.

    Flow per ticker:
      1. Resolve ticker → CIK  (company_tickers.json)
      2. Fetch filing history  (submissions/CIK{cik}.json, paginated)
      3. Filter by form type
      4. Concurrently fetch filing index pages → resolve primary document URL
      5. Fetch and clean primary document HTML
    """

    def _get_source_tag(self) -> str:
        return "sec"

    # ── CIK resolution ────────────────────────────────────────────────────────

    def _get_cik_for_ticker(self, ticker: str) -> Optional[str]:
        """
        Resolve ticker → zero-padded 10-digit CIK.
        Uses the official SEC company_tickers.json mapping.
        """
        try:
            with httpx.Client(
                timeout=10.0,
                headers={**BASE_HEADERS, "Host": "www.sec.gov"},
            ) as client:
                r = client.get(COMPANY_TICKERS_URL)
                r.raise_for_status()
                for item in r.json().values():
                    if item.get("ticker", "").upper() == ticker.upper():
                        cik = str(item["cik_str"]).zfill(10)
                        _LOG.info("Resolved %s → CIK %s", ticker, cik)
                        return cik
            _LOG.warning("Ticker %s not found in SEC company_tickers.json", ticker)
            return None
        except httpx.HTTPError as e:
            _LOG.error("CIK lookup failed for %s: %s", ticker, e)
            return None

    # ── Official submissions API ───────────────────────────────────────────────

    def _fetch_submissions(self, cik: str, max_filings: int = 10000) -> dict:
        """
        Fetch the complete submission history for a CIK from the official
        data.sec.gov/submissions/ REST API.

        The primary JSON contains at least 1 year or 1,000 filings.
        If the company has more filings, an additional `files` array lists
        supplemental JSON files — we fetch and merge those too.

        Args:
            cik: 10-digit CIK number
            max_filings: Maximum number of filings to fetch (default: 10000)

        Returns the `filings.recent` dict (columnar arrays) with all historical
        filings merged in, capped at max_filings.
        """
        url = SUBMISSIONS_URL.format(cik=cik)
        try:
            with httpx.Client(
                timeout=15.0,
                headers=BASE_HEADERS,
                follow_redirects=True,
            ) as client:
                r = client.get(url)
                r.raise_for_status()
                data = r.json()

                recent = data.get("filings", {}).get("recent", {})

                # Fetch any additional paginated filing files
                extra_files = data.get("filings", {}).get("files", [])
                _LOG.info(
                    "CIK %s: found %d extra submission files, fetching all...",
                    cik,
                    len(extra_files),
                )
                for file_info in extra_files:
                    fname = file_info.get("name", "")
                    if not fname:
                        continue
                    extra_url = f"{DATA_API_BASE}/submissions/{fname}"
                    time.sleep(SEC_RATE_LIMIT_DELAY)
                    try:
                        er = client.get(extra_url)
                        er.raise_for_status()
                        extra = er.json()
                        for key, values in extra.items():
                            if isinstance(values, list) and key in recent:
                                recent[key].extend(values)
                        _LOG.debug(
                            "Merged extra file %s (%d items)",
                            fname,
                            len(extra.get(key, [])),
                        )
                    except httpx.HTTPError as e:
                        _LOG.warning(
                            "Failed to fetch extra submissions file %s: %s", fname, e
                        )

                # Cap results if we have more than requested
                total_filings = len(recent.get("form", []))
                if total_filings > max_filings:
                    _LOG.info(
                        "CIK %s: capping %d filings to %d (max_filings)",
                        cik,
                        total_filings,
                        max_filings,
                    )
                    for key in recent:
                        if isinstance(recent[key], list):
                            recent[key] = recent[key][:max_filings]

            return recent

        except httpx.HTTPError as e:
            _LOG.error("Submissions API failed for CIK %s: %s", cik, e)
            return {}

    def _filter_submissions_by_type(
        self,
        recent: dict,
        filing_type: str,
        limit: int,
    ) -> list[dict]:
        """
        Extract matching filings from the columnar submissions data structure.

        The submissions JSON uses parallel arrays (not a list of objects):
          recent["form"]       → ["10-K", "8-K", ...]
          recent["accessionNumber"] → ["0001234567-23-000001", ...]
          recent["filingDate"] → ["2023-02-03", ...]
          etc.

        Returns list of dicts, newest first, up to `limit`.
        """
        forms = recent.get("form", [])
        accessions = recent.get("accessionNumber", [])
        filing_dates = recent.get("filingDate", [])
        primary_docs = recent.get("primaryDocument", [])
        descriptions = recent.get("primaryDocDescription", [])
        report_dates = recent.get("reportDate", [])

        matched = []
        for i, form in enumerate(forms):
            # Match exact form type or amendment variants (e.g. 10-K/A)
            if not (form == filing_type or form.startswith(f"{filing_type}/")):
                continue

            matched.append(
                {
                    "form": form,
                    "accession": accessions[i] if i < len(accessions) else "",
                    "filing_date": filing_dates[i] if i < len(filing_dates) else "",
                    "primary_doc": primary_docs[i] if i < len(primary_docs) else "",
                    "description": descriptions[i] if i < len(descriptions) else "",
                    "report_date": report_dates[i] if i < len(report_dates) else "",
                }
            )

            if len(matched) >= limit:
                break  # submissions are already newest-first

        return matched

    # ── Async document fetching ───────────────────────────────────────────────

    async def _async_get(
        self,
        client: httpx.AsyncClient,
        url: str,
        host_header: str = "www.sec.gov",
    ) -> Optional[httpx.Response]:
        """
        Async GET with proactive rate-limit delay and exponential-backoff
        retry on 429/503 (the only codes SEC returns for throttling).
        """
        for attempt in range(SEC_MAX_RETRIES):
            await asyncio.sleep(SEC_RATE_LIMIT_DELAY)
            try:
                r = await client.get(
                    url,
                    headers={**BASE_HEADERS, "Host": host_header},
                )
                if r.status_code in (429, 503):
                    wait = (attempt + 1) * 2  # 2s, 4s, 6s, 8s
                    _LOG.warning(
                        "HTTP %s on %s — retrying in %ds (attempt %d/%d)",
                        r.status_code,
                        url,
                        wait,
                        attempt + 1,
                        SEC_MAX_RETRIES,
                    )
                    await asyncio.sleep(wait)
                    continue
                r.raise_for_status()
                return r
            except httpx.HTTPError as e:
                if attempt == SEC_MAX_RETRIES - 1:
                    _LOG.error(
                        "Request failed after %d attempts: %s — %s",
                        SEC_MAX_RETRIES,
                        url,
                        e,
                    )
                    return None
                await asyncio.sleep(2**attempt)
        return None

    async def _fetch_document(
        self,
        client: httpx.AsyncClient,
        semaphore: asyncio.Semaphore,
        cik: str,
        filing: dict,
    ) -> tuple[dict, str]:
        """
        Fetch the primary document for a single filing.

        Strategy (using official URL patterns from SEC docs):
          1. Build primary doc URL directly from submissions data if available.
             URL pattern: /Archives/edgar/data/{cik_int}/{accession_nodash}/{primary_doc}
          2. Fall back to parsing the filing index page if primary_doc is missing.
        """
        async with semaphore:
            accession = filing["accession"]
            accession_clean = accession.replace("-", "")
            cik_int = int(cik)  # SEC URLs use integer CIK (no leading zeros)
            base_archive = f"{SEC_BASE}/Archives/edgar/data/{cik_int}/{accession_clean}"

            # Path 1: primary document filename is in the submissions JSON
            primary_doc = filing.get("primary_doc", "")
            if primary_doc:
                doc_url = f"{base_archive}/{primary_doc}"
                resp = await self._async_get(client, doc_url)
                if resp and len(resp.text) > 500:
                    return filing, self._strip_html(resp.text)

            # Path 2: fetch the index page and parse the primary document link
            index_url = f"{base_archive}/{accession_clean}-index.htm"
            index_resp = await self._async_get(client, index_url)
            if not index_resp:
                return filing, ""

            doc_url = self._find_primary_doc_in_index(index_resp.text, base_archive)
            if not doc_url:
                # Last resort: return cleaned index text
                return filing, self._strip_html(index_resp.text)

            doc_resp = await self._async_get(client, doc_url)
            if not doc_resp:
                return filing, ""

            return filing, self._strip_html(doc_resp.text)

    def _find_primary_doc_in_index(
        self, index_html: str, base_url: str
    ) -> Optional[str]:
        """
        Parse the EDGAR filing index page to find the primary document.
        Prefers .htm/.html files; skips exhibits and the index page itself.
        """
        # Match links in the filing index table
        pattern = re.compile(r'href="([^"]+\.htm[l]?)"', re.IGNORECASE)
        for href in pattern.findall(index_html):
            if href.endswith("-index.htm"):
                continue
            # Relative href → absolute
            if href.startswith("/Archives"):
                return f"{SEC_BASE}{href}"
            if not href.startswith("http"):
                return f"{base_url}/{href}"
            return href
        return None

    # ── HTML cleaning ─────────────────────────────────────────────────────────

    def _strip_html(self, html: str) -> str:
        """Clean HTML filing to plain text. Handles inline XBRL."""
        # Remove non-content blocks
        for pat in (
            r"<script[^>]*>.*?</script>",
            r"<style[^>]*>.*?</style>",
            r"<ix:[^>]*/>",  # self-closing inline XBRL tags
            r"</?ix:[a-z]+[^>]*>",  # opening/closing XBRL wrappers
            r"<!--.*?-->",  # HTML comments
        ):
            html = re.sub(pat, " ", html, flags=re.DOTALL | re.IGNORECASE)
        text = re.sub(r"<[^>]+>", " ", html)  # strip remaining tags
        text = re.sub(r"[ \t]+", " ", text)  # collapse horizontal whitespace
        text = re.sub(r"\n{3,}", "\n\n", text)  # max 2 consecutive newlines
        return text.strip()

    # ── Main async pipeline ───────────────────────────────────────────────────

    async def _fetch_filing_type_async(
        self,
        cik: str,
        filing_type: str,
        filings_meta: list[dict],
    ) -> list[dict]:
        """Concurrently fetch document content for a list of filing metadata dicts."""
        semaphore = asyncio.Semaphore(SEC_CONCURRENCY)

        async with httpx.AsyncClient(
            timeout=30.0,
            follow_redirects=True,
        ) as client:
            tasks = [
                self._fetch_document(client, semaphore, cik, f) for f in filings_meta
            ]
            results = await asyncio.gather(*tasks, return_exceptions=True)

        output = []
        for result in results:
            if isinstance(result, Exception):
                _LOG.warning("Document fetch raised: %s", result)
                continue
            filing_meta, text = result
            if not text or len(text) < 100:
                continue
            output.append(
                {
                    "text": text,
                    "metadata": {
                        "form_type": filing_meta["form"],
                        "filing_date": filing_meta["filing_date"],
                        "report_date": filing_meta["report_date"],
                        "accession_number": filing_meta["accession"],
                        "description": filing_meta["description"],
                        "cik": cik,
                        "url": (
                            f"{SEC_BASE}/Archives/edgar/data/{int(cik)}/"
                            f"{filing_meta['accession'].replace('-', '')}/"
                            f"{filing_meta['accession'].replace('-', '')}-index.htm"
                        ),
                    },
                }
            )
        return output

    # ── Public interface ──────────────────────────────────────────────────────

    def _fetch_data(
        self,
        ticker: str,
        filing_types: Optional[list[str]] = None,
        limit: int = 5000,
        max_filings: int = 10000,
    ) -> list[dict]:
        """
        Main entry point. Resolves CIK, fetches submission history via the
        official data.sec.gov API, then concurrently downloads filing content.

        Args:
            ticker: Stock ticker symbol
            filing_types: List of form types to collect (default: 10-K, 10-Q, 8-K, DEF 14A, S-1)
            limit: Maximum filings to return (default: 5000)
            max_filings: Maximum filings to fetch from SEC API (default: 10000)

        Returns:
            List of filing dicts with 'text' and 'metadata' keys

        Note:
            For large-scale collection (1000+ filings), expect 5-15 minutes per ticker
            depending on network speed and SEC API response times.
        """
        if filing_types is None:
            filing_types = DEFAULT_FILING_TYPES

        cik = self._get_cik_for_ticker(ticker)
        if not cik:
            return []

        t0 = time.perf_counter()

        # ── Step 1: fetch full submission history (single API call) ──
        _LOG.info(
            "Fetching submission history for %s (CIK %s), max_filings=%d…",
            ticker,
            cik,
            max_filings,
        )
        recent = self._fetch_submissions(cik, max_filings=max_filings)
        if not recent:
            _LOG.error("No submission data returned for CIK %s", cik)
            return []

        total_on_record = len(recent.get("form", []))
        _LOG.info("Submission history: %d filings on record", total_on_record)

        # ── Step 2: filter by type (in-memory, no extra requests) ──
        # For large-scale: get proportional share per filing type
        per_type = max(100, limit // len(filing_types))
        all_meta: list[dict] = []
        for ft in filing_types:
            matched = self._filter_submissions_by_type(recent, ft, per_type)
            _LOG.info(
                "  [%s] matched %d filings (requested %d)", ft, len(matched), per_type
            )
            all_meta.extend(matched)

        if not all_meta:
            _LOG.warning(
                "No matching filings found for %s with types %s", ticker, filing_types
            )
            return []

        _LOG.info(
            "Total filings to fetch: %d (types: %s)",
            len(all_meta),
            ", ".join(filing_types),
        )

        # ── Step 3: concurrently fetch document content ──
        # Process in batches to avoid memory issues with large collections
        BATCH_SIZE = 100
        all_filings: list[dict] = []

        for batch_start in range(0, len(all_meta), BATCH_SIZE):
            batch_end = min(batch_start + BATCH_SIZE, len(all_meta))
            batch_meta = all_meta[batch_start:batch_end]

            _LOG.info(
                "Fetching batch %d-%d of %d filings (concurrency=%d)…",
                batch_start + 1,
                batch_end,
                len(all_meta),
                SEC_CONCURRENCY,
            )

            batch_results = _run_async(self._fetch_all_types(cik, batch_meta))
            all_filings.extend(batch_results)

            # Progress update
            if (batch_end // BATCH_SIZE) % 10 == 0:
                _LOG.info(
                    "Progress: %d/%d filings processed", len(all_filings), len(all_meta)
                )

        # Sort newest-first and cap at limit
        all_filings.sort(
            key=lambda x: x["metadata"].get("filing_date", ""),
            reverse=True,
        )
        all_filings = all_filings[:limit]

        elapsed = time.perf_counter() - t0
        _LOG.info(
            "Done: %d filings fetched in %.1fs (%.2fs avg/filing)",
            len(all_filings),
            elapsed,
            elapsed / max(len(all_filings), 1),
        )
        return all_filings

    async def _fetch_all_types(self, cik: str, all_meta: list[dict]) -> list[dict]:
        """Run all document fetches in a single async context."""
        semaphore = asyncio.Semaphore(SEC_CONCURRENCY)
        async with httpx.AsyncClient(
            timeout=30.0,
            follow_redirects=True,
        ) as client:
            tasks = [self._fetch_document(client, semaphore, cik, f) for f in all_meta]
            results = await asyncio.gather(*tasks, return_exceptions=True)

        output = []
        for result in results:
            if isinstance(result, Exception):
                _LOG.warning("Document fetch error: %s", result)
                continue
            filing_meta, text = result
            if not text or len(text) < 100:
                continue
            output.append(
                {
                    "text": text,
                    "metadata": {
                        "form_type": filing_meta["form"],
                        "filing_date": filing_meta["filing_date"],
                        "report_date": filing_meta["report_date"],
                        "accession_number": filing_meta["accession"],
                        "description": filing_meta["description"],
                        "cik": cik,
                        "url": (
                            f"{SEC_BASE}/Archives/edgar/data/{int(cik)}/"
                            f"{filing_meta['accession'].replace('-', '')}/"
                            f"{filing_meta['accession'].replace('-', '')}-index.htm"
                        ),
                    },
                }
            )
        return output

    def collect(
        self,
        ticker: str,
        filing_types: Optional[list[str]] = None,
        limit: int = 5000,
        max_filings: int = 10000,
        store_cold: bool = True,
        store_warm: bool = True,
        store_search: bool = True,
        use_cache: bool = False,
    ) -> dict[str, int]:
        """
        Collect SEC filings for a ticker.

        Args:
            ticker: Stock ticker symbol
            filing_types: List of form types (default: 10-K, 10-Q, 8-K, DEF 14A, S-1)
            limit: Maximum filings to process (default: 5000)
            max_filings: Max filings to fetch from SEC API (default: 10000)
            store_cold: Store raw filings in MinIO
            store_warm: Store chunks + embeddings in PostgreSQL
            store_search: Index in txtai for semantic search
            use_cache: Use cached results if available
        """
        if filing_types is None:
            filing_types = DEFAULT_FILING_TYPES
        return super().collect(
            ticker=ticker,
            filing_types=filing_types,
            limit=limit,
            max_filings=max_filings,
            store_cold=store_cold,
            store_warm=store_warm,
            store_search=store_search,
            use_cache=use_cache,
        )
