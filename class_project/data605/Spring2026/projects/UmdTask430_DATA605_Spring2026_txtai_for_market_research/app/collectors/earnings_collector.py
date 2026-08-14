"""
Earnings call transcript collector.

Fetches full earnings call transcripts from Alpha Vantage's
``EARNINGS_CALL_TRANSCRIPT`` endpoint and stores them across all four tiers.

The free Alpha Vantage tier supports this endpoint at 25 calls/day, so we
default to the last 4 quarters per ticker.

Stores:
- Cold (MinIO):   raw transcript JSON under ``earnings/{ticker}/{quarter}.json``
- Warm (Postgres): filing row (filing_type=``EARNINGS_TRANSCRIPT``)
                  + chunks + document_metadata
- Search (txtai):  chunks indexed with ``tags="earnings"``
- Hot (KeyDB):     fetch cache via the base collector
"""

import logging
import os
from datetime import datetime
from typing import Any

import httpx

from app.collectors.base_collector import BaseCollector

_LOG = logging.getLogger(__name__)


# Calendar quarter -> end-of-quarter month/day used for period_of_report.
_QUARTER_END = {
    1: (3, 31),
    2: (6, 30),
    3: (9, 30),
    4: (12, 31),
}


class EarningsCollector(BaseCollector):
    """
    Collector for earnings call transcripts.
    """

    def _get_source_tag(self) -> str:
        return "earnings"

    def _fetch_data(
        self,
        ticker: str,
        quarters: int = 4,
        year: int | None = None,
        quarter: int | None = None,
        **_,
    ) -> list[dict]:
        """
        Fetch earnings transcripts for the given ticker.

        :param ticker: stock ticker symbol
        :param quarters: number of trailing quarters to fetch (default 4)
        :param year: optional explicit year (overrides ``quarters``)
        :param quarter: optional explicit quarter 1-4 (overrides ``quarters``)
        :return: list of dicts with ``text`` and ``metadata``
        """
        api_key = os.getenv("ALPHAVANTAGE_API_KEY")
        if not api_key:
            _LOG.error(
                "ALPHAVANTAGE_API_KEY not set; cannot fetch earnings transcripts"
            )
            return []
        if year is not None and quarter is not None:
            quarter_codes = [self._format_quarter(year, quarter)]
        else:
            quarter_codes = self._recent_quarter_codes(quarters)
        results: list[dict] = []
        for q_code in quarter_codes:
            doc = self._fetch_alphavantage_transcript(ticker, q_code, api_key)
            if doc is not None:
                results.append(doc)
        _LOG.info("Fetched %d transcript(s) for %s", len(results), ticker)
        return results

    @staticmethod
    def _format_quarter(year: int, quarter: int) -> str:
        return f"{year}Q{quarter}"

    @staticmethod
    def _recent_quarter_codes(n: int) -> list[str]:
        """
        Return the last ``n`` finished calendar quarter codes (most recent first).
        """
        now = datetime.utcnow()
        # Most recent finished quarter is the one before the current calendar
        # quarter, since reports lag a few weeks.
        cur_q = (now.month - 1) // 3 + 1
        year, quarter = now.year, cur_q - 1
        if quarter == 0:
            year, quarter = year - 1, 4
        codes: list[str] = []
        for _ in range(n):
            codes.append(f"{year}Q{quarter}")
            quarter -= 1
            if quarter == 0:
                year, quarter = year - 1, 4
        return codes

    def _fetch_alphavantage_transcript(
        self,
        ticker: str,
        quarter_code: str,
        api_key: str,
    ) -> dict | None:
        """
        Hit the Alpha Vantage transcript endpoint for one ticker / quarter.

        Returns None if the response is empty or rate-limited.
        """
        url = "https://www.alphavantage.co/query"
        params = {
            "function": "EARNINGS_CALL_TRANSCRIPT",
            "symbol": ticker,
            "quarter": quarter_code,
            "apikey": api_key,
        }
        try:
            with httpx.Client(timeout=20.0) as client:
                response = client.get(url, params=params)
                response.raise_for_status()
                payload = response.json()
        except httpx.HTTPError as e:
            _LOG.error("Alpha Vantage transcript HTTP error for %s %s: %s", ticker, quarter_code, e)
            return None
        # Alpha Vantage signals throttling and empty responses with informational keys.
        if "Note" in payload or "Information" in payload:
            _LOG.warning(
                "Alpha Vantage rate-limit / info response for %s %s: %s",
                ticker,
                quarter_code,
                payload.get("Note") or payload.get("Information"),
            )
            return None
        turns = payload.get("transcript") or []
        if not turns:
            _LOG.info("No transcript available for %s %s", ticker, quarter_code)
            return None
        # Join all speaker turns into a single text blob; keep speakers in metadata.
        text_lines = []
        speakers: list[str] = []
        for turn in turns:
            speaker = (turn.get("speaker") or "").strip()
            content = (turn.get("content") or "").strip()
            if not content:
                continue
            if speaker:
                text_lines.append(f"{speaker}: {content}")
                if speaker not in speakers:
                    speakers.append(speaker)
            else:
                text_lines.append(content)
        text = "\n".join(text_lines).strip()
        if not text:
            return None
        year, q = self._parse_quarter_code(quarter_code)
        period_end = self._quarter_end_date(year, q)
        metadata: dict[str, Any] = {
            "ticker": ticker,
            "form_type": "EARNINGS_TRANSCRIPT",
            "accession_number": f"{ticker}-EARN-{quarter_code}",
            "quarter": quarter_code,
            "fiscal_year": year,
            "fiscal_quarter": q,
            "period_of_report": period_end,
            # filing_date is unknown from this endpoint; agents can fall back to period.
            "filing_date": period_end,
            "url": f"alphavantage:EARNINGS_CALL_TRANSCRIPT/{ticker}/{quarter_code}",
            "company_name": payload.get("symbol", ticker),
            "speakers": speakers,
            "speaker_count": len(speakers),
            "turn_count": len(turns),
        }
        return {"text": text, "metadata": metadata, "raw": payload}

    @staticmethod
    def _parse_quarter_code(code: str) -> tuple[int, int]:
        year_str, q_str = code.split("Q")
        return int(year_str), int(q_str)

    @staticmethod
    def _quarter_end_date(year: int, quarter: int) -> str:
        month, day = _QUARTER_END[quarter]
        return f"{year:04d}-{month:02d}-{day:02d}"
