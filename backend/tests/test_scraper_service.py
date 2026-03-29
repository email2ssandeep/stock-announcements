"""
Module 1 — Data Scraping Layer
TC-F1.1, TC-F1.2, TC-F1.3, TC-F1.4
"""
import pytest
from unittest.mock import patch, MagicMock
from app.services.scraper_service import (
    scrape_company, scrape_all, _parse_announcements, MAX_ANNOUNCEMENTS
)
from app.config import COMPANY_URLS


# ── TC-F1.2 : URL Mapping ──────────────────────────────────────────────────

class TestUrlMapping:
    def test_all_four_companies_present(self):
        """TC-F1.2-01 — All 4 companies must be in the URL map."""
        assert len(COMPANY_URLS) == 4

    def test_exact_company_keys(self):
        """TC-F1.2-02 — Keys must be exactly infosys, hcl, reliance, tcs."""
        assert set(COMPANY_URLS.keys()) == {"infosys", "hcl", "reliance", "tcs"}

    def test_all_urls_point_to_screener(self):
        for ticker, url in COMPANY_URLS.items():
            assert "screener.in" in url, f"{ticker} URL does not point to screener.in"

    def test_all_urls_non_empty(self):
        for ticker, url in COMPANY_URLS.items():
            assert url.strip(), f"{ticker} URL is empty"


# ── Helpers: sample Screener.in HTML ──────────────────────────────────────

def _make_screener_html(items):
    """Build minimal Screener.in-style HTML for a given list of (title, date, description, url)."""
    lis = ""
    for title, date, desc, url in items:
        lis += f"""
        <li class="overflow-wrap-anywhere">
          <a href="{url}" target="_blank">
            {title}
            <div class="ink-600 smaller">{date} - {desc}</div>
          </a>
        </li>"""
    return f"""
    <html><body>
      <section id="documents">
        <ul class="list-links">{lis}</ul>
      </section>
    </body></html>"""


# ── TC-F1.1 : Scraper returns correct data ─────────────────────────────────

class TestScraperParsing:
    def test_returns_list_of_dicts(self):
        """TC-F1.1-01 — Scraper output is a list of dicts with title + date."""
        html = _make_screener_html([
            ("Acquisition", "25 Mar", "Company acquired X for $100m", "https://bse.com/1.pdf"),
        ])
        results = _parse_announcements(html)
        assert isinstance(results, list)
        assert len(results) == 1
        assert "title" in results[0]
        assert "date" in results[0]
        assert "source_url" in results[0]

    def test_title_and_date_non_empty(self):
        """TC-F1.1-02 — title and date fields must not be empty."""
        html = _make_screener_html([
            ("Board Meeting", "24 Mar", "Results to be declared on April 9", "https://bse.com/2.pdf"),
        ])
        results = _parse_announcements(html)
        assert results[0]["title"].strip()
        assert results[0]["date"].strip()

    def test_source_url_preserved(self):
        html = _make_screener_html([
            ("Dividend", "20 Mar", "Interim dividend recommended", "https://bse.com/div.pdf"),
        ])
        results = _parse_announcements(html)
        assert results[0]["source_url"] == "https://bse.com/div.pdf"

    def test_missing_section_returns_empty(self):
        """Scraper returns [] when announcements section is absent."""
        html = "<html><body><p>No data</p></body></html>"
        results = _parse_announcements(html)
        assert results == []

    def test_empty_html_returns_empty(self):
        results = _parse_announcements("")
        assert results == []


# ── TC-F1.3 : Top-3 Filter ─────────────────────────────────────────────────

class TestTopThreeFilter:
    def test_returns_at_most_three_items(self):
        """TC-F1.3-01 — Only 3 items returned even if page has 10."""
        items = [
            (f"Announcement {i}", f"{i} Mar", f"Description {i}", f"https://bse.com/{i}.pdf")
            for i in range(1, 11)
        ]
        html = _make_screener_html(items)
        results = _parse_announcements(html)
        assert len(results) <= MAX_ANNOUNCEMENTS
        assert len(results) == 3

    def test_fewer_than_three_returns_all(self):
        """TC-F1.3-03 — If only 1 announcement, returns exactly 1 (no padding)."""
        html = _make_screener_html([
            ("Only Announcement", "25 Mar", "Single item only", "https://bse.com/1.pdf"),
        ])
        results = _parse_announcements(html)
        assert len(results) == 1

    def test_empty_list_returns_zero(self):
        html = _make_screener_html([])
        results = _parse_announcements(html)
        assert len(results) == 0


# ── TC-F1.4 : Date Extraction ──────────────────────────────────────────────

class TestDateExtraction:
    def test_date_extracted_from_div(self):
        """TC-F1.4-01 — Date is parsed from ink-600 div."""
        html = _make_screener_html([
            ("Results", "25 Mar", "Q4 FY2026 results", "https://bse.com/r.pdf"),
        ])
        results = _parse_announcements(html)
        assert results[0]["date"] == "25 Mar"

    def test_relative_date_extracted(self):
        """TC-F1.4-01 — Relative dates like '2d' are also extracted."""
        html = _make_screener_html([
            ("Acquisition", "2d", "Company acquired something", "https://bse.com/a.pdf"),
        ])
        results = _parse_announcements(html)
        assert results[0]["date"] == "2d"

    def test_date_before_description_in_title(self):
        """TC-F1.4 — Parsed title should include description, date should be separate."""
        html = _make_screener_html([
            ("Board Meeting", "24 Mar", "April 20 results meeting", "https://bse.com/b.pdf"),
        ])
        results = _parse_announcements(html)
        assert results[0]["date"] == "24 Mar"
        assert "April 20" in results[0]["title"]

    def test_multiple_items_dates_are_independent(self):
        """TC-F1.4-02 — Each item has its own correctly parsed date."""
        html = _make_screener_html([
            ("Item A", "25 Mar", "Desc A", "https://bse.com/a.pdf"),
            ("Item B", "20 Mar", "Desc B", "https://bse.com/b.pdf"),
            ("Item C", "15 Mar", "Desc C", "https://bse.com/c.pdf"),
        ])
        results = _parse_announcements(html)
        assert results[0]["date"] == "25 Mar"
        assert results[1]["date"] == "20 Mar"
        assert results[2]["date"] == "15 Mar"


# ── TC-F1.1 : scrape_company with mocked HTTP ──────────────────────────────

class TestScrapeCompanyHttp:
    def _mock_response(self, html):
        mock_resp = MagicMock()
        mock_resp.text = html
        mock_resp.raise_for_status = MagicMock()
        return mock_resp

    def test_scrape_company_returns_data(self):
        """TC-F1.1-01 — scrape_company returns list of announcements."""
        html = _make_screener_html([
            ("Results", "25 Mar", "Q4 FY2026", "https://bse.com/1.pdf"),
        ])
        with patch("app.services.scraper_service.httpx.Client") as mock_client:
            mock_client.return_value.__enter__.return_value.get.return_value = self._mock_response(html)
            results = scrape_company("infosys")
        assert isinstance(results, list)
        assert len(results) == 1

    def test_unknown_ticker_returns_empty(self):
        """scrape_company with unknown ticker returns []."""
        results = scrape_company("UNKNOWN_TICKER")
        assert results == []

    def test_timeout_returns_empty(self):
        """TC-F2.3 — Timeout is caught gracefully, returns []."""
        import httpx
        with patch("app.services.scraper_service.httpx.Client") as mock_client:
            mock_client.return_value.__enter__.return_value.get.side_effect = httpx.TimeoutException("timeout")
            results = scrape_company("infosys")
        assert results == []

    def test_http_error_returns_empty(self):
        """TC-F2.3 — HTTP error (e.g. 503) is caught gracefully, returns []."""
        import httpx
        mock_resp = MagicMock()
        mock_resp.status_code = 503
        with patch("app.services.scraper_service.httpx.Client") as mock_client:
            mock_client.return_value.__enter__.return_value.get.side_effect = httpx.HTTPStatusError(
                "503", request=MagicMock(), response=mock_resp
            )
            results = scrape_company("tcs")
        assert results == []

    def test_scrape_all_returns_all_four_companies(self):
        """TC-F1.1-02 — scrape_all covers all 4 tickers."""
        html = _make_screener_html([
            ("Item", "25 Mar", "Desc", "https://bse.com/1.pdf"),
        ])
        with patch("app.services.scraper_service.httpx.Client") as mock_client:
            mock_client.return_value.__enter__.return_value.get.return_value = self._mock_response(html)
            results = scrape_all()
        assert set(results.keys()) == {"infosys", "hcl", "reliance", "tcs"}
