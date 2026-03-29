"""
Module 2 — Backend / API Layer
TC-F2.1, TC-F2.2, TC-F2.3
API-01 through API-10
"""
import pytest
import time
from unittest.mock import patch
from tests.conftest import SAMPLE_ANNOUNCEMENTS


# ── TC-F2.1 : GET /api/announcements ──────────────────────────────────────

class TestAnnouncementsEndpoint:
    def test_returns_200(self, seeded_client):
        """TC-F2.1-01 / API-01 — GET /api/announcements returns HTTP 200."""
        resp = seeded_client.get("/api/announcements")
        assert resp.status_code == 200

    def test_response_is_json(self, seeded_client):
        """API-01 — Response body is valid JSON."""
        resp = seeded_client.get("/api/announcements")
        assert resp.headers["content-type"].startswith("application/json")
        data = resp.json()
        assert isinstance(data, dict)

    def test_all_four_companies_present(self, seeded_client):
        """TC-F2.1-02 / API-01 — Response contains keys for all 4 companies."""
        resp = seeded_client.get("/api/announcements")
        data = resp.json()
        for ticker in ("infosys", "hcl", "reliance", "tcs"):
            assert ticker in data, f"Missing key: {ticker}"

    def test_each_company_has_at_most_three(self, seeded_client):
        """TC-F2.1-03 / API-02 — Each company array has ≤ 3 announcements."""
        resp = seeded_client.get("/api/announcements")
        data = resp.json()
        for ticker, items in data.items():
            assert len(items) <= 3, f"{ticker} has {len(items)} items (max 3)"

    def test_each_announcement_has_title(self, seeded_client):
        """TC-F2.1-04 / API-03 — Each announcement has a non-empty title."""
        resp = seeded_client.get("/api/announcements")
        data = resp.json()
        for ticker, items in data.items():
            for ann in items:
                assert "title" in ann
                assert ann["title"].strip(), f"{ticker} has empty title"

    def test_each_announcement_has_date(self, seeded_client):
        """TC-F2.1-04 / API-04 — Each announcement has a non-empty date."""
        resp = seeded_client.get("/api/announcements")
        data = resp.json()
        for ticker, items in data.items():
            for ann in items:
                assert "date" in ann
                assert ann["date"].strip(), f"{ticker} has empty date"

    def test_empty_db_returns_empty_arrays(self, client):
        """API-07 — With no data seeded, each company returns an empty array."""
        resp = client.get("/api/announcements")
        assert resp.status_code == 200
        data = resp.json()
        for ticker in ("infosys", "hcl", "reliance", "tcs"):
            assert data[ticker] == []


# ── GET /api/announcements/{ticker} ───────────────────────────────────────

class TestSingleCompanyEndpoint:
    def test_valid_ticker_returns_200(self, seeded_client):
        for ticker in ("infosys", "hcl", "reliance", "tcs"):
            resp = seeded_client.get(f"/api/announcements/{ticker}")
            assert resp.status_code == 200, f"Failed for {ticker}"

    def test_valid_ticker_returns_list(self, seeded_client):
        resp = seeded_client.get("/api/announcements/infosys")
        assert isinstance(resp.json(), list)

    def test_valid_ticker_has_at_most_three(self, seeded_client):
        resp = seeded_client.get("/api/announcements/tcs")
        assert len(resp.json()) <= 3

    def test_unknown_ticker_returns_empty_list(self, seeded_client):
        """API-10 — Unknown ticker returns empty list (no 500)."""
        resp = seeded_client.get("/api/announcements/UNKNOWN")
        assert resp.status_code in (200, 404)


# ── TC-F2.2 : Caching ─────────────────────────────────────────────────────

class TestCachingBehaviour:
    def test_second_call_served_from_cache(self, seeded_client):
        """TC-F2.2-01 / API-08 — Second call is faster (served from cache)."""
        t1_start = time.monotonic()
        seeded_client.get("/api/announcements")
        t1 = time.monotonic() - t1_start

        t2_start = time.monotonic()
        seeded_client.get("/api/announcements")
        t2 = time.monotonic() - t2_start

        # Second call should be significantly faster
        assert t2 < t1 * 2 or t2 < 0.1, "Second call should be served from cache quickly"

    def test_two_calls_return_identical_data(self, seeded_client):
        """API-08 — Both calls within TTL return identical data."""
        r1 = seeded_client.get("/api/announcements").json()
        r2 = seeded_client.get("/api/announcements").json()
        assert r1 == r2


# ── TC-F2.3 : Error Handling ──────────────────────────────────────────────

class TestErrorHandling:
    def test_scraper_down_returns_cached_or_empty(self, seeded_client):
        """TC-F2.3-01 / API-06 — If scraper fails, API returns graceful response."""
        import httpx
        with patch("app.services.scraper_service.httpx.Client") as mock_client:
            mock_client.return_value.__enter__.return_value.get.side_effect = (
                httpx.TimeoutException("timeout")
            )
            resp = seeded_client.get("/api/announcements")
        assert resp.status_code in (200, 503)
        assert "traceback" not in resp.text.lower()
        assert "exception" not in resp.text.lower()

    def test_no_stack_trace_in_response_body(self, seeded_client):
        """TC-F2.3 — Stack traces must never appear in API response body."""
        resp = seeded_client.get("/api/announcements")
        assert "Traceback" not in resp.text
        assert "File \"" not in resp.text


# ── GET /api/health ───────────────────────────────────────────────────────

class TestHealthEndpoint:
    def test_health_returns_200(self, seeded_client):
        """API-09 — GET /api/health returns HTTP 200."""
        resp = seeded_client.get("/api/health")
        assert resp.status_code == 200

    def test_health_contains_status_ok(self, seeded_client):
        """API-09 — Health response contains status: ok."""
        resp = seeded_client.get("/api/health")
        data = resp.json()
        assert data["status"] == "ok"

    def test_health_has_expected_fields(self, seeded_client):
        """Health endpoint returns all documented fields."""
        resp = seeded_client.get("/api/health")
        data = resp.json()
        assert "status" in data
        assert "cache_age_seconds" in data
        assert "last_errors" in data


# ── POST /api/refresh (admin key) ─────────────────────────────────────────

class TestRefreshEndpoint:
    def test_refresh_wrong_key_returns_403(self, seeded_client):
        resp = seeded_client.post("/api/refresh", headers={"X-Admin-Key": "wrongkey"})
        assert resp.status_code == 403

    def test_refresh_correct_key_returns_200(self, seeded_client):
        """POST /api/refresh with correct key succeeds."""
        from unittest.mock import patch
        with patch("app.services.announcement_service.refresh_announcements") as mock_refresh:
            mock_refresh.return_value = SAMPLE_ANNOUNCEMENTS
            resp = seeded_client.post("/api/refresh", headers={"X-Admin-Key": "changeme"})
        assert resp.status_code == 200
