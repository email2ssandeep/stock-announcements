"""
Compliance Gate — BR-04 / TC-F3.5
Zero share price or financial metric data anywhere in the API.
"""
import pytest

FORBIDDEN_FIELDS = {"price", "ltp", "close", "open", "high", "low", "volume", "market_cap", "pe_ratio"}
FORBIDDEN_KEYWORDS = ["₹", "$", "price", "ltp", "volume", "market cap"]


def _flatten_announcements(data: dict) -> list[dict]:
    items = []
    for ticker, anns in data.items():
        items.extend(anns)
    return items


class TestComplianceNoPriceData:
    def test_no_price_fields_in_api_response(self, seeded_client):
        """TC-F3.5-02 / API-05 — No price/financial fields in /api/announcements JSON."""
        resp = seeded_client.get("/api/announcements")
        assert resp.status_code == 200
        data = resp.json()
        items = _flatten_announcements(data)
        for ann in items:
            for field in FORBIDDEN_FIELDS:
                assert field not in ann, f"Forbidden field '{field}' found in announcement: {ann}"

    def test_announcement_objects_only_have_allowed_fields(self, seeded_client):
        """Each announcement may only have: date, title, source_url."""
        resp = seeded_client.get("/api/announcements")
        data = resp.json()
        allowed = {"date", "title", "source_url"}
        items = _flatten_announcements(data)
        for ann in items:
            extra = set(ann.keys()) - allowed
            assert not extra, f"Unexpected fields in announcement: {extra}"

    def test_no_price_keywords_in_titles(self, seeded_client):
        """TC-F3.5 — Titles must not contain structured SHARE PRICE values.
        Note: deal/acquisition amounts like '$465m' are permitted per BRD —
        BR-04 only prohibits share price data (e.g. ₹1,234.56 per share / LTP).
        """
        import re
        # Match share price patterns: ₹1234.56, Rs.1234, LTP 123, close price 123
        # NOT acquisition deal values like $465m or $1bn
        share_price_pattern = re.compile(
            r"(₹|rs\.?)\s*[\d,]+\.?\d*\s*(per\s+share|ltp|close|open)|"
            r"\bltp\s*[=:₹$]?\s*\d+|"
            r"\bclose\s+price\b",
            re.IGNORECASE
        )
        resp = seeded_client.get("/api/announcements")
        data = resp.json()
        for ticker, items in data.items():
            for ann in items:
                match = share_price_pattern.search(ann.get("title", ""))
                assert not match, (
                    f"Share price data found in {ticker} title: '{ann['title']}'"
                )

    def test_health_endpoint_has_no_price_fields(self, seeded_client):
        """Health endpoint also must not expose financial data."""
        resp = seeded_client.get("/api/health")
        data = resp.json()
        for field in FORBIDDEN_FIELDS:
            assert field not in data, f"Forbidden field '{field}' in /api/health response"

    def test_single_company_endpoint_no_price_fields(self, seeded_client):
        """TC-F3.5-02 — Single-company endpoint also has no price fields."""
        for ticker in ("infosys", "hcl", "reliance", "tcs"):
            resp = seeded_client.get(f"/api/announcements/{ticker}")
            items = resp.json()
            for ann in items:
                for field in FORBIDDEN_FIELDS:
                    assert field not in ann, f"Field '{field}' in {ticker} response"


class TestComplianceDataSourced:
    def test_all_source_urls_point_to_bse_or_screener(self, seeded_client):
        """BR-05 — Source URLs should come from Screener.in or its linked BSE filings."""
        resp = seeded_client.get("/api/announcements")
        data = resp.json()
        for ticker, items in data.items():
            for ann in items:
                if ann.get("source_url"):
                    url = ann["source_url"].lower()
                    assert any(domain in url for domain in ["bseindia.com", "screener.in", "nseindia.com"]), (
                        f"Unexpected source URL for {ticker}: {ann['source_url']}"
                    )

    def test_exactly_four_companies_in_response(self, seeded_client):
        """BR-01 — Response must contain exactly the 4 monitored companies."""
        resp = seeded_client.get("/api/announcements")
        data = resp.json()
        assert set(data.keys()) == {"infosys", "hcl", "reliance", "tcs"}
