"""Tests for src.ingestion.edgar — fully mocked, no live network."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

from src.ingestion import edgar


SAMPLE_TICKERS = {
    "0": {"cik_str": 789019, "ticker": "MSFT", "title": "MICROSOFT CORP"},
}

SAMPLE_SUBMISSIONS = {
    "filings": {
        "recent": {
            "form": ["10-Q", "10-K", "8-K"],
            "accessionNumber": [
                "0000000000-24-000001",
                "0000789019-24-000010",
                "0000000000-24-000002",
            ],
            "filingDate": ["2024-04-25", "2024-07-30", "2024-08-01"],
            "primaryDocument": ["msft10q.htm", "msft10k.htm", "msft8k.htm"],
        }
    }
}

SAMPLE_10K_HTML = """
<html><body>
<p>Table of contents: Item 1A. Risk Factors ... page 12</p>
<h2>Item 1A. Risk Factors</h2>
<p>Our business faces material risks including cybersecurity threats,
regulatory scrutiny, and competition from other cloud providers.</p>
<h2>Item 1B. Unresolved Staff Comments</h2>
<p>None.</p>
</body></html>
"""


def _json_response(payload):
    r = MagicMock()
    r.json.return_value = payload
    r.raise_for_status = MagicMock()
    return r


def _html_response(payload):
    r = MagicMock()
    r.text = payload
    r.raise_for_status = MagicMock()
    return r


def test_get_latest_10k_happy_path(monkeypatch):
    monkeypatch.setenv("EDGAR_USER_AGENT", "Test Runner test@example.com")

    with patch.object(edgar._RateLimitedSession, "get") as mock_get:
        mock_get.side_effect = [
            _json_response(SAMPLE_TICKERS),
            _json_response(SAMPLE_SUBMISSIONS),
            _html_response(SAMPLE_10K_HTML),
        ]
        result = edgar.get_latest_10k("msft")

    assert result["ticker"] == "MSFT"
    assert result["cik"] == "0000789019"
    assert result["accession"] == "0000789019-24-000010"
    assert result["filing_date"] == "2024-07-30"

    text = result["risk_factors_text"].lower()
    assert "cybersecurity" in text
    assert "unresolved staff comments" not in text
