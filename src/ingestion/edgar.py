"""SEC EDGAR fetcher for 10-K filings. Module 1 vertical slice.

Filled out in Module 02 with broader filing support, structured parsing,
incremental ingestion to S3, and a real chunker. The Item 1A extractor here
is deliberately brittle — readers should feel the seams before Module 02
fixes them.
"""

from __future__ import annotations

import os
import re
import time
from html.parser import HTMLParser

import requests
from dotenv import load_dotenv

load_dotenv()

TICKERS_URL = "https://www.sec.gov/files/company_tickers.json"
SUBMISSIONS_URL = "https://data.sec.gov/submissions/CIK{cik}.json"
ARCHIVE_URL = "https://www.sec.gov/Archives/edgar/data/{cik_int}/{accession_nodash}/{doc}"

# SEC caps callers at 10 req/s. 0.11s spacing keeps us safely under.
_MIN_INTERVAL_SECONDS = 0.11


class EdgarError(RuntimeError):
    """Anything that goes wrong fetching or parsing an EDGAR filing."""


def _user_agent() -> str:
    ua = os.environ.get("EDGAR_USER_AGENT", "").strip()
    if not ua:
        raise EdgarError(
            "EDGAR_USER_AGENT is empty. Set it in .env to 'Your Name your@email'."
        )
    return ua


class _RateLimitedSession:
    def __init__(self, user_agent: str) -> None:
        self._session = requests.Session()
        self._session.headers.update({
            "User-Agent": user_agent,
            "Accept-Encoding": "gzip, deflate",
        })
        self._last_call = 0.0

    def get(self, url: str) -> requests.Response:
        wait = _MIN_INTERVAL_SECONDS - (time.monotonic() - self._last_call)
        if wait > 0:
            time.sleep(wait)
        resp = self._session.get(url, timeout=30)
        self._last_call = time.monotonic()
        resp.raise_for_status()
        return resp


class _TextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self._chunks: list[str] = []
        self._skip_depth = 0

    def handle_starttag(self, tag: str, attrs: list) -> None:
        if tag in ("script", "style"):
            self._skip_depth += 1
        elif tag in ("br", "p", "div", "tr", "li", "h1", "h2", "h3"):
            self._chunks.append("\n")

    def handle_endtag(self, tag: str) -> None:
        if tag in ("script", "style") and self._skip_depth > 0:
            self._skip_depth -= 1
        elif tag in ("p", "div", "tr", "li", "h1", "h2", "h3"):
            self._chunks.append("\n")

    def handle_data(self, data: str) -> None:
        if self._skip_depth == 0:
            self._chunks.append(data)

    def text(self) -> str:
        return "".join(self._chunks)


def _html_to_text(html: str) -> str:
    parser = _TextExtractor()
    parser.feed(html)
    text = parser.text()
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{2,}", "\n\n", text)
    return text.strip()


def _resolve_cik(ticker: str, session: _RateLimitedSession) -> str:
    data = session.get(TICKERS_URL).json()
    needle = ticker.upper()
    for row in data.values():
        if row.get("ticker", "").upper() == needle:
            return f"{int(row['cik_str']):010d}"
    raise EdgarError(f"Ticker {ticker!r} not found in SEC company_tickers.json.")


def _find_latest_10k(submissions: dict) -> dict:
    recent = submissions.get("filings", {}).get("recent", {})
    forms = recent.get("form", [])
    accessions = recent.get("accessionNumber", [])
    dates = recent.get("filingDate", [])
    docs = recent.get("primaryDocument", [])
    for form, acc, date, doc in zip(forms, accessions, dates, docs):
        if form == "10-K":
            return {"accession": acc, "filing_date": date, "primary_document": doc}
    raise EdgarError("No 10-K filing found in the recent submissions feed.")


_ITEM_1A_RE = re.compile(r"item\s*1a\.?\s*risk\s*factors", re.IGNORECASE)
_ITEM_1B_RE = re.compile(r"item\s*1b\.?\s*unresolved\s*staff\s*comments", re.IGNORECASE)
_ITEM_2_RE = re.compile(r"item\s*2\.?\s*properties", re.IGNORECASE)


def _extract_risk_factors(text: str) -> str:
    # The first occurrence is almost always the table-of-contents entry; the
    # second is the real section heading. Brittle on purpose — Module 02
    # replaces this with structured XBRL section parsing.
    starts = [m.start() for m in _ITEM_1A_RE.finditer(text)]
    if not starts:
        raise EdgarError("Could not locate 'Item 1A. Risk Factors' in the filing.")
    start = starts[1] if len(starts) > 1 else starts[0]
    section = text[start:]
    end_match = _ITEM_1B_RE.search(section, 1) or _ITEM_2_RE.search(section, 1)
    end = end_match.start() if end_match else len(section)
    return section[:end].strip()


def get_latest_10k(ticker: str) -> dict:
    session = _RateLimitedSession(_user_agent())
    cik = _resolve_cik(ticker, session)
    submissions = session.get(SUBMISSIONS_URL.format(cik=cik)).json()
    meta = _find_latest_10k(submissions)
    doc_url = ARCHIVE_URL.format(
        cik_int=int(cik),
        accession_nodash=meta["accession"].replace("-", ""),
        doc=meta["primary_document"],
    )
    html = session.get(doc_url).text
    risk_text = _extract_risk_factors(_html_to_text(html))
    return {
        "ticker": ticker.upper(),
        "cik": cik,
        "accession": meta["accession"],
        "filing_date": meta["filing_date"],
        "risk_factors_text": risk_text,
    }


if __name__ == "__main__":
    result = get_latest_10k("MSFT")
    print(
        f"ticker={result['ticker']} cik={result['cik']} "
        f"accession={result['accession']} filing_date={result['filing_date']}"
    )
    print(f"risk_factors_text length: {len(result['risk_factors_text'])} chars")
    print("--- first 500 chars ---")
    print(result["risk_factors_text"][:500])
