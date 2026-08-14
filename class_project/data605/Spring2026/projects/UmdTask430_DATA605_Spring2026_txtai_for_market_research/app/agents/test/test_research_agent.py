"""
Unit tests for the research agent's pure functions.

Covers:
- ``_extract_ticker``: cashtag, company name, bare uppercase token, ambiguous
- ``_route``: keyword routing for SEC / News / both
- ``_filter_by_ticker``: dict and JSON-string metadata shapes
- ``_first_sentences``: short text, multi-sentence text
- ``_format_citation``: minimal vs. full metadata
"""

import json
import logging
import unittest

from app.agents.research_agent import (
    _extract_ticker,
    _filter_by_ticker,
    _first_sentences,
    _format_citation,
    _route,
)

_LOG = logging.getLogger(__name__)


# #############################################################################
# Test__extract_ticker
# #############################################################################


class Test__extract_ticker(unittest.TestCase):
    """
    Test ticker extraction from natural-language queries.
    """

    def helper(self, query: str, expected: str | None) -> None:
        """
        Run extractor and compare to expected ticker.

        :param query: raw user query
        :param expected: expected ticker symbol, or ``None``
        """
        # Run test.
        actual = _extract_ticker(query)
        # Check output.
        self.assertEqual(actual, expected)

    def test1(self) -> None:
        """
        Cashtag mention returns the explicit ticker.
        """
        self.helper("How is $AAPL doing?", "AAPL")

    def test2(self) -> None:
        """
        Company name maps to the canonical ticker.
        """
        self.helper("What's the latest on apple?", "AAPL")

    def test3(self) -> None:
        """
        Bare uppercase token is treated as a ticker when it is not a common
        English word.
        """
        self.helper("Tell me about NVDA earnings", "NVDA")

    def test4(self) -> None:
        """
        Common acronyms (SEC, CEO, AI, ML) are not mistaken for tickers.
        """
        self.helper("Are there any SEC issues?", None)

    def test5(self) -> None:
        """
        Query with no ticker-like content returns ``None``.
        """
        self.helper("how are markets today", None)


# #############################################################################
# Test__route
# #############################################################################


class Test__route(unittest.TestCase):
    """
    Test the keyword router that chooses sub-agents.
    """

    def test1(self) -> None:
        """
        SEC-only keyword routes to the SEC agent.
        """
        # Run test.
        out = _route("Summarize the latest 10-K filing")
        # Check outputs.
        self.assertEqual(out["agents"], ["sec"])

    def test2(self) -> None:
        """
        News-only keyword routes to the News agent.
        """
        # Run test.
        out = _route("Any bullish analyst upgrades?")
        # Check outputs.
        self.assertEqual(out["agents"], ["news"])

    def test3(self) -> None:
        """
        Generic question fans out to both sub-agents.
        """
        # Run test.
        out = _route("Tell me about Apple")
        # Check outputs.
        self.assertEqual(out["agents"], ["sec", "news"])

    def test4(self) -> None:
        """
        Router carries the extracted ticker through.
        """
        # Run test.
        out = _route("Tell me about $TSLA")
        # Check outputs.
        self.assertEqual(out["ticker"], "TSLA")


# #############################################################################
# Test__filter_by_ticker
# #############################################################################


class Test__filter_by_ticker(unittest.TestCase):
    """
    Test that ticker filtering handles both dict and JSON-string metadata.
    """

    def test1(self) -> None:
        """
        Dict metadata is matched case-insensitively.
        """
        # Prepare inputs.
        results = [
            {"text": "a", "metadata": {"ticker": "AAPL"}},
            {"text": "b", "metadata": {"ticker": "MSFT"}},
        ]
        # Run test.
        out = _filter_by_ticker(results, "aapl")
        # Check outputs.
        self.assertEqual(len(out), 1)
        self.assertEqual(out[0]["text"], "a")

    def test2(self) -> None:
        """
        JSON-string metadata is parsed and matched.
        """
        # Prepare inputs.
        results = [
            {"text": "a", "metadata": json.dumps({"ticker": "AAPL"})},
            {"text": "b", "metadata": json.dumps({"ticker": "NVDA"})},
        ]
        # Run test.
        out = _filter_by_ticker(results, "NVDA")
        # Check outputs.
        self.assertEqual(len(out), 1)
        self.assertEqual(out[0]["text"], "b")

    def test3(self) -> None:
        """
        ``None`` ticker disables filtering and returns the input unchanged.
        """
        # Prepare inputs.
        results = [{"text": "a"}, {"text": "b"}]
        # Run test.
        out = _filter_by_ticker(results, None)
        # Check outputs.
        self.assertEqual(out, results)


# #############################################################################
# Test__first_sentences
# #############################################################################


class Test__first_sentences(unittest.TestCase):
    """
    Test the simple sentence picker used by the extractive synthesizer.
    """

    def test1(self) -> None:
        """
        Multi-sentence text returns the first ``n`` sentences joined.
        """
        # Prepare inputs (each sentence > 30 chars to clear the fragment filter).
        text = (
            "Apple reported record fiscal-year revenue across services. "
            "Services grew double digits versus the prior year period. "
            "Hardware revenue was approximately flat compared to prior year. "
            "The CEO commented at length about long-term gross margins."
        )
        # Run test.
        out = _first_sentences(text, n=2)
        # Check outputs.
        self.assertIn("Apple reported record", out)
        self.assertIn("Services grew", out)
        self.assertNotIn("CEO commented", out)

    def test2(self) -> None:
        """
        Short single-fragment text falls back to a 300-char window.
        """
        # Prepare inputs.
        text = "Quarterly highlights"
        # Run test.
        out = _first_sentences(text)
        # Check outputs.
        self.assertEqual(out, "Quarterly highlights")


# #############################################################################
# Test__format_citation
# #############################################################################


class Test__format_citation(unittest.TestCase):
    """
    Test citation rendering for source list bullets.
    """

    def test1(self) -> None:
        """
        Full SEC metadata renders ticker, source, form type, and date.
        """
        # Prepare inputs.
        chunk = {
            "score": 0.87,
            "text": "Risk factors include macro uncertainty.",
            "metadata": {
                "ticker": "AAPL",
                "source": "sec",
                "filing_type": "10-K",
                "filing_date": "2024-09-30",
            },
        }
        # Run test.
        out = _format_citation(1, chunk)
        # Check outputs.
        self.assertIn("[1]", out)
        self.assertIn("AAPL", out)
        self.assertIn("sec", out)
        self.assertIn("10-K", out)
        self.assertIn("2024-09-30", out)
        self.assertIn("0.870", out)

    def test2(self) -> None:
        """
        Minimal metadata still renders a valid line.
        """
        # Prepare inputs.
        chunk = {"score": 0.1, "text": "x", "metadata": {}}
        # Run test.
        out = _format_citation(7, chunk)
        # Check outputs.
        self.assertIn("[7]", out)
        self.assertIn("0.100", out)


if __name__ == "__main__":
    unittest.main()
